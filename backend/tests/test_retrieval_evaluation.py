"""Pure contract tests for retrieval evaluation record building.

The real 104-case runs against Qdrant are validated separately in the
integration/acceptance gates; these tests cover the deterministic helpers.
"""

from core.schema import RetrievedDocument
from evaluation.retrieval_eval import (
    build_retrieval_record,
    evidence_unit_id,
    item_record,
)

D1 = "foods/restaurants/quan a.md"


def make_doc(section="Thông tin", score=0.7, extra=None):
    return RetrievedDocument(
        id="chunk-1",
        score=score,
        text="Nội dung đoạn",
        metadata={
            "chunk_id": "chunk-1",
            "source": D1,
            "section": section,
            "title": "Quán A",
            "dense_score": score,
            "retrieval_profile": "dense_only",
            "retrieval_rank": 1,
            **(extra or {}),
        },
    )


def test_evidence_unit_id_source_section():
    assert evidence_unit_id(make_doc()) == (D1, "Thông tin")


def test_item_record_is_safe_projection():
    """The artifact projection carries data needed for audit and coverage only."""
    record = item_record(make_doc())
    for field in (
        "id",
        "chunk_id",
        "score",
        "source",
        "section",
        "title",
        "text",
        "retrieval_profile",
        "retrieval_rank",
    ):
        assert field in record
        assert record[field] is not None
    # no nested metadata, no raw provider/secret fields.
    assert "metadata" not in record
    assert "api_key" not in json_dump(record)
    assert "OPENAI" not in json_dump(record).upper()


def test_build_retrieval_record_carries_run_identity():
    doc = make_doc(extra={"bm25_score": 0.5, "hybrid_score": 0.6})
    record = build_retrieval_record(
        run_id="retrieval-20260822-142157-hybrid_rerank-cf601f16",
        timestamp_utc_plus_7="2026-08-22 14:21:57",
        dataset_path="knowledge-base-hue/foods/evaluation/tests.jsonl",
        dataset_checksum="cf601f16",
        corpus_checksum="12345678",
        config_checksum="abcd1234",
        case_id="foods-0001",
        category="direct_fact",
        question="Quán A nằm ở đâu?",
        profile="hybrid_rerank",
        embedding_provider="sentence_transformer",
        embedding_model="intfloat/multilingual-e5-small",
        collection_name="hue_foods_e5_small_384",
        retrieved_items=[item_record(doc)],
        metrics={"recall_at_5": 1.0},
        setup_latency_ms=120,
        latency_ms=45,
    )
    assert record["run_id"] == "retrieval-20260822-142157-hybrid_rerank-cf601f16"
    assert record["case_id"] == "foods-0001"
    assert record["profile"] == "hybrid_rerank"
    assert record["collection_name"] == "hue_foods_e5_small_384"
    assert record["metrics"] == {"recall_at_5": 1.0}
    assert record["status"] == "complete"
    assert record["error_type"] is None
    assert record["latency_ms"] == 45
    assert record["setup_latency_ms"] == 120
    assert record["retrieved_items"][0]["bm25_score"] == 0.5


def test_failed_retrieval_record_keeps_status_and_error_type():
    record = build_retrieval_record(
        run_id="r",
        timestamp_utc_plus_7="t",
        dataset_path="d",
        dataset_checksum="c",
        corpus_checksum="c2",
        config_checksum="c3",
        case_id="foods-0002",
        category="temporal",
        question="q",
        profile="dense_only",
        embedding_provider="sentence_transformer",
        embedding_model="m",
        collection_name="col",
        retrieved_items=[],
        metrics={},
        setup_latency_ms=None,
        latency_ms=None,
        status="qdrant_error",
        error_type="RetrievalDependencyError",
    )
    assert record["status"] == "qdrant_error"
    assert record["error_type"] == "RetrievalDependencyError"
    assert record["metrics"] == {}


def json_dump(obj):
    import json

    return json.dumps(obj)
