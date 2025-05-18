 
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login():
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass123"
    }

    res = client.post("/auth/register", json=user_data)
    assert res.status_code in [200, 400]  # Might already exist if rerunning

    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    res = client.post("/auth/login", json=login_data)
    assert res.status_code == 200
    assert "access_token" in res.json()
