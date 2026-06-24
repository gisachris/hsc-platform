from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user, RequireModerator
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "",
    response_model=PaginatedResponse[dict],
    summary="List engagement polls",
)
async def list_polls(params: PaginationParams = Depends()):
    """Retrieves a paginated listing of all configured engagement polls."""
    return {
        "success": True,
        "message": "Polls list retrieved",
        "data": {
            "items": [{"id": "mock_poll_uuid", "question": "Rate the session", "status": "active"}],
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
    summary="Configure a new poll",
)
async def create_poll():
    """Adds a new multiple-choice question poll config to a session."""
    return {
        "success": True,
        "message": "Poll configured successfully",
        "data": {"id": "new_poll_uuid", "question": "Rate the session", "status": "draft"},
    }


@router.get(
    "/{id}",
    response_model=APIResponse[dict],
    summary="Get poll details and tallies",
)
async def get_poll(id: str):
    """Fetches diagnostic tallies and choice selections of a poll."""
    return {
        "success": True,
        "message": "Poll details retrieved",
        "data": {"id": id, "question": "Rate the session", "status": "active", "results": {"good": 10, "bad": 1}},
    }


@router.patch(
    "/{id}",
    response_model=APIResponse[dict],
    dependencies=[Depends(RequireModerator)],
    summary="Update poll choices or state",
)
async def update_poll(id: str):
    """Updates poll question properties or transitions states (e.g. active to closed)."""
    return {
        "success": True,
        "message": "Poll updated successfully",
        "data": {"id": id, "status": "closed"},
    }


@router.delete(
    "/{id}",
    response_model=APIResponse[None],
    dependencies=[Depends(RequireModerator)],
    summary="Purge a poll configuration",
)
async def delete_poll(id: str):
    """Permanently deletes a poll and its associated results from databases."""
    return {
        "success": True,
        "message": f"Poll {id} successfully deleted",
        "data": None,
    }
