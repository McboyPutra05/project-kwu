"""
webhook/handler.py

Parser payload webhook dari Evolution API.

Tanggung jawab:
1. Parse raw payload dari Evolution API
2. Validasi bahwa payload adalah pesan masuk yang valid
3. Ekstrak phone number dan teks pesan
4. Kembalikan ParsedIncomingMessage yang siap diproses ChatbotService

Memisahkan parsing dari routing memudahkan testing
dan memungkinkan support multi-provider di masa depan.
"""

from typing import Optional

from loguru import logger  # type: ignore

from schemas.webhook import ParsedIncomingMessage, WhatsAppWebhookPayload


def parse_evolution_payload(
    payload: WhatsAppWebhookPayload,
) -> Optional[ParsedIncomingMessage]:
    """
    Parse payload Evolution API menjadi ParsedIncomingMessage.

    Evolution API mengirim berbagai jenis event (message, status, dll).
    Kita hanya proses event "messages.upsert" dari pesan masuk (bukan dari kita sendiri).

    Args:
        payload: Raw webhook payload dari Evolution API

    Returns:
        ParsedIncomingMessage jika valid dan harus diproses.
        None jika harus di-ignore.
    """
    # Hanya proses event pesan baru
    if payload.event not in ("messages.upsert", "message"):
        logger.debug(f"Ignoring event: {payload.event}")
        return None

    # Pastikan ada data pesan
    if not payload.data:
        logger.debug("Payload has no data")
        return None

    message_data = None
    if isinstance(payload.data, dict):
        try:
            from schemas.webhook import MessageData
            message_data = MessageData(**payload.data)
        except Exception as e:
            logger.error(f"Failed to parse MessageData: {e}")
            return None
    else:
        # Mungkin sudah object Pydantic jika ter-parse otomatis
        message_data = payload.data
        
    if not message_data or not hasattr(message_data, 'key'):
        return None

    # Abaikan pesan yang dikirim bot sendiri (fromMe=True)
    if message_data.key.fromMe:
        logger.debug("Ignoring outgoing message (fromMe=True)")
        return None

    # Ekstrak teks pesan
    message_text = _extract_message_text(message_data)
    if not message_text:
        logger.debug(f"No text found in message type: {message_data.messageType}")
        return None

    # Ekstrak dan bersihkan nomor telepon
    phone_number = _extract_phone_number(message_data.key.remoteJid)
    if not phone_number:
        logger.warning(
            f"Cannot extract phone from remoteJid: {message_data.key.remoteJid}"
        )
        return None

    # Ekstrak nama pengirim
    sender_name = message_data.pushName

    # Extract ID pesan untuk mark as read
    message_id = message_data.key.id

    return ParsedIncomingMessage(
        phone_number=phone_number,
        message_text=message_text.strip(),
        message_id=message_id,
        sender_name=sender_name,
    )


def _extract_message_text(message_data) -> Optional[str]:
    """
    Ekstrak teks dari berbagai tipe pesan WhatsApp.

    WhatsApp memiliki banyak tipe pesan (text, image caption, dll).
    Kita ambil teks dari tipe yang paling umum.
    """
    if not message_data.message:
        return None

    msg = message_data.message

    # Teks biasa
    if msg.conversation:
        return msg.conversation

    # Extended text (pesan dengan preview link, format, dll)
    if msg.extendedTextMessage:
        return msg.extendedTextMessage.get("text", "")

    return None


def _extract_phone_number(remote_jid: str) -> Optional[str]:
    """
    Ekstrak nomor telepon bersih dari remoteJid WhatsApp.

    remoteJid format:
    - Pesan personal: "628123456789@s.whatsapp.net"
    - Pesan group: "1234567890-1234567890@g.us" (diabaikan)

    Returns:
        Nomor telepon (misal: "628123456789"), atau None jika group/invalid.
    """
    if not remote_jid:
        return None

    # Abaikan pesan dari group
    if "@g.us" in remote_jid:
        logger.debug(f"Ignoring group message: {remote_jid}")
        return None

    # Ambil bagian sebelum "@"
    phone = remote_jid.split("@")[0]

    # Hapus karakter non-digit
    phone = "".join(filter(str.isdigit, phone))

    if not phone:
        return None

    return phone
