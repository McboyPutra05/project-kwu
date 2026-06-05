"""
services/auth_service.py

Business logic untuk autentikasi admin dashboard.
"""

from typing import Optional

from loguru import logger

from core.config import settings
from core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_token,
)
from models.admin import Admin
from schemas.auth import AdminCreateRequest, AdminResponse, TokenResponse


class AuthService:
    """
    Service untuk autentikasi dan manajemen akun admin.
    """

    async def login(self, username: str, password: str) -> Optional[TokenResponse]:
        """
        Login admin dengan username dan password.

        Returns:
            TokenResponse jika berhasil, None jika gagal.
        """
        # Cari admin berdasarkan username
        admin = await Admin.find_one(Admin.username == username)

        if not admin:
            logger.warning(f"🔒 Login failed: user not found | username={username}")
            return None

        if not admin.is_active:
            logger.warning(f"🔒 Login failed: account disabled | username={username}")
            return None

        # Verifikasi password
        if not verify_password(password, admin.hashed_password):
            logger.warning(f"🔒 Login failed: wrong password | username={username}")
            return None

        # Buat tokens
        access_token = create_access_token(data={"sub": admin.username})
        refresh_token = create_refresh_token(data={"sub": admin.username})

        logger.info(f"✅ Admin logged in: {username}")

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.jwt_access_token_expire_minutes * 60,
        )

    async def refresh_access_token(self, refresh_token: str) -> Optional[TokenResponse]:
        """
        Buat access token baru menggunakan refresh token.
        """
        username = verify_token(refresh_token, token_type="refresh")
        if not username:
            return None

        # Pastikan admin masih aktif
        admin = await Admin.find_one(Admin.username == username)
        if not admin or not admin.is_active:
            return None

        new_access_token = create_access_token(data={"sub": username})
        new_refresh_token = create_refresh_token(data={"sub": username})

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.jwt_access_token_expire_minutes * 60,
        )

    async def create_admin(self, data: AdminCreateRequest) -> AdminResponse:
        """
        Buat akun admin baru.
        Dipanggil dari script create_admin.py atau endpoint protected.
        """
        # Cek username sudah ada
        existing = await Admin.find_one(Admin.username == data.username)
        if existing:
            raise ValueError(f"Username '{data.username}' sudah digunakan")

        # Buat admin baru
        admin = Admin(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
        )
        await admin.insert()

        logger.info(f"👤 Admin account created: {data.username}")

        return AdminResponse(
            id=str(admin.id),
            username=admin.username,
            email=admin.email,
            is_active=admin.is_active,
            created_at=admin.created_at.isoformat(),
        )

    async def get_admin_by_username(self, username: str) -> Optional[Admin]:
        """Cari admin berdasarkan username (untuk dependency injection)."""
        return await Admin.find_one(Admin.username == username)
