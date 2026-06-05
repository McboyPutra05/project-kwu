"""
api/routes/logs.py

Route untuk melihat log percakapan chatbot (admin dashboard).
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query

from api.dependencies.auth import get_current_admin
from models.log import Log
from schemas.common import PaginatedResponse
from schemas.log import LogResponse

router = APIRouter(
    prefix="/api/v1/logs",
    tags=["Logs"],
    dependencies=[Depends(get_current_admin)],
)


@router.get(
    "",
    response_model=PaginatedResponse[LogResponse],
    summary="List Chatbot Logs",
    description="""
    Dapatkan log percakapan chatbot dengan pagination dan filter.
    
    Berguna untuk:
    - Monitoring percakapan user
    - Debugging chatbot
    - Audit trail
    """,
)
async def list_logs(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    phone_number: Optional[str] = Query(
        default=None,
        description="Filter berdasarkan nomor HP",
    ),
) -> PaginatedResponse[LogResponse]:
    """
    Daftar log percakapan chatbot dengan pagination.
    Di-sort dari yang terbaru ke terlama.
    """
    skip = (page - 1) * limit

    # Build query
    query = Log.find()
    if phone_number:
        query = query.find(Log.phone_number == phone_number)

    total = await query.count()
    logs = await query.sort(-Log.created_at).skip(skip).limit(limit).to_list()

    items = [
        LogResponse(
            id=str(log.id),
            phone_number=log.phone_number,
            message=log.message,
            response=log.response,
            created_at=log.created_at,
        )
        for log in logs
    ]

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=page,
        limit=limit,
    )
