from __future__ import annotations

from collections.abc import Iterable

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from app.models.review import Review


class ReviewSearchService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        reviews = self.db.query(Review).all()
        if not reviews:
            return []

        documents = [self._serialize(review) for review in reviews]
        embeddings = self.model.encode(documents, normalize_embeddings=True)
        vectors = np.asarray(embeddings, dtype=np.float32)
        index = faiss.IndexFlatIP(vectors.shape[1])
        index.add(vectors)

        query_vector = self.model.encode([query], normalize_embeddings=True)
        scores, indices = index.search(np.asarray(query_vector, dtype=np.float32), top_k)

        results: list[dict] = []
        for score, index_position in zip(scores[0], indices[0], strict=False):
            if index_position < 0:
                continue
            review = reviews[index_position]
            results.append(
                {
                    "review_id": review.id,
                    "repository_id": review.repository_id,
                    "pull_request_number": review.pull_request_number,
                    "summary": review.summary,
                    "score": float(score),
                }
            )
        return results

    def _serialize(self, review: Review) -> str:
        findings = review.findings or []
        finding_text = " ".join(
            f"{finding.get('title', '')} {finding.get('explanation', '')} {finding.get('suggestion', '')}"
            for finding in findings
        )
        return f"review {review.id} pr {review.pull_request_number} {review.summary or ''} {finding_text}"
