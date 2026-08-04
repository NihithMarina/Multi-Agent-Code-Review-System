from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import db_session, require_roles
from app.core.config import get_settings
from app.schemas.github import GitHubReviewRequest
from app.schemas.reviews import ReviewRead
from app.services.review_service import ReviewService

router = APIRouter(prefix="/github", tags=["github"])


@router.post("/pull-requests/analyze", response_model=ReviewRead, dependencies=[Depends(require_roles("admin", "member", "reviewer"))])
async def analyze_github_pull_request(payload: GitHubReviewRequest, db: Session = Depends(db_session)) -> ReviewRead:
    service = ReviewService(db, get_settings())
    return await service.analyze_github_pull_request(
        owner=payload.owner,
        repo_name=payload.repository,
        pull_request_number=payload.pull_request_number,
        github_token=payload.github_token,
        post_to_github=payload.post_to_github,
    )
