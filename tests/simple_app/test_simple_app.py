from fastapi.testclient import TestClient

from .app import app


client = TestClient(app)


def test_data_json():
    response = client.get("/static/data.json")
    assert response.status_code == 200
    assert response.json() == {"mylist": [1, 2, 3]}