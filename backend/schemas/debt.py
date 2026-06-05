"""
schemas/debt.py

Schema untuk data hutang.
"""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class DebtCreate(BaseModel):
    """Schema untuk mencatat hutang baru (via API)."""
    description: str = Field(..., min_length=1, max_length=500)
    amount: float = Field(..., gt=0)
    due_date: Optional[datetime] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "description": "Hutang ke Supplier Tepung",
                "amount": 300000,
                "due_date": None,
            }
        }
    }


class DebtResponse(BaseModel):
    """Response data hutang."""
    id: str
    user_id: str
    phone_number: str
    description: str
    amount: float
    status: Literal["unpaid", "paid"]
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DebtUpdate(BaseModel):
    """Schema untuk update hutang."""
    status: Optional[Literal["unpaid", "paid"]] = None
    due_date: Optional[datetime] = None
