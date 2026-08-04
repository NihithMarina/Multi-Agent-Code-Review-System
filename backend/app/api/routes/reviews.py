from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import db_session, require_roles
from app.core.config import get_settings
from app.schemas.reviews import ReviewCreate, ReviewRead
from app.services.review_service import ReviewService

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/analyze", response_model=ReviewRead, dependencies=[Depends(require_roles("admin", "member", "reviewer"))])
def analyze_review(payload: ReviewCreate, db: Session = Depends(db_session)) -> ReviewRead:
    service = ReviewService(db, get_settings())
    return service.analyze_files(payload)


@router.get("/{review_id}", response_model=ReviewRead, dependencies=[Depends(require_roles("admin", "member", "viewer", "reviewer"))])
def get_review(review_id: int, db: Session = Depends(db_session)) -> ReviewRead:
    from app.models.review import Review

    review = db.query(Review).filter(Review.id == review_id).one()
    return ReviewRead.model_validate(review)
