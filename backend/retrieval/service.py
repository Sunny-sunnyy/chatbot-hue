"""Profile router enforcing component availability for retrieval queries."""
import logging

from core.schema import (
    ComponentNotReadyError,
    InvalidQueryError,
    RetrievedDocument,
    RetrievalConfigurationError,
)
from core.settings_loader import load_settings
from core.startup import build_retrieval_stack

logger = logging.getLogger(__name__)

PROFILE_REQUIREMENTS = {
    "dense_only": ("dense_retriever",),
    "hybrid_no_rerank": ("hybrid_retriever",),
    "hybrid_rerank": ("hybrid_retriever", "reranker"),
}

VALID_PROFILES = frozenset(PROFILE_REQUIREMENTS)


class RetrievalService:
    """Route queries to the active profile; components arrive pre-built.

    The service only touches components the active profile requires, so
    dense_only works when BM25 and the reranker were never initialized.
    RetrievedDocument.score is always the final score of the stage that ran.
    Output documents and metadata are created fresh; component objects are
    never mutated.
    """

    def __init__(self, stack, *, rerank_top_k=5):
        self._stack = stack
        self._profile = stack.snapshot.active_profile
        if self._profile not in VALID_PROFILES:
            raise RetrievalConfigurationError(
                f"unknown active_profile {self._profile!r}"
            )
        for component in PROFILE_REQUIREMENTS[self._profile]:
            if getattr(stack, component) is None:
                raise ComponentNotReadyError(
                    f"profile {self._profile} requires {component} but it is missing"
                )
        self._rerank_top_k = rerank_top_k

    @property
    def snapshot(self):
        """Immutable verified state of the retrieval stack."""
        return self._stack.snapshot

    @property
    def active_profile(self):
        return self._profile

    def search(self, query):
        """Validate the query, run the active profile and return ranked documents."""
        if not isinstance(query, str) or not query.strip():
            raise InvalidQueryError("query must be a non-empty string")
        if self._profile == "dense_only":
            documents = self._stack.dense_retriever.search(query)
        elif self._profile == "hybrid_no_rerank":
            documents = self._stack.hybrid_retriever.search(query)
        else:
            pre_rerank = self._stack.hybrid_retriever.search(query)
            documents = self._stack.reranker.rerank(
                query, pre_rerank, self._rerank_top_k
            )
        ranked = [
            RetrievedDocument(
                id=document.id,
                score=document.score,
                text=document.text,
                metadata={
                    **document.metadata,
                    "retrieval_profile": self._profile,
                    "retrieval_rank": rank,
                },
            )
            for rank, document in enumerate(documents, start=1)
        ]
        logger.info(
            "retrieval profile=%s documents=%d", self._profile, len(ranked)
        )
        return ranked


def build_service(settings=None, **kwargs):
    """Convenience factory: build the profile-scoped stack and route queries."""
    if settings is None:
        try:
            settings = load_settings()
        except Exception as exc:  # invalid or unreadable settings file
            raise RetrievalConfigurationError("settings could not be loaded") from exc
    stack = build_retrieval_stack(settings, **kwargs)
    return RetrievalService(stack, rerank_top_k=settings["reranking"]["top_k"])
