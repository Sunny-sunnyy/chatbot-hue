"""Load application settings from config/settings.yaml."""
from pathlib import Path

import yaml


BACKEND_DIR = Path(__file__).resolve().parents[1]
SETTINGS_PATH = BACKEND_DIR / "config" / "settings.yaml"


def load_settings():
    """Load settings and reject an unknown active retrieval profile."""
    with SETTINGS_PATH.open() as file:
        settings = yaml.safe_load(file)
    active_profile = settings.get("active_profile")
    profiles = settings.get("profiles", {})
    if active_profile not in profiles:
        raise ValueError(
            f"Unknown active_profile: {active_profile!r}. "
            f"Valid profiles: {sorted(profiles)}"
        )
    if "full_corpus" in settings:
        validate_full_corpus_settings(settings["full_corpus"])
    return settings


def validate_full_corpus_settings(full_corpus: dict) -> None:
    """Validate full-corpus settings fail-closed."""
    if not isinstance(full_corpus, dict):
        raise ValueError("full_corpus configuration must be a dictionary")
    kb = full_corpus.get("knowledge_base")
    if not isinstance(kb, dict):
        raise ValueError("full_corpus.knowledge_base must be a dictionary")
    root_dir = kb.get("root_dir")
    if not root_dir or not isinstance(root_dir, str):
        raise ValueError("full_corpus.knowledge_base.root_dir must be a non-empty string")
    resolved_root = (BACKEND_DIR / root_dir).resolve()
    if not resolved_root.is_dir():
        raise ValueError(f"full_corpus knowledge base root does not exist: {resolved_root}")

    include_globs = kb.get("include_globs")
    if not isinstance(include_globs, list) or not include_globs:
        raise ValueError("full_corpus.knowledge_base.include_globs must be a non-empty list of strings")
    if not all(isinstance(g, str) and g.strip() for g in include_globs):
        raise ValueError("full_corpus.knowledge_base.include_globs elements must be non-empty strings")

    exclude_parts = kb.get("exclude_parts")
    if not isinstance(exclude_parts, list) or not exclude_parts:
        raise ValueError("full_corpus.knowledge_base.exclude_parts must be a non-empty list of strings")

    exclude_files = kb.get("exclude_files")
    if exclude_files is not None and not isinstance(exclude_files, list):
        raise ValueError("full_corpus.knowledge_base.exclude_files must be a list of strings")

    conditions_file = full_corpus.get("conditions_file")
    if not conditions_file or not isinstance(conditions_file, str):
        raise ValueError("full_corpus.conditions_file must be a non-empty string")
    resolved_cond = (BACKEND_DIR / conditions_file).resolve()
    if not resolved_cond.is_file():
        raise ValueError(f"full_corpus conditions file does not exist: {resolved_cond}")

    embedding_models = full_corpus.get("embedding_models")
    if not isinstance(embedding_models, list) or not embedding_models:
        raise ValueError("full_corpus.embedding_models must be a non-empty list")
    for m in embedding_models:
        if not isinstance(m, dict):
            raise ValueError("Each item in full_corpus.embedding_models must be a dictionary")
        if not m.get("id") or not isinstance(m["id"], str):
            raise ValueError("embedding_models item missing valid 'id' string")
        if not isinstance(m.get("max_tokens"), int) or m["max_tokens"] <= 0:
            raise ValueError("embedding_models item missing positive integer 'max_tokens'")
        if "prefix" not in m or not isinstance(m["prefix"], str):
            raise ValueError("embedding_models item missing string 'prefix'")
        if not isinstance(m.get("word_segment"), bool):
            raise ValueError("embedding_models item missing boolean 'word_segment'")


def get_full_corpus_settings(settings: dict | None = None) -> dict:
    """Return validated full_corpus settings dictionary."""
    if settings is None:
        settings = load_settings()
    full_corpus = settings.get("full_corpus")
    if not full_corpus:
        raise ValueError("full_corpus settings missing from configuration")
    validate_full_corpus_settings(full_corpus)
    return full_corpus
