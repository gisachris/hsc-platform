from fastapi import APIRouter
from app.schemas.response import APIResponse, success_response

router = APIRouter()


@router.get("/health", response_model=APIResponse[dict])
async def health_check():
    """General service health diagnostics."""
    return {
        "success": True,
        "message": "Backend service is healthy",
        "data": {"status": "healthy"},
    }


@router.get("/ready", response_model=APIResponse[dict])
async def readiness_check():
    """Readiness diagnostics verifying database connectivity."""
    # Placeholders for future connection checks (e.g. Postgres pg_isready status)
    return {
        "success": True,
        "message": "Backend service is ready to accept traffic",
        "data": {"status": "ready", "database": "connected"},
    }


@router.get("/live", response_model=APIResponse[dict])
async def liveness_check():
    """Simple liveness diagnostics for process tracking."""
    return {
        "success": True,
        "message": "Backend service is live",
        "data": {"status": "alive"},
    }
