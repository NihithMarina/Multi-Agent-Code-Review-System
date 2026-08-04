from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import db_session, require_roles
from app.schemas.analytics import AnalyticsOverview
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", response_model=AnalyticsOverview, dependencies=[Depends(require_roles("admin", "member", "reviewer"))])
def overview(db: Session = Depends(db_session)) -> AnalyticsOverview:
    service = AnalyticsService(db)
    return AnalyticsOverview.model_validate(service.overview())
