from fastapi import APIRouter
from app.schemas.response import APIResponse, success_response

router = APIRouter()


@router.get("/health", response_model=APIResponse[dict])
async def health_check():
    return success_response(
        data={"status": "healthy", "service": "backend"},
        message="Backend service is fully functional",
    )
