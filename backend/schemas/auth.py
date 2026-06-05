"""
schemas/auth.py

Schema untuk autentikasi admin (login & JWT token).
"""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Request body untuk admin login."""
    username: str = Field(..., min_length=3, description="Username admin")
    password: str = Field(..., min_length=6, description="Password admin")

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "admin",
                "password": "rahasia123",
            }
        }
    }


class TokenResponse(BaseModel):
    """Response setelah login berhasil."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # Detik sampai token expired


class RefreshTokenRequest(BaseModel):
    """Request body untuk refresh token."""
    refresh_token: str


class AdminCreateRequest(BaseModel):
    """Request untuk membuat akun admin baru."""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., description="Email admin")
    password: str = Field(..., min_length=8, description="Password minimal 8 karakter")


class AdminResponse(BaseModel):
    """Response data admin (tanpa password)."""
    id: str
    username: str
    email: str
    is_active: bool
    created_at: str
