"""`GET /api/lich/pptx`, `POST /api/lich/pptx` và `GET /api/lich/ics` — tải lịch của cuộc trò chuyện (cờ `xuat_pptx`, `xuat_nang_cao`, `slide_designer`).

Server KHÔNG nhận dữ liệu lịch nào từ trình duyệt: lịch lấy từ trạng thái server đã lưu cho cuộc trò chuyện (`store.lay_lich(cookie)`),
dựng lại bằng đúng các hàm của lượt trả lời (`dung_lich`, `gan_o_an`). Lịch hết hạn (30 phút) / cuộc chưa có lịch ⇒ 404 có lời, không dựng file rỗng.
"""
import json
import logging
from pathlib import Path

from fastapi import APIRouter, Query, Request
from fastapi.responses import Response

logger = logging.getLogger("slide_designer")

from api.hanh_trinh_chuan import chuan_hoa_lich
from api.lich_ics import ThieuNgayDiError, dung_ics
from api.lich_pptx import dung_pptx, dung_pptx_v2, trang_lich
from api.pptx_catalog import ALLOWED_THEMES, chon_theme_mac_dinh
from api.routes.chat import CONVERSATION_COOKIE, _flags, error_response
from llm import lich_trinh_v2 as lt2
from llm import thoi_tiet as tt
from llm.len_ke_hoach import gan_o_an
from llm.slide_designer import thiet_ke_slide

router = APIRouter()
THU_MUC_ANH = Path(__file__).resolve().parents[3] / "frontend" / "public"   # ảnh tự host của giao diện (`/anh/lich/…`)
KIEU_PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
KIEU_ICS = "text/calendar; charset=utf-8"
CAU_HET_HAN = "Chưa có lịch để tải hoặc lịch đã hết hạn — bấm Lên kế hoạch để tạo lại rồi tải."
CAU_THIEU_NGAY_DI = "Lịch chưa có ngày đi — hãy chọn ngày đi ở biểu mẫu hoặc nhắn ngày khởi hành để tải file .ics."


def lich_tu_luu(luu: dict, flags) -> tuple[dict, dict]:
    """Trạng thái lưu của cuộc (`len_ke_hoach.luu_sau_luot`) ⇒ (đối tượng lịch như giao diện nhận — trừ số nguồn + dòng dự báo, câu tả theo mã mục)."""
    bang, khung = flags.bang_lich_v2, luu["khung"]
    lich = lt2.dung_lich(bang, khung, {}, luu["ngay_di"], (), flags.toa_do_lich if flags.ban_do_lich else None,
                         flags.anh_lich_bang if flags.anh_lich else None)
    gan_o_an(lich, bang, khung, flags)
    da_kiem = luu.get("cau") or {}
    return lich, {m["id_muc"]: da_kiem[m["id_diem"]] for m in lt2.moi_muc(lich) if m.get("id_diem") in da_kiem}


def _gan_ngay_tao(deck: dict, ngay_tao: str) -> dict:
    slides = deck.get("slides") or []
    if slides and slides[0].get("kieu") == "bia" and not slides[0].get("ngay_tao"):
        slides[0] = {**slides[0], "ngay_tao": ngay_tao}
    return {**deck, "ngay_tao": ngay_tao, "slides": slides}


async def _tao_pptx_v2(request: Request, luu: dict, flags, *, theme_id: str | None = None, use_llm: bool = True) -> Response:
    state = request.app.state
    store = state.conversations
    cookie = request.cookies.get(CONVERSATION_COOKIE)
    lich, cau = lich_tu_luu(luu, flags)
    canonical = chuan_hoa_lich(lich, cau, an_toan=luu.get("an_toan"), thu_muc_anh=THU_MUC_ANH)
    theme = theme_id if theme_id in ALLOWED_THEMES else chon_theme_mac_dinh(canonical.get("tham_so"))
    deck = store.lay_slide_cache(cookie, canonical["itinerary_hash"], theme) if hasattr(store, "lay_slide_cache") else None
    if deck is None:
        client = getattr(getattr(state, "generator", None), "client", None)
        res = await thiet_ke_slide(
            canonical,
            theme_id=theme,
            cfg=getattr(flags, "slide_designer_cfg", None),
            client=client,
            use_llm=use_llm,
        )
        deck = res.deck_plan
        if use_llm and hasattr(store, "luu_slide_cache") and deck is not None:
            store.luu_slide_cache(cookie, canonical["itinerary_hash"], theme, deck)
    else:
        layouts_cached = list(dict.fromkeys(s.get("layout_id", "") for s in (deck or {}).get("slides", []) if s.get("layout_id")))
        logger.info(
            "slide_designer %s",
            json.dumps(
                {
                    "slide_designer": True,
                    "used_llm": False,
                    "cache_hit": True,
                    "usd": 0.0,
                    "input_tokens": 0,
                    "cached_tokens": 0,
                    "output_tokens": 0,
                    "retries": 0,
                    "layouts": layouts_cached,
                },
                ensure_ascii=False,
            ),
        )
    hom_nay = tt.hom_nay_vn()
    ngay_tao = f"{hom_nay.day}/{hom_nay.month}/{hom_nay.year}"
    deck = _gan_ngay_tao(deck, ngay_tao)
    layouts_hdr = ",".join(dict.fromkeys(s.get("layout_id", "") for s in (deck or {}).get("slides", []) if s.get("layout_id")))
    return Response(
        dung_pptx_v2(deck, THU_MUC_ANH),
        media_type=KIEU_PPTX,
        headers={
            "Content-Disposition": 'attachment; filename="lich-trinh-hue.pptx"',
            "Cache-Control": "no-store",
            "X-Slide-Layouts": layouts_hdr,
        },
    )


@router.get("/api/lich/pptx")
async def tai_pptx(request: Request, theme: str | None = Query(default=None, max_length=40)):
    state = request.app.state
    flags = _flags(state)
    if not flags.xuat_pptx and not getattr(flags, "slide_designer", False):
        return error_response(404, "not_found", "Tính năng này chưa bật.")
    store = getattr(state, "conversations", None)
    luu = store.lay_lich(request.cookies.get(CONVERSATION_COOKIE)) if store is not None else None
    if luu is None:
        return error_response(404, "khong_co_lich", CAU_HET_HAN)
    if getattr(flags, "slide_designer", False):
        return await _tao_pptx_v2(request, luu, flags, theme_id=theme, use_llm=False)
    lich, cau = lich_tu_luu(luu, flags)
    hom_nay = tt.hom_nay_vn()
    trang = trang_lich(lich, cau, ngay_tao=f"{hom_nay.day}/{hom_nay.month}/{hom_nay.year}", an_toan=luu.get("an_toan"))
    return Response(dung_pptx(trang, THU_MUC_ANH), media_type=KIEU_PPTX,
                    headers={"Content-Disposition": 'attachment; filename="lich-trinh-hue.pptx"', "Cache-Control": "no-store"})


@router.post("/api/lich/pptx")
async def tai_pptx_thong_minh(request: Request):
    state = request.app.state
    flags = _flags(state)
    if not getattr(flags, "slide_designer", False):
        return error_response(404, "not_found", "Tính năng này chưa bật.")
    store = getattr(state, "conversations", None)
    luu = store.lay_lich(request.cookies.get(CONVERSATION_COOKIE)) if store is not None else None
    if luu is None:
        return error_response(404, "khong_co_lich", CAU_HET_HAN)
    theme_id = None
    try:
        body = await request.json()
        if isinstance(body, dict) and isinstance(body.get("theme_id"), str):
            theme_id = body["theme_id"]
    except Exception:
        theme_id = None
    return await _tao_pptx_v2(request, luu, flags, theme_id=theme_id)


@router.get("/api/lich/ics")
def tai_ics(request: Request):
    state = request.app.state
    flags = _flags(state)
    if not getattr(flags, "xuat_nang_cao", False):
        return error_response(404, "not_found", "Tính năng này chưa bật.")
    store = getattr(state, "conversations", None)
    luu = store.lay_lich(request.cookies.get(CONVERSATION_COOKIE)) if store is not None else None
    if luu is None:
        return error_response(404, "khong_co_lich", CAU_HET_HAN)
    if not luu.get("ngay_di"):
        return error_response(400, "thieu_ngay_di", CAU_THIEU_NGAY_DI)
    lich, cau = lich_tu_luu(luu, flags)
    canonical = chuan_hoa_lich(lich, cau, an_toan=luu.get("an_toan"), thu_muc_anh=THU_MUC_ANH)
    try:
        kq = dung_ics(canonical)
    except ThieuNgayDiError as exc:
        return error_response(400, "thieu_ngay_di", str(exc))
    return Response(
        kq["ics"].encode("utf-8"),
        media_type=KIEU_ICS,
        headers={"Content-Disposition": 'attachment; filename="lich-trinh-hue.ics"', "Cache-Control": "no-store"},
    )
