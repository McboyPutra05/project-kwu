"""
services/debt_service.py

Business logic untuk pencatatan dan manajemen hutang.
"""

from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId  # type: ignore
from loguru import logger  # type: ignore

from models.debt import Debt
from repositories.debt_repository import DebtRepository
from schemas.common import PaginatedResponse
from schemas.debt import DebtResponse


class DebtService:
    """
    Service untuk pencatatan dan query hutang.
    """

    def __init__(self, repository: DebtRepository) -> None:
        self._repo = repository

    async def record_debt(
        self,
        user_id: str,
        phone_number: str,
        description: str,
        amount: float,
        due_date: Optional[datetime] = None,
    ) -> Debt:
        """
        Catat hutang baru.

        Dipanggil dari ChatbotService saat user mengirim data hutang.
        """
        debt = Debt(
            user_id=PydanticObjectId(user_id),
            phone_number=phone_number,
            description=description,
            amount=amount,
            due_date=due_date,
        )
        saved = await self._repo.create(debt)
        logger.info(f"💳 Debt recorded: {description} = {amount} | user={phone_number}")
        return saved

    async def mark_as_paid(self, debt_id: str) -> Optional[DebtResponse]:
        """
        Tandai hutang sebagai lunas.

        Dipanggil dari admin dashboard.
        """
        debt = await self._repo.find_by_id(debt_id)
        if not debt:
            return None

        debt.mark_as_paid()
        updated = await self._repo.update(debt)
        logger.info(f"✅ Debt marked as paid: {debt_id}")

        return self._to_response(updated)

    async def get_total_unpaid_by_phone(self, phone_number: str) -> float:
        """Hitung total hutang belum lunas milik user."""
        return await self._repo.sum_unpaid_by_phone(phone_number)

    async def count_unpaid_by_phone(self, phone_number: str) -> int:
        """Hitung jumlah hutang belum lunas milik user."""
        unpaid = await self._repo.find_unpaid_by_phone(phone_number)
        return len(unpaid)

    async def list_debts(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        phone_number: Optional[str] = None,
    ) -> PaginatedResponse[DebtResponse]:
        """Ambil hutang dengan pagination dan filter (untuk admin dashboard)."""
        skip = (page - 1) * limit

        debts = await self._repo.get_all_paginated(
            skip=skip,
            limit=limit,
            status=status,
            phone_number=phone_number,
        )
        total = await self._repo.count_all_filtered(
            status=status,
            phone_number=phone_number,
        )

        return PaginatedResponse.create(
            items=[self._to_response(d) for d in debts],
            total=total,
            page=page,
            limit=limit,
        )

    async def get_total_unpaid_all(self) -> float:
        """Hitung total hutang belum lunas semua user (untuk dashboard)."""
        return await self._repo.sum_all_unpaid()

    def _to_response(self, debt: Debt) -> DebtResponse:
        """Convert Debt model ke DebtResponse schema."""
        return DebtResponse(
            id=str(debt.id),
            user_id=str(debt.user_id),
            phone_number=debt.phone_number,
            description=debt.description,
            amount=debt.amount,
            status=debt.status,
            due_date=debt.due_date,
            created_at=debt.created_at,
            updated_at=debt.updated_at,
        )
