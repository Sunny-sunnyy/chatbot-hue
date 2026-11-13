"""Lượt biểu mẫu "Lên kế hoạch" bản 2 (cờ `len_ke_hoach_v2`) — bước (c) của plan `docs/superpowers/plans/2026-11-12-len-ke-hoach-dot-1-plan.md`
(spec bản 3.3 §5c.5, §5c.6).

Luồng: code xếp (`lich_trinh_v2.xep_v2`) ⇒ lấy một đoạn kho đúng file cho mỗi điểm (dùng lại phần lấy nguồn của đường cũ) ⇒ dựng `lich` ⇒
**phát khung trước lần gọi model** ⇒ một lần gọi model (không công cụ) chỉ viết `[{id_muc, cau}]` ⇒ kiểm TỪNG câu, câu lỗi / thiếu ⇒ câu dự phòng
của riêng mục đó ⇒ code ghép chữ thuần `answer` (lịch sử, nút chép, giao diện cũ). Model lỗi / hết giờ / sai khuôn ⇒ lịch vẫn đủ khung,
mọi mục dùng câu dự phòng (không rút cả lịch — khác đường cũ). Lõi (`assistant.py`) gọi vào đây khi cờ bật; cờ tắt ⇒ không chạm module này.
"""
import asyncio
import time
from collections import Counter

import anyio
from agents.exceptions import AgentsException
from openai import OpenAIError

from llm import lich_trinh_v2 as lt2
from llm.assistant import (STREAM_DRAIN_SECONDS, AnswerTrace, AssistantFlags, CallLog, GenerationError, GeneratorNotReadyError, ROUTE_TRO_LY_HUE,
                           _lay_nguon_lich, check_citations, elapsed_ms, record_llm_calls)

LOI_MODEL = (GenerationError, TimeoutError, AgentsException, OpenAIError)  # lỗi của lần gọi viết câu ⇒ câu dự phòng, lịch vẫn hiện


async def chuan_bi(query: str, retrieval_service, context_builder, trace: AnswerTrace, flags: AssistantFlags, today: str | None) -> str:
    """Xếp + lấy nguồn + dựng `lich` (lưu ở `trace.lich_v2`); trả tin nhắn gửi model. Lỗi tìm / ngữ cảnh đi ra nguyên kiểu như đường cũ."""
    bang = flags.bang_lich_v2
    ts = lt2.tu_truong(trace.truong)
    khung = lt2.xep_v2(bang, ts)
    nhap = lt2.tin_nhan_model(lt2.dung_lich(bang, khung, dict.fromkeys(lt2.diem_v2(khung), 0)), "")  # đếm ngân sách bằng bản nháp
    packed, nguon, _ = await _lay_nguon_lich(bang, khung, query, retrieval_service, context_builder, trace, today, None, nhap=nhap, lay_ve=False)
    lich = lt2.dung_lich(bang, khung, nguon, trace.truong.get("ngay_di"))
    trace.lich_v2 = {"lich": lich, "loi_khung": lt2.kiem_khung_v2(bang, khung), "cau": None, "loi_cau": None}
    trace.buoc_lich += [{"buoc": "xep_xong", "n_diem": len(lt2.diem_v2(khung))}, {"buoc": "lay_nguon", "n_doan": len(packed.sources)}]
    return lt2.tin_nhan_model(lich, packed.text)


def hoan_tat(trace: AnswerTrace, flags: AssistantFlags, cau: dict[str, str], loi: dict[str, str]) -> None:
    """Câu cuối ⇒ `answer` chữ thuần + kiểm citation trên sổ nguồn (mỗi dòng mang mã nguồn của điểm)."""
    trace.lich_v2.update(cau=cau, loi_cau=dict(Counter(loi.values())), so_cau_du_phong=len(loi))
    trace.answer = lt2.ghep_chu(trace.lich_v2["lich"], cau)
    check_citations(trace)


async def answer_v2(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags, today: str | None) -> None:
    """`POST /api/chat`: một lần gọi không stream."""
    if generator is None:
        raise GeneratorNotReadyError("generator is not ready")
    prompt = await chuan_bi(query, retrieval_service, context_builder, trace, flags, today)
    call_log, started = CallLog(), time.perf_counter()
    tu_model: list[dict] = []
    try:
        trace.generated, tu_model = await generator.generate_lich_v2(prompt, call_log)
    except LOI_MODEL as exc:
        trace.lich_v2["loi_model"] = type(exc).__name__
    finally:
        trace.generation_ms = elapsed_ms(started)
        record_llm_calls(trace, call_log.calls, ROUTE_TRO_LY_HUE)
    hoan_tat(trace, flags, *lt2.chon_cau(flags.bang_lich_v2, trace.lich_v2["lich"], tu_model))


async def stream_v2(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags, today: str | None):
    """`POST /api/chat/stream`: sự kiện `("lich_khung", lich)` ngay sau khi code xếp xong (trước lần gọi model) ⇒ `("lich_cau", {id_muc, cau})`
    mỗi khi model đóng một phần tử (câu đã qua kiểm, hoặc câu dự phòng) ⇒ câu dự phòng cho mục còn thiếu ⇒ `("lich_xong", {so_cau_du_phong})`
    ⇒ một `("delta", answer)` chữ thuần. Huỷ / đọc nốt lần gọi model như đường cũ (spec streaming §4.5)."""
    if generator is None:
        raise GeneratorNotReadyError("generator is not ready")
    yield "status", {"stage": "lich_trinh", "buoc": "dang_xep"}
    prompt = await chuan_bi(query, retrieval_service, context_builder, trace, flags, today)
    bang, lich = flags.bang_lich_v2, trace.lich_v2["lich"]
    muc = {m["id_muc"]: m for m in lt2.moi_muc(lich)}
    yield "lich_khung", lich
    yield "status", {"stage": "generating"}
    result, call_log = generator.start_lich_v2_stream(prompt)
    started, generator_started = time.perf_counter(), time.monotonic()
    da_phat: dict[str, str] = {}
    loi: dict[str, str] = {}
    extractor = lt2.CauStream()
    stream_live = True
    try:
        events = result.stream_events()
        deadline = asyncio.get_running_loop().time() + generator.timeout
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
                stream_live = False
                raise
            if event.type == "raw_response_event" and event.data.type == "response.output_text.delta":
                for x in extractor.feed(event.data.delta):
                    id_muc = x.get("id_muc")
                    if id_muc in muc and id_muc not in da_phat:  # lặp id ⇒ phần tử đầu; id lạ ⇒ bỏ
                        ma = lt2.kiem_cau(bang, muc[id_muc], x.get("cau") or "")
                        da_phat[id_muc] = lt2.cau_du_phong(bang, muc[id_muc]) if ma else x["cau"].strip()
                        if ma:
                            loi[id_muc] = ma
                        yield "lich_cau", {"id_muc": id_muc, "cau": da_phat[id_muc]}
        trace.generated, _ = generator.finish_lich_v2_stream(result, call_log, generator_started)  # khuôn sai ⇒ lỗi ⇒ dự phòng phần còn lại
    except LOI_MODEL as exc:
        trace.lich_v2["loi_model"] = type(exc).__name__
    finally:
        trace.generation_ms = elapsed_ms(started)
        record_llm_calls(trace, call_log.calls, ROUTE_TRO_LY_HUE)
        if stream_live:  # rời vòng đọc khi luồng còn sống (hết giờ, ngắt, lỗi của code mình) ⇒ huỷ + đọc nốt trong vùng che có hạn giờ
            result.cancel()
            with anyio.CancelScope(shield=True):
                with anyio.move_on_after(STREAM_DRAIN_SECONDS):
                    async for _ in result.stream_events():
                        pass
    for id_muc, m in muc.items():  # mục model không trả (hoặc lần gọi lỗi) ⇒ câu dự phòng, vẫn đúng thứ tự khung ở phía giao diện (theo id_muc)
        if id_muc not in da_phat:
            da_phat[id_muc], loi[id_muc] = lt2.cau_du_phong(bang, m), "thieu"
            yield "lich_cau", {"id_muc": id_muc, "cau": da_phat[id_muc]}
    hoan_tat(trace, flags, {k: da_phat[k] for k in muc}, loi)
    yield "lich_xong", {"so_cau_du_phong": len(loi)}
    yield "delta", trace.answer
