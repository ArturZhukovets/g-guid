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


def test_create_product(client: TestClient):
    product_data = {
        "title": "Test product",
        "calories": 500.0,
        "proteins": 500.0,
        "fat": 500.0,
        "carbohydrates": 500.0,
        "category_id": 1,
    }
    response = client.post("/products/", json=product_data)
    assert response.json()
    assert response.status_code == 201


def test_update_product(client: TestClient):
    response = client.get('products/')
    response_data = response.json()
    assert response_data['count'] > 0
    product = response_data['items'][0]
    product_id = product['id']

    updated_product_data = product.copy()
    updated_product_data['title'] = "UpdatedProductTitle"
    update_response = client.put(f"products/{product_id}", json=updated_product_data)
    assert update_response.status_code == 200
    assert update_response.json()['title'] == "UpdatedProductTitle"


def test_delete_product(client: TestClient):
    product_id = 1
    response = client.delete(f"products/{product_id}")
    assert response.status_code == 200
