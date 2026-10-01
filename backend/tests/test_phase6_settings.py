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
    assert settings["full_corpus_generation"] == {
        "provider": "openai",
        "model": "gpt-5.4-nano",
        "api_key_env": "OPENAI_API_KEY",
        "token_encoding": "o200k_base",
        "answer_max_output_tokens": 2048,
        "representation_b_max_output_tokens": 256,
        "timeout_seconds": 45,
        "context_limit": 16384,
        "reserved_output_tokens": 2048,
        "safety_margin": 512,
        "max_context_documents": 5,
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
    from core.schema import CitationIntegrityError, ContextBudgetError

    assert issubclass(ContextBudgetError, RuntimeError)
    assert issubclass(CitationIntegrityError, RuntimeError)


def test_openai_tokenizer_constants_and_loading():
    from llm.openai_tokenizer import (
        OPENAI_GENERATION_MODEL,
        OPENAI_TOKEN_ENCODING,
        load_openai_tokenizer,
    )

    assert OPENAI_GENERATION_MODEL == "gpt-5.4-nano"
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
