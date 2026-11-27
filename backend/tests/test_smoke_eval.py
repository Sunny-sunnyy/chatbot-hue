"""Unit tests cho `evaluation.smoke_eval` (0 USD, không cần `.env` hay Qdrant)."""

import json
from pathlib import Path

import httpx

from evaluation import smoke_eval
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER, OUT_OF_SCOPE_ANSWER


def test_load_smoke_cases_has_14_public_cases_and_no_sealed():
    cases = smoke_eval.load_smoke_cases()
    assert len(cases) == 14
    kinds = {c.kind for c in cases}
    assert kinds == {"in_corpus", "refusal", "small_talk", "itinerary"}
    assert sum(1 for c in cases if c.kind == "refusal") == 2
    assert sum(1 for c in cases if c.kind == "small_talk") == 1
    assert sum(1 for c in cases if c.kind == "itinerary") == 1
    assert sum(1 for c in cases if c.kind == "in_corpus") == 10
    for c in cases:
        assert "sealed" not in c.case_id.lower()
        assert "sealed" not in c.query.lower()


def test_score_case_catches_all_failure_modes():
    in_corpus = smoke_eval.SmokeCase(
        case_id="c1",
        kind="in_corpus",
        query="Vé vào Xương Lăng bao nhiêu?",
        payload={"query": "Vé vào Xương Lăng bao nhiêu?"},
        keywords=("Xương Lăng", "50.000"),
    )
    # 1. Đạt chuẩn + ghi nhận keyword hit/miss
    ok = smoke_eval.score_case(
        in_corpus,
        http_status=200,
        body={"answer": "Vé vào Xương Lăng là 50.000 đồng [1].", "sources": [{"id": 1, "title": "Vé"}]},
        latency_ms=100.0,
    )
    assert ok.passed and ok.keyword_hits == ["Xương Lăng", "50.000"] and ok.keyword_misses == []

    # 2. Từ chối sai trên câu trong kho -> FAIL
    wrong_refusal = smoke_eval.score_case(
        in_corpus,
        http_status=200,
        body={"answer": INSUFFICIENT_ANSWER, "sources": []},
        latency_ms=100.0,
    )
    assert not wrong_refusal.passed and wrong_refusal.is_refusal

    # 3. Thiếu sources hoặc lộ [n] / [Nguồn 1] / [99] -> FAIL
    leak = smoke_eval.score_case(
        in_corpus,
        http_status=200,
        body={"answer": "Vé là 50.000 [Nguồn 1] [99] [n].", "sources": [{"id": 1, "title": "Vé"}]},
        latency_ms=100.0,
    )
    assert not leak.passed
    assert any("citation_leak" in r for r in leak.reasons)

    # 4. Câu ngoài kho / ngoài tỉnh KHÔNG từ chối -> FAIL
    oos = smoke_eval.SmokeCase(case_id="oos", kind="refusal", query="Ở Hội An ăn gì?", payload={"query": "Ở Hội An ăn gì?"})
    not_refused = smoke_eval.score_case(
        oos,
        http_status=200,
        body={"answer": "Hội An có cao lầu rất ngon [1].", "sources": [{"id": 1, "title": "Ẩm thực"}]},
        latency_ms=80.0,
    )
    assert not not_refused.passed

    # 5. Câu ngoài kho từ chối đúng chuẩn -> PASS
    refused_ok = smoke_eval.score_case(
        oos,
        http_status=200,
        body={"answer": OUT_OF_SCOPE_ANSWER, "sources": []},
        latency_ms=80.0,
    )
    assert refused_ok.passed and refused_ok.is_refusal

    # 6. Lập lịch biểu mẫu thiếu ngày -> FAIL
    itin = smoke_eval.SmokeCase(
        case_id="itin",
        kind="itinerary",
        query="lên lịch",
        payload={"query": "lên lịch", "bieu_mau": True, "truong": {"so_ngay": "2", "nguoi_lon": 2}},
        expected_days=2,
    )
    bad_itin = smoke_eval.score_case(
        itin,
        http_status=200,
        body={
            "answer": "Lịch 1 ngày [1].",
            "sources": [{"id": 1, "title": "Đại Nội"}],
            "lich_trinh": {"phien_ban": 2, "lich": {"ngay": [{"ngay": 1, "muc": [{"id_muc": "1"}]}]}},
        },
        latency_ms=200.0,
    )
    assert not bad_itin.passed and any("expected 2 days" in r for r in bad_itin.reasons)


def test_dry_run_cli_writes_json_and_catches_control_fail(tmp_path: Path, capsys):
    out_file = tmp_path / "nested" / "smoke.json"
    code = smoke_eval.main(["--base-url", "http://127.0.0.1:8010", "--dry-run", "--output", str(out_file)])
    assert code == 0
    assert out_file.is_file()
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert data["mode"] == "dry_run"
    assert data["total_cases"] == 14
    assert data["passed_cases"] == 14
    assert data["overall_passed"] is True
    assert data["control_case"]["passed"] is False
    assert data["latency_ms"]["p50"] is not None and data["latency_ms"]["p95"] is not None
    out = capsys.readouterr().out
    assert "control_intentional_fail" in out and "CAUGHT" in out


def test_run_live_uses_mock_transport_and_returns_exit_1_on_fail(monkeypatch, tmp_path: Path):
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content.decode("utf-8"))
        if "Hội An" in body["query"] or "Thăng Long" in body["query"]:
            return httpx.Response(200, json={"answer": OUT_OF_SCOPE_ANSWER, "sources": []})
        if body["query"] == "Xin chào":
            return httpx.Response(200, json={"answer": "Xin chào bạn!", "sources": []})
        if body.get("bieu_mau"):
            return httpx.Response(200, json={"answer": "Lịch của bạn", "sources": []})  # cố tình thiếu lich_trinh + sources -> FAIL
        return httpx.Response(200, json={"answer": "Câu trả lời mẫu [1].", "sources": [{"id": 1, "title": "Kho"}]})

    transport = httpx.MockTransport(handler)
    real_client = httpx.Client
    monkeypatch.setattr(smoke_eval.httpx, "Client", lambda **kw: real_client(transport=transport, **kw))

    out_file = tmp_path / "live_fail.json"
    code = smoke_eval.main(["--base-url", "http://testserver", "--output", str(out_file)])
    assert code == 1
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert data["overall_passed"] is False
    assert data["failed_cases"] == 1
