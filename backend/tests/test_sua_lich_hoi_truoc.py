"""Công tắc `sua_lich_hoi_truoc` (23/11/2026) — 0 USD, không gọi model. Vì sao: chủ dự án tự test 23/11 và nêu nguyên tắc — lệnh sửa lịch THIẾU thông
tin (ngày nào, buổi nào) thì trợ lý hỏi lại kèm gợi ý và câu "hay để mình tự xếp"; trợ lý chỉ tự làm khi người dùng bảo; không làm được thì không "từ
chối" mà nói tình hình và đưa lối đi. Bật: lệnh "thêm X" thiếu ngày / buổi ⇒ lịch đứng yên + MỘT câu hỏi do code viết + nút (chỗ gợi ý = đúng chỗ bản cũ tự
xếp, các chỗ đặt được khác, "Xếp giúp mình"); lệnh đủ ngày + buổi mà không đụng điểm nào ⇒ làm luôn như cũ; không làm được ⇒ câu thường + nút lối đi; điểm
khu xa ⇒ nói thật + nút mở biểu mẫu. File kiểm phần code trên bảng điểm thật và bộ áp thật; phép đếm cả lưới nằm ở hồ sơ riêng tư của nhánh."""
import copy

from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from llm.assistant import AssistantFlags
from test_sua_lich_v2 import B, _lich

T = B.theo_id
ID = {d["ten"]: d["id"] for d in B.diem}
CU = {"them_khong_the": True, "them_day": True, "them_khu": True, "them_han_che": True}  # các công tắc lệnh thêm đang mở ở main
MOI = {**CU, "them_hoi_truoc": True}


def _them(luu, ten, ngay=None, buoi=None, **kw):
    return s.ap(B, luu, [s.HanhDong(loai="them_diem", ten=ten, ngay=ngay, buoi=buoi)], **kw)


def _mac_dinh():
    return _lich(2, "can_bang", so_thich=())  # lịch mặc định của trang Lên kế hoạch


def _dong(kq):
    (d,) = [x for x in s.thay_doi(B, kq) if not x["duoc"]]
    return d


def test_switch_defaults_off_and_needs_the_no_auto_replace_switch():
    assert AssistantFlags().sua_lich_hoi_truoc is False
    try:
        AssistantFlags(sua_lich_hoi_truoc=True)
    except ValueError as loi:
        assert "sua_lich_hoi_truoc needs" in str(loi)
    else:
        raise AssertionError("công tắc mới phải đòi sua_lich_them_khong_the")


def test_auto_arrange_phrase_is_read_by_code_and_the_button_sentence_carries_it():
    for cau in ("thêm Hổ Quyền, bạn tự xếp giúp mình", "thêm Hổ Quyền, bạn tự xếp đi", "bạn xếp giúp mình nhé", "ngày nào cũng được", "tuỳ bạn chọn",
                "tùy bạn", "bạn chọn giúp mình", "mình để bạn tự sắp xếp", "buổi nào cũng được"):
        assert s.cho_tu_xep(cau), cau
    for cau in ("thêm Hổ Quyền", "thêm Hổ Quyền vào ngày 2", "xếp lại lịch giúp mình", "bạn xếp Hổ Quyền vào sáng ngày 2 nhé", "mình tự đi được không"):
        assert not s.cho_tu_xep(cau), cau
    assert s.cho_tu_xep(f"thêm Hổ Quyền, {s.CAU_TU_XEP}")


def test_add_without_day_and_session_asks_first_and_the_first_button_is_what_the_old_code_picked():
    k, luu = _mac_dinh()
    cu = _them(luu, "Hổ Quyền", **CU)
    (ap_cu,) = cu["da_ap"]  # bản cũ: tự xếp ngay
    kq = _them(luu, "Hổ Quyền", **MOI)
    assert kq["khung"] == k and kq["da_ap"] == [] and kq["the"] is None  # lịch đứng yên
    (m,) = kq["khong_doi"]
    assert m["ma_luat"] == "them_hoi" and m["goi_y"] is True and (m["cho"][0]["ngay"], m["cho"][0]["buoi"]) == (ap_cu["ngay"], ap_cu["buoi"])
    d = _dong(kq)
    assert d["hoi"] is True and d["cau"].startswith("Bạn muốn thêm Hổ Quyền vào ngày nào, buổi nào?") and "Lịch chưa đổi gì." in d["cau"]
    assert "«" not in d["cau"] and "Chưa làm" not in d["cau"] and "mình gợi ý chỗ này" in d["cau"] and s.CAU_TU_XEP in d["cau"]
    nut = d["nut"]
    assert nut[0]["nhan"].endswith("(gợi ý)") and nut[-1] == {"nhan": "Xếp giúp mình", "gui": f"thêm Hổ Quyền, {s.CAU_TU_XEP}"}
    assert len(nut) == len(m["cho"]) + 1 and all(set(n) == {"nhan", "gui"} for n in nut)
    assert [n["gui"] for n in nut[:-1]] == [f"thêm Hổ Quyền vào buổi {s.NHAN_BUOI[g['buoi']]} ngày {g['ngay']}" for g in m["cho"]]
    assert s.cau_goi_y(B, kq) == tuple(n["gui"] for n in nut)  # lượt kế hiểu được lời đáp cụt ("sáng ngày 2", "bạn tự xếp đi")
    # bấm nút gợi ý = lệnh đủ ngày + buổi ⇒ làm luôn, ra ĐÚNG khung bản cũ tự xếp; "Xếp giúp mình" cũng vậy
    g = m["cho"][0]
    assert _them(luu, "Hổ Quyền", g["ngay"], g["buoi"], **MOI)["khung"] == cu["khung"]
    assert _them(luu, "Hổ Quyền", tu_xep=True, **MOI)["khung"] == cu["khung"]
    # mọi nút chỗ khác cũng là lệnh bộ áp nhận, không mất điểm nào của lịch
    for g in m["cho"][1:]:
        sau = _them(luu, "Hổ Quyền", g["ngay"], g["buoi"], **MOI)
        assert [(a["ngay"], a["buoi"], a["the_cho"]) for a in sau["da_ap"]] == [(g["ngay"], g["buoi"], None)] and not v2.kiem_khung_v2(B, sau["khung"])
        assert set(s._vi_tri(k)) < set(s._vi_tri(sau["khung"]))


def test_naming_only_the_day_still_asks_and_offers_only_that_day():
    k, luu = _mac_dinh()
    kq = _them(luu, "Hổ Quyền", ngay=2, **MOI)
    (m,) = kq["khong_doi"]
    assert kq["khung"] == k and m["ma_luat"] == "them_hoi" and m["cho"] and {g["ngay"] for g in m["cho"]} == {2}
    assert _dong(kq)["cau"].startswith("Bạn muốn thêm Hổ Quyền vào buổi nào của ngày 2?")
    mot_buoi = _them(luu, "Hổ Quyền", buoi="sang", **MOI)["khong_doi"]
    assert mot_buoi and mot_buoi[0]["ma_luat"] == "them_hoi" and {g["buoi"] for g in mot_buoi[0]["cho"]} == {"sang"}


def test_switch_off_is_the_old_behaviour_and_a_full_command_is_applied_at_once():
    k, luu = _mac_dinh()
    assert _them(luu, "Hổ Quyền", **CU)["da_ap"] and _them(luu, "Hổ Quyền", them_hoi_truoc=False, **CU) == _them(luu, "Hổ Quyền", **CU)
    cu = _them(luu, "Hổ Quyền", 2, "sang", **CU)
    assert cu["da_ap"] and _them(luu, "Hổ Quyền", 2, "sang", **MOI) == cu  # đủ ngày + buổi, không đụng điểm nào ⇒ y như cũ


def test_every_add_on_the_default_plan_gets_a_question_or_an_honest_line_with_a_way_out():
    k, luu = _mac_dinh()
    trong = set(s._vi_tri(k)) | {j for ng in k["ngay"] for j in ng["buoi"]["toi"]}
    hoi = tu_choi = 0
    for i, d in T.items():
        if i in trong or not set(d["buoi"]) & set(v2.BUOI_NGAY):
            continue
        cu, moi = _them(luu, d["ten"], **CU), _them(luu, d["ten"], **MOI)
        assert moi["khung"] == k and moi["da_ap"] == [] and len(moi["khong_doi"]) == 1, d["ten"]  # thiếu ngày / buổi ⇒ không bao giờ tự làm
        m, dong = moi["khong_doi"][0], _dong(moi)
        assert dong.get("hoi") is True and "«" not in dong["cau"] and not dong["cau"].startswith("Chưa làm"), d["ten"]
        if cu["da_ap"]:  # bản cũ tự xếp được ⇒ nay là câu hỏi; nút đầu ra đúng khung cũ
            hoi += 1
            g = m["cho"][0]
            assert m["ma_luat"] == "them_hoi" and _them(luu, d["ten"], g["ngay"], g["buoi"], **MOI)["khung"] == cu["khung"], d["ten"]
        else:  # bản cũ từ chối ⇒ nay có nút lối đi, hoặc câu nói thật là lịch không còn chỗ
            tu_choi += 1
            assert m["ma_luat"] in ("them_can_thay", "them_bi_chan") and m["hoi_truoc"] is True, d["ten"]
            assert dong.get("nut") or "không còn chỗ nào" in dong["cau"], d["ten"]
    assert hoi >= 10 and tu_choi >= 1  # lịch mặc định: đa số điểm thêm được, vài điểm bị chặn


def test_far_area_place_gets_a_plain_explanation_and_a_button_to_the_form():
    k, luu = _mac_dinh()
    kq = _them(luu, "Vườn quốc gia Bạch Mã", **MOI)
    (m,) = kq["khong_doi"]
    d = _dong(kq)
    assert kq["khung"] == k and m["ma_luat"] == "them_bi_chan" and d["hoi"] is True
    assert d["cau"].startswith("Vườn quốc gia Bạch Mã ở xa trung tâm") and "biểu mẫu Lên kế hoạch" in d["cau"] and "Lịch chưa đổi gì." in d["cau"]
    assert d["nut"] == [{"nhan": "Mở biểu mẫu Lên kế hoạch", "mo": "bieu_mau"}]


def test_a_full_slot_offers_replacement_buttons_that_the_card_path_applies_without_a_model():
    k, luu = _mac_dinh()
    ten_ban_dau = {T[j]["ten"] for j in s._vi_tri(k)}
    for i, d in T.items():  # tìm một lệnh "thêm X vào <buổi> ngày <n>" mà bản cũ chỉ làm được bằng cách thay một điểm
        if i in s._vi_tri(k) or not set(d["buoi"]) & set(v2.BUOI_NGAY):
            continue
        for ng in k["ngay"]:
            for b in v2.BUOI_NGAY:
                kq = _them(luu, d["ten"], ng["ngay"], b, **MOI) if b in d["buoi"] else None
                thay = [n for n in (_dong(kq).get("nut") or []) if "chon" in n] if kq and kq["khong_doi"] else []
                if thay:
                    cau = _dong(kq)["cau"]
                    assert kq["khung"] == k and "«" not in cau and not cau.startswith("Chưa làm") and "Lịch chưa đổi gì." in cau
                    n = thay[0]
                    assert n["nhan"] == n["gui"][0].upper() + n["gui"][1:] and T[n["chon"]["cu"]]["ten"] in ten_ban_dau and n["chon"]["moi"] == i
                    sau = s.ap(B, luu, [], sua_chon=copy.deepcopy(n["chon"]))  # đúng đường thẻ chọn: không gọi model
                    assert i in s._vi_tri(sau["khung"]) and n["chon"]["cu"] not in s._vi_tri(sau["khung"])
                    return
    raise AssertionError("lịch mặc định phải có ít nhất một lệnh thêm cần thay một điểm")
