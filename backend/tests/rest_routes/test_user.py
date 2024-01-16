def test_create_user(client):
    data = {"name": "testuser@nofoobar.com", "password": "testing"}
    response = client.post("/users", json=data)
    response_json = response.json()
    print("RESPONSE: ")
    print(response_json)
    assert response_json["name"] == "testuser@nofoobar.com"
    assert not response_json["is_superuser"]
    assert response.status_code == 201


def test_user_is_super_user(admin_user):
    assert admin_user.is_superuser


def test_user_change_role(client, admin_user, admin_authorization_token_header):
    data = {"id": admin_user.id, "role": "Coach"}
    response = client.post(
        "/users/change_user_role/", json=data, headers=admin_authorization_token_header
    )
    print(response)
    assert response.status_code == 200
    assert response.json()["role"] == "Coach"
