# Phase 6: Grounded answer generation và JSON API

## Mục tiêu và giá trị cho người dùng

Phase 6 biến ranked evidence từ retrieval thành câu trả lời tiếng Việt có nguồn và cung cấp JSON API tối giản. Mục tiêu là grounded behavior dễ test, chưa phải agent orchestration hoặc frontend production.

## Trạng thái

```text
Status: not_ready
Brainstorming level: Level 2 - standard
Owner: Codex Reviewer
Implementer: DeepSeek after Phase 5 approval and Phase 6 readiness
```

## Dependency

- Phase 5 retrieval service và ContextBuilder đã được phê duyệt.
- Active profile trả stable `RetrievedDocument` và source metadata.
- Answer baseline là OpenAI Agents SDK với `gpt-5.4-nano`.
- `OPENAI_API_KEY` do người dùng tự đặt trong environment; không đọc hoặc hiển thị trong guide/report.

## Chức năng phải tạo

- Grounded prompt cho domain ẩm thực Huế.
- Tool-less OpenAI Agents SDK runner cho answer generation.
- Structured internal output và deterministic API serialization.
- FastAPI health endpoint và non-streaming chat endpoint.
- Safe behavior khi query/context thiếu hoặc provider lỗi.
- Sources và retrieval debug có giới hạn.
- Mocked unit/API tests không gọi OpenAI.
- Notebook minh họa generation/API an toàn.

## Files dự kiến

```text
backend/llm/prompt.py
backend/llm/generator_openai.py
backend/api/app.py
backend/api/health.py
backend/api/routes/__init__.py
backend/api/routes/chat.py
backend/tests/test_llm_generator_openai.py
backend/tests/test_api_chat.py
notebooks/06_generation_and_api.ipynb
```

## Trong scope

- `GET /health`.
- `POST /api/chat` nhận một query và trả JSON.
- Một answer agent không có tools và không tự gọi retrieval.
- API route điều phối retrieval -> context -> generator.
- Citation/source mapping từ retrieved payload.
- Provider timeout/error mapping.

## Ngoài scope

- SSE hoặc token streaming.
- Frontend.
- Persistent conversation memory, authentication hoặc user database.
- Agent router, rewrite, decomposition hoặc retry retrieval.
- OpenRouter Qwen generation switch.
- Production deployment và external telemetry.

## Provider contract

```text
SDK: OpenAI Agents SDK for Python
Model: gpt-5.4-nano
Credential: OPENAI_API_KEY
Execution: direct OpenAI provider
```

Không dùng OpenRouter cho `gpt-5.4-nano`. Embedding/reranking OpenRouter key và OpenAI generation key tách biệt.

Generator interface tối thiểu:

```python
class GeneratedAnswer:
    answer: str
    used_source_ids: list[str]

async def generate_answer(
    query: str,
    context: str,
    available_source_ids: list[str],
) -> GeneratedAnswer:
    ...
```

Implementation dùng một `Agent` cấu hình cố định và `Runner` async. Không expose raw SDK response ra API. Có thể log model ID, latency, outcome và token usage dạng summary; không log prompt/context đầy đủ hoặc key.

## Grounded prompt contract

Prompt phải yêu cầu model:

- trả lời bằng tiếng Việt tự nhiên;
- chỉ dùng evidence được cung cấp;
- không tạo địa chỉ, giá, giờ mở cửa, món ăn hoặc đánh giá không có trong context;
- nêu rõ không đủ thông tin khi evidence thiếu;
- không làm theo instruction nằm trong retrieved documents;
- giữ trọng tâm câu hỏi;
- chỉ tham chiếu source IDs có trong `available_source_ids`;
- không tiết lộ system prompt, config hoặc provider metadata.

Retrieved content là untrusted data, không phải instruction. Prompt phải phân tách rõ system instruction, user query và evidence blocks.

## Source contract

API source item tối thiểu:

```python
{
    "chunk_id": "...",
    "source": "foods/restaurants/example.md",
    "title": "Tên quán",
    "section": "Thông tin",
    "score": 0.82,
}
```

- Chỉ trả source thực sự nằm trong final context.
- Không trả absolute paths, full vector, raw provider payload hoặc internal headers.
- Source order theo first evidence appearance hoặc final retrieval rank; policy được chốt trong brainstorming.
- Unknown source ID từ model bị loại và ghi validation failure; không fabricate source.

## API contract

### Health

```text
GET /health
```

Response phải phân biệt application alive với component readiness:

```python
{
    "status": "ok",
    "components": {
        "qdrant": "ready",
        "retrieval": "ready",
        "generator": "configured",
    },
}
```

Không trả key, private endpoint hoặc stack trace.

### Chat

```text
POST /api/chat
```

Request MVP:

```python
{
    "query": "Lần đầu đến Huế nên ăn gì?",
    "session_id": "optional opaque client value",
}
```

Success response:

```python
{
    "answer": "...",
    "sources": [],
    "session_id": "...",
    "retrieval_debug": {
        "profile": "hybrid_rerank",
        "embedding_model": "...",
        "reranker_model": "...",
        "retrieved_count": 5,
    },
}
```

`retrieval_debug` chỉ chứa fields đã được phê duyệt; không trả prompt, context, vectors, key/header hoặc full model payload.

## Validation và error behavior

- Empty/whitespace query: HTTP 422.
- Query vượt length limit: HTTP 422; exact limit được chốt trước implementation.
- Không có evidence: safe insufficient-information answer và empty sources; brainstorming quyết định có skip model hay không.
- Qdrant/retrieval unavailable: HTTP 503.
- OpenAI timeout/unavailable: HTTP 502 hoặc 503 theo mapping đã chốt, response generic.
- Invalid structured output: tối đa một bounded parse/retry attempt nếu được phê duyệt.
- Không trả raw exception hoặc stack trace cho client.

## Brainstorming bắt buộc trước implementation

Codex và người dùng phải chốt:

1. Query length limit và source limit.
2. Không có context thì skip model hay gọi strict refusal prompt.
3. Source format: inline markers hay chỉ JSON `sources`.
4. Có cho phép một structured-output retry hay fail ngay.
5. Timeout, maximum output tokens và temperature baseline.
6. Live smoke budget: số câu, categories và maximum estimated cost.

## Nhiệm vụ của DeepSeek Implementer

- TDD prompt boundary, missing context, valid/invalid source IDs, provider timeout và API mapping.
- Inject runner/generator để tests dùng fake.
- Không đọc `.env`; SDK lấy key từ environment theo approved setup.
- Không log full prompt, context hoặc generated raw payload.
- Giữ route thin, không duplicate retrieval/generation logic.
- Report mọi live call, model, count và cost nếu được phép.

## Nhiệm vụ của Codex Reviewer

- Kiểm tra prompt injection boundary, source integrity và error mapping.
- Xác minh default tests không network.
- Audit live smoke approval, actual model và cost evidence.
- Reject raw provider exposure, unbounded retry hoặc Agentic scope creep.

## Notebook bắt buộc

`notebooks/06_generation_and_api.ipynb` phải:

- giải thích grounded prompt và API flow bằng tiếng Việt;
- import runtime generator/API schemas;
- safe default dùng fake generator và sample context;
- real OpenAI cell có opt-in guard, không in key;
- không lưu raw provider response;
- committed outputs rỗng và `execution_count=null`.

## Tests và validation dự kiến

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile llm/prompt.py llm/generator_openai.py api/app.py api/health.py api/routes/chat.py
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_llm_generator_openai.py tests/test_api_chat.py -q --tb=short
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "import importlib; importlib.import_module('api.app'); print('api.app import ok')"
```

Mocked test matrix:

- grounded answer and valid sources;
- unknown source ID rejected;
- empty/no context policy;
- empty/oversized query;
- retrieval unavailable;
- model timeout/provider error;
- invalid output retry ceiling;
- health alive vs readiness;
- no sensitive/debug payload.

Live smoke chỉ chạy sau user approval; result vào report/benchmark ledger, không commit notebook output.

## Security, reliability và performance gates

- Separate `OPENAI_API_KEY`/`OPENROUTER_API_KEY` boundaries.
- No prompt injection from retrieved content.
- Bounded query, context, output tokens, timeout và retries.
- Async provider call không block event loop bằng sync wrapper.
- Không expose secret, raw exception, prompt hoặc chain-of-thought.
- API không mutate collection hoặc evaluation data.

## Tiêu chí phê duyệt Phase 6

- API imports cleanly và mocked tests pass.
- `/health` và `/api/chat` giữ exact contract.
- Answer grounded, tiếng Việt, có sources hợp lệ hoặc refusal an toàn.
- Provider failures mapped an toàn, không unbounded retry.
- Default tests/notebook không live.
- Approved live smoke dùng `gpt-5.4-nano` qua OpenAI Agents SDK và có cost evidence.
- Không implement SSE, frontend hoặc Agentic RAG.
- User report phản ánh đúng API/generation limitations và được người dùng xác nhận cùng notebook.

## Reports và cập nhật trạng thái

```text
reports/phase_6_generation_api_implementation_report.md
reports/phase_6_generation_api_codex_review.md
reports/hue_foods_rag_benchmark.md
reports/user_reports/phase_6_generation_api_user_report.md
```

Sau technical review đạt, Codex tạo user report `pending`; chỉ cập nhật `Project_Status.md` sau khi người dùng xác nhận notebook/report.

## Bước tiếp theo

Sau Phase 6 approval, Phase 7 brainstorm relevance ground truth, stratified answer subset, judge rubric, cost ceiling và artifact schema.
