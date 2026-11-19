"""Rào đổi số ngày sau lần hiểu ý sửa lịch (`sua_lich_v2.so_ngay_co_trong_cau`): số trong một ngày tháng không thành số ngày (C 15/11)."""
import pytest

from llm import sua_lich_v2 as sl


@pytest.mark.parametrize("cau, so_ngay, hien_tai, duoc", [
    ("Mình đi từ ngày 20/12 nhé", 1, 3, False),        # lỗi thật 15/11: 20/12 ⇒ "1 ngày"
    ("Đi từ 20/12 nhé", 2, 3, False),
    ("Mình đi từ ngày 20/12 nhé", None, 3, False),     # đổi số ngày không kèm số
    ("Đổi sang ngày 1/1 và cho khách sạn 5 sao", 1, 3, False),
    ("Bỏ đồi Vọng Cảnh, thêm Hổ Quyền, với lại rút xuống 2 ngày thôi.", 2, 3, True),  # Q3 đã thấy S03
    ("Giờ rút xuống còn 2 ngày giúp mình.", 2, 3, True),
    ("Cho mình đi hai ngày thôi", 2, 3, True),
    ("Lịch 4N3Đ nhé", 4, 3, True),
    ("Thêm một ngày nữa", 4, 3, True),                 # tương đối
    ("Thêm một ngày nữa", 1, 3, False),                # "một ngày" sau "thêm" không phải tổng
    ("Bớt 1 ngày", 2, 3, True),
    ("Chiều ngày 2 đổi Đại Nội sang Bảo tàng", 2, 3, False),  # "ngày 2" là ngày thứ mấy, không phải số ngày
    ("Đi từ thứ hai ngày 20/12", 2, 3, False),          # review E m-2: "thứ hai" không phải "hai ngày"
    ("Mình đi thứ ba ngày 18/11", 3, 4, False),
    ("Đi 2 hôm thôi", 2, 3, True),                      # review E m-3
    ("Bỏ ngày cuối đi", 2, 3, True),
    ("Bỏ ngày 3 nhé", 2, 3, True),
    ("Bỏ ngày 2 nhé", 2, 3, False),                     # bỏ ngày giữa không phải bớt ngày cuối
])
def test_day_count_needs_a_number_of_days_in_the_text(cau, so_ngay, hien_tai, duoc):
    assert sl.so_ngay_co_trong_cau(cau, so_ngay, hien_tai) is duoc


def test_filter_keeps_other_actions():
    luu = {"khung": {"tham_so": {"so_ngay": 3}}}
    hd = [sl.HanhDong(loai="doi_so_ngay", so_ngay=1), sl.HanhDong(loai="bo_diem", ten="Đại Nội")]
    giu, bi_chan = sl.loc_hanh_dong(hd, "Bỏ Đại Nội, mình đi từ ngày 20/12", luu)
    assert [h.loai for h in giu] == ["bo_diem"] and bi_chan == 1


def test_blocked_day_count_stays_an_edit_turn_with_not_done_line(monkeypatch):
    """Review E M-1: rào bỏ hết hành động ⇒ vẫn là lượt sửa (lịch không đổi) + dòng "Chưa làm: đổi số ngày", không rơi về đường trả lời thường."""
    import asyncio
    from test_len_ke_hoach_v2 import V2
    from llm import len_ke_hoach as lkh, lich_trinh_v2 as v2
    from llm.assistant import AnswerTrace
    k = v2.xep_v2(V2.bang_lich_v2, v2.ThamSoV2(3, so_thich=("di_tich",)))
    tr = AnswerTrace(); tr.lich_luu = sl.luu_tu_lich(k, None, None); tr.sua_chon = None

    class Gen:
        async def hieu_sua(self, prompt, call_log):
            return [sl.HanhDong(loai="doi_so_ngay", so_ngay=1)]
    kq = asyncio.run(lkh.hieu_va_ap("Mình đi từ ngày 20/12 nhé", Gen(), tr, V2))
    assert kq is not None and kq["khung"]["tham_so"]["so_ngay"] == 3
    assert [d["cau"] for d in sl.thay_doi(V2.bang_lich_v2, kq)] == ["Chưa làm: đổi số ngày — bạn nhắn tiếp nhé."]


# ---------- (C 17/11) ý đổi chỗ ngày khi model ĐÃ nhận câu là câu sửa (tự thử 16/11: "Chưa làm: đổi số ngày" sai việc) ----------

@pytest.mark.parametrize("cau, la", [
    ("Đổi chỗ ngày 1 với ngày 2", True),                     # tự thử 16/11 (A, C, E)
    ("Hoán đổi ngày 2 và ngày 3 giúp mình", True),
    ("Đảo thứ tự hai ngày nhé", True),
    ("Ngày 1 và ngày 3 đổi chỗ cho nhau", True),
    ("Gộp ngày 2 với ngày 3", True),
    ("Đổi chỗ ở sang khách sạn khác ngày 2 và ngày 3", False),  # "chỗ ở" = lưu trú
    ("Đổi ngày đi sang 20/12", False),                       # hành động có sẵn (đổi ngày đi)
    ("Dời Đại Nội từ ngày 1 sang ngày 2", False),            # dời buổi — làm được
    ("Ngày 2 nên ăn gì ở đâu?", False),
])
def test_day_reorder_requests_are_recognised(cau, la):
    assert sl.la_viec_ngay_chua_lam(cau) is la


def _hieu(cau, ra):
    import asyncio
    from test_len_ke_hoach_v2 import V2
    from llm import len_ke_hoach as lkh, lich_trinh_v2 as v2
    from llm.assistant import AnswerTrace
    k = v2.xep_v2(V2.bang_lich_v2, v2.ThamSoV2(3, so_thich=("di_tich",)))
    tr = AnswerTrace(); tr.lich_luu = sl.luu_tu_lich(k, None, None); tr.sua_chon = None

    class Gen:
        async def hieu_sua(self, prompt, call_log):
            return list(ra)
    return k, asyncio.run(lkh.hieu_va_ap(cau, Gen(), tr, V2))


def test_blocked_day_count_on_a_swap_request_says_the_right_thing():
    k, kq = _hieu("Đổi chỗ ngày 1 với ngày 2", [sl.HanhDong(loai="doi_so_ngay")])  # model đoán "đổi số ngày" ⇒ rào chặn
    from test_len_ke_hoach_v2 import V2
    assert kq["khung"] == k and [d["cau"] for d in sl.thay_doi(V2.bang_lich_v2, kq)] == [sl.CAU_VIEC_KHAC]


def test_swap_next_to_a_doable_action_is_reported_not_dropped():
    from test_len_ke_hoach_v2 import V2
    k, kq = _hieu("Đổi chỗ ngày 1 với ngày 2, và đổi sang kiểu đi nhẹ nhàng", [sl.HanhDong(loai="doi_tham_so", kieu_di="nhe_nhang")])
    cau = [d["cau"] for d in sl.thay_doi(V2.bang_lich_v2, kq)]
    assert cau[-1] == sl.CAU_VIEC_KHAC and any(c.startswith("Đã đổi") for c in cau)


def test_model_empty_stays_normal_path():  # lưới ở đường "model trả rỗng" đã thử và bỏ (bộ kề bên E 10 / 20) ⇒ việc của `chua_ho_tro`
    _, kq = _hieu("Đổi chỗ ngày 1 với ngày 2", [])
    assert kq is None


def test_merge_read_as_day_count_change_has_no_contradicting_line():  # review E m-1: "Đã đổi số ngày" + "Chưa làm: gộp…" cùng hiện
    from test_len_ke_hoach_v2 import V2
    _, kq = _hieu("Gộp ngày 2 với ngày 3 cho còn 2 ngày thôi", [sl.HanhDong(loai="doi_so_ngay", so_ngay=2)])  # câu có "2 ngày" ⇒ rào cho qua
    cau = [d["cau"] for d in sl.thay_doi(V2.bang_lich_v2, kq)]
    assert any(c.startswith("Đã đổi số ngày") for c in cau) and sl.CAU_VIEC_KHAC not in cau


# ---------- cờ `sua_lich_chua_ho_tro` (plan 2026-11-17-chua-ho-tro-plan.md): model nhận câu sửa chưa làm được ----------

def _hieu_cht(cau, ra):
    import asyncio
    from test_cong_dot_1 import flags_from
    from llm import len_ke_hoach as lkh, lich_trinh_v2 as v2
    from llm.assistant import AnswerTrace
    f = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, sua_lich_v2=True, sua_lich_chua_ho_tro=True)
    k = v2.xep_v2(f.bang_lich_v2, v2.ThamSoV2(3, so_thich=("di_tich",)))
    tr = AnswerTrace(); tr.lich_luu = sl.luu_tu_lich(k, None, None); tr.sua_chon = None
    goi = []

    class Gen:
        async def hieu_sua(self, prompt, call_log, **kw):
            goi.append(kw)
            return list(ra)
    return f, k, asyncio.run(lkh.hieu_va_ap(cau, Gen(), tr, f)), goi


def test_unsupported_edit_flagged_by_model_keeps_plan_and_says_so():
    f, k, kq, goi = _hieu_cht("Dời cả lịch sớm lên 2 tiếng", [sl.HanhDongCHT(loai="chua_ho_tro")])
    assert goi == [{"chua_ho_tro": True}] and kq is not None and kq["khung"] == k and kq["da_ap"] == []
    assert [d["cau"] for d in sl.thay_doi(f.bang_lich_v2, kq)] == [sl.CAU_CHUA_HO_TRO]


def test_unsupported_swap_uses_the_swap_line():
    f, k, kq, _ = _hieu_cht("Cho ngày 3 lên trước ngày 1", [sl.HanhDongCHT(loai="chua_ho_tro")])
    assert kq["khung"] == k and [d["cau"] for d in sl.thay_doi(f.bang_lich_v2, kq)] == [sl.CAU_CHUA_HO_TRO]
    f, k, kq, _ = _hieu_cht("Đổi chỗ ngày 1 với ngày 2", [sl.HanhDongCHT(loai="chua_ho_tro")])
    assert [d["cau"] for d in sl.thay_doi(f.bang_lich_v2, kq)] == [sl.CAU_VIEC_KHAC]


def test_unsupported_next_to_doable_action_applies_the_doable_one():
    f, k, kq, _ = _hieu_cht("Đi nhẹ nhàng thôi, và nghỉ trưa lâu hơn mỗi ngày",
                            [sl.HanhDongCHT(loai="doi_tham_so", kieu_di="nhe_nhang"), sl.HanhDongCHT(loai="chua_ho_tro")])
    cau = [d["cau"] for d in sl.thay_doi(f.bang_lich_v2, kq)]
    assert any(c.startswith("Đã đổi kiểu đi") for c in cau) and cau[-1] == sl.CAU_CHUA_HO_TRO


def test_plain_question_still_goes_normal_with_flag_on():
    _, _, kq, _ = _hieu_cht("Ngày 2 nên ăn gì ở đâu?", [])
    assert kq is None


def test_flag_off_calls_understanding_exactly_as_before():
    goi = []

    class Gen:
        async def hieu_sua(self, prompt, call_log, **kw):
            goi.append(kw)
            return []
    import asyncio
    from test_len_ke_hoach_v2 import V2
    from llm import len_ke_hoach as lkh, lich_trinh_v2 as v2
    from llm.assistant import AnswerTrace
    tr = AnswerTrace(); tr.lich_luu = sl.luu_tu_lich(v2.xep_v2(V2.bang_lich_v2, v2.ThamSoV2(3, so_thich=("di_tich",))), None, None); tr.sua_chon = None
    assert asyncio.run(lkh.hieu_va_ap("Đổi chỗ ngày 1 với ngày 2", Gen(), tr, V2)) is None and goi == [{}]


def test_flag_off_agent_and_schema_unchanged_flag_on_only_adds_two_lines():
    import difflib
    from openai import AsyncOpenAI
    from llm.full_corpus_prompt import SUA_LICH_LOI_DAN, SUA_LICH_LOI_DAN_CHT
    from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator, SuaLichOutput, SuaLichOutputCHT
    g = OpenAIFullCorpusGenerator(client=AsyncOpenAI(api_key="x", base_url="http://127.0.0.1:9"), model="gpt-6-luna")
    assert g.sua_lich_agent.instructions is SUA_LICH_LOI_DAN and g.sua_lich_agent.output_type is SuaLichOutput
    assert "chua_ho_tro" not in str(SuaLichOutput.model_json_schema()) and "chua_ho_tro" in str(SuaLichOutputCHT.model_json_schema())
    them = [d for d in difflib.ndiff(SUA_LICH_LOI_DAN.splitlines(), SUA_LICH_LOI_DAN_CHT.splitlines()) if d[:1] in "+-"]
    assert len([d for d in them if d[0] == "+"]) == 2 and len([d for d in them if d[0] == "-"]) == 1
    assert g.sua_lich_cht_agent.model_settings.max_tokens == g.sua_lich_agent.model_settings.max_tokens


def test_flag_needs_edit_flag():
    import pytest as _p
    from test_cong_dot_1 import flags_from
    with _p.raises(ValueError):
        flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, sua_lich_v2=False, sua_lich_chua_ho_tro=True)


def test_trace_keeps_what_the_model_returned_before_filtering():  # review E: sổ vết từng chỉ có hành động SAU lọc ([] ở lượt "Chưa làm")
    import asyncio
    from test_cong_dot_1 import flags_from
    from llm import len_ke_hoach as lkh, lich_trinh_v2 as v2
    from llm.assistant import AnswerTrace
    f = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, sua_lich_v2=True, sua_lich_chua_ho_tro=True)
    tr = AnswerTrace(); tr.lich_luu = sl.luu_tu_lich(v2.xep_v2(f.bang_lich_v2, v2.ThamSoV2(3, so_thich=("di_tich",))), None, None); tr.sua_chon = None

    class Gen:
        async def hieu_sua(self, prompt, call_log, **kw):
            return [sl.HanhDongCHT(loai="chua_ho_tro")]
    asyncio.run(lkh.hieu_va_ap("Dời cả lịch sớm lên 2 tiếng", Gen(), tr, f))
    assert tr.vet["sua"]["hanh_dong"] == [] and tr.vet["sua"]["model_ra"] == [{"loai": "chua_ho_tro"}]


# ---------- cờ `sua_lich_doi_cho_code`: model trả "chưa hỗ trợ" cho câu DỜI HAI ĐIỂM (mỗi vế một điểm đang có + một buổi) ⇒ code đọc câu ----------
# Lượt đo cuối 18/11: lớp câu này bị model gắn "chưa hỗ trợ" ổn định dù bước áp làm được. Câu trong test dựng từ TÊN của bảng điểm lúc chạy
# (không chép câu của bộ đo vào file được git theo dõi).

def _lich_3_ngay():
    from test_cong_dot_1 import flags_from
    from llm import lich_trinh_v2 as v2
    f = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, sua_lich_v2=True, sua_lich_chua_ho_tro=True, sua_lich_doi_cho_code=True)
    k = v2.xep_v2(f.bang_lich_v2, v2.ThamSoV2(3, so_thich=("di_tich",)))
    return f, k, sl.luu_tu_lich(k, None, None)


def _hai_diem(bang, khung):
    """Hai điểm ban ngày của lịch ở hai NGÀY khác nhau, cùng buổi sáng, mỗi điểm đứng một mình trong buổi của nó ⇒ đổi chỗ được cho nhau."""
    mot_minh = [(ng["ngay"], ng["buoi"]["sang"][0]) for ng in khung["ngay"] if len(ng["buoi"]["sang"]) == 1]
    (na, a), (nb, b) = mot_minh[0], mot_minh[-1]
    assert na != nb
    return (a, na, bang.theo_id[a]["ten"]), (b, nb, bang.theo_id[b]["ten"])


def test_doi_buoi_tu_cau_doc_dung_hai_ve_va_tu_choi_moi_cau_mo_ho():
    f, k, luu = _lich_3_ngay()
    bang = f.bang_lich_v2
    (a, na, ten_a), (b, nb, ten_b) = _hai_diem(bang, k)
    doc = lambda cau: [(h.loai, h.ten, h.ngay, h.buoi) for h in sl.doi_buoi_tu_cau(bang, luu, cau)]  # noqa: E731
    dung = [("doi_buoi", a, nb, "sang"), ("doi_buoi", b, na, "sang")]
    assert doc(f"Cho {ten_a} lên sáng ngày {nb}, còn {ten_b} để sáng ngày {na} nhé.") == dung
    assert doc(f"{ten_a.upper()} sang buổi sáng ngày {nb}; {ten_b} về buổi sáng ngày {na}") == dung  # hoa / thường, "buổi sáng", dấu chấm phẩy
    # vế sau không nêu ngày ⇒ lấy ngày của vế trước; không vế nào nêu ngày ⇒ để trống (bước áp dùng ngày hiện tại của điểm)
    assert doc(f"Ngày {nb} cho {ten_a} lên buổi sáng, {ten_b} để buổi chiều nhé") == [("doi_buoi", a, nb, "sang"), ("doi_buoi", b, nb, "chieu")]
    assert doc(f"{ten_a} lên buổi chiều, {ten_b} để buổi sáng") == [("doi_buoi", a, None, "chieu"), ("doi_buoi", b, None, "sang")]
    ngoai = next(d["ten"] for d in bang.diem if d["id"] not in sl._vi_tri(k))
    for cau in (
        f"Cho {ten_a} lên sáng ngày {nb}",  # một vế
        f"{ten_a} lên sáng ngày {nb}, {ten_b} để sáng ngày {na}, {ten_a} về chiều",  # ba vế
        f"{ten_a} lên sáng ngày {nb}, {ten_a} để chiều ngày {na}",  # hai vế cùng một điểm
        f"{ten_a} với {ten_b} lên sáng ngày {nb}, còn lại để chiều",  # một vế hai điểm, một vế không điểm
        f"{ten_a} lên sáng ngày {nb}, {ngoai} để sáng ngày {na}",  # điểm không có trong lịch
        f"{ten_a} lên ngày {nb}, {ten_b} để sáng ngày {na}",  # vế thiếu buổi
        f"{ten_a} lên sáng hoặc chiều ngày {nb}, {ten_b} để sáng ngày {na}",  # hai buổi trong một vế
        f"{ten_a} lên tối ngày {nb}, {ten_b} để sáng ngày {na}",  # buổi tối: hành động dời không có
        f"{ten_a} lên sáng ngày 9, {ten_b} để sáng ngày {na}",  # ngày ngoài lịch
        f"Đừng cho {ten_a} lên sáng ngày {nb}, {ten_b} để sáng ngày {na}",  # phủ định
        f"{ten_a} lên sáng ngày {nb}, {ten_b} để sáng ngày {na} được không?",  # câu hỏi, không phải yêu cầu
        f"Bỏ {ten_a} sáng ngày {nb}, {ten_b} để sáng ngày {na}",  # có việc khác (bỏ)
        f"Thay {ten_a} sáng ngày {nb}, thêm {ten_b} sáng ngày {na}",
    ):
        assert doc(cau) == [], cau


def _hieu_doi_cho(cau, ra, **co):
    import asyncio
    from dataclasses import replace
    from llm import len_ke_hoach as lkh
    from llm.assistant import AnswerTrace
    f, k, luu = _lich_3_ngay()
    f = replace(f, **co)
    tr = AnswerTrace(); tr.lich_luu = luu; tr.sua_chon = None

    class Gen:
        async def hieu_sua(self, prompt, call_log, **kw):
            return list(ra)
    return f, k, asyncio.run(lkh.hieu_va_ap(cau, Gen(), tr, f)), tr


def test_model_tra_chua_ho_tro_cho_cau_doi_hai_diem_thi_code_ap_hai_lan_doi_buoi_khi_co_bat():
    f, k, _ = _lich_3_ngay()
    (a, na, ten_a), (b, nb, ten_b) = _hai_diem(f.bang_lich_v2, k)
    cau = f"Cho {ten_a} lên sáng ngày {nb}, còn {ten_b} để sáng ngày {na} nhé."
    cht = [sl.HanhDongCHT(loai="chua_ho_tro")]
    # cờ BẬT: lịch đổi đúng hai điểm, không còn câu "chưa làm"
    f, k, kq, tr = _hieu_doi_cho(cau, cht)
    vt = sl._vi_tri(kq["khung"])
    assert vt[a] == (nb, "sang") and vt[b] == (na, "sang") and kq["chua_lam"] == [] and kq["khong_doi"] == []
    assert {x: v for x, v in vt.items() if x not in (a, b)} == {x: v for x, v in sl._vi_tri(k).items() if x not in (a, b)}  # điểm khác giữ chỗ
    assert tr.vet["sua"]["doc_cau"] is True and tr.vet["sua"]["chua_ho_tro"] == 1
    # cờ TẮT: y như hôm nay — lịch giữ nguyên + câu cố định
    f, k, kq, tr = _hieu_doi_cho(cau, cht, sua_lich_doi_cho_code=False)
    assert kq["khung"] == k and [d["cau"] for d in sl.thay_doi(f.bang_lich_v2, kq)] == [sl.CAU_CHUA_HO_TRO] and tr.vet["sua"]["doc_cau"] is False
    # cờ BẬT nhưng câu không thuộc lớp này ⇒ vẫn câu cố định
    f, k, kq, tr = _hieu_doi_cho("Dời cả lịch sớm lên 2 tiếng", cht)
    assert kq["khung"] == k and [d["cau"] for d in sl.thay_doi(f.bang_lich_v2, kq)] == [sl.CAU_CHUA_HO_TRO]
    # cờ BẬT, model trả "chưa hỗ trợ" KÈM một hành động khác ⇒ code không đọc câu (chỉ áp hành động của model, giữ dòng "chưa làm")
    f, k, kq, tr = _hieu_doi_cho(cau, [sl.HanhDong(loai="bo_diem", ten=a), *cht])
    assert a not in sl._vi_tri(kq["khung"]) and sl._vi_tri(kq["khung"])[b] == sl._vi_tri(k)[b] and kq["chua_lam"] == [sl.CHUA_HO_TRO]
    assert tr.vet["sua"]["doc_cau"] is False


def test_co_doi_cho_code_can_co_chua_ho_tro():
    from test_cong_dot_1 import flags_from
    with pytest.raises(ValueError, match="sua_lich_doi_cho_code"):
        flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, sua_lich_v2=True, sua_lich_chua_ho_tro=False, sua_lich_doi_cho_code=True)

