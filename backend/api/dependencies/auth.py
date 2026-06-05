"""
api/dependencies/auth.py

FastAPI Dependency Injection untuk autentikasi admin.
Menggunakan OAuth2 Bearer Token scheme.

Cara pakai di route:
    @router.get("/protected")
    async def protected_route(
        current_admin: Admin = Depends(get_current_admin)
    ):
        ...
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.security import verify_token
from models.admin import Admin

# Skema OAuth2 — token diambil dari header "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_admin(
    token: str = Depends(oauth2_scheme),
) -> Admin:
    """
    Dependency untuk memvalidasi JWT token dan mendapatkan admin yang sedang login.
    
    Gunakan sebagai parameter di route yang membutuhkan autentikasi.
    FastAPI secara otomatis inject token dari header Authorization.
    
    Raises:
        HTTPException 401: Jika token tidak valid atau expired.
        HTTPException 403: Jika akun admin tidak aktif.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau sudah expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verifikasi token
    username = verify_token(token, token_type="access")
    if username is None:
        raise credentials_exception

    # Cari admin di database
    admin = await Admin.find_one(Admin.username == username)
    if admin is None:
        raise credentials_exception

    # Cek status aktif
    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akun admin tidak aktif",
        )

    return admin
