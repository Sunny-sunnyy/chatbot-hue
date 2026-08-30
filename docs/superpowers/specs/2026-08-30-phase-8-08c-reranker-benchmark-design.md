# Phase 8 — Notebook 08c MiniLM Reranker Benchmark Design

Date: 2026-08-30 (+07)

Status: `approved_design` by the user on 2026-08-30 (+07). The separate
implementation plan and Review Contract were approved by the user later that
day; exact implementation and real local MiniLM execution are now authorized
through the current Implementer handoff.

## Purpose

Notebook 08c determines whether the existing lightweight MiniLM reranker improves
or harms final Top-5 ranking on three representative, fixed Foods Top-10 inputs.
It compares evidence and reports trade-offs to the user; it does not select or
activate a production pipeline automatically.

The only reranker candidate is
`cross-encoder/ms-marco-MiniLM-L-6-v2`. BGE and Qwen rerankers are removed from
the active Phase 8 scope because their additional resource, integration and
maintenance cost is not needed for the current decision. Historical records may
retain them only as superseded context.

## Scope and fixed inputs

08c compares exactly two states:

1. `no-rerank`: the first five documents of the fixed pre-rerank Top 10;
2. `minilm`: the current Hue RAG `CrossEncoderReranker` scores the same Top 10
   and returns Top 5.

It uses exactly three 08b setting keys:

1. `dense__e5-small-384` — current production embedding control;
2. `dense__huydang-dek21-embedding-768` — Vietnamese-specialized dense input;
3. `hybrid-bm25-weighted__huydang-dek21-embedding-768` — high-recall diagnostic
   input used to test whether MiniLM repairs the observed `relationship`
   ranking regression.

The hybrid input is not an 08b finalist and is not silently promoted. A repaired
hybrid result is only evidence for a later user decision about 08d.

## Explicit non-scope

08c does not:

- query retrieval again or modify 08a/08b artifacts;
- benchmark BGE, Qwen or another reranker;
- create a generic reranker interface or evaluation-only model adapter;
- modify `backend/reranking/cross_encoder.py` or production settings;
- change Golden V3, curated Foods data, chunking or Qdrant;
- run generation, judging or paid APIs;
- select or cut over a production pipeline;
- curate festivals, heritage, performing arts or tourism data.

## Architecture and data flow

```text
Golden V3 + 572 canonical chunks
              |
phase8_sparse_manifest.json + phase8_sparse_cases.jsonl
              |
select 3 setting keys x 45 completed cases
              |
read immutable fusion_top_10 and map chunk_id to canonical text
              |
       +------+------+
       |             |
no-rerank Top 5   current MiniLM rerank Top 10 -> Top 5
       |             |
       +------+------+
              |
quality, category, bootstrap, latency and stability evidence
              |
Reviewer report -> user decision
```

`backend/evaluation/reranker_benchmark.py` owns input validation, canonical
text mapping, orchestration, metrics and persistence. The notebook remains a
short Vietnamese learning layer that calls backend functions directly.

## Input contract

The benchmark reads the approved 08b manifest and per-case JSONL. It validates:

- exact experiment version `phase8-08b-v1`;
- the three approved setting keys only;
- exactly 45 completed cases with `fusion_top_10` for each setting;
- exactly 135 selected input records;
- ten unique canonical `chunk_id` values per input ranking;
- every selected ID maps to current text from exactly 572 canonical chunks;
- Golden, corpus and chunker identity agrees with approved 08b evidence.

Any mismatch stops before MiniLM loads. 08c does not copy the 135 inputs into a
new artifact and does not query Qdrant to regenerate them.

## Runtime model contract

08c calls the existing `backend/reranking/cross_encoder.py` implementation
directly. It does not introduce benchmark-only inference behavior.

The run records:

- actual model ID and resolved revision when available;
- Sentence Transformers, Transformers and Torch versions;
- device `cpu` and FP32 execution;
- cold load time;
- warm rerank p50/p95 for each fixed input;
- process RSS before/after load and observed peak RSS at explicit boundaries;
- ranking stability across repetitions.

Official current compatibility research confirms that Sentence Transformers
`CrossEncoder` still accepts text pairs and exposes direct `predict` inference.
MiniLM was trained on English MS MARCO, so successful inference is integration
evidence only; Golden V3 decides its Vietnamese quality.

Primary references checked on 2026-08-30 (+07):

- https://www.sbert.net/docs/package_reference/cross_encoder/model.html
- https://www.sbert.net/docs/cross_encoder/usage/usage.html
- https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2

If the runtime exposes no resolved model revision without changing the current
class, record `not_reported`; that is a limitation, not permission to add a
revision-discovery adapter.

## Execution protocol

1. Validate all canonical and fixed-input prerequisites.
2. Load MiniLM once.
3. Run one warm-up prediction excluded from measurements.
4. Run a 10-case technical smoke check.
5. Run the three fixed inputs sequentially over all 45 cases, three repetitions
   per input.
6. Persist each completed input atomically before continuing.
7. Release the model and large temporary objects after completion.

There is no model reload between inputs, auto-retry, fallback, device change or
changed input. A model load failure blocks all scoring. An input-scoring failure
is persisted as failed and independent inputs may continue.

## Metrics and evidence flags

For every input, `no-rerank` is the paired fixed control. Report:

- Recall@5, MRR@5 and nDCG@5;
- hit-case count and all nine Golden V3 category slices;
- exact gained/lost relevant cases and relevant-rank movement;
- paired bootstrap over 45 case pairs using 10,000 resamples, seed 42 and 95%
  percentile intervals;
- latency, resource use and three-repetition ranking stability.

Keep the approved Gate 1 category rules:

- categories with at least six cases cannot lose hit@5 cases; when hit counts
  tie, `delta nDCG@5` must be at least `-0.02`;
- categories with fewer than six cases cannot lose all relevant Top-5 evidence
  for a case hit by the control.

Each MiniLM/input pairing receives two descriptive evidence flags:

- `eligible`: 3/3 repetitions complete, ranking is stable, all category
  guardrails pass and warm rerank p95 for ten pairs is at most three seconds;
- `clear_gain`: the pairing is eligible, aggregate `delta nDCG@5 >= +0.03` and
  the bootstrap 95% lower bound for delta nDCG@5 is greater than zero.

The hybrid diagnostic has an additional `production_safety` comparison against
E5-small no-rerank. It must pass the same category guardrails and its aggregate
Recall@5 may not be more than `0.005` below that production control.

Flags do not approve a winner. Reviewer reports the observed evidence and the
user decides which pairings, if any, continue.

## Durable evidence

08c writes exactly two cumulative artifacts:

```text
evaluation/results/phase8_reranker_results.csv
evaluation/results/phase8_reranker_cases.jsonl
```

The summary CSV contains exactly 60 reconciled rows:

```text
3 inputs x 2 states x (overall + 9 categories)
```

It records readable input/state identity, status/error, metrics, deltas,
bootstrap intervals, category/evidence flags, repetitions, stability and
applicable latency/resource observations.

The per-case JSONL contains exactly 135 reconciled records. Each record contains
case/category identity, relevant evidence, fixed pre-rerank Top 10, no-rerank
Top 5, MiniLM Top 5 and scores, gained/lost status, relevant rank movement,
per-case metrics and three repetition latencies.

The ordered summary CSV columns are:

```text
experiment_version, input_order, input_key, input_label,
state_order, state_key, model_id, model_revision, category,
status, error, case_count, hit_case_count, successful_repetitions,
ranking_stable, recall_at_5, mrr_at_5, ndcg_at_5,
delta_recall_at_5, delta_mrr_at_5, delta_ndcg_at_5,
recall_ci_lower, recall_ci_upper, mrr_ci_lower, mrr_ci_upper,
ndcg_ci_lower, ndcg_ci_upper, category_guardrail_pass,
all_category_guardrails_pass, eligible, clear_gain, production_safety,
cold_load_ms, rerank_p50_ms, rerank_p95_ms,
rss_before_load_mb, rss_after_load_mb, observed_peak_rss_mb,
device, dtype
```

Run/resource fields and aggregate flags appear only on `category=overall` rows
where applicable. Non-applicable values are blank, not fabricated as zero.

The ordered top-level per-case JSON keys are:

```text
experiment_version, input_order, input_key, case_id, category,
status, error, relevant_source_sections, pre_rerank_top_10,
no_rerank_top_5, minilm_top_5, successful_repetitions,
ranking_stable, hit_before, hit_after, hit_change,
relevant_rank_before, relevant_rank_after,
recall_at_5_before, recall_at_5_after,
mrr_at_5_before, mrr_at_5_after,
ndcg_at_5_before, ndcg_at_5_after,
latency_by_repetition_ms
```

`experiment_version` is `phase8-08c-v1`. Ranked document objects retain only
the readable fields needed to audit order: `chunk_id`, `rank`, score, `source`
and `section`. Persisted errors contain an exception type and bounded safe
message, never a raw traceback or secret-bearing payload.

Writes are atomic after each input. An approved rerun replaces the exact input
rows and records. There is no new manifest, run registry, checksum package,
duplicate input artifact or resume engine.

## Notebook structure

The canonical notebook contains short alternating Vietnamese Markdown and code
sections:

1. purpose and Foods-only boundary;
2. environment and actual MiniLM/runtime identity;
3. Golden V3, canonical chunks and fixed-input validation;
4. three no-rerank controls;
5. MiniLM load and warm-up;
6. ten-case smoke;
7. sequential full runs for the three inputs;
8. aggregate and category deltas;
9. gained/lost drill-down, especially `relationship`;
10. latency, resources and stability;
11. evidence flags and user-decision handoff.

Notebook cells do not duplicate evaluation logic or act as validators/tests.
The repository notebook has empty outputs and null execution counts. Reviewer
verification executes a temporary copy through the real MiniLM path.

## Verification contract

Focused deterministic tests cover only:

- exact selection of 135 fixed records;
- canonical chunk mapping and missing/duplicate rejection;
- no-rerank Top-5 and deterministic ranking/tie behavior;
- metrics, category rules, paired bootstrap and production-safety logic using
  existing reusable Phase 8 helpers where possible;
- exact artifact schemas and idempotent per-input replacement.

Mock or fake model output is not completion evidence. Real completion requires
the MiniLM smoke and temporary Notebook Run All on all 45 cases. The review also
checks source-notebook cleanliness, exact 60/135 artifact counts, unchanged
08a/08b artifacts, unchanged Golden/corpus/runtime files and `git diff --check`.

## Documentation synchronization

Before implementation handoff, Reviewer synchronizes active Phase 8 documents:

- mark 08b approved with no BM25/TF-IDF finalist;
- remove BGE/Qwen from active candidate tables, matrices and next-step
  contracts while preserving clearly superseded history;
- replace unsupported production hybrid recommendations with the approved 08b
  verdict;
- describe exact 08c no-rerank/MiniLM scope and three fixed inputs;
- keep multi-domain expansion as a separate post-08c workstream.

## 08d and multi-domain boundaries

After 08c, Reviewer presents all three pairing outcomes to the user. If MiniLM
is eligible on at least one input, Reviewer may recommend a user-approved 08d
run over remaining pre-rerank inputs; the three 08c results are reused without
rerun. If none is eligible, Reviewer recommends removing reranking from 08d.
The user makes the decision in either case.

After the Foods 08c lifecycle closes, the next workstream expands the complete
answer-facing corpus under `knowledge-base-hue/`, rather than running only a
festivals pilot. It must curate and review Markdown for Foods, Festivals,
Heritage, Tourism, Performing Arts and every other approved answer-facing domain
such as Services, Statistics and Tickets. Raw `_source-dumps` and governance
files under `meta` are source/support material, not automatically retrievable
content.

After corpus coverage is complete, the project must update domain-aware
chunking/metadata, create fresh embeddings and an isolated full-corpus index,
then build a new combined Golden Dataset with explicit domain quotas and
evidence across all included domains. The exact total is set by the later
dataset design; it must be large and balanced enough for both overall and
per-domain reporting instead of treating Foods-only results as globally
representative. Evaluation then restarts at the Phase 7 baseline and reruns the
affected Phase 8 comparisons on the combined corpus/Golden contract.

Existing Foods 07/08 evidence remains valid only as historical Foods evidence.
Corpus edits, embedding/index creation, active Qdrant mutation, the combined
Golden Dataset and production transition all require a separate post-08c design,
plan and user approval.

## Expected implementation file scope

The later implementation plan may create or modify only:

- `backend/evaluation/reranker_benchmark.py`;
- `backend/tests/test_reranker_benchmark.py`;
- `notebooks/08c_reranker_benchmark.ipynb`;
- the two approved 08c result artifacts after an authorized run;
- the 08c implementation report and exact lifecycle handoff.

Any runtime reranker change, new model, dependency change, retrieval rerun,
Qdrant write, corpus/Golden edit, paid call or multi-domain work requires a new
user-approved scope.

## Acceptance and approval boundary

Implementation is technically ready only when:

1. all 135 fixed input records validate against canonical data;
2. production `CrossEncoderReranker` remains unchanged;
3. the exact three inputs and two states are evaluated;
4. smoke succeeds before the full run;
5. each input completes 45 cases x 3 repetitions or preserves its true
   failed/partial status;
6. artifacts reconcile to exactly 60 summary rows and 135 case records;
7. metrics and flags match per-case evidence;
8. MiniLM p95 for ten pairs is at most three seconds for an eligible pairing;
9. the temporary notebook Run All uses the real model and the repository copy
   remains clean;
10. Golden V3, corpus, 08a/08b artifacts, Qdrant and production configuration
    are unchanged.

The written specification, implementation plan and Review Contract are
approved. Exact implementation and real local MiniLM execution are authorized
through the current Implementer handoff. Git authorization remains separate.

## Approved complexity-reset amendment — 2026-08-30 (+07)

Sau verdict `changes_requested` thứ tư, user đã xác nhận complexity reset cho
numeric reconciliation boundary. Amendment này không đổi benchmark design,
producer, schema, notebook, artifacts hoặc quality decision.

Reconciler phải normalize mọi persisted numeric value bắt buộc qua một finite
numeric boundary trước compare/recompute. Parse failure, `NaN`, `+Inf` và `-Inf`
đều fail closed. Field phải blank theo schema được kiểm blank riêng và không bị
coerce thành zero. Tests dùng helper/parameterization để giữ prior tamper
coverage mà không tiếp tục thêm duplicated one-off validation branches.

Vì artifact-producing data flow không đổi, approved reset reuse real MiniLM Run
All và durable artifacts đã pass trong cùng implementation series. Reset không
authorize model load/run mới, artifact rewrite, dependency/network action,
Qdrant access/mutation, Git operation hoặc production change.

## Approval closure — 2026-08-30 (+07)

User đã xác nhận Notebook 08c sau independent final review. Work package hiện
`approved`; cả ba MiniLM pairings đều `eligible=False`, không có reranker
finalist và production giữ nguyên. Foods evidence này không đại diện cho full
Hue corpus. Next boundary là thiết kế riêng cho curated multi-domain data,
domain-aware chunking/metadata, isolated index và Combined Golden Dataset; chưa
authorize implementation hoặc mutation của workstream đó.
