"""Cờ `web_chi_khi_tu_choi` (21/11/2026) — 0 USD. Vì sao: ở chế độ "trả lời theo ý", lượt đã trả lời được một phần mà còn một dòng "Tư liệu chưa có thông tin
về: …" thì mở mục "Từ web". Đếm trên ba lượt mốc 12 vai: model đang chạy mở mục web ở 64 / 79 lượt nhiều ý, model cũ 44 / 71; trên mẫu 68 dòng dò kho, mục
web đáp đúng điều thiếu ở 1 dòng; lượt có mục web chậm hơn khoảng 4,5–10 giây. Cờ bật: mục web chỉ mở khi CẢ câu trả lời là câu từ chối. Dòng "chưa có"
giữ nguyên. File này kiểm phần code (tìm kho thật, model giả, dịch vụ tìm web giả); thời gian và chất lượng là lượt đo có phí ghi ở report của nhánh."""
import asyncio
import dataclasses

import pytest

from api.routes.chat import _luu_cache
from llm import thoi_tiet as tt
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, luoi_cuoi_bao, so_y_thieu, web_gate_open
from llm.full_corpus_prompt import CAU_Y_THIEU, INSUFFICIENT_ANSWER
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from llm.tra_web import KetQuaWeb
from test_b6_tra_web import BAO_WEB, _nguoi_dung_nhan
from test_cau_nhieu_y import CAU_HAI_Y, TRA_LOI, Client, deps  # noqa: F401  (`deps` = fixture tìm kho thật)

TAT = AssistantFlags(router=True, tim_them=True, tra_web=True, cau_nhieu_y=True)
BAT = dataclasses.replace(TAT, web_chi_khi_tu_choi=True)


def test_flag_defaults_off_and_needs_the_web_flag():
    assert AssistantFlags().web_chi_khi_tu_choi is False
    with pytest.raises(ValueError, match="web_chi_khi_tu_choi needs"):
        AssistantFlags(web_chi_khi_tu_choi=True)


@pytest.mark.parametrize("answer, nhieu_y, mo_tat, mo_bat", [
    (INSUFFICIENT_ANSWER, False, True, True),                      # cả câu là câu từ chối ⇒ mở như cũ, cờ nào cũng vậy (luật gốc)
    (INSUFFICIENT_ANSWER, True, True, True),
    (TRA_LOI, True, True, False),                                  # lượt nhiều ý đã trả lời một phần + dòng "chưa có" ⇒ ĐÚNG chỗ cờ đổi
    (TRA_LOI, False, False, False),                                # câu một ý: dòng "chưa có" không mở cổng (như cũ)
    ("Vé lẻ người lớn 200.000 đồng [1].", True, False, False),     # lượt nhiều ý đủ ý ⇒ không mở (như cũ)
])
def test_gate_changes_only_for_partly_answered_multi_part_turns(answer, nhieu_y, mo_tat, mo_bat):
    def mo(flags):
        return web_gate_open(AnswerTrace(route="tro_ly_hue", answer=answer, nhieu_y=nhieu_y), flags, object())
    assert (mo(TAT), mo(BAT)) == (mo_tat, mo_bat)


def test_missing_line_count_uses_the_same_rule_as_the_gate():
    assert so_y_thieu(TRA_LOI) == 1 and so_y_thieu(INSUFFICIENT_ANSWER) == 0 and so_y_thieu("") == 0
    assert so_y_thieu(f"A [1].\n- {CAU_Y_THIEU} x.\n* {CAU_Y_THIEU} y.\n{CAU_Y_THIEU} z [2].\nCó ghi: {CAU_Y_THIEU} t.") == 2  # dòng có trích dẫn / không ở đầu dòng: không tính


def _chay(deps, flags, cau=CAU_HAI_Y, text=TRA_LOI):
    truy_van = []

    async def tim_web(q):
        truy_van.append(q)
        return KetQuaWeb(trang_thai="rong", so_web=[], ms=1.0, loi=None, usd=0.0)
    client, trace = Client(text), AnswerTrace()
    asyncio.run(answer_turn(cau, *deps, OpenAIFullCorpusGenerator(client=client, model="probe"), trace, flags, tim_web=tim_web))
    return trace, truy_van, client.calls


def test_whole_turn_partly_answered_keeps_the_missing_line_and_skips_the_web_lookup_only_with_the_flag(deps):
    """Qua lõi thật: cùng một lượt nhiều ý trả lời được một phần. Cờ tắt ⇒ tra web một lần (như cũ). Cờ bật ⇒ không tra web, không có mục web, bớt đúng
    phần gọi thêm; chữ trả lời — gồm dòng "Tư liệu chưa có thông tin về…" — y hệt bên tắt, và lời gọi model đầu tiên giống hệt (cờ không đổi thứ gửi model)."""
    t_tat, web_tat, goi_tat = _chay(deps, TAT)
    t_bat, web_bat, goi_bat = _chay(deps, BAT)
    assert len(web_tat) == 1 and t_tat.web is not None
    assert web_bat == [] and t_bat.web is None
    assert t_bat.answer == t_tat.answer and CAU_Y_THIEU in t_bat.answer and so_y_thieu(t_bat.answer) == 1
    assert goi_bat[0]["instructions"] == goi_tat[0]["instructions"] and goi_bat[0]["input"] == goi_tat[0]["input"]
    assert len(goi_bat) <= len(goi_tat)


def test_whole_turn_refused_still_opens_the_web_section_with_the_flag(deps):
    """Bất biến: lượt bị từ chối CẢ câu vẫn tra web như trước khi có cờ."""
    for flags in (TAT, BAT):
        trace, truy_van, _ = _chay(deps, flags, text=INSUFFICIENT_ANSWER)
        assert trace.answer.strip() == INSUFFICIENT_ANSWER and len(truy_van) == 1 and trace.web is not None, flags.web_chi_khi_tu_choi


def test_storm_turn_partly_answered_still_gets_the_official_bulletin_line_and_112_once(deps):
    """Chỗ gặp lưới thiên tai: lượt nhiều ý có từ nguy hiểm thời tiết, trả lời được một phần. Cờ bật thì mục web (chế độ thiên tai) không còn mở —
    người dùng vẫn phải nhận câu bản tin chính thức với hai địa chỉ và số 112 ĐÚNG một lần (lưới cuối của route), ở cả hai bên cờ."""
    cau = "Chiều nay ở Huế có bão không, vé lẻ vào Đại Nội giá bao nhiêu?"
    for flags in (dataclasses.replace(BAO_WEB, cau_nhieu_y=True), dataclasses.replace(BAO_WEB, cau_nhieu_y=True, web_chi_khi_tu_choi=True)):
        trace, truy_van, _ = _chay(deps, flags, cau=cau, text=f"Vé lẻ người lớn 200.000 đồng [1].\n{CAU_Y_THIEU} dự báo bão chiều nay.")
        luoi_cuoi_bao(cau, trace, flags)
        thay = _nguoi_dung_nhan(trace)
        assert thay.count("112") == 1 and tt.NCHMF_URL in thay and tt.LU_QUET_URL in thay, flags.web_chi_khi_tu_choi
        if flags.web_chi_khi_tu_choi:
            assert trace.web is None and truy_van == []


def test_partly_answered_turn_is_still_not_saved_to_the_answer_cache(deps):
    """Bộ nhớ đệm câu trả lời: trước đây lượt có dòng "chưa có" luôn kèm mục web nên không bao giờ được lưu. Cờ bật thì lượt đó không còn mục web ⇒ nơi lưu
    phải tự loại nó; lượt nhiều ý ĐỦ ý vẫn được lưu như trước."""
    class Kho:
        def __init__(self): self.da_luu = []
        def luu(self, cau, ban): self.da_luu.append(cau)

    t_thieu, _, _ = _chay(deps, BAT)
    t_du, _, _ = _chay(deps, BAT, text="Vé lẻ người lớn 200.000 đồng [1].")
    kho = Kho()
    _luu_cache(kho, "câu thiếu ý", t_thieu, {"refusal": False}, True)
    assert kho.da_luu == []
    _luu_cache(kho, "câu đủ ý", t_du, {"refusal": False}, True)
    assert kho.da_luu == ["câu đủ ý"]
