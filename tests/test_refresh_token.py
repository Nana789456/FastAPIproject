def test_login_sets_refresh_cookie(logged_in_client):
    assert logged_in_client.cookies.get("refresh_token")


def test_refresh_returns_new_access_token(logged_in_client):
    old_refresh_token = logged_in_client.cookies.get("refresh_token")

    response = logged_in_client.post("/v1/user/refresh")

    assert response.status_code == 200
    access_token = response.json()["access_token"]
    assert logged_in_client.cookies.get("refresh_token") != old_refresh_token

    me = logged_in_client.get(
        "/v1/user/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert me.status_code == 200
    assert me.json()["login"] == "user1"


def test_old_refresh_token_is_rejected_after_rotation(logged_in_client):
    old_refresh_token = logged_in_client.cookies.get("refresh_token")
    logged_in_client.post("/v1/user/refresh")

    logged_in_client.cookies.clear()
    logged_in_client.cookies.set("refresh_token", old_refresh_token)
    response = logged_in_client.post("/v1/user/refresh")

    assert response.status_code == 401


def test_refresh_after_logout_is_rejected(logged_in_client):
    refresh_token = logged_in_client.cookies.get("refresh_token")

    response = logged_in_client.post("/v1/user/logout")
    assert response.status_code == 204

    logged_in_client.cookies.set("refresh_token", refresh_token)
    response = logged_in_client.post("/v1/user/refresh")

    assert response.status_code == 401


def test_refresh_without_cookie_is_rejected(client):
    response = client.post("/v1/user/refresh")

    assert response.status_code == 401
