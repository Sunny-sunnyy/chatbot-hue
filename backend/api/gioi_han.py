"""Chốt trước deploy (checklist E-dep #1 a): giới hạn lượt gọi model theo IP / ngày, đếm trong RAM — đủ cho một máy chủ một tiến trình.

Bật bằng biến môi trường `HUE_LUOT_MOI_NGAY=<n>` (> 0); không đặt / 0 ⇒ tắt (hành vi như trước). Ngày theo giờ Việt Nam; sang ngày mới ⇒ xoá sổ đếm.
Thêm 22/11 (rà bảo mật trước deploy): `HUE_LUOT_TONG_MOI_NGAY=<n>` = trần TỔNG lượt gọi model mỗi ngày của cả máy chủ (mọi IP cộng lại; không đặt ⇒ tắt)
— lớp chặn chi tiêu thứ hai khi nhiều địa chỉ cùng gọi; và khi bộ giới hạn đang bật, lượt tải file lịch `.pptx` (GET) cũng được đếm theo IP / ngày
(`TRAN_TAI_FILE`). Chỉ cần MỘT trong hai biến được đặt là bộ giới hạn bật.
IP = địa chỉ kết nối (`scope["client"]`) — sau proxy phải chạy uvicorn `--proxy-headers --forwarded-allow-ips <ip proxy>`; không tự đọc `X-Forwarded-For` (giả mạo được).
Không log IP (dữ liệu cá nhân)."""
import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi.responses import JSONResponse

logger = logging.getLogger("api")

LUOT_MOI_NGAY_ENV = "HUE_LUOT_MOI_NGAY"
LUOT_TONG_ENV = "HUE_LUOT_TONG_MOI_NGAY"
# Trọng số lượt gọi model theo đường dẫn (chống cost-amplification): chat/ảnh thường = 1; Sổ tay (<= 9-10 call) = 10; Hồ sơ chủ đề (<= 3-9 call) = 8.
TRONG_SO_DUONG: dict[str, int] = {
    "/api/chat": 1,
    "/api/chat/stream": 1,
    "/api/anh/ung_vien": 1,
    "/api/so_tay": 10,
    "/api/ho_so": 8,
    "/api/lich/pptx": 3,  # Đợt 5A (Slide Designer Agent, POST tối đa 1 + max_retries=2 = 3 lượt gọi model)
}
DUONG_TINH_LUOT = frozenset(TRONG_SO_DUONG)  # các đường gọi model (tốn tiền)
DUONG_TAI_FILE = "/api/lich/pptx"  # GET: dựng file .pptx từ lịch đã lưu (không gọi model, nhưng tốn CPU + băng thông)
# 30 lượt tải / IP / ngày: một lịch thường tải một hai lần, sửa lịch rồi tải lại vài lần nữa; 30 đủ cho một nhóm dùng chung một mạng mà vẫn chặn vòng lặp tải
TRAN_TAI_FILE = 30
LOI_BAO = "Bạn đã dùng hết số lượt hỏi hôm nay. Vui lòng quay lại vào ngày mai."
LOI_BAO_TONG = "Hôm nay trợ lý đã nhận đủ số lượt hỏi cho phép. Vui lòng quay lại vào ngày mai."
LOI_BAO_TAI_FILE = "Bạn đã tải file quá số lần cho phép hôm nay. Vui lòng quay lại vào ngày mai."
_VN = ZoneInfo("Asia/Ho_Chi_Minh")


def tran_tu_moi_truong(ten: str = LUOT_MOI_NGAY_ENV) -> int:
    """Số lượt / ngày từ một biến môi trường (mặc định: số lượt / IP); không đặt, rỗng, không phải số nguyên dương ⇒ 0 (tắt)."""
    try:
        return max(int(os.getenv(ten, "0").strip() or 0), 0)
    except ValueError:
        return 0


class GioiHanLuot:
    def __init__(self, tran: int, tran_tong: int = 0):
        self.tran, self.tran_tong = tran, tran_tong  # 0 = không giới hạn loại đó
        self._ngay = None
        self._dem: dict[str, int] = {}
        self._tong = 0

    def chan(self, ip: str, hom_nay=None, tai_file: bool = False, trong_so: int = 1) -> str | None:
        """Tính `trong_so` điểm lượt cho `ip`; trả LỜI BÁO khi số điểm còn lại < `trong_so` (không cộng thêm), None khi cho qua.
        `tai_file`: lượt tải file, đếm riêng (luôn trọng số 1)."""
        if not tai_file and trong_so < 1:
            raise ValueError("trong_so must be >= 1")
        hom_nay = hom_nay or datetime.now(_VN).date()
        if hom_nay != self._ngay:
            self._ngay, self._dem, self._tong = hom_nay, {}, 0
        buoc = 1 if tai_file else trong_so
        khoa, tran = (f"tai_file|{ip}", TRAN_TAI_FILE) if tai_file else (ip, self.tran)
        if tran and self._dem.get(khoa, 0) + buoc > tran:
            return LOI_BAO_TAI_FILE if tai_file else LOI_BAO
        if not tai_file and self.tran_tong and self._tong + buoc > self.tran_tong:
            return LOI_BAO_TONG
        self._dem[khoa] = self._dem.get(khoa, 0) + buoc
        if not tai_file:
            self._tong += buoc
        return None

    def cho_qua(self, ip: str, hom_nay=None, trong_so: int = 1) -> bool:
        """Tính `trong_so` lượt gọi model cho `ip`; False khi đã hết lượt hôm nay."""
        return self.chan(ip, hom_nay, trong_so=trong_so) is None


class ChanLuot:
    """Middleware ASGI thuần (không `BaseHTTPMiddleware`: lớp đó bọc luồng SSE và việc dò ngắt kết nối của nút Dừng). POST tới đường gọi model, hoặc
    GET tải file lịch, mà đã hết lượt ⇒ 429 JSON cùng khuôn lỗi của API (giao diện hiện `error.message`), không chạm route."""

    def __init__(self, app, gioi_han: GioiHanLuot):
        self.app, self.gioi_han = app, gioi_han

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            method, path = scope["method"], scope["path"]
            tai_file = method == "GET" and path == DUONG_TAI_FILE
            trong_so = TRONG_SO_DUONG.get(path) if method == "POST" else None
            if tai_file or trong_so is not None:
                loi = self.gioi_han.chan(
                    (scope.get("client") or ("khong_ro", 0))[0],
                    tai_file=tai_file,
                    trong_so=trong_so or 1,
                )
                if loi:
                    logger.warning(f"Rate limited: {path}")  # không ghi IP
                    await JSONResponse(status_code=429, content={"error": {"code": "rate_limited", "message": loi}})(scope, receive, send)
                    return
        await self.app(scope, receive, send)
