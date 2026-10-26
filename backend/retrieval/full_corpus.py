"""Canonical Full-corpus retrieval module for Phase 5.

Implements typed result models, private technical trace, exact Python RRF,
strict readiness, dense/sparse retrieval treatments, and service composition.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
import hashlib
import json
import math
from pathlib import Path
import time
from typing import Any, Literal

from qdrant_client import QdrantClient, models

from core.schema import (
    ComponentNotReadyError,
    InvalidQueryError,
    RetrievalConfigurationError,
    RetrievalDependencyError,
    RetrievedDocument,
    domain_for_source,
    point_id_for_chunk_id,
    validate_chunk_id,
)
from core.settings_loader import load_settings
from embedding.full_corpus import (
    FullCorpusDenseRunner,
    OpenRouterDenseRunner,
    create_dense_runner,
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
    SPARSE_STATE_PATH,
    FullCorpusCandidate,
    build_record_path,
    candidate_by_id,
)
from ingestion.source_state import (
    FULL_CORPUS_BUILD_SCHEMA,
    FULL_CORPUS_PAYLOAD_SCHEMA_V2,
    compute_corpus_state,
    discover_full_corpus_files,
    verify_full_corpus_record_freshness,
)
from vectorstore.qdrant import (
    client_from_settings,
    validate_full_corpus_collection_info,
)

RetrievalTreatment = Literal["dense_bm25_rrf", "native_hybrid_rrf"]
RerankerMode = Literal["none"]
Classification = Literal["PASS", "REVIEW_REQUIRED", "FAIL"]

BACKEND_DIR = Path(__file__).resolve().parents[1]


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


def order_by_score_then_point_id(points: Sequence[Any]) -> list[Any]:
    """Sort Qdrant scored points descending by score, tie-break ascending by point_id.

    Qdrant không cam kết thứ tự giữa các điểm bằng điểm (đổi theo `limit` và trạng thái nội bộ, B12);
    phá hòa như `rank_positive_bm25` để nhánh sparse của `native_hybrid_rrf` tất định.
    """
    return sorted(points, key=lambda point: (-float(point.score), str(point.id)))


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


REQUIRED_PAYLOAD_FIELDS = frozenset(
    {
        "search_text",
        "source",
        "title",
        "heading_path",
        "evidence_parts",
        "chunk_id",
        "domain",
    }
)
REQUIRED_EVIDENCE_PART_FIELDS = frozenset({"role", "start", "end", "text"})
ALLOWED_EVIDENCE_ROLES = frozenset({"body", "header", "condition"})


def validate_point_payload(point_id: str, payload: Any) -> dict[str, Any]:
    """Validate that point payload is a dict with exact 7 expected fields and valid types.

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

    source = payload["source"]
    chunk_id = payload["chunk_id"]
    domain = payload["domain"]

    try:
        validate_chunk_id(source, chunk_id)
    except Exception:
        raise RetrievalDependencyError(f"Point {point_id} has invalid chunk identity relation") from None

    try:
        expected_point_id = point_id_for_chunk_id(chunk_id)
    except Exception:
        raise RetrievalDependencyError(f"Point {point_id} cannot compute point ID from chunk identity") from None

    if str(expected_point_id) != str(point_id):
        raise RetrievalDependencyError(f"Point {point_id} chunk identity does not match point ID")

    try:
        expected_domain = domain_for_source(source)
    except Exception:
        raise RetrievalDependencyError(f"Point {point_id} has invalid source for domain derivation") from None

    if domain != expected_domain:
        raise RetrievalDependencyError(f"Point {point_id} has domain mismatch")

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
            raise RetrievalDependencyError(f"Point {point_id} evidence_parts[{idx}] invalid role")

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
            raise RetrievalDependencyError(f"Point {point_id} evidence_parts[{idx}] invalid start/end offsets")

    return payload


def format_stage_entry(
    point_id: str,
    payload: Mapping[str, Any],
    rank: int,
    score: float,
) -> dict[str, Any]:
    """Format an allowlisted stage row for technical trace.

    Contains only point_id, chunk_id, domain, rank, score.
    """
    return {
        "point_id": str(point_id),
        "chunk_id": payload["chunk_id"],
        "domain": payload["domain"],
        "rank": rank,
        "score": float(score),
    }


def build_retrieved_document(
    payload: Mapping[str, Any],
    final_score: float,
) -> RetrievedDocument:
    """Build canonical RetrievedDocument with logical chunk_id and 5 metadata fields."""
    return RetrievedDocument(
        id=payload["chunk_id"],
        score=float(final_score),
        text=payload["search_text"],
        metadata={
            "source": payload["source"],
            "title": payload["title"],
            "heading_path": list(payload.get("heading_path", [])),
            "evidence_parts": list(payload.get("evidence_parts", [])),
            "domain": payload["domain"],
        },
    )


def assemble_final_documents(
    candidate_docs: Mapping[str, Any],
    ranked_point_ids_and_scores: Sequence[tuple[str, float]],
) -> list[RetrievedDocument]:
    """Assemble final RetrievedDocument list up to limit using validated candidate doc payloads."""
    documents: list[RetrievedDocument] = []
    for pid, score in ranked_point_ids_and_scores:
        pt = candidate_docs[pid]
        documents.append(build_retrieved_document(pt.payload, score))
    return documents


def validate_full_corpus_build_record(
    record_data: Mapping[str, Any],
    candidate: FullCorpusCandidate,
    current_sources: Mapping[str, str],
) -> None:
    """Kiểm build record khớp candidate, schema Qdrant và corpus hiện tại (freshness).

    Fails closed with ComponentNotReadyError.
    """
    if record_data.get("status") != "complete":
        raise ComponentNotReadyError(f"Build record status is not complete: {record_data.get('status')}")
    if record_data.get("representation") != "A":
        raise ComponentNotReadyError(f"Build record representation is not A: {record_data.get('representation')}")
    if record_data.get("schema_version") != FULL_CORPUS_BUILD_SCHEMA:
        raise ComponentNotReadyError(
            f"Build record schema_version invalid: {record_data.get('schema_version')}, expected {FULL_CORPUS_BUILD_SCHEMA}"
        )
    if record_data.get("collection_name") != candidate.collection_name:
        raise ComponentNotReadyError(
            f"Build record collection_name mismatch: {record_data.get('collection_name')}, expected {candidate.collection_name}"
        )

    qdrant_info = record_data.get("qdrant", {})
    if not isinstance(qdrant_info, dict):
        raise ComponentNotReadyError("Build record missing qdrant info dictionary")
    if qdrant_info.get("payload_schema_version") != FULL_CORPUS_PAYLOAD_SCHEMA_V2:
        raise ComponentNotReadyError(
            f"Build record payload_schema_version invalid: {qdrant_info.get('payload_schema_version')}, expected {FULL_CORPUS_PAYLOAD_SCHEMA_V2}"
        )
    if qdrant_info.get("dense_vector_name") != "dense":
        raise ComponentNotReadyError(
            f"Build record qdrant dense_vector_name invalid: {qdrant_info.get('dense_vector_name')}, expected 'dense'"
        )
    if qdrant_info.get("sparse_vector_name") != "sparse":
        raise ComponentNotReadyError(
            f"Build record qdrant sparse_vector_name invalid: {qdrant_info.get('sparse_vector_name')}, expected 'sparse'"
        )
    if qdrant_info.get("distance") != "cosine":
        raise ComponentNotReadyError(
            f"Build record qdrant distance invalid: {qdrant_info.get('distance')}, expected 'cosine'"
        )

    corpus_info = record_data.get("corpus", {})
    if qdrant_info.get("point_count") != corpus_info.get("chunk_count"):
        raise ComponentNotReadyError(
            f"Build record qdrant point_count invalid: {qdrant_info.get('point_count')}, expected corpus chunk_count {corpus_info.get('chunk_count')}"
        )

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

    fresh, _ = verify_full_corpus_record_freshness(current_sources, record_data)
    if not fresh:
        raise ComponentNotReadyError("Full-corpus source state is stale")


class FullCorpusRetrievalService:
    """Canonical Full-corpus retrieval service: dense + BM25 -> RRF -> top 10, no reranking."""

    def __init__(
        self,
        candidate: FullCorpusCandidate,
        retrieval_treatment: RetrievalTreatment,
        reranker: RerankerMode,
        dense_runner: FullCorpusDenseRunner | OpenRouterDenseRunner,
        sparse_state: SparseState,
        vocabulary_index: dict[str, int],
        client: QdrantClient,
        *,
        candidate_pool: int = 30,
        rrf_k: int = 60,
        search_params: models.SearchParams | None = None,
    ) -> None:
        # candidate_pool / rrf_k / search_params: chỉ để harness Phase 8.1 thử; mặc định = runtime.
        # candidate_pool là số ứng viên mỗi nhánh Qdrant và số giữ lại sau RRF (runtime: 30 và 30).
        # search_params=None giữ HNSW mặc định; models.SearchParams(exact=True) để so với tìm chính xác.
        self.candidate = candidate
        self.retrieval_treatment = retrieval_treatment
        self.reranker = reranker
        self.dense_runner = dense_runner
        self.sparse_state = sparse_state
        self.vocabulary_index = vocabulary_index
        self.client = client
        self.candidate_pool = candidate_pool
        self.rrf_k = rrf_k
        self.search_params = search_params

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
                limit=self.candidate_pool,
                search_params=self.search_params,
                with_payload=[
                    "search_text",
                    "source",
                    "title",
                    "heading_path",
                    "evidence_parts",
                    "chunk_id",
                    "domain",
                ],
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
            dense_stage.append(format_stage_entry(point_id=pid, payload=p.payload, rank=rank, score=score))

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
                format_stage_entry(
                    point_id=pid,
                    payload=candidate_docs[pid].payload,
                    rank=rank,
                    score=bm25_scores_map[pid],
                )
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
                        limit=self.candidate_pool,
                        search_params=self.search_params,
                        with_payload=[
                            "search_text",
                            "source",
                            "title",
                            "heading_path",
                            "evidence_parts",
                            "chunk_id",
                            "domain",
                        ],
                        with_vectors=False,
                    )
                    sparse_points = order_by_score_then_point_id(sparse_response.points)
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
                sparse_stage.append(format_stage_entry(point_id=pid, payload=p.payload, rank=rank, score=score))

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
        fused = reciprocal_rank_fusion(branches, k=self.rrf_k, limit=self.candidate_pool)
        counts["rrf_pre_rerank"] = len(fused)
        stages["rrf"] = [
            format_stage_entry(
                point_id=pid,
                payload=candidate_docs[pid].payload,
                rank=rank,
                score=round(score, 6),
            )
            for rank, (pid, score) in enumerate(fused, start=1)
        ]
        t_rrf_end = time.perf_counter()
        timings["rrf_ms"] = round((t_rrf_end - t_rrf_start) * 1000.0, 3)

        # 4. Không rerank: giữ thứ tự RRF, lấy 10 đầu (rerank thử ở harness 8.1 G4, ngoài service).
        rerank_status = "not_applicable"
        timings["rerank_ms"] = 0.0
        documents = assemble_final_documents(candidate_docs, fused[:10])

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
            anomalies=tuple(sorted(set(anomalies))),
            classification=classification,
        )
        return RetrievalResult(documents=documents, trace=trace)

    def close(self) -> None:
        if self.dense_runner is not None:
            self.dense_runner.close()
        if self.client is not None:
            self.client.close()


def _repo_relative(path: Path) -> str:
    """Đường dẫn tương đối gốc repo cho thông báo lỗi (không lộ đường tuyệt đối)."""
    root = BACKEND_DIR.parent
    return str(path.relative_to(root)) if path.is_relative_to(root) else path.name


def build_full_corpus_retrieval_service(
    candidate_id: str,
    retrieval_treatment: RetrievalTreatment,
    reranker: RerankerMode = "none",
    *,
    settings: dict[str, Any] | None = None,
    client: QdrantClient | None = None,
    collection_name: str | None = None,
    record_path: Path | None = None,
    sparse_state_path: Path = SPARSE_STATE_PATH,
    candidate_pool: int = 30,
    rrf_k: int = 60,
    search_params: models.SearchParams | None = None,
) -> FullCorpusRetrievalService:
    """Build and strictly validate a canonical Full-corpus retrieval service.

    collection_name / record_path / sparse_state_path: chỉ để harness Phase 8.1 đọc biến thể index riêng;
    mặc định = collection runtime của candidate, build record cạnh nó, sparse state chung.
    """
    try:
        candidate = candidate_by_id(candidate_id)
    except ValueError as exc:
        raise RetrievalConfigurationError(f"Unknown candidate ID: {candidate_id}") from exc
    if collection_name is not None:
        candidate = replace(candidate, collection_name=collection_name)

    if retrieval_treatment not in ("dense_bm25_rrf", "native_hybrid_rrf"):
        raise RetrievalConfigurationError(f"Unsupported retrieval treatment: {retrieval_treatment}")
    if reranker != "none":
        raise RetrievalConfigurationError(f"Unsupported reranker mode: {reranker}")

    # 1. Validate matching build record and source freshness
    collection_name = candidate.collection_name
    if record_path is None:
        record_path = build_record_path(candidate)
    rel_build_record = _repo_relative(record_path)
    if not record_path.is_file():
        raise ComponentNotReadyError(f"Build record does not exist: {rel_build_record}")

    try:
        record_data = json.loads(record_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ComponentNotReadyError(f"Failed to read build record: {rel_build_record}") from exc

    if settings is None:
        settings = load_settings()
    root, rel_paths = discover_full_corpus_files(settings)
    current_sources = compute_corpus_state(root, rel_paths)
    validate_full_corpus_build_record(record_data, candidate, current_sources)

    # 2. Validate shared sparse state against the build record
    rel_sparse_state = _repo_relative(sparse_state_path)
    if not sparse_state_path.is_file():
        raise ComponentNotReadyError(f"Sparse state file not found: {rel_sparse_state}")

    state_sha = hashlib.sha256(sparse_state_path.read_bytes()).hexdigest()
    expected_state_sha = record_data["sparse"].get("state_sha256")
    if state_sha != expected_state_sha:
        raise ComponentNotReadyError(f"Sparse state SHA-256 mismatch: {state_sha} != {expected_state_sha}")

    sparse_state = load_sparse_state(sparse_state_path)
    if sparse_state.corpus_identity != record_data["corpus"].get("identity"):
        raise ComponentNotReadyError(f"Sparse state corpus identity mismatch: {sparse_state.corpus_identity}")

    vocab_index = build_vocabulary_index(sparse_state)

    # 3. Validate live Qdrant collection
    if client is None:
        client = client_from_settings(settings)

    if not client.collection_exists(collection_name):
        raise ComponentNotReadyError(f"Qdrant collection {collection_name} does not exist")

    info = client.get_collection(collection_name)
    try:
        validate_full_corpus_collection_info(info, candidate.dense_spec.dimension)
    except Exception as exc:
        raise ComponentNotReadyError(f"Collection {collection_name} schema invalid") from exc

    expected_points = record_data["corpus"].get("chunk_count")
    if info.points_count != expected_points:
        raise ComponentNotReadyError(
            f"Collection {collection_name} point count mismatch: {info.points_count} != {expected_points}"
        )

    # 4. Load dense runner (local model or OpenRouter) and warm up with one query
    try:
        dense_runner = create_dense_runner(candidate.dense_spec)
        dense_runner.load()
        warm_vec = dense_runner.embed_queries(["ấm trà cung đình Huế"])
        if len(warm_vec) != 1 or len(warm_vec[0]) != candidate.dense_spec.dimension:
            raise ComponentNotReadyError(f"Warm-up embedding output invalid for {candidate.candidate_id}")
    except Exception as exc:
        # Model không nạp được (thiếu HF cache, lỗi tải) là phụ thuộc chưa sẵn sàng (503), không phải index cũ (409) — C-01.
        raise RetrievalDependencyError(f"Dense model readiness failed for {candidate.candidate_id}") from exc

    return FullCorpusRetrievalService(
        candidate=candidate,
        retrieval_treatment=retrieval_treatment,
        reranker=reranker,
        dense_runner=dense_runner,
        sparse_state=sparse_state,
        vocabulary_index=vocab_index,
        client=client,
        candidate_pool=candidate_pool,
        rrf_k=rrf_k,
        search_params=search_params,
    )
