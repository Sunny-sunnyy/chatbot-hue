# Codex Review: Phase 6 Generation API Simplicity

Decision: ready_for_user_confirmation
Reviewer: Codex
Date: 2026-08-26 08:54 +07
Canonical guide: `guides/phase_6_generation_api.md`
Implementation report: `reports/phase_6_generation_api_simplicity_implementation_report.md`

## 1. Phạm vi đã review

Reviewer đã review correction vòng 2 cho bốn finding của vòng 1: SDK refusal
boundary trong generator, biến câu hỏi và offline flag của Notebook 06, mô tả
context trong Notebook 05, cùng integrity check. Review đối chiếu guide,
simplicity design/plan, implementation report, source SDK đang cài, exact diff,
tests và hai notebook.

Reviewer chạy lại Qdrant, E5, MiniLM, `gpt-5.4-nano` và FastAPI thật. Notebook
chỉ được execute trên bản sao trong `/tmp`. Active collection chỉ được đọc.

## 2. Findings

Không còn blocker hoặc major. Bốn finding vòng 1 đã được xử lý đúng phạm vi:

- `AgentsException` bao phủ cả `ModelRefusalError` và `ModelBehaviorError` của
  SDK đang cài; generator chuyển chúng thành `GenerationError`, để route trả
  HTTP 503. Không thêm retry, wrapper, subtype hoặc fake refusal test.
- Notebook 06 chỉ khai báo `question` một lần và API cell dùng lại biến đó;
  không còn `HF_HUB_OFFLINE` hoặc wording offline.
- Notebook 05 chỉ mô tả `context character count`, khớp contract string.
- Source, tests, notebooks và reports trong scoped Phase 6 không còn lỗi
  `git diff --check`.

Không có minor mới cần chặn xác nhận.

## 3. Cách Reviewer chạy lại thật

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-phase6-review-uv-cache uv run --env-file ../.env \
  python -m pytest \
  tests/test_context_builder.py \
  tests/test_llm_generator_openai.py::test_prompt_keeps_policy_in_system_instructions_and_data_in_runner_message \
  tests/test_llm_generator_openai.py::test_answer_output_has_only_answer \
  tests/test_api_chat.py::TestChatValidation \
  tests/test_api_chat.py::TestChatBehavior::test_chat_before_lifespan_returns_simple_503 \
  tests/test_api_chat.py::TestChatBehavior::test_real_chat_returns_only_answer_and_writes_backend_logs \
  -q --tb=short -s

cd ..
UV_CACHE_DIR=/tmp/hue-rag-phase6-review-uv-cache uv run --env-file .env \
  jupyter nbconvert --execute --to notebook \
  notebooks/05_retrieval_profiles.ipynb \
  --output 05_retrieval_profiles-phase6-review-r2.ipynb --output-dir /tmp \
  --ExecutePreprocessor.timeout=900

UV_CACHE_DIR=/tmp/hue-rag-phase6-review-uv-cache uv run --env-file .env \
  jupyter nbconvert --execute --to notebook \
  notebooks/06_generation_and_api.ipynb \
  --output 06_generation_and_api-phase6-review-r2.ipynb --output-dir /tmp \
  --ExecutePreprocessor.timeout=900

git diff --check -- backend/llm backend/api backend/core backend/retrieval \
  backend/evaluation/eval.py backend/tests notebooks reports
```

Reviewer cũng compile sáu runtime modules, đọc exception hierarchy của Agents
SDK, kiểm tra notebook repo có outputs rỗng và execution counts null, xác nhận
semantic diff của `retrieval_results.csv` rỗng khi bỏ khác biệt line ending, và
đọc exact point count của active Qdrant collection.

## 4. Kết quả quan sát

- Exact focused suite: `10 passed, 3 warnings in 54.35s`.
- Real API dùng `gpt-5.4-nano`, retrieval trả 10 documents, response HTTP 200
  chỉ có field `answer`; log token quan sát là `1063/143`.
- Notebook 05 chạy đủ `dense_only`, `hybrid_no_rerank` và `hybrid_rerank` trên
  candidate 572 points; context lần lượt 2214, 2228 và 2216 characters.
- Notebook 06 dùng đúng câu hỏi ở cell trước, health `ok`, HTTP 200, response
  fields `['answer']`; real call ghi `1063/160` tokens.
- Hai notebook trong repo vẫn có `execution_count: null` và outputs rỗng.
- Python compile và scoped `git diff --check` đạt.
- Guarded test collection cleanup báo `ok`; active
  `hue_foods_e5_small_384` vẫn đúng 572 points.

## 5. Giới hạn hoặc phần chưa chạy

Reviewer không chạy broad backend suite hoặc batch answer 20 câu. Correction
chỉ đổi exception boundary và notebook lesson, không đổi retrieval, prompt hoặc
generation success path; chạy lại hai phạm vi đó không tạo thêm bằng chứng cần
thiết. Notebook 07 không Run All để tránh ghi đè dirty retrieval CSV.

Full-worktree `git diff --check` vẫn đỏ do CRLF trong hai CSV đã tồn tại trong
worktree. Scoped Phase 6 check đạt; `retrieval_results.csv` không có semantic
diff khi bỏ khác biệt line ending và không được Reviewer sửa.

Lần chạy notebook đầu tiên trong sandbox không khởi tạo được local kernel socket
(`Operation not permitted`). Hai kết quả notebook nêu trên là fresh runs ngoài
sandbox sau khi được cấp quyền.

## 6. Decision và bước tiếp theo

Decision là `ready_for_user_confirmation` sau correction vòng 2. Guide giữ
`under_review` cho đến khi user chạy Notebook 06 và xác nhận Phase 6 simplicity.

User report hiện hành nằm tại
`reports/user_reports/phase_6_generation_api_user_report.md`. Phase 8 vẫn đóng.
Reviewer chưa commit hoặc push.
