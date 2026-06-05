"""
services/chatbot_service.py

INTI dari FinanceBot UMKM — State Machine Chatbot.

Setiap pesan WhatsApp yang masuk diproses di sini.
Chatbot menggunakan State Machine Pattern:

State disimpan di field `session_state` pada model User (di MongoDB),
sehingga state persists meskipun server restart.

┌──────────────────────────────────────────────────────────────┐
│                    STATE MACHINE DIAGRAM                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [IDLE/None] ←──────────── Batal / Menu                     │
│      │                                                       │
│      │ halo/hai/menu/start/1/2/3/4                           │
│      ▼                                                       │
│  [menu_main]                                                 │
│      │                                                       │
│      ├── "Pemasukan" / "1" ──→ [awaiting_income_input]       │
│      │                               │                       │
│      │                               │ "Nama, Jumlah"        │
│      │                               └──→ Simpan → [IDLE]   │
│      │                                                       │
│      ├── "Pengeluaran" / "2" ─→ [awaiting_expense_input]     │
│      │                               │                       │
│      │                               │ "Nama, Jumlah"        │
│      │                               └──→ Simpan → [IDLE]   │
│      │                                                       │
│      ├── "Hutang" / "3" ────→ [awaiting_debt_input]          │
│      │                               │                       │
│      │                               │ "Nama, Jumlah"        │
│      │                               └──→ Simpan → [IDLE]   │
│      │                                                       │
│      └── "Laporan" / "4" ──→ [report_menu]                  │
│                                       │                      │
│                                       ├── "Hari Ini" / "1"  │
│                                       │     └──→ Laporan     │
│                                       │                      │
│                                       └── "Bulan Ini" / "2" │
│                                             └──→ Laporan     │
└──────────────────────────────────────────────────────────────┘
"""

from loguru import logger  # type: ignore
import random

from models.log import Log
from models.user import User
from repositories.user_repository import UserRepository
from schemas.webhook import ParsedIncomingMessage
from services.debt_service import DebtService
from services.report_service import ReportService
from services.transaction_service import TransactionService
from services.user_service import UserService
from services.whatsapp_service import WhatsAppService
from utils import message_templates as tmpl
from utils.date_helper import format_short_date_id, now_wib
from utils.number_formatter import parse_amount

# ─────────────────────────────────────────────────────────────────
# Keyword Sets (lowercase)
# ─────────────────────────────────────────────────────────────────

GREETING_KEYWORDS = {"halo", "hai", "hello", "hi", "start", "mulai", "menu", "home"}
INCOME_KEYWORDS = {"pemasukan", "masuk", "income", "1"}
EXPENSE_KEYWORDS = {"pengeluaran", "keluar", "expense", "pengeluaran", "2"}
DEBT_KEYWORDS = {"hutang", "utang", "debt", "3"}
REPORT_KEYWORDS = {"laporan", "report", "4"}
CANCEL_KEYWORDS = {"batal", "cancel", "kembali", "back"}
DAILY_REPORT_KEYWORDS = {"laporan hari ini", "hari ini", "1", "daily"}
MONTHLY_REPORT_KEYWORDS = {"laporan bulan ini", "bulan ini", "2", "monthly"}
HELP_KEYWORDS = {"bantuan", "help", "?"}


class ChatbotService:
    """
    State machine chatbot untuk FinanceBot UMKM.

    Menerima ParsedIncomingMessage, memproses state,
    dan mengembalikan response text yang akan dikirim ke user.
    """

    def __init__(
        self,
        user_service: UserService,
        user_repository: UserRepository,
        transaction_service: TransactionService,
        debt_service: DebtService,
        report_service: ReportService,
        whatsapp_service: WhatsAppService,
    ) -> None:
        self._user_service = user_service
        self._user_repo = user_repository
        self._tx_service = transaction_service
        self._debt_service = debt_service
        self._report_service = report_service
        self._wa_service = whatsapp_service

    async def process_message(self, incoming: ParsedIncomingMessage) -> None:
        """
        Entry point — proses pesan masuk dan kirim balasan.

        Flow:
        1. Dapatkan/buat user
        2. Cek session_state user
        3. Proses pesan berdasarkan state
        4. Kirim balasan via WhatsApp
        5. Log percakapan
        """
        phone = incoming.phone_number
        text = incoming.message_text.strip()
        text_lower = text.lower()

        logger.info(f"📩 Incoming message | phone={phone} | text={text!r}")

        # ── 1. Get or create user ──────────────────────────────
        user, is_new = await self._user_service.get_or_create_user(
            phone_number=phone,
            name=incoming.sender_name,
        )

        # ── 2. Tentukan response berdasarkan state ─────────────
        response_text = await self._dispatch(
            user=user, text=text, text_lower=text_lower
        )

        # ── 3. Tandai sudah dibaca & Kirim balasan via WhatsApp ─
        # Simulasi human: Baca dulu (centang biru)
        if incoming.message_id:
            await self._wa_service.mark_as_read(phone, incoming.message_id)

        # Simulasi human: Ngetik 1-2 detik sebelum balas
        delay_ms = random.randint(1000, 2000)
        await self._wa_service.send_text_message(
            phone_number=phone,
            message=response_text,
            delay_ms=delay_ms,
        )

        # ── 4. Simpan log percakapan ───────────────────────────
        await self._save_log(phone=phone, message=text, response=response_text)

    async def _dispatch(self, user: User, text: str, text_lower: str) -> str:
        """
        Router utama — tentukan handler berdasarkan session_state.
        """
        current_state = user.session_state

        # ── Cancel selalu bisa dilakukan dari state apapun ──
        if text_lower in CANCEL_KEYWORDS:
            await self._user_repo.update_session_state(user, None)
            return tmpl.CANCELLED_MESSAGE

        # ── Help selalu bisa dilakukan dari state apapun ────
        if text_lower in HELP_KEYWORDS:
            return tmpl.HELP_MESSAGE

        # ── Route berdasarkan state saat ini ─────────────────
        if current_state is None or current_state == "menu_main":
            return await self._handle_menu(user, text_lower)

        elif current_state == "awaiting_income_input":
            return await self._handle_income_input(user, text)

        elif current_state == "awaiting_expense_input":
            return await self._handle_expense_input(user, text)

        elif current_state == "awaiting_debt_input":
            return await self._handle_debt_input(user, text)

        elif current_state == "report_menu":
            return await self._handle_report_menu(user, text_lower)

        else:
            # State tidak dikenal — reset ke idle
            await self._user_repo.update_session_state(user, None)
            return tmpl.MENU_MESSAGE

    # ─────────────────────────────────────────────────────────────
    # Handler: Menu Utama
    # ─────────────────────────────────────────────────────────────

    async def _handle_menu(self, user: User, text_lower: str) -> str:
        """
        Handle pesan ketika user di menu utama atau idle.
        """
        # Salam / inisiasi
        if text_lower in GREETING_KEYWORDS:
            await self._user_repo.update_session_state(user, "menu_main")
            return tmpl.WELCOME_MESSAGE

        # Navigasi ke sub-menu
        if text_lower in INCOME_KEYWORDS:
            await self._user_repo.update_session_state(user, "awaiting_income_input")
            return tmpl.INCOME_PROMPT

        if text_lower in EXPENSE_KEYWORDS:
            await self._user_repo.update_session_state(user, "awaiting_expense_input")
            return tmpl.EXPENSE_PROMPT

        if text_lower in DEBT_KEYWORDS:
            await self._user_repo.update_session_state(user, "awaiting_debt_input")
            return tmpl.DEBT_PROMPT

        if text_lower in REPORT_KEYWORDS:
            await self._user_repo.update_session_state(user, "report_menu")
            return tmpl.REPORT_MENU

        # Shortcut laporan langsung
        if "hari ini" in text_lower:
            return await self._generate_daily_report(user)

        if "bulan ini" in text_lower:
            return await self._generate_monthly_report(user)

        # Pesan tidak dikenal
        return tmpl.UNKNOWN_MESSAGE

    # ─────────────────────────────────────────────────────────────
    # Handler: Input Pemasukan
    # ─────────────────────────────────────────────────────────────

    async def _handle_income_input(self, user: User, text: str) -> str:
        """
        Proses input pemasukan dari user.
        Format yang diharapkan: "Nama Pemasukan, Jumlah"
        """
        result = self._parse_transaction_input(text)
        if result is None:
            return tmpl.INVALID_FORMAT_MESSAGE

        description, amount = result
        if amount is None:
            return tmpl.INVALID_AMOUNT_MESSAGE

        # Simpan transaksi
        await self._tx_service.record_income(
            user_id=str(user.id),
            phone_number=user.phone_number,
            description=description,
            amount=amount,
        )

        # Reset state
        await self._user_repo.update_session_state(user, None)

        date_str = format_short_date_id(now_wib())
        return tmpl.income_success(description, amount, date_str)

    # ─────────────────────────────────────────────────────────────
    # Handler: Input Pengeluaran
    # ─────────────────────────────────────────────────────────────

    async def _handle_expense_input(self, user: User, text: str) -> str:
        """
        Proses input pengeluaran dari user.
        Format yang diharapkan: "Nama Pengeluaran, Jumlah"
        """
        result = self._parse_transaction_input(text)
        if result is None:
            return tmpl.INVALID_FORMAT_MESSAGE

        description, amount = result
        if amount is None:
            return tmpl.INVALID_AMOUNT_MESSAGE

        await self._tx_service.record_expense(
            user_id=str(user.id),
            phone_number=user.phone_number,
            description=description,
            amount=amount,
        )

        await self._user_repo.update_session_state(user, None)

        date_str = format_short_date_id(now_wib())
        return tmpl.expense_success(description, amount, date_str)

    # ─────────────────────────────────────────────────────────────
    # Handler: Input Hutang
    # ─────────────────────────────────────────────────────────────

    async def _handle_debt_input(self, user: User, text: str) -> str:
        """
        Proses input hutang dari user.
        Format yang diharapkan: "Nama Hutang, Jumlah"
        """
        result = self._parse_transaction_input(text)
        if result is None:
            return tmpl.INVALID_FORMAT_MESSAGE

        description, amount = result
        if amount is None:
            return tmpl.INVALID_AMOUNT_MESSAGE

        await self._debt_service.record_debt(
            user_id=str(user.id),
            phone_number=user.phone_number,
            description=description,
            amount=amount,
        )

        await self._user_repo.update_session_state(user, None)

        date_str = format_short_date_id(now_wib())
        return tmpl.debt_success(description, amount, date_str)

    # ─────────────────────────────────────────────────────────────
    # Handler: Menu Laporan
    # ─────────────────────────────────────────────────────────────

    async def _handle_report_menu(self, user: User, text_lower: str) -> str:
        """
        Handle pilihan di menu laporan.
        """
        if text_lower in DAILY_REPORT_KEYWORDS or "hari ini" in text_lower:
            await self._user_repo.update_session_state(user, None)
            return await self._generate_daily_report(user)

        if text_lower in MONTHLY_REPORT_KEYWORDS or "bulan ini" in text_lower:
            await self._user_repo.update_session_state(user, None)
            return await self._generate_monthly_report(user)

        # Pilihan tidak valid
        return tmpl.REPORT_MENU

    # ─────────────────────────────────────────────────────────────
    # Report Generators
    # ─────────────────────────────────────────────────────────────

    async def _generate_daily_report(self, user: User) -> str:
        """Generate dan format laporan harian."""
        try:
            report = await self._report_service.get_daily_report(user.phone_number)
            from utils.date_helper import format_short_date_id
            import datetime

            date_str = format_short_date_id(
                datetime.datetime.combine(report.report_date, datetime.time.min)
            )
            return tmpl.daily_report(
                date_str=date_str,
                total_income=report.total_income,
                total_expense=report.total_expense,
                net_profit=report.net_profit,
                tx_count=report.transaction_count,
            )
        except Exception as e:
            logger.error(f"Error generating daily report: {e}")
            return tmpl.SYSTEM_ERROR_MESSAGE

    async def _generate_monthly_report(self, user: User) -> str:
        """Generate dan format laporan bulanan."""
        try:
            report = await self._report_service.get_monthly_report(user.phone_number)
            return tmpl.monthly_report(
                month_name=report.month_name,
                year=report.year,
                total_income=report.total_income,
                total_expense=report.total_expense,
                total_debt=report.total_debt,
                net_profit=report.net_profit,
                tx_count=report.transaction_count,
                debt_count=report.debt_count,
            )
        except Exception as e:
            logger.error(f"Error generating monthly report: {e}")
            return tmpl.SYSTEM_ERROR_MESSAGE

    # ─────────────────────────────────────────────────────────────
    # Input Parser
    # ─────────────────────────────────────────────────────────────

    def _parse_transaction_input(
        self,
        text: str,
    ) -> tuple[str, float] | None:
        """
        Parse input transaksi dari user.
        Format: "Nama Transaksi, Jumlah"

        Returns:
            Tuple (description, amount) jika valid.
            None jika format salah.
            (description, None) jika amount tidak valid.
        """
        # Harus ada koma sebagai separator
        if "," not in text:
            return None

        # Split hanya pada koma pertama
        parts = text.split(",", 1)
        if len(parts) != 2:
            return None

        description = parts[0].strip()
        amount_text = parts[1].strip()

        if not description:
            return None

        try:
            amount = parse_amount(amount_text)
            return description, amount
        except ValueError:
            return description, None  # type: ignore

    # ─────────────────────────────────────────────────────────────
    # Logging
    # ─────────────────────────────────────────────────────────────

    async def _save_log(self, phone: str, message: str, response: str) -> None:
        """Simpan percakapan ke collection logs."""
        try:
            log = Log(
                phone_number=phone,
                message=message,
                response=response,
            )
            await log.insert()
        except Exception as e:
            # Log error tidak boleh menghentikan flow utama
            logger.warning(f"⚠️ Failed to save log: {e}")

    # ─────────────────────────────────────────────────────────────
    # Background Tasks
    # ─────────────────────────────────────────────────────────────

    async def process_timeouts(self, timeout_minutes: int = 3) -> None:
        """
        Cari user yang idle selama timeout_minutes, lalu kirim pesan penutup.
        Reset state mereka kembali ke None.
        """
        from datetime import datetime, timezone, timedelta
        
        threshold = datetime.now(timezone.utc) - timedelta(minutes=timeout_minutes)
        idle_users = await self._user_repo.get_idle_users(threshold)
        
        if not idle_users:
            return
            
        timeout_message = (
            "Halo sobat Chatet, karena tidak ada aktivitas dalam beberapa menit, "
            "percakapan ini akan tertutup secara otomatis.\n\n"
            "Sobat Chatet bisa langsung chat kembali kapan saja atau bisa "
            "langsung kirim pesan sekarang untuk melanjutkan."
        )
        
        for user in idle_users:
            logger.info(f"⏰ Timeout reached for user {user.phone_number}, resetting state.")
            # Kirim pesan penutup
            await self._wa_service.send_text_message(
                phone_number=user.phone_number, 
                message=timeout_message
            )
            # Reset state ke None (IDLE)
            await self._user_repo.update_session_state(user, None)
