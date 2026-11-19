"""`GET /api/lich/pptx` — tải lịch của cuộc trò chuyện dưới dạng PowerPoint (cờ `xuat_pptx`, mặc định tắt; plan private
`data/xuat_lich_dep_2026-11-19/PLAN.md`). Không gọi model, không ghi gì.

Server KHÔNG nhận dữ liệu lịch nào từ trình duyệt: yêu cầu không có thân, không có tham số; lịch lấy từ trạng thái server đã lưu cho cuộc trò
chuyện (cookie HttpOnly sẵn có) rồi dựng lại bằng đúng các hàm của lượt trả lời (`dung_lich`, `gan_o_an`) ⇒ mọi chữ trong file là chữ của bảng
điểm, câu tả đã kiểm, hoặc hằng số của khuôn. Lịch hết hạn (30 phút) / cuộc chưa có lịch ⇒ 404 có lời, không dựng file rỗng.
Những thứ trạng thái lưu không có (số nguồn [n], dòng dự báo thời tiết) không vào file — `api/lich_pptx.py` in một dòng cố định thay dự báo."""
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import Response

from api.lich_pptx import KIEU_MAC_DINH, MUC_MOI_TRANG, dung_pptx, trang_lich
from api.routes.chat import CONVERSATION_COOKIE, _flags, error_response
from llm import lich_trinh_v2 as lt2
from llm import thoi_tiet as tt
from llm.len_ke_hoach import gan_o_an

router = APIRouter()
THU_MUC_ANH = Path(__file__).resolve().parents[3] / "frontend" / "public"   # ảnh tự host của giao diện (`/anh/lich/…`)
KIEU_PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
CAU_HET_HAN = "Chưa có lịch để tải hoặc lịch đã hết hạn — bấm Lên kế hoạch để tạo lại rồi tải."


def lich_tu_luu(luu: dict, flags) -> tuple[dict, dict]:
    """Trạng thái lưu của cuộc (`len_ke_hoach.luu_sau_luot`) ⇒ (đối tượng lịch như giao diện nhận — trừ số nguồn + dòng dự báo, câu tả theo mã mục)."""
    bang, khung = flags.bang_lich_v2, luu["khung"]
    lich = lt2.dung_lich(bang, khung, {}, luu["ngay_di"], (), flags.toa_do_lich if flags.ban_do_lich else None,
                         flags.anh_lich_bang if flags.anh_lich else None)
    gan_o_an(lich, bang, khung, flags)
    da_kiem = luu.get("cau") or {}
    return lich, {m["id_muc"]: da_kiem[m["id_diem"]] for m in lt2.moi_muc(lich) if m.get("id_diem") in da_kiem}


@router.get("/api/lich/pptx")
def tai_pptx(request: Request):
    state = request.app.state
    flags = _flags(state)
    if not flags.xuat_pptx:
        return error_response(404, "not_found", "Tính năng này chưa bật.")
    store = getattr(state, "conversations", None)
    luu = store.lay_lich(request.cookies.get(CONVERSATION_COOKIE)) if store is not None else None
    if luu is None:
        return error_response(404, "khong_co_lich", CAU_HET_HAN)
    lich, cau = lich_tu_luu(luu, flags)
    hom_nay = tt.hom_nay_vn()
    trang = trang_lich(lich, cau, MUC_MOI_TRANG[KIEU_MAC_DINH], ngay_tao=f"{hom_nay.day}/{hom_nay.month}/{hom_nay.year}")
    return Response(dung_pptx(trang, KIEU_MAC_DINH, THU_MUC_ANH), media_type=KIEU_PPTX,
                    headers={"Content-Disposition": 'attachment; filename="lich-trinh-hue.pptx"', "Cache-Control": "no-store"})
