from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user, RequireOrganizer
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "",
    response_model=PaginatedResponse[dict],
    summary="List event invitations",
)
async def list_invitations(params: PaginationParams = Depends()):
    """Retrieves a paginated listing of speaker and VIP invitations."""
    return {
        "success": True,
        "message": "Invitations retrieved successfully",
        "data": {
            "items": [{"id": "mock_invite_uuid", "email": "speaker@example.com", "status": "pending"}],
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
    dependencies=[Depends(RequireOrganizer)],
    summary="Dispatch a new invitation",
)
async def create_invitation():
    """Generates an invitation passcode and dispatches secure sign-up links."""
    return {
        "success": True,
        "message": "Invitation sent successfully",
        "data": {"id": "new_invite_uuid", "email": "speaker@example.com", "status": "pending"},
    }


@router.get(
    "/{id}",
    response_model=APIResponse[dict],
    summary="Get invitation details by ID",
)
async def get_invitation(id: str):
    """Fetches lifecycle records and roles parameters of an invitation."""
    return {
        "success": True,
        "message": "Invitation details retrieved",
        "data": {"id": id, "email": "speaker@example.com", "status": "pending"},
    }


@router.delete(
    "/{id}",
    response_model=APIResponse[None],
    dependencies=[Depends(RequireOrganizer)],
    summary="Revoke an invitation",
)
async def delete_invitation(id: str):
    """Cancels and invalidates an outstanding invitation link."""
    return {
        "success": True,
        "message": f"Invitation {id} successfully revoked",
        "data": None,
    }
