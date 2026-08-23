"""Pure metric tests with hand-calculated known rankings.

The relevance judgments here are fabricated rankings only to verify metric
math; they are NOT RAG quality evidence (the guide requires the real gold
annotation for that).
"""

import math

import pytest

from core.schema import RetrievedDocument
from evaluation.metrics import (
    aggregate_metrics,
    case_metrics,
    evidence_units,
    keyword_coverage,
    latency_stats,
)


def full_metrics(recall_at_5):
    """Real record shape: every per-case metric key is present."""
    return {
        "recall_at_1": recall_at_5,
        "recall_at_3": recall_at_5,
        "recall_at_5": recall_at_5,
        "recall_at_10": recall_at_5,
        "mrr_at_10": recall_at_5,
        "ndcg_at_5": recall_at_5,
        "ndcg_at_10": recall_at_5,
    }


def doc(source, section, text="Nội dung mẫu", title="Tên nguồn", doc_id=None):
    """Build a RetrievedDocument in rank order with a stable identity."""
    return RetrievedDocument(
        id=doc_id or f"{source}|{section}|{text[:8]}",
        score=0.5,
        text=text,
        metadata={
            "source": source,
            "section": section,
            "title": title,
        },
    )


D1 = "foods/restaurants/quan a.md"
D2 = "foods/restaurants/quan b.md"
D3 = "foods/guides/food-guides.md"


def test_evidence_units_source_without_sections_match_any_section():
    """A source with no declared section is one unit matching any section."""
    units = evidence_units([D2], {})
    assert units == {(D2, None)}


def test_evidence_units_declared_sections_boundary():
    units = evidence_units([D1, D2], {D1: ["Thông tin"], D2: ["Tóm tắt"]})
    assert units == {(D1, "Thông tin"), (D2, "Tóm tắt")}


def test_no_relevant_result_returns_zeros():
    """All metrics are zero when no retrieved item matches gold evidence."""
    retrieved = [doc(D2, "Thông tin"), doc(D3, "Giới thiệu")]
    metrics = case_metrics(retrieved, [D1], {D1: ["Tóm tắt"]})
    assert metrics["recall_at_1"] == 0.0
    assert metrics["recall_at_3"] == 0.0
    assert metrics["recall_at_5"] == 0.0
    assert metrics["recall_at_10"] == 0.0
    assert metrics["mrr_at_10"] == 0.0
    assert metrics["ndcg_at_5"] == 0.0
    assert metrics["ndcg_at_10"] == 0.0
    assert metrics["first_relevant_rank"] is None


def test_first_rank_relevant_gets_perfect_recall_and_mrr():
    retrieved = [doc(D1, "Thông tin"), doc(D2, "Thông tin"), doc(D3, "Địa điểm")]
    metrics = case_metrics(retrieved, [D1], {D1: ["Thông tin"]})
    # idcg = 1/log2(2) and dcg has the relevant unit at rank 1.
    assert metrics["recall_at_1"] == 1.0
    assert metrics["recall_at_3"] == 1.0
    assert metrics["recall_at_10"] == 1.0
    assert metrics["mrr_at_10"] == 1.0
    assert metrics["ndcg_at_5"] == 1.0
    assert metrics["ndcg_at_10"] == 1.0
    assert metrics["first_relevant_rank"] == 1


def test_second_rank_relevant_mrr_and_recall():
    """MRR@10 uses the first relevant rank; recall@1 must miss it."""
    retrieved = [doc(D2, "Giá"), doc(D1, "Thông tin")]
    metrics = case_metrics(retrieved, [D1], {D1: ["Thông tin"]})
    assert metrics["recall_at_1"] == 0.0
    assert metrics["recall_at_3"] == 1.0
    assert metrics["mrr_at_10"] == 0.5
    assert metrics["first_relevant_rank"] == 2
    # ndcg@5 = (1/log2(3)) / (1/log2(2)) = 0.6309...
    assert metrics["ndcg_at_5"] == pytest.approx(math.log2(2) / math.log2(3))


def test_multiple_relevant_and_duplicates_keep_first_rank():
    """Duplicated (source, section) pairs count only at their first rank."""
    retrieved = [
        doc(D1, "Thông tin", doc_id="a1"),
        doc(D1, "Thông tin", doc_id="a2"),  # duplicate pair -> dropped
        doc(D1, "Tóm tắt", doc_id="b1"),
        doc(D2, "Món ăn", doc_id="c1"),  # D2 declared no section: any section
        doc(D3, "Nơi ăn", text="Không liên quan", doc_id="d1"),
    ]
    metrics = case_metrics(retrieved, [D1, D2], {D1: ["Thông tin", "Tóm tắt"]})
    assert metrics["total_units"] == 3
    # One unit matched at rank 1 out of three units.
    assert metrics["recall_at_1"] == pytest.approx(1 / 3)
    assert metrics["recall_at_3"] == 1.0
    assert metrics["recall_at_10"] == 1.0
    assert metrics["mrr_at_10"] == 1.0
    # All three units are in the top 2 after dedup, so ndcg@5 is perfect.
    assert metrics["ndcg_at_5"] == 1.0
    assert metrics["first_relevant_rank"] == 1


def test_more_evidence_units_than_results():
    """Fewer than k results: recall is partial and ndcg uses the observed items."""
    retrieved = [doc(D1, "Thông tin")]
    metrics = case_metrics(
        retrieved, [D1, D2], {D1: ["Thông tin"], D2: ["Thông tin"]}
    )
    assert metrics["total_units"] == 2
    assert metrics["recall_at_1"] == 0.5
    assert metrics["recall_at_5"] == 0.5
    # dcg = 1/log2(2); idcg = 1/log2(2) + 1/log2(3)
    expected_ndcg = (1 / math.log2(2)) / (1 / math.log2(2) + 1 / math.log2(3))
    assert metrics["ndcg_at_5"] == pytest.approx(expected_ndcg)
    assert metrics["ndcg_at_10"] == pytest.approx(expected_ndcg)


def test_empty_gold_evidence_is_rejected():
    """An empty relevant set is an invalid case, rejected like the loader does."""
    with pytest.raises(ValueError):
        case_metrics([doc(D1, "Thông tin")], [], {})


def test_keyword_coverage_normalizes_unicode_case_and_whitespace():
    """NFC + casefold + collapsed whitespace; Vietnamese diacritics preserved."""
    text = "quán bé\tbạch\n　đằng"  # decomposed accents, tabs/newlines
    retrieved = [
        RetrievedDocument(
            id="x1",
            score=0.5,
            text=text,
            metadata={"source": D3, "section": "Giới thiệu", "title": "Cẩm nang"},
        )
    ]
    # keywords in different case / spacing still match after normalization.
    covered = keyword_coverage(retrieved, ["quán bé", "BẠCH ĐẰNG"], k=5)
    assert covered == 1.0


def test_keyword_coverage_matches_title_section_or_text_only():
    assert keyword_coverage([doc(D1, "Thông tin", text="nội dung", title="An Cựu")], ["an cựu"], k=5) == 1.0
    # section heading alone counts too.
    assert keyword_coverage([doc(D1, "Địa điểm", title="X")], ["địa điểm"], k=5) == 1.0
    # phrase must appear inside the normalized text of a ranked doc.
    assert keyword_coverage([doc(D1, "X", text="nội dung", title="Y")], ["mè xửng"], k=5) == 0.0


def test_keyword_coverage_respects_k():
    """Coverage uses only the first k ranked documents."""
    retrieved = [doc(D1, "X", text="nội dung", title="Y"), doc(D2, "Z", text="mè xửng", title="W")]
    assert keyword_coverage(retrieved, ["mè xửng"], k=1) == 0.0
    assert keyword_coverage(retrieved, ["mè xửng"], k=2) == 1.0


def test_aggregate_overall_per_category_and_macro():
    """Overall means, per-category means and macro recall@5 over 8 categories."""
    records = [
        {
            "case_id": "foods-0001",
            "category": "direct_fact",
            "status": "complete",
            "metrics": full_metrics(1.0),
            "latency_ms": 10,
        },
        {
            "case_id": "foods-0002",
            "category": "direct_fact",
            "status": "complete",
            "metrics": full_metrics(0.0),
            "latency_ms": 20,
        },
        {
            "case_id": "foods-0003",
            "category": "holistic",
            "status": "complete",
            "metrics": full_metrics(0.5),
            "latency_ms": 30,
        },
    ]
    agg = aggregate_metrics(records)
    assert agg["overall"]["recall_at_5"] == pytest.approx(0.5)
    assert agg["overall"]["cases_complete"] == 3
    assert agg["per_category"]["direct_fact"]["recall_at_5"] == pytest.approx(0.5)
    assert agg["per_category"]["holistic"]["recall_at_5"] == pytest.approx(0.5)
    # macro = equal weight per category present: mean(0.5, 0.5) = 0.5.
    assert agg["macro_recall_at_5"] == pytest.approx(0.5)
    assert agg["cases_total"] == 3


def test_effective_recall_at_5_counts_failed_case_as_zero():
    """Summary must keep failed rows in the denominator of effective recall."""
    records = [
        {
            "case_id": "foods-0001",
            "category": "direct_fact",
            "status": "complete",
            "metrics": full_metrics(1.0),
            "latency_ms": 10,
        },
        {
            "case_id": "foods-0002",
            "category": "direct_fact",
            "status": "complete",
            "metrics": full_metrics(0.5),
            "latency_ms": 20,
        },
        {
            "case_id": "foods-0003",
            "category": "direct_fact",
            "status": "retrieval_error",
            "metrics": {},
            "latency_ms": None,
        },
    ]
    agg = aggregate_metrics(records)
    # complete-case mean is higher; effective recall drops the failure to 0.
    assert agg["overall"]["recall_at_5"] == pytest.approx(0.75)
    assert agg["overall"]["effective_recall_at_5"] == pytest.approx(0.5)
    assert agg["overall"]["cases_complete"] == 2
    assert agg["per_category"]["direct_fact"]["effective_recall_at_5"] == pytest.approx(0.5)
    assert agg["macro_recall_at_5"] == pytest.approx(0.5)


def test_latency_stats_median_and_p95():
    values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    stats = latency_stats(values)
    assert stats["median_ms"] == 55.0
    # nearest-rank p95: rank = ceil(0.95 * 10) = 10 -> max value.
    assert stats["p95_ms"] == 100.0
    empty = latency_stats([])
    assert empty["median_ms"] is None
    assert empty["p95_ms"] is None
