from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    total_reviews: int
    open_reviews: int
    findings_by_severity: dict[str, int]
