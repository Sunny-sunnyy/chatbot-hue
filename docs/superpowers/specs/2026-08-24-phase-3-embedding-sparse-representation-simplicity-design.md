# Phase 3 Embedding and Sparse Representation Simplicity Design

Date: `2026-08-24 +07`

Status: `approved by user`

## Purpose

Simplify Phase 3 around the one dense embedding model used by the current Hue
Foods RAG system: `intfloat/multilingual-e5-small` running locally on CPU. The
result must be readable to a learner, use the real model and corpus, and keep
the current Phase 4–7 runtime working without speculative provider machinery.

This design uses `/home/minhhieu/llm_rag/backend/embedding` as a learning and
readability reference. Hue RAG keeps the useful ideas—one loaded local model,
normalized dense vectors and understandable TF-IDF—but does not copy the
reference project's module-global API, unused outer batching, nondeterministic
vocabulary construction or tutorial-length inline comments.

## Current phase and observed behavior

The current dense implementation is split across:

```text
backend/embedding/base.py
backend/embedding/embedder.py
backend/embedding/batch_embed.py
backend/embedding/openrouter_embedder.py
```

It has an abstract provider interface, a custom exception, shared NumPy vector
processing, an outer batching helper and a remote adapter with no production
consumer or live provider evidence. The local SentenceTransformer already
receives `batch_size`, so ingestion currently batches the same workload twice.

The reference `llm_rag` implementation is shorter, but it does not pass
`batch_size` to `SentenceTransformer.encode()`. Its separate batch helper is
also bypassed by the real hybrid upsert path. Copying that structure would not
fix the actual batching boundary in Hue RAG.

The current sparse implementation is concise and has stronger behavior than
the reference:

- deterministic first-occurrence vocabulary indices instead of `set()` order;
- state reset on repeated `fit()`;
- explicit rejection of `encode()` before `fit()`;
- one compiled tokenization regex;
- reproducible vectors for the same ordered corpus.

It can still be made easier to learn through clearer types, names and concise
explanations. Detailed worked examples belong in Notebook 03 and the Phase 3
guide rather than as large tutorial blocks inside runtime code.

## Approved constraints

Phase 3 uses only:

```text
Model: intfloat/multilingual-e5-small
Execution: local CPU
Dimension: 384
Batch size: 64
Document instruction: passage:
Query instruction: query:
```

The active Qdrant collection remains strictly read-only. Existing live tests
may create, upsert and delete only isolated collections whose names start with
`hue_rag_live_test_`; their existing target guards and cleanup reporting must
remain in force. No test or implementation step may reset, reindex, upsert or
otherwise mutate `hue_foods_e5_small_384`.

Do not change the Phase 4 Qdrant schema, Phase 5 retrieval algorithms, BM25,
reranking, generation or evaluation behavior. `dense_only` remains the active
MVP profile until Phase 8 comparison evidence supports another choice.

OpenRouter embedding is not a current runtime capability. It will be designed
again in Phase 8 from the then-current real API, exact model catalog,
dimensions, provider limits and pricing. No unused adapter, provider boundary,
remote configuration or fake HTTP tests remain in Phase 3.

## Approved dense architecture

Use one concrete class in `backend/embedding/embedder.py`:

```text
E5Embedder
├── model_id
├── dimension
├── device
├── batch_size
├── _model = None
├── _get_model()
├── embed_documents(texts)
└── embed_query(query)
```

Delete:

```text
backend/embedding/base.py
backend/embedding/batch_embed.py
backend/embedding/openrouter_embedder.py
```

Do not add compatibility wrappers for these internal modules.

### Model lifecycle

The model is loaded lazily into `self._model` and reused by that embedder
instance. This matches the Hue lifecycle:

- API startup creates one embedder, performs one real warm-up and keeps the
  same instance inside `DenseRetriever` for all requests;
- ingestion is a separate command/process and uses one embedder for the full
  corpus;
- the health endpoint reports cached startup readiness and does not load a
  second model.

No module-global singleton or `lru_cache` is needed. Tests should share a real
fixture/instance when repeated model loading would waste time.

### Document and query behavior

`embed_documents(texts)`:

1. returns `[]` for an empty input list without loading the model;
2. prepends `passage: ` to every text;
3. calls `SentenceTransformer.encode()` once with `batch_size=64` and
   `normalize_embeddings=True`;
4. returns plain Python `list[list[float]]` in input order.

`embed_query(query)`:

1. rejects a non-string, empty or whitespace-only query;
2. prepends `query: `;
3. calls the same loaded model;
4. returns one plain Python `list[float]`.

The E5 prefixes are constants owned by `E5Embedder`; they are not duplicated
in YAML. A future non-E5 or remote candidate receives its own Phase 8 design
instead of making this local baseline generic in advance.

### Minimal validation

Use built-in `ValueError` with short messages for contract/config errors. Do
not retain `EmbeddingError` or the shared BaseEmbedder validation framework.

Validate only:

- query input is non-empty text;
- the loaded model's actual dimension matches configured `dimension`;
- the number of returned document vectors matches the number of input texts;
- every returned vector has the configured dimension.

SentenceTransformer owns normalization through `normalize_embeddings=True`.
Do not normalize a second time or retain a separate NumPy validation layer.
Phase 4 continues to validate finite document vectors at the indexing
boundary. Model loading and encoding failures propagate to the existing
consumer error mapping; there is no silent fallback, padding, truncation or
automatic config rewrite.

## Configuration

The Phase 3 embedding configuration contains only values used by the local
runtime:

```yaml
embedding:
  model: intfloat/multilingual-e5-small
  vector_size: 384
  device: cpu
  batch_size: 64
```

Remove:

```text
embedding.provider
embedding.remote
embedding.document_prefix
embedding.query_prefix
```

These keys are not roadmap storage. Phase 8 will introduce exact provider and
instruction configuration only after a real candidate has been selected and
verified.

OpenAI/OpenRouter configuration used for answer generation is a separate
subsystem and is not changed by this Phase 3 work.

## Sparse representation

Keep the current deterministic TF-IDF behavior and output contract because
Phase 4 ingestion still creates named sparse vectors:

```python
{
    "indices": [0, 4, 9],
    "values": [1.2, 2.4, 1.0],
}
```

The runtime code should be moderately detailed rather than artificially
short. Use type hints, full variable names, small docstrings and comments only
where they explain a non-obvious reason.

The readable flow is:

```text
tokenize
-> fit ordered vocabulary and document frequency
-> count term frequency for one text
-> calculate IDF
-> return aligned indices and values
```

Preserve these behaviors:

- lowercase Unicode text;
- replace non-word/non-space characters with spaces;
- split on whitespace;
- assign vocabulary indices by deterministic first occurrence;
- count document frequency once per unique token in each document;
- reset all state when `fit()` is called again;
- ignore unknown tokens;
- return empty indices/values for empty encoded text;
- reject `encode()` before a non-empty vocabulary has been fitted;
- reproduce identical vectors from the same ordered corpus.

Notebook 03 must not access `_vocab`, `_document_frequency` or another private
attribute. Add only the smallest public explanatory surface actually needed;
do not expose internal state merely to make the notebook an inspector.

BM25 in Hue RAG imports only the shared `tokenize()` function; it does not
depend on the `SparseEmbedder` class. The class remains in Phase 3 because the
current Phase 4 ingestion/schema still stores sparse vectors. Removing that
unused stored representation is a coordinated Phase 4–5 decision, not part of
this implementation.

## Retrieval compatibility

Hue RAG already has both retrievers. `HybridRetriever` composes rather than
replaces `DenseRetriever`:

```text
E5Embedder
-> DenseRetriever
-> optional HybridRetriever BM25 fusion
-> optional CrossEncoder reranking
```

The three profiles remain:

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

`HybridRetriever` continues to request dense candidates through
`DenseRetriever` and applies Python BM25 only to that fixed candidate set. It
does not embed the query again and does not query Qdrant sparse vectors.

Do not assume hybrid is always better. Existing 104-case evidence has higher
Recall@5 for `dense_only`, higher Recall@10 for `hybrid_no_rerank`, and worse
quality/latency for the current `hybrid_rerank`. Phase 8 exists to compare the
trade-offs rather than promote a profile by intuition.

## Consumer changes

Update only the wiring directly required by the deleted modules and renamed
class:

- `backend/ingestion/pipeline.py` constructs `E5Embedder` and calls
  `embed_documents(texts)` directly;
- `backend/core/startup.py` constructs one `E5Embedder`, performs the existing
  real warm-up and passes that instance to `DenseRetriever`;
- imports, docstrings and type references to `BaseEmbedder`, `EmbeddingError`,
  `SentenceTransformerEmbedder`, `embed_in_batches` and
  `OpenRouterEmbedder` are removed or updated.

Do not redesign `DenseRetriever`, `HybridRetriever`, the profile router or the
ingestion/vectorstore contract. Necessary consumer edits are compatibility
wiring, not authorization to simplify another phase.

## Test design

Use a small behavior-oriented permanent suite. Test count is not an
acceptance criterion.

Dense tests use the real locally cached E5 model and cover:

- real document and query vectors have dimension 384;
- real vectors are normalized;
- empty document input returns `[]`;
- an empty query is rejected;
- multiple inputs produce the same number of vectors in the same order;
- a deliberately wrong configured dimension fails against the real model.

Sparse tests use a small, readable corpus with hand-computable output and
cover:

- Vietnamese lowercase/punctuation tokenization;
- known TF-IDF weights;
- deterministic vocabulary/vector output;
- reset on repeated `fit()`;
- empty and unknown text behavior;
- rejection before `fit()`.

Combine related assertions when one behavioral example proves them. Do not
test private helpers, every branch, logging text or an arbitrary target number
of cases. Delete OpenRouter embedding tests. Do not use mocked
SentenceTransformer responses, fake HTTP or replayed provider output as
implementation or completion evidence.

Existing downstream tests are run only as targeted smoke checks; do not create
a new downstream suite. The directly affected existing checks are ingestion
pipeline, startup and hybrid point building. Their purpose is to catch stale
imports or API wiring after files are deleted, not to replace real execution.

## Notebook 03

Keep `notebooks/03_embedding_models.ipynb` as a concise Vietnamese learning
walkthrough. It must:

- import only public Phase 2 and Phase 3 runtime APIs;
- load the real ordered 572-chunk corpus;
- run the real local E5 model on CPU with batch size 64;
- show model ID, dimension, `572 x 384` output shape, norms and elapsed time;
- demonstrate the query/document E5 roles;
- explain sparse tokenization, DF, IDF and output with a small worked corpus;
- avoid private attributes, copied algorithms and OpenRouter code;
- avoid becoming a test suite or validator;
- remain committed with empty outputs and `execution_count: null`.

Elapsed time is observed and reported, not enforced as a flaky threshold. The
Reviewer executes Run All on a temporary copy.

## Real verification

Verification proceeds from the focused behavior to the real runtime:

```text
compile affected Python modules
-> run focused real E5 and sparse tests
-> run Notebook 03 on all 572 real chunks
-> inspect active Qdrant read-only and confirm 572 points
-> execute one real query through E5 and the active collection
-> run existing ingestion/startup/hybrid-index smoke tests
-> run the full backend suite once before handoff
-> inspect deleted imports, config references and scoped diff
```

The direct active-Qdrant check must not upsert, reindex, reset or create a
collection. Downstream/full-suite tests may mutate only guarded isolated
collections with the `hue_rag_live_test_` prefix and must report cleanup.
Exact float equality or a vector checksum is not required because library
batching can introduce harmless floating-point differences. Compatibility is
proven by the same model/dimension/instructions and a successful real query
against the active index.

Focused tests and targeted consumer tests are supporting checks. The primary
evidence is the real E5 model, canonical data, executable Notebook 03 and
read-only active Qdrant query.

## Documentation changes

The implementation must align these canonical documents with the approved
design:

### Phase 3 guide

Update `guides/phase_3_embedding_sparse_representation.md` to remove the stale
requirements for `BaseEmbedder`, a live-ready OpenRouter adapter, remote config
and mock-only tests. Record the local E5 architecture, instance lifecycle,
native batching, minimal validation, real verification and temporary Phase 4
sparse compatibility.

### Phase 8 guide

Update `guides/phase_8_benchmark_model_selection.md` to record:

- the exact three-profile mapping shown above;
- local E5 versus future OpenRouter embedding as an approved future experiment
  group, not a current implementation;
- real API/model/dimension/limit/pricing verification before adapter design;
- separate collection/index when dimension or vector space changes;
- same corpus, questions and metrics for fair comparison;
- accuracy, latency, reliability/stability and API cost as decision criteria;
- no fake provider, silent fallback or assumption that hybrid always wins.

When Phase 8 begins, it may reintroduce provider/config abstractions justified
by the exact candidates being run.

### Reference guide

Update `guides/llm_rag_reference_for_hue_rag.md` to make the chosen lexical
path explicit:

```text
Qdrant dense candidate retrieval
-> Python BM25 fusion over those candidates
-> optional CrossEncoder reranking
```

Record that current stored Qdrant sparse vectors have no query consumer and
that their removal belongs to a coordinated Phase 4–5 simplicity review.

`session_prompt/Project_Status.md` changes only after implementation and
independent review are complete. `session_prompt/Session_Prompt.md` is general
governance and is not changed by this design.

## Implementation scope

Expected runtime/config/test/notebook edits:

```text
backend/embedding/base.py                         # delete
backend/embedding/batch_embed.py                  # delete
backend/embedding/openrouter_embedder.py          # delete
backend/embedding/embedder.py
backend/embedding/sparse_embedder.py
backend/config/settings.yaml
backend/ingestion/pipeline.py                     # compatibility wiring only
backend/core/startup.py                           # compatibility wiring only
backend/tests/test_embedder.py
backend/tests/test_sparse_embedder.py
notebooks/03_embedding_models.ipynb
```

Canonical documentation edits:

```text
guides/phase_3_embedding_sparse_representation.md
guides/phase_8_benchmark_model_selection.md
guides/llm_rag_reference_for_hue_rag.md
```

Tests owned by later phases may be updated only when a stale Phase 3 class or
module name makes the test fail to import. Do not use this exception to
rewrite later-phase behavior.

## Reviewer and Implementer workflow

The roles remain separate:

1. the Reviewer owns this approved design and the later implementation plan;
2. an Implementer changes only the approved scope and reports exact observed
   commands/results;
3. the Reviewer audits the diff independently and repeats the real verification;
4. only the user confirms final Phase 3 simplicity approval.

No code implementation is authorized by this design file. After the user
reviews this saved specification, the Reviewer uses `writing-plans` to produce
a separate step-by-step implementation plan.
