"""
api/routes/auth.py

Route untuk autentikasi admin dashboard.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from models.admin import Admin
from api.dependencies.auth import get_current_admin
from schemas.auth import (
    AdminResponse,
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
)
from services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

auth_service = AuthService()


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Admin Login",
    description="Login dengan username dan password untuk mendapatkan JWT token.",
)
async def login(request: LoginRequest) -> TokenResponse:
    """
    Login admin dashboard.
    
    Kembalikan access_token (30 menit) dan refresh_token (7 hari).
    Gunakan access_token di header: `Authorization: Bearer <token>`
    """
    token = await auth_service.login(
        username=request.username,
        password=request.password,
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh Token",
    description="Dapatkan access token baru menggunakan refresh token.",
)
async def refresh_token(request: RefreshTokenRequest) -> TokenResponse:
    """
    Refresh access token menggunakan refresh token yang masih valid.
    """
    token = await auth_service.refresh_access_token(request.refresh_token)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token tidak valid atau sudah expired",
        )

    return token


@router.get(
    "/me",
    response_model=AdminResponse,
    summary="Get Current Admin",
    description="Dapatkan informasi admin yang sedang login.",
)
async def get_me(
    current_admin: Admin = Depends(get_current_admin),
) -> AdminResponse:
    """
    Endpoint untuk mendapatkan data admin yang sedang login.
    Berguna untuk frontend memvalidasi token masih valid.
    """
    return AdminResponse(
        id=str(current_admin.id),
        username=current_admin.username,
        email=current_admin.email,
        is_active=current_admin.is_active,
        created_at=current_admin.created_at.isoformat(),
    )
