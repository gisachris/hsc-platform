from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user, RequireModerator
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "",
    response_model=PaginatedResponse[dict],
    summary="List session summaries",
)
async def list_summaries(params: PaginationParams = Depends()):
    """Retrieves a paginated list of all generated session summaries and key takeaways."""
    return {
        "success": True,
        "message": "Summaries list retrieved",
        "data": {
            "items": [{"id": "mock_sum_uuid", "sessionId": "mock_session_uuid", "format": "bullets"}],
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
    dependencies=[Depends(RequireModerator)],
    summary="Trigger AI summary generation",
)
async def create_summary():
    """Starts an asynchronous AI pipeline to summarize a transcript and extract action items."""
    return {
        "success": True,
        "message": "AI summary task dispatched successfully",
        "data": {"id": "new_sum_uuid", "status": "processing"},
    }


@router.get(
    "/{id}",
    response_model=APIResponse[dict],
    summary="Get summary by ID",
)
async def get_summary(id: str):
    """Retrieves full text layout and bullet-point tasks list of a session summary."""
    return {
        "success": True,
        "message": "Summary details retrieved",
        "data": {
            "id": id,
            "status": "completed",
            "takeaways": ["Introduced V2 blueprints", "Migrated dependencies to Poetry"],
        },
    }
