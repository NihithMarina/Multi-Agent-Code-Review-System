from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import db_session, require_roles
from app.schemas.search import ReviewSearchHit
from app.services.search_service import ReviewSearchService

router = APIRouter(prefix="/reviews", tags=["reviews-search"])


@router.get("/search", response_model=list[ReviewSearchHit], dependencies=[Depends(require_roles("admin", "member", "reviewer", "viewer"))])
def search_reviews(q: str = Query(..., min_length=2), top_k: int = Query(default=5, ge=1, le=20), db: Session = Depends(db_session)) -> list[ReviewSearchHit]:
    service = ReviewSearchService(db)
    return [ReviewSearchHit.model_validate(item) for item in service.search(q, top_k=top_k)]
