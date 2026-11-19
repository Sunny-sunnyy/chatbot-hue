"""Xuất lịch ra PowerPoint (plan private `data/xuat_lich_dep_2026-11-19/PLAN.md`): code điền đối tượng lịch đã dựng vào các trang; KHÔNG gọi model.

Hai lớp tách nhau để kiểm riêng:
- `trang_lich(lich, cau, …)` — hàm THUẦN: đối tượng lịch bản 2 (như giao diện nhận) + câu tả đã kiểm ⇒ danh sách trang (dict). Mọi chữ lấy từ lịch
  hoặc là hằng số ở file này; ngày dài ⇒ trang "tiếp", không bỏ điểm, không cắt tên / giờ (câu tả quá dài thì cắt ở ranh giới từ, thêm "…").
- `dung_pptx(trang, thu_muc_anh)` — vẽ các trang bằng `python-pptx` theo kiểu "Di sản" (chủ dự án chọn 19/11/2026 bằng ảnh mẫu). Vẽ bằng toạ độ,
  không dùng file khuôn nhị phân. Ảnh chỉ lấy từ thư mục ảnh tự host, chỉ ảnh có giấy phép ghi trong bảng ảnh (ảnh lấy từ trang web khác không
  có giấy phép ⇒ không vào file tải về; chỗ đó là ô hoạ tiết mang tên điểm).
"""
import datetime as dt
import io
import re
from pathlib import Path

TIEU_DE = "Lịch trình Huế {n} ngày"
DONG_THAY_DOI = "Giờ mở cửa, giá vé, lịch lễ hội có thể đã thay đổi — hãy kiểm lại với nơi đến trước khi đi."
DONG_DU_BAO = "Thời tiết: xem dự báo trước ngày đi; trời mưa lớn thì đổi điểm ngoài trời sang điểm trong nhà."
DONG_NGUON = "Thông tin lấy từ kho tư liệu của trợ lý du lịch Huế; lịch do chương trình xếp, câu mô tả đã đối chiếu nguồn."
TEN_BUOI = {"sang": "Sáng", "chieu": "Chiều", "toi": "Tối"}
THU = ("Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật")
MAP_PREFIX = "https://www.google.com/maps/search/"   # chỉ link bản đồ do code dựng mới được gắn vào file
_MA_NGUON = re.compile(r"\s*\[(?:Nguồn\s*)?\d+\]")
MUC_MOI_TRANG = 5            # số điểm tối đa trên một trang "ngày"
DONG_LUU_Y_MOI_TRANG = 6
CAU_TOI_DA = 170             # trần ký tự câu tả một điểm (câu thật dài nhất đã thấy: 109)
DIEM_CHINH_TREN_BIA = 4


def _anh_duoc_phep(anh: dict | None) -> dict | None:
    """Chỉ ảnh có tác giả + giấy phép (ảnh Wikimedia Commons) và nằm dưới `/anh/lich/`."""
    if anh and anh.get("giay_phep") and anh.get("tac_gia") and str(anh.get("src", "")).startswith("/anh/lich/"):
        return {"src": anh["src"], "tac_gia": anh["tac_gia"], "giay_phep": anh["giay_phep"]}
    return None


def _ngay_chu(ng: dict) -> str | None:
    if not ng.get("ngay_thang"):
        return None
    d = dt.date.fromisoformat(ng["ngay_thang"])
    return f"{THU[d.weekday()]} {d.day}/{d.month}/{d.year}"


def _gon(cau: str | None) -> str | None:
    """Câu tả đã bỏ mã nguồn [n]; quá `CAU_TOI_DA` ký tự ⇒ cắt ở ranh giới từ + "…" (tên, giờ, ghi chú không bao giờ bị cắt)."""
    chu = _MA_NGUON.sub("", cau or "").strip()
    if len(chu) <= CAU_TOI_DA:
        return chu or None
    return chu[:CAU_TOI_DA].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"


def trang_lich(lich: dict, cau: dict[str, str], muc_moi_trang: int = MUC_MOI_TRANG, ngay_tao: str | None = None) -> list[dict]:
    """Đối tượng lịch ⇒ các trang: bìa · mỗi ngày ≥ 1 trang (quá `muc_moi_trang` điểm ⇒ chia ĐỀU sang trang "tiếp") · lưu ý + bản đồ · nguồn ảnh."""
    ts = lich["tham_so"]
    tom_tat = lich["minh_hieu"].removeprefix("Mình hiểu: ").split(" — sai thì bấm")[0]
    moi_muc = [m for ng in lich["ngay"] for m in ng["muc"]]
    diem = [m for m in moi_muc if m["loai"] != "nghi"]
    anh_co = list({a["src"]: a for a in (_anh_duoc_phep(m.get("anh")) for m in moi_muc) if a}.values())   # theo thứ tự đi, không lặp
    trang = [{"kieu": "bia", "tieu_de": TIEU_DE.format(n=len(lich["ngay"])), "tom_tat": tom_tat, "anh": anh_co[:3], "so_diem": len(diem),
              "diem_chinh": [m["ten"] for m in diem if m["buoi"] != "toi"][:DIEM_CHINH_TREN_BIA], "ngay_tao": ngay_tao, "ngay_di": ts.get("ngay_di")}]
    da_dung: dict[str, dict] = {}
    for a in anh_co[:3]:   # ảnh bìa cũng phải có dòng nguồn
        da_dung[a["src"]] = {**a, "ten": next(m["ten"] for m in moi_muc if (m.get("anh") or {}).get("src") == a["src"])}
    for ng in lich["ngay"]:
        an = [{"bua": "Trưa" if a["bua"] == "trua" else "Tối", "gan": a["gan"], "quan": [q["ten"] for q in a["quan"]]}
              for a in (lich.get("an") or []) if a["ngay"] == ng["ngay"] and a.get("quan")]
        muc = []
        for m in ng["muc"]:
            anh = _anh_duoc_phep(m.get("anh"))
            if anh:
                da_dung.setdefault(anh["src"], {**anh, "ten": m["ten"]})
            muc.append({"buoi": TEN_BUOI[m["buoi"]], "ma_buoi": m["buoi"], "gio": m.get("gio"), "ten": m["ten"], "nghi": m["loai"] == "nghi",
                        "cau": _gon(cau.get(m["id_muc"])), "ghi_chu": m.get("ghi_chu"), "anh": anh})
        so_trang = max(1, -(-len(muc) // muc_moi_trang))
        moi = -(-len(muc) // so_trang) if muc else 1   # chia ĐỀU (6 điểm ⇒ 3 + 3, không 5 + 1) để không có trang gần trống
        cac = [muc[i:i + moi] for i in range(0, len(muc), moi)] or [[]]
        for k, phan in enumerate(cac):
            trang.append({"kieu": "ngay", "so": ng["ngay"], "tiep": k > 0, "ngay_chu": _ngay_chu(ng), "chang": " · ".join(ng.get("chang") or []),
                          "muc": phan, "an": an if k == len(cac) - 1 else []})
    luu_y = [g["cau"] for g in lich.get("ghi_chu") or [] if g.get("ma") != "du_bao"] + [DONG_DU_BAO, DONG_THAY_DOI, DONG_NGUON]
    ban_do = [{"ten": m["ten"], "url": m["map_url"]} for m in diem if str(m.get("map_url") or "").startswith(MAP_PREFIX)]
    for i in range(0, len(luu_y), DONG_LUU_Y_MOI_TRANG):
        cuoi = i + DONG_LUU_Y_MOI_TRANG >= len(luu_y)
        trang.append({"kieu": "luu_y", "tiep": i > 0, "dong": luu_y[i:i + DONG_LUU_Y_MOI_TRANG], "ban_do": ban_do if cuoi else []})
    if da_dung:
        trang.append({"kieu": "nguon_anh", "dong": [f"{a['ten']}: ảnh của {a['tac_gia']} — {a['giay_phep']} (Wikimedia Commons)" for a in da_dung.values()]})
    return trang


# ---------- vẽ: kiểu "Di sản" ----------
MAU = {"nen": "F8F4E9", "chu": "282923", "chinh": "49634D", "phu": "A75B43", "nhan": "B28739", "nhat": "EBE4D2", "hoa_tiet": "DDD3B8",
       "sang": "B28739", "chieu": "A75B43", "toi": "34495E", "trang": "FFFFFF"}   # ba màu cuối: chấm + nhãn theo buổi
PHONG_TD, PHONG = "Georgia", "Arial"   # hai phông có sẵn trên Windows / macOS / Google Slides (pptx không nhúng phông)
RONG, CAO = 13.333, 7.5   # inch, khổ 16:9


def dung_pptx(trang: list[dict], thu_muc_anh: Path) -> bytes:
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Inches, Pt

    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(RONG), Inches(CAO)

    def hop(s, x, y, w, h, ma, hinh=MSO_SHAPE.RECTANGLE, bo=None):
        sh = s.shapes.add_shape(hinh, Inches(x), Inches(y), Inches(w), Inches(h))
        sh.fill.solid()
        sh.fill.fore_color.rgb = RGBColor.from_string(MAU[ma])
        sh.line.fill.background()
        sh.shadow.inherit = False
        if bo is not None:
            sh.adjustments[0] = bo
        return sh

    def chu(s, x, y, w, h, doan, co=14, ma="chu", dam=False, phong=PHONG, can=PP_ALIGN.LEFT, giua=False, cach=0):
        """`doan`: chuỗi, hoặc danh sách (chuỗi, cỡ, màu, đậm[, link]) — mỗi phần tử một đoạn. Luôn bật xuống dòng trong ô."""
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.04)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE if giua else MSO_ANCHOR.TOP
        for i, d in enumerate([(doan, co, ma, dam)] if isinstance(doan, str) else doan):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = can
            if cach:
                p.space_after = Pt(cach)
            r = p.add_run()
            r.text = d[0]
            r.font.size, r.font.bold, r.font.name = Pt(d[1]), d[3], phong
            r.font.color.rgb = RGBColor.from_string(MAU[d[2]])
            if len(d) > 4 and d[4]:
                r.hyperlink.address = d[4]
        return tb

    def anh(s, a, x, y, w, h, ten=None):
        """Ảnh lấp đầy ô (cắt cho đúng tỉ lệ, không méo). Không có ảnh được phép / thiếu file ⇒ ô hoạ tiết (hai vòng tròn NẰM TRONG ô) mang tên điểm."""
        f = thu_muc_anh / a["src"].lstrip("/") if a else None
        if not f or not f.is_file():
            hop(s, x, y, w, h, "nhat")
            d = min(w, h) * 0.62
            hop(s, x + w - d - 0.06, y + h - d - 0.06, d, d, "hoa_tiet", MSO_SHAPE.OVAL)
            hop(s, x + 0.06, y + 0.06, d * 0.5, d * 0.5, "hoa_tiet", MSO_SHAPE.OVAL)
            if ten:
                chu(s, x + 0.05, y, w - 0.1, h, ten, 11, "chinh", True, PHONG_TD, PP_ALIGN.CENTER, True)
            return
        pic = s.shapes.add_picture(str(f), Inches(x), Inches(y))
        ti_anh, ti_o = pic.width / pic.height, w / h
        if ti_anh > ti_o:
            pic.crop_left = pic.crop_right = (1 - ti_o / ti_anh) / 2
        else:
            pic.crop_top = pic.crop_bottom = (1 - ti_anh / ti_o) / 2
        pic.left, pic.top, pic.width, pic.height = Inches(x), Inches(y), Inches(w), Inches(h)

    for so, t in enumerate(trang, start=1):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        hop(s, 0, 0, RONG, CAO, "nen")
        if t["kieu"] == "bia":
            hop(s, 0, 0, 5.2, CAO, "chinh")
            hop(s, 0.6, 1.0, 0.9, 0.07, "nhan")
            chu(s, 0.6, 1.2, 4.2, 2.2, t["tieu_de"], 42, "nen", True, PHONG_TD)
            chu(s, 0.6, 3.45, 4.2, 0.9, t["tom_tat"], 17, "nhat")
            if t["diem_chinh"]:
                chu(s, 0.6, 4.4, 4.2, 1.5, [(ten, 14, "nen", False) for ten in t["diem_chinh"]], cach=3)
            chu(s, 0.6, 6.2, 4.2, 0.8, [(f"{t['so_diem']} điểm tham quan", 15, "nhan", True)]
                + ([(f"Tạo ngày {t['ngay_tao']}", 11, "nhat", False)] if t["ngay_tao"] else []))
            a = t["anh"] + [None] * (3 - len(t["anh"]))
            anh(s, a[0], 5.6, 0.6, 7.15, 4.05)                       # một ảnh lớn + hai ảnh nhỏ (ảnh gốc ~640 px: không phóng tràn trang)
            anh(s, a[1], 5.6, 4.8, 3.5, 2.1)
            anh(s, a[2], 9.25, 4.8, 3.5, 2.1)
        elif t["kieu"] == "ngay":
            hop(s, 0, 0, 2.5, CAO, "chinh")
            hop(s, 0.3, 0.55, 0.7, 0.06, "nhan")
            chu(s, 0.3, 0.7, 1.9, 1.3, f"Ngày {t['so']}" + (" (tiếp)" if t["tiep"] else ""), 32, "nen", True, PHONG_TD)
            chu(s, 0.3, 2.1, 1.9, 2.4, " — ".join(x for x in (t["ngay_chu"], t["chang"]) if x), 13, "nhat")
            n = max(len(t["muc"]), 1)
            day = 5.15 if t["an"] else 6.15                          # chiều cao dành cho các điểm (chừa chỗ khối "Ăn gần đó")
            cao_hang = min(1.95, day / n)
            to = cao_hang >= 1.5                                      # ít điểm ⇒ ảnh + chữ to hơn, lấp trang
            rong_anh = 2.6 if to else 1.85
            hop(s, 3.27, 0.75, 0.04, cao_hang * (n - 1) + 0.2, "nhat")   # trục thời gian
            for i, m in enumerate(t["muc"]):
                y = 0.55 + i * cao_hang
                hop(s, 3.12, y + 0.1, 0.34, 0.34, m["ma_buoi"], MSO_SHAPE.OVAL)
                hop(s, 3.7, y + 0.06, 0.95, 0.34, m["ma_buoi"], MSO_SHAPE.ROUNDED_RECTANGLE, 0.5)
                chu(s, 3.7, y + 0.06, 0.95, 0.34, m["buoi"], 12, "trang", True, can=PP_ALIGN.CENTER, giua=True)
                chu(s, 3.66, y + 0.45, 1.75, 0.5, m["gio"] or "", 14 if to else 13, "chu", True)
                anh(s, m["anh"], 5.5, y, rong_anh, cao_hang - 0.2, m["ten"])
                dong = [(m["ten"], 21 if to else 17, "chinh", True)] + ([(m["cau"], 14 if to else 12, "chu", False)] if m["cau"] else []) \
                    + ([(m["ghi_chu"], 12 if to else 11, "phu", False)] if m["ghi_chu"] else [])
                chu(s, 5.7 + rong_anh, y - 0.04, RONG - 6.2 - rong_anh, cao_hang - 0.1, dong, cach=2)
            if t["an"]:
                hop(s, 3.1, 5.85, RONG - 3.6, 1.05, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.12)
                hop(s, 3.1, 5.85, 0.1, 1.05, "phu")
                chu(s, 3.35, 5.9, 1.6, 0.95, "Ăn gần đó", 14, "phu", True, PHONG_TD, giua=True)
                chu(s, 4.95, 5.9, RONG - 5.6, 0.95, [(f"{a['bua']} gần {a['gan']}: " + ", ".join(a["quan"]), 12, "chu", False) for a in t["an"]],
                    giua=True, cach=2)
        else:
            la_luu_y = t["kieu"] == "luu_y"
            hop(s, 0, 0, RONG, 1.15, "chinh")
            hop(s, 0.6, 1.15, 1.2, 0.07, "nhan")
            chu(s, 0.6, 0.18, 10, 0.8, ("Lưu ý trước khi đi" + (" (tiếp)" if t.get("tiep") else "")) if la_luu_y else "Nguồn ảnh", 30, "nen", True,
                PHONG_TD, giua=True)
            ban_do = t.get("ban_do") or []
            rong_trai = 7.4 if ban_do else RONG - 1.6
            chu(s, 0.8, 1.55, rong_trai, 5.2, [("•  " + d, 15 if la_luu_y else 13, "chu", False) for d in t["dong"]], cach=9)
            if ban_do:
                hop(s, 8.6, 1.55, 4.15, 5.2, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.05)
                chu(s, 8.8, 1.65, 3.8, 0.5, "Mở bản đồ từng điểm", 15, "phu", True, PHONG_TD)
                co = 12 if len(ban_do) <= 12 else 10
                chu(s, 8.8, 2.2, 3.8, 4.4, [(d["ten"], co, "chinh", False, d["url"]) for d in ban_do], cach=3)
        chu(s, 0.6, CAO - 0.42, RONG - 1.2, 0.3, f"Lịch trình Huế · trang {so}", 10, "phu", can=PP_ALIGN.RIGHT)
    out = io.BytesIO()
    prs.save(out)
    return out.getvalue()
