from dataclasses import dataclass
from dataclasses import asdict
from typing import Protocol

from app.schemas.reviews import ChangedFile, ReviewSummary


@dataclass(slots=True)
class ReviewFinding:
    agent: str
    severity: str
    title: str
    explanation: str
    suggestion: str | None = None
    file_path: str | None = None

    def to_summary(self) -> ReviewSummary:
        return ReviewSummary.model_validate(asdict(self))


class ReviewAgent(Protocol):
    name: str

    def analyze(self, files: list[ChangedFile], standards_context: str | None = None) -> list[ReviewFinding]:
        ...


def severity_rank(severity: str) -> int:
    ordering = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    return ordering.get(severity.lower(), 4)
