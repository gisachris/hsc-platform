import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_auth_placeholder(client: AsyncClient):
    # Future milestones will implement full authorization and registry flows
    response = await client.post("/api/v1/auth/login")
    assert response.status_code == 422
    assert response.json()["success"] is False
