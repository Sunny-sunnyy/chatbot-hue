"""Retrieval evaluation: artifact record building from real retrieval output.

The runner resolves the real Qdrant/embedder stack and calls the retrieval
service once per case; this module only projects documents into safe artifact
records and stamps the run identity. No provider or storage access happens
here.
"""

from evaluation.answer_eval import CircuitBreaker
from retrieval.service import RetrievalService

MAX_RETRIEVED_ITEMS = 10


RETRIEVED_ITEM_FIELDS = (
    "id",
    "chunk_id",
    "score",
    "source",
    "section",
    "title",
    "text",
    "dense_score",
    "bm25_score",
    "hybrid_score",
    "rerank_score",
    "reranker_model",
    "retrieval_profile",
    "retrieval_rank",
)


def evidence_unit_id(document):
    """Return the (source, section) pair used for dedup and matching."""
    return (document.metadata.get("source"), document.metadata.get("section"))


def item_record(document):
    """Safe projection of one retrieved document; never nests raw metadata."""
    metadata = document.metadata
    record = {
        field: metadata[field]
        for field in RETRIEVED_ITEM_FIELDS
        if field in metadata
    }
    record["id"] = document.id
    record["score"] = document.score
    record["text"] = document.text
    return record


def build_retrieval_record(
    *,
    run_id,
    timestamp_utc_plus_7,
    dataset_path,
    dataset_checksum,
    corpus_checksum,
    config_checksum,
    case_id,
    category,
    question,
    profile,
    embedding_provider,
    embedding_model,
    collection_name,
    retrieved_items,
    metrics,
    setup_latency_ms,
    latency_ms,
    status="complete",
    error_type=None,
):
    """One JSONL record for one case in the retrieval run."""
    return {
        "run_id": run_id,
        "timestamp_utc_plus_7": timestamp_utc_plus_7,
        "dataset_path": dataset_path,
        "dataset_checksum": dataset_checksum,
        "corpus_checksum": corpus_checksum,
        "config_checksum": config_checksum,
        "case_id": case_id,
        "category": category,
        "question": question,
        "profile": profile,
        "embedding_provider": embedding_provider,
        "embedding_model": embedding_model,
        "collection_name": collection_name,
        "retrieved_items": retrieved_items,
        "metrics": metrics,
        "setup_latency_ms": setup_latency_ms,
        "latency_ms": latency_ms,
        "status": status,
        "error_type": error_type,
    }


# --------------------------------------------------------------------- orchestration
def compute_corpus_checksum(settings, client):
    """Read-only SHA-256 over sorted chunk_id+text payloads (active collection)."""
    import hashlib

    db = settings["vector_database"]
    records, offset = [], None
    while True:
        batch, offset = client.scroll(
            db["collection_name"],
            limit=db["scroll_batch_size"],
            offset=offset,
            with_payload=["chunk_id", "text"],
            with_vectors=False,
            timeout=db["timeout"],
        )
        records.extend(batch)
        if offset is None:
            break
    lines = []
    for record in records:
        payload = record.payload or {}
        chunk_id, text = payload.get("chunk_id"), payload.get("text")
        if not isinstance(chunk_id, str) or not isinstance(text, str):
            raise ValueError("collection payload missing chunk_id/text")
        lines.append(f"{chunk_id}\x00{text}")
    return hashlib.sha256("\n".join(sorted(lines)).encode("utf-8")).hexdigest()


def build_service(settings, profile, client):
    """Profile-scoped real stack over the ACTIVE collection (in-memory override only)."""
    import copy

    from core.startup import build_retrieval_stack

    profile_settings = copy.deepcopy(settings)
    profile_settings["active_profile"] = profile
    return RetrievalService(
        build_retrieval_stack(profile_settings, client=client),
        rerank_top_k=settings["reranking"]["top_k"],
    )


def config_fingerprint(settings, profile):
    """Profile-scoped config digest matching the retrieval snapshot algorithm.

    Uses core.startup's verified semantic config digest (same function as the
    retrieval snapshot) so evaluation records and notebook identity checks
    agree with runtime profiles; callers must not duplicate it.
    """
    import copy

    from core.startup import _config_fingerprint

    scoped = copy.deepcopy(settings)
    scoped["active_profile"] = profile
    return _config_fingerprint(scoped)


def summarise_retrieval(records, run_id, settings, snapshot, corpus_checksum,
                        timestamp_utc_plus_7, override, results_dir,
                        status="complete"):
    """Write and return the retrieval summary payload.

    A summary with status "partial" may be replaced by a later run of the same
    run id (resume); a "complete" summary is immutable.
    """
    from evaluation import artifacts, metrics

    agg = metrics.aggregate_metrics(
        [
            {"case_id": r["case_id"], "category": r["category"],
             "status": r["status"], "metrics": r["metrics"],
             "latency_ms": r["latency_ms"]}
            for r in records
        ]
    )
    per_category_latency = {}
    for category in sorted({r["category"] for r in records}):
        values = [r["latency_ms"] for r in records
                  if r["category"] == category and r["latency_ms"]]
        if values:
            per_category_latency[category] = metrics.latency_stats(values)
    payload = {
        "run_id": run_id,
        "table": "retrieval",
        "timestamp_utc_plus_7": timestamp_utc_plus_7,
        "status": status,
        "dataset_path": records[0]["dataset_path"] if records else None,
        "dataset_checksum": records[0]["dataset_checksum"] if records else None,
        "corpus_checksum": corpus_checksum,
        "profile": records[0]["profile"] if records else None,
        "collection_name": snapshot.collection_name,
        "point_count": snapshot.point_count,
        "embedding_model": snapshot.embedding_model,
        "embedding_dimension": snapshot.embedding_dimension,
        "config_checksum": snapshot.config_fingerprint,
        "evaluation_override": override,
        "metrics": agg,
        "latency": {
            "overall": metrics.latency_stats(
                [r["latency_ms"] for r in records if r["latency_ms"]]
            ),
            "per_category": per_category_latency,
            "setup_latency_ms": records[0]["setup_latency_ms"] if records else None,
        },
        "completed_case_count": len([r for r in records if r.get("status") == "complete"]),
        "failed_case_count": len([r for r in records if r.get("status") != "complete"]),
    }
    artifacts.write_summary(
        results_dir / "retrieval" / f"{run_id}.summary.json", payload)
    return payload


def run_retrieval(settings, dataset, profiles, *, results_dir, quiet=False,
                  resume=None, max_cases=None, print_fn=print, timestamp_utc7=None):
    """Retrieval stage: sequential, read-only, resumable, circuit-broken.

    Each case contributes exactly one effective row (resume rewrites the
    partial file atomically), and a summary marked "partial" is replaceable
    while the run is still working. Only a fully complete run is finalized.
    max_cases clips the case list for fast diagnostic subsets; it is recorded
    via the summary status/override and never treated as comparison evidence.
    """
    import time as _time

    from datetime import datetime, timedelta, timezone

    from evaluation import artifacts, metrics
    from vectorstore.qdrant import get_client

    timestamp_utc7 = timestamp_utc7 or datetime.now(timezone(timedelta(hours=7)))
    ts_run = timestamp_utc7.strftime("%Y%m%d-%H%M%S")
    ts_display = timestamp_utc7.strftime("%Y-%m-%d %H:%M:%S")
    db = settings["vector_database"]
    embedding = settings["embedding"]
    client = get_client(db["url"], db["timeout"])
    corpus_checksum = compute_corpus_checksum(settings, client)
    summaries = []
    for profile in profiles:
        if resume:
            run_id = resume
            if not run_id.startswith("retrieval-") or len(profiles) != 1:
                raise ValueError(
                    "resume takes exactly one profile and a retrieval run id "
                    f"(profiles={list(profiles)}, resume={resume!r})"
                )
            partial = results_dir / "retrieval" / f"{run_id}.partial.jsonl"
            final = results_dir / "retrieval" / f"{run_id}.jsonl"
            if not (partial.exists() or final.exists()):
                raise ValueError(f"cannot resume {run_id}: no partial or final artifact found")
        else:
            run_id = artifacts.make_run_id("retrieval", profile,
                                           dataset.dataset_checksum, ts_run)
            partial = results_dir / "retrieval" / f"{run_id}.partial.jsonl"
            final = results_dir / "retrieval" / f"{run_id}.jsonl"
            if final.exists():
                raise ValueError(f"run {run_id} already completed; refusing to overwrite")
        started = _time.monotonic()
        service = build_service(settings, profile, client)
        setup_latency_ms = round((_time.monotonic() - started) * 1000)
        snapshot = service.snapshot
        cases_by_id = {c.case_id: c for c in dataset.cases}

        records = {}
        if final.exists():
            raw_records = artifacts.read_records(final)
        elif partial.exists():
            raw_records = artifacts.read_records(partial)
        else:
            raw_records = []

        seen_cases = set()
        for r in raw_records:
            if not isinstance(r, dict):
                raise ValueError(f"cannot resume {run_id}: row is not a dict")
            if r.get("run_id") != run_id:
                raise ValueError(
                    f"cannot resume {run_id}: row has unexpected run_id {r.get('run_id')!r}"
                )
            case_id = r.get("case_id")
            if not case_id or not isinstance(case_id, str):
                raise ValueError(f"cannot resume {run_id}: row missing valid case_id")
            if case_id in seen_cases:
                raise ValueError(
                    f"cannot resume {run_id}: duplicate case_id {case_id}"
                )
            seen_cases.add(case_id)
            case = cases_by_id.get(case_id)
            if case is None:
                raise ValueError(
                    f"cannot resume {run_id}: row {case_id} is not in the dataset"
                )
            if r.get("dataset_checksum") != dataset.dataset_checksum:
                raise ValueError(
                    f"cannot resume {run_id}: row {case_id} has a different dataset checksum"
                )
            if r.get("corpus_checksum") != corpus_checksum:
                raise ValueError(
                    f"cannot resume {run_id}: row {case_id} corpus checksum mismatch"
                )
            if r.get("config_checksum") != snapshot.config_fingerprint:
                raise ValueError(
                    f"cannot resume {run_id}: row {case_id} config checksum mismatch"
                )
            if r.get("collection_name") != db["collection_name"]:
                raise ValueError(
                    f"cannot resume {run_id}: row {case_id} collection mismatch"
                )
            if r.get("embedding_provider") != embedding["provider"]:
                raise ValueError(
                    f"cannot resume {run_id}: row {case_id} embedding provider mismatch"
                )
            if r.get("embedding_model") != embedding["model"]:
                raise ValueError(
                    f"cannot resume {run_id}: row {case_id} embedding model mismatch"
                )
            if r.get("category") != case.category:
                raise ValueError(
                    f"cannot resume {run_id}: row {case_id} category mismatch"
                )
            if r.get("question") != case.question:
                raise ValueError(
                    f"cannot resume {run_id}: row {case_id} question mismatch"
                )
            if r.get("profile") != profile:
                raise ValueError(
                    f"cannot resume {run_id}: row {case_id} profile mismatch"
                )
            records[case_id] = r

        if records:
            done = len([r for r in records.values() if r.get("status") == "complete"])
            print_fn(f"[retrieval] resuming {run_id}: {done} complete rows, "
                     f"{len(records)} total")
        print_fn(
            f"[retrieval] run profile={profile} run={run_id} "
            f"collection={snapshot.collection_name} points={snapshot.point_count}"
        )
        breaker = CircuitBreaker()
        stopped = False
        cases = dataset.cases[:max_cases] if max_cases else dataset.cases
        for case in cases:
            existing = records.get(case.case_id)
            if existing is not None and existing.get("status") == "complete":
                continue
            if stopped:
                record = _failed_record(case, run_id, ts_display, dataset, snapshot,
                                        settings, setup_latency_ms, corpus_checksum,
                                        "not_run", "circuit_open")
            else:
                case_started = _time.monotonic()
                try:
                    documents = service.search(case.question)[:MAX_RETRIEVED_ITEMS]
                    case_metrics = metrics.case_metrics(
                        documents, case.relevant_sources, case.relevant_sections
                    )
                    case_metrics["keyword_coverage_at_5"] = metrics.keyword_coverage(
                        documents, case.keywords, 5
                    )
                    case_metrics["keyword_coverage_at_10"] = metrics.keyword_coverage(
                        documents, case.keywords, 10
                    )
                    record = build_retrieval_record(
                        run_id=run_id, timestamp_utc_plus_7=ts_display,
                        dataset_path=settings["evaluation"]["test_file"],
                        dataset_checksum=dataset.dataset_checksum,
                        corpus_checksum=corpus_checksum,
                        config_checksum=snapshot.config_fingerprint,
                        case_id=case.case_id, category=case.category,
                        question=case.question, profile=profile,
                        embedding_provider=embedding["provider"],
                        embedding_model=embedding["model"],
                        collection_name=db["collection_name"],
                        retrieved_items=[item_record(d) for d in documents],
                        metrics=case_metrics,
                        setup_latency_ms=setup_latency_ms,
                        latency_ms=round((_time.monotonic() - case_started) * 1000),
                    )
                except Exception as exc:
                    record = _failed_record(case, run_id, ts_display, dataset,
                                            snapshot, settings, setup_latency_ms,
                                            corpus_checksum, "error",
                                            type(exc).__name__)
            records[case.case_id] = record
            if not final.exists():
                artifacts.replace_partial(partial, list(records.values()))
            if not quiet:
                print_fn(
                    f"  {case.case_id} [{case.category}] status={record['status']} "
                    f"latency={record['latency_ms']}"
                    + (f" recall@5={record['metrics'].get('recall_at_5'):.3f}"
                       if record["metrics"] else "")
                )
            if not stopped:
                # record(False) resets the counter so only CONSECUTIVE
                # dependency failures can open the breaker.
                if breaker.record(record.get("status") != "complete"):
                    stopped = True
                    print_fn(
                        f"[retrieval] circuit breaker opened after 3 consecutive "
                        f"dependency failures; remaining cases marked not_run"
                    )
        effective = list(records.values())
        complete = (
            not max_cases
            and len(records) == len(cases)
            and all(r.get("status") == "complete" for r in effective)
        )
        if complete:
            if not final.exists():
                artifacts.replace_partial(partial, effective)
                check_records = artifacts.read_records(partial)
                if len(check_records) != len(cases) or len({r["case_id"] for r in check_records}) != len(cases):
                    raise ValueError(
                        f"final payload row count mismatch for {run_id}: expected {len(cases)}, got {len(check_records)}"
                    )
                if not all(r.get("status") == "complete" and r.get("run_id") == run_id for r in check_records):
                    raise ValueError(f"final payload contains incomplete or wrong-run rows for {run_id}")
                artifacts.finalize_run(partial, final)
            else:
                check_records = artifacts.read_records(final)
                if len(check_records) != len(cases) or len({r["case_id"] for r in check_records}) != len(cases):
                    raise ValueError(
                        f"final payload row count mismatch for {run_id}: expected {len(cases)}, got {len(check_records)}"
                    )
                if not all(r.get("status") == "complete" and r.get("run_id") == run_id for r in check_records):
                    raise ValueError(f"final payload contains incomplete or wrong-run rows for {run_id}")
        override = {"max_results": MAX_RETRIEVED_ITEMS, "concurrency": 1}
        if max_cases:
            override["cases"] = len(cases)
        payload = summarise_retrieval(
            effective, run_id, settings, snapshot, corpus_checksum, ts_display,
            override, results_dir,
            status="complete" if complete else "partial",
        )
        print_fn(
            f"[retrieval] {profile} {payload['status']}: "
            f"{payload['completed_case_count']}/{len(records)} complete, "
            f"Recall@5={payload['metrics']['overall']['recall_at_5']}"
            if payload["metrics"]["overall"].get("recall_at_5") is not None
            else f"[retrieval] {profile} {payload['status']}: "
            f"{payload['completed_case_count']}/{len(records)} complete"
        )
        summaries.append(payload)
    return summaries


def _failed_record(case, run_id, ts_display, dataset, snapshot, settings,
                   setup_latency_ms, corpus_checksum, status, error_type):
    """One failed/not_run retrieval row; identical checksum identity to a pass."""
    return build_retrieval_record(
        run_id=run_id, timestamp_utc_plus_7=ts_display,
        dataset_path=settings["evaluation"]["test_file"],
        dataset_checksum=dataset.dataset_checksum,
        corpus_checksum=corpus_checksum,
        config_checksum=snapshot.config_fingerprint,
        case_id=case.case_id, category=case.category,
        question=case.question, profile=snapshot.active_profile,
        embedding_provider=settings["embedding"]["provider"],
        embedding_model=settings["embedding"]["model"],
        collection_name=snapshot.collection_name,
        retrieved_items=[], metrics={},
        setup_latency_ms=setup_latency_ms, latency_ms=None,
        status=status, error_type=error_type,
    )
