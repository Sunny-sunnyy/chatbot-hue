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
])
def test_day_count_needs_a_number_of_days_in_the_text(cau, so_ngay, hien_tai, duoc):
    assert sl.so_ngay_co_trong_cau(cau, so_ngay, hien_tai) is duoc


def test_filter_keeps_other_actions():
    luu = {"khung": {"tham_so": {"so_ngay": 3}}}
    hd = [sl.HanhDong(loai="doi_so_ngay", so_ngay=1), sl.HanhDong(loai="bo_diem", ten="Đại Nội")]
    assert [h.loai for h in sl.loc_hanh_dong(hd, "Bỏ Đại Nội, mình đi từ ngày 20/12", luu)] == ["bo_diem"]
