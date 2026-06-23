from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.exceptions import register_exception_handlers
from app.api.v1.middlewares import RequestLoggingMiddleware
from app.api.v1.routers import api_router
from app.core.config import settings
from app.core.logging import setup_logging

# Setup centralized logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    debug=settings.DEBUG,
)

# CORS middleware config
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).rstrip("/") for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Request logger and process time instrumentation
app.add_middleware(RequestLoggingMiddleware)

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
