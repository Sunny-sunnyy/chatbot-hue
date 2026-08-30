import csv
import json
from pathlib import Path

import pytest

from core.schema import RetrievedDocument
from evaluation.embedding_benchmark import (
    CaseMetrics,
    evaluate_category_guardrails,
    score_retrieval_case,
)
from evaluation.golden_dataset import GoldenCase
from evaluation.reranker_benchmark import (
    CASE_RECORD_FIELDS,
    GOLDEN_CATEGORIES,
    INPUT_SETTINGS,
    REPO_ROOT,
    RESULT_COLUMNS,
    _atomic_csv,
    _atomic_jsonl,
    _read_jsonl,
    _write_truthful_failure_for_all_inputs,
    evaluate_input_evidence,
    evaluate_production_safety,
    load_reranker_benchmark_inputs,
    load_runtime_reranker,
    reconcile_reranker_artifacts,
    score_fixed_pair,
    upsert_input_artifacts,
    validate_reranker_inputs,
)


def _make_dummy_case(
    case_id: str = "foods-v3-0001",
    category: str = "direct_fact",
    source: str = "foods/restaurants/bun_bo.md",
    section: str = "Thông tin",
) -> GoldenCase:
    return GoldenCase(
        case_id=case_id,
        category=category,
        question="Quán bún bò nào ngon?",
        reference_answer="Quán 1",
        evidence={source: [section]},
        keywords=["bún bò", "quán 1"],
    )


def test_input_settings_order_and_uniqueness():
    assert len(INPUT_SETTINGS) == 3
    orders = [s.order for s in INPUT_SETTINGS]
    keys = [s.key for s in INPUT_SETTINGS]
    assert orders == [1, 2, 3]
    assert len(set(keys)) == 3
    assert keys == [
        "dense__e5-small-384",
        "dense__huydang-dek21-embedding-768",
        "hybrid-bm25-weighted__huydang-dek21-embedding-768",
    ]


@pytest.mark.parametrize(
    "fingerprint_key",
    ["corpus_fingerprint", "golden_fingerprint", "chunker_fingerprint"],
)
def test_validate_reranker_inputs_rejects_fingerprint_mismatch(fingerprint_key):
    inputs = load_reranker_benchmark_inputs()
    corrupt_manifest = json.loads(json.dumps(inputs.manifest))
    corrupt_manifest["immutable_identity"][fingerprint_key] = "corrupted_hash"

    raw_cases = _read_jsonl(REPO_ROOT / "evaluation" / "results" / "phase8_sparse_cases.jsonl")
    chunks = list(inputs.chunks_by_id.values())
    smoke_cases = [c for c in inputs.cases if c.case_id in inputs.smoke_case_ids]

    with pytest.raises(ValueError, match=fingerprint_key.split("_")[0]):
        validate_reranker_inputs(
            manifest=corrupt_manifest,
            sparse_case_records=raw_cases,
            cases=inputs.cases,
            smoke_cases=smoke_cases,
            chunks=chunks,
        )


def test_validate_reranker_inputs_rejects_manifest_mismatch():
    inputs = load_reranker_benchmark_inputs()
    corrupt_manifest = dict(inputs.manifest)
    corrupt_manifest["experiment_version"] = "wrong_version"

    raw_cases = _read_jsonl(REPO_ROOT / "evaluation" / "results" / "phase8_sparse_cases.jsonl")
    chunks = list(inputs.chunks_by_id.values())
    smoke_cases = [c for c in inputs.cases if c.case_id in inputs.smoke_case_ids]

    with pytest.raises(ValueError, match="expected source manifest version"):
        validate_reranker_inputs(
            manifest=corrupt_manifest,
            sparse_case_records=raw_cases,
            cases=inputs.cases,
            smoke_cases=smoke_cases,
            chunks=chunks,
        )


def test_validate_reranker_inputs_rejects_uncompleted_status():
    inputs = load_reranker_benchmark_inputs()
    raw_cases = _read_jsonl(REPO_ROOT / "evaluation" / "results" / "phase8_sparse_cases.jsonl")
    for r in raw_cases:
        if r.get("setting_key") == "dense__e5-small-384":
            r["status"] = "failed"
            break
    chunks = list(inputs.chunks_by_id.values())
    smoke_cases = [c for c in inputs.cases if c.case_id in inputs.smoke_case_ids]

    with pytest.raises(ValueError, match="uncompleted status"):
        validate_reranker_inputs(
            manifest=inputs.manifest,
            sparse_case_records=raw_cases,
            cases=inputs.cases,
            smoke_cases=smoke_cases,
            chunks=chunks,
        )


def test_validate_reranker_inputs_rejects_invalid_chunk_count_or_ordering():
    inputs = load_reranker_benchmark_inputs()
    raw_cases = _read_jsonl(REPO_ROOT / "evaluation" / "results" / "phase8_sparse_cases.jsonl")
    for r in raw_cases:
        if r.get("setting_key") == "dense__e5-small-384":
            r["fusion_top_10"] = r["fusion_top_10"][:9]
            break
    chunks = list(inputs.chunks_by_id.values())
    smoke_cases = [c for c in inputs.cases if c.case_id in inputs.smoke_case_ids]

    with pytest.raises(ValueError, match="does not have exactly 10 candidate chunks"):
        validate_reranker_inputs(
            manifest=inputs.manifest,
            sparse_case_records=raw_cases,
            cases=inputs.cases,
            smoke_cases=smoke_cases,
            chunks=chunks,
        )


def test_validate_reranker_inputs_rejects_duplicate_chunk_in_top10():
    inputs = load_reranker_benchmark_inputs()
    raw_cases = _read_jsonl(REPO_ROOT / "evaluation" / "results" / "phase8_sparse_cases.jsonl")
    for r in raw_cases:
        if r.get("setting_key") == "dense__e5-small-384":
            r["fusion_top_10"][1]["chunk_id"] = r["fusion_top_10"][0]["chunk_id"]
            break
    chunks = list(inputs.chunks_by_id.values())
    smoke_cases = [c for c in inputs.cases if c.case_id in inputs.smoke_case_ids]

    with pytest.raises(ValueError, match="duplicate chunk_id"):
        validate_reranker_inputs(
            manifest=inputs.manifest,
            sparse_case_records=raw_cases,
            cases=inputs.cases,
            smoke_cases=smoke_cases,
            chunks=chunks,
        )


def test_real_load_reranker_benchmark_inputs_passes():
    inputs = load_reranker_benchmark_inputs()
    assert len(inputs.cases) == 45
    assert len(inputs.smoke_case_ids) == 10
    assert len(inputs.chunks_by_id) == 572
    assert len(inputs.fixed_cases) == 135

    cases_s1 = [fc for fc in inputs.fixed_cases if fc.input_order == 1]
    cases_s2 = [fc for fc in inputs.fixed_cases if fc.input_order == 2]
    cases_s3 = [fc for fc in inputs.fixed_cases if fc.input_order == 3]
    assert len(cases_s1) == 45
    assert len(cases_s2) == 45
    assert len(cases_s3) == 45

    for fc in inputs.fixed_cases:
        assert len(fc.pre_rerank_documents) == 10
        for doc in fc.pre_rerank_documents:
            assert doc.id in inputs.chunks_by_id
            assert doc.metadata.get("text")
            assert doc.text


def test_score_fixed_pair_all_hit_change_branches():
    case = _make_dummy_case(source="foods/r.md", section="S1")
    doc_hit = RetrievedDocument(id="c1", text="hit", score=0.9, metadata={"source": "foods/r.md", "section": "S1"})
    doc_miss = RetrievedDocument(id="c2", text="miss", score=0.8, metadata={"source": "foods/other.md", "section": "Other"})

    # 1. gained: before=miss, after=hit
    p_gained = score_fixed_pair(case, [doc_miss] * 5, [doc_hit] + [doc_miss] * 4)
    assert p_gained.hit_change == "gained"
    assert p_gained.before.hit is False
    assert p_gained.after.hit is True
    assert p_gained.relevant_rank_before == {"foods/r.md::S1": None}
    assert p_gained.relevant_rank_after == {"foods/r.md::S1": 1}

    # 2. lost: before=hit, after=miss
    p_lost = score_fixed_pair(case, [doc_hit] + [doc_miss] * 4, [doc_miss] * 5)
    assert p_lost.hit_change == "lost"
    assert p_lost.before.hit is True
    assert p_lost.after.hit is False
    assert p_lost.relevant_rank_before == {"foods/r.md::S1": 1}
    assert p_lost.relevant_rank_after == {"foods/r.md::S1": None}

    # 3. unchanged_hit: before=hit, after=hit
    p_unchanged_hit = score_fixed_pair(case, [doc_hit] + [doc_miss] * 4, [doc_miss, doc_hit] + [doc_miss] * 3)
    assert p_unchanged_hit.hit_change == "unchanged_hit"
    assert p_unchanged_hit.before.hit is True
    assert p_unchanged_hit.after.hit is True
    assert p_unchanged_hit.relevant_rank_before == {"foods/r.md::S1": 1}
    assert p_unchanged_hit.relevant_rank_after == {"foods/r.md::S1": 2}

    # 4. unchanged_miss: before=miss, after=miss
    p_unchanged_miss = score_fixed_pair(case, [doc_miss] * 5, [doc_miss] * 5)
    assert p_unchanged_miss.hit_change == "unchanged_miss"
    assert p_unchanged_miss.before.hit is False
    assert p_unchanged_miss.after.hit is False
    assert p_unchanged_miss.relevant_rank_before == {"foods/r.md::S1": None}
    assert p_unchanged_miss.relevant_rank_after == {"foods/r.md::S1": None}


def test_evaluate_input_evidence_eligibility_and_clear_gain_boundaries():
    categories = list(GOLDEN_CATEGORIES)
    paired_cases = []
    for i in range(45):
        cat = categories[i % len(categories)]
        case = _make_dummy_case(case_id=f"foods-v3-{i:04d}", category=cat)
        doc_hit = RetrievedDocument(id=f"c-{i}", text="hit", score=0.9, metadata={"source": "foods/restaurants.md", "section": "Quán Bún Bò Huế 1"})
        p = score_fixed_pair(case, [doc_hit] * 5, [doc_hit] * 5)
        paired_cases.append(p)

    # 1. Baseline: all guardrails pass, p95 <= 3000 -> eligible = True, clear_gain = False (delta = 0)
    ev1 = evaluate_input_evidence(paired_cases, successful_repetitions=3, ranking_stable=True, rerank_p95_ms=100.0)
    assert ev1.all_category_guardrails_pass is True
    assert ev1.eligible is True
    assert ev1.clear_gain is False

    # 2. P95 latency boundary > 3000 -> eligible = False
    ev2 = evaluate_input_evidence(paired_cases, successful_repetitions=3, ranking_stable=True, rerank_p95_ms=3000.1)
    assert ev2.eligible is False
    assert ev2.clear_gain is False

    # 3. Successful repetitions != 3 -> eligible = False
    ev3 = evaluate_input_evidence(paired_cases, successful_repetitions=2, ranking_stable=True, rerank_p95_ms=100.0)
    assert ev3.eligible is False

    # 4. Ranking stable False -> eligible = False
    ev4 = evaluate_input_evidence(paired_cases, successful_repetitions=3, ranking_stable=False, rerank_p95_ms=100.0)
    assert ev4.eligible is False

    # 5. Clear gain positive case: all cases gained (delta nDCG = 1.0 > 0.03, CI lower > 0) -> clear_gain = True
    paired_gained = []
    for i in range(45):
        cat = categories[i % len(categories)]
        case = _make_dummy_case(case_id=f"foods-v3-{i:04d}", category=cat, source="foods/restaurants.md", section="Quán Bún Bò Huế 1")
        doc_hit = RetrievedDocument(id=f"c-hit-{i}", text="hit", score=0.9, metadata={"source": "foods/restaurants.md", "section": "Quán Bún Bò Huế 1"})
        doc_miss = RetrievedDocument(id=f"c-miss-{i}", text="miss", score=0.8, metadata={"source": "foods/other.md", "section": "Other"})
        p = score_fixed_pair(case, [doc_miss] * 5, [doc_hit] * 5)
        paired_gained.append(p)
    ev5 = evaluate_input_evidence(paired_gained, successful_repetitions=3, ranking_stable=True, rerank_p95_ms=100.0)
    assert ev5.eligible is True
    assert ev5.clear_gain is True


def test_evaluate_production_safety():
    categories = list(GOLDEN_CATEGORIES)
    ref_metrics = []
    cand_metrics = []
    for i in range(45):
        cat = categories[i % len(categories)]
        m_ref = CaseMetrics(
            case_id=f"foods-v3-{i:04d}",
            category=cat,
            recall_at_5=1.0,
            mrr_at_5=1.0,
            ndcg_at_5=1.0,
            hit=True,
            relevant_keys=(("s", "sec"),),
            ranked_keys=(("s", "sec"),),
        )
        ref_metrics.append(m_ref)
        cand_metrics.append(m_ref)

    # Identical -> safety True
    assert evaluate_production_safety(cand_metrics, ref_metrics) is True

    # Drop overall recall > 0.005 -> safety False
    cand_metrics_bad = list(cand_metrics)
    cand_metrics_bad[0] = CaseMetrics(
        case_id="foods-v3-0000",
        category=categories[0],
        recall_at_5=0.0,
        mrr_at_5=0.0,
        ndcg_at_5=0.0,
        hit=False,
        relevant_keys=(("s", "sec"),),
        ranked_keys=(),
    )
    assert evaluate_production_safety(cand_metrics_bad, ref_metrics) is False


def _make_dummy_summary_rows(setting_order: int, setting_key: str, p50: float = 20.0) -> list[dict]:
    categories = ["overall"] + sorted(GOLDEN_CATEGORIES)
    rows = []
    for state_order, state_key, model_id in [(1, "no-rerank", ""), (2, "minilm", "cross-encoder/ms-marco-MiniLM-L-6-v2")]:
        for cat in categories:
            rows.append({
                "experiment_version": "phase8-08c-v1",
                "input_order": setting_order,
                "input_key": setting_key,
                "input_label": f"Label {setting_key}",
                "state_order": state_order,
                "state_key": state_key,
                "model_id": model_id,
                "model_revision": "not_reported" if state_key == "minilm" else "",
                "category": cat,
                "status": "completed",
                "error": "",
                "case_count": 45 if cat == "overall" else 5,
                "hit_case_count": 40 if cat == "overall" else 4,
                "successful_repetitions": 3 if state_key == "minilm" else "",
                "ranking_stable": "True" if state_key == "minilm" else "",
                "recall_at_5": 0.8,
                "mrr_at_5": 0.75,
                "ndcg_at_5": 0.78,
                "delta_recall_at_5": 0.0 if state_key == "no-rerank" else 0.05,
                "delta_mrr_at_5": 0.0 if state_key == "no-rerank" else 0.05,
                "delta_ndcg_at_5": 0.0 if state_key == "no-rerank" else 0.05,
                "recall_ci_lower": 0.0 if state_key == "no-rerank" else -0.01,
                "recall_ci_upper": 0.0 if state_key == "no-rerank" else 0.1,
                "mrr_ci_lower": 0.0 if state_key == "no-rerank" else -0.01,
                "mrr_ci_upper": 0.0 if state_key == "no-rerank" else 0.1,
                "ndcg_ci_lower": 0.0 if state_key == "no-rerank" else -0.01,
                "ndcg_ci_upper": 0.0 if state_key == "no-rerank" else 0.1,
                "category_guardrail_pass": "True" if (state_key == "minilm" and cat != "overall") else "",
                "all_category_guardrails_pass": "True" if (state_key == "minilm" and cat == "overall") else "",
                "eligible": "True" if (state_key == "minilm" and cat == "overall") else "",
                "clear_gain": "False" if (state_key == "minilm" and cat == "overall") else "",
                "production_safety": "True" if (state_key == "minilm" and cat == "overall" and setting_order == 3) else "",
                "cold_load_ms": 150.0 if (setting_order == 1 and state_key == "minilm" and cat == "overall") else "",
                "rerank_p50_ms": p50 if (state_key == "minilm" and cat == "overall") else "",
                "rerank_p95_ms": 30.0 if (state_key == "minilm" and cat == "overall") else "",
                "rss_before_load_mb": 100.0 if (setting_order == 1 and state_key == "minilm" and cat == "overall") else "",
                "rss_after_load_mb": 200.0 if (setting_order == 1 and state_key == "minilm" and cat == "overall") else "",
                "observed_peak_rss_mb": 250.0 if (setting_order == 1 and state_key == "minilm" and cat == "overall") else "",
                "device": "cpu" if state_key == "minilm" else "",
                "dtype": "float32" if state_key == "minilm" else "",
            })
    return rows


def _make_dummy_case_records(setting_order: int, setting_key: str, p50: float = 20.0) -> list[dict]:
    records = []
    for i in range(1, 46):
        records.append({
            "experiment_version": "phase8-08c-v1",
            "input_order": setting_order,
            "input_key": setting_key,
            "case_id": f"foods-v3-{i:04d}",
            "category": "direct_fact",
            "status": "completed",
            "error": "",
            "relevant_source_sections": [{"source": "foods/a.md", "section": "A"}],
            "pre_rerank_top_10": [{"chunk_id": f"chunk-{j:03d}", "rank": j, "score": 1.0/j, "source": "foods/a.md", "section": "A"} for j in range(1, 11)],
            "no_rerank_top_5": [{"chunk_id": f"chunk-{j:03d}", "rank": j, "score": 1.0/j, "source": "foods/a.md", "section": "A"} for j in range(1, 6)],
            "minilm_top_5": [{"chunk_id": f"chunk-{j:03d}", "rank": j, "score": 1.0/j, "source": "foods/a.md", "section": "A"} for j in range(1, 6)],
            "successful_repetitions": 3,
            "ranking_stable": True,
            "hit_before": True,
            "hit_after": True,
            "hit_change": "unchanged_hit",
            "relevant_rank_before": {"foods/a.md|A": 1},
            "relevant_rank_after": {"foods/a.md|A": 1},
            "recall_at_5_before": 1.0,
            "recall_at_5_after": 1.0,
            "mrr_at_5_before": 1.0,
            "mrr_at_5_after": 1.0,
            "ndcg_at_5_before": 1.0,
            "ndcg_at_5_after": 1.0,
            "latency_by_repetition_ms": [p50, p50 + 0.1, p50 + 0.2],
        })
    return records


def test_upsert_input_artifacts_idempotent_and_ordered(tmp_path):
    results_path = tmp_path / "results.csv"
    cases_path = tmp_path / "cases.jsonl"

    # 1. Upsert input 1
    s1_v1 = _make_dummy_summary_rows(1, "dense__e5-small-384", p50=20.0)
    c1_v1 = _make_dummy_case_records(1, "dense__e5-small-384", p50=20.0)
    upsert_input_artifacts("dense__e5-small-384", s1_v1, c1_v1, results_path=results_path, cases_path=cases_path)

    # 2. Upsert input 2
    s2_v1 = _make_dummy_summary_rows(2, "dense__huydang-dek21-embedding-768", p50=20.0)
    c2_v1 = _make_dummy_case_records(2, "dense__huydang-dek21-embedding-768", p50=20.0)
    upsert_input_artifacts("dense__huydang-dek21-embedding-768", s2_v1, c2_v1, results_path=results_path, cases_path=cases_path)

    # 3. Replace input 1 with updated latency p50=25.0
    s1_v2 = _make_dummy_summary_rows(1, "dense__e5-small-384", p50=25.0)
    c1_v2 = _make_dummy_case_records(1, "dense__e5-small-384", p50=25.0)
    upsert_input_artifacts("dense__e5-small-384", s1_v2, c1_v2, results_path=results_path, cases_path=cases_path)

    # Verify input 1 updated to 25.0, input 2 remained 20.0
    with results_path.open("r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        assert len(reader) == 40
        for row in reader:
            if row["input_key"] == "dense__e5-small-384" and row["state_key"] == "minilm" and row["category"] == "overall":
                assert float(row["rerank_p50_ms"]) == 25.0
            elif row["input_key"] == "dense__huydang-dek21-embedding-768" and row["state_key"] == "minilm" and row["category"] == "overall":
                assert float(row["rerank_p50_ms"]) == 20.0

    cases_lines = [json.loads(line) for line in cases_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(cases_lines) == 90
    for cl in cases_lines:
        if cl["input_key"] == "dense__e5-small-384":
            assert cl["latency_by_repetition_ms"][0] == 25.0
        elif cl["input_key"] == "dense__huydang-dek21-embedding-768":
            assert cl["latency_by_repetition_ms"][0] == 20.0


def test_upsert_atomic_replace_failure_preserves_original(tmp_path, monkeypatch):
    results_path = tmp_path / "results.csv"
    cases_path = tmp_path / "cases.jsonl"

    s1 = _make_dummy_summary_rows(1, "dense__e5-small-384", p50=20.0)
    c1 = _make_dummy_case_records(1, "dense__e5-small-384", p50=20.0)
    upsert_input_artifacts("dense__e5-small-384", s1, c1, results_path=results_path, cases_path=cases_path)

    orig_content = results_path.read_text(encoding="utf-8")

    def fake_replace(src, dst):
        raise OSError("disk error")

    monkeypatch.setattr("os.replace", fake_replace)

    s1_new = _make_dummy_summary_rows(1, "dense__e5-small-384", p50=30.0)
    c1_new = _make_dummy_case_records(1, "dense__e5-small-384", p50=30.0)

    with pytest.raises(OSError, match="disk error"):
        upsert_input_artifacts("dense__e5-small-384", s1_new, c1_new, results_path=results_path, cases_path=cases_path)

    assert results_path.read_text(encoding="utf-8") == orig_content


def _prepare_test_artifacts(tmp_path: Path) -> tuple[Path, Path]:
    res_path = tmp_path / "phase8_reranker_results.csv"
    cases_path = tmp_path / "phase8_reranker_cases.jsonl"
    real_res = REPO_ROOT / "evaluation" / "results" / "phase8_reranker_results.csv"
    real_cases = REPO_ROOT / "evaluation" / "results" / "phase8_reranker_cases.jsonl"
    res_path.write_text(real_res.read_text(encoding="utf-8"), encoding="utf-8")
    cases_path.write_text(real_cases.read_text(encoding="utf-8"), encoding="utf-8")
    return res_path, cases_path


def test_reconcile_rejects_wrong_experiment_version(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    rows = list(csv.DictReader(res_path.open("r", encoding="utf-8")))
    for r in rows:
        r["experiment_version"] = "phase8-08c-v2"
    _atomic_csv(rows, res_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("experiment_version" in e for e in recon.errors)


def test_reconcile_rejects_summary_metric_tamper(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    rows = list(csv.DictReader(res_path.open("r", encoding="utf-8")))
    rows[0]["recall_at_5"] = "999"
    _atomic_csv(rows, res_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("recall_at_5 mismatch" in e for e in recon.errors)


def test_reconcile_rejects_case_metric_contradiction(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    cases = _read_jsonl(cases_path)
    cases[0]["hit_before"] = not cases[0]["hit_before"]
    _atomic_jsonl(cases, cases_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("hit_before contradiction" in e for e in recon.errors)


def test_reconcile_rejects_flag_tamper(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    rows = list(csv.DictReader(res_path.open("r", encoding="utf-8")))
    for r in rows:
        if r.get("state_key") == "minilm" and r.get("category") == "overall":
            r["eligible"] = "True"
            break
    _atomic_csv(rows, res_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("eligible mismatch" in e for e in recon.errors)


def test_reconcile_rejects_failed_status_as_complete(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    rows = list(csv.DictReader(res_path.open("r", encoding="utf-8")))
    rows[0]["status"] = "failed"
    _atomic_csv(rows, res_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("uncompleted status" in e for e in recon.errors)


def test_reconcile_rejects_bootstrap_ci_tamper(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    rows = list(csv.DictReader(res_path.open("r", encoding="utf-8")))
    for r in rows:
        if r.get("state_key") == "minilm" and r.get("category") == "overall":
            r["ndcg_ci_lower"] = "0.999"
            break
    _atomic_csv(rows, res_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("ndcg_ci_lower mismatch" in e for e in recon.errors)


def test_reconcile_rejects_successful_repetitions_tamper(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    cases = _read_jsonl(cases_path)
    cases[0]["successful_repetitions"] = 2
    _atomic_jsonl(cases, cases_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("successful_repetitions mismatch" in e for e in recon.errors)


def test_reconcile_rejects_ranking_stable_tamper(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    cases = _read_jsonl(cases_path)
    cases[0]["ranking_stable"] = False
    _atomic_jsonl(cases, cases_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("ranking_stable mismatch" in e for e in recon.errors)


def test_reconcile_rejects_state_order_tamper(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    rows = list(csv.DictReader(res_path.open("r", encoding="utf-8")))
    rows[0]["state_order"] = "2"
    _atomic_csv(rows, res_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("state_order mismatch" in e for e in recon.errors)


def test_reconcile_rejects_relevant_rank_tamper(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    cases = _read_jsonl(cases_path)
    first_key = list(cases[0]["relevant_rank_before"].keys())[0]
    cases[0]["relevant_rank_before"][first_key] = 99
    _atomic_jsonl(cases, cases_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("relevant_rank_before mismatch" in e for e in recon.errors)


def test_reconcile_rejects_pre_rerank_top_10_chunk_identity_tamper(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    cases = _read_jsonl(cases_path)
    cases[0]["pre_rerank_top_10"][0]["chunk_id"] = "corrupted_chunk_id"
    _atomic_jsonl(cases, cases_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("pre_rerank_top_10 chunk_id mismatch" in e for e in recon.errors)


def test_reconcile_rejects_minilm_top5_chunk_not_in_fixed_top10(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    cases = _read_jsonl(cases_path)
    case0_chunk_ids = {d["chunk_id"] for d in cases[0]["pre_rerank_top_10"]}
    foreign_chunk_id = None
    for d in cases[1]["pre_rerank_top_10"]:
        if d["chunk_id"] not in case0_chunk_ids:
            foreign_chunk_id = d["chunk_id"]
            break
    assert foreign_chunk_id is not None
    cases[0]["minilm_top_5"][0]["chunk_id"] = foreign_chunk_id
    _atomic_jsonl(cases, cases_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("not in fixed pre_rerank_top_10" in e for e in recon.errors)


def test_reconcile_rejects_summary_p95_latency_tamper(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    rows = list(csv.DictReader(res_path.open("r", encoding="utf-8")))
    for r in rows:
        if r.get("state_key") == "minilm" and r.get("category") == "overall":
            r["rerank_p95_ms"] = "9999.0"
            break
    _atomic_csv(rows, res_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("rerank_p95_ms mismatch" in e for e in recon.errors)


def test_reconcile_rejects_negative_or_nonfinite_case_latency(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    cases = _read_jsonl(cases_path)
    cases[0]["latency_by_repetition_ms"][0] = -5.0
    _atomic_jsonl(cases, cases_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("must be positive finite" in e for e in recon.errors)


def test_reconcile_rejects_negative_or_nonfinite_cold_load_ms(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    rows = list(csv.DictReader(res_path.open("r", encoding="utf-8")))
    for r in rows:
        if r.get("input_order") == "1" and r.get("state_key") == "minilm" and r.get("category") == "overall":
            r["cold_load_ms"] = "-10.0"
            break
    _atomic_csv(rows, res_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("cold_load_ms must be positive finite" in e for e in recon.errors)


# =========================================================================
# Complexity Reset: Non-Finite Numeric Normalization Probes (NaN, +Inf, -Inf)
# =========================================================================

@pytest.mark.parametrize("bad_val", ["nan", "NaN", "+inf", "-inf", "inf", "-Inf"])
def test_reconcile_rejects_case_metric_non_finite(tmp_path, bad_val):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    cases = _read_jsonl(cases_path)
    cases[0]["ndcg_at_5_after"] = bad_val
    _atomic_jsonl(cases, cases_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("non-finite float" in e for e in recon.errors)


@pytest.mark.parametrize("bad_val", ["nan", "NaN", "+inf", "-inf"])
def test_reconcile_rejects_case_latency_non_finite(tmp_path, bad_val):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    cases = _read_jsonl(cases_path)
    cases[0]["latency_by_repetition_ms"][0] = bad_val
    _atomic_jsonl(cases, cases_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("non-finite float" in e or "must be positive finite" in e for e in recon.errors)


@pytest.mark.parametrize("bad_val", ["nan", "NaN", "+inf", "-inf"])
def test_reconcile_rejects_summary_metric_non_finite(tmp_path, bad_val):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    rows = list(csv.DictReader(res_path.open("r", encoding="utf-8")))
    rows[0]["ndcg_at_5"] = bad_val
    _atomic_csv(rows, res_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("non-finite float" in e for e in recon.errors)


@pytest.mark.parametrize("bad_val", ["nan", "NaN", "+inf", "-inf"])
def test_reconcile_rejects_summary_delta_non_finite(tmp_path, bad_val):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    rows = list(csv.DictReader(res_path.open("r", encoding="utf-8")))
    for r in rows:
        if r.get("state_key") == "minilm" and r.get("category") == "overall":
            r["delta_ndcg_at_5"] = bad_val
            break
    _atomic_csv(rows, res_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("non-finite float" in e for e in recon.errors)


@pytest.mark.parametrize("bad_val", ["nan", "NaN", "+inf", "-inf"])
def test_reconcile_rejects_bootstrap_ci_non_finite(tmp_path, bad_val):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    rows = list(csv.DictReader(res_path.open("r", encoding="utf-8")))
    for r in rows:
        if r.get("state_key") == "minilm" and r.get("category") == "overall":
            r["ndcg_ci_lower"] = bad_val
            break
    _atomic_csv(rows, res_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("non-finite float" in e for e in recon.errors)


@pytest.mark.parametrize("bad_val", ["nan", "NaN", "+inf", "-inf"])
def test_reconcile_rejects_summary_latency_non_finite(tmp_path, bad_val):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    rows = list(csv.DictReader(res_path.open("r", encoding="utf-8")))
    for r in rows:
        if r.get("state_key") == "minilm" and r.get("category") == "overall":
            r["rerank_p50_ms"] = bad_val
            break
    _atomic_csv(rows, res_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("non-finite float" in e for e in recon.errors)


@pytest.mark.parametrize("bad_val", ["nan", "NaN", "+inf", "-inf"])
def test_reconcile_rejects_resource_metric_non_finite(tmp_path, bad_val):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    rows = list(csv.DictReader(res_path.open("r", encoding="utf-8")))
    for r in rows:
        if r.get("input_order") == "1" and r.get("state_key") == "minilm" and r.get("category") == "overall":
            r["cold_load_ms"] = bad_val
            break
    _atomic_csv(rows, res_path)

    recon = reconcile_reranker_artifacts(results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert any("non-finite float" in e or "must be positive finite" in e for e in recon.errors)


def test_truthful_failure_handling_preserves_no_rerank_control(tmp_path):
    res_path, cases_path = _prepare_test_artifacts(tmp_path)
    inputs = load_reranker_benchmark_inputs()
    _write_truthful_failure_for_all_inputs(
        inputs,
        "SimulatedError: model failed",
        results_path=res_path,
        cases_path=cases_path,
    )

    rows = list(csv.DictReader(res_path.open("r", encoding="utf-8")))
    assert len(rows) == 60
    no_rerank_rows = [r for r in rows if r["state_key"] == "no-rerank"]
    minilm_rows = [r for r in rows if r["state_key"] == "minilm"]

    assert len(no_rerank_rows) == 30
    assert len(minilm_rows) == 30

    for nr in no_rerank_rows:
        assert nr["status"] == "completed"
        assert float(nr["recall_at_5"]) > 0.0

    for mr in minilm_rows:
        assert mr["status"] == "failed"
        assert mr["error"] == "SimulatedError: model failed"
        assert mr["recall_at_5"] == ""

    recon = reconcile_reranker_artifacts(inputs=inputs, results_path=res_path, cases_path=cases_path)
    assert recon.complete is False
    assert recon.summary_rows == 60
    assert recon.case_records == 135
    assert any("uncompleted status" in e for e in recon.errors)


def test_08c_notebook_structure_and_clean_outputs():
    nb_path = REPO_ROOT / "notebooks" / "08c_reranker_benchmark.ipynb"
    assert nb_path.exists()
    notebook = json.loads(nb_path.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4
    code_cells = [cell for cell in notebook["cells"] if cell.get("cell_type") == "code"]
    assert len(notebook["cells"]) == 24
    assert len(code_cells) == 12

    # Check cell IDs
    for idx, cell in enumerate(notebook["cells"]):
        assert "id" in cell and isinstance(cell["id"], str) and len(cell["id"]) > 0, f"cell {idx} missing valid id"

    assert all(cell.get("execution_count") is None for cell in code_cells)
    assert all(cell.get("outputs") == [] for cell in code_cells)
    source = "\n".join("".join(cell["source"]) for cell in notebook["cells"])
    assert "load_reranker_benchmark_inputs" in source
    assert "run_all_reranker_inputs" in source
    assert "reconcile_reranker_artifacts" in source
    # Must NOT call load_runtime_reranker or run_technical_smoke directly in notebook cells
    code_source = "\n".join("".join(cell["source"]) for cell in code_cells)
    assert "load_runtime_reranker(" not in code_source
    assert "run_technical_smoke(" not in code_source
    assert "CrossEncoder(" not in source
    assert "Qwen" not in source
    assert "bge-reranker" not in source
