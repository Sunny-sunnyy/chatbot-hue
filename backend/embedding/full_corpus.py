"""Khai báo hợp đồng dense model, tiền xử lý vai trò và runner tuần tự cho Phase 3."""

from collections.abc import Sequence
from dataclasses import dataclass
import gc
import math
from pathlib import Path
from typing import Any, Literal
from huggingface_hub import snapshot_download
import numpy as np
from pyvi import ViTokenizer
from sentence_transformers import SentenceTransformer
import torch


@dataclass(frozen=True)
class DenseModelSpec:
    """Hợp đồng bất biến cho một ứng viên dense embedding trong Phase 3."""

    key: str
    model_id: str
    revision: str
    dimension: int
    max_tokens: int
    input_contract: Literal["e5", "pyvi", "qwen3"]
    device: Literal["cpu", "cuda"]
    dtype: Literal["float32", "float16"]
    batch_size: int


# Bốn dense model specs chuẩn hóa đã được User phê duyệt trong Phase 3
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
    ),
    DenseModelSpec(
        key="e5-base-768",
        model_id="intfloat/multilingual-e5-base",
        revision="d128750597153bb5987e10b1c3493a34e5a4502a",
        dimension=768,
        max_tokens=512,
        input_contract="e5",
        device="cpu",
        dtype="float32",
        batch_size=8,
    ),
    DenseModelSpec(
        key="huydang-dek21-768",
        model_id="CODE4LIFEOFFICIAL/huydang-dek21-embedding",
        revision="517f1af7dd04a57194f1de2990f0c6ede0a3109b",
        dimension=768,
        max_tokens=256,
        input_contract="pyvi",
        device="cpu",
        dtype="float32",
        batch_size=8,
    ),
    DenseModelSpec(
        key="qwen3-embedding-0.6b-1024",
        model_id="Qwen/Qwen3-Embedding-0.6B",
        revision="97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3",
        dimension=1024,
        max_tokens=32768,
        input_contract="qwen3",
        device="cuda",
        dtype="float16",
        batch_size=1,
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
    elif spec.input_contract == "pyvi":
        return ViTokenizer.tokenize(text)
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
    elif spec.input_contract == "pyvi":
        return ViTokenizer.tokenize(query)
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


def count_tokens(tokenizer: Any, prepared_text: str) -> int:
    """Đếm số token khi áp dụng đầy đủ special tokens và không cắt ngắn (truncation=False)."""
    tokens = tokenizer.encode(prepared_text, add_special_tokens=True, truncation=False)
    return len(tokens)


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
        # Kiểm tra chuẩn L2 xấp xỉ 1.0 (cho phép sai số float16 trong ngưỡng 1e-3)
        if not math.isclose(norm, 1.0, rel_tol=1e-3, abs_tol=1e-3):
            raise ValueError(f"Vector L2 norm is {norm:.4f}, expected unit vector (~1.0)")
        validated.append(vec)

    return validated


class FullCorpusDenseRunner:
    """Runner thực thi tuần tự cho từng dense embedding candidate trong Phase 3."""

    def __init__(self, spec: DenseModelSpec, snapshot_path: Path) -> None:
        self.spec = spec
        self.snapshot_path = validate_snapshot_path(snapshot_path, spec.revision)
        self._model: SentenceTransformer | None = None

    def load(self) -> None:
        """Tải mô hình vào đúng device và dtype theo spec đã duyệt; không dùng device_map tự động."""
        if self._model is not None:
            return

        model_kwargs: dict[str, Any] = {}
        if self.spec.device == "cuda":
            if not torch.cuda.is_available():
                raise RuntimeError(
                    f"CUDA is required for model {self.spec.key} but torch.cuda.is_available() is False"
                )
            model_kwargs["torch_dtype"] = torch.float16
            model_kwargs["attn_implementation"] = "eager"
            device = "cuda"
        else:
            model_kwargs["torch_dtype"] = torch.float32
            device = "cpu"

        # Tải SentenceTransformer trực tiếp từ đường dẫn snapshot đã xác thực revision
        self._model = SentenceTransformer(
            str(self.snapshot_path),
            device=device,
            model_kwargs=model_kwargs,
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
            expected_torch_dtype = torch.float16 if self.spec.dtype == "float16" else torch.float32
            if first_param.dtype != expected_torch_dtype:
                raise ValueError(
                    f"Parameter dtype mismatch for {self.spec.key}: actual {first_param.dtype} != expected {expected_torch_dtype}"
                )

    def tokenizer(self) -> Any:
        """Trả về tokenizer của mô hình."""
        if self._model is None:
            self.load()
        assert self._model is not None
        return self._model.tokenizer

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        """Mã hóa danh sách văn bản theo đúng document preprocessing và kiểm tra vector đầu ra."""
        if self._model is None:
            self.load()
        assert self._model is not None

        if not texts:
            return []

        prepared = [prepare_document(self.spec, t) for t in texts]
        raw_vectors = self._model.encode(
            prepared,
            batch_size=self.spec.batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return validate_vectors(raw_vectors, expected_count=len(texts), expected_dim=self.spec.dimension)

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

    def runtime_identity(self) -> dict[str, object]:
        """Trả về thông tin định danh runtime phục vụ kiểm tra bằng chứng."""
        return {
            "key": self.spec.key,
            "model_id": self.spec.model_id,
            "revision": self.spec.revision,
            "dimension": self.spec.dimension,
            "max_tokens": self.spec.max_tokens,
            "input_contract": self.spec.input_contract,
            "device": self.spec.device,
            "dtype": self.spec.dtype,
            "batch_size": self.spec.batch_size,
            "snapshot_path": str(self.snapshot_path),
            "loaded": self._model is not None,
        }

    def observed_runtime_state(self) -> dict[str, Any]:
        """Trả về các trường quan sát thực tế từ model instance đã nạp."""
        if self._model is None:
            return {}
        first_param = next(self._model.parameters(), None)
        dim_getter = getattr(self._model, "get_embedding_dimension", None) or getattr(
            self._model, "get_sentence_embedding_dimension", None
        )
        actual_dim = dim_getter() if dim_getter is not None else None
        return {
            "dimension": actual_dim,
            "parameter_device": str(first_param.device) if first_param is not None else None,
            "parameter_dtype": str(first_param.dtype) if first_param is not None else None,
            "attn_implementation": getattr(
                getattr(self._model, "config", None),
                "_attn_implementation",
                "eager",
            ),
        }

    def close(self) -> None:
        """Giải phóng mô hình khỏi bộ nhớ RAM/VRAM và dọn dẹp cache CUDA."""
        self._model = None
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
