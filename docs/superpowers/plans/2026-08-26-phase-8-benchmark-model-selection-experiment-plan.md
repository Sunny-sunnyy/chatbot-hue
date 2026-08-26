# Phase 8 Benchmark Model Selection Master Experiment Plan

**Status:** `design_in_progress`; sequencing plan only, not an implementation
plan or execution authorization.

**Goal:** So sánh các embedding, lexical/sparse/hybrid, reranker và final RAG
pipeline trên tiếng Việt bằng controlled experiment groups, đồng thời ưu tiên
quality đáng tin cậy, latency và simplicity.

**Canonical design:**
`docs/superpowers/specs/2026-08-26-phase-8-benchmark-model-selection-design.md`

## Global gates

1. Golden dataset correction phải hoàn tất và được user phê duyệt ở scope riêng.
2. Không sửa dataset trong Phase 8 design/benchmark implementation.
3. Không mutate active Qdrant collection; mọi reindex dùng isolated collection.
4. Chỉ thay đổi một experiment group trong mỗi comparison chính.
5. Không dùng mock/fake/replayed output làm benchmark evidence.
6. User phải duyệt detailed experiment group trước khi implement hoặc chạy.
7. GPU/WSL2 remediation thuộc session riêng; CPU fallback được chấp nhận.

## Experiment order

| Stage | Experiment group | Ordered candidates/capabilities | Fixed boundary |
|---:|---|---|---|
| 0 | Golden prerequisite | corrected Vietnamese golden dataset | separate scope; no Phase 8 run before approval |
| 1 | Dense embedding | E5 small → multilingual MiniLM-L12 → E5 base → E5 large → BGE-M3 dense → Qwen3 Embedding 0.6B at 384D → Qwen3 Embedding 0.6B at 1024D | chunks, gold, dense retrieval settings, metrics |
| 2 | Lexical/sparse/fusion | current BM25-on-dense candidates → independent BM25 candidates → experimental TF-IDF sparse → BGE-M3 learned sparse → true hybrid | selected/fixed dense evidence, reranker off |
| 3 | Reranker | current MiniLM-L6 → BGE reranker base → Qwen3 Reranker 0.6B | identical pre-rerank candidate artifacts |
| 4 | Context | maximum 5 whole chunks/3000 characters | retrieval output and generator |
| 5 | End-to-end finalists | selected retrieval/reranking finalists | `qwen/qwen3.5-9b` via OpenRouter; judge `gpt-5.4-mini` |
| 6 | Final decision | quality, latency, reliability, cost, complexity | approved selection rule |

All local model stages run sequentially from lightweight to heavier candidates.
The local retrieval/reranking stage uses the full compatibility-aware matrix.
Only the later paid generation/judge stage uses finalists selected from that
matrix; its exact gate/count remains a design question.

### Valid retrieval coverage

| Retrieval path | Runs required before reranking |
|---|---:|
| Dense-only | Seven, one per dense configuration |
| BM25-only full corpus | One |
| Dense → BM25 rescoring | Seven, one per dense configuration |
| True hybrid dense + BM25 | Seven, one per dense configuration |
| TF-IDF SparseEmbedder-only | One |
| True hybrid dense + TF-IDF | Seven, one per dense configuration |
| BGE-M3 learned sparse-only | One |
| BGE-M3 dense + learned sparse | One |

The full local matrix applies four reranker states—none, current MiniLM, BGE
reranker base and Qwen3 Reranker 0.6B—to each valid pre-rerank pipeline. It does
not duplicate BM25-only/TF-IDF-only by embedding label and does not construct an
unsupported learned-sparse pairing.

Qwen3 Embedding contributes two configurations, 384D and native 1024D. Each is
indexed separately. Do not include 768D in the initial experiment matrix.

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

Implementation tasks, exact commands, test cases, notebook structure and commit
boundaries will be written only after the remaining design questions are user
approved.

## Deferred discussion queue for the next session

Resolve these gates in order; do not let an Implementer infer them:

1. Finish the separate 104-case golden-data audit/correction design, lock the
   representative 20-case smoke subset, and decide surgical correction versus
   a separately named new dataset from evidence.
2. Decide whether Phase 8 needs chunk/document relevance labels beyond the
   current keyword proxy; lock category distribution, regression blockers and
   uncertainty/clear-gain rules.
3. Lock exact embedding instructions/pooling/normalization/truncation/dtype/
   batching and reranker formatting/truncation/batching for every candidate.
4. Design BGE-M3 learned-sparse representation, isolated Qdrant schema,
   collection naming and retention/cleanup without touching the active
   collection.
5. Enumerate the exact non-duplicate matrix manifest, including both fusion
   methods and the mandatory `llm_rag_reference_on_hue` row.
6. Lock warm-up/repetition, p50/p95, cold-load, failure/OOM and CPU-versus-GPU
   measurement rules.
7. Lock the paid-finalist rule/count, Qwen generator settings, GPT judge rubric
   and repetition policy.
8. Lock readable CSV columns/category views, notebook update behavior, focused
   tests, real Run All review commands and final winner rerun.
9. Treat any production switch, active collection mutation or cleanup as a
   later proposal requiring explicit user approval.

GPU/WSL2 remediation remains a different session. Model catalogs, licenses,
provider IDs, API schemas and resource compatibility must be rechecked from
primary sources immediately before implementation/execution.
