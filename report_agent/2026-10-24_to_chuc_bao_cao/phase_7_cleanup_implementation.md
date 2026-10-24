# Implementation Report: dọn sau Phase 7 (B9) — **DỞ, dừng ở điểm an toàn**

Người làm: B (Claude Opus 5.5, terminal `hue-rag-64`)
Date: 2026-10-24 17:10 +0700 (lấy bằng `date`)
Việc: `session_prompt/CURRENT_HANDOFF.md` → B9; đích theo `reports/phase_7_cleanup_inventory_2026_10_24.md` (C2)

## 0. Tóm tắt trạng thái

| Bước | Trạng thái |
|---|---|
| 1. Gỡ code/test/notebook/settings Foods, sửa notebook 03/04/06, xóa `requirements.txt` | **Xong**, nằm trong working tree, **chưa commit** |
| 2. Sửa test chunker so với artifact 8.460 | **Xong** (so với build record đang chạy) |
| 3. Kiểm (C2 §5 + so byte retrieval + `/health` + smoke 10 paid) | **PARTIAL**. Lượt pytest sau khi dọn gặp Qdrant tắt giữa chừng. Các phần cần Qdrant **NOT RUN** (mục 4) |
| 4. Xóa 2 collection Foods + 5 file `data/full_corpus_metadata_v2_*.json` | **NOT RUN**. Chưa xóa gì ở Qdrant hay `data/`, vì bước 3 chưa đạt |

Lý do dừng: điều kiện dừng của B9 là "test full-corpus fail; API không lên". Lúc 17:10 +0700,
Qdrant `127.0.0.1:6335` không trả lời (`curl` exit 7, không có tiến trình nghe ở 6335/6336).
B chỉ gọi GET tới Qdrant nên Qdrant tắt không do thao tác của B; A báo phiên đang kết thúc.
B không tự khởi động lại Qdrant.

## 1. Mốc trước khi dọn (ghi trước, 2026-10-24 ~16:55)

- Qdrant `GET /collections`: đúng 3 collection. `hue_foods_e5_small_384` 572,
  `hue_foods_e5_small_384_dense` 572, `hue_full_corpus_7a2_e5_small_384` 8.459. Khớp
  {2 Foods + 1 full-corpus}, nên đi tiếp được.
- Mốc retrieval: `data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl`, SHA-256
  `cefb2d1ad6094913064dd469acaa6ffb00aebd79f654ba89b7d8b07fe55826e4`. Bản sao:
  `/tmp/phase7_cleanup/retrieval_baseline.jsonl`.
- `backend/evaluation/full_corpus_eval.py` không import `evaluation.eval` (grep), đạt ràng buộc C2 §3.1.
- Pytest trước khi dọn: 15 file full-corpus (C2 §5 cộng `test_full_corpus_eval`, `test_api_chat`,
  `test_openai_full_corpus_generator`, `test_phase6_live_smoke`) cho **192 passed, 1 failed**. Test
  fail là `test_full_corpus_determinism_and_preview_byte_equality` (8.459 ≠ 8.460, đã biết).
  Log: `/tmp/phase7_cleanup/pytest_before.txt`.
- 5 file sẽ xóa ở bước 4 (chưa xóa): `data/full_corpus_metadata_v2_{execution,smoke,minilm_smoke,reviewer_smoke,reviewer_minilm_smoke}.json`.

## 2. Đã xóa (42 file tracked + thư mục `backend/ingestion/helpers/`)

- **Code Foods** (C2 §2.2):
  - `backend/core/startup.py`, `backend/embedding/{embedder,dense_benchmark}.py`;
  - `backend/ingestion/{pipeline.py,chunking/markdown_chunker.py,helpers/}`;
  - `backend/retrieval/{service,dense_retriever,hybrid_retriever,context_builder}.py`;
  - `backend/llm/{generator_openai,prompt}.py`, `backend/vectorstore/reset.py`;
  - `backend/evaluation/{eval,evaluator,test,template,golden_dataset,retrieval_comparison,embedding_benchmark,sparse_benchmark,reranker_benchmark}.py`;
  - `backend/evaluation/{answer,retrieval}_results.csv`.
- **Test Foods** (C2 §2.3): `test_{retrieval_service,embedder,embedding_benchmark,evaluation,reranker_benchmark,sparse_benchmark,ingestion_pipeline,markdown_chunker,context_builder,llm_generator_openai}.py`.
  Không test nào trong số này được chạy trước khi xóa, vì chúng ghi Qdrant hoặc gọi paid.
- **Notebook** (C2 §2.4): 02, 05, 07, 08a, 08b, 08c.
- **Gốc repo:** `requirements.txt`.

Giữ nguyên, ngoài phạm vi: `backend/scripts/`, `backend/test.ipynb`, `evaluation/results/` (kết quả
lịch sử), `retrieval/full_corpus_smoke.py`, `llm/phase6_live_smoke.py`, `knowledge-base-hue/`,
`session_prompt/`.

## 3. Đã sửa

| File | Thay đổi |
|---|---|
| `backend/config/settings.yaml` | Bỏ `active_profile`, `profiles`, `knowledge_base` (Foods), `embedding`, `retrieval`, `reranking`, `llm`, `evaluation`, cùng các khóa Foods của `vector_database`. Giữ `vector_database.url/timeout`, `full_corpus*`, `full_corpus_runtime`, `full_corpus_generation` |
| `backend/core/settings_loader.py` | Bỏ kiểm `active_profile` (sửa cùng lượt với `settings.yaml`, C2 §3.2) |
| `backend/vectorstore/qdrant.py` | Bỏ `expected_schema`, `validate_collection_info`, `ensure_collection` |
| `backend/vectorstore/points.py` | Bỏ `point_id_for`, `validate_chunks`, `build_points`, import `uuid` |
| `backend/vectorstore/upsert.py` | Bỏ `upsert_points`, `validate_existing_points`, `verify_point_count`, `SCROLL_LIMIT`, logger không còn dùng |
| `backend/scoring/bm25.py` | Bỏ `min_max_normalize`, `validate_weights`. Giữ `tokenize`, `K1`, `B`, `BM25` (test sparse và notebook 03 dùng để đối chiếu) |
| `backend/tests/conftest.py` | Chỉ còn fixture full-corpus: `live_settings`, `require_openai_key`, `full_corpus_service`, `full_corpus_documents`. Bỏ mọi fixture tạo/ghi collection test |
| `backend/tests/test_bm25.py` | Bỏ 2 test của 2 hàm đã xóa |
| `backend/tests/test_full_corpus_chunker.py` | Test determinism so số file/chunk với **build record đang chạy** (`data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json`) thay cho artifact 2026-09-11 (8.460). Bỏ khóa `active_profile`/`profiles` thừa trong 2 settings giả lập. Không đổi chunker |
| `backend/tests/test_full_corpus_qdrant_ingestion.py` | Bỏ assert tên 2 collection Foods không trùng candidate (C2 §2.1) |
| `notebooks/04_qdrant_ingestion.ipynb` | Code: chỉ kiểm candidate có build record (8B in "skipped"); lấy sample id như `full_corpus_pipeline.build_candidate` (chunk đầu mỗi domain). Markdown: 1 collection, 8.459 chunk. Outputs rỗng |
| `notebooks/03_embedding_models.ipynb` | Chỉ sửa markdown: 2 candidate hiện hành, 8.459 chunk, bỏ mô tả preflight/4 model |
| `notebooks/06_generation_and_api.ipynb` | Chỉ sửa markdown: collection 7a2 8.459 point; bỏ metadata v2 và `qwen3.5-9b` |

## 4. Kiểm sau khi dọn

| Kiểm | Lệnh | Kết quả |
|---|---|---|
| Import mọi module còn lại trong `backend/` + `load_settings()` | `uv run python` walk 10 package | **PASS**. 0 lỗi import; settings còn 4 nhóm |
| Import `retrieval.full_corpus_smoke`, `llm.phase6_live_smoke` | `uv run python -c …` | **PASS** |
| Grep tên module/collection/hàm đã xóa trong `backend/`, `notebooks/`, `frontend/`, `pyproject.toml` | `grep -rnE …` | **PASS**. 0 kết quả |
| Notebook 04 Run All trên bản tạm (Qdrant chỉ đọc, lúc Qdrant còn chạy) | `nbclient` với cwd `notebooks/` → `/tmp/phase7_cleanup/nb04_run.ipynb` | **PASS**. 0 lỗi; e5: point 8.459, payload 8.459, 5 vector mẫu; 8B "skipped: no build record" |
| Notebook 03 Run All trên bản tạm | như trên → `nb03_run.ipynb` | **PASS**. 0 lỗi |
| Pytest 15 file như lượt "trước" | `cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m pytest …` | **FAIL vì môi trường**: 176 passed, 6 failed, 9 errors. Cả 15 lỗi là `Connection refused` tới Qdrant hoặc `/health` "degraded" (retrieval không sẵn sàng vì Qdrant tắt). Log: `/tmp/phase7_cleanup/pytest_after.txt`. Test chunker 8.460 trước đây fail, giờ không còn trong danh sách lỗi |
| So byte retrieval với mốc | `full_corpus_eval retrieval --treatment dense_bm25_rrf` + `cmp` | **NOT RUN** (Qdrant tắt) |
| API in-process `/health` 200 + 1 retrieval | `create_app` + lifespan + `httpx.ASGITransport` | **NOT RUN** (Qdrant tắt) |
| `golden_full_corpus check` | `uv run python -m evaluation.golden_full_corpus check …` | **NOT RUN** (dừng trước bước này) |
| Smoke 10 paid | `full_corpus_eval generate --golden smoke` | **NOT RUN**, 0 USD |

`git diff --check`: sạch.

## 5. Tiền

Paid trong B9: **0 USD** (smoke 10 chưa chạy). Cả phiên, B dùng khoảng 0,087 USD (7B 0,082 + probe B5 0,005).

## 6. Phần còn dở và cách làm tiếp (phiên sau)

1. Bật lại Qdrant ở `127.0.0.1:6335`, rồi `curl -s http://127.0.0.1:6335/collections` phải còn đúng 3
   collection như mục 1. Khác thì dừng.
2. Chạy lại đúng lệnh pytest ở mục 4. Kỳ vọng ghi trước: không còn lỗi nào; test chunker determinism pass.
3. `cd backend && HF_HUB_OFFLINE=1 uv run python -m evaluation.full_corpus_eval retrieval --treatment dense_bm25_rrf --out /tmp/phase7_cleanup/retrieval_after.jsonl`
   rồi `cmp /tmp/phase7_cleanup/retrieval_after.jsonl /tmp/phase7_cleanup/retrieval_baseline.jsonl`. Phải
   giống từng byte. Nếu `/tmp` đã mất, dùng `data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl`
   (SHA ở mục 1).
4. API in-process `/health` 200 + 1 retrieval; `golden_full_corpus check` cho cả official và smoke.
5. Smoke 10 paid (≤0,005 USD; Gate 1 tốn 0,0013 USD cho phần sinh).
6. Đạt hết thì xóa 2 collection Foods (liệt kê trước/sau) và 5 file `data/full_corpus_metadata_v2_*.json`.
7. Cập nhật report này, C review, A commit.

Nếu phiên sau muốn bỏ thay đổi: toàn bộ đang ở working tree, `git checkout`/`git restore` theo đường
dẫn ở mục 2–3 là quay về được. Chưa có thao tác nào không đảo ngược được.

## 7. Bẫy / ghi chú

- Pytest chạy được dù Qdrant tắt. Lỗi môi trường trông giống lỗi code, nên phải đọc dòng `E` trước
  khi kết luận.
- Chạy notebook trên bản tạm bằng `nbclient` cần `resources={"metadata": {"path": "<repo>/notebooks"}}`
  để cell tìm repo root.
- `backend/test.ipynb` và `backend/scripts/` không thuộc C2; A xem có cần dọn không.
