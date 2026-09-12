# Phase 4 Full-corpus Qdrant Ingestion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking. Do not dispatch sub-agents unless the
> User grants that authority separately.

**Goal:** Tạo và kiểm chứng bốn isolated full-corpus Qdrant collections, mỗi
collection chứa exact `8.460` Representation A points với named dense/sparse
vectors và một final-only deterministic build record.

**Architecture:** Một static Phase 4 registry ghép bốn Phase 3 dense specs với
bốn semantic collection names. Pipeline rediscover/chunk fresh, xác minh exact
corpus/sparse identities, encode một NumPy matrix cho từng model, rồi dựng và
upsert tối đa 64 dense+sparse points mỗi batch; completion verification xảy ra
trước atomic build-record write. Foods code/config/collections được giữ nguyên,
Notebook 04 chỉ inspect bốn targets read-only.

**Tech Stack:** Python 3.13, NumPy 2.5.1, Sentence Transformers 5.6.1,
Transformers 5.14.1, PyTorch 2.13.0+cu130, PyVi 0.1.1, qdrant-client 1.19.0,
Qdrant v1.18.3, pytest, Jupyter/nbconvert, JSON/SHA-256.

```text
Status: approved by User 2026-09-12 +07
Written Spec: approved by User 2026-09-12 +07
Risk: high
Implementation authorization: Tasks 1–6 through the active implementation handoff
Read-only Qdrant authorization: exact four-target preflight in Task 6
Live Qdrant write authorization: separate exact gate after Task 6 preflight
Git authorization: none
```

## Global Constraints

- Canonical Written Spec:
  `docs/superpowers/specs/2026-09-12-phase-4-full-corpus-qdrant-ingestion-written-spec.md`.
- Closed input is exactly `205` sorted canonical files, `8.460` Representation A
  chunks and corpus identity
  `0e5c059516cd942b151286cf597f785c65e642cacd1b0421124fe50fe574f223`.
- Sparse state is exactly `data/full_corpus_builds/phase_3_sparse_state.json`,
  SHA-256 `5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be`,
  schema `phase_3_sparse_state:v1`, `8.460` documents, vocabulary `5.662`,
  `k1=1.5`, `b=0.75`.
- Exact 12-point sample comes from
  `reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json`.
- Candidate order and exact targets are:
  `e5-small-384 -> hue_full_corpus_a_e5_small_384`,
  `e5-base-768 -> hue_full_corpus_a_e5_base_768`,
  `huydang-dek21-768 -> hue_full_corpus_a_huydang_dek21_768`,
  `qwen3-embedding-0.6b-1024 -> hue_full_corpus_a_qwen3_06b_1024`.
- Read model ID/revision/dimension/preprocessing/device/dtype/batch directly from
  `DENSE_MODEL_SPECS`; do not duplicate model configuration in settings.
- E5-small/E5-base/HuyDang run CPU FP32 batch 8. Qwen runs CUDA FP16/eager,
  native 1024D, batch 1. No fallback, quantization, alternate dimension,
  revision, attention or automatic batch change.
- Schema contains only named `dense` cosine and named `sparse` with
  `SparseVectorParams()` and `modifier=None`. Do not enable Qdrant IDF.
- Payload has exactly `search_text`, `source`, `title`, `heading_path`,
  `evidence_parts`; IDs use the existing Hue UUID5 contract.
- Target is absent or existing-empty with exact schema and no final record.
  Non-empty/mismatched/record-present fails before model/write. Recheck exact
  observed state immediately before create/upsert.
- No replace, reset, delete, reconcile, resume, retry, suffix, alias, shared
  registry, rollback or cleanup path.
- Keep one NumPy matrix per candidate; never call `.tolist()` on the entire
  matrix. Convert rows only while building at most 64 points.
- Run candidates sequentially in the locked order and stop on first failure.
  Phase PASS requires all four collections and records.
- Plan approval authorizes only code/docs, pure/local checks and read-only
  inspection of the four targets. Full dense inference and Qdrant writes wait
  for the separate live approval after Task 6.
- Do not query or mutate `hue_foods_e5_small_384` or
  `hue_foods_e5_small_384_dense`; do not edit `backend/config/settings.yaml`.
- No fake/mock/stub Qdrant client, embedded Qdrant or disposable test collection.
  Real integration evidence is the four approved candidate builds.
- No retrieval/RRF/reranker/benchmark/winner/cutover/Representation B/API/
  frontend/generation/Golden/evaluation/paid API.
- Notebook 04 remains read-only; canonical outputs are empty and execution
  counts null. Run All only on a `/tmp` copy after all four builds.
- Git authorization is `none`: no add, commit, push, reset, clean or checkout.

---

## File map and ownership

| Path | Action | Responsibility |
|---|---|---|
| `backend/embedding/full_corpus.py` | Modify | Add validated NumPy output while preserving Phase 3 list API. |
| `backend/embedding/sparse.py` | Modify | Reuse one checked vocabulary index across document encodes. |
| `backend/ingestion/source_state.py` | Modify | Build/serialize/write/freshness-check Phase 4 records. |
| `backend/vectorstore/qdrant.py` | Modify | Dense+sparse schema and fresh-target guards beside unchanged Foods APIs. |
| `backend/vectorstore/points.py` | Modify | Construct exact full-corpus points in batches of at most 64. |
| `backend/vectorstore/upsert.py` | Modify | Batch write and completion verification helpers. |
| `backend/ingestion/full_corpus_pipeline.py` | Create | Registry, fresh preparation, preflight CLI and one-candidate orchestration. |
| `backend/tests/test_full_corpus_embedding.py` | Modify | NumPy contract tests. |
| `backend/tests/test_full_corpus_sparse.py` | Modify | Vocabulary lookup equivalence tests. |
| `backend/tests/test_full_corpus_qdrant_ingestion.py` | Create | Pure Phase 4 guards; no client double. |
| `notebooks/04_qdrant_ingestion.ipynb` | Modify | Read-only four-target inspector. |
| `reports/artifacts/full_corpus_phase_4_qdrant_preflight_2026_09_12.json` | Create in Task 6 | Fresh preflight package. |
| `data/full_corpus_builds/<exact_collection>.json` | Generate after live approval | Four ignored final records. |
| `reports/full_corpus_phase_4_qdrant_ingestion_implementation_2026_09_12.md` | Create | Evidence and acceptance map, not approval. |

Reviewer owns this Plan, Written Spec, Phase 4 guide, `CURRENT_HANDOFF.md`, final
review and user report. Immutable paths requiring before/after evidence are
`backend/config/settings.yaml`, `docker-compose.yml`, `pyproject.toml`, `uv.lock`,
Foods pipeline/embedder, retrieval/generation/API/frontend trees, all 205 source
Markdown files, Phase 2/3 artifacts, Phase 3 sparse state, Foods Golden/results
and both Foods collections.

## Public interfaces locked by this plan

```text
backend.embedding.full_corpus
  validate_vector_matrix(np.ndarray, expected_count, expected_dim) -> np.ndarray
  FullCorpusDenseRunner.embed_documents_matrix(texts) -> np.ndarray

backend.embedding.sparse
  build_vocabulary_index(SparseState) -> dict[str, int]
  encode_sparse_document(text, state, vocabulary_index=None) -> SparseVector

backend.ingestion.source_state
  make_full_corpus_build_record(collection_name, candidate_id, model_id,
    revision, dimension, corpus_identity, sources, sparse_state,
    sparse_state_sha256; all keyword-only) -> dict[str, Any]
  serialize_full_corpus_build_record(record) -> bytes
  write_final_full_corpus_build_record(record, path) -> str
  verify_full_corpus_record_freshness(current_state, record) -> tuple[bool, list[str]]

backend.vectorstore.qdrant
  FullCorpusTargetObservation(state, point_count, build_record_exists, blockers)
  expected_full_corpus_schema(dimension) -> tuple[dense config, sparse config]
  validate_full_corpus_collection_params(params, dimension) -> None
  validate_full_corpus_collection_info(info, dimension) -> None
  classify_full_corpus_target(exists, point_count, schema_error,
    build_record_exists; all keyword-only) -> FullCorpusTargetObservation
  inspect_full_corpus_target(client, collection_name, dimension, record_path, timeout)
  require_fresh_full_corpus_target(observation) -> Literal["absent", "empty"]
  create_full_corpus_collection(client, collection_name, dimension, timeout) -> None

backend.vectorstore.points
  validate_full_corpus_point_inputs(chunks, dense_matrix, dimension,
    sparse_state, vocabulary_index) -> None
  build_full_corpus_point_batch(chunks, dense_rows, dimension, sparse_state, vocabulary_index)
    -> list[models.PointStruct]

backend.vectorstore.upsert
  upsert_full_corpus_batch(client, collection_name, points, timeout) -> int
  compare_full_corpus_records(records, expected_payloads) -> set[str]
  validate_sample_vectors(records, expected_dimension, expected_ids) -> None
  verify_full_corpus_collection(client, collection_name, dimension, chunks,
    sample_chunk_ids, timeout) -> dict[str, int]

backend.ingestion.full_corpus_pipeline
  FullCorpusCandidate(candidate_id, collection_name, dense_spec)
  FULL_CORPUS_CANDIDATES: tuple[FullCorpusCandidate, ...]
  candidate_by_id(candidate_id) -> FullCorpusCandidate
  prepare_full_corpus_input() -> PreparedFullCorpus
  run_read_only_preflight() -> tuple[dict[str, Any], int]
  build_candidate(candidate_id) -> dict[str, Any]
  main() -> None
```

## Review Contract

**Risk level:** `high`. Triggers are durable database writes, four full-corpus
model runs, CUDA/VRAM, public vector/payload/record contracts, ignored local
records, corpus-wide verification and a dirty worktree.

**Required Implementer evidence:**

1. exact base `071b1137bd5d1af60053bd3bb2c3fe47ba29ac0f`, head and complete
   before/after worktree inventory with unrelated changes preserved;
2. exact Phase 4 changed paths and immutable before/after evidence;
3. every focused RED/GREEN command and final deterministic test result;
4. NumPy matrix identity/no-full-list proof and preserved Phase 3 list behavior;
5. registry plus exact model/revision/dimension/device/dtype/batch mapping;
6. fresh 205/8.460/corpus/sparse/sample identities and the same preflight
   205-source LF-hash mapping before every candidate;
7. initial preflight artifact with server/client, RAM/swap/disk/GPU and four
   exact target/record states;
8. verbatim User live-write approval before Task 7;
9. per candidate command, target state, matrix shape/dtype/norm range, resource
   observations, batch counts, exact schema/count, full ID/payload result,
   12-sample vector result and record path/SHA;
10. exact failure/progress evidence with preserved partial target and stopped
    sequence; no automatic delete/retry/continuation;
11. final read-only preflight proving non-empty plus record-present guards;
12. temporary Notebook 04 Run All and canonical cleanliness;
13. report acceptance map, failed/skipped/not-verified items, limitations and
    statement that Implementer does not approve/close the Phase.

**Independent Reviewer:** read all changed/untracked paths and exact diffs; map
them to Spec/Plan; inspect no-fallback/pre-mutation/TOCTOU guards, exact schema,
batch memory behavior, records and evidence; run targeted read-only checks on
all four exact targets after builds; verify immutable paths and `git diff --check`.

Exact deterministic rerun from repository root:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-review-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_qdrant_ingestion.py \
  -q --tb=short
git diff --check
```

Expected: tests PASS without model load/network/Qdrant connection or mutation;
`git diff --check` prints nothing. Reviewer does not repeat four expensive
encodes/writes unless evidence conflicts or relevant inputs/runtime changed.

Phase 2/3 evidence supplies expected identities only. Phase 4 corpus checks,
target state, inference, writes, completion and records require fresh evidence.
Within corrections, a completed candidate is reusable only when corpus, sparse,
model, schema, verification code and Qdrant state are unchanged.

**New User authority required:** Qdrant read before Plan approval; create/upsert
before exact live approval; delete/reset/recovery; Foods access; replacement/
resume; model/schema/payload/ID/dependency/settings change; Qdrant tuning;
retrieval/benchmark/cutover; paid API; Git write; scope/risk expansion.

Blocker/major prevents readiness; non-impacting minor does not force correction.
Reviewer verdict is `PASS`, `PASS WITH LIMITATIONS`, `BLOCKED` or `FAIL`; only
User confirms Phase closure.

## Written Spec coverage map

| Written Spec requirement | Plan coverage |
|---|---|
| §2 exact fresh corpus/sparse dependencies | Task 6 Steps 3–5; Task 7 Step 1 |
| §3 two authority checkpoints | Task 6 Step 8; Task 7 Step 1; Plan approval effect |
| §4 static four-candidate registry | Task 6 Steps 1–3 |
| §5 exact dense+sparse/default schema | Task 4; Task 7 completion evidence |
| §6 UUID5, five-field payload, pre-write validation | Task 5 Steps 1–3 |
| §7 fresh target, TOCTOU recheck, partial failure | Task 4; Task 6 Step 5; Task 7 |
| §8 NumPy matrix, batch 64, sequential model lifecycle | Tasks 1–2, Task 5, Task 6 Step 5, Task 7 |
| §9 count/full ID-payload/12-vector verification | Task 5 Steps 4–5; Task 7 Step 6 |
| §10 final-only deterministic records | Task 3; Task 7 Steps 2–6 |
| §11 direct component ownership | File map and Tasks 1–6 |
| §12 pure tests plus real candidate evidence | Review Contract; Tasks 1–7 |
| §13 Notebook 04 read-only | Task 8 Steps 1–3 |
| §14 all-four acceptance | Review Contract; Task 7; Task 8 report |
| §15 exclusions/Phase 5 boundary | Global Constraints; Task 8 narrative |

---

### Task 1: Dense NumPy matrix path

**Files:** Modify `backend/embedding/full_corpus.py` and
`backend/tests/test_full_corpus_embedding.py`.

**Interfaces:** Consumes existing `DenseModelSpec`, preprocessing and loaded
model lifecycle. Produces `validate_vector_matrix()` and
`embed_documents_matrix()` for Task 5 while preserving the Phase 3 list API.

- [ ] **Step 1: Add RED matrix-validation tests**

Import `validate_vector_matrix` and append:

```python
def test_validate_vector_matrix_preserves_numpy_storage() -> None:
    matrix = np.asarray([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    validated = validate_vector_matrix(matrix, expected_count=2, expected_dim=2)
    assert validated is matrix
    assert validated.dtype == np.float32


def test_validate_vector_matrix_rejects_wrong_shape() -> None:
    with pytest.raises(ValueError, match="shape"):
        validate_vector_matrix(
            np.ones((2, 3), dtype=np.float32), expected_count=1, expected_dim=2
        )


@pytest.mark.parametrize(
    ("matrix", "message"),
    [
        (np.asarray([[float("nan"), 0.0]], dtype=np.float32), "non-finite"),
        (np.asarray([[2.0, 0.0]], dtype=np.float32), "unit vector"),
        (np.asarray([[1, 0]], dtype=np.int64), "floating dtype"),
    ],
)
def test_validate_vector_matrix_rejects_invalid_values(
    matrix: np.ndarray, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        validate_vector_matrix(matrix, expected_count=1, expected_dim=2)
```

- [ ] **Step 2: Run RED**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-task1-uv-cache \
uv run python -m pytest backend/tests/test_full_corpus_embedding.py -q --tb=short
```

Expected: collection error because `validate_vector_matrix` is absent.

- [ ] **Step 3: Implement exact NumPy validation and encode path**

Add beside `validate_vectors`:

```python
def validate_vector_matrix(
    vectors: np.ndarray,
    expected_count: int,
    expected_dim: int,
) -> np.ndarray:
    """Validate a dense matrix without materializing nested Python lists."""
    if not isinstance(vectors, np.ndarray):
        raise ValueError("Dense vectors must be a NumPy array")
    if vectors.shape != (expected_count, expected_dim):
        raise ValueError(
            f"Dense matrix shape {vectors.shape} != "
            f"({expected_count}, {expected_dim})"
        )
    if not np.issubdtype(vectors.dtype, np.floating):
        raise ValueError(f"Dense matrix must have floating dtype, got {vectors.dtype}")
    if not np.isfinite(vectors).all():
        raise ValueError("Dense matrix contains non-finite values")
    norms = np.linalg.norm(vectors.astype(np.float64, copy=False), axis=1)
    invalid = np.flatnonzero(~np.isclose(norms, 1.0, rtol=1e-3, atol=1e-3))
    if invalid.size:
        index = int(invalid[0])
        raise ValueError(
            f"Dense vector {index} L2 norm is {norms[index]:.6f}, "
            "expected unit vector (~1.0)"
        )
    return vectors
```

Add the method and replace only the current document-list method:

```python
def embed_documents_matrix(self, texts: Sequence[str]) -> np.ndarray:
    """Encode documents into one validated NumPy matrix for Phase 4."""
    if self._model is None:
        self.load()
    assert self._model is not None
    if not texts:
        return np.empty((0, self.spec.dimension), dtype=np.float32)
    prepared = [prepare_document(self.spec, text) for text in texts]
    raw_vectors = self._model.encode(
        prepared,
        batch_size=self.spec.batch_size,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    if not isinstance(raw_vectors, np.ndarray):
        raise ValueError("SentenceTransformer did not return a NumPy array")
    return validate_vector_matrix(raw_vectors, len(texts), self.spec.dimension)


def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
    """Preserve the bounded Phase 3 list API."""
    return self.embed_documents_matrix(texts).tolist()
```

Do not change query embedding, load/runtime identity or `close()`.

- [ ] **Step 4: Run GREEN and inspect list conversion**

Run Step 2 again; expected all tests PASS. Then:

```bash
rg -n "validate_vector_matrix|embed_documents_matrix|\.tolist" \
  backend/embedding/full_corpus.py
```

Expected: whole-matrix `.tolist()` exists only in the legacy list API; Phase 4
will call the matrix API.

---

### Task 2: Reusable sparse vocabulary lookup

**Files:** Modify `backend/embedding/sparse.py` and
`backend/tests/test_full_corpus_sparse.py`.

**Interfaces:** Consumes the closed `SparseState`; produces one checked lookup
for Task 4 while preserving exact BM25 values and serialized state bytes.

- [ ] **Step 1: Add RED equivalence tests**

Import `build_vocabulary_index` and append:

```python
def test_reusable_vocabulary_index_keeps_document_vector_exact() -> None:
    state = fit_sparse_state([
        make_chunk("c1", "bún bò huế"),
        make_chunk("c2", "cơm hến huế"),
    ])
    index = build_vocabulary_index(state)
    assert index == {term: position for position, term in enumerate(state.vocabulary)}
    assert encode_sparse_document("bún bò huế", state, index) == (
        encode_sparse_document("bún bò huế", state)
    )
```

- [ ] **Step 2: Run RED**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-task2-uv-cache \
uv run python -m pytest backend/tests/test_full_corpus_sparse.py -q --tb=short
```

Expected: import/call failure because the reusable index API is absent.

- [ ] **Step 3: Add the checked lookup and optional argument**

Import `Mapping` from `collections.abc`, then add the sole constructor for the
reused lookup:

```python
def build_vocabulary_index(state: SparseState) -> dict[str, int]:
    return {term: index for index, term in enumerate(state.vocabulary)}
```

Change `encode_sparse_document` to use this initialization, leaving its BM25
loop and sorted tuple return unchanged:

```python
def encode_sparse_document(
    text: str,
    state: SparseState,
    vocabulary_index: Mapping[str, int] | None = None,
) -> SparseVector:
    tokens = tokenize(text)
    if not tokens:
        return SparseVector(indices=(), values=())
    lookup = build_vocabulary_index(state) if vocabulary_index is None else vocabulary_index
    tf_counts = Counter(tokens)
    doc_length = len(tokens)
    matched: list[tuple[int, float]] = []
    for term, tf in tf_counts.items():
        idx = lookup.get(term)
        if idx is None:
            continue
        denominator = tf + state.k1 * (
            1.0 - state.b + state.b * doc_length / state.average_document_length
        )
        value = state.idf[idx] * (tf * (state.k1 + 1.0)) / denominator
        matched.append((idx, float(value)))
    matched.sort(key=lambda item: item[0])
    return SparseVector(
        indices=tuple(item[0] for item in matched),
        values=tuple(item[1] for item in matched),
    )
```

- [ ] **Step 4: Run GREEN and verify immutable sparse state**

Run Step 2 again; expected all tests PASS. Then:

```bash
sha256sum data/full_corpus_builds/phase_3_sparse_state.json
```

Expected:
`5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be`.

---

### Task 3: Deterministic final-only build records

**Files:** Modify `backend/ingestion/source_state.py`; create
`backend/tests/test_full_corpus_qdrant_ingestion.py`.

**Interfaces:** Consumes exact source hashes, candidate primitives and loaded
`SparseState`. Produces one deterministic record mapping/byte stream, exclusive
atomic write and full-corpus freshness comparison for Task 5/Notebook 04.

- [ ] **Step 1: Create RED record tests with real filesystem writes only**

Create the test file with these imports/helpers/tests:

```python
from pathlib import Path
import hashlib

import pytest

from backend.embedding.sparse import SparseState
from backend.ingestion.source_state import (
    make_full_corpus_build_record,
    serialize_full_corpus_build_record,
    verify_full_corpus_record_freshness,
    write_final_full_corpus_build_record,
)

CORPUS_ID = "0e5c059516cd942b151286cf597f785c65e642cacd1b0421124fe50fe574f223"
SPARSE_SHA = "5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be"


def sparse_state() -> SparseState:
    return SparseState(
        schema_version="phase_3_sparse_state:v1",
        corpus_identity=CORPUS_ID,
        document_count=8460,
        average_document_length=67.87423167848699,
        k1=1.5,
        b=0.75,
        tokenizer="backend.scoring.bm25.tokenize:v1",
        vocabulary=tuple(f"term-{index:04d}" for index in range(5662)),
        idf=tuple(1.0 for _ in range(5662)),
    )


def source_hashes() -> dict[str, str]:
    return {
        f"foods/source-{index:03d}.md": hashlib.sha256(str(index).encode()).hexdigest()
        for index in range(205)
    }


def build_record() -> dict[str, object]:
    return make_full_corpus_build_record(
        collection_name="hue_full_corpus_a_e5_small_384",
        candidate_id="e5-small-384",
        model_id="intfloat/multilingual-e5-small",
        revision="614241f622f53c4eeff9890bdc4f31cfecc418b3",
        dimension=384,
        corpus_identity=CORPUS_ID,
        sources=source_hashes(),
        sparse_state=sparse_state(),
        sparse_state_sha256=SPARSE_SHA,
    )


def test_full_corpus_record_is_exact_and_deterministic() -> None:
    record = build_record()
    assert set(record) == {
        "schema_version", "status", "collection_name", "representation",
        "corpus", "dense", "sparse", "qdrant",
    }
    assert record["status"] == "complete"
    assert serialize_full_corpus_build_record(record) == (
        serialize_full_corpus_build_record(build_record())
    )
    text = serialize_full_corpus_build_record(record).decode("utf-8")
    for forbidden in ("timestamp", "run_id", "endpoint", "absolute_path"):
        assert forbidden not in text


def test_final_record_write_is_atomic_and_exclusive(tmp_path: Path) -> None:
    path = tmp_path / "hue_full_corpus_a_e5_small_384.json"
    expected = serialize_full_corpus_build_record(build_record())
    digest = write_final_full_corpus_build_record(build_record(), path)
    assert path.read_bytes() == expected
    assert digest == hashlib.sha256(expected).hexdigest()
    assert list(tmp_path.glob("*.tmp.*")) == []
    with pytest.raises(FileExistsError, match="already exists"):
        write_final_full_corpus_build_record(build_record(), path)


def test_full_corpus_record_freshness_reports_exact_changes() -> None:
    record = build_record()
    current = source_hashes()
    assert verify_full_corpus_record_freshness(current, record) == (True, [])
    changed = dict(current)
    changed["foods/source-000.md"] = "f" * 64
    changed["travel/new.md"] = "a" * 64
    del changed["foods/source-001.md"]
    fresh, discrepancies = verify_full_corpus_record_freshness(changed, record)
    assert fresh is False
    assert any(item.startswith("Added files:") for item in discrepancies)
    assert any(item.startswith("Deleted files:") for item in discrepancies)
    assert any(item.startswith("Content changed:") for item in discrepancies)
```

- [ ] **Step 2: Run RED**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-task3-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_qdrant_ingestion.py -q --tb=short
```

Expected: import failure for the four new source-state functions.

- [ ] **Step 3: Add exact record construction and serialization**

Import `json`, `uuid`, `Mapping` and `SparseState`, preserving the module's
existing import fallback convention. Add:

```python
FULL_CORPUS_BUILD_SCHEMA = "phase_4_full_corpus_build:v1"


def make_full_corpus_build_record(
    *,
    collection_name: str,
    candidate_id: str,
    model_id: str,
    revision: str,
    dimension: int,
    corpus_identity: str,
    sources: Mapping[str, str],
    sparse_state: SparseState,
    sparse_state_sha256: str,
) -> dict[str, Any]:
    if len(sources) != 205:
        raise ValueError(f"Source count {len(sources)} != expected 205")
    if sparse_state.corpus_identity != corpus_identity:
        raise ValueError("Sparse state corpus identity mismatch")
    if sparse_state.document_count != 8460 or len(sparse_state.vocabulary) != 5662:
        raise ValueError("Sparse state count or vocabulary mismatch")
    return {
        "schema_version": FULL_CORPUS_BUILD_SCHEMA,
        "status": "complete",
        "collection_name": collection_name,
        "representation": "A",
        "corpus": {
            "identity": corpus_identity,
            "file_count": 205,
            "chunk_count": 8460,
            "sources": dict(sorted(sources.items())),
        },
        "dense": {
            "candidate_id": candidate_id,
            "model_id": model_id,
            "revision": revision,
            "dimension": dimension,
        },
        "sparse": {
            "schema_version": sparse_state.schema_version,
            "state_sha256": sparse_state_sha256,
            "vocabulary_size": len(sparse_state.vocabulary),
        },
        "qdrant": {
            "dense_vector_name": "dense",
            "sparse_vector_name": "sparse",
            "distance": "cosine",
            "point_count": 8460,
        },
    }


def serialize_full_corpus_build_record(record: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
```

- [ ] **Step 4: Add exclusive atomic write and nested freshness**

```python
def write_final_full_corpus_build_record(
    record: Mapping[str, Any], path: Path
) -> str:
    if path.exists():
        raise FileExistsError(f"Final build record already exists: {path}")
    data = serialize_full_corpus_build_record(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{uuid.uuid4().hex}")
    try:
        temporary.write_bytes(data)
        if path.exists():
            raise FileExistsError(f"Final build record already exists: {path}")
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return hashlib.sha256(data).hexdigest()


def verify_full_corpus_record_freshness(
    current_state: Mapping[str, str], record: Mapping[str, Any]
) -> tuple[bool, list[str]]:
    corpus = record.get("corpus")
    recorded = corpus.get("sources") if isinstance(corpus, dict) else None
    if not isinstance(recorded, dict):
        return False, ["Full-corpus build record missing corpus.sources mapping"]
    discrepancies: list[str] = []
    current_keys = set(current_state)
    recorded_keys = set(recorded)
    if current_keys - recorded_keys:
        discrepancies.append(f"Added files: {sorted(current_keys - recorded_keys)}")
    if recorded_keys - current_keys:
        discrepancies.append(f"Deleted files: {sorted(recorded_keys - current_keys)}")
    for path in sorted(current_keys & recorded_keys):
        if current_state[path] != recorded[path]:
            discrepancies.append(f"Content changed: {path}")
    return not discrepancies, discrepancies
```

Do not change the existing Foods/Phase 2 `verify_build_record_freshness()`.

- [ ] **Step 5: Run GREEN**

Run Step 2 again. Expected: three record tests PASS and no Qdrant/model access.

---

### Task 4: Qdrant schema and fresh-target safety

**Files:** Modify `backend/vectorstore/qdrant.py` and
`backend/tests/test_full_corpus_qdrant_ingestion.py`.

**Interfaces:** Consumes qdrant-client model objects and the existing client
factory. Produces exact schema validation, reportable target observations,
fail-closed readiness and guarded creation for Task 5. Existing Foods functions
remain unchanged.

- [ ] **Step 1: Add RED schema/target tests without a Qdrant client**

Append imports and tests:

```python
from qdrant_client import models

from backend.vectorstore.qdrant import (
    QdrantSchemaError,
    classify_full_corpus_target,
    expected_full_corpus_schema,
    require_fresh_full_corpus_target,
    validate_full_corpus_collection_params,
)


def test_full_corpus_schema_is_exact_and_has_no_idf_modifier() -> None:
    dense, sparse = expected_full_corpus_schema(768)
    assert set(dense) == {"dense"}
    assert dense["dense"].size == 768
    assert dense["dense"].distance == models.Distance.COSINE
    assert dense["dense"].on_disk is None
    assert dense["dense"].quantization_config is None
    assert set(sparse) == {"sparse"}
    assert sparse["sparse"] == models.SparseVectorParams()
    assert sparse["sparse"].modifier is None


def test_full_corpus_schema_validation_rejects_idf_and_extra_vectors() -> None:
    dense, sparse = expected_full_corpus_schema(384)
    validate_full_corpus_collection_params(
        models.CollectionParams(vectors=dense, sparse_vectors=sparse), 384
    )
    with pytest.raises(QdrantSchemaError, match="sparse"):
        validate_full_corpus_collection_params(
            models.CollectionParams(
                vectors=dense,
                sparse_vectors={
                    "sparse": models.SparseVectorParams(modifier=models.Modifier.IDF)
                },
            ),
            384,
        )
    with pytest.raises(QdrantSchemaError, match="dense vector names"):
        validate_full_corpus_collection_params(
            models.CollectionParams(
                vectors={
                    **dense,
                    "extra": models.VectorParams(size=2, distance=models.Distance.COSINE),
                },
                sparse_vectors=sparse,
            ),
            384,
        )


@pytest.mark.parametrize(
    ("exists", "count", "schema_error", "record_exists", "state", "ready"),
    [
        (False, 0, None, False, "absent", True),
        (True, 0, None, False, "empty", True),
        (True, 1, None, False, "non_empty", False),
        (True, 0, "dense dimension mismatch", False, "empty", False),
        (False, 0, None, True, "absent", False),
    ],
)
def test_fresh_target_classification_is_fail_closed(
    exists: bool, count: int, schema_error: str | None,
    record_exists: bool, state: str, ready: bool,
) -> None:
    observation = classify_full_corpus_target(
        exists=exists,
        point_count=count,
        schema_error=schema_error,
        build_record_exists=record_exists,
    )
    assert observation.state == state
    if ready:
        assert require_fresh_full_corpus_target(observation) == state
    else:
        with pytest.raises(QdrantSchemaError):
            require_fresh_full_corpus_target(observation)
```

- [ ] **Step 2: Run RED**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-task4-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_qdrant_ingestion.py -q --tb=short
```

Expected: imports fail because the full-corpus Qdrant APIs are absent.

- [ ] **Step 3: Add exact dense+sparse schema validation**

Import `dataclass`, `Path`, `Any`, `Literal`; add beside existing constants:

```python
SPARSE_VECTOR_NAME = "sparse"


def expected_full_corpus_schema(
    dimension: int,
) -> tuple[dict[str, models.VectorParams], dict[str, models.SparseVectorParams]]:
    if dimension not in {384, 768, 1024}:
        raise ValueError(f"Unsupported full-corpus dense dimension: {dimension}")
    return (
        {DENSE_VECTOR_NAME: models.VectorParams(size=dimension, distance=DISTANCE)},
        {SPARSE_VECTOR_NAME: models.SparseVectorParams()},
    )


def validate_full_corpus_collection_params(params: Any, dimension: int) -> None:
    dense = params.vectors
    if not isinstance(dense, dict) or set(dense) != {DENSE_VECTOR_NAME}:
        names = sorted(dense) if isinstance(dense, dict) else ["unnamed"]
        raise QdrantSchemaError(f"dense vector names {names} != ['dense']")
    if dense[DENSE_VECTOR_NAME].size != dimension:
        raise QdrantSchemaError(
            f"dense dimension {dense[DENSE_VECTOR_NAME].size} != {dimension}"
        )
    if dense[DENSE_VECTOR_NAME].distance != DISTANCE:
        raise QdrantSchemaError("dense distance is not cosine")
    sparse = params.sparse_vectors or {}
    if set(sparse) != {SPARSE_VECTOR_NAME}:
        raise QdrantSchemaError(f"sparse vector names {sorted(sparse)} != ['sparse']")
    if sparse[SPARSE_VECTOR_NAME].modifier is not None:
        raise QdrantSchemaError("sparse modifier must be none/default")


def validate_full_corpus_collection_info(info: Any, dimension: int) -> None:
    validate_full_corpus_collection_params(info.config.params, dimension)
    if info.payload_schema:
        raise QdrantSchemaError(
            f"full-corpus collection has payload indexes: {sorted(info.payload_schema)}"
        )
```

- [ ] **Step 4: Add observation, inspection and guarded creation**

```python
@dataclass(frozen=True)
class FullCorpusTargetObservation:
    state: Literal["absent", "empty", "non_empty"]
    point_count: int
    build_record_exists: bool
    blockers: tuple[str, ...]


def classify_full_corpus_target(
    *, exists: bool, point_count: int, schema_error: str | None,
    build_record_exists: bool,
) -> FullCorpusTargetObservation:
    if not exists and point_count != 0:
        raise ValueError("Absent target cannot have points")
    state: Literal["absent", "empty", "non_empty"]
    state = "absent" if not exists else ("empty" if point_count == 0 else "non_empty")
    blockers: list[str] = []
    if schema_error is not None:
        blockers.append(f"schema mismatch: {schema_error}")
    if state == "non_empty":
        blockers.append(f"target is non-empty: {point_count} points")
    if build_record_exists:
        blockers.append("final build record already exists")
    return FullCorpusTargetObservation(
        state=state, point_count=point_count,
        build_record_exists=build_record_exists, blockers=tuple(blockers),
    )


def inspect_full_corpus_target(
    client: QdrantClient, collection_name: str, dimension: int,
    build_record_path: Path, timeout: int,
) -> FullCorpusTargetObservation:
    exists = client.collection_exists(collection_name)
    if not exists:
        return classify_full_corpus_target(
            exists=False, point_count=0, schema_error=None,
            build_record_exists=build_record_path.exists(),
        )
    info = client.get_collection(collection_name)
    try:
        validate_full_corpus_collection_info(info, dimension)
        schema_error = None
    except QdrantSchemaError as error:
        schema_error = str(error)
    count = client.count(collection_name, exact=True, timeout=timeout).count
    return classify_full_corpus_target(
        exists=True, point_count=count, schema_error=schema_error,
        build_record_exists=build_record_path.exists(),
    )


def require_fresh_full_corpus_target(
    observation: FullCorpusTargetObservation,
) -> Literal["absent", "empty"]:
    if observation.blockers:
        raise QdrantSchemaError("; ".join(observation.blockers))
    if observation.state not in {"absent", "empty"}:
        raise QdrantSchemaError(f"target state is not fresh: {observation.state}")
    return observation.state


def create_full_corpus_collection(
    client: QdrantClient, collection_name: str, dimension: int, timeout: int
) -> None:
    dense, sparse = expected_full_corpus_schema(dimension)
    client.create_collection(
        collection_name,
        vectors_config=dense,
        sparse_vectors_config=sparse,
        timeout=timeout,
    )
```

- [ ] **Step 5: Run GREEN and inspect Foods preservation**

Run Step 2 again; expected all cases PASS. Then:

```bash
git diff -- backend/vectorstore/qdrant.py
```

Expected: existing Foods functions are unchanged and no delete/reset/recreate
function was added.

---

### Task 5: Bounded point construction and completion verification

**Files:** Modify `backend/vectorstore/points.py`,
`backend/vectorstore/upsert.py` and
`backend/tests/test_full_corpus_qdrant_ingestion.py`.

**Interfaces:** Consumes canonical `FullCorpusChunk`, one matrix slice, closed
sparse state and exact candidate metadata. Produces maximum-64 point batches,
one-batch writes and full completion verification for Task 6.

- [ ] **Step 1: Add RED point and readback tests using Qdrant value models**

Append imports/helper/tests:

```python
import numpy as np

from backend.core.schema import EvidencePart, FullCorpusChunk
from backend.embedding.sparse import build_vocabulary_index, fit_sparse_state
from backend.vectorstore.points import (
    build_full_corpus_point_batch,
    validate_full_corpus_point_inputs,
)
from backend.vectorstore.upsert import (
    compare_full_corpus_records,
    validate_sample_vectors,
)


def sample_chunk(chunk_id: str = "foods/test.md#0") -> FullCorpusChunk:
    return FullCorpusChunk(
        chunk_id=chunk_id,
        source="foods/test.md",
        title="Món Huế",
        heading_path=["Tóm tắt"],
        evidence_parts=[EvidencePart(role="body", start=0, end=7, text="Bún bò")],
        search_text="Món Huế\nTóm tắt\nBún bò",
    )


def test_full_corpus_point_batch_has_exact_vectors_payload_and_id() -> None:
    chunk = sample_chunk()
    state = fit_sparse_state([chunk])
    index = build_vocabulary_index(state)
    matrix = np.asarray([[1.0, 0.0]], dtype=np.float32)
    validate_full_corpus_point_inputs([chunk], matrix, 2, state, index)
    points = build_full_corpus_point_batch(
        [chunk], matrix, 2, state, index,
    )
    assert len(points) == 1
    point = points[0]
    assert str(point.id) == chunk.point_id
    assert set(point.vector) == {"dense", "sparse"}
    assert point.vector["dense"] == [1.0, 0.0]
    assert isinstance(point.vector["sparse"], models.SparseVector)
    assert point.payload == chunk.to_qdrant_payload()
    assert set(point.payload) == {
        "search_text", "source", "title", "heading_path", "evidence_parts"
    }


def test_full_corpus_point_batch_rejects_more_than_64() -> None:
    chunks = [sample_chunk(f"foods/test.md#{index}") for index in range(65)]
    state = fit_sparse_state(chunks)
    with pytest.raises(ValueError, match="64"):
        build_full_corpus_point_batch(
            chunks, np.tile([[1.0, 0.0]], (65, 1)), 2,
            state, build_vocabulary_index(state),
        )


def test_record_and_sample_vector_validation_is_exact() -> None:
    chunk = sample_chunk()
    record = models.Record(id=chunk.point_id, payload=chunk.to_qdrant_payload())
    seen = compare_full_corpus_records(
        [record], {chunk.point_id: chunk.to_qdrant_payload()}
    )
    assert seen == {chunk.point_id}
    vector_record = models.Record(
        id=chunk.point_id,
        vector={
            "dense": [1.0, 0.0],
            "sparse": models.SparseVector(indices=[1, 3], values=[0.5, 1.25]),
        },
    )
    validate_sample_vectors([vector_record], 2, {chunk.point_id})
    with pytest.raises(ValueError, match="payload mismatch"):
        compare_full_corpus_records(
            [models.Record(id=chunk.point_id, payload={})],
            {chunk.point_id: chunk.to_qdrant_payload()},
        )
```

- [ ] **Step 2: Run RED**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-task5-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_qdrant_ingestion.py -q --tb=short
```

Expected: imports fail for the full-corpus point/verification functions.

- [ ] **Step 3: Implement maximum-64 point construction**

Add the needed backend imports with the file's existing import convention, then:

```python
FULL_CORPUS_BATCH_SIZE = 64


def _validate_sparse_vector(chunk_id: str, sparse: SparseVector) -> None:
    if len(sparse.indices) != len(sparse.values):
        raise ValueError(f"Sparse indices/values mismatch for {chunk_id}")
    if tuple(sorted(set(sparse.indices))) != sparse.indices:
        raise ValueError(f"Sparse indices are not unique/sorted for {chunk_id}")
    if not all(math.isfinite(value) for value in sparse.values):
        raise ValueError(f"Sparse vector contains non-finite value for {chunk_id}")


def validate_full_corpus_point_inputs(
    chunks: Sequence[FullCorpusChunk],
    dense_matrix: np.ndarray,
    dimension: int,
    sparse_state: SparseState,
    vocabulary_index: Mapping[str, int],
) -> None:
    if not chunks:
        raise ValueError("Full-corpus chunks must not be empty")
    validate_vector_matrix(dense_matrix, len(chunks), dimension)
    chunk_ids = [chunk.chunk_id for chunk in chunks]
    point_ids = [chunk.point_id for chunk in chunks]
    if len(set(chunk_ids)) != len(chunk_ids):
        raise ValueError("Duplicate chunk_id in full corpus")
    if len(set(point_ids)) != len(point_ids):
        raise ValueError("Duplicate point ID in full corpus")
    required_payload = {
        "search_text", "source", "title", "heading_path", "evidence_parts"
    }
    for chunk in chunks:
        if set(chunk.to_qdrant_payload()) != required_payload:
            raise ValueError(f"Payload fields mismatch for {chunk.chunk_id}")
        sparse = encode_sparse_document(
            chunk.search_text, sparse_state, vocabulary_index
        )
        _validate_sparse_vector(chunk.chunk_id, sparse)


def build_full_corpus_point_batch(
    chunks: Sequence[FullCorpusChunk],
    dense_rows: np.ndarray,
    dimension: int,
    sparse_state: SparseState,
    vocabulary_index: Mapping[str, int],
) -> list[models.PointStruct]:
    if not chunks:
        raise ValueError("Full-corpus point batch must not be empty")
    if len(chunks) > FULL_CORPUS_BATCH_SIZE:
        raise ValueError(f"Full-corpus point batch exceeds {FULL_CORPUS_BATCH_SIZE}")
    validate_vector_matrix(dense_rows, len(chunks), dimension)
    if len({chunk.chunk_id for chunk in chunks}) != len(chunks):
        raise ValueError("Duplicate chunk_id in full-corpus point batch")
    points: list[models.PointStruct] = []
    for chunk, dense_row in zip(chunks, dense_rows, strict=True):
        sparse = encode_sparse_document(
            chunk.search_text, sparse_state, vocabulary_index
        )
        _validate_sparse_vector(chunk.chunk_id, sparse)
        payload = chunk.to_qdrant_payload()
        if set(payload) != {
            "search_text", "source", "title", "heading_path", "evidence_parts"
        }:
            raise ValueError(f"Payload fields mismatch for {chunk.chunk_id}")
        points.append(models.PointStruct(
            id=chunk.point_id,
            vector={
                "dense": dense_row.tolist(),
                "sparse": models.SparseVector(
                    indices=list(sparse.indices), values=list(sparse.values)
                ),
            },
            payload=payload,
        ))
    return points
```

Required imports are `Mapping`, `Sequence`, `numpy as np`, `FullCorpusChunk`,
`SparseState`, `encode_sparse_document`, and `validate_vector_matrix`. Keep the
existing Foods `build_points()` unchanged.

- [ ] **Step 4: Implement one-batch write and pure record validators**

Add to `backend/vectorstore/upsert.py`:

```python
FULL_CORPUS_SCROLL_LIMIT = 1000
FULL_CORPUS_BATCH_SIZE = 64


def upsert_full_corpus_batch(
    client: QdrantClient,
    collection_name: str,
    points: Sequence[models.PointStruct],
    timeout: int,
) -> int:
    if not 1 <= len(points) <= FULL_CORPUS_BATCH_SIZE:
        raise ValueError("Full-corpus upsert batch size must be between 1 and 64")
    client.upsert(
        collection_name, points=points, wait=True, timeout=timeout
    )
    return len(points)


def compare_full_corpus_records(
    records: Sequence[models.Record],
    expected_payloads: Mapping[str, Mapping[str, Any]],
) -> set[str]:
    seen: set[str] = set()
    for record in records:
        point_id = str(record.id)
        if point_id in seen:
            raise ValueError(f"Duplicate point returned by Qdrant: {point_id}")
        expected = expected_payloads.get(point_id)
        if expected is None:
            raise ValueError(f"Foreign point returned by Qdrant: {point_id}")
        if record.payload != expected:
            raise ValueError(f"Full-corpus payload mismatch for point {point_id}")
        seen.add(point_id)
    return seen


def validate_sample_vectors(
    records: Sequence[models.Record],
    expected_dimension: int,
    expected_ids: set[str],
) -> None:
    if {str(record.id) for record in records} != expected_ids:
        raise ValueError("Sample vector IDs do not match the exact expected set")
    for record in records:
        vectors = record.vector
        if not isinstance(vectors, dict) or set(vectors) != {"dense", "sparse"}:
            raise ValueError(f"Sample vector names mismatch for point {record.id}")
        dense = np.asarray(vectors["dense"], dtype=np.float32).reshape(1, -1)
        validate_vector_matrix(dense, 1, expected_dimension)
        sparse = vectors["sparse"]
        if not isinstance(sparse, models.SparseVector):
            raise ValueError(f"Sparse sample has wrong type for point {record.id}")
        if len(sparse.indices) != len(sparse.values):
            raise ValueError(f"Sparse sample length mismatch for point {record.id}")
        if sorted(set(sparse.indices)) != sparse.indices:
            raise ValueError(f"Sparse sample indices invalid for point {record.id}")
        if not all(math.isfinite(value) for value in sparse.values):
            raise ValueError(f"Sparse sample values invalid for point {record.id}")
```

Import `math`, `Any`, `Mapping`, `Sequence`, `numpy as np`, qdrant `models`,
`QdrantClient` and `validate_vector_matrix`. Do not alter existing Foods upsert.

- [ ] **Step 5: Add real-client completion verification without test doubles**

```python
def verify_full_corpus_collection(
    client: QdrantClient,
    collection_name: str,
    dimension: int,
    chunks: Sequence[FullCorpusChunk],
    sample_chunk_ids: Sequence[str],
    timeout: int,
) -> dict[str, int]:
    validate_full_corpus_collection_info(
        client.get_collection(collection_name), dimension
    )
    actual_count = client.count(collection_name, exact=True, timeout=timeout).count
    if actual_count != len(chunks):
        raise ValueError(
            f"Collection {collection_name} point count {actual_count} != {len(chunks)}"
        )
    expected_payloads = {
        chunk.point_id: chunk.to_qdrant_payload() for chunk in chunks
    }
    seen: set[str] = set()
    offset = None
    while True:
        records, next_offset = client.scroll(
            collection_name,
            limit=FULL_CORPUS_SCROLL_LIMIT,
            offset=offset,
            with_payload=True,
            with_vectors=False,
            timeout=timeout,
        )
        page_ids = compare_full_corpus_records(records, expected_payloads)
        duplicate = seen & page_ids
        if duplicate:
            raise ValueError(f"Duplicate point across scroll pages: {sorted(duplicate)}")
        seen.update(page_ids)
        if next_offset is None:
            break
        offset = next_offset
    if seen != set(expected_payloads):
        missing = sorted(set(expected_payloads) - seen)
        raise ValueError(f"Full-corpus point ID set mismatch; missing={missing[:10]}")
    chunk_by_id = {chunk.chunk_id: chunk for chunk in chunks}
    if any(chunk_id not in chunk_by_id for chunk_id in sample_chunk_ids):
        raise ValueError("Phase 3 sample chunk ID is absent from fresh corpus")
    sample_point_ids = {chunk_by_id[chunk_id].point_id for chunk_id in sample_chunk_ids}
    sample_records = client.retrieve(
        collection_name,
        ids=sorted(sample_point_ids),
        with_payload=False,
        with_vectors=["dense", "sparse"],
        timeout=timeout,
    )
    validate_sample_vectors(sample_records, dimension, sample_point_ids)
    return {
        "point_count": actual_count,
        "payloads_verified": len(seen),
        "sample_vectors_verified": len(sample_records),
    }
```

Import `FullCorpusChunk` and `validate_full_corpus_collection_info`.

- [ ] **Step 6: Run GREEN**

Run Step 2 again. Expected: all pure Task 3–5 cases PASS without Qdrant access.

---

### Task 6: Static registry, fresh preparation, CLI and read-only preflight

**Files:** Create `backend/ingestion/full_corpus_pipeline.py`; modify
`backend/tests/test_full_corpus_qdrant_ingestion.py`; create
`reports/artifacts/full_corpus_phase_4_qdrant_preflight_2026_09_12.json` only
after deterministic tests pass.

**Interfaces:** Consumes Tasks 1–5 and existing settings/client/chunker/model
contracts. Produces the only Phase 4 CLI, fresh prepared input, one-candidate
build path and a four-target read-only preflight package. No arbitrary model or
collection argument exists.

- [ ] **Step 1: Add RED registry tests**

Append:

```python
from backend.ingestion.full_corpus_pipeline import (
    FULL_CORPUS_CANDIDATES,
    candidate_by_id,
)


def test_phase4_candidate_registry_is_exact_ordered_and_isolated() -> None:
    assert [
        (item.candidate_id, item.collection_name, item.dense_spec.dimension)
        for item in FULL_CORPUS_CANDIDATES
    ] == [
        ("e5-small-384", "hue_full_corpus_a_e5_small_384", 384),
        ("e5-base-768", "hue_full_corpus_a_e5_base_768", 768),
        ("huydang-dek21-768", "hue_full_corpus_a_huydang_dek21_768", 768),
        ("qwen3-embedding-0.6b-1024", "hue_full_corpus_a_qwen3_06b_1024", 1024),
    ]
    assert not {
        "hue_foods_e5_small_384", "hue_foods_e5_small_384_dense"
    } & {item.collection_name for item in FULL_CORPUS_CANDIDATES}
    assert candidate_by_id("e5-small-384") is FULL_CORPUS_CANDIDATES[0]
    with pytest.raises(ValueError, match="Unknown Phase 4 candidate"):
        candidate_by_id("arbitrary-model")
```

- [ ] **Step 2: Run RED**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-task6-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_qdrant_ingestion.py -q --tb=short
```

Expected: import failure because the pipeline module is absent.

- [ ] **Step 3: Create constants, registry and fresh input loader**

Create the module with this exact import surface:

```python
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import importlib.metadata
import json
import logging
from pathlib import Path
import shutil
from typing import Any
import uuid

import numpy as np
import torch

from backend.core.schema import FullCorpusChunk
from backend.core.settings_loader import load_settings
from backend.embedding.full_corpus import (
    DENSE_MODEL_SPECS,
    DenseModelSpec,
    FullCorpusDenseRunner,
    resolve_snapshot,
)
from backend.embedding.sparse import (
    SparseState,
    build_vocabulary_index,
    compute_corpus_identity,
    load_sparse_state,
)
from backend.ingestion.chunking.full_corpus_chunker import chunk_full_corpus
from backend.ingestion.source_state import (
    compute_corpus_state,
    discover_full_corpus_files,
    make_full_corpus_build_record,
    write_final_full_corpus_build_record,
)
from backend.vectorstore.points import (
    build_full_corpus_point_batch,
    validate_full_corpus_point_inputs,
)
from backend.vectorstore.qdrant import (
    client_from_settings,
    create_full_corpus_collection,
    inspect_full_corpus_target,
    require_fresh_full_corpus_target,
)
from backend.vectorstore.upsert import (
    upsert_full_corpus_batch,
    verify_full_corpus_collection,
)
```

Then define:

```python
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SPARSE_STATE_PATH = REPOSITORY_ROOT / "data/full_corpus_builds/phase_3_sparse_state.json"
PHASE3_EVIDENCE_PATH = REPOSITORY_ROOT / "reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json"
PREFLIGHT_OUTPUT_PATH = REPOSITORY_ROOT / "reports/artifacts/full_corpus_phase_4_qdrant_preflight_2026_09_12.json"
BUILD_RECORD_ROOT = REPOSITORY_ROOT / "data/full_corpus_builds"
EXPECTED_FILE_COUNT = 205
EXPECTED_CHUNK_COUNT = 8460
EXPECTED_CORPUS_IDENTITY = "0e5c059516cd942b151286cf597f785c65e642cacd1b0421124fe50fe574f223"
EXPECTED_SPARSE_SHA256 = "5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be"
QDRANT_TIMEOUT = 30


@dataclass(frozen=True)
class FullCorpusCandidate:
    candidate_id: str
    collection_name: str
    dense_spec: DenseModelSpec

_COLLECTION_BY_CANDIDATE = {
    "e5-small-384": "hue_full_corpus_a_e5_small_384",
    "e5-base-768": "hue_full_corpus_a_e5_base_768",
    "huydang-dek21-768": "hue_full_corpus_a_huydang_dek21_768",
    "qwen3-embedding-0.6b-1024": "hue_full_corpus_a_qwen3_06b_1024",
}
if set(_COLLECTION_BY_CANDIDATE) != {spec.key for spec in DENSE_MODEL_SPECS}:
    raise RuntimeError("Phase 4 collection mapping does not match Phase 3 dense specs")
FULL_CORPUS_CANDIDATES = tuple(
    FullCorpusCandidate(spec.key, _COLLECTION_BY_CANDIDATE[spec.key], spec)
    for spec in DENSE_MODEL_SPECS
)


@dataclass(frozen=True)
class PreparedFullCorpus:
    chunks: list[FullCorpusChunk]
    sources: dict[str, str]
    source_state_sha256: str
    sparse_state: SparseState
    sparse_state_sha256: str
    sample_chunk_ids: tuple[str, ...]


def candidate_by_id(candidate_id: str) -> FullCorpusCandidate:
    for candidate in FULL_CORPUS_CANDIDATES:
        if candidate.candidate_id == candidate_id:
            return candidate
    raise ValueError(f"Unknown Phase 4 candidate: {candidate_id}")


def build_record_path(candidate: FullCorpusCandidate) -> Path:
    return BUILD_RECORD_ROOT / f"{candidate.collection_name}.json"


def _phase4_settings() -> dict[str, Any]:
    settings = load_settings()
    database = settings.get("vector_database", {})
    if database.get("url") != "http://localhost:6333":
        raise ValueError("Phase 4 requires the pinned local Hue Qdrant URL")
    if database.get("timeout") != QDRANT_TIMEOUT:
        raise ValueError("Phase 4 Qdrant timeout must remain 30 seconds")
    return settings
```

Implement fresh validation exactly:

```python
def prepare_full_corpus_input() -> PreparedFullCorpus:
    settings = _phase4_settings()
    root, relative_paths = discover_full_corpus_files(settings)
    sources = compute_corpus_state(root, relative_paths)
    source_state_bytes = json.dumps(
        sources, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    source_state_sha = hashlib.sha256(source_state_bytes).hexdigest()
    chunks, errors = chunk_full_corpus(settings)
    if errors:
        raise ValueError(f"Fresh full-corpus chunking failed: {errors}")
    if len(relative_paths) != EXPECTED_FILE_COUNT:
        raise ValueError(f"File count {len(relative_paths)} != {EXPECTED_FILE_COUNT}")
    if len(chunks) != EXPECTED_CHUNK_COUNT:
        raise ValueError(f"Chunk count {len(chunks)} != {EXPECTED_CHUNK_COUNT}")
    corpus_identity = compute_corpus_identity(chunks)
    if corpus_identity != EXPECTED_CORPUS_IDENTITY:
        raise ValueError(f"Corpus identity mismatch: {corpus_identity}")
    sparse_bytes = SPARSE_STATE_PATH.read_bytes()
    sparse_sha = hashlib.sha256(sparse_bytes).hexdigest()
    if sparse_sha != EXPECTED_SPARSE_SHA256:
        raise ValueError(f"Sparse state SHA-256 mismatch: {sparse_sha}")
    sparse_state = load_sparse_state(SPARSE_STATE_PATH)
    if (
        sparse_state.corpus_identity != corpus_identity
        or sparse_state.document_count != EXPECTED_CHUNK_COUNT
        or len(sparse_state.vocabulary) != 5662
        or sparse_state.k1 != 1.5
        or sparse_state.b != 0.75
    ):
        raise ValueError("Sparse state identity/shape/constants mismatch")
    evidence = json.loads(PHASE3_EVIDENCE_PATH.read_text(encoding="utf-8"))
    if evidence.get("status") != "PASS":
        raise ValueError("Phase 3 evidence status is not PASS")
    if evidence.get("corpus", {}).get("corpus_identity") != corpus_identity:
        raise ValueError("Phase 3 evidence corpus identity mismatch")
    if evidence.get("sparse", {}).get("sha256") != sparse_sha:
        raise ValueError("Phase 3 evidence sparse SHA-256 mismatch")
    sample_ids = tuple(item["chunk_id"] for item in evidence.get("sample", []))
    if len(sample_ids) != 12 or len(set(sample_ids)) != 12:
        raise ValueError("Phase 3 deterministic sample must contain 12 unique IDs")
    chunk_ids = {chunk.chunk_id for chunk in chunks}
    if any(sample_id not in chunk_ids for sample_id in sample_ids):
        raise ValueError("Phase 3 sample ID is absent from fresh chunks")
    for candidate in FULL_CORPUS_CANDIDATES:
        model = evidence.get("models", {}).get(candidate.candidate_id, {})
        spec = candidate.dense_spec
        observed = (
            model.get("model_id"), model.get("revision"), model.get("dimension"),
            model.get("max_tokens"), model.get("input_contract"),
            model.get("device"), model.get("dtype"), model.get("batch_size"),
        )
        expected = (
            spec.model_id, spec.revision, spec.dimension,
            spec.max_tokens, spec.input_contract,
            spec.device, spec.dtype, spec.batch_size,
        )
        if observed != expected:
            raise ValueError(f"Phase 3 model evidence mismatch for {spec.key}")
    return PreparedFullCorpus(
        chunks=chunks,
        sources=sources,
        source_state_sha256=source_state_sha,
        sparse_state=sparse_state,
        sparse_state_sha256=sparse_sha,
        sample_chunk_ids=sample_ids,
    )
```

- [ ] **Step 4: Implement safe resource inspection and four-target preflight**

```python
def _linux_memory_bytes() -> dict[str, int]:
    values: dict[str, int] = {}
    for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
        key, raw = line.split(":", 1)
        if key in {"MemTotal", "MemAvailable", "SwapTotal", "SwapFree"}:
            values[key] = int(raw.strip().split()[0]) * 1024
    return values


def _resource_evidence() -> dict[str, Any]:
    disk = shutil.disk_usage(REPOSITORY_ROOT)
    gpu: dict[str, Any] = {
        "cuda_available": torch.cuda.is_available(),
        "torch_version": torch.__version__,
        "torch_cuda_version": torch.version.cuda,
    }
    if torch.cuda.is_available():
        gpu.update({
            "device_name": torch.cuda.get_device_name(0),
            "total_vram_bytes": torch.cuda.get_device_properties(0).total_memory,
        })
    return {
        "memory": _linux_memory_bytes(),
        "disk": {"total_bytes": disk.total, "free_bytes": disk.free},
        "gpu": gpu,
    }


def run_read_only_preflight() -> tuple[dict[str, Any], int]:
    prepared = prepare_full_corpus_input()
    settings = _phase4_settings()
    client = client_from_settings(settings)
    try:
        version = client.info()
        targets = []
        for candidate in FULL_CORPUS_CANDIDATES:
            observation = inspect_full_corpus_target(
                client, candidate.collection_name, candidate.dense_spec.dimension,
                build_record_path(candidate), QDRANT_TIMEOUT,
            )
            targets.append({
                "candidate_id": candidate.candidate_id,
                "collection_name": candidate.collection_name,
                "dimension": candidate.dense_spec.dimension,
                "state": observation.state,
                "point_count": observation.point_count,
                "build_record_exists": observation.build_record_exists,
                "blockers": list(observation.blockers),
            })
    finally:
        client.close()
    ready = all(not target["blockers"] for target in targets)
    evidence = {
        "schema_version": "phase_4_qdrant_preflight:v1",
        "status": "READY" if ready else "BLOCKED",
        "corpus": {
            "file_count": len(prepared.sources),
            "chunk_count": len(prepared.chunks),
            "identity": EXPECTED_CORPUS_IDENTITY,
            "source_state_sha256": prepared.source_state_sha256,
        },
        "sparse": {
            "state_sha256": prepared.sparse_state_sha256,
            "vocabulary_size": len(prepared.sparse_state.vocabulary),
        },
        "qdrant": {
            "server_version": version.version,
            "client_version": importlib.metadata.version("qdrant-client"),
        },
        "resources": _resource_evidence(),
        "targets": targets,
        "build_commands": [
            f"python -m backend.ingestion.full_corpus_pipeline build --candidate {item.candidate_id}"
            for item in FULL_CORPUS_CANDIDATES
        ],
    }
    return evidence, 0 if ready else 2
```

This function calls only `info`, `collection_exists`, `get_collection` and
`count` for the four exact targets; it never lists or accesses Foods collections.

- [ ] **Step 5: Implement one-candidate build orchestration**

```python
def build_candidate(candidate_id: str) -> dict[str, Any]:
    candidate = candidate_by_id(candidate_id)
    prepared = prepare_full_corpus_input()
    approved_preflight = json.loads(
        PREFLIGHT_OUTPUT_PATH.read_text(encoding="utf-8")
    )
    if approved_preflight.get("status") != "READY":
        raise ValueError("Initial Phase 4 preflight status is not READY")
    preflight_corpus = approved_preflight.get("corpus", {})
    if (
        preflight_corpus.get("identity") != EXPECTED_CORPUS_IDENTITY
        or preflight_corpus.get("source_state_sha256")
        != prepared.source_state_sha256
        or approved_preflight.get("sparse", {}).get("state_sha256")
        != prepared.sparse_state_sha256
    ):
        raise ValueError("Fresh corpus/sparse state differs from approved preflight")
    settings = _phase4_settings()
    client = client_from_settings(settings)
    record_path = build_record_path(candidate)
    first = inspect_full_corpus_target(
        client, candidate.collection_name, candidate.dense_spec.dimension,
        record_path, QDRANT_TIMEOUT,
    )
    require_fresh_full_corpus_target(first)
    runner: FullCorpusDenseRunner | None = None
    completed = 0
    resources_before = _resource_evidence()
    try:
        snapshot = resolve_snapshot(candidate.dense_spec, allow_download=False)
        runner = FullCorpusDenseRunner(candidate.dense_spec, snapshot)
        runner.load()
        runtime = runner.observed_runtime_state()
        if candidate.dense_spec.device == "cuda":
            torch.cuda.reset_peak_memory_stats()
        texts = [chunk.search_text for chunk in prepared.chunks]
        dense = runner.embed_documents_matrix(texts)
        resources_after_encode = _resource_evidence()
        if candidate.dense_spec.device == "cuda":
            resources_after_encode["gpu"]["peak_allocated_bytes"] = (
                torch.cuda.max_memory_allocated()
            )
        vocabulary_index = build_vocabulary_index(prepared.sparse_state)
        validate_full_corpus_point_inputs(
            prepared.chunks, dense, candidate.dense_spec.dimension,
            prepared.sparse_state, vocabulary_index,
        )
        root, relative_paths = discover_full_corpus_files(settings)
        if compute_corpus_state(root, relative_paths) != prepared.sources:
            raise ValueError("Canonical source hashes changed during dense encoding")
        second = inspect_full_corpus_target(
            client, candidate.collection_name, candidate.dense_spec.dimension,
            record_path, QDRANT_TIMEOUT,
        )
        require_fresh_full_corpus_target(second)
        if second != first:
            raise ValueError("Target/build-record state changed after preflight")
        if second.state == "absent":
            create_full_corpus_collection(
                client, candidate.collection_name,
                candidate.dense_spec.dimension, QDRANT_TIMEOUT,
            )
            created = inspect_full_corpus_target(
                client, candidate.collection_name, candidate.dense_spec.dimension,
                record_path, QDRANT_TIMEOUT,
            )
            require_fresh_full_corpus_target(created)
            if created.state != "empty":
                raise ValueError("New full-corpus target is not schema-valid and empty")
        for start in range(0, len(prepared.chunks), 64):
            stop = min(start + 64, len(prepared.chunks))
            points = build_full_corpus_point_batch(
                prepared.chunks[start:stop], dense[start:stop],
                candidate.dense_spec.dimension, prepared.sparse_state,
                vocabulary_index,
            )
            try:
                completed += upsert_full_corpus_batch(
                    client, candidate.collection_name, points, QDRANT_TIMEOUT
                )
            except Exception:
                observed = client.count(
                    candidate.collection_name, exact=True, timeout=QDRANT_TIMEOUT
                ).count
                logging.exception(
                    "Phase 4 upsert failed candidate=%s completed=%d observed=%d",
                    candidate.candidate_id, completed, observed,
                )
                raise
        verification = verify_full_corpus_collection(
            client, candidate.collection_name, candidate.dense_spec.dimension,
            prepared.chunks, prepared.sample_chunk_ids, QDRANT_TIMEOUT,
        )
        record = make_full_corpus_build_record(
            collection_name=candidate.collection_name,
            candidate_id=candidate.candidate_id,
            model_id=candidate.dense_spec.model_id,
            revision=candidate.dense_spec.revision,
            dimension=candidate.dense_spec.dimension,
            corpus_identity=EXPECTED_CORPUS_IDENTITY,
            sources=prepared.sources,
            sparse_state=prepared.sparse_state,
            sparse_state_sha256=prepared.sparse_state_sha256,
        )
        record_sha = write_final_full_corpus_build_record(record, record_path)
        norms = np.linalg.norm(dense.astype(np.float64, copy=False), axis=1)
        return {
            "candidate_id": candidate.candidate_id,
            "collection_name": candidate.collection_name,
            "model_id": candidate.dense_spec.model_id,
            "revision": candidate.dense_spec.revision,
            "runtime": runtime,
            "matrix_shape": list(dense.shape),
            "matrix_dtype": str(dense.dtype),
            "norm_min": float(norms.min()),
            "norm_max": float(norms.max()),
            "corpus_identity": EXPECTED_CORPUS_IDENTITY,
            "source_state_sha256": prepared.source_state_sha256,
            "sparse_state_sha256": prepared.sparse_state_sha256,
            "resources_before": resources_before,
            "resources_after_encode": resources_after_encode,
            "completed_upserts": completed,
            "verification": verification,
            "build_record_path": str(record_path.relative_to(REPOSITORY_ROOT)),
            "build_record_sha256": record_sha,
        }
    finally:
        if runner is not None:
            runner.close()
        client.close()
```

Do not wrap provider/model/Qdrant failures into success. The Implementer runs
one candidate command at a time in registry order and stops after any nonzero
exit; there is no `build-all` command.

- [ ] **Step 6: Implement CLI and atomic preflight artifact output**

```python
def _write_preflight_output(evidence: dict[str, Any], output: Path) -> None:
    data = (
        json.dumps(evidence, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f"{output.name}.tmp.{uuid.uuid4().hex}")
    try:
        temporary.write_bytes(data)
        temporary.replace(output)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description="Full-corpus Phase 4 ingestion")
    subparsers = parser.add_subparsers(dest="command", required=True)
    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--output", type=Path)
    build = subparsers.add_parser("build")
    build.add_argument(
        "--candidate",
        required=True,
        choices=[item.candidate_id for item in FULL_CORPUS_CANDIDATES],
    )
    args = parser.parse_args()
    if args.command == "preflight":
        evidence, exit_code = run_read_only_preflight()
        if args.output is not None:
            _write_preflight_output(evidence, args.output.resolve())
        print(json.dumps(evidence, ensure_ascii=False, sort_keys=True, indent=2))
        raise SystemExit(exit_code)
    summary = build_candidate(args.candidate)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
```

- [ ] **Step 7: Run deterministic GREEN checks before any Qdrant access**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-task6-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_qdrant_ingestion.py \
  -q --tb=short
git diff --check
```

Expected: all focused tests PASS, whitespace check empty, no model/Qdrant call.

- [ ] **Step 8: Run the approved read-only preflight and stop**

This step is allowed only after User approval of this Plan/Review Contract. Run:

```bash
docker compose ps
docker compose config --images
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-preflight-uv-cache \
uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline \
  preflight \
  --output reports/artifacts/full_corpus_phase_4_qdrant_preflight_2026_09_12.json
```

Expected: Compose resolves the pinned
`qdrant/qdrant@sha256:0bd98fa7977f1e75694779359ca4e212822e5a71334e28421182f72f209d5286`;
Qdrant v1.18.3 is available; artifact status `READY`; all four exact
targets are `absent` or schema-valid `empty`, point count `0`, record absent,
blockers empty; corpus/sparse/resources/commands populated. If not, mark Task 7
blocked and do not load any dense model or mutate Qdrant.

Present the exact artifact and commands to Reviewer/User. Stop for one explicit
live-write approval naming all four target collections. Plan approval alone is
not live-write approval.

---

### Task 7: Sequential live full-corpus builds under the separate gate

**Files/state:** Generate four ignored records under
`data/full_corpus_builds/`; create/write only the four exact Qdrant collections.
No source file is edited in this task.

**Interfaces:** Consumes Task 6 `READY` artifact and verbatim User authority.
Produces real integration evidence and four complete targets/records. Any first
failure terminates this task with Phase 4 incomplete.

- [ ] **Step 1: Verify the live approval and unchanged preflight inputs**

The approval must explicitly name:

```text
hue_full_corpus_a_e5_small_384
hue_full_corpus_a_e5_base_768
hue_full_corpus_a_huydang_dek21_768
hue_full_corpus_a_qwen3_06b_1024
```

Record the exact approval text. Re-run deterministic tests from Task 6 Step 7
and compare source/sparse/Phase 3 artifact hashes to the preflight artifact.
Expected: unchanged and PASS. If anything changed, rerun read-only preflight and
return to the live approval gate; do not infer authority for new state.

- [ ] **Step 2: Build E5-small and verify its record**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-live-uv-cache \
uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline \
  build --candidate e5-small-384
sha256sum data/full_corpus_builds/hue_full_corpus_a_e5_small_384.json
```

Expected: matrix `[8460, 384]`; completed upserts `8460`; exact schema/count;
`8460` payloads and `12` sampled vectors verified; final record status complete.
If the command fails, preserve the target, do not write/fabricate a record, stop
and report exact completed/observed counts.

- [ ] **Step 3: Build E5-base only if Step 2 passed**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-live-uv-cache \
uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline \
  build --candidate e5-base-768
sha256sum data/full_corpus_builds/hue_full_corpus_a_e5_base_768.json
```

Expected: matrix `[8460, 768]` and the same exact `8460/8460/12` completion
counts. On failure, stop without running HuyDang/Qwen.

- [ ] **Step 4: Build HuyDang only if Step 3 passed**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-live-uv-cache \
uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline \
  build --candidate huydang-dek21-768
sha256sum data/full_corpus_builds/hue_full_corpus_a_huydang_dek21_768.json
```

Expected: CPU FP32/PyVi batch 8, matrix `[8460, 768]`, and exact
`8460/8460/12` completion counts. On failure, stop without running Qwen.

- [ ] **Step 5: Build Qwen only if Step 4 passed**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-live-uv-cache \
uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline \
  build --candidate qwen3-embedding-0.6b-1024
sha256sum data/full_corpus_builds/hue_full_corpus_a_qwen3_06b_1024.json
```

Expected: CUDA FP16/eager/batch 1, native matrix `[8460, 1024]`, finite unit
norms within the locked `1e-3` relative/absolute tolerance, and exact
`8460/8460/12` completion counts. OOM/CUDA/provider failure is `BLOCKED` or
`FAIL`, never CPU fallback or optional success.

- [ ] **Step 6: Cross-check four records and completed-target guards**

```bash
jq '{status,collection_name,representation,corpus,dense,sparse,qdrant}' \
  data/full_corpus_builds/hue_full_corpus_a_e5_small_384.json
jq '{status,collection_name,representation,corpus,dense,sparse,qdrant}' \
  data/full_corpus_builds/hue_full_corpus_a_e5_base_768.json
jq '{status,collection_name,representation,corpus,dense,sparse,qdrant}' \
  data/full_corpus_builds/hue_full_corpus_a_huydang_dek21_768.json
jq '{status,collection_name,representation,corpus,dense,sparse,qdrant}' \
  data/full_corpus_builds/hue_full_corpus_a_qwen3_06b_1024.json
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-postbuild-uv-cache \
uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline preflight
```

Expected: all records use the same exact corpus/sparse identities, identical
205-entry source-hash mappings and `8460` points; model/revision/dimension and
collection differ only according to the registry. Final preflight exits `2`
with status `BLOCKED`, and each target entry
reports both `non_empty: 8460` and final-record-present blockers. This expected
nonzero result proves rerun stops before model load/write; it is not a Phase
failure. Do not overwrite the initial `READY` artifact.

---

### Task 8: Read-only Notebook 04 and implementation evidence

**Files:** Modify `notebooks/04_qdrant_ingestion.ipynb`; create
`reports/full_corpus_phase_4_qdrant_ingestion_implementation_2026_09_12.md`.

**Interfaces:** Consumes four completed records/collections. Produces a learning
inspector and final Implementer evidence. It does not mutate data or claim review.

- [ ] **Step 1: Replace Notebook 04 with the exact read-only narrative**

Use the existing notebook metadata/kernel and replace cells with these sections:

```text
# 04 — Full-corpus Qdrant ingestion inspection

Phase 4 stores the same 8,460 Representation A chunks in four isolated
candidate collections. Each point has named dense and sparse vectors. This
notebook reads only the fixed candidate registry, final records and Qdrant
metadata/points; it never loads a dense model or creates, writes, resets or
deletes a collection.

## Fresh local identities and final records
## Exact live schema/count/payload/sample inspection
## Phase boundary

Dense and native hybrid retrieval belong to Phase 5. Quality comparison,
winner selection and cutover belong to Phase 8.
```

The first code cell must add the repository root, not `backend/`, to `sys.path`:

```python
import sys
from pathlib import Path

for base in (Path.cwd(), *Path.cwd().parents):
    if (base / "backend").is_dir():
        sys.path.insert(0, str(base))
        break
else:
    raise RuntimeError("Không tìm thấy repository root chứa backend/.")
print("repository root resolved")
```

Use this exact inspection path in the second code cell:

```python
import json

from backend.core.settings_loader import load_settings
from backend.ingestion.full_corpus_pipeline import (
    FULL_CORPUS_CANDIDATES,
    build_record_path,
    prepare_full_corpus_input,
)
from backend.ingestion.source_state import verify_full_corpus_record_freshness
from backend.vectorstore.qdrant import (
    client_from_settings,
    validate_full_corpus_collection_info,
)
from backend.vectorstore.upsert import verify_full_corpus_collection

prepared = prepare_full_corpus_input()
settings = load_settings()
client = client_from_settings(settings)
try:
    for candidate in FULL_CORPUS_CANDIDATES:
        record_path = build_record_path(candidate)
        record = json.loads(record_path.read_text(encoding="utf-8"))
        fresh, discrepancies = verify_full_corpus_record_freshness(
            prepared.sources, record
        )
        if not fresh:
            raise RuntimeError(
                f"Stale build record for {candidate.collection_name}: {discrepancies}"
            )
        info = client.get_collection(candidate.collection_name)
        validate_full_corpus_collection_info(info, candidate.dense_spec.dimension)
        verification = verify_full_corpus_collection(
            client,
            candidate.collection_name,
            candidate.dense_spec.dimension,
            prepared.chunks,
            prepared.sample_chunk_ids,
            30,
        )
        records, _ = client.scroll(
            candidate.collection_name,
            limit=2,
            with_payload=True,
            with_vectors=False,
            timeout=30,
        )
        projections = []
        for item in records:
            payload = item.payload or {}
            projections.append({
                "id": str(item.id),
                "payload_fields": sorted(payload),
                "search_text_length": len(payload.get("search_text", "")),
                "evidence_part_count": len(payload.get("evidence_parts", [])),
            })
        print({
            "candidate": candidate.candidate_id,
            "collection": candidate.collection_name,
            "record_status": record["status"],
            "verification": verification,
            "payload_projection": projections,
        })
finally:
    client.close()
```

No cell imports/calls `FullCorpusDenseRunner`, `build_candidate`,
`create_collection`, `upsert`, `delete_collection` or `reset_collection`.

- [ ] **Step 2: Clear and statically validate the canonical notebook**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase4-notebook-uv-cache \
uv run jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace \
  notebooks/04_qdrant_ingestion.ipynb
UV_CACHE_DIR=/tmp/hue-rag-phase4-notebook-uv-cache uv run python -c \
'import json; from pathlib import Path; p=Path("notebooks/04_qdrant_ingestion.ipynb"); n=json.loads(p.read_text()); assert all(c.get("execution_count") is None and not c.get("outputs", []) for c in n["cells"] if c["cell_type"]=="code"); code="\n".join("".join(c["source"]) for c in n["cells"] if c["cell_type"]=="code"); assert all(x not in code for x in ("build_candidate", "create_collection", ".upsert(", "delete_collection", "reset_collection", "FullCorpusDenseRunner")); print("notebook read-only and clean")'
```

Expected: `notebook read-only and clean`.

- [ ] **Step 3: Run a temporary Notebook 04 copy read-only**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase4-notebook-uv-cache \
uv run --env-file .env jupyter nbconvert --execute --to notebook \
  notebooks/04_qdrant_ingestion.ipynb \
  --output /tmp/04_qdrant_ingestion-phase4-live.ipynb \
  --ExecutePreprocessor.timeout=1800
```

Expected: all four records fresh, schemas/counts/payloads/sample vectors pass;
only safe payload field names/lengths are printed. Canonical notebook remains
clean. Do not query Foods.

- [ ] **Step 4: Run final deterministic checks and immutable audits**

Run the exact Review Contract pytest command and `git diff --check`. Recompute
before/after hashes for all immutable files and source-state mapping. Expected:
focused tests PASS; no whitespace error; no immutable deviation. Do not run the
old live `backend/tests/test_ingestion_pipeline.py`, because it creates/deletes
test collections and is explicitly outside this Phase 4 evidence design.

- [ ] **Step 5: Write the implementation report and hand back to Reviewer**

The report must contain these exact sections:

```text
# Full-corpus Phase 4 Qdrant Ingestion — Implementation Report
## Authority and repository state
## Changed paths and immutable paths
## RED/GREEN deterministic checks
## Initial read-only preflight
## Exact live-write approval
## Candidate 1 — e5-small-384
## Candidate 2 — e5-base-768
## Candidate 3 — huydang-dek21-768
## Candidate 4 — qwen3-embedding-0.6b-1024
## Cross-collection/build-record verification
## Notebook 04 read-only evidence
## Acceptance mapping
## Failed, skipped and not verified
## Limitations and Reviewer handoff
```

For each command record actual exit/result, never expected text as observed
evidence. If fewer than four candidates completed, state `Phase incomplete` and
list later candidates as skipped after the first failure. End with: `This report
is Implementer evidence and does not constitute Reviewer approval or User
closure.` Do not edit Reviewer-owned status/guide/spec/plan documents.

---

## Plan approval effect

User approval of this Plan and Review Contract authorizes one Implementer effort
for Tasks 1–6: exact code/tests, local offline checks and one read-only preflight
artifact against only the four named full-corpus targets. It does not authorize
any dense full-corpus encode or Qdrant mutation.

After Reviewer inspects the `READY` preflight, a second explicit User approval
naming all four collections authorizes Task 7's four sequential dense encodes,
collection creation/upserts and Task 8's read-only inspection/reporting. That
approval does not authorize deletion/recovery, Foods access, replacement,
cleanup, cutover, Phase 5, dependencies/settings, paid APIs or Git operations.

Any failed partial target remains untouched and has no final record. Recovery
requires a new exact guarded-delete approval and an updated execution handoff;
this Plan contains no recovery command.
