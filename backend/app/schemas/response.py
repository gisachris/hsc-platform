from datetime import datetime, timezone
from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class ResponseMeta(BaseModel):
    requestId: str = Field(..., description="Unique Request identifier UUID")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp",
    )


class APIResponse(BaseModel, Generic[T]):
    success: bool = Field(True, description="Indicates if the operation was successful")
    message: str = Field("", description="Human-readable response message")
    data: Optional[T] = Field(None, description="Response payload data")
    errors: Optional[List[Any]] = Field(None, description="List of errors if failed")
    meta: Optional[ResponseMeta] = Field(
        None, description="Response tracking metadata"
    )


def success_response(
    data: Optional[T] = None, message: str = "Operation successful"
) -> APIResponse[T]:
    return APIResponse(success=True, message=message, data=data, errors=None)


def error_response(
    errors: Optional[List[Any]] = None, message: str = "Operation failed"
) -> APIResponse[None]:
    return APIResponse(success=False, message=message, data=None, errors=errors)

