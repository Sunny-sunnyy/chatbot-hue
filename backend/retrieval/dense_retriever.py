"""Dense Qdrant retriever producing deterministic top-k RetrievedDocuments."""
import math

from core.schema import (
    RetrievedDocument,
    RetrievalDependencyError,
)
from vectorstore.qdrant import DENSE_VECTOR_NAME

SAFE_PAYLOAD_FIELDS = (
    "chunk_id",
    "source",
    "title",
    "section",
    "category",
    "subcategory",
    "chunk_type",
)

QUERY_PAYLOAD_FIELDS = list(SAFE_PAYLOAD_FIELDS) + ["text"]


class DenseRetriever:
    """Embed a query and search the dense vector of one collection.

    The result is ordered by raw cosine score descending then chunk_id
    ascending so identical scores never depend on Qdrant's point order.
    Embedder and client failures surface as RetrievalDependencyError; the
    Qdrant query requests only the safe payload fields.
    """

    def __init__(self, client, embedder, collection_name, top_k=10):
        self._client = client
        self._embedder = embedder
        self._collection_name = collection_name
        self._top_k = top_k

    @property
    def top_k(self):
        return self._top_k

    def search(self, query, limit=None):
        """Return up to `limit` (default top_k) documents, best first."""
        try:
            vector = self._embedder.embed_query(query)
        except Exception as exc:  # embedder/model runtime failures
            raise RetrievalDependencyError("query embedding failed") from exc
        depth = self._top_k if limit is None else limit
        try:
            response = self._client.query_points(
                self._collection_name,
                query=vector,
                using=DENSE_VECTOR_NAME,
                limit=depth,
                with_payload=QUERY_PAYLOAD_FIELDS,
                with_vectors=False,
            )
        except Exception as exc:  # client transport/protocol failures
            raise RetrievalDependencyError("Qdrant dense query failed") from exc
        documents = [self._to_document(point) for point in response.points]
        documents.sort(key=lambda doc: (-doc.score, doc.metadata["chunk_id"]))
        return documents

    def _to_document(self, point):
        """Convert one ScoredPoint into a RetrievedDocument with safe metadata."""
        payload = point.payload or {}
        text = payload.get("text")
        chunk_id = payload.get("chunk_id")
        if (
            not isinstance(text, str)
            or not text.strip()
            or not isinstance(chunk_id, str)
            or not chunk_id
        ):
            raise RetrievalDependencyError(
                "retrieved point has invalid text or chunk_id payload"
            )
        try:
            score = float(point.score)
        except (TypeError, ValueError) as exc:
            raise RetrievalDependencyError(
                "retrieved point has a non-numeric score"
            ) from exc
        if not math.isfinite(score):
            raise RetrievalDependencyError("retrieved point has a non-finite score")
        metadata = {
            field: payload[field] for field in SAFE_PAYLOAD_FIELDS if field in payload
        }
        metadata["dense_score"] = score
        metadata["embedding_model"] = self._embedder.model_id
        return RetrievedDocument(id=chunk_id, score=score, text=text, metadata=metadata)
