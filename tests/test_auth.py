import os

import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"
USERNAME = os.environ["RB_USERNAME"]
PASSWORD = os.environ["RB_PASSWORD"]


def test_valid_credentials_return_token():
    payload = {"username": USERNAME, "password": PASSWORD}

    response = requests.post(f"{BASE_URL}/auth", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "token" in body
    assert body["token"]


def test_invalid_password_is_rejected():
    payload = {"username": USERNAME, "password": "wrong"}

    response = requests.post(f"{BASE_URL}/auth", json=payload)

    body = response.json()
    assert "token" not in body
    assert body["reason"] == "Bad credentials"


@pytest.mark.xfail(
    strict=True,
    reason="BUG: failed login returns 200 instead of 401 Unauthorized",
)

def test_invalid_password_returns_401():
    payload = {"username": USERNAME, "password": "wrong"}

    response = requests.post(f"{BASE_URL}/auth", json=payload)

    assert response.status_code == 401

    # This test is expected to fail because the API currently returns a 200 status code for failed login attempts instead of the expected 401 Unauthorized status code.