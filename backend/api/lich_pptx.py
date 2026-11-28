"""Xuất lịch ra PowerPoint (plan private `data/xuat_lich_dep_2026-11-19/PLAN.md`): code điền đối tượng lịch đã dựng vào các trang; KHÔNG gọi model.

Hai lớp tách nhau để kiểm riêng:
- `trang_lich(lich, cau, …)` — hàm THUẦN: đối tượng lịch bản 2 (như giao diện nhận) + câu tả đã kiểm ⇒ danh sách trang (dict). Mọi chữ lấy từ lịch
  hoặc là hằng số ở file này; ngày dài ⇒ trang "tiếp", không bỏ điểm, không cắt tên / giờ (câu tả quá dài thì cắt ở ranh giới từ, thêm "…").
- `dung_pptx(trang, thu_muc_anh)` — vẽ các trang bằng `python-pptx` theo kiểu "Di sản" (chủ dự án chọn 19/11/2026 bằng ảnh mẫu). Vẽ bằng toạ độ,
  không dùng file khuôn nhị phân. Ảnh = ảnh tự host của bảng ảnh đang chạy (mọi ảnh giao diện đang hiện); điểm không có ảnh ⇒ ô hoạ tiết mang tên
  điểm. KHÔNG in tác giả / giấy phép / trang nguồn ảnh ở đâu trong file (chủ dự án 14/11/2026: gỡ mọi chữ ghi công khỏi hệ thống; nhắc lại 19/11).
- Câu AN TOÀN của lượt (bão / lũ: bản tin chính thức + 112) nếu có ⇒ in ở bìa và là dòng ĐẦU trang "Lưu ý trước khi đi".
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
DONG_LUU_Y_MOI_TRANG = 8
DONG_BAN_DO = "Bấm tên điểm để mở bản đồ."
DONG_SUA_FILE = "File này sửa được: đổi chữ, thêm ảnh của bạn trước khi gửi cho người đi cùng."
CAU_TOI_DA = 170             # trần ký tự câu tả một điểm (câu thật dài nhất đã thấy: 109)
DIEM_CHINH_TREN_BIA = 4


ANH_LICH = "/anh/lich/"


def _anh_hop_le(anh: dict | None) -> dict | None:
    """Ảnh tự host của bảng ảnh: `src` ngay dưới `/anh/lich/` (không thư mục con, không "..") — cùng luật với giao diện. Chỉ giữ `src`."""
    src = str((anh or {}).get("src") or "")
    if src.startswith(ANH_LICH) and "/" not in src[len(ANH_LICH):] and ".." not in src:
        return {"src": src}
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


def trang_lich(lich: dict, cau: dict[str, str], muc_moi_trang: int = MUC_MOI_TRANG, ngay_tao: str | None = None, an_toan: str | None = None) -> list[dict]:
    """Đối tượng lịch ⇒ các trang: bìa · mỗi ngày ≥ 1 trang (quá `muc_moi_trang` điểm ⇒ chia ĐỀU sang trang "tiếp") · lưu ý + bản đồ.
    `an_toan` = câu an toàn của lượt đã lưu cùng lịch (hằng số của code), None khi lượt không có."""
    ts = lich["tham_so"]
    tom_tat = lich["minh_hieu"].removeprefix("Mình hiểu: ").split(" — sai thì bấm")[0]
    moi_muc = [m for ng in lich["ngay"] for m in ng["muc"]]
    diem = [m for m in moi_muc if m["loai"] != "nghi"]
    anh_co = list({a["src"]: a for a in (_anh_hop_le(m.get("anh")) for m in moi_muc) if a}.values())   # theo thứ tự đi, không lặp
    trang = [{"kieu": "bia", "tieu_de": TIEU_DE.format(n=len(lich["ngay"])), "tom_tat": tom_tat, "anh": anh_co[:3], "so_diem": len(diem),
              "diem_chinh": [m["ten"] for m in diem if m["buoi"] != "toi"][:DIEM_CHINH_TREN_BIA], "ngay_tao": ngay_tao, "ngay_di": ts.get("ngay_di"), "an_toan": an_toan}]
    for ng in lich["ngay"]:
        an = [{"bua": "Trưa" if a["bua"] == "trua" else "Tối", "gan": a["gan"], "quan": [q["ten"] for q in a["quan"]]}
              for a in (lich.get("an") or []) if a["ngay"] == ng["ngay"] and a.get("quan")]
        muc = []
        for m in ng["muc"]:
            anh = _anh_hop_le(m.get("anh"))
            muc.append({"buoi": TEN_BUOI[m["buoi"]], "ma_buoi": m["buoi"], "gio": m.get("gio"), "ten": m["ten"], "nghi": m["loai"] == "nghi",
                        "cau": _gon(cau.get(m["id_muc"])), "ghi_chu": m.get("ghi_chu"), "anh": anh})
        so_trang = max(1, -(-len(muc) // muc_moi_trang))
        moi = -(-len(muc) // so_trang) if muc else 1   # chia ĐỀU (6 điểm ⇒ 3 + 3, không 5 + 1) để không có trang gần trống
        cac = [muc[i:i + moi] for i in range(0, len(muc), moi)] or [[]]
        for k, phan in enumerate(cac):
            trang.append({"kieu": "ngay", "so": ng["ngay"], "tiep": k > 0, "ngay_chu": _ngay_chu(ng), "chang": " · ".join(ng.get("chang") or []),
                          "muc": phan, "an": an if k == len(cac) - 1 else []})
    luu_y = ([an_toan] if an_toan else []) + [g["cau"] for g in lich.get("ghi_chu") or [] if g.get("ma") != "du_bao"] + [DONG_DU_BAO, DONG_THAY_DOI, DONG_NGUON]
    ban_do = [{"ten": m["ten"], "url": m["map_url"]} for m in diem if str(m.get("map_url") or "").startswith(MAP_PREFIX)]
    for i in range(0, len(luu_y), DONG_LUU_Y_MOI_TRANG):
        cuoi = i + DONG_LUU_Y_MOI_TRANG >= len(luu_y)
        trang.append({"kieu": "luu_y", "tiep": i > 0, "dong": luu_y[i:i + DONG_LUU_Y_MOI_TRANG], "ban_do": ban_do if cuoi else [],
                      "an_toan": bool(an_toan) and i == 0})   # dòng đầu của trang đầu là câu an toàn ⇒ vẽ nổi
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
            thap = 0.95 if t["an_toan"] else 0                       # có câu an toàn ⇒ ảnh thấp lại, chừa một dải dưới cùng cho câu đó
            anh(s, a[0], 5.6, 0.6, 7.15, 4.05 - thap * 0.5)          # một ảnh lớn + hai ảnh nhỏ (ảnh gốc ~640 px: không phóng tràn trang)
            anh(s, a[1], 5.6, 4.8 - thap * 0.5, 3.5, 2.1 - thap * 0.5)
            anh(s, a[2], 9.25, 4.8 - thap * 0.5, 3.5, 2.1 - thap * 0.5)
            if t["an_toan"]:
                hop(s, 5.6, 6.02, 7.15, 0.9, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.1)
                hop(s, 5.6, 6.02, 0.1, 0.9, "phu")
                chu(s, 5.8, 6.04, 6.85, 0.86, t["an_toan"], 10.5, "chu", True, giua=True)
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
                if m["nghi"]:   # "tối nghỉ" là một câu do code viết, không phải điểm tham quan ⇒ không ô ảnh, chữ thường, chạy hết bề ngang
                    chu(s, 5.5, y + 0.02, RONG - 6.0, cao_hang - 0.1, m["ten"], 14 if to else 13, "chu")
                    continue
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
            hop(s, 0, 0, RONG, 1.15, "chinh")
            hop(s, 0.6, 1.15, 1.2, 0.07, "nhan")
            chu(s, 0.6, 0.18, 10, 0.8, "Lưu ý trước khi đi" + (" (tiếp)" if t.get("tiep") else ""), 30, "nen", True, PHONG_TD, giua=True)
            ban_do = t.get("ban_do") or []
            rong_trai = 7.4 if ban_do else RONG - 1.6
            co = 15 if len(t["dong"]) <= 6 else 13
            chu(s, 0.8, 1.55, rong_trai, 5.2, [("•  " + d, co, "phu" if t.get("an_toan") and i == 0 else "chu", bool(t.get("an_toan")) and i == 0)
                                               for i, d in enumerate(t["dong"])], cach=9 if len(t["dong"]) <= 6 else 6)
            if ban_do:
                hop(s, 8.6, 1.55, 4.15, 5.2, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.05)
                chu(s, 8.8, 1.65, 3.8, 0.5, "Mở bản đồ từng điểm", 16, "phu", True, PHONG_TD)
                # mỗi tên một ô chữ riêng, link gắn vào Ô (không vào chữ) ⇒ chữ giữ màu của kiểu thay vì màu xanh mặc định của link
                cao_dong = min(0.42, 3.55 / len(ban_do))
                for i, d in enumerate(ban_do):
                    o = chu(s, 8.8, 2.2 + i * cao_dong, 3.8, cao_dong, d["ten"], 14 if cao_dong >= 0.36 else 11, "phu", giua=True)
                    o.text_frame.paragraphs[0].runs[0].font.underline = True
                    o.click_action.hyperlink.address = d["url"]
                chu(s, 8.8, 5.85, 3.8, 0.85, [(DONG_BAN_DO, 11, "chu", False), (DONG_SUA_FILE, 11, "chu", False)], cach=2)
        chu(s, 0.6, CAO - 0.42, RONG - 1.2, 0.3, f"Lịch trình Huế · trang {so}", 10, "phu", can=PP_ALIGN.RIGHT)
    out = io.BytesIO()
    prs.save(out)
    return out.getvalue()

# =====================================================================================================================================
# Đợt 5 — Phần A: `.pptx` v2 (3 bảng màu · 9 layout · `pptx_fit` 3 tầng · center-crop Pillow · 0 chữ ghi công ảnh)
# =====================================================================================================================================

DISCLAIMER_O_DAU = "Gợi ý theo vị trí và hạng — chưa kiểm giá, phòng trống."
_MUC_TOI_DA_V2 = 6  # ngày > 6 điểm tự tách thành Phần 1 / Phần 2 để không bóp khung chữ


def _ten_ngay_vn(ng: dict) -> str:
    chu = _ngay_chu(ng)
    return f"Ngày {ng['ngay']} · {chu}" if chu else f"Ngày {ng['ngay']}"


def _muc_chuan_v2(m: dict, copy_override: str | None = None) -> dict:
    anh_src = None
    if isinstance(m.get("anh"), dict) and m["anh"].get("src"):
        a = _anh_hop_le(m["anh"])
        anh_src = a["src"] if a else None
    cau = copy_override if copy_override is not None else m.get("cau")
    return {
        "id_muc": m.get("id_muc"),
        "buoi": TEN_BUOI.get(m.get("buoi"), str(m.get("buoi") or "")),
        "ma_buoi": m.get("buoi") or "sang",
        "gio": m.get("gio"),
        "ten": m.get("ten") or "",
        "nghi": m.get("loai") == "nghi",
        "cau": _MA_NGUON.sub("", cau or "").strip() or None,
        "ghi_chu": m.get("ghi_chu"),
        "anh_src": anh_src,
    }


def _tach_trang_ngay(ng: dict, layout_id: str, day_header: str, route_summary: str, muc_ds: list[dict],
                     an_ds: list[dict], dining_note: str | None) -> list[dict]:
    if not muc_ds:
        return [{
            "kieu": "ngay",
            "layout_id": layout_id,
            "so": ng["ngay"],
            "tiep": False,
            "ngay_tieu_de": day_header,
            "ngay_chu": _ngay_chu(ng),
            "chang": route_summary,
            "muc": [],
            "an": an_ds,
            "dining_note": dining_note,
        }]
    per_page = 4 if layout_id == "day_cards_2col" and len(muc_ds) > 4 else _MUC_TOI_DA_V2
    if len(muc_ds) <= per_page:
        chunks = [muc_ds]
    else:
        so_trang = max(2, -(-len(muc_ds) // per_page))
        moi = -(-len(muc_ds) // so_trang)
        chunks = [muc_ds[i:i + moi] for i in range(0, len(muc_ds), moi)]
    out = []
    for k, phan in enumerate(chunks):
        sub_lay = layout_id
        if k > 0 and layout_id == "day_photo_feature" and len(phan) >= 3:
            sub_lay = "day_timeline"
        out.append({
            "kieu": "ngay",
            "layout_id": sub_lay,
            "so": ng["ngay"],
            "tiep": k > 0,
            "ngay_tieu_de": f"{day_header} (tiếp)" if k > 0 else day_header,
            "ngay_chu": _ngay_chu(ng),
            "chang": route_summary,
            "muc": phan,
            "an": an_ds if k == len(chunks) - 1 else [],
            "dining_note": dining_note if k == len(chunks) - 1 else None,
        })
    return out


def _slides_chung(canonical: dict, theme_id: str, slides: list[dict], ngay_tao: str | None,
                  o_dau_header: str | None = None, o_dau_indices: list[int] | None = None,
                  notes_header: str | None = None, include_lodging: bool = True) -> dict:
    an_toan = canonical.get("an_toan")
    o_dau = canonical.get("o_dau")
    an_all = canonical.get("an") or []

    if include_lodging and (isinstance(o_dau, dict) and (o_dau.get("co_so") or [])):
        co_so_goc = o_dau["co_so"]
        idxs = [i for i in (o_dau_indices or [0, 1, 2]) if 0 <= i < len(co_so_goc)][:3]
        if not idxs:
            idxs = list(range(min(3, len(co_so_goc))))
        co_so_chon = [co_so_goc[i] for i in idxs]
        disclaimer = o_dau.get("nhan") or DISCLAIMER_O_DAU
        if "chưa kiểm giá, phòng trống" not in disclaimer:
            disclaimer = f"{disclaimer} — {DISCLAIMER_O_DAU}"
        slides.append({
            "kieu": "o_dau",
            "layout_id": "lodging_dining",
            "header": o_dau_header or f"Gợi ý lưu trú: khu {o_dau.get('ten_khu') or 'Huế'}",
            "ly_do": o_dau.get("ly_do") or "",
            "co_so": co_so_chon,
            "an_tong": an_all,
            "disclaimer": disclaimer,
        })

    luu_y = ([an_toan] if an_toan else []) + [
        g["cau"] for g in (canonical.get("ghi_chu") or []) if g.get("ma") != "du_bao" and g.get("cau")
    ] + [DONG_DU_BAO, DONG_THAY_DOI, DONG_NGUON]
    diem_all = [m for ng in (canonical.get("ngay") or []) for m in (ng.get("muc") or []) if m.get("loai") != "nghi"]
    ban_do = [
        {"ten": m["ten"], "url": m["map_url"]}
        for m in diem_all
        if isinstance(m.get("map_url"), str) and m["map_url"].startswith(MAP_PREFIX)
    ]
    for i in range(0, len(luu_y), DONG_LUU_Y_MOI_TRANG):
        cuoi = i + DONG_LUU_Y_MOI_TRANG >= len(luu_y)
        slides.append({
            "kieu": "luu_y",
            "layout_id": "notes_map",
            "header": (notes_header or "Lưu ý trước khi đi") + (" (tiếp)" if i > 0 else ""),
            "tiep": i > 0,
            "dong": luu_y[i:i + DONG_LUU_Y_MOI_TRANG],
            "ban_do": ban_do if cuoi else [],
            "an_toan": bool(an_toan) and i == 0,
            "an_toan_cau": an_toan if (an_toan and i == 0) else None,
        })
    return {"theme_id": theme_id, "ngay_tao": ngay_tao, "slides": slides}


def trang_lich_v2(canonical: dict, theme_id: str | None = None, ngay_tao: str | None = None) -> dict:
    """Bộ dựng slide thuần code v2 (`0 USD`) dùng đủ 3 theme + 9 layout từ `CanonicalItinerary`."""
    from api.pptx_catalog import ALLOWED_THEMES, chon_layout_ngay, chon_theme_mac_dinh

    ts = canonical.get("tham_so") or {}
    theme = theme_id if theme_id in ALLOWED_THEMES else chon_theme_mac_dinh(ts)
    ngay_ds = canonical.get("ngay") or []
    an_toan = canonical.get("an_toan")
    minh_hieu = str(canonical.get("minh_hieu") or "")
    tom_tat = minh_hieu.removeprefix("Mình hiểu: ").split(" — sai thì bấm")[0]
    diem_all = [m for ng in ngay_ds for m in (ng.get("muc") or []) if m.get("loai") != "nghi"]
    manifest_diem = (canonical.get("anh_manifest") or {}).get("diem") or {}
    anh_srcs = list(dict.fromkeys(manifest_diem.values()))
    if not anh_srcs:
        anh_srcs = list(dict.fromkeys(m["anh"]["src"] for m in diem_all if isinstance(m.get("anh"), dict) and m["anh"].get("src")))

    cover_layout = "cover_hero" if anh_srcs else "cover_split"
    slides: list[dict] = [{
        "kieu": "bia",
        "layout_id": cover_layout,
        "tieu_de": TIEU_DE.format(n=len(ngay_ds)),
        "tom_tat": tom_tat,
        "anh_srcs": anh_srcs[:3],
        "so_diem": len(diem_all),
        "diem_chinh": [m["ten"] for m in diem_all if m.get("buoi") != "toi"][:DIEM_CHINH_TREN_BIA],
        "ngay_tao": ngay_tao,
        "ngay_di": ts.get("ngay_di"),
        "an_toan": an_toan,
    }]

    if len(ngay_ds) >= 2:
        slides.append({
            "kieu": "tong_quan",
            "layout_id": "overview_route",
            "header": f"Tổng quan hành trình {len(ngay_ds)} ngày",
            "ngay_tom_tat": [
                {
                    "ngay": ng["ngay"],
                    "ngay_tieu_de": _ten_ngay_vn(ng),
                    "chang": " → ".join(ng.get("chang") or []) or "Trung tâm Huế",
                    "diem": [m["ten"] for m in (ng.get("muc") or []) if m.get("loai") != "nghi"],
                }
                for ng in ngay_ds
            ],
        })

    for ng in ngay_ds:
        an_ngay = [
            {"bua": "Trưa" if a["bua"] == "trua" else "Tối", "gan": a.get("gan") or "", "quan": [q["ten"] for q in (a.get("quan") or [])]}
            for a in (canonical.get("an") or [])
            if a.get("ngay") == ng["ngay"] and a.get("quan")
        ]
        muc_goc = [m for m in (ng.get("muc") or []) if m.get("loai") != "nghi"]
        co_anh = any(isinstance(m.get("anh"), dict) and m["anh"].get("src") for m in muc_goc)
        lay = chon_layout_ngay(ng, co_anh=co_anh)
        muc_v2 = [_muc_chuan_v2(m) for m in (ng.get("muc") or []) if m.get("loai") != "nghi"]
        if not muc_v2:
            muc_v2 = [_muc_chuan_v2(m) for m in (ng.get("muc") or [])]
        route_str = " → ".join(ng.get("chang") or []) or "Lịch trình trong ngày"
        dining_note = " · ".join(f"{a['bua']} gần {a['gan']}: {', '.join(a['quan'])}" for a in an_ngay) if an_ngay else None
        slides.extend(_tach_trang_ngay(ng, lay, _ten_ngay_vn(ng), route_str, muc_v2, an_ngay, dining_note))

    return _slides_chung(canonical, theme, slides, ngay_tao)


def plan_sang_cac_trang(plan: dict, canonical: dict, ngay_tao: str | None = None) -> dict:
    """Chuyển `SlideDeckPlan` (đã hậu kiểm) sang cấu trúc slides sẵn sàng cho `dung_pptx_v2`, ép giữ bất biến từ `canonical`."""
    from api.pptx_catalog import ALLOWED_THEMES, chon_theme_mac_dinh

    ts = canonical.get("tham_so") or {}
    theme = plan.get("theme_id") if plan.get("theme_id") in ALLOWED_THEMES else chon_theme_mac_dinh(ts)
    ngay_ds = canonical.get("ngay") or []
    ngay_theo_so = {ng["ngay"]: ng for ng in ngay_ds}
    muc_theo_id = {m["id_muc"]: m for ng in ngay_ds for m in (ng.get("muc") or [])}
    diem_all = [m for ng in ngay_ds for m in (ng.get("muc") or []) if m.get("loai") != "nghi"]
    manifest_diem = (canonical.get("anh_manifest") or {}).get("diem") or {}

    anh_srcs: list[str] = []
    for key in [plan.get("hero_image_id"), *(plan.get("secondary_image_ids") or [])]:
        if key and key in manifest_diem and manifest_diem[key] not in anh_srcs:
            anh_srcs.append(manifest_diem[key])
    for src in manifest_diem.values():
        if src not in anh_srcs and len(anh_srcs) < 3:
            anh_srcs.append(src)

    slides: list[dict] = [{
        "kieu": "bia",
        "layout_id": plan.get("cover_layout") or "cover_hero",
        "tieu_de": plan.get("deck_title") or TIEU_DE.format(n=len(ngay_ds)),
        "tom_tat": plan.get("deck_subtitle") or "",
        "anh_srcs": anh_srcs[:3],
        "so_diem": len(diem_all),
        "diem_chinh": list(plan.get("highlights") or [m["ten"] for m in diem_all if m.get("buoi") != "toi"][:DIEM_CHINH_TREN_BIA]),
        "ngay_tao": ngay_tao,
        "ngay_di": ts.get("ngay_di"),
        "an_toan": canonical.get("an_toan"),
    }]

    if plan.get("include_overview") and len(ngay_ds) >= 2:
        ov_map = {x["ngay"]: x["summary"] for x in (plan.get("overview_summaries") or [])}
        slides.append({
            "kieu": "tong_quan",
            "layout_id": "overview_route",
            "header": f"Tổng quan hành trình {len(ngay_ds)} ngày",
            "ngay_tom_tat": [
                {
                    "ngay": ng["ngay"],
                    "ngay_tieu_de": _ten_ngay_vn(ng),
                    "chang": ov_map.get(ng["ngay"]) or (" → ".join(ng.get("chang") or []) or "Trung tâm Huế"),
                    "diem": [m["ten"] for m in (ng.get("muc") or []) if m.get("loai") != "nghi"],
                }
                for ng in ngay_ds
            ],
        })

    for d_plan in plan.get("days") or []:
        ng_so = d_plan["day_number"]
        ng_goc = ngay_theo_so.get(ng_so) or {"ngay": ng_so, "ngay_thang": None, "chang": [], "muc": []}
        an_ngay = [
            {"bua": "Trưa" if a["bua"] == "trua" else "Tối", "gan": a.get("gan") or "", "quan": [q["ten"] for q in (a.get("quan") or [])]}
            for a in (canonical.get("an") or [])
            if a.get("ngay") == ng_so and a.get("quan")
        ]
        muc_v2 = []
        for slot in d_plan.get("items") or []:
            goc = muc_theo_id.get(slot["id_muc"])
            if goc is None:
                continue
            item = _muc_chuan_v2(goc, copy_override=slot.get("short_copy"))
            if not slot.get("show_image", True):
                item["anh_src"] = None
            muc_v2.append(item)
        dining_note = d_plan.get("dining_note") or (
            " · ".join(f"{a['bua']} gần {a['gan']}: {', '.join(a['quan'])}" for a in an_ngay) if an_ngay else None
        )
        slides.extend(_tach_trang_ngay(
            ng_goc,
            d_plan["layout_id"],
            d_plan.get("day_header") or _ten_ngay_vn(ng_goc),
            d_plan.get("route_summary") or (" → ".join(ng_goc.get("chang") or []) or "Lịch trình trong ngày"),
            muc_v2,
            an_ngay,
            dining_note,
        ))

    return _slides_chung(
        canonical,
        theme,
        slides,
        ngay_tao,
        o_dau_header=plan.get("lodging_header"),
        o_dau_indices=plan.get("lodging_indices"),
        notes_header=plan.get("notes_header"),
        include_lodging=bool(canonical.get("o_dau")),
    )


def dung_pptx_v2(deck: dict, thu_muc_anh: Path) -> bytes:
    """Dựng `.pptx` v2 từ `deck` (`theme_id` + `slides` theo 9 layout), dùng `pptx_fit` và `crop_anh_giua`."""
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Inches, Pt

    from api.hanh_trinh_chuan import hop_le_anh_ks, hop_le_anh_lich
    from api.pptx_catalog import CAO, PHONG, PHONG_TD, RONG, THEMES
    from api.pptx_fit import cat_sach_ranh_gioi, co_chu_vua_khung, crop_anh_giua

    pal = THEMES.get(deck.get("theme_id") or "di_san_tram", THEMES["di_san_tram"])
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(RONG), Inches(CAO)

    def hop(s, x, y, w, h, ma, hinh=MSO_SHAPE.RECTANGLE, bo=None):
        sh = s.shapes.add_shape(hinh, Inches(x), Inches(y), Inches(w), Inches(h))
        sh.fill.solid()
        sh.fill.fore_color.rgb = RGBColor.from_string(pal[ma])
        sh.line.fill.background()
        sh.shadow.inherit = False
        if bo is not None:
            sh.adjustments[0] = bo
        return sh

    def fit_run(text: str, w: float, h: float, base_pt: float, min_pt: float, margin_v: float = 0.04) -> tuple[str, float]:
        mv = margin_v * 2.0
        pt, fits, _, _ = co_chu_vua_khung(text, w, h, base_pt, min_pt, margin_v_in=mv)
        if fits:
            return text, pt
        return cat_sach_ranh_gioi(text, w, h, pt, margin_v_in=mv), pt

    def chu(s, x, y, w, h, doan, co=14.0, min_co=9.0, ma="chu", dam=False, phong=PHONG, can=PP_ALIGN.LEFT, giua=False, cach=0, auto_fit=True, margin_v: float = 0.04):
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.04)
        tf.margin_top = tf.margin_bottom = Inches(margin_v)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE if giua else MSO_ANCHOR.TOP
        items = [(doan, co, ma, dam)] if isinstance(doan, str) else list(doan)
        if auto_fit and len(items) == 1 and isinstance(items[0][0], str):
            txt, pt_used = fit_run(items[0][0], w, h, float(items[0][1]), float(min_co), margin_v=margin_v)
            items = [(txt, pt_used, items[0][2], items[0][3], *items[0][4:])]
        for i, d in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = can
            if cach:
                p.space_after = Pt(cach)
            r = p.add_run()
            r.text = str(d[0])
            r.font.size, r.font.bold, r.font.name = Pt(d[1]), d[3], phong
            r.font.color.rgb = RGBColor.from_string(pal[d[2]])
            if len(d) > 4 and d[4]:
                r.hyperlink.address = d[4]
        return tb

    def anh(s, src: str | None, x: float, y: float, w: float, h: float, ten: str | None = None):
        valid = hop_le_anh_lich(src, thu_muc_anh=thu_muc_anh) or hop_le_anh_ks(src, thu_muc_anh=thu_muc_anh)
        f = (thu_muc_anh / valid.lstrip("/")) if valid else None
        buf = crop_anh_giua(f, w, h) if f else None
        if buf is None:
            hop(s, x, y, w, h, "nhat")
            d = min(w, h) * 0.56
            hop(s, x + w - d - 0.06, y + h - d - 0.06, d, d, "hoa_tiet", MSO_SHAPE.OVAL)
            hop(s, x + 0.06, y + 0.06, d * 0.48, d * 0.48, "hoa_tiet", MSO_SHAPE.OVAL)
            if ten:
                chu(s, x + 0.06, y + 0.04, w - 0.12, h - 0.08, ten, 11.5, 8.5, "chinh", True, PHONG_TD, PP_ALIGN.CENTER, True)
            return
        s.shapes.add_picture(buf, Inches(x), Inches(y), width=Inches(w), height=Inches(h))

    def ve_bia(s, t: dict):
        lay = t.get("layout_id") or "cover_hero"
        hop(s, 0, 0, 5.2, CAO, "chinh")
        hop(s, 0.6, 0.85, 0.9, 0.07, "nhan")
        chu(s, 0.6, 1.05, 4.2, 2.0, t["tieu_de"], 36.0, 22.0, "nen", True, PHONG_TD)
        chu(s, 0.6, 3.15, 4.2, 0.95, t["tom_tat"], 15.5, 11.0, "nhat")
        if t.get("diem_chinh"):
            chu(s, 0.6, 4.25, 4.2, 1.6, [(ten, 13.0, "nen", False) for ten in t["diem_chinh"][:4]], cach=3, auto_fit=False)
        chu(s, 0.6, 6.15, 4.2, 0.85, [
            (f"{t['so_diem']} điểm tham quan", 14.5, "nhan", True),
            *([(f"Tạo ngày {t['ngay_tao']}", 10.5, "nhat", False)] if t.get("ngay_tao") else []),
        ], auto_fit=False)
        a = list(t.get("anh_srcs") or []) + [None] * 3
        thap = 0.95 if t.get("an_toan") else 0.0
        if lay == "cover_hero":
            anh(s, a[0], 5.55, 0.55, 7.2, 4.35 - thap * 0.55)
            anh(s, a[1], 5.55, 5.05 - thap * 0.55, 3.5, 1.9 - thap * 0.45)
            anh(s, a[2], 9.25, 5.05 - thap * 0.55, 3.5, 1.9 - thap * 0.45)
        else:
            anh(s, a[0], 5.6, 0.6, 7.15, 4.05 - thap * 0.5)
            anh(s, a[1], 5.6, 4.8 - thap * 0.5, 3.5, 2.1 - thap * 0.5)
            anh(s, a[2], 9.25, 4.8 - thap * 0.5, 3.5, 2.1 - thap * 0.5)
        if t.get("an_toan"):
            hop(s, 5.55, 6.02, 7.2, 0.9, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.1)
            hop(s, 5.55, 6.02, 0.1, 0.9, "phu")
            chu(s, 5.75, 6.04, 6.9, 0.86, t["an_toan"], 10.5, 8.0, "chu", True, giua=True)

    def ve_tong_quan(s, t: dict):
        hop(s, 0, 0, RONG, 1.05, "chinh")
        hop(s, 0.6, 1.05, 1.2, 0.06, "nhan")
        chu(s, 0.6, 0.16, 11.8, 0.72, t["header"], 26.0, 18.0, "nen", True, PHONG_TD, giua=True)
        ngays = t.get("ngay_tom_tat") or []
        n = max(1, len(ngays))
        row_h = min(1.06, 5.5 / n)
        for i, ng in enumerate(ngays):
            y = 1.32 + i * (row_h + 0.08)
            hop(s, 0.6, y, 12.1, row_h, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.08)
            hop(s, 0.6, y, 2.55, row_h, "chinh")
            chu(s, 0.75, y + 0.06, 2.25, row_h - 0.12, ng["ngay_tieu_de"], 13.5, 10.0, "nen", True, PHONG_TD, giua=True)
            route_txt = f"{ng['chang']} · " + " → ".join(ng["diem"])
            chu(s, 3.3, y + 0.06, 9.25, row_h - 0.12, route_txt, 12.5, 9.5, "chu", False, giua=True)

    def ve_ngay_timeline(s, t: dict):
        hop(s, 0, 0, 2.5, CAO, "chinh")
        hop(s, 0.3, 0.55, 0.7, 0.06, "nhan")
        ngay_td = f"Ngày {t['so']}" + (" (tiếp)" if t.get("tiep") else "")
        chu(s, 0.3, 0.7, 1.9, 0.95, ngay_td, 28.0, 20.0, "nen", True, PHONG_TD)
        chu(s, 0.3, 1.72, 1.9, 0.7, t.get("ngay_chu") or "", 13.0, 10.0, "nhat", True)
        chu(s, 0.3, 2.48, 1.9, 2.1, t["chang"], 12.5, 9.5, "nhat")
        muc = t.get("muc") or []
        n = max(len(muc), 1)
        day_h = 5.15 if t.get("dining_note") else 6.15
        cao_hang = min(1.85, day_h / n)
        to = cao_hang >= 1.45
        rong_anh = 2.45 if to else 1.75
        if n > 1:
            hop(s, 3.27, 0.75, 0.04, cao_hang * (n - 1) + 0.2, "nhat")
        for i, m in enumerate(muc):
            y = 0.55 + i * cao_hang
            ma_b = m["ma_buoi"] if m["ma_buoi"] in pal else "sang"
            hop(s, 3.12, y + 0.1, 0.34, 0.34, ma_b, MSO_SHAPE.OVAL)
            hop(s, 3.7, y + 0.06, 0.95, 0.34, ma_b, MSO_SHAPE.ROUNDED_RECTANGLE, 0.5)
            chu(s, 3.7, y + 0.06, 0.95, 0.34, m["buoi"], 11.5, 9.5, "trang", True, can=PP_ALIGN.CENTER, giua=True)
            chu(s, 3.66, y + 0.44, 1.75, 0.46, m["gio"] or "Trong ngày", 12.5 if to else 11.5, 9.5, "chu", True)
            anh(s, m.get("anh_src"), 5.5, y, rong_anh, cao_hang - 0.18, m["ten"])
            tx = 5.68 + rong_anh
            tw = RONG - tx - 0.5
            chu(s, tx, y, tw, 0.4, m["ten"], 16.5 if to else 14.5, 11.5, "chinh", True, PHONG_TD)
            body = " · ".join(x for x in (m.get("cau"), m.get("ghi_chu")) if x)
            if body:
                chu(s, tx, y + 0.4, tw, max(0.45, cao_hang - 0.5), body, 12.0 if to else 10.5, 8.8, "chu")
        if t.get("dining_note"):
            hop(s, 3.1, 5.85, RONG - 3.6, 1.0, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.12)
            hop(s, 3.1, 5.85, 0.1, 1.0, "phu")
            chu(s, 3.35, 5.9, 1.55, 0.9, "Ăn gần đó", 13.5, 10.5, "phu", True, PHONG_TD, giua=True)
            chu(s, 4.95, 5.9, RONG - 5.6, 0.9, t["dining_note"], 11.5, 9.0, "chu", giua=True)

    def ve_ngay_cards_2col(s, t: dict):
        hop(s, 0, 0, RONG, 1.02, "chinh")
        hop(s, 0.6, 1.02, 1.1, 0.06, "nhan")
        chu(s, 0.6, 0.12, 12.1, 0.52, t["ngay_tieu_de"], 24.0, 17.0, "nen", True, PHONG_TD)
        chu(s, 0.6, 0.64, 12.1, 0.34, t["chang"], 12.0, 9.5, "nhat")
        muc = (t.get("muc") or [])[:4]
        has_dining = bool(t.get("dining_note"))
        grid_h = 5.0 if has_dining else 5.85
        rows = 2 if len(muc) > 2 else 1
        card_h = (grid_h - 0.2 * (rows - 1)) / rows
        card_w = 5.9
        for i, m in enumerate(muc):
            col, row = i % 2, i // 2
            x = 0.6 + col * (card_w + 0.33)
            y = 1.22 + row * (card_h + 0.2)
            hop(s, x, y, card_w, card_h, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.06)
            img_w = 2.05
            anh(s, m.get("anh_src"), x + 0.12, y + 0.12, img_w, card_h - 0.24, m["ten"])
            ma_b = m["ma_buoi"] if m["ma_buoi"] in pal else "sang"
            hop(s, x + img_w + 0.26, y + 0.14, 0.85, 0.28, ma_b, MSO_SHAPE.ROUNDED_RECTANGLE, 0.45)
            chu(s, x + img_w + 0.26, y + 0.14, 0.85, 0.28, m["buoi"], 10.5, 8.5, "trang", True, can=PP_ALIGN.CENTER, giua=True)
            chu(s, x + img_w + 1.2, y + 0.14, card_w - img_w - 1.34, 0.28, m["gio"] or "Trong ngày", 10.5, 8.5, "chu_phu", True, giua=True)
            chu(s, x + img_w + 0.26, y + 0.46, card_w - img_w - 0.4, 0.42, m["ten"], 14.5, 11.0, "chinh", True, PHONG_TD)
            body = " · ".join(x for x in (m.get("cau"), m.get("ghi_chu")) if x)
            if body:
                chu(s, x + img_w + 0.26, y + 0.9, card_w - img_w - 0.4, max(0.45, card_h - 1.02), body, 11.5, 8.8, "chu")
        if has_dining:
            hop(s, 0.6, 6.32, 12.13, 0.65, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.1)
            hop(s, 0.6, 6.32, 0.1, 0.65, "phu")
            chu(s, 0.82, 6.35, 11.75, 0.58, f"Ăn gần đó: {t['dining_note']}", 11.5, 9.0, "chu", giua=True)

    def ve_ngay_photo_feature(s, t: dict):
        muc = t.get("muc") or []
        feature = muc[0] if muc else None
        rest = muc[1:]
        anh(s, feature.get("anh_src") if feature else None, 0.55, 0.55, 5.75, 6.4, feature["ten"] if feature else t["ngay_tieu_de"])
        hop(s, 6.6, 0.55, 6.18, 1.15, "chinh", MSO_SHAPE.ROUNDED_RECTANGLE, 0.05)
        chu(s, 6.8, 0.65, 5.8, 0.55, t["ngay_tieu_de"], 24.0, 17.0, "nen", True, PHONG_TD)
        chu(s, 6.8, 1.22, 5.8, 0.38, t["chang"], 12.0, 9.5, "nhat")
        cur_y = 1.88
        has_dining = bool(t.get("dining_note"))
        avail_h = (5.95 if has_dining else 6.95) - cur_y
        n_m = max(1, len(muc))
        box_h = (avail_h - 0.14 * (n_m - 1)) / n_m
        for m in muc:
            hop(s, 6.6, cur_y, 6.18, box_h, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.06)
            chu(s, 6.78, cur_y + 0.1, 5.8, 0.32, f"{m['buoi']} · {m['gio'] or 'Trong ngày'}", 11.0, 8.8, "phu", True)
            chu(s, 6.78, cur_y + 0.4, 5.8, 0.42, m["ten"], 16.0, 12.0, "chinh", True, PHONG_TD)
            body = " · ".join(x for x in (m.get("cau"), m.get("ghi_chu")) if x)
            if body:
                chu(s, 6.78, cur_y + 0.84, 5.8, max(0.42, box_h - 0.94), body, 12.5, 9.2, "chu")
            cur_y += box_h + 0.14
        if has_dining:
            hop(s, 6.6, 6.1, 6.18, 0.85, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.1)
            hop(s, 6.6, 6.1, 0.1, 0.85, "phu")
            chu(s, 6.82, 6.14, 5.85, 0.77, f"Ăn gần đó: {t['dining_note']}", 11.5, 9.0, "chu", giua=True)
        _ = rest

    def ve_ngay_compact_grid(s, t: dict):
        hop(s, 0, 0, RONG, 0.95, "chinh")
        chu(s, 0.6, 0.1, 12.1, 0.48, t["ngay_tieu_de"], 22.5, 16.5, "nen", True, PHONG_TD)
        chu(s, 0.6, 0.56, 12.1, 0.32, t["chang"], 11.5, 9.0, "nhat")
        muc = (t.get("muc") or [])[:6]
        has_dining = bool(t.get("dining_note"))
        grid_h = 5.15 if has_dining else 5.95
        rows = max(1, -(-len(muc) // 2))
        cell_h = (grid_h - 0.15 * (rows - 1)) / rows
        cell_w = 5.95
        for i, m in enumerate(muc):
            col, row = i % 2, i // 2
            x = 0.6 + col * (cell_w + 0.23)
            y = 1.12 + row * (cell_h + 0.15)
            hop(s, x, y, cell_w, cell_h, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.06)
            img_w = 1.35
            anh(s, m.get("anh_src"), x + 0.1, y + 0.1, img_w, cell_h - 0.2, m["ten"])
            chu(s, x + img_w + 0.22, y + 0.08, cell_w - img_w - 0.32, 0.26, f"{m['buoi']} · {m['gio'] or 'Trong ngày'}", 10.0, 8.2, "phu", True)
            chu(s, x + img_w + 0.22, y + 0.34, cell_w - img_w - 0.32, 0.34, m["ten"], 13.0, 10.0, "chinh", True, PHONG_TD)
            body = " · ".join(x for x in (m.get("cau"), m.get("ghi_chu")) if x)
            if body:
                chu(s, x + img_w + 0.22, y + 0.68, cell_w - img_w - 0.32, max(0.35, cell_h - 0.76), body, 10.2, 8.2, "chu")
        if has_dining:
            hop(s, 0.6, 6.38, 12.13, 0.6, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.1)
            hop(s, 0.6, 6.38, 0.1, 0.6, "phu")
            chu(s, 0.82, 6.4, 11.75, 0.54, f"Ăn gần đó: {t['dining_note']}", 11.0, 8.8, "chu", giua=True)

    def ve_o_dau(s, t: dict):
        hop(s, 0, 0, RONG, 1.0, "chinh")
        hop(s, 0.6, 1.0, 1.2, 0.06, "nhan")
        chu(s, 0.6, 0.14, 12.1, 0.72, t["header"], 25.0, 17.5, "nen", True, PHONG_TD, giua=True)
        if t.get("ly_do"):
            chu(s, 0.6, 1.15, 12.1, 0.4, t["ly_do"], 12.0, 9.5, "chu_phu")
        co_so = (t.get("co_so") or [])[:3]
        n = max(1, len(co_so))
        col_w = (12.13 - 0.25 * (n - 1)) / n
        for i, c in enumerate(co_so):
            x = 0.6 + i * (col_w + 0.25)
            hop(s, x, 1.62, col_w, 3.15, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.06)
            anh(s, c.get("anh"), x + 0.15, 1.74, col_w - 0.3, 1.65, c["ten"])
            chu(s, x + 0.15, 3.48, col_w - 0.3, 0.45, c["ten"], 14.0, 10.5, "chinh", True, PHONG_TD)
            meta = f"{c.get('xep_hang') or ''}" + (f" · {c['dia_chi']}" if c.get("dia_chi") else "")
            chu(s, x + 0.15, 3.96, col_w - 0.3, 0.72, meta, 11.0, 8.8, "chu")
        an_tong = t.get("an_tong") or []
        if an_tong:
            hop(s, 0.6, 4.92, 12.13, 1.38, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.08)
            chu(s, 0.8, 4.98, 11.7, 0.35, "Quán ăn gợi ý theo ngày", 13.5, 10.5, "phu", True, PHONG_TD)
            an_lines = " · ".join(
                f"Ngày {a['ngay']} ({'Trưa' if a['bua'] == 'trua' else 'Tối'}): {', '.join(q['ten'] for q in a['quan'])}"
                for a in an_tong[:6] if a.get("quan")
            )
            chu(s, 0.8, 5.34, 11.7, 0.88, an_lines, 11.0, 8.5, "chu")
        chu(s, 0.6, 6.42, 12.13, 0.42, t["disclaimer"], 11.0, 9.0, "phu", True)

    def ve_luu_y(s, t: dict):
        hop(s, 0, 0, RONG, 1.05, "chinh")
        hop(s, 0.6, 1.05, 1.2, 0.06, "nhan")
        chu(s, 0.6, 0.16, 10.5, 0.72, t.get("header") or "Lưu ý trước khi đi", 26.0, 18.0, "nen", True, PHONG_TD, giua=True)
        ban_do = t.get("ban_do") or []
        y_top = 1.35
        if t.get("an_toan") and t.get("an_toan_cau"):
            hop(s, 0.6, 1.25, 12.13, 0.82, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.08)
            hop(s, 0.6, 1.25, 0.12, 0.82, "phu")
            chu(s, 0.84, 1.28, 11.75, 0.76, t["an_toan_cau"], 11.5, 9.0, "phu", True, giua=True)
            y_top = 2.22
        ha_cot = len(ban_do) > 8
        rong_trai = 7.05 if ha_cot else (7.5 if ban_do else RONG - 1.4)
        dong_thuong = [d for d in (t.get("dong") or []) if d != t.get("an_toan_cau")]
        body = "\n".join("•  " + d for d in dong_thuong)
        if body:
            chu(s, 0.7, y_top, rong_trai, 6.85 - y_top, body, 13.5, 9.5, "chu")
        if ban_do:
            px, pw = (8.05, 4.68) if ha_cot else (8.55, 4.2)
            hop(s, px, y_top, pw, 6.85 - y_top, "nhat", MSO_SHAPE.ROUNDED_RECTANGLE, 0.05)
            chu(s, px + 0.15, y_top + 0.08, pw - 0.3, 0.44, "Mở bản đồ từng điểm", 15.0, 11.5, "phu", True, PHONG_TD)
            y_list = y_top + 0.56
            avail = max(1.6, 5.90 - y_list)
            if ha_cot:
                n_rows = (len(ban_do) + 1) // 2
                cao_dong = min(0.36, avail / n_rows)
                col_w = 2.16
                x_cols = (8.18, 10.46)
                for i, d in enumerate(ban_do):
                    col, row = i // n_rows, i % n_rows
                    o = chu(s, x_cols[col], y_list + row * cao_dong, col_w, cao_dong, d["ten"], 10.5, 7.5, "phu", giua=True, margin_v=0.01)
                    o.text_frame.paragraphs[0].runs[0].font.underline = True
                    o.click_action.hyperlink.address = d["url"]
            else:
                cao_dong = min(0.4, avail / len(ban_do))
                for i, d in enumerate(ban_do):
                    o = chu(s, 8.75, y_list + i * cao_dong, 3.8, cao_dong, d["ten"], 12.0 if cao_dong >= 0.34 else 10.0, 8.0, "phu", giua=True, margin_v=0.01)
                    o.text_frame.paragraphs[0].runs[0].font.underline = True
                    o.click_action.hyperlink.address = d["url"]
            chu(s, px + 0.15, 5.95, pw - 0.3, 0.8, f"{DONG_BAN_DO}\n{DONG_SUA_FILE}", 10.5, 8.5, "chu")

    for so, t in enumerate(deck.get("slides") or [], start=1):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        hop(s, 0, 0, RONG, CAO, "nen")
        lay = t.get("layout_id")
        if t.get("kieu") == "bia":
            ve_bia(s, t)
        elif lay == "overview_route" or t.get("kieu") == "tong_quan":
            ve_tong_quan(s, t)
        elif lay == "day_cards_2col":
            ve_ngay_cards_2col(s, t)
        elif lay == "day_photo_feature":
            ve_ngay_photo_feature(s, t)
        elif lay == "day_compact_grid":
            ve_ngay_compact_grid(s, t)
        elif lay == "day_timeline" or t.get("kieu") == "ngay":
            ve_ngay_timeline(s, t)
        elif lay == "lodging_dining" or t.get("kieu") == "o_dau":
            ve_o_dau(s, t)
        else:
            ve_luu_y(s, t)
        chu(s, 0.6, CAO - 0.42, RONG - 1.2, 0.3, f"Lịch trình Huế · trang {so}", 9.5, 8.0, "phu", can=PP_ALIGN.RIGHT)

    out = io.BytesIO()
    prs.save(out)
    return out.getvalue()
