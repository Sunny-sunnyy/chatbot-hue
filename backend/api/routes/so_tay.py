"""`POST /api/so_tay` — sổ tay cho chuyến đi dựng từ lịch ĐANG LƯU của cuộc trò chuyện (công tắc `so_tay`, mặc định tắt; bản thử nhánh thu-b-so-tay).

Server KHÔNG nhận dữ liệu nào từ trình duyệt (không thân, không tham số): lịch lấy từ trạng thái đã lưu của cuộc (cookie sẵn có) rồi dựng lại bằng đúng hàm
của đường tải PowerPoint (`xuat.lich_tu_luu`). Không có chữ người dùng gõ nào đi vào model ở đường này.

Luồng SSE: `dan_y` (các mục, do code, có ngay) ⇒ một `muc` cho mỗi mục khi nó xong (thứ tự bất kỳ — các mục chạy song song, tối đa `SONG_SONG` mục một lúc)
⇒ `xong`. Lỗi trước khi mở luồng trả JSON như `/api/chat`: công tắc tắt 404 · không có lịch đang lưu 409 `khong_co_lich` · tìm kho / model chưa sẵn 503.
Lời gọi model của MỘT mục hỏng ⇒ mục đó `trang_thai: "loi"` và chỉ gồm các dòng do code chép; các mục khác không bị ảnh hưởng.
Chia việc code ↔ model, khuôn dữ liệu của từng đoạn: `llm/so_tay.py`."""
import asyncio
import logging
import time

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from api.routes.chat import CONVERSATION_COOKIE, _flags, _ready_generator, _retrieval_not_ready, error_response, sse_event
from api.routes.xuat import lich_tu_luu
from core.schema import GenerationError, RetrievalDependencyError
from llm import so_tay as st
from llm.generator_openai_full_corpus import CallLog
from retrieval.full_corpus_context import FullCorpusContextBuilder

router = APIRouter()
logger = logging.getLogger("so_tay")
SONG_SONG = 4
CAU_KHONG_CO_LICH = "Chưa có lịch để dựng sổ tay hoặc lịch không còn được giữ — bấm Lên kế hoạch để xếp lại lịch."


def _bang_chung(tai_lieu: list, tu_so: int) -> tuple[str, list[dict]]:
    """Các đoạn kho ⇒ (chữ ngữ cảnh "[Nguồn n] …" đánh số từ `tu_so`, danh sách nguồn dạng `SourceResponse` của chat)."""
    khoi, nguon = [], []
    for d in tai_lieu:
        src = FullCorpusContextBuilder._source(d, tu_so + len(nguon))
        if src is None:
            continue
        khoi.append(FullCorpusContextBuilder._block(src))
        nguon.append({"id": src.id, "title": src.title, "bai_id": src.source if src.source.endswith(".md") else None,
                      "heading_path": list(src.heading_path), "excerpts": list(src.excerpts)})
    return "\n\n".join(khoi), nguon


async def _muc_model(loai: str, ten_khoi: tuple[str, ...], cau_tim: str, de: str, bai_id: str | None, doan: list[dict], nguon: list[dict], state,
                     generator, dem: dict, ten_rieng: str | None = None) -> str:
    """Phần model của một mục: tìm kho bằng câu tìm cố định của code ⇒ một lời gọi có khuôn ⇒ lọc bằng luật của code ⇒ nối vào `doan` / `nguon`.
    Trả trạng thái mục ("xong" | "loi")."""
    try:
        ket_qua = await asyncio.to_thread(state.retrieval_service.search, cau_tim)
        doan_bai = await asyncio.to_thread(state.retrieval_service.doan_cua_bai, bai_id) if bai_id else []
        chu, nguon_kho = _bang_chung(st.chon_bang_chung(ket_qua.documents, doan_bai, bai_id, ten_rieng=ten_rieng), len(nguon) + 1)
        if not nguon_kho:  # không đoạn nào ⇒ không gọi model; mọi khối là "Kho chưa có"
            doan.extend({"nhan": st.NHAN[k], "kieu": "thieu", "chu": None, "gach": None} for k in ten_khoi)
            return "xong"
        log = CallLog()
        try:
            ra = await generator.viet_so_tay(loai, f"{de}\n\nBằng chứng:\n{chu}", log)
        finally:
            dem["goi_model"] += len(log.calls)
        nguon.extend(nguon_kho)
        hop_le = {s["id"] for s in nguon_kho}
        for k in ten_khoi:
            khoi, bo = st.khoi_model(k, ra.get(k) or [], hop_le, cam_gio_gia=loai == "diem")
            doan.append(khoi)
            for ly_do, n in bo.items():
                dem["bo_" + ly_do] += n
        return "xong"
    except (GenerationError, RetrievalDependencyError) as exc:
        logger.warning("so_tay section failed: %s", type(exc).__name__)
        return "loi"


async def _dung_muc(muc: dict, lich: dict, an_toan: str | None, state, flags, generator, dem: dict) -> dict:
    started = time.perf_counter()
    trang_thai = "xong"
    if muc["loai"] == "diem":
        bang_the = flags.the_noi_bang
        noi = next((n for n in (bang_the.noi if bang_the else ()) if n.rel == muc["bai_id"]), None) if muc["bai_id"] else None
        diem = flags.bang_lich_v2.theo_id.get(muc["id_diem"], {}) if flags.bang_lich_v2 else {}
        doan, nguon = st.du_kien(noi, bang_the, muc["bai_id"], (diem.get("gio_mo_cua"), diem.get("gio_nguon")), muc["ten"])
        # điểm không có bài riêng ⇒ bằng chứng là các đoạn NHẮC TÊN điểm trong bài mà bảng điểm trỏ tới (`llm/so_tay.chon_bang_chung`)
        trang_thai = await _muc_model("diem", ("nen_xem", "luu_y"), st.CAU_TIM_DIEM.format(ten=muc["ten"]), f"Điểm: {muc['ten']}",
                                      muc["bai_id"] or diem.get("nguon"), doan, nguon, state, generator, dem,
                                      ten_rieng=None if muc["bai_id"] else muc["ten"])
    elif muc["loai"] == "an_uong":
        doan, nguon = st.muc_an_uong(muc["an"])
    else:
        doan, nguon = [], []
        trang_thai = await _muc_model("di_lai", ("di_lai",), st.CAU_TIM_DI_LAI, "Phần cần viết: Đi lại giữa các điểm tham quan ở Huế", None, doan, nguon,
                                      state, generator, dem)
        doan.extend(st.doan_chung(lich, an_toan))
    # chữ gửi ra KHÔNG mang mã [n]: số nguồn của từng dòng nằm ở `so` / `gach_so` (`llm/so_tay.tach_ma`)
    return {"id": muc["id"], "trang_thai": trang_thai, "doan": st.tach_ma(doan), "nguon": st.nguon_da_dung(doan, nguon),
            "giay": round(time.perf_counter() - started, 1)}


async def _su_kien(dan_y: list[dict], lich: dict, an_toan: str | None, state, flags, generator):
    started = time.perf_counter()
    dem = {"goi_model": 0, "bo_khong_nguon": 0, "bo_qua_dai": 0, "bo_gio_gia": 0, "bo_qua_tran": 0}
    yield sse_event("dan_y", {"tieu_de": f"Sổ tay cho chuyến đi Huế {len(lich['ngay'])} ngày", "so_ngay": len(lich["ngay"]),
                              "muc": [st.ra_giao_dien(m) for m in dan_y]})
    khoa = asyncio.Semaphore(SONG_SONG)

    async def mot(muc: dict) -> dict:
        async with khoa:
            return await _dung_muc(muc, lich, an_toan, state, flags, generator, dem)

    viec = [asyncio.create_task(mot(m)) for m in dan_y]
    loi = 0
    try:
        for xong in asyncio.as_completed(viec):
            ket_qua = await xong
            loi += ket_qua["trang_thai"] == "loi"
            yield sse_event("muc", ket_qua)
    finally:
        for v in viec:  # trình duyệt đóng luồng giữa chừng ⇒ không để lời gọi model chạy tiếp vô ích
            v.cancel()
    giay = round(time.perf_counter() - started, 1)
    logger.info("so_tay done: sections=%d failed=%d seconds=%.1f llm_calls=%d dropped=%s", len(dan_y), loi, giay, dem["goi_model"],
                {k: v for k, v in dem.items() if k.startswith("bo_") and v})
    yield sse_event("xong", {"giay": giay, "so_muc": len(dan_y), "so_muc_loi": loi, "so_loi_goi_model": dem["goi_model"],
                             "y_bi_bo": {k[3:]: v for k, v in dem.items() if k.startswith("bo_")}})


@router.post("/api/so_tay")
async def so_tay(request: Request):
    state = request.app.state
    flags = _flags(state)
    if not getattr(flags, "so_tay", False):
        return error_response(404, "not_found", "Tính năng này chưa bật.")
    store = getattr(state, "conversations", None)
    luu = store.lay_lich(request.cookies.get(CONVERSATION_COOKIE)) if store is not None else None
    if luu is None:
        return error_response(409, "khong_co_lich", CAU_KHONG_CO_LICH)
    chua_san = _retrieval_not_ready(state, None)
    if chua_san is not None:
        return chua_san
    generator = _ready_generator(state)
    if generator is None:
        return error_response(503, "generator_not_ready", "Không thể tạo sổ tay vào lúc này.")
    lich, _ = lich_tu_luu(luu, flags)
    return StreamingResponse(_su_kien(st.dan_y(lich), lich, luu.get("an_toan"), state, flags, generator), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
