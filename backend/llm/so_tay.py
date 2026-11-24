"""Công tắc `so_tay` — SỔ TAY CHO CHUYẾN ĐI dựng từ lịch đang lưu của cuộc (bản thử, nhánh thu-b-so-tay; chủ dự án chọn 21:21 24/11/2026 sau khi xem
hai hồ sơ mẫu: "Đúng, làm cả hai kiểu", sổ tay trước).

Chia việc code ↔ model (luật nền: thứ phải luôn đúng do code làm):
- DÀN Ý do code lấy từ lịch: mỗi điểm một mục, mỗi ngày một mục ăn uống, cuối cùng "Trước khi đi".
- ĐỊA CHỈ / GIỜ MỞ CỬA / GIÁ VÉ do code chép từ bảng "thẻ nơi" (`the_noi.Bang`: dòng chép nguyên từ bài riêng + hàng bảng vé lẻ); ăn uống = đúng quán gợi ý
  của lịch (`lich["an"]`). Model KHÔNG viết giờ / giá: ý nào của model chứa giờ hoặc giá bị bỏ (`loc_y`).
- Model chỉ viết hai danh sách ngắn cho mỗi điểm ("Nên xem", "Lưu ý") và một danh sách "Đi lại", mỗi ý kèm số nguồn; code giữ ĐỘ DÀI (số ý, số ký tự) và
  bỏ ý không có nguồn hợp lệ.
- Ô thiếu là MỘT khuôn do code đặt (`kieu: "thieu"`): ô dữ kiện bài không có DÒNG NHÃN để chép, hoặc danh sách model trả rỗng / bị bỏ hết. Model không tự
  viết câu thiếu. NGHĨA của ô này là "sổ tay chưa ghi được dòng này", KHÔNG phải "kho không có": bài có thể nói điều đó trong câu văn (Đồi Vọng Cảnh "mở tự
  do 24/24", Chùa Từ Hiếu "không niêm yết giờ") mà code không chép được. Giao diện in "Sổ tay chưa ghi được: … — mở bài của điểm để xem, hoặc hỏi Trợ lý"
  (phiên đo nêu, phiên điều phối quyết 24/11/2026; bản đầu in "Kho chưa có" là nói quá về kho).

Vì sao không dùng vòng hỏi đáp cho từng mục (cách của hai hồ sơ mẫu, `data/x15_phan_ai_2026-11-23/b_ho_so_mau/KET_QUA.md`): 3,2 lời gọi + định tuyến mỗi
mục, 78–87 giây cho 11 mục; độ dài không do code giữ; các mục cãi nhau về số (mục này "kho chưa có khoảng cách", mục kia "khoảng 7 km"; "vé lẻ mỗi lăng
150.000 đồng" trong khi ba lăng giá khác); dấu "kho chưa có" lúc là câu cố định lúc là lời tự do.

Giới hạn đã biết: sổ tay KHÔNG đi qua lớp "Lưu ý trong nguồn" của hỏi đáp (`llm/luu_y_nguon.py` — câu "tạm ngừng / lũ, bão" của bài được nối vào dòng ghi
chú). Phiên đo đếm 24/11/2026: 1 / 47 điểm của bảng (Thác Nhị Hồ) có câu như vậy và đoạn đó không nằm trong 8 đoạn được chọn.

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
# Hai chỗ dành riêng cho đoạn LỜI DẶN, xếp bằng cụm riêng: xếp chung một cụm thì đoạn "Thông tin dành cho du khách" của bài Chùa Từ Hiếu đứng hạng 9 / 19
# (ngoài 8 đoạn được chọn) ⇒ mục "Lưu ý" rỗng dù bài có lời dặn; xếp riêng thì nó đứng hạng 1 (đếm 0 đồng 24/11/2026).
CUM_LOI_DAN = "lưu ý du khách trang phục ứng xử quy tắc nên không được giữ yên lặng xin phép an toàn giày"
SO_DOAN_LOI_DAN = 2
CAU_TIM_DI_LAI = "Đi lại giữa các điểm tham quan ở Huế: taxi, xe máy, xe đạp, xích lô, thuyền"
# Một VẾ câu của model NÓI VỀ giờ mở cửa hoặc giá ⇒ vế đó bị gỡ (`go_ve_gio_gia`): hai thứ này chỉ đi đường code chép. Phải có ĐỦ hai dấu hiệu mới tính:
# từ về mở / đóng cửa + một mốc giờ hay ngày; hoặc từ về vé / phí + một số tiền; hoặc câu nói rõ không thu tiền / không bán vé / không niêm yết giờ.
# KHÔNG tính: giờ trong ngày nói về cảnh ("bình minh 04h30 – 06h00"), giờ nên đi, số không phải tiền ("2 triệu lượt khách", "11.000 hiện vật"), "đã đóng
# cửa vĩnh viễn", "vé xe không gồm vé vào cổng", "bãi gửi xe miễn phí".
# Lịch sử (đều thấy trên lượt thật 24/11/2026): luật "mọi con số giờ" làm mục Đầm Chuồn mất hết ý "Nên xem"; phiên đo dò 22 câu: lọt 8, bỏ oan 4; bản một
# mẫu chữ gỡ mất vế "nay đã đóng cửa vĩnh viễn" của một quán (người đọc tưởng quán còn mở) và vế "vé xe không gồm vé vào cổng".
_SO_TIEN = re.compile(r"\d[\d.,]*\s*(?:đồng|đ\b|vnd|vnđ|k\b)|\d[\d.,]*\s*(?:nghìn|ngàn|triệu)(?!\s*(?:lượt|người|khách|m\b|m²|m2|km|ha|năm))")
_SO_NGHIN = re.compile(r"\d{2,3}\.\d{3}")
_TU_VE = re.compile(r"\bvé\b|\bphí\b|người lớn|trẻ em")
_KHONG_THU = re.compile(r"không (?:thu|mất) (?:phí|tiền)|không bán vé|vào (?:cửa|cổng) tự do|không niêm yết|giờ mở cửa|ngừng bán vé")
_MIEN_PHI_VE = re.compile(r"miễn phí[^,;.]*(?:\bvé\b|vào cửa|vào cổng|tham quan)|(?:\bvé\b|vào cửa|vào cổng|tham quan)[^,;.]*miễn phí")
_MO_DONG = re.compile(r"mở cửa|đóng cửa|giờ mở|mở từ|mở (?:cho|đón) khách|đón khách|hoạt động từ|nghỉ trưa|tham quan được từ")
_MOC_GIO = re.compile(r"\d{1,2}\s*(?:h|g|:)\s*\d{0,2}(?!\w)|\b\d{1,2}\s*giờ\b|thứ (?:hai|ba|tư|năm|sáu|bảy)|chủ nhật|hằng ngày|hàng ngày|cả ngày|cả tuần")


_PHU_THUOC = re.compile(r"(?:trừ|ngoại trừ|kể cả|riêng|trong đó|sau đó)\b", re.IGNORECASE)
_TIEN_KHONG_SO = re.compile(r"miễn phí|\bgiảm\b|phụ thu|trả thêm", re.IGNORECASE)


def noi_gio_gia(ve: str) -> bool:
    """Một vế câu có nói giờ mở cửa hoặc giá không (xem chú thích trên)."""
    v = _nfc(ve).casefold()
    return bool(_SO_TIEN.search(v) or (_SO_NGHIN.search(v) and _TU_VE.search(v)) or _KHONG_THU.search(v) or _MIEN_PHI_VE.search(v)
                or (_MO_DONG.search(v) and _MOC_GIO.search(v)))


_TU = re.compile(r"[^\W_]+", re.UNICODE)
DIA_CHI_DAI = 120   # dòng địa chỉ dài hơn ⇒ cắt ở dấu ngoặc đầu (phần trong ngoặc của kho là lịch sử địa giới hành chính); nguồn vẫn giữ nguyên dòng
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


def du_kien(noi: "thn.Noi | None", bang_the: "thn.Bang | None", bai_id: str | None) -> tuple[list[dict], list[dict]]:
    """Các dòng dữ kiện của MỘT điểm do code chép NGUYÊN từ bài kho (bảng thẻ nơi): (đoạn, nguồn). Nguồn đánh số từ 1 trong mục. Bài không có dòng mở đầu bằng
    nhãn ⇒ đoạn `thieu` (giờ mở cửa: mọi điểm; giá vé: chỉ di tích; địa chỉ: không có thì bỏ qua — thẻ lịch đã có nút bản đồ).
    KHÔNG lấy giờ từ bảng điểm của lịch (`gio_mo_cua`): đó là sổ ghi chú của nhóm, không phải câu của bài — phiên đo nạp bảng thật 24/11/2026: 16 / 19 dòng
    mang chữ nội bộ ("Kho: không niêm yết giờ; web lệch…"), một dòng là giờ từ trang web ngoài kho."""
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
    else:
        doan.append({"nhan": "Giờ mở cửa", "kieu": "thieu", "chu": None, "gach": None})
    ve = _ve_chu(noi.ve) if noi and noi.ve else None
    if ve:
        so_ve = them_nguon(bang_the.ve_tieu_de, bang_the.ve_rel, thn.MUC_VE, [d for d in (bang_the.ve_dau, noi.ve) if d])
        doan.append({"nhan": "Giá vé", "kieu": "van", "chu": f"{ve[:1].upper()}{ve[1:]} [{so_ve}]", "gach": None})
    elif (bai_id or "").startswith(NHOM_CO_VE):
        doan.append({"nhan": "Giá vé", "kieu": "thieu", "chu": None, "gach": None})
    return doan, nguon


VE_CON_LAI_NGAN = 25   # sau khi gỡ vế nói giờ / giá, phần còn lại ngắn hơn chừng này ký tự ⇒ bỏ cả ý


def go_ve_gio_gia(chu: str) -> str | None:
    """Ý có vế nói giờ mở cửa / giá: gỡ ĐÚNG các vế đó (vế = phần giữa hai dấu phẩy / chấm phẩy), giữ phần còn lại khi nó còn đủ dài; trả None khi không còn
    gì đáng giữ. Ý không có vế nào như vậy ⇒ trả nguyên. Vì sao không bỏ cả ý (bản trước): bài Chùa Từ Hiếu viết "không niêm yết giờ mở cửa hay vé chính
    thức, nên đến vào ban ngày… mặc trang phục kín đáo" — model gộp thành một ý, bỏ cả ý làm mục "Lưu ý" rỗng trong khi bài có lời dặn (phiên đo 24/11/2026)."""
    ve = re.split(r"[,;]\s+", chu)
    giu = [v for v in ve if not noi_gio_gia(v)]
    if len(giu) == len(ve):
        return chu
    con = re.sub(r"^(?:và|nhưng|còn|song)\s+", "", ", ".join(giu).strip(" .,;"), flags=re.IGNORECASE)
    # phần còn lại đứng không vững sau khi mất vế trước (phiên đo dò 24/11/2026): mở đầu bằng từ phụ thuộc vế đã gỡ ("Trừ các dịp lễ lớn…"), hoặc còn nói
    # tiền bằng từ không kèm số ("miễn phí cho trẻ dưới 7 tuổi", "người cao tuổi được giảm một nửa") ⇒ bỏ cả ý
    if len(con) < VE_CON_LAI_NGAN or _PHU_THUOC.match(con) or _TIEN_KHONG_SO.search(con):
        return None
    return con[:1].upper() + con[1:] + ("" if con.endswith((".", "!", "?")) else ".")


def loc_y(y_model: list[dict], hop_le: set[int], tran: int, cam_gio_gia: bool = True, nguon_uu_tien: frozenset = frozenset()) -> tuple[list[str], dict]:
    """Các ý model trả (`{chu, nguon}`) ⇒ các dòng gạch "chữ [n][m]" đã qua luật của code + số đếm lý do bỏ. Giữ khi: có chữ, ≤ `TRAN_KY_TU` ký tự, có ít
    nhất một số nguồn hợp lệ (số lạ bị gỡ khỏi ý), không nói giờ mở cửa / giá (`cam_gio_gia`: vế nói giờ / giá bị gỡ — `go_ve_gio_gia`; không còn gì thì bỏ
    cả ý; ý bị gỡ một phần ghi lý do `gio_gia_cat` trong `chu` để soát). Nhiều hơn `tran` ý ⇒ lấy `tran` ý đầu."""
    giu, bo = [], {"khong_nguon": 0, "qua_dai": 0, "gio_gia": 0, "qua_tran": 0, "chu": []}  # `chu`: (lý do, chữ) của từng ý bị bỏ — route ghi log để soát bỏ oan
    for y in y_model or ():
        chu = " ".join(_MA.sub("", _nfc(str(y.get("chu") or ""))).split())
        so = [n for n in dict.fromkeys(y.get("nguon") or ()) if isinstance(n, int) and n in hop_le]
        if not chu:
            continue
        con = go_ve_gio_gia(chu) if cam_gio_gia else chu
        ly_do = ("khong_nguon" if not so else "qua_dai" if len(chu) > TRAN_KY_TU else "gio_gia" if con is None
                 else "qua_tran" if len(giu) >= tran and not nguon_uu_tien & set(so) else None)  # ý dẫn đoạn cảnh báo an toàn không bị trần số ý cắt
        if ly_do is None and con != chu:  # gỡ một phần: ý vẫn được giữ, ghi lại chữ gốc để soát
            bo["chu"].append(("gio_gia_cat", chu))
            chu = con
        if ly_do:
            bo[ly_do] += 1
            bo["chu"].append((ly_do, chu))
        else:
            giu.append(chu + " " + "".join(f"[{n}]" for n in so))
    return giu, bo


def khoi_model(ten_khoi: str, y_model: list[dict], hop_le: set[int], cam_gio_gia: bool = True, nguon_uu_tien: frozenset = frozenset()) -> tuple[dict, dict]:
    """Một danh sách của model ⇒ MỘT đoạn: `gach` khi còn ý sau khi lọc, không thì `thieu` (khuôn "Kho chưa có" do giao diện in)."""
    giu, bo = loc_y(y_model, hop_le, TRAN_Y[ten_khoi], cam_gio_gia, nguon_uu_tien)
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


def muc_an_uong(an: list[dict], bang_the: "thn.Bang | None" = None) -> tuple[list[dict], list[dict]]:
    """Mục ăn uống của một ngày = đúng quán gợi ý của lịch (`quan_lich.an_uong`), không gọi model. Quán có bài kho ⇒ một nguồn trỏ bài đó, kèm dòng địa chỉ
    và giờ hoạt động code chép từ bài của quán (bảng thẻ nơi) khi bài có; quán chưa có bài ⇒ giữ nhãn của lịch ("chưa kiểm"…), không số nguồn. Bữa có ghi
    chú ăn riêng của điểm ⇒ in ghi chú đó."""
    the = {n.rel: n for n in (bang_the.noi if bang_the else ())}
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
                noi = the.get(q["bai_id"])
                dia_chi = next((_NHAN_DIA_CHI.sub("", d).strip() for d in (noi.dong if noi else ()) if _NHAN_DIA_CHI.match(d)), None)
                gio = next((_NHAN_GIO.sub("", d).strip() for d in (noi.dong if noi else ()) if _NHAN_GIO.match(d)), None)
                if dia_chi and len(dia_chi) > DIA_CHI_DAI and " (" in dia_chi:
                    dia_chi = dia_chi.split(" (", 1)[0].rstrip(" ,;")
                chu += "".join(f" · {nhan}: {x.rstrip('.')}" for nhan, x in (("địa chỉ", dia_chi), ("giờ", gio)) if x)
                nguon.append({"id": len(nguon) + 1, "title": q["ten"], "bai_id": q["bai_id"], "heading_path": [MUC_QUAN if not (dia_chi or gio) else thn.MUC_THE],
                              "excerpts": [d for d in (noi.dong if noi else ()) if _NHAN_DIA_CHI.match(d) or _NHAN_GIO.match(d)]})
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


# CẢNH BÁO AN TOÀN của bài phải đi theo sổ tay. Lượt thật trên main 24/11/2026 (lịch 4 ngày thiên nhiên): 9 / 12 điểm không có ý cảnh báo theo mùa nào —
# đoạn "mùa mưa lũ: tạm dừng bơi lội", "sạt lở", "cấm tắm" của bài không nằm trong các đoạn được chọn (phiên đo đếm: lọt ở 3 / 10 điểm thiên nhiên của bảng).
# Mỗi bài: đoạn khớp nhiều NHÓM dấu hiệu nhất được thêm vào bằng chứng (ngoài trần); ý "Lưu ý" dẫn đoạn đó không bị trần số ý cắt; không ý nào dẫn nó ⇒ code
# thêm một dòng `an_toan` trỏ tới đúng mục của bài (code không tóm tắt nội dung cảnh báo, chỉ trỏ).
MAU_CANH_BAO = tuple(re.compile(m, re.IGNORECASE) for m in (
    r"cấm tắm|không (?:được|nên) (?:tắm|bơi|ra bờ)|tránh leo|tạm (?:dừng|ngừng) (?:bơi|tắm|đón khách|hoạt động|tham quan)", r"biển động|sóng (?:lớn|to)|dòng chảy xa bờ|nước xiết|xoáy",
    r"lũ quét|sạt lở|lũ ống|ngập lụt|nước dâng", r"đuối nước|nguy hiểm|tai nạn|cảnh báo", r"mùa mưa (?:bão|lũ)|mùa lũ|mưa bão|bão lũ|áp thấp nhiệt đới|[dg]i?ông (?:sét|lốc)",
    r"trơn trượt|trơn trợt|dốc đứng"))
_MUC_AN_TOAN = re.compile(r"an toàn|lưu ý|mùa|thời tiết|cảnh báo|dành cho du khách", re.IGNORECASE)  # tên mục của bài hay chứa phần cảnh báo
_LOI_DAN_CANH_BAO = re.compile(r"\bnên\b|\bkhông\b|\bcấm\b|tránh|hạn chế|tuyệt đối|\bphải\b|cẩn thận|lưu ý", re.IGNORECASE)
CAU_TRO_AN_TOAN = "Bài của điểm này có phần lưu ý an toàn ở mục «{muc}» — mở bài để đọc trước khi đi."


def doan_canh_bao(doan_bai: list):
    """Đoạn cảnh báo an toàn của MỘT bài: đoạn khớp nhiều nhóm dấu hiệu nhất của `MAU_CANH_BAO` (bằng nhau ⇒ đoạn đứng trước); phải khớp ít nhất HAI nhóm, hoặc một
    trong hai nhóm đầu (cấm / tạm dừng; biển động – nước xiết) — một chữ "nguy hiểm" hay "mùa mưa bão" đứng lẻ chưa đủ. Không có ⇒ None."""
    tot, diem_tot = None, 0
    for d in doan_bai:
        muc = " ".join(d.metadata.get("heading_path") or ())
        khop = [bool(m.search(f"{muc} {d.text or ''}")) for m in MAU_CANH_BAO]
        # đủ điều kiện rồi mới cộng điểm tên mục: đoạn nằm dưới mục "Mùa…", "Lưu ý…", "Thông tin dành cho du khách" được chọn trước đoạn kể chuyện lịch sử / địa mạo
        # có cùng số dấu hiệu (đếm 0 đồng trên 47 điểm 24/11/2026: Phá Tam Giang, Đầm Lập An từng ra mục "dấu ấn lịch sử", "địa mạo")
        diem = sum(khop) + (2 if _MUC_AN_TOAN.search(muc) else 0)
        if (sum(khop) >= 2 or khop[0] or khop[1]) and diem > diem_tot:
            tot, diem_tot = d, diem
    return tot


def la_y_canh_bao(dong: str, nguon_canh_bao) -> bool:
    """Một ý đã qua lọc (kết bằng "[n]…") là ý CẢNH BÁO khi nó dẫn một đoạn cảnh báo VÀ chữ của nó là lời cảnh báo: có câu cấm / tạm dừng, hoặc hai nhóm dấu hiệu,
    hoặc một dấu hiệu đi cùng lời dặn (một dấu hiệu lẻ như "che chắn sóng lớn" chưa phải cảnh báo)."""
    if nguon_canh_bao is not None and not {int(n) for n in re.findall(r"\[(\d+)\]", dong)} & set(nguon_canh_bao):
        return False  # `nguon_canh_bao=None`: chỉ xét chữ của ý, không xét nó dẫn đoạn nào
    khop = [bool(m.search(dong)) for m in MAU_CANH_BAO]
    return khop[0] or sum(khop) >= 2 or (any(khop) and bool(_LOI_DAN_CANH_BAO.search(dong)))


def _tu(chu: str) -> list[str]:
    return _TU.findall(_nfc(chu).casefold())


def xep_trong_bai(doan_bai: list, cum: str = CUM_TRONG_BAI, chi_khop: bool = False) -> list:
    """Các đoạn của MỘT bài xếp theo điểm từ khoá (BM25 tính riêng trong bài) với `cum`; bằng điểm ⇒ đoạn đứng trước trong bài trước. `chi_khop`: bỏ đoạn
    không khớp từ nào của cụm (điểm 0)."""
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
    return [d for am_diem, _, d in sorted(((-round(diem(t), 6), i, d) for i, (t, d) in enumerate(zip(chu, doan_bai))), key=lambda x: x[:2])
            if not chi_khop or am_diem < 0]


def chon_bang_chung(ket_qua_tim: list, doan_bai: list, bai_id: str | None, k: int = SO_DOAN_BANG_CHUNG, ten_rieng: str | None = None) -> list:
    """Bằng chứng cho mục của một điểm, nhiều nhất `k` đoạn. Điểm có bài riêng trong chỉ mục ⇒ CHỈ đoạn của bài đó: tới `SO_DOAN_TU_TIM` đoạn theo thứ hạng
    của lần tìm chung, rồi `SO_DOAN_LOI_DAN` đoạn lời dặn (`CUM_LOI_DAN`), phần còn lại theo `xep_trong_bai`. Điểm không có bài riêng (hoặc bài không có đoạn nào) ⇒ kết quả tìm như nó vốn có.
    Vì sao không lấy thẳng kết quả tìm (bản đầu, lượt thật 24/11/2026): mục Đại Nội nhận 8 đoạn của bài vé và bài dịch vụ ⇒ "Nên xem" toàn máy thuyết minh,
    xe điện."""
    if not bai_id or not doan_bai:
        return list(ket_qua_tim)[:k]
    if ten_rieng:  # điểm KHÔNG có bài riêng (bảng 16: Trung tâm Nghệ thuật Lê Bá Đảng lấy tư liệu từ bài phố đi bộ): `bai_id` = bài bảng điểm trỏ tới ⇒ chỉ
        # các đoạn của bài đó CÓ NHẮC tên điểm (tìm chung theo tên dễ mang về bài của một nơi khác trùng tên — "Không gian lưu niệm Lê Bá Đảng")
        ten = " ".join(_tu(ten_rieng))
        return [d for d in xep_trong_bai(doan_bai, ten_rieng) if ten in " ".join(_tu(d.text or ""))][:SO_DOAN_TU_TIM]
    chon = [d for d in ket_qua_tim if d.metadata.get("source") == bai_id][:SO_DOAN_TU_TIM]
    for xep, so in ((xep_trong_bai(doan_bai, CUM_LOI_DAN, chi_khop=True), SO_DOAN_LOI_DAN), (xep_trong_bai(doan_bai), k)):
        da_co = {d.id for d in chon}
        chon += [d for d in xep if d.id not in da_co][:so]
    chon = chon[:k]
    canh_bao = doan_canh_bao(doan_bai)  # thêm NGOÀI trần `k`: không đẩy đoạn nào ra
    return chon if canh_bao is None or canh_bao.id in {d.id for d in chon} else [*chon, canh_bao]
