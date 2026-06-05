"""
utils/number_formatter.py

Utility untuk memformat angka ke format Rupiah Indonesia.
Digunakan di seluruh aplikasi untuk konsistensi format.
"""


def format_rupiah(amount: float) -> str:
    """
    Format angka ke format Rupiah Indonesia.
    
    Contoh:
        format_rupiah(150000) → "Rp 150.000"
        format_rupiah(1500000) → "Rp 1.500.000"
        format_rupiah(1500000.50) → "Rp 1.500.000"
    
    Args:
        amount: Jumlah dalam Rupiah (angka bulat, desimal diabaikan)
    
    Returns:
        String dalam format "Rp X.XXX.XXX"
    """
    # Bulatkan ke integer (Rupiah tidak pakai desimal)
    amount_int = int(round(amount))
    
    # Format dengan separator ribuan menggunakan titik (standar Indonesia)
    formatted = f"{amount_int:,}".replace(",", ".")
    
    return f"Rp {formatted}"


def parse_amount(text: str) -> float:
    """
    Parse teks jumlah dari input user ke float.
    
    Mendukung berbagai format input:
    - "150000"
    - "150.000"
    - "150,000"
    - "150rb" → 150000
    - "1jt" → 1000000
    - "1.5jt" → 1500000
    
    Args:
        text: Teks jumlah dari user
    
    Returns:
        Jumlah dalam float
    
    Raises:
        ValueError: Jika format tidak valid atau jumlah <= 0
    """
    text = text.strip().lower()
    
    # Cek shorthand Indonesia
    multiplier = 1
    if text.endswith("jt") or text.endswith("juta"):
        multiplier = 1_000_000
        text = text.replace("jt", "").replace("juta", "").strip()
    elif text.endswith("rb") or text.endswith("ribu"):
        multiplier = 1_000
        text = text.replace("rb", "").replace("ribu", "").strip()
    
    # Tangani separator berdasarkan multiplier
    if multiplier == 1:
        # Jika angka biasa (150.000), hapus semua titik dan koma
        text = text.replace(".", "").replace(",", "").strip()
    else:
        # Jika ada multiplier (1.5jt), asumsikan titik/koma adalah desimal
        text = text.replace(",", ".").strip()
        
    try:
        amount = float(text) * multiplier
    except ValueError:
        raise ValueError(f"Format jumlah tidak valid: '{text}'")
    
    if amount <= 0:
        raise ValueError("Jumlah harus lebih dari 0")
    
    return amount
