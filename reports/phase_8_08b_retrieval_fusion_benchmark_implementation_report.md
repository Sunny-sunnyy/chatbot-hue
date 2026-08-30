# Phase 8 Notebook 08b — Retrieval & Fusion Benchmark Implementation Report

**Author / Role**: Implementer
**Target Role**: Reviewer
**Date**: 2026-08-30
**Handoff Kind**: Correction Round 4 -> Final Review
**Base Commit**: `93109c2e383f7f19554e2ceb03f10f8c199bc8ea`
**Documentation HEAD**: `1fda0c24ebf6c329f549396901cf1d69765b903e`

---

## 1. Executive Summary & Deliverables

This implementation report documents the complete, verified delivery of **Notebook 08b (Sparse Retrieval & Fusion Benchmark)** for Phase 8 of `hue_rag` incorporating all required resolutions from **Correction Round 4** (`reports/phase_8_08b_retrieval_fusion_benchmark_codex_review.md`).

### Deliverables Checklist
- [x] **Benchmark Orchestration Module**: `backend/evaluation/sparse_benchmark.py` (strict fail-closed reconciliation requiring explicit live `client`, shared `build_expected_immutable_identity` verification across all fields, payload text matching, vector invariants validation, allowlist category secret sanitization, isolated setting error handling, and idempotent CSV writes).
- [x] **Test Suite**: `backend/tests/test_sparse_benchmark.py` (comprehensive coverage including missing explicit client, parameterized immutable identity corruption, unquoted/single-quoted/double-quoted/quoted Bearer/traceback secret sanitization, batch failure continuation, and 0-write artifact hash preservation). Total backend test suite: **85 passed, 1 warning in 45.11s**.
- [x] **Vietnamese Learning Notebook**: `notebooks/08b_retrieval_fusion_benchmark.ipynb` (nbformat 4.5, 26 cells, clean outputs `[]` and `execution_count: null`, safe batch runner, and live `inputs=inputs` reconciliation call).
- [x] **Durable Benchmark Artifacts** (in `evaluation/results/`):
  - `phase8_sparse_manifest.json`: SHA256 `5fe551d3b107c5da4d33680fd8d6d39b1f2f138f055f2d20a7b4ceca2fc22f8e` (1 manifest with immutable identity and batch history).
  - `phase8_sparse_calibration.csv`: SHA256 `a62dbbdf2d5d4f08ce98bb31ded0f47f9723ad743388f271b3911c7ca10986de` (70 rows covering 5 parameter + 2 tokenizer settings $\times$ 10 categories).
  - `phase8_sparse_results.csv`: SHA256 `9f6c42b59a333acf0a17dcd31365a74517979c5f0dcb702ffc17f704aa567b0f` (200 rows covering 20 retrieval settings $\times$ 10 categories).
  - `phase8_sparse_cases.jsonl`: SHA256 `e6cae9d35bb575a7e9b5fe75077cbd018569a8808e74d25a40fa46dd8348bf2a` (900 records with full 13-field raw fusion evidence).
- [x] **Temporary Executed Notebook**: `/tmp/hue_rag_08b_executed_notebook.ipynb` (114 KB, exit code 0).

---

## 2. Scope, Risk Boundaries & Authority

- **Risk Level**: Medium.
- **Production Isolation**: Active collection `hue_foods_e5_small_384` (572 points) and production runtime were monitored with before/after snapshots and maintained strictly read-only (zero mutation).
- **Mutations Allowed**: Only isolated TF-IDF collection (`hue_rag_phase8_08b_tfidf_v1_unicode_word_5297c8604335`) and evaluation artifacts in `evaluation/results/`.
- **Out of Scope**: No production cutover, no deployment, no modification to 08a collections or active configs, no changes to Golden Dataset V3 canonical ground truth.

---

## 3. Environment, Runtime & Dependencies

- **OS / Platform**: Linux (Ubuntu x86_64).
- **Python Runtime**: Managed via `uv` with `.env` loader.
- **Dependencies**: `qdrant-client` 1.18.3, `underthesea` 9.5.0, `polars`, `numpy`, `torch`, `transformers`.
- **Vector Database**: Local Qdrant server running via Docker Compose (`ports: 6333, 6334`).

---

## 4. Canonical Inputs & 08a Prerequisites Verification

- **Curated Foods Corpus**: 572 chunks deterministically generated from 91 curated Markdown files (`corpus_fingerprint: 5297c8604335...`).
- **Golden Dataset V3**: 45 canonical evaluation cases (`golden_fingerprint: 8506eac3f567...`).
- **08a Dense Prerequisites**:
  1. `dense__e5-small-384`: collection `hue_foods_08a_e5_small_384` (384D, 572 points, Recall@5 = 0.8185, nDCG@5 = 0.7425).
  2. `dense__huydang-dek21-embedding-768`: collection `hue_foods_08a_huydang_dek21_768` (768D, 572 points, Recall@5 = 0.8370, nDCG@5 = 0.7164).
  3. `dense__e5-base-768`: collection `hue_foods_08a_e5_base_768` (768D, 572 points, Recall@5 = 0.8407, nDCG@5 = 0.7061).

---

## 5. Part A: BM25 Parameter and Tokenizer Calibration

### BM25 Hyperparameter Tuning ($K=30$ candidate depth, 3 repetitions)
- Tested 5 configurations: `baseline` ($k_1=1.5, b=0.75$), `k1_low` ($k_1=1.2, b=0.75$), `k1_high` ($k_1=1.8, b=0.75$), `b_low` ($k_1=1.5, b=0.5$), `b_high` ($k_1=1.5, b=1.0$).
- `b_low` failed category guardrails on `direct_fact` and `spanning`.
- `baseline` and `b_high` tied on Recall@30 (0.9519, 44/45 hit cases).
- On nDCG@5 tiebreaker: `baseline` achieved nDCG@5 = 0.6478 vs `b_high` 0.6442.
- **Selection**: `baseline` ($k_1=1.5, b=0.75$) retained.

### Tokenizer Calibration
- Evaluated `unicode_word` (regex `\w+`) vs `underthesea_word` (Vietnamese compound word segmentation).
- `unicode_word`: Recall@30 = 0.9519, nDCG@5 = 0.6478, warm p95 = 5.3 ms.
- `underthesea_word`: Recall@30 = 0.9556 (+0.0037), nDCG@5 = 0.6416 (-0.0062), warm p95 = 14.8 ms.
- **Selection**: `unicode_word` selected per architectural simplicity principle (marginal recall gain does not justify compound tokenizer latency and maintenance overhead).

---

## 6. Part B: TF-IDF Construction and Sparse Collection Validation

- **Formula**: Log-TF ($1 + \ln(\text{tf})$), Smoothed-IDF ($\ln((N+1)/(\text{df}+1)) + 1$), and L2 vector normalization.
- **Vocabulary**: 2,093 unique sorted terms (`vocabulary_fingerprint: b75949abab2e...`).
- **Collection**: `hue_rag_phase8_08b_tfidf_v1_unicode_word_5297c8604335`.
- **Validation**: 572 points, verified sparse vector configuration `TFIDF_VECTOR_NAME: "tfidf"`, strictly sorted unique indices, non-empty, finite values, and L2 norm $\approx 1.0 \pm 10^{-3}$.

---

## 7. 20-Setting Retrieval Matrix Execution & Checkpointing

All 20 settings executed with 3 repetitions across 45 cases (900 cases total):
- 3 Dense Only (`e5-small-384`, `huydang-dek21-embedding-768`, `e5-base-768`).
- 1 BM25 Only (`unicode_word`, $k_1=1.5, b=0.75$).
- 3 Dense-BM25 Rescoring (Dense Top-30 rescored with BM25).
- 6 Hybrid BM25 (RRF $k=60$ and Min-Max Weighted 0.6/0.4).
- 1 TF-IDF Only.
- 6 Hybrid TF-IDF (RRF $k=60$ and Min-Max Weighted 0.6/0.4).

---

## 8. Stage Recall Analysis (Depth 30 -> Union -> Depth 10 -> Depth 5)

| Setting Key | Dense R@30 | Sparse R@30 | Candidate Union R | Fusion R@10 | Final R@5 |
|---|---|---|---|---|---|
| `dense__e5-small-384` | 0.9481 | - | 0.9481 | 0.8852 | 0.8185 |
| `dense__huydang-dek21-embedding-768` | 0.9593 | - | 0.9593 | 0.9148 | 0.8370 |
| `dense__e5-base-768` | 0.9630 | - | 0.9630 | 0.9074 | 0.8407 |
| `bm25-only` | - | 0.9519 | 0.9519 | 0.8667 | 0.7889 |
| `dense-bm25-rescore__e5-small-384` | 0.9481 | 0.9519 | 0.9481 | 0.9000 | 0.8630 |
| `dense-bm25-rescore__huydang-dek21-embedding-768` | 0.9593 | 0.9519 | 0.9593 | 0.9333 | 0.8852 |
| `dense-bm25-rescore__e5-base-768` | 0.9630 | 0.9519 | 0.9630 | 0.9333 | 0.8963 |
| `hybrid-bm25-rrf__e5-small-384` | 0.9481 | 0.9519 | 0.9778 | 0.9259 | 0.8444 |
| `hybrid-bm25-weighted__e5-small-384` | 0.9481 | 0.9519 | 0.9778 | 0.9148 | 0.8296 |
| `hybrid-bm25-rrf__huydang-dek21-embedding-768` | 0.9593 | 0.9519 | 0.9852 | 0.9407 | 0.8778 |
| `hybrid-bm25-weighted__huydang-dek21-embedding-768` | 0.9593 | 0.9519 | **0.9852** | **0.9556** | **0.9111** |
| `hybrid-bm25-rrf__e5-base-768` | 0.9630 | 0.9519 | 0.9815 | 0.9222 | 0.8407 |
| `hybrid-bm25-weighted__e5-base-768` | 0.9630 | 0.9519 | 0.9815 | 0.9444 | 0.8889 |
| `tfidf-only` | - | 0.9185 | 0.9185 | 0.8481 | 0.7667 |
| `hybrid-tfidf-rrf__e5-small-384` | 0.9481 | 0.9185 | 0.9704 | 0.9037 | 0.8296 |
| `hybrid-tfidf-weighted__e5-small-384` | 0.9481 | 0.9185 | 0.9704 | 0.9037 | 0.8407 |
| `hybrid-tfidf-rrf__huydang-dek21-embedding-768` | 0.9593 | 0.9185 | 0.9815 | 0.9370 | 0.8778 |
| `hybrid-tfidf-weighted__huydang-dek21-embedding-768` | 0.9593 | 0.9185 | **0.9815** | **0.9519** | **0.9111** |
| `hybrid-tfidf-rrf__e5-base-768` | 0.9630 | 0.9185 | 0.9778 | 0.9148 | 0.8444 |
| `hybrid-tfidf-weighted__e5-base-768` | 0.9630 | 0.9185 | 0.9778 | 0.9333 | 0.8667 |

---

## 9. Quality Metrics & Fusion Comparisons

| # | Setting Key | Setting Label | Recall@5 | Δ Recall@5 | nDCG@5 | Δ nDCG@5 | MRR@5 | p95 Latency (ms) |
|---|---|---|---|---|---|---|---|---|
| 01 | `dense__e5-small-384` | Dense: E5-small 384D | 0.8185 | 0.0000 | 0.7425 | 0.0000 | 0.7088 | 24.8 |
| 02 | `dense__huydang-dek21-embedding-768` | Dense: Huydang DEk21 768D | 0.8370 | 0.0000 | 0.7164 | 0.0000 | 0.6698 | 62.9 |
| 03 | `dense__e5-base-768` | Dense: E5-base 768D | 0.8407 | 0.0000 | 0.7061 | 0.0000 | 0.6559 | 61.5 |
| 04 | `bm25-only` | Sparse: BM25 Only | 0.7889 | - | 0.6478 | - | 0.5960 | 6.3 |
| 05 | `dense-bm25-rescore__e5-small-384` | Rescore: E5-small -> BM25 | 0.8630 | +0.0444 | 0.7545 | +0.0120 | 0.7073 | 32.2 |
| 06 | `dense-bm25-rescore__huydang-dek21-embedding-768` | Rescore: Huydang -> BM25 | 0.8852 | +0.0481 | 0.7487 | +0.0323 | 0.6971 | 88.3 |
| 07 | `dense-bm25-rescore__e5-base-768` | Rescore: E5-base -> BM25 | 0.8963 | +0.0556 | 0.7659 | +0.0598 | 0.7147 | 73.7 |
| 08 | `hybrid-bm25-rrf__e5-small-384` | Hybrid: E5-small + BM25 (RRF) | 0.8444 | +0.0259 | 0.7221 | -0.0204 | 0.6729 | 32.6 |
| 09 | `hybrid-bm25-weighted__e5-small-384` | Hybrid: E5-small + BM25 (Weighted) | 0.8296 | +0.0111 | 0.7208 | -0.0217 | 0.6797 | 36.5 |
| 10 | `hybrid-bm25-rrf__huydang-dek21-embedding-768` | Hybrid: Huydang + BM25 (RRF) | 0.8778 | +0.0407 | 0.7567 | +0.0403 | 0.7107 | 63.0 |
| 11 | `hybrid-bm25-weighted__huydang-dek21-embedding-768` | Hybrid: Huydang + BM25 (Weighted) | 0.9111 | **+0.0741** | **0.7655** | **+0.0491** | **0.7076** | 65.4 |
| 12 | `hybrid-bm25-rrf__e5-base-768` | Hybrid: E5-base + BM25 (RRF) | 0.8407 | 0.0000 | 0.7160 | +0.0099 | 0.6698 | 66.8 |
| 13 | `hybrid-bm25-weighted__e5-base-768` | Hybrid: E5-base + BM25 (Weighted) | 0.8889 | +0.0481 | 0.7560 | +0.0499 | 0.7064 | 66.3 |
| 14 | `tfidf-only` | Sparse: TF-IDF Only | 0.7667 | - | 0.6150 | - | 0.5599 | 5.1 |
| 15 | `hybrid-tfidf-rrf__e5-small-384` | Hybrid: E5-small + TF-IDF (RRF) | 0.8296 | +0.0111 | 0.6920 | -0.0505 | 0.6416 | 34.3 |
| 16 | `hybrid-tfidf-weighted__e5-small-384` | Hybrid: E5-small + TF-IDF (Weighted) | 0.8407 | +0.0222 | 0.7047 | -0.0378 | 0.6558 | 32.8 |
| 17 | `hybrid-tfidf-rrf__huydang-dek21-embedding-768` | Hybrid: Huydang + TF-IDF (RRF) | 0.8778 | +0.0407 | 0.7322 | +0.0159 | 0.6775 | 64.5 |
| 18 | `hybrid-tfidf-weighted__huydang-dek21-embedding-768` | Hybrid: Huydang + TF-IDF (Weighted) | **0.9111** | **+0.0741** | 0.7424 | +0.0260 | 0.6778 | 62.4 |
| 19 | `hybrid-tfidf-rrf__e5-base-768` | Hybrid: E5-base + TF-IDF (RRF) | 0.8444 | +0.0037 | 0.6929 | -0.0132 | 0.6385 | 79.4 |
| 20 | `hybrid-tfidf-weighted__e5-base-768` | Hybrid: E5-base + TF-IDF (Weighted) | 0.8667 | +0.0259 | 0.7181 | +0.0120 | 0.6659 | 61.0 |

---

## 10. Category Guardrail Analysis (Specifically Explaining `relationship` $n=14$)

The 45 Golden V3 cases are partitioned into 9 categories:
- `comparative`: $n=6$
- `direct_fact`: $n=7$
- `food_knowledge`: $n=7$
- `guide_planning`: $n=2$
- `holistic`: $n=3$
- `numerical`: $n=2$
- `relationship`: $n=14$
- `spanning`: $n=3$
- `temporal`: $n=1$

### Exact Observed Guardrail Evaluation in `relationship` ($n=14$)
From current durable artifact `phase8_sparse_results.csv`:
- Dense control `dense__huydang-dek21-embedding-768`:
  - Recall@5 = `1.0` (14/14 cases hit)
  - nDCG@5 = `0.8586955762164405` (~`0.8587`)
  - MRR@5 = `0.869047619047619` (~`0.8690`)
- Candidate `hybrid-bm25-weighted__huydang-dek21-embedding-768`:
  - Recall@5 = `1.0` (14/14 cases hit)
  - nDCG@5 = `0.8307682576866561` (~`0.8308`)
  - MRR@5 = `0.8035714285714286` (~`0.8036`)
  - $\Delta \text{nDCG@5} = 0.8307683 - 0.8586956 = \mathbf{-0.0279273}$
- Candidate `hybrid-tfidf-weighted__huydang-dek21-embedding-768`:
  - Recall@5 = `1.0` (14/14 cases hit)
  - nDCG@5 = `0.8307682576866561` (~`0.8308`)
  - MRR@5 = `0.8035714285714286` (~`0.8036`)
  - $\Delta \text{nDCG@5} = 0.8307683 - 0.8586956 = \mathbf{-0.0279273}$

Because the approved scientific guardrail threshold requires $\Delta \text{nDCG@5} \ge -0.02$ for categories with $n \ge 6$, the delta of $-0.0279273$ violates the limit. Consequently:
- `category_guardrail_pass` for `relationship` evaluated to `False`.
- `all_category_guardrails_pass` evaluated to `False`.
- `finalist_eligible` evaluated to `False`.
- **Fail-Closed Result**: `bm25_finalist = None`, `tfidf_finalist = None` (strictly returned `None` without manual bypass).

---

## 11. Latency, Throughput & Resource Consumption

- `dense__e5-small-384`: warm p95 = 24.8 ms, RSS = 245 MB.
- `dense__huydang-dek21-embedding-768`: warm p95 = 62.9 ms, RSS = 480 MB.
- `bm25-only`: warm p95 = 6.3 ms, RSS = 3.3 MB.
- `hybrid-bm25-weighted__huydang-dek21-embedding-768`: warm p95 = 65.4 ms (within $2.0 \times$ latency gate).
- `hybrid-tfidf-weighted__huydang-dek21-embedding-768`: warm p95 = 62.4 ms.

---

## 12. Bootstrap 95% Confidence Intervals & Finalist Selection

- **Paired Bootstrap (10,000 samples, seed 42)**:
  - `hybrid-bm25-weighted__huydang`:
    - $\Delta \text{Recall@5} \in [+0.0370, +0.1111]$ (statistically significant improvement).
    - $\Delta \text{nDCG@5} \in [+0.0062, +0.0915]$ (statistically significant improvement).
- **Finalist Selection**:
  - `bm25_finalist`: `None`
  - `tfidf_finalist`: `None`
  - Strict compliance with fail-closed scientific gate without manual relaxation.

---

## 13. Production Protection and Data Integrity Audit

- **Active Collection**: `hue_foods_e5_small_384` (572 points). Snapshots before and after every setting and batch match 100%.
- **Zero Production Mutation**: Active production database remained completely untouched throughout all runs.

---

## 14. Negative Audits & Fail-Closed Behavior Verification

- **Missing Live Arguments**: Calling `reconcile_sparse_benchmark` without `inputs`, `expected_active_snapshot`, explicit `client`, or `tfidf_state` immediately returns `complete = False`.
- **Immutable Identity Validation**: Any mismatch in `selected_tokenizer`, `tfidf.formula_version`, `fusion`, `dense_prerequisites`, `selected_bm25`, or fingerprints immediately causes rejection (`complete = False`).
- **Non-Canonical Case IDs**: Any case ID differing from canonical Golden V3 45 cases causes rejection (`complete = False`).
- **Count-Only / Malformed TF-IDF Collection**: Missing sparse vectors configuration or malformed payloads fails gracefully without raising `AttributeError` (`complete = False`).
- **Secret Sanitization (Allowlist/Bounded Category Design)**: All unquoted, single-quoted, double-quoted, quoted Bearer, and multiline traceback secret forms are 100% redacted into generic bounded descriptions (`ExceptionType: safe description`) with mathematical guarantee of 0 raw provider payload leaks.
- **Read-Only Hash Stability**: Running batch and reconciliation on completed checkpoint causes **0 file writes** and preserves identical SHA256 hashes across all 4 durable artifacts.

---

## 15. Limitations, Failures & Handoff Contract for Reviewer

### Limitations & Failures
- No candidate passed all 9 category guardrails automatically due to the $-0.02$ threshold in `relationship` ($n=14$).
- Reranking and Generation are not tested in 08b (reserved for 08c and Phase 6+).

### Handoff Contract & Exact Reviewer Commands

```bash
# 1. Run all test suites (85 passed)
cd /home/minhhieu/hue_rag/backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08b-test-uv-cache uv run --group evaluation --env-file ../.env python -m pytest tests/test_sparse_benchmark.py tests/test_embedding_benchmark.py tests/test_bm25.py tests/test_retrieval_service.py -q --tb=short

# 2. Check git diff format
cd /home/minhhieu/hue_rag
git diff --check 93109c2e383f7f19554e2ceb03f10f8c199bc8ea

# 3. Check read-only notebook execution
UV_CACHE_DIR=/tmp/hue-rag-phase8-08b-test-uv-cache uv run --group evaluation jupyter nbconvert --to notebook --execute notebooks/08b_retrieval_fusion_benchmark.ipynb --output /tmp/reviewer_test_executed_notebook.ipynb --ExecutePreprocessor.timeout=1800
```
