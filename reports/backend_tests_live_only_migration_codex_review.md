# Codex Review: Backend Tests Live-Only Migration

Decision: accepted
Reviewer: Codex
Date: 2026-08-13
Review path:

```text
reports/backend_tests_live_only_migration_codex_review.md
```

Implementer report:

```text
reports/backend_tests_live_only_migration_implementation_report.md
```

## Tóm Tắt

Review ban đầu phát hiện fake escape hatches trong runtime và một lệnh không
phù hợp với secret policy trong implementation report. Correction re-review
đối chiếu lại source, tests, report, worktree và CodeGraph xác nhận cả ba
major findings đã được xử lý. Migration được technical accepted.

## Initial Findings (Resolved)

- resolved major: `backend/llm/generator_openai.py` từng nhận `runner` tại
  `OpenAIAnswerGenerator.__init__`. Khi truyền runner, `configured` trở thành
  true dù thiếu `OPENAI_API_KEY`, và `generate_answer` sẽ gọi runner đó thay vì
  `Agents SDK Runner.run`. Đây là fake-runner escape hatch trong runtime, không
  phải chỉ là pure logic test.
- resolved major: `backend/api/app.py` từng nhận `stack`, `context_builder` và
  `generator`; lifespan dùng trực tiếp các dependency truyền vào. Docstring còn
  nói rõ tests inject fake components. Đây là fake-stack/fake-generator escape
  hatch còn tồn tại trong production factory. Các live test hiện không cần các
  parameters này.
- resolved major: implementation report, mục `Commands Run`, từng ghi lệnh lấy
  `OPENAI_API_KEY` từ `.env`. Dù lệnh không in giá trị, nó vẫn đọc credential
  file, trái quy tắc không đọc hoặc expose secret/private config. Report phải
  bỏ lệnh này và chỉ nói key được provision sẵn trong process environment qua
  cơ chế ngoài repo.
- minor: reviewer không thể tái chạy paid subset/full suite trong process hiện
  tại vì kiểm tra presence-only cho thấy `OPENAI_API_KEY` không có trong
  environment. Không dùng `.env` hoặc workaround để vượt qua điều kiện này.

## Correction Re-Review

- `OpenAIAnswerGenerator` chỉ configured khi API key có thật trong environment
  và luôn gọi `Runner.run`; không còn parameter/branch runner injection.
- `create_app(settings=None)` không còn nhận component injection; lifespan luôn
  xây retrieval stack, context builder và generator thật.
- Implementation report chỉ mô tả key được provision sẵn ngoài repo; không còn
  lệnh hoặc hướng dẫn đọc `.env`.
- Compile của runtime và test source pass. Nhóm 17 pure prompt/telemetry/source
  contract tests pass; 4 test live/key-dependent được deselect có chủ đích.
- Còn một minor documentation issue: module docstring đầu
  `backend/llm/generator_openai.py` vẫn nói “with an injectable runner”, trái
  với source đã sửa. Đây không tạo runtime escape hatch và không chặn acceptance;
  sửa trong lần chỉnh documentation/runtime kế tiếp.

## Verification

```bash
git status --short
git diff --check
codegraph status .
codegraph explore "Trace FastAPI chat request from api.app.create_app through retrieval and OpenAI generation, including external dependencies."
codegraph impact backend/api/app.py
codegraph impact backend/ingestion/pipeline.py
rg -n -i 'fake|mock|monkeypatch|SimpleNamespace|replay|sample vector|make_payloads|offline|live-only' backend/tests backend -g '*.py'
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile backend/api/app.py backend/llm/generator_openai.py backend/tests/conftest.py backend/tests/test_api_chat.py backend/tests/test_llm_generator_openai.py
cd backend && HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/test_llm_generator_openai.py -q --tb=short -k 'PromptContract or UsageTokens or SourceMapping or PromptInjectionBoundary or not_configured'
```

Kết quả quan trọng:

- `git diff --check` sạch; CodeGraph index up to date.
- Test source dùng Qdrant/E5/MiniLM/API thật; `SimpleNamespace` chỉ nằm trong
  pure telemetry parser và environment monkeypatch chỉ dùng để tái tạo failure
  thật.
- Correction source không còn runner/component injection; compile pass và 17
  pure tests pass trong 1,91s.
- Implementation report ghi corrected full suite `205 passed`, 3 warnings,
  trong 177,21s; 5 `gpt-5.4-nano` calls không retry, cleanup marker collections
  thành công và active collection còn `572` points. Đây là evidence implementer
  cung cấp; reviewer không lặp lại paid run vì process thiếu key.

## Scope Check

Migration test, fixture collection marker, cleanup và xóa escape hatches runtime
nằm trong scope được duyệt. Không thấy fake runner/stack còn lại trong test path
hoặc runtime factory/generator.

## Safety And Quality Check

- Security: không thấy secret literal, raw provider payload hoặc system prompt
  bị lưu trong test source. Report correction không còn hướng dẫn đọc `.env`.
- Data safety: fixture dùng prefix `hue_rag_live_test_`, có assert marker và
  cleanup/final sweep. Active collection không có dấu hiệu bị mutate trong
  source đã review.
- Reliability: real failure paths dead URL, collection biến mất và HTTP 400 là
  hợp lệ. Generator và app factory không còn đường injection fake.
- Performance: fixture session scope giảm số lần ingest/model load; chưa thấy
  repeated load không cần thiết trong test source.
- Tests: implementer evidence là 205 passed; reviewer independently compile và
  chạy 17 pure contract tests. Independent paid re-run không thực hiện vì key
  không có trong environment reviewer.
- Notebooks: không thuộc migration scope; không thay đổi notebook canonical
  trong review này.
- Evaluation: không thuộc migration scope.

## Required Changes

Not applicable. Recommended minor follow-up: correct the stale module docstring
in `backend/llm/generator_openai.py` so it no longer says the runner is
injectable.
