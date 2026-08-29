"""Orchestration, scoring, guardrails, bootstrap, CSV persistence and display helpers for Phase 8 08a."""
from dataclasses import dataclass
import copy
import csv
import gc
import math
import os
from pathlib import Path
import re
import time
from typing import Literal

import numpy as np
import polars as pl
import psutil
import torch

from core.schema import RetrievedDocument, RetrievalDependencyError
from core.settings_loader import load_settings

REPO_ROOT = Path(__file__).resolve().parents[2]
from vectorstore.qdrant import (
    client_from_settings,
    ensure_collection,
    validate_collection_info,
    DENSE_VECTOR_NAME,
)
from vectorstore.points import validate_chunks, build_points
from vectorstore.upsert import upsert_points, validate_existing_points, verify_point_count
from ingestion.chunking.markdown_chunker import chunk_foods_markdown
from retrieval.dense_retriever import DenseRetriever
from evaluation.golden_dataset import (
    GoldenCase,
    load_golden,
    validate_v3_full,
    document_is_relevant,
    V3_FULL_PATH,
)
from embedding.dense_benchmark import (
    DenseBenchmarkSetting,
    DocumentEmbeddingResult,
    E5_SMALL_SETTING,
    MINILM_L12_SETTING,
    HUYDANG_DEK21_SETTING,
    E5_BASE_SETTING,
    QWEN3_384_SETTING,
    E5_LARGE_SETTING,
    BGE_M3_SETTING,
    QWEN3_1024_SETTING,
    ALL_DENSE_SETTINGS,
    AUTHORIZED_DENSE_SETTINGS,
    AUTHORIZED_DENSE_CANDIDATE_SETTINGS,
    DEFERRED_DENSE_SETTINGS,
    build_dense_runner,
)

CANONICAL_CHUNK_COUNT = 572
EMBEDDING_RESULTS_PATH = REPO_ROOT / "evaluation" / "results" / "phase8_embedding_results.csv"

CANONICAL_SETTINGS_MAP = {s.setting_key: s for s in ALL_DENSE_SETTINGS}
AUTHORIZED_SETTING_KEYS = {s.setting_key for s in AUTHORIZED_DENSE_SETTINGS}
DEFERRED_SETTING_KEYS = {s.setting_key for s in DEFERRED_DENSE_SETTINGS}
APPROVED_COLLECTIONS = {s.collection_name for s in ALL_DENSE_SETTINGS}

CSV_COLUMNS = (
    "setting_key",
    "setting_label",
    "category",
    "model_id",
    "model_revision",
    "dimension",
    "max_length",
    "collection_name",
    "retrieval_mode",
    "use_bm25",
    "use_reranker",
    "status",
    "error",
    "case_count",
    "hit_case_count",
    "recall_at_5",
    "mrr_at_5",
    "ndcg_at_5",
    "successful_repetitions",
    "ranking_stable",
    "truncated_document_count",
    "cold_load_ms",
    "document_embedding_ms",
    "query_embedding_p50_ms",
    "query_embedding_p95_ms",
    "retrieval_p50_ms",
    "retrieval_p95_ms",
    "warm_total_p50_ms",
    "warm_total_p95_ms",
    "rss_before_load_mb",
    "rss_after_load_mb",
    "observed_peak_rss_mb",
    "device",
    "dtype",
    "document_batch_size",
    "query_batch_size",
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
    "clear_gain_vs_control",
    "best_lighter_setting",
    "clear_gain_vs_best_lighter",
    "finalist_eligible",
)


@dataclass(frozen=True)
class CaseMetrics:
    case_id: str
    category: str
    recall_at_5: float
    mrr_at_5: float
    ndcg_at_5: float
    hit: bool
    relevant_keys: tuple[tuple[str, str], ...]
    ranked_keys: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class BootstrapInterval:
    delta: float
    lower: float
    upper: float


@dataclass
class EmbeddingBenchmarkInputs:
    cases: list[GoldenCase]
    chunks: list[dict[str, object]]
    client: object
    settings: dict[str, object]


@dataclass
class EmbeddingBenchmarkResult:
    setting: DenseBenchmarkSetting
    status: str
    error: str
    summary: dict[str, object]
    category_rows: list[dict[str, object]]
    case_metrics: list[CaseMetrics]
    rankings_by_repetition: list[dict[str, tuple[str, ...]]]


# --- 1. Scoring & Aggregation ---


def score_retrieval_case(
    case: GoldenCase,
    documents: list[RetrievedDocument],
    *,
    k: int = 5,
) -> CaseMetrics:
    """Tính toán Recall@k, MRR@k, nDCG@k và hit cho 1 câu hỏi đánh giá theo chuẩn evidence binary."""
    declared_relevant_pairs = [
        (source, sec)
        for source, sections in case.evidence.items()
        for sec in sections
    ]
    relevant_count = len(declared_relevant_pairs)
    if relevant_count == 0:
        raise ValueError(f"case {case.case_id} has empty evidence")

    top_k_docs = documents[:k]
    seen_credited_pairs: set[tuple[str, str]] = set()
    gains: list[float] = []

    for doc in top_k_docs:
        doc_source = str(doc.metadata.get("source", ""))
        doc_section = str(doc.metadata.get("section", ""))
        pair = (doc_source, doc_section)

        if document_is_relevant(case, doc) and pair not in seen_credited_pairs:
            gains.append(1.0)
            seen_credited_pairs.add(pair)
        else:
            gains.append(0.0)

    credited_count = len(seen_credited_pairs)
    recall_at_5 = credited_count / relevant_count

    first_credited_rank = next((rank for rank, g in enumerate(gains, 1) if g > 0.0), None)
    mrr_at_5 = (1.0 / first_credited_rank) if first_credited_rank is not None else 0.0

    dcg = sum(g / math.log2(rank + 1) for rank, g in enumerate(gains, 1))
    idcg = sum(1.0 / math.log2(rank + 1) for rank in range(1, min(k, relevant_count) + 1))
    ndcg_at_5 = (dcg / idcg) if idcg > 0.0 else 0.0
    hit = credited_count > 0

    ranked_keys = tuple(
        (str(doc.metadata.get("source", "")), str(doc.metadata.get("section", "")))
        for doc in top_k_docs
    )

    return CaseMetrics(
        case_id=case.case_id,
        category=case.category,
        recall_at_5=recall_at_5,
        mrr_at_5=mrr_at_5,
        ndcg_at_5=ndcg_at_5,
        hit=hit,
        relevant_keys=tuple(declared_relevant_pairs),
        ranked_keys=ranked_keys,
    )


def aggregate_case_metrics(
    case_metrics: list[CaseMetrics],
) -> dict[str, dict[str, int | float]]:
    """Tổng hợp kết quả metrics theo overall và từng danh mục category đã quan sát."""
    if not case_metrics:
        raise ValueError("case_metrics list is empty")

    categories = sorted(list({m.category for m in case_metrics}))
    result: dict[str, dict[str, int | float]] = {}

    def _calc_stats(subset: list[CaseMetrics]) -> dict[str, int | float]:
        n = len(subset)
        return {
            "case_count": n,
            "hit_case_count": sum(1 for m in subset if m.hit),
            "recall_at_5": sum(m.recall_at_5 for m in subset) / n,
            "mrr_at_5": sum(m.mrr_at_5 for m in subset) / n,
            "ndcg_at_5": sum(m.ndcg_at_5 for m in subset) / n,
        }

    result["overall"] = _calc_stats(case_metrics)
    for cat in categories:
        subset = [m for m in case_metrics if m.category == cat]
        result[cat] = _calc_stats(subset)

    return result


# --- 2. Category Guardrails, Bootstrap & Finalist Selection ---


def evaluate_category_guardrails(
    reference: list[CaseMetrics],
    candidate: list[CaseMetrics],
) -> dict[str, bool]:
    """Đánh giá 9 category guardrails bảo vệ chất lượng theo quy tắc V3 Gate 1."""
    if len(reference) != len(candidate):
        raise ValueError("reference and candidate length mismatch")

    ref_pairs = [(r.case_id, r.category) for r in reference]
    cand_pairs = [(c.case_id, c.category) for c in candidate]
    if ref_pairs != cand_pairs:
        raise ValueError("reference and candidate (case_id, category) mismatch")

    categories = sorted(list({r.category for r in reference}))
    guardrails: dict[str, bool] = {}

    for cat in categories:
        ref_subset = [r for r in reference if r.category == cat]
        cand_subset = [c for c in candidate if c.category == cat]
        n = len(ref_subset)

        if n >= 6:
            ref_hits = sum(1 for r in ref_subset if r.hit)
            cand_hits = sum(1 for c in cand_subset if c.hit)
            if cand_hits < ref_hits:
                guardrails[cat] = False
            elif cand_hits == ref_hits:
                ref_ndcg = sum(r.ndcg_at_5 for r in ref_subset) / n
                cand_ndcg = sum(c.ndcg_at_5 for c in cand_subset) / n
                delta_ndcg = cand_ndcg - ref_ndcg
                guardrails[cat] = bool(delta_ndcg >= -0.02)
            else:
                guardrails[cat] = True
        else:
            # Quy tắc n <= 3: không được mất hit đối với bất kỳ case nào reference đã hit
            lost_hits = [
                c.case_id
                for r, c in zip(ref_subset, cand_subset)
                if r.hit and not c.hit
            ]
            guardrails[cat] = (len(lost_hits) == 0)

    return guardrails


def paired_bootstrap_intervals(
    reference: list[CaseMetrics],
    candidate: list[CaseMetrics],
    *,
    samples: int = 10_000,
    seed: int = 42,
) -> dict[str, BootstrapInterval]:
    """Tính 95% Percentile Confidence Interval bằng phương pháp Paired Bootstrap 10.000 lần."""
    if len(reference) != len(candidate):
        raise ValueError("reference and candidate length mismatch")
    if [(r.case_id, r.category) for r in reference] != [(c.case_id, c.category) for c in candidate]:
        raise ValueError("reference and candidate (case_id, category) mismatch")

    n = len(reference)
    ref_recall = np.array([r.recall_at_5 for r in reference], dtype=np.float64)
    cand_recall = np.array([c.recall_at_5 for c in candidate], dtype=np.float64)
    ref_mrr = np.array([r.mrr_at_5 for r in reference], dtype=np.float64)
    cand_mrr = np.array([c.mrr_at_5 for c in candidate], dtype=np.float64)
    ref_ndcg = np.array([r.ndcg_at_5 for r in reference], dtype=np.float64)
    cand_ndcg = np.array([c.ndcg_at_5 for c in candidate], dtype=np.float64)

    delta_recall = cand_recall - ref_recall
    delta_mrr = cand_mrr - ref_mrr
    delta_ndcg = cand_ndcg - ref_ndcg

    rng = np.random.default_rng(seed)
    indices = rng.integers(0, n, size=(samples, n))

    boot_recall = delta_recall[indices].mean(axis=1)
    boot_mrr = delta_mrr[indices].mean(axis=1)
    boot_ndcg = delta_ndcg[indices].mean(axis=1)

    return {
        "recall": BootstrapInterval(
            delta=float(delta_recall.mean()),
            lower=float(np.percentile(boot_recall, 2.5)),
            upper=float(np.percentile(boot_recall, 97.5)),
        ),
        "mrr": BootstrapInterval(
            delta=float(delta_mrr.mean()),
            lower=float(np.percentile(boot_mrr, 2.5)),
            upper=float(np.percentile(boot_mrr, 97.5)),
        ),
        "ndcg": BootstrapInterval(
            delta=float(delta_ndcg.mean()),
            lower=float(np.percentile(boot_ndcg, 2.5)),
            upper=float(np.percentile(boot_ndcg, 97.5)),
        ),
    }


def has_clear_gain(
    *,
    status: str,
    successful_repetitions: int,
    guardrails: dict[str, bool],
    ndcg_interval: BootstrapInterval,
) -> bool:
    """Xác định xem candidate có clear gain vượt reference hay không theo quy tắc Gate 1."""
    return bool(
        status == "completed"
        and successful_repetitions == 3
        and all(guardrails.values())
        and ndcg_interval.delta >= 0.03
        and ndcg_interval.lower > 0.0
    )


def select_best_lighter_finalist(
    current_order: int,
    finalist_rows: list[dict[str, object]],
) -> str:
    """Chọn cấu hình nhẹ hơn tốt nhất từ danh sách các finalist đã đạt trước đó."""
    if not finalist_rows:
        return "e5-small-384"

    eligible = [
        row for row in finalist_rows
        if int(row.get("order", 999)) < current_order
    ]
    if not eligible:
        return "e5-small-384"

    # Sắp xếp theo ndcg_at_5 giảm dần, mrr_at_5 giảm dần, recall_at_5 giảm dần, order tăng dần
    def _sort_key(r: dict[str, object]):
        return (
            -float(r.get("ndcg_at_5", 0.0)),
            -float(r.get("mrr_at_5", 0.0)),
            -float(r.get("recall_at_5", 0.0)),
            int(r.get("order", 999)),
        )

    sorted_eligible = sorted(eligible, key=_sort_key)
    return str(sorted_eligible[0].get("setting_key", "e5-small-384"))


def sanitize_benchmark_error(exc: Exception) -> str:
    """Làm sạch thông báo lỗi, loại bỏ secret, signed query parameters, authorization headers, cookies."""
    root = exc
    while root.__cause__ is not None:
        root = root.__cause__

    raw_msg = str(root)
    # Loại bỏ query string sau dấu ? trong URL
    msg = re.sub(r"(https?://[^\s\?]+)\?[^\s]+", r"\1?[REDACTED]", raw_msg)
    # Loại bỏ query parameters riêng lẻ (? hoặc &)
    msg = re.sub(r"([?&])(X-Amz-[^=\s]+|token|api_key|password|secret|key|sig|signature)=[^&\s]+", r"\1\2=[REDACTED]", msg, flags=re.IGNORECASE)
    # Loại bỏ header Authorization (Bearer, Basic, v.v.)
    msg = re.sub(r"(?i)(authorization\s*:\s*)([^\s,;]+(?:\s+[^\s,;]+)?)", r"\1[REDACTED]", msg)
    msg = re.sub(r"(?i)\b(bearer|basic)\s+[a-zA-Z0-9_\-\.\+/=]+", r"\1 [REDACTED]", msg)
    # Loại bỏ Cookie / Set-Cookie
    msg = re.sub(r"(?i)(cookie|set-cookie)\s*:\s*[^\r\n]+", r"\1: [REDACTED]", msg)
    # Loại bỏ các cặp key=value nhạy cảm
    msg = re.sub(r"(?i)(password|secret|token|api_key|client_secret|aws_secret_access_key|x-amz-signature|x-amz-credential)\s*[:=]\s*[^\s,;]+", r"\1=[REDACTED]", msg)
    cleaned = " ".join(msg.split())
    return f"{type(root).__name__}: {cleaned[:500]}"


# --- 3. CSV Persistence ---


def upsert_embedding_results_csv(
    rows: list[dict[str, object]],
    *,
    path: Path = EMBEDDING_RESULTS_PATH,
) -> Path:
    """Ghi hoặc cập nhật kết quả benchmark vào file CSV long format bền vững."""
    path.parent.mkdir(parents=True, exist_ok=True)
    existing_rows: dict[tuple[str, str], dict[str, object]] = {}

    if path.is_file():
        with path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != list(CSV_COLUMNS):
                raise ValueError(
                    f"existing CSV header {reader.fieldnames} != expected {list(CSV_COLUMNS)}"
                )
            for r in reader:
                key = (r.get("setting_key", ""), r.get("category", ""))
                existing_rows[key] = r

    for row in rows:
        key = (str(row.get("setting_key", "")), str(row.get("category", "")))
        existing_rows[key] = row

    # Thứ tự các settings theo approved order
    order_map = {s.setting_key: s.order for s in ALL_DENSE_SETTINGS}

    def _sort_key(item: tuple[tuple[str, str], dict[str, object]]):
        (s_key, cat), _ = item
        s_order = order_map.get(s_key, 999)
        cat_order = 0 if cat == "overall" else 1
        return (s_order, cat_order, cat)

    sorted_items = sorted(existing_rows.items(), key=_sort_key)

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(CSV_COLUMNS))
        writer.writeheader()
        for _, row in sorted_items:
            sanitized_row = {col: row.get(col, "") for col in CSV_COLUMNS}
            writer.writerow(sanitized_row)

    return path


# --- 4. Inputs & Safety Snapshots ---


def load_embedding_benchmark_inputs() -> EmbeddingBenchmarkInputs:
    """Nạp canonical Golden V3 và 572 chunks, validate toàn vẹn trước khi chạy benchmark."""
    cases = load_golden(V3_FULL_PATH)
    validate_v3_full(cases)
    chunks = chunk_foods_markdown()
    chunk_ids = validate_chunks(chunks)

    if len(cases) != 45:
        raise ValueError(f"Golden V3 case count {len(cases)} != 45")
    if len(chunk_ids) != CANONICAL_CHUNK_COUNT:
        raise ValueError(f"chunk count {len(chunk_ids)} != {CANONICAL_CHUNK_COUNT}")

    settings = load_settings()
    client = client_from_settings(settings)

    return EmbeddingBenchmarkInputs(
        cases=cases,
        chunks=chunks,
        client=client,
        settings=settings,
    )


def snapshot_active_collection(inputs: EmbeddingBenchmarkInputs) -> dict[str, object]:
    """Ghi lại snapshot read-only về schema và point count của active production collection."""
    client = inputs.client
    name = str(inputs.settings["vector_database"]["collection_name"])
    info = client.get_collection(name)
    vectors_conf = info.config.params.vectors
    dense_params = vectors_conf.get(DENSE_VECTOR_NAME) if isinstance(vectors_conf, dict) else None
    sparse_conf = info.config.params.sparse_vectors or {}

    return {
        "collection_name": name,
        "points_count": info.points_count,
        "dense_vector_name": DENSE_VECTOR_NAME,
        "dense_size": dense_params.size if dense_params else None,
        "dense_distance": str(dense_params.distance) if dense_params else None,
        "sparse_vector_names": sorted(list(sparse_conf.keys())),
    }


class TimedQueryRunnerWrapper:
    """Wrapper đo thời gian embed_query mà không sửa đổi DenseRetriever hay runner."""

    def __init__(self, runner) -> None:
        self._runner = runner
        self.last_query_embed_ns: int = 0
        self.model_id = runner.model_id
        self.dimension = runner.dimension

    def embed_query(self, query: str) -> list[float]:
        t0 = time.perf_counter_ns()
        vec = self._runner.embed_query(query)
        self.last_query_embed_ns = time.perf_counter_ns() - t0
        return vec


# --- 5. One-Setting & Sequential Execution ---


def run_embedding_benchmark(
    setting: DenseBenchmarkSetting,
    benchmark_inputs: EmbeddingBenchmarkInputs,
    *,
    expected_active_snapshot: dict[str, object],
    control_result: EmbeddingBenchmarkResult | None = None,
    lighter_results: tuple[EmbeddingBenchmarkResult, ...] = (),
) -> EmbeddingBenchmarkResult:
    """Thực thi toàn bộ vòng đời của 1 cấu hình dense benchmark trên collection cô lập."""
    # Boundary check 1: expected_active_snapshot is strictly mandatory
    if expected_active_snapshot is None:
        raise ValueError("expected_active_snapshot is mandatory for benchmark execution")

    # Boundary check 2: setting must match canonical approved constant exactly
    if setting.setting_key not in CANONICAL_SETTINGS_MAP:
        raise ValueError(f"unapproved benchmark setting key: {setting.setting_key!r}")
    canonical = CANONICAL_SETTINGS_MAP[setting.setting_key]
    if setting != canonical:
        raise ValueError(f"forged or altered setting object for {setting.setting_key!r}")

    # Boundary check 3: deferred settings must be rejected at runtime boundary
    if setting.setting_key in DEFERRED_SETTING_KEYS:
        raise ValueError(f"setting {setting.setting_key!r} is deferred and not authorized in this run round")
    if setting.setting_key not in AUTHORIZED_SETTING_KEYS:
        raise ValueError(f"setting {setting.setting_key!r} is not authorized for execution")

    # Boundary check 4: collection must be in approved isolated list and not equal to active collection
    if setting.collection_name not in APPROVED_COLLECTIONS:
        raise ValueError(f"unapproved isolated collection target: {setting.collection_name!r}")

    active_name = str(benchmark_inputs.settings["vector_database"]["collection_name"])
    if setting.collection_name == active_name:
        raise ValueError(f"cannot use active production collection {active_name!r} as benchmark write target")

    # Boundary check 5: active collection snapshot unchanged before any mutation
    current_active_snap = snapshot_active_collection(benchmark_inputs)
    if current_active_snap != expected_active_snapshot:
        raise ValueError(f"active collection snapshot mismatch before running {setting.setting_key}")

    process = psutil.Process()
    client = benchmark_inputs.client
    cases = benchmark_inputs.cases
    chunks = benchmark_inputs.chunks

    # Isolated settings copy
    isolated_settings = copy.deepcopy(benchmark_inputs.settings)
    isolated_settings["embedding"]["model"] = setting.model_id
    isolated_settings["embedding"]["vector_size"] = setting.dimension
    isolated_settings["vector_database"]["collection_name"] = setting.collection_name
    isolated_settings["vector_database"]["vector_size"] = setting.dimension
    isolated_settings["profiles"]["dense_only"]["retrieval_mode"] = "dense"
    isolated_settings["profiles"]["dense_only"]["use_bm25"] = False
    isolated_settings["profiles"]["dense_only"]["use_reranker"] = False

    rss_checkpoints: list[float] = []
    rss_before_load_mb = process.memory_info().rss / (1024 * 1024)
    rss_checkpoints.append(rss_before_load_mb)

    runner = build_dense_runner(setting)
    status = "failed"
    error_msg = ""
    cold_load_ms = 0.0
    doc_embed_ms = 0.0
    truncated_count = 0
    q_embed_ms_list: list[float] = []
    retrieval_ms_list: list[float] = []
    warm_total_ms_list: list[float] = []
    rankings_by_rep: list[dict[str, tuple[str, ...]]] = []
    case_metrics_rep1: list[CaseMetrics] = []
    summary: dict[str, object] = {}
    category_rows: list[dict[str, object]] = []

    try:
        # 1. Cold load model
        t0_load = time.perf_counter_ns()
        runner.load()
        cold_load_ms = (time.perf_counter_ns() - t0_load) / 1_000_000.0
        rss_after_load_mb = process.memory_info().rss / (1024 * 1024)
        rss_checkpoints.append(rss_after_load_mb)

        # 2. Document embedding & indexing
        chunk_texts = [str(c["text"]) for c in chunks]
        t0_embed = time.perf_counter_ns()
        doc_result = runner.embed_documents(chunk_texts)
        doc_embed_ms = (time.perf_counter_ns() - t0_embed) / 1_000_000.0
        truncated_count = doc_result.truncated_document_count
        rss_checkpoints.append(process.memory_info().rss / (1024 * 1024))

        points = build_points(chunks, doc_result.vectors, setting.model_id, setting.dimension)
        ensure_collection(client, isolated_settings)
        validate_existing_points(client, isolated_settings, points, setting.model_id)
        upsert_points(client, isolated_settings, points)
        validate_collection_info(client.get_collection(setting.collection_name), isolated_settings, strict_dense_only=True)
        verify_point_count(client, isolated_settings, len(chunks))

        # 3. Discarded warm-up (exact case foods-v3-0001)
        timed_runner = TimedQueryRunnerWrapper(runner)
        retriever = DenseRetriever(
            client=client,
            embedder=timed_runner,
            collection_name=setting.collection_name,
            top_k=30,
        )
        warmup_case = cases[0]
        _ = retriever.search(warmup_case.question, limit=30)

        # 4. Three full repetitions
        successful_reps = 0
        for rep_idx in range(1, 4):
            rep_rankings: dict[str, tuple[str, ...]] = {}
            for case in cases:
                t0_query = time.perf_counter_ns()
                docs = retriever.search(case.question, limit=30)
                t_total_ns = time.perf_counter_ns() - t0_query

                q_ms = timed_runner.last_query_embed_ns / 1_000_000.0
                total_ms = t_total_ns / 1_000_000.0
                ret_ms = max(0.0, total_ms - q_ms)

                q_embed_ms_list.append(q_ms)
                retrieval_ms_list.append(ret_ms)
                warm_total_ms_list.append(total_ms)

                rep_rankings[case.case_id] = tuple(str(d.id) for d in docs)

                if rep_idx == 1:
                    cm = score_retrieval_case(case, docs, k=5)
                    case_metrics_rep1.append(cm)

            rankings_by_rep.append(rep_rankings)
            successful_reps += 1
            rss_checkpoints.append(process.memory_info().rss / (1024 * 1024))

        status = "completed" if successful_reps == 3 else "partial"

    except Exception as exc:
        error_msg = sanitize_benchmark_error(exc)
        if len(rankings_by_rep) > 0 and len(case_metrics_rep1) == len(cases):
            status = "partial"
        else:
            status = "failed"

    finally:
        runner.close()

    observed_peak_rss_mb = max(rss_checkpoints) if rss_checkpoints else 0.0
    rss_after_load_val = rss_checkpoints[1] if len(rss_checkpoints) > 1 else 0.0

    ranking_stable = (
        len(rankings_by_rep) == 3
        and rankings_by_rep[0] == rankings_by_rep[1] == rankings_by_rep[2]
    )

    # Calculate timings
    q_p50 = float(np.percentile(q_embed_ms_list, 50)) if q_embed_ms_list else 0.0
    q_p95 = float(np.percentile(q_embed_ms_list, 95)) if q_embed_ms_list else 0.0
    ret_p50 = float(np.percentile(retrieval_ms_list, 50)) if retrieval_ms_list else 0.0
    ret_p95 = float(np.percentile(retrieval_ms_list, 95)) if retrieval_ms_list else 0.0
    warm_p50 = float(np.percentile(warm_total_ms_list, 50)) if warm_total_ms_list else 0.0
    warm_p95 = float(np.percentile(warm_total_ms_list, 95)) if warm_total_ms_list else 0.0

    # Derive quality from rep 1
    agg_stats: dict[str, dict[str, int | float]] = {}
    if case_metrics_rep1:
        agg_stats = aggregate_case_metrics(case_metrics_rep1)

    overall_stats = agg_stats.get("overall", {
        "case_count": len(cases),
        "hit_case_count": 0,
        "recall_at_5": 0.0,
        "mrr_at_5": 0.0,
        "ndcg_at_5": 0.0,
    })

    # Gates & Comparisons
    guardrails: dict[str, bool] = {}
    all_guardrails_pass: bool | str = ""
    delta_recall_val: float | str = ""
    delta_mrr_val: float | str = ""
    delta_ndcg_val: float | str = ""
    recall_ci_lower: float | str = ""
    recall_ci_upper: float | str = ""
    mrr_ci_lower: float | str = ""
    mrr_ci_upper: float | str = ""
    ndcg_ci_lower: float | str = ""
    ndcg_ci_upper: float | str = ""
    clear_gain_ctrl_val: bool | str = ""
    best_lighter_key = ""
    clear_gain_lighter_val: bool | str = ""

    ctrl_agg_stats = (
        aggregate_case_metrics(control_result.case_metrics)
        if (control_result is not None and control_result.status == "completed" and control_result.case_metrics)
        else {}
    )

    if control_result is not None and control_result.status == "completed" and case_metrics_rep1:
        guardrails = evaluate_category_guardrails(control_result.case_metrics, case_metrics_rep1)
        all_guardrails_pass = all(guardrails.values())
        boot = paired_bootstrap_intervals(control_result.case_metrics, case_metrics_rep1, samples=10_000, seed=42)

        delta_recall_val = boot["recall"].delta
        delta_mrr_val = boot["mrr"].delta
        delta_ndcg_val = boot["ndcg"].delta
        recall_ci_lower = boot["recall"].lower
        recall_ci_upper = boot["recall"].upper
        mrr_ci_lower = boot["mrr"].lower
        mrr_ci_upper = boot["mrr"].upper
        ndcg_ci_lower = boot["ndcg"].lower
        ndcg_ci_upper = boot["ndcg"].upper

        clear_gain_ctrl_val = has_clear_gain(
            status=status,
            successful_repetitions=len(rankings_by_rep),
            guardrails=guardrails,
            ndcg_interval=boot["ndcg"],
        )

        finalist_pool = [r.summary for r in lighter_results] if lighter_results else [control_result.summary]
        best_lighter_key = select_best_lighter_finalist(setting.order, finalist_pool)

        # So sánh với best lighter
        best_lighter_match = next((r for r in lighter_results if r.setting.setting_key == best_lighter_key), None)
        if best_lighter_match is not None and best_lighter_match.status == "completed":
            guardrails_l = evaluate_category_guardrails(best_lighter_match.case_metrics, case_metrics_rep1)
            boot_l = paired_bootstrap_intervals(best_lighter_match.case_metrics, case_metrics_rep1, samples=10_000, seed=42)
            clear_gain_lighter_val = has_clear_gain(
                status=status,
                successful_repetitions=len(rankings_by_rep),
                guardrails=guardrails_l,
                ndcg_interval=boot_l["ndcg"],
            )
        else:
            clear_gain_lighter_val = clear_gain_ctrl_val

    finalist_eligible = (status == "completed" and len(rankings_by_rep) == 3)

    # Build summary (overall row)
    summary = {
        "setting_key": setting.setting_key,
        "setting_label": setting.setting_label,
        "order": setting.order,
        "category": "overall",
        "model_id": setting.model_id,
        "model_revision": setting.revision,
        "dimension": setting.dimension,
        "max_length": setting.max_length,
        "collection_name": setting.collection_name,
        "retrieval_mode": "dense",
        "use_bm25": False,
        "use_reranker": False,
        "status": status,
        "error": error_msg,
        "case_count": overall_stats["case_count"],
        "hit_case_count": overall_stats["hit_case_count"],
        "recall_at_5": overall_stats["recall_at_5"] if case_metrics_rep1 else "",
        "mrr_at_5": overall_stats["mrr_at_5"] if case_metrics_rep1 else "",
        "ndcg_at_5": overall_stats["ndcg_at_5"] if case_metrics_rep1 else "",
        "successful_repetitions": len(rankings_by_rep),
        "ranking_stable": ranking_stable if status == "completed" else "",
        "truncated_document_count": truncated_count,
        "cold_load_ms": cold_load_ms if cold_load_ms > 0 else "",
        "document_embedding_ms": doc_embed_ms if doc_embed_ms > 0 else "",
        "query_embedding_p50_ms": q_p50 if q_embed_ms_list else "",
        "query_embedding_p95_ms": q_p95 if q_embed_ms_list else "",
        "retrieval_p50_ms": ret_p50 if retrieval_ms_list else "",
        "retrieval_p95_ms": ret_p95 if retrieval_ms_list else "",
        "warm_total_p50_ms": warm_p50 if warm_total_ms_list else "",
        "warm_total_p95_ms": warm_p95 if warm_total_ms_list else "",
        "rss_before_load_mb": rss_before_load_mb,
        "rss_after_load_mb": rss_after_load_val if rss_after_load_val > 0 else "",
        "observed_peak_rss_mb": observed_peak_rss_mb if observed_peak_rss_mb > 0 else "",
        "device": "cpu",
        "dtype": "float32",
        "document_batch_size": 8,
        "query_batch_size": 1,
        "delta_recall_at_5": delta_recall_val,
        "delta_mrr_at_5": delta_mrr_val,
        "delta_ndcg_at_5": delta_ndcg_val,
        "recall_ci_lower": recall_ci_lower,
        "recall_ci_upper": recall_ci_upper,
        "mrr_ci_lower": mrr_ci_lower,
        "mrr_ci_upper": mrr_ci_upper,
        "ndcg_ci_lower": ndcg_ci_lower,
        "ndcg_ci_upper": ndcg_ci_upper,
        "category_guardrail_pass": "",
        "all_category_guardrails_pass": all_guardrails_pass,
        "clear_gain_vs_control": clear_gain_ctrl_val,
        "best_lighter_setting": best_lighter_key,
        "clear_gain_vs_best_lighter": clear_gain_lighter_val,
        "finalist_eligible": finalist_eligible,
    }

    # Build category rows
    all_cats = sorted(list({c.category for c in cases}))
    for cat in all_cats:
        cat_stat = agg_stats.get(cat, {
            "case_count": sum(1 for c in cases if c.category == cat),
            "hit_case_count": 0,
            "recall_at_5": "",
            "mrr_at_5": "",
            "ndcg_at_5": "",
        })
        cat_guardrail = guardrails.get(cat, "") if guardrails else ""

        # Calculate simple category deltas if control_result exists and is not control itself
        cat_delta_recall = ""
        cat_delta_mrr = ""
        cat_delta_ndcg = ""
        if (
            ctrl_agg_stats
            and cat in ctrl_agg_stats
            and control_result is not None
            and setting.setting_key != control_result.setting.setting_key
            and case_metrics_rep1
        ):
            ctrl_c = ctrl_agg_stats[cat]
            if isinstance(cat_stat.get("recall_at_5"), (int, float)) and isinstance(ctrl_c.get("recall_at_5"), (int, float)):
                cat_delta_recall = float(cat_stat["recall_at_5"]) - float(ctrl_c["recall_at_5"])
            if isinstance(cat_stat.get("mrr_at_5"), (int, float)) and isinstance(ctrl_c.get("mrr_at_5"), (int, float)):
                cat_delta_mrr = float(cat_stat["mrr_at_5"]) - float(ctrl_c["mrr_at_5"])
            if isinstance(cat_stat.get("ndcg_at_5"), (int, float)) and isinstance(ctrl_c.get("ndcg_at_5"), (int, float)):
                cat_delta_ndcg = float(cat_stat["ndcg_at_5"]) - float(ctrl_c["ndcg_at_5"])

        c_row = {
            "setting_key": setting.setting_key,
            "setting_label": setting.setting_label,
            "category": cat,
            "model_id": setting.model_id,
            "model_revision": setting.revision,
            "dimension": setting.dimension,
            "max_length": setting.max_length,
            "collection_name": setting.collection_name,
            "retrieval_mode": "dense",
            "use_bm25": False,
            "use_reranker": False,
            "status": status,
            "error": error_msg,
            "case_count": cat_stat["case_count"],
            "hit_case_count": cat_stat["hit_case_count"],
            "recall_at_5": cat_stat["recall_at_5"] if case_metrics_rep1 else "",
            "mrr_at_5": cat_stat["mrr_at_5"] if case_metrics_rep1 else "",
            "ndcg_at_5": cat_stat["ndcg_at_5"] if case_metrics_rep1 else "",
            "successful_repetitions": len(rankings_by_rep),
            "ranking_stable": "",
            "truncated_document_count": "",
            "cold_load_ms": "",
            "document_embedding_ms": "",
            "query_embedding_p50_ms": "",
            "query_embedding_p95_ms": "",
            "retrieval_p50_ms": "",
            "retrieval_p95_ms": "",
            "warm_total_p50_ms": "",
            "warm_total_p95_ms": "",
            "rss_before_load_mb": "",
            "rss_after_load_mb": "",
            "observed_peak_rss_mb": "",
            "device": "cpu",
            "dtype": "float32",
            "document_batch_size": 8,
            "query_batch_size": 1,
            "delta_recall_at_5": cat_delta_recall,
            "delta_mrr_at_5": cat_delta_mrr,
            "delta_ndcg_at_5": cat_delta_ndcg,
            "recall_ci_lower": "",
            "recall_ci_upper": "",
            "mrr_ci_lower": "",
            "mrr_ci_upper": "",
            "ndcg_ci_lower": "",
            "ndcg_ci_upper": "",
            "category_guardrail_pass": cat_guardrail,
            "all_category_guardrails_pass": "",
            "clear_gain_vs_control": "",
            "best_lighter_setting": "",
            "clear_gain_vs_best_lighter": "",
            "finalist_eligible": "",
        }
        category_rows.append(c_row)

    # Persist setting rows immediately to CSV
    all_setting_rows = [summary] + category_rows
    upsert_embedding_results_csv(all_setting_rows)

    return EmbeddingBenchmarkResult(
        setting=setting,
        status=status,
        error=error_msg,
        summary=summary,
        category_rows=category_rows,
        case_metrics=case_metrics_rep1,
        rankings_by_repetition=rankings_by_rep,
    )


def run_embedding_benchmarks(
    settings: tuple[DenseBenchmarkSetting, ...],
    benchmark_inputs: EmbeddingBenchmarkInputs,
    *,
    control_result: EmbeddingBenchmarkResult,
    expected_active_snapshot: dict[str, object],
):
    """Generator tuần tự chạy từng candidate, cập nhật danh sách lighter finalists và giải phóng tài nguyên."""
    lighter_finalists: list[EmbeddingBenchmarkResult] = []
    if control_result.status == "completed":
        lighter_finalists.append(control_result)

    for setting in settings:
        res = run_embedding_benchmark(
            setting,
            benchmark_inputs,
            control_result=control_result,
            lighter_results=tuple(lighter_finalists),
            expected_active_snapshot=expected_active_snapshot,
        )
        if res.status == "completed" and res.summary.get("clear_gain_vs_control") is True:
            lighter_finalists.append(res)

        yield res


# --- 6. Display Helpers for Notebook ---


def describe_embedding_benchmark_environment() -> dict[str, str]:
    """Hiển thị thông tin môi trường thực thi CPU FP32, Qdrant và các gói phụ thuộc an toàn."""
    import importlib.metadata as m
    packages = {
        "FlagEmbedding": m.version("FlagEmbedding"),
        "sentence-transformers": m.version("sentence-transformers"),
        "transformers": m.version("transformers"),
        "torch": m.version("torch"),
        "qdrant-client": m.version("qdrant-client"),
        "pyvi": m.version("pyvi"),
    }
    return {
        "device": "CPU",
        "dtype": "FP32",
        "packages": str(packages),
        "cpu_count": str(os.cpu_count()),
    }


def settings_table() -> pl.DataFrame:
    """Trả về bảng 8 cấu hình dense embedding trong catalog Phase 8 08a kèm trạng thái authorized/deferred."""
    data = [
        {
            "Order": s.order,
            "Key": s.setting_key,
            "Label": s.setting_label,
            "Model ID": s.model_id,
            "Revision": s.revision[:8] + "...",
            "Dim": s.dimension,
            "Max Len": s.max_length,
            "Collection": s.collection_name,
            "Scope Status": "Authorized (Now)" if s in AUTHORIZED_DENSE_SETTINGS else "Deferred (Future)",
        }
        for s in ALL_DENSE_SETTINGS
    ]
    return pl.DataFrame(data)


def display_canonical_inputs(inputs: EmbeddingBenchmarkInputs) -> dict[str, object]:
    """Hiển thị tóm tắt canonical inputs (số câu Golden V3, số chunks)."""
    return {
        "golden_v3_cases": len(inputs.cases),
        "canonical_chunks": len(inputs.chunks),
        "sample_question": inputs.cases[0].question,
        "sample_evidence": inputs.cases[0].evidence,
    }


def quality_table(control_result: EmbeddingBenchmarkResult, candidate_results: list[EmbeddingBenchmarkResult]) -> pl.DataFrame:
    """Bảng hiển thị chất lượng retrieval (Recall@5, MRR@5, nDCG@5) cho control và candidates."""
    all_res = [control_result] + candidate_results
    data = []
    for r in all_res:
        s = r.summary
        data.append({
            "Key": s.get("setting_key"),
            "Label": s.get("setting_label"),
            "Status": s.get("status"),
            "Hits": f"{s.get('hit_case_count')}/{s.get('case_count')}",
            "Recall@5": f"{s.get('recall_at_5'):.4f}" if isinstance(s.get("recall_at_5"), (int, float)) else "",
            "MRR@5": f"{s.get('mrr_at_5'):.4f}" if isinstance(s.get("mrr_at_5"), (int, float)) else "",
            "nDCG@5": f"{s.get('ndcg_at_5'):.4f}" if isinstance(s.get("ndcg_at_5"), (int, float)) else "",
            "Stable": s.get("ranking_stable"),
        })
    return pl.DataFrame(data)


def comparison_table(control_result: EmbeddingBenchmarkResult, candidate_results: list[EmbeddingBenchmarkResult]) -> pl.DataFrame:
    """Bảng so sánh Bootstrap Delta nDCG, Guardrails và Clear Gain decisions."""
    data = []
    for r in candidate_results:
        s = r.summary
        delta_str = f"{s.get('delta_ndcg_at_5'):+.4f}" if isinstance(s.get("delta_ndcg_at_5"), (int, float)) else ""
        ci_str = f"[{s.get('ndcg_ci_lower'):+.4f}, {s.get('ndcg_ci_upper'):+.4f}]" if isinstance(s.get("ndcg_ci_lower"), (int, float)) else ""
        data.append({
            "Candidate": s.get("setting_key"),
            "Delta nDCG@5": delta_str,
            "95% CI": ci_str,
            "Guardrails": s.get("all_category_guardrails_pass"),
            "Gain vs Control": s.get("clear_gain_vs_control"),
            "Best Lighter": s.get("best_lighter_setting"),
            "Gain vs Lighter": s.get("clear_gain_vs_best_lighter"),
            "Finalist Eligible": s.get("finalist_eligible"),
        })
    return pl.DataFrame(data)


def category_table(control_result: EmbeddingBenchmarkResult, candidate_results: list[EmbeddingBenchmarkResult]) -> pl.DataFrame:
    """Bảng hiển thị chi tiết chất lượng truy xuất và guardrail theo từng category."""
    all_res = [control_result] + candidate_results
    data = []
    for r in all_res:
        for c_row in r.category_rows:
            delta_ndcg = c_row.get("delta_ndcg_at_5")
            delta_str = f"{delta_ndcg:+.4f}" if isinstance(delta_ndcg, (int, float)) else ""
            data.append({
                "Category": c_row.get("category"),
                "Model": c_row.get("setting_key"),
                "Cases": f"{c_row.get('hit_case_count')}/{c_row.get('case_count')}",
                "Recall@5": f"{c_row.get('recall_at_5'):.4f}" if isinstance(c_row.get("recall_at_5"), (int, float)) else "",
                "MRR@5": f"{c_row.get('mrr_at_5'):.4f}" if isinstance(c_row.get("mrr_at_5"), (int, float)) else "",
                "nDCG@5": f"{c_row.get('ndcg_at_5'):.4f}" if isinstance(c_row.get("ndcg_at_5"), (int, float)) else "",
                "Delta nDCG": delta_str,
                "Guardrail": c_row.get("category_guardrail_pass"),
            })
    return pl.DataFrame(data).sort(["Category", "Model"])


def latency_table(control_result: EmbeddingBenchmarkResult, candidate_results: list[EmbeddingBenchmarkResult]) -> pl.DataFrame:
    """Bảng hiển thị chi tiết độ trễ cold load, document embedding và per-query p50/p95."""
    all_res = [control_result] + candidate_results
    data = []
    for r in all_res:
        s = r.summary
        data.append({
            "Key": s.get("setting_key"),
            "Cold Load (s)": f"{s.get('cold_load_ms') / 1000.0:.2f}" if isinstance(s.get("cold_load_ms"), (int, float)) else "",
            "Doc Embed (s)": f"{s.get('document_embedding_ms') / 1000.0:.2f}" if isinstance(s.get("document_embedding_ms"), (int, float)) else "",
            "Query p50 (ms)": f"{s.get('query_embedding_p50_ms'):.2f}" if isinstance(s.get("query_embedding_p50_ms"), (int, float)) else "",
            "Query p95 (ms)": f"{s.get('query_embedding_p95_ms'):.2f}" if isinstance(s.get("query_embedding_p95_ms"), (int, float)) else "",
            "Ret p50 (ms)": f"{s.get('retrieval_p50_ms'):.2f}" if isinstance(s.get("retrieval_p50_ms"), (int, float)) else "",
            "Ret p95 (ms)": f"{s.get('retrieval_p95_ms'):.2f}" if isinstance(s.get("retrieval_p95_ms"), (int, float)) else "",
            "Total p50 (ms)": f"{s.get('warm_total_p50_ms'):.2f}" if isinstance(s.get("warm_total_p50_ms"), (int, float)) else "",
            "Total p95 (ms)": f"{s.get('warm_total_p95_ms'):.2f}" if isinstance(s.get("warm_total_p95_ms"), (int, float)) else "",
        })
    return pl.DataFrame(data)


def resource_table(control_result: EmbeddingBenchmarkResult, candidate_results: list[EmbeddingBenchmarkResult]) -> pl.DataFrame:
    """Bảng hiển thị mức tiêu thụ bộ nhớ RSS và số lượng văn bản bị cắt ngắn."""
    all_res = [control_result] + candidate_results
    data = []
    for r in all_res:
        s = r.summary
        data.append({
            "Key": s.get("setting_key"),
            "RSS Before (MB)": f"{s.get('rss_before_load_mb'):.1f}" if isinstance(s.get("rss_before_load_mb"), (int, float)) else "",
            "RSS After Load (MB)": f"{s.get('rss_after_load_mb'):.1f}" if isinstance(s.get("rss_after_load_mb"), (int, float)) else "",
            "Peak RSS (MB)": f"{s.get('observed_peak_rss_mb'):.1f}" if isinstance(s.get("observed_peak_rss_mb"), (int, float)) else "",
            "Truncated Docs": s.get("truncated_document_count"),
        })
    return pl.DataFrame(data)


def failure_table(control_result: EmbeddingBenchmarkResult, candidate_results: list[EmbeddingBenchmarkResult]) -> pl.DataFrame:
    """Bảng ghi nhận trạng thái và lỗi (nếu có) của từng cấu hình."""
    all_res = [control_result] + candidate_results
    data = []
    for r in all_res:
        s = r.summary
        data.append({
            "Key": s.get("setting_key"),
            "Status": s.get("status"),
            "Reps": s.get("successful_repetitions"),
            "Error": s.get("error") if s.get("error") else "None",
        })
    return pl.DataFrame(data)
