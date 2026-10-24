# Implementation Report: Phase 7B Gate 0 — kiểm sức khỏe các Phase trước (B1)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-64`)
Date: 2026-10-24
Canonical guide:

```text
guides/full_corpus_rag.md (mục "Cập nhật Phase 7A2")
```

## 1. Phạm vi

Việc B1 trong `session_prompt/CURRENT_HANDOFF.md`: trước baseline 7B, xác nhận hệ
thống thật khớp tài liệu. Chỉ đọc và chạy free; không sửa code, dữ liệu, Qdrant;
không build lại index. Đã làm đủ 6 mục; có **một sự cố lệch quyền** khi chạy test
(mục 5.1).

## 2. Thay đổi chính

Không sửa file nào trong repo ngoài report này và `session_prompt/sessions/STATUS_B.md`.
Script kiểm tạm và output thô (private) nằm ngoài repo: `/tmp/phase7b_b1/`
(`audit.py`, `audit.json`, `pytest.txt`).

## 3. Cách đã chạy thật

```bash
# Mục 1–3: corpus, build record, Qdrant, runtime in-process + 1 retrieval (không generation)
HF_HUB_OFFLINE=1 uv run --env-file .env python /tmp/phase7b_b1/audit.py
# Mục 4: Golden
cd backend
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus.jsonl
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl
uv run python -c "<so khớp deep-equal smoke ⊂ official>"
# Mục 5: test suite (danh sách file ở mục 4.5)
HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m pytest -q -p no:cacheprovider -rfEs <17 file + test_evaluation.py> --deselect tests/test_evaluation.py::<5 test>
```

`audit.py` gọi đúng code production: `prepare_full_corpus_input()` (discover → hash →
chunker → identity → sparse refit), `verify_full_corpus_record_freshness`,
Qdrant `get_collection` / `scroll` toàn bộ payload / `retrieve` 1 point có vector,
`create_app()` + `lifespan_context` + `httpx.ASGITransport` → `GET /health`, rồi
`app.state.retrieval_service.search(<1 câu hỏi tự đặt, không thuộc Golden>)`.

## 4. Kết quả quan sát

| # | Mục kiểm | Kết quả | Bằng chứng |
|---|---|---|---|
| 1 | Corpus 205 file, 8.459 chunk | PASS | chunker hiện hành: 205 file (foods 91, heritages 29, festivals 27, performing_arts 13, travel 45), 8.459 chunk, 0 lỗi; 23 s |
| 2a | Build record khớp corpus | PASS | `full_corpus_build:v3`, `complete`, file 205 / chunk 8.459 / point 8.459; identity record = identity chunk lại; freshness `fresh`, 0 discrepancy; dense `intfloat/multilingual-e5-small` 384, providers rỗng |
| 2b | Sparse state | PASS | vocabulary 5.660; SHA-256 file = record; refit từ corpus hiện tại byte-identical với file |
| 2c | Qdrant collection runtime | PASS | `hue_full_corpus_7a2_e5_small_384`: 8.459 point, `green`; dense `dense` 384 Cosine + sparse `sparse`; scroll 8.459 point, **mọi** point đúng 7 field payload; tập point ID = UUID5 của chunk ID chunker (bằng nhau); point mẫu có dense 384 + sparse 79 nnz; domain: travel 3.322, foods 1.670, heritages 1.613, festivals 1.130, performing_arts 724 |
| 2d | Qdrant tổng | PASS | đúng 3 collection: 8.459 / 572 / 572 |
| 3 | Runtime | PASS | `/health` 200, `status: ok`, 5 component ready; 1 retrieval `dense_bm25_rrf`: 10 tài liệu, 0,03 s, classification `PASS`, 0 anomaly, top nguồn đúng chủ đề |
| 4 | Golden | PASS | `check` official: 176 case, exit 0 (direct_fact 75, multi_source 29, conditional 29, comparative 25, out_of_scope 18); smoke: 10 case, exit 0; 10/10 dòng smoke deep-equal một dòng official; schema đúng 4 field |
| 5 | Test suite free | PARTIAL | trong tập dự định: 213 test → 211 passed, 2 failed (đều do hằng số/dữ liệu cũ, không phải lỗi runtime); 7 file NOT RUN; sự cố deselect (5.1) |
| 6 | Đối chiếu `Project_Status.md` §4 | PASS | mọi số đo khớp (205 / 8.459 / 7 field / dense+sparse / 5.660 / 3 collection / `dense_bm25_rrf` / reranker `none` / `gpt-6-luna` trong `settings.yaml`) |

### 4.5 Chi tiết test suite

Đã chạy (17 file + phần free của `test_evaluation.py`): `test_api_chat`, `test_bm25`,
`test_citations`, `test_context_builder`, `test_embedder`, `test_full_corpus_chunker`,
`test_full_corpus_context`, `test_full_corpus_embedding`,
`test_full_corpus_qdrant_ingestion`, `test_full_corpus_retrieval`,
`test_full_corpus_sparse`, `test_golden_full_corpus`, `test_markdown_chunker`,
`test_openai_full_corpus_generator`, `test_phase6_live_smoke`, `test_phase6_settings`,
`test_static_ui`. Các test `require_openai_key` trong `test_api_chat`,
`test_phase6_live_smoke`, `test_openai_full_corpus_generator` đã đọc code: chúng
dừng trước provider (lỗi budget context / `generator_ready=False` / input rỗng), không
gọi paid.

Failed trong tập dự định (ghi lại, **không sửa** — thuộc việc dọn C2):

| Test | Nguyên nhân quan sát |
|---|---|
| `test_full_corpus_chunker.py::test_full_corpus_determinism_and_preview_byte_equality` | so số chunk với artifact cũ `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json` (8.460); corpus sau 7A2 cho 8.459 → test lỗi thời, không phải chunker hỏng |
| `test_evaluation.py::test_golden_v2_contract_and_distribution` | Foods Golden V2 (lịch sử): 1 keyword của case `foods-0087` không còn trong evidence sau khi sửa corpus 7A2 |

NOT RUN (lý do):

| File | Lý do |
|---|---|
| `test_llm_generator_openai.py` | paid call (handoff loại) |
| `test_ingestion_pipeline.py`, `test_retrieval_service.py` | tạo collection test tạm trong Qdrant thật (vi phạm "Qdrant chỉ đọc") |
| `test_sparse_benchmark.py`, `test_reranker_benchmark.py`, `test_embedding_benchmark.py` | benchmark Foods/Phase 8 cũ: code dưới test có `create_collection`/`upsert` Qdrant và ghi `evaluation/results`, tham chiếu collection đã xóa ở 7A2 → rủi ro tạo lại collection/ghi file; đích dọn C2 |
| `test_evaluation.py` 5 test dùng `ingested_collection` | định deselect vì tạo collection tạm + 1 test paid — **nhưng vẫn chạy**, xem 5.1 |

## 5. Lỗi và giới hạn

### 5.1 Sự cố: deselect không có hiệu lực (đã báo A ngay)

- **Quan sát:** `--deselect tests/test_evaluation.py::…` không khớp node id vì rootdir
  pytest là gốc repo (node id thật `backend/tests/…`). Năm test định loại đã chạy:
  4 passed, 1 failed.
- **Hậu quả Qdrant:** fixture `ingested_collection` (`backend/tests/conftest.py`) tạo
  collection tạm `hue_rag_live_test_e5_small_384` (Foods 572 chunk) rồi tự xóa ở
  teardown. Sau khi chạy: `GET /collections` còn đúng 3 collection; collection thật
  không bị ghi (conftest chặn mọi tên không có prefix test).
- **Hậu quả paid:** `test_answer_evaluation_calls_real_generation_and_judge_models`
  (evaluator Foods cũ, `backend/llm/generator_openai.py`) gửi **1** request tới
  OpenAI `gpt-6-luna`; nhận HTTP 400 `Unsupported parameter: 'temperature'`, không có
  output. Usage: không có token output; chi phí ước tính ~0 USD (request 400 thường
  không tính token; chưa đối chiếu dashboard OpenAI).
- **Hậu quả file tracked (A phát hiện):** test retrieval Foods ghi đè
  `backend/evaluation/retrieval_results.csv` (diff 26 dòng). B đã khôi phục bằng
  `git checkout -- backend/evaluation/retrieval_results.csv`; sau đó `git status --short`
  không còn file tracked nào bị test đổi (chỉ còn file governance/report của A/B/C).
  File ignored bị ghi thêm: `backend/logs/application.log` (log runtime, do app
  in-process của audit và test) — không ảnh hưởng.
- **Bài học:** chỉ liệt kê đúng file test free cần chạy, không dựa vào `--deselect`
  (A đã ghi bẫy vào `Project_Status.md` §8). Với repo này chạy pytest từ `backend/` thì node id vẫn là
  `backend/tests/<file>::<test>`; muốn loại test có side effect thì nên loại cả file
  hoặc kiểm danh sách bằng `--collect-only` trước.

### 5.2 Phát hiện cho việc dọn (C2) và Phase 7B

- Evaluator/generator Foods cũ (`backend/evaluation/evaluator.py` → `llm/generator_openai.py`)
  **đã gãy với `gpt-6-luna`**: model không nhận `temperature`. 7B dùng đường
  `generator_openai_full_corpus.py` thì cần chắc judge mới không truyền `temperature`.
- Test chunker còn so với artifact preview 2026-09-11 (8.460), cần cập nhật hoặc gỡ.
- Foods Golden V2 không còn khớp corpus sau 7A2 (1 keyword) — lịch sử, đích dọn.
- `gửi chatgpt/` và `báo cáo nghiên cứu github.txt` untracked nhưng không nằm trong
  `.gitignore` (đã báo A khi mở phiên).

Không có lệch nào giữa `Project_Status.md` §4 và hệ thống thật.

## 6. Bàn giao cho người kiểm

- Đọc trước: bảng mục 4 và mục 5.1.
- Chạy lại nhanh nếu cần: `HF_HUB_OFFLINE=1 uv run --env-file .env python /tmp/phase7b_b1/audit.py`
  (chỉ đọc, ~1 phút); output thô ở `/tmp/phase7b_b1/audit.json`, `pytest.txt`.
- Kết luận của người làm: nền full-corpus (corpus → build record → Qdrant → runtime →
  Golden) khớp tài liệu, đủ để lấy baseline 7B. Các lỗi còn lại nằm ở code/test Foods
  và hằng số lịch sử.
- Không commit (B không có quyền).
