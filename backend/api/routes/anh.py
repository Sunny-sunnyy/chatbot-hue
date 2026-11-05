"""`POST /api/anh/ung_vien` — hỏi bằng ảnh, Phase 10 A1 (plan `2026-11-05-phase-10-a1-plan.md` bản 2 `2fc2fcea33d4` D2, D6, D8, D9; spec A10).

Thân yêu cầu = **bytes ảnh** (`Content-Type: image/jpeg|png|webp`), không multipart: kiểu này buộc trình duyệt hỏi trước (preflight) khi gửi từ
trang khác, server không bật CORS ⇒ trang lạ không gửi được. Thêm lớp kiểm `Sec-Fetch-Site` / `Origin` + giới hạn byte **trước khi đọc thân**.
Phản hồi chỉ có id + tên chuẩn để người dùng bấm xác nhận (không chữ tự do — Q-f). Cờ `anh.bat` tắt ⇒ `app.state.anh is None` ⇒ 404.
"""
import asyncio
import json
import logging
import time

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from core.schema import GenerationError
from llm.generator_openai_full_corpus import CallLog
from llm.nhan_anh import AnhKhongHopLe, chuan_bi_anh, doan_ten

logger = logging.getLogger("chat")
router = APIRouter()

KIEU_ANH = {"image/jpeg", "image/png", "image/webp"}
# Một dòng `anh_metrics` mỗi yêu cầu: chỉ số đếm / mã / thời gian / tiền — KHÔNG ảnh, tên file, id / tên ứng viên, header (Q-g).
ANH_FIELDS = ("outcome", "status_code", "bytes_vao", "w", "h", "n_ung_vien", "n_llm_calls", "input_tokens", "output_tokens",
              "reasoning_tokens", "usd", "ms_xu_ly", "ms_model", "ms_tong")


def kiem_dau_vao(headers, origin_cua_server: str, max_bytes: int) -> tuple[int, str] | None:
    """Rào A10 (1)–(4), chưa đọc thân. Trả (mã HTTP, mã lỗi) hoặc None nếu qua. `headers` là mapping không phân biệt hoa thường."""
    site = headers.get("sec-fetch-site")
    if site is not None and site != "same-origin":
        return 403, "cross_site"
    origin = headers.get("origin")
    if origin is not None and origin != origin_cua_server:
        return 403, "cross_origin"
    if (headers.get("content-type") or "").split(";")[0].strip().lower() not in KIEU_ANH:
        return 415, "unsupported_media_type"
    length = headers.get("content-length")
    if length is None or not length.isdigit() or int(length) > max_bytes:
        return 413, "payload_too_large"
    return None


async def doc_than(request: Request, max_bytes: int) -> bytes | None:
    """Đọc luồng thân có bộ đếm (không `UploadFile` / `Form` — Starlette sẽ ghi cả thân ra file tạm trước khi vào hàm). Vượt ⇒ None."""
    phan, n = [], 0
    async for chunk in request.stream():
        n += len(chunk)
        if n > max_bytes:
            return None
        phan.append(chunk)
    return b"".join(phan)


def _tra(metrics: dict, status: int, body: dict) -> JSONResponse:
    metrics["status_code"] = status
    logger.info("anh_metrics %s", json.dumps({k: metrics.get(k) for k in ANH_FIELDS}))
    return JSONResponse(status_code=status, content=body)


@router.get("/api/anh/ung_vien")
async def trang_thai(request: Request):
    """Giao diện hỏi trước để chỉ hiện nút ảnh khi cờ bật (tắt ⇒ 404, như POST). Không đọc gì, không ghi log."""
    if getattr(request.app.state, "anh", None) is None:
        return JSONResponse(status_code=404, content={"code": "not_found"})
    return {"bat": True}


@router.post("/api/anh/ung_vien")
async def ung_vien(request: Request):
    started = time.perf_counter()
    metrics: dict = {"n_llm_calls": 0}
    cfg = getattr(request.app.state, "anh", None)
    if cfg is None:  # cờ tắt (D2) — như route không có, không đọc thân
        metrics["outcome"] = "tat"
        return _tra(metrics, 404, {"code": "not_found"})

    loi = kiem_dau_vao(request.headers, f"{request.url.scheme}://{request.url.netloc}", cfg["max_bytes"])
    if loi is not None:
        metrics["outcome"] = f"tu_choi_{loi[1]}"
        return _tra(metrics, loi[0], {"code": loi[1]})
    data = await doc_than(request, cfg["max_bytes"])
    if data is None:  # Content-Length khai thấp hơn thân thật
        metrics["outcome"] = "tu_choi_payload_too_large"
        return _tra(metrics, 413, {"code": "payload_too_large"})
    metrics["bytes_vao"] = len(data)

    generator = getattr(request.app.state, "generator", None)
    if generator is None:
        metrics["outcome"] = "generator_unavailable"
        return _tra(metrics, 503, {"code": "generator_unavailable"})

    t0 = time.perf_counter()
    try:
        jpeg, metrics["w"], metrics["h"] = await asyncio.to_thread(chuan_bi_anh, data, max_pixels=cfg["max_pixels"], canh_dai=cfg["canh_dai"])
    except AnhKhongHopLe as exc:
        metrics["outcome"] = f"tu_choi_{exc.code}"
        return _tra(metrics, exc.status, {"code": exc.code})
    metrics["ms_xu_ly"] = round((time.perf_counter() - t0) * 1000, 1)

    call_log = CallLog()
    t1 = time.perf_counter()
    try:
        ten = await doan_ten(generator, cfg["agent"], jpeg, cfg["danh_sach"], call_log, cfg["timeout"])
        metrics["outcome"] = "ok" if ten else "khong_nhan_ra"
        body = {"ung_vien": ten, "khong_nhan_ra": not ten}
    except GenerationError:  # lỗi / quá hạn / đầu ra hỏng ⇒ không đoán, không thử lại (D8); giao diện hiện câu A9
        ten, metrics["outcome"] = [], "loi_model"
        body = {"ung_vien": [], "khong_nhan_ra": True, "loi": "khong_doan_duoc"}
    metrics["ms_model"] = round((time.perf_counter() - t1) * 1000, 1)
    calls = call_log.calls
    metrics.update(n_ung_vien=len(ten), n_llm_calls=len(calls), ms_tong=round((time.perf_counter() - started) * 1000, 1))
    for key in ("input_tokens", "output_tokens", "reasoning_tokens", "usd"):
        values = [c.get(key) for c in calls if c.get(key) is not None]
        metrics[key] = round(sum(values), 8) if values else None
    return _tra(metrics, 200, body)
