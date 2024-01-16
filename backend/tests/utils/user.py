from fastapi.testclient import TestClient


def auth_token_by_user_credentials(
    client: TestClient, username: str, password: str
) -> str:
    """
    Return a valid token for the user with given username.
    If the user does not exist - it is created first.
    """
    json_data = {"username": username, "password": password}
    response = client.post("/auth/token", data=json_data)
    return response.json()["access_token"]
