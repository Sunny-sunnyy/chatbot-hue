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
    # lượt thật của phiên đo 23/11/2026: gõ tay đúng chữ trên nút và các lời cho phép không có chủ ngữ "bạn" từng bị hỏi lại
    for cau in ("Xếp giúp mình", "xếp giúp mình đi", "tự xếp đi", "tự chọn giúp mình", "bạn chọn đi", "bạn quyết đi", "hôm nào cũng được",
                "thêm Đàn Nam Giao, hôm nào cũng được", "sáng hay chiều đều được", "sao cũng được", "để bạn xếp"):
        assert s.cho_tu_xep(cau), cau
    for cau in ("thêm Hổ Quyền", "thêm Hổ Quyền vào ngày 2", "xếp lại lịch giúp mình", "bạn xếp Hổ Quyền vào sáng ngày 2 nhé", "mình tự đi được không",
                "bạn đừng tự xếp", "mình không muốn bạn tự xếp", "để mình tự chọn ngày sau"):  # phủ định / người dùng tự chọn ⇒ không phải lời cho phép
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
    assert "«" not in d["cau"] and "Chưa làm" not in d["cau"] and f"Mình gợi ý buổi {s.NHAN_BUOI[ap_cu['buoi']]} ngày {ap_cu['ngay']}." in d["cau"] and s.CAU_TU_XEP in d["cau"]
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


def _hieu(cau, ten, **cong_tac):
    """Chạy `len_ke_hoach.hieu_va_ap` THẬT trên lịch mặc định; chỉ lần gọi model là đồ giả trả đúng một hành động `them_diem` không ngày, không buổi
    (thứ model thật trả cho câu "thêm X") — tức đường người dùng đi: câu gõ ⇒ hiểu ý ⇒ bộ áp ⇒ khối thay đổi + câu nhớ cho lượt kế."""
    import asyncio

    from llm import len_ke_hoach as lkh
    from llm.assistant import AnswerTrace
    from test_cong_dot_1 import flags_from

    k, luu = _mac_dinh()

    class Gen:
        async def hieu_sua(self, prompt, call_log, **kw):
            return [s.HanhDong(loai="them_diem", ten=ten)]

    tr = AnswerTrace(history=(("Lên kế hoạch tham quan Huế", "(lịch)"),))
    tr.lich_luu, tr.sua_chon = luu, None
    flags = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, sua_lich_v2=True, sua_lich_chua_ho_tro=True, sua_lich_them_khong_the=True,
                       sua_lich_them_day=True, sua_lich_them_khu=True, sua_lich_them_han_che=True, **cong_tac)
    return k, asyncio.run(lkh.hieu_va_ap(cau, Gen(), tr, flags)), tr


def test_typed_command_goes_through_the_understanding_step_and_the_next_turn_remembers_the_button_sentences():
    """Đường người dùng đi (route ⇒ `hieu_va_ap`): công tắc bật — câu "thêm X" ra dòng hỏi + các câu nút được nhớ cho lượt kế; câu có lời cho tự xếp
    ("…, bạn tự xếp giúp mình" — chính câu nút "Xếp giúp mình" gửi) thì áp như bản cũ. Công tắc tắt — bộ áp không nhận tham số mới, kết quả y như cũ."""
    k, cu, tr_cu = _hieu("thêm Hổ Quyền", "Hổ Quyền")
    assert cu["da_ap"] and tr_cu.goi_y_moi == ()  # công tắc tắt: tự xếp ngay, không có câu nào để nhớ
    k, kq, tr = _hieu("thêm Hổ Quyền", "Hổ Quyền", sua_lich_hoi_truoc=True)
    assert kq["khung"] == k and kq["da_ap"] == [] and [m["ma_luat"] for m in kq["khong_doi"]] == ["them_hoi"]
    nut = _dong(kq)["nut"]
    assert tr.goi_y_moi == tuple(n["gui"] for n in nut) and tr.goi_y_moi[-1] == f"thêm Hổ Quyền, {s.CAU_TU_XEP}"
    assert tr.sua_dong == (_dong(kq)["cau"],) and tr.sua["n_ap"] == 0 and tr.sua["n_khong"] == 1  # ô lịch sử mang câu hỏi; lượt không áp gì
    k, tu, _ = _hieu(nut[-1]["gui"], "Hổ Quyền", sua_lich_hoi_truoc=True)  # bấm "Xếp giúp mình": câu nút đi qua đúng đường này
    assert tu["khung"] == cu["khung"] and tu["khong_doi"] == []


def _bo(luu, ten, **kw):
    return s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten=ten)], **kw)


def test_removing_the_only_place_of_a_session_leaves_it_empty_and_offers_one_suggestion_button():
    """Chủ dự án chọn 23/11/2026 (sau khi tự test: "Đã bỏ Lăng Tự Đức thì trợ lý lại tự động thêm lăng Dục Đức?"): lệnh BỎ chỉ bỏ đúng điểm đó — buổi
    vừa trống KHÔNG tự lấp, kể cả ở các lượt sửa sau; điểm bản cũ tự lấp thành MỘT nút "Gợi ý điểm thay"; không bấm thì buổi đó cứ trống. Buổi còn điểm
    khác (bản cũ vốn không lấp) và công tắc tắt ⇒ y như cũ."""
    k, luu = _mac_dinh()
    vt = s._vi_tri(k)
    co_nut = 0
    for i, (ngay, buoi) in vt.items():
        ten = T[i]["ten"]
        cu, moi = _bo(luu, ten, **CU), _bo(luu, ten, **MOI)
        assert _bo(luu, ten, them_hoi_truoc=False, **CU) == cu
        if list(vt.values()).count((ngay, buoi)) > 1:  # buổi còn điểm khác: không có gì để lấp ⇒ không đổi
            assert moi == cu, ten
            continue
        (a,), sau, dong = moi["da_ap"], moi["khung"], s.thay_doi(B, moi)
        assert a["trong"] == [ngay, buoi] and sau["buoi_trong"] == [[ngay, buoi]] and not v2.kiem_khung_v2(B, sau), ten
        assert set(s._vi_tri(sau)) == set(vt) - {i}, ten  # không điểm ban ngày nào tự vào lịch
        assert dong[0]["duoc"] and dong[0]["cau"].startswith(f"Đã bỏ {ten}. Buổi {s.NHAN_BUOI[buoi]} ngày {ngay} nay để trống."), ten
        assert s.ap(B, luu, [], sua_chon={"cu": i, "moi": "bo"}, them_hoi_truoc=True)["khung"] == sau, ten  # nút "Bỏ điểm này" của thẻ chọn: cùng kết quả
        lap = [x["diem"] for x in cu["da_ap"][0].get("lap", ()) if (x["ngay"], x["buoi"]) == (ngay, buoi)]
        if not lap:  # bản cũ cũng không lấp được gì ⇒ không có gợi ý, không có nút
            assert len(dong) == 1 and "goi_y_thay" not in a and s.cau_goi_y(B, moi) == (), ten
            continue
        co_nut += 1
        goi = T[lap[0]]["ten"]
        cau = f"thêm {goi} vào buổi {s.NHAN_BUOI[buoi]} ngày {ngay}"
        assert a["goi_y_thay"] == lap[0] and dong[1]["hoi"] is True and dong[1]["duoc"] is False and len(dong) == 2, ten
        assert dong[1]["nut"] == [{"nhan": f"Gợi ý điểm thay: {goi}", "gui": cau}] and goi in dong[1]["cau"] and "cứ để trống" in dong[1]["cau"], ten
        assert s.cau_goi_y(B, moi) == (cau,), ten  # lời đáp cụt ("ừ thêm đi") ở lượt kế hiểu được
        # bấm nút = lệnh đủ ngày + buổi ⇒ điểm gợi ý vào đúng buổi đó, dấu "để trống" tự gỡ
        bam = _them(moi["luu"], goi, ngay, buoi, **MOI)
        assert s._vi_tri(bam["khung"])[lap[0]] == (ngay, buoi) and "buoi_trong" not in bam["khung"] and not v2.kiem_khung_v2(B, bam["khung"]), ten
        # KHÔNG bấm: một lượt sửa khác (bỏ thêm một điểm ở buổi khác) không làm bộ xếp lấp lại buổi đã để trống
        khac = next(j for j, v in s._vi_tri(sau).items() if v != (ngay, buoi))
        sau2 = _bo(moi["luu"], T[khac]["ten"], **MOI)["khung"]
        assert not next(x for x in sau2["ngay"] if x["ngay"] == ngay)["buoi"][buoi] and [ngay, buoi] in sau2["buoi_trong"], ten
        # đổi chỗ hai ngày: buổi để trống đi theo nội dung của ngày
        doi = s.doi_cho_ngay(B, moi["luu"], 1, 2)
        if doi["da_ap"]:
            assert doi["khung"]["buoi_trong"] == [[3 - ngay, buoi]], ten
    assert co_nut >= 1


def test_a_turn_that_also_applied_something_does_not_end_the_question_with_nothing_changed():
    """Lượt thật 23/11/2026: tin vừa bỏ vừa thêm ⇒ thẻ in "Đã bỏ X." rồi câu hỏi kết "Lịch chưa đổi gì." (sai). Lượt có ý đã áp ⇒ câu hỏi bỏ câu kết đó."""
    k, luu = _mac_dinh()
    bo = T[next(iter(s._vi_tri(k)))]["ten"]
    kq = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten=bo), s.HanhDong(loai="them_diem", ten="Hổ Quyền")], **MOI)
    dong = s.thay_doi(B, kq)
    hoi = next(d for d in dong if d.get("nut") and d["cau"].startswith("Bạn muốn thêm Hổ Quyền"))
    assert dong[0]["cau"].startswith(f"Đã bỏ {bo}.") and "Lịch chưa đổi gì." not in hoi["cau"]
    assert "Lịch chưa đổi gì." in _dong(_them(luu, "Hổ Quyền", **MOI))["cau"]  # lượt chỉ có câu hỏi: giữ câu kết


def test_removing_the_last_place_of_a_day_removes_it_and_leaves_the_daytime_of_that_day_empty():
    """Chủ dự án 07:2x 24/11/2026: "khi người dùng đã nhắn bỏ địa điểm thì bỏ luôn… không cần hỏi lại xác nhận… để trống khung giờ đã bỏ". Trước đó (23/11)
    điểm ban ngày CUỐI CÙNG của một ngày không được bỏ (luật "ngày không được rỗng": câu tình hình + nút thay / rút ngày); bản cũ hơn thì tự lấp điểm khác
    (ca dò của phiên đo: «bỏ <điểm sáng ngày 1>» rồi «bỏ <điểm chiều ngày 1>»). Nay: bỏ ngay, ban ngày của ngày đó trống, hoạt động tối và mọi ngày khác
    y như đang có, không rút ngày, MỘT nút gợi ý điểm thay; thêm lại vào ngày đó chạy bình thường. Công tắc tắt ⇒ đường cũ (tự lấp)."""
    k, luu = _mac_dinh()
    (sang,), (chieu,) = k["ngay"][0]["buoi"]["sang"], k["ngay"][0]["buoi"]["chieu"]
    k1 = _bo(luu, T[sang]["ten"], **MOI)
    assert k1["da_ap"] and k1["khung"]["buoi_trong"] == [[1, "sang"]]
    k2 = _bo(k1["luu"], T[chieu]["ten"], **MOI)
    (a,), sau = k2["da_ap"], k2["khung"]
    assert k2["khong_doi"] == [] and all(sau["ngay"][0]["buoi"][b] == [] for b in v2.BUOI_NGAY) and sau["buoi_trong"] == [[1, "chieu"], [1, "sang"]]
    assert sau["ngay"][0]["buoi"]["toi"] == k["ngay"][0]["buoi"]["toi"] and sau["ngay"][1:] == k["ngay"][1:]  # tối ngày 1 + cả ngày 2 y như lịch gốc
    assert sau["tham_so"]["so_ngay"] == 2 and not v2.kiem_khung_v2(B, sau) and a["ngay_trong"] == 1 and a["trong"] == [1, "chieu"]
    dong = s.thay_doi(B, k2)
    assert dong[0]["duoc"] and dong[0]["cau"] == (f"Đã bỏ {T[chieu]['ten']}. Ban ngày của ngày 1 nay không còn điểm nào; buổi tối của ngày 1 và các điểm "
                                               "của những ngày khác giữ nguyên.")
    # dấu chỉ sinh khi người dùng tự bỏ: thiếu dấu của một trong hai buổi ⇒ luật "ngày không được rỗng" vẫn bắt
    assert "ngay_rong" in v2.kiem_khung_v2(B, {**sau, "buoi_trong": [[1, "sang"]]}) and "ngay_rong" in v2.kiem_khung_v2(B, {x: v for x, v in sau.items() if x != "buoi_trong"})
    # thẻ lịch: MỘT dòng ghi chú cho cả ngày, không phải hai dòng theo buổi
    assert [g for g in v2.dung_lich(B, sau, {})["ghi_chu"] if g["ma"] in ("ngay_trong", "buoi_trong")] == [
        {"ma": "ngay_trong", "cau": "Ban ngày của ngày 1 để trống — bạn đã bỏ các điểm của ngày này.", "ngay": 1}]
    # nút gợi ý điểm thay (điểm bản cũ định tự lấp): bấm = lệnh thêm đủ ngày + buổi ⇒ thêm được, dấu của buổi đó tự gỡ, buổi kia vẫn trống
    (nut,) = dong[1]["nut"]
    assert nut == {"nhan": f"Gợi ý điểm thay: {T[a['goi_y_thay']]['ten']}", "gui": f"thêm {T[a['goi_y_thay']]['ten']} vào buổi chiều ngày 1"}
    lai = _them(k2["luu"], T[a["goi_y_thay"]]["ten"], 1, "chieu", **MOI)
    assert lai["da_ap"] and lai["khung"]["ngay"][0]["buoi"]["chieu"] == [a["goi_y_thay"]] and lai["khung"]["buoi_trong"] == [[1, "sang"]]
    assert not v2.kiem_khung_v2(B, lai["khung"])
    assert _bo(k1["luu"], T[chieu]["ten"], **CU)["da_ap"]  # công tắc tắt ⇒ đường cũ (tự lấp) y như trước
    # bỏ lần lượt MỌI điểm ban ngày của NGÀY CUỐI: lệnh cuối cũng bỏ ngay, số ngày giữ nguyên (không tự rút ngày), ngày 1 không đổi
    luu2 = luu
    for j in [x for x, v in s._vi_tri(k).items() if v[0] == 2]:
        kq = _bo(luu2, T[j]["ten"], **MOI)
        assert kq["da_ap"] and not kq["khong_doi"]
        luu2 = kq["luu"]
    k3 = luu2["khung"]
    assert k3["tham_so"]["so_ngay"] == 2 and all(k3["ngay"][1]["buoi"][b] == [] for b in v2.BUOI_NGAY) and not v2.kiem_khung_v2(B, k3)
    assert k3["ngay"][0] == k["ngay"][0] and k3["ngay"][1]["buoi"]["toi"] == k["ngay"][1]["buoi"]["toi"]
    # ngày ĐI XA (tối nghỉ sau chuyến đi xa, không có hoạt động tối): bỏ hết điểm thì ngày đó hết "đi xa" — bản đầu của nhánh để bộ xếp tự chọn một
    # hoạt động tối cho nó (15 / 216 ngày của lưới, 3 ca còn xếp lại tối ngày khác). Nay tối của ngày đó GIỮ trống, tối các ngày khác y nguyên
    kx, luux = _lich(3, "nhe_nhang", so_thich=("thien_nhien",))
    (dx,) = [d for d, ma in kx.get("toi_nghi", {}).items() if ma == "xa"]
    for j in [x for x, v in s._vi_tri(kx).items() if v[0] == dx]:
        kq = _bo(luux, T[j]["ten"], **MOI)
        luux = kq["luu"]
    sau_x, cau = luux["khung"], s.thay_doi(B, kq)[0]["cau"]
    assert kq["da_ap"][0]["ngay_trong"] == dx and not v2.kiem_khung_v2(B, sau_x)
    assert [ng["buoi"]["toi"] for ng in sau_x["ngay"]] == [ng["buoi"]["toi"] for ng in kx["ngay"]] and sau_x["ngay"][dx - 1]["buoi"]["toi"] == []
    assert cau.endswith(f"Ban ngày của ngày {dx} nay không còn điểm nào; buổi tối của ngày {dx} và các điểm của những ngày khác giữ nguyên.")
    assert "vào chỗ trống" not in cau and "Buổi tối xếp lại" not in cau


def test_after_a_removal_the_emptied_session_is_the_place_suggested_for_a_later_add():
    """Lượt trình duyệt cả cụm 23/11/2026: bỏ điểm duy nhất của chiều ngày 1 (buổi đó để trống) rồi xin thêm một điểm vào một buổi không nhận được ⇒ gợi ý
    từng là "buổi sáng ngày 1" (xếp theo ngày rồi buổi) dù buổi chiều ngày 1 đang trống cũng đặt được. Buổi mang dấu để trống không bị chặn — và nay
    được nêu trước; thêm vào đó thì dấu tự gỡ. Công tắc tắt ⇒ cách chọn gợi ý y như cũ (hàm không nhận `khung`)."""
    k, luu = _mac_dinh()
    (chieu1,) = k["ngay"][0]["buoi"]["chieu"]
    luu1 = _bo(luu, T[chieu1]["ten"], **MOI)["luu"]
    k1, vt1 = luu1["khung"], s._vi_tri(luu1["khung"])
    assert k1["buoi_trong"] == [[1, "chieu"]]
    n = 0
    for i, d in T.items():
        if i in vt1 or i == chieu1 or "chieu" not in d["buoi"] or any(i in ng["buoi"]["toi"] for ng in k1["ngay"]):
            continue
        thang = [g for g in s._cach_them(B, luu1, s._ts(k1["tham_so"]), k1, vt1, list(luu1["loai"]), i, None, None, day=True, khu=True) if g["thay"] is None]
        kq = _them(luu1, d["ten"], 2, "chieu", **MOI)
        if kq["da_ap"] or not any((g["ngay"], g["buoi"]) == (1, "chieu") for g in thang):
            continue
        n += 1
        (m,) = kq["khong_doi"]
        assert [(g["ngay"], g["buoi"], g["thay"]) for g in m["cach"]] == [(1, "chieu", None)], d["ten"]  # buổi đang trống là chỗ được gợi ý
        (nut,) = _dong(kq)["nut"]
        assert nut == {"nhan": "Thêm vào buổi chiều ngày 1", "gui": f"thêm {d['ten']} vào buổi chiều ngày 1"}, d["ten"]
        sau = _them(luu1, d["ten"], 1, "chieu", **MOI)["khung"]
        assert s._vi_tri(sau)[i] == (1, "chieu") and "buoi_trong" not in sau and not v2.kiem_khung_v2(B, sau), d["ten"]
    assert n >= 1


def test_a_blocked_move_offers_each_working_slot_as_a_button_and_every_button_applies():
    """Lệnh DỜI bị luật xếp chặn: câu vốn kể các chỗ dời được ("Dời được sang: …") nhưng người dùng phải gõ lại (sổ vết 24/11/2026: 30 / 143 dòng "không
    đổi" là loại này). Công tắc bật ⇒ mỗi chỗ đó (nhiều nhất `MAX_CHO_HOI`) là một nút gửi lệnh dời đủ tên; áp đúng lệnh của nút ⇒ dời được, kể cả nút
    mà lần dời thật đổi chỗ hai điểm (nhãn nút nói rõ điểm kia). Công tắc tắt ⇒ câu y như cũ, không nút."""
    k, luu = _lich()
    vt = s._vi_tri(k)
    cho = sorted({(ng["ngay"], b) for ng in k["ngay"] for b in v2.BUOI_NGAY})
    co_nut = doi_cho = khong_cho = 0
    for a in sorted(vt):
        for c in [x for x in cho if x != vt[a]] + [(vt[a][0], "toi")]:  # kèm một ca "dời điểm ban ngày sang buổi tối" (mục `khong_buoi_hop_le`)
            hd = [(s.HanhDongToi if c[1] == "toi" else s.HanhDong)(loai="doi_buoi", ten=a, ngay=c[0], buoi=c[1])]
            kq = s.ap(B, luu, hd, **MOI)
            if kq["da_ap"] or "goi_y" not in kq["khong_doi"][0]:
                continue
            (kd,), dong, cu = kq["khong_doi"], _dong(kq), _dong(s.ap(B, luu, hd, **CU))
            assert kq["khung"] == k and "nut" not in cu and cu["cau"] == dong["cau"].replace(" Bấm một nút dưới đây để dời.", "")
            if not kd["goi_y"]:
                khong_cho += 1
                assert "nut" not in dong and dong["cau"].endswith("chỉ đứng được ở chỗ hiện tại.")
                continue
            co_nut += 1
            assert dong["cau"].endswith("Bấm một nút dưới đây để dời.") and len(dong["nut"]) == min(len(kd["goi_y"]), s.MAX_CHO_HOI)
            for g, nut in zip(kd["goi_y"], dong["nut"]):
                noi = f"buổi {s.NHAN_BUOI[g['buoi']]} ngày {g['ngay']}"
                kem = f", đổi chỗ với {T[g['doi_voi']]['ten']}" if g["doi_voi"] else ""  # câu gửi nhắc tên điểm bị đổi chỗ ⇒ bấm là làm, không hỏi lần hai
                assert nut["gui"] == f"dời {T[a]['ten']} sang {noi}{kem}" and nut["nhan"].startswith(f"Dời sang {noi}") and "chon" not in nut
                assert (f"(đổi chỗ với {T[g['doi_voi']]['ten']})" in nut["nhan"]) if g["doi_voi"] else "đổi chỗ" not in nut["nhan"]
                dong_y = s.diem_dong_y_doi_cho(B, nut["gui"], set(vt))  # đúng thứ route đưa cho bộ áp khi nút được bấm
                assert dong_y == ({g["doi_voi"]} if g["doi_voi"] else set())
                sau = s.ap(B, luu, [s.HanhDong(loai="doi_buoi", ten=a, ngay=g["ngay"], buoi=g["buoi"])], dong_y_doi_cho=dong_y, **MOI)  # đúng lệnh mà câu `gui` nói
                assert sau["da_ap"] and s._vi_tri(sau["khung"])[a] == (g["ngay"], g["buoi"])
                doi_cho += bool(g["doi_voi"])
    assert co_nut and doi_cho  # bảng điểm thật phải có cả nút dời thẳng lẫn nút đổi chỗ hai điểm, không thì test này không kiểm gì


def test_an_ambiguous_short_name_asks_which_place_with_one_button_each():
    """Chủ dự án 24/11/2026: tên ngắn phải dùng được cho mọi điểm; nguyên tắc 22:02 23/11: thiếu thông tin thì hỏi lại kèm gợi ý. Cách gọi trỏ tới NHIỀU
    điểm ("lăng" khi lịch có hai lăng) ⇒ lịch đứng yên + câu hỏi "bạn muốn nói điểm nào" + mỗi ứng viên một nút gửi lại đúng lệnh đó với tên đủ (trước:
    "chưa có trong danh sách điểm của lịch"). Tên ngắn RÕ trong lịch ("Tự Đức", gõ không dấu cũng được) ⇒ làm luôn. Công tắc tắt ⇒ câu cũ."""
    k, luu = _lich()
    vt = s._vi_tri(k)
    lang = [j for j in vt if T[j]["ten"].startswith("Lăng ")]
    assert len(lang) >= 2
    kq = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten="lăng")], **MOI)
    (m,), d = kq["khong_doi"], _dong(kq)
    assert kq["khung"] == k and kq["da_ap"] == [] and m["ma_luat"] == "ten_mo_ho" and m["ung_vien"] == lang[:s.MAX_CHO_HOI]
    assert d["hoi"] is True and d["cau"].startswith("“lăng” có thể là ") and d["cau"].endswith("Lịch chưa đổi gì.") and "Chưa làm" not in d["cau"]
    assert [n["gui"] for n in d["nut"]] == [f"bỏ {T[j]['ten']}" for j in m["ung_vien"]] and [n["nhan"] for n in d["nut"]] == [T[j]["ten"] for j in m["ung_vien"]]
    assert s.cau_goi_y(B, kq) == tuple(n["gui"] for n in d["nut"])
    for j in m["ung_vien"]:  # bấm một nút = lệnh đủ tên ⇒ bỏ đúng điểm đó
        assert s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten=T[j]["ten"])], **MOI)["da_ap"][0]["diem"] == j
    rut = T[lang[0]]["ten"].split(" ", 1)[1]  # "Lăng Tự Đức" ⇒ "Tự Đức": trong lịch chỉ trỏ tới một điểm ⇒ làm luôn, không hỏi
    for cach in (rut, rut.lower(), s._bo_dau(rut).lower()):
        assert s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten=cach)], **MOI)["da_ap"][0]["diem"] == lang[0], cach
    # lệnh THÊM gọi theo loại: ứng viên là các điểm CHƯA có trong lịch; nút mang đủ ngày + buổi người dùng đã nói
    them = s.ap(B, luu, [s.HanhDong(loai="them_diem", ten="lăng", ngay=1, buoi="sang")], **MOI)
    (mt,) = them["khong_doi"]
    assert them["khung"] == k and mt["ma_luat"] == "ten_mo_ho" and mt["ung_vien"] and not set(mt["ung_vien"]) & set(vt)
    assert _dong(them)["nut"][0]["gui"] == f"thêm {T[mt['ung_vien'][0]]['ten']} vào buổi sáng ngày 1"
    # lệnh DỜI và THAY cũng hỏi; câu của nút giữ chỗ muốn dời tới / điểm thay vào
    doi = s.ap(B, luu, [s.HanhDong(loai="doi_buoi", ten="lăng", ngay=2, buoi="chieu")], **MOI)
    assert doi["khung"] == k and _dong(doi)["nut"][0]["gui"] == f"dời {T[lang[0]]['ten']} sang buổi chiều ngày 2"
    thay = s.ap(B, luu, [s.HanhDong(loai="thay_diem", ten="lăng", ten_moi="Hổ Quyền")], **MOI)
    assert thay["khung"] == k and _dong(thay)["nut"][0]["gui"] == f"thay {T[lang[0]]['ten']} bằng Hổ Quyền"
    cu = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten="lăng")], **CU)  # công tắc tắt: không hỏi, câu cũ
    assert cu["khung"] == k and [x["ma_luat"] for x in cu["khong_doi"]] == ["ngoai_bang"]


def test_an_add_whose_wording_matches_several_places_asks_even_when_only_one_is_not_in_the_plan():
    """Người đọc nhánh 24/11/2026: "thêm sông Hương" khi lịch đã có Ca Huế trên sông Hương từng TỰ thêm Công viên ven sông Hương (dòng duy nhất chưa có) —
    người dùng có thể đang nói về thứ đã có ⇒ không đoán: câu hỏi nêu cả dòng đã có, MỘT nút cho dòng chưa có."""
    ca_hue, cong_vien = s.khop_ten(B, "Ca Huế trên sông Hương"), s.khop_ten(B, "Công viên ven sông Hương")
    assert ca_hue and cong_vien and s.ung_vien_ten(B, "sông Hương") == [ca_hue, cong_vien] or s.ung_vien_ten(B, "sông Hương") == [cong_vien, ca_hue]
    assert s.tim_diem(B, "them_diem", "sông Hương", {ca_hue})[0] is None
    k, luu = next((k, luu) for n in (2, 3, 4, 5) for k, luu in [_lich(n, "can_bang", so_thich=())] if ca_hue in s._ngay_toi(k) and cong_vien not in s._ngay_toi(k))
    kq = s.ap(B, luu, [s.HanhDong(loai="them_diem", ten="sông Hương")], **MOI)
    (m,), d = kq["khong_doi"], _dong(kq)
    assert kq["khung"] == k and kq["da_ap"] == [] and m["ma_luat"] == "ten_mo_ho" and m["ung_vien"] == [cong_vien] and m["da_co"] == [T[ca_hue]["ten"]]
    assert "Ca Huế trên sông Hương cũng khớp “sông Hương” nhưng đã có trong lịch" in d["cau"] and [n["gui"] for n in d["nut"]] == ["thêm Công viên ven sông Hương"]


def test_a_typed_move_into_an_occupied_slot_asks_before_swapping_the_other_place():
    """Nguyên tắc chủ dự án xác nhận 22:02 23/11/2026: việc nào chạm tới thứ người dùng không nhắc cũng hỏi trước. Lệnh "dời X sang buổi B ngày N" mà chỗ đó
    đang có đúng một điểm Y từng ĐỔI CHỖ hai điểm ngay và câu báo không nêu Y (đếm 24/11/2026: 117 / 117 lệnh dời áp được của lưới). Nay: lịch đứng yên +
    câu nói Y sẽ chuyển đi đâu + MỘT nút; câu có nhắc tên Y (chính câu của nút, hay "đổi chỗ X với Y") hoặc đáp lại ngay sau câu hỏi ⇒ làm, và câu báo
    nêu cả Y. Công tắc tắt ⇒ đổi chỗ ngay như cũ (câu báo vẫn nêu Y)."""
    k, luu = _mac_dinh()
    vt = s._vi_tri(k)
    n = 0
    for a in sorted(vt):
        for c in sorted({v for v in vt.values()} - {vt[a]}):
            hd = [s.HanhDong(loai="doi_buoi", ten=a, ngay=c[0], buoi=c[1])]
            cu = s.ap(B, luu, hd, **CU)
            if not cu["da_ap"] or "doi_voi" not in cu["da_ap"][0]:
                continue  # lệnh bị luật chặn, hoặc không đổi chỗ ai
            n += 1
            y = cu["da_ap"][0]["doi_voi"]["diem"]
            assert vt[y] == c and f"{T[y]['ten']} chuyển sang buổi {s.NHAN_BUOI[vt[a][1]]} ngày {vt[a][0]}." in s.thay_doi(B, cu)[0]["cau"]
            hoi = s.ap(B, luu, hd, **MOI)
            (m,), d = hoi["khong_doi"], _dong(hoi)
            assert hoi["khung"] == k and hoi["da_ap"] == [] and m["ma_luat"] == "doi_cho_hoi" and d["hoi"] is True
            assert d["cau"].startswith(f"Buổi {s.NHAN_BUOI[c[1]]} ngày {c[0]} đang là {T[y]['ten']} — dời {T[a]['ten']} sang đó thì {T[y]['ten']} chuyển sang buổi ")
            (nut,) = d["nut"]
            assert nut["gui"] == f"dời {T[a]['ten']} sang buổi {s.NHAN_BUOI[c[1]]} ngày {c[0]}, đổi chỗ với {T[y]['ten']}" and nut["gui"] in s.cau_goi_y(B, hoi)
            assert s.diem_dong_y_doi_cho(B, nut["gui"], set(vt)) == {y}
            for cau in (f"đổi chỗ với {T[y]['ten']}", f"hoán đổi với {T[y]['ten']} nhé", f"dời {T[a]['ten']} sang buổi {s.NHAN_BUOI[c[1]]} ngày {c[0]}; tráo với {T[y]['ten']} giúp mình"):
                assert s.diem_dong_y_doi_cho(B, cau, set(vt)) == {y}, cau  # lời đổi chỗ thật vẫn là đồng ý
            for dong_y in ({"dong_y_doi_cho": frozenset({y})}, {"chen_da_hoi": (nut["gui"],)}):  # bấm nút · đáp "ừ" ở lượt kế
                assert s.ap(B, luu, hd, **dong_y, **MOI)["khung"] == cu["khung"]
            # câu chỉ NHẮC TÊN Y mà không có lời đổi chỗ (người đọc nhánh dò 24/11/2026: 28 / 28 mẫu từng làm Y bị đẩy đi) ⇒ không phải đồng ý ⇒ vẫn hỏi
            x_ten, y_ten, noi = T[a]["ten"], T[y]["ten"], f"buổi {s.NHAN_BUOI[c[1]]} ngày {c[0]}"
            for cau in (f"dời {x_ten} sang {noi}, giữ nguyên {y_ten}", f"dời {x_ten} sang {noi}, đừng đụng tới {y_ten}", f"dời {x_ten} sang {noi} đi cùng {y_ten}",
                        f"dời {x_ten} sang {noi} cho gần {y_ten}", f"dời {x_ten} sang {noi} vì {y_ten} mình đi rồi", f"dời {x_ten} sang {noi}, đừng đổi chỗ với {y_ten}",
                        f"dời {x_ten} sang {noi}, không đổi chỗ với {y_ten}",
                        # lượt dò thứ hai: có lời đổi chỗ + tên Y nhưng câu KHÔNG phải lời đồng ý (câu hỏi, điều kiện, phủ định đứng sau, tên Y ở vế khác ý)
                        f"dời {x_ten} sang {noi}, có phải đổi chỗ với {y_ten} không?", f"dời {x_ten} sang {noi} thì có phải đổi chỗ với {y_ten} không",
                        f"dời {x_ten} sang {noi}, đổi chỗ với {y_ten} được không?", f"dời {x_ten} sang {noi}, nếu phải đổi chỗ với {y_ten} thì thôi",
                        f"dời {x_ten} sang {noi}, đổi chỗ với {y_ten} thì mình không chịu", f"dời {x_ten} sang {noi}, đổi chỗ với Hổ Quyền và {y_ten} giữ nguyên",
                        f"dời {x_ten} sang {noi}, đảo lại cho {y_ten} khỏi bị dời"):
                dy = s.diem_dong_y_doi_cho(B, cau, set(vt))
                assert dy == frozenset() and s.ap(B, luu, hd, dong_y_doi_cho=dy, **MOI)["khung"] == k, cau
            # Y có lệnh dời RIÊNG trong cùng lượt ("cho X lên…, còn Y để <chỗ cũ của X>") ⇒ không hỏi; câu báo không lặp vế "Y chuyển sang…"
            hai = s.ap(B, luu, hd + [s.HanhDong(loai="doi_buoi", ten=y, ngay=vt[a][0], buoi=vt[a][1])], **MOI)
            assert hai["khung"] == cu["khung"] and hai["khong_doi"] == [] and "chuyển sang" not in s.thay_doi(B, hai)[0]["cau"]
            assert s.ap(B, luu, hd, chen_da_hoi=("dời Hổ Quyền sang buổi sáng ngày 1, đổi chỗ với Đại Nội Huế",), **MOI)["da_ap"] == []  # câu gợi ý của việc khác
    assert n  # lịch mặc định phải có ít nhất một lệnh dời đổi chỗ được, không thì test này không kiểm gì


def test_swap_two_named_places_is_read_by_code_and_applied_without_asking():
    """Lượt thật 24/11/2026: "đổi chỗ Lăng Tự Đức với Lăng Khải Định" ⇒ model trả "chưa hỗ trợ" ⇒ "việc này mình chưa sửa được" — trong khi đó là câu dễ gõ
    nhất sau câu hỏi "dời X sang đó thì Y chuyển đi". Nay code tự đọc câu đó (cả hai là điểm ban ngày của lịch) thành MỘT lệnh dời A vào chỗ của B; người
    dùng đã nhắc cả hai điểm ⇒ bộ áp đổi chỗ luôn, không hỏi lại. Đọc theo danh sách cho phép: có chữ lạ, là câu hỏi, điểm ngoài lịch ⇒ không đọc."""
    k, luu = _mac_dinh()
    vt = s._vi_tri(k)
    # một cặp điểm ở hai chỗ khác nhau mà lần dời thật đổi chỗ được đúng hai điểm đó (luật xếp cho phép)
    a, b = next((x, y) for x in sorted(vt) for y in sorted(vt) if vt[x] != vt[y]
                and (kq := s.ap(B, luu, [s.HanhDong(loai="doi_buoi", ten=x, ngay=vt[y][0], buoi=vt[y][1])], **CU))["da_ap"]
                and kq["da_ap"][0].get("doi_voi", {}).get("diem") == y)
    for cau in (f"đổi chỗ {T[a]['ten']} với {T[b]['ten']}", f"Hoán đổi {T[a]['ten']} và {T[b]['ten']} giúp mình nhé", f"bạn tráo {T[a]['ten']} với {T[b]['ten']} đi"):
        hd = s.doi_buoi_tu_cau(B, luu, cau)
        assert [(h.loai, h.ten, h.ngay, h.buoi) for h in hd] == [("doi_buoi", a, vt[b][0], vt[b][1])], cau
        assert s.diem_dong_y_doi_cho(B, cau, set(vt)) == {b}, cau
        kq = s.ap(B, luu, hd, dong_y_doi_cho=s.diem_dong_y_doi_cho(B, cau, set(vt)), **MOI)
        sau = s._vi_tri(kq["khung"])
        assert kq["khong_doi"] == [] and sau[a] == vt[b] and sau[b] == vt[a] and not v2.kiem_khung_v2(B, kq["khung"]), cau
        assert f"{T[b]['ten']} chuyển sang buổi {s.NHAN_BUOI[vt[a][1]]} ngày {vt[a][0]}." in s.thay_doi(B, kq)[0]["cau"]
    ngoai = next(d["ten"] for d in B.diem if d["id"] not in vt and d["id"] not in s._ngay_toi(k) and len(d["ten"].split()) >= 2)
    for cau in (f"đổi chỗ {T[a]['ten']} với {T[b]['ten']} được không?", f"đổi chỗ {T[a]['ten']} với {ngoai}", f"đổi chỗ {T[a]['ten']} với {T[b]['ten']} rồi bỏ Đại Nội Huế",
                f"đừng đổi chỗ {T[a]['ten']} với {T[b]['ten']}", f"{T[a]['ten']} với {T[b]['ten']} cái nào đẹp hơn"):
        assert s.doi_buoi_tu_cau(B, luu, cau) == [], cau
