"""
services/transaction_service.py

Business logic untuk pencatatan transaksi keuangan.
"""

from datetime import datetime, timezone
from typing import Optional

from beanie import PydanticObjectId
from loguru import logger

from models.transaction import Transaction
from repositories.transaction_repository import TransactionRepository
from schemas.common import PaginatedResponse
from schemas.transaction import TransactionResponse, TransactionSummary


class TransactionService:
    """
    Service untuk pencatatan dan query transaksi keuangan.
    Dipanggil oleh ChatbotService (dari WhatsApp) dan API routes (dari dashboard).
    """

    def __init__(self, repository: TransactionRepository) -> None:
        self._repo = repository

    async def record_income(
        self,
        user_id: str,
        phone_number: str,
        description: str,
        amount: float,
    ) -> Transaction:
        """
        Catat pemasukan baru.

        Dipanggil dari ChatbotService saat user mengirim data pemasukan.
        """
        transaction = Transaction(
            user_id=PydanticObjectId(user_id),
            phone_number=phone_number,
            transaction_type="income",
            description=description,
            amount=amount,
            transaction_date=datetime.now(timezone.utc),
        )
        saved = await self._repo.create(transaction)
        logger.info(
            f"💰 Income recorded: {description} = {amount} | user={phone_number}"
        )
        return saved

    async def record_expense(
        self,
        user_id: str,
        phone_number: str,
        description: str,
        amount: float,
    ) -> Transaction:
        """
        Catat pengeluaran baru.

        Dipanggil dari ChatbotService saat user mengirim data pengeluaran.
        """
        transaction = Transaction(
            user_id=PydanticObjectId(user_id),
            phone_number=phone_number,
            transaction_type="expense",
            description=description,
            amount=amount,
            transaction_date=datetime.now(timezone.utc),
        )
        saved = await self._repo.create(transaction)
        logger.info(
            f"💸 Expense recorded: {description} = {amount} | user={phone_number}"
        )
        return saved

    async def get_daily_summary(
        self,
        phone_number: str,
        start_date: datetime,
        end_date: datetime,
    ) -> TransactionSummary:
        """
        Hitung ringkasan transaksi untuk rentang tanggal tertentu.
        Digunakan untuk laporan harian dan bulanan.
        """
        total_income = await self._repo.sum_by_type_and_date(
            phone_number=phone_number,
            transaction_type="income",
            start_date=start_date,
            end_date=end_date,
        )
        total_expense = await self._repo.sum_by_type_and_date(
            phone_number=phone_number,
            transaction_type="expense",
            start_date=start_date,
            end_date=end_date,
        )

        # Hitung jumlah transaksi
        transactions = await self._repo.find_by_date_range(
            phone_number=phone_number,
            start_date=start_date,
            end_date=end_date,
        )

        return TransactionSummary(
            total_income=total_income,
            total_expense=total_expense,
            net_profit=total_income - total_expense,
            transaction_count=len(transactions),
        )

    async def list_transactions(
        self,
        page: int = 1,
        limit: int = 20,
        transaction_type: Optional[str] = None,
        phone_number: Optional[str] = None,
    ) -> PaginatedResponse[TransactionResponse]:
        """Ambil transaksi dengan pagination dan filter (untuk admin dashboard)."""
        skip = (page - 1) * limit

        transactions = await self._repo.get_all_paginated(
            skip=skip,
            limit=limit,
            transaction_type=transaction_type,
            phone_number=phone_number,
        )
        total = await self._repo.count_all_filtered(
            transaction_type=transaction_type,
            phone_number=phone_number,
        )

        items = [
            TransactionResponse(
                id=str(t.id),
                user_id=str(t.user_id),
                phone_number=t.phone_number,
                transaction_type=t.transaction_type,
                description=t.description,
                amount=t.amount,
                transaction_date=t.transaction_date,
                created_at=t.created_at,
            )
            for t in transactions
        ]

        return PaginatedResponse.create(
            items=items,
            total=total,
            page=page,
            limit=limit,
        )

    async def get_dashboard_totals(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> tuple[float, float]:
        """
        Hitung total income dan expense SEMUA user untuk dashboard.

        Returns:
            Tuple (total_income, total_expense)
        """
        total_income = await self._repo.sum_all_by_type_and_date(
            transaction_type="income",
            start_date=start_date,
            end_date=end_date,
        )
        total_expense = await self._repo.sum_all_by_type_and_date(
            transaction_type="expense",
            start_date=start_date,
            end_date=end_date,
        )
        return total_income, total_expense

    async def count_transactions_today(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> int:
        """Hitung transaksi hari ini untuk dashboard."""
        return await self._repo.count_all_filtered()
