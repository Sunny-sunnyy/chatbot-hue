"""Lệnh "thêm X" — bước cuối CHÈN điểm mới vào TRƯỚC một điểm đang có của buổi, HỎI TRƯỚC BẰNG NÚT (24/11/2026) — 0 USD, không gọi model, bảng điểm thật.

Vì sao có bước chèn: bộ sửa lịch đặt điểm mới vào cuối danh sách giữ chỗ nên bộ xếp luôn xếp nó SAU các điểm đang có của buổi; điểm có suất diễn giờ cố
định, đóng cửa sớm hay xa hơn thì đứng sau là phạm luật ⇒ lệnh bị từ chối dù đổi thứ tự trong buổi là hợp luật.
Vì sao HỎI TRƯỚC: chèn trước làm điểm đang có lùi giờ (đếm 24/11 trên 407 lệnh đủ ngày + buổi: 407 / 407 lùi từ 60 phút) = "một mục khác của lịch phải
dời" ⇒ theo nguyên tắc chủ dự án xác nhận 22:02 23/11/2026, lịch đứng yên, trợ lý nói điểm nào lùi tới mấy giờ + MỘT nút; bấm (hoặc đáp lại đúng lệnh
đó ở lượt kế) mới áp. Chỉ có khi công tắc `sua_lich_hoi_truoc` bật; tắt ⇒ như main (không có bước chèn). Lệnh nào trước nay làm được thì kết quả y như cũ."""
from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from test_sua_lich_v2 import B, _lich

T = B.theo_id
ID = {d["ten"]: d["id"] for d in B.diem}
CU = {"them_khong_the": True, "them_day": True, "them_khu": True, "them_han_che": True}
HOI = {**CU, "them_hoi_truoc": True}
X = "Duyệt Thị Đường"


def _them(luu, ten, ngay=None, buoi=None, **kw):
    return s.ap(B, luu, [s.HanhDong(loai="them_diem", ten=ten, ngay=ngay, buoi=buoi)], **kw)


def test_an_add_that_only_fits_before_an_existing_place_asks_first_and_applies_on_consent():
    k, luu = _lich(1, "nhe_nhang", so_thich=("di_tich",))  # mỗi buổi một điểm; suất diễn của điểm xin thêm có giờ cố định
    vt, i, ts = s._vi_tri(k), ID[X], s._ts(k["tham_so"])
    # đứng SAU các điểm đang có: không chỗ nào được, kể cả khi nới nhịp / nới khu
    assert all(s._thu_cho(B, luu, ts, vt, [], i, cho, False, **kw)[0] is None for cho in s._cho_thu(B, k, i, None, None)
               for kw in ({}, {"day_moi": cho[0]}, {"day_moi": cho[0], "khu_moi": cho[0]}))
    # công tắc hỏi-trước TẮT ⇒ không có bước chèn: lịch đứng yên, không cách nào là chỗ chèn-trước
    tat = _them(luu, X, **CU)
    assert tat["da_ap"] == [] and tat["khung"] == k and not any(g.get("chen") for m in tat["khong_doi"] for g in m.get("cach") or [])
    # công tắc BẬT, lệnh không nói chỗ: chỉ còn chỗ chèn-trước ⇒ MỘT câu hỏi nêu điểm bị lùi + giờ cũ / mới, MỘT nút; lịch đứng yên
    hoi = _them(luu, X, **HOI)
    (m,) = hoi["khong_doi"]
    assert hoi["da_ap"] == [] and hoi["khung"] == k and m["ma_luat"] == "them_chen_hoi" and m["hoi_truoc"] is True
    d, b = m["dich"]
    (ke,) = [j for j, v in vt.items() if v == (d, b)]  # điểm đang có của buổi đó — nó là điểm sẽ lùi
    (dong,) = s.thay_doi(B, hoi)
    (nut,) = dong["nut"]
    assert nut == {"nhan": f"Đặt {X} trước {T[ke]['ten']}", "gui": f"thêm {X} vào buổi {s.NHAN_BUOI[b]} ngày {d}, đặt trước {T[ke]['ten']}"}
    assert dong["duoc"] is False and dong["hoi"] is True and m["lui"][0]["diem"] == T[ke]["ten"] and m["lui"][0]["tu"] == k["gio"][ke] != m["lui"][0]["den"]
    assert f"{T[ke]['ten']} lùi từ {k['gio'][ke]} sang {m['lui'][0]['den']}" in dong["cau"] and dong["cau"].endswith("Lịch chưa đổi gì.")
    assert "Chưa làm" not in dong["cau"] and "«" not in dong["cau"]
    assert nut["gui"] in s.cau_goi_y(B, hoi)  # route nhớ câu của nút đúng một lượt
    # nói đủ ngày + buổi, hoặc "xếp giúp mình": vẫn là một mục khác phải lùi ⇒ vẫn hỏi, cùng câu hỏi đó
    for kw in ({"ngay": d, "buoi": b}, {"tu_xep": True}):
        lai = _them(luu, X, **kw, **HOI)
        assert lai["da_ap"] == [] and lai["khung"] == k and [x["ma_luat"] for x in lai["khong_doi"]] == ["them_chen_hoi"] and lai["khong_doi"][0]["gui"] == nut["gui"]
    # ĐỒNG Ý — bấm nút (câu gửi có lời "đặt trước") hoặc đáp lại đúng lệnh đó ngay sau câu hỏi ⇒ áp, điểm mới đứng trước, điểm kia lùi đúng giờ đã nói
    assert s.dong_y_chen_cau(nut["gui"]) and not s.dong_y_chen_cau(f"thêm {X} vào buổi chiều ngày 1") and not s.dong_y_chen_cau("đừng đặt trước Đại Nội")
    kq = _them(luu, X, d, b, dong_y_chen=True, **HOI)
    (a,), sau = kq["da_ap"], kq["khung"]
    ds = next(x for x in sau["ngay"] if x["ngay"] == d)["buoi"][b]
    assert ds.index(i) < ds.index(ke) and not v2.kiem_khung_v2(B, sau)  # điểm mới đứng TRƯỚC điểm đang có, lịch đúng luật
    assert {j: v for j, v in s._vi_tri(sau).items() if j != i} == vt  # không điểm nào đổi ngày / buổi
    assert a["dung_sau"] == [{"diem": ke, "gio": sau["gio"][ke]}] and sau["gio"][ke] == m["lui"][0]["den"]  # giờ thật = giờ câu hỏi đã nói
    assert f"{X} xếp trước {T[ke]['ten']} (nay {sau['gio'][ke]}) cho kịp giờ." in s.thay_doi(B, kq)[0]["cau"]
    assert _them(luu, X, d, b, chen_da_hoi=(nut["gui"],), **HOI)["khung"] == sau and _them(luu, X, chen_da_hoi=(nut["gui"],), **HOI)["khung"] == sau
    assert _them(luu, X, d, b, chen_da_hoi=("thêm Hổ Quyền vào buổi sáng ngày 1, đặt trước Đại Nội Huế",), **HOI)["da_ap"] == []  # câu gợi ý của việc khác


def test_an_add_that_already_worked_is_placed_exactly_as_before():
    """Chèn trước là bước CUỐI: lệnh đặt được sau các điểm đang có thì vẫn đứng cuối buổi, không có vế "xếp trước …", không bị hỏi."""
    k, luu = _lich(2, "can_bang", so_thich=())
    for kw in (CU, {**HOI, "tu_xep": True}):
        kq = _them(luu, "Hổ Quyền", **kw)
        (a,), sau = kq["da_ap"], kq["khung"]
        ds = next(x for x in sau["ngay"] if x["ngay"] == a["ngay"])["buoi"][a["buoi"]]
        assert ds[-1] == ID["Hổ Quyền"] and "dung_sau" not in a and "xếp trước" not in s.thay_doi(B, kq)[0]["cau"]
