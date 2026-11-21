"""Cờ `su_kien_theo_ngay` (20/11/2026) — hỏi "tối nay / cuối tuần này / tháng 3 ở Huế có lễ hội, sự kiện gì" ⇒ code tra MỘT bảng nhỏ chép từ kho
(`assistant.su_kien_bang`, file private trong `data/`: lễ hội có ngày hằng năm + hoạt động lặp theo tuần), đổi ngày âm ⇒ dương bằng `llm/ngay_lich.py`, đăng thành một
nguồn trong ngữ cảnh trước lần gọi model đầu. Model chỉ diễn đạt; ngày do code tính (luật: phép tính ngày ⇒ code).

Vì sao: câu "cuối tuần này có sự kiện gì" bị từ chối (đếm 12/11) vì không đoạn kho nào tự nói "tuần này có …" — phải có người đổi ngày âm của từng
lễ hội sang ngày dương rồi so với khoảng được hỏi. Bản này KHÔNG có sự kiện một lần của năm, KHÔNG có lễ hội "theo kế hoạch từng năm" (bài không
ghi ngày thì không nêu), KHÔNG hiện trong lịch "Lên kế hoạch".
Hàm thuần: bảng + câu gõ + ngày hôm nay ⇒ các dòng nguồn. Cổng HẸP: câu phải có cả từ chỉ khoảng ngày lẫn từ hỏi lễ hội / sự kiện; sót ⇒ y như cờ tắt.
"""
import datetime as dt
import json
import re
import unicodedata
from pathlib import Path

from llm import ngay_lich as nl

TIEU_DE_NGUON = "Lễ hội và hoạt động theo ngày — code tra từ các bài của kho"
MUC_NGUON = "Lễ hội có ngày hằng năm và hoạt động lặp theo tuần"
NGUON_SOURCE = "he-thong-su-kien"  # `source` của nguồn — không phải bài kho (không `bai_id`)
KHOANG_TOI_DA = 62  # ngày; khoảng hỏi dài hơn ⇒ không tra (danh sách sẽ thành "cả năm")
CAU_CUOI = ("Ngày trên do hệ thống đổi từ ngày ghi trong bài của kho; ban tổ chức có thể đổi ngày từng năm. Lễ hội tổ chức theo kế hoạch từng năm và sự kiện "
            "chỉ có một lần không nằm trong danh sách này.")

_THANG_CHU = {"giêng": 1, "hai": 2, "ba": 3, "tư": 4, "năm": 5, "sáu": 6, "bảy": 7, "tám": 8, "chín": 9, "mười": 10, "mười một": 11, "chạp": 12,
              "mười hai": 12}
# Từ hỏi LỄ HỘI / SỰ KIỆN — theo danh từ, không theo chữ "có gì" trần ("cuối tuần này thời tiết có gì đáng lo" không phải hỏi sự kiện).
_HOI = re.compile(r"(?<!\w)(?:lễ hội|sự kiện|festival|hội hè|hoạt động (?:gì|nào|văn hoá|văn hóa|vui chơi|giải trí)|chương trình (?:gì|nào|biểu diễn|nghệ thuật)|"
                  r"biểu diễn (?:gì|nào)|có gì (?:vui|chơi|hay|đặc biệt|đáng xem|diễn ra)|có gì (?:không|ko|k)\s*[?.!]*$|"  # "có gì không" chỉ khi đứng CUỐI câu (review B)
                  r"(?:ở|tại) huế có gì\s*\??$)", re.I)
_KHONG_HOI = re.compile(r"(?<!\w)(?:thời tiết|mưa|nắng|bão|lũ|lụt|giông|dông|nhiệt độ|giá vé|bao nhiêu tiền|mở cửa|đóng cửa)(?!\w)", re.I)
# Hỏi về QUÁ KHỨ ("tháng 3 năm ngoái", "tuần trước", "cuối tuần vừa rồi") ⇒ không tra: bảng chỉ tính lần SẮP TỚI (bộ dò mù của E 20/11)
_QUA_KHU = re.compile(r"(?<!\w)(?:năm ngoái|năm trước|năm rồi|hôm qua|hôm kia|tuần trước|tuần rồi|tháng trước|tháng rồi|vừa rồi|vừa qua|đã qua|trước đây|hồi (?:đó|trước|xưa))(?!\w)", re.I)
_NGAY_SO = re.compile(r"(?<![\d/])(\d{1,2})/(\d{1,2})(?:/(\d{4}))?(?![\d/])")
_NGAY_CHU = re.compile(r"(?<!\w)ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})(?:\s+năm\s+(\d{4}))?(?!\s*âm)(?!\w)", re.I)
_THANG_AM = re.compile(r"(?<!\w)tháng\s+(giêng|chạp|\d{1,2})\s+âm(?:\s+lịch)?(?!\w)", re.I)
_THANG_DUONG = re.compile(r"(?<!\w)tháng\s+(\d{1,2})(?:\s+năm\s+(\d{4}))?(?!\s*âm)(?!\w)", re.I)


def nap_bang(path: Path) -> tuple[dict, ...]:
    """Đọc bảng; sai khuôn ⇒ ném ngay lúc khởi động (không chạy với bảng hỏng)."""
    dong = json.loads(Path(path).read_text(encoding="utf-8"))["dong"]
    for d in dong:
        if d["lich"] == "tuan":
            assert d["thu"] and all(0 <= t <= 6 for t in d["thu"]), d["ten"]
        else:
            assert d["lich"] in ("am", "duong") and len(d["tu"]) == 2 and len(d["den"]) == 2, d["ten"]
        assert d["ten"] and d["bai"] and d["chu"], d
    return tuple(dong)


def hoi_su_kien(cau: str) -> bool:
    return bool(_HOI.search(cau)) and not _KHONG_HOI.search(cau) and not _QUA_KHU.search(cau)


def _cuoi_thang_am(dau: dt.date) -> dt.date:
    am = nl.solar_to_lunar(dau)
    d = dau + dt.timedelta(days=28)
    while (nxt := nl.solar_to_lunar(d + dt.timedelta(days=1))).month == am.month and nxt.leap == am.leap:
        d += dt.timedelta(days=1)
    return d


def _cac_khoang(c: str, hom: dt.date) -> list[tuple[int, dt.date, dt.date, str, bool]]:
    """Mọi khoảng ngày chữ `c` (đã chuẩn hoá) nêu ⇒ [(vị trí trong chữ, từ, đến, nhãn, là MỘT ngày ghi bằng số)], xếp theo THỨ TỰ ƯU TIÊN của các luật
    (danh sách dạng ĐÓNG, như trước 21/11: ngày ghi số · hôm nay · mai · cuối tuần · tuần · tháng âm · tháng này / sau · tháng dương) ⇒ phần tử đầu là đáp
    án của bản cũ. Chỗ chữ đã được một luật đứng trước nhận thì luật sau không nhận lại ("cuối tuần này" không thành thêm "tuần này"). Tuần tính từ thứ Hai."""
    mot = dt.timedelta(days=1)
    dau_tuan = hom - dt.timedelta(days=hom.weekday())
    ra, da_nhan = [], []

    def trong(m) -> bool:
        return any(m.start() < b and a < m.end() for a, b in da_nhan)

    def them(m, tu, den, nhan, ngay_so=False):
        da_nhan.append((m.start(), m.end()))
        ra.append((m.start(), tu, den, nhan, ngay_so))

    for mau in (_NGAY_SO, _NGAY_CHU):
        for m in mau.finditer(c):
            if trong(m):
                continue
            nam = int(m.group(3)) if m.group(3) else hom.year
            try:
                d = dt.date(nam, int(m.group(2)), int(m.group(1)))
            except ValueError:
                da_nhan.append((m.start(), m.end()))  # ngày không có thật ("31/2"): giữ chỗ để luật sau không đọc nhầm, không ra khoảng
                continue
            if not m.group(3) and d < hom:  # không nêu năm, ngày đã qua ⇒ lần tới
                d = dt.date(nam + 1, d.month, d.day)
            them(m, d, d, f"ngày {d:%d/%m/%Y}", True)
    cuoi_thang = (hom.replace(day=1) + dt.timedelta(days=32)).replace(day=1) - mot
    dau_thang_sau = (hom.replace(day=1) + dt.timedelta(days=32)).replace(day=1)
    for mau, tu, den, nhan in (
            (r"(?<!\w)(?:hôm nay|bữa nay|(?:sáng|trưa|chiều|tối|đêm) nay)(?!\w)", hom, hom, "hôm nay"),
            (r"(?<!\w)(?:ngày mai|(?:sáng|trưa|chiều|tối|đêm) mai)(?!\w)", hom + mot, hom + mot, "ngày mai"),
            (r"(?<!\w)cuối tuần (?:sau|tới)(?!\w)", dau_tuan + 12 * mot, dau_tuan + 13 * mot, "cuối tuần sau"),
            (r"(?<!\w)cuối tuần(?!\w)", max(hom, dau_tuan + 5 * mot), dau_tuan + 6 * mot, "cuối tuần này"),
            (r"(?<!\w)tuần (?:sau|tới)(?!\w)", dau_tuan + 7 * mot, dau_tuan + 13 * mot, "tuần sau"),
            (r"(?<!\w)tuần này(?!\w)", hom, dau_tuan + 6 * mot, "tuần này (từ hôm nay)")):
        for m in re.finditer(mau, c):
            if not trong(m):
                them(m, tu, den, nhan)
    for m in _THANG_AM.finditer(c):
        if trong(m):
            continue
        thang = _THANG_CHU.get(m.group(1)) or int(m.group(1))
        da_nhan.append((m.start(), m.end()))  # "tháng 13 âm": không ra khoảng, và không để luật tháng dương đọc lại
        if not 1 <= thang <= 12:
            continue
        nam_am = nl.solar_to_lunar(hom).year
        for nam in (nam_am, nam_am + 1):
            dau = nl.ngay_duong(1, thang, nam, "am")
            if isinstance(dau, dt.date) and (cuoi := _cuoi_thang_am(dau)) >= hom:
                ra.append((m.start(), dau, cuoi, f"tháng {m.group(1)} âm lịch", False))
                break
    for mau, tu, den, nhan in ((r"(?<!\w)tháng này(?!\w)", hom, cuoi_thang, "tháng này (từ hôm nay)"),
                               (r"(?<!\w)tháng (?:sau|tới)(?!\w)", dau_thang_sau, (dau_thang_sau + dt.timedelta(days=32)).replace(day=1) - mot, "tháng sau")):
        for m in re.finditer(mau, c):
            if not trong(m):
                them(m, tu, den, nhan)
    for m in _THANG_DUONG.finditer(c):
        if trong(m):
            continue
        thang = int(m.group(1))
        if not 1 <= thang <= 12:
            continue
        nam = int(m.group(2)) if m.group(2) else (hom.year if thang >= hom.month else hom.year + 1)
        dau = dt.date(nam, thang, 1)
        them(m, dau, (dau + dt.timedelta(days=32)).replace(day=1) - mot, f"tháng {thang}/{nam}")
    return ra


def _mot_khoang(ds: list) -> tuple[dt.date, dt.date, str] | None:
    """Một khoảng từ các khoảng một đoạn chữ nêu: không có ⇒ None; một ⇒ nó; mọi khoảng đều là MỘT ngày ("từ 23/11 đến 25/11", "hôm nay với ngày mai")
    ⇒ từ ngày sớm nhất tới ngày muộn nhất; còn lại ("tuần này với tháng này") ⇒ khoảng RỘNG nhất (hẹp hơn sẽ bỏ sót sự kiện người dùng hỏi tới), bằng
    nhau thì khoảng nêu trước."""
    if not ds:
        return None
    if len(ds) >= 2 and all(x[1] == x[2] for x in ds):
        tu, den = min(x[1] for x in ds), max(x[1] for x in ds)
        if tu != den:
            return tu, den, f"từ {tu:%d/%m/%Y} đến {den:%d/%m/%Y}"
    _, tu, den, nhan, _ = max(ds, key=lambda x: ((x[2] - x[1]).days, -x[0]))
    return tu, den, nhan


def khoang_hoi(cau: str, hom: dt.date) -> tuple[dt.date, dt.date, str] | None:
    """Khoảng ngày câu gõ nêu ⇒ (từ, đến, nhãn); không nêu / không đọc được ⇒ None.
    21/11/2026 (tin của người dùng mô phỏng: "ok thứ 2 23/11 nhé. Thế tuần này với tháng này ở Huế có lễ hội gì không?" từng ra "ngày 23/11" — con số
    ngày ở câu đệm thắng khoảng ngày ở câu hỏi): đọc khoảng ngày trong CÂU có từ hỏi sự kiện trước; câu đó không nêu khoảng nào mới đọc cả tin (như
    cũ, theo thứ tự ưu tiên cũ — luật "khoảng rộng nhất" KHÔNG áp cho cả tin: tin dài lẫn nhiều mốc ngày không thuộc câu hỏi, ví dụ một tin thật có
    "rằm tháng 10" ở câu khác từng bị kéo sang cả tháng 10 năm sau). Trong CÂU HỎI nêu nhiều khoảng: xem `_mot_khoang`."""
    chu = unicodedata.normalize("NFC", cau).casefold()
    cau_con = [" ".join(x.split()) for x in re.split(r"(?<=[.?!…])\s+|\n+", chu) if x.strip()]
    for x in cau_con:
        if _HOI.search(x) and (k := _mot_khoang(_cac_khoang(x, hom))) is not None:
            return k
    ca_tin = _cac_khoang(" ".join(chu.split()), hom)
    return ca_tin[0][1:4] if ca_tin else None


def _ngay(lich: str, ngay: int, thang: int, nam: int) -> dt.date | None:
    """Ngày dương của (ngày, tháng) theo lịch của dòng trong năm `nam`; ngày 30 / 31 không có trong tháng đó ⇒ lùi tới ngày cuối tháng."""
    for lui in range(3):
        if lich == "am":
            d = nl.ngay_duong(ngay - lui, thang, nam, "am")
            if isinstance(d, dt.date):
                return d
        else:
            try:
                return dt.date(nam, thang, ngay - lui)
            except ValueError:
                continue
    return None


def cac_lan(dong: dict, quanh: dt.date) -> list[tuple[dt.date, dt.date]]:
    """Các lần diễn ra (dương lịch) của một dòng CÓ NGÀY HẰNG NĂM quanh ngày `quanh` (năm trước, năm đó, năm sau — theo lịch của dòng)."""
    nam0 = nl.solar_to_lunar(quanh).year if dong["lich"] == "am" else quanh.year
    lan = []
    for nam in (nam0 - 1, nam0, nam0 + 1):
        tu = _ngay(dong["lich"], dong["tu"][0], dong["tu"][1], nam)
        vat_nam = (dong["den"][1], dong["den"][0]) < (dong["tu"][1], dong["tu"][0])  # "23 tháng Chạp đến mồng 7 tháng Giêng"
        den = _ngay(dong["lich"], dong["den"][0], dong["den"][1], nam + 1 if vat_nam else nam)
        if tu and den:
            lan.append((tu, den))
    return lan


def _d(d: dt.date) -> str:
    return f"{nl.THU[d.weekday()]} {d:%d/%m/%Y}"


def _khoang(tu: dt.date, den: dt.date) -> str:
    return _d(tu) if tu == den else f"từ {_d(tu)} đến {_d(den)}"


def tra(bang: tuple[dict, ...], tu: dt.date, den: dt.date) -> dict:
    """Bảng + khoảng ⇒ {co_dinh: [(dòng, từ, đến)], uoc: [...], tuan: [dòng], sap_toi: (dòng, từ, đến) | None}. `sap_toi` chỉ tính khi không có
    lễ hội ngày cố định nào trong khoảng: lần gần nhất bắt đầu SAU khoảng hỏi."""
    kq = {"co_dinh": [], "uoc": [], "tuan": [], "sap_toi": None}
    cac_thu = {(tu + dt.timedelta(days=k)).weekday() for k in range(min((den - tu).days + 1, 7))}
    sau = []
    for dong in bang:
        if dong["lich"] == "tuan":
            if cac_thu & set(dong["thu"]):
                kq["tuan"].append(dong)
            continue
        lan = cac_lan(dong, tu)
        trung = [(a, b) for a, b in lan if a <= den and b >= tu]
        if trung:
            kq["uoc" if dong.get("uoc") else "co_dinh"].append((dong, *trung[0]))
        elif not dong.get("uoc"):
            sau += [(a, b, dong) for a, b in lan if a > den]
    kq["co_dinh"].sort(key=lambda x: x[1])
    kq["uoc"].sort(key=lambda x: x[1])
    if not kq["co_dinh"] and sau:
        a, b, dong = min(sau, key=lambda x: x[0])
        kq["sap_toi"] = (dong, a, b)
    return kq


def _dong_le_hoi(dong: dict, a: dt.date, b: dt.date) -> str:
    ghi_chu = f" Bài cũng ghi: “{dong['ghi_chu']}”." if dong.get("ghi_chu") else ""
    return f"- {dong['ten']}: {_khoang(a, b)}. Bài «{dong['ten']}» của kho ghi: “{dong['chu']}”.{ghi_chu}"


def dong_nguon(cau: str, bang: tuple[dict, ...], now: dt.datetime | None = None) -> list[str] | None:
    """Các dòng của nguồn cho câu gõ này, hoặc None khi câu không qua cổng (không hỏi sự kiện, không nêu khoảng ngày đọc được, khoảng quá dài)."""
    if not hoi_su_kien(cau):
        return None
    hom = nl.hom_nay(now)
    khoang = khoang_hoi(cau, hom)
    if khoang is None or (khoang[1] - khoang[0]).days + 1 > KHOANG_TOI_DA or khoang[1] < hom:
        return None
    tu, den, nhan = khoang
    kq = tra(bang, tu, den)
    dong = [f"Khoảng được hỏi ({nhan}): {_khoang(tu, den)}."]
    if kq["co_dinh"]:
        dong.append("Lễ hội có ngày cố định hằng năm rơi vào khoảng này:")
        dong += [_dong_le_hoi(d, a, b) for d, a, b in kq["co_dinh"]]
    else:
        dong.append("Trong khoảng này kho KHÔNG ghi lễ hội nào có ngày cố định hằng năm.")
        if kq["sap_toi"]:
            d, a, b = kq["sap_toi"]
            dong.append("Lễ hội có ngày cố định gần nhất sau khoảng này:")
            dong.append(_dong_le_hoi(d, a, b))
    if kq["uoc"]:
        dong.append("Lễ hội mà kho chỉ ghi một KHOẢNG thời gian — lễ chỉ diễn ra một hoặc vài ngày TRONG khoảng đó, ngày cụ thể do ban tổ chức công bố từng năm — và "
                    "khoảng đó chạm khoảng được hỏi (không khẳng định là có diễn ra đúng những ngày được hỏi):")
        dong += [f"- {d['ten']}: bài «{d['ten']}» của kho ghi: “{d['chu']}”." + (f" Bài cũng ghi: “{d['ghi_chu']}”." if d.get("ghi_chu") else "")
                 for d, _, _ in kq["uoc"]]
    if kq["tuan"]:
        dong.append("Hoạt động lặp lại hằng tuần có trong khoảng này:")
        dong += [f"- {d['ten']}: bài «{d['ten']}» của kho ghi: “{d['chu']}”." for d in kq["tuan"]]
    dong.append(CAU_CUOI)
    return dong
