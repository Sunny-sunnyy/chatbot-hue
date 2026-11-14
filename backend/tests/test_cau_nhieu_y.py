"""Việc agent (3) 14/11 — câu nhiều ý (plan `docs/superpowers/plans/2026-11-14-cau-nhieu-y-plan.md`, cờ `cau_nhieu_y`).
Khoá: lời dặn chỉ đổi đúng đoạn luật từ chối; cờ tắt ⇒ chuỗi gửi model giống byte; cổng web mở khi có dòng `CAU_Y_THIEU` không [n], đóng khi
dòng đó có [n] hoặc cờ tắt. Không gọi mạng (client giả ghi lại lời dặn gửi đi)."""
import asyncio
import dataclasses
import json
import itertools

import pytest
from openai.types.responses import Response

from llm.assistant import (AnswerTrace, AssistantFlags, _con_la_y_thieu, answer_turn, answer_turn_stream, answer_turn_stream_parallel,
                           chi_y_thieu, co_y_thieu, so_y, ve_y_thieu, web_gate_open)
from llm.full_corpus_prompt import (ANSWER_SYSTEM_INSTRUCTIONS, ANSWER_SYSTEM_INSTRUCTIONS_NHIEU_Y, CAU_Y_THIEU, INSUFFICIENT_ANSWER,
                                    _LUAT_NHIEU_Y, _LUAT_TU_CHOI)
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from llm.tra_web import KetQuaWeb

_ids = itertools.count(1)
USAGE = {"input_tokens": 100, "output_tokens": 20, "total_tokens": 120,
         "input_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0}, "output_tokens_details": {"reasoning_tokens": 3}}
TRA_LOI = f"Vé lẻ người lớn 200.000 đồng [1].\n{CAU_Y_THIEU} chương trình dịp Tết năm tới."


class Client:
    """Trả một câu trả lời cố định, ghi kwargs mọi lần gọi (để đọc lời dặn thật sự gửi đi)."""

    def __init__(self, text):
        self.calls, self.text = [], text
        self.responses = self

    async def create(self, **kwargs):
        self.calls.append(kwargs)
        out = [{"type": "message", "id": f"m{next(_ids)}", "role": "assistant", "status": "completed",
                "content": [{"type": "output_text", "text": json.dumps({"answer": self.text}, ensure_ascii=False), "annotations": []}]}]
        return Response.model_validate({"id": f"r{next(_ids)}", "created_at": 0, "model": "probe", "object": "response", "output": out,
                                        "parallel_tool_calls": False, "tool_choice": "auto", "tools": [], "usage": USAGE, "status": "completed"})

    async def close(self):
        return None


@pytest.fixture(scope="module")
def deps():
    from core.settings_loader import load_settings
    from evaluation.full_corpus_eval import build_context_builder, build_retrieval
    settings = load_settings(validate_private_paths=False)
    service = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    yield service, build_context_builder(settings)
    service.close()


def chay(deps, flags, text=TRA_LOI):
    client = Client(text)
    trace = AnswerTrace()
    asyncio.run(answer_turn("Vé lẻ vào Đại Nội giá bao nhiêu, dịp Tết năm tới có chương trình gì?", *deps,
                            OpenAIFullCorpusGenerator(client=client, model="probe"), trace, flags))
    return trace, client.calls


def test_instructions_change_only_the_refusal_paragraph():
    assert ANSWER_SYSTEM_INSTRUCTIONS.count(_LUAT_TU_CHOI) == 1
    assert ANSWER_SYSTEM_INSTRUCTIONS_NHIEU_Y == ANSWER_SYSTEM_INSTRUCTIONS.replace(_LUAT_TU_CHOI, _LUAT_NHIEU_Y)
    assert CAU_Y_THIEU in ANSWER_SYSTEM_INSTRUCTIONS_NHIEU_Y and INSUFFICIENT_ANSWER in ANSWER_SYSTEM_INSTRUCTIONS_NHIEU_Y
    assert CAU_Y_THIEU not in ANSWER_SYSTEM_INSTRUCTIONS


@pytest.mark.parametrize("text, co", [
    (TRA_LOI, True),
    (f"Giá 200.000 đồng [1].\n- {CAU_Y_THIEU} lịch Tết.", True),           # gạch đầu dòng
    (f"Giá 200.000 đồng [1].\n{CAU_Y_THIEU} lịch Tết [2].", False),        # dòng thiếu có trích dẫn ⇒ không tính
    (f"Giá 200.000 đồng [1].\n{CAU_Y_THIEU} lịch Tết [Nguồn 2].", False),
    (f"Giá vé có ghi: {CAU_Y_THIEU} x.", False),                             # không ở đầu dòng
    ("Giá 200.000 đồng [1].", False),
])
def test_missing_part_marker_detected_only_at_line_start_without_citation(text, co):
    assert co_y_thieu(text) is co


def _trace(answer, nhieu_y=True):
    return AnswerTrace(route="tro_ly_hue", answer=answer, nhieu_y=nhieu_y)


def test_gate_opens_on_marker_only_for_multi_part_turn():
    bat = AssistantFlags(router=True, tim_them=True, tra_web=True, cau_nhieu_y=True)
    assert web_gate_open(_trace(TRA_LOI), bat, object())
    assert not web_gate_open(_trace(TRA_LOI, nhieu_y=False), bat, object())                      # cờ tắt / câu một ý ⇒ như cũ: kho thắng
    assert not web_gate_open(_trace(f"Giá [1].\n{CAU_Y_THIEU} x [2]."), bat, object())            # dòng thiếu có [n]
    assert web_gate_open(_trace(INSUFFICIENT_ANSWER), bat, object())                              # câu từ chối vẫn mở như cũ
    assert not web_gate_open(dataclasses.replace(_trace(TRA_LOI), web={"outcome": "co_muc"}), bat, object())  # ≤ 1 lần tra / câu


def test_flag_off_sends_old_instructions_byte_identical_and_on_sends_per_part_rule(deps):
    tat = AssistantFlags(tim_them=True)
    bat = dataclasses.replace(tat, cau_nhieu_y=True)
    _, goi_tat = chay(deps, tat)
    _, goi_bat = chay(deps, bat)
    lo_tat, lo_bat = goi_tat[0]["instructions"], goi_bat[0]["instructions"]
    assert lo_tat == OpenAIFullCorpusGenerator(client=Client(""), model="probe").assistant_instructions   # giống byte bản trước
    assert CAU_Y_THIEU not in lo_tat
    assert lo_bat == lo_tat.replace(_LUAT_TU_CHOI, _LUAT_NHIEU_Y)                                        # chỉ khác đúng đoạn luật
    assert goi_tat[0]["input"] == goi_bat[0]["input"]                                                  # tin nhắn người dùng / ngữ cảnh không đổi


def test_answer_with_marker_opens_web_once_with_user_question(deps):
    flags = AssistantFlags(router=True, tim_them=True, tra_web=True, cau_nhieu_y=True)  # định tuyến giả lỗi ⇒ về tro_ly_hue
    truy_van = []

    async def tim_web(q):
        truy_van.append(q)
        return KetQuaWeb(trang_thai="rong", so_web=[], ms=1.0, loi=None, usd=0.0)
    client = Client(TRA_LOI)
    trace = AnswerTrace()
    cau = "Vé lẻ vào Đại Nội giá bao nhiêu, dịp Tết năm tới có chương trình gì?"
    asyncio.run(answer_turn(cau, *deps, OpenAIFullCorpusGenerator(client=client, model="probe"), trace, flags, tim_web=tim_web))
    assert trace.answer.startswith("Vé lẻ") and CAU_Y_THIEU in trace.answer                            # phần kho giữ nguyên
    assert len(truy_van) == 1 and "Đại Nội" in truy_van[0]                                             # truy vấn từ câu người dùng (D2)


# ---------- Vòng 2 (plan 2026-11-14-cau-nhieu-y-v2): (b) đếm vế hỏi · (a) chỉ dòng ý thiếu ⇒ câu từ chối ----------
CAU_HAI_Y = "Vé lẻ vào Đại Nội giá bao nhiêu, dịp Tết năm tới có chương trình gì?"


@pytest.mark.parametrize("cau, n", [
    (CAU_HAI_Y, 2),
    ("Huế có những loại chè nào nổi tiếng, quán chè nào đang được giới trẻ ghé nhiều nhất?", 2),
    ("Đồi Vọng Cảnh ngắm được cảnh gì, đi xe buýt lên đó có tiện không?", 2),
    ("Vé vào Đại Nội giá bao nhiêu?", 1),
    ("Con mình 14 tuổi nhưng cao hơn 1 mét 3, vào Bạch Mã mua vé trẻ em cần mang gì?", 1),  # dấu phẩy nhưng chỉ một vế hỏi
    ("Mình không cần hướng dẫn viên, chỉ muốn đi bộ quanh Kinh thành.", 0),                  # "không" giữa câu không phải tiểu từ hỏi
    # 14/11 chiều: hai vế nối bằng "và / còn" (không dấu phẩy) — câu thật bị từ chối cả câu vì đếm 1
    ("Đại Nội Huế mở cửa mấy giờ và gần đó có quán karaoke nào giá rẻ không?", 2),
    ("Vé Đại Nội bao nhiêu còn vé lăng Minh Mạng bao nhiêu?", 2),
    ("Bún bò và bánh khoái giá bao nhiêu?", 1),                                               # "và" nối hai món của MỘT câu hỏi
    ("Đi với trẻ nhỏ thì nên tham quan đâu?", 1),
])
def test_so_y_counts_question_clauses(cau, n):
    assert so_y(cau) == n


@pytest.mark.parametrize("text, chi", [
    (f"{CAU_Y_THIEU} khu cắm trại ở bãi biển X.", True),
    (f"- {CAU_Y_THIEU} giá vé tàu.\n\n- {CAU_Y_THIEU} giờ chạy.", True),
    (TRA_LOI, False),                                                                             # có phần kho ⇒ giữ
    ("", False),
])
def test_only_missing_lines_detected(text, chi):
    assert chi_y_thieu(text) is chi


def test_stream_hold_rule_keeps_prefixes_of_missing_lines_only():
    assert _con_la_y_thieu("") and _con_la_y_thieu(CAU_Y_THIEU[:6]) and _con_la_y_thieu(f"{CAU_Y_THIEU} x.\n- Tư")
    assert not _con_la_y_thieu("Vé lẻ") and not _con_la_y_thieu(f"{CAU_Y_THIEU} x.\nVé lẻ 200.000 đồng")


def test_one_part_question_with_flag_on_sends_old_instructions(deps):
    """(b): cờ bật nhưng câu một ý ⇒ lời dặn + tin nhắn gửi model giống byte cờ tắt."""
    tat = AssistantFlags(tim_them=True)
    bat = dataclasses.replace(tat, cau_nhieu_y=True)
    goi = {}
    for ten, f in (("tat", tat), ("bat", bat)):
        client = Client("Vé lẻ người lớn 200.000 đồng [1].")
        asyncio.run(answer_turn("Vé vào Đại Nội giá bao nhiêu?", *deps, OpenAIFullCorpusGenerator(client=client, model="probe"), AnswerTrace(), f))
        goi[ten] = client.calls[0]
    assert goi["tat"]["instructions"] == goi["bat"]["instructions"] and goi["tat"]["input"] == goi["bat"]["input"]
    assert CAU_Y_THIEU not in goi["bat"]["instructions"]


def test_only_missing_lines_becomes_refusal_and_opens_web(deps):
    """(a) đường không stream: chữ model chỉ còn dòng ý thiếu ⇒ câu từ chối chuẩn, không lỗi trích dẫn, cổng web mở một lần."""
    flags = AssistantFlags(router=True, tim_them=True, tra_web=True, cau_nhieu_y=True)
    truy_van = []

    async def tim_web(q):
        truy_van.append(q)
        return KetQuaWeb(trang_thai="rong", so_web=[], ms=1.0, loi=None, usd=0.0)
    trace = AnswerTrace()
    client = Client(f"{CAU_Y_THIEU} giá vé.\n{CAU_Y_THIEU} chương trình dịp Tết.")
    asyncio.run(answer_turn(CAU_HAI_Y, *deps, OpenAIFullCorpusGenerator(client=client, model="probe"), trace, flags, tim_web=tim_web))
    assert trace.nhieu_y and trace.chi_y_thieu and trace.answer == INSUFFICIENT_ANSWER and trace.citation_error is None
    assert len(truy_van) == 1


@pytest.mark.parametrize("parallel", [False, True])
def test_stream_never_shows_missing_only_text(deps, parallel):
    """(a) đường stream (cả #6 song song — đang bật ở settings): giao diện chỉ nhận câu từ chối chuẩn, không thấy dòng ý thiếu rồi bị thay."""
    from test_b2_tool_loop import generator
    from test_b6_tra_web import _events, serper
    flags = AssistantFlags(router=True, tim_them=True, tra_web=True, cau_nhieu_y=True, song_song_tra_loi=parallel)
    chi_thieu = f"{CAU_Y_THIEU} giá vé.\n{CAU_Y_THIEU} chương trình dịp Tết."

    def script(n, kw):
        ins = kw.get("instructions") or ""
        if "tro_ly_hue" in ins and "ngoai_pham_vi" in ins:  # lời dặn định tuyến
            return [{"type": "message", "id": f"r{n}", "role": "assistant", "status": "completed",
                     "content": [{"type": "output_text", "text": json.dumps({"route": "tro_ly_hue"}), "annotations": []}]}]
        from test_b2_tool_loop import answer
        return [answer(chi_thieu)]
    trace = AnswerTrace()
    path = answer_turn_stream_parallel if parallel else answer_turn_stream
    events = _events(path, CAU_HAI_Y, *deps, generator(script), trace, flags, None, serper())
    assert "".join(d for k, d in events if k == "delta") == INSUFFICIENT_ANSWER
    assert trace.answer == INSUFFICIENT_ANSWER and trace.citation_error is None and trace.web is not None


# 14/11 chiều: mục web của câu nhiều ý chỉ viết cho vế ý thiếu (plan 2026-11-14-web-y-thieu-plan.md) — vế do code chọn từ chữ người dùng
@pytest.mark.parametrize("cau, tra_loi, ve", [
    ("Đại Nội Huế mở cửa mấy giờ và gần đó có quán karaoke nào giá rẻ không?",
     f"Đại Nội mở từ 7 giờ [1].\n{CAU_Y_THIEU} quán karaoke giá rẻ gần Đại Nội Huế.", "gần đó có quán karaoke nào giá rẻ không"),
    (CAU_HAI_Y, TRA_LOI, "dịp Tết năm tới có chương trình gì"),
    ("Chùa Thiên Mụ ở đâu và có chỗ gửi xe máy không?",                                         # tên nơi ở cả hai vế (review B m-1)
     f"Chùa Thiên Mụ nằm trên đồi Hà Khê [1].\n{CAU_Y_THIEU} chỗ gửi xe máy ở chùa Thiên Mụ.", "có chỗ gửi xe máy không"),
    (CAU_HAI_Y, "Vé lẻ người lớn 200.000 đồng [1].", ""),                                    # không có dòng ý thiếu ⇒ cả câu như cũ
    ("Vé vào Đại Nội giá bao nhiêu?", f"{CAU_Y_THIEU} giá vé", ""),                            # một vế ⇒ cả câu
    (CAU_HAI_Y, f"{CAU_Y_THIEU} vé lẻ Đại Nội.\n{CAU_Y_THIEU} chương trình Tết.", ""),         # thiếu cả hai vế ⇒ cả câu
])
def test_web_section_targets_the_missing_clause(cau, tra_loi, ve):
    assert ve_y_thieu(cau, tra_loi) == ve
