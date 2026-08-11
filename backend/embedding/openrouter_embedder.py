"""Live-ready OpenRouter dense embedder adapter.

Never activated by default; only instantiated explicitly for approved
benchmark runs. A failed request raises and never falls back to a local
model, because mixing vector spaces in one collection is not allowed.
"""
import os
import time

from embedding.base import BaseEmbedder, EmbeddingError
from embedding.batch_embed import batches

EMBEDDINGS_URL = "https://openrouter.ai/api/v1/embeddings"
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
MAX_BACKOFF_SECONDS = 8.0


class OpenRouterEmbedder(BaseEmbedder):
    """Remote embedder posting bounded batches to the embeddings endpoint."""

    def __init__(
        self,
        model_id,
        dimension,
        *,
        api_key=None,
        session=None,
        batch_size=64,
        timeout=30,
        max_retries=2,
        input_type_document="search_document",
        input_type_query="search_query",
        sleep=time.sleep,
    ):
        if batch_size <= 0:
            raise EmbeddingError(f"batch_size must be positive, got {batch_size}")
        if timeout <= 0:
            raise EmbeddingError(f"timeout must be positive, got {timeout}")
        if max_retries < 0:
            raise EmbeddingError(f"max_retries must be >= 0, got {max_retries}")
        self._model_id = model_id
        self._dimension = dimension
        self._api_key = api_key
        self._session = session
        self._batch_size = batch_size
        self._timeout = timeout
        self._max_retries = max_retries
        self._input_type_document = input_type_document
        self._input_type_query = input_type_query
        self._sleep = sleep

    @property
    def model_id(self):
        return self._model_id

    @property
    def dimension(self):
        return self._dimension

    def embed_documents(self, texts):
        """Embed texts in bounded batches with the document input type."""
        if not texts:
            return []
        vectors = []
        for batch in batches(texts, self._batch_size):
            vectors.extend(self._request_embeddings(batch, self._input_type_document))
        return vectors

    def embed_query(self, query):
        """Embed a single query with the query input type."""
        self._validate_query(query)
        return self._request_embeddings([query], self._input_type_query)[0]

    def _request_embeddings(self, texts, input_type):
        session = self._session or self._default_session()
        payload = {"model": self._model_id, "input": texts, "input_type": input_type}
        headers = {"Authorization": f"Bearer {self._api_key_value()}"}
        last_status = None
        for attempt in range(self._max_retries + 1):
            response = session.post(
                EMBEDDINGS_URL, json=payload, headers=headers, timeout=self._timeout
            )
            if response.status_code in RETRYABLE_STATUS:
                last_status = response.status_code
                if attempt < self._max_retries:
                    self._sleep(self._backoff_delay(response, attempt))
                continue
            if response.status_code != 200:
                raise EmbeddingError(
                    f"OpenRouter embedding request failed with HTTP "
                    f"{response.status_code}"
                )
            raw = self._ordered_embeddings(response.json(), len(texts))
            return self._process_vectors(raw)
        raise EmbeddingError(
            f"OpenRouter embedding request failed after retries "
            f"(last HTTP {last_status})"
        )

    def _ordered_embeddings(self, payload, expected_count):
        """Return embeddings reordered by index, rejecting a bad index set.

        Indexes must be an exact permutation of 0..expected_count-1;
        duplicates, missing or out-of-range indexes are rejected so vectors
        never get paired with the wrong input text.
        """
        data = payload["data"]
        indexes = [item["index"] for item in data]
        expected = set(range(expected_count))
        if len(indexes) != expected_count or set(indexes) != expected:
            raise EmbeddingError(
                f"mismatched embedding count: OpenRouter returned {len(data)} "
                f"embeddings with indexes {sorted(indexes)} for "
                f"{expected_count} inputs"
            )
        return [
            item["embedding"]
            for item in sorted(data, key=lambda item: item["index"])
        ]

    def _backoff_delay(self, response, attempt):
        """Return seconds to wait before the next retry.

        Prefer the provider's Retry-After header when valid, otherwise fall
        back to capped exponential backoff.
        """
        retry_after = getattr(response, "headers", {}).get("Retry-After")
        if retry_after is not None:
            try:
                seconds = float(retry_after)
                if seconds > 0:
                    return min(seconds, MAX_BACKOFF_SECONDS)
            except (TypeError, ValueError):
                pass
        return min(2.0 ** attempt, MAX_BACKOFF_SECONDS)

    def _api_key_value(self):
        """Return the API key from constructor or environment; never logged."""
        key = self._api_key or os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise EmbeddingError("OPENROUTER_API_KEY is not set in the environment")
        return key

    def _default_session(self):
        import requests

        return requests.Session()
