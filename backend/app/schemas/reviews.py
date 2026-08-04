from datetime import datetime

from pydantic import BaseModel, Field


class ChangedFile(BaseModel):
    path: str
    patch: str | None = None
    language: str | None = None


class ReviewCreate(BaseModel):
    repository_id: int
    pull_request_number: int
    commit_sha: str
    files: list[ChangedFile] = Field(default_factory=list)
    post_to_github: bool = False


class ReviewSummary(BaseModel):
    agent: str
    severity: str
    title: str
    explanation: str
    suggestion: str | None = None
    file_path: str | None = None


class CodeFixSuggestion(BaseModel):
    file_path: str | None = None
    title: str
    explanation: str
    patch: str | None = None


class ReviewRead(BaseModel):
    id: int
    repository_id: int
    pull_request_number: int
    commit_sha: str
    status: str
    summary: str | None = None
    findings: list[ReviewSummary] | dict | None = None
    fixes: list[CodeFixSuggestion] | dict | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
