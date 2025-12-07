from unittest.mock import patch

from src.checker import check_password_pwned, sha1_hex, split_prefix_suffix


def test_check_password_pwned_found():
    password = "password"
    full_hash = sha1_hex(password)
    prefix, suffix = split_prefix_suffix(full_hash)

    fake_results = [
        (suffix, 123),  # eşleşen kayıt
        ("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 10),
    ]

    with patch("src.checker.query_range", return_value=fake_results) as mock_query:
        is_pwned, count = check_password_pwned(password)

    mock_query.assert_called_once_with(prefix)
    assert is_pwned is True
    assert count == 123


def test_check_password_pwned_not_found():
    password = "some-unique-password"
    full_hash = sha1_hex(password)
    prefix, _ = split_prefix_suffix(full_hash)

    fake_results = [
        ("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 10),
    ]

    with patch("src.checker.query_range", return_value=fake_results) as mock_query:
        is_pwned, count = check_password_pwned(password)

    mock_query.assert_called_once_with(prefix)
    assert is_pwned is False
    assert count == 0
