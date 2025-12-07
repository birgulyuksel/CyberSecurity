"""
checker.py
Parola hash'leme, HIBP sonuçlarına göre 'pwned' kontrolü ve
parola güç analizi.
"""

import hashlib
from typing import Tuple, List, Dict, Any


from .hibp_client import query_range


def sha1_hex(password: str) -> str:
    """
    Verilen parolanın SHA-1 hash'ini büyük harfli HEX string olarak döndürür.
    HIBP, SHA-1'i büyük harfle kullanıyor.
    """
    if not isinstance(password, str):
        raise TypeError("password bir string olmalıdır.")
    # UTF-8 encode + SHA-1
    digest = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    return digest


def split_prefix_suffix(sha1_hash: str) -> Tuple[str, str]:
    """
    SHA-1 hash'ini 5 karakterlik prefix ve 35 karakterlik suffix olarak ayırır.
    """
    if len(sha1_hash) != 40:
        raise ValueError("SHA-1 hash uzunluğu 40 olmalıdır.")
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    return prefix, suffix


def check_password_pwned(password: str) -> Tuple[bool, int]:
    """
    Verilen parolanın HIBP Pwned Passwords veritabanında olup olmadığını kontrol eder.

    Dönüş:
        (is_pwned: bool, count: int)
    """
    sha1_hash = sha1_hex(password)
    prefix, suffix = split_prefix_suffix(sha1_hash)

    results: List[Tuple[str, int]] = query_range(prefix)
    # Gelen sonuçlarda suffix'i ara
    for sfx, count in results:
        if sfx == suffix:
            return True, count

    return False, 0


# ---------------------------------------------------------------------------
# Bonus: Parola Güç Analizi
# ---------------------------------------------------------------------------

def evaluate_password_strength(password: str) -> Dict[str, Any]:
    """
    Basit bir parola güçlendirme analizi yapar.

    Dönüş:
        {
            "score": int,        # 0-4 arası puan
            "label": str,        # "çok zayıf", "zayıf", "orta", "güçlü", "çok güçlü"
            "reasons": [str],    # zayıflık nedenleri
            "length": int,
            "has_lower": bool,
            "has_upper": bool,
            "has_digit": bool,
            "has_symbol": bool,
        }
    """
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    reasons = []

    # Uzunluk kriterleri
    if length < 8:
        reasons.append("Parola çok kısa (en az 8 karakter olmalı).")
    elif length < 12:
        reasons.append("Parola daha uzun olabilir (12+ karakter önerilir).")

    # Karakter çeşitliliği
    categories = sum([has_lower, has_upper, has_digit, has_symbol])

    if categories <= 1:
        reasons.append("Sadece tek tip karakter içeriyor (küçük/büyük/rakam/sembol).")
    elif categories == 2:
        reasons.append("Karakter çeşitliliği sınırlı (3-4 kategori kullanmak daha güvenli).")

    # Basit heuristik skor
    score = 0

    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if categories >= 2:
        score += 1
    if categories >= 3:
        score += 1

    if score <= 1:
        label = "çok zayıf"
    elif score == 2:
        label = "zayıf"
    elif score == 3:
        label = "orta"
    elif score == 4:
        label = "güçlü"
    else:
        label = "çok güçlü"

    return {
        "score": score,
        "label": label,
        "reasons": reasons,
        "length": length,
        "has_lower": has_lower,
        "has_upper": has_upper,
        "has_digit": has_digit,
        "has_symbol": has_symbol,
    }
