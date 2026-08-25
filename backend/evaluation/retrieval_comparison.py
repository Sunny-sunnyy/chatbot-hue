import argparse
import copy
import json
import statistics
import time
from pathlib import Path

from core.settings_loader import load_settings
from evaluation.eval import score_retrieval
from evaluation.test import DEFAULT_TEST_FILE, load_tests
from retrieval.service import build_service

PROFILES = ("dense_only", "hybrid_no_rerank", "hybrid_rerank")


def summarize_profile(rows):
    successful = [row for row in rows if not row["error"]]
    latencies = [row["latency_ms"] for row in successful]
    summary = {
        "questions": len(rows),
        "successful": len(successful),
        "failed": len(rows) - len(successful),
        "mean_latency_ms": round(statistics.fmean(latencies), 2) if latencies else 0.0,
    }
    metric_rows = [row["metrics"] for row in successful if row.get("metrics")]
    if metric_rows:
        summary.update({
            "mean_mrr": round(statistics.fmean(row["mrr"] for row in metric_rows), 4),
            "mean_ndcg": round(statistics.fmean(row["ndcg"] for row in metric_rows), 4),
            "mean_keyword_coverage": round(
                statistics.fmean(row["keyword_coverage"] for row in metric_rows), 2
            ),
        })
    return summary


def run_collection_profiles(collection_name, profiles=PROFILES, test_path=DEFAULT_TEST_FILE):
    tests = load_tests(test_path)
    runs = {}
    for profile in profiles:
        settings = copy.deepcopy(load_settings())
        settings["active_profile"] = profile
        settings["vector_database"]["collection_name"] = collection_name
        service = build_service(settings)
        rows = []
        for test in tests:
            started = time.perf_counter()
            try:
                documents = service.search(test.question)
                latency_ms = round((time.perf_counter() - started) * 1000, 2)
                metrics = score_retrieval(test.keywords, [doc.text for doc in documents])
                rows.append({
                    "category": test.category,
                    "question": test.question,
                    "ids": [doc.id for doc in documents],
                    "scores": [doc.score for doc in documents],
                    "latency_ms": latency_ms,
                    "metrics": metrics.model_dump(),
                    "error": "",
                })
            except Exception as exc:
                rows.append({
                    "category": test.category,
                    "question": test.question,
                    "ids": [],
                    "scores": [],
                    "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                    "metrics": {},
                    "error": f"{type(exc).__name__}: {exc}",
                })
        runs[profile] = {"summary": summarize_profile(rows), "rows": rows}
    return {"collection_name": collection_name, "profiles": runs}


def compare_profile_runs(active_rows, candidate_rows):
    if [row["question"] for row in active_rows] != [row["question"] for row in candidate_rows]:
        raise ValueError("active and candidate questions differ")
    return [
        {
            "question": active["question"],
            "active_ids": active["ids"],
            "candidate_ids": candidate["ids"],
            "same_ids_in_order": active["ids"] == candidate["ids"],
            "active_error": active["error"],
            "candidate_error": candidate["error"],
        }
        for active, candidate in zip(active_rows, candidate_rows)
    ]


def compare_runs(active, candidate):
    if set(active["profiles"]) != set(candidate["profiles"]):
        raise ValueError("active and candidate profiles differ")
    return {
        "active": active,
        "candidate": candidate,
        "differences": {
            profile: compare_profile_runs(
                active["profiles"][profile]["rows"],
                candidate["profiles"][profile]["rows"],
            )
            for profile in active["profiles"]
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run retrieval-only evidence on one exact collection")
    parser.add_argument("--collection", required=True)
    parser.add_argument("--tests", type=Path, default=DEFAULT_TEST_FILE)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = run_collection_profiles(args.collection, test_path=args.tests)
    if args.baseline is not None:
        active = json.loads(args.baseline.read_text(encoding="utf-8"))
        result = compare_runs(active, result)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    displayed = result["candidate"] if args.baseline is not None else result
    print(json.dumps({p: value["summary"] for p, value in displayed["profiles"].items()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
