"""Unit tests for Phase 5 full-corpus retrieval, trace privacy, and reciprocal rank fusion."""
import copy
from dataclasses import asdict
import json
import math
import pytest

from backend.retrieval.full_corpus import (
    RetrievalResult,
    RetrievalTrace,
    RetrievalTreatment,
    RerankerMode,
    reciprocal_rank_fusion,
    rank_positive_bm25,
    compute_sparse_dot_product,
)
from backend.core.schema import FullCorpusChunk, RetrievedDocument
from backend.embedding.sparse import (
    SparseState,
    build_vocabulary_index,
    encode_sparse_document,
    encode_sparse_query,
    fit_sparse_state,
)


def test_rrf_uses_k_60_rank_from_one_and_point_id_tie_break():
    assert reciprocal_rank_fusion([["b", "a"], ["a", "b"]]) == [
        ("a", 1 / 61 + 1 / 62),
        ("b", 1 / 61 + 1 / 62),
    ]


def test_rrf_one_branch_preserves_branch_order():
    assert [point_id for point_id, _ in reciprocal_rank_fusion([["c", "a", "b"]])] == [
        "c", "a", "b"
    ]


def test_rrf_unions_branches_limits_output_and_rejects_malformed_branch():
    ranked = reciprocal_rank_fusion([["a", "b"], ["b", "c"]], limit=2)
    assert len(ranked) == 2
    assert len({point_id for point_id, _ in ranked}) == 2
    with pytest.raises(ValueError, match="duplicate"):
        reciprocal_rank_fusion([["a", "a"]])


def test_rrf_rejects_non_positive_k_or_limit():
    with pytest.raises(ValueError, match="k must be positive"):
        reciprocal_rank_fusion([["a"]], k=0)
    with pytest.raises(ValueError, match="limit must be positive"):
        reciprocal_rank_fusion([["a"]], limit=0)


def test_rrf_rejects_empty_or_non_string_point_ids():
    with pytest.raises(ValueError, match="invalid point ID"):
        reciprocal_rank_fusion([[""]])
    with pytest.raises(ValueError, match="invalid point ID"):
        reciprocal_rank_fusion([[None]])  # type: ignore


def test_retrieval_trace_fields_and_privacy_boundary():
    trace = RetrievalTrace(
        candidate_id="e5-small-384",
        collection_name="hue_full_corpus_a_e5_small_384",
        retrieval_treatment="dense_bm25_rrf",
        reranker="none",
        counts={"dense": 30, "bm25": 12, "rrf_pre_rerank": 30, "final": 10},
        timings_ms={"dense_ms": 15.2, "bm25_ms": 2.1, "rrf_ms": 0.3, "total_ms": 17.6},
        stages={
            "dense": [{"point_id": "p1", "rank": 1, "score": 0.85}],
            "bm25": [{"point_id": "p1", "rank": 1, "score": 2.4}],
            "rrf": [{"point_id": "p1", "rank": 1, "score": 0.032}],
        },
        rerank_status="not_applicable",
        anomalies=(),
        classification="PASS",
    )
    data = asdict(trace)
    serialized = json.dumps(data)
    forbidden_keys = {"query", "search_text", "evidence_parts", "text"}
    for key in forbidden_keys:
        assert key not in data, f"Forbidden key {key} in trace data"
    # Ensure no absolute paths leaked
    assert "/home/" not in serialized
    assert "C:\\" not in serialized


def test_retrieval_result_structure():
    trace = RetrievalTrace(
        candidate_id="e5-small-384",
        collection_name="hue_full_corpus_a_e5_small_384",
        retrieval_treatment="dense_bm25_rrf",
        reranker="none",
        counts={},
        timings_ms={},
        stages={},
        rerank_status="not_applicable",
        anomalies=(),
        classification="PASS",
    )
    doc = RetrievedDocument(
        id="uuid-1",
        score=0.032,
        text="search text sample",
        metadata={"source": "test.md", "title": "Test", "heading_path": [], "evidence_parts": []},
    )
    result = RetrievalResult(documents=[doc], trace=trace)
    assert len(result.documents) == 1
    assert result.documents[0].id == "uuid-1"
    assert result.trace.classification == "PASS"


def test_rank_positive_bm25():
    positive = rank_positive_bm25([("a", 0.0), ("b", 2.0), ("c", 1.0)])
    assert positive == ["b", "c"]
    assert rank_positive_bm25([("a", 0.0), ("b", 0.0)]) == []
    # Test tie-break ascending point_id
    assert rank_positive_bm25([("z", 1.0), ("a", 1.0)]) == ["a", "z"]


def test_sparse_dot_product_matching_and_non_mutation():
    chunks = [
        FullCorpusChunk(
            chunk_id="f1#0",
            source="foods/bún_bò.md",
            title="Bún bò Huế",
            heading_path=[],
            evidence_parts=[],
            search_text="Bún bò Huế thơm ngon đậm đà nước dùng",
        ),
        FullCorpusChunk(
            chunk_id="f2#0",
            source="heritages/đại_nội.md",
            title="Đại Nội Huế",
            heading_path=[],
            evidence_parts=[],
            search_text="Đại Nội Huế kinh thành hoàng cung cổ kính",
        ),
    ]
    state = fit_sparse_state(chunks)
    vocab_index = build_vocabulary_index(state)

    query = "bún bò"
    q_vec = encode_sparse_query(query, state)
    doc_match = encode_sparse_document(chunks[0].search_text, state, vocab_index)
    doc_other = encode_sparse_document(chunks[1].search_text, state, vocab_index)

    score_match = compute_sparse_dot_product(q_vec, doc_match)
    score_other = compute_sparse_dot_product(q_vec, doc_other)

    assert score_match > 0.0
    assert score_other == 0.0

    # Test non-mutation of input documents/payload
    original_payload = {"search_text": chunks[0].search_text, "source": chunks[0].source}
    payload_copy = copy.deepcopy(original_payload)
    doc = RetrievedDocument(id="p1", score=1.0, text=chunks[0].search_text, metadata=payload_copy)
    doc_before = copy.deepcopy(doc)

    # Perform score computation
    _ = compute_sparse_dot_product(q_vec, doc_match)
    assert doc.id == doc_before.id
    assert doc.score == doc_before.score
    assert doc.text == doc_before.text
    assert doc.metadata == original_payload


def test_cross_encoder_primitives_contract():
    from backend.reranking.cross_encoder import CrossEncoderReranker
    reranker = CrossEncoderReranker()
    assert isinstance(reranker.max_length, int)
    assert reranker.max_length > 0

    token_count = reranker.input_token_count("query", "doc text")
    assert isinstance(token_count, int)
    assert token_count > 0

    docs = [
        RetrievedDocument(id="p1", score=1.0, text="Bún bò Huế", metadata={"chunk_id": "c1"}),
        RetrievedDocument(id="p2", score=2.0, text="Cơm hến", metadata={"chunk_id": "c2"}),
    ]
    docs_before = copy.deepcopy(docs)
    scores = reranker.score_documents("món ăn", docs)
    assert len(scores) == 2
    assert all(isinstance(s, float) for s in scores)
    assert all(math.isfinite(s) for s in scores)
    # Check input documents are not mutated
    assert docs == docs_before


def test_validate_point_payload_valid_and_malformed():
    from backend.retrieval.full_corpus import validate_point_payload
    from backend.core.schema import RetrievalDependencyError, point_id_for_chunk_id

    source = "foods/sample.md"
    chunk_id = "foods/sample.md#0"
    point_id = point_id_for_chunk_id(chunk_id)
    valid_payload = {
        "search_text": "sample text",
        "source": source,
        "title": "Sample Title",
        "heading_path": ["H2", "H3"],
        "evidence_parts": [
            {"role": "body", "start": 0, "end": 11, "text": "sample text"}
        ],
        "chunk_id": chunk_id,
        "domain": "foods",
    }
    # Valid passes
    result = validate_point_payload(point_id, valid_payload)
    assert result == valid_payload

    # Non-dict payload raises
    with pytest.raises(RetrievalDependencyError, match="must be a dict"):
        validate_point_payload(point_id, "not-a-dict")

    # Missing key raises
    incomplete = {k: v for k, v in valid_payload.items() if k != "search_text"}
    with pytest.raises(RetrievalDependencyError, match="missing:.*search_text"):
        validate_point_payload(point_id, incomplete)

    # Extra key raises
    extra = {**valid_payload, "extra_field": 123}
    with pytest.raises(RetrievalDependencyError, match="extra:.*extra_field"):
        validate_point_payload(point_id, extra)

    # Non-string / empty search_text raises
    bad_st = {**valid_payload, "search_text": "   "}
    with pytest.raises(RetrievalDependencyError, match="search_text must be non-empty string"):
        validate_point_payload(point_id, bad_st)

    # Malformed heading_path raises
    bad_hp = {**valid_payload, "heading_path": "not-a-list"}
    with pytest.raises(RetrievalDependencyError, match="heading_path must be list of strings"):
        validate_point_payload(point_id, bad_hp)

    bad_hp_item = {**valid_payload, "heading_path": [123]}
    with pytest.raises(RetrievalDependencyError, match="heading_path must be list of strings"):
        validate_point_payload(point_id, bad_hp_item)

    # Malformed evidence_parts raises
    bad_ep = {**valid_payload, "evidence_parts": [{"role": "body", "start": "0", "end": 5, "text": "text"}]}
    with pytest.raises(RetrievalDependencyError, match="evidence_parts.*invalid start/end"):
        validate_point_payload(point_id, bad_ep)


def test_validate_point_payload_nested_evidence_parts_fail_closed():
    from backend.retrieval.full_corpus import validate_point_payload
    from backend.core.schema import RetrievalDependencyError, point_id_for_chunk_id

    source = "foods/sample.md"
    chunk_id = "foods/sample.md#0"
    point_id = point_id_for_chunk_id(chunk_id)
    base_payload = {
        "search_text": "sample text",
        "source": source,
        "title": "Sample Title",
        "heading_path": ["H2", "H3"],
        "evidence_parts": [
            {"role": "body", "start": 0, "end": 11, "text": "sample text"}
        ],
        "chunk_id": chunk_id,
        "domain": "foods",
    }

    # Valid roles: body, header, condition
    for valid_role in ("body", "header", "condition"):
        p = copy.deepcopy(base_payload)
        p["evidence_parts"][0]["role"] = valid_role
        assert validate_point_payload(point_id, p) == p

    # Extra key in evidence_parts item raises
    bad_extra = copy.deepcopy(base_payload)
    bad_extra["evidence_parts"][0]["extra"] = "unexpected"
    with pytest.raises(RetrievalDependencyError, match="evidence_parts.*fields mismatch.*extra: extra"):
        validate_point_payload(point_id, bad_extra)

    # Missing key in evidence_parts item raises
    bad_missing = copy.deepcopy(base_payload)
    del bad_missing["evidence_parts"][0]["end"]
    with pytest.raises(RetrievalDependencyError, match="evidence_parts.*fields mismatch.*missing: end"):
        validate_point_payload(point_id, bad_missing)

    # Invalid string role raises
    bad_role = copy.deepcopy(base_payload)
    bad_role["evidence_parts"][0]["role"] = "INVALID"
    with pytest.raises(RetrievalDependencyError, match="evidence_parts.*invalid role"):
        validate_point_payload(point_id, bad_role)

    # Non-string roles (list, dict, int, bool, None) raise RetrievalDependencyError, not TypeError
    for bad_non_str_role in ([], {}, 123, True, False, None):
        bad_payload = copy.deepcopy(base_payload)
        bad_payload["evidence_parts"][0]["role"] = bad_non_str_role
        with pytest.raises(RetrievalDependencyError, match="evidence_parts.*invalid role"):
            validate_point_payload(point_id, bad_payload)

    # Boolean start offset raises (bool is not int)
    bad_bool_start = copy.deepcopy(base_payload)
    bad_bool_start["evidence_parts"][0]["start"] = False
    with pytest.raises(RetrievalDependencyError, match="invalid start/end offsets"):
        validate_point_payload(point_id, bad_bool_start)

    # Boolean end offset raises
    bad_bool_end = copy.deepcopy(base_payload)
    bad_bool_end["evidence_parts"][0]["end"] = True
    with pytest.raises(RetrievalDependencyError, match="invalid start/end offsets"):
        validate_point_payload(point_id, bad_bool_end)

    # Both boolean offsets raise
    bad_bool_both = copy.deepcopy(base_payload)
    bad_bool_both["evidence_parts"][0]["start"] = False
    bad_bool_both["evidence_parts"][0]["end"] = True
    with pytest.raises(RetrievalDependencyError, match="invalid start/end offsets"):
        validate_point_payload(point_id, bad_bool_both)

    # Negative start raises
    bad_neg = copy.deepcopy(base_payload)
    bad_neg["evidence_parts"][0]["start"] = -1
    with pytest.raises(RetrievalDependencyError, match="invalid start/end offsets"):
        validate_point_payload(point_id, bad_neg)

    # end < start raises
    bad_order = copy.deepcopy(base_payload)
    bad_order["evidence_parts"][0]["start"] = 10
    bad_order["evidence_parts"][0]["end"] = 5
    with pytest.raises(RetrievalDependencyError, match="invalid start/end offsets"):
        validate_point_payload(point_id, bad_order)

    # Non-string text raises
    bad_text = copy.deepcopy(base_payload)
    bad_text["evidence_parts"][0]["text"] = 12345
    with pytest.raises(RetrievalDependencyError, match="text must be string"):
        validate_point_payload(point_id, bad_text)


def test_validate_selectors_rejects_unknown_and_empty():
    from backend.retrieval.full_corpus_smoke import validate_selectors

    # Valid full selectors
    c, t, r, q = validate_selectors(None, None, None, None)
    assert len(c) == 4
    assert len(t) == 2
    assert len(r) == 2
    assert len(q) == 7

    # Unknown candidate
    with pytest.raises(ValueError, match="Unknown candidate selector"):
        validate_selectors(["unknown-model"], None, None, None)

    # Unknown treatment
    with pytest.raises(ValueError, match="Unknown treatment selector"):
        validate_selectors(None, ["typo"], None, None)

    # Unknown reranker
    with pytest.raises(ValueError, match="Unknown reranker selector"):
        validate_selectors(None, None, ["qwen_reranker"], None)

    # Unknown query ID
    with pytest.raises(ValueError, match="Unknown query selector"):
        validate_selectors(None, None, None, ["P5-Q99"])


def test_validate_safe_output_path_and_sanitization():
    from pathlib import Path
    from backend.retrieval.full_corpus_smoke import (
        validate_safe_output_path,
        sanitize_error_detail,
    )

    # Safe outside repo
    safe_tmp = Path("/tmp/test_trace.json")
    assert validate_safe_output_path(safe_tmp) == safe_tmp.resolve()

    # Safe inside repo (gitignored data/ path)
    safe_data = Path("data/test_trace.json")
    assert validate_safe_output_path(safe_data) == safe_data.resolve()

    # Unsafe inside repo (tracked folder)
    unsafe_path = Path("backend/test_trace.json")
    with pytest.raises(ValueError, match="Unsafe output path"):
        validate_safe_output_path(unsafe_path)

    # Sanitized error detail does not contain raw exception text
    exc = ValueError("Failed at /home/minhhieu/hue_rag/data/file.json: bad value")
    detail = sanitize_error_detail(exc)
    assert detail["error_type"] == "ValueError"
    assert detail["error_category"] == "value_error"
    assert detail["error_code"] == "ERR_VALUE"
    assert "error_message" not in detail
    serialized = json.dumps(detail)
    assert "/home/minhhieu" not in serialized
    assert "bad value" not in serialized


def test_error_sanitization_privacy_probe_markers():
    """Verify that exception details with query, secret, config, and paths never leak into serialized record."""
    from backend.retrieval.full_corpus_smoke import sanitize_error_detail

    marker_query = "PRIVATE_QUERY_PHASE5_MARKER"
    marker_secret = "sk-secret-key-phase5-test"
    marker_config = "DB_CONFIG_PASSWORD_SECRET"
    marker_path = "/home/minhhieu/hue_rag/private_data.json"

    exc = RuntimeError(f"Query '{marker_query}' failed with secret '{marker_secret}', config '{marker_config}' at '{marker_path}'")
    detail = sanitize_error_detail(exc)
    assert detail["error_type"] == "RuntimeError"
    assert detail["error_category"] == "internal_error"
    assert detail["error_code"] == "ERR_INTERNAL"

    serialized = json.dumps(detail)
    for marker in (marker_query, marker_secret, marker_config, marker_path, "/home/"):
        assert marker not in serialized

    # Check full cell record serialization
    cell_record = {
        "candidate_id": "e5-small-384",
        "retrieval_treatment": "dense_bm25_rrf",
        "reranker": "none",
        "classification": "FAIL",
        "anomalies": ["cell_exception"],
        "error": detail,
    }
    serialized_trace = json.dumps({"cells": {"cell_0": cell_record}})
    for marker in (marker_query, marker_secret, marker_config, marker_path, "/home/"):
        assert marker not in serialized_trace


def test_v2_payload_accepts_exact_identity_and_domain():
    from backend.retrieval.full_corpus import validate_point_payload
    from backend.core.schema import point_id_for_chunk_id

    source = "foods/sample.md"
    chunk_id = "foods/sample.md#0"
    point_id = point_id_for_chunk_id(chunk_id)
    payload = {
        "search_text": "sample text",
        "source": source,
        "title": "Sample Title",
        "heading_path": ["H2", "H3"],
        "evidence_parts": [
            {"role": "body", "start": 0, "end": 11, "text": "sample text"}
        ],
        "chunk_id": chunk_id,
        "domain": "foods",
    }
    validated = validate_point_payload(point_id, payload)
    assert validated == payload


def test_v2_payload_rejects_legacy_five_fields():
    from backend.retrieval.full_corpus import validate_point_payload
    from backend.core.schema import RetrievalDependencyError, point_id_for_chunk_id

    chunk_id = "foods/sample.md#0"
    point_id = point_id_for_chunk_id(chunk_id)
    legacy_payload = {
        "search_text": "sample text",
        "source": "foods/sample.md",
        "title": "Sample Title",
        "heading_path": ["H2", "H3"],
        "evidence_parts": [
            {"role": "body", "start": 0, "end": 11, "text": "sample text"}
        ],
    }
    with pytest.raises(RetrievalDependencyError) as exc_info:
        validate_point_payload(point_id, legacy_payload)
    err = str(exc_info.value)
    assert "missing" in err
    assert "chunk_id" in err or "domain" in err


def test_v2_payload_rejects_extra_field():
    from backend.retrieval.full_corpus import validate_point_payload
    from backend.core.schema import RetrievalDependencyError, point_id_for_chunk_id

    chunk_id = "foods/sample.md#0"
    point_id = point_id_for_chunk_id(chunk_id)
    payload_extra = {
        "search_text": "sample text",
        "source": "foods/sample.md",
        "title": "Sample Title",
        "heading_path": ["H2", "H3"],
        "evidence_parts": [
            {"role": "body", "start": 0, "end": 11, "text": "sample text"}
        ],
        "chunk_id": chunk_id,
        "domain": "foods",
        "extra_field": "unexpected",
    }
    with pytest.raises(RetrievalDependencyError) as exc_info:
        validate_point_payload(point_id, payload_extra)
    assert "extra: extra_field" in str(exc_info.value)


def test_v2_payload_rejects_point_uuid_chunk_id_mismatch():
    from backend.retrieval.full_corpus import validate_point_payload
    from backend.core.schema import RetrievalDependencyError, point_id_for_chunk_id

    chunk_id = "foods/sample.md#0"
    wrong_point_id = point_id_for_chunk_id("foods/sample.md#1")
    payload = {
        "search_text": "sample text",
        "source": "foods/sample.md",
        "title": "Sample Title",
        "heading_path": ["H2", "H3"],
        "evidence_parts": [
            {"role": "body", "start": 0, "end": 11, "text": "sample text"}
        ],
        "chunk_id": chunk_id,
        "domain": "foods",
    }
    with pytest.raises(RetrievalDependencyError, match="chunk identity does not match point ID"):
        validate_point_payload(wrong_point_id, payload)


def test_v2_payload_rejects_domain_source_mismatch():
    from backend.retrieval.full_corpus import validate_point_payload
    from backend.core.schema import RetrievalDependencyError, point_id_for_chunk_id

    chunk_id = "foods/sample.md#0"
    point_id = point_id_for_chunk_id(chunk_id)
    payload_wrong_domain = {
        "search_text": "sample text",
        "source": "foods/sample.md",
        "title": "Sample Title",
        "heading_path": ["H2", "H3"],
        "evidence_parts": [
            {"role": "body", "start": 0, "end": 11, "text": "sample text"}
        ],
        "chunk_id": chunk_id,
        "domain": "travel",
    }
    with pytest.raises(RetrievalDependencyError, match="domain mismatch"):
        validate_point_payload(point_id, payload_wrong_domain)


def test_v2_payload_validation_errors_never_leak_private_paths_or_text():
    from backend.retrieval.full_corpus import validate_point_payload
    from backend.core.schema import RetrievalDependencyError, point_id_for_chunk_id

    secret_source = "foods/top_secret_recipe_source.md"
    secret_chunk = f"{secret_source}#42"
    safe_point_id = point_id_for_chunk_id(secret_chunk)
    secret_text = "CONFIDENTIAL_PAYLOAD_BODY_TEXT_XYZ"

    base_payload = {
        "search_text": secret_text,
        "source": secret_source,
        "title": "Confidential Title",
        "heading_path": ["Secret", "Path"],
        "evidence_parts": [
            {"role": "body", "start": 0, "end": 10, "text": secret_text}
        ],
        "chunk_id": secret_chunk,
        "domain": "foods",
    }

    # Case 1: Invalid chunk relation (source vs chunk_id mismatch)
    bad_rel = copy.deepcopy(base_payload)
    bad_rel["source"] = "foods/unrelated_source.md"
    with pytest.raises(RetrievalDependencyError) as exc_info:
        validate_point_payload(safe_point_id, bad_rel)
    err = str(exc_info.value)
    assert safe_point_id in err
    assert "invalid chunk identity relation" in err
    assert secret_chunk not in err
    assert secret_source not in err
    assert "foods/unrelated_source.md" not in err

    # Case 2: Point UUID mismatch
    wrong_point_id = point_id_for_chunk_id("foods/other.md#0")
    with pytest.raises(RetrievalDependencyError) as exc_info:
        validate_point_payload(wrong_point_id, base_payload)
    err = str(exc_info.value)
    assert wrong_point_id in err
    assert "chunk identity does not match point ID" in err
    assert secret_chunk not in err
    assert secret_source not in err

    # Case 3: Invalid source for domain derivation
    bad_src = copy.deepcopy(base_payload)
    bad_source_str = "/absolute/private/path.md"
    bad_chunk_str = f"{bad_source_str}#0"
    bad_point_id = point_id_for_chunk_id(bad_chunk_str)
    bad_src["source"] = bad_source_str
    bad_src["chunk_id"] = bad_chunk_str
    with pytest.raises(RetrievalDependencyError) as exc_info:
        validate_point_payload(bad_point_id, bad_src)
    err = str(exc_info.value)
    assert bad_point_id in err
    assert "invalid source for domain derivation" in err
    assert bad_source_str not in err
    assert bad_chunk_str not in err

    # Case 4: Domain mismatch
    bad_dom = copy.deepcopy(base_payload)
    bad_dom["domain"] = "travel"
    with pytest.raises(RetrievalDependencyError) as exc_info:
        validate_point_payload(safe_point_id, bad_dom)
    err = str(exc_info.value)
    assert safe_point_id in err
    assert "domain mismatch" in err
    assert secret_source not in err
    assert secret_chunk not in err
    assert secret_text not in err


def test_v2_build_record_rejects_wrong_build_or_payload_schema():
    import hashlib
    from backend.retrieval.full_corpus import BUILD_RECORDS_DIR, validate_full_corpus_build_record
    from backend.core.schema import ComponentNotReadyError
    from backend.ingestion.full_corpus_pipeline import (
        candidate_by_id,
        EXPECTED_CORPUS_IDENTITY,
        EXPECTED_CHUNK_COUNT,
        EXPECTED_SPARSE_SHA256,
    )

    candidate = candidate_by_id("e5-small-384")
    legacy_path = BUILD_RECORDS_DIR / f"{candidate.collection_name}.json"
    legacy_sha = hashlib.sha256(legacy_path.read_bytes()).hexdigest()

    valid_record = {
        "schema_version": "phase_4_full_corpus_build:v2",
        "status": "complete",
        "collection_name": candidate.metadata_v2_collection_name,
        "representation": "A",
        "corpus": {
            "identity": EXPECTED_CORPUS_IDENTITY,
            "file_count": 205,
            "chunk_count": EXPECTED_CHUNK_COUNT,
            "sources": {"foods/a.md": "a" * 64},
        },
        "dense": {
            "candidate_id": candidate.candidate_id,
            "model_id": candidate.dense_spec.model_id,
            "revision": candidate.dense_spec.revision,
            "dimension": candidate.dense_spec.dimension,
        },
        "sparse": {
            "schema_version": "phase_3_sparse_state:v1",
            "state_sha256": EXPECTED_SPARSE_SHA256,
            "vocabulary_size": 5662,
        },
        "qdrant": {
            "payload_schema_version": "full_corpus_qdrant_payload:v2",
            "dense_vector_name": "dense",
            "sparse_vector_name": "sparse",
            "distance": "cosine",
            "point_count": EXPECTED_CHUNK_COUNT,
        },
        "migration": {
            "mode": "copy_verified_vectors",
            "source_collection": candidate.collection_name,
            "source_build_record_sha256": legacy_sha,
        },
    }

    # Should pass when valid
    validate_full_corpus_build_record(valid_record, candidate)

    # Wrong build record schema_version
    bad_build = copy.deepcopy(valid_record)
    bad_build["schema_version"] = "phase_4_full_corpus_build:v1"
    with pytest.raises(ComponentNotReadyError, match="schema_version"):
        validate_full_corpus_build_record(bad_build, candidate)

    # Wrong collection_name (target collection mismatch)
    bad_col = copy.deepcopy(valid_record)
    bad_col["collection_name"] = "wrong_target_collection"
    with pytest.raises(ComponentNotReadyError, match="collection_name mismatch"):
        validate_full_corpus_build_record(bad_col, candidate)

    # Wrong payload_schema_version
    bad_payload = copy.deepcopy(valid_record)
    bad_payload["qdrant"]["payload_schema_version"] = "full_corpus_qdrant_payload:v1"
    with pytest.raises(ComponentNotReadyError, match="payload_schema_version"):
        validate_full_corpus_build_record(bad_payload, candidate)

    # Missing payload_schema_version
    missing_payload = copy.deepcopy(valid_record)
    del missing_payload["qdrant"]["payload_schema_version"]
    with pytest.raises(ComponentNotReadyError, match="payload_schema_version"):
        validate_full_corpus_build_record(missing_payload, candidate)

    # Wrong dense_vector_name
    bad_dense = copy.deepcopy(valid_record)
    bad_dense["qdrant"]["dense_vector_name"] = "wrong_dense"
    with pytest.raises(ComponentNotReadyError, match="dense_vector_name invalid"):
        validate_full_corpus_build_record(bad_dense, candidate)

    # Wrong sparse_vector_name
    bad_sparse = copy.deepcopy(valid_record)
    bad_sparse["qdrant"]["sparse_vector_name"] = "wrong_sparse"
    with pytest.raises(ComponentNotReadyError, match="sparse_vector_name invalid"):
        validate_full_corpus_build_record(bad_sparse, candidate)

    # Wrong distance
    bad_dist = copy.deepcopy(valid_record)
    bad_dist["qdrant"]["distance"] = "dot"
    with pytest.raises(ComponentNotReadyError, match="distance invalid"):
        validate_full_corpus_build_record(bad_dist, candidate)

    # Wrong point_count
    bad_pts = copy.deepcopy(valid_record)
    bad_pts["qdrant"]["point_count"] = 8459
    with pytest.raises(ComponentNotReadyError, match="point_count invalid"):
        validate_full_corpus_build_record(bad_pts, candidate)

    # Wrong migration source collection
    bad_source_col = copy.deepcopy(valid_record)
    bad_source_col["migration"]["source_collection"] = "wrong_source"
    with pytest.raises(ComponentNotReadyError, match="source_collection"):
        validate_full_corpus_build_record(bad_source_col, candidate)

    # Wrong lineage SHA-256
    bad_lineage = copy.deepcopy(valid_record)
    bad_lineage["migration"]["source_build_record_sha256"] = "f" * 64
    with pytest.raises(ComponentNotReadyError, match="source_build_record_sha256 mismatch"):
        validate_full_corpus_build_record(bad_lineage, candidate)

    # Malformed lineage SHA
    malformed_lineage = copy.deepcopy(valid_record)
    malformed_lineage["migration"]["source_build_record_sha256"] = 12345
    with pytest.raises(ComponentNotReadyError, match="source_build_record_sha256 mismatch"):
        validate_full_corpus_build_record(malformed_lineage, candidate)


def test_v2_freshness_rejects_added_deleted_and_changed_source():
    from backend.retrieval.full_corpus import validate_full_corpus_build_record
    from backend.core.schema import ComponentNotReadyError
    from backend.ingestion.full_corpus_pipeline import (
        candidate_by_id,
        EXPECTED_CORPUS_IDENTITY,
        EXPECTED_CHUNK_COUNT,
        EXPECTED_SPARSE_SHA256,
    )

    import hashlib
    from backend.retrieval.full_corpus import BUILD_RECORDS_DIR
    candidate = candidate_by_id("e5-small-384")
    legacy_path = BUILD_RECORDS_DIR / f"{candidate.collection_name}.json"
    legacy_sha = hashlib.sha256(legacy_path.read_bytes()).hexdigest()
    recorded_sources = {
        "foods/file1.md": "sha_1111",
        "foods/file2.md": "sha_2222",
    }
    base_record = {
        "schema_version": "phase_4_full_corpus_build:v2",
        "status": "complete",
        "collection_name": candidate.metadata_v2_collection_name,
        "representation": "A",
        "corpus": {
            "identity": EXPECTED_CORPUS_IDENTITY,
            "file_count": 205,
            "chunk_count": EXPECTED_CHUNK_COUNT,
            "sources": recorded_sources,
        },
        "dense": {
            "candidate_id": candidate.candidate_id,
            "model_id": candidate.dense_spec.model_id,
            "revision": candidate.dense_spec.revision,
            "dimension": candidate.dense_spec.dimension,
        },
        "sparse": {
            "schema_version": "phase_3_sparse_state:v1",
            "state_sha256": EXPECTED_SPARSE_SHA256,
            "vocabulary_size": 5662,
        },
        "qdrant": {
            "payload_schema_version": "full_corpus_qdrant_payload:v2",
            "dense_vector_name": "dense",
            "sparse_vector_name": "sparse",
            "distance": "cosine",
            "point_count": EXPECTED_CHUNK_COUNT,
        },
        "migration": {
            "mode": "copy_verified_vectors",
            "source_collection": candidate.collection_name,
            "source_build_record_sha256": legacy_sha,
        },
    }

    # Added source
    added = {**recorded_sources, "foods/file3.md": "sha_3333"}
    with pytest.raises(ComponentNotReadyError, match="stale"):
        validate_full_corpus_build_record(base_record, candidate, current_sources=added)

    # Deleted source
    deleted = {"foods/file1.md": "sha_1111"}
    with pytest.raises(ComponentNotReadyError, match="stale"):
        validate_full_corpus_build_record(base_record, candidate, current_sources=deleted)

    # Changed source
    changed = {"foods/file1.md": "sha_1111", "foods/file2.md": "sha_CHANGED"}
    with pytest.raises(ComponentNotReadyError, match="stale"):
        validate_full_corpus_build_record(base_record, candidate, current_sources=changed)


def test_result_uses_chunk_id_and_domain_but_rrf_ties_still_use_point_id():
    from backend.retrieval.full_corpus import (
        build_retrieved_document,
        reciprocal_rank_fusion,
        assemble_final_documents,
    )
    from backend.core.schema import point_id_for_chunk_id

    chunk_a = "travel/tickets/z.md#9"
    chunk_b = "foods/a.md#0"
    point_a = point_id_for_chunk_id(chunk_a)
    point_b = point_id_for_chunk_id(chunk_b)

    if point_a > point_b:
        chunk_a, chunk_b = chunk_b, chunk_a
        point_a, point_b = point_b, point_a

    payload_a = {
        "search_text": "text a",
        "source": chunk_a.split("#")[0],
        "title": "Title A",
        "heading_path": [],
        "evidence_parts": [],
        "chunk_id": chunk_a,
        "domain": chunk_a.split("/")[0],
    }
    payload_b = {
        "search_text": "text b",
        "source": chunk_b.split("#")[0],
        "title": "Title B",
        "heading_path": [],
        "evidence_parts": [],
        "chunk_id": chunk_b,
        "domain": chunk_b.split("/")[0],
    }

    class MockPoint:
        def __init__(self, id, payload):
            self.id = id
            self.payload = payload

    candidate_docs = {
        point_a: MockPoint(point_a, payload_a),
        point_b: MockPoint(point_b, payload_b),
    }

    fused = reciprocal_rank_fusion([[point_a, point_b], [point_b, point_a]])
    assert len(fused) == 2
    assert fused[0][1] == fused[1][1]  # tied score
    assert fused[0][0] == point_a  # tie-break by point UUID string ascending!
    assert fused[1][0] == point_b

    docs = assemble_final_documents(candidate_docs, fused)
    assert len(docs) == 2
    assert docs[0].id == chunk_a
    assert docs[0].metadata["domain"] == payload_a["domain"]
    assert docs[0].text == "text a"
    assert docs[1].id == chunk_b
    assert docs[1].metadata["domain"] == payload_b["domain"]
    assert docs[1].text == "text b"


def test_trace_contains_only_point_id_chunk_id_domain_rank_score_allowlist():
    from backend.retrieval.full_corpus import (
        format_stage_entry,
        assemble_final_documents,
        RetrievedDocument,
        RetrievalTrace,
    )
    from backend.core.schema import point_id_for_chunk_id

    chunk_id = "foods/bún_bò.md#0"
    point_id = point_id_for_chunk_id(chunk_id)
    payload = {
        "search_text": "Bún bò Huế thơm ngon",
        "source": "foods/bún_bò.md",
        "title": "Bún bò Huế",
        "heading_path": ["Món ăn"],
        "evidence_parts": [{"role": "body", "start": 0, "end": 20, "text": "Bún bò Huế thơm ngon"}],
        "chunk_id": chunk_id,
        "domain": "foods",
    }

    entry = format_stage_entry(point_id=point_id, payload=payload, rank=1, score=0.95)
    assert set(entry.keys()) == {"point_id", "chunk_id", "domain", "rank", "score"}
    assert entry["point_id"] == point_id
    assert entry["chunk_id"] == chunk_id
    assert entry["domain"] == "foods"
    assert entry["rank"] == 1
    assert entry["score"] == 0.95

    forbidden_keys = {"query", "search_text", "evidence_parts", "text", "source", "title", "heading_path"}
    for k in forbidden_keys:
        assert k not in entry

    class MockPoint:
        def __init__(self, id, payload):
            self.id = id
            self.payload = payload

    candidate_docs = {point_id: MockPoint(point_id, payload)}

    no_rerank_docs = assemble_final_documents(candidate_docs, [(point_id, 0.05)])
    assert len(no_rerank_docs) == 1
    assert no_rerank_docs[0].id == chunk_id
    assert no_rerank_docs[0].metadata["domain"] == "foods"
    assert "point_id" not in no_rerank_docs[0].metadata
    assert "rank" not in no_rerank_docs[0].metadata
    assert "score" not in no_rerank_docs[0].metadata

    rerank_pairs = [(0.88, point_id)]
    minilm_docs = assemble_final_documents(candidate_docs, [(pid, score) for score, pid in rerank_pairs])
    assert len(minilm_docs) == 1
    assert minilm_docs[0].id == chunk_id
    assert minilm_docs[0].metadata["domain"] == "foods"
    assert "point_id" not in minilm_docs[0].metadata

    trace = RetrievalTrace(
        candidate_id="e5-small-384",
        collection_name="hue_full_corpus_a_e5_small_384_metadata_v2",
        retrieval_treatment="dense_bm25_rrf",
        reranker="minilm",
        counts={"final": 1},
        timings_ms={"total_ms": 10.0},
        stages={"dense": [entry], "rrf": [entry], "rerank": [entry]},
        rerank_status="completed",
        anomalies=(),
        classification="PASS",
    )
    serialized = json.dumps(asdict(trace))
    for k in forbidden_keys:
        assert f'"{k}":' not in serialized
    assert "/home/" not in serialized
