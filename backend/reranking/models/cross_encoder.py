"""Local MiniLM CrossEncoder reranker baseline on CPU, cache-only."""
import math
from functools import lru_cache

from core.schema import ComponentNotReadyError
from reranking.reranker import ScorerReranker

# Internal warm-up pair: verifies the cached model produces one finite score
# at startup; never a user query and never logged.
WARMUP_QUERY = "món ăn Huế"
WARMUP_DOCUMENT = "Bún bò Huế là một món ăn nổi tiếng của Huế."


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

    def warm_up(self):
        """Run one prediction on the internal pair; fail when score is invalid.

        A cached model that loads but returns a non-numeric, non-finite or
        unexpected number of scores must never be marked ready.
        """
        try:
            model = _get_cross_encoder(self._model_id, self._device)
            scores = model.predict(
                [(WARMUP_QUERY, WARMUP_DOCUMENT)], show_progress_bar=False
            ).tolist()
        except Exception as exc:  # load or prediction failures
            raise ComponentNotReadyError(
                "local reranker warm-up prediction failed"
            ) from exc
        if len(scores) != 1:
            raise ComponentNotReadyError(
                "local reranker warm-up returned an unexpected score count"
            )
        raw = scores[0]
        try:
            score = float(raw)
        except (TypeError, ValueError) as exc:
            raise ComponentNotReadyError(
                "local reranker warm-up returned a non-numeric score"
            ) from exc
        if not math.isfinite(score):
            raise ComponentNotReadyError(
                "local reranker warm-up returned a non-finite score"
            )
        return score

    def _score_pairs(self, query, documents):
        model = _get_cross_encoder(self._model_id, self._device)
        pairs = [(query, document.text) for document in documents]
        return model.predict(pairs, show_progress_bar=False).tolist()
