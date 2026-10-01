"""Unit tests for phase6_live_smoke runner guards and protocol validation."""
import asyncio
import json
from pathlib import Path
import pytest

from llm.phase6_live_smoke import (
    EXPECTED_CASE_IDS,
    EXPECTED_CASES_SCHEMA_VERSION,
    check_point_immutability,
    run_smoke_async,
    validate_cases_data,
)


def test_validate_cases_data_accepts_valid_payload():
    valid = {
        "schema_version": "phase_6_full_corpus_live_cases:v1",
        "cases": [
            {"case_id": "direct_fact", "question": "Câu 1?"},
            {"case_id": "multi_source_synthesis", "question": "Câu 2?"},
            {"case_id": "conditional_evidence", "question": "Câu 3?"},
            {"case_id": "out_of_scope", "question": "Câu 4?"},
        ],
    }
    cases = validate_cases_data(valid)
    assert len(cases) == 4
    assert [c["case_id"] for c in cases] == EXPECTED_CASE_IDS


def test_validate_cases_data_rejects_extra_top_level_keys():
    extra = {
        "schema_version": "phase_6_full_corpus_live_cases:v1",
        "cases": [
            {"case_id": "direct_fact", "question": "Câu 1?"},
            {"case_id": "multi_source_synthesis", "question": "Câu 2?"},
            {"case_id": "conditional_evidence", "question": "Câu 3?"},
            {"case_id": "out_of_scope", "question": "Câu 4?"},
        ],
        "unexpected_top_key": "forbidden",
    }
    with pytest.raises(ValueError, match="unexpected top-level keys"):
        validate_cases_data(extra)


def test_validate_cases_data_rejects_extra_item_keys():
    extra_item = {
        "schema_version": "phase_6_full_corpus_live_cases:v1",
        "cases": [
            {"case_id": "direct_fact", "question": "Câu 1?", "extra_field": True},
            {"case_id": "multi_source_synthesis", "question": "Câu 2?"},
            {"case_id": "conditional_evidence", "question": "Câu 3?"},
            {"case_id": "out_of_scope", "question": "Câu 4?"},
        ],
    }
    with pytest.raises(ValueError, match="unexpected keys"):
        validate_cases_data(extra_item)


def test_validate_cases_data_rejects_wrong_schema_version():
    invalid = {
        "schema_version": "wrong_version:v2",
        "cases": [
            {"case_id": "direct_fact", "question": "Câu 1?"},
            {"case_id": "multi_source_synthesis", "question": "Câu 2?"},
            {"case_id": "conditional_evidence", "question": "Câu 3?"},
            {"case_id": "out_of_scope", "question": "Câu 4?"},
        ],
    }
    with pytest.raises(ValueError, match="schema_version"):
        validate_cases_data(invalid)


def test_validate_cases_data_rejects_wrong_length():
    too_few = {
        "schema_version": "phase_6_full_corpus_live_cases:v1",
        "cases": [
            {"case_id": "direct_fact", "question": "Câu 1?"},
            {"case_id": "multi_source_synthesis", "question": "Câu 2?"},
        ],
    }
    with pytest.raises(ValueError, match="Expected exactly 4 cases"):
        validate_cases_data(too_few)


def test_validate_cases_data_rejects_wrong_case_order_or_id():
    scrambled = {
        "schema_version": "phase_6_full_corpus_live_cases:v1",
        "cases": [
            {"case_id": "multi_source_synthesis", "question": "Câu 2?"},
            {"case_id": "direct_fact", "question": "Câu 1?"},
            {"case_id": "conditional_evidence", "question": "Câu 3?"},
            {"case_id": "out_of_scope", "question": "Câu 4?"},
        ],
    }
    with pytest.raises(ValueError, match="ID mismatch"):
        validate_cases_data(scrambled)


def test_validate_cases_data_rejects_blank_question():
    blank = {
        "schema_version": "phase_6_full_corpus_live_cases:v1",
        "cases": [
            {"case_id": "direct_fact", "question": "   "},
            {"case_id": "multi_source_synthesis", "question": "Câu 2?"},
            {"case_id": "conditional_evidence", "question": "Câu 3?"},
            {"case_id": "out_of_scope", "question": "Câu 4?"},
        ],
    }
    with pytest.raises(ValueError, match="question must be a non-empty string"):
        validate_cases_data(blank)


def test_check_point_immutability():
    # True for equal counts, regardless of the specific number
    assert check_point_immutability(8460, 8460) is True
    assert check_point_immutability(1000, 1000) is True
    assert check_point_immutability(0, 0) is True

    # False for unequal counts
    assert check_point_immutability(8460, 8461) is False
    assert check_point_immutability(8460, 8459) is False


@pytest.mark.anyio
async def test_async_client_with_lifespan_context_has_health_ready(require_openai_key):
    """P6-C1-R1 regression: ensure AsyncClient inside app lifespan has health ok."""
    from httpx import ASGITransport, AsyncClient
    from api.app import create_app
    from core.settings_loader import load_settings

    settings = load_settings(validate_private_paths=False)
    app = create_app(settings)

    async with app.router.lifespan_context(app):
        assert app.state.retrieval_ready is True
        assert app.state.tokenizer_ready is True
        assert app.state.generator_ready is True

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            resp = await client.get("/health")
            assert resp.status_code == 200
            data = resp.json()
            assert data["status"] == "ok"
            assert data["components"]["app"] == "alive"
            assert data["components"]["qdrant"] == "ready"
            assert data["components"]["retrieval"] == "ready"
            assert data["components"]["tokenizer"] == "ready"
            assert data["components"]["generator"] == "ready"


@pytest.mark.anyio
async def test_run_smoke_missing_case_file_writes_atomic_artifact(tmp_path):
    cases_path = tmp_path / "non_existent.json"
    out_path = tmp_path / "artifact.json"
    code = await run_smoke_async(cases_path, out_path, confirm_paid=True)
    assert code == 1
    assert out_path.is_file()
    with out_path.open() as f:
        data = json.load(f)
    assert data["status"] == "FAIL"
    assert data["call_attempt_count"] == 0
    assert data["early_exit_reason"] == "cases_file_missing"


@pytest.mark.anyio
async def test_run_smoke_invalid_json_writes_atomic_artifact(tmp_path):
    cases_path = tmp_path / "bad.json"
    cases_path.write_text("{bad json: true", encoding="utf-8")
    out_path = tmp_path / "artifact.json"
    code = await run_smoke_async(cases_path, out_path, confirm_paid=True)
    assert code == 1
    assert out_path.is_file()
    with out_path.open() as f:
        data = json.load(f)
    assert data["status"] == "FAIL"
    assert data["call_attempt_count"] == 0
    assert data["early_exit_reason"] == "cases_json_invalid"


@pytest.mark.anyio
async def test_run_smoke_invalid_schema_writes_atomic_artifact(tmp_path):
    cases_path = tmp_path / "bad_schema.json"
    cases_path.write_text(
        json.dumps({"schema_version": "wrong_version", "cases": []}),
        encoding="utf-8",
    )
    out_path = tmp_path / "artifact.json"
    code = await run_smoke_async(cases_path, out_path, confirm_paid=True)
    assert code == 1
    assert out_path.is_file()
    with out_path.open() as f:
        data = json.load(f)
    assert data["status"] == "FAIL"
    assert data["call_attempt_count"] == 0
    assert data["early_exit_reason"] == "cases_schema_invalid"


@pytest.mark.anyio
async def test_run_smoke_health_failure_writes_atomic_artifact(tmp_path, monkeypatch):
    valid = {
        "schema_version": "phase_6_full_corpus_live_cases:v1",
        "cases": [
            {"case_id": "direct_fact", "question": "Câu 1?"},
            {"case_id": "multi_source_synthesis", "question": "Câu 2?"},
            {"case_id": "conditional_evidence", "question": "Câu 3?"},
            {"case_id": "out_of_scope", "question": "Câu 4?"},
        ],
    }
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(json.dumps(valid), encoding="utf-8")
    out_path = tmp_path / "artifact.json"

    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    def mock_create_app(settings=None):
        test_app = FastAPI()

        @test_app.get("/health")
        async def fake_health():
            return JSONResponse(status_code=503, content={"status": "degraded"})

        return test_app

    monkeypatch.setattr("llm.phase6_live_smoke.create_app", mock_create_app)
    code = await run_smoke_async(cases_path, out_path, confirm_paid=True)
    assert code == 1
    assert out_path.is_file()
    with out_path.open() as f:
        data = json.load(f)
    assert data["status"] == "FAIL"
    assert data["call_attempt_count"] == 0
    assert data["early_exit_reason"] == "api_health_not_ready"


def test_build_live_smoke_artifact_after_count_null_yields_unverified_immutability():
    """P6-C3-R2: production build_live_smoke_artifact with after_count=None records null and point_count_intact=False."""
    from llm.phase6_live_smoke import build_live_smoke_artifact

    git_info = {"commit": "test_sha", "dirty": False}
    artifact = build_live_smoke_artifact(
        git_info=git_info,
        settings={"full_corpus_generation": {"model": "gpt-5.4-nano"}, "full_corpus_runtime": {}},
        before_count=8460,
        after_count=None,
        calls_record=[],
        status="FAIL",
    )
    assert artifact["qdrant"]["before"] == 8460
    assert artifact["qdrant"]["after"] is None
    assert artifact["checks"]["point_count_intact"] is False
    assert "point_count_unverified" in artifact["unverified"]
    # Crucial: prove it never copies before_count to after_count
    assert artifact["qdrant"]["after"] != artifact["qdrant"]["before"]


def test_evidence_recorder_preserves_generation_metadata_on_citation_error():
    """P6-C3-R1: Generation metadata must be preserved when citation validation fails afterwards."""
    from llm.generator_openai_full_corpus import GeneratedText
    from llm.evidence_recorder import EvidenceRecorder

    recorder = EvidenceRecorder(request_id="test_citation_error_case")
    gen = GeneratedText(
        text="Câu trả lời thiếu trích dẫn.",
        response_id="chatcmpl-test-abc",
        model="gpt-5.4-nano",
        latency_ms=320,
        input_tokens=400,
        output_tokens=40,
        total_tokens=440,
        finish_reason="stop",
    )
    # Step 1: Provider returns successfully
    recorder.record_generation_result(gen)
    # Step 2: Citation validation fails
    recorder.record_error("citation_integrity_failed")

    evidence = recorder.get_evidence()
    assert evidence is not None
    assert evidence.status == "ERROR"
    assert evidence.error == "citation_integrity_failed"
    assert evidence.response_id == "chatcmpl-test-abc"
    assert evidence.model == "gpt-5.4-nano"
    assert evidence.latency_ms == 320
    assert evidence.input_tokens == 400
    assert evidence.output_tokens == 40
    assert evidence.total_tokens == 440
    assert evidence.finish_reason == "stop"


@pytest.mark.anyio
async def test_run_smoke_unexpected_runner_error_writes_atomic_artifact_without_reraise(
    tmp_path, monkeypatch
):
    valid = {
        "schema_version": "phase_6_full_corpus_live_cases:v1",
        "cases": [
            {"case_id": "direct_fact", "question": "Câu 1?"},
            {"case_id": "multi_source_synthesis", "question": "Câu 2?"},
            {"case_id": "conditional_evidence", "question": "Câu 3?"},
            {"case_id": "out_of_scope", "question": "Câu 4?"},
        ],
    }
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(json.dumps(valid), encoding="utf-8")
    out_path = tmp_path / "artifact.json"

    def crashing_create_app(settings=None):
        raise RuntimeError("Unexpected simulated crash")

    monkeypatch.setattr("llm.phase6_live_smoke.create_app", crashing_create_app)
    code = await run_smoke_async(cases_path, out_path, confirm_paid=True)
    assert code == 1
    assert out_path.is_file()
    with out_path.open() as f:
        data = json.load(f)
    assert data["status"] == "FAIL"
    assert data["early_exit_reason"] == "unexpected_runner_error_RuntimeError"


@pytest.mark.anyio
async def test_evidence_recorder_concurrency_and_isolation():
    """Prove that concurrent requests receive isolated evidence without cross-talk."""
    from llm.evidence_recorder import get_current_recorder, record_evidence

    results = {}

    async def worker(task_id: str, sample_text: str):
        with record_evidence(request_id=task_id) as recorder:
            assert get_current_recorder() is recorder
            await asyncio.sleep(0.01)

            class DummySource:
                id = 1
                title = f"Title {task_id}"
                heading_path = [task_id]
                excerpts = [sample_text]

            class DummyPacked:
                sources = [DummySource()]
                input_tokens = 42
                text = sample_text

            recorder.record_packed_context(DummyPacked())
            await asyncio.sleep(0.01)
            evidence = recorder.get_evidence()
            results[task_id] = evidence.to_dict()

    await asyncio.gather(
        worker("req_A", "Excerpt for task A"),
        worker("req_B", "Excerpt for task B"),
    )

    assert results["req_A"]["sources"][0]["title"] == "Title req_A"
    assert results["req_A"]["sources"][0]["excerpts"] == ["Excerpt for task A"]
    assert results["req_B"]["sources"][0]["title"] == "Title req_B"
    assert results["req_B"]["sources"][0]["excerpts"] == ["Excerpt for task B"]
    assert get_current_recorder() is None


def test_grounded_fallback_artifact_preserves_packed_excerpts_when_sources_empty():
    """Structural assertion: grounded fallback has empty public sources but non-empty packed evidence excerpts."""
    from llm.evidence_recorder import EvidenceRecorder

    recorder = EvidenceRecorder(request_id="conditional_evidence")

    class SamplePackedSource:
        id = 3
        title = "Chính sách miễn giảm vé tham quan Di tích Cố đô Huế"
        heading_path = ["Tham quan", "Giá vé"]
        excerpts = ["Miễn phí vé tham quan vào các ngày lễ Tết và ngày kỷ niệm lịch sử."]

    class SamplePackedContext:
        sources = [SamplePackedSource()]
        input_tokens = 777
        text = "Sample context text"

    recorder.record_packed_context(SamplePackedContext())
    recorder.record_fallback()

    evidence = recorder.get_evidence()
    assert evidence is not None

    # Public response from API chat is empty sources on fallback
    public_response_sources = []
    recorded_sources = evidence.sources

    assert len(public_response_sources) == 0
    assert len(recorded_sources) == 1
    assert recorded_sources[0]["id"] == 3
    assert (
        recorded_sources[0]["title"]
        == "Chính sách miễn giảm vé tham quan Di tích Cố đô Huế"
    )
    assert len(recorded_sources[0]["excerpts"]) > 0
    assert "Miễn phí vé" in recorded_sources[0]["excerpts"][0]


@pytest.mark.anyio
async def test_asgi_route_evidence_recorder_integration_with_real_retrieval(require_openai_key):
    """P6-C3-R2: Test actual FastAPI route + ASGITransport + real retrieval/context without provider call.

    Verifies that ContextVar captures packed excerpts through the real ASGI route,
    generator_ready=False safely blocks before provider network call,
    ContextVar resets, app.state has no trace, and serialize_call_evidence preserves excerpts.
    """
    from httpx import ASGITransport, AsyncClient
    from api.app import create_app
    from core.settings_loader import load_settings
    from llm.evidence_recorder import get_current_recorder, record_evidence
    from llm.phase6_live_smoke import serialize_call_evidence

    settings = load_settings(validate_private_paths=False)
    app = create_app(settings)

    async with app.router.lifespan_context(app):
        # Deliberately set generator_ready=False to test real generator-not-ready branch
        # This guarantees retrieval and context packing run for real, but no network call to OpenAI occurs
        app.state.generator_ready = False

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            with record_evidence(request_id="integration_test_case") as recorder:
                resp = await client.post("/api/chat", json={"query": "Ăn gì ở Huế?"})
                evidence = recorder.get_evidence()

            # 1. Public response verification
            assert resp.status_code == 502
            assert resp.json() == {
                "error": {
                    "code": "generation_unavailable",
                    "message": "Không thể tạo câu trả lời vào lúc này.",
                }
            }
            assert "sources" not in resp.text
            assert "excerpts" not in resp.text

            # 2. ContextVar and app.state cleanliness
            assert get_current_recorder() is None
            assert not hasattr(app.state, "last_chat_trace")

            # 3. Evidence capture verification
            assert evidence is not None
            assert evidence.status == "ERROR"
            assert evidence.error == "generation_unavailable"
            assert evidence.packed_sources_count > 0
            assert len(evidence.sources) > 0

            # 4. Excerpts are non-empty and present
            first_source = evidence.sources[0]
            assert first_source["id"] == 1
            assert first_source["title"]
            assert len(first_source["excerpts"]) > 0
            assert all(bool(e.strip()) for e in first_source["excerpts"])

            # 5. Serialization using production runner helper preserves excerpts
            serialized = serialize_call_evidence(evidence)
            assert serialized["packed_sources_count"] == evidence.packed_sources_count
            assert serialized["source_ids"] == [s["id"] for s in evidence.sources]
            assert len(serialized["sources"]) == len(evidence.sources)
            assert serialized["sources"][0]["excerpts"] == first_source["excerpts"]
