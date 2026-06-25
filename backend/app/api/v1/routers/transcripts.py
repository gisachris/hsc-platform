from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user, RequireModerator
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginationParams, PaginatedResponse

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "",
    response_model=PaginatedResponse[dict],
    summary="List speech transcripts",
)
async def list_transcripts(params: PaginationParams = Depends()):
    """Retrieves a paginated listing of all speech-to-text transcript records."""
    return {
        "success": True,
        "message": "Transcripts list retrieved",
        "data": {
            "items": [{"id": "mock_trans_uuid", "sessionId": "mock_session_uuid", "language": "en"}],
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
    summary="Trigger transcription job",
)
async def create_transcript():
    """Triggers an asynchronous AI transcription task on a finished audio recording."""
    return {
        "success": True,
        "message": "AI transcription job triggered successfully",
        "data": {"id": "new_trans_uuid", "status": "processing"},
    }


@router.get(
    "/{id}",
    response_model=APIResponse[dict],
    summary="Get transcript text by ID",
)
async def get_transcript(id: str):
    """Fetches full generated text and speaker segment pings of a transcript."""
    return {
        "success": True,
        "message": "Transcript details retrieved",
        "data": {"id": id, "status": "completed", "content": "Welcome to the hybrid conference..."},
    }
