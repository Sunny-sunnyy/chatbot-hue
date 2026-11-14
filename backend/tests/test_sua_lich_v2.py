"""Sửa lịch bằng lời trên lịch bản 2 (plan `docs/superpowers/plans/2026-11-14-sua-lich-v2-plan.md`) — phần code (0 USD): bộ xếp giữ chỗ / loại điểm,
áp hành động, khối "Đã đổi / Không đổi được", từ dò câu sửa, trạng thái lưu. Phép thử mọi tổ hợp ở `data/len_ke_hoach_v2_2026-11-13/tools/do_sua_lich_v2.py`."""
import datetime as dt

from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from llm.assistant import AssistantFlags
from test_cong_dot_1 import flags_from

V2 = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True)
B = V2.bang_lich_v2


def _lich(n=3, kieu="can_bang", so_thich=("di_tich",), ngay=None):
    k = v2.xep_v2(B, v2.ThamSoV2(n, kieu_di=kieu, so_thich=so_thich), ngay_bat_dau=ngay)
    return k, s.luu_tu_lich(k, None if ngay is None else ngay.isoformat(), None)


def test_default_scheduler_unchanged_and_keep_exclude_work():
    k, _ = _lich()
    assert v2.xep_v2(B, v2.ThamSoV2(3, kieu_di="can_bang", so_thich=("di_tich",)), giu=None, loai=frozenset()) == k
    vt = s._vi_tri(k)
    x = sorted(vt)[0]
    k2 = v2.xep_v2(B, v2.ThamSoV2(3, kieu_di="can_bang", so_thich=("di_tich",)), giu={j: v for j, v in vt.items() if j != x}, loai=frozenset({x}))
    tat = {j for ng in k2["ngay"] for b in v2.BUOI for j in ng["buoi"][b]}
    assert x not in tat and all(s._vi_tri(k2)[j] == v for j, v in vt.items() if j != x) and v2.kiem_khung_v2(B, k2) == []


def test_remove_replace_move_and_card():
    k, luu = _lich()
    vt = s._vi_tri(k)
    x = sorted(vt)[0]
    kq = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten=B.theo_id[x]["ten"])])
    assert kq["da_ap"] == [{"loai": "bo_diem", "diem": x}] and x in kq["luu"]["loai"] and v2.kiem_khung_v2(B, kq["khung"]) == []
    assert s.thay_doi(B, kq)[0] == {"cau": f"Đã bỏ {B.theo_id[x]['ten']}.", "duoc": True}
    the = s.ap(B, luu, [s.HanhDong(loai="thay_diem", ten=x)])  # không nói thay bằng gì ⇒ thẻ, khung không đổi
    assert the["the"]["cu"] == x and the["khung"] == k and the["the"]["lua_chon"][-1]["gia_tri"] == "bo"
    moi = the["the"]["lua_chon"][0]["gia_tri"]
    bam = s.ap(B, luu, [], sua_chon={"cu": x, "moi": moi})  # bấm nút ⇒ đúng điểm đã chọn vào đúng chỗ cũ
    assert s._vi_tri(bam["khung"])[moi] == vt[x] and x in bam["luu"]["loai"]
    dich = "chieu" if vt[x][1] == "sang" else "sang"
    dd = s.ap(B, luu, [s.HanhDong(loai="doi_buoi", ten=x, buoi=dich)])
    assert (dd["da_ap"] and s._vi_tri(dd["khung"])[x][1] == dich) or dd["khong_doi"]


def test_unknown_names_and_limits_are_reported_not_guessed():
    k, luu = _lich()
    kq = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten="Tháp Eiffel"), s.HanhDong(loai="them_diem", ten="x"), s.HanhDong(loai="doi_so_ngay", so_ngay=2)])
    assert kq["khong_doi"][0]["ma_luat"] == "ngoai_bang" and kq["chua_lam"] == ["doi_so_ngay"] and kq["khung"] == k
    dong = s.thay_doi(B, kq)
    assert all(not d["duoc"] for d in dong) and dong[-1]["cau"].startswith("Chưa làm")


def test_change_days_keeps_points_that_still_fit():
    k, luu = _lich(n=3)
    kq = s.ap(B, luu, [s.HanhDong(loai="doi_so_ngay", so_ngay=2)])
    assert len(kq["khung"]["ngay"]) == 2 and kq["doi_truong"] == [("so_ngay", 3, 2)]
    giu = {j: v for j, v in s._vi_tri(k).items() if v[0] <= 2}
    assert all(s._vi_tri(kq["khung"]).get(j) == v for j, v in giu.items()) or v2.kiem_khung_v2(B, kq["khung"]) == []


def test_intent_message_and_name_matching():
    k, luu = _lich(n=1)
    tin = s.tin_nhan_hieu(B, luu, "  bỏ điểm đầu  ")
    assert tin.endswith("Câu người dùng: bỏ điểm đầu") and "Ngày 1" in tin
    assert s.khop_ten(B, "Đại Nội Huế") == "dai_noi" and s.khop_ten(B, "đại nội") == "dai_noi" and s.khop_ten(B, "Đại") is None
    assert s.khop_ten(B, "Quốc Học") == "quoc_hoc" and s.khop_ten(B, "Lăng") is None  # tên ngắn chỉ nhận khi nằm trong đúng một điểm
    assert "Điểm khác có thể thêm" in tin


def test_flag_needs_v2():
    import pytest
    with pytest.raises(ValueError):
        AssistantFlags(sua_lich_v2=True)


def test_card_turn_applies_nothing_else_and_lists_the_rest_as_not_done():
    """Review E M-1: lượt có "thay" không nói điểm ⇒ chỉ thẻ chọn; hành động khác (trước hay sau) vào "Chưa làm", khung không đổi, không báo "Đã"."""
    k, luu = _lich()
    a, b = sorted(s._vi_tri(k))[:2]
    for thu_tu in ([s.HanhDong(loai="bo_diem", ten=a), s.HanhDong(loai="thay_diem", ten=b)],
                   [s.HanhDong(loai="thay_diem", ten=b), s.HanhDong(loai="bo_diem", ten=a)]):
        kq = s.ap(B, luu, thu_tu)
        assert kq["the"]["cu"] == b and kq["da_ap"] == [] and kq["chua_lam"] == ["bo_diem"] and kq["khung"] == k
        assert not any(d["duoc"] for d in s.thay_doi(B, kq)) and any(d["cau"].startswith("Chưa làm") for d in s.thay_doi(B, kq))


def test_parallel_normal_path_waits_for_intent_before_web_and_emergency_wins(monkeypatch):
    """Review E m-1 / B-1 trên đường song song (`assistant._sua_song_song`): đường thường chạy ngay nhưng tra web CHỜ kết quả hiểu ý — lượt sửa
    ⇒ không gọi tra web (chữ người dùng không ra Serper); lượt thường ⇒ có; định tuyến của đường thường thấy khẩn cấp ⇒ không thành lượt sửa."""
    import asyncio
    import dataclasses
    from llm import assistant as a, len_ke_hoach as lkh
    goi_web = []

    def lam(hieu_ra, khan_cap=False):
        async def core(query, rs, cb, gen, tr, flags, recorder, tim_web):
            tr.routing_ms, tr.emergency_by = 1.0, ("router" if khan_cap else None)
            yield "status", {"stage": "routing"}
            if tim_web is not None:
                await tim_web(query)
            yield "delta", "trả lời thường"

        async def hieu(query, gen, tr, flags):
            await asyncio.sleep(0.05)
            return hieu_ra

        async def sua(query, rs, cb, gen, tr, flags, kq):
            yield "lich_khung", {"sua": True}

        async def web(cau):
            goi_web.append(cau)

        monkeypatch.setattr(a, "_answer_core", core)
        monkeypatch.setattr(lkh, "hieu_va_ap", hieu)
        monkeypatch.setattr(lkh, "stream_sua", sua)
        tr = a.AnswerTrace(); tr.lich_luu = {"x": 1}
        fl = dataclasses.replace(V2, router=True)

        async def chay():
            return [e async for e in a._sua_song_song("q", None, None, object(), tr, fl, None, web)]
        return asyncio.run(chay())

    ev = lam({"the": None})  # lượt sửa
    assert ev[-1][0] == "lich_khung" and goi_web == []
    ev = lam(None)  # câu thường
    assert ("delta", "trả lời thường") in ev and goi_web == ["q"]
    goi_web.clear()
    ev = lam({"the": None}, khan_cap=True)  # câu trộn khẩn cấp
    assert ("delta", "trả lời thường") in ev and not any(e[0] == "lich_khung" for e in ev)
