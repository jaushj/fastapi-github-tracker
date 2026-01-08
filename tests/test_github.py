import pytest
from unittest.mock import patch

@pytest.mark.asyncio
@patch("app.services.github.httpx.AsyncClient.get")
async def test_fetch_repo_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "description": "FastAPI framework",
        "stargazers_count": 100,
        "forks_count": 50,
        "html_url": "https://github.com/tiangolo/fastapi",
    }

    from app.services.github import fetch_repo
    data = await fetch_repo("tiangolo", "fastapi")
    assert data["stars"] == 100
