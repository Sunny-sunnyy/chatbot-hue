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
    from backend.core.schema import RetrievalDependencyError

    valid_payload = {
        "search_text": "sample text",
        "source": "foods/sample.md",
        "title": "Sample Title",
        "heading_path": ["H2", "H3"],
        "evidence_parts": [
            {"role": "body", "start": 0, "end": 11, "text": "sample text"}
        ],
    }
    # Valid passes
    result = validate_point_payload("p1", valid_payload)
    assert result == valid_payload

    # Non-dict payload raises
    with pytest.raises(RetrievalDependencyError, match="must be a dict"):
        validate_point_payload("p1", "not-a-dict")

    # Missing key raises
    incomplete = {k: v for k, v in valid_payload.items() if k != "search_text"}
    with pytest.raises(RetrievalDependencyError, match="missing:.*search_text"):
        validate_point_payload("p1", incomplete)

    # Extra key raises
    extra = {**valid_payload, "extra_field": 123}
    with pytest.raises(RetrievalDependencyError, match="extra:.*extra_field"):
        validate_point_payload("p1", extra)

    # Non-string / empty search_text raises
    bad_st = {**valid_payload, "search_text": "   "}
    with pytest.raises(RetrievalDependencyError, match="search_text must be non-empty string"):
        validate_point_payload("p1", bad_st)

    # Malformed heading_path raises
    bad_hp = {**valid_payload, "heading_path": "not-a-list"}
    with pytest.raises(RetrievalDependencyError, match="heading_path must be list of strings"):
        validate_point_payload("p1", bad_hp)

    bad_hp_item = {**valid_payload, "heading_path": [123]}
    with pytest.raises(RetrievalDependencyError, match="heading_path must be list of strings"):
        validate_point_payload("p1", bad_hp_item)

    # Malformed evidence_parts raises
    bad_ep = {**valid_payload, "evidence_parts": [{"role": "body", "start": "0", "end": 5, "text": "text"}]}
    with pytest.raises(RetrievalDependencyError, match="evidence_parts.*invalid start/end"):
        validate_point_payload("p1", bad_ep)


def test_validate_point_payload_nested_evidence_parts_fail_closed():
    from backend.retrieval.full_corpus import validate_point_payload
    from backend.core.schema import RetrievalDependencyError

    base_payload = {
        "search_text": "sample text",
        "source": "foods/sample.md",
        "title": "Sample Title",
        "heading_path": ["H2", "H3"],
        "evidence_parts": [
            {"role": "body", "start": 0, "end": 11, "text": "sample text"}
        ],
    }

    # Valid roles: body, header, condition
    for valid_role in ("body", "header", "condition"):
        p = copy.deepcopy(base_payload)
        p["evidence_parts"][0]["role"] = valid_role
        assert validate_point_payload("p1", p) == p

    # Extra key in evidence_parts item raises
    bad_extra = copy.deepcopy(base_payload)
    bad_extra["evidence_parts"][0]["extra"] = "unexpected"
    with pytest.raises(RetrievalDependencyError, match="evidence_parts.*fields mismatch.*extra: extra"):
        validate_point_payload("p1", bad_extra)

    # Missing key in evidence_parts item raises
    bad_missing = copy.deepcopy(base_payload)
    del bad_missing["evidence_parts"][0]["end"]
    with pytest.raises(RetrievalDependencyError, match="evidence_parts.*fields mismatch.*missing: end"):
        validate_point_payload("p1", bad_missing)

    # Invalid string role raises
    bad_role = copy.deepcopy(base_payload)
    bad_role["evidence_parts"][0]["role"] = "INVALID"
    with pytest.raises(RetrievalDependencyError, match="evidence_parts.*invalid role: 'INVALID'"):
        validate_point_payload("p1", bad_role)

    # Non-string roles (list, dict, int, bool, None) raise RetrievalDependencyError, not TypeError
    for bad_non_str_role in ([], {}, 123, True, False, None):
        bad_payload = copy.deepcopy(base_payload)
        bad_payload["evidence_parts"][0]["role"] = bad_non_str_role
        with pytest.raises(RetrievalDependencyError, match="evidence_parts.*invalid role"):
            validate_point_payload("p1", bad_payload)

    # Boolean start offset raises (bool is not int)
    bad_bool_start = copy.deepcopy(base_payload)
    bad_bool_start["evidence_parts"][0]["start"] = False
    with pytest.raises(RetrievalDependencyError, match="invalid start/end offsets"):
        validate_point_payload("p1", bad_bool_start)

    # Boolean end offset raises
    bad_bool_end = copy.deepcopy(base_payload)
    bad_bool_end["evidence_parts"][0]["end"] = True
    with pytest.raises(RetrievalDependencyError, match="invalid start/end offsets"):
        validate_point_payload("p1", bad_bool_end)

    # Both boolean offsets raise
    bad_bool_both = copy.deepcopy(base_payload)
    bad_bool_both["evidence_parts"][0]["start"] = False
    bad_bool_both["evidence_parts"][0]["end"] = True
    with pytest.raises(RetrievalDependencyError, match="invalid start/end offsets"):
        validate_point_payload("p1", bad_bool_both)

    # Negative start raises
    bad_neg = copy.deepcopy(base_payload)
    bad_neg["evidence_parts"][0]["start"] = -1
    with pytest.raises(RetrievalDependencyError, match="invalid start/end offsets"):
        validate_point_payload("p1", bad_neg)

    # end < start raises
    bad_order = copy.deepcopy(base_payload)
    bad_order["evidence_parts"][0]["start"] = 10
    bad_order["evidence_parts"][0]["end"] = 5
    with pytest.raises(RetrievalDependencyError, match="invalid start/end offsets"):
        validate_point_payload("p1", bad_order)

    # Non-string text raises
    bad_text = copy.deepcopy(base_payload)
    bad_text["evidence_parts"][0]["text"] = 12345
    with pytest.raises(RetrievalDependencyError, match="text must be string"):
        validate_point_payload("p1", bad_text)


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
