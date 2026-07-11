"""
main.py

Entry point aplikasi FinanceBot UMKM Backend.

Tanggung jawab:
1. Inisialisasi FastAPI application
2. Konfigurasi middleware (CORS, Rate Limiter)
3. Register semua routers
4. Lifecycle management (startup/shutdown)
5. Global exception handler
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from api.routes import auth, debts, logs, reports, transactions, users, webhook
from core.config import settings
from core.database import close_db, init_db
from core.logging import setup_logging


# ─────────────────────────────────────────────────────────────────
# Rate Limiter Setup
# ─────────────────────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)


# ─────────────────────────────────────────────────────────────────
# Background Tasks
# ─────────────────────────────────────────────────────────────────
import asyncio

async def timeout_worker():
    """
    Worker yang berjalan di background setiap 60 detik.
    Akan mengecek apakah ada user yang idle > 3 menit.
    """
    from api.routes.webhook import get_chatbot_service
    while True:
        try:
            await asyncio.sleep(60)
            service = get_chatbot_service()
            await service.process_timeouts(timeout_minutes=3)
        except asyncio.CancelledError:
            logger.info("🛑 Timeout worker cancelled")
            break
        except Exception as e:
            logger.error(f"❌ Error in timeout worker: {e}")


# ─────────────────────────────────────────────────────────────────
# Application Lifespan
# ─────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Lifespan context manager — dijalankan saat startup dan shutdown.
    
    Menggantikan event handler @app.on_event yang sudah deprecated.
    """
    # ── Startup ────────────────────────────────────────────────
    setup_logging()
    logger.info(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"📦 Environment: {settings.app_env}")

    # Inisialisasi database
    await init_db()

    logger.info("✅ Application started successfully")
    logger.info(f"📖 API Docs: http://{settings.host}:{settings.port}/docs")

    # Jalankan background worker jika tidak berjalan di Vercel (Serverless)
    import os
    if not os.environ.get("VERCEL"):
        timeout_task = asyncio.create_task(timeout_worker())
    else:
        timeout_task = None
        logger.info("⚡ Berjalan di Vercel, timeout_worker dinonaktifkan")

    yield  # Aplikasi berjalan di sini

    # ── Shutdown ───────────────────────────────────────────────
    logger.info("🛑 Shutting down application...")
    if timeout_task:
        timeout_task.cancel()
        try:
            await timeout_task
        except asyncio.CancelledError:
            pass
    
    await close_db()
    logger.info("👋 Application stopped")


# ─────────────────────────────────────────────────────────────────
# FastAPI Application
# ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    ## FinanceBot UMKM — Backend API
    
    API backend untuk sistem chatbot keuangan WhatsApp yang membantu UMKM
    mencatat pemasukan, pengeluaran, hutang, dan laporan keuangan.
    
    ### Fitur Utama
    - 🤖 **Webhook WhatsApp** — menerima & memproses pesan dari Evolution API
    - 👥 **User Management** — manajemen pengguna chatbot
    - 💰 **Transaction Management** — pencatatan transaksi keuangan
    - 💳 **Debt Management** — pencatatan dan tracking hutang
    - 📊 **Reports** — laporan keuangan harian & bulanan
    - 📝 **Logs** — audit trail percakapan chatbot
    
    ### Autentikasi
    Gunakan endpoint `/api/v1/auth/login` untuk mendapatkan JWT token,
    lalu sertakan di header: `Authorization: Bearer <token>`
    """,
    contact={
        "name": "FinanceBot UMKM Team",
        "email": "admin@financebot-umkm.id",
    },
    license_info={
        "name": "MIT License",
    },
    lifespan=lifespan,
    # Nonaktifkan docs di production
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)


# ─────────────────────────────────────────────────────────────────
# Middleware
# ─────────────────────────────────────────────────────────────────

# Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────────────
# Global Exception Handlers
# ─────────────────────────────────────────────────────────────────

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler untuk error yang tidak tertangani.
    
    Memastikan semua error mengembalikan format JSON yang konsisten,
    bukan HTML error page default dari FastAPI/Starlette.
    """
    logger.exception(f"Unhandled exception: {exc} | path={request.url.path}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal server error",
            "detail": str(exc) if settings.debug else "Terjadi kesalahan pada server",
        },
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Handler untuk ValueError — biasanya error validasi business logic."""
    logger.warning(f"ValueError: {exc} | path={request.url.path}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "message": str(exc),
        },
    )


# ─────────────────────────────────────────────────────────────────
# Router Registration
# ─────────────────────────────────────────────────────────────────

# Webhook (tidak butuh prefix /api/v1, diakses langsung oleh Evolution API)
app.include_router(webhook.router)

# API Routes
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(debts.router)
app.include_router(reports.router)
app.include_router(logs.router)


# ─────────────────────────────────────────────────────────────────
# Health Check
# ─────────────────────────────────────────────────────────────────

@app.get(
    "/health",
    tags=["System"],
    summary="Health Check",
    description="Cek status aplikasi. Digunakan oleh Docker health check.",
)
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Return HTTP 200 jika aplikasi berjalan normal.
    Docker dan load balancer menggunakan endpoint ini untuk monitoring.
    """
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@app.get(
    "/",
    tags=["System"],
    summary="Root",
    include_in_schema=False,
)
async def root() -> dict:
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_name} API",
        "version": settings.app_version,
        "docs": "/docs",
    }
