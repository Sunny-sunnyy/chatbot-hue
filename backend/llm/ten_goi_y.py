"""Cờ `nho_ten_goi_y` (19/11/2026, plan private `data/hoi_tiep_goi_y_2026-11-19/PLAN.md`) — nhớ TÊN nơi trợ lý vừa gợi ý.

Vì sao: lịch sử chỉ nhớ câu hỏi (`nho_cau_tra_loi: false` — 03/11 nhớ cả câu trả lời làm lượt hỏi tiếp mượn đoạn của đối tượng khác). Hệ quả đo
19/11: người dùng hỏi tiếp "cho địa chỉ quán đó" thì model không biết quán nào vừa được gợi ý, tự tìm lại kho và trả địa chỉ quán khác.
Cách làm: CODE (không model) lấy tên bài của các nguồn câu trả lời ĐÃ TRÍCH là bài riêng của một nơi, đưa vào chỗ tin trợ lý của lịch sử dưới dạng một dòng ghi
chú (không đánh số, không gọi là "đã gợi ý" — xem `ghi_chu_goi_y`). Không lấy chữ model viết, không lấy mục web, không lấy lịch (chữ lịch có tên quán từ bản đồ mở).
Nơi chỉ được nêu qua bài tổng hợp (cẩm nang) KHÔNG được nhớ; câu hỏi tiếp kiểu "quán thứ hai / chỗ đầu tiên" KHÔNG được dòng này giải — giới hạn
đã nhận của bản đầu.

Sửa nhỏ 20/11/2026 (plan private `data/kich_ban_pho_thong_2026-11-19/viec_2_sua_nho/PLAN.md`): dòng ghi chú chỉ là MỘT PHẦN các nơi đã nêu, nhưng khi
người dùng hỏi tiếp "kể hết các chỗ vừa nêu" model có lúc coi nó là danh sách đủ và chỉ kể mấy tên đó (đo 19/11: một lượt kể 3 / 8). Nên lượt mà CÂU GÕ
là câu xin liệt kê lại thì không nhận dòng ghi chú (`lich_su_cho_luot`) — lịch sử của đúng lượt đó về như khi cờ tắt; ghi chú vẫn nằm trong kho lịch sử cho lượt sau.
"""
import re
import unicodedata
from collections.abc import Sequence

from llm.citations import CITATION_PATTERN

# Thư mục kho mà mỗi bài nói về MỘT nơi (quán ăn, quán cà phê, điểm đến, di tích). Không lấy: bài tổng hợp, món ăn, lễ hội, nghệ thuật, vé, dịch vụ.
# Giới hạn đã biết (review E 19/11): `heritages/heritage/` có hai bài tổng hợp nhiều nơi không mang chữ "guide" ⇒ vẫn được nhớ như một nơi (tên có thật).
# Tên bài đi thẳng vào dòng ghi chú, không lọc ký tự: kho hôm nay không có tên bài chứa `[`, `]`, `;` — thêm bài có ký tự đó thì xem lại khuôn dòng.
THU_MUC_NOI = ("foods/restaurants/", "foods/cafes/", "travel/places/", "heritages/heritage/")
TOI_DA = 5
TIEN_TO_GHI_CHU = "[Ghi chú hệ thống — câu trả lời lượt này có trích bài kho của các nơi: "

# Câu xin liệt kê lại — luật HẸP có chủ ý: bắt nhầm (câu "địa chỉ các quán đó" mất dòng ghi chú ⇒ model lại nói về nơi khác) nặng hơn bỏ sót
# (danh sách có lúc thiếu, như trước bản sửa). Câu được nhận khi có một cụm xin danh sách đủ VÀ, sau khi bỏ các cụm trỏ lại, MỌI từ còn lại thuộc
# `TU_CHO_PHEP`. Một từ ngoài bộ (địa chỉ, giá, thứ hai, món, "trong lăng đó"…) ⇒ không nhận. Thêm từ vào ba bộ dưới ⇒ chạy lại bộ dò của việc này.
CUM_XIN_DU = ("kể hết", "kể đủ", "kể đầy đủ", "nêu hết", "nêu đủ", "nêu đầy đủ", "liệt kê", "danh sách", "tất cả", "toàn bộ",
              "kể lại các", "kể lại những", "nêu lại các", "nêu lại những", "nhắc lại các", "nhắc lại những",
              "kể tên các", "kể tên những", "nêu tên các", "nêu tên những")
# Cụm trỏ lại câu trả lời trước. "trong" / "ở" chỉ được nhận bên trong các cụm này: "trong lăng đó", "ở quán đó" là hỏi về MỘT nơi.
CUM_TRO_LAI = ("trong bài đó", "trong bài này", "trong bài ấy", "trong bài", "trong câu trả lời", "trong câu đó", "trong danh sách",
               "trong đó", "ở trên", "phía trên", "bên trên", "ở câu trước", "lúc nãy", "khi nãy", "hồi nãy", "vừa rồi")
TU_CHO_PHEP = frozenset((
    "kể hết đủ đầy lại nêu nhắc liệt kê tên danh sách tất cả toàn bộ "                                      # chữ của các cụm xin danh sách đủ
    "giúp mình tôi tớ em anh chị bạn với nhé nha nhỉ đi ạ cho xem hãy làm ơn vui lòng được không có thể thử coi ra luôn hộ dùm giùm xin nhờ biết "
    "muốn viết full còn nữa nào sót thiếu "                                                                 # thêm sau lần chạy đầu bộ dò (20/11)
    "đó này ấy kia vừa nói gợi ý đã mới nãy mà đến tới đề cập "                                             # trỏ lại
    "các những mọi mấy chỗ nơi điểm địa tham quan quán ăn uống cà phê cafe nhà hàng lăng tẩm vua chùa di tích đền miếu cung điện làng nghề chợ bãi biển "
    "du lịch chơi mục cái"                                                                                  # danh từ chỉ nơi
).split())
TU_TRO_MOT, TU_SO_NHIEU = frozenset("đó này ấy kia".split()), frozenset("các những mấy mọi".split())
_CUM_TRO_LAI_RE = re.compile(r"(?<!\w)(?:" + "|".join(sorted(CUM_TRO_LAI, key=len, reverse=True)) + r")(?!\w)")


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
    return (TIEN_TO_GHI_CHU + "; ".join(ten)
            + ". Danh sách có thể thiếu nơi đã được nêu và không theo thứ tự trong câu trả lời.]")


def la_cau_xin_liet_ke_lai(cau: str) -> bool:
    """Câu gõ CHỈ xin kể lại / kể đủ các nơi vừa nêu ("Kể đủ các chùa trong bài đó giúp tôi")? Câu ghép hay câu hỏi thêm điều gì về nơi ⇒ False."""
    chu = " ".join(re.sub(r"[^\w\s]", " ", unicodedata.normalize("NFC", cau or "").lower()).split())
    if not any(re.search(rf"(?<!\w){cum}(?!\w)", chu) for cum in CUM_XIN_DU):
        return False
    tu = _CUM_TRO_LAI_RE.sub(" ", chu).split()
    # "quán đó / lăng này" không có "các / những / mấy / mọi" đứng trước = trỏ MỘT nơi ("nêu đủ tên quán đó") ⇒ không nhận
    for i, t in enumerate(tu):
        if t in TU_TRO_MOT and not TU_SO_NHIEU.intersection(tu[:i]):
            return False
    return all(t in TU_CHO_PHEP for t in tu)


def lich_su_cho_luot(lich_su: Sequence, cau: str) -> tuple:
    """Lịch sử gửi model ở lượt có câu gõ `cau`: câu xin liệt kê lại ⇒ các dòng ghi chú tên nơi thành chuỗi rỗng (như cờ tắt); câu khác ⇒ nguyên.
    Lịch sử không có dòng ghi chú (cờ tắt, hoặc nhớ cả câu trả lời) ⇒ luôn trả đúng nội dung cũ."""
    if not la_cau_xin_liet_ke_lai(cau):
        return tuple(lich_su)
    return tuple((hoi, "" if dap.startswith(TIEN_TO_GHI_CHU) else dap) for hoi, dap in lich_su)
