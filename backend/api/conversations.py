"""Nhớ hội thoại trong một cuộc trò chuyện (Phase 9 B3, plan `docs/superpowers/plans/2026-11-03-phase-9-b3-plan.md` D1, D2, D4).

Kho trong RAM của app: `conversation_id` (mã ngẫu nhiên, nằm trong cookie HttpOnly) → các lượt đã xong. Server giữ lịch sử — trình duyệt
không gửi lại "trợ lý đã nói…" (chỗ cài lệnh, spec §3). Hết hạn 30 phút từ lượt cuối; trần 500 cuộc; mỗi cuộc giữ 3 lượt gần nhất và
≤ 1.500 token lịch sử (bỏ lượt cũ nhất trước, không tóm tắt). Không ghi đĩa, không log chữ / mã cuộc. Khởi động lại server ⇒ mất hết.
Không khoá: hai yêu cầu cùng cuộc chạy song song thì lượt xong sau ghi sau (một người dùng — spec §7).
"""
import re
import secrets
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Callable

from llm.citations import CITATION_PATTERN

TTL_SECONDS = 30 * 60
MAX_CONVERSATIONS = 500
MAX_TURNS = 3
_SPACE_BEFORE_PUNCT = re.compile(r"\s+([.,;:!?])")
# Cờ `nho_cau_tra_loi` nghĩa MỚI (20/11/2026, plan `report_agent/2026-11-20/b_nho_cau_tra_loi_plan.md`): lịch sử mang câu trả lời của lượt LIỀN TRƯỚC
# (đã bỏ mã trích dẫn, cắt ngắn) sau một dòng nhãn do code viết — để hiểu "quán thứ hai bạn vừa nói", "chia ra mỗi người". Nhãn nằm trong chính ô
# lịch sử nên lời dặn hệ thống không đổi (lời dặn lịch sử sẵn có đã buộc mỗi nhận định lấy từ Bằng chứng của lượt này).
NHAN_LOI_TRUOC = "[Lời trợ lý ở lượt trước — chỉ để hiểu câu hỏi tiếp; KHÔNG phải nguồn, không được trích hay coi là bằng chứng]"
# ký tự; dài hơn ⇒ cắt đuôi. 20/11 đặt 1.200 (luna trả lời ngắn); 21/11 model viết là Sonnet: 2 / 7 câu trả lời của lượt tự kiểm dài hơn 1.200 (dài nhất
# cả ngày 2.229) ⇒ nâng lên 4.000 để mục cuối một danh sách không bị mất; vẫn giữ MỘT trần để bộ bẫy "mượn nhầm đoạn" đọc được trên lượng chữ có giới hạn
CAT_LOI_TRUOC = 4000


def loi_luot_truoc(answer: str) -> str:
    """Ô lịch sử của lượt LIỀN TRƯỚC khi nhớ câu trả lời: nhãn + chữ đã bỏ mã trích dẫn, cắt ở `CAT_LOI_TRUOC`. Không có chữ ⇒ ""."""
    text = stored_answer(answer or "")
    if not text:
        return ""
    if len(text) > CAT_LOI_TRUOC:
        text = text[:CAT_LOI_TRUOC].rstrip() + " …"
    return f"{NHAN_LOI_TRUOC}\n{text}"


def stored_answer(answer: str) -> str:
    """Câu trả lời đem vào lịch sử: bỏ mã trích dẫn `[n]` / `[Nguồn n]` — số nguồn đánh lại mỗi lượt, mã cũ làm model trích nhầm sổ nguồn
    lượt mới (D2). Mục "Từ web" (B6 D7) không cần cắt ở đây: chữ web nằm riêng ở `trace.web`, không bao giờ vào câu trả lời được nhớ."""
    text = CITATION_PATTERN.sub("", answer)
    return _SPACE_BEFORE_PUNCT.sub(r"\1", re.sub(r"[ \t]{2,}", " ", text)).strip()


# Tên mục `trace.tools` của các nguồn / công cụ ĐỔI THEO GIỜ hoặc theo người: dự báo, ngày - lịch âm (công cụ và bản code tính sẵn), sự kiện theo ngày, khoảng
# cách (công cụ và bản tính sẵn), lịch đã lưu của cuộc. Lượt có một trong số này không được giữ đáp. `tim_kho`, `tra_web` (chữ web không nằm trong câu trả lời),
# `liet_ke_bai` (danh sách — đúng thứ người dùng hay trỏ ngược bằng thứ tự) thì giữ.
CONG_CU_KHONG_NHO_DAP = frozenset({"thoi_tiet", "ngay_lich", "lich_san", "su_kien_san", "khoang_cach", "khoang_cach_san", "lich_dang_co"})


# Lượt SỬA lịch không giữ đáp (`dap_duoc_nho`: chữ thẻ lịch có tên quán lấy từ bản đồ mở). Hệ quả đo 23/11/2026: lượt kế thấy câu LỆNH với ô đáp rỗng cạnh
# lịch ĐÃ sửa ⇒ model áp lệnh ấy thêm một lần trong đầu ("bỏ điểm đầu tiên của ngày 2" rồi "ngày 2 giờ còn những điểm nào?" — kể sai điểm đã bỏ, cãi thẻ
# lịch: 2 / 3 lần trên model đang chạy, 1 / 1 trên model cũ). Ô lịch sử của lượt sửa nay mang ĐÚNG các dòng do CODE viết ở đầu thẻ lịch
# (`sua_lich_v2.thay_doi` — "Đã bỏ X.", "Không đổi được: …", "Chưa làm: …"; tên điểm lấy từ bảng điểm): không chữ model, không chữ thẻ, không tên quán.
GHI_CHU_SUA_DAU = ("[Ghi chú hệ thống — lệnh sửa lịch ở lượt này đã được xử lý xong, lịch hiện có là lịch SAU lệnh này; không áp lại lệnh. "
                   "Kết quả đã báo cho người dùng: ")


def ghi_chu_sua_lich(trace) -> str:
    """Dòng ghi chú cho ô lịch sử của một lượt sửa lịch đã xong, hoặc "" khi lượt không phải lượt sửa (`trace.sua_dong` rỗng)."""
    dong = getattr(trace, "sua_dong", ())
    return f"{GHI_CHU_SUA_DAU}{' '.join(dong)}]" if dong else ""


def dap_duoc_nho(trace, outcome: str | None, *, mo_cho_cuoc_co_lich: bool = False) -> bool:
    """Lượt này có được giữ câu trả lời cho lượt kế không (`chi_dap_lien_truoc`): chỉ lượt hỏi đáp thường trả lời được. KHÔNG giữ: câu cố định (từ chối,
    ngoài phạm vi, nói thật giới hạn, hỏi lại), lượt lịch / biểu mẫu / sửa lịch — chữ lịch có tên quán lấy từ bản đồ mở, model không được thấy
    (`llm/quan_lich.py`). Chữ mục web vốn không nằm trong `trace.answer`.
    `mo_cho_cuoc_co_lich` = GIÁ TRỊ của cờ `nho_dap_cuoc_co_lich` (22/11/2026), không phải "cuộc này có lịch" — cuộc không có lịch thì hai nhánh dưới cho cùng kết quả. Trong cuộc ĐÃ LƯU lịch, đường thường luôn để lại `trace.sua = {n_hanh_dong: 0}` và luôn nối
    nguồn lịch (`lich_dang_co`) ⇒ luật "lượt DÙNG lịch không giữ đáp" thành "cả cuộc không giữ". Bật ⇒ chỉ chặn lượt THẬT là lượt sửa lịch (có hành động
    / khẩn cấp) hoặc câu trả lời có TRÍCH nguồn lịch; các công cụ đổi theo giờ khác vẫn chặn. Câu hỏi về lịch mà model chỉ trích bài kho thì VẪN được giữ — không gây đáp cũ sai,
    vì lịch chỉ đổi qua một lượt sửa đạt và lượt đó làm rơi đáp nhớ. Tắt ⇒ y như trước."""
    # 21/11/2026: KHÔNG giữ đáp của lượt đã dùng công cụ đổi theo giờ (thời tiết, ngày / lịch âm, khoảng cách — cùng luật `luot_luu_duoc` của bộ nhớ câu trả
    # lời giữa các cuộc). Lượt tự kiểm trên Sonnet: hỏi tiếp về "con số khả năng mưa bạn vừa đưa" — có đáp cũ trong lịch sử thì model tự từ chối 8 / 10 lần
    # (số đã nằm trong lời "không phải nguồn" nên nó không gọi lại công cụ), không có thì 0 / 6. Số dự báo phải luôn đến từ công cụ của LƯỢT NÀY.
    thuong = outcome == "success" and not trace.bieu_mau and trace.lich is None and trace.lich_v2 is None
    if not mo_cho_cuoc_co_lich:
        return thuong and trace.sua is None and not any(cong_cu["name"] in CONG_CU_KHONG_NHO_DAP for cong_cu in trace.tools)
    from llm.lich_trinh_v2 import NGUON_LICH_SOURCE  # import muộn: module này chỉ cần hằng đó khi cờ bật
    sua = trace.sua or {}
    la_luot_sua = bool(sua.get("n_hanh_dong") or sua.get("khan_cap"))
    trich_lich = any(getattr(nguon, "source", None) == NGUON_LICH_SOURCE for nguon in (trace.cited or ()))
    return (thuong and not la_luot_sua and not trich_lich
            and not any(cong_cu["name"] in CONG_CU_KHONG_NHO_DAP - {"lich_dang_co"} for cong_cu in trace.tools))


@dataclass
class Conversation:
    turns: list[tuple[str, str]] = field(default_factory=list)  # (câu hỏi, câu trả lời đã cắt) — chỉ nhớ câu hỏi ⇒ "" hoặc dòng ghi chú tên nơi do code dựng
    expires_at: float = 0.0
    lich: dict | None = None  # sửa lịch bản 2: lịch đã lưu của cuộc (chỉ dữ liệu code dựng — khung, ngày đi, điểm đã bỏ, câu đã kiểm)
    ghi_chu_cuoi: str | None = None  # `chi_dap_lien_truoc`: lượt cuối đang giữ câu trả lời ⇒ dòng ghi chú sẽ thế chỗ nó khi có lượt mới; None = không giữ
    goi_y_sua: tuple = ()  # cờ `sua_lich_them_khong_the`: câu sửa lịch code vừa gợi ý ("thay Y bằng X") — sống đúng MỘT lượt, không chữ người dùng / model


class ConversationStore:
    def __init__(self, count_tokens: Callable[[str], int], *, ttl: float = TTL_SECONDS, max_conversations: int = MAX_CONVERSATIONS,
                 max_turns: int = MAX_TURNS, keep_answers: bool = True, chi_dap_lien_truoc: bool = False,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self._count = count_tokens
        self._ttl, self._max_conversations = ttl, max_conversations
        self._max_turns = max_turns
        self._keep_answers = keep_answers
        # nghĩa mới của cờ `nho_cau_tra_loi`: chỉ lượt LIỀN TRƯỚC mang câu trả lời (`loi_luot_truoc`), lượt cũ hơn về dòng ghi chú / rỗng như khi chỉ nhớ
        # câu hỏi. `keep_answers` (nhớ đáp của cả ba lượt, bản 03/11 đã đo và không dùng) chỉ còn test cũ gọi — nơi dựng app không bật nữa.
        self.chi_dap_lien_truoc = chi_dap_lien_truoc
        self._clock = clock
        self._items: OrderedDict[str, Conversation] = OrderedDict()

    def _drop_expired(self) -> None:
        now = self._clock()
        for cid in [cid for cid, c in self._items.items() if c.expires_at <= now]:
            del self._items[cid]

    def ensure(self, conversation_id: str | None) -> str:
        """Mã cuộc dùng cho lượt này: mã còn hạn ⇒ giữ; không có / hết hạn / lạ ⇒ cuộc mới (mã mới)."""
        self._drop_expired()
        if conversation_id in self._items:
            return conversation_id
        new_id = secrets.token_urlsafe(16)
        self._items[new_id] = Conversation(expires_at=self._clock() + self._ttl)
        while len(self._items) > self._max_conversations:  # trần RAM: bỏ cuộc cũ nhất
            self._items.popitem(last=False)
        return new_id

    def history(self, conversation_id: str) -> tuple[tuple[str, str], ...]:
        conversation = self._items.get(conversation_id)
        return () if conversation is None else tuple(conversation.turns)

    def history_khong_dap(self, conversation_id: str) -> tuple[tuple[str, str], ...] | None:
        """Lịch sử của cuộc với ô CUỐI về dòng ghi chú / rỗng — đúng thứ lượt này sẽ thấy nếu không nhớ câu trả lời liền trước. None khi ô cuối
        không mang câu trả lời (không có gì để lùi). Dùng cho lần chạy lại của lượt bị rút vì lỗi trích dẫn (`llm.assistant.answer_turn_stream_parallel`)."""
        conversation = self._items.get(conversation_id)
        if conversation is None or not conversation.turns or conversation.ghi_chu_cuoi is None:
            return None
        return (*conversation.turns[:-1], (conversation.turns[-1][0], conversation.ghi_chu_cuoi))

    def history_tokens(self, conversation_id: str) -> int:
        """Số token lịch sử của cuộc (chỉ số đếm cho log — không chữ)."""
        return self.tokens_of(self.history(conversation_id))

    def tokens_of(self, turns) -> int:
        """Số token của một dãy lượt — route dùng cho lịch sử THẬT gửi model khi nó khác bản lưu (lượt xin liệt kê lại bỏ dòng ghi chú tên nơi)."""
        return sum(self._count(q) + self._count(a) for q, a in turns)

    def append(self, conversation_id: str, question: str, answer: str, ghi_chu: str = "") -> None:
        """Ghi một lượt đã xong rồi cắt theo trần SỐ LƯỢT (bỏ lượt cũ nhất trước). Không còn trần token của lịch sử (User 19/11/2026).
        `ghi_chu` (cờ `nho_ten_goi_y`): dòng do CODE dựng — tên nơi lượt này đã gợi ý — đứng ở chỗ câu trả lời khi chỉ nhớ câu hỏi.
        `chi_dap_lien_truoc`: lượt vừa xong giữ câu trả lời (KHÔNG kèm dòng ghi chú — tên nơi đã nằm trong chính câu trả lời, không nói hai lần);
        khi có lượt mới thì ô của nó về dòng ghi chú."""
        conversation = self._items.get(conversation_id)
        if conversation is None:  # hết hạn trong lúc trả lời ⇒ không ghi
            return
        if self.chi_dap_lien_truoc:
            if conversation.turns and conversation.ghi_chu_cuoi is not None:  # lượt trước thôi là "liền trước" ⇒ bỏ câu trả lời, về dòng ghi chú
                conversation.turns[-1] = (conversation.turns[-1][0], conversation.ghi_chu_cuoi)
            dap = loi_luot_truoc(answer)  # nơi gọi đưa `answer` rỗng cho lượt không được nhớ đáp (lịch, câu cố định…)
            conversation.turns.append((question, dap or ghi_chu))
            conversation.ghi_chu_cuoi = ghi_chu if dap else None
        else:
            conversation.turns.append((question, stored_answer(answer) if self._keep_answers else ghi_chu))
        del conversation.turns[:-self._max_turns]
        conversation.expires_at = self._clock() + self._ttl
        self._items.move_to_end(conversation_id)

    def lay_lich(self, conversation_id: str | None) -> dict | None:
        """Lịch đã lưu của cuộc CÒN HẠN (cuộc đã quá hạn mà chưa bị dọn ⇒ None — đường tải file không gọi `ensure`, phải tự xét hạn)."""
        conversation = self._items.get(conversation_id)
        return None if conversation is None or conversation.expires_at <= self._clock() else conversation.lich

    def lay_goi_y_sua(self, conversation_id: str | None) -> tuple:
        """Câu sửa lịch code đã gợi ý ở lượt trước — ĐỌC LÀ XOÁ: lượt này dùng xong (hoặc lỗi giữa chừng) thì lượt sau không còn thấy."""
        conversation = self._items.get(conversation_id)
        if conversation is None or conversation.expires_at <= self._clock():
            return ()
        goi_y, conversation.goi_y_sua = conversation.goi_y_sua, ()
        return goi_y

    def luu_goi_y_sua(self, conversation_id: str | None, goi_y: tuple) -> None:
        conversation = self._items.get(conversation_id)
        if conversation is not None:
            conversation.goi_y_sua = tuple(goi_y)

    def luu_lich(self, conversation_id: str | None, lich: dict) -> None:
        """Ghi lịch mới nhất của cuộc (thay lịch cũ); cuộc hết hạn ⇒ không ghi. Cùng hạn với lịch sử (30 phút từ lượt cuối)."""
        conversation = self._items.get(conversation_id)
        if conversation is not None:
            conversation.lich = lich

    def reset(self, conversation_id: str | None) -> str:
        """"Cuộc trò chuyện mới": xoá cuộc hiện tại khỏi RAM, trả mã mới. Mã mới CHƯA chiếm chỗ trong kho — lượt hỏi đầu tiên mới tạo cuộc (`ensure` gặp
        mã lạ ⇒ cấp mã khác và đặt lại cookie). Rà bảo mật 22/11 (R4): trước đây mỗi lần gọi (giao diện gọi ở MỖI lần tải trang) chiếm một chỗ ⇒ 500 lần
        gọi, của bất kỳ ai, đẩy mọi cuộc đang có — kèm lịch đã lưu — ra khỏi kho."""
        self._items.pop(conversation_id, None)
        return secrets.token_urlsafe(16)
