from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.core.config import get_settings
from app.schemas.webhooks import GitHubPullRequestWebhookPayload
from app.services.review_service import ReviewService

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/github/pull-request")
async def handle_github_pull_request_webhook(
    request: Request,
    payload: GitHubPullRequestWebhookPayload,
    x_github_event: str | None = Header(default=None),
    db: Session = Depends(db_session),
):
    if x_github_event not in {None, "pull_request"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported GitHub event")

    if payload.action not in {"opened", "synchronize", "reopened", "ready_for_review"}:
        return {"status": "ignored", "action": payload.action}

    owner = payload.repository.owner.get("login", payload.repository.full_name.split("/")[0])
    repo_name = payload.repository.name
    service = ReviewService(db, get_settings())
    review = await service.analyze_github_pull_request(owner, repo_name, payload.pull_request.number)
    return {"status": "processed", "review": review}