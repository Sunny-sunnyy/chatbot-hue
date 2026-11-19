"""Cờ `nho_ten_goi_y` (19/11/2026, plan private `data/hoi_tiep_goi_y_2026-11-19/PLAN.md`) — nhớ TÊN nơi trợ lý vừa gợi ý.

Vì sao: lịch sử chỉ nhớ câu hỏi (`nho_cau_tra_loi: false` — 03/11 nhớ cả câu trả lời làm lượt hỏi tiếp mượn đoạn của đối tượng khác). Hệ quả đo
19/11: người dùng hỏi tiếp "cho địa chỉ quán đó" thì model không biết quán nào vừa được gợi ý, tự tìm lại kho và trả địa chỉ quán khác.
Cách làm: CODE (không model) lấy tên bài của các nguồn câu trả lời ĐÃ TRÍCH là bài riêng của một nơi, đưa vào chỗ tin trợ lý của lịch sử dưới dạng một dòng ghi
chú (không đánh số, không gọi là "đã gợi ý" — xem `ghi_chu_goi_y`). Không lấy chữ model viết, không lấy mục web, không lấy lịch (chữ lịch có tên quán từ bản đồ mở).
Nơi chỉ được nêu qua bài tổng hợp (cẩm nang) KHÔNG được nhớ; câu hỏi tiếp kiểu "quán thứ hai / chỗ đầu tiên" KHÔNG được dòng này giải — giới hạn
đã nhận của bản đầu.
"""
from collections.abc import Sequence

from llm.citations import CITATION_PATTERN

# Thư mục kho mà mỗi bài nói về MỘT nơi (quán ăn, quán cà phê, điểm đến, di tích). Không lấy: bài tổng hợp, món ăn, lễ hội, nghệ thuật, vé, dịch vụ.
# Giới hạn đã biết (review E 19/11): `heritages/heritage/` có hai bài tổng hợp nhiều nơi không mang chữ "guide" ⇒ vẫn được nhớ như một nơi (tên có thật).
# Tên bài đi thẳng vào dòng ghi chú, không lọc ký tự: kho hôm nay không có tên bài chứa `[`, `]`, `;` — thêm bài có ký tự đó thì xem lại khuôn dòng.
THU_MUC_NOI = ("foods/restaurants/", "foods/cafes/", "travel/places/", "heritages/heritage/")
TOI_DA = 5


def _la_bai_mot_noi(source: str) -> bool:
    return source.startswith(THU_MUC_NOI) and "guide" not in source.rsplit("/", 1)[-1].lower()


def ten_noi_da_trich(answer: str, cited: Sequence) -> tuple[str, ...]:
    """Tên bài (≤ `TOI_DA`) của các nguồn đã trích là bài riêng của một nơi, theo thứ tự mã trích xuất hiện lần đầu trong câu trả lời; mỗi bài một lần."""
    theo_ma = {src.id: src for src in cited}
    ten, da_co = [], set()
    for ma in CITATION_PATTERN.findall(answer or ""):
        src = theo_ma.get(int(ma))
        if src is not None and src.source not in da_co and _la_bai_mot_noi(src.source):
            da_co.add(src.source)
            ten.append(src.title)
    return tuple(ten[:TOI_DA])


def ghi_chu_goi_y(trace) -> str:
    """Dòng ghi chú cho lịch sử của một lượt ĐÃ XONG, hoặc "" khi lượt không được nhớ tên: lượt lịch / biểu mẫu, lượt kết thúc bằng câu cố định
    (từ chối, ngoài phạm vi, hỏi lại…), lượt không trích nguồn nào hay không trích bài riêng của nơi nào."""
    if trace.bieu_mau or trace.lich is not None or trace.lich_v2 is not None or trace.fixed_outcome is not None or not trace.cited:
        return ""
    ten = ten_noi_da_trich(trace.answer or "", trace.cited)
    if not ten:
        return ""
    # Chỉ nói điều code biết chắc (sửa 19/11 trước lượt đo, sau khi người soạn bộ đích thấy hai cơ chế trên dữ liệu thật): bài riêng được TRÍCH,
    # không phải "đã gợi ý" (có bài được trích chỉ để nêu vị trí / so sánh), không đánh số (nơi được nêu qua bài tổng hợp không có trong danh sách
    # ⇒ số thứ tự lệch với thứ tự người dùng thấy, "quán thứ hai" sẽ trỏ nhầm nơi).
    return ("[Ghi chú hệ thống — câu trả lời lượt này có trích bài kho của các nơi: " + "; ".join(ten)
            + ". Danh sách có thể thiếu nơi đã được nêu và không theo thứ tự trong câu trả lời.]")
