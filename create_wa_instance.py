"""
Script untuk membuat instance WhatsApp di Evolution API
dan menyimpan QR Code sebagai gambar PNG.

Jalankan: backend\venv\Scripts\python create_wa_instance.py
"""

import base64
import os
import time

import httpx

EVO_URL = "http://127.0.0.1:8182"
API_KEY = "changeme-secret-key"
INSTANCE_NAME = "bot-umkm"
QR_FILE = "wa_qrcode.png"

HEADERS = {
    "apikey": API_KEY,
    "Content-Type": "application/json",
}


def save_qrcode(base64_string: str) -> bool:
    """Simpan QR code dari base64 ke file PNG."""
    try:
        # Hapus prefix "data:image/png;base64," jika ada
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]
        img_data = base64.b64decode(base64_string)
        with open(QR_FILE, "wb") as f:
            f.write(img_data)
        return True
    except Exception as e:
        print(f"Gagal menyimpan QR: {e}")
        return False


def delete_instance(client: httpx.Client):
    """Hapus instance lama jika ada."""
    try:
        res = client.delete(f"{EVO_URL}/instance/delete/{INSTANCE_NAME}", headers=HEADERS, timeout=10)
        if res.status_code in (200, 201):
            print(f"Instance lama '{INSTANCE_NAME}' berhasil dihapus.")
        else:
            print(f"Tidak ada instance lama atau sudah terhapus.")
    except Exception:
        pass


def create_instance(client: httpx.Client) -> bool:
    """Buat instance baru."""
    payload = {
        "instanceName": INSTANCE_NAME,
        "integration": "WHATSAPP-BAILEYS",
        "qrcode": True,
    }
    try:
        res = client.post(f"{EVO_URL}/instance/create", json=payload, headers=HEADERS, timeout=15)
        data = res.json()
        print(f"Response create: status={res.status_code}")

        # Cek apakah QR langsung ada di response create
        if "qrcode" in data and data["qrcode"].get("base64"):
            print("QR Code langsung ada di response create!")
            if save_qrcode(data["qrcode"]["base64"]):
                return True

        return res.status_code in (200, 201)
    except httpx.ReadTimeout:
        # Timeout saat create itu normal, lanjut ke connect
        print("Timeout saat create (normal). Lanjut ke connect...")
        return True
    except Exception as e:
        print(f"Gagal create instance: {e}")
        return False


def fetch_qrcode(client: httpx.Client) -> bool:
    """Ambil QR Code dari endpoint connect."""
    try:
        res = client.get(f"{EVO_URL}/instance/connect/{INSTANCE_NAME}", headers=HEADERS, timeout=30)
        data = res.json()

        # Cek berbagai kemungkinan key QR code di response
        qr_base64 = None
        if "base64" in data:
            qr_base64 = data["base64"]
        elif "qrcode" in data and isinstance(data["qrcode"], dict):
            qr_base64 = data["qrcode"].get("base64")
        elif "code" in data:
            # Beberapa versi mengembalikan raw code, bukan base64
            print("QR ditemukan sebagai text code (bukan gambar).")
            print(f"\nQR Code text:\n{data['code']}\n")
            return True

        if qr_base64:
            if save_qrcode(qr_base64):
                return True

    except httpx.ReadTimeout:
        print("Timeout saat fetch QR (server masih proses)...")
    except Exception as e:
        print(f"Error fetch QR: {e}")

    return False


def main():
    print("=" * 60)
    print("  Setup WhatsApp Bot - FinanceBot UMKM")
    print("=" * 60)

    # Hapus file QR lama jika ada
    if os.path.exists(QR_FILE):
        os.remove(QR_FILE)
        print("File QR lama dihapus.")

    with httpx.Client() as client:
        # Test koneksi dulu
        try:
            res = client.get(f"{EVO_URL}/instance/fetchInstances", headers=HEADERS, timeout=5)
            print(f"Koneksi ke Evolution API: OK (port 8181)")
        except Exception as e:
            print(f"GAGAL: Tidak bisa konek ke Evolution API: {e}")
            print("Pastikan 'docker compose up -d' sudah dijalankan!")
            return

        # Hapus instance lama
        delete_instance(client)
        time.sleep(1)

        # Buat instance baru
        print(f"\nMembuat instance '{INSTANCE_NAME}'...")
        ok = create_instance(client)
        if not ok:
            print("Gagal membuat instance. Cek log Docker.")
            return

        # Cek apakah QR sudah tersimpan dari response create
        if os.path.exists(QR_FILE):
            print(f"\n[BERHASIL] QR Code tersimpan di: {QR_FILE}")
            print("-> Buka file tersebut dan scan dengan WhatsApp Anda!")
            return

        # Polling untuk QR code dari endpoint connect
        print("\nMengambil QR Code...")
        for i in range(15):
            time.sleep(3)
            print(f"Percobaan {i+1}/15...")

            if fetch_qrcode(client):
                if os.path.exists(QR_FILE):
                    print(f"\n[BERHASIL] QR Code tersimpan di: {QR_FILE}")
                    print("-> Buka file tersebut dan scan dengan WhatsApp Anda!")
                    print("-> Pilih menu 'Tautkan Perangkat' di WhatsApp HP Anda.")
                    return

    print("\n[GAGAL] QR Code tidak berhasil didapatkan setelah 15 percobaan.")
    print("Cek log Docker: docker compose logs evolution-api")


if __name__ == "__main__":
    main()
