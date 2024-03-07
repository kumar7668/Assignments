from fastapi.testclient import TestClient
from main import app  # for app instance from main

client = TestClient(app)


def test_add_review():
    # Test adding a review
    response = client.post(
        "/books/1/reviews/",
        json={"text": "Great book!", "rating": 5}
    )
    assert response.status_code == 200
    assert response.json().get("book_id") == 1
    assert response.json().get("text") == "Great book!"
    assert response.json().get("rating") == 5
