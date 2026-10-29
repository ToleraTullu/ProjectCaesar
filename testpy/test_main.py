from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    # Verify that the server responds with a 200 OK status code
    assert response.status_code == 200

def test_addition():
    assert 1 + 1 == 2