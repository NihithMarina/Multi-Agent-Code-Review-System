from __future__ import annotations

from app.agents.base import ReviewFinding
from app.schemas.reviews import ChangedFile


class BaseHeuristicAgent:
    name = "base"

    def _finding(
        self,
        severity: str,
        title: str,
        explanation: str,
        suggestion: str | None = None,
        file_path: str | None = None,
    ) -> ReviewFinding:
        return ReviewFinding(
            agent=self.name,
            severity=severity,
            title=title,
            explanation=explanation,
            suggestion=suggestion,
            file_path=file_path,
        )


class SecurityAgent(BaseHeuristicAgent):
    name = "security"

    def analyze(self, files: list[ChangedFile], standards_context: str | None = None) -> list[ReviewFinding]:
        findings: list[ReviewFinding] = []
        for changed_file in files:
            patch = (changed_file.patch or "").lower()
            if "eval(" in patch or "exec(" in patch:
                findings.append(self._finding("critical", "Dynamic code execution", "The patch introduces dynamic execution primitives that can lead to remote code execution.", "Replace with a constrained parser or a fixed dispatch table.", changed_file.path))
            if "secret" in patch or "password" in patch:
                findings.append(self._finding("high", "Potential secret handling issue", "The patch appears to touch credential-related data and should be reviewed for leakage or logging risks.", "Ensure secrets are never logged or stored in plaintext.", changed_file.path))
        return findings


class PerformanceAgent(BaseHeuristicAgent):
    name = "performance"

    def analyze(self, files: list[ChangedFile], standards_context: str | None = None) -> list[ReviewFinding]:
        findings: list[ReviewFinding] = []
        for changed_file in files:
            patch = changed_file.patch or ""
            if patch.count("for ") >= 2:
                findings.append(self._finding("medium", "Possible nested loop hotspot", "The patch adds repeated iteration that could become expensive on large inputs.", "Measure complexity and cache repeated work where possible.", changed_file.path))
            if "select *" in patch.lower():
                findings.append(self._finding("medium", "Inefficient data access", "The patch suggests broad reads that may return unnecessary columns.", "Select only the fields required by the caller.", changed_file.path))
        return findings


class CleanCodeAgent(BaseHeuristicAgent):
    name = "clean-code"

    def analyze(self, files: list[ChangedFile], standards_context: str | None = None) -> list[ReviewFinding]:
        findings: list[ReviewFinding] = []
        for changed_file in files:
            patch = changed_file.patch or ""
            if "todo" in patch.lower() or "fixme" in patch.lower():
                findings.append(self._finding("low", "Leftover implementation note", "A TODO/FIXME marker remains in the patch and should not ship without an owner.", "Track the follow-up in an issue or resolve it before merge.", changed_file.path))
            if len(patch) > 5000:
                findings.append(self._finding("low", "Large change surface", "This file has a broad patch footprint and may benefit from smaller, reviewable chunks.", "Split into focused commits or extract helper functions.", changed_file.path))
        return findings


class TestingAgent(BaseHeuristicAgent):
    name = "testing"

    def analyze(self, files: list[ChangedFile], standards_context: str | None = None) -> list[ReviewFinding]:
        file_names = {changed_file.path.lower() for changed_file in files}
        source_changes = [changed_file for changed_file in files if not changed_file.path.lower().endswith(("test.py", "spec.ts", "spec.tsx", "test.ts", "test.tsx"))]
        has_test_changes = any(name.endswith(("test.py", "spec.ts", "spec.tsx", "test.ts", "test.tsx")) for name in file_names)
        findings: list[ReviewFinding] = []
        if source_changes and not has_test_changes:
            findings.append(self._finding("high", "Missing test coverage", "The change touches source code but no matching tests were included.", "Add unit or integration tests that cover the new behavior.", source_changes[0].path))
        return findings


class DocumentationAgent(BaseHeuristicAgent):
    name = "documentation"

    def analyze(self, files: list[ChangedFile], standards_context: str | None = None) -> list[ReviewFinding]:
        findings: list[ReviewFinding] = []
        for changed_file in files:
            if changed_file.path.endswith((".py", ".ts", ".tsx", ".js", ".jsx")) and (changed_file.patch or "").count("def ") + (changed_file.patch or "").count("class ") > 0:
                findings.append(self._finding("low", "Docstring or API note may be needed", "Public-facing code changed and should be documented for maintainers.", "Add a concise docstring, README note, or API description if this is externally visible.", changed_file.path))
        return findings


class DependencyAgent(BaseHeuristicAgent):
    name = "dependency"

    def analyze(self, files: list[ChangedFile], standards_context: str | None = None) -> list[ReviewFinding]:
        findings: list[ReviewFinding] = []
        for changed_file in files:
            path = changed_file.path.lower()
            if path.endswith(("requirements.txt", "package.json", "poetry.lock", "pnpm-lock.yaml", "yarn.lock")):
                findings.append(self._finding("medium", "Dependency surface changed", "The change modifies the dependency graph and should be checked for supply-chain or compatibility risk.", "Confirm lockfiles are updated and run the relevant security checks.", changed_file.path))
        return findings


class ArchitectureAgent(BaseHeuristicAgent):
    name = "architecture"

    def analyze(self, files: list[ChangedFile], standards_context: str | None = None) -> list[ReviewFinding]:
        findings: list[ReviewFinding] = []
        for changed_file in files:
            patch = (changed_file.patch or "").lower()
            if "from app.db" in patch and "route" in changed_file.path.lower():
                findings.append(self._finding("high", "Layering violation risk", "The route layer appears to access the database directly, which can erode architectural boundaries.", "Move the persistence logic into a service or repository class.", changed_file.path))
            if "cross-file" in patch or "circular" in patch:
                findings.append(self._finding("medium", "Possible dependency entanglement", "The patch suggests a coupling pattern that could make future refactors harder.", "Keep the domain, service, and transport layers isolated.", changed_file.path))
        return findings
