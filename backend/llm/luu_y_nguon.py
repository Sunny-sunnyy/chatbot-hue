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
# "nguồn không nêu việc tạm ngừng…" không phải là đã nêu. "chưa có thông tin" phải có: dòng ý thiếu của câu nhiều ý mở bằng hằng `CAU_Y_THIEU`
# ("Tư liệu chưa có thông tin về:") — thiếu nó thì dòng ý thiếu nhắc "tạm ngừng … lệnh cấm" bị coi là đã nêu cảnh báo (soát khác hãng 20/11).
_PHU_DINH = re.compile(r"không (nêu|đề cập|ghi|nói|có thông tin)|chưa (nêu|đề cập|ghi|nói|có thông tin)", re.I)
_TACH_CAU = re.compile(r"(?<=[.!?])\s+(?!\[)|\n")  # câu TRẢ LỜI: không tách trước mã trích đứng sau dấu chấm
# Câu của NGUỒN (chữ sẽ hiện cho người dùng): chỉ tách ở dấu kết câu + khoảng trắng + chữ HOA / số / dấu mở, và không tách sau viết tắt ("TP. Huế").
# Dấu chấm trong số tiền ("1.200.000") không có khoảng trắng sau nên không bao giờ là ranh câu. Tách thừa ⇒ câu cụt, nên thà không tách.
_KET_CAU = re.compile(r"[.!?]\s+")
_VIET_TAT = re.compile(r"\b(?:TP|Tp|Q|P|TS|ThS|GS|PGS|BS|St)\.$")
# Câu mở đầu bằng từ chỉ ngược về câu trước ⇒ đứng một mình thì thiếu nghĩa ⇒ không chép (review E 19/11)
_CHI_NGUOC = re.compile(r"^(?:Khi đó|Khi ấy|Lúc đó|Lúc này|Vào mùa này|Mùa này|Tại đây|Ở đây|Do đó|Vì vậy|Vì thế|Như vậy|Trong trường hợp này|"
                        r"Trường hợp này|Điều này|Việc này|Ngoài ra)\b", re.I)
# Điều khoản hoàn vé có nhắc thiên tai không phải cảnh báo an toàn của hoạt động ⇒ không chép vào dòng đậm (A quyết 19/11)
_HOAN_VE = re.compile(r"hoàn (?:trả|tiền|hủy|huỷ|vé)", re.I)
_MO_DON_VI = re.compile(r"^\s*(?:[-*+•]\s+|\d+[.)]\s+|#|\|)")  # dòng mở một gạch đầu dòng / mục số / tiêu đề / dòng bảng
_DAU_DONG = re.compile(r"^\s*(?:[-*+•]\s+|\d+[.)]\s+|#+\s*)*")
_LUU_Y_LAP = re.compile(r"^Lưu ý(?: quan trọng)?\s*:\s*", re.I)
TIEN_TO = "Lưu ý trong nguồn"
MAX_CAU = 400  # câu nguồn dài hơn ⇒ không nối (không cắt giữa câu: cắt có thể đổi nghĩa)


def _co_y(cau: str) -> bool:
    return bool(TAM_NGUNG.search(cau) and DIEU_KIEN.search(cau))


def _don_vi(doan: str) -> list[str]:
    """Bài kho có chỗ ngắt dòng cứng GIỮA câu ⇒ nối các dòng của cùng một đoạn văn / cùng một gạch đầu dòng thành một đơn vị trước khi tách câu
    (đọc từng dòng sẽ chép ra mẩu câu cụt — review E 19/11). Dòng trống, gạch đầu dòng, mục số, tiêu đề, dòng bảng mở đơn vị mới; dòng bảng bị bỏ."""
    ra: list[str] = []
    noi = False
    for dong in doan.split("\n"):
        if not dong.strip():
            noi = False
        elif dong.lstrip().startswith("|"):
            noi = False
        elif dong.lstrip().startswith("#"):  # dòng tiêu đề là đơn vị riêng: không nối dòng sau vào (chữ tiêu đề sẽ dính vào câu)
            ra.append(dong.strip())
            noi = False
        elif noi and not _MO_DON_VI.match(dong) and ra[-1][-1] not in ".!?:…":  # dòng trước đã kết câu ⇒ dòng này không phải phần nối của nó
            ra[-1] = f"{ra[-1]} {dong.strip()}"
        else:
            ra.append(dong.strip())
            noi = True
    return ra


def _gon(cau: str) -> str:
    """Bỏ ký hiệu trình bày quanh câu, không đổi chữ của câu: dấu `*`, cặp ngoặc bọc CẢ câu, chữ "Lưu ý:" mở đầu (tiền tố ghi chú đã nói)."""
    chu = cau.replace("*", "").strip()
    if chu.startswith("(") and chu.rstrip(".").endswith(")") and chu.count("(") == 1:
        chu = chu.rstrip(".")[1:-1].strip()
    chu = _LUU_Y_LAP.sub("", chu).strip()
    return chu if not chu or chu[-1] in ".!?…" else f"{chu}."


def cau_cua_don_vi(don_vi: str) -> list[str]:
    """Các câu của một đơn vị nguồn (đã bỏ gạch đầu dòng / số thứ tự)."""
    chu, ra, dau = _DAU_DONG.sub("", don_vi).strip(), [], 0
    for m in _KET_CAU.finditer(chu):
        sau = chu[m.end():m.end() + 1]
        if (sau.isupper() or sau.isdigit() or sau in "\"“«(*") and not _VIET_TAT.search(chu[:m.start() + 1]):
            ra.append(chu[dau:m.start() + 1])
            dau = m.end()
    return [c for c in (*ra, chu[dau:]) if c.strip()]


def cac_cau_tam_ngung(doan: str) -> list[str]:
    """Mọi câu của đoạn nguồn tự nó có đủ từ tạm ngừng + điều kiện và đứng một mình được: mở bằng chữ hoa / số, không mở bằng từ chỉ ngược,
    không phải điều khoản hoàn vé, không quá dài (theo thứ tự trong đoạn). Công cụ quét kho dùng hàm này để liệt kê MỌI câu luật có thể chép."""
    ra = []
    for don_vi in _don_vi(doan):
        for tho in cau_cua_don_vi(don_vi):
            cau = _gon(tho)
            if (cau and _co_y(cau) and (cau[0].isupper() or cau[0].isdigit()) and not _CHI_NGUOC.search(cau) and not _HOAN_VE.search(cau)
                    and len(cau) <= MAX_CAU):
                ra.append(cau)
    return ra


def cau_tam_ngung(doan: str) -> str | None:
    """Câu đầu tiên của `cac_cau_tam_ngung`, hoặc None."""
    return next(iter(cac_cau_tam_ngung(doan)), None)


def dong_tam_ngung(answer: str, nguon_da_trich: Iterable[tuple[str, Iterable[str]]]) -> str | None:
    """Dòng ghi chú cho một câu trả lời, hoặc None. `nguon_da_trich` = (nhãn nguồn — tên bài [— tên mục], các đoạn chữ) của từng nguồn câu trả lời
    ĐÃ TRÍCH, theo thứ tự. Câu trả lời đã có một câu nêu ý ⇒ None (không nối trùng). Nhiều nguồn cùng có ⇒ chỉ câu đầu tiên của nguồn đầu tiên."""
    if any(_co_y(cau) and not _PHU_DINH.search(cau) for cau in _TACH_CAU.split(answer or "")):
        return None
    for nhan, cac_doan in nguon_da_trich:
        for doan in cac_doan:
            cau = cau_tam_ngung(doan)
            if cau:
                return f"{TIEN_TO} «{nhan}»: {cau}"
    return None


def nhan_nguon(ten_bai: str, duong_muc: Iterable[str] = ()) -> str:
    """Nhãn hiện cho người dùng: tên bài, kèm tên mục cuối của đoạn khi có (bài chung nhiều nơi — tên bài một mình không nói đoạn nói về đâu)."""
    muc = [m for m in duong_muc if m and m != ten_bai]
    return f"{ten_bai} — {muc[-1]}" if muc else ten_bai
