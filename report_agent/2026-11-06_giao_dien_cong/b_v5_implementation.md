# Implementation Report: V5 vào lượt biểu mẫu (nhánh `p11-cong-dot-1` `632a4f7`)

Người làm: B (Claude Code, Opus 5.5) · 13:19 07/11/2026 (`date`) · A giao sau X1c của C (`c_x1_luot_bieu_mau.md` §6). Cờ `lich_trinh_bieu_mau` vẫn tắt; merge / bật chờ S3 + User (đổi lời dặn ngoài phạm vi spec).

## Thay đổi

Chỉ lần gọi model của lượt biểu mẫu đổi; mọi lượt khác gọi `answer_agent` như cũ.
- `llm/generator_openai_full_corpus.py`:
  - `bieu_mau_agent` = agent trả lời, lời dặn = lời dặn trả lời + `\n\n` + `LICH_TRINH_LUAT`, `reasoning.effort = "low"` (`BIEU_MAU_REASONING`) — đúng cấu hình C đo;
  - `generate_answer` / `start_answer_stream` thêm `bieu_mau=False`.
- `llm/assistant.py`: đường biểu mẫu (stream + không stream) truyền `bieu_mau=True`.
- Trước đó: merge `main` `0dab4e5` vào nhánh (tua thẳng).

## Bằng chứng [Chạy]

- **Test mỗi loại lượt** (`tests/test_cong_dot_1.py`, 20 / 20):
  - lượt biểu mẫu đầu (stream / không stream, có / không lịch sử) gửi lời dặn có luật + `low`;
  - lượt hỏi tiếp sau biểu mẫu: không luật, không `low`, giống `PROD`.
  - Generator: 26 đạt, 2 lỗi = test cần khoá (như cũ).
- **Q1:** chuỗi gửi model của 228 lượt thường **giống byte** giữa nhánh và `main` mới `0dab4e5` (cùng cờ, thời tiết bật). Mốc mới `data/phase_11/cong_dot_1/q1/main_0dab4e5.jsonl` sha `d9bdb467a501` — mốc cũ `dba1f578eef1` không còn dùng vì thời tiết đã bật.
- **1 lượt thật** (tổ hợp 2 ngày · gia đình có trẻ em · di tích, server bật cờ, stream):
  - model tự viết lời lịch — cùng tổ hợp này trước đây bị từ chối ở pilot sau (e);
  - kiểm cuối qua; 4 nguồn; chữ đầu **3,1 s**, cả lượt 4,9 s; 109 token suy luận; **0,00037 USD**.
  - Đây là thử khả thi, không phải lượt quyết định (S3 của C).

## Review chéo dòng test A sửa (`0dab4e5`)

**Đúng.** `settings.yaml` bật `thoi_tiet` ⇒ `PROD` có cờ bật ⇒ ca "cờ tắt ⇒ 404" phải đặt rõ `dataclasses.replace(PROD, thoi_tiet=False)`. Cờ tắt thì không kiểm tới `du_bao`; các ca "cờ bật" sau đó vẫn tự đặt hàm dự báo ghi sẵn.

**Giải thích ngắn:** lượt "Lên kế hoạch" nay đưa luật viết lịch vào lời dặn hệ thống và cho model suy nghĩ ít hơn — cách C đo không còn từ chối mà chữ đầu nhanh hơn. Lượt hỏi đáp thường không đổi gì (đã so đủ 228 lượt).
