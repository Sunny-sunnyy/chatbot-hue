"""Luật khẩn cấp bằng code (Phase 9 B1 D1, D2; plan `docs/superpowers/plans/2026-11-02-phase-9-b1-plan.md`).

Câu người dùng **đang** gặp nguy ⇒ trả đúng nguyên văn câu soạn sẵn Bản 1 (`data/phase_9/cau_khan_cap_soan_san.md`, A chốt; số kiểm ở
`data/phase_9/so_khan_cap.md` — kiểm lại trước bảo vệ / deploy vì Kế hoạch 642 có thể gộp số về 113), **không gọi model nào**.
Mẫu viết + chỉnh chỉ trên phần đã thấy (10 câu C122 + 4 câu khẩn cấp của bộ tuyến đã thấy; không được khớp 208 câu hồi quy + câu thường của
bộ tuyến); phần kín chỉ đo một lần sau khi khoá. Chữ "khẩn cấp" một mình **không** đủ (ca lái tuyến).
"""
import re
import unicodedata

EMERGENCY_ANSWER = (
    # Dòng mở PA1 (C162 `chu_moi_phuong_an.md` `a0bc71cbfaff`, User chọn 04/11): phủ cả người **vừa** gặp chuyện (bị cướp…) — tuyến khan_cap từ B143.
    "Nếu bạn hoặc người bên cạnh đang gặp nguy hiểm hoặc vừa gặp chuyện (bị cướp, tai nạn, cháy, ốm nặng), hãy gọi ngay số khẩn cấp (miễn phí):\n"
    "113 Công an · 114 Cháy, cứu nạn cứu hộ · 115 Cấp cứu y tế · 112 Thiên tai, lũ lụt.\n"
    "Khi gọi, nói rõ bạn đang ở đâu và chuyện gì đang xảy ra.\n"
    "Mình là trợ lý thông tin du lịch, không gọi hộ hay điều người tới giúp được.\n"
    "Emergency in Vietnam (free): 113 Police · 114 Fire & rescue · 115 Ambulance · 112 Natural disasters."
)

# Dấu thanh đặt hai kiểu (hoà / hòa, doạ / dọa…) ⇒ mẫu viết bằng lớp ký tự.
_OA = "(?:oạ|ọa)"
_OA_HOI = "(?:oả|ỏa)"

# Mỗi mẫu là một dấu hiệu "đang gặp nguy ngay lúc này" (luật phân xử 1 của bộ tuyến). Không dùng từ đơn dễ trùng câu thường
# ("cháy" — cơm cháy; "lũ" — mùa lũ; "cấp cứu" — hỏi bệnh viện; "cứu với" — cách nói quá).
_PATTERNS = (
    r"bốc cháy", rf"h{_OA_HOI} hoạn", r"(?:đang|bị) cháy\b", r"cháy (?:lớn|to|dữ)",
    r"(?:vừa|đang|mới) (?:bị )?(?:đuối nước|chết đuối)",  # "đuối nước" / "dễ bị đuối nước" một mình: câu hỏi an toàn sông nước (bộ an toàn)
    r"không thở(?: được)?\b", r"ngừng thở", r"tắt thở",
    r"ngất xỉu", r"bất tỉnh", r"co giật", r"đột quỵ", r"méo miệng", r"không cử động được",
    r"chảy máu (?:nhiều|không ngừng|rất nhiều)",
    r"bị (?:xe(?: máy| ô tô)?|ô tô|xe hơi|xe tải) (?:tông|đâm|húc)", r"\bbị tông\b", r"(?:vừa|bị|gặp|đang) tai nạn",
    r"bị nôn ói", r"nôn ói", r"đau bụng dữ dội", r"bị ngộ độc",
    r"rắn cắn",
    r"bị giật (?:túi|ví|điện thoại|đồ|balo)", r"bị cướp", r"bị móc túi",
    rf"đe d{_OA}", r"bị (?:đánh|tấn công|hành hung)",
    r"\b(?:con|bé|cháu|em bé|trẻ|đứa nhỏ|thằng bé|con bé)\b[^.?!]{0,40}\bbị lạc\b", r"lạc mất (?:con|bé|cháu)",
    r"bị hóc", r"hóc (?:hạt|xương|dị vật)",
    r"(?:nước )?lũ (?:đang )?dâng", r"nước (?:đang )?dâng (?:vào|lên|cao)", r"sạt lở (?:đất )?(?:đang|vừa)",
)
_EMERGENCY = re.compile("|".join(f"(?:{p})" for p in _PATTERNS))


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).lower().split())


def is_emergency(text: str) -> bool:
    """Câu có dấu hiệu đang gặp nguy (tất định, không gọi model)."""
    return _EMERGENCY.search(normalize(text)) is not None
