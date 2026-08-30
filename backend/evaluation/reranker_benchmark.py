"""Phase 8 — Notebook 08c: MiniLM Reranker Benchmark module.

Evaluates applying local cross-encoder `cross-encoder/ms-marco-MiniLM-L-6-v2` on fixed
Top-10 retrieval inputs from Phase 8 Notebook 08b on Golden Dataset V3 (45 cases) and
572 canonical Hue foods chunks.
"""

from __future__ import annotations

import csv
import gc
import json
import os
import psutil
import re
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from core.schema import RetrievedDocument
from evaluation.embedding_benchmark import (
    BootstrapInterval,
    CaseMetrics,
    aggregate_case_metrics,
    evaluate_category_guardrails,
    paired_bootstrap_intervals,
    score_retrieval_case,
)
from evaluation.golden_dataset import (
    GoldenCase,
    KB_ROOT,
    V3_FULL_PATH,
    V3_SMOKE_PATH,
    load_golden,
    validate_v3_full,
    validate_v3_smoke,
)
from evaluation.sparse_benchmark import (
    CHUNKER_PATH,
    DEFAULT_RESULTS_DIR,
    REPO_ROOT,
    fingerprint_chunker_code,
    fingerprint_corpus,
    fingerprint_golden,
    sanitize_error_message,
)
from ingestion.chunking.markdown_chunker import chunk_foods_markdown
from reranking.cross_encoder import CrossEncoderReranker
from vectorstore.points import validate_chunks

SPARSE_MANIFEST_PATH = DEFAULT_RESULTS_DIR / "phase8_sparse_manifest.json"
SPARSE_CASES_PATH = DEFAULT_RESULTS_DIR / "phase8_sparse_cases.jsonl"
RESULTS_PATH = DEFAULT_RESULTS_DIR / "phase8_reranker_results.csv"
CASES_PATH = DEFAULT_RESULTS_DIR / "phase8_reranker_cases.jsonl"
EXPERIMENT_VERSION = "phase8-08c-v1"
SOURCE_EXPERIMENT_VERSION = "phase8-08b-v1"
MODEL_ID = "cross-encoder/ms-marco-MiniLM-L-6-v2"

RESULT_COLUMNS = (
    "experiment_version",
    "input_order",
    "input_key",
    "input_label",
    "state_order",
    "state_key",
    "model_id",
    "model_revision",
    "category",
    "status",
    "error",
    "case_count",
    "hit_case_count",
    "successful_repetitions",
    "ranking_stable",
    "recall_at_5",
    "mrr_at_5",
    "ndcg_at_5",
    "delta_recall_at_5",
    "delta_mrr_at_5",
    "delta_ndcg_at_5",
    "recall_ci_lower",
    "recall_ci_upper",
    "mrr_ci_lower",
    "mrr_ci_upper",
    "ndcg_ci_lower",
    "ndcg_ci_upper",
    "category_guardrail_pass",
    "all_category_guardrails_pass",
    "eligible",
    "clear_gain",
    "production_safety",
    "cold_load_ms",
    "rerank_p50_ms",
    "rerank_p95_ms",
    "rss_before_load_mb",
    "rss_after_load_mb",
    "observed_peak_rss_mb",
    "device",
    "dtype",
)

CASE_RECORD_FIELDS = (
    "experiment_version",
    "input_order",
    "input_key",
    "case_id",
    "category",
    "status",
    "error",
    "relevant_source_sections",
    "pre_rerank_top_10",
    "no_rerank_top_5",
    "minilm_top_5",
    "successful_repetitions",
    "ranking_stable",
    "hit_before",
    "hit_after",
    "hit_change",
    "relevant_rank_before",
    "relevant_rank_after",
    "recall_at_5_before",
    "recall_at_5_after",
    "mrr_at_5_before",
    "mrr_at_5_after",
    "ndcg_at_5_before",
    "ndcg_at_5_after",
    "latency_by_repetition_ms",
)

GOLDEN_CATEGORIES = (
    "direct_fact",
    "temporal",
    "comparative",
    "numerical",
    "relationship",
    "spanning",
    "holistic",
    "food_knowledge",
    "guide_planning",
)
SORTED_GOLDEN_CATEGORIES = tuple(sorted(GOLDEN_CATEGORIES))


@dataclass(frozen=True)
class RerankerInputSetting:
    order: int
    key: str
    label: str
    source_setting_key: str


INPUT_SETTINGS: tuple[RerankerInputSetting, ...] = (
    RerankerInputSetting(
        order=1,
        key="dense__e5-small-384",
        label="Dense E5-Small (384d)",
        source_setting_key="dense__e5-small-384",
    ),
    RerankerInputSetting(
        order=2,
        key="dense__huydang-dek21-embedding-768",
        label="Dense HuyDang (768d)",
        source_setting_key="dense__huydang-dek21-embedding-768",
    ),
    RerankerInputSetting(
        order=3,
        key="hybrid-bm25-weighted__huydang-dek21-embedding-768",
        label="Hybrid BM25 Weighted + HuyDang (768d)",
        source_setting_key="hybrid-bm25-weighted__huydang-dek21-embedding-768",
    ),
)


@dataclass(frozen=True)
class FixedRerankerCase:
    input_order: int
    input_key: str
    case: GoldenCase
    relevant_source_sections: tuple[tuple[str, str], ...]
    derived_relevant_chunk_ids: tuple[str, ...]
    pre_rerank_documents: tuple[RetrievedDocument, ...]


@dataclass(frozen=True)
class RerankerBenchmarkInputs:
    manifest: dict
    cases: tuple[GoldenCase, ...]
    smoke_case_ids: tuple[str, ...]
    chunks_by_id: dict[str, dict]
    fixed_cases: tuple[FixedRerankerCase, ...]


@dataclass(frozen=True)
class RuntimeEvidence:
    model_id: str
    model_revision: str
    device: str
    dtype: str
    cold_load_ms: float
    rss_before_load_mb: float
    rss_after_load_mb: float
    observed_peak_rss_mb: float


@dataclass(frozen=True)
class PairedCaseEvidence:
    case_id: str
    category: str
    before: CaseMetrics
    after: CaseMetrics
    hit_change: str
    relevant_rank_before: dict[str, int | None]
    relevant_rank_after: dict[str, int | None]


@dataclass(frozen=True)
class InputEvidence:
    paired_cases: tuple[PairedCaseEvidence, ...]
    before_metrics: tuple[CaseMetrics, ...]
    after_metrics: tuple[CaseMetrics, ...]
    aggregates_before: dict[str, dict[str, float]]
    aggregates_after: dict[str, dict[str, float]]
    deltas: dict[str, dict[str, float]]
    bootstrap_intervals: dict[str, BootstrapInterval]
    category_guardrail_passes: dict[str, bool]
    all_category_guardrails_pass: bool
    successful_repetitions: int
    ranking_stable: bool
    rerank_p95_ms: float
    eligible: bool
    clear_gain: bool


@dataclass(frozen=True)
class InputRunResult:
    input_key: str
    status: str
    error: str
    summary_rows: tuple[dict, ...]
    case_records: tuple[dict, ...]
    evidence: InputEvidence | None


@dataclass(frozen=True)
class ReconciliationResult:
    complete: bool
    summary_rows: int
    case_records: int
    errors: tuple[str, ...]


def _rss_mb(process: psutil.Process | None = None) -> float:
    p = process or psutil.Process()
    return float(p.memory_info().rss / (1024 * 1024))


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if line_str:
                records.append(json.loads(line_str))
    return records


def _atomic_jsonl(records: Sequence[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as tmp:
        for r in records:
            tmp.write(json.dumps(r, ensure_ascii=False) + "\n")
        tmp_name = tmp.name
    os.replace(tmp_name, path)


def _atomic_csv(rows: Sequence[dict], path: Path, columns: Sequence[str] = RESULT_COLUMNS) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8", newline="") as tmp:
        writer = csv.DictWriter(tmp, fieldnames=columns)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
        tmp_name = tmp.name
    os.replace(tmp_name, path)


def _relevant_ranks(
    declared_relevant: Sequence[tuple[str, str]],
    docs: Sequence[RetrievedDocument],
) -> dict[str, int | None]:
    result: dict[str, int | None] = {}
    for source, section in declared_relevant:
        key = f"{source}::{section}"
        matched_rank: int | None = None
        for rank, doc in enumerate(docs, start=1):
            if doc.metadata.get("source") == source and doc.metadata.get("section") == section:
                matched_rank = rank
                break
        result[key] = matched_rank
    return result


def score_fixed_pair(
    case: GoldenCase,
    no_rerank_docs: Sequence[RetrievedDocument],
    minilm_docs: Sequence[RetrievedDocument],
) -> PairedCaseEvidence:
    before = score_retrieval_case(case, list(no_rerank_docs), k=5)
    after = score_retrieval_case(case, list(minilm_docs), k=5)

    if not before.hit and after.hit:
        hit_change = "gained"
    elif before.hit and not after.hit:
        hit_change = "lost"
    elif before.hit and after.hit:
        hit_change = "unchanged_hit"
    else:
        hit_change = "unchanged_miss"

    declared_relevant = tuple(
        (source, section)
        for source, sections in sorted(case.evidence.items())
        for section in sorted(sections)
    )

    rank_before = _relevant_ranks(declared_relevant, no_rerank_docs)
    rank_after = _relevant_ranks(declared_relevant, minilm_docs)

    return PairedCaseEvidence(
        case_id=case.case_id,
        category=case.category,
        before=before,
        after=after,
        hit_change=hit_change,
        relevant_rank_before=rank_before,
        relevant_rank_after=rank_after,
    )


def evaluate_input_evidence(
    paired_cases: Sequence[PairedCaseEvidence],
    *,
    successful_repetitions: int,
    ranking_stable: bool,
    rerank_p95_ms: float,
) -> InputEvidence:
    before_metrics = tuple(p.before for p in paired_cases)
    after_metrics = tuple(p.after for p in paired_cases)

    agg_before = aggregate_case_metrics(list(before_metrics))
    agg_after = aggregate_case_metrics(list(after_metrics))

    all_categories = ("overall",) + GOLDEN_CATEGORIES
    deltas: dict[str, dict[str, float]] = {}
    for cat in all_categories:
        deltas[cat] = {
            "delta_recall_at_5": agg_after[cat]["recall_at_5"] - agg_before[cat]["recall_at_5"],
            "delta_mrr_at_5": agg_after[cat]["mrr_at_5"] - agg_before[cat]["mrr_at_5"],
            "delta_ndcg_at_5": agg_after[cat]["ndcg_at_5"] - agg_before[cat]["ndcg_at_5"],
        }

    bootstrap = paired_bootstrap_intervals(list(before_metrics), list(after_metrics), seed=42, samples=10000)
    guardrail_passes = evaluate_category_guardrails(list(before_metrics), list(after_metrics))
    all_guardrails = all(guardrail_passes.values())

    eligible = (
        successful_repetitions == 3
        and ranking_stable
        and all_guardrails
        and (rerank_p95_ms <= 3000.0)
    )
    delta_ndcg_overall = deltas["overall"]["delta_ndcg_at_5"]
    ndcg_ci_lower = bootstrap["ndcg"].lower
    clear_gain = eligible and (delta_ndcg_overall >= 0.03) and (ndcg_ci_lower > 0.0)

    return InputEvidence(
        paired_cases=tuple(paired_cases),
        before_metrics=before_metrics,
        after_metrics=after_metrics,
        aggregates_before=agg_before,
        aggregates_after=agg_after,
        deltas=deltas,
        bootstrap_intervals=bootstrap,
        category_guardrail_passes=guardrail_passes,
        all_category_guardrails_pass=all_guardrails,
        successful_repetitions=successful_repetitions,
        ranking_stable=ranking_stable,
        rerank_p95_ms=rerank_p95_ms,
        eligible=eligible,
        clear_gain=clear_gain,
    )


def evaluate_production_safety(
    candidate_metrics: Sequence[CaseMetrics],
    production_reference_metrics: Sequence[CaseMetrics],
) -> bool:
    if len(candidate_metrics) != len(production_reference_metrics):
        raise ValueError("candidate and production reference metrics count mismatch")
    cand_agg = aggregate_case_metrics(list(candidate_metrics))
    ref_agg = aggregate_case_metrics(list(production_reference_metrics))

    cand_recall = cand_agg["overall"]["recall_at_5"]
    ref_recall = ref_agg["overall"]["recall_at_5"]
    if cand_recall < (ref_recall - 0.005):
        return False

    guardrails = evaluate_category_guardrails(list(production_reference_metrics), list(candidate_metrics))
    return all(guardrails.values())


def validate_reranker_inputs(
    *,
    manifest: dict,
    sparse_case_records: Sequence[dict],
    cases: Sequence[GoldenCase],
    smoke_cases: Sequence[GoldenCase],
    chunks: Sequence,
) -> RerankerBenchmarkInputs:
    validate_v3_full(list(cases))
    validate_v3_smoke(list(cases), list(smoke_cases))
    validate_chunks(chunks)

    if manifest.get("experiment_version") != SOURCE_EXPERIMENT_VERSION:
        raise ValueError(
            f"expected source manifest version {SOURCE_EXPERIMENT_VERSION}, got {manifest.get('experiment_version')}"
        )

    corpus_fp = fingerprint_corpus(chunks)
    golden_fp = fingerprint_golden(cases)
    chunker_fp = fingerprint_chunker_code(CHUNKER_PATH)

    immutable_id = manifest.get("immutable_identity", manifest)
    if immutable_id.get("corpus_fingerprint") != corpus_fp:
        raise ValueError("corpus fingerprint mismatch against 08b manifest")
    if (immutable_id.get("golden_fingerprint") or immutable_id.get("golden_v3_fingerprint")) != golden_fp:
        raise ValueError("golden fingerprint mismatch against 08b manifest")
    if immutable_id.get("chunker_fingerprint") != chunker_fp:
        raise ValueError("chunker fingerprint mismatch against 08b manifest")

    smoke_ids = tuple(sc.case_id for sc in smoke_cases)
    if len(smoke_ids) != 10:
        raise ValueError(f"expected 10 smoke cases, got {len(smoke_ids)}")
    case_ids = {c.case_id for c in cases}
    if not set(smoke_ids).issubset(case_ids):
        raise ValueError("smoke case IDs are not a subset of Golden V3 cases")

    chunks_by_id = {
        str(c["metadata"]["chunk_id"]): {
            "id": str(c["metadata"]["chunk_id"]),
            "text": str(c["text"]),
            "metadata": dict(c["metadata"]),
        }
        for c in chunks
    }

    expected_setting_keys = {setting.key for setting in INPUT_SETTINGS}
    cases_by_setting: dict[str, list[dict]] = {k: [] for k in expected_setting_keys}
    for record in sparse_case_records:
        setting_key = record.get("setting_key")
        if setting_key in cases_by_setting:
            cases_by_setting[setting_key].append(record)

    golden_cases_by_id = {c.case_id: c for c in cases}
    fixed_cases_list: list[FixedRerankerCase] = []

    for setting in INPUT_SETTINGS:
        records = cases_by_setting[setting.key]
        if len(records) != 45:
            raise ValueError(f"expected 45 records for {setting.key}, found {len(records)}")

        seen_case_ids = set()
        for rec in records:
            if rec.get("status") != "completed":
                raise ValueError(f"uncompleted status in sparse record: {rec.get('case_id')}")
            cid = rec.get("case_id")
            if cid in seen_case_ids:
                raise ValueError(f"duplicate case_id {cid} in setting {setting.key}")
            seen_case_ids.add(cid)

            golden_case = golden_cases_by_id.get(cid)
            if golden_case is None:
                raise ValueError(f"unknown case_id {cid} not found in Golden V3")
            if rec.get("category") != golden_case.category:
                raise ValueError(f"category mismatch for case {cid}: {rec.get('category')} vs {golden_case.category}")

            top_10_raw = rec.get("fusion_top_10") or rec.get("top_10") or []
            if len(top_10_raw) != 10:
                raise ValueError(f"case {cid} in setting {setting.key} does not have exactly 10 candidate chunks")

            pre_docs = []
            seen_chunks = set()
            for r_idx, item in enumerate(top_10_raw, start=1):
                chunk_id = item.get("chunk_id")
                if chunk_id in seen_chunks:
                    raise ValueError(f"duplicate chunk_id {chunk_id} in top_10 of case {cid}")
                seen_chunks.add(chunk_id)

                if item.get("rank") != r_idx:
                    raise ValueError(f"invalid rank ordering for chunk {chunk_id} in case {cid}")

                canonical_chunk = chunks_by_id.get(chunk_id)
                if canonical_chunk is None:
                    raise ValueError(f"chunk_id {chunk_id} not found in 572 canonical chunks")

                metadata = dict(canonical_chunk["metadata"])
                metadata["text"] = canonical_chunk["text"]

                raw_score = item.get("fused_score") if item.get("fused_score") is not None else item.get("score", 0.0)
                pre_docs.append(
                    RetrievedDocument(
                        id=canonical_chunk["id"],
                        text=canonical_chunk["text"],
                        score=float(raw_score or 0.0),
                        metadata=metadata,
                    )
                )

            declared_relevant = tuple(
                (source, section)
                for source, sections in sorted(golden_case.evidence.items())
                for section in sorted(sections)
            )
            derived_relevant_ids = tuple(
                chunk_id
                for chunk_id, c in chunks_by_id.items()
                if (c["metadata"].get("source"), c["metadata"].get("section")) in declared_relevant
            )

            fixed_cases_list.append(
                FixedRerankerCase(
                    input_order=setting.order,
                    input_key=setting.key,
                    case=golden_case,
                    relevant_source_sections=declared_relevant,
                    derived_relevant_chunk_ids=derived_relevant_ids,
                    pre_rerank_documents=tuple(pre_docs),
                )
            )

    return RerankerBenchmarkInputs(
        manifest=manifest,
        cases=tuple(cases),
        smoke_case_ids=smoke_ids,
        chunks_by_id=chunks_by_id,
        fixed_cases=tuple(fixed_cases_list),
    )


def load_reranker_benchmark_inputs(
    *,
    manifest_path: Path = SPARSE_MANIFEST_PATH,
    sparse_cases_path: Path = SPARSE_CASES_PATH,
    golden_path: Path = V3_FULL_PATH,
    smoke_path: Path = V3_SMOKE_PATH,
) -> RerankerBenchmarkInputs:
    if not manifest_path.exists():
        raise FileNotFoundError(f"08b sparse manifest not found at {manifest_path}")
    if not sparse_cases_path.exists():
        raise FileNotFoundError(f"08b sparse cases not found at {sparse_cases_path}")
    if not golden_path.exists():
        raise FileNotFoundError(f"golden dataset not found at {golden_path}")
    if not smoke_path.exists():
        raise FileNotFoundError(f"smoke dataset not found at {smoke_path}")

    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    sparse_cases = _read_jsonl(sparse_cases_path)
    cases = load_golden(golden_path)
    smoke_cases = load_golden(smoke_path)
    chunks = chunk_foods_markdown()

    return validate_reranker_inputs(
        manifest=manifest,
        sparse_case_records=sparse_cases,
        cases=cases,
        smoke_cases=smoke_cases,
        chunks=chunks,
    )


def upsert_input_artifacts(
    input_key: str,
    summary_rows: Sequence[dict],
    case_records: Sequence[dict],
    *,
    results_path: Path = RESULTS_PATH,
    cases_path: Path = CASES_PATH,
) -> None:
    if input_key not in {setting.key for setting in INPUT_SETTINGS}:
        raise ValueError(f"unapproved input key: {input_key}")
    if len(summary_rows) != 20 or {row.get("input_key") for row in summary_rows} != {input_key}:
        raise ValueError("each input must provide exactly 20 summary rows")
    if len(case_records) != 45 or {row.get("input_key") for row in case_records} != {input_key}:
        raise ValueError("each input must provide exactly 45 case records")

    existing_summary = []
    if results_path.exists():
        with results_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != RESULT_COLUMNS:
                raise ValueError("existing reranker CSV schema mismatch")
            existing_summary = [row for row in reader if row.get("input_key") != input_key]
    existing_cases = [row for row in _read_jsonl(cases_path) if row.get("input_key") != input_key] if cases_path.exists() else []

    all_summary = existing_summary + list(summary_rows)
    all_cases = existing_cases + list(case_records)
    all_summary.sort(key=lambda row: (int(row["input_order"]), int(row["state_order"]), row["category"] != "overall", row["category"]))
    all_cases.sort(key=lambda row: (int(row["input_order"]), row["case_id"]))
    _atomic_csv(all_summary, results_path)
    _atomic_jsonl(all_cases, cases_path)


def load_runtime_reranker() -> tuple[CrossEncoderReranker, RuntimeEvidence]:
    process = psutil.Process()
    gc.collect()
    rss_before = _rss_mb(process)

    reranker = CrossEncoderReranker()
    t0 = time.perf_counter_ns()
    reranker.load()
    t1 = time.perf_counter_ns()

    cold_load_ms = (t1 - t0) / 1_000_000
    rss_after = _rss_mb(process)

    evidence = RuntimeEvidence(
        model_id=MODEL_ID,
        model_revision="not_reported",
        device=str(reranker._device),
        dtype="float32",
        cold_load_ms=cold_load_ms,
        rss_before_load_mb=rss_before,
        rss_after_load_mb=rss_after,
        observed_peak_rss_mb=max(rss_before, rss_after),
    )
    return reranker, evidence


def run_technical_smoke(
    inputs: RerankerBenchmarkInputs,
    reranker: CrossEncoderReranker,
) -> dict:
    smoke_ids = set(inputs.smoke_case_ids)
    setting1_cases = [fc for fc in inputs.fixed_cases if fc.input_order == 1 and fc.case.case_id in smoke_ids]
    if len(setting1_cases) != 10:
        raise ValueError(f"expected 10 smoke cases in setting 1, found {len(setting1_cases)}")

    for fc in setting1_cases:
        res = reranker.rerank(fc.case.question, list(fc.pre_rerank_documents), top_k=5)
        if len(res) != 5:
            raise RuntimeError("smoke rerank returned invalid length")
    return {"status": "passed", "smoke_cases_count": 10}


def run_reranker_input(
    inputs: RerankerBenchmarkInputs,
    input_setting: RerankerInputSetting,
    reranker: CrossEncoderReranker,
    runtime_evidence: RuntimeEvidence,
    *,
    results_path: Path = RESULTS_PATH,
    cases_path: Path = CASES_PATH,
) -> InputRunResult:
    fixed_cases = [fc for fc in inputs.fixed_cases if fc.input_key == input_setting.key]
    fixed_cases.sort(key=lambda fc: fc.case.case_id)
    if len(fixed_cases) != 45:
        raise ValueError(f"expected 45 cases for {input_setting.key}, found {len(fixed_cases)}")

    # 1. Always evaluate fixed no-rerank control truthfully
    before_metrics = [
        score_retrieval_case(fc.case, list(fc.pre_rerank_documents[:5]), k=5)
        for fc in fixed_cases
    ]
    agg_before = aggregate_case_metrics(before_metrics)

    all_categories = ("overall",) + SORTED_GOLDEN_CATEGORIES
    no_rerank_summary_rows = []
    for cat in all_categories:
        agg = agg_before[cat]
        no_rerank_summary_rows.append({
            "experiment_version": EXPERIMENT_VERSION,
            "input_order": input_setting.order,
            "input_key": input_setting.key,
            "input_label": input_setting.label,
            "state_order": 1,
            "state_key": "no-rerank",
            "model_id": "",
            "model_revision": "",
            "category": cat,
            "status": "completed",
            "error": "",
            "case_count": agg["case_count"],
            "hit_case_count": agg["hit_case_count"],
            "successful_repetitions": "",
            "ranking_stable": "",
            "recall_at_5": agg["recall_at_5"],
            "mrr_at_5": agg["mrr_at_5"],
            "ndcg_at_5": agg["ndcg_at_5"],
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
            "eligible": "",
            "clear_gain": "",
            "production_safety": "",
            "cold_load_ms": "",
            "rerank_p50_ms": "",
            "rerank_p95_ms": "",
            "rss_before_load_mb": "",
            "rss_after_load_mb": "",
            "observed_peak_rss_mb": "",
            "device": "",
            "dtype": "",
        })

    # 2. Run MiniLM on candidates with truthful error boundary
    successful_reps = 0
    reps_docs: list[list[list[RetrievedDocument]]] = []
    reps_latencies: list[list[float]] = []

    try:
        for rep in range(3):
            rep_docs: list[list[RetrievedDocument]] = []
            rep_lats: list[float] = []
            for fc in fixed_cases:
                t0 = time.perf_counter_ns()
                docs = reranker.rerank(fc.case.question, list(fc.pre_rerank_documents), top_k=5)
                t1 = time.perf_counter_ns()
                lat_ms = (t1 - t0) / 1_000_000
                rep_lats.append(lat_ms)
                rep_docs.append(docs)
            reps_docs.append(rep_docs)
            reps_latencies.append(rep_lats)
            successful_reps += 1

        # Check stability across 3 repetitions
        ranking_stable = True
        for i in range(45):
            order0 = tuple(d.id for d in reps_docs[0][i])
            order1 = tuple(d.id for d in reps_docs[1][i])
            order2 = tuple(d.id for d in reps_docs[2][i])
            if order0 != order1 or order0 != order2:
                ranking_stable = False
                break

        latencies_all = [lat for rep_lat in reps_latencies for lat in rep_lat]
        rerank_p50_ms = float(np.percentile(latencies_all, 50))
        rerank_p95_ms = float(np.percentile(latencies_all, 95))

        paired_cases = []
        for i, fc in enumerate(fixed_cases):
            no_rerank_docs = fc.pre_rerank_documents[:5]
            minilm_docs = reps_docs[0][i]
            paired = score_fixed_pair(fc.case, no_rerank_docs, minilm_docs)
            paired_cases.append(paired)

        evidence = evaluate_input_evidence(
            paired_cases,
            successful_repetitions=3,
            ranking_stable=ranking_stable,
            rerank_p95_ms=rerank_p95_ms,
        )

        production_safety = None
        if input_setting.order == 3:
            e5_fixed = [fc for fc in inputs.fixed_cases if fc.input_order == 1]
            e5_fixed.sort(key=lambda fc: fc.case.case_id)
            e5_no_rerank_metrics = [
                score_retrieval_case(fc.case, list(fc.pre_rerank_documents[:5]), k=5)
                for fc in e5_fixed
            ]
            production_safety = evaluate_production_safety(evidence.after_metrics, e5_no_rerank_metrics)

        minilm_summary_rows = []
        for cat in all_categories:
            agg = evidence.aggregates_after[cat]
            delta = evidence.deltas[cat]
            is_overall = cat == "overall"
            minilm_summary_rows.append({
                "experiment_version": EXPERIMENT_VERSION,
                "input_order": input_setting.order,
                "input_key": input_setting.key,
                "input_label": input_setting.label,
                "state_order": 2,
                "state_key": "minilm",
                "model_id": runtime_evidence.model_id,
                "model_revision": runtime_evidence.model_revision,
                "category": cat,
                "status": "completed",
                "error": "",
                "case_count": agg["case_count"],
                "hit_case_count": agg["hit_case_count"],
                "successful_repetitions": 3 if is_overall else "",
                "ranking_stable": evidence.ranking_stable if is_overall else "",
                "recall_at_5": agg["recall_at_5"],
                "mrr_at_5": agg["mrr_at_5"],
                "ndcg_at_5": agg["ndcg_at_5"],
                "delta_recall_at_5": delta["delta_recall_at_5"],
                "delta_mrr_at_5": delta["delta_mrr_at_5"],
                "delta_ndcg_at_5": delta["delta_ndcg_at_5"],
                "recall_ci_lower": evidence.bootstrap_intervals["recall"].lower if is_overall else "",
                "recall_ci_upper": evidence.bootstrap_intervals["recall"].upper if is_overall else "",
                "mrr_ci_lower": evidence.bootstrap_intervals["mrr"].lower if is_overall else "",
                "mrr_ci_upper": evidence.bootstrap_intervals["mrr"].upper if is_overall else "",
                "ndcg_ci_lower": evidence.bootstrap_intervals["ndcg"].lower if is_overall else "",
                "ndcg_ci_upper": evidence.bootstrap_intervals["ndcg"].upper if is_overall else "",
                "category_guardrail_pass": "" if is_overall else evidence.category_guardrail_passes[cat],
                "all_category_guardrails_pass": evidence.all_category_guardrails_pass if is_overall else "",
                "eligible": evidence.eligible if is_overall else "",
                "clear_gain": evidence.clear_gain if is_overall else "",
                "production_safety": production_safety if (is_overall and input_setting.order == 3) else "",
                "cold_load_ms": runtime_evidence.cold_load_ms if (is_overall and input_setting.order == 1) else "",
                "rerank_p50_ms": rerank_p50_ms if is_overall else "",
                "rerank_p95_ms": rerank_p95_ms if is_overall else "",
                "rss_before_load_mb": runtime_evidence.rss_before_load_mb if (is_overall and input_setting.order == 1) else "",
                "rss_after_load_mb": runtime_evidence.rss_after_load_mb if (is_overall and input_setting.order == 1) else "",
                "observed_peak_rss_mb": runtime_evidence.observed_peak_rss_mb if (is_overall and input_setting.order == 1) else "",
                "device": runtime_evidence.device if is_overall else "",
                "dtype": runtime_evidence.dtype if is_overall else "",
            })

        case_records = []
        for i, fc in enumerate(fixed_cases):
            p = paired_cases[i]
            case_latencies = [reps_latencies[r][i] for r in range(3)]
            case_records.append({
                "experiment_version": EXPERIMENT_VERSION,
                "input_order": input_setting.order,
                "input_key": input_setting.key,
                "case_id": fc.case.case_id,
                "category": fc.case.category,
                "status": "completed",
                "error": "",
                "relevant_source_sections": [
                    {"source": s, "section": sec} for s, sec in fc.relevant_source_sections
                ],
                "pre_rerank_top_10": [
                    {"chunk_id": doc.id, "rank": r, "score": doc.score, "source": doc.metadata.get("source"), "section": doc.metadata.get("section")}
                    for r, doc in enumerate(fc.pre_rerank_documents, start=1)
                ],
                "no_rerank_top_5": [
                    {"chunk_id": doc.id, "rank": r, "score": doc.score, "source": doc.metadata.get("source"), "section": doc.metadata.get("section")}
                    for r, doc in enumerate(fc.pre_rerank_documents[:5], start=1)
                ],
                "minilm_top_5": [
                    {"chunk_id": doc.id, "rank": r, "score": doc.score, "source": doc.metadata.get("source"), "section": doc.metadata.get("section")}
                    for r, doc in enumerate(reps_docs[0][i], start=1)
                ],
                "successful_repetitions": 3,
                "ranking_stable": ranking_stable,
                "hit_before": p.before.hit,
                "hit_after": p.after.hit,
                "hit_change": p.hit_change,
                "relevant_rank_before": p.relevant_rank_before,
                "relevant_rank_after": p.relevant_rank_after,
                "recall_at_5_before": p.before.recall_at_5,
                "recall_at_5_after": p.after.recall_at_5,
                "mrr_at_5_before": p.before.mrr_at_5,
                "mrr_at_5_after": p.after.mrr_at_5,
                "ndcg_at_5_before": p.before.ndcg_at_5,
                "ndcg_at_5_after": p.after.ndcg_at_5,
                "latency_by_repetition_ms": case_latencies,
            })

        summary_rows = no_rerank_summary_rows + minilm_summary_rows
        upsert_input_artifacts(
            input_setting.key,
            summary_rows,
            case_records,
            results_path=results_path,
            cases_path=cases_path,
        )

        return InputRunResult(
            input_key=input_setting.key,
            status="completed",
            error="",
            summary_rows=tuple(summary_rows),
            case_records=tuple(case_records),
            evidence=evidence,
        )
    except Exception as exc:
        sanitized = sanitize_error_message(exc)
        # Truthful failed MiniLM summary rows
        minilm_summary_rows = []
        for cat in all_categories:
            minilm_summary_rows.append({
                "experiment_version": EXPERIMENT_VERSION,
                "input_order": input_setting.order,
                "input_key": input_setting.key,
                "input_label": input_setting.label,
                "state_order": 2,
                "state_key": "minilm",
                "model_id": runtime_evidence.model_id,
                "model_revision": runtime_evidence.model_revision,
                "category": cat,
                "status": "failed",
                "error": sanitized,
                "case_count": agg_before[cat]["case_count"],
                "hit_case_count": "",
                "successful_repetitions": successful_reps if cat == "overall" else "",
                "ranking_stable": "",
                "recall_at_5": "",
                "mrr_at_5": "",
                "ndcg_at_5": "",
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
                "eligible": "",
                "clear_gain": "",
                "production_safety": "",
                "cold_load_ms": "",
                "rerank_p50_ms": "",
                "rerank_p95_ms": "",
                "rss_before_load_mb": "",
                "rss_after_load_mb": "",
                "observed_peak_rss_mb": "",
                "device": "",
                "dtype": "",
            })

        case_records = []
        for i, fc in enumerate(fixed_cases):
            bm = before_metrics[i]
            rank_before = _relevant_ranks(fc.relevant_source_sections, fc.pre_rerank_documents[:5])
            case_latencies = [reps_latencies[r][i] for r in range(successful_reps)]
            case_records.append({
                "experiment_version": EXPERIMENT_VERSION,
                "input_order": input_setting.order,
                "input_key": input_setting.key,
                "case_id": fc.case.case_id,
                "category": fc.case.category,
                "status": "failed",
                "error": sanitized,
                "relevant_source_sections": [
                    {"source": s, "section": sec} for s, sec in fc.relevant_source_sections
                ],
                "pre_rerank_top_10": [
                    {"chunk_id": doc.id, "rank": r, "score": doc.score, "source": doc.metadata.get("source"), "section": doc.metadata.get("section")}
                    for r, doc in enumerate(fc.pre_rerank_documents, start=1)
                ],
                "no_rerank_top_5": [
                    {"chunk_id": doc.id, "rank": r, "score": doc.score, "source": doc.metadata.get("source"), "section": doc.metadata.get("section")}
                    for r, doc in enumerate(fc.pre_rerank_documents[:5], start=1)
                ],
                "minilm_top_5": [],
                "successful_repetitions": successful_reps,
                "ranking_stable": "",
                "hit_before": bm.hit,
                "hit_after": "",
                "hit_change": "",
                "relevant_rank_before": rank_before,
                "relevant_rank_after": {},
                "recall_at_5_before": bm.recall_at_5,
                "recall_at_5_after": "",
                "mrr_at_5_before": bm.mrr_at_5,
                "mrr_at_5_after": "",
                "ndcg_at_5_before": bm.ndcg_at_5,
                "ndcg_at_5_after": "",
                "latency_by_repetition_ms": case_latencies,
            })

        summary_rows = no_rerank_summary_rows + minilm_summary_rows
        upsert_input_artifacts(
            input_setting.key,
            summary_rows,
            case_records,
            results_path=results_path,
            cases_path=cases_path,
        )

        return InputRunResult(
            input_key=input_setting.key,
            status="failed",
            error=sanitized,
            summary_rows=tuple(summary_rows),
            case_records=tuple(case_records),
            evidence=None,
        )


def _write_truthful_failure_for_all_inputs(
    inputs: RerankerBenchmarkInputs,
    error: str,
    *,
    results_path: Path = RESULTS_PATH,
    cases_path: Path = CASES_PATH,
) -> None:
    all_categories = ("overall",) + SORTED_GOLDEN_CATEGORIES
    for setting in INPUT_SETTINGS:
        fixed_cases = [fc for fc in inputs.fixed_cases if fc.input_key == setting.key]
        fixed_cases.sort(key=lambda fc: fc.case.case_id)

        before_metrics = [
            score_retrieval_case(fc.case, list(fc.pre_rerank_documents[:5]), k=5)
            for fc in fixed_cases
        ]
        agg_before = aggregate_case_metrics(before_metrics)

        no_rerank_summary_rows = []
        minilm_summary_rows = []
        for cat in all_categories:
            agg = agg_before[cat]
            no_rerank_summary_rows.append({
                "experiment_version": EXPERIMENT_VERSION,
                "input_order": setting.order,
                "input_key": setting.key,
                "input_label": setting.label,
                "state_order": 1,
                "state_key": "no-rerank",
                "model_id": "",
                "model_revision": "",
                "category": cat,
                "status": "completed",
                "error": "",
                "case_count": agg["case_count"],
                "hit_case_count": agg["hit_case_count"],
                "successful_repetitions": "",
                "ranking_stable": "",
                "recall_at_5": agg["recall_at_5"],
                "mrr_at_5": agg["mrr_at_5"],
                "ndcg_at_5": agg["ndcg_at_5"],
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
                "eligible": "",
                "clear_gain": "",
                "production_safety": "",
                "cold_load_ms": "",
                "rerank_p50_ms": "",
                "rerank_p95_ms": "",
                "rss_before_load_mb": "",
                "rss_after_load_mb": "",
                "observed_peak_rss_mb": "",
                "device": "",
                "dtype": "",
            })
            minilm_summary_rows.append({
                "experiment_version": EXPERIMENT_VERSION,
                "input_order": setting.order,
                "input_key": setting.key,
                "input_label": setting.label,
                "state_order": 2,
                "state_key": "minilm",
                "model_id": MODEL_ID,
                "model_revision": "not_reported",
                "category": cat,
                "status": "failed",
                "error": error,
                "case_count": agg["case_count"],
                "hit_case_count": "",
                "successful_repetitions": 0 if cat == "overall" else "",
                "ranking_stable": "",
                "recall_at_5": "",
                "mrr_at_5": "",
                "ndcg_at_5": "",
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
                "eligible": "",
                "clear_gain": "",
                "production_safety": "",
                "cold_load_ms": "",
                "rerank_p50_ms": "",
                "rerank_p95_ms": "",
                "rss_before_load_mb": "",
                "rss_after_load_mb": "",
                "observed_peak_rss_mb": "",
                "device": "",
                "dtype": "",
            })

        case_records = []
        for i, fc in enumerate(fixed_cases):
            bm = before_metrics[i]
            rank_before = _relevant_ranks(fc.relevant_source_sections, fc.pre_rerank_documents[:5])
            case_records.append({
                "experiment_version": EXPERIMENT_VERSION,
                "input_order": setting.order,
                "input_key": setting.key,
                "case_id": fc.case.case_id,
                "category": fc.case.category,
                "status": "failed",
                "error": error,
                "relevant_source_sections": [
                    {"source": s, "section": sec} for s, sec in fc.relevant_source_sections
                ],
                "pre_rerank_top_10": [
                    {"chunk_id": doc.id, "rank": r, "score": doc.score, "source": doc.metadata.get("source"), "section": doc.metadata.get("section")}
                    for r, doc in enumerate(fc.pre_rerank_documents, start=1)
                ],
                "no_rerank_top_5": [
                    {"chunk_id": doc.id, "rank": r, "score": doc.score, "source": doc.metadata.get("source"), "section": doc.metadata.get("section")}
                    for r, doc in enumerate(fc.pre_rerank_documents[:5], start=1)
                ],
                "minilm_top_5": [],
                "successful_repetitions": 0,
                "ranking_stable": "",
                "hit_before": bm.hit,
                "hit_after": "",
                "hit_change": "",
                "relevant_rank_before": rank_before,
                "relevant_rank_after": {},
                "recall_at_5_before": bm.recall_at_5,
                "recall_at_5_after": "",
                "mrr_at_5_before": bm.mrr_at_5,
                "mrr_at_5_after": "",
                "ndcg_at_5_before": bm.ndcg_at_5,
                "ndcg_at_5_after": "",
                "latency_by_repetition_ms": [],
            })

        summary_rows = no_rerank_summary_rows + minilm_summary_rows
        upsert_input_artifacts(
            setting.key,
            summary_rows,
            case_records,
            results_path=results_path,
            cases_path=cases_path,
        )


def run_all_reranker_inputs(
    inputs: RerankerBenchmarkInputs,
    *,
    results_path: Path = RESULTS_PATH,
    cases_path: Path = CASES_PATH,
) -> ReconciliationResult:
    process = psutil.Process()
    rss_checkpoints = [_rss_mb(process)]

    reranker = None
    try:
        reranker, runtime_evidence = load_runtime_reranker()
        rss_checkpoints.append(runtime_evidence.rss_after_load_mb)

        # 1 exact one-pair production warm-up (excluded from cold-load timing)
        reranker.warm_up()
        rss_checkpoints.append(_rss_mb(process))

        smoke_res = run_technical_smoke(inputs, reranker)
        if smoke_res.get("status") != "passed":
            raise RuntimeError("technical smoke failed")
        rss_checkpoints.append(_rss_mb(process))

        for setting in INPUT_SETTINGS:
            run_reranker_input(
                inputs,
                setting,
                reranker,
                runtime_evidence,
                results_path=results_path,
                cases_path=cases_path,
            )
            rss_checkpoints.append(_rss_mb(process))

        # Update final observed peak RSS on input 1 summary row
        peak_rss = max(rss_checkpoints + [runtime_evidence.observed_peak_rss_mb])
        if results_path.exists():
            with results_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            updated = False
            for row in rows:
                if (
                    row.get("input_order") == "1"
                    and row.get("state_key") == "minilm"
                    and row.get("category") == "overall"
                ):
                    row["observed_peak_rss_mb"] = peak_rss
                    updated = True
            if updated:
                _atomic_csv(rows, results_path)

    except Exception as exc:
        sanitized = sanitize_error_message(exc)
        _write_truthful_failure_for_all_inputs(
            inputs,
            sanitized,
            results_path=results_path,
            cases_path=cases_path,
        )
    finally:
        if reranker is not None:
            if hasattr(reranker, "_model"):
                reranker._model = None
        del reranker
        gc.collect()

    return reconcile_reranker_artifacts(inputs=inputs, results_path=results_path, cases_path=cases_path)


def _parse_finite_float(val: object, field_name: str) -> tuple[float | None, str | None]:
    """Parses a required numeric field into a finite float. Rejects missing/empty, non-numeric, and NaN/Inf."""
    if val is None or val == "":
        return None, f"{field_name} missing required numeric value"
    try:
        f_val = float(val)
        if not np.isfinite(f_val):
            return None, f"{field_name} non-finite float: {val}"
        return f_val, None
    except (TypeError, ValueError):
        return None, f"{field_name} invalid numeric: {val}"


def _check_finite_close(val: object, expected: float, field_name: str, tol: float = 1e-4) -> tuple[float | None, str | None]:
    """Parses value and verifies it is finite and matches expected within tolerance."""
    parsed, err = _parse_finite_float(val, field_name)
    if err:
        return None, err
    assert parsed is not None
    if abs(parsed - expected) > tol:
        return parsed, f"{field_name} mismatch: expected {expected}, got {parsed}"
    return parsed, None


def _check_positive_finite(val: object, field_name: str) -> tuple[float | None, str | None]:
    """Parses value and verifies it is positive (> 0) and finite."""
    parsed, err = _parse_finite_float(val, field_name)
    if err:
        return None, err
    assert parsed is not None
    if parsed <= 0.0:
        return parsed, f"{field_name} must be positive finite, got {parsed}"
    return parsed, None


def _check_finite_int(val: object, expected: int, field_name: str) -> tuple[int | None, str | None]:
    """Parses integer/float and verifies exact integer match."""
    parsed, err = _parse_finite_float(val, field_name)
    if err:
        return None, err
    assert parsed is not None
    try:
        int_val = int(parsed)
        if int_val != expected or abs(parsed - expected) > 1e-6:
            return None, f"{field_name} mismatch: expected {expected}, got {val}"
        return int_val, None
    except Exception:
        return None, f"{field_name} invalid int: {val}"


def reconcile_reranker_artifacts(
    inputs: RerankerBenchmarkInputs | None = None,
    *,
    results_path: Path = RESULTS_PATH,
    cases_path: Path = CASES_PATH,
) -> ReconciliationResult:
    errors: list[str] = []
    if not results_path.exists():
        return ReconciliationResult(complete=False, summary_rows=0, case_records=0, errors=("results file missing",))
    if not cases_path.exists():
        return ReconciliationResult(complete=False, summary_rows=0, case_records=0, errors=("cases file missing",))

    try:
        if inputs is None:
            inputs = load_reranker_benchmark_inputs()
    except Exception as exc:
        return ReconciliationResult(
            complete=False,
            summary_rows=0,
            case_records=0,
            errors=(f"failed loading canonical inputs for reconciliation: {exc}",),
        )

    canonical_fixed_by_setting: dict[str, list[FixedRerankerCase]] = {}
    for fc in inputs.fixed_cases:
        canonical_fixed_by_setting.setdefault(fc.input_key, []).append(fc)
    for k in canonical_fixed_by_setting:
        canonical_fixed_by_setting[k].sort(key=lambda fc: fc.case.case_id)

    # 1. Read files and validate raw structure
    summary_rows: list[dict] = []
    with results_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != RESULT_COLUMNS:
            errors.append("results CSV header mismatch")
        summary_rows = list(reader)

    case_records: list[dict] = []
    try:
        case_records = _read_jsonl(cases_path)
    except Exception as exc:
        errors.append(f"failed reading cases JSONL: {exc}")

    expected_summary_count = len(INPUT_SETTINGS) * 2 * (1 + len(GOLDEN_CATEGORIES))
    expected_cases_count = len(INPUT_SETTINGS) * len(inputs.cases)

    if len(summary_rows) != expected_summary_count:
        errors.append(f"expected {expected_summary_count} summary rows, got {len(summary_rows)}")
    if len(case_records) != expected_cases_count:
        errors.append(f"expected {expected_cases_count} case records, got {len(case_records)}")

    # 2. Recompute and validate Case Records
    cases_by_setting: dict[str, list[dict]] = {}
    for idx, r in enumerate(case_records):
        if tuple(r.keys()) != CASE_RECORD_FIELDS:
            errors.append(f"case record {idx} keys mismatch")
        if r.get("experiment_version") != EXPERIMENT_VERSION:
            errors.append(f"case record {r.get('case_id')} wrong experiment_version: {r.get('experiment_version')}")
        k = str(r.get("input_key"))
        cases_by_setting.setdefault(k, []).append(r)

    recomputed_setting_evidence: dict[str, tuple[list[CaseMetrics], list[CaseMetrics], dict, dict, dict, dict[str, BootstrapInterval], dict[str, bool], bool, float, float]] = {}

    for setting in INPUT_SETTINGS:
        setting_cases = cases_by_setting.get(setting.key, [])
        canonical_fcs = canonical_fixed_by_setting.get(setting.key, [])
        if len(setting_cases) != 45 or len(canonical_fcs) != 45:
            errors.append(f"setting {setting.key} case count mismatch: actual {len(setting_cases)}, expected 45")
            continue

        setting_before_metrics: list[CaseMetrics] = []
        setting_after_metrics: list[CaseMetrics] = []
        setting_latencies: list[float] = []
        has_failed_case = False

        for i in range(45):
            r = setting_cases[i]
            fc = canonical_fcs[i]
            cid = str(r.get("case_id"))

            if cid != fc.case.case_id:
                errors.append(f"setting {setting.key} case index {i} ID mismatch: expected {fc.case.case_id}, got {cid}")
            if str(r.get("input_order")) != str(setting.order):
                errors.append(f"setting {setting.key} case {cid} input_order mismatch")
            if str(r.get("category")) != fc.case.category:
                errors.append(f"case {cid} category mismatch: expected {fc.case.category}, got {r.get('category')}")
            if r.get("status") != "completed":
                errors.append(f"uncompleted status in case {cid}: {r.get('status')}")
                has_failed_case = True
                continue

            # Check repetitions and stability in case record
            if str(r.get("successful_repetitions")) != "3":
                errors.append(f"case {cid} successful_repetitions mismatch: expected 3, got {r.get('successful_repetitions')}")
            if str(r.get("ranking_stable")).lower() != "true":
                errors.append(f"case {cid} ranking_stable mismatch: expected True, got {r.get('ranking_stable')}")

            # Validate pre_rerank_top_10 matches canonical fixed input
            actual_pre = r.get("pre_rerank_top_10", [])
            if len(actual_pre) != 10:
                errors.append(f"case {cid} pre_rerank_top_10 length != 10")
            else:
                for r_idx, (act_doc, exp_doc) in enumerate(zip(actual_pre, fc.pre_rerank_documents), start=1):
                    if act_doc.get("chunk_id") != exp_doc.id:
                        errors.append(f"case {cid} pre_rerank_top_10 chunk_id mismatch at rank {r_idx}: expected {exp_doc.id}, got {act_doc.get('chunk_id')}")
                    if act_doc.get("rank") != r_idx:
                        errors.append(f"case {cid} pre_rerank_top_10 rank mismatch at {r_idx}")

            # Validate no_rerank_top_5 matches first 5 of pre_rerank_top_10
            actual_no_rerank = r.get("no_rerank_top_5", [])
            if len(actual_no_rerank) != 5:
                errors.append(f"case {cid} no_rerank_top_5 length != 5")
            elif actual_pre and [d.get("chunk_id") for d in actual_no_rerank] != [d.get("chunk_id") for d in actual_pre[:5]]:
                errors.append(f"case {cid} no_rerank_top_5 does not match first 5 of pre_rerank_top_10")

            # Validate minilm_top_5: ranks 1-5, unique chunks, subset of fixed pre_rerank_top_10
            actual_minilm = r.get("minilm_top_5", [])
            pre_chunk_ids = {doc.id for doc in fc.pre_rerank_documents}
            if len(actual_minilm) != 5:
                errors.append(f"case {cid} minilm_top_5 length != 5")
            else:
                seen_minilm_chunks = set()
                for m_idx, m_doc in enumerate(actual_minilm, start=1):
                    mid = m_doc.get("chunk_id")
                    if not mid or mid not in pre_chunk_ids:
                        errors.append(f"case {cid} minilm_top_5 chunk_id not in fixed pre_rerank_top_10: {mid}")
                    if mid in seen_minilm_chunks:
                        errors.append(f"case {cid} minilm_top_5 duplicate chunk_id: {mid}")
                    seen_minilm_chunks.add(mid)
                    if m_doc.get("rank") != m_idx:
                        errors.append(f"case {cid} minilm_top_5 rank mismatch at {m_idx}")

            # Reconstruct docs and score pair
            no_docs = [
                RetrievedDocument(id=d["chunk_id"], text="", score=float(d.get("score") or 0), metadata={"source": d.get("source"), "section": d.get("section")})
                for d in actual_no_rerank
            ]
            mini_docs = [
                RetrievedDocument(id=d["chunk_id"], text="", score=float(d.get("score") or 0), metadata={"source": d.get("source"), "section": d.get("section")})
                for d in actual_minilm
            ]
            exp_pair = score_fixed_pair(fc.case, no_docs, mini_docs)

            # Check hit, hit_change, relevant_rank
            if r.get("hit_before") != exp_pair.before.hit:
                errors.append(f"case {cid} hit_before contradiction: expected {exp_pair.before.hit}, got {r.get('hit_before')}")
            if r.get("hit_after") != exp_pair.after.hit:
                errors.append(f"case {cid} hit_after contradiction: expected {exp_pair.after.hit}, got {r.get('hit_after')}")
            if r.get("hit_change") != exp_pair.hit_change:
                errors.append(f"case {cid} hit_change mismatch: expected {exp_pair.hit_change}, got {r.get('hit_change')}")
            if r.get("relevant_rank_before") != exp_pair.relevant_rank_before:
                errors.append(f"case {cid} relevant_rank_before mismatch: expected {exp_pair.relevant_rank_before}, got {r.get('relevant_rank_before')}")
            if r.get("relevant_rank_after") != exp_pair.relevant_rank_after:
                errors.append(f"case {cid} relevant_rank_after mismatch: expected {exp_pair.relevant_rank_after}, got {r.get('relevant_rank_after')}")

            # Check per-case metrics via finite normalization boundary
            for m_name, exp_val in [
                ("recall_at_5_before", exp_pair.before.recall_at_5),
                ("recall_at_5_after", exp_pair.after.recall_at_5),
                ("mrr_at_5_before", exp_pair.before.mrr_at_5),
                ("mrr_at_5_after", exp_pair.after.mrr_at_5),
                ("ndcg_at_5_before", exp_pair.before.ndcg_at_5),
                ("ndcg_at_5_after", exp_pair.after.ndcg_at_5),
            ]:
                _, err = _check_finite_close(r.get(m_name), exp_val, f"case {cid} {m_name}")
                if err:
                    errors.append(err)

            # Validate exactly 3 positive finite latency numbers
            lats = r.get("latency_by_repetition_ms", [])
            if not isinstance(lats, list) or len(lats) != 3:
                errors.append(f"case {cid} latency_by_repetition_ms length != 3")
            else:
                for lat_idx, lat_val in enumerate(lats, start=1):
                    f_lat, err = _check_positive_finite(lat_val, f"case {cid} latency rep {lat_idx}")
                    if err:
                        errors.append(err)
                    elif f_lat is not None:
                        setting_latencies.append(f_lat)

            setting_before_metrics.append(exp_pair.before)
            setting_after_metrics.append(exp_pair.after)

        if not has_failed_case and len(setting_before_metrics) == 45:
            agg_b = aggregate_case_metrics(setting_before_metrics)
            agg_a = aggregate_case_metrics(setting_after_metrics)
            deltas: dict[str, dict[str, float]] = {}
            all_cats = ("overall",) + SORTED_GOLDEN_CATEGORIES
            for cat in all_cats:
                deltas[cat] = {
                    "delta_recall_at_5": agg_a[cat]["recall_at_5"] - agg_b[cat]["recall_at_5"],
                    "delta_mrr_at_5": agg_a[cat]["mrr_at_5"] - agg_b[cat]["mrr_at_5"],
                    "delta_ndcg_at_5": agg_a[cat]["ndcg_at_5"] - agg_b[cat]["ndcg_at_5"],
                }
            boot = paired_bootstrap_intervals(setting_before_metrics, setting_after_metrics, seed=42, samples=10000)
            guardrails = evaluate_category_guardrails(setting_before_metrics, setting_after_metrics)
            all_g = all(guardrails.values())
            p50 = float(np.percentile(setting_latencies, 50)) if len(setting_latencies) == 135 else 0.0
            p95 = float(np.percentile(setting_latencies, 95)) if len(setting_latencies) == 135 else 0.0
            recomputed_setting_evidence[setting.key] = (
                setting_before_metrics, setting_after_metrics, agg_b, agg_a, deltas, boot, guardrails, all_g, p50, p95
            )

    # 3. Validate Summary Rows against Recomputed Evidence
    summary_by_setting_state: dict[tuple[str, str], dict[str, dict]] = {}
    for row_idx, row in enumerate(summary_rows):
        if row.get("experiment_version") != EXPERIMENT_VERSION:
            errors.append(f"summary row {row_idx} wrong experiment_version: {row.get('experiment_version')}")
        k = (str(row.get("input_key")), str(row.get("state_key")))
        cat = str(row.get("category"))
        if cat in summary_by_setting_state.setdefault(k, {}):
            errors.append(f"duplicate summary row for {k} {cat}")
        summary_by_setting_state[k][cat] = row

    expected_categories = ("overall",) + SORTED_GOLDEN_CATEGORIES

    for setting in INPUT_SETTINGS:
        ev_tuple = recomputed_setting_evidence.get(setting.key)
        if not ev_tuple:
            continue
        (
            setting_before_metrics,
            setting_after_metrics,
            agg_before,
            agg_after,
            deltas,
            bootstrap,
            guardrail_passes,
            all_guardrails,
            exp_p50_lat,
            exp_p95_lat,
        ) = ev_tuple

        # Check state 1 (no-rerank)
        no_rerank_rows = summary_by_setting_state.get((setting.key, "no-rerank"), {})
        for cat in expected_categories:
            row = no_rerank_rows.get(cat)
            if not row:
                errors.append(f"missing summary row for {setting.key} no-rerank {cat}")
                continue
            if str(row.get("input_order")) != str(setting.order):
                errors.append(f"{setting.key} no-rerank {cat} input_order mismatch: expected {setting.order}, got {row.get('input_order')}")
            if str(row.get("state_order")) != "1":
                errors.append(f"{setting.key} no-rerank {cat} state_order mismatch: expected 1, got {row.get('state_order')}")
            if row.get("status") != "completed":
                errors.append(f"uncompleted status in {setting.key} no-rerank {cat}: {row.get('status')}")
            exp_agg = agg_before[cat]

            _, err = _check_finite_int(row.get("case_count"), exp_agg["case_count"], f"{setting.key} no-rerank {cat} case_count")
            if err:
                errors.append(err)
            _, err = _check_finite_int(row.get("hit_case_count"), exp_agg["hit_case_count"], f"{setting.key} no-rerank {cat} hit_case_count")
            if err:
                errors.append(err)

            for m in ("recall_at_5", "mrr_at_5", "ndcg_at_5"):
                _, err = _check_finite_close(row.get(m), exp_agg[m], f"{setting.key} no-rerank {cat} {m}")
                if err:
                    errors.append(err)

            for blank_f in (
                "delta_recall_at_5", "delta_mrr_at_5", "delta_ndcg_at_5",
                "recall_ci_lower", "recall_ci_upper", "mrr_ci_lower", "mrr_ci_upper", "ndcg_ci_lower", "ndcg_ci_upper",
                "category_guardrail_pass", "all_category_guardrails_pass", "eligible", "clear_gain", "production_safety",
                "cold_load_ms", "rerank_p50_ms", "rerank_p95_ms",
                "rss_before_load_mb", "rss_after_load_mb", "observed_peak_rss_mb",
                "successful_repetitions", "ranking_stable", "device", "dtype",
            ):
                if str(row.get(blank_f) or "") != "":
                    errors.append(f"{setting.key} no-rerank {cat} expected blank {blank_f}, got {row.get(blank_f)}")

        # Check state 2 (minilm)
        minilm_rows = summary_by_setting_state.get((setting.key, "minilm"), {})
        for cat in expected_categories:
            row = minilm_rows.get(cat)
            if not row:
                errors.append(f"missing summary row for {setting.key} minilm {cat}")
                continue
            if str(row.get("input_order")) != str(setting.order):
                errors.append(f"{setting.key} minilm {cat} input_order mismatch: expected {setting.order}, got {row.get('input_order')}")
            if str(row.get("state_order")) != "2":
                errors.append(f"{setting.key} minilm {cat} state_order mismatch: expected 2, got {row.get('state_order')}")
            if row.get("status") != "completed":
                errors.append(f"uncompleted status in {setting.key} minilm {cat}: {row.get('status')}")
            exp_agg = agg_after[cat]

            _, err = _check_finite_int(row.get("case_count"), exp_agg["case_count"], f"{setting.key} minilm {cat} case_count")
            if err:
                errors.append(err)
            _, err = _check_finite_int(row.get("hit_case_count"), exp_agg["hit_case_count"], f"{setting.key} minilm {cat} hit_case_count")
            if err:
                errors.append(err)

            for m in ("recall_at_5", "mrr_at_5", "ndcg_at_5"):
                _, err = _check_finite_close(row.get(m), exp_agg[m], f"{setting.key} minilm {cat} {m}")
                if err:
                    errors.append(err)

            exp_d = deltas[cat]
            for delta_name in ("delta_recall_at_5", "delta_mrr_at_5", "delta_ndcg_at_5"):
                _, err = _check_finite_close(row.get(delta_name), exp_d[delta_name], f"{setting.key} minilm {cat} {delta_name}")
                if err:
                    errors.append(err)

            if cat != "overall":
                exp_guardrail = guardrail_passes[cat]
                act_guardrail = str(row.get("category_guardrail_pass")).lower() == "true"
                if act_guardrail != exp_guardrail:
                    errors.append(f"{setting.key} minilm {cat} category_guardrail_pass mismatch: expected {exp_guardrail}, got {act_guardrail}")
                for blank_f in (
                    "recall_ci_lower", "recall_ci_upper", "mrr_ci_lower", "mrr_ci_upper", "ndcg_ci_lower", "ndcg_ci_upper",
                    "all_category_guardrails_pass", "eligible", "clear_gain", "production_safety",
                    "cold_load_ms", "rerank_p50_ms", "rerank_p95_ms",
                    "rss_before_load_mb", "rss_after_load_mb", "observed_peak_rss_mb",
                    "successful_repetitions", "ranking_stable",
                ):
                    if str(row.get(blank_f) or "") != "":
                        errors.append(f"{setting.key} minilm {cat} expected blank {blank_f}, got {row.get(blank_f)}")
            else:
                # Overall row checks
                if str(row.get("successful_repetitions")) != "3":
                    errors.append(f"{setting.key} minilm overall successful_repetitions mismatch: expected 3, got {row.get('successful_repetitions')}")
                if str(row.get("ranking_stable")).lower() != "true":
                    errors.append(f"{setting.key} minilm overall ranking_stable mismatch: expected True, got {row.get('ranking_stable')}")

                # Check p50 and p95 latencies against recomputed per-case latencies
                _, err = _check_finite_close(row.get("rerank_p50_ms"), exp_p50_lat, f"{setting.key} minilm overall rerank_p50_ms")
                if err:
                    errors.append(err)
                parsed_p95, err = _check_finite_close(row.get("rerank_p95_ms"), exp_p95_lat, f"{setting.key} minilm overall rerank_p95_ms")
                if err:
                    errors.append(err)

                # Check all six bootstrap CI fields against recomputed bootstrap
                for ci_field, metric_name, bound_name in [
                    ("recall_ci_lower", "recall", "lower"),
                    ("recall_ci_upper", "recall", "upper"),
                    ("mrr_ci_lower", "mrr", "lower"),
                    ("mrr_ci_upper", "mrr", "upper"),
                    ("ndcg_ci_lower", "ndcg", "lower"),
                    ("ndcg_ci_upper", "ndcg", "upper"),
                ]:
                    exp_val = getattr(bootstrap[metric_name], bound_name)
                    _, err = _check_finite_close(row.get(ci_field), exp_val, f"{setting.key} minilm overall {ci_field}")
                    if err:
                        errors.append(err)

                act_all_guardrails = str(row.get("all_category_guardrails_pass")).lower() == "true"
                if act_all_guardrails != all_guardrails:
                    errors.append(f"{setting.key} minilm overall all_category_guardrails_pass mismatch: expected {all_guardrails}, got {act_all_guardrails}")

                p95_val = parsed_p95 if parsed_p95 is not None else float("inf")
                exp_eligible = (
                    str(row.get("successful_repetitions")) == "3"
                    and str(row.get("ranking_stable")).lower() == "true"
                    and all_guardrails
                    and (p95_val <= 3000.0)
                )
                act_eligible = str(row.get("eligible")).lower() == "true"
                if act_eligible != exp_eligible:
                    errors.append(f"{setting.key} minilm overall eligible mismatch: expected {exp_eligible}, got {act_eligible}")

                exp_clear_gain = exp_eligible and (deltas["overall"]["delta_ndcg_at_5"] >= 0.03) and (bootstrap["ndcg"].lower > 0.0)
                act_clear_gain = str(row.get("clear_gain")).lower() == "true"
                if act_clear_gain != exp_clear_gain:
                    errors.append(f"{setting.key} minilm overall clear_gain mismatch: expected {exp_clear_gain}, got {act_clear_gain}")

                # Check production safety on setting 3
                if setting.order == 3:
                    e5_tuple = recomputed_setting_evidence.get("dense__e5-small-384")
                    if e5_tuple:
                        e5_before_metrics = e5_tuple[0]
                        exp_prod_safety = evaluate_production_safety(setting_after_metrics, e5_before_metrics)
                        act_prod_safety = str(row.get("production_safety")).lower() == "true"
                        if act_prod_safety != exp_prod_safety:
                            errors.append(f"{setting.key} minilm overall production_safety mismatch: expected {exp_prod_safety}, got {act_prod_safety}")
                else:
                    if str(row.get("production_safety") or "") != "":
                        errors.append(f"{setting.key} minilm overall expected blank production_safety, got {row.get('production_safety')}")

                # Resource checks on setting 1 vs blank on settings 2 & 3
                if setting.order == 1:
                    parsed_cold, err = _check_positive_finite(row.get("cold_load_ms"), "setting 1 minilm overall cold_load_ms")
                    if err:
                        errors.append(err)
                    parsed_before, err = _check_positive_finite(row.get("rss_before_load_mb"), "setting 1 minilm overall rss_before_load_mb")
                    if err:
                        errors.append(err)
                    parsed_after, err = _check_positive_finite(row.get("rss_after_load_mb"), "setting 1 minilm overall rss_after_load_mb")
                    if err:
                        errors.append(err)
                    parsed_peak, err = _check_positive_finite(row.get("observed_peak_rss_mb"), "setting 1 minilm overall observed_peak_rss_mb")
                    if err:
                        errors.append(err)

                    if parsed_before is not None and parsed_after is not None and parsed_peak is not None:
                        if parsed_peak < parsed_before or parsed_peak < parsed_after:
                            errors.append(f"setting 1 minilm overall observed_peak_rss_mb ({parsed_peak}) cannot be less than before ({parsed_before}) or after ({parsed_after})")
                else:
                    for res_field in ("cold_load_ms", "rss_before_load_mb", "rss_after_load_mb", "observed_peak_rss_mb"):
                        if str(row.get(res_field) or "") != "":
                            errors.append(f"{setting.key} minilm overall expected blank {res_field}, got {row.get(res_field)}")

    is_complete = (len(summary_rows) == expected_summary_count and len(case_records) == expected_cases_count and len(errors) == 0)
    return ReconciliationResult(
        complete=is_complete,
        summary_rows=len(summary_rows),
        case_records=len(case_records),
        errors=tuple(errors),
    )
