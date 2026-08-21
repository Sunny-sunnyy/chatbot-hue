# Implementation Report: Phase 6.1 Baseline Lifecycle Hardening

Implementer: DeepSeek
Date: 2026-08-21
Report path:

```text
reports/phase_6_1_baseline_lifecycle_hardening_implementation_report.md
```

Phase guide context:

```text
guides/phase_0_mvp_foundation.md
guides/phase_6_generation_api.md  # "Milestone 6.1: Baseline Lifecycle Hardening" section
session_prompt/Project_Status.md
```

## Approved Scope

Milestone 6.1 `Baseline Lifecycle Hardening`, status `ready` in
`guides/phase_6_generation_api.md` (design approved by user 2026-08-13).
Move the complete mandatory cold-start work of the retrieval stack into the
FastAPI lifespan: Qdrant read-only preflight -> create/warm E5 with one
internal fixed query -> for hybrid profiles fit BM25 on the real 572 texts ->
for `hybrid_rerank` load MiniLM and run one internal prediction -> publish the
immutable `RetrievalStack` and set `retrieval_ready`. Profile-scoped
behavior, fail-closed failure policy, live-only validation contract.

Implementer-only allowlist (per guide):

```text
backend/core/startup.py
backend/reranking/models/cross_encoder.py
backend/tests/test_startup.py
backend/tests/test_api_chat.py
notebooks/06_generation_and_api.ipynb
reports/phase_6_1_baseline_lifecycle_hardening_implementation_report.md
```

`backend/embedding/embedder.py` and `backend/api/app.py` were NOT modified
(guide explicitly keeps them out of scope: the milestone reuses the existing
`embed_query()` and cached readiness).

## Summary

- `build_retrieval_stack()` now warms the real E5 model via
  `embed_query()` with an internal constant query after config-identity
  verification, for every profile. The shared `BaseEmbedder` validation
  (dimension, finiteness, non-zero norm, L2 normalization) runs on that
  warm-up vector.
- For `hybrid_rerank`, after `load()` the stack runs exactly one MiniLM
  prediction on an internal text pair and raises `ComponentNotReadyError`
  when the score is non-numeric, non-finite or not a single value.
- BM25 fit failure is now wrapped as `ComponentNotReadyError` at the
  lifecycle boundary.
- Cache evidence: the E5 model loads exactly once during
  `build_retrieval_stack`; the first real dense search after a warm build
  adds 0 new model loads.
- Failure paths stay fail-closed with typed errors; no retry, no fallback
  profile/model, no partial stack publish; `/health` remains cached-readiness
  only; `/api/chat` returns 503 when the stack failed.
- Notebook 06 updated to show startup latency, warm-up evidence and cached
  `/health`, still exactly one OpenAI call per Run All.

## Correction After Codex Review (2026-08-21)

Codex review verdict: `changes_requested` (see
`reports/phase_6_1_baseline_lifecycle_hardening_codex_review.md`). Both
major findings were in the notebook; runtime code required no change.

Finding 1 - notebook JSON not valid per nbformat:

- Cause: the previous cleanup pass set `outputs`/`execution_count` on
  markdown cells too (those keys are only valid on code cells), and
  `metadata.execution` plus 11 artifact entries (widget state) remained
  from the real execution.
- Fix: the canonical notebook was rewritten clean: markdown cells carry only
  `cell_type`/`id`/`metadata`/`source`; code cells have `outputs=[]` and
  `execution_count=None`; `metadata.execution`, `metadata.widgets`,
  whole-cell widget state and notebook-level widget/execution keys removed
  (15 artifacts stripped).
- Verification: `nbformat.validate()` passes (`nbformat.validate: OK`);
  code-cell outputs empty, code-cell execution counts null; file size
  12,583 bytes (reviewed state had 22,777 bytes).

Finding 2 - cache evidence only captured after `/api/chat`:

- Fix: evidence is now captured at three boundaries, before and after
  requests, with asserts:
  - Evidence A: right after lifespan startup (before `/health` and
    `/api/chat`);
  - Evidence A2: after `/health` (cached readiness only);
  - Evidence B: after first `/api/chat`.
  - Asserts: E5 and MiniLM cache misses after first retrieval must equal
    the values right after startup; a miss increase fails the notebook
    with a clear message.
- Real notebook execution (output copy outside the repo, canonical left
  clean):

  ```text
  cache evidence AFTER startup (before any request):
    E5 cache:    CacheInfo(hits=0, misses=1, maxsize=4, currsize=1)
    MiniLM cache: CacheInfo(hits=0, misses=0, maxsize=4, currsize=0)
  health status: 200  (status ok, all components ready)
  cache AFTER /health (cached readiness):
    E5 misses: 1 | MiniLM misses: 0
  chat status: 200; elapsed 3.8 s; grounded Vietnamese answer; sources real
  cache evidence AFTER first /api/chat:
    E5 cache:    CacheInfo(hits=1, misses=1)   # misses unchanged
    MiniLM cache: CacheInfo(hits=0, misses=0)  # misses unchanged
  PASS: cache misses unchanged by first retrieval - components were fully
        warm at startup
  startup_seconds: 8.4
  runtime snapshot: {'profile': 'dense_only',
                     'embedding_model': 'intfloat/multilingual-e5-small',
                     'reranker_model': None}
  ```

  `E5 misses=1` right after startup proves the model loaded during the
  lifespan; `hits=1` after first chat proves the request reused that
  loaded model (no new model cache miss). MiniLM stays at 0 for
  `dense_only`, demonstrating profile-scoped warm-up.

New commands run:

```bash
uv run jupyter nbconvert --execute --to notebook --output-dir /tmp/nb06_evidence \
  notebooks/06_generation_and_api.ipynb --ExecutePreprocessor.timeout=900
# single OpenAI call; evidence extracted from /tmp copy

uv run python -c '<nbformat clean + validate script>'
# nbformat.validate: OK; removed 15 keys/artifacts; code cells clean;
# file size 12,583 bytes
```

No runtime regression was found during correction; runtime files are
unchanged since the first implementation.

Full live-only suite re-run after the notebook correction (with
`HF_TOKEN` available in the environment):

```bash
set -a; . .env; set +a
uv run python -m pytest tests/ -q --tb=short -s
# 214 passed in 241.36s; no "unauthenticated requests" warning anymore
# (HF_TOKEN now present); 4 known warnings only (StarletteDeprecation +
# Qdrant version check). OpenAI calls: 5 success + 1 dead-provider attempt,
# estimated cost 0.00097430 + 0.00079055 + 0.00072250 + 0.00080930 +
# 0.00064025 = 0.0039370 USD, no retry. All LIVE CLEANUP ok.
```

Fresh lifecycle latency evidence (cold cache, this run):

```text
LIVE_LOG lifecycle profile=dense_only       startup_ms=12407 first_retrieval_ms=18 documents=10
LIVE_LOG lifecycle profile=hybrid_no_rerank startup_ms=14755 first_retrieval_ms=17 documents=10
LIVE_LOG lifecycle profile=hybrid_rerank    startup_ms=14181 first_retrieval_ms=18 documents=10
```

## Files Created

- `reports/phase_6_1_baseline_lifecycle_hardening_implementation_report.md` - this report.

## Files Modified

- `backend/core/startup.py` - added `E5_WARMUP_QUERY` internal constant,
  `_warm_embedder()` helper (calls `embed_query()` once, wraps failures as
  `ComponentNotReadyError`), call after `_verify_config_consistency()`;
  wrapped BM25 `fit()` failure as `ComponentNotReadyError`; call
  `reranker_instance.warm_up()` after `load()` for `hybrid_rerank`; updated
  `build_retrieval_stack` docstring.
- `backend/reranking/models/cross_encoder.py` - added `WARMUP_QUERY` /
  `WARMUP_DOCUMENT` internal constants and `CrossEncoderReranker.warm_up()`
  (one real prediction, validates single numeric finite score, raises typed
  error otherwise).
- `backend/tests/test_startup.py` - added `make_fresh_embedder()` helper and
  7 tests: E5 warm-up loads the model during build (cache-miss evidence);
  first search after warm build adds no model load; non-rerank profiles
  never load MiniLM; `warm_up()` returns a single finite score; missing
  MiniLM cache fails closed; dead Qdrant URL raises
  `RetrievalDependencyError`; real per-profile startup/first-retrieval
  latency evidence (no hard threshold).
- `backend/tests/test_api_chat.py` - added `TestLifecycleWarmup` (2 tests):
  `hybrid_rerank` lifespan loads E5 and MiniLM before ready; `dense_only`
  lifespan loads E5 and never MiniLM.
- `notebooks/06_generation_and_api.ipynb` - updated intro markdown
  (milestone 6.1 contract, expected results), main cell (startup timing,
  before/after warm-up cache evidence with asserts, cached `/health`
  latency) and checklist. Corrections for the Codex review are documented
  below.

## Notebooks Created Or Modified

- `notebooks/06_generation_and_api.ipynb` - canonical Phase 6 notebook,
  updated for Milestone 6.1. Run All: starts the real app (real lifespan
  against the active collection, read-only), prints startup seconds,
  runtime snapshot (profile/embedding model from the immutable snapshot),
  E5/MiniLM cache evidence, cached `/health` latency, then runs exactly one
  question through the real API path with `gpt-5.4-nano`.
  Expected observations (verified on this machine): `/health` 200 `ok`,
  `startup_seconds` ~7.1 s cold, health calls 1 ms (cached), chat 200 with
  grounded Vietnamese answer + sources, E5 cache `misses=1`, MiniLM cache
  `misses=0` when `active_profile=dense_only`. Committed with empty outputs
  and `execution_count=null`.
  How the user verifies: export `OPENAI_API_KEY`, Run All, compare against
  the checklist in the last markdown cell; evidence lines are printed by the
  cells without printing credentials.

## Commands Run

```bash
# Baseline before changes (env clean, Qdrant up):
cd backend
uv run python -m pytest tests/test_startup.py -q --tb=short
# -> 22 passed in 49.22s

# RED run (new tests, before implementation):
uv run python -m pytest tests/test_startup.py tests/test_api_chat.py -q --tb=short \
  -k "warm_up or no_model_load or never_load or fails_closed or dead_qdrant or LifecycleWarmup"
# -> 5 failed, 3 passed in 61.37s
#   failures: E5 0 loads at build (expected feature missing), 1 new load at
#   first search (expected), warm_up AttributeError (expected), 2 app-level
#   E5-not-loaded-at-startup (expected). 3 guards passed pre-change.

# Compile check:
uv run python -m py_compile core/startup.py reranking/models/cross_encoder.py
# -> OK

# GREEN run:
uv run python -m pytest tests/test_startup.py tests/test_api_chat.py -q --tb=short \
  -k "warm_up or no_model_load or never_load or fails_closed or dead_qdrant or LifecycleWarmup"
# -> 8 passed in 86.37s

# Full live-only backend suite (OPENAI_API_KEY sourced from user .env, never printed):
set -a; . ../.env; set +a
uv run python -m pytest tests/ -q --tb=short -s
# -> 214 passed in 243.81s (4:03)

# Notebook runtime-real execution:
cd . # repo root
uv run jupyter nbconvert --execute --to notebook --inplace notebooks/06_generation_and_api.ipynb \
  --ExecutePreprocessor.timeout=900
# -> success (single OpenAI call); outputs then cleared to empty,
#    execution_count -> null, notebook JSON validated (9 cells):
#    uv run python -c "import json; nb=json.load(open('notebooks/06_generation_and_api.ipynb')); ..."

# CodeGraph:
codegraph status .    # before: up to date; after edits: pending -> synced
codegraph sync .
codegraph status .    # -> ✓ Index is up to date
codegraph affected backend/core/startup.py backend/reranking/models/cross_encoder.py
# -> 5 affected test files: test_api_chat, test_ingestion_pipeline,
#    test_reranker, test_retrieval_service, test_startup (all green in full suite)

# Scope check:
git diff --check     # -> clean
git diff --name-only # -> only the allowlisted files + pre-existing unrelated
                     #    knowledge-base/ deletions from before this session
```

## Tests And Verification

- Baseline green before changes: `test_startup.py` 22 passed.
- RED verified before any production code: 5 failures with the expected
  reasons (feature missing, not typos).
- GREEN after minimal implementation: 8/8 targeted tests.
- Full backend live-only suite: 214 passed, 4 warnings, 0 failures
  (pre-existing `StarletteDeprecationWarning` and Qdrant version-check
  warning only).
- Py_compile clean for both modified runtime modules.
- Notebook executed end-to-end with real runtime: `/health` 200 `ok`
  (qdrant/retrieval ready, generator configured), chat 200, grounded
  Vietnamese answer, real sources, `retrieval_debug` profile `dense_only`,
  1 OpenAI call.
- Failure matrix covered by real states: dead Qdrant URL
  (`RetrievalDependencyError` at stack level; 503 `retrieval_not_ready` at
  API level), collection schema mismatch / wrong dimension / wrong point
  count / duplicated chunk_ids / empty text / payload model mismatch
  (typed `RetrievalConfigurationError`/`ComponentNotReadyError`), MiniLM
  model not in local cache (`ComponentNotReadyError`), E5 dimension
  mismatch with the real embedder (`RetrievalConfigurationError`),
  missing key (503 `generator_not_configured`), dead OpenAI base URL
  (502 `generator_unavailable`), pre-verified production path and
  `verify_snapshot` staleness checks.

### Cache / warm-up evidence (real dependency state)

```text
E5 model cache after build (dense_only): CacheInfo(hits=1, misses=1)   # 1 load at build
First dense search after warm build: 0 additional cache misses
Non-rerank profiles: MiniLM cache misses = 0
hybrid_rerank lifespan: E5 misses >= 1 AND MiniLM misses >= 1 before /health ready
dense_only lifespan:     E5 misses >= 1, MiniLM misses = 0   # profile-scoped
```

### Real latency evidence (cold process cache, this machine, 2026-08-21)

```text
LIVE_LOG lifecycle profile=dense_only       startup_ms=14122 first_retrieval_ms=16 documents=10
LIVE_LOG lifecycle profile=hybrid_no_rerank startup_ms=13951 first_retrieval_ms=18 documents=10
LIVE_LOG lifecycle profile=hybrid_rerank    startup_ms=12278 first_retrieval_ms=16 documents=10
```

An earlier instrumented run showed 9.6-10.9 s per startup at lower disk
load; numbers vary with machine/IO. No hard threshold is asserted (per
guide). First retrieval after warm startup is ~16-18 ms: model loads are
fully out of the request path.

## Evaluation Results

Not applicable. Milestone 6.1 does not add evaluation; retrieval/answer
quality evaluation stays in Phase 7-8.

```text
Retrieval result file: n/a
Answer result file: n/a
Benchmark log updated: no (no benchmark changed)
```

## Deviations From Approved Guide

None.

Guide-level observations recorded (not deviations):

- The local MiniLM `CrossEncoder.predict()` returns raw logits
  (single-label model, no sigmoid applied; verified value 6.218 for the
  internal warm-up pair). `warm_up()` validates a single numeric finite
  score per contract; no 0..1 range is asserted anywhere.
- Notebook startup timing measures lifespan completion (first request after
  context entry); per-profile exact stage timings are reported from the
  live suite evidence above.

## Known Issues

- Cold startup latency ~12-14 s per profile on this machine (E5 load
  ~10 s + MiniLM load/prediction for `hybrid_rerank`), warming the kernel
  cache on later launches. This is the expected cost of the approved
  warm-at-startup contract; no latency gate per guide, numbers reported.
- The internal warm-up constants (`E5_WARMUP_QUERY`, `WARMUP_QUERY`,
  `WARMUP_DOCUMENT`) are Vietnamese words that already exist in the corpus;
  they are constants, never user queries and never logged.
- Pre-existing warnings unchanged: `StarletteDeprecationWarning` (httpx /
  TestClient) and Qdrant server-version check warning. No new warnings
  introduced.
- Notebook 06 cache evidence shows `misses=1` for E5 under
  `active_profile=dense_only` because the notebook reuses the process-level
  model cache; `misses>=1` is the asserted contract, exact count depends on
  prior loads in the same process.

## Security, Data Safety, Reliability, Performance Self-Check

- Security: No secret read, print, log or exposure. `OPENAI_API_KEY` was
  sourced from the user's `.env` for live runs only (never echoed, never
  written to any file or log; the command output does not contain it).
  Notebook still prints only presence. No credential in report, notebook or
  test artifacts.
- Data safety: Active Hue collection `hue_foods_e5_small_384` untouched
  (read-only preflight + read-only queries). All mutations on marked
  `hue_rag_live_test_*` collections, every one cleaned up
  (`LIVE CLEANUP ...: ok` for all, including the shared test collection and
  the final session sweep). Warm-up texts and vectors are never logged;
  no model payloads persisted.
- Reliability: Fail-closed verified with real states; typed exception
  boundaries; no retry/fallback/partial publish; startup failure keeps the
  app alive (`degraded`, chat 503). Import of `api.app` unchanged and still
  side-effect-free. Startup is deterministic and re-runs cleanly.
- Performance: One warm-up embed per startup (not per request), BM25 fit
  once per startup for hybrid profiles, MiniLM one prediction per startup
  for `hybrid_rerank`. Cache evidence proves first retrieval adds 0 model
  loads. No repeated expensive loads, no unbounded work, no new sleeps or
  polling.
- Tests: Full suite uses real dependencies only (real Qdrant, real E5,
  real cached MiniLM, real OpenAI API), failure paths use real states, no
  mocks/fakes/replay. 214 passed.
- Notebooks: Executed for real (real app, real Qdrant, real API call),
  outputs cleared, `execution_count` null, JSON valid, no credential and no
  raw provider payload stored.

## Live Access / Secrets Statement

Live network, model API, Qdrant and model-cache access occurred (approved
by user for this milestone and Live-Only Validation Policy).

- Provider: OpenAI, model `gpt-5.4-nano` via OpenAI Agents SDK.
- Full-suite run: 5 successful generation calls plus 1 real failed-path
  attempt (dead base URL, correctly mapped to 502). Estimated cost from the
  logged usage summaries: `0.00074680 + 0.00081680 + 0.00073250 +
  0.00078305 + 0.00043275 = 0.00351190 USD` (approx. $0.0035), no retries.
- Notebook run: exactly 1 OpenAI call (below 0.001 USD estimated).
- Qdrant: local Docker, one isolated ingestion session +
  per-test marked collections, all cleaned up; active collection read-only.
- E5 and MiniLM loaded from local cache only (notebook sets
  `HF_HUB_OFFLINE=1`; tests use real cache with `local_files_only` for
  MiniLM). E5 warm-up in tests without HF offline flag reported the
  pre-existing unauthenticated-HF warning (no downloads occurred).
- No secrets were read into context, printed, logged or committed.

## Handoff To Codex

Review first:

1. `backend/core/startup.py` - warm-up ordering, exception mapping and
   profile-scoped behavior against the milestone lifecycle contract.
2. `backend/reranking/models/cross_encoder.py` - `warm_up()` single
   prediction and finite-score validation.
3. `backend/tests/test_startup.py` + `test_api_chat.py` - cache-evidence
   assertions (real dependency state) and failure matrix.
4. `notebooks/06_generation_and_api.ipynb` - updated cells, committed clean
   outputs.

Risk areas: cache-miss assertions depend on the real lru_cache wrappers
(`_get_model`, `_get_cross_encoder`) - intentional evidence, not mocks;
MiniLM raw-logit (not sigmoid) semantics; startup latency is machine
dependent (no threshold, measured numbers provided).

Canonical notebook: `notebooks/06_generation_and_api.ipynb`.
Safe-default steps for Codex/user verification:

```bash
# 1. Targeted lifecycle tests (live Qdrant + local models; OpenAI key not required):
cd backend
set -a; . .env; set +a   # ensures key present for the API tests; never prints values
uv run python -m pytest tests/test_startup.py tests/test_api_chat.py -q --tb=short -s

# 2. Full live-only suite (~4 min, ~6 OpenAI calls, ~$0.004):
uv run python -m pytest tests/ -q --tb=short -s

# 3. Notebook from repo root:
uv run jupyter nbconvert --execute --to notebook --inplace notebooks/06_generation_and_api.ipynb
# then verify: outputs empty, execution_count null, JSON valid.

# 4. Scope/codegraph:
codegraph status .   # must say Index is up to date
git diff --check
git diff --name-only
```

Do not modify the user report or guide/README (Codex owns those).
