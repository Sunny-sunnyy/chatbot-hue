"""Trang theo dõi cho CHỦ dự án (Phase 12, plan `report_agent/2026-11-20/e_trang_theo_doi_plan.md`): số lượt / kết cục / tiền / độ trễ theo ngày, dựng từ
các dòng `chat_metrics` ĐÃ có trong log — không thêm gì vào log, không cơ sở dữ liệu, không model.

Ai xem được: chỉ khi server bật với biến môi trường `HUE_KHOA_THEO_DOI` (≥ 16 ký tự) VÀ yêu cầu mang đúng khoá ở header `X-Khoa-Theo-Doi`. Chưa đặt biến
⇒ 404 như đường không tồn tại (mặc định TẮT, cùng kiểu các chốt deploy `HUE_LUOT_MOI_NGAY`, `HUE_TAT_DOCS`). Không dựa vào "chỉ máy local": sau một proxy
cùng máy mọi yêu cầu đều trông như từ localhost. Khoá không nằm trong URL, không được ghi vào log.

Không lộ gì của người dùng: dòng `chat_metrics` không có chữ câu hỏi / câu trả lời (`routes/chat.py` `METRIC_FIELDS`, có test khoá); ở đây chỉ trả TỔNG theo
ngày — không dòng riêng lẻ, không mã lượt."""
import hmac
import json
import os
from collections import Counter
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from core.logging_setup import LOG_FILE_NAME, LOGS_DIR

router = APIRouter()

KHOA_ENV = "HUE_KHOA_THEO_DOI"
KHOA_HEADER = "X-Khoa-Theo-Doi"
KHOA_DAI_TOI_THIEU = 16
SO_NGAY = 14
SO_BAN_XOAY_VONG = 3  # `config/logging.yaml`: application.log.1 … .3
MODEL_GIA = "probe"   # model giả của các bộ test ⇒ không phải lượt thật
# Kết cục KHÔNG phải lỗi; mọi mã khác (sinh câu trả lời lỗi, lỗi nội bộ, không tìm được kho, người dùng ngắt…) tính vào cột "lỗi"
KHONG_LOI = frozenset({"success", "out_of_scope", "emergency", "hoi_lai", "sua_the", "lam_thay"})
COT = ("tra_loi", "tu_choi", "ngoai_pham_vi", "web", "lich", "cache", "loi")


def _loai(m: dict) -> str:
    """Mỗi lượt vào ĐÚNG một cột (cộng các cột = số lượt). Thứ tự xét: lỗi > trúng bản lưu > lượt lịch > ngoài phạm vi > có mục web > từ chối > trả lời."""
    if m.get("outcome") not in KHONG_LOI:
        return "loi"
    if m.get("cache") == "trung":
        return "cache"
    if m.get("lich_trinh_ok") is not None or m.get("sua_lich") is not None:
        return "lich"
    if m.get("outcome") in ("out_of_scope", "emergency"):
        return "ngoai_pham_vi"
    if m.get("has_web_section"):
        return "web"
    return "tu_choi" if m.get("refusal") else "tra_loi"


def _phan_vi(xs: list, p: float):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, round(p * (len(xs) - 1)))] if xs else None


def tong_hop(dong_log, so_ngay: int = SO_NGAY) -> dict:
    """Các dòng log (bất kỳ dòng nào; chỉ dòng `chat_metrics` được đọc) ⇒ tổng theo ngày của `so_ngay` ngày gần nhất CÓ lượt, mới nhất trước.
    Ngày = ngày ghi ở đầu dòng log (giờ máy chủ). Dòng cắt dở (log xoay vòng) và dòng của model giả bị bỏ, có đếm."""
    ngay: dict[str, dict] = {}
    bo_gia = bo_hong = 0
    for dong in dong_log:
        if "chat_metrics " not in dong:
            continue
        try:
            m = json.loads(dong.split("chat_metrics ", 1)[1])
            d = datetime.strptime(dong[1:11], "%Y-%m-%d").date().isoformat()
        except ValueError:  # gồm cả json.JSONDecodeError
            bo_hong += 1
            continue
        if m.get("model") == MODEL_GIA:
            bo_gia += 1
            continue
        o = ngay.setdefault(d, {"dem": Counter(), "usd": 0.0, "ms": [], "git_sha": None})
        loai = _loai(m)
        o["dem"][loai] += 1
        o["usd"] += m.get("usd") or 0
        if loai != "loi" and m.get("total_ms") is not None:
            o["ms"].append(m["total_ms"])
        o["git_sha"] = m.get("git_sha") or o["git_sha"]  # dòng đọc theo thứ tự thời gian ⇒ còn lại là bản của lượt gần nhất trong ngày
    hang = [{"ngay": d, "luot": sum(o["dem"].values()), **{c: o["dem"][c] for c in COT}, "usd": round(o["usd"], 4),
             "p50_ms": _phan_vi(o["ms"], 0.5), "p95_ms": _phan_vi(o["ms"], 0.95), "git_sha": o["git_sha"]}
            for d, o in sorted(ngay.items(), reverse=True)[:so_ngay]]
    return {"ngay": hang, "bo_model_gia": bo_gia, "bo_dong_hong": bo_hong}


def doc_log(thu_muc: Path = LOGS_DIR):
    """Các dòng của bản xoay vòng cũ nhất trước, file đang ghi sau cùng (đúng thứ tự thời gian). File không có ⇒ bỏ qua."""
    for ten in [f"{LOG_FILE_NAME}.{i}" for i in range(SO_BAN_XOAY_VONG, 0, -1)] + [LOG_FILE_NAME]:
        duong = thu_muc / ten
        if duong.is_file():
            with duong.open(encoding="utf-8", errors="replace") as f:
                yield from f


def khoa_dung(gui: str | None) -> bool | None:
    """None = trang TẮT (chưa đặt khoá đủ dài) · True / False = khoá gửi lên đúng / sai."""
    khoa = os.getenv(KHOA_ENV, "").strip()
    if len(khoa) < KHOA_DAI_TOI_THIEU:
        return None
    return hmac.compare_digest((gui or "").encode(), khoa.encode())


@router.get("/api/theo_doi")
async def theo_doi(request: Request):
    """Bảng theo ngày cho trang theo dõi. Trang tắt ⇒ 404; sai / thiếu khoá ⇒ 403; cả hai không kèm số nào."""
    dung = khoa_dung(request.headers.get(KHOA_HEADER))
    if dung is None:
        return JSONResponse({"detail": "Not Found"}, status_code=404)
    if not dung:
        return JSONResponse({"detail": "Sai khoá."}, status_code=403)
    return {**tong_hop(doc_log()), "doc_luc": datetime.now().strftime("%H:%M %d/%m/%Y"), "so_ngay": SO_NGAY}
