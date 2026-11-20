"""Cờ `len_lich_dan_trang` (20/11/2026) — người dùng gõ trong ô chat một câu NHỜ LẬP LỊCH NHIỀU NGÀY ("lên lịch giúp mình 2 ngày ở Huế") ⇒ code nối
vào dòng ghi chú một câu trỏ sang trang Lên kế hoạch.

Vì sao: đo 20/11 (hai lượt thật qua giao diện) — câu kiểu này được trả lời bằng một lịch CHỮ chung chung lấy từ bài lịch trình mẫu trong kho, không
nhắc tới trang Lên kế hoạch (lịch theo giờ từng điểm, bản đồ, sửa bằng lời, tải file). Bản này KHÔNG đổi câu trả lời, không tự lập lịch trong ô chat.
Hàm thuần: chỉ đọc câu người dùng của lượt đó; không model, không kho. Khuôn HẸP — sót một cách nói lạ ⇒ lượt đó y như khi cờ tắt. Chỉ nhận tiếng
Việt CÓ DẤU (quyết định sản phẩm sẵn có). Cùng kiểu với `llm/danh_sach.py`.
"""
import re

TEN_TRANG = "trang Lên kế hoạch"  # giao diện (`chat.jsx`) đổi đúng cụm chữ này trong dòng ghi chú thành link `#/len-ke-hoach`
CAU_DAN_TRANG = f"Muốn lịch có giờ từng điểm, bản đồ và sửa được bằng lời, bạn mở {TEN_TRANG}."

_NHO = r"(?:lên|xếp|sắp xếp|sắp|lập|soạn|tạo|làm|thiết kế|vạch|gợi ý|tư vấn|xin|cần)"  # "xin", "cần": bộ dò mù của phiên C 20/11 ("cho mình xin lịch trình…")
# "lịch" theo nghĩa lịch đi chơi: không phải lịch diễn / lịch mở cửa / lịch tàu xe / lịch tổ chức lễ hội
_LICH = r"(?:lịch trình|kế hoạch|lịch)(?!\s+(?:diễn|chiếu|mở|đóng|tàu|xe|bay|chạy|tổ chức|thi đấu|làm việc|sự kiện|lễ|âm|dương|học|nhắc|chi tiêu|tài chính))"
# Giữa động từ nhờ và chữ "lịch" chỉ nhận từ ĐỆM (review của phiên C 20/11: "vài từ bất kỳ" làm 10 / 14 câu kiểu "gợi ý quán ăn theo lịch trình 2 ngày của
# mình" bị nhận — động từ và "lịch" không thuộc về nhau)
_DEM = r"(?:giúp|cho|hộ|dùm|giùm|với|mình|tôi|em|anh|chị|tớ|tụi|bọn|nhà|gia đình|một|bản|cái)"
_MAU = re.compile(rf"(?<!\w){_NHO}\s+(?:{_DEM}\s+){{0,4}}{_LICH}(?!\w)", re.I)
_SO_NGAY = re.compile(r"(?<!\w)(?:\d{1,2}|một|hai|ba|bốn|năm|sáu|bảy)\s+ngày(?!\w)|(?<!\w)\d\s?n\s?\d\s?đ(?!\w)", re.I)  # cả kiểu gõ tắt "2N1Đ"
# đang nói về một lịch ĐÃ có (sửa / hỏi về nó) hoặc hỏi giá ⇒ không phải nhờ lập lịch mới
_KHONG = re.compile(r"(?<!\w)lịch\s+(?:này|đó|trên|vừa|đã|cũ)(?!\w)|(?<!\w)(?:tự|đã)\s+(?:lên|xếp|lập|soạn|làm)(?!\w)|(?<!\w)(?:ổn|hợp lý)\s+không(?!\w)|(?<!\w)(?:bao nhiêu tiền|giá bao nhiêu|hết bao nhiêu|tốn bao nhiêu)(?!\w)", re.I)


def nho_len_lich(cau: str) -> bool:
    """True khi câu gõ nhờ lập một lịch đi chơi có số ngày. Chỉ đọc chữ của lượt này."""
    chu = " ".join((cau or "").split())
    return bool(_MAU.search(chu)) and bool(_SO_NGAY.search(chu)) and not _KHONG.search(chu)
