"""Hybrid dense + BM25 retriever with min-max normalization and fusion."""
from core.schema import RetrievedDocument
from scoring.bm25 import min_max_normalize, validate_weights


class HybridRetriever:
    """Fuse dense and BM25 scores over a fixed candidate set deterministically.

    Dense and BM25 signals are min-max normalized independently over the same
    candidates; a constant signal normalizes to 0.0 and does not affect the
    ranking. The final order is fused score descending then chunk_id ascending.
    Result objects and metadata are created fresh: the dense candidates passed
    in are never mutated.
    """

    def __init__(
        self,
        dense_retriever,
        bm25,
        candidate_depth=30,
        top_k=10,
        dense_weight=0.6,
        bm25_weight=0.4,
    ):
        self._dense = dense_retriever
        self._bm25 = bm25
        self._candidate_depth = candidate_depth
        self._top_k = top_k
        self._dense_weight, self._bm25_weight = validate_weights(
            dense_weight, bm25_weight
        )

    @property
    def top_k(self):
        return self._top_k

    @property
    def candidate_depth(self):
        return self._candidate_depth

    def search(self, query, limit=None):
        """Return the top fused documents from dense candidates + BM25."""
        candidates = self._dense.search(query, limit=self._candidate_depth)
        if not candidates:
            return []
        dense_scores = [doc.metadata["dense_score"] for doc in candidates]
        bm25_scores = [self._bm25.score(query, doc.text) for doc in candidates]
        normalized_dense = min_max_normalize(dense_scores)
        normalized_bm25 = min_max_normalize(bm25_scores)
        fused = []
        for doc, bm25_score, norm_dense, norm_bm25 in zip(
            candidates, bm25_scores, normalized_dense, normalized_bm25
        ):
            hybrid_score = (
                self._dense_weight * norm_dense + self._bm25_weight * norm_bm25
            )
            fused.append(
                RetrievedDocument(
                    id=doc.id,
                    score=hybrid_score,
                    text=doc.text,
                    metadata={
                        **doc.metadata,
                        "bm25_score": bm25_score,
                        "normalized_dense_score": norm_dense,
                        "normalized_bm25_score": norm_bm25,
                        "hybrid_score": hybrid_score,
                    },
                )
            )
        fused.sort(key=lambda doc: (-doc.score, doc.metadata["chunk_id"]))
        depth = self._top_k if limit is None else limit
        return fused[:depth]
