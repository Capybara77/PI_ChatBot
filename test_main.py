from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_clear_history():
    response = client.get("/clear")
    assert response.status_code == 200
    assert response.json() == {"message": "Chat history cleared"}


def test_response_model():
    response = client.get("/chat?input_data=Hello")
    assert response.status_code == 200
    assert response.json()
