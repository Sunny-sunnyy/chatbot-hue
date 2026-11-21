"""Cờ `sua_lich_them_khong_the` (21/11/2026) — 0 USD, không gọi model. Vì sao: người dùng mô phỏng (vai sửa lịch, cả hai model) nhờ "thêm X" ⇒ code tự
thế chỗ một điểm đang có ⇒ người dùng xin trả lại ⇒ code thế chỗ điểm kia (5 / 8 lượt sửa lịch của lượt mốc). Cờ bật: lệnh THÊM không bao giờ làm mất
một điểm đang có — lịch giữ nguyên, code nói điểm nào thay được; lệnh thêm bị luật xếp chặn ⇒ lý do + chỗ làm được. File này kiểm phần code trên bảng
điểm thật và bộ áp thật; người dùng thật có nhắn theo câu gợi ý hay không, và lần hiểu ý có hiểu câu đó không, là lượt đo ghi ở report của nhánh."""
import asyncio

import pytest

from llm import len_ke_hoach as lkh
from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from llm.assistant import AnswerTrace, AssistantFlags
from test_cong_dot_1 import flags_from
from test_sua_lich_v2 import B, _lich

NGAY_DIEM = [i for i, d in B.theo_id.items() if set(d["buoi"]) & set(v2.BUOI_NGAY)]


def _them(luu, i, ngay=None, buoi=None, **kw):
    return s.ap(B, luu, [s.HanhDong(loai="them_diem", ten=B.theo_id[i]["ten"], ngay=ngay, buoi=buoi)], **kw)


def _moi_lenh(n=2, so_thich=("di_tich",)):
    """Mọi lệnh "thêm X vào <buổi> ngày <n>" + "thêm X" (không nói chỗ) trên một lịch mẫu."""
    k, luu = _lich(n, so_thich=so_thich)
    vt = s._vi_tri(k)
    for i in NGAY_DIEM:
        if i in vt:
            continue
        yield k, luu, i, None, None
        for ng in range(1, n + 1):
            for b in v2.BUOI_NGAY:
                if b in B.theo_id[i]["buoi"]:
                    yield k, luu, i, ng, b


def test_flag_defaults_off_and_needs_the_edit_flag():
    assert AssistantFlags().sua_lich_them_khong_the is False
    with pytest.raises(ValueError, match="sua_lich_them_khong_the needs"):
        AssistantFlags(sua_lich_them_khong_the=True)


def test_add_never_removes_a_point_and_every_suggestion_really_works():
    """Quét mọi lệnh thêm trên hai lịch mẫu. Cờ tắt: có ca tự thế chỗ (hành vi cũ, để chắc phép quét chạm đúng chỗ). Cờ bật: 0 ca làm mất điểm; ca thêm
    thẳng được thì y như cờ tắt; ca cũ tự thế chỗ ⇒ lịch giữ nguyên + ít nhất một cách; MỌI cách được nêu đều làm được khi áp đúng lệnh đó."""
    n_the = n_them = n_chan = n_cach = 0
    for so_thich in (("di_tich",), ()):
        for k, luu, i, ng, b in _moi_lenh(2, so_thich):
            cu, moi = _them(luu, i, ng, b), _them(luu, i, ng, b, them_khong_the=True)
            the_cu = bool(cu["da_ap"] and cu["da_ap"][0].get("the_cho"))
            if cu["da_ap"] and not the_cu:  # thêm thẳng, không mất gì ⇒ cờ không đổi gì
                n_them += 1
                assert moi == cu
                continue
            assert not moi["da_ap"] and moi["khung"] == k and len(moi["khong_doi"]) == 1  # không áp, lịch giữ nguyên, đúng một dòng
            kd = moi["khong_doi"][0]
            cau = s.thay_doi(B, moi)[0]
            assert cau["duoc"] is False and cau["cau"].startswith(f"Chưa làm: thêm {B.theo_id[i]['ten']}")
            if the_cu:
                n_the += 1
                assert kd["ma_luat"] == "them_can_thay" and 1 <= len(kd["cach"]) <= 2 and all(g["thay"] is not None for g in kd["cach"])
                assert "Muốn đổi, bạn nhắn đủ câu: thay " in cau["cau"]
            else:
                n_chan += 1
                assert kd["ma_luat"] == "them_bi_chan" and len(kd["cach"]) <= 2
                assert ("Làm được, bạn nhắn đủ câu: " in cau["cau"]) == bool(kd["cach"]) and ("không còn chỗ nào" in cau["cau"]) == (not kd["cach"])
            for g in kd["cach"]:  # mỗi cách = một lệnh người dùng nhắn lại ⇒ áp thật phải làm được, và X vào đúng buổi được nêu
                n_cach += 1
                if g["thay"] is None:
                    sau = _them(luu, i, g["ngay"], g["buoi"], them_khong_the=True)
                else:
                    assert B.theo_id[g["thay"]]["ten"] in cau["cau"]
                    sau = s.ap(B, luu, [s.HanhDong(loai="thay_diem", ten=B.theo_id[g["thay"]]["ten"], ten_moi=B.theo_id[i]["ten"])], them_khong_the=True)
                assert sau["da_ap"] and s._vi_tri(sau["khung"])[i] == (g["ngay"], g["buoi"]) and v2.kiem_khung_v2(B, sau["khung"]) == []
                assert not any(a.get("the_cho") for a in sau["da_ap"])
    assert n_the > 50 and n_chan > 50 and n_cach > 50  # phép quét thật sự chạm cả hai nhánh mới


def test_named_slot_line_says_what_is_there_and_who_can_be_swapped():
    """Một ca cụ thể: buổi được nói rõ ⇒ câu nêu buổi đó đang có gì + đúng câu để nhắn."""
    for k, luu, i, ng, b in _moi_lenh(2):
        if ng is None:
            continue
        cu = _them(luu, i, ng, b)
        if cu["da_ap"] and cu["da_ap"][0].get("the_cho"):
            break
    moi = _them(luu, i, ng, b, them_khong_the=True)
    x, cau = B.theo_id[i]["ten"], s.thay_doi(B, moi)[0]["cau"]
    dang_co = [B.theo_id[j]["ten"] for j, v in s._vi_tri(k).items() if v == (ng, b)]
    y = B.theo_id[moi["khong_doi"][0]["cach"][0]["thay"]]["ten"]
    ly_do = moi["khong_doi"][0]["ly_do"]
    vi = f"thêm vào đó thì {s.CAU_LY_DO[ly_do]}" if ly_do else "không xếp thêm được một điểm nữa"
    assert cau.startswith(f"Chưa làm: thêm {x} — buổi {s.NHAN_BUOI[b]} ngày {ng} đang có {' và '.join(dang_co)}; {vi}. Muốn đổi, bạn nhắn đủ câu: thay {y} bằng {x}")
    assert y in dang_co


def test_add_after_a_removal_in_the_same_message_is_judged_on_the_new_itinerary():
    """"Bỏ A, thêm B": lệnh thêm được xét trên lịch SAU khi bỏ — có chỗ thì thêm thật (không dòng "chưa làm"), và A không quay lại."""
    k, luu = _lich(2)
    vt = s._vi_tri(k)
    for a in sorted(vt):
        for i in NGAY_DIEM:
            if i in vt:
                continue
            kq = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten=B.theo_id[a]["ten"]),
                               s.HanhDong(loai="them_diem", ten=B.theo_id[i]["ten"], ngay=vt[a][0], buoi=vt[a][1])], them_khong_the=True)
            if len(kq["da_ap"]) == 2:
                sau = s._vi_tri(kq["khung"])
                assert a not in sau and sau[i] == vt[a] and not kq["khong_doi"] and not kq["da_ap"][1].get("the_cho")
                return
    raise AssertionError("không tìm được ca bỏ rồi thêm thẳng")


def test_replace_blocked_by_the_rules_gives_the_reason_and_ways_that_work():
    """Cùng cờ: lệnh THAY bị luật xếp chặn (người dùng chọn thay một điểm khác điểm được gợi ý). Cờ tắt: câu chung như cũ. Cờ bật: lý do cụ thể hoặc ít nhất
    câu mở đầu "Chưa làm: thay Y bằng X", lịch giữ nguyên, và mọi cách nêu ra đều làm được. Lệnh thay làm được thì hai cờ cho cùng kết quả."""
    k, luu = _lich(2)
    vt = s._vi_tri(k)
    n_chan = n_duoc = 0
    for y in sorted(vt):
        for i in NGAY_DIEM:
            if i in vt or vt[y][1] not in B.theo_id[i]["buoi"]:
                continue
            hd = [s.HanhDong(loai="thay_diem", ten=B.theo_id[y]["ten"], ten_moi=B.theo_id[i]["ten"])]
            cu, moi = s.ap(B, luu, hd), s.ap(B, luu, hd, them_khong_the=True)
            if cu["da_ap"]:
                n_duoc += 1
                assert moi == cu
                continue
            n_chan += 1
            assert cu["khong_doi"][0]["ma_luat"] == "khong_hop_luat" and "phạm luật xếp" in s.thay_doi(B, cu)[0]["cau"]
            kd, cau = moi["khong_doi"][0], s.thay_doi(B, moi)[0]["cau"]
            assert not moi["da_ap"] and moi["khung"] == k and kd["ma_luat"] == "thay_bi_chan"
            assert cau.startswith(f"Chưa làm: thay {B.theo_id[y]['ten']} bằng {B.theo_id[i]['ten']} — vì ")
            for g in kd["cach"]:
                sau = (s.ap(B, luu, [s.HanhDong(loai="them_diem", ten=B.theo_id[i]["ten"], ngay=g["ngay"], buoi=g["buoi"])], them_khong_the=True) if g["thay"] is None
                       else s.ap(B, luu, [s.HanhDong(loai="thay_diem", ten=B.theo_id[g["thay"]]["ten"], ten_moi=B.theo_id[i]["ten"])], them_khong_the=True))
                assert g["thay"] != y and sau["da_ap"] and s._vi_tri(sau["khung"])[i] == (g["ngay"], g["buoi"])
    assert n_chan > 10 and n_duoc > 10


def _chay(ra, flags):
    k, luu = _lich(2)

    class Gen:
        async def hieu_sua(self, prompt, call_log, **kw):
            return list(ra(k))

    tr = AnswerTrace(history=(("Lên kế hoạch tham quan Huế", "(lịch)"),))
    tr.lich_luu, tr.sua_chon = luu, None
    return k, asyncio.run(lkh.hieu_va_ap("Thêm một điểm vào giúp mình", Gen(), tr, flags)), tr


def _co(**kw):
    return flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, sua_lich_v2=True, sua_lich_chua_ho_tro=True, **kw)


def test_turn_level_flag_off_replaces_as_before_and_flag_on_keeps_the_itinerary():
    """Qua `hieu_va_ap` (đường của lượt sửa thật): cờ tắt ⇒ tự thế chỗ như cũ; cờ bật ⇒ vẫn là LƯỢT SỬA, lịch giữ nguyên, một dòng "Chưa làm: thêm …";
    ghép với cờ "tin sửa kèm câu hỏi": dòng câu hỏi vẫn là dòng cuối."""
    k0, luu0 = _lich(2)
    i, ng, b = next((i, ng, b) for _, luu, i, ng, b in _moi_lenh(2) if ng is not None and (_them(luu, i, ng, b)["da_ap"] or [{}])[0].get("the_cho"))

    def ra(k, hoi=False):
        return [s.HanhDongHoi(loai="them_diem", ten=B.theo_id[i]["ten"], ngay=ng, buoi=b)] + ([s.HanhDongHoi(loai="hoi_them")] if hoi else [])

    _, kq_tat, tr_tat = _chay(ra, _co())
    assert kq_tat["da_ap"][0]["the_cho"] and "thế chỗ" in s.thay_doi(B, kq_tat)[0]["cau"] and kq_tat["khung"] != k0
    _, kq, tr = _chay(ra, _co(sua_lich_them_khong_the=True))
    assert kq is not None and kq["khung"] == k0 and not kq["da_ap"] and tr.sua == {"n_hanh_dong": 1, "n_ap": 0, "n_khong": 1, "the": False}
    dong = s.thay_doi(B, kq)
    assert len(dong) == 1 and dong[0]["cau"].startswith("Chưa làm: thêm ") and not any(d["duoc"] for d in dong)
    _, kq2, _ = _chay(lambda k: ra(k, hoi=True), _co(sua_lich_them_khong_the=True, sua_lich_kem_hoi=True))
    dong2 = s.thay_doi(B, kq2)
    assert [d["cau"] for d in dong2] == [dong[0]["cau"], s.CAU_HOI_THEM]
