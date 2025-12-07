from src.checker import evaluate_password_strength


def test_evaluate_password_strength_short_simple_password():
    result = evaluate_password_strength("12345")
    assert result["score"] <= 1
    assert "Parola çok kısa" in result["reasons"][0]


def test_evaluate_password_strength_strong_password():
    pwd = "SüperGüçlüParola123!"
    result = evaluate_password_strength(pwd)
    assert result["length"] == len(pwd)
    assert result["has_lower"] is True
    assert result["has_upper"] is True
    assert result["has_digit"] is True
    assert result["has_symbol"] is True
    assert result["score"] >= 3
