"""Local MiniLM CrossEncoder reranker baseline on CPU, cache-only."""
from functools import lru_cache

from core.schema import ComponentNotReadyError
from reranking.reranker import ScorerReranker


@lru_cache(maxsize=4)
def _get_cross_encoder(model_id, device):
    """Return one cached CrossEncoder instance per (model_id, device) pair.

    local_files_only=True makes downloads impossible: a missing cache raises
    instead of fetching weights.
    """
    from sentence_transformers import CrossEncoder

    return CrossEncoder(model_id, device=device, local_files_only=True)


class CrossEncoderReranker(ScorerReranker):
    """Local cross-encoder reranker; the model loads once per process.

    load() verifies the model exists in the local cache (downloads disabled)
    and is called by startup before the stack is marked ready. Reranking an
    empty input never loads the model.
    """

    def __init__(
        self,
        model_id="cross-encoder/ms-marco-MiniLM-L-6-v2",
        device="cpu",
    ):
        super().__init__(scorer=self._score_pairs, model_id=model_id)
        self._device = device

    def load(self):
        """Load the cached model once; fail explicitly when cache is missing."""
        try:
            _get_cross_encoder(self._model_id, self._device)
        except Exception as exc:  # missing/corrupt local cache
            raise ComponentNotReadyError(
                "local reranker model is not available from cache; downloads are disabled"
            ) from exc

    def _score_pairs(self, query, documents):
        model = _get_cross_encoder(self._model_id, self._device)
        pairs = [(query, document.text) for document in documents]
        return model.predict(pairs, show_progress_bar=False).tolist()
