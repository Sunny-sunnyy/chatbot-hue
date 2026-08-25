# Phase 4–5 Qdrant and Retrieval Simplicity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the unused stored sparse-vector path and layered retrieval machinery with one dense-only Qdrant candidate plus direct BM25 and MiniLM stages, while preserving and measuring all three canonical profiles on real Hue Foods data.

**Architecture:** Build deterministic dense `PointStruct` objects, ingest them through one uncached Qdrant client into an isolated blue-green candidate, and keep lexical BM25 in Python over dense candidates. Startup returns `RetrievalService` directly with a small immutable status; one concrete instance-owned CrossEncoder handles optional reranking. The active collection remains read-only and configuration remains unchanged until a separately approved cutover.

**Tech Stack:** Python 3.11+, uv, pytest, Qdrant/qdrant-client, sentence-transformers E5 and CrossEncoder, FastAPI, Jupyter nbconvert, YAML.

## Global Constraints

- Canonical corpus is exactly 572 chunks produced by `chunk_foods_markdown()`.
- Active collection `hue_foods_e5_small_384` is read-only throughout implementation and review.
- Fixed candidate name is `hue_foods_e5_small_384_dense`; ephemeral test collections must start with `hue_rag_live_test_`.
- Candidate schema is one named `dense` vector, size 384, cosine distance; it has no sparse vector configuration.
- Keep exactly `dense_only`, `hybrid_no_rerank`, and `hybrid_rerank` with their approved depths, weights and top-k values.
- Use real Qdrant, real E5, real MiniLM and canonical Hue Foods data as system evidence; mocks, fakes and fabricated output are forbidden.
- Tests protect user-needed behavior and important real failure only; there is no target test count.
- Before retaining an affected old test, write one plain sentence answering: “What user-needed behavior does this protect?” Delete it when there is no concrete answer or another retained test already protects the same behavior.
- Qdrant timeout remains 30 seconds, upsert batch size remains 64, startup payload scroll uses internal batch size 128.
- No manual upsert retry, app-level model/client cache, fingerprint, hot reload, compatibility wrapper, run registry or new dependency.
- Do not run paid generation or judge evaluation for this phase.
- Do not mutate `backend/config/settings.yaml` to point at the candidate before cutover approval.
- Do not delete the active collection or a rollback collection. Guarded test cleanup and the separately approved candidate creation/upsert are the only collection mutations in scope.
- Do not commit or push unless the user issues a separate explicit request.
- Preserve unrelated dirty-worktree changes; stage or edit only files listed by the active task.
- Canonical design: `docs/superpowers/specs/2026-08-25-phase-4-5-qdrant-retrieval-simplicity-design.md`.

---

## File Structure

### Create

- `backend/vectorstore/points.py`: deterministic UUID5, chunk/vector validation and dense `PointStruct` construction.
- `backend/reranking/cross_encoder.py`: the single concrete MiniLM reranker.
- `backend/evaluation/retrieval_comparison.py`: retrieval-only active/candidate evidence with per-query IDs, scores, latency and summaries.
- `reports/phase_4_5_active_retrieval_baseline.json`: fresh pre-refactor 104 × 3 active evidence.
- `reports/phase_4_5_dense_candidate_comparison.json`: post-refactor active/candidate comparison.
- `reports/phase_4_5_qdrant_retrieval_simplicity_implementation.md`: implementation and real-verification report.

### Modify

- `backend/config/settings.yaml`: remove reset/retry/scroll knobs only; keep active collection unchanged.
- `backend/vectorstore/qdrant.py`: uncached client and exact dense-only schema.
- `backend/vectorstore/upsert.py`: direct bounded upsert and pre-upsert identity scan.
- `backend/vectorstore/reset.py`: explicit exact-target CLI.
- `backend/ingestion/pipeline.py`: dense-only orchestration and optional exact candidate target.
- `backend/scoring/bm25.py`: own Unicode tokenization and all lexical statistics.
- `backend/core/startup.py`: direct service composition and small runtime status.
- `backend/retrieval/service.py`: direct component ownership; no `RetrievalStack`.
- `backend/api/app.py`: consume the service returned by startup.
- `backend/evaluation/eval.py`: optional exact collection target at evaluation composition root.
- `backend/tests/conftest.py`: uncached real client and dense-only guarded fixture.
- `backend/tests/test_ingestion_pipeline.py`: consolidated dense schema/point/ingestion/reset behavior.
- `backend/tests/test_bm25.py`: concise lexical behavior and fusion guards.
- `backend/tests/test_retrieval_service.py`: consolidated startup/profile/reranker behavior.
- `backend/tests/test_context_builder.py`: retain only distinct context contract tests.
- `backend/tests/test_api_chat.py`: dense-only collection helper and direct service startup expectations.
- `backend/tests/test_evaluation.py`: exact collection targeting and comparison-summary behavior.
- `notebooks/03_embedding_models.ipynb`: dense E5 lesson only.
- `notebooks/04_qdrant_ingestion.ipynb`: read-only candidate inspection.
- `notebooks/05_retrieval_profiles.ipynb`: real three-profile candidate queries.
- Phase 4/5/7/8 guides, `guides/README.md`, `session_prompt/Project_Status.md`: observed implementation state only after evidence exists.

### Delete after consumer audit

- `backend/vectorstore/hybrid_index.py`
- `backend/embedding/sparse_embedder.py`
- `backend/reranking/base.py`
- `backend/reranking/reranker.py`
- `backend/reranking/models/cross_encoder.py`
- `backend/reranking/models/__init__.py` if empty
- `backend/tests/test_hybrid_index.py`
- `backend/tests/test_sparse_embedder.py`
- `backend/tests/test_qdrant_schema.py`
- `backend/tests/test_reranker.py`
- `backend/tests/test_startup.py`

The listed test files are deletion candidates, not a mechanical deletion instruction. Each task first moves any still-required user behavior into the owning retained test file.

---

### Task 1: Capture the Fresh Active 104 × 3 Baseline

**Files:**
- Create: `backend/evaluation/retrieval_comparison.py`
- Modify: `backend/tests/test_evaluation.py`
- Create: `reports/phase_4_5_active_retrieval_baseline.json`

**Interfaces:**
- Consumes: `load_tests(path)`, `build_service(settings)`, `score_retrieval(keywords, texts)`.
- Produces: `run_collection_profiles(collection_name: str, profiles: tuple[str, ...], test_path: Path) -> dict` and a JSON document with per-query IDs/scores/latency/failures plus profile summaries.

- [ ] **Step 1: Record preflight state without mutation**

Run from `backend/`:

```bash
git status --short
docker compose ps
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -c 'from core.settings_loader import load_settings; from vectorstore.qdrant import client_from_settings; s=load_settings(); c=client_from_settings(s); n=s["vector_database"]["collection_name"]; print(n, c.count(n, exact=True).count, c.get_collection(n).config.params)'
```

Expected: dirty files are inventoried, Qdrant is reachable, and the active collection is `hue_foods_e5_small_384` with 572 points. Do not continue if the active name/count differs.

- [ ] **Step 2: Add one pure comparison-summary test**

Append to `backend/tests/test_evaluation.py`:

```python
from evaluation.retrieval_comparison import compare_profile_runs, summarize_profile


def test_retrieval_comparison_reports_latency_failures_and_rank_changes():
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
```

This is a small deterministic test of the report calculation, not evidence that retrieval works. The 104 × 3 real runs are the system evidence; do not add more synthetic comparison cases.

- [ ] **Step 3: Run RED**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run python -m pytest tests/test_evaluation.py::test_retrieval_comparison_reports_latency_failures_and_rank_changes -q --tb=short
```

Expected: FAIL because `evaluation.retrieval_comparison` does not exist.

- [ ] **Step 4: Implement the retrieval-only evidence runner**

Create `backend/evaluation/retrieval_comparison.py` with these concrete data rules:

```python
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
```

The implementation must not instantiate `OpenAIAnswerGenerator` or a judge.

- [ ] **Step 5: Run GREEN and then the fresh active baseline**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run python -m pytest tests/test_evaluation.py::test_retrieval_comparison_reports_latency_failures_and_rank_changes -q --tb=short
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -m evaluation.retrieval_comparison --collection hue_foods_e5_small_384 --tests ../knowledge-base-hue/foods/evaluation/tests.jsonl --output ../reports/phase_4_5_active_retrieval_baseline.json
```

Expected: the test passes; the JSON contains 104 rows for each profile, zero unexplained failures, real latency values and actual IDs/scores. This command is the final action before any runtime source edit.

- [ ] **Step 6: Review checkpoint**

Inspect the baseline file and report its summaries. Do not commit. Stop if any profile fails or if the output does not contain exactly 312 rows.

---

### Task 2: Move Lexical Ownership into BM25

**Files:**
- Modify: `backend/scoring/bm25.py`
- Modify: `backend/tests/test_bm25.py`

**Interfaces:**
- Produces: `tokenize(text: str) -> list[str]`, `BM25.fit(texts) -> BM25`, `BM25.score(query, document) -> float`, `min_max_normalize`, `validate_weights`.
- Preserves: `HybridRetriever` imports only BM25 normalization/weight helpers and observes identical approved lexical behavior.

- [ ] **Step 1: Write the Vietnamese tokenization behavior in the owning test**

Replace formula-detail duplication in `backend/tests/test_bm25.py` with the distinct public behavior below, retaining the existing known-corpus ranking, normalization and weight validation tests:

```python
from scoring.bm25 import BM25, min_max_normalize, tokenize, validate_weights


def test_tokenize_keeps_vietnamese_words_and_removes_punctuation():
    assert tokenize("Bún bò Huế, ngon! Giá 35.000đ.") == [
        "bún", "bò", "huế", "ngon", "giá", "35", "000đ"
    ]


def test_bm25_known_hue_corpus_ranking():
    corpus = ["bún bò huế", "cơm hến huế", "chè cung đình"]
    bm25 = BM25().fit(corpus)
    scores = [bm25.score("bún bò", text) for text in corpus]
    assert scores[0] > scores[1] == scores[2]
```

- [ ] **Step 2: Run RED after changing the import**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run python -m pytest tests/test_bm25.py -q --tb=short
```

Expected: FAIL because `scoring.bm25.tokenize` is not defined.

- [ ] **Step 3: Implement tokenizer directly in `scoring/bm25.py`**

Add the exact simple tokenizer used by the current sparse module:

```python
import re

TOKEN_PATTERN = re.compile(r"\w+", flags=re.UNICODE)


def tokenize(text: str) -> list[str]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return TOKEN_PATTERN.findall(text.lower())
```

Remove `from embedding.sparse_embedder import tokenize`. Do not change `K1=1.5`, `B=0.75`, IDF, query-term deduplication, normalization or fusion weights.

- [ ] **Step 4: Prove no sparse consumer remains, then delete it**

Run:

```bash
rg -n "SparseEmbedder|embedding\.sparse_embedder|from embedding.sparse_embedder" backend notebooks guides --glob '!docs/superpowers/**'
```

Expected before later ingestion edits: remaining matches are isolated to ingestion/tests/notebook 03. Do not delete the module yet if a runtime consumer remains. After Task 4 removes those consumers, rerun the command; then delete `backend/embedding/sparse_embedder.py` and `backend/tests/test_sparse_embedder.py` in Task 4's final cleanup.

- [ ] **Step 5: Run the focused lexical tests**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run python -m pytest tests/test_bm25.py -q --tb=short
```

Expected: all retained BM25 tests pass and remain readable as user behavior.

---

### Task 3: Build Dense-Only PointStruct Objects

**Files:**
- Create: `backend/vectorstore/points.py`
- Modify: `backend/tests/test_ingestion_pipeline.py`

**Interfaces:**
- Produces: `point_id_for(chunk_id: str) -> UUID`, `validate_chunks(chunks) -> list[str]`, `build_points(chunks, dense, model_id, dimension) -> list[models.PointStruct]`.
- Consumed by: the ingestion/upsert conversion in Task 4 and real tests.

- [ ] **Step 1: Add the dense point contract**

Move this assertion into `backend/tests/test_ingestion_pipeline.py`:

```python
def test_dense_point_contract_uses_uuid5_and_model_identity(real_chunks, real_embedder):
    chunk = real_chunks[0]
    dense = real_embedder.embed_documents([chunk["text"]])
    point = build_points([chunk], dense, MODEL_ID, DIMENSION)[0]
    assert point.id == point_id_for(chunk["metadata"]["chunk_id"])
    assert set(point.vector) == {"dense"}
    assert len(point.vector["dense"]) == 384
    assert point.payload["embedding_model"] == MODEL_ID
    assert "embedding_dimension" not in point.payload
```

- [ ] **Step 2: Run RED**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_ingestion_pipeline.py -q --tb=short -k dense_point_contract
```

Expected: FAIL because `vectorstore.points` does not exist.

- [ ] **Step 3: Implement `vectorstore/points.py`**

Use direct Qdrant objects; validate counts before `zip`:

```python
import math
import uuid

from qdrant_client import models

POINT_ID_NAMESPACE = uuid.NAMESPACE_URL


def point_id_for(chunk_id: str):
    return uuid.uuid5(POINT_ID_NAMESPACE, f"hue-rag:{chunk_id}")


def validate_chunks(chunks):
    if not chunks:
        raise ValueError("no chunks to index")
    chunk_ids = []
    for chunk in chunks:
        chunk_id = (chunk.get("metadata") or {}).get("chunk_id")
        if not isinstance(chunk_id, str) or not chunk_id:
            raise ValueError("chunk missing a non-empty metadata.chunk_id")
        if chunk_id in chunk_ids:
            raise ValueError(f"duplicate chunk_id: {chunk_id}")
        chunk_ids.append(chunk_id)
    return chunk_ids


def build_points(chunks, dense, model_id, dimension):
    chunk_ids = validate_chunks(chunks)
    if len(dense) != len(chunk_ids):
        raise ValueError(f"dense vector count {len(dense)} != chunk count {len(chunk_ids)}")
    points = []
    for chunk, chunk_id, vector in zip(chunks, chunk_ids, dense):
        if len(vector) != dimension:
            raise ValueError(f"dense dimension {len(vector)} != expected {dimension}")
        if not all(math.isfinite(float(value)) for value in vector):
            raise ValueError("dense vector contains non-finite values")
        metadata = chunk["metadata"]
        points.append(models.PointStruct(
            id=point_id_for(chunk_id),
            vector={"dense": vector},
            payload={
                "text": chunk["text"],
                "chunk_id": chunk_id,
                "source": metadata["source"],
                "title": metadata["title"],
                "section": metadata["section"],
                "category": metadata["category"],
                "subcategory": metadata["subcategory"],
                "chunk_type": metadata["chunk_type"],
                "embedding_model": model_id,
            },
        ))
    return points
```

Use a `seen` set in the final implementation so duplicate validation remains linear while preserving the shown behavior and errors.

- [ ] **Step 4: Run the dense point slice**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_ingestion_pipeline.py -q --tb=short -k dense_point_contract
```

Expected: the new point test passes without Qdrant mutation.

---

### Task 4: Simplify Upsert, Pipeline, Candidate Targeting and Reset

**Files:**
- Modify: `backend/vectorstore/qdrant.py`
- Modify: `backend/vectorstore/upsert.py`
- Modify: `backend/vectorstore/reset.py`
- Modify: `backend/ingestion/pipeline.py`
- Modify: `backend/config/settings.yaml`
- Modify: `backend/tests/test_api_chat.py`
- Modify: `backend/tests/test_ingestion_pipeline.py`
- Modify: `backend/tests/conftest.py`
- Delete: `backend/embedding/sparse_embedder.py`
- Delete: `backend/tests/test_sparse_embedder.py`
- Delete: `backend/vectorstore/hybrid_index.py`
- Delete: `backend/tests/test_hybrid_index.py`
- Delete: `backend/tests/test_qdrant_schema.py`

**Interfaces:**
- Produces: `run_ingestion(settings=None, *, collection_name=None, chunker=None, embedder=None, client=None) -> dict`.
- Produces: `client_from_settings(settings) -> QdrantClient`, `expected_schema(settings) -> dict[str, VectorParams]`, `ensure_collection(client, settings) -> str`.
- Produces: `upsert_points(client, settings, points) -> int`, `validate_existing_points(client, settings, expected_points, model_id)`, `verify_point_count`.
- Produces: `reset_collection(client, settings, *, collection_name, confirmation) -> tuple[str, int]` and CLI `--collection/--confirm`.

- [ ] **Step 1: Rewrite retained ingestion tests around real behavior**

Keep these distinct cases in `test_ingestion_pipeline.py` and remove retry/cache/schema-permutation cases:

```python
def test_ingestion_idempotent_rerun_on_real_dense_collection(
    ingested_collection, real_client, real_embedder
):
    first_count = real_client.count(TEST_COLLECTION, exact=True).count
    summary = run_ingestion(
        make_test_settings(TEST_COLLECTION),
        embedder=real_embedder,
        client=real_client,
    )
    assert first_count == summary["point_count"] == CANONICAL_CHUNK_COUNT


def test_ingestion_rejects_existing_model_mismatch_before_mutation(
    real_client, real_embedder, real_chunks
):
    name = "hue_rag_live_test_model_mismatch"
    settings = make_test_settings(name)
    ensure_collection(real_client, settings)
    point = build_points(
        real_chunks[:1],
        real_embedder.embed_documents([real_chunks[0]["text"]]),
        MODEL_ID,
        DIMENSION,
    )[0]
    point.payload["embedding_model"] = "other/model"
    real_client.upsert(name, points=[point], wait=True)
    try:
        with pytest.raises(ValueError, match="embedding_model"):
            run_ingestion(settings, embedder=real_embedder, client=real_client)
        assert real_client.count(name, exact=True).count == 1
    finally:
        cleanup_collection(real_client, name)


def test_reset_deletes_only_exact_guarded_target_and_reports_count(real_client):
    name = "hue_rag_live_test_reset_exact"
    settings = make_test_settings(name)
    ensure_collection(real_client, settings)
    deleted_name, count = reset_collection(
        real_client,
        settings,
        collection_name=name,
        confirmation=f"DELETE {name}",
    )
    assert (deleted_name, count) == (name, 0)
    assert not real_client.collection_exists(name)


def test_reset_rejects_confirmation_mismatch_without_deleting(real_client):
    name = "hue_rag_live_test_reset_confirmation"
    settings = make_test_settings(name)
    ensure_collection(real_client, settings)
    try:
        with pytest.raises(ValueError, match="confirmation"):
            reset_collection(
                real_client,
                settings,
                collection_name=name,
                confirmation=f"DELETE {name} extra",
            )
        assert real_client.collection_exists(name)
    finally:
        cleanup_collection(real_client, name)
```

Keep the existing foreign-point test after converting its point to dense-only. The reset tests must not use active or candidate names.

Add the real dense-only schema behavior:

```python
def test_live_dense_schema_has_no_sparse_vectors(real_client):
    name = "hue_rag_live_test_dense_schema"
    settings = make_test_settings(name)
    try:
        assert ensure_collection(real_client, settings) == "created"
        info = real_client.get_collection(name)
        assert set(info.config.params.vectors) == {"dense"}
        assert not info.config.params.sparse_vectors
    finally:
        cleanup_collection(real_client, name)
```

- [ ] **Step 2: Run RED for the new signatures and dense-only pipeline**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_ingestion_pipeline.py -q --tb=short
```

Expected: failures mention obsolete sparse inputs, reset arguments, retry settings or point dict conversion.

- [ ] **Step 3: Make `qdrant.py` dense-only and uncached**

Remove `lru_cache`, `get_client`, `SPARSE_VECTOR_NAME` and sparse validation. Use:

```python
def client_from_settings(settings=None):
    settings = load_settings() if settings is None else settings
    db = settings["vector_database"]
    return QdrantClient(url=db["url"], timeout=db["timeout"])


def expected_schema(settings):
    dimension = settings["vector_database"]["vector_size"]
    return {DENSE_VECTOR_NAME: models.VectorParams(size=dimension, distance=DISTANCE)}


def ensure_collection(client, settings):
    db = settings["vector_database"]
    name = db["collection_name"]
    if client.collection_exists(name):
        validate_collection_info(client.get_collection(name), settings)
        return "existing"
    client.create_collection(
        name,
        vectors_config=expected_schema(settings),
        timeout=db["timeout"],
    )
    return "created"
```

`validate_collection_info` must require exactly one named dense vector and no sparse vectors. In `conftest.py`, replace `get_client` with `client_from_settings`; in `test_api_chat.py`, create guarded collections with `vectors_config=expected_schema(settings)` and no sparse config.

- [ ] **Step 4: Make upsert direct and fail-explicit**

Delete `httpx`, `TRANSIENT_ERRORS`, `to_point_struct`, `upsert_batch` and `max_retries`. The write loop must be:

```python
def upsert_points(client, settings, points):
    db = settings["vector_database"]
    name = db["collection_name"]
    completed = 0
    for start in range(0, len(points), db["upsert_batch_size"]):
        batch = points[start:start + db["upsert_batch_size"]]
        try:
            client.upsert(name, points=batch, wait=True, timeout=db["timeout"])
        except Exception:
            logger.exception(
                "upsert failed after %d/%d points completed; rerun is idempotent",
                completed,
                len(points),
            )
            raise
        completed += len(batch)
    return completed
```

`validate_existing_points` must map `str(point.id)` to the expected `PointStruct`, compare `record.id`, `payload.chunk_id` and `payload.embedding_model`, and must not inspect `embedding_dimension`.

- [ ] **Step 5: Make ingestion dense-only with an exact optional target**

At the composition root:

```python
import copy


def run_ingestion(settings=None, *, collection_name=None, chunker=None, embedder=None, client=None):
    settings = copy.deepcopy(load_settings() if settings is None else settings)
    if collection_name is not None:
        if not isinstance(collection_name, str) or not collection_name.strip():
            raise ValueError("collection_name must be a non-empty exact name")
        settings["vector_database"]["collection_name"] = collection_name
    chunks = chunk_foods_markdown() if chunker is None else chunker()
    chunk_ids = validate_chunks(chunks)
    if len(chunk_ids) != CANONICAL_CHUNK_COUNT:
        raise ValueError(
            f"chunk count {len(chunk_ids)} != canonical {CANONICAL_CHUNK_COUNT}; "
            "report the corpus/chunking input diff instead of reindexing"
        )
    texts = [chunk["text"] for chunk in chunks]
    dense_embedder = embedder if embedder is not None else _build_embedder(settings)
    dense = dense_embedder.embed_documents(texts)
    points = build_points(chunks, dense, settings["embedding"]["model"], settings["vector_database"]["vector_size"])
    client = client_from_settings(settings) if client is None else client
    ensure_collection(client, settings)
    validate_existing_points(client, settings, points, settings["embedding"]["model"])
    upsert_points(client, settings, points)
    validate_collection_info(client.get_collection(settings["vector_database"]["collection_name"]), settings)
    actual = verify_point_count(client, settings, CANONICAL_CHUNK_COUNT)
    return {
        "collection_name": settings["vector_database"]["collection_name"],
        "embedding_model": settings["embedding"]["model"],
        "embedding_dimension": settings["vector_database"]["vector_size"],
        "chunk_count": CANONICAL_CHUNK_COUNT,
        "point_count": actual,
    }
```

Delete `_reject_reset` and every sparse import/call.

- [ ] **Step 6: Implement exact-target reset**

Use this contract:

```python
def reset_collection(client, settings, *, collection_name, confirmation):
    if confirmation != f"DELETE {collection_name}":
        raise ValueError(f"confirmation mismatch; expected 'DELETE {collection_name}'")
    if not client.collection_exists(collection_name):
        raise ValueError(f"collection {collection_name} does not exist; nothing to reset")
    count = client.count(collection_name, exact=True).count
    print(f"collection {collection_name} currently has {count} points")
    client.delete_collection(collection_name, timeout=settings["vector_database"]["timeout"])
    if client.collection_exists(collection_name):
        raise RuntimeError(f"collection {collection_name} still exists after delete")
    return collection_name, count
```

CLI arguments are exactly `--collection` and `--confirm`. Do not validate schema, model, payload or expected count.

- [ ] **Step 7: Remove obsolete configuration and modules**

Delete from `backend/config/settings.yaml`:

```yaml
reset_collection: false
upsert_max_retries: 1
```

After this consumer audit returns no runtime hits, delete sparse/hybrid modules and their test files:

```bash
rg -n "SparseEmbedder|sparse_embedder|hybrid_index|SPARSE_VECTOR_NAME|upsert_max_retries|reset_collection|scroll_batch_size" backend notebooks --glob '*.py' --glob '*.ipynb'
```

Expected remaining matches at this point: notebook 03 content and possibly startup's `scroll_batch_size`, both handled in later tasks; no ingestion/vectorstore runtime consumer remains.

- [ ] **Step 8: Run focused real ingestion verification**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_ingestion_pipeline.py -q --tb=short -s
```

Expected: dense-only real 572-point ingestion, idempotent rerun, foreign/model guard and exact guarded reset pass. Cleanup reports no `hue_rag_live_test_` leftovers.

---

### Task 5: Replace the Reranker Layers with One Concrete Class

**Files:**
- Create: `backend/reranking/cross_encoder.py`
- Modify: `backend/tests/test_retrieval_service.py`
- Delete: `backend/tests/test_reranker.py`

**Interfaces:**
- Produces: `CrossEncoderReranker(model_id: str, device: str)`, `.model_id`, `.load()`, `.warm_up() -> float`, `.rerank(query, documents, top_k) -> list[RetrievedDocument]`.
- Consumed by: `core.startup.build_retrieval_service` only for `hybrid_rerank`.

- [ ] **Step 1: Move the meaningful real reranker behavior into service tests**

Add one consolidated test to `test_retrieval_service.py` that uses real retrieved documents and real MiniLM, asserts top-k, finite descending scores, `reranker_model` and non-mutation. Keep score-count/finite validation in production code to prevent silent truncation or invalid ranking, but do not add a private-helper or fabricated-model-output test. Deterministic ordering is verified by repeated real profile search in Task 6.

The key public assertions are:

```python
before = copy.deepcopy([(d.id, d.score, d.text, d.metadata) for d in documents])
result = reranker.rerank("bún bò Huế", documents, top_k=3)
assert len(result) == 3
assert all(math.isfinite(doc.score) for doc in result)
assert [doc.score for doc in result] == sorted((doc.score for doc in result), reverse=True)
assert all(doc.metadata["reranker_model"] == MINILM_ID for doc in result)
assert [(d.id, d.score, d.text, d.metadata) for d in documents] == before
```

- [ ] **Step 2: Run RED after importing the new module**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_retrieval_service.py -q --tb=short -k rerank
```

Expected: FAIL because `reranking.cross_encoder` does not exist.

- [ ] **Step 3: Implement the concrete instance-owned reranker**

Create `backend/reranking/cross_encoder.py` with no inheritance and no cache:

```python
import math

from core.schema import ComponentNotReadyError, RetrievedDocument, RetrievalDependencyError

WARMUP_QUERY = "món ăn Huế"
WARMUP_DOCUMENT = "Bún bò Huế là một món ăn nổi tiếng của Huế."


class CrossEncoderReranker:
    def __init__(self, model_id="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu"):
        self._model_id = model_id
        self._device = device
        self._model = None

    @property
    def model_id(self):
        return self._model_id

    def load(self):
        if self._model is None:
            try:
                from sentence_transformers import CrossEncoder
                self._model = CrossEncoder(self._model_id, device=self._device)
            except Exception as exc:
                raise ComponentNotReadyError("reranker model load failed") from exc
        return self

    def _predict(self, pairs):
        try:
            raw = self.load()._model.predict(pairs, show_progress_bar=False)
            return list(raw.tolist() if hasattr(raw, "tolist") else raw)
        except ComponentNotReadyError:
            raise
        except Exception as exc:
            raise RetrievalDependencyError("reranker scoring failed") from exc

    @staticmethod
    def _finite_scores(scores, expected_count):
        if len(scores) != expected_count:
            raise RetrievalDependencyError(
                f"reranker returned {len(scores)} scores for {expected_count} documents"
            )
        converted = []
        for score in scores:
            try:
                value = float(score)
            except (TypeError, ValueError) as exc:
                raise RetrievalDependencyError("reranker returned a non-numeric score") from exc
            if not math.isfinite(value):
                raise RetrievalDependencyError("reranker returned a non-finite score")
            converted.append(value)
        return converted

    def warm_up(self):
        try:
            return self._finite_scores(self._predict([(WARMUP_QUERY, WARMUP_DOCUMENT)]), 1)[0]
        except Exception as exc:
            if isinstance(exc, ComponentNotReadyError):
                raise
            raise ComponentNotReadyError("reranker warm-up prediction failed") from exc

    def rerank(self, query, documents, top_k):
        if not documents:
            return []
        if top_k <= 0:
            raise ValueError("top_k must be positive")
        chunk_ids = [doc.metadata.get("chunk_id") for doc in documents]
        if any(not isinstance(value, str) or not value for value in chunk_ids):
            raise RetrievalDependencyError("reranker input document has an invalid chunk_id")
        if len(chunk_ids) != len(set(chunk_ids)):
            raise RetrievalDependencyError("reranker input contains duplicate chunk_id")
        scores = self._finite_scores(
            self._predict([(query, doc.text) for doc in documents]), len(documents)
        )
        ranked = sorted(zip(scores, documents), key=lambda item: (-item[0], item[1].metadata["chunk_id"]))
        return [
            RetrievedDocument(
                id=doc.id,
                score=score,
                text=doc.text,
                metadata={**doc.metadata, "reranker_model": self._model_id, "rerank_score": score},
            )
            for score, doc in ranked[:top_k]
        ]
```

- [ ] **Step 4: Audit old wrapper consumers before Task 6**

Run:

```bash
rg -n "reranking\.base|reranking\.reranker|reranking\.models|BaseReranker|ScorerReranker" backend --glob '*.py'
```

Expected: startup is the only runtime consumer of the old wrapper path. Delete `test_reranker.py` after its required public behaviors are present in `test_retrieval_service.py`; Task 6 updates startup and deletes the old modules without re-export shims.

- [ ] **Step 5: Run real reranker slice**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_retrieval_service.py -q --tb=short -s -k rerank
```

Expected: real MiniLM loads/downloads through the library's normal path, warm-up and reranking pass, and input documents remain unchanged.

---

### Task 6: Return RetrievalService Directly from Startup

**Files:**
- Modify: `backend/core/startup.py`
- Modify: `backend/retrieval/service.py`
- Modify: `backend/api/app.py`
- Modify: `backend/evaluation/eval.py`
- Modify: `backend/config/settings.yaml`
- Modify: `backend/tests/test_retrieval_service.py`
- Modify: `backend/tests/test_api_chat.py`
- Modify: `backend/tests/test_evaluation.py`
- Delete: `backend/reranking/base.py`
- Delete: `backend/reranking/reranker.py`
- Delete: `backend/reranking/models/cross_encoder.py`
- Delete: `backend/reranking/models/__init__.py` if empty
- Delete: `backend/tests/test_startup.py`

**Interfaces:**
- Produces: immutable `RetrievalStatus(collection_name, point_count, embedding_model, embedding_dimension, active_profile, bm25_ready, reranker_ready)`.
- Produces: `build_retrieval_service(settings=None, *, client=None, embedder=None) -> RetrievalService`.
- Produces: `RetrievalService(status, dense_retriever, hybrid_retriever=None, reranker=None, rerank_top_k=5)`.
- Preserves: `service.status`, `service.snapshot` only if existing API consumers require a temporary rename within the same task; final public property is `status`.

- [ ] **Step 1: Rewrite service tests to describe only constructible profiles**

Replace `RetrievalStack`/missing-optional-component tests with real startup assertions:

```python
def make_live_service(profile, real_client, real_embedder):
    settings = make_test_settings(TEST_COLLECTION, **{"active_profile": profile})
    return build_retrieval_service(settings, client=real_client, embedder=real_embedder)


def test_dense_only_builds_only_required_runtime(
    ingested_collection, real_client, real_embedder
):
    service = make_live_service("dense_only", real_client, real_embedder)
    assert service.status.active_profile == "dense_only"
    assert service.status.bm25_ready is False
    assert service.status.reranker_ready is False
    documents = service.search("bún bò Huế")
    assert documents
    assert all("bm25_score" not in doc.metadata for doc in documents)


def test_hybrid_no_rerank_runs_dense_then_python_bm25(
    ingested_collection, real_client, real_embedder
):
    service = make_live_service("hybrid_no_rerank", real_client, real_embedder)
    documents = service.search("bún bò Huế")
    assert service.status.bm25_ready is True
    assert service.status.reranker_ready is False
    assert documents
    assert all("bm25_score" in doc.metadata for doc in documents)
    assert all("rerank_score" not in doc.metadata for doc in documents)


def test_hybrid_rerank_runs_dense_bm25_then_real_minilm(
    ingested_collection, real_client, real_embedder
):
    service = make_live_service("hybrid_rerank", real_client, real_embedder)
    documents = service.search("bún bò Huế")
    assert service.status.bm25_ready is True
    assert service.status.reranker_ready is True
    assert 1 <= len(documents) <= 5
    assert all("hybrid_score" in doc.metadata for doc in documents)
    assert all(doc.metadata["reranker_model"] == MINILM_ID for doc in documents)


def test_repeated_real_search_is_deterministic(
    ingested_collection, real_client, real_embedder
):
    service = make_live_service("dense_only", real_client, real_embedder)
    first = service.search("bún bò Huế")
    second = service.search("bún bò Huế")
    assert [(doc.id, doc.score) for doc in first] == [
        (doc.id, doc.score) for doc in second
    ]
```

Do not add another service-level dead-Qdrant test. Retain the real API behavior that returns retrieval-not-ready/503 when Qdrant is unavailable or the collection disappears; that is the user-visible failure contract.

Delete fingerprint, scroll override, injected invalid stack and missing-cache tests.

- [ ] **Step 2: Run RED**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_retrieval_service.py -q --tb=short
```

Expected: FAIL because `build_retrieval_service` and `.status` do not exist.

- [ ] **Step 3: Simplify `RetrievalService` ownership**

Use a direct constructor and preserve routing:

```python
class RetrievalService:
    def __init__(
        self,
        status,
        dense_retriever,
        hybrid_retriever=None,
        reranker=None,
        rerank_top_k=5,
    ):
        self._status = status
        self._dense = dense_retriever
        self._hybrid = hybrid_retriever
        self._reranker = reranker
        self._rerank_top_k = rerank_top_k

    @property
    def status(self):
        return self._status

    @property
    def active_profile(self):
        return self._status.active_profile
```

`search()` must use `_dense`, `_hybrid`, `_reranker`; retain input validation, fresh output documents, `retrieval_profile` and `retrieval_rank`. Delete `PROFILE_REQUIREMENTS`, `RetrievalStack` validation and the import cycle from service to startup. Keep `build_service()` as the public convenience wrapper used by API/evaluation/notebooks:

```python
def build_service(settings=None, **kwargs):
    from core.startup import build_retrieval_service
    return build_retrieval_service(settings, **kwargs)
```

- [ ] **Step 4: Rewrite startup as direct composition**

Keep `_query_embedder`, `_warm_embedder`, `_verify_collection`, `_verify_config_consistency`, `_scroll_all_payloads` and `_corpus_pairs`, but remove `hashlib`, `json`, fingerprints, `RetrievalStack`, `verify_snapshot`, injected reranker and scroll override.

Define:

```python
@dataclass(frozen=True)
class RetrievalStatus:
    collection_name: str
    point_count: int
    embedding_model: str
    embedding_dimension: int
    active_profile: str
    bm25_ready: bool
    reranker_ready: bool


def _scroll_all_payloads(client, collection_name, timeout):
    records = []
    offset = None
    while True:
        batch, offset = client.scroll(
            collection_name,
            limit=128,
            offset=offset,
            with_payload=["chunk_id", "text", "embedding_model"],
            with_vectors=False,
            timeout=timeout,
        )
        records.extend(batch)
        if offset is None:
            return records
```

`_corpus_pairs` validates `chunk_id`, non-empty `text`, and `embedding_model`; it does not read payload dimension. `build_retrieval_service` validates the profile, builds/warms E5, always builds dense retrieval, scrolls/fits BM25 only for hybrid profiles, and loads/warms `CrossEncoderReranker` only for `hybrid_rerank`. It returns `RetrievalService(status, dense_retriever, hybrid_retriever, reranker_instance, reranking["top_k"])`.

Delete `vector_database.scroll_batch_size` from `backend/config/settings.yaml`; the only pagination value is the internal `limit=128` shown above.

- [ ] **Step 5: Update API and evaluation composition roots**

In `api/app.py`, replace stack construction with:

```python
retrieval_service = build_retrieval_service(settings)
retrieval_ready = True
```

Read runtime fields from `retrieval_service.status`. In `evaluation/eval.py`, change:

```python
def build_services(profile="dense_only", collection_name=None):
    settings = copy.deepcopy(load_settings())
    settings["active_profile"] = profile
    if collection_name is not None:
        settings["vector_database"]["collection_name"] = collection_name
    retrieval = build_service(settings)
    context = ContextBuilder(
        max_documents=settings["retrieval"]["max_context_documents"],
        max_characters=settings["retrieval"]["max_context_characters"],
    )
    generator = OpenAIAnswerGenerator(
        model=settings["llm"]["answer_model"],
        temperature=settings["llm"]["temperature"],
        max_output_tokens=settings["llm"]["max_output_tokens"],
        timeout_seconds=settings["llm"]["timeout"],
    )
    judge_model = settings["evaluation"]["judge_model"]
    return EvaluationServices(
        retrieval,
        context,
        generator,
        build_judge(judge_model),
        judge_model,
    )
```

Do not add environment variables, extra YAML files or global settings mutation.

- [ ] **Step 6: Delete startup tests only after behavior migration**

Move into `test_retrieval_service.py` the real behaviors still needed: exact 572 count, dense schema validation, E5 warm-up, unique/non-empty/model-matching hybrid payloads and profile-scoped MiniLM load. Move API runtime debug assertions into `test_api_chat.py`. Then delete `test_startup.py`.

- [ ] **Step 7: Run affected real runtime tests**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_retrieval_service.py tests/test_api_chat.py tests/test_evaluation.py -q --tb=short -s -k 'not TestChatSuccess and not test_answer_evaluation_calls_real_generation_and_judge_models and not test_no_sensitive_payload_in_responses'
```

Expected: all three real retrieval profiles pass; API startup/debug stays truthful; pytest reports the explicitly deselected paid tests and no paid generation/judge call runs.

---

### Task 7: Preserve the Context Contract and Remove Duplicate Tests

**Files:**
- Modify: `backend/tests/test_context_builder.py`
- Modify: `backend/tests/test_llm_generator_openai.py` only if the `rg` audit finds a test that merely duplicates ContextBuilder behavior

**Interfaces:**
- Preserves: `ContextBuilder(max_documents=5, max_characters=3000).build(documents) -> ContextResult`.
- Preserves: JSON structural separation, source mapping, whole chunks, input order and non-mutation.

- [ ] **Step 1: Audit each context test by user behavior**

Run:

```bash
rg -n "ContextBuilder|context_json|max_context|whole.chunk|source mapping" backend/tests
```

Retain one clear test for each: whole-chunk budget/document cap, JSON injection safety/source mapping, empty input and non-mutation. Remove arithmetic duplicates and generator tests that merely repeat the same builder behavior.

- [ ] **Step 2: Run the retained contract**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run python -m pytest tests/test_context_builder.py -q --tb=short
```

Expected: retained tests pass without runtime code changes. If a removed test exposed distinct user behavior, restore that behavior as one readable test before proceeding.

---

### Task 8: Rewrite Notebooks 03–05 Around the Final Public APIs

**Files:**
- Modify: `notebooks/03_embedding_models.ipynb`
- Modify: `notebooks/04_qdrant_ingestion.ipynb`
- Modify: `notebooks/05_retrieval_profiles.ipynb`

**Interfaces:**
- Notebook 03 calls `chunk_foods_markdown` and `E5Embedder` only.
- Notebook 04 uses `client_from_settings`, exact candidate name and read-only Qdrant calls only.
- Notebook 05 uses `build_service(settings)` for each exact profile against the candidate.

- [ ] **Step 1: Rewrite Notebook 03 as dense E5 only**

Keep code equivalent to:

```python
chunks = chunk_foods_markdown()
texts = [chunk["text"] for chunk in chunks]
embedder = E5Embedder(model_id="intfloat/multilingual-e5-small", dimension=384, device="cpu", batch_size=64)
vectors = embedder.embed_documents(texts)
print(len(vectors), len(vectors[0]))
print(np.linalg.norm(vectors[0]))
```

Remove every sparse import, TF-IDF explanation and sparse output.

- [ ] **Step 2: Rewrite Notebook 04 as read-only candidate inspection**

The only Qdrant calls are `collection_exists`, `get_collection`, `count` and `scroll` against `hue_foods_e5_small_384_dense`. Assert count 572, one named dense vector of size 384/cosine, no sparse vectors, and show only safe payload fields. No create/upsert/reset/delete cell is allowed.

- [ ] **Step 3: Rewrite Notebook 05 for three real profiles**

For each profile, deep-copy settings, set `active_profile` and exact candidate collection in memory, call `build_service(settings)`, then show IDs and dense/BM25/rerank metadata for representative Hue queries. Explain that BM25 reranks dense candidates and that this is not native Qdrant sparse retrieval. Do not declare a winner.

- [ ] **Step 4: Clear repository outputs and execution counts**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace notebooks/03_embedding_models.ipynb notebooks/04_qdrant_ingestion.ipynb notebooks/05_retrieval_profiles.ipynb
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run python -c 'import json; from pathlib import Path; paths=[Path("notebooks/03_embedding_models.ipynb"),Path("notebooks/04_qdrant_ingestion.ipynb"),Path("notebooks/05_retrieval_profiles.ipynb")]; assert all(cell.get("execution_count") is None and not cell.get("outputs", []) for path in paths for cell in json.loads(path.read_text())["cells"] if cell["cell_type"]=="code"); print("notebook outputs clean")'
```

Expected: `notebook outputs clean`.

Do not run Notebook 04/05 until the candidate exists in Task 9.

---

### Task 9: Create the Candidate and Run Final Real Verification

**Files:**
- Create: `reports/phase_4_5_dense_candidate_comparison.json`
- Create: `reports/phase_4_5_qdrant_retrieval_simplicity_implementation.md`
- Modify: guides/status documents with observed results only

**Interfaces:**
- Consumes: final `run_ingestion(..., collection_name=...)`, `retrieval_comparison`, notebooks and tests.
- Produces: verified dense-only 572-point candidate and reviewer-ready evidence; no cutover.

- [ ] **Step 1: Verify mutation targets immediately before candidate creation**

Run from `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -c 'from core.settings_loader import load_settings; from vectorstore.qdrant import client_from_settings; s=load_settings(); c=client_from_settings(s); active=s["vector_database"]["collection_name"]; candidate="hue_foods_e5_small_384_dense"; print("active", active, c.count(active, exact=True).count); print("candidate_exists", c.collection_exists(candidate))'
```

Expected: active is unchanged at 572. If candidate already exists, inspect schema/count/payload before deciding whether idempotent rerun is safe; never delete it implicitly.

- [ ] **Step 2: Create or idempotently ingest the fixed candidate**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -c 'from ingestion.pipeline import run_ingestion; print(run_ingestion(collection_name="hue_foods_e5_small_384_dense"))'
```

Expected: summary reports exact candidate name, E5 model, dimension 384, 572 chunks and 572 points. Run the same command a second time and require the same count.

- [ ] **Step 3: Verify active safety and candidate payload/schema**

Run from `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -c 'from core.settings_loader import load_settings; from vectorstore.qdrant import client_from_settings; s=load_settings(); c=client_from_settings(s); a="hue_foods_e5_small_384"; n="hue_foods_e5_small_384_dense"; info=c.get_collection(n); rows,_=c.scroll(n,limit=20,with_payload=True,with_vectors=False); print("counts",c.count(a,exact=True).count,c.count(n,exact=True).count); print("vectors",info.config.params.vectors,"sparse",info.config.params.sparse_vectors); print("payload_dimension_present",any("embedding_dimension" in (row.payload or {}) for row in rows))'
```

Expected: active 572, candidate 572, one dense 384/cosine vector, no sparse config, and `payload_dimension_present False`.

- [ ] **Step 4: Run the four retained focused test files**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_ingestion_pipeline.py tests/test_bm25.py tests/test_retrieval_service.py tests/test_context_builder.py -q --tb=short -s
```

Expected: all pass with real Qdrant/E5/MiniLM evidence and reported guarded cleanup.

- [ ] **Step 5: Run Notebook 03–05 temporary copies**

Run from repository root:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file .env jupyter nbconvert --execute --to notebook notebooks/03_embedding_models.ipynb --output /tmp/03_embedding_models-phase45-live.ipynb --ExecutePreprocessor.timeout=900
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file .env jupyter nbconvert --execute --to notebook notebooks/04_qdrant_ingestion.ipynb --output /tmp/04_qdrant_ingestion-phase45-live.ipynb --ExecutePreprocessor.timeout=900
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file .env jupyter nbconvert --execute --to notebook notebooks/05_retrieval_profiles.ipynb --output /tmp/05_retrieval_profiles-phase45-live.ipynb --ExecutePreprocessor.timeout=1800
```

Expected: all Run All commands succeed against real data/services; repository notebook outputs remain empty.

- [ ] **Step 6: Run the candidate 104 × 3 comparison**

Run from `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -m evaluation.retrieval_comparison --collection hue_foods_e5_small_384_dense --tests ../knowledge-base-hue/foods/evaluation/tests.jsonl --baseline ../reports/phase_4_5_active_retrieval_baseline.json --output ../reports/phase_4_5_dense_candidate_comparison.json
```

Expected: the report contains embedded immutable active evidence, the candidate run, profile summaries, metrics, latency, failures and per-query ordered ID differences. Do not demand exact floating-point equality; explain every ranking or metric delta.

- [ ] **Step 7: Run the full backend suite once**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase45-plan-uv-cache uv run --env-file ../.env python -m pytest tests -q --tb=short -k 'not TestChatSuccess and not test_answer_evaluation_calls_real_generation_and_judge_models and not test_live_generate_answer_success and not test_no_sensitive_payload_in_responses'
```

Expected: every non-paid backend test passes; pytest reports the explicitly deselected paid chat/generation/judge tests. Record pass/deselection counts. Phase 4–5 verification must not incur paid calls.

- [ ] **Step 8: Audit source hygiene and leftovers**

Run:

```bash
rg -n "SparseEmbedder|sparse_embedder|SPARSE_VECTOR_NAME|hybrid_index|RetrievalStack|verify_snapshot|corpus_fingerprint|config_fingerprint|scroll_batch_size|upsert_max_retries|reset_collection|lru_cache|local_files_only" backend notebooks --glob '*.py' --glob '*.ipynb'
git diff --check
git status --short
```

Expected: no obsolete runtime mechanism remains; any textual historical mention is explicitly non-runtime. No guarded test collection remains. Active and candidate both have 572 points.

- [ ] **Step 9: Write the implementation report and update status documents**

`reports/phase_4_5_qdrant_retrieval_simplicity_implementation.md` must state:

1. exact scoped files changed/deleted;
2. baseline active state and 104 × 3 results;
3. TDD RED/GREEN evidence by task;
4. real Qdrant/E5/MiniLM/notebook/full-suite evidence;
5. active/candidate schema, counts and comparison;
6. cleanup results and remaining unrelated dirty files;
7. explicit statement that active config, active collection, cutover, rollback deletion, commit and push were not performed;
8. recommendation to cut over or not, based only on observed evidence.

It must also include a compact retained-test audit for every affected test file: test name or behavior group, the user-needed behavior protected, and which duplicate/mechanism-only tests were removed. This is documentation in the implementation report, not a new registry or runtime artifact.

Update Phase 4/5 guides and `Project_Status.md` to `under_review` only after all evidence is complete. Phase 8 remains `not_ready`; record that true Qdrant sparse retrieval remains a separate isolated Phase 8 experiment.

- [ ] **Step 10: Stop at the reviewer/cutover gate**

Do not change `vector_database.collection_name`, delete either long-lived collection, commit or push. Hand off exact commands/results and wait for independent Reviewer verification, then a separate user cutover decision.

---

## Self-Review Checklist

- Every approved design section maps to a task: dense schema/points/upsert/reset (Tasks 3–4), BM25 (Task 2), concrete reranker (Task 5), startup/service/status (Task 6), context (Task 7), notebooks (Task 8), baseline/candidate comparison and blue-green gates (Tasks 1 and 9).
- Candidate targeting exists only at ingestion/evaluation composition roots and uses deep-copied settings.
- Active collection is never written or deleted; guarded tests and the approved fixed candidate are the only mutation targets.
- Phase 8 true sparse retrieval is not implemented here.
- No paid generation/judge command is included.
- No cache-only, retry, fingerprint, mock/fake, compatibility layer or hypothetical provider abstraction is introduced.
- No automatic commit/push/cutover/delete step exists.
