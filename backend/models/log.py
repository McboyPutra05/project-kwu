"""
models/log.py

Beanie Document model untuk collection 'logs'.
Menyimpan semua percakapan masuk/keluar chatbot.
Berguna untuk debugging, audit, dan monitoring.
"""

from datetime import datetime, timezone

from beanie import Document, Indexed
from pydantic import Field


class Log(Document):
    """
    Log setiap percakapan WhatsApp dengan chatbot.

    Setiap pasangan pesan-masuk dan respons-bot
    disimpan sebagai satu document Log.
    """

    # Nomor telepon pengirim
    phone_number: Indexed(str)  # type: ignore

    # Pesan yang dikirim user
    message: str

    # Respons yang dikirim bot
    response: str

    # Timestamp pesan diterima
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "logs"
