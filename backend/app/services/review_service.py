from __future__ import annotations

from sqlalchemy.orm import Session

from app.agents.graph import build_review_graph
from app.core.config import Settings
from app.models.organization import Organization
from app.models.repository import Repository
from app.models.review import Review
from app.schemas.reviews import ChangedFile, ReviewCreate, ReviewRead
from app.services.fix_service import CodeFixService
from app.services.github_service import GitHubService
from app.services.rag_service import StandardsRAGService


class ReviewService:
    def __init__(self, db: Session, settings: Settings) -> None:
        self.db = db
        self.settings = settings
        self.graph = build_review_graph()
        self.rag = StandardsRAGService(settings.standards_corpus_path, settings.rag_index_path)
        self.fixes = CodeFixService()
        self.rag.load_corpus()

    def analyze_files(self, request: ReviewCreate) -> ReviewRead:
        standards_context = "\n\n".join(self.rag.search("review coding standards", top_k=3)) or None
        result = self.graph.invoke({"files": request.files, "standards_context": standards_context})
        summary = result.get("summary", "Review completed.")
        findings = [item.model_dump() for item in result.get("findings", [])]
        fixes = [item.model_dump() for item in self.fixes.generate(result.get("findings", []))]

        record = Review(
            repository_id=request.repository_id,
            pull_request_number=request.pull_request_number,
            commit_sha=request.commit_sha,
            status="completed",
            summary=summary,
            findings=findings,
            fixes=fixes,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return ReviewRead.model_validate(record)

    async def analyze_github_pull_request(
        self,
        owner: str,
        repo_name: str,
        pull_request_number: int,
        github_token: str | None = None,
        post_to_github: bool = False,
    ) -> ReviewRead:
        github = GitHubService(token=github_token)
        pr = await github.fetch_pull_request(owner, repo_name, pull_request_number)
        files = await github.fetch_pull_request_files(owner, repo_name, pull_request_number)
        repository = self._get_or_create_repository(owner, repo_name)
        review = self.analyze_files(
            ReviewCreate(
                repository_id=repository.id,
                pull_request_number=pull_request_number,
                commit_sha=pr.get("head", {}).get("sha", "unknown"),
                files=[ChangedFile(path=item.path, patch=item.patch, language=item.language) for item in files],
                post_to_github=post_to_github,
            )
        )
        if post_to_github and review.summary:
            await github.post_review_comment(owner, repo_name, pull_request_number, review.summary)
        return review

    def _get_or_create_repository(self, owner: str, name: str) -> Repository:
        organization = self.db.query(Organization).filter(Organization.slug == "default").one_or_none()
        if organization is None:
            organization = Organization(name="Default Organization", slug="default")
            self.db.add(organization)
            self.db.flush()

        repository = (
            self.db.query(Repository)
            .filter(Repository.github_owner == owner, Repository.github_name == name)
            .one_or_none()
        )
        if repository is not None:
            return repository
        repository = Repository(organization_id=organization.id, github_owner=owner, github_name=name)
        self.db.add(repository)
        self.db.commit()
        self.db.refresh(repository)
        return repository
