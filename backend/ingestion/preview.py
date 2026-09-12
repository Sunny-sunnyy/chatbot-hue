"""Full-corpus RAG Wave 1 preview CLI module.

Execution contract:
    uv run python -m backend.ingestion.preview --output reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json

Performs deterministic discovery, Markdown parsing, condition attachment,
source locator verification, representation A text construction, and
tokenizer limit verification across all approved dense candidates offline.
Fails closed if any blocking errors or oversized groups are found.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import sys
from typing import Any

from pyvi import ViTokenizer
from transformers import AutoTokenizer

try:
    from backend.core.schema import FullCorpusChunk
    from backend.core.settings_loader import BACKEND_DIR, get_full_corpus_settings, load_settings
    from backend.ingestion.chunking.full_corpus_chunker import (
        ConditionManager,
        chunk_document,
        chunk_full_corpus,
    )
    from backend.ingestion.chunking.markdown_blocks import parse_markdown_blocks
    from backend.ingestion.source_state import (
        discover_full_corpus_files,
        read_source_lf,
    )
except ModuleNotFoundError:
    from core.schema import FullCorpusChunk
    from core.settings_loader import BACKEND_DIR, get_full_corpus_settings, load_settings
    from ingestion.chunking.full_corpus_chunker import (
        ConditionManager,
        chunk_document,
        chunk_full_corpus,
    )
    from ingestion.chunking.markdown_blocks import parse_markdown_blocks
    from ingestion.source_state import (
        discover_full_corpus_files,
        read_source_lf,
    )


def resolve_local_model_path(model_id: str) -> Path:
    """Resolve local directory path for model snapshot without hardcoding absolute hashes."""
    direct = Path(model_id)
    if direct.is_dir():
        return direct

    hf_home = os.environ.get("HF_HOME")
    if hf_home:
        hub_dir = Path(hf_home) / "hub"
    else:
        hub_dir = Path(os.environ.get("HF_HUB_CACHE", Path.home() / ".cache" / "huggingface" / "hub"))

    repo_name = "models--" + model_id.replace("/", "--")
    repo_dir = hub_dir / repo_name
    snapshots_dir = repo_dir / "snapshots"
    if snapshots_dir.is_dir():
        snapshots = [s for s in snapshots_dir.iterdir() if s.is_dir()]
        if snapshots:
            return sorted(snapshots)[-1]

    raise FileNotFoundError(f"No local snapshot found for {model_id} in {hub_dir}")


def load_tokenizers(settings: dict[str, Any] | None = None) -> tuple[dict[str, Any], list[str]]:
    """Load candidate tokenizers offline from local cache based on settings."""
    fc_settings = get_full_corpus_settings(settings)
    models_cfg = fc_settings.get("embedding_models", [])

    tokenizers: dict[str, Any] = {}
    errors: list[str] = []

    for spec in models_cfg:
        model_id = spec["id"]
        try:
            local_path = resolve_local_model_path(model_id)
            tok = AutoTokenizer.from_pretrained(str(local_path), local_files_only=True)
            tokenizers[model_id] = tok
        except Exception as e:
            errors.append(f"Failed to load tokenizer offline for {model_id}: {e}")

    return tokenizers, errors


def count_tokens_for_chunk(
    text: str,
    tokenizers: dict[str, Any],
    models_cfg: list[dict[str, Any]],
) -> dict[str, int]:
    """Count tokens across all configured models with truncation=False."""
    counts: dict[str, int] = {}
    for spec in models_cfg:
        mid = spec["id"]
        tok = tokenizers.get(mid)
        if tok is None:
            counts[mid] = -1
            continue

        prep_text = text
        if spec.get("word_segment", False):
            prep_text = ViTokenizer.tokenize(prep_text)
        if spec.get("prefix"):
            prep_text = spec["prefix"] + prep_text

        input_ids = tok(prep_text, truncation=False)["input_ids"]
        counts[mid] = len(input_ids)

    return counts


def partition_for_source(source: str) -> str:
    """Map KB-relative source path to one of the seven P7 partitions."""
    if source.startswith("travel/places/"):
        return "travel_places"
    if source.startswith("travel/services/"):
        return "travel_services"
    if source.startswith("travel/tickets/"):
        return "travel_tickets"
    return source.split("/")[0]


def generate_preview(
    output_path: Path | str,
    settings: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], int]:
    """Generate deterministic preview artifact and return (artifact_dict, exit_code)."""
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    if settings is None:
        settings = load_settings()

    fc_settings = get_full_corpus_settings(settings)
    models_cfg = fc_settings["embedding_models"]
    cond_mgr = ConditionManager(settings=settings)

    tokenizers, tok_errors = load_tokenizers(settings)
    blocking_errors: list[str] = list(tok_errors)

    def is_fits_tokenizer_fn(search_text: str) -> bool:
        if tok_errors:
            return False  # Fail-closed
        for spec in models_cfg:
            mid = spec["id"]
            tok = tokenizers.get(mid)
            if not tok:
                return False
            prep = search_text
            if spec.get("word_segment", False):
                prep = ViTokenizer.tokenize(prep)
            if spec.get("prefix"):
                prep = spec["prefix"] + prep
            ids = tok(prep, truncation=False)["input_ids"]
            if len(ids) > spec["max_tokens"]:
                return False
        return True

    # Discover files
    try:
        root, files = discover_full_corpus_files(settings)
    except Exception as e:
        blocking_errors.append(f"Discovery error: {e}")
        root = Path(".")
        files = []

    # Chunk corpus
    chunks: list[FullCorpusChunk] = []
    if not tok_errors:
        try:
            chunks, chunk_errors = chunk_full_corpus(
                settings=settings,
                is_fits_tokenizer_fn=is_fits_tokenizer_fn,
                condition_manager=cond_mgr,
            )
            blocking_errors.extend(chunk_errors)
        except Exception as e:
            blocking_errors.append(f"Chunking failed: {e}")

    # Inspect all chunks for tokenizer limits and oversized groups
    oversized_groups: list[dict[str, Any]] = []
    max_observed_tokens: dict[str, int] = {s["id"]: 0 for s in models_cfg}

    for ch in chunks:
        if tokenizers:
            counts = count_tokens_for_chunk(ch.search_text, tokenizers, models_cfg)
            exceeded = []
            for spec in models_cfg:
                mid = spec["id"]
                c = counts.get(mid, 0)
                max_observed_tokens[mid] = max(max_observed_tokens[mid], c)
                if c > spec["max_tokens"]:
                    exceeded.append(mid)

            if exceeded:
                group_entry = {
                    "chunk_id": ch.chunk_id,
                    "source": ch.source,
                    "heading_path": list(ch.heading_path),
                    "character_count": len(ch.search_text),
                    "tokens": counts,
                    "limits": {s["id"]: s["max_tokens"] for s in models_cfg},
                    "exceeded_models": exceeded,
                }
                oversized_groups.append(group_entry)
                blocking_errors.append(
                    f"Oversized group: {ch.chunk_id} exceeds limits on {exceeded} "
                    f"(tokens={counts})"
                )

    # Domain breakdown (5 domains)
    domain_files: Counter[str] = Counter()
    domain_chunks: Counter[str] = Counter()
    for f in files:
        domain = f.split("/")[0]
        domain_files[domain] += 1
    for ch in chunks:
        domain = ch.source.split("/")[0]
        domain_chunks[domain] += 1

    all_domains = sorted(set(domain_files.keys()) | set(domain_chunks.keys()))
    domain_breakdown: dict[str, dict[str, int]] = {}
    for d in all_domains:
        domain_breakdown[d] = {
            "file_count": domain_files[d],
            "chunk_count": domain_chunks[d],
        }

    # P7 breakdown (7 partitions)
    p7_files: Counter[str] = Counter()
    p7_chunks: Counter[str] = Counter()
    for f in files:
        p7_files[partition_for_source(f)] += 1
    for ch in chunks:
        p7_chunks[partition_for_source(ch.source)] += 1

    canonical_p7_order = [
        "foods",
        "heritages",
        "festivals",
        "performing_arts",
        "travel_places",
        "travel_services",
        "travel_tickets",
    ]
    p7_breakdown: dict[str, dict[str, int]] = {}
    for p in canonical_p7_order:
        p7_breakdown[p] = {
            "file_count": p7_files[p],
            "chunk_count": p7_chunks[p],
        }

    # Tokenizer limits reporting
    tok_limits_report: dict[str, dict[str, Any]] = {}
    for spec in models_cfg:
        mid = spec["id"]
        tok_limits_report[mid] = {
            "max_tokens": spec["max_tokens"],
            "prefix": spec.get("prefix", ""),
            "max_observed_tokens": max_observed_tokens.get(mid, 0),
        }

    # Overall status
    non_oversized_errors = [e for e in blocking_errors if not e.startswith("Oversized group:")]
    if oversized_groups and not non_oversized_errors:
        status = "BLOCKED_OVERSIZED_GROUP"
        exit_code = 1
    elif non_oversized_errors or blocking_errors:
        status = "BLOCKED_ERRORS"
        exit_code = 1
    else:
        status = "PASS"
        exit_code = 0

    artifact: dict[str, Any] = {
        "schema_version": "1.0.0",
        "status": status,
        "summary": {
            "total_files": len(files),
            "total_chunks": len(chunks),
            "condition_rules_count": len(cond_mgr.rules),
            "blocking_errors_count": len(blocking_errors),
            "oversized_groups_count": len(oversized_groups),
        },
        "domain_breakdown": domain_breakdown,
        "p7_breakdown": p7_breakdown,
        "tokenizer_limits": tok_limits_report,
        "oversized_groups": oversized_groups,
        "errors": blocking_errors,
        "sources": files,
    }

    # Write byte-deterministic JSON artifact (no dynamic timestamp, fixed indentation)
    artifact_json = json.dumps(artifact, indent=2, ensure_ascii=False) + "\n"
    out_file.write_text(artifact_json, encoding="utf-8")

    return artifact, exit_code


def main() -> None:
    parser = argparse.ArgumentParser(description="Full-corpus RAG Wave 1 preview generator")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json",
        help="Destination path for preview artifact JSON",
    )
    args = parser.parse_args()

    print(f"Generating full-corpus Wave 1 preview to: {args.output}")
    artifact, exit_code = generate_preview(args.output)

    summary = artifact["summary"]
    print(f"Status: {artifact['status']}")
    print(f"Total files: {summary['total_files']}")
    print(f"Total chunks: {summary['total_chunks']}")
    print(f"Blocking errors: {summary['blocking_errors_count']}")
    print(f"Oversized groups: {summary['oversized_groups_count']}")

    if exit_code != 0:
        print("\n--- Blocking Errors / Oversized Groups ---")
        for err in artifact["errors"]:
            print(f"  [ERROR] {err}")
        print("\nIngestion blocked fail-closed. Exiting with code 1.")
        sys.exit(1)
    else:
        print("\nPreview PASS with zero blocking errors. Exiting with code 0.")
        sys.exit(0)


if __name__ == "__main__":
    main()
