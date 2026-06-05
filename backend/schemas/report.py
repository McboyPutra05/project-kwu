"""
schemas/report.py

Schema untuk laporan keuangan (harian & bulanan).
"""

from datetime import date, datetime
from typing import List

from pydantic import BaseModel


class DailyReportResponse(BaseModel):
    """Laporan keuangan harian."""
    report_date: date
    total_income: float
    total_expense: float
    net_profit: float  # total_income - total_expense
    transaction_count: int

    # Formatted dalam Rupiah (untuk response API)
    total_income_formatted: str
    total_expense_formatted: str
    net_profit_formatted: str


class MonthlyReportResponse(BaseModel):
    """Laporan keuangan bulanan."""
    year: int
    month: int
    month_name: str  # "Januari", "Februari", dst.
    total_income: float
    total_expense: float
    total_debt: float  # Total hutang yang belum lunas
    net_profit: float

    # Formatted
    total_income_formatted: str
    total_expense_formatted: str
    total_debt_formatted: str
    net_profit_formatted: str

    transaction_count: int
    debt_count: int


class DashboardSummaryResponse(BaseModel):
    """Ringkasan untuk halaman utama admin dashboard."""
    total_users: int
    active_users_today: int
    total_transactions_today: int
    total_income_today: float
    total_expense_today: float
    net_profit_today: float
    total_unpaid_debts: float
    total_messages_today: int

    # Formatted
    total_income_today_formatted: str
    total_expense_today_formatted: str
    net_profit_today_formatted: str
    total_unpaid_debts_formatted: str
