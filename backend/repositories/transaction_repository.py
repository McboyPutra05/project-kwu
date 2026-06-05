"""
repositories/transaction_repository.py

Repository untuk operasi database Transaction.
Fokus pada query agregasi untuk laporan keuangan.
"""

from datetime import datetime
from typing import List, Optional

from beanie import PydanticObjectId

from models.transaction import Transaction
from repositories.base import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    """
    Repository untuk collection 'transactions'.
    
    Selain CRUD dasar, repository ini menyediakan
    aggregation queries untuk laporan keuangan.
    """

    def __init__(self) -> None:
        super().__init__(Transaction)

    async def find_by_phone(
        self,
        phone_number: str,
        skip: int = 0,
        limit: int = 20,
    ) -> List[Transaction]:
        """Ambil semua transaksi milik user berdasarkan phone number."""
        return (
            await Transaction.find(Transaction.phone_number == phone_number)
            .sort(-Transaction.created_at)
            .skip(skip)
            .limit(limit)
            .to_list()
        )

    async def find_by_date_range(
        self,
        phone_number: str,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Transaction]:
        """Ambil transaksi dalam rentang tanggal tertentu."""
        return await Transaction.find(
            Transaction.phone_number == phone_number,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date < end_date,
        ).to_list()

    async def sum_by_type_and_date(
        self,
        phone_number: str,
        transaction_type: str,
        start_date: datetime,
        end_date: datetime,
    ) -> float:
        """
        Hitung total transaksi berdasarkan tipe dan rentang tanggal.
        
        Digunakan untuk menghitung:
        - Total pemasukan hari ini
        - Total pengeluaran bulan ini
        - dll.
        
        Returns:
            Total jumlah dalam Rupiah (0 jika tidak ada transaksi).
        """
        pipeline = [
            {
                "$match": {
                    "phone_number": phone_number,
                    "transaction_type": transaction_type,
                    "transaction_date": {
                        "$gte": start_date,
                        "$lt": end_date,
                    },
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$amount"},
                }
            },
        ]
        result = await Transaction.aggregate(pipeline).to_list()
        return result[0]["total"] if result else 0.0

    async def count_by_phone(self, phone_number: str) -> int:
        """Hitung total transaksi milik user."""
        return await Transaction.find(
            Transaction.phone_number == phone_number
        ).count()

    async def get_all_paginated(
        self,
        skip: int = 0,
        limit: int = 20,
        transaction_type: Optional[str] = None,
        phone_number: Optional[str] = None,
    ) -> List[Transaction]:
        """
        Ambil semua transaksi dengan filter opsional (untuk admin dashboard).
        """
        query = Transaction.find()

        if transaction_type:
            query = query.find(Transaction.transaction_type == transaction_type)

        if phone_number:
            query = query.find(Transaction.phone_number == phone_number)

        return await query.sort(-Transaction.created_at).skip(skip).limit(limit).to_list()

    async def count_all_filtered(
        self,
        transaction_type: Optional[str] = None,
        phone_number: Optional[str] = None,
    ) -> int:
        """Hitung total transaksi dengan filter opsional."""
        query = Transaction.find()

        if transaction_type:
            query = query.find(Transaction.transaction_type == transaction_type)

        if phone_number:
            query = query.find(Transaction.phone_number == phone_number)

        return await query.count()

    async def sum_all_by_type_and_date(
        self,
        transaction_type: str,
        start_date: datetime,
        end_date: datetime,
    ) -> float:
        """Hitung total SEMUA user untuk dashboard summary."""
        pipeline = [
            {
                "$match": {
                    "transaction_type": transaction_type,
                    "transaction_date": {
                        "$gte": start_date,
                        "$lt": end_date,
                    },
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$amount"},
                }
            },
        ]
        result = await Transaction.aggregate(pipeline).to_list()
        return result[0]["total"] if result else 0.0
