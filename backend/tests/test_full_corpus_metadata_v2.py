"""Unit tests for Full-corpus Metadata v2 migration primitives and verification."""
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Sequence
import pytest
from qdrant_client import models

from backend.core.schema import EvidencePart, FullCorpusChunk, point_id_for_chunk_id
from backend.embedding.sparse import fit_sparse_state, load_sparse_state, serialize_sparse_state
from backend.ingestion.full_corpus_pipeline import SPARSE_STATE_PATH, PreparedFullCorpus
from backend.ingestion.source_state import (
    FULL_CORPUS_BUILD_SCHEMA_V2,
    FULL_CORPUS_PAYLOAD_SCHEMA_V2,
    make_full_corpus_metadata_v2_build_record,
    write_final_full_corpus_build_record,
)
from backend.ingestion.full_corpus_metadata_v2 import (
    LEGACY_PAYLOAD_FIELDS,
    MIGRATION_BATCH_SIZE,
    MigrationPair,
    assert_migrated_record_equal,
    build_migrated_point,
    get_migration_pair,
    get_migration_pairs,
    main,
    run_migration,
    run_preflight,
    run_verify,
    validate_candidate_confirmation,
    validate_legacy_payload,
    validate_named_vectors,
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


def sample_legacy_payload() -> dict[str, object]:
    chunk = sample_chunk()
    return {
        "search_text": chunk.search_text,
        "source": chunk.source,
        "title": chunk.title,
        "heading_path": chunk.heading_path,
        "evidence_parts": [part.to_dict() for part in chunk.evidence_parts],
    }


def sample_source_record(
    point_id: str | None = None,
    dense: list[float] | None = None,
    sparse_indices: list[int] | None = None,
    sparse_values: list[float] | None = None,
    payload: dict[str, object] | None = None,
) -> models.Record:
    chunk = sample_chunk()
    pid = point_id if point_id is not None else chunk.point_id
    d = dense if dense is not None else [1.0, 0.5]
    s_idx = sparse_indices if sparse_indices is not None else [0, 2]
    s_val = sparse_values if sparse_values is not None else [0.25, 0.75]
    p = payload if payload is not None else sample_legacy_payload()
    return models.Record(
        id=pid,
        vector={
            "dense": d,
            "sparse": models.SparseVector(indices=s_idx, values=s_val),
        },
        payload=p,
    )


def test_build_migrated_point_preserves_vectors_and_replaces_payload():
    chunk = sample_chunk()
    source = sample_source_record()
    point = build_migrated_point(source, chunk, expected_dimension=2)

    assert str(point.id) == chunk.point_id
    assert point.vector["dense"] == [1.0, 0.5]
    assert isinstance(point.vector["sparse"], models.SparseVector)
    assert point.vector["sparse"].indices == [0, 2]
    assert point.vector["sparse"].values == [0.25, 0.75]
    assert point.payload == chunk.to_qdrant_payload()
    assert set(point.payload) == {
        "search_text", "source", "title", "heading_path", "evidence_parts",
        "chunk_id", "domain",
    }


def test_legacy_reader_rejects_seven_fields_or_wrong_vectors():
    pid = sample_chunk().point_id

    # 1. 7-field payload rejected by legacy validator
    v2_payload = sample_chunk().to_qdrant_payload()
    with pytest.raises(ValueError, match="Legacy payload"):
        validate_legacy_payload(pid, v2_payload)

    # 2. Missing field rejected
    missing_field = sample_legacy_payload()
    del missing_field["title"]
    with pytest.raises(ValueError, match="Legacy payload"):
        validate_legacy_payload(pid, missing_field)

    # 3. Extra field rejected
    extra_field = sample_legacy_payload()
    extra_field["extra"] = 123
    with pytest.raises(ValueError, match="Legacy payload"):
        validate_legacy_payload(pid, extra_field)

    # 4. Vector missing dense or sparse
    with pytest.raises(ValueError, match="named vectors"):
        validate_named_vectors(pid, {"dense": [1.0, 0.5]}, 2)
    with pytest.raises(ValueError, match="named vectors"):
        validate_named_vectors(pid, {"sparse": models.SparseVector(indices=[0], values=[1.0])}, 2)

    # 5. Dense dimension mismatch
    with pytest.raises(ValueError, match="dimension"):
        validate_named_vectors(
            pid,
            {"dense": [1.0, 0.5, 0.0], "sparse": models.SparseVector(indices=[0], values=[1.0])},
            2,
        )

    # 6. Dense non-finite
    with pytest.raises(ValueError, match="non-finite"):
        validate_named_vectors(
            pid,
            {"dense": [1.0, float("nan")], "sparse": models.SparseVector(indices=[0], values=[1.0])},
            2,
        )

    # 7. Sparse length mismatch
    with pytest.raises(ValueError, match="Sparse"):
        validate_named_vectors(
            pid,
            {"dense": [1.0, 0.5], "sparse": models.SparseVector(indices=[0, 1], values=[1.0])},
            2,
        )

    # 8. Sparse indices not strictly sorted/unique
    with pytest.raises(ValueError, match="Sparse"):
        validate_named_vectors(
            pid,
            {"dense": [1.0, 0.5], "sparse": models.SparseVector(indices=[2, 0], values=[1.0, 2.0])},
            2,
        )
    with pytest.raises(ValueError, match="Sparse"):
        validate_named_vectors(
            pid,
            {"dense": [1.0, 0.5], "sparse": models.SparseVector(indices=[1, 1], values=[1.0, 2.0])},
            2,
        )

    # 9. Sparse non-finite value
    with pytest.raises(ValueError, match="non-finite"):
        validate_named_vectors(
            pid,
            {"dense": [1.0, 0.5], "sparse": models.SparseVector(indices=[0], values=[float("inf")])},
            2,
        )


def test_build_migrated_point_rejects_point_id_or_dimension_mismatch():
    chunk = sample_chunk()
    mismatched_id_source = sample_source_record(point_id="00000000-0000-0000-0000-000000000000")
    with pytest.raises(ValueError, match="point ID mismatch"):
        build_migrated_point(mismatched_id_source, chunk, expected_dimension=2)

    valid_source = sample_source_record()
    with pytest.raises(ValueError, match="dimension"):
        build_migrated_point(valid_source, chunk, expected_dimension=3)


def test_migrated_comparison_rejects_one_dense_value_change():
    source = sample_source_record()
    target_dense = list(source.vector["dense"])
    target_dense[0] += 0.0001
    target = models.Record(
        id=source.id,
        vector={"dense": target_dense, "sparse": source.vector["sparse"]},
        payload=sample_chunk().to_qdrant_payload(),
    )
    with pytest.raises(ValueError, match="Dense vector mismatch"):
        assert_migrated_record_equal(source, target, sample_chunk().to_qdrant_payload(), 2)


def test_migrated_comparison_rejects_sparse_index_or_value_change():
    source = sample_source_record()

    # Index change
    target_bad_idx = models.Record(
        id=source.id,
        vector={
            "dense": source.vector["dense"],
            "sparse": models.SparseVector(indices=[0, 3], values=[0.25, 0.75]),
        },
        payload=sample_chunk().to_qdrant_payload(),
    )
    with pytest.raises(ValueError, match="Sparse vector mismatch"):
        assert_migrated_record_equal(source, target_bad_idx, sample_chunk().to_qdrant_payload(), 2)

    # Value change
    target_bad_val = models.Record(
        id=source.id,
        vector={
            "dense": source.vector["dense"],
            "sparse": models.SparseVector(indices=[0, 2], values=[0.25, 0.7501]),
        },
        payload=sample_chunk().to_qdrant_payload(),
    )
    with pytest.raises(ValueError, match="Sparse vector mismatch"):
        assert_migrated_record_equal(source, target_bad_val, sample_chunk().to_qdrant_payload(), 2)


def test_migrated_comparison_rejects_payload_or_id_change():
    source = sample_source_record()

    # ID change
    target_bad_id = models.Record(
        id="11111111-1111-1111-1111-111111111111",
        vector=source.vector,
        payload=sample_chunk().to_qdrant_payload(),
    )
    with pytest.raises(ValueError, match="Point ID mismatch"):
        assert_migrated_record_equal(source, target_bad_id, sample_chunk().to_qdrant_payload(), 2)

    # Payload change
    altered_payload = sample_chunk().to_qdrant_payload()
    altered_payload["title"] = "Tiêu đề khác"
    target_bad_payload = models.Record(
        id=source.id,
        vector=source.vector,
        payload=altered_payload,
    )
    with pytest.raises(ValueError, match="Payload mismatch"):
        assert_migrated_record_equal(source, target_bad_payload, sample_chunk().to_qdrant_payload(), 2)


def test_candidate_confirmation_rejects_arbitrary_target():
    # Valid confirmation succeeds
    pair = validate_candidate_confirmation("e5-small-384", "hue_full_corpus_a_e5_small_384_metadata_v2")
    assert pair.candidate_id == "e5-small-384"
    assert pair.target_collection == "hue_full_corpus_a_e5_small_384_metadata_v2"

    # Arbitrary target rejected
    with pytest.raises(ValueError, match="exact target confirmation"):
        validate_candidate_confirmation("e5-small-384", "arbitrary_target_name")

    # Mismatched target from another candidate rejected
    with pytest.raises(ValueError, match="exact target confirmation"):
        validate_candidate_confirmation("e5-small-384", "hue_full_corpus_a_e5_base_768_metadata_v2")

    # Unknown candidate rejected
    with pytest.raises(ValueError, match="Unknown candidate"):
        validate_candidate_confirmation("unknown-candidate", "hue_full_corpus_a_e5_small_384_metadata_v2")


def test_migration_pairs_ordering_and_isolation():
    pairs = get_migration_pairs()
    assert len(pairs) == 4
    assert [p.candidate_id for p in pairs] == [
        "e5-small-384", "e5-base-768", "huydang-dek21-768", "qwen3-embedding-0.6b-1024"
    ]
    for p in pairs:
        assert p.source_collection != p.target_collection
        assert p.target_collection.endswith("_metadata_v2")


def make_mock_prepared_corpus(chunks: list[FullCorpusChunk] | None = None) -> PreparedFullCorpus:
    if chunks is None:
        chunks = [
            FullCorpusChunk(
                chunk_id="foods/test1.md#0",
                source="foods/test1.md",
                title="Món Huế 1",
                heading_path=["Tóm tắt 1"],
                evidence_parts=[EvidencePart(role="body", start=0, end=7, text="Bún bò")],
                search_text="Món Huế 1\nTóm tắt 1\nBún bò",
            ),
            FullCorpusChunk(
                chunk_id="foods/test2.md#0",
                source="foods/test2.md",
                title="Món Huế 2",
                heading_path=["Tóm tắt 2"],
                evidence_parts=[EvidencePart(role="body", start=0, end=8, text="Cơm hến")],
                search_text="Món Huế 2\nTóm tắt 2\nCơm hến",
            ),
        ]
    sources = {
        chunk.source: hashlib.sha256(chunk.search_text.encode("utf-8")).hexdigest()
        for chunk in chunks
    }
    # Pad to 205 sources required by make_full_corpus_build_record
    for i in range(len(sources), 205):
        sources[f"dummy/file_{i}.md"] = "0" * 64

    sparse_state = load_sparse_state(SPARSE_STATE_PATH)
    sparse_state_bytes = SPARSE_STATE_PATH.read_bytes()
    sparse_state_sha = hashlib.sha256(sparse_state_bytes).hexdigest()

    source_state_bytes = json.dumps(
        sources, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    source_state_sha = hashlib.sha256(source_state_bytes).hexdigest()
    sample_chunk_ids = tuple(c.chunk_id for c in chunks)
    return PreparedFullCorpus(
        chunks=chunks,
        sources=sources,
        source_state_sha256=source_state_sha,
        sparse_state=sparse_state,
        sparse_state_sha256=sparse_state_sha,
        sample_chunk_ids=sample_chunk_ids,
    )


def make_mock_v1_source_record(
    pair: MigrationPair,
    prepared: PreparedFullCorpus,
    point_count: int | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "phase_4_full_corpus_build:v1",
        "status": "complete",
        "collection_name": pair.source_collection,
        "representation": "A",
        "corpus": {
            "identity": prepared.sparse_state.corpus_identity,
            "file_count": len(prepared.sources),
            "chunk_count": len(prepared.chunks),
            "sources": dict(prepared.sources),
        },
        "dense": {
            "candidate_id": pair.candidate_id,
            "dimension": pair.dimension,
            "model_id": pair.model_id,
            "revision": pair.revision,
        },
        "sparse": {
            "schema_version": prepared.sparse_state.schema_version,
            "state_sha256": prepared.sparse_state_sha256,
            "vocabulary_size": len(prepared.sparse_state.vocabulary),
        },
        "qdrant": {
            "dense_vector_name": "dense",
            "sparse_vector_name": "sparse",
            "distance": "cosine",
            "point_count": point_count if point_count is not None else len(prepared.chunks),
        },
    }


def make_mock_source_points(
    chunks: Sequence[FullCorpusChunk],
    dimension: int = 384,
) -> list[models.Record]:
    points = []
    for i, chunk in enumerate(chunks):
        dense = [0.1 * ((j % 10) + 1) for j in range(dimension)]
        points.append(
            models.Record(
                id=chunk.point_id,
                vector={
                    "dense": dense,
                    "sparse": models.SparseVector(indices=[i, i + 1], values=[0.5, 0.8]),
                },
                payload={
                    "search_text": chunk.search_text,
                    "source": chunk.source,
                    "title": chunk.title,
                    "heading_path": list(chunk.heading_path),
                    "evidence_parts": [p.to_dict() for p in chunk.evidence_parts],
                },
            )
        )
    return points


class RecordingClient:
    def __init__(
        self,
        existing_collections=None,
        points_by_collection=None,
        collection_configs=None,
        payload_schemas=None,
    ):
        self.mutations: list[tuple[str, str, Any]] = []
        self.existing_collections = set(existing_collections or [])
        self.points_by_collection = dict(points_by_collection or {})
        self.collection_configs = dict(collection_configs or {})
        self.payload_schemas = dict(payload_schemas or {})

    def collection_exists(self, collection_name: str) -> bool:
        return collection_name in self.existing_collections

    def get_collection(self, collection_name: str):
        if collection_name not in self.existing_collections:
            raise ValueError(f"Collection {collection_name} does not exist")
        points = self.points_by_collection.get(collection_name, [])
        config = self.collection_configs.get(collection_name)
        payload_schema = self.payload_schemas.get(collection_name, {})
        dim = 384
        if "768" in collection_name:
            dim = 768
        elif "1024" in collection_name:
            dim = 1024

        from types import SimpleNamespace
        if config is not None:
            col_config = config
        else:
            params = SimpleNamespace(
                vectors={"dense": models.VectorParams(size=dim, distance=models.Distance.COSINE)},
                sparse_vectors={"sparse": models.SparseVectorParams()},
            )
            col_config = SimpleNamespace(params=params)

        return SimpleNamespace(
            status=models.CollectionStatus.GREEN,
            optimizer_status=models.OptimizersStatusOneOf.OK,
            vectors_count=len(points),
            indexed_vectors_count=0,
            points_count=len(points),
            segments_count=1,
            config=col_config,
            payload_schema=payload_schema,
        )

    def scroll(self, collection_name: str, limit: int = 64, offset=None, with_payload=True, with_vectors=True):
        all_points = self.points_by_collection.get(collection_name, [])
        start = int(offset) if offset is not None else 0
        end = start + limit
        page = all_points[start:end]
        next_offset = end if end < len(all_points) else None
        records = []
        for p in page:
            if isinstance(p, models.PointStruct):
                records.append(models.Record(id=p.id, vector=p.vector, payload=p.payload))
            elif isinstance(p, models.Record):
                records.append(p)
            else:
                records.append(p)
        return records, next_offset

    def retrieve(self, collection_name: str, ids: Sequence[Any], with_payload=True, with_vectors=True):
        points = self.points_by_collection.get(collection_name, [])
        by_id = {str(p.id): p for p in points}
        records = []
        for pid in ids:
            p = by_id.get(str(pid))
            if p is not None:
                if isinstance(p, models.PointStruct):
                    records.append(models.Record(id=p.id, vector=p.vector, payload=p.payload))
                else:
                    records.append(p)
        return records

    def create_collection(self, collection_name: str, **kwargs):
        self.mutations.append(("create_collection", collection_name, kwargs))
        self.existing_collections.add(collection_name)

    def upsert(self, collection_name: str, points, **kwargs):
        self.mutations.append(("upsert", collection_name, len(points)))
        self.points_by_collection.setdefault(collection_name, []).extend(points)


def test_cli_routing_and_no_mutation_guarantees(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    client = RecordingClient()

    # Preflight performs zero mutations and returns exact BLOCKED status
    evidence = run_preflight(client, [pair], prepared_corpus=prepared)
    assert client.mutations == []
    assert evidence["status"] == "BLOCKED"
    assert evidence["summary"]["total_mutations"] == 0

    # Verify performs zero mutations and returns exact FAILED status
    verify_evidence = run_verify(client, [pair], prepared_corpus=prepared)
    assert client.mutations == []
    assert verify_evidence["status"] == "FAILED"
    assert verify_evidence["summary"]["total_mutations"] == 0

    # Migration rejects invalid confirm_target with zero mutations
    with pytest.raises(ValueError, match="exact target confirmation"):
        run_migration(client, pair, confirm_target="wrong", prepared_corpus=prepared)
    assert client.mutations == []


def test_preflight_blocks_when_target_already_exists(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    # Target collection already exists in client
    client = RecordingClient(existing_collections=[pair.target_collection])
    evidence = run_preflight(client, [pair], prepared_corpus=prepared)
    assert evidence["status"] == "BLOCKED"
    assert any("already exists" in err for err in evidence["errors"])
    assert client.mutations == []


def test_preflight_artifact_sanitization(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    client = RecordingClient()
    evidence = run_preflight(client, [pair], prepared_corpus=prepared)

    # Convert to serialized string to audit contents
    text = json.dumps(evidence)
    for forbidden in (
        "knowledge-base-hue",
        "/home/",
        ".md#",
        "search_text",
        "evidence_parts",
        "heading_path",
    ):
        assert forbidden not in text


def test_cli_rejects_unknown_candidate_or_missing_confirmation():
    # Unknown candidate in preflight
    with pytest.raises(SystemExit):
        main(["preflight", "--candidate", "unknown-cand", "--output", "out.json"])

    # Migrate missing confirm-target
    with pytest.raises(SystemExit):
        main(["migrate", "--candidate", "e5-small-384"])


def test_cli_rejects_duplicate_candidate_selectors(tmp_path):
    out_file = tmp_path / "out.json"
    with pytest.raises(SystemExit) as exc_info:
        main(["preflight", "--candidate", "e5-small-384", "e5-small-384", "--output", str(out_file)])
    assert exc_info.value.code == 2

    with pytest.raises(SystemExit) as exc_info:
        main(["verify", "--candidate", "e5-small-384", "e5-small-384"])
    assert exc_info.value.code == 2


def test_functions_reject_duplicate_candidates():
    pair = get_migration_pair("e5-small-384")
    client = RecordingClient()
    with pytest.raises(ValueError, match="Duplicate candidate selector: e5-small-384"):
        run_preflight(client, [pair, pair])
    with pytest.raises(ValueError, match="Duplicate candidate selector: e5-small-384"):
        run_verify(client, [pair, pair])


# --- R1 Tests: Fail-closed and sanitized on preparation and dependency errors ---

def test_preflight_fails_closed_when_corpus_prep_raises_error(monkeypatch, tmp_path):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    client = RecordingClient()

    def mock_prepare_fail():
        raise RuntimeError("/home/private/corpus.md FAKE_SECRET_MARKER")

    monkeypatch.setattr(
        "backend.ingestion.full_corpus_metadata_v2.prepare_full_corpus_input",
        mock_prepare_fail,
    )

    result = run_preflight(client, [pair], prepared_corpus=None)

    assert result["status"] == "BLOCKED"
    assert result["summary"]["ready_pairs"] == 0
    assert result["summary"]["blocked_pairs"] == 1
    assert result["summary"]["total_mutations"] == 0
    assert any("Corpus preparation failed: RuntimeError" in err for err in result["errors"])
    assert "FAKE_SECRET_MARKER" not in str(result)
    assert "/home/private" not in str(result)
    assert client.mutations == []

    cand = result["candidates"][0]
    assert cand["status"] == "BLOCKED"
    assert cand["source_points_count"] == 0
    assert cand["corpus_identity"] == ""
    assert cand["sparse_state_sha256"] == ""
    assert cand["source_build_record_sha256"] == ""


def test_preflight_cli_exits_nonzero_when_prep_fails(monkeypatch, tmp_path):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)

    def mock_prepare_fail():
        raise RuntimeError("/home/private/corpus.md FAKE_SECRET_MARKER")

    monkeypatch.setattr(
        "backend.ingestion.full_corpus_metadata_v2.prepare_full_corpus_input",
        mock_prepare_fail,
    )
    monkeypatch.setattr(
        "backend.ingestion.full_corpus_metadata_v2.client_from_settings",
        lambda _: RecordingClient(),
    )

    out_file = tmp_path / "preflight_fail.json"
    exit_code = main(["preflight", "--candidate", "e5-small-384", "--output", str(out_file)])
    assert exit_code == 1

    assert out_file.exists()
    payload = json.loads(out_file.read_text(encoding="utf-8"))
    assert payload["status"] == "BLOCKED"
    assert any("Corpus preparation failed: RuntimeError" in err for err in payload["errors"])
    assert "FAKE_SECRET_MARKER" not in str(payload)
    assert "/home/private" not in str(payload)


def test_preflight_fails_closed_on_dependency_inspection_errors(monkeypatch, tmp_path):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_record = make_mock_v1_source_record(pair, prepared)
    record_file = tmp_path / f"{pair.source_collection}.json"
    record_file.write_text(json.dumps(source_record), encoding="utf-8")

    # 1. Target collection_exists error
    class TargetExistsErrorClient(RecordingClient):
        def collection_exists(self, collection_name: str) -> bool:
            if collection_name == pair.target_collection:
                raise RuntimeError("Connection dropped on target /home/secret")
            return super().collection_exists(collection_name)

    res1 = run_preflight(TargetExistsErrorClient(), [pair], prepared_corpus=prepared)
    assert res1["status"] == "BLOCKED"
    assert any("Failed inspecting target collection: RuntimeError" in err for err in res1["errors"])
    assert "/home/secret" not in str(res1)
    assert res1["summary"]["total_mutations"] == 0

    # 2. Source collection_exists error
    class SourceExistsErrorClient(RecordingClient):
        def collection_exists(self, collection_name: str) -> bool:
            if collection_name == pair.source_collection:
                raise RuntimeError("Connection dropped on source /home/secret")
            return super().collection_exists(collection_name)

    res2 = run_preflight(SourceExistsErrorClient(), [pair], prepared_corpus=prepared)
    assert res2["status"] == "BLOCKED"
    assert any("Failed inspecting source collection: RuntimeError" in err for err in res2["errors"])
    assert "/home/secret" not in str(res2)
    assert res2["summary"]["total_mutations"] == 0

    # 3. get_collection error
    class GetCollectionErrorClient(RecordingClient):
        def __init__(self):
            super().__init__(existing_collections=[pair.source_collection])

        def get_collection(self, collection_name: str):
            raise RuntimeError("Corrupted collection metadata /home/secret")

    res3 = run_preflight(GetCollectionErrorClient(), [pair], prepared_corpus=prepared)
    assert res3["status"] == "BLOCKED"
    assert any("Failed inspecting source collection: RuntimeError" in err for err in res3["errors"])
    assert "/home/secret" not in str(res3)
    assert res3["summary"]["total_mutations"] == 0

    # 4. scroll error
    class ScrollErrorClient(RecordingClient):
        def __init__(self):
            super().__init__(existing_collections=[pair.source_collection])

        def scroll(self, collection_name: str, **kwargs):
            raise RuntimeError("Scroll timeout /home/secret")

    res4 = run_preflight(ScrollErrorClient(), [pair], prepared_corpus=prepared)
    assert res4["status"] == "BLOCKED"
    assert any("Failed scrolling source collection: RuntimeError" in err for err in res4["errors"])
    assert "/home/secret" not in str(res4)
    assert res4["summary"]["total_mutations"] == 0


# --- R2 Tests: Legacy build record and payload validation ---

def test_preflight_happy_path_mock(monkeypatch, tmp_path):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_record = make_mock_v1_source_record(pair, prepared)
    record_file = tmp_path / f"{pair.source_collection}.json"
    record_file.write_text(json.dumps(source_record), encoding="utf-8")

    source_points = make_mock_source_points(prepared.chunks, pair.dimension)
    client = RecordingClient(
        existing_collections=[pair.source_collection],
        points_by_collection={pair.source_collection: source_points},
    )

    result = run_preflight(client, [pair], prepared_corpus=prepared)
    assert result["status"] == "READY"
    assert result["errors"] == []
    assert result["summary"]["ready_pairs"] == 1
    assert result["summary"]["blocked_pairs"] == 0

    cand = result["candidates"][0]
    assert cand["status"] == "READY"
    assert cand["source_points_count"] == 2
    assert cand["corpus_identity"] == prepared.sparse_state.corpus_identity
    assert cand["sparse_state_sha256"] == prepared.sparse_state_sha256
    assert cand["target_collection_absent"] is True
    assert cand["target_build_record_absent"] is True


@pytest.mark.parametrize(
    "mutator,expected_err",
    [
        (lambda r: r.update({"collection_name": "wrong_col"}), "collection_name mismatch"),
        (lambda r: r.update({"representation": "B"}), "representation mismatch"),
        (lambda r: r.update({"schema_version": "v2"}), "schema version is not v1"),
        (lambda r: r.update({"status": "failed"}), "status is not complete"),
        (lambda r: r["dense"].update({"candidate_id": "other-cand"}), "candidate_id mismatch"),
        (lambda r: r["dense"].update({"dimension": 999}), "dimension mismatch"),
        (lambda r: r["dense"].update({"model_id": "wrong-model"}), "model_id mismatch"),
        (lambda r: r["dense"].update({"revision": "wrong-rev"}), "revision mismatch"),
        (lambda r: r["corpus"].update({"identity": "wrong-identity"}), "corpus identity mismatch"),
        (lambda r: r["corpus"].update({"file_count": 999}), "corpus file_count"),
        (lambda r: r["corpus"].update({"chunk_count": 999}), "corpus chunk_count"),
        (lambda r: r["sparse"].update({"schema_version": "wrong-sparse-schema"}), "sparse schema_version mismatch"),
        (lambda r: r["sparse"].update({"state_sha256": "wrong-hash"}), "sparse state_sha256 mismatch"),
        (lambda r: r["sparse"].update({"vocabulary_size": 9999}), "sparse vocabulary_size mismatch"),
        (lambda r: r["qdrant"].update({"dense_vector_name": "wrong_dense"}), "dense_vector_name is not 'dense'"),
        (lambda r: r["qdrant"].update({"sparse_vector_name": "wrong_sparse"}), "sparse_vector_name is not 'sparse'"),
        (lambda r: r["qdrant"].update({"distance": "dot"}), "distance is not 'cosine'"),
        (lambda r: r["qdrant"].update({"point_count": 999}), "point_count mismatch"),
    ],
)
def test_preflight_fails_on_build_record_field_mismatches(tmp_path, monkeypatch, mutator, expected_err):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_record = make_mock_v1_source_record(pair, prepared)
    mutator(source_record)
    record_file = tmp_path / f"{pair.source_collection}.json"
    record_file.write_text(json.dumps(source_record), encoding="utf-8")

    source_points = make_mock_source_points(prepared.chunks, pair.dimension)
    client = RecordingClient(
        existing_collections=[pair.source_collection],
        points_by_collection={pair.source_collection: source_points},
    )

    result = run_preflight(client, [pair], prepared_corpus=prepared)
    assert result["status"] == "BLOCKED"
    assert any(expected_err in err for err in result["errors"])
    cand = result["candidates"][0]
    assert cand["status"] == "BLOCKED"
    assert cand["source_points_count"] == 0
    assert cand["corpus_identity"] == ""
    assert cand["sparse_state_sha256"] == ""


def test_preflight_fails_on_stale_source_state(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_record = make_mock_v1_source_record(pair, prepared)
    # Stale hash for one file
    first_file = next(iter(source_record["corpus"]["sources"]))
    source_record["corpus"]["sources"][first_file] = "0000000000000000000000000000000000000000000000000000000000000000"
    record_file = tmp_path / f"{pair.source_collection}.json"
    record_file.write_text(json.dumps(source_record), encoding="utf-8")

    source_points = make_mock_source_points(prepared.chunks, pair.dimension)
    client = RecordingClient(
        existing_collections=[pair.source_collection],
        points_by_collection={pair.source_collection: source_points},
    )

    result = run_preflight(client, [pair], prepared_corpus=prepared)
    assert result["status"] == "BLOCKED"
    assert any("freshness mismatch" in err for err in result["errors"])


@pytest.mark.parametrize(
    "tamper_key,tamper_val",
    [
        ("search_text", "tampered search text"),
        ("source", "foods/tampered.md"),
        ("title", "Tampered Title"),
        ("heading_path", ["Tampered Heading"]),
        ("evidence_parts", [{"role": "body", "start": 0, "end": 4, "text": "test"}]),
    ],
)
def test_preflight_fails_on_legacy_payload_value_mismatch(tmp_path, monkeypatch, tamper_key, tamper_val):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_record = make_mock_v1_source_record(pair, prepared)
    record_file = tmp_path / f"{pair.source_collection}.json"
    record_file.write_text(json.dumps(source_record), encoding="utf-8")

    source_points = make_mock_source_points(prepared.chunks, pair.dimension)
    # Tamper payload of first point
    source_points[0].payload[tamper_key] = tamper_val

    client = RecordingClient(
        existing_collections=[pair.source_collection],
        points_by_collection={pair.source_collection: source_points},
    )

    result = run_preflight(client, [pair], prepared_corpus=prepared)
    assert result["status"] == "BLOCKED"
    assert any("Legacy payload" in err for err in result["errors"])


def test_preflight_fails_on_duplicate_foreign_or_missing_point_id(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_record = make_mock_v1_source_record(pair, prepared)
    record_file = tmp_path / f"{pair.source_collection}.json"
    record_file.write_text(json.dumps(source_record), encoding="utf-8")

    # 1. Duplicate point ID
    source_points = make_mock_source_points(prepared.chunks, pair.dimension)
    dup_point = models.Record(
        id=source_points[0].id,
        vector=source_points[0].vector,
        payload=source_points[0].payload,
    )
    client_dup = RecordingClient(
        existing_collections=[pair.source_collection],
        points_by_collection={pair.source_collection: [source_points[0], dup_point]},
    )
    res_dup = run_preflight(client_dup, [pair], prepared_corpus=prepared)
    assert res_dup["status"] == "BLOCKED"
    assert any("Duplicate point ID" in err for err in res_dup["errors"])

    # 2. Foreign point ID
    foreign_point = models.Record(
        id="00000000-0000-0000-0000-000000000000",
        vector=source_points[0].vector,
        payload=source_points[0].payload,
    )
    client_foreign = RecordingClient(
        existing_collections=[pair.source_collection],
        points_by_collection={pair.source_collection: [source_points[0], foreign_point]},
    )
    res_foreign = run_preflight(client_foreign, [pair], prepared_corpus=prepared)
    assert res_foreign["status"] == "BLOCKED"
    assert any("Foreign point ID" in err for err in res_foreign["errors"])

    # 3. Missing point (only 1 point out of 2)
    client_missing = RecordingClient(
        existing_collections=[pair.source_collection],
        points_by_collection={pair.source_collection: [source_points[0]]},
    )
    res_missing = run_preflight(client_missing, [pair], prepared_corpus=prepared)
    assert res_missing["status"] == "BLOCKED"
    assert any("points count" in err for err in res_missing["errors"])


# --- R3 Tests: Migration safety and record write gating ---

def test_migration_happy_path(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_record = make_mock_v1_source_record(pair, prepared)
    record_file = tmp_path / f"{pair.source_collection}.json"
    record_file.write_text(json.dumps(source_record), encoding="utf-8")

    source_points = make_mock_source_points(prepared.chunks, pair.dimension)
    client = RecordingClient(
        existing_collections=[pair.source_collection],
        points_by_collection={pair.source_collection: source_points},
    )

    res = run_migration(client, pair, confirm_target=pair.target_collection, prepared_corpus=prepared)
    assert res["status"] == "MIGRATED"
    assert res["upserted_points"] == len(prepared.chunks)

    target_record_path = tmp_path / f"{pair.target_collection}.json"
    assert target_record_path.exists()
    record_data = json.loads(target_record_path.read_text(encoding="utf-8"))
    assert record_data["status"] == "complete"
    assert record_data["schema_version"] == FULL_CORPUS_BUILD_SCHEMA_V2

    # Check mutations
    mutation_types = [m[0] for m in client.mutations]
    assert "create_collection" in mutation_types
    assert "upsert" in mutation_types


def test_migration_aborts_without_writing_record_when_target_verification_fails(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_record = make_mock_v1_source_record(pair, prepared)
    record_file = tmp_path / f"{pair.source_collection}.json"
    record_file.write_text(json.dumps(source_record), encoding="utf-8")

    source_points = make_mock_source_points(prepared.chunks, pair.dimension)

    class CorruptingUpsertClient(RecordingClient):
        def upsert(self, collection_name: str, points, **kwargs):
            # Corrupt vector of first point
            corrupted = []
            for p in points:
                bad_dense = list(p.vector["dense"])
                bad_dense[0] += 0.5
                corrupted.append(
                    models.PointStruct(id=p.id, vector={"dense": bad_dense, "sparse": p.vector["sparse"]}, payload=p.payload)
                )
            super().upsert(collection_name, corrupted, **kwargs)

    client = CorruptingUpsertClient(
        existing_collections=[pair.source_collection],
        points_by_collection={pair.source_collection: source_points},
    )

    with pytest.raises(RuntimeError, match="Post-migration target verification failed"):
        run_migration(client, pair, confirm_target=pair.target_collection, prepared_corpus=prepared)

    target_record_path = tmp_path / f"{pair.target_collection}.json"
    # Build record must NEVER be written
    assert not target_record_path.exists()
    # Partial target collection must remain intact for diagnosis
    assert client.collection_exists(pair.target_collection)


def test_migration_fails_when_source_record_modified_after_preflight(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_record = make_mock_v1_source_record(pair, prepared)
    record_file = tmp_path / f"{pair.source_collection}.json"
    record_file.write_text(json.dumps(source_record), encoding="utf-8")

    source_points = make_mock_source_points(prepared.chunks, pair.dimension)

    class TamperingUpsertClient(RecordingClient):
        def upsert(self, collection_name: str, points, **kwargs):
            # Modify legacy source record bytes on disk during migration (after preflight)
            tampered = dict(source_record)
            tampered["corpus"]["identity"] = "tampered_identity_hash"
            record_file.write_text(json.dumps(tampered), encoding="utf-8")
            super().upsert(collection_name, points, **kwargs)

    client = TamperingUpsertClient(
        existing_collections=[pair.source_collection],
        points_by_collection={pair.source_collection: source_points},
    )

    with pytest.raises(RuntimeError, match="Legacy source build record SHA changed after preflight"):
        run_migration(client, pair, confirm_target=pair.target_collection, prepared_corpus=prepared)

    target_record_path = tmp_path / f"{pair.target_collection}.json"
    # Target build record must NEVER be written
    assert not target_record_path.exists()
    # Partial target collection must remain intact for diagnosis
    assert client.collection_exists(pair.target_collection)


def test_migration_fails_when_source_record_deleted_after_preflight(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_record = make_mock_v1_source_record(pair, prepared)
    record_file = tmp_path / f"{pair.source_collection}.json"
    record_file.write_text(json.dumps(source_record), encoding="utf-8")

    source_points = make_mock_source_points(prepared.chunks, pair.dimension)

    class DeletingUpsertClient(RecordingClient):
        def upsert(self, collection_name: str, points, **kwargs):
            # Delete legacy source record on disk during migration (after preflight)
            record_file.unlink()
            super().upsert(collection_name, points, **kwargs)

    client = DeletingUpsertClient(
        existing_collections=[pair.source_collection],
        points_by_collection={pair.source_collection: source_points},
    )

    with pytest.raises(RuntimeError, match="Failed reading legacy source build record before final write"):
        run_migration(client, pair, confirm_target=pair.target_collection, prepared_corpus=prepared)

    target_record_path = tmp_path / f"{pair.target_collection}.json"
    # Target build record must NEVER be written
    assert not target_record_path.exists()
    # Partial target collection must remain intact for diagnosis
    assert client.collection_exists(pair.target_collection)


# --- R4 Tests: Multi-page retrieval and complete target verification ---

def _write_legacy_source_record(tmp_path: Path, pair: MigrationPair, prepared: PreparedFullCorpus) -> str:
    source_record = make_mock_v1_source_record(pair, prepared)
    record_file = tmp_path / f"{pair.source_collection}.json"
    record_file.write_text(json.dumps(source_record), encoding="utf-8")
    return hashlib.sha256(record_file.read_bytes()).hexdigest()


def test_verify_multi_page_success(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.MIGRATION_BATCH_SIZE", 2)
    pair = get_migration_pair("e5-small-384")

    # 4 chunks
    chunks = [
        FullCorpusChunk(
            chunk_id=f"foods/test{i}.md#0",
            source=f"foods/test{i}.md",
            title=f"Món Huế {i}",
            heading_path=[f"Tóm tắt {i}"],
            evidence_parts=[EvidencePart(role="body", start=0, end=5, text=f"Item{i}")],
            search_text=f"Món Huế {i}\nTóm tắt {i}\nItem{i}",
        )
        for i in range(4)
    ]
    prepared = make_mock_prepared_corpus(chunks)
    source_points = make_mock_source_points(chunks, pair.dimension)

    # Migrated target points with 7 fields
    target_points = [
        models.Record(
            id=s.id,
            vector=s.vector,
            payload=chunks[i].to_qdrant_payload(),
        )
        for i, s in enumerate(source_points)
    ]

    # Write source legacy record and target build record with matching SHA-256
    source_sha = _write_legacy_source_record(tmp_path, pair, prepared)
    v2_record = make_full_corpus_metadata_v2_build_record(
        collection_name=pair.target_collection,
        source_collection=pair.source_collection,
        source_build_record_sha256=source_sha,
        candidate_id=pair.candidate_id,
        model_id=pair.model_id,
        revision=pair.revision,
        dimension=pair.dimension,
        corpus_identity=prepared.sparse_state.corpus_identity,
        sources=prepared.sources,
        sparse_state=prepared.sparse_state,
        sparse_state_sha256=prepared.sparse_state_sha256,
    )
    target_record_path = tmp_path / f"{pair.target_collection}.json"
    write_final_full_corpus_build_record(v2_record, target_record_path)

    client = RecordingClient(
        existing_collections=[pair.source_collection, pair.target_collection],
        points_by_collection={
            pair.source_collection: source_points,
            pair.target_collection: target_points,
        },
    )

    res = run_verify(client, [pair], prepared_corpus=prepared)
    assert res["status"] == "VERIFIED"
    assert res["errors"] == []
    assert res["summary"]["verified_pairs"] == 1
    assert res["candidates"][0]["verified_points_count"] == 4


def test_verify_detects_missing_point_in_target(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_points = make_mock_source_points(prepared.chunks, pair.dimension)

    # Target only has 1 point out of 2
    target_points = [
        models.Record(
            id=source_points[0].id,
            vector=source_points[0].vector,
            payload=prepared.chunks[0].to_qdrant_payload(),
        )
    ]

    source_sha = _write_legacy_source_record(tmp_path, pair, prepared)
    v2_record = make_full_corpus_metadata_v2_build_record(
        collection_name=pair.target_collection,
        source_collection=pair.source_collection,
        source_build_record_sha256=source_sha,
        candidate_id=pair.candidate_id,
        model_id=pair.model_id,
        revision=pair.revision,
        dimension=pair.dimension,
        corpus_identity=prepared.sparse_state.corpus_identity,
        sources=prepared.sources,
        sparse_state=prepared.sparse_state,
        sparse_state_sha256=prepared.sparse_state_sha256,
    )
    target_record_path = tmp_path / f"{pair.target_collection}.json"
    write_final_full_corpus_build_record(v2_record, target_record_path)

    client = RecordingClient(
        existing_collections=[pair.source_collection, pair.target_collection],
        points_by_collection={
            pair.source_collection: source_points,
            pair.target_collection: target_points,
        },
    )

    res = run_verify(client, [pair], prepared_corpus=prepared)
    assert res["status"] == "FAILED"
    assert any("missing from target" in err or "points count" in err for err in res["errors"])


def test_verify_detects_extra_points_or_count_mismatch(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_points = make_mock_source_points(prepared.chunks, pair.dimension)

    target_points = [
        models.Record(id=s.id, vector=s.vector, payload=prepared.chunks[i].to_qdrant_payload())
        for i, s in enumerate(source_points)
    ]
    # Add an extra point to target
    target_points.append(
        models.Record(
            id="00000000-0000-0000-0000-000000000000",
            vector=source_points[0].vector,
            payload=prepared.chunks[0].to_qdrant_payload(),
        )
    )

    source_sha = _write_legacy_source_record(tmp_path, pair, prepared)
    v2_record = make_full_corpus_metadata_v2_build_record(
        collection_name=pair.target_collection,
        source_collection=pair.source_collection,
        source_build_record_sha256=source_sha,
        candidate_id=pair.candidate_id,
        model_id=pair.model_id,
        revision=pair.revision,
        dimension=pair.dimension,
        corpus_identity=prepared.sparse_state.corpus_identity,
        sources=prepared.sources,
        sparse_state=prepared.sparse_state,
        sparse_state_sha256=prepared.sparse_state_sha256,
    )
    target_record_path = tmp_path / f"{pair.target_collection}.json"
    write_final_full_corpus_build_record(v2_record, target_record_path)

    client = RecordingClient(
        existing_collections=[pair.source_collection, pair.target_collection],
        points_by_collection={
            pair.source_collection: source_points,
            pair.target_collection: target_points,
        },
    )

    res = run_verify(client, [pair], prepared_corpus=prepared)
    assert res["status"] == "FAILED"
    assert any("points count" in err for err in res["errors"])


def test_verify_detects_invalid_target_payload_schema(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_points = make_mock_source_points(prepared.chunks, pair.dimension)
    target_points = [
        models.Record(id=s.id, vector=s.vector, payload=prepared.chunks[i].to_qdrant_payload())
        for i, s in enumerate(source_points)
    ]

    source_sha = _write_legacy_source_record(tmp_path, pair, prepared)
    v2_record = make_full_corpus_metadata_v2_build_record(
        collection_name=pair.target_collection,
        source_collection=pair.source_collection,
        source_build_record_sha256=source_sha,
        candidate_id=pair.candidate_id,
        model_id=pair.model_id,
        revision=pair.revision,
        dimension=pair.dimension,
        corpus_identity=prepared.sparse_state.corpus_identity,
        sources=prepared.sources,
        sparse_state=prepared.sparse_state,
        sparse_state_sha256=prepared.sparse_state_sha256,
    )
    target_record_path = tmp_path / f"{pair.target_collection}.json"
    write_final_full_corpus_build_record(v2_record, target_record_path)

    client = RecordingClient(
        existing_collections=[pair.source_collection, pair.target_collection],
        points_by_collection={
            pair.source_collection: source_points,
            pair.target_collection: target_points,
        },
        payload_schemas={pair.target_collection: {"domain": models.PayloadSchemaType.KEYWORD}},
    )

    res = run_verify(client, [pair], prepared_corpus=prepared)
    assert res["status"] == "FAILED"
    assert any("non-empty payload_schema" in err for err in res["errors"])


def test_verify_detects_vector_or_payload_mismatch(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_points = make_mock_source_points(prepared.chunks, pair.dimension)

    # Alter title in target payload
    altered_payload = prepared.chunks[0].to_qdrant_payload()
    altered_payload["title"] = "Món Huế Altered"
    target_points = [
        models.Record(id=source_points[0].id, vector=source_points[0].vector, payload=altered_payload),
        models.Record(id=source_points[1].id, vector=source_points[1].vector, payload=prepared.chunks[1].to_qdrant_payload()),
    ]

    source_sha = _write_legacy_source_record(tmp_path, pair, prepared)
    v2_record = make_full_corpus_metadata_v2_build_record(
        collection_name=pair.target_collection,
        source_collection=pair.source_collection,
        source_build_record_sha256=source_sha,
        candidate_id=pair.candidate_id,
        model_id=pair.model_id,
        revision=pair.revision,
        dimension=pair.dimension,
        corpus_identity=prepared.sparse_state.corpus_identity,
        sources=prepared.sources,
        sparse_state=prepared.sparse_state,
        sparse_state_sha256=prepared.sparse_state_sha256,
    )
    target_record_path = tmp_path / f"{pair.target_collection}.json"
    write_final_full_corpus_build_record(v2_record, target_record_path)

    client = RecordingClient(
        existing_collections=[pair.source_collection, pair.target_collection],
        points_by_collection={
            pair.source_collection: source_points,
            pair.target_collection: target_points,
        },
    )

    res = run_verify(client, [pair], prepared_corpus=prepared)
    assert res["status"] == "FAILED"
    assert any("Payload mismatch" in err for err in res["errors"])


def test_verify_fails_when_source_legacy_record_missing(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_points = make_mock_source_points(prepared.chunks, pair.dimension)
    target_points = [
        models.Record(id=s.id, vector=s.vector, payload=prepared.chunks[i].to_qdrant_payload())
        for i, s in enumerate(source_points)
    ]

    # Target build record exists, but legacy source record does NOT exist
    v2_record = make_full_corpus_metadata_v2_build_record(
        collection_name=pair.target_collection,
        source_collection=pair.source_collection,
        source_build_record_sha256="a" * 64,
        candidate_id=pair.candidate_id,
        model_id=pair.model_id,
        revision=pair.revision,
        dimension=pair.dimension,
        corpus_identity=prepared.sparse_state.corpus_identity,
        sources=prepared.sources,
        sparse_state=prepared.sparse_state,
        sparse_state_sha256=prepared.sparse_state_sha256,
    )
    target_record_path = tmp_path / f"{pair.target_collection}.json"
    write_final_full_corpus_build_record(v2_record, target_record_path)

    client = RecordingClient(
        existing_collections=[pair.source_collection, pair.target_collection],
        points_by_collection={
            pair.source_collection: source_points,
            pair.target_collection: target_points,
        },
    )

    res = run_verify(client, [pair], prepared_corpus=prepared)
    assert res["status"] == "FAILED"
    assert any("does not exist for lineage check" in err for err in res["errors"])


def test_verify_fails_when_source_legacy_record_sha_mismatch(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_points = make_mock_source_points(prepared.chunks, pair.dimension)
    target_points = [
        models.Record(id=s.id, vector=s.vector, payload=prepared.chunks[i].to_qdrant_payload())
        for i, s in enumerate(source_points)
    ]

    # Write legacy source record
    _write_legacy_source_record(tmp_path, pair, prepared)

    # But v2 target record records a DIFFERENT sha256
    v2_record = make_full_corpus_metadata_v2_build_record(
        collection_name=pair.target_collection,
        source_collection=pair.source_collection,
        source_build_record_sha256="f" * 64,
        candidate_id=pair.candidate_id,
        model_id=pair.model_id,
        revision=pair.revision,
        dimension=pair.dimension,
        corpus_identity=prepared.sparse_state.corpus_identity,
        sources=prepared.sources,
        sparse_state=prepared.sparse_state,
        sparse_state_sha256=prepared.sparse_state_sha256,
    )
    target_record_path = tmp_path / f"{pair.target_collection}.json"
    write_final_full_corpus_build_record(v2_record, target_record_path)

    client = RecordingClient(
        existing_collections=[pair.source_collection, pair.target_collection],
        points_by_collection={
            pair.source_collection: source_points,
            pair.target_collection: target_points,
        },
    )

    res = run_verify(client, [pair], prepared_corpus=prepared)
    assert res["status"] == "FAILED"
    assert any("Target build record lineage SHA-256 mismatch" in err for err in res["errors"])


def test_verify_fails_when_migration_lineage_mode_or_source_mismatch(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_points = make_mock_source_points(prepared.chunks, pair.dimension)
    target_points = [
        models.Record(id=s.id, vector=s.vector, payload=prepared.chunks[i].to_qdrant_payload())
        for i, s in enumerate(source_points)
    ]
    source_sha = _write_legacy_source_record(tmp_path, pair, prepared)

    # 1. Mode mismatch
    v2_record = make_full_corpus_metadata_v2_build_record(
        collection_name=pair.target_collection,
        source_collection=pair.source_collection,
        source_build_record_sha256=source_sha,
        candidate_id=pair.candidate_id,
        model_id=pair.model_id,
        revision=pair.revision,
        dimension=pair.dimension,
        corpus_identity=prepared.sparse_state.corpus_identity,
        sources=prepared.sources,
        sparse_state=prepared.sparse_state,
        sparse_state_sha256=prepared.sparse_state_sha256,
    )
    v2_record["migration"]["mode"] = "wrong_mode"
    target_record_path = tmp_path / f"{pair.target_collection}.json"
    write_final_full_corpus_build_record(v2_record, target_record_path)

    client = RecordingClient(
        existing_collections=[pair.source_collection, pair.target_collection],
        points_by_collection={
            pair.source_collection: source_points,
            pair.target_collection: target_points,
        },
    )

    res = run_verify(client, [pair], prepared_corpus=prepared)
    assert res["status"] == "FAILED"
    assert any("Target build record migration mode mismatch" in err for err in res["errors"])

    # 2. Source collection mismatch
    target_record_path.unlink()
    v2_record["migration"]["mode"] = "copy_verified_vectors"
    v2_record["migration"]["source_collection"] = "other_source"
    write_final_full_corpus_build_record(v2_record, target_record_path)

    res2 = run_verify(client, [pair], prepared_corpus=prepared)
    assert res2["status"] == "FAILED"
    assert any("Target build record source_collection mismatch" in err for err in res2["errors"])


@pytest.mark.parametrize(
    "mutator,expected_err",
    [
        (lambda r: r.update({"schema_version": "v1"}), "Target build record schema_version is not v2"),
        (lambda r: r.update({"status": "failed"}), "Target build record status is not complete"),
        (lambda r: r.update({"collection_name": "wrong_col"}), "Target build record collection_name mismatch"),
        (lambda r: r.update({"representation": "B"}), "Target build record representation mismatch"),
        (lambda r: r["dense"].update({"candidate_id": "other"}), "Target build record candidate_id mismatch"),
        (lambda r: r["dense"].update({"dimension": 999}), "Target build record dimension mismatch"),
        (lambda r: r["corpus"].update({"identity": "wrong"}), "Target build record corpus identity mismatch"),
        (lambda r: r["sparse"].update({"state_sha256": "wrong"}), "Target build record sparse state_sha256 mismatch"),
        (lambda r: r["qdrant"].update({"payload_schema_version": "v1"}), "Target build record payload_schema_version is not v2"),
        (lambda r: r["qdrant"].update({"dense_vector_name": "vec"}), "Target build record dense_vector_name is not 'dense'"),
    ],
)
def test_verify_fails_on_target_build_record_field_mismatches(tmp_path, monkeypatch, mutator, expected_err):
    monkeypatch.setattr("backend.ingestion.full_corpus_metadata_v2.BUILD_RECORD_ROOT", tmp_path)
    pair = get_migration_pair("e5-small-384")
    prepared = make_mock_prepared_corpus()
    source_points = make_mock_source_points(prepared.chunks, pair.dimension)
    target_points = [
        models.Record(id=s.id, vector=s.vector, payload=prepared.chunks[i].to_qdrant_payload())
        for i, s in enumerate(source_points)
    ]
    source_sha = _write_legacy_source_record(tmp_path, pair, prepared)

    v2_record = make_full_corpus_metadata_v2_build_record(
        collection_name=pair.target_collection,
        source_collection=pair.source_collection,
        source_build_record_sha256=source_sha,
        candidate_id=pair.candidate_id,
        model_id=pair.model_id,
        revision=pair.revision,
        dimension=pair.dimension,
        corpus_identity=prepared.sparse_state.corpus_identity,
        sources=prepared.sources,
        sparse_state=prepared.sparse_state,
        sparse_state_sha256=prepared.sparse_state_sha256,
    )
    mutator(v2_record)
    target_record_path = tmp_path / f"{pair.target_collection}.json"
    write_final_full_corpus_build_record(v2_record, target_record_path)

    client = RecordingClient(
        existing_collections=[pair.source_collection, pair.target_collection],
        points_by_collection={
            pair.source_collection: source_points,
            pair.target_collection: target_points,
        },
    )

    res = run_verify(client, [pair], prepared_corpus=prepared)
    assert res["status"] == "FAILED"
    assert any(expected_err in err for err in res["errors"])
