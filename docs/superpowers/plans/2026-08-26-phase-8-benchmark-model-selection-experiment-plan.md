# Phase 8 Benchmark Model Selection Master Experiment Plan

**Status:** Gate 1 common contracts approved; Notebook 08a completed and user
confirmed on `2026-08-29 +07`. Notebook 08b research/brainstorming is next;
later notebook implementation/execution remains pending.

**Goal:** So sánh các embedding, lexical/sparse/hybrid, reranker và final RAG
pipeline trên tiếng Việt bằng controlled experiment groups, đồng thời ưu tiên
quality đáng tin cậy, latency và simplicity.

**Canonical design:**
`docs/superpowers/specs/2026-08-26-phase-8-benchmark-model-selection-design.md`

## Global gates

1. Golden Dataset V3 đã được Reviewer kiểm tra và user chấp nhận với 45 full
   cases cùng exact 10-case smoke subset.
2. Không sửa dataset trong Phase 8 design/benchmark implementation.
3. Không mutate active Qdrant collection; mọi reindex dùng isolated collection.
4. Chỉ thay đổi một experiment group trong mỗi comparison chính.
5. Không dùng mock/fake/replayed output làm benchmark evidence.
6. User phải duyệt detailed experiment group trước khi implement hoặc chạy.
7. GPU/WSL2 remediation thuộc session riêng; CPU fallback được chấp nhận.
8. Trước mỗi notebook group: research current primary sources/hardware/
   dependencies, brainstorm exact settings, nhận user approval, rồi mới
   implement hoặc Run All.
9. Evidence mới, failure/OOM hoặc scope conflict bắt buộc quay lại brainstorming;
   không silent retry, shrink batch, đổi device hoặc fallback.

## Experiment order

| Stage | Experiment group | Ordered candidates/capabilities | Fixed boundary |
|---:|---|---|---|
| 0 | Golden prerequisite | approved 45-case Golden Dataset V3 + exact 10-case smoke subset | completed and approved; dataset remains unchanged during benchmark work |
| 1 | Local dense embedding | E5 small → Huydang DEk21 768D → E5 base; completed/approved | chunks, gold, dense retrieval settings, metrics |
| 2 | Local lexical/sparse/fusion | current BM25-on-dense candidates → independent BM25 candidates → experimental TF-IDF sparse → true hybrid dense+BM25/TF-IDF | selected/fixed dense evidence, reranker off |
| 3 | Reranker | current MiniLM-L6 → BGE reranker base → Qwen3 Reranker 0.6B | identical pre-rerank candidate artifacts |
| 4 | Context | maximum 5 whole chunks/3000 characters | retrieval output and generator |
| 5 | End-to-end finalists | selected retrieval/reranking finalists | `qwen/qwen3.5-9b` via OpenRouter; judge `gpt-5.4-mini` |
| 6 | Final decision | quality, latency, reliability, cost, complexity | approved selection rule |

All local model stages run sequentially from lightweight to heavier candidates.
The local retrieval/reranking stage uses the full compatibility-aware matrix.
Only the later paid generation/judge stage uses finalists selected from that
matrix: two fixed reference rows plus at most three new finalists.

## Gate 1 quality and regression gates

- Protect all nine V3 categories.
- Large categories (`n >= 6`) may not lose Top-5 hit cases; with equal hit count,
  block `delta nDCG@5 < -0.02`. Report MRR@5 as support.
- Small categories (`n <= 3`) use exact per-case protection: a case where the
  baseline found exact relevant `source + section` in Top 5 may not lose all
  relevant evidence from Top 5.
- Compute paired bootstrap over 45 candidate-baseline pairs with 10,000
  resamples, fixed seed and 95% percentile CI.
- Clear gain requires every guardrail, aggregate `delta nDCG@5 >= +0.03`, and
  bootstrap 95% CI lower bound for `delta nDCG@5 > 0`.
- Compare every candidate to the group fixed control; survivors/heavier choices
  also compare against the best lighter finalist.

Fixed controls are E5-small dense-only for embedding, Unicode `\w+` for
tokenization, same-embedding dense-only for lexical/sparse/hybrid, the same
pre-rerank ranking with no-rerank for rerankers, and both production baseline
and `llm_rag_reference_on_hue` as full-pipeline reference rows.

Focused automated tests cover only deterministic reusable metrics/gates,
paired bootstrap, category aggregation and CSV upsert. Real model/Qdrant/
provider behavior is verified by temporary-copy notebook Run All, never by
mock/fake completion evidence.

## Common execution and result protocol

- Main profile: CPU FP32, no quantization; document batch 8, query batch 1,
  reranker pair batch 4; no silent auto-shrink. GPU policy remains separate.
- Measure cold load once, discard one warm-up, then run three full 45-case
  repetitions. A finalist must succeed `3/3`; report warm `p50`/`p95` and exact
  ranking variation.
- Record RSS before/after load and observed peak RSS. If CUDA is separately
  approved later, add PyTorch peak allocated/reserved.
- On failure/OOM, persist exact `status`/`error`, release resources and continue
  independent settings without changing configuration.
- Use one long-format cumulative CSV per notebook: `overall` plus category rows.
  Upsert by human-readable setting key after each approved configuration; no
  run registry or historical duplicate artifacts.
- Complexity is `low`/`medium`/`high` with rationale, not a numeric composite.
- No arbitrary latency cutoff is invented before evidence is observed.

### Valid retrieval coverage

| Retrieval path | Runs required before reranking |
|---|---:|
| Dense-only | Four, one per local dense configuration |
| BM25-only full corpus | One |
| Dense → BM25 rescoring | Four, one per local dense configuration |
| True hybrid dense + BM25 | Four, one per local dense configuration |
| TF-IDF SparseEmbedder-only | One |
| True hybrid dense + TF-IDF | Four, one per local dense configuration |

The full local matrix applies four reranker states—none, current MiniLM, BGE
reranker base and Qwen3 Reranker 0.6B—to each valid pre-rerank pipeline. It does
not duplicate BM25-only/TF-IDF-only by embedding label and does not construct an
unsupported learned-sparse pairing.

Qwen3 Embedding is excluded from this machine's experiment matrix at every
dimension. Historical 384D rows remain rejection evidence only.

For every true-hybrid path, run RRF and independent min-max weighted fusion at
`0.6 dense / 0.4 sparse`. Do not add a fusion-weight grid to the initial matrix.
If weighted fusion later shows real benefit, return to user with observed
evidence before adding a targeted tuning comparison.

Notebook 08b includes one controlled Vietnamese tokenization comparison:
current lowercase Unicode `\w+` versus Underthesea
`word_tokenize(..., format="text")`. Run both on the same full-corpus BM25
inputs and parameters, record quality/category deltas and latency, and keep the
current tokenizer unless Underthesea earns its added dependency. Do not add a
third tokenizer in the initial matrix.

### Mandatory reference and depth contract

Run `llm_rag_reference_on_hue` as a named baseline using E5-small, dense top 30,
raw `0.6 dense + 0.4 BM25` rescoring over the dense candidates, hybrid top 10,
current MiniLM input 10/output 5, and context capped at 5 whole chunks/3000
characters. Use Qwen3.5-9B through OpenRouter and GPT-5.4-mini only at the
approved end-to-end stage.

All other local paths use candidate depth 30 per generator, fusion top 10,
reranker input 10/output 5, and no-rerank top 5 for the final comparison. Record
Recall@30 for generation, Recall@10 after fusion and MRR@5/nDCG@5/Recall@5 for
the final ranked output.

## Required result tables

### Dense embedding table

| Model | Dimension | Device/dtype | Index time | Query p50/p95 | MRR/nDCG/Recall | Category regressions | Failures |
|---|---:|---|---:|---:|---:|---|---|

### Retrieval/fusion table

| Dense source | Sparse source | Candidate depths | Fusion | Retrieval p50/p95 | MRR/nDCG/Recall | Coverage | Failures |
|---|---|---|---|---:|---:|---:|---|

### Reranker table

| Model | Published languages | Input/output depth | Device/dtype | Warm p50/p95 | Quality delta | Category regressions | Keep/drop evidence |
|---|---|---|---|---:|---:|---|---|

### End-to-end table

| Pipeline | Generator | Judge | Retrieval quality | Answer scores | Total p50/p95 | Cost | Reliability | Complexity |
|---|---|---|---:|---:|---:|---:|---|---|

## Notebook sequence and durable outputs

| Order | Notebook | Cumulative CSV |
|---:|---|---|
| 1 | `notebooks/08a_embedding_benchmark.ipynb` | `evaluation/results/phase8_embedding_results.csv` |
| 2 | `notebooks/08b_retrieval_fusion_benchmark.ipynb` | `evaluation/results/phase8_retrieval_results.csv` |
| 3 | `notebooks/08c_reranker_benchmark.ipynb` | `evaluation/results/phase8_reranker_results.csv` |
| 4 | `notebooks/08d_full_pipeline_matrix.ipynb` | `evaluation/results/phase8_pipeline_matrix.csv` |
| 5 | `notebooks/08e_generation_finalists.ipynb` | `evaluation/results/phase8_generation_results.csv` |
| 6 | `notebooks/08_benchmark_model_selection.ipynb` | Reads the five group CSVs and explains the final choice |

Every notebook is a human learning document: heading and explanation precede
each runnable section, cells are short and direct, and outputs are interpreted
in plain language. The required style references are `rag_old_0/*.ipynb` and
`notebook_simple/**/*.ipynb`; their presentation style is reused, not any fake
data or unnecessary framework code.

Notebook Markdown is Vietnamese and code identifiers are English. Each cell has
one job, a short Markdown explanation immediately before code, and short code
that imports clear backend functions instead of duplicating runtime logic. Do
not turn notebooks into validators, audit packages or test suites. Verify each
with a real Run All on a temporary copy; repository notebooks keep empty outputs
and null execution counts.

Each completed configuration updates a human-readable CSV row before its model
and large temporary data are released. Python garbage collection and CUDA cache
cleanup happen between models. After kernel restart, the setup cell reloads the
CSV. No run IDs, JSON duplicates, audit packages, memory manager or resume
engine are planned. Canonical notebooks remain clean before commit.

## Selection step

First reject candidates with explicit failures or important Vietnamese category
regressions. Among candidates with a trustworthy quality improvement, compare
latency, reliability, cost and operational complexity. If quality is not
meaningfully different, select the lighter, faster and simpler candidate.

Paid evaluation keeps production baseline and `llm_rag_reference_on_hue` as
reference rows and adds at most three passing finalists. When more than three
are eligible, deduplicate the quality leader, fastest/simplest passing leader
and balanced Pareto leader roles.

After user winner selection, run a clean-kernel 45-case confirmation for the
winner and nearest simpler comparator. If the winner is baseline/lightest, run
only the winner. Update the benchmark summary; production transition is a
separate proposal requiring explicit user approval.

Detailed implementation tasks, exact commands and notebook cells are written
only at the approved research/brainstorm checkpoint for that notebook group.

## Notebook-specific design queue

Gate 1 common decisions and the exact Notebook 08a design/implementation plan
are approved. This master plan deliberately does not guess later groups:

1. `08a`: implement and Run All the approved exact design/plan, then independent
   review and user confirmation before starting 08b.
2. `08b`: research and brainstorm BM25 parameters, Vietnamese tokenizer and
   exact TF-IDF isolated schema/query/fusion behavior.
3. `08c`: verify current reranker library/template compatibility and brainstorm
   exact integration.
4. `08d`: enumerate and approve the exact non-duplicate matrix and execution
   order only after upstream evidence exists.
5. `08e`: approve exact Qwen generation, GPT judge rubric/repetition and paid
   protocol after finalists exist.
6. Final notebook: read approved CSV evidence and present trade-offs; do not
   rerun the entire matrix.

GPU/WSL2 remediation remains a different session. Recheck model catalogs,
licenses, provider IDs, API schemas and resource compatibility from primary
sources immediately before the affected notebook; this check cannot silently
expand candidate scope.

## Resource-bound execution amendment (2026-08-29 +07)

Run exactly three local embedding settings: E5-small 384D, Huydang DEk21 768D
and E5-base 768D. Remove MiniLM-L12, E5-large 1024D, BGE-M3 1024D, every Qwen3
Embedding setting and all BGE learned-sparse paths from local execution plans.

Only after the local three finish may a later checkpoint propose paid OpenRouter
dense runs for `intfloat/multilingual-e5-large` and `baai/bge-m3`. Do not write
the remote adapter, read a key, create remote-vector collections or make an API
request without a new exact plan, budget and explicit user authorization.

Reviewer evidence from `2026-08-29 +07` covers the retained three models at 3/3
repetitions. MiniLM-L12/Qwen caches and isolated collections have been deleted;
their CSV rows remain historical evidence. Notebook 08a is approved and the
next action is exact Notebook 08b research/brainstorming.
