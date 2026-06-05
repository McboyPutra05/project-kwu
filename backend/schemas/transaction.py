"""
schemas/transaction.py

Schema untuk data transaksi keuangan (pemasukan & pengeluaran).
"""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    """Schema untuk membuat transaksi baru (via API, bukan chatbot)."""
    transaction_type: Literal["income", "expense"]
    description: str = Field(..., min_length=1, max_length=500)
    amount: float = Field(..., gt=0, description="Jumlah dalam Rupiah")
    transaction_date: Optional[datetime] = None  # Default: sekarang

    model_config = {
        "json_schema_extra": {
            "example": {
                "transaction_type": "income",
                "description": "Penjualan Keripik",
                "amount": 150000,
            }
        }
    }


class TransactionResponse(BaseModel):
    """Response data transaksi."""
    id: str
    user_id: str
    phone_number: str
    transaction_type: Literal["income", "expense"]
    description: str
    amount: float
    transaction_date: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class TransactionSummary(BaseModel):
    """Ringkasan transaksi untuk laporan."""
    total_income: float = 0
    total_expense: float = 0
    net_profit: float = 0  # income - expense
    transaction_count: int = 0
