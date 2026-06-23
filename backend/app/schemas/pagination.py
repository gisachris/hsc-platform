from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field, conint
from app.schemas.response import ResponseMeta

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Current page number (1-indexed)")
    pageSize: int = Field(
        10, ge=1, le=100, description="Number of items per page"
    )
    sort: Optional[str] = Field(None, description="Field name to sort by")
    order: str = Field(
        "asc", pattern="^(asc|desc)$", description="Sort direction: asc or desc"
    )
    search: Optional[str] = Field(
        None, description="Search query string for filtering"
    )


class PaginationMeta(BaseModel):
    totalRecords: int = Field(..., description="Total count of matching records")
    totalPages: int = Field(..., description="Total pages available")
    currentPage: int = Field(..., description="Current active page")
    pageSize: int = Field(..., description="Limit size of page records")


class PaginatedData(BaseModel, Generic[T]):
    items: List[T] = Field(..., description="List of paginated records")
    pagination: PaginationMeta = Field(..., description="Pagination metadata properties")


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = Field(True, description="Indicates operation success")
    message: str = Field("", description="Response status message")
    data: PaginatedData[T] = Field(..., description="Paginated data payload")
    errors: Optional[List[str]] = Field(None, description="Detailed errors")
    meta: Optional[ResponseMeta] = Field(
        None, description="Request tracking metadata"
    )
