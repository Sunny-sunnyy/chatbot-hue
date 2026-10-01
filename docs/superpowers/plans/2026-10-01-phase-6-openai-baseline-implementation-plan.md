# Phase 6 Full-corpus — OpenAI Baseline Revised Implementation Plan

> **For the Implementer:** User đã duyệt plan và Review Contract ngày
> 2026-10-01. Chỉ bắt đầu từ exact scope trong `CURRENT_HANDOFF.md`; handoff Qwen
> ngày 2026-09-30 không còn quyền thực thi.

**Status:** User-approved
**Owner:** Codex Reviewer
**Approved by:** User
**Approval date:** 2026-10-01 (+07)
**Implementation authorization:** One active handoff in `session_prompt/CURRENT_HANDOFF.md`
**Date:** 2026-10-01 (+07)

## 1. Goal và precedence

Triển khai Full-corpus Phase 6 trên canonical Metadata v2 với OpenAI
`gpt-5.4-nano` làm baseline generation, response-local citations và
static UI, đồng thời giữ private corpus fail-closed và đúng năm paid attempts.

Plan này là delta bắt buộc trên plan ngày 2026-09-30:

```text
docs/superpowers/plans/2026-09-30-phase-6-full-corpus-generation-api-ui-metadata-v2-implementation-plan.md
```

Implementer phải đọc cả hai. Mọi phần Metadata v2, retrieval cell, evidence-only
context, citation/API/UI, private provisioning, case set, non-paid gate và
five-attempt ceiling của plan 2026-09-30 vẫn giữ nguyên, trừ những mục được
override rõ trong plan này. Khi xung đột, plan 2026-10-01 ưu tiên.

Review Contract canonical cho package này:

```text
handoff_prompt/PHASE_6_OPENAI_BASELINE_REVIEW_CONTRACT.md
```

## 2. Canonical inputs

Đọc trước implementation theo thứ tự:

```text
full-read: session_prompt/IMPLEMENTER_WORKFLOW.md
full-read: session_prompt/Session_Prompt.md
targeted-read: session_prompt/Project_Status.md — current snapshot/safety only
full-read: session_prompt/CURRENT_HANDOFF.md — phải là handoff GPT mới
full-read: docs/superpowers/specs/2026-10-01-phase-6-openai-baseline-amendment.md
full-read: docs/superpowers/plans/2026-10-01-phase-6-openai-baseline-implementation-plan.md
full-read: handoff_prompt/PHASE_6_OPENAI_BASELINE_REVIEW_CONTRACT.md
full-read: docs/superpowers/specs/2026-09-30-phase-6-full-corpus-generation-api-ui-amendment.md
full-read: docs/superpowers/plans/2026-09-30-phase-6-full-corpus-generation-api-ui-metadata-v2-implementation-plan.md
targeted-read: backend/llm/generator_openai.py — existing Agent/Runner pattern only
targeted-read: backend/retrieval/full_corpus.py — canonical result/readiness contracts
```

Nguồn model/tokenizer phải re-verify ngay trước implementation:

- OpenAI model page:
  <https://developers.openai.com/api/docs/models/gpt-5.4-nano>
- OpenAI `tiktoken` model mapping:
  <https://github.com/openai/tiktoken/blob/main/tiktoken/model.py>

Nếu alias `gpt-5.4-nano`, `o200k_base`, Agents SDK structured output hoặc
parameter support khác với contract này, dừng và báo Reviewer; không tự pin
snapshot, đổi model, SDK path hoặc budget.

## 3. Locked OpenAI profile

```text
Provider: OpenAI direct
SDK: OpenAI Agents SDK for Python
Resolved SDK versions inspected for this plan: openai 2.53.0; openai-agents 0.19.4
Model: gpt-5.4-nano (floating alias; intentionally not snapshot-pinned)
Credential: OPENAI_API_KEY from process environment
Tokenizer encoding for application budget: o200k_base
Reasoning: do not configure or send; use model/SDK default
Temperature/top_p/penalties/verbosity: do not configure or send; use defaults
Answer max output: 2048 tokens
Representation B max output: 256 tokens
Application context limit: 16384 tokens
Reserved answer budget: 2048 tokens
Safety margin: 512 tokens
Maximum whole chunks: 5
Timeout: 45 seconds
OpenAI client max_retries: 0
Runner max_turns: 1
Model fallback: none
Application retry: none
Tracing: disabled
```

`16384` là application packing budget, không phải model context window. Token
counter phải dùng explicit `tiktoken.get_encoding("o200k_base")`; không gọi
`encoding_for_model()` để tránh phụ thuộc mapping alias/version. Output cap,
timeout và call ceiling là safety/reproducibility controls, không phải quality
tuning.

`gpt-5.4-mini` chỉ là Phase 7/8 evaluation judge. Nó không được khởi tạo hoặc
gọi trong Phase 6 implementation/live runner và không là fallback.

## 4. Global constraints

- Giữ toàn bộ private-data, Metadata v2, Qdrant read-only, citation, public
  envelope, UI và worktree constraints của plan 2026-09-30.
- Không tạo `qwen_tokenizer.py`, `generator_openrouter.py` hoặc dùng
  `OPENROUTER_API_KEY` trong Phase 6 generation.
- Không thêm direct `transformers` dependency chỉ để count generation tokens.
  Thêm direct `tiktoken` dependency và lock version qua `uv.lock`.
- Không chủ động upgrade/downgrade `openai` hoặc `openai-agents`. Nếu thêm
  `tiktoken` làm resolved versions trên thay đổi, dừng để Reviewer đánh giá SDK
  compatibility và lockfile diff trước khi tiếp tục.
- Không sửa existing Foods behavior ngoài phần thật sự cần cho full-corpus
  composition. `backend/llm/generator_openai.py` là lịch sử/as-built Foods;
  không mở rộng nó thành mutable multi-profile generator.
- Không mock/fake/stub/replay provider response làm acceptance evidence. Pure
  tests chỉ inspect deterministic configuration/schema/packing logic và không
  gọi mạng.
- Không paid call trước khi toàn bộ non-paid gate đạt. Mỗi attempted request dù
  fail vẫn tính; không có attempt thứ sáu.
- Không sửa Golden/evaluator, không chạy GPT-vs-Qwen benchmark và không thêm
  Phase 9 router/history/tool behavior.
- Không commit/push; không dùng sub-agent; không sửa Reviewer-owned docs ngoài
  final handoff path khi plan đã được cấp quyền.

## 5. Revised file map

Plan 2026-09-30 giữ nguyên file map, với các thay thế sau.

Không tạo:

```text
backend/llm/qwen_tokenizer.py
backend/llm/generator_openrouter.py
backend/tests/test_openrouter_generator.py
```

Tạo thay thế:

```text
backend/llm/openai_tokenizer.py
backend/llm/generator_openai_full_corpus.py
backend/tests/test_openai_full_corpus_generator.py
reports/full_corpus_phase_6_openai_baseline_implementation_2026_10_01.md
```

Các file Representation B, prompt/context/citations/API/UI/live runner và
notebook vẫn theo plan cũ nhưng đổi imports/config/model wording tương ứng.
Ignored private case/evidence paths giữ nguyên để không nhân đôi artifact:

```text
data/full_corpus_phase_6_live_cases.json
data/full_corpus_phase_6_live_smoke.json
```

## 6. Review Contract

Risk level vẫn là **high**: public API/runtime, paid provider, private corpus,
browser rendering và citation integrity. Exact evidence, Reviewer minimum gate,
stop conditions và closure boundary nằm trong:

```text
handoff_prompt/PHASE_6_OPENAI_BASELINE_REVIEW_CONTRACT.md
```

Technical PASS chỉ tạo `ready_for_user_confirmation`; không tự đóng Phase 6.

---

## Task 1 — Preflight, revised settings và OpenAI tokenizer

**Override plan 2026-09-30 Task 1.** Metadata v2 preflight và typed errors giữ
nguyên; Qwen tokenizer/dependency steps bị thay hoàn toàn.

**Files:** `pyproject.toml`, `uv.lock`, `backend/config/settings.yaml`,
`backend/core/settings_loader.py`, `backend/core/schema.py`,
`backend/llm/openai_tokenizer.py`, `backend/tests/test_phase6_settings.py`.

- [ ] Snapshot base/head/worktree và chạy fresh Metadata v2 complete verify theo
      command của plan 2026-09-30. Mismatch dừng trước edits.
- [ ] Viết RED tests cho exact settings và tokenizer constants:

```python
OPENAI_GENERATION_MODEL == "gpt-5.4-nano"
OPENAI_TOKEN_ENCODING == "o200k_base"
```

- [ ] `full_corpus_generation` phải có exact values:

```yaml
provider: openai
model: gpt-5.4-nano
api_key_env: OPENAI_API_KEY
token_encoding: o200k_base
answer_max_output_tokens: 2048
representation_b_max_output_tokens: 256
timeout_seconds: 45
context_limit: 16384
reserved_output_tokens: 2048
safety_margin: 512
max_context_documents: 5
```

Không thêm `temperature`, `top_p`, `reasoning_effort`, `verbosity`, provider
fallback hoặc retry key.

- [ ] Thêm direct dependency `tiktoken>=0.12,<1`, chạy `uv sync` và ghi thay đổi
      tương ứng vào `uv.lock`; không Git commit.
- [ ] `load_openai_tokenizer()` dùng explicit
      `tiktoken.get_encoding("o200k_base")`, cache một lần và trả object có
      `encode(text)`. Không network/model download ở runtime.
- [ ] Chạy focused settings/tokenizer tests GREEN và xác nhận không đọc/in key.

## Task 2 — Evidence-only context và citation integrity

**Giữ plan 2026-09-30 Task 2**, chỉ thay `load_qwen_tokenizer()` bằng
`load_openai_tokenizer()`. Các invariant vẫn là whole chunks theo rank,
stop-at-first-overflow, evidence parts only, response-local sources và không lộ
`source`, `chunk_id`, `domain`, document ID, score hoặc trace.

- [ ] Chạy RED rồi GREEN cho `test_full_corpus_context.py` và
      `test_citations.py` bằng tokenizer mới.
- [ ] Thêm một fixed Unicode/Vietnamese token-count assertion để phát hiện đổi
      encoding ngoài ý muốn; expected count phải được tính từ locked tiktoken
      version sau Task 1 và ghi trong test.
- [ ] Xác nhận context pack không import Transformers/Qwen tokenizer.

## Task 3 — OpenAI Agents SDK full-corpus generator và Representation B

**Override toàn bộ plan 2026-09-30 Task 3.**

**Files:** `backend/llm/generator_openai_full_corpus.py`,
`backend/llm/representation_b.py`,
`backend/tests/test_openai_full_corpus_generator.py`.

Interfaces:

```python
class AnswerOutput(BaseModel):
    answer: str

class SearchContextOutput(BaseModel):
    search_context: str

@dataclass(frozen=True)
class GeneratedText:
    text: str
    response_id: str | None
    model: str
    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None
    latency_ms: int

class OpenAIFullCorpusGenerator:
    @classmethod
    def from_environment(cls, settings: dict): ...
    async def generate_answer(self, query: str, context: str) -> GeneratedText: ...
    async def generate_search_context(self, search_text: str) -> GeneratedText: ...
    async def aclose(self) -> None: ...
```

- [ ] RED tests kiểm exact alias, `OPENAI_API_KEY`, empty/blank rejection,
      one-field schemas, `max_turns=1`, cap 2048/256, timeout 45 và absence của
      temperature/reasoning/sampling overrides. Tests không completion call.
- [ ] Tạo một reusable `AsyncOpenAI(api_key=..., timeout=45, max_retries=0)` và
      `OpenAIResponsesModel(model="gpt-5.4-nano", openai_client=client)`.
- [ ] Tạo hai fixed tool-less Agents dùng chung client/model, mỗi Agent có đúng
      một structured output schema. `ModelSettings` chỉ đặt exact `max_tokens`
      của operation, `include_usage=True` và `store=False`; không truyền
      temperature, reasoning, verbosity hoặc sampling knobs.
- [ ] Gọi `Runner.run(..., max_turns=1, run_config=RunConfig(
      tracing_disabled=True, trace_include_sensitive_data=False))` bên trong
      `asyncio.wait_for(..., timeout=45)`.
- [ ] Parse `final_output`, strip/reject blank, và trích safe response ID/usage
      từ `raw_responses` nếu SDK trả. Không gọi request thứ hai để lấy metadata.
- [ ] Map timeout/Agents/OpenAI/invalid-output thành `GenerationError`, không
      retry và không đổi model.
- [ ] Representation B assembly giữ deterministic length gates từ plan cũ;
      provider failure không được biến thành successful fallback.
- [ ] GREEN focused tests; xác nhận zero provider calls và close client đúng.

## Task 4 — FastAPI cutover

**Giữ plan 2026-09-30 Task 4** với substitutions:

```text
load_qwen_tokenizer              -> load_openai_tokenizer
OpenRouterQwenGenerator          -> OpenAIFullCorpusGenerator
OPENROUTER_API_KEY               -> OPENAI_API_KEY
Qwen/OpenRouter failure wording  -> OpenAI generation failure wording
timeout 90                       -> timeout 45
```

- [ ] Lifespan tạo canonical retrieval, tokenizer, context builder và generator
      đúng một lần; `finally` gọi `await generator.aclose()`.
- [ ] Cached health chỉ báo readiness, không gọi provider.
- [ ] Import-safe app không đọc private corpus/key khi import module.
- [ ] Strict API/citation/error envelopes giữ nguyên; không lộ raw provider
      error, response ID, token usage hoặc private metadata.
- [ ] Start real API read-only và gọi `/health`; không gửi `/api/chat` trước
      paid gate.

## Task 5 — Static UI

**Giữ nguyên plan 2026-09-30 Task 5.** Pinned marked/DOMPurify hashes, sanitized
Markdown, `textContent` source cards, keyboard citation focus và manual error
retry không phụ thuộc generator provider. Không gửi paid request khi kiểm UI.

## Task 6 — Non-paid gate, five-call runner và report

**Giữ case set và cấu trúc plan 2026-09-30 Task 6**, với overrides:

- runner dùng `OpenAIFullCorpusGenerator` và alias `gpt-5.4-nano`;
- configuration ledger ghi provider `openai`, model alias, `o200k_base`, caps,
  timeout, `max_retries=0`, `max_turns=1` và absence of overrides;
- đúng một Representation B attempt + bốn answer attempts;
- report path là
  `reports/full_corpus_phase_6_openai_baseline_implementation_2026_10_01.md`;
- notebook mô tả GPT baseline và Qwen mandatory Phase 8 candidate, không mô tả
  Qwen là Phase 6 runtime.

Non-paid focused command tối thiểu từ `backend/`:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase6-openai-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_phase6_settings.py tests/test_full_corpus_context.py tests/test_citations.py tests/test_openai_full_corpus_generator.py tests/test_api_chat.py tests/test_static_ui.py tests/test_full_corpus_retrieval.py tests/test_full_corpus_metadata_v2.py -q --tb=short
```

Sau đó Metadata v2 verify và `git diff --check` như plan cũ. Chỉ khi tất cả
PASS mới chạy đúng một lần:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase6-openai-live-uv-cache uv run --env-file ../.env python -m llm.phase6_live_smoke --cases ../data/full_corpus_phase_6_live_cases.json --output ../data/full_corpus_phase_6_live_smoke.json --confirm-paid
```

Runner phải atomically ghi artifact cả khi FAIL/incomplete và đếm attempted
calls, không chỉ successful calls. Không rerun. Audit ba grounded cases theo
claim/citation/excerpt và out-of-scope case theo exact fallback; replay recorded
response chỉ để render UI, không được dùng làm provider evidence mới.

Implementation report dùng 12 sections của plan 2026-09-30, đổi mọi Qwen/
OpenRouter wording sang observed OpenAI facts. Tracked report không chứa query,
answer, excerpt, source path, secret hoặc raw provider error.

## 7. Acceptance mapping

| Requirement | Evidence |
|---|---|
| GPT alias/direct OpenAI | Settings test, construction audit, live ledger |
| Model/SDK-default reasoning và sampling | Xác nhận các fields tương ứng không được cấu hình/truyền |
| Reproducible `o200k_base` budget | Tokenizer test và context tests |
| No retry/fallback, one turn | Client/Runner configuration audit |
| Metadata v2/evidence-only citations | Existing Task 2/4/6 gates |
| Strict API/safe UI | Existing Task 4/5 gates |
| Exactly five attempts | Atomic private ledger và Reviewer audit |
| Qdrant/corpus immutable | Before/after verify và command ledger |
| Qwen deferred to Phase 8 | Config/import scan và notebook/report wording |

## 8. Stop conditions

Ngoài stop conditions của plan 2026-09-30, dừng nếu:

- alias `gpt-5.4-nano` hoặc structured output không available;
- tiktoken mapping/encoding evidence không còn hỗ trợ `o200k_base`;
- Agents SDK buộc gửi reasoning/sampling override hoặc không thể tắt retry;
- `OPENAI_API_KEY` thiếu trước live gate;
- implementation cần OpenRouter/Qwen call hoặc thay đổi năm-call set;
- plan/handoff hiện hành chưa được User duyệt.

Observed provider failure được ghi FAIL/incomplete; không chuyển sang alias,
Qwen, `gpt-5.4-mini` hoặc model khác.

## 9. Approval effect

User đã duyệt plan và Review Contract ngày 2026-10-01. Reviewer đã cập nhật
canonical status/guide và tạo exact GPT Implementer handoff. Implementation chỉ
được bắt đầu theo handoff đó; paid calls vẫn bị khóa đến non-paid gate, còn
collection mutation, Git write và Phase 7/8/9 không được mở.
