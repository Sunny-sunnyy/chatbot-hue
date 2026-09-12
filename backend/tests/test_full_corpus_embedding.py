"""Deterministic tests for full-corpus dense embedding specifications and preprocessing."""

import math
from pathlib import Path
import numpy as np
import pytest
from pyvi import ViTokenizer

from backend.embedding.full_corpus import (
    DENSE_MODEL_SPECS,
    QWEN_QUERY_TASK,
    DenseModelSpec,
    prepare_document,
    prepare_query,
    validate_snapshot_path,
    validate_vectors,
)


def test_dense_specs_are_exact_and_ordered() -> None:
    assert [
        (
            s.key,
            s.model_id,
            s.revision,
            s.dimension,
            s.max_tokens,
            s.device,
            s.dtype,
            s.batch_size,
        )
        for s in DENSE_MODEL_SPECS
    ] == [
        (
            "e5-small-384",
            "intfloat/multilingual-e5-small",
            "614241f622f53c4eeff9890bdc4f31cfecc418b3",
            384,
            512,
            "cpu",
            "float32",
            8,
        ),
        (
            "e5-base-768",
            "intfloat/multilingual-e5-base",
            "d128750597153bb5987e10b1c3493a34e5a4502a",
            768,
            512,
            "cpu",
            "float32",
            8,
        ),
        (
            "huydang-dek21-768",
            "CODE4LIFEOFFICIAL/huydang-dek21-embedding",
            "517f1af7dd04a57194f1de2990f0c6ede0a3109b",
            768,
            256,
            "cpu",
            "float32",
            8,
        ),
        (
            "qwen3-embedding-0.6b-1024",
            "Qwen/Qwen3-Embedding-0.6B",
            "97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3",
            1024,
            32768,
            "cuda",
            "float16",
            1,
        ),
    ]


def test_role_preprocessing_is_exact() -> None:
    e5_small, e5_base, huydang, qwen = DENSE_MODEL_SPECS
    assert prepare_document(e5_small, "Văn bản") == "passage: Văn bản"
    assert prepare_query(e5_small, "Câu hỏi") == "query: Câu hỏi"
    assert prepare_document(e5_base, "Văn bản") == "passage: Văn bản"
    assert prepare_query(e5_base, "Câu hỏi") == "query: Câu hỏi"
    assert prepare_document(huydang, "Văn bản") == ViTokenizer.tokenize("Văn bản")
    assert prepare_query(huydang, "Câu hỏi") == ViTokenizer.tokenize("Câu hỏi")
    assert prepare_document(qwen, "Văn bản") == "Văn bản"
    assert prepare_query(qwen, "Câu hỏi") == (
        "Instruct: Given a Vietnamese question about Hue culture, heritage, "
        "festivals, performing arts, food, and travel, retrieve relevant "
        "Vietnamese passages that answer the question.\nQuery: Câu hỏi"
    )


def test_role_preprocessing_rejects_empty_or_whitespace() -> None:
    spec = DENSE_MODEL_SPECS[0]
    for invalid in ("", "   ", "\n\t"):
        with pytest.raises(ValueError, match="non-empty"):
            prepare_document(spec, invalid)
        with pytest.raises(ValueError, match="non-empty"):
            prepare_query(spec, invalid)


def test_role_preprocessing_rejects_unknown_contract() -> None:
    invalid_spec = DenseModelSpec(
        key="unknown",
        model_id="org/unknown",
        revision="0" * 40,
        dimension=128,
        max_tokens=128,
        input_contract="invalid",  # type: ignore[arg-type]
        device="cpu",
        dtype="float32",
        batch_size=1,
    )
    with pytest.raises(ValueError, match="Unknown input contract"):
        prepare_document(invalid_spec, "Hợp lệ")
    with pytest.raises(ValueError, match="Unknown input contract"):
        prepare_query(invalid_spec, "Hợp lệ")


def test_validate_snapshot_path_success(tmp_path: Path) -> None:
    revision = "614241f622f53c4eeff9890bdc4f31cfecc418b3"
    rev_dir = tmp_path / revision
    rev_dir.mkdir()
    resolved = validate_snapshot_path(rev_dir, revision)
    assert resolved == rev_dir.resolve()


def test_validate_snapshot_path_mismatch(tmp_path: Path) -> None:
    revision = "614241f622f53c4eeff9890bdc4f31cfecc418b3"
    wrong_dir = tmp_path / "wrong_revision_name"
    wrong_dir.mkdir()
    with pytest.raises(ValueError, match="does not match expected revision"):
        validate_snapshot_path(wrong_dir, revision)


def test_validate_snapshot_path_missing(tmp_path: Path) -> None:
    revision = "614241f622f53c4eeff9890bdc4f31cfecc418b3"
    missing_dir = tmp_path / revision
    with pytest.raises(ValueError, match="does not exist or is not a directory"):
        validate_snapshot_path(missing_dir, revision)


def test_validate_vectors_success() -> None:
    vec1 = [1.0, 0.0, 0.0]
    vec2 = [0.0, 1.0, 0.0]
    validated = validate_vectors([vec1, vec2], expected_count=2, expected_dim=3)
    assert len(validated) == 2
    assert validated[0] == vec1
    assert validated[1] == vec2


def test_validate_vectors_from_numpy() -> None:
    arr = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    validated = validate_vectors(arr, expected_count=2, expected_dim=2)
    assert len(validated) == 2
    assert validated[0] == [1.0, 0.0]


def test_validate_vectors_wrong_count() -> None:
    vec = [[1.0, 0.0]]
    with pytest.raises(ValueError, match="Vector count 1 != expected 2"):
        validate_vectors(vec, expected_count=2, expected_dim=2)


def test_validate_vectors_wrong_dim() -> None:
    vec = [[1.0, 0.0, 0.0]]
    with pytest.raises(ValueError, match="Vector dimension 3 != expected 2"):
        validate_vectors(vec, expected_count=1, expected_dim=2)


def test_validate_vectors_non_finite() -> None:
    vec_inf = [[1.0, float("inf")]]
    with pytest.raises(ValueError, match="non-finite value"):
        validate_vectors(vec_inf, expected_count=1, expected_dim=2)

    vec_nan = [[1.0, float("nan")]]
    with pytest.raises(ValueError, match="non-finite value"):
        validate_vectors(vec_nan, expected_count=1, expected_dim=2)


def test_validate_vectors_non_unit_norm() -> None:
    vec_unnorm = [[2.0, 0.0]]
    with pytest.raises(ValueError, match="expected unit vector"):
        validate_vectors(vec_unnorm, expected_count=1, expected_dim=2)
