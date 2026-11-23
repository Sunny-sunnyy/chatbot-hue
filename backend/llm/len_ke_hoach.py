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
from llm import quan_lich as ql
from llm import sua_lich_v2 as sl
from llm import thoi_tiet as tt
from llm.citations import CITATION_PATTERN
from llm.assistant import (STREAM_DRAIN_SECONDS, AnswerTrace, AssistantFlags, CallLog, GenerationError, GeneratorNotReadyError, ROUTE_TRO_LY_HUE,
                           _lay_nguon_lich, check_citations, elapsed_ms, record_llm_calls)

# Một đoạn nguồn mỗi điểm. Điểm nào không có đoạn vào được ngữ cảnh thì `assistant._lay_nguon_lich` CẮT NGÀY CUỐI của lịch ⇒ trần này phải phủ lịch dày
# nhất có thể có: từ khi lệnh "thêm <điểm>" được vượt nhịp đi (công tắc `sua_lich_them_day`, 23/11/2026) một buổi có tới `TOI_DA_BUOI` + 1 điểm ⇒
# (3 × 2 buổi + 1 tối) × 5 ngày = 35. Trần cũ 25 (= 4 điểm ban ngày + 1 tối × 5 ngày): đếm 23/11/2026 bằng hàm áp lệnh thật — lịch 5 ngày "khám phá
# nhiều" (22 điểm) vượt 25 từ lệnh thêm thứ tư ở 3 / 4 bộ sở thích, tức lệnh thêm đó sẽ làm mất cả ngày 5 (phiên viết giáo trình nêu từ đọc code).
MAX_DOAN = (lt2.TOI_DA_BUOI + 1) * 2 * lt2.SO_NGAY_TOI_DA + lt2.SO_NGAY_TOI_DA
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


CAU_O_MOT_NGAY = "Lịch đi trong ngày (không có đêm nào) nên mình chưa gợi ý chỗ ở."


def dong_du_bao(bang, khung: dict, db: dict | None) -> list[dict]:
    """Dòng dự báo theo ngày của lịch (số do code in) + "Nếu mưa" cho điểm ưu tiên ngoài trời đã giữ chỗ (5c.2) + dòng nguồn.
    Mỗi dòng `{"cau", "ngay"}` — `ngay` = số ngày của lịch để giao diện đặt dòng đúng chỗ, không bóc chữ (giao diện mới 14/11); dòng nguồn không có `ngay`."""
    if db is None:  # có ngày đi mà không có dự báo (quá 7 ngày / lỗi / tắt) ⇒ nói thẳng, như đường sửa ngày đi (`sua_lich_v2`)
        return [{"cau": lt2.CAU_CHUA_DU_BAO}] if any(khung.get("ngay_thang") or ()) else []
    dong, T = [], bang.theo_id
    for ng, ngay in zip(khung["ngay"], khung["ngay_thang"]):
        d = db["ngay"].get(dt.date.fromisoformat(ngay)) if ngay else None
        if d is None:
            continue
        dong.append({"cau": f"Ngày {ng['ngay']} — {tt.dong_ngay(d)}.", "ngay": ng["ngay"]})
        if d["xs"] is not None and d["xs"] >= lt2.NGUONG_MUA:
            dong.append({"cau": dong_neu_mua(bang, khung, ng), "ngay": ng["ngay"]})
    return dong + [{"cau": db["nguon"]}] if dong else []


def ngay_mua_xep(db: dict | None) -> dict | None:
    """Dict `mua` cho bộ xếp: chỉ ngày có lượng mưa dự báo ≥ `MM_MUA_XEP` mm (User 15/11); bộ xếp tự xét thêm ≥ `NGUONG_MUA` %.
    Ngày mưa nhỏ (< 6 mm) không đổi thứ tự xếp, nhưng vẫn có dòng "Nếu mưa" nếu ≥ 60 % (`dong_du_bao` đọc `db`, không đọc dict này)."""
    if db is None:
        return None
    return {k: v["xs"] for k, v in db["ngay"].items() if v["xs"] is not None and v["mua"] >= lt2.MM_MUA_XEP}


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
    mua = ngay_mua_xep(db)
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
    gan_o_an(lich, bang, khung, flags)
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


def gan_o_an(lich: dict, bang, khung: dict, flags: AssistantFlags) -> None:
    """Theo cờ: nơi ở (`o_dau`, khu cả chuyến + cơ sở) và quán mỗi bữa (`an`) — đều do code chọn, không vào tin nhắn gửi model (`tin_nhan_model`
    không đọc hai khoá này). Dùng chung cho lịch thật (`chuan_bi`) và lịch mẫu "Ví dụ" (`api/routes/cong.py`)."""
    if flags.luu_tru_lich:
        # User 15/11: khối nơi ở CHỈ khi người dùng hỏi = lịch có mức hạng (ô hạng sao của biểu mẫu, hoặc nói bằng lời — `doi_hang_o`; mức được
        # giữ qua mọi lượt sửa). Chưa hỏi ⇒ không khối, giao diện chỉ hiện một dòng link sang trang Chỗ ở (lịch 1 ngày: không có đêm ⇒ không link).
        muc = khung["tham_so"].get("ngan_sach")
        if muc:
            lich["o_dau"] = lt2.o_dau_khung(flags.luu_tru_bang, bang, khung, muc)
            if len(khung["ngay"]) < 2:  # đã chọn hạng mà lịch 1 ngày (không có đêm) ⇒ nói lý do thay vì im lặng bỏ khối
                lich.setdefault("ghi_chu", []).append({"ma": "o_dau_mot_ngay", "cau": CAU_O_MOT_NGAY})
        elif len(khung["ngay"]) >= 2:
            lich["cho_o_link"] = True
    if flags.quan_lich:
        lich["an"] = ql.an_uong(flags.quan_bang, bang, khung, flags.quan_toa_do)


def ghi_cau_bi_loai(trace: AnswerTrace, id_muc: str, ma: str, cau: str) -> None:
    """Câu model viết bị `kiem_cau` loại ⇒ giữ nguyên văn cho sổ vết (`core/so_vet.py`, chỉ máy local). Trước 23/11/2026 chỉ có mã lỗi nên không biết
    model đã viết gì; câu là chữ của model về một điểm của bảng, không có chữ người dùng."""
    trace.lich_v2.setdefault("cau_bi_loai", []).append({"id_muc": id_muc, "ma": ma, "cau": cau[:500]})


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
    cau, loi = lt2.chon_cau(flags.bang_lich_v2, trace.lich_v2["lich"], tu_model)
    da_ghi: set[str] = set()
    for x in tu_model:  # `chon_cau` lấy phần tử ĐẦU của mỗi id ⇒ ghi đúng câu đó
        if loi.get(x.get("id_muc")) not in (None, "thieu") and x["id_muc"] not in da_ghi:
            da_ghi.add(x["id_muc"])
            ghi_cau_bi_loai(trace, x["id_muc"], loi[x["id_muc"]], x.get("cau") or "")
    hoan_tat(trace, flags, cau, loi)


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
                            ghi_cau_bi_loai(trace, id_muc, ma, x.get("cau") or "")
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
    Trả None khi model trả danh sách rỗng / lỗi ⇒ lõi đi đường thường."""
    bang, luu = flags.bang_lich_v2, trace.lich_luu
    luu_tru = flags.luu_tru_bang if flags.luu_tru_lich else None  # cờ nơi ở tắt ⇒ "đổi hạng chỗ ở" báo không có mục chỗ ở
    if trace.sua_chon is not None:
        kq = sl.ap(bang, luu, [], sua_chon=trace.sua_chon, luu_tru=luu_tru)
    else:
        call_log = CallLog()
        try:
            # cờ `sua_lich_them_khong_the`: câu code đã gợi ý ở lượt NGAY TRƯỚC (route nạp, đọc là xoá) vào tin hiểu ý; không có ⇒ tin như cũ
            goi_y = tuple(trace.goi_y_sua or ()) if flags.sua_lich_them_khong_the else ()
            ra = await generator.hieu_sua(sl.tin_nhan_hieu(bang, luu, query, **({"goi_y": goi_y} if goi_y else {})), call_log,
                                          **({"chua_ho_tro": True} if flags.sua_lich_chua_ho_tro else {}),  # cờ tắt ⇒ lời gọi như cũ
                                          **({"buoi_toi": True} if flags.sua_lich_buoi_toi else {}),
                                          **({"kem_hoi": True} if flags.sua_lich_kem_hoi else {}),
                                          **({"bo_toi_hoi": True} if flags.bo_toi_hoi_lai else {}))
            # cờ `sua_lich_kem_hoi`: `hoi_them` không phải hành động sửa ⇒ tách ra TRƯỚC mọi bước cũ (tin chỉ có `hoi_them` ⇒ như danh sách rỗng ⇒
            # đường thường). Cờ tắt ⇒ khuôn không có loại này ⇒ `ra` giữ nguyên.
            hoi_them = any(h.loai == sl.HOI_THEM for h in ra)
            ra = [h for h in ra if h.loai != sl.HOI_THEM]
            hanh_dong, bi_chan = sl.loc_hanh_dong([h for h in ra if h.loai != sl.CHUA_HO_TRO], query, luu)
            # rào 22/11: bỏ / thay mà câu không có tên điểm bị chạm lẫn mốc của lịch ("bỏ quán đầu đi rồi viết lại danh sách" — nói về câu trả lời vừa
            # rồi) ⇒ không áp. Lượt đồng ý với câu code vừa gợi ý ("ok thay đi") không qua rào: tên nằm trong câu gợi ý, không trong câu người dùng.
            hanh_dong, khong_neo = (hanh_dong, []) if goi_y else sl.loc_bo_thay(bang, hanh_dong, query)
            cht = len(ra) - len([h for h in ra if h.loai != sl.CHUA_HO_TRO])
        except GenerationError:
            ra, hanh_dong, bi_chan, cht, hoi_them, khong_neo = [], [], 0, 0, False, []
        finally:
            record_llm_calls(trace, call_log.calls, "sua_lich")
        # cờ `sua_lich_doi_cho_code`: model CHỈ trả "chưa hỗ trợ" ⇒ code đọc câu "dời hai điểm"; đọc được ⇒ áp hai lần dời thay cho câu cố định
        doc_cau = sl.doi_buoi_tu_cau(bang, luu, query) if flags.sua_lich_doi_cho_code and cht and not hanh_dong and not bi_chan else []
        if doc_cau:
            hanh_dong = doc_cau
        trace.vet["sua"] = {"hanh_dong": [h.model_dump(exclude_none=True) for h in hanh_dong], "bi_chan": bi_chan, "chua_ho_tro": cht, "doc_cau": bool(doc_cau),
                           "model_ra": [h.model_dump(exclude_none=True) for h in ra],  # sổ vết (RAM): `model_ra` = trước khi lọc (review E)
                           **({"hoi_them": True} if hoi_them else {}), **({"khong_neo": len(khong_neo)} if khong_neo else {})}
        if not hanh_dong and not bi_chan and not cht:
            trace.sua = {"n_hanh_dong": 0}
            return None
        ngay_moi = None
        if any(h.loai == "doi_ngay_di" for h in hanh_dong):  # ngày đọc từ chữ người dùng (code); dự báo cho ngày mới lấy TRƯỚC khi áp
            hom = tt.hom_nay_vn()
            ngay_moi = sl.ngay_di_moi(query, hom)
            if "ngay" in ngay_moi:
                db = await du_bao_lich(flags, ngay_moi["ngay"], lt2.SO_NGAY_TOI_DA, trace, hom)
                ngay_moi.update(mua={k.isoformat(): v for k, v in (ngay_mua_xep(db) or {}).items()}, co_du_bao=db is not None)
        kq = sl.ap(bang, luu, hanh_dong, luu_tru=luu_tru, ngay_moi=ngay_moi,
                   **({"them_khong_the": True} if flags.sua_lich_them_khong_the else {}),  # cờ tắt ⇒ lời gọi như cũ
                   **({"them_day": True} if flags.sua_lich_them_day else {}),
                   **({"bo_toi_de_trong": True} if flags.bo_toi_de_trong else {}),
                   **({"bo_toi_hoi_lai": True} if flags.bo_toi_hoi_lai else {}))
        kq["chua_lam"] += [h.loai for h in khong_neo]  # lượt còn ý sửa khác: ý bỏ / thay không neo được nói ra ("Chưa làm: bỏ điểm"), không bỏ lặng
        # (C 17/11) model đã nhận là câu sửa: "đổi chỗ ngày 1 với ngày 2" từng ra "Chưa làm: đổi số ngày"; ý đổi chỗ ngày đi kèm ý làm được từng bị bỏ lặng
        if sl.la_viec_ngay_chua_lam(query) and not any(f == "so_ngay" for f, _, _ in kq["doi_truong"]):  # "gộp…" đã ra đổi số ngày ⇒ không báo ngược
            # cờ `sua_lich_doi_cho_ngay`: câu CHỈ nhờ đổi chỗ hai ngày (code đọc được cặp ngày, lượt không có ý nào khác đã áp / bị chặn) ⇒ hoán đổi thật
            sach = not (kq["da_ap"] or kq["khong_doi"] or kq["doi_truong"] or kq["ngay_di"] or kq["the"] or bi_chan)
            cap = sl.cap_ngay_doi_cho(query, luu["khung"]["tham_so"]["so_ngay"]) if flags.sua_lich_doi_cho_ngay and sach else None
            if cap is None and hoi_them and flags.sua_lich_doi_cho_ngay and sach:  # tin còn kèm câu hỏi (model báo) ⇒ đọc riêng vế nhờ đổi chỗ
                cap = sl.cap_ngay_doi_cho_kem_hoi(query, luu["khung"]["tham_so"]["so_ngay"])
            if cap:
                kq = sl.doi_cho_ngay(bang, luu, *cap)
            else:
                kq["chua_lam"].append(sl.VIEC_KHAC)
        elif cht and not doc_cau:  # cờ `sua_lich_chua_ho_tro`: model nhận câu sửa chưa làm được ⇒ lượt sửa, lịch giữ nguyên, câu cố định (không đường thường)
            kq["chua_lam"].append(sl.CHUA_HO_TRO)
        elif bi_chan:  # rào số ngày (review E M-1): vẫn là lượt SỬA, code nói thẳng "chưa làm" — đường thường từng viết "đã rút" mà lịch không đổi
            kq["chua_lam"].append("doi_so_ngay")
        if hoi_them:  # lượt này là lượt sửa VÀ tin còn có câu hỏi ⇒ `thay_doi` thêm dòng nói thật (không vào `chua_lam`: không phải việc sửa)
            kq["hoi_them"] = True
    if flags.sua_lich_them_khong_the:  # câu gợi ý của CHÍNH lượt này ⇒ route nhớ cho đúng một lượt kế (lượt không gợi ý gì ⇒ rỗng ⇒ xoá)
        trace.goi_y_moi = sl.cau_goi_y(bang, kq)
    trace.vet.setdefault("sua", {}).update(chon_the=trace.sua_chon, thay_doi=sl.thay_doi(bang, kq))
    trace.sua = {"n_hanh_dong": len(kq["da_ap"]) + len(kq["khong_doi"]) + len(kq["chua_lam"]), "n_ap": len(kq["da_ap"]) + len(kq["doi_truong"]),
                 "n_khong": len(kq["khong_doi"]), "the": kq["the"] is not None, **({"hoi_them": True} if kq.get("hoi_them") else {})}
    # model đã hiểu là câu sửa ⇒ luôn là lượt sửa, kể cả khi mọi hành động trượt (báo "Không đổi được: X không có trong lịch" thay vì trả lời
    # lạc đề — Q3 pilot 14/11). Câu không phải sửa ⇒ model trả danh sách rỗng ⇒ None ở trên (Q5: 0 / 64 câu an toàn ra hành động).
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
    sua = {"khung": kq["khung"], "ngay_di": kq["luu"]["ngay_di"], "thay_doi": sl.thay_doi(bang, kq), "cau_cu": dict(luu.get("cau") or {}),
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
    # Soát khác hãng 20/11: lượt SỬA mà không ý nào làm được (lịch giữ nguyên) ⇒ không lưu lại — giao diện vẫn giữ thẻ lịch cũ (`App.jsx`), nên file
    # tải về phải dựng từ bản lưu cũ, còn nguyên câu an toàn (bão / lũ + 112) của lượt đã tạo ra nó. Lượt biểu mẫu không có `thay_doi`.
    thay_doi = v["lich"].get("thay_doi")
    if thay_doi is not None and not any(d["duoc"] for d in thay_doi):
        return None
    luu = sl.luu_tu_lich(v["khung"], v["ngay_di"], v["mua"])
    luu["loai"] = list(v.get("loai") or [])
    muc = {m["id_muc"]: m["id_diem"] for m in lt2.moi_muc(v["lich"]) if m.get("id_diem")}
    luu["cau"] = {muc[k]: c for k, c in v["cau"].items() if k in muc}
    return luu
