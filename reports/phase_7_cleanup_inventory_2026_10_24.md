# Danh sách dọn sau Phase 7 (C2, chỉ đọc)

Ngày: 2026-10-24 · Người làm: C · Việc: `session_prompt/CURRENT_HANDOFF.md` → C2 · Rủi ro: thấp.

Không xóa hay sửa gì. Không đụng `backend/evaluation/full_corpus_*` (B đang làm 7B). Report không
chép nội dung corpus hay Golden.

## 1. Cách xác định

- **Đang dùng** = module mà ba lối vào hiện hành import tới (bắc cầu): API `api.app`, build
  `ingestion.full_corpus_pipeline`, Golden `evaluation.golden_full_corpus`. Tôi lập đồ thị import
  bằng AST (script `/tmp/c_probe/imports.py`, ngoài repo). Kết quả: 26 module đang dùng; mọi
  module khác trong `backend/` không được runtime/build/Golden gọi tới.
- Ai tham chiếu: grep tên module, collection, file trên toàn repo (trừ `.venv`, `data/`,
  `knowledge-base-hue/`, `qdrant_storage/`). Tham chiếu trong `docs/`, `reports/`, `handoff_prompt/`
  và `PROJECT_HISTORY.md` là lịch sử, không tính là đang dùng.
- Qdrant: chỉ GET `/collections/<tên>` và `/snapshots`.
- Notebook: đọc tĩnh (import, tên collection/model), **không chạy**.

## 2. Đích dọn

Đề xuất: **Xóa** · **Sửa** (giữ file, bỏ phần cũ) · **Giữ**.

### 2.1 Qdrant

| Đích | Hiện trạng | Ai tham chiếu (đang dùng) | Xóa làm gãy gì | Đề xuất |
|---|---|---|---|---|
| `hue_foods_e5_small_384` | 572 point, dense + sparse, không có snapshot | `settings.yaml` `vector_database.collection_name` → chỉ `core/startup.py` (API Foods cũ, không còn được API gọi); `evaluation/sparse_benchmark.py`; notebook 08a, 08b; `tests/conftest.py` `ACTIVE_COLLECTION` (chỉ để **từ chối** ghi đè) | Không gãy runtime full-corpus. Gãy notebook 08a/08b và benchmark Foods (cũng nằm trong danh sách xóa) | Xóa, cùng đợt với code Foods (§2.2) |
| `hue_foods_e5_small_384_dense` | 572 point, chỉ dense, không có snapshot | notebook 05 | Gãy notebook 05 (cũng đề xuất xóa) | Xóa |

Không cần snapshot nếu User đồng ý bỏ hẳn Foods: kết quả benchmark Foods đã lưu ở
`evaluation/results/` và report. `test_full_corpus_qdrant_ingestion.py:399` chỉ kiểm hai tên này
**không** trùng candidate → không cần sửa test, có thể bỏ dòng đó khi dọn cho gọn.

### 2.2 Code `backend/` Foods (không lối vào hiện hành nào gọi)

| Đích | Ai đang import (ngoài nhóm Foods) | Đề xuất |
|---|---|---|
| `core/startup.py` (khởi động API Foods theo `active_profile`) | `retrieval/service.py`, `tests/test_retrieval_service.py` | Xóa |
| `embedding/embedder.py`, `embedding/dense_benchmark.py` | `core/startup`, `ingestion/pipeline`, benchmark, `conftest.py` | Xóa |
| `ingestion/pipeline.py`, `ingestion/chunking/markdown_chunker.py`, `ingestion/helpers/split_text.py` (+ `helpers/__init__.py`) | nhóm Foods, `conftest.py`, notebook 02 | Xóa |
| `retrieval/service.py`, `dense_retriever.py`, `hybrid_retriever.py`, `context_builder.py` | nhóm Foods, `evaluation/eval.py` | Xóa |
| `llm/generator_openai.py`, `llm/prompt.py` | `evaluation/eval.py`, `tests/test_llm_generator_openai.py` | Xóa. **Đường này đã gãy thật** (B1, A chuyển 2026-10-24): generator gửi `temperature` (`generator_openai.py:30,44`, lấy từ `settings.yaml` `llm.temperature: 0.2` qua `eval.py:148`), `gpt-6-luna` trả HTTP 400. Judge Foods `eval.py:131` cũng đặt `temperature=0` |
| `vectorstore/reset.py` (reset collection Foods) | `tests/test_ingestion_pipeline.py` | Xóa |
| `evaluation/eval.py`, `evaluator.py`, `test.py`, `template.py`, `golden_dataset.py`, `retrieval_comparison.py`, `embedding_benchmark.py`, `sparse_benchmark.py`, `reranker_benchmark.py` | lẫn nhau, tests Foods, notebook 07, 08a/b/c | Xóa — **sau khi** B2 xong (xem §3.1) |
| `evaluation/answer_results.csv`, `evaluation/retrieval_results.csv` (tracked, output của `eval.py`) | `eval.py:21–22` ghi đè qua `save_csv` (dòng 286, 327); guide Phase 7/8 cũ. B1: chạy test evaluator Foods **ghi đè file tracked này** | Xóa (an toàn: không code đang dùng nào đọc; xóa cùng `eval.py`) |

Hàm Foods trong module **đang dùng** (giữ module, bỏ hàm):

| Module | Hàm chỉ Foods dùng | Đề xuất |
|---|---|---|
| `vectorstore/qdrant.py` | `expected_schema`, `validate_collection_info`, `ensure_collection` (đọc `vector_database.collection_name/vector_size`) | Sửa |
| `vectorstore/points.py` | `point_id_for`, `validate_chunks`, `build_points` | Sửa |
| `vectorstore/upsert.py` | `upsert_points`, `validate_existing_points`, `verify_point_count` | Sửa |
| `scoring/bm25.py` | class `BM25`, `min_max_normalize`, `validate_weights` (live chỉ dùng `tokenize`, `K1`, `B`). `BM25` còn được `tests/test_bm25.py`, `test_full_corpus_sparse.py` và notebook 03 dùng để đối chiếu sparse = BM25 | Sửa: bỏ `min_max_normalize`, `validate_weights`; `BM25` giữ nếu muốn giữ phép đối chiếu trong test/notebook 03 |
| `core/settings_loader.py` | `load_settings` bắt buộc `active_profile` nằm trong `profiles` (dòng 15–21) | Sửa cùng lúc với `settings.yaml` (§2.5), nếu không mọi lối vào sẽ raise |

### 2.3 Tests

| Đích | Lý do | Đề xuất |
|---|---|---|
| `test_retrieval_service.py`, `test_embedder.py`, `test_embedding_benchmark.py`, `test_evaluation.py`, `test_reranker_benchmark.py`, `test_sparse_benchmark.py`, `test_ingestion_pipeline.py`, `test_markdown_chunker.py`, `test_context_builder.py`, `test_llm_generator_openai.py` | Chỉ test module Foods ở §2.2. `test_ingestion_pipeline`/`test_retrieval_service`/`test_evaluation` dùng fixture `ingested_collection` **ghi collection test vào Qdrant**. B1: `test_evaluation.py` (một phần) còn **gọi paid** và ghi đè `retrieval_results.csv`/`answer_results.csv` tracked; `test_llm_generator_openai.py` gọi paid (đã ghi trong `Project_Status.md` §8) | Xóa (an toàn: không test nào của code đang dùng phụ thuộc; xóa cùng fixture Foods trong `conftest.py`). Trước khi xóa: **không chạy** các test này |
| `tests/conftest.py` | Fixture Foods: `real_chunks`, `real_embedder`, `ingested_collection`, `ingested_point_structs`, `real_retrieved_docs`, `make_test_settings`, `cleanup_collection`, `sweep_test_collections`, `ACTIVE_COLLECTION`. Fixture full-corpus còn dùng: `live_settings`, `require_openai_key`, `full_corpus_service`, `full_corpus_documents` (`test_citations`, `test_full_corpus_context`, `test_api_chat`, …) | Sửa: chỉ giữ fixture full-corpus |
| Còn lại (`test_full_corpus_*`, `test_api_chat`, `test_citations`, `test_bm25`, `test_golden_full_corpus`, `test_openai_full_corpus_generator`, `test_phase6_*`, `test_static_ui`) | Test module đang dùng | Giữ (`test_bm25`: bỏ phần `min_max_normalize`/`validate_weights` nếu bỏ hàm) |

### 2.4 Notebook

| Notebook | Hiện trạng (đọc tĩnh) | Đề xuất |
|---|---|---|
| 02 `foods_data_and_chunking` | Import `ingestion.chunking.markdown_chunker` (Foods) | Xóa (hoặc viết lại cho chunker full-corpus nếu User muốn giữ notebook học chunking) |
| 03 `embedding_models` | Code dùng module hiện hành (`DENSE_MODEL_SPECS`, sparse). Markdown cell 0, 2, 6 còn mô tả **4 model** (e5-base, HuyDang, Qwen3-0.6B CUDA) và 8.460 chunk | Sửa markdown → 2 candidate hiện hành, 8.459 chunk |
| 04 `qdrant_ingestion` | Lặp `FULL_CORPUS_CANDIDATES` (2 candidate) nhưng build record 8B không tồn tại → `read_text` lỗi; gọi `prepared.sample_chunk_ids` nhưng `PreparedFullCorpus` không có field này (`full_corpus_pipeline.py:77–82`); markdown ghi "four isolated candidate collections", 8.460 | Sửa: chỉ kiểm candidate có build record; lấy sample id như `full_corpus_pipeline.py:147` |
| 05 `retrieval_profiles` | Dùng `retrieval.service`/`context_builder` (Foods) + collection `_dense` | Xóa (hoặc viết lại trên `retrieval.full_corpus`) |
| 06 `generation_and_api` | Code dùng `api.app` hiện hành (chưa chạy: có gọi OpenAI trả phí). Markdown cell 0 và 7 ghi collection `..._metadata_v2` đã xóa, 8.460 point, `qwen3.5-9b` | Sửa markdown |
| 07 `evaluation` | Dùng `evaluation.eval/evaluator/test` (Foods) | Xóa; 7B có thể tạo notebook mới nếu có giá trị học tập |
| 08a, 08b, 08c | Benchmark Foods (`evaluation.*_benchmark`); 08a tham chiếu collection `hue_foods_08a_*` đã xóa; **08b còn output ở 16 cell** (trái `Session_Prompt.md` §11) | Xóa; kết quả đã lưu ở `evaluation/results/` |

### 2.5 `backend/config/settings.yaml`

| Khóa | Ai đọc | Đề xuất |
|---|---|---|
| `active_profile`, `profiles` | `settings_loader.load_settings` (validate), `core/startup.py` | Xóa + sửa `settings_loader` |
| `knowledge_base` (glob `foods/**`) | Foods pipeline | Xóa |
| `embedding` | `core/startup`, `ingestion/pipeline` | Xóa |
| `vector_database.url`, `.timeout` | **Đang dùng**: `vectorstore/qdrant.client_from_settings`, `full_corpus_pipeline._phase4_settings` (pin `localhost:6335`, timeout 30) | Giữ |
| `vector_database.collection_name`, `.vector_size`, `.distance`, `.upsert_batch_size` + comment reset | Foods (`ensure_collection`, `expected_schema`, `core/startup`) | Xóa |
| `retrieval`, `reranking`, `llm`, `evaluation` (trỏ `foods/evaluation/tests.jsonl`) | Foods (`core/startup`, `eval.py`). Reranker full-corpus lấy model id mặc định trong code `cross_encoder.py:13`, không đọc `reranking` | Xóa |
| `full_corpus.embedding_models` (3 tokenizer gồm e5-base, HuyDang) | Chunker full-corpus | Giữ — đổi là quyết định Phase 8 (H1 trong `reports/phase_8_candidate_hypotheses_2026_10_24.md`), đổi sẽ đổi chunk |
| `full_corpus*`, `full_corpus_runtime`, `full_corpus_generation` | Runtime | Giữ |

### 2.6 Dữ liệu private ngoài Git (`data/`, `knowledge-base-hue/`)

| Đích | Ai tham chiếu | Đề xuất |
|---|---|---|
| `data/full_corpus_metadata_v2_{execution,smoke,minilm_smoke,reviewer_smoke,reviewer_minilm_smoke}.json` | Không code nào (chỉ report lịch sử); của collection metadata v2 đã xóa ở 7A2 | Xóa |
| `data/full_corpus_phase_5_smoke_{questions,trace}.json` | `retrieval/full_corpus_smoke.py` (Phase 5 smoke runner) | Giữ cùng runner (xem §4) |
| `data/full_corpus_phase_6_live_{cases,smoke}.json`, `data/full_corpus_phase_7a2_live_smoke.json` | `llm/phase6_live_smoke.py`; bằng chứng Phase 6/7A2 | Giữ |
| `knowledge-base-hue/foods/evaluation/`: `golden_v2*.jsonl`, `golden_v3*.jsonl`, `tests.jsonl`, `test2.jsonl`, `answer_subset_v1.json`, `judge_calibration_v1.jsonl`, `validate_tests.py` | `evaluation/golden_dataset.py`, `evaluation/test.py`, `settings.yaml` `evaluation.test_file` (đều Foods) | Giữ hay xóa là quyết định User (Foods Golden V3 ghi là "lịch sử"); nếu xóa code Foods thì file không còn consumer |
| `knowledge-base-hue/foods/evaluation/golden_full_corpus_authoring.jsonl` | **Đang dùng**: `evaluation/golden_full_corpus.py` (`check`/merge Golden 7A) | **Giữ** — không xóa cả thư mục `foods/evaluation/` |

### 2.7 `session_prompt/` và file gốc repo

| Đích | Hiện trạng | Ai tham chiếu | Đề xuất |
|---|---|---|---|
| `FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md`, `FULL_CORPUS_GOLDEN_EVALUATION_REFERENCE_HANDOFF.md`, `FULL_CORPUS_PARSER_LOCATOR_SURVEY_HANDOFF.md`, `FULL_CORPUS_REVIEWER_NEXT_SESSION_PROMPT.md`, `FULL_CORPUS_VN_QT_TOKEN_CHECK_HANDOFF.md` | Stub 5 dòng "đã chuyển" sang `handoff_prompt/` | Link trong `handoff_prompt/`, report, docs lịch sử | Xóa được; link lịch sử sẽ chết. Nếu muốn link không chết: giữ (mỗi file 5 dòng) |
| `IMPLEMENTER_WORKFLOW.md`, `REVIEWER_WORKFLOW.md`, `brainstorming.md` | Stub 5 dòng "thay bởi Governance v2 / propose-options" | Lịch sử; `REVIEWER_WORKFLOW.md` còn trong `.claude/settings.local.json` (permission cũ) | Như trên |
| `TICKETS_IMPLEMENTER_NEXT_SESSION_PROMPT.md` (42 dòng, prompt Implementer tháng 09) | Không ai tham chiếu | — | Xóa |
| `chạy_môi_trường.md` (26 dòng) | Không ai tham chiếu; trùng `Session_Prompt.md` §10 và còn ví dụ `python -m ingestion.pipeline` (Foods) | — | Xóa |
| `requirements.txt` (gốc repo, tracked) | Không ai tham chiếu (ngoài lịch sử); trái `Session_Prompt.md` §10 (chỉ `uv`); chứa mục `vectorstore` không phải package PyPI | — | Xóa (ngoài danh sách A giao, ghi thêm) |
| `PROJECT_DOCUMENT_REGISTRY.md` (gốc) | `Status: audit_in_progress`, `Owner: Reviewer` — vai cũ | Lịch sử | A xem: cập nhật hay chuyển `handoff_prompt/` |
| Guide `guides/phase_{0..8}_*.md`, `llm_rag_reference_for_hue_rag.md` | Mô tả Foods/Phase cũ, trỏ module sẽ xóa | Lịch sử | Giữ (reference-only); nếu xóa code Foods, A thêm một dòng đầu guide Phase 2–8 "code Foods đã gỡ ngày …" |

## 3. Ràng buộc khi dọn

1. **7B đang chép hàm metric từ `eval.py`** (spec `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md` §4.5 "nên chép hàm metric từ `eval.py`":
   `calculate_mrr`, `calculate_dcg`, `calculate_ndcg`, `score_retrieval`, `RetrievalScores`). Chỉ
   xóa `backend/evaluation/eval.py` sau khi B2 đã chép xong và `full_corpus_eval.py` **không**
   import `evaluation.eval` (kiểm bằng grep lúc dọn).
2. `settings.yaml` và `settings_loader.py` phải sửa trong cùng một thay đổi (validate
   `active_profile`); giữ `vector_database.url/timeout`.
3. Xóa module Foods và test/fixture Foods cùng lúc, nếu không pytest collect lỗi import.
4. Không xóa `knowledge-base-hue/foods/evaluation/` nguyên thư mục (file authoring 7A).
5. Qdrant: xóa đúng 2 tên ở §2.1; liệt kê lại collection trước khi xóa, khác danh sách thì dừng
   (`WORKFLOW.md` §3.4).

Thứ tự đề xuất: (a) đợi B2 xong → (b) một commit gỡ code/test/notebook/settings Foods + sửa hàm
Foods trong module dùng chung → (c) chạy kiểm (§5) → (d) xóa 2 collection Foods → (e) sửa markdown
notebook 03/04/06, dọn `session_prompt/` và `requirements.txt` → (f) xóa file `data/` metadata v2.

## 4. Ngoài phạm vi, ghi để A cân nhắc

- `retrieval/full_corpus_smoke.py` (Phase 5 smoke) và `llm/phase6_live_smoke.py` (Phase 6 live
  smoke, có paid call) là runner một-lần của gate đã đóng; chỉ test của chính chúng dùng. Không
  phải Foods nên tôi không xếp xóa; 7B thay vai đo chất lượng. `llm/representation_b.py` được
  `phase6_live_smoke` và test generator dùng; Representation B là ứng viên Phase 8 (H10) → giữ.
- Một số hàm full-corpus Phase 4 chỉ còn test dùng: `vectorstore/qdrant.py`
  `classify_full_corpus_target`, `FullCorpusTargetObservation`, `validate_full_corpus_collection_params`;
  `vectorstore/upsert.py` `compare_full_corpus_records`; `ingestion/preview.py` `generate_preview`,
  `partition_for_source`, `resolve_local_model_path`. Cần đọc kỹ từng hàm trước khi kết luận là
  code chết.
- `.claude/settings.local.json` còn permission `curl` tới cổng 6333 / collection Foods — là cấu
  hình permission của User, tôi không đề xuất sửa.
- `khoi_phuc_moi_truong/` (ghi chú khôi phục WSL) — không thuộc dọn Phase 7.

## 5. Cách kiểm sau khi dọn (đề xuất cho người làm)

- `cd backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_full_corpus_chunker.py
  tests/test_full_corpus_sparse.py tests/test_full_corpus_embedding.py
  tests/test_full_corpus_qdrant_ingestion.py tests/test_full_corpus_retrieval.py
  tests/test_full_corpus_context.py tests/test_citations.py tests/test_bm25.py
  tests/test_golden_full_corpus.py tests/test_phase6_settings.py tests/test_static_ui.py -q`
  (không chạy test có paid call ngoài giới hạn).
- `uv run python -c` import ba lối vào (`api.app`, `ingestion.full_corpus_pipeline`,
  `evaluation.golden_full_corpus`) + `load_settings()`.
- Khởi động API, `GET /health` 200 (runtime vẫn từ chối nếu corpus lệch build record).
- `cd backend && HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check`.
- `curl -s http://127.0.0.1:6335/collections` còn đúng 1 collection full-corpus.
- grep lại tên module/collection đã xóa trên `backend/`, `notebooks/`, `session_prompt/` (trừ
  `PROJECT_HISTORY.md`).

## 6. Giới hạn

- Đồ thị import là phân tích tĩnh; import động (chuỗi, `importlib`) không bắt được — grep
  `importlib`/`import_module` trong `backend/` không thấy dùng ngoài thư viện.
- Notebook chỉ đọc tĩnh, không chạy; nhận định "gãy" của notebook 04 dựa trên code và file build
  record hiện có, chưa chạy thật.
- Không chạy test.
