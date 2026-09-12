"""Source state and LF normalization utilities for full-corpus RAG.

Handles strict UTF-8 reading, CRLF/CR to LF normalization, SHA-256 hashing,
deterministic file discovery, and build-record validation helpers.
Wave 1 constraint: Never write completion build records.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

try:
    from backend.core.settings_loader import BACKEND_DIR, get_full_corpus_settings, load_settings
except ModuleNotFoundError:
    from core.settings_loader import BACKEND_DIR, get_full_corpus_settings, load_settings


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
