from __future__ import annotations

from app.schemas.reviews import CodeFixSuggestion, ReviewSummary


class CodeFixService:
    def generate(self, findings: list[ReviewSummary]) -> list[CodeFixSuggestion]:
        fixes: list[CodeFixSuggestion] = []
        for finding in findings:
            title = finding.title.lower()
            if "dynamic code execution" in title:
                fixes.append(
                    CodeFixSuggestion(
                        file_path=finding.file_path,
                        title="Replace eval/exec with a safe dispatcher",
                        explanation="Use an allowlisted function map or parser instead of runtime code execution.",
                        patch="# Example\n# action = ACTIONS[user_input]\n# action()",
                    )
                )
            elif "missing test coverage" in title:
                fixes.append(
                    CodeFixSuggestion(
                        file_path=finding.file_path,
                        title="Add regression tests for the new behavior",
                        explanation="Create targeted unit tests that cover the new branches and error paths.",
                        patch="def test_new_feature():\n    assert new_feature() == expected",
                    )
                )
            elif finding.suggestion:
                fixes.append(
                    CodeFixSuggestion(
                        file_path=finding.file_path,
                        title=finding.title,
                        explanation=finding.suggestion,
                        patch=None,
                    )
                )
        return fixes
