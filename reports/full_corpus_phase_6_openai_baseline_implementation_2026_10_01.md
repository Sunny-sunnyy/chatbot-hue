# Báo cáo triển khai & Correction 4 — Full-corpus Phase 6 OpenAI Baseline

**Ngày cập nhật:** 2026-10-01 (+07)
**Vai trò:** Implementer
**Thẩm quyền thực thi:** `session_prompt/CURRENT_HANDOFF.md`, `reports/full_corpus_phase_6_openai_baseline_correction_3_codex_review_2026_10_01.md` và `docs/superpowers/plans/2026-10-01-phase-6-openai-baseline-implementation-plan.md`
**Base commit:** `d0494072ae335f1e3f2492ed3be30a3ed42acb8b`
**Head commit:** worktree (dirty)
**Quyền Git:** `none` (không commit/push)
**Quyền Sub-agent:** `none`
**Quyền Paid Call:** `none` (không gọi lại OpenAI API trong correction batch này; 5 replacement calls chờ User cấp quyền riêng sau independent review)
**Trạng thái kiểm thử:** 141 non-paid tests PASS, 1 warning (46.91s); Metadata v2 complete verify `VERIFIED` (33.840 points); Exact uvicorn production startup `/health` HTTP 200 `ok` (đủ 5 components `ready`); `git diff --check` PASS (clean exit code 0); 5 prior live calls preserved (3 PASS, 2 FAIL).
**Kết luận kỹ thuật:** Hoàn tất 100% Correction batch 4 đóng toàn diện các findings P6-C3-R1 (Major) và P6-C3-R2 (Major). Sẵn sàng chuyển giao gói bàn giao `final_review` cho Reviewer Codex thẩm định độc lập.

---

## 1. Scope, authority and preserved dirty worktree

- Triển khai Tasks 1–6 theo kế hoạch ngày 01/10/2026 và thực hiện bốn đợt correction tinh chỉnh:
  - Correction 1: Xử lý production uvicorn import, runner single-loop, fail-closed structured output.
  - Correction 2: Quản lý FastAPI lifespan thật trong runner, loại bỏ provider response mocks, hoãn settings vào lifespan và làm sạch log.
  - Correction 3: Loại bỏ hoàn toàn global `app.state.last_chat_trace`; thay bằng request-scoped `EvidenceRecorder` (dựa trên `contextvars.ContextVar`); lưu trữ trích đoạn `excerpts` thực tế trong `packed_evidence`; đảm bảo atomic failure artifact cho mọi exit path sau paid confirmation; xử lý after-count failure thành `null`/unverified.
  - Correction 4:
    - **P6-C3-R1:** Ghi nhận metadata phản hồi từ provider (`response_id`, `model`, `latency_ms`, token usage, `finish_reason`) ngay sau khi `generator.generate_answer()` trả về thành công trước khi tiến hành bước xác thực trích dẫn (`select_cited_sources()`). Nếu trích dẫn vi phạm `CitationIntegrityError`, trạng thái được cập nhật thành `ERROR` và `error = "citation_integrity_failed"`, nhưng toàn bộ metadata kỹ thuật của provider đã trả được bảo lưu nguyên vẹn trong `RecordedEvidence`.
    - **P6-C3-R2:** Tách logic hoàn thiện artifact thành pure production helper `build_live_smoke_artifact(...)` và helper tuần tự hóa bằng chứng cuộc gọi `serialize_call_evidence(...)`. Thêm unit test kiểm định trực tiếp trên production helper xác nhận khi `after_count=None` thì `qdrant["after"] is None`, `point_count_intact = False` và đưa vào `unverified`, tuyệt đối không copy `before` sang `after`. Thêm integration test non-paid qua actual FastAPI route + `ASGITransport` + real retrieval/context builder từ Qdrant, kích hoạt nhánh `generator_ready = False` để chặn trước network call provider (không mock provider), chứng minh ContextVar thu thập excerpts thực tế qua ASGI route, ContextVar reset sau request, `app.state` không có trace, public envelope không lộ excerpts và `serialize_call_evidence` bảo toàn đầy đủ excerpts.
- Tuyệt đối tuân thủ hard boundaries:
  - Không gọi OpenAI, không chạy `phase6_live_smoke --confirm-paid`.
  - Không mutate Metadata v2 collections, Qdrant storage hay private corpus (33.840 points verified nguyên vẹn).
  - Không mock/fake/stub/replay provider response làm acceptance evidence.
  - Không commit/push Git; không gọi sub-agent.
  - Bảo lưu giao diện static HTML/CSS/JS thuần cho Phase 6 (Next.js dành cho phase frontend sản xuất kế tiếp theo thỏa thuận với User).
  - Giữ nguyên public API envelope `{answer, sources}`, không để rò rỉ private telemetry/trace ra response hay global shared state.
- Toàn bộ các tài liệu dirty pre-existing của Reviewer và User trên cây làm việc được bảo toàn nguyên vẹn:
  - `guides/README.md`, `guides/full_corpus_rag.md`, `guides/phase_6_generation_api.md`, `guides/phase_8_benchmark_model_selection.md`, `guides/phase_9_agentic_rag_roadmap.md`
  - `handoff_prompt/README.md`, `handoff_prompt/PHASE_6_OPENAI_BASELINE_REVIEW_CONTRACT.md`
  - `docs/superpowers/plans/2026-10-01-phase-6-openai-baseline-implementation-plan.md`
  - `docs/superpowers/specs/2026-10-01-phase-6-openai-baseline-amendment.md`
  - `reports/full_corpus_phase_6_openai_baseline_codex_review_2026_10_01.md`
  - `reports/full_corpus_phase_6_openai_baseline_correction_1_codex_review_2026_10_01.md`
  - `reports/full_corpus_phase_6_openai_baseline_correction_2_codex_review_2026_10_01.md`
  - `reports/full_corpus_phase_6_openai_baseline_correction_3_codex_review_2026_10_01.md`
  - `reports/user_reports/full_corpus_phase_6_openai_baseline_user_report_2026_10_01.md`
  - `session_prompt/Project_Status.md`
  - `"báo cáo nghiên cứu github.txt"`

---

## 2. Complete File Inventory

### A. Pre-existing Reviewer / User files (Preserved read-only)
- `guides/README.md`
- `guides/full_corpus_rag.md`
- `guides/phase_6_generation_api.md`
- `guides/phase_8_benchmark_model_selection.md`
- `guides/phase_9_agentic_rag_roadmap.md`
- `handoff_prompt/README.md`
- `handoff_prompt/PHASE_6_OPENAI_BASELINE_REVIEW_CONTRACT.md`
- `docs/superpowers/plans/2026-10-01-phase-6-openai-baseline-implementation-plan.md`
- `docs/superpowers/specs/2026-10-01-phase-6-openai-baseline-amendment.md`
- `reports/full_corpus_phase_6_openai_baseline_codex_review_2026_10_01.md`
- `reports/full_corpus_phase_6_openai_baseline_correction_1_codex_review_2026_10_01.md`
- `reports/full_corpus_phase_6_openai_baseline_correction_2_codex_review_2026_10_01.md`
- `reports/full_corpus_phase_6_openai_baseline_correction_3_codex_review_2026_10_01.md`
- `reports/user_reports/full_corpus_phase_6_openai_baseline_user_report_2026_10_01.md`
- `session_prompt/Project_Status.md`
- `"báo cáo nghiên cứu github.txt"`

### B. Core Implementation files (Tasks 1–6)
- `pyproject.toml`, `uv.lock`: Khai báo dependencies, pinned httpx 0.28.1, openai, pydantic.
- `backend/config/settings.yaml`: Cấu hình Phase 6 `full_corpus_generation`.
- `backend/core/schema.py`: Pydantic schema cho ChatRequest, ChatResponse, ErrorResponse, HealthResponse.
- `backend/core/settings_loader.py`: Nạp cấu hình settings an toàn.
- `backend/api/health.py`: Endpoint `/health` kiểm tra 5 thành phần.
- `backend/llm/openai_tokenizer.py`: Bộ đếm token o200k_base.
- `backend/llm/full_corpus_prompt.py`: Prompt builder và structured answer schema.
- `backend/retrieval/full_corpus_context.py`: Đóng gói ngữ cảnh và trích xuất `[citation]`.
- `backend/llm/citations.py`: Xử lý citations mapping.
- `backend/llm/representation_b.py`: Fallback và context representation.
- `backend/tests/conftest.py`: Fixtures kiểm thử.
- `backend/tests/test_phase6_settings.py`: 8 tests cấu hình settings.
- `backend/tests/test_full_corpus_context.py`: 6 tests đóng gói context.
- `backend/tests/test_citations.py`: 12 tests citations.
- `backend/tests/test_static_ui.py`: 2 tests static HTML/JS/CSS.
- `frontend/index.html`, `frontend/styles.css`, `frontend/app.js`: Static UI gọn gàng.
- `frontend/vendor/marked.umd.js`, `frontend/vendor/purify.min.js`: Thư viện vendor đã hash-pin.
- `notebooks/06_generation_and_api.ipynb`: Notebook sạch execution.
- `data/full_corpus_phase_6_live_cases.json`: File dữ liệu 4 test cases (git-ignored).
- `data/full_corpus_phase_6_live_smoke.json`: File kết quả 5 live calls ban đầu (git-ignored).

### C. Correction batch 4 files (Các tệp được tinh chỉnh để đóng P6-C3-R1 và P6-C3-R2)
- `backend/llm/evidence_recorder.py`: Bổ sung phương thức `record_generation_result(self, generated: Any)` và `mark_success(self)`; đảm bảo `record_error(...)` không xóa metadata kỹ thuật đã nhận từ provider.
- `backend/api/routes/chat.py`: Tách khối try/except cho `generate_answer` và `select_cited_sources`; gọi `recorder.record_generation_result(generated)` ngay sau khi generation thành công. Nếu citation validation ném ngoại lệ `CitationIntegrityError`, gọi `recorder.record_error("citation_integrity_failed")`, bảo lưu toàn bộ response ID/model/usage/finish metadata trong recorder.
- `backend/llm/phase6_live_smoke.py`:
  - Hiện thực hóa hàm thuần sản xuất `build_live_smoke_artifact(...)` dựng dictionary artifact hoàn chỉnh, độc lập với việc ghi file I/O.
  - Hiện thực hóa hàm thuần sản xuất `serialize_call_evidence(...)` trích xuất thông tin evidence thành dictionary an toàn cho runner artifact.
  - Sử dụng `build_live_smoke_artifact` bên trong `write_atomic_artifact`.
  - Sử dụng `serialize_call_evidence` trong runner loop Attempt 2–5.
- `backend/tests/test_phase6_live_smoke.py`:
  - Thay thế test dict giả lập bằng test trực tiếp hàm thuần sản xuất `test_build_live_smoke_artifact_after_count_null_yields_unverified_immutability`.
  - Bổ sung unit test thuần deterministic `test_evidence_recorder_preserves_generation_metadata_on_citation_error` chứng minh trình tự generation metadata -> citation error bảo lưu toàn bộ response ID/model/tokens/finish và status `ERROR`.
  - Bổ sung integration test `test_asgi_route_evidence_recorder_integration_with_real_retrieval` chạy qua actual FastAPI route + `ASGITransport` + real Qdrant retrieval/context packing, chặn trước network call provider bằng nhánh `generator_ready = False`, chứng minh ContextVar thu thập excerpts thực tế, ContextVar reset sau request, `app.state` không có trace và `serialize_call_evidence` bảo toàn trích đoạn excerpts (tổng 19 tests PASS).
- `reports/full_corpus_phase_6_openai_baseline_implementation_2026_10_01.md`: Cập nhật chi tiết kết quả Correction 4.
- `session_prompt/CURRENT_HANDOFF.md`: Cập nhật gói bàn giao `final_review` cho Reviewer.

---

## 3. Findings Resolution Mapping (Correction 4: P6-C3-R1..P6-C3-R2)

| Finding ID | Phân loại | Nội dung từ Reviewer Codex | Giải pháp kỹ thuật đã triển khai | Bằng chứng kiểm thử quan sát |
|---|---|---|---|---|
| **P6-C3-R1** | **Major** | Provider metadata bị mất khi SDK trả lời thành công nhưng citation validation ném ngoại lệ `CitationIntegrityError`. | Tách việc ghi nhận metadata: gọi `recorder.record_generation_result(generated)` ngay sau khi `generator.generate_answer()` trả về thành công, trước khi gọi `select_cited_sources()`. Khi citation thất bại, `record_error("citation_integrity_failed")` chỉ cập nhật status thành `ERROR` và ghi nhận mã lỗi mà không xóa các trường metadata kỹ thuật của provider. | Test `test_evidence_recorder_preserves_generation_metadata_on_citation_error` PASS: chứng minh sequence `record_generation_result` -> `record_error` bảo lưu nguyên vẹn `response_id`, `model`, `latency_ms`, `input_tokens`, `output_tokens`, `total_tokens`, `finish_reason` và gán status `ERROR`. |
| **P6-C3-R2** | **Major** | Hai regression tests quan trọng kiểm tra dict tự dựng thay vì production helper; chưa kiểm tra integration qua actual ASGI route và runner serialization với real retrieval. | (1) Tách logic hoàn thiện artifact và serialization thành 2 pure production helpers `build_live_smoke_artifact` và `serialize_call_evidence` trong `phase6_live_smoke.py`.<br>(2) Test trực tiếp `build_live_smoke_artifact` với `after_count=None` chứng minh `point_count_intact = False` và đưa vào `unverified` (không copy before count).<br>(3) Tạo integration test non-paid qua actual FastAPI route + `ASGITransport` + real retrieval từ Qdrant, chặn network call bằng nhánh `generator_ready = False`, xác nhận ContextVar truyền qua route thu thập trích đoạn excerpts, ContextVar reset sau request, `app.state` không có trace, public envelope không lộ excerpts và `serialize_call_evidence` bảo toàn excerpts. | Test `test_build_live_smoke_artifact_after_count_null_yields_unverified_immutability` PASS; test `test_asgi_route_evidence_recorder_integration_with_real_retrieval` PASS với real Qdrant retrieval; 0 provider mock. |

---

## 4. Fresh Non-Paid Command Ledger and Observed Results

Tất cả các kiểm tra dưới đây được chạy trực tiếp và ghi nhận kết quả quan sát thật (observed results) tại thời điểm lập báo cáo:

### Check 1: Focused pytest suite (141 passed, 1 warning in 46.91s)
```bash
cd /home/minhhieu/hue_rag/backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase6-review-uv-cache \
  uv run --env-file ../.env python -m pytest \
  tests/test_phase6_settings.py tests/test_full_corpus_context.py \
  tests/test_citations.py tests/test_openai_full_corpus_generator.py \
  tests/test_api_chat.py tests/test_static_ui.py \
  tests/test_phase6_live_smoke.py \
  tests/test_full_corpus_retrieval.py tests/test_full_corpus_metadata_v2.py \
  -q --tb=short
```
**Kết quả quan sát thực tế:**
```text
141 passed, 1 warning in 46.91s
```
*Ghi chú phân bổ số lượng test qua các đợt:*
- Ban đầu: 117 tests.
- Correction 1: 127 tests (+10 tests).
- Correction 2: 130 tests (+3 tests).
- Correction 3: 139 tests (+9 tests).
- Correction 4: **141 tests passed** (+2 tests mới):
  - +1 test `test_evidence_recorder_preserves_generation_metadata_on_citation_error` (kiểm tra bảo toàn provider metadata khi citation lỗi).
  - +1 test `test_asgi_route_evidence_recorder_integration_with_real_retrieval` (kiểm tra integration actual ASGI route + real retrieval + production runner serialization).
  - Test dict cũ được thay bằng `test_build_live_smoke_artifact_after_count_null_yields_unverified_immutability` kiểm tra trực tiếp pure production helper.
  - Toàn bộ suite không có bất kỳ provider-response mock hay fake nào.

### Check 2: Metadata v2 complete verify (33.840 points)
```bash
cd /home/minhhieu/hue_rag
UV_CACHE_DIR=/tmp/hue-rag-phase6-review-verify-uv-cache \
  uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify
```
**Kết quả quan sát thực tế:**
```text
Verification status: VERIFIED
```
(Xác nhận toàn bộ 4 collections Metadata v2 nguyên vẹn 8.460 points/collection, tổng 33.840 points, không bị mutate).

### Check 3: Exact real uvicorn startup from `backend/` and `/health`
```bash
cd /home/minhhieu/hue_rag/backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase6-review-api-uv-cache \
  uv run --env-file ../.env uvicorn api.app:app --host 127.0.0.1 --port 8016
```
Từ terminal khác:
```bash
curl -s http://127.0.0.1:8016/health
```
**Kết quả quan sát thực tế:**
```json
{"status":"ok","components":{"app":"alive","qdrant":"ready","retrieval":"ready","tokenizer":"ready","generator":"ready"}}
```
Khởi động thành công, trả HTTP 200 với tất cả 5 thành phần sẵn sàng. Tiến trình uvicorn sau đó được dừng an toàn.

### Check 4: Vendor asset hashes
```bash
cd /home/minhhieu/hue_rag
sha256sum frontend/vendor/marked.umd.js frontend/vendor/purify.min.js
```
**Kết quả quan sát thực tế:**
```text
fa0cfbf0181339312eaa3709b577ad698fc21a9baa42d580a3fd1f267b19b4a8  frontend/vendor/marked.umd.js
f263b05369e050fa175d4ecb9c9358eb4253602d510297adfb31df48b2f1c4d5  frontend/vendor/purify.min.js
```
Khớp hoàn toàn với các giá trị đã pin trong Review Contract.

### Check 5: Notebook clean state
```bash
python3 -c "import json; nb=json.load(open('notebooks/06_generation_and_api.ipynb')); code_cells=[c for c in nb['cells'] if c['cell_type']=='code']; assert all(c.get('outputs')==[] for c in code_cells); assert all(c.get('execution_count') is None for c in code_cells); print('NOTEBOOK_CLEAN_OK: cell_count =', len(nb['cells']), 'code_cells =', len(code_cells))"
```
**Kết quả quan sát thực tế:**
```text
NOTEBOOK_CLEAN_OK: cell_count = 8 code_cells = 3
```

### Check 6: Git formatting check
```bash
git diff --check
```
**Kết quả quan sát thực tế:**
```text
(Clean exit code 0, không có trailing whitespace hay lỗi newline at EOF)
```

### Check 7: Static audit
- 0 `logger.exception` trong toàn bộ `backend/api/` và `backend/llm/`.
- 0 `str(exc)` trong `backend/api/` và `backend/llm/`.
- 0 `last_chat_trace` trong production code (`backend/api/`, `backend/llm/`, `backend/retrieval/`).
- Bằng chứng context và trích đoạn excerpts được thu thập theo request scope độc lập, không tồn tại trong `app.state`.
- Provider metadata được bắt tức thì khi generator hoàn tất, bảo lưu ngay cả khi citation validation thất bại.
- Production helper `build_live_smoke_artifact` và `serialize_call_evidence` độc lập, có unit test bao phủ.

---

## 5. Reused Prior Five-call Ledger and Clarifications

Trong Correction 4, Implementer **tuyệt đối không thực hiện cuộc gọi có phí nào**. Dữ liệu cuộc gọi cũ trong `data/full_corpus_phase_6_live_smoke.json` được bảo lưu nguyên vẹn để phục vụ audit:

| Attempt | Case ID | Loại gọi | HTTP / Status | Ghi chú kỹ thuật |
|:---:|:---|:---|:---:|:---|
| 1 | `representation_b` | Direct context generation | PASS | Sinh ngữ cảnh Representation B thành công. |
| 2 | `direct_fact` | Chat request `/api/chat` | FAIL (502, 67ms) | Nguyên nhân do lỗi connection pool / event loop xung đột giữa asyncio.run và TestClient trong runner cũ. Đã sửa sang single async lifespan context trong runner mới. |
| 3 | `multi_source_synthesis` | Chat request `/api/chat` | PASS (200) | Trả lời thành công có trích dẫn `[3]`, khớp tài liệu Quần thể Di tích Cố đô Huế. |
| 4 | `conditional_evidence` | Chat request `/api/chat` | FAIL (200) | Trả về `INSUFFICIENT_ANSWER` dù context có chứa thông tin vé/miễn/giảm (Reviewer probe xác nhận 5 sources / 777 tokens). Runner mới đã trang bị cơ chế lưu giữ toàn bộ excerpts trong `packed_evidence` để audit trực tiếp vì sao model fallback. |
| 5 | `out_of_scope` | Chat request `/api/chat` | PASS (200) | Trả về chuẩn fallback `INSUFFICIENT_ANSWER` với `sources: []`. |

---

## 6. Handoff cho Reviewer

Gói bàn giao Correction 4 được chuyển giao sang cho Reviewer độc lập Codex thẩm định:
- **Tệp bàn giao:** `session_prompt/CURRENT_HANDOFF.md`
- **Mục tiêu:** Thẩm định độc lập việc đóng 2 findings P6-C3-R1 và P6-C3-R2.
- **Thẩm quyền tiếp theo:** Sau khi Reviewer xác nhận non-paid correction đạt chuẩn nghiệm thu kỹ thuật, việc thực hiện đúng 1 lần sequence 5 cuộc gọi thay thế (replacement five-call run) sẽ được đề xuất lên User cấp quyền thực thi riêng.
