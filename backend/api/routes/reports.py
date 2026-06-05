"""
api/routes/reports.py

Route untuk laporan keuangan (admin dashboard).
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query

from api.dependencies.auth import get_current_admin
from repositories.debt_repository import DebtRepository
from repositories.transaction_repository import TransactionRepository
from repositories.user_repository import UserRepository
from schemas.report import (
    DashboardSummaryResponse,
    DailyReportResponse,
    MonthlyReportResponse,
)
from services.debt_service import DebtService
from services.report_service import ReportService
from services.transaction_service import TransactionService
from services.user_service import UserService

router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Reports"],
    dependencies=[Depends(get_current_admin)],
)


def get_report_service() -> ReportService:
    """Factory untuk ReportService dengan semua dependency."""
    user_repo = UserRepository()
    tx_repo = TransactionRepository()
    debt_repo = DebtRepository()

    user_service = UserService(user_repo)
    tx_service = TransactionService(tx_repo)
    debt_service = DebtService(debt_repo)

    return ReportService(tx_service, debt_service, user_service)


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
    summary="Dashboard Summary",
    description="Ringkasan statistik untuk halaman utama admin dashboard.",
)
async def get_dashboard_summary(
    service: ReportService = Depends(get_report_service),
) -> DashboardSummaryResponse:
    """
    Statistik utama untuk dashboard:
    - Total user, user aktif hari ini
    - Total transaksi hari ini
    - Total pemasukan, pengeluaran, laba bersih hari ini
    - Total hutang belum lunas
    - Total pesan hari ini
    """
    return await service.get_dashboard_summary()


@router.get(
    "/daily",
    response_model=DailyReportResponse,
    summary="Daily Report",
    description="Laporan keuangan harian untuk satu user.",
)
async def get_daily_report(
    phone_number: str = Query(..., description="Nomor HP user"),
    service: ReportService = Depends(get_report_service),
) -> DailyReportResponse:
    """Laporan harian untuk user tertentu berdasarkan nomor HP."""
    return await service.get_daily_report(phone_number)


@router.get(
    "/monthly",
    response_model=MonthlyReportResponse,
    summary="Monthly Report",
    description="Laporan keuangan bulanan untuk satu user.",
)
async def get_monthly_report(
    phone_number: str = Query(..., description="Nomor HP user"),
    service: ReportService = Depends(get_report_service),
) -> MonthlyReportResponse:
    """Laporan bulanan untuk user tertentu berdasarkan nomor HP."""
    return await service.get_monthly_report(phone_number)
