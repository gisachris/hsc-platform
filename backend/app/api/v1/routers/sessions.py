from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user, RequireOrganizer, RequireSpeaker
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "",
    response_model=PaginatedResponse[dict],
    summary="Retrieve agenda sessions",
)
async def list_sessions(params: PaginationParams = Depends()):
    """Retrieves a paginated directory of agenda tracks and presentations."""
    return {
        "success": True,
        "message": "Sessions retrieved successfully",
        "data": {
            "items": [{"id": "mock_session_uuid", "title": "Keynote Speech", "status": "scheduled"}],
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
    summary="Create a new presentation session",
)
async def create_session():
    """Defines a session slot in the conference calendar."""
    return {
        "success": True,
        "message": "Session created successfully",
        "data": {"id": "new_session_uuid", "title": "New Panel Discussion", "status": "scheduled"},
    }


@router.get(
    "/{id}",
    response_model=APIResponse[dict],
    summary="Get session details by ID",
)
async def get_session(id: str):
    """Fetches details, speaker profiles, and track locations of a session."""
    return {
        "success": True,
        "message": "Session details retrieved",
        "data": {"id": id, "title": "Keynote Speech", "status": "scheduled"},
    }


@router.patch(
    "/{id}",
    response_model=APIResponse[dict],
    dependencies=[Depends(RequireOrganizer)],
    summary="Update session schedule settings",
)
async def update_session(id: str):
    """Edits track durations, time boundaries, or speaker allocations."""
    return {
        "success": True,
        "message": "Session updated successfully",
        "data": {"id": id, "title": "Keynote Speech", "status": "updated"},
    }


@router.delete(
    "/{id}",
    response_model=APIResponse[None],
    dependencies=[Depends(RequireOrganizer)],
    summary="Delete a session track",
)
async def delete_session(id: str):
    """Removes a session track from the agenda schedule."""
    return {
        "success": True,
        "message": f"Session {id} successfully deleted",
        "data": None,
    }


# Action Endpoints
@router.post(
    "/{id}/start",
    response_model=APIResponse[dict],
    dependencies=[Depends(RequireSpeaker)],
    summary="Start broadcasting session",
)
async def start_session(id: str):
    """Action Endpoint: Commences live broadcasting, opens chat widgets, and starts recording."""
    return {
        "success": True,
        "message": f"Session {id} has started broadcasting",
        "data": {"id": id, "status": "live"},
    }


@router.post(
    "/{id}/end",
    response_model=APIResponse[dict],
    dependencies=[Depends(RequireSpeaker)],
    summary="End session broadcast",
)
async def end_session(id: str):
    """Action Endpoint: Stops video feeds, compiles live chats, and closes interactive dashboards."""
    return {
        "success": True,
        "message": f"Session {id} has successfully concluded",
        "data": {"id": id, "status": "ended"},
    }


# Nested Resources
@router.get(
    "/{sessionId}/questions",
    response_model=PaginatedResponse[dict],
    summary="Retrieve questions asked during a session",
)
async def list_session_questions(sessionId: str, params: PaginationParams = Depends()):
    """Nested Resource: Retrieves all audience Q&A questions asked during a session."""
    return {
        "success": True,
        "message": f"Questions for session {sessionId} retrieved",
        "data": {
            "items": [{"id": "mock_question_uuid", "text": "What is the timeline for roll-out?", "sessionId": sessionId}],
            "pagination": {
                "totalRecords": 1,
                "totalPages": 1,
                "currentPage": params.page,
                "pageSize": params.pageSize,
            },
        },
    }


@router.get(
    "/{sessionId}/polls",
    response_model=PaginatedResponse[dict],
    summary="Retrieve interactive polls run in a session",
)
async def list_session_polls(sessionId: str, params: PaginationParams = Depends()):
    """Nested Resource: Retrieves all engagement polls configured for a session."""
    return {
        "success": True,
        "message": f"Polls for session {sessionId} retrieved",
        "data": {
            "items": [{"id": "mock_poll_uuid", "question": "Are you ready for V2?", "sessionId": sessionId}],
            "pagination": {
                "totalRecords": 1,
                "totalPages": 1,
                "currentPage": params.page,
                "pageSize": params.pageSize,
            },
        },
    }
