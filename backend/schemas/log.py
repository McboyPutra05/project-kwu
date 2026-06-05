"""
schemas/log.py

Schema untuk data log chatbot.
"""

from datetime import datetime

from pydantic import BaseModel


class LogResponse(BaseModel):
    """Response data log percakapan chatbot."""
    id: str
    phone_number: str
    message: str
    response: str
    created_at: datetime

    model_config = {"from_attributes": True}
