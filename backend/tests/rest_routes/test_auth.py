from fastapi.security import OAuth2PasswordRequestForm


def test_authorize(client, user):
    json_data = {"username": user.name, "password": "password"}
    response = client.post(
        "/auth/token",
        data=json_data,
    )
    assert response.status_code == 200
