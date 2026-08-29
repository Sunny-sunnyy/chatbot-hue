# Phase 8 — Notebook 08b Retrieval and Fusion Benchmark Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

Status: `approved_for_implementation_handoff` by the user on 2026-08-29 (+07).
Implementation starts only when the user delivers the prepared Implementer
prompt in the implementation session. Git commit/push remains separately scoped
by that session's handoff.

**Goal:** Build the approved Notebook 08b backend, tests, notebook and auditable artifacts for BM25 calibration, normalized TF-IDF sparse retrieval, 20 no-rerank retrieval/fusion settings and a gated two-family shortlist for Notebook 08d.

**Architecture:** Add one evaluation-scoped module that owns deterministic lexical/sparse retrieval, Qdrant isolation, fusion, metrics, checkpointing and sequential orchestration. Keep the canonical notebook as a Vietnamese teaching/display layer. Reuse the three real 08a dense collections and query runners without changing production BM25, startup, retrieval profiles or active settings.

**Tech Stack:** Python 3.13, uv, pytest, Underthesea 9.x, NumPy, Polars, psutil, qdrant-client 1.19.x, SentenceTransformers/PyVi through the existing 08a runners, Jupyter/nbconvert.

## Global Constraints

- Follow the approved spec exactly: `docs/superpowers/specs/2026-08-29-phase-8-08b-retrieval-fusion-benchmark-design.md`.
- Work only in `/home/minhhieu/hue_rag`; preserve all unrelated user changes in the dirty worktree.
- Do not change `backend/scoring/bm25.py`, production retrieval/startup/config, Golden V3, any 08a collection or the active production collection.
- Dense scope is exactly `e5-small-384`, `huydang-dek21-embedding-768`, and `e5-base-768` with the approved 08a revisions/contracts.
- BM25 settings are exactly `(1.5,0.75)`, `(0.9,0.75)`, `(2.0,0.75)`, `(1.5,0.25)`, `(1.5,1.0)`.
- Tokenizers are exactly Unicode `\w+` and Underthesea `word_tokenize(..., format="text")`; no third tokenizer.
- TF-IDF is exact log-TF, smoothed-IDF, L2-normalized unigram vocabulary with `min_df=1`, no cap and no stopwords.
- Generator depth is 30, fusion depth is 10, final depth is 5, repetitions are 3, RRF `k=60`, and weighted fusion is fixed `0.6/0.4`.
- The main matrix contains exactly 20 settings and no dense-to-TF-IDF rescoring.
- Qdrant creation requires `ALLOW_EXPERIMENT_MUTATION=true`; mismatch never deletes/rebuilds automatically.
- No reranker, generation, paid call, model fallback, automatic retry, device change or production cutover.
- The implementer may split execution into any number of sequential batches. Persist after every completed setting, resume only on exact provenance, and reconcile the entire matrix before finalist selection.
- Between batches, release models/clients/large objects, run garbage collection, clear CUDA cache only when applicable, restart processes, and remove only exact task-created ephemeral paths. Never delete durable artifacts, 08a/TF-IDF review collections, model caches or production resources without separate authorization.
- Repository notebook outputs remain empty and execution counts null; reviewer execution goes to `/tmp`.
- Do not commit or push unless the user separately grants Git authorization. The commit steps below are conditional gates, not present authorization.

---

## File map

- Create `backend/evaluation/sparse_benchmark.py`: all 08b contracts, retrieval, evaluation, persistence, display helpers and batch orchestration.
- Create `backend/tests/test_sparse_benchmark.py`: deterministic unit and local-Qdrant integration coverage.
- Modify `pyproject.toml`: add the `evaluation` dependency group containing Underthesea 9.x.
- Modify `uv.lock`: lock the evaluation dependency graph.
- Create `notebooks/08b_retrieval_fusion_benchmark.ipynb`: Vietnamese orchestration/display notebook with clean outputs.
- Create on authorized live execution only:
  - `evaluation/results/phase8_sparse_manifest.json`;
  - `evaluation/results/phase8_sparse_calibration.csv`;
  - `evaluation/results/phase8_sparse_results.csv`;
  - `evaluation/results/phase8_sparse_cases.jsonl`.
- Create after authorized implementation/run: `reports/phase_8_08b_retrieval_fusion_benchmark_implementation_report.md`.

The existing `backend/evaluation/embedding_benchmark.py`,
`backend/embedding/dense_benchmark.py`, `backend/evaluation/golden_dataset.py`,
`backend/retrieval/dense_retriever.py`, `backend/vectorstore/points.py` and
`backend/vectorstore/qdrant.py` are consumed, not modified.

---

### Task 1: Lock the evaluation dependency and implement deterministic tokenization/BM25

**Files:**
- Modify: `pyproject.toml`
- Modify: `uv.lock`
- Create: `backend/evaluation/sparse_benchmark.py`
- Create: `backend/tests/test_sparse_benchmark.py`

**Interfaces:**
- Produces: `unicode_word_tokenize(text: str) -> tuple[str, ...]`
- Produces: `underthesea_word_tokenize(text: str) -> tuple[str, ...]`
- Produces: `BM25Setting`, `BM25_SETTINGS`, `FullCorpusBM25`
- Produces: `FullCorpusBM25.search(query: str, limit: int = 30) -> list[RetrievedDocument]`
- Consumes later: canonical chunk dictionaries with `text` and `metadata.chunk_id/source/section`

- [ ] **Step 1: Write failing tokenizer and BM25 tests**

Add exact imports and tests to `backend/tests/test_sparse_benchmark.py`:

```python
import math

import pytest

from scoring.bm25 import BM25 as RuntimeBM25
from evaluation.sparse_benchmark import (
    BM25_SETTINGS,
    FullCorpusBM25,
    unicode_word_tokenize,
    underthesea_word_tokenize,
)


def make_chunk(chunk_id: str, text: str, source: str = "foods/a.md", section: str = "A"):
    return {
        "text": text,
        "metadata": {
            "chunk_id": chunk_id,
            "source": source,
            "title": source,
            "section": section,
            "category": "foods",
            "subcategory": "test",
            "chunk_type": "section",
        },
    }


def test_approved_bm25_settings_are_exact_and_ordered():
    assert [(s.setting_key, s.k1, s.b) for s in BM25_SETTINGS] == [
        ("baseline", 1.5, 0.75),
        ("k1_low", 0.9, 0.75),
        ("k1_high", 2.0, 0.75),
        ("b_low", 1.5, 0.25),
        ("b_high", 1.5, 1.0),
    ]


def test_unicode_tokenizer_normalizes_nfc_and_keeps_numbers():
    assert unicode_word_tokenize("BÚN bò Huế 2026!") == ("bún", "bò", "huế", "2026")


def test_underthesea_tokenizer_preserves_compound_tokens():
    tokens = underthesea_word_tokenize("Thừa Thiên Huế có bún bò.")
    assert "thừa_thiên_huế" in tokens
    assert "bún_bò" in tokens


def test_full_corpus_bm25_unicode_baseline_matches_runtime_scores():
    chunks = [
        make_chunk("c-1", "bún bò huế đặc biệt"),
        make_chunk("c-2", "cơm hến huế"),
        make_chunk("c-3", "chè cung đình"),
    ]
    runtime = RuntimeBM25().fit([c["text"] for c in chunks])
    candidate = FullCorpusBM25(chunks, unicode_word_tokenize, k1=1.5, b=0.75)
    expected = [runtime.score("bún bò", c["text"]) for c in chunks]
    observed = [candidate.score("bún bò", i) for i in range(3)]
    assert observed == pytest.approx(expected)
    assert [d.id for d in candidate.search("bún bò", limit=3)] == ["c-1"]


def test_full_corpus_bm25_rejects_invalid_parameters_and_handles_oov():
    chunks = [make_chunk("c-1", "bún bò huế")]
    with pytest.raises(ValueError, match="k1"):
        FullCorpusBM25(chunks, unicode_word_tokenize, k1=-0.1, b=0.75)
    with pytest.raises(ValueError, match="b"):
        FullCorpusBM25(chunks, unicode_word_tokenize, k1=1.5, b=1.1)
    assert FullCorpusBM25(chunks, unicode_word_tokenize).search("xyzzy") == []
```

- [ ] **Step 2: Run the focused tests and verify RED**

Run from `backend/`:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08b-test-uv-cache \
uv run --group evaluation --env-file ../.env \
python -m pytest tests/test_sparse_benchmark.py -q --tb=short
```

Expected: FAIL during import because `evaluation.sparse_benchmark` does not exist.

- [ ] **Step 3: Add the evaluation dependency group**

Run from repository root:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase8-08b-lock-uv-cache \
uv add --group evaluation "underthesea>=9.5,<10"
```

Expected: `pyproject.toml` gains this exact group and `uv.lock` resolves an exact
Underthesea 9.x version:

```toml
[dependency-groups]
evaluation = [
    "underthesea>=9.5,<10",
]
```

Do not add Underthesea to `[project].dependencies` and do not install it in a
notebook cell.

- [ ] **Step 4: Implement the minimal tokenizer and BM25 contracts**

Create `backend/evaluation/sparse_benchmark.py` with these exact public shapes:

```python
from collections import Counter
from dataclasses import dataclass
import math
import re
import unicodedata
from typing import Callable

from core.schema import RetrievedDocument

Tokenizer = Callable[[str], tuple[str, ...]]
UNICODE_TOKEN_PATTERN = re.compile(r"\w+", flags=re.UNICODE)
GENERATOR_DEPTH = 30


def _normalized_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return unicodedata.normalize("NFC", text).lower()


def unicode_word_tokenize(text: str) -> tuple[str, ...]:
    return tuple(UNICODE_TOKEN_PATTERN.findall(_normalized_text(text)))


def underthesea_word_tokenize(text: str) -> tuple[str, ...]:
    from underthesea import word_tokenize

    segmented = word_tokenize(_normalized_text(text), format="text")
    return tuple(token for token in segmented.split() if token)


@dataclass(frozen=True)
class BM25Setting:
    setting_key: str
    k1: float
    b: float


BM25_SETTINGS = (
    BM25Setting("baseline", 1.5, 0.75),
    BM25Setting("k1_low", 0.9, 0.75),
    BM25Setting("k1_high", 2.0, 0.75),
    BM25Setting("b_low", 1.5, 0.25),
    BM25Setting("b_high", 1.5, 1.0),
)


class FullCorpusBM25:
    def __init__(self, chunks, tokenizer: Tokenizer, *, k1: float = 1.5, b: float = 0.75):
        if not math.isfinite(k1) or k1 < 0:
            raise ValueError("k1 must be finite and >= 0")
        if not math.isfinite(b) or not 0 <= b <= 1:
            raise ValueError("b must be finite and in [0, 1]")
        self.k1, self.b, self.tokenizer = k1, b, tokenizer
        self.chunks = tuple(chunks)
        self.term_counts = tuple(Counter(tokenizer(str(c["text"]))) for c in self.chunks)
        lengths = [sum(counts.values()) for counts in self.term_counts]
        if not lengths or any(length == 0 for length in lengths):
            raise ValueError("BM25 requires non-empty tokenized documents")
        self.average_document_length = sum(lengths) / len(lengths)
        document_frequency = Counter()
        for counts in self.term_counts:
            document_frequency.update(counts.keys())
        n = len(self.chunks)
        self.idf = {
            term: math.log(((n - df + 0.5) / (df + 0.5)) + 1.0)
            for term, df in document_frequency.items()
        }

    def score(self, query: str, document_index: int) -> float:
        counts = self.term_counts[document_index]
        dl = sum(counts.values())
        total = 0.0
        for term in dict.fromkeys(self.tokenizer(query)):
            tf = counts.get(term, 0)
            idf = self.idf.get(term)
            if tf == 0 or idf is None:
                continue
            denominator = tf + self.k1 * (
                1.0 - self.b + self.b * dl / self.average_document_length
            )
            total += idf * (tf * (self.k1 + 1.0)) / denominator
        if not math.isfinite(total):
            raise ValueError("BM25 produced a non-finite score")
        return float(total)

    def search(self, query: str, limit: int = GENERATOR_DEPTH) -> list[RetrievedDocument]:
        if limit < 1:
            raise ValueError("limit must be positive")
        scored = [(self.score(query, i), i) for i in range(len(self.chunks))]
        positive = [(score, i) for score, i in scored if score > 0.0]
        positive.sort(key=lambda item: (-item[0], self.chunks[item[1]]["metadata"]["chunk_id"]))
        return [
            RetrievedDocument(
                id=str(self.chunks[i]["metadata"]["chunk_id"]),
                score=score,
                text=str(self.chunks[i]["text"]),
                metadata={**self.chunks[i]["metadata"], "bm25_score": score},
            )
            for score, i in positive[:limit]
        ]
```

- [ ] **Step 5: Run Task 1 tests and inspect the dependency diff**

Run the focused command from Step 2. Expected: all Task 1 tests PASS.

Also run from repository root:

```bash
git diff --check
git diff -- pyproject.toml uv.lock backend/evaluation/sparse_benchmark.py backend/tests/test_sparse_benchmark.py
```

Expected: no whitespace errors; Underthesea appears only in the evaluation group.

- [ ] **Step 6: Conditional commit gate**

Only if Git authorization has been granted:

```bash
git add pyproject.toml uv.lock backend/evaluation/sparse_benchmark.py backend/tests/test_sparse_benchmark.py
git commit -m "feat: add phase 8 sparse lexical primitives"
```

Otherwise record the passing test and continue without committing.

---

### Task 2: Implement normalized TF-IDF and the isolated sparse Qdrant collection

**Files:**
- Modify: `backend/evaluation/sparse_benchmark.py`
- Modify: `backend/tests/test_sparse_benchmark.py`

**Interfaces:**
- Consumes: `Tokenizer`, canonical chunks, Qdrant client
- Produces: `TfidfSparseEncoder.fit(chunks, tokenizer_key, tokenizer)`
- Produces: `TfidfSparseEncoder.encode(text) -> models.SparseVector | None`
- Produces: `TfidfState`
- Produces: `tfidf_collection_name(tokenizer_key, corpus_fingerprint) -> str`
- Produces: `ensure_tfidf_collection(client, collection_name: str, chunks, encoder: TfidfSparseEncoder, corpus_fingerprint: str, *, allow_mutation: bool) -> Literal["existing", "created"]`
- Produces: `query_tfidf(client, collection_name, encoder, query, limit=30)`
- Produces: `build_or_validate_tfidf(inputs, selected_lexical, expected_active_snapshot, allow_mutation) -> TfidfState`

- [ ] **Step 1: Write RED tests for exact TF-IDF math and deterministic vocabulary**

```python
from qdrant_client import QdrantClient

from evaluation.sparse_benchmark import (
    TfidfSparseEncoder,
    ensure_tfidf_collection,
    query_tfidf,
    tfidf_collection_name,
)


def test_tfidf_uses_log_tf_smoothed_idf_l2_and_sorted_vocabulary():
    chunks = [make_chunk("c-1", "bún bún bò"), make_chunk("c-2", "bò chè")]
    encoder = TfidfSparseEncoder.fit(chunks, "unicode_word", unicode_word_tokenize)
    assert encoder.vocabulary == {"bò": 0, "bún": 1, "chè": 2}
    vector = encoder.document_vectors[0]
    raw_bun = (1.0 + math.log(2.0)) * (math.log(3.0 / 2.0) + 1.0)
    raw_bo = 1.0
    norm = math.sqrt(raw_bun**2 + raw_bo**2)
    assert vector.indices == [0, 1]
    assert vector.values == pytest.approx([raw_bo / norm, raw_bun / norm])
    assert math.isclose(sum(v * v for v in vector.values), 1.0)


def test_tfidf_oov_query_returns_none():
    encoder = TfidfSparseEncoder.fit(
        [make_chunk("c-1", "bún bò")], "unicode_word", unicode_word_tokenize
    )
    assert encoder.encode("xyzzy") is None


def test_tfidf_collection_requires_explicit_mutation_and_is_reusable():
    client = QdrantClient(":memory:")
    chunks = [make_chunk("c-1", "bún bò"), make_chunk("c-2", "cơm hến")]
    encoder = TfidfSparseEncoder.fit(chunks, "unicode_word", unicode_word_tokenize)
    name = tfidf_collection_name("unicode_word", "a" * 64)
    with pytest.raises(PermissionError, match="ALLOW_EXPERIMENT_MUTATION"):
        ensure_tfidf_collection(client, name, chunks, encoder, "a" * 64, allow_mutation=False)
    assert ensure_tfidf_collection(client, name, chunks, encoder, "a" * 64, allow_mutation=True) == "created"
    assert ensure_tfidf_collection(client, name, chunks, encoder, "a" * 64, allow_mutation=False) == "existing"
    assert [d.id for d in query_tfidf(client, name, encoder, "bún", limit=2)] == ["c-1"]
```

- [ ] **Step 2: Run only the new tests and verify RED**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08b-test-uv-cache \
uv run --group evaluation --env-file ../.env \
python -m pytest tests/test_sparse_benchmark.py \
  -q --tb=short -k "tfidf"
```

Expected: FAIL because the TF-IDF interfaces are undefined.

- [ ] **Step 3: Implement exact TF-IDF vectors and collection naming**

Add imports and these public contracts:

```python
import hashlib
import json
from qdrant_client import models
from vectorstore.points import point_id_for

TFIDF_VECTOR_NAME = "tfidf"
TFIDF_FORMULA_VERSION = "logtf-smoothedidf-l2-v1"


@dataclass(frozen=True)
class TfidfSparseEncoder:
    tokenizer_key: str
    vocabulary: dict[str, int]
    idf: dict[str, float]
    document_vectors: tuple[models.SparseVector, ...]
    vocabulary_fingerprint: str
    tokenizer: Tokenizer

    @classmethod
    def fit(cls, chunks, tokenizer_key: str, tokenizer: Tokenizer):
        if tokenizer_key not in {"unicode_word", "underthesea_word"}:
            raise ValueError("unapproved tokenizer key")
        token_counts = [Counter(tokenizer(str(c["text"]))) for c in chunks]
        if not token_counts or any(not counts for counts in token_counts):
            raise ValueError("TF-IDF requires non-empty tokenized documents")
        terms = sorted({term for counts in token_counts for term in counts})
        vocabulary = {term: index for index, term in enumerate(terms)}
        n = len(token_counts)
        df = Counter(term for counts in token_counts for term in counts)
        idf = {term: math.log((n + 1.0) / (df[term] + 1.0)) + 1.0 for term in terms}
        vectors = tuple(cls._vector_from_counts(counts, vocabulary, idf) for counts in token_counts)
        digest = hashlib.sha256(
            json.dumps(terms, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return cls(tokenizer_key, vocabulary, idf, vectors, digest, tokenizer)

    @staticmethod
    def _vector_from_counts(counts, vocabulary, idf):
        weighted = {
            vocabulary[term]: (1.0 + math.log(count)) * idf[term]
            for term, count in counts.items()
            if term in vocabulary and count > 0
        }
        norm = math.sqrt(sum(value * value for value in weighted.values()))
        if norm == 0.0:
            raise ValueError("TF-IDF document vector is empty")
        indices = sorted(weighted)
        values = [weighted[index] / norm for index in indices]
        if not all(math.isfinite(value) and value != 0.0 for value in values):
            raise ValueError("TF-IDF vector contains invalid values")
        return models.SparseVector(indices=indices, values=values)

    def encode(self, text: str):
        counts = Counter(self.tokenizer(text))
        known = Counter({term: count for term, count in counts.items() if term in self.vocabulary})
        if not known:
            return None
        return self._vector_from_counts(known, self.vocabulary, self.idf)


@dataclass(frozen=True)
class TfidfState:
    encoder: TfidfSparseEncoder
    collection_name: str
    collection_status: str
    build_ms: float
    observed_peak_rss_mb: float


def tfidf_collection_name(tokenizer_key: str, corpus_fingerprint: str) -> str:
    if not re.fullmatch(r"[a-z0-9_]+", tokenizer_key):
        raise ValueError("invalid tokenizer key")
    if not re.fullmatch(r"[0-9a-f]{64}", corpus_fingerprint):
        raise ValueError("invalid corpus fingerprint")
    return f"hue_rag_phase8_08b_tfidf_v1_{tokenizer_key}_{corpus_fingerprint[:12]}"
```

- [ ] **Step 4: Implement fail-closed sparse collection create/reuse/query**

Implement `ensure_tfidf_collection` so the create branch is exactly:

```python
client.create_collection(
    collection_name,
    vectors_config=None,
    sparse_vectors_config={
        TFIDF_VECTOR_NAME: models.SparseVectorParams(
            index=models.SparseIndexParams(on_disk=False)
        )
    },
)
points = [
    models.PointStruct(
        id=point_id_for(str(chunk["metadata"]["chunk_id"])),
        vector={TFIDF_VECTOR_NAME: vector},
        payload={
            **chunk["metadata"],
            "text": chunk["text"],
            "corpus_fingerprint": corpus_fingerprint,
            "tokenizer_key": encoder.tokenizer_key,
            "tfidf_formula_version": TFIDF_FORMULA_VERSION,
            "vocabulary_fingerprint": encoder.vocabulary_fingerprint,
        },
    )
    for chunk, vector in zip(chunks, encoder.document_vectors)
]
client.upsert(collection_name=collection_name, points=points, wait=True)
```

The existing branch must inspect schema, count and scroll all payloads/vectors;
compare exact `chunk_id`, text hash and all four provenance values; and raise
`ValueError` without mutation on mismatch. Implement the query branch as:

```python
def query_tfidf(client, collection_name, encoder, query, limit=GENERATOR_DEPTH):
    vector = encoder.encode(query)
    if vector is None:
        return []
    response = client.query_points(
        collection_name=collection_name,
        query=vector,
        using=TFIDF_VECTOR_NAME,
        limit=limit,
        with_payload=True,
    )
    return [_retrieved_document_from_sparse_point(point, "tfidf_score") for point in response.points]
```

Validate every returned score as finite and preserve canonical payload metadata.

`build_or_validate_tfidf` must compare the active snapshot before work, fit the
encoder with the selected tokenizer key/callable, derive the deterministic
collection name, time `ensure_tfidf_collection`, compare the active snapshot
again, and return `TfidfState`. It must not catch a provenance or permission
failure as permission to rebuild.

- [ ] **Step 5: Run Task 2 and all focused tests**

Run the Task 2 command, then the full focused file. Expected: PASS and the
in-memory Qdrant collection reports exactly two points.

- [ ] **Step 6: Conditional commit gate**

```bash
git add backend/evaluation/sparse_benchmark.py backend/tests/test_sparse_benchmark.py
git commit -m "feat: add phase 8 tfidf sparse index"
```

Run only with separate Git authorization.

---

### Task 3: Implement fusion, stage metrics and category/finalist decisions

**Files:**
- Modify: `backend/evaluation/sparse_benchmark.py`
- Modify: `backend/tests/test_sparse_benchmark.py`

**Interfaces:**
- Produces: `rrf_fuse(dense, sparse, limit=10, rrf_k=60)`
- Produces: `weighted_fuse(dense, sparse, limit=10, dense_weight=0.6, sparse_weight=0.4)`
- Produces: `DepthCaseMetrics`, `score_at_depth`, `evaluate_stage_metrics`
- Produces: `evaluate_depth_category_guardrails`
- Produces: `select_family_finalist(results, dense_controls, family)`
- Reuses: `paired_bootstrap_intervals` only after converting exact 08b final-depth metrics to the existing 08a `CaseMetrics` shape.

- [ ] **Step 1: Write RED tests for union fusion and deterministic ties**

```python
from core.schema import RetrievedDocument
from evaluation.sparse_benchmark import rrf_fuse, weighted_fuse


def make_ranked(chunk_id: str, score: float):
    return RetrievedDocument(
        id=chunk_id,
        score=score,
        text=chunk_id,
        metadata={"chunk_id": chunk_id, "source": "foods/a.md", "section": chunk_id},
    )


def test_rrf_uses_union_rank_one_k60_and_chunk_id_ties():
    dense = [make_ranked("a", 0.9), make_ranked("b", 0.8)]
    sparse = [make_ranked("c", 9.0), make_ranked("b", 8.0)]
    fused = rrf_fuse(dense, sparse, limit=10, rrf_k=60)
    assert [d.id for d in fused] == ["b", "a", "c"]
    assert fused[0].score == pytest.approx(2 / 62)
    assert fused[1].score == fused[2].score


def test_weighted_fusion_normalizes_independently_and_missing_is_zero():
    dense = [make_ranked("a", 10.0), make_ranked("b", 5.0)]
    sparse = [make_ranked("b", 100.0), make_ranked("c", 50.0)]
    fused = weighted_fuse(dense, sparse, limit=10)
    assert [d.id for d in fused] == ["a", "b", "c"]
    assert [d.score for d in fused] == pytest.approx([0.6, 0.4, 0.0])


def test_weighted_constant_signal_maps_to_zero():
    dense = [make_ranked("b", 1.0), make_ranked("a", 1.0)]
    assert [d.id for d in weighted_fuse(dense, [], limit=10)] == ["a", "b"]
    assert all(d.score == 0.0 for d in weighted_fuse(dense, [], limit=10))
```

- [ ] **Step 2: Write RED tests for stage metrics and finalist gates**

Use six ordered `direct_fact` records for the large-category branch and two
ordered `numerical` records for the small-category branch. Assert:

```python
def test_family_finalist_requires_all_quality_category_and_latency_gates():
    dense = FinalistEvidence(
        setting_key="dense__e5-small-384",
        dense_setting_key="e5-small-384",
        sparse_family="dense",
        status="completed",
        successful_repetitions=3,
        fusion_recall_at_10=0.70,
        recall_at_5=0.60,
        ndcg_at_5=0.55,
        mrr_at_5=0.65,
        warm_total_p95_ms=30.0,
        all_category_guardrails_pass=True,
    )
    passing = FinalistEvidence(
        setting_key="hybrid-bm25-rrf__e5-small-384",
        dense_setting_key="e5-small-384",
        sparse_family="bm25",
        status="completed",
        successful_repetitions=3,
        fusion_recall_at_10=0.75,
        recall_at_5=0.60,
        ndcg_at_5=0.60,
        mrr_at_5=0.68,
        warm_total_p95_ms=59.0,
        all_category_guardrails_pass=True,
    )
    too_slow = FinalistEvidence(
        setting_key="hybrid-bm25-weighted__e5-small-384",
        dense_setting_key="e5-small-384",
        sparse_family="bm25",
        status="completed",
        successful_repetitions=3,
        fusion_recall_at_10=0.80,
        recall_at_5=0.65,
        ndcg_at_5=0.65,
        mrr_at_5=0.70,
        warm_total_p95_ms=61.0,
        all_category_guardrails_pass=True,
    )
    assert select_family_finalist(
        [passing, too_slow], {"e5-small-384": dense}, "bm25"
    ) == passing
```

Also assert ordered selection by Recall@5, nDCG@5, MRR@5 and latency; no
candidate returns `None`; ordered `(case_id, category)` mismatch raises; large
categories use hit count/nDCG `-0.02`, and small categories cannot lose an
existing hit.

- [ ] **Step 3: Run fusion/decision tests and verify RED**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08b-test-uv-cache \
uv run --group evaluation --env-file ../.env \
python -m pytest tests/test_sparse_benchmark.py \
  -q --tb=short -k "fusion or finalist or guardrail or stage"
```

Expected: FAIL because the interfaces do not exist.

- [ ] **Step 4: Implement RRF and weighted fusion exactly**

Use dictionaries keyed only by canonical `chunk_id`. Copy result objects and
metadata; never mutate generator inputs. The core loops must be:

```python
for rank, doc in enumerate(dense, start=1):
    entries[doc.id]["rrf"] += 1.0 / (rrf_k + rank)
for rank, doc in enumerate(sparse, start=1):
    entries[doc.id]["rrf"] += 1.0 / (rrf_k + rank)
```

and:

```python
dense_norm = _min_max_by_id(dense)
sparse_norm = _min_max_by_id(sparse)
for chunk_id in set(dense_norm) | set(sparse_norm):
    score = 0.6 * dense_norm.get(chunk_id, 0.0) + 0.4 * sparse_norm.get(chunk_id, 0.0)
```

Validate fixed weights sum to one, `rrf_k == 60`, generator lists contain no
duplicate `chunk_id`, all scores are finite, and sort `(-score, chunk_id)`.

- [ ] **Step 5: Implement depth-aware relevance, guards, bootstrap and finalist selection**

Define immutable metrics with explicit depth names instead of reusing an
`at_5` field for depth 30:

```python
@dataclass(frozen=True)
class DepthCaseMetrics:
    case_id: str
    category: str
    depth: int
    recall: float
    mrr: float
    ndcg: float
    hit: bool
    relevant_keys: tuple[tuple[str, str], ...]
    ranked_keys: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class FinalistEvidence:
    setting_key: str
    dense_setting_key: str
    sparse_family: str
    status: str
    successful_repetitions: int
    fusion_recall_at_10: float
    recall_at_5: float
    ndcg_at_5: float
    mrr_at_5: float
    warm_total_p95_ms: float
    all_category_guardrails_pass: bool
```

`score_at_depth(case, docs, depth)` must apply the same exact source+section
deduplication as 08a. `evaluate_stage_metrics` computes only applicable stages.
For final bootstrap, convert the 45 depth-five records to 08a `CaseMetrics` and
call `paired_bootstrap_intervals(reference, candidate, samples=10_000, seed=42)`.

Implement the five finalist predicates exactly as the spec and return `None`
when no candidate passes.

- [ ] **Step 6: Run all focused tests and conditional commit**

Expected: all Task 1–3 tests PASS.

```bash
git add backend/evaluation/sparse_benchmark.py backend/tests/test_sparse_benchmark.py
git commit -m "feat: add phase 8 retrieval fusion metrics"
```

Commit only when authorized.

---

### Task 4: Implement canonical inputs, 08a prerequisite identity and production isolation

**Files:**
- Modify: `backend/evaluation/sparse_benchmark.py`
- Modify: `backend/tests/test_sparse_benchmark.py`

**Interfaces:**
- Produces: `SparseBenchmarkInputs`
- Produces: `load_sparse_benchmark_inputs() -> SparseBenchmarkInputs`
- Produces: `fingerprint_corpus(chunks)`, `fingerprint_golden(cases)`
- Produces: `validate_08a_prerequisites(inputs) -> tuple[DensePrerequisite, ...]`
- Reuses: `ALL_DENSE_SETTINGS`, `EMBEDDING_RESULTS_PATH`, `CSV_COLUMNS`, `snapshot_active_collection`

- [ ] **Step 1: Write RED tests for stable fingerprints and exact 08a identity**

Use a fake read-only client only for unit-level schema/payload validation; it is
not integration evidence. Assert that text, chunk ID, dimension, model ID,
collection name, CSV header, `status=completed` and
`successful_repetitions=3` mismatches each fail with a targeted message.

```python
def test_corpus_fingerprint_is_order_independent_but_text_sensitive():
    first = [make_chunk("b", "cơm hến"), make_chunk("a", "bún bò")]
    second = list(reversed(first))
    assert fingerprint_corpus(first) == fingerprint_corpus(second)
    changed = [make_chunk("b", "cơm hến khác"), make_chunk("a", "bún bò")]
    assert fingerprint_corpus(first) != fingerprint_corpus(changed)
```

- [ ] **Step 2: Run prerequisite tests and verify RED**

Run `pytest ... -k "fingerprint or prerequisite or production_snapshot"`.
Expected: FAIL on missing interfaces.

- [ ] **Step 3: Implement canonical loading and computed 08a identities**

`load_sparse_benchmark_inputs()` must call the existing Golden V3 loader and
validator, production chunker, `validate_chunks`, `load_settings` and
`client_from_settings`; enforce 45/572 before returning.

Use compact UTF-8 JSON with sorted keys and SHA-256. Corpus fingerprint input is
the list sorted by `chunk_id`, retaining `chunk_id`, text, source, section,
title, category, subcategory and chunk type. Golden fingerprint input is the
45 `GoldenCase.model_dump(mode="json")` mappings sorted by `case_id`. Chunker
fingerprint is SHA-256 of the exact bytes of
`backend/ingestion/chunking/markdown_chunker.py`. Resolve that path from the
imported module, never from the current working directory.

There is no separate 08a manifest file. Build each approved 08a prerequisite
identity from all three real sources:

```text
ALL_DENSE_SETTINGS constant
+ phase8_embedding_results.csv overall completed row
+ live collection schema/count/payload identity
```

Store the resulting three computed identities in the new 08b manifest. Require
the exact 08a CSV ordered header and exact current setting model/revision/
dimension/collection fields. Scroll only required payload fields with vectors
disabled and compare all 572 canonical `(chunk_id, text)` pairs.

- [ ] **Step 4: Protect the active snapshot before and after every mutable stage**

Reuse `snapshot_active_collection(inputs)` from 08a. Require an
`expected_active_snapshot` argument for TF-IDF creation and every main setting.
Compare immediately before and after. Reject the active collection name as any
write target.

- [ ] **Step 5: Run focused tests, full existing 08a tests and conditional commit**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08b-test-uv-cache \
uv run --group evaluation --env-file ../.env \
python -m pytest tests/test_sparse_benchmark.py tests/test_embedding_benchmark.py -q --tb=short
```

Expected: PASS; existing 08a behavior remains unchanged.

Conditional commit:

```bash
git add backend/evaluation/sparse_benchmark.py backend/tests/test_sparse_benchmark.py
git commit -m "feat: validate phase 8 dense prerequisites"
```

---

### Task 5: Implement exact artifacts, atomic checkpoints and batch resume

**Files:**
- Modify: `backend/evaluation/sparse_benchmark.py`
- Modify: `backend/tests/test_sparse_benchmark.py`

**Interfaces:**
- Produces: `ExperimentManifest`, `CheckpointState`
- Produces: `write_manifest_atomic`, `upsert_calibration_rows`, `upsert_result_rows`, `upsert_case_records`
- Produces: `load_checkpoint(expected_manifest) -> CheckpointState`
- Produces: `load_checkpoint_for_inputs(inputs, selected_lexical, tfidf_state) -> CheckpointState`
- Produces: `pending_setting_keys(requested_keys, checkpoint) -> tuple[str, ...]`

- [ ] **Step 1: Lock exact schemas in tests**

Define and assert exact tuple constants:

```python
CALIBRATION_COLUMNS = (
    "experiment_version", "calibration_stage", "setting_key", "category",
    "tokenizer_key", "k1", "b", "status", "error", "case_count",
    "hit_case_count", "recall_at_30", "mrr_at_5", "ndcg_at_5",
    "successful_repetitions", "ranking_stable", "build_ms",
    "warm_total_p50_ms", "warm_total_p95_ms", "observed_peak_rss_mb",
    "delta_recall_at_30", "delta_mrr_at_5", "delta_ndcg_at_5",
    "category_guardrail_pass", "all_category_guardrails_pass",
    "selected", "selection_reason",
)
```

Lock the other exact schemas:

```python
RESULT_COLUMNS = (
    "experiment_version", "setting_order", "setting_key", "setting_label",
    "category", "path", "dense_setting_key", "sparse_family",
    "fusion_method", "status", "error", "case_count", "hit_case_count",
    "successful_repetitions", "ranking_stable", "dense_recall_at_30",
    "sparse_recall_at_30", "candidate_union_recall", "fusion_recall_at_10",
    "recall_at_5", "mrr_at_5", "ndcg_at_5", "dense_query_p50_ms",
    "dense_query_p95_ms", "sparse_query_p50_ms", "sparse_query_p95_ms",
    "fusion_p50_ms", "fusion_p95_ms", "warm_total_p50_ms",
    "warm_total_p95_ms", "build_ms", "observed_peak_rss_mb",
    "delta_fusion_recall_at_10", "delta_recall_at_5", "delta_mrr_at_5",
    "delta_ndcg_at_5", "recall_ci_lower", "recall_ci_upper",
    "mrr_ci_lower", "mrr_ci_upper", "ndcg_ci_lower", "ndcg_ci_upper",
    "category_guardrail_pass", "all_category_guardrails_pass",
    "fusion_recall_gate", "final_recall_gate", "latency_gate",
    "complete_gate", "finalist_eligible", "finalist_selected",
)

CASE_RECORD_FIELDS = (
    "experiment_version", "setting_order", "setting_key", "case_id",
    "category", "status", "error", "relevant_source_sections",
    "derived_relevant_chunk_ids", "successful_repetitions",
    "ranking_stable", "dense_top_30", "sparse_top_30",
    "candidate_union_chunk_ids", "fusion_top_10", "final_top_5",
    "dense_recall_at_30", "sparse_recall_at_30",
    "candidate_union_recall", "fusion_recall_at_10", "recall_at_5",
    "mrr_at_5", "ndcg_at_5", "latency_by_repetition_ms",
)
```

Each ranked-list item is a JSON mapping with exact applicable keys from
`chunk_id`, `rank`, `raw_score`, `normalized_score`, `rrf_score`, `fused_score`,
`source` and `section`. Omit non-applicable score keys rather than storing false
zeros.

Test wrong/missing/reordered CSV headers, wrong experiment version, wrong
fingerprint, duplicate keys and malformed JSONL as fail-closed cases.

- [ ] **Step 2: Write RED tests for atomic idempotent resume behavior**

```python
def make_test_manifest(corpus_fingerprint: str):
    return ExperimentManifest(
        schema_version="phase8-sparse-manifest-v1",
        experiment_version="phase8-08b-v1",
        immutable_identity={
            "corpus_fingerprint": corpus_fingerprint,
            "golden_fingerprint": "b" * 64,
            "chunker_fingerprint": "c" * 64,
            "dense_prerequisites": [],
            "dependencies": {},
            "selected_bm25": {"setting_key": "baseline", "k1": 1.5, "b": 0.75},
            "selected_tokenizer": "unicode_word",
            "tfidf": {
                "formula_version": "logtf-smoothedidf-l2-v1",
                "vocabulary_fingerprint": "d" * 64,
                "collection_name": "hue_rag_phase8_08b_tfidf_v1_unicode_word_aaaaaaaaaaaa",
            },
            "fusion": {"rrf_k": 60, "dense_weight": 0.6, "sparse_weight": 0.4},
            "depths": {"generator": 30, "fusion": 10, "final": 5},
            "repetitions": 3,
            "bootstrap": {"samples": 10_000, "seed": 42},
            "artifact_schemas": {"calibration": 1, "results": 1, "cases": 1},
        },
        batch_history=(),
    )


def make_completed_result_row(setting_key: str, category: str):
    row = {column: "" for column in RESULT_COLUMNS}
    row.update(
        experiment_version="phase8-08b-v1",
        setting_key=setting_key,
        category=category,
        status="completed",
        successful_repetitions=3,
    )
    return row


def test_checkpoint_skips_only_exact_completed_settings(tmp_path):
    manifest = make_test_manifest(corpus_fingerprint="a" * 64)
    write_manifest_atomic(manifest, tmp_path / "manifest.json")
    upsert_result_rows(
        [make_completed_result_row("bm25-only", "overall")],
        tmp_path / "results.csv",
    )
    checkpoint = load_checkpoint(manifest, results_dir=tmp_path)
    assert pending_setting_keys(("bm25-only", "tfidf-only"), checkpoint) == ("tfidf-only",)


def test_checkpoint_rejects_provenance_mismatch(tmp_path):
    write_manifest_atomic(
        make_test_manifest(corpus_fingerprint="a" * 64),
        tmp_path / "manifest.json",
    )
    with pytest.raises(ValueError, match="corpus_fingerprint"):
        load_checkpoint(
            make_test_manifest(corpus_fingerprint="b" * 64),
            results_dir=tmp_path,
        )
```

- [ ] **Step 3: Run artifact/resume tests and verify RED**

Run `pytest ... -k "artifact or checkpoint or resume or schema"`.
Expected: FAIL on missing interfaces.

- [ ] **Step 4: Implement same-directory atomic writes and exact upserts**

Define the manifest container used by the tests and orchestration:

```python
@dataclass(frozen=True)
class ExperimentManifest:
    schema_version: str
    experiment_version: str
    immutable_identity: dict[str, object]
    batch_history: tuple[dict[str, object], ...]
```

Validate that `immutable_identity` contains exactly the keys shown in
`make_test_manifest`; production construction fills their real values. Batch
history may grow, but resume equality compares `schema_version`,
`experiment_version` and `immutable_identity` exactly.

Use `tempfile.NamedTemporaryFile(delete=False, dir=path.parent)` followed by
flush, `os.fsync`, close and `os.replace`. On exception, unlink only that exact
temporary path.

CSV keys are:

```text
calibration: experiment_version + calibration_stage + setting_key + category
main result: experiment_version + setting_key + category
case JSONL: experiment_version + setting_key + case_id
```

Sort calibration by stage/approved setting/category, main results by the exact
20-setting order then overall/category, and cases by setting order/case ID.
Sanitize every error as `ExceptionType: message` with credential/header patterns
removed.

- [ ] **Step 5: Implement manifest-exact resume and partial status**

The manifest equality gate includes corpus/Golden/chunker fingerprints, all
three computed 08a identities, dependency versions, selected BM25/tokenizer,
TF-IDF formula/vocabulary/collection, depths, weights, RRF constant,
repetitions, bootstrap seed and artifact schema version.

`completed` requires all three 45-case repetitions. `partial` and `failed` are
persisted but remain pending on the next authorized attempt. A rerun replaces
only the exact setting/category/case keys.

- [ ] **Step 6: Run focused tests and conditional commit**

Expected: all artifact/checkpoint tests PASS; repeated writes are byte-stable.

```bash
git add backend/evaluation/sparse_benchmark.py backend/tests/test_sparse_benchmark.py
git commit -m "feat: checkpoint phase 8 sparse benchmarks"
```

Commit only when authorized.

---

### Task 6: Implement calibration orchestration and selection

**Files:**
- Modify: `backend/evaluation/sparse_benchmark.py`
- Modify: `backend/tests/test_sparse_benchmark.py`

**Interfaces:**
- Produces: `CalibrationSelection`
- Produces: `run_bm25_parameter_calibration(inputs, checkpoint) -> CalibrationSelection`
- Produces: `run_tokenizer_calibration(inputs, parameter_selection, checkpoint) -> CalibrationSelection`
- Produces: `load_or_run_calibration(inputs, checkpoint, *, expected_active_snapshot) -> SelectedLexicalContract`

- [ ] **Step 1: Write RED tests for the two-stage decision hierarchy**

Create deterministic result fixtures proving:

- Recall@30 dominates supporting metrics when difference is greater than 0.005;
- within 0.005, nDCG@5, then MRR@5, then latency decide;
- a failed category guard excludes a candidate;
- no passing parameter candidate returns baseline;
- an Underthesea tie retains Unicode;
- a resumed exact completed calibration does not execute the scorer again.

Lock the exact selection types before implementing orchestration:

```python
@dataclass(frozen=True)
class CalibrationSelection:
    stage: str
    selected_setting_key: str
    selection_reason: str
    rows: tuple[dict[str, object], ...]


@dataclass(frozen=True)
class SelectedLexicalContract:
    bm25_setting_key: str
    k1: float
    b: float
    tokenizer_key: str
    tokenizer: Tokenizer
    parameter_selection_reason: str
    tokenizer_selection_reason: str
```

- [ ] **Step 2: Run calibration tests and verify RED**

Run `pytest ... -k "calibration or tokenizer_selection or parameter_selection"`.
Expected: FAIL on missing orchestration.

- [ ] **Step 3: Implement one-calibration-setting lifecycle**

For each setting:

```text
record RSS -> build pre-tokenized corpus cache -> discarded warm-up
-> 3 repetitions x 45 full-corpus queries -> canonical quality from rep 1
-> ranking stability -> p50/p95 from per-query medians
-> overall/category rows -> atomic calibration upsert -> release cache
```

Use parameter settings in exact approved order. Only after parameter selection,
run the two tokenizer rows at the selected `k1/b`. Use hit@30 category guards.
Persist selected reason and selected lexical contract in the manifest.

- [ ] **Step 4: Implement dependency/version and cleanup behavior**

Import Underthesea lazily only for its row. Record exact installed version.
After each setting execute:

```python
del bm25_index
gc.collect()
if torch.cuda.is_available():
    torch.cuda.empty_cache()
```

Do not catch an Underthesea import/inference error as a Unicode fallback. Save
the failure and block dependent selection.

- [ ] **Step 5: Run all focused tests and conditional commit**

Expected: five parameter settings and two tokenizer settings reconcile; all
Task 1–6 tests PASS.

```bash
git add backend/evaluation/sparse_benchmark.py backend/tests/test_sparse_benchmark.py
git commit -m "feat: calibrate phase 8 lexical retrieval"
```

---

### Task 7: Implement the exact 20-setting catalog, sequential runner and shortlist

**Files:**
- Modify: `backend/evaluation/sparse_benchmark.py`
- Modify: `backend/tests/test_sparse_benchmark.py`

**Interfaces:**
- Produces: `RetrievalSetting`, `RETRIEVAL_SETTINGS`
- Produces: `run_retrieval_setting(setting, inputs, selected_lexical, tfidf_state, *, expected_active_snapshot) -> SparseBenchmarkResult`
- Produces: `run_retrieval_batch(inputs, selected_lexical, tfidf_state, *, requested_setting_keys, expected_active_snapshot) -> Iterator[SparseBenchmarkResult]`
- Produces: `reconcile_sparse_benchmark(checkpoint, *, expected_active_snapshot) -> ReconciliationResult`
- Produces: notebook display helpers for settings, calibration, quality, category, latency, cases and finalists.

- [ ] **Step 1: Lock the exact catalog in a RED test**

Assert 20 unique ordered keys composed as:

```python
expected = [
    "dense__e5-small-384",
    "dense__huydang-dek21-embedding-768",
    "dense__e5-base-768",
    "bm25-only",
    "dense-bm25-rescore__e5-small-384",
    "dense-bm25-rescore__huydang-dek21-embedding-768",
    "dense-bm25-rescore__e5-base-768",
    "hybrid-bm25-rrf__e5-small-384",
    "hybrid-bm25-weighted__e5-small-384",
    "hybrid-bm25-rrf__huydang-dek21-embedding-768",
    "hybrid-bm25-weighted__huydang-dek21-embedding-768",
    "hybrid-bm25-rrf__e5-base-768",
    "hybrid-bm25-weighted__e5-base-768",
    "tfidf-only",
    "hybrid-tfidf-rrf__e5-small-384",
    "hybrid-tfidf-weighted__e5-small-384",
    "hybrid-tfidf-rrf__huydang-dek21-embedding-768",
    "hybrid-tfidf-weighted__huydang-dek21-embedding-768",
    "hybrid-tfidf-rrf__e5-base-768",
    "hybrid-tfidf-weighted__e5-base-768",
]
assert [setting.setting_key for setting in RETRIEVAL_SETTINGS] == expected
assert not any("tfidf-rescore" in key for key in expected)
```

Lock the orchestration result interfaces used by later notebook cells:

```python
@dataclass(frozen=True)
class RetrievalSetting:
    order: int
    setting_key: str
    setting_label: str
    path: str
    dense_setting_key: str | None
    sparse_family: str | None
    fusion_method: str | None


@dataclass
class SparseBenchmarkResult:
    setting: RetrievalSetting
    status: str
    error: str
    summary: dict[str, object]
    category_rows: list[dict[str, object]]
    case_records: list[dict[str, object]]
    rankings_by_repetition: list[dict[str, tuple[str, ...]]]


@dataclass(frozen=True)
class ReconciliationResult:
    complete: bool
    summary: dict[str, object]
    bm25_finalist: str | None
    tfidf_finalist: str | None
```

- [ ] **Step 2: Write RED lifecycle/batch tests**

Use injected deterministic dense/sparse search callables to prove generator
depth 30, fusion depth 10, final depth 5, three complete repetitions, raw
evidence capture, failure persistence, exact requested-key validation, canonical
ordering, completed-setting skip and resource cleanup callback execution.

Also prove reconciliation rejects 19/20 settings, fewer than 200 result rows,
fewer than 900 case records, any setting below 3/3, and a changed active snapshot.

- [ ] **Step 3: Run catalog/orchestration tests and verify RED**

Run `pytest ... -k "catalog or retrieval_batch or lifecycle or reconciliation"`.
Expected: FAIL on missing interfaces.

- [ ] **Step 4: Implement one-setting execution without hidden reuse**

For each setting, execute the exact declared pipeline end-to-end so measured
latency includes its applicable components. Dense settings use the existing 08a
`build_dense_runner`, `TimedQueryRunnerWrapper` and `DenseRetriever` against the
approved collection; never embed documents.

For true hybrid, independently query dense top 30 and the selected sparse top
30, fuse to top 10, and evaluate top 5. For dense-to-BM25, score only dense top
30 and use the same independent min-max `0.6/0.4` control.

After each setting:

1. write overall/category rows;
2. write all 45 per-case records including three-repetition evidence;
3. yield the result to the notebook;
4. close runner/client handles owned by the setting;
5. delete large objects, `gc.collect()`, and conditionally clear CUDA cache.

- [ ] **Step 5: Implement arbitrary requested batches and exact resume**

Parse a comma-separated environment value only through:

```python
def requested_setting_keys_from_env(value: str | None) -> tuple[str, ...]:
    if value is None or not value.strip():
        return tuple(setting.setting_key for setting in RETRIEVAL_SETTINGS)
    requested = tuple(part.strip() for part in value.split(",") if part.strip())
    unknown = set(requested) - {setting.setting_key for setting in RETRIEVAL_SETTINGS}
    if unknown:
        raise ValueError(f"unknown 08b setting keys: {sorted(unknown)}")
    return tuple(key for key in (s.setting_key for s in RETRIEVAL_SETTINGS) if key in requested)
```

The operator may choose any subset per process. The runner skips only exact
completed checkpoints and records requested/executed/skipped keys in the
manifest/report. It must not require one process or one notebook execution.

- [ ] **Step 6: Implement final reconciliation, bootstrap and per-family shortlist**

Reconciliation requires exactly 20 completed overall settings, 200 main rows,
900 case rows, 3/3 repetitions and unchanged production snapshot. Only then
compute five finalist gates against same-model dense controls, bootstrap CIs,
and select at most one BM25 plus one TF-IDF candidate.

- [ ] **Step 7: Run focused and regression tests**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08b-test-uv-cache \
uv run --group evaluation --env-file ../.env \
python -m pytest \
  tests/test_sparse_benchmark.py \
  tests/test_embedding_benchmark.py \
  tests/test_bm25.py \
  tests/test_retrieval_service.py \
  -q --tb=short
```

Expected: PASS; runtime BM25/retrieval tests remain unchanged.

- [ ] **Step 8: Conditional commit gate**

```bash
git add backend/evaluation/sparse_benchmark.py backend/tests/test_sparse_benchmark.py
git commit -m "feat: orchestrate phase 8 retrieval benchmark"
```

---

### Task 8: Build the clean Vietnamese Notebook 08b teaching layer

**Files:**
- Create: `notebooks/08b_retrieval_fusion_benchmark.ipynb`
- Modify: `backend/evaluation/sparse_benchmark.py`
- Modify: `backend/tests/test_sparse_benchmark.py`

**Interfaces:**
- Consumes all public orchestration/display APIs from Tasks 1–7.
- Produces a parseable notebook with approximately 35 alternating Markdown/code cells, empty outputs and null execution counts.

- [ ] **Step 1: Write RED structure tests before creating the notebook**

Add a test that loads JSON and asserts:

```python
def test_08b_notebook_structure_and_clean_outputs():
    notebook = json.loads((REPO_ROOT / "notebooks/08b_retrieval_fusion_benchmark.ipynb").read_text())
    headings = "\n".join(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "markdown"
    )
    assert "Phần A — BM25 và tokenizer" in headings
    assert "Phần B — TF-IDF và fusion" in headings
    assert "Không phải cutover" in headings
    assert all(cell.get("execution_count") is None for cell in notebook["cells"] if cell["cell_type"] == "code")
    assert all(cell.get("outputs") == [] for cell in notebook["cells"] if cell["cell_type"] == "code")
    code = "\n".join("".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "code")
    assert "word_tokenize(" not in code
    assert "client.query_points(" not in code
    assert "rrf_score" not in code
```

Expected RED: notebook path is absent.

- [ ] **Step 2: Add exact display helpers to the backend**

Implement Polars-returning helpers:

```text
environment_table()
canonical_inputs_table(inputs)
dense_prerequisite_table(prerequisites)
bm25_parameter_table()
calibration_table(checkpoint)
retrieval_settings_table()
quality_table(checkpoint)
stage_recall_table(checkpoint)
category_guardrail_table(checkpoint)
latency_resource_table(checkpoint)
case_disagreement_table(checkpoint)
bootstrap_finalist_table(checkpoint)
artifact_reconciliation_table(checkpoint)
```

Helpers may shape existing results only; they cannot score, retrieve, mutate or
persist.

- [ ] **Step 3: Create the notebook with the approved cell flow**

Use the exact backend-driven code sequence below, separated by concise
Vietnamese Markdown cells explaining purpose, fixed variables, expected
resource behavior and how to read each result:

```python
import os

from evaluation.sparse_benchmark import (
    load_sparse_benchmark_inputs,
    snapshot_active_collection,
    validate_08a_prerequisites,
    load_or_run_calibration,
    build_or_validate_tfidf,
    requested_setting_keys_from_env,
    run_retrieval_batch,
    load_checkpoint_for_inputs,
    reconcile_sparse_benchmark,
)
```

```python
inputs = load_sparse_benchmark_inputs()
active_before = snapshot_active_collection(inputs)
prerequisites = validate_08a_prerequisites(inputs)
```

```python
selected_lexical = load_or_run_calibration(
    inputs,
    expected_active_snapshot=active_before,
)
```

```python
tfidf_state = build_or_validate_tfidf(
    inputs,
    selected_lexical,
    expected_active_snapshot=active_before,
    allow_mutation=os.getenv("ALLOW_EXPERIMENT_MUTATION", "").lower() == "true",
)
```

```python
requested_keys = requested_setting_keys_from_env(os.getenv("HUE_RAG_08B_SETTING_KEYS"))
batch_results = []
for result in run_retrieval_batch(
    inputs,
    selected_lexical,
    tfidf_state,
    requested_setting_keys=requested_keys,
    expected_active_snapshot=active_before,
):
    batch_results.append(result)
    display(result.summary)
```

```python
checkpoint = load_checkpoint_for_inputs(inputs, selected_lexical, tfidf_state)
reconciliation = reconcile_sparse_benchmark(
    checkpoint,
    expected_active_snapshot=active_before,
)
display(artifact_reconciliation_table(checkpoint))
display(bootstrap_finalist_table(checkpoint) if reconciliation.complete else reconciliation.summary)
```

The notebook must visibly state that incomplete batches are expected and safe;
the final shortlist remains unavailable until reconciliation is complete.

- [ ] **Step 4: Add the three approved plots without notebook scoring logic**

Plot only backend-returned tables for stage recall, quality/latency and category
deltas. Keep the source table immediately above each plot. Do not add a plotting
dependency if Polars/Pandas/Matplotlib already available through the locked
environment; if Matplotlib is not installed, omit plots and keep tables rather
than mutate scope.

- [ ] **Step 5: Run notebook structure and import-only smoke checks**

From repository root:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase8-08b-test-uv-cache \
uv run --group evaluation --env-file .env \
python -m pytest backend/tests/test_sparse_benchmark.py \
  -q --tb=short -k "notebook or display"
```

Then parse without execution:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase8-08b-test-uv-cache \
uv run --group evaluation python -m jupyter nbconvert \
  --to notebook notebooks/08b_retrieval_fusion_benchmark.ipynb \
  --stdout >/dev/null
```

Expected: tests PASS; nbconvert exits 0; source notebook remains clean.

- [ ] **Step 6: Conditional commit gate**

```bash
git add notebooks/08b_retrieval_fusion_benchmark.ipynb backend/evaluation/sparse_benchmark.py backend/tests/test_sparse_benchmark.py
git commit -m "docs: add phase 8 retrieval fusion notebook"
```

---

### Task 9: Execute in approved batches, reconcile evidence and write the implementation report

**Files:**
- Create/update only after authorized live execution:
  - `evaluation/results/phase8_sparse_manifest.json`
  - `evaluation/results/phase8_sparse_calibration.csv`
  - `evaluation/results/phase8_sparse_results.csv`
  - `evaluation/results/phase8_sparse_cases.jsonl`
- Create: `reports/phase_8_08b_retrieval_fusion_benchmark_implementation_report.md`

**Interfaces:**
- Consumes: exact checkpoint/resume notebook from Task 8.
- Produces: complete 5+2 calibration evidence, 20-setting/200-row/900-case evidence, one 572-point TF-IDF review collection, zero-to-two 08b finalists, implementation handoff.

- [ ] **Step 1: Run focused and relevant regression tests before live mutation**

```bash
cd /home/minhhieu/hue_rag/backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08b-test-uv-cache \
uv run --group evaluation --env-file ../.env \
python -m pytest \
  tests/test_sparse_benchmark.py \
  tests/test_embedding_benchmark.py \
  tests/test_bm25.py \
  tests/test_retrieval_service.py \
  -q --tb=short
```

Expected: all selected tests PASS. Stop before live execution on failure.

- [ ] **Step 2: Record the exact operator-selected batch partition**

The implementer may choose one, five, ten or any other practical number of
batches. Before each batch, record its exact comma-separated setting keys and
expected remaining count in the implementation report. The first batch that
needs to create the TF-IDF collection uses the explicit mutation flag; later
batches validate/reuse with the flag false.

Example command template from repository root:

```bash
ALLOW_EXPERIMENT_MUTATION=true \
HUE_RAG_08B_SETTING_KEYS="dense__e5-small-384,dense__huydang-dek21-embedding-768,dense__e5-base-768,bm25-only,tfidf-only" \
UV_CACHE_DIR=/tmp/hue-rag-phase8-08b-live-uv-cache \
uv run --group evaluation --env-file .env \
jupyter nbconvert --execute --to notebook \
  notebooks/08b_retrieval_fusion_benchmark.ipynb \
  --output /tmp/08b-retrieval-fusion-batch-01.ipynb \
  --ExecutePreprocessor.timeout=28800
```

This five-setting list is a concrete valid first-batch example, not a required
partition. The operator may replace it with any exact subset copied from the
printed 20-setting catalog and must log the chosen keys before execution.
Subsequent batches set
`ALLOW_EXPERIMENT_MUTATION=false` and increment the exact output name, beginning
with `/tmp/08b-retrieval-fusion-batch-02.ipynb`.

- [ ] **Step 3: Checkpoint and release resources after every batch**

After each notebook process exits:

```bash
git status --short
```

Then inspect the manifest's `requested_setting_keys`, `completed_setting_keys`,
`pending_setting_keys`, active snapshot and artifact row counts through the
notebook output or a read-only backend display call. Do not continue if
provenance changed. Because nbconvert exits its process, RAM/VRAM is released;
remove only exact failed temporary notebook outputs if cleanup is necessary.

- [ ] **Step 4: Resume until all 20 settings reconcile**

Repeat Steps 2–3 with any practical batch grouping. Completed exact setting
keys must be skipped; partial/failed settings remain explicit. Do not change
models, formulas, depths, repetitions or gates to make a batch pass.

Expected final reconciliation:

```text
BM25 parameter settings: 5
tokenizer settings: 2
main settings completed 3/3: 20
main long-format rows: 200
per-case records: 900
TF-IDF collection points: 572
production snapshot changed: false
```

- [ ] **Step 5: Run a final read-only complete notebook execution**

After all checkpoints are complete, run with all setting keys omitted and
mutation false. It must skip exact completed settings, reconcile artifacts and
display the final shortlist without recomputing the matrix:

```bash
ALLOW_EXPERIMENT_MUTATION=false \
UV_CACHE_DIR=/tmp/hue-rag-phase8-08b-live-uv-cache \
uv run --group evaluation --env-file .env \
jupyter nbconvert --execute --to notebook \
  notebooks/08b_retrieval_fusion_benchmark.ipynb \
  --output /tmp/08b-retrieval-fusion-final-review.ipynb \
  --ExecutePreprocessor.timeout=28800
```

Expected: exit 0, no setting rerun, complete reconciliation and zero-to-two
08b finalists.

- [ ] **Step 6: Independently verify evidence and non-mutation**

Run read-only checks that:

- recompute one BM25 score, one TF-IDF vector norm, one RRF case and one weighted
  fusion case from raw case evidence;
- recompute one overall metric and one category gate;
- verify exact artifact headers/counts/keys;
- verify the TF-IDF schema/name/fingerprints and 572 points;
- compare active collection before/after snapshots and production settings;
- parse the repository notebook for empty outputs/null counts;
- run `git diff --check` and inspect the complete diff.

- [ ] **Step 7: Write the implementation report with batch history**

Create `reports/phase_8_08b_retrieval_fusion_benchmark_implementation_report.md`
with exact sections:

```markdown
# Phase 8 — Notebook 08b Retrieval and Fusion Benchmark Implementation Report

## Scope and authorization
## Files changed
## Dependency and environment
## Canonical/08a prerequisite verification
## BM25 parameter calibration
## Tokenizer comparison
## TF-IDF collection evidence
## Operational batch/checkpoint history
## Exact 20-setting reconciliation
## Quality/category/bootstrap results
## Latency and resource results
## 08b finalists for 08d
## Production non-mutation proof
## Tests and live commands
## Failures, limitations and reviewer handoff
```

Record every batch's requested/completed/skipped/failed setting keys and cleanup
actions. Link the four artifacts and temporary executed notebook path. State
explicitly that no cutover occurred.

- [ ] **Step 8: Final verification and conditional commit gate**

Run:

```bash
cd /home/minhhieu/hue_rag
git diff --check
git status --short
```

If and only if the user separately authorizes Git operations:

```bash
git add \
  pyproject.toml uv.lock \
  backend/evaluation/sparse_benchmark.py \
  backend/tests/test_sparse_benchmark.py \
  notebooks/08b_retrieval_fusion_benchmark.ipynb \
  evaluation/results/phase8_sparse_manifest.json \
  evaluation/results/phase8_sparse_calibration.csv \
  evaluation/results/phase8_sparse_results.csv \
  evaluation/results/phase8_sparse_cases.jsonl \
  reports/phase_8_08b_retrieval_fusion_benchmark_implementation_report.md
git commit -m "feat: complete phase 8 retrieval fusion benchmark"
```

Never push without a separate explicit push authorization.

---

## Plan completion gate

Implementation is complete only when all deterministic tests pass, the exact
source notebook is clean, the real benchmark has reconciled across any number
of approved batches, the four durable artifacts agree, the TF-IDF review
collection validates at 572 points, production state is unchanged, and the
implementation report gives a reviewer enough exact evidence to reproduce the
decision.

An incomplete or failed batch is valid operational evidence but is not task
completion. Resume it under the exact manifest; never weaken the experiment to
manufacture a PASS.
