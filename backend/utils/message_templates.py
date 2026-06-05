"""
utils/message_templates.py

Semua template pesan WhatsApp dalam satu file terpusat.
Keuntungan: mudah diubah konten pesan tanpa menyentuh logic.
Bisa diextend untuk mendukung multi-bahasa di masa depan.
"""

from utils.number_formatter import format_rupiah


# ─────────────────────────────────────────────────────────────────
# Menu Utama
# ─────────────────────────────────────────────────────────────────

WELCOME_MESSAGE = """👋 *Selamat datang di FinanceBot UMKM!*

Saya siap membantu Anda mencatat keuangan bisnis dengan mudah.

Apa yang bisa saya bantu?

1️⃣ *Pemasukan* — Catat uang masuk
2️⃣ *Pengeluaran* — Catat uang keluar
3️⃣ *Hutang* — Catat hutang
4️⃣ *Laporan* — Lihat laporan keuangan

Ketik angka atau nama menu di atas 👆"""

MENU_MESSAGE = """📋 *Menu Utama FinanceBot UMKM*

Pilih menu yang ingin Anda gunakan:

1️⃣ *Pemasukan*
2️⃣ *Pengeluaran*
3️⃣ *Hutang*
4️⃣ *Laporan*

Ketik angka atau nama menu 👆"""

HELP_MESSAGE = """❓ *Bantuan FinanceBot UMKM*

Kata kunci yang bisa digunakan:
• *Halo / Hai / Menu* — Tampilkan menu utama
• *Pemasukan / 1* — Catat pemasukan
• *Pengeluaran / 2* — Catat pengeluaran
• *Hutang / 3* — Catat hutang
• *Laporan / 4* — Lihat laporan
• *Laporan Hari Ini* — Laporan harian
• *Laporan Bulan Ini* — Laporan bulanan
• *Batal* — Batalkan input saat ini

Butuh bantuan lebih? Hubungi admin."""


# ─────────────────────────────────────────────────────────────────
# Input Prompts
# ─────────────────────────────────────────────────────────────────

INCOME_PROMPT = """📥 *Catat Pemasukan*

Kirim pesan dengan format:
`Nama Pemasukan, Jumlah`

Contoh:
`Penjualan Keripik, 150000`
`Jasa Jahit Baju, 75rb`

Atau ketik *Batal* untuk kembali ke menu."""

EXPENSE_PROMPT = """📤 *Catat Pengeluaran*

Kirim pesan dengan format:
`Nama Pengeluaran, Jumlah`

Contoh:
`Beli Tepung, 50000`
`Ongkos kirim, 15rb`

Atau ketik *Batal* untuk kembali ke menu."""

DEBT_PROMPT = """💳 *Catat Hutang*

Kirim pesan dengan format:
`Nama Hutang, Jumlah`

Contoh:
`Hutang ke Supplier Tepung, 300000`
`Pinjam modal teman, 500rb`

Atau ketik *Batal* untuk kembali ke menu."""

REPORT_MENU = """📊 *Laporan Keuangan*

Pilih jenis laporan:

1️⃣ *Laporan Hari Ini*
2️⃣ *Laporan Bulan Ini*

Atau ketik *Menu* untuk kembali."""


# ─────────────────────────────────────────────────────────────────
# Success Messages
# ─────────────────────────────────────────────────────────────────

def income_success(description: str, amount: float, date_str: str) -> str:
    return f"""✅ *Pemasukan Berhasil Dicatat!*

📥 Pemasukan: {description}
💰 Jumlah: {format_rupiah(amount)}
📅 Tanggal: {date_str}

Ketik *Menu* untuk kembali atau langsung catat lagi."""


def expense_success(description: str, amount: float, date_str: str) -> str:
    return f"""✅ *Pengeluaran Berhasil Dicatat!*

📤 Pengeluaran: {description}
💸 Jumlah: {format_rupiah(amount)}
📅 Tanggal: {date_str}

Ketik *Menu* untuk kembali atau langsung catat lagi."""


def debt_success(description: str, amount: float, date_str: str) -> str:
    return f"""✅ *Hutang Berhasil Dicatat!*

💳 Hutang: {description}
💰 Jumlah: {format_rupiah(amount)}
📅 Tanggal: {date_str}

Ketik *Menu* untuk kembali."""


# ─────────────────────────────────────────────────────────────────
# Report Messages
# ─────────────────────────────────────────────────────────────────

def daily_report(
    date_str: str,
    total_income: float,
    total_expense: float,
    net_profit: float,
    tx_count: int,
) -> str:
    profit_emoji = "📈" if net_profit >= 0 else "📉"
    return f"""📊 *Laporan Harian*
📅 {date_str}
━━━━━━━━━━━━━━━━━━

💰 Total Pemasukan:
    {format_rupiah(total_income)}

💸 Total Pengeluaran:
    {format_rupiah(total_expense)}

{profit_emoji} Laba Bersih:
    {format_rupiah(net_profit)}

📝 Total Transaksi: {tx_count}
━━━━━━━━━━━━━━━━━━
Ketik *Menu* untuk kembali."""


def monthly_report(
    month_name: str,
    year: int,
    total_income: float,
    total_expense: float,
    total_debt: float,
    net_profit: float,
    tx_count: int,
    debt_count: int,
) -> str:
    profit_emoji = "📈" if net_profit >= 0 else "📉"
    return f"""📊 *Laporan Bulanan*
📅 {month_name} {year}
━━━━━━━━━━━━━━━━━━

💰 Total Pemasukan:
    {format_rupiah(total_income)}

💸 Total Pengeluaran:
    {format_rupiah(total_expense)}

💳 Total Hutang Belum Lunas:
    {format_rupiah(total_debt)}

{profit_emoji} Laba Bersih:
    {format_rupiah(net_profit)}

📝 Total Transaksi: {tx_count}
🔴 Hutang Belum Lunas: {debt_count}
━━━━━━━━━━━━━━━━━━
Ketik *Menu* untuk kembali."""


# ─────────────────────────────────────────────────────────────────
# Error Messages
# ─────────────────────────────────────────────────────────────────

INVALID_FORMAT_MESSAGE = """❌ *Format tidak valid*

Pastikan format yang Anda kirim sudah benar.
Gunakan tanda koma (,) untuk memisahkan nama dan jumlah.

Contoh:
`Penjualan Keripik, 150000`

Atau ketik *Batal* untuk kembali ke menu."""

INVALID_AMOUNT_MESSAGE = """❌ *Jumlah tidak valid*

Pastikan jumlah yang Anda masukkan adalah angka positif.

Contoh yang benar:
• `150000`
• `150rb` (= 150.000)
• `1.5jt` (= 1.500.000)

Coba lagi atau ketik *Batal* untuk kembali."""

NO_DATA_MESSAGE = """📭 *Belum ada data*

Belum ada transaksi yang tercatat untuk periode ini.

Mulai catat dengan:
• Ketik *Pemasukan* untuk catat uang masuk
• Ketik *Pengeluaran* untuk catat uang keluar

Ketik *Menu* untuk kembali."""

CANCELLED_MESSAGE = """🔙 *Dibatalkan*

Kembali ke menu utama.

""" + MENU_MESSAGE

UNKNOWN_MESSAGE = """🤔 Maaf, saya tidak mengerti pesan Anda.

Ketik *Menu* untuk melihat pilihan yang tersedia,
atau *Bantuan* untuk panduan penggunaan."""

SYSTEM_ERROR_MESSAGE = """⚠️ *Terjadi kesalahan sistem*

Mohon coba lagi beberapa saat.
Jika masalah berlanjut, hubungi admin."""
