"""Cờ `nho_cau_tra_loi` — lượt bị rút vì lỗi trích dẫn trong khi lịch sử đang mang câu trả lời liền trước ⇒ chạy lại MỘT lần với lịch sử như khi cờ tắt
(22/11/2026). 0 USD: tìm kho thật, model theo kịch bản. Vì sao: lượt đo 22/11, chuỗi "Lên kế hoạch tham quan Huế 2 ngày" ⇒ "Bỏ Chợ Đông Ba đi": 3 / 7 lần
người dùng thấy màn hình lỗi trích dẫn (model chép lại lời cũ của nó, không trích nguồn). Mọi ca đi qua `answer_turn_stream_parallel` — đường người dùng đi."""
import dataclasses
import json
import time

import pytest

from api.conversations import NHAN_LOI_TRUOC, ConversationStore
from api.routes.chat import STREAM_METRIC_FIELDS, _answer_events
from llm.assistant import TEN_CHAY_LAI, AnswerTrace, AssistantFlags, _luot_stream, answer_turn_stream_parallel
from test_b2_tool_loop import answer, deps, generator  # noqa: F401  (`deps` = fixture tìm kho thật)
from test_b6_tra_web import _events
from test_chat_stream import parse_sse

CO = AssistantFlags(router=True, tim_them=True)
CAU_TRUOC, CAU = "Vé lẻ vào Đại Nội giá bao nhiêu?", "Thế trẻ em thì bao nhiêu?"
CO_DAP = ((CAU_TRUOC, f"{NHAN_LOI_TRUOC}\nVé lẻ người lớn 200.000 đồng."),)   # lịch sử đang mang câu trả lời liền trước
KHONG_DAP = ((CAU_TRUOC, ""),)                                                  # chính lịch sử đó khi không nhớ câu trả lời
KHONG_TRICH, CO_TRICH = "Trẻ em 40.000 đồng.", "Trẻ em 40.000 đồng [1]."


def kich_ban(luon_khong_trich=False):
    """Model: thấy câu trả lời nhớ trong lịch sử ⇒ trả lời KHÔNG trích nguồn (như lượt đo thật); không thấy ⇒ trả lời có trích nguồn."""
    thay_dap = []  # mỗi lần gọi TRẢ LỜI: đầu vào có mang câu trả lời nhớ không

    def script(n, kw):
        ins = kw.get("instructions") or ""
        if "tro_ly_hue" in ins and "ngoai_pham_vi" in ins:  # lời dặn định tuyến
            return [{"type": "message", "id": f"r{n}", "role": "assistant", "status": "completed",
                     "content": [{"type": "output_text", "text": json.dumps({"route": "tro_ly_hue"}), "annotations": []}]}]
        co = NHAN_LOI_TRUOC in json.dumps(kw["input"], ensure_ascii=False)
        thay_dap.append(co)
        return [answer(KHONG_TRICH if co or luon_khong_trich else CO_TRICH)]
    return script, thay_dap


def chay(deps, parallel, *, history=CO_DAP, khong_dap=KHONG_DAP, luon_khong_trich=False, ham=answer_turn_stream_parallel):
    script, thay_dap = kich_ban(luon_khong_trich)
    trace = AnswerTrace(history=history, lich_su_khong_dap=khong_dap)
    events = _events(ham, CAU, *deps, generator(script), trace, dataclasses.replace(CO, song_song_tra_loi=parallel), None, None)
    return trace, events, thay_dap


@pytest.mark.parametrize("parallel", [False, True])
def test_retracted_turn_with_a_remembered_answer_is_rerun_once_without_it(deps, parallel):
    trace, events, thay_dap = chay(deps, parallel)
    assert thay_dap == [True, False]                       # lần đầu thấy câu trả lời nhớ; lần chạy lại thì không
    assert [d for k, d in events if k == "thay_chu"] == [""]  # gỡ chữ chưa trích nguồn đã hiện, đúng một lần
    i = next(n for n, (k, _) in enumerate(events) if k == "thay_chu")
    assert KHONG_TRICH in "".join(d for k, d in events[:i] if k == "delta") and CO_TRICH in "".join(d for k, d in events[i:] if k == "delta")
    assert trace.citation_error is None and trace.answer == CO_TRICH and trace.cited      # kết quả của lượt = kết quả lần hai
    assert trace.history == CO_DAP                         # đầu vào của route giữ nguyên (số đo lịch sử của lượt không đổi nghĩa)
    assert trace.tools[-1] == {"name": TEN_CHAY_LAI, "ms": 0.0, "loi_lan_dau": "Grounded answer has no citation"}
    assert len(trace.llm_calls) == 4                       # tiền của CẢ hai lần: hai lần định tuyến + hai lần trả lời


@pytest.mark.parametrize("parallel", [False, True])
def test_second_run_also_retracted_ends_as_the_old_error_and_does_not_loop(deps, parallel):
    trace, events, thay_dap = chay(deps, parallel, luon_khong_trich=True)
    assert thay_dap == [True, False]                       # đúng hai lần gọi trả lời, không lần thứ ba
    assert trace.citation_error is not None and [d for k, d in events if k == "thay_chu"] == [""]
    assert trace.tools[-1]["name"] == TEN_CHAY_LAI


@pytest.mark.parametrize("parallel", [False, True])
def test_turns_without_a_remembered_answer_or_not_retracted_run_exactly_as_before(deps, parallel):
    """Cờ tắt (route không bao giờ đặt `lich_su_khong_dap`) hoặc ô cuối không mang câu trả lời: lượt bị rút vẫn là lỗi cũ, không chạy lại, và chuỗi sự
    kiện GIỐNG HỆT hàm thân `_luot_stream`. Lượt có câu trả lời nhớ mà KHÔNG bị rút: cũng không chạy lại."""
    trace, events, thay_dap = chay(deps, parallel, history=KHONG_DAP, khong_dap=None, luon_khong_trich=True)
    assert thay_dap == [False] and trace.citation_error is not None
    assert all(c["name"] != TEN_CHAY_LAI for c in trace.tools) and not [e for e in events if e[0] == "thay_chu"]
    _, goc, _ = chay(deps, parallel, history=KHONG_DAP, khong_dap=None, luon_khong_trich=True, ham=_luot_stream)
    assert events == goc
    # có câu trả lời nhớ nhưng model vẫn trích nguồn đúng ⇒ một lần gọi, không sự kiện thay chữ
    script_tot = lambda n, kw: ([{"type": "message", "id": f"r{n}", "role": "assistant", "status": "completed", "content": [
        {"type": "output_text", "text": json.dumps({"route": "tro_ly_hue"}), "annotations": []}]}]
        if "ngoai_pham_vi" in (kw.get("instructions") or "") else [answer(CO_TRICH)])
    trace = AnswerTrace(history=CO_DAP, lich_su_khong_dap=KHONG_DAP)
    events = _events(answer_turn_stream_parallel, CAU, *deps, generator(script_tot), trace, dataclasses.replace(CO, song_song_tra_loi=parallel), None, None)
    assert trace.citation_error is None and len(trace.llm_calls) == 2 and not [e for e in events if e[0] == "thay_chu"]
    assert all(c["name"] != TEN_CHAY_LAI for c in trace.tools)


def test_conversation_with_a_saved_plan_is_not_rerun(deps):
    """Cuộc có lịch đã lưu đi đường sửa lịch — bản sửa hẹp này không chạm (chưa đo): lượt bị rút vẫn là lỗi cũ."""
    script, thay_dap = kich_ban(luon_khong_trich=True)
    trace = AnswerTrace(history=CO_DAP, lich_su_khong_dap=KHONG_DAP, lich_luu={"khung": {}})
    _events(answer_turn_stream_parallel, CAU, *deps, generator(script), trace, CO, None, None)  # `sua_lich_v2` tắt ⇒ vẫn đường thường, nhưng không chạy lại
    assert thay_dap == [True] and trace.citation_error is not None


def test_store_gives_the_history_without_the_remembered_answer_only_when_one_is_held():
    kho = ConversationStore(len, chi_dap_lien_truoc=True)
    cid = kho.ensure(None)
    assert kho.history_khong_dap(cid) is None                                   # cuộc mới: không có gì để lùi
    kho.append(cid, "câu 1", "Trả lời một [1].", ghi_chu="[ghi chú tên nơi]")
    assert kho.history(cid)[-1][1].startswith(NHAN_LOI_TRUOC)
    assert kho.history_khong_dap(cid) == (("câu 1", "[ghi chú tên nơi]"),)      # ô cuối về dòng ghi chú, như khi cờ tắt
    kho.append(cid, "câu 2", "", ghi_chu="")                                    # lượt không được nhớ đáp (câu cố định, lịch…)
    assert kho.history_khong_dap(cid) is None and kho.history(cid)[0] == ("câu 1", "[ghi chú tên nơi]")
    assert ConversationStore(len).history_khong_dap(ConversationStore(len).ensure(None)) is None


def test_route_turns_the_core_replace_event_into_one_clean_final_text():
    """Route: `thay_chu` từ lõi xoá sổ chữ đã phát ⇒ chữ lần hai hiện như một lượt thường (không nối vào chữ lần đầu, không thêm sự kiện thay chữ lúc kết)."""
    from retrieval.full_corpus_context import PackedSource
    src = PackedSource(id=1, title="Bài", heading_path=("Mục",), excerpts=("Trẻ em 40.000 đồng.",), source="travel/tickets/x.md")
    trace = AnswerTrace(answer=CO_TRICH, cited=(src,), so_nguon=[src])

    async def luot():
        yield "delta", KHONG_TRICH
        yield "thay_chu", ""
        yield "status", {"stage": "generating"}
        yield "delta", CO_TRICH

    async def go():
        metrics = dict.fromkeys(STREAM_METRIC_FIELDS)
        return metrics, parse_sse([e async for e in _answer_events(luot(), trace, metrics, time.perf_counter())])
    import asyncio
    metrics, events = asyncio.run(go())
    assert [k for k, _ in events] == ["delta", "thay_chu", "status", "delta", "sources", "done"]
    assert events[1][1] == {"text": ""} and metrics["outcome"] == "success" and metrics["delta_matches_final"] is True and metrics["thay_chu"] is True


def test_whole_route_reruns_and_the_user_gets_an_answer_instead_of_the_error_screen():
    """Qua CẢ route thật (kho cuộc trò chuyện ⇒ lịch sử để lùi ⇒ lõi chạy lại ⇒ sự kiện gửi trình duyệt ⇒ sổ số đo ⇒ lượt được nhớ), model theo kịch bản:
    lượt 1 trả lời có nguồn ⇒ được nhớ; lượt 2 model thấy câu trả lời nhớ thì viết không trích nguồn ⇒ trước bản sửa là sự kiện `error` (màn hình
    "Thử lại"); nay: chữ lần đầu bị gỡ, lượt kết thúc `success` bằng câu trả lời có nguồn của lần chạy lại."""
    import copy
    import logging

    from fastapi.testclient import TestClient

    from api.app import create_app
    from core.settings_loader import load_settings

    s = copy.deepcopy(load_settings(validate_private_paths=False))
    s["assistant"]["cache_cau_tra_loi"] = False
    assert s["assistant"]["nho_cau_tra_loi"] is True  # tính năng đang mở ở settings — bản sửa này sống cùng nó
    script, thay_dap = kich_ban()
    so_do = []

    class Bat(logging.Handler):
        def emit(self, r):
            m = r.getMessage()
            if m.startswith("chat_metrics "):
                so_do.append(json.loads(m[len("chat_metrics "):]))
    bat = Bat()
    app = create_app(s)
    with TestClient(app) as client:
        logging.getLogger("chat").addHandler(bat)
        goc = app.state.generator, app.state.generator_ready
        app.state.generator, app.state.generator_ready = generator(script), True
        try:
            r1 = client.post("/api/chat/stream", json={"query": CAU_TRUOC})
            r2 = client.post("/api/chat/stream", json={"query": CAU})
            lich_su = app.state.conversations.history(client.cookies.get("hue_conversation") or next(iter(app.state.conversations._items)))
        finally:
            app.state.generator, app.state.generator_ready = goc
            logging.getLogger("chat").removeHandler(bat)
    e1, e2 = (parse_sse([k + b"\n\n" for k in r.content.split(b"\n\n") if k.strip()]) for r in (r1, r2))
    assert [k for k, _ in e1 if k in ("error", "thay_chu")] == [] and so_do[0]["outcome"] == "success"
    assert thay_dap == [False, True, False]                                    # lượt 1 · lượt 2 lần đầu (thấy câu trả lời nhớ) · lượt 2 chạy lại (không thấy)
    ten = [k for k, _ in e2]
    assert "error" not in ten and ten.count("thay_chu") == 1 and ten[-1] == "done" and "sources" in ten
    i = ten.index("thay_chu")
    assert e2[i][1] == {"text": ""} and KHONG_TRICH in "".join(d["text"] for k, d in e2[:i] if k == "delta")
    assert "".join(d["text"] for k, d in e2[i:] if k == "delta").strip() == CO_TRICH
    assert so_do[1]["outcome"] == "success" and so_do[1]["loi_kiem"] is None and so_do[1]["thay_chu"] is True
    assert {"name": TEN_CHAY_LAI, "ms": 0.0, "loi_lan_dau": "Grounded answer has no citation"} in so_do[1]["tools"]
    assert so_do[1]["n_llm_calls"] == 4                                        # cả hai lần chạy của lượt 2 đều vào sổ tiền
    assert lich_su[-1][0] == CAU and "Trẻ em 40.000 đồng" in lich_su[-1][1]    # lượt 2 được nhớ bằng câu trả lời của lần chạy lại
