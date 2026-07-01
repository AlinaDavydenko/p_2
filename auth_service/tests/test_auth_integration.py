import pytest

pytestmark = pytest.mark.asyncio


EMAIL = "petrov@email.com"
PASSWORD = "strongpassword123"


async def test_register_login_me_flow(client):
    # Register
    register_resp = await client.post("/auth/register", json={"email": EMAIL, "password": PASSWORD})
    assert register_resp.status_code == 201
    body = register_resp.json()
    assert body["email"] == EMAIL
    assert "password_hash" not in body

    # Login
    login_resp = await client.post(
        "/auth/login",
        data={"username": EMAIL, "password": PASSWORD},
    )
    assert login_resp.status_code == 200
    token_body = login_resp.json()
    assert token_body["token_type"] == "bearer"
    token = token_body["access_token"]
    assert token

    # Me
    me_resp = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    me_body = me_resp.json()
    assert me_body["email"] == EMAIL
    assert me_body["role"] == "user"


async def test_register_duplicate_email_returns_409(client):
    await client.post("/auth/register", json={"email": EMAIL, "password": PASSWORD})
    resp = await client.post("/auth/register", json={"email": EMAIL, "password": PASSWORD})

    assert resp.status_code == 409


async def test_login_wrong_password_returns_401(client):
    await client.post("/auth/register", json={"email": EMAIL, "password": PASSWORD})
    resp = await client.post("/auth/login", data={"username": EMAIL, "password": "wrong-password"})

    assert resp.status_code == 401


async def test_me_without_token_returns_401(client):
    resp = await client.get("/auth/me")
    assert resp.status_code == 401


async def test_me_with_invalid_token_returns_401(client):
    resp = await client.get("/auth/me", headers={"Authorization": "Bearer garbage-token"})
    assert resp.status_code == 401
