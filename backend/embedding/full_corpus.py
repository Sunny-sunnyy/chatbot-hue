"""Khai báo hợp đồng dense model, tiền xử lý vai trò và runner local/OpenRouter cho full-corpus."""

from collections.abc import Sequence
from dataclasses import dataclass
import gc
import logging
import math
import os
from pathlib import Path
from typing import Any, Literal
import httpx
from huggingface_hub import snapshot_download
import numpy as np
from sentence_transformers import SentenceTransformer
import torch

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DenseModelSpec:
    """Hợp đồng bất biến cho một ứng viên dense embedding full-corpus.

    Model `local` chạy bằng SentenceTransformer từ snapshot HF đúng revision;
    model `openrouter` gọi API nên không có revision/device/dtype local.
    """

    key: str
    model_id: str
    revision: str | None
    dimension: int
    max_tokens: int
    input_contract: Literal["e5", "qwen3"]
    device: Literal["cpu"] | None
    dtype: Literal["float32"] | None
    batch_size: int
    provider: Literal["local", "openrouter"]


# Hai dense model specs full-corpus được User chốt trong Phase 7A2
DENSE_MODEL_SPECS: tuple[DenseModelSpec, ...] = (
    DenseModelSpec(
        key="e5-small-384",
        model_id="intfloat/multilingual-e5-small",
        revision="614241f622f53c4eeff9890bdc4f31cfecc418b3",
        dimension=384,
        max_tokens=512,
        input_contract="e5",
        device="cpu",
        dtype="float32",
        batch_size=8,
        provider="local",
    ),
    DenseModelSpec(
        key="qwen3-embedding-8b-4096",
        model_id="qwen/qwen3-embedding-8b",
        revision=None,
        dimension=4096,
        max_tokens=32768,
        input_contract="qwen3",
        device=None,
        dtype=None,
        batch_size=64,
        provider="openrouter",
    ),
)

# Nhiệm vụ hướng dẫn cố định bằng tiếng Anh dành riêng cho query của Qwen
QWEN_QUERY_TASK: str = (
    "Given a Vietnamese question about Hue culture, heritage, "
    "festivals, performing arts, food, and travel, retrieve relevant "
    "Vietnamese passages that answer the question."
)


def prepare_document(spec: DenseModelSpec, text: str) -> str:
    """Áp dụng tiền xử lý document theo đúng hợp đồng của mô hình."""
    if not text or not text.strip():
        raise ValueError("Input document text must be non-empty and non-whitespace.")

    if spec.input_contract == "e5":
        return f"passage: {text}"
    elif spec.input_contract == "qwen3":
        # Document của Qwen giữ nguyên Representation A, không gắn instruction
        return text
    else:
        raise ValueError(f"Unknown input contract: {spec.input_contract}")


def prepare_query(spec: DenseModelSpec, query: str) -> str:
    """Áp dụng tiền xử lý query theo đúng hợp đồng của mô hình."""
    if not query or not query.strip():
        raise ValueError("Input query text must be non-empty and non-whitespace.")

    if spec.input_contract == "e5":
        return f"query: {query}"
    elif spec.input_contract == "qwen3":
        return f"Instruct: {QWEN_QUERY_TASK}\nQuery: {query}"
    else:
        raise ValueError(f"Unknown input contract: {spec.input_contract}")


def validate_snapshot_path(snapshot_path: Path, expected_revision: str) -> Path:
    """Kiểm tra đường dẫn snapshot tồn tại và có tên thư mục khớp chính xác revision SHA."""
    resolved = snapshot_path.resolve()
    if not resolved.is_dir():
        raise ValueError(f"Snapshot path does not exist or is not a directory: {resolved}")
    if resolved.name != expected_revision:
        raise ValueError(
            f"Snapshot directory name {resolved.name!r} does not match expected revision {expected_revision!r}"
        )
    return resolved


def resolve_snapshot(spec: DenseModelSpec, allow_download: bool) -> Path:
    """Phân giải snapshot từ Hugging Face cache hoặc tải về ở đúng exact revision."""
    raw_path = snapshot_download(
        repo_id=spec.model_id,
        revision=spec.revision,
        local_files_only=not allow_download,
    )
    return validate_snapshot_path(Path(raw_path), spec.revision)


def validate_vectors(
    vectors: Sequence[Sequence[float]] | np.ndarray,
    expected_count: int,
    expected_dim: int,
) -> list[list[float]]:
    """Kiểm tra tính hợp lệ của danh sách vector embedding: số lượng, chiều, finite và chuẩn L2."""
    if isinstance(vectors, np.ndarray):
        raw_list: list[list[float]] = vectors.tolist()
    elif isinstance(vectors, list):
        raw_list = vectors
    else:
        raw_list = list(vectors)  # type: ignore[arg-type]

    if len(raw_list) != expected_count:
        raise ValueError(f"Vector count {len(raw_list)} != expected {expected_count}")

    validated: list[list[float]] = []
    for vec in raw_list:
        if len(vec) != expected_dim:
            raise ValueError(f"Vector dimension {len(vec)} != expected {expected_dim}")

        norm_sq = 0.0
        for v in vec:
            if not math.isfinite(v):
                raise ValueError(f"Vector contains non-finite value: {v}")
            norm_sq += v * v

        norm = math.sqrt(norm_sq)
        # Kiểm tra chuẩn L2 xấp xỉ 1.0 (cho phép sai số làm tròn trong ngưỡng 1e-3)
        if not math.isclose(norm, 1.0, rel_tol=1e-3, abs_tol=1e-3):
            raise ValueError(f"Vector L2 norm is {norm:.4f}, expected unit vector (~1.0)")
        validated.append(vec)

    return validated


def validate_vector_matrix(
    vectors: np.ndarray,
    expected_count: int,
    expected_dim: int,
) -> np.ndarray:
    """Validate a dense matrix without materializing nested Python lists."""
    if not isinstance(vectors, np.ndarray):
        raise ValueError("Dense vectors must be a NumPy array")
    if vectors.shape != (expected_count, expected_dim):
        raise ValueError(
            f"Dense matrix shape {vectors.shape} != "
            f"({expected_count}, {expected_dim})"
        )
    if not np.issubdtype(vectors.dtype, np.floating):
        raise ValueError(f"Dense matrix must have floating dtype, got {vectors.dtype}")
    if not np.isfinite(vectors).all():
        raise ValueError("Dense matrix contains non-finite values")
    norms = np.linalg.norm(vectors.astype(np.float64, copy=False), axis=1)
    invalid = np.flatnonzero(~np.isclose(norms, 1.0, rtol=1e-3, atol=1e-3))
    if invalid.size:
        index = int(invalid[0])
        raise ValueError(
            f"Dense vector {index} L2 norm is {norms[index]:.6f}, "
            "expected unit vector (~1.0)"
        )
    return vectors


class FullCorpusDenseRunner:
    """Runner local chạy SentenceTransformer cho một dense candidate."""

    def __init__(self, spec: DenseModelSpec, snapshot_path: Path) -> None:
        self.spec = spec
        self.snapshot_path = validate_snapshot_path(snapshot_path, spec.revision)
        self._model: SentenceTransformer | None = None

    def load(self) -> None:
        """Tải mô hình trên CPU float32 (spec local duy nhất là CPU); không dùng device_map tự động."""
        if self._model is not None:
            return

        # Tải SentenceTransformer trực tiếp từ đường dẫn snapshot đã xác thực revision
        self._model = SentenceTransformer(
            str(self.snapshot_path),
            device="cpu",
            model_kwargs={"torch_dtype": torch.float32},
        )

        # Xác thực kích thước vector output khớp với spec
        dim_getter = getattr(self._model, "get_embedding_dimension", None) or getattr(
            self._model, "get_sentence_embedding_dimension", None
        )
        actual_dim = dim_getter() if dim_getter is not None else None
        if actual_dim != self.spec.dimension:
            raise ValueError(
                f"Model dimension mismatch for {self.spec.key}: actual {actual_dim} != expected {self.spec.dimension}"
            )

        # Xác thực parameter device và dtype thực tế
        first_param = next(self._model.parameters(), None)
        if first_param is not None:
            param_device_type = first_param.device.type
            if param_device_type != self.spec.device:
                raise ValueError(
                    f"Parameter device mismatch for {self.spec.key}: actual {param_device_type} != expected {self.spec.device}"
                )
            if first_param.dtype != torch.float32:
                raise ValueError(
                    f"Parameter dtype mismatch for {self.spec.key}: actual {first_param.dtype} != expected {torch.float32}"
                )

    def embed_documents_matrix(self, texts: Sequence[str]) -> np.ndarray:
        """Encode documents into one validated NumPy matrix for Phase 4."""
        if self._model is None:
            self.load()
        assert self._model is not None
        if not texts:
            return np.empty((0, self.spec.dimension), dtype=np.float32)
        prepared = [prepare_document(self.spec, text) for text in texts]
        raw_vectors = self._model.encode(
            prepared,
            batch_size=self.spec.batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        if not isinstance(raw_vectors, np.ndarray):
            raise ValueError("SentenceTransformer did not return a NumPy array")
        return validate_vector_matrix(raw_vectors, len(texts), self.spec.dimension)

    def embed_queries(self, queries: Sequence[str]) -> list[list[float]]:
        """Mã hóa danh sách câu hỏi theo đúng query preprocessing và kiểm tra vector đầu ra."""
        if self._model is None:
            self.load()
        assert self._model is not None

        if not queries:
            return []

        prepared = [prepare_query(self.spec, q) for q in queries]
        raw_vectors = self._model.encode(
            prepared,
            batch_size=self.spec.batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return validate_vectors(raw_vectors, expected_count=len(queries), expected_dim=self.spec.dimension)

    def close(self) -> None:
        """Giải phóng mô hình khỏi bộ nhớ RAM/VRAM và dọn dẹp cache CUDA."""
        self._model = None
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


OPENROUTER_EMBEDDINGS_URL = "https://openrouter.ai/api/v1/embeddings"
# Pin một provider cho cả build và query: build không pin đầu tiên trộn ba provider
# và cho cos mẫu min 0,99535 (amendment User 2026-10-24, spec §5.2).
OPENROUTER_PROVIDER_ROUTING = {"order": ["nebius"], "allow_fallbacks": False, "data_collection": "deny"}
OPENROUTER_EXPECTED_PROVIDER = "Nebius"


def parse_embeddings_response(
    body: dict[str, Any], expected_count: int, dimension: int
) -> tuple[np.ndarray, str]:
    """Sắp vector theo `index`, kiểm số lượng/số chiều và provider đã pin; sai thì raise.

    Trả về ma trận vector và tên provider đã phục vụ (field `provider` của body).
    """
    if "data" not in body:
        raise ValueError(f"OpenRouter response has no data: {body.get('error')}")
    if body.get("provider") != OPENROUTER_EXPECTED_PROVIDER:
        raise ValueError(
            f"OpenRouter provider {body.get('provider')!r} != {OPENROUTER_EXPECTED_PROVIDER!r}"
        )
    rows = sorted(body["data"], key=lambda item: item["index"])
    if [item["index"] for item in rows] != list(range(expected_count)):
        raise ValueError("OpenRouter response index mismatch")
    matrix = np.asarray([item["embedding"] for item in rows], dtype=np.float32)
    if matrix.shape != (expected_count, dimension):
        raise ValueError(
            f"OpenRouter response shape {matrix.shape} != {(expected_count, dimension)}"
        )
    return matrix, body["provider"]


class OpenRouterDenseRunner:
    """Gọi OpenRouter embeddings theo batch cố định; lỗi thì raise, không retry/fallback.

    Mọi request pin Nebius (`allow_fallbacks: false`) và yêu cầu `data_collection: deny`.
    `providers_seen` ghi các provider đã thực sự phục vụ để đưa vào build record.
    """

    def __init__(self, spec: DenseModelSpec) -> None:
        self.spec = spec
        self.providers_seen: set[str] = set()
        self._client: httpx.Client | None = None

    def load(self) -> None:
        if self._client is not None:
            return
        self._client = httpx.Client(
            timeout=180,
            headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
        )

    def _embed(self, texts: Sequence[str]) -> np.ndarray:
        if self._client is None:
            self.load()
        assert self._client is not None
        response = self._client.post(OPENROUTER_EMBEDDINGS_URL, json={
            "model": self.spec.model_id,
            "input": list(texts),
            "encoding_format": "float",
            "provider": OPENROUTER_PROVIDER_ROUTING,
        })
        if response.status_code != 200:
            raise RuntimeError(
                f"OpenRouter HTTP {response.status_code}: {response.text[:500]}"
            )
        matrix, provider = parse_embeddings_response(
            response.json(), len(texts), self.spec.dimension
        )
        self.providers_seen.add(provider)
        return matrix

    def embed_documents_matrix(self, texts: Sequence[str]) -> np.ndarray:
        """Embed documents theo batch `spec.batch_size`; một batch lỗi làm cả lần build dừng."""
        if not texts:
            return np.empty((0, self.spec.dimension), dtype=np.float32)
        prepared = [prepare_document(self.spec, text) for text in texts]
        size = self.spec.batch_size
        batches = [prepared[i:i + size] for i in range(0, len(prepared), size)]
        matrices = []
        for number, batch in enumerate(batches, start=1):
            matrices.append(self._embed(batch))
            logger.info("OpenRouter embedding batch %d/%d done", number, len(batches))
        return validate_vector_matrix(np.vstack(matrices), len(texts), self.spec.dimension)

    def embed_queries(self, queries: Sequence[str]) -> list[list[float]]:
        """Một request cho toàn bộ queries truyền vào (runtime gọi với một query)."""
        if not queries:
            return []
        matrix = self._embed([prepare_query(self.spec, q) for q in queries])
        return validate_vectors(matrix, expected_count=len(queries), expected_dim=self.spec.dimension)

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None


def create_dense_runner(spec: DenseModelSpec) -> FullCorpusDenseRunner | OpenRouterDenseRunner:
    """Chọn runner theo provider của spec; dùng chung cho build và runtime."""
    if spec.provider == "openrouter":
        return OpenRouterDenseRunner(spec)
    return FullCorpusDenseRunner(spec, resolve_snapshot(spec, allow_download=False))
