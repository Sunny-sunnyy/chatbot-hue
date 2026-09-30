# Phase 6 Full-corpus Generation, API, Citations và Static UI — Metadata v2 Implementation Plan

> **For the Implementer:** Thực hiện tuần tự theo
> `session_prompt/IMPLEMENTER_WORKFLOW.md` và checkbox trong plan này. Một
> Implementer handoff duy nhất; `Sub-agent authorization: none`. Không dùng
> sub-agent, không commit/push và không chạy paid call trước non-paid gate.

**Status:** User-approved

**Approved by:** User

**Approval date:** 2026-09-30

**Goal:** Mở public full-corpus chat runtime trên canonical Metadata v2
retrieval, Qwen/OpenRouter generation, response-local citations và static UI,
với private corpus fail-closed và đúng năm paid call attempts.

**Architecture:** FastAPI chỉ load private settings/dependencies trong lifespan,
tạo canonical full-corpus retrieval service, pinned Qwen tokenizer,
evidence-only context builder và reusable `AsyncOpenAI` client. Request đi tuyến
tính `retrieval v2 -> whole-chunk packing -> one-shot generation -> citation
validation -> source mapping -> static UI`; không duplicate Metadata v2
validation và không thêm fallback/abstraction.

**Tech Stack:** Python 3.13, FastAPI, Pydantic, OpenAI Python SDK 2.53.0,
Transformers 5.x, Qdrant, pytest, vanilla HTML/CSS/JavaScript, marked 18.0.12,
DOMPurify 3.4.15.

## Canonical inputs

Đọc theo mức sau trước implementation:

```text
full-read: session_prompt/IMPLEMENTER_WORKFLOW.md
full-read: session_prompt/Session_Prompt.md
targeted-read: session_prompt/Project_Status.md — current snapshot, safety boundaries, Phase 6/Metadata v2 status
full-read: session_prompt/CURRENT_HANDOFF.md
full-read: docs/superpowers/specs/2026-09-30-phase-6-full-corpus-generation-api-ui-amendment.md
full-read: docs/superpowers/specs/2026-09-14-phase-6-full-corpus-generation-api-ui-written-spec.md
full-read: docs/superpowers/plans/2026-09-14-phase-6-full-corpus-generation-api-ui-implementation-plan.md
targeted-read: docs/superpowers/specs/2026-09-29-full-corpus-metadata-v2-written-spec.md — §§8–11
targeted-read: backend/retrieval/full_corpus.py — result models, payload validation, search(), build_full_corpus_retrieval_service()
```

Plan ngày 2026-09-14 cung cấp exact component bodies, prompt copy, static UI
code, five-call case list và locked hashes. Plan hiện tại cấp lại authority theo
source Metadata v2 hiện hành và thay thế task/checkpoint/lifecycle instructions
cũ. Nếu hai plan mâu thuẫn, plan này ưu tiên.

## Global constraints

- Private corpus phải tồn tại local tại `knowledge-base-hue/`; không track,
  download, reconstruct, print hoặc copy corpus vào artifact.
- Metadata v2 build records và bốn Metadata v2 Qdrant targets immutable/read-only.
- Runtime cell cố định:
  `e5-small-384 + dense_bm25_rrf + none`; không phải benchmark winner.
- Model cố định `qwen/qwen3.5-9b`; `temperature=0`; answer cap `2048`;
  Representation B cap `256`; timeout `90`; OpenAI client `max_retries=0`.
- OpenRouter request gửi `provider.require_parameters=true`; không provider pin,
  provider order, model fallback hoặc application retry.
- Context limit `16384`, output reserve `2048`, safety margin `512`, tối đa năm
  whole chunks theo rank.
- Context/citations chỉ dùng `title`, `heading_path`, `evidence_parts`.
  `search_text`, `chunk_id`, `domain`, point ID, path, score và trace là private.
- Public success đúng `{answer,sources}`; public failure đúng
  `{error:{code,message}}`.
- Không mock, fake, stub, replay hoặc fabricated provider response làm evidence.
  Pure deterministic values nhỏ chỉ dùng cho pure decision logic.
- Non-paid gate phải đạt trước bounded runner; runner có đúng năm Qwen attempts,
  call thất bại vẫn tính và không có call thứ sáu.
- Không sửa `knowledge-base-hue/`, Qdrant data, build records, Metadata v2
  migration/retrieval semantics hoặc Golden/evaluator.
- Không hoàn tác/stage các thay đổi hiện có của User. Git authorization là
  `none`; mọi proposed commit label dưới đây chỉ là nhãn lịch sử, không phải lệnh.

## Locked external artifacts

- Qwen tokenizer repo: `Qwen/Qwen3.5-9B`.
- Qwen tokenizer revision:
  `c202236235762e1c871ad0ccb60c8ee5ba337b9a`.
- marked 18.0.12:
  `https://cdn.jsdelivr.net/npm/marked@18.0.12/lib/marked.umd.js`.
- marked SHA-256:
  `fa0cfbf0181339312eaa3709b577ad698fc21a9baa42d580a3fd1f267b19b4a8`.
- DOMPurify 3.4.15:
  `https://cdn.jsdelivr.net/npm/dompurify@3.4.15/dist/purify.min.js`.
- DOMPurify SHA-256:
  `f263b05369e050fa175d4ecb9c9358eb4253602d510297adfb31df48b2f1c4d5`.

Các pin trên là behavior đã duyệt, không tự nâng version. Preflight ngày
2026-09-30 xác nhận model/revision và package versions vẫn tồn tại; missing
local tokenizer được tải đúng revision trong Task 1.

## Planned file map

Create:

```text
backend/llm/qwen_tokenizer.py
backend/llm/full_corpus_prompt.py
backend/llm/generator_openrouter.py
backend/llm/representation_b.py
backend/llm/citations.py
backend/llm/phase6_live_smoke.py
backend/retrieval/full_corpus_context.py
backend/tests/test_phase6_settings.py
backend/tests/test_full_corpus_context.py
backend/tests/test_citations.py
backend/tests/test_openrouter_generator.py
backend/tests/test_static_ui.py
frontend/index.html
frontend/styles.css
frontend/app.js
frontend/vendor/marked.umd.js
frontend/vendor/purify.min.js
data/full_corpus_phase_6_live_cases.json  # ignored/private execution input
data/full_corpus_phase_6_live_smoke.json  # ignored/private exact evidence
reports/full_corpus_phase_6_generation_api_ui_implementation_2026_09_30.md
```

Modify:

```text
pyproject.toml
uv.lock
backend/config/settings.yaml
backend/core/settings_loader.py
backend/core/schema.py
backend/api/app.py
backend/api/health.py
backend/api/routes/chat.py
backend/retrieval/full_corpus.py
backend/tests/conftest.py
backend/tests/test_api_chat.py
backend/tests/test_full_corpus_retrieval.py
notebooks/06_generation_and_api.ipynb
session_prompt/CURRENT_HANDOFF.md  # exact final transfer only
```

Implementer không sửa guide, spec, plan, status, user report hoặc
Reviewer-owned document khác. `CURRENT_HANDOFF.md` chỉ được thay ở final step
bằng exact `final_review` transfer được Review Contract yêu cầu.

## Review Contract

**Risk level:** high — public API/runtime, browser rendering, paid provider,
private corpus và citation integrity.

### Evidence Implementer phải cung cấp

- exact changed/untracked path inventory và diff;
- non-paid command ledger với observed result, không ghi expected thành PASS;
- fresh Metadata v2 complete verify hoặc exact failure;
- startup/health/API/UI observations trên approved read-only runtime cell;
- pinned tokenizer revision và browser-asset hashes;
- ignored/private JSON ledger của đúng năm Qwen attempts, gồm response
  ID/model/provider
  nếu có, latency, token usage, cost nếu có, finish reason và classification;
- manual citation-to-excerpt audit cho ba grounded answer cases;
- Qdrant point count/schema trước/sau và confirmation không mutation;
- failed, skipped, partial và not-live-verified branches;
- implementation report theo Task 6.

### Independent Reviewer minimum gate

Reviewer phải:

1. xác nhận base/head/worktree và mọi changed/untracked path;
2. đọc exact diff và map vào amendment + Phase 6 acceptance;
3. chạy `git diff --check`;
4. chạy focused non-paid settings/context/citation/API/UI/retrieval checks;
5. start real API read-only, kiểm cached health và một non-paid route boundary;
6. kiểm static assets/hash/sanitization và keyboard citation code path;
7. audit từng claim/citation trong paid artifact với exact returned excerpts;
8. xác nhận không leak private Metadata v2 fields và không mutation.

Reviewer được reuse five-call artifact nếu timestamp, config, exact call count
và safe metadata nhất quán. Reviewer không tự chạy paid call bổ sung.

### Stop conditions

Dừng ngay trước paid runner nếu:

- private corpus/build records/Qdrant targets chưa ready hoặc source hashes lệch;
- exact tokenizer/assets không resolve hoặc hash sai;
- focused affected checks chưa PASS;
- public output có thể lộ path, trace, `chunk_id`, `domain`, score hoặc secret;
- worktree overlap không thể giữ nguyên;
- implementation cần collection mutation, model/provider change hoặc call thứ
  sáu.

Provider/Qwen failure trong bounded runner được ghi là observed FAIL/incomplete,
không retry hoặc thay call.

### Closure boundary

Technical PASS chỉ tạo `ready_for_user_confirmation`. Reviewer sẽ viết review,
Approval Closure Contract và user report; User confirmation mới đóng Phase 6.
Git commit/push cần exact authorization riêng ở cuối session.

---

### Task 1: Preflight, Phase 6 settings và pinned tokenizer

**Files:**

- Modify: `pyproject.toml`
- Modify: `uv.lock`
- Modify: `backend/config/settings.yaml`
- Modify: `backend/core/settings_loader.py`
- Modify: `backend/core/schema.py`
- Create: `backend/llm/qwen_tokenizer.py`
- Create: `backend/tests/test_phase6_settings.py`

**Interfaces:**

- Produces `validate_phase6_settings(settings: dict) -> None`.
- Preserves strict default `load_settings()` while allowing the API lifespan to
  call `load_settings(validate_private_paths=False)` and defer only private-path
  existence to canonical retrieval readiness.
- Produces `load_qwen_tokenizer(*, local_files_only: bool = True)`.
- Produces `ContextBudgetError` và `CitationIntegrityError`.
- Produces exact `full_corpus_runtime`/`full_corpus_generation` settings consumed
  by Tasks 2–6.

- [ ] **Step 1: Snapshot authority và private readiness**

Run from repository root:

```bash
git rev-parse HEAD
git status --short
UV_CACHE_DIR=/tmp/hue-rag-phase6-preflight-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify
```

Expected only when observed: four Metadata v2 target pairs `VERIFIED`, total
33,840 points. Any mismatch stops before edits. Do not print `.env`, corpus
paths, payloads or vectors.

- [ ] **Step 2: Add failing settings/tokenizer/error tests**

Use the tests in historical Plan Task 1 with these additions:

```python
def test_phase6_errors_are_typed():
    from core.schema import CitationIntegrityError, ContextBudgetError
    assert issubclass(ContextBudgetError, RuntimeError)
    assert issubclass(CitationIntegrityError, RuntimeError)


def test_qwen_tokenizer_constants_are_exact():
    from llm.qwen_tokenizer import QWEN_TOKENIZER_REPO, QWEN_TOKENIZER_REVISION
    assert QWEN_TOKENIZER_REPO == "Qwen/Qwen3.5-9B"
    assert QWEN_TOKENIZER_REVISION == "c202236235762e1c871ad0ccb60c8ee5ba337b9a"
```

Run:

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-phase6-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_phase6_settings.py -q --tb=short
```

Expected RED: missing Phase 6 settings/module/error types.

- [ ] **Step 3: Add exact configuration and dependency**

Add `"transformers>=5.14.1,<6"` as a direct dependency and run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase6-plan-uv-cache uv sync
```

Add exact `full_corpus_runtime` and `full_corpus_generation` mappings from
historical Plan Task 1. Implement `validate_phase6_settings(settings)` with
exact-key/value checks and call it from `load_settings()` after current
full-corpus validation. Add keyword-only `validate_private_paths: bool = True`
to `load_settings()` and `validate_full_corpus_settings()`: the default keeps
the current `root.is_dir()` gate; `False` skips only that existence check, not
schema/glob/conditions/model validation. Add the two typed errors immediately
after `GenerationError`.

- [ ] **Step 4: Implement and cache the exact tokenizer revision**

Create `backend/llm/qwen_tokenizer.py` exactly as historical Plan Task 1. Then
download tokenizer-only files for the locked revision:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase6-plan-uv-cache uv run python -c "from huggingface_hub import snapshot_download; print(snapshot_download(repo_id='Qwen/Qwen3.5-9B', revision='c202236235762e1c871ad0ccb60c8ee5ba337b9a', allow_patterns=['tokenizer*', '*.json', '*.jinja', 'chat_template*']))"
```

Do not download 19GB model weights. The runtime uses tokenizer files locally
and remote OpenRouter generation.

- [ ] **Step 5: Run GREEN and self-review Task 1**

Run the Step 2 test command. Expected: exact tests PASS with
`local_files_only=True` and no key in output. Read Task 1 diff; do not commit.

---

### Task 2: Evidence-only context packing và citation integrity

**Files:**

- Create: `backend/llm/full_corpus_prompt.py`
- Create: `backend/retrieval/full_corpus_context.py`
- Create: `backend/llm/citations.py`
- Modify: `backend/tests/conftest.py`
- Create: `backend/tests/test_full_corpus_context.py`
- Create: `backend/tests/test_citations.py`

**Interfaces:**

- Produces `build_answer_messages(query: str, context: str)` and
  `build_representation_b_messages(search_text: str)`.
- Produces immutable `PackedSource`, `PackedContext` and
  `FullCorpusContextBuilder.build(query, documents) -> PackedContext`.
- Produces `select_cited_sources(answer, sources) -> tuple[PackedSource, ...]`.

- [ ] **Step 1: Add one read-only canonical retrieval fixture**

Append fixtures from historical Plan Task 2, but consume Metadata v2 result
correctly:

```python
PHASE6_CONTEXT_CHECK_QUESTION = "Huế"


@pytest.fixture(scope="session")
def full_corpus_documents(full_corpus_service):
    result = full_corpus_service.search(PHASE6_CONTEXT_CHECK_QUESTION)
    assert result.documents
    assert all(doc.id and doc.metadata.get("domain") for doc in result.documents)
    assert all(doc.metadata.get("evidence_parts") for doc in result.documents)
    return result.documents
```

`PHASE6_CONTEXT_CHECK_QUESTION` là input integration tối thiểu, không phải fixed
private evaluation case. Fixture không được create/delete collection.

- [ ] **Step 2: Write RED packing/citation tests**

Implement the exact tests from historical Plan Task 2 and add private-boundary
assertions:

```python
def test_packed_context_excludes_metadata_v2_private_fields(full_corpus_documents):
    packed = make_builder().build("Huế", full_corpus_documents)
    assert packed.sources
    for document in full_corpus_documents[:len(packed.sources)]:
        assert document.id not in packed.text
        assert document.metadata["source"] not in packed.text
        assert document.metadata["domain"] not in packed.text
```

Run:

```bash
cd backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase6-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_full_corpus_context.py tests/test_citations.py -q --tb=short
```

Expected RED: missing context/citation modules.

- [ ] **Step 3: Implement prompt, packing and citation modules**

Use exact prompt copy, types, signatures and algorithms from historical Plan
Task 2. Mandatory Metadata v2 rules:

```python
PackedSource(
    id=response_local_number,
    title=document.metadata["title"],
    heading_path=tuple(document.metadata["heading_path"]),
    excerpts=tuple(part["text"] for part in document.metadata["evidence_parts"]),
)
```

Never read `document.text`, `document.id`, `metadata.source` or
`metadata.domain` when building answer blocks/source cards. Preserve whole
chunks, rank order, stop-at-first-overflow and exact fallback/citation rules.

- [ ] **Step 4: Run GREEN and read-only invariants**

Run Step 2. Record observed test count, selected collection, point count before
and after, and confirm no write API was called. Self-review Task 2 diff; do not
commit.

---

### Task 3: Direct OpenRouter generator và Representation B capability

**Files:**

- Create: `backend/llm/generator_openrouter.py`
- Create: `backend/llm/representation_b.py`
- Create: `backend/tests/test_openrouter_generator.py`

**Interfaces:**

- Produces `OpenRouterQwenGenerator.from_environment(settings)`.
- Produces async `generate_answer(query, context) -> GeneratedText`.
- Produces async `generate_search_context(search_text) -> GeneratedText`.
- Produces `build_representation_b_search_text(...) -> RepresentationBResult`.

- [ ] **Step 1: Write RED construction/schema/pure-length tests**

Use the three exact tests from historical Plan Task 3. The real client
construction test may read `OPENROUTER_API_KEY` but must not make a completion
call. The length decision may use a callable over a deterministic string; it is
not provider evidence.

Run:

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-phase6-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_openrouter_generator.py -q --tb=short
```

Expected RED: missing generator/Representation B modules.

- [ ] **Step 2: Implement direct structured generation**

Implement historical Plan Task 3 exactly, with these required request fields:

```python
response = await client.chat.completions.create(
    model="qwen/qwen3.5-9b",
    messages=messages,
    temperature=0,
    max_tokens=max_tokens,
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": schema_name,
            "strict": True,
            "schema": output_type.model_json_schema(),
        },
    },
    extra_body={"provider": {"require_parameters": True}},
)
```

Use `AsyncOpenAI(base_url="https://openrouter.ai/api/v1", timeout=90,
max_retries=0)`. Parse strict one-field Pydantic models, reject blank/invalid
output and keep provider/cost fields `None` when not returned. Never make a
secondary metadata/cost request.

- [ ] **Step 3: Implement deterministic Representation B assembly**

Use exact `RepresentationBResult` and
`build_representation_b_search_text(...)` from historical Plan Task 3. A valid
generated augmentation that exceeds any of the three embedding tokenizer limits
returns unchanged A with reason `combined_text_exceeds_embedding_limit`.
Provider/generation failure is not a successful fallback.

- [ ] **Step 4: Run GREEN without paid completion**

Run Step 1. Confirm no completion log/response ID exists and no secret appears.
Self-review Task 3 diff; do not commit.

---

### Task 4: Import-safe FastAPI cutover và typed public API

**Files:**

- Modify: `backend/api/app.py`
- Modify: `backend/api/health.py`
- Modify: `backend/api/routes/chat.py`
- Modify: `backend/retrieval/full_corpus.py`
- Modify: `backend/tests/test_api_chat.py`
- Modify: `backend/tests/test_full_corpus_retrieval.py`

**Interfaces:**

- Consumes canonical `build_full_corpus_retrieval_service`,
  `FullCorpusContextBuilder`, `OpenRouterQwenGenerator`, `select_cited_sources`.
- Produces cached readiness and strict `/api/chat` envelopes.
- Keeps module-level `app = create_app()` import-safe without private corpus.
- Normalizes missing/unreadable private corpus discovery to
  `ComponentNotReadyError` before any Qdrant/model work.

- [ ] **Step 1: Write RED import/readiness/API contract tests**

Replace Foods answer-only assertions with the Phase 6 contract from historical
Plan Task 4. Add an import-safety test that does not load settings:

```python
def test_module_app_import_does_not_load_private_runtime():
    module = importlib.import_module("api.app")
    assert module.app.state.retrieval_ready is False
    assert module.app.state.tokenizer_ready is False
    assert module.app.state.generator_ready is False
```

Add strict 422 tests for blank, oversized, wrong-type and extra-field bodies.
Do not create fake retrieval/provider objects to force dependency failures.

Run:

```bash
cd backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase6-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_api_chat.py -q --tb=short
```

Expected RED: old Foods lifecycle, `detail` envelope and answer-only response.

- [ ] **Step 2: Move settings/private dependency loading into lifespan**

`create_app(settings=None)` must not call `load_settings()` before constructing
the app. Resolve inside lifespan:

```python
runtime_settings = (
    settings
    if settings is not None
    else load_settings(validate_private_paths=False)
)
runtime = runtime_settings["full_corpus_runtime"]
generation = runtime_settings["full_corpus_generation"]
```

This preserves strict path validation for ingestion while allowing clean-clone
module import. Catch settings/root/source/build/schema freshness failures at the
startup boundary and cache:

```python
(409, "corpus_reingest_required", "Dữ liệu tra cứu cần được lập chỉ mục lại.")
```

Default settings/ingestion validation remains strict. The runtime-only flag
defers private root existence to the readiness boundary; it does not synthesize
missing files or allow stale service startup.

- [ ] **Step 3: Build the canonical Metadata v2 runtime once**

Before app composition, wrap source discovery/state computation at the start of
`build_full_corpus_retrieval_service(...)`:

```python
try:
    root, rel_paths = discover_full_corpus_files(settings)
    current_sources = compute_corpus_state(root, rel_paths)
except (OSError, ValueError) as exc:
    raise ComponentNotReadyError(
        "Full-corpus private source state is unavailable"
    ) from exc
```

Require at least one discovered path before build-record validation. Add a
focused test using a nonexistent temporary root and assert
`ComponentNotReadyError`; because discovery fails first, the test must not
construct or call Qdrant/model dependencies.

Inside lifespan construct exactly:

```python
retrieval_service = build_full_corpus_retrieval_service(
    candidate_id=runtime["candidate_id"],
    retrieval_treatment=runtime["retrieval_treatment"],
    reranker=runtime["reranker"],
    settings=runtime_settings,
)
tokenizer = load_qwen_tokenizer(local_files_only=True)
context_builder = FullCorpusContextBuilder(
    tokenizer,
    context_limit=generation["context_limit"],
    reserved_output_tokens=generation["reserved_output_tokens"],
    safety_margin=generation["safety_margin"],
    max_documents=generation["max_context_documents"],
)
generator = OpenRouterQwenGenerator.from_environment(runtime_settings)
```

Close created resources in `finally`. Never call Metadata v2 validators a
second way or load MiniLM for the `none` cell.

- [ ] **Step 4: Implement strict route and health**

Use strict Pydantic request/source/response models and `error_response(...)`
from historical Plan Task 4. Consume `result.documents`; never return
`result.trace`. Apply exact mapping from amendment §7. Health only reads cached
state and returns components `app`, `qdrant`, `retrieval`, `tokenizer`,
`generator`.

Known failure branches not naturally triggered are static-reviewed and reported
`not live-verified`; do not monkeypatch dependencies or use a dead URL.

- [ ] **Step 5: Run GREEN and real read-only startup**

Run:

```bash
cd backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase6-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_api_chat.py tests/test_full_corpus_retrieval.py -q --tb=short
```

Start the app without sending a paid chat request:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase6-plan-uv-cache uv run --env-file ../.env uvicorn api.app:app --host 127.0.0.1 --port 8016
```

Observe `/health`, then stop. Expected only when observed: status `ok`, Metadata
v2 retrieval/tokenizer/generator ready, zero Qwen completion calls and unchanged
Qdrant point count. Self-review Task 4 diff; do not commit.

---

### Task 5: Minimal safe static UI

**Files:**

- Create: `frontend/index.html`
- Create: `frontend/styles.css`
- Create: `frontend/app.js`
- Create: `frontend/vendor/marked.umd.js`
- Create: `frontend/vendor/purify.min.js`
- Modify: `backend/api/app.py`
- Create: `backend/tests/test_static_ui.py`

**Interfaces:**

- Consumes public `{answer,sources}` hoặc `{error:{code,message}}`.
- Produces `/`, `/static/*`, sanitized Markdown and accessible `[n]` focus.

- [ ] **Step 1: Download and verify exact pinned assets**

Run from repository root:

```bash
mkdir -p frontend/vendor
curl --fail --silent https://cdn.jsdelivr.net/npm/marked@18.0.12/lib/marked.umd.js -o frontend/vendor/marked.umd.js
curl --fail --silent https://cdn.jsdelivr.net/npm/dompurify@3.4.15/dist/purify.min.js -o frontend/vendor/purify.min.js
sha256sum frontend/vendor/marked.umd.js frontend/vendor/purify.min.js
```

Require the exact hashes in `Locked external artifacts`; mismatch stops Task 5.

- [ ] **Step 2: Write RED local-asset/static-serving tests**

Use exact `test_static_ui.py` from historical Plan Task 5. Add assertions that
no CDN URL exists and only sanitized marked output reaches `innerHTML`.

Run:

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-phase6-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_static_ui.py -q --tb=short
```

Expected RED: missing UI or 404.

- [ ] **Step 3: Implement the approved static UI**

Use exact HTML/CSS/JavaScript behavior from historical Plan Task 5: one form,
loading/duplicate-submit guard, sanitized Markdown, source cards built with
`textContent`, citation click and Enter/Space focus, Vietnamese error and manual
retry. Mount `/static` and `/` after API routers; no catch-all route.

- [ ] **Step 4: Run GREEN and non-paid accessibility observation**

Run Step 2, start the server as in Task 4, and inspect `/` plus local assets.
Verify tab order, visible focus, disabled/loading state code and retry control
without submitting a paid chat request. Self-review Task 5 diff; do not commit.

---

### Task 6: Non-paid gate, exactly-five-call runner và evidence handoff

**Files:**

- Create: `backend/llm/phase6_live_smoke.py`
- Create ignored/private: `data/full_corpus_phase_6_live_cases.json`
- Create ignored/private: `data/full_corpus_phase_6_live_smoke.json`
- Create: `reports/full_corpus_phase_6_generation_api_ui_implementation_2026_09_30.md`
- Modify: `notebooks/06_generation_and_api.ipynb`
- Modify at final transfer only: `session_prompt/CURRENT_HANDOFF.md`

**Interfaces:**

- Consumes Tasks 1–5 and ignored/private input containing the exact four answer
  cases locked in historical Plan Task 6.
- Produces exactly five observed Qwen attempts and one ignored/private exact
  evidence artifact.
- Produces final implementation report and Reviewer handoff data.

- [ ] **Step 1: Implement guarded runner before executing it**

Before coding the runner, create ignored
`data/full_corpus_phase_6_live_cases.json` from the four exact approved cases in
historical Plan lines 1549–1566. Convert the `ANSWER_CASES` tuple mechanically
to JSON with top-level
`{"schema_version":"phase_6_full_corpus_live_cases:v1","cases":[...]}`;
each ordered item has exactly string fields `case_id` and `question`. Require
the exact ordered case IDs `direct_fact`, `multi_source_synthesis`,
`conditional_evidence`, `out_of_scope`. Do not copy the question strings into
source, notebook, report or handoff.

Use runner contract from historical Plan Task 6, changing the output to ignored
`data/full_corpus_phase_6_live_smoke.json`. Preserve the historical top-level
shape and set `schema_version` to `phase_6_full_corpus_live_smoke:v2`; add
`configuration.collection_contract = "metadata_v2"`; require configuration
values from Global constraints; require `call_attempt_count = 5`; derive
`calls`, `checks`, `unverified` and final `status` from execution.

`status` must be computed, never hard-coded. The ignored local artifact may hold
the exact question, answer and returned excerpts needed for independent audit,
but must not store source paths, `chunk_id`, `domain`, full private trace,
secrets or raw provider errors. Tracked files contain only case IDs, safe
aggregate metadata and audit conclusions. Use the exact one Representation B +
four answer cases already approved; do not invent a new query set.

- [ ] **Step 2: Run the complete non-paid gate**

Run from `backend/`:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase6-plan-uv-cache uv run --env-file ../.env python -m pytest tests/test_phase6_settings.py tests/test_full_corpus_context.py tests/test_citations.py tests/test_openrouter_generator.py tests/test_api_chat.py tests/test_static_ui.py tests/test_full_corpus_retrieval.py tests/test_full_corpus_metadata_v2.py -q --tb=short
```

Then from repository root:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase6-preflight-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify
git diff --check
```

Do not continue unless every required check freshly PASSes, eight collections
remain green/read-only and all four Metadata v2 pairs verify. Full backend suite
is not required unless these changes produce an unexplained failure indicating
wider blast radius.

- [ ] **Step 3: Execute the single bounded paid run**

Run exactly once from `backend/`:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase6-live-uv-cache uv run --env-file ../.env python -m llm.phase6_live_smoke --cases ../data/full_corpus_phase_6_live_cases.json --output ../data/full_corpus_phase_6_live_smoke.json --confirm-paid
```

The runner must expose the exact `--cases` and `--output` arguments shown above.

The command records exactly five attempts and writes PASS/FAIL/incomplete
artifact atomically. Any failure consumes its slot. No rerun or sixth call
without new User authority.

- [ ] **Step 4: Audit observed answers and UI without another call**

For the three grounded answer cases, compare every claim/citation with exact
returned excerpts and preserve conditions/conflicts. Require out-of-scope exact
fallback with `sources: []`. Render one recorded real response in the UI without
calling `/api/chat` again; verify Markdown sanitization and citation focus.

- [ ] **Step 5: Update notebook as an explanation, not an executor**

Update `notebooks/06_generation_and_api.ipynb` to explain Metadata v2 runtime,
Qwen profile, Representation B separation, public contract and links to the
implementation report plus ignored local evidence path. Copy only safe observed
summaries; do not copy questions, answers or excerpts. Repository notebook must
have empty outputs and `execution_count: null`; Run All must not silently issue
paid calls.

- [ ] **Step 6: Write the implementation report**

Create the dated report with sections:

```text
1. Scope, authority and preserved dirty worktree
2. Changed paths and responsibility
3. Private prerequisites and Metadata v2 readiness
4. Runtime configuration and immutable revisions
5. Non-paid command ledger and observed results
6. Five-call ledger
7. Citation-to-evidence manual audit
8. API/static UI observations
9. Qdrant/build-record immutability
10. Failed, skipped and not-live-verified
11. Acceptance mapping and final implementation conclusion
12. Reviewer handoff
```

Report is an evidence index, not approval. It must not contain private corpus
inventory, source paths, fixed query set, exact answers/excerpts/payloads,
secrets or raw provider response. It references local case IDs and the ignored
exact evidence path for Reviewer inspection.

- [ ] **Step 7: Final self-review and handoff**

Run:

```bash
git status --short
git diff --check
git diff --stat
```

Read every changed path and remove duplication, unused helpers, defensive
fallbacks, test-only mechanisms and out-of-scope edits. Provide the Reviewer:

- base/head plus complete changed/untracked inventory;
- exact commands and observed results;
- artifact/report/notebook paths;
- deviations, failures, skipped and not-verified items;
- one next action: independent Phase 6 final review.

Replace `session_prompt/CURRENT_HANDOFF.md` with one concise `final_review`
handoff containing base/head, complete changed paths, acceptance/evidence map,
ignored exact evidence path, implementation-report path, failures/limits,
Reviewer reruns, `Git authorization: none` and `Sub-agent authorization: none`.
Do not commit, push, edit other Reviewer-owned docs or run additional paid calls.

## Spec coverage and simplicity check

| Requirement | Plan coverage |
|---|---|
| Private corpus provisioned outside Git, fail-closed | Tasks 1, 4, 6 |
| Strict Metadata v2 retrieval only | Tasks 1, 2, 4, 6 |
| Evidence-only Top-5/token budget | Task 2 |
| Direct Qwen/OpenRouter and Representation B | Task 3 |
| Strict API, errors and cached health | Task 4 |
| Sanitized static UI and accessible citations | Task 5 |
| Real-system verification and five-call ceiling | Task 6 |
| No collection mutation/private-field leak | Review Contract, Tasks 2, 4, 6 |
| One Implementer handoff | Review Contract, Task 6 |

The plan adds only components with a named Phase 6 consumer. Metadata v2
validation remains in canonical retrieval; private provisioning remains an
operator precondition; error handling has no retry/recovery stack; static UI has
no framework or build pipeline.

## Approval effect

User approval of this plan authorizes Reviewer to update canonical guide/status
and create one exact Implementer handoff. It does not itself start execution,
commit/push Git, mutate collections, extend paid calls, change model/provider or
open Phase 7.
