"""Cờ `sua_lich_kem_hoi` (21/11/2026) — 0 USD. Vì sao: một tin vừa sửa lịch vừa hỏi ("bỏ lăng Đồng Khánh đi. Mà chùa Thiên Mụ có cần mặc kín không?") —
model nhận ra ý sửa ⇒ cả lượt thành lượt sửa, phần hỏi bị bỏ không một lời (người dùng mô phỏng 21/11: 4 / 4 lượt, cả hai model). Cờ bật: lần hiểu ý có
thêm hành động `hoi_them`; CODE thêm một dòng cố định vào khối thay đổi. File này kiểm phần code (bảng điểm thật, bộ áp thật); model có trả `hoi_them`
đúng lúc hay không là lượt đo có phí ghi ở report của nhánh."""
import asyncio

import pytest

from llm import full_corpus_prompt as p
from llm import len_ke_hoach as lkh
from llm import sua_lich_v2 as s
from llm.assistant import AnswerTrace, AssistantFlags
from llm.generator_openai_full_corpus import (MAX_HANH_DONG, GenerationError, OpenAIFullCorpusGenerator, SuaLichOutputCHT, SuaLichOutputHoi, SuaLichOutputToi,
                                              SuaLichOutputToiHoi)
from test_cong_dot_1 import flags_from
from test_sua_lich_v2 import B, _lich


def _co(**kw):
    return flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, sua_lich_v2=True, sua_lich_chua_ho_tro=True, **kw)


def _chay(ra, flags, cau="Bỏ một điểm đi. Mà vé vào cửa bao nhiêu?"):
    """Chạy `hieu_va_ap` thật trên một lịch 3 ngày thật; chỉ lần gọi model là đồ giả trả `ra` — ghi lại tham số nơi gọi truyền."""
    k, luu = _lich()
    goi = []

    class Gen:
        async def hieu_sua(self, prompt, call_log, **kw):
            goi.append(kw)
            return list(ra(k) if callable(ra) else ra)

    tr = AnswerTrace(history=(("Lên kế hoạch tham quan Huế", "(lịch)"),))
    tr.lich_luu, tr.sua_chon = luu, None
    return k, asyncio.run(lkh.hieu_va_ap(cau, Gen(), tr, flags)), tr, goi


def _bo(k):
    return s.HanhDongHoi(loai="bo_diem", ten=B.theo_id[sorted(s._vi_tri(k))[0]]["ten"])


def test_flag_defaults_off_and_needs_the_unsupported_action_flag():
    assert AssistantFlags().sua_lich_kem_hoi is False
    with pytest.raises(ValueError, match="sua_lich_kem_hoi needs"):
        AssistantFlags(sua_lich_kem_hoi=True)


def test_only_the_new_schemas_and_prompts_know_the_extra_question_action():
    """Cờ tắt ⇒ khuôn và lời dặn cũ không có `hoi_them`; bản mới = bản cũ + ĐÚNG một gạch, và danh sách dài hơn đúng một phần tử."""
    for cu, moi in ((SuaLichOutputCHT, SuaLichOutputHoi), (SuaLichOutputToi, SuaLichOutputToiHoi)):
        assert "hoi_them" not in repr(cu.model_json_schema()) and "hoi_them" in repr(moi.model_json_schema())
        assert moi.model_json_schema()["properties"]["hanh_dong"]["maxItems"] == cu.model_json_schema()["properties"]["hanh_dong"]["maxItems"] + 1 == MAX_HANH_DONG + 1
    for cu, moi in ((p.SUA_LICH_LOI_DAN_CHT, p.SUA_LICH_LOI_DAN_CHT_HOI), (p.SUA_LICH_LOI_DAN_TOI, p.SUA_LICH_LOI_DAN_TOI_HOI)):
        assert "hoi_them" not in cu and moi.replace(p._GACH_HOI_THEM, "") == cu and moi.count(p._GACH_HOI_THEM) == 1
    with pytest.raises(Exception):
        s.HanhDongCHT(loai="hoi_them")
    with pytest.raises(Exception):
        s.HanhDongToi(loai="hoi_them")
    assert s.HanhDongToiHoi(loai="doi_buoi", ten="x", buoi="toi").buoi == "toi"  # bản ghép hai cờ giữ buổi tối


def test_edit_plus_question_applies_the_edit_and_adds_one_fixed_line():
    f = _co(sua_lich_kem_hoi=True)
    k, kq, tr, goi = _chay(lambda k: [_bo(k), s.HanhDongHoi(loai="hoi_them")], f)
    assert goi == [{"chua_ho_tro": True, "kem_hoi": True}]
    assert kq is not None and len(kq["da_ap"]) == 1 and kq["khung"] != k and kq["chua_lam"] == []  # ý sửa được áp như thường; `hoi_them` không vào "chưa làm"
    dong = s.thay_doi(B, kq)
    assert dong[-1] == {"cau": s.CAU_HOI_THEM, "duoc": False} and [d["duoc"] for d in dong[:-1]] == [True]
    assert s.CAU_HOI_THEM.startswith("Chưa làm: ")  # giao diện: dòng không `duoc` mà không bắt đầu bằng "Chưa làm" bị gắn tiền tố "Không đổi được"
    assert tr.sua == {"n_hanh_dong": 1, "n_ap": 1, "n_khong": 0, "the": False, "hoi_them": True}  # số đo: đếm được lượt sửa có kèm câu hỏi, không chữ
    assert tr.vet["sua"]["hoi_them"] is True and all(h["loai"] != "hoi_them" for h in tr.vet["sua"]["hanh_dong"])


def test_question_only_message_still_goes_to_the_normal_path():
    """Bất biến: tin KHÔNG có ý sửa không bao giờ thành lượt sửa — kể cả khi model trả `hoi_them` một mình."""
    f = _co(sua_lich_kem_hoi=True)
    for ra in ([s.HanhDongHoi(loai="hoi_them")], []):
        _, kq, tr, _ = _chay(ra, f, cau="Chùa Thiên Mụ có cần mặc kín không?")
        assert kq is None and tr.sua == {"n_hanh_dong": 0}


def test_edit_without_question_is_exactly_as_before():
    """Bất biến: cùng hành động sửa, cờ bật mà không có `hoi_them` ⇒ kết quả áp, khối thay đổi và số đo y như cờ tắt."""
    k, kq_bat, tr_bat, _ = _chay(lambda k: [_bo(k)], _co(sua_lich_kem_hoi=True))
    _, kq_tat, tr_tat, goi = _chay(lambda k: [s.HanhDongCHT(loai="bo_diem", ten=_bo(k).ten)], _co())
    assert goi == [{"chua_ho_tro": True}]  # cờ tắt ⇒ nơi gọi không truyền `kem_hoi` ⇒ agent và chuỗi gửi model như cũ
    assert kq_bat == kq_tat and s.thay_doi(B, kq_bat) == s.thay_doi(B, kq_tat) and tr_bat.sua == tr_tat.sua
    assert "hoi_them" not in kq_tat and "hoi_them" not in tr_tat.vet["sua"]


def test_unsupported_edit_plus_question_keeps_both_lines():
    """Ý sửa chưa làm được + câu hỏi ⇒ vẫn là lượt sửa: câu "chưa hỗ trợ" cũ + dòng câu hỏi; lịch giữ nguyên."""
    k, kq, _, _ = _chay([s.HanhDongHoi(loai="chua_ho_tro"), s.HanhDongHoi(loai="hoi_them")], _co(sua_lich_kem_hoi=True), cau="Dời cả lịch sớm 2 tiếng. Vé bao nhiêu?")
    assert kq["khung"] == k and [d["cau"] for d in s.thay_doi(B, kq)] == [s.CAU_CHUA_HO_TRO, s.CAU_HOI_THEM]


def test_generator_keeps_the_cap_on_edit_actions_and_picks_the_right_agent():
    """`hieu_sua` thật với `_run` giả: khuôn mới dài hơn một phần tử nhưng số hành động SỬA vẫn ≤ MAX_HANH_DONG; chọn đúng agent theo ba tham số."""
    g = object.__new__(OpenAIFullCorpusGenerator)
    g.sua_lich_timeout = 1
    for ten in ("sua_lich_agent", "sua_lich_cht_agent", "sua_lich_toi_agent", "sua_lich_hoi_agent", "sua_lich_toi_hoi_agent"):
        setattr(g, ten, ten)
    da_goi = []

    def gia(ra):
        async def _run(agent, prompt, call_log, timeout):
            da_goi.append(agent)
            return type("R", (), {"final_output": {"hanh_dong": ra}})()
        g._run = _run

    bo = {"loai": "bo_diem", "ten": "x"}
    gia([bo, bo, bo, {"loai": "hoi_them"}])
    ra = asyncio.run(g.hieu_sua("p", None, chua_ho_tro=True, kem_hoi=True))
    assert [h.loai for h in ra] == ["bo_diem"] * 3 + ["hoi_them"]
    gia([bo, bo, bo, bo])
    with pytest.raises(GenerationError):
        asyncio.run(g.hieu_sua("p", None, chua_ho_tro=True, kem_hoi=True))
    gia([bo, {"loai": "hoi_them"}])
    with pytest.raises(GenerationError):  # khuôn cũ không nhận `hoi_them`
        asyncio.run(g.hieu_sua("p", None, chua_ho_tro=True))
    gia([bo])
    for kw in ({}, {"chua_ho_tro": True}, {"chua_ho_tro": True, "buoi_toi": True}, {"chua_ho_tro": True, "kem_hoi": True},
               {"chua_ho_tro": True, "buoi_toi": True, "kem_hoi": True}, {"kem_hoi": True}):
        asyncio.run(g.hieu_sua("p", None, **kw))
    assert da_goi[-6:] == ["sua_lich_agent", "sua_lich_cht_agent", "sua_lich_toi_agent", "sua_lich_hoi_agent", "sua_lich_toi_hoi_agent", "sua_lich_agent"]
