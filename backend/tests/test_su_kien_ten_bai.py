"""Sự kiện `searched` mang tên các BÀI đã tìm thấy (22/11/2026, việc X13 — giao diện mới dùng cho lúc chờ). Vì sao: tin dài nhiều ý chờ 22–30 giây, mọi
sự kiện dồn vào 5–10 giây đầu rồi im 17–20 giây lúc model viết; server chỉ báo SỐ nguồn nên màn hình không có gì để đọc. Nay sự kiện kèm tên bài (không
trùng, theo thứ tự vào ngữ cảnh, không tính nguồn do code dựng) + `bai_id` như danh sách nguồn. Giao diện hiện tại bỏ qua trường mới. 0 USD."""
import asyncio
import dataclasses
import json
import time

import pytest

from api.routes.chat import STREAM_METRIC_FIELDS, StreamEvents, _answer_events
from core.settings_loader import load_settings
from ingestion.source_state import discover_full_corpus_files
from llm import liet_ke as lk
from llm import the_noi as thn
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn_stream_parallel, bai_da_tim
from retrieval.full_corpus_context import PackedSource
from test_b2_tool_loop import answer, deps, generator, tool_call  # noqa: F401  (`deps` = fixture tìm kho thật)
from test_chat_stream import parse_sse


def _nguon(i, ten, rel, muc=("Mục",)):
    return PackedSource(id=i, title=ten, heading_path=muc, excerpts=("đoạn",), source=rel)


def test_found_articles_are_unique_in_context_order_and_skip_sources_built_by_code():
    trace = AnswerTrace(so_nguon=[
        _nguon(1, "Dinh Gió Bấc", "heritages/heritage/dinh gio bac.md"),
        _nguon(2, "Quán Mây", "foods/restaurants/quan may.md"),
        _nguon(3, "Dinh Gió Bấc", "heritages/heritage/dinh gio bac.md", ("Mục khác",)),   # đoạn thứ hai của cùng bài ⇒ một tên
        _nguon(4, "Lăng Thử", "heritages/heritage/lang thu.md", (thn.MUC_THE,)),            # thẻ nơi ⇒ không phải bài vừa tìm thấy
        _nguon(5, "Vé thử", thn.BAI_VE_LE, (thn.MUC_VE,)),                                  # hàng vé của thẻ
        _nguon(6, lk.TIEU_DE_NGUON, lk.NGUON_SOURCE),                                       # nguồn do công cụ liệt kê dựng
    ])
    assert bai_da_tim(trace) == [{"title": "Dinh Gió Bấc", "source": "heritages/heritage/dinh gio bac.md"}, {"title": "Quán Mây", "source": "foods/restaurants/quan may.md"}]
    assert bai_da_tim(AnswerTrace()) == []


def test_route_turns_the_article_path_into_bai_id_and_leaves_other_status_events_alone():
    stream = StreamEvents(dict.fromkeys(STREAM_METRIC_FIELDS), time.perf_counter(), bai_ids=frozenset({"a/co.md"}))
    su_kien = {"stage": "searched", "n_sources": 3, "bai": [{"title": "Có", "source": "a/co.md"}, {"title": "Không", "source": "a/khong.md"}]}
    (_, du), = parse_sse([stream.status(su_kien)])
    assert du == {"stage": "searched", "n_sources": 3, "bai": [{"title": "Có", "bai_id": "a/co.md"}, {"title": "Không", "bai_id": None}]}
    assert su_kien["bai"][0] == {"title": "Có", "source": "a/co.md"}                       # dữ liệu của lõi không bị sửa tại chỗ
    assert parse_sse([stream.status({"stage": "generating"})]) == [("status", {"stage": "generating"})]


@pytest.mark.parametrize("parallel", [False, True])
def test_through_the_route_each_search_reports_the_articles_found_so_far(deps, parallel):
    """Đúng đường người dùng đi: lần tìm đầu của code rồi một lần tìm của model — mỗi sự kiện `searched` kèm danh sách cộng dồn."""
    dem = []

    def script(n, kw):
        if "ngoai_pham_vi" in (kw.get("instructions") or ""):  # lời dặn định tuyến
            return [{"type": "message", "id": f"r{n}", "role": "assistant", "status": "completed",
                     "content": [{"type": "output_text", "text": json.dumps({"route": "tro_ly_hue"}), "annotations": []}]}]
        dem.append(n)
        return [tool_call("quán bún bò ngon ở Huế")] if len(dem) == 1 else [answer("Huế có nhiều món đáng thử [1].")]

    settings = load_settings(validate_private_paths=False)
    flags = AssistantFlags(router=True, tim_them=True, cau_nhieu_y=True, song_song_tra_loi=parallel, the_noi=True,
                           the_noi_bang=thn.dung_bang(lk.nap_muc_luc(*discover_full_corpus_files(settings))))
    trace, metrics = AnswerTrace(), dict.fromkeys(STREAM_METRIC_FIELDS)

    async def go():
        turn = answer_turn_stream_parallel("Huế có món gì ngon, ăn ở đâu?", *deps, generator(script), trace, flags, None, None)
        return parse_sse([e async for e in _answer_events(turn, trace, metrics, time.perf_counter())])
    events = asyncio.run(go())
    da_tim = [d for k, d in events if k == "status" and d.get("stage") == "searched"]
    assert len(da_tim) == 2 and "error" not in [k for k, _ in events]
    dau, sau = ([b["title"] for b in d["bai"]] for d in da_tim)
    assert dau and sau[:len(dau)] == dau and len(sau) > len(dau) and len(set(sau)) == len(sau)   # cộng dồn, giữ thứ tự, không trùng
    that = {s.title for s in trace.so_nguon if s.source.endswith(".md") and s.heading_path not in ((thn.MUC_THE,), (thn.MUC_VE,))}
    assert set(sau) == that and trace.the_noi and not (set(trace.the_noi) - that) & set(sau)        # có thẻ nơi trong lượt mà tên thẻ không lọt vào danh sách
    assert all(set(b) == {"title", "bai_id"} for d in da_tim for b in d["bai"]) and da_tim[1]["n_sources"] == len(trace.so_nguon)
