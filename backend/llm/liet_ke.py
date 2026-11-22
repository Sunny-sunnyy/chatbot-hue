"""Công cụ `liet_ke_bai` — liệt kê BÀI của kho theo nhóm / cụm từ, do code trả lời (plan `report_agent/2026-11-21/b_cong_cu_liet_ke_plan.md`).

Vì sao: câu xin danh sách và câu "nơi nào có đặc điểm X" cần chạm NHIỀU BÀI, mà bước tìm chỉ trả 10 đoạn (đếm 21/11: lăng 2 / 8 bài, quán cà phê
3 / 24, lễ hội 0 / 39). Ở đây code đi qua mọi bài của một nhóm, so NGUYÊN CỤM TỪ trên tên bài + toàn văn, trả mỗi bài một dòng kèm một dòng làm chứng
lấy từ chính bài đó. Không gọi model, không dữ liệu mới: nhóm = thư mục của bài trong kho (không nhãn tự đặt).

Module thuần (không đọc cấu hình, không SDK); `assistant.py` bọc thành công cụ của một lượt.
"""
from dataclasses import dataclass
from pathlib import Path
import re
import unicodedata

from ingestion.chunking.markdown_blocks import EXCLUDED_SECTIONS
from ingestion.source_state import read_source_lf

# Nhóm = thư mục của bài trong kho ⇒ nhãn hiển thị. Bài cẩm nang nằm ngay ở thư mục lĩnh vực (không thuộc nhóm nào) chỉ có mặt khi chọn `tat_ca`.
NHOM = {
    "quan_an": ("foods/restaurants/", "quán ăn"),
    "quan_ca_phe": ("foods/cafes/", "quán cà phê"),
    "mon_dac_san": ("foods/local_specialties/", "món đặc sản"),
    "le_hoi": ("festivals/festival/", "lễ hội"),
    "di_tich": ("heritages/heritage/", "di tích"),
    "nghe_thuat": ("performing_arts/arts/", "nghệ thuật biểu diễn"),
    "diem_den": ("travel/places/", "điểm đến"),
    "dich_vu": ("travel/services/", "dịch vụ du lịch"),
    "ve": ("travel/tickets/", "vé"),
}
TAT_CA = "tat_ca"
TIEU_DE_NGUON = "Mục lục kho tư liệu"
NGUON_SOURCE = "he-thong-muc-luc"  # `source` của nguồn — không phải một bài kho (không `bai_id`)
TOI_DA_DONG = 40          # số bài tối đa trong một kết quả; nhiều hơn ⇒ dòng "còn k bài nữa"
TOI_DA_CUM_TU = 3
CUM_TU_DAI_NHAT = 40      # ký tự; cụm dài hơn bị bỏ (câu cả dòng không phải "cụm từ")
DONG_DAI_NHAT = 220       # ký tự của dòng làm chứng
SO_LAN_MOI_LUOT = 2
NGOAI_NHOM_IT = 5         # nhóm đang lọc CÓ bài khớp mà ngoài nhóm còn nhiều hơn số này ⇒ không nhắc mở rộng (cụm từ phổ biến: nhắc là nhiễu)

_GACH = re.compile(r"\s*[-–—−]\s*")
_DAU_DONG = re.compile(r"^(?:[-*+]\s+|\d+\.\s+)")
_MARKUP = re.compile(r"\*\*|__|`")


def chuan(text: str) -> str:
    """Dạng để SO cụm từ: NFC, không phân biệt hoa thường, gộp khoảng trắng, mọi kiểu gạch nối thành `-` và bỏ khoảng trắng quanh nó
    ("6h - 8h" khớp "6h–8h"). GIỮ dấu tiếng Việt — bỏ dấu dễ khớp nhầm."""
    return _GACH.sub("-", " ".join(unicodedata.normalize("NFC", text).casefold().split()))


@dataclass(frozen=True)
class Bai:
    rel: str                       # đường dẫn tương đối của file trong kho
    tieu_de: str
    dong: tuple[str, ...]          # các dòng chữ của bài (đã bỏ ký hiệu Markdown đầu dòng), không gồm tiêu đề
    dong_chuan: tuple[str, ...]    # `chuan` của từng dòng — tính một lần lúc nạp
    tom_tat: str                   # dòng giới thiệu bài khi không lọc theo cụm từ


@dataclass(frozen=True)
class KetQua:
    tong: int                      # số bài khớp (trước khi cắt trang)
    o_ten: int                     # trong đó số bài có cụm từ ngay ở TÊN bài (xếp trước)
    dong: tuple[str, ...]          # "Tên bài — dòng làm chứng", tối đa `TOI_DA_DONG`
    cum_tu: tuple[str, ...]        # cụm từ thật sự dùng để lọc (đã bỏ cụm rỗng / quá dài)
    ngoai_nhom: int = 0            # số bài Ở NHÓM KHÁC cũng có cụm từ (0 khi lọc `tat_ca` hoặc không có cụm từ) — để model biết nên mở rộng nhóm
    nhom: str = TAT_CA             # nhóm đã lọc — dòng trạng thái nói "trong nhóm …" chứ không nói "trong tư liệu" khi chỉ lọc một nhóm
    bai: tuple[Bai, ...] = ()      # các bài ứng với `dong` (cùng thứ tự) — để phần nối ghi chú / cảnh báo của nguồn bài vẫn chạy khi câu trả lời trích mục lục


def _sach(line: str) -> str:
    return _MARKUP.sub("", _DAU_DONG.sub("", line.strip())).strip()


def _tom_tat(dong: list[tuple[str, str]]) -> str:
    """Dòng giới thiệu một bài: dòng "Loại hình: …" nếu có, không thì câu đầu của mục "Tóm tắt", không thì dòng chữ đầu tiên."""
    for _, text in dong:
        if text.casefold().startswith("loại hình:"):
            return text
    for muc, text in dong:
        if muc.casefold() == "tóm tắt":
            return text
    return dong[0][1] if dong else ""


def bai_tu_markdown(rel: str, markdown: str) -> Bai:
    """Các dòng chữ của một bài — KHÔNG gồm mục bộ chia đoạn bỏ (`EXCLUDED_SECTIONS`: "Nguồn dữ liệu", kể cả mục con). Soát khác hãng 22/11 (K6): mục đó
    chứa ghi chú đối chiếu nội bộ, URL và dòng giá CŨ mà lệnh sửa kho giữ làm lịch sử ("mục này chatbot không đọc"); công cụ từng đọc cả mục nên các
    dòng ấy thành căn cứ [n] (cụm "đối chiếu" khớp 29 bài, "https://" khớp 79 bài)."""
    tieu_de, muc, dong, cap_bo = Path(rel).stem, "", [], 0  # `cap_bo` > 0: đang ở trong một mục bị bỏ, = cấp tiêu đề của mục đó
    for raw in markdown.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# ") and tieu_de == Path(rel).stem:
            tieu_de = line[2:].strip()
        elif line.startswith("#"):
            muc, cap = line.lstrip("#").strip(), len(line) - len(line.lstrip("#"))
            if cap_bo and cap <= cap_bo:  # tiêu đề cùng cấp hoặc cao hơn ⇒ ra khỏi mục bị bỏ
                cap_bo = 0
            if not cap_bo and muc in EXCLUDED_SECTIONS:
                cap_bo = cap
        elif cap_bo:
            continue
        else:
            text = _sach(line)
            if text:
                dong.append((muc, text))
    return Bai(rel=rel, tieu_de=tieu_de, dong=tuple(t for _, t in dong), dong_chuan=tuple(chuan(t) for _, t in dong), tom_tat=_tom_tat(dong))


def nap_muc_luc(root: Path, rel_paths: list[str]) -> tuple[Bai, ...]:
    """Mục lục của kho đang chạy: mọi file mà `discover_full_corpus_files` trả (cùng danh sách bài của chỉ mục), xếp theo tiêu đề."""
    bai = [bai_tu_markdown(rel, read_source_lf(root / rel)) for rel in rel_paths]
    return tuple(sorted(bai, key=lambda b: chuan(b.tieu_de)))


def _cat(text: str) -> str:
    return text if len(text) <= DONG_DAI_NHAT else text[:DONG_DAI_NHAT].rsplit(" ", 1)[0] + "…"


def _cat_quanh(text: str, cum: tuple[str, ...]) -> str:
    """Dòng làm chứng của bài chỉ nhắc cụm từ trong thân: dòng dài hơn `DONG_DAI_NHAT` thì cắt MỘT CỬA SỔ QUANH chỗ có cụm từ (review 21/11: cắt 220 ký tự
    đầu dòng làm 6 / 16 bài của cụm "chợ" nhận dòng không còn chữ "chợ" ⇒ model nêu chi tiết không có trong nguồn đã trích). Luôn trả đoạn CÒN chứa cụm
    từ: thử cửa sổ quanh vị trí ước lượng, chưa chứa thì nới gấp đôi cho tới cả dòng."""
    if len(text) <= DONG_DAI_NHAT:
        return text
    ca = chuan(text)
    vi_tri = min(ca.find(c) for c in cum if c in ca)
    giua = int(vi_tri / max(len(ca), 1) * len(text))  # `chuan` chỉ gộp khoảng trắng / gạch nối ⇒ vị trí trên chữ gốc lệch ít
    rong = DONG_DAI_NHAT
    while True:
        dau = max(0, min(giua - rong // 3, len(text) - rong))
        doan = text[dau:dau + rong]
        if any(c in chuan(doan) for c in cum) or rong >= len(text):
            break
        rong *= 2
    if dau > 0:
        doan = "…" + doan.split(" ", 1)[-1]
    if dau + rong < len(text):
        doan = doan.rsplit(" ", 1)[0] + "…"
    return doan if any(c in chuan(doan) for c in cum) else text  # cắt ở ranh từ làm mất cụm từ (hiếm) ⇒ giữ cả dòng


def loc(muc_luc: tuple[Bai, ...], nhom: str, cum_tu: list[str]) -> KetQua:
    """Bài của `nhom` (hoặc mọi bài khi `tat_ca`) mà tên bài hoặc toàn văn chứa ÍT NHẤT MỘT cụm từ; không có cụm từ ⇒ mọi bài của nhóm.
    So nguyên cụm sau `chuan` — không phải biểu thức. Bài có cụm từ ngay ở TÊN xếp trước (đó thường là "loại" người hỏi cần: lăng, chùa, bún bò…) với
    dòng giới thiệu của bài; bài chỉ nhắc cụm từ trong thân xếp sau, kèm đúng dòng đầu tiên chứa cụm từ để model đọc ngữ cảnh (kể cả câu phủ định)."""
    prefix = "" if nhom == TAT_CA else NHOM[nhom][0]
    cum = tuple(dict.fromkeys(c for c in (chuan(x) for x in cum_tu[:TOI_DA_CUM_TU]) if c and len(c) <= CUM_TU_DAI_NHAT))
    o_ten, o_than, ngoai_nhom = [], [], 0
    for bai in muc_luc:
        trong_nhom = bai.rel.startswith(prefix)
        if not cum:
            if trong_nhom:
                o_than.append((bai, bai.tom_tat))
            continue
        o_tieu_de = any(c in chuan(bai.tieu_de) for c in cum)
        co = [i for i, d in enumerate(bai.dong_chuan) if any(c in d for c in cum)]
        if not trong_nhom:
            ngoai_nhom += bool(o_tieu_de or co)
        elif o_tieu_de:
            o_ten.append((bai, _cat(bai.tom_tat)))
        elif co:
            # dòng ĐẦU TIÊN chứa cụm từ, cắt quanh cụm từ; bài còn dòng khác cũng có cụm từ ⇒ nói số dòng (review 21/11: ý cần tìm nằm ở dòng sau ⇒ model
            # đọc đúng dòng nhận được nhưng sót ý) để model biết cần `tim_kho` bài đó
            them = f" (+{len(co) - 1} dòng khác của bài cũng có cụm từ)" if len(co) > 1 else ""
            o_than.append((bai, _cat_quanh(bai.dong[co[0]], cum) + them))
    khop = o_ten + o_than
    if not cum:
        khop = [(bai, _cat(chung)) for bai, chung in khop]
    dong = tuple(f"{bai.tieu_de} — {chung}" if chung else bai.tieu_de for bai, chung in khop[:TOI_DA_DONG])
    return KetQua(tong=len(khop), o_ten=len(o_ten), dong=dong, cum_tu=cum, ngoai_nhom=ngoai_nhom, nhom=nhom, bai=tuple(bai for bai, _ in khop[:TOI_DA_DONG]))


def muc_nguon(nhom: str, kq: KetQua) -> str:
    """Tên mục của nguồn (model và người đọc sổ nguồn thấy): nhóm + cụm từ đã lọc."""
    ten = "mọi nhóm" if nhom == TAT_CA else NHOM[nhom][1]
    return f"Bài thuộc nhóm {ten}" + (f" có cụm từ: {'; '.join(kq.cum_tu)}" if kq.cum_tu else "")


LAN_CUOI = ("Đây là lần dùng cuối của công cụ liet_ke_bai trong câu này: bước kế hãy viết câu trả lời từ Bằng chứng đã có, hoặc dùng tim_kho nếu còn "
            "cần chi tiết của một nơi.")


def trang_thai_lap(ma_nguon: int | None) -> str:
    """Model gọi lại đúng nhóm + cụm từ đã gọi trong câu này: không lọc lại, không đăng nguồn lần hai."""
    da_co = f"kết quả đã có ở nguồn [{ma_nguon}] phía trên" if ma_nguon is not None else "lần trước đã không có bài nào khớp"
    return f"Trạng thái: lời gọi này trùng một lời gọi trước trong câu — {da_co}. Không gọi lại với cùng nhóm và cụm từ."


def trang_thai(kq: KetQua) -> str:
    """Dòng đầu của kết quả công cụ (đứng ngoài khối nguồn): có bao nhiêu bài khớp, có bị cắt trang không."""
    # lọc theo MỘT nhóm che bài ở nhóm khác (review 21/11: "công viên nước" nằm ở một bài vé, model lọc nhóm điểm đến ⇒ nói "tư liệu không thấy") ⇒ luôn nói
    # còn bao nhiêu bài ngoài nhóm có cụm từ
    # … nhưng chỉ khi nhóm này ra 0 bài hoặc số bài ngoài nhóm ÍT: lượt thật sau khi thêm câu nhắc — cụm "chợ" có 39 bài ngoài nhóm, luna nghe theo, gọi lại
    # `tat_ca` (61 bài) rồi tìm thêm hai lần ⇒ 29 giây cho một câu trước đó 15 giây.
    nhac = kq.ngoai_nhom and (kq.tong == 0 or kq.ngoai_nhom <= NGOAI_NHOM_IT)
    ngoai = f" Ngoài nhóm này còn {kq.ngoai_nhom} bài khác có cụm từ — gọi lại với nhom = tat_ca để xem." if nhac else ""
    if kq.tong == 0:
        if ngoai:
            return "Trạng thái: không có bài nào của nhóm này khớp." + ngoai
        return "Trạng thái: không có bài nào trong tư liệu khớp. Thử một lần với cụm từ khác (ngắn hơn, cách viết khác) hoặc nhóm khác; vẫn không có thì coi như tư liệu không có thông tin này."
    con = kq.tong - len(kq.dong)
    ten = f" ({kq.o_ten} bài có cụm từ ngay ở tên, xếp trước; {kq.tong - kq.o_ten} bài chỉ nhắc tới trong nội dung)" if kq.cum_tu and kq.o_ten and kq.o_ten < kq.tong else ""
    # lọc MỘT nhóm ⇒ "trong nhóm …" (review 21/11: viết "trong tư liệu có 22 bài" khi ngoài nhóm còn 39 bài có cụm từ làm model nói sai tổng số)
    o_dau = "trong tư liệu" if kq.nhom == TAT_CA else f"trong nhóm {NHOM[kq.nhom][1]}"
    return (f"Trạng thái: {o_dau} có {kq.tong} bài khớp{ten}" + (f", dưới đây là {len(kq.dong)} bài đầu; còn {con} bài nữa — thêm cụm từ để thu hẹp." if con else ".")
            + " Mỗi dòng là tên bài và một dòng lấy từ chính bài đó." + ngoai)
