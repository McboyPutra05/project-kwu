"""
api/routes/webhook.py

Route untuk menerima webhook dari Evolution API.

Ini adalah endpoint yang paling kritis:
- Evolution API mengirim POST ke sini setiap ada pesan masuk
- Harus responsif (return cepat, proses di background)
- Validasi IP source di production (opsional)
"""

import asyncio

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status
from loguru import logger # type: ignore

from repositories.debt_repository import DebtRepository
from repositories.transaction_repository import TransactionRepository
from repositories.user_repository import UserRepository
from schemas.webhook import WhatsAppWebhookPayload
from services.chatbot_service import ChatbotService
from services.debt_service import DebtService
from services.report_service import ReportService
from services.transaction_service import TransactionService
from services.user_service import UserService
from services.whatsapp_service import WhatsAppService
from webhook.handler import parse_evolution_payload  # type: ignore

router = APIRouter(tags=["Webhook"])


def get_chatbot_service() -> ChatbotService:
    """
    Factory function untuk membuat ChatbotService dengan semua dependency-nya.
    
    Di production, gunakan Dependency Injection framework yang lebih canggih
    atau singleton pattern untuk performa lebih baik.
    """
    user_repo = UserRepository()
    tx_repo = TransactionRepository()
    debt_repo = DebtRepository()

    user_service = UserService(user_repo)
    tx_service = TransactionService(tx_repo)
    debt_service = DebtService(debt_repo)
    report_service = ReportService(tx_service, debt_service, user_service)
    wa_service = WhatsAppService()

    return ChatbotService(
        user_service=user_service,
        user_repository=user_repo,
        transaction_service=tx_service,
        debt_service=debt_service,
        report_service=report_service,
        whatsapp_service=wa_service,
    )


@router.post(
    "/webhook/whatsapp",
    status_code=status.HTTP_200_OK,
    summary="WhatsApp Webhook",
    description="""
    Endpoint untuk menerima webhook dari Evolution API.
    
    Evolution API mengirim POST request setiap kali ada event WhatsApp
    (pesan masuk, status update, dll).
    
    **Penting**: Endpoint ini harus selalu return HTTP 200,
    bahkan jika ada error, agar Evolution API tidak retry terus-menerus.
    """,
)
async def whatsapp_webhook(
    payload: WhatsAppWebhookPayload,
    background_tasks: BackgroundTasks,
) -> dict:
    """
    Terima dan proses webhook dari Evolution API.
    
    Menggunakan BackgroundTasks FastAPI untuk memproses pesan
    secara asynchronous — endpoint return segera, proses berjalan di background.
    """
    logger.debug(f"📥 Webhook received: event={payload.event}")

    # Cek apakah ini event update QR Code
    if payload.event == "qrcode.updated":
        import base64
        import os
        
        logger.info(f"🔑 Memproses QR Code baru dari Evolution API...")
        try:
            if isinstance(payload.data, dict) and "qrcode" in payload.data:
                b64_data = payload.data["qrcode"].get("base64", "")
            elif hasattr(payload, "model_extra") and payload.model_extra and "qrcode" in payload.model_extra:
                b64_data = payload.model_extra["qrcode"].get("base64", "")
            else:
                b64_data = ""
                
            if b64_data:
                b64_string = b64_data.replace("data:image/png;base64,", "")
                img_data = base64.b64decode(b64_string)
                filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "wa_qrcode.png")
                with open(filepath, "wb") as f:
                    f.write(img_data)
                logger.info(f"✅ QR Code berhasil disimpan ke {filepath}")
            else:
                logger.warning("QR Code terdeteksi tapi tidak ada data base64.")
        except Exception as e:
            logger.error(f"Gagal memproses QR Code: {e}")
        return {"status": "qrcode_saved"}

    # Parse payload menjadi ParsedIncomingMessage
    incoming = parse_evolution_payload(payload)

    if incoming is None:
        # Payload valid tapi tidak perlu diproses (event lain, group, dll)
        return {"status": "ignored"}

    logger.info(f"💬 Processing message from {incoming.phone_number}")

    # Proses pesan di background agar response cepat
    chatbot_service = get_chatbot_service()
    background_tasks.add_task(
        chatbot_service.process_message,
        incoming,
    )

    return {"status": "processing"}
