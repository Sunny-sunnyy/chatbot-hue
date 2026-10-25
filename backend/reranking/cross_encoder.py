import math

from core.schema import ComponentNotReadyError, RetrievedDocument, RetrievalDependencyError

WARMUP_QUERY = "món ăn Huế"
WARMUP_DOCUMENT = "Bún bò Huế là một món ăn nổi tiếng của Huế."


class CrossEncoderReranker:
    def __init__(self, model_id="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu", max_length=None):
        # max_length: chỉ để harness Phase 8.1 G4 cắt cặp (câu hỏi, đoạn) cùng mức cho mọi model;
        # None = để sentence-transformers lấy theo tokenizer (hành vi đang chạy).
        self._model_id = model_id
        self._device = device
        self._max_length = max_length
        self._model = None

    @property
    def model_id(self):
        return self._model_id

    @property
    def loaded_device(self) -> str:
        """Thiết bị thật của model sau khi nạp (ví dụ `cuda:0`), để kiểm không chạy nhầm CPU."""
        return str(self.load()._model.device)

    @property
    def max_length(self) -> int:
        self.load()
        tokenizer = getattr(self._model, "tokenizer", None)
        max_len = getattr(tokenizer, "model_max_length", 512)
        return int(max_len) if isinstance(max_len, int) else 512

    def input_token_count(self, query: str, document: str) -> int:
        self.load()
        tokenizer = getattr(self._model, "tokenizer", None)
        if tokenizer is None:
            raise ComponentNotReadyError("reranker tokenizer not available")
        tokens = tokenizer.encode(query, document, add_special_tokens=True, truncation=False)
        return len(tokens)

    def load(self):
        if self._model is None:
            try:
                from sentence_transformers import CrossEncoder

                self._model = CrossEncoder(self._model_id, device=self._device, max_length=self._max_length)
            except Exception as exc:
                raise ComponentNotReadyError("reranker model load failed") from exc
        return self

    def _predict(self, pairs):
        try:
            raw = self.load()._model.predict(pairs, show_progress_bar=False)
            return list(raw.tolist() if hasattr(raw, "tolist") else raw)
        except ComponentNotReadyError:
            raise
        except Exception as exc:
            raise RetrievalDependencyError("reranker scoring failed") from exc

    @staticmethod
    def _finite_scores(scores, expected_count):
        if len(scores) != expected_count:
            raise RetrievalDependencyError(
                f"reranker returned {len(scores)} scores for {expected_count} documents"
            )
        converted = []
        for score in scores:
            try:
                value = float(score)
            except (TypeError, ValueError) as exc:
                raise RetrievalDependencyError("reranker returned a non-numeric score") from exc
            if not math.isfinite(value):
                raise RetrievalDependencyError("reranker returned a non-finite score")
            converted.append(value)
        return converted

    def score_documents(self, query: str, documents: list[RetrievedDocument]) -> list[float]:
        if not documents:
            return []
        pairs = [(query, doc.text) for doc in documents]
        return self._finite_scores(self._predict(pairs), len(documents))

    def warm_up(self):
        try:
            return self._finite_scores(self._predict([(WARMUP_QUERY, WARMUP_DOCUMENT)]), 1)[0]
        except Exception as exc:
            if isinstance(exc, ComponentNotReadyError):
                raise
            raise ComponentNotReadyError("reranker warm-up prediction failed") from exc
