"""Lượt biểu mẫu "Lên kế hoạch" bản 2 (cờ `len_ke_hoach_v2`) — bước (c) của plan `docs/superpowers/plans/2026-11-12-len-ke-hoach-dot-1-plan.md`
(spec bản 3.3 §5c.5, §5c.6).

Luồng: code xếp (`lich_trinh_v2.xep_v2`) ⇒ lấy một đoạn kho đúng file cho mỗi điểm (dùng lại phần lấy nguồn của đường cũ) ⇒ dựng `lich` ⇒
**phát khung trước lần gọi model** ⇒ một lần gọi model (không công cụ) chỉ viết `[{id_muc, cau}]` ⇒ kiểm TỪNG câu, câu lỗi / thiếu ⇒ câu dự phòng
của riêng mục đó ⇒ code ghép chữ thuần `answer` (lịch sử, nút chép, giao diện cũ). Model lỗi / hết giờ / sai khuôn ⇒ lịch vẫn đủ khung,
mọi mục dùng câu dự phòng (không rút cả lịch — khác đường cũ). Lõi (`assistant.py`) gọi vào đây khi cờ bật; cờ tắt ⇒ không chạm module này.
"""
import asyncio
import datetime as dt
import time
from collections import Counter

import anyio
from agents.exceptions import AgentsException
from openai import OpenAIError

from llm import lich_trinh_v2 as lt2
from llm import sua_lich_v2 as sl
from llm import thoi_tiet as tt
from llm.citations import CITATION_PATTERN
from llm.assistant import (STREAM_DRAIN_SECONDS, AnswerTrace, AssistantFlags, CallLog, GenerationError, GeneratorNotReadyError, ROUTE_TRO_LY_HUE,
                           _lay_nguon_lich, check_citations, elapsed_ms, record_llm_calls)

MAX_DOAN = lt2.TOI_DA_BUOI * 2 * lt2.SO_NGAY_TOI_DA + lt2.SO_NGAY_TOI_DA  # một đoạn mỗi điểm: ≤ 4 điểm ban ngày + 1 tối × 5 ngày = 25
TIM_MO_TA = "tổng quan kiến trúc cảnh quan"  # vòng chỉnh nghiệm thu 13/11 (A chọn (a)): chọn đoạn TẢ điểm cho câu "ở đây có gì"
LOI_MODEL = (GenerationError, TimeoutError, AgentsException, OpenAIError)  # lỗi của lần gọi viết câu ⇒ câu dự phòng, lịch vẫn hiện


async def du_bao_lich(flags: AssistantFlags, bat_dau: dt.date | None, n: int, trace: AnswerTrace, hom_nay: dt.date) -> dict | None:
    """5c.2: ngày đi có ít nhất một ngày trong 7 ngày tới (dự báo đang dùng) ⇒ MỘT lần lấy dự báo (cache 30 phút) ⇒ {ngày: dict ngày}; không
    ngày đi / mọi ngày ngoài 7 ngày ⇒ không gọi mạng; lỗi / tắt ⇒ None (xếp như không có dự báo, không dòng dự báo)."""
    if bat_dau is None or not flags.thoi_tiet or flags.du_bao is None:
        return None
    if not any(0 <= (bat_dau + dt.timedelta(days=k) - hom_nay).days < tt.SO_NGAY for k in range(n)):
        return None
    kq = await flags.du_bao()
    trace.tools.append({"name": "thoi_tiet", "ms": kq.ms, "by": "code", "trang_thai": kq.trang_thai, "loi": kq.loi})
    if kq.trang_thai != "ok":
        return None
    return {"ngay": {d["ngay"]: d for d in kq.ngay}, "nguon": tt.dong_nguon(kq)}


def dong_du_bao(bang, khung: dict, db: dict | None) -> list[dict]:
    """Dòng dự báo theo ngày của lịch (số do code in) + "Nếu mưa" cho điểm ưu tiên ngoài trời đã giữ chỗ (5c.2) + dòng nguồn.
    Mỗi dòng `{"cau", "ngay"}` — `ngay` = số ngày của lịch để giao diện đặt dòng đúng chỗ, không bóc chữ (giao diện mới 14/11); dòng nguồn không có `ngay`."""
    if db is None:
        return []
    dong, T = [], bang.theo_id
    for ng, ngay in zip(khung["ngay"], khung["ngay_thang"]):
        d = db["ngay"].get(dt.date.fromisoformat(ngay)) if ngay else None
        if d is None:
            continue
        dong.append({"cau": f"Ngày {ng['ngay']} — {tt.dong_ngay(d)}.", "ngay": ng["ngay"]})
        if d["xs"] is not None and d["xs"] >= lt2.NGUONG_MUA:
            dong.append({"cau": dong_neu_mua(bang, khung, ng), "ngay": ng["ngay"]})
    return dong + [{"cau": db["nguon"]}] if dong else []


def dong_neu_mua(bang, khung: dict, ng: dict) -> str:
    """Ngày dự báo mưa ≥ ngưỡng ⇒ LUÔN đúng một dòng "Nếu mưa" (review 14/11, thước ý 6): có điểm ngoài trời thay được ⇒ gợi ý thay; ngoài trời
    không có điểm thay ⇒ nói thẳng; không điểm ngoài trời ⇒ nói các điểm có chỗ trong nhà."""
    T = bang.theo_id
    ngoai = [j for b in lt2.BUOI_NGAY for j in ng["buoi"][b] if T[j]["trong_nha"] == "ngoai_troi"]
    for j in ngoai:
        thay = next((x["id"] for x in bang.diem if x["trong_nha"] in ("trong_nha", "ca_hai") and x["cum"] == T[j]["cum"]
                     and x["id"] not in lt2.diem_v2(khung) and set(x["buoi"]) & set(lt2.BUOI_NGAY)), None)
        if thay is not None:
            return f"Nếu mưa ngày {ng['ngay']}: có thể thay {T[j]['ten']} bằng {T[thay]['ten']} (trong nhà)."
    if ngoai:
        return f"Nếu mưa ngày {ng['ngay']}: {T[ngoai[0]]['ten']} ở ngoài trời và gần đó chưa có điểm trong nhà để thay — mang áo mưa hoặc đổi ngày."
    return f"Nếu mưa ngày {ng['ngay']}: các điểm trong ngày đều trong nhà hoặc có phần trong nhà, vẫn đi được — nhớ mang áo mưa."


async def chuan_bi(query: str, retrieval_service, context_builder, trace: AnswerTrace, flags: AssistantFlags, today: str | None,
                   sua: dict | None = None) -> str:
    """Xếp + lấy nguồn + dựng `lich` (lưu ở `trace.lich_v2`); trả tin nhắn gửi model. Lỗi tìm / ngữ cảnh đi ra nguyên kiểu như đường cũ.
    Sửa lịch (plan 2026-11-14-sua-lich-v2): `sua` = {khung, ngay_di, thay_doi, cau_cu} ⇒ KHÔNG xếp lại (khung code đã áp), lịch mang `thay_doi`;
    mục có câu cũ (`cau_cu` theo id điểm) giữ câu cũ (đánh lại số nguồn), tin nhắn gửi model chỉ còn mục mới."""
    bang = flags.bang_lich_v2
    ngay_di = sua["ngay_di"] if sua else trace.truong.get("ngay_di")
    bat_dau = dt.date.fromisoformat(ngay_di) if ngay_di else None
    khung = sua["khung"] if sua else None
    ts = lt2.tu_truong(trace.truong) if khung is None else None
    db = await du_bao_lich(flags, bat_dau, (ts.so_ngay if ts else khung["tham_so"]["so_ngay"]), trace, tt.hom_nay_vn())
    mua = None if db is None else {k: v["xs"] for k, v in db["ngay"].items() if v["xs"] is not None}
    if khung is None:
        khung = lt2.xep_v2(bang, ts, ngay_bat_dau=bat_dau, mua=mua)
    nhap = lt2.tin_nhan_model(lt2.dung_lich(bang, khung, dict.fromkeys(lt2.diem_v2(khung), 0)), "")  # đếm ngân sách bằng bản nháp
    chon = {j: bang.theo_id[j]["doan_mo_ta"] for j in dict.fromkeys(lt2.diem_v2(khung)) if bang.theo_id[j].get("doan_mo_ta")}
    co = await asyncio.to_thread(retrieval_service.lay_doan, list(chon.values())) if chon else {}
    doan_chon = {j: co[c] for j, c in chon.items() if c in co}  # khởi động đã kiểm đủ; vắng (không nên xảy ra) ⇒ luật tìm
    packed, nguon, _ = await _lay_nguon_lich(bang, khung, query, retrieval_service, context_builder, trace, today, None, nhap=nhap, lay_ve=False,
                                             max_doan=MAX_DOAN, tim_mo_ta=TIM_MO_TA, doan_chon=doan_chon)
    lich = lt2.dung_lich(bang, khung, nguon, ngay_di, dong_du_bao(bang, khung, db),
                         flags.toa_do_lich if flags.ban_do_lich else None, flags.anh_lich_bang if flags.anh_lich else None)
    giu_cau: dict[str, str] = {}
    if sua:
        lich["thay_doi"] = sua["thay_doi"]  # giao diện H1: khối "Đã đổi / Không đổi được" đầu thẻ (câu do code)
        lich["sua_ap"] = sua["sua_ap"]  # dữ liệu code (id, mã luật) — bộ đo so nhãn; không vào tin nhắn gửi model
        for m in lt2.moi_muc(lich):  # câu cũ đã kiểm của cùng điểm ⇒ giữ, chỉ đổi mã nguồn sang số mới của điểm đó
            cu = sua["cau_cu"].get(m["id_diem"])
            if cu and m["nguon"] is not None:
                giu_cau[m["id_muc"]] = CITATION_PATTERN.sub(f"[{m['nguon']}]", cu)
    trace.lich_v2 = {"lich": lich, "loi_khung": lt2.kiem_khung_v2(bang, khung), "cau": None, "loi_cau": None, "khung": khung,
                     "ngay_di": ngay_di, "mua": mua, "giu_cau": giu_cau}
    trace.buoc_lich += [{"buoc": "xep_xong", "n_diem": len(lt2.diem_v2(khung))}, {"buoc": "lay_nguon", "n_doan": len(packed.sources)}]
    moi = {**lich, "ngay": [{**ng, "muc": [m for m in ng["muc"] if m["id_muc"] not in giu_cau]} for ng in lich["ngay"]]}
    return lt2.tin_nhan_model(moi, packed.text)


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


async def stream_v2(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags, today: str | None,
                    sua: dict | None = None):
    """`POST /api/chat/stream`: sự kiện `("lich_khung", lich)` ngay sau khi code xếp xong (trước lần gọi model) ⇒ `("lich_cau", {id_muc, cau})`
    mỗi khi model đóng một phần tử (câu đã qua kiểm, hoặc câu dự phòng) ⇒ câu dự phòng cho mục còn thiếu ⇒ `("lich_xong", {so_cau_du_phong})`
    ⇒ một `("delta", answer)` chữ thuần. Huỷ / đọc nốt lần gọi model như đường cũ (spec streaming §4.5)."""
    if generator is None:
        raise GeneratorNotReadyError("generator is not ready")
    yield "status", {"stage": "lich_trinh", "buoc": "dang_xep"}
    prompt = await chuan_bi(query, retrieval_service, context_builder, trace, flags, today, sua)
    bang, lich = flags.bang_lich_v2, trace.lich_v2["lich"]
    giu_cau = trace.lich_v2["giu_cau"]
    muc = {m["id_muc"]: m for m in lt2.moi_muc(lich) if m["id_muc"] not in giu_cau}
    yield "lich_khung", lich
    da_phat: dict[str, str] = {}
    loi: dict[str, str] = {}
    for id_muc, cau in giu_cau.items():  # sửa lịch: mục không đổi ⇒ câu cũ ngay (không gọi model cho mục này)
        ma = lt2.kiem_cau(bang, next(m for m in lt2.moi_muc(lich) if m["id_muc"] == id_muc), cau)
        da_phat[id_muc] = cau if not ma else lt2.cau_du_phong(bang, next(m for m in lt2.moi_muc(lich) if m["id_muc"] == id_muc))
        yield "lich_cau", {"id_muc": id_muc, "cau": da_phat[id_muc]}
    if not muc:  # không còn mục mới (vd chỉ dời buổi) ⇒ không gọi model
        trace.lich_v2["loi_model"] = None
        yield "lich_xong", {"so_cau_du_phong": 0}
        hoan_tat(trace, flags, da_phat, loi)
        yield "delta", trace.answer
        return
    yield "status", {"stage": "generating"}
    result, call_log = generator.start_lich_v2_stream(prompt)
    started, generator_started = time.perf_counter(), time.monotonic()
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
    hoan_tat(trace, flags, dict(da_phat), loi)  # gồm cả câu cũ giữ lại của lượt sửa
    yield "lich_xong", {"so_cau_du_phong": len(loi)}
    yield "delta", trace.answer


# ---------- Sửa lịch bằng lời (plan 2026-11-14-sua-lich-v2) ----------

async def hieu_va_ap(query: str, generator, trace: AnswerTrace, flags: AssistantFlags) -> dict | None:
    """Câu người dùng ⇒ (một lần gọi hiểu ý) hành động có tên ⇒ code áp trên lịch đã lưu. Bấm nút thẻ chọn ⇒ không gọi model.
    Trả None khi không có gì để làm (danh sách rỗng, model lỗi, hoặc mọi hành động trượt vì tên lạ / không có trong lịch) ⇒ lõi đi đường thường."""
    bang, luu = flags.bang_lich_v2, trace.lich_luu
    if trace.sua_chon is not None:
        kq = sl.ap(bang, luu, [], sua_chon=trace.sua_chon)
    else:
        call_log = CallLog()
        try:
            hanh_dong = await generator.hieu_sua(sl.tin_nhan_hieu(bang, luu, query), call_log)
        except GenerationError:
            hanh_dong = []
        finally:
            record_llm_calls(trace, call_log.calls, "sua_lich")
        if not hanh_dong:
            trace.sua = {"n_hanh_dong": 0}
            return None
        kq = sl.ap(bang, luu, hanh_dong)
    trace.sua = {"n_hanh_dong": len(kq["da_ap"]) + len(kq["khong_doi"]) + len(kq["chua_lam"]), "n_ap": len(kq["da_ap"]) + len(kq["doi_truong"]),
                 "n_khong": len(kq["khong_doi"]), "the": kq["the"] is not None}
    if not kq["da_ap"] and kq["the"] is None and all(k["ma_luat"] in ("ngoai_bang", "khong_co_trong_lich") for k in kq["khong_doi"]):
        return None  # không chạm được gì trong lịch ⇒ có thể không phải câu sửa lịch
    return kq


async def stream_sua(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags, kq: dict):
    """Lượt sửa: thẻ chọn ⇒ một sự kiện `sua_the` (khung không đổi); còn lại ⇒ đúng luồng sự kiện lịch bản 2 trên khung code đã áp."""
    bang = flags.bang_lich_v2
    if kq["the"] is not None:
        trace.answer = f"Bạn muốn thay {kq['the']['ten_cu']} bằng điểm nào?"
        trace.fixed_outcome = "sua_the"
        yield "sua_the", {**kq["the"], "thay_doi": sl.thay_doi(bang, kq), "sua_ap": sl.sua_ap(kq)}
        yield "delta", trace.answer
        return
    luu = trace.lich_luu
    sua = {"khung": kq["khung"], "ngay_di": luu["ngay_di"], "thay_doi": sl.thay_doi(bang, kq), "cau_cu": dict(luu.get("cau") or {}),
           "sua_ap": sl.sua_ap(kq)}
    async for event in stream_v2(query, retrieval_service, context_builder, generator, trace, flags, _today_v2(flags, trace), sua):
        yield event
    trace.lich_v2["loai"] = kq["luu"]["loai"]


def _today_v2(flags: AssistantFlags, trace: AnswerTrace) -> str | None:
    from llm.assistant import _today
    return _today(flags, trace)


def luu_sau_luot(trace: AnswerTrace, flags: AssistantFlags) -> dict | None:
    """Sau lượt lịch bản 2 đạt (biểu mẫu hoặc sửa): trạng thái lưu của cuộc = khung + ngày đi + mưa + điểm đã bỏ + câu đã kiểm theo id điểm."""
    v = trace.lich_v2
    if v is None or v.get("cau") is None or v.get("loi_khung"):
        return None
    luu = sl.luu_tu_lich(v["khung"], v["ngay_di"], v["mua"])
    luu["loai"] = list(v.get("loai") or [])
    muc = {m["id_muc"]: m["id_diem"] for m in lt2.moi_muc(v["lich"]) if m.get("id_diem")}
    luu["cau"] = {muc[k]: c for k, c in v["cau"].items() if k in muc}
    return luu
