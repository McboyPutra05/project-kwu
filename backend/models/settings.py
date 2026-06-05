"""
models/settings.py

Beanie Document model untuk collection 'settings'.
Menyimpan konfigurasi aplikasi yang bisa diubah via dashboard
tanpa perlu restart server.
"""

from datetime import datetime, timezone
from typing import Any

from beanie import Document, Indexed
from pydantic import Field


class AppSettings(Document):
    """
    Konfigurasi dinamis aplikasi.

    Berbeda dengan core/config.py yang dibaca dari .env,
    AppSettings menyimpan konfigurasi yang bisa diubah
    admin melalui dashboard saat runtime.

    Contoh:
    - key: "welcome_message", value: "Selamat datang..."
    - key: "bot_active", value: True
    """

    # Kunci konfigurasi (unik)
    key: Indexed(str, unique=True)  # type: ignore

    # Nilai konfigurasi (bisa berupa tipe apapun)
    value: Any

    # Deskripsi untuk admin dashboard
    description: str = ""

    # Timestamp
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "settings"
