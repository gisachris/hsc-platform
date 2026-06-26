import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_api_registration_success(client: AsyncClient):
    payload = {
        "email": "api_register@example.com",
        "password": "ComplexPassword123!",
        "first_name": "API",
        "last_name": "User"
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "api_register@example.com"


@pytest.mark.asyncio
async def test_api_login_success(client: AsyncClient, test_user):
    payload = {
        "email": "test_auth@example.com",
        "password": "ComplexP@ss123!"
    }
    response = await client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]


@pytest.mark.asyncio
async def test_api_get_me_unauthorized(client: AsyncClient):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401
