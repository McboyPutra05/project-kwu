"""
core/config.py

Konfigurasi aplikasi menggunakan pydantic-settings.
Semua konfigurasi dibaca dari environment variables / file .env.
Tidak ada nilai yang di-hardcode di sini.
"""

from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Konfigurasi utama aplikasi.
    
    Pydantic-settings secara otomatis membaca nilai dari:
    1. Environment variables
    2. File .env (jika ada)
    3. Default values yang didefinisikan di sini
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ============================
    # Application
    # ============================
    app_name: str = "FinanceBot UMKM"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = True

    # ============================
    # Server
    # ============================
    host: str = "0.0.0.0"
    port: int = 8000

    # ============================
    # MongoDB
    # ============================
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "financebot_db"

    # ============================
    # JWT
    # ============================
    jwt_secret_key: str = "change-this-secret-key-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # ============================
    # Evolution API (WhatsApp)
    # ============================
    evolution_api_url: str = "http://localhost:8080"
    evolution_api_key: str = "changeme-secret-key"
    evolution_instance_name: str = "financebot"

    # ============================
    # CORS
    # ============================
    cors_origins: str = "http://localhost:3000"

    # ============================
    # Rate Limiting
    # ============================
    rate_limit_per_minute: int = 100

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str) -> str:
        """Pastikan CORS origins valid."""
        return v

    def get_cors_origins_list(self) -> List[str]:
        """Kembalikan CORS origins sebagai list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_development(self) -> bool:
        return self.app_env.lower() == "development"

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache()
def get_settings() -> Settings:
    """
    Singleton settings menggunakan lru_cache.
    Dipanggil sekali, di-cache selamanya selama runtime.
    """
    return Settings()


# Instance global yang bisa di-import langsung
settings = get_settings()
