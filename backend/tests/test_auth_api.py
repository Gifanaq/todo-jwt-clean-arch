from fastapi.testclient import TestClient


def register_user(client: TestClient, login: str = "alice") -> dict[str, str]:
    response = client.post(
        "/auth/register",
        json={"login": login, "password": "correct horse battery"},
    )
    assert response.status_code == 201
    return response.json()


def test_register_me_and_login_are_case_insensitive(client: TestClient) -> None:
    registered = register_user(client, "Alice")
    assert "refresh_token" not in registered
    assert client.cookies.get("refresh_token") is not None

    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {registered['access_token']}"},
    )
    assert me_response.status_code == 200
    assert me_response.json() == {
        "user_id": registered["user_id"],
        "login": "alice",
    }

    duplicate_response = client.post(
        "/auth/register",
        json={"login": "ALICE", "password": "another password"},
    )
    assert duplicate_response.status_code == 409

    login_response = client.post(
        "/auth/login",
        json={"login": "ALICE", "password": "correct horse battery"},
    )
    assert login_response.status_code == 200
    assert login_response.json()["user_id"] == registered["user_id"]


def test_refresh_rotates_token_and_logout_revokes_it(client: TestClient) -> None:
    register_user(client)
    original_refresh_token = client.cookies.get("refresh_token")
    assert original_refresh_token is not None

    refreshed = client.post("/auth/refresh")
    assert refreshed.status_code == 200
    rotated_refresh_token = client.cookies.get("refresh_token")
    assert rotated_refresh_token is not None
    assert rotated_refresh_token != original_refresh_token

    client.cookies.set("refresh_token", original_refresh_token, path="/auth")
    assert client.post("/auth/refresh").status_code == 401

    client.cookies.set("refresh_token", rotated_refresh_token, path="/auth")
    logout_response = client.post("/auth/logout")
    assert logout_response.status_code == 204
    assert "refresh_token=" in logout_response.headers["set-cookie"]
    client.cookies.set("refresh_token", rotated_refresh_token, path="/auth")
    assert client.post("/auth/refresh").status_code == 401


def test_todos_are_private_and_wrong_token_types_are_rejected(
    client: TestClient,
) -> None:
    first_user = register_user(client)
    first_headers = {"Authorization": f"Bearer {first_user['access_token']}"}
    todo_response = client.post(
        "/todos",
        headers=first_headers,
        json={"title": "  private task  "},
    )
    assert todo_response.status_code == 201
    todo = todo_response.json()
    assert todo["title"] == "private task"
    update_response = client.patch(
        f"/todos/{todo['id']}",
        headers=first_headers,
        json={"is_done": True},
    )
    assert update_response.status_code == 200
    assert update_response.json()["is_done"] is True

    refresh_token = client.cookies.get("refresh_token")
    assert refresh_token is not None
    wrong_type_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )
    assert wrong_type_response.status_code == 401

    second_user = register_user(client, "bob")
    second_headers = {"Authorization": f"Bearer {second_user['access_token']}"}
    assert client.get("/todos", headers=second_headers).json() == []
    assert (
        client.patch(
            f"/todos/{todo['id']}",
            headers=second_headers,
            json={"is_done": True},
        ).status_code
        == 404
    )
    assert (
        client.delete(f"/todos/{todo['id']}", headers=second_headers).status_code == 404
    )

    owner_todos = client.get("/todos", headers=first_headers).json()
    assert owner_todos[0]["id"] == todo["id"]
    assert owner_todos[0]["is_done"] is True
    assert (
        client.delete(f"/todos/{todo['id']}", headers=first_headers).status_code == 204
    )
    assert client.get("/todos", headers=first_headers).json() == []
