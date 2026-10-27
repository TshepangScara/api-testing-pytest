import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"


def test_valid_credentials_return_token():
    payload = {"username": "admin", "password": "password123"}

    response = requests.post(f"{BASE_URL}/auth", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "token" in body
    assert body["token"]

    # Test to verify that valid credentials return a token


def test_invalid_password_is_rejected():
    payload = {"username": "admin", "password": "wrong"}

    response = requests.post(f"{BASE_URL}/auth", json=payload)

    body = response.json()
    assert "token" not in body
    assert body["reason"] == "Bad credentials"

    # Test to verify that an invalid password is rejected


@pytest.mark.xfail(
    strict=True,
    reason="BUG: failed login returns 200 instead of 401 Unauthorized",
)
def test_invalid_password_returns_401():
    payload = {"username": "admin", "password": "wrong"}

    response = requests.post(f"{BASE_URL}/auth", json=payload)

    assert response.status_code == 401

    # Test to verify that an invalid password is rejected