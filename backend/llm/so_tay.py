"""Công tắc `so_tay` — SỔ TAY CHO CHUYẾN ĐI dựng từ lịch đang lưu của cuộc (bản thử, nhánh thu-b-so-tay; chủ dự án chọn 21:21 24/11/2026 sau khi xem
hai hồ sơ mẫu: "Đúng, làm cả hai kiểu", sổ tay trước).

Chia việc code ↔ model (luật nền: thứ phải luôn đúng do code làm):
- DÀN Ý do code lấy từ lịch: mỗi điểm một mục, mỗi ngày một mục ăn uống, cuối cùng "Trước khi đi".
- ĐỊA CHỈ / GIỜ MỞ CỬA / GIÁ VÉ do code chép từ bảng "thẻ nơi" (`the_noi.Bang`: dòng chép nguyên từ bài riêng + hàng bảng vé lẻ); ăn uống = đúng quán gợi ý
  của lịch (`lich["an"]`). Model KHÔNG viết giờ / giá: ý nào của model chứa giờ hoặc giá bị bỏ (`loc_y`).
- Model chỉ viết hai danh sách ngắn cho mỗi điểm ("Nên xem", "Lưu ý") và một danh sách "Đi lại", mỗi ý kèm số nguồn; code giữ ĐỘ DÀI (số ý, số ký tự) và
  bỏ ý không có nguồn hợp lệ.
- "Kho chưa có" là MỘT khuôn do code đặt (`kieu: "thieu"`): ô dữ kiện bảng không có, hoặc danh sách model trả rỗng / bị bỏ hết. Model không tự viết câu thiếu.

Vì sao không dùng vòng hỏi đáp cho từng mục (cách của hai hồ sơ mẫu, `data/x15_phan_ai_2026-11-23/b_ho_so_mau/KET_QUA.md`): 3,2 lời gọi + định tuyến mỗi
mục, 78–87 giây cho 11 mục; độ dài không do code giữ; các mục cãi nhau về số (mục này "kho chưa có khoảng cách", mục kia "khoảng 7 km"; "vé lẻ mỗi lăng
150.000 đồng" trong khi ba lăng giá khác); dấu "kho chưa có" lúc là câu cố định lúc là lời tự do.

Module thuần (không đọc cấu hình, không SDK, không mạng); route `api/routes/so_tay.py` nối tìm kho + model.
"""
import math
import re
import unicodedata

from llm import the_noi as thn
from llm.full_corpus_prompt import MAY_HAVE_CHANGED_NOTICE

TRAN_Y = {"nen_xem": 4, "luu_y": 3, "di_lai": 4}   # số ý nhiều nhất mỗi danh sách
TRAN_KY_TU = 200                                    # một ý dài hơn ⇒ bỏ (lời dặn xin dưới 30 từ)
SO_DOAN_BANG_CHUNG = 8                              # số đoạn kho đưa cho model ở một mục
NHAN = {"nen_xem": "Nên xem", "luu_y": "Lưu ý", "di_lai": "Đi lại"}
NHAN_BUA = {"trua": "Bữa trưa", "toi": "Bữa tối"}
MUC_QUAN = "Quán gợi ý của lịch (theo vị trí điểm tham quan)"
CAU_TIM_DIEM = "{ten}: những điểm đáng xem và lưu ý khi tham quan"
# cụm để xếp các đoạn TRONG bài của một điểm (điểm từ khoá tính riêng trong bài) khi lần tìm chung mang về ít đoạn của bài đó
CUM_TRONG_BAI = "điểm đáng xem nổi bật kiến trúc công trình cảnh quan trải nghiệm tham quan lưu ý quy tắc ứng xử trang phục"
SO_DOAN_TU_TIM = 4   # nhiều nhất chừng này đoạn của bài lấy theo thứ hạng của lần tìm; phần còn lại lấy theo xếp trong bài
CAU_TIM_DI_LAI = "Đi lại giữa các điểm tham quan ở Huế: taxi, xe máy, xe đạp, xích lô, thuyền"
# Ý của model NÓI VỀ giờ mở cửa hoặc giá ("mở cửa…", "ngừng bán vé", "giá vé", "150.000 đồng", "miễn phí") ⇒ ý đó bị bỏ: hai thứ này chỉ đi đường code
# chép. Giờ trong ngày nói về cảnh ("bình minh 04h30 – 06h00") KHÔNG bị bỏ — lượt thật đầu tiên (24/11/2026) luật "mọi con số giờ" làm mục Đầm Chuồn mất
# hết ý "Nên xem".
_GIO_GIA = re.compile(r"mở cửa|đóng cửa|giờ mở|mở từ|ngừng bán vé|giá vé|vé vào|vé tham quan|vé người lớn|vé trẻ em|miễn phí|"
                      r"\d[\d.,]*\s*(?:đồng|đ\b|vnd|vnđ|k\b|nghìn|ngàn|triệu)", re.IGNORECASE)
_TU = re.compile(r"[^\W_]+", re.UNICODE)
DIA_CHI_DAI = 120   # dòng địa chỉ dài hơn ⇒ cắt ở dấu ngoặc đầu (phần trong ngoặc của kho là lịch sử địa giới hành chính); nguồn vẫn giữ nguyên dòng
MUC_GIO_BANG = "Giờ mở cửa (bảng điểm của lịch, chép từ bài)"
_MA = re.compile(r"\s*\[\s*(?:nguồn\s*)?\d+\s*\]", re.IGNORECASE)
_NHAN_DIA_CHI = re.compile(r"^(địa chỉ[^:]{0,25}|khu vực)\s*:\s*", re.IGNORECASE)
_NHAN_GIO = re.compile(r"^giờ (mở cửa|hoạt động)[^:]{0,25}:\s*", re.IGNORECASE)
NHOM_CO_VE = "heritages/"   # chỉ di tích mới có ô "Giá vé" (quán, phố đi bộ, đầm phá không bán vé ⇒ không in "Kho chưa có: Giá vé")


def _nfc(chu: str) -> str:
    return unicodedata.normalize("NFC", chu or "")


def dan_y(lich: dict) -> list[dict]:
    """Lịch (đối tượng giao diện nhận, `xuat.lich_tu_luu`) ⇒ các mục của sổ tay theo thứ tự in. Mục điểm mang `id_diem` để route lấy bài / thẻ nơi
    (khoá này không gửi ra giao diện — `ra_giao_dien`)."""
    muc, an = [], {}
    for a in lich.get("an") or ():
        an.setdefault(a["ngay"], []).append(a)
    for ng in lich["ngay"]:
        for m in ng["muc"]:
            if not m.get("id_diem"):
                continue  # tối nghỉ: dòng do code của lịch, không có gì để viết
            muc.append({"id": m["id_muc"], "loai": "diem", "ngay": ng["ngay"], "buoi": m["buoi"], "ten": m["ten"], "gio": m.get("gio"),
                        "bai_id": m.get("bai_id"), "anh": {"src": m["anh"]["src"]} if m.get("anh") and m["anh"].get("src") else None, "id_diem": m["id_diem"]})
        if an.get(ng["ngay"]):
            muc.append({"id": f"n{ng['ngay']}-an", "loai": "an_uong", "ngay": ng["ngay"], "buoi": None, "ten": f"Ăn uống ngày {ng['ngay']}", "gio": None,
                        "bai_id": None, "anh": None, "an": an[ng["ngay"]]})
    muc.append({"id": "truoc-khi-di", "loai": "truoc_khi_di", "ngay": None, "buoi": None, "ten": "Trước khi đi", "gio": None, "bai_id": None, "anh": None})
    return muc


def ra_giao_dien(muc: dict) -> dict:
    return {k: muc[k] for k in ("id", "loai", "ngay", "buoi", "ten", "gio", "bai_id", "anh")}


def _ve_chu(hang: str) -> str | None:
    """Hàng bảng vé lẻ "| 1 | Tên | Địa giới | 200.000 | 40.000 |" ⇒ "người lớn 200.000 đồng · trẻ em 7–12 tuổi 40.000 đồng" (hai ô cuối = người lớn, trẻ em)."""
    o = [x.strip() for x in hang.strip().strip("|").split("|")]
    if len(o) < 2:
        return None
    gia = lambda x: f"{x} đồng" if re.fullmatch(r"[\d.]+", x) else x.lower() if x else None  # noqa: E731
    lon, tre = gia(o[-2]), gia(o[-1])
    return " · ".join(p for p in (f"người lớn {lon}" if lon else None, f"trẻ em 7–12 tuổi {tre}" if tre else None) if p) or None


def du_kien(noi: "thn.Noi | None", bang_the: "thn.Bang | None", bai_id: str | None, gio_bang: tuple[str, str] | None = None,
            ten: str = "") -> tuple[list[dict], list[dict]]:
    """Các dòng dữ kiện của MỘT điểm do code chép: (đoạn, nguồn). Nguồn đánh số từ 1 trong mục. Ô bảng không có ⇒ đoạn `thieu` (giờ mở cửa: mọi điểm;
    giá vé: chỉ di tích; địa chỉ: không có thì bỏ qua — thẻ lịch đã có nút bản đồ). `gio_bang` = (chữ giờ mở cửa, bài nguồn) của bảng điểm lịch — dùng khi
    bài không có dòng mở đầu bằng nhãn giờ (bảng điểm chép giờ từ câu văn của bài, kèm đường dẫn bài)."""
    doan, nguon = [], []

    def them_nguon(title: str, rel: str, muc: str, trich: list[str]) -> int:
        nguon.append({"id": len(nguon) + 1, "title": title, "bai_id": rel or None, "heading_path": [muc], "excerpts": trich})
        return len(nguon)

    dia_chi = next((d for d in (noi.dong if noi else ()) if _NHAN_DIA_CHI.match(d)), None)
    gio = next((d for d in (noi.dong if noi else ()) if _NHAN_GIO.match(d)), None)
    so_the = them_nguon(noi.ten, noi.rel, thn.MUC_THE, [d for d in (dia_chi, gio) if d]) if (dia_chi or gio) else None
    if dia_chi:
        chu = _NHAN_DIA_CHI.sub("", dia_chi).strip()
        if len(chu) > DIA_CHI_DAI and " (" in chu:
            chu = chu.split(" (", 1)[0].rstrip(" ,;")
        doan.append({"nhan": "Địa chỉ", "kieu": "van", "chu": f"{chu} [{so_the}]", "gach": None})
    if gio:
        doan.append({"nhan": "Giờ mở cửa", "kieu": "van", "chu": f"{_NHAN_GIO.sub('', gio).strip()} [{so_the}]", "gach": None})
    elif gio_bang and gio_bang[0] and gio_bang[1]:
        so = them_nguon(ten or (noi.ten if noi else ""), gio_bang[1], MUC_GIO_BANG, [gio_bang[0]])
        doan.append({"nhan": "Giờ mở cửa", "kieu": "van", "chu": f"{gio_bang[0][:1].upper()}{gio_bang[0][1:]} [{so}]", "gach": None})
    else:
        doan.append({"nhan": "Giờ mở cửa", "kieu": "thieu", "chu": None, "gach": None})
    ve = _ve_chu(noi.ve) if noi and noi.ve else None
    if ve:
        so_ve = them_nguon(bang_the.ve_tieu_de, bang_the.ve_rel, thn.MUC_VE, [d for d in (bang_the.ve_dau, noi.ve) if d])
        doan.append({"nhan": "Giá vé", "kieu": "van", "chu": f"{ve[:1].upper()}{ve[1:]} [{so_ve}]", "gach": None})
    elif (bai_id or "").startswith(NHOM_CO_VE):
        doan.append({"nhan": "Giá vé", "kieu": "thieu", "chu": None, "gach": None})
    return doan, nguon


def loc_y(y_model: list[dict], hop_le: set[int], tran: int, cam_gio_gia: bool = True) -> tuple[list[str], dict]:
    """Các ý model trả (`{chu, nguon}`) ⇒ các dòng gạch "chữ [n][m]" đã qua luật của code + số đếm lý do bỏ. Giữ khi: có chữ, ≤ `TRAN_KY_TU` ký tự, có ít
    nhất một số nguồn hợp lệ (số lạ bị gỡ khỏi ý), không chứa giờ / giá (`cam_gio_gia`). Nhiều hơn `tran` ý ⇒ lấy `tran` ý đầu."""
    giu, bo = [], {"khong_nguon": 0, "qua_dai": 0, "gio_gia": 0, "qua_tran": 0}
    for y in y_model or ():
        chu = " ".join(_MA.sub("", _nfc(str(y.get("chu") or ""))).split())
        so = [n for n in dict.fromkeys(y.get("nguon") or ()) if isinstance(n, int) and n in hop_le]
        if not chu:
            continue
        if not so:
            bo["khong_nguon"] += 1
        elif len(chu) > TRAN_KY_TU:
            bo["qua_dai"] += 1
        elif cam_gio_gia and _GIO_GIA.search(chu):
            bo["gio_gia"] += 1
        elif len(giu) >= tran:
            bo["qua_tran"] += 1
        else:
            giu.append(chu + " " + "".join(f"[{n}]" for n in so))
    return giu, bo


def khoi_model(ten_khoi: str, y_model: list[dict], hop_le: set[int], cam_gio_gia: bool = True) -> tuple[dict, dict]:
    """Một danh sách của model ⇒ MỘT đoạn: `gach` khi còn ý sau khi lọc, không thì `thieu` (khuôn "Kho chưa có" do giao diện in)."""
    giu, bo = loc_y(y_model, hop_le, TRAN_Y[ten_khoi], cam_gio_gia)
    if giu:
        return {"nhan": NHAN[ten_khoi], "kieu": "gach", "chu": None, "gach": giu}, bo
    return {"nhan": NHAN[ten_khoi], "kieu": "thieu", "chu": None, "gach": None}, bo


def nguon_da_dung(doan: list[dict], nguon: list[dict]) -> list[dict]:
    """Chỉ giữ nguồn có số xuất hiện trong chữ của mục (số giữ nguyên — không đánh lại, để [n] trong chữ vẫn trỏ đúng)."""
    co = {int(n) for d in doan for chu in ([d["chu"]] if d.get("chu") else []) + list(d.get("gach") or ()) for n in re.findall(r"\[(\d+)\]", chu)}
    return [s for s in nguon if s["id"] in co]


def tach_ma(doan: list[dict]) -> list[dict]:
    """Bước CUỐI trước khi gửi ra giao diện: gỡ mã [n] khỏi chữ, đưa số nguồn thành danh sách riêng — `so` cho `chu`, `gach_so` (song song với `gach`) cho
    từng dòng gạch. Vì sao: sản phẩm không hiện số tham chiếu chen trong chữ (chủ dự án nhắc lại 21:4x 24/11/2026 khi xem trang sổ tay); mã vẫn cần ở tầng
    dữ liệu để code kiểm ý nào có nguồn hợp lệ và để giao diện biết dòng nào dựa vào nguồn nào."""
    def tach(chu: str) -> tuple[str, list[int]]:
        return " ".join(_MA.sub("", chu).split()), [int(n) for n in dict.fromkeys(re.findall(r"\[(\d+)\]", chu))]
    ra = []
    for d in doan:
        chu, so = tach(d["chu"]) if d.get("chu") else (d.get("chu"), [])
        cap = [tach(g) for g in d.get("gach") or ()]
        ra.append({"nhan": d["nhan"], "kieu": d["kieu"], "chu": chu, "so": so, "gach": [c for c, _ in cap] if d.get("gach") is not None else None,
                   "gach_so": [s for _, s in cap] if d.get("gach") is not None else None})
    return ra


def muc_an_uong(an: list[dict]) -> tuple[list[dict], list[dict]]:
    """Mục ăn uống của một ngày = đúng quán gợi ý của lịch (`quan_lich.an_uong`), không gọi model. Quán có bài kho ⇒ một nguồn trỏ bài đó; quán chưa có
    bài ⇒ giữ nhãn của lịch ("chưa kiểm"…), không số nguồn. Bữa có ghi chú ăn riêng của điểm ⇒ in ghi chú đó."""
    doan, nguon = [], []
    for a in an:
        nhan = f"{NHAN_BUA.get(a['bua'], a['bua'])} — gần {a['gan']}" if a.get("gan") else NHAN_BUA.get(a["bua"], a["bua"])
        if a.get("ghi_chu"):
            doan.append({"nhan": nhan, "kieu": "gach", "chu": None, "gach": [a["ghi_chu"]]})
            continue
        gach = []
        for q in a.get("quan") or ():
            chu = q["ten"] + (f" ({q['loai']})" if q.get("loai") else "") + (f" — {q['nhan']}" if q.get("nhan") else "")
            if q.get("bai_id"):
                nguon.append({"id": len(nguon) + 1, "title": q["ten"], "bai_id": q["bai_id"], "heading_path": [MUC_QUAN], "excerpts": []})
                chu += f" [{len(nguon)}]"
            gach.append(chu)
        doan.append({"nhan": nhan, "kieu": "gach", "chu": None, "gach": gach} if gach else {"nhan": nhan, "kieu": "thieu", "chu": None, "gach": None})
    return doan, nguon


def doan_chung(lich: dict, an_toan: str | None) -> list[dict]:
    """Các dòng do code của mục "Trước khi đi" (đứng SAU khối "Đi lại" của model): câu an toàn của lượt đã lưu cùng lịch (bão / lũ) nếu có · dòng nhắc mùa
    mưa của chính lịch nếu lịch có · dòng cố định "có thể đã thay đổi" (sổ tay in giờ và giá chép từ kho)."""
    doan = [{"nhan": None, "kieu": "an_toan", "chu": c, "gach": None}
            for c in ([an_toan] if an_toan else []) + [g["cau"] for g in lich.get("ghi_chu") or () if g.get("ma") == "mua_mua"]]
    doan.append({"nhan": "Lưu ý chung", "kieu": "van", "chu": MAY_HAVE_CHANGED_NOTICE, "gach": None})
    return doan


def _tu(chu: str) -> list[str]:
    return _TU.findall(_nfc(chu).casefold())


def xep_trong_bai(doan_bai: list, cum: str = CUM_TRONG_BAI) -> list:
    """Các đoạn của MỘT bài xếp theo điểm từ khoá (BM25 tính riêng trong bài) với `cum`; bằng điểm ⇒ đoạn đứng trước trong bài trước."""
    chu = [_tu(" ".join([" ".join(d.metadata.get("heading_path") or ()), d.text or ""])) for d in doan_bai]
    n, tb = len(doan_bai), (sum(len(t) for t in chu) / len(doan_bai)) if doan_bai else 1.0
    co = {}
    for t in chu:
        for w in set(t):
            co[w] = co.get(w, 0) + 1
    hoi = set(_tu(cum))

    def diem(t: list[str]) -> float:
        return sum(math.log(1 + (n - co[w] + 0.5) / (co[w] + 0.5)) * t.count(w) * 2.2 / (t.count(w) + 1.2 * (0.25 + 0.75 * len(t) / (tb or 1.0)))
                   for w in hoi if w in co and w in t)
    return [d for _, _, d in sorted(((-round(diem(t), 6), i, d) for i, (t, d) in enumerate(zip(chu, doan_bai))), key=lambda x: x[:2])]


def chon_bang_chung(ket_qua_tim: list, doan_bai: list, bai_id: str | None, k: int = SO_DOAN_BANG_CHUNG, ten_rieng: str | None = None) -> list:
    """Bằng chứng cho mục của một điểm, nhiều nhất `k` đoạn. Điểm có bài riêng trong chỉ mục ⇒ CHỈ đoạn của bài đó: tới `SO_DOAN_TU_TIM` đoạn theo thứ hạng
    của lần tìm chung, phần còn lại theo `xep_trong_bai`. Điểm không có bài riêng (hoặc bài không có đoạn nào) ⇒ kết quả tìm như nó vốn có.
    Vì sao không lấy thẳng kết quả tìm (bản đầu, lượt thật 24/11/2026): mục Đại Nội nhận 8 đoạn của bài vé và bài dịch vụ ⇒ "Nên xem" toàn máy thuyết minh,
    xe điện."""
    if not bai_id or not doan_bai:
        return list(ket_qua_tim)[:k]
    if ten_rieng:  # điểm KHÔNG có bài riêng (bảng 16: Trung tâm Nghệ thuật Lê Bá Đảng lấy tư liệu từ bài phố đi bộ): `bai_id` = bài bảng điểm trỏ tới ⇒ chỉ
        # các đoạn của bài đó CÓ NHẮC tên điểm (tìm chung theo tên dễ mang về bài của một nơi khác trùng tên — "Không gian lưu niệm Lê Bá Đảng")
        ten = " ".join(_tu(ten_rieng))
        return [d for d in xep_trong_bai(doan_bai, ten_rieng) if ten in " ".join(_tu(d.text or ""))][:SO_DOAN_TU_TIM]
    tu_tim = [d for d in ket_qua_tim if d.metadata.get("source") == bai_id][:SO_DOAN_TU_TIM]
    da_co = {d.id for d in tu_tim}
    return (tu_tim + [d for d in xep_trong_bai(doan_bai) if d.id not in da_co])[:k]
