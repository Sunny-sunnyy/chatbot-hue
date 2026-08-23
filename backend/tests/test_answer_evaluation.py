"""Pure contract tests for answer generation and LLM-as-judge helpers.

Live provider calls are validated separately inside the bounded paid run;
these tests cover the deterministic rubric, retry and record-shape logic.
"""

import pytest

from evaluation.answer_eval import (
    JUDGE_DIMENSIONS,
    build_judge_input,
    entity_record,
    generation_record,
    is_retryable,
    judge_passes,
    judge_record,
    validate_judge_scores,
)


def test_judge_passes_uses_accuracy_groundedness_mean_and_floor():
    """Pass requires accuracy>=4, groundedness>=4, mean>=4 and no dimension <3."""
    assert judge_passes({"accuracy": 5, "completeness": 4, "relevance": 4, "groundedness": 4})
    assert judge_passes({"accuracy": 4, "completeness": 3, "relevance": 4, "groundedness": 5})
    # mean of (4,3,3,4)=3.5 <4 -> fail despite floors satisfied.
    assert not judge_passes({"accuracy": 5, "completeness": 3, "relevance": 3, "groundedness": 4})
    # groundedness floor
    assert not judge_passes({"accuracy": 5, "completeness": 5, "relevance": 5, "groundedness": 3})
    # accuracy floor
    assert not judge_passes({"accuracy": 3, "completeness": 5, "relevance": 5, "groundedness": 5})
    # hard floor: any dimension below 3 fails even with high mean.
    assert not judge_passes({"accuracy": 5, "completeness": 2, "relevance": 5, "groundedness": 5})


def test_validate_judge_scores_accepts_full_scale():
    scores = validate_judge_scores({"accuracy": 5, "completeness": 1, "relevance": 3, "groundedness": 4})
    assert scores["accuracy"] == 5


def test_validate_judge_scores_rejects_out_of_range_and_missing():
    with pytest.raises(ValueError):
        validate_judge_scores({"accuracy": 6, "completeness": 4, "relevance": 4, "groundedness": 4})
    with pytest.raises(ValueError):
        validate_judge_scores({"accuracy": 3.2, "completeness": 4, "relevance": 4, "groundedness": 4})
    with pytest.raises(ValueError):
        validate_judge_scores({"accuracy": 4, "relevance": 4, "groundedness": 4})


def test_is_retryable_only_for_transient_failures():
    """One retry max, only timeout/transient/invalid-structured errors."""
    for error_type in ("timeout", "transient_network", "invalid_structured_output"):
        assert is_retryable(error_type)
    for error_type in ("low_judge_score", "provider_quota", "rate_limited", "unexpected"):
        assert not is_retryable(error_type)


def test_build_judge_input_only_contains_current_case():
    """Judge gets question/reference/answer and bounded evidence only."""
    payload = build_judge_input(
        question="Quán A ở đâu?",
        reference_answer="Quán A ở 123 đường X.",
        answer="Quán A ở 123 đường X.",
        evidence=[
            {"source": "foods/restaurants/quan a.md", "section": "Thông tin", "text": "Quán A ở 123 đường X."}
        ],
        rubric_version="v1",
    )
    assert payload["question"] == "Quán A ở đâu?"
    assert payload["reference_answer"] == "Quán A ở 123 đường X."
    assert payload["grounded_answer"] == "Quán A ở 123 đường X."
    assert payload["rubric_version"] == "v1"
    assert len(payload["evidence"]) == 1
    assert payload["evidence"][0]["source"] == "foods/restaurants/quan a.md"
    assert set(payload.keys()) <= {
        "question",
        "reference_answer",
        "grounded_answer",
        "evidence",
        "rubric_version",
    }


def test_entity_record_bounds_evidence_and_drops_scores():
    """Generation evidence records keep source labels and text, no rank noise."""
    rec = entity_record("foods/restaurants/quan a.md", "Thông tin", "text đoạn", 0.9)
    assert rec == {
        "source": "foods/restaurants/quan a.md",
        "section": "Thông tin",
        "text": "text đoạn",
        "score": 0.9,
    }


def test_generation_and_judge_record_shapes():
    gen = generation_record(
        run_id="answers-20260822-142157-hybrid_rerank-cf601f16",
        timestamp_utc_plus_7="2026-08-22 14:21:57",
        dataset_path="d",
        dataset_checksum="c",
        config_checksum="c2",
        case_id="foods-0001",
        category="direct_fact",
        question="q",
        reference_answer="ref",
        answer="ans",
        used_sources=["s1"],
        used_evidence=[entity_record("f.md", "Tóm tắt", "txt", 0.5)],
        answer_model="gpt-5.4-nano",
        prompt_hash="e6fbcef32bbc083c",
        latency_ms=800,
        usage_tokens={"input": 100, "output": 50},
        cost_usd=0.0001,
    )
    assert gen["status"] == "complete"
    assert gen["answer_model"] == "gpt-5.4-nano"
    assert gen["prompt_hash"] == "e6fbcef32bbc083c"
    assert gen["used_sources"] == ["s1"]
    assert gen["usage_tokens"] == {"input": 100, "output": 50}
    assert "system_prompt" not in gen

    judge = judge_record(
        run_id="answers-...-j",
        timestamp_utc_plus_7="t",
        case_id="foods-0001",
        category="direct_fact",
        generation_run_id="gens-1",
        rubric_version="v1",
        prompt_hash="4e45983e2a49d743",
        scores={"accuracy": 5, "completeness": 4, "relevance": 4, "groundedness": 4},
        feedback="Đúng địa chỉ chính xác.",
        judge_model="gpt-5.4-mini",
        latency_ms=900,
        usage_tokens={"input": 10, "output": 5},
        cost_usd=0.00005,
        attempts=1,
    )
    assert judge["generation_run_id"] == "gens-1"
    assert judge["prompt_hash"] == "4e45983e2a49d743"
    assert judge["scores"] == {
        "accuracy": 5,
        "completeness": 4,
        "relevance": 4,
        "groundedness": 4,
    }
    assert judge["status"] == "complete"
    assert set(judge["scores"]) == set(JUDGE_DIMENSIONS)
