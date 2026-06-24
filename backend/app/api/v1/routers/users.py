from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user, RequireAdmin
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "",
    response_model=PaginatedResponse[dict],
    summary="Retrieve users list",
)
async def list_users(params: PaginationParams = Depends()):
    """Retrieves a paginated, filterable directory of platform users."""
    return {
        "success": True,
        "message": "Users list retrieved successfully",
        "data": {
            "items": [{"id": "mock_user_uuid", "email": "user@example.com", "role": "attendee"}],
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
    dependencies=[Depends(RequireAdmin)],
    summary="Create a new user profile",
)
async def create_user():
    """Allows administrators to directly provision new user profiles."""
    return {
        "success": True,
        "message": "User profile created successfully",
        "data": {"id": "new_user_uuid", "email": "new_user@example.com"},
    }


@router.get(
    "/{id}",
    response_model=APIResponse[dict],
    summary="Get user details by ID",
)
async def get_user(id: str):
    """Fetches detailed user account and profile metadata."""
    return {
        "success": True,
        "message": "User details retrieved",
        "data": {"id": id, "email": "user@example.com", "role": "attendee"},
    }


@router.patch(
    "/{id}",
    response_model=APIResponse[dict],
    summary="Modify user profile properties",
)
async def update_user(id: str):
    """Applies patch modifications to user profile data fields."""
    return {
        "success": True,
        "message": "User profile updated successfully",
        "data": {"id": id, "email": "user@example.com", "status": "updated"},
    }


@router.delete(
    "/{id}",
    response_model=APIResponse[None],
    dependencies=[Depends(RequireAdmin)],
    summary="Deactivate or delete user account",
)
async def delete_user(id: str):
    """Disables user account access and flags the record for deletion."""
    return {
        "success": True,
        "message": f"User account {id} successfully deleted",
        "data": None,
    }
