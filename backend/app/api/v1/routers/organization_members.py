from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user, RequireOrganizer
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse

# We can nest this under the /organizations prefix during registry, or handle it here
router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "/organizations/{organizationId}/members",
    response_model=PaginatedResponse[dict],
    summary="List members in an organization",
)
async def list_organization_members(organizationId: str, params: PaginationParams = Depends()):
    """Retrieves a paginated list of all users joined as members of an organization workspace."""
    return {
        "success": True,
        "message": f"Members of organization {organizationId} retrieved",
        "data": {
            "items": [{"userId": "mock_user_uuid", "role": "editor", "joinedAt": "2026-06-25T23:00:00"}],
            "pagination": {
                "totalRecords": 1,
                "totalPages": 1,
                "currentPage": params.page,
                "pageSize": params.pageSize,
            },
        },
    }


@router.post(
    "/organizations/{organizationId}/members",
    response_model=APIResponse[dict],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RequireOrganizer)],
    summary="Add a member to the organization",
)
async def add_organization_member(organizationId: str):
    """Associates a platform user account to an organization with custom role attributes."""
    return {
        "success": True,
        "message": "User added to organization members",
        "data": {"organizationId": organizationId, "userId": "mock_user_uuid", "role": "viewer"},
    }


@router.delete(
    "/organizations/{organizationId}/members/{userId}",
    response_model=APIResponse[None],
    dependencies=[Depends(RequireOrganizer)],
    summary="Remove member from the organization",
)
async def remove_organization_member(organizationId: str, userId: str):
    """Deletes an organizational membership association."""
    return {
        "success": True,
        "message": f"User {userId} successfully removed from organization {organizationId}",
        "data": None,
    }
