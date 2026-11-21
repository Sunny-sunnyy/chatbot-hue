"""Khoảng cách + phút đi xe giữa hai điểm của bảng lịch (plan `docs/superpowers/plans/2026-11-16-khoang-cach-plan.md`).

Vì sao là code: số km / phút là phép tra bảng tất định — model chỉ chọn MÃ hai điểm trong danh sách cố định (tham số công cụ là enum), code tra
bảng dựng sẵn một lần từ OSRM (`data/phase_9/lich_trinh/khoang_cach_v1.json`; lúc chạy KHÔNG gọi mạng) rồi viết câu có số. Code không đọc tên nơi
từ chữ người dùng; chữ người dùng chỉ dùng để quyết có đưa công cụ hay không (`co_tu_khoa`). Công cụ này không đổi lịch (lịch dùng phút theo cụm).
"""
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

KHAC = "khac"  # nơi không có trong danh sách ⇒ câu "chưa có số", không ước
TIEU_DE_NGUON = "Khoảng cách ước tính (bản đồ)"
MUC_NGUON = "Ước theo đường ô tô / xe máy"
NGUON_SOURCE = "osrm-khoang-cach"  # `source` của nguồn — không thuộc tiền tố bài kho
CAU_CHUA_CO = "Mình chưa có số khoảng cách cho nơi này."
CAU_GHI_CHU = "Số ước theo đường đi trên bản đồ, chưa tính kẹt xe hay dừng nghỉ."
# Phút hiện = 1,25 × phút OSRM + 5 (review 16/11 M1; đối chiếu 6 cặp có nguồn công khai — report `c_khoang_cach_implementation.md`): OSRM (hồ sơ ô tô)
# tính theo tốc độ giới hạn ⇒ chặng nội thành nhanh quá (Đại Nội → Tự Đức OSRM 12 phút, nguồn 20 phút), còn sàn 40 km/h làm chặng dài chậm quá
# (Huế → Lập An 105 phút, nguồn 75). Hệ số + 5 phút (ra / vào bãi, đèn đỏ) khớp cả hai đầu: 6 / 6 cặp trong khoảng nguồn ghi.
HE_SO_OSRM, PHUT_CONG = 1.25, 5

# Từ khoá khoảng cách (câu cuối hoặc câu hỏi liền trước). Bật thừa vô hại (model không gọi, hoặc công cụ nói "chưa có số"); bỏ sót ⇒ đi như cũ.
# Không bắt "mấy giờ" (giờ mở cửa), "bao lâu" đứng một mình (thời lượng tham quan / lưu trú), "cách làm / nấu / tính / đây…" (review 16/11 m1).
_TU_KM = re.compile(
    r"\bbao\s+xa\b|\bcó\s+xa\b|\bxa\s+(?:không|ko|k|hông|hok|hem)\b|\bxa\s+lắm\s+không\b"
    r"|\b(?:bao\s+nhiêu|mấy)\s+(?:km|ki\s*lô\s*mét|kilomet|kilômét|cây\s+số|cây)\b"
    r"|\bkhoảng\s+cách\b|\bcách\s+nhau\b|\bgần\s+nhau\b|\bcó\s+gần\b|\bgần\s+(?:không|ko|hông)\b"
    r"|\bcách\b(?!\s+(?:làm|nấu|tính|chế\s+biến|đây|pha|ăn|chọn|dùng|bảo\s+quản|thức|nhận|đặt|mua|gọi))[^.?!\n]{0,40}\b(?:bao\s+nhiêu|mấy)\b",
    re.IGNORECASE,
)
# Từ chỉ thời gian chỉ tính khi câu có từ chỉ di chuyển ("luộc mấy tiếng", "nấu mất bao lâu", "kéo dài mấy tiếng" ⇒ không bật — review 16/11 m1)
_TU_THOI_GIAN = re.compile(r"\b(?:bao\s+nhiêu|mấy)\s+(?:phút|tiếng)\b|\bmất\s+bao\s+lâu\b|\bbao\s+lâu\b", re.IGNORECASE)
_DI_CHUYEN = re.compile(r"\b(?:đi|từ|tới|đến|sang|ra|vào|xe|chạy)\b", re.IGNORECASE)
# Số kèm đơn vị trong chữ model: "12–14 km" ⇒ cả hai số; "15p", "1h" (viết tắt) cũng xét. km ↔ thời gian tách riêng (review m2: đảo đơn vị lọt qua).
_SO_DON_VI = re.compile(r"(\d+(?:[.,]\d+)?)(?:\s*(?:–|-|đến|tới)\s*(\d+(?:[.,]\d+)?))?\s*"
                        r"(km|ki\s*lô\s*mét|kilô?mét|kilomet|cây\s+số|cây|phút|p|tiếng|giờ|h)\b", re.IGNORECASE)
_MOI_SO = re.compile(r"\d+(?:[.,]\d+)?")


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text or "")


def co_tu_khoa(text: str) -> bool:
    t = _nfc(text)
    return bool(_TU_KM.search(t) or (_TU_THOI_GIAN.search(t) and _DI_CHUYEN.search(t)))


def co_tu_khoa_luot(query: str, history) -> bool:
    """Như `thoi_tiet.co_tu_khoa_luot`: câu cuối hoặc câu hỏi liền trước có từ khoá (câu hỏi tiếp "còn sang lăng X thì sao?")."""
    return co_tu_khoa(query) or bool(history and co_tu_khoa(history[-1][0]))


@dataclass(frozen=True)
class BangKhoangCach:
    ten: dict[str, str]  # id ⇒ tên hiện cho người dùng (theo thứ tự bảng lịch)
    ten_khac: dict[str, tuple[str, ...]]
    cap: dict[str, dict]  # "a|b" ⇒ {"km", "phut"}

    @property
    def ids(self) -> tuple[str, ...]:
        return tuple(self.ten)


def nap_bang(path_khoang_cach: str | Path, path_diem: str | Path) -> BangKhoangCach:
    """Bảng km / phút (dựng sẵn) + tên điểm từ bảng lịch. Cặp có mã lạ ⇒ lỗi lúc khởi động (bảng lệch bảng điểm)."""
    diem = json.loads(Path(path_diem).read_text(encoding="utf-8"))["diem"]
    ten = {d["id"]: d["ten"] for d in diem}
    ten_khac = {d["id"]: tuple(d.get("ten_khac") or ()) for d in diem}
    cap = json.loads(Path(path_khoang_cach).read_text(encoding="utf-8"))["cap"]
    la = {i for k in cap for i in k.split("|")} - set(ten)
    if la:
        raise ValueError(f"distance table has ids not in the itinerary table: {sorted(la)}")
    return BangKhoangCach(ten=ten, ten_khac=ten_khac, cap=cap)


# ---------- Khoảng cách tính sẵn (plan `2026-11-17-khoang-cach-tinh-san-plan.md`) ----------
# Tên ngắn người dùng hay gõ mà bảng không có. Để ở đây, KHÔNG thêm vào `ten_khac` của bảng điểm: `ten_khac` còn vào mô tả công cụ (chuỗi gửi
# model) và vào bước kiểm câu mô tả của lịch (`lich_trinh_v2`: câu nhắc tên điểm khác ⇒ bỏ) — hai chỗ đó không được đổi theo việc này.
# Chỉ thêm tên không trùng nghĩa khác ("Thuận An", "Bạch Mã", "Tự Đức" đứng một mình có thể là khách sạn / núi / vua ⇒ không thêm).
TEN_NGAN = {"cho_dong_ba": ("Đông Ba",), "chua_thien_mu": ("Thiên Mụ",), "cau_truong_tien": ("Cầu Tràng Tiền", "Trường Tiền", "Tràng Tiền")}
# "A hay B gần hơn?", "nơi nào xa nhất?" = so hai lựa chọn từ một nơi khác, không phải khoảng cách GIỮA hai nơi ⇒ không tính sẵn
_SO_SANH = re.compile(r"\b(?:gần|xa)\s+(?:hơn|nhất)\b|\bnào\s+(?:gần|xa)\b|\bhơn\b", re.IGNORECASE)
# DẠNG CÂU được tính sẵn (review E 16/11 M-1: có đủ hai tên bảng chưa đủ — câu có thể hỏi khoảng cách tới nơi thứ ba "cách trung tâm", "từ ga…",
# hoặc tên điểm nằm trong tên riêng khác "khách sạn Đông Ba", "Trường Tiền Plaza"): chữ TRƯỚC tên thứ nhất, GIỮA hai tên và SAU tên thứ hai đều phải
# thuộc danh sách đóng dưới đây. Câu viết kiểu khác ⇒ None ⇒ đường cũ (model gọi công cụ) — chậm hơn nhưng không nối nhầm số.
_TRUOC = {"", "từ", "đi từ"}
_GIUA_HUONG = {"đến", "tới", "sang", "ra", "về", "đi", "qua", "vào", "lên", "xuống", "đi đến", "đi tới", "đi sang", "đi ra", "đi về", "đi qua",
               "-", "–", "cách"}
_GIUA_CAP = {"và", "với"}
_GIUA_HOI = {"có gần", "có xa"}
_SAU_HOI = re.compile(r"(?:lắm\s+)?(?:không|ko|k|hông|hok|hem)?\W*")  # "A có gần B không?"
_SAU_CAP = re.compile(r"(?:thì\s+|là\s+)?(?:cách\s+nhau|có\s+gần\s+nhau|gần\s+nhau|có\s+xa\s+nhau|xa\s+nhau)\b")  # "A với B cách nhau bao xa?"
_SAU_DEM = re.compile(r"(?:thì\s+|là\s+)?(?:đi\s+bộ\s+|đi\s+xe\s+máy\s+|đi\s+xe\s+|đi\s+ô\s+tô\s+|chạy\s+xe\s+)?(?:mất\s+|hết\s+|khoảng\s+|tầm\s+)*")


def _chuan_ten(text: str) -> str:
    return " ".join(_nfc(text).casefold().split())


def _khoa_ten(bang: BangKhoangCach) -> list[tuple[str, str]]:
    """(cụm chữ đã chuẩn hoá, mã) của mọi tên đọc được từ chữ người dùng, cụm dài trước. Tên kết thúc bằng " Huế" có thêm dạng bỏ " Huế" khi
    phần còn lại ≥ 2 chữ ("Đại Nội Huế" ⇒ "đại nội", "Phố Tây Huế" ⇒ "phố tây") — cùng luật với `lich_trinh.chuan_ten`."""
    khoa = {}
    for i in bang.ids:
        for ten in (bang.ten[i], *bang.ten_khac[i], *TEN_NGAN.get(i, ())):
            k = _chuan_ten(ten)
            dang = [k] + ([k[: -len(" huế")]] if k.endswith(" huế") and len(k.split()) >= 3 else [])
            for d in dang:
                khoa[d] = None if khoa.get(d, i) != i else i  # một cụm trỏ hai mã ⇒ mập mờ, bỏ cụm đó
    return sorted(((k, i) for k, i in khoa.items() if i is not None), key=lambda x: -len(x[0]))


def _sau_dat(giua: str, sau: str) -> bool:
    if giua in _GIUA_HOI:
        return bool(_SAU_HOI.fullmatch(sau))
    if giua in _GIUA_CAP:
        return bool(_SAU_CAP.match(sau))
    if giua in _GIUA_HUONG:  # "Từ A đến B bao xa / mất bao lâu…": ngay sau tên thứ hai phải là từ hỏi khoảng cách, không phải "cách <nơi khác>…"
        con = sau[_SAU_DEM.match(sau).end():]
        return not con.startswith("cách") and bool(_TU_KM.match(con) or _TU_THOI_GIAN.match(con))
    return False


def tim_hai_diem(cau: str, bang: BangKhoangCach) -> tuple[str, str] | None:
    """Câu có ĐÚNG HAI tên điểm của bảng (hai mã khác nhau, mỗi tên một lần) và đúng dạng "[từ] A <từ nối> B <hỏi khoảng cách>" ⇒ (mã A, mã B)
    theo thứ tự trong câu; còn lại ⇒ None. So tên nguyên cụm theo ranh giới chữ, cụm dài trước, không chồng nhau. "Đến B từ A" ⇒ None (bảng hai
    chiều có thể lệch, không đoán chiều — review E m-1)."""
    chu = _chuan_ten(cau)
    da_dung = [False] * len(chu)
    thay: list[tuple[int, int, str]] = []  # (đầu, cuối, mã)
    for khoa, ma in _khoa_ten(bang):
        for m in re.finditer(rf"(?<!\w){re.escape(khoa)}(?!\w)", chu):
            if not any(da_dung[m.start():m.end()]):
                da_dung[m.start():m.end()] = [True] * (m.end() - m.start())
                thay.append((m.start(), m.end(), ma))
    thay.sort()
    if len(thay) != 2 or thay[0][2] == thay[1][2]:
        return None
    (dau_a, cuoi_a, a), (dau_b, cuoi_b, b) = thay
    truoc, giua, sau = chu[:dau_a].strip(" ,"), chu[cuoi_a:dau_b].strip(" ,"), chu[cuoi_b:].strip(" ,")
    return (a, b) if truoc in _TRUOC and _sau_dat(giua, sau) else None


def cap_tinh_san(cau: str, bang: BangKhoangCach) -> tuple[str, str] | None:
    """Cặp điểm để code tra bảng TRƯỚC lần gọi model đầu: câu đang gõ (không lịch sử) có từ khoá khoảng cách, không phải câu so sánh, đúng dạng
    hai điểm của bảng (`tim_hai_diem`) và bảng có số cho cặp đó. None ⇒ đi đường cũ (model gọi công cụ)."""
    if not co_tu_khoa(cau) or _SO_SANH.search(_nfc(cau)):
        return None
    cap = tim_hai_diem(cau, bang)
    return cap if cap and f"{cap[0]}|{cap[1]}" in bang.cap else None


def mo_ta_cong_cu(bang: BangKhoangCach) -> str:
    """Mô tả công cụ: luật ngắn + danh sách `mã: tên (tên khác)` để model ánh xạ tên người dùng gõ ⇒ mã."""
    dong = [f"{i}: {bang.ten[i]}" + (f" ({', '.join(bang.ten_khac[i])})" if bang.ten_khac[i] else "") for i in bang.ids]
    return ("Khoảng cách và thời gian đi xe ước tính giữa HAI điểm ở Huế trong danh sách dưới. Chỉ gọi khi người dùng hỏi hai nơi cách nhau bao xa / "
            f"đi mất bao lâu. diem_a, diem_b = mã của hai nơi; nơi không có trong danh sách (khách sạn, sân bay, \"trung tâm\", nơi ngoài Huế…) ⇒ \"{KHAC}\", "
            "không chọn điểm gần giống. Kết quả là một nguồn có mã [n]: chỉ dùng đúng số trong đó, ghi mã [n]; không tự ước số khác.\n"
            "Danh sách:\n" + "\n".join(dong))


def _km(km: float) -> str:
    if km < 0.5:
        return "dưới 0,5 km"
    return f"khoảng {km:.1f} km".replace(".", ",") if km < 10 else f"khoảng {round(km)} km"


def _phut(phut: int) -> str:
    if phut < 60:
        return f"khoảng {phut} phút đi xe"
    gio, du = divmod(phut, 60)
    return f"khoảng {gio} giờ {du} phút đi xe" if du else f"khoảng {gio} giờ đi xe"


def ket_qua(bang: BangKhoangCach, diem_a: str, diem_b: str) -> tuple[str, ...]:
    """Các dòng của nguồn khoảng cách. Mã `khac` / cặp không có số / hai mã trùng ⇒ câu cố định, không số."""
    if KHAC in (diem_a, diem_b) or diem_a == diem_b:
        return (CAU_CHUA_CO,)
    v = bang.cap.get(f"{diem_a}|{diem_b}")
    if v is None:
        return (f"Mình chưa có số khoảng cách từ {bang.ten[diem_a]} đến {bang.ten[diem_b]}.",)
    phut = int(v["phut"] * HE_SO_OSRM + 0.5) + PHUT_CONG  # làm tròn nửa lên (không kiểu ngân hàng — review m4)
    return (f"Từ {bang.ten[diem_a]} đến {bang.ten[diem_b]}: {_km(v['km'])} đường đi, {_phut(phut)} (ước theo đường).", CAU_GHI_CHU)


def _chuan(s: str) -> str:
    s = s.replace(".", ",")
    nguyen, _, le = s.partition(",")
    return (nguyen.lstrip("0") or "0") + ("," + le if le else "")  # "07" ⇒ "7"


def _loai(don_vi: str) -> str:
    return "km" if don_vi.lower().startswith(("k", "c")) else "tg"


# 21/11/2026 (lượt người dùng mô phỏng: câu "bạn vào từ 13h thì không vướng giờ này" làm cả câu trả lời bị rút): GIỜ ĐỒNG HỒ không phải thời lượng.
# Hẹp có chủ ý: chỉ "<lúc | từ | vào | trước | sau> N h / giờ" với N từ 5 tới 23; "mất tới 2h", "khoảng 3 giờ" vẫn là thời lượng và vẫn bị kiểm.
_TRUOC_GIO_DONG_HO = re.compile(r"\b(?:lúc|từ|vào|trước|sau)\s+$", re.IGNORECASE)


def _la_gio_dong_ho(t: str, m: re.Match) -> bool:
    return (m.group(2) is None and m.group(3).lower() in ("h", "giờ") and m.group(1).isdigit() and 5 <= int(m.group(1)) <= 23
            and bool(_TRUOC_GIO_DONG_HO.search(t[max(0, m.start() - 8):m.start()])))


def vi_tri_so_khoang_cach(text: str, bo_gio_dong_ho: bool = True) -> list[tuple[str, str, int, int]]:
    """(loại, số, đầu, cuối) của mọi số đi kèm đơn vị khoảng cách (`km`) / thời gian (`tg`) — vị trí trên chữ đã chuẩn NFC. Mặc định dùng cho CHỮ
    MODEL: giờ đồng hồ không tính. `bo_gio_dong_ho=False`: mọi số (dùng khi dựng tập số được phép từ dòng code in — tập đó không được hẹp đi)."""
    t = _nfc(text)
    out = []
    for m in _SO_DON_VI.finditer(t):
        if not (bo_gio_dong_ho and _la_gio_dong_ho(t, m)):
            out += [(_loai(m.group(3)), _chuan(g), m.start(), m.end()) for g in m.groups()[:2] if g]
    return out


def so_khoang_cach(text: str) -> list[tuple[str, str]]:
    """(loại, số) của MỌI số đi kèm đơn vị khoảng cách / thời gian trong `text`, kể cả giờ đồng hồ (như trước 21/11) — `tap_so_theo_loai` dựng tập số
    được phép từ đây."""
    return [(loai, s) for loai, s, _, _ in vi_tri_so_khoang_cach(text, bo_gio_dong_ho=False)]


def tap_so(text: str) -> set[str]:
    """Mọi số trong `text` (chuẩn hoá), kèm số làm tròn tới phần nguyên của số thập phân (lượt đo 16/11: nguồn "4,0 km" / "8,3 km", model viết
    "4 km" / "8 km" ⇒ bị rút lại oan 2 / 14). Số tự ước khác hẳn (5 so với 4,0) vẫn bị bắt."""
    out = set()
    for s in _MOI_SO.findall(_nfc(text)):
        s = _chuan(s)
        out.add(s)
        if "," in s:
            x = float(s.replace(",", "."))
            out |= {str(int(x)), str(round(x))}
    return out


def tap_so_theo_loai(text: str) -> dict[str, set[str]]:
    """Số của nguồn khoảng cách do code dựng, tách theo loại (km / thời gian) — kèm số làm tròn như `tap_so`."""
    out = {"km": set(), "tg": set()}
    for loai, s in so_khoang_cach(text):
        out[loai] |= tap_so(s)
    return out


def kiem_so(text: str, cho_phep: dict[str, set[str]]) -> list[str]:
    """Số km / thời gian trong chữ model nằm ngoài tập cho phép CÙNG LOẠI (rỗng = đạt). Giới hạn đã biết: không tách theo cặp (lượt gọi nhiều cặp
    ⇒ số của cặp này dùng cho cặp kia vẫn lọt), không xét số viết bằng chữ ("hai cây số")."""
    return [s for loai, s, _, _ in vi_tri_so_khoang_cach(text) if s not in cho_phep[loai]]
