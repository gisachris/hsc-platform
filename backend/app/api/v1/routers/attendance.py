from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user, RequireModerator
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "",
    response_model=PaginatedResponse[dict],
    summary="List attendance logs",
)
async def list_attendance(params: PaginationParams = Depends()):
    """Retrieves a paginated listing of user check-in and session attendance logs."""
    return {
        "success": True,
        "message": "Attendance records retrieved",
        "data": {
            "items": [{"id": "mock_attend_uuid", "userId": "mock_user_uuid", "sessionId": "mock_session_uuid"}],
            "pagination": {
                "totalRecords": 1,
                "totalPages": 1,
                "currentPage": params.page,
                "pageSize": params.pageSize,
            },
        },
    }


@router.post(
    "",
    response_model=APIResponse[dict],
    status_code=status.HTTP_201_CREATED,
    summary="Record a check-in action",
)
async def create_attendance():
    """Logs a user check-in or engagement ping inside a physical or virtual session."""
    return {
        "success": True,
        "message": "Attendance check-in logged successfully",
        "data": {"id": "new_attend_uuid", "userId": "mock_user_uuid", "status": "present"},
    }


@router.get(
    "/{id}",
    response_model=APIResponse[dict],
    summary="Get attendance log by ID",
)
async def get_attendance(id: str):
    """Fetches diagnostic check-in timelines for a specific log record."""
    return {
        "success": True,
        "message": "Attendance record details retrieved",
        "data": {"id": id, "userId": "mock_user_uuid", "status": "present"},
    }
