from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user, RequireModerator
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "",
    response_model=PaginatedResponse[dict],
    summary="List Q&A questions",
)
async def list_questions(params: PaginationParams = Depends()):
    """Retrieves a paginated listing of all questions asked across active tracks."""
    return {
        "success": True,
        "message": "Questions retrieved successfully",
        "data": {
            "items": [{"id": "mock_quest_uuid", "text": "Is this recorded?", "upvotes": 5}],
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
    summary="Submit a new question",
)
async def create_question():
    """Appends a new audience question to the active session board."""
    return {
        "success": True,
        "message": "Question posted successfully",
        "data": {"id": "new_quest_uuid", "text": "Is this recorded?", "upvotes": 0},
    }


@router.get(
    "/{id}",
    response_model=APIResponse[dict],
    summary="Get question by ID",
)
async def get_question(id: str):
    """Fetches details of a Q&A question."""
    return {
        "success": True,
        "message": "Question details retrieved",
        "data": {"id": id, "text": "Is this recorded?", "upvotes": 5},
    }


@router.patch(
    "/{id}",
    response_model=APIResponse[dict],
    summary="Modify question content or upvotes",
)
async def update_question(id: str):
    """Updates question details, upvote tallies, or approval flags."""
    return {
        "success": True,
        "message": "Question updated successfully",
        "data": {"id": id, "upvotes": 6},
    }


@router.delete(
    "/{id}",
    response_model=APIResponse[None],
    dependencies=[Depends(RequireModerator)],
    summary="Remove audience question",
)
async def delete_question(id: str):
    """Deletes or hides an audience question from presentation boards."""
    return {
        "success": True,
        "message": f"Question {id} successfully removed",
        "data": None,
    }
