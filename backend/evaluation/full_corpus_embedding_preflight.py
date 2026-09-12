"""Orchestration CLI và kiểm tra tiền kiểm (preflight) cho Phase 3.

Thực hiện:
1. Đối chiếu fresh Phase 2 chunking với artifact lịch sử đã đóng.
2. Khởi tạo và lưu trữ deterministic sparse state.
3. Quét toàn bộ tokenizer trên toàn corpus (truncation=False) để kiểm tra max tokens.
4. Chọn mẫu cố định 10-15 chunks phủ 7 P7, 4 content tags, và các chunks dài nhất.
5. Kiểm tra tính khả dụng của CUDA / GTX 1650.
6. Chạy bounded dense inference tuần tự cho 4 mô hình.
7. Xuất bằng chứng JSON được làm sạch hoàn toàn (không lưu vector, text, cache path, bí mật).
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
import json
from pathlib import Path
import re
import sys
import time
from typing import Any, Callable

import numpy as np
import torch
from transformers import AutoTokenizer

from backend.core.schema import FullCorpusChunk
from backend.core.settings_loader import load_settings
from backend.embedding.full_corpus import (
    DENSE_MODEL_SPECS,
    QWEN_QUERY_TASK,
    DenseModelSpec,
    FullCorpusDenseRunner,
    count_tokens,
    prepare_document,
    prepare_query,
    resolve_snapshot,
)
from backend.embedding.sparse import (
    SparseState,
    fit_sparse_state,
    load_sparse_state,
    write_sparse_state,
)
from backend.ingestion.chunking.full_corpus_chunker import (
    ConditionManager,
    chunk_full_corpus,
)
from backend.ingestion.source_state import discover_full_corpus_files

P7_ORDER: tuple[str, ...] = (
    "foods",
    "heritages",
    "festivals",
    "performing_arts",
    "travel_places",
    "travel_services",
    "travel_tickets",
)

SMOKE_QUERIES: tuple[str, ...] = (
    "Đại Nội Huế có những điểm tham quan nào?",
    "Lễ hội truyền thống ở Huế thường diễn ra khi nào?",
    "Tôi nên ăn món gì và di chuyển thế nào khi du lịch Huế?",
)


def partition_for_source(source: str) -> str:
    """Xác định phân vùng P7 từ đường dẫn nguồn chuẩn hóa."""
    s = source.removeprefix("knowledge-base-hue/")
    if s.startswith("travel/places/"):
        return "travel_places"
    if s.startswith("travel/services/"):
        return "travel_services"
    if s.startswith("travel/tickets/"):
        return "travel_tickets"
    return s.split("/")[0]


def classify_chunk(chunk: FullCorpusChunk) -> frozenset[str]:
    """Phân loại cấu trúc nội dung của chunk thành các nhãn: paragraph, list, table, condition."""
    tags: set[str] = set()
    list_pattern = re.compile(r"^\s*([*+-]|\d+\.)\s+", re.MULTILINE)

    has_table = False
    has_condition = False
    has_list = False
    has_body = False

    for part in chunk.evidence_parts:
        if part.role == "header":
            has_table = True
            tags.add("table")
        elif part.role == "condition":
            has_condition = True
            tags.add("condition")
        elif part.role == "body":
            has_body = True
            if list_pattern.search(part.text):
                has_list = True
                tags.add("list")

    if not chunk.evidence_parts:
        if list_pattern.search(chunk.search_text):
            tags.add("list")
        else:
            tags.add("paragraph")
    else:
        if has_body and not has_table and not has_list:
            tags.add("paragraph")
        if not tags:
            tags.add("paragraph")

    return frozenset(tags)


def select_dense_sample(
    chunks: Sequence[FullCorpusChunk],
    longest_by_model: Mapping[str, str],
    minimum: int = 10,
    maximum: int = 15,
) -> list[FullCorpusChunk]:
    """Chọn mẫu cố định 10-15 chunks bảo đảm tính xác định và độ bao phủ toàn diện."""
    sorted_chunks = sorted(chunks, key=lambda c: c.chunk_id)
    chunk_by_id = {c.chunk_id: c for c in sorted_chunks}

    selected_ids: list[str] = []
    selected_set: set[str] = set()

    def add_id(cid: str) -> None:
        if cid in chunk_by_id and cid not in selected_set:
            selected_set.add(cid)
            selected_ids.append(cid)

    # 1. Chunk đầu tiên theo thứ tự từ điển cho mỗi P7
    for p in P7_ORDER:
        found = False
        for c in sorted_chunks:
            if partition_for_source(c.source) == p:
                add_id(c.chunk_id)
                found = True
                break
        if not found:
            raise ValueError(f"No chunk found for partition {p}")

    # 2. Chunk đầu tiên cho mỗi content tag còn thiếu
    required_tags = ("paragraph", "list", "table", "condition")
    for tag in required_tags:
        covered = set().union(*(classify_chunk(chunk_by_id[cid]) for cid in selected_ids))
        if tag not in covered:
            for c in sorted_chunks:
                if tag in classify_chunk(c):
                    add_id(c.chunk_id)
                    break

    # 3. Các chunks dài nhất theo từng model
    for model_key, cid in sorted(longest_by_model.items()):
        if cid not in chunk_by_id:
            raise ValueError(f"Longest chunk {cid} for {model_key} not in corpus")
        add_id(cid)

    # 4. Bổ sung tuần tự cho đủ tối thiểu (10 chunks)
    for c in sorted_chunks:
        if len(selected_ids) >= minimum:
            break
        add_id(c.chunk_id)

    # 5. Kiểm tra ranh giới fail-closed
    if len(selected_ids) < minimum or len(selected_ids) > maximum:
        raise ValueError(
            f"Sample size {len(selected_ids)} outside allowed range [{minimum}, {maximum}]"
        )

    # Kiểm tra bao phủ đầy đủ 7 P7
    sample_partitions = {partition_for_source(chunk_by_id[cid].source) for cid in selected_ids}
    if not set(P7_ORDER).issubset(sample_partitions):
        missing = set(P7_ORDER) - sample_partitions
        raise ValueError(f"Sample failed to cover partitions: {missing}")

    # Kiểm tra bao phủ đầy đủ 4 tags
    all_covered_tags = set().union(*(classify_chunk(chunk_by_id[cid]) for cid in selected_ids))
    if not set(required_tags).issubset(all_covered_tags):
        missing_tags = set(required_tags) - all_covered_tags
        raise ValueError(f"Sample failed to cover tags: {missing_tags}")

    # Kiểm tra có mặt đầy đủ longest chunks
    for cid in longest_by_model.values():
        if cid not in selected_set:
            raise ValueError(f"Sample missing longest chunk {cid}")

    return [chunk_by_id[cid] for cid in selected_ids]


def inspect_cuda() -> dict[str, object]:
    """Kiểm tra môi trường CUDA và thiết bị GPU thực tế."""
    info: dict[str, object] = {
        "torch_version": torch.__version__,
        "torch_cuda_version": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "device_count": torch.cuda.device_count(),
    }
    if not torch.cuda.is_available() or torch.cuda.device_count() == 0:
        info["error"] = "CUDA is not available in PyTorch environment"
        return info

    device_name = torch.cuda.get_device_name(0)
    total_vram = torch.cuda.get_device_properties(0).total_memory
    info["device_index"] = 0
    info["device_name"] = device_name
    info["total_vram_bytes"] = total_vram

    if "GTX 1650" not in device_name:
        info["error"] = f"Device name {device_name!r} does not match required GTX 1650"

    return info


def validate_phase_2_identity(
    p2_artifact: Mapping[str, Any],
    discovered_sources: Sequence[str],
    total_chunks: int,
    condition_rules_count: int,
) -> None:
    """Đối chiếu toàn diện kết quả Phase 2 tươi mới với artifact lịch sử đã đóng."""
    expected_status = p2_artifact.get("status")
    if expected_status != "PASS":
        raise ValueError(f"Phase 2 artifact status is not PASS: {expected_status}")

    p2_summary = p2_artifact.get("summary", {})
    expected_files = p2_summary.get("total_files")
    if len(discovered_sources) != expected_files:
        raise ValueError(
            f"Discovered file count mismatch: actual {len(discovered_sources)} != expected {expected_files}"
        )

    expected_sources = p2_artifact.get("sources", [])
    if list(discovered_sources) != list(expected_sources):
        raise ValueError(
            "Discovered sources list does not match exact ordered Phase 2 sources list"
        )

    expected_chunks = p2_summary.get("total_chunks")
    if total_chunks != expected_chunks:
        raise ValueError(
            f"Chunk count mismatch: actual {total_chunks} != expected {expected_chunks}"
        )

    expected_conditions = p2_summary.get("condition_rules_count")
    if condition_rules_count != expected_conditions:
        raise ValueError(
            f"Condition rules count mismatch: actual {condition_rules_count} != expected {expected_conditions}"
        )


def validate_phase_2_tokenizer_maxima(
    p2_artifact: Mapping[str, Any],
    observed_maxima: Mapping[str, int],
) -> None:
    """Đối chiếu ba tokenizer maxima của Phase 2 (E5-small, E5-base, HuyDang)."""
    p2_limits = p2_artifact.get("tokenizer_limits", {})
    key_to_p2_id = {
        "e5-small-384": "intfloat/multilingual-e5-small",
        "e5-base-768": "intfloat/multilingual-e5-base",
        "huydang-dek21-768": "CODE4LIFEOFFICIAL/huydang-dek21-embedding",
    }
    for model_key, p2_id in key_to_p2_id.items():
        limit_data = p2_limits.get(p2_id)
        if not limit_data:
            raise ValueError(f"Missing tokenizer limit entry in Phase 2 artifact for {p2_id}")
        expected_max = limit_data.get("max_observed_tokens")
        actual_max = observed_maxima.get(model_key)
        if actual_max is None:
            actual_max = observed_maxima.get(p2_id)
        if actual_max is None:
            raise ValueError(f"Missing observed tokenizer maximum for {model_key} ({p2_id})")
        if actual_max != expected_max:
            raise ValueError(
                f"Tokenizer maximum mismatch for {model_key} ({p2_id}): "
                f"actual {actual_max} != expected {expected_max}"
            )


def derive_status(component_statuses: Mapping[str, str]) -> str:
    """Quyết định trạng thái tổng thể dựa trên thứ tự ưu tiên các ranh giới an toàn."""
    if component_statuses.get("phase_2") in ("BLOCKED_PHASE_2", "FAILED"):
        return "BLOCKED_PHASE_2"
    if component_statuses.get("gpu") in ("BLOCKED_GPU", "UNAVAILABLE", "FAILED"):
        return "BLOCKED_GPU"
    if component_statuses.get("tokenizers") in ("BLOCKED_TOKEN_LIMIT", "OVER_LIMIT", "FAILED"):
        return "BLOCKED_TOKEN_LIMIT"
    if component_statuses.get("qwen") in ("BLOCKED_QWEN", "OOM", "FAILED"):
        return "BLOCKED_QWEN"
    if component_statuses.get("cpu_models") in ("FAILED_MODEL", "FAILED"):
        return "FAILED_MODEL"
    if component_statuses.get("sparse") in ("FAILED_SPARSE", "FAILED"):
        return "FAILED_SPARSE"

    required_components = ("phase_2", "gpu", "tokenizers", "qwen", "cpu_models", "sparse")
    for req in required_components:
        if component_statuses.get(req) != "PASS":
            return "FAILED"

    return "PASS"


def validate_evidence_redaction(evidence: dict[str, Any]) -> None:
    """Kiểm tra bảo mật làm sạch dữ liệu: không lưu vector, text, token bí mật hay đường dẫn cache."""
    forbidden_keys = {"vectors", "search_text", "evidence_text"}
    forbidden_patterns = [
        re.compile(r"Bearer\s+", re.IGNORECASE),
        re.compile(r"sk-[a-zA-Z0-9]{20,}"),
        re.compile(r"api[_-]?key", re.IGNORECASE),
        re.compile(r"/home/\w+/\.cache"),
    ]

    def _check(obj: Any, path: str) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in forbidden_keys:
                    raise ValueError(f"Forbidden key '{k}' found at {path}")
                _check(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, elem in enumerate(obj):
                _check(elem, f"{path}[{i}]")
        elif isinstance(obj, str):
            for pat in forbidden_patterns:
                if pat.search(obj):
                    raise ValueError(f"Forbidden content pattern '{pat.pattern}' found at {path}")

    _check(evidence, "root")


def run_preflight(
    sparse_output: Path,
    evidence_output: Path,
    allow_downloads: bool = False,
    phase_2_preview_path: Path = Path("reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json"),
) -> tuple[dict[str, object], int]:
    """Thực thi chuỗi tiền kiểm Phase 3 và tạo artifact / evidence JSON."""
    component_statuses: dict[str, str] = {}
    errors: list[str] = []
    models_summary: dict[str, Any] = {}

    evidence: dict[str, Any] = {
        "schema_version": "phase_3_preflight_evidence:v1",
        "status": "INITIALIZING",
        "corpus": {},
        "sample": [],
        "queries": list(SMOKE_QUERIES),
        "models": models_summary,
        "gpu": {},
        "sparse": {},
        "errors": errors,
    }

    # 1. Phân giải snapshot cho 4 mô hình
    snapshot_paths: dict[str, Path] = {}
    tokenizers: dict[str, Any] = {}
    for spec in DENSE_MODEL_SPECS:
        models_summary[spec.key] = {
            "model_id": spec.model_id,
            "revision": spec.revision,
            "dimension": spec.dimension,
            "max_tokens": spec.max_tokens,
            "input_contract": spec.input_contract,
            "device": spec.device,
            "dtype": spec.dtype,
            "batch_size": spec.batch_size,
            "configured": {
                "native_output_dimension": spec.dimension,
                "parameter_device": spec.device,
                "parameter_dtype": spec.dtype,
                "attention_implementation": "eager" if spec.device == "cuda" else None,
                "batch_size": spec.batch_size,
                "input_contract": spec.input_contract,
                "document_preprocessing": "prefix: passage: " if "e5" in spec.key else ("pyvi_tokenize" if "huydang" in spec.key else "raw_representation_a"),
                "query_instruction": "prefix: query: " if "e5" in spec.key else ("pyvi_tokenize" if "huydang" in spec.key else QWEN_QUERY_TASK),
            },
        }
        try:
            snap_path = resolve_snapshot(spec, allow_download=allow_downloads)
            snapshot_paths[spec.key] = snap_path
            # Tải tokenizer từ snapshot cục bộ
            tok = AutoTokenizer.from_pretrained(str(snap_path), local_files_only=True)
            tokenizers[spec.key] = tok
        except Exception as e:
            err_msg = f"Failed to resolve snapshot or tokenizer for {spec.key}: {type(e).__name__}: {e}"
            errors.append(err_msg)
            if spec.key == "qwen3-embedding-0.6b-1024":
                component_statuses["qwen"] = "BLOCKED_QWEN"
            else:
                component_statuses["cpu_models"] = "FAILED_MODEL"

    if len(snapshot_paths) != len(DENSE_MODEL_SPECS):
        evidence["status"] = derive_status(component_statuses)
        validate_evidence_redaction(evidence)
        evidence_output.parent.mkdir(parents=True, exist_ok=True)
        evidence_output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
        return evidence, 1

    # 2. Khởi tạo Phase 2 fit checker từ 3 spec đầu tiên (e5-small, e5-base, huydang)
    def phase_2_checker(search_text: str) -> bool:
        for spec in DENSE_MODEL_SPECS[:3]:
            tok = tokenizers[spec.key]
            prep = prepare_document(spec, search_text)
            n_tokens = count_tokens(tok, prep)
            if n_tokens > spec.max_tokens:
                return False
        return True

    # 3. Kiểm tra tính nhất quán với Phase 2 preview artifact
    try:
        if not phase_2_preview_path.is_file():
            raise FileNotFoundError(f"Preserved Phase 2 preview artifact not found: {phase_2_preview_path}")

        p2_artifact = json.loads(phase_2_preview_path.read_text(encoding="utf-8"))

        settings = load_settings()
        root, discovered_files = discover_full_corpus_files(settings)
        discovered_sources = [f.as_posix() if hasattr(f, "as_posix") else str(f) for f in discovered_files]
        cond_mgr = ConditionManager(settings=settings)
        condition_rules_count = len(cond_mgr.rules)

        chunks, chunk_errors = chunk_full_corpus(
            settings=settings,
            is_fits_tokenizer_fn=phase_2_checker,
        )
        if chunk_errors:
            raise ValueError(f"Phase 2 chunking produced blocking errors: {chunk_errors}")

        validate_phase_2_identity(
            p2_artifact=p2_artifact,
            discovered_sources=discovered_sources,
            total_chunks=len(chunks),
            condition_rules_count=condition_rules_count,
        )

        # Kiểm tra tính duy nhất của chunk_id
        chunk_ids = [c.chunk_id for c in chunks]
        if len(set(chunk_ids)) != len(chunk_ids):
            raise ValueError("Duplicate chunk_ids found in fresh chunking result")

        component_statuses["phase_2"] = "PASS"
        evidence["corpus"] = {
            "total_files": len(discovered_files),
            "total_chunks": len(chunks),
            "condition_rules_count": condition_rules_count,
        }
    except Exception as e:
        err_msg = f"Phase 2 validation failed: {type(e).__name__}: {e}"
        errors.append(err_msg)
        component_statuses["phase_2"] = "BLOCKED_PHASE_2"
        evidence["status"] = derive_status(component_statuses)
        validate_evidence_redaction(evidence)
        evidence_output.parent.mkdir(parents=True, exist_ok=True)
        evidence_output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
        return evidence, 1

    # 4. Khởi tạo và ghi deterministic sparse state
    try:
        sparse_state = fit_sparse_state(chunks)
        # Ghi và kiểm tra lặp byte-identical
        sha_1 = write_sparse_state(sparse_state, sparse_output)
        tmp_check_path = sparse_output.with_name(f"{sparse_output.name}.verify")
        sha_2 = write_sparse_state(sparse_state, tmp_check_path)
        repeated_byte_identical = (sha_1 == sha_2) and (sparse_output.read_bytes() == tmp_check_path.read_bytes())
        tmp_check_path.unlink(missing_ok=True)
        if not repeated_byte_identical:
            raise ValueError("Sparse state serialization failed repeated byte-identical check")

        # Kiểm tra round-trip equality
        loaded_sparse = load_sparse_state(sparse_output)
        round_trip_equality = (
            loaded_sparse.schema_version == sparse_state.schema_version
            and loaded_sparse.corpus_identity == sparse_state.corpus_identity
            and loaded_sparse.document_count == sparse_state.document_count
            and loaded_sparse.average_document_length == sparse_state.average_document_length
            and loaded_sparse.k1 == sparse_state.k1
            and loaded_sparse.b == sparse_state.b
            and loaded_sparse.vocabulary == sparse_state.vocabulary
            and loaded_sparse.idf == sparse_state.idf
        )
        if not round_trip_equality:
            raise ValueError("Sparse state serialization failed round-trip equality check")

        component_statuses["sparse"] = "PASS"
        evidence["sparse"] = {
            "schema_version": sparse_state.schema_version,
            "sha256": sha_1,
            "document_count": sparse_state.document_count,
            "vocabulary_size": len(sparse_state.vocabulary),
            "average_document_length": sparse_state.average_document_length,
            "k1": sparse_state.k1,
            "b": sparse_state.b,
            "repeated_byte_identical": repeated_byte_identical,
            "round_trip_equality": round_trip_equality,
        }
        evidence["corpus"]["corpus_identity"] = sparse_state.corpus_identity
    except Exception as e:
        err_msg = f"Sparse state creation failed: {type(e).__name__}: {e}"
        errors.append(err_msg)
        component_statuses["sparse"] = "FAILED_SPARSE"

    # 5. Quét toàn bộ tokenizer trên 8.460 chunks
    longest_by_model: dict[str, str] = {}
    tokenizer_has_over_limit = False
    observed_maxima: dict[str, int] = {}

    for spec in DENSE_MODEL_SPECS:
        tok = tokenizers[spec.key]
        max_tokens = 0
        longest_cid = ""
        over_limit_ids: list[str] = []

        for ch in chunks:
            prep_doc = prepare_document(spec, ch.search_text)
            cnt = count_tokens(tok, prep_doc)
            if cnt > max_tokens:
                max_tokens = cnt
                longest_cid = ch.chunk_id
            if cnt > spec.max_tokens:
                over_limit_ids.append(ch.chunk_id)

        # Kiểm tra thêm 3 query mẫu
        for q in SMOKE_QUERIES:
            prep_q = prepare_query(spec, q)
            q_cnt = count_tokens(tok, prep_q)
            if q_cnt > spec.max_tokens:
                over_limit_ids.append(f"query:{q[:20]}")

        longest_by_model[spec.key] = longest_cid
        observed_maxima[spec.key] = max_tokens
        models_summary[spec.key]["tokenizer_scan"] = {
            "max_observed_tokens": max_tokens,
            "max_chunk_id": longest_cid,
            "over_limit_count": len(over_limit_ids),
            "over_limit_ids": over_limit_ids[:10],
        }

        if over_limit_ids:
            tokenizer_has_over_limit = True

    # Đối chiếu 3 tokenizer maxima với Phase 2 artifact (fail-closed BLOCKED_PHASE_2)
    try:
        validate_phase_2_tokenizer_maxima(p2_artifact, observed_maxima)
    except Exception as e:
        err_msg = f"Phase 2 tokenizer maxima validation failed: {type(e).__name__}: {e}"
        errors.append(err_msg)
        component_statuses["phase_2"] = "BLOCKED_PHASE_2"
        evidence["status"] = derive_status(component_statuses)
        validate_evidence_redaction(evidence)
        evidence_output.parent.mkdir(parents=True, exist_ok=True)
        evidence_output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
        return evidence, 1

    if tokenizer_has_over_limit:
        component_statuses["tokenizers"] = "OVER_LIMIT"
        errors.append("One or more models exceeded tokenizer max_tokens limit on corpus")
        evidence["status"] = derive_status(component_statuses)
        validate_evidence_redaction(evidence)
        evidence_output.parent.mkdir(parents=True, exist_ok=True)
        evidence_output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
        return evidence, 1
    else:
        component_statuses["tokenizers"] = "PASS"

    # 6. Kiểm tra CUDA readiness
    cuda_info = inspect_cuda()
    evidence["gpu"] = cuda_info
    if not cuda_info.get("cuda_available") or "error" in cuda_info:
        component_statuses["gpu"] = "BLOCKED_GPU"
        errors.append(f"CUDA inspection failed: {cuda_info.get('error', 'unknown error')}")
        evidence["status"] = derive_status(component_statuses)
        validate_evidence_redaction(evidence)
        evidence_output.parent.mkdir(parents=True, exist_ok=True)
        evidence_output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
        return evidence, 1
    else:
        component_statuses["gpu"] = "PASS"

    # 7. Chọn mẫu cố định 10-15 chunks
    try:
        sample_chunks = select_dense_sample(chunks, longest_by_model, minimum=10, maximum=15)
        for idx, ch in enumerate(sample_chunks):
            # Tính token counts cho từng model trên sample
            ch_tokens = {
                spec.key: count_tokens(tokenizers[spec.key], prepare_document(spec, ch.search_text))
                for spec in DENSE_MODEL_SPECS
            }
            evidence["sample"].append({
                "index": idx,
                "chunk_id": ch.chunk_id,
                "source": ch.source,
                "heading_path": list(ch.heading_path),
                "tags": sorted(classify_chunk(ch)),
                "tokens": ch_tokens,
            })
    except Exception as e:
        err_msg = f"Sample selection failed: {type(e).__name__}: {e}"
        errors.append(err_msg)
        component_statuses["cpu_models"] = "FAILED_MODEL"
        evidence["status"] = derive_status(component_statuses)
        validate_evidence_redaction(evidence)
        evidence_output.parent.mkdir(parents=True, exist_ok=True)
        evidence_output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
        return evidence, 1

    sample_texts = [c.search_text for c in sample_chunks]

    # 8. Chạy bounded dense inference tuần tự
    cpu_pass = True
    qwen_pass = True

    for spec in DENSE_MODEL_SPECS:
        snap_path = snapshot_paths[spec.key]
        runner = FullCorpusDenseRunner(spec, snap_path)

        t0 = time.perf_counter()
        try:
            if spec.device == "cuda":
                torch.cuda.reset_peak_memory_stats(0)

            runner.load()
            obs_state = runner.observed_runtime_state()

            # Mã hóa documents và queries
            doc_vecs = runner.embed_documents(sample_texts)
            query_vecs = runner.embed_queries(SMOKE_QUERIES)

            elapsed = time.perf_counter() - t0

            # Tính norm range
            doc_norms = [float(np.linalg.norm(np.array(v))) for v in doc_vecs]
            query_norms = [float(np.linalg.norm(np.array(v))) for v in query_vecs]
            all_norms = doc_norms + query_norms

            smoke_info: dict[str, Any] = {
                "document_count": len(doc_vecs),
                "query_count": len(query_vecs),
                "dimension": spec.dimension,
                "norm_min": min(all_norms),
                "norm_max": max(all_norms),
                "elapsed_seconds": round(elapsed, 4),
            }

            if spec.device == "cuda":
                # Đo VRAM cho Qwen
                alloc = torch.cuda.memory_allocated(0)
                reserved = torch.cuda.memory_reserved(0)
                peak = torch.cuda.max_memory_allocated(0)
                smoke_info["vram"] = {
                    "allocated_bytes": alloc,
                    "reserved_bytes": reserved,
                    "peak_bytes": peak,
                }
                evidence["gpu"]["qwen_vram"] = smoke_info["vram"]

            models_summary[spec.key]["smoke"] = smoke_info
            models_summary[spec.key]["observed"] = {
                "native_output_dimension": obs_state.get("dimension"),
                "parameter_device": obs_state.get("parameter_device"),
                "parameter_dtype": obs_state.get("parameter_dtype"),
                "attention_implementation": obs_state.get("attn_implementation"),
                "batch_size": spec.batch_size,
                "document_preprocessing": "prefix: passage: " if "e5" in spec.key else ("pyvi_tokenize" if "huydang" in spec.key else "raw_representation_a"),
                "query_instruction": "prefix: query: " if "e5" in spec.key else ("pyvi_tokenize" if "huydang" in spec.key else QWEN_QUERY_TASK),
            }

        except Exception as e:
            err_msg = f"Dense inference failed for {spec.key}: {type(e).__name__}: {e}"
            errors.append(err_msg)
            if spec.key == "qwen3-embedding-0.6b-1024":
                qwen_pass = False
            else:
                cpu_pass = False
        finally:
            runner.close()

    component_statuses["cpu_models"] = "PASS" if cpu_pass else "FAILED_MODEL"
    component_statuses["qwen"] = "PASS" if qwen_pass else "BLOCKED_QWEN"

    final_status = derive_status(component_statuses)
    evidence["status"] = final_status

    # 9. Làm sạch và ghi evidence JSON
    validate_evidence_redaction(evidence)
    evidence_output.parent.mkdir(parents=True, exist_ok=True)
    evidence_output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")

    exit_code = 0 if final_status == "PASS" else 1
    return evidence, exit_code


def main() -> None:
    """Hàm thực thi CLI chính."""
    parser = argparse.ArgumentParser(description="Full-corpus embedding and sparse preflight CLI.")
    parser.add_argument(
        "--sparse-output",
        type=Path,
        default=Path("data/full_corpus_builds/phase_3_sparse_state.json"),
        help="Path to output sparse state JSON.",
    )
    parser.add_argument(
        "--evidence-output",
        type=Path,
        default=Path("reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json"),
        help="Path to output preflight evidence JSON.",
    )
    parser.add_argument(
        "--allow-downloads",
        action="store_true",
        help="Allow downloading models from Hugging Face if not cached.",
    )
    args = parser.parse_args()

    _, exit_code = run_preflight(
        sparse_output=args.sparse_output,
        evidence_output=args.evidence_output,
        allow_downloads=args.allow_downloads,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
