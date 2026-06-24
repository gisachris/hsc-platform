from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user, RequireOrganizer
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "",
    response_model=PaginatedResponse[dict],
    summary="List event registrations",
)
async def list_registrations(params: PaginationParams = Depends()):
    """Retrieves a paginated listing of ticketing orders and registrations."""
    return {
        "success": True,
        "message": "Registrations retrieved successfully",
        "data": {
            "items": [{"id": "mock_reg_uuid", "eventId": "mock_event_uuid", "status": "pending"}],
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
    summary="Submit event ticket registration",
)
async def create_registration():
    """Places a new ticket order request for a conference event."""
    return {
        "success": True,
        "message": "Registration submitted successfully",
        "data": {"id": "new_reg_uuid", "eventId": "mock_event_uuid", "status": "pending"},
    }


@router.get(
    "/{id}",
    response_model=APIResponse[dict],
    summary="Get registration details by ID",
)
async def get_registration(id: str):
    """Fetches details of a ticketing order registration."""
    return {
        "success": True,
        "message": "Registration details retrieved",
        "data": {"id": id, "eventId": "mock_event_uuid", "status": "pending"},
    }


@router.delete(
    "/{id}",
    response_model=APIResponse[None],
    summary="Cancel ticket registration",
)
async def delete_registration(id: str):
    """Cancels ticket orders and returns seats to availability pools."""
    return {
        "success": True,
        "message": f"Registration {id} has been successfully cancelled",
        "data": None,
    }


# Action Endpoints
@router.post(
    "/{id}/approve",
    response_model=APIResponse[dict],
    dependencies=[Depends(RequireOrganizer)],
    summary="Approve pending ticket registration",
)
async def approve_registration(id: str):
    """Action Endpoint: Approves a registration request and dispatches ticket barcodes."""
    return {
        "success": True,
        "message": f"Registration {id} has been approved",
        "data": {"id": id, "status": "approved"},
    }


@router.post(
    "/{id}/reject",
    response_model=APIResponse[dict],
    dependencies=[Depends(RequireOrganizer)],
    summary="Reject pending ticket registration",
)
async def reject_registration(id: str):
    """Action Endpoint: Rejects a registration request and releases reserved slots."""
    return {
        "success": True,
        "message": f"Registration {id} has been rejected",
        "data": {"id": id, "status": "rejected"},
    }
