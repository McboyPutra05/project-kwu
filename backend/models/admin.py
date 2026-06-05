"""
models/admin.py

Beanie Document model untuk collection 'admins'.
Menyimpan data akun admin untuk dashboard.
Berbeda dari User (pengguna WhatsApp), Admin adalah pengelola sistem.
"""

from datetime import datetime, timezone

from beanie import Document, Indexed
from pydantic import Field


class Admin(Document):
    """
    Akun admin untuk mengakses dashboard.

    Password disimpan sebagai bcrypt hash,
    TIDAK PERNAH simpan password plaintext.
    """

    # Username untuk login (unik)
    username: Indexed(str, unique=True)  # type: ignore

    # Email admin (unik)
    email: Indexed(str, unique=True)  # type: ignore

    # Password yang sudah di-hash dengan bcrypt
    hashed_password: str

    # Status aktif
    is_active: bool = True

    # Timestamp
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "admins"
