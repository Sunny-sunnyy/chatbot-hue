"""Unit test cho `evaluation/faithfulness_eval.py` (HF_HUB_OFFLINE=1, không .env, 0 USD)."""
import asyncio
import json
from types import SimpleNamespace

import pytest

from core.schema import point_id_for_chunk_id
from evaluation import faithfulness_eval as fe
from llm.full_corpus_prompt import CAU_Y_THIEU, INSUFFICIENT_ANSWER, OUT_OF_SCOPE_ANSWER
from llm import thoi_tiet as tt
from retrieval.full_corpus_context import PackedSource


def test_strip_code_appended_blocks_removes_weather_and_missing_lines():
    answer = (
        f"{tt.CAU_DAU_BAO_LU}\n\n"
        "Chùa Thiên Mụ mở cửa ban ngày [1].\n"
        f"{CAU_Y_THIEU} giá gửi xe qua đêm.\n\n"
        "**Dự báo thời tiết Huế**\n"
        "- Thứ Hai 30/11: 22–26 °C, khả năng mưa cao nhất trong ngày 98 %, lượng mưa 36,0 mm\n"
        "Dữ liệu thời tiết: Open-Meteo.com (CC BY 4.0) — số liệu lúc 13:45 27/11.\n\n"
        f"{tt.CAU_BAO_LU}"
    )
    cleaned = fe.strip_code_appended_blocks(answer)
    assert cleaned == "Chùa Thiên Mụ mở cửa ban ngày [1]."


def test_resolve_row_sources_handles_api_sources_dict_and_chunk_resolver():
    api_row = {
        "sources": [
            {"id": 1, "title": "Chùa Thiên Mụ", "heading_path": ["Thông tin"], "excerpts": ["Khởi lập năm 1601."], "bai_id": "heritages/heritage/Chùa Thiên Mụ.md"},
        ]
    }
    res1 = fe.resolve_row_sources(api_row)
    assert len(res1) == 1 and res1[0].id == 1 and res1[0].excerpts == ("Khởi lập năm 1601.",)

    dict_row = {"sources": {"2": "Lăng Khải Định có 127 bậc thang.", "1": "Chùa Thiên Mụ xây năm 1601."}}
    res2 = fe.resolve_row_sources(dict_row)
    assert [s.id for s in res2] == [1, 2]

    seen_calls = []

    def fake_resolver(chunk_ids, limit):
        seen_calls.append((list(chunk_ids), limit))
        return [PackedSource(id=1, title="Quán Mệ Kéo", heading_path=(), excerpts=("20 Bạch Đằng.",))]

    eval_row = {"top_chunk_ids": ["a.md#0", "b.md#1"], "context_sources": 1}
    res3 = fe.resolve_row_sources(eval_row, resolver=fake_resolver)
    assert len(res3) == 1 and seen_calls == [(["a.md#0", "b.md#1"], 1)]


def test_qdrant_chunk_resolver_batches_retrieve_and_caches():
    chunk_a = "heritages/heritage/Chùa Thiên Mụ.md#0"
    chunk_b = "foods/restaurants/quan bun bo me keo.md#0"

    class FakeQdrant:
        def __init__(self):
            self.calls = []

        def retrieve(self, *, collection_name, ids, with_payload):
            self.calls.append((collection_name, list(ids)))
            assert ids == [point_id_for_chunk_id(chunk_a), point_id_for_chunk_id(chunk_b)]
            return [
                SimpleNamespace(payload={
                    "chunk_id": chunk_a,
                    "source": "heritages/heritage/Chùa Thiên Mụ.md",
                    "title": "Chùa Thiên Mụ",
                    "heading_path": ["Thông tin"],
                    "evidence_parts": [{"role": "body", "start": 0, "end": 10, "text": "Năm 1601."}],
                    "domain": "heritages",
                    "search_text": "Năm 1601.",
                }),
                SimpleNamespace(payload={
                    "chunk_id": chunk_b,
                    "source": "foods/restaurants/quan bun bo me keo.md",
                    "title": "Quán bún bò Mệ Kéo",
                    "heading_path": ["Thông tin"],
                    "evidence_parts": [{"role": "body", "start": 0, "end": 13, "text": "20 Bạch Đằng."}],
                    "domain": "foods",
                    "search_text": "20 Bạch Đằng.",
                }),
            ]

    qdrant = FakeQdrant()
    resolver = fe.QdrantChunkResolver(client=qdrant)
    sources = resolver.resolve([chunk_a, chunk_b], limit=2)
    assert [(s.id, s.title, s.excerpts) for s in sources] == [
        (1, "Chùa Thiên Mụ", ("Năm 1601.",)),
        (2, "Quán bún bò Mệ Kéo", ("20 Bạch Đằng.",)),
    ]
    # Lần hai dùng cache, không gọi lại Qdrant.
    sources_cached = resolver.resolve([chunk_a], limit=1)
    assert len(sources_cached) == 1 and len(qdrant.calls) == 1


def test_evaluate_row_faithfulness_catches_misattributed_and_hallucinated(monkeypatch):
    def fake_usage(in_tok, out_tok, cached_tok=0):
        return SimpleNamespace(
            input_tokens=in_tok,
            output_tokens=out_tok,
            input_tokens_details=SimpleNamespace(cached_tokens=cached_tok, cache_write_tokens=0),
        )

    extract_agent = fe.extract_statements_agent("gpt-6-luna")
    nli_agent = fe.nli_judge_agent("gpt-6-luna")

    async def fake_run(agent, *, input, max_turns, run_config):
        assert max_turns == 1
        if agent is extract_agent:
            return SimpleNamespace(
                raw_responses=[SimpleNamespace(usage=fake_usage(500, 40, 200))],
                final_output=fe.StatementsOutput(statements=[
                    fe.StatementItem(statement="Chùa Thiên Mụ khởi lập năm 1601.", cited_ids=[1]),
                    fe.StatementItem(statement="Lăng Khải Định có 127 bậc thang.", cited_ids=[1]),  # gán sai [1] thay vì [2]
                    fe.StatementItem(statement="Vé gửi xe qua đêm là 50.000 VNĐ.", cited_ids=[99]),  # mã lạ
                ]),
            )
        return SimpleNamespace(
            raw_responses=[SimpleNamespace(usage=fake_usage(700, 60, 400))],
            final_output=fe.NLIOutput(verdicts=[
                fe.NLIVerdict(statement_index=0, cited_supported=True, context_supported=True, reason="Đúng nguồn [1]."),
                fe.NLIVerdict(statement_index=1, cited_supported=False, context_supported=True, reason="Nằm ở [2], không phải [1]."),
                fe.NLIVerdict(statement_index=2, cited_supported=True, context_supported=False, reason="Không có trong nguồn."),
            ]),
        )

    monkeypatch.setattr(fe.Runner, "run", fake_run)

    row = {
        "id": "k_01",
        "question": "Thông tin Chùa Thiên Mụ và Lăng Khải Định?",
        "answer": "Chùa Thiên Mụ khởi lập năm 1601 [1]. Lăng Khải Định có 127 bậc thang [1]. Vé gửi xe qua đêm là 50.000 VNĐ [99].",
        "sources": [
            {"id": 1, "title": "Chùa Thiên Mụ", "heading_path": [], "excerpts": ["Khởi lập năm 1601."]},
            {"id": 2, "title": "Lăng Khải Định", "heading_path": [], "excerpts": ["Có 127 bậc thang."]},
        ],
        "expected_faithful": False,
    }
    res = asyncio.run(fe.evaluate_row_faithfulness(row, extract_agent=extract_agent, nli_agent=nli_agent))
    assert res["status"] == "ok"
    assert res["num_statements"] == 3
    assert res["cited_supported_count"] == 1
    assert res["context_supported_count"] == 2
    assert res["misattributed_count"] == 1
    assert res["hallucinated_count"] == 1
    assert res["is_faithful"] is False
    assert math_close(res["faithfulness_cited"], 1 / 3)
    assert math_close(res["faithfulness_context"], 2 / 3)
    assert res["input_tokens"] == 1200
    assert res["cached_tokens"] == 600
    assert res["output_tokens"] == 100
    assert res["usd"] > 0

    refusal_row = {"id": "k_ref", "answer": INSUFFICIENT_ANSWER, "sources": []}
    ref_res = asyncio.run(fe.evaluate_row_faithfulness(refusal_row, extract_agent=extract_agent, nli_agent=nli_agent))
    assert ref_res["status"] == "skipped_refusal" and ref_res["usd"] == 0.0

    oos_row = {"id": "k_oos", "answer": OUT_OF_SCOPE_ANSWER, "sources": []}
    oos_res = asyncio.run(fe.evaluate_row_faithfulness(oos_row, extract_agent=extract_agent, nli_agent=nli_agent))
    assert oos_res["status"] == "skipped_refusal" and oos_res["usd"] == 0.0

    summary = fe.summarize_faithfulness([res, ref_res])
    assert summary["evaluated"] == 1 and summary["skipped_refusal"] == 1
    assert summary["agreement"] == {"n": 1, "matched": 1, "agreement_rate": 1.0, "tp": 0, "tn": 1, "fp": 0, "fn": 0}


def math_close(a: float, b: float) -> bool:
    return abs(a - b) < 1e-5


def test_cli_dry_run_and_overwrite_guard(tmp_path, capsys):
    inp = tmp_path / "in.jsonl"
    inp.write_text(
        "\n".join([
            json.dumps({
                "id": "c1",
                "question": "Q1",
                "answer": "Cà phê muối giá 15.000 VNĐ [1].",
                "sources": [{"id": 1, "title": "Quán Cà Phê Muối", "heading_path": [], "excerpts": ["Cà phê muối: 15.000 VNĐ."]}],
            }, ensure_ascii=False),
            json.dumps({"id": "c2", "question": "Q2", "answer": INSUFFICIENT_ANSWER, "sources": []}, ensure_ascii=False),
            json.dumps({"id": "c3", "question": "Q3", "error": "Timeout", "answer": None}, ensure_ascii=False),
        ]) + "\n",
        encoding="utf-8",
    )
    assert fe.main(["--input", str(inp), "--dry-run", "--no-qdrant"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["dry_run"] == "ok"
    assert report["usd"] == 0.0
    assert report["total_rows"] == 3
    assert report["eligible_to_score"] == 1
    assert report["skipped_refusal"] == 1
    assert report["skipped_error"] == 1

    existing_out = tmp_path / "existing.jsonl"
    existing_out.write_text("", encoding="utf-8")
    with pytest.raises(SystemExit, match="exists:"):
        fe.main(["--input", str(inp), "--out", str(existing_out), "--no-qdrant"])
