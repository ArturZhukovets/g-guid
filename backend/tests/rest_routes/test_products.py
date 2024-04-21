from fastapi.testclient import TestClient


def test_create_category(client: TestClient):
    category_data = {
        "title": "TestCategory"
    }
    response = client.post(
        url="/products/category",
        json=category_data
    )
    assert response.json()
    assert response.status_code == 200


def test_category_list(client: TestClient):
    page = 1
    per_page = 50
    order = "desc"
    response = client.get(f"/products/category?page={page}&per_page={per_page}&order={order}")
    assert response.status_code == 200


