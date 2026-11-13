"""Lõi chung của trợ lý (Phase 9; đổi tên + thêm `tim_kho` / sổ nguồn / log ở B0): tìm kho (`tim_kho`) → dựng ngữ cảnh → sinh → kiểm citation.

`POST /api/chat` (`api/routes/chat.py`) và bộ đánh giá (`evaluation/full_corpus_eval.py` `answer_case`) cùng gọi `answer_query`;
`POST /api/chat/stream` gọi chung `prepare_answer` (phần trước model) và `check_citations`, chỉ phần sinh là stream
(spec streaming `2026-10-31-streaming-design.md` §3, §4.8). Phase 9 B0 (plan `docs/superpowers/plans/2026-11-02-phase-9-b0-plan.md`):
đường trả lời giữ y RAG 1–8 — code gọi `tim_kho` bằng câu gốc, sinh một lần; định tuyến (B1) và vòng công cụ do model gọi (B2) chưa có.

Ranh giới (plan B0 D3, test `tests/test_assistant_boundary.py`): module này **không** import SDK / client mạng; mọi lần gọi OpenAI nằm ở
`llm/generator_openai_full_corpus.py`. Lõi giữ chính sách (tuyến, công cụ, sổ nguồn, tiền mỗi lượt) bằng hàm Python thường.

Lõi chỉ làm các bước và ném lỗi có kiểu; nó **không** quyết phản hồi. Mỗi nơi gọi tự giữ cách của mình (spec streaming §4.8):
route đổi lỗi ra mã HTTP, chuẩn hóa `[Nguồn n]` → `[n]`, trả 500 khi citation hỏng, ghi `EvidenceRecorder`; bộ đánh giá
giữ chữ gốc, giữ chữ khi citation hỏng, đổi mọi lỗi thành `row["error"]`.
"""
import asyncio
import dataclasses
import time
from dataclasses import dataclass, field
from pathlib import Path

import json
import logging
from typing import Literal

import anyio

from core.schema import (ContextBudgetError, CitationIntegrityError, GenerationError, GeneratorNotReadyError, RetrievalDependencyError,
                         RetrievedDocument)
from llm.answer_stream import AnswerTextStream
from llm.citations import select_cited_sources
from llm import lich_trinh as lt
from llm import lich_trinh_v2 as lt2
from llm import tra_web as tw
from llm import thoi_tiet as tt
from llm import ngay_lich as nl
from llm.do_so import do_ngay_di
from llm.hoi_lai import TRUONG_THEO_LOAI, the_hoi_lai
from llm.full_corpus_prompt import (INSUFFICIENT_ANSWER, LICH_TRINH_LUAT, MAY_HAVE_CHANGED_NOTICE, OUT_OF_SCOPE_ANSWER, TOOL_DA_DU_LICH,
                                   TOOL_LIMIT_TEXT, TOOL_NO_NEW_TEXT, build_assistant_input, today_line)
from llm.generator_openai_full_corpus import CallLog, GeneratedText
from llm.pricing import cost_usd
from retrieval.full_corpus_context import LICH_TRINH_TOOL_OVERHEAD, FullCorpusContextBuilder, PackedContext, PackedSource

logger = logging.getLogger("chat")  # cùng logger với route: dòng `chat_stream_drain` giữ tên + khuôn như trước B1

# Tuyến (spec Phase 9 §3). B0: mọi câu `tro_ly_hue` = đường RAG 1–8. B1: luật khẩn cấp + định tuyến chọn một trong 4.
ROUTE_TRO_LY_HUE = "tro_ly_hue"
ROUTE_TRO_CHUYEN = "tro_chuyen"
ROUTE_NGOAI_PHAM_VI = "ngoai_pham_vi"
ROUTE_KHAN_CAP = "khan_cap"
# H4c (B1 D8): nguồn trích thuộc vé / điểm đến / lễ hội ⇒ dòng "có thể đã thay đổi".
NOTICE_SOURCE_PREFIXES = ("travel/tickets/", "travel/places/", "festivals/")
MODEL_SEARCH_LIMIT = 2  # B2 D5: số lần MODEL gọi `tim_kho` được tìm thật (lần tìm đầu của code không tính); lần 3 ⇒ TOOL_LIMIT_TEXT
SEARCH_VARIANTS = ("v0", "v1", "v2", "v3")  # B2a: lần tìm đầu (plan D1)
STREAM_DRAIN_SECONDS = 0.5  # ngắt giữa chừng: sau `result.cancel()` đọc nốt tối đa chừng này giây (spec streaming §4.5 bước 3)


# Các ô của biểu mẫu "Lên kế hoạch" bản 2 (spec §3.1); thứ tự = thứ tự trên biểu mẫu
O_BIEU_MAU_V2 = ("so_ngay", "nguoi_lon", "tre_em", "lon_tuoi", "kieu_di", "so_thich", "ngay_di")


@dataclass(frozen=True)
class AssistantFlags:
    """Cờ từng phần B1 (plan D9, `settings.yaml` khối `assistant:`); tắt cả 4 ⇒ chuỗi gửi model như B0.
    B2 (plan B2 D1): `lan_tim_dau` — v0 câu gốc · v1 / v3 câu tìm do định tuyến viết (cần `router`) · v2 trợ lý tự gọi `tim_kho`;
    `tim_them` — sau lần tìm đầu của code, trợ lý được gọi `tim_kho` thêm (B2b). `v0` + `tim_them` tắt ⇒ chuỗi gửi model như B1."""
    router: bool = False
    today_line: bool = False
    may_have_changed_notice: bool = False
    lan_tim_dau: str = "v0"
    tim_them: bool = False
    # B3 (plan B3 D7): nhớ hội thoại trong một cuộc trò chuyện — tắt tới khi giao diện nhiều lượt xong (D8); chỉ nhớ câu hỏi khi `nho_cau_tra_loi` tắt
    nho_hoi_thoai: bool = False
    nho_cau_tra_loi: bool = True
    # B5 (plan B5 bản 7 D1): công cụ `lich_trinh` — tắt tới khi đạt luật ghi trước; cần bảng điểm User duyệt (`bang_lich`, nạp ở rìa)
    lich_trinh: bool = False
    bang_lich: "lt.Bang | None" = field(default=None, compare=False, repr=False)
    # Cổng đợt 1 (spec `2026-11-06-giao-dien-cong-dot-1-design.md` D3 / D4): lượt từ biểu mẫu "Lên kế hoạch" — code xếp lịch bằng giá trị nút; tách khỏi
    # `lich_trinh` (câu gõ tự do). TẮT tới khi đạt Q-F; cần bảng điểm (không cần vòng công cụ: lượt biểu mẫu sinh một lần, không công cụ)
    lich_trinh_bieu_mau: bool = False
    # Bản đồ lịch trình (plan `2026-11-08-ban-do-lich-trinh-plan.md`): toạ độ do code gắn vào dữ liệu giao diện của lịch (không vào chuỗi gửi model);
    # bật ⇒ CSP cho ảnh tile OSM (`api/app.py`). Cần bảng điểm + bảng toạ độ (`toa_do_lich`, nạp ở rìa)
    ban_do_lich: bool = False
    toa_do_lich: "dict | None" = field(default=None, compare=False, repr=False)
    # Thí nghiệm tốc độ #6 (plan 2026-11-04-phase-9-toc-do-song-song): đường stream chạy phần `tro_ly_hue` cùng lúc định tuyến; tắt = như cũ
    song_song_tra_loi: bool = False
    # B6 (plan B6 bản 3 D10): cổng web sau câu trả lời kho — TẮT tới khi đạt luật ghi trước; cần định tuyến + vòng công cụ
    tra_web: bool = False
    # B5b (plan B5b bản 2 D11): thời tiết Huế (Open-Meteo) — TẮT tới khi đạt luật ghi trước; `du_bao` = hàm lấy dự báo (nạp ở rìa; test truyền
    # phản hồi ghi sẵn)
    thoi_tiet: bool = False
    # Phase 9 T1 (plan `2026-11-08-phase-9-t1-ngay-plan.md`): công cụ `ngay_lich` (code tính ngày + đổi âm ↔ dương) — chỉ đưa khi câu có từ chỉ ngày
    ngay_lich: bool = False
    # 12/11 (plan `2026-11-12-het-luot-tim-plan.md`): model đã dùng hết `MODEL_SEARCH_LIMIT` lần tìm thật ⇒ lượt gọi model kế tiếp không còn công cụ
    # `tim_kho` (bớt một lượt gọi chỉ để nhận chữ "đã hết lượt"). TẮT tới khi đo đạt; tắt ⇒ gọi generator y như trước.
    het_luot_bo_cong_cu: bool = False
    # "Lên kế hoạch" đợt 1 (plan `2026-11-12-len-ke-hoach-dot-1-plan.md`, spec bản 3.3 §5c.8): biểu mẫu bốn nhóm + hợp đồng `truong` mới — một cờ cho
    # cả đợt, TẮT tới khi đạt nghiệm thu; cần `lich_trinh_bieu_mau`. `len_ke_hoach_o_hien` = các ô biểu mẫu hiện (`/api/tinh_nang`): ô chưa có tác
    # dụng với bộ xếp đang dùng thì chưa hiện (spec N1)
    len_ke_hoach_v2: bool = False
    len_ke_hoach_o_hien: tuple[str, ...] = ()
    bang_lich_v2: "lt2.BangV2 | None" = field(default=None, compare=False, repr=False)  # bảng v8 (`assistant.lich_trinh_bang_v2`), nạp khi cờ bật
    # sở thích dưới sàn "có tác dụng" của mô phỏng (plan §3 (b)) ⇒ ô ẩn; test khoá danh sách này khớp kết quả mô phỏng trên bảng đang dùng
    len_ke_hoach_so_thich_an: tuple[str, ...] = ()
    du_bao: "object | None" = field(default=None, compare=False, repr=False)

    def __post_init__(self) -> None:
        if self.lan_tim_dau not in SEARCH_VARIANTS:
            raise ValueError(f"assistant.lan_tim_dau must be one of {SEARCH_VARIANTS}")
        if self.lan_tim_dau in ("v1", "v3") and not self.router:
            raise ValueError("assistant.lan_tim_dau v1 / v3 needs assistant.router: true (search text is written by the router)")
        if self.lich_trinh and (not self.tim_them or self.bang_lich is None):
            raise ValueError("assistant.lich_trinh needs assistant.tim_them: true and the itinerary table (assistant.lich_trinh_bang)")
        if self.lich_trinh_bieu_mau and self.bang_lich is None:
            raise ValueError("assistant.lich_trinh_bieu_mau needs the itinerary table (assistant.lich_trinh_bang)")
        if self.ban_do_lich and (self.bang_lich is None or self.toa_do_lich is None):
            raise ValueError("assistant.ban_do_lich needs the itinerary table and assistant.lich_trinh_toa_do")
        if self.tra_web and not (self.router and self.tim_them):
            raise ValueError("assistant.tra_web needs assistant.router: true and assistant.tim_them: true")
        if self.ngay_lich and not self.tim_them:
            raise ValueError("assistant.ngay_lich needs assistant.tim_them: true (tool loop)")
        if self.thoi_tiet and (not self.tim_them or self.du_bao is None):
            raise ValueError("assistant.thoi_tiet needs assistant.tim_them: true and a forecast function")
        if self.len_ke_hoach_v2 and (not self.lich_trinh_bieu_mau or self.bang_lich_v2 is None):
            raise ValueError("assistant.len_ke_hoach_v2 needs assistant.lich_trinh_bieu_mau: true and the v2 table (assistant.lich_trinh_bang_v2)")
        if not set(self.len_ke_hoach_o_hien) <= set(O_BIEU_MAU_V2):
            raise ValueError(f"assistant.len_ke_hoach_o_hien must be a subset of {O_BIEU_MAU_V2}")

    @classmethod
    def from_settings(cls, settings: dict) -> "AssistantFlags":
        config = settings.get("assistant") or {}
        values = {name: bool(config.get(name, cls.__dataclass_fields__[name].default)) for name in BOOL_FIELDS}
        # chỉ nạp khi một trong hai cờ lịch bật (clone không có `data/` vẫn chạy cờ tắt)
        bang = nap_bang_lich(settings) if values["lich_trinh"] or values["lich_trinh_bieu_mau"] else None
        toa_do = lt.nap_toa_do(BACKEND_DIR / config["lich_trinh_toa_do"], bang) if values["ban_do_lich"] and bang is not None else None
        return cls(**values, lan_tim_dau=str(config.get("lan_tim_dau", "v0")), bang_lich=bang, toa_do_lich=toa_do,
                   du_bao=tt.lay_du_bao if values["thoi_tiet"] else None,
                   len_ke_hoach_o_hien=tuple(config.get("len_ke_hoach_o_hien") or ()),
                   len_ke_hoach_so_thich_an=tuple(config.get("len_ke_hoach_so_thich_an") or ()),
                   bang_lich_v2=lt2.nap_bang_v2(BACKEND_DIR / config["lich_trinh_bang_v2"]) if values["len_ke_hoach_v2"] else None)

    @property
    def so_thich_hien(self) -> tuple[str, ...]:
        """Sở thích hiện trên biểu mẫu bản 2: loại đủ điểm trong bảng (≥ 4) trừ loại dưới sàn mô phỏng."""
        if self.bang_lich_v2 is None:
            return ()
        return tuple(s for s in self.bang_lich_v2.loai_hien if s not in self.len_ke_hoach_so_thich_an)

    @property
    def uses_tools(self) -> bool:
        """Tuyến `tro_ly_hue` đi vòng công cụ (trợ lý có `tim_kho`) thay vì sinh một lần."""
        return self.lan_tim_dau == "v2" or self.tim_them


BACKEND_DIR = Path(__file__).resolve().parents[1]  # đường dẫn trong settings tương đối theo `backend/`


def nap_bang_lich(settings: dict) -> "lt.Bang":
    """Bảng điểm lịch trình (B5 D2) từ `assistant.lich_trinh_bang` (tương đối theo `backend/`, như các đường dẫn khác của settings)."""
    return lt.nap_bang(BACKEND_DIR / settings["assistant"]["lich_trinh_bang"])


BOOL_FIELDS = tuple(name for name in AssistantFlags.__dataclass_fields__
                    if name not in ("lan_tim_dau", "bang_lich", "toa_do_lich", "du_bao", "len_ke_hoach_o_hien", "bang_lich_v2",
                                     "len_ke_hoach_so_thich_an"))


def elapsed_ms(started: float) -> float:
    return round((time.perf_counter() - started) * 1000, 1)


@dataclass
class AnswerTrace:
    """Một lượt đã đi tới đâu. Lõi điền dần từng bước, nên khi một bước ném lỗi nơi gọi vẫn đọc được các bước trước
    (route: số đo `chat_metrics` của lần lỗi; bộ đánh giá: `top_chunk_ids`, `context_sources`, token của dòng lỗi)."""

    documents: list[RetrievedDocument] | None = None  # toàn bộ kết quả tìm, đúng thứ tự
    search_ms: float | None = None
    dense_ms: float | None = None
    packed: PackedContext | None = None
    context_ms: float | None = None
    generated: GeneratedText | None = None  # None khi ngữ cảnh không có nguồn ⇒ từ chối, không gọi model
    generation_ms: float | None = None
    answer: str | None = None  # chữ gốc của model (chưa chuẩn hóa citation) hoặc câu từ chối chuẩn
    cited: tuple[PackedSource, ...] | None = None  # nguồn được trích; chỉ có khi citation hợp lệ
    citation_ms: float | None = None
    citation_error: CitationIntegrityError | None = None  # citation hỏng: không ném, để mỗi nơi tự xử (spec §4.8 khác biệt 2)
    route: str = ROUTE_TRO_LY_HUE
    # Sổ nguồn của cả lượt: mọi kiểm citation đọc từ đây. B0 một lần tìm ⇒ sổ = nguồn của ngữ cảnh, giữ nguyên số [n];
    # đánh số nối khi tìm nhiều lần (B2b) và phần web [w n] (B6) để plan bậc đó (plan B0 D4).
    so_nguon: list[PackedSource] = field(default_factory=list)
    tools: list[dict] = field(default_factory=list)  # mỗi lần chạy công cụ: {"name", "ms"}
    llm_calls: list[dict] = field(default_factory=list)  # mỗi lần gọi model (generator `CallLog`) + `route` của lần gọi
    # B1: câu trả lời cố định (không qua kiểm citation) ⇒ outcome riêng: "out_of_scope" / "refusal_no_sources" (phương án B G: bỏ "emergency")
    fixed_outcome: str | None = None
    emergency_by: str | None = None  # "router" — định tuyến chọn khan_cap (phương án B G: câu vẫn đi agent Huế, không câu soạn sẵn)
    route_error: str | None = None  # định tuyến lỗi ⇒ đi `tro_ly_hue`
    routing_ms: float | None = None
    today: str | None = None  # dòng ngày đã gửi model (D7) — log chỉ ghi phần ngày
    notice: str | None = None  # dòng H4c (D8)
    # B2: câu tìm định tuyến viết (V1 / V3) — chỉ trong RAM, KHÔNG log (chữ người dùng); số câu + cờ rỗng thì log được
    cau_tim: list[str] | None = None
    cau_tim_rong: bool = False
    model_searches: int = 0  # số lần model gọi `tim_kho` (D5 trần)
    model_queries: list[str] = field(default_factory=list)  # câu tìm model viết khi gọi `tim_kho` — KHÔNG log
    context_parts: list[str] = field(default_factory=list)  # chữ ngữ cảnh mỗi lần tìm — đếm ngân sách chung (D5)
    seen_ids: list[str] = field(default_factory=list)  # chunk_id đã vào ngữ cảnh — lần tìm sau bỏ trùng (D5)
    tool_error: Exception | None = None  # lỗi tìm / ngữ cảnh trong công cụ: SDK có thể bọc lại ⇒ lõi ném lại đúng lỗi gốc
    # B3: lịch sử cuộc trò chuyện của lượt này ((câu hỏi, câu trả lời đã cắt), …) — route đọc từ kho; rỗng = không nhớ (B2). KHÔNG log.
    history: tuple[tuple[str, str], ...] = ()
    # B4 D4: lượt ghép mang giá trị trường từ nút (`truong`, `{}` = "Trả lời luôn"); lần tìm đầu dùng câu gốc (m-3) thay vì câu ghép
    truong: dict | None = None
    search_query: str | None = None
    bieu_mau: bool = False  # cổng đợt 1 D3: lượt từ biểu mẫu "Lên kế hoạch" (route đặt; `truong` có đủ giá trị nút, `so_ngay` bắt buộc)
    clarify: dict | None = None  # dữ liệu thẻ hỏi lại (B5 D15: do code của `lich_trinh` dựng)
    # B5: lượt đưa công cụ `lich_trinh` (đếm ngân sách cộng LICH_TRINH_TOOL_OVERHEAD — D16); kết quả lần xếp (khung, số nguồn mỗi điểm…);
    # bước tiến độ đã làm (D14, mã + số / tên điểm — không chữ người dùng); mã vi phạm kiểm cuối (D8). KHÔNG log chữ.
    lich_offered: bool = False
    lich_calls: int = 0
    lich: dict | None = None
    buoc_lich: list[dict] = field(default_factory=list)
    lich_kiem: list[str] | None = None
    # "Lên kế hoạch" bản 2 (`llm/len_ke_hoach.py`): {"lich", "loi_khung", "cau", "loi_cau", "so_cau_du_phong", "loi_model"?}; None = không phải lượt bản 2
    lich_v2: dict | None = None
    # #6 (plan D2): phần `tro_ly_hue` chạy trước định tuyến rồi bị bỏ vì tuyến khác — số lần, USD (lần gọi xong = usage thật; lần bị huỷ
    # giữa chừng không có usage ⇒ cộng token vào bộ dựng đếm × giá vào = cận dưới), cờ bị huỷ giữa chừng. Chỉ số đếm, không chữ.
    n_tra_loi_bo: int = 0
    usd_bo: float | None = None
    bo_huy_giua: bool | None = None
    # B6: kết quả cổng web — {"outcome", "text", "nguon", "n_ket_qua", "n_ma", "kiem", "usd_serper"}; None = cổng không mở. Chữ web chỉ ở đây
    # (không vào `answer`) ⇒ lịch sử nhớ (`answer`) không bao giờ chứa chữ web (D7). KHÔNG log chữ.
    web: dict | None = None
    # B5b: ngữ cảnh code dò ở câu này (bão / lũ, ngoài 7 ngày, có buổi, có đưa công cụ) · kết quả công cụ `thoi_tiet` (trạng thái, khối số liệu code
    # in) · phần code nối sau chữ model · số thời tiết ngoài tập cho phép (D8). KHÔNG log chữ.
    thoi_tiet_ctx: dict | None = None
    thoi_tiet: dict | None = None
    thoi_tiet_noi: str | None = None
    thoi_tiet_kiem: list[str] | None = None


async def search_into_trace(queries: list[str], *, cau_hoi: str, retrieval_service, context_builder, trace: AnswerTrace,
                            today: str | None = None, instructions: str | None = None, by: str = "code") -> PackedContext:
    """Một lần tìm của lượt: tìm `queries` (1 câu ⇒ `search`; nhiều ⇒ `search_many`, B2 V3) → dựng ngữ cảnh → nối sổ nguồn.
    Ngân sách token đếm bằng `cau_hoi` (câu thật gửi model — B2 D3) + ngữ cảnh các lần trước (`trace.context_parts`) + `instructions` của
    đường trợ lý (B2 D5); lần sau đánh số tiếp, bỏ đoạn đã có. Lần đầu điền `trace.documents` / `trace.packed` (như B1); thời gian cộng dồn.
    Lỗi đi ra nguyên kiểu: `RetrievalDependencyError` (tìm), `ContextBudgetError` (ngữ cảnh)."""
    tool_started = time.perf_counter()
    first = trace.packed is None
    packed = None
    try:
        started = time.perf_counter()
        if len(queries) == 1:
            result = await asyncio.to_thread(retrieval_service.search, queries[0])
        else:
            result = await asyncio.to_thread(retrieval_service.search_many, queries)
        search_ms = elapsed_ms(started)
        dense_ms = result.trace.timings_ms.get("dense_ms")  # trace giữ 3 chữ số; làm tròn 1 chữ số như các trường *_ms khác
        dense_ms = None if dense_ms is None else round(dense_ms, 1)
        if first:  # ghi ngay (như B1): ngữ cảnh lỗi sau đó thì nơi gọi vẫn đọc được số đo + kết quả tìm
            trace.documents, trace.search_ms, trace.dense_ms = result.documents, search_ms, dense_ms
        else:
            trace.search_ms = round((trace.search_ms or 0) + search_ms, 1)
            trace.dense_ms = None if dense_ms is None else round((trace.dense_ms or 0) + dense_ms, 1)

        started = time.perf_counter()
        packed = context_builder.build(cau_hoi, result.documents, today=today, first_id=len(trace.so_nguon) + 1,
                                       prior_context="\n\n".join(trace.context_parts), skip_ids=frozenset(trace.seen_ids),
                                       instructions=instructions, history=trace.history,
                                       n_tool_items=2 * trace.model_searches if by == "model" else 0,
                                       extra_tool_tokens=LICH_TRINH_TOOL_OVERHEAD if trace.lich_offered else 0)
        context_ms = elapsed_ms(started)
        if first:
            trace.packed, trace.context_ms = packed, context_ms
        else:
            trace.context_ms = round((trace.context_ms or 0) + context_ms, 1)
        trace.so_nguon.extend(packed.sources)
        trace.context_parts.append(packed.text)
        trace.seen_ids.extend(packed.document_ids)
        return packed
    finally:
        entry = {"name": "tim_kho", "ms": elapsed_ms(tool_started)}
        if not first or by == "model" or len(queries) > 1:  # B2: thêm số đo cho lần tìm thêm / do model / nhiều câu; lần tìm đầu một câu giữ như B1
            entry.update(by=by, n_queries=len(queries), n_new=None if packed is None else len(packed.sources))
        trace.tools.append(entry)


async def tim_kho(cau_tim: str, *, retrieval_service, context_builder, trace: AnswerTrace, today: str | None = None,
                  cau_hoi: str | None = None) -> None:
    """Công cụ tìm kho: tìm `cau_tim` → dựng ngữ cảnh, ghi vào `trace` + sổ nguồn. Tham số vị trí là phần model thấy (chỉ `cau_tim`);
    top-k, collection, pool, giới hạn token nằm trong `retrieval_service` / `context_builder` do code dựng (plan B0 D2). `cau_hoi` (B2 D3):
    câu thật gửi model để đếm ngân sách — None ⇒ chính `cau_tim` (B0 / B1)."""
    await search_into_trace([cau_tim], cau_hoi=cau_tim if cau_hoi is None else cau_hoi, retrieval_service=retrieval_service,
                            context_builder=context_builder, trace=trace, today=today)


def tool_for_turn(query: str, retrieval_service, context_builder, trace: AnswerTrace, today: str | None, instructions: str):
    """Hàm `tim_kho` của **một lượt** cho trợ lý có công cụ (B2 D5): generator bọc thành công cụ SDK (lõi không import SDK — T-3).
    Model chỉ thấy `cau_tim`; trần `MODEL_SEARCH_LIMIT` đếm ở đây; lần vượt ⇒ chữ "đã hết lượt", không tìm. Lỗi tìm / ngữ cảnh: ghi
    `trace.tool_error` rồi ném (lõi ném lại đúng lỗi gốc ⇒ route ra câu lỗi như B1, không đưa lỗi cho model)."""

    async def tim_kho(cau_tim: str) -> str:
        """Tìm thêm Bằng chứng trong kho tri thức Huế bằng một câu tìm đứng một mình; trả các nguồn mới, đánh số tiếp theo.

        Args:
            cau_tim: câu tìm đứng một mình cho phần thông tin còn thiếu.
        """
        trace.model_searches += 1
        trace.model_queries.append(cau_tim)  # chỉ RAM / file private của harness — không log (chữ do model viết từ câu người dùng)
        if trace.lich is not None:  # B5 vòng chỉnh 1 (a): đã có khung lịch + đoạn từng điểm ⇒ không tìm thật, bảo model viết ngay (chặn bằng code)
            trace.tools.append({"name": "tim_kho", "ms": 0.0, "by": "model", "n_queries": 0, "n_new": 0, "sau_lich": True})
            return TOOL_DA_DU_LICH
        if trace.model_searches > MODEL_SEARCH_LIMIT:
            trace.tools.append({"name": "tim_kho", "ms": 0.0, "by": "model", "n_queries": 0, "n_new": 0, "het_luot": True})
            return TOOL_LIMIT_TEXT
        try:
            packed = await search_into_trace([cau_tim], cau_hoi=query, retrieval_service=retrieval_service, context_builder=context_builder,
                                             trace=trace, today=today, instructions=instructions, by="model")
        except (RetrievalDependencyError, ContextBudgetError) as exc:
            trace.tool_error = exc
            raise
        return packed.text or TOOL_NO_NEW_TEXT

    return tim_kho


# Mọi công cụ của trợ lý, một chỗ (test ranh giới khoá tên + tham số; B2 bọc `function_tool` từ đây).
TOOLS = {"tim_kho": tim_kho}


def _history_kwargs(trace: AnswerTrace) -> dict:
    """`history=` chỉ truyền khi có lịch sử: lượt không lịch sử gọi generator y như B2 (generator thay thế trong test không cần tham số này)."""
    return {"history": trace.history} if trace.history else {}


def _assistant_instructions(generator, trace: AnswerTrace) -> str:
    """Lời dặn trợ lý thật sự gửi ở lượt này (có câu dặn lịch sử khi có lịch sử — B3 D3) — để đếm ngân sách đúng chuỗi gửi (D5).
    B5: công cụ `lich_trinh` không đổi lời dặn (D7). Không lịch sử ⇒ đọc thẳng thuộc tính (generator thay thế trong test không cần hàm)."""
    return generator.assistant_instructions_for(trace.history) if trace.history else generator.assistant_instructions


def lich_trinh_for_turn(query: str, retrieval_service, context_builder, trace: AnswerTrace, today: str | None, instructions: str, bang,
                        du_bao=None):
    """Hàm `lich_trinh` của **một lượt** (plan B5 bản 7 D1, D6, D14, D15): generator bọc thành công cụ SDK (lõi không import SDK).
    Model chỉ trích trường; **code** chốt số ngày (thiếu ⇒ trả dữ liệu thẻ hỏi lại — `tool_use_behavior` dừng lượt), xếp, kiểm luật, lấy một
    đoạn kho đúng file cho mỗi điểm vào sổ nguồn, rồi trả chữ khung + đoạn mới cho model viết lời. Trần ≤ 1 lần / câu."""

    async def lich_trinh(so_ngay: lt.SoNgay | None, di_cung: lt.DiCung | None, kieu_di: lt.KieuDi | None, so_thich: lt.SoThich | None,
                         them_diem: list[str] | None) -> "str | dict":
        """Xếp lịch tham quan.

        Args:
            so_ngay: số ngày người dùng nói (1, 2, 3, 4+); chưa nói thì null.
            di_cung: người đi cùng nếu người dùng nói; chưa nói thì null.
            kieu_di: thong_tha hoặc day_lich nếu người dùng nói; chưa nói thì null.
            so_thich: sở thích chính nếu người dùng nói; chưa nói thì null.
            them_diem: tên điểm người dùng muốn ghé, đúng chữ người dùng gõ (tối đa 3); không có thì null.
        """
        started = time.perf_counter()
        trace.lich_calls += 1
        entry = {"name": "lich_trinh"}
        try:
            if trace.lich_calls > 1:
                entry["het_luot"] = True
                return "Lịch đã xếp ở lần gọi trước trong lượt này; hãy viết câu trả lời theo khung đó."
            truong = trace.truong
            so_ngay_chot, tam = lt.chot_so_ngay(truong, so_ngay, query)
            if so_ngay_chot is None:  # D15 (4) / D12 (b): code hỏi lại — chỉ số ngày
                entry["hoi_lai"] = True
                return the_hoi_lai("lich_trinh", ["so_ngay"], trace.search_query or query)
            tu_nut = truong or {}
            ts = lt.ThamSo(so_ngay=so_ngay_chot, di_cung=di_cung or tu_nut.get("di_cung"), kieu_di=kieu_di or tu_nut.get("kieu_di"),
                           so_thich=so_thich or tu_nut.get("so_thich"), them_diem=tuple(them_diem or ()), so_ngay_tam=tam,
                           hoi_toi=lt.hoi_buoi_toi(query))
            khung = lt.xep(bang, ts)
            n_xep = len(lt.diem_trong_khung(khung))
            packed, nguon, nguon_ve = await _lay_nguon_lich(bang, khung, query, retrieval_service, context_builder, trace, today, instructions)
            loi = lt.kiem_khung(bang, khung)
            trace.lich = {"khung": khung, "nguon": nguon, "nguon_ve": nguon_ve, "loi_khung": loi}
            if du_bao is not None:  # B5b D9 / D10: dòng dự báo theo ngày đi + "nếu mưa" + bậc thang — chỉ thêm vào ghi chú, khung không đổi
                trace.lich["them_dong"] = await _dong_thoi_tiet_lich(bang, khung, query, du_bao, trace)
            # D14 (a): bước = việc code đã làm xong, đúng thứ tự (`kiem_luat_ok` chỉ khi khung 0 lỗi)
            trace.buoc_lich += [{"buoc": "xep_xong", "n_diem": n_xep},
                                {"buoc": "kiem_luat_ok"} if not loi else {"buoc": "kiem_luat_loi", "n_loi": len(loi)},
                                *({"buoc": "bo_diem", "diem": k["diem"], "ly_do": lt.CAU_KHONG_XEP[k["ma_luat"]].format(diem=k["diem"])}
                                  for k in khung["khong_xep"]),
                                {"buoc": "lay_nguon", "n_doan": len(packed.sources)}]
            entry.update(n_diem=len(lt.diem_trong_khung(khung)), n_new=len(packed.sources), n_khong_xep=len(khung["khong_xep"]))
            chu = lt.khung_chu(bang, khung, nguon, LICH_TRINH_LUAT, nguon_ve)
            trace.context_parts.append(chu)  # lần tìm thêm sau đó (nếu có) đếm cả chữ khung
            return f"{chu}\n\n{packed.text}" if packed.text else chu
        finally:
            entry["ms"] = elapsed_ms(started)
            trace.tools.append(entry)

    return lich_trinh


hom_nay_vn = tt.hom_nay_vn  # một chỗ tính "hôm nay" giờ Việt Nam cho lịch + thời tiết (cache dự báo dùng cùng hàm)


async def _dong_thoi_tiet_lich(bang, khung: dict, query: str, du_bao, trace: AnswerTrace) -> list[str]:
    """B5b D9: lịch có ngày đi trong 7 ngày (code dò — `do_so.do_ngay_di`) ⇒ một dòng dự báo / ngày của lịch + "Nếu mưa: thay <điểm ngoài trời> bằng
    <điểm trong nhà cùng cụm>" khi khả năng mưa ≥ 60 % (cột `trong_nha` của bảng; thiếu cột ⇒ không gợi ý). API lỗi ⇒ một câu cố định, 0 số. Không dò
    được ngày ⇒ không dòng nào (lịch như B5). D10: `bac_thang: nhieu` + người lớn tuổi ⇒ "X có nhiều bậc thang (theo kho)"."""
    ids = lt.diem_trong_khung(khung)
    dong = [f"{bang.theo_id[i]['ten']} có nhiều bậc thang (theo kho)." for i in ids
            if khung["tham_so"].get("di_cung") == "nguoi_lon_tuoi" and bang.theo_id[i].get("bac_thang") == "nhieu"]
    if do_ngay_di(query, hom_nay_vn()) is None:
        return dong
    kq = await du_bao()
    # lưu riêng ở `trace.lich` — không đè kết quả công cụ `thoi_tiet` nếu model cũng gọi trong lượt này
    trace.lich["thoi_tiet"] = {"trang_thai": kq.trang_thai, "loi": kq.loi, "ms": kq.ms, "tu_cache": kq.tu_cache}
    trace.tools.append({"name": "thoi_tiet", "ms": kq.ms, "by": "code", "trang_thai": kq.trang_thai, "loi": kq.loi})
    if kq.trang_thai != "ok":
        return dong + [tt.CAU_LOI]
    bat_dau = do_ngay_di(query, kq.ngay[0]["ngay"])  # ngày theo lịch của API (giờ Việt Nam) — tất định theo bản ghi API
    if bat_dau is None:
        return dong
    co = set(ids)
    for k, ngay in enumerate(khung["ngay"]):
        n = bat_dau + k
        if n >= tt.SO_NGAY:
            break
        d = kq.ngay[n]
        dong.append(f"Ngày {ngay['ngay']} — {tt.dong_ngay(d)}.")
        if d["xs"] is not None and d["xs"] >= tt.NGUONG_MUA:
            ngoai = [i for b in lt.BUOI for i in ngay["buoi"][b] if bang.theo_id[i].get("trong_nha") == "ngoai_troi"]
            for i in ngoai:
                thay = next((x["id"] for x in bang.diem if x.get("trong_nha") in ("trong_nha", "ca_hai") and x["cum"] == bang.theo_id[i]["cum"]
                             and x["id"] not in co), None)
                if thay is not None:
                    dong.append(f"Nếu mưa ngày {ngay['ngay']}: có thể thay {bang.theo_id[i]['ten']} bằng {bang.theo_id[thay]['ten']} (trong nhà).")
                    break
    return dong + [tt.dong_nguon(kq)]


def _nguon_thoi_tiet(trace: AnswerTrace, title: str, excerpts: tuple[str, ...]) -> str:
    """E17 (A chọn): kết quả công cụ thời tiết là **một nguồn thật** trong sổ nguồn (id tiếp theo, khuôn như đoạn kho) ⇒ model trích [k] như mọi
    nguồn; bộ kiểm citation giữ nguyên như `main` (không miễn [n]). Trả chữ nguồn cho model; đếm vào ngân sách như lần tìm thêm."""
    src = PackedSource(id=len(trace.so_nguon) + 1, title=title, heading_path=(tt.MUC_NGUON,), excerpts=excerpts, source=tt.NGUON_SOURCE)
    trace.so_nguon.append(src)
    chu = FullCorpusContextBuilder._block(src)
    trace.context_parts.append(chu)
    trace.thoi_tiet["nguon_id"] = src.id
    return chu


def thoi_tiet_for_turn(trace: AnswerTrace, du_bao):
    """Hàm `thoi_tiet` của **một lượt** (B5b D3, D5, D7): model chỉ gửi số ngày (0–6); code lấy dự báo, dựng khối số liệu cố định. ≤ 1 lần / câu."""
    Ngay = Literal[0, 1, 2, 3, 4, 5, 6]

    async def thoi_tiet(tu_ngay: Ngay, den_ngay: Ngay) -> str:
        """Lấy dự báo thời tiết Huế theo ngày.

        Args:
            tu_ngay: ngày đầu, tính từ hôm nay (0 = hôm nay, 1 = mai, … 6).
            den_ngay: ngày cuối, tính từ hôm nay (0–6); một ngày thì bằng tu_ngay.
        """
        entry = {"name": "thoi_tiet"}
        try:
            if trace.thoi_tiet is not None:
                entry["het_luot"] = True
                return "Đã lấy dự báo ở lần gọi trước trong lượt này; hãy viết câu trả lời."
            kq = await du_bao()
            trace.thoi_tiet = {"trang_thai": kq.trang_thai, "loi": kq.loi, "ms": kq.ms, "tu_cache": kq.tu_cache, "khoi": None}
            entry.update(ms=kq.ms, trang_thai=kq.trang_thai, loi=kq.loi)
            if kq.trang_thai != "ok":
                return _nguon_thoi_tiet(trace, tt.TIEU_DE_NGUON_LOI, (tt.CAU_LOI,))
            khoi = tt.khoi_du_bao(kq, tu_ngay, den_ngay, bool(trace.thoi_tiet_ctx and trace.thoi_tiet_ctx["buoi"]))
            trace.thoi_tiet.update(khoi=khoi, n_ngay=abs(den_ngay - tu_ngay) + 1)
            return _nguon_thoi_tiet(trace, tt.TIEU_DE_NGUON, tuple(x for x in khoi.splitlines()[1:] if x))  # bỏ dòng tiêu đề; còn dòng ngày + dòng ghi công / giờ
        finally:
            entry.setdefault("ms", 0.0)
            trace.tools.append(entry)

    return thoi_tiet


def ngay_lich_for_turn(trace: AnswerTrace, query: str = ""):
    """Hàm `ngay_lich` của **một lượt** (T1): model chỉ gửi loại lịch + số; code tính, dựng chữ, đăng thành **một nguồn** trong sổ nguồn (như
    `_nguon_thoi_tiet` — câu chỉ có ngày vẫn trích được [n]). ≤ 2 lần / câu (lần thứ 3 ⇒ câu nhắc, không tính)."""
    LoaiLich = Literal["hom_nay", "duong", "am"]

    async def ngay_lich(loai: LoaiLich, ngay: int, thang: int, nam: int, thang_nhuan: bool) -> str:
        """Hôm nay theo giờ Việt Nam và đổi ngày dương ↔ âm lịch Việt Nam.

        Args:
            loai: "hom_nay" (chỉ hôm nay), "duong" (đổi ngày dương sang âm) hoặc "am" (đổi ngày âm sang dương).
            ngay: ngày cần đổi (0 khi loai là "hom_nay").
            thang: tháng cần đổi (0 khi loai là "hom_nay").
            nam: năm cần đổi; 0 = người dùng không nêu năm (công cụ trả lần gần nhất đã qua và lần sắp tới).
            thang_nhuan: true nếu là tháng âm nhuận.
        """
        lan = sum(t["name"] == "ngay_lich" for t in trace.tools)
        entry = {"name": "ngay_lich", "ms": 0.0, "loai": loai, "nam": nam}  # 09/11: `nam` để biết model gửi năm nào (chỉ số, không chữ)
        trace.tools.append(entry)
        if lan >= 2:
            entry["het_luot"] = True
            return "Đã đổi ngày ở các lần gọi trước trong lượt này; hãy viết câu trả lời."
        # (i) A 08/11: khoảng "tuần này / tuần sau / tháng này" do code ghi — xét câu cuối + câu hỏi liền trước (như bộ dò)
        cau = " ".join([query] + ([trace.history[-1][0]] if trace.history else []))
        dong = nl.ket_qua(loai, ngay, thang, nam, thang_nhuan, cau=cau).splitlines()
        src = PackedSource(id=len(trace.so_nguon) + 1, title=nl.TIEU_DE_NGUON, heading_path=(nl.MUC_NGUON,), excerpts=tuple(dong), source=nl.NGUON_SOURCE)
        trace.so_nguon.append(src)
        chu = FullCorpusContextBuilder._block(src)
        trace.context_parts.append(chu)
        return chu

    return ngay_lich


def _nguon_lich_san(trace: AnswerTrace, query: str) -> str:
    """T1 nhanh (plan `2026-11-10-phase-9-t1-nhanh-plan.md` D2): S5 09/11 câu ngày gọi model 2–4 lần vì model phải gọi `ngay_lich` rồi mới viết ⇒
    code tính sẵn hôm nay / mai / tuần / ngày âm nêu trong câu và trong đoạn kho lần tìm đầu, đăng thành **một nguồn** (như kết quả `ngay_lich`), nối
    sau ngữ cảnh. Log chỉ số đếm (số dòng, số ngày âm), không chữ."""
    started = time.perf_counter()
    cau = " ".join([query] + ([trace.history[-1][0]] if trace.history else []))  # như `ngay_lich_for_turn`: câu cuối + câu hỏi liền trước
    dong, n_am = nl.lich_san(cau, trace.packed.text)
    src = PackedSource(id=len(trace.so_nguon) + 1, title=nl.TIEU_DE_NGUON, heading_path=(nl.MUC_NGUON,), excerpts=tuple(dong), source=nl.NGUON_SOURCE)
    trace.so_nguon.append(src)
    chu = FullCorpusContextBuilder._block(src)
    trace.context_parts.append(chu)
    trace.tools.append({"name": "lich_san", "ms": elapsed_ms(started), "n_dong": len(dong), "n_am": n_am})
    return chu


def chu_cua_model(trace: AnswerTrace) -> str:
    """Câu trả lời bỏ phần code nối sau chữ model (khối / câu thời tiết B5b) — cờ `refusal` của log tính trên phần này (review C m-1)."""
    answer, noi = trace.answer or "", trace.thoi_tiet_noi
    return answer[: -len(noi) - 2] if noi and answer.endswith(f"\n\n{noi}") else answer


def _thoi_tiet_cuoi(trace: AnswerTrace, text: str) -> None:
    """B5b, sau lần sinh (cờ bật, mọi câu tuyến `tro_ly_hue` — D8 m-1): số thời tiết trong chữ model ⊂ số code in ∪ số trong đoạn kho được trích; hỏng
    ⇒ rút lại như citation hỏng. Rồi code nối: khối số liệu (hoặc câu lỗi) · câu bão / lũ (D6) · câu "chỉ có dự báo 7 ngày" (D3)."""
    ctx = trace.thoi_tiet_ctx or {}
    tool = trace.thoi_tiet
    cho_phep = tt.tap_so(tool["khoi"]) if tool and tool["khoi"] else set()
    cho_phep |= tt.tap_so(" ".join(e for src in (trace.cited or ()) for e in src.excerpts))
    trace.thoi_tiet_kiem = tt.kiem_so(text, cho_phep)
    if tool is not None and tool["khoi"] and (trace.answer or "").strip() == INSUFFICIENT_ANSWER:
        trace.answer = tt.CAU_DAN_DU_BAO  # review C M-1: có dự báo mà model từ chối ⇒ không để câu từ chối đứng trước số liệu
        tool["thay_tu_choi"] = True
    noi = []
    if tool is not None:
        noi.append(tool["khoi"] or tt.CAU_LOI)
    if ctx.get("bao_lu"):
        noi.append(tt.CAU_BAO_LU)
    if ctx.get("ngoai_7") and ctx.get("tu_khoa"):
        noi.append(tt.CAU_NGOAI_7_NGAY)
    trace.thoi_tiet_noi = "\n\n".join(noi) or None
    if trace.thoi_tiet_noi:
        trace.answer = f"{trace.answer}\n\n{trace.thoi_tiet_noi}"
    if trace.thoi_tiet_kiem and trace.citation_error is None:
        trace.citation_error = CitationIntegrityError(f"weather numbers without source: {len(trace.thoi_tiet_kiem)}")


def _do_dai_bang_chung(doc: RetrievedDocument) -> int:
    """Số ký tự bằng chứng của một đoạn — đúng phần đi vào ngữ cảnh (`evidence_parts`, như `FullCorpusContextBuilder._source`)."""
    return sum(len(part["text"].strip()) for part in doc.metadata.get("evidence_parts") or []
               if isinstance(part, dict) and isinstance(part.get("text"), str))


async def _lay_nguon_lich(bang, khung: dict, query: str, retrieval_service, context_builder, trace: AnswerTrace, today: str | None,
                          instructions: str, nhap: str | None = None, lay_ve: bool = True, max_doan: int | None = None,
                          tim_mo_ta: str | None = None):
    """D6: mỗi điểm trong khung — `retrieval_service.search(<tên điểm>)` (đọc Qdrant, không ghi), chọn **đúng 1 đoạn** = đoạn có bằng chứng dài
    nhất trong top-10 có `source` = file nguồn của điểm (cổng đợt 1 S1, A chốt: "đoạn đầu" hay chỉ là dòng tên — 11/28 điểm < 80 ký tự — nên
    luật "kèm một ý ngắn lấy từ tài liệu" không viết được ⇒ model từ chối; bằng nhau ⇒ đoạn đứng trước); đoạn đã có trong sổ nguồn ⇒ dùng lại số [n] cũ; không có đoạn đúng file ⇒ bỏ điểm (mã `khong_co_doan_nguon`).
    Có điểm Quần thể ⇒ thêm 1 đoạn file vé chứa khung giờ (D5 (a)). Đoạn mới dựng ngữ cảnh nối sổ nguồn; vượt ngân sách ⇒ bớt ngày cuối (iii).
    Lỗi tìm / ngữ cảnh ⇒ `trace.tool_error` rồi ném (như `tim_kho`). Lịch bản 2: `nhap` = bản nháp tin nhắn của nó (đếm ngân sách), `lay_ve=False`
    (giờ gợi ý do code in — không cần đoạn file vé); mặc định ⇒ đúng như đường cũ. `tim_mo_ta` (lịch bản 2, vòng chỉnh nghiệm thu 13/11): tìm bằng
    "<tên> <tim_mo_ta>", lấy đoạn xếp hạng cao nhất cùng file NẾU đoạn đó nhắc tên điểm (đoạn tả điểm — luật cũ hay chọn đoạn "bằng chứng" như lăng
    lân cận / quy tắc ứng xử ⇒ model trả câu rỗng); không có ⇒ luật cũ."""
    try:
        da_co = {doc_id: i + 1 for i, doc_id in enumerate(trace.seen_ids)}  # sổ nguồn đánh số liền từ 1, song song `seen_ids`
        cho: dict[str, list[str]] = {}  # chunk_id mới ⇒ điểm dùng đoạn đó
        moi: list[RetrievedDocument] = []
        nguon: dict[str, int] = {}

        async def chon_doan(cau: str, source: str, chua: str | None = None) -> RetrievedDocument | None:
            result = await asyncio.to_thread(retrieval_service.search, cau)
            cung_file = [d for d in result.documents[:10] if d.metadata.get("source") == source and (chua is None or chua in d.text)]
            return max(cung_file, key=_do_dai_bang_chung, default=None)

        async def doan_mo_ta(d: dict) -> RetrievedDocument | None:
            result = await asyncio.to_thread(retrieval_service.search, f"{d['ten']} {tim_mo_ta}")
            ten = [lt.chuan_ten(t) for t in (d["ten"], *d["ten_khac"])]
            return next((x for x in result.documents[:10] if x.metadata.get("source") == d["nguon"]
                         and any(t in lt.chuan_ten(x.text) for t in ten)), None)

        for id_ in dict.fromkeys(lt.diem_trong_khung(khung)):  # hoạt động tối lặp lại ⇒ tìm một lần
            d = bang.theo_id[id_]
            doc = (await doan_mo_ta(d) if tim_mo_ta else None) or await chon_doan(d["ten"], d["nguon"])
            if doc is None:
                lt.bo_diem(khung, id_, d["ten"], "khong_co_doan_nguon")
            elif doc.id in da_co:
                nguon[id_] = da_co[doc.id]
            else:
                if doc.id not in cho:
                    moi.append(doc)
                cho.setdefault(doc.id, []).append(id_)
        ve = None
        if lay_ve and any(bang.theo_id[i]["quan_the"] for i in lt.diem_trong_khung(khung)):
            ve = await chon_doan(lt.VE_CAU_TIM, lt.VE_NGUON, chua="17h30")
            if ve is not None and ve.id not in da_co and ve.id not in cho:
                moi.append(ve)
        # chữ khung cũng vào model ⇒ đếm vào ngân sách bằng bản nháp (số nguồn tạm) — D6 (iii)
        if nhap is None:
            nhap = lt.khung_chu(bang, khung, dict.fromkeys(lt.diem_trong_khung(khung), 0), LICH_TRINH_LUAT, 0)
        packed = context_builder.build(query, moi, today=today, first_id=len(trace.so_nguon) + 1,
                                       prior_context="\n\n".join([*trace.context_parts, nhap]),
                                       skip_ids=frozenset(trace.seen_ids), instructions=instructions, history=trace.history,
                                       n_tool_items=2 * (trace.model_searches + 1), extra_tool_tokens=LICH_TRINH_TOOL_OVERHEAD,
                                       max_documents=max_doan)
    except (RetrievalDependencyError, ContextBudgetError) as exc:
        trace.tool_error = exc
        raise
    so = dict(zip(packed.document_ids, (src.id for src in packed.sources)))
    for doc_id, ids in cho.items():
        for id_ in ids:
            if doc_id in so:
                nguon[id_] = so[doc_id]
    while khung["ngay"] and any(i not in nguon for i in lt.diem_trong_khung(khung)):  # đoạn không vừa ngân sách ⇒ bớt từ ngày cuối
        lt.cat_ngay_cuoi(khung)
    nguon = {i: nguon[i] for i in lt.diem_trong_khung(khung)}
    nguon_ve = None if ve is None else (da_co.get(ve.id) or so.get(ve.id))
    trace.so_nguon.extend(packed.sources)
    trace.context_parts.append(packed.text)
    trace.seen_ids.extend(packed.document_ids)
    return packed, nguon, nguon_ve


def record_llm_calls(trace: AnswerTrace, calls, call_route: str | None = None) -> None:
    """Nối các lần gọi model đã xong vào `trace.llm_calls`, mỗi mục gắn tuyến của **lần gọi** (`router` / `tro_chuyen` / `tro_ly_hue`)."""
    trace.llm_calls.extend({"route": call_route or trace.route, **call} for call in calls)


def turn_usd(trace: AnswerTrace) -> float | None:
    """USD của cả lượt = cộng từng lần gọi. Không gọi model (câu cố định, từ chối trước model, lỗi trước bước sinh) ⇒ 0; đã gọi mà không có
    mục nào (ngắt / lỗi giữa chừng — không có usage) ⇒ None, không đoán."""
    serper = (trace.web or {}).get("usd_serper", 0.0)  # B6: lượt tra web (lần gọi model mục web đã nằm trong `llm_calls`)
    if trace.llm_calls:
        return sum(call["usd"] for call in trace.llm_calls) + serper
    return serper if trace.generation_ms is None and trace.routing_ms is None else None


async def prepare_answer(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, recorder=None,
                         today: str | None = None, instructions: str | None = None) -> None:
    """Phần trước model của tuyến `tro_ly_hue`: lần tìm đầu của code → ngữ cảnh. Câu tìm = câu gốc (V0) hoặc câu định tuyến viết
    (`trace.cau_tim`, B2 V1 / V3); ngân sách luôn đếm bằng câu gốc (B2 D3). `instructions`: lời dặn trợ lý khi lượt đi vòng công cụ (B2b).
    Ngữ cảnh không có nguồn ⇒ `trace.answer` = câu từ chối chuẩn (không gọi model). Còn lại cần model: `generator=None` nghĩa là
    chưa sẵn sàng ⇒ `GeneratorNotReadyError`. `recorder` chỉ route truyền (spec §4.8 khác biệt 4).

    Lỗi đi ra nguyên kiểu: `RetrievalDependencyError` (tìm), `ContextBudgetError` (ngữ cảnh), `GeneratorNotReadyError`."""
    await search_into_trace(trace.cau_tim or [trace.search_query or query], cau_hoi=query, retrieval_service=retrieval_service, context_builder=context_builder,
                            trace=trace, today=today, instructions=instructions)
    if recorder:
        recorder.record_packed_context(trace.packed)

    if not trace.packed.sources:
        if recorder:
            recorder.record_fallback()
        trace.answer = INSUFFICIENT_ANSWER  # từ chối trước khi gọi model
        trace.fixed_outcome = "refusal_no_sources"
        return

    if generator is None:
        raise GeneratorNotReadyError("generator is not ready")


def check_citations(trace: AnswerTrace) -> None:
    """Kiểm citation của `trace.answer` (chữ gốc model) với sổ nguồn. Kiểm trên chữ gốc: regex citation nhận cả `[n]` lẫn
    `[Nguồn n]` nên kết quả giống hệt kiểm sau chuẩn hóa. Hỏng ⇒ ghi `trace.citation_error`, không ném."""
    started = time.perf_counter()
    try:
        trace.cited = select_cited_sources(trace.answer, trace.so_nguon)
        trace.citation_ms = elapsed_ms(started)
    except CitationIntegrityError as exc:
        trace.citation_error = exc


def set_notice(trace: AnswerTrace, flags: AssistantFlags) -> None:
    """H4c (D8): câu trả lời kho có nguồn được trích thuộc vé / điểm đến / lễ hội ⇒ dòng cố định. Chữ câu trả lời không đổi."""
    if flags.may_have_changed_notice and trace.cited and any(src.source.startswith(NOTICE_SOURCE_PREFIXES) for src in trace.cited):
        trace.notice = MAY_HAVE_CHANGED_NOTICE


async def _before_model(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, recorder, today: str | None,
                        flags: AssistantFlags) -> str | None:
    """Phần trước lần gọi model của tuyến `tro_ly_hue`. Trả tin nhắn user cho trợ lý có công cụ (None = đường sinh một lần như B1).
    V2: không tìm trước (chỉ cần generator). Còn lại: `prepare_answer` (có thể đặt câu từ chối khi ngữ cảnh rỗng ⇒ `fixed_outcome`)."""
    if flags.lan_tim_dau == "v2":
        if generator is None:
            raise GeneratorNotReadyError("generator is not ready")
        return build_assistant_input(query, None, today)
    trace.lich_offered = flags.lich_trinh and generator is not None  # D16: mọi lượt có công cụ khi cờ bật (cờ cần `tim_them`)
    instructions = _assistant_instructions(generator, trace) if (flags.tim_them and generator is not None) else None
    await prepare_answer(query, retrieval_service, context_builder, generator, trace, recorder, today, instructions)
    if not flags.tim_them:
        return None
    context = trace.packed.text
    if flags.ngay_lich and trace.fixed_outcome is None and nl.co_tu_ngay_luot(query, trace.history):
        context = f"{context}\n\n{_nguon_lich_san(trace, query)}"  # T1 nhanh D2: lượt có từ chỉ ngày ⇒ lịch code tính trước lần gọi model đầu
    return build_assistant_input(query, context, today)


def _finish_generated(trace: AnswerTrace, flags: AssistantFlags | None = None) -> None:
    """Sau lần sinh: dừng ở thẻ hỏi lại (B5 D15) ⇒ lượt hỏi lại (không chữ, không kiểm citation); chạm `max_turns` (cờ generator, B2 D5) ⇒ câu
    từ chối cố định `max_turns`; lượt có lịch ⇒ ghép dòng "Mình hiểu" + chữ model + khối ghi chú (D12, D4b) rồi kiểm citation + kiểm cuối (D8);
    còn lại ⇒ kiểm citation trên sổ nguồn (cờ `lich_trinh` bật mà chữ có dạng lịch ⇒ kiểm cuối với khung rỗng, D8 (7))."""
    clarify = getattr(trace.generated, "clarify", None)
    if clarify is not None:
        trace.clarify = clarify
        _set_fixed(trace, "", "hoi_lai")
        return
    if getattr(trace.generated, "hit_max_turns", False):  # getattr: generator thay thế trong test chỉ có `text` (như route, B68 m-4)
        _set_fixed(trace, INSUFFICIENT_ANSWER, "max_turns")
        return
    text = trace.generated.text
    if trace.lich is not None:
        bang, khung, nguon = flags.bang_lich, trace.lich["khung"], trace.lich["nguon"]
        if text.strip() == INSUFFICIENT_ANSWER:  # B171 T3 (b): có khung mà model từ chối ⇒ code dựng lời lịch tối thiểu (stream: `_chu_giu_lai`)
            text = trace.lich["chu_thay"] = lt.loi_lich_toi_thieu(bang, khung, nguon)
        loi = lt.kiem_cuoi(bang, text, khung, nguon)
        trace.lich["minh_hieu"] = lt.dong_minh_hieu(khung)
        trace.lich["ghi_chu"] = lt.khoi_ghi_chu(bang, khung, nguon, trace.lich.get("them_dong", ()))
        trace.lich["nhac_lai"] = lt.dem_nhac_lai(bang, text, khung)
        trace.answer = "\n\n".join(part for part in (trace.lich["minh_hieu"], text, trace.lich["ghi_chu"]) if part)
    else:
        loi = lt.kiem_cuoi(flags.bang_lich, text, None) if flags is not None and flags.lich_trinh and lt.co_dang_lich(text) else []
        trace.answer = text
    check_citations(trace)
    if trace.lich is not None or loi:
        trace.lich_kiem = loi
    if loi and trace.citation_error is None:  # D8: hỏng ⇒ xử như citation hỏng hôm nay (rút lại + lời báo + "Thử lại")
        trace.citation_error = CitationIntegrityError("itinerary check failed: " + ",".join(loi))
    if flags is not None and flags.thoi_tiet:
        _thoi_tiet_cuoi(trace, text)


def lich_cho_giao_dien(trace: AnswerTrace, flags: AssistantFlags, cau_goc: str) -> dict | None:
    """D11 + D12 (a): dữ liệu có cấu trúc cho giao diện khi lượt có lịch — link bản đồ (code dựng) + thẻ "Sửa" chọn sẵn tham số đã dùng
    (`cau_goc` = câu người dùng gõ, không phải câu ghép; "Gửi" của thẻ = câu ghép B4 D4). Lịch bản 2 ⇒ khung + câu cuối (giao diện vẽ từ khung)."""
    if trace.lich_v2 is not None:
        v = trace.lich_v2
        return {"phien_ban": 2, "lich": v["lich"], "cau": v["cau"], "so_cau_du_phong": v.get("so_cau_du_phong")}
    if trace.lich is None:
        return None
    khung = trace.lich["khung"]
    ts = khung["tham_so"]
    sua = the_hoi_lai("lich_trinh", list(TRUONG_THEO_LOAI["lich_trinh"]), cau_goc)
    sua["chon"] = {k: ts[k] for k in TRUONG_THEO_LOAI["lich_trinh"] if ts[k] and not (k == "so_ngay" and ts["so_ngay_tam"])}
    return {"ban_do": lt.ban_do(flags.bang_lich, khung, flags.toa_do_lich if flags.ban_do_lich else None), "sua": sua}


async def answer_query(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, recorder=None,
                       today: str | None = None, flags: AssistantFlags | None = None) -> None:
    """Tuyến `tro_ly_hue` không stream: lần tìm đầu (theo `flags.lan_tim_dau`) → sinh một lần, hoặc trợ lý có công cụ (`flags.uses_tools`)
    → `check_citations`, điền `trace`. Lỗi đi ra nguyên kiểu như `prepare_answer`, thêm `GenerationError` (sinh); lỗi tìm trong công cụ
    ra đúng lỗi gốc."""
    flags = flags or AssistantFlags()
    tool_prompt = await _before_model(query, retrieval_service, context_builder, generator, trace, recorder, today, flags)
    if trace.fixed_outcome is not None:
        return

    started = time.perf_counter()
    call_log = CallLog()
    try:
        if flags.uses_tools:
            instructions = _assistant_instructions(generator, trace)
            tool_fn = tool_for_turn(query, retrieval_service, context_builder, trace, today, instructions)
            extra = _lich_extra(query, retrieval_service, context_builder, trace, today, instructions, flags)
            try:
                trace.generated = await generator.generate_with_tools(tool_prompt, tool_fn, call_log, **_history_kwargs(trace), **extra)
            except GenerationError:
                if trace.tool_error is not None:
                    raise trace.tool_error from None
                raise
        else:
            # `today` chỉ truyền khi có: generator thay thế trong test route chỉ nhận (query, context)
            kwargs = {"call_log": call_log} if today is None else {"call_log": call_log, "today": today}
            trace.generated = await generator.generate_answer(query, trace.packed.text, **kwargs, **_history_kwargs(trace))
    finally:
        trace.generation_ms = elapsed_ms(started)  # có cả khi model lỗi (route log `generation_failed` kèm thời gian)
        record_llm_calls(trace, call_log.calls, ROUTE_TRO_LY_HUE)  # cả khi lượt lỗi sau phản hồi (review C128 m-1)
    if recorder:
        recorder.record_generation_result(trace.generated)
    _finish_generated(trace, flags)


def _lich_extra(query, retrieval_service, context_builder, trace, today, instructions, flags) -> dict:
    """Cờ `lich_trinh` bật ⇒ công cụ thứ hai cho generator; B5b: cờ `thoi_tiet` bật ⇒ code dò ngữ cảnh thời tiết của câu, và **chỉ khi** câu cuối /
    câu hỏi liền trước có từ khoá ⇒ thêm công cụ `thoi_tiet` (D4). Cờ tắt ⇒ {} (generator gọi y như trước — Q1)."""
    extra = {}
    if flags.lich_trinh:
        extra["lich_trinh_fn"] = lich_trinh_for_turn(query, retrieval_service, context_builder, trace, today, instructions, flags.bang_lich,
                                                     flags.du_bao if flags.thoi_tiet else None)
    if flags.thoi_tiet:
        tu_khoa, ngoai_7 = tt.co_tu_khoa_luot(query, trace.history), tt.ngoai_7_ngay(query, hom_nay_vn())
        # vòng chỉnh 1 (A duyệt, sửa D3): câu ngoài 7 ngày ⇒ KHÔNG đưa công cụ (không số dự báo nào để model chép) — code nối câu cố định
        trace.thoi_tiet_ctx = {"bao_lu": tt.la_cau_bao_lu(query), "ngoai_7": ngoai_7, "buoi": tt.co_buoi(query), "tu_khoa": tu_khoa,
                               "co_cong_cu": tu_khoa and not ngoai_7}
        if trace.thoi_tiet_ctx["co_cong_cu"]:
            extra["thoi_tiet_fn"] = thoi_tiet_for_turn(trace, flags.du_bao)
    if flags.ngay_lich and nl.co_tu_ngay_luot(query, trace.history):  # T1: như thời tiết — lượt không có từ chỉ ngày ⇒ danh sách công cụ như cũ (Q1)
        extra["ngay_lich_fn"] = ngay_lich_for_turn(trace, query)
    if flags.het_luot_bo_cong_cu:  # hết lượt tìm thật ⇒ generator ẩn `tim_kho` ở lượt gọi model kế tiếp (cờ tắt ⇒ không truyền, gọi y như trước)
        extra["con_luot_fn"] = lambda: trace.model_searches < MODEL_SEARCH_LIMIT
    return extra


# ---------- Biểu mẫu "Lên kế hoạch" (cổng đợt 1, spec D3) ----------

async def _xep_bieu_mau(query: str, retrieval_service, context_builder, trace: AnswerTrace, flags: AssistantFlags, today: str | None) -> str:
    """D3: **code** gọi `lich_trinh` với giá trị nút ở cả 4 trường (không định tuyến, model không chọn công cụ, không lần tìm đầu). Trả ngữ cảnh
    cho lần sinh không công cụ = đúng chuỗi công cụ trả ở đường câu tự do (chữ khung có `LICH_TRINH_LUAT` + đoạn nguồn của các điểm).
    `instructions=None`: ngân sách đếm như đường sinh một lần (lời dặn trả lời) — đúng lần gọi của lượt này."""
    t = trace.truong
    lich_trinh = lich_trinh_for_turn(query, retrieval_service, context_builder, trace, today, None, flags.bang_lich,
                                     flags.du_bao if flags.thoi_tiet else None)
    return await lich_trinh(t["so_ngay"], t.get("di_cung"), t.get("kieu_di"), t.get("so_thich"), None)


async def answer_bieu_mau(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags) -> None:
    """Lượt biểu mẫu không stream (`POST /api/chat`): code xếp ⇒ một lần sinh **không công cụ** bằng agent biểu mẫu (luật lịch trong lời dặn +
    mức suy luận thấp — V5 X1c) ⇒ kiểm như lượt có lịch (`_finish_generated`).
    Lỗi tìm / ngữ cảnh / sinh đi ra nguyên kiểu như `answer_query`."""
    if generator is None:
        raise GeneratorNotReadyError("generator is not ready")
    today = _today(flags, trace)
    if flags.len_ke_hoach_v2:  # bản 2: khung + câu theo mục (`llm/len_ke_hoach.py`); cờ tắt ⇒ đường dưới y như cũ
        from llm import len_ke_hoach  # import muộn: module đó import lõi này
        await len_ke_hoach.answer_v2(query, retrieval_service, context_builder, generator, trace, flags, today)
        set_notice(trace, flags)
        return
    context = await _xep_bieu_mau(query, retrieval_service, context_builder, trace, flags, today)
    started = time.perf_counter()
    call_log = CallLog()
    try:
        trace.generated = await generator.generate_answer(query, context, today=today, call_log=call_log, bieu_mau=True,
                                                          **_history_kwargs(trace))
    finally:
        trace.generation_ms = elapsed_ms(started)
        record_llm_calls(trace, call_log.calls, ROUTE_TRO_LY_HUE)
    _finish_generated(trace, flags)
    set_notice(trace, flags)


# ---------- Một lượt có định tuyến (Phase 9 B1, plan D1, D6) ----------

def _set_fixed(trace: AnswerTrace, text: str, outcome: str) -> None:
    trace.answer, trace.cited, trace.fixed_outcome = text, (), outcome


async def _pick_route(query: str, generator, trace: AnswerTrace, flags: AssistantFlags) -> None:
    """Định tuyến (model) ⇒ câu cố định cho `ngoai_pham_vi`; `khan_cap` đi agent Huế (phương án B của bậc G, spec bản 13 §12.2: bỏ câu soạn sẵn
    khẩn cấp, giữ 4 tuyến). Còn lại để `trace.route` cho bước sau."""
    if flags.router and generator is not None:
        started = time.perf_counter()
        call_log = CallLog()
        try:
            if flags.lan_tim_dau in ("v1", "v3"):  # B2 D2: định tuyến viết luôn câu tìm (cùng một lần gọi)
                trace.route, queries = await generator.route_search(query, call_log, flags.lan_tim_dau)
                trace.cau_tim = [q.strip() for q in queries if q.strip()] or None
                trace.cau_tim_rong = trace.cau_tim is None  # rỗng ⇒ tìm bằng câu gốc, đếm được
            else:
                trace.route = await generator.route(query, call_log, **_history_kwargs(trace))
        except GenerationError:
            trace.route, trace.route_error = ROUTE_TRO_LY_HUE, "router_failed"  # lỗi ⇒ đường cũ (D3)
        finally:
            trace.routing_ms = elapsed_ms(started)
            record_llm_calls(trace, call_log.calls, "router")
    if trace.route == ROUTE_KHAN_CAP:  # phương án B G: không câu soạn sẵn — trả lời như câu về Huế; log giữ dấu định tuyến đã chọn khẩn cấp
        trace.route, trace.emergency_by = ROUTE_TRO_LY_HUE, "router"
    elif trace.route == ROUTE_NGOAI_PHAM_VI:
        _set_fixed(trace, OUT_OF_SCOPE_ANSWER, "out_of_scope")


def _today(flags: AssistantFlags, trace: AnswerTrace) -> str | None:
    trace.today = today_line() if flags.today_line else None
    return trace.today


# ---------- Cổng web (Phase 9 B6, plan B6 bản 3 D1–D9) ----------

def web_gate_open(trace: AnswerTrace, flags: AssistantFlags, tim_web) -> bool:
    """D1 — luật mở cổng, **một chỗ** cho cả 3 đường: câu trả lời kho đúng bằng câu từ chối "không đủ thông tin" (so sau `strip()` như cờ
    `refusal`; không mở với câu ngoài phạm vi) ∧ outcome thường (model tự từ chối, hoặc ngữ cảnh rỗng `refusal_no_sources`) — không chạm trần,
    không lỗi công cụ, không hỏi lại ∧ tuyến `tro_ly_hue` (khẩn cấp / ngoài phạm vi / trò chuyện không mở) ∧ chưa tra ∧ lượt không có lịch ∧
    không phải lượt ghép từ nút (D8) ∧ cờ bật ∧ nơi gọi có hàm tra (bộ đánh giá không truyền ⇒ không tra)."""
    return (flags.tra_web and tim_web is not None and trace.web is None and trace.route == ROUTE_TRO_LY_HUE
            and trace.fixed_outcome in (None, "refusal_no_sources") and trace.citation_error is None and trace.tool_error is None
            and trace.clarify is None and trace.lich is None and trace.truong is None
            and (trace.answer or "").strip() == INSUFFICIENT_ANSWER)


async def cong_web(query: str, generator, trace: AnswerTrace, tim_web) -> None:
    """Sau khi cổng mở: truy vấn do code dựng từ câu hỏi lượt này (D2) ⇒ một lần tra (D3) ⇒ một lần gọi model riêng viết mục web (D4) ⇒ kiểm
    cuối (D5). Kết quả vào `trace.web`; câu trả lời kho (`trace.answer`) giữ nguyên. Tra lỗi / 0 kết quả / model lỗi / kiểm hỏng ⇒ câu cố định
    (không đoán, không thử lại). Lần tra ghi một mục `tools` (ms, trạng thái, số kết quả, USD — không chữ)."""
    kq = await tim_web(tw.cau_tim_web(query))
    trace.tools.append({"name": "tra_web", "ms": kq.ms, "trang_thai": kq.trang_thai, "loi": kq.loi, "n_ket_qua": len(kq.so_web),
                        "usd": kq.usd})
    web = {"outcome": "web_loi", "text": tw.WEB_LOI_TEXT, "nguon": [], "n_ket_qua": len(kq.so_web), "n_ma": 0, "kiem": None,
           "usd_serper": kq.usd}
    trace.web = web
    if kq.trang_thai == "rong":
        web.update(outcome="web_rong", text=tw.WEB_RONG_TEXT)
    if kq.trang_thai != "ok":
        return
    if tw.la_cau_thien_tai(query):  # vòng chỉnh 1: câu thiên tai ⇒ không gọi model; câu cố định (NCHMF / chính quyền / 112) + link nguồn do code
        web.update(outcome="thien_tai", text=tw.THIEN_TAI_TEXT, nguon=list(kq.so_web))
        return
    call_log = CallLog()
    try:
        generated = await generator.generate_web_section(tw.dau_vao_model(query, kq.so_web), call_log)
    except GenerationError:
        web["kiem"] = ["model_loi"]
        return
    finally:
        record_llm_calls(trace, call_log.calls, "tra_web")
    loi = tw.kiem_muc_web(generated.text, kq.so_web, tw.la_cau_luu_tru(query), tw.la_cau_thoi_gian_thuc(query))
    web["kiem"] = loi
    if loi == ["so_thoi_gian_thuc"]:  # vòng chỉnh 1: câu thời gian thực có số / ngày giờ ⇒ câu cố định "chưa xác minh" + link nguồn
        web.update(outcome="chua_xac_minh", text=tw.CHUA_XAC_MINH_TEXT, nguon=list(kq.so_web))
        return
    if loi:  # D5 (iv): bỏ mục model viết, giữ câu từ chối của kho + câu cố định
        web.update(outcome="khong_tin_cay", text=tw.WEB_KHONG_TIN_CAY_TEXT)
        return
    ma = tw.ma_da_dung(generated.text)
    web.update(outcome="co_muc", text=generated.text.strip(), n_ma=len(ma),
               nguon=[s for s in kq.so_web if s["id"] in ma])  # chỉ nguồn được trích, đúng số w n của sổ


async def _web_stream(query: str, generator, trace: AnswerTrace, flags: AssistantFlags, tim_web):
    """Đường stream: cổng mở ⇒ trạng thái "đang tra web…" rồi tra. Mục web không stream từng chữ — phải kiểm cuối (D5) trước khi hiện; route
    gửi cả mục một sự kiện `web` sau `sources`."""
    if web_gate_open(trace, flags, tim_web):
        yield "status", {"stage": "tra_web"}
        await cong_web(query, generator, trace, tim_web)


async def answer_turn(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags,
                      recorder=None, tim_web=None) -> None:
    """Một lượt không stream (`POST /api/chat`, `answer_case`): luật khẩn cấp ⇒ định tuyến ⇒ trả lời theo tuyến ⇒ cổng web (B6; `tim_web` do route
    truyền, None ⇒ không tra). Lỗi như `answer_query`. Lượt biểu mẫu (D3) ⇒ `answer_bieu_mau` (không định tuyến, không web)."""
    if trace.bieu_mau:
        await answer_bieu_mau(query, retrieval_service, context_builder, generator, trace, flags)
        return
    await _pick_route(query, generator, trace, flags)
    if trace.fixed_outcome is not None:
        return
    if trace.route == ROUTE_TRO_CHUYEN:
        started = time.perf_counter()
        call_log = CallLog()
        try:
            trace.generated = await generator.generate_chat(query, call_log, **_history_kwargs(trace))
        finally:
            trace.generation_ms = elapsed_ms(started)
            record_llm_calls(trace, call_log.calls, ROUTE_TRO_CHUYEN)
        trace.answer, trace.cited = trace.generated.text, ()  # trò chuyện không có sổ nguồn, không kiểm citation (D4)
        return
    await answer_query(query, retrieval_service, context_builder, generator, trace, recorder, _today(flags, trace), flags)
    set_notice(trace, flags)
    if web_gate_open(trace, flags, tim_web):
        await cong_web(query, generator, trace, tim_web)


async def answer_turn_stream(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags,
                             recorder=None, tim_web=None):
    """Cùng thứ tự `answer_turn` nhưng phát sự kiện: `("status", dict)` / `("delta", str)`. Kết thúc ⇒ `trace` đủ để route dựng `sources` /
    `error` / `notice` / `done`. Hạn giờ model bọc cả vòng đọc (spec streaming §4.3); tự dừng đọc (hết giờ / ngắt) ⇒ `cancel()` + đọc nốt
    trong vùng che (spec §4.5). Lỗi đi ra nguyên kiểu (route đổi thành sự kiện `error`)."""
    result = call_log = tool_state = None
    pending_generating = False
    cong_cu = None  # tên công cụ của lần gọi đang chạy (gọi lần lượt, `parallel_tool_calls=False`) — B5 D14 (b): mỗi công cụ một loại trạng thái
    da_phat_buoc = 0  # số bước `trace.buoc_lich` đã phát
    da_noi_dau = False  # D12 (a): dòng "Mình hiểu" đi liền trước chữ đầu của model
    giu_chu: str | bool | None = None  # review C M-1: None = chưa có chữ; "" / chuỗi = đang giữ; False = không giữ
    call_route = None
    # Việc nhỏ (12) 08/11 — review streaming 31/10 m-1: huỷ theo "luồng model còn sống" thay vì liệt kê lỗi. Mọi cách rời vòng đọc khi luồng chưa
    # hết (hết giờ, người dùng ngắt, lỗi trong code của mình) ⇒ `cancel()`; luồng tự hết hoặc chính luồng báo lỗi (lần chạy đã dừng) ⇒ không.
    stream_live = False
    try:
        if not trace.bieu_mau:  # D3: lượt biểu mẫu không định tuyến
            if flags.router and generator is not None:
                yield "status", {"stage": "routing"}
            await _pick_route(query, generator, trace, flags)
            if trace.fixed_outcome is not None:
                yield "delta", trace.answer
                return
        if trace.bieu_mau:
            # D3: code xếp ngay (bước tiến độ như đường công cụ — D14) rồi một lần sinh không công cụ; phần sau vòng đọc dùng chung
            # (giữ chữ khi còn có thể là câu từ chối, dòng "Mình hiểu", kiểm cuối, khối ghi chú)
            if generator is None:
                raise GeneratorNotReadyError("generator is not ready")
            if flags.len_ke_hoach_v2:  # bản 2: sự kiện lich_khung / lich_cau / lich_xong (`llm/len_ke_hoach.py`); cờ tắt ⇒ y như cũ
                from llm import len_ke_hoach
                async for event in len_ke_hoach.stream_v2(query, retrieval_service, context_builder, generator, trace, flags, _today(flags, trace)):
                    yield event
                set_notice(trace, flags)
                return
            yield "status", {"stage": "lich_trinh", "buoc": "dang_xep"}
            today = _today(flags, trace)
            context = await _xep_bieu_mau(query, retrieval_service, context_builder, trace, flags, today)
            for buoc in trace.buoc_lich:
                yield "status", {"stage": "lich_trinh", **buoc}
            yield "status", {"stage": "generating"}
            call_route = ROUTE_TRO_LY_HUE
            result, call_log = generator.start_answer_stream(query, context, today, bieu_mau=True, **_history_kwargs(trace))
        elif trace.route == ROUTE_TRO_CHUYEN:
            yield "status", {"stage": "generating"}
            call_route = ROUTE_TRO_CHUYEN
            result, call_log = generator.start_chat_stream(query, **_history_kwargs(trace))
        else:
            today = _today(flags, trace)
            tool_prompt = await _before_model(query, retrieval_service, context_builder, generator, trace, recorder, today, flags)
            if trace.packed is not None:  # V2 không tìm trước (B2 D5): `searching` / `searched` đến từ lần gọi công cụ
                yield "status", {"stage": "searched", "n_sources": len(trace.packed.sources)}
            if trace.fixed_outcome is not None:  # ngữ cảnh không có nguồn ⇒ từ chối, không gọi model
                yield "delta", trace.answer
                async for event in _web_stream(query, generator, trace, flags, tim_web):  # B6: đúng ca "kho không có"
                    yield event
                return
            call_route = ROUTE_TRO_LY_HUE
            if flags.uses_tools:
                # B3 D9 (b): vòng công cụ ⇒ "đang viết" phát ngay trước chữ đầu (không trước các lượt `tim_kho`)
                pending_generating = True
                instructions = _assistant_instructions(generator, trace)
                tool_fn = tool_for_turn(query, retrieval_service, context_builder, trace, today, instructions)
                extra = _lich_extra(query, retrieval_service, context_builder, trace, today, instructions, flags)
                result, call_log, tool_state = generator.start_tools_stream(tool_prompt, tool_fn, **_history_kwargs(trace), **extra)
            else:
                yield "status", {"stage": "generating"}
                result, call_log = generator.start_answer_stream(query, trace.packed.text, trace.today, **_history_kwargs(trace))

        started, generator_started = time.perf_counter(), time.monotonic()
        extractor = AnswerTextStream()
        events = result.stream_events()
        stream_live = True
        deadline = asyncio.get_running_loop().time() + generator.timeout
        try:
            while True:
                try:
                    async with asyncio.timeout_at(deadline):
                        event = await anext(events)
                except StopAsyncIteration:
                    stream_live = False
                    break
                except TimeoutError:
                    raise
                except Exception:
                    stream_live = False  # lỗi của chính luồng (SDK / provider): lần chạy đã dừng, đọc nốt sẽ ném lại lỗi đó
                    raise
                if event.type == "raw_response_event" and event.data.type == "response.output_text.delta":
                    text = extractor.feed(event.data.delta)
                    if text:
                        if pending_generating:
                            pending_generating = False
                            yield "status", {"stage": "generating"}
                        if giu_chu is None:  # review C M-1: đã có dự báo / khung lịch (B171 T3) ⇒ giữ chữ chừng nào còn có thể là câu từ chối
                            giu_chu = "" if (flags.thoi_tiet and trace.thoi_tiet and trace.thoi_tiet["khoi"]) or trace.lich is not None else False
                        if giu_chu is not False:
                            giu_chu += text
                            if INSUFFICIENT_ANSWER.startswith(giu_chu.lstrip()):
                                continue
                            text, giu_chu = giu_chu, False
                        if trace.lich is not None and not da_noi_dau:
                            da_noi_dau = True
                            text = f"{lt.dong_minh_hieu(trace.lich['khung'])}\n\n{text}"
                        yield "delta", text
                elif event.type == "run_item_stream_event" and event.name == "tool_called":  # thẻ công cụ (B2 D7): lượt gọi không có chữ
                    cong_cu = getattr(getattr(event.item, "raw_item", None), "name", None)
                    if cong_cu == "lich_trinh":  # D14: "đang xếp lịch…" khi code bắt đầu chạy — không phát "đang tìm" (m-6)
                        yield "status", {"stage": "lich_trinh", "buoc": "dang_xep"}
                    elif cong_cu == "thoi_tiet":  # B5b: "đang xem dự báo…" (không phải "đang tìm kho")
                        yield "status", {"stage": "thoi_tiet"}
                    elif cong_cu == "ngay_lich":  # T1: tính ngày ở code, tức thì — không báo "đang tìm kho" (giữ trạng thái đang có)
                        pass
                    else:
                        yield "status", {"stage": "searching"}
                elif event.type == "run_item_stream_event" and event.name == "tool_output":
                    if cong_cu == "lich_trinh":  # D14 (b): phát các bước code vừa làm xong, đúng thứ tự
                        for buoc in trace.buoc_lich[da_phat_buoc:]:
                            yield "status", {"stage": "lich_trinh", **buoc}
                        da_phat_buoc = len(trace.buoc_lich)
                    elif cong_cu not in ("thoi_tiet", "ngay_lich"):  # B5b / T1: kết quả dự báo / ngày không phải "đã tìm kho"
                        yield "status", {"stage": "searched", "n_sources": len(trace.so_nguon)}
        except Exception as exc:
            if trace.tool_error is not None:  # lỗi tìm trong công cụ: SDK có thể bọc lại ⇒ ném đúng lỗi gốc (route ra câu lỗi như B1)
                raise trace.tool_error from None
            # hết lượt tìm (cờ `het_luot_bo_cong_cu`): model vẫn xin `tim_kho` đã ẩn ⇒ không phải lỗi 500 — câu từ chối cố định như chạm `max_turns`
            if tool_state is None or not generator.xin_cong_cu_da_an(exc, tool_state):
                raise
        finally:
            trace.generation_ms = elapsed_ms(started)

        trace.generated = generator.finish_answer_stream(result, call_log, generator_started, tool_state)
        if call_route == ROUTE_TRO_CHUYEN:
            trace.answer, trace.cited = trace.generated.text, ()
        else:
            _finish_generated(trace, flags)
            if trace.fixed_outcome is not None:  # chạm `max_turns`: không có chữ model nào ⇒ câu từ chối thành một `delta` (B2 D5)
                if trace.answer:  # lượt hỏi lại: không chữ ⇒ route gửi `clarify`
                    yield "delta", trace.answer
                return
            if giu_chu:  # chữ giữ lại đến hết = câu từ chối (đã thay) hoặc một khúc đầu của nó
                yield "delta", _chu_giu_lai(trace, giu_chu, da_noi_dau)
            if trace.lich is not None and trace.citation_error is None and trace.lich["ghi_chu"]:
                yield "delta", f"\n\n{trace.lich['ghi_chu']}"  # D4b: khối ghi chú do code nối, sau phần model
            if trace.thoi_tiet_noi and trace.citation_error is None:
                yield "delta", f"\n\n{trace.thoi_tiet_noi}"  # B5b: khối số liệu / câu cố định do code nối, sau phần model
            set_notice(trace, flags)
            async for event in _web_stream(query, generator, trace, flags, tim_web):
                yield event
    finally:
        if call_log is not None:
            record_llm_calls(trace, call_log.calls, call_route)
        if result is not None and stream_live:
            # dừng lần gọi model rồi đọc nốt bằng iterator mới, trong vùng che có hạn giờ (spec streaming §4.5). Không dựa `result.is_complete`.
            result.cancel()
            drain_started = time.perf_counter()
            with anyio.CancelScope(shield=True):
                with anyio.move_on_after(STREAM_DRAIN_SECONDS) as drain_scope:
                    async for _ in result.stream_events():
                        pass
            logger.info("chat_stream_drain %s", json.dumps({"finished": not drain_scope.cancelled_caught,
                                                             "ms": elapsed_ms(drain_started)}))


def _chu_giu_lai(trace: AnswerTrace, giu: str, da_noi_dau: bool) -> str:
    """Stream: chữ model giữ lại tới hết ⇒ chữ phát ra — lời lịch code dựng (B171 T3) / câu dẫn dự báo (B5b M-1) / chính chữ đó; lượt có lịch
    chưa phát chữ nào ⇒ dòng "Mình hiểu" đi trước (D12 (a))."""
    if trace.lich is not None and trace.lich.get("chu_thay"):
        chu = trace.lich["chu_thay"]
    elif trace.thoi_tiet and trace.thoi_tiet.get("thay_tu_choi"):
        chu = tt.CAU_DAN_DU_BAO
    else:
        chu = giu
    return f"{lt.dong_minh_hieu(trace.lich['khung'])}\n\n{chu}" if trace.lich is not None and not da_noi_dau else chu


_SPEC_END = object()  # dấu hết hàng đợi của phần chạy trước (#6)
# Trường của trace do route đặt **trước** khi gọi lõi (chat.py `_start_conversation`, `_model_query`) — phần chạy trước phải nhận đủ (B161 M-1)
ROUTE_INPUTS = ("history", "truong", "search_query")


async def answer_turn_stream_parallel(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags,
                                      recorder=None, tim_web=None):
    """Thí nghiệm tốc độ #6 (plan `2026-11-04-phase-9-toc-do-song-song-plan.md`). Cờ `song_song_tra_loi` tắt (hoặc định tuyến không chạy /
    câu tìm do định tuyến viết) ⇒ đúng `answer_turn_stream`. Bật ⇒ (i) định tuyến và (ii) phần của tuyến `tro_ly_hue`
    chạy cùng lúc. (ii) chính là `answer_turn_stream` với `router` tắt trên **trace phụ** (đi thẳng lần tìm đầu câu gốc + lần gọi trợ lý —
    đầu vào hai lần gọi model không phụ thuộc tuyến). Sự kiện của (ii) giữ trong hàng đợi tới khi có tuyến:
    `tro_ly_hue` ⇒ xả hàng đợi, gộp trace phụ vào trace chính (D1); tuyến khác ⇒ huỷ (ii), bỏ trace phụ, đi đường của tuyến đó (D2, D3).
    B6: (ii) **không** tra web (chưa biết tuyến — câu trò chuyện không được ra Serper); cổng web chạy trên trace chính **sau khi gộp**."""
    if trace.bieu_mau or not (flags.song_song_tra_loi and flags.router and generator is not None and flags.lan_tim_dau == "v0"):
        # lượt biểu mẫu (cổng D3): không định tuyến ⇒ không có gì để chạy song song
        async for event in answer_turn_stream(query, retrieval_service, context_builder, generator, trace, flags, recorder, tim_web):
            yield event
        return

    # B6: bản cờ của phần chạy song song / đường trò chuyện tắt cả `tra_web` (cờ này cần `router`; cổng web chạy bằng `flags` gốc sau khi gộp)
    without_router = dataclasses.replace(flags, router=False, tra_web=False)
    # B161 M-1: trace phụ mang **mọi đầu vào route đặt trước khi gọi lõi** (lịch sử B3; giá trị nút + câu gốc của lượt ghép B4b / B5) — chép
    # từng trường (không `dataclasses.replace`: sẽ dùng chung list sổ nguồn / công cụ giữa hai trace)
    spec = AnswerTrace(**{name: getattr(trace, name) for name in ROUTE_INPUTS})
    queue: asyncio.Queue = asyncio.Queue()

    async def run_spec() -> None:
        try:
            async for event in answer_turn_stream(query, retrieval_service, context_builder, generator, spec, without_router):
                queue.put_nowait(event)
        finally:
            queue.put_nowait(_SPEC_END)

    yield "status", {"stage": "routing"}
    task = asyncio.create_task(run_spec())
    keep = merged = False
    finished_before_route = False
    try:
        await _pick_route(query, generator, trace, flags)
        keep = trace.route == ROUTE_TRO_LY_HUE and trace.fixed_outcome is None
        if keep:
            while (event := await queue.get()) is not _SPEC_END:
                yield event
            await task  # lỗi của (ii) đi ra nguyên kiểu như đường cũ
            _merge_spec(trace, spec, recorder)
            merged = True
            async for event in _web_stream(query, generator, trace, flags, tim_web):  # B6: sau khi gộp (tuyến đã chắc là `tro_ly_hue`)
                yield event
            return
        finished_before_route = task.done()
        task.cancel()  # huỷ ngay: lần gọi bị bỏ không giữ chữ đầu của tuyến khác (sàn KC)
        if trace.fixed_outcome is not None:
            yield "delta", trace.answer
            return
        # `tro_chuyen`: định tuyến đã xong ⇒ đường cũ của tuyến này, không định tuyến lại
        async for event in answer_turn_stream(query, retrieval_service, context_builder, generator, trace, without_router, recorder, tim_web):
            yield event
    finally:
        if not task.done():
            task.cancel()
        # Việc nhỏ (7) 08/11: người dùng ngắt ⇒ Starlette huỷ kiểu anyio (mọi lần chờ trong vùng bị huỷ lại) ⇒ không che thì `gather` bị huỷ, bỏ qua
        # bước gộp dưới ⇒ `chat_metrics` mất `llm_calls` / USD của (ii) (tái tạo: `data/phase_11/viec_nho_e/do_dung_song_song.py`).
        with anyio.CancelScope(shield=True):
            await asyncio.gather(task, return_exceptions=True)  # (ii) tự ghi `llm_calls` + đọc nốt trong `finally` của nó; lỗi của (ii) bị bỏ (D3)
        if keep and not merged:  # lỗi / ngắt trước khi gộp xong ⇒ gộp ở đây như trước B6
            _merge_spec(trace, spec, recorder)
        elif not keep:
            usd = sum(call["usd"] for call in spec.llm_calls)
            trace.n_tra_loi_bo, trace.bo_huy_giua = 1, not finished_before_route
            if trace.bo_huy_giua and spec.generation_ms is not None and spec.packed is not None:
                usd += cost_usd(spec.packed.input_tokens, 0)  # lần gọi bị huỷ không có usage ⇒ cận dưới (plan D2)
            trace.usd_bo = usd


def _merge_spec(trace: AnswerTrace, spec: AnswerTrace, recorder) -> None:
    """Tuyến `tro_ly_hue` ⇒ trace chính nhận mọi thứ (ii) đã làm; giữ phần định tuyến của trace chính; `llm_calls` = định tuyến rồi trả lời."""
    keep_own = {"route", "route_error", "routing_ms", "emergency_by", "llm_calls", *ROUTE_INPUTS}
    for item in dataclasses.fields(AnswerTrace):
        if item.name not in keep_own:
            setattr(trace, item.name, getattr(spec, item.name))
    trace.llm_calls = trace.llm_calls + spec.llm_calls
    if recorder and trace.packed is not None:  # như `prepare_answer` của đường cũ (recorder chỉ route truyền)
        recorder.record_packed_context(trace.packed)
        if trace.fixed_outcome == "refusal_no_sources":
            recorder.record_fallback()
