"""
models/debt.py

Beanie Document model untuk collection 'debts'.
Menyimpan catatan hutang user.
"""

from datetime import datetime, timezone
from typing import Literal, Optional

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field


class Debt(Document):
    """
    Representasi satu catatan hutang.

    User mencatat hutang, kemudian dapat menandai
    hutang sebagai "lunas" (paid) melalui dashboard.
    """

    # Referensi ke user
    user_id: PydanticObjectId
    phone_number: Indexed(str)  # type: ignore

    # Deskripsi hutang (misal: "Hutang ke Supplier Tepung")
    description: str

    # Jumlah hutang dalam Rupiah
    amount: float = Field(gt=0)

    # Status hutang
    status: Literal["unpaid", "paid"] = "unpaid"

    # Tanggal jatuh tempo (opsional)
    due_date: Optional[datetime] = None

    # Timestamp
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "debts"

    def mark_as_paid(self) -> None:
        """Tandai hutang sebagai lunas."""
        self.status = "paid"
        self.updated_at = datetime.now(timezone.utc)
