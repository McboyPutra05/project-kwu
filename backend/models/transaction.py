"""
models/transaction.py

Beanie Document model untuk collection 'transactions'.
Menyimpan setiap transaksi keuangan (pemasukan & pengeluaran).
"""

from datetime import datetime, timezone
from typing import Literal

from beanie import Document, Indexed
from beanie import PydanticObjectId
from pydantic import Field


class Transaction(Document):
    """
    Representasi satu transaksi keuangan.

    Setiap pesan pemasukan/pengeluaran dari user
    menghasilkan satu document Transaction.
    """

    # Referensi ke user (phone_number untuk kemudahan query)
    user_id: PydanticObjectId
    phone_number: Indexed(str)  # type: ignore  # untuk query tanpa join

    # Tipe transaksi
    transaction_type: Literal["income", "expense"]

    # Deskripsi dari user
    description: str

    # Jumlah dalam Rupiah (float untuk fleksibilitas)
    amount: float = Field(gt=0)  # Harus lebih dari 0

    # Tanggal transaksi (bisa berbeda dengan created_at)
    transaction_date: datetime

    # Timestamp record dibuat
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "transactions"  # Nama collection di MongoDB
