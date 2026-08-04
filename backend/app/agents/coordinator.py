from collections.abc import Iterable

from app.agents.base import ReviewFinding, severity_rank
from app.schemas.reviews import ReviewSummary


class CoordinatorAgent:
    name = "coordinator"

    def consolidate(self, findings: Iterable[ReviewFinding]) -> tuple[str, list[ReviewSummary]]:
        unique: dict[tuple[str | None, str], ReviewFinding] = {}
        for finding in findings:
            key = (finding.file_path, finding.title.lower())
            if key not in unique or severity_rank(finding.severity) < severity_rank(unique[key].severity):
                unique[key] = finding

        ordered = sorted(unique.values(), key=lambda item: (severity_rank(item.severity), item.agent, item.title))
        summaries = [finding.to_summary() for finding in ordered]
        if not summaries:
            return "No blocking issues detected. The change set looks consistent with current standards.", []

        headline = f"{len(summaries)} findings from {len({finding.agent for finding in ordered})} review perspectives."
        return headline, summaries
