"""
hibp_client.py
haveibeenpwned Pwned Passwords K-anon API istemcisi.
"""

import logging
from typing import List, Tuple
import requests

from . import config

logger = logging.getLogger(__name__)


class HibpClientError(Exception):
    """HIBP istemcisi ile ilgili genel hata sınıfı."""
    pass


def build_range_url(prefix: str) -> str:
    """
    HIBP range endpoint URL'sini oluşturur.
    Örnek: https://api.pwnedpasswords.com/range/ABCDE
    """
    if len(prefix) != 5 or not all(c in "0123456789ABCDEF" for c in prefix):
        raise ValueError("Prefix 5 karakter uzunluğunda ve HEX (SHA-1) olmalıdır.")
    return config.HIBP_API_BASE_URL + config.HIBP_RANGE_ENDPOINT.format(prefix=prefix)


def query_range(prefix: str) -> List[Tuple[str, int]]:
    """
    Verilen SHA-1 hash prefix'i için HIBP range API'sini çağırır.

    Dönüş:
        List[ (suffix, count) ]  # suffix: kalan 35 karakter, count: int
    """
    url = build_range_url(prefix)
    headers = {
        "User-Agent": config.USER_AGENT,
    }
    if config.ADD_PADDING:
        headers["Add-Padding"] = "true"

    logger.debug("HIBP range endpoint çağrılıyor: %s", url)

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=config.REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        logger.error("HIBP isteği sırasında ağ hatası: %s", exc)
        raise HibpClientError(f"HIBP isteği başarısız: {exc}") from exc

    if response.status_code == 429:
        logger.error("HIBP rate limit aşıldı (HTTP 429).")
        raise HibpClientError("HIBP rate limit aşıldı (HTTP 429).")

    if not response.ok:
        logger.error("HIBP isteği başarısız. Status: %s, Body: %s",
                     response.status_code, response.text[:200])
        raise HibpClientError(
            f"HIBP isteği başarısız. HTTP {response.status_code}"
        )

    lines = response.text.splitlines()
    results: List[Tuple[str, int]] = []

    for line in lines:
        # Format: "SUFFIX:COUNT"
        if ":" not in line:
            continue
        suffix, count_str = line.split(":", 1)
        suffix = suffix.strip().upper()
        try:
            count = int(count_str.strip())
        except ValueError:
            logger.warning("Geçersiz count değeri: %s", line)
            continue
        if len(suffix) != 35:
            logger.warning("Geçersiz suffix uzunluğu: %s", suffix)
            continue
        results.append((suffix, count))

    logger.debug("HIBP'den %d kayıt alındı.", len(results))
    return results
