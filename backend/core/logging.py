"""
core/logging.py

Konfigurasi structured logging menggunakan Loguru.
Loguru lebih simple dan powerful dibanding logging standard Python.
"""

import sys
from loguru import logger

from core.config import settings


def setup_logging() -> None:
    """
    Setup konfigurasi logging global.
    
    - Development: format yang mudah dibaca manusia
    - Production: format JSON untuk log aggregation (Datadog, Loki, dll)
    
    Dipanggil sekali saat aplikasi startup.
    """
    # Hapus handler default loguru
    logger.remove()

    if settings.is_production:
        # Production: JSON format untuk log aggregation
        log_format = (
            '{{"time":"{time:YYYY-MM-DD HH:mm:ss}", '
            '"level":"{level}", '
            '"message":"{message}", '
            '"module":"{module}", '
            '"function":"{function}", '
            '"line":{line}}}'
        )
        log_level = "INFO"
    else:
        # Development: format yang mudah dibaca
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
        log_level = "DEBUG"

    # Handler untuk stdout
    logger.add(
        sys.stdout,
        format=log_format,
        level=log_level,
        colorize=not settings.is_production,
        backtrace=settings.debug,
        diagnose=settings.debug,
    )

    # Handler untuk file (selalu disimpan)
    logger.add(
        "logs/app_{time:YYYY-MM-DD}.log",
        format=log_format,
        level="INFO",
        rotation="00:00",  # Rotate setiap tengah malam
        retention="30 days",  # Simpan 30 hari
        compression="gz",  # Kompres file lama
        backtrace=True,
        diagnose=False,  # Jangan expose detail sensitif di log file
    )

    logger.info(f"📝 Logging configured | env={settings.app_env} | level={log_level}")


def get_logger(name: str):
    """
    Kembalikan logger dengan konteks nama modul.
    Berguna untuk memberi konteks pada log messages.
    """
    return logger.bind(module_name=name)
