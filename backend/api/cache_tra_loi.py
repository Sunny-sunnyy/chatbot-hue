"""Nhớ câu trả lời giữa các cuộc trò chuyện (plan `report_agent/2026-11-20/b_cache_cau_tra_loi_plan.md`; User 20/11/2026).

Một người hỏi một câu và được trả lời từ kho; trong 24 giờ người KHÁC gõ ĐÚNG câu đó ở lượt đầu của một cuộc mới ⇒ route trả lại bản đã lưu
(cùng chữ, cùng nguồn, cùng dòng ghi chú), không tìm kho, không gọi model. Chỉ khớp đúng chữ sau chuẩn hoá — KHÔNG khớp theo nghĩa (khớp theo
nghĩa trả nhầm câu của "lăng A" cho "lăng B"; nghiên cứu 05/11).

Kho trong RAM của một tiến trình, trần số mục, không ghi đĩa, không log chữ hay khoá. Khởi động lại server ⇒ mất hết. Bản lưu không mang mã
cuộc, cookie hay IP: chỉ chữ trả lời + nguồn kho + ghi chú của một lượt KHÔNG có lịch sử (không dựa vào gì của cuộc trước).
"""
import hashlib
import time
import unicodedata
from collections import OrderedDict
from dataclasses import dataclass
from typing import Callable

from llm import thoi_tiet as tt

SONG_GIAY = 24 * 60 * 60
TRAN_SO_MUC = 500


@dataclass(frozen=True)
class BanLuu:
    """Đúng những gì route cần để dựng lại phản hồi của lượt: chữ gốc của model (chưa chuẩn hoá mã trích dẫn — route chuẩn hoá như mọi lượt),
    các nguồn kho được trích, dòng ghi chú "có thể đã thay đổi" (hoặc None), tuyến."""
    answer: str
    cited: tuple
    notice: str | None
    route: str


def chuan_hoa(cau: str) -> str:
    """Câu để so khớp: Unicode NFC, gộp khoảng trắng, bỏ khoảng trắng hai đầu, chữ thường. KHÔNG bỏ dấu thanh, dấu câu hay sửa lỗi gõ —
    đổi một ký tự có nghĩa là một câu khác."""
    return " ".join(unicodedata.normalize("NFC", cau).split()).casefold()


def dau_phien_ban(*phan: str | bytes) -> str:
    """Băm các thứ quyết định câu trả lời ngoài chính câu hỏi (kho, lời dặn, model, cờ, bản code) — nơi dựng app gom rồi đưa vào.
    Một thứ đổi ⇒ dấu đổi ⇒ mọi bản lưu cũ không còn trúng."""
    bam = hashlib.sha256()
    for p in phan:
        du_lieu = p if isinstance(p, bytes) else p.encode("utf-8")
        bam.update(len(du_lieu).to_bytes(8, "big") + du_lieu)  # kèm độ dài: ("ab", "c") khác ("a", "bc")
    return bam.hexdigest()


def luot_luu_duoc(trace, tu_choi: bool) -> bool:
    """Lượt ĐÃ XONG có được lưu không (nơi gọi đã chắc: lượt đầu của cuộc, không nút / biểu mẫu, kết quả "success").
    Chỉ lượt trả lời từ kho, có nguồn, và mọi công cụ đã chạy đều là tìm kho — một luật loại cả thời tiết, ngày / lịch âm, khoảng cách, lịch,
    tra web, bão lũ (đều đổi theo giờ hoặc theo người). Lượt có câu an toàn trong ghi chú cũng không lưu: chỗ an toàn chọn chặt."""
    cau_an_toan = tt.CAU_BAO_LU in (trace.notice or "") or trace.luu_y_nguon is not None
    return (not tu_choi and trace.fixed_outcome is None and trace.citation_error is None and bool(trace.cited)
            and trace.web is None and trace.lich is None and trace.lich_v2 is None and trace.clarify is None and trace.lam_thay is None
            and trace.today is None and trace.thoi_tiet_noi is None and trace.thoi_tiet_dau is None
            and all(cong_cu["name"] == "tim_kho" for cong_cu in trace.tools) and not cau_an_toan)


class CacheTraLoi:
    def __init__(self, phien_ban: str, *, song_giay: float = SONG_GIAY, tran: int = TRAN_SO_MUC,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self._phien_ban, self._song_giay, self._tran, self._clock = phien_ban, song_giay, tran, clock
        self._muc: OrderedDict[str, tuple[float, BanLuu]] = OrderedDict()  # khoá ⇒ (giờ hết hạn, bản lưu); thứ tự = thứ tự lưu

    def _khoa(self, cau: str) -> str:
        return dau_phien_ban(self._phien_ban, chuan_hoa(cau))

    def lay(self, cau: str) -> BanLuu | None:
        khoa = self._khoa(cau)
        muc = self._muc.get(khoa)
        if muc is None:
            return None
        if muc[0] <= self._clock():  # hết hạn ⇒ coi như không có
            del self._muc[khoa]
            return None
        return muc[1]

    def luu(self, cau: str, ban: BanLuu) -> None:
        khoa = self._khoa(cau)
        self._muc.pop(khoa, None)  # lưu lại ⇒ tính hạn mới, xếp cuối
        self._muc[khoa] = (self._clock() + self._song_giay, ban)
        while len(self._muc) > self._tran:  # trần RAM: bỏ mục lưu sớm nhất
            self._muc.popitem(last=False)

    def __len__(self) -> int:
        return len(self._muc)
