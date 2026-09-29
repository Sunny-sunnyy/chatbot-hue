"""CLI runner for Phase 5 full-corpus retrieval preflight and smoke matrix.

Executes all 16 configuration cells across 7 private P7 questions, validates
determinism, measures cold/warm latency, and records redacted local evidence.
"""
from __future__ import annotations

import argparse
from collections.abc import Sequence
from dataclasses import asdict
import datetime
import json
import logging
import math
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import numpy as np

try:
    from backend.core.schema import (
        ComponentNotReadyError,
        InvalidQueryError,
        RetrievalConfigurationError,
        RetrievalDependencyError,
    )
    from backend.ingestion.full_corpus_pipeline import (
        FULL_CORPUS_CANDIDATES,
        candidate_by_id,
    )
    from backend.retrieval.full_corpus import (
        Classification,
        FullCorpusRetrievalService,
        RerankerMode,
        RetrievalResult,
        RetrievalTreatment,
        build_full_corpus_retrieval_service,
    )
except ModuleNotFoundError:
    from core.schema import (
        ComponentNotReadyError,
        InvalidQueryError,
        RetrievalConfigurationError,
        RetrievalDependencyError,
    )
    from ingestion.full_corpus_pipeline import (
        FULL_CORPUS_CANDIDATES,
        candidate_by_id,
    )
    from retrieval.full_corpus import (
        Classification,
        FullCorpusRetrievalService,
        RerankerMode,
        RetrievalResult,
        RetrievalTreatment,
        build_full_corpus_retrieval_service,
    )

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("full_corpus_smoke")

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_QUESTIONS_PATH = REPO_ROOT / "data/full_corpus_phase_5_smoke_questions.json"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "data/full_corpus_phase_5_smoke_trace.json"

EXPECTED_P7_ORDER = (
    "foods",
    "heritages",
    "festivals",
    "performing_arts",
    "travel_places",
    "travel_services",
    "travel_tickets",
)
EXPECTED_QUERY_IDS = tuple(f"P5-Q0{i}" for i in range(1, 8))
ALL_CANDIDATE_IDS = tuple(c.candidate_id for c in FULL_CORPUS_CANDIDATES)
ALL_TREATMENTS: tuple[RetrievalTreatment, ...] = ("dense_bm25_rrf", "native_hybrid_rrf")
ALL_RERANKERS: tuple[RerankerMode, ...] = ("none", "minilm")

PATH_PATTERN = re.compile(r"(?:/|[a-zA-Z]:\\)[^\s,;:\"'()<>]+")


def sanitize_error_detail(exc: Exception) -> dict[str, str]:
    """Sanitize exception into fixed allowlisted code and safe type/category.

    Guaranteed not to derive any persisted field from raw str(exc),
    preventing query, secret, config, or path leakage.
    """
    error_type = type(exc).__name__
    if isinstance(exc, (ComponentNotReadyError, RetrievalConfigurationError)):
        category = "readiness_or_configuration"
        error_code = "ERR_READINESS"
    elif isinstance(exc, RetrievalDependencyError):
        category = "dependency_failure"
        error_code = "ERR_DEPENDENCY"
    elif isinstance(exc, InvalidQueryError):
        category = "invalid_query"
        error_code = "ERR_INVALID_QUERY"
    elif isinstance(exc, (FileNotFoundError, PermissionError)):
        category = "filesystem"
        error_code = "ERR_FILESYSTEM"
    elif isinstance(exc, ValueError):
        category = "value_error"
        error_code = "ERR_VALUE"
    else:
        category = "internal_error"
        error_code = "ERR_INTERNAL"

    return {
        "error_type": error_type,
        "error_category": category,
        "error_code": error_code,
    }


def validate_safe_output_path(output_path: Path) -> Path:
    """Validate that output path is safe (outside repository or gitignored within repo)."""
    resolved = output_path.resolve()
    is_inside_repo = False
    try:
        rel_path = resolved.relative_to(REPO_ROOT)
        is_inside_repo = True
    except ValueError:
        is_inside_repo = False

    if is_inside_repo:
        proc = subprocess.run(
            ["git", "check-ignore", "-q", str(rel_path)],
            cwd=REPO_ROOT,
            capture_output=True,
        )
        if proc.returncode != 0:
            raise ValueError(f"Unsafe output path: {output_path} is inside repository and not gitignored")

    return resolved


def validate_selectors(
    select_candidate: Sequence[str] | None = None,
    select_treatment: Sequence[str] | None = None,
    select_reranker: Sequence[str] | None = None,
    select_query_id: Sequence[str] | None = None,
) -> tuple[tuple[str, ...], tuple[RetrievalTreatment, ...], tuple[RerankerMode, ...], tuple[str, ...]]:
    """Strictly validate matrix selectors, rejecting unknown values or empty combinations."""
    if select_candidate is not None:
        if len(select_candidate) == 0:
            raise ValueError("Candidate selector list cannot be empty")
        for c in select_candidate:
            if c not in ALL_CANDIDATE_IDS:
                raise ValueError(f"Unknown candidate selector: {c!r}. Allowed: {ALL_CANDIDATE_IDS}")
        candidates = tuple(select_candidate)
    else:
        candidates = ALL_CANDIDATE_IDS

    if select_treatment is not None:
        if len(select_treatment) == 0:
            raise ValueError("Treatment selector list cannot be empty")
        for t in select_treatment:
            if t not in ALL_TREATMENTS:
                raise ValueError(f"Unknown treatment selector: {t!r}. Allowed: {ALL_TREATMENTS}")
        treatments = tuple(select_treatment)  # type: ignore
    else:
        treatments = ALL_TREATMENTS

    if select_reranker is not None:
        if len(select_reranker) == 0:
            raise ValueError("Reranker selector list cannot be empty")
        for r in select_reranker:
            if r not in ALL_RERANKERS:
                raise ValueError(f"Unknown reranker selector: {r!r}. Allowed: {ALL_RERANKERS}")
        rerankers = tuple(select_reranker)  # type: ignore
    else:
        rerankers = ALL_RERANKERS

    if select_query_id is not None:
        if len(select_query_id) == 0:
            raise ValueError("Query selector list cannot be empty")
        for q in select_query_id:
            if q not in EXPECTED_QUERY_IDS:
                raise ValueError(f"Unknown query selector: {q!r}. Allowed: {EXPECTED_QUERY_IDS}")
        queries = tuple(select_query_id)
    else:
        queries = EXPECTED_QUERY_IDS

    total_cells = len(candidates) * len(treatments) * len(rerankers)
    if total_cells == 0:
        raise ValueError("Matrix selector combination results in 0 cells")
    if len(queries) == 0:
        raise ValueError("Selected query list is empty")

    return candidates, treatments, rerankers, queries


def load_and_validate_questions(questions_path: Path) -> list[dict[str, str]]:
    """Validate that questions file has exactly 7 valid items in exact P7 order."""
    if not questions_path.is_file():
        raise FileNotFoundError(f"Smoke questions file not found: {questions_path}")

    raw_data = json.loads(questions_path.read_text(encoding="utf-8"))
    if not isinstance(raw_data, list):
        raise ValueError("Questions file root must be a JSON array")
    if len(raw_data) != 7:
        raise ValueError(f"Questions file must contain exactly 7 queries, got {len(raw_data)}")

    validated = []
    for idx, item in enumerate(raw_data):
        qid = item.get("query_id")
        partition = item.get("partition")
        question = item.get("question")

        expected_qid = EXPECTED_QUERY_IDS[idx]
        expected_part = EXPECTED_P7_ORDER[idx]

        if qid != expected_qid:
            raise ValueError(f"Query {idx} ID mismatch: {qid!r} != {expected_qid!r}")
        if partition != expected_part:
            raise ValueError(f"Query {idx} partition mismatch: {partition!r} != {expected_part!r}")
        if not isinstance(question, str) or not question.strip():
            raise ValueError(f"Query {idx} question must be non-empty string")

        validated.append({"query_id": qid, "partition": partition, "question": question.strip()})

    return validated


def run_preflight(questions_path: Path, candidate_filter: Sequence[str] | None = None) -> int:
    """Preflight all candidate collection/state/model contracts."""
    logger.info("Starting Full-corpus Phase 5 preflight...")
    questions = load_and_validate_questions(questions_path)
    logger.info("Validated %d smoke questions in exact P7 order", len(questions))

    if candidate_filter is not None:
        if len(candidate_filter) == 0:
            raise ValueError("Candidate selector list cannot be empty")
        for c in candidate_filter:
            if c not in ALL_CANDIDATE_IDS:
                raise ValueError(f"Unknown candidate selector: {c!r}. Allowed: {ALL_CANDIDATE_IDS}")
        candidates_to_check = candidate_filter
    else:
        candidates_to_check = ALL_CANDIDATE_IDS
    failures = 0

    for cid in candidates_to_check:
        logger.info("--- Preflighting candidate: %s ---", cid)
        t_start = time.perf_counter()
        try:
            # Build service with none reranker
            service_none = build_full_corpus_retrieval_service(
                candidate_id=cid,
                retrieval_treatment="dense_bm25_rrf",
                reranker="none",
            )
            service_none.close()
            logger.info("  [OK] candidate %s build-record, sparse-state, Qdrant collection, dense model ready", cid)

            # Preflight MiniLM reranker
            service_minilm = build_full_corpus_retrieval_service(
                candidate_id=cid,
                retrieval_treatment="dense_bm25_rrf",
                reranker="minilm",
            )
            service_minilm.close()
            logger.info("  [OK] candidate %s MiniLM reranker ready", cid)

            elapsed_s = time.perf_counter() - t_start
            logger.info("  Candidate %s preflight PASSED (%.2f s)", cid, elapsed_s)
        except Exception as exc:
            err = sanitize_error_detail(exc)
            logger.error(
                "  [FAIL] Candidate %s preflight failed: code=%s, type=%s, category=%s",
                cid,
                err["error_code"],
                err["error_type"],
                err["error_category"],
            )
            failures += 1

    if failures > 0:
        logger.error("Preflight finished with %d failure(s)", failures)
        return 1
    logger.info("Preflight finished successfully: all candidates ready.")
    return 0


def run_smoke_matrix(
    questions_path: Path,
    output_path: Path,
    select_candidate: Sequence[str] | None = None,
    select_treatment: Sequence[str] | None = None,
    select_reranker: Sequence[str] | None = None,
    select_query_id: Sequence[str] | None = None,
) -> int:
    """Run smoke matrix, determinism check, and latency profiling."""
    candidates, treatments, rerankers, target_qids = validate_selectors(
        select_candidate=select_candidate,
        select_treatment=select_treatment,
        select_reranker=select_reranker,
        select_query_id=select_query_id,
    )
    safe_output = validate_safe_output_path(output_path)

    all_questions = load_and_validate_questions(questions_path)
    questions = [q for q in all_questions if q["query_id"] in target_qids]
    if not questions:
        raise ValueError(f"No questions matched selected query IDs: {target_qids}")

    logger.info(
        "Running matrix: %d candidates × %d treatments × %d rerankers = %d cells on %d queries",
        len(candidates),
        len(treatments),
        len(rerankers),
        len(candidates) * len(treatments) * len(rerankers),
        len(questions),
    )

    cell_results: dict[str, Any] = {}
    any_cell_failed = False
    any_cell_review_required = False

    for cid in candidates:
        for treatment in treatments:
            for reranker_mode in rerankers:
                cell_id = f"{cid}__{treatment}__{reranker_mode}"
                logger.info(">>> Executing cell: %s <<<", cell_id)
                cell_anomalies: set[str] = set()
                cell_classification: Classification = "PASS"
                query_records: list[dict[str, Any]] = []

                t_cold_start = time.perf_counter()
                service: FullCorpusRetrievalService | None = None
                try:
                    service = build_full_corpus_retrieval_service(
                        candidate_id=cid,
                        retrieval_treatment=treatment,
                        reranker=reranker_mode,
                    )
                    cold_load_ms = round((time.perf_counter() - t_cold_start) * 1000.0, 2)

                    # Pass 1: Run each query once
                    first_pass_results: list[RetrievalResult] = []
                    for q_item in questions:
                        res = service.search(q_item["question"])
                        first_pass_results.append(res)
                        for anom in res.trace.anomalies:
                            cell_anomalies.add(anom)
                        if res.trace.classification == "REVIEW_REQUIRED":
                            cell_classification = "REVIEW_REQUIRED"
                        elif res.trace.classification == "FAIL":
                            cell_classification = "FAIL"

                        query_records.append({
                            "query_id": q_item["query_id"],
                            "partition": q_item["partition"],
                            "counts": res.trace.counts,
                            "timings_ms": res.trace.timings_ms,
                            "rerank_status": res.trace.rerank_status,
                            "anomalies": list(res.trace.anomalies),
                            "classification": res.trace.classification,
                            "final_doc_ids": [doc.id for doc in res.documents],
                            "final_scores": [round(doc.score, 6) for doc in res.documents],
                        })

                    # Pass 2: Determinism check (rerun exact 7 queries and assert identical IDs/scores)
                    determinism_pass = True
                    for q_item, first_res in zip(questions, first_pass_results):
                        second_res = service.search(q_item["question"])
                        first_ids = [d.id for d in first_res.documents]
                        second_ids = [d.id for d in second_res.documents]
                        first_scores = [round(d.score, 6) for d in first_res.documents]
                        second_scores = [round(d.score, 6) for d in second_res.documents]

                        if first_ids != second_ids or first_scores != second_scores:
                            logger.error(
                                "Determinism failure on query %s: IDs (%s vs %s) or scores differ",
                                q_item["query_id"],
                                first_ids,
                                second_ids,
                            )
                            determinism_pass = False
                            cell_classification = "FAIL"
                            cell_anomalies.add("determinism_mismatch")

                    # If MiniLM reranker mode: collect at least 20 warm Top30 reranker observations
                    warm_latencies_ms: list[float] = []
                    p95_latency_ms = 0.0

                    if reranker_mode == "minilm":
                        # We already did pass 1 (7 queries) and pass 2 (7 queries) = 14 queries.
                        # Do additional deterministic repeats until at least 21 warm observations total.
                        warm_latencies_ms.extend([r.trace.timings_ms.get("total_ms", 0.0) for r in first_pass_results])
                        while len(warm_latencies_ms) < 21:
                            for q_item in questions:
                                rep_res = service.search(q_item["question"])
                                warm_latencies_ms.append(rep_res.trace.timings_ms.get("total_ms", 0.0))
                                if len(warm_latencies_ms) >= 21:
                                    break

                        p95_latency_ms = float(np.percentile(warm_latencies_ms, 95))
                        logger.info(
                            "MiniLM warm observations: count=%d, p95=%.1f ms, cold_load=%.1f ms",
                            len(warm_latencies_ms),
                            p95_latency_ms,
                            cold_load_ms,
                        )
                        if p95_latency_ms > 3000.0:
                            logger.error("Latency gate exceeded: p95=%.1f ms > 3000 ms", p95_latency_ms)
                            cell_classification = "FAIL"
                            cell_anomalies.add("latency_gate_exceeded")
                    else:
                        all_totals = [r.trace.timings_ms.get("total_ms", 0.0) for r in first_pass_results]
                        p95_latency_ms = float(np.percentile(all_totals, 95)) if all_totals else 0.0

                    cell_results[cell_id] = {
                        "candidate_id": cid,
                        "retrieval_treatment": treatment,
                        "reranker": reranker_mode,
                        "classification": cell_classification,
                        "anomalies": sorted(cell_anomalies),
                        "determinism_pass": determinism_pass,
                        "cold_load_ms": cold_load_ms,
                        "latency_p95_ms": round(p95_latency_ms, 2),
                        "observation_count": len(warm_latencies_ms) if reranker_mode == "minilm" else len(questions),
                        "queries": query_records,
                    }

                    if cell_classification == "FAIL":
                        any_cell_failed = True
                    elif cell_classification == "REVIEW_REQUIRED":
                        any_cell_review_required = True

                    logger.info(
                        "Cell %s result: %s (anomalies=%s, determinism=%s, p95=%.1f ms)",
                        cell_id,
                        cell_classification,
                        list(cell_anomalies),
                        determinism_pass,
                        p95_latency_ms,
                    )

                except Exception as exc:
                    err = sanitize_error_detail(exc)
                    logger.error(
                        "Cell %s failed: code=%s, type=%s, category=%s",
                        cell_id,
                        err["error_code"],
                        err["error_type"],
                        err["error_category"],
                    )
                    any_cell_failed = True
                    cell_results[cell_id] = {
                        "candidate_id": cid,
                        "retrieval_treatment": treatment,
                        "reranker": reranker_mode,
                        "classification": "FAIL",
                        "anomalies": ["cell_exception"],
                        "error": err,
                    }
                finally:
                    if service is not None:
                        service.close()

    # Determine overall status
    if len(cell_results) == 0:
        overall_classification: Classification = "FAIL"
    elif any_cell_failed:
        overall_classification = "FAIL"
    elif any_cell_review_required:
        overall_classification = "REVIEW_REQUIRED"
    else:
        overall_classification = "PASS"

    # Write output trace atomically to validated safe path
    trace_data = {
        "schema_version": "phase_5_full_corpus_smoke_trace:v1",
        "timestamp_iso": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_cells": len(cell_results),
        "overall_classification": overall_classification,
        "cells": cell_results,
    }

    safe_output.parent.mkdir(parents=True, exist_ok=True)
    temp_output = safe_output.with_name(f"{safe_output.name}.tmp.{int(time.time())}")
    temp_output.write_text(json.dumps(trace_data, indent=2, ensure_ascii=False), encoding="utf-8")
    temp_output.replace(safe_output)
    logger.info("Wrote smoke trace to %s", safe_output)

    # Return exit code
    if overall_classification != "PASS":
        logger.warning("Smoke matrix finished with status %s", overall_classification)
        return 1
    logger.info("Smoke matrix finished successfully: PASS on all cells.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Full-corpus Phase 5 Smoke Matrix CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # preflight command
    p_preflight = subparsers.add_parser("preflight", help="Preflight readiness for all candidates")
    p_preflight.add_argument("--questions", type=Path, default=DEFAULT_QUESTIONS_PATH)
    p_preflight.add_argument("--candidates", nargs="*", default=None)

    # run command
    p_run = subparsers.add_parser("run", help="Run the full smoke matrix")
    p_run.add_argument("--questions", type=Path, default=DEFAULT_QUESTIONS_PATH)
    p_run.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    p_run.add_argument("--candidate", nargs="*", default=None)
    p_run.add_argument("--treatment", nargs="*", default=None)
    p_run.add_argument("--reranker", nargs="*", default=None)
    p_run.add_argument("--select", nargs="*", default=None, help="Select specific query IDs")

    args = parser.parse_args()

    try:
        if args.command == "preflight":
            return run_preflight(args.questions, args.candidates)
        elif args.command == "run":
            return run_smoke_matrix(
                questions_path=args.questions,
                output_path=args.output,
                select_candidate=args.candidate,
                select_treatment=args.treatment,
                select_reranker=args.reranker,
                select_query_id=args.select,
            )
    except Exception as exc:
        err = sanitize_error_detail(exc)
        logger.error(
            "CLI execution failed: code=%s, type=%s, category=%s",
            err["error_code"],
            err["error_type"],
            err["error_category"],
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
