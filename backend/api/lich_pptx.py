"""Xuất lịch ra PowerPoint (plan private `data/xuat_lich_dep_2026-11-19/PLAN.md`): code điền đối tượng lịch đã dựng vào các trang; KHÔNG gọi model.

Hai lớp tách nhau để kiểm riêng:
- `trang_lich(lich, cau, …)` — hàm THUẦN: đối tượng lịch bản 2 (như giao diện nhận) + câu tả đã kiểm ⇒ danh sách trang (dict). Mọi chữ lấy từ lịch
  hoặc là hằng số ở file này; ngày dài ⇒ trang "tiếp", không bỏ điểm, không cắt tên / giờ.
- `dung_pptx(trang, kieu, thu_muc_anh)` — vẽ các trang bằng `python-pptx` theo một trong các KIỂU (bảng màu + bố cục). Ảnh chỉ lấy từ thư mục ảnh
  tự host, chỉ ảnh có giấy phép ghi trong bảng ảnh (ảnh lấy từ trang web khác không có giấy phép ⇒ không vào file tải về).
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
_MA_NGUON = re.compile(r"\s*\[(?:Nguồn\s*)?\d+\]")
MUC_MOI_TRANG = {"di_san": 5, "song_huong": 5}   # số điểm tối đa trên một trang "ngày" của từng kiểu
DONG_LUU_Y_MOI_TRANG = 7


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


def trang_lich(lich: dict, cau: dict[str, str], muc_moi_trang: int = 5, ngay_tao: str | None = None) -> list[dict]:
    """Đối tượng lịch ⇒ các trang: bìa · mỗi ngày ≥ 1 trang (quá `muc_moi_trang` điểm ⇒ trang "tiếp") · lưu ý + nguồn · nguồn ảnh (khi có ảnh)."""
    ts = lich["tham_so"]
    tom_tat = lich["minh_hieu"].removeprefix("Mình hiểu: ").split(" — sai thì bấm")[0]
    moi_muc = [m for ng in lich["ngay"] for m in ng["muc"]]
    anh_co = list({a["src"]: a for a in (_anh_duoc_phep(m.get("anh")) for m in moi_muc) if a}.values())   # theo thứ tự đi, không lặp
    anh_bia = anh_co[0] if anh_co else None
    trang = [{"kieu": "bia", "tieu_de": TIEU_DE.format(n=len(lich["ngay"])), "tom_tat": tom_tat, "anh": anh_bia, "anh_dai": anh_co[:3],
              "so_diem": sum(m["loai"] != "nghi" for m in moi_muc), "ngay_tao": ngay_tao, "ngay_di": ts.get("ngay_di")}]
    da_dung: dict[str, dict] = {}
    for a in anh_co[:3]:   # ảnh bìa (kiểu một ảnh dùng ảnh đầu, kiểu dải ảnh dùng tới ba) cũng phải có dòng nguồn
        da_dung[a["src"]] = {**a, "ten": next(m["ten"] for m in moi_muc if (m.get("anh") or {}).get("src") == a["src"])}
    for ng in lich["ngay"]:
        an = [f"{'Trưa' if a['bua'] == 'trua' else 'Tối'} gần {a['gan']}: " + ", ".join(q["ten"] for q in a["quan"])
              for a in (lich.get("an") or []) if a["ngay"] == ng["ngay"] and a.get("quan")]
        muc = []
        for m in ng["muc"]:
            anh = _anh_duoc_phep(m.get("anh"))
            if anh:
                da_dung.setdefault(anh["src"], {**anh, "ten": m["ten"]})
            muc.append({"buoi": TEN_BUOI[m["buoi"]], "gio": m.get("gio"), "ten": m["ten"], "nghi": m["loai"] == "nghi",
                        "cau": _MA_NGUON.sub("", cau.get(m["id_muc"], "")).strip() or None, "ghi_chu": m.get("ghi_chu"), "anh": anh})
        so_trang = max(1, -(-len(muc) // muc_moi_trang))
        moi = -(-len(muc) // so_trang) if muc else 1   # chia ĐỀU giữa các trang (6 điểm ⇒ 3 + 3, không 5 + 1) để không có trang gần trống
        cac = [muc[i:i + moi] for i in range(0, len(muc), moi)] or [[]]
        for k, phan in enumerate(cac):
            trang.append({"kieu": "ngay", "so": ng["ngay"], "tiep": k > 0, "ngay_chu": _ngay_chu(ng), "chang": " · ".join(ng.get("chang") or []),
                          "muc": phan, "an": an if k == len(cac) - 1 else []})
    luu_y = [g["cau"] for g in lich.get("ghi_chu") or [] if g.get("ma") != "du_bao"] + [DONG_DU_BAO, DONG_THAY_DOI, DONG_NGUON]
    for i in range(0, len(luu_y), DONG_LUU_Y_MOI_TRANG):
        trang.append({"kieu": "luu_y", "tiep": i > 0, "dong": luu_y[i:i + DONG_LUU_Y_MOI_TRANG]})
    if da_dung:
        trang.append({"kieu": "nguon_anh", "dong": [f"{a['ten']}: ảnh của {a['tac_gia']} — {a['giay_phep']} (Wikimedia Commons)" for a in da_dung.values()]})
    return trang


# ---------- vẽ ----------
KIEU = {
    "di_san": {"ten": "Di sản", "nen": "F8F4E9", "chu": "282923", "chinh": "49634D", "phu": "A75B43", "nhan": "B28739", "nhat": "EBE4D2",
               "phong_td": "Georgia", "phong": "Arial"},
    "song_huong": {"ten": "Sông Hương", "nen": "FFFFFF", "chu": "1E2A38", "chinh": "1F3A5F", "phu": "2A9D8F", "nhan": "E76F51", "nhat": "EEF3F7",
                   "phong_td": "Arial", "phong": "Arial"},
}
RONG, CAO = 13.333, 7.5   # inch, khổ 16:9


def dung_pptx(trang: list[dict], kieu: str, thu_muc_anh: Path) -> bytes:
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Inches, Pt

    k = KIEU[kieu]
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(RONG), Inches(CAO)

    def mau(ma):
        return RGBColor.from_string(k[ma] if ma in k else ma)

    def hop(s, x, y, w, h, ma, hinh=MSO_SHAPE.RECTANGLE):
        sh = s.shapes.add_shape(hinh, Inches(x), Inches(y), Inches(w), Inches(h))
        sh.fill.solid()
        sh.fill.fore_color.rgb = mau(ma)
        sh.line.fill.background()
        sh.shadow.inherit = False
        return sh

    def chu(s, x, y, w, h, doan, co=14, ma="chu", dam=False, phong=None, can=PP_ALIGN.LEFT, giua=False):
        """`doan`: chuỗi hoặc danh sách (chuỗi, cỡ, màu, đậm) — mỗi phần tử một đoạn. Luôn bật xuống dòng trong ô."""
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.04)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE if giua else MSO_ANCHOR.TOP
        for i, d in enumerate([(doan, co, ma, dam)] if isinstance(doan, str) else doan):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = can
            r = p.add_run()
            r.text = d[0]
            r.font.size, r.font.bold, r.font.name = Pt(d[1]), d[3], phong or k["phong"]
            r.font.color.rgb = mau(d[2])
        return tb

    def anh(s, a, x, y, w, h):
        """Ảnh lấp đầy ô (cắt hai bên / trên dưới cho đúng tỉ lệ, không méo). Thiếu file / không có ảnh ⇒ ô màu."""
        f = thu_muc_anh / a["src"].lstrip("/") if a else None
        if not f or not f.is_file():
            hop(s, x, y, w, h, "nhat")
            return
        pic = s.shapes.add_picture(str(f), Inches(x), Inches(y))
        ti_anh, ti_o = pic.width / pic.height, w / h
        if ti_anh > ti_o:
            pic.crop_left = pic.crop_right = (1 - ti_o / ti_anh) / 2
        else:
            pic.crop_top = pic.crop_bottom = (1 - ti_anh / ti_o) / 2
        pic.left, pic.top, pic.width, pic.height = Inches(x), Inches(y), Inches(w), Inches(h)

    def nen(s):
        hop(s, 0, 0, RONG, CAO, "nen")

    def chan(s, so):
        chu(s, 0.6, CAO - 0.42, RONG - 1.2, 0.3, f"Lịch trình Huế · trang {so}", 10, "phu", can=PP_ALIGN.RIGHT)

    for so, t in enumerate(trang, start=1):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        nen(s)
        if t["kieu"] == "bia":
            if kieu == "di_san":
                hop(s, 0, 0, 5.2, CAO, "chinh")
                anh(s, t["anh"], 5.6, 0.9, 7.1, 5.0)
                hop(s, 5.6, 6.05, 7.1, 0.08, "nhan")
                chu(s, 0.6, 1.5, 4.2, 2.4, t["tieu_de"], 40, "nen", True, k["phong_td"])
                chu(s, 0.6, 4.0, 4.2, 1.4, t["tom_tat"], 16, "nhat")
                chu(s, 0.6, 5.6, 4.2, 0.9, [(f"{t['so_diem']} điểm tham quan", 14, "nhan", True)] + ([(f"Tạo ngày {t['ngay_tao']}", 11, "nhat", False)] if t["ngay_tao"] else []))
            else:
                dai = t["anh_dai"] or [None]
                rong_anh = RONG / len(dai)
                for i, a in enumerate(dai):   # ảnh nguồn nhỏ (~640 px): một ảnh tràn ngang bị nhoè ⇒ dải tới ba ảnh
                    anh(s, a, i * rong_anh, 0, rong_anh - (0.06 if i < len(dai) - 1 else 0), 4.3)
                hop(s, 0, 4.3, RONG, 0.12, "phu")
                chu(s, 0.8, 4.65, 11.7, 1.1, t["tieu_de"], 44, "chinh", True)
                chu(s, 0.8, 5.75, 8.5, 0.6, t["tom_tat"], 18, "chu")
                hop(s, 9.9, 5.7, 2.6, 0.7, "nhan", MSO_SHAPE.ROUNDED_RECTANGLE)
                chu(s, 9.9, 5.7, 2.6, 0.7, f"{t['so_diem']} điểm tham quan", 15, "FFFFFF", True, can=PP_ALIGN.CENTER, giua=True)
                if t["ngay_tao"]:
                    chu(s, 0.8, 6.45, 8, 0.4, f"Tạo ngày {t['ngay_tao']}", 11, "phu")
        elif t["kieu"] == "ngay":
            tieu = f"Ngày {t['so']}" + (" (tiếp)" if t["tiep"] else "")
            phu = " — ".join(x for x in (t["ngay_chu"], t["chang"]) if x)
            if kieu == "di_san":
                hop(s, 0, 0, 2.5, CAO, "chinh")
                chu(s, 0.3, 0.7, 1.9, 1.3, tieu, 32, "nen", True, k["phong_td"])
                chu(s, 0.3, 2.1, 1.9, 2.2, phu, 13, "nhat")
                cao_hang = min(1.45, 5.75 / max(len(t["muc"]), 1))
                hop(s, 3.25, 0.7, 0.05, cao_hang * len(t["muc"]) - 0.25, "nhan")   # trục thời gian
                for i, m in enumerate(t["muc"]):
                    y = 0.6 + i * cao_hang
                    hop(s, 3.13, y + 0.12, 0.29, 0.29, "phu", MSO_SHAPE.OVAL)
                    chu(s, 3.65, y, 2.0, 0.5, [(m["buoi"], 11, "phu", True), (m["gio"] or "", 13, "chu", True)])
                    anh(s, m["anh"], 5.7, y, 1.75, cao_hang - 0.22)
                    dong = [(m["ten"], 17, "chinh", True)] + ([(m["cau"], 12, "chu", False)] if m["cau"] else []) \
                        + ([(m["ghi_chu"], 11, "phu", False)] if m["ghi_chu"] else [])
                    chu(s, 7.65, y - 0.03, 5.2, cao_hang - 0.1, dong, phong=None)
                if t["an"]:
                    chu(s, 3.65, 6.4, 9.2, 0.6, [("Ăn gần đó — " + " · ".join(t["an"]), 11, "phu", False)])
            else:
                hop(s, 0, 0, RONG, 1.15, "chinh")
                chu(s, 0.6, 0.18, 4.5, 0.8, tieu, 30, "FFFFFF", True, giua=True)
                chu(s, 5.1, 0.18, 7.6, 0.8, phu, 14, "nhat", can=PP_ALIGN.RIGHT, giua=True)
                n = max(len(t["muc"]), 1)
                rong_the = (RONG - 1.2 - 0.3 * (n - 1)) / n if n > 2 else 3.8
                x0 = (RONG - (rong_the * n + 0.3 * (n - 1))) / 2
                for i, m in enumerate(t["muc"]):
                    x = x0 + i * (rong_the + 0.3)
                    the = hop(s, x, 1.5, rong_the, 4.35, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE)
                    the.adjustments[0] = 0.04
                    anh(s, m["anh"], x + 0.12, 1.62, rong_the - 0.24, 1.7)
                    hop(s, x + 0.12, 3.42, min(1.9, rong_the - 0.24), 0.38, "phu", MSO_SHAPE.ROUNDED_RECTANGLE)
                    chu(s, x + 0.12, 3.42, min(1.9, rong_the - 0.24), 0.38, f"{m['buoi']} {m['gio'] or ''}".strip(), 11, "FFFFFF", True, can=PP_ALIGN.CENTER, giua=True)
                    dong = [(m["ten"], 15, "chinh", True)] + ([(m["cau"], 11, "chu", False)] if m["cau"] else []) \
                        + ([(m["ghi_chu"], 10, "nhan", False)] if m["ghi_chu"] else [])
                    chu(s, x + 0.12, 3.88, rong_the - 0.24, 1.9, dong)
                if t["an"]:
                    chu(s, 0.6, 6.2, RONG - 1.2, 0.6, [("Ăn gần đó — " + " · ".join(t["an"]), 11, "chinh", False)])
        else:
            tieu = ("Lưu ý trước khi đi" + (" (tiếp)" if t.get("tiep") else "")) if t["kieu"] == "luu_y" else "Nguồn ảnh"
            hop(s, 0, 0, RONG, 1.15, "chinh")
            chu(s, 0.6, 0.18, 10, 0.8, tieu, 30, "nen" if kieu == "di_san" else "FFFFFF", True, k["phong_td"], giua=True)
            co = 15 if t["kieu"] == "luu_y" else 12
            tb = chu(s, 0.8, 1.5, RONG - 1.6, 5.2, [("•  " + d, co, "chu", False) for d in t["dong"]])
            for doan in tb.text_frame.paragraphs:
                doan.space_after = Pt(10)
        chan(s, so)
    out = io.BytesIO()
    prs.save(out)
    return out.getvalue()
