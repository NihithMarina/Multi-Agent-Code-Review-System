from __future__ import annotations

from collections import Counter

from sqlalchemy.orm import Session

from app.models.review import Review


class AnalyticsService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def overview(self) -> dict:
        reviews = self.db.query(Review).all()
        severity_counter: Counter[str] = Counter()
        for review in reviews:
            for finding in review.findings or []:
                severity_counter[str(finding.get("severity", "info")).lower()] += 1
        return {
            "total_reviews": len(reviews),
            "open_reviews": sum(1 for review in reviews if review.status != "completed"),
            "findings_by_severity": dict(severity_counter),
        }
