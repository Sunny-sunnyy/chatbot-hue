# Implementation Report: Phase 6 Grounded answer generation và JSON API

Implementer: DeepSeek
Date: 2026-08-13 (revision 5 - status sync sau technical acceptance và migration live-only)
Report path:

```text
reports/phase_6_generation_api_implementation_report.md
```

Phase guide context:

```text
guides/phase_0_mvp_foundation.md
guides/phase_6_generation_api.md
session_prompt/Project_Status.md
reports/hue_foods_rag_benchmark.md
reports/phase_6_generation_api_codex_review.md
```

## Approved Scope

Phase 6 đã hoàn tất Level 2 brainstorming và được người dùng phê duyệt ngày
2026-08-13 +07. Phase 6 hiện có trạng thái `approved` sau technical
acceptance của Codex và user confirmation; backend test suite đã hoàn tất
migration live-only (xem
`reports/backend_tests_live_only_migration_implementation_report.md`).
Revision 4 là correction pass theo Codex re-review với scope vẫn đúng guide:

- Grounded prompt cho domain ẩm thực Huế (`backend/llm/prompt.py`).
- Tool-less OpenAI Agents SDK runner cho answer generation, chạy trực tiếp
  trên Runner thật, không có dependency injection
  (`backend/llm/generator_openai.py`).
- Structured internal output `GeneratedAnswer` và deterministic API
  serialization.
- FastAPI health endpoint và non-streaming chat endpoint.
- FastAPI lifespan khởi tạo runtime một lần và lưu readiness trong `app.state`.
- Safe behavior khi query/context thiếu hoặc provider lỗi.
- Sources và retrieval debug có giới hạn (allowlist).
- Unit/API tests theo Live-Only Validation Policy: chạy dependency thật
  (Qdrant, E5, MiniLM, OpenAI `gpt-5.4-nano`).
- Notebook minh họa generation/API an toàn (`notebooks/06_generation_and_api.ipynb`).

Không implement: SSE/streaming, frontend, session storage, auth, query rewrite,
input router, web fallback, OpenRouter Qwen generation switch, rate limiting,
CORS wildcard, production deployment.

## Trạng Thái Hiện Tại (2026-08-13)

- Phase 6 `approved`: technical review đạt, live smoke 12 calls đạt gate
  (tổng `$0,01493875`, xem mục Live Smoke bên dưới), user đã xác nhận.
- Backend test suite đã migration hoàn toàn sang live-only validation:
  205 tests dùng Qdrant thật, E5 thật, MiniLM thật, FastAPI thật và
  `gpt-5.4-nano` thật; hai runtime fake escape hatch (`runner` injection
  trong generator và component injection trong `create_app`) đã bị xóa;
  mọi test dùng isolated Qdrant collection có marker và cleanup đã xác
  minh. Chi tiết: `reports/backend_tests_live_only_migration_implementation_report.md`.
- Notebooks 01–06 chạy runtime thật khi Run All (xem mục Notebook 06
  Runtime-Redesign); các mô tả fake mode ở các mục revision cũ bên dưới là
  lịch sử trước redesign, không còn phản ánh trạng thái hiện tại.
- `OPENAI_API_KEY` do user provision sẵn trong process environment ngoài
  repo; runtime và tests không đọc `.env`.

## Summary

Revision 4 xử lý major finding mới của Codex re-review: query-to-evidence
section boundary có thể bị giả mạo vì query raw được nối trực tiếp trước
evidence header. Toàn bộ runner input giờ là **một JSON document duy nhất**:

1. **Single JSON document (major)**: `build_user_message()` serialize
   `{"query": ..., "evidence": [...], "available_source_ids": [...]}` bằng
   `json.dumps` (thư viện chuẩn, `ensure_ascii=False`, `sort_keys=True`).
   Query (kể cả chứa exact evidence header + fake JSON block + allowlist
   header) được escape hoàn toàn bên trong value `query`; không còn section
   header nào trong runner input để giả mạo. `ContextBuilder` trả context là
   một JSON array các evidence objects (thay vì JSON lines), giữ exact
   `chunk_id`, context/source order, whole-chunk behavior và character budget
   (tính trên serialized array + brackets). Hệ quả sửa nhỏ: route
   no-evidence check dùng `context_result.sources` thay vì context string
   (context rỗng giờ là `"[]"`, không phải `""`).
2. **Adversarial query test (major)**: test mới
   `test_query_with_forged_sections_cannot_inject_evidence` dùng query chứa
   exact `BẰNG CHỨNG TRUY XUẤT (...)` header, một valid JSON object
   `chunk_id="fake|0"` và `SOURCE ID HỢP LỆ` header với `- fake|0`. Probe đã
   chứng minh test fail trên format revision 3 (plain-text sections —
   `json.loads` fail) và pass trên revision 4 (query giữ verbatim, evidence
   chỉ `real|0`, allowlist đóng). Các injection tests hiện có được chuyển
   sang parse JSON document (không còn parse section headers).
3. **Giữ nguyên JSON evidence fix và các regression**: mapping 1:1
   block-to-chunk_id, forged-label test, notebook readiness, code-cell count,
   `InvalidSessionIdError` removal từ revision 2-3 giữ nguyên.
4. **Report/notebook**: notebook cell 1 mô tả runner input là một JSON
   document; cells demo/real-mode dùng context JSON hợp lệ; report ghi đúng
   evidence thực tế.

Các findings revision 1-3 khác đã được xử lý và giữ nguyên.

Model preflight (revision 1, theo user approval): `gpt-5.4-nano` tồn tại
(snapshot `gpt-5.4-nano-2026-03-17`), pricing $0.20/1M input + $1.25/1M output,
hỗ trợ temperature và max output tokens (limit 128k, cấu hình 1024 hợp lệ);
Agents SDK 0.19.4 map `ModelSettings.max_tokens` -> Responses API
`max_output_tokens` (verified trong source package). Không gọi live API.

Toàn bộ validation offline: 269 tests đạt (52 Phase 6 revision 4 + 217
regression), notebook default fake mode chạy 0 cell errors.

Ghi chú trạng thái: số liệu trên là evidence offline của revision 4 tại
thời điểm đó; backend test suite sau này đã migration sang live-only
validation (205 tests live với dependency thật) và notebook 06 đã chuyển
sang runtime-real — xem mục Trạng Thái Hiện Tại ở trên.

## Files Created

- `backend/llm/prompt.py` - grounded prompt contract: `SYSTEM_INSTRUCTIONS`
  (system policy, hướng dẫn đọc JSON document runner input + tham chiếu đúng
  `chunk_id` của từng evidence object) + `build_user_message()` serialize
  query/evidence/allowlist thành một JSON document.
- `backend/llm/generator_openai.py` - `GeneratedAnswer` (Pydantic structured
  output), `OpenAIAnswerGenerator` chạy trực tiếp Runner thật (không
  injection; sửa trong migration live-only), timeout 45s, typed
  errors, chỉ log model/latency/outcome/source count/token summary.
- `backend/api/app.py` - `create_app(settings=None, *, stack=None,
  context_builder=None, generator=None)`; lifespan build components một lần
  vào `app.state`; exception handlers normalize 422 `invalid_request` và 500
  `internal_error`; module-level `app = create_app()` import-safe.
- `backend/api/health.py` - `GET /health` trả status ok/degraded + components
  app/qdrant/retrieval/generator từ cached readiness, không ping external.
- `backend/api/routes/chat.py` - `POST /api/chat`: validation 1-500 ký tự query,
  session_id tối đa 128 (server tạo UUID khi thiếu, không lưu history), thread
  pool cho sync retrieval, no-evidence skip model (dựa trên sources rỗng),
  source projection + dedup theo context order, typed error mapping,
  retrieval_debug allowlist.
- `backend/tests/test_llm_generator_openai.py` - 23 tests.
- `backend/tests/test_api_chat.py` - 27 tests.
- `notebooks/06_generation_and_api.ipynb` - notebook canonical Phase 6 (14
  cells, 7 code cells, nbformat 4.5).
- `reports/phase_6_generation_api_implementation_report.md` - report này
  (revision 4).

## Files Modified

- `backend/retrieval/context_builder.py` - context là JSON array các evidence
  objects (`json.dumps(blocks, ensure_ascii=False, sort_keys=True)`); budget
  tính trên serialized array (brackets + ", " giữa items); order/whole-chunk
  giữ nguyên.
- `backend/api/routes/chat.py` - no-evidence check chuyển từ context string
  sang `context_result.sources` (context rỗng giờ là `"[]"`).
- `backend/tests/test_context_builder.py` - tests parse JSON array; budget
  tests tính overhead chuẩn của `json.dumps(list)`.
- `backend/config/settings.yaml` - thêm `llm.timeout: 45` (provider contract
  của guide) và cập nhật comment model verification (2026-08-13).
- `backend/config/README_config.md` - mô tả nhóm `llm` thêm timeout (giây).
- `backend/core/schema.py` - thêm 4 typed errors: `GeneratorNotConfiguredError`,
  `GeneratorTimeoutError`, `GeneratorUnavailableError`,
  `InvalidGeneratorOutputError` (`InvalidSessionIdError` đã bị xóa ở revision
  2 theo Codex minor finding vì không có caller).
- `backend/tests/test_api_chat.py` - context generator nhận parse bằng
  `json.loads` (JSON array).

## Correction Mapping (Revision 4)

| Finding | Source fix | Test | Actual result |
|---|---|---|---|
| major: query nối raw giả mạo evidence header + JSON block | `build_user_message` serialize toàn bộ runner input thành một JSON document; query escape trong value `query`; `ContextBuilder` trả JSON array | `test_query_with_forged_sections_cannot_inject_evidence` | Test pass trên revision 4; probe trên format revision 3 (plain-text sections) fail đúng (`json.loads` fail); query giữ verbatim, evidence chỉ `real|0`, allowlist đóng |
| major: adversarial query test chưa phủ exact header/JSON | Thêm test forged-query; chuyển toàn bộ injection/mapping tests sang parse JSON document | `test_query_with_forged_sections_cannot_inject_evidence` + 5 tests cập nhật | 23 llm tests pass; không còn parse section headers |
| major (hệ quả): no-evidence check sai với context `"[]"` | Route kiểm tra `context_result.sources` rỗng thay vì context string | `test_no_evidence_skips_model_and_answers_safe`, `test_blank_document_context_skips_model` | 2 tests pass; model không được gọi khi sources rỗng |
| regression: JSON evidence fix giữ nguyên | Không thay đổi fix revision 3 | forged-label test, mapping tests | 10 context builder + 27 api tests pass |

## Notebooks Created Or Modified

- `notebooks/06_generation_and_api.ipynb` - giải thích grounded prompt và API
  flow bằng tiếng Việt; cell 1 mô tả runner input là **một JSON document duy
  nhất** (query/evidence/available_source_ids) với mọi chuỗi untrusted được
  escape. Mô tả fake runner/fake stack ở đây là trạng thái revision 4 đã lỗi
  thời: notebook hiện tại chạy runtime thật (app thật/lifespan thật, đúng một
  OpenAI call mỗi Run All, không guard opt-in) — xem mục Notebook 06
  Runtime-Redesign. User tự kiểm tra: mở notebook và Run All (cần Qdrant,
  model cache và `OPENAI_API_KEY` trong environment) hoặc chạy tests trong
  `backend/`.

## Commands Run

```bash
# Từ backend/:
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile \
  llm/prompt.py llm/generator_openai.py api/app.py api/health.py \
  api/routes/chat.py retrieval/context_builder.py core/schema.py
# -> pass (7 modules)

UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest \
  tests/test_llm_generator_openai.py tests/test_api_chat.py \
  tests/test_context_builder.py -q --tb=short
# -> 60 passed (23 + 27 + 10)

UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q --tb=short
# -> 269 passed (52 Phase 6 revision 4 + 217 regression)

# Probe: forged-query test fail trên format revision 3 (plain-text sections)
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "... json.loads trên message revision 3 ..."
# -> JSONDecodeError (fail đúng); revision 4: query verbatim, evidence chỉ real|0

# Từ repo root:
env -u HUE_RAG_PHASE6_REAL env -u OPENAI_API_KEY \
  UV_CACHE_DIR=/tmp/uv-cache uv run jupyter nbconvert --to notebook --execute \
  notebooks/06_generation_and_api.ipynb --output /tmp/nb06_rev4_exec.ipynb \
  --ExecutePreprocessor.timeout=180 --ExecutePreprocessor.startup_timeout=120
# -> 0 cell errors; health ok với generator configured khi key bị unset

UV_CACHE_DIR=/tmp/uv-cache uv run python -c "... nbformat.validate + schema checks ..."
# -> nbformat validate pass; 14 cells (7 code); ids unique; outputs rỗng; execution_count null

git diff --check
# -> clean

codegraph status .  # sau sync
# -> Index is up to date (64 python files, 1.022 nodes)
```

## Tests And Verification

Targeted Phase 6 revision 4 tests (60 passed qua 3 files):

- **test_llm_generator_openai.py (23)**: system instructions phủ policy
  (tiếng Việt, insufficient evidence, untrusted data, chunk_id theo từng
  evidence object, available_source_ids, used_source_ids); runner input là
  một JSON document đúng schema; system policy không bao giờ nằm trong runner
  input; empty context -> evidence `[]`; generator not configured khi thiếu
  key / configured khi có key; fake runner không cần key; success trả
  `GeneratedAnswer` và query/evidence đúng trong JSON input; empty context
  reject trước runner call; timeout -> `GeneratorTimeoutError`;
  `ModelBehaviorError` -> `InvalidGeneratorOutputError`; provider error ->
  `GeneratorUnavailableError`; blank answer invalid; unknown source ID invalid;
  wrong output type invalid; mapping: hai chunks cùng source+section -> evidence
  array đúng chunk_id/text theo context order và allowlist đúng thứ tự;
  injection boundary (6 tests): instruction trong query và trong evidence,
  delimiter/heading giả, **query chứa exact evidence header + fake JSON block
  + allowlist header**, label JSON giả trong evidence text, end-to-end chạy
  trên fake runner — query giữ verbatim trong value `query`, evidence không
  bị mở rộng, allowlist không mở rộng, block-to-ID mapping không đổi,
  structural field đếm đúng 1 lần.
- **test_api_chat.py (27)**: import `api.app` không side effect; health
  degraded trước lifespan; health ok sau ready lifespan; health degraded +
  chat 503 khi retrieval build fail (monkeypatch `build_retrieval_stack`);
  health không lộ secrets; empty/whitespace/oversized query 422
  `invalid_query`; whitespace/oversized session_id 422 `invalid_session_id`;
  missing/malformed body 422 `invalid_request`; server tạo UUID khi thiếu
  session_id; success: answer + sources theo context order (không theo model
  order) + score mapping + retrieval_debug đúng (profile/embedding_model,
  không reranker_model khi không rerank); hai chunks cùng source+section ->
  sources theo context order, scores từng chunk, context JSON array generator
  nhận đúng + allowlist order; reranker model hiện trong debug khi profile
  hybrid_rerank; used_source_ids dedup; no-evidence -> 200 safe refusal,
  sources=[], model không được gọi; blank document context skip model; empty
  used_source_ids -> safe refusal; retrieval dependency failure 503
  `retrieval_unavailable`; generator not configured 503; timeout 504; provider
  unavailable 502; invalid output 502; unexpected failure 500
  `internal_error`; không sensitive payload; retrieval chạy qua thread pool.
- **test_context_builder.py (10)**: budget tính serialized JSON array (brackets
  + ", " giữa items); second chunk fit; stop trước chunk không vừa (whole chunk
  giữ nguyên trong block); max documents cap; empty input -> `"[]"`; empty
  text skip giữ rank; mapping cùng source+section -> JSON array đúng chunk_id;
  text chứa label giả của chunk khác -> không tạo block thừa và structural
  field đếm đúng 1 lần; source mapping fields và order; không mutate documents.

Full backend regression: `269 passed` (217 tests Phase 1-5 giữ nguyên + 52
mới cho Phase 6 revision 4).

Notebook checks: JSON hợp lệ; nbformat validate pass; 14 cells (7 code); mọi
`execution_count` null; mọi outputs rỗng; cell ids unique; nbconvert default
mode chạy đạt 0 cell errors với env `OPENAI_API_KEY`/`HUE_RAG_PHASE6_REAL` bị
unset (fake runner + fake stack); health trả ok với generator configured; real
mode skip đúng khi guard tắt.

`git diff --check` sạch; `git diff --name-only` + `git status --short` chỉ
chứa files thuộc allowlist Phase 6 cộng các thay đổi có sẵn của user
(`notebooks/01`, `notebooks/02`, `skills/karpathy-guidelines/`,
`knowledge-base/` deletions, guide Phase 6 do Codex cập nhật) — giữ nguyên,
không stage, không commit.

CodeGraph: sync theo workflow vì source thay đổi; index up to date với 64
python files, 1.022 nodes.

## Evaluation Results

Không có retrieval/answer benchmark run trong Phase 6 (thuộc Phase 7-8).
`reports/hue_foods_rag_benchmark.md` không được cập nhật vì smoke không phải
benchmark controlled run.

Live OpenAI smoke đã chạy ngày 2026-08-13 theo user approval — xem mục
"Live Smoke (2026-08-13)" bên dưới.

```text
Retrieval result file: none (deferred to Phase 7-8)
Answer result file: /tmp/phase6_live_smoke_evidence.json (safe summary, ngoài repo)
Benchmark log updated: no (smoke evidence không phải benchmark run)
```

## Deviations From Approved Guide

- Không deviation so với approved guide. Các interpretation note:
  - `Agent` config dùng `ModelSettings(max_tokens=1024)` vì Agents SDK 0.19.4
    expose `max_tokens` và map sang Responses API `max_output_tokens`; đã
    verify trong source package cài đặt — không âm thầm bỏ tham số.
  - Generator coi injected runner là ready mà không cần API key (fake runner
    không gọi network); `configured` = có key hoặc có runner. Health báo
    generator `configured` trong notebook fake mode.
  - `build_user_message` serialize toàn bộ runner input thành một JSON
    document; context format là JSON array do ContextBuilder tạo (contract
    nội bộ builder -> prompt); prompt builder và API route không đổi interface
    ngoài format context nội bộ.
  - Route no-evidence check dựa trên `context_result.sources` rỗng (context
    rỗng là `"[]"`, không còn `""`).
  - Test command dùng `uv run python -m pytest` (console entrypoint không hỗ
    trợ local package layout, precedent đã được Reviewer chấp nhận ở Phase 4-5).
  - Model ID preflight đã verify qua web 2026-08-13 (user approved web access);
    pricing/capability re-verify vẫn nằm trong preflight trước live smoke.

## Known Issues

- Severity: low. Live smoke đã chạy ngày 2026-08-13 (xem mục "Live Smoke
  (2026-08-13)"): hai đợt user-approved, tổng 12 calls, tổng 0,01493875 USD,
  không retry, dưới ceiling 0,25 USD. Mọi số liệu là live thật, không suy
  diễn từ fake runner.
- Severity: low. Adversarial tests kiểm tra boundary trên fake runner (JSON
  escaping ngăn forged structural field/section, allowlist không mở rộng,
  mapping không đổi); chúng không chứng minh LLM tuyệt đối miễn nhiễm prompt
  injection — real prompt-hardening cần evidence live smoke/evaluation
  Phase 7-8.
- Severity: low. JSON serialization làm runner input dài hơn plain text
  (overhead khoảng 100-150 ký tự/block tùy fields) — nằm trong budget 3000 ký
  tự đã enforce và được tính đúng trong tests.
- Severity: low. Latency gate và cost evidence chưa đo — thuộc live smoke
  approval.
- Severity: low. `verify_snapshot()` chưa được gọi trong request path (guide
  cấm per-request); lifespan build một lần và fail closed ở startup. App
  degraded-startup behavior được test bằng monkeypatch retrieval build fail.
- Severity: low. StarletteDeprecationWarning về httpx/TestClient (fastapi
  testclient) — không ảnh hưởng contract, thuộc ecosystem.
- Severity: low. No-evidence case trả safe refusal tiếng Việt cố định
  (`INSUFFICIENT_ANSWER`); nội dung refusal có thể tinh chỉnh ở Phase 7 khi có
  evaluation evidence.

## Security, Data Safety, Reliability, Performance Self-Check

- Security: không đọc/in/log `.env`, keys, headers; generator không log query,
  session ID, prompt, context, answer đầy đủ (chỉ model/latency/outcome/source
  count/token summary); error body chỉ chứa code + message tiếng Việt cố định,
  không raw exception/stack trace; prompt injection boundary: system policy
  nằm trong `Agent.instructions`, toàn bộ runner input là một JSON document
  serialize bằng thư viện chuẩn nên query và evidence text đều được escape —
  không thể giả mạo structural field hoặc section header; allowlist là field
  riêng không thể mở rộng bởi injected content; generic exception handler log
  exception cục bộ nhưng trả 500 an toàn; health/chat response không chứa
  secret (test riêng).
- Data safety: API không mutate collection/evaluation data; không lưu session
  hoặc history (UUID chỉ echo); sources chỉ projection fields approved; debug
  chỉ fields approved từ immutable startup snapshot; không trả vectors/raw
  provider payload; ContextBuilder không mutate documents (purity test giữ).
- Reliability: failure paths deterministic qua typed errors (10 codes);
  invalid structured output fail ngay không retry/repair; no-evidence skip
  model; generator not configured -> 503; retrieval build fail -> app vẫn
  alive degraded; thread pool cho sync retrieval; không silent fallback
  provider/profile.
- Performance: lifespan khởi tạo một lần (không per-request build); timeout
  45s enforce qua `asyncio.wait_for`; retrieval sync chạy qua thread pool
  không block event loop; generator là async await trực tiếp; JSON serialize
  bằng thư viện chuẩn (không parser tự viết) và nằm trong budget đã enforce;
  không unbounded work trong request path.
- Tests: 52 tests Phase 6 revision 4 + 269 full regression đều offline bằng
  fakes, không cần secrets, paid API, deploy hoặc external services.
- Notebooks: JSON hợp lệ, nbformat validate pass, outputs rỗng, execution_count
  null, cell ids unique, default cells chỉ dùng fake dependencies, real mode
  opt-in bằng env guard `HUE_RAG_PHASE6_REAL=1`.

## Live Smoke (2026-08-13)

Ghi chú governance: theo Codex review, live smoke là gate của session Reviewer.
Người dùng đã giao rõ nhiệm vụ này cho session Implementer (DeepSeek) và phê
duyệt hai đợt chạy riêng. Implementer chỉ chạy smoke và ghi evidence; phán
quyết final và user report vẫn thuộc Codex Reviewer.

Môi trường chạy:

- Qdrant 1.18.3 khởi động bằng Docker Compose pinned digest (không sửa
  container/config), collection `hue_foods_e5_small_384` green với đúng 572
  points, dense 384 cosine và sparse index — khớp contract Phase 4.
- Local models đã có cache: `intfloat/multilingual-e5-small` và
  `cross-encoder/ms-marco-MiniLM-L-6-v2`; không download mới.
- `OPENAI_API_KEY` được user provision sẵn trong process environment ngoài
  repo (chỉ kiểm tra presence, không đọc hoặc in giá trị).
- Active profile runtime: `dense_only` (config hiện hành, không sửa settings).
- Smoke runner: script dùng một lần đặt ngoài repo
  (`/tmp/phase6_live_smoke.py`), đi đúng runtime path retrieval -> context ->
  generator; capturing runner bọc đúng SDK `Runner.run` (cùng call path) để
  lấy token usage thật từ `result.raw_responses[].usage`.

Đợt 1 (6 calls, user-approved): cả 6 categories pass; token usage không bắt
được do SDK 0.19.4 không expose `RunResult.usage` (runtime log
`tokens=unknown`) nên chi phí tính theo worst-case estimate 2500/1024 mỗi call
= 0,00178 USD/call, tổng 0,01068000 USD.

Đợt 2 (6 calls, user-approved thêm để lấy usage thật):

| Category | Outcome | Tokens in/out | Retrieval ms | Generation ms | Cost USD |
|---|---|---|---|---|---|
| direct_fact | success | 1084/78 | 12896 | 3173 | 0,00031430 |
| comparative | error `InvalidGeneratorOutputError` | n/a (usage mất khi SDK raise) | n/a | n/a | 0,00178000 (worst-case charge) |
| relationship | success | 1265/108 | 23 | 1629 | 0,00038800 |
| spanning | success | 1446/463 | 18 | 3600 | 0,00086795 |
| food_knowledge | success | 1320/177 | 20 | 1727 | 0,00048525 |
| guide_planning | success | 1385/117 | 17 | 1261 | 0,00042325 |

Đợt 2 tổng: 0,00425875 USD. Tổng hai đợt: 12 calls, 0,01493875 USD, không
retry, dưới hard ceiling 0,25 USD.

Quan sát chất lượng:

- 5/6 answers tiếng Việt tự nhiên, grounded đúng evidence, `used_source_ids`
  hợp lệ theo context order (spanning dùng 3 sources, food_knowledge dùng 3
  chunks cùng document, guide_planning dùng food tour nửa ngày từ
  `food-guides.md`).
- Câu comparative ("Mệ Kéo hay Bà Nga mở buổi tối") đợt 2 bị
  `InvalidGeneratorOutputError`: model trả structured output không hợp lệ,
  generator fail-closed đúng contract (không retry, không repair, không
  fabricate source; API sẽ trả HTTP 502 `invalid_generator_output`). Cùng câu
  ở đợt 1 trả lời an toàn "Không đủ thông tin". Đây là observation cho Phase
  7 evaluation, không phải failure của error-mapping contract.
- No-evidence offline probe: `generate_answer` với context rỗng raise
  `InvalidQueryError` trước mọi runner call; counting runner ghi nhận 0 calls.
  Đúng zero-call path, không tốn chi phí.
- Model thỉnh thoảng tự chèn text `chunk_id` vào answer body; Phase 6 hoãn
  inline markers nên đây không vi phạm contract, ghi nhận cho Phase 7.

Findings cho Codex:

1. Minor runtime (đã sửa 2026-08-13 trong audit task): `_usage_tokens` đọc
   `result.usage` nhưng SDK 0.19.4 chỉ expose usage tại
   `result.raw_responses[].usage`, nên runtime log luôn `tokens=unknown`.
   Đã fix, thêm 3 unit tests và live verify - xem mục "Runtime Audit Fix
   (2026-08-13)".
2. Observation: 1/12 calls (2 đợt gộp) trả invalid structured output dù
   temperature 0.2; fail-closed hoạt động đúng. Đưa vào đánh giá Phase 7.
3. Evidence an toàn lưu tại `/tmp/phase6_live_smoke_evidence.json` (ngoài
   repo): category, question, outcome, latency, tokens, cost, used_source_ids
   — không chứa answer, raw payload hoặc secret.

## Notebook 06 Runtime-Real Redesign (2026-08-13)

Người dùng phê duyệt thiết kế lại toàn bộ sáu notebook canonical để Run All chạy
runtime thật (xem addendum `reports/notebooks_runtime_redesign_implementation_report.md`).
Riêng notebook Phase 6:

- Xóa fake generator, fake runner, fake stack, timeout fake demo, manual
  `json.dumps` evidence demo và guard `HUE_RAG_PHASE6_REAL`.
- Run All: một biến `question` -> key-presence check fail actionable ->
  `TestClient` với app thật/lifespan thật -> `/health` (cached readiness) ->
  đúng 1 `POST /api/chat` qua retrieval thật, ContextBuilder thật và OpenAI
  generator thật.
- Không retry; in safe fields: status, elapsed, answer, sources projection,
  session_id, retrieval_debug.

Live evidence ngày 2026-08-13 (đợt notebook validation, 1 paid call):

```text
OPENAI_API_KEY present: True
health: 200 ok, qdrant/retrieval ready, generator configured
chat: 200 trong 13.6s; answer tiếng Việt grounded; 3 sources hợp lệ;
retrieval_debug: dense_only, intfloat/multilingual-e5-small, 10 retrieved, 5 context sources
```

Chi phí: API response không chứa usage (SDK 0.19.4); worst-case charge 0,00178
USD, thực tế khoảng 0,0005-0,001 USD. Không in key, prompt, raw payload hoặc
header trong notebook hay report.

## Runtime Audit Fix (2026-08-13)

Audit bổ sung do user chỉ định (xem
`reports/runtime_fake_audit_implementation_report.md`) tìm thấy đúng một
finding thuộc Phase 6 cần sửa:

- `backend/llm/generator_openai.py` - `_usage_tokens` đọc `result.usage`
  nhưng Agents SDK 0.19.4 expose usage tại `result.raw_responses[].usage`,
  nên log runtime luôn in `tokens=unknown`. Đã sửa: duyệt `raw_responses`,
  lấy `input_tokens`/`output_tokens` từ entry đầu tiên có usage; không có
  usage vẫn trả `unknown` (không fabricate số).
- `backend/tests/test_llm_generator_openai.py` - thêm class `TestUsageTokens`
  (3 tests offline, deterministic): đọc từ raw_responses, first-with-usage
  wins, unknown khi thiếu usage.

Live evidence ngày 2026-08-13 (1 paid call, user-approved):

```text
answer generated model=gpt-5.4-nano outcome=success latency_ms=5440
source_count=1 tokens=421/48
```

Trước fix log này là `tokens=unknown`; sau fix là token counts thật. Chi phí
call này khoảng 0,00014 USD (421 input + 48 output theo giá official
0,20/1M input + 1,25/1M output). Full offline suite: 272 tests pass.

## Live Access / Secrets Statement

Đã chạy 14 live OpenAI calls (model `gpt-5.4-nano` qua OpenAI Agents SDK)
trong các đợt được người dùng phê duyệt rõ: 12 calls smoke (tổng 0,01493875
USD) + 1 call notebook runtime-real redesign (worst-case charge 0,00178 USD,
thực tế khoảng 0,0005-0,001 USD) + 1 call runtime audit fix (421 input + 48
output tokens, khoảng 0,00014 USD), không retry.
Không đọc hoặc in giá trị `OPENAI_API_KEY` (chỉ kiểm tra presence). Không lưu
answer, raw provider payload hoặc secret vào bất kỳ artifact repo nào; evidence
summary nằm ngoài repo tại `/tmp/phase6_live_smoke_evidence.json`. Không có
web access, deploy, dependency install hoặc collection mutation trong smoke.
Đã duyệt web (OpenAI developers docs + Agents SDK docs) theo user approval ở
revision 1 để verify model ID/pricing/parameters — read-only research, không
gọi model API.

## Handoff To Codex

Codex nên re-review lại sau revision 4:

1. **Single JSON runner input**: probe query chứa exact evidence header + fake
   JSON block + allowlist header — `json.loads` runner input phải cho query
   verbatim (escaped), evidence chỉ real blocks, allowlist đóng. Probe trên
   format plain-text sections phải fail (đã ghi evidence trong report).
2. **JSON evidence serialization**: probe text chứa bản sao exact structural
   object của chunk khác — evidence array parse đúng (chunk_id, text) theo
   context order, structural field đếm đúng 1 lần, text giả nằm trong value
   `text` được escape.
3. **Adversarial boundary**: probe injection trong query/evidence, delimiter
   giả, label JSON giả — system policy không lộ trong runner input, allowlist
   không mở rộng, mapping không đổi; boundary tests chạy trên fake runner
   (không live model); note: tests không chứng minh LLM miễn nhiễm injection
   tuyệt đối.
4. **Generator typed boundary**: fake runner probes cho timeout, blank answer,
   unknown source ID, wrong output type, provider error — mọi case ra typed
   error với safe fixed message; không retry.
5. **API mapping**: probe tất cả 10 codes (422 invalid_query/
   invalid_session_id/invalid_request, 503 retrieval_not_ready/
   retrieval_unavailable/generator_not_configured, 504 generator_timeout, 502
   generator_unavailable/invalid_generator_output, 500 internal_error) và
   normalized error shape `{"detail": {"code", "message"}}`.
6. **Source integrity**: sources theo context order, dedup, score ghép từ
   `RetrievedDocument`, unknown source ID reject; no-evidence skip model (sources
   rỗng) và empty used_source_ids -> safe refusal; context generator nhận là
   JSON array đúng chunk_id.
7. **Thread pool**: retrieval chạy qua `asyncio.to_thread` (test ghi thread id).
8. **Notebook**: nbformat validate, outputs rỗng, execution_count null, default
   mode chạy bằng fake, health ok không phụ thuộc key, real guard
   `HUE_RAG_PHASE6_REAL=1`.
9. **Model preflight**: ghi trong report là đã verify `gpt-5.4-nano` qua
   developers.openai.com (2026-08-13); re-verify trước live smoke.

Safe-default steps Codex/user dùng để verify phase:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile \
  llm/prompt.py llm/generator_openai.py api/app.py api/health.py \
  api/routes/chat.py retrieval/context_builder.py core/schema.py
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest \
  tests/test_llm_generator_openai.py tests/test_api_chat.py \
  tests/test_context_builder.py -q --tb=short
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q --tb=short
# Notebook default mode (an toàn, không cần OpenAI/Qdrant/model):
# mở notebooks/06_generation_and_api.ipynb và Run All
```

Live smoke đã chạy ngày 2026-08-13 theo user approval: Codex review thêm mục
"Live Smoke (2026-08-13)" ở trên và evidence summary tại
`/tmp/phase6_live_smoke_evidence.json` (safe summary ngoài repo). Phase 6
status hiện tại: `approved` — technical acceptance của Codex và user
confirmation đã hoàn tất; backend test suite đã migration live-only (xem
mục Trạng Thái Hiện Tại ở đầu report và
`reports/backend_tests_live_only_migration_implementation_report.md`).
Không tạo user report; không cập nhật `Project_Status.md`; không sửa guide;
không commit/push (thuộc Reviewer sau staged-scope audit).
