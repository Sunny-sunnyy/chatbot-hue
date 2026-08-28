# Phase 8 — Notebook 08a Dense Embedding Benchmark Design

Date: 2026-08-28 (+07)

Status: design and implementation plan approved by the user on 2026-08-28.
The user authorized the exact Notebook 08a implementation and real local Run
All described by those documents, including pinned model downloads and writes
only to the seven approved isolated Qdrant collections. Paid calls, active
collection mutation, production cutover and later Notebook 08 groups remain
unauthorized.

## Purpose

Notebook 08a teaches and measures seven local dense embedding configurations on
the Hue food corpus. It uses Golden Dataset V3, production chunking and dense
retrieval semantics, and isolated Qdrant collections. Its output is technical
evidence for later model selection, not a production cutover.

The notebook must help a person understand the system. Markdown is Vietnamese,
identifiers are English, each cell has one purpose, and code cells stay short by
calling backend functions.

## Relationship to current retrieval profiles

The repository has three pipeline capabilities:

    dense_only:
      retrieval_mode: dense
      use_bm25: false
      use_reranker: false
    hybrid_no_rerank:
      retrieval_mode: hybrid
      use_bm25: true
      use_reranker: false
    hybrid_rerank:
      retrieval_mode: hybrid
      use_bm25: true
      use_reranker: true

Notebook 08a fixes every run to dense_only. This isolates the embedding
variable. The two hybrid profiles remain existing capabilities but are not
executed or modified here:

- Notebook 08b researches BM25, sparse and fusion behavior without reranking.
- Notebook 08c researches rerankers on fixed pre-rerank inputs.
- Notebook 08d combines approved embedding, retrieval and reranker finalists.

## Approved scope

08a compares exactly these configurations in this order:

1. multilingual E5-small 384D, the fixed control;
2. multilingual MiniLM-L12 384D;
3. multilingual E5-base 768D;
4. multilingual E5-large 1024D;
5. BGE-M3 dense 1024D;
6. Qwen3 Embedding 0.6B with official 384D truncation;
7. Qwen3 Embedding 0.6B native 1024D.

It uses real local models, CPU FP32, the canonical 572 chunks, all 45 Golden V3
cases, actual isolated Qdrant targets, and production backend data paths.

## Explicit non-scope

08a does not implement, run, review or authorize:

- BGE-M3 learned sparse or ColBERT vectors;
- BM25, dense-to-BM25 rescoring or true-hybrid fusion;
- reranking, generation or LLM judging;
- paid APIs;
- Golden Dataset changes based on candidate results;
- production configuration changes or collection cutover;
- GPU, quantization or mixed precision;
- a registry, validator framework, audit package, run identity, resume engine,
  mock integration or speculative abstraction.

## Exact model settings

All revisions below were observed from official repositories on 2026-08-28 and
are pinned during loading.

| Order | Setting key | Model ID | Revision | License | Dim | Max | Collection |
|---:|---|---|---|---|---:|---:|---|
| 1 | e5-small-384 | intfloat/multilingual-e5-small | 614241f622f53c4eeff9890bdc4f31cfecc418b3 | MIT | 384 | 512 | hue_foods_08a_e5_small_384 |
| 2 | multilingual-minilm-l12-384 | sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 | e8f8c211226b894fcb81acc59f3b34ba3efd5f42 | Apache-2.0 | 384 | 128 | hue_foods_08a_minilm_l12_384 |
| 3 | e5-base-768 | intfloat/multilingual-e5-base | d128750597153bb5987e10b1c3493a34e5a4502a | MIT | 768 | 512 | hue_foods_08a_e5_base_768 |
| 4 | e5-large-1024 | intfloat/multilingual-e5-large | 3d7cfbdacd47fdda877c5cd8a79fbcc4f2a574f3 | MIT | 1024 | 512 | hue_foods_08a_e5_large_1024 |
| 5 | bge-m3-dense-1024 | BAAI/bge-m3 | 5617a9f61b028005a4858fdac845db406aefb181 | MIT | 1024 | 512 | hue_foods_08a_bge_m3_1024 |
| 6 | qwen3-embedding-0.6b-384 | Qwen/Qwen3-Embedding-0.6B | 97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3 | Apache-2.0 | 384 | 512 | hue_foods_08a_qwen3_06b_384 |
| 7 | qwen3-embedding-0.6b-1024 | Qwen/Qwen3-Embedding-0.6B | 97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3 | Apache-2.0 | 1024 | 512 | hue_foods_08a_qwen3_06b_1024 |

Official sources:

- https://huggingface.co/intfloat/multilingual-e5-small
- https://huggingface.co/intfloat/multilingual-e5-base
- https://huggingface.co/intfloat/multilingual-e5-large
- https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- https://huggingface.co/BAAI/bge-m3
- https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
- https://github.com/QwenLM/Qwen3-Embedding
- https://github.com/FlagOpen/FlagEmbedding

Qwen 384D and 1024D are separate vector spaces. Qwen 384D never shares the
E5-small collection merely because both have 384 dimensions.

Exact human-readable labels are:

- `E5-small 384D (control)`;
- `Multilingual MiniLM-L12 384D`;
- `E5-base 768D`;
- `E5-large 1024D`;
- `BGE-M3 dense 1024D`;
- `Qwen3 Embedding 0.6B 384D`;
- `Qwen3 Embedding 0.6B native 1024D`.

Every setting also records the same locked 08a profile fields:

    retrieval_mode: dense
    use_bm25: false
    use_reranker: false

## Native encoding contracts

All query and document vectors are L2-normalized after native pooling. Qwen
384D is normalized after official SentenceTransformers truncation.

### E5 family

- Load the pinned revision with SentenceTransformers.
- Prefix documents with passage: and queries with query:.
- Use the model attention-mask mean pooling.
- Cap tokenized input at 512 tokens.

### Multilingual MiniLM-L12

- Use raw query and document text.
- Use the model mean-pooling configuration.
- Keep its native maximum of 128 tokens.

### Qwen3 Embedding 0.6B

- Use last-token pooling.
- Keep documents raw.
- Use this exact query instruction:

    Instruct: Với một câu hỏi du lịch ẩm thực Huế, hãy truy xuất các đoạn văn liên quan có thể trả lời câu hỏi.
    Query: {question}

- The 384D setting passes official truncate_dim=384. Manual slicing and PCA are
  forbidden.
- The 1024D setting uses native output.

### BGE-M3 dense

- Add and pin FlagEmbedding==1.4.0.
- Download the pinned model snapshot and pass its local path to BGEM3FlagModel.
- Use CPU FP32, raw text, CLS pooling and dense output only.
- Never request sparse weights or ColBERT vectors.
- Consume dense_vecs from the official underlying BGE-M3 model.

The public FlagEmbedding encoding path silently reduces batch size after
RuntimeError or OOM. That violates the approved no-auto-shrink contract. The
approved adapter therefore:

1. loads BGEM3FlagModel from the pinned snapshot;
2. creates exact external batches of eight documents or one query;
3. invokes its official tokenizer and underlying model once per batch;
4. requests dense output only and reads outputs["dense_vecs"];
5. fails immediately if the exact batch cannot run.

Pooling and normalization remain inside the official BGE-M3 model. The adapter
does not recreate those algorithms. Because this relies on
BGEM3FlagModel.tokenizer and .model, compatibility with FlagEmbedding==1.4.0
must be verified live. If unavailable in the locked environment, implementation
is blocked and the design is reopened; no fallback is allowed.

## Execution profile

Every configuration uses:

- device: CPU;
- dtype: float32;
- quantization: none;
- document batch size: 8;
- query batch size: 1;
- dense candidate depth: 30;
- final metric depth: 5;
- one discarded warm-up using case foods-v3-0001;
- three complete repetitions of all 45 cases.

There is no silent retry, batch shrink, device/dtype/revision change or model
fallback.

## Backend architecture

Implementation adds two focused modules.

### backend/embedding/dense_benchmark.py

This module owns model loading and dense encoding only. It contains:

- DenseBenchmarkSetting;
- E5_SMALL_SETTING;
- DENSE_CANDIDATE_SETTINGS in approved order;
- SentenceTransformerDenseRunner;
- Qwen3DenseRunner;
- BGEM3DenseRunner;
- build_dense_runner(setting), using explicit if/elif branches.

There is no dynamic registry, plug-in system, inheritance hierarchy or
validator framework. The notebook cannot supply arbitrary prefixes, pooling
modes or Qwen instructions.

Every runner exposes:

    load()
    embed_documents(texts)
    embed_query(query)
    close()

Every runner checks vector count, dimension and finite values.

Production E5Embedder, startup wiring and active settings remain unchanged. The
control uses equivalent E5 model, prefix and normalization semantics, protected
by focused regression evidence.

### backend/evaluation/embedding_benchmark.py

This module owns one-setting orchestration and deterministic comparison logic:

    canonical chunks
    -> model load
    -> document encoding
    -> isolated dense collection
    -> discarded warm-up
    -> 3 x 45 dense retrieval
    -> metrics and category aggregation
    -> paired bootstrap and gates
    -> cumulative CSV upsert

It reuses production chunking, point-building, Qdrant schema and dense retrieval
behavior. It contains no BM25, fusion, reranking, generation or provider calls.

## Canonical inputs and collection safety

Before model loading, the backend:

1. loads all 45 rows from knowledge-base-hue/foods/evaluation/golden_v3.jsonl;
2. creates 572 chunks with production chunk_foods_markdown();
3. confirms canonical count and required source/section metadata;
4. records a read-only active hue_foods_e5_small_384 snapshot containing only
   name, vector schema and exact point count.

The active collection is never benchmark input or a write target. Even the
control writes only to hue_foods_08a_e5_small_384.

Each isolated collection is dense-only, has named dense vectors with cosine
distance, and receives deterministic UUID5 points from canonical chunks. Create
when absent. When present with exact schema, deterministically upsert. On schema
mismatch, fail without deletion or recreation.

Read the active snapshot after the baseline and after all candidates. Changed
schema or count prevents a successful conclusion. Diff review also confirms
that every write target is an approved isolated name.

Isolated collections remain through technical review. Notebook 08a does not
delete them or perform cutover.

## One-setting lifecycle

For each setting:

1. record RSS before load;
2. load the pinned model once and measure cold load;
3. record RSS after load;
4. count documents whose exact preprocessed tokens exceed max length;
5. encode 572 documents with batch size 8;
6. check vector count, dimension and finite values;
7. create or upsert the isolated collection;
8. run and discard one fixed warm-up;
9. run three complete 45-case repetitions in the same order;
10. retain per-case rankings from each repetition;
11. derive canonical quality from repetition one;
12. report exact ranking variation rather than averaging it away;
13. compute gates/comparisons when a reference exists;
14. upsert CSV rows, including failure rows;
15. yield a human-readable summary to the notebook;
16. close the model, release large objects and run garbage collection.

Measure query embedding, retrieval and combined warm latency separately.
Report p50/p95. Memory observation is limited to RSS before load, RSS after
load, after document embedding, and after each full repetition.
observed_peak_rss_mb is the maximum of only those explicit checkpoints; no
profiler or background sampling timeline is introduced.

## Failure behavior

Allowed statuses are:

- completed: all three full repetitions succeeded;
- partial: observed results exist but fewer than three full repetitions worked;
- failed: no valid completed result exists.

The error field contains ExceptionType: sanitized message. It never contains
secrets, raw headers, provider payloads or sensitive stack traces.

After failure, persist the setting row, release resources and continue to the
next independent setting. Never retry, shrink, change device/dtype/revision or
substitute a model.

## Metrics

Relevance is binary exact canonical source + section. It does not use keywords,
an LLM label or stored chunk IDs.

Each declared source + section pair can receive credit at most once in one
ranked list. If multiple chunks from the same relevant section appear in Top 5,
only the highest-ranked chunk represents that evidence pair; later duplicates
receive zero gain. This keeps Recall and nDCG bounded by the declared evidence
rather than by chunk duplication.

For every case:

- Recall@5 is the fraction of declared relevant evidence represented in Top 5.
- MRR@5 is reciprocal rank of the first relevant result, or zero.
- nDCG@5 is binary DCG relative to the ideal declared-evidence ranking.
- A hit means at least one relevant source + section appears in Top 5.

Overall/category quality comes from repetition one. Three repetitions establish
3/3 eligibility and reveal ranking instability.

## Category guardrails

All nine categories are protected.

For categories with n >= 6:

1. candidate hit-case count cannot be lower than the reference;
2. when hit counts tie, fail if delta nDCG@5 < -0.02;
3. MRR@5 is supporting information.

For categories with n <= 3, apply an exact per-case guardrail: if the reference
has relevant Top-5 evidence, the candidate cannot lose all evidence for that
case. Rank movement within Top 5 alone is not a blocker.

## Bootstrap and clear gain

Use 45 paired candidate-reference per-case score pairs:

- 10,000 resamples;
- seed 42;
- 95% percentile CI;
- delta Recall@5, MRR@5 and nDCG@5.

Clear gain versus control requires:

- status completed;
- successful repetitions equal 3;
- all category guardrails pass;
- aggregate delta nDCG@5 >= 0.03;
- lower 95% CI for delta nDCG@5 > 0.

Every candidate compares with E5-small. A candidate that clears it becomes a
survivor.

Approved order defines lighter. For a heavier survivor, select the best earlier
survivor by nDCG@5, then MRR@5, then Recall@5, then earlier approved order.
E5-small is the initial lighter reference. A heavier survivor must pass the same
clear-gain rule against that best lighter finalist. Otherwise prefer the lighter
finalist. No composite score is allowed.

## Durable CSV

Notebook 08a writes exactly:

    evaluation/results/phase8_embedding_results.csv

The CSV is long format: category=overall plus one row for each of nine
categories per setting. Approved reruns replace matching setting_key + category
rows and preserve other settings. There is no run history, ID, timestamped
package, checksum manifest or duplicate JSON.

Columns:

    setting_key
    setting_label
    category
    model_id
    model_revision
    dimension
    max_length
    collection_name
    retrieval_mode
    use_bm25
    use_reranker
    status
    error
    case_count
    hit_case_count
    recall_at_5
    mrr_at_5
    ndcg_at_5
    successful_repetitions
    ranking_stable
    truncated_document_count
    cold_load_ms
    document_embedding_ms
    query_embedding_p50_ms
    query_embedding_p95_ms
    retrieval_p50_ms
    retrieval_p95_ms
    warm_total_p50_ms
    warm_total_p95_ms
    rss_before_load_mb
    rss_after_load_mb
    observed_peak_rss_mb
    device
    dtype
    document_batch_size
    query_batch_size
    delta_recall_at_5
    delta_mrr_at_5
    delta_ndcg_at_5
    recall_ci_lower
    recall_ci_upper
    mrr_ci_lower
    mrr_ci_upper
    ndcg_ci_lower
    ndcg_ci_upper
    category_guardrail_pass
    all_category_guardrails_pass
    clear_gain_vs_control
    best_lighter_setting
    clear_gain_vs_best_lighter
    finalist_eligible

Run-level resource/latency values appear only on category=overall. Baseline
delta/CI/comparison fields are blank. A completed 3/3 setting is
finalist-eligible; ranking variation remains separately visible and reviewed.

## Notebook structure

notebooks/08a_embedding_benchmark.ipynb has about 26 alternating Markdown/code
cells in seven sections.

### 1. Purpose and scope

- Show the three current profiles.
- Explain why 08a fixes dense_only and defers hybrid/reranking.
- Import backend functions without model loading.

### 2. Environment

- Explain CPU FP32, batches, repetitions and expected long runtime.
- Display only safe package, CPU, RAM, Qdrant and device information.

### 3. Canonical inputs

- Load through backend functions.
- Show a few Golden cases and chunk metadata.
- Show 45 category counts and 572 chunks.
- Explain source + section relevance.

### 4. Settings and isolation

- Display seven pinned settings.
- Explain isolated collections.
- Capture/display the safe active snapshot.

### 5. Fixed E5-small control

One cell runs:

    control_result = run_embedding_benchmark(
        E5_SMALL_SETTING,
        benchmark_inputs,
    )

A later cell displays its summary and category rows.

### 6. Six candidates

One cell runs all six sequentially:

    candidate_results = []

    for result in run_embedding_benchmarks(
        DENSE_CANDIDATE_SETTINGS,
        benchmark_inputs,
        control_result=control_result,
    ):
        candidate_results.append(result)
        display(result.summary)

The loop is presentation only. Backend orchestration encodes, retrieves,
measures, persists and cleans up before yielding.

### 7. Comparison and conclusion

- Show separate quality, bootstrap/gate, latency, resource, truncation and
  failure views.
- Show lighter-versus-heavier decisions.
- Show CSV path and final active comparison.
- State that results are not cutover or total Phase 8 approval.

Markdown is short and immediately precedes related code. Notebook contains no
encoding, retrieval, metric, bootstrap, CSV or collection mutation logic.
Repository outputs are empty and execution counts null. Reviewer execution goes
only to a temporary copy.

## Dependency change

Current lock includes:

- sentence-transformers==5.6.1;
- transformers==5.14.1;
- torch==2.13.0;
- qdrant-client==1.19.0.

Implementation adds FlagEmbedding==1.4.0 to pyproject.toml and uv.lock. There is
no second environment or notebook installation cell. Dependency or Python 3.13
integration failure reopens the design; versions are not changed silently.

## Exact implementation file scope

Implementation may create/change only:

- pyproject.toml;
- uv.lock;
- backend/embedding/dense_benchmark.py;
- backend/evaluation/embedding_benchmark.py;
- backend/tests/test_embedding_benchmark.py;
- notebooks/08a_embedding_benchmark.ipynb;
- evaluation/results/phase8_embedding_results.csv after an authorized run;
- reports/phase_8_08a_embedding_benchmark_implementation_report.md.

Production E5 runtime, startup/config, retrieval profiles, Golden V3, BM25,
reranking and generation stay unchanged. Any changed file outside this scope is
an out-of-scope finding.

## Automated verification

Tests cover only reusable deterministic behavior:

1. exact Recall@5, MRR@5 and nDCG@5 from source + section;
2. overall/category aggregation;
3. large-category guardrails;
4. small-category per-case guardrails;
5. paired bootstrap with 10,000 resamples and seed 42;
6. clear-gain logic;
7. best-lighter-finalist selection;
8. CSV upsert by setting_key + category.

Tests do not mock models or Qdrant to claim integration success. Test count and
coverage are not acceptance criteria.

Focused command from backend/:

    HF_HUB_OFFLINE=1 \
    UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-test-uv-cache \
    uv run --env-file ../.env \
    python -m pytest tests/test_embedding_benchmark.py -q --tb=short

## Independent real Run All

Reviewer runs from repository root:

    UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-review-uv-cache \
    uv run --env-file .env \
    jupyter nbconvert \
      --execute \
      --to notebook \
      notebooks/08a_embedding_benchmark.ipynb \
      --output /tmp/08a_embedding_benchmark-review-live.ipynb \
      --ExecutePreprocessor.timeout=28800

The run uses real pinned models, full canonical inputs, actual isolated Qdrant
collections and production backend functions. Smoke data, fake vectors, mocks,
replay and old output are not PASS evidence.

After Run All, Reviewer:

1. reconciles CSV with the temporary notebook;
2. independently recomputes at least one sample metric and gate;
3. confirms Qwen 384D used official truncate_dim=384;
4. compares one successful exact BGE adapter batch with public dense_vecs when
   the public call succeeds without shrinking;
5. confirms all seven isolated collections have 572 points and dimensions;
6. confirms active schema/count and production config are unchanged;
7. parses the repository notebook and confirms clean outputs/counts;
8. runs focused tests and git diff --check;
9. reads the complete diff and all changed files.

Dependency, download, Qdrant or RAM failure is reported as failed, partial or
blocked. No benchmark setting is changed to manufacture PASS.

## Review and approval boundaries

Implementer writes
reports/phase_8_08a_embedding_benchmark_implementation_report.md after an
authorized implementation/run. Reviewer writes
reports/phase_8_08a_embedding_benchmark_codex_review.md and, only for
ready_for_user_confirmation, the matching user report.

Technical readiness does not approve 08a automatically. The user must inspect
and confirm the notebook. Only then may canonical guide/design/plan,
guides/README.md, Project_Status.md and the reports index mark 08a approved and
move to Notebook 08b research/brainstorming. Phase 8 remains not_ready.

No commit or push is part of this workflow.
