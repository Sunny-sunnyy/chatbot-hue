"""Local dense embedder backed by sentence-transformers."""
from functools import lru_cache

from embedding.base import BaseEmbedder

DOCUMENT_PREFIX = "passage: "
QUERY_PREFIX = "query: "


def _load_model(model_id, device):
    """Build a SentenceTransformer instance; lazy import keeps tests offline."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_id, device=device)


@lru_cache(maxsize=4)
def _get_model(model_id, device):
    """Return one cached SentenceTransformer instance per (model_id, device)."""
    return _load_model(model_id, device)


class SentenceTransformerEmbedder(BaseEmbedder):
    """Local baseline embedder with E5 query/document prefixes.

    The model loads lazily, only when a non-empty input is embedded, and is
    cached once per process.
    """

    def __init__(
        self,
        model_id,
        dimension,
        device="cpu",
        batch_size=64,
        document_prefix=DOCUMENT_PREFIX,
        query_prefix=QUERY_PREFIX,
    ):
        self._model_id = model_id
        self._dimension = dimension
        self._device = device
        self._batch_size = batch_size
        self._document_prefix = document_prefix
        self._query_prefix = query_prefix

    @property
    def model_id(self):
        return self._model_id

    @property
    def dimension(self):
        return self._dimension

    def embed_documents(self, texts):
        """Embed texts with the document prefix; empty input loads no model."""
        if not texts:
            return []
        model = _get_model(self._model_id, self._device)
        prefixed = [f"{self._document_prefix}{text}" for text in texts]
        raw = model.encode(prefixed, batch_size=self._batch_size)
        return self._process_vectors(raw)

    def embed_query(self, query):
        """Embed a single query with the query prefix."""
        self._validate_query(query)
        model = _get_model(self._model_id, self._device)
        raw = model.encode([f"{self._query_prefix}{query}"], batch_size=self._batch_size)
        return self._process_vectors(raw)[0]
