from __future__ import annotations

from typing import Annotated, TypedDict

from langgraph.graph import END, StateGraph

from app.agents.coordinator import CoordinatorAgent
from app.agents.specialized import (
    ArchitectureAgent,
    CleanCodeAgent,
    DependencyAgent,
    DocumentationAgent,
    PerformanceAgent,
    SecurityAgent,
    TestingAgent,
)
from app.schemas.reviews import ChangedFile, ReviewSummary


class ReviewGraphState(TypedDict, total=False):
    files: list[ChangedFile]
    standards_context: str | None
    findings: list[ReviewSummary]
    summary: str


def _agent_node(agent):
    def run(state: ReviewGraphState) -> ReviewGraphState:
        current = state.get("findings", [])
        results = agent.analyze(state.get("files", []), state.get("standards_context"))
        return {"findings": current + [finding.to_summary() for finding in results]}

    return run


def build_review_graph():
    graph = StateGraph(ReviewGraphState)
    graph.add_node("security", _agent_node(SecurityAgent()))
    graph.add_node("performance", _agent_node(PerformanceAgent()))
    graph.add_node("clean_code", _agent_node(CleanCodeAgent()))
    graph.add_node("testing", _agent_node(TestingAgent()))
    graph.add_node("documentation", _agent_node(DocumentationAgent()))
    graph.add_node("dependency", _agent_node(DependencyAgent()))
    graph.add_node("architecture", _agent_node(ArchitectureAgent()))

    coordinator = CoordinatorAgent()

    def finalize(state: ReviewGraphState) -> ReviewGraphState:
        from app.agents.base import ReviewFinding

        findings = [
            ReviewFinding(
                agent=item.agent,
                severity=item.severity,
                title=item.title,
                explanation=item.explanation,
                suggestion=item.suggestion,
                file_path=item.file_path,
            )
            for item in state.get("findings", [])
        ]
        summary, consolidated = coordinator.consolidate(findings)
        return {"summary": summary, "findings": consolidated}

    graph.add_node("coordinator", finalize)
    graph.set_entry_point("security")
    graph.add_edge("security", "performance")
    graph.add_edge("performance", "clean_code")
    graph.add_edge("clean_code", "testing")
    graph.add_edge("testing", "documentation")
    graph.add_edge("documentation", "dependency")
    graph.add_edge("dependency", "architecture")
    graph.add_edge("architecture", "coordinator")
    graph.add_edge("coordinator", END)
    return graph.compile()
