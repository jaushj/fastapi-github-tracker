import httpx
from app.core.config import GITHUB_API_BASE

class GitHubServiceError(Exception):
    pass

async def fetch_repo(owner: str, name: str) -> dict:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{name}"

    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(url)

    if response.status_code == 404:
        raise GitHubServiceError("Repository not found")

    response.raise_for_status()
    data = response.json()

    return {
        "owner": owner,
        "name": name,
        "description": data.get("description"),
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "url": data["html_url"],
    }
