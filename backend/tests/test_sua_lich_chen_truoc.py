"""Lệnh "thêm X" — bước cuối CHÈN điểm mới vào TRƯỚC một điểm đang có của buổi (23/11/2026) — 0 USD, không gọi model, bảng điểm thật.

Vì sao: bộ sửa lịch đặt điểm mới vào cuối danh sách giữ chỗ nên bộ xếp luôn xếp nó SAU các điểm đang có của buổi; điểm có suất diễn giờ cố định, đóng
cửa sớm hay xa hơn thì đứng sau là phạm luật ⇒ lệnh bị từ chối dù đổi thứ tự trong buổi là hợp luật (đếm trên lưới 1.143 lệnh thêm của đoàn thường:
31 / 291 lệnh bị từ chối). Nay, CHỈ khi mọi lần thử "đứng sau" đều không được, bộ áp thử chèn điểm mới vào trước từng điểm đang có; không điểm nào đổi
ngày / buổi, dòng báo nêu giờ mới của điểm đứng sau. Lệnh nào trước nay làm được thì kết quả y như cũ."""
from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from test_sua_lich_v2 import B, _lich

T = B.theo_id
ID = {d["ten"]: d["id"] for d in B.diem}
CU = {"them_khong_the": True, "them_day": True, "them_khu": True, "them_han_che": True}


def _them(luu, ten, ngay=None, buoi=None, **kw):
    return s.ap(B, luu, [s.HanhDong(loai="them_diem", ten=ten, ngay=ngay, buoi=buoi)], **kw)


def test_an_add_that_only_fits_before_an_existing_place_is_applied_and_reports_the_shifted_time():
    k, luu = _lich(1, "nhe_nhang", so_thich=("di_tich",))  # mỗi buổi một điểm; suất diễn của điểm xin thêm có giờ cố định
    vt, i, ts = s._vi_tri(k), ID["Duyệt Thị Đường"], s._ts(k["tham_so"])
    # đứng SAU các điểm đang có: không chỗ nào được, kể cả khi nới nhịp / nới khu ⇒ trước đây lệnh này bị từ chối
    assert all(s._thu_cho(B, luu, ts, vt, [], i, cho, False, **kw)[0] is None for cho in s._cho_thu(B, k, i, None, None)
               for kw in ({}, {"day_moi": cho[0]}, {"day_moi": cho[0], "khu_moi": cho[0]}))
    kq = _them(luu, "Duyệt Thị Đường", **CU)
    (a,), sau = kq["da_ap"], kq["khung"]
    ds = next(x for x in sau["ngay"] if x["ngay"] == a["ngay"])["buoi"][a["buoi"]]
    assert ds.index(i) < len(ds) - 1 and not v2.kiem_khung_v2(B, sau)  # điểm mới đứng TRƯỚC một điểm đang có, lịch đúng luật
    assert {j: v for j, v in s._vi_tri(sau).items() if j != i} == vt  # không điểm nào đổi ngày / buổi
    ke = ds[ds.index(i) + 1]
    assert a["dung_sau"] == [{"diem": ke, "gio": sau["gio"][ke]}] and sau["gio"][ke] != k["gio"][ke]  # điểm đứng sau lùi giờ — dòng báo nói giờ mới
    assert f"Duyệt Thị Đường xếp trước {T[ke]['ten']} (nay {sau['gio'][ke]}) cho kịp giờ." in s.thay_doi(B, kq)[0]["cau"]
    # công tắc `sua_lich_hoi_truoc`: chỗ đó thành nút gợi ý của câu hỏi; bấm ra đúng khung trên
    hoi = _them(luu, "Duyệt Thị Đường", them_hoi_truoc=True, **CU)
    (m,) = hoi["khong_doi"]
    assert hoi["khung"] == k and m["ma_luat"] == "them_hoi" and (m["cho"][0]["ngay"], m["cho"][0]["buoi"]) == (a["ngay"], a["buoi"])
    assert _them(luu, "Duyệt Thị Đường", a["ngay"], a["buoi"], them_hoi_truoc=True, **CU)["khung"] == sau


def test_an_add_that_already_worked_is_placed_exactly_as_before():
    """Chèn trước là bước CUỐI: lệnh đặt được sau các điểm đang có thì vẫn đứng cuối buổi, không có vế "xếp trước …" (bản thử đầu chèn ngay trong
    lần thử thường làm 47 / 852 lệnh đang làm được của lưới đổi sang chỗ khác)."""
    k, luu = _lich(2, "can_bang", so_thich=())
    kq = _them(luu, "Hổ Quyền", **CU)
    (a,), sau = kq["da_ap"], kq["khung"]
    ds = next(x for x in sau["ngay"] if x["ngay"] == a["ngay"])["buoi"][a["buoi"]]
    assert ds[-1] == ID["Hổ Quyền"] and "dung_sau" not in a and "xếp trước" not in s.thay_doi(B, kq)[0]["cau"]
