# Codex Review: Phase 6 Grounded answer generation và JSON API

Decision: ready_for_user_confirmation
Reviewer: Codex
Date: 2026-08-13
Review path:

```text
reports/phase_6_generation_api_codex_review.md
```

Implementer report:

```text
reports/phase_6_generation_api_implementation_report.md
```

Phase guide context:

```text
guides/phase_0_mvp_foundation.md
guides/phase_6_generation_api.md
session_prompt/Project_Status.md
reports/hue_foods_rag_benchmark.md
```

## Tóm Tắt

Revision 4 giữ runner input là một JSON document duy nhất; query, evidence và
allowlist có ranh giới cấu trúc rõ. Offline review đã đạt. Live smoke do
Implementer thực hiện theo hai lần user-approved xác nhận runtime path
`retrieval -> context -> generator` hoạt động với Qdrant collection 572 points
và profile `dense_only`.

Đợt đầu phủ sáu category và đạt 6/6. Đợt bổ sung lấy usage thật có 5 success;
một output structured không hợp lệ bị generator chặn đúng contract, không retry
và không bịa nguồn. Tổng 12 calls là 0,01493875 USD, thấp hơn hard ceiling
0,25 USD. Technical decision là `ready_for_user_confirmation`; Phase chưa
`approved` cho đến khi người dùng xác nhận notebook và user report.

Redesign notebook sau đó đã thay fake/opt-in flow bằng runtime thật theo yêu cầu
user. Codex chạy độc lập notebook 01–05: E5 cache-only tạo 572 vectors chuẩn
hóa; Qdrant collection green có 572 points; ba profile dùng đúng score fields.
Notebook 06 được kiểm tra source/static và có evidence một OpenAI call qua full
`/api/chat` path, không cần phát sinh thêm paid call trong review.

## Findings

Không có blocker hoặc major findings.

- resolved minor: runtime audit follow-up đã sửa `_usage_tokens()` để đọc
  `raw_responses[].usage` của Agents SDK 0.19.4. Chỉ entry có đủ input và
  output tokens mới được log; partial/missing usage trả `unknown` mà không bịa.
  Re-review xác nhận 28 targeted tests; evidence Implementer ghi 274 full
  backend tests pass. Không ảnh hưởng answer, source integrity hay cost ceiling.
- minor: script smoke tạm thời in tối đa 400 ký tự answer ra stdout. JSON evidence
  ngoài repo không chứa answer/payload/secret và không có raw answer được commit.
  Nếu chạy lại smoke, script phải bỏ dòng in này để chỉ giữ safe summary.

## Verification

Các validation Codex chạy độc lập:

```bash
codegraph status .
# Index is up to date: 64 files, 1,022 nodes, 2,988 edges.

cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile \
  llm/prompt.py llm/generator_openai.py api/app.py api/health.py \
  api/routes/chat.py retrieval/context_builder.py core/schema.py
# Pass.

UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest \
  tests/test_llm_generator_openai.py tests/test_api_chat.py \
  tests/test_context_builder.py -q --tb=short
# 60 passed, 1 StarletteDeprecationWarning.

UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q --tb=short
# 269 passed, 1 StarletteDeprecationWarning.

# Notebook runtime-real redesign review
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "... nbformat.validate notebooks/01-06 ..."
# 6/6 valid; committed outputs empty and execution_count null.
# Reviewer executed notebooks/01-05 with local runtime: all 0 cell errors.
# Notebook 06 source/static check passed; one paid API call is evidenced in the
# implementation report and was not repeated by reviewer.

git diff --check
# Clean.
```

Reviewer probe với query chứa exact forged evidence header, fake JSON block và
forged allowlist xác nhận payload parse thành đúng ba top-level fields: query
giữ nguyên verbatim, evidence chỉ có `real|0`, và allowlist chỉ có `real|0`.
ContextBuilder JSON-array budget và no-evidence path `sources == []` cũng được
đối chiếu trực tiếp.

Notebook redesign validation đạt: cả 6 notebook parse được, cell IDs duy nhất,
mọi committed output rỗng và mọi `execution_count` là `null`. Reviewer chạy
01–05 độc lập: E5 cache-only tạo 572 vectors 384 chiều normalized, Qdrant
read-only xác nhận schema/count 572, ba profile thực chạy đúng score fields.
Notebook 06 dùng full API path và có evidence đúng một OpenAI call; reviewer
không lặp lại call này.

Live smoke evidence `/tmp/phase6_live_smoke_evidence.json` được reviewer đọc
trực tiếp. Đợt đầu: 6/6 category pass, worst-case estimate 0,01068000 USD.
Đợt hai (user-approved bổ sung): 5 success, 1 `InvalidGeneratorOutputError`,
usage thật 0,00425875 USD. No-evidence probe có 0 runner call. Tổng 12 calls:
0,01493875 USD, không retry. Evidence chỉ chứa summary an toàn.

Official OpenAI preflight ngày 2026-08-13 xác nhận alias
`gpt-5.4-nano`, snapshot `gpt-5.4-nano-2026-03-17`, Responses API,
structured outputs, context window 400.000 tokens, maximum output 128.000
tokens và giá standard text `$0.20/1M` input, `$1.25/1M` output. Phase config
giới hạn 1.024 output tokens/call, nên riêng worst-case output của 6 calls là
6.144 tokens, tương đương `$0.00768`; toàn smoke vẫn phải kiểm tra input estimate
trước từng call và dừng nếu có nguy cơ vượt tổng ceiling `$0.25`.
Nguồn: [official OpenAI documentation](https://developers.openai.com/api/docs/models/gpt-5.4-nano).

Không in hoặc lưu giá trị credential trong review. Reviewer không gọi lại live
API; validation live dựa trên safe evidence do Implementer ghi ngoài repo.

## Runtime Audit Follow-up

Finding telemetry được resolved trước final technical verdict. Reviewer probe
xác nhận usage không có token fields trả `unknown`; entry partial trước entry
đầy đủ trả `421/48`. `tests/test_llm_generator_openai.py` đạt 28 passed và
full backend suite đạt 274 passed theo re-run/evidence của Implementer, với một
`StarletteDeprecationWarning` đã biết. Không có OpenAI call mới trong follow-up.

## Scope Check

Revision 4 và live smoke nằm trong allowlist Phase 6. User đã phê duyệt thêm
một đợt sáu calls chỉ để lấy usage thật; đây là exception execution có ghi
evidence, vẫn không retry và tổng chi phí dưới ceiling. Các deletions dưới `knowledge-base/`,
thay đổi `notebooks/01_backend_foundation.ipynb`,
`notebooks/02_foods_data_and_chunking.ipynb` và thư mục `skills/` là thay đổi
có sẵn ngoài Phase 6; Codex không sửa, stage hoặc reset chúng.

Reviewer chỉ cập nhật guide/index, Codex review report và snapshot bàn giao theo
yêu cầu kết thúc session của người dùng. Không sửa implementation report, runtime
code, notebook hoặc benchmark ledger.

## Safety And Quality Check

- Security: JSON structural boundary và safe provider-error mapping đạt; không
  đọc `.env`, không log prompt/context/answer hoặc credential trong runtime.
- Data safety: API không mutate Qdrant, collection, evaluation data hoặc session
  history.
- Reliability: typed failures, timeout, no retry, cached readiness và
  no-evidence zero-call path đạt offline tests.
- Performance: sync retrieval chạy qua thread pool; provider runner async có
  timeout 45 giây và output bound 1.024 tokens.
- Tests: 60 targeted tests và 269 full backend tests đạt.
- Notebooks: 01–06 dùng runtime thật theo user-approved contract; 04 chỉ
  Qdrant read-only, 06 đúng một paid call mỗi Run All, outputs committed rỗng.
- Evaluation: smoke chỉ xác nhận integration/failure handling, không phải
  benchmark retrieval hoặc answer quality Phase 7-8.

## Required Changes

Not applicable.

## User Confirmation Readiness

- Files accepted technically: Phase 6 runtime, tests, config, notebook,
  implementation report và review report theo guide.
- Notebook: `notebooks/06_generation_and_api.ipynb`; Run All dùng full API path
  thật, yêu cầu key đã có trong environment và gọi đúng một OpenAI call;
  committed notebook không có outputs hay execution count.
- User report: `reports/user_reports/phase_6_generation_api_user_report.md`.
- User cần chạy notebook từ trên xuống với key đã export, đọc giới hạn và xác
  nhận hoặc yêu cầu sửa. Phase 7 vẫn đóng; `Project_Status.md` chưa được đánh
  dấu approved.
