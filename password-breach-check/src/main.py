"""
main.py
Komut satırından parola ihlal kontrolü için CLI arayüzü.
"""

import argparse
import getpass
import logging
import sys
import json

from .checker import check_password_pwned, evaluate_password_strength
from .hibp_client import HibpClientError


def setup_logging(verbose: bool = False) -> None:
    """
    Basit logging yapılandırmasıdır.
    Güvenlik amaçlı parola veya hash'leri asla log'lamaz.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Password Breach Check (haveibeenpwned K-anonim entegrasyonu)"
    )
    parser.add_argument(
        "-p", "--password",
        help="Kontrol edilecek parola. Güvenlik nedeniyle önerilmez; "
             "parolayı gizli girmek için argümansız çalıştır.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Daha detaylı log çıktısı.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Sonucu JSON formatında yazdırır.",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    setup_logging(verbose=args.verbose)

    if args.password:
        password = args.password
        print("UYARI: Parolayı komut satırı argümanı ile vermek güvenli değildir.")
    else:
        # getpass ile gizli giriş 
        password = getpass.getpass("Lütfen kontrol etmek istediğiniz parolayı girin: ")

    if not password:
        print("Boş parola kontrol edilemez.")
        return 1

    # Önce güç analizi yap
    strength = evaluate_password_strength(password)

    try:
        is_pwned, count = check_password_pwned(password)
    except HibpClientError as exc:
        if args.json:
            error_payload = {
                "status": "error",
                "error_type": "hibp_client_error",
                "message": str(exc),
            }
            print(json.dumps(error_payload, ensure_ascii=False))
        else:
            print(f"Hata: HIBP servisi ile iletişimde problem oluştu: {exc}")
        return 2
    except Exception as exc:  # beklenmeyen hatalar için
        if args.json:
            error_payload = {
                "status": "error",
                "error_type": "unexpected_error",
                "message": str(exc),
            }
            print(json.dumps(error_payload, ensure_ascii=False))
        else:
            print(f"Beklenmeyen bir hata oluştu: {exc}")
        return 3

    if args.json:
        payload = {
            "status": "ok",
            "pwned": is_pwned,
            "pwned_count": count,
            "strength": strength,
        }
        print(json.dumps(payload, ensure_ascii=False))
    else:
        # İnsan okunur çıktı
        print(f"Parola uzunluğu: {strength['length']}")
        print(f"Parola gücü: {strength['label']} (skor: {strength['score']}/4)")

        if strength["reasons"]:
            print("Değerlendirme notları:")
            for reason in strength["reasons"]:
                print(f" - {reason}")

        print()

        if is_pwned:
            print(
                f"⚠ BU PAROLA İHLAL EDİLMİŞ! "
                f"haveibeenpwned veritabanında yaklaşık {count} kez görünüyor."
            )
            print("Bu parolayı DERHAL değiştirmeli ve tekrar kullanmamalısınız. :(")
        else:
            print("Bu parola HIBP Pwned Passwords veritabanında bulunamadı.")
            print("Yine de güçlü ve benzersiz parola kullanmaya dikkat edin. :)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
