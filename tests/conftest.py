import os

import pytest

#fixture to provide the base URL for the API

@pytest.fixture
def base_url():
    return "https://restful-booker.herokuapp.com"

 #fixture to provide valid credentials for authentication tests

@pytest.fixture
def credentials():
    username = os.environ.get("RB_USERNAME")
    password = os.environ.get("RB_PASSWORD")

    if not username or not password:
        pytest.fail("Set RB_USERNAME and RB_PASSWORD in the terminal before running tests")

    return {"username": username, "password": password}