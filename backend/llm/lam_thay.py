"""Cờ `noi_that_lam_thay` (19/11/2026) — người dùng NHỜ TRỢ LÝ TỰ LÀM một việc hệ thống không có (đặt chỗ, gửi thư / tin, xem tình trạng phòng)
mà câu trả lời đã là câu từ chối khuôn ⇒ code thay bằng một câu nói thật giới hạn (`full_corpus_prompt.CAU_LAM_THAY`), không mở mục web.

Hàm thuần: chỉ đọc câu người dùng của lượt đó; không model, không kho, không lịch sử. Danh sách CHO PHÉP hẹp — câu phải có dấu "nhờ làm",
câu hỏi thông tin (ở đâu, cách nào, số điện thoại…) và câu nhờ soạn / tóm / chép ⇒ None. Sót một cách nói lạ ⇒ lượt đó y như khi cờ tắt.
Chỉ nhận tiếng Việt CÓ DẤU (quyết định sản phẩm sẵn có).
"""
import re

DAT_CHO, GUI, TINH_TRANG = "dat_cho", "gui", "tinh_trang"

_TOI = r"(?:mình|tôi|tui|tớ|em|anh|chị|bọn mình|tụi mình|chúng tôi|nhà mình|gia đình mình)"
_GIUP = r"(?:giúp|hộ|dùm|giùm)"
_THU_DAT = r"(?:phòng|bàn|vé|xe|tour|chỗ|khách sạn|homestay|resort|villa)"
_KENH = r"(?:mail|email|e-mail|gmail|thư|zalo|tin nhắn|sms|messenger|số điện thoại|số đt|số máy)"
# Hỏi THÔNG TIN (nơi, cách, kênh liên hệ) hoặc nhờ việc hệ thống làm được bằng chữ (soạn, tóm, chép, dịch) ⇒ không phải "làm thay"
_HOI_THONG_TIN = re.compile(r"ở đâu|chỗ nào|nơi nào|cách nào|bằng cách|\bcách\b|như thế nào|thế nào|làm sao|ra sao|hướng dẫn|"
                            r"(?:xin|cho|biết|có)\b[^,;.?!]*số điện thoại|số điện thoại (?:để|nào)|sđt|hotline|website|trang nào|trang web|app nào|ứng dụng nào|kênh nào|qua đâu|"
                            r"trước bao lâu|bao lâu|khi nào|có cần|có nên|nên đặt|phải đặt|cần đặt")
_VIEC_BANG_CHU = re.compile(r"\b(?:soạn|viết|tóm|tóm tắt|tóm gọn|copy|chép|dịch|mẫu)\b")

# Review B (19/11): mẫu rộng bắt nhầm "đã đặt phòng …, gợi ý giúp mình quán", "đặt vé tàu … giúp tiết kiệm hơn …", "bạn đặt lịch … xe đỡ chạy vòng",
# "đặt giúp mình một câu hỏi về phòng trưng bày" ⇒ thứ được đặt phải đứng GẦN động từ (≤ 3 từ), không vắt qua dấu phẩy; dấu nhờ đứng SAU thứ
# được đặt chỉ nhận ở cuối câu ("đặt phòng này giúp mình nhé"); câu kể việc đã đặt / hỏi kinh nghiệm ⇒ không phải nhờ.
_GAN = r"(?:[^\s,;:.?!]+\s+){0,3}"
_CUOI = rf"(?:\s+{_TOI})?(?:\s+(?:với|nhé|nha|nhen|đi|luôn|được không|được ko|được k|nha bạn|nhé bạn))*\s*[.!?]*$"
_DA_DAT = re.compile(r"\b(?:đã|vừa|mới|lỡ|từng)\s+(?:đặt|book)\b|bao giờ chưa|\b(?:đặt|book)\s+(?:giúp\s+\S+\s+)?(?:một\s+|1\s+)?(?:câu hỏi|tên|lịch)\b")
_DAT_NHO = re.compile(rf"\b(?:đặt|book)\s+{_GIUP}\s+(?:{_TOI}\s+)?{_GAN}{_THU_DAT}\b"         # "đặt giúp mình 1 phòng đôi"
                      rf"|\b(?:đặt|book)\s+cho\s+{_TOI}\s+{_GAN}{_THU_DAT}\b"                # "đặt cho mình một bàn"
                      rf"|\b(?:{_GIUP}|nhờ)\s+(?:{_TOI}|bạn)\s+(?:đặt|book)\s+{_GAN}{_THU_DAT}\b"  # "giúp mình đặt phòng", "nhờ bạn đặt bàn"
                      rf"|\b(?:đặt|book)\s+{_GAN}{_THU_DAT}\b[^,;:.?!]*?\s{_GIUP}{_CUOI}"     # "đặt phòng này giúp mình nhé" (dấu nhờ ở cuối câu)
                      rf"|\b(?:bạn|bot|trợ lý|ad)\s+(?:có thể\s+)?(?:đặt|book)\s+{_GAN}{_THU_DAT}\b")  # "bạn đặt xe đi Lăng Cô … luôn nhé"
_LINK_DAT = re.compile(r"\blink\s+(?:để\s+)?(?:đặt|book)")                                  # "cho link đặt đúng khách sạn này"
# Bộ dò của C (19/11, sửa đúng một lần): thêm "gửi tin nhắn / thư … giúp", "nhắn … cho <nơi> … giúp", "email cho mình …"; câu gửi ĐỒ VẬT
# (bưu thiếp, hành lý, quà, xe…) là việc của người dùng ⇒ không bắt.
_BEN_NHAN = r"(?:khách sạn|nhà hàng|quán|homestay|resort|chủ nhà|lễ tân|nhà xe|tài xế|bên đó|họ)"
_GUI_KENH = re.compile(rf"\bgửi\b.*\b(?:qua|vào|tới|đến|sang|lên)\s+{_KENH}"
                       rf"|\bgửi\s+(?:một\s+|1\s+)?(?:tin nhắn|thư|mail|email|e-mail|sms)\b[^,;.?!]*\b{_GIUP}\b"   # "gửi tin nhắn cho khách sạn báo giúp mình là…"
                       rf"|\bnhắn(?:\s+tin)?\b[^,;.?!]*\bcho\s+{_BEN_NHAN}\b[^,;.?!]*\b{_GIUP}\b"               # "nhắn tin cho khách sạn giúp mình là…"
                       rf"|\bnhắn(?:\s+tin)?\s+{_GIUP}\s+{_TOI}\s+cho\s+{_BEN_NHAN}\b"                          # "nhắn giúp mình cho nhà hàng là…"
                       rf"|^(?:email|mail)\s+cho\s+{_TOI}\b")                                                    # "email cho mình bản lịch này"
_GUI_NHO = re.compile(rf"^\s*gửi\b|\bgửi\s+{_GIUP}\b|\b{_GIUP}\s+{_TOI}\s+gửi\b|\bgửi\b.*\bcho\s+{_TOI}\b"       # người gửi là trợ lý
                      rf"|\bnhắn(?:\s+tin)?\b|^(?:email|mail)\s+cho\b")
_GUI_DO = re.compile(r"bưu thiếp|bưu điện|bưu phẩm|bưu kiện|hành lý|vali|\bquà\b|\bđồ\b|gửi hàng|hàng hoá|gửi xe|gửi tiền")
_CON_PHONG = re.compile(r"\b(?:có|còn)\s+phòng\s+(?:trống\s+)?(?:chưa|không|ko|k|hông|hem)\b")
_YEU_CAU = re.compile(r"\b(?:yêu cầu|đơn|booking|đơn đặt)\b.*\b(?:được chưa|tới đâu|đến đâu|xác nhận chưa|xong chưa|được duyệt chưa)")


def nho_lam_thay(cau: str) -> str | None:
    """Loại việc "làm thay" của câu người dùng, hoặc None. Thứ tự: tình trạng ⇒ gửi ⇒ đặt chỗ (câu "mới gửi yêu cầu, có phòng chưa" là hỏi tình
    trạng; "gửi thư xác nhận đặt phòng vào mail giúp mình" là nhờ GỬI, không phải nhờ đặt)."""
    chu = " ".join((cau or "").casefold().split())
    if not chu or _VIEC_BANG_CHU.search(chu):
        return None
    if _CON_PHONG.search(chu) or _YEU_CAU.search(chu):
        return TINH_TRANG
    if _HOI_THONG_TIN.search(chu):
        return None
    if _GUI_KENH.search(chu) and _GUI_NHO.search(chu) and not _GUI_DO.search(chu):
        return GUI
    if _LINK_DAT.search(chu) or (_DAT_NHO.search(chu) and not _DA_DAT.search(chu)):
        return DAT_CHO
    return None
