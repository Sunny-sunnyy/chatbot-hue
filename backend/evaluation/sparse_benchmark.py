"""Sparse and retrieval fusion benchmark orchestration for Phase 8 Notebook 08b."""
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import gc
import hashlib
import json
import math
import os
from pathlib import Path
import re
import tempfile
import time
import unicodedata
from typing import Callable, Sequence

import numpy as np
from qdrant_client import models

from core.schema import RetrievedDocument
from embedding.dense_benchmark import (
    ALL_DENSE_SETTINGS,
    DenseBenchmarkSetting,
    build_dense_runner,
)
from evaluation.embedding_benchmark import (
    BootstrapInterval,
    CaseMetrics,
    paired_bootstrap_intervals,
    snapshot_active_collection as _snap_active,
)
from evaluation.golden_dataset import GoldenCase, load_golden, V3_FULL_PATH
from retrieval.dense_retriever import DenseRetriever
from vectorstore.qdrant import DENSE_VECTOR_NAME

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_RESULTS_DIR = REPO_ROOT / "evaluation" / "results"
MANIFEST_FILENAME = "phase8_sparse_manifest.json"
CALIBRATION_FILENAME = "phase8_sparse_calibration.csv"
RESULTS_FILENAME = "phase8_sparse_results.csv"
CASES_FILENAME = "phase8_sparse_cases.jsonl"
CHUNKER_PATH = REPO_ROOT / "backend" / "ingestion" / "chunking" / "markdown_chunker.py"

UNICODE_TOKEN_PATTERN = re.compile(r"\w+", re.UNICODE)
TFIDF_FORMULA_VERSION = "phase8-tfidf-logtf-smoothedidf-l2-v1"
TFIDF_VECTOR_NAME = "tfidf"
GENERATOR_DEPTH = 30
FUSION_DEPTH = 10
FINAL_DEPTH = 5
RRF_K = 60
WEIGHTED_DENSE_WEIGHT = 0.6
WEIGHTED_SPARSE_WEIGHT = 0.4

Tokenizer = Callable[[str], list[str]]


def sanitize_error_message(exc: Exception) -> str:
    """Format exception as 'ExceptionType: safe bounded description' without raw payload or secrets."""
    exc_type = type(exc).__name__
    raw_msg = str(exc).lower()

    if "timeout" in raw_msg:
        detail = "operation timed out"
    elif "connection" in raw_msg or "connect" in raw_msg:
        detail = "connection failed"
    elif "not found" in raw_msg or "404" in raw_msg:
        detail = "resource not found"
    elif "memory" in raw_msg or "oom" in raw_msg:
        detail = "memory limit exceeded"
    elif "rate limit" in raw_msg or "429" in raw_msg:
        detail = "rate limit exceeded"
    elif "auth" in raw_msg or "permission" in raw_msg or "forbidden" in raw_msg or "401" in raw_msg or "403" in raw_msg:
        detail = "authentication or authorization failure"
    elif "dimension" in raw_msg or "shape" in raw_msg:
        detail = "vector dimension mismatch"
    elif "value" in raw_msg or "invalid" in raw_msg:
        detail = "invalid argument or value error"
    else:
        detail = "execution failure"

    return f"{exc_type}: {detail}"


def unicode_word_tokenize(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFC", text).lower()
    return UNICODE_TOKEN_PATTERN.findall(normalized)


def underthesea_word_tokenize(text: str) -> list[str]:
    import underthesea
    normalized = unicodedata.normalize("NFC", text)
    segmented = underthesea.word_tokenize(normalized, format="text")
    return UNICODE_TOKEN_PATTERN.findall(segmented.lower())


# ---------------------------------------------------------------------------
# BM25 Algorithm (Parity with backend/scoring/bm25.py)
# ---------------------------------------------------------------------------

class FullCorpusBM25:
    def __init__(
        self,
        chunks: Sequence[dict],
        tokenizer: Tokenizer,
        k1: float = 1.5,
        b: float = 0.75,
    ):
        self.chunks = list(chunks)
        self.tokenizer = tokenizer
        self.k1 = k1
        self.b = b
        self.n_docs = len(chunks)

        self.doc_tokens = [tokenizer(str(c["text"])) for c in self.chunks]
        self.doc_lens = [len(tokens) for tokens in self.doc_tokens]
        self.avgdl = sum(self.doc_lens) / self.n_docs if self.n_docs > 0 else 0.0

        df = Counter()
        self.doc_term_freqs = []
        for tokens in self.doc_tokens:
            tf = Counter(tokens)
            self.doc_term_freqs.append(tf)
            for term in tf:
                df[term] += 1

        self.idf = {}
        for term, freq in df.items():
            val = (self.n_docs - freq + 0.5) / (freq + 0.5)
            self.idf[term] = math.log(1.0 + val)

    def score_query_per_doc(self, query: str) -> list[float]:
        q_tokens = self.tokenizer(query)
        scores = [0.0] * self.n_docs
        if not q_tokens or self.n_docs == 0 or self.avgdl == 0.0:
            return scores

        for q_term in q_tokens:
            if q_term not in self.idf:
                continue
            idf_val = self.idf[q_term]
            for doc_idx, tf_map in enumerate(self.doc_term_freqs):
                tf = tf_map.get(q_term, 0)
                if tf <= 0:
                    continue
                d_len = self.doc_lens[doc_idx]
                denom = tf + self.k1 * (1.0 - self.b + self.b * (d_len / self.avgdl))
                num = tf * (self.k1 + 1.0)
                scores[doc_idx] += idf_val * (num / denom)
        return scores

    def search(self, query: str, limit: int = GENERATOR_DEPTH) -> list[RetrievedDocument]:
        if limit < 1:
            raise ValueError("limit must be positive")
        scores = self.score_query_per_doc(query)
        ranked_indices = [
            i for i, s in sorted(
                enumerate(scores),
                key=lambda x: (-x[1], str(self.chunks[x[0]]["metadata"]["chunk_id"])),
            )
            if s > 0.0
        ]
        results = []
        for idx in ranked_indices[:limit]:
            chunk = self.chunks[idx]
            cid = str(chunk["metadata"]["chunk_id"])
            meta = dict(chunk["metadata"])
            meta["bm25_score"] = float(scores[idx])
            results.append(
                RetrievedDocument(
                    id=cid,
                    score=float(scores[idx]),
                    text=chunk["text"],
                    metadata=meta,
                )
            )
        return results


# ---------------------------------------------------------------------------
# TF-IDF Sparse Vector Encoder & Collection
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TfidfSparseEncoder:
    tokenizer_key: str
    vocabulary: dict[str, int]
    idf: dict[str, float]
    document_vectors: tuple[models.SparseVector, ...]
    vocabulary_fingerprint: str
    tokenizer: Tokenizer

    @property
    def vocab_size(self) -> int:
        return len(self.vocabulary)

    @classmethod
    def fit(cls, chunks: Sequence[dict], tokenizer_key: str, tokenizer: Tokenizer):
        if tokenizer_key not in {"unicode_word", "underthesea_word"}:
            raise ValueError(f"unapproved tokenizer key: {tokenizer_key}")
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
    def _vector_from_counts(counts: Counter, vocabulary: dict[str, int], idf: dict[str, float]) -> models.SparseVector:
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

    def encode(self, text: str) -> models.SparseVector | None:
        counts = Counter(self.tokenizer(text))
        known = Counter({term: count for term, count in counts.items() if term in self.vocabulary and count > 0})
        if not known:
            return None
        return self._vector_from_counts(known, self.vocabulary, self.idf)


@dataclass(frozen=True)
class TfidfState:
    collection_name: str
    encoder: TfidfSparseEncoder
    status: str


def tfidf_collection_name(tokenizer_key: str, corpus_fingerprint: str) -> str:
    if not re.fullmatch(r"[a-z0-9_]+", tokenizer_key):
        raise ValueError(f"invalid tokenizer key: {tokenizer_key}")
    if not re.fullmatch(r"[0-9a-f]{64}", corpus_fingerprint):
        raise ValueError(f"invalid corpus fingerprint: {corpus_fingerprint}")
    return f"hue_rag_phase8_08b_tfidf_v1_{tokenizer_key}_{corpus_fingerprint[:12]}"


def _retrieved_document_from_sparse_point(point, score_key: str = "tfidf_score") -> RetrievedDocument:
    chunk_id = str(point.payload.get("chunk_id", point.id)) if point.payload else str(point.id)
    text = str(point.payload.get("text", "")) if point.payload else ""
    metadata = dict(point.payload) if point.payload else {}
    metadata[score_key] = float(point.score)
    return RetrievedDocument(
        id=chunk_id,
        score=float(point.score),
        text=text,
        metadata=metadata,
    )


def ensure_tfidf_collection(
    client,
    collection_name: str,
    chunks: Sequence[dict],
    encoder: TfidfSparseEncoder,
    corpus_fingerprint: str,
    *,
    allow_mutation: bool,
) -> str:
    from vectorstore.points import point_id_for

    if not client.collection_exists(collection_name):
        if not allow_mutation:
            raise PermissionError(
                f"Collection '{collection_name}' does not exist and ALLOW_EXPERIMENT_MUTATION is false"
            )
        client.create_collection(
            collection_name=collection_name,
            vectors_config={},
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
        return "created"

    # Existing collection validation
    info = client.get_collection(collection_name)
    if info.points_count != len(chunks):
        raise ValueError(
            f"Collection '{collection_name}' point count mismatch: expected {len(chunks)}, got {info.points_count}"
        )

    # Validate sparse vectors config
    sparse_cfg = getattr(info.config.params, "sparse_vectors", None)
    if sparse_cfg is None or TFIDF_VECTOR_NAME not in sparse_cfg:
        raise ValueError(
            f"Collection '{collection_name}' missing sparse vector config '{TFIDF_VECTOR_NAME}'"
        )

    # Scroll all points to check identity, provenance, and vectors
    scroll_result = client.scroll(
        collection_name=collection_name,
        limit=len(chunks) + 10,
        with_payload=True,
        with_vectors=True,
    )
    points = scroll_result[0]
    if len(points) != len(chunks):
        raise ValueError(
            f"Collection '{collection_name}' scroll count mismatch: expected {len(chunks)}, got {len(points)}"
        )

    payload_by_id = {str(p.payload.get("chunk_id")): p.payload for p in points if p.payload}
    vector_by_id = {
        str(p.payload.get("chunk_id")): (p.vector.get(TFIDF_VECTOR_NAME) if isinstance(p.vector, dict) else p.vector)
        for p in points if p.payload
    }

    for chunk in chunks:
        cid = str(chunk["metadata"]["chunk_id"])
        if cid not in payload_by_id:
            raise ValueError(f"Collection '{collection_name}' missing chunk_id: {cid}")
        payload = payload_by_id[cid]
        if payload.get("corpus_fingerprint") != corpus_fingerprint:
            raise ValueError(f"Collection '{collection_name}' corpus_fingerprint mismatch for chunk {cid}")
        if payload.get("tokenizer_key") != encoder.tokenizer_key:
            raise ValueError(f"Collection '{collection_name}' tokenizer_key mismatch for chunk {cid}")
        if payload.get("tfidf_formula_version") != TFIDF_FORMULA_VERSION:
            raise ValueError(f"Collection '{collection_name}' tfidf_formula_version mismatch for chunk {cid}")
        if payload.get("vocabulary_fingerprint") != encoder.vocabulary_fingerprint:
            raise ValueError(f"Collection '{collection_name}' vocabulary_fingerprint mismatch for chunk {cid}")
        if payload.get("text") != chunk["text"]:
            raise ValueError(f"Collection '{collection_name}' text mismatch for chunk {cid}")

        # Validate stored vector
        vec = vector_by_id.get(cid)
        if vec is None:
            raise ValueError(f"Collection '{collection_name}' missing vector for chunk {cid}")
        indices = vec.indices if hasattr(vec, "indices") else (vec.get("indices", []) if isinstance(vec, dict) else [])
        values = vec.values if hasattr(vec, "values") else (vec.get("values", []) if isinstance(vec, dict) else [])
        if not indices or not values or len(indices) != len(values):
            raise ValueError(f"Collection '{collection_name}' invalid sparse vector for chunk {cid}")
        if indices != sorted(indices) or len(set(indices)) != len(indices):
            raise ValueError(f"Collection '{collection_name}' unsorted or duplicate sparse indices for chunk {cid}")
        if not all(math.isfinite(v) and v != 0.0 for v in values):
            raise ValueError(f"Collection '{collection_name}' non-finite or zero sparse values for chunk {cid}")
        l2 = sum(v * v for v in values)
        if not math.isclose(l2, 1.0, rel_tol=1e-3, abs_tol=1e-3):
            raise ValueError(f"Collection '{collection_name}' sparse vector L2 norm {l2} != 1.0 for chunk {cid}")

    return "existing"


def build_or_validate_tfidf(
    client,
    chunks: Sequence[dict],
    tokenizer: Tokenizer,
    tokenizer_key: str,
    corpus_fingerprint: str | None = None,
    *,
    expected_active_snapshot: dict[str, object] | None = None,
    allow_mutation: bool | None = None,
) -> TfidfState:
    if allow_mutation is None:
        allow_mutation = os.environ.get("ALLOW_EXPERIMENT_MUTATION", "").lower() in {"1", "true", "yes"}

    if expected_active_snapshot is not None:
        snap_before = snapshot_active_collection(client)
        if snap_before != expected_active_snapshot:
            raise ValueError(
                f"Active production snapshot changed before TF-IDF stage: expected {expected_active_snapshot}, got {snap_before}"
            )

    fp = corpus_fingerprint or fingerprint_corpus(chunks)
    encoder = TfidfSparseEncoder.fit(chunks, tokenizer_key, tokenizer)
    coll_name = tfidf_collection_name(tokenizer_key, fp)

    status = ensure_tfidf_collection(
        client,
        coll_name,
        chunks,
        encoder,
        fp,
        allow_mutation=allow_mutation,
    )

    if expected_active_snapshot is not None:
        snap_after = snapshot_active_collection(client)
        if snap_after != expected_active_snapshot:
            raise ValueError(
                f"Active production snapshot changed after TF-IDF stage: expected {expected_active_snapshot}, got {snap_after}"
            )

    return TfidfState(collection_name=coll_name, encoder=encoder, status=status)


def query_tfidf(
    client,
    collection_name: str,
    encoder: TfidfSparseEncoder,
    query: str,
    limit: int = GENERATOR_DEPTH,
) -> list[RetrievedDocument]:
    if limit < 1:
        raise ValueError("limit must be positive")
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


# ---------------------------------------------------------------------------
# Fusion Algorithms (RRF & Min-Max Weighted)
# ---------------------------------------------------------------------------

def rrf_fuse(
    dense: list[RetrievedDocument],
    sparse: list[RetrievedDocument],
    limit: int = 10,
    rrf_k: int = 60,
) -> list[RetrievedDocument]:
    if limit < 1:
        raise ValueError("limit must be positive")
    if rrf_k != 60:
        raise ValueError(f"rrf_k must be exact 60, got {rrf_k}")
    if len({d.id for d in dense}) != len(dense):
        raise ValueError("Duplicate document IDs in dense results")
    if len({d.id for d in sparse}) != len(sparse):
        raise ValueError("Duplicate document IDs in sparse results")
    if not all(math.isfinite(d.score) for d in dense) or not all(math.isfinite(d.score) for d in sparse):
        raise ValueError("Non-finite scores in input documents")

    entries: dict[str, dict] = {}

    for rank, doc in enumerate(dense, start=1):
        if doc.id not in entries:
            entries[doc.id] = {
                "doc": doc,
                "dense_rank": rank,
                "dense_score": doc.score,
                "sparse_rank": None,
                "sparse_score": None,
                "rrf_score": 0.0,
            }
        entries[doc.id]["rrf_score"] += 1.0 / (rrf_k + rank)

    for rank, doc in enumerate(sparse, start=1):
        if doc.id not in entries:
            entries[doc.id] = {
                "doc": doc,
                "dense_rank": None,
                "dense_score": None,
                "sparse_rank": rank,
                "sparse_score": doc.score,
                "rrf_score": 0.0,
            }
        else:
            entries[doc.id]["sparse_rank"] = rank
            entries[doc.id]["sparse_score"] = doc.score
        entries[doc.id]["rrf_score"] += 1.0 / (rrf_k + rank)

    sorted_items = sorted(
        entries.values(),
        key=lambda item: (-item["rrf_score"], item["doc"].id),
    )

    fused_docs = []
    for item in sorted_items[:limit]:
        base_doc = item["doc"]
        metadata = dict(base_doc.metadata) if base_doc.metadata else {}
        metadata.update({
            "dense_rank": item["dense_rank"],
            "dense_score": item["dense_score"],
            "sparse_rank": item["sparse_rank"],
            "sparse_score": item["sparse_score"],
            "rrf_score": item["rrf_score"],
        })
        fused_docs.append(
            RetrievedDocument(
                id=base_doc.id,
                score=float(item["rrf_score"]),
                text=base_doc.text,
                metadata=metadata,
            )
        )
    return fused_docs


def _min_max_by_id(docs: list[RetrievedDocument]) -> dict[str, float]:
    if not docs:
        return {}
    scores = [doc.score for doc in docs]
    min_score, max_score = min(scores), max(scores)
    if math.isclose(min_score, max_score) or max_score == min_score:
        return {doc.id: 0.0 for doc in docs}
    return {doc.id: (doc.score - min_score) / (max_score - min_score) for doc in docs}


def weighted_fuse(
    dense: list[RetrievedDocument],
    sparse: list[RetrievedDocument],
    limit: int = 10,
    dense_weight: float = 0.6,
    sparse_weight: float = 0.4,
) -> list[RetrievedDocument]:
    if limit < 1:
        raise ValueError("limit must be positive")
    if dense_weight < 0.0 or sparse_weight < 0.0:
        raise ValueError("Weights must be non-negative")
    if not math.isclose(dense_weight + sparse_weight, 1.0):
        raise ValueError("Weights must sum to 1.0")
    if len({d.id for d in dense}) != len(dense):
        raise ValueError("Duplicate document IDs in dense results")
    if len({d.id for d in sparse}) != len(sparse):
        raise ValueError("Duplicate document IDs in sparse results")
    if not all(math.isfinite(d.score) for d in dense) or not all(math.isfinite(d.score) for d in sparse):
        raise ValueError("Non-finite scores in input documents")

    dense_norm = _min_max_by_id(dense)
    sparse_norm = _min_max_by_id(sparse)

    docs_by_id: dict[str, RetrievedDocument] = {}
    dense_by_id: dict[str, tuple[int, float]] = {}
    sparse_by_id: dict[str, tuple[int, float]] = {}

    for rank, doc in enumerate(dense, start=1):
        docs_by_id[doc.id] = doc
        dense_by_id[doc.id] = (rank, doc.score)

    for rank, doc in enumerate(sparse, start=1):
        if doc.id not in docs_by_id:
            docs_by_id[doc.id] = doc
        sparse_by_id[doc.id] = (rank, doc.score)

    fused_items = []
    for chunk_id, doc in docs_by_id.items():
        norm_d = dense_norm.get(chunk_id, 0.0)
        norm_s = sparse_norm.get(chunk_id, 0.0)
        fused_score = dense_weight * norm_d + sparse_weight * norm_s
        d_rank, d_score = dense_by_id.get(chunk_id, (None, None))
        s_rank, s_score = sparse_by_id.get(chunk_id, (None, None))
        fused_items.append({
            "doc": doc,
            "fused_score": fused_score,
            "normalized_dense": norm_d,
            "normalized_sparse": norm_s,
            "dense_rank": d_rank,
            "dense_score": d_score,
            "sparse_rank": s_rank,
            "sparse_score": s_score,
        })

    sorted_items = sorted(
        fused_items,
        key=lambda item: (-item["fused_score"], item["doc"].id),
    )

    fused_docs = []
    for item in sorted_items[:limit]:
        base_doc = item["doc"]
        metadata = dict(base_doc.metadata) if base_doc.metadata else {}
        metadata.update({
            "dense_rank": item["dense_rank"],
            "dense_score": item["dense_score"],
            "normalized_dense": item["normalized_dense"],
            "sparse_rank": item["sparse_rank"],
            "sparse_score": item["sparse_score"],
            "normalized_sparse": item["normalized_sparse"],
            "fused_score": item["fused_score"],
        })
        fused_docs.append(
            RetrievedDocument(
                id=base_doc.id,
                score=float(item["fused_score"]),
                text=base_doc.text,
                metadata=metadata,
            )
        )
    return fused_docs


# ---------------------------------------------------------------------------
# Metrics & Guardrails
# ---------------------------------------------------------------------------

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


def _extract_case_relevant_keys(case) -> tuple[tuple[str, str], ...]:
    if hasattr(case, "evidence") and isinstance(case.evidence, dict):
        return tuple(
            (source, section)
            for source, sections in case.evidence.items()
            for section in sections
        )
    if hasattr(case, "expected_evidence"):
        return tuple((e.source, e.section) for e in case.expected_evidence)
    if isinstance(case, dict):
        if "evidence" in case and isinstance(case["evidence"], dict):
            return tuple(
                (source, section)
                for source, sections in case["evidence"].items()
                for section in sections
            )
        if "expected_evidence" in case:
            return tuple((e["source"], e["section"]) for e in case["expected_evidence"])
    return ()


def _case_query(case) -> str:
    if hasattr(case, "question"):
        return case.question
    if hasattr(case, "query"):
        return case.query
    if isinstance(case, dict):
        return case.get("question") or case.get("query") or ""
    return ""


def score_at_depth(
    case,
    docs: list[RetrievedDocument],
    depth: int,
) -> DepthCaseMetrics:
    relevant_keys = _extract_case_relevant_keys(case)

    sliced = docs[:depth]
    ranked_keys = tuple(
        (doc.metadata.get("source", ""), doc.metadata.get("section", ""))
        for doc in sliced
    )

    if not relevant_keys:
        return DepthCaseMetrics(
            case_id=case.case_id if hasattr(case, "case_id") else case.get("case_id", ""),
            category=case.category if hasattr(case, "category") else case.get("category", ""),
            depth=depth,
            recall=0.0,
            mrr=0.0,
            ndcg=0.0,
            hit=False,
            relevant_keys=relevant_keys,
            ranked_keys=ranked_keys,
        )

    matched_keys = set()
    first_rank = None
    dcg = 0.0

    for rank, key in enumerate(ranked_keys, start=1):
        if key in relevant_keys and key not in matched_keys:
            matched_keys.add(key)
            if first_rank is None:
                first_rank = rank
            dcg += 1.0 / math.log2(rank + 1)

    hit = len(matched_keys) > 0
    recall = len(matched_keys) / len(relevant_keys)
    mrr = (1.0 / first_rank) if first_rank is not None else 0.0

    ideal_hits = min(len(relevant_keys), depth)
    idcg = sum(1.0 / math.log2(i + 1) for i in range(1, ideal_hits + 1))
    ndcg = (dcg / idcg) if idcg > 0.0 else 0.0

    return DepthCaseMetrics(
        case_id=case.case_id if hasattr(case, "case_id") else case.get("case_id", ""),
        category=case.category if hasattr(case, "category") else case.get("category", ""),
        depth=depth,
        recall=recall,
        mrr=mrr,
        ndcg=ndcg,
        hit=hit,
        relevant_keys=relevant_keys,
        ranked_keys=ranked_keys,
    )


def evaluate_depth_category_guardrails(
    control_cases: list[DepthCaseMetrics],
    candidate_cases: list[DepthCaseMetrics],
    control_ndcg5_cases: list[DepthCaseMetrics] | None = None,
    candidate_ndcg5_cases: list[DepthCaseMetrics] | None = None,
) -> tuple[bool, float]:
    if len(control_cases) != len(candidate_cases):
        raise ValueError("control and candidate case lists must have same length")
    if not control_cases:
        return True, 0.0

    ctrl_by_id = {c.case_id: c for c in control_cases}
    cand_by_id = {c.case_id: c for c in candidate_cases}
    if set(ctrl_by_id) != set(cand_by_id):
        raise ValueError("case IDs do not match between control and candidate")

    # If separate depth-5 cases provided for nDCG tiebreaker (e.g. calibration)
    if control_ndcg5_cases is not None and candidate_ndcg5_cases is not None:
        ctrl_mean_ndcg = sum(c.ndcg for c in control_ndcg5_cases) / len(control_ndcg5_cases)
        cand_mean_ndcg = sum(c.ndcg for c in candidate_ndcg5_cases) / len(candidate_ndcg5_cases)
    else:
        ctrl_mean_ndcg = sum(c.ndcg for c in control_cases) / len(control_cases)
        cand_mean_ndcg = sum(c.ndcg for c in candidate_cases) / len(candidate_cases)
    delta_ndcg = cand_mean_ndcg - ctrl_mean_ndcg

    if len(control_cases) >= 6:
        ctrl_hits = sum(1 for c in control_cases if c.hit)
        cand_hits = sum(1 for c in candidate_cases if c.hit)
        if cand_hits < ctrl_hits:
            return False, delta_ndcg
        if cand_hits == ctrl_hits and delta_ndcg < -0.02:
            return False, delta_ndcg
        return True, delta_ndcg
    else:
        for cid, ctrl_metric in ctrl_by_id.items():
            if ctrl_metric.hit and not cand_by_id[cid].hit:
                return False, delta_ndcg
        return True, delta_ndcg


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


def select_family_finalist(
    results: list[FinalistEvidence],
    dense_controls: dict[str, FinalistEvidence],
    family: str,
) -> FinalistEvidence | None:
    candidates = [r for r in results if r.sparse_family == family]
    eligible = []
    for cand in candidates:
        control = dense_controls.get(cand.dense_setting_key)
        if control is None:
            continue
        if cand.status != "completed" or cand.successful_repetitions < 3:
            continue
        if cand.fusion_recall_at_10 < control.fusion_recall_at_10:
            continue
        if cand.recall_at_5 < control.recall_at_5 - 0.005:
            continue
        if not cand.all_category_guardrails_pass:
            continue
        if cand.warm_total_p95_ms > 2.0 * control.warm_total_p95_ms:
            continue
        eligible.append(cand)

    if not eligible:
        return None

    sorted_eligible = sorted(
        eligible,
        key=lambda c: (-c.recall_at_5, -c.ndcg_at_5, c.warm_total_p95_ms),
    )
    return sorted_eligible[0]


# ---------------------------------------------------------------------------
# Canonical Inputs, Fingerprints & 08a Provenance
# ---------------------------------------------------------------------------

def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def fingerprint_corpus(chunks: Sequence[dict]) -> str:
    canonical = [
        {"chunk_id": str(c["metadata"]["chunk_id"]), "text": str(c["text"]), "metadata": dict(c["metadata"])}
        for c in chunks
    ]
    canonical.sort(key=lambda x: x["chunk_id"])
    encoded = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def fingerprint_golden(cases: Sequence[GoldenCase]) -> str:
    canonical = [
        {
            "case_id": c.case_id,
            "category": c.category,
            "question": c.question,
            "evidence": {k: sorted(v) for k, v in sorted(c.evidence.items())},
        }
        for c in cases
    ]
    canonical.sort(key=lambda x: x["case_id"])
    encoded = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def fingerprint_chunker_code(path: Path = CHUNKER_PATH) -> str:
    return _hash_file(path)


@dataclass(frozen=True)
class DensePrerequisite:
    dense_setting_key: str
    model_id: str
    model_revision: str
    dimension: int
    collection_name: str
    point_count: int
    csv_recall_at_5: float
    csv_ndcg_at_5: float
    csv_mrr_at_5: float
    csv_p95_latency_ms: float


@dataclass(frozen=True)
class SparseBenchmarkInputs:
    cases: list[GoldenCase]
    chunks: list[dict]
    client: object
    settings: dict
    corpus_fingerprint: str
    golden_fingerprint: str
    chunker_fingerprint: str


def load_sparse_benchmark_inputs(root_dir: Path | None = None) -> SparseBenchmarkInputs:
    from core.settings_loader import load_settings
    from vectorstore.qdrant import client_from_settings
    from ingestion.chunking.markdown_chunker import chunk_foods_markdown
    from vectorstore.points import validate_chunks

    r_dir = root_dir or REPO_ROOT
    golden_path = V3_FULL_PATH
    chunker_path = r_dir / "backend" / "ingestion" / "chunking" / "markdown_chunker.py"

    if not golden_path.exists():
        raise FileNotFoundError(f"golden dataset not found at {golden_path}")

    chunks = chunk_foods_markdown()
    chunk_ids = validate_chunks(chunks)

    if len(chunk_ids) != 572:
        raise ValueError(f"Expected 572 canonical chunks, got {len(chunk_ids)}")

    cases = load_golden(golden_path)
    if len(cases) != 45:
        raise ValueError(f"Expected 45 Golden Dataset V3 cases, got {len(cases)}")

    corpus_fp = fingerprint_corpus(chunks)
    golden_fp = fingerprint_golden(cases)
    chunker_fp = fingerprint_chunker_code(chunker_path)

    settings = load_settings()
    client = client_from_settings(settings)

    return SparseBenchmarkInputs(
        cases=cases,
        chunks=chunks,
        client=client,
        settings=settings,
        corpus_fingerprint=corpus_fp,
        golden_fingerprint=golden_fp,
        chunker_fingerprint=chunker_fp,
    )


def validate_08a_prerequisites(inputs: SparseBenchmarkInputs) -> tuple[DensePrerequisite, ...]:
    import csv
    from evaluation.embedding_benchmark import ALL_DENSE_SETTINGS, EMBEDDING_RESULTS_PATH, CSV_COLUMNS

    if not EMBEDDING_RESULTS_PATH.exists():
        raise FileNotFoundError(f"08a results CSV not found at {EMBEDDING_RESULTS_PATH}")

    with open(EMBEDDING_RESULTS_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or []) != CSV_COLUMNS:
            raise ValueError(f"08a results CSV header mismatch at {EMBEDDING_RESULTS_PATH}")
        rows = list(reader)

    overall_rows = {
        r["setting_key"]: r for r in rows if r.get("category") == "overall"
    }

    prerequisites = []
    for dense_setting in ALL_DENSE_SETTINGS:
        key = dense_setting.setting_key
        if key not in overall_rows:
            raise ValueError(f"08a results missing overall row for setting '{key}'")
        row = overall_rows[key]
        if row.get("status") != "completed":
            raise ValueError(f"08a setting '{key}' status is '{row.get('status')}', expected 'completed'")
        if int(row.get("successful_repetitions", 0)) < 3:
            raise ValueError(f"08a setting '{key}' successful_repetitions < 3")
        if row.get("model_id") != dense_setting.model_id:
            raise ValueError(f"08a CSV model_id mismatch for '{key}': expected {dense_setting.model_id}, got {row.get('model_id')}")
        if row.get("model_revision") != dense_setting.revision:
            raise ValueError(f"08a CSV model_revision mismatch for '{key}': expected {dense_setting.revision}, got {row.get('model_revision')}")
        if int(row.get("dimension", 0)) != dense_setting.dimension:
            raise ValueError(f"08a CSV dimension mismatch for '{key}': expected {dense_setting.dimension}, got {row.get('dimension')}")
        if row.get("collection_name") != dense_setting.collection_name:
            raise ValueError(f"08a CSV collection_name mismatch for '{key}': expected {dense_setting.collection_name}, got {row.get('collection_name')}")

        coll_name = dense_setting.collection_name
        if not inputs.client.collection_exists(coll_name):
            raise ValueError(f"08a collection '{coll_name}' does not exist in Qdrant")

        info = inputs.client.get_collection(coll_name)
        if info.points_count != len(inputs.chunks):
            raise ValueError(
                f"08a collection '{coll_name}' point count mismatch: expected {len(inputs.chunks)}, got {info.points_count}"
            )

        # Validate live vectors config
        vectors_cfg = getattr(info.config.params, "vectors", None)
        if isinstance(vectors_cfg, dict):
            if DENSE_VECTOR_NAME not in vectors_cfg:
                raise ValueError(f"08a collection '{coll_name}' missing dense vector '{DENSE_VECTOR_NAME}'")
            vparams = vectors_cfg[DENSE_VECTOR_NAME]
        else:
            vparams = vectors_cfg

        if vparams.size != dense_setting.dimension:
            raise ValueError(f"08a collection '{coll_name}' dimension mismatch: expected {dense_setting.dimension}, got {vparams.size}")
        if str(vparams.distance).lower() != "cosine" and vparams.distance != models.Distance.COSINE:
            raise ValueError(f"08a collection '{coll_name}' distance mismatch: expected Cosine, got {vparams.distance}")

        scroll_res = inputs.client.scroll(
            collection_name=coll_name,
            limit=len(inputs.chunks) + 10,
            with_payload=True,
            with_vectors=False,
        )
        points = scroll_res[0]
        if len(points) != len(inputs.chunks):
            raise ValueError(f"08a collection '{coll_name}' scroll count mismatch")

        payload_by_id = {str(p.payload.get("chunk_id")): p.payload for p in points if p.payload}
        for chunk in inputs.chunks:
            cid = str(chunk["metadata"]["chunk_id"])
            if cid not in payload_by_id:
                raise ValueError(f"08a collection '{coll_name}' missing chunk '{cid}'")
            if payload_by_id[cid].get("text") != chunk["text"]:
                raise ValueError(f"08a collection '{coll_name}' text mismatch for chunk '{cid}'")

        prereq = DensePrerequisite(
            dense_setting_key=key,
            model_id=dense_setting.model_id,
            model_revision=dense_setting.revision,
            dimension=dense_setting.dimension,
            collection_name=coll_name,
            point_count=info.points_count,
            csv_recall_at_5=float(row.get("recall_at_5", 0.0)),
            csv_ndcg_at_5=float(row.get("ndcg_at_5", 0.0)),
            csv_mrr_at_5=float(row.get("mrr_at_5", 0.0)),
            csv_p95_latency_ms=float(row.get("warm_total_p95_ms", 0.0)),
        )
        prerequisites.append(prereq)

    return tuple(prerequisites)


def snapshot_active_collection(inputs: SparseBenchmarkInputs | object) -> dict[str, object]:
    client = inputs.client if hasattr(inputs, "client") else (inputs.get("client") if isinstance(inputs, dict) else inputs)
    settings = inputs.settings if hasattr(inputs, "settings") else (inputs.get("settings") if isinstance(inputs, dict) else {})
    if isinstance(settings, dict) and "vector_database" in settings:
        name = str(settings["vector_database"].get("collection_name", "hue_foods_e5_small_384"))
    else:
        name = "hue_foods_e5_small_384"
    info = client.get_collection(name)
    vectors_conf = info.config.params.vectors
    dense_params = vectors_conf.get(DENSE_VECTOR_NAME) if isinstance(vectors_conf, dict) else (vectors_conf if hasattr(vectors_conf, "size") else None)
    sparse_conf = info.config.params.sparse_vectors or {}

    return {
        "collection_name": name,
        "points_count": info.points_count,
        "dense_vector_name": DENSE_VECTOR_NAME,
        "dense_size": dense_params.size if dense_params else None,
        "dense_distance": str(dense_params.distance) if dense_params else None,
        "sparse_vector_names": sorted(list(sparse_conf.keys())),
    }


# ---------------------------------------------------------------------------
# Atomic Persistence & Checkpointing
# ---------------------------------------------------------------------------

CALIBRATION_COLUMNS = (
    "experiment_version",
    "calibration_stage",
    "setting_key",
    "category",
    "tokenizer_key",
    "k1",
    "b",
    "status",
    "error",
    "case_count",
    "hit_case_count",
    "recall_at_30",
    "mrr_at_5",
    "ndcg_at_5",
    "successful_repetitions",
    "ranking_stable",
    "build_ms",
    "warm_total_p50_ms",
    "warm_total_p95_ms",
    "observed_peak_rss_mb",
    "delta_recall_at_30",
    "delta_mrr_at_5",
    "delta_ndcg_at_5",
    "category_guardrail_pass",
    "all_category_guardrails_pass",
    "selected",
    "selection_reason",
)

RESULT_COLUMNS = (
    "experiment_version",
    "setting_order",
    "setting_key",
    "setting_label",
    "category",
    "path",
    "dense_setting_key",
    "sparse_family",
    "fusion_method",
    "status",
    "error",
    "case_count",
    "hit_case_count",
    "successful_repetitions",
    "ranking_stable",
    "dense_recall_at_30",
    "sparse_recall_at_30",
    "candidate_union_recall",
    "fusion_recall_at_10",
    "recall_at_5",
    "mrr_at_5",
    "ndcg_at_5",
    "dense_query_p50_ms",
    "dense_query_p95_ms",
    "sparse_query_p50_ms",
    "sparse_query_p95_ms",
    "fusion_p50_ms",
    "fusion_p95_ms",
    "warm_total_p50_ms",
    "warm_total_p95_ms",
    "build_ms",
    "observed_peak_rss_mb",
    "delta_fusion_recall_at_10",
    "delta_recall_at_5",
    "delta_mrr_at_5",
    "delta_ndcg_at_5",
    "recall_ci_lower",
    "recall_ci_upper",
    "mrr_ci_lower",
    "mrr_ci_upper",
    "ndcg_ci_lower",
    "ndcg_ci_upper",
    "category_guardrail_pass",
    "all_category_guardrails_pass",
    "fusion_recall_gate",
    "final_recall_gate",
    "latency_gate",
    "complete_gate",
    "finalist_eligible",
    "finalist_selected",
)

CASE_RECORD_FIELDS = (
    "experiment_version",
    "setting_order",
    "setting_key",
    "case_id",
    "category",
    "status",
    "error",
    "relevant_source_sections",
    "derived_relevant_chunk_ids",
    "successful_repetitions",
    "ranking_stable",
    "dense_top_30",
    "sparse_top_30",
    "candidate_union_chunk_ids",
    "fusion_top_10",
    "final_top_5",
    "dense_recall_at_30",
    "sparse_recall_at_30",
    "candidate_union_recall",
    "fusion_recall_at_10",
    "recall_at_5",
    "mrr_at_5",
    "ndcg_at_5",
    "latency_by_repetition_ms",
)


@dataclass(frozen=True)
class ExperimentManifest:
    schema_version: str
    experiment_version: str
    immutable_identity: dict[str, object]
    batch_history: tuple[dict[str, object], ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "experiment_version": self.experiment_version,
            "immutable_identity": self.immutable_identity,
            "batch_history": list(self.batch_history),
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]):
        return cls(
            schema_version=str(data["schema_version"]),
            experiment_version=str(data["experiment_version"]),
            immutable_identity=dict(data["immutable_identity"]),
            batch_history=tuple(dict(x) for x in data.get("batch_history", [])),
        )


@dataclass(frozen=True)
class CheckpointState:
    manifest: ExperimentManifest
    completed_setting_keys: tuple[str, ...]
    calibration_rows: tuple[dict[str, object], ...]
    result_rows: tuple[dict[str, object], ...]
    case_records: tuple[dict[str, object], ...]


def write_manifest_atomic(manifest: ExperimentManifest, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as tf:
        json.dump(manifest.to_dict(), tf, ensure_ascii=False, indent=2)
        tf.write("\n")
        tf.flush()
        os.fsync(tf.fileno())
        temp_name = tf.name
    os.replace(temp_name, path)


def upsert_calibration_rows(new_rows: list[dict[str, object]], path: Path):
    import csv
    path.parent.mkdir(parents=True, exist_ok=True)
    existing_rows = []
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            existing_rows = list(csv.DictReader(f))

    rows_by_key = {
        (r["calibration_stage"], r["setting_key"], r["category"]): r
        for r in existing_rows
    }
    for r in new_rows:
        rows_by_key[(r["calibration_stage"], r["setting_key"], r["category"])] = {k: str(r.get(k, "")) for k in CALIBRATION_COLUMNS}

    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8", newline="") as tf:
        writer = csv.DictWriter(tf, fieldnames=CALIBRATION_COLUMNS)
        writer.writeheader()
        for r in rows_by_key.values():
            writer.writerow(r)
        tf.flush()
        os.fsync(tf.fileno())
        temp_name = tf.name
    os.replace(temp_name, path)


def upsert_result_rows(new_rows: list[dict[str, object]], path: Path):
    import csv
    path.parent.mkdir(parents=True, exist_ok=True)
    existing_rows = []
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            existing_rows = list(csv.DictReader(f))

    rows_by_key = {
        (r["setting_key"], r["category"]): r
        for r in existing_rows
    }
    for r in new_rows:
        rows_by_key[(r["setting_key"], r["category"])] = {k: str(r.get(k, "")) for k in RESULT_COLUMNS}

    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8", newline="") as tf:
        writer = csv.DictWriter(tf, fieldnames=RESULT_COLUMNS)
        writer.writeheader()
        for r in rows_by_key.values():
            writer.writerow(r)
        tf.flush()
        os.fsync(tf.fileno())
        temp_name = tf.name
    os.replace(temp_name, path)


def upsert_case_records(new_records: list[dict[str, object]], path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    existing_records = []
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    existing_records.append(json.loads(line))

    records_by_key = {
        (r["setting_key"], r["case_id"]): r
        for r in existing_records
    }
    for r in new_records:
        records_by_key[(r["setting_key"], r["case_id"])] = r

    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as tf:
        for r in records_by_key.values():
            tf.write(json.dumps(r, ensure_ascii=False) + "\n")
        tf.flush()
        os.fsync(tf.fileno())
        temp_name = tf.name
    os.replace(temp_name, path)


def load_checkpoint(manifest: ExperimentManifest, results_dir: Path | None = None) -> CheckpointState:
    import csv
    r_dir = results_dir or DEFAULT_RESULTS_DIR
    calib_path = r_dir / CALIBRATION_FILENAME
    res_path = r_dir / RESULTS_FILENAME
    cases_path = r_dir / CASES_FILENAME

    calib_rows = []
    if calib_path.exists():
        with open(calib_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            if headers != list(CALIBRATION_COLUMNS):
                raise ValueError(
                    f"Calibration CSV headers mismatch or reordered: expected {list(CALIBRATION_COLUMNS)}, got {headers}"
                )
            f.seek(0)
            dict_reader = csv.DictReader(f)
            seen_calib_keys = set()
            for r in dict_reader:
                if r.get("experiment_version") != manifest.experiment_version:
                    raise ValueError(
                        f"Calibration row experiment_version '{r.get('experiment_version')}' != '{manifest.experiment_version}'"
                    )
                key = (r.get("calibration_stage"), r.get("setting_key"), r.get("category"))
                if key in seen_calib_keys:
                    raise ValueError(f"Duplicate calibration key: {key}")
                seen_calib_keys.add(key)
                calib_rows.append(r)

    result_rows = []
    if res_path.exists():
        with open(res_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            if headers != list(RESULT_COLUMNS):
                raise ValueError(
                    f"Result CSV headers mismatch or reordered: expected {list(RESULT_COLUMNS)}, got {headers}"
                )
            f.seek(0)
            dict_reader = csv.DictReader(f)
            seen_res_keys = set()
            for r in dict_reader:
                if r.get("experiment_version") != manifest.experiment_version:
                    raise ValueError(
                        f"Result row experiment_version '{r.get('experiment_version')}' != '{manifest.experiment_version}'"
                    )
                key = (r.get("setting_key"), r.get("category"))
                if key in seen_res_keys:
                    raise ValueError(f"Duplicate result key: {key}")
                seen_res_keys.add(key)
                result_rows.append(r)

    case_records = []
    if cases_path.exists():
        seen_case_keys = set()
        with open(cases_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    c_dict = json.loads(line)
                except json.JSONDecodeError as err:
                    raise ValueError(f"Malformed JSON in cases file line {line_no}: {err}")
                if not isinstance(c_dict, dict):
                    raise ValueError(f"Case record line {line_no} is not a JSON object")
                if c_dict.get("experiment_version") != manifest.experiment_version:
                    raise ValueError(
                        f"Case record line {line_no} experiment_version '{c_dict.get('experiment_version')}' != '{manifest.experiment_version}'"
                    )
                missing_fields = set(CASE_RECORD_FIELDS) - set(c_dict.keys())
                if missing_fields:
                    raise ValueError(f"Case record line {line_no} missing fields: {missing_fields}")
                key = (c_dict.get("setting_key"), c_dict.get("case_id"))
                if key in seen_case_keys:
                    raise ValueError(f"Duplicate case record key: {key}")
                seen_case_keys.add(key)
                case_records.append(c_dict)

    # Determine completed setting keys: must have 10 result rows (overall + 9 categories) all completed with 3 reps, AND exactly 45 completed case records with 3 reps
    completed_keys = []
    res_by_setting: dict[str, list[dict]] = {}
    for r in result_rows:
        s_key = r.get("setting_key")
        if s_key:
            res_by_setting.setdefault(s_key, []).append(r)

    cases_by_setting: dict[str, list[dict]] = {}
    for c in case_records:
        s_key = c.get("setting_key")
        if s_key:
            cases_by_setting.setdefault(s_key, []).append(c)

    for s_key, s_rows in res_by_setting.items():
        if len(s_rows) == 10 and all(
            r.get("status") == "completed" and str(r.get("successful_repetitions", "")).strip() == "3"
            for r in s_rows
        ):
            s_cases = cases_by_setting.get(s_key, [])
            if len(s_cases) == 45 and all(
                c.get("status") == "completed" and int(c.get("successful_repetitions", 0)) == 3
                for c in s_cases
            ):
                completed_keys.append(s_key)

    return CheckpointState(
        manifest=manifest,
        completed_setting_keys=tuple(completed_keys),
        calibration_rows=tuple(calib_rows),
        result_rows=tuple(result_rows),
        case_records=tuple(case_records),
    )


# ---------------------------------------------------------------------------
# Calibration Orchestration (BM25 Parameters & Tokenizers)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Bm25ParameterSetting:
    setting_key: str
    k1: float
    b: float


BM25_SETTINGS = (
    Bm25ParameterSetting("baseline", 1.5, 0.75),
    Bm25ParameterSetting("k1_low", 1.2, 0.75),
    Bm25ParameterSetting("k1_high", 1.8, 0.75),
    Bm25ParameterSetting("b_low", 1.5, 0.5),
    Bm25ParameterSetting("b_high", 1.5, 1.0),
)


@dataclass(frozen=True)
class CalibrationSelection:
    stage: str
    selected_setting_key: str
    selection_reason: str
    all_rows: tuple[dict[str, object], ...]


@dataclass(frozen=True)
class SelectedLexicalContract:
    bm25_setting_key: str
    k1: float
    b: float
    tokenizer_key: str
    tokenizer: Tokenizer
    parameter_selection_reason: str
    tokenizer_selection_reason: str


def _evaluate_bm25_setting(
    inputs: SparseBenchmarkInputs,
    tokenizer: Tokenizer,
    tokenizer_key: str,
    k1: float,
    b: float,
    setting_key: str,
    stage: str,
) -> tuple[list[DepthCaseMetrics], list[DepthCaseMetrics], float, float, float, float, bool]:
    import tracemalloc
    tracemalloc.start()
    t0 = time.perf_counter()
    bm25 = FullCorpusBM25(inputs.chunks, tokenizer, k1=k1, b=b)
    build_ms = (time.perf_counter() - t0) * 1000.0
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_rss_mb = peak_bytes / (1024.0 * 1024.0)

    # Discarded warmup query
    if inputs.cases:
        bm25.search(_case_query(inputs.cases[0]), limit=GENERATOR_DEPTH)

    rankings_by_rep: list[dict[str, tuple[str, ...]]] = []
    latencies_ms: list[float] = []

    for _ in range(3):
        rep_ranks = {}
        for case in inputs.cases:
            t_case = time.perf_counter()
            top30 = bm25.search(_case_query(case), limit=GENERATOR_DEPTH)
            lat = (time.perf_counter() - t_case) * 1000.0
            latencies_ms.append(lat)
            rep_ranks[case.case_id] = tuple(doc.id for doc in top30)
        rankings_by_rep.append(rep_ranks)

    # Ranking stability
    stable = (rankings_by_rep[0] == rankings_by_rep[1] == rankings_by_rep[2])

    p50_ms = float(np.percentile(latencies_ms, 50))
    p95_ms = float(np.percentile(latencies_ms, 95))

    # Evaluate rep 1 for metrics
    d30_metrics = []
    d5_metrics = []
    for case in inputs.cases:
        c_query = _case_query(case)
        top30 = bm25.search(c_query, limit=GENERATOR_DEPTH)
        d30_metrics.append(score_at_depth(case, top30, depth=30))
        d5_metrics.append(score_at_depth(case, top30, depth=5))

    return d30_metrics, d5_metrics, build_ms, p50_ms, p95_ms, peak_rss_mb, stable


def run_bm25_parameter_calibration(
    inputs: SparseBenchmarkInputs,
    checkpoint: CheckpointState | None = None,
    results_dir: Path | None = None,
) -> CalibrationSelection:
    r_dir = results_dir or DEFAULT_RESULTS_DIR
    calib_path = r_dir / CALIBRATION_FILENAME

    # Check if all 5 parameter settings are already completed in checkpoint
    if checkpoint is not None:
        param_rows = [
            r for r in checkpoint.calibration_rows
            if r.get("calibration_stage") == "parameter"
        ]
        param_keys = {r.get("setting_key") for r in param_rows if r.get("category") == "overall" and r.get("status") == "completed"}
        if param_keys == {s.setting_key for s in BM25_SETTINGS}:
            sel_row = next((r for r in param_rows if r.get("category") == "overall" and r.get("selected") == "true"), None)
            if sel_row:
                return CalibrationSelection(
                    stage="parameter",
                    selected_setting_key=sel_row["setting_key"],
                    selection_reason=sel_row.get("selection_reason", ""),
                    all_rows=tuple(param_rows),
                )

    eval_results = {}
    for setting in BM25_SETTINGS:
        d30, d5, b_ms, p50, p95, rss, stable = _evaluate_bm25_setting(
            inputs,
            unicode_word_tokenize,
            "unicode_word",
            setting.k1,
            setting.b,
            setting.setting_key,
            "parameter",
        )
        eval_results[setting.setting_key] = {
            "setting": setting,
            "d30": d30,
            "d5": d5,
            "build_ms": b_ms,
            "p50_ms": p50,
            "p95_ms": p95,
            "peak_rss": rss,
            "ranking_stable": stable,
        }

    base_d30 = eval_results["baseline"]["d30"]
    base_d5 = eval_results["baseline"]["d5"]
    base_overall_r30 = sum(m.recall for m in base_d30) / len(base_d30)
    base_overall_mrr5 = sum(m.mrr for m in base_d5) / len(base_d5)
    base_overall_ndcg5 = sum(m.ndcg for m in base_d5) / len(base_d5)

    categories = sorted({c.category for c in inputs.cases})
    all_rows: list[dict[str, object]] = []
    candidate_summary = {}

    for setting in BM25_SETTINGS:
        key = setting.setting_key
        data = eval_results[key]
        d30 = data["d30"]
        d5 = data["d5"]

        overall_r30 = sum(m.recall for m in d30) / len(d30)
        overall_mrr5 = sum(m.mrr for m in d5) / len(d5)
        overall_ndcg5 = sum(m.ndcg for m in d5) / len(d5)
        overall_hits = sum(1 for m in d30 if m.hit)

        delta_r30 = overall_r30 - base_overall_r30
        delta_mrr5 = overall_mrr5 - base_overall_mrr5
        delta_ndcg5 = overall_ndcg5 - base_overall_ndcg5

        all_guards_pass = True
        cat_rows = []

        for cat in categories:
            cat_d30 = [m for m in d30 if m.category == cat]
            cat_d5 = [m for m in d5 if m.category == cat]
            ctrl_cat_d30 = [m for m in base_d30 if m.category == cat]
            ctrl_cat_d5 = [m for m in base_d5 if m.category == cat]

            cat_n = len(cat_d30)
            cat_hits = sum(1 for m in cat_d30 if m.hit)
            cat_r30 = sum(m.recall for m in cat_d30) / cat_n if cat_n else 0.0
            cat_mrr5 = sum(m.mrr for m in cat_d5) / cat_n if cat_n else 0.0
            cat_ndcg5 = sum(m.ndcg for m in cat_d5) / cat_n if cat_n else 0.0

            ctrl_r30 = sum(m.recall for m in ctrl_cat_d30) / cat_n if cat_n else 0.0
            ctrl_mrr5 = sum(m.mrr for m in ctrl_cat_d5) / cat_n if cat_n else 0.0
            ctrl_ndcg5 = sum(m.ndcg for m in ctrl_cat_d5) / cat_n if cat_n else 0.0

            c_delta_r30 = cat_r30 - ctrl_r30
            c_delta_mrr5 = cat_mrr5 - ctrl_mrr5
            c_delta_ndcg5 = cat_ndcg5 - ctrl_ndcg5

            # Evaluate calibration guardrail: hit@30 and nDCG@5 tiebreaker
            guard_pass, _ = evaluate_depth_category_guardrails(ctrl_cat_d30, cat_d30, ctrl_cat_d5, cat_d5)
            if not guard_pass:
                all_guards_pass = False

            cat_rows.append({
                "experiment_version": "phase8-08b-v1",
                "calibration_stage": "parameter",
                "setting_key": key,
                "category": cat,
                "tokenizer_key": "unicode_word",
                "k1": setting.k1,
                "b": setting.b,
                "status": "completed",
                "error": "",
                "case_count": cat_n,
                "hit_case_count": cat_hits,
                "recall_at_30": cat_r30,
                "mrr_at_5": cat_mrr5,
                "ndcg_at_5": cat_ndcg5,
                "successful_repetitions": 3,
                "ranking_stable": data["ranking_stable"],
                "build_ms": data["build_ms"],
                "warm_total_p50_ms": data["p50_ms"],
                "warm_total_p95_ms": data["p95_ms"],
                "observed_peak_rss_mb": data["peak_rss"],
                "delta_recall_at_30": c_delta_r30,
                "delta_mrr_at_5": c_delta_mrr5,
                "delta_ndcg_at_5": c_delta_ndcg5,
                "category_guardrail_pass": guard_pass,
                "all_category_guardrails_pass": "",
                "selected": "",
                "selection_reason": "",
            })

        overall_row = {
            "experiment_version": "phase8-08b-v1",
            "calibration_stage": "parameter",
            "setting_key": key,
            "category": "overall",
            "tokenizer_key": "unicode_word",
            "k1": setting.k1,
            "b": setting.b,
            "status": "completed",
            "error": "",
            "case_count": len(inputs.cases),
            "hit_case_count": overall_hits,
            "recall_at_30": overall_r30,
            "mrr_at_5": overall_mrr5,
            "ndcg_at_5": overall_ndcg5,
            "successful_repetitions": 3,
            "ranking_stable": data["ranking_stable"],
            "build_ms": data["build_ms"],
            "warm_total_p50_ms": data["p50_ms"],
            "warm_total_p95_ms": data["p95_ms"],
            "observed_peak_rss_mb": data["peak_rss"],
            "delta_recall_at_30": delta_r30,
            "delta_mrr_at_5": delta_mrr5,
            "delta_ndcg_at_5": delta_ndcg5,
            "category_guardrail_pass": all_guards_pass,
            "all_category_guardrails_pass": all_guards_pass,
            "selected": "",
            "selection_reason": "",
        }

        all_rows.append(overall_row)
        all_rows.extend(cat_rows)

        candidate_summary[key] = {
            "recall_at_30": overall_r30,
            "ndcg_at_5": overall_ndcg5,
            "mrr_at_5": overall_mrr5,
            "delta_recall_at_30": delta_r30,
            "delta_ndcg_at_5": delta_ndcg5,
            "all_guards_pass": all_guards_pass,
            "warm_total_p95_ms": data["p95_ms"],
        }

    # Selection logic:
    # 1. Candidate must pass all category guardrails
    # 2. Maximize Recall@30
    # 3. Tiebreak by nDCG@5, MRR@5, lowest p95 latency
    # 4. If no candidate strictly beats baseline, baseline retained
    valid_candidates = [
        k for k, v in candidate_summary.items()
        if v["all_guards_pass"]
    ]

    if not valid_candidates:
        selected_key = "baseline"
        selected_reason = "Baseline retained (no candidate passed all category guardrails)"
    else:
        sorted_cands = sorted(
            valid_candidates,
            key=lambda k: (
                -candidate_summary[k]["recall_at_30"],
                -candidate_summary[k]["ndcg_at_5"],
                -candidate_summary[k]["mrr_at_5"],
                candidate_summary[k]["warm_total_p95_ms"],
            ),
        )
        best_cand = sorted_cands[0]
        if best_cand == "baseline":
            selected_key = "baseline"
            selected_reason = "Baseline optimal among valid candidates"
        else:
            selected_key = best_cand
            selected_reason = f"Selected {best_cand} (R@30={candidate_summary[best_cand]['recall_at_30']:.4f}, nDCG@5={candidate_summary[best_cand]['ndcg_at_5']:.4f})"

    for r in all_rows:
        if r.get("setting_key") == selected_key:
            r["selected"] = "true"
            r["selection_reason"] = selected_reason
        else:
            r["selected"] = "false"
            r["selection_reason"] = ""

    upsert_calibration_rows(all_rows, calib_path)
    return CalibrationSelection("parameter", selected_key, selected_reason, tuple(all_rows))


def run_tokenizer_calibration(
    inputs: SparseBenchmarkInputs,
    parameter_selection: CalibrationSelection,
    checkpoint: CheckpointState | None = None,
    results_dir: Path | None = None,
) -> CalibrationSelection:
    r_dir = results_dir or DEFAULT_RESULTS_DIR
    calib_path = r_dir / CALIBRATION_FILENAME

    # Check if both tokenizer settings are already completed in checkpoint
    if checkpoint is not None:
        tok_rows = [
            r for r in checkpoint.calibration_rows
            if r.get("calibration_stage") == "tokenizer"
        ]
        tok_keys = {r.get("setting_key") for r in tok_rows if r.get("category") == "overall" and r.get("status") == "completed"}
        if tok_keys == {"unicode_word", "underthesea_word"}:
            sel_row = next((r for r in tok_rows if r.get("category") == "overall" and r.get("selected") == "true"), None)
            if sel_row:
                return CalibrationSelection(
                    stage="tokenizer",
                    selected_setting_key=sel_row["setting_key"],
                    selection_reason=sel_row.get("selection_reason", ""),
                    all_rows=tuple(tok_rows),
                )

    selected_param_setting = next(
        (s for s in BM25_SETTINGS if s.setting_key == parameter_selection.selected_setting_key),
        BM25_SETTINGS[0],
    )
    k1, b = selected_param_setting.k1, selected_param_setting.b

    tokenizers = (
        ("unicode_word", unicode_word_tokenize),
        ("underthesea_word", underthesea_word_tokenize),
    )

    eval_results = {}
    for tok_key, tok_fn in tokenizers:
        d30, d5, b_ms, p50, p95, rss, stable = _evaluate_bm25_setting(
            inputs,
            tok_fn,
            tok_key,
            k1,
            b,
            tok_key,
            "tokenizer",
        )
        eval_results[tok_key] = {
            "d30": d30,
            "d5": d5,
            "build_ms": b_ms,
            "p50_ms": p50,
            "p95_ms": p95,
            "peak_rss": rss,
            "ranking_stable": stable,
        }

    base_d30 = eval_results["unicode_word"]["d30"]
    base_d5 = eval_results["unicode_word"]["d5"]
    base_overall_r30 = sum(m.recall for m in base_d30) / len(base_d30)
    base_overall_mrr5 = sum(m.mrr for m in base_d5) / len(base_d5)
    base_overall_ndcg5 = sum(m.ndcg for m in base_d5) / len(base_d5)

    categories = sorted({c.category for c in inputs.cases})
    all_rows: list[dict[str, object]] = []
    candidate_summary = {}

    for tok_key, tok_fn in tokenizers:
        data = eval_results[tok_key]
        d30 = data["d30"]
        d5 = data["d5"]

        overall_r30 = sum(m.recall for m in d30) / len(d30)
        overall_mrr5 = sum(m.mrr for m in d5) / len(d5)
        overall_ndcg5 = sum(m.ndcg for m in d5) / len(d5)
        overall_hits = sum(1 for m in d30 if m.hit)

        delta_r30 = overall_r30 - base_overall_r30
        delta_mrr5 = overall_mrr5 - base_overall_mrr5
        delta_ndcg5 = overall_ndcg5 - base_overall_ndcg5

        all_guards_pass = True
        cat_rows = []

        for cat in categories:
            cat_d30 = [m for m in d30 if m.category == cat]
            cat_d5 = [m for m in d5 if m.category == cat]
            ctrl_cat_d30 = [m for m in base_d30 if m.category == cat]
            ctrl_cat_d5 = [m for m in base_d5 if m.category == cat]

            cat_n = len(cat_d30)
            cat_hits = sum(1 for m in cat_d30 if m.hit)
            cat_r30 = sum(m.recall for m in cat_d30) / cat_n if cat_n else 0.0
            cat_mrr5 = sum(m.mrr for m in cat_d5) / cat_n if cat_n else 0.0
            cat_ndcg5 = sum(m.ndcg for m in cat_d5) / cat_n if cat_n else 0.0

            ctrl_r30 = sum(m.recall for m in ctrl_cat_d30) / cat_n if cat_n else 0.0
            ctrl_mrr5 = sum(m.mrr for m in ctrl_cat_d5) / cat_n if cat_n else 0.0
            ctrl_ndcg5 = sum(m.ndcg for m in ctrl_cat_d5) / cat_n if cat_n else 0.0

            c_delta_r30 = cat_r30 - ctrl_r30
            c_delta_mrr5 = cat_mrr5 - ctrl_mrr5
            c_delta_ndcg5 = cat_ndcg5 - ctrl_ndcg5

            # Evaluate calibration guardrail: hit@30 and nDCG@5 tiebreaker
            guard_pass, _ = evaluate_depth_category_guardrails(ctrl_cat_d30, cat_d30, ctrl_cat_d5, cat_d5)
            if not guard_pass:
                all_guards_pass = False

            cat_rows.append({
                "experiment_version": "phase8-08b-v1",
                "calibration_stage": "tokenizer",
                "setting_key": tok_key,
                "category": cat,
                "tokenizer_key": tok_key,
                "k1": k1,
                "b": b,
                "status": "completed",
                "error": "",
                "case_count": cat_n,
                "hit_case_count": cat_hits,
                "recall_at_30": cat_r30,
                "mrr_at_5": cat_mrr5,
                "ndcg_at_5": cat_ndcg5,
                "successful_repetitions": 3,
                "ranking_stable": data["ranking_stable"],
                "build_ms": data["build_ms"],
                "warm_total_p50_ms": data["p50_ms"],
                "warm_total_p95_ms": data["p95_ms"],
                "observed_peak_rss_mb": data["peak_rss"],
                "delta_recall_at_30": c_delta_r30,
                "delta_mrr_at_5": c_delta_mrr5,
                "delta_ndcg_at_5": c_delta_ndcg5,
                "category_guardrail_pass": guard_pass,
                "all_category_guardrails_pass": "",
                "selected": "",
                "selection_reason": "",
            })

        overall_row = {
            "experiment_version": "phase8-08b-v1",
            "calibration_stage": "tokenizer",
            "setting_key": tok_key,
            "category": "overall",
            "tokenizer_key": tok_key,
            "k1": k1,
            "b": b,
            "status": "completed",
            "error": "",
            "case_count": len(inputs.cases),
            "hit_case_count": overall_hits,
            "recall_at_30": overall_r30,
            "mrr_at_5": overall_mrr5,
            "ndcg_at_5": overall_ndcg5,
            "successful_repetitions": 3,
            "ranking_stable": data["ranking_stable"],
            "build_ms": data["build_ms"],
            "warm_total_p50_ms": data["p50_ms"],
            "warm_total_p95_ms": data["p95_ms"],
            "observed_peak_rss_mb": data["peak_rss"],
            "delta_recall_at_30": delta_r30,
            "delta_mrr_at_5": delta_mrr5,
            "delta_ndcg_at_5": delta_ndcg5,
            "category_guardrail_pass": all_guards_pass,
            "all_category_guardrails_pass": all_guards_pass,
            "selected": "",
            "selection_reason": "",
        }

        all_rows.append(overall_row)
        all_rows.extend(cat_rows)

        candidate_summary[tok_key] = {
            "recall_at_30": overall_r30,
            "ndcg_at_5": overall_ndcg5,
            "mrr_at_5": overall_mrr5,
            "delta_recall_at_30": delta_r30,
            "delta_ndcg_at_5": delta_ndcg5,
            "all_guards_pass": all_guards_pass,
            "warm_total_p95_ms": data["p95_ms"],
        }

    # Simplicity preference: Underthesea chosen only if strictly better Recall@30 or nDCG@5 AND passes all guardrails
    u_cand = candidate_summary.get("underthesea_word")
    base_cand = candidate_summary.get("unicode_word")
    if (
        u_cand
        and u_cand["all_guards_pass"]
        and (
            u_cand["recall_at_30"] > base_cand["recall_at_30"] + 0.001
            or (
                math.isclose(u_cand["recall_at_30"], base_cand["recall_at_30"])
                and u_cand["ndcg_at_5"] > base_cand["ndcg_at_5"] + 0.005
            )
        )
    ):
        selected_key = "underthesea_word"
        selected_reason = "Underthesea improved quality beyond Unicode baseline"
    else:
        selected_key = "unicode_word"
        selected_reason = "Unicode word tokenizer retained (simplicity preference)"

    for r in all_rows:
        if r.get("setting_key") == selected_key:
            r["selected"] = "true"
            r["selection_reason"] = selected_reason
        else:
            r["selected"] = "false"
            r["selection_reason"] = ""

    upsert_calibration_rows(all_rows, calib_path)
    return CalibrationSelection("tokenizer", selected_key, selected_reason, tuple(all_rows))


def load_or_run_calibration(
    inputs: SparseBenchmarkInputs,
    *,
    expected_active_snapshot: dict[str, object],
    checkpoint: CheckpointState | None = None,
    results_dir: Path | None = None,
) -> SelectedLexicalContract:
    current_snap = snapshot_active_collection(inputs)
    if current_snap != expected_active_snapshot:
        raise ValueError(
            f"Active production snapshot changed before calibration: expected {expected_active_snapshot}, got {current_snap}"
        )

    r_dir = results_dir or DEFAULT_RESULTS_DIR
    param_sel = run_bm25_parameter_calibration(inputs, checkpoint=checkpoint, results_dir=r_dir)
    tok_sel = run_tokenizer_calibration(inputs, param_sel, checkpoint=checkpoint, results_dir=r_dir)

    after_snap = snapshot_active_collection(inputs)
    if after_snap != expected_active_snapshot:
        raise ValueError(
            f"Active production snapshot changed after calibration: expected {expected_active_snapshot}, got {after_snap}"
        )

    param_setting = next(
        s for s in BM25_SETTINGS if s.setting_key == param_sel.selected_setting_key
    )
    tokenizer_fn = (
        underthesea_word_tokenize if tok_sel.selected_setting_key == "underthesea_word" else unicode_word_tokenize
    )

    return SelectedLexicalContract(
        bm25_setting_key=param_setting.setting_key,
        k1=param_setting.k1,
        b=param_setting.b,
        tokenizer_key=tok_sel.selected_setting_key,
        tokenizer=tokenizer_fn,
        parameter_selection_reason=param_sel.selection_reason,
        tokenizer_selection_reason=tok_sel.selection_reason,
    )


# ---------------------------------------------------------------------------
# Exact 20-Setting Catalog & Orchestration
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RetrievalSetting:
    order: int
    setting_key: str
    setting_label: str
    path: str
    dense_setting_key: str | None
    sparse_family: str | None
    fusion_method: str | None


RETRIEVAL_SETTINGS = (
    RetrievalSetting(1, "dense__e5-small-384", "Dense: E5-small 384D", "dense_only", "e5-small-384", None, None),
    RetrievalSetting(2, "dense__huydang-dek21-embedding-768", "Dense: Huydang DEk21 768D", "dense_only", "huydang-dek21-embedding-768", None, None),
    RetrievalSetting(3, "dense__e5-base-768", "Dense: E5-base 768D", "dense_only", "e5-base-768", None, None),
    RetrievalSetting(4, "bm25-only", "Sparse: BM25 Only", "sparse_only", None, "bm25", None),
    RetrievalSetting(5, "dense-bm25-rescore__e5-small-384", "Rescore: E5-small -> BM25", "dense_bm25_rescore", "e5-small-384", "bm25", "weighted"),
    RetrievalSetting(6, "dense-bm25-rescore__huydang-dek21-embedding-768", "Rescore: Huydang DEk21 -> BM25", "dense_bm25_rescore", "huydang-dek21-embedding-768", "bm25", "weighted"),
    RetrievalSetting(7, "dense-bm25-rescore__e5-base-768", "Rescore: E5-base -> BM25", "dense_bm25_rescore", "e5-base-768", "bm25", "weighted"),
    RetrievalSetting(8, "hybrid-bm25-rrf__e5-small-384", "Hybrid: E5-small + BM25 (RRF)", "hybrid_dense_sparse", "e5-small-384", "bm25", "rrf"),
    RetrievalSetting(9, "hybrid-bm25-weighted__e5-small-384", "Hybrid: E5-small + BM25 (Weighted)", "hybrid_dense_sparse", "e5-small-384", "bm25", "weighted"),
    RetrievalSetting(10, "hybrid-bm25-rrf__huydang-dek21-embedding-768", "Hybrid: Huydang DEk21 + BM25 (RRF)", "hybrid_dense_sparse", "huydang-dek21-embedding-768", "bm25", "rrf"),
    RetrievalSetting(11, "hybrid-bm25-weighted__huydang-dek21-embedding-768", "Hybrid: Huydang DEk21 + BM25 (Weighted)", "hybrid_dense_sparse", "huydang-dek21-embedding-768", "bm25", "weighted"),
    RetrievalSetting(12, "hybrid-bm25-rrf__e5-base-768", "Hybrid: E5-base + BM25 (RRF)", "hybrid_dense_sparse", "e5-base-768", "bm25", "rrf"),
    RetrievalSetting(13, "hybrid-bm25-weighted__e5-base-768", "Hybrid: E5-base + BM25 (Weighted)", "hybrid_dense_sparse", "e5-base-768", "bm25", "weighted"),
    RetrievalSetting(14, "tfidf-only", "Sparse: TF-IDF Only", "sparse_only", None, "tfidf", None),
    RetrievalSetting(15, "hybrid-tfidf-rrf__e5-small-384", "Hybrid: E5-small + TF-IDF (RRF)", "hybrid_dense_sparse", "e5-small-384", "tfidf", "rrf"),
    RetrievalSetting(16, "hybrid-tfidf-weighted__e5-small-384", "Hybrid: E5-small + TF-IDF (Weighted)", "hybrid_dense_sparse", "e5-small-384", "tfidf", "weighted"),
    RetrievalSetting(17, "hybrid-tfidf-rrf__huydang-dek21-embedding-768", "Hybrid: Huydang DEk21 + TF-IDF (RRF)", "hybrid_dense_sparse", "huydang-dek21-embedding-768", "tfidf", "rrf"),
    RetrievalSetting(18, "hybrid-tfidf-weighted__huydang-dek21-embedding-768", "Hybrid: Huydang DEk21 + TF-IDF (Weighted)", "hybrid_dense_sparse", "huydang-dek21-embedding-768", "tfidf", "weighted"),
    RetrievalSetting(19, "hybrid-tfidf-rrf__e5-base-768", "Hybrid: E5-base + TF-IDF (RRF)", "hybrid_dense_sparse", "e5-base-768", "tfidf", "rrf"),
    RetrievalSetting(20, "hybrid-tfidf-weighted__e5-base-768", "Hybrid: E5-base + TF-IDF (Weighted)", "hybrid_dense_sparse", "e5-base-768", "tfidf", "weighted"),
)


def requested_setting_keys_from_env(value: str | None) -> tuple[str, ...]:
    val = value or os.environ.get("HUE_RAG_08B_SETTING_KEYS") or os.environ.get("SPARSE_BENCHMARK_SETTINGS")
    if val is None or not val.strip():
        return tuple(setting.setting_key for setting in RETRIEVAL_SETTINGS)
    requested = tuple(part.strip() for part in val.split(",") if part.strip())
    valid_keys = {setting.setting_key for setting in RETRIEVAL_SETTINGS}
    invalid = [k for k in requested if k not in valid_keys]
    if invalid:
        raise ValueError(f"Invalid setting keys requested: {invalid}")
    return requested


def _build_fusion_item_record(doc: RetrievedDocument, rank: int) -> dict[str, object]:
    meta = doc.metadata or {}
    dense_rank = meta.get("dense_rank")
    dense_raw = meta.get("dense_score")
    dense_norm = meta.get("normalized_dense")
    sparse_rank = meta.get("sparse_rank")
    sparse_raw = meta.get("sparse_score")
    sparse_norm = meta.get("normalized_sparse")
    rrf_dense = (1.0 / (60 + dense_rank)) if (dense_rank is not None and isinstance(dense_rank, int)) else None
    rrf_sparse = (1.0 / (60 + sparse_rank)) if (sparse_rank is not None and isinstance(sparse_rank, int)) else None

    return {
        "chunk_id": doc.id,
        "rank": rank,
        "fused_score": doc.score,
        "dense_rank": dense_rank,
        "dense_raw_score": dense_raw,
        "dense_norm_score": dense_norm,
        "sparse_rank": sparse_rank,
        "sparse_raw_score": sparse_raw,
        "sparse_norm_score": sparse_norm,
        "rrf_dense_component": rrf_dense,
        "rrf_sparse_component": rrf_sparse,
        "source": meta.get("source", ""),
        "section": meta.get("section", ""),
    }


@dataclass(frozen=True)
class SparseBenchmarkResult:
    setting: RetrievalSetting
    status: str
    error: str
    summary: dict[str, object]
    category_rows: list[dict[str, object]]
    case_records: list[dict[str, object]]
    rankings_by_repetition: list[dict[str, tuple[str, ...]]]


def run_retrieval_setting(
    setting: RetrievalSetting,
    inputs: SparseBenchmarkInputs,
    selected_lexical: SelectedLexicalContract,
    tfidf_state: TfidfState,
    results_dir: Path | None = None,
    expected_active_snapshot: dict[str, object] | None = None,
) -> SparseBenchmarkResult:
    import tracemalloc
    r_dir = results_dir or DEFAULT_RESULTS_DIR
    res_path = r_dir / RESULTS_FILENAME
    cases_path = r_dir / CASES_FILENAME

    if expected_active_snapshot is not None:
        snap_now = snapshot_active_collection(inputs)
        if snap_now != expected_active_snapshot:
            raise ValueError(
                f"Active production snapshot changed before setting '{setting.setting_key}': expected {expected_active_snapshot}, got {snap_now}"
            )

    dense_retriever = None
    dense_runner = None
    bm25 = None
    doc_idx_by_id = {}

    try:
        tracemalloc.start()

        if setting.dense_setting_key:
            dense_cfg = next(s for s in ALL_DENSE_SETTINGS if s.setting_key == setting.dense_setting_key)
            dense_runner = build_dense_runner(dense_cfg)
            dense_retriever = DenseRetriever(
                client=inputs.client,
                embedder=dense_runner,
                collection_name=dense_cfg.collection_name,
                top_k=30,
            )

        if setting.sparse_family == "bm25":
            bm25 = FullCorpusBM25(
                inputs.chunks,
                selected_lexical.tokenizer,
                k1=selected_lexical.k1,
                b=selected_lexical.b,
            )
            doc_idx_by_id = {str(c["metadata"]["chunk_id"]): i for i, c in enumerate(inputs.chunks)}

        # Warmup query (discarded)
        if inputs.cases:
            q_warm = _case_query(inputs.cases[0])
            if dense_retriever:
                dense_retriever.search(q_warm, limit=30)
            if bm25:
                bm25.search(q_warm, limit=30)
            elif setting.sparse_family == "tfidf":
                query_tfidf(inputs.client, tfidf_state.collection_name, tfidf_state.encoder, q_warm, limit=30)

        # 3 repetitions
        results_by_rep: list[dict[str, dict]] = []
        case_latencies: dict[str, dict[str, list[float]]] = {
            c.case_id: {"dense": [], "sparse": [], "fusion": [], "total": []} for c in inputs.cases
        }

        for _ in range(3):
            rep_results: dict[str, dict] = {}
            for case in inputs.cases:
                c_query = _case_query(case)
                dense_top30: list[RetrievedDocument] = []
                sparse_top30: list[RetrievedDocument] = []
                fused_top10: list[RetrievedDocument] = []
                final_top5: list[RetrievedDocument] = []

                dense_lat = 0.0
                sparse_lat = 0.0
                fusion_lat = 0.0

                if dense_retriever:
                    t0 = time.perf_counter()
                    dense_top30 = dense_retriever.search(c_query, limit=30)
                    dense_lat = (time.perf_counter() - t0) * 1000.0

                if bm25:
                    t0 = time.perf_counter()
                    sparse_top30 = bm25.search(c_query, limit=30)
                    sparse_lat = (time.perf_counter() - t0) * 1000.0
                elif setting.sparse_family == "tfidf":
                    t0 = time.perf_counter()
                    sparse_top30 = query_tfidf(
                        inputs.client,
                        tfidf_state.collection_name,
                        tfidf_state.encoder,
                        c_query,
                        limit=30,
                    )
                    sparse_lat = (time.perf_counter() - t0) * 1000.0

                t0 = time.perf_counter()
                if setting.path == "dense_only":
                    # Attach metadata for evidence
                    for r, d in enumerate(dense_top30, start=1):
                        d.metadata["dense_rank"] = r
                        d.metadata["dense_score"] = d.score
                    fused_top10 = dense_top30[:10]
                    final_top5 = dense_top30[:5]
                elif setting.path == "sparse_only":
                    for r, d in enumerate(sparse_top30, start=1):
                        d.metadata["sparse_rank"] = r
                        d.metadata["sparse_score"] = d.score
                    fused_top10 = sparse_top30[:10]
                    final_top5 = sparse_top30[:5]
                elif setting.path == "dense_bm25_rescore":
                    # Rescore top 30 dense candidates with BM25
                    candidate_chunks = [
                        inputs.chunks[doc_idx_by_id[d.id]]
                        for d in dense_top30
                        if d.id in doc_idx_by_id
                    ]
                    if candidate_chunks:
                        sub_bm25 = FullCorpusBM25(
                            candidate_chunks,
                            selected_lexical.tokenizer,
                            k1=selected_lexical.k1,
                            b=selected_lexical.b,
                        )
                        sparse_top30 = sub_bm25.search(c_query, limit=len(candidate_chunks))
                    else:
                        sparse_top30 = []
                    fused_all = weighted_fuse(dense_top30, sparse_top30, limit=30, dense_weight=0.6, sparse_weight=0.4)
                    fused_top10 = fused_all[:10]
                    final_top5 = fused_all[:5]
                elif setting.path == "hybrid_dense_sparse":
                    if setting.fusion_method == "rrf":
                        fused_all = rrf_fuse(dense_top30, sparse_top30, limit=30, rrf_k=60)
                    elif setting.fusion_method == "weighted":
                        fused_all = weighted_fuse(dense_top30, sparse_top30, limit=30, dense_weight=0.6, sparse_weight=0.4)
                    else:
                        raise ValueError(f"Unknown fusion method: {setting.fusion_method}")
                    fused_top10 = fused_all[:10]
                    final_top5 = fused_all[:5]

                fusion_lat = (time.perf_counter() - t0) * 1000.0
                total_lat = dense_lat + sparse_lat + fusion_lat

                case_latencies[case.case_id]["dense"].append(dense_lat)
                case_latencies[case.case_id]["sparse"].append(sparse_lat)
                case_latencies[case.case_id]["fusion"].append(fusion_lat)
                case_latencies[case.case_id]["total"].append(total_lat)

                rep_results[case.case_id] = {
                    "dense_top30": dense_top30,
                    "sparse_top30": sparse_top30,
                    "fused_top10": fused_top10,
                    "final_top5": final_top5,
                    "final_ranks": tuple(d.id for d in final_top5),
                }
            results_by_rep.append(rep_results)

        _, peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_rss = peak_bytes / (1024.0 * 1024.0)

        # Check ranking stability across 3 repetitions
        rankings_by_rep = [
            {c.case_id: rep_results[c.case_id]["final_ranks"] for c in inputs.cases}
            for rep_results in results_by_rep
        ]
        ranking_stable = True
        for c in inputs.cases:
            r0 = rankings_by_rep[0][c.case_id]
            r1 = rankings_by_rep[1][c.case_id]
            r2 = rankings_by_rep[2][c.case_id]
            if not (r0 == r1 == r2):
                ranking_stable = False
                break

        # Calculate median latencies across repetitions
        dense_medians = [float(np.median(case_latencies[c.case_id]["dense"])) for c in inputs.cases if case_latencies[c.case_id]["dense"]]
        sparse_medians = [float(np.median(case_latencies[c.case_id]["sparse"])) for c in inputs.cases if case_latencies[c.case_id]["sparse"]]
        fusion_medians = [float(np.median(case_latencies[c.case_id]["fusion"])) for c in inputs.cases if case_latencies[c.case_id]["fusion"]]
        total_medians = [float(np.median(case_latencies[c.case_id]["total"])) for c in inputs.cases]

        dense_p50 = float(np.percentile(dense_medians, 50)) if dense_medians else ""
        dense_p95 = float(np.percentile(dense_medians, 95)) if dense_medians else ""
        sparse_p50 = float(np.percentile(sparse_medians, 50)) if sparse_medians else ""
        sparse_p95 = float(np.percentile(sparse_medians, 95)) if sparse_medians else ""
        fusion_p50 = float(np.percentile(fusion_medians, 50)) if fusion_medians else ""
        fusion_p95 = float(np.percentile(fusion_medians, 95)) if fusion_medians else ""
        warm_p50 = float(np.percentile(total_medians, 50))
        warm_p95 = float(np.percentile(total_medians, 95))

        # Evaluate rep 1 per-case records and stage metrics
        case_records = []
        d5_metrics_list = []
        d10_metrics_list = []
        d30_dense_list = []
        d30_sparse_list = []
        union_recall_list = []

        for case in inputs.cases:
            c_res = results_by_rep[0][case.case_id]
            d_top30 = c_res["dense_top30"]
            s_top30 = c_res["sparse_top30"]
            f_top10 = c_res["fused_top10"]
            f_top5 = c_res["final_top5"]

            m5 = score_at_depth(case, f_top5, depth=5)
            m10 = score_at_depth(case, f_top10, depth=10)
            d5_metrics_list.append(m5)
            d10_metrics_list.append(m10)

            d30_dense_r = ""
            if d_top30:
                m_dense = score_at_depth(case, d_top30, depth=30)
                d30_dense_list.append(m_dense)
                d30_dense_r = m_dense.recall

            d30_sparse_r = ""
            if s_top30:
                m_sparse = score_at_depth(case, s_top30, depth=30)
                d30_sparse_list.append(m_sparse)
                d30_sparse_r = m_sparse.recall

            union_r = ""
            union_ids = []
            if d_top30 or s_top30:
                seen_u = {}
                for d in d_top30 + s_top30:
                    if d.id not in seen_u:
                        seen_u[d.id] = d
                union_docs = list(seen_u.values())
                union_ids = list(seen_u.keys())
                m_union = score_at_depth(case, union_docs, depth=len(union_docs))
                union_recall_list.append(m_union)
                union_r = m_union.recall

            case_rel_keys = _extract_case_relevant_keys(case)
            case_rec = {
                "experiment_version": "phase8-08b-v1",
                "setting_order": setting.order,
                "setting_key": setting.setting_key,
                "case_id": case.case_id,
                "category": case.category,
                "status": "completed",
                "error": "",
                "relevant_source_sections": [
                    {"source": src, "section": sec} for src, sec in case_rel_keys
                ],
                "derived_relevant_chunk_ids": [
                    str(chunk["metadata"]["chunk_id"])
                    for chunk in inputs.chunks
                    if (chunk["metadata"].get("source"), chunk["metadata"].get("section")) in case_rel_keys
                ],
                "successful_repetitions": 3,
                "ranking_stable": ranking_stable,
                "dense_top_30": [
                    {
                        "chunk_id": d.id,
                        "rank": r,
                        "raw_score": d.score,
                        "source": d.metadata.get("source", ""),
                        "section": d.metadata.get("section", ""),
                    }
                    for r, d in enumerate(d_top30, start=1)
                ],
                "sparse_top_30": [
                    {
                        "chunk_id": d.id,
                        "rank": r,
                        "raw_score": d.score,
                        "source": d.metadata.get("source", ""),
                        "section": d.metadata.get("section", ""),
                    }
                    for r, d in enumerate(s_top30, start=1)
                ],
                "candidate_union_chunk_ids": union_ids,
                "fusion_top_10": [
                    _build_fusion_item_record(d, r)
                    for r, d in enumerate(f_top10, start=1)
                ],
                "final_top_5": [
                    _build_fusion_item_record(d, r)
                    for r, d in enumerate(f_top5, start=1)
                ],
                "dense_recall_at_30": d30_dense_r,
                "sparse_recall_at_30": d30_sparse_r,
                "candidate_union_recall": union_r,
                "fusion_recall_at_10": m10.recall,
                "recall_at_5": m5.recall,
                "mrr_at_5": m5.mrr,
                "ndcg_at_5": m5.ndcg,
                "latency_by_repetition_ms": case_latencies[case.case_id]["total"],
            }
            case_records.append(case_rec)

        # Build category rows and overall summary
        categories = sorted({c.category for c in inputs.cases})
        cat_rows = []

        for cat in categories:
            cat_d5 = [m for m in d5_metrics_list if m.category == cat]
            cat_d10 = [m for m in d10_metrics_list if m.category == cat]
            cat_n = len(cat_d5)
            cat_hits = sum(1 for m in cat_d5 if m.hit)
            cat_r5 = sum(m.recall for m in cat_d5) / cat_n if cat_n else 0.0
            cat_mrr5 = sum(m.mrr for m in cat_d5) / cat_n if cat_n else 0.0
            cat_ndcg5 = sum(m.ndcg for m in cat_d5) / cat_n if cat_n else 0.0
            cat_r10 = sum(m.recall for m in cat_d10) / cat_n if cat_n else 0.0

            cat_d30_d = [m.recall for m in d30_dense_list if m.category == cat]
            cat_d30_s = [m.recall for m in d30_sparse_list if m.category == cat]
            cat_u = [m.recall for m in union_recall_list if m.category == cat]

            cat_row = {
                "experiment_version": "phase8-08b-v1",
                "setting_order": setting.order,
                "setting_key": setting.setting_key,
                "setting_label": setting.setting_label,
                "category": cat,
                "path": setting.path,
                "dense_setting_key": setting.dense_setting_key or "",
                "sparse_family": setting.sparse_family or "",
                "fusion_method": setting.fusion_method or "",
                "status": "completed",
                "error": "",
                "case_count": cat_n,
                "hit_case_count": cat_hits,
                "successful_repetitions": 3,
                "ranking_stable": ranking_stable,
                "dense_recall_at_30": (sum(cat_d30_d) / cat_n) if cat_d30_d else "",
                "sparse_recall_at_30": (sum(cat_d30_s) / cat_n) if cat_d30_s else "",
                "candidate_union_recall": (sum(cat_u) / cat_n) if cat_u else "",
                "fusion_recall_at_10": cat_r10,
                "recall_at_5": cat_r5,
                "mrr_at_5": cat_mrr5,
                "ndcg_at_5": cat_ndcg5,
                "dense_query_p50_ms": dense_p50,
                "dense_query_p95_ms": dense_p95,
                "sparse_query_p50_ms": sparse_p50,
                "sparse_query_p95_ms": sparse_p95,
                "fusion_p50_ms": fusion_p50,
                "fusion_p95_ms": fusion_p95,
                "warm_total_p50_ms": warm_p50,
                "warm_total_p95_ms": warm_p95,
                "build_ms": "",
                "observed_peak_rss_mb": peak_rss,
                "delta_fusion_recall_at_10": "",
                "delta_recall_at_5": "",
                "delta_mrr_at_5": "",
                "delta_ndcg_at_5": "",
                "recall_ci_lower": "",
                "recall_ci_upper": "",
                "mrr_ci_lower": "",
                "mrr_ci_upper": "",
                "ndcg_ci_lower": "",
                "ndcg_ci_upper": "",
                "category_guardrail_pass": "",
                "all_category_guardrails_pass": "",
                "fusion_recall_gate": "",
                "final_recall_gate": "",
                "latency_gate": "",
                "complete_gate": "",
                "finalist_eligible": "",
                "finalist_selected": "",
            }
            cat_rows.append(cat_row)

        overall_hits = sum(1 for m in d5_metrics_list if m.hit)
        overall_r5 = sum(m.recall for m in d5_metrics_list) / len(inputs.cases)
        overall_mrr5 = sum(m.mrr for m in d5_metrics_list) / len(inputs.cases)
        overall_ndcg5 = sum(m.ndcg for m in d5_metrics_list) / len(inputs.cases)
        overall_r10 = sum(m.recall for m in d10_metrics_list) / len(inputs.cases)

        overall_d30_d = (sum(m.recall for m in d30_dense_list) / len(inputs.cases)) if d30_dense_list else ""
        overall_d30_s = (sum(m.recall for m in d30_sparse_list) / len(inputs.cases)) if d30_sparse_list else ""
        overall_u = (sum(m.recall for m in union_recall_list) / len(inputs.cases)) if union_recall_list else ""

        overall_row = {
            "experiment_version": "phase8-08b-v1",
            "setting_order": setting.order,
            "setting_key": setting.setting_key,
            "setting_label": setting.setting_label,
            "category": "overall",
            "path": setting.path,
            "dense_setting_key": setting.dense_setting_key or "",
            "sparse_family": setting.sparse_family or "",
            "fusion_method": setting.fusion_method or "",
            "status": "completed",
            "error": "",
            "case_count": len(inputs.cases),
            "hit_case_count": overall_hits,
            "successful_repetitions": 3,
            "ranking_stable": ranking_stable,
            "dense_recall_at_30": overall_d30_d,
            "sparse_recall_at_30": overall_d30_s,
            "candidate_union_recall": overall_u,
            "fusion_recall_at_10": overall_r10,
            "recall_at_5": overall_r5,
            "mrr_at_5": overall_mrr5,
            "ndcg_at_5": overall_ndcg5,
            "dense_query_p50_ms": dense_p50,
            "dense_query_p95_ms": dense_p95,
            "sparse_query_p50_ms": sparse_p50,
            "sparse_query_p95_ms": sparse_p95,
            "fusion_p50_ms": fusion_p50,
            "fusion_p95_ms": fusion_p95,
            "warm_total_p50_ms": warm_p50,
            "warm_total_p95_ms": warm_p95,
            "build_ms": "",
            "observed_peak_rss_mb": peak_rss,
            "delta_fusion_recall_at_10": "",
            "delta_recall_at_5": "",
            "delta_mrr_at_5": "",
            "delta_ndcg_at_5": "",
            "recall_ci_lower": "",
            "recall_ci_upper": "",
            "mrr_ci_lower": "",
            "mrr_ci_upper": "",
            "ndcg_ci_lower": "",
            "ndcg_ci_upper": "",
            "category_guardrail_pass": "",
            "all_category_guardrails_pass": "",
            "fusion_recall_gate": "",
            "final_recall_gate": "",
            "latency_gate": "",
            "complete_gate": "",
            "finalist_eligible": "",
            "finalist_selected": "",
        }

        all_setting_rows = [overall_row] + cat_rows

        # Upsert atomically
        upsert_result_rows(all_setting_rows, res_path)
        upsert_case_records(case_records, cases_path)

        return SparseBenchmarkResult(
            setting=setting,
            status="completed",
            error="",
            summary=overall_row,
            category_rows=cat_rows,
            case_records=case_records,
            rankings_by_repetition=rankings_by_rep,
        )

    except Exception as exc:
        err_msg = sanitize_error_message(exc)
        failed_overall = {
            "experiment_version": "phase8-08b-v1",
            "setting_order": setting.order,
            "setting_key": setting.setting_key,
            "setting_label": setting.setting_label,
            "category": "overall",
            "path": setting.path,
            "dense_setting_key": setting.dense_setting_key or "",
            "sparse_family": setting.sparse_family or "",
            "fusion_method": setting.fusion_method or "",
            "status": "failed",
            "error": err_msg,
            "case_count": len(inputs.cases),
            "hit_case_count": 0,
            "successful_repetitions": 0,
            "ranking_stable": False,
            "dense_recall_at_30": "",
            "sparse_recall_at_30": "",
            "candidate_union_recall": "",
            "fusion_recall_at_10": "",
            "recall_at_5": "",
            "mrr_at_5": "",
            "ndcg_at_5": "",
            "dense_query_p50_ms": "",
            "dense_query_p95_ms": "",
            "sparse_query_p50_ms": "",
            "sparse_query_p95_ms": "",
            "fusion_p50_ms": "",
            "fusion_p95_ms": "",
            "warm_total_p50_ms": "",
            "warm_total_p95_ms": "",
            "build_ms": "",
            "observed_peak_rss_mb": "",
            "delta_fusion_recall_at_10": "",
            "delta_recall_at_5": "",
            "delta_mrr_at_5": "",
            "delta_ndcg_at_5": "",
            "recall_ci_lower": "",
            "recall_ci_upper": "",
            "mrr_ci_lower": "",
            "mrr_ci_upper": "",
            "ndcg_ci_lower": "",
            "ndcg_ci_upper": "",
            "category_guardrail_pass": "",
            "all_category_guardrails_pass": "",
            "fusion_recall_gate": "",
            "final_recall_gate": "",
            "latency_gate": "",
            "complete_gate": "",
            "finalist_eligible": "",
            "finalist_selected": "",
        }
        failed_cases = [
            {
                "experiment_version": "phase8-08b-v1",
                "setting_order": setting.order,
                "setting_key": setting.setting_key,
                "case_id": c.case_id,
                "category": c.category,
                "status": "failed",
                "error": err_msg,
                "relevant_source_sections": [],
                "derived_relevant_chunk_ids": [],
                "successful_repetitions": 0,
                "ranking_stable": False,
                "dense_top_30": [],
                "sparse_top_30": [],
                "candidate_union_chunk_ids": [],
                "fusion_top_10": [],
                "final_top_5": [],
                "dense_recall_at_30": "",
                "sparse_recall_at_30": "",
                "candidate_union_recall": "",
                "fusion_recall_at_10": "",
                "recall_at_5": "",
                "mrr_at_5": "",
                "ndcg_at_5": "",
                "latency_by_repetition_ms": [],
            }
            for c in inputs.cases
        ]
        upsert_result_rows([failed_overall], res_path)
        upsert_case_records(failed_cases, cases_path)

        return SparseBenchmarkResult(
            setting=setting,
            status="failed",
            error=err_msg,
            summary=failed_overall,
            category_rows=[],
            case_records=failed_cases,
            rankings_by_repetition=[],
        )

    finally:
        if dense_runner is not None:
            dense_runner.close()
        del dense_runner
        del dense_retriever
        del bm25
        gc.collect()

        if expected_active_snapshot is not None:
            after_snap = snapshot_active_collection(inputs)
            if after_snap != expected_active_snapshot:
                raise ValueError(
                    f"Active production snapshot changed after setting '{setting.setting_key}': expected {expected_active_snapshot}, got {after_snap}"
                )


def build_expected_immutable_identity(
    inputs: SparseBenchmarkInputs,
    selected_lexical: SelectedLexicalContract,
    tfidf_state: TfidfState,
    active_snapshot_before: dict[str, object] | None = None,
) -> dict[str, object]:
    dense_prereqs = [
        {
            "dense_setting_key": s.setting_key,
            "model_id": s.model_id,
            "model_revision": s.revision,
            "dimension": s.dimension,
            "collection_name": s.collection_name,
        }
        for s in ALL_DENSE_SETTINGS
    ]

    import underthesea
    dependencies = {
        "underthesea": getattr(underthesea, "__version__", "unknown"),
    }

    return {
        "corpus_fingerprint": inputs.corpus_fingerprint,
        "golden_fingerprint": inputs.golden_fingerprint,
        "chunker_fingerprint": inputs.chunker_fingerprint,
        "dense_prerequisites": dense_prereqs,
        "dependencies": dependencies,
        "selected_bm25": {
            "setting_key": selected_lexical.bm25_setting_key,
            "k1": selected_lexical.k1,
            "b": selected_lexical.b,
        },
        "selected_tokenizer": selected_lexical.tokenizer_key,
        "tfidf": {
            "formula_version": TFIDF_FORMULA_VERSION,
            "vocabulary_fingerprint": tfidf_state.encoder.vocabulary_fingerprint,
            "collection_name": tfidf_state.collection_name,
        },
        "fusion": {"rrf_k": 60, "dense_weight": 0.6, "sparse_weight": 0.4},
        "depths": {"generator": 30, "fusion": 10, "final": 5},
        "repetitions": 3,
        "bootstrap": {"samples": 10_000, "seed": 42},
        "artifact_schemas": {"calibration": 1, "results": 1, "cases": 1},
        "active_snapshot_before": active_snapshot_before or snapshot_active_collection(inputs),
    }


def load_or_create_manifest(
    inputs: SparseBenchmarkInputs,
    selected_lexical: SelectedLexicalContract,
    tfidf_state: TfidfState,
    results_dir: Path | None = None,
    active_snapshot_before: dict[str, object] | None = None,
) -> ExperimentManifest:
    r_dir = results_dir or DEFAULT_RESULTS_DIR
    manifest_path = r_dir / MANIFEST_FILENAME

    expected_immutable = build_expected_immutable_identity(
        inputs,
        selected_lexical,
        tfidf_state,
        active_snapshot_before=active_snapshot_before,
    )

    if manifest_path.exists():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        existing_manifest = ExperimentManifest.from_dict(data)
        if existing_manifest.schema_version != "phase8-sparse-manifest-v1":
            raise ValueError(
                f"Manifest schema_version '{existing_manifest.schema_version}' != 'phase8-sparse-manifest-v1'"
            )
        if existing_manifest.experiment_version != "phase8-08b-v1":
            raise ValueError(
                f"Manifest experiment_version '{existing_manifest.experiment_version}' != 'phase8-08b-v1'"
            )

        ex_imm = existing_manifest.immutable_identity
        for k, expected_v in expected_immutable.items():
            if k == "active_snapshot_before":
                continue
            if ex_imm.get(k) != expected_v:
                raise ValueError(
                    f"Manifest immutable identity mismatch on '{k}': expected {expected_v}, got {ex_imm.get(k)}"
                )
        return existing_manifest

    manifest = ExperimentManifest(
        schema_version="phase8-sparse-manifest-v1",
        experiment_version="phase8-08b-v1",
        immutable_identity=expected_immutable,
        batch_history=(),
    )

    write_manifest_atomic(manifest, manifest_path)
    return manifest


def load_checkpoint_for_inputs(
    inputs: SparseBenchmarkInputs,
    selected_lexical: SelectedLexicalContract,
    tfidf_state: TfidfState,
    results_dir: Path | None = None,
) -> CheckpointState:
    r_dir = results_dir or DEFAULT_RESULTS_DIR
    manifest = load_or_create_manifest(inputs, selected_lexical, tfidf_state, results_dir=r_dir)
    return load_checkpoint(manifest, results_dir=r_dir)


def pending_setting_keys(
    checkpoint: CheckpointState,
    requested_keys: tuple[str, ...],
) -> tuple[str, ...]:
    completed = set(checkpoint.completed_setting_keys)
    return tuple(k for k in requested_keys if k not in completed)


def run_retrieval_batch(
    inputs: SparseBenchmarkInputs,
    selected_lexical: SelectedLexicalContract,
    tfidf_state: TfidfState,
    requested_setting_keys: tuple[str, ...] | None = None,
    expected_active_snapshot: dict[str, object] | None = None,
    results_dir: Path | None = None,
):
    r_dir = results_dir or DEFAULT_RESULTS_DIR
    manifest_path = r_dir / MANIFEST_FILENAME
    keys = requested_setting_keys or requested_setting_keys_from_env(None)
    snap0 = expected_active_snapshot or snapshot_active_collection(inputs)

    manifest = load_or_create_manifest(
        inputs, selected_lexical, tfidf_state, results_dir=r_dir, active_snapshot_before=snap0
    )
    checkpoint = load_checkpoint(manifest, results_dir=r_dir)

    executed_keys = []
    skipped_keys = []
    failed_keys = []

    try:
        for setting in RETRIEVAL_SETTINGS:
            if setting.setting_key not in keys:
                continue
            if setting.setting_key in checkpoint.completed_setting_keys:
                skipped_keys.append(setting.setting_key)
                # Yield cached completed result
                s_row = next(r for r in checkpoint.result_rows if r.get("setting_key") == setting.setting_key and r.get("category") == "overall")
                s_cats = [r for r in checkpoint.result_rows if r.get("setting_key") == setting.setting_key and r.get("category") != "overall"]
                s_cases = [c for c in checkpoint.case_records if c.get("setting_key") == setting.setting_key]
                yield SparseBenchmarkResult(
                    setting=setting,
                    status="completed",
                    error="",
                    summary=s_row,
                    category_rows=s_cats,
                    case_records=s_cases,
                    rankings_by_repetition=[],
                )
                continue

            try:
                result = run_retrieval_setting(
                    setting,
                    inputs,
                    selected_lexical,
                    tfidf_state,
                    results_dir=r_dir,
                    expected_active_snapshot=snap0,
                )
            except Exception as exc:
                err_msg = sanitize_error_message(exc)
                result = SparseBenchmarkResult(
                    setting=setting,
                    status="failed",
                    error=err_msg,
                    summary={"setting_key": setting.setting_key, "category": "overall", "status": "failed", "error": err_msg},
                    category_rows=[],
                    case_records=[],
                    rankings_by_repetition=[],
                )

            if result.status == "completed":
                executed_keys.append(setting.setting_key)
            else:
                failed_keys.append(setting.setting_key)

            yield result
    finally:
        # Only record batch history entry if there was actual mutation / execution
        if executed_keys or failed_keys:
            snap_after = snapshot_active_collection(inputs)
            new_batch_entry = {
                "batch_index": len(manifest.batch_history) + 1,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "requested_keys": list(keys),
                "executed_keys": executed_keys,
                "skipped_keys": skipped_keys,
                "failed_keys": failed_keys,
                "active_snapshot_before": snap0,
                "active_snapshot_after": snap_after,
            }
            updated_manifest = ExperimentManifest(
                schema_version=manifest.schema_version,
                experiment_version=manifest.experiment_version,
                immutable_identity=manifest.immutable_identity,
                batch_history=manifest.batch_history + (new_batch_entry,),
            )
            write_manifest_atomic(updated_manifest, manifest_path)


# ---------------------------------------------------------------------------
# Reconciliation & Finalist Selection
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ReconciliationResult:
    complete: bool
    summary: dict[str, object]
    bm25_finalist: str | None
    tfidf_finalist: str | None


def reconcile_sparse_benchmark(
    checkpoint: CheckpointState,
    *,
    inputs: SparseBenchmarkInputs | None = None,
    expected_active_snapshot: dict[str, object] | None = None,
    client: object | None = None,
    tfidf_state: TfidfState | None = None,
    selected_lexical: SelectedLexicalContract | None = None,
    results_dir: Path | None = None,
) -> ReconciliationResult:
    r_dir = results_dir or DEFAULT_RESULTS_DIR
    res_path = r_dir / RESULTS_FILENAME

    summary = {
        "bm25_parameter_settings_completed": 0,
        "tokenizer_settings_completed": 0,
        "main_settings_completed": 0,
        "total_calibration_rows": len(checkpoint.calibration_rows),
        "total_result_rows": len(checkpoint.result_rows),
        "total_case_records": len(checkpoint.case_records),
        "reconciliation_complete": False,
        "bm25_finalist": None,
        "tfidf_finalist": None,
    }

    # 1. Require explicit live arguments - fail closed if any is missing
    if inputs is None or expected_active_snapshot is None or client is None or tfidf_state is None:
        return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

    actual_client = client

    # 2. Derive or validate selected lexical contract
    if selected_lexical is None:
        try:
            selected_lexical = load_or_run_calibration(
                inputs,
                expected_active_snapshot=expected_active_snapshot,
                checkpoint=checkpoint,
                results_dir=r_dir,
            )
        except Exception:
            return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

    expected_immutable = build_expected_immutable_identity(
        inputs,
        selected_lexical,
        tfidf_state,
        active_snapshot_before=expected_active_snapshot,
    )

    # 3. Exact immutable identity validation
    manifest = checkpoint.manifest
    if manifest.schema_version != "phase8-sparse-manifest-v1" or manifest.experiment_version != "phase8-08b-v1":
        return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)
    imm = manifest.immutable_identity
    if not imm or not isinstance(imm, dict):
        return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

    for k, expected_v in expected_immutable.items():
        if k == "active_snapshot_before":
            continue
        if imm.get(k) != expected_v:
            return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

    # 3. Active snapshot and isolated TF-IDF collection validation (fail-closed)
    try:
        snap_now = snapshot_active_collection(actual_client)
        if snap_now != expected_active_snapshot:
            return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

        target_tfidf_name = tfidf_state.collection_name
        if not actual_client.collection_exists(target_tfidf_name):
            return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)
        info = actual_client.get_collection(target_tfidf_name)
        if getattr(info, "points_count", None) != 572:
            return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

        params = getattr(getattr(info, "config", None), "params", None)
        if params is None:
            return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)
        sparse_cfg = getattr(params, "sparse_vectors", None)
        if not isinstance(sparse_cfg, dict) or TFIDF_VECTOR_NAME not in sparse_cfg:
            return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

        scroll_res = actual_client.scroll(
            collection_name=target_tfidf_name,
            limit=580,
            with_payload=True,
            with_vectors=True,
        )
        points = scroll_res[0] if scroll_res else []
        if len(points) != 572:
            return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

        canonical_chunks_by_id = {
            (c.get("metadata", {}).get("chunk_id") if isinstance(c.get("metadata"), dict) else c.get("chunk_id")): c.get("text")
            for c in inputs.chunks
        }
        seen_chunk_ids = set()
        for p in points:
            if not p.payload:
                return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)
            c_id = p.payload.get("chunk_id")
            text = p.payload.get("text")
            if not c_id or not text or c_id not in canonical_chunks_by_id or canonical_chunks_by_id[c_id] != text:
                return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)
            seen_chunk_ids.add(c_id)
            if p.payload.get("vocabulary_fingerprint") != tfidf_state.encoder.vocabulary_fingerprint:
                return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)
            if p.payload.get("tfidf_formula_version") != TFIDF_FORMULA_VERSION:
                return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)
            if p.payload.get("corpus_fingerprint") != inputs.corpus_fingerprint:
                return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

            vec = p.vector.get(TFIDF_VECTOR_NAME) if isinstance(p.vector, dict) else p.vector
            if vec is None:
                return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)
            indices = vec.indices if hasattr(vec, "indices") else (vec.get("indices", []) if isinstance(vec, dict) else [])
            values = vec.values if hasattr(vec, "values") else (vec.get("values", []) if isinstance(vec, dict) else [])
            if not indices or not values or len(indices) != len(values):
                return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)
            if indices != sorted(indices) or len(set(indices)) != len(indices):
                return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)
            if not all(isinstance(v, (int, float)) and math.isfinite(v) and v != 0.0 for v in values):
                return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)
            l2 = sum(v * v for v in values)
            if not math.isclose(l2, 1.0, rel_tol=1e-3, abs_tol=1e-3):
                return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

        if seen_chunk_ids != set(canonical_chunks_by_id.keys()):
            return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

        snap_after = snapshot_active_collection(actual_client)
        if snap_after != expected_active_snapshot:
            return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)
    except Exception:
        return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

    # 4. Calibration verification: exact 70 rows (5 parameter + 2 tokenizer settings x 10 categories, all 3 reps)
    expected_categories = {
        "overall", "comparative", "direct_fact", "food_knowledge", "guide_planning",
        "holistic", "numerical", "relationship", "spanning", "temporal"
    }
    if len(checkpoint.calibration_rows) != 70:
        return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

    calib_by_stage_setting_cat = {}
    for r in checkpoint.calibration_rows:
        if r.get("status") != "completed" or str(r.get("successful_repetitions", "")).strip() != "3":
            return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)
        stage = r.get("calibration_stage")
        s_key = r.get("setting_key")
        cat = r.get("category")
        calib_by_stage_setting_cat[(stage, s_key, cat)] = r

    expected_param_keys = {s.setting_key for s in BM25_SETTINGS}
    expected_tok_keys = {"unicode_word", "underthesea_word"}

    for p_key in expected_param_keys:
        for cat in expected_categories:
            if ("parameter", p_key, cat) not in calib_by_stage_setting_cat:
                return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

    for t_key in expected_tok_keys:
        for cat in expected_categories:
            if ("tokenizer", t_key, cat) not in calib_by_stage_setting_cat:
                return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

    summary["bm25_parameter_settings_completed"] = len(expected_param_keys)
    summary["tokenizer_settings_completed"] = len(expected_tok_keys)

    # 5. Main settings verification: exact 200 result rows (20 settings x 10 categories, all 3 reps)
    if len(checkpoint.result_rows) != 200:
        return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

    expected_main_keys = {s.setting_key for s in RETRIEVAL_SETTINGS}
    res_by_setting_cat = {}
    for r in checkpoint.result_rows:
        if r.get("status") != "completed" or str(r.get("successful_repetitions", "")).strip() != "3":
            return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)
        res_by_setting_cat[(r.get("setting_key"), r.get("category"))] = r

    for m_key in expected_main_keys:
        for cat in expected_categories:
            if (m_key, cat) not in res_by_setting_cat:
                return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

    comp_main_keys = set(checkpoint.completed_setting_keys)
    summary["main_settings_completed"] = len(comp_main_keys)
    if comp_main_keys != expected_main_keys:
        return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

    # 6. Case records verification: exact 900 records (20 settings x 45 canonical cases, all 3 reps)
    if len(checkpoint.case_records) != 900:
        return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

    canonical_case_ids = {c.case_id for c in inputs.cases}
    if len(canonical_case_ids) != 45:
        return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

    cases_by_setting_id: dict[str, set[str]] = {}
    for c in checkpoint.case_records:
        if c.get("status") != "completed" or int(c.get("successful_repetitions", 0)) != 3:
            return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)
        cases_by_setting_id.setdefault(c.get("setting_key"), set()).add(c.get("case_id"))

    if set(cases_by_setting_id.keys()) != expected_main_keys:
        return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

    for m_key, c_ids in cases_by_setting_id.items():
        if c_ids != canonical_case_ids:
            return ReconciliationResult(complete=False, summary=summary, bm25_finalist=None, tfidf_finalist=None)

    # 7. Build dense controls map
    dense_controls: dict[str, FinalistEvidence] = {}
    rows_by_setting_cat = {
        (r.get("setting_key"), r.get("category")): r
        for r in checkpoint.result_rows
    }

    for s in RETRIEVAL_SETTINGS:
        if s.path == "dense_only" and s.dense_setting_key:
            row = rows_by_setting_cat.get((s.setting_key, "overall"))
            if row:
                dense_controls[s.dense_setting_key] = FinalistEvidence(
                    setting_key=s.setting_key,
                    dense_setting_key=s.dense_setting_key,
                    sparse_family="",
                    status=row.get("status", ""),
                    successful_repetitions=int(row.get("successful_repetitions", 0)),
                    fusion_recall_at_10=float(row.get("fusion_recall_at_10", 0.0)),
                    recall_at_5=float(row.get("recall_at_5", 0.0)),
                    ndcg_at_5=float(row.get("ndcg_at_5", 0.0)),
                    mrr_at_5=float(row.get("mrr_at_5", 0.0)),
                    warm_total_p95_ms=float(row.get("warm_total_p95_ms", 0.0)),
                    all_category_guardrails_pass=True,
                )

    # Evaluate guardrails, gates, bootstrap for all settings vs controls
    candidate_evidences: list[FinalistEvidence] = []
    cases_by_setting: dict[str, list[dict]] = {}
    for c in checkpoint.case_records:
        cases_by_setting.setdefault(c["setting_key"], []).append(c)

    updated_rows = [dict(r) for r in checkpoint.result_rows]

    for setting in RETRIEVAL_SETTINGS:
        key = setting.setting_key
        row = next((r for r in updated_rows if r.get("setting_key") == key and r.get("category") == "overall"), None)
        if not row:
            continue

        dense_key = setting.dense_setting_key
        control = dense_controls.get(dense_key) if dense_key else None

        cand_cases = cases_by_setting.get(key, [])
        cand_d5 = [
            DepthCaseMetrics(
                case_id=c["case_id"],
                category=c["category"],
                depth=5,
                recall=float(c.get("recall_at_5", 0.0)),
                mrr=float(c.get("mrr_at_5", 0.0)),
                ndcg=float(c.get("ndcg_at_5", 0.0)),
                hit=float(c.get("recall_at_5", 0.0)) > 0.0,
                relevant_keys=(),
                ranked_keys=(),
            )
            for c in cand_cases
        ]

        all_guards_pass = True
        if control:
            ctrl_cases = cases_by_setting.get(control.setting_key, [])
            ctrl_d5 = [
                DepthCaseMetrics(
                    case_id=c["case_id"],
                    category=c["category"],
                    depth=5,
                    recall=float(c.get("recall_at_5", 0.0)),
                    mrr=float(c.get("mrr_at_5", 0.0)),
                    ndcg=float(c.get("ndcg_at_5", 0.0)),
                    hit=float(c.get("recall_at_5", 0.0)) > 0.0,
                    relevant_keys=(),
                    ranked_keys=(),
                )
                for c in ctrl_cases
            ]

            # Category guardrails
            categories = sorted({c.category for c in cand_d5})
            for cat in categories:
                c_cand = [m for m in cand_d5 if m.category == cat]
                c_ctrl = [m for m in ctrl_d5 if m.category == cat]
                g_pass, _ = evaluate_depth_category_guardrails(c_ctrl, c_cand)
                if not g_pass:
                    all_guards_pass = False

                # update category row
                cat_r = next((r for r in updated_rows if r.get("setting_key") == key and r.get("category") == cat), None)
                if cat_r:
                    cat_r["category_guardrail_pass"] = g_pass

            # Deltas & Bootstrap vs control
            d_r5 = float(row.get("recall_at_5", 0.0)) - control.recall_at_5
            d_mrr5 = float(row.get("mrr_at_5", 0.0)) - control.mrr_at_5
            d_ndcg5 = float(row.get("ndcg_at_5", 0.0)) - control.ndcg_at_5
            d_r10 = float(row.get("fusion_recall_at_10", 0.0)) - control.fusion_recall_at_10

            row["delta_recall_at_5"] = d_r5
            row["delta_mrr_at_5"] = d_mrr5
            row["delta_ndcg_at_5"] = d_ndcg5
            row["delta_fusion_recall_at_10"] = d_r10

            ctrl_cm = [
                CaseMetrics(
                    case_id=m.case_id,
                    category=m.category,
                    recall_at_5=m.recall,
                    mrr_at_5=m.mrr,
                    ndcg_at_5=m.ndcg,
                    hit=m.hit,
                    relevant_keys=m.relevant_keys,
                    ranked_keys=m.ranked_keys,
                )
                for m in ctrl_d5
            ]
            cand_cm = [
                CaseMetrics(
                    case_id=m.case_id,
                    category=m.category,
                    recall_at_5=m.recall,
                    mrr_at_5=m.mrr,
                    ndcg_at_5=m.ndcg,
                    hit=m.hit,
                    relevant_keys=m.relevant_keys,
                    ranked_keys=m.ranked_keys,
                )
                for m in cand_d5
            ]
            bs_intervals = paired_bootstrap_intervals(ctrl_cm, cand_cm, samples=10_000, seed=42)

            row["recall_ci_lower"] = bs_intervals["recall"].lower
            row["recall_ci_upper"] = bs_intervals["recall"].upper
            row["mrr_ci_lower"] = bs_intervals["mrr"].lower
            row["mrr_ci_upper"] = bs_intervals["mrr"].upper
            row["ndcg_ci_lower"] = bs_intervals["ndcg"].lower
            row["ndcg_ci_upper"] = bs_intervals["ndcg"].upper

            f_gate = float(row.get("fusion_recall_at_10", 0.0)) >= control.fusion_recall_at_10
            r_gate = float(row.get("recall_at_5", 0.0)) >= control.recall_at_5 - 0.005
            lat_gate = float(row.get("warm_total_p95_ms", 0.0)) <= 2.0 * control.warm_total_p95_ms
            c_gate = row.get("status") == "completed" and int(row.get("successful_repetitions", 0)) == 3
            eligible = f_gate and r_gate and lat_gate and c_gate and all_guards_pass

            row["fusion_recall_gate"] = f_gate
            row["final_recall_gate"] = r_gate
            row["latency_gate"] = lat_gate
            row["complete_gate"] = c_gate
            row["category_guardrail_pass"] = all_guards_pass
            row["all_category_guardrails_pass"] = all_guards_pass
            row["finalist_eligible"] = eligible

            if setting.sparse_family:
                candidate_evidences.append(
                    FinalistEvidence(
                        setting_key=key,
                        dense_setting_key=dense_key,
                        sparse_family=setting.sparse_family,
                        status=row["status"],
                        successful_repetitions=int(row.get("successful_repetitions", 0)),
                        fusion_recall_at_10=float(row.get("fusion_recall_at_10", 0.0)),
                        recall_at_5=float(row.get("recall_at_5", 0.0)),
                        ndcg_at_5=float(row.get("ndcg_at_5", 0.0)),
                        mrr_at_5=float(row.get("mrr_at_5", 0.0)),
                        warm_total_p95_ms=float(row.get("warm_total_p95_ms", 0.0)),
                        all_category_guardrails_pass=all_guards_pass,
                    )
                )
        else:
            row["all_category_guardrails_pass"] = True
            row["complete_gate"] = True

    # Select finalists
    bm25_finalist = select_family_finalist(candidate_evidences, dense_controls, "bm25")
    tfidf_finalist = select_family_finalist(candidate_evidences, dense_controls, "tfidf")

    bm25_key = bm25_finalist.setting_key if bm25_finalist else None
    tfidf_key = tfidf_finalist.setting_key if tfidf_finalist else None

    for r in updated_rows:
        if r.get("category") == "overall":
            s_key = r.get("setting_key")
            if s_key == bm25_key or s_key == tfidf_key:
                r["finalist_selected"] = "true"
            else:
                r["finalist_selected"] = "false"

    # Only write results.csv if there are actual diffs
    needs_write = not res_path.exists()
    if not needs_write:
        for orig_r, new_r in zip(checkpoint.result_rows, updated_rows):
            for k in RESULT_COLUMNS:
                if str(orig_r.get(k, "")) != str(new_r.get(k, "")):
                    needs_write = True
                    break
            if needs_write:
                break

    if needs_write:
        upsert_result_rows(updated_rows, res_path)

    summary["reconciliation_complete"] = True
    summary["bm25_finalist"] = bm25_key
    summary["tfidf_finalist"] = tfidf_key

    return ReconciliationResult(
        complete=True,
        summary=summary,
        bm25_finalist=bm25_key,
        tfidf_finalist=tfidf_key,
    )


# ---------------------------------------------------------------------------
# Notebook Display Helpers
# ---------------------------------------------------------------------------

def environment_table():
    import importlib.metadata
    import platform
    import polars as pl

    try:
        qdrant_ver = importlib.metadata.version("qdrant-client")
    except Exception:
        qdrant_ver = "unknown"

    try:
        underthesea_ver = importlib.metadata.version("underthesea")
    except Exception:
        underthesea_ver = "unknown"

    data = [
        {"Property": "OS / Kernel", "Value": f"{platform.system()} {platform.release()}"},
        {"Property": "Python Version", "Value": platform.python_version()},
        {"Property": "Qdrant Client Version", "Value": qdrant_ver},
        {"Property": "Underthesea Version", "Value": underthesea_ver},
    ]
    return pl.DataFrame(data)


def canonical_inputs_table(inputs: SparseBenchmarkInputs):
    import polars as pl
    from collections import Counter

    cat_counts = Counter(c.category for c in inputs.cases)
    rows = [
        {"Item": "Total Canonical Chunks", "Count / Value": str(len(inputs.chunks))},
        {"Item": "Total Golden V3 Cases", "Count / Value": str(len(inputs.cases))},
        {"Item": "Corpus Fingerprint (12 chars)", "Count / Value": inputs.corpus_fingerprint[:12]},
        {"Item": "Golden V3 Fingerprint (12 chars)", "Count / Value": inputs.golden_fingerprint[:12]},
        {"Item": "Chunker Fingerprint (12 chars)", "Count / Value": inputs.chunker_fingerprint[:12]},
    ]
    for cat, cnt in sorted(cat_counts.items()):
        rows.append({"Item": f"Category: {cat}", "Count / Value": str(cnt)})
    return pl.DataFrame(rows)


def dense_prerequisite_table(prerequisites: tuple[DensePrerequisite, ...]):
    import polars as pl

    data = [
        {
            "Dense Setting": p.dense_setting_key,
            "Model ID": p.model_id,
            "Dimension": p.dimension,
            "Collection Name": p.collection_name,
            "Point Count": p.point_count,
            "Recall@5": f"{p.csv_recall_at_5:.4f}",
            "nDCG@5": f"{p.csv_ndcg_at_5:.4f}",
            "MRR@5": f"{p.csv_mrr_at_5:.4f}",
            "p95 Latency (ms)": f"{p.csv_p95_latency_ms:.1f}",
        }
        for p in prerequisites
    ]
    return pl.DataFrame(data)


def bm25_parameter_table():
    import polars as pl

    data = [
        {"Order": i, "Setting Key": s.setting_key, "k1": s.k1, "b": s.b}
        for i, s in enumerate(BM25_SETTINGS, start=1)
    ]
    return pl.DataFrame(data)


def calibration_table(checkpoint: CheckpointState):
    import polars as pl

    rows = [r for r in checkpoint.calibration_rows if r.get("category") == "overall"]
    if not rows:
        return pl.DataFrame({"Status": ["No calibration data yet"]})
    return pl.DataFrame(rows)


def retrieval_settings_table():
    import polars as pl

    data = [
        {
            "Order": s.order,
            "Setting Key": s.setting_key,
            "Setting Label": s.setting_label,
            "Path": s.path,
            "Dense Setting": s.dense_setting_key or "-",
            "Sparse Family": s.sparse_family or "-",
            "Fusion Method": s.fusion_method or "-",
        }
        for s in RETRIEVAL_SETTINGS
    ]
    return pl.DataFrame(data)


def quality_table(checkpoint: CheckpointState):
    import polars as pl

    rows = [r for r in checkpoint.result_rows if r.get("category") == "overall"]
    if not rows:
        return pl.DataFrame({"Status": ["No main results yet"]})
    return pl.DataFrame(rows)


def stage_recall_table(checkpoint: CheckpointState):
    import polars as pl

    rows = [
        {
            "Setting Key": r.get("setting_key"),
            "Dense Recall@30": r.get("dense_recall_at_30"),
            "Sparse Recall@30": r.get("sparse_recall_at_30"),
            "Candidate Union Recall": r.get("candidate_union_recall"),
            "Fusion Recall@10": r.get("fusion_recall_at_10"),
            "Final Recall@5": r.get("recall_at_5"),
        }
        for r in checkpoint.result_rows
        if r.get("category") == "overall"
    ]
    if not rows:
        return pl.DataFrame({"Status": ["No stage recall data yet"]})
    return pl.DataFrame(rows)


def category_guardrail_table(checkpoint: CheckpointState):
    import polars as pl

    rows_by_setting_cat = {
        (r.get("setting_key"), r.get("category")): r
        for r in checkpoint.result_rows
    }

    # Find dense controls
    dense_controls = {}
    for s in RETRIEVAL_SETTINGS:
        if s.path == "dense_only" and s.dense_setting_key:
            dense_controls[s.dense_setting_key] = {
                cat: rows_by_setting_cat.get((s.setting_key, cat))
                for cat in {r.get("category") for r in checkpoint.result_rows if r.get("category") != "overall"}
            }

    table_rows = []
    for s in RETRIEVAL_SETTINGS:
        if s.path == "dense_only":
            continue
        ctrl_cats = dense_controls.get(s.dense_setting_key, {})
        for cat in sorted({r.get("category") for r in checkpoint.result_rows if r.get("category") != "overall"}):
            cand_r = rows_by_setting_cat.get((s.setting_key, cat))
            if not cand_r:
                continue
            ctrl_r = ctrl_cats.get(cat)
            ctrl_ndcg = float(ctrl_r.get("ndcg_at_5", 0.0)) if ctrl_r and ctrl_r.get("ndcg_at_5") else 0.0
            cand_ndcg = float(cand_r.get("ndcg_at_5", 0.0)) if cand_r.get("ndcg_at_5") else 0.0
            delta_ndcg = cand_ndcg - ctrl_ndcg if ctrl_r else 0.0
            table_rows.append({
                "Setting Key": s.setting_key,
                "Category": cat,
                "Candidate Recall@5": f"{float(cand_r.get('recall_at_5', 0.0)):.4f}" if cand_r.get("recall_at_5") else "-",
                "Candidate nDCG@5": f"{cand_ndcg:.4f}",
                "Control nDCG@5": f"{ctrl_ndcg:.4f}" if ctrl_r else "-",
                "Δ nDCG@5": f"{delta_ndcg:+.4f}" if ctrl_r else "-",
                "Guardrail Pass": str(cand_r.get("category_guardrail_pass", "")),
            })

    if not table_rows:
        return pl.DataFrame({"Status": ["No category guardrail data yet"]})
    return pl.DataFrame(table_rows)


def latency_resource_table(checkpoint: CheckpointState):
    import polars as pl

    rows = [
        {
            "Setting Key": r.get("setting_key"),
            "Dense Query p95 (ms)": r.get("dense_query_p95_ms"),
            "Sparse Query p95 (ms)": r.get("sparse_query_p95_ms"),
            "Fusion p95 (ms)": r.get("fusion_p95_ms"),
            "Warm Total p50 (ms)": r.get("warm_total_p50_ms"),
            "Warm Total p95 (ms)": r.get("warm_total_p95_ms"),
            "Peak RSS (MB)": r.get("observed_peak_rss_mb"),
        }
        for r in checkpoint.result_rows
        if r.get("category") == "overall"
    ]
    if not rows:
        return pl.DataFrame({"Status": ["No latency data yet"]})
    return pl.DataFrame(rows)


def case_disagreement_table(checkpoint: CheckpointState):
    import polars as pl

    if not checkpoint.case_records:
        return pl.DataFrame({"Status": ["No case records yet"]})

    cases_by_setting: dict[str, dict[str, dict]] = {}
    for c in checkpoint.case_records:
        cases_by_setting.setdefault(c["setting_key"], {})[c["case_id"]] = c

    dense_key = "dense__huydang-dek21-embedding-768"
    hybrid_key = "hybrid-bm25-weighted__huydang-dek21-embedding-768"
    sparse_key = "bm25-only"

    dense_cases = cases_by_setting.get(dense_key, {})
    hybrid_cases = cases_by_setting.get(hybrid_key, {})
    sparse_cases = cases_by_setting.get(sparse_key, {})

    disagreements = []
    for case_id, h_case in hybrid_cases.items():
        d_case = dense_cases.get(case_id, {})
        s_case = sparse_cases.get(case_id, {})

        d_r5 = float(d_case.get("recall_at_5", 0.0)) if d_case.get("recall_at_5") else 0.0
        h_r5 = float(h_case.get("recall_at_5", 0.0)) if h_case.get("recall_at_5") else 0.0
        s_r5 = float(s_case.get("recall_at_5", 0.0)) if s_case.get("recall_at_5") else 0.0

        d_ndcg5 = float(d_case.get("ndcg_at_5", 0.0)) if d_case.get("ndcg_at_5") else 0.0
        h_ndcg5 = float(h_case.get("ndcg_at_5", 0.0)) if h_case.get("ndcg_at_5") else 0.0

        diff_recall = not math.isclose(d_r5, h_r5, abs_tol=1e-4)
        diff_ndcg = not math.isclose(d_ndcg5, h_ndcg5, abs_tol=1e-4)

        if diff_recall or diff_ndcg or not math.isclose(d_r5, s_r5, abs_tol=1e-4):
            dis_type = []
            if h_r5 > d_r5:
                dis_type.append("Hybrid improved Recall")
            elif h_r5 < d_r5:
                dis_type.append("Hybrid regressed Recall")
            if h_ndcg5 > d_ndcg5 + 0.001:
                dis_type.append("Hybrid improved nDCG")
            elif h_ndcg5 < d_ndcg5 - 0.001:
                dis_type.append("Hybrid regressed nDCG")
            if s_r5 > d_r5:
                dis_type.append("Sparse beat Dense")
            elif d_r5 > s_r5:
                dis_type.append("Dense beat Sparse")

            disagreements.append({
                "Case ID": case_id,
                "Category": h_case.get("category", ""),
                "Dense R@5": f"{d_r5:.4f}",
                "Sparse R@5": f"{s_r5:.4f}",
                "Hybrid R@5": f"{h_r5:.4f}",
                "Dense nDCG@5": f"{d_ndcg5:.4f}",
                "Hybrid nDCG@5": f"{h_ndcg5:.4f}",
                "Δ nDCG@5": f"{(h_ndcg5 - d_ndcg5):+.4f}",
                "Disagreement Type": "; ".join(dis_type) if dis_type else "Ranking difference",
            })

    if not disagreements:
        return pl.DataFrame({"Status": ["No case disagreements observed"]})
    return pl.DataFrame(disagreements)


def bootstrap_finalist_table(checkpoint: CheckpointState):
    import polars as pl

    rows = [
        {
            "Setting Key": r.get("setting_key"),
            "Path": r.get("path"),
            "Recall@5": r.get("recall_at_5"),
            "Δ Recall@5": r.get("delta_recall_at_5"),
            "Recall 95% CI": f"[{r.get('recall_ci_lower', '')}, {r.get('recall_ci_upper', '')}]",
            "nDCG@5": r.get("ndcg_at_5"),
            "Δ nDCG@5": r.get("delta_ndcg_at_5"),
            "nDCG 95% CI": f"[{r.get('ndcg_ci_lower', '')}, {r.get('ndcg_ci_upper', '')}]",
            "Guardrails Pass": r.get("all_category_guardrails_pass"),
            "Eligible": r.get("finalist_eligible"),
            "Selected Finalist": r.get("finalist_selected"),
        }
        for r in checkpoint.result_rows
        if r.get("category") == "overall"
    ]
    if not rows:
        return pl.DataFrame({"Status": ["No finalist evaluation yet"]})
    return pl.DataFrame(rows)


def artifact_reconciliation_table(checkpoint: CheckpointState):
    import polars as pl

    data = [
        {"Artifact": "Manifest JSON", "Status": "Valid" if checkpoint.manifest else "Missing"},
        {"Artifact": "Calibration CSV Rows", "Count / Status": str(len(checkpoint.calibration_rows))},
        {"Artifact": "Results CSV Rows", "Count / Status": str(len(checkpoint.result_rows))},
        {"Artifact": "Case Records JSONL", "Count / Status": str(len(checkpoint.case_records))},
        {"Artifact": "Completed Settings", "Count / Status": f"{len(checkpoint.completed_setting_keys)} / 20"},
    ]
    return pl.DataFrame(data)
