# Phase 4–5 Qdrant and Retrieval Simplicity Design

Date: `2026-08-25 +07`

Status: `approved by user`

## Purpose

Simplify the tightly coupled Phase 4 Qdrant ingestion and Phase 5 retrieval
runtime without removing the three retrieval profiles that Phase 8 must compare.
The result must use real Hue Foods data, real Qdrant, real E5 and real MiniLM,
while remaining direct enough for a learner to trace from canonical chunks to a
retrieved context.

This design was produced after direct review of:

```text
/home/minhhieu/llm_rag/backend/vectorstore
/home/minhhieu/llm_rag/backend/scoring
/home/minhhieu/llm_rag/backend/retrieval
/home/minhhieu/llm_rag/backend/reranking
```

and the Hue reference note:

```text
guides/llm_rag_reference_for_hue_rag.md
```

Hue keeps the reference project's understandable vertical flow, but does not
copy its module globals, implicit schema trust, random IDs, unused stored sparse
vectors, BM25/SparseEmbedder coupling, thin reranker wrappers, input mutation or
silent fallback.

## Approved principles

- Code must be easy to read, explain and run.
- Do not retain abstractions for hypothetical implementations.
- Do not build collection orchestration, run registries or audit machinery.
- Use canonical data and actual services/models.
- Do not use mocks, fakes, replayed output or fabricated results as system
  evidence.
- Keep or create a test only when it protects a real user-needed behavior or an
  important real failure.
- Do not set a target test count.
- Do not split tests into many files for rare technical cases.
- Every retained test must have a plain answer to: “What user-needed behavior
  does this protect?”
- Active, rollback and destructive collection actions require explicit user
  approval at the exact transition gate.
- Commit and push require a separate user request.

## Reference findings

The actual `llm_rag` ingestion path stores both named dense and sparse vectors,
but its query path only searches the named dense vector and then applies Python
BM25 to dense candidates. Stored sparse vectors therefore add schema and
ingestion work without affecting its current retrieval results.

The reference reranker uses:

```text
BaseReranker
-> CrossEncoderReranker
-> thin CrossEncoderModel wrapper
```

for one real implementation. It eagerly loads the model, mutates input
documents, trusts `zip()` score alignment and may silently continue without a
reranker after startup failure. Hue keeps direct batch scoring, but not those
behaviors.

The reference BM25 depends on `SparseEmbedder` for corpus statistics. Hue's BM25
already owns its own DF/IDF fit and only imports the shared tokenizer, so the
remaining embedding-to-lexical dependency can be removed directly.

## Current state before implementation

The active collection is:

```text
hue_foods_e5_small_384
```

Observed state:

- 572 canonical points;
- named dense vector `dense`, 384-dimensional cosine;
- named sparse vector `sparse` on every point;
- the active collection remains read-only during design and candidate work;
- query runtime never queries `sparse`;
- hybrid profiles use Python BM25 over dense candidates;
- payload repeats both `embedding_model` and `embedding_dimension`;
- ingestion owns manual retry, cached Qdrant client lookup and a reset config
  flag;
- startup owns corpus/config fingerprints and a `verify_snapshot()` function
  without a production caller;
- reranking is split across an abstract base, scorer adapter and model wrapper;
- many tests protect cache, retry, fingerprint, sparse and manually invalid
  composition mechanisms.

## Capability boundary

The three canonical profiles remain exactly:

```yaml
profiles:
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
```

Their runtime flow remains:

```text
dense_only:
  Qdrant dense top 10

hybrid_no_rerank:
  Qdrant dense top 30
  -> Python BM25 on the same candidates
  -> independent min-max normalization
  -> 0.6 dense + 0.4 BM25
  -> top 10

hybrid_rerank:
  same hybrid top 10
  -> real MiniLM CrossEncoder
  -> top 5
```

This design does not claim that hybrid or reranking is better. Phase 8 selects a
winner from real observed metrics.

## Target Qdrant architecture

The production target is one named dense vector:

```text
name: dense
size: 384
distance: cosine
```

Remove the custom TF-IDF sparse vector from:

- expected collection schema;
- point construction;
- ingestion;
- Qdrant validation;
- notebooks and tests that describe the active baseline.

Removing stored sparse vectors does not remove Python BM25 or CrossEncoder.

### Point contract

Each point keeps a deterministic UUID5 derived from the canonical `chunk_id`:

```python
uuid.uuid5(uuid.NAMESPACE_URL, f"hue-rag:{chunk_id}")
```

The target point shape is:

```python
{
    "id": "deterministic UUID5",
    "vector": {"dense": [0.01, 0.02]},
    "payload": {
        "text": "...",
        "chunk_id": "...",
        "source": "foods/...",
        "title": "...",
        "section": "...",
        "category": "foods",
        "subcategory": "...",
        "chunk_type": "...",
        "embedding_model": "intfloat/multilingual-e5-small",
    },
}
```

Keep `embedding_model` because two embedding models can share dimension 384 but
produce incompatible vector spaces. Remove `embedding_dimension` from payload
because Qdrant schema and settings are already its authoritative source.

### Vectorstore modules

Use direct functional modules:

```text
backend/vectorstore/qdrant.py
backend/vectorstore/points.py
backend/vectorstore/upsert.py
backend/vectorstore/reset.py
backend/ingestion/pipeline.py
```

Responsibilities:

- `qdrant.py`: create one client, check availability, create/validate the exact
  dense-only schema;
- `points.py`: pure chunk/vector validation, UUID5 and dense PointStruct
  construction;
- `upsert.py`: existing-point scan, bounded batch writes and exact count gate;
- `reset.py`: one explicit-target destructive command;
- `pipeline.py`: Phase 2–4 orchestration with no deletion path.

Delete `vectorstore/hybrid_index.py`; do not leave a compatibility wrapper.

### Client and upsert lifecycle

Each composition root creates one Qdrant client and passes it to consumers. Do
not use `lru_cache` or a module singleton.

Keep:

```text
timeout: 30 seconds
upsert batch: 64
wait: true
```

Remove manual retry and `upsert_max_retries`. An upsert failure is reported
directly. A full ingestion rerun is safe because IDs are deterministic and
Qdrant upsert is idempotent.

Before a rerun writes into a candidate that already contains points, scan the
existing payloads and require:

- every existing ID belongs to the 572 expected UUID5 IDs;
- payload `chunk_id` matches the expected point;
- payload `embedding_model` matches the configured E5 model.

Do not check payload dimension. After upsert, require exact point count 572.

### Reset command

Remove `vector_database.reset_collection`. Ingestion cannot trigger deletion.

The separate reset CLI requires:

```text
--collection <exact-name>
--confirm "DELETE <exact-name>"
```

It must:

1. require the exact target and matching confirmation;
2. verify the target exists;
3. read and display the current point count;
4. delete exactly that target;
5. verify that target is absent;
6. stop without starting ingestion or another mutation after failure.

It must not require the target to equal active config and must not validate the
expected schema or every payload before deletion. Schema mismatch may be the
reason a failed candidate or retired collection needs cleanup.

Exact arguments do not replace explicit user approval before deleting an active
or rollback collection. Real automated reset checks may delete only guarded test
collections.

## Blue-green migration

Keep the current active collection read-only:

```text
hue_foods_e5_small_384
```

Create one fixed dense-only candidate:

```text
hue_foods_e5_small_384_dense
```

Ephemeral tests use names beginning with:

```text
hue_rag_live_test_
```

Do not use timestamps, run IDs or a collection registry.

The lifecycle is:

```text
fresh active retrieval baseline
-> implement and verify on guarded collections
-> create/ingest fixed dense-only candidate
-> run candidate retrieval comparison
-> independent reviewer verification
-> stop for user cutover approval
-> update canonical collection_name only after approval
-> retain old collection as rollback
-> delete old collection only after another explicit approval
```

Because dense model, dimension, document instructions and chunks are unchanged,
Phase 4 success means equivalent retrieval quality with simpler code/schema and
no meaningful latency or reliability regression. Removing sparse storage alone
is not a quality claim.

### Candidate targeting

Before cutover, production settings continue to point to the old active
collection. Candidate commands use an optional exact `collection_name` only at
composition roots:

- `run_ingestion(..., collection_name=...)`;
- retrieval evaluation service/batch construction.

The composition root deep-copies settings and changes only
`vector_database.collection_name` in memory. Do not create candidate YAML, mutate
`settings.yaml`, use global environment overrides or build a multi-collection
runtime.

## Target Phase 5 architecture

Keep three concrete behavior components:

```text
DenseRetriever
HybridRetriever
RetrievalService
```

Remove `RetrievalStack`. Startup creates only the components required by the
active profile and returns `RetrievalService` directly. The service owns the
small immutable runtime status and routes the profile.

Tests must not construct invalid/missing optional stacks that production startup
cannot create.

### BM25 ownership

`backend/scoring/bm25.py` owns:

- Unicode lowercase/punctuation tokenization;
- corpus document frequency and IDF;
- BM25 scoring with `k1=1.5`, `b=0.75`;
- min-max normalization;
- dense/BM25 weight validation.

Delete `backend/embedding/sparse_embedder.py` and its tests after a full consumer
audit. Do not add `rank_bm25`; the existing formula is small, readable and
already exercised by real retrieval.

### Concrete reranker

Use one file:

```text
backend/reranking/cross_encoder.py
```

`CrossEncoderReranker` owns its model instance and directly implements:

- model load;
- one real warm-up;
- batch prediction;
- exact score-count validation;
- numeric/finite score validation;
- deterministic ordering by score descending then `chunk_id`;
- fresh output documents with `reranker_model` and `rerank_score` metadata.

It must not mutate input documents.

Delete:

```text
backend/reranking/base.py
backend/reranking/reranker.py
backend/reranking/models/cross_encoder.py
```

Do not keep scorer injection or compatibility wrappers. Phase 8 creates a shared
interface only if a second real reranker is approved and implemented alongside
the local model.

Only `hybrid_rerank` loads MiniLM. Normal online model download is allowed in the
approved run; use the library's ordinary download cache but no application
`lru_cache`, `local_files_only` gate, preload script or missing-cache tests.
Download/load/predict failure is explicit and never changes the active profile.

### Startup and runtime status

Startup must:

1. create one Qdrant client;
2. validate collection existence, exact dense schema and count 572;
3. create and warm E5;
4. build only `DenseRetriever` for `dense_only`;
5. for hybrid profiles, scroll all 572 safe payloads and validate unique IDs,
   non-empty text and `embedding_model`;
6. fit BM25 once;
7. load/warm MiniLM only for `hybrid_rerank`;
8. return `RetrievalService` with small runtime status.

Payload scrolling uses a fixed internal batch size 128. Remove
`vector_database.scroll_batch_size`, function overrides and tests for that knob.

Runtime status keeps only fields with real API/health/debug consumers:

```text
collection_name
point_count
embedding_model
embedding_dimension
active_profile
bm25_ready
reranker_ready
```

Delete corpus/config fingerprints and `verify_snapshot()`. Collection or config
changes require process restart; do not build hot reload or stale-state audit.

### ContextBuilder

Keep `ContextBuilder` and its JSON evidence contract because API, evaluation and
prompt generation consume it directly.

Preserve:

- whole chunks only;
- maximum 5 documents;
- maximum 3,000 serialized characters;
- source mapping;
- JSON structural separation between metadata and document text;
- input order and non-mutation.

Do not rewrite it as plaintext or a standalone function merely to reduce class
count.

## Configuration changes

The target vector database section is:

```yaml
vector_database:
  url: http://localhost:6333
  collection_name: hue_foods_e5_small_384  # changes only at approved cutover
  vector_size: 384
  distance: cosine
  timeout: 30
  upsert_batch_size: 64
```

Remove:

```text
vector_database.reset_collection
vector_database.upsert_max_retries
vector_database.scroll_batch_size
```

Retrieval weights, depths, context limits and the three profile mappings remain
unchanged.

## Tests

Tests are behavior evidence, not a coverage/count exercise.

Target ownership is:

```text
backend/tests/test_ingestion_pipeline.py
backend/tests/test_bm25.py
backend/tests/test_retrieval_service.py
backend/tests/test_context_builder.py
```

`test_ingestion_pipeline.py` should cover only the meaningful dense-only
schema/point/ingestion behaviors:

- deterministic dense point and payload contract;
- real guarded dense-only schema;
- real canonical 572-point ingestion;
- idempotent rerun;
- one foreign/model-mismatch rejection before mutation;
- exact-target guarded reset.

`test_bm25.py` should cover:

- Vietnamese tokenization;
- a known-corpus ranking;
- normalization and valid/invalid fusion configuration needed by runtime.

`test_retrieval_service.py` should cover:

- real startup and search for all three profiles;
- stages used by each profile;
- real E5/Qdrant/MiniLM behavior;
- deterministic output and important explicit dependency failure.

`test_context_builder.py` should cover:

- whole-chunk budget and document limit;
- JSON structural safety and source mapping;
- empty input and non-mutation.

Delete or merge meaningful behavior from:

```text
backend/tests/test_hybrid_index.py
backend/tests/test_sparse_embedder.py
backend/tests/test_qdrant_schema.py
backend/tests/test_reranker.py
backend/tests/test_startup.py
```

Remove overlapping generator tests that merely retest ContextBuilder. Before
deleting any old test, identify the user-needed behavior it protects; move that
behavior if it remains required. Do not delete mechanically from a filename
list.

Pure deterministic tests are allowed. System-running evidence must use real
Qdrant and real models, never mocks or fakes.

## Notebooks

### Notebook 03

Keep the E5 dense embedding lesson and real 572 × 384 run. Remove sparse TF-IDF
content/imports; lexical scoring now belongs in Phase 5.

### Notebook 04

Inspect `hue_foods_e5_small_384_dense` read-only after ingestion. Show exact
dense-only schema, count 572 and safe payload projection. Do not include create,
upsert, reset or delete cells.

### Notebook 05

Explain BM25 and the exact three profiles, then run real candidate queries with
E5/Qdrant/MiniLM. Do not claim a winner.

Repository notebook files keep empty outputs and null execution counts. Run All
evidence comes from temporary executed copies. No fake fallback.

## Real verification

### Fresh pre-change baseline

Before runtime edits, run all 104 canonical retrieval questions on the current
active collection for:

```text
dense_only
hybrid_no_rerank
hybrid_rerank
```

Record metrics, latency and failures in a simple report. Do not reuse historical
output as fresh evidence.

### Implementation verification

Use guarded real Qdrant collections and actual E5/MiniLM to verify the smallest
affected behaviors. Run the final backend suite once because ingestion, startup
and retrieval are shared contracts; do not repeatedly use the full suite as a
checkpoint.

### Candidate verification

Create and ingest:

```text
hue_foods_e5_small_384_dense
```

Verify:

- exact dense-only schema;
- exact 572 canonical points;
- payload model identity and no payload dimension;
- idempotent rerun;
- all three real profiles;
- Notebook 04 and Notebook 05 temporary Run All.

Then run the same 104 retrieval questions for all three profiles on the
candidate. Compare metrics, latency, failures and relevant per-query ID/score
differences against the fresh active baseline.

Exact floating-point equality is not required if real model/library numerical
noise is observed, but every ranking or metric delta must be explained before a
cutover recommendation.

Do not run paid generation/judge for this comparison because prompt, context
contract and generator are not changed. If retrieval differences change selected
context or source mapping materially, stop and design the smallest downstream
answer-impact check.

## Cutover and completion gates

Implementation stops after candidate verification and the implementation report.
The Reviewer independently checks code, tests, notebooks, candidate state and
the 104 × 3 comparison.

The candidate does not become active automatically. Config cutover requires a
new explicit user approval after technical review.

After cutover:

- keep `hue_foods_e5_small_384` read-only as rollback;
- report the exact active collection in runtime status and benchmark summary;
- delete the rollback collection only after another explicit user approval.

Implementation authorization does not authorize active/rollback deletion,
cutover, commit or push.

## Expected simplification

The design removes unused sparse storage and the machinery built around it,
while preserving all three benchmarkable profiles. It also removes cache/retry,
fingerprint, optional-stack and single-implementation abstraction layers.

The intended result is one traceable path:

```text
canonical chunks
-> E5 dense points
-> dense-only Qdrant candidate
-> DenseRetriever
-> optional Python BM25 fusion
-> optional concrete MiniLM reranking
-> bounded JSON context
```

No part of this design predicts a Phase 8 winner. Every production transition
must follow real evidence and the explicit user gates above.
