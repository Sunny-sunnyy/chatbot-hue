"""Profile router enforcing component availability for retrieval queries."""
import logging

from core.schema import (
    ComponentNotReadyError,
    InvalidQueryError,
    RetrievedDocument,
    RetrievalConfigurationError,
)

logger = logging.getLogger(__name__)

VALID_PROFILES = frozenset({"dense_only", "hybrid_no_rerank", "hybrid_rerank"})


class RetrievalService:
    """Route queries to the active profile; components arrive pre-built.

    The service only touches components the active profile requires, so
    dense_only works when BM25 and the reranker were never initialized.
    RetrievedDocument.score is always the final score of the stage that ran.
    Output documents and metadata are created fresh; component objects are
    never mutated.
    """

    def __init__(
        self,
        status,
        dense_retriever,
        hybrid_retriever=None,
        reranker=None,
        rerank_top_k=5,
    ):
        self._status = status
        self._dense = dense_retriever
        self._hybrid = hybrid_retriever
        self._reranker = reranker
        self._rerank_top_k = rerank_top_k

    @property
    def status(self):
        """Immutable verified state of the retrieval service."""
        return self._status

    @property
    def active_profile(self):
        return self._status.active_profile

    def search(self, query: str) -> list[RetrievedDocument]:
        """Validate the query, run the active profile and return ranked documents."""
        if not isinstance(query, str) or not query.strip():
            raise InvalidQueryError("query must be a non-empty string")
        profile = self._status.active_profile
        if profile == "dense_only":
            documents = self._dense.search(query)
        elif profile == "hybrid_no_rerank":
            if self._hybrid is None:
                raise ComponentNotReadyError("hybrid_retriever is not configured")
            documents = self._hybrid.search(query)
        elif profile == "hybrid_rerank":
            if self._hybrid is None:
                raise ComponentNotReadyError("hybrid_retriever is not configured")
            if self._reranker is None:
                raise ComponentNotReadyError("reranker is not configured")
            pre_rerank = self._hybrid.search(query)
            documents = self._reranker.rerank(
                query, pre_rerank, self._rerank_top_k
            )
        else:
            raise RetrievalConfigurationError(f"unknown profile: {profile}")
        ranked = [
            RetrievedDocument(
                id=document.id,
                score=document.score,
                text=document.text,
                metadata={
                    **document.metadata,
                    "retrieval_profile": profile,
                    "retrieval_rank": rank,
                },
            )
            for rank, document in enumerate(documents, start=1)
        ]
        logger.info(
            "retrieval profile=%s documents=%d", profile, len(ranked)
        )
        return ranked


def build_service(settings=None, **kwargs):
    """Convenience factory: build the profile-scoped service and route queries."""
    from core.startup import build_retrieval_service

    return build_retrieval_service(settings, **kwargs)
