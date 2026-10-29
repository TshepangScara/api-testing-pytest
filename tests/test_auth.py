import pytest
import requests


def test_valid_credentials_return_token(base_url, credentials):
    payload = credentials

    response = requests.post(f"{base_url}/auth", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "token" in body
    assert body["token"]


def test_invalid_password_is_rejected(base_url, credentials):
    payload = {"username": credentials["username"], "password": "wrong"}

    response = requests.post(f"{base_url}/auth", json=payload)

    body = response.json()
    assert "token" not in body
    assert body["reason"] == "Bad credentials"


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="BUG: failed login returns 200 instead of 401 Unauthorized",
)
def test_invalid_password_returns_401(base_url, credentials):
    payload = {"username": credentials["username"], "password": "wrong"}

    response = requests.post(f"{base_url}/auth", json=payload)

    assert response.status_code == 401