"""Logic thuần của evaluator Phase 7B (không mạng, không Qdrant)."""
import math
import unicodedata

from evaluation.full_corpus_eval import (
    answer_keywords,
    classify_refusal_evidence,
    compare_scores,
    parse_user_scores,
    answered_cases,
    citation_error_rates,
    cost_usd,
    error_case_indexes,
    is_refusal,
    judge_input_rows,
    mean_by_category,
    merge_retried,
    refusal_rates,
    score_retrieval,
    select_cases,
    validate_score_rows,
)
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER


def test_score_retrieval_keyword_rank_casefold_and_nfc():
    # "Huế" dạng tổ hợp (NFD) trong text vẫn khớp keyword dạng NFC.
    decomposed = unicodedata.normalize("NFD", "Đặc sản HUẾ")
    texts = ["không liên quan", decomposed, "bún bò"]
    scores = score_retrieval(["huế", "bún bò", "không có"], texts)
    assert scores["keywords_found"] == 2
    assert scores["total_keywords"] == 3
    assert math.isclose(scores["mrr"], (1 / 2 + 1 / 3 + 0) / 3)
    assert math.isclose(scores["keyword_coverage"], 200 / 3)
    # nDCG mỗi keyword có một tài liệu liên quan: DCG/IDCG = (1/log2(r+1)) / 1.
    assert math.isclose(scores["ndcg"], (1 / math.log2(3) + 1 / math.log2(4) + 0) / 3)


def test_score_retrieval_only_counts_top_k():
    texts = ["x"] * 10 + ["keyword"]
    assert score_retrieval(["keyword"], texts)["keywords_found"] == 0


def test_refusal_is_exact_fallback_sentence():
    assert is_refusal(f"  {INSUFFICIENT_ANSWER}\n")
    assert not is_refusal(f"{INSUFFICIENT_ANSWER} Tuy nhiên có thể thử [1].")


def test_refusal_and_citation_rates():
    rows = [
        {"category": "out_of_scope", "refusal": True, "citation_error": None},
        {"category": "out_of_scope", "refusal": False, "citation_error": "Grounded answer has no citation"},
        {"category": "direct_fact", "refusal": True, "citation_error": None},
        {"category": "direct_fact", "refusal": False, "citation_error": None},
        {"category": "direct_fact", "refusal": False, "citation_error": None},
        {"category": "direct_fact", "refusal": False, "citation_error": None},
    ]
    rates = refusal_rates(rows)
    assert rates["correct_refusal_rate"] == 0.5
    assert rates["false_refusal_rate"] == 0.25
    citation = citation_error_rates(rows)
    assert citation["overall"] == {"n": 6, "rate": 1 / 6}
    assert citation["out_of_scope"] == {"n": 2, "rate": 0.5}


def test_mean_by_category_is_macro_average_over_cases():
    rows = [
        {"category": "a", "accuracy": 5},
        {"category": "a", "accuracy": 3},
        {"category": "b", "accuracy": 1},
    ]
    summary = mean_by_category(rows, ("accuracy",))
    assert summary["overall"] == {"n": 3, "accuracy": 3.0}
    assert summary["a"] == {"n": 2, "accuracy": 4.0}


def test_cost_uses_luna_price():
    # 1M input = 0,1 USD; 1M output = 0,5 USD.
    assert math.isclose(cost_usd(1_000_000, 0), 0.1)
    assert math.isclose(cost_usd(2_000, 1_000), 0.0007)


def test_validate_score_rows_rejects_bad_scores():
    rows = [
        {"case_index": 0, "accuracy": 5, "completeness": 4, "relevance": 3, "feedback": "ok"},
        {"case_index": 1, "accuracy": 6, "completeness": 4, "relevance": 3, "feedback": ""},
        {"case_index": 2, "accuracy": True, "completeness": 4.0, "relevance": 3, "feedback": ""},
        {"case_index": 0, "accuracy": 5, "completeness": 5, "relevance": 5, "feedback": ""},
    ]
    errors = validate_score_rows(rows)
    assert errors == [
        "case 1: accuracy=6 is not an integer 1-5",
        "case 2: accuracy=True is not an integer 1-5",
        "case 2: completeness=4.0 is not an integer 1-5",
        "case 0: duplicated",
    ]


def test_merge_retried_replaces_rows_in_place():
    existing = [{"case_index": 3, "error": None}, {"case_index": 7, "error": "Timeout"}]
    merged = merge_retried(existing, [{"case_index": 7, "error": None}])
    assert merged == [{"case_index": 3, "error": None}, {"case_index": 7, "error": None}]


def test_judge_input_hides_category_and_shuffles_by_seed():
    cases = [
        {"case_index": i, "question": f"q{i}", "reference_answer": f"r{i}", "category": "direct_fact"}
        for i in range(20)
    ]
    answers = [{"case_index": i, "answer": f"a{i}", "category": "direct_fact"} for i in range(20)]
    first = judge_input_rows(cases, answers, seed=1)
    assert set(first[0]) == {"case_index", "question", "reference_answer", "answer"}
    assert first == judge_input_rows(cases, answers, seed=1)
    assert first != judge_input_rows(cases, answers, seed=2)
    assert sorted(row["case_index"] for row in first) == list(range(20))


def test_retry_with_no_error_rows_selects_no_case():
    # Bug thật: danh sách rỗng từng bị hiểu là "mọi case" → retry chạy lại cả Golden (paid).
    cases = [{"case_index": i} for i in range(3)]
    assert select_cases(cases, error_case_indexes([{"case_index": 0, "error": None}])) == []
    assert select_cases(cases, None) == cases
    assert select_cases(cases, [2]) == [{"case_index": 2}]


def test_cases_flag_without_values_selects_no_case_to_judge():
    # m1 (A review Gate 1): `--cases` rỗng từng thành "mọi case" ở judge-luna (paid).
    cases = [{"case_index": i} for i in range(3)]
    answers = [
        {"case_index": 0, "error": None},
        {"case_index": 1, "error": "TimeoutError"},
        {"case_index": 2, "error": None},
    ]
    assert answered_cases(cases, answers, []) == []
    assert answered_cases(cases, answers, None) == [{"case_index": 0}, {"case_index": 2}]
    assert answered_cases(cases, answers, [1, 2]) == [{"case_index": 2}]


def _score(index, a, c, r):
    return {"case_index": index, "accuracy": a, "completeness": c, "relevance": r, "feedback": ""}


def test_compare_scores_signed_diff_and_agreement_rates():
    first = [_score(0, 5, 5, 5), _score(1, 4, 4, 4), _score(2, 3, 3, 3), _score(3, 5, 5, 5)]
    second = [_score(0, 5, 4, 5), _score(1, 2, 4, 5), _score(2, 3, 3, 3),
              {"case_index": 3, "error": "Timeout"}]
    result = compare_scores(first, second)
    assert result["n"] == 3  # case 3 lỗi ở nguồn B bị bỏ
    acc = result["accuracy"]
    assert math.isclose(acc["mean_signed_diff"], -2 / 3)
    assert math.isclose(acc["exact_rate"], 2 / 3)
    assert math.isclose(acc["within_1_rate"], 2 / 3)
    assert math.isclose(acc["diff_ge_2_rate"], 1 / 3)
    assert math.isclose(result["completeness"]["within_1_rate"], 1.0)
    assert compare_scores(first, second, [0, 3, 9])["missing_in_b"] == [3, 9]


def test_parse_user_scores_reads_score_lines_and_reports_unscored():
    sheet = """# Chấm tay

Ghi điểm vào dòng `Điểm:` theo thứ tự, ví dụ `Điểm: 5 / 4 / 5`.

## Câu 1

> Bot: Điểm: 1 / 1 / 1 nằm trong câu trả lời, không phải dòng chấm.

Điểm: 5 / 4 / 3
Ghi chú: thiếu giờ mở cửa

## Câu 2

Điểm: _ / _ / _
"""
    rows, errors = parse_user_scores(sheet, {"1": 17, "2": 40, "3": 99})
    assert rows == [{"case_index": 17, "accuracy": 5, "completeness": 4, "relevance": 3,
                     "feedback": "thiếu giờ mở cửa"}]
    assert errors == ["Câu 2: điểm chưa đủ hoặc không hợp lệ: '_ / _ / _'",
                      "Câu 3: không thấy trong file"]


def test_answer_keywords_and_refusal_evidence_classes():
    case = {"question": "Quán Mệ Kéo ở đâu?", "reference_answer": "Quán Mệ Kéo ở số 20 Bạch Đằng.",
            "keywords": ["Mệ Kéo", "Bạch Đằng", "số 20"]}
    keywords = answer_keywords(case)
    assert keywords == ["Bạch Đằng", "số 20"]
    assert classify_refusal_evidence(keywords, "Mệ Kéo: món bún") == "retrieval_miss"
    assert classify_refusal_evidence(keywords, "địa chỉ BẠCH ĐẰNG") == "partial_evidence"
    assert classify_refusal_evidence(keywords, "số 20 Bạch Đằng") == "evidence_present"
