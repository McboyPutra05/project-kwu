"""
scripts/create_admin.py

Script CLI untuk membuat akun admin pertama.

Cara penggunaan:
    # Lokal (tanpa Docker):
    cd backend
    python scripts/create_admin.py

    # Di dalam Docker:
    docker exec -it financebot_backend python scripts/create_admin.py

Script ini menggunakan motor langsung (bukan Beanie)
karena harus berjalan standalone tanpa FastAPI app.
"""

import asyncio
import sys
import os

# Tambahkan parent directory ke path agar bisa import modules backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def create_admin_interactive():
    """
    Create admin account secara interaktif via CLI.
    """
    print("\n" + "=" * 50)
    print("  FinanceBot UMKM — Create Admin Account")
    print("=" * 50 + "\n")

    # Input username
    username = input("Username: ").strip()
    if not username or len(username) < 3:
        print("❌ Username minimal 3 karakter")
        return

    # Input email
    email = input("Email: ").strip()
    if not email or "@" not in email:
        print("❌ Email tidak valid")
        return

    # Input password
    import getpass
    password = getpass.getpass("Password (min 8 karakter): ")
    if len(password) < 8:
        print("❌ Password minimal 8 karakter")
        return

    confirm_password = getpass.getpass("Konfirmasi Password: ")
    if password != confirm_password:
        print("❌ Password tidak cocok")
        return

    # Inisialisasi database
    print("\n⏳ Menghubungkan ke database...")

    try:
        from core.database import init_db
        from services.auth_service import AuthService
        from schemas.auth import AdminCreateRequest

        await init_db()

        auth_service = AuthService()
        admin = await auth_service.create_admin(
            AdminCreateRequest(
                username=username,
                email=email,
                password=password,
            )
        )

        print(f"\n✅ Admin berhasil dibuat!")
        print(f"   Username : {admin.username}")
        print(f"   Email    : {admin.email}")
        print(f"   ID       : {admin.id}")
        print(f"\n🔗 Login di: http://localhost:3000/login")

    except ValueError as e:
        print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ Database error: {e}")
        print("Pastikan MongoDB berjalan dan .env sudah dikonfigurasi.")


if __name__ == "__main__":
    asyncio.run(create_admin_interactive())
