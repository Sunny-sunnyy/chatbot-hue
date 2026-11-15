"""Dò số trong câu người dùng bằng luật code (Phase 9 B5, plan `docs/superpowers/plans/2026-11-03-phase-9-b5-plan.md` bản 7 D12 (b), D15).

Một chỗ dò số dùng chung: B5 dò **số ngày**; B5c (plan `2026-11-05-phase-9-b5c-plan.md` D6) thêm số người vào đây. Không gọi model.
"""
import re
import unicodedata

CHU_SO = {"một": 1, "hai": 2, "ba": 3, "bốn": 4, "năm": 5, "sáu": 6, "bảy": 7, "tám": 8, "chín": 9, "mười": 10}
_SO = r"(\d+|" + "|".join(CHU_SO) + r")"
# "3 ngày", "ba ngày", "3 ngày 2 đêm" (lấy số ngày) · "3N2Đ" / "3n2đ" (sau khi hạ chữ thường)
_NGAY = re.compile(r"(?<![\w])" + _SO + r"\s+ngày(?![\w])")
_NGAY_DEM_TAT = re.compile(r"(?<![\w])(\d+)\s*n\s*(\d+)\s*đ(?![\w])")


def _so(text: str) -> int:
    return int(text) if text.isdigit() else CHU_SO[text]


def gia_tri_so_ngay(n: int) -> str:
    """Số ngày ⇒ giá trị trường `so_ngay` của B4 ({1, 2, 3, 4+})."""
    return "4+" if n >= 4 else str(n)


def do_so_ngay(text: str) -> str | None:
    """Số ngày người dùng nêu trong `text` ⇒ "1" / "2" / "3" / "4+"; không thấy, hoặc thấy **nhiều giá trị khác nhau** ⇒ None (không đoán).
    "ngày thứ 2", "mỗi ngày" không phải số ngày (số phải đứng ngay trước chữ "ngày")."""
    t = unicodedata.normalize("NFC", text).casefold()
    so = {_so(m.group(1)) for m in _NGAY.finditer(t)} | {int(m.group(1)) for m in _NGAY_DEM_TAT.finditer(t)}
    so.discard(0)
    gia_tri = {gia_tri_so_ngay(n) for n in so}
    return gia_tri.pop() if len(gia_tri) == 1 else None


# Phase 9 B5b D9 (plan `2026-11-05-phase-9-b5b-plan.md` bản 2): ngày đi của lịch ⇒ số ngày tính từ hôm nay (0–6), cho dòng dự báo trong ghi chú.
_THU_SO = {"hai": 0, "ba": 1, "tư": 2, "năm": 3, "sáu": 4, "bảy": 5}
_MAI = re.compile(r"(?<![\w])(?:ngày\s+)?mai(?![\w])")
_NGAY_KIA = re.compile(r"(?<![\w])ngày\s+(?:kia|mốt)(?![\w])")
_THU = re.compile(r"(?<![\w])(?<!ngày )(?:thứ\s+(hai|ba|tư|năm|sáu|bảy)|(chủ\s+nhật))(?![\w])")  # "ngày thứ ba" = ngày 3 của chuyến, không phải thứ Ba
_CUOI_TUAN = re.compile(r"(?<![\w])cuối\s+tuần(?:\s+này)?(?![\w])")
_DD_MM = re.compile(r"(?<![\d/])(\d{1,2})/(\d{1,2})(?![\d/])")


def do_ngay_di(text: str, hom_nay) -> int | None:
    """Số ngày từ `hom_nay` (date, giờ Việt Nam) tới ngày đi người dùng nêu: "mai" 1 · "ngày kia / mốt" 2 · "thứ X" / "chủ nhật" lần tới gần nhất
    (hôm nay đúng thứ đó ⇒ 0) · "cuối tuần (này)" thứ Bảy gần nhất · "dd/mm" ⇒ đúng ngày. Ngoài 0–6, không thấy, hoặc thấy **nhiều giá trị khác
    nhau** ⇒ None (không đoán; lịch như B5)."""
    import datetime as _dt
    t = unicodedata.normalize("NFC", text).casefold()
    found = set()
    if _MAI.search(t):
        found.add(1)
    if _NGAY_KIA.search(t):
        found.add(2)
    for m in _THU.finditer(t):
        thu = 6 if m.group(2) else _THU_SO[m.group(1)]
        found.add((thu - hom_nay.weekday()) % 7)
    if _CUOI_TUAN.search(t):
        found.add((5 - hom_nay.weekday()) % 7)
    for d, mo in _DD_MM.findall(t):
        try:
            ngay = _dt.date(hom_nay.year, int(mo), int(d))
        except ValueError:
            continue
        found.add((ngay - hom_nay).days)
    if len(found) != 1:
        return None
    n = found.pop()
    return n if 0 <= n <= 6 else None


# Sửa lịch bằng lời — đổi ngày đi (plan 2026-11-15-sua-lich-ngay-di): NGÀY do code đọc từ chính chữ người dùng (model chỉ nhận ra ý "đổi ngày đi",
# không viết ngày). Khác `do_ngay_di`: không giới hạn 0–6 ngày, đọc thêm "dd/mm/yyyy", "ngày d tháng m", "tuần sau"; trả ngày thật.
# Review E M-1 (15/11): chữ GIỐNG ngày không phải ngày ⇒ không đọc (thà hỏi lại còn hơn đổi sai): phân số / "24/7" / "1/2 ngày" · "2 tháng 3 ngày" ·
# "điểm thứ hai" (thứ tự, không phải thứ Hai) · "Mai" là tên người / tên đường.
_DON_VI = re.compile(r"\s*(?:ngày|giờ|buổi|tiếng|nhóm|phần|chặng|số|người|quãng|đoạn|tuần|tháng|giá)(?![\w])")
_SAU_THANG = re.compile(r"\s+(?:ngày|tuần)(?![\w])")
_DMY = re.compile(r"(?<![\d/])(\d{1,2})/(\d{1,2})(?:/(\d{4}))?(?![\d/])")
_D_THANG_M = re.compile(r"(?<![\w/])(\d{1,2})\s+tháng\s+(\d{1,2})(?:\s+năm\s+(\d{4}))?(?![\w/])")
_THU_CN = re.compile(r"(?<![\w])(?:(\w+)\s+)?(?:thứ\s+(hai|ba|tư|năm|sáu|bảy|[2-7])|(chủ\s+nhật|cn))(?![\w])")  # như `_THU` + "thứ 3", "CN"
_TRUOC_THU_TU = {"ngày", "tuần", "tháng", "điểm", "nơi", "chỗ", "lần", "mục", "người", "cái", "món", "quán", "bước", "ý", "phần", "chặng", "hạng", "câu", "lượt", "bữa"}
_MAI_CHU = re.compile(r"(?<![\w])(?:(\w+)\s+)?(mai)(?![\w])(?:\s+(\w))?", re.IGNORECASE)  # chạy trên chữ GỐC (còn hoa / thường)
_TRUOC_TEN = {"chị", "anh", "cô", "bà", "ông", "em", "bạn", "bé", "chú", "bác", "dì", "đường", "phố", "hoa", "chợ", "cây", "cành", "tên"}


def _co_mai(goc: str) -> bool:
    """"mai" = ngày mai? Không tính khi là tên: viết hoa giữa câu ("chị Mai"), đứng sau từ xưng hô / đường / phố / hoa…, hoặc theo sau là một
    chữ viết hoa ("Mai Thúc Loan")."""
    for m in _MAI_CHU.finditer(goc):
        truoc, chu, sau = m.group(1), m.group(2), m.group(3)
        dau_cau = not goc[:m.start(2)].strip() or goc[:m.start(2)].rstrip()[-1] in ".!?…;:"
        if (truoc or "").casefold() in _TRUOC_TEN or (chu[0].isupper() and not dau_cau) or (sau is not None and sau.isupper()):
            continue
        return True
    return False
_TUAN_SAU = re.compile(r"(?<![\w])tuần\s+(?:sau|tới)(?![\w])")
_CUOI_TUAN_SAU = re.compile(r"(?<![\w])cuối\s+tuần(?:\s+(này|sau|tới))?(?![\w])")
_HOM_NAY = re.compile(r"(?<![\w])hôm\s+nay(?![\w])")
_AM_LICH = re.compile(r"(?<![\w])(âm(?:\s+lịch)?|tết|rằm|mùng|mồng)(?![\w])")
NGAY_CHUA_RO, NGAY_KHONG_CO = "ngay_chua_ro", "ngay_khong_co"


def ngay_tu_cau(text: str, hom_nay):
    """Ngày đi người dùng nêu trong câu ⇒ `datetime.date`; không đọc được MỘT ngày ⇒ mã lý do (chuỗi): `ngay_chua_ro` (không thấy ngày, thấy
    ≥ 2 ngày khác nhau, ngày âm / dịp Tết, chỉ nói tương đối "dời 2 hôm") · `ngay_khong_co` (30/2). Không kiểm quá khứ / quá xa — việc của nơi gọi.
    Đọc: dd/mm[/yyyy] · "d tháng m [năm yyyy]" (không năm ⇒ lần tới gần nhất, kể cả hôm nay) · hôm nay · mai · ngày kia / mốt · thứ X / chủ nhật
    (lần tới gần nhất; kèm "tuần sau / tuần tới" ⇒ đúng thứ đó của tuần sau) · cuối tuần [này / sau] (thứ Bảy)."""
    import datetime as _dt
    goc = unicodedata.normalize("NFC", text)
    if goc == goc.upper():  # cả câu viết HOA ⇒ không dùng được dấu hiệu "viết hoa = tên riêng"
        goc = goc.lower()
    t = goc.casefold()
    if _AM_LICH.search(t):
        return NGAY_CHUA_RO
    found, sai = set(), False
    for m in list(_DMY.finditer(t)) + list(_D_THANG_M.finditer(t)):
        d, mo, y = m.group(1), m.group(2), m.group(3)
        truoc, sau = t[:m.start()].rstrip(), t[m.end():]
        if "/" in m.group(0):
            if (d, mo, y) == ("24", "7", None):  # "mở 24/7"
                continue
            # phân số: "tỉ lệ 3/4", "1/2 ngày", "vé 1/2 giá" (tử < mẫu + đơn vị đi sau); "20/12 ngày đẹp" vẫn là ngày
            mo_ho = truoc.endswith(("tỉ lệ", "tỷ lệ", "khoảng")) or (not y and int(d) < int(mo) and bool(_DON_VI.match(sau)))
        else:
            mo_ho = not y and bool(_SAU_THANG.match(sau))  # "2 tháng 3 ngày nghỉ" = hai tháng ba ngày
        if mo_ho:  # một cụm số có thể là ngày mà cũng có thể không ⇒ cả câu "chưa rõ" (không lấy ngày khác trong câu rồi đổi)
            return NGAY_CHUA_RO
        try:
            ngay = _dt.date(int(y) if y else hom_nay.year, int(mo), int(d))
            if not y and ngay < hom_nay:
                ngay = _dt.date(hom_nay.year + 1, int(mo), int(d))
        except ValueError:
            sai = True
            continue
        found.add(ngay)
    if _HOM_NAY.search(t):
        found.add(hom_nay)
    if _co_mai(goc):
        found.add(hom_nay + _dt.timedelta(days=1))
    if _NGAY_KIA.search(t):
        found.add(hom_nay + _dt.timedelta(days=2))
    tuan_sau = bool(_TUAN_SAU.search(t))
    dau_tuan_sau = hom_nay + _dt.timedelta(days=7 - hom_nay.weekday())  # thứ Hai tuần sau
    for m in _THU_CN.finditer(t):
        if m.group(2) and m.group(1) in _TRUOC_THU_TU:  # "điểm thứ hai", "ngày thứ ba" = thứ tự, không phải thứ trong tuần
            continue
        thu = 6 if m.group(3) else (int(m.group(2)) - 2 if m.group(2).isdigit() else _THU_SO[m.group(2)])
        found.add(dau_tuan_sau + _dt.timedelta(days=thu) if tuan_sau else hom_nay + _dt.timedelta(days=(thu - hom_nay.weekday()) % 7))
    for m in _CUOI_TUAN_SAU.finditer(t):
        found.add(dau_tuan_sau + _dt.timedelta(days=5) if m.group(1) in ("sau", "tới") else hom_nay + _dt.timedelta(days=(5 - hom_nay.weekday()) % 7))
    if len(found) == 1:
        return found.pop()
    return NGAY_KHONG_CO if sai and not found else NGAY_CHUA_RO
