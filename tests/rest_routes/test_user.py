

def test_create_user(client):
    data = {"name": "testuser@nofoobar.com", "password": "testing"}
    response = client.post("/users", json=data)
    response_json = response.json()
    assert response_json["name"] == "testuser@nofoobar.com"
    assert not response_json["is_superuser"]
    assert response.status_code == 201


def test_user_is_super_user(admin_user):
    assert admin_user.is_superuser


