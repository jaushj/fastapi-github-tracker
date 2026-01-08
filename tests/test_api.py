import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_repository():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/repositories",
            json={"owner": "tiangolo", "name": "fastapi"},
        )
    assert response.status_code in (201, 409)
