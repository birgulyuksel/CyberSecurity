import pytest
from src.checker import sha1_hex, split_prefix_suffix


def test_sha1_hex_returns_uppercase_40_chars():
    h = sha1_hex("Password123")
    assert isinstance(h, str)
    assert len(h) == 40
    # SHA-1 hex sadece 0-9A-F olmalı ve büyük harf olmalı
    assert h == h.upper()
    assert all(c in "0123456789ABCDEF" for c in h)


def test_split_prefix_suffix_rule():
    full_hash = sha1_hex("Password123")
    prefix, suffix = split_prefix_suffix(full_hash)

    assert len(prefix) == 5
    assert len(suffix) == 35
    assert full_hash == prefix + suffix
    assert prefix == full_hash[:5]
    assert suffix == full_hash[5:]


def test_split_prefix_suffix_invalid_length_raises():
    with pytest.raises(ValueError):
        split_prefix_suffix("ABC")  # 40 değil

    with pytest.raises(ValueError):
        split_prefix_suffix("A" * 41)  # 40 değil
