# Phase 8 Benchmark Model Selection Design

**Status:** `design_in_progress`

**Purpose:** Khóa các quyết định Phase 8 đã được user xác nhận trong khi tiếp
tục brainstorming những biến thí nghiệm còn lại. Tài liệu này không authorize
code, dataset correction, model download, CUDA/PyTorch changes, paid runs,
Qdrant mutation, commit hoặc push.

## Boundary và prerequisite

- Golden Dataset V2 là scope riêng đã được user phê duyệt thiết kế tại
  `docs/superpowers/specs/2026-08-26-phase-8-golden-dataset-v2-design.md`.
  Implementer phải hoàn tất plan riêng và qua Reviewer Gate 0 trước bất kỳ
  Phase 8 benchmark nào.
- Phase 8 hiện chỉ thiết kế master framework và thứ tự experiment groups.
- Active Qdrant collection tiếp tục read-only; candidate indexes/collections
  phải isolated.
- Mỗi comparison chính chỉ thay đổi một experiment group.

## Fixed end-to-end boundary

```text
Generator: qwen/qwen3.5-9b qua OpenRouter
Judge: gpt-5.4-mini
Primary language: Vietnamese
Local execution: GPU khi session riêng enable thành công; CPU fallback bắt buộc
```

## Mandatory llm_rag reference baseline

`llm_rag_reference_on_hue` ports the exact current `llm_rag` runtime flow onto
the Hue corpus and corrected golden data:

```text
E5-small dense top 30
→ raw 0.6 dense + 0.4 BM25 rescoring on those same candidates
→ top 10
→ current MiniLM reranker input 10/output 5
→ at most 5 whole chunks and 3000 context characters
→ qwen/qwen3.5-9b via OpenRouter
→ gpt-5.4-mini judge
```

Raw unnormalized fusion is preserved only to reproduce the reference. Runtime
source, which truncates to 10 before reranking, overrides an inconsistent prose
sentence in the deep-dive document that says reranking sees 30.

Generator và judge giữ cố định khi so retrieval/reranking. Answer generation
chỉ chạy cho end-to-end finalists sau khi retrieval evidence được khóa.

## Dense embedding candidate order

Thứ tự dưới đây đi từ nhẹ đến nặng/mạnh hơn để tạo baseline sớm và kiểm soát
tài nguyên. Nó không giả định trước winner.

| Thứ tự | Model | Dimension/capability | Vietnamese policy |
|---:|---|---|---|
| 1 | `intfloat/multilingual-e5-small` | 384D; current control | benchmark corrected Vietnamese gold |
| 2 | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | 384D; lightweight multilingual | benchmark corrected Vietnamese gold |
| 3 | `intfloat/multilingual-e5-base` | 768D | benchmark corrected Vietnamese gold |
| 4 | `intfloat/multilingual-e5-large` | 1024D | benchmark corrected Vietnamese gold |
| 5 | `BAAI/bge-m3` | 1024D; dense + learned sparse + multi-vector | dense và sparse/hybrid ở separate groups |
| 6a | `Qwen/Qwen3-Embedding-0.6B` | 384D MRL variant; instruction-aware | lightweight/storage trade-off |
| 6b | `Qwen/Qwen3-Embedding-0.6B` | native 1024D; instruction-aware | maximum-quality variant |

The scope therefore contains six model families and seven dense configurations.
Do not add a 768D Qwen variant initially. Each Qwen dimension uses its own
isolated index; equal dimensions never make embeddings from different models
compatible.

## Sparse and hybrid capabilities in scope

Phase 8 must create controlled real comparisons for:

| Retrieval path | Required compatible coverage |
|---|---|
| Dense-only | All seven dense configurations |
| Independent full-corpus BM25-only | Once; embedding-independent |
| Current dense-candidate then BM25 rescoring | All seven dense configurations |
| True hybrid dense + independent full-corpus BM25 | All seven dense configurations |
| Custom TF-IDF `SparseEmbedder`-only | Once as an experimental control |
| True hybrid dense + custom TF-IDF sparse | All seven dense configurations |
| BGE-M3 learned sparse-only | BGE-M3 only |
| BGE-M3 dense + learned sparse true hybrid | BGE-M3 only |

Notebook 08d combines every valid pre-rerank pipeline with no reranker and each
of the three reranker candidates. Complete coverage means every real component,
path and compatible interaction is measured. It does not mean repeating an
embedding-independent result under six embedding labels or inventing a learned-
sparse pairing for a model that cannot produce that representation.

Compatibility-aware local matrix, initial fusion methods and depth contract have
been locked. The finalist gate before paid generation continues through
brainstorming before implementation authorization.

Initial true-hybrid comparisons use exactly two fusion methods:

- Reciprocal Rank Fusion (RRF) as the primary rank-based method;
- independent min-max normalization followed by `0.6 dense / 0.4 sparse`
  weighted sum, preserving the current baseline weighting.

No initial weight grid is allowed. Targeted weight tuning can be proposed only
after real results show that weighted fusion is beneficial and tuning could
change the final decision.

## Depth and context contract

- Dense, BM25 and sparse candidate generators each retrieve up to 30.
- Fusion retains the top 10 as the common pre-rerank input.
- Every reranker scores the same 10 and returns top 5.
- No-rerank final comparison uses the top 5 of the same pre-rerank ranking.
- Generation receives at most 5 whole chunks and 3000 characters; it may receive
  fewer when the character budget is reached.
- Report candidate Recall@30, fusion Recall@10 and final MRR@5/nDCG@5/Recall@5.

This keeps final retrieval comparisons at the same depth. Ten documents are
never passed directly to the generator under this contract.

## Reranker candidate order

| Thứ tự | Model | Published language scope | Design treatment |
|---:|---|---|---|
| 1 | `cross-encoder/ms-marco-MiniLM-L-6-v2` | English | lightweight current baseline; full Vietnamese measurement |
| 2 | `BAAI/bge-reranker-base` | Chinese, English | retain only if Vietnamese evidence passes quality gates |
| 3 | `Qwen/Qwen3-Reranker-0.6B` | multilingual | heavier primary multilingual candidate |

Model code producing scores for Vietnamese input is integration evidence, not
quality evidence. Models without an explicit Vietnamese claim are not rejected
before measurement, but cannot win without corrected-gold Vietnamese evidence.

## Measurement contract

Every candidate records:

- corrected-gold retrieval quality, including aggregate and category slices;
- failures and stability across repeated runs where applicable;
- model load/cold-start latency separately from warm inference;
- indexing/corpus embedding time;
- query embedding, dense retrieval, sparse retrieval/fusion, reranking and
  generation latency separately;
- warm online latency with at least p50 and p95;
- device, dtype, batch size, candidate depth and top-k;
- memory/resource observations, provider cost and operational complexity when
  applicable.

CPU and GPU measurements are separate execution profiles. A model running on
CPU is not directly ranked against another model running on GPU for latency.

## Approved selection rule

When Vietnamese quality differences are not trustworthy, select the lighter,
faster and simpler model/pipeline. A heavier candidate wins only when it shows a
clear quality improvement, does not regress important categories, and its
latency and operational complexity remain acceptable. Tiny aggregate gains do
not override simplicity by themselves.

Exact uncertainty method and category thresholds will be designed against the
approved corrected golden dataset, rather than invented before that dataset is
known.

## GPU boundary

The available GPU is NVIDIA GTX 1650 under Windows/WSL2. Current Hue environment
has a CUDA-enabled PyTorch build but WSL reports GPU access blocked by the
operating system. Diagnosis and remediation belong to a separate session.
Phase 8 design neither installs `cu132` nor changes dependencies. CPU execution
remains accepted as fallback.

## Notebook experience

Phase 8 uses notebooks by experiment group rather than one notebook per
configuration:

| Notebook | Human-facing responsibility |
|---|---|
| `notebooks/08a_embedding_benchmark.ipynb` | Learn and compare all dense embedding candidates |
| `notebooks/08b_retrieval_fusion_benchmark.ipynb` | Learn and compare lexical, sparse and fusion paths |
| `notebooks/08c_reranker_benchmark.ipynb` | Compare no-rerank and all reranker candidates on fixed inputs |
| `notebooks/08d_full_pipeline_matrix.ipynb` | Run the approved local embedding × retrieval × reranker matrix |
| `notebooks/08e_generation_finalists.ipynb` | Generate and judge answers for approved finalists |
| `notebooks/08_benchmark_model_selection.ipynb` | Read group results, explain trade-offs and select the final pipeline |

Notebook design follows the teaching style of the required references:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/*.ipynb
/home/minhhieu/llm_rag/tai_lieu/notebook_simple/**/*.ipynb
```

Each section starts with a clear heading and short explanation of what will run,
why it matters, what stays fixed, expected resource/time considerations and how
to read the result. Cells remain short and direct. Helpers are allowed only when
they visibly remove repetition. Real Hue data/services/models are mandatory;
fake data or mocked execution cannot be implementation or evidence.

## Minimal persistence and memory cleanup

Each experiment notebook writes one cumulative CSV:

| Notebook group | Durable result |
|---|---|
| Embedding | `evaluation/results/phase8_embedding_results.csv` |
| Retrieval/fusion | `evaluation/results/phase8_retrieval_results.csv` |
| Reranker | `evaluation/results/phase8_reranker_results.csv` |
| Full local matrix | `evaluation/results/phase8_pipeline_matrix.csv` |
| Generation finalists | `evaluation/results/phase8_generation_results.csv` |

No run ID, timestamped package, checksum manifest, duplicate JSON artifact or
opaque `configuration_id` is needed. Human-readable configuration columns
identify results. Minimal `status` and `error` columns preserve real failures;
category results remain visible because the approved selection rule forbids
hiding important regressions behind an aggregate mean.

After each model/configuration, save or update its CSV row before releasing the
model and large temporary tensors/embeddings. Run Python garbage collection and
clear the CUDA cache when CUDA is active. A kernel restart then reloads the
cumulative CSV; no resume framework is introduced.

Canonical notebooks are committed with null execution counts and empty outputs.
Interactive outputs may remain visible while the user is running locally, but
they are not the durable checkpoint or committed evidence.

## Decisions still requiring brainstorming

- exact finalist gate/count before paid generation and judging;
- exact uncertainty method, clear-gain rule and statistical/category gates over
  the approved Golden Dataset V2 distribution;
- BGE-M3 learned-sparse representation and isolated storage/query path;
- exact per-model embedding instructions, normalization, truncation, dtype and
  batch settings needed for a fair comparison;
- reranker input formatting, truncation and batching (depth is already fixed at
  input 10/output 5);
- latency repetition/warm-up method and treatment of real failed runs;
- exact generator settings and judge rubric/repetition policy for finalists;
- exact human-readable columns and compact category presentation in each CSV;
- exact implementation checkpoints, verification commands and reviewer reruns;
- post-benchmark rule for proposing, but not automatically performing, a
  production transition.

No item in this section may be assumed by an Implementer.

## BM25 Vietnamese tokenizer decision

Notebook 08b must compare exactly two tokenization variants on the same
full-corpus BM25 path:

1. the current lowercase Unicode `\w+` tokenizer as control;
2. Underthesea word segmentation using `word_tokenize(..., format="text")`.

The comparison records retrieval quality by category and tokenization/query
latency. Underthesea is an experiment dependency, not a predetermined runtime
dependency. Keep it only if observed Vietnamese quality gain justifies its
latency and maintenance cost. Do not add PyVi, VnCoreNLP or a tokenizer grid to
the initial scope.

## Approved Gate 0: Golden Dataset V2

Implementation plan:
`docs/superpowers/plans/2026-08-26-phase-8-golden-dataset-v2-implementation-plan.md`.

No Phase 8 benchmark may run until that plan produces a Reviewer-approved
100-case `golden_v2.jsonl` and exact 20-case smoke subset.

### Locked dataset decisions

- Preserve Phase 7 `tests.jsonl` unchanged; curated rebuild may reuse good old
  cases but writes a separately named 100-case dataset.
- Use exactly nine approved categories, including eight natural grounded
  `numerical` cases, and the approved 40/20/20/20 source targets.
- Keep only six row fields: `case_id`, `question`, `keywords`,
  `reference_answer`, `category`, `evidence`.
- Use binary exact `source + section` relevance; no keyword proxy, LLM labeling
  or stored chunk IDs for Phase 8 retrieval ground truth.
- Smoke contains 20 exact full-dataset rows and covers all nine categories and
  all four source families, including cafes.
- Stop and ask the user when sources conflict or cannot support a natural quota;
  never force weak questions to make counts pass.

### Benchmark-grade ground truth decisions resolved by Gate 0

The new evidence mapping is stable across embedding-specific isolated indexes
because it labels canonical source/section pairs rather than chunk IDs. The full
100 cases support final local retrieval selection; the 20-case subset is smoke
only. Winner regression blockers, uncertainty and the paid generation subset
remain Phase 8 design questions.

## Mandatory backlog after Gate 0 implementation

After golden-data approval, resume brainstorming in this order:

1. **Ground-truth contract and winner gates:** resolve the items above first,
   because they define whether model differences are meaningful.
2. **Exact model settings:** query/document instructions, pooling,
   normalization, max length, dimension, dtype and batch size for every dense
   candidate; input format, truncation and batch size for every reranker.
3. **Sparse/index design:** exact BGE-M3 learned-sparse output, Qdrant schema,
   isolated collection names, indexing/query flow and cleanup/retention policy.
4. **Notebook 08b protocol:** keep current Unicode BM25 as control, compare the
   confirmed Underthesea variant, lock BM25 parameters, and define identical
   RRF/min-max inputs without adding a weight grid.
5. **Matrix manifest:** enumerate every valid, non-duplicate configuration and
   the lightweight-to-heavy run order before implementation so full coverage is
   measurable and unsupported pairings cannot appear.
6. **Latency/reliability protocol:** warm-up count, measured repetitions,
   cold-load versus warm-query reporting, CPU/GPU separation, memory notes and
   explicit handling of failed or out-of-memory configurations.
7. **Paid finalist gate:** exact number or rule for finalists, category and
   quality requirements, generator settings, judge rubric/repeats and cost/
   latency fields. Paid evaluation remains finalist-only.
8. **Notebook/result contract:** exact CSV columns, category views, overwrite/
   update behavior, cleanup cells and which temporary notebook copies the
   Reviewer must Run All.
9. **Verification and handoff:** focused automated tests only for reusable
   behavior, real notebook/service runs as primary evidence, final winner rerun,
   report update and a separate user-approved production transition if needed.
10. **GPU prerequisite if desired:** diagnose WSL2/GTX 1650 and dependency
    compatibility in its already-separated session. CPU fallback remains valid;
    latency rankings must never mix different device policies.

Before real execution, current model/provider availability, model IDs, licenses,
dimensions, API schemas and limits must be reverified from primary sources.
That verification may refine settings but must not silently expand the approved
candidate set.
