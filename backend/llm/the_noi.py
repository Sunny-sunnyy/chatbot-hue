"""Công tắc `the_noi` — THẺ NƠI: dòng địa chỉ / giờ mở cửa / giá vé lẻ của một nơi, do code chép nguyên từ bài riêng của nơi đó.

Vì sao (đếm 0 đồng 22/11/2026 trên sổ vết): ở tin nhiều ý, TÊN một nơi tới ngữ cảnh từ nguồn chỉ liệt kê (đoạn "Leo bậc…", công cụ liệt kê bài, công cụ
gần một điểm) còn THUỘC TÍNH của nơi đó nằm ở bài riêng không ai tra ⇒ model ghi "Tư liệu chưa có thông tin về giờ mở cửa…" cho thứ kho có (tin gia đình
8 / 9 câu trả lời; tin nhiều ý khác 11 / 46 lượt). Khâu tìm không hỏng — model nói "chưa có" cho thứ nó CHƯA TRA, và hết lượt tìm trước khi biết tên.
Chữa: sau mỗi lần tìm, nơi có bài riêng được nhắc ĐÚNG TÊN trong ngữ cảnh mà bài riêng chưa có đoạn nào ở đó ⇒ một nguồn mang mã nguồn của chính bài
ấy, chỉ gồm dòng bắt đầu bằng nhãn địa chỉ / giờ; hàng của nơi đó trong bảng vé lẻ đi vào một nguồn của bài vé. Không gọi model, không tìm thêm.

Module thuần (không đọc cấu hình, không SDK); `assistant.py` đăng kết quả vào sổ nguồn của lượt.
"""
from dataclasses import dataclass
import re
import unicodedata

from llm import liet_ke as lk

# Nhóm bài "một bài = một nơi" (thư mục của bài trong kho). Bài món, lễ hội, dịch vụ, vé không phải một nơi có địa chỉ / giờ mở cửa.
NHOM_NOI = ("heritages/heritage/", "travel/places/", "foods/restaurants/", "foods/cafes/")
BAI_VE_LE = "travel/tickets/Vé tham quan Quần thể Di tích Cố đô Huế.md"  # bài có bảng vé lẻ từng điểm
TRAN_THE = 25  # số nơi nhiều nhất được gắn thẻ trong một lượt (đếm 54 lượt nhiều ý đã ghi: trung vị 10, lớn nhất 21)
MUC_THE = "Địa chỉ và giờ mở cửa (dòng chép nguyên từ bài)"
MUC_VE = "Bảng giá vé lẻ từng điểm (hàng chép nguyên từ bài)"
# Cổng của lượt: tin có chữ hỏi hẹp về giờ / địa chỉ (17 / 17 lượt có dòng "chưa có" sai đều có; cổng tha 17 / 54 lượt nhiều ý).
HOI_HEP = re.compile(r"giờ|mở cửa|địa chỉ|ở đâu|đường nào|chỗ nào", re.I)

# Chỉ dòng BẮT ĐẦU bằng nhãn — chữ "mở cửa" giữa dòng không tính (bài Lăng Dục Đức có dòng "Mở cửa phục vụ công chúng… 01/01/2025").
_NHAN = (re.compile(r"^(địa chỉ[^:]{0,25}|khu vực)\s*:", re.I), re.compile(r"^giờ (mở cửa|hoạt động)[^:]{0,25}:", re.I))
# Hàng của bảng vé lẻ: "| 10 | Cung An Định | … | 50.000 | Miễn phí |" — ô tên có thể kèm tên chữ Hán trong ngoặc ("Lăng vua Dục Đức *(An Lăng)*").
_HANG_VE = re.compile(r"^\|\s*\d+\s*\|\s*([^|(*]+?)\s*(?:\*?\([^|]*\)\*?)?\s*\|[^|]*\|\s*(?:[\d.]+|Miễn phí)\s*\|")


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text or "")


@dataclass(frozen=True)
class Noi:
    ten: str                    # tên bài = tên nơi
    rel: str                    # đường dẫn bài trong kho ⇒ `source` của thẻ (người dùng bấm nguồn mở đúng bài)
    mau: re.Pattern             # khớp ĐÚNG hoa thường, cả tên, có biên chữ — không khúc tên, không tên gọi khác
    dong: tuple[str, ...]       # dòng địa chỉ / giờ chép từ bài (0–2 dòng)
    ve: str | None              # hàng của nơi này trong bảng vé lẻ (None = bảng không có)


@dataclass(frozen=True)
class Bang:
    noi: tuple[Noi, ...]        # chỉ nơi có ít nhất một dòng để chép — bài không ghi giờ / địa chỉ / vé thì không bao giờ ra thẻ
    ve_rel: str = ""
    ve_tieu_de: str = ""
    ve_dau: str = ""            # hàng tiêu đề của bảng vé lẻ (để hàng chép ra còn đọc được cột nào là giá nào)


def dung_bang(muc_luc: tuple[lk.Bai, ...]) -> Bang:
    """Bảng thẻ từ mục lục kho (`lk.nap_muc_luc`) — tính MỘT lần lúc nạp cấu hình."""
    bai_ve = next((b for b in muc_luc if b.rel == BAI_VE_LE), None)
    hang_ve, ve_dau = {}, ""
    for i, dong in enumerate(bai_ve.dong if bai_ve else ()):
        khop = _HANG_VE.match(dong)
        if khop:
            hang_ve[" ".join(_nfc(khop.group(1)).replace("Lăng vua", "Lăng").split())] = dong
        elif not hang_ve and dong.startswith("|") and bai_ve.dong[i + 1:i + 2] and bai_ve.dong[i + 1].startswith("| :"):
            ve_dau = dong  # hàng tiêu đề đứng ngay trên hàng gạch của bảng ĐẦU có hàng đánh số
    noi = []
    for bai in muc_luc:
        if not bai.rel.startswith(NHOM_NOI):
            continue
        ten = _nfc(bai.tieu_de)
        dong = tuple(d for d in (next((d for d in bai.dong if nhan.match(d)), None) for nhan in _NHAN) if d)
        ve = hang_ve.get(ten) or hang_ve.get(ten.removesuffix(" Huế"))
        if dong or ve:
            noi.append(Noi(ten, bai.rel, re.compile(rf"(?<!\w){re.escape(ten)}(?!\w)"), dong, ve))
    return Bang(tuple(noi), bai_ve.rel if bai_ve else "", bai_ve.tieu_de if bai_ve else "", ve_dau)


def the_moi(bang: Bang, ngu_canh: str, rel_da_co: frozenset[str], con: int) -> tuple[tuple[Noi, ...], tuple[str, ...]]:
    """Thẻ MỚI cho ngữ cảnh hiện có của lượt: (các nơi được gắn thẻ, các hàng vé lẻ kèm theo).
    Một nơi được gắn khi tên nó có trong `ngu_canh` VÀ bài riêng của nó chưa có nguồn nào trong sổ nguồn (`rel_da_co` — gồm cả thẻ đã gắn ở lần trước
    của lượt ⇒ không gắn hai lần). Nhiều nhất `con` nơi. Hàng vé đã có nguyên văn trong ngữ cảnh thì không chép lại; nơi chỉ có hàng vé mà hàng đó đã
    ở ngữ cảnh thì không còn gì để gắn."""
    ngu_canh = _nfc(ngu_canh)
    noi = tuple(n for n in bang.noi if n.rel not in rel_da_co and (n.dong or n.ve not in ngu_canh) and n.mau.search(ngu_canh))[:max(con, 0)]
    return noi, tuple(n.ve for n in noi if n.ve and n.ve not in ngu_canh)
