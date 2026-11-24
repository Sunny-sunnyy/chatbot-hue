"""Công tắc `so_tay` (bản thử, nhánh thu-b-so-tay): phần THUẦN của sổ tay chuyến đi — dàn ý từ lịch, dòng dữ kiện do code chép, luật lọc ý của model, mục ăn
uống. Không model, không Qdrant. Đường API chạy thật: `data/x15_phan_ai_2026-11-23/b_so_tay/`."""
import asyncio
import inspect
import json
import re
from types import SimpleNamespace

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
    # địa chỉ dài cắt ở ngoặc đầu (nguồn giữ nguyên dòng)
    dai = "Địa chỉ: Làng An Truyền, phường Mỹ Thượng, thành phố Huế (" + "lịch sử địa giới " * 10 + ")."
    doan, nguon = st.du_kien(_noi([dai], rel="travel/places/Y.md"), BANG, "travel/places/Y.md")
    assert [(d["nhan"], d["kieu"], d["chu"]) for d in doan] == [("Địa chỉ", "van", "Làng An Truyền, phường Mỹ Thượng, thành phố Huế [1]"), ("Giờ mở cửa", "thieu", None)]
    assert nguon[0]["excerpts"] == [dai]


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
    assert {k: v for k, v in bo.items() if k != "chu"} == {"khong_nguon": 1, "qua_dai": 1, "gio_gia": 3, "qua_tran": 1}
    assert [ly for ly, _ in bo["chu"]] == ["khong_nguon", "gio_gia", "gio_gia", "gio_gia", "qua_dai", "qua_tran"]
    assert st.loc_y([{"chu": "Taxi khoảng 15.000 đồng mỗi km", "nguon": [1]}], {1}, 4, cam_gio_gia=False)[0] == ["Taxi khoảng 15.000 đồng mỗi km [1]"]


def test_khoi_model_rong_thi_la_o_thieu():
    assert st.khoi_model("luu_y", [], {1})[0] == {"nhan": "Lưu ý", "kieu": "thieu", "chu": None, "gach": None}
    assert st.khoi_model("luu_y", [{"chu": "Giá vé 50.000 đồng", "nguon": [1]}], {1})[0]["kieu"] == "thieu"  # bị lọc hết cũng là ô thiếu
    assert st.khoi_model("nen_xem", [{"chu": "Hồ Lưu Khiêm", "nguon": [1]}], {1})[0] == {"nhan": "Nên xem", "kieu": "gach", "chu": None, "gach": ["Hồ Lưu Khiêm [1]"]}


def test_muc_an_uong_la_quan_cua_lich_va_doan_chung():
    doan, nguon = st.muc_an_uong(st.dan_y(LICH)[1]["an"])
    assert doan == [{"nhan": "Bữa trưa — gần Đại Nội Huế", "kieu": "gach", "chu": None, "gach": ["Quán A (quán ăn) [1]", "Quán B (quán ăn) — chưa kiểm"]}]
    assert nguon == [{"id": 1, "title": "Quán A", "bai_id": "foods/restaurants/a.md", "heading_path": [st.MUC_QUAN], "excerpts": []}]
    # bài của quán có dòng địa chỉ / giờ ⇒ code chép kèm vào dòng quán, nguồn mang đúng các dòng đó
    the = thn.Bang((thn.Noi("Quán A", "foods/restaurants/a.md", re.compile("Quán A"), ("Địa chỉ: 12 Lê Lợi, Huế.", "Giờ hoạt động: 06:00 – 14:00."), None, None),))
    doan, nguon = st.muc_an_uong(st.dan_y(LICH)[1]["an"], the)
    assert doan[0]["gach"][0] == "Quán A (quán ăn) · địa chỉ: 12 Lê Lợi, Huế · giờ: 06:00 – 14:00 [1]" and doan[0]["gach"][1] == "Quán B (quán ăn) — chưa kiểm"
    assert nguon[0]["excerpts"] == ["Địa chỉ: 12 Lê Lợi, Huế.", "Giờ hoạt động: 06:00 – 14:00."] and nguon[0]["heading_path"] == [thn.MUC_THE]
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


def test_gio_mo_cua_chi_tu_dong_cua_bai_khong_tu_bang_diem_cua_lich():
    """Phiên đo đọc nhánh 24/11/2026: `gio_mo_cua` của bảng điểm là sổ ghi chú của nhóm, không phải câu của bài — 16 / 19 dòng không sạch, ví dụ Chùa Từ
    Hiếu "Kho: không niêm yết giờ; web lệch (06–17 … · 07–17 … · 07:30–20:00 …) ⇒ không đặt giờ", Đèo Hải Vân lấy giờ từ một trang web ngoài kho. Thứ
    phải luôn đúng không chép từ sổ ghi chú ⇒ `du_kien` không nhận dòng nào của bảng điểm; bài không có dòng nhãn giờ ⇒ ô "Kho chưa có"."""
    assert "gio_bang" not in inspect.signature(st.du_kien).parameters
    doan, nguon = st.du_kien(_noi(["Địa chỉ: Thôn Dương Xuân Thượng III, phường Thủy Xuân."], rel="heritages/heritage/Chùa Từ Hiếu.md"), BANG,
                             "heritages/heritage/Chùa Từ Hiếu.md")
    assert [(d["nhan"], d["kieu"]) for d in doan] == [("Địa chỉ", "van"), ("Giờ mở cửa", "thieu"), ("Giá vé", "thieu")]
    assert all("web" not in json.dumps(s, ensure_ascii=False) for s in nguon)


@pytest.mark.parametrize("chu", ["Lăng mở cho khách từ 7h đến 17h30", "Phố hoạt động từ 18h đến 22h", "Chùa đón khách cả ngày, nghỉ trưa 11h30–13h30",
                                 "Vào cổng tự do, không thu phí", "Điểm này không bán vé", "Phí tham quan 50.000/người", "Người lớn 150.000, trẻ em 30.000",
                                 "Trẻ dưới 7 tuổi không mất tiền vé", "Mở cửa từ 7h30", "Giá vé 50.000 đồng", "Vào cửa miễn phí",
                                 "Tham quan được từ 7:00 tới 17:30", "Bảo tàng đóng cửa thứ Hai hằng tuần"])
def test_loc_y_bo_y_noi_gio_mo_cua_hoac_gia_bang_loi_khac(chu):
    assert st.loc_y([{"chu": chu, "nguon": [1]}], {1}, 4) == ([], {"khong_nguon": 0, "qua_dai": 0, "gio_gia": 1, "qua_tran": 0, "chu": [("gio_gia", chu)]})


@pytest.mark.parametrize("chu", ["Có bãi gửi xe miễn phí cạnh cổng", "Mỗi năm đón hơn 2 triệu lượt khách", "Khuôn viên rộng hơn 12 nghìn m²", "Chợ mở từ thời Gia Long",
                                 "Bình minh 04h30 – 06h00 mặt đầm phủ sương", "Nên bắt đầu đi từ khoảng 17:30 để kịp hoàng hôn", "Lăng xây năm 1864, hoạt động từ năm 1883",
                                 "Quán từng có phòng trưng bày gốm sứ, nhưng nay đã đóng cửa vĩnh viễn", "Bảo tàng quản lý hơn 11.000 hiện vật triều Nguyễn",
                                 "Xe buýt hai tầng dừng ở Lăng Tự Đức nhưng vé xe không gồm vé vào cổng, du khách phải mua vé di tích riêng",
                                 "Nên dành 2 giờ tham quan và mang theo nước uống",
                                 "Đón hoàng hôn trên sông Hương từ cầu gỗ lim, nên bắt đầu tham quan từ khoảng 17:30"])
def test_loc_y_khong_bo_oan_y_chi_nhac_so_hoac_gio_trong_ngay(chu):
    assert st.loc_y([{"chu": chu, "nguon": [1]}], {1}, 4)[0] == [f"{chu} [1]"]


def test_y_gop_gio_voi_loi_dan_chi_bi_go_ve_noi_gio_gia():
    """Bài Chùa Từ Hiếu: "nhà chùa không niêm yết giờ mở cửa hay vé chính thức, nên đến vào ban ngày… mặc trang phục kín đáo…". Bản trước bỏ cả ý ⇒ mục
    "Lưu ý" ra ô thiếu trong khi bài có lời dặn."""
    cau = "Nhà chùa không niêm yết giờ mở cửa hay vé chính thức, nên đến vào ban ngày, mặc trang phục kín đáo và giữ yên lặng"
    giu, bo = st.loc_y([{"chu": cau, "nguon": [1]}], {1}, 3)
    assert giu == ["Nên đến vào ban ngày, mặc trang phục kín đáo và giữ yên lặng. [1]"]
    assert bo["gio_gia"] == 0 and bo["chu"] == [("gio_gia_cat", cau)]
    assert st.khoi_model("luu_y", [{"chu": cau, "nguon": [1]}], {1})[0]["kieu"] == "gach"
    assert st.go_ve_gio_gia("Hồ Lưu Khiêm có đảo Tịnh Khiêm, ba cầu đá") == "Hồ Lưu Khiêm có đảo Tịnh Khiêm, ba cầu đá"  # không có vế giờ / giá ⇒ nguyên văn
    assert st.go_ve_gio_gia("Vé người lớn 150.000 đồng, trẻ em 30.000") is None


def test_mot_muc_gap_loi_la_khong_lam_dut_luong_va_muc_truoc_khi_di_luon_con_dong_do_code():
    """Phiên đo: ngoại lệ không phải `GenerationError` / `RetrievalDependencyError` của MỘT mục từng làm cả luồng đóng không có `xong`, các mục chưa về mất,
    và nếu mục hỏng là "Trước khi đi" thì câu an toàn mất theo."""
    from api.routes import so_tay as r

    doan_kho = SimpleNamespace(id="a.md#0", text="chữ", metadata={"source": "a.md", "title": "A", "heading_path": ["Tổng quan"], "domain": "x",
                                                                  "evidence_parts": [{"role": "body", "text": "Hồ sen trước lăng", "start": 0, "end": 1}]})

    class Kho:
        def search(self, cau):
            if "Đầm Chuồn" in cau or "Đi lại" in cau:
                raise ValueError("lỗi lạ trong lúc tìm")
            return SimpleNamespace(documents=[doan_kho])

        def doan_cua_bai(self, rel):
            return []

    class May:
        async def viet_so_tay(self, loai, prompt, log):
            return {"nen_xem": [{"chu": "Hồ sen trước lăng", "nguon": [1]}], "luu_y": [], "di_lai": []}

    async def gom():
        return [e async for e in r._su_kien(st.dan_y(LICH), LICH, "Câu an toàn bão lũ", SimpleNamespace(retrieval_service=Kho()),
                                             SimpleNamespace(the_noi_bang=None, bang_lich_v2=None), May())]
    su_kien = [(k.split("event: ", 1)[1].split("\n", 1)[0], json.loads(k.split("data: ", 1)[1])) for k in (e.decode() for e in asyncio.run(gom()))]
    assert [t for t, _ in su_kien][0] == "dan_y" and [t for t, _ in su_kien][-1] == "xong" and sum(t == "muc" for t, _ in su_kien) == 4
    muc = {d["id"]: d for t, d in su_kien if t == "muc"}
    assert muc["n1-sang-1"]["trang_thai"] == "xong" and muc["n1-sang-1"]["doan"][-2]["gach"] == ["Hồ sen trước lăng"]
    assert muc["n2-sang-1"]["trang_thai"] == "loi" and [d["kieu"] for d in muc["n2-sang-1"]["doan"]] == ["thieu"]  # chỉ còn dòng do code (ô giờ)
    cuoi = muc["truoc-khi-di"]
    assert cuoi["trang_thai"] == "loi" and [d["chu"] for d in cuoi["doan"] if d["kieu"] == "an_toan"][0] == "Câu an toàn bão lũ" and cuoi["doan"][-1]["nhan"] == "Lưu ý chung"
    assert su_kien[-1][1]["so_muc_loi"] == 2
