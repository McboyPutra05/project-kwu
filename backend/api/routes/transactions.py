"""
api/routes/transactions.py

Route untuk melihat transaksi keuangan (admin dashboard).
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies.auth import get_current_admin
from repositories.transaction_repository import TransactionRepository
from schemas.common import PaginatedResponse
from schemas.transaction import TransactionResponse
from services.transaction_service import TransactionService

router = APIRouter(
    prefix="/api/v1/transactions",
    tags=["Transactions"],
    dependencies=[Depends(get_current_admin)],
)


def get_transaction_service() -> TransactionService:
    return TransactionService(TransactionRepository())


@router.get(
    "",
    response_model=PaginatedResponse[TransactionResponse],
    summary="List All Transactions",
    description="""
    Dapatkan daftar transaksi dengan filter opsional.
    
    **Filter tersedia:**
    - `transaction_type`: filter berdasarkan tipe (`income` atau `expense`)
    - `phone_number`: filter berdasarkan nomor HP user
    """,
)
async def list_transactions(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    transaction_type: Optional[str] = Query(
        default=None,
        description="Filter: 'income' atau 'expense'",
    ),
    phone_number: Optional[str] = Query(
        default=None,
        description="Filter berdasarkan nomor HP",
    ),
    service: TransactionService = Depends(get_transaction_service),
) -> PaginatedResponse[TransactionResponse]:
    """Daftar semua transaksi dengan pagination dan filter."""
    return await service.list_transactions(
        page=page,
        limit=limit,
        transaction_type=transaction_type,
        phone_number=phone_number,
    )


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
    summary="Get Transaction Detail",
)
async def get_transaction(
    transaction_id: str,
    service: TransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    """Detail satu transaksi."""
    repo = TransactionRepository()
    tx = await repo.find_by_id(transaction_id)

    if not tx:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaksi {transaction_id} tidak ditemukan",
        )

    return TransactionResponse(
        id=str(tx.id),
        user_id=str(tx.user_id),
        phone_number=tx.phone_number,
        transaction_type=tx.transaction_type,
        description=tx.description,
        amount=tx.amount,
        transaction_date=tx.transaction_date,
        created_at=tx.created_at,
    )
