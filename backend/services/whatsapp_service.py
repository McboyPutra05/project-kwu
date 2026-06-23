"""
services/whatsapp_service.py

Wrapper untuk Evolution API — WhatsApp Gateway.
Semua komunikasi keluar (kirim pesan) melalui service ini.

Keuntungan memisahkan di service sendiri:
- Mudah di-swap jika ganti provider WhatsApp
- Mudah di-mock saat testing
- Error handling terpusat
"""

import httpx
from loguru import logger  # type: ignore

from core.config import settings


class WhatsAppService:
    """
    Service untuk mengirim pesan WhatsApp via Evolution API.

    Evolution API Docs: https://doc.evolution-api.com
    """

    def __init__(self) -> None:
        self._base_url = settings.evolution_api_url
        self._api_key = settings.evolution_api_key
        self._instance = settings.evolution_instance_name
        self._headers = {
            "apikey": self._api_key,
            "Content-Type": "application/json",
        }

    async def send_text_message(
        self,
        phone_number: str,
        message: str,
        delay_ms: int = 0,
    ) -> bool:
        """
        Kirim pesan teks ke nomor WhatsApp.

        Args:
            phone_number: Nomor dalam format "628123456789"
            message: Teks pesan yang akan dikirim
            delay_ms: Waktu jeda (simulasi ngetik) dalam milliseconds


        Returns:
            True jika berhasil, False jika gagal
        """
        url = f"{self._base_url}/message/sendText/{self._instance}"

        payload = {
            "number": phone_number,
            "text": message,
            "delay": delay_ms,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._headers,
                )
                response.raise_for_status()
                logger.debug(f"📤 Message sent to {phone_number}")
                return True

        except httpx.TimeoutException:
            logger.error(f"❌ Timeout sending to {phone_number}")
            return False

        except httpx.HTTPStatusError as e:
            logger.error(
                f"❌ HTTP error sending to {phone_number}: "
                f"{e.response.status_code} - {e.response.text}"
            )
            return False

        except Exception as e:
            logger.error(f"❌ Unexpected error sending to {phone_number}: {e}")
            return False

    async def mark_as_read(
        self,
        phone_number: str,
        message_id: str,
    ) -> bool:
        """
        Tandai pesan dari user sebagai sudah dibaca (read/blue tick).
        
        Args:
            phone_number: Nomor pengirim
            message_id: ID pesan yang diterima
        """
        url = f"{self._base_url}/chat/markMessageAsRead/{self._instance}"
        payload = {
            "readMessages": [
                {
                    "remoteJid": f"{phone_number}@s.whatsapp.net",
                    "fromMe": False,
                    "id": message_id,
                }
            ]
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._headers,
                )
                response.raise_for_status()
                logger.debug(f"👀 Message {message_id} marked as read")
                return True
        except Exception as e:
            logger.warning(f"⚠️ Failed to mark message as read: {e}")
            return False

    async def send_reaction(
        self,
        phone_number: str,
        message_key: str,
        reaction: str = "👍",
    ) -> bool:
        """
        Kirim reaction emoji ke pesan WhatsApp.

        Args:
            phone_number: Nomor tujuan
            message_key: ID pesan yang akan di-react
            reaction: Emoji reaction
        """
        url = f"{self._base_url}/message/sendReaction/{self._instance}"

        payload = {
            "key": {
                "remoteJid": f"{phone_number}@s.whatsapp.net",
                "fromMe": False,
                "id": message_key,
            },
            "reaction": reaction,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._headers,
                )
                response.raise_for_status()
                return True

        except Exception as e:
            logger.warning(f"⚠️ Failed to send reaction: {e}")
            return False

    async def check_instance_status(self) -> dict:
        """
        Cek status koneksi instance Evolution API.
        Berguna untuk health check dan monitoring.

        Returns:
            Dict berisi status koneksi (connected/disconnected)
        """
        url = f"{self._base_url}/instance/connectionState/{self._instance}"

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url, headers=self._headers)
                response.raise_for_status()
                return response.json()

        except Exception as e:
            logger.error(f"❌ Cannot check Evolution API status: {e}")
            return {"state": "error", "error": str(e)}


    async def send_document(
        self,
        phone_number: str,
        file_path: str,
        filename: str,
        caption: str = "",
    ) -> bool:
        """
        Kirim file dokumen (Excel, PDF, dll) via WhatsApp.
        
        Menggunakan Evolution API sendMedia endpoint dengan mediatype=document.
        File dibaca dari disk, di-encode base64, dan dikirim.
        
        Args:
            phone_number: Nomor tujuan
            file_path: Path absolut ke file yang akan dikirim
            filename: Nama file yang ditampilkan ke user
            caption: Pesan tambahan yang menyertai file
        """
        import base64
        import os

        url = f"{self._base_url}/message/sendMedia/{self._instance}"

        try:
            if not os.path.exists(file_path):
                logger.error(f"❌ File not found: {file_path}")
                return False

            with open(file_path, "rb") as f:
                file_bytes = f.read()
            
            b64_data = base64.b64encode(file_bytes).decode("utf-8")
            
            # Tentukan mimetype dari ekstensi
            ext = os.path.splitext(filename)[1].lower()
            mime_map = {
                ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ".xls": "application/vnd.ms-excel",
                ".pdf": "application/pdf",
                ".csv": "text/csv",
            }
            mimetype = mime_map.get(ext, "application/octet-stream")

            payload = {
                "number": phone_number,
                "mediatype": "document",
                "mimetype": mimetype,
                "caption": caption,
                "fileName": filename,
                "media": b64_data,
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url, json=payload, headers=self._headers
                )
                response.raise_for_status()
                logger.info(f"📎 Document '{filename}' sent to {phone_number}")
                return True

        except httpx.HTTPStatusError as e:
            logger.error(
                f"❌ HTTP error sending document to {phone_number}: "
                f"{e.response.status_code} - {e.response.text}"
            )
            return False

        except Exception as e:
            logger.error(f"❌ Failed to send document to {phone_number}: {e}")
            return False

