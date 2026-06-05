"""
repositories/user_repository.py

Repository untuk operasi database User.
Extends BaseRepository dengan method spesifik user.
"""

from typing import Optional

from models.user import User
from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository untuk collection 'users'.
    
    Method tambahan di luar CRUD dasar:
    - find_by_phone: untuk lookup user dari webhook
    - get_or_create_by_phone: untuk auto-register user baru
    """

    def __init__(self) -> None:
        super().__init__(User)

    async def find_by_phone(self, phone_number: str) -> Optional[User]:
        """
        Cari user berdasarkan nomor telepon.
        
        Ini adalah operasi paling sering dipanggil —
        setiap pesan WhatsApp masuk akan trigger method ini.
        
        Args:
            phone_number: Nomor dalam format "628123456789"
        """
        return await User.find_one(User.phone_number == phone_number)

    async def get_or_create_by_phone(
        self,
        phone_number: str,
        name: Optional[str] = None,
    ) -> tuple[User, bool]:
        """
        Cari user berdasarkan nomor telepon.
        Jika tidak ada, buat user baru.
        
        Returns:
            Tuple (user, is_created):
            - user: User yang ditemukan atau dibuat
            - is_created: True jika user baru dibuat
        """
        existing_user = await self.find_by_phone(phone_number)
        if existing_user:
            return existing_user, False

        # Buat user baru
        new_user = User(phone_number=phone_number, name=name)
        created_user = await self.create(new_user)
        return created_user, True

    async def update_session_state(
        self,
        user: User,
        state: Optional[str],
    ) -> User:
        """
        Update session_state user untuk chatbot flow.
        
        Args:
            user: User object
            state: State baru. None untuk reset ke idle.
        """
        user.session_state = state
        user.update_timestamp()
        return await self.update(user)

    async def get_idle_users(self, threshold) -> list[User]:
        """
        Mendapatkan list user yang memiliki session_state aktif (tidak None)
        dan updated_at lebih lama dari threshold (idle timeout).
        """
        return await User.find(
            User.session_state != None,
            User.updated_at < threshold
        ).to_list()

    async def count_active_today(self) -> int:
        """Hitung user yang aktif (mengirim pesan) hari ini."""
        from datetime import datetime, timezone
        from utils.date_helper import get_today_range
        
        start, end = get_today_range()
        # Count distinct users dari logs hari ini
        from models.log import Log
        pipeline = [
            {"$match": {"created_at": {"$gte": start, "$lt": end}}},
            {"$group": {"_id": "$phone_number"}},
            {"$count": "total"},
        ]
        result = await Log.aggregate(pipeline).to_list()
        return result[0]["total"] if result else 0
