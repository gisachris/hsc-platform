from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.exceptions import register_exception_handlers
from app.api.v1.middlewares import RequestLoggingMiddleware
from app.api.v1.middlewares.security import SecurityAndRequestIdMiddleware
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging

# Setup centralized logging
setup_logging()

# Static assets directory (swagger-ui files bundled locally)
STATIC_DIR = Path(__file__).parent / "static"

# Configure a professional OpenAPI specification
# docs_url/redoc_url are disabled so we can serve assets from local static files
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "Production-quality REST API contract for the Smart Hybrid Conference "
        "Management Platform, providing modular orchestration for scheduling, streaming, "
        "ticketing, and AI summarization services."
    ),
    version="1.0.0",
    contact={
        "name": "SHC Platform Engineering Team",
        "email": "engineering@conference-platform.com",
    },
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=None,    # Disabled — served manually below with local assets
    redoc_url=None,   # Disabled — served manually below with local assets
    debug=settings.DEBUG,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

# Mount local static directory (swagger-ui JS/CSS bundled here)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# 1. CORS middleware config
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).rstrip("/") for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 2. Request logger and process time instrumentation
app.add_middleware(RequestLoggingMiddleware)

# 3. Security and Request ID instrumentation
app.add_middleware(SecurityAndRequestIdMiddleware)

# Centralized exception handlers registration
register_exception_handlers(app)

# Include core api v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)


# ── Self-hosted docs endpoints ──────────────────────────────────────────────

@app.get(f"{settings.API_V1_STR}/docs", include_in_schema=False)
async def swagger_ui() -> HTMLResponse:
    """Swagger UI served from locally bundled assets (no CDN dependency)."""
    return get_swagger_ui_html(
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        title=f"{settings.PROJECT_NAME} — Swagger UI",
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
        swagger_favicon_url="/static/swagger-ui/favicon.png",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    )


@app.get(f"{settings.API_V1_STR}/redoc", include_in_schema=False)
async def redoc_ui() -> HTMLResponse:
    """ReDoc UI served from locally bundled assets (no CDN dependency)."""
    return get_redoc_html(
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        title=f"{settings.PROJECT_NAME} — ReDoc",
        redoc_favicon_url="/static/swagger-ui/favicon.png",
    )


@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs": f"{settings.API_V1_STR}/docs",
        "redoc": f"{settings.API_V1_STR}/redoc",
    }
