import requests

BASE_URL = "https://restful-booker.herokuapp.com"


def test_ping_returns_201():
    response = requests.get(f"{BASE_URL}/ping")
    assert response.status_code == 201
