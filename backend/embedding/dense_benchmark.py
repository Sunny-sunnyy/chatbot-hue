"""Native dense model runners and benchmark setting contracts for Phase 8 08a."""
from dataclasses import dataclass
import gc
import math
from typing import Literal
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

RunnerKind = Literal["sentence_transformer", "huydang"]
InputContract = Literal["e5", "pyvi_segmented"]


@dataclass(frozen=True)
class DenseBenchmarkSetting:
    order: int
    setting_key: str
    setting_label: str
    model_id: str
    revision: str
    dimension: int
    max_length: int
    collection_name: str
    runner_kind: RunnerKind
    input_contract: InputContract
    retrieval_mode: str = "dense"
    use_bm25: bool = False
    use_reranker: bool = False


@dataclass(frozen=True)
class DocumentEmbeddingResult:
    vectors: list[list[float]]
    truncated_document_count: int


E5_SMALL_SETTING = DenseBenchmarkSetting(
    order=1,
    setting_key="e5-small-384",
    setting_label="E5-small 384D (control)",
    model_id="intfloat/multilingual-e5-small",
    revision="614241f622f53c4eeff9890bdc4f31cfecc418b3",
    dimension=384,
    max_length=512,
    collection_name="hue_foods_08a_e5_small_384",
    runner_kind="sentence_transformer",
    input_contract="e5",
)

HUYDANG_DEK21_SETTING = DenseBenchmarkSetting(
    order=2,
    setting_key="huydang-dek21-embedding-768",
    setting_label="Huydang DEk21 768D",
    model_id="CODE4LIFEOFFICIAL/huydang-dek21-embedding",
    revision="517f1af7dd04a57194f1de2990f0c6ede0a3109b",
    dimension=768,
    max_length=256,
    collection_name="hue_foods_08a_huydang_dek21_768",
    runner_kind="huydang",
    input_contract="pyvi_segmented",
)

E5_BASE_SETTING = DenseBenchmarkSetting(
    order=3,
    setting_key="e5-base-768",
    setting_label="E5-base 768D",
    model_id="intfloat/multilingual-e5-base",
    revision="d128750597153bb5987e10b1c3493a34e5a4502a",
    dimension=768,
    max_length=512,
    collection_name="hue_foods_08a_e5_base_768",
    runner_kind="sentence_transformer",
    input_contract="e5",
)

ALL_DENSE_SETTINGS = (
    E5_SMALL_SETTING,
    HUYDANG_DEK21_SETTING,
    E5_BASE_SETTING,
)

DENSE_CANDIDATE_SETTINGS = (
    HUYDANG_DEK21_SETTING,
    E5_BASE_SETTING,
)


def _validate_vector(vector: list[float] | np.ndarray, expected_dim: int) -> list[float]:
    """Kiểm tra tính hợp lệ của một vector embedding (kích thước, giá trị hữu hạn, chuẩn L2)."""
    if isinstance(vector, np.ndarray):
        vec_list = [float(x) for x in vector.tolist()]
    else:
        vec_list = [float(x) for x in vector]

    if len(vec_list) != expected_dim:
        raise ValueError(f"Vector dimension {len(vec_list)} != expected {expected_dim}")

    norm_sq = 0.0
    for v in vec_list:
        if not math.isfinite(v):
            raise ValueError(f"Vector contains non-finite value: {v}")
        norm_sq += v * v

    norm = math.sqrt(norm_sq)
    if not math.isclose(norm, 1.0, rel_tol=1e-2, abs_tol=1e-2):
        raise ValueError(f"Vector L2 norm is {norm:.4f}, expected unit vector (~1.0)")

    return vec_list


def _validate_vectors(vectors: list[list[float]] | np.ndarray, expected_count: int, expected_dim: int) -> list[list[float]]:
    """Kiểm tra tập hợp các vector embedding."""
    if isinstance(vectors, np.ndarray):
        raw_list = vectors.tolist()
    else:
        raw_list = vectors

    if len(raw_list) != expected_count:
        raise ValueError(f"Vector count {len(raw_list)} != expected {expected_count}")

    validated: list[list[float]] = []
    for vec in raw_list:
        validated.append(_validate_vector(vec, expected_dim))
    return validated


def _count_truncated_documents(tokenizer, texts: list[str], max_length: int) -> int:
    """Đếm số lượng văn bản vượt quá max_length token của tokenizer."""
    truncated = 0
    for text in texts:
        tokens = tokenizer.encode(text, add_special_tokens=True, truncation=False)
        if len(tokens) > max_length:
            truncated += 1
    return truncated


class SentenceTransformerDenseRunner:
    """Runner cho họ mô hình SentenceTransformers (E5 family, MiniLM)."""

    def __init__(self, setting: DenseBenchmarkSetting) -> None:
        self.setting = setting
        self.model_id = setting.model_id
        self.dimension = setting.dimension
        self._model: SentenceTransformer | None = None

    def load(self) -> None:
        if self._model is None:
            self._model = SentenceTransformer(
                self.setting.model_id,
                revision=self.setting.revision,
                device="cpu",
            )
            self._model.eval()

    def embed_documents(self, documents: list[str]) -> DocumentEmbeddingResult:
        self.load()
        assert self._model is not None

        tokenizer = self._model.tokenizer
        if self.setting.input_contract == "e5":
            prepared_texts = [f"passage: {doc}" for doc in documents]
        else:
            prepared_texts = list(documents)

        truncated_count = _count_truncated_documents(
            tokenizer, prepared_texts, self.setting.max_length
        )

        encoded = self._model.encode(
            prepared_texts,
            batch_size=8,
            precision="float32",
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        validated = _validate_vectors(encoded, len(documents), self.setting.dimension)
        return DocumentEmbeddingResult(
            vectors=validated,
            truncated_document_count=truncated_count,
        )

    def embed_query(self, query: str) -> list[float]:
        self.load()
        assert self._model is not None

        if self.setting.input_contract == "e5":
            prepared_query = f"query: {query}"
        else:
            prepared_query = query

        encoded = self._model.encode(
            [prepared_query],
            batch_size=1,
            precision="float32",
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        validated = _validate_vectors(encoded, 1, self.setting.dimension)
        return validated[0]

    def close(self) -> None:
        self._model = None
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


class HuydangDenseRunner:
    """Runner cho mô hình Huydang DEk21 native 768D với ViTokenizer word segmentation."""

    def __init__(self, setting: DenseBenchmarkSetting) -> None:
        self.setting = setting
        self.model_id = setting.model_id
        self.dimension = setting.dimension
        self._model: SentenceTransformer | None = None

    def load(self) -> None:
        if self._model is None:
            self._model = SentenceTransformer(
                self.setting.model_id,
                revision=self.setting.revision,
                device="cpu",
            )
            self._model.eval()

    def embed_documents(self, documents: list[str]) -> DocumentEmbeddingResult:
        self.load()
        assert self._model is not None
        from pyvi import ViTokenizer

        tokenizer = self._model.tokenizer
        # Áp dụng ViTokenizer.tokenize() cho documents
        segmented_docs = [ViTokenizer.tokenize(doc) for doc in documents]

        truncated_count = _count_truncated_documents(
            tokenizer, segmented_docs, self.setting.max_length
        )

        encoded = self._model.encode(
            segmented_docs,
            batch_size=8,
            precision="float32",
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        validated = _validate_vectors(encoded, len(documents), self.setting.dimension)
        return DocumentEmbeddingResult(
            vectors=validated,
            truncated_document_count=truncated_count,
        )

    def embed_query(self, query: str) -> list[float]:
        self.load()
        assert self._model is not None
        from pyvi import ViTokenizer

        segmented_query = ViTokenizer.tokenize(query)
        encoded = self._model.encode(
            [segmented_query],
            batch_size=1,
            precision="float32",
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        validated = _validate_vectors(encoded, 1, self.setting.dimension)
        return validated[0]

    def close(self) -> None:
        self._model = None
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


def build_dense_runner(setting: DenseBenchmarkSetting):
    """Factory trực tiếp tạo runner tương ứng với cấu hình dense benchmark."""
    if setting.runner_kind == "sentence_transformer":
        return SentenceTransformerDenseRunner(setting)
    if setting.runner_kind == "huydang":
        return HuydangDenseRunner(setting)
    raise ValueError(f"unsupported runner kind: {setting.runner_kind}")
