from pydantic import BaseModel


class GitHubReviewRequest(BaseModel):
    owner: str
    repository: str
    pull_request_number: int
    github_token: str | None = None
    post_to_github: bool = False
