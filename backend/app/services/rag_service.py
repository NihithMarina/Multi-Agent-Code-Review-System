from __future__ import annotations

from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class StandardsRAGService:
    def __init__(self, corpus_path: str, index_path: str) -> None:
        self.corpus_path = Path(corpus_path)
        self.index_path = Path(index_path)
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.documents: list[str] = []
        self.index: faiss.Index | None = None

    def load_corpus(self) -> None:
        self.documents = [path.read_text(encoding="utf-8") for path in sorted(self.corpus_path.glob("**/*")) if path.is_file()]
        if not self.documents:
            self.index = None
            return
        embeddings = self.model.encode(self.documents, normalize_embeddings=True)
        vectors = np.asarray(embeddings, dtype=np.float32)
        self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(vectors)

    def search(self, query: str, top_k: int = 4) -> list[str]:
        if self.index is None or not self.documents:
            return []
        embedding = self.model.encode([query], normalize_embeddings=True)
        scores, indices = self.index.search(np.asarray(embedding, dtype=np.float32), top_k)
        matches: list[str] = []
        for index in indices[0]:
            if index >= 0 and index < len(self.documents):
                matches.append(self.documents[index])
        return matches
