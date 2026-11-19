"""Cờ `noi_dong_tam_ngung` (19/11/2026) — dòng ghi chú an toàn do CODE chép từ nguồn câu trả lời đã trích.

Vì sao: lượt đo cuối 18/11, câu hỏi về quy định của một hoạt động trên sông — model trích đúng đoạn kho có dòng "mùa mưa lũ / có lệnh cấm thì
tạm ngừng" nhưng bỏ dòng đó 7 / 7 lần. Thử dặn model bằng một câu lời dặn (cờ `luu_y_an_toan`, nhánh riêng): nêu được, nhưng câu dặn vào mọi câu
hỏi và lượt đo không đạt mức tụt ghi trước ⇒ làm bằng code: không gọi model, không đổi chuỗi gửi model, chép NGUYÊN một câu của nguồn.
Luật hẹp có chủ ý: chỉ nguồn ĐÃ ĐƯỢC TRÍCH; chỉ khi MỘT câu của nguồn vừa có từ tạm ngừng vừa có điều kiện (không ghép hai câu / hai dòng rời).
"""
import re
from collections.abc import Iterable

# Hai bộ từ = bộ dò đã dùng để đo (`data/phase_9/s09_luu_y/tools/do_y.py` bản 2, 14 câu dò). Đổi bộ từ ⇒ đo lại bước nối trên câu trả lời đã có.
TAM_NGUNG = re.compile(r"tạm ngừng|tạm dừng|tạm nghỉ|tạm đóng|ngừng hoạt động|dừng hoạt động|không hoạt động|ngừng phục vụ|ngừng chạy|ngừng đón|"
                       r"\bhoãn\b|\bhuỷ\b|\bhủy\b|không xuất bến|cấm xuất bến|không được (phép )?xuất bến", re.I)
DIEU_KIEN = re.compile(r"\blũ\b|\blụt\b|lệnh cấm|thời tiết xấu|mưa bão|\bbão\b(?! ho[àa])|nước (sông )?(dâng|lên)", re.I)
_PHU_DINH = re.compile(r"không (nêu|đề cập|ghi|nói|có thông tin)|chưa (nêu|đề cập|ghi)", re.I)  # "nguồn không nêu việc tạm ngừng…" không phải là đã nêu
_TACH_CAU = re.compile(r"(?<=[.!?])\s+(?!\[)|\n")  # câu TRẢ LỜI: không tách trước mã trích đứng sau dấu chấm
# Câu của NGUỒN (chữ sẽ hiện cho người dùng): chỉ tách ở dấu kết câu + khoảng trắng + chữ HOA / số / dấu mở, và không tách sau viết tắt ("TP. Huế").
# Dấu chấm trong số tiền ("1.200.000") không có khoảng trắng sau nên không bao giờ là ranh câu. Tách thừa ⇒ câu cụt, nên thà không tách.
_KET_CAU = re.compile(r"[.!?]\s+")
_VIET_TAT = re.compile(r"\b(?:TP|Tp|Q|P|TS|ThS|GS|PGS|BS|St)\.$")
# Câu mở đầu bằng từ chỉ ngược về câu trước ⇒ đứng một mình thì thiếu nghĩa ⇒ không chép (review E 19/11)
_CHI_NGUOC = re.compile(r"^(?:Khi đó|Khi ấy|Lúc đó|Lúc này|Vào mùa này|Mùa này|Tại đây|Ở đây|Do đó|Vì vậy|Vì thế|Như vậy|Trong trường hợp này|"
                        r"Trường hợp này|Điều này|Việc này|Ngoài ra)\b", re.I)
_DAU_DONG = re.compile(r"^\s*(?:[-*+•]\s+|\d+[.)]\s+)*")
TIEN_TO = "Lưu ý trong nguồn"
MAX_CAU = 400  # câu nguồn dài hơn ⇒ không nối (không cắt giữa câu: cắt có thể đổi nghĩa)


def _co_y(cau: str) -> bool:
    return bool(TAM_NGUNG.search(cau) and DIEU_KIEN.search(cau))


def cau_cua_dong(dong: str) -> list[str]:
    """Các câu của một dòng nguồn, đã bỏ gạch đầu dòng / số thứ tự / dấu `**`. Dòng bảng (mở bằng "|") ⇒ không câu nào."""
    if dong.lstrip().startswith("|"):
        return []
    chu, ra, dau = _DAU_DONG.sub("", dong).replace("**", "").strip(), [], 0
    for m in _KET_CAU.finditer(chu):
        sau = chu[m.end():m.end() + 1]
        if (sau.isupper() or sau.isdigit() or sau in "\"“«(") and not _VIET_TAT.search(chu[:m.start() + 1]):
            ra.append(chu[dau:m.start() + 1])
            dau = m.end()
    return [c for c in (*ra, chu[dau:]) if c]


def cau_tam_ngung(dong: str) -> str | None:
    """Câu ĐẦU TIÊN của dòng nguồn tự nó có đủ từ tạm ngừng + điều kiện, đứng một mình được (không mở bằng từ chỉ ngược), không quá dài; không có ⇒ None."""
    return next((c for c in cau_cua_dong(dong) if _co_y(c) and not _CHI_NGUOC.search(c) and len(c) <= MAX_CAU), None)


def dong_tam_ngung(answer: str, nguon_da_trich: Iterable[tuple[str, Iterable[str]]]) -> str | None:
    """Dòng ghi chú cho một câu trả lời, hoặc None. `nguon_da_trich` = (tên bài, các đoạn chữ) của từng nguồn câu trả lời ĐÃ TRÍCH, theo thứ tự.
    Câu trả lời đã có một câu nêu ý ⇒ None (không nối trùng). Nhiều nguồn cùng có ⇒ chỉ câu đầu tiên của nguồn đầu tiên (tối đa một dòng)."""
    if any(_co_y(cau) and not _PHU_DINH.search(cau) for cau in _TACH_CAU.split(answer or "")):
        return None
    for ten_bai, cac_doan in nguon_da_trich:
        for doan in cac_doan:
            for dong in doan.split("\n"):
                cau = cau_tam_ngung(dong)
                if cau:
                    return f"{TIEN_TO} «{ten_bai}»: {cau}"
    return None
