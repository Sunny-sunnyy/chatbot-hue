"""Cờ `danh_sach_noi_that` (20/11/2026) — người dùng XIN MỘT DANH SÁCH (những / các … nào, kể hết, liệt kê) ⇒ code nối một dòng nói thật vào dòng
ghi chú: danh sách chỉ gồm các bài tìm được, có thể chưa đủ.

Vì sao: trợ lý tìm theo đoạn văn, không lọc cả kho theo một đặc điểm ⇒ câu "những quán nào có <đặc điểm>" thường chỉ ra một phần danh sách mà không
nói là có thể thiếu (bộ câu mẫu 6 / 18 câu dạng này; hỏi tiếp "kể hết các nơi vừa nêu" thiếu 5 / 6 lần đo 20/11). Bản này KHÔNG làm danh sách đủ hơn.
Hàm thuần: chỉ đọc câu người dùng của lượt đó; không model, không kho. Danh sách CHO PHÉP hẹp — sót một cách nói lạ ⇒ lượt đó y như khi cờ tắt;
câu xin MỘT gợi ý ("quán nào ngon") cố ý KHÔNG nhận. Chỉ nhận tiếng Việt CÓ DẤU (quyết định sản phẩm sẵn có).
"""
import re

CAU_DANH_SACH = "Danh sách trên chỉ gồm những nơi có trong các bài tìm được, nên có thể chưa đủ."

# Thứ người dùng xin kể: nơi chốn / món / sự kiện có bài trong kho. Từ chung ("thông tin", "lưu ý", "bước") cố ý không có.
_LOAI = (r"(?:quán|nhà hàng|tiệm|hàng|chỗ|nơi|điểm|địa điểm|địa chỉ|lăng|lăng tẩm|chùa|đền|miếu|nhà vườn|làng|làng nghề|chợ|bãi biển|bãi tắm|bãi|biển|"
         r"khách sạn|homestay|resort|món|đặc sản|lễ hội|bảo tàng|di tích|cà phê|cafe)")
_GIUA = r"(?:[^\s,;:.?!]+\s+){0,6}?"  # vài từ chen giữa, không vắt qua dấu câu
_MAU = re.compile(
    rf"(?<!\w)(?:những|các)\s+{_LOAI}\s+{_GIUA}(?:nào|gì)(?!\w)"                      # "những quán nào mở sớm", "các lăng vua nào mở cửa"
    rf"|(?<!\w)có\s+(?:những|các)\s+{_LOAI}\s+{_GIUA}(?:nào|gì)(?!\w)"
    rf"|(?<!\w)(?:kể hết|kể tên|kể ra|liệt kê|danh sách|tất cả)\s+(?:[^\s,;:.?!]+\s+){{0,3}}?{_LOAI}(?!\w)"  # "kể hết các lăng", "liệt kê quán chay"
    rf"|(?<!\w)(?:những|các)\s+{_LOAI}\s+{_GIUA}(?:kể hết|kể tên|liệt kê)(?!\w)", re.I)
# Hỏi so sánh / chọn một trong vài thứ đã nêu, hoặc hỏi về giá / giờ của các nơi ⇒ không phải xin danh sách
_KHONG = re.compile(r"(?<!\w)(?:nào|gì)\s+(?:hơn|nhất)(?!\w)|(?<!\w)(?:hay|hoặc)\s+(?:là\s+)?\S+\s*\?*$|(?<!\w)trong\s+(?:hai|ba|2|3)\s"
                    r"|(?<!\w)trong\s+(?:số\s+)?(?:các|những|mấy)\s", re.I)  # "trong các quán vừa nêu, quán nào …": chọn MỘT (bộ dò mù của E 20/11)


def xin_danh_sach(cau: str) -> bool:
    """True khi câu gõ khớp khuôn xin danh sách. Chỉ đọc chữ của lượt này."""
    chu = " ".join((cau or "").split())
    return bool(_MAU.search(chu)) and not _KHONG.search(chu)


def hoi_ve_mot_noi(cau: str, ten_bai: list[str]) -> bool:
    """Câu gõ có TÊN BÀI của một nguồn đã trích ("các món ở <tên quán> gồm những gì") ⇒ câu hỏi về một nơi, không phải danh sách nơi."""
    chu = " ".join((cau or "").casefold().split())
    return any(len(t) >= 4 and t in chu for t in (" ".join(x.casefold().split()) for x in ten_bai))
