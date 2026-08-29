# Phase 8 — Notebook 08a Dense Embedding Benchmark Implementation Plan

**Status:** `ready_for_implementation`. User approved this exact plan and
authorized its amended real local Run All on `2026-08-28 +07`. Authorization is limited
to the approved 08a files, pinned local model downloads, four isolated Qdrant
collections and the durable 08a CSV; it excludes paid calls, active collection
mutation, production cutover and later Notebook 08 groups.

> **For Implementer:** Start with `using-superpowers`. Read and apply
> `/home/minhhieu/hue_rag/skills/practical-project-coding/SKILL.md`, execute this
> plan task by task, use `verification-before-completion` before reporting, and
> use `requesting-code-review` for the handoff. Do not commit or push.

**Goal:** Implement one educational Notebook 08a and the smallest reusable
backend needed to benchmark the four approved local dense vector spaces on the real
Hue food corpus without changing production retrieval behavior.

**Architecture:** Keep native model loading and encoding in one small embedding
module. Keep canonical input loading, isolated Qdrant lifecycle, exact metrics,
gates, timings, resource observations and CSV persistence in one evaluation
module. The notebook is presentation and orchestration only: one explicit cell
for the E5-small control, then one sequential loop cell for the three authorized candidates.

The local execution amendment at the end supersedes every earlier
five/seven-model and Qwen/1024D local instruction retained as history.

**Tech stack:** Python 3.13, uv, PyTorch CPU FP32, SentenceTransformers 5.6.1,
Transformers 5.14.1, PyVi 0.1.1, Qdrant client 1.19.0, NumPy,
Polars, the already-resolved psutil package, pytest and Jupyter.

**Approved design:**
`docs/superpowers/specs/2026-08-28-phase-8-08a-embedding-benchmark-design.md`

**Hard boundary:** Change only the files listed in the approved design. Preserve
all pre-existing worktree changes. Do not edit the production E5 embedder,
settings/profiles, Golden Dataset V3, BM25, reranker, generation, guides, status
files or Reviewer reports. Do not add a registry, validator framework, audit
package, run identity, resume mechanism, mock integration or fallback path.

---

## Task 0: Reconfirm authority and establish a read-only baseline

**Files:**

- Read: `session_prompt/Session_Prompt.md`
- Read: `session_prompt/Project_Status.md`
- Read: `docs/superpowers/specs/2026-08-28-phase-8-08a-embedding-benchmark-design.md`
- Read: `docs/superpowers/plans/2026-08-28-phase-8-08a-embedding-benchmark-implementation-plan.md`
- Do not modify anything in this task

**Step 1: Record the exact authorization**

The user authorized the exact Notebook 08a implementation and real local Run
All on `2026-08-28 +07`. Record that authority in the implementation report.
Do not expand it to paid calls, active collection mutation, production cutover,
GPU work or later Notebook 08 groups.

**Step 2: Capture the dirty worktree without changing it**

Run:

```bash
git status --short
git diff -- docs/superpowers/specs/2026-08-28-phase-8-08a-embedding-benchmark-design.md
git diff -- docs/superpowers/plans/2026-08-28-phase-8-08a-embedding-benchmark-implementation-plan.md
```

Expected: unrelated modified/untracked files may already exist. Record them in
the implementation report and do not stage, restore or rewrite them.

**Step 3: Confirm production state before implementation**

Run:

```bash
rg -n "active_profile|collection_name|vector_size|retrieval_mode|use_bm25|use_reranker" backend/config/settings.yaml
```

Expected: active profile remains `dense_only`; production collection remains
`hue_foods_e5_small_384`; the three existing profile definitions are unchanged.

---

## Historical Task 1 — cancelled: do not add or retain FlagEmbedding for local 08a

The commands below are retained only as superseded history. Current local scope
uses pinned PyVi for Huydang DEk21 preprocessing and removes `FlagEmbedding`
when no other authorized local consumer remains.

**Files:**

- Modify: `pyproject.toml`
- Modify: `uv.lock`

**Step 1: Add the exact pin**

Run from repository root:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-implement-uv-cache uv add "FlagEmbedding==1.4.0"
```

Expected: `pyproject.toml` contains the exact direct dependency and `uv.lock`
resolves it without changing the approved Python/model stack to an incompatible
version. Do not create a second environment or notebook install cell.

**Step 2: Verify the resolved versions**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-implement-uv-cache uv run python -c "import importlib.metadata as m; print({p: m.version(p) for p in ['FlagEmbedding', 'sentence-transformers', 'transformers', 'torch', 'qdrant-client']})"
```

Expected: FlagEmbedding is `1.4.0`; the other versions remain compatible with
the versions recorded in the design. If resolution or Python 3.13 import fails,
stop and reopen the design. Do not silently choose another release.

**Step 3: Inspect the installed BGE-M3 path before coding the adapter**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-implement-uv-cache uv run python -c "import inspect; from FlagEmbedding import BGEM3FlagModel; print(inspect.getsourcefile(BGEM3FlagModel)); print(inspect.signature(BGEM3FlagModel)); print(inspect.signature(BGEM3FlagModel.encode))"
```

Then read the installed 1.4.0 implementation of `BGEM3FlagModel.encode`, its
single-device encoding helper, tokenizer call and underlying model forward.
Expected: the exact internal path can produce `dense_vecs` while caller-owned
batches remain fixed. If the needed stable objects are absent, stop with
`blocked`; do not use the public auto-shrinking loop or a substitute model.

---

## Task 2: Implement native dense model runners

**Files:**

- Create: `backend/embedding/dense_benchmark.py`

There are intentionally no mocked model tests. Native encoding is accepted only
through the real Run All and Reviewer's independent model checks.

**Step 1: Define the immutable setting and result contracts**

Create these public shapes:

```python
from dataclasses import dataclass
from typing import Literal

RunnerKind = Literal["sentence_transformer", "huydang"]
InputContract = Literal["e5", "minilm", "pyvi_segmented"]


@dataclass(frozen=True)
class DenseBenchmarkSetting:
    order: int
    setting_key: str
    setting_label: str
    model_id: str
    revision: str
    dimension: int
    max_length: int
    collection_name: str
    runner_kind: RunnerKind
    input_contract: InputContract
    truncate_dim: int | None = None
    retrieval_mode: str = "dense"
    use_bm25: bool = False
    use_reranker: bool = False


@dataclass(frozen=True)
class DocumentEmbeddingResult:
    vectors: list[list[float]]
    truncated_document_count: int
```

Do not add a registry. Define the four local constants directly in approved order,
then expose:

```python
E5_SMALL_SETTING: DenseBenchmarkSetting
DENSE_CANDIDATE_SETTINGS: tuple[DenseBenchmarkSetting, ...]
ALL_DENSE_SETTINGS: tuple[DenseBenchmarkSetting, ...]
```

Copy every model ID, revision, dimension, maximum length, label and isolated
collection name exactly from the approved design.

**Step 2: Implement shared observable behavior without a base framework**

Each of `SentenceTransformerDenseRunner` and `HuydangDenseRunner` exposes only:

```python
model_id: str
dimension: int
load() -> None
embed_documents(texts: list[str]) -> DocumentEmbeddingResult
embed_query(question: str) -> list[float]
close() -> None
```

Required invariants:

- lazy load only when `load()` or encoding is called;
- CPU only, FP32 only, no quantization;
- document batches exactly 8 and query batches exactly 1;
- no catch-and-retry, batch shrink, fallback model, device switch or revision
  change;
- token lengths are counted on the exact prepared text before truncation;
- native model paths perform L2 normalization in the approved position, then a
  shared helper validates that all returned vectors are finite, exact-dimension
  and unit norm rather than silently repairing invalid output;
- `close()` drops model/tokenizer references, invokes `gc.collect()`, and calls
  `torch.cuda.empty_cache()` only when CUDA is actually present; it does not
  mutate Qdrant or production configuration.

Use one small private normalization/check helper; do not introduce an abstract
base class or plugin mechanism.

**Step 3: Implement SentenceTransformers E5 and MiniLM contracts**

Load with the pinned `revision`, `device="cpu"` and the approved maximum
sequence length. For E5, prepare `passage: {text}` and `query: {question}`. For
MiniLM, pass raw text and raw question. Encode documents with `batch_size=8`,
queries with `batch_size=1`, `precision="float32"`,
`normalize_embeddings=True`, and convert the resulting NumPy values to ordinary
Python lists.

Do not reuse production `E5Embedder`: it has batch size 64 and does not expose
revision/max-length/truncation evidence. Do not change that production class.

**Historical Step 5 — cancelled: do not implement or retain the local BGE-M3 adapter**

The text below records the superseded design only. The current resource
amendment prohibits local BGE-M3 download/execution and requires removal of the
unused local adapter/dependency.

Load `BGEM3FlagModel` at the exact revision on CPU with FP32 behavior. Keep the
public class for loading/tokenizer/model ownership, but do not call its public
batch loop because it catches runtime errors and shrinks batch size.

Because `BGEM3FlagModel` does not provide the same `revision=` loading contract
as SentenceTransformers, resolve the approved BGE repository with
`huggingface_hub.snapshot_download(repo_id=setting.model_id,
revision=setting.revision)` and pass that pinned local snapshot path to
`BGEM3FlagModel`. Do not load a moving branch.

Implement one private `_encode_exact_batch(texts)` based on the installed 1.4.0
source inspected in Task 1. For each caller-owned batch, it must:

1. tokenize once with `max_length=512`, padding and truncation;
2. move that tokenized batch to CPU;
3. invoke the official underlying M3 model once requesting dense output only;
4. read `outputs["dense_vecs"]` (or the exact typed equivalent exposed by
   1.4.0);
5. return that batch without a retry loop.

Use the underlying official pooling and normalization; do not reimplement M3
pooling. Query input is raw and uses one-item batches. If a RuntimeError/OOM
occurs, let it escape immediately so orchestration records the exact failure.

**Step 6: Add the direct factory**

```python
def build_dense_runner(setting: DenseBenchmarkSetting):
    if setting.runner_kind == "sentence_transformer":
        return SentenceTransformerDenseRunner(setting)
    if setting.runner_kind == "huydang":
        return HuydangDenseRunner(setting)
    raise ValueError(f"unsupported runner kind: {setting.runner_kind}")
```

This explicit branch is the full supported set. Do not add dynamic registration,
entry points, YAML model catalogs or duplicate configurations.

**Step 7: Verify import and static contracts offline**

Run from `backend/`:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-test-uv-cache uv run python -c "from embedding.dense_benchmark import ALL_DENSE_SETTINGS, DENSE_CANDIDATE_SETTINGS, E5_SMALL_SETTING; assert len(ALL_DENSE_SETTINGS) == 4; assert E5_SMALL_SETTING.order == 1; assert len(DENSE_CANDIDATE_SETTINGS) == 3; assert len({s.collection_name for s in ALL_DENSE_SETTINGS}) == 4; print('dense setting contracts: PASS')"
```

Expected: `dense setting contracts: PASS` without loading any model.

---

## Task 3: Build exact deterministic scoring and aggregation test-first

**Files:**

- Create: `backend/tests/test_embedding_benchmark.py`
- Create: `backend/evaluation/embedding_benchmark.py`

**Step 1: Write failing tests for source + section scoring**

Use real `GoldenCase` and `RetrievedDocument` value objects, not mocks. Include:

- relevant source with wrong section is not relevant;
- relevant section at ranks 2 and 5 produces exact MRR/Recall/nDCG;
- two chunks from the same relevant source + section receive credit once;
- no relevant result gives all zeros and `hit=False`;
- Top 6 cannot affect Top-5 metrics.

The key fixture should resemble:

```python
def retrieved(rank: int, source: str, section: str) -> RetrievedDocument:
    return RetrievedDocument(
        id=f"chunk-{rank}",
        score=1.0 / rank,
        text="safe test text",
        metadata={"chunk_id": f"chunk-{rank}", "source": source, "section": section},
    )
```

Run:

```bash
cd backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-test-uv-cache uv run --env-file ../.env python -m pytest tests/test_embedding_benchmark.py -q --tb=short
```

Expected: FAIL because the scoring functions do not exist.

**Step 2: Implement the smallest scoring API**

Define:

```python
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


def score_retrieval_case(
    case: GoldenCase,
    documents: list[RetrievedDocument],
    *,
    k: int = 5,
) -> CaseMetrics:
    ...
```

Build declared relevance from the case's canonical evidence. Use
`document_is_relevant` for the exact repository mapping. Give a relevant
`(source, section)` pair gain 1 only on its first appearance in the ranked Top
5; later duplicates get gain 0. Compute:

```python
recall = credited_relevant_pairs / len(declared_relevant_pairs)
mrr = 1.0 / first_credited_rank if any_credit else 0.0
dcg = sum(gain / math.log2(rank + 1) for rank, gain in enumerate(gains, 1))
idcg = sum(1.0 / math.log2(rank + 1) for rank in range(1, min(k, relevant_count) + 1))
ndcg = dcg / idcg
```

Reject empty declared evidence rather than divide by zero.

**Step 3: Write failing aggregation tests**

Cover one overall row plus exact category rows, arithmetic means, hit-case
counts and case counts. Assert categories are deterministic and no missing or
extra category is synthesized.

Expected after running the focused test command: FAIL because aggregation is
not implemented.

**Step 4: Implement aggregation**

Define:

```python
def aggregate_case_metrics(
    case_metrics: list[CaseMetrics],
) -> dict[str, dict[str, int | float]]:
    ...
```

Return `overall` followed by sorted observed categories. Overall/category
quality must be derived from repetition one only; the orchestration layer is
responsible for passing those first-repetition rows.

**Step 5: Run the focused tests**

Run the command from Step 1. Expected: scoring and aggregation tests PASS.

---

## Task 4: Implement bootstrap, guardrails and finalist decisions test-first

**Files:**

- Modify: `backend/tests/test_embedding_benchmark.py`
- Modify: `backend/evaluation/embedding_benchmark.py`

**Step 1: Write failing guardrail tests**

Cover all three rules explicitly:

- n>=6 fails when candidate hit count is lower;
- n>=6 with tied hits fails when delta nDCG@5 is below -0.02;
- n<=3 fails when any reference-hit case becomes a candidate miss;
- protected categories that satisfy their applicable rule pass.

Use the actual V3 category sizes as boundary examples: `relationship` (14),
`direct_fact` (7), `comparative` (6), `holistic` (3), `numerical` (2) and
`temporal` (1).

**Step 2: Implement guardrails**

Define:

```python
def evaluate_category_guardrails(
    reference: list[CaseMetrics],
    candidate: list[CaseMetrics],
) -> dict[str, bool]:
    ...
```

Require exact matching case IDs and categories before comparing. Return one
boolean for every observed category. Do not average away a small-category lost
case.

**Step 3: Write failing paired-bootstrap tests**

Use 45 deterministic pairs. Assert:

- two calls with 10,000 samples and seed 42 are identical;
- identical arrays return delta and both CI bounds equal to zero;
- a constant positive delta returns that exact positive delta at both bounds;
- mismatched case IDs or lengths raise.

**Step 4: Implement paired bootstrap**

Define:

```python
@dataclass(frozen=True)
class BootstrapInterval:
    delta: float
    lower: float
    upper: float


def paired_bootstrap_intervals(
    reference: list[CaseMetrics],
    candidate: list[CaseMetrics],
    *,
    samples: int = 10_000,
    seed: int = 42,
) -> dict[str, BootstrapInterval]:
    ...
```

Pair by case ID in canonical order. Resample paired row indices, compute the
candidate-minus-reference mean for Recall/MRR/nDCG, and use NumPy percentiles
2.5 and 97.5. Do not resample candidate/reference independently.

**Step 5: Write failing decision tests**

Cover:

- status not completed or repetitions not 3 rejects clear gain;
- any category failure rejects clear gain;
- delta nDCG exactly 0.03 is allowed;
- lower CI exactly 0 is rejected;
- the best earlier survivor uses nDCG, then MRR, then Recall, then approved
  order;
- E5-small is the initial lighter reference;
- a heavier survivor that does not clearly beat its best lighter finalist
  keeps the lighter finalist preferred.

**Step 6: Implement decisions directly**

Define small functions, not a rules engine:

```python
def has_clear_gain(
    *,
    status: str,
    successful_repetitions: int,
    guardrails: dict[str, bool],
    ndcg_interval: BootstrapInterval,
) -> bool:
    return (
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
    ...
```

Do not create a composite score.

**Step 7: Run focused tests**

Run the Task 3 command. Expected: metric, aggregation, guardrail, bootstrap and
decision tests PASS.

---

## Task 5: Implement durable long-format CSV upsert test-first

**Files:**

- Modify: `backend/tests/test_embedding_benchmark.py`
- Modify: `backend/evaluation/embedding_benchmark.py`

**Step 1: Write failing CSV tests with `tmp_path`**

Assert:

- first write creates exactly `overall` plus the nine category rows;
- rerunning the same setting replaces matching `(setting_key, category)` rows;
- rows for another setting are preserved;
- columns exactly match the approved ordered list;
- output ordering is stable by approved setting order, then `overall`, then
  category name;
- category rows leave run-level latency/RSS and aggregate comparison fields
  blank, while retaining their own quality values, metric deltas and
  `category_guardrail_pass`;
- a failed setting retains exact status and sanitized error.

**Step 2: Implement exact ordered schema and upsert**

Expose:

```python
EMBEDDING_RESULTS_PATH = REPO_ROOT / "evaluation/results/phase8_embedding_results.csv"
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


def upsert_embedding_results_csv(
    rows: list[dict[str, object]],
    *,
    path: Path = EMBEDDING_RESULTS_PATH,
) -> Path:
    ...
```

Read an existing file when present, replace only matching
`setting_key + category`, validate exact known columns, sort deterministically,
create only the existing `evaluation/results` parent if necessary, and write one
CSV. Do not add JSON, timestamps, run IDs, manifests or history files.

Candidate `overall` rows carry aggregate deltas, bootstrap CIs,
`all_category_guardrails_pass`, both clear-gain decisions, best-lighter key and
finalist eligibility. Candidate category rows carry category metrics, simple
candidate-minus-control metric deltas and `category_guardrail_pass`; aggregate
CI/final-selection fields stay blank there. Control delta, CI and comparison
fields stay blank, while a completed 3/3 control may still be
`finalist_eligible=true`.

**Step 3: Sanitize errors at the boundary**

Implement:

```python
def sanitize_benchmark_error(exc: Exception) -> str:
    root = exc
    while root.__cause__ is not None:
        root = root.__cause__
    message = " ".join(str(root).split())
    return f"{type(root).__name__}: {message[:500]}"
```

Before persistence/display, additionally redact URL query strings, authorization
or API-key-like fields and raw headers. Never persist traceback text or provider
payloads.

**Step 4: Run focused tests**

Run the Task 3 command. Expected: all deterministic tests PASS with no model
load and no Qdrant mutation.

---

## Task 6: Implement canonical inputs, collection safety and one-setting lifecycle

**Files:**

- Modify: `backend/evaluation/embedding_benchmark.py`

Do not write mocked integration tests. Verify this path with real models and
real isolated Qdrant only in Task 9.

**Step 1: Define the notebook-facing data contracts**

Expose compact dataclasses with ordinary displayable fields:

```python
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
```

Keep measurement details in `summary`; do not introduce a generic event or
artifact hierarchy.

**Step 2: Load and validate canonical inputs**

Implement:

```python
def load_embedding_benchmark_inputs() -> EmbeddingBenchmarkInputs:
    cases = load_golden(V3_FULL_PATH)
    validate_v3_full(cases)
    chunks = chunk_foods_markdown()
    chunk_ids = validate_chunks(chunks)
    if len(cases) != 45:
        raise ValueError(f"Golden V3 case count {len(cases)} != 45")
    if len(chunk_ids) != CANONICAL_CHUNK_COUNT:
        raise ValueError(
            f"chunk count {len(chunk_ids)} != {CANONICAL_CHUNK_COUNT}"
        )
    settings = load_settings()
    return EmbeddingBenchmarkInputs(
        cases=cases,
        chunks=chunks,
        client=client_from_settings(settings),
        settings=settings,
    )
```

Use imports from the existing Golden loader, chunker, point builder, Qdrant
helpers, upsert helpers and `DenseRetriever`; do not duplicate those pipelines.

**Step 3: Implement safe active-collection snapshots**

Define:

```python
def snapshot_active_collection(inputs: EmbeddingBenchmarkInputs) -> dict[str, object]:
    ...
```

It must read the configured active collection name, exact point count and safe
schema summary (dense vector names/dimensions/distances and sparse vector names).
It must not scroll payload text or vectors. Compare snapshots with ordinary dict
equality and fail if any field changes.

Capture/display:

1. before any 08a model load or candidate mutation;
2. immediately after the E5-small control;
3. after all candidates.

**Step 4: Derive isolated settings without mutating production settings**

Use `copy.deepcopy(inputs.settings)` per setting and change only the copied
embedding model/revision metadata, vector size and isolated collection name.
Force the copied profile fields to dense-only for reporting, but do not edit
`backend/config/settings.yaml` and do not select either hybrid profile.

**Step 5: Implement timing and RSS helpers**

Use `time.perf_counter_ns()` and `psutil.Process().memory_info().rss`. Record:

- RSS immediately before load;
- RSS immediately after load;
- RSS after document embedding;
- RSS after each of three full repetitions;
- observed peak as the maximum of those checkpoints;
- cold load separately;
- document embedding separately;
- per-query query-embedding, Qdrant retrieval and warm-total timings.

Compute p50/p95 from all 135 measured values for a completed setting. The one
warm-up case is excluded from metrics and timing arrays.

**Step 6: Implement collection creation and indexing**

For each setting:

1. call the runner once for all 572 document texts;
2. build real points with `build_points` using returned vectors;
3. call `ensure_collection` on the isolated name/dimension;
4. call `validate_existing_points` before upsert;
5. call `upsert_points` once;
6. call `validate_collection_info` and `verify_point_count(..., 572)`;
7. never call `reset_collection` or `delete_collection`.

An existing mismatched/foreign candidate collection must fail closed; it is not
automatically recreated.

**Step 7: Implement measured retrieval without duplicating DenseRetriever**

Instantiate production `DenseRetriever` with the isolated collection and
`top_k=30`. To time query encoding separately while still using production
retrieval conversion/sorting, use a one-query timing wrapper around the real
runner: its `embed_query` records the duration and delegates exactly once. Time
the whole `DenseRetriever.search(question, limit=30)` call and derive Qdrant
retrieval time as total search time minus the recorded query-embedding time.

Do not copy `query_points`, payload conversion or tie-breaking logic into the
benchmark module.

**Step 8: Execute the exact sequence**

Implement:

```python
def run_embedding_benchmark(
    setting: DenseBenchmarkSetting,
    benchmark_inputs: EmbeddingBenchmarkInputs,
    *,
    control_result: EmbeddingBenchmarkResult | None = None,
    lighter_results: tuple[EmbeddingBenchmarkResult, ...] = (),
) -> EmbeddingBenchmarkResult:
    ...


def run_embedding_benchmarks(
    settings: tuple[DenseBenchmarkSetting, ...],
    benchmark_inputs: EmbeddingBenchmarkInputs,
    *,
    control_result: EmbeddingBenchmarkResult,
):
    ...
```

Exact order inside one setting:

1. validate supported setting and active snapshot;
2. record RSS-before-load and cold load;
3. embed/index all documents;
4. run one warm-up query: exact case `foods-v3-0001`;
5. run all 45 cases in canonical order three times;
6. score quality from repetition one and verify case IDs/ranking stability across
   all three, where stability means exact ordered Top-30 chunk-ID equality for
   every case;
7. compute gates/bootstrap/control and best-lighter comparison when applicable;
8. write the setting's overall plus nine category CSV rows;
9. close the runner and yield/return the result.

Status rules:

- `completed`: 3/3 measured repetitions plus required scoring/comparison row
  construction succeeded;
- `partial`: usable observed results exist but only 1/3 or 2/3 full repetitions
  completed;
- `failed`: no valid completed setting result exists;
- `finalist_eligible`: only `completed` with 3 successful repetitions;
- preserve the exact sanitized first failure; do not retry;
- after persistence and cleanup, the sequential candidate generator continues
  with the next independent setting.

`run_embedding_benchmarks` maintains the lighter-reference list internally. It
starts with the completed E5-small control, adds only earlier candidates that
are finalist-eligible and clear the control, passes that tuple into the next
one-setting call, closes each runner before yielding, and preserves approved
order.

For partial/failed rows, preserve observed resource/timing data and leave
unavailable quality/comparison fields blank. Do not manufacture zeroes.

**Step 9: Implement notebook display helpers only where they remove cell logic**

Expose small functions returning dicts/lists or Polars DataFrames:

```python
describe_embedding_benchmark_environment()
settings_table()
quality_table(control_result, candidate_results)
comparison_table(control_result, candidate_results)
latency_table(control_result, candidate_results)
resource_table(control_result, candidate_results)
failure_table(control_result, candidate_results)
display_canonical_inputs(benchmark_inputs)
```

These are views over result data, not validators or another report framework.

---

## Task 7: Create the educational repository notebook

**Files:**

- Create: `notebooks/08a_embedding_benchmark.ipynb`

**Step 1: Build about 26 alternating cells in seven sections**

Follow the exact seven-section outline from the design. Markdown is concise
Vietnamese; identifiers are English. Each code cell does one thing. Use the same
simple path setup pattern as existing notebooks, then import only public backend
objects.

The notebook must visibly explain:

- all three current profiles;
- `dense_only` fixed for 08a;
- `hybrid_no_rerank` deferred to 08b;
- `hybrid_rerank` split across 08b/08c then combined in 08d;
- CPU FP32, fixed batches, warm-up and 3x45 repetitions;
- source + section relevance and isolated collections;
- metrics, latency, RSS, truncation, failures and lighter/heavier trade-offs;
- no production cutover and no total Phase 8 approval.

**Step 2: Keep canonical input cells short**

The cells should be equivalent to:

```python
benchmark_inputs = load_embedding_benchmark_inputs()
```

```python
display_canonical_inputs(benchmark_inputs)
```

```python
active_before = snapshot_active_collection(benchmark_inputs)
active_before
```

No file parsing, chunking, validation or Qdrant mutation logic belongs in the
notebook.

**Step 3: Put E5-small in its own run cell**

Use exactly the approved shape:

```python
control_result = run_embedding_benchmark(
    E5_SMALL_SETTING,
    benchmark_inputs,
)
```

The next cells display its overall/category metrics and confirm the active
snapshot still equals `active_before`.

**Step 4: Put all three authorized candidates in one sequential run cell**

Use exactly:

```python
candidate_results = []

for result in run_embedding_benchmarks(
    DENSE_CANDIDATE_SETTINGS,
    benchmark_inputs,
    control_result=control_result,
):
    candidate_results.append(result)
    display(result.summary)
```

Do not use parallel model loading. Backend must close each runner before the
generator yields the completed result.

**Step 5: Add separate human-facing result views**

Show quality, bootstrap/guardrails, latency, resources/truncation, failures and
best-lighter decisions separately. Show the CSV path and the final active
snapshot comparison. Do not dump raw stack traces, headers, secrets or model
provider payloads.

**Step 6: Normalize the repository notebook**

Every code cell must have:

```json
"execution_count": null,
"outputs": []
```

Do not save the real execution back into the repository notebook.

**Step 7: Parse and inspect structure**

Run:

```bash
jq empty notebooks/08a_embedding_benchmark.ipynb
jq -e 'all(.cells[] | select(.cell_type == "code"); .execution_count == null and (.outputs | length) == 0)' notebooks/08a_embedding_benchmark.ipynb
jq -r '.cells[] | [.cell_type, ((.source // []) | join("") | split("\n")[0])] | @tsv' notebooks/08a_embedding_benchmark.ipynb
```

Expected: valid JSON, clean code cells, and an easily readable alternating
Markdown/code progression.

---

## Task 8: Finish focused deterministic verification before the real run

**Files:**

- Verify: `backend/tests/test_embedding_benchmark.py`
- Verify: `backend/embedding/dense_benchmark.py`
- Verify: `backend/evaluation/embedding_benchmark.py`
- Verify: `notebooks/08a_embedding_benchmark.ipynb`

**Step 1: Run only the focused tests**

From `backend/`:

```bash
HF_HUB_OFFLINE=1 \
UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-test-uv-cache \
uv run --env-file ../.env \
python -m pytest tests/test_embedding_benchmark.py -q --tb=short
```

Expected: PASS without network, model load, Qdrant mutation, mocks/fakes or old
benchmark output.

**Step 2: Inspect the full implementation diff**

Run from root:

```bash
git diff --check
git status --short
git diff -- pyproject.toml uv.lock backend/embedding/dense_benchmark.py backend/evaluation/embedding_benchmark.py backend/tests/test_embedding_benchmark.py notebooks/08a_embedding_benchmark.ipynb
```

Expected: no whitespace errors; every implementation change is within approved
scope. Read untracked files directly because ordinary `git diff` omits them.

**Step 3: Recheck forbidden changes**

Run:

```bash
git diff -- backend/config/settings.yaml backend/embedding/embedder.py backend/evaluation/golden_dataset.py knowledge-base-hue/foods/evaluation/golden_v3.jsonl knowledge-base-hue/foods/evaluation/golden_v3_smoke.jsonl
```

Expected: no implementation diff in these files.

---

## Task 9: Run the real authorized benchmark on a temporary notebook copy

**Files:**

- Create after authorized successful/partial run:
  `evaluation/results/phase8_embedding_results.csv`
- Do not modify repository notebook outputs

This task mutates only the four approved isolated Qdrant collections and the
one durable CSV. The required real-run authorization is recorded in this plan's
status; an available Qdrant service is still required. It uses real pinned
models, full 45 cases and all 572 chunks.

**Step 1: Capture production and candidate state read-only**

Use the backend snapshot helper to record active collection schema/count. Also
list whether each approved isolated collection exists and, if it exists, its
safe schema/count. Do not scroll payload text/vectors and do not delete anything.

Expected: active target is `hue_foods_e5_small_384`. Any existing isolated
collection with wrong schema or foreign points will fail closed later.

**Step 2: Execute Run All to `/tmp`**

Run from repository root:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-implement-uv-cache \
uv run --env-file .env \
jupyter nbconvert \
  --execute \
  --to notebook \
  notebooks/08a_embedding_benchmark.ipynb \
  --output /tmp/08a_embedding_benchmark-implement-live.ipynb \
  --ExecutePreprocessor.timeout=28800
```

Expected: the temporary copy records real outputs; repository notebook stays
clean. E5-small runs in its separate cell, then candidates run sequentially.
Do not alter the timeout, model revision, device, dtype, batch size or data if a
setting fails.

**Step 3: Treat failures exactly**

If dependency, model download, network, RAM or Qdrant fails:

- preserve `failed`, `partial` or `blocked` according to observed progress;
- retain the sanitized exact first error;
- persist any setting rows the backend safely produced;
- do not retry, shrink batches, switch devices, change revision or replay old
  output;
- continue only to the next independent setting when the designed generator can
  do so safely.

**Step 4: Reconcile observed artifacts**

Check:

```bash
jq empty /tmp/08a_embedding_benchmark-implement-live.ipynb
test -f evaluation/results/phase8_embedding_results.csv
```

Then verify from the temporary notebook and real Qdrant:

- one overall plus nine category rows per attempted setting;
- exactly 3 successful repetitions for each finalist-eligible setting;
- latency arrays exclude warm-up and contain 135 values for completed settings;
- all successful isolated collections have 572 points and exact dimensions;
- no removed Qwen/BGE/E5-large collection is created or mutated;
- production active snapshot equals the baseline;
- `backend/config/settings.yaml` remains unchanged.

**Step 5: Independently recompute one sample before reporting**

Select one Golden V3 case with multiple declared evidence pairs. From its first
repetition Top 5, manually derive unique source+section gains, Recall@5, MRR@5
and nDCG@5 using the formula in Task 3. Compare with notebook/result data.

Also recompute one category guardrail from its per-case rows. Expected: exact
agreement within floating-point display precision. A mismatch is a correctness
failure, not a documentation issue.

---

## Task 10: Write the implementation report and hand off for independent review

**Files:**

- Create: `reports/phase_8_08a_embedding_benchmark_implementation_report.md`

**Step 1: Report observed evidence, not claims**

Include:

- exact user authorization for implementation and for the real run;
- exact changed files and confirmation that unrelated dirty files were
  preserved;
- focused test command and observed result;
- real Run All command, start/end state and observed result;
- package/model revisions actually loaded;
- per-setting status, 3/3 eligibility, collection/dimension/count, truncation,
  latency and RSS summary;
- active collection before/after snapshots;
- CSV/notebook reconciliation and the independently recomputed sample;
- every failure/partial result with sanitized exact error;
- explicit statement that BM25, fusion, reranker, generation, judge, Golden V3
  optimization and production cutover were not performed;
- explicit statement that Phase 8 remains `not_ready`.

Do not paste secrets, raw headers, raw provider payloads or sensitive stack
traces.

**Step 2: Perform verification-before-completion**

Run again:

```bash
cd backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-test-uv-cache uv run --env-file ../.env python -m pytest tests/test_embedding_benchmark.py -q --tb=short
cd ..
git diff --check
git status --short
jq -e 'all(.cells[] | select(.cell_type == "code"); .execution_count == null and (.outputs | length) == 0)' notebooks/08a_embedding_benchmark.ipynb
```

Expected: focused tests PASS, diff check clean, repository notebook clean. Do
not describe the implementation as complete if fresh evidence contradicts it.

**Step 3: Request independent code review**

Hand the Reviewer:

- the approved design and this plan;
- exact implementation/run authorization;
- implementation report;
- complete worktree status and diff;
- source/tests/notebook/CSV;
- temporary executed notebook path if still present;
- official model sources and exact installed BGE 1.4.0 source path used for the
  adapter.

The Reviewer must independently run the focused tests and real temporary-copy
Run All. Implementer must not write or overwrite the Codex review or user
report.

**Step 4: Stop at the review boundary**

Do not update canonical guides, README indexes, Project Status or Phase 8 status.
Do not mark 08a approved. Do not begin 08b. Do not commit or push. User approval
comes only after independent technical review and the user's own Notebook 08a
confirmation.

## Local execution amendment (2026-08-29 +07, superseding earlier local scope)

Implement and execute exactly these 4 local dense configurations:
1. `e5-small-384` (Control, 384D, Authorized)
2. `multilingual-minilm-l12-384` (384D, Authorized)
3. `huydang-dek21-embedding-768` (PhoBERT ~135M params, 768D, max length 256, PyVi segmentation, Authorized)
4. `e5-base-768` (768D, Authorized)

Do not locally download or execute `e5-large-1024`, `bge-m3-dense-1024`,
`qwen3-embedding-0.6b-384` or `qwen3-embedding-0.6b-1024`. Runtime boundaries must reject them before model
load, network access or Qdrant mutation. Notebook Run All must iterate an exact
three-candidate tuple after the separate control cell, never the historical full
catalog.

The local implementation should remove both Qwen settings and runner, the three
1024D setting constants, their local collection targets and local-only
adapter/test paths. In particular, remove the BGE-M3 local runner and direct
`FlagEmbedding` dependency if no other authorized local consumer remains. A future OpenRouter adapter must be designed
from the remote API contract rather than retaining the local BGE adapter.

After the four-setting local run is complete, write a proposal only—not an
adapter or paid run—for OpenRouter `intfloat/multilingual-e5-large` and
`baai/bge-m3`. Any remote benchmark requires a new explicit user authorization,
budget, exact model IDs, current embeddings schema, preprocessing contract and
isolated remote-vector collections. Do not propose or run Qwen3 Embedding unless
the user explicitly reopens that scope.

Reviewer fresh evidence from `2026-08-29 +07` already covers all four retained
models at 3/3 repetitions on 45 cases and 572 chunks. The correction handoff may
reuse that evidence without rerunning models when code changes only remove
Qwen/deferred paths and do not alter encoding, retrieval or metrics. Historical
Qwen CSV rows remain evidence only; do not recreate its cache or collection.
