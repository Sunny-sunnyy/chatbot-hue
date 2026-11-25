"""`POST /api/lich/hoan_tac` — BẢN THỬ công tắc `sua_lich_hoan_tac` (mặc định tắt ⇒ 404): hoàn tác lần sửa lịch vừa rồi. Không gọi model.

Thân yêu cầu chỉ có `ma` — mã của nút "Hoàn tác" mà thẻ của lượt sửa mang (`sua_lich_v2.nut_hoan_tac`, gắn ở `len_ke_hoach.chuan_bi`): dấu của lịch SAU lần sửa đó. Server không nhận dữ liệu lịch
nào từ trình duyệt: bản lịch trước lần sửa nằm trong trạng thái của cuộc (RAM, cookie HttpOnly sẵn có — `ConversationStore.hoan_tac`). Mã khớp lịch đang
lưu và cuộc còn bản trước ⇒ lịch của cuộc trở về bản đó, trả thẻ lịch dựng bằng đúng hàm của sổ tay / file tải (`xuat.lich_tu_luu`: quán ăn, ghi chú, giờ
đều theo khung cũ) + một câu do code viết nêu lần sửa vừa được hoàn tác; ô lịch sử có thêm một lượt ghi chú để lượt hỏi kế hiểu lịch đã trở lại.
Không khớp (lịch đã đổi thêm, nút của lần sửa cũ, đã hoàn tác rồi, cuộc hết hạn / server khởi động lại) ⇒ 409, lịch giữ nguyên. Chỉ MỘT bước."""
from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from api.conversations import GHI_CHU_SUA_DAU
from api.routes.chat import CONVERSATION_COOKIE, _flags, error_response
from api.routes.xuat import lich_tu_luu

router = APIRouter()
CAU_HOI = "Hoàn tác lần sửa lịch vừa rồi"  # chữ của ô câu hỏi trong lịch sử cuộc (do code đặt — lần bấm nút không có chữ người dùng)
CAU_DA_HOAN_TAC = "Đã hoàn tác lần sửa «{dong}» — lịch trở lại như trước lần sửa đó."  # dòng của lần sửa đứng trong «…»: nó tả lịch SAU lần sửa ("…nay để trống")
CAU_KHONG_DUOC = "Không hoàn tác được nữa: lịch đã đổi thêm sau lần sửa đó, hoặc lần sửa đó đã được hoàn tác."


class HoanTac(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ma: str = Field(min_length=1, max_length=64)


@router.post("/api/lich/hoan_tac")
def hoan_tac(body: HoanTac, request: Request):
    state = request.app.state
    flags = _flags(state)
    if not getattr(flags, "sua_lich_hoan_tac", False):
        return error_response(404, "not_found", "Tính năng này chưa bật.")
    store = getattr(state, "conversations", None)
    cid = request.cookies.get(CONVERSATION_COOKIE)
    ra = store.hoan_tac(cid, body.ma) if store is not None else None
    if ra is None:
        return error_response(409, "khong_hoan_tac_duoc", CAU_KHONG_DUOC)
    luu, dong = ra
    cau = CAU_DA_HOAN_TAC.format(dong=" ".join(dong))
    store.append(cid, CAU_HOI, "", f"{GHI_CHU_SUA_DAU}{cau}]")
    lich, cau_muc = lich_tu_luu(luu, flags)
    # `lich`: đối tượng lịch như thẻ của một lượt lịch (không `thay_doi`, không `hoan_tac`, số nguồn của mục là null, không dòng dự báo); `cau_muc`: câu tả theo mã mục
    return {"trang_thai": "da_hoan_tac", "cau": cau, "lich": lich, "cau_muc": cau_muc}
