from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
import hashlib
import json
import logging
from pathlib import Path
from typing import Any

import numpy as np

from backend.core.schema import FullCorpusChunk, domain_for_source
from backend.core.settings_loader import load_settings
from backend.embedding.full_corpus import (
    DENSE_MODEL_SPECS,
    DenseModelSpec,
    OpenRouterDenseRunner,
    create_dense_runner,
)
from backend.embedding.sparse import (
    SparseState,
    build_vocabulary_index,
    compute_corpus_identity,
    fit_sparse_state,
    serialize_sparse_state,
    write_sparse_state,
)
from backend.ingestion.chunking.full_corpus_chunker import chunk_full_corpus
from backend.ingestion.source_state import (
    compute_corpus_state,
    discover_full_corpus_files,
    make_full_corpus_build_record,
    write_final_full_corpus_build_record,
)
from backend.vectorstore.points import (
    FULL_CORPUS_BATCH_SIZE,
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
BUILD_RECORD_ROOT = REPOSITORY_ROOT / "data/full_corpus_builds"
# Sparse state dùng chung cho mọi collection build trên cùng corpus.
SPARSE_STATE_PATH = BUILD_RECORD_ROOT / "full_corpus_sparse_state.json"
QDRANT_TIMEOUT = 30


@dataclass(frozen=True)
class FullCorpusCandidate:
    candidate_id: str
    collection_name: str
    dense_spec: DenseModelSpec


_COLLECTION_BY_CANDIDATE = {
    "e5-small-384": "hue_full_corpus_7a2_e5_small_384",
    "qwen3-embedding-8b-4096": "hue_full_corpus_7a2_qwen3_8b_4096",
}

FULL_CORPUS_CANDIDATES = tuple(
    FullCorpusCandidate(spec.key, _COLLECTION_BY_CANDIDATE[spec.key], spec)
    for spec in DENSE_MODEL_SPECS
)


@dataclass(frozen=True)
class PreparedFullCorpus:
    chunks: list[FullCorpusChunk]
    sources: dict[str, str]
    corpus_identity: str
    sparse_state: SparseState


def candidate_by_id(candidate_id: str) -> FullCorpusCandidate:
    for candidate in FULL_CORPUS_CANDIDATES:
        if candidate.candidate_id == candidate_id:
            return candidate
    raise ValueError(f"Unknown full-corpus candidate: {candidate_id}")


def build_record_path(candidate: FullCorpusCandidate) -> Path:
    return BUILD_RECORD_ROOT / f"{candidate.collection_name}.json"


def _phase4_settings() -> dict[str, Any]:
    settings = load_settings()
    database = settings.get("vector_database", {})
    if database.get("url") != "http://localhost:6335":
        raise ValueError("Full-corpus build requires the pinned local Hue Qdrant URL")
    if database.get("timeout") != QDRANT_TIMEOUT:
        raise ValueError("Full-corpus Qdrant timeout must remain 30 seconds")
    return settings


def prepare_full_corpus_input(
    *, embedding_models: list[dict[str, Any]] | None = None,
) -> PreparedFullCorpus:
    """Đọc corpus hiện tại: discover → hash source → chunk → identity → sparse state.

    embedding_models: danh sách tokenizer chunker kiểm giới hạn; None = `full_corpus.embedding_models`
    trong settings.yaml (harness Phase 8.1 dùng để thử bỏ bớt tokenizer).
    """
    settings = _phase4_settings()
    if embedding_models is not None:
        settings = {
            **settings,
            "full_corpus": {**settings["full_corpus"], "embedding_models": list(embedding_models)},
        }
    root, relative_paths = discover_full_corpus_files(settings)
    sources = compute_corpus_state(root, relative_paths)
    chunks, errors = chunk_full_corpus(settings)
    if errors:
        raise ValueError(f"Fresh full-corpus chunking failed: {errors}")
    return PreparedFullCorpus(
        chunks=chunks,
        sources=sources,
        corpus_identity=compute_corpus_identity(chunks),
        sparse_state=fit_sparse_state(chunks),
    )


def _write_or_check_sparse_state(sparse_state: SparseState, sparse_state_path: Path) -> str:
    """Ghi sparse state nếu chưa có; nếu đã có thì phải byte-identical với lần build này."""
    data = serialize_sparse_state(sparse_state)
    if sparse_state_path.exists():
        if sparse_state_path.read_bytes() != data:
            raise ValueError(
                f"Existing sparse state differs from current corpus: {sparse_state_path.name}"
            )
        return hashlib.sha256(data).hexdigest()
    return write_sparse_state(sparse_state, sparse_state_path)


def build_candidate(
    candidate_id: str,
    *,
    collection_name: str | None = None,
    sparse_state_path: Path = SPARSE_STATE_PATH,
    record_path: Path | None = None,
    embedding_models: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build một collection mới cho candidate từ corpus hiện tại; lỗi ở bước nào cũng raise.

    Không ghi đè collection/record có sẵn, không retry, không resume.
    Tham số keyword chỉ để harness Phase 8.1 build biến thể vào collection/sparse state/build record
    riêng; mặc định = collection runtime của candidate, sparse state chung, record cạnh nó.
    """
    candidate = candidate_by_id(candidate_id)
    if collection_name is not None:
        candidate = replace(candidate, collection_name=collection_name)
    spec = candidate.dense_spec
    prepared = prepare_full_corpus_input(embedding_models=embedding_models)
    sparse_sha = _write_or_check_sparse_state(prepared.sparse_state, sparse_state_path)
    # Mẫu kiểm vector sau upsert: chunk đầu tiên của mỗi domain, theo thứ tự chunker.
    first_chunk_by_domain: dict[str, str] = {}
    for chunk in prepared.chunks:
        first_chunk_by_domain.setdefault(domain_for_source(chunk.source), chunk.chunk_id)
    sample_chunk_ids = tuple(first_chunk_by_domain.values())

    settings = _phase4_settings()
    client = client_from_settings(settings)
    if record_path is None:
        record_path = build_record_path(candidate)
    runner = None
    try:
        target = inspect_full_corpus_target(
            client, candidate.collection_name, spec.dimension, record_path, QDRANT_TIMEOUT,
        )
        if require_fresh_full_corpus_target(target) != "absent":
            raise ValueError(f"Target collection already exists: {candidate.collection_name}")

        runner = create_dense_runner(spec)
        runner.load()
        dense = runner.embed_documents_matrix([chunk.search_text for chunk in prepared.chunks])

        vocabulary_index = build_vocabulary_index(prepared.sparse_state)
        validate_full_corpus_point_inputs(
            prepared.chunks, dense, spec.dimension, prepared.sparse_state, vocabulary_index,
        )
        root, relative_paths = discover_full_corpus_files(settings)
        if compute_corpus_state(root, relative_paths) != prepared.sources:
            raise ValueError("Canonical source hashes changed during dense encoding")

        create_full_corpus_collection(
            client, candidate.collection_name, spec.dimension, QDRANT_TIMEOUT,
        )
        for start in range(0, len(prepared.chunks), FULL_CORPUS_BATCH_SIZE):
            stop = start + FULL_CORPUS_BATCH_SIZE
            points = build_full_corpus_point_batch(
                prepared.chunks[start:stop], dense[start:stop], spec.dimension,
                prepared.sparse_state, vocabulary_index,
            )
            upsert_full_corpus_batch(client, candidate.collection_name, points, QDRANT_TIMEOUT)
        verification = verify_full_corpus_collection(
            client, candidate.collection_name, spec.dimension,
            prepared.chunks, sample_chunk_ids, QDRANT_TIMEOUT,
        )

        providers = (
            sorted(runner.providers_seen) if isinstance(runner, OpenRouterDenseRunner) else []
        )
        record = make_full_corpus_build_record(
            collection_name=candidate.collection_name,
            candidate_id=candidate.candidate_id,
            dense={
                "model_id": spec.model_id,
                "revision": spec.revision,
                "dimension": spec.dimension,
            },
            sources=prepared.sources,
            chunk_count=len(prepared.chunks),
            corpus_identity=prepared.corpus_identity,
            sparse_state=prepared.sparse_state,
            sparse_state_sha256=sparse_sha,
            providers=providers,
        )
        record_sha = write_final_full_corpus_build_record(record, record_path)
        norms = np.linalg.norm(dense.astype(np.float64, copy=False), axis=1)
        return {
            "candidate_id": candidate.candidate_id,
            "collection_name": candidate.collection_name,
            "model_id": spec.model_id,
            "provider": spec.provider,
            "providers_seen": providers,
            "file_count": len(prepared.sources),
            "chunk_count": len(prepared.chunks),
            "matrix_shape": list(dense.shape),
            "norm_min": float(norms.min()),
            "norm_max": float(norms.max()),
            "corpus_identity": prepared.corpus_identity,
            "sparse_state_sha256": sparse_sha,
            "sample_rule": "first chunk of each domain in chunker order",
            "sample_chunk_count": len(sample_chunk_ids),
            "verification": verification,
            "build_record_path": str(record_path.relative_to(REPOSITORY_ROOT)),
            "build_record_sha256": record_sha,
        }
    finally:
        if runner is not None:
            runner.close()
        client.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Full-corpus index build")
    subparsers = parser.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser("build")
    build.add_argument(
        "--candidate",
        required=True,
        choices=[item.candidate_id for item in FULL_CORPUS_CANDIDATES],
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    summary = build_candidate(args.candidate)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
