"""B5c (plan `docs/superpowers/plans/2026-11-05-phase-9-b5c-plan.md` D6, D9): dò số người / ngày-đêm và chuẩn hoá số tiền — hàm thuần, 0 USD.
Câu thử là bảng §3b của plan + câu tự viết (không lấy từ bộ đo). Chưa nối vào lõi chat (B5 chưa merge)."""
import pytest

from llm.do_so import MAX_NGUOI, SoNguoi, do_ngay_du_toan, do_so_ngay, do_so_nguoi
from llm.so_tien import gia_tri_dong, tim_gia_tri, tim_so_tien


@pytest.mark.parametrize("cau, nguoi, ngay", [
    ("hai vợ chồng đi Huế 3 ngày hết bao nhiêu", 2, ("3", None)),
    ("đi 2N1Đ, nhóm 4 người", 4, ("2", None)),
    ("3n2đ cho 1 người", 1, ("3", None)),
    ("đi một mình hai ngày", 1, ("2", None)),
    ("gia đình năm người, 2 ngày 2 đêm", 5, (None, "dem_lech")),   # đêm ≠ ngày − 1 ⇒ ngoài bảng
    ("đi 3 ngày, ngày thứ 2 nghỉ", None, ("3", None)),             # "ngày thứ 2" không phải số ngày
    ("đi 3 ngày hay 4 ngày cũng được", None, (None, None)),        # nhiều giá trị ⇒ không đoán
    ("cả nhà đi cuối tuần", None, (None, None)),                    # không dò được ⇒ hỏi
    ("năm nay đi 2 ngày", None, ("2", None)),                       # "năm" không đứng trước "người"
    ("đi nửa ngày thôi", None, (None, "nua_ngay")),
    ("1 ngày 1 đêm cho 2 khách", 2, (None, "dem_lech")),
    ("3 ngày 2 đêm, nhóm 6 thành viên", 6, ("3", None)),
], ids=lambda x: x if isinstance(x, str) else None)
def test_plan_table_people_and_days(cau, nguoi, ngay):
    assert do_so_nguoi(cau).tong == nguoi
    assert do_ngay_du_toan(cau) == ngay


@pytest.mark.parametrize("cau, ket_qua", [
    ("2 người lớn và 1 trẻ em mua vé Đại Nội", SoNguoi(3, 2, 1)),
    ("vé cho 3 người lớn", SoNguoi(3, 3, 0)),                      # không nhắc trẻ ⇒ 0 trẻ
    ("2 người lớn và mấy đứa nhỏ", SoNguoi(None, 2, None)),         # có trẻ không rõ số ⇒ không tổng (D2b)
    ("vợ chồng mình và 2 con", SoNguoi(4, 2, 2)),
    ("vé cho 2 bé", SoNguoi(None, None, 2)),                        # chỉ số trẻ ⇒ không biết người lớn
    ("nhóm 5 người, 2 người lớn", SoNguoi()),                       # mâu thuẫn ⇒ không đoán
    ("3 người lớn rồi 4 người lớn", SoNguoi()),                     # hai giá trị ⇒ không đoán
    ("nhóm 5 đứa bạn", SoNguoi(5)),
])
def test_adults_and_children(cau, ket_qua):
    assert do_so_nguoi(cau) == ket_qua


def test_over_limit_is_flagged():
    assert do_so_nguoi("nhóm 30 người").tong == 30 and do_so_nguoi("nhóm 30 người").qua_gioi_han
    assert not do_so_nguoi(f"nhóm {MAX_NGUOI} người").qua_gioi_han


def test_b5_day_detector_unchanged():
    # B5 (lịch trình) giữ nguyên: "2 ngày 2 đêm" vẫn là 2 ngày ở đó; chỉ dự toán B5c coi là ngoài bảng
    assert do_so_ngay("2 ngày 2 đêm") == "2" and do_ngay_du_toan("2 ngày 2 đêm") == (None, "dem_lech")


@pytest.mark.parametrize("text, dong", [
    ("50.000đ", [50_000]), ("50.000 đ", [50_000]), ("1,5 triệu", [1_500_000]), ("200k", [200_000]), ("200.000 VNĐ", [200_000]),
    ("300 nghìn", [300_000]), ("1,500,000 đ", [1_500_000]), ("2.5 triệu", [2_500_000]),
    ("150.000–300.000 đồng", [150_000, 300_000]), ("1–1,5 triệu", [1_000_000, 1_500_000]), ("từ 100 đến 200 nghìn", [100_000, 200_000]),
    ("đi 3N2Đ", []), ("nghìn năm lịch sử", []), ("2 người, 3 ngày", []),
])
def test_money_values(text, dong):
    assert tim_gia_tri(text) == dong


def test_money_value_matches_detector_strings():
    # một chuỗi `tim_so_tien` (B5 dùng) ⇒ đúng một giá trị; "1,5 triệu" = "1.500.000 đ" sau chuẩn hoá (D9)
    assert [gia_tri_dong(s) for s in tim_so_tien("vé 1,5 triệu, phòng 1.500.000 đ")] == [1_500_000, 1_500_000]
