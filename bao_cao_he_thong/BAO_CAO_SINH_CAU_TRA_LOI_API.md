# Báo cáo cho bạn: Phase 6 — Sinh câu trả lời, API và giao diện

```text
Trạng thái: Đã đóng 23/10/2026 (Đạt kèm giới hạn F1, F2)
Cập nhật lúc: 24-10-2026 +07
Người viết: C · Review: A
```

## 1. Bạn nhận được gì

Chatbot Huế **trả lời được câu hỏi trên toàn bộ kho dữ liệu** (món ăn, di tích, lễ hội, nghệ thuật,
du lịch) qua một API và một trang web đơn giản. Mỗi câu trả lời có trích dẫn `[1]`, `[2]`… trỏ tới
đoạn nguồn thật trong kho. Không tìm thấy thông tin thì chatbot nói không đủ thông tin, không bịa.

Ví dụ: hỏi về đồi Vọng Cảnh → câu trả lời có `[1]`; bấm `[1]` trên trang web sẽ cuộn tới thẻ nguồn
ghi tiêu đề, mục và đoạn trích nguyên văn.

Phase 6 cũng có hai đời: đời Foods (08/2026, `gpt-5.4-nano`) và đời toàn corpus (đổi model nhiều lần:
Qwen → `gpt-5.4-nano` → `gpt-6-luna`, đóng 23/10/2026).

## 2. Hệ thống hoạt động như thế nào

```text
trang web / POST /api/chat {"query": "..."}
 → tìm 10 đoạn (Phase 5) → lấy tối đa 5 đoạn nguyên vẹn, vừa ngân sách token
 → gpt-6-luna viết câu trả lời, chỉ dùng 5 đoạn đó, đặt [n] sau mỗi ý
 → backend kiểm từng [n] có trỏ đúng nguồn đã đưa không
 → trả {answer, sources} — hoặc lỗi có mã rõ ràng (vd. 500 nếu trích dẫn hỏng)
```

- Khi khởi động, hệ thống so "dấu vân tay" dữ liệu với chỉ mục; dữ liệu đổi mà chưa build lại thì
  từ chối chạy.
- Câu hỏi 1–500 ký tự (sau khi bỏ khoảng trắng đầu/cuối).

## 3. Đã chạy và quan sát gì

| Nội dung | Kết quả | Ý nghĩa |
|---|---|---|
| Lúc đóng (23/10): 5 câu thật với `gpt-6-luna` | 4 đạt / 1 không đạt | Câu không đạt: "giá vé + miễn giảm" — không tìm ra bảng giá (F2) |
| Câu tổng hợp nhiều nguồn lúc đóng | Đạt nhưng chỉ dùng 1 nguồn | Chưa chứng minh tổng hợp nhiều nguồn (F1) |
| Đo đủ ở Phase 7B (176 câu, 24/10) | Đúng/Đủ/Trúng ý 4,43 / 4,28 / 4,45 | Khi đã trả lời thì gần tối đa (~4,9) |
| Từ chối đúng câu ngoài kho | 18/18 | Không bịa |
| Từ chối nhầm câu có trong kho | 22/158 | Nguồn mất điểm lớn nhất |
| Lỗi trích dẫn (người dùng thấy lỗi 500) | 4/176 | Hiếm |
| Chi phí sinh 176 câu | ~0,024 USD | Rẻ |

Số 7B là lần đo mới trên chỉ mục 7A2 (cùng code Phase 6); số lúc đóng là của 23/10.

## 4. Cách bạn kiểm tra thêm nếu cần

Không bắt buộc. Muốn tự hỏi chatbot: bật Qdrant (`docker compose up -d`), chạy API từ `backend/`
(`HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8000`), mở
`http://localhost:8000`. Mỗi câu hỏi gọi `gpt-6-luna` (có phí rất nhỏ).

## 5. Hôm nay còn đúng không

Kiểm với code và `session_prompt/Project_Status.md` §4 ngày 24/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ |
|---|---|---|
| API `POST /api/chat`, trả `{answer, sources}`, câu hỏi 1–500 ký tự | **còn dùng** | `backend/api/routes/chat.py:24–26,48` |
| Model sinh `gpt-6-luna` (OpenAI) | **còn dùng** | `backend/config/settings.yaml:117` |
| Tối đa 5 đoạn nguyên vẹn, ngân sách 16.384 token | **còn dùng**; Phase 8 sẽ thử 10 đoạn | `settings.yaml:123,126`; `backend/retrieval/full_corpus_context.py` |
| Prompt "thiếu bằng chứng thì từ chối cả câu" | **còn dùng**; Phase 8 xem xét cho trả lời phần có căn cứ (bạn quyết) | `backend/llm/full_corpus_prompt.py:14` |
| Backend kiểm trích dẫn, lỗi trả mã rõ ràng | **còn dùng** | `backend/llm/citations.py:12`; `backend/api/routes/chat.py` |
| Trang web tối giản, bấm `[n]` tới thẻ nguồn | **còn dùng** | `frontend/`; `backend/api/app.py:147–151` |
| Từ chối chạy khi dữ liệu lệch chỉ mục | **còn dùng** | `backend/retrieval/full_corpus.py:353,415` |
| Qdrant cổng 6335 | **còn dùng** | `settings.yaml` `vector_database.url` |
| Qwen 3.5-9B qua OpenRouter, `gpt-5.4-nano` | **đã thay** bởi `gpt-6-luna` (amendment 23/10) | `docs/superpowers/specs/2026-10-23-phase-6-gpt-6-luna-amendment.md` |
| Collection metadata v2 (8.460 đoạn) mà Phase 6 đóng trên đó | **đã thay** bởi chỉ mục 7A2 (8.459 đoạn) | `Project_Status.md` §4 |
| "Representation B" (LLM viết thêm ngữ cảnh cho đoạn) | **có code, chưa từng dùng** | `backend/llm/full_corpus_prompt.py:37` |
| API/sinh câu trả lời đời Foods | **đã bỏ, hỏng thật**: gửi `temperature` nên `gpt-6-luna` trả lỗi 400; nằm trong danh sách dọn | `backend/llm/generator_openai.py:30,44` |

## 6. Giới hạn và bước tiếp theo

- **F2 bảng giá** và **F1 tổng hợp nhiều nguồn** vẫn còn (xem Phase 5 và 7B).
- 22 câu từ chối nhầm: 8 do không tìm ra đoạn, 10 có một vế thiếu vế kia, 4 có đủ mà vẫn từ chối.
  Thử nhanh 10 đoạn ngữ cảnh: 10/22 câu hết từ chối (chưa chấm đúng/sai).
- Phase 8 sẽ thử: 10 đoạn ngữ cảnh, prompt cho trả lời phần có căn cứ, tách câu hỏi hai ý.

## Lệch phát hiện

- Spec chung (2026-09-11 §1, Decision #6a) cho phép "trả phần có căn cứ", nhưng spec Phase 6
  (2026-09-14 §10) và prompt bắt từ chối cả câu khi bằng chứng không đủ. Code đúng theo spec Phase 6;
  đây là lựa chọn của bạn ở Phase 8 (đã báo A từ C1).
- Guide `guides/full_corpus_rag.md` (Decision #6d, lịch sử) còn ghi "dùng `AsyncOpenAI` trực tiếp,
  không Agent/Runner"; code dùng OpenAI Agents SDK một lượt, không tool
  (`backend/llm/generator_openai_full_corpus.py`) — **đúng** theo amendment 2026-10-01 §SDK boundary
  (`docs/superpowers/specs/2026-10-01-phase-6-openai-baseline-amendment.md:29,59`). Không phải lỗi code;
  chỉ là đoạn guide lịch sử dễ gây hiểu nhầm.
