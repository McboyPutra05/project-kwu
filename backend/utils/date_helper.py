"""
utils/date_helper.py

Helper untuk operasi tanggal yang sering digunakan
dalam laporan keuangan.

Semua datetime menggunakan timezone UTC untuk konsistensi database,
lalu dikonversi ke WIB (UTC+7) untuk tampilan ke user.
"""

from datetime import datetime, timedelta, timezone
from typing import Tuple

import pytz

# Timezone Indonesia (WIB = UTC+7)
WIB = pytz.timezone("Asia/Jakarta")

# Nama bulan dalam Bahasa Indonesia
MONTH_NAMES_ID = {
    1: "Januari",
    2: "Februari",
    3: "Maret",
    4: "April",
    5: "Mei",
    6: "Juni",
    7: "Juli",
    8: "Agustus",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Desember",
}

# Nama hari dalam Bahasa Indonesia
DAY_NAMES_ID = {
    0: "Senin",
    1: "Selasa",
    2: "Rabu",
    3: "Kamis",
    4: "Jumat",
    5: "Sabtu",
    6: "Minggu",
}


def now_wib() -> datetime:
    """Kembalikan waktu sekarang dalam timezone WIB."""
    return datetime.now(WIB)


def now_utc() -> datetime:
    """Kembalikan waktu sekarang dalam UTC (untuk disimpan ke database)."""
    return datetime.now(timezone.utc)


def get_today_range() -> Tuple[datetime, datetime]:
    """
    Kembalikan range waktu UTC untuk hari ini (WIB).
    
    Contoh: Jika sekarang 03 Juni 2026 WIB,
    kembalikan (2026-06-02 17:00:00 UTC, 2026-06-03 17:00:00 UTC)
    
    Returns:
        Tuple (start_of_day_utc, end_of_day_utc)
    """
    today_wib = now_wib().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow_wib = today_wib + timedelta(days=1)
    
    # Konversi ke UTC untuk query MongoDB
    start = today_wib.astimezone(timezone.utc)
    end = tomorrow_wib.astimezone(timezone.utc)
    
    return start, end


def get_month_range(year: int, month: int) -> Tuple[datetime, datetime]:
    """
    Kembalikan range waktu UTC untuk bulan tertentu (WIB).
    
    Args:
        year: Tahun (misal: 2026)
        month: Bulan 1-12
    
    Returns:
        Tuple (start_of_month_utc, start_of_next_month_utc)
    """
    # Awal bulan dalam WIB
    start_wib = WIB.localize(datetime(year, month, 1, 0, 0, 0))
    
    # Awal bulan berikutnya
    if month == 12:
        end_wib = WIB.localize(datetime(year + 1, 1, 1, 0, 0, 0))
    else:
        end_wib = WIB.localize(datetime(year, month + 1, 1, 0, 0, 0))
    
    return start_wib.astimezone(timezone.utc), end_wib.astimezone(timezone.utc)


def get_current_month_range() -> Tuple[datetime, datetime]:
    """Kembalikan range untuk bulan berjalan."""
    now = now_wib()
    return get_month_range(now.year, now.month)


def format_date_id(dt: datetime) -> str:
    """
    Format datetime ke string Bahasa Indonesia.
    
    Contoh: "Selasa, 03 Juni 2026"
    """
    # Konversi ke WIB jika belum
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt).astimezone(WIB)
    else:
        dt = dt.astimezone(WIB)
    
    day_name = DAY_NAMES_ID[dt.weekday()]
    month_name = MONTH_NAMES_ID[dt.month]
    
    return f"{day_name}, {dt.day:02d} {month_name} {dt.year}"


def format_short_date_id(dt: datetime) -> str:
    """
    Format datetime ke string singkat Bahasa Indonesia.
    
    Contoh: "03 Juni 2026"
    """
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt).astimezone(WIB)
    else:
        dt = dt.astimezone(WIB)
    
    month_name = MONTH_NAMES_ID[dt.month]
    return f"{dt.day:02d} {month_name} {dt.year}"


def get_month_name_id(month: int) -> str:
    """Kembalikan nama bulan dalam Bahasa Indonesia."""
    return MONTH_NAMES_ID.get(month, "Unknown")
