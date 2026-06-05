"""
services/report_service.py

Business logic untuk kalkulasi laporan keuangan.
Menggunakan TransactionService dan DebtService untuk mengumpulkan data,
lalu menghitung dan memformat laporan.
"""

from schemas.report import (
    DailyReportResponse,
    DashboardSummaryResponse,
    MonthlyReportResponse,
)
from services.debt_service import DebtService
from services.transaction_service import TransactionService
from services.user_service import UserService
from utils.date_helper import (
    get_current_month_range,
    get_month_name_id,
    get_today_range,
    now_wib,
)
from utils.number_formatter import format_rupiah


class ReportService:
    """
    Service untuk menghasilkan laporan keuangan.

    Mengaggregasi data dari multiple services dan
    memformat hasilnya untuk ditampilkan ke user atau dashboard.
    """

    def __init__(
        self,
        transaction_service: TransactionService,
        debt_service: DebtService,
        user_service: UserService,
    ) -> None:
        self._tx_service = transaction_service
        self._debt_service = debt_service
        self._user_service = user_service

    async def get_daily_report(self, phone_number: str) -> DailyReportResponse:
        """
        Buat laporan harian untuk user.

        Menghitung total pemasukan, pengeluaran, dan laba bersih
        untuk hari ini (timezone WIB).
        """
        start, end = get_today_range()

        summary = await self._tx_service.get_daily_summary(
            phone_number=phone_number,
            start_date=start,
            end_date=end,
        )

        today = now_wib().date()

        return DailyReportResponse(
            report_date=today,
            total_income=summary.total_income,
            total_expense=summary.total_expense,
            net_profit=summary.net_profit,
            transaction_count=summary.transaction_count,
            total_income_formatted=format_rupiah(summary.total_income),
            total_expense_formatted=format_rupiah(summary.total_expense),
            net_profit_formatted=format_rupiah(summary.net_profit),
        )

    async def get_monthly_report(self, phone_number: str) -> MonthlyReportResponse:
        """
        Buat laporan bulanan untuk user.

        Menghitung total pemasukan, pengeluaran, hutang belum lunas,
        dan laba bersih untuk bulan berjalan (timezone WIB).
        """
        now = now_wib()
        start, end = get_current_month_range()

        summary = await self._tx_service.get_daily_summary(
            phone_number=phone_number,
            start_date=start,
            end_date=end,
        )

        total_debt = await self._debt_service.get_total_unpaid_by_phone(phone_number)
        debt_count = await self._debt_service.count_unpaid_by_phone(phone_number)

        return MonthlyReportResponse(
            year=now.year,
            month=now.month,
            month_name=get_month_name_id(now.month),
            total_income=summary.total_income,
            total_expense=summary.total_expense,
            total_debt=total_debt,
            net_profit=summary.net_profit,
            total_income_formatted=format_rupiah(summary.total_income),
            total_expense_formatted=format_rupiah(summary.total_expense),
            total_debt_formatted=format_rupiah(total_debt),
            net_profit_formatted=format_rupiah(summary.net_profit),
            transaction_count=summary.transaction_count,
            debt_count=debt_count,
        )

    async def get_dashboard_summary(self) -> DashboardSummaryResponse:
        """
        Buat ringkasan untuk halaman utama admin dashboard.

        Mengumpulkan statistik dari semua users:
        - Total user, user aktif hari ini
        - Total transaksi & nominal hari ini
        - Total hutang belum lunas
        """
        start_today, end_today = get_today_range()

        total_users = await self._user_service.get_total_users()
        active_users_today = await self._user_service.get_active_users_today()

        total_income_today, total_expense_today = (
            await self._tx_service.get_dashboard_totals(
                start_date=start_today,
                end_date=end_today,
            )
        )
        net_profit_today = total_income_today - total_expense_today

        total_unpaid_debts = await self._debt_service.get_total_unpaid_all()

        # Hitung pesan hari ini dari Log
        from models.log import Log

        total_messages_today = await Log.find(
            Log.created_at >= start_today,
            Log.created_at < end_today,
        ).count()

        # Hitung transaksi hari ini
        from models.transaction import Transaction

        total_transactions_today = await Transaction.find(
            Transaction.transaction_date >= start_today,
            Transaction.transaction_date < end_today,
        ).count()

        return DashboardSummaryResponse(
            total_users=total_users,
            active_users_today=active_users_today,
            total_transactions_today=total_transactions_today,
            total_income_today=total_income_today,
            total_expense_today=total_expense_today,
            net_profit_today=net_profit_today,
            total_unpaid_debts=total_unpaid_debts,
            total_messages_today=total_messages_today,
            total_income_today_formatted=format_rupiah(total_income_today),
            total_expense_today_formatted=format_rupiah(total_expense_today),
            net_profit_today_formatted=format_rupiah(net_profit_today),
            total_unpaid_debts_formatted=format_rupiah(total_unpaid_debts),
        )
