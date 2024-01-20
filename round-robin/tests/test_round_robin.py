from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_post():
    response = client.post("/", json={"game": "name"})
    assert response.status_code == 200
    assert response.json() == {"game": "name"}
