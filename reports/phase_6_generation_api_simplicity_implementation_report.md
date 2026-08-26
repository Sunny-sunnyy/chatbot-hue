# Implementation Report: Phase 6 Generation API Simplicity

Implementer: DeepSeek & Antigravity
Date: 2026-08-26 (Revision 1 - Corrections applied)
Canonical guide: `guides/phase_6_generation_api.md`
Codex review: `reports/phase_6_generation_api_simplicity_codex_review.md`

---

## 1. Phạm vi

Triển khai đầy đủ thiết kế đơn giản hóa Phase 6 theo đúng spec `docs/superpowers/specs/2026-08-25-phase-6-generation-api-simplicity-design.md`, plan `docs/superpowers/plans/2026-08-25-phase-6-generation-api-simplicity-implementation.md` và giải quyết toàn bộ findings trong Codex review vòng 1:

- Thu gọn luồng RAG thành single-turn tuyến tính: `query -> retrieval -> ContextBuilder.build(documents) -> labeled str -> OpenAIAnswerGenerator.generate_answer(query, context) -> str -> {"answer": "..."}`.
- Loại bỏ toàn bộ `ContextResult`, JSON evidence array, `used_source_ids`, parallel sources mapping, `session_id`, `retrieval_debug`, 4 generation exception classes và các public error codes chi tiết.
- Bắt `AgentsException` bao gồm cả `ModelRefusalError` và `ModelBehaviorError` cùng `OpenAIError`, gom thành một `GenerationError` nội bộ, đảm bảo route trả HTTP 503 rõ ràng khi có lỗi SDK/provider thay vì lọt thành HTTP 500.
- Chuẩn hóa public error status về `422`, `503`, `500` với thông báo tiếng Việt cố định.
- Ghi log backend tuyến tính, dễ đọc ra console và `backend/logs/application.log` mà không để lọt log/debug/exception vào API response.
- Migrate downstream Phase 7 (`eval.py`), Notebook 05 (`05_retrieval_profiles.ipynb`), Notebook 06 (`06_generation_and_api.ipynb`).
- Sửa Notebook 06 dùng chung một biến `question`, bỏ forced `HF_HUB_OFFLINE=1`. Sửa Notebook 05 bỏ mô tả stale `context source count`.
- Bảo toàn nguyên vẹn file `backend/evaluation/retrieval_results.csv` của người dùng; static-audit Notebook 07.

---

## 2. Thay đổi chính

| File | Mục đích và vai trò |
|---|---|
| `backend/retrieval/context_builder.py` | Ghép tối đa 5 whole chunks / 3.000 ký tự thành 1 chuỗi text gắn nhãn `[Nguồn n] Tiêu đề / Mục / Nội dung`; trả `""` khi rỗng; bỏ `ContextResult` và source list. |
| `backend/llm/prompt.py` | Chứa `INSUFFICIENT_ANSWER`, `SYSTEM_INSTRUCTIONS` và hàm `build_user_message(query, context)` gồm 2 phần rõ ràng; không lặp policy vào user message. |
| `backend/llm/generator_openai.py` | Sử dụng 1 `Agent` cố định không tool với `output_type=AnswerOutput(answer: str)`; bắt `(asyncio.TimeoutError, AgentsException, OpenAIError)` ném `GenerationError` nội bộ; method `generate_answer(query, context) -> str` unwrap và trả chuỗi; log stage/latency/tokens. |
| `backend/core/schema.py` | Gom 4 exception cũ (`GeneratorNotConfiguredError`, `GeneratorTimeoutError`, `GeneratorUnavailableError`, `InvalidGeneratorOutputError`) thành một `GenerationError`. |
| `backend/api/routes/chat.py` | Route `/api/chat` single-turn gọn gàng: validate query, gọi retrieval qua thread pool, build context, zero-model fallback khi rỗng, gọi generator async và trả `ChatResponse(answer: str)`. Bắt `GenerationError` trả HTTP 503. |
| `backend/api/app.py` | Quản lý lifespan khởi tạo component 1 lần, lưu cached readiness trong `app.state`, bắt `RequestValidationError` (422) và `Exception` (500) với body `{"detail": "..."}`. |
| `backend/evaluation/eval.py` | Cập nhật `evaluate_answer` nhận context string và generator string, dùng `INSUFFICIENT_ANSWER` khi context rỗng. |
| `backend/evaluation/answer_results.csv` | Lưu kết quả chạy batch evaluation 20 câu với `gpt-5.4-nano` và judge `gpt-5.4-mini`. |
| `backend/tests/test_context_builder.py` | Rút gọn 3 behavior tests: labeled whole chunks, budget cap dừng trước chunk vượt ngưỡng, empty/blank input. |
| `backend/tests/test_llm_generator_openai.py` | Giữ 3 tests: prompt/runner structure, `AnswerOutput` schema, và 1 real call `gpt-5.4-nano`. |
| `backend/tests/test_api_chat.py` | Giữ import/health test, validation 422, pre-lifespan 503, no-context fallback (zero model), 1 real answer-only chat test kèm backend log verification, và 2 real warm-up tests từ Milestone 6.1. |
| `notebooks/05_retrieval_profiles.ipynb` | Cập nhật hiển thị ContextBuilder dạng chuỗi (`len(context)`), sửa mô tả stale `context character count`, làm sạch output. |
| `notebooks/06_generation_and_api.ipynb` | Cập nhật minh họa API trả về duy nhất trường `answer`, dùng đúng 1 biến `question`, bỏ `HF_HUB_OFFLINE`, làm sạch output. |

---

## 3. Cách đã chạy thật

Toàn bộ quá trình triển khai và kiểm tra sử dụng dữ liệu thật, Qdrant thật (`localhost:6333`, collection `hue_foods_e5_small_384` 572 points và guarded test collections `hue_rag_live_test_*`), model embedding thật (`intfloat/multilingual-e5-small`), model reranking thật (`cross-encoder/ms-marco-MiniLM-L-6-v2`), và OpenAI API thật (`gpt-5.4-nano`, `gpt-5.4-mini`):

```bash
# 1. Python compilation check
uv run python -m py_compile \
  backend/retrieval/context_builder.py backend/llm/prompt.py backend/llm/generator_openai.py \
  backend/api/app.py backend/api/routes/chat.py backend/evaluation/eval.py

# 2. Targeted tests của Phase 6 (17 tests)
PYTHONPATH=backend uv run --env-file .env python -m pytest \
  backend/tests/test_context_builder.py \
  backend/tests/test_llm_generator_openai.py \
  backend/tests/test_api_chat.py -v

# 3. Reviewer exact test command (10 tests)
cd backend && uv run --env-file ../.env python -m pytest \
  tests/test_context_builder.py \
  tests/test_llm_generator_openai.py::test_prompt_keeps_policy_in_system_instructions_and_data_in_runner_message \
  tests/test_llm_generator_openai.py::test_answer_output_has_only_answer \
  tests/test_api_chat.py::TestChatValidation \
  tests/test_api_chat.py::TestChatBehavior::test_chat_before_lifespan_returns_simple_503 \
  tests/test_api_chat.py::TestChatBehavior::test_real_chat_returns_only_answer_and_writes_backend_logs \
  -q --tb=short -s

# 4. Chạy thực thi temporary Notebook 05 & 06
uv run --env-file .env jupyter nbconvert --to notebook --execute \
  notebooks/05_retrieval_profiles.ipynb --output /tmp/05_retrieval_profiles-phase6-correction.ipynb
uv run --env-file .env jupyter nbconvert --to notebook --execute \
  notebooks/06_generation_and_api.ipynb --output /tmp/06_generation_and_api-phase6-correction.ipynb

# 5. Integrity check scoped
git diff --check backend/llm/ notebooks/
```

---

## 4. Kết quả quan sát

### 4.1. Tests & Runtime Verification

- **Targeted suite (17 tests)**: `17 passed, 7 warnings in 115.92s` (0:01:55).
- **Reviewer exact suite (10 tests)**: `10 passed, 3 warnings in 52.77s`.
- **Guarded test collection cleanup**: Tất cả các fixture tạo collection tạm thời đều tự dọn dẹp sạch (`LIVE CLEANUP hue_rag_live_test_e5_small_384: ok`).
- **Active collection**: `hue_foods_e5_small_384` luôn được bảo vệ và giữ nguyên 572 points.

### 4.2. API Response & Logging quan sát thực tế

Request thực tế tới `POST /api/chat`:
```json
{"query": "Bún bò Huế có đặc điểm gì nổi bật?"}
```

Response JSON quan sát được:
```json
{
  "answer": "Bún bò Huế nổi bật bởi nét mộc mạc dân gian nhưng vẫn tinh tế, gắn với văn hóa ẩm thực Huế. Món này có nguồn gốc từ Cố đô Huế và thường được nhận ra nhờ nước dùng đậm đà từ xương, sả và mắm ruốc; kết hợp với sợi bún và các thành phần như thịt bò, giò heo, huyết luộc, chả cua hoặc chả bò cùng rau ăn kèm. Khi nhắc “bún bò Huế” thường là để nhấn mạnh phong cách chế biến đặc trưng của món khi lan rộng ra ngoài Huế."
}
```
Keys trong response đúng duy nhất: `['answer']`.

Backend logs ghi nhận tuyến tính (không đưa vào response):
```text
[2026-08-26 08:36:22] INFO - chat - Received question: Bún bò Huế có đặc điểm gì nổi bật?
[2026-08-26 08:36:22] INFO - chat - Running retrieval
[2026-08-26 08:36:22] INFO - retrieval.service - retrieval profile=dense_only documents=10
[2026-08-26 08:36:22] INFO - chat - Retrieved 10 documents
[2026-08-26 08:36:22] INFO - llm - Generating answer with model: gpt-5.4-nano
[2026-08-26 08:36:25] INFO - llm - Generated answer successfully in 3749 ms; tokens=1063/140
[2026-08-26 08:36:25] INFO - chat - Chat request completed successfully
```

### 4.3. Notebook Execution & Audit

- **Notebook 05**: Chạy thành công toàn bộ 3 profiles trên bản sao `/tmp/05_retrieval_profiles-phase6-correction.ipynb`. Kết quả in: `dense_only` (2214 chars), `hybrid_no_rerank` (2228 chars), `hybrid_rerank` (2216 chars), typed errors reject empty query.
- **Notebook 06**: Chạy thành công qua `TestClient` với 1 real API call trên bản sao `/tmp/06_generation_and_api-phase6-correction.ipynb`. Dùng đúng 1 biến `question` từ cell trước, `/health` trả `status: ok`, `/api/chat` trả `status: 200` với đúng trường `['answer']` và sinh token `1063/153`. Không ép `HF_HUB_OFFLINE`.
- **Notebook 07**: Static audit sạch, không phụ thuộc vào contract cũ. Không chạy Run All Notebook 07 để bảo vệ file `backend/evaluation/retrieval_results.csv` của người dùng.
- Cả hai file `.ipynb` trong repo đều có `execution_count: null` và outputs rỗng `[]`.

### 4.4. Đánh giá 20 câu Phase 7 Answer Evaluation

Bộ đánh giá 20 câu `test2.jsonl` đã được thực thi và xác nhận ở vòng 1:
```text
{'questions': 20, 'successful': 20, 'failed': 0, 'accuracy': 4.25, 'completeness': 4.0, 'relevance': 4.3}
```
Không chạy lại 20 câu vì correction không thay đổi retrieval hay prompt logic.

---

## 5. Lỗi, giới hạn và kiểm tra toàn vẹn

1. **Over-Engineering Self-Review**:
   - *Exception handling*: Bắt `AgentsException` (bao gồm `ModelRefusalError`, `ModelBehaviorError`) và `OpenAIError`, chuyển về `GenerationError` nội bộ, map thành HTTP 503 rõ ràng. Không thêm exception class, retry, repair hay fake refusal test.
   - *Notebooks*: Giữ nguyên lý đơn giản, gọi đúng public backend API, không duplicate code, không ép offline flag khi không có yêu cầu.
2. **Kiểm tra tính toàn vẹn (Integrity Checks)**:
   - `git diff --check backend/llm/ notebooks/ reports/`: **PASS** (hoàn toàn sạch, không có trailing whitespace hay lỗi định dạng).
   - `git diff --check` trên toàn bộ worktree: **PARTIAL** (báo trailing whitespace trên các dòng CRLF của `backend/evaluation/retrieval_results.csv` và `backend/evaluation/answer_results.csv`). Đây là giới hạn đã biết: file `retrieval_results.csv` là user-owned, theo quy tắc an toàn không được sửa hay ghi đè.

---

## 6. Handoff cho Reviewer

- **Tài liệu đối chiếu**:
  - `reports/phase_6_generation_api_simplicity_codex_review.md`
  - `docs/superpowers/specs/2026-08-25-phase-6-generation-api-simplicity-design.md`
  - `docs/superpowers/plans/2026-08-25-phase-6-generation-api-simplicity-implementation.md`
  - Báo cáo này (`reports/phase_6_generation_api_simplicity_implementation_report.md`).
- **Lệnh Reviewer có thể chạy lại**:
  ```bash
  cd backend
  uv run --env-file ../.env python -m pytest \
    tests/test_context_builder.py \
    tests/test_llm_generator_openai.py::test_prompt_keeps_policy_in_system_instructions_and_data_in_runner_message \
    tests/test_llm_generator_openai.py::test_answer_output_has_only_answer \
    tests/test_api_chat.py::TestChatValidation \
    tests/test_api_chat.py::TestChatBehavior::test_chat_before_lifespan_returns_simple_503 \
    tests/test_api_chat.py::TestChatBehavior::test_real_chat_returns_only_answer_and_writes_backend_logs \
    -q --tb=short -s
  ```
- **Notebooks sẵn sàng**:
  - `notebooks/05_retrieval_profiles.ipynb` (outputs sạch).
  - `notebooks/06_generation_and_api.ipynb` (outputs sạch, dùng biến `question` từ cell trước, không forced offline).
- **Trạng thái**: Implementer không tự ý commit, push, sửa guide canonical, status hay review file. Toàn bộ code đã sẵn sàng để Reviewer thẩm định lại.
