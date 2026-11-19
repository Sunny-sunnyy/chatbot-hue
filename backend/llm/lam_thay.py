"""Cờ `noi_that_lam_thay` (19/11/2026) — người dùng NHỜ TRỢ LÝ TỰ LÀM một việc hệ thống không có (đặt chỗ, gửi thư / tin, xem tình trạng phòng)
mà câu trả lời đã là câu từ chối khuôn ⇒ code thay bằng một câu nói thật giới hạn (`full_corpus_prompt.CAU_LAM_THAY`), không mở mục web.

Hàm thuần: chỉ đọc câu người dùng của lượt đó; không model, không kho, không lịch sử. Danh sách CHO PHÉP hẹp — câu phải có dấu "nhờ làm",
câu hỏi thông tin (ở đâu, cách nào, số điện thoại…) và câu nhờ soạn / tóm / chép ⇒ None. Sót một cách nói lạ ⇒ lượt đó y như khi cờ tắt.
Chỉ nhận tiếng Việt CÓ DẤU (quyết định sản phẩm sẵn có).
"""
import re

DAT_CHO, GUI, TINH_TRANG = "dat_cho", "gui", "tinh_trang"
XEP_LICH = "xep_lich"  # cờ `chi_sang_len_ke_hoach`: lời nhờ XẾP LỊCH gõ tự do (`nho_xep_lich`) — câu cố định chỉ sang trang Lên kế hoạch

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
_DA_DAT = re.compile(r"\b(?:đã|vừa|mới|lỡ|từng)\s+(?:đặt|book)\b|bao giờ chưa|đặt cọc|tiền cọc"
                     r"|\b(?:đặt|book)\s+(?:giúp\s+\S+\s+)?(?:một\s+|1\s+)?(?:câu hỏi|tên|lịch)\b")
# Bản sửa CUỐI (phiên điều phối chốt 19/11, sau bộ bù của reviewer): THU HẸP — "giúp / hộ" chỉ là dấu nhờ khi KỀ đại từ ("đặt giúp mình …",
# "giúp mình đặt …") hoặc ở CUỐI câu ("đặt phòng này giúp mình nhé"); bắt nhầm một câu hỏi thông tin tệ hơn sót một câu nhờ làm thay.
_DAT_NHO = re.compile(rf"\b(?:đặt|book)\s+{_GIUP}\s+{_TOI}\s+{_GAN}{_THU_DAT}\b"              # "đặt giúp mình 1 phòng đôi"
                      rf"|\b(?:đặt|book)\s+cho\s+{_TOI}\s+{_GAN}{_THU_DAT}\b"                # "đặt cho mình một bàn"
                      rf"|\b(?:{_GIUP}|nhờ)\s+(?:{_TOI}|bạn)\s+(?:đặt|book)\s+{_GAN}{_THU_DAT}\b"  # "giúp mình đặt phòng", "nhờ bạn đặt bàn"
                      rf"|\b(?:đặt|book)\s+{_GAN}{_THU_DAT}\b[^,;:.?!]*?\s{_GIUP}{_CUOI}"     # "đặt phòng này giúp mình nhé" (dấu nhờ ở cuối câu)
                      rf"|\b(?:bạn|bot|trợ lý|ad)\s+(?:có thể\s+)?(?:đặt|book)\s+{_GAN}{_THU_DAT}\b")  # "bạn đặt xe đi Lăng Cô … luôn nhé"
_LINK_DAT = re.compile(r"\blink\s+(?:để\s+)?(?:đặt|book)")                                  # "cho link đặt đúng khách sạn này"
# Gửi: phải có KÊNH sau giới từ ("gửi … qua / vào / tới mail, zalo, số điện thoại…") hoặc "email cho mình …". Ba mẫu "gửi tin nhắn … giúp",
# "nhắn … cho <nơi> … giúp", "nhắn giúp mình cho …" đã thử ở bản trước và BỎ: bắt nhầm câu hỏi thông tin ("nhắn tin cho quán trước có giúp giữ
# bàn không") ⇒ các cách nói đó nay là SÓT có chủ ý. Câu gửi ĐỒ VẬT (bưu thiếp, hành lý, quà, xe…) là việc của người dùng ⇒ không bắt.
_GUI_KENH = re.compile(rf"\bgửi\b.*\b(?:qua|vào|tới|đến|sang|lên)\s+{_KENH}|^(?:email|mail)\s+cho\s+{_TOI}\b")
_GUI_NHO = re.compile(rf"^\s*gửi\b|\bgửi\s+{_GIUP}\s+{_TOI}\b|\bgửi\b[^,;:.?!]*\s{_GIUP}{_CUOI}|\b{_GIUP}\s+{_TOI}\s+gửi\b"
                      rf"|\bgửi\b.*\bcho\s+{_TOI}\b|^(?:email|mail)\s+cho\b")           # người gửi là trợ lý
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


# ---------- cờ `chi_sang_len_ke_hoach` (19/11/2026, plan private `data/len_lich_chat_2026-11-19/PLAN.md`) ----------
# Lịch gõ tự do đang TẮT (đo không đạt) ⇒ người gõ "lên lịch 2 ngày giúp mình" trong ô chat có lượt nhận câu từ chối khuôn. Hàm thuần dưới chỉ
# nhận lời NHỜ XẾP LỊCH đi Huế; câu HỎI VỀ lịch (lịch lễ hội, lịch diễn, giờ mở cửa, lịch tàu xe), câu hỏi chi phí / "nên đi mấy điểm", câu sửa
# một lịch đã có ⇒ False. Chỉ dùng để thay câu từ chối khuôn (`assistant._noi_that_lam_thay`) ⇒ sót một cách nói lạ thì lượt đó y như cờ tắt.
_SO_NGAY = r"(?:(?:\d+|một|hai|ba|bốn|năm|nửa)\s*ngày|\d\s*n\s*\d\s*đ\b)"
_LICH = r"(?:lịch trình|lịch(?!\s*(?:sử|thiệp|vạn niên))|kế hoạch|hành trình)"
_LAP = r"(?:lên|xếp|sắp xếp|sắp|lập|làm|tạo|thiết kế|vạch|gợi ý|đề xuất|tư vấn)"  # sau bộ dò của người khác: thêm "sắp", "gợi ý / đề xuất / tư vấn"
# "lên lịch …", "xếp giúp mình lịch trình …", "lập cho mình kế hoạch …"
_NHO_LICH = re.compile(rf"\b{_LAP}\s+(?:(?:{_GIUP}|cho)\s+(?:{_TOI}\s+)?)?(?:một\s+|1\s+|cái\s+)?{_LICH}\b")
# câu mở đầu bằng chính cụm lịch + số ngày: "lịch 1 ngày chỉ đi các lăng, xuất phát 8h"
_LICH_N_NGAY = re.compile(rf"^(?:(?:cho\s+)?{_TOI}\s+(?:cần|muốn|xin)?\s*|xin\s+)?(?:một\s+|1\s+)?{_LICH}\s+(?:đi\s+|tham quan\s+|du lịch\s+|chơi\s+)?(?:huế\s+)?{_SO_NGAY}")
# câu kể chuyến đi, không hỏi gì: "mình đi Huế 2 ngày 1 đêm"
_DI_N_NGAY = re.compile(rf"\b(?:đi|tới|đến|ra|vào|ở|chơi|thăm|du lịch|tham quan)\s+(?:chơi\s+)?huế\s+{_SO_NGAY}")
# "…, xếp giúp" ở cuối câu
_XEP_GIUP_CUOI = re.compile(rf"\b(?:xếp|sắp xếp)\s+{_GIUP}(?:\s+{_TOI})?(?:\s+(?:với|nhé|nha|đi|luôn))*\s*[.!]*$")
# "lịch" của thứ khác (không phải lịch đi chơi) · lịch đã có · câu hỏi thông tin quanh việc lập lịch
_LICH_THU_KHAC = re.compile(r"lịch(?:\s+trình)?\s+(?:của\s+)?(?:lễ hội|festival|diễn|biểu diễn|trình diễn|mở cửa|đóng cửa|hoạt động|tàu|xe|bay|chuyến|chạy|khởi hành|"
                            r"chiếu|làm việc|nghỉ|thi|học|tết|sự kiện|ca huế|nhã nhạc)|âm lịch|dương lịch")
_LICH_DA_CO = re.compile(r"lịch(?:\s+trình)?\s+(?:này|đó|kia|vừa|trên|cũ|đang|hiện|hôm nay|của mình|của tôi|của em)|(?:trong|khỏi|vào|ra khỏi)\s+lịch")
# sau bộ dò của người khác (một lần sửa): bỏ "tiền / giá / chi phí / ngân sách" đứng một mình — đó là RÀNG BUỘC của lời nhờ ("… cho nhóm sinh viên ít tiền"),
# câu hỏi chi phí thật luôn có "bao nhiêu / hết / tốn / mấy"; thêm từ hỏi "nào / ai / gì / đâu" ("công ty nào nhận xếp lịch tour …" là hỏi thông tin)
_HOI_QUANH_LICH = re.compile(r"bao nhiêu|\bhết\b|\btốn\b|\bmấy\b|\bcách\b|làm sao|thế nào|ra sao|kinh nghiệm|\bnên\b|\bnào\b|\bai\b|\bgì\b|"
                             r"\bđâu\b|khi nào|bao giờ|tại sao|vì sao")
_CO_HOI = re.compile(r"\?|bao nhiêu|\bmấy\b|\bgì\b|\bnào\b|\bkhông\b|\bko\b|\bk\b|\bchưa\b|\bsao\b|\bđâu\b|bao giờ|\bnên\b|\bđủ\b|\bhết\b|\btốn\b|"
                     r"\bgiá\b|\btiền\b|chi phí|ngân sách")


def nho_xep_lich(cau: str) -> bool:
    """Câu người dùng là lời NHỜ XẾP / LÊN LỊCH đi Huế gõ tự do. Danh sách cho phép hẹp, theo ba dạng: (1) động từ lập + "lịch / kế hoạch / hành
    trình" (kể cả "… được không"); (2) câu KHÔNG có từ hỏi mở đầu bằng "lịch N ngày …" hoặc kể "đi Huế N ngày …"; (3) câu không có từ hỏi kết bằng
    "xếp giúp". Việc bằng chữ (tóm, chép, viết), lịch của thứ khác, lịch đã có, câu hỏi chi phí / cách làm ⇒ False."""
    chu = " ".join((cau or "").casefold().split())
    if not chu or _VIEC_BANG_CHU.search(chu) or _LICH_THU_KHAC.search(chu) or _LICH_DA_CO.search(chu):
        return False
    if _NHO_LICH.search(chu):
        return not _HOI_QUANH_LICH.search(chu)
    if _CO_HOI.search(chu):
        return False
    return bool(_LICH_N_NGAY.search(chu) or _DI_N_NGAY.search(chu) or _XEP_GIUP_CUOI.search(chu))

