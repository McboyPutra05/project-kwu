"""
schemas/webhook.py

Schema untuk payload webhook dari Evolution API.
Disesuaikan dengan format Evolution API v2.

Dokumentasi Evolution API: https://doc.evolution-api.com
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


# ─────────────────────────────────────────────────────────────────
# Evolution API Webhook Payload Structure
# ─────────────────────────────────────────────────────────────────

class MessageKey(BaseModel):
    """Identifikasi unik sebuah pesan WhatsApp."""
    remoteJid: str  # Format: "628123456789@s.whatsapp.net"
    fromMe: bool
    id: str


class TextMessage(BaseModel):
    """Konten pesan teks."""
    conversation: Optional[str] = None
    extendedTextMessage: Optional[Dict[str, Any]] = None


class MessageData(BaseModel):
    """Data pesan dari Evolution API."""
    key: MessageKey
    message: Optional[TextMessage] = None
    messageType: Optional[str] = None
    messageTimestamp: Optional[int] = None
    pushName: Optional[str] = None  # Nama profil WhatsApp pengirim


class WhatsAppWebhookPayload(BaseModel):
    """
    Payload utama webhook dari Evolution API.
    
    Evolution API mengirim POST request ke /webhook/whatsapp
    setiap kali ada event WhatsApp (pesan masuk, status, dll).
    """
    event: str  # "messages.upsert", "messages.update", dll.
    instance: str  # Nama instance Evolution API
    data: Optional[Any] = None

    # Metadata tambahan (opsional)
    destination: Optional[str] = None
    date_time: Optional[str] = None
    sender: Optional[str] = None
    server_url: Optional[str] = None
    apikey: Optional[str] = None

    model_config = {"extra": "allow"}  # Allow field tambahan dari Evolution API


class ParsedIncomingMessage(BaseModel):
    """
    Pesan yang sudah di-parse dan siap diproses ChatbotService.
    Abstraksi dari format Evolution API yang verbose.
    """
    phone_number: str  # Sudah dalam format bersih: "628123456789"
    message_text: str  # Teks pesan yang sudah di-strip
    message_id: str    # ID unik dari pesan masuk (untuk mark as read)
    sender_name: Optional[str] = None  # Nama profil WhatsApp


# ─────────────────────────────────────────────────────────────────
# Evolution API Send Message Payload
# ─────────────────────────────────────────────────────────────────

class SendTextPayload(BaseModel):
    """Payload untuk mengirim pesan teks via Evolution API."""
    number: str
    text: str


class SendButtonPayload(BaseModel):
    """Payload untuk mengirim pesan dengan tombol (button message)."""
    number: str
    title: str
    description: str
    footer: Optional[str] = None
    buttons: List[Dict[str, str]]
