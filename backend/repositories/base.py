"""
repositories/base.py

Generic Base Repository menggunakan Python Generics.

Pola Repository memisahkan logika akses data dari business logic.
Service tidak perlu tahu cara query MongoDB — cukup panggil method repository.

Keuntungan:
- Mudah di-test (bisa mock repository)
- Mudah diganti database (swap MongoDB ke SQL tanpa ubah service)
- DRY — CRUD logic tidak berulang di setiap repository
"""

from typing import Generic, List, Optional, Type, TypeVar

from beanie import Document, PydanticObjectId
from pydantic import BaseModel

# TypeVar untuk Document Beanie
DocType = TypeVar("DocType", bound=Document)


class BaseRepository(Generic[DocType]):
    """
    Generic repository dengan operasi CRUD dasar.
    
    Semua repository lain mewarisi class ini dan
    bisa menambahkan method spesifik sesuai kebutuhan.
    
    Usage:
        class UserRepository(BaseRepository[User]):
            pass
    """

    def __init__(self, model: Type[DocType]) -> None:
        self._model = model

    async def find_by_id(self, id: str) -> Optional[DocType]:
        """
        Cari dokumen berdasarkan MongoDB ObjectId.
        
        Returns:
            Document jika ditemukan, None jika tidak ada.
        """
        try:
            object_id = PydanticObjectId(id)
            return await self._model.get(object_id)
        except Exception:
            return None

    async def find_all(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> List[DocType]:
        """
        Ambil semua dokumen dengan pagination.
        
        Args:
            skip: Jumlah dokumen yang dilewati (offset).
            limit: Maksimum dokumen yang dikembalikan.
        """
        return await self._model.find_all().skip(skip).limit(limit).to_list()

    async def count_all(self) -> int:
        """Hitung total dokumen dalam collection."""
        return await self._model.find_all().count()

    async def create(self, document: DocType) -> DocType:
        """
        Simpan dokumen baru ke database.
        
        Returns:
            Document yang sudah disimpan (dengan id yang sudah di-assign).
        """
        return await document.insert()

    async def update(self, document: DocType) -> DocType:
        """
        Update dokumen yang sudah ada.
        
        Returns:
            Document yang sudah diupdate.
        """
        await document.save()
        return document

    async def delete(self, document: DocType) -> bool:
        """
        Hapus dokumen dari database.
        
        Returns:
            True jika berhasil dihapus.
        """
        await document.delete()
        return True

    async def delete_by_id(self, id: str) -> bool:
        """
        Hapus dokumen berdasarkan id.
        
        Returns:
            True jika ditemukan dan dihapus, False jika tidak ada.
        """
        document = await self.find_by_id(id)
        if document is None:
            return False
        return await self.delete(document)
