# Phase 5 Full-corpus Retrieval and Reranking Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking. Do not dispatch sub-agents unless the
> User grants that authority separately.

**Goal:** Triển khai và kiểm chứng hai retrieval treatments cùng optional
MiniLM reranker trên bốn completed Full-corpus Representation A collections,
trả deterministic Top 10 và private technical trace.

**Architecture:** Một module Full-corpus riêng sở hữu readiness, Qdrant
dense/sparse queries, BM25-local ranking, Python RRF và typed result/trace. Nó
tái sử dụng Phase 3 dense/sparse contracts, Phase 4 registry/build records và
model wrapper MiniLM hiện hữu; một CLI nhỏ chạy ma trận local và ghi evidence
đã tách private/tracked. Foods runtime giữ nguyên.

**Tech Stack:** Python 3.13, Sentence Transformers 5.6.1, Transformers 5.14.1,
PyTorch 2.13.0+cu130, PyVi 0.1.1, qdrant-client 1.19.0, Qdrant v1.18.3, pytest,
JSON/SHA-256.

```text
Status: approved by User 2026-09-13 +07
Written Spec: approved by User 2026-09-13 +07
Risk: high
Implementation authorization: none until this Plan and Review Contract are approved
Canonical collections: read-only
Isolated experiment collection creation: allowed after plan approval, only when observed need exists
Collection deletion/replacement/cleanup: none
External corpus/payload upload: none
Git authorization: none
```

## Global Constraints

- Canonical Written Spec:
  `docs/superpowers/specs/2026-09-13-phase-5-full-corpus-retrieval-reranking-written-spec.md`.
- Query exactly four Phase 4 collections; each currently has 8.460 points,
  exact `dense`/`sparse` vector schema and exact five-field payload.
- Load exact Phase 3 state at
  `data/full_corpus_builds/phase_3_sparse_state.json`, SHA-256
  `5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be`;
  do not refit or scroll 8.460 payloads at startup.
- Config axes are only `dense_bm25_rrf|native_hybrid_rrf` and `none|minilm`.
- Candidate depth 30, RRF `k=60`, final depth 10; rank starts at 1 and ties use
  ascending Qdrant point UUID string.
- Baseline BM25 ranks only dense candidates with score `> 0`; native dense and
  sparse branches query Qdrant independently.
- Use two explicit Qdrant branch calls plus the local Python RRF function; do
  not use server fusion or qdrant-client RRF helper.
- MiniLM is `cross-encoder/ms-marco-MiniLM-L-6-v2` on CPU, scores
  `(query, search_text)`, reranks at most 30 into Top 10 and never truncates a
  pair. One overlength pair skips reranking for the whole request.
- No silent fallback. Keep successful empty/zero-signal semantics and mark the
  specified anomalies for Reviewer.
- Return `RetrievalResult(documents, trace)`; do not store trace in service
  mutable state or document metadata.
- Detailed query/point evidence stays ignored under `data/`; tracked artifacts
  contain no query, `search_text`, `evidence_parts`, corpus excerpt, absolute
  path or secret.
- `knowledge-base-hue/`, `qdrant_storage/` and all `data/` remain local and
  ignored. Do not undo the existing staged ignore/untrack changes.
- No ContextBuilder, generation, API/UI, production config, Golden metric,
  finalist/winner, Qwen reranker or Foods feature work.
- No notebook. No plugin framework, registry framework, trace database,
  telemetry service, retry/resume/fallback or speculative validator.
- Do not add dependency or change `pyproject.toml`/`uv.lock`.
- Git authorization is `none`: do not add, commit, push, reset, clean or
  checkout.

---

## File map

| Path | Action | Responsibility |
|---|---|---|
| `backend/retrieval/full_corpus.py` | Create | Types, readiness, dense/BM25/sparse retrieval, RRF and service composition. |
| `backend/reranking/cross_encoder.py` | Modify narrowly | Expose non-mutating score/token-limit primitives while preserving Foods behavior. |
| `backend/retrieval/full_corpus_smoke.py` | Create | Run the private seven-question/16-configuration matrix and write redacted local evidence. |
| `backend/tests/test_full_corpus_retrieval.py` | Create | Pure RRF/BM25/result/trace checks; no system double. |
| `backend/tests/test_retrieval_service.py` | Modify only if needed | Preserve existing real MiniLM/Foods reranker behavior after wrapper change. |
| `data/full_corpus_phase_5_smoke_questions.json` | Create, ignored | Seven private fixed questions, one per P7. |
| `data/full_corpus_phase_5_smoke_trace.json` | Generate, ignored | Detailed real matrix evidence without query/corpus text. |
| `data/full_corpus_phase_5_experiments/*.json` | Optional, ignored | Minimal manifests only for experiment collections actually created. |
| `reports/full_corpus_phase_5_retrieval_reranking_implementation_2026_09_13.md` | Create | Sanitized Implementer report and acceptance map. |
| `session_prompt/CURRENT_HANDOFF.md` | Replace at completion | Compact `final_review` packet required by Implementer workflow. |

Do not modify `backend/config/settings.yaml`, current Foods retrieval files,
ContextBuilder, API/generation/frontend, Phase 2–4 code/contracts, collection
contents, `.gitignore`, `knowledge-base-hue/`, `qdrant_storage/`, build records,
Golden/evaluation artifacts or Reviewer-owned spec/plan/guide files. The only
Reviewer-owned routing file Implementer may replace is `CURRENT_HANDOFF.md` at
the final handoff step.

## Locked public interfaces

Exact internal helper names may stay private. `backend/retrieval/full_corpus.py`
defines:

- `RetrievalTreatment = Literal["dense_bm25_rrf", "native_hybrid_rrf"]`;
- `RerankerMode = Literal["none", "minilm"]`;
- frozen `RetrievalTrace` with fields `candidate_id`, `collection_name`,
  `retrieval_treatment`, `reranker`, `counts`, `timings_ms`, `stages`,
  `rerank_status`, `anomalies` and `classification` (`PASS` or
  `REVIEW_REQUIRED`);
- frozen `RetrievalResult` with `documents: list[RetrievedDocument]` and
  `trace: RetrievalTrace`;
- `reciprocal_rank_fusion(ranked_ids, *, k=60, limit=30)`, returning ordered
  `(point_id, rrf_score)` pairs;
- `FullCorpusRetrievalService.search(query) -> RetrievalResult` and `close()`;
- `build_full_corpus_retrieval_service(candidate_id, retrieval_treatment,
  reranker) -> FullCorpusRetrievalService`.

`counts` and `timings_ms` use aggregate numeric values only. Each row inside
`stages` is allowlisted to `point_id`, `rank` and `score`; branch identity is
the enclosing stage key. No free-form payload dictionary is copied into trace.

`RetrievedDocument` keeps the existing shared schema. For this path,
`id=point UUID`, `text=search_text`, `metadata` contains only
`source/title/heading_path/evidence_parts`, and `score` is RRF or MiniLM score
according to the Written Spec.

The existing `CrossEncoderReranker.rerank()` interface remains compatible.
Only three reusable non-mutating primitives are added: `max_length -> int`,
`input_token_count(query, document) -> int` and
`score_documents(query, documents) -> list[float]`.

## Review Contract

### Risk and independent-review boundary

Risk is `high` because the change executes four real local embedding models,
queries corpus-derived Qdrant payloads, adds a new retrieval boundary and must
prove private evidence does not enter tracked artifacts. Canonical collections
remain read-only, so no separate live-read approval is required after this Plan
is approved.

Reviewer does not repeat the full 112-request/latency run by default. Reviewer
reads the complete Implementer report and local evidence summary, inspects all
changed paths, reruns focused pure tests, then executes a selected real matrix
covering all four dense candidates, both treatments and both reranker modes.
The worst reported MiniLM latency cell is repeated independently when it is
close to or above the 3-second gate, or when raw evidence is inconsistent.

### Required Implementer evidence

1. base/head plus full before/after worktree inventory; preserve staged
   `.gitignore`/264 corpus removals and untracked
   `PROJECT_DOCUMENT_REGISTRY.md`;
2. exact changed paths and immutable-path confirmation;
3. focused RED/GREEN commands for pure RRF, BM25 positive-only ranking, result
   score semantics, trace privacy and wrapper regression;
4. strict readiness for all four exact canonical collections and their local
   Phase 3/4 records;
5. one real run of all seven P7 questions across all 16 configurations;
6. repeated deterministic point-ID/rank evidence and all stage candidate
   counts without private text;
7. MiniLM cold-load observations and at least 20 warm Top-30 observations per
   candidate × retrieval-treatment MiniLM cell, with p95 and exact failures;
8. every matrix cell classified `PASS`, `FAIL` or `REVIEW_REQUIRED`;
9. any anomaly, uncertainty or unexplained observation reported to Reviewer;
10. isolated experiment target/manifest/comparison evidence if any experiment
    collection was created, otherwise an explicit `not used` statement;
11. sanitized tracked report with no private query, payload, per-source list,
    point-level trace, absolute path or secret;
12. failed, skipped, partial and not-verified outcomes preserved exactly.

### Reviewer checks

Minimum independent gate:

```bash
git status --short
git diff --check
git diff -- backend/retrieval/full_corpus.py backend/reranking/cross_encoder.py backend/retrieval/full_corpus_smoke.py backend/tests/test_full_corpus_retrieval.py backend/tests/test_retrieval_service.py
UV_CACHE_DIR=/tmp/hue-rag-phase5-review-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_retrieval.py backend/tests/test_retrieval_service.py -q --tb=short
```

Because new files may be untracked, Reviewer reads them directly and uses
`git diff --no-index /dev/null <path>` where necessary. Reviewer then runs the
smallest real selection that covers four candidates, both treatments and both
reranker modes through `backend.retrieval.full_corpus_smoke`; exact selector is
taken from the CLI implemented in Task 4. No mock/fake/stub result counts as
integration evidence.

Reviewer also verifies:

- Qdrant collections/build records were not mutated;
- dense query preprocessing matches each Phase 3 candidate;
- sparse query and BM25-local both use the exact loaded Phase 3 state;
- two native branches are independent Qdrant calls;
- RRF formula/tie-break/depth and score semantics are exact;
- overlength skips the whole reranker request without truncation;
- tracked artifacts contain no private corpus/query material;
- no compatibility framework, duplicate model registry or unnecessary test
  machinery was added;
- every `FAIL`/`REVIEW_REQUIRED` is resolved before technical PASS.

Findings use `blocker`, `major`, `minor`. Verdict is one of
`ready_for_user_confirmation`, `changes_requested`, `blocked`. Reviewer writes
`reports/full_corpus_phase_5_retrieval_reranking_codex_review_2026_09_13.md`.
User closure is still required after technical PASS.

---

### Task 1: Typed result, trace and exact RRF

**Files:** Create `backend/retrieval/full_corpus.py` and
`backend/tests/test_full_corpus_retrieval.py`.

**Produces:** `RetrievalTrace`, `RetrievalResult`, configuration literals and
`reciprocal_rank_fusion()` from the locked interfaces.

- [ ] **Step 1: Inventory the dirty worktree and record immutable baselines**

Run:

```bash
git status --short
git diff --cached --stat
git diff --name-only
```

Expected: existing staged `.gitignore` plus 264 cached corpus removals remain;
`PROJECT_DOCUMENT_REGISTRY.md` remains untracked. Do not stage or modify them.

- [ ] **Step 2: Write focused failing RRF/result tests**

Use these exact behavior cases:

```python
def test_rrf_uses_k_60_rank_from_one_and_point_id_tie_break():
    assert reciprocal_rank_fusion([["b", "a"], ["a", "b"]]) == [
        ("a", 1 / 61 + 1 / 62),
        ("b", 1 / 61 + 1 / 62),
    ]


def test_rrf_one_branch_preserves_branch_order():
    assert [point_id for point_id, _ in reciprocal_rank_fusion([["c", "a", "b"]])] == [
        "c", "a", "b"
    ]


def test_rrf_unions_branches_limits_output_and_rejects_malformed_branch():
    ranked = reciprocal_rank_fusion([["a", "b"], ["b", "c"]], limit=2)
    assert len(ranked) == 2
    assert len({point_id for point_id, _ in ranked}) == 2
    with pytest.raises(ValueError, match="duplicate"):
        reciprocal_rank_fusion([["a", "a"]])
```

Also construct a `RetrievalTrace` and assert its serialized field names do not
include `query`, `search_text`, `evidence_parts`, `text` or absolute paths.

- [ ] **Step 3: Run RED**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase5-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_retrieval.py -q --tb=short
```

Expected: FAIL because the module/interfaces do not exist.

- [ ] **Step 4: Implement the smallest deterministic core**

Implement the locked dataclasses/literals and RRF directly. Required RRF loop:

```python
scores: dict[str, float] = {}
for branch in ranked_ids:
    seen: set[str] = set()
    for rank, point_id in enumerate(branch, start=1):
        if point_id in seen:
            raise ValueError(f"duplicate point ID within one branch: {point_id}")
        seen.add(point_id)
        scores[point_id] = scores.get(point_id, 0.0) + 1.0 / (k + rank)
return sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:limit]
```

Reject non-positive `k`/`limit` and non-string/empty point IDs. Do not add a
generic scorer/fusion base class.

- [ ] **Step 5: Run GREEN**

Run the Task 1 command. Expected: all new pure tests PASS.

### Task 2: Strict readiness and two real retrieval treatments

**Files:** Modify `backend/retrieval/full_corpus.py` and
`backend/tests/test_full_corpus_retrieval.py`.

**Consumes:** Phase 3 `DENSE_MODEL_SPECS`, `FullCorpusDenseRunner`,
`encode_sparse_query()`, `encode_sparse_document()`; Phase 4
`FULL_CORPUS_CANDIDATES`, build records and Qdrant schema validator.

**Produces:** `FullCorpusRetrievalService.search()` for both treatments before
optional reranking and `build_full_corpus_retrieval_service()`.

- [ ] **Step 1: Add failing pure behavior tests**

Add exact checks that:

```python
positive = rank_positive_bm25([("a", 0.0), ("b", 2.0), ("c", 1.0)])
assert positive == ["b", "c"]
assert rank_positive_bm25([("a", 0.0), ("b", 0.0)]) == []
```

Use a tiny real `SparseState` value to prove the local sparse dot product gives
positive score only for a matching document and zero otherwise. Assert the
input documents/payload dictionaries are not mutated. These are pure math/data
checks, not claimed Qdrant integration evidence.

- [ ] **Step 2: Run RED, then implement readiness and retrieval**

Run the Task 1 pytest command; expect the new tests to fail first.

Implementation must:

1. resolve the candidate only through Phase 4 `candidate_by_id()`;
2. read the matching ignored build record and sparse-state bytes without
   logging their private `corpus.sources` mapping;
3. compare schema/status/candidate/dimension/count/corpus/sparse identities;
4. validate live Qdrant dense+sparse schema and exact count;
5. resolve/load the candidate's pinned snapshot and warm one real query;
6. issue dense Top30 with exact five payload fields;
7. for baseline, encode the query once, encode only returned `search_text`
   candidates and use sparse dot product as the exact local BM25 score;
8. for native hybrid, issue a second independent sparse Top30 query unless the
   encoded sparse query is empty;
9. validate returned IDs, finite scores and five payload field types;
10. fuse exact ranked IDs, create fresh `RetrievedDocument` values and record
    counts/ranks/scores/timings in a trace containing no text;
11. mark `bm25_zero_matches`, `sparse_query_no_vocabulary_tokens`,
    `sparse_zero_hits` or `dense_zero_hits` when observed;
12. surface typed input/config/not-ready/dependency errors; never return `[]`
    for an exception.

Use Qdrant `models.SparseVector` with exact Phase 3 indices/values. Do not call
`prepare_full_corpus_input()`, scan `knowledge-base-hue/`, scroll collection
payloads or recompute corpus identity in the request/startup path.

- [ ] **Step 3: Run GREEN and focused Phase 3–4 regressions**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase5-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_retrieval.py backend/tests/test_full_corpus_sparse.py backend/tests/test_full_corpus_qdrant_ingestion.py -q --tb=short
```

Expected: PASS. This proves pure/shared contracts only; live Qdrant evidence is
Task 4.

### Task 3: Non-mutating MiniLM primitives and optional Top30 rerank

**Files:** Modify `backend/reranking/cross_encoder.py`,
`backend/retrieval/full_corpus.py`, `backend/tests/test_full_corpus_retrieval.py`
and only if necessary `backend/tests/test_retrieval_service.py`.

**Produces:** public `max_length`, `input_token_count()` and
`score_documents()` primitives; `none|minilm` behavior in Full-corpus service.

- [ ] **Step 1: Add failing checks for wrapper and service semantics**

Required cases:

- `score_documents()` returns exactly one finite float per input and leaves
  input documents unchanged;
- existing Foods `rerank()` still returns fresh documents with its historical
  metadata behavior;
- `none` returns RRF Top10 and never loads/calls MiniLM;
- MiniLM scores at most 30 `(query, doc.text)` pairs, sorts score descending
  then point ID ascending, sets final `RetrievedDocument.score`, and keeps
  stage scores only in trace;
- one token count above `max_length` yields
  `rerank_status=skipped_overlength`, preserves RRF order/score and makes no
  scoring call;
- scoring count/type/non-finite failure raises the existing typed dependency
  error.

Pure validation can use direct numeric lists. MiniLM availability and scoring
must be checked with the real local model; do not monkeypatch `_predict` or use
a fake scorer.

- [ ] **Step 2: Run RED and implement the narrow wrapper extension**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase5-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_retrieval.py backend/tests/test_retrieval_service.py::test_cross_encoder_rerank_contract_and_non_mutation -q --tb=short
```

Expected before implementation: new interface tests FAIL while the existing
Foods test remains a baseline.

Use the loaded CrossEncoder tokenizer with `truncation=False` to count the
complete pair. `score_documents()` delegates to the existing validated batch
prediction; `rerank()` reuses it so there is one scoring implementation.

- [ ] **Step 3: Run GREEN and existing Foods regression**

Run the Task 3 command, then:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase5-uv-cache uv run --env-file .env python -m pytest backend/tests/test_retrieval_service.py -q --tb=short
```

Expected: PASS; existing Foods behavior remains unchanged.

### Task 4: Private seven-question matrix and real local evidence

**Files:** Create `backend/retrieval/full_corpus_smoke.py`, ignored question and
trace JSON files, and optional ignored experiment manifests only if used.

**Produces:** one CLI with `preflight`, `run` and bounded `--select` modes.

- [ ] **Step 1: Create the private question file**

Create a JSON list of exactly seven objects. Every object has only
`query_id`, `partition` and `question`. IDs are `P5-Q01` through `P5-Q07` in
this exact P7 order: `foods`, `heritages`, `festivals`, `performing_arts`,
`travel_places`, `travel_services`, `travel_tickets`. Author one non-empty,
natural Vietnamese question grounded in the corresponding local partition;
do not copy the question into a tracked file. Confirm `git check-ignore`
matches the file before adding its private values.

- [ ] **Step 2: Implement the direct matrix CLI**

The CLI must:

- validate exact seven IDs/partitions with non-empty questions;
- preflight all four candidate collection/state/model contracts;
- iterate candidates sequentially and close each service/model in `finally`;
- run all four configuration combinations and seven queries;
- rerun the seven-query sequence to compare deterministic final IDs/scores;
- for each MiniLM cell, collect at least 20 warm Top30 reranker observations
  by repeating the fixed sequence in deterministic order;
- measure cold load separately and compute p95 from raw warm observations;
- continue independent cells after a cell failure;
- classify each cell `PASS`, `FAIL` or `REVIEW_REQUIRED`;
- write JSON atomically to the ignored trace path;
- omit question text and all document/payload text from output;
- exit non-zero when any cell is `FAIL` or `REVIEW_REQUIRED`.

`--select` accepts explicit candidate/treatment/reranker/query IDs for bounded
Reviewer reruns. It must use the same production service path, not alternate
smoke logic.

- [ ] **Step 3: Run real read-only preflight**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase5-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke preflight --questions data/full_corpus_phase_5_smoke_questions.json
```

Expected: all four canonical collections/state/model contracts report ready;
no collection write occurs. Any mismatch is preserved and reported to Reviewer.

- [ ] **Step 4: Run the full real matrix**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase5-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke run --questions data/full_corpus_phase_5_smoke_questions.json --output data/full_corpus_phase_5_smoke_trace.json
```

Expected for closure: 16 configuration cells, seven questions per cell,
deterministic repeats, MiniLM warm p95 `≤ 3000 ms` in all eight MiniLM cells,
and no unresolved `FAIL`/`REVIEW_REQUIRED`.

If a zero lexical/sparse signal or any other unexplained behavior appears,
finish safe independent cells, preserve the local evidence and stop before
claiming Phase PASS. Send Reviewer the exact redacted cell/config/counts/error.

- [ ] **Step 5: Handle experiment collections only when evidence requires one**

Default is no experiment collection. If diagnosis requires one, resolve and
record an absent semantic target before write, keep canonical/Foods targets
immutable, write one ignored minimal manifest and report baseline versus the
single main changed variable. Do not delete it. A failed/mismatched existing
target is reported rather than replaced.

### Task 5: Focused regression, privacy review and Implementer report

**Files:** All changed paths; create the tracked implementation report; replace
`session_prompt/CURRENT_HANDOFF.md` only after self-review/evidence is complete.

- [ ] **Step 1: Run final focused checks**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase5-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_retrieval.py backend/tests/test_full_corpus_sparse.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_retrieval_service.py -q --tb=short
git diff --check
```

Expected: PASS. Do not run the full backend suite unless an observed changed
dependency or failure expands the actual blast radius.

- [ ] **Step 2: Self-review scope, simplicity and privacy**

Inspect every changed/untracked file. Confirm:

- data flow can be followed directly from service to dense/BM25-or-sparse,
  RRF, optional MiniLM and result;
- no duplicate model/collection registry, generic strategy hierarchy, mutable
  trace cache, retry/fallback or test-only runtime hook exists;
- original Foods inputs/results are not mutated;
- canonical and experimental Qdrant target actions match authorization;
- no ignored private content appears in a tracked path or Git diff;
- existing unrelated staged/untracked user changes are untouched.

- [ ] **Step 3: Write the implementation report**

Use these sections:

```text
## Authority and repository state
## Changed paths and responsibilities
## RED/GREEN focused checks
## Four-collection readiness
## Seven-question / 16-configuration matrix
## Determinism and stage counts
## MiniLM cold and warm latency
## Anomalies and Reviewer-required items
## Experiment collections and comparisons
## Privacy and immutable-path evidence
## Acceptance mapping
## Failed, skipped and not verified
## Limitations and Reviewer handoff
```

Do not copy questions, point rows, payload text, per-source lists or absolute
paths into the report. The report is evidence, not approval.

- [ ] **Step 4: Write the compact final-review handoff and stop**

Replace `session_prompt/CURRENT_HANDOFF.md` with `Target role: reviewer`,
`Handoff kind: final_review` and one next action: independently review this
Phase 5 implementation. Include base/head, exact changed paths, acceptance
mapping, command/result summary, anomaly/deviation status, implementation
report path, ignored trace path, exact Reviewer reruns and Git state. Do not
copy private questions or payload text into the handoff.

Do not update the Written Spec, Plan, guide, Project Status, Codex review or
user report. Do not commit/push. Give the user the standard four-file Reviewer
bootstrap prompt; no extra next-session prompt is needed.

## Spec coverage and simplicity check

| Written Spec area | Plan coverage |
|---|---|
| Four collections, 16 configurations, one service/config | Tasks 2 and 4 |
| BM25 positive-only baseline and native independent sparse | Task 2 |
| Exact Python RRF/depth/tie-break | Task 1 |
| MiniLM Top30→Top10, overlength, latency | Tasks 3 and 4 |
| RetrievalResult/private trace/final score | Tasks 1–3 |
| Strict readiness/no fallback | Task 2 |
| General anomaly escalation | Task 4 and Review Contract |
| Local corpus/Qdrant privacy | Global constraints, Tasks 4–5 |
| Optional isolated experiments | Task 4 |
| Real verification without quality claims | Task 4 |
| Phase 6/8 and Qwen deferral | Global constraints and stop boundary |

This Plan intentionally uses one Full-corpus retrieval module, one narrow
extension to the current MiniLM wrapper, one smoke CLI and one focused test
file. It does not add a framework, notebook or persistence layer.

## Approval effect

User approval of this Plan and Review Contract authorizes one Implementer effort
for Tasks 1–5, real read-only queries against the four canonical collections,
real local dense/MiniLM model execution, and absent-target experiment collection
creation only when observed diagnosis needs it. It does not authorize mutation
of any existing collection, cleanup/delete, external corpus upload, production
cutover, Qwen reranker, Git commit or push.
