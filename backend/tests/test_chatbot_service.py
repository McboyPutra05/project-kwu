"""
tests/test_chatbot_service.py

Unit test untuk logika chatbot — khususnya parsing input
dan state machine routing.

Test ini tidak membutuhkan koneksi MongoDB (pure unit test).
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from utils.number_formatter import format_rupiah, parse_amount
from services.chatbot_service import ChatbotService


# ─────────────────────────────────────────────────────────────────
# Tests: Number Formatter
# ─────────────────────────────────────────────────────────────────

class TestFormatRupiah:
    """Test fungsi format_rupiah."""

    def test_basic_amount(self):
        assert format_rupiah(150000) == "Rp 150.000"

    def test_large_amount(self):
        assert format_rupiah(1500000) == "Rp 1.500.000"

    def test_million(self):
        assert format_rupiah(10000000) == "Rp 10.000.000"

    def test_small_amount(self):
        assert format_rupiah(1000) == "Rp 1.000"

    def test_float_rounded(self):
        assert format_rupiah(150000.50) == "Rp 150.001" or format_rupiah(150000.50) == "Rp 150.000"

    def test_zero(self):
        assert format_rupiah(0) == "Rp 0"


class TestParseAmount:
    """Test fungsi parse_amount."""

    def test_plain_number(self):
        assert parse_amount("150000") == 150000

    def test_number_with_dots(self):
        assert parse_amount("150.000") == 150000

    def test_number_with_commas(self):
        assert parse_amount("150,000") == 150000

    def test_ribu_shorthand(self):
        assert parse_amount("150rb") == 150000

    def test_ribu_shorthand_full(self):
        assert parse_amount("150ribu") == 150000

    def test_juta_shorthand(self):
        assert parse_amount("1.5jt") == 1500000

    def test_juta_shorthand_full(self):
        assert parse_amount("2juta") == 2000000

    def test_invalid_text(self):
        with pytest.raises(ValueError):
            parse_amount("tidak valid")

    def test_zero_amount(self):
        with pytest.raises(ValueError):
            parse_amount("0")

    def test_negative_amount(self):
        with pytest.raises(ValueError):
            parse_amount("-100")


# ─────────────────────────────────────────────────────────────────
# Tests: ChatbotService._parse_transaction_input
# ─────────────────────────────────────────────────────────────────

class TestParseTransactionInput:
    """
    Test parsing input transaksi dari user.
    
    Kita test method private _parse_transaction_input
    karena ini adalah logika yang paling kritis.
    """

    def setup_method(self):
        """Setup ChatbotService dengan mock dependencies."""
        self.chatbot = ChatbotService(
            user_service=MagicMock(),
            user_repository=MagicMock(),
            transaction_service=MagicMock(),
            debt_service=MagicMock(),
            report_service=MagicMock(),
            whatsapp_service=MagicMock(),
        )

    def test_valid_format(self):
        result = self.chatbot._parse_transaction_input("Penjualan Keripik, 150000")
        assert result is not None
        description, amount = result
        assert description == "Penjualan Keripik"
        assert amount == 150000

    def test_valid_format_with_rb(self):
        result = self.chatbot._parse_transaction_input("Beli Tepung, 50rb")
        assert result is not None
        description, amount = result
        assert description == "Beli Tepung"
        assert amount == 50000

    def test_valid_format_with_juta(self):
        result = self.chatbot._parse_transaction_input("Hutang Supplier, 1jt")
        assert result is not None
        description, amount = result
        assert description == "Hutang Supplier"
        assert amount == 1000000

    def test_no_comma(self):
        """Format tanpa koma harus return None."""
        result = self.chatbot._parse_transaction_input("Penjualan Keripik 150000")
        assert result is None

    def test_empty_description(self):
        """Deskripsi kosong harus return None."""
        result = self.chatbot._parse_transaction_input(", 150000")
        assert result is None

    def test_invalid_amount(self):
        """Amount tidak valid harus return (description, None)."""
        result = self.chatbot._parse_transaction_input("Penjualan, tidak valid")
        assert result is not None
        description, amount = result
        assert description == "Penjualan"
        assert amount is None

    def test_description_with_comma(self):
        """Deskripsi dengan koma — hanya split pada koma pertama."""
        result = self.chatbot._parse_transaction_input("Jualan Keripik, Basreng, 150000")
        assert result is not None
        description, amount = result
        # Koma kedua dimasukkan ke amount — akan gagal parse
        assert description == "Jualan Keripik"


# ─────────────────────────────────────────────────────────────────
# Tests: Webhook Handler
# ─────────────────────────────────────────────────────────────────

class TestWebhookHandler:
    """Test parsing webhook Evolution API."""

    def test_parse_phone_number(self):
        """Test ekstraksi nomor dari remoteJid."""
        from webhook.handler import _extract_phone_number

        assert _extract_phone_number("628123456789@s.whatsapp.net") == "628123456789"
        assert _extract_phone_number("6281234567890@s.whatsapp.net") == "6281234567890"

    def test_ignore_group(self):
        """Group message harus di-ignore."""
        from webhook.handler import _extract_phone_number

        assert _extract_phone_number("1234567890-1234567890@g.us") is None

    def test_parse_text_message(self):
        """Test parse pesan teks biasa."""
        from webhook.handler import parse_evolution_payload
        from schemas.webhook import (
            WhatsAppWebhookPayload,
            MessageData,
            MessageKey,
            TextMessage,
        )

        payload = WhatsAppWebhookPayload(
            event="messages.upsert",
            instance="financebot",
            data=MessageData(
                key=MessageKey(
                    remoteJid="628123456789@s.whatsapp.net",
                    fromMe=False,
                    id="msg123",
                ),
                message=TextMessage(conversation="Halo"),
                messageType="conversation",
                pushName="Pak Budi",
            ),
        )

        result = parse_evolution_payload(payload)
        assert result is not None
        assert result.phone_number == "628123456789"
        assert result.message_text == "Halo"
        assert result.sender_name == "Pak Budi"

    def test_ignore_outgoing_message(self):
        """Pesan dari bot sendiri (fromMe=True) harus di-ignore."""
        from webhook.handler import parse_evolution_payload
        from schemas.webhook import (
            WhatsAppWebhookPayload,
            MessageData,
            MessageKey,
            TextMessage,
        )

        payload = WhatsAppWebhookPayload(
            event="messages.upsert",
            instance="financebot",
            data=MessageData(
                key=MessageKey(
                    remoteJid="628123456789@s.whatsapp.net",
                    fromMe=True,  # Pesan dari bot
                    id="msg123",
                ),
                message=TextMessage(conversation="Pesan dari bot"),
                messageType="conversation",
            ),
        )

        result = parse_evolution_payload(payload)
        assert result is None

    def test_ignore_non_message_event(self):
        """Event selain messages.upsert harus di-ignore."""
        from webhook.handler import parse_evolution_payload
        from schemas.webhook import WhatsAppWebhookPayload

        payload = WhatsAppWebhookPayload(
            event="messages.update",  # Bukan messages.upsert
            instance="financebot",
        )

        result = parse_evolution_payload(payload)
        assert result is None
