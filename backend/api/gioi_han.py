"""Chốt trước deploy (checklist E-dep #1 a): giới hạn lượt gọi model theo IP / ngày, đếm trong RAM — đủ cho một máy chủ một tiến trình.

Bật bằng biến môi trường `HUE_LUOT_MOI_NGAY=<n>` (> 0); không đặt / 0 ⇒ tắt (hành vi như trước). Ngày theo giờ Việt Nam; sang ngày mới ⇒ xoá sổ đếm.
IP = địa chỉ kết nối (`scope["client"]`) — sau proxy phải chạy uvicorn `--proxy-headers --forwarded-allow-ips <ip proxy>`; không tự đọc `X-Forwarded-For` (giả mạo được).
Không log IP (dữ liệu cá nhân)."""
import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi.responses import JSONResponse

logger = logging.getLogger("api")

LUOT_MOI_NGAY_ENV = "HUE_LUOT_MOI_NGAY"
DUONG_TINH_LUOT = frozenset({"/api/chat", "/api/chat/stream", "/api/anh/ung_vien"})  # các đường gọi model (tốn tiền)
LOI_BAO = "Bạn đã dùng hết số lượt hỏi hôm nay. Vui lòng quay lại vào ngày mai."
_VN = ZoneInfo("Asia/Ho_Chi_Minh")


def tran_tu_moi_truong() -> int:
    """Số lượt / IP / ngày từ biến môi trường; không đặt, rỗng, không phải số nguyên dương ⇒ 0 (tắt)."""
    try:
        return max(int(os.getenv(LUOT_MOI_NGAY_ENV, "0").strip() or 0), 0)
    except ValueError:
        return 0


class GioiHanLuot:
    def __init__(self, tran: int):
        self.tran = tran
        self._ngay = None
        self._dem: dict[str, int] = {}

    def cho_qua(self, ip: str, hom_nay=None) -> bool:
        """Tính một lượt cho `ip`; False khi đã đủ `tran` lượt hôm nay (lượt bị chặn không cộng thêm)."""
        hom_nay = hom_nay or datetime.now(_VN).date()
        if hom_nay != self._ngay:
            self._ngay, self._dem = hom_nay, {}
        if self._dem.get(ip, 0) >= self.tran:
            return False
        self._dem[ip] = self._dem.get(ip, 0) + 1
        return True


class ChanLuot:
    """Middleware ASGI thuần (không `BaseHTTPMiddleware`: lớp đó bọc luồng SSE và việc dò ngắt kết nối của nút Dừng). POST tới đường gọi model mà IP
    đã hết lượt ⇒ 429 JSON cùng khuôn lỗi của API (giao diện hiện `error.message`), không chạm route."""

    def __init__(self, app, gioi_han: GioiHanLuot):
        self.app, self.gioi_han = app, gioi_han

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope["method"] == "POST" and scope["path"] in DUONG_TINH_LUOT:
            ip = (scope.get("client") or ("khong_ro", 0))[0]
            if not self.gioi_han.cho_qua(ip):
                logger.warning(f"Rate limited: {scope['path']}")  # không ghi IP
                await JSONResponse(status_code=429, content={"error": {"code": "rate_limited", "message": LOI_BAO}})(scope, receive, send)
                return
        await self.app(scope, receive, send)
