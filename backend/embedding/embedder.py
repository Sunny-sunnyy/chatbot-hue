"""Local dense embedding with multilingual E5."""

DOCUMENT_PREFIX = "passage: "
QUERY_PREFIX = "query: "


class E5Embedder:
    """Embed documents and queries with one lazily loaded local E5 model."""

    def __init__(self, model_id, dimension, device="cpu", batch_size=64):
        self.model_id = model_id
        self.dimension = dimension
        self.device = device
        self.batch_size = batch_size
        self._model = None

    def _get_model(self):
        """Load the configured model once for this embedder instance."""
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer(self.model_id, device=self.device)
            actual_dimension = model.get_sentence_embedding_dimension()
            if actual_dimension != self.dimension:
                raise ValueError(
                    f"model dimension {actual_dimension} != configured "
                    f"{self.dimension}"
                )
            self._model = model
        return self._model

    def _encode(self, texts):
        model = self._get_model()
        vectors = model.encode(
            texts,
            batch_size=self.batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).tolist()
        if len(vectors) != len(texts):
            raise ValueError(
                f"model returned {len(vectors)} vectors for {len(texts)} texts"
            )
        for vector in vectors:
            if len(vector) != self.dimension:
                raise ValueError(
                    f"vector dimension {len(vector)} != configured {self.dimension}"
                )
        return vectors

    def embed_documents(self, texts):
        """Return normalized passage vectors in the same order as texts."""
        if not texts:
            return []
        return self._encode([f"{DOCUMENT_PREFIX}{text}" for text in texts])

    def embed_query(self, query):
        """Return one normalized query vector."""
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        return self._encode([f"{QUERY_PREFIX}{query}"])[0]
