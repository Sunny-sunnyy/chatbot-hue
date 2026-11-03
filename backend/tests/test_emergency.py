"""Luật khẩn cấp Phase 9 B1 (plan D2) — logic thuần, câu tự viết (không phải câu bộ đo). Bằng chứng trên bộ đo đã thấy + 208 câu hồi quy:
`data/phase_9/b1/tools/emergency_check.py`; phần kín do C chạy sau khi khoá."""
from llm.emergency import EMERGENCY_ANSWER, is_emergency


def test_present_danger_is_emergency():
    for text in ("Nhà nghỉ bên cạnh đang bốc cháy, khói đầy hành lang", "Bạn tôi vừa bị đuối nước ở sông",
                 "Có người ngất xỉu giữa sân", "Tôi bị giật điện thoại ngoài chợ", "Con tôi đi chơi bị lạc ở bến xe rồi",
                 "Bà tôi đột quỵ, méo miệng", "Thằng bé bị hóc kẹo"):
        assert is_emergency(text), text


def test_ordinary_questions_with_risky_words_are_not():
    for text in ("Cơm cháy chà bông ở Huế mua ở đâu?", "Mùa lũ ở Huế thường vào tháng mấy?", "KHẨN CẤP!!! quán chè nào ngon?",
                 "Tắm biển Thuận An có dễ bị đuối nước không?", "Bệnh viện cấp cứu gần Đại Nội là bệnh viện nào?",
                 "Huế có nhiều tai nạn giao thông không?", "Chào bạn"):
        assert not is_emergency(text), text


def test_answer_is_exact_approved_text_with_four_numbers():
    lines = EMERGENCY_ANSWER.split("\n")
    assert len(lines) == 5 and lines[1] == "113 Công an · 114 Cháy, cứu nạn cứu hộ · 115 Cấp cứu y tế · 112 Thiên tai, lũ lụt."
