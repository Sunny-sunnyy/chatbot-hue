# Implementation Report: Phase 7A2 Gate 2 — Build 2 index và cutover runtime

Implementer: Claude Opus 5.5
Date: 2026-10-24
Canonical inputs:

```text
docs/superpowers/specs/2026-10-23-phase-7a2-corpus-correction-reindex-design.md (§5, §8, §9)
docs/superpowers/plans/2026-10-23-phase-7a2-corpus-correction-reindex-implementation-plan.md (Global Constraints, Task 4–8, Review Contract)
session_prompt/CURRENT_HANDOFF.md (implementation, base 5e8aff1)
```

Report không chép nội dung corpus, câu hỏi Golden, vector hay payload. Bảng
retrieval smoke chỉ ghi số dòng smoke, category và số đếm.

## 1. Phạm vi

Gate 2 gồm plan Task 4–8:

- Task 4: build record là nguồn sự thật duy nhất; bỏ hằng số cứng
  corpus/chunk/sparse/vocab, preflight Phase 4 và nhánh migration.
- Task 5: còn đúng hai candidate (`e5-small-384`, `qwen3-embedding-8b-4096`),
  thêm `OpenRouterDenseRunner`, xóa module/test metadata v2 và spec model cũ.
- Task 6: một đường build thẳng (`build --candidate <id>`).
- Task 7: build thật hai collection `hue_full_corpus_7a2_e5_small_384` và
  `hue_full_corpus_7a2_qwen3_8b_4096`, verify thật.
- Task 8: health runtime, live smoke Phase 6 (5 call `gpt-6-luna`), retrieval
  smoke 10 trên cả hai index, focused suite.

Không đổi chunker, payload, retrieval profile, reranker, context hay generation.
Không đụng collection Foods hay 13 collection cũ (chỉ đọc một collection cũ cho
probe root cause, mục 4.6). Không commit.

Ba điểm phạm vi Task 5 được Reviewer chốt qua tin nhắn ngày 2026-10-24 (trong
phạm vi spec):

1. Preflight Phase 3 (`backend/evaluation/full_corpus_embedding_preflight.py`)
   và test của nó: **xóa** (phương án A). Notebook 03 chỉ bỏ cell gọi
   `run_preflight` và cell đọc evidence.
2. Notebook 04, 06, 08b: không sửa trong Gate 2, ghi thành giới hạn (mục 5).
3. Chuỗi `e5-base-768` trong code benchmark Foods: không sửa, là ngoại lệ có chủ
   đích của grep Step 6 (mục 4.7).

Sub-agent: không dùng.

## 2. Thay đổi chính

| File | Thay đổi |
|---|---|
| `backend/embedding/full_corpus.py` | `DenseModelSpec` thêm `provider` (`local`/`openrouter`); `revision/device/dtype` được `None` cho model API. `DENSE_MODEL_SPECS` còn 2 spec. Thêm `parse_embeddings_response`, `OpenRouterDenseRunner` (batch 64, `encoding_format: float`, `provider.data_collection: deny`, không `dimensions`, không pin, không retry/fallback/resume; lỗi HTTP/thiếu `data`/sai index/sai chiều đều raise) và `create_dense_runner` dùng chung cho build và runtime. Bỏ nhánh `pyvi` và các helper chỉ preflight/build cũ dùng (`count_tokens`, `tokenizer`, `embed_documents`, `runtime_identity`, `observed_runtime_state`). |
| `backend/ingestion/source_state.py` | Một hàm `make_full_corpus_build_record` (schema `full_corpus_build:v3`): `file_count = len(sources)`, `chunk_count` truyền vào, `dense.providers`, `qdrant.payload_schema_version`. Xóa hằng số 205/8460/5662 và `make_full_corpus_metadata_v2_build_record`. |
| `backend/ingestion/full_corpus_pipeline.py` | Hai candidate, `FullCorpusCandidate` chỉ còn `collection_name`. `prepare_full_corpus_input()` = discover → hash → chunk → identity → `fit_sparse_state`. `build_candidate` là đường build duy nhất (8 bước plan Task 6). Sparse state dùng chung `data/full_corpus_builds/full_corpus_sparse_state.json`. Xóa preflight Phase 4, artifact path, resource evidence. CLI chỉ còn `build`. |
| `backend/retrieval/full_corpus.py` | `validate_full_corpus_build_record(record, candidate, current_sources)`: kiểm status/representation/schema/collection/Qdrant/dense/sparse schema + freshness, `point_count == corpus.chunk_count`; không còn migration/lineage. Runtime kiểm SHA sparse state theo `record.sparse.state_sha256`, identity theo `record.corpus.identity`, `points_count` theo `record.corpus.chunk_count`; runner qua `create_dense_runner`. |
| `backend/vectorstore/qdrant.py` | `expected_full_corpus_schema` cho phép chiều `{384, 4096}` (trước `{384, 768, 1024}`). |
| `backend/llm/phase6_live_smoke.py` | Token checker Representation B dùng `get_default_tokenizer_checker()` của chunker (3 tokenizer local trong `full_corpus.embedding_models`); point count đọc collection của candidate runtime thay tên cứng metadata v2. 5 case và logic chấm không đổi. |
| Xóa | `backend/ingestion/full_corpus_metadata_v2.py`, `backend/tests/test_full_corpus_metadata_v2.py`, `backend/evaluation/full_corpus_embedding_preflight.py`, `backend/tests/test_full_corpus_embedding_preflight.py`. |
| Tests | `test_full_corpus_embedding.py` (2 spec, test thuần parser OpenRouter), `test_full_corpus_qdrant_ingestion.py` (record không hằng số, registry 2 candidate, schema 4096), `test_full_corpus_retrieval.py` (record dựng bằng `make_full_corpus_build_record`; test thuần freshness; bỏ case migration; số candidate 2). |
| `notebooks/03_embedding_models.ipynb` | Bỏ import preflight, cell `run_preflight` và cell evidence (kèm markdown); dòng in spec đổi từ `revision[:8]` sang `provider`. Outputs rỗng, `execution_count` null. |
| `pyproject.toml`, `uv.lock` | `uv add httpx` (khai báo trực tiếp, `httpx>=0.28.1`). |

Sai lệch so với plan (Reviewer đã chấp nhận ngày 2026-10-24):

- **D1:** `backend/vectorstore/qdrant.py` không có trong mục Files của plan
  nhưng phải đổi tập chiều hợp lệ sang `{384, 4096}`, nếu không không tạo được
  collection 8B.
- **D2:** `verify_full_corpus_collection` cần `sample_chunk_ids` mà trước lấy từ
  evidence Phase 3 (12 ID). Đường build mới chọn tất định **chunk đầu tiên của
  mỗi domain theo thứ tự chunker** (5 ID); build summary ghi `sample_rule` và
  `sample_chunk_count`.

Sai lệch nhỏ khác:

- Plan Task 5 Step 1–2 yêu cầu viết test parser trước và quan sát FAIL. Tôi viết
  code runner trước rồi mới viết test, nên **không quan sát RED**; test chạy
  PASS sau đó.
- Lệnh build/verify được chạy với `HF_HUB_OFFLINE=1` (chunker và e5 nạp từ HF
  cache, như rủi ro 5 của handoff); plan Task 7 không ghi biến này.
- `git rm` lỡ stage 4 file xóa vào index; tôi đã `git restore --staged` ngay
  cho đúng 4 path đó. Index hiện không có gì staged (Git authorization `none`).

## 3. Cách đã chạy thật

Từ repo root, Qdrant `127.0.0.1:6335`:

```bash
# Task 4 Step 5
cd backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_full_corpus_retrieval.py tests/test_full_corpus_qdrant_ingestion.py -q
# Task 5 Step 6
grep -rn "metadata_v2_collection_name\|full_corpus_metadata_v2\|hue_full_corpus_a_\|e5-base-768\|huydang-dek21-768\|qwen3-embedding-0.6b" backend
# Task 7 Step 1–2
HF_HUB_OFFLINE=1 uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline build --candidate e5-small-384
HF_HUB_OFFLINE=1 uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline build --candidate qwen3-embedding-8b-4096
# Task 7 Step 3 (script tạm ngoài repo)
HF_HUB_OFFLINE=1 PYTHONPATH=. uv run --env-file .env python /tmp/phase7a2_gate2/verify_collections.py <candidate>
# Task 8 Step 2
cd backend && uv run --env-file ../.env uvicorn api.app:app --host 127.0.0.1 --port 8016
curl -s http://127.0.0.1:8016/health
# Task 8 Step 3
HF_HUB_OFFLINE=1 uv run --env-file .env python -m backend.llm.phase6_live_smoke \
  --cases data/full_corpus_phase_6_live_cases.json \
  --output data/full_corpus_phase_7a2_live_smoke.json --confirm-paid
# Task 8 Step 4 (script tạm ngoài repo)
HF_HUB_OFFLINE=1 PYTHONPATH=. uv run --env-file .env python /tmp/phase7a2_gate2/retrieval_smoke.py <candidate> <output>
# Task 8 Step 5
cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m pytest tests/test_full_corpus_retrieval.py tests/test_full_corpus_qdrant_ingestion.py tests/test_full_corpus_embedding.py tests/test_phase6_live_smoke.py tests/test_phase6_settings.py tests/test_golden_full_corpus.py -q
cd .. && git diff --check
```

Notebook 03 được chạy thật trên bản output tạm (`jupyter nbconvert --execute
... --output-dir /tmp/nb03_run`); file trong repo giữ outputs rỗng.

Artifact private (không tracked): build summary/log, verify, retrieval smoke ở
`/tmp/phase7a2_gate2/`; live smoke `data/full_corpus_phase_7a2_live_smoke.json`;
build record `data/full_corpus_builds/hue_full_corpus_7a2_*.json`; sparse state
`data/full_corpus_builds/full_corpus_sparse_state.json`.

## 4. Kết quả quan sát

### 4.1 Code và test

- Task 4 Step 5 (`test_full_corpus_retrieval.py` + `test_full_corpus_qdrant_ingestion.py`):
  **40 passed**.
- Task 5 Step 7, chạy lúc collection 7a2 **chưa** được build: 83 passed, 4
  failed. 4 test fail đều trong `test_phase6_live_smoke.py`, cần runtime thật
  (một test thấy `early_exit_reason = before_count_failed` vì collection chưa
  tồn tại). Sau Task 7, chạy lại trong suite Task 8 Step 5 thì PASS (mục 4.5).
- Task 8 Step 5 (6 file test, sau khi build xong): **95 passed in 22.07s**.
  `git diff --check`: exit 0. Không test nào gọi provider trả phí (test ASGI
  integration đặt `generator_ready=False` trước khi gọi `/api/chat`).

### 4.2 Build

| | e5-small-384 | qwen3-embedding-8b-4096 |
|---|---|---|
| Lần build | 1 (local, exit 0) | **1/2** (OpenRouter, exit 0, không lỗi) |
| Collection | `hue_full_corpus_7a2_e5_small_384` | `hue_full_corpus_7a2_qwen3_8b_4096` |
| File / chunk | 205 / 8.459 | 205 / 8.459 |
| Matrix | 8.459 × 384 | 8.459 × 4096 |
| Norm min / max | 0,99999989 / 1,00000014 | 0,99999989 / 1,00000014 |
| Verify trong build | 8.459 point, 8.459 payload khớp, 5 mẫu vector | 8.459 point, 8.459 payload khớp, 5 mẫu vector |
| Request OpenRouter | 0 | 133 (batch 64), tất cả HTTP 200 |
| Provider phục vụ (record) | `[]` | `DeepInfra`, `Nebius`, `SiliconFlow` |
| Record SHA-256 | `03829ed6…606c` | `ea4672c1…2208` |

Hai build dùng chung corpus identity `5869d3cc…716f` và sparse state SHA
`dbd5f7bc…aa7` (vocabulary 5.660, trước là 5.662). Build record thật có đúng
các field của `make_full_corpus_build_record` (schema `full_corpus_build:v3`,
`point_count = chunk_count = 8459`).

### 4.3 Verify thật từng collection (Task 7 Step 3)

| | e5-small-384 | qwen3-8b-4096 |
|---|---|---|
| `points_count` / count exact / scroll | 8.459 / 8.459 / 8.459 | 8.459 / 8.459 / 8.459 |
| = `corpus.chunk_count` trong record | có | có |
| Payload không đúng 7 field | 0 | 0 |
| Dense sai chiều (config 384 / 4096) | 0 | 0 |
| Thiếu hoặc rỗng sparse | 0 | 0 |
| Mẫu embed lại | 20 (4/domain × 5 domain) | 20 (1 request, Nebius phục vụ) |
| cos min / mean | 0,9999999999998 / 0,9999999999999 | **0,99535 / 0,99826** |
| Đạt ≥ 0,999 | **có** | **không** |

**8B không đạt acceptance spec §5.5 mục 2 (cos ≥ 0,999).** Chẩn đoán bằng 1
request thêm (cùng 20 chunk, Nebius phục vụ), ghép mỗi mẫu với batch build chứa
nó:

| Nhóm | Số mẫu | cos | Batch build |
|---|---:|---|---|
| Khớp | 10 | 0,99987–0,99993 | 5, 9, 14, 18, 25, 31, 44, 51, 57, 94 |
| Lệch | 10 | 0,99534–0,99736 | 1, 38, 63, 69, 72, 75, 78, 81, 107, 120 |

Phân bố tách hẳn thành hai nhóm. Nhóm khớp nằm đúng khoảng survey đo được giữa
batch/provider (≥ 0,99985). Nhóm lệch thấp hơn rõ. Root cause (suy ra từ
evidence, chưa chứng minh từng batch): build không pin provider nên OpenRouter
chia 133 batch cho 3 provider. Một provider cho vector khác Nebius tới cos ≈
0,996, nhiều khả năng là DeepInfra vì survey chưa đo được DeepInfra lần nào
(429), còn SiliconFlow fp8 so với Nebius đã đo ≥ 0,99985. Không xác định được
provider của từng batch: runner chỉ ghi tập `providers_seen` theo plan, không
ghi provider theo batch.

Hệ quả: index 8B trộn vector từ ba provider; query runtime 8B cũng không pin
nên có thể được một provider khác phục vụ. Retrieval smoke 8B vẫn chạy (mục
4.5), nhưng chất lượng so sánh ở Phase 7B/8 có thể bị ảnh hưởng bởi độ lệch
này. e5-small (runtime mặc định) không bị ảnh hưởng.

### 4.4 Runtime và live smoke (Task 8 Step 2–3)

- Health (uvicorn `127.0.0.1:8016`, candidate `e5-small-384` → collection mới):
  **HTTP 200**, `{"status":"ok","components":{"app":"alive","qdrant":"ready","retrieval":"ready","tokenizer":"ready","generator":"ready"}}`.
  Retrieval đã qua kiểm freshness theo build record. Server đã dừng sau khi đo.
- Live smoke, một invocation, **đúng 5 call `gpt-6-luna`**, artifact
  `data/full_corpus_phase_7a2_live_smoke.json`; Qdrant before/after 8.459/8.459,
  `exact_five_attempts = true`, `point_count_intact = true`. Runner exit 1 và
  `status = FAIL` vì runner chỉ PASS khi đủ 5/5, giống Phase 6.

| Call | Case | Phase 6 (2026-10-23) | 7A2 (2026-10-24) |
|---:|---|---|---|
| 1 | representation_b | PASS (B used) | PASS (B used) |
| 2 | direct_fact | PASS, cite 4 source | PASS, cite 4 source |
| 3 | multi_source_synthesis | PASS, cite 1 source | PASS, cite 1 source |
| 4 | conditional_evidence | FAIL, 0 source | FAIL, 0 source |
| 5 | out_of_scope | PASS (fallback chuẩn, 0 source) | PASS (fallback chuẩn, 0 source) |

**4 PASS / 1 FAIL, không tệ hơn Phase 6.** Probe miễn phí (retrieval local e5,
đọc một collection cũ chỉ để lấy payload) cho `conditional_evidence`: ba chunk
bảng giá/tư vấn giá của file vé Cố đô (`#9`, `#77`, `#78`) có `search_text`
giống hệt bản cũ, và **vẫn không nằm trong top-30** của dense, BM25 lẫn RRF.
Root cause trùng với F2 của Phase 6 (retrieval miss, chuyển Phase 8); không phải
regression. Case 3 vẫn chỉ cite 1 source (F1 Phase 6, limitation đã biết).

### 4.5 Retrieval smoke 10 (Task 8 Step 4)

Profile `dense_bm25_rrf`, reranker `none`, K=10, 10 dòng của
`golden_full_corpus_smoke.jsonl`. Keyword được tính là xuất hiện nếu là chuỗi
con (sau casefold) của text top-10. Không ngưỡng. Chi tiết top-10 source để ở
`/tmp/phase7a2_gate2/retrieval_smoke_{e5,8b}.json` (private).

| Dòng | Category | Keyword e5 | Keyword 8B | Source khác nhau e5 / 8B | Source chung | Top-1 cùng source |
|---:|---|---|---|---|---:|---|
| 1 | direct_fact | 2/2 | 2/2 | 3 / 4 | 3 | có |
| 2 | conditional | 3/3 | 3/3 | 2 / 3 | 2 | có |
| 3 | multi_source | 2/2 | 2/2 | 3 / 4 | 2 | có |
| 4 | out_of_scope | 0/0 | 0/0 | 2 / 4 | 2 | không |
| 5 | comparative | 2/2 | 2/2 | 3 / 2 | 2 | có |
| 6 | direct_fact | 1/1 | 1/1 | 3 / 3 | 3 | có |
| 7 | comparative | 1/2 | 1/2 | 2 / 2 | 1 | có |
| 8 | conditional | 2/2 | 1/2 | 9 / 8 | 8 | có |
| 9 | multi_source | 2/2 | 2/2 | 9 / 6 | 4 | có |
| 10 | direct_fact | 3/3 | 3/3 | 1 / 2 | 1 | có |
| Tổng | | **18/19** | **17/19** | | | 9/10 |

Mọi query có trace `PASS`, không anomaly. Latency mỗi query: e5 khoảng 22–31 ms;
8B khoảng 1,1–1,5 s, một query 8,8 s (thời gian gọi OpenRouter).

### 4.6 Số call trả phí đã dùng

| Loại | Giới hạn | Đã dùng |
|---|---:|---:|
| Build 8B đầy đủ | 2 | **1** (133 request) |
| Embed query/mẫu OpenRouter | 50 | **13** = verify 1 + chẩn đoán 1 + retrieval smoke 11 (1 warm-up khi build service + 10 query) |
| `gpt-6-luna` | 5 | **5** |

Mọi request OpenRouter gửi `provider: {"data_collection": "deny"}`, không pin
provider. Data egress: toàn bộ 8.459 chunk (build) và 20 chunk mẫu × 2, 10 câu
smoke + 1 câu warm-up.

### 4.7 Grep Step 6

```text
grep -rn "metadata_v2_collection_name\|full_corpus_metadata_v2\|hue_full_corpus_a_\|e5-base-768\|huydang-dek21-768\|qwen3-embedding-0.6b" backend
```

Còn đúng 11 dòng, đều là setting key benchmark Foods 08a/08b (ngoại lệ Reviewer
đã chấp nhận): `backend/embedding/dense_benchmark.py:65`,
`backend/evaluation/sparse_benchmark.py:1965,1969,1974,1975,1981,1982`,
`backend/tests/test_embedding_benchmark.py:410,595,598`,
`backend/tests/test_sparse_benchmark.py:293`. Hai module này không import
`DENSE_MODEL_SPECS` full-corpus. Không còn tham chiếu tới hằng số
`EXPECTED_*`, `5662`, `PREFLIGHT_OUTPUT_PATH`, `PHASE3_EVIDENCE_PATH`,
`FULL_CORPUS_BUILD_SCHEMA_V2` hay `phase_3_sparse_state.json` trong `backend/`.

## 5. Lỗi và giới hạn

- **8B FAIL acceptance §5.5 mục 2** (cos min 0,99535 < 0,999), root cause ở
  mục 4.3. Không tự rebuild: build đã thành công nên không thuộc trường hợp
  "build lỗi" được phép chạy lại, và cách sửa khả dĩ (pin một provider cho build
  và query) là quyết định mới của User theo handoff/spec §8. Các lựa chọn để
  Reviewer/User quyết: (a) chấp nhận index trộn provider làm giới hạn cho Phase
  7B/8; (b) cấp quyền pin provider (ví dụ Nebius) rồi dùng lần build 8B thứ hai
  còn lại (cần xóa collection/record 8B hiện tại, là quyền mới vì build không
  lỗi) và chạy lại verify + retrieval smoke 8B (~12 call, còn dư 37); (c) đổi
  ngưỡng.
- Build record 8B chỉ ghi tập provider, không ghi provider theo batch, nên không
  chứng minh được batch nào do provider nào phục vụ.
- Live smoke vẫn 4/5: `conditional_evidence` FAIL (F2 Phase 6) và
  `multi_source_synthesis` PASS với 1 source (F1 Phase 6), đều là limitation đã
  biết, không đổi.
- Notebook không sửa theo chốt của Reviewer, **chưa chạy lại**:
  `notebooks/06_generation_and_api.ipynb` có tên cứng
  `hue_full_corpus_a_e5_small_384_metadata_v2` (sẽ gãy sau Gate 3);
  `notebooks/04_qdrant_ingestion.ipynb` lặp `FULL_CORPUS_CANDIDATES` và
  `build_record_path` chung (không còn tên cũ, nhưng chưa kiểm hành vi với 2
  candidate mới); `notebooks/08b_retrieval_fusion_benchmark.ipynb` có
  `e5-base-768` là setting Foods benchmark. Notebook 03 còn markdown mô tả 4
  model của Phase 3 (chỉ code cell được sửa).
- Sparse state dùng chung chỉ được ghi một lần; nếu corpus đổi về sau, build mới
  sẽ raise cho tới khi xóa `full_corpus_sparse_state.json` cũ (đúng plan Task 6
  Step 1.2).
- `data/full_corpus_builds/phase_3_sparse_state.json` và 8 build record cũ vẫn
  còn, xóa ở Gate 3.
- Runtime 8B cần mạng và mỗi lần build service tốn 1 call warm-up; không phải
  runtime mặc định.

## 6. Handoff cho Reviewer

- `full-read`: report này; exact diff `git diff 5e8aff1 -- backend notebooks/03_embedding_models.ipynb pyproject.toml uv.lock`
  (4 file xóa hiện là ` D` trong worktree, không staged).
- Reviewer chạy lại theo Review Contract Gate 2 (read-only): count + payload +
  chiều hai collection; đọc hai build record
  `data/full_corpus_builds/hue_full_corpus_7a2_*.json`; health runtime. Không
  chạy lại paid call.
- Quyết định cần trình User: hướng xử lý 8B cos < 0,999 (mục 5, lựa chọn a/b/c).
- Deviation D1 (qdrant `{384, 4096}`) và D2 (mẫu verify = chunk đầu mỗi domain)
  đã được Reviewer chấp nhận ngày 2026-10-24.
- Script tạm và output private: `/tmp/phase7a2_gate2/` (không commit).
- Git: không commit, index trống.

## Correction 1 — pin Nebius cho 8B (2026-10-24)

Handoff `correction` (A), finding F1 trong
`reports/phase_7a2_gate_2_review_2026_10_24.md`. User chọn (b), xác nhận lại
một dòng với B trước khi xóa và build.

**Kết quả: dừng theo điều kiện dừng.** Build 8B lần 2/2 lỗi HTTP 504 ở batch
20/133. Không build lần 3, không đổi provider.

### C1.1 Thay đổi code

- `backend/embedding/full_corpus.py`: thêm `OPENROUTER_PROVIDER_ROUTING =
  {"order": ["nebius"], "allow_fallbacks": False, "data_collection": "deny"}`
  và gửi nó trong mọi request. `parse_embeddings_response` raise nếu
  `provider != "Nebius"` (`OPENROUTER_EXPECTED_PROVIDER`). Docstring runner đổi
  từ "không pin" sang pin Nebius. Vẫn không retry/fallback/resume.
- `backend/tests/test_full_corpus_embedding.py`: thêm case thuần (dict response
  viết tay) cho provider `SiliconFlow` → raise `provider`.
- `HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_full_corpus_embedding.py -q`:
  **24 passed**.

### C1.2 Xóa index 8B cũ

Trạng thái trước: `hue_full_corpus_7a2_qwen3_8b_4096` 8.459 point, status
green; record SHA-256 `ea4672c16bc9c606d3f2f805f447a0539261ecd4da4bba0b4147f18800372208`.
Đã xóa đúng collection đó (`DELETE /collections/hue_full_corpus_7a2_qwen3_8b_4096`
→ `result: true`) và file record của nó. Sau xóa: collection 7a2 còn lại chỉ
`hue_full_corpus_7a2_e5_small_384`; record 7a2 còn lại chỉ của e5; sparse state
chung không đổi.

### C1.3 Build lần 2/2

```bash
HF_HUB_OFFLINE=1 uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline build --candidate qwen3-embedding-8b-4096
```

- 20 request OpenRouter, 19 HTTP 200 (batch 1–19), request thứ 20 trả **HTTP
  504 Gateway Timeout** (body `error code: 504`) lúc 12:17:58, khoảng 60 s sau
  request trước. Exit 1, lỗi raise trong `OpenRouterDenseRunner._embed`.
- Khi pin Nebius, mỗi batch mất khoảng 10–30 s (12:13:29 → 12:16:58 cho 19
  batch). Build không pin trước đó trung bình khoảng 3 s/batch.
- Lỗi xảy ra trong bước embed, **trước khi tạo collection**: Qdrant không có
  collection 8B mới, không có record 8B. Sparse state chung không bị ghi lại
  (đã có sẵn, byte-identical).
- Data egress lần này: 20 batch × 64 chunk = 1.280 chunk (19 batch thành công
  và 1 batch lỗi), gửi kèm routing pin Nebius.

### C1.4 Không chạy

Do build lỗi, bước 5–6 của handoff **không chạy**: verify 8B và retrieval
smoke 8B mới. Không call query nào được dùng trong Correction 1.

Bước 7 vẫn chạy được vì không phụ thuộc index 8B: focused suite 6 file
(như Task 8 Step 5) cho **96 passed in 22.16s** (thêm 1 case provider so với 95),
`git diff --check` exit 0.

### C1.5 Paid đã dùng (cộng dồn Gate 2)

| Loại | Giới hạn | Đã dùng |
|---|---:|---:|
| Build 8B đầy đủ | 2 | **2** (lần 1 xong 133 request; lần 2 lỗi ở request 20) |
| Query/mẫu OpenRouter | 50 | 13 (không đổi) |
| `gpt-6-luna` | 5 | 5 (không đổi) |

### C1.6 Trạng thái hiện tại và quyết định cần User

- Runtime mặc định (e5-small) không bị ảnh hưởng: collection, record, health và
  live smoke vẫn như mục 4.
- Hiện **không có index 8B**. Đường query 8B (`build_full_corpus_retrieval_service`
  với `qwen3-embedding-8b-4096`) sẽ báo collection không tồn tại.
- Lựa chọn để A trình User (B không tự làm): (1) cấp thêm một lần build 8B
  (pin Nebius như cũ) và chấp nhận rủi ro 504 lặp lại; (2) cho phép provider
  khác hoặc batch nhỏ hơn (đổi spec §5.2); (3) hoãn index 8B sang Phase 7B/8,
  đóng Gate 2 chỉ với e5.
- Evidence e5/health/live smoke/retrieval smoke e5 vẫn hợp lệ vì correction chỉ
  đổi nhánh OpenRouter, không đổi corpus, chunker, build path local, retrieval
  profile hay runtime mặc định.
