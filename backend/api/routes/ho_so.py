"""Hồ sơ theo chủ đề (công tắc `ho_so_chu_de`, mặc định tắt; bản thử nhánh thu-b-ho-so-chu-de — chủ dự án chọn 22:19 24/11/2026: chọn chủ đề từ danh sách).

- `GET /api/ho_so/chu_de` — danh sách chủ đề do code dựng từ mục lục kho (`llm/ho_so_chu_de.danh_sach`), kèm các bài của từng chủ đề (giao diện lấy ảnh thẻ).
- `POST /api/ho_so` thân `{"ma": …}` — dựng hồ sơ của MỘT chủ đề trong danh sách. Không nhận chữ tự do của người dùng: `ma` phải là mã có trong danh sách.

Luồng SSE: `chu_de` (có ngay) ⇒ `dan_y` (model gom các bài thành mục, code kiểm lại; bước này hỏng ⇒ code tự chia mục) ⇒ một `muc` cho mỗi mục (song song,
thứ tự bất kỳ; khuôn đoạn như sổ tay — `llm/so_tay.tach_ma`) ⇒ `xong`. Lỗi của MỘT mục chỉ làm mục đó `loi`.
Bộ nhớ đệm: hồ sơ của một chủ đề chỉ phụ thuộc kho ⇒ hồ sơ dựng xong KHÔNG có mục lỗi được giữ trong RAM theo mã chủ đề (mất khi khởi động lại server); lần gọi
sau phát lại y nguyên các sự kiện, không gọi model (sự kiện `xong` mang `tu_dem: true`). Lý do: trang mở thẳng / F5 là một lượt dựng 5–9 lời gọi model."""
import asyncio
import logging
import re
import time

import anyio
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict, Field

from api.routes.chat import _flags, _ready_generator, _retrieval_not_ready, error_response, sse_event
from api.routes.so_tay import SONG_SONG, _bang_chung
from llm import ho_so_chu_de as hs
from llm import so_tay as st
from llm.generator_openai_full_corpus import CallLog
from retrieval.full_corpus_context import FullCorpusContextBuilder

router = APIRouter()
logger = logging.getLogger("ho_so")


class HoSoRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    ma: str = Field(min_length=1, max_length=40)


def _bai_ra(bai) -> dict:
    return {"ten": bai.tieu_de, "bai_id": bai.rel}


@router.get("/api/ho_so/chu_de")
async def chu_de(request: Request):
    flags = _flags(request.app.state)
    if not getattr(flags, "ho_so_chu_de", False) or flags.muc_luc is None:
        return error_response(404, "not_found", "Tính năng này chưa bật.")
    theo_ma = {c.ma: c for c in hs.CHU_DE}
    return {"chu_de": [{**c, "bai": [_bai_ra(b) for b in hs.bai_cua(theo_ma[c["ma"]], flags.muc_luc)[:hs.TRAN_BAI]]} for c in hs.danh_sach(flags.muc_luc)]}


async def _mot_muc(muc: dict, ten_chu_de: str, state, flags, generator, dem: dict) -> dict:
    """MỘT mục của hồ sơ; không bao giờ ném (trừ khi bị huỷ). Lời gọi model của mục hỏng ⇒ mục `loi` nhưng các phần do CODE dựng vẫn có: khối giờ / giá, và
    dòng trỏ tới phần lưu ý an toàn của từng bài có đoạn cảnh báo."""
    started = time.perf_counter()
    bai, doan, nguon, trang_thai, y, thieu = muc["bai_goc"], [], [], "xong", [], []
    try:
        moi_bai = hs.so_doan_moi_bai(len(bai))
        tai_lieu, canh_bao = [], {}  # canh_bao: mã đoạn cảnh báo an toàn ⇒ (bài của nó, chính đoạn đó)
        for b in bai:  # code chọn đoạn của CHÍNH các bài trong mục: xếp trong bài theo tên chủ đề + tên mục, cộng đoạn cảnh báo an toàn của bài (nếu có)
            cua_bai = await asyncio.to_thread(state.retrieval_service.doan_cua_bai, b.rel)
            chon = st.xep_trong_bai(cua_bai, f"{ten_chu_de} {muc['ten']} {hs.CUM_XEP}")[:moi_bai]
            cb = hs.doan_canh_bao(cua_bai)
            if cb is not None:
                canh_bao[cb.id] = (b, cb)
                if cb.id not in {d.id for d in chon}:
                    chon.append(cb)
            tai_lieu += chon
        chu, nguon_kho = _bang_chung(tai_lieu, 1)
        ma_cua_so = dict(zip((s["id"] for s in nguon_kho), (d.id for d in tai_lieu if FullCorpusContextBuilder._source(d, 0) is not None)))
        so_canh_bao = {so: canh_bao[ma] for so, ma in ma_cua_so.items() if ma in canh_bao}
        thieu = [b.tieu_de for b in bai]
        if nguon_kho:
            try:
                log = CallLog()
                try:
                    ra = await generator.viet_so_tay("ho_so_muc", f"Chủ đề hồ sơ: {ten_chu_de}\nMục cần viết: {muc['ten']}\nCác bài của mục: "
                                                     f"{'; '.join(b.tieu_de for b in bai)}\n\nBằng chứng:\n{chu}", log)
                finally:
                    dem["goi_model"] += len(log.calls)
                qua_luat, bo = st.loc_y(ra.get("y") or [], {s["id"] for s in nguon_kho}, 50, tran_ky_tu=hs.TRAN_KY_TU_Y)
                for ly_do, gia_tri in bo.items():
                    if ly_do == "chu":
                        for ly, cau in gia_tri:
                            logger.info("ho_so dropped item (%s): %s", ly, cau)
                    else:
                        dem["bo_" + ly_do] += gia_tri
                ten_theo_rel = {b.rel: b.tieu_de for b in bai}
                y, thieu = hs.chon_y_phu_bai(qua_luat, {s["id"]: ten_theo_rel.get(s["bai_id"], "") for s in nguon_kho}, [b.tieu_de for b in bai],
                                             frozenset(so_canh_bao))
            except asyncio.CancelledError:
                raise
            except Exception:  # noqa: BLE001 — model / khuôn hỏng: mục `loi`, phần do code dựng bên dưới vẫn chạy
                logger.exception("ho_so section model call failed")
                trang_thai = "loi"
        nguon = list(nguon_kho)
        y_canh_bao = [dong for dong in y if hs.la_y_canh_bao(dong, so_canh_bao)]
        y_thuong = [dong for dong in y if dong not in y_canh_bao]
        if y_thuong:
            doan.append({"nhan": None, "kieu": "gach", "chu": None, "gach": y_thuong})
        # cảnh báo an toàn của kho không lẫn trong danh sách ý thường: mỗi ý cảnh báo là MỘT phần tử `an_toan` (giao diện vẽ bằng lớp câu an toàn của sản phẩm)
        doan += [{"nhan": hs.NHAN_AN_TOAN, "kieu": "an_toan", "chu": dong, "gach": None} for dong in y_canh_bao]
        # bài có đoạn cảnh báo mà mục KHÔNG có ý cảnh báo nào dẫn bài đó (model không viết, viết bị lọc, hoặc lời gọi hỏng) ⇒ code thêm dòng trỏ — chỉ khi đoạn nằm
        # dưới một mục dặn du khách (nêu tên mục) hoặc có câu cấm (không nêu tên mục); đoạn chỉ là bằng chứng thì không trỏ (`so_tay.muc_tro_an_toan`)
        bai_cua_so = {s["id"]: s["bai_id"] for s in nguon_kho}
        bai_da_co = {bai_cua_so.get(int(n)) for dong in y if st.la_y_canh_bao(dong, None) for n in re.findall(r"\[(\d+)\]", dong)}
        for so, (b, cb) in so_canh_bao.items():
            muc_bai = st.muc_tro_an_toan(cb)
            if muc_bai is not None and b.rel not in bai_da_co:
                cau = hs.CAU_TRO_AN_TOAN.format(ten=b.tieu_de, muc=muc_bai) if muc_bai else hs.CAU_TRO_AN_TOAN_CHUNG.format(ten=b.tieu_de)
                doan.append({"nhan": None, "kieu": "an_toan", "chu": f"{cau} [{so}]", "gach": None})
                dem["tro_an_toan"] += 1
        du_kien, nguon_dk = hs.dong_du_kien(bai, flags.the_noi_bang, len(nguon) + 1)
        if du_kien:
            doan.append(du_kien)
            nguon += nguon_dk
        if trang_thai == "xong":  # mục lỗi thì không in ô "chưa ghi được" cho từng bài — cả mục đã mang trạng thái lỗi
            id_theo_ten = {b.tieu_de: b.rel for b in bai}
            doan += [{"nhan": ten, "kieu": "thieu", "chu": None, "gach": None, "bai_id": id_theo_ten.get(ten)} for ten in thieu]
    except asyncio.CancelledError:
        raise
    except Exception:  # noqa: BLE001 — một mục hỏng không làm đứt luồng
        logger.exception("ho_so section failed")
        trang_thai = "loi"
    sach = st.tach_ma(doan)
    for d, goc in zip(sach, doan):  # ô thiếu của hồ sơ mang mã bài để giao diện mở được bài
        if goc.get("bai_id"):
            d["bai_id"] = goc["bai_id"]
    return {"id": muc["id"], "trang_thai": trang_thai, "muc_do": hs.muc_do(len(y)), "doan": sach, "nguon": st.nguon_da_dung(doan, nguon),
            "giay": round(time.perf_counter() - started, 1)}


async def _su_kien(cd: "hs.ChuDe", bai: list, state, flags, generator, dem_ho_so: dict):
    started = time.perf_counter()
    dem = {"goi_model": 0, "bo_khong_nguon": 0, "bo_qua_dai": 0, "bo_gio_gia": 0, "bo_qua_tran": 0, "tro_an_toan": 0}
    phat = [sse_event("chu_de", {"ma": cd.ma, "ten": cd.ten, "so_bai": len(bai), "bai": [_bai_ra(b) for b in bai]})]
    yield phat[-1]
    dan_y_loi = False
    try:  # dàn ý: model chỉ GOM các bài đã chọn; code kiểm lại — hỏng thì code tự chia
        log = CallLog()
        try:
            ra = await generator.viet_so_tay("ho_so_dan_y", f"Chủ đề: {cd.ten}\n\nDanh sách bài đã chọn:\n"
                                             + "\n".join(f"{i} | {b.tieu_de} | {(b.tom_tat or '')[:110]}" for i, b in enumerate(bai, 1)), log)
        finally:
            dem["goi_model"] += len(log.calls)
        chia = hs.kiem_dan_y(ra.get("muc") or [], len(bai))
    except asyncio.CancelledError:
        raise
    except Exception:  # noqa: BLE001
        logger.exception("ho_so outline failed")
        chia, dan_y_loi = hs.chia_muc_du_phong(len(bai)), True
    muc = [{"id": f"m{k}", "ten": m["tieu_de"] or ", ".join(bai[n - 1].tieu_de for n in m["bai"][:3]) + ("…" if len(m["bai"]) > 3 else ""),
            "bai_goc": [bai[n - 1] for n in m["bai"]]} for k, m in enumerate(chia, 1)]
    phat.append(sse_event("dan_y", {"tieu_de": cd.ten, "muc": [{"id": m["id"], "ten": m["ten"], "bai": [_bai_ra(b) for b in m["bai_goc"]]} for m in muc]}))
    yield phat[-1]
    khoa = asyncio.Semaphore(SONG_SONG)

    async def mot(m: dict) -> dict:
        async with khoa:
            return await _mot_muc(m, cd.ten, state, flags, generator, dem)

    viec = [asyncio.create_task(mot(m)) for m in muc]
    loi = du = 0
    try:
        for xong in asyncio.as_completed(viec):
            ket_qua = await xong
            loi += ket_qua["trang_thai"] == "loi"
            du += ket_qua["trang_thai"] == "xong" and ket_qua["muc_do"] == "du"
            phat.append(sse_event("muc", ket_qua))
            yield phat[-1]
    finally:
        for v in viec:
            if not v.done():
                v.cancel()
        with anyio.CancelScope(shield=True):
            await asyncio.gather(*viec, return_exceptions=True)
    giay = round(time.perf_counter() - started, 1)
    logger.info("ho_so done: topic=%s sections=%d failed=%d outline_fallback=%s seconds=%.1f llm_calls=%d", cd.ma, len(muc), loi, dan_y_loi, giay, dem["goi_model"])
    # `ban_ngan`: dưới nửa số mục có đủ ý ⇒ giao diện nói rõ đây là bản ngắn (code đếm, không phải model tự nhận)
    cuoi = {"giay": giay, "so_muc": len(muc), "so_muc_loi": loi, "so_muc_du": du, "ban_ngan": du * 2 < len(muc), "dan_y_do_code": dan_y_loi, "so_loi_goi_model": dem["goi_model"],
            "y_bi_bo": {k[3:]: v for k, v in dem.items() if k.startswith("bo_")}, "so_dong_tro_an_toan": dem["tro_an_toan"]}
    if not loi and not dan_y_loi:  # chỉ nhớ bản dựng trọn vẹn
        dem_ho_so[cd.ma] = [*phat, sse_event("xong", {**cuoi, "tu_dem": True})]
    yield sse_event("xong", {**cuoi, "tu_dem": False})


async def _phat_lai(su_kien: list[bytes]):
    for e in su_kien:
        yield e


@router.post("/api/ho_so")
async def ho_so(body: HoSoRequest, request: Request):
    state = request.app.state
    flags = _flags(state)
    if not getattr(flags, "ho_so_chu_de", False) or flags.muc_luc is None:
        return error_response(404, "not_found", "Tính năng này chưa bật.")
    cd = next((c for c in hs.CHU_DE if c.ma == body.ma), None)
    bai = hs.bai_cua(cd, flags.muc_luc)[:hs.TRAN_BAI] if cd else []
    if len(bai) < hs.NGUONG_BAI:
        return error_response(404, "khong_co_chu_de", "Chủ đề này không có trong danh sách.")
    dau = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    dem_ho_so = getattr(state, "ho_so_dem", None)
    if dem_ho_so is None:
        dem_ho_so = state.ho_so_dem = {}
    if cd.ma in dem_ho_so:
        return StreamingResponse(_phat_lai(dem_ho_so[cd.ma]), media_type="text/event-stream", headers=dau)
    chua_san = _retrieval_not_ready(state, None)
    if chua_san is not None:
        return chua_san
    generator = _ready_generator(state)
    if generator is None:
        return error_response(503, "generator_not_ready", "Không thể tạo hồ sơ vào lúc này.")
    return StreamingResponse(_su_kien(cd, bai, state, flags, generator, dem_ho_so), media_type="text/event-stream", headers=dau)
