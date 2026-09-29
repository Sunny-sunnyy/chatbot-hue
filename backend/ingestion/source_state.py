"""Source state and LF normalization utilities for full-corpus RAG.

Handles strict UTF-8 reading, CRLF/CR to LF normalization, SHA-256 hashing,
deterministic file discovery, and build-record validation helpers.
Wave 1 constraint: Never write completion build records.
"""
from __future__ import annotations

from collections.abc import Mapping
import hashlib
import json
import os
from pathlib import Path
from typing import Any
import uuid

try:
    from backend.core.settings_loader import BACKEND_DIR, get_full_corpus_settings, load_settings
    from backend.embedding.sparse import SparseState
except ModuleNotFoundError:
    from core.settings_loader import BACKEND_DIR, get_full_corpus_settings, load_settings
    from embedding.sparse import SparseState


def normalize_lf(text: str) -> str:
    """Normalize CRLF and CR to LF once. Preserve all other characters."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def read_source_lf(file_path: Path | str) -> str:
    """Read a markdown file with strict UTF-8 and normalize CRLF/CR to LF."""
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as f:
        raw = f.read()
    return normalize_lf(raw)


def compute_source_hash(lf_text: str) -> str:
    """Compute SHA-256 hex digest of LF text encoded as UTF-8."""
    return hashlib.sha256(lf_text.encode("utf-8")).hexdigest()


def compute_file_hash(file_path: Path | str) -> str:
    """Read file with LF normalization and return SHA-256 hash."""
    return compute_source_hash(read_source_lf(file_path))


def discover_full_corpus_files(
    settings: dict[str, Any] | None = None,
) -> tuple[Path, list[str]]:
    """Discover curated Markdown files across the 5 domains deterministically.

    Returns:
        (resolved_root, sorted_relative_posix_paths)
    """
    fc_settings = get_full_corpus_settings(settings)
    kb = fc_settings["knowledge_base"]
    root = (BACKEND_DIR / kb["root_dir"]).resolve()
    exclude_parts = set(kb.get("exclude_parts", []))
    exclude_files = set(kb.get("exclude_files", []))

    discovered_rel_paths: set[str] = set()

    for glob_pattern in kb.get("include_globs", []):
        for full_path in root.glob(glob_pattern):
            if not full_path.is_file():
                continue
            try:
                rel_path = full_path.relative_to(root).as_posix()
            except ValueError:
                continue

            # Check exclude_parts
            rel_parts = set(Path(rel_path).parts)
            if any(part in exclude_parts for part in rel_parts):
                continue

            # Check exclude_files
            if rel_path in exclude_files:
                continue

            discovered_rel_paths.add(rel_path)

    sorted_rel_paths = sorted(discovered_rel_paths)
    return root, sorted_rel_paths


def compute_corpus_state(
    root: Path,
    rel_paths: list[str],
) -> dict[str, str]:
    """Compute mapping of relative path to SHA-256 hash of normalized LF text."""
    state: dict[str, str] = {}
    for rel in sorted(rel_paths):
        full_path = root / rel
        state[rel] = compute_file_hash(full_path)
    return state


def verify_build_record_freshness(
    current_state: dict[str, str],
    build_record: dict[str, Any],
) -> tuple[bool, list[str]]:
    """Verify that current corpus state matches the recorded build state.

    Returns (is_fresh, list_of_discrepancies).
    """
    recorded_sources = build_record.get("sources", {})
    if not isinstance(recorded_sources, dict):
        return False, ["Build record missing valid sources dictionary"]

    discrepancies = []
    current_keys = set(current_state.keys())
    recorded_keys = set(recorded_sources.keys())

    added = current_keys - recorded_keys
    if added:
        discrepancies.append(f"Added files: {sorted(added)}")

    deleted = recorded_keys - current_keys
    if deleted:
        discrepancies.append(f"Deleted files: {sorted(deleted)}")

    for common_key in sorted(current_keys & recorded_keys):
        if current_state[common_key] != recorded_sources[common_key]:
            discrepancies.append(
                f"Content changed: {common_key} "
                f"(current={current_state[common_key][:8]} vs recorded={recorded_sources[common_key][:8]})"
            )

    return len(discrepancies) == 0, discrepancies


FULL_CORPUS_BUILD_SCHEMA = "phase_4_full_corpus_build:v1"
FULL_CORPUS_BUILD_SCHEMA_V2 = "phase_4_full_corpus_build:v2"
FULL_CORPUS_PAYLOAD_SCHEMA_V2 = "full_corpus_qdrant_payload:v2"


def make_full_corpus_build_record(
    *,
    collection_name: str,
    candidate_id: str,
    model_id: str,
    revision: str,
    dimension: int,
    corpus_identity: str,
    sources: Mapping[str, str],
    sparse_state: SparseState,
    sparse_state_sha256: str,
) -> dict[str, Any]:
    if len(sources) != 205:
        raise ValueError(f"Source count {len(sources)} != expected 205")
    if sparse_state.corpus_identity != corpus_identity:
        raise ValueError("Sparse state corpus identity mismatch")
    if sparse_state.document_count != 8460 or len(sparse_state.vocabulary) != 5662:
        raise ValueError("Sparse state count or vocabulary mismatch")
    return {
        "schema_version": FULL_CORPUS_BUILD_SCHEMA,
        "status": "complete",
        "collection_name": collection_name,
        "representation": "A",
        "corpus": {
            "identity": corpus_identity,
            "file_count": 205,
            "chunk_count": 8460,
            "sources": dict(sorted(sources.items())),
        },
        "dense": {
            "candidate_id": candidate_id,
            "model_id": model_id,
            "revision": revision,
            "dimension": dimension,
        },
        "sparse": {
            "schema_version": sparse_state.schema_version,
            "state_sha256": sparse_state_sha256,
            "vocabulary_size": len(sparse_state.vocabulary),
        },
        "qdrant": {
            "dense_vector_name": "dense",
            "sparse_vector_name": "sparse",
            "distance": "cosine",
            "point_count": 8460,
        },
    }


def make_full_corpus_metadata_v2_build_record(
    *,
    collection_name: str,
    source_collection: str,
    source_build_record_sha256: str,
    candidate_id: str,
    model_id: str,
    revision: str,
    dimension: int,
    corpus_identity: str,
    sources: Mapping[str, str],
    sparse_state: SparseState,
    sparse_state_sha256: str,
) -> dict[str, Any]:
    if collection_name == source_collection:
        raise ValueError("source_collection must be distinct from collection_name")
    if not isinstance(source_build_record_sha256, str) or len(source_build_record_sha256) != 64:
        raise ValueError("source_build_record_sha256 must be a 64-character hex string")
    try:
        int(source_build_record_sha256, 16)
    except ValueError:
        raise ValueError("source_build_record_sha256 must be a valid hex string")

    v1_record = make_full_corpus_build_record(
        collection_name=collection_name,
        candidate_id=candidate_id,
        model_id=model_id,
        revision=revision,
        dimension=dimension,
        corpus_identity=corpus_identity,
        sources=sources,
        sparse_state=sparse_state,
        sparse_state_sha256=sparse_state_sha256,
    )

    return {
        "schema_version": FULL_CORPUS_BUILD_SCHEMA_V2,
        "status": v1_record["status"],
        "collection_name": collection_name,
        "representation": v1_record["representation"],
        "corpus": v1_record["corpus"],
        "dense": v1_record["dense"],
        "sparse": v1_record["sparse"],
        "qdrant": {
            **v1_record["qdrant"],
            "payload_schema_version": FULL_CORPUS_PAYLOAD_SCHEMA_V2,
        },
        "migration": {
            "mode": "copy_verified_vectors",
            "source_collection": source_collection,
            "source_build_record_sha256": source_build_record_sha256,
        },
    }


def serialize_full_corpus_build_record(record: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def write_final_full_corpus_build_record(
    record: Mapping[str, Any], path: Path
) -> str:
    if path.exists():
        raise FileExistsError(f"Final build record already exists: {path}")
    data = serialize_full_corpus_build_record(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{uuid.uuid4().hex}")
    try:
        temporary.write_bytes(data)
        try:
            os.link(temporary, path)
        except FileExistsError:
            raise FileExistsError(f"Final build record already exists: {path}") from None
    finally:
        if temporary.exists():
            temporary.unlink()
    return hashlib.sha256(data).hexdigest()


def verify_full_corpus_record_freshness(
    current_state: Mapping[str, str], record: Mapping[str, Any]
) -> tuple[bool, list[str]]:
    corpus = record.get("corpus")
    recorded = corpus.get("sources") if isinstance(corpus, dict) else None
    if not isinstance(recorded, dict):
        return False, ["Full-corpus build record missing corpus.sources mapping"]
    discrepancies: list[str] = []
    current_keys = set(current_state)
    recorded_keys = set(recorded)
    if current_keys - recorded_keys:
        discrepancies.append(f"Added files: {sorted(current_keys - recorded_keys)}")
    if recorded_keys - current_keys:
        discrepancies.append(f"Deleted files: {sorted(recorded_keys - current_keys)}")
    for path in sorted(current_keys & recorded_keys):
        if current_state[path] != recorded[path]:
            discrepancies.append(f"Content changed: {path}")
    return not discrepancies, discrepancies
