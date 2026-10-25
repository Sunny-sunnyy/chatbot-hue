"""Unit tests for Phase 5 full-corpus retrieval, trace privacy, and reciprocal rank fusion."""
import copy
from dataclasses import asdict
import json
import math
import unicodedata
import pytest

from retrieval.full_corpus import (
    RetrievalResult,
    RetrievalTrace,
    RetrievalTreatment,
    RerankerMode,
    reciprocal_rank_fusion,
    rank_positive_bm25,
    order_by_score_then_point_id,
    compute_sparse_dot_product,
    normalize_query,
)
from core.schema import FullCorpusChunk, InvalidQueryError, RetrievedDocument
from embedding.sparse import (
    SparseState,
    build_vocabulary_index,
    encode_sparse_document,
    encode_sparse_query,
    fit_sparse_state,
)


def test_normalize_query_turns_nfd_into_nfc_and_rejects_blank():
    nfc = "Huế có món bún bò không?"
    nfd = unicodedata.normalize("NFD", nfc)
    assert nfd != nfc
    assert normalize_query(nfd) == nfc
    assert normalize_query(nfc) == nfc
    with pytest.raises(InvalidQueryError):
        normalize_query("  ")


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
        collection_name="hue_full_corpus_7a2_e5_small_384",
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
        collection_name="hue_full_corpus_7a2_e5_small_384",
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


def test_order_by_score_then_point_id_breaks_ties_by_point_id():
    from qdrant_client import models

    def point(point_id: str, score: float) -> models.ScoredPoint:
        return models.ScoredPoint(id=point_id, version=0, score=score)

    # Cùng tập điểm, hai thứ tự đến khác nhau (như Qdrant trả khác nhau theo limit) phải ra một thứ tự.
    ids = ["00000000-0000-0000-0000-00000000000b", "00000000-0000-0000-0000-00000000000a",
           "00000000-0000-0000-0000-00000000000c"]
    first = [point(ids[0], 2.0), point(ids[1], 2.0), point(ids[2], 3.0)]
    second = [point(ids[2], 3.0), point(ids[1], 2.0), point(ids[0], 2.0)]
    expected = [ids[2], ids[1], ids[0]]
    assert [str(p.id) for p in order_by_score_then_point_id(first)] == expected
    assert [str(p.id) for p in order_by_score_then_point_id(second)] == expected


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
    from reranking.cross_encoder import CrossEncoderReranker
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
    from retrieval.full_corpus import validate_point_payload
    from core.schema import RetrievalDependencyError, point_id_for_chunk_id

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
    from retrieval.full_corpus import validate_point_payload
    from core.schema import RetrievalDependencyError, point_id_for_chunk_id

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


def test_v2_payload_accepts_exact_identity_and_domain():
    from retrieval.full_corpus import validate_point_payload
    from core.schema import point_id_for_chunk_id

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
    from retrieval.full_corpus import validate_point_payload
    from core.schema import RetrievalDependencyError, point_id_for_chunk_id

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
    from retrieval.full_corpus import validate_point_payload
    from core.schema import RetrievalDependencyError, point_id_for_chunk_id

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
    from retrieval.full_corpus import validate_point_payload
    from core.schema import RetrievalDependencyError, point_id_for_chunk_id

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
    from retrieval.full_corpus import validate_point_payload
    from core.schema import RetrievalDependencyError, point_id_for_chunk_id

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
    from retrieval.full_corpus import validate_point_payload
    from core.schema import RetrievalDependencyError, point_id_for_chunk_id

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


def _valid_build_record_and_sources():
    from embedding.sparse import fit_sparse_state
    from ingestion.full_corpus_pipeline import candidate_by_id
    from ingestion.source_state import make_full_corpus_build_record

    candidate = candidate_by_id("e5-small-384")
    chunk = FullCorpusChunk(
        chunk_id="foods/a.md#0",
        source="foods/a.md",
        title="Bún bò",
        heading_path=[],
        evidence_parts=[],
        search_text="Bún bò Huế",
    )
    state = fit_sparse_state([chunk])
    sources = {"foods/a.md": "a" * 64, "foods/b.md": "b" * 64}
    record = make_full_corpus_build_record(
        collection_name=candidate.collection_name,
        candidate_id=candidate.candidate_id,
        dense={
            "model_id": candidate.dense_spec.model_id,
            "revision": candidate.dense_spec.revision,
            "dimension": candidate.dense_spec.dimension,
        },
        sources=sources,
        chunk_count=1,
        corpus_identity=state.corpus_identity,
        sparse_state=state,
        sparse_state_sha256="c" * 64,
    )
    return candidate, record, sources


def test_build_record_rejects_wrong_schema_target_or_dense_contract():
    from retrieval.full_corpus import validate_full_corpus_build_record
    from core.schema import ComponentNotReadyError

    candidate, valid_record, sources = _valid_build_record_and_sources()
    validate_full_corpus_build_record(valid_record, candidate, sources)

    def mutated(path, value):
        record = copy.deepcopy(valid_record)
        target = record
        for key in path[:-1]:
            target = target[key]
        if value is None:
            del target[path[-1]]
        else:
            target[path[-1]] = value
        return record

    cases = [
        (("schema_version",), "phase_4_full_corpus_build:v2", "schema_version"),
        (("collection_name",), "wrong_target_collection", "collection_name mismatch"),
        (("qdrant", "payload_schema_version"), None, "payload_schema_version"),
        (("qdrant", "dense_vector_name"), "wrong_dense", "dense_vector_name invalid"),
        (("qdrant", "distance"), "dot", "distance invalid"),
        (("qdrant", "point_count"), 2, "point_count invalid"),
        (("dense", "candidate_id"), "qwen3-embedding-8b-4096", "candidate_id mismatch"),
        (("dense", "dimension"), 4096, "dimension mismatch"),
        (("dense", "revision"), "0" * 40, "revision mismatch"),
    ]
    for path, value, message in cases:
        with pytest.raises(ComponentNotReadyError, match=message):
            validate_full_corpus_build_record(mutated(path, value), candidate, sources)


def test_build_record_freshness_rejects_added_deleted_and_changed_source():
    from retrieval.full_corpus import validate_full_corpus_build_record
    from core.schema import ComponentNotReadyError

    candidate, record, sources = _valid_build_record_and_sources()

    added = {**sources, "foods/c.md": "c" * 64}
    deleted = {"foods/a.md": "a" * 64}
    changed = {**sources, "foods/b.md": "f" * 64}
    for current in (added, deleted, changed):
        with pytest.raises(ComponentNotReadyError, match="stale"):
            validate_full_corpus_build_record(record, candidate, current)


def test_result_uses_chunk_id_and_domain_but_rrf_ties_still_use_point_id():
    from retrieval.full_corpus import (
        build_retrieved_document,
        reciprocal_rank_fusion,
        assemble_final_documents,
    )
    from core.schema import point_id_for_chunk_id

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
    from retrieval.full_corpus import (
        format_stage_entry,
        assemble_final_documents,
        RetrievedDocument,
        RetrievalTrace,
    )
    from core.schema import point_id_for_chunk_id

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

    trace = RetrievalTrace(
        candidate_id="e5-small-384",
        collection_name="hue_full_corpus_7a2_e5_small_384",
        retrieval_treatment="dense_bm25_rrf",
        reranker="none",
        counts={"final": 1},
        timings_ms={"total_ms": 10.0},
        stages={"dense": [entry], "rrf": [entry]},
        rerank_status="not_applicable",
        anomalies=(),
        classification="PASS",
    )
    serialized = json.dumps(asdict(trace))
    for k in forbidden_keys:
        assert f'"{k}":' not in serialized
    assert "/home/" not in serialized
