# Phase 8 — Notebook 08c MiniLM Reranker Benchmark Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

Status: `approved` by the user on 2026-08-30 (+07). The exact implementation,
real local MiniLM execution and approved 08c artifact creation are authorized
through the current Implementer handoff. Commit and push remain unauthorized.

**Goal:** Build an auditable Foods-only benchmark that compares no-rerank with the existing `cross-encoder/ms-marco-MiniLM-L-6-v2` runtime on exactly three immutable 08b Top-10 inputs and reports evidence for a user decision.

**Architecture:** Add one evaluation-scoped module that validates approved 08b evidence, maps fixed chunk IDs to the canonical 572 chunk texts, runs the unchanged production `CrossEncoderReranker`, computes paired quality/resource evidence and atomically reconciles exactly two artifacts. Keep the notebook as a short Vietnamese orchestration and display layer; it must not contain scoring, validation or persistence logic.

**Tech Stack:** Python 3.13, uv, pytest, Sentence Transformers 5.6.1, Transformers 5.14.1, Torch 2.13.0, NumPy, Polars, psutil, Jupyter/nbconvert, existing Hue RAG evaluation and reranking modules.

## Global Constraints

- Follow the approved spec exactly: `docs/superpowers/specs/2026-08-30-phase-8-08c-reranker-benchmark-design.md`.
- Work only in `/home/minhhieu/hue_rag`; preserve all unrelated user changes. In particular, do not absorb or revert the pre-existing concurrent modification to `notebooks/08b_retrieval_fusion_benchmark.ipynb`.
- Compare exactly `no-rerank` and `minilm`; do not add BGE, Qwen or another reranker.
- Use exactly `dense__e5-small-384`, `dense__huydang-dek21-embedding-768`, and `hybrid-bm25-weighted__huydang-dek21-embedding-768`, in that order.
- Read `fusion_top_10` from approved `evaluation/results/phase8_sparse_cases.jsonl`; do not rerun retrieval, query Qdrant or create a duplicate input artifact.
- Validate exactly 45 completed cases per input, 135 selected records, ten unique canonical chunk IDs per record, 45 Golden V3 cases and 572 canonical chunks before loading MiniLM.
- Call the existing `backend/reranking/cross_encoder.py::CrossEncoderReranker` directly and do not modify it, wrap inference in a benchmark-only model adapter or add a generic reranker interface.
- Device is CPU and dtype is FP32. Load once, warm up once, run a 10-case smoke on the E5-small control input, then run 45 cases x 3 repetitions for each input sequentially.
- The smoke case IDs come from canonical `golden_v3_smoke.jsonl`; smoke is an integration gate and is excluded from artifacts and latency aggregates.
- No fallback, retry, reload between inputs, device change or altered input is permitted. A load failure blocks all MiniLM scoring; an input failure is recorded and independent later inputs may continue.
- Persist after every completed or failed input. A rerun replaces rows/records for that exact input and preserves the other two inputs.
- Produce only `evaluation/results/phase8_reranker_results.csv` and `evaluation/results/phase8_reranker_cases.jsonl`; no 08c manifest, registry, checksum package, cache or copied inputs.
- Summary schema/order is exactly the 39 columns in the approved spec and reconciles to 60 rows. Per-case schema/order is exactly the 24 top-level keys in the approved spec and reconciles to 135 records.
- Bootstrap uses 10,000 paired resamples, seed 42 and 95% percentile intervals. Eligibility requires stable 3/3 repetitions, all category guardrails and warm p95 <= 3000 ms for a ten-pair rerank call.
- Flags are descriptive evidence only. Code and notebook must not select a winner, authorize 08d or change production.
- Do not edit Golden V3, Foods Markdown, chunking, 08a/08b artifacts, active Qdrant, production settings/startup/retrieval, dependencies or lockfiles.
- Repository notebook outputs remain empty and execution counts null. Real verification executes to `/tmp`.
- No paid API, generation, multi-domain work, active mutation or production cutover.
- Do not commit or push unless the user separately grants Git authorization. Commit steps below are conditional checkpoints, not authorization.

---

## File map

- Create `backend/evaluation/reranker_benchmark.py`: immutable input loading/validation, canonical mapping, metrics/flags, runtime orchestration, atomic persistence and reconciliation.
- Create `backend/tests/test_reranker_benchmark.py`: deterministic tests for the exact contracts; no model download and no fake-model claim of completion.
- Create `notebooks/08c_reranker_benchmark.ipynb`: clean Vietnamese learning/orchestration notebook calling backend functions.
- Create during an explicitly authorized real run only:
  - `evaluation/results/phase8_reranker_results.csv`;
  - `evaluation/results/phase8_reranker_cases.jsonl`.
- Create after the authorized run: `reports/phase_8_08c_reranker_benchmark_implementation_report.md`.
- Modify at implementation handoff/closure only: `session_prompt/CURRENT_HANDOFF.md`.

The following paths are consumed but must remain byte-for-byte unchanged:

- `backend/reranking/cross_encoder.py`;
- `backend/evaluation/embedding_benchmark.py`;
- `backend/evaluation/sparse_benchmark.py`;
- `backend/evaluation/golden_dataset.py`;
- `backend/ingestion/chunking/markdown_chunker.py`;
- `knowledge-base-hue/foods/evaluation/golden_v3.jsonl`;
- `knowledge-base-hue/foods/evaluation/golden_v3_smoke.jsonl`;
- all curated Foods Markdown;
- `evaluation/results/phase8_sparse_manifest.json`;
- `evaluation/results/phase8_sparse_cases.jsonl`;
- production config and Qdrant collections.

## Review Contract

**Risk:** `high` because this work loads a real ML model, computes decision-grade
quality metrics and durable artifacts, and can influence a later production
choice. Triggers are model/retrieval/scoring, quality/evaluation, resource
measurement, durable evidence and lifecycle documentation.

**Implementer evidence required:**

1. exact base/head/worktree state and every changed/untracked path;
2. focused RED/GREEN command results for each task;
3. source-notebook structural check proving empty outputs/null execution counts;
4. one real MiniLM smoke result and a temporary full Notebook Run All result;
5. observed cold load, per-input warm p50/p95, RSS checkpoints and stability;
6. exact 60/135 artifact reconciliation and schema/order checks;
7. before/after SHA256 for Golden V3, Foods corpus inventory/content,
   chunker, 08a/08b artifacts, production reranker/config and active-collection
   read-only snapshot when available;
8. acceptance-to-evidence mapping, failed/skipped checks and limitations in
   `reports/phase_8_08c_reranker_benchmark_implementation_report.md`;
9. no winner/08d/production decision represented as automatic approval.

**Minimum independent Reviewer checks:** inspect all changed/untracked paths and
the exact diff; map it to the approved spec; inspect the direct use of
`CrossEncoderReranker`; recompute selected per-case metrics/flags from artifacts;
check exact input identity/counts, schemas, row counts, notebook cleanliness and
immutable-file hashes; run `git diff --check`.

**Exact Reviewer reruns from `backend/`:**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-08c-review-uv-cache uv run python -m pytest tests/test_reranker_benchmark.py tests/test_reranker.py -q --tb=short -s
```

Expected: all focused deterministic tests pass without network or model load.

```bash
UV_CACHE_DIR=/tmp/hue-rag-08c-review-live-uv-cache uv run --env-file ../.env jupyter nbconvert --execute --to notebook ../notebooks/08c_reranker_benchmark.ipynb --output /tmp/08c_reranker_benchmark-review-live.ipynb --ExecutePreprocessor.timeout=1800
```

Expected: exit 0 through the real MiniLM path; output exists only in `/tmp`.

```bash
UV_CACHE_DIR=/tmp/hue-rag-08c-review-uv-cache uv run python -m pytest tests -q --tb=short
git diff --check
```

Expected: full backend suite passes and diff check emits no output. The Reviewer
also runs the artifact reconciliation helper from the executed notebook and
expects `complete=true`, `summary_rows=60`, `case_records=135`.

**Correction evidence eligible for reuse:** unchanged deterministic test logs,
immutable-input hashes and completed real input artifacts may be reused only
when the correction does not touch their producer, schema, scoring, input
identity, runtime model or environment. Any change to those boundaries requires
rerunning the affected test and real input; model execution is not rerun for a
documentation-only correction.

**New authority required:** any runtime reranker/dependency change, new model,
retrieval rerun, Qdrant write, Golden/corpus/chunker edit, paid call, generation,
08d, multi-domain work, production selection/cutover, destructive cleanup,
commit or push.

**Intended approval closure:** Reviewer reports evidence for all three inputs
and asks the user for the final 08c verdict. If no pairing is eligible, recommend
removing reranking from 08d. If at least one is eligible, present trade-offs and
ask whether to open a separately scoped 08d. Only after that user decision may
Reviewer update benchmark/status docs and write an Approval Closure Contract.

---

### Task 1: Lock immutable 08b input selection and canonical text mapping

**Files:**
- Create: `backend/evaluation/reranker_benchmark.py`
- Create: `backend/tests/test_reranker_benchmark.py`

**Interfaces:**
- Produces: `RerankerInputSetting(order: int, key: str, label: str)` and `INPUT_SETTINGS`
- Produces: `FixedRerankerCase(input_order, input_key, case, pre_rerank_documents)`
- Produces: `RerankerBenchmarkInputs(cases, smoke_case_ids, chunks_by_id, fixed_cases, immutable_identity)`
- Produces: `load_reranker_benchmark_inputs(*, manifest_path: Path = SPARSE_MANIFEST_PATH, sparse_cases_path: Path = SPARSE_CASES_PATH, chunk_loader: Callable[[], list[dict]] = chunk_foods_markdown) -> RerankerBenchmarkInputs`
- Consumes: 08b manifest/cases, Golden V3 full/smoke and `chunk_foods_markdown()`

- [ ] **Step 1: Write failing tests for exact setting order and successful 135-record selection**

Add imports and fixtures to `backend/tests/test_reranker_benchmark.py`:

```python
import json
from pathlib import Path

import pytest

from evaluation.golden_dataset import GoldenCase
from evaluation.reranker_benchmark import (
    INPUT_SETTINGS,
    validate_reranker_inputs,
)


def make_case(case_id: str, category: str = "direct_fact") -> GoldenCase:
    return GoldenCase(
        case_id=case_id,
        question=f"Câu hỏi {case_id}?",
        keywords=["Huế", "món"],
        reference_answer="Huế có món ngon.",
        category=category,
        evidence={"foods/a.md": ["A"]},
    )


def make_chunk(chunk_id: str) -> dict:
    return {
        "text": f"Nội dung {chunk_id}",
        "metadata": {
            "chunk_id": chunk_id,
            "source": "foods/a.md",
            "section": "A",
        },
    }


def make_manifest(corpus_fp: str, golden_fp: str, chunker_fp: str) -> dict:
    return {
        "schema_version": "phase8-sparse-manifest-v1",
        "experiment_version": "phase8-08b-v1",
        "immutable_identity": {
            "corpus_fingerprint": corpus_fp,
            "golden_fingerprint": golden_fp,
            "chunker_fingerprint": chunker_fp,
        },
    }


def make_fixed_rows(cases: list[GoldenCase], chunk_ids: list[str]) -> list[dict]:
    rows = []
    for setting in INPUT_SETTINGS:
        for case in cases:
            rows.append({
                "experiment_version": "phase8-08b-v1",
                "setting_order": setting.order,
                "setting_key": setting.key,
                "case_id": case.case_id,
                "category": case.category,
                "status": "completed",
                "successful_repetitions": 3,
                "ranking_stable": True,
                "relevant_source_sections": [{"source": "foods/a.md", "section": "A"}],
                "fusion_top_10": [
                    {
                        "chunk_id": chunk_id,
                        "rank": rank,
                        "fused_score": 1.0 / rank,
                        "source": "foods/a.md",
                        "section": "A",
                    }
                    for rank, chunk_id in enumerate(chunk_ids, start=1)
                ],
            })
    return rows


def test_input_settings_are_exact_and_ordered():
    assert [(s.order, s.key) for s in INPUT_SETTINGS] == [
        (1, "dense__e5-small-384"),
        (2, "dense__huydang-dek21-embedding-768"),
        (3, "hybrid-bm25-weighted__huydang-dek21-embedding-768"),
    ]


def test_validate_reranker_inputs_selects_exact_records_and_maps_text(monkeypatch):
    cases = [make_case(f"foods-v3-{i:04d}") for i in range(1, 46)]
    chunks = [make_chunk(f"chunk-{i:03d}") for i in range(1, 573)]
    selected_ids = [f"chunk-{i:03d}" for i in range(1, 11)]
    monkeypatch.setattr("evaluation.reranker_benchmark.fingerprint_corpus", lambda value: "c" * 64)
    monkeypatch.setattr("evaluation.reranker_benchmark.fingerprint_golden", lambda value: "g" * 64)
    monkeypatch.setattr("evaluation.reranker_benchmark.fingerprint_chunker_code", lambda path: "k" * 64)

    result = validate_reranker_inputs(
        manifest=make_manifest("c" * 64, "g" * 64, "k" * 64),
        sparse_case_records=make_fixed_rows(cases, selected_ids),
        cases=cases,
        smoke_cases=cases[:10],
        chunks=chunks,
        chunker_path=Path("chunker.py"),
    )

    assert len(result.fixed_cases) == 135
    assert len(result.chunks_by_id) == 572
    assert result.smoke_case_ids == tuple(c.case_id for c in cases[:10])
    first = result.fixed_cases[0]
    assert [doc.id for doc in first.pre_rerank_documents] == selected_ids
    assert first.pre_rerank_documents[0].text == "Nội dung chunk-001"
```

- [ ] **Step 2: Run the focused tests and verify RED**

Run from `backend/`:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-08c-uv-cache uv run python -m pytest tests/test_reranker_benchmark.py -q --tb=short
```

Expected: collection fails with `ModuleNotFoundError: evaluation.reranker_benchmark`.

- [ ] **Step 3: Implement constants, dataclasses, loaders and fail-closed validation**

Create `backend/evaluation/reranker_benchmark.py` with these public contracts:

```python
"""Fixed-input MiniLM reranker benchmark orchestration for Phase 8 Notebook 08c."""
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Callable, Sequence

from core.schema import RetrievedDocument
from evaluation.golden_dataset import GoldenCase, V3_FULL_PATH, V3_SMOKE_PATH, load_golden, validate_v3_full, validate_v3_smoke
from evaluation.sparse_benchmark import CHUNKER_PATH, fingerprint_chunker_code, fingerprint_corpus, fingerprint_golden
from ingestion.chunking.markdown_chunker import chunk_foods_markdown
from vectorstore.points import validate_chunks

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESULTS_DIR = REPO_ROOT / "evaluation" / "results"
SPARSE_MANIFEST_PATH = DEFAULT_RESULTS_DIR / "phase8_sparse_manifest.json"
SPARSE_CASES_PATH = DEFAULT_RESULTS_DIR / "phase8_sparse_cases.jsonl"
EXPERIMENT_VERSION = "phase8-08c-v1"
SOURCE_EXPERIMENT_VERSION = "phase8-08b-v1"
MODEL_ID = "cross-encoder/ms-marco-MiniLM-L-6-v2"


@dataclass(frozen=True)
class RerankerInputSetting:
    order: int
    key: str
    label: str


INPUT_SETTINGS = (
    RerankerInputSetting(1, "dense__e5-small-384", "E5-small dense control"),
    RerankerInputSetting(2, "dense__huydang-dek21-embedding-768", "Huydang dense"),
    RerankerInputSetting(3, "hybrid-bm25-weighted__huydang-dek21-embedding-768", "Huydang + BM25 weighted diagnostic"),
)


@dataclass(frozen=True)
class FixedRerankerCase:
    input_order: int
    input_key: str
    case: GoldenCase
    relevant_source_sections: tuple[tuple[str, str], ...]
    pre_rerank_documents: tuple[RetrievedDocument, ...]


@dataclass(frozen=True)
class RerankerBenchmarkInputs:
    cases: tuple[GoldenCase, ...]
    smoke_case_ids: tuple[str, ...]
    chunks_by_id: dict[str, dict]
    fixed_cases: tuple[FixedRerankerCase, ...]
    immutable_identity: dict[str, str]


def _read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSONL at line {line_number}: {path}") from exc
    return rows


def validate_reranker_inputs(
    *,
    manifest: dict,
    sparse_case_records: Sequence[dict],
    cases: Sequence[GoldenCase],
    smoke_cases: Sequence[GoldenCase],
    chunks: Sequence[dict],
    chunker_path: Path = CHUNKER_PATH,
) -> RerankerBenchmarkInputs:
    if manifest.get("schema_version") != "phase8-sparse-manifest-v1":
        raise ValueError("08b manifest schema mismatch")
    if manifest.get("experiment_version") != SOURCE_EXPERIMENT_VERSION:
        raise ValueError("08b experiment version mismatch")
    if len(cases) != 45:
        raise ValueError(f"expected 45 Golden V3 cases, got {len(cases)}")
    if len(smoke_cases) != 10:
        raise ValueError(f"expected 10 Golden V3 smoke cases, got {len(smoke_cases)}")
    validate_v3_smoke(list(cases), list(smoke_cases))
    chunk_ids = validate_chunks(list(chunks))
    if len(chunk_ids) != 572:
        raise ValueError(f"expected 572 canonical chunks, got {len(chunk_ids)}")

    identity = {
        "corpus_fingerprint": fingerprint_corpus(chunks),
        "golden_fingerprint": fingerprint_golden(cases),
        "chunker_fingerprint": fingerprint_chunker_code(chunker_path),
    }
    approved_identity = manifest.get("immutable_identity", {})
    if any(approved_identity.get(key) != value for key, value in identity.items()):
        raise ValueError("08b immutable identity mismatch")

    cases_by_id = {case.case_id: case for case in cases}
    chunks_by_id = {str(chunk["metadata"]["chunk_id"]): chunk for chunk in chunks}
    selected_keys = {setting.key for setting in INPUT_SETTINGS}
    selected = [row for row in sparse_case_records if row.get("setting_key") in selected_keys]
    if len(selected) != 135:
        raise ValueError(f"expected 135 selected 08b records, got {len(selected)}")

    fixed = []
    for setting in INPUT_SETTINGS:
        rows = [row for row in selected if row.get("setting_key") == setting.key]
        if len(rows) != 45 or {row.get("case_id") for row in rows} != set(cases_by_id):
            raise ValueError(f"{setting.key}: expected each canonical case exactly once")
        rows.sort(key=lambda row: row["case_id"])
        for row in rows:
            if row.get("experiment_version") != SOURCE_EXPERIMENT_VERSION or row.get("status") != "completed":
                raise ValueError(f"{setting.key}/{row.get('case_id')}: incomplete 08b record")
            ranking = row.get("fusion_top_10")
            if not isinstance(ranking, list) or len(ranking) != 10:
                raise ValueError(f"{setting.key}/{row.get('case_id')}: expected fusion_top_10")
            ids = [item.get("chunk_id") for item in ranking]
            if len(set(ids)) != 10 or [item.get("rank") for item in ranking] != list(range(1, 11)):
                raise ValueError(f"{setting.key}/{row.get('case_id')}: invalid Top-10 order")
            if any(chunk_id not in chunks_by_id for chunk_id in ids):
                raise ValueError(f"{setting.key}/{row.get('case_id')}: unknown canonical chunk")
            documents = tuple(
                RetrievedDocument(
                    id=chunk_id,
                    score=float(item["fused_score"]),
                    text=str(chunks_by_id[chunk_id]["text"]),
                    metadata={
                        **dict(chunks_by_id[chunk_id]["metadata"]),
                        "pre_rerank_score": float(item["fused_score"]),
                    },
                )
                for chunk_id, item in zip(ids, ranking)
            )
            relevant = tuple(
                (item["source"], item["section"])
                for item in row.get("relevant_source_sections", [])
            )
            case = cases_by_id[row["case_id"]]
            expected_relevant = tuple((source, section) for source, sections in case.evidence.items() for section in sections)
            if relevant != expected_relevant or row.get("category") != case.category:
                raise ValueError(f"{setting.key}/{case.case_id}: Golden evidence mismatch")
            fixed.append(FixedRerankerCase(setting.order, setting.key, case, relevant, documents))

    return RerankerBenchmarkInputs(
        tuple(sorted(cases, key=lambda case: case.case_id)),
        tuple(case.case_id for case in smoke_cases),
        chunks_by_id,
        tuple(fixed),
        identity,
    )


def load_reranker_benchmark_inputs(
    *,
    manifest_path: Path = SPARSE_MANIFEST_PATH,
    sparse_cases_path: Path = SPARSE_CASES_PATH,
    chunk_loader: Callable[[], list[dict]] = chunk_foods_markdown,
) -> RerankerBenchmarkInputs:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cases = load_golden(V3_FULL_PATH)
    smoke_cases = load_golden(V3_SMOKE_PATH)
    validate_v3_full(cases)
    return validate_reranker_inputs(
        manifest=manifest,
        sparse_case_records=_read_jsonl(sparse_cases_path),
        cases=cases,
        smoke_cases=smoke_cases,
        chunks=chunk_loader(),
    )
```

- [ ] **Step 4: Add rejection tests and run GREEN**

Parameterize mutations for wrong experiment version, missing/duplicate case,
non-completed status, Top-10 length/rank/duplicate, unknown chunk, Golden
category/evidence mismatch and all three fingerprint mismatches. Each mutation
must assert `ValueError` and the relevant boundary term. Then rerun the focused
command and expect all Task 1 tests to pass.

- [ ] **Step 5: Conditional commit checkpoint**

Only with separate Git authorization:

```bash
git add backend/evaluation/reranker_benchmark.py backend/tests/test_reranker_benchmark.py
git commit -m "test: lock phase 8 reranker benchmark inputs"
```

Otherwise record `not run: Git authorization none`.

---

### Task 2: Implement paired scoring, evidence flags and audit deltas

**Files:**
- Modify: `backend/evaluation/reranker_benchmark.py`
- Modify: `backend/tests/test_reranker_benchmark.py`

**Interfaces:**
- Consumes: `score_retrieval_case`, `aggregate_case_metrics`, `evaluate_category_guardrails`, `paired_bootstrap_intervals`
- Produces: `score_fixed_pair(case, no_rerank_docs, minilm_docs) -> PairedCaseEvidence`
- Produces: `evaluate_input_evidence(paired_cases: Sequence[PairedCaseEvidence], *, successful_repetitions: int, ranking_stable: bool, rerank_p95_ms: float) -> InputEvidence`
- Produces: `evaluate_production_safety(hybrid_metrics, production_metrics) -> bool`

- [ ] **Step 1: Write failing tests for before/after metrics and rank movement**

Use two evidence sections and controlled `RetrievedDocument` lists. Assert:

```python
paired = score_fixed_pair(case, before_docs, after_docs)
assert paired.before.hit is True
assert paired.after.hit is True
assert paired.hit_change == "unchanged_hit"
assert paired.relevant_rank_before == {"foods/a.md|A": 4, "foods/b.md|B": None}
assert paired.relevant_rank_after == {"foods/a.md|A": 2, "foods/b.md|B": 5}
assert paired.after.ndcg_at_5 > paired.before.ndcg_at_5
```

Also cover `lost`, `unchanged_hit`, `unchanged_miss`, duplicate source/section
credit and deterministic MiniLM tie order inherited from the runtime class.

- [ ] **Step 2: Run RED**

Run the focused test module. Expected: import errors for the new scoring APIs.

- [ ] **Step 3: Implement paired evidence with existing metric helpers**

Add dataclasses and functions:

```python
from evaluation.embedding_benchmark import (
    BootstrapInterval,
    CaseMetrics,
    aggregate_case_metrics,
    evaluate_category_guardrails,
    paired_bootstrap_intervals,
    score_retrieval_case,
)


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
    before_metrics: tuple[CaseMetrics, ...]
    after_metrics: tuple[CaseMetrics, ...]
    aggregates_before: dict[str, dict[str, int | float]]
    aggregates_after: dict[str, dict[str, int | float]]
    guardrails: dict[str, bool]
    bootstrap: dict[str, BootstrapInterval]
    eligible: bool
    clear_gain: bool


def _relevant_ranks(case: GoldenCase, docs: Sequence[RetrievedDocument]) -> dict[str, int | None]:
    keys = [(source, section) for source, sections in case.evidence.items() for section in sections]
    ranks = {}
    for source, section in keys:
        key = f"{source}|{section}"
        ranks[key] = next(
            (rank for rank, doc in enumerate(docs[:5], start=1)
             if doc.metadata.get("source") == source and doc.metadata.get("section") == section),
            None,
        )
    return ranks


def score_fixed_pair(case: GoldenCase, no_rerank_docs: Sequence[RetrievedDocument], minilm_docs: Sequence[RetrievedDocument]) -> PairedCaseEvidence:
    before = score_retrieval_case(case, list(no_rerank_docs), k=5)
    after = score_retrieval_case(case, list(minilm_docs), k=5)
    if not before.hit and after.hit:
        change = "gained"
    elif before.hit and not after.hit:
        change = "lost"
    elif before.hit and after.hit:
        change = "unchanged_hit"
    else:
        change = "unchanged_miss"
    return PairedCaseEvidence(case.case_id, case.category, before, after, change, _relevant_ranks(case, no_rerank_docs), _relevant_ranks(case, minilm_docs))


def evaluate_input_evidence(
    paired_cases: Sequence[PairedCaseEvidence],
    *,
    successful_repetitions: int,
    ranking_stable: bool,
    rerank_p95_ms: float,
) -> InputEvidence:
    before = tuple(item.before for item in paired_cases)
    after = tuple(item.after for item in paired_cases)
    guards = evaluate_category_guardrails(list(before), list(after))
    bootstrap = paired_bootstrap_intervals(list(before), list(after), samples=10_000, seed=42)
    eligible = bool(successful_repetitions == 3 and ranking_stable and all(guards.values()) and rerank_p95_ms <= 3000.0)
    clear_gain = bool(eligible and bootstrap["ndcg"].delta >= 0.03 and bootstrap["ndcg"].lower > 0.0)
    return InputEvidence(
        before,
        after,
        aggregate_case_metrics(list(before)),
        aggregate_case_metrics(list(after)),
        guards,
        bootstrap,
        eligible,
        clear_gain,
    )


def evaluate_production_safety(hybrid_metrics: Sequence[CaseMetrics], production_metrics: Sequence[CaseMetrics]) -> bool:
    guards = evaluate_category_guardrails(list(production_metrics), list(hybrid_metrics))
    production_recall = aggregate_case_metrics(list(production_metrics))["overall"]["recall_at_5"]
    hybrid_recall = aggregate_case_metrics(list(hybrid_metrics))["overall"]["recall_at_5"]
    return bool(all(guards.values()) and hybrid_recall >= production_recall - 0.005)
```

Use the exact persisted vocabulary `gained`, `lost`, `unchanged_hit`, and
`unchanged_miss`.

- [ ] **Step 4: Add boundary tests for flags and production safety, then run GREEN**

Test p95 exactly `3000.0` passes and `3000.0001` fails; unstable ranking and
2/3 repetitions fail; nDCG delta exactly `0.03` with lower bound `>0` passes;
lower bound `0` fails; hybrid recall loss exactly `0.005` passes and a larger
loss fails; every category guardrail failure dominates aggregate gain.

- [ ] **Step 5: Conditional commit checkpoint**

```bash
git add backend/evaluation/reranker_benchmark.py backend/tests/test_reranker_benchmark.py
git commit -m "feat: add phase 8 reranker evidence rules"
```

Run only with separate Git authorization.

---

### Task 3: Implement exact artifact schemas and atomic per-input replacement

**Files:**
- Modify: `backend/evaluation/reranker_benchmark.py`
- Modify: `backend/tests/test_reranker_benchmark.py`

**Interfaces:**
- Produces: `RESULT_COLUMNS`, `CASE_RECORD_FIELDS`
- Produces: `upsert_input_artifacts(input_key, summary_rows, case_records, *, results_path, cases_path) -> None`
- Produces: `reconcile_reranker_artifacts(*, results_path: Path = RESULTS_PATH, cases_path: Path = CASES_PATH) -> ReconciliationResult`

- [ ] **Step 1: Write failing schema and idempotent replacement tests**

Create 20 summary rows and 45 case records for each of three inputs. Call the
upsert function first for inputs 1 and 2, then replace input 1. Assert input 2
is unchanged, input 1 has only replacement data, CSV headers equal
`RESULT_COLUMNS`, JSON key order equals `CASE_RECORD_FIELDS`, final counts are
40/90 before input 3 and 60/135 after input 3.

- [ ] **Step 2: Run RED**

Expected: missing persistence APIs.

- [ ] **Step 3: Implement ordered schemas, atomic writes and reconciliation**

Copy `RESULT_COLUMNS` and `CASE_RECORD_FIELDS` verbatim from the approved spec.
Use only keyed replacement and `os.replace`:

```python
import csv
import os
import tempfile

RESULTS_PATH = DEFAULT_RESULTS_DIR / "phase8_reranker_results.csv"
CASES_PATH = DEFAULT_RESULTS_DIR / "phase8_reranker_cases.jsonl"


@dataclass(frozen=True)
class ReconciliationResult:
    complete: bool
    summary_rows: int
    case_records: int
    errors: tuple[str, ...]


def _atomic_csv(rows: Sequence[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(RESULT_COLUMNS))
        writer.writeheader()
        writer.writerows({key: row.get(key, "") for key in RESULT_COLUMNS} for row in rows)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def _atomic_jsonl(rows: Sequence[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as handle:
        for row in rows:
            ordered = {key: row.get(key, "") for key in CASE_RECORD_FIELDS}
            handle.write(json.dumps(ordered, ensure_ascii=False, separators=(",", ":")) + "\n")
        temporary = Path(handle.name)
    os.replace(temporary, path)


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
```

Implement `reconcile_reranker_artifacts` fail-closed: exact headers/keys,
approved input/state keys and orders, `overall` plus the exact nine observed
Golden categories, unique `(input_key,state_key,category)` rows, unique
`(input_key,case_id)` records, exact 60/135 for complete, status-aware blank
non-applicable fields, and recomputed metrics/flags matching records within
`1e-12`. It must read only; it never repairs artifacts.

- [ ] **Step 4: Run GREEN and verify no temporary files remain**

Use `tmp_path` for every persistence test. Assert no sibling temporary files
remain after success. Add a monkeypatched `os.replace` failure test proving the
existing durable file is not partially overwritten.

- [ ] **Step 5: Conditional commit checkpoint**

```bash
git add backend/evaluation/reranker_benchmark.py backend/tests/test_reranker_benchmark.py
git commit -m "feat: persist phase 8 reranker evidence atomically"
```

Run only with separate Git authorization.

---

### Task 4: Orchestrate the unchanged real MiniLM runtime and resource evidence

**Files:**
- Modify: `backend/evaluation/reranker_benchmark.py`
- Modify: `backend/tests/test_reranker_benchmark.py`

**Interfaces:**
- Consumes: `CrossEncoderReranker(model_id=MODEL_ID, device="cpu")`
- Produces: `load_runtime_reranker() -> tuple[CrossEncoderReranker, RuntimeEvidence]`
- Produces: `run_technical_smoke(inputs, reranker) -> dict[str, object]`
- Produces: `run_reranker_input(inputs: RerankerBenchmarkInputs, input_setting: RerankerInputSetting, reranker: CrossEncoderReranker, runtime_evidence: RuntimeEvidence, *, results_path: Path = RESULTS_PATH, cases_path: Path = CASES_PATH) -> InputRunResult`
- Produces: `run_all_reranker_inputs(inputs: RerankerBenchmarkInputs, *, results_path: Path = RESULTS_PATH, cases_path: Path = CASES_PATH) -> ReconciliationResult`

- [ ] **Step 1: Write failing orchestration tests without loading a model**

Patch `CrossEncoderReranker.rerank` itself, not a new adapter. Record received
query/document pairs and return deterministic `RetrievedDocument` objects.
Assert:

- the smoke uses exactly ten canonical smoke IDs from input 1;
- each full input invokes rerank `45 * 3` times with `top_k=5` and ten docs;
- all repetitions receive identical ordered chunk IDs;
- the first repetition supplies persisted rankings/scores;
- all three ordered rankings must match for `ranking_stable=True`;
- one input failure writes its failed 20/45 records and input 3 still runs;
- model load failure prevents all calls and preserves truthful failed states;
- no retry or second model construction occurs.

- [ ] **Step 2: Run RED**

Expected: missing orchestration APIs.

- [ ] **Step 3: Implement runtime identity, load/warm-up and measurement**

Add exact direct imports and evidence types:

```python
from datetime import datetime, timezone
import gc
import importlib.metadata
import statistics
import time

import psutil

from evaluation.sparse_benchmark import sanitize_error_message
from reranking.cross_encoder import CrossEncoderReranker


@dataclass(frozen=True)
class RuntimeEvidence:
    model_id: str
    model_revision: str
    sentence_transformers_version: str
    transformers_version: str
    torch_version: str
    device: str
    dtype: str
    cold_load_ms: float
    rss_before_load_mb: float
    rss_after_load_mb: float
    observed_peak_rss_mb: float


def _rss_mb(process: psutil.Process) -> float:
    return process.memory_info().rss / (1024 * 1024)


def load_runtime_reranker() -> tuple[CrossEncoderReranker, RuntimeEvidence]:
    process = psutil.Process()
    before = _rss_mb(process)
    reranker = CrossEncoderReranker(model_id=MODEL_ID, device="cpu")
    started = time.perf_counter_ns()
    reranker.load()
    cold_load_ms = (time.perf_counter_ns() - started) / 1_000_000
    after = _rss_mb(process)
    reranker.warm_up()
    peak = max(before, after, _rss_mb(process))
    evidence = RuntimeEvidence(
        model_id=reranker.model_id,
        model_revision="not_reported",
        sentence_transformers_version=importlib.metadata.version("sentence-transformers"),
        transformers_version=importlib.metadata.version("transformers"),
        torch_version=importlib.metadata.version("torch"),
        device="cpu",
        dtype="float32",
        cold_load_ms=cold_load_ms,
        rss_before_load_mb=before,
        rss_after_load_mb=after,
        observed_peak_rss_mb=peak,
    )
    return reranker, evidence
```

Do not inspect Hugging Face caches or introduce revision-discovery logic;
persist `not_reported` as approved.

- [ ] **Step 4: Implement smoke and sequential 3-repetition execution**

For every rerank call, measure only `reranker.rerank(question, exact_top_10,
top_k=5)` using `perf_counter_ns`. Store all 135 full-run latencies per input;
compute p50/p95 using `numpy.percentile`. Stability compares the ordered
`chunk_id` tuple across all three repetitions for every case. Build paired
case evidence from repetition one and generate the exact 20 summary/45 case
records before calling `upsert_input_artifacts`.

Always create the no-rerank state from `pre_rerank_documents[:5]`; it has no
latency/resource values. `cold_load_ms` and RSS fields appear only on input 1,
`minilm`, `overall`; per-input rerank p50/p95 appear on each `minilm/overall`.
Blank values, never zero, represent non-applicable fields.

The orchestrator owns one RSS checkpoint list: before load, after load, after
warm-up and after each input. After input 3 it recomputes the observed maximum
and atomically replaces the input-1 MiniLM overall row so the persisted peak
covers the complete one-load lifecycle. `production_safety` is blank for both
dense inputs and is computed only for hybrid MiniLM against E5-small
no-rerank; if either comparison branch failed, it is blank rather than false.

Wrap each input independently. Persist `status=failed`, the sanitized bounded
error, true successful repetition count and blank unavailable metrics for a
failed MiniLM branch while retaining its completed no-rerank control. Release
with:

```python
if reranker is not None:
    reranker._model = None
del reranker
gc.collect()
```

This cleanup is evaluation lifecycle handling, not a change to the runtime
class. Do not clear or delete any model cache.

- [ ] **Step 5: Add record-building assertions and run GREEN**

Assert exact ranked document fields:

```python
{"chunk_id", "rank", "score", "source", "section"}
```

Assert per-case repetition latencies contain exactly three positive finite
milliseconds on success and no raw text, traceback or exception payload is
persisted. Run the focused tests and expect all pass offline.

- [ ] **Step 6: Conditional commit checkpoint**

```bash
git add backend/evaluation/reranker_benchmark.py backend/tests/test_reranker_benchmark.py
git commit -m "feat: run fixed-input MiniLM benchmark"
```

Run only with separate Git authorization.

---

### Task 5: Create the clean Vietnamese orchestration notebook

**Files:**
- Create: `notebooks/08c_reranker_benchmark.ipynb`
- Modify: `backend/evaluation/reranker_benchmark.py`
- Modify: `backend/tests/test_reranker_benchmark.py`

**Interfaces:**
- Consumes all execution and reconciliation APIs from Tasks 1–4
- Produces read-only Polars views from the two durable artifacts

- [ ] **Step 1: Write a failing notebook structure test**

Read the notebook as JSON and assert:

```python
assert notebook["nbformat"] == 4
assert len(notebook["cells"]) >= 22
assert all(cell.get("execution_count") is None for cell in code_cells)
assert all(cell.get("outputs") == [] for cell in code_cells)
source = "\n".join("".join(cell["source"]) for cell in notebook["cells"])
assert "load_reranker_benchmark_inputs" in source
assert "run_all_reranker_inputs" in source
assert "reconcile_reranker_artifacts" in source
assert "CrossEncoder(" not in source
assert "Qwen" not in source
assert "bge-reranker" not in source
```

- [ ] **Step 2: Run RED**

Expected: notebook file does not exist.

- [ ] **Step 3: Create the notebook with 11 alternating sections**

Build a valid nbformat 4 notebook with paired Vietnamese Markdown/code cells:

1. purpose and Foods-only/no-auto-selection boundary;
2. environment and runtime identity;
3. Golden V3/canonical/fixed-input validation;
4. three no-rerank controls;
5. MiniLM load and one warm-up;
6. ten Golden V3 smoke IDs on E5-small control;
7. sequential three-input full run;
8. aggregate/category deltas and bootstrap intervals;
9. gained/lost drill-down with `relationship` filter;
10. latency/RSS/stability;
11. evidence flags and explicit user-decision handoff.

The only execution cell that triggers the benchmark must call the backend
orchestrator. No cell may reimplement scoring, loop over model pairs, write CSV
or JSONL directly, access Qdrant, mutate environment variables or install a
dependency.

- [ ] **Step 4: Add exact read-only display cells and run notebook structure GREEN**

After orchestration succeeds, use these display-only cells; keep all scoring
and validation in the backend:

```python
import polars as pl

summary_df = pl.read_csv("../evaluation/results/phase8_reranker_results.csv")
cases_df = pl.read_ndjson("../evaluation/results/phase8_reranker_cases.jsonl")
display(summary_df.filter(pl.col("category") == "overall"))
display(summary_df.filter(pl.col("category") != "overall"))
display(cases_df.filter(pl.col("hit_change").is_in(["gained", "lost"])))
display(cases_df.filter(pl.col("category") == "relationship"))
display(
    summary_df.filter(
        (pl.col("category") == "overall") & (pl.col("state_key") == "minilm")
    ).select(
        "input_key", "eligible", "clear_gain", "production_safety",
        "rerank_p50_ms", "rerank_p95_ms", "observed_peak_rss_mb",
    )
)
```

The final Markdown cell states that these flags are evidence and asks for a
user decision; it must not render a winner. Rerun the notebook structure test
and expect GREEN.

- [ ] **Step 5: Conditional commit checkpoint**

```bash
git add notebooks/08c_reranker_benchmark.ipynb backend/evaluation/reranker_benchmark.py backend/tests/test_reranker_benchmark.py
git commit -m "docs: add phase 8 reranker benchmark notebook"
```

Run only with separate Git authorization.

---

### Task 6: Run deterministic verification, then the authorized real benchmark

**Files:**
- Create only during the authorized run: `evaluation/results/phase8_reranker_results.csv`
- Create only during the authorized run: `evaluation/results/phase8_reranker_cases.jsonl`
- Create: `reports/phase_8_08c_reranker_benchmark_implementation_report.md`

**Interfaces:**
- Consumes: completed backend/notebook APIs
- Produces: real MiniLM evidence and implementation report; no verdict

- [ ] **Step 1: Record immutable before-state**

Record `git status --short`, the exact diff and SHA256 values for the consumed
immutable paths listed in the Review Contract. Record the active collection
snapshot read-only if the configured service is available. Do not create or
modify Qdrant resources.

- [ ] **Step 2: Run focused and full deterministic tests**

From `backend/`:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-08c-uv-cache uv run python -m pytest tests/test_reranker_benchmark.py tests/test_reranker.py -q --tb=short -s
UV_CACHE_DIR=/tmp/hue-rag-08c-uv-cache uv run python -m pytest tests -q --tb=short
```

Expected: all pass. Stop and debug any failure before model execution.

- [ ] **Step 3: Execute a temporary real Notebook Run All**

This step requires explicit model-run authorization. From `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-08c-live-uv-cache uv run --env-file ../.env jupyter nbconvert --execute --to notebook ../notebooks/08c_reranker_benchmark.ipynb --output /tmp/08c_reranker_benchmark-live.ipynb --ExecutePreprocessor.timeout=1800
```

Expected: input validation occurs before model load; smoke passes before full
execution; exactly three inputs are persisted sequentially; command exits 0.
If a real load/input failure occurs, preserve truthful failed artifacts and
report it; do not retry or change the model/device/input.

- [ ] **Step 4: Reconcile artifacts and inspect evidence**

Run the read-only reconciliation helper and assert:

```python
result.complete is True
result.summary_rows == 60
result.case_records == 135
result.errors == ()
```

Independently inspect all three overall comparisons, all nine category slices,
gained/lost cases, `relationship`, bootstrap intervals, p50/p95, RSS and
stability. Do not translate `eligible` or `clear_gain` into approval.

- [ ] **Step 5: Verify immutable after-state and notebook cleanliness**

Recompute all before-state hashes/snapshots and require equality. Verify the
repository notebook remains empty/null and only the `/tmp` copy has outputs.
Run `git diff --check`.

- [ ] **Step 6: Write the implementation report**

The report must include:

- base/head/worktree and changed paths;
- exact environment/model identity and `model_revision=not_reported` limitation;
- command/result table distinguishing deterministic, smoke and full live runs;
- exact artifact counts/schemas and pointers;
- per-input quality/category/bootstrap/resource/stability evidence;
- gained/lost case IDs with special attention to `relationship`;
- acceptance criteria mapped to observed evidence;
- immutable before/after proof;
- failures, skipped work, deviations and residual risks;
- explicit statement that Reviewer/user verdict is pending and 08d is closed.

- [ ] **Step 7: Conditional commit checkpoint**

Only after artifacts/report are complete and only with separate Git authority:

```bash
git add backend/evaluation/reranker_benchmark.py backend/tests/test_reranker_benchmark.py notebooks/08c_reranker_benchmark.ipynb evaluation/results/phase8_reranker_results.csv evaluation/results/phase8_reranker_cases.jsonl reports/phase_8_08c_reranker_benchmark_implementation_report.md
git commit -m "feat: benchmark MiniLM reranking on fixed phase 8 inputs"
```

Otherwise leave the complete reviewed worktree uncommitted and report that
fact exactly.

---

### Task 7: Self-review and prepare the risk-gated Reviewer handoff

**Files:**
- Modify: `session_prompt/CURRENT_HANDOFF.md`
- Inspect: every changed and untracked path

**Interfaces:**
- Consumes: implementation report and all Task 1–6 evidence
- Produces: one `final_review` handoff; no approval closure

- [ ] **Step 1: Inspect the exact worktree and diff**

Run:

```bash
git status --short
git diff --check
git diff -- backend/evaluation/reranker_benchmark.py backend/tests/test_reranker_benchmark.py notebooks/08c_reranker_benchmark.ipynb reports/phase_8_08c_reranker_benchmark_implementation_report.md session_prompt/CURRENT_HANDOFF.md
```

Inspect artifacts separately because CSV/JSONL diffs are evidence, not source
review substitutes. Confirm the unrelated 08b notebook modification remains
outside this work package.

- [ ] **Step 2: Map every acceptance criterion to evidence**

Use the approved spec's ten acceptance criteria. For each, point to a test,
artifact field, immutable hash/snapshot or live-run observation. Mark any item
without evidence as `unverified`; do not infer a pass.

- [ ] **Step 3: Replace the current handoff with exact final-review context**

Set:

```text
Target role: reviewer
Authored by: implementer
Handoff kind: final_review
State: ready
Risk level: high
Git authorization: none
Sub-agent authorization: none
```

Include only acceptance-to-evidence mapping, changed paths, command/result
summary, risk/deviation flags, report/artifact pointers, failures/skips and the
exact Reviewer reruns from this plan. Do not include a self-issued verdict or
ask to open 08d.

- [ ] **Step 4: Stop for independent review**

Do not update benchmark/status verdicts, production config or Phase 8 closure.
Reviewer independently verifies this Review Contract, reports results to the
user and waits for the user's decision.

## Plan approval boundary

User approval of this document authorizes only the exact implementation and
real local MiniLM run described here when transferred into an Implementer
handoff. It does not authorize Git operations, new downloads beyond resolving
the already selected MiniLM model, Qdrant mutation, paid calls, 08d,
multi-domain work or production change. If the model is not already available
and network download is required, the Implementer must request that authority
explicitly before proceeding.

## Post-08c roadmap boundary

08c closes the current Foods-only experiment; its results must be labeled as
Foods evidence, not a project-wide quality estimate. The next separately
designed workstream will complete curated answer-facing Markdown across
`knowledge-base-hue/` (including Foods, Festivals, Heritage, Tourism,
Performing Arts and other approved domains), update domain-aware
chunking/metadata, generate fresh embeddings in an isolated full-corpus index,
and create a balanced combined Golden Dataset spanning every included domain.
Only after those prerequisites pass review does evaluation restart from the
Phase 7 baseline and rerun the affected Phase 8 experiments. None of that work
is authorized by this 08c implementation plan.

## Approved complexity-reset implementation delta — 2026-08-30 (+07)

User đã xác nhận reset direction sau Correction Review 4. Delta này supersede
mọi đề xuất tiếp tục vá reconciler theo từng field.

### Exact changed paths

- `backend/evaluation/reranker_benchmark.py`: refactor only
  `reconcile_reranker_artifacts()` và local reconciliation helpers.
- `backend/tests/test_reranker_benchmark.py`: refactor duplicated tamper setup và
  thêm representative non-finite cases.
- `reports/phase_8_08c_reranker_benchmark_implementation_report.md`: cập nhật
  fresh/reused evidence.
- `session_prompt/CURRENT_HANDOFF.md`: return `final_review` packet.

Không sửa producer functions, production reranker, notebook, CSV/JSONL
artifacts, schema constants, inputs, metrics, thresholds hoặc flags.

### Required implementation shape

1. Tạo một local helper/path parse required numeric value thành `float`; chỉ trả
   value khi `np.isfinite(value)` là true, còn lại append exact reconciliation
   error và fail closed.
2. Mọi persisted required numeric field được dùng trong case metrics, summary
   metrics/deltas, bootstrap bounds, summary latency và resource checks phải đi
   qua boundary này trước compare/recompute.
3. Blank-by-schema checks giữ riêng; không dùng `or 0.0` để biến missing/blank
   thành giá trị hợp lệ.
4. Reuse normalized value cho downstream eligibility/clear-gain/resource
   relations; không parse lại bằng distributed raw `float(...)` calls.
5. Gom copy/write/tamper test setup bằng helper hoặc parameterization. Prior ten
   tamper behaviors phải tiếp tục pass. Thêm representative `NaN`, `+Inf` và
   `-Inf` probes cho ít nhất: per-case metric, summary metric/delta, bootstrap CI,
   summary p50/p95 và resource numeric field.
6. Không thêm generic validator framework, typed artifact layer, manifest,
   checksum machinery hoặc artifact mới.

### Acceptance and reruns

Từ `backend/`:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-08c-reset-uv-cache uv run python -m pytest tests/test_reranker_benchmark.py -q --tb=short -s
PYTHONPATH=. HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-08c-reset-uv-cache uv run python -c "from evaluation.reranker_benchmark import reconcile_reranker_artifacts; r=reconcile_reranker_artifacts(); assert r.complete and r.summary_rows == 60 and r.case_records == 135 and not r.errors"
git diff --check
```

Acceptance cần chứng minh:

- current untampered artifacts vẫn `complete=True` 60/135;
- representative non-finite probes đều `complete=False`;
- prior ten tamper boundaries vẫn fail closed;
- focused suite pass;
- no diff ở producer/notebook/durable artifacts và concurrent 08b work được giữ.

Không chạy lại MiniLM/Notebook vì producer/data flow/artifacts không đổi. Nếu
implementation cần chạm một trong các phần đó, dừng và trả Reviewer để đổi
contract. Git và sub-agent authorization vẫn `none`.

## Approval closure — 2026-08-30 (+07)

Complexity reset và independent final review đã pass; user xác nhận Notebook
08c. Implementation plan này đã hoàn thành. Closure giữ kết luận ba pairings
`eligible=False`, không có reranker finalist/cutover và chuyển lifecycle sang
next-design cho full curated `knowledge-base-hue` coverage. Post-08c corpus,
chunking, embedding/index, Combined Golden Dataset và benchmark work chưa được
authorize bởi plan này.
