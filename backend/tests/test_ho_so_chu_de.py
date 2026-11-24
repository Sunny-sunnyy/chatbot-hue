"""Công tắc `ho_so_chu_de` (bản thử, nhánh thu-b-ho-so-chu-de): danh sách chủ đề do code dựng, luật kiểm dàn ý, chọn ý phủ mọi bài, khối giờ / giá do code
chép, và luồng của đường API với kho + model giả. Không model thật, không Qdrant."""
import asyncio
import json
import re
from types import SimpleNamespace

import pytest

from llm import ho_so_chu_de as hs
from llm import the_noi as thn
from llm.assistant import AssistantFlags


def _b(rel, ten, tom_tat=""):
    return SimpleNamespace(rel=rel, tieu_de=ten, tom_tat=tom_tat)


LANG = [_b(f"heritages/heritage/Lăng {t}.md", f"Lăng {t}") for t in ("Gia Long", "Minh Mạng", "Thiệu Trị", "Tự Đức", "Khải Định")]
ML = LANG + [_b("heritages/heritage/Chùa Thiên Mụ.md", "Chùa Thiên Mụ"), _b("travel/places/Vịnh Lăng Cô.md", "Vịnh Lăng Cô"),
             _b("foods/restaurants/x.md", "Nhà hàng hải sản Làng Chài Lăng Cô")]


def test_danh_sach_chi_gom_chu_de_du_bai_va_tap_bai_do_luat_chon():
    ds = hs.danh_sach(ML)
    assert ds == [{"ma": "lang_tam", "ten": "Lăng tẩm các vua Nguyễn", "so_bai": 5, "bi_cat": False}]  # "Chùa" chỉ 1 bài ⇒ ẩn; Lăng Cô không phải lăng
    assert [b.tieu_de for b in hs.bai_cua(hs.CHU_DE[0], ML)] == [b.tieu_de for b in LANG]
    assert hs.danh_sach(LANG[:4]) == []  # dưới 5 bài ⇒ không còn chủ đề nào
    assert len({c.ma for c in hs.CHU_DE}) == len(hs.CHU_DE) and all(re.fullmatch(r"[a-z_]+", c.ma) for c in hs.CHU_DE)


def test_kiem_dan_y_moi_bai_dung_mot_muc_khong_bai_nao_bi_bo():
    muc = hs.kiem_dan_y([{"tieu_de": "Đầu triều", "bai": [1, 2, 9]}, {"tieu_de": "Trùng", "bai": [2]}, {"tieu_de": "Cuối triều", "bai": [4, 4]}], 5)
    assert muc == [{"tieu_de": "Đầu triều", "bai": [1, 2]}, {"tieu_de": "Cuối triều", "bai": [4]}, {"tieu_de": hs.MUC_KHAC, "bai": [3, 5]}]
    assert hs.kiem_dan_y([], 7) == [{"tieu_de": "", "bai": [1, 2, 3, 4, 5, 6]}, {"tieu_de": "", "bai": [7]}]  # model trả rỗng ⇒ code tự chia
    # mục quá `BAI_MOI_MUC` bài bị tách (một mục 14 bài = 28 đoạn trong một lời gọi); bài model bỏ sót cũng vậy
    to = hs.kiem_dan_y([{"tieu_de": "Tất cả", "bai": list(range(1, 15))}], 20)
    assert [(m["tieu_de"], len(m["bai"])) for m in to] == [("Tất cả", 6), ("Tất cả (tiếp)", 6), ("Tất cả (tiếp)", 2), (hs.MUC_KHAC, 6)]
    assert sorted(n for m in to for n in m["bai"]) == list(range(1, 21))
    # ra quá nhiều mục ⇒ bỏ dàn ý của model, code tự chia
    assert hs.kiem_dan_y([{"tieu_de": f"M{i}", "bai": [i]} for i in range(1, 12)], 11) == hs.chia_muc_du_phong(11)


def test_chon_y_moi_bai_co_it_nhat_mot_y_truoc_khi_lay_them():
    y = [f"Ý {i} về A [1]" for i in range(1, 8)] + ["Ý về B [2]", "Ý về A và C [1][3]"]
    giu, thieu = hs.chon_y_phu_bai(y, {1: "A", 2: "B", 3: "C", 4: "D"}, ["A", "B", "C", "D"])
    assert "Ý về B [2]" in giu and "Ý về A và C [1][3]" in giu and len(giu) == 6 and giu == sorted(giu, key=y.index)  # trần 6 (4 bài + 2), thứ tự gốc
    assert thieu == ["D"]  # bài không ý nào nói tới ⇒ ô thiếu mang tên bài
    assert hs.chon_y_phu_bai([], {1: "A"}, ["A"]) == ([], ["A"]) and hs.muc_do(2) == "mong" and hs.muc_do(3) == "du"


def test_dong_du_kien_chep_gio_va_gia_tu_the_noi():
    the = thn.Bang((thn.Noi("Lăng Gia Long", LANG[0].rel, re.compile("x"), ("Giờ mở cửa: 07h00 – 17h30.",), "| 2 | Lăng Gia Long | Phường | 150.000 | Miễn phí |", None),),
                   "travel/tickets/ve.md", "Vé tham quan", "| STT | Tên | Địa giới | Người lớn | Trẻ em |")
    doan, nguon = hs.dong_du_kien(LANG[:2], the, 7)
    assert doan == {"nhan": hs.NHAN_DU_KIEN, "kieu": "gach", "chu": None,
                    "gach": ["Lăng Gia Long — giờ mở cửa: 07h00 – 17h30; giá vé: người lớn 150.000 đồng · trẻ em 7–12 tuổi miễn phí [7][8]"]}
    assert [(s["id"], s["bai_id"]) for s in nguon] == [(7, LANG[0].rel), (8, "travel/tickets/ve.md")]
    assert hs.dong_du_kien(LANG[1:], the, 1) == (None, [])  # bài không có dòng nhãn ⇒ không có khối (không in ô thiếu ở hồ sơ)


def _doan(rel, so, chu):
    return SimpleNamespace(id=f"{rel}#{so}", text=chu, metadata={"source": rel, "title": rel.rsplit("/", 1)[-1][:-3], "heading_path": ["Tổng quan"], "domain": "x",
                                                                 "evidence_parts": [{"role": "body", "text": chu, "start": 0, "end": 1}]})


class _Kho:
    def doan_cua_bai(self, rel):
        return [_doan(rel, i, f"đoạn {i} của {rel}") for i in range(3)]


def _chay(may, dem):
    from api.routes import ho_so as r
    state = SimpleNamespace(retrieval_service=_Kho())
    flags = SimpleNamespace(the_noi_bang=None, muc_luc=ML)

    async def gom():
        return [e async for e in r._su_kien(hs.CHU_DE[0], LANG, state, flags, may, dem)]
    return [(k.split("event: ", 1)[1].split("\n", 1)[0], json.loads(k.split("data: ", 1)[1])) for k in (e.decode() for e in asyncio.run(gom()))]


def test_luong_ho_so_dan_y_roi_tung_muc_va_nho_dem_khi_tron_ven():
    class May:
        async def viet_so_tay(self, loai, prompt, log):
            if loai == "ho_so_dan_y":
                return {"muc": [{"tieu_de": "Đầu triều", "bai": [1, 2, 3]}, {"tieu_de": "Cuối triều", "bai": [4, 5]}]}
            # mục "Đầu triều": chỉ viết về hai bài đầu (nguồn 1 và 3 là đoạn của Lăng Gia Long, Lăng Minh Mạng) ⇒ Lăng Thiệu Trị phải ra ô thiếu
            return {"y": [{"chu": "Lăng Gia Long nằm giữa 42 ngọn núi", "nguon": [1]}, {"chu": "Lăng Minh Mạng đăng đối theo trục Thần đạo", "nguon": [5]},
                          {"chu": "Vé người lớn 150.000 đồng", "nguon": [1]}]} if "Đầu triều" in prompt else {"y": []}
    dem = {}
    sk = _chay(May(), dem)
    assert [t for t, _ in sk] == ["chu_de", "dan_y", "muc", "muc", "xong"]
    assert sk[0][1]["so_bai"] == 5 and [m["ten"] for m in sk[1][1]["muc"]] == ["Đầu triều", "Cuối triều"]
    muc = {d["id"]: d for t, d in sk if t == "muc"}
    assert muc["m1"]["doan"][0]["gach"] == ["Lăng Gia Long nằm giữa 42 ngọn núi", "Lăng Minh Mạng đăng đối theo trục Thần đạo"]  # ý nói giá bị bỏ, chữ sạch mã
    assert [(d["kieu"], d["nhan"], d.get("bai_id")) for d in muc["m1"]["doan"][1:]] == [("thieu", "Lăng Thiệu Trị", LANG[2].rel)] and muc["m1"]["muc_do"] == "mong"
    assert [d["kieu"] for d in muc["m2"]["doan"]] == ["thieu", "thieu"] and muc["m2"]["trang_thai"] == "xong"
    assert sk[-1][1]["tu_dem"] is False and sk[-1][1]["y_bi_bo"]["gio_gia"] == 1 and "lang_tam" in dem  # trọn vẹn ⇒ được nhớ
    assert sk[-1][1]["so_muc_du"] == 0 and sk[-1][1]["ban_ngan"] is True  # cả hai mục đều dưới 3 ý ⇒ hồ sơ tự nhận là bản ngắn
    assert json.loads(dem["lang_tam"][-1].decode().split("data: ", 1)[1])["tu_dem"] is True


def test_dan_y_hong_thi_code_tu_chia_va_mot_muc_loi_khong_dut_luong():
    class May:
        async def viet_so_tay(self, loai, prompt, log):
            raise RuntimeError("model hỏng")
    dem = {}
    sk = _chay(May(), dem)
    assert [t for t, _ in sk] == ["chu_de", "dan_y", "muc", "xong"] and sk[1][1]["muc"][0]["ten"].startswith("Lăng Gia Long, Lăng Minh Mạng")
    assert sk[2][1]["trang_thai"] == "loi" and sk[-1][1]["dan_y_do_code"] is True and sk[-1][1]["so_muc_loi"] == 1 and dem == {}  # bản hỏng không được nhớ


def test_cong_tac_mac_dinh_tat_va_can_muc_luc():
    assert AssistantFlags().ho_so_chu_de is False
    with pytest.raises(ValueError):
        AssistantFlags(ho_so_chu_de=True)


def _d(rel, so, muc, chu):
    return SimpleNamespace(id=f"{rel}#{so}", text=chu, metadata={"source": rel, "title": rel.rsplit("/", 1)[-1][:-3], "heading_path": [muc], "domain": "x",
                                                                 "evidence_parts": [{"role": "body", "text": chu, "start": 0, "end": 1}]})


def test_doan_canh_bao_chi_nhan_doan_co_dau_hieu_ro():
    bai = [_d("b.md", 0, "Tổng quan", "Bãi biển dài 5 km, cát trắng, mùa hè đông khách."),
           _d("b.md", 1, "Ẩm thực", "Hải sản tươi; mùa mưa bão ít quán mở."),                                    # một dấu hiệu lẻ, không thuộc nhóm cấm / biển động
           _d("b.md", 2, "Mùa mưa bão và biển động (tháng 9 đến tháng 12)", "Biển động, sóng lớn; chính quyền cấm tắm khi có áp thấp nhiệt đới."),
           _d("b.md", 3, "Lưu ý", "Không nên tắm xa bờ.")]
    assert hs.doan_canh_bao(bai).id == "b.md#2"                       # đoạn khớp nhiều nhóm dấu hiệu nhất
    assert hs.doan_canh_bao(bai[:2]) is None                          # "mùa mưa bão" đứng lẻ chưa đủ
    assert hs.doan_canh_bao([bai[3]]).id == "b.md#3"                  # một câu cấm tắm là đủ
    # ý dẫn đoạn cảnh báo: chỉ là Ý CẢNH BÁO khi có câu cấm / hai nhóm dấu hiệu / một dấu hiệu đi cùng lời dặn
    assert hs.la_y_canh_bao("Bãi biển Thuận An mùa mưa bão có sóng cao, phải tuân thủ lệnh cấm tắm [3]", {3})
    assert hs.la_y_canh_bao("Từ tháng 9 biển động, du khách nên hạn chế tắm biển [3]", {3})
    assert not hs.la_y_canh_bao("Dải cồn cát Lăng Cô là đê tự nhiên che chắn sóng lớn từ biển hở [3]", {3})
    assert not hs.la_y_canh_bao("Thời các chúa Nguyễn, sóng to và xoáy nước ở phá dễ lật thuyền nan [3]", {3})
    assert not hs.la_y_canh_bao("Mùa mưa bão biển động, cấm tắm [4]", {3})   # không dẫn đoạn cảnh báo ⇒ không tính


class _KhoBien:
    def doan_cua_bai(self, rel):
        return [_d(rel, 0, "Tổng quan", f"giới thiệu tổng quan {rel}"), _d(rel, 1, "Đặc điểm", "nổi bật đặc điểm lịch sử"),
                _d(rel, 2, "Mùa mưa bão và biển động", "Từ tháng 9 đến tháng 12 biển động, sóng lớn, chính quyền cấm tắm.")]


def _chay_bien(may):
    from api.routes import ho_so as r
    bai = [_b(f"travel/places/Bãi biển {t}.md", f"Bãi biển {t}") for t in ("A", "B", "C", "D", "E")]
    cd = next(c for c in hs.CHU_DE if c.ma == "bien_dam_pha")

    async def gom():
        return [e async for e in r._su_kien(cd, bai, SimpleNamespace(retrieval_service=_KhoBien()), SimpleNamespace(the_noi_bang=None, muc_luc=bai), may, {})]
    return [(k.split("event: ", 1)[1].split("\n", 1)[0], json.loads(k.split("data: ", 1)[1])) for k in (e.decode() for e in asyncio.run(gom()))]


def test_canh_bao_an_toan_cua_bai_luon_di_theo_ho_so():
    """Phiên đo đọc nhánh 24/11/2026: hồ sơ "Biển và đầm phá" 36 ý, 0 ý cảnh báo dù kho có (cấm tắm mùa mưa bão). Nay: đoạn cảnh báo của mỗi bài được đưa cho
    model; ý cảnh báo thành khối riêng "Lưu ý an toàn theo mùa"; bài nào model KHÔNG viết cảnh báo thì code tự thêm dòng trỏ tới mục cảnh báo của bài."""
    da_thay = {}

    class May:
        async def viet_so_tay(self, loai, prompt, log):
            if loai == "ho_so_dan_y":
                return {"muc": [{"tieu_de": "Các bãi biển", "bai": [1, 2, 3, 4, 5]}]}
            da_thay["prompt"] = prompt
            # 5 bài × (2 đoạn + 1 đoạn cảnh báo) ⇒ nguồn 3, 6, 9, 12, 15 là đoạn cảnh báo; model chỉ viết cảnh báo cho bài A (nguồn 3), và một ý thường dẫn nguồn 6
            return {"y": [{"chu": f"Bãi biển {t} có bãi cát dài", "nguon": [n]} for t, n in zip("ABCDE", (1, 4, 7, 10, 13))]
                    + [{"chu": "Bãi biển A: từ tháng 9 đến tháng 12 biển động, sóng lớn, chính quyền cấm tắm", "nguon": [3]},
                       {"chu": "Bãi biển B có khu cắm trại sát rừng dương", "nguon": [6]}]}  # dẫn đoạn cảnh báo nhưng không nói gì về an toàn ⇒ ý thường
    sk = _chay_bien(May())
    assert da_thay["prompt"].count("cấm tắm") == 5                    # đoạn cảnh báo của CẢ năm bài có trong bằng chứng
    muc = next(d for t, d in sk if t == "muc")
    thuong = next(d for d in muc["doan"] if d["kieu"] == "gach")
    assert len(thuong["gach"]) == 6 and all("cấm tắm" not in g for g in thuong["gach"])   # ý cảnh báo không lẫn trong danh sách thường
    an_toan = [(d["nhan"], d["chu"], d["so"]) for d in muc["doan"] if d["kieu"] == "an_toan"]
    assert an_toan[0] == (hs.NHAN_AN_TOAN, "Bãi biển A: từ tháng 9 đến tháng 12 biển động, sóng lớn, chính quyền cấm tắm", [3])   # ý cảnh báo model viết, có nguồn
    # bốn bài model không viết cảnh báo ⇒ code trỏ tới đúng mục cảnh báo của từng bài
    assert an_toan[1:] == [(None, hs.CAU_TRO_AN_TOAN.format(ten=f"Bãi biển {t}", muc="Mùa mưa bão và biển động"), [n]) for t, n in zip("BCDE", (6, 9, 12, 15))]
    assert next(d for t, d in sk if t == "xong")["so_dong_tro_an_toan"] == 4


def test_model_hong_thi_dong_tro_an_toan_van_co():
    class May:
        async def viet_so_tay(self, loai, prompt, log):
            if loai == "ho_so_dan_y":
                return {"muc": [{"tieu_de": "Các bãi biển", "bai": [1, 2, 3, 4, 5]}]}
            raise RuntimeError("model hỏng")
    muc = next(d for t, d in _chay_bien(May()) if t == "muc")
    assert muc["trang_thai"] == "loi" and len([d for d in muc["doan"] if d["kieu"] == "an_toan"]) == 5 and len(muc["nguon"]) == 5
