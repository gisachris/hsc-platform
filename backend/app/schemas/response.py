from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = ""
    data: Optional[T] = None
    errors: Optional[Any] = None


def success_response(
    data: Optional[T] = None, message: str = "Operation successful"
) -> APIResponse[T]:
    return APIResponse(success=True, message=message, data=data, errors=None)


def error_response(
    errors: Any = None, message: str = "Operation failed"
) -> APIResponse[None]:
    return APIResponse(success=False, message=message, data=None, errors=errors)
