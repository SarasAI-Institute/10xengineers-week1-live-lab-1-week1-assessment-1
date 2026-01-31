import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.storage import books, members, loans

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear():
    books.clear()
    members.clear()
    loans.clear()

def test_add_book():
    r = client.post("/books", json={
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "1234567890"
    })
    assert r.status_code == 200

def test_list_books():
    r = client.get("/books")
    assert r.status_code == 200

