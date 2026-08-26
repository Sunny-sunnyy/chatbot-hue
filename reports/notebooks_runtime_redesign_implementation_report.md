# Implementation Report: Notebooks Runtime-Redesign (01-06)

Implementer: DeepSeek
Date: 2026-08-13
Report path:

```text
reports/notebooks_runtime_redesign_implementation_report.md
```

Phase guide context:

```text
guides/phase_0_mvp_foundation.md
guides/phase_1_backend_skeleton.md ... guides/phase_6_generation_api.md
session_prompt/IMPLEMENTER_WORKFLOW.md
session_prompt/Project_Status.md
reports/phase_6_generation_api_implementation_report.md
```

## Approved Scope

Người dùng phê duyệt thiết kế lại toàn bộ sáu notebook canonical trong
`notebooks/` để Run All chạy runtime thật và trả kết quả thật: loại bỏ fake,
mock, sample vector giả, fake runner, fake Qdrant client và opt-in real-mode
guard.

Phê duyệt kèm theo:

- Qdrant Docker đang chạy, collection `hue_foods_e5_small_384` với 572 points.
- Local E5 và MiniLM đã cache; không download mới (`HF_HUB_OFFLINE=1`).
- Live OpenAI `gpt-5.4-nano` được phép; tổng ngân sách mới tối đa 3 USD.
- Không gọi OpenRouter; không reset/delete/recreate collection, không reindex,
  không đổi `settings.yaml`; không implement Phase 7 hoặc Phase 8.
- Không sửa runtime backend (không có blocker thực tế phát sinh).
- Không sửa Project_Status.md, guides, Codex review, user reports; không
  commit/push.

Đây là thay đổi hợp đồng notebook do chính người dùng chỉ định: notebook chạy
runtime thật khi Run All thay vì safe-default + opt-in guard như các guide
Phase 1-6 đang mô tả. Guides và Notebook Rules hiện hành chưa phản ánh thay đổi
này (ngoài scope Implementer); xem mục Deviations.

## Summary

Sáu notebooks được chuẩn hóa lại quanh một nguyên tắc: mỗi notebook import
backend modules, không duplicate pipeline logic, Run All chạy đúng runtime thật
và fail rõ ràng khi thiếu prerequisite (key, Qdrant, model cache) - không
fallback fake.

- `01`, `02`: giữ nguyên nội dung runtime thật hiện có; làm sạch outputs và đặt
  mọi `execution_count = null`.
- `03`: bỏ `FakeEmbedder` và fake demo; Run All chunk 572 curated foods thật,
  load E5 từ cache (`HF_HUB_OFFLINE=1`), embed thật 572 chunks, fit TF-IDF thật.
- `04`: bỏ fake dense vectors và sample point giả; read-only inspect collection
  thật, kiểm tra schema/count/payload projection; không có cell mutation.
- `05`: bỏ `FakeEmbedder`, `FakeClient`, fake payloads, fake scorer, fake
  reranker; demo ba profiles bằng deep copy settings trong memory, build stack
  thật với Qdrant/E5/MiniLM thật, chạy cùng một câu hỏi qua cả ba profiles.
- `06`: bỏ fake generator/runner/stack, timeout demo, manual `json.dumps`
  evidence demo và guard `HUE_RAG_PHASE6_REAL`; Run All gọi đúng 1 `POST
  /api/chat` qua app thật/lifespan thật với generator OpenAI thật.

## Files Modified

- `notebooks/01_backend_foundation.ipynb` - giữ runtime thật; strip outputs,
  execution counts null.
- `notebooks/02_foods_data_and_chunking.ipynb` - giữ runtime thật; strip
  outputs, execution counts null.
- `notebooks/03_embedding_models.ipynb` - viết lại: real E5 cache-only + real
  TF-IDF trên 572 chunks, safe summary (chunk count, model ID, dimension,
  normalized check, query dim, latency).
- `notebooks/04_qdrant_ingestion.ipynb` - viết lại: read-only real inspection
  (name, dense 384 cosine, sparse index, exact count 572, approved payload
  projection); fail rõ khi lệch.
- `notebooks/05_retrieval_profiles.ipynb` - viết lại: ba profiles thật qua
  deep-copy settings, cùng câu hỏi, safe summary per profile, typed-error
  checks; không benchmark/winner claim.
- `notebooks/06_generation_and_api.ipynb` - viết lại: một biến `question`,
  key-presence check fail actionable, `TestClient` với app thật, `/health` +
  đúng 1 `POST /api/chat`, in safe fields, không retry.

## Fake/Guard Removed

| Notebook | Đã xóa |
|---|---|
| 03 | class `FakeEmbedder` + demo vector giả; markdown "safe default mode"; guard `HUE_RAG_LOCAL_E5` |
| 04 | cell "Build sample point" với `fake_dense` vectors; guard `HUE_RAG_QDRANT_REAL` |
| 05 | `FakeEmbedder`, `make_payloads` (572 fake payloads), `FakeClient`, `fake_scorer`, `ScorerReranker` fake, guard `HUE_RAG_QDRANT_REAL` |
| 06 | `fake_runner`, `slow_runner` timeout demo, fake stack/retriever, manual evidence `json.dumps` demo, guard `HUE_RAG_PHASE6_REAL` |
| 01, 02 | không có fake/guard từ trước; giữ nguyên |

## Commands Run

```bash
# Build notebooks 03-06 và clean 01-02
UV_CACHE_DIR=/tmp/uv-cache uv run python /tmp/build_notebooks.py
UV_CACHE_DIR=/tmp/uv-cache uv run python /tmp/clean_notebooks_01_02.py

# Static validation
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "nbformat.validate all 6"  # pass
git diff --check                                                    # clean
codegraph status .                                                  # up to date

# Real execution (output copies ngoài repo /tmp/exec_*.ipynb)
UV_CACHE_DIR=/tmp/uv-cache uv run jupyter nbconvert --to notebook --execute \
  notebooks/01_backend_foundation.ipynb --output /tmp/exec_01.ipynb
UV_CACHE_DIR=/tmp/uv-cache uv run jupyter nbconvert --to notebook --execute \
  notebooks/02_foods_data_and_chunking.ipynb --output /tmp/exec_02.ipynb
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run jupyter nbconvert --to notebook --execute \
  notebooks/03_embedding_models.ipynb --output /tmp/exec_03.ipynb
UV_CACHE_DIR=/tmp/uv-cache uv run jupyter nbconvert --to notebook --execute \
  notebooks/04_qdrant_ingestion.ipynb --output /tmp/exec_04.ipynb
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run jupyter nbconvert --to notebook --execute \
  notebooks/05_retrieval_profiles.ipynb --output /tmp/exec_05.ipynb
# 06: OPENAI_API_KEY từ .env được export vào environment, không in giá trị
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run jupyter nbconvert --to notebook --execute \
  notebooks/06_generation_and_api.ipynb --output /tmp/exec_06.ipynb
# -> cả sáu notebook 0 cell errors
```

## Tests And Verification

- `nbformat.validate` pass cho cả 6 notebooks; cell IDs unique; mọi code cell có
  outputs rỗng và `execution_count = null` trong repo.
- Grep source cells: không còn từ khóa `FakeEmbedder`, `FakeClient`,
  `fake_scorer`, `fake_runner`, `fake payloads`, `HUE_RAG_*` guard, `default
  mode`, `real mode`, `opt-in` trong cả 6 notebooks.
- `git diff --check` sạch; CodeGraph index up to date.
- Không sửa backend runtime, settings, guides, Project_Status, Codex review,
  user reports. Không commit/push.

## Live Evidence (mỗi notebook đã chạy thật, 0 cell errors)

| Notebook | Runtime thật | Kết quả quan sát |
|---|---|---|
| 01 | config, logging, schema local | 10 packages; 3 profiles resolve đúng; log file tạo + tự xóa; `RetrievedDocument` khởi tạo ok |
| 02 | chunking local | 91 files -> 572 chunks (restaurants 249, cafes 162, local_specialties 118, guide 43); trung bình 272.8 ký tự; 0 đoạn thường vượt 400; 8 bảng vượt 400 |
| 03 | E5 cache-only + TF-IDF thật | 572 vectors 384 chiều, all finite, norm min/mean/max = 1.0; query vector 384 chiều norm 1.0; latency 36.1s; vocabulary 2093, deterministic qua refit |
| 04 | Qdrant read-only thật | collection `hue_foods_e5_small_384` status green; dense 384 Cosine; sparse index enabled; exact count 572; 2 payload mẫu chỉ in approved metadata + text length |
| 05 | Qdrant + E5 + MiniLM thật, 3 profiles | dense_only: 10 docs, chỉ `dense_score`; hybrid_no_rerank: 10 docs, `hybrid_score` + normalized fields; hybrid_rerank: 5 docs, `rerank_score` + `reranker_model`; context 5 sources, 2859-2903 ký tự; cùng câu hỏi cho cả ba |
| 06 | app thật + 1 OpenAI call thật | key present: True; `/health` 200 `ok` (qdrant/retrieval ready, generator configured); `/api/chat` 200 trong 13.6s; answer tiếng Việt grounded; 3 sources hợp lệ; retrieval_debug: `dense_only`, E5, 10 retrieved, 5 context sources |

Tổng live OpenAI calls trong đợt notebook validation này: 1 (notebook 06).
Chi phí: API response không chứa token usage (SDK 0.19.4 không expose usage qua
response - minor finding đã biết từ smoke), nên chi phí được tính theo
worst-case charge 0,00178 USD (2500 input + 1024 output tokens). Thực tế
khoảng 0,0005-0,001 USD. Nằm xa dưới ngân sách 3 USD.

## Deviations From Approved Guide

- Contract notebook cũ trong guides Phase 1-6 và Notebook Rules (Session_Prompt)
  yêu cầu safe-default + opt-in real-mode guards; thiết kế mới do người dùng chỉ
  định thay thế contract này: Run All chạy runtime thật. Guides và
  Session_Prompt chưa được cập nhật vì ngoài scope Implementer - Codex/user cần
  quyết định cập nhật governance docs riêng.
- Notebook 06 dùng `TestClient` (in-process) thay vì uvicorn server: vẫn là app
  thật và lifespan thật, đúng full runtime path qua `POST /api/chat`.
- Notebook 03/05 đặt `HF_HUB_OFFLINE=1` ngay trong notebook để đảm bảo cache-
  only; đây là thiết lập môi trường nội bộ notebook, không sửa runtime.
- Không có deviation nào khác.

## Known Issues

- Severity: low. `StarletteDeprecationWarning` về `httpx`/`starlette.testclient`
  xuất hiện trong output notebook 06 - là warning của ecosystem (đã được Codex
  ghi nhận ở review Phase 6 trước), không ảnh hưởng hành vi.
- Severity: low. Hugging Face Hub in cảnh báo "unauthenticated requests" khi
  load model từ cache - vô hại với `HF_HUB_OFFLINE=1`.
- Severity: low. Notebook 03 mất khoảng 36 giây để embed 572 chunks trên CPU
  khi chạy lần đầu; đã ghi trong markdown.
- Severity: low. Notebooks 04/05/06 fail rõ ràng khi Qdrant tắt, thiếu model
  cache hoặc thiếu `OPENAI_API_KEY` - đây là hành vi mong muốn, không phải lỗi.
- Severity: low. Không có usage tokens trong response `/api/chat` nên chi phí
  notebook 06 chỉ ước lượng được; runtime fix `_usage_tokens` là minor finding
  riêng đã ghi trong Phase 6 implementation report, ngoài scope task này.

## Security, Data Safety, Reliability, Performance Self-Check

- Security: notebook 06 chỉ kiểm tra presence `OPENAI_API_KEY`
  (`bool(os.environ.get(...))`), không đọc `.env`, không dùng `load_dotenv`,
  không in giá trị key; không in prompt, raw SDK response, header hoặc
  chain-of-thought.
- Data safety: notebook 04 chỉ đọc Qdrant (không có cell upsert/reset/delete);
  không reindex, không đổi settings; payload chỉ in approved metadata fields.
- Reliability: mọi prerequisite thiếu đều fail actionable (RuntimeError với
  hướng dẫn), không silent fallback; không retry trong notebook 06.
- Performance: mỗi notebook load model một lần mỗi process; 03/05 dùng
  `HF_HUB_OFFLINE=1`; context luôn bounded bởi runtime; notebook 06 đúng 1 paid
  call mỗi Run All.
- Tests: default verification không cần secrets ngoài notebook 06 (đúng 1 call
  đã được user phê duyệt); notebooks 01-05 không tốn phí.
- Notebooks: JSON hợp lệ, cell IDs unique, outputs rỗng, execution counts null,
  không chứa private absolute path trong markdown committed, import runtime
  modules, không duplicate pipeline logic.

## Live Access / Secrets Statement

Đã chạy 1 live OpenAI call (notebook 06 qua `/api/chat`, model `gpt-5.4-nano`,
được user phê duyệt trong ngân sách 3 USD). Không gọi OpenRouter. Không đọc
hoặc in giá trị `OPENAI_API_KEY`; chỉ kiểm tra presence. Không có web access,
deploy, dependency install hoặc collection mutation. Model load chỉ từ local
cache với `HF_HUB_OFFLINE=1`.

## Handoff To Codex

Codex nên review trước tiên:

1. Notebook 06: đúng 1 paid call qua app thật/lifespan thật; key-presence check
   fail actionable; in safe fields đúng allowlist; không retry.
2. Notebook 05: ba profiles build stack thật (không injected client/embedder);
   deep-copy settings không làm rò config file; score fields đúng stage.
3. Notebook 04: chỉ read-only (collection_exists/get_collection/count/scroll);
   không có cell mutation nào.
4. Notebook 03: `HF_HUB_OFFLINE=1` đặt trước khi load model; kiểm tra
   normalized/finite/dimension thật.
5. Notebooks 01-02: nội dung giữ nguyên runtime thật; chỉ strip outputs.
6. Governance: guides Phase 1-6 và Notebook Rules mô tả safe-default + opt-in
   guards - đã lỗi thời so với thiết kế runtime-real mà user vừa phê duyệt.
   Cần Codex/user quyết định cập nhật governance docs (ngoài scope Implementer).

Safe-default steps để Codex/user tự xác minh lại (không tốn phí cho 01-05):

```bash
cd /home/minhhieu/hue_rag
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "import nbformat; [nbformat.validate(nbformat.read(p, as_version=4)) for p in __import__('glob').glob('notebooks/*.ipynb')]"
# 01: uv run jupyter nbconvert --to notebook --execute notebooks/01_backend_foundation.ipynb --output /tmp/nb01.ipynb
# 02: tuong tu notebooks/02_foods_data_and_chunking.ipynb
# 03: HF_HUB_OFFLINE=1 ... notebooks/03_embedding_models.ipynb
# 04: ... notebooks/04_qdrant_ingestion.ipynb (can Qdrant chay)
# 05: HF_HUB_OFFLINE=1 ... notebooks/05_retrieval_profiles.ipynb
# 06: export OPENAI_API_KEY truoc khi chay (1 paid call, duoi 0,002 USD)
```
