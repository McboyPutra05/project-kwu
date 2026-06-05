"""
schemas/user.py

Schema untuk data pengguna WhatsApp chatbot.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    """Response data user untuk API."""
    id: str
    phone_number: str
    name: Optional[str] = None
    is_active: bool
    session_state: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """Schema untuk update data user."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None
