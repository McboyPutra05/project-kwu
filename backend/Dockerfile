# ─────────────────────────────────────────────────────────────────
# FinanceBot UMKM — Backend Dockerfile
# Multi-stage build untuk image yang lebih kecil & aman
# ─────────────────────────────────────────────────────────────────

# ================================
# Stage 1: Builder
# ================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dan install dependencies terlebih dahulu
# (Docker layer caching — dependencies tidak berubah sesering kode)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt

# ================================
# Stage 2: Production
# ================================
FROM python:3.12-slim AS production

WORKDIR /app

# Install runtime dependencies saja
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages dari builder stage
COPY --from=builder /install /usr/local

# Copy source code
COPY . .

# Buat non-root user untuk keamanan
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command untuk menjalankan aplikasi
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
