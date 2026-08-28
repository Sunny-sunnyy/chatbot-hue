import asyncio
import math
from pathlib import Path

import pytest

from evaluation.eval import (
    build_services,
    calculate_mrr,
    calculate_ndcg,
    evaluate_answer,
    evaluate_retrieval,
)
from evaluation.evaluator import run_retrieval_ui
from evaluation.golden_dataset import (
    ALLOWED_CATEGORIES,
    CATEGORY_QUOTAS,
    SOURCE_TARGETS,
    V3_ALLOWED_COUNTS,
    document_is_relevant,
    load_golden,
    validate_full,
    validate_smoke,
    validate_v3_full,
    validate_v3_smoke,
)
from evaluation.test import load_tests

REPO = Path(__file__).resolve().parents[2]
SMALL_DATASET = REPO / "knowledge-base-hue/foods/evaluation/test2.jsonl"
FULL_DATASET = REPO / "knowledge-base-hue/foods/evaluation/tests.jsonl"
GOLDEN_V2 = REPO / "knowledge-base-hue/foods/evaluation/golden_v2.jsonl"
GOLDEN_V2_SMOKE = REPO / "knowledge-base-hue/foods/evaluation/golden_v2_smoke.jsonl"
GOLDEN_V3 = REPO / "knowledge-base-hue/foods/evaluation/golden_v3.jsonl"
GOLDEN_V3_SMOKE = REPO / "knowledge-base-hue/foods/evaluation/golden_v3_smoke.jsonl"


def test_golden_v3_rejects_a_full_size_outside_approved_levels():
    assert V3_ALLOWED_COUNTS == {40, 45, 50}
    with pytest.raises(ValueError, match="expected 40, 45, or 50 cases"):
        validate_v3_full([])


def test_golden_v3_smoke_requires_exactly_ten_rows():
    with pytest.raises(ValueError, match="expected 10 smoke cases"):
        validate_v3_smoke([], [])


def test_golden_v3_keeps_the_nine_diagnostic_category_names_without_quotas():
    assert ALLOWED_CATEGORIES == set(CATEGORY_QUOTAS)


def test_golden_v3_contract_uses_an_approved_size_without_distribution_quotas():
    cases = load_golden(GOLDEN_V3)
    summary = validate_v3_full(cases)
    assert summary["cases"] in V3_ALLOWED_COUNTS
    assert sum(summary["categories"].values()) == summary["cases"]
    assert set(summary["categories"]) <= ALLOWED_CATEGORIES


def test_golden_v3_smoke_is_an_exact_ten_row_subset():
    full = load_golden(GOLDEN_V3)
    smoke = load_golden(GOLDEN_V3_SMOKE)
    assert validate_v3_smoke(full, smoke) == {"cases": 10}


def test_small_dataset_contains_twenty_real_questions():
    questions = load_tests(SMALL_DATASET)
    assert len(questions) == 20
    assert questions[0].question == "Quán bún bò Mệ Kéo nằm ở đâu?"
    assert questions[-1].question == "Gợi ý food tour 1 ngày ở Huế?"
    assert {q.category for q in questions} == {
        "direct_fact", "temporal", "comparative", "relationship",
        "spanning", "holistic", "food_knowledge", "guide_planning",
    }


def test_questions_have_the_fields_used_by_evaluation():
    for question in load_tests(SMALL_DATASET):
        assert question.question.strip()
        assert question.category.strip()
        assert question.reference_answer.strip()
        assert question.keywords
        assert all(keyword.strip() for keyword in question.keywords)


def test_load_tests_uses_the_supplied_path():
    assert len(load_tests(SMALL_DATASET)) == 20
    assert len(load_tests(FULL_DATASET)) == 104


def test_mrr_uses_keyword_position_in_real_hue_text():
    texts = [
        "Bún bò Huế — giới thiệu\nNước dùng được nấu từ xương.",
        "Bún bò Mệ Kéo — địa chỉ\nQuán nằm tại 20 Bạch Đằng.",
    ]
    assert calculate_mrr("Mệ Kéo", texts) == 0.5
    assert calculate_mrr("Bạch Đằng", texts) == 0.5


def test_ndcg_uses_binary_keyword_relevance():
    texts = [
        "Bún bò Huế — giới thiệu\nNước dùng được nấu từ xương.",
        "Bún bò Mệ Kéo — địa chỉ\nQuán nằm tại 20 Bạch Đằng.",
    ]
    assert math.isclose(calculate_ndcg("Mệ Kéo", texts), 1 / math.log2(3))
    assert calculate_ndcg("không tồn tại", texts) == 0.0


def test_retrieval_evaluation_uses_the_real_dense_collection(ingested_collection):
    from conftest import TEST_COLLECTION

    question = load_tests(SMALL_DATASET)[0]
    services = build_services("dense_only", collection_name=TEST_COLLECTION)
    row = evaluate_retrieval(question, services)
    assert row["question"] == question.question
    assert row["mrr"] >= 0
    assert row["ndcg"] >= 0
    assert row["total_keywords"] == len(question.keywords)
    assert row["error"] == ""


def test_answer_evaluation_calls_real_generation_and_judge_models(ingested_collection):
    from conftest import TEST_COLLECTION

    question = load_tests(SMALL_DATASET)[0]
    services = build_services("dense_only", collection_name=TEST_COLLECTION)
    row = asyncio.run(evaluate_answer(question, services))
    assert row["question"] == question.question
    assert row["generated_answer"].strip()
    assert 1 <= row["accuracy"] <= 5
    assert 1 <= row["completeness"] <= 5
    assert 1 <= row["relevance"] <= 5
    assert row["feedback"].strip()
    assert row["error"] == ""


def test_retrieval_handler_returns_named_columns_and_rows(ingested_collection):
    from conftest import TEST_COLLECTION

    summary, table = run_retrieval_ui(SMALL_DATASET, 3, collection_name=TEST_COLLECTION)
    assert "## Kết quả retrieval" in summary
    assert isinstance(table, dict)
    assert table["headers"] == [
        "category", "question", "keywords", "mrr", "ndcg",
        "keywords_found", "total_keywords", "keyword_coverage", "error",
    ]
    assert len(table["data"]) == 20
    assert len(table["data"][0]) == 9



def test_retrieval_comparison_reports_latency_failures_and_rank_changes():
    from evaluation.retrieval_comparison import compare_profile_runs, summarize_profile

    active = [
        {"question": "q", "ids": ["a", "b"], "scores": [0.9, 0.8], "latency_ms": 10.0, "error": ""}
    ]
    candidate = [
        {"question": "q", "ids": ["b", "a"], "scores": [0.91, 0.79], "latency_ms": 12.0, "error": ""}
    ]
    assert summarize_profile(active) == {
        "questions": 1,
        "successful": 1,
        "failed": 0,
        "mean_latency_ms": 10.0,
    }
    comparison = compare_profile_runs(active, candidate)
    assert comparison[0]["same_ids_in_order"] is False
    assert comparison[0]["active_ids"] == ["a", "b"]
    assert comparison[0]["candidate_ids"] == ["b", "a"]


def test_golden_v2_contract_and_distribution():
    cases = load_golden(GOLDEN_V2)
    summary = validate_full(cases)
    assert summary["cases"] == 100
    assert summary["categories"] == CATEGORY_QUOTAS
    assert all(
        summary["source_coverage"][family] >= target
        for family, target in SOURCE_TARGETS.items()
    )


def test_golden_v2_smoke_is_exact_representative_subset():
    full = load_golden(GOLDEN_V2)
    smoke = load_golden(GOLDEN_V2_SMOKE)
    summary = validate_smoke(full, smoke)
    assert summary == {"cases": 20, "categories": 9, "source_families": 4}


def test_golden_v2_binary_relevance_uses_real_retrieval_metadata(ingested_collection):
    from conftest import TEST_COLLECTION

    smoke = load_golden(GOLDEN_V2_SMOKE)
    assert len(smoke) == 20
    services = build_services("dense_only", collection_name=TEST_COLLECTION)

    for case in smoke:
        documents = services.retrieval.search(case.question)
        assert len(documents) > 0
        for doc in documents:
            assert isinstance(doc.metadata.get("source"), str)
            assert doc.metadata["source"].startswith("foods/")
            assert isinstance(doc.metadata.get("section"), str)
            relevance = document_is_relevant(case, doc)
            assert isinstance(relevance, bool)


def test_golden_v3_binary_relevance_uses_real_retrieval_metadata(ingested_collection):
    from conftest import TEST_COLLECTION

    smoke = load_golden(GOLDEN_V3_SMOKE)
    assert len(smoke) == 10
    services = build_services("dense_only", collection_name=TEST_COLLECTION)

    for case in smoke:
        documents = services.retrieval.search(case.question)
        assert len(documents) > 0
        for document in documents:
            assert isinstance(document.metadata.get("source"), str)
            assert document.metadata["source"].startswith("foods/")
            assert isinstance(document.metadata.get("section"), str)
            assert isinstance(document_is_relevant(case, document), bool)
