"""
api/routes/debts.py

Route untuk manajemen hutang (admin dashboard).
Admin dapat melihat hutang dan menandai sebagai lunas.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies.auth import get_current_admin
from repositories.debt_repository import DebtRepository
from schemas.common import PaginatedResponse
from schemas.debt import DebtResponse
from services.debt_service import DebtService

router = APIRouter(
    prefix="/api/v1/debts",
    tags=["Debts"],
    dependencies=[Depends(get_current_admin)],
)


def get_debt_service() -> DebtService:
    return DebtService(DebtRepository())


@router.get(
    "",
    response_model=PaginatedResponse[DebtResponse],
    summary="List All Debts",
    description="""
    Dapatkan daftar hutang dengan filter opsional.
    
    **Filter tersedia:**
    - `status`: filter berdasarkan status (`unpaid` atau `paid`)
    - `phone_number`: filter berdasarkan nomor HP user
    """,
)
async def list_debts(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    status_filter: Optional[str] = Query(
        default=None,
        alias="status",
        description="Filter: 'unpaid' atau 'paid'",
    ),
    phone_number: Optional[str] = Query(
        default=None,
        description="Filter berdasarkan nomor HP",
    ),
    service: DebtService = Depends(get_debt_service),
) -> PaginatedResponse[DebtResponse]:
    """Daftar semua hutang."""
    return await service.list_debts(
        page=page,
        limit=limit,
        status=status_filter,
        phone_number=phone_number,
    )


@router.get(
    "/{debt_id}",
    response_model=DebtResponse,
    summary="Get Debt Detail",
)
async def get_debt(
    debt_id: str,
    service: DebtService = Depends(get_debt_service),
) -> DebtResponse:
    """Detail satu catatan hutang."""
    repo = DebtRepository()
    debt = await repo.find_by_id(debt_id)

    if not debt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hutang {debt_id} tidak ditemukan",
        )

    return service._to_response(debt)


@router.patch(
    "/{debt_id}/pay",
    response_model=DebtResponse,
    summary="Mark Debt as Paid",
    description="Tandai hutang sebagai lunas. Hanya bisa dilakukan oleh admin.",
)
async def mark_debt_as_paid(
    debt_id: str,
    service: DebtService = Depends(get_debt_service),
) -> DebtResponse:
    """
    Tandai hutang sebagai lunas.
    
    Dipanggil dari admin dashboard ketika admin konfirmasi
    bahwa hutang sudah dibayar.
    """
    result = await service.mark_as_paid(debt_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hutang {debt_id} tidak ditemukan",
        )
    return result
