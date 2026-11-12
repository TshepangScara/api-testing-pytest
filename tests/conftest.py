from dotenv import load_dotenv
load_dotenv()

import os

import pytest
import requests

#fixture to provide the base URL for the API

@pytest.fixture(scope="session")
def base_url():
    return "https://restful-booker.herokuapp.com"

 #fixture to provide valid credentials for authentication tests

@pytest.fixture(scope="session")
def credentials():
    username = os.environ.get("RB_USERNAME")
    password = os.environ.get("RB_PASSWORD")

    if not username or not password:
        pytest.fail("Set RB_USERNAME and RB_PASSWORD in the terminal before running tests")

    return {"username": username, "password": password}

@pytest.fixture(scope="session")
def token(base_url, credentials):
    print("\n[LOGIN] calling /auth for a token")
    response = requests.post(f"{base_url}/auth", json=credentials)
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()["token"]
