"""
core/security.py

Utilitas keamanan: JWT token management dan password hashing.
Menggunakan python-jose untuk JWT dan passlib untuk bcrypt hashing.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from core.config import settings


# ─────────────────────────────────────────────────────────────────
# Password Hashing
# ─────────────────────────────────────────────────────────────────

# CryptContext dengan bcrypt — auto-deprecated scheme untuk upgrade mudah
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password menggunakan bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifikasi password plain text terhadap hash yang tersimpan."""
    return pwd_context.verify(plain_password, hashed_password)


# ─────────────────────────────────────────────────────────────────
# JWT Token Management
# ─────────────────────────────────────────────────────────────────

def create_access_token(
    data: dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Buat JWT access token.
    
    Args:
        data: Payload yang akan di-encode ke dalam token.
              Minimal harus ada field "sub" (subject).
        expires_delta: Durasi token. Default dari settings.
    
    Returns:
        JWT token sebagai string.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )

    to_encode.update({
        "exp": expire,
        "type": "access",
    })

    return jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token(data: dict[str, Any]) -> str:
    """
    Buat JWT refresh token dengan durasi lebih panjang.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.jwt_refresh_token_expire_days
    )
    to_encode.update({
        "exp": expire,
        "type": "refresh",
    })

    return jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode dan validasi JWT token.
    
    Raises:
        JWTError: Jika token tidak valid atau sudah expired.
    
    Returns:
        Payload token sebagai dict.
    """
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )


def verify_token(token: str, token_type: str = "access") -> Optional[str]:
    """
    Verifikasi token dan kembalikan subject (username/id).
    
    Args:
        token: JWT token string.
        token_type: "access" atau "refresh".
    
    Returns:
        Subject (username) jika valid, None jika tidak valid.
    """
    try:
        payload = decode_token(token)
        
        # Cek tipe token
        if payload.get("type") != token_type:
            return None
        
        subject: str = payload.get("sub")
        if subject is None:
            return None
            
        return subject
        
    except JWTError:
        return None
