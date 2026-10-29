import requests


def test_ping_returns_201(base_url):
    response = requests.get(f"{base_url}/ping")

    assert response.status_code == 201
#Health check test to verify the API is up and running