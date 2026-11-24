"""Công tắc `so_tay` (bản thử, nhánh thu-b-so-tay): phần THUẦN của sổ tay chuyến đi — dàn ý từ lịch, dòng dữ kiện do code chép, luật lọc ý của model, mục ăn
uống. Không model, không Qdrant. Đường API chạy thật: `data/x15_phan_ai_2026-11-23/b_so_tay/`."""
import re

import pytest

from llm import so_tay as st
from llm import the_noi as thn
from llm.assistant import AssistantFlags

LICH = {"ngay": [{"ngay": 1, "muc": [
            {"id_muc": "n1-sang-1", "buoi": "sang", "id_diem": "dai_noi", "ten": "Đại Nội Huế", "gio": "8:00 – 10:30", "bai_id": "heritages/heritage/Đại Nội Huế.md",
             "anh": {"src": "/anh/lich/dai_noi.jpg", "tac_gia": "X", "giay_phep": "Y"}},
            {"id_muc": "n1-toi-1", "buoi": "toi", "id_diem": None, "ten": "Tối nghỉ", "gio": None}]},
                 {"ngay": 2, "muc": [{"id_muc": "n2-sang-1", "buoi": "sang", "id_diem": "dam_chuon", "ten": "Đầm Chuồn", "gio": "8:00 – 10:30",
                                      "bai_id": "travel/places/Đầm Chuồn.md", "anh": None}]}],
        "an": [{"ngay": 1, "bua": "trua", "gan": "Đại Nội Huế", "quan": [{"ten": "Quán A", "loai": "quán ăn", "nhan": None, "bai_id": "foods/restaurants/a.md"},
                                                                         {"ten": "Quán B", "loai": "quán ăn", "nhan": "chưa kiểm", "bai_id": None}]}],
        "ghi_chu": [{"ma": "mua_mua", "cau": "Huế đang mùa mưa — nên mang áo mưa"}, {"ma": "gio_goi_y", "cau": "…"}]}


def test_dan_y_theo_lich_moi_diem_mot_muc_an_uong_theo_ngay_roi_truoc_khi_di():
    muc = st.dan_y(LICH)
    assert [m["id"] for m in muc] == ["n1-sang-1", "n1-an", "n2-sang-1", "truoc-khi-di"]  # tối nghỉ không thành mục; ngày 2 không có quán ⇒ không có mục ăn
    assert [m["loai"] for m in muc] == ["diem", "an_uong", "diem", "truoc_khi_di"]
    ra = st.ra_giao_dien(muc[0])
    assert ra == {"id": "n1-sang-1", "loai": "diem", "ngay": 1, "buoi": "sang", "ten": "Đại Nội Huế", "gio": "8:00 – 10:30",
                  "bai_id": "heritages/heritage/Đại Nội Huế.md", "anh": {"src": "/anh/lich/dai_noi.jpg"}}  # không gửi tác giả / giấy phép ảnh, không gửi id_diem


def _noi(dong=(), ve=None, rel="heritages/heritage/X.md"):
    return thn.Noi("X", rel, re.compile("X"), tuple(dong), ve, None)


BANG = thn.Bang((), "travel/tickets/ve.md", "Vé tham quan", "| STT | Tên | Địa giới | Người lớn | Trẻ em |")


def test_du_kien_chep_tu_the_noi_va_o_thieu_la_mot_khuon():
    doan, nguon = st.du_kien(_noi(["Địa chỉ: 1 Lê Lợi, Huế.", "Giờ mở cửa: 07h00 – 17h30; mùa đông 07h30."], "| 6 | X *(Y)* | Phường Z | 100.000 | Miễn phí |"), BANG,
                             "heritages/heritage/X.md")
    assert [(d["nhan"], d["kieu"], d["chu"]) for d in doan] == [
        ("Địa chỉ", "van", "1 Lê Lợi, Huế. [1]"), ("Giờ mở cửa", "van", "07h00 – 17h30; mùa đông 07h30. [1]"),
        ("Giá vé", "van", "Người lớn 100.000 đồng · trẻ em 7–12 tuổi miễn phí [2]")]
    assert [(s["id"], s["bai_id"]) for s in nguon] == [(1, "heritages/heritage/X.md"), (2, "travel/tickets/ve.md")] and nguon[1]["excerpts"][1].startswith("| 6 |")
    # bảng không có gì: di tích ⇒ hai ô thiếu; nơi không phải di tích ⇒ chỉ ô giờ (không in "Kho chưa có: Giá vé" cho đầm phá, quán)
    assert [(d["nhan"], d["kieu"]) for d in st.du_kien(None, BANG, "heritages/heritage/X.md")[0]] == [("Giờ mở cửa", "thieu"), ("Giá vé", "thieu")]
    assert [(d["nhan"], d["kieu"]) for d in st.du_kien(None, BANG, "travel/places/Đầm Chuồn.md")[0]] == [("Giờ mở cửa", "thieu")]
    assert [(d["nhan"], d["kieu"]) for d in st.du_kien(None, None, None)[0]] == [("Giờ mở cửa", "thieu")]  # điểm không có bài riêng
    # bài không có dòng nhãn giờ nhưng bảng điểm của lịch có (chép từ câu văn của bài) ⇒ dùng dòng của bảng, nguồn trỏ về bài; địa chỉ dài cắt ở ngoặc đầu
    dai = "Địa chỉ: Làng An Truyền, phường Mỹ Thượng, thành phố Huế (" + "lịch sử địa giới " * 10 + ")."
    doan, nguon = st.du_kien(_noi([dai], rel="travel/places/Y.md"), BANG, "travel/places/Y.md", ("mở tự do 24/24", "travel/places/Y.md"), "Y")
    assert [(d["nhan"], d["chu"]) for d in doan] == [("Địa chỉ", "Làng An Truyền, phường Mỹ Thượng, thành phố Huế [1]"), ("Giờ mở cửa", "Mở tự do 24/24 [2]")]
    assert nguon[0]["excerpts"] == [dai] and nguon[1]["heading_path"] == [st.MUC_GIO_BANG] and nguon[1]["bai_id"] == "travel/places/Y.md"


class _D:
    def __init__(self, i, bai, muc, chu):
        self.id, self.text, self.metadata = f"{bai}#{i}", chu, {"source": bai, "heading_path": [muc]}


def test_chon_bang_chung_chi_doan_cua_bai_rieng_khi_co():
    bai = [_D(0, "a.md", "Tổng quan", "giới thiệu chung"), _D(1, "a.md", "Kiến trúc", "công trình kiến trúc nổi bật đáng xem"), _D(2, "a.md", "Lịch sử", "năm xây dựng"),
           _D(3, "a.md", "Lưu ý tham quan", "quy tắc ứng xử trang phục")]
    tim = [_D(9, "ve.md", "Vé", "xe điện"), bai[2], _D(8, "dv.md", "Dịch vụ", "máy thuyết minh")]
    chon = st.chon_bang_chung(tim, bai, "a.md", k=3)
    assert [d.id for d in chon] == ["a.md#2", "a.md#3", "a.md#1"]  # đoạn của bài theo lần tìm trước, rồi theo xếp trong bài (đoạn khớp nhiều từ của cụm hơn đứng trước); không đoạn nào của bài khác
    assert [d.id for d in st.chon_bang_chung(tim, [], None, k=2)] == ["ve.md#9", "a.md#2"]  # không biết bài nào ⇒ kết quả tìm như nó vốn có
    # điểm không có bài riêng, bảng điểm trỏ sang bài khác ⇒ chỉ đoạn của bài đó có nhắc đúng tên điểm
    pho = [_D(0, "pho.md", "Tổng quan", "Phố đi bộ ven sông"), _D(1, "pho.md", "Gần đó", "Trung tâm Nghệ thuật Lê Bá Đảng nằm ở đầu phố"), _D(2, "pho.md", "Ăn uống", "quầy ăn vặt")]
    assert [d.id for d in st.chon_bang_chung(tim, pho, "pho.md", ten_rieng="Trung tâm Nghệ thuật Lê Bá Đảng")] == ["pho.md#1"]


def test_loc_y_bo_y_khong_nguon_qua_dai_co_gio_gia_va_giu_tran():
    y = [{"chu": "Điện Thái Hòa là nơi đặt ngai vàng [3]", "nguon": [3, 99]},          # giữ; mã trong câu và số lạ bị gỡ
         {"chu": "Ý không có nguồn hợp lệ", "nguon": [99]},
         {"chu": "Mở cửa từ 7h30 đến 17h", "nguon": [3]}, {"chu": "Vé người lớn 200.000 đồng", "nguon": [3]}, {"chu": "Vào cửa miễn phí", "nguon": [4]},
         {"chu": "Bình minh 04h30 – 06h00 mặt đầm phủ sương", "nguon": [4]},             # giờ trong ngày nói về cảnh ⇒ giữ
         {"chu": "x" * 201, "nguon": [3]},
         {"chu": "Lăng có 127 bậc tam cấp, xây năm 1920", "nguon": [4]},               # số không phải giờ / giá ⇒ giữ
         {"chu": "Nên dành 2 giờ tham quan", "nguon": [4]}, {"chu": "Ý thứ tư", "nguon": [3]}, {"chu": "Ý thứ năm vượt trần", "nguon": [3]}]
    giu, bo = st.loc_y(y, {3, 4}, 5)
    assert giu == ["Điện Thái Hòa là nơi đặt ngai vàng [3]", "Bình minh 04h30 – 06h00 mặt đầm phủ sương [4]", "Lăng có 127 bậc tam cấp, xây năm 1920 [4]",
                   "Nên dành 2 giờ tham quan [4]", "Ý thứ tư [3]"]
    assert bo == {"khong_nguon": 1, "qua_dai": 1, "gio_gia": 3, "qua_tran": 1}
    assert st.loc_y([{"chu": "Taxi khoảng 15.000 đồng mỗi km", "nguon": [1]}], {1}, 4, cam_gio_gia=False)[0] == ["Taxi khoảng 15.000 đồng mỗi km [1]"]


def test_khoi_model_rong_thi_la_o_thieu():
    assert st.khoi_model("luu_y", [], {1})[0] == {"nhan": "Lưu ý", "kieu": "thieu", "chu": None, "gach": None}
    assert st.khoi_model("luu_y", [{"chu": "Giá vé 50.000 đồng", "nguon": [1]}], {1})[0]["kieu"] == "thieu"  # bị lọc hết cũng là ô thiếu
    assert st.khoi_model("nen_xem", [{"chu": "Hồ Lưu Khiêm", "nguon": [1]}], {1})[0] == {"nhan": "Nên xem", "kieu": "gach", "chu": None, "gach": ["Hồ Lưu Khiêm [1]"]}


def test_muc_an_uong_la_quan_cua_lich_va_doan_chung():
    doan, nguon = st.muc_an_uong(st.dan_y(LICH)[1]["an"])
    assert doan == [{"nhan": "Bữa trưa — gần Đại Nội Huế", "kieu": "gach", "chu": None, "gach": ["Quán A (quán ăn) [1]", "Quán B (quán ăn) — chưa kiểm"]}]
    assert nguon == [{"id": 1, "title": "Quán A", "bai_id": "foods/restaurants/a.md", "heading_path": [st.MUC_QUAN], "excerpts": []}]
    chung = st.doan_chung(LICH, "Câu an toàn bão lũ")
    assert [(d["kieu"], d["chu"]) for d in chung[:2]] == [("an_toan", "Câu an toàn bão lũ"), ("an_toan", "Huế đang mùa mưa — nên mang áo mưa")] and chung[-1]["nhan"] == "Lưu ý chung"
    assert st.nguon_da_dung([{"chu": "a [2]", "gach": None}, {"chu": None, "gach": ["b [3][2]"]}], [{"id": i} for i in (1, 2, 3)]) == [{"id": 2}, {"id": 3}]


def test_tach_ma_chu_gui_ra_khong_con_so_tham_chieu():
    ra = st.tach_ma([{"nhan": "Giờ mở cửa", "kieu": "van", "chu": "07h00 – 17h30. [1]", "gach": None},
                     {"nhan": "Nên xem", "kieu": "gach", "chu": None, "gach": ["Hồ Lưu Khiêm [3][2]", "Quán B (quán ăn) — chưa kiểm"]},
                     {"nhan": "Lưu ý", "kieu": "thieu", "chu": None, "gach": None}])
    assert ra == [{"nhan": "Giờ mở cửa", "kieu": "van", "chu": "07h00 – 17h30.", "so": [1], "gach": None, "gach_so": None},
                  {"nhan": "Nên xem", "kieu": "gach", "chu": None, "so": [], "gach": ["Hồ Lưu Khiêm", "Quán B (quán ăn) — chưa kiểm"], "gach_so": [[3, 2], []]},
                  {"nhan": "Lưu ý", "kieu": "thieu", "chu": None, "so": [], "gach": None, "gach_so": None}]


def test_cong_tac_mac_dinh_tat_va_can_lich_luu():
    assert AssistantFlags().so_tay is False
    with pytest.raises(ValueError):
        AssistantFlags(so_tay=True)
