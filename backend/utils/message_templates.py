"""
utils/message_templates.py

Semua template pesan WhatsApp dalam satu file terpusat.
Keuntungan: mudah diubah konten pesan tanpa menyentuh logic.
Bisa diextend untuk mendukung multi-bahasa di masa depan.
"""

from utils.number_formatter import format_rupiah


# ─────────────────────────────────────────────────────────────────
# Menu Utama (untuk List Message — teks di atas tombol)
# ─────────────────────────────────────────────────────────────────

WELCOME_TEXT = """👋 *Selamat datang di FinanceBot UMKM!*

Saya siap membantu Anda mencatat keuangan bisnis dengan mudah.

Silakan ketik nomor menu di bawah untuk memulai 👇

1️⃣ *Catat Pemasukan*
2️⃣ *Catat Pengeluaran*
3️⃣ *Catat Hutang*
4️⃣ *Lihat Laporan*"""

# Keep old constants for backward compatibility (fallback text)
WELCOME_MESSAGE = WELCOME_TEXT

MENU_TEXT = """📋 *Menu Utama FinanceBot UMKM*

Silakan ketik nomor menu yang ingin Anda gunakan 👇

1️⃣ *Catat Pemasukan*
2️⃣ *Catat Pengeluaran*
3️⃣ *Catat Hutang*
4️⃣ *Lihat Laporan*"""

MENU_MESSAGE = MENU_TEXT

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

💡 Anda tinggal ketik angka (misal: 1) untuk memilih menu.

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

REPORT_MENU_TEXT = """📊 *Laporan Keuangan*

Pilih jenis laporan yang ingin Anda lihat.
Setiap laporan disertai file Excel yang bisa diunduh 📎

Ketik angka pilihan Anda:
1️⃣ *Laporan Hari Ini*
2️⃣ *Laporan Bulan Ini*

Ketik *Batal* untuk kembali ke Menu Utama."""

# Keep old constant for backward compatibility
REPORT_MENU = REPORT_MENU_TEXT


# ─────────────────────────────────────────────────────────────────
# Success Messages
# ─────────────────────────────────────────────────────────────────

def income_success(description: str, amount: float, date_str: str) -> str:
    return f"""✅ *Pemasukan Berhasil Dicatat!*

📥 Pemasukan: {description}
💰 Jumlah: {format_rupiah(amount)}
📅 Tanggal: {date_str}

Silakan ketik langsung data pemasukan selanjutnya jika ada.
Atau ketik *Menu* untuk kembali ke pilihan utama."""


def expense_success(description: str, amount: float, date_str: str) -> str:
    return f"""✅ *Pengeluaran Berhasil Dicatat!*

📤 Pengeluaran: {description}
💸 Jumlah: {format_rupiah(amount)}
📅 Tanggal: {date_str}

Silakan ketik langsung data pengeluaran selanjutnya jika ada.
Atau ketik *Menu* untuk kembali ke pilihan utama."""


def debt_success(description: str, amount: float, date_str: str) -> str:
    return f"""✅ *Hutang Berhasil Dicatat!*

💳 Hutang: {description}
💰 Jumlah: {format_rupiah(amount)}
📅 Tanggal: {date_str}

Silakan ketik langsung data hutang selanjutnya jika ada.
Atau ketik *Menu* untuk kembali ke pilihan utama."""


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
📎 _File Excel detail terlampir di bawah._"""


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
    
    debt_text = ""
    debt_count_text = ""
    if total_debt > 0:
        debt_text = f"""
💳 Total Hutang Belum Lunas:
    {format_rupiah(total_debt)}
"""
    if debt_count > 0:
        debt_count_text = f"\n⚠️ Sisa Hutang: {debt_count}"

    return f"""📊 *Laporan Bulanan*
📅 {month_name} {year}
━━━━━━━━━━━━━━━━━━

💰 Total Pemasukan:
    {format_rupiah(total_income)}

💸 Total Pengeluaran:
    {format_rupiah(total_expense)}
{debt_text}
{profit_emoji} Laba Bersih:
    {format_rupiah(net_profit)}

📝 Total Transaksi: {tx_count}{debt_count_text}
━━━━━━━━━━━━━━━━━━
📎 _File Excel detail terlampir di bawah._"""


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

CANCELLED_TEXT = """🔙 *Dibatalkan*

Kembali ke menu utama. Ketik *Menu* untuk melihat daftar."""

# Keep old constant
CANCELLED_MESSAGE = CANCELLED_TEXT + "\n\n" + MENU_TEXT

UNKNOWN_MESSAGE = """🤔 Maaf, saya tidak mengerti pesan Anda.

Ketik *Menu* untuk melihat pilihan yang tersedia,
atau *Bantuan* untuk panduan penggunaan."""

SYSTEM_ERROR_MESSAGE = """⚠️ *Terjadi kesalahan sistem*

Mohon coba lagi beberapa saat.
Jika masalah berlanjut, hubungi admin."""
