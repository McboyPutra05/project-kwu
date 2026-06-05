"""
api/routes/users.py

Route untuk manajemen user (hanya untuk admin dashboard).
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies.auth import get_current_admin
from models.admin import Admin
from repositories.user_repository import UserRepository
from schemas.common import PaginatedResponse
from schemas.user import UserResponse, UserUpdate
from services.user_service import UserService

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
    dependencies=[Depends(get_current_admin)],  # Semua route butuh auth
)

# Dependency injection sederhana
def get_user_service() -> UserService:
    return UserService(UserRepository())


@router.get(
    "",
    response_model=PaginatedResponse[UserResponse],
    summary="List All Users",
    description="Dapatkan daftar semua pengguna chatbot dengan pagination.",
)
async def list_users(
    page: int = Query(default=1, ge=1, description="Nomor halaman"),
    limit: int = Query(default=20, ge=1, le=100, description="Item per halaman"),
    service: UserService = Depends(get_user_service),
) -> PaginatedResponse[UserResponse]:
    """Daftar semua user yang terdaftar di chatbot."""
    return await service.list_users(page=page, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get User Detail",
    description="Dapatkan detail satu user berdasarkan ID.",
)
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Detail satu user."""
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User dengan ID {user_id} tidak ditemukan",
        )

    return UserResponse(
        id=str(user.id),
        phone_number=user.phone_number,
        name=user.name,
        is_active=user.is_active,
        session_state=user.session_state,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update User",
    description="Update data user (nama, status aktif).",
)
async def update_user(
    user_id: str,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Update data user."""
    updated = await service.update_user(user_id, data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User dengan ID {user_id} tidak ditemukan",
        )
    return updated
