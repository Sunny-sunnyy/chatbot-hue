# Implementation Report: Runtime Fake/Fallback Audit (2026-08-13)

Implementer: DeepSeek
Date: 2026-08-13
Report path:

```text
reports/runtime_fake_audit_implementation_report.md
```

Context:

```text
session_prompt/IMPLEMENTER_WORKFLOW.md
guides/phase_0_mvp_foundation.md
reports/phase_6_generation_api_implementation_report.md
```

## Approved Scope

Người dùng chỉ định audit bổ sung toàn bộ `backend/**/*.py`, Python scripts và
tài liệu runtime: tìm mọi fake/mock/stub/sample vector giả, fake runner, fake
Qdrant client, opt-in real-mode guard, fallback từ runtime thật sang fake và
runtime path không đi qua Qdrant/local model/OpenAI đúng contract.

Nguyên tắc bắt buộc: fake/mock trong `backend/tests/**` phải giữ nguyên (test
offline, deterministic); runtime production không được có fake fallback;
dependency injection chỉ phục vụ unit tests, không làm production fallback;
missing key/Qdrant/model cache phải fail closed và actionable.

Phê duyệt kèm: Qdrant read-only, E5/MiniLM cache-only (`HF_HUB_OFFLINE=1`),
OpenAI `gpt-5.4-nano` được gọi thật thoải mái trong ngân sách còn lại 3 USD,
không OpenRouter, không collection mutation, không đụng notebooks (task riêng
đang chạy), không sửa Project_Status/guides/Codex review/user reports, không
commit/push.

## Audit Table

| Area | File | Symbol | Loại phát hiện | Runtime/Test/Doc | Quyết định |
|---|---|---|---|---|---|
| Test | `backend/tests/test_qdrant_schema.py` | `FakeClient`, `fake_constructor`, `fake_get_client` | fake Qdrant client | test | Giữ - offline deterministic |
| Test | `backend/tests/test_api_chat.py` | `FakeDenseRetriever`, `FakeReranker`, `FakeGenerator`, fake stack | fakes qua DI | test | Giữ - offline deterministic |
| Test | `backend/tests/test_llm_generator_openai.py` | `fake_runner_factory`, `SimpleNamespace` results | fake runner | test | Giữ - offline deterministic |
| Test | `backend/tests/test_ingestion_pipeline.py`, `test_hybrid_index.py`, `test_markdown_chunker.py` | example chunk fixtures, image URL mẫu | sample data | test | Giữ - sample data chỉ trong unit test |
| Runtime | `backend/llm/generator_openai.py` | `_usage_tokens` | đọc sai attribute SDK 0.19.4 -> log luôn `tokens=unknown` | production | **Đã sửa** + 3 tests + live verify |
| Runtime | `backend/llm/generator_openai.py` | `runner` injectable, `configured` | DI cho unit tests; production không inject runner, `configured` = key presence | production | Giữ - đúng contract fail closed |
| Runtime | `backend/core/startup.py`, `backend/ingestion/pipeline.py`, `backend/api/app.py` | `client`/`embedder`/`reranker`/`generator`/`stack` injectable | DI cho unit tests; production build dependencies thật | production | Giữ - đúng contract |
| Runtime | `backend/reranking/reranker.py` | `ScorerReranker` | wrapper thật quanh injected scorer; production dùng `CrossEncoderReranker` (MiniLM thật cache-only) | production | Giữ - không phải fake |
| Runtime | `backend/reranking/models/cross_encoder.py` | `_get_cross_encoder(local_files_only=True)` | model thật từ cache; thiếu cache fail rõ | production | Giữ |
| Runtime | `backend/embedding/embedder.py`, `backend/embedding/openrouter_embedder.py` | `SentenceTransformerEmbedder`, `OpenRouterEmbedder` | embedder thật; OpenRouter raise khi lỗi, không fallback local | production | Giữ |
| Runtime | `backend/retrieval/dense_retriever.py`, `hybrid_retriever.py`, `backend/scoring/bm25.py` | query path | Qdrant thật + E5 thật + BM25 thật | production | Giữ |
| Runtime | `backend/vectorstore/*` | `ensure_collection`, `reset_collection`, `upsert_points` | guard an toàn destructive actions, không phải fake-mode guard | production | Giữ |
| Runtime | `backend/api/health.py`, `backend/api/routes/chat.py` | degraded/fail-closed mapping | thiếu dependency -> typed 503/502/504, không fake response | production | Giữ |
| Runtime | `backend/ingestion/*`, `backend/core/*` | toàn bộ | không tìm thấy fake/mock/sample vector/guard | production | Giữ |
| Script | `backend/scripts/convert_huegov_*_to_md.py` | conversion scripts | chuyển đổi dữ liệu thật, không fake | script | Giữ |
| Script | `knowledge-base-hue/foods/evaluation/validate_tests.py` | validator | validation thật trên KB | script | Giữ |
| Doc | `backend/config/README_config.md` | toàn bộ | mô tả đúng runtime thật, không có nội dung "chạy fake mặc định" | doc | Giữ - không cần sửa |
| Doc | `backend/config/settings.yaml`, `logging.yaml` | comments | mô tả đúng provider/limit; không có fake-mode claim | doc | Giữ |
| Data | `backend/data/**` | raw HueGov dumps | dữ liệu nguồn, không phải code/tài liệu runtime | data | Ngoài scope |

Kết luận: **không có fake/fallback/guard sai contract trên production path**.
Toàn bộ fake/mock tập trung trong `backend/tests/**` (đúng quy định giữ
nguyên) và phục vụ offline determinism. Đúng một finding runtime cần sửa:
`_usage_tokens` log `tokens=unknown` thay vì token thật.

## Files Changed

- `backend/llm/generator_openai.py` - `_usage_tokens` đọc usage từ
  `result.raw_responses[].usage` (SDK 0.19.4 không expose `RunResult.usage`);
  chỉ format khi cả `input_tokens` và `output_tokens` đều không phải `None`;
  entry partial bị bỏ qua và không có entry hoàn chỉnh thì trả `unknown`
  (không fabricate).
- `backend/tests/test_llm_generator_openai.py` - thêm class `TestUsageTokens`
  (5 tests offline): đọc từ raw_responses, first-with-usage wins, unknown khi
  thiếu usage, partial entry bị skip, partial entry trước complete entry.

## Correction After Codex Review (2026-08-13)

Codex review `reports/runtime_fake_audit_codex_review.md` ghi một minor
finding: `_usage_tokens` coi usage object thiếu một token field là valid và
trả chuỗi như `None/None` thay vì `unknown` theo contract report.

Sửa:

- Chỉ format `input_tokens/output_tokens` khi cả hai field đều khác `None`.
- Usage entry thiếu một trong hai field bị bỏ qua, tiếp tục duyệt entry kế
  tiếp.
- Không có entry hoàn chỉnh -> trả `unknown`.

Tests bổ sung (offline, deterministic):

- `test_partial_usage_entry_is_skipped`: usage chỉ có `input_tokens` ->
  `"unknown"`.
- `test_partial_entry_before_complete_entry`: entry partial đứng trước entry
  complete -> trả token của entry complete.

Verification thực tế (không gọi OpenAI theo yêu cầu Codex):

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "
from types import SimpleNamespace
from llm.generator_openai import _usage_tokens
# probe Codex: usage object thiếu fields
print(_usage_tokens(SimpleNamespace(raw_responses=[SimpleNamespace(usage=SimpleNamespace())])))
# -> 'unknown' (trước sửa là 'None/None')
"
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/test_llm_generator_openai.py -q --tb=short
# -> 28 passed (26 cũ + 2 mới)
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q --tb=short
# -> 274 passed, 1 StarletteDeprecationWarning
git diff --check
# -> clean
```

Không có live OpenAI call, không sửa notebook/guides/Project_Status/Codex
review/user report, không commit/push trong correction này.

## Fakes/Mocks Giữ Lại Trong Tests Và Lý Do

- `FakeClient` (test_qdrant_schema.py), fake stack/generator/reranker
  (test_api_chat.py), `fake_runner_factory` (test_llm_generator_openai.py) và
  sample chunk fixtures: test phải offline, deterministic, không cần Qdrant
  thật, model hoặc OpenAI; DI là cơ chế đã phê duyệt để inject chúng. Không
  fake nào nằm trên production path.

## Runtime Fake/Fallback Đã Xóa/Sửa

- `_usage_tokens`: trước đọc sai attribute và luôn trả `unknown` - đây là
  runtime path báo cáo dữ liệu không thật. Đã sửa để log token counts thật từ
  provider. Không có fake fallback nào khác để xóa.

## Live Checks Đã Chạy

- Full offline suite: `UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest
  tests/ -q --tb=short` -> **274 passed** (269 cũ + 5 mới sau correction
  Codex), 1 StarletteDeprecationWarning.
- Live probe `_usage_tokens` (1 OpenAI call, user-approved): log thật
  `answer generated model=gpt-5.4-nano outcome=success latency_ms=5440
  source_count=1 tokens=421/48`; chi phí khoảng 0,00014 USD.
- Không cần chạy lại Qdrant/E5/MiniLM validation vì sửa đổi không chạm
  retrieval/embedding/vectorstore paths (đã được xác minh thật trong cùng
  session ở các task trước và covered bởi tests).
- `git diff --check` sạch; CodeGraph đã sync và index up to date sau khi sửa
  runtime.

Tổng OpenAI calls của task audit này: 1. Chi phí: khoảng 0,00014 USD (421
input + 48 output tokens, giá official 0,20/1M input + 1,25/1M output).
Ngân sách 3 USD còn dư rất nhiều.

## Validation Pass/Fail

| Check | Kết quả |
|---|---|
| `rg` + đọc toàn bộ production `backend/**/*.py` (47 files) | pass - không fake/guard/fallback |
| Tests fake/mock classification | pass - toàn bộ nằm trong `tests/`, giữ nguyên |
| Full offline pytest | pass - 274 tests (sau correction Codex) |
| Live token logging sau fix | pass - `tokens=421/48` (trước là `unknown`) |
| `git diff --check` | pass - clean |
| `codegraph status .` sau sync | pass - up to date |
| Notebooks, guides, Project_Status, Codex review, user reports | không đụng - đúng scope |

## Blockers / Limitations

- Không có blocker. `StarletteDeprecationWarning` (httpx/TestClient) vẫn là
  warning ecosystem đã biết, không thuộc scope audit.
- `usage` chỉ có trên `raw_responses` khi provider trả về; một số failure path
  (timeout/exception) vẫn không có usage - log giữ `unknown` đúng sự thật,
  không ước lượng trong runtime.

## Live Access / Secrets Statement

Đã chạy 1 live OpenAI call (model `gpt-5.4-nano`, user-approved, không retry).
Không đọc hoặc in giá trị `OPENAI_API_KEY`; key lấy từ environment qua SDK.
Không gọi OpenRouter. Không collection mutation. Model load không diễn ra
trong probe này (không dùng embedder); mọi thao tác Qdrant/E5/MiniLM trong
session đều read-only và cache-only.

## Handoff To Codex

1. Review `_usage_tokens` fix và 3 tests mới; xác nhận không ảnh hưởng failure
   paths (usage None -> "unknown").
2. Xác nhận audit table: toàn bộ fake/mock chỉ trong `tests/`; không có
   production fake fallback; DI không bị dùng làm fallback production.
3. Lưu ý governance: contract notebook runtime-real (task trước) và audit này
   cùng củng cố nguyên tắc "runtime thật, test offline" - có thể cần Codex/user
   cập nhật Notebook Rules trong governance docs.
