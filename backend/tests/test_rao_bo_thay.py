"""Rào "bỏ / thay phải có chỗ neo" (22/11/2026) — 0 USD. Vì sao: trong cuộc đã có lịch, sau lượt "Kể các quán chè ở Huế", tin "Bỏ quán đầu đi rồi viết
lại danh sách" bị lần hiểu ý sửa lịch gán "quán đầu" cho điểm đầu của lịch và lịch bị đổi thật ("Đã bỏ Đại Nội Huế, thêm…" — 5 / 6 lượt thật). Lần hiểu
ý chỉ thấy lịch + đúng câu đó, nên code chỉ nhận hành động bỏ / thay khi câu người dùng có TÊN điểm bị chạm hoặc MỐC của lịch. File này kiểm phần code
(bảng điểm thật, lịch 3 ngày thật, bộ áp thật); model chỉ là đồ giả để DỰNG điều kiện "model đã trả hành động bỏ / thay"."""
import asyncio
import copy

import pytest

from llm import len_ke_hoach as lkh
from llm import sua_lich_v2 as s
from llm.assistant import AnswerTrace
from test_cong_dot_1 import flags_from
from test_sua_lich_v2 import B, _lich

K, _ = _lich()
DAU = sorted(s._vi_tri(K))[0]                 # một điểm đang nằm trong lịch
TEN = B.theo_id[DAU]["ten"]
NGOAI = next(d["ten"] for d in B.diem if d["id"] not in s._vi_tri(K))  # một điểm của bảng chưa có trong lịch


def _bo(ten=TEN):
    return s.HanhDong(loai="bo_diem", ten=ten)


@pytest.mark.parametrize("cau", [
    "Bỏ quán đầu đi rồi viết lại danh sách",           # ca lỗi thật
    "bỏ cái thứ hai đi",
    "Xoá câu vừa rồi đi",
    "Bỏ quán đầu đi, mình đi du lịch tự túc mà",        # "du lịch" không phải mốc của lịch
    "Bỏ cái đó đi rồi kể lịch sử quán thứ hai",          # "lịch sử" cũng không
    "Bỏ món đầu, tra giúp âm lịch hôm nay",
    "Bỏ điểm đầu đi rồi viết lại danh sách",           # lượt thật 22/11 sau "Kể các điểm tham quan miễn phí": "điểm + vị trí" trần không phải mốc
    "Bỏ điểm đầu tiên đi",
    "mình đi ngày 2/12, bỏ quán đầu đi",                # ngày tháng, không phải ngày 2 của lịch
    "Bỏ món đầu đi cho lịch sự",
])
def test_remove_without_place_name_or_plan_anchor_is_dropped(cau):
    assert s.loc_bo_thay(B, [_bo()], cau) == ([], [_bo()])
    thay = s.HanhDong(loai="thay_diem", ten=TEN, ten_moi=NGOAI)
    assert s.loc_bo_thay(B, [thay], cau.replace("Bỏ", "Thay").replace("bỏ", "thay")) == ([], [thay])


@pytest.mark.parametrize("cau", [
    f"Bỏ {TEN} đi",
    f"bỏ {TEN.lower()} giúp mình nhé",
    "Bỏ điểm đầu tiên của ngày 2",
    "Bỏ điểm cuối ngày 3 nhé",
    "Bỏ cái buổi chiều hôm đầu",
    "Ngày 2 nặng quá, bớt một chỗ đi giúp mình",
    "Bỏ điểm đầu tiên khỏi lịch vì đang có bão",
    "Chuyến đi này bỏ bớt một chỗ cho nhẹ",
])
def test_real_edit_with_a_name_or_a_plan_anchor_is_kept(cau):
    assert s.loc_bo_thay(B, [_bo()], cau) == ([_bo()], [])


def test_a_distinctive_part_of_the_name_counts_as_the_name():
    tu_duc, thien_mu = s.khop_ten(B, "Lăng Tự Đức"), s.khop_ten(B, "Chùa Thiên Mụ")
    assert tu_duc and thien_mu
    assert s._neo_trong_cau(B, tu_duc, "Lăng Tự Đức", "bỏ tự đức đi") == (True, None)
    assert s._neo_trong_cau(B, thien_mu, "Chùa Thiên Mụ", "Thay Thiên Mụ bằng chỗ khác") == (True, None)
    # chữ loại ("lăng") không đủ để LÀM: danh sách vừa kể cũng có thể toàn lăng — từ 24/11/2026 nó thành cách gọi mơ hồ (hỏi lại), không còn bị bỏ im
    assert s._neo_trong_cau(B, tu_duc, "Lăng Tự Đức", "bỏ cái lăng đầu đi") == (False, "lăng")
    le_ba_dang = s.khop_ten(B, "Trung tâm Nghệ thuật Lê Bá Đảng")
    assert le_ba_dang and s._neo_trong_cau(B, le_ba_dang, "Trung tâm Nghệ thuật Lê Bá Đảng", "bỏ quán đầu đi, quán ở trung tâm ấy") == (False, None)  # khúc chung, không tên riêng


def test_one_word_brand_names_of_evening_cafes_count_as_the_name():
    """Chủ dự án, lúc tự test 23/11/2026: sau "tối ngày 1 đi cà phê HANOK", gõ `thay HANOK bằng MoKa Kafe` ⇒ lần hiểu ý trả ĐÚNG thay_diem
    "HANOK Cafe Huế" ⇒ "MoKa KaFe" nhưng rào loại hành động (câu chỉ có MỘT chữ của tên) ⇒ lượt rơi về hỏi đáp thường. Tên thương hiệu một chữ
    của bảng (HANOK, MoKa, TIME, AEON) là tên gọi tắt người ta thật sự gõ ⇒ là "tên khác" của dòng; chữ thường một âm tiết thì vẫn KHÔNG đủ."""
    thay = s.HanhDongToiHoiBo(loai="thay_diem", ten="HANOK Cafe Huế", ten_moi="MoKa KaFe")
    assert s.loc_bo_thay(B, [thay], "thay HANOK bằng MoKa Kafe") == ([thay], [])   # nguyên văn câu của chủ dự án
    for cau, ten in (("bỏ MoKa", "MoKa KaFe"), ("bỏ HANOK đi", "HANOK Cafe Huế"), ("bỏ TIME", "The TIME Coffee & Bakery"), ("bỏ AEON đi", "AEON Mall Huế")):
        h = _bo(ten)
        assert s.loc_bo_thay(B, [h], cau) == ([h], []), cau
    assert [s.khop_ten(B, t) for t in ("HANOK", "moka", "TIME", "AEON")] == ["ca_phe_hanok", "ca_phe_moka", "ca_phe_the_time", "aeon_mall"]
    # không nới cho chữ thường: một âm tiết của tên Việt ("Mụ", "Nội", "Trăng") hay chữ loại ("cafe", "phố") vẫn không phải chỗ neo
    for cau, ten in (("bỏ Mụ đi", "Chùa Thiên Mụ"), ("bỏ Nội", "Đại Nội Huế"), ("bỏ quán cafe đi", "HANOK Cafe Huế"), ("bỏ Trăng", "Bến Trăng Café & Bar")):
        h = _bo(ten)
        assert s.loc_bo_thay(B, [h], cau) == ([], [h]), cau
    assert [s.khop_ten(B, t) for t in ("Mụ", "cafe", "Huế", "phố")] == [None] * 4


def test_a_name_outside_the_table_is_kept_only_when_it_is_a_real_name_in_the_message():
    """Tên model điền không phải điểm của bảng: tên riêng có trong câu ⇒ giữ (bộ áp nói thật "không có trong lịch"); chỉ là chữ trỏ ⇒ bỏ."""
    assert s.khop_ten(B, "Vincom Plaza") is None and s.khop_ten(B, "quán đầu") is None
    assert s.loc_bo_thay(B, [_bo("Vincom Plaza")], "Bỏ Vincom Plaza đi")[1] == []
    assert s.loc_bo_thay(B, [_bo("quán đầu")], "Bỏ quán đầu đi rồi viết lại danh sách")[0] == []
    assert s.loc_bo_thay(B, [_bo(None)], "bỏ đi")[0] == []


def test_other_action_kinds_are_not_touched():
    them = s.HanhDong(loai="them_diem", ten=NGOAI)
    assert s.loc_bo_thay(B, [them, _bo()], "thêm cái đó vào, bỏ cái kia") == ([them], [_bo()])


def _chay(ra, cau, flags=None, goi_y=()):
    flags = flags or flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, sua_lich_v2=True)
    k, luu = _lich()

    class Gen:
        async def hieu_sua(self, prompt, call_log, **kw):
            return list(ra)

    tr = AnswerTrace(history=(("Kể các quán chè ở Huế", ""),))
    tr.lich_luu, tr.sua_chon, tr.goi_y_sua = luu, None, goi_y
    truoc = copy.deepcopy(luu)
    return asyncio.run(lkh.hieu_va_ap(cau, Gen(), tr, flags)), tr, luu == truoc


def test_message_about_the_list_just_given_leaves_the_plan_alone_and_goes_the_ordinary_way():
    kq, tr, nguyen = _chay([_bo()], "Bỏ quán đầu đi rồi viết lại danh sách")
    assert kq is None and tr.sua == {"n_hanh_dong": 0} and nguyen          # None ⇒ lõi đi đường hỏi đáp thường; lịch đã lưu không đổi
    assert tr.vet["sua"]["khong_neo"] == 1 and tr.vet["sua"]["hanh_dong"] == [] and tr.vet["sua"]["model_ra"][0]["loai"] == "bo_diem"


def test_same_action_with_the_place_named_is_still_applied():
    kq, tr, _ = _chay([_bo()], f"Bỏ {TEN} đi")
    assert kq is not None and [x["loai"] for x in kq["da_ap"]] == ["bo_diem"] and "khong_neo" not in tr.vet["sua"]


def test_dropped_action_is_said_out_loud_when_the_turn_has_another_edit():
    kq, tr, _ = _chay([_bo(), s.HanhDong(loai="them_diem", ten=NGOAI)], f"Bỏ quán đầu đi, thêm {NGOAI} vào")
    assert kq is not None and "bo_diem" in kq["chua_lam"] and all(x["loai"] != "bo_diem" for x in kq["da_ap"])
    assert any(d["cau"].startswith("Chưa làm: bỏ điểm") for d in s.thay_doi(B, kq))


def test_agreeing_to_the_suggestion_of_the_previous_turn_is_not_guarded():
    """"ok thay đi" sau một câu code gợi ý: tên điểm nằm trong câu gợi ý, không trong câu người dùng ⇒ rào không áp cho lượt này."""
    co = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, sua_lich_v2=True, sua_lich_them_khong_the=True)
    thay = s.HanhDong(loai="thay_diem", ten=TEN, ten_moi=NGOAI)
    kq, tr, _ = _chay([thay], "ok thay đi", co, goi_y=(f"thay {TEN} bằng {NGOAI}",))
    assert kq is not None and "khong_neo" not in tr.vet["sua"] and "thay_diem" not in kq["chua_lam"]
    kq, tr, _ = _chay([thay], "ok thay đi", co)                              # không có câu gợi ý nào ⇒ rào áp như thường
    assert kq is None and tr.vet["sua"]["khong_neo"] == 1


def test_short_names_work_for_every_place_not_only_the_cafes():
    """Chủ dự án 24/11/2026: lỗi «thay HANOK bằng MoKa Kafe» (chữa 23/11 bằng ba tên gọi tắt ghi tay trong bảng) "phải áp dụng cho mọi trường hợp, mọi
    địa điểm". Với MỌI dòng của bảng: tên đủ viết thường, tên đủ gõ không dấu, tên bỏ chữ loại đứng đầu ("Tự Đức", "tu duc"), và chữ kiểu tên thương
    hiệu ("HANOK") đều phải ra đúng dòng đó — ở bộ khớp tên (model chép chữ người dùng) lẫn ở rào chỗ neo (model điền tên đủ, người dùng gõ tên ngắn).
    Đếm trước trên code cũ: 92 / 221 cách gọi chỉ-một-dòng được nhận; không dấu gần như không cách nào."""
    import collections
    import re
    dau = collections.Counter(re.findall(r"\w+", d["ten"])[0].casefold() for d in B.diem)
    n = 0
    for d in B.diem:
        w = re.findall(r"\w+", d["ten"])
        cach = [d["ten"].lower(), s._bo_dau(d["ten"]).lower()]
        if dau[w[0].casefold()] >= 2 and len(w) >= 3:  # bỏ chữ loại mà còn từ hai chữ ("Đầm Chuồn" ⇒ "Chuồn" là một âm tiết thường: cố ý không nhận)
            rut = " ".join(w[1:])
            cach += [rut, rut.lower(), s._bo_dau(rut).lower()]
        cach += [x for x in w if sum(c.isupper() for c in x) >= 2]
        for c in cach:
            if s.ung_vien_ten(B, c) != [d["id"]]:  # cách gọi này trỏ tới nhiều dòng (hai phố đi bộ chung chữ…) ⇒ không thuộc ca "chỉ một dòng"
                continue
            n += 1
            h = _bo(d["ten"])
            assert s.khop_ten(B, c) == d["id"], c
            # cách gọi gõ không dấu chỉ được nhận trong câu gõ không dấu cả câu (câu có dấu thì "hai ba", "cho" là chữ thật)
            assert s.loc_bo_thay(B, [h], f"bo {c} di" if c == s._bo_dau(c) else f"bỏ {c} đi") == ([h], []), c
    assert n >= 150  # 47 dòng × (tên đủ + không dấu) + các tên bỏ chữ loại + chữ thương hiệu; ít hơn ⇒ điều kiện "chỉ một dòng" đang lọc quá tay


def test_ordinary_syllables_and_type_words_do_not_name_a_place_silently():
    """Mặt trái phải giữ: một âm tiết thường của tên không phải cách gọi ("tiền" ≠ Cầu Trường Tiền; "bỏ" bỏ dấu ≠ "bộ" của "Phố đi bộ…"; "cho" ≠ "chợ");
    gọi trần theo LOẠI ("lăng") không bao giờ được làm luôn — rào trả hành động về đúng chữ người dùng gõ để bộ áp hỏi lại."""
    for cau, ten in (("bỏ bớt một chỗ cho đỡ tốn tiền", "Cầu Trường Tiền"), ("bỏ Nguyễn đi", "Phố đi bộ Nguyễn Đình Chiểu"), ("Bỏ món đầu đi cho lịch sự", "Chợ Đông Ba"),
                     ("bỏ Hai đi", "Phố đi bộ Hai Bà Trưng")):
        h = _bo(ten)
        assert s.loc_bo_thay(B, [h], cau) == ([], [h]), cau
    assert [s.khop_ten(B, t) for t in ("tiền", "Nguyễn", "cho", "lăng", "phố đi bộ", "đi bộ")] == [None] * 6
    h = _bo("Lăng Tự Đức")
    (giu,), bo = s.loc_bo_thay(B, [h], "bỏ cái lăng đầu đi")
    assert bo == [] and giu.loai == "bo_diem" and giu.ten == "lăng"  # không bị bỏ im, không làm theo lựa chọn của model
    assert s.tim_diem(B, "bo_diem", "lăng", {s.khop_ten(B, "Lăng Tự Đức")}) == (None, [s.khop_ten(B, "Lăng Tự Đức")])  # lịch chỉ có một lăng: vẫn hỏi
    assert s.tim_diem(B, "bo_diem", "Tự Đức", {s.khop_ten(B, "Lăng Tự Đức")}) == (s.khop_ten(B, "Lăng Tự Đức"), [])


def test_accent_free_matching_does_not_turn_ordinary_words_into_place_names():
    """Người đọc nhánh (24/11/2026) dò ra hai lỗ của bản đầu: (1) so không dấu chạy cả trong câu gõ ĐỦ DẤU — "bỏ hai ba điểm cho đỡ mệt" bị đọc ra Phố đi
    bộ Hai Bà Trưng; (2) câu gõ không dấu — động từ lệnh + chữ kế trùng một khúc của tên: "bo nguyen ngay 2 di" (bỏ nguyên ngày 2) ⇒ "…bộ Nguyễn Đình
    Chiểu", "doi vong lai…" ⇒ Đồi Vọng Cảnh, "bo hai diem dau…" ⇒ "…bộ Hai Bà Trưng". Nay: so không dấu chỉ khi CẢ CÂU gõ không dấu, và chỉ nhận khúc
    bằng trọn một tên hoặc gồm toàn chữ tên riêng (không tính chữ đầu tên), không phải chỉ chữ số đếm. Tên thật gõ không dấu vẫn được nhận."""
    for cau, ten in (("bỏ hai ba điểm cho đỡ mệt", "Phố đi bộ Hai Bà Trưng"), ("cho bao nhiêu điểm thì bỏ bớt đi", "Phố cổ và chợ Bao Vinh"),
                     ("bo hai diem dau ngay 1", "Phố đi bộ Hai Bà Trưng"), ("bo nguyen ngay 2 di", "Phố đi bộ Nguyễn Đình Chiểu"),
                     ("doi vong lai thu tu hai ngay", "Đồi Vọng Cảnh"), ("bo hai ba diem cho do met", "Phố đi bộ Hai Bà Trưng")):
        h = _bo(ten)
        assert s._neo_trong_cau(B, s.khop_ten(B, ten), ten, cau) == (False, None), cau
        assert s.loc_bo_thay(B, [h], cau) == ([], [h]), cau
    assert [s.khop_ten(B, t) for t in ("bo nguyen", "bo hai", "doi vong", "cho bao", "hai ba")] == [None] * 5
    for cach, ten in (("tu duc", "Lăng Tự Đức"), ("lang tu duc", "Lăng Tự Đức"), ("an dinh", "Cung An Định"), ("ho quyen", "Hổ Quyền"), ("dai noi hue", "Đại Nội Huế"),
                      ("hai ba trung", "Phố đi bộ Hai Bà Trưng"), ("thien mu", "Chùa Thiên Mụ")):
        assert s.khop_ten(B, cach) == s.khop_ten(B, ten), cach
        h = _bo(ten)
        assert s.loc_bo_thay(B, [h], f"bo {cach} di") == ([h], []), cach
        assert s.loc_bo_thay(B, [h], f"bỏ {cach} đi") == ([], [h]), cach  # câu có dấu: chữ không dấu trong nó không được coi là tên gõ tắt
