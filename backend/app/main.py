from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.exceptions import register_exception_handlers
from app.api.v1.middlewares import RequestLoggingMiddleware
from app.api.v1.middlewares.security import SecurityAndRequestIdMiddleware
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging

# Setup centralized logging
setup_logging()

# Configure a professional OpenAPI specification
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
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    debug=settings.DEBUG,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

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


@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs": f"{settings.API_V1_STR}/docs",
    }
