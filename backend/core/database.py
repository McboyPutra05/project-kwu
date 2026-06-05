"""
core/database.py

Inisialisasi koneksi MongoDB menggunakan Beanie ODM.
Beanie adalah ODM (Object Document Mapper) di atas Motor (async MongoDB driver).
"""

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from core.config import settings


async def init_db() -> None:
    """
    Inisialisasi koneksi MongoDB dan Beanie ODM.
    
    Dipanggil saat aplikasi startup (lifespan event di main.py).
    Import model di sini untuk menghindari circular imports.
    """
    try:
        # Import semua models Beanie di sini
        from models.user import User
        from models.transaction import Transaction
        from models.debt import Debt
        from models.log import Log
        from models.settings import AppSettings
        from models.admin import Admin

        # Buat client MongoDB
        client = AsyncIOMotorClient(
            settings.mongodb_url,
            serverSelectionTimeoutMS=5000,  # Timeout 5 detik
        )

        # Inisialisasi Beanie dengan semua document models
        await init_beanie(
            database=client[settings.mongodb_db_name],
            document_models=[
                User,
                Transaction,
                Debt,
                Log,
                AppSettings,
                Admin,
            ],
        )

        logger.info(f"✅ MongoDB connected: {settings.mongodb_db_name}")

    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        raise


async def close_db() -> None:
    """
    Tutup koneksi MongoDB saat aplikasi shutdown.
    """
    logger.info("🔌 MongoDB connection closed")
