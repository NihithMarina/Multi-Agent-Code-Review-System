from pydantic import BaseModel


class ReviewSearchQuery(BaseModel):
    query: str
    top_k: int = 5


class ReviewSearchHit(BaseModel):
    review_id: int
    repository_id: int
    pull_request_number: int
    summary: str | None = None
    score: float
