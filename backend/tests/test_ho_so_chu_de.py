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
    nhieu = hs.kiem_dan_y([{"tieu_de": f"M{i}", "bai": [i]} for i in range(1, 11)], 10)
    assert len(nhieu) == hs.SO_MUC_TOI_DA and nhieu[-1]["bai"] == [8, 9, 10]


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
