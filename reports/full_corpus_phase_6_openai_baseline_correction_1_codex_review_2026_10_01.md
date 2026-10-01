# Codex Review: Phase 6 OpenAI baseline — correction 1

Decision: changes_requested
Reviewer: Codex
Date: 2026-10-01 (+07)
Prior review: `reports/full_corpus_phase_6_openai_baseline_codex_review_2026_10_01.md`
Implementation report: `reports/full_corpus_phase_6_openai_baseline_implementation_2026_10_01.md`

## 1. Phạm vi và evidence đã kiểm

Reviewer đã đọc correction handoff, prior review, revised implementation plan,
Review Contract và implementation report; inspect toàn bộ correction paths và
chạy lại non-paid gate. Không chạy `phase6_live_smoke`, không gọi OpenAI, không
mutate Qdrant/corpus và không commit/push.

Fresh observations:

- focused suite: `127 passed, 1 warning in 34.31s`;
- Metadata v2 complete verify: `VERIFIED` cho 33.840 points;
- exact uvicorn command từ `backend/`: khởi động thành công; `/health` trả HTTP
  200 và cả 5 components `ready`;
- `git diff --check`: exit 0;
- vendor SHA-256 khớp hai pin đã duyệt;
- notebook: 8 cells, 3 code cells, 0 outputs, mọi `execution_count` là `null`;
- installed `httpx` là 0.28.1; `ASGITransport` không có lifespan option.

## 2. Findings

### P6-C1-R1 — blocker — replacement runner không chạy FastAPI lifespan

- Vị trí: `backend/llm/phase6_live_smoke.py:149-163`.
- Evidence: runner tạo `create_app(settings)`, sau đó dùng
  `ASGITransport(app=app)` và gọi `/health`. Với `httpx 0.28.1`, transport này
  không quản lý ASGI lifespan. Vì vậy các dependency chỉ được dựng trong
  `app` lifespan không chạy; state giữ `retrieval_ready/tokenizer_ready/
  generator_ready = False`, `/health` là `degraded`, và runner return trước
  attempt 1.
- Tác động: sequence thay thế không thể bắt đầu đúng protocol dù production
  uvicorn đã hoạt động.
- Tiêu chí đóng: quản lý lifespan thực sự trên cùng async lifecycle/event loop,
  thêm non-paid regression chứng minh `/health` `ok` và state dependencies có
  mặt trước attempt 1. Test không được gọi provider.

### P6-C1-R2 — major — acceptance suite mới dùng mock/fake trái hard boundary

- Vị trí: `backend/tests/test_api_chat.py:86-126`,
  `backend/tests/test_openai_full_corpus_generator.py:93-158`.
- Evidence: tests dùng `AsyncMock`, `MagicMock`, fake API key,
  `FakeRunResult`, fabricated `GeneratedText` và monkeypatch `Runner.run`.
  Revised plan cấm mock/fake/stub/replay provider response làm acceptance
  evidence; pure tests chỉ được kiểm deterministic configuration/schema/
  packing logic mà không gọi mạng.
- Tác động: con số 127 pass không phải acceptance evidence hợp lệ cho các
  claims private trace và strict provider boundary.
- Tiêu chí đóng: bỏ các mocked/fabricated acceptance tests; tách parser/helper
  thuần để kiểm malformed JSON/dict/blank/extra field trực tiếp, và dùng
  dependency thật hoặc deterministic boundary được contract cho phép ở các
  test route. Báo lại số test hợp lệ, không chỉ đổi nhãn mock.

### P6-C1-R3 — major — P6-R1/P6-R4 chưa đóng trọn contract

- Vị trí: `backend/api/app.py:7-11,33,37-42,126-132`.
- Evidence: exact uvicorn startup đã được sửa, nhưng `create_app()` vẫn gọi
  `load_settings(...)` trước lifespan khi không truyền settings, trái yêu cầu
  factory import-safe/resolve private runtime trong lifespan. Module còn mutate
  `sys.path` ở import time và khai báo `REPO_ROOT` hai lần. Hai cleanup branches
  vẫn log raw `str(exc)`, trái safe-log acceptance của P6-R4.
- Tác động: import/construction vẫn có side effect ngoài lifecycle và raw
  exception có thể đưa private/provider detail vào log.
- Tiêu chí đóng: defer default settings/runtime resolution vào lifespan, giữ
  exact production command hoạt động bằng packaging/import solution tối thiểu,
  xóa duplicate/path workaround không cần thiết, và log cleanup bằng safe
  category không chứa exception payload.

### P6-C1-R4 — major — evidence capture/protocol runner chưa fail-closed

- Vị trí: `backend/llm/phase6_live_smoke.py:39-64,201-204,223-243,276-279,
  283-336`; `backend/api/routes/chat.py:48-154`.
- Evidence:
  - case validator không reject extra top-level keys hoặc extra/missing item
    fields, nên chưa bảo vệ exact schema `{schema_version,cases}` và exact
    `{case_id,question}`;
  - `last_chat_trace` là mutable global app state chứa query và packed private
    context; nó không được clear ở đầu request và chỉ update ở no-evidence hoặc
    success path. Một generation/citation failure có thể khiến runner gắn trace
    của request trước vào attempt hiện tại;
  - runner dùng `logger.exception`, nên traceback/raw exception có thể lọt log;
  - artifact chỉ được ghi sau toàn bộ flow; health failure hoặc exception sớm
    return/raise mà không tạo artifact ghi trạng thái incomplete/attempt count.
- Tác động: provenance có thể sai request, dữ liệu private tồn tại trong shared
  production state, guard paid input chưa exact và evidence có thể mất đúng ở
  failure path cần audit nhất.
- Tiêu chí đóng: exact-schema fail closed; capture per-call evidence theo scope
  runner/request mà không giữ query/context trong shared production state; xóa
  stale state trước mọi request nếu cơ chế tạm còn tồn tại; dùng safe logging;
  atomically persist FAIL/incomplete artifact cho mọi exit sau khi paid run đã
  được xác nhận, với attempted-call count trung thực.

## 3. Đánh giá P6-R1..P6-R5

| Finding cũ | Kết luận correction 1 |
|---|---|
| P6-R1 | Đóng một phần: production uvicorn đã PASS; lifecycle/settings contract còn major gap |
| P6-R2 | Đóng một phần: real retrieval, single loop intent và dynamic count đã sửa; runner bị blocker lifespan và schema chưa exact |
| P6-R3 | Chưa đóng: metadata fields đã được nối, nhưng trace có thể stale và private shared state không an toàn |
| P6-R4 | Đóng một phần: generator fail-closed tốt hơn; acceptance tests không hợp lệ và cleanup log còn raw payload |
| P6-R5 | Đã đóng: formatting/inventory/fresh observations hiện nhất quán trong phạm vi kiểm |

## 4. Frontend/Next.js

Static frontend không phải deviation của Implementer. Canonical guide hiện ghi
rõ UI Phase 6 là static HTML/CSS/JavaScript và Next.js được dành cho frontend
phase sau. Vì vậy Reviewer không mở finding về việc chưa dùng Next.js. Nếu User
muốn Next.js ngay trong Phase 6, đó là scope/design amendment mới và phải được
chốt trước khi tiếp tục paid acceptance.

## 5. Decision và bước tiếp theo

Verdict: **CHANGES REQUESTED**.

Không cấp quyền cho replacement five-call sequence. Implementer cần correction
non-paid thứ hai cho P6-C1-R1..R4; giữ Qdrant/corpus read-only, không paid call,
không Git write và không sub-agent. Sau independent review đạt, Reviewer mới
trình User xin authority riêng cho đúng một replacement five-call sequence.
