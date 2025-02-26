from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_joke():
    response = client.get("/joke")
    assert response.status_code == 200
    assert "setup" in response.json()
    assert "punchline" in response.json()
