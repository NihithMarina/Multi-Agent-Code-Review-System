from dataclasses import dataclass

import httpx


@dataclass(slots=True)
class PullRequestFile:
    path: str
    patch: str | None = None
    language: str | None = None


class GitHubService:
    def __init__(self, token: str | None = None, api_base: str = "https://api.github.com") -> None:
        self.token = token
        self.api_base = api_base.rstrip("/")

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/vnd.github+json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def fetch_pull_request(self, owner: str, repo: str, number: int) -> dict:
        async with httpx.AsyncClient(base_url=self.api_base, headers=self._headers(), timeout=30.0) as client:
            response = await client.get(f"/repos/{owner}/{repo}/pulls/{number}")
            response.raise_for_status()
            return response.json()

    async def fetch_pull_request_files(self, owner: str, repo: str, number: int) -> list[PullRequestFile]:
        async with httpx.AsyncClient(base_url=self.api_base, headers=self._headers(), timeout=30.0) as client:
            response = await client.get(f"/repos/{owner}/{repo}/pulls/{number}/files")
            response.raise_for_status()
            payload = response.json()
        return [PullRequestFile(path=item["filename"], patch=item.get("patch"), language=item.get("language")) for item in payload]

    async def post_review_comment(self, owner: str, repo: str, number: int, body: str) -> None:
        async with httpx.AsyncClient(base_url=self.api_base, headers=self._headers(), timeout=30.0) as client:
            response = await client.post(
                f"/repos/{owner}/{repo}/issues/{number}/comments",
                json={"body": body},
            )
            response.raise_for_status()
