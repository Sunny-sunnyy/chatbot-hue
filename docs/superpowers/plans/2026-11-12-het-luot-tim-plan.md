# Plan (mức nhẹ) — hết lượt tìm kho thì không để model xin tìm nữa · **NHÁP — chờ User chọn**

Người viết: C, 19:30 12/11/2026 (`date`), A giao. Chưa code, 0 USD.

## Căn cứ để review

- Số đếm: `report_agent/2026-11-12_ra_khoang_cach/c_phan_chua_on.md` mục 3b (b), (b2).
- Code: `backend/llm/assistant.py` (`MODEL_SEARCH_LIMIT`, hàm `tool_for_turn` / `tim_kho`) · `backend/llm/generator_openai_full_corpus.py` (`ASSISTANT_MAX_TURNS`, `max_turns_for`, chỗ dựng danh sách công cụ của trợ lý) · `backend/llm/full_corpus_prompt.py` (`TOOL_LIMIT_TEXT`).
- Sàn: spec Phase 9 §12.3.

## 1. Lỗi đã đếm

Hôm nay model được tìm kho thật 2 lần; xin lần thứ ba thì code trả chữ "đã hết lượt" — nhưng **lần xin đó vẫn là một lượt gọi model**, rồi thêm một lượt nữa để viết câu trả lời.
- 8 câu "kho thiếu hẳn" gửi qua server thật 12/11: **6 / 8 câu** có lượt xin thứ ba bị chặn; cả câu trung vị 22,9 giây, trong đó 10–20 giây là 3–4 lượt gọi model trước khi từ chối.
- Golden trong kho (158 câu): **0 câu** dùng tới lượt thứ ba; hai lần tìm thật cứu 10 câu ⇒ **giữ nguyên hai lần tìm**.

## 2. Việc đề xuất (bản hẹp)

Khi model đã dùng hết 2 lần tìm thật, **lượt gọi model kế tiếp không còn công cụ `tim_kho`** ⇒ model buộc phải viết câu trả lời / câu từ chối ngay. Bớt đúng một lượt gọi model ở các câu trên.

- **Chỗ sửa:** `generator_openai_full_corpus.py`, nơi bọc `tim_kho` thành công cụ — thêm điều kiện bật / tắt theo số lần đã tìm (`trace.model_searches < MODEL_SEARCH_LIMIT`), đọc từ `assistant.py`. `ASSISTANT_MAX_TURNS` giảm tương ứng nếu probe cho thấy an toàn. `TOOL_LIMIT_TEXT` giữ làm dự phòng.
- **Probe 0 USD trước khi code** (bắt buộc — đây là khẳng định về hành vi thư viện): thư viện agent đang dùng (bản 0.19.4) có trường `is_enabled` trên công cụ; cần xác nhận nó được xét lại **mỗi lượt** trong một lần chạy, và ở đường stream. Không được ⇒ phương án 2: dừng vòng bằng `tool_use_behavior` dạng hàm (đã dùng cho thẻ hỏi lại) — ghi vào report, không tự mở rộng.
- **Cờ:** `assistant.het_luot_bo_cong_cu` (mặc định tắt cho tới khi đo đạt).
- **Chuỗi gửi model đổi ở đâu:** chỉ ở lượt gọi **sau lần tìm thật thứ hai** — danh sách công cụ thiếu `tim_kho`. Mọi lượt trước đó, lời dặn, mô tả công cụ: giống byte. Câu không tìm thêm hoặc tìm thêm 1 lần: giống byte hoàn toàn. Lượt có lịch trình / thời tiết / ngày: các công cụ đó không đổi.

## 3. Tiêu chí ghi trước

| | Mức | Đo bằng |
|---|---|---|
| **Quyết — tốc độ câu kho thiếu** | số lượt gọi model của trợ lý trước khi từ chối giảm ≥ 1 ở ≥ 5 / 8 câu; thời gian cả câu trung vị giảm ≥ 2 giây; USD / câu không tăng | 8 câu đi web của lượt đếm 12/11 (đã có số "trước" trên `main`) + 8 câu kho-thiếu **mới** (viết trước khi đo), qua server thật, 1 lượt |
| Sàn — không mất câu đang cứu được | trong 26 câu Golden có tìm thêm ở B7 giữa kỳ: 0 câu chuyển từ trả lời sang từ chối; số đoạn mới tìm được không giảm | chạy lại đúng 26 câu đó (đường chỉ-kho), so với file B7 |
| Sàn an toàn 32 ×2 | 4 số như mọi bậc (0 / 0 mới / 0 mới / 0) | bộ an toàn |
| Sàn ngoài phạm vi | 0 câu ngoài phạm vi bị trả lời; cổng web không mở thêm ở câu ngoài phạm vi | 44 câu S2 ×1 (có số "trước" từ B7) |
| Giống byte khi cờ tắt | 228 / 228 | Q1 sẵn có |
| Test theo loại lượt | lượt đầu · lượt sau 1 lần tìm · lượt sau 2 lần tìm · lượt có lịch sử · lượt biểu mẫu: chuỗi gửi model có / không có `tim_kho` đúng như mục 2 | test mới (0 USD) |

Không đạt "quyết" hoặc phạm sàn ⇒ cờ tắt, tag hồ sơ, không chỉnh rồi đo lại quá 1 vòng.

## 4. Tiền · giờ · file chạm

- **Tiền ≤ 0,09 USD:** 16 câu kho thiếu (đường web ≈ 0,002) 0,032 · 26 câu Golden 0,015 · an toàn 32 ×2 0,03 · S2 44 câu 0,009. Mốc "trước" lấy từ B7 giữa kỳ + lượt đếm 12/11 (cùng `main`) ⇒ không sinh lại.
- **Giờ:** ~2 giờ agent (probe 15 phút · code + test 45 phút · đo 30 phút · report + review).
- **Chạm:** `backend/llm/generator_openai_full_corpus.py` · `backend/llm/assistant.py` (cờ) · `backend/config/settings.yaml` · 1 file test mới. Không chạm kho, chỉ mục, lời dặn.

## 5. Khi nào sai

- Model, khi mất công cụ, viết câu trả lời "cố" từ bằng chứng yếu thay vì từ chối ⇒ sàn ngoài kho / an toàn sẽ bắt; đó là lý do giữ đủ hai sàn dù việc nhỏ.
- Lợi nhỏ hơn dự kiến nếu phần lớn 10–20 giây nằm ở hai lần tìm thật chứ không ở lượt xin thứ ba ⇒ tiêu chí "≥ 2 giây" sẽ trượt, đóng hồ sơ.

## 6. Cần User chọn

Làm / không làm; trần 0,09 USD. (Không đổi kiến trúc ⇒ mức nhẹ: A đọc plan rồi duyệt, một review cả nhánh.)
