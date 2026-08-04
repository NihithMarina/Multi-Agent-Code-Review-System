from pydantic import BaseModel


class GitHubWebhookRepository(BaseModel):
    full_name: str
    owner: dict[str, str]
    name: str


class GitHubWebhookPullRequest(BaseModel):
    number: int
    head: dict[str, str | dict]


class GitHubPullRequestWebhookPayload(BaseModel):
    action: str
    repository: GitHubWebhookRepository
    pull_request: GitHubWebhookPullRequest
