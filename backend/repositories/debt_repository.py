"""
repositories/debt_repository.py

Repository untuk operasi database Debt.
"""

from datetime import datetime
from typing import List, Optional

from models.debt import Debt
from repositories.base import BaseRepository


class DebtRepository(BaseRepository[Debt]):
    """Repository untuk collection 'debts'."""

    def __init__(self) -> None:
        super().__init__(Debt)

    async def find_by_phone(
        self,
        phone_number: str,
        skip: int = 0,
        limit: int = 20,
    ) -> List[Debt]:
        """Ambil semua hutang milik user."""
        return (
            await Debt.find(Debt.phone_number == phone_number)
            .sort("-created_at")
            .skip(skip)
            .limit(limit)
            .to_list()
        )

    async def find_unpaid_by_phone(self, phone_number: str) -> List[Debt]:
        """Ambil hutang yang belum lunas milik user."""
        return await Debt.find(
            Debt.phone_number == phone_number,
            Debt.status == "unpaid",
        ).to_list()

    async def sum_unpaid_by_phone(self, phone_number: str) -> float:
        """Hitung total hutang belum lunas milik user."""
        pipeline = [
            {
                "$match": {
                    "phone_number": phone_number,
                    "status": "unpaid",
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$amount"},
                }
            },
        ]
        result = await Debt.aggregate(pipeline).to_list()
        return result[0]["total"] if result else 0.0

    async def sum_all_unpaid(self) -> float:
        """Hitung total hutang belum lunas SEMUA user (untuk dashboard)."""
        pipeline = [
            {"$match": {"status": "unpaid"}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}},
        ]
        result = await Debt.aggregate(pipeline).to_list()
        return result[0]["total"] if result else 0.0

    async def get_all_paginated(
        self,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
        phone_number: Optional[str] = None,
    ) -> List[Debt]:
        """Ambil semua hutang dengan filter (untuk admin dashboard)."""
        query = Debt.find()

        if status:
            query = query.find(Debt.status == status)

        if phone_number:
            query = query.find(Debt.phone_number == phone_number)

        return await query.sort("-created_at").skip(skip).limit(limit).to_list()

    async def count_all_filtered(
        self,
        status: Optional[str] = None,
        phone_number: Optional[str] = None,
    ) -> int:
        """Hitung hutang dengan filter."""
        query = Debt.find()

        if status:
            query = query.find(Debt.status == status)

        if phone_number:
            query = query.find(Debt.phone_number == phone_number)

        return await query.count()
