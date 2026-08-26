# Prompt Handoff: Phase 6 Generation API Simplicity Implementer

Bạn là **Implementer** của Phase 6 simplicity scope trong dự án:

```text
/home/minhhieu/hue_rag
```

Nhiệm vụ của bạn là triển khai đúng spec và plan đã được người dùng phê duyệt.
Bạn không phải Reviewer và không được tự mở rộng thiết kế.

## 1. Quy trình bắt buộc

Luôn bắt đầu bằng `using-superpowers`.

Sau đó:

1. đọc đầy đủ các file bắt buộc bên dưới;
2. dùng `executing-plans` làm quy trình thực thi chính;
3. dùng `test-driven-development` cho từng thay đổi hành vi;
4. dùng `systematic-debugging` nếu có failure ngoài dự kiến;
5. dùng `verification-before-completion` trước handoff;
6. áp dụng `skills/karpathy-guidelines/SKILL.md` trong toàn bộ code/test review.

Không dispatch subagent hoặc tạo worktree nếu người dùng chưa yêu cầu riêng.

## 2. Đọc trước khi sửa

Đọc toàn bộ, không đọc lướt:

```text
/home/minhhieu/hue_rag/session_prompt/Session_Prompt.md
/home/minhhieu/hue_rag/session_prompt/Project_Status.md
/home/minhhieu/hue_rag/session_prompt/IMPLEMENTER_WORKFLOW.md
/home/minhhieu/hue_rag/guides/README.md
/home/minhhieu/hue_rag/guides/phase_0_mvp_foundation.md
/home/minhhieu/hue_rag/guides/phase_6_generation_api.md
/home/minhhieu/hue_rag/docs/superpowers/specs/2026-08-25-phase-6-generation-api-simplicity-design.md
/home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-25-phase-6-generation-api-simplicity-implementation.md
/home/minhhieu/hue_rag/session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md
/home/minhhieu/hue_rag/skills/karpathy-guidelines/SKILL.md
```

Đọc source hiện tại và direct consumers trước khi edit:

```text
backend/retrieval/context_builder.py
backend/llm/prompt.py
backend/llm/generator_openai.py
backend/core/schema.py
backend/api/routes/chat.py
backend/api/app.py
backend/api/health.py
backend/evaluation/eval.py
backend/tests/test_context_builder.py
backend/tests/test_llm_generator_openai.py
backend/tests/test_api_chat.py
backend/tests/test_evaluation.py
notebooks/05_retrieval_profiles.ipynb
notebooks/06_generation_and_api.ipynb
notebooks/07_evaluation.ipynb
```

Đọc các reference code sau để học cách viết tuyến tính và logger dễ đọc; không
copy architecture/session/rate-limit/streaming của chúng:

```text
/home/minhhieu/llm_rag/backend/api/app.py
/home/minhhieu/llm_rag/backend/api/health.py
/home/minhhieu/llm_rag/backend/api/routes/chat.py
/home/minhhieu/llm_rag/backend/api/routes/chat_openai.py
/home/minhhieu/llm_rag/backend/llm/generator_openai.py
```

## 3. Authority và source of truth

Canonical guide đang ở trạng thái `ready`. Spec và plan đã được user xác nhận:

```text
docs/superpowers/specs/2026-08-25-phase-6-generation-api-simplicity-design.md
docs/superpowers/plans/2026-08-25-phase-6-generation-api-simplicity-implementation.md
```

Thực hiện plan **Task 1 đến Task 5 theo thứ tự**, dừng ở mỗi Reviewer checkpoint
để tự review exact diff trước khi tiếp tục.

Nếu source hiện tại khác plan vì thay đổi mới của người dùng:

- giữ nguyên thay đổi không liên quan;
- áp dụng intent/interface đã khóa bằng thay đổi nhỏ nhất;
- nếu khác biệt làm thay đổi scope, interface, provider, model hoặc acceptance,
  dừng và báo user/Reviewer thay vì tự quyết.

Không sửa canonical guide, approved spec/plan, Reviewer report, user report,
`Project_Status.md` hoặc workflow files.

## 4. Kết quả phải đạt

Luồng cuối:

```text
query
-> retrieval
-> ContextBuilder.build(documents) -> labeled str
-> no context: skip model, exact fallback
-> OpenAIAnswerGenerator.generate_answer(query, context) -> str
-> {"answer": "..."}
```

Contract đã khóa:

```text
Model: gpt-5.4-nano
OpenAI Agents SDK: Agent/Runner, direct OpenAI Responses path
Temperature: 0.2
Maximum output tokens: 1024
Timeout: 45 seconds
Agent tools/handoffs: none
Structured output: AnswerOutput(answer: str)
```

Exact fallback:

```text
Mình không tìm thấy thông tin phù hợp trong dữ liệu hiện tại.
```

Success response chỉ có:

```json
{"answer": "..."}
```

Public errors:

```text
422 -> Yêu cầu không hợp lệ.
503 -> Hệ thống tạm thời không khả dụng. Vui lòng thử lại sau.
500 -> Đã xảy ra lỗi trong hệ thống. Vui lòng thử lại sau.
```

Error body:

```json
{"detail": "..."}
```

Không public component error code.

## 5. Logging đã khóa

Logging chỉ ở backend console và `backend/logs/application.log`; không trả log
trong response.

Viết log tuyến tính, dễ đọc theo phong cách:

```python
logger.info(f"Received question: {query}")
logger.info("Running retrieval")
logger.info(f"Retrieved {len(documents)} documents")
logger.info(f"Generating answer with model: {model}")
logger.info(f"Generated answer successfully in {latency_ms} ms")
logger.warning("No relevant context found")
logger.error(f"Answer generation failed: {error}")
```

Được log nguyên văn user query theo quyết định của user. Không log full prompt,
full retrieved context, generated answer, vector, API key hoặc raw provider
response. Known failure dùng `logger.error`; unexpected failure mới dùng
`logger.exception`. Không để exception/stack trace đi vào API.

Không thêm request ID, session ID, JSON logger, rotation policy, telemetry
service hoặc dependency logging mới.

## 6. Những thứ phải xóa khỏi Phase 6 contract

```text
ContextResult
parallel sources
JSON evidence object
available_source_ids
used_source_ids
GeneratedAnswer
session_id
retrieval_debug
source projection helpers
app.state.runtime
_runtime_info
GeneratorNotConfiguredError
GeneratorTimeoutError
GeneratorUnavailableError
InvalidGeneratorOutputError
public 502/504 branches và component subcodes
```

Thay bốn generation exception bằng đúng một internal `GenerationError`.

Không giữ compatibility wrapper, alias hoặc dead field để test cũ pass.

## 7. Không được thêm

- streaming/SSE;
- rate limiting;
- CORS wildcard;
- retry, repair hoặc provider fallback;
- OpenRouter generator adapter;
- tools, agent loop, handoff hoặc router;
- conversation/session memory hoặc query rewrite;
- public sources/path/score/debug;
- request ID hoặc external observability;
- mock/fake/replay/dead endpoint tests;
- abstraction, validator hoặc config phòng xa;
- test count/coverage target;
- 104-question evaluation mặc định.

## 8. Worktree và data safety

Chạy đầu tiên:

```bash
git status --short
```

Worktree đã có nhiều thay đổi không thuộc task. Mọi thay đổi đó thuộc người dùng.
Đặc biệt:

```text
backend/evaluation/retrieval_results.csv
```

đang modified và không được ghi đè hoặc restore. Vì vậy:

- không Run All Notebook 07 trong worktree này;
- không chạy
  `test_retrieval_handler_returns_named_columns_and_rows` vì test đó ghi đè
  retrieval CSV;
- chạy exact exclusion command trong Task 5;
- chạy 20-question **answer** batch trực tiếp; việc refresh
  `backend/evaluation/answer_results.csv` nằm trong scope;
- Notebook 07 chỉ static-audit; ghi rõ intentional skip trong report.

Active collection `hue_foods_e5_small_384` luôn read-only. Chỉ existing guarded
test collections có prefix `hue_rag_live_test_` được mutation/cleanup theo
fixture hiện hành.

Không dùng `git reset`, `git checkout --`, broad delete, stage, commit hoặc push.
Dùng `apply_patch` để sửa file. Không mở hoặc in secret values; dùng
`uv --env-file` như plan.

## 9. Test và verification

Không dùng mock/fake. Không dựng outage bằng dead URL, unset key hoặc xóa
collection giữa request.

Giữ test cho:

- labeled context/order/budget/empty;
- prompt policy và one-field output;
- one real generator call;
- 422/503 simple public contract;
- zero-model no-context fallback;
- one real answer-only API call và backend logs;
- retained Phase 6.1 warm-up behavior;
- one real Phase 7 generation+judge consumer;
- affected 20-question answer evaluation.

Xóa test chỉ bảo vệ source/session/debug/source-ID/public subcode và simulated
outages.

Chạy exact commands và expected checkpoints trong plan. Expected result trong
plan không phải observed evidence. Nếu command fail, ghi failed/partial đúng sự
thật và debug root cause; không tạo fallback để biến đỏ thành xanh.

## 10. Notebook

- Notebook 05: hiển thị labeled context string, không `.sources`/`.context`.
- Notebook 06: một real API call, chỉ in health/status/response fields/answer;
  không source/session/debug.
- Notebook 07: không sửa lesson nếu không có stale contract; không Run All vì
  retrieval CSV đang dirty. Direct 20-answer batch thay cho affected live check.
- Notebook được sửa phải committed-state sạch outputs và execution counts.
- Run All 05/06 trên temporary output dưới `/tmp`, không copy output về repo.

## 11. Over-engineering self-review bắt buộc

Trước report, đọc exact diff và trả lời:

1. Mỗi helper/class/test còn lại phục vụ hành vi thật nào?
2. Có thể theo data flow từ route tới answer mà không nhảy qua layer không cần
   thiết không?
3. Có code/test nào chỉ bảo vệ contract vừa xóa không?
4. Có feature từ `llm_rag` bị copy nhưng Hue RAG không cần không?
5. Có retry, fallback, compatibility code hoặc flexibility phòng xa không?

Nếu có, xóa phần do scope này tạo ra hoặc làm orphan. Không refactor dead code
không liên quan.

## 12. Báo cáo và handoff

Tạo đúng file:

```text
reports/phase_6_generation_api_simplicity_implementation_report.md
```

Dùng `session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md`. Báo cáo phải chứa exact
commands và observed results:

- changed files và data flow mới;
- test counts thật;
- model/provider thật;
- API body chỉ có answer;
- log backend quan sát được nhưng không có trong response;
- Notebook 05/06 temporary Run All outcome;
- direct 20-answer evaluation summary;
- Notebook 07 intentional skip và lý do bảo vệ dirty retrieval CSV;
- failed/skipped/partial checks;
- guarded Qdrant cleanup outcome;
- giới hạn còn lại.

Cuối cùng chạy:

```bash
git diff --check
git status --short
git diff --name-only
```

Không commit/push. Không tự approve. Bàn giao implementation report và exact
changed-file list cho Codex Reviewer.
