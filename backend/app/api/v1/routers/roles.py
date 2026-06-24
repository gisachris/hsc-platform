from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user, RequireAdmin
from app.schemas.response import APIResponse

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "",
    response_model=APIResponse[list],
    summary="List all security roles",
)
async def list_roles():
    """Returns all security access control roles defined within the platform."""
    return {
        "success": True,
        "message": "Roles list retrieved",
        "data": [
            {"id": "role_admin", "name": "Admin", "permissions": ["*"]},
            {"id": "role_organizer", "name": "Organizer", "permissions": ["events:write", "sessions:write"]},
        ],
    }


@router.post(
    "",
    response_model=APIResponse[dict],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RequireAdmin)],
    summary="Create a custom security role",
)
async def create_role():
    """Defines a new platform security role with specific permissions scopes."""
    return {
        "success": True,
        "message": "Role created successfully",
        "data": {"id": "role_custom", "name": "Custom Role"},
    }


@router.delete(
    "/{id}",
    response_model=APIResponse[None],
    dependencies=[Depends(RequireAdmin)],
    summary="Remove a security role",
)
async def delete_role(id: str):
    """Deletes a custom security role from the system."""
    return {
        "success": True,
        "message": f"Role {id} successfully removed",
        "data": None,
    }
