# FinanceBot UMKM

Chatbot keuangan berbasis WhatsApp yang membantu UMKM mencatat pemasukan, pengeluaran, hutang, dan laporan keuangan.

## Tech Stack

| Layer | Teknologi |
|-------|-----------|
| Backend | Python 3.12 + FastAPI |
| Database | MongoDB 7.0 |
| ODM | Beanie (atas Motor) |
| WhatsApp Gateway | Evolution API v2 |
| Frontend | Next.js 15 + TypeScript + Tailwind CSS |
| Container | Docker + Docker Compose |
| Auth | JWT (RS256) |

## Prasyarat

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac/Linux)
- [Git](https://git-scm.com/)
- Port yang tersedia: **3000**, **8000**, **8080**, **27017**

## Quick Start (Docker)

### 1. Clone Repository

```bash
git clone <repo-url>
cd project-kwu
```

### 2. Konfigurasi Environment

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` sesuai kebutuhan (minimal ubah JWT_SECRET_KEY dan EVOLUTION_API_KEY).

### 3. Jalankan Docker Compose

```bash
docker-compose up -d
```

Tunggu semua service selesai startup (±30-60 detik).

### 4. Verifikasi Berjalan

```bash
# Cek status semua container
docker-compose ps

# Cek logs backend
docker-compose logs backend -f
```

### 5. Buat Akun Admin Pertama

```bash
docker exec -it financebot_backend python scripts/create_admin.py
```

### 6. Akses Aplikasi

| Service | URL |
|---------|-----|
| Admin Dashboard | http://localhost:3000 |
| API Backend | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| Evolution API | http://localhost:8080 |

## Development Lokal (Tanpa Docker)

### Backend

```bash
# Masuk ke folder backend
cd backend

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy dan edit .env
cp .env.example .env
# Edit MONGODB_URL ke: mongodb://localhost:27017

# Jalankan server
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
# Masuk ke folder frontend
cd frontend

# Install dependencies
npm install

# Copy .env
cp .env.example .env.local
# Edit NEXT_PUBLIC_API_URL ke: http://localhost:8000

# Jalankan dev server
npm run dev
```

## Setup WhatsApp (Evolution API)

### 1. Akses Evolution API

Buka http://localhost:8080 di browser.

### 2. Buat Instance

Via API atau UI, buat instance baru dengan nama `financebot`:

```bash
curl -X POST "http://localhost:8080/instance/create" \
  -H "apikey: changeme-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "instanceName": "financebot",
    "qrcode": true,
    "webhookUrl": "http://backend:8000/webhook/whatsapp",
    "webhookByEvents": false,
    "events": ["MESSAGES_UPSERT"]
  }'
```

### 3. Scan QR Code

```bash
curl "http://localhost:8080/instance/connect/financebot" \
  -H "apikey: changeme-secret-key"
```

Scan QR code yang muncul dengan WhatsApp di HP Anda.

### 4. Test Koneksi

Kirim pesan "Halo" ke nomor WhatsApp yang di-scan. Bot akan membalas.

## Struktur Folder

```
project-kwu/
├── backend/
│   ├── api/
│   │   ├── dependencies/    # FastAPI Dependency Injection
│   │   └── routes/          # API route handlers
│   ├── core/                # Config, Database, Security, Logging
│   ├── models/              # Beanie Document models (MongoDB)
│   ├── repositories/        # Data access layer
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # Business logic layer
│   ├── utils/               # Helper functions
│   ├── webhook/             # Webhook payload parser
│   ├── scripts/             # CLI scripts (create_admin, dll)
│   ├── tests/               # Unit & integration tests
│   ├── main.py              # FastAPI entry point
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── app/             # Next.js App Router pages
│       ├── components/      # React components
│       ├── lib/             # Utilities
│       ├── services/        # API client functions
│       └── types/           # TypeScript type definitions
└── docker-compose.yml
```

## API Documentation

Setelah backend berjalan, akses Swagger UI di:
**http://localhost:8000/docs**

### Endpoint Utama

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/webhook/whatsapp` | Webhook dari Evolution API |
| POST | `/api/v1/auth/login` | Login admin |
| POST | `/api/v1/auth/refresh` | Refresh token |
| GET | `/api/v1/users` | Daftar user |
| GET | `/api/v1/transactions` | Daftar transaksi |
| GET | `/api/v1/debts` | Daftar hutang |
| PATCH | `/api/v1/debts/{id}/pay` | Tandai hutang lunas |
| GET | `/api/v1/reports/summary` | Ringkasan dashboard |
| GET | `/api/v1/reports/daily` | Laporan harian |
| GET | `/api/v1/reports/monthly` | Laporan bulanan |
| GET | `/api/v1/logs` | Log percakapan |
| GET | `/health` | Health check |

## Chatbot Commands

User cukup mengirim pesan ke WhatsApp bot:

| Pesan User | Aksi Bot |
|------------|----------|
| `Halo` / `Hai` / `Menu` | Tampilkan menu utama |
| `Pemasukan` / `1` | Mode catat pemasukan |
| `Pengeluaran` / `2` | Mode catat pengeluaran |
| `Hutang` / `3` | Mode catat hutang |
| `Laporan` / `4` | Menu laporan |
| `Laporan Hari Ini` | Laporan harian |
| `Laporan Bulan Ini` | Laporan bulanan |
| `Batal` | Kembali ke menu |
| `Bantuan` | Panduan penggunaan |

### Format Input Transaksi

```
Nama Transaksi, Jumlah
```

Contoh:
```
Penjualan Keripik, 150000
Beli Tepung, 50rb
Hutang Supplier, 1.5jt
```

Format jumlah yang didukung:
- `150000` — angka biasa
- `150.000` — dengan titik ribuan
- `150rb` / `150ribu` — shorthand ribu
- `1.5jt` / `2juta` — shorthand juta

## Testing

```bash
cd backend

# Jalankan semua test
pytest tests/ -v

# Jalankan test dengan coverage
pytest tests/ -v --cov=. --cov-report=html
```

## Perintah Docker Berguna

```bash
# Jalankan semua service
docker-compose up -d

# Stop semua service
docker-compose down

# Rebuild backend setelah perubahan kode
docker-compose up -d --build backend

# Lihat logs real-time
docker-compose logs -f backend

# Masuk ke container backend
docker exec -it financebot_backend bash

# Buat admin baru
docker exec -it financebot_backend python scripts/create_admin.py

# Reset database (HATI-HATI: hapus semua data!)
docker-compose down -v
```

## Variabel Environment Penting

| Variable | Deskripsi | Wajib Diubah di Production |
|----------|-----------|---------------------------|
| `JWT_SECRET_KEY` | Secret key untuk JWT | ✅ Ya |
| `EVOLUTION_API_KEY` | API key Evolution API | ✅ Ya |
| `MONGO_INITDB_ROOT_PASSWORD` | Password MongoDB | ✅ Ya |
| `MONGODB_URL` | Connection string MongoDB | Sesuaikan dengan MongoDB |
| `CORS_ORIGINS` | Allowed origins frontend | Sesuaikan domain production |

## License

MIT License — bebas digunakan dan dikembangkan.
