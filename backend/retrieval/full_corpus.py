"""Canonical Full-corpus retrieval module for Phase 5.

Implements typed result models, private technical trace, exact Python RRF,
strict readiness, dense/sparse retrieval treatments, and service composition.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import sys
import time
from typing import Any, Literal

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from qdrant_client import QdrantClient, models

try:
    from backend.core.schema import (
        ComponentNotReadyError,
        InvalidQueryError,
        RetrievalConfigurationError,
        RetrievalDependencyError,
        RetrievedDocument,
    )
    from backend.embedding.full_corpus import (
        FullCorpusDenseRunner,
        resolve_snapshot,
    )
    from backend.embedding.sparse import (
        SparseState,
        SparseVector,
        build_vocabulary_index,
        encode_sparse_document,
        encode_sparse_query,
        load_sparse_state,
    )
    from backend.ingestion.full_corpus_pipeline import (
        FullCorpusCandidate,
        candidate_by_id,
        EXPECTED_CHUNK_COUNT,
        EXPECTED_CORPUS_IDENTITY,
        EXPECTED_SPARSE_SHA256,
    )
    from backend.reranking.cross_encoder import CrossEncoderReranker
    from backend.vectorstore.qdrant import (
        client_from_settings,
        validate_full_corpus_collection_info,
    )
except ModuleNotFoundError:
    from core.schema import (
        ComponentNotReadyError,
        InvalidQueryError,
        RetrievalConfigurationError,
        RetrievalDependencyError,
        RetrievedDocument,
    )
    from embedding.full_corpus import (
        FullCorpusDenseRunner,
        resolve_snapshot,
    )
    from embedding.sparse import (
        SparseState,
        SparseVector,
        build_vocabulary_index,
        encode_sparse_document,
        encode_sparse_query,
        load_sparse_state,
    )
    from ingestion.full_corpus_pipeline import (
        FullCorpusCandidate,
        candidate_by_id,
        EXPECTED_CHUNK_COUNT,
        EXPECTED_CORPUS_IDENTITY,
        EXPECTED_SPARSE_SHA256,
    )
    from reranking.cross_encoder import CrossEncoderReranker
    from vectorstore.qdrant import (
        client_from_settings,
        validate_full_corpus_collection_info,
    )

RetrievalTreatment = Literal["dense_bm25_rrf", "native_hybrid_rrf"]
RerankerMode = Literal["none", "minilm"]
Classification = Literal["PASS", "REVIEW_REQUIRED", "FAIL"]

REPO_ROOT = Path(__file__).resolve().parents[2]
BUILD_RECORDS_DIR = REPO_ROOT / "data/full_corpus_builds"
SPARSE_STATE_FILE = BUILD_RECORDS_DIR / "phase_3_sparse_state.json"


@dataclass(frozen=True)
class RetrievalTrace:
    """Private technical trace explaining the execution of a retrieval request.

    Guaranteed not to contain query text, corpus excerpts, payload text,
    absolute filesystem paths, or sensitive credentials.
    """

    candidate_id: str
    collection_name: str
    retrieval_treatment: RetrievalTreatment
    reranker: RerankerMode
    counts: dict[str, int]
    timings_ms: dict[str, float]
    stages: dict[str, list[dict[str, Any]]]
    rerank_status: str
    anomalies: tuple[str, ...]
    classification: Classification


@dataclass(frozen=True)
class RetrievalResult:
    """Typed result of a full-corpus retrieval request."""

    documents: list[RetrievedDocument]
    trace: RetrievalTrace


def reciprocal_rank_fusion(
    ranked_ids: Sequence[Sequence[str]],
    *,
    k: int = 60,
    limit: int = 30,
) -> list[tuple[str, float]]:
    """Deterministic Reciprocal Rank Fusion across ranked candidate branches.

    Formula: score(point_id) = sum(1.0 / (k + rank))
    - rank starts from 1 for each branch.
    - duplicates within a single branch are rejected.
    - tied scores break by ascending point ID string.
    - returns ordered list of (point_id, rrf_score) pairs up to `limit`.
    """
    if k <= 0:
        raise ValueError("k must be positive")
    if limit <= 0:
        raise ValueError("limit must be positive")

    scores: dict[str, float] = {}
    for branch in ranked_ids:
        seen: set[str] = set()
        for rank, point_id in enumerate(branch, start=1):
            if not isinstance(point_id, str) or not point_id.strip():
                raise ValueError(f"invalid point ID: {point_id!r}")
            if point_id in seen:
                raise ValueError(f"duplicate point ID within one branch: {point_id}")
            seen.add(point_id)
            scores[point_id] = scores.get(point_id, 0.0) + 1.0 / (k + rank)

    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:limit]


def rank_positive_bm25(scored_items: Sequence[tuple[str, float]]) -> list[str]:
    """Filter items with score > 0.0, sort descending by score, tie-break ascending by point_id."""
    positive = [(pid, float(score)) for pid, score in scored_items if score > 0.0]
    sorted_items = sorted(positive, key=lambda item: (-item[1], item[0]))
    return [pid for pid, _ in sorted_items]


def compute_sparse_dot_product(query_vec: SparseVector, doc_vec: SparseVector) -> float:
    """Compute dot product between a query sparse vector and document sparse vector."""
    if not query_vec.indices or not doc_vec.indices:
        return 0.0
    q_indices = set(query_vec.indices)
    score = 0.0
    for idx, val in zip(doc_vec.indices, doc_vec.values):
        if idx in q_indices:
            score += val
    return float(score)


REQUIRED_PAYLOAD_FIELDS = frozenset({"search_text", "source", "title", "heading_path", "evidence_parts"})
REQUIRED_EVIDENCE_PART_FIELDS = frozenset({"role", "start", "end", "text"})
ALLOWED_EVIDENCE_ROLES = frozenset({"body", "header", "condition"})


def validate_point_payload(point_id: str, payload: Any) -> dict[str, Any]:
    """Validate that point payload is a dict with exact 5 expected fields and valid types.

    Fails closed with RetrievalDependencyError if malformed.
    """
    if not isinstance(payload, dict):
        raise RetrievalDependencyError(f"Point {point_id} payload must be a dict, got {type(payload).__name__}")

    keys = set(payload.keys())
    if keys != REQUIRED_PAYLOAD_FIELDS:
        missing = sorted(REQUIRED_PAYLOAD_FIELDS - keys)
        extra = sorted(keys - REQUIRED_PAYLOAD_FIELDS)
        msg_parts = []
        if missing:
            msg_parts.append(f"missing: {', '.join(missing)}")
        if extra:
            msg_parts.append(f"extra: {', '.join(extra)}")
        raise RetrievalDependencyError(f"Point {point_id} payload fields mismatch: {'; '.join(msg_parts)}")

    if not isinstance(payload["search_text"], str) or not payload["search_text"].strip():
        raise RetrievalDependencyError(f"Point {point_id} search_text must be non-empty string")
    if not isinstance(payload["source"], str) or not payload["source"].strip():
        raise RetrievalDependencyError(f"Point {point_id} source must be non-empty string")
    if not isinstance(payload["title"], str):
        raise RetrievalDependencyError(f"Point {point_id} title must be string")
    if not isinstance(payload["heading_path"], list) or not all(isinstance(x, str) for x in payload["heading_path"]):
        raise RetrievalDependencyError(f"Point {point_id} heading_path must be list of strings")
    if not isinstance(payload["evidence_parts"], list):
        raise RetrievalDependencyError(f"Point {point_id} evidence_parts must be list")

    for idx, part in enumerate(payload["evidence_parts"]):
        if not isinstance(part, dict):
            raise RetrievalDependencyError(f"Point {point_id} evidence_parts[{idx}] must be dict")
        part_keys = set(part.keys())
        if part_keys != REQUIRED_EVIDENCE_PART_FIELDS:
            missing_parts = sorted(REQUIRED_EVIDENCE_PART_FIELDS - part_keys)
            extra_parts = sorted(part_keys - REQUIRED_EVIDENCE_PART_FIELDS)
            msg_parts = []
            if missing_parts:
                msg_parts.append(f"missing: {', '.join(missing_parts)}")
            if extra_parts:
                msg_parts.append(f"extra: {', '.join(extra_parts)}")
            raise RetrievalDependencyError(f"Point {point_id} evidence_parts[{idx}] fields mismatch: {'; '.join(msg_parts)}")

        role = part["role"]
        if not isinstance(role, str) or role not in ALLOWED_EVIDENCE_ROLES:
            raise RetrievalDependencyError(
                f"Point {point_id} evidence_parts[{idx}] invalid role: {role!r}. Allowed: {sorted(ALLOWED_EVIDENCE_ROLES)}"
            )

        text = part["text"]
        if not isinstance(text, str):
            raise RetrievalDependencyError(f"Point {point_id} evidence_parts[{idx}] text must be string")

        start = part["start"]
        end = part["end"]
        if (
            type(start) is not int
            or type(end) is not int
            or start < 0
            or end < start
        ):
            raise RetrievalDependencyError(
                f"Point {point_id} evidence_parts[{idx}] invalid start/end offsets: start={start!r}, end={end!r}"
            )

    return payload


class FullCorpusRetrievalService:
    """Canonical Full-corpus retrieval service executing treatments and reranking."""

    def __init__(
        self,
        candidate: FullCorpusCandidate,
        retrieval_treatment: RetrievalTreatment,
        reranker: RerankerMode,
        dense_runner: FullCorpusDenseRunner,
        sparse_state: SparseState,
        vocabulary_index: dict[str, int],
        client: QdrantClient,
        reranker_instance: CrossEncoderReranker | None = None,
    ) -> None:
        self.candidate = candidate
        self.retrieval_treatment = retrieval_treatment
        self.reranker = reranker
        self.dense_runner = dense_runner
        self.sparse_state = sparse_state
        self.vocabulary_index = vocabulary_index
        self.client = client
        self.reranker_instance = reranker_instance

    def search(self, query: str) -> RetrievalResult:
        if not isinstance(query, str) or not query.strip():
            raise InvalidQueryError("Query must be non-empty and non-whitespace string")

        t0 = time.perf_counter()
        timings: dict[str, float] = {}
        counts: dict[str, int] = {}
        stages: dict[str, list[dict[str, Any]]] = {}
        anomalies: list[str] = []

        # 1. Dense query
        t_dense_start = time.perf_counter()
        try:
            dense_vec = self.dense_runner.embed_queries([query])[0]
        except Exception as exc:
            raise RetrievalDependencyError("Dense query embedding failed") from exc

        try:
            dense_response = self.client.query_points(
                collection_name=self.candidate.collection_name,
                query=dense_vec,
                using="dense",
                limit=30,
                with_payload=["search_text", "source", "title", "heading_path", "evidence_parts"],
                with_vectors=False,
            )
        except Exception as exc:
            raise RetrievalDependencyError("Qdrant dense query failed") from exc

        t_dense_end = time.perf_counter()
        timings["dense_ms"] = round((t_dense_end - t_dense_start) * 1000.0, 3)
        dense_points = dense_response.points
        counts["dense"] = len(dense_points)

        dense_stage: list[dict[str, Any]] = []
        dense_ranked_ids: list[str] = []
        candidate_docs: dict[str, Any] = {}

        for rank, p in enumerate(dense_points, start=1):
            pid = str(p.id)
            score = float(p.score)
            if not math.isfinite(score):
                raise RetrievalDependencyError(f"Non-finite dense score: {score}")
            if pid in candidate_docs:
                raise RetrievalDependencyError(f"Duplicate point ID in dense results: {pid}")
            validate_point_payload(pid, p.payload)
            candidate_docs[pid] = p
            dense_ranked_ids.append(pid)
            dense_stage.append({"point_id": pid, "rank": rank, "score": score})

        stages["dense"] = dense_stage
        if len(dense_ranked_ids) == 0:
            anomalies.append("dense_zero_hits")

        # 2. Retrieval treatment
        if self.retrieval_treatment == "dense_bm25_rrf":
            t_bm25_start = time.perf_counter()
            sparse_q = encode_sparse_query(query, self.sparse_state)
            counts["sparse_in_vocab"] = len(sparse_q.indices)
            if len(sparse_q.indices) == 0:
                anomalies.append("sparse_query_no_vocabulary_tokens")

            bm25_scores: list[tuple[str, float]] = []
            for pid in dense_ranked_ids:
                text = candidate_docs[pid].payload["search_text"]
                doc_sparse = encode_sparse_document(text, self.sparse_state, self.vocabulary_index)
                score = compute_sparse_dot_product(sparse_q, doc_sparse)
                if not math.isfinite(score):
                    raise RetrievalDependencyError(f"Non-finite BM25 score: {score}")
                bm25_scores.append((pid, score))

            bm25_ranked_ids = rank_positive_bm25(bm25_scores)
            counts["bm25"] = len(bm25_ranked_ids)
            if len(dense_ranked_ids) > 0 and len(bm25_ranked_ids) == 0:
                anomalies.append("bm25_zero_matches")

            bm25_scores_map = dict(bm25_scores)
            bm25_stage = [
                {"point_id": pid, "rank": rank, "score": bm25_scores_map[pid]}
                for rank, pid in enumerate(bm25_ranked_ids, start=1)
            ]
            stages["bm25"] = bm25_stage
            t_bm25_end = time.perf_counter()
            timings["treatment_ms"] = round((t_bm25_end - t_bm25_start) * 1000.0, 3)

            branches = [dense_ranked_ids]
            if bm25_ranked_ids:
                branches.append(bm25_ranked_ids)

        elif self.retrieval_treatment == "native_hybrid_rrf":
            t_sparse_start = time.perf_counter()
            sparse_q = encode_sparse_query(query, self.sparse_state)
            counts["sparse_in_vocab"] = len(sparse_q.indices)
            sparse_points = []
            if len(sparse_q.indices) == 0:
                anomalies.append("sparse_query_no_vocabulary_tokens")
            else:
                try:
                    sparse_response = self.client.query_points(
                        collection_name=self.candidate.collection_name,
                        query=models.SparseVector(
                            indices=list(sparse_q.indices),
                            values=list(sparse_q.values),
                        ),
                        using="sparse",
                        limit=30,
                        with_payload=["search_text", "source", "title", "heading_path", "evidence_parts"],
                        with_vectors=False,
                    )
                    sparse_points = sparse_response.points
                except Exception as exc:
                    raise RetrievalDependencyError("Qdrant sparse query failed") from exc

            counts["sparse"] = len(sparse_points)
            if len(sparse_q.indices) > 0 and len(sparse_points) == 0:
                anomalies.append("sparse_zero_hits")

            sparse_stage: list[dict[str, Any]] = []
            sparse_ranked_ids: list[str] = []
            for rank, p in enumerate(sparse_points, start=1):
                pid = str(p.id)
                score = float(p.score)
                if not math.isfinite(score):
                    raise RetrievalDependencyError(f"Non-finite sparse score: {score}")
                if pid in sparse_ranked_ids:
                    raise RetrievalDependencyError(f"Duplicate point ID in sparse results: {pid}")
                validate_point_payload(pid, p.payload)
                if pid not in candidate_docs:
                    candidate_docs[pid] = p
                sparse_ranked_ids.append(pid)
                sparse_stage.append({"point_id": pid, "rank": rank, "score": score})

            stages["sparse"] = sparse_stage
            t_sparse_end = time.perf_counter()
            timings["treatment_ms"] = round((t_sparse_end - t_sparse_start) * 1000.0, 3)

            branches = [dense_ranked_ids]
            if sparse_ranked_ids:
                branches.append(sparse_ranked_ids)
        else:
            raise RetrievalConfigurationError(f"Unknown retrieval treatment: {self.retrieval_treatment}")

        # 3. RRF fusion
        t_rrf_start = time.perf_counter()
        fused = reciprocal_rank_fusion(branches, k=60, limit=30)
        counts["rrf_pre_rerank"] = len(fused)
        stages["rrf"] = [
            {"point_id": pid, "rank": rank, "score": round(score, 6)}
            for rank, (pid, score) in enumerate(fused, start=1)
        ]
        t_rrf_end = time.perf_counter()
        timings["rrf_ms"] = round((t_rrf_end - t_rrf_start) * 1000.0, 3)

        # 4. Reranker mode
        documents: list[RetrievedDocument] = []
        if self.reranker == "none":
            rerank_status = "not_applicable"
            timings["rerank_ms"] = 0.0
            final_fused = fused[:10]
            for pid, score in final_fused:
                pt = candidate_docs[pid]
                pl = pt.payload
                documents.append(
                    RetrievedDocument(
                        id=pid,
                        score=float(score),
                        text=pl["search_text"],
                        metadata={
                            "source": pl["source"],
                            "title": pl["title"],
                            "heading_path": list(pl.get("heading_path", [])),
                            "evidence_parts": pl.get("evidence_parts", []),
                        },
                    )
                )
        elif self.reranker == "minilm":
            if self.reranker_instance is None:
                raise ComponentNotReadyError("MiniLM reranker instance is not initialized")
            t_rerank_start = time.perf_counter()
            # Check for overlength pairs
            overlength = False
            for pid, _ in fused:
                st = candidate_docs[pid].payload["search_text"]
                tok_len = self.reranker_instance.input_token_count(query, st)
                if tok_len > self.reranker_instance.max_length:
                    overlength = True
                    break

            if overlength:
                rerank_status = "skipped_overlength"
                timings["rerank_ms"] = round((time.perf_counter() - t_rerank_start) * 1000.0, 3)
                final_fused = fused[:10]
                for pid, score in final_fused:
                    pt = candidate_docs[pid]
                    pl = pt.payload
                    documents.append(
                        RetrievedDocument(
                            id=pid,
                            score=float(score),
                            text=pl["search_text"],
                            metadata={
                                "source": pl["source"],
                                "title": pl["title"],
                                "heading_path": list(pl.get("heading_path", [])),
                                "evidence_parts": pl.get("evidence_parts", []),
                            },
                        )
                    )
            else:
                candidate_docs_for_rerank = [
                    RetrievedDocument(
                        id=pid,
                        score=float(score),
                        text=candidate_docs[pid].payload["search_text"],
                        metadata={},
                    )
                    for pid, score in fused
                ]
                rerank_scores = self.reranker_instance.score_documents(query, candidate_docs_for_rerank)
                ranked_pairs = sorted(
                    zip(rerank_scores, candidate_docs_for_rerank),
                    key=lambda item: (-item[0], item[1].id),
                )
                stages["rerank"] = [
                    {"point_id": doc.id, "rank": rank, "score": score}
                    for rank, (score, doc) in enumerate(ranked_pairs, start=1)
                ]
                final_pairs = ranked_pairs[:10]
                for score, doc in final_pairs:
                    pt = candidate_docs[doc.id]
                    pl = pt.payload
                    documents.append(
                        RetrievedDocument(
                            id=doc.id,
                            score=float(score),
                            text=pl["search_text"],
                            metadata={
                                "source": pl["source"],
                                "title": pl["title"],
                                "heading_path": list(pl.get("heading_path", [])),
                                "evidence_parts": pl.get("evidence_parts", []),
                            },
                        )
                    )
                rerank_status = "completed"
                timings["rerank_ms"] = round((time.perf_counter() - t_rerank_start) * 1000.0, 3)
        else:
            raise RetrievalConfigurationError(f"Unknown reranker mode: {self.reranker}")

        counts["final"] = len(documents)
        t_total_end = time.perf_counter()
        timings["total_ms"] = round((t_total_end - t0) * 1000.0, 3)

        classification: Classification = "REVIEW_REQUIRED" if anomalies else "PASS"

        trace = RetrievalTrace(
            candidate_id=self.candidate.candidate_id,
            collection_name=self.candidate.collection_name,
            retrieval_treatment=self.retrieval_treatment,
            reranker=self.reranker,
            counts=counts,
            timings_ms=timings,
            stages=stages,
            rerank_status=rerank_status,
            anomalies=tuple(anomalies),
            classification=classification,
        )
        return RetrievalResult(documents=documents, trace=trace)

    def close(self) -> None:
        if self.dense_runner is not None:
            self.dense_runner.close()
        if self.client is not None:
            self.client.close()


def build_full_corpus_retrieval_service(
    candidate_id: str,
    retrieval_treatment: RetrievalTreatment,
    reranker: RerankerMode = "none",
    *,
    settings: dict[str, Any] | None = None,
    client: QdrantClient | None = None,
) -> FullCorpusRetrievalService:
    """Build and strictly validate a canonical Full-corpus retrieval service."""
    try:
        candidate = candidate_by_id(candidate_id)
    except ValueError as exc:
        raise RetrievalConfigurationError(f"Unknown candidate ID: {candidate_id}") from exc

    if retrieval_treatment not in ("dense_bm25_rrf", "native_hybrid_rrf"):
        raise RetrievalConfigurationError(f"Unsupported retrieval treatment: {retrieval_treatment}")
    if reranker not in ("none", "minilm"):
        raise RetrievalConfigurationError(f"Unsupported reranker mode: {reranker}")

    # 1. Validate matching build record
    build_record_path = BUILD_RECORDS_DIR / f"{candidate.collection_name}.json"
    rel_build_record = f"data/full_corpus_builds/{candidate.collection_name}.json"
    if not build_record_path.is_file():
        raise ComponentNotReadyError(f"Build record does not exist: {rel_build_record}")

    try:
        record_data = json.loads(build_record_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ComponentNotReadyError(f"Failed to read build record: {rel_build_record}") from exc

    if record_data.get("status") != "complete":
        raise ComponentNotReadyError(f"Build record status is not complete: {record_data.get('status')}")
    if record_data.get("representation") != "A":
        raise ComponentNotReadyError(f"Build record representation is not A: {record_data.get('representation')}")
    if record_data.get("schema_version") != "phase_4_full_corpus_build:v1":
        raise ComponentNotReadyError(f"Build record schema_version invalid: {record_data.get('schema_version')}")

    corpus_info = record_data.get("corpus", {})
    if corpus_info.get("identity") != EXPECTED_CORPUS_IDENTITY:
        raise ComponentNotReadyError(f"Corpus identity mismatch in build record: {corpus_info.get('identity')}")
    if corpus_info.get("chunk_count") != EXPECTED_CHUNK_COUNT:
        raise ComponentNotReadyError(f"Chunk count mismatch in build record: {corpus_info.get('chunk_count')}")

    dense_info = record_data.get("dense", {})
    if dense_info.get("candidate_id") != candidate.candidate_id:
        raise ComponentNotReadyError(f"Dense candidate_id mismatch: {dense_info.get('candidate_id')}")
    if dense_info.get("dimension") != candidate.dense_spec.dimension:
        raise ComponentNotReadyError(f"Dense dimension mismatch: {dense_info.get('dimension')}")
    if dense_info.get("model_id") != candidate.dense_spec.model_id:
        raise ComponentNotReadyError(f"Dense model_id mismatch: {dense_info.get('model_id')}")
    if dense_info.get("revision") != candidate.dense_spec.revision:
        raise ComponentNotReadyError(f"Dense revision mismatch: {dense_info.get('revision')}")

    sparse_info = record_data.get("sparse", {})
    if sparse_info.get("schema_version") != "phase_3_sparse_state:v1":
        raise ComponentNotReadyError(f"Sparse schema_version mismatch: {sparse_info.get('schema_version')}")
    if sparse_info.get("state_sha256") != EXPECTED_SPARSE_SHA256:
        raise ComponentNotReadyError(f"Sparse state SHA256 mismatch: {sparse_info.get('state_sha256')}")
    if sparse_info.get("vocabulary_size") != 5662:
        raise ComponentNotReadyError(f"Sparse vocabulary size mismatch: {sparse_info.get('vocabulary_size')}")

    # 2. Validate sparse state file
    rel_sparse_state = "data/full_corpus_builds/phase_3_sparse_state.json"
    if not SPARSE_STATE_FILE.is_file():
        raise ComponentNotReadyError(f"Sparse state file not found: {rel_sparse_state}")

    state_bytes = SPARSE_STATE_FILE.read_bytes()
    state_sha = hashlib.sha256(state_bytes).hexdigest()
    if state_sha != EXPECTED_SPARSE_SHA256:
        raise ComponentNotReadyError(f"Sparse state SHA-256 mismatch: {state_sha} != {EXPECTED_SPARSE_SHA256}")

    sparse_state = load_sparse_state(SPARSE_STATE_FILE)
    if sparse_state.document_count != EXPECTED_CHUNK_COUNT:
        raise ComponentNotReadyError(f"Sparse state document count mismatch: {sparse_state.document_count}")
    if len(sparse_state.vocabulary) != 5662:
        raise ComponentNotReadyError(f"Sparse state vocabulary size mismatch: {len(sparse_state.vocabulary)}")
    if sparse_state.corpus_identity != EXPECTED_CORPUS_IDENTITY:
        raise ComponentNotReadyError(f"Sparse state corpus identity mismatch: {sparse_state.corpus_identity}")

    vocab_index = build_vocabulary_index(sparse_state)

    # 3. Validate live Qdrant collection
    if client is None:
        client = client_from_settings(settings)

    if not client.collection_exists(candidate.collection_name):
        raise ComponentNotReadyError(f"Qdrant collection {candidate.collection_name} does not exist")

    info = client.get_collection(candidate.collection_name)
    validate_full_corpus_collection_info(info, candidate.dense_spec.dimension)
    if info.points_count != EXPECTED_CHUNK_COUNT:
        raise ComponentNotReadyError(
            f"Collection {candidate.collection_name} point count mismatch: {info.points_count} != {EXPECTED_CHUNK_COUNT}"
        )

    # 4. Resolve and load dense model
    try:
        snapshot_path = resolve_snapshot(candidate.dense_spec, allow_download=False)
        dense_runner = FullCorpusDenseRunner(candidate.dense_spec, snapshot_path)
        dense_runner.load()
        warm_vec = dense_runner.embed_queries(["ấm trà cung đình Huế"])
        if len(warm_vec) != 1 or len(warm_vec[0]) != candidate.dense_spec.dimension:
            raise ComponentNotReadyError(f"Warm-up embedding output invalid for {candidate.candidate_id}")
    except Exception as exc:
        raise ComponentNotReadyError(f"Dense model readiness failed for {candidate.candidate_id}") from exc

    # 5. MiniLM reranker if requested
    reranker_instance = None
    if reranker == "minilm":
        try:
            reranker_instance = CrossEncoderReranker()
            reranker_instance.load()
            reranker_instance.warm_up()
        except Exception as exc:
            dense_runner.close()
            raise ComponentNotReadyError("MiniLM reranker readiness failed") from exc

    return FullCorpusRetrievalService(
        candidate=candidate,
        retrieval_treatment=retrieval_treatment,
        reranker=reranker,
        dense_runner=dense_runner,
        sparse_state=sparse_state,
        vocabulary_index=vocab_index,
        client=client,
        reranker_instance=reranker_instance,
    )
