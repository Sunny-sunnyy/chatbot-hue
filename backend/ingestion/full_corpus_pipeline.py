from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import importlib.metadata
import json
import logging
from pathlib import Path
import shutil
from typing import Any
import uuid

import numpy as np
import torch

from backend.core.schema import FullCorpusChunk
from backend.core.settings_loader import load_settings
from backend.embedding.full_corpus import (
    DENSE_MODEL_SPECS,
    DenseModelSpec,
    FullCorpusDenseRunner,
    resolve_snapshot,
)
from backend.embedding.sparse import (
    SparseState,
    build_vocabulary_index,
    compute_corpus_identity,
    load_sparse_state,
)
from backend.ingestion.chunking.full_corpus_chunker import chunk_full_corpus
from backend.ingestion.source_state import (
    compute_corpus_state,
    discover_full_corpus_files,
    make_full_corpus_build_record,
    write_final_full_corpus_build_record,
)
from backend.vectorstore.points import (
    build_full_corpus_point_batch,
    validate_full_corpus_point_inputs,
)
from backend.vectorstore.qdrant import (
    client_from_settings,
    create_full_corpus_collection,
    inspect_full_corpus_target,
    require_fresh_full_corpus_target,
)
from backend.vectorstore.upsert import (
    upsert_full_corpus_batch,
    verify_full_corpus_collection,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SPARSE_STATE_PATH = REPOSITORY_ROOT / "data/full_corpus_builds/phase_3_sparse_state.json"
PHASE3_EVIDENCE_PATH = REPOSITORY_ROOT / "reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json"
PREFLIGHT_OUTPUT_PATH = REPOSITORY_ROOT / "reports/artifacts/full_corpus_phase_4_qdrant_preflight_2026_09_12.json"
BUILD_RECORD_ROOT = REPOSITORY_ROOT / "data/full_corpus_builds"
EXPECTED_FILE_COUNT = 205
EXPECTED_CHUNK_COUNT = 8460
EXPECTED_CORPUS_IDENTITY = "0e5c059516cd942b151286cf597f785c65e642cacd1b0421124fe50fe574f223"
EXPECTED_SPARSE_SHA256 = "5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be"
QDRANT_TIMEOUT = 30


@dataclass(frozen=True)
class FullCorpusCandidate:
    candidate_id: str
    collection_name: str
    dense_spec: DenseModelSpec


_COLLECTION_BY_CANDIDATE = {
    "e5-small-384": "hue_full_corpus_a_e5_small_384",
    "e5-base-768": "hue_full_corpus_a_e5_base_768",
    "huydang-dek21-768": "hue_full_corpus_a_huydang_dek21_768",
    "qwen3-embedding-0.6b-1024": "hue_full_corpus_a_qwen3_06b_1024",
}
if set(_COLLECTION_BY_CANDIDATE) != {spec.key for spec in DENSE_MODEL_SPECS}:
    raise RuntimeError("Phase 4 collection mapping does not match Phase 3 dense specs")
FULL_CORPUS_CANDIDATES = tuple(
    FullCorpusCandidate(spec.key, _COLLECTION_BY_CANDIDATE[spec.key], spec)
    for spec in DENSE_MODEL_SPECS
)


@dataclass(frozen=True)
class PreparedFullCorpus:
    chunks: list[FullCorpusChunk]
    sources: dict[str, str]
    source_state_sha256: str
    sparse_state: SparseState
    sparse_state_sha256: str
    sample_chunk_ids: tuple[str, ...]


def candidate_by_id(candidate_id: str) -> FullCorpusCandidate:
    for candidate in FULL_CORPUS_CANDIDATES:
        if candidate.candidate_id == candidate_id:
            return candidate
    raise ValueError(f"Unknown Phase 4 candidate: {candidate_id}")


def build_record_path(candidate: FullCorpusCandidate) -> Path:
    return BUILD_RECORD_ROOT / f"{candidate.collection_name}.json"


def _phase4_settings() -> dict[str, Any]:
    settings = load_settings()
    database = settings.get("vector_database", {})
    if database.get("url") != "http://localhost:6333":
        raise ValueError("Phase 4 requires the pinned local Hue Qdrant URL")
    if database.get("timeout") != QDRANT_TIMEOUT:
        raise ValueError("Phase 4 Qdrant timeout must remain 30 seconds")
    return settings


def prepare_full_corpus_input() -> PreparedFullCorpus:
    settings = _phase4_settings()
    root, relative_paths = discover_full_corpus_files(settings)
    sources = compute_corpus_state(root, relative_paths)
    source_state_bytes = json.dumps(
        sources, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    source_state_sha = hashlib.sha256(source_state_bytes).hexdigest()
    chunks, errors = chunk_full_corpus(settings)
    if errors:
        raise ValueError(f"Fresh full-corpus chunking failed: {errors}")
    if len(relative_paths) != EXPECTED_FILE_COUNT:
        raise ValueError(f"File count {len(relative_paths)} != {EXPECTED_FILE_COUNT}")
    if len(chunks) != EXPECTED_CHUNK_COUNT:
        raise ValueError(f"Chunk count {len(chunks)} != {EXPECTED_CHUNK_COUNT}")
    corpus_identity = compute_corpus_identity(chunks)
    if corpus_identity != EXPECTED_CORPUS_IDENTITY:
        raise ValueError(f"Corpus identity mismatch: {corpus_identity}")
    sparse_bytes = SPARSE_STATE_PATH.read_bytes()
    sparse_sha = hashlib.sha256(sparse_bytes).hexdigest()
    if sparse_sha != EXPECTED_SPARSE_SHA256:
        raise ValueError(f"Sparse state SHA-256 mismatch: {sparse_sha}")
    sparse_state = load_sparse_state(SPARSE_STATE_PATH)
    if (
        sparse_state.corpus_identity != corpus_identity
        or sparse_state.document_count != EXPECTED_CHUNK_COUNT
        or len(sparse_state.vocabulary) != 5662
        or sparse_state.k1 != 1.5
        or sparse_state.b != 0.75
    ):
        raise ValueError("Sparse state identity/shape/constants mismatch")
    evidence = json.loads(PHASE3_EVIDENCE_PATH.read_text(encoding="utf-8"))
    if evidence.get("status") != "PASS":
        raise ValueError("Phase 3 evidence status is not PASS")
    if evidence.get("corpus", {}).get("corpus_identity") != corpus_identity:
        raise ValueError("Phase 3 evidence corpus identity mismatch")
    if evidence.get("sparse", {}).get("sha256") != sparse_sha:
        raise ValueError("Phase 3 evidence sparse SHA-256 mismatch")
    sample_ids = tuple(item["chunk_id"] for item in evidence.get("sample", []))
    if len(sample_ids) != 12 or len(set(sample_ids)) != 12:
        raise ValueError("Phase 3 deterministic sample must contain 12 unique IDs")
    chunk_ids = {chunk.chunk_id for chunk in chunks}
    if any(sample_id not in chunk_ids for sample_id in sample_ids):
        raise ValueError("Phase 3 sample ID is absent from fresh chunks")
    for candidate in FULL_CORPUS_CANDIDATES:
        model = evidence.get("models", {}).get(candidate.candidate_id, {})
        spec = candidate.dense_spec
        observed = (
            model.get("model_id"), model.get("revision"), model.get("dimension"),
            model.get("max_tokens"), model.get("input_contract"),
            model.get("device"), model.get("dtype"), model.get("batch_size"),
        )
        expected = (
            spec.model_id, spec.revision, spec.dimension,
            spec.max_tokens, spec.input_contract,
            spec.device, spec.dtype, spec.batch_size,
        )
        if observed != expected:
            raise ValueError(f"Phase 3 model evidence mismatch for {spec.key}")
    return PreparedFullCorpus(
        chunks=chunks,
        sources=sources,
        source_state_sha256=source_state_sha,
        sparse_state=sparse_state,
        sparse_state_sha256=sparse_sha,
        sample_chunk_ids=sample_ids,
    )


def _linux_memory_bytes() -> dict[str, int]:
    values: dict[str, int] = {}
    for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
        key, raw = line.split(":", 1)
        if key in {"MemTotal", "MemAvailable", "SwapTotal", "SwapFree"}:
            values[key] = int(raw.strip().split()[0]) * 1024
    return values


def _resource_evidence() -> dict[str, Any]:
    disk = shutil.disk_usage(REPOSITORY_ROOT)
    gpu: dict[str, Any] = {
        "cuda_available": torch.cuda.is_available(),
        "torch_version": torch.__version__,
        "torch_cuda_version": torch.version.cuda,
    }
    if torch.cuda.is_available():
        gpu.update({
            "device_name": torch.cuda.get_device_name(0),
            "total_vram_bytes": torch.cuda.get_device_properties(0).total_memory,
        })
    return {
        "memory": _linux_memory_bytes(),
        "disk": {"total_bytes": disk.total, "free_bytes": disk.free},
        "gpu": gpu,
    }


def run_read_only_preflight() -> tuple[dict[str, Any], int]:
    prepared = prepare_full_corpus_input()
    settings = _phase4_settings()
    client = client_from_settings(settings)
    try:
        version = client.info()
        targets = []
        for candidate in FULL_CORPUS_CANDIDATES:
            observation = inspect_full_corpus_target(
                client, candidate.collection_name, candidate.dense_spec.dimension,
                build_record_path(candidate), QDRANT_TIMEOUT,
            )
            targets.append({
                "candidate_id": candidate.candidate_id,
                "collection_name": candidate.collection_name,
                "dimension": candidate.dense_spec.dimension,
                "state": observation.state,
                "point_count": observation.point_count,
                "build_record_exists": observation.build_record_exists,
                "blockers": list(observation.blockers),
            })
    finally:
        client.close()
    ready = all(not target["blockers"] for target in targets)
    evidence = {
        "schema_version": "phase_4_qdrant_preflight:v1",
        "status": "READY" if ready else "BLOCKED",
        "corpus": {
            "file_count": len(prepared.sources),
            "chunk_count": len(prepared.chunks),
            "identity": EXPECTED_CORPUS_IDENTITY,
            "source_state_sha256": prepared.source_state_sha256,
        },
        "sparse": {
            "state_sha256": prepared.sparse_state_sha256,
            "vocabulary_size": len(prepared.sparse_state.vocabulary),
        },
        "qdrant": {
            "server_version": version.version,
            "client_version": importlib.metadata.version("qdrant-client"),
        },
        "resources": _resource_evidence(),
        "targets": targets,
        "build_commands": [
            f"python -m backend.ingestion.full_corpus_pipeline build --candidate {item.candidate_id}"
            for item in FULL_CORPUS_CANDIDATES
        ],
    }
    return evidence, 0 if ready else 2


def build_candidate(candidate_id: str) -> dict[str, Any]:
    candidate = candidate_by_id(candidate_id)
    prepared = prepare_full_corpus_input()
    approved_preflight = json.loads(
        PREFLIGHT_OUTPUT_PATH.read_text(encoding="utf-8")
    )
    if approved_preflight.get("status") != "READY":
        raise ValueError("Initial Phase 4 preflight status is not READY")
    preflight_corpus = approved_preflight.get("corpus", {})
    if (
        preflight_corpus.get("identity") != EXPECTED_CORPUS_IDENTITY
        or preflight_corpus.get("source_state_sha256")
        != prepared.source_state_sha256
        or approved_preflight.get("sparse", {}).get("state_sha256")
        != prepared.sparse_state_sha256
    ):
        raise ValueError("Fresh corpus/sparse state differs from approved preflight")
    settings = _phase4_settings()
    client = client_from_settings(settings)
    record_path = build_record_path(candidate)
    first = inspect_full_corpus_target(
        client, candidate.collection_name, candidate.dense_spec.dimension,
        record_path, QDRANT_TIMEOUT,
    )
    require_fresh_full_corpus_target(first)
    runner: FullCorpusDenseRunner | None = None
    completed = 0
    resources_before = _resource_evidence()
    try:
        snapshot = resolve_snapshot(candidate.dense_spec, allow_download=False)
        runner = FullCorpusDenseRunner(candidate.dense_spec, snapshot)
        runner.load()
        runtime = runner.observed_runtime_state()
        if candidate.dense_spec.device == "cuda":
            torch.cuda.reset_peak_memory_stats()
        texts = [chunk.search_text for chunk in prepared.chunks]
        dense = runner.embed_documents_matrix(texts)
        resources_after_encode = _resource_evidence()
        if candidate.dense_spec.device == "cuda":
            resources_after_encode["gpu"]["peak_allocated_bytes"] = (
                torch.cuda.max_memory_allocated()
            )
        vocabulary_index = build_vocabulary_index(prepared.sparse_state)
        validate_full_corpus_point_inputs(
            prepared.chunks, dense, candidate.dense_spec.dimension,
            prepared.sparse_state, vocabulary_index,
        )
        root, relative_paths = discover_full_corpus_files(settings)
        if compute_corpus_state(root, relative_paths) != prepared.sources:
            raise ValueError("Canonical source hashes changed during dense encoding")
        second = inspect_full_corpus_target(
            client, candidate.collection_name, candidate.dense_spec.dimension,
            record_path, QDRANT_TIMEOUT,
        )
        require_fresh_full_corpus_target(second)
        if second != first:
            raise ValueError("Target/build-record state changed after preflight")
        if second.state == "absent":
            create_full_corpus_collection(
                client, candidate.collection_name,
                candidate.dense_spec.dimension, QDRANT_TIMEOUT,
            )
            created = inspect_full_corpus_target(
                client, candidate.collection_name, candidate.dense_spec.dimension,
                record_path, QDRANT_TIMEOUT,
            )
            require_fresh_full_corpus_target(created)
            if created.state != "empty":
                raise ValueError("New full-corpus target is not schema-valid and empty")
        for start in range(0, len(prepared.chunks), 64):
            stop = min(start + 64, len(prepared.chunks))
            points = build_full_corpus_point_batch(
                prepared.chunks[start:stop], dense[start:stop],
                candidate.dense_spec.dimension, prepared.sparse_state,
                vocabulary_index,
            )
            try:
                completed += upsert_full_corpus_batch(
                    client, candidate.collection_name, points, QDRANT_TIMEOUT
                )
            except Exception:
                observed = client.count(
                    candidate.collection_name, exact=True, timeout=QDRANT_TIMEOUT
                ).count
                logging.exception(
                    "Phase 4 upsert failed candidate=%s completed=%d observed=%d",
                    candidate.candidate_id, completed, observed,
                )
                raise
        verification = verify_full_corpus_collection(
            client, candidate.collection_name, candidate.dense_spec.dimension,
            prepared.chunks, prepared.sample_chunk_ids, QDRANT_TIMEOUT,
        )
        record = make_full_corpus_build_record(
            collection_name=candidate.collection_name,
            candidate_id=candidate.candidate_id,
            model_id=candidate.dense_spec.model_id,
            revision=candidate.dense_spec.revision,
            dimension=candidate.dense_spec.dimension,
            corpus_identity=EXPECTED_CORPUS_IDENTITY,
            sources=prepared.sources,
            sparse_state=prepared.sparse_state,
            sparse_state_sha256=prepared.sparse_state_sha256,
        )
        record_sha = write_final_full_corpus_build_record(record, record_path)
        norms = np.linalg.norm(dense.astype(np.float64, copy=False), axis=1)
        return {
            "candidate_id": candidate.candidate_id,
            "collection_name": candidate.collection_name,
            "model_id": candidate.dense_spec.model_id,
            "revision": candidate.dense_spec.revision,
            "runtime": runtime,
            "matrix_shape": list(dense.shape),
            "matrix_dtype": str(dense.dtype),
            "norm_min": float(norms.min()),
            "norm_max": float(norms.max()),
            "corpus_identity": EXPECTED_CORPUS_IDENTITY,
            "source_state_sha256": prepared.source_state_sha256,
            "sparse_state_sha256": prepared.sparse_state_sha256,
            "resources_before": resources_before,
            "resources_after_encode": resources_after_encode,
            "completed_upserts": completed,
            "verification": verification,
            "build_record_path": str(record_path.relative_to(REPOSITORY_ROOT)),
            "build_record_sha256": record_sha,
        }
    finally:
        if runner is not None:
            runner.close()
        client.close()


def _write_preflight_output(evidence: dict[str, Any], output: Path) -> None:
    data = (
        json.dumps(evidence, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f"{output.name}.tmp.{uuid.uuid4().hex}")
    try:
        temporary.write_bytes(data)
        temporary.replace(output)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description="Full-corpus Phase 4 ingestion")
    subparsers = parser.add_subparsers(dest="command", required=True)
    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--output", type=Path)
    build = subparsers.add_parser("build")
    build.add_argument(
        "--candidate",
        required=True,
        choices=[item.candidate_id for item in FULL_CORPUS_CANDIDATES],
    )
    args = parser.parse_args()
    if args.command == "preflight":
        evidence, exit_code = run_read_only_preflight()
        if args.output is not None:
            _write_preflight_output(evidence, args.output.resolve())
        print(json.dumps(evidence, ensure_ascii=False, sort_keys=True, indent=2))
        raise SystemExit(exit_code)
    summary = build_candidate(args.candidate)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
