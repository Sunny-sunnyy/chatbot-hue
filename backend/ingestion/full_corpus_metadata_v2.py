"""Full-corpus Metadata v2 migration primitives, verification, and guarded CLI.

This module copies verified vectors from legacy Representation A collections
to isolated metadata-v2 collections with the canonical seven-field payload.
No dense embedding model is loaded.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import sys
from typing import Any, Mapping, Sequence
import uuid

import numpy as np
from qdrant_client import QdrantClient, models

from backend.core.schema import (
    FullCorpusChunk,
    point_id_for_chunk_id,
    validate_chunk_id,
)
from backend.core.settings_loader import load_settings
from backend.embedding.sparse import (
    SparseState,
    compute_corpus_identity,
    load_sparse_state,
)
from backend.ingestion.chunking.full_corpus_chunker import chunk_full_corpus
from backend.ingestion.full_corpus_pipeline import (
    BUILD_RECORD_ROOT,
    EXPECTED_CHUNK_COUNT,
    EXPECTED_CORPUS_IDENTITY,
    EXPECTED_FILE_COUNT,
    EXPECTED_SPARSE_SHA256,
    FULL_CORPUS_CANDIDATES,
    QDRANT_TIMEOUT,
    SPARSE_STATE_PATH,
    PreparedFullCorpus,
    prepare_full_corpus_input,
)
from backend.ingestion.source_state import (
    FULL_CORPUS_BUILD_SCHEMA_V2,
    FULL_CORPUS_PAYLOAD_SCHEMA_V2,
    compute_corpus_state,
    discover_full_corpus_files,
    make_full_corpus_metadata_v2_build_record,
    verify_full_corpus_record_freshness,
    write_final_full_corpus_build_record,
)
from backend.vectorstore.qdrant import (
    QdrantSchemaError,
    client_from_settings,
    create_full_corpus_collection,
    expected_full_corpus_schema,
    inspect_full_corpus_target,
    validate_full_corpus_collection_params,
)

LEGACY_PAYLOAD_FIELDS = frozenset(
    {"search_text", "source", "title", "heading_path", "evidence_parts"}
)
CANONICAL_PAYLOAD_FIELDS = frozenset(
    {
        "search_text",
        "source",
        "title",
        "heading_path",
        "evidence_parts",
        "chunk_id",
        "domain",
    }
)
MIGRATION_BATCH_SIZE = 64


@dataclass(frozen=True)
class MigrationPair:
    candidate_id: str
    source_collection: str
    target_collection: str
    dimension: int
    model_id: str
    revision: str


def get_migration_pairs() -> tuple[MigrationPair, ...]:
    return tuple(
        MigrationPair(
            candidate_id=c.candidate_id,
            source_collection=c.collection_name,
            target_collection=c.metadata_v2_collection_name,
            dimension=c.dense_spec.dimension,
            model_id=c.dense_spec.model_id,
            revision=c.dense_spec.revision,
        )
        for c in FULL_CORPUS_CANDIDATES
    )


def get_migration_pair(candidate_id: str) -> MigrationPair:
    pairs = {p.candidate_id: p for p in get_migration_pairs()}
    if candidate_id not in pairs:
        raise ValueError(f"Unknown candidate: {candidate_id}")
    return pairs[candidate_id]


def validate_candidate_confirmation(candidate_id: str, confirm_target: str) -> MigrationPair:
    pair = get_migration_pair(candidate_id)
    if confirm_target != pair.target_collection:
        raise ValueError(
            f"Migration requires exact target confirmation: expected {pair.target_collection!r}, got {confirm_target!r}"
        )
    return pair


def validate_legacy_payload(point_id: str, payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError(f"Legacy payload for point {point_id} is not a dictionary")
    if set(payload) != LEGACY_PAYLOAD_FIELDS:
        raise ValueError(f"Legacy payload for point {point_id} does not have exactly 5 fields")
    if not isinstance(payload["search_text"], str) or not payload["search_text"]:
        raise ValueError(f"Legacy payload search_text invalid for point {point_id}")
    if not isinstance(payload["source"], str) or not payload["source"]:
        raise ValueError(f"Legacy payload source invalid for point {point_id}")
    if not isinstance(payload["title"], str):
        raise ValueError(f"Legacy payload title invalid for point {point_id}")
    if not isinstance(payload["heading_path"], list):
        raise ValueError(f"Legacy payload heading_path invalid for point {point_id}")
    if not isinstance(payload["evidence_parts"], list):
        raise ValueError(f"Legacy payload evidence_parts invalid for point {point_id}")
    return payload


def validate_named_vectors(
    point_id: str, vector: Any, expected_dimension: int
) -> tuple[list[float], models.SparseVector]:
    if not isinstance(vector, dict):
        raise ValueError(f"Point {point_id} vectors must be a dict of named vectors")
    if set(vector) != {"dense", "sparse"}:
        raise ValueError(f"Point {point_id} named vectors must be exactly 'dense' and 'sparse'")

    dense_val = vector["dense"]
    if isinstance(dense_val, np.ndarray):
        dense_list = dense_val.tolist()
    elif isinstance(dense_val, (list, tuple)):
        dense_list = list(dense_val)
    else:
        raise ValueError(f"Point {point_id} dense vector is not a sequence")

    if len(dense_list) != expected_dimension:
        raise ValueError(
            f"Point {point_id} dense vector dimension {len(dense_list)} != expected {expected_dimension}"
        )
    for val in dense_list:
        if not math.isfinite(float(val)):
            raise ValueError(f"Point {point_id} dense vector contains non-finite value")

    sparse_val = vector["sparse"]
    if isinstance(sparse_val, models.SparseVector):
        indices = list(sparse_val.indices)
        values = list(sparse_val.values)
    elif isinstance(sparse_val, dict):
        indices = list(sparse_val.get("indices", []))
        values = list(sparse_val.get("values", []))
    else:
        raise ValueError(f"Point {point_id} sparse vector is invalid")

    if len(indices) != len(values):
        raise ValueError(f"Point {point_id} Sparse indices/values length mismatch")
    if tuple(sorted(set(indices))) != tuple(indices):
        raise ValueError(f"Point {point_id} Sparse indices not strictly sorted/unique")
    for val in values:
        if not math.isfinite(float(val)):
            raise ValueError(f"Point {point_id} Sparse vector contains non-finite value")

    return dense_list, models.SparseVector(indices=indices, values=values)


def build_migrated_point(
    source_record: models.Record,
    chunk: FullCorpusChunk,
    expected_dimension: int,
) -> models.PointStruct:
    point_id_str = str(source_record.id)
    if point_id_str != chunk.point_id:
        raise ValueError(
            f"Source record point ID mismatch: record {point_id_str} != chunk {chunk.point_id}"
        )

    validate_legacy_payload(point_id_str, source_record.payload)
    dense_list, sparse_vector = validate_named_vectors(
        point_id_str, source_record.vector, expected_dimension
    )

    validate_chunk_id(chunk.source, chunk.chunk_id)
    payload_v2 = chunk.to_qdrant_payload()
    if set(payload_v2) != CANONICAL_PAYLOAD_FIELDS:
        raise ValueError(f"Constructed chunk payload does not match 7 fields: {chunk.chunk_id}")

    return models.PointStruct(
        id=chunk.point_id,
        vector={
            "dense": dense_list,
            "sparse": sparse_vector,
        },
        payload=payload_v2,
    )


def assert_migrated_record_equal(
    source_record: models.Record,
    target_record: models.Record,
    expected_payload: Mapping[str, Any],
    expected_dimension: int,
) -> None:
    if str(target_record.id) != str(source_record.id):
        raise ValueError(
            f"Point ID mismatch: target {target_record.id} != source {source_record.id}"
        )

    s_dense, s_sparse = validate_named_vectors(
        str(source_record.id), source_record.vector, expected_dimension
    )
    t_dense, t_sparse = validate_named_vectors(
        str(target_record.id), target_record.vector, expected_dimension
    )

    if s_dense != t_dense:
        raise ValueError(f"Dense vector mismatch for point {source_record.id}")

    if list(s_sparse.indices) != list(t_sparse.indices) or list(s_sparse.values) != list(t_sparse.values):
        raise ValueError(f"Sparse vector mismatch for point {source_record.id}")

    if target_record.payload != dict(expected_payload):
        raise ValueError(f"Payload mismatch for point {source_record.id}")


def run_preflight(
    client: Any,
    candidates: Sequence[MigrationPair],
    prepared_corpus: PreparedFullCorpus | None = None,
) -> dict[str, Any]:
    """Run read-only preflight checks for selected candidate pairs without mutating Qdrant."""
    seen_cand_ids: set[str] = set()
    for pair in candidates:
        if pair.candidate_id in seen_cand_ids:
            raise ValueError(f"Duplicate candidate selector: {pair.candidate_id}")
        seen_cand_ids.add(pair.candidate_id)

    corpus_prep_error: str | None = None
    if prepared_corpus is None:
        try:
            prepared_corpus = prepare_full_corpus_input()
        except Exception as exc:
            corpus_prep_error = f"Corpus preparation failed: {type(exc).__name__}"
            prepared_corpus = None

    if prepared_corpus is None and corpus_prep_error is None:
        corpus_prep_error = "Corpus preparation failed: Prepared corpus is None"

    chunks_by_point_id: dict[str, FullCorpusChunk] = {}
    if prepared_corpus is not None:
        chunks_by_point_id = {c.point_id: c for c in prepared_corpus.chunks}

    candidate_results = []
    overall_errors = []
    if corpus_prep_error:
        overall_errors.append(corpus_prep_error)

    for pair in candidates:
        pair_errors: list[str] = []
        if corpus_prep_error:
            pair_errors.append(corpus_prep_error)

        target_absent = False
        try:
            target_absent = not client.collection_exists(pair.target_collection)
            if not target_absent:
                pair_errors.append(f"Target collection {pair.target_collection} already exists")
        except Exception as exc:
            pair_errors.append(f"Failed inspecting target collection: {type(exc).__name__}")

        target_record_absent = False
        try:
            target_record_path = BUILD_RECORD_ROOT / f"{pair.target_collection}.json"
            target_record_absent = not target_record_path.exists()
            if not target_record_absent:
                pair_errors.append(f"Target build record {target_record_path.name} already exists")
        except Exception as exc:
            pair_errors.append(f"Failed inspecting target build record: {type(exc).__name__}")

        source_record_path = BUILD_RECORD_ROOT / f"{pair.source_collection}.json"
        source_record_sha = None
        source_record: dict[str, Any] | None = None
        try:
            if not source_record_path.exists():
                pair_errors.append(f"Source build record {source_record_path.name} does not exist")
            else:
                source_bytes = source_record_path.read_bytes()
                source_record_sha = hashlib.sha256(source_bytes).hexdigest()
                source_record = json.loads(source_bytes.decode("utf-8"))

                if source_record.get("schema_version") != "phase_4_full_corpus_build:v1":
                    pair_errors.append("Source build record schema version is not v1")
                if source_record.get("status") != "complete":
                    pair_errors.append("Source build record status is not complete")
                if source_record.get("collection_name") != pair.source_collection:
                    pair_errors.append(
                        f"Source build record collection_name mismatch: expected {pair.source_collection}, got {source_record.get('collection_name')}"
                    )
                if source_record.get("representation") != "A":
                    pair_errors.append(
                        f"Source build record representation mismatch: expected 'A', got {source_record.get('representation')!r}"
                    )

                dense_info = source_record.get("dense", {})
                if dense_info.get("candidate_id") != pair.candidate_id:
                    pair_errors.append("Source build record candidate_id mismatch")
                if dense_info.get("dimension") != pair.dimension:
                    pair_errors.append("Source build record dimension mismatch")
                if dense_info.get("model_id") != pair.model_id:
                    pair_errors.append("Source build record model_id mismatch")
                if dense_info.get("revision") != pair.revision:
                    pair_errors.append("Source build record revision mismatch")

                if prepared_corpus is not None:
                    corpus_info = source_record.get("corpus", {})
                    if corpus_info.get("identity") != prepared_corpus.sparse_state.corpus_identity:
                        pair_errors.append("Source build record corpus identity mismatch")
                    if corpus_info.get("file_count") != len(prepared_corpus.sources):
                        pair_errors.append(
                            f"Source build record corpus file_count {corpus_info.get('file_count')} != {len(prepared_corpus.sources)}"
                        )
                    if corpus_info.get("chunk_count") != len(prepared_corpus.chunks):
                        pair_errors.append(
                            f"Source build record corpus chunk_count {corpus_info.get('chunk_count')} != {len(prepared_corpus.chunks)}"
                        )

                    is_fresh, discrepancies = verify_full_corpus_record_freshness(
                        prepared_corpus.sources, source_record
                    )
                    if not is_fresh:
                        pair_errors.append(
                            f"Source state freshness mismatch: {len(discrepancies)} discrepancies"
                        )

                    sparse_info = source_record.get("sparse", {})
                    if sparse_info.get("schema_version") != prepared_corpus.sparse_state.schema_version:
                        pair_errors.append("Source build record sparse schema_version mismatch")
                    if sparse_info.get("state_sha256") != prepared_corpus.sparse_state_sha256:
                        pair_errors.append("Source build record sparse state_sha256 mismatch")
                    if sparse_info.get("vocabulary_size") != len(prepared_corpus.sparse_state.vocabulary):
                        pair_errors.append(
                            f"Source build record sparse vocabulary_size mismatch: expected {len(prepared_corpus.sparse_state.vocabulary)}, got {sparse_info.get('vocabulary_size')}"
                        )

                    qdrant_info = source_record.get("qdrant", {})
                    if qdrant_info.get("dense_vector_name") != "dense":
                        pair_errors.append("Source build record dense_vector_name is not 'dense'")
                    if qdrant_info.get("sparse_vector_name") != "sparse":
                        pair_errors.append("Source build record sparse_vector_name is not 'sparse'")
                    if qdrant_info.get("distance") != "cosine":
                        pair_errors.append("Source build record distance is not 'cosine'")
                    if qdrant_info.get("point_count") != len(prepared_corpus.chunks):
                        pair_errors.append(
                            f"Source build record point_count mismatch: expected {len(prepared_corpus.chunks)}, got {qdrant_info.get('point_count')}"
                        )
        except Exception as exc:
            pair_errors.append(f"Failed inspecting source build record: {type(exc).__name__}")

        seen_point_ids: set[str] = set()
        expected_chunk_count = len(prepared_corpus.chunks) if prepared_corpus is not None else 0

        source_exists = False
        try:
            source_exists = client.collection_exists(pair.source_collection)
            if not source_exists:
                pair_errors.append(f"Source collection {pair.source_collection} does not exist")
        except Exception as exc:
            pair_errors.append(f"Failed inspecting source collection: {type(exc).__name__}")

        if source_exists:
            source_info = None
            try:
                source_info = client.get_collection(pair.source_collection)
            except Exception as exc:
                pair_errors.append(f"Failed inspecting source collection: {type(exc).__name__}")

            if source_info is not None:
                try:
                    if prepared_corpus is not None and source_info.points_count != expected_chunk_count:
                        pair_errors.append(
                            f"Source collection points count {source_info.points_count} != expected {expected_chunk_count}"
                        )
                    validate_full_corpus_collection_params(source_info.config.params, pair.dimension)

                    offset = None
                    while True:
                        try:
                            records, offset = client.scroll(
                                pair.source_collection,
                                limit=MIGRATION_BATCH_SIZE,
                                offset=offset,
                                with_payload=True,
                                with_vectors=True,
                            )
                        except Exception as exc:
                            pair_errors.append(f"Failed scrolling source collection: {type(exc).__name__}")
                            break

                        if not records:
                            break
                        for rec in records:
                            pid = str(rec.id)
                            if pid in seen_point_ids:
                                pair_errors.append(f"Duplicate point ID in source collection: {pid}")
                                break
                            seen_point_ids.add(pid)
                            if chunks_by_point_id and pid not in chunks_by_point_id:
                                pair_errors.append(f"Foreign point ID in source collection: {pid}")
                                break
                            try:
                                validate_legacy_payload(pid, rec.payload)
                                validate_named_vectors(pid, rec.vector, pair.dimension)
                            except ValueError as ve:
                                pair_errors.append(f"Point {pid} validation failed: {type(ve).__name__}")
                                break

                            if chunks_by_point_id:
                                chunk = chunks_by_point_id[pid]
                                expected_legacy_payload = {
                                    "search_text": chunk.search_text,
                                    "source": chunk.source,
                                    "title": chunk.title,
                                    "heading_path": list(chunk.heading_path),
                                    "evidence_parts": [part.to_dict() for part in chunk.evidence_parts],
                                }
                                if rec.payload != expected_legacy_payload:
                                    pair_errors.append(f"Legacy payload value mismatch for point {pid}")
                                    break

                        if pair_errors or offset is None:
                            break

                    if not pair_errors:
                        if prepared_corpus is not None and len(seen_point_ids) != expected_chunk_count:
                            pair_errors.append(
                                f"Scrolled source points count {len(seen_point_ids)} != expected {expected_chunk_count}"
                            )
                        if chunks_by_point_id and seen_point_ids != set(chunks_by_point_id.keys()):
                            pair_errors.append("Scrolled source point IDs do not match canonical point IDs")

                except Exception as exc:
                    pair_errors.append(f"Failed scrolling source collection: {type(exc).__name__}")

        pair_ready = len(pair_errors) == 0 and corpus_prep_error is None
        if not pair_ready:
            overall_errors.extend(err for err in pair_errors if err not in overall_errors)

        # Artifact only emits validated observed values if pair_ready is True
        observed_corpus_identity = (
            source_record["corpus"]["identity"]
            if pair_ready and source_record and "corpus" in source_record
            else ""
        )
        observed_sparse_sha256 = (
            source_record["sparse"]["state_sha256"]
            if pair_ready and source_record and "sparse" in source_record
            else ""
        )

        candidate_results.append(
            {
                "candidate_id": pair.candidate_id,
                "source_collection": pair.source_collection,
                "target_collection": pair.target_collection,
                "dimension": pair.dimension,
                "source_points_count": len(seen_point_ids) if pair_ready else 0,
                "source_build_record_sha256": source_record_sha if pair_ready and source_record_sha else "",
                "corpus_identity": observed_corpus_identity,
                "sparse_state_sha256": observed_sparse_sha256,
                "target_collection_absent": target_absent,
                "target_build_record_absent": target_record_absent,
                "status": "READY" if pair_ready else "BLOCKED",
                "errors": pair_errors,
            }
        )

    ready_count = sum(1 for c in candidate_results if c["status"] == "READY")
    overall_status = "READY" if ready_count == len(candidates) and not overall_errors else "BLOCKED"

    return {
        "status": overall_status,
        "schema_version": "phase_4_metadata_v2_preflight:v1",
        "summary": {
            "total_pairs": len(candidates),
            "ready_pairs": ready_count,
            "blocked_pairs": len(candidates) - ready_count,
            "total_mutations": 0,
        },
        "candidates": candidate_results,
        "errors": overall_errors,
    }


def run_verify(
    client: Any,
    candidates: Sequence[MigrationPair],
    prepared_corpus: PreparedFullCorpus | None = None,
    require_build_record: bool = True,
) -> dict[str, Any]:
    """Run read-only full verification of existing target collections and v2 build records."""
    seen_cand_ids: set[str] = set()
    for pair in candidates:
        if pair.candidate_id in seen_cand_ids:
            raise ValueError(f"Duplicate candidate selector: {pair.candidate_id}")
        seen_cand_ids.add(pair.candidate_id)

    if prepared_corpus is None:
        try:
            prepared_corpus = prepare_full_corpus_input()
        except Exception as exc:
            err = f"Corpus preparation failed: {type(exc).__name__}"
            return {
                "status": "FAILED",
                "summary": {
                    "total_pairs": len(candidates),
                    "verified_pairs": 0,
                    "failed_pairs": len(candidates),
                    "total_mutations": 0,
                },
                "candidates": [
                    {
                        "candidate_id": p.candidate_id,
                        "target_collection": p.target_collection,
                        "verified_points_count": 0,
                        "status": "FAILED",
                        "errors": [err],
                    }
                    for p in candidates
                ],
                "errors": [err],
            }

    chunks_by_point_id = {c.point_id: c for c in prepared_corpus.chunks}
    expected_chunk_count = len(prepared_corpus.chunks)

    results = []
    overall_errors = []

    for pair in candidates:
        pair_errors: list[str] = []

        try:
            if not client.collection_exists(pair.target_collection):
                pair_errors.append(f"Target collection {pair.target_collection} does not exist")
        except Exception as exc:
            pair_errors.append(f"Failed inspecting target collection: {type(exc).__name__}")

        if require_build_record:
            target_record_path = BUILD_RECORD_ROOT / f"{pair.target_collection}.json"
            if not target_record_path.exists():
                pair_errors.append(f"Target build record {target_record_path.name} does not exist")
            else:
                try:
                    target_bytes = target_record_path.read_bytes()
                    target_record = json.loads(target_bytes.decode("utf-8"))

                    # Base v2 record fields
                    if target_record.get("schema_version") != FULL_CORPUS_BUILD_SCHEMA_V2:
                        pair_errors.append("Target build record schema_version is not v2")
                    if target_record.get("status") != "complete":
                        pair_errors.append("Target build record status is not complete")
                    if target_record.get("collection_name") != pair.target_collection:
                        pair_errors.append("Target build record collection_name mismatch")
                    if target_record.get("representation") != "A":
                        pair_errors.append("Target build record representation mismatch")

                    # Migration lineage validation
                    migration_info = target_record.get("migration", {})
                    if migration_info.get("mode") != "copy_verified_vectors":
                        pair_errors.append("Target build record migration mode mismatch")
                    if migration_info.get("source_collection") != pair.source_collection:
                        pair_errors.append("Target build record source_collection mismatch")

                    recorded_source_sha = migration_info.get("source_build_record_sha256")
                    source_record_path = BUILD_RECORD_ROOT / f"{pair.source_collection}.json"
                    if not source_record_path.exists():
                        pair_errors.append(
                            f"Source build record {source_record_path.name} does not exist for lineage check"
                        )
                    else:
                        actual_source_sha = hashlib.sha256(source_record_path.read_bytes()).hexdigest()
                        if recorded_source_sha != actual_source_sha:
                            pair_errors.append("Target build record lineage SHA-256 mismatch")

                    # Dense spec
                    dense_info = target_record.get("dense", {})
                    if dense_info.get("candidate_id") != pair.candidate_id:
                        pair_errors.append("Target build record candidate_id mismatch")
                    if dense_info.get("dimension") != pair.dimension:
                        pair_errors.append("Target build record dimension mismatch")
                    if dense_info.get("model_id") != pair.model_id:
                        pair_errors.append("Target build record model_id mismatch")
                    if dense_info.get("revision") != pair.revision:
                        pair_errors.append("Target build record revision mismatch")

                    # Corpus spec
                    corpus_info = target_record.get("corpus", {})
                    if corpus_info.get("identity") != prepared_corpus.sparse_state.corpus_identity:
                        pair_errors.append("Target build record corpus identity mismatch")
                    if corpus_info.get("file_count") not in {len(prepared_corpus.sources), EXPECTED_FILE_COUNT}:
                        pair_errors.append("Target build record corpus file_count mismatch")
                    if corpus_info.get("chunk_count") not in {len(prepared_corpus.chunks), EXPECTED_CHUNK_COUNT}:
                        pair_errors.append("Target build record corpus chunk_count mismatch")
                    is_fresh, discrepancies = verify_full_corpus_record_freshness(
                        prepared_corpus.sources, target_record
                    )
                    if not is_fresh:
                        pair_errors.append(
                            f"Target build record freshness mismatch: {len(discrepancies)} discrepancies"
                        )

                    # Sparse spec
                    sparse_info = target_record.get("sparse", {})
                    if sparse_info.get("schema_version") != prepared_corpus.sparse_state.schema_version:
                        pair_errors.append("Target build record sparse schema_version mismatch")
                    if sparse_info.get("state_sha256") != prepared_corpus.sparse_state_sha256:
                        pair_errors.append("Target build record sparse state_sha256 mismatch")
                    if sparse_info.get("vocabulary_size") != len(prepared_corpus.sparse_state.vocabulary):
                        pair_errors.append("Target build record sparse vocabulary_size mismatch")

                    # Qdrant params
                    qdrant_info = target_record.get("qdrant", {})
                    if qdrant_info.get("dense_vector_name") != "dense":
                        pair_errors.append("Target build record dense_vector_name is not 'dense'")
                    if qdrant_info.get("sparse_vector_name") != "sparse":
                        pair_errors.append("Target build record sparse_vector_name is not 'sparse'")
                    if qdrant_info.get("distance") != "cosine":
                        pair_errors.append("Target build record distance is not 'cosine'")
                    if qdrant_info.get("point_count") not in {len(prepared_corpus.chunks), EXPECTED_CHUNK_COUNT}:
                        pair_errors.append("Target build record point_count mismatch")
                    if qdrant_info.get("payload_schema_version") != FULL_CORPUS_PAYLOAD_SCHEMA_V2:
                        pair_errors.append("Target build record payload_schema_version is not v2")

                except Exception as exc:
                    pair_errors.append(f"Failed reading target build record: {type(exc).__name__}")

        try:
            if not client.collection_exists(pair.source_collection):
                pair_errors.append(f"Source collection {pair.source_collection} does not exist")
        except Exception as exc:
            pair_errors.append(f"Failed inspecting source collection: {type(exc).__name__}")

        verified_count = 0
        if not pair_errors:
            target_info = None
            try:
                target_info = client.get_collection(pair.target_collection)
            except Exception as exc:
                pair_errors.append(f"Failed inspecting target collection: {type(exc).__name__}")

            if target_info is not None:
                try:
                    if target_info.points_count != expected_chunk_count:
                        pair_errors.append(
                            f"Target collection points count {target_info.points_count} != expected {expected_chunk_count}"
                        )
                    if getattr(target_info, "payload_schema", None) != {}:
                        pair_errors.append("Target collection has non-empty payload_schema (indexes forbidden)")
                    validate_full_corpus_collection_params(target_info.config.params, pair.dimension)

                    offset = None
                    seen_target_ids: set[str] = set()

                    while True:
                        try:
                            source_page, offset = client.scroll(
                                pair.source_collection,
                                limit=MIGRATION_BATCH_SIZE,
                                offset=offset,
                                with_payload=True,
                                with_vectors=True,
                            )
                        except Exception as exc:
                            pair_errors.append(f"Failed scrolling source collection: {type(exc).__name__}")
                            break

                        if not source_page:
                            break
                        ids = [rec.id for rec in source_page]

                        try:
                            target_points = client.retrieve(
                                pair.target_collection,
                                ids=ids,
                                with_payload=True,
                                with_vectors=True,
                            )
                        except Exception as exc:
                            pair_errors.append(f"Failed retrieving target points: {type(exc).__name__}")
                            break

                        target_by_id = {str(rec.id): rec for rec in target_points}

                        for s_rec in source_page:
                            pid = str(s_rec.id)
                            if pid not in target_by_id:
                                pair_errors.append(f"Point {pid} missing from target collection")
                                break
                            t_rec = target_by_id[pid]
                            seen_target_ids.add(pid)
                            chunk = chunks_by_point_id[pid]
                            try:
                                assert_migrated_record_equal(
                                    s_rec, t_rec, chunk.to_qdrant_payload(), pair.dimension
                                )
                            except ValueError as ve:
                                pair_errors.append(str(ve))
                                break
                            verified_count += 1

                        if pair_errors or offset is None:
                            break

                    if not pair_errors:
                        if verified_count != expected_chunk_count:
                            pair_errors.append(
                                f"Verified points count {verified_count} != expected {expected_chunk_count}"
                            )
                        elif seen_target_ids != set(chunks_by_point_id.keys()):
                            pair_errors.append("Verified target point IDs do not match canonical point IDs")

                except Exception as exc:
                    pair_errors.append(f"Verification error: {type(exc).__name__}")

        pair_verified = len(pair_errors) == 0
        if not pair_verified:
            overall_errors.extend(err for err in pair_errors if err not in overall_errors)

        results.append(
            {
                "candidate_id": pair.candidate_id,
                "target_collection": pair.target_collection,
                "verified_points_count": verified_count if pair_verified else 0,
                "status": "VERIFIED" if pair_verified else "FAILED",
                "errors": pair_errors,
            }
        )

    verified_count_total = sum(1 for r in results if r["status"] == "VERIFIED")
    overall_status = "VERIFIED" if verified_count_total == len(candidates) and not overall_errors else "FAILED"

    return {
        "status": overall_status,
        "summary": {
            "total_pairs": len(candidates),
            "verified_pairs": verified_count_total,
            "failed_pairs": len(candidates) - verified_count_total,
            "total_mutations": 0,
        },
        "candidates": results,
        "errors": overall_errors,
    }


def run_migration(
    client: Any,
    pair: MigrationPair,
    confirm_target: str,
    prepared_corpus: PreparedFullCorpus | None = None,
) -> dict[str, Any]:
    """Execute migration for one pair after strict confirmation and preflight."""
    validate_candidate_confirmation(pair.candidate_id, confirm_target)

    if prepared_corpus is None:
        prepared_corpus = prepare_full_corpus_input()
    chunks_by_point_id = {c.point_id: c for c in prepared_corpus.chunks}
    expected_chunk_count = len(prepared_corpus.chunks)

    # Preflight check for this single pair
    preflight = run_preflight(client, [pair], prepared_corpus=prepared_corpus)
    if preflight["status"] != "READY":
        raise ValueError(f"Preflight failed before migration: {preflight['errors']}")

    preflight_cand = preflight["candidates"][0]
    preflight_source_sha = preflight_cand.get("source_build_record_sha256", "")
    if not preflight_source_sha:
        raise RuntimeError(
            f"Preflight did not return source_build_record_sha256 for {pair.candidate_id}"
        )

    create_full_corpus_collection(
        client, pair.target_collection, pair.dimension, timeout=QDRANT_TIMEOUT
    )

    offset = None
    upserted_count = 0
    while True:
        records, offset = client.scroll(
            pair.source_collection,
            limit=MIGRATION_BATCH_SIZE,
            offset=offset,
            with_payload=True,
            with_vectors=True,
        )
        if not records:
            break
        target_points = []
        for s_rec in records:
            pid = str(s_rec.id)
            chunk = chunks_by_point_id[pid]
            pt = build_migrated_point(s_rec, chunk, pair.dimension)
            target_points.append(pt)

        client.upsert(pair.target_collection, points=target_points, wait=True)
        upserted_count += len(target_points)
        if offset is None:
            break

    if upserted_count != expected_chunk_count:
        raise RuntimeError(
            f"Upserted point count {upserted_count} != expected {expected_chunk_count}"
        )

    # Full target collection verification before writing build record (R3)
    target_verify = run_verify(
        client, [pair], prepared_corpus=prepared_corpus, require_build_record=False
    )
    if target_verify["status"] != "VERIFIED":
        err_msg = "; ".join(target_verify.get("errors", []))
        raise RuntimeError(
            f"Post-migration target verification failed for {pair.target_collection}: {err_msg}"
        )

    # Re-validate source build record SHA before writing v2 build record (C2-R1)
    source_record_path = BUILD_RECORD_ROOT / f"{pair.source_collection}.json"
    try:
        current_source_bytes = source_record_path.read_bytes()
        current_source_sha = hashlib.sha256(current_source_bytes).hexdigest()
    except Exception as exc:
        raise RuntimeError(
            f"Failed reading legacy source build record before final write: {type(exc).__name__}"
        ) from exc

    if current_source_sha != preflight_source_sha:
        raise RuntimeError(
            f"Legacy source build record SHA changed after preflight: "
            f"preflight={preflight_source_sha} != current={current_source_sha}"
        )

    # Write v2 build record only after target verification and lineage re-validation succeed
    v2_record = make_full_corpus_metadata_v2_build_record(
        collection_name=pair.target_collection,
        source_collection=pair.source_collection,
        source_build_record_sha256=preflight_source_sha,
        candidate_id=pair.candidate_id,
        model_id=pair.model_id,
        revision=pair.revision,
        dimension=pair.dimension,
        corpus_identity=prepared_corpus.sparse_state.corpus_identity,
        sources=prepared_corpus.sources,
        sparse_state=prepared_corpus.sparse_state,
        sparse_state_sha256=prepared_corpus.sparse_state_sha256,
    )
    target_record_path = BUILD_RECORD_ROOT / f"{pair.target_collection}.json"
    record_digest = write_final_full_corpus_build_record(v2_record, target_record_path)

    # Final verify including build record
    final_verify = run_verify(
        client, [pair], prepared_corpus=prepared_corpus, require_build_record=True
    )
    if final_verify["status"] != "VERIFIED":
        err_msg = "; ".join(final_verify.get("errors", []))
        raise RuntimeError(
            f"Final post-write verification failed for {pair.target_collection}: {err_msg}"
        )

    return {
        "candidate_id": pair.candidate_id,
        "source_collection": pair.source_collection,
        "target_collection": pair.target_collection,
        "upserted_points": upserted_count,
        "build_record_path": str(target_record_path),
        "build_record_sha256": record_digest,
        "status": "MIGRATED",
    }


def _atomic_write_json(data: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_name(f"{output_path.name}.tmp.{uuid.uuid4().hex}")
    content = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    temp_path.write_text(content, encoding="utf-8")
    os.replace(temp_path, output_path)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m backend.ingestion.full_corpus_metadata_v2",
        description="Full-corpus Metadata v2 migration and verification CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Preflight
    parser_preflight = subparsers.add_parser("preflight", help="Run read-only preflight checks")
    parser_preflight.add_argument(
        "--candidate",
        nargs="+",
        choices=[c.candidate_id for c in FULL_CORPUS_CANDIDATES],
        default=[c.candidate_id for c in FULL_CORPUS_CANDIDATES],
        help="One or more candidate IDs to preflight",
    )
    parser_preflight.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Path to write the sanitized preflight JSON artifact",
    )

    # Migrate
    parser_migrate = subparsers.add_parser("migrate", help="Execute vector copy migration for one candidate")
    parser_migrate.add_argument(
        "--candidate",
        required=True,
        choices=[c.candidate_id for c in FULL_CORPUS_CANDIDATES],
        help="Single candidate ID to migrate",
    )
    parser_migrate.add_argument(
        "--confirm-target",
        required=True,
        type=str,
        help="Exact target collection name confirmation",
    )

    # Verify
    parser_verify = subparsers.add_parser("verify", help="Verify migrated collections and build records")
    parser_verify.add_argument(
        "--candidate",
        nargs="+",
        choices=[c.candidate_id for c in FULL_CORPUS_CANDIDATES],
        default=[c.candidate_id for c in FULL_CORPUS_CANDIDATES],
        help="One or more candidate IDs to verify",
    )

    args = parser.parse_args(argv)

    if args.command in {"preflight", "verify"}:
        seen_candidates: set[str] = set()
        for cid in args.candidate:
            if cid in seen_candidates:
                parser.error(f"Duplicate candidate selector: {cid}")
            seen_candidates.add(cid)

    settings = load_settings()
    client = client_from_settings(settings)

    if args.command == "preflight":
        pairs = [get_migration_pair(cid) for cid in args.candidate]
        result = run_preflight(client, pairs)
        _atomic_write_json(result, args.output)
        print(f"Preflight status: {result['status']}")
        if result["status"] != "READY":
            for err in result["errors"]:
                print(f"ERROR: {err}", file=sys.stderr)
            return 1
        return 0

    if args.command == "migrate":
        pair = get_migration_pair(args.candidate)
        result = run_migration(client, pair, confirm_target=args.confirm_target)
        print(f"Migration completed for {pair.candidate_id}: {result}")
        return 0

    if args.command == "verify":
        pairs = [get_migration_pair(cid) for cid in args.candidate]
        result = run_verify(client, pairs)
        print(f"Verification status: {result['status']}")
        if result["status"] != "VERIFIED":
            for err in result["errors"]:
                print(f"ERROR: {err}", file=sys.stderr)
            return 1
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
