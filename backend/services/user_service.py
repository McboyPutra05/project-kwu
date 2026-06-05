"""
services/user_service.py

Business logic untuk manajemen User.
Menjadi perantara antara route/chatbot dan UserRepository.
"""

from typing import Optional, Tuple

from loguru import logger

from models.user import User
from repositories.user_repository import UserRepository
from schemas.common import PaginatedResponse
from schemas.user import UserResponse, UserUpdate


class UserService:
    """
    Service untuk manajemen user chatbot.

    Semua business logic user ada di sini.
    Route hanya memanggil method dari service ini.
    """

    def __init__(self, repository: UserRepository) -> None:
        self._repo = repository

    async def get_or_create_user(
        self,
        phone_number: str,
        name: Optional[str] = None,
    ) -> Tuple[User, bool]:
        """
        Dapatkan atau buat user baru berdasarkan nomor telepon.

        Dipanggil setiap kali ada pesan masuk dari WhatsApp.

        Returns:
            Tuple (user, is_new_user)
        """
        user, is_created = await self._repo.get_or_create_by_phone(
            phone_number=phone_number,
            name=name,
        )

        if is_created:
            logger.info(f"👤 New user registered: {phone_number}")

        return user, is_created

    async def get_user_by_phone(self, phone_number: str) -> Optional[User]:
        """Cari user berdasarkan nomor telepon."""
        return await self._repo.find_by_phone(phone_number)

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Cari user berdasarkan ID."""
        return await self._repo.find_by_id(user_id)

    async def list_users(
        self,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedResponse[UserResponse]:
        """
        Ambil semua user dengan pagination (untuk admin dashboard).
        """
        skip = (page - 1) * limit
        users = await self._repo.find_all(skip=skip, limit=limit)
        total = await self._repo.count_all()

        user_responses = []
        for u in users:
            user_responses.append(
                UserResponse(
                    id=str(u.id),
                    phone_number=u.phone_number,
                    name=u.name,
                    is_active=u.is_active,
                    session_state=u.session_state,
                    created_at=u.created_at,
                    updated_at=u.updated_at,
                )
            )

        return PaginatedResponse.create(
            items=user_responses,
            total=total,
            page=page,
            limit=limit,
        )

    async def update_user(
        self, user_id: str, data: UserUpdate
    ) -> Optional[UserResponse]:
        """Update data user."""
        user = await self._repo.find_by_id(user_id)
        if not user:
            return None

        if data.name is not None:
            user.name = data.name
        if data.is_active is not None:
            user.is_active = data.is_active

        user.update_timestamp()
        updated = await self._repo.update(user)

        return UserResponse(
            id=str(updated.id),
            phone_number=updated.phone_number,
            name=updated.name,
            is_active=updated.is_active,
            session_state=updated.session_state,
            created_at=updated.created_at,
            updated_at=updated.updated_at,
        )

    async def get_total_users(self) -> int:
        """Hitung total user terdaftar."""
        return await self._repo.count_all()

    async def get_active_users_today(self) -> int:
        """Hitung user aktif hari ini."""
        return await self._repo.count_active_today()
