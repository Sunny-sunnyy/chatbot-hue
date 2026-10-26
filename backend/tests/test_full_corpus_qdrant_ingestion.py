from pathlib import Path
import hashlib

import pytest

from embedding.sparse import SparseState
from ingestion.source_state import (
    make_full_corpus_build_record,
    serialize_full_corpus_build_record,
    verify_full_corpus_record_freshness,
    write_final_full_corpus_build_record,
)

CORPUS_ID = "a" * 64
SPARSE_SHA = "b" * 64


def sparse_state() -> SparseState:
    return SparseState(
        schema_version="phase_3_sparse_state:v1",
        corpus_identity=CORPUS_ID,
        document_count=3,
        average_document_length=4.0,
        k1=1.5,
        b=0.75,
        tokenizer="backend.scoring.bm25.tokenize:v1",
        vocabulary=("bún", "bò", "huế"),
        idf=(1.0, 1.0, 1.0),
    )


def source_hashes() -> dict[str, str]:
    return {
        f"foods/source-{index:03d}.md": hashlib.sha256(str(index).encode()).hexdigest()
        for index in range(3)
    }


def build_record(providers: tuple[str, ...] = ()) -> dict[str, object]:
    return make_full_corpus_build_record(
        collection_name="hue_full_corpus_7a2_e5_small_384",
        candidate_id="e5-small-384",
        dense={
            "model_id": "intfloat/multilingual-e5-small",
            "revision": "614241f622f53c4eeff9890bdc4f31cfecc418b3",
            "dimension": 384,
        },
        sources=source_hashes(),
        chunk_count=3,
        corpus_identity=CORPUS_ID,
        sparse_state=sparse_state(),
        sparse_state_sha256=SPARSE_SHA,
        providers=providers,
    )


def test_full_corpus_record_is_exact_and_deterministic() -> None:
    record = build_record()
    assert set(record) == {
        "schema_version", "status", "collection_name", "representation",
        "corpus", "dense", "sparse", "qdrant",
    }
    assert record["status"] == "complete"
    assert record["schema_version"] == "full_corpus_build:v3"
    # Số file/chunk lấy từ chính lần build, không từ hằng số cứng
    assert record["corpus"]["file_count"] == 3
    assert record["corpus"]["chunk_count"] == 3
    assert record["qdrant"]["point_count"] == 3
    assert record["qdrant"]["payload_schema_version"] == "full_corpus_qdrant_payload:v2"
    assert record["dense"]["providers"] == []
    assert build_record(("SiliconFlow", "Nebius"))["dense"]["providers"] == ["Nebius", "SiliconFlow"]
    assert serialize_full_corpus_build_record(record) == (
        serialize_full_corpus_build_record(build_record())
    )
    text = serialize_full_corpus_build_record(record).decode("utf-8")
    for forbidden in ("timestamp", "run_id", "endpoint", "absolute_path"):
        assert forbidden not in text


def test_final_record_write_is_atomic_and_exclusive(tmp_path: Path) -> None:
    path = tmp_path / "hue_full_corpus_7a2_e5_small_384.json"
    expected = serialize_full_corpus_build_record(build_record())
    digest = write_final_full_corpus_build_record(build_record(), path)
    assert path.read_bytes() == expected
    assert digest == hashlib.sha256(expected).hexdigest()
    assert list(tmp_path.glob("*.tmp.*")) == []
    with pytest.raises(FileExistsError, match="already exists"):
        write_final_full_corpus_build_record(build_record(), path)
    assert path.read_bytes() == expected
    assert list(tmp_path.glob("*.tmp.*")) == []

    preexisting_path = tmp_path / "preexisting.json"
    preexisting_path.write_bytes(b'{"preserved": true}')
    with pytest.raises(FileExistsError, match="already exists"):
        write_final_full_corpus_build_record(build_record(), preexisting_path)
    assert preexisting_path.read_bytes() == b'{"preserved": true}'
    assert list(tmp_path.glob("*.tmp.*")) == []


def test_full_corpus_record_freshness_reports_exact_changes() -> None:
    record = build_record()
    current = source_hashes()
    assert verify_full_corpus_record_freshness(current, record) == (True, [])
    changed = dict(current)
    changed["foods/source-000.md"] = "f" * 64
    changed["travel/new.md"] = "a" * 64
    del changed["foods/source-001.md"]
    fresh, discrepancies = verify_full_corpus_record_freshness(changed, record)
    assert fresh is False
    assert any(item.startswith("Added files:") for item in discrepancies)
    assert any(item.startswith("Deleted files:") for item in discrepancies)
    assert any(item.startswith("Content changed:") for item in discrepancies)


from qdrant_client import models

from vectorstore.qdrant import (
    QdrantSchemaError,
    classify_full_corpus_target,
    expected_full_corpus_schema,
    require_fresh_full_corpus_target,
    validate_full_corpus_collection_params,
)


def test_full_corpus_schema_is_exact_and_has_no_idf_modifier() -> None:
    dense, sparse = expected_full_corpus_schema(4096)
    assert set(dense) == {"dense"}
    assert dense["dense"].size == 4096
    assert dense["dense"].distance == models.Distance.COSINE
    assert dense["dense"].on_disk is None
    assert dense["dense"].quantization_config is None
    assert set(sparse) == {"sparse"}
    assert sparse["sparse"] == models.SparseVectorParams()
    assert sparse["sparse"].modifier is None


def test_full_corpus_schema_validation_rejects_idf_and_extra_vectors() -> None:
    dense, sparse = expected_full_corpus_schema(384)
    validate_full_corpus_collection_params(
        models.CollectionParams(vectors=dense, sparse_vectors=sparse), 384
    )
    with pytest.raises(QdrantSchemaError, match="sparse"):
        validate_full_corpus_collection_params(
            models.CollectionParams(
                vectors=dense,
                sparse_vectors={
                    "sparse": models.SparseVectorParams(modifier=models.Modifier.IDF)
                },
            ),
            384,
        )
    with pytest.raises(QdrantSchemaError, match="dense vector names"):
        validate_full_corpus_collection_params(
            models.CollectionParams(
                vectors={
                    **dense,
                    "extra": models.VectorParams(size=2, distance=models.Distance.COSINE),
                },
                sparse_vectors=sparse,
            ),
            384,
        )
    with pytest.raises(QdrantSchemaError, match="dense vector on_disk is not allowed"):
        validate_full_corpus_collection_params(
            models.CollectionParams(
                vectors={
                    "dense": models.VectorParams(
                        size=384, distance=models.Distance.COSINE, on_disk=True
                    )
                },
                sparse_vectors=sparse,
            ),
            384,
        )
    with pytest.raises(QdrantSchemaError, match="sparse index on_disk is not allowed"):
        validate_full_corpus_collection_params(
            models.CollectionParams(
                vectors=dense,
                sparse_vectors={
                    "sparse": models.SparseVectorParams(
                        index=models.SparseIndexParams(on_disk=True)
                    )
                },
            ),
            384,
        )
    with pytest.raises(QdrantSchemaError, match="dense vector custom hnsw_config is not allowed"):
        validate_full_corpus_collection_params(
            models.CollectionParams(
                vectors={
                    "dense": models.VectorParams(
                        size=384,
                        distance=models.Distance.COSINE,
                        hnsw_config=models.HnswConfigDiff(m=16),
                    )
                },
                sparse_vectors=sparse,
            ),
            384,
        )
    with pytest.raises(QdrantSchemaError, match="dense vector custom quantization_config is not allowed"):
        validate_full_corpus_collection_params(
            models.CollectionParams(
                vectors={
                    "dense": models.VectorParams(
                        size=384,
                        distance=models.Distance.COSINE,
                        quantization_config=models.ScalarQuantization(
                            scalar=models.ScalarQuantizationConfig(
                                type=models.ScalarType.INT8
                            )
                        ),
                    )
                },
                sparse_vectors=sparse,
            ),
            384,
        )
    with pytest.raises(QdrantSchemaError, match="sparse index custom parameters are not allowed"):
        validate_full_corpus_collection_params(
            models.CollectionParams(
                vectors=dense,
                sparse_vectors={
                    "sparse": models.SparseVectorParams(
                        index=models.SparseIndexParams(full_scan_threshold=1000)
                    )
                },
            ),
            384,
        )


@pytest.mark.parametrize(
    ("exists", "count", "schema_error", "record_exists", "state", "ready"),
    [
        (False, 0, None, False, "absent", True),
        (True, 0, None, False, "empty", True),
        (True, 1, None, False, "non_empty", False),
        (True, 0, "dense dimension mismatch", False, "empty", False),
        (False, 0, None, True, "absent", False),
    ],
)
def test_fresh_target_classification_is_fail_closed(
    exists: bool, count: int, schema_error: str | None,
    record_exists: bool, state: str, ready: bool,
) -> None:
    observation = classify_full_corpus_target(
        exists=exists,
        point_count=count,
        schema_error=schema_error,
        build_record_exists=record_exists,
    )
    assert observation.state == state
    if ready:
        assert require_fresh_full_corpus_target(observation) == state
    else:
        with pytest.raises(QdrantSchemaError):
            require_fresh_full_corpus_target(observation)


import numpy as np

from core.schema import EvidencePart, FullCorpusChunk
from embedding.sparse import build_vocabulary_index, fit_sparse_state
from vectorstore.points import (
    build_full_corpus_point_batch,
    validate_full_corpus_point_inputs,
)
from vectorstore.upsert import (
    compare_full_corpus_records,
    validate_sample_vectors,
)


def sample_chunk(chunk_id: str = "foods/test.md#0") -> FullCorpusChunk:
    return FullCorpusChunk(
        chunk_id=chunk_id,
        source="foods/test.md",
        title="Món Huế",
        heading_path=["Tóm tắt"],
        evidence_parts=[EvidencePart(role="body", start=0, end=7, text="Bún bò")],
        search_text="Món Huế\nTóm tắt\nBún bò",
    )


def test_full_corpus_point_batch_has_exact_vectors_payload_and_id() -> None:
    chunk = sample_chunk()
    state = fit_sparse_state([chunk])
    index = build_vocabulary_index(state)
    matrix = np.asarray([[1.0, 0.0]], dtype=np.float32)
    validate_full_corpus_point_inputs([chunk], matrix, 2, state, index)
    points = build_full_corpus_point_batch(
        [chunk], matrix, state, index,
    )
    assert len(points) == 1
    point = points[0]
    assert str(point.id) == chunk.point_id
    assert set(point.vector) == {"dense", "sparse"}
    assert point.vector["dense"] == [1.0, 0.0]
    assert isinstance(point.vector["sparse"], models.SparseVector)
    assert point.payload == chunk.to_qdrant_payload()
    assert set(point.payload) == {
        "search_text", "source", "title", "heading_path", "evidence_parts",
        "chunk_id", "domain",
    }


def test_full_corpus_point_inputs_validation_rejects_invalid_chunk_identity() -> None:
    state = fit_sparse_state([sample_chunk()])
    index = build_vocabulary_index(state)
    matrix = np.asarray([[1.0, 0.0]], dtype=np.float32)

    # Wrong source prefix
    chunk_bad_prefix = sample_chunk("wrong/path.md#0")
    with pytest.raises(ValueError):
        validate_full_corpus_point_inputs([chunk_bad_prefix], matrix, 2, state, index)

    # Missing #
    chunk_missing_hash = sample_chunk("foods/test.md")
    with pytest.raises(ValueError):
        validate_full_corpus_point_inputs([chunk_missing_hash], matrix, 2, state, index)

    # Negative ordinal
    chunk_neg = sample_chunk("foods/test.md#-1")
    with pytest.raises(ValueError):
        validate_full_corpus_point_inputs([chunk_neg], matrix, 2, state, index)

    # Non-canonical decimal (leading zero)
    chunk_nondecimal = sample_chunk("foods/test.md#01")
    with pytest.raises(ValueError):
        validate_full_corpus_point_inputs([chunk_nondecimal], matrix, 2, state, index)

    # Wrong point UUID
    class TamperedChunk(FullCorpusChunk):
        @property
        def point_id(self) -> str:
            return "00000000-0000-0000-0000-000000000000"

    tampered = TamperedChunk(
        chunk_id="foods/test.md#0",
        source="foods/test.md",
        title="Món Huế",
        heading_path=["Tóm tắt"],
        evidence_parts=[EvidencePart(role="body", start=0, end=7, text="Bún bò")],
        search_text="Món Huế\nTóm tắt\nBún bò",
    )
    with pytest.raises(ValueError, match="[Pp]oint ID"):
        validate_full_corpus_point_inputs([tampered], matrix, 2, state, index)


def test_full_corpus_point_batch_rejects_more_than_64() -> None:
    chunks = [sample_chunk(f"foods/test.md#{index}") for index in range(65)]
    state = fit_sparse_state(chunks)
    with pytest.raises(ValueError, match="64"):
        build_full_corpus_point_batch(
            chunks, np.tile([[1.0, 0.0]], (65, 1)),
            state, build_vocabulary_index(state),
        )


def test_record_and_sample_vector_validation_is_exact() -> None:
    chunk = sample_chunk()
    record = models.Record(id=chunk.point_id, payload=chunk.to_qdrant_payload())
    seen = compare_full_corpus_records(
        [record], {chunk.point_id: chunk.to_qdrant_payload()}
    )
    assert seen == {chunk.point_id}
    vector_record = models.Record(
        id=chunk.point_id,
        vector={
            "dense": [1.0, 0.0],
            "sparse": models.SparseVector(indices=[1, 3], values=[0.5, 1.25]),
        },
    )
    validate_sample_vectors([vector_record], 2, {chunk.point_id})
    with pytest.raises(ValueError, match="payload mismatch"):
        compare_full_corpus_records(
            [models.Record(id=chunk.point_id, payload={})],
            {chunk.point_id: chunk.to_qdrant_payload()},
        )


from ingestion.full_corpus_pipeline import (
    FULL_CORPUS_CANDIDATES,
    candidate_by_id,
)


def test_full_corpus_candidate_registry_is_exact_ordered_and_isolated() -> None:
    assert [
        (item.candidate_id, item.collection_name, item.dense_spec.dimension, item.dense_spec.provider)
        for item in FULL_CORPUS_CANDIDATES
    ] == [
        ("e5-small-384", "hue_full_corpus_7a2_e5_small_384", 384, "local"),
        ("qwen3-embedding-8b-4096", "hue_full_corpus_7a2_qwen3_8b_4096", 4096, "openrouter"),
    ]
    assert candidate_by_id("e5-small-384") is FULL_CORPUS_CANDIDATES[0]
    with pytest.raises(ValueError, match="Unknown full-corpus candidate"):
        candidate_by_id("arbitrary-model")


def test_build_writes_nothing_before_the_target_is_known_fresh(tmp_path: Path) -> None:
    """C-21: build dừng ở bước kiểm đích (collection runtime đã có point) **trước** khi ghi sparse state — trước đây sparse state được
    ghi rồi mới dừng, xóa thiếu một thứ là runtime hỏng. Chỉ đọc Qdrant (dừng trước create_collection), không nạp model dense."""
    from core.settings_loader import load_settings
    from ingestion.full_corpus_pipeline import build_candidate
    from vectorstore.qdrant import QdrantSchemaError, client_from_settings

    runtime = candidate_by_id("e5-small-384")
    client = client_from_settings(load_settings())
    try:
        assert client.collection_exists(runtime.collection_name), "Qdrant :6335 phải chạy và có collection runtime (điều kiện trước)"
    finally:
        client.close()
    sparse_state_path = tmp_path / "sparse_state.json"
    # Đích runtime có point ⇒ bước kiểm đích dừng với blocker "target is non-empty" (QdrantSchemaError) — đúng lý do, không phải lỗi khác.
    with pytest.raises(QdrantSchemaError, match="target is non-empty"):
        build_candidate(
            "e5-small-384",
            collection_name=runtime.collection_name,
            sparse_state_path=sparse_state_path,
            record_path=tmp_path / "record.json",
        )
    assert not sparse_state_path.exists()
