 
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_token():
    res = client.post("/auth/login", json={"username": "testuser", "password": "testpass123"})
    return res.json()["access_token"]

def test_deposit():
    token = get_auth_token()
    res = client.post("/wallet/", json={
        "type": "deposit",
        "amount": 100,
        "currency": "USD"
    }, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
