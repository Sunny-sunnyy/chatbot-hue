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

# Câu xin liệt kê lại — luật HẸP có chủ ý: bắt nhầm (câu hỏi về MỘT nơi mất dòng ghi chú ⇒ model lại nói về nơi khác) nặng hơn bỏ sót (danh sách có
# lúc thiếu, như trước bản sửa). Câu được nhận khi có một cụm xin danh sách đủ VÀ cả câu đúng MỘT khuôn:
#   [lời lịch sự] <lời xin kể — BẮT BUỘC> [tất cả / toàn bộ] các / những / mấy / mọi <ĐÚNG MỘT loại nơi> [cụm trỏ lại] [lời lịch sự]
# Bản đầu xét "mọi từ thuộc bộ cho phép" đã bị bộ dò thêm bắt (review 20/11): túi từ không thấy cấu trúc, nên "liệt kê các điểm tham quan lăng đó",
# "nêu đủ tên quán vừa gợi ý", "tất cả các điểm đó có cho tham quan không" đều lọt. Khuôn buộc dấu số nhiều đứng NGAY trước loại nơi, chỉ một loại
# nơi, và sau cụm trỏ lại chỉ còn lời lịch sự. Lời xin kể bắt buộc vì "đi", "được không" ở cuối cũng là câu hỏi thật ("tất cả mấy quán đó đi được không"). Sửa khuôn ⇒ chạy lại hai bộ dò của việc này.
CUM_XIN_DU = ("kể hết", "kể đủ", "kể đầy đủ", "nêu hết", "nêu đủ", "nêu đầy đủ", "liệt kê", "danh sách", "tất cả", "toàn bộ",
              "kể lại các", "kể lại những", "nêu lại các", "nêu lại những", "nhắc lại các", "nhắc lại những",
              "kể tên các", "kể tên những", "nêu tên các", "nêu tên những")
_LICH_SU_DAU = r"(?:bạn|hãy|làm ơn|vui lòng|nhờ bạn|xin|có thể|cho (?:mình|tôi|em|xin)|giúp (?:mình|tôi|em))"
_XIN_KE = (r"(?:(?:kể|nêu|liệt kê|nhắc|viết)(?: (?:lại|tên|hết|đủ|đầy đủ|ra))*(?: (?:full )?danh sách(?: (?:đầy đủ|đủ))?)?"
           r"|(?:full )?danh sách(?: (?:đầy đủ|đủ))?|tên)")
_LOAI_NOI = (r"(?:chỗ|nơi|địa điểm|điểm tham quan|điểm du lịch|điểm đến|điểm|quán ăn|quán cà phê|quán cafe|quán|nhà hàng|lăng tẩm|lăng vua|lăng|chùa"
             r"|di tích|đền|làng nghề|làng|chợ|bãi biển|cung điện)")
_TRO_LAI = (r"(?:đó|này|ấy|kia|ở trên|vừa rồi|lúc nãy|trong bài(?: (?:đó|này|ấy))?|trong danh sách"
            r"|(?:bạn )?(?:vừa|mới|đã) (?:nêu|nói|nhắc|kể|gợi ý|đề cập))")
_LICH_SU_CUOI = r"(?:giúp (?:mình|tôi|em)|với|nhé|nha|đi|ạ|được không|xem nào|ra|luôn)"
_KHUON_LIET_KE_LAI = re.compile(rf"(?:{_LICH_SU_DAU} )*(?:{_XIN_KE} )(?:(?:tất cả|toàn bộ) )?(?:các|những|mấy|mọi) {_LOAI_NOI}"
                                rf"(?: {_TRO_LAI}){{0,2}}(?: {_LICH_SU_CUOI})*")


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
    if re.search(r"[.?!;…]\s*\w", cau or ""):  # dấu ngắt câu ở GIỮA = có thêm một câu nữa ("Liệt kê các chỗ đó. Đi được không?" — soát khác hãng 20/11)
        return False
    chu = " ".join(re.sub(r"[^\w\s]", " ", unicodedata.normalize("NFC", cau or "").lower()).split())
    if not any(re.search(rf"(?<!\w){cum}(?!\w)", chu) for cum in CUM_XIN_DU):
        return False
    return _KHUON_LIET_KE_LAI.fullmatch(chu) is not None


def lich_su_cho_luot(lich_su: Sequence, cau: str) -> tuple:
    """Lịch sử gửi model ở lượt có câu gõ `cau`: câu xin liệt kê lại ⇒ các dòng ghi chú tên nơi thành chuỗi rỗng (như cờ tắt); câu khác ⇒ nguyên.
    Lịch sử không có dòng ghi chú (cờ tắt, hoặc nhớ cả câu trả lời) ⇒ luôn trả đúng nội dung cũ."""
    if not la_cau_xin_liet_ke_lai(cau):
        return tuple(lich_su)
    return tuple((hoi, "" if dap.startswith(TIEN_TO_GHI_CHU) else dap) for hoi, dap in lich_su)
