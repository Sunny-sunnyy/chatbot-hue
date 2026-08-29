"""Focused deterministic tests for Phase 8 08a dense embedding benchmark."""
import csv
import math
from pathlib import Path
import pytest
import numpy as np

from core.schema import RetrievedDocument
from evaluation.golden_dataset import GoldenCase
from embedding.dense_benchmark import (
    ALL_DENSE_SETTINGS,
    AUTHORIZED_DENSE_SETTINGS,
    DEFERRED_DENSE_SETTINGS,
    E5_SMALL_SETTING,
    E5_BASE_SETTING,
    HUYDANG_DEK21_SETTING,
    E5_LARGE_SETTING,
    DenseBenchmarkSetting,
)
from evaluation.embedding_benchmark import (
    score_retrieval_case,
    aggregate_case_metrics,
    evaluate_category_guardrails,
    paired_bootstrap_intervals,
    has_clear_gain,
    select_best_lighter_finalist,
    sanitize_benchmark_error,
    upsert_embedding_results_csv,
    run_embedding_benchmark,
    category_table,
    settings_table,
    EmbeddingBenchmarkInputs,
    CaseMetrics,
    BootstrapInterval,
    CSV_COLUMNS,
)


def make_case(
    case_id: str = "foods-v3-0001",
    category: str = "direct_fact",
    evidence: dict[str, list[str]] | None = None,
) -> GoldenCase:
    if evidence is None:
        evidence = {"foods/restaurants/bun-bo-hue.md": ["Giới thiệu và hương vị"]}
    return GoldenCase(
        case_id=case_id,
        question="Bún bò Huế ở đâu ngon?",
        keywords=["bún bò", "huế"],
        reference_answer="Bún bò Huế ngon ở đường Nguyễn Du.",
        category=category,
        evidence=evidence,
    )


def make_doc(rank: int, source: str, section: str, chunk_id: str | None = None) -> RetrievedDocument:
    cid = chunk_id or f"chunk-{rank}"
    return RetrievedDocument(
        id=cid,
        score=1.0 / rank,
        text="Văn bản ẩm thực an toàn",
        metadata={"chunk_id": cid, "source": source, "section": section},
    )


# --- 1. Scoring tests ---


def test_score_retrieval_case_exact_relevance():
    case = make_case(
        evidence={"foods/restaurants/a.md": ["Sec1"], "foods/restaurants/b.md": ["Sec2"]}
    )
    docs = [
        make_doc(1, "foods/restaurants/x.md", "Sec1"),
        make_doc(2, "foods/restaurants/a.md", "Sec1"),
        make_doc(3, "foods/restaurants/a.md", "WrongSec"),
        make_doc(4, "foods/restaurants/a.md", "Sec1", chunk_id="chunk-4-dup"),
        make_doc(5, "foods/restaurants/b.md", "Sec2"),
        make_doc(6, "foods/restaurants/b.md", "Sec2", chunk_id="chunk-6"),
    ]

    metrics = score_retrieval_case(case, docs, k=5)

    assert metrics.case_id == "foods-v3-0001"
    assert metrics.category == "direct_fact"
    assert metrics.hit is True
    assert metrics.recall_at_5 == 1.0
    assert metrics.mrr_at_5 == 0.5

    expected_dcg = (1.0 / math.log2(3)) + (1.0 / math.log2(6))
    expected_idcg = 1.0 + (1.0 / math.log2(3))
    assert math.isclose(metrics.ndcg_at_5, expected_dcg / expected_idcg, rel_tol=1e-5)


def test_score_retrieval_case_no_hit():
    case = make_case(evidence={"foods/restaurants/a.md": ["Sec1"]})
    docs = [make_doc(i, "foods/restaurants/other.md", "Sec1") for i in range(1, 6)]

    metrics = score_retrieval_case(case, docs, k=5)

    assert metrics.hit is False
    assert metrics.recall_at_5 == 0.0
    assert metrics.mrr_at_5 == 0.0
    assert metrics.ndcg_at_5 == 0.0


def test_score_retrieval_case_empty_evidence_raises():
    case = make_case(evidence={})
    docs = [make_doc(1, "foods/restaurants/a.md", "Sec1")]
    with pytest.raises(ValueError, match="empty evidence"):
        score_retrieval_case(case, docs, k=5)


# --- 2. Aggregation tests ---


def test_aggregate_case_metrics():
    m1 = CaseMetrics(
        case_id="foods-v3-0001",
        category="direct_fact",
        recall_at_5=1.0,
        mrr_at_5=1.0,
        ndcg_at_5=1.0,
        hit=True,
        relevant_keys=(("s1", "sec1"),),
        ranked_keys=(("s1", "sec1"),),
    )
    m2 = CaseMetrics(
        case_id="foods-v3-0002",
        category="direct_fact",
        recall_at_5=0.0,
        mrr_at_5=0.0,
        ndcg_at_5=0.0,
        hit=False,
        relevant_keys=(("s2", "sec2"),),
        ranked_keys=(("s3", "sec3"),),
    )
    m3 = CaseMetrics(
        case_id="foods-v3-0003",
        category="comparative",
        recall_at_5=0.5,
        mrr_at_5=0.5,
        ndcg_at_5=0.6,
        hit=True,
        relevant_keys=(("s4", "sec4"), ("s5", "sec5")),
        ranked_keys=(("s4", "sec4"),),
    )

    agg = aggregate_case_metrics([m1, m2, m3])

    assert list(agg.keys()) == ["overall", "comparative", "direct_fact"]
    assert agg["overall"]["case_count"] == 3
    assert agg["overall"]["hit_case_count"] == 2
    assert math.isclose(agg["overall"]["recall_at_5"], (1.0 + 0.0 + 0.5) / 3)
    assert math.isclose(agg["overall"]["mrr_at_5"], (1.0 + 0.0 + 0.5) / 3)
    assert math.isclose(agg["overall"]["ndcg_at_5"], (1.0 + 0.0 + 0.6) / 3)

    assert agg["direct_fact"]["case_count"] == 2
    assert agg["direct_fact"]["hit_case_count"] == 1
    assert agg["direct_fact"]["recall_at_5"] == 0.5
    assert agg["direct_fact"]["mrr_at_5"] == 0.5
    assert agg["direct_fact"]["ndcg_at_5"] == 0.5

    assert agg["comparative"]["case_count"] == 1
    assert agg["comparative"]["hit_case_count"] == 1
    assert agg["comparative"]["recall_at_5"] == 0.5
    assert agg["comparative"]["ndcg_at_5"] == 0.6


# --- 3. Guardrail & Category Invariant tests ---


def test_evaluate_category_guardrails_large_category():
    ref = [
        CaseMetrics(f"id-{i}", "direct_fact", 1.0, 1.0, 1.0, True, (), ())
        for i in range(7)
    ]

    cand_fewer_hits = [
        CaseMetrics(f"id-{i}", "direct_fact", 1.0 if i < 6 else 0.0, 1.0 if i < 6 else 0.0, 1.0 if i < 6 else 0.0, i < 6, (), ())
        for i in range(7)
    ]
    res1 = evaluate_category_guardrails(ref, cand_fewer_hits)
    assert res1["direct_fact"] is False

    cand_tied_low_ndcg = [
        CaseMetrics(f"id-{i}", "direct_fact", 1.0, 0.8, 0.95, True, (), ())
        for i in range(7)
    ]
    res2 = evaluate_category_guardrails(ref, cand_tied_low_ndcg)
    assert res2["direct_fact"] is False

    cand_tied_ok_ndcg = [
        CaseMetrics(f"id-{i}", "direct_fact", 1.0, 0.99, 0.99, True, (), ())
        for i in range(7)
    ]
    res3 = evaluate_category_guardrails(ref, cand_tied_ok_ndcg)
    assert res3["direct_fact"] is True


def test_evaluate_category_guardrails_small_category():
    ref = [
        CaseMetrics("id-1", "numerical", 1.0, 1.0, 1.0, True, (), ()),
        CaseMetrics("id-2", "numerical", 0.0, 0.0, 0.0, False, (), ()),
    ]

    cand_lost = [
        CaseMetrics("id-1", "numerical", 0.0, 0.0, 0.0, False, (), ()),
        CaseMetrics("id-2", "numerical", 1.0, 1.0, 1.0, True, (), ()),
    ]
    res1 = evaluate_category_guardrails(ref, cand_lost)
    assert res1["numerical"] is False

    cand_kept = [
        CaseMetrics("id-1", "numerical", 1.0, 0.2, 0.3, True, (), ()),
        CaseMetrics("id-2", "numerical", 0.0, 0.0, 0.0, False, (), ()),
    ]
    res2 = evaluate_category_guardrails(ref, cand_kept)
    assert res2["numerical"] is True


def test_evaluate_category_guardrails_mismatch_raises():
    ref = [CaseMetrics("id-1", "direct_fact", 1.0, 1.0, 1.0, True, (), ())]
    cand = [CaseMetrics("id-1", "comparative", 1.0, 1.0, 1.0, True, (), ())]
    with pytest.raises(ValueError, match="mismatch"):
        evaluate_category_guardrails(ref, cand)


# --- 4. Paired Bootstrap tests ---


def test_paired_bootstrap_intervals():
    ref = [CaseMetrics(f"id-{i}", "cat", 0.5, 0.5, 0.5, True, (), ()) for i in range(45)]
    cand = [CaseMetrics(f"id-{i}", "cat", 0.6, 0.7, 0.8, True, (), ()) for i in range(45)]

    res = paired_bootstrap_intervals(ref, cand, samples=10_000, seed=42)

    assert math.isclose(res["recall"].delta, 0.1, rel_tol=1e-5)
    assert math.isclose(res["mrr"].delta, 0.2, rel_tol=1e-5)
    assert math.isclose(res["ndcg"].delta, 0.3, rel_tol=1e-5)

    assert math.isclose(res["ndcg"].lower, 0.3, rel_tol=1e-5)
    assert math.isclose(res["ndcg"].upper, 0.3, rel_tol=1e-5)

    res_repeat = paired_bootstrap_intervals(ref, cand, samples=10_000, seed=42)
    assert res == res_repeat


def test_paired_bootstrap_mismatch_raises():
    ref = [CaseMetrics("id-1", "catA", 0.5, 0.5, 0.5, True, (), ())]
    cand = [CaseMetrics("id-1", "catB", 0.5, 0.5, 0.5, True, (), ())]
    with pytest.raises(ValueError, match="mismatch"):
        paired_bootstrap_intervals(ref, cand, samples=1000, seed=42)


# --- 5. Decision & Clear Gain tests ---


def test_has_clear_gain_rules():
    guardrails_all_pass = {"cat1": True, "cat2": True}
    guardrails_fail = {"cat1": True, "cat2": False}

    ndcg_clear = BootstrapInterval(delta=0.035, lower=0.01, upper=0.06)
    ndcg_borderline = BootstrapInterval(delta=0.03, lower=0.005, upper=0.05)
    ndcg_low_delta = BootstrapInterval(delta=0.029, lower=0.01, upper=0.05)
    ndcg_zero_lower = BootstrapInterval(delta=0.04, lower=0.0, upper=0.07)

    assert has_clear_gain(
        status="completed",
        successful_repetitions=3,
        guardrails=guardrails_all_pass,
        ndcg_interval=ndcg_clear,
    ) is True

    assert has_clear_gain(
        status="completed",
        successful_repetitions=3,
        guardrails=guardrails_all_pass,
        ndcg_interval=ndcg_borderline,
    ) is True

    assert has_clear_gain(
        status="partial",
        successful_repetitions=3,
        guardrails=guardrails_all_pass,
        ndcg_interval=ndcg_clear,
    ) is False

    assert has_clear_gain(
        status="completed",
        successful_repetitions=2,
        guardrails=guardrails_all_pass,
        ndcg_interval=ndcg_clear,
    ) is False

    assert has_clear_gain(
        status="completed",
        successful_repetitions=3,
        guardrails=guardrails_fail,
        ndcg_interval=ndcg_clear,
    ) is False

    assert has_clear_gain(
        status="completed",
        successful_repetitions=3,
        guardrails=guardrails_all_pass,
        ndcg_interval=ndcg_low_delta,
    ) is False

    assert has_clear_gain(
        status="completed",
        successful_repetitions=3,
        guardrails=guardrails_all_pass,
        ndcg_interval=ndcg_zero_lower,
    ) is False


def test_select_best_lighter_finalist():
    finalist_rows = [
        {"order": 1, "setting_key": "e5-small-384", "ndcg_at_5": 0.60, "mrr_at_5": 0.65, "recall_at_5": 0.70}
    ]
    assert select_best_lighter_finalist(2, finalist_rows) == "e5-small-384"

    finalist_rows_with_survivor = [
        {"order": 1, "setting_key": "e5-small-384", "ndcg_at_5": 0.60, "mrr_at_5": 0.65, "recall_at_5": 0.70},
        {"order": 2, "setting_key": "cand-2", "ndcg_at_5": 0.65, "mrr_at_5": 0.68, "recall_at_5": 0.72},
    ]
    assert select_best_lighter_finalist(3, finalist_rows_with_survivor) == "cand-2"


# --- 6. CSV Upsert & Header Validation tests ---


def test_upsert_embedding_results_csv(tmp_path: Path):
    csv_file = tmp_path / "test_results.csv"

    row_overall = {
        "setting_key": "e5-small-384",
        "setting_label": "E5-small 384D (control)",
        "category": "overall",
        "model_id": "intfloat/multilingual-e5-small",
        "model_revision": "rev1",
        "dimension": 384,
        "max_length": 512,
        "collection_name": "hue_foods_08a_e5_small_384",
        "retrieval_mode": "dense",
        "use_bm25": False,
        "use_reranker": False,
        "status": "completed",
        "error": "",
        "case_count": 45,
        "hit_case_count": 40,
        "recall_at_5": 0.85,
        "mrr_at_5": 0.80,
        "ndcg_at_5": 0.82,
        "successful_repetitions": 3,
        "ranking_stable": True,
        "truncated_document_count": 0,
        "cold_load_ms": 1200.0,
        "document_embedding_ms": 5000.0,
        "query_embedding_p50_ms": 10.0,
        "query_embedding_p95_ms": 15.0,
        "retrieval_p50_ms": 5.0,
        "retrieval_p95_ms": 8.0,
        "warm_total_p50_ms": 15.0,
        "warm_total_p95_ms": 23.0,
        "rss_before_load_mb": 100.0,
        "rss_after_load_mb": 500.0,
        "observed_peak_rss_mb": 600.0,
        "device": "cpu",
        "dtype": "float32",
        "document_batch_size": 8,
        "query_batch_size": 1,
        "delta_recall_at_5": "",
        "delta_mrr_at_5": "",
        "delta_ndcg_at_5": "",
        "recall_ci_lower": "",
        "recall_ci_upper": "",
        "mrr_ci_lower": "",
        "mrr_ci_upper": "",
        "ndcg_ci_lower": "",
        "ndcg_ci_upper": "",
        "category_guardrail_pass": "",
        "all_category_guardrails_pass": "",
        "clear_gain_vs_control": "",
        "best_lighter_setting": "",
        "clear_gain_vs_best_lighter": "",
        "finalist_eligible": True,
    }

    row_cat1 = dict(row_overall)
    row_cat1["category"] = "direct_fact"
    row_cat1["cold_load_ms"] = ""
    row_cat1["document_embedding_ms"] = ""
    row_cat1["query_embedding_p50_ms"] = ""
    row_cat1["query_embedding_p95_ms"] = ""
    row_cat1["retrieval_p50_ms"] = ""
    row_cat1["retrieval_p95_ms"] = ""
    row_cat1["warm_total_p50_ms"] = ""
    row_cat1["warm_total_p95_ms"] = ""
    row_cat1["rss_before_load_mb"] = ""
    row_cat1["rss_after_load_mb"] = ""
    row_cat1["observed_peak_rss_mb"] = ""

    upsert_embedding_results_csv([row_overall, row_cat1], path=csv_file)
    assert csv_file.is_file()

    row_overall_updated = dict(row_overall)
    row_overall_updated["ndcg_at_5"] = 0.83

    row_cand = dict(row_overall)
    row_cand["setting_key"] = "e5-base-768"
    row_cand["setting_label"] = "E5-base 768D"
    row_cand["dimension"] = 768

    upsert_embedding_results_csv([row_overall_updated, row_cand], path=csv_file)

    lines = csv_file.read_text(encoding="utf-8").splitlines()
    header = lines[0].split(",")
    assert header == list(CSV_COLUMNS)
    assert len(lines) == 4


def test_upsert_csv_rejects_corrupted_header(tmp_path: Path):
    csv_file = tmp_path / "corrupted.csv"
    csv_file.write_text("setting_key,category,wrong_col\n", encoding="utf-8")

    with pytest.raises(ValueError, match="existing CSV header"):
        upsert_embedding_results_csv([{"setting_key": "e5-small-384", "category": "overall"}], path=csv_file)


# --- 7. Boundary Protection & Safety Invariant tests ---


def test_run_embedding_benchmark_rejects_missing_snapshot():
    fake_inputs = EmbeddingBenchmarkInputs(
        cases=[],
        chunks=[],
        client=None,
        settings={"vector_database": {"collection_name": "hue_foods_e5_small_384"}},
    )

    with pytest.raises(TypeError, match="missing 1 required keyword-only argument: 'expected_active_snapshot'"):
        run_embedding_benchmark(E5_SMALL_SETTING, fake_inputs)


def test_run_embedding_benchmark_rejects_unapproved_setting():
    invalid_setting = DenseBenchmarkSetting(
        order=99,
        setting_key="arbitrary-model",
        setting_label="Arbitrary",
        model_id="arbitrary/model",
        revision="rev",
        dimension=128,
        max_length=128,
        collection_name="arbitrary_collection",
        runner_kind="sentence_transformer",
        input_contract="minilm",
    )
    fake_inputs = EmbeddingBenchmarkInputs(
        cases=[],
        chunks=[],
        client=None,
        settings={"vector_database": {"collection_name": "hue_foods_e5_small_384"}},
    )

    with pytest.raises(ValueError, match="unapproved benchmark setting key"):
        run_embedding_benchmark(invalid_setting, fake_inputs, expected_active_snapshot={})


def test_run_embedding_benchmark_rejects_forged_setting():
    # Setting with approved key but modified dimension
    forged_setting = DenseBenchmarkSetting(
        order=1,
        setting_key="e5-small-384",
        setting_label="E5-small 384D (control)",
        model_id="intfloat/multilingual-e5-small",
        revision="614241f622f53c4eeff9890bdc4f31cfecc418b3",
        dimension=768,  # forged dimension!
        max_length=512,
        collection_name="hue_foods_08a_e5_small_384",
        runner_kind="sentence_transformer",
        input_contract="e5",
    )
    fake_inputs = EmbeddingBenchmarkInputs(
        cases=[],
        chunks=[],
        client=None,
        settings={"vector_database": {"collection_name": "hue_foods_e5_small_384"}},
    )

    with pytest.raises(ValueError, match="forged or altered setting object"):
        run_embedding_benchmark(forged_setting, fake_inputs, expected_active_snapshot={})


def test_run_embedding_benchmark_rejects_deferred_setting():
    fake_inputs = EmbeddingBenchmarkInputs(
        cases=[],
        chunks=[],
        client=None,
        settings={"vector_database": {"collection_name": "hue_foods_e5_small_384"}},
    )

    with pytest.raises(ValueError, match="deferred and not authorized"):
        run_embedding_benchmark(E5_LARGE_SETTING, fake_inputs, expected_active_snapshot={})


def test_run_embedding_benchmark_rejects_active_target():
    fake_inputs = EmbeddingBenchmarkInputs(
        cases=[],
        chunks=[],
        client=None,
        settings={"vector_database": {"collection_name": "hue_foods_08a_e5_small_384"}},
    )

    with pytest.raises(ValueError, match="cannot use active production collection"):
        run_embedding_benchmark(E5_SMALL_SETTING, fake_inputs, expected_active_snapshot={})


# --- 8. Error Sanitizer tests ---


def test_sanitize_benchmark_error():
    # 1. Signed URL with credentials / signatures
    err1 = RuntimeError("Download failed: https://hf-mirror.com/models/bge.bin?X-Amz-Credential=AKIAIOSFODNN7EXAMPLE&X-Amz-Signature=d2c602&token=hf_secret")
    sanitized1 = sanitize_benchmark_error(err1)
    assert "AKIAIOSFODNN7EXAMPLE" not in sanitized1
    assert "d2c602" not in sanitized1
    assert "hf_secret" not in sanitized1
    assert "[REDACTED]" in sanitized1

    # 2. Authorization headers (Basic & Bearer)
    err2 = RuntimeError("HTTP 401 Unauthorized: Authorization: Basic dXNlcjpwYXNz and Authorization: Bearer eyJhbGciOi...")
    sanitized2 = sanitize_benchmark_error(err2)
    assert "dXNlcjpwYXNz" not in sanitized2
    assert "eyJhbGciOi" not in sanitized2

    # 3. Cookie headers
    err3 = RuntimeError("Request error with Cookie: session_id=12345; auth_token=abcdef")
    sanitized3 = sanitize_benchmark_error(err3)
    assert "12345" not in sanitized3
    assert "abcdef" not in sanitized3

    # 4. Nested cause traversal
    cause = ValueError("Underlying token=SECRET_TOKEN failed")
    wrapper = RuntimeError("Outer error")
    wrapper.__cause__ = cause
    sanitized4 = sanitize_benchmark_error(wrapper)
    assert "ValueError" in sanitized4
    assert "SECRET_TOKEN" not in sanitized4


# --- 9. Category Table & Settings Table View tests ---


def test_category_table_helper():
    from evaluation.embedding_benchmark import EmbeddingBenchmarkResult

    ctrl_res = EmbeddingBenchmarkResult(
        setting=E5_SMALL_SETTING,
        status="completed",
        error="",
        summary={"setting_key": "e5-small-384"},
        category_rows=[
            {
                "setting_key": "e5-small-384",
                "category": "direct_fact",
                "case_count": 7,
                "hit_case_count": 6,
                "recall_at_5": 0.85,
                "mrr_at_5": 0.78,
                "ndcg_at_5": 0.79,
                "delta_ndcg_at_5": "",
                "category_guardrail_pass": "",
            }
        ],
        case_metrics=[],
        rankings_by_repetition=[],
    )

    cand_res = EmbeddingBenchmarkResult(
        setting=E5_BASE_SETTING,
        status="completed",
        error="",
        summary={"setting_key": "e5-base-768"},
        category_rows=[
            {
                "setting_key": "e5-base-768",
                "category": "direct_fact",
                "case_count": 7,
                "hit_case_count": 7,
                "recall_at_5": 1.0,
                "mrr_at_5": 0.80,
                "ndcg_at_5": 0.81,
                "delta_ndcg_at_5": 0.02,
                "category_guardrail_pass": True,
            }
        ],
        case_metrics=[],
        rankings_by_repetition=[],
    )

    df = category_table(ctrl_res, [cand_res])
    assert df.shape == (2, 8)
    assert "direct_fact" in df["Category"].to_list()
    assert "+0.0200" in df["Delta nDCG"].to_list()


def test_settings_table_helper():
    df = settings_table()
    assert df.shape == (8, 9)
    assert "Scope Status" in df.columns
    assert "huydang-dek21-embedding-768" in df["Key"].to_list()


# --- 10. Huydang DEk21 & PyVi Integration tests ---


def test_huydang_dek21_setting_contract():
    s = HUYDANG_DEK21_SETTING
    assert s.order == 3
    assert s.setting_key == "huydang-dek21-embedding-768"
    assert s.model_id == "CODE4LIFEOFFICIAL/huydang-dek21-embedding"
    assert s.revision == "517f1af7dd04a57194f1de2990f0c6ede0a3109b"
    assert s.dimension == 768
    assert s.max_length == 256
    assert s.collection_name == "hue_foods_08a_huydang_dek21_768"
    assert s.runner_kind == "huydang"
    assert s.input_contract == "pyvi_segmented"


def test_pyvi_segmentation_food_text():
    from pyvi import ViTokenizer
    text = "Bún bò Huế rất ngon và nổi tiếng ở cố đô Huế."
    segmented = ViTokenizer.tokenize(text)
    assert segmented == "Bún_bò Huế rất ngon và nổi_tiếng ở cố_đô Huế ."
