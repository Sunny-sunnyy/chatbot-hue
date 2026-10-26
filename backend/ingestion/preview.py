"""Tokenizer offline cho phép kiểm giới hạn token của chunker (`full_corpus_chunker.get_default_tokenizer_checker`) và harness 8.1 G3.

CLI "Wave 1 preview" cũ (báo cáo phân bố đoạn toàn kho, ghi `reports/artifacts/`) đã gỡ ở đợt 3 rà code (B-04): phép kiểm "không đoạn nào
vượt token" giờ nằm trong chính chunker (B-11), nên build tự dừng.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from pyvi import ViTokenizer
from transformers import AutoTokenizer

from core.settings_loader import get_full_corpus_settings


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
