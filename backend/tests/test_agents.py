from app.agents.coordinator import CoordinatorAgent
from app.agents.specialized import SecurityAgent, TestingAgent
from app.schemas.reviews import ChangedFile


def test_security_agent_detects_dynamic_execution() -> None:
    agent = SecurityAgent()
    findings = agent.analyze([ChangedFile(path="app/service.py", patch="result = eval(user_input)")])
    assert any(f.title == "Dynamic code execution" for f in findings)


def test_testing_agent_flags_missing_tests() -> None:
    agent = TestingAgent()
    findings = agent.analyze([ChangedFile(path="app/service.py", patch="def new_feature():\n    return 1")])
    assert any(f.title == "Missing test coverage" for f in findings)


def test_coordinator_sorts_and_deduplicates() -> None:
    coordinator = CoordinatorAgent()
    security_agent = SecurityAgent()
    findings = security_agent.analyze([ChangedFile(path="app/service.py", patch="result = eval(user_input)")])
    summary, consolidated = coordinator.consolidate([findings[0], findings[0]])
    assert summary.startswith("1 findings")
    assert len(consolidated) == 1
