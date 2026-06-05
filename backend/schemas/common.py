"""
schemas/common.py

Schema umum yang digunakan di seluruh aplikasi:
- Pagination
- Standard API response
- Error response
"""

from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

# Generic type untuk data payload
T = TypeVar("T")


class PaginationParams(BaseModel):
    """Parameter untuk pagination request."""
    page: int = Field(default=1, ge=1, description="Nomor halaman (mulai dari 1)")
    limit: int = Field(default=20, ge=1, le=100, description="Jumlah item per halaman")

    @property
    def skip(self) -> int:
        """Hitung offset untuk MongoDB query."""
        return (self.page - 1) * self.limit


class PaginatedResponse(BaseModel, Generic[T]):
    """Response wrapper untuk data yang di-paginate."""
    items: List[T]
    total: int
    page: int
    limit: int
    total_pages: int

    @classmethod
    def create(cls, items: List[T], total: int, page: int, limit: int) -> "PaginatedResponse[T]":
        total_pages = (total + limit - 1) // limit  # ceiling division
        return cls(
            items=items,
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
        )


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""
    success: bool = True
    message: str = "OK"
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    message: str
    detail: Optional[Any] = None
