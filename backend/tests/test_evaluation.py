import asyncio
import math
from pathlib import Path

from evaluation.eval import (
    build_services,
    calculate_mrr,
    calculate_ndcg,
    evaluate_answer,
    evaluate_retrieval,
)
from evaluation.evaluator import run_retrieval_ui
from evaluation.test import load_tests

REPO = Path(__file__).resolve().parents[2]
SMALL_DATASET = REPO / "knowledge-base-hue/foods/evaluation/test2.jsonl"
FULL_DATASET = REPO / "knowledge-base-hue/foods/evaluation/tests.jsonl"


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
