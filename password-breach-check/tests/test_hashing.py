import pytest

from src.checker import sha1_hex, split_prefix_suffix


def test_sha1_hex_known_value():
    # Bilinen bir SHA-1 değeri ile test (örnek: "password")
    # "password" -> 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
    expected = "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8"
    assert sha1_hex("password") == expected


def test_sha1_hex_type_error():
    with pytest.raises(TypeError):
        sha1_hex(123)  # type: ignore[arg-type]


def test_split_prefix_suffix_length():
    full_hash = "A" * 40
    prefix, suffix = split_prefix_suffix(full_hash)
    assert len(prefix) == 5
    assert len(suffix) == 35


def test_split_prefix_suffix_invalid_length():
    with pytest.raises(ValueError):
        split_prefix_suffix("ABC")  # çok kısa
