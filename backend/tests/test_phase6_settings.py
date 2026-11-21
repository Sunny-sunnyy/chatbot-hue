import os
import pytest

from core.settings_loader import load_settings


def test_phase6_settings_are_exact():
    settings = load_settings()
    assert settings["full_corpus_runtime"] == {
        "candidate_id": "e5-small-384",
        "retrieval_treatment": "dense_bm25_rrf",
        "reranker": "none",
    }
    # `provider` là công tắc đổi qua / đổi về model viết (21/11/2026) ⇒ không khoá giá trị ở đây; mọi dòng còn lại vẫn khoá đúng từng chữ
    assert settings["full_corpus_generation"].pop("provider") in ("openai", "bedrock")
    assert settings["full_corpus_generation"] == {
        "model": "gpt-6-luna",
        "api_key_env": "OPENAI_API_KEY",
        "token_encoding": "o200k_base",
        "timeout_seconds": 45,
        "max_context_documents": 10,
        "bedrock": {
            "model": "global.anthropic.claude-sonnet-5-5",
            "region": "ap-southeast-1",
            "max_tokens": 128000,
            "reasoning_default": "low",
            "creds_file_env": "HUE_BEDROCK_CREDS_FILE",
        },
    }
    forbidden_keys = {
        "temperature",
        "top_p",
        "reasoning_effort",
        "verbosity",
        "fallback",
        "retry",
        "require_parameters",
    }
    for key in forbidden_keys:
        assert key not in settings["full_corpus_generation"]


def test_phase6_errors_are_typed():
    from core.schema import CitationIntegrityError

    assert issubclass(CitationIntegrityError, RuntimeError)


def test_openai_tokenizer_constants_and_loading():
    from llm.openai_tokenizer import (
        OPENAI_GENERATION_MODEL,
        OPENAI_TOKEN_ENCODING,
        load_openai_tokenizer,
    )

    assert OPENAI_GENERATION_MODEL == "gpt-6-luna"
    assert OPENAI_TOKEN_ENCODING == "o200k_base"

    tokenizer = load_openai_tokenizer()
    tokens = tokenizer.encode("Huế")
    assert isinstance(tokens, list)
    assert len(tokens) > 0

    # Ensure caching
    assert load_openai_tokenizer() is tokenizer


def test_openai_api_key_exists_without_leaking():
    key = os.getenv("OPENAI_API_KEY", "").strip()
    assert bool(key)


def test_load_settings_deferred_private_paths():
    settings = load_settings(validate_private_paths=False)
    assert "full_corpus_generation" in settings
