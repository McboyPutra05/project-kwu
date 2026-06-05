"""
models/user.py

Beanie Document model untuk collection 'users'.
Menyimpan data pengguna WhatsApp yang menggunakan chatbot.

Field session_state digunakan untuk chatbot state machine:
- Menyimpan konteks percakapan saat ini
- Persistent across server restarts
"""

from datetime import datetime, timezone
from typing import Optional

from beanie import Document, Indexed
from pydantic import Field


class User(Document):
    """
    Representasi pengguna chatbot WhatsApp.

    Satu user = satu nomor telepon WhatsApp.
    User dibuat otomatis saat pertama kali mengirim pesan.
    """

    # Nomor telepon sebagai identifier unik
    # Format: "628123456789" (tanpa + atau 0)
    phone_number: Indexed(str, unique=True)  # type: ignore

    # Nama user (opsional, bisa diupdate nanti)
    name: Optional[str] = None

    # Status aktif user
    is_active: bool = True

    # ─────────────────────────────────────────
    # Chatbot State Machine
    # ─────────────────────────────────────────
    # Menyimpan "posisi" user dalam alur percakapan chatbot.
    # Nilai: None | "menu_main" | "awaiting_income_input" |
    #        "awaiting_expense_input" | "awaiting_debt_input"
    session_state: Optional[str] = None

    # Timestamp
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"  # Nama collection di MongoDB
        use_state_management = True

    def update_timestamp(self) -> None:
        """Update field updated_at ke waktu sekarang."""
        self.updated_at = datetime.now(timezone.utc)
