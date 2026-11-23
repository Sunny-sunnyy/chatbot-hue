"""Lớp mỏng quanh model OpenAI của SDK cho đường `provider: openai` (bản deploy dùng đường này — chủ dự án chốt 23/11/2026).

Hai việc, đều ở LỚP MODEL như bản Bedrock (`bedrock_model.py`, `MA_GOI_LAI`):
1. Lời gọi model hỏng ⇒ ghi một dòng log ĐẾM ĐƯỢC: loại lỗi của thư viện + mã HTTP. Trước đây lỗi gốc bị gói thành `GenerationError` ở generator,
   log chỉ còn tên lớp đó ⇒ không biết lỗi là 500, 429 hay rớt mạng. Không ghi thân lỗi (có thể mang chữ của yêu cầu).
2. Lỗi THOÁNG QUA phía nhà cung cấp — 5xx hoặc lỗi kết nối — ⇒ gọi lại ĐÚNG MỘT lần. KHÔNG gọi lại: hết giờ (gọi lại là chờ gấp đôi), 4xx (401 khoá
   sai, 429 hết hạn mức / hết tiền — gọi lại không chữa được). Client dựng `max_retries=0` nên thư viện không tự gọi lại; `max_retries=1` của chính thư
   viện không dùng được vì nó gọi lại cả hết giờ, 408, 409, 429.
   Đường chữ chạy dần: chỉ gọi lại khi CHƯA sự kiện nào đi ra (lỗi 5xx tới lúc mở yêu cầu, trước mọi sự kiện); đã có sự kiện ⇒ lỗi đi ra như cũ —
   gọi lại lúc đó là phát trùng chữ người dùng đã thấy.
Căn cứ đo: 0 lỗi nhà cung cấp / 2.169 lượt thật trước 21/11 ⇒ đây là lưới cho ngày demo, không phải chữa lỗi đang gặp."""
import logging

from agents import OpenAIResponsesModel
from openai import APIConnectionError, APIStatusError, APITimeoutError

logger = logging.getLogger("llm.full_corpus")


def goi_lai_duoc(exc: BaseException) -> bool:
    """5xx hoặc lỗi kết nối. `APITimeoutError` là lớp CON của `APIConnectionError` ⇒ phải loại ra trước."""
    if isinstance(exc, APITimeoutError):
        return False
    return isinstance(exc, APIConnectionError) or (isinstance(exc, APIStatusError) and exc.status_code >= 500)


def _ghi(nhan: str, exc: BaseException) -> None:
    logger.warning("%s loai=%s status=%s", nhan, type(exc).__name__, getattr(exc, "status_code", None))


class OpenAIGoiLaiModel(OpenAIResponsesModel):
    async def get_response(self, *args, **kwargs):
        try:
            return await super().get_response(*args, **kwargs)
        except Exception as exc:
            if not goi_lai_duoc(exc):
                _ghi("openai_loi", exc)
                raise
            _ghi("openai_goi_lai", exc)
        try:
            return await super().get_response(*args, **kwargs)
        except Exception as exc:
            _ghi("openai_loi", exc)
            raise

    async def stream_response(self, *args, **kwargs):
        da_phat = False
        try:
            async for su_kien in super().stream_response(*args, **kwargs):
                da_phat = True
                yield su_kien
            return
        except Exception as exc:
            if da_phat or not goi_lai_duoc(exc):
                _ghi("openai_loi", exc)
                raise
            _ghi("openai_goi_lai", exc)
        try:
            async for su_kien in super().stream_response(*args, **kwargs):
                yield su_kien
        except Exception as exc:
            _ghi("openai_loi", exc)
            raise
