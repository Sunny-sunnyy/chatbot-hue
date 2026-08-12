"""Scorer-backed reranker implementing the shared rerank invariants."""
import math

from core.schema import (
    RetrievedDocument,
    RetrievalDependencyError,
)
from reranking.base import BaseReranker


def _to_finite_scores(scores, documents):
    """Convert and validate every reranker score into a finite numeric value.

    Non-numeric, malformed, nan/inf values and count mismatches all surface as
    RetrievalDependencyError; the message never contains the query or raw
    exception detail.
    """
    if len(scores) != len(documents):
        raise RetrievalDependencyError(
            f"reranker returned {len(scores)} scores for {len(documents)} documents"
        )
    converted = []
    for score in scores:
        try:
            numeric = float(score)
        except (TypeError, ValueError) as exc:
            raise RetrievalDependencyError(
                "reranker returned a non-numeric score"
            ) from exc
        if not math.isfinite(numeric):
            raise RetrievalDependencyError("reranker returned a non-finite score")
        converted.append(numeric)
    return converted


class ScorerReranker(BaseReranker):
    """Rerank via an injected scorer: scorer(query, documents) -> list[float].

    Input chunk_ids must be unique: duplicate input is rejected before the
    scorer runs, so the output can never contain a duplicated or foreign
    document. Output documents and metadata are created fresh; input objects
    are never mutated. Ties are deterministic: score descending, then
    chunk_id ascending.
    """

    def __init__(self, scorer, model_id):
        self._scorer = scorer
        self._model_id = model_id

    @property
    def model_id(self):
        return self._model_id

    def rerank(self, query, documents, top_k):
        if not documents:
            return []
        if top_k <= 0:
            raise ValueError("top_k must be positive")
        seen = set()
        for document in documents:
            chunk_id = document.metadata.get("chunk_id")
            if not isinstance(chunk_id, str) or not chunk_id:
                raise RetrievalDependencyError(
                    "reranker input document has an invalid chunk_id"
                )
            if chunk_id in seen:
                raise RetrievalDependencyError(
                    "reranker input contains duplicate chunk_id"
                )
            seen.add(chunk_id)
        try:
            scores = list(self._scorer(query, documents))
        except Exception as exc:  # scorer/model runtime failures
            raise RetrievalDependencyError("reranker scoring failed") from exc
        scores = _to_finite_scores(scores, documents)
        ranked = sorted(
            zip(scores, documents),
            key=lambda item: (-item[0], item[1].metadata["chunk_id"]),
        )
        return [
            RetrievedDocument(
                id=document.id,
                score=score,
                text=document.text,
                metadata={
                    **document.metadata,
                    "reranker_model": self._model_id,
                    "rerank_score": score,
                },
            )
            for score, document in ranked[:top_k]
        ]
