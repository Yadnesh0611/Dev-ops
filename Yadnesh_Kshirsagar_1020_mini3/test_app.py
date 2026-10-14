import pytest
from app import app, books

@pytest.fixture
def client():
    books.clear()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
    books.clear()

def test_home(client):
    assert client.get("/").status_code == 200

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_add_book(client):
    response = client.post("/books", json={"title": "Python", "author": "Alex"})
    assert response.status_code == 201
    assert response.json["title"] == "Python"

def test_list_books(client):
    client.post("/books", json={"title": "Python", "author": "Alex"})
    assert len(client.get("/books").json) == 1

def test_reject_invalid_book(client):
    assert client.post("/books", json={}).status_code == 400

def test_delete_book(client):
    book = client.post("/books", json={"title": "Python", "author": "Alex"}).json
    assert client.delete(f"/books/{book['id']}").status_code == 204

def test_missing_book(client):
    assert client.delete("/books/999").status_code == 404
