# Phase 3 Embedding and Sparse Representation Simplicity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce Phase 3 to one readable local E5 embedder plus one clear,
deterministic TF-IDF sparse representation while preserving the approved
Phase 4–7 runtime and proving compatibility with real data, models and Qdrant.

**Architecture:** `E5Embedder` owns the local model lifecycle, E5 instructions,
native SentenceTransformer batching and minimal boundary validation. The
existing deterministic `SparseEmbedder` keeps its Phase 4 output contract but
becomes easier to read. `DenseRetriever` remains the embedding consumer and
`HybridRetriever` continues to compose it with Python BM25.

**Tech Stack:** Python 3.13, sentence-transformers,
`intfloat/multilingual-e5-small`, pytest, Jupyter/nbconvert, Qdrant, YAML, `uv`.

## Global Constraints

- Read `session_prompt/Session_Prompt.md`, `session_prompt/Project_Status.md`,
  `session_prompt/IMPLEMENTER_WORKFLOW.md`, `guides/README.md`,
  `guides/phase_0_mvp_foundation.md`, the ready Phase 3 guide and
  `docs/superpowers/specs/2026-08-24-phase-3-embedding-sparse-representation-simplicity-design.md`
  before editing.
- Start with `using-superpowers`, use `executing-plans` task by task, apply
  `test-driven-development` to the dense API replacement,
  `systematic-debugging` to any unexpected real failure and
  `verification-before-completion` before handoff.
- Apply `skills/karpathy-guidelines/SKILL.md`: direct data flow, descriptive
  names, no speculative abstraction, no one-caller wrapper unless it makes a
  genuinely distinct concept easier to understand.
- Run `git status --short` and inspect exact scoped diffs first. Preserve every
  unrelated deletion and the existing Phase 6 notebook/report edits.
- The only dense model in Phase 3 is
  `intfloat/multilingual-e5-small`, local CPU, 384 dimensions, batch size 64.
- Keep `passage: ` for documents and `query: ` for queries. Do not make these
  configurable in Phase 3.
- Do not retain `BaseEmbedder`, `EmbeddingError`, outer batch helpers,
  `OpenRouterEmbedder`, embedding provider switching or remote embedding
  settings under another name.
- Do not change the Phase 4 dense+sparse Qdrant schema, point payload, BM25,
  retrieval fusion, reranking, generation, evaluation or active profile.
- The active `hue_foods_e5_small_384` collection is strictly read-only.
  Existing tests may mutate only guarded collections whose names begin with
  `hue_rag_live_test_`, and must report cleanup.
- Use the real locally cached E5 model, the real 572-chunk corpus and real
  Qdrant. Do not use mock/fake model output, HTTP responses, services, corpus
  data, replay or prior output as completion evidence.
- Do not run OpenRouter embedding calls. OpenRouter embedding belongs to
  Phase 8 and has no Phase 3 adapter/config/test after this change.
- Do not run the 20- or 104-question Phase 7 evaluation: the approved design
  preserves the same E5 model, instructions, dimension and retrieval
  algorithms. Stop and return to the Reviewer if observed retrieval behavior
  indicates this assumption is false.
- Do not edit canonical guides, the approved design, Reviewer reports,
  `Project_Status.md` or `Session_Prompt.md`; those belong to the Reviewer.
- Do not stage, commit or push. Each task ends in a testable checkpoint for
  Reviewer inspection instead of a commit.

## Reviewer Readiness Prerequisite

Before an Implementer starts Task 1, the Reviewer must align these canonical
documents with the approved design and set the Phase 3 simplicity work to
`ready`:

- `guides/phase_3_embedding_sparse_representation.md` — local E5-only
  architecture, deleted provider machinery, native batching, real tests and
  temporary Phase 4 sparse compatibility;
- `guides/phase_8_benchmark_model_selection.md` — future real OpenRouter
  embedding comparison and the exact three-profile mapping;
- `guides/llm_rag_reference_for_hue_rag.md` — dense Qdrant candidates, Python
  BM25 fusion, optional CrossEncoder, and deferred removal of unused stored
  sparse vectors.

The Implementer must stop if the guide still says to build an OpenRouter
adapter, mock provider calls or keep `BaseEmbedder`.

## File Map

**Delete:**

- `backend/embedding/base.py` — unused abstract provider contract and custom
  exception.
- `backend/embedding/batch_embed.py` — redundant outer batching layer.
- `backend/embedding/openrouter_embedder.py` — unused, unverified future
  provider adapter.

**Modify:**

- `backend/embedding/embedder.py` — concrete `E5Embedder` and instance-owned
  lazy model.
- `backend/embedding/sparse_embedder.py` — readable deterministic TF-IDF flow.
- `backend/config/settings.yaml` — only actual local embedding settings.
- `backend/ingestion/pipeline.py` — call `embed_documents()` directly.
- `backend/core/startup.py` — construct and warm one `E5Embedder` instance.
- `backend/tests/conftest.py` — real session fixture uses `E5Embedder`.
- `backend/tests/test_embedder.py` — minimal real E5 behaviors.
- `backend/tests/test_sparse_embedder.py` — concise hand-computable sparse
  behaviors.
- `backend/tests/test_startup.py` — rename stale concrete embedder imports.
- `notebooks/03_embedding_models.ipynb` — real 572-chunk learning walkthrough.

**Create:**

- `reports/phase_3_embedding_sparse_representation_simplicity_implementation_report.md`
  — exact observed evidence and Reviewer handoff.

**Verify without behavioral edits:**

- `backend/retrieval/dense_retriever.py`
- `backend/retrieval/hybrid_retriever.py`
- `backend/retrieval/service.py`
- `backend/vectorstore/hybrid_index.py`
- `backend/tests/test_ingestion_pipeline.py`
- `backend/tests/test_hybrid_index.py`

---

### Task 1: Lock scope and current real baseline

**Files:**

- Inspect: every file in the file map.
- Modify: none.

**Interfaces:**

- Consumes: current `SentenceTransformerEmbedder`, `SparseEmbedder`, 572 real
  chunks and active Qdrant state.
- Produces: an observed Before baseline and a confirmed caller list for safe
  module deletion.

- [ ] **Step 1: Inspect worktree and scoped changes**

From the repository root:

```bash
git status --short
git diff -- backend/embedding backend/config/settings.yaml backend/ingestion/pipeline.py backend/core/startup.py backend/tests/conftest.py backend/tests/test_embedder.py backend/tests/test_sparse_embedder.py backend/tests/test_startup.py notebooks/03_embedding_models.ipynb
```

Expected: the approved design/plan may be new, but no pre-existing change may
overlap the runtime/test/notebook scope. If an overlap exists, stop and report
the exact file instead of overwriting it.

- [ ] **Step 2: Confirm every current consumer before deletion/rename**

```bash
rg -n 'BaseEmbedder|EmbeddingError|SentenceTransformerEmbedder|embed_in_batches|batch_embed|OpenRouterEmbedder|embedding\["provider"\]|embedding\["remote"\]|document_prefix|query_prefix' backend notebooks guides --glob '*.py' --glob '*.ipynb' --glob '*.md'
```

Expected: runtime references are confined to the current embedding modules,
ingestion/startup and their tests; notebook/guide references match the known
stale Phase 3 material. Any new runtime consumer changes the approved file map
and must be returned to the Reviewer.

- [ ] **Step 3: Run the current focused baseline with real E5**

```bash
cd backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -m pytest tests/test_embedder.py tests/test_sparse_embedder.py -q --tb=short
```

Expected current baseline: 26 tests pass. Record the exact observed duration
and warnings. Cleanup output, if any, must mention only guarded
`hue_rag_live_test_` collections.

- [ ] **Step 4: Confirm the active collection without mutation**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -c 'from core.settings_loader import load_settings; from vectorstore.qdrant import client_from_settings; settings = load_settings(); db = settings["vector_database"]; client = client_from_settings(settings); print("collection", db["collection_name"]); print("points", client.count(db["collection_name"], exact=True).count)'
```

Expected:

```text
collection hue_foods_e5_small_384
points 572
```

Do not call collection creation, upsert, reset or deletion APIs in this step.

---

### Task 2: Replace the dense provider framework with `E5Embedder`

**Files:**

- Modify: `backend/tests/test_embedder.py`
- Modify: `backend/tests/conftest.py`
- Modify: `backend/embedding/embedder.py`
- Modify: `backend/config/settings.yaml`
- Modify: `backend/ingestion/pipeline.py`
- Modify: `backend/core/startup.py`
- Modify: `backend/tests/test_startup.py`
- Delete: `backend/embedding/base.py`
- Delete: `backend/embedding/batch_embed.py`
- Delete: `backend/embedding/openrouter_embedder.py`

**Interfaces:**

- Consumes: `SentenceTransformer`, local model ID, configured dimension/device/
  batch size and existing consumer calls to `embed_documents()`/
  `embed_query()`.
- Produces: `E5Embedder(model_id: str, dimension: int, device: str = "cpu",
  batch_size: int = 64)`, public `model_id`/`dimension` attributes,
  `embed_documents(list[str]) -> list[list[float]]` and
  `embed_query(str) -> list[float]`.

- [ ] **Step 1: Replace dense tests with the approved real behaviors**

Replace `backend/tests/test_embedder.py` with a compact suite equivalent to:

```python
"""Real behavioral tests for the local multilingual E5 embedder."""
import math

import pytest

from embedding.embedder import E5Embedder

MODEL_ID = "intfloat/multilingual-e5-small"
DIMENSION = 384


def test_empty_documents_and_invalid_queries(real_embedder):
    assert real_embedder.embed_documents([]) == []
    for query in ("", "   ", None):
        with pytest.raises(ValueError, match="query"):
            real_embedder.embed_query(query)


def test_real_document_vectors_keep_order_shape_and_norm(real_embedder):
    texts = ["Bún bò Huế", "Cơm hến", "Bánh ép mè xửng"]
    vectors = real_embedder.embed_documents(texts)
    assert real_embedder.model_id == MODEL_ID
    assert real_embedder.dimension == DIMENSION
    assert len(vectors) == len(texts)
    assert all(len(vector) == DIMENSION for vector in vectors)
    assert all(math.isfinite(value) for vector in vectors for value in vector)
    assert all(
        math.sqrt(sum(value * value for value in vector))
        == pytest.approx(1.0, abs=1e-4)
        for vector in vectors
    )
    first_alone = real_embedder.embed_documents([texts[0]])[0]
    last_alone = real_embedder.embed_documents([texts[-1]])[0]
    assert vectors[0] == pytest.approx(first_alone, abs=1e-5)
    assert vectors[-1] == pytest.approx(last_alone, abs=1e-5)


def test_query_and_document_use_distinct_real_e5_roles(real_embedder):
    text = "Bún bò Huế"
    query_vector = real_embedder.embed_query(text)
    document_vector = real_embedder.embed_documents([text])[0]
    assert len(query_vector) == DIMENSION
    assert query_vector != pytest.approx(document_vector, abs=1e-6)


def test_real_model_rejects_wrong_configured_dimension():
    embedder = E5Embedder(MODEL_ID, dimension=3, device="cpu", batch_size=64)
    with pytest.raises(ValueError, match="dimension"):
        embedder.embed_query("Bún bò Huế")
```

Delete every OpenRouter, custom-prefix, shared-process-cache and outer-batch
test. These tests protect mechanisms being removed, not current user behavior.

- [ ] **Step 2: Rename the real shared fixture and observe RED**

In `backend/tests/conftest.py`, change only the concrete import/construction:

```python
from embedding.embedder import E5Embedder

return E5Embedder(
    model_id=embedding["model"],
    dimension=embedding["vector_size"],
    device=embedding["device"],
    batch_size=embedding["batch_size"],
)
```

Run:

```bash
cd backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -m pytest tests/test_embedder.py -q --tb=short
```

Expected RED: test collection fails during import because `E5Embedder` does not
exist yet. Do not keep a temporary alias to make the old implementation pass.

- [ ] **Step 3: Implement the concrete local E5 class**

Replace `backend/embedding/embedder.py` with this direct structure:

```python
"""Local dense embedding with multilingual E5."""

DOCUMENT_PREFIX = "passage: "
QUERY_PREFIX = "query: "


class E5Embedder:
    """Embed documents and queries with one lazily loaded local E5 model."""

    def __init__(self, model_id, dimension, device="cpu", batch_size=64):
        self.model_id = model_id
        self.dimension = dimension
        self.device = device
        self.batch_size = batch_size
        self._model = None

    def _get_model(self):
        """Load the configured model once for this embedder instance."""
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer(self.model_id, device=self.device)
            actual_dimension = model.get_sentence_embedding_dimension()
            if actual_dimension != self.dimension:
                raise ValueError(
                    f"model dimension {actual_dimension} != configured "
                    f"{self.dimension}"
                )
            self._model = model
        return self._model

    def _encode(self, texts):
        model = self._get_model()
        vectors = model.encode(
            texts,
            batch_size=self.batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).tolist()
        if len(vectors) != len(texts):
            raise ValueError(
                f"model returned {len(vectors)} vectors for {len(texts)} texts"
            )
        for vector in vectors:
            if len(vector) != self.dimension:
                raise ValueError(
                    f"vector dimension {len(vector)} != configured {self.dimension}"
                )
        return vectors

    def embed_documents(self, texts):
        """Return normalized passage vectors in the same order as texts."""
        if not texts:
            return []
        return self._encode([f"{DOCUMENT_PREFIX}{text}" for text in texts])

    def embed_query(self, query):
        """Return one normalized query vector."""
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        return self._encode([f"{QUERY_PREFIX}{query}"])[0]
```

Do not add logging, NumPy processing, a base class, protocol, factory, provider
switch or configurable prefixes.

- [ ] **Step 4: Update configuration and the two runtime constructors**

Reduce the YAML embedding block to:

```yaml
embedding:
  model: intfloat/multilingual-e5-small
  vector_size: 384
  device: cpu
  batch_size: 64
```

In `backend/ingestion/pipeline.py`, import `E5Embedder`, construct it from the
four keys above, remove `embed_in_batches`, and replace the dense call with:

```python
dense_embedder = embedder if embedder is not None else _build_embedder(settings)
dense = dense_embedder.embed_documents(texts)
```

In `backend/core/startup.py`, import and return `E5Embedder` from
`_query_embedder(settings)`. Update `_warm_embedder()` documentation so it says
the concrete embedder validates query input and dimension; remove the stale
`BaseEmbedder` claim.

In `backend/tests/test_startup.py`, update `make_fresh_embedder()` to import and
construct `E5Embedder` with the same four arguments. Do not otherwise change
startup behavior or tests.

- [ ] **Step 5: Remove obsolete modules after all callers are updated**

Delete exactly:

```text
backend/embedding/base.py
backend/embedding/batch_embed.py
backend/embedding/openrouter_embedder.py
```

Then verify no Python consumer remains:

```bash
rg -n 'BaseEmbedder|EmbeddingError|SentenceTransformerEmbedder|embed_in_batches|OpenRouterEmbedder|embedding\.base|embedding\.batch_embed|embedding\.openrouter_embedder' backend --glob '*.py'
```

Expected: no matches. Guide/report history may still mention old names until
Reviewer-owned documentation is synchronized; do not edit it here.

- [ ] **Step 6: Reach GREEN with the real model**

```bash
cd backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -m pytest tests/test_embedder.py -q --tb=short
```

Expected: the four approved dense behavior tests pass using the real cached
E5 model. No OpenRouter test is collected and no network provider call occurs.

---

### Task 3: Make `SparseEmbedder` moderately detailed and readable

**Files:**

- Modify: `backend/tests/test_sparse_embedder.py`
- Modify: `backend/embedding/sparse_embedder.py`

**Interfaces:**

- Consumes: ordered `list[str]` corpus texts.
- Produces: `tokenize(str) -> list[str]`,
  `SparseEmbedder.fit(list[str]) -> SparseEmbedder`, `vocabulary_size: int`
  and `encode(str) -> dict[str, list]` with aligned deterministic indices and
  positive TF-IDF values.

- [ ] **Step 1: Consolidate sparse tests around six distinct behaviors**

Replace overlapping checks with a suite equivalent to:

```python
"""Behavioral tests for the deterministic TF-IDF sparse representation."""
import math

import pytest

from embedding.sparse_embedder import SparseEmbedder, tokenize


def test_tokenize_vietnamese_text():
    assert tokenize("Bún bò Huế, cà-phê (muối)!") == [
        "bún", "bò", "huế", "cà", "phê", "muối"
    ]


def test_known_tfidf_values_and_document_frequency():
    embedder = SparseEmbedder().fit(["a b a c", "b c"])
    result = embedder.encode("a a b")
    expected_a = 2 * (math.log(3 / 2) + 1)
    assert embedder.vocabulary_size == 3
    assert result["indices"] == [0, 1]
    assert result["values"] == pytest.approx([expected_a, 1.0])


def test_same_ordered_corpus_reproduces_vectors():
    corpus = ["bún bò huế", "cơm hến", "bánh ép mè xửng"]
    first = SparseEmbedder().fit(corpus)
    second = SparseEmbedder().fit(corpus)
    assert [first.encode(text) for text in corpus] == [
        second.encode(text) for text in corpus
    ]


def test_fit_again_resets_previous_state():
    embedder = SparseEmbedder().fit(["bún bò huế"])
    embedder.fit(["cơm hến"])
    assert embedder.vocabulary_size == 2
    assert embedder.num_documents == 1
    assert embedder.encode("bún") == {"indices": [], "values": []}


def test_empty_and_unknown_text_return_empty_vectors():
    embedder = SparseEmbedder().fit(["bún bò huế"])
    expected = {"indices": [], "values": []}
    assert embedder.encode("") == expected
    assert embedder.encode("phở gà") == expected


def test_encode_before_fit_is_rejected():
    with pytest.raises(ValueError, match="fit"):
        SparseEmbedder().encode("bún bò huế")
```

Run this suite against the current implementation first:

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -m pytest tests/test_sparse_embedder.py -q --tb=short
```

Expected: all six characterization tests pass before the readability refactor.
If one fails, verify the approved contract instead of changing behavior to fit
the draft test.

- [ ] **Step 2: Refactor the module without changing its contract**

Keep the module close to this complete structure:

```python
"""Deterministic TF-IDF sparse representation for lexical signals."""
import math
import re
from collections import Counter

NON_WORD = re.compile(r"[^\w\s]")


def tokenize(text: str) -> list[str]:
    """Lowercase text, replace punctuation with spaces and split tokens."""
    return NON_WORD.sub(" ", text.lower()).split()


class SparseEmbedder:
    """Build an ordered vocabulary and encode texts with TF-IDF values."""

    def __init__(self):
        self.num_documents = 0
        self._vocabulary: dict[str, int] = {}
        self._document_frequency: dict[str, int] = {}

    @property
    def vocabulary_size(self) -> int:
        """Return the number of tokens learned by the latest fit."""
        return len(self._vocabulary)

    def fit(self, texts: list[str]) -> "SparseEmbedder":
        """Reset state and learn vocabulary/DF in corpus order."""
        self.num_documents = 0
        self._vocabulary = {}
        self._document_frequency = {}
        for text in texts:
            # dict.fromkeys keeps first occurrence while counting each token's
            # document frequency only once for this document.
            for token in dict.fromkeys(tokenize(text)):
                if token not in self._vocabulary:
                    self._vocabulary[token] = len(self._vocabulary)
                self._document_frequency[token] = (
                    self._document_frequency.get(token, 0) + 1
                )
            self.num_documents += 1
        return self

    def encode(self, text: str) -> dict[str, list]:
        """Encode one text as aligned vocabulary indices and TF-IDF values."""
        if not self._vocabulary:
            raise ValueError("SparseEmbedder must be fit before encode")
        term_frequencies = Counter(
            token for token in tokenize(text) if token in self._vocabulary
        )
        indices: list[int] = []
        values: list[float] = []
        for token, term_frequency in term_frequencies.items():
            document_frequency = self._document_frequency[token]
            inverse_document_frequency = math.log(
                (self.num_documents + 1) / (document_frequency + 1)
            ) + 1
            indices.append(self._vocabulary[token])
            values.append(float(term_frequency * inverse_document_frequency))
        return {"indices": indices, "values": values}
```

Do not expose the vocabulary mapping, add serialization, create a statistics
object or move BM25 into this module.

- [ ] **Step 3: Prove the refactor stayed GREEN**

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -m pytest tests/test_sparse_embedder.py -q --tb=short
```

Expected: the same six tests pass. Then run the real Phase 4 point builder
consumer:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -m pytest tests/test_hybrid_index.py -q --tb=short
```

Expected: all collected hybrid-index tests pass with real E5/sparse outputs;
no active collection is mutated. Record the exact observed count rather than
treating it as a permanent target.

---

### Task 4: Rewrite Notebook 03 as the real learning walkthrough

**Files:**

- Modify: `notebooks/03_embedding_models.ipynb`

**Interfaces:**

- Consumes: `chunk_foods_markdown()`, `E5Embedder`, `SparseEmbedder`,
  `tokenize()` and the four local embedding settings.
- Produces: a clean notebook that runs the real 572-document embedding path
  and explains dense/sparse output without private APIs.

- [ ] **Step 1: Reduce the notebook to one concept per cell**

Use this cell sequence:

1. Markdown: Phase 3 purpose and local-only E5 boundary.
2. Code: imports, backend path setup and settings load.
3. Markdown: why E5 distinguishes passages and queries.
4. Code: create `E5Embedder`, load 572 chunks and embed all texts while timing.
5. Code: print model ID, chunk count, dense shape, first-vector norm and elapsed
   seconds.
6. Markdown: explain what the observed shape/norm/time mean; time is not a
   pass threshold.
7. Code: embed the same Vietnamese phrase once as a query and once as a
   document, then print their cosine similarity.
8. Markdown: explain tokenization, TF, DF and IDF using a three-document mini
   corpus.
9. Code: call public `tokenize()`, `SparseEmbedder.fit()` and `encode()` and
   print only public outputs plus `vocabulary_size`.
10. Markdown: explain that sparse vectors remain for current Phase 4
    compatibility, while retrieval uses dense candidates plus Python BM25.
11. Markdown: state that OpenRouter embedding comparison belongs to Phase 8.

The core code cells should use these calls rather than copying algorithms:

```python
embedding = settings["embedding"]
embedder = E5Embedder(
    model_id=embedding["model"],
    dimension=embedding["vector_size"],
    device=embedding["device"],
    batch_size=embedding["batch_size"],
)
chunks = chunk_foods_markdown()
texts = [chunk["text"] for chunk in chunks]
started = time.perf_counter()
dense_vectors = embedder.embed_documents(texts)
elapsed_seconds = time.perf_counter() - started
```

```python
sample = "Bún bò Huế"
query_vector = embedder.embed_query(sample)
document_vector = embedder.embed_documents([sample])[0]
cosine_similarity = sum(
    query_value * document_value
    for query_value, document_value in zip(query_vector, document_vector)
)
print("query/document cosine:", round(cosine_similarity, 4))
```

```python
sparse_corpus = ["bún bò huế", "cơm hến", "bún bò giò heo"]
sparse_embedder = SparseEmbedder().fit(sparse_corpus)
print("tokens:", tokenize(sparse_corpus[0]))
print("documents:", sparse_embedder.num_documents)
print("vocabulary size:", sparse_embedder.vocabulary_size)
print("encoded sample:", sparse_embedder.encode("bún bò bò huế"))
```

Do not access `_model`, `_vocabulary`, `_document_frequency` or copy the IDF
formula into Python. A hand calculation may appear in the preceding Markdown
cell.

- [ ] **Step 2: Keep the repository notebook clean**

Use `apply_patch` for the notebook JSON edit. The committed file must satisfy:

```bash
jq -e 'all(.cells[] | select(.cell_type == "code"); .execution_count == null and (.outputs | length == 0))' notebooks/03_embedding_models.ipynb
```

Expected: exit code 0 and output `true`.

- [ ] **Step 3: Run All on a temporary output**

From repository root:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file .env jupyter nbconvert --execute --to notebook notebooks/03_embedding_models.ipynb --output /tmp/03_embedding_models-phase3-simplicity.ipynb --ExecutePreprocessor.timeout=900
```

Expected: nbconvert exits 0. Inspect the temporary notebook and record these
observations in the implementation report:

```text
chunks 572
dense shape 572 x 384
first vector norm approximately 1.0
one finite elapsed time
one finite query/document cosine
one deterministic sparse example
```

Do not copy executed outputs back into the repository notebook.

---

### Task 5: Verify the real runtime and write the Implementer handoff

**Files:**

- Create:
  `reports/phase_3_embedding_sparse_representation_simplicity_implementation_report.md`
- Verify: all modified/deleted files and direct consumers.

**Interfaces:**

- Consumes: completed Tasks 1–4, active read-only Qdrant, guarded isolated
  test collections and the real local E5 model.
- Produces: independently auditable evidence for the Codex Reviewer.

- [ ] **Step 1: Compile and scan deleted APIs/config**

From repository root:

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run python -m compileall -q embedding ingestion/pipeline.py core/startup.py
cd ..
test ! -e backend/embedding/base.py
test ! -e backend/embedding/batch_embed.py
test ! -e backend/embedding/openrouter_embedder.py
rg -n 'BaseEmbedder|EmbeddingError|SentenceTransformerEmbedder|embed_in_batches|OpenRouterEmbedder|embedding\.remote|document_prefix|query_prefix' backend notebooks/03_embedding_models.ipynb --glob '*.py' --glob '*.ipynb'
```

Expected: compile and the three deletion checks exit 0; the final `rg` returns
no match.

- [ ] **Step 2: Run the final focused Phase 3 tests**

```bash
cd backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -m pytest tests/test_embedder.py tests/test_sparse_embedder.py -q --tb=short
```

Expected: all ten deliberately retained focused tests pass using the real E5
model and real code. The count documents the planned suite shape; quality is
still judged by distinct behaviors and real execution, not the number ten.

- [ ] **Step 3: Query the active collection read-only through the real stack**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -c 'from core.settings_loader import load_settings; from retrieval.service import build_service; settings = load_settings(); service = build_service(settings); documents = service.search("Bún bò Huế có đặc điểm gì?"); print("profile", service.active_profile); print("results", len(documents)); print("top_chunk", documents[0].metadata["chunk_id"] if documents else None)'
```

Expected: `profile dense_only`, a positive result count and a non-empty top
chunk ID. This command must not call any Qdrant mutation API.

- [ ] **Step 4: Run directly affected existing tests**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -m pytest tests/test_ingestion_pipeline.py tests/test_startup.py tests/test_hybrid_index.py -q --tb=short
```

Expected: all collected tests pass. Qdrant mutation is limited to guarded
`hue_rag_live_test_` collections; cleanup must be reported and the active
collection must remain untouched. Record the exact count/duration as observed
evidence, not a future acceptance target.

- [ ] **Step 5: Run the final full backend suite once**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -m pytest tests -q --tb=short
```

Expected: every collected backend test passes. The total will be lower than
the historical 206 because obsolete OpenRouter, batching and abstraction tests
were intentionally removed. Report the observed count and warnings without
turning them into a permanent threshold. Confirm guarded collection cleanup.

- [ ] **Step 6: Reconfirm active Qdrant safety**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -c 'from core.settings_loader import load_settings; from vectorstore.qdrant import client_from_settings; settings = load_settings(); db = settings["vector_database"]; client = client_from_settings(settings); print("active_collection", db["collection_name"], "points", client.count(db["collection_name"], exact=True).count); print("guarded_leftovers", sorted(c.name for c in client.get_collections().collections if c.name.startswith("hue_rag_live_test_")))'
```

Expected:

```text
active_collection hue_foods_e5_small_384 points 572
guarded_leftovers []
```

If a guarded leftover exists, use only the existing guarded cleanup function
and report the exact collection/outcome. Never delete an unmarked collection.

- [ ] **Step 7: Inspect final scope and write the six-section report**

```bash
cd ..
git diff --check
git diff --name-status
git diff -- backend/embedding backend/config/settings.yaml backend/ingestion/pipeline.py backend/core/startup.py backend/tests/conftest.py backend/tests/test_embedder.py backend/tests/test_sparse_embedder.py backend/tests/test_startup.py notebooks/03_embedding_models.ipynb
rg -n '<<<<<<<|=======|>>>>>>>' backend notebooks/03_embedding_models.ipynb guides reports --glob '*.py' --glob '*.yaml' --glob '*.ipynb' --glob '*.md'
```

Expected: no whitespace errors or merge markers; scoped changes match the file
map; unrelated worktree changes remain untouched.

Create the implementation report from
`session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md` with exactly these observed
categories:

1. Phase 3 scope and deleted abstractions;
2. concrete E5/sparse/config/notebook changes;
3. exact real commands run;
4. observed focused, notebook, read-only active query, downstream and full-suite
   results;
5. failures/limitations, including anything not run;
6. handoff asking the Reviewer to audit independently.

Do not describe expected commands as observed results. Do not approve the
phase, edit Reviewer documents, stage, commit or push.

## Reviewer Audit Handoff

The Reviewer independently checks:

1. the diff contains no compatibility wrapper or future-provider machinery;
2. the saved notebook is clean and its temporary Run All uses all 572 chunks;
3. focused tests use the real E5 model and preserve only distinct behaviors;
4. the active collection remains `hue_foods_e5_small_384` with 572 points;
5. a real active-collection query succeeds;
6. any Qdrant mutations target only guarded test collections and cleanup is
   complete;
7. Phase 8 documentation contains the approved OpenRouter/profile comparison
   roadmap without claiming a winner.

Only the user may confirm final Phase 3 simplicity approval and separately
authorize commit/push.
