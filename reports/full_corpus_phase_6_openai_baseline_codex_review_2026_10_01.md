# Codex Review: Phase 6 OpenAI baseline

Decision: changes_requested
Reviewer: Codex
Date: 2026-10-01 (+07)
Canonical guide: `guides/phase_6_generation_api.md`
Implementation report: `reports/full_corpus_phase_6_openai_baseline_implementation_2026_10_01.md`

## 1. Phạm vi đã review

Reviewer đã đọc full current handoff, OpenAI amendment, revised plan, Review
Contract và implementation report; đối chiếu delta còn hiệu lực từ package
Metadata v2. Review bao phủ toàn bộ runtime/config/test/UI/notebook mới, exact
tracked diff, untracked inventory và ignored five-attempt artifact.

Reviewer đã chạy focused suite với Qdrant thật, complete Metadata v2 verify,
`git diff --check`, kiểm SDK construction/signatures, asset hashes, notebook
clean state, exact artifact shape và một read-only retrieval/context probe cho
case `conditional_evidence`. Không gọi thêm OpenAI API.

## 2. Findings

### P6-R1 — blocker — public API không khởi động bằng exact production command

- Vị trí: `backend/api/app.py:20-22`, `backend/retrieval/full_corpus.py:18-83`,
  `backend/embedding/sparse.py:16-17`.
- Requirement: Task 4 yêu cầu chạy từ `backend/` bằng
  `uv run --env-file ../.env uvicorn api.app:app --host 127.0.0.1 --port 8016`,
  sau đó `/health` phải `ok` mà không gửi paid request.
- Evidence: fresh Reviewer run dừng lúc import với
  `ModuleNotFoundError: No module named 'backend'`; server chưa mở cổng và
  `/health` không thể kiểm. Focused pytest vẫn pass vì `tests/conftest.py` tự
  thêm cả repository root và `backend/` vào `sys.path`, nên không bảo vệ entry
  point production.
- Tác động: runtime/API/UI cốt lõi không thể khởi động theo contract; report
  khẳng định real `/health` HTTP 200 không được fresh production command hỗ trợ.
- Tiêu chí đóng: sửa import/package entry path bằng giải pháp trực tiếp, thêm
  focused regression bảo vệ exact import/startup path, chạy đúng uvicorn command
  và quan sát `/health` `ok`; không dùng `PYTHONPATH` tạm hoặc test-only path
  injection làm acceptance.

### P6-R2 — major — runner không thực hiện đúng approved five-call protocol

- Vị trí: `backend/llm/phase6_live_smoke.py:88-91,109-180,226-235`.
- Requirement: Representation B phải dùng `documents[0].text` từ real approved
  retrieval; exact cases schema/order phải fail closed; một reusable async
  client phải được dùng an toàn; immutability so sánh before/after chứ không biến
  observed count thành product invariant.
- Evidence:
  - runner chỉ kiểm `len(cases) == 4`, không khóa schema/version/order IDs;
  - attempt 1 dùng một đoạn text hard-code trong tracked source thay vì real
    retrieved `documents[0].text`;
  - generator được tạo trong TestClient lifespan nhưng attempt 1 được gọi qua
    `asyncio.run()` ở event loop khác; sau đó attempt 2 qua app loop thất bại
    trong 67 ms. Artifact không đủ để chứng minh đây là OpenAI failure thay vì
    runner/client-loop failure;
  - `point_count_intact` hard-code `8460`, trái boundary coi `8460` là observed
    count, không phải invariant.
- Tác động: attempt 1 không phải approved evidence; nguyên nhân attempt 2 không
  đáng tin; guard không bảo vệ exact paid input; runner có thể báo sai khi corpus
  hợp lệ thay đổi.
- Tiêu chí đóng: runner validate exact private schema/order, lấy Representation
  B input từ real retrieval, giữ cả năm calls trên một lifecycle/event-loop an
  toàn, so sánh point count before/after và không đặt corpus/query text trong
  tracked source. Thêm smallest useful non-paid regression cho các guard này.

### P6-R3 — major — live artifact thiếu evidence bắt buộc và grounded behavior chưa đạt

- Vị trí: ignored `data/full_corpus_phase_6_live_smoke.json`,
  `backend/llm/phase6_live_smoke.py:166-221`, implementation report §§6–7/10.
- Requirement: artifact phải giữ response ID/model/latency/usage/finish metadata
  khi SDK trả, packed excerpts cần cho independent audit, audit đủ ba grounded
  cases và out-of-scope fallback.
- Evidence:
  - cả bốn answer records không có response ID hoặc usage/finish metadata; runner
    chỉ giữ public API envelope nên làm mất metadata mà generator có thể trả;
  - attempt 4 fallback có `sources: []` và artifact không giữ packed evidence,
    khiến report không thể tự chứng minh nhận định “dù tài liệu có thông tin”;
  - fresh read-only Reviewer probe xác nhận case này retrieve 10 documents,
    pack 5 sources/777 tokens, và packed context có term vé, miễn, giảm cùng dữ
    liệu số; model vẫn trả insufficient fallback;
  - chỉ attempt 3 có thể audit citation/excerpt; hai grounded cases còn lại fail.
- Tác động: live acceptance là `FAIL` 3/5, required conditional answer chưa đạt,
  và không đủ provenance để phân loại attempt 2 hay audit đủ contract.
- Tiêu chí đóng: runner lưu safe per-call metadata cùng private packed evidence
  cần audit mà không lộ qua public API/tracked artifact; report không gán lỗi cho
  provider nếu evidence không chứng minh. Sau khi non-paid correction được
  Reviewer chấp nhận, một fresh replacement five-call sequence cần User cấp
  authority riêng; hiện không có quyền paid rerun.

### P6-R4 — major — structured-output failure có thể bị chấp nhận như success

- Vị trí: `backend/llm/generator_openai_full_corpus.py:155-177` và các log tại
  `backend/llm/generator_openai_full_corpus.py:146-153`,
  `backend/api/app.py:63-110`, `backend/api/routes/chat.py:65-112`.
- Requirement: structured output/provider failure phải fail closed thành typed
  error; không log raw provider body, private path/context hoặc unexpected
  exception text.
- Evidence: nếu `final_output` là string nhưng không parse được bằng Pydantic,
  code gán nguyên string vào `val` và tiếp tục trả `GeneratedText`. Các broad
  exception/log branches đưa `str(exc)` vào GenerationError hoặc log.
- Tác động: unstructured output có thể vượt strict one-field contract; unexpected
  provider/private detail có thể đi vào tracked application logs.
- Tiêu chí đóng: mọi non-conforming output bị reject bằng generic typed error;
  logs chỉ ghi safe category/context, không raw exception payload. Thêm focused
  deterministic tests cho malformed string/dict/blank/extra-field outputs.

### P6-R5 — major — evidence index và handoff không khớp worktree thật

- Vị trí: `session_prompt/CURRENT_HANDOFF.md` §§2/5, implementation report
  §§5/8/11.
- Requirement: complete changed/untracked inventory, truthful command ledger và
  fresh `git diff --check` PASS.
- Evidence:
  - fresh `git diff --check` fail tại old handoff line 70 do trailing whitespace;
  - handoff/report ghi check sạch và real `/health` đạt, trái fresh observations;
  - handoff §5 không liệt kê đầy đủ các dirty Reviewer-owned paths/untracked
    artifacts đang có, dù phần đầu chỉ mô tả chúng theo nhóm.
- Tác động: Reviewer không thể dùng handoff như complete evidence index.
- Tiêu chí đóng: sửa whitespace, ghi complete inventory phân biệt preserved
  pre-existing paths với correction paths, cập nhật report bằng observed facts
  và fresh exact commands; không ghi expected hoặc TestClient observation thành
  production uvicorn PASS.

## 3. Cách Reviewer chạy lại thật

```bash
cd /home/minhhieu/hue_rag/backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase6-review-uv-cache \
  uv run --env-file ../.env python -m pytest \
  tests/test_phase6_settings.py tests/test_full_corpus_context.py \
  tests/test_citations.py tests/test_openai_full_corpus_generator.py \
  tests/test_api_chat.py tests/test_static_ui.py \
  tests/test_full_corpus_retrieval.py tests/test_full_corpus_metadata_v2.py \
  -q --tb=short

cd /home/minhhieu/hue_rag
UV_CACHE_DIR=/tmp/hue-rag-phase6-review-verify-uv-cache \
  uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify

git diff --check

cd /home/minhhieu/hue_rag/backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase6-review-api-uv-cache \
  uv run --env-file ../.env uvicorn api.app:app --host 127.0.0.1 --port 8016
```

Reviewer còn inspect SDK/config bằng construction-only Python, kiểm SHA-256 hai
vendor assets, notebook JSON, ignored case/artifact schemas và chạy một read-only
retrieval/context probe. Không chạy lệnh `phase6_live_smoke`.

## 4. Kết quả quan sát

- Focused non-paid suite: `117 passed, 1 warning`.
- Metadata v2 complete verify: `VERIFIED` cho 33.840 points.
- SDK/config: `openai 2.53.0`, `openai-agents 0.19.4`, `tiktoken 0.14.0`, alias
  `gpt-5.4-nano`, client retries 0, caps 2048/256; reasoning/sampling fields
  không được cấu hình.
- Vendor hashes: khớp hai pin đã duyệt.
- Notebook: parse được, 8 cells, mọi code cell có `execution_count: null` và
  outputs rỗng.
- Reused live artifact: timestamp/config/base nhất quán, đúng 5 records, Qdrant
  8460 trước/sau, nhưng overall `FAIL` với 3 PASS/2 FAIL. Evidence được reuse vì
  Reviewer không sửa code/config và không được phép gọi paid lần nữa.
- `git diff --check`: FAIL do trailing whitespace.
- Exact uvicorn startup: FAIL do import path trước khi `/health` có thể gọi.
- Conditional read-only probe: retrieval/context có evidence liên quan nhưng
  live answer vẫn fallback.

## 5. Giới hạn hoặc phần chưa chạy

- Reviewer không chạy thêm paid call theo five-attempt ceiling.
- Artifact hiện tại không giữ answer-call response metadata hoặc packed evidence
  cho failed cases, nên không thể xác nhận nguyên nhân attempt 2 và không thể
  audit đủ ba grounded cases.
- Reviewer chưa chạy browser tương tác thủ công; static source/tests được kiểm,
  nhưng runtime server blocker khiến end-to-end UI path chưa hợp lệ.

## 6. Decision và bước tiếp theo

Verdict: **CHANGES REQUESTED**.

Non-paid implementation có nhiều phần đúng, nhưng Phase 6 chưa sẵn sàng cho User
confirmation do public runtime blocker, live runner/evidence deviations, strict
structured-output gap và observed grounded-answer failure. `CURRENT_HANDOFF.md`
được chuyển thành một correction batch cho Implementer. Correction không cấp
paid call, Git write, Qdrant mutation hoặc sub-agent authority.

Sau khi correction non-paid được independent review đạt, Reviewer phải trình
User xin exact authority cho một replacement five-call sequence; artifact cũ
không thể được gọi là PASS và không được rerun trước authorization đó.
