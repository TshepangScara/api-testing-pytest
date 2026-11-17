import requests


def test_create_booking_returns_booking_id(base_url):
    headers = {"Accept": "application/json"}
    payload = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-01-01",
            "checkout": "2023-01-10"
        },
        "additionalneeds": "Breakfast"
    }

    response = requests.post(f"{base_url}/booking", json=payload, headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert "bookingid" in body
    assert isinstance(body["bookingid"], int)
    assert body["booking"]["firstname"] == payload["firstname"]