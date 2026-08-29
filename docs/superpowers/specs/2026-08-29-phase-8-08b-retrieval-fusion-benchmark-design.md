# Phase 8 — Notebook 08b Retrieval and Fusion Benchmark Design

Date: 2026-08-29 (+07)

Status: `approved_for_implementation_handoff`. The complete design, exact
written specification and implementation plan were approved by the user on
2026-08-29 (+07). Implementation and the exact isolated evaluation run begin
only when the user delivers the prepared Implementer prompt. Active mutation,
paid calls, production configuration changes and cutover remain unauthorized;
Git authority is scoped separately by the current handoff.

## Purpose

Notebook 08b teaches and measures lexical, custom sparse and no-rerank fusion
paths on the Hue food corpus. It uses the canonical 572 chunks, all 45 Golden
Dataset V3 cases and the three approved dense collections from Notebook 08a.
It produces at most one dense+BM25 and one dense+TF-IDF 08b finalist for the
later Notebook 08d compatibility benchmark. It never selects or activates a
production pipeline.

The notebook is intentionally allowed to be long. Its Markdown is Vietnamese,
identifiers are English, each code cell performs one visible action, and all
retrieval, scoring, evaluation, persistence and safety logic lives in backend
code rather than being duplicated in notebook cells.

## Relationship to current Hue RAG and `llm_rag`

The current Hue runtime and the reference `llm_rag` flow both start with dense
retrieval and apply BM25 only to those dense candidates. BM25 therefore cannot
recover a relevant document omitted by dense retrieval.

The current Hue runtime is the cleaner reference row:

```text
dense top 30
-> BM25 scores only those 30 candidates
-> independent min-max normalization
-> 0.6 dense + 0.4 BM25
-> top 10
-> no-rerank top 5 for this notebook
```

`llm_rag` also uses dense-first BM25 candidate rescoring, but combines raw dense
and BM25 scores. That raw-score behavior is documented as a limitation and is
not added as another executable 08b setting because the two score scales are
not comparable.

08b adds two independent full-corpus sparse generators:

```text
BM25 over all 572 chunks -> top 30
TF-IDF sparse Qdrant query over all 572 chunks -> top 30
```

True hybrid fusion then combines one independent sparse top-30 list with one
dense top-30 list. Reranking belongs to 08c, the complete compatibility matrix
belongs to 08d, and generation belongs to 08e.

## Approved scope

08b includes exactly:

- five controlled BM25 parameter settings using the current Unicode tokenizer;
- one controlled comparison of Unicode `\w+` and Underthesea tokenization;
- one independent full-corpus BM25 generator;
- one custom normalized TF-IDF full-corpus sparse generator;
- three dense-only controls from the approved 08a collections;
- three current-style dense-to-BM25 rescoring settings;
- six dense+BM25 true-hybrid settings;
- six dense+TF-IDF true-hybrid settings;
- RRF and independently normalized weighted fusion;
- candidate, fusion and final-depth metrics, category evidence, latency,
  resource observations, paired-bootstrap intervals and auditable artifacts;
- at most two 08b finalists for 08d.

The executable local dense configurations remain exactly:

1. `e5-small-384` — `intfloat/multilingual-e5-small`, 384D;
2. `huydang-dek21-embedding-768` —
   `CODE4LIFEOFFICIAL/huydang-dek21-embedding`, 768D;
3. `e5-base-768` — `intfloat/multilingual-e5-base`, 768D.

The implementation consumes the exact approved model revisions, encoding
contracts, manifests and isolated collections established by 08a. It does not
download, index or execute another dense model.

## Explicit non-scope

08b does not implement, run, review or authorize:

- rerankers, answer generation or LLM judging;
- paid APIs;
- BGE learned sparse, ColBERT or another learned sparse representation;
- PyVi, VnCoreNLP or a tokenizer grid;
- BM25 parameter grid search beyond the exact five settings;
- fusion-weight tuning or RRF-constant tuning;
- dense-to-TF-IDF candidate rescoring;
- Golden Dataset changes based on benchmark results;
- active/production collection writes, runtime settings changes or cutover;
- automatic deletion or rebuild of a mismatched Qdrant collection;
- automatic retries, fallback models, device changes or changed formulas;
- production winner selection.

## Architecture and safety boundary

```text
canonical knowledge base
        -> production chunker
        -> 572 chunks + corpus fingerprint
        -> exact validation against all three 08a artifacts/collections
        -> BM25 parameter calibration
        -> tokenizer comparison
        -> selected lexical contract
        -> TF-IDF experimental sparse collection
        -> 20-setting retrieval benchmark
        -> quality/category/latency gates
        -> zero, one or two 08b finalists for 08d
```

`backend/evaluation/sparse_benchmark.py` owns the experiment logic:

- canonical input and 08a provenance validation;
- evaluation-scoped full-corpus BM25;
- tokenizer adapters and calibration;
- deterministic TF-IDF vocabulary and vectors;
- experimental sparse collection validation/build/query;
- dense, sparse, rescoring and fusion orchestration;
- metrics, category gates, bootstrap, latency and resource observations;
- checkpoint loading, reconciliation and durable artifact persistence.

`notebooks/08b_retrieval_fusion_benchmark.ipynb` only imports the backend,
supplies immutable approved configuration, invokes sequential stages and
displays human-readable evidence.

The evaluation-scoped BM25 must not change production `scoring/bm25.py` or its
runtime behavior. A focused parity test proves that the Unicode baseline uses
the same BM25 formula and ranking semantics as the current runtime.

Before any write, capture a read-only active-production snapshot containing the
collection name, vector schema and exact point count. Capture it again at the
end. A difference blocks successful completion.

## Canonical inputs and 08a validation

The source of truth is production `chunk_foods_markdown()` output, not a Qdrant
payload copy. Preflight must:

1. load and validate all 45 Golden V3 cases;
2. regenerate exactly 572 canonical chunks;
3. derive relevant chunks at evaluation time from exact canonical
   `source + section` evidence, never from ground-truth stored chunk IDs;
4. compute corpus, chunker-contract and Golden V3 fingerprints;
5. load the three approved 08a manifests/settings;
6. verify every 08a collection name, dimension, distance, model ID/revision,
   point count, exact `chunk_id` set and exact text hash;
7. stop before calibration when any identity or provenance check fails.

Dense results are queried again through the 08a collections so all 20 settings
use the same evaluator and measurement session. Document vectors are not
recomputed by default. A future rebuild is allowed only through a separately
visible opt-in recovery path and the exact approved 08a contract.

## BM25 full-corpus implementation

The BM25 generator pre-tokenizes all 572 documents once per tokenizer and keeps
document term counts in process memory. Each query is scored against all 572
documents, then sorted by descending score and ascending `chunk_id` for exact
ties. It returns at most 30 results.

For non-empty canonical documents:

```text
N = number of documents
avgdl = mean document token count
idf(t) = log(((N - df(t) + 0.5) / (df(t) + 0.5)) + 1)
score(q, d) = sum over unique query terms of
  idf(t) * tf(t,d) * (k1 + 1)
  / (tf(t,d) + k1 * (1 - b + b * dl(d) / avgdl))
```

Invalid `k1 < 0`, `b < 0`, `b > 1`, empty corpora and non-finite scores fail
validation. An empty/OOV query returns an empty result with a structured reason
rather than raising during the benchmark.

The in-memory BM25 corpus cache is expected to consume only a few to a few tens
of MB at this corpus size. Build time and RSS change are measured separately
from warm query latency. The cache disappears when the process/kernel exits.

## BM25 parameter calibration

Parameter calibration uses only the current lowercase Unicode tokenizer and
exactly these five settings:

| Order | Setting key | `k1` | `b` |
|---:|---|---:|---:|
| 1 | `baseline` | 1.5 | 0.75 |
| 2 | `k1_low` | 0.9 | 0.75 |
| 3 | `k1_high` | 2.0 | 0.75 |
| 4 | `b_low` | 1.5 | 0.25 |
| 5 | `b_high` | 1.5 | 1.00 |

The selected pair must pass candidate-depth category guardrails against the
baseline. Rank candidates by macro Recall@30. Treat an absolute Recall@30
difference at or below 0.005 as a tie, then compare nDCG@5, MRR@5 and latency in
that order. If no candidate passes, retain `k1=1.5, b=0.75`. The baseline stays
visible in the calibration artifact and notebook regardless of selection.

This is calibration on Golden V3, not an independent unbiased quality estimate.
The report must state that limitation and must not describe the selected pair
as a production default.

## Tokenizer comparison

Hold the selected `k1/b` pair fixed and compare exactly:

- `unicode_word`: Unicode NFC, lowercase, Unicode `\w+`, retaining Vietnamese
  accents and numbers;
- `underthesea_word`: Unicode NFC and Underthesea
  `word_tokenize(text, format="text")`, preserving underscore-joined compound
  words as individual vocabulary tokens.

Neither path removes accents or uses a stopword list. Tokenization is identical
for corpus documents and queries.

Use the same Recall@30, category, nDCG@5, MRR@5 and latency selection order as
parameter calibration. When the Recall@30 difference is at most 0.005 and
the ordered nDCG@5, MRR@5 and latency tie-breakers do not strictly favor
Underthesea, retain Unicode because it has lower dependency and operational
complexity. Unicode remains the visible control in every case.

Underthesea belongs to a research/evaluation dependency group, not production
runtime dependencies. The dependency declaration uses a compatible major
range, the lock records the exact resolved version, and the manifest records
the version actually executed. There is no `%pip install` notebook cell.

## Calibration category guardrails

Calibration uses hit@30 because BM25 is being selected as a candidate generator.
For the actual Golden V3 category distribution:

- categories with at least six cases cannot lose hit@30 cases; when hit counts
  tie, candidate category nDCG@5 delta must be at least -0.02;
- categories with fewer than six cases cannot lose any exact case that the
  reference hit at depth 30.

The parameter reference is Unicode `k1=1.5, b=0.75`. The tokenizer reference is
Unicode at the selected parameter pair.

## Custom normalized TF-IDF contract

TF-IDF uses the selected tokenizer and a deterministic full unigram vocabulary:

- `min_df=1`;
- no `max_features`;
- no stopword list;
- lexical sorting before assigning integer token indices.

Weights are:

```text
tf(t,d) = 1 + log(count(t,d)) when count > 0, otherwise 0
idf(t) = log((N + 1) / (df(t) + 1)) + 1
weight(t,d) = tf(t,d) * idf(t)
```

Document and query vectors are L2-normalized. Qdrant sparse dot product is
therefore equivalent to cosine similarity for non-zero vectors. Sparse indices
are strictly increasing; values are finite and non-zero. OOV tokens are ignored.
A zero query vector returns an empty result with a structured reason.

This standard normalized formula intentionally does not copy `llm_rag` raw
term-count weighting. It is an experimental control, not a runtime migration.

## Experimental TF-IDF collection

08b uses one sparse-only Qdrant collection. Its deterministic name includes the
experiment version, selected tokenizer and the first 12 corpus-fingerprint
characters, for example:

```text
hue_rag_phase8_08b_tfidf_v1_<tokenizer>_<fingerprint12>
```

The collection has:

- one named sparse vector, `tfidf`;
- no copied dense vectors;
- exactly 572 deterministic points;
- deterministic UUID5 point IDs derived from canonical `chunk_id`;
- payload fields needed for canonical identity, evidence display and provenance;
- corpus, tokenizer, formula and vocabulary fingerprints.

Fusion across collections always joins on canonical `chunk_id`, never on the
Qdrant point ID.

Reuse requires exact collection name, vector name, point count, `chunk_id` set,
text hash, corpus fingerprint, tokenizer key, formula version and vocabulary
fingerprint. Empty/non-finite stored vectors fail validation.

The default is validate/reuse only. Creating the missing collection requires:

```text
ALLOW_EXPERIMENT_MUTATION=true
```

A mismatched existing collection always fails closed. The notebook never
automatically deletes, clears, overwrites or rebuilds it. The collection remains
available for reviewer inspection and later 08d planning.

## Exact 20-setting matrix

The calibration rows are separate evidence and do not count in this matrix.

| Group | Count | Exact behavior |
|---|---:|---|
| Dense-only | 3 | Query each approved 08a dense collection |
| BM25-only | 1 | Independent full-corpus BM25 top 30 |
| Dense -> BM25 rescore | 3 | Dense top 30; BM25 only those candidates; independent min-max `0.6/0.4` |
| Dense + BM25 true hybrid | 6 | Three dense models times RRF/weighted |
| TF-IDF-only | 1 | Independent Qdrant sparse top 30 |
| Dense + TF-IDF true hybrid | 6 | Three dense models times RRF/weighted |
| **Total** | **20** | No reranker |

There is no dense-to-TF-IDF rescoring row.

## Depth and relevance contract

- Dense, BM25 and TF-IDF generators each return at most 30.
- True-hybrid candidate union may contain at most 60 unique chunks.
- Fusion retains top 10.
- No-rerank final evaluation uses the top 5.
- Relevance is binary exact canonical `source + section`.
- Each declared source+section evidence pair receives credit at most once in a
  ranked list; duplicate chunks from the same relevant section receive no
  additional gain.

Every setting records whichever stages apply:

- dense Recall@30;
- sparse Recall@30;
- candidate-union recall;
- fusion Recall@10;
- final Recall@5, MRR@5 and nDCG@5;
- overall and nine-category aggregations;
- raw rankings and scores needed to reproduce the final order.

Non-applicable stage metrics are blank, not fabricated as zeros.

## Fusion contracts

### Primary RRF

RRF is implemented deterministically on the client:

```text
rrf_score(d) = sum over available generator lists of 1 / (60 + rank(d))
```

- rank starts at one;
- fusion uses the union of the two top-30 lists;
- absence from one list contributes no score for that list;
- `k=60` is fixed and not tuned;
- exact ties resolve by ascending `chunk_id`.

### Weighted control

Dense and sparse scores are min-max normalized independently within their own
top-30 lists. A chunk absent from one list receives normalized score zero for
that signal. Fuse the union with:

```text
0.6 * normalized_dense + 0.4 * normalized_sparse
```

A constant generator signal normalizes to zero. Non-finite input fails. Exact
ties resolve by ascending `chunk_id`. There is no weight grid.

Raw scores, normalized scores, per-generator ranks and fused scores are retained
in per-case evidence.

## Latency and resource measurement

Execution is sequential. Do not load all three dense query models at once.
Each configuration has a discarded warm-up, followed by all 45 Golden V3
queries repeated three times. Take the median latency for each query, then
report p50 and p95 across the 45 per-query medians.

End-to-end warm query latency includes the applicable query embedding or
tokenization, generator query and fusion. Also retain separable component
latencies. Report BM25 cache build, TF-IDF vocabulary/vector build and Qdrant
index time separately; never mix them into warm query latency.

Memory observation remains lightweight: RSS before/after building an in-memory
index, observed peak RSS at explicit stage boundaries, and collection size when
available. Do not add a profiler or background sampling timeline.

An 08b finalist must satisfy p95 hybrid latency at or below two times its exact
same-model dense-only p95. Every path must also finish without timeout/error.

## Incremental execution, checkpointing and resource release

The implementer is explicitly allowed to divide implementation-time evaluation
and the real notebook run into any practical number of sequential execution
batches. Examples include five, ten or another number of steps chosen from the
observed runtime and available RAM, VRAM and disk. There is no requirement to
complete the whole benchmark in one process, one kernel session or one command.

Scientific behavior must not depend on that operational partition:

- prerequisite order remains preflight -> calibration -> tokenizer selection
  -> TF-IDF validation/build -> main matrix -> reconciliation;
- an execution batch contains explicit setting keys in canonical order;
- each completed setting is atomically persisted before moving to the next;
- a setting is `completed` only after its required warm-up and all three
  45-case repetitions finish under the exact manifest;
- interrupted or incomplete work is recorded as `partial` or `failed`, never
  silently treated as completed;
- resume is allowed only when manifest, schemas, fingerprints, selected
  calibration result and dependency versions match exactly;
- resuming skips exact completed settings and continues remaining settings;
- an exact setting rerun replaces its own idempotent keys instead of producing
  duplicate rows;
- the final gates and shortlist run only after reconciliation proves the whole
  mandatory matrix is complete.

Between settings or batches, the implementer may close models and clients,
delete large in-process objects, run Python garbage collection, clear the CUDA
cache when CUDA is active, restart the kernel/process and remove task-created
ephemeral files when their exact paths are known. This permission does not
authorize deletion of durable result artifacts, the TF-IDF review collection,
08a collections, model caches, repository data or production resources. Any
such material cleanup requires separate exact authorization.

Batch size and grouping are operational metadata recorded in the manifest or
execution report, not an experimental variable and not a reason to change
formulas, depths, repetitions, ordering, models or gates.

## Finalist gates and selection

Each true-hybrid setting compares with the dense-only control using the same
embedding model. It is eligible only when:

1. all 45 cases and all three repetitions complete without error;
2. fusion Recall@10 is at least the dense control's Recall@10;
3. final Recall@5 is no more than 0.005 below the dense control;
4. every final-depth category guardrail passes;
5. hybrid p95 latency is at most twice the dense control p95.

Final-depth category guardrails are:

- for categories with at least six cases, candidate hit@5 count cannot be lower;
  if hit counts tie, category nDCG@5 delta must be at least -0.02;
- for categories with fewer than six cases, the candidate cannot lose any exact
  case hit by the dense control at depth five.

Eligible settings within each sparse family are ordered by Recall@5, nDCG@5,
MRR@5 and latency. RRF is the primary analysis method, but a weighted setting
may be selected when its observed evidence is better under this rule.

Use 10,000 paired bootstrap resamples, seed 42 and 95% percentile intervals for
delta Recall@5, MRR@5 and nDCG@5. These intervals express uncertainty and are
not an additional hard gate for the 08b-to-08d shortlist.

Select at most:

- one dense+BM25 08b finalist;
- one dense+TF-IDF 08b finalist.

Do not fill a quota. If no setting in a family passes, record `no finalist`.
These are research candidates for 08d, not global Phase 8 winners and not
production cutover approval. This exact 08b shortlist rule supersedes the
master document's general clear-gain rule only for admission from 08b into 08d;
later full-pipeline and production decisions remain separate approval gates.

## Durable artifacts

This exact 08b design supersedes the earlier master preference for one retrieval
CSV because raw per-generator rankings and cross-collection fusion require
auditable case-level evidence.

08b writes exactly four cumulative artifacts under `evaluation/results/`:

```text
phase8_sparse_manifest.json
phase8_sparse_calibration.csv
phase8_sparse_results.csv
phase8_sparse_cases.jsonl
```

### Manifest

The manifest records experiment/schema version, Git commit and dirty state,
corpus/chunker/Golden fingerprints, three 08a identities, dependency versions,
selected BM25/tokenizer contract, TF-IDF formula/vocabulary/collection identity,
fusion constants, depths, metric contract, bootstrap seed, operational batch
grouping and safe timestamps.

### Calibration CSV

It contains the five parameter settings and two tokenizer rows with overall and
category metrics, deltas, gates, latency, status, sanitized error and exact
selection rationale.

### Main results CSV

It is long format: 20 settings times `category=overall` plus all nine categories,
for exactly 200 reconciled rows. It contains readable setting/component/fusion
identity, depths, metrics, deltas, category/finalist gates, latency, status,
sanitized error and finalist result. Run/resource fields appear only on overall
rows where appropriate.

### Per-case JSONL

It contains exactly 20 settings times 45 cases, for 900 reconciled records.
Each record contains case/category identity, derived relevant evidence/chunks,
applicable dense/sparse top-30 ranks and raw scores, union identity, fusion top
10, final top 5, normalized/fused scores, per-case metrics, latency and a
structured sanitized error.

All schemas are exact and ordered where applicable. Writes are atomic. Upsert
keys include experiment version plus setting/category or setting/case identity.
Existing artifacts with mismatched schema or provenance fail closed. No secret,
credential, raw provider payload or sensitive stack trace is persisted.

A partial run may contain fewer rows with explicit partial/failed status, but
cannot be reconciled as complete and cannot produce finalists.

## Notebook structure

The canonical notebook contains approximately 35 short alternating Markdown
and code cells.

### 1. Purpose, reference and scope

- Explain dense-only, dense-to-BM25 and true-hybrid differences.
- Explain the relevant `llm_rag` limitation.
- State no reranker, generation, paid call or cutover.

### 2. Environment and safety

- Import backend functions without building indexes.
- Show safe dependency, CPU/RAM/Qdrant information.
- Display immutable experiment configuration and mutation flag.
- Capture the active production snapshot.

### 3. Canonical inputs and 08a prerequisites

- Load 45 Golden V3 cases and 572 chunks.
- Show category counts and fingerprints.
- Validate all three 08a manifests/collections.
- Display the three dense controls.

### 4. Part A — BM25 parameters and tokenizer

- Build the Unicode corpus cache.
- Run/display five parameter settings sequentially.
- Apply/display parameter selection.
- Build the Underthesea corpus cache.
- Run/display the exact two-tokenizer comparison.
- Apply/display tokenizer selection and lock the lexical contract.

### 5. Part B — TF-IDF and fusion

- Build/display vocabulary, TF-IDF and resource statistics.
- Validate or explicitly create the isolated sparse collection.
- Confirm 572 points and exact provenance.
- Display the exact 20-setting catalog.
- Execute pending settings sequentially or in approved operational batches.
- Display checkpoint/resume status after each batch.

### 6. Evidence and decision

- Show overall quality and stage-recall tables.
- Show all-category deltas and guardrails.
- Show latency/resource tables.
- Provide per-case regression/disagreement drill-down.
- Show paired-bootstrap intervals and finalist gates.
- Reconcile all four artifacts.
- Show zero, one or two 08b finalists and handoff to 08d.
- Re-read the production snapshot and state unchanged postconditions.

Three data-driven visualizations are allowed: stage recall, quality-versus-
latency, and category delta heatmap. Each follows the exact source table and is
not decorative.

The repository notebook has null execution counts and empty outputs. Reviewer
execution writes an executed copy outside the repository.

## Failure behavior

Allowed setting statuses are `completed`, `partial` and `failed`. Persist
`ExceptionType: sanitized message`; never persist secrets or sensitive traces.

After a setting failure, save its state, release resources and continue only
with settings independent of the failed prerequisite. Calibration failure,
tokenizer-selection failure, canonical/08a mismatch or TF-IDF provenance
failure blocks dependent work. There is no silent retry, fallback, changed
batch size inside a setting, changed model, changed tokenizer or changed score
formula.

Evidence of ranking instability across the three repetitions is reported
exactly rather than averaged away. A setting below 3/3 is ineligible.

## Verification contract

Automated unit tests cover reusable deterministic behavior:

1. Unicode baseline BM25 parity with current runtime;
2. known-corpus rankings for all five `k1/b` settings;
3. Unicode NFC and Underthesea compound-token behavior;
4. parameter/tokenizer selection and candidate-depth category guards;
5. hand-calculated TF-IDF weights, L2 norm and stable vocabulary indices;
6. empty/OOV/non-finite sparse behavior;
7. RRF `k=60`, union, missing signals and deterministic ties;
8. independent min-max weighted fusion and constant signals;
9. source+section relevance and all stage/final metrics;
10. final category gates, paired bootstrap and family finalist selection;
11. exact artifact schemas, atomic/idempotent checkpoint writes and resume;
12. provenance mismatch and mutation-flag failure;
13. production snapshot isolation.

A focused integration test uses a uniquely named isolated Qdrant test collection
and a small corpus with known sparse and fusion rankings. It may clean up only
that exact test-created collection after verifying the name.

Real completion requires an executed temporary notebook using the canonical
corpus, Golden V3, all three real 08a collections and the real isolated TF-IDF
collection. Fake vectors, mocked Qdrant, replayed results, smoke-only data or
old notebook outputs are not completion evidence.

The full run may use any number of sequential batches under the incremental
execution contract. Final review must reconcile:

- five BM25 parameter settings;
- two tokenizer settings;
- all 20 main settings at 3/3 repetitions;
- 200 main summary rows;
- 900 per-case records;
- one valid 572-point TF-IDF collection;
- exact agreement between notebook displays and durable artifacts;
- unchanged production collection snapshot and runtime settings;
- clean source-notebook outputs/execution counts;
- focused/full relevant tests and `git diff --check`.

## Expected implementation file scope

The later implementation plan may create or modify only the exact files needed
for this approved design, expected to include:

- `pyproject.toml`;
- `uv.lock`;
- `backend/evaluation/sparse_benchmark.py`;
- `backend/tests/test_sparse_benchmark.py`;
- `notebooks/08b_retrieval_fusion_benchmark.ipynb`;
- the four approved `evaluation/results/phase8_sparse_*` artifacts after an
  authorized run;
- the 08b implementation report.

The implementation plan must enumerate exact paths and may narrow this list.
Any expansion into production BM25, retrieval startup/service, active settings,
Golden V3, 08a collections, reranking or generation requires renewed user
approval.

## Review and approval boundaries

After the user approves this exact specification, create a detailed
test-driven implementation plan. That plan must preserve the arbitrary
multi-batch execution permission, atomic per-setting checkpointing, exact
resume/reconciliation behavior and safe resource release described above.

The user approved the plan and requested a prepared Implementer handoff on
2026-08-29 (+07). Delivering that prompt starts exact plan execution. Commit and
push during implementation still require the handoff's separate Git authority.
