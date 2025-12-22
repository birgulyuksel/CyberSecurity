from unittest.mock import patch
from src.main import main


def test_e2e_password_not_pwned(capsys):
    with patch("src.main.check_password_pwned", return_value=(False, 0)):
        exit_code = main(["--password", "StrongPass123!"])

    captured = capsys.readouterr().out.lower()
    assert exit_code == 0
    assert "bulunamadı" in captured or "bulunamadı." in captured or "bulunamad" in captured


def test_e2e_password_pwned(capsys):
    with patch("src.main.check_password_pwned", return_value=(True, 42)):
        exit_code = main(["--password", "password"])

    captured = capsys.readouterr().out.lower()
    assert exit_code == 0
    assert "ihl" in captured or "pwned" in captured or "derhal" in captured
    assert "42" in captured
