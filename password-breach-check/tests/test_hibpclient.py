from unittest.mock import patch, Mock

import pytest

from src.hibp_client import build_range_url, query_range, HibpClientError
from src import config


def test_build_range_url_valid():
    prefix = "ABCDE"
    url = build_range_url(prefix)
    assert url == config.HIBP_API_BASE_URL + config.HIBP_RANGE_ENDPOINT.format(prefix=prefix)


def test_build_range_url_invalid_prefix_length():
    with pytest.raises(ValueError):
        build_range_url("ABC")  # 5 karakter değil


def test_query_range_parses_response_correctly():
    fake_body = "1234567890ABCDEF1234567890ABCDE1234:42\n" \
                "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF:100\n"

    mock_response = Mock()
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.text = fake_body

    with patch("src.hibp_client.requests.get", return_value=mock_response) as mock_get:
        results = query_range("ABCDE")

    mock_get.assert_called_once()
    assert len(results) == 2
    assert results[0] == ("1234567890ABCDEF1234567890ABCDE1234", 42)
    assert results[1] == ("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 100)


def test_query_range_handles_http_error():
    mock_response = Mock()
    mock_response.ok = False
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"

    with patch("src.hibp_client.requests.get", return_value=mock_response):
        with pytest.raises(HibpClientError):
            query_range("ABCDE")


def test_query_range_handles_rate_limit():
    mock_response = Mock()
    mock_response.ok = False
    mock_response.status_code = 429
    mock_response.text = "Too Many Requests"

    with patch("src.hibp_client.requests.get", return_value=mock_response):
        with pytest.raises(HibpClientError):
            query_range("ABCDE")
