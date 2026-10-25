# Rà code Phase 0–7 — luồng dựng index + nền (B25)

**DỞ — dừng 17:05 25/10 (User kết phiên).** Người làm: B (Claude Opus 5.5, terminal `hue-rag-de`) · 2026-10-25 17:05 +0700 (`date`) ·
chỉ đọc, 0 USD · rà trên `main` `bc568f1` (code B1 ở nhánh `p82-b1`, không rà ở đây).

- **Đã rà:** `backend/ingestion/full_corpus_pipeline.py`, `ingestion/source_state.py`, `ingestion/preview.py` (cấu trúc + nơi dùng),
  `embedding/full_corpus.py`, `embedding/sparse.py`, `scoring/bm25.py`, `vectorstore/qdrant.py`, `vectorstore/points.py`,
  `core/settings_loader.py`, `core/schema.py`, `core/logging_setup.py`, `config/settings.yaml`, `config/logging.yaml`, `pyproject.toml`,
  `docker-compose.yml`. Quét code thừa bằng AST + grep cho cả 5 thư mục (`/tmp/b25/usage.py`). Đo khởi động phần index (`/tmp/b25/startup.py`).
- **Chưa rà (phiên sau làm tiếp):** đọc kỹ `ingestion/chunking/full_corpus_chunker.py` (mới đọc đầu file + `ConditionManager`),
  `ingestion/chunking/markdown_blocks.py`, `vectorstore/upsert.py`; **test** (`test_bm25`, `test_full_corpus_chunker`, `_embedding`,
  `_qdrant_ingestion`, `_sparse`, `test_phase6_settings`, `conftest`); **notebook 03, 04**; **guide** `phase_0`–`phase_4`, phần index của
  `full_corpus_rag.md`, `guides/README.md`. Hai sub-agent rà guide và test / notebook đã bị B dừng khi kết phiên, **chưa ra file**
  (`data/ra_soat_code/` rỗng) ⇒ phiên sau giao lại.
- `scripts/` **không tồn tại** (mục việc B25 có nhắc) — lệch nhỏ giữa đề bài và repo.
- Mức của từng finding là tạm; top 10 chốt khi rà xong.

## Top (tạm, theo mức)

| # | id | Mức | Một dòng |
|---:|---|---|---|
| 1 | B-01 | **cao** | Cùng một module nạp hai lần (`core.schema` và `backend.core.schema`) ⇒ API bắt sai lớp lỗi: lỗi Qdrant khi đang hỏi ra 500 thay 503; corpus đổi lúc khởi động ra 503 thay 409 |
| 2 | B-02 | vừa | Kiểm hợp lệ chồng lớp khi build điểm Qdrant: cùng chunk được kiểm + mã hóa sparse hai lần |
| 3 | B-03 | vừa | `settings_loader` ghim cứng mọi giá trị sinh câu trả lời ⇒ `settings.yaml` thành bản sao hằng số; đổi một tham số phải sửa 2–3 chỗ |
| 4 | B-04 | vừa | `ingestion/preview.py` trộn hai việc: hàm đếm token mà chunker production dùng + CLI "Wave 1 preview" lịch sử (chỉ test gọi); chunker ↔ preview import vòng |
| 5 | B-05 | thấp | `verify_build_record_freshness` (schema build record cũ) không còn ai gọi ngoài một test; bản dùng thật là `verify_full_corpus_record_freshness` |
| 6 | B-06 | thấp | Ghim lặp: URL / timeout Qdrant ghim trong `full_corpus_pipeline._phase4_settings`, tên collection ghim trong `_COLLECTION_BY_CANDIDATE`, số chiều `{384, 4096}` ghim trong `qdrant.py` |
| 7 | B-07 | thấp | Code phòng xa không đường chạy: nhánh CUDA/float16 trong `FullCorpusDenseRunner.load`; trạng thái "empty" của target Qdrant; lớp `BM25` chỉ test dùng |
| 8 | B-08 | thấp | Câu hỏi đầu tiên sau khởi động chậm thêm ~1 s (e5 chưa "nóng") — giả thuyết cải thiện |
| 9 | B-09 | thấp | Lệch chữ: comment `docker-compose.yml` "Hue Foods RAG MVP"; `logging.yaml` đặt tên logger không khớp tên code dùng |
| 10 | B-10 | thấp (chỉ ghi) | 9 dependency không có `import` nào trong `backend/`, `notebooks/`, `frontend/` (User giữ thư viện thừa) |

## Findings

### B-01 — module nạp hai lần ⇒ API bắt sai lớp lỗi (cao)
- Khâu: nền (`core/`) + mọi module dùng mẫu `try: from backend.X … except ModuleNotFoundError: from X …`.
- Vị trí: mẫu import kép ở 9 file (`grep -rn "except ModuleNotFoundError" backend` ⇒ `retrieval/full_corpus.py:24`, `embedding/sparse.py:16`,
  `ingestion/source_state.py:16`, `ingestion/preview.py:24`, `ingestion/chunking/full_corpus_chunker.py` (2), `vectorstore/points.py:7`,
  `vectorstore/upsert.py`, `reranking/cross_encoder.py`, `retrieval/full_corpus_smoke.py`); bên bắt lỗi: `api/routes/chat.py` (import
  `core.schema`), `api/app.py:69-89`.
- Loại: 2 (khó theo / phức tạp) dẫn tới bug thật; liên quan cả khâu trả lời (phạm vi C34) — gốc ở cách import của nền.
- Quan sát (lệnh trong `backend/`, nạp đúng như production `import api.app`):
  - `sys.modules` có **cả** `core.schema` **và** `backend.core.schema` (cùng `core.settings_loader` / `backend.core.settings_loader`).
  - `retrieval.full_corpus.RetrievalDependencyError` lấy từ `backend.core.schema`; `api.routes.chat.RetrievalDependencyError` lấy từ
    `core.schema` ⇒ **hai lớp khác nhau** (`is` = False). Tương tự `ComponentNotReadyError`, `InvalidQueryError`. Các lỗi của context /
    citation / generator cùng một lớp (đều `core.schema`) nên không bị.
  - Lý do: `api/app.py` thêm cả gốc repo và `backend/` vào `sys.path` ⇒ nhánh `from backend.core.schema …` của `retrieval/full_corpus.py`
    import được, còn `chat.py` / `app.py` import `core.schema`.
- *Suy ra* (từ code, **chưa tái tạo bằng lỗi thật** — luật không cho tắt Qdrant / sửa kho để tạo lỗi):
  - Qdrant lỗi khi đang hỏi ⇒ `search` raise `backend.core.schema.RetrievalDependencyError`; `except (RetrievalDependencyError,)` trong
    `chat.py` không khớp ⇒ rơi vào `unhandled_handler` ⇒ **HTTP 500 `internal_error`** thay vì 503 `retrieval_unavailable`.
  - Corpus đổi so với build record lúc khởi động ⇒ lỗi `ComponentNotReadyError` / `RetrievalConfigurationError` (bản `backend.`) không khớp
    `except` đầu ⇒ rơi vào `except Exception` ⇒ **503 "tạm thời không khả dụng"** thay vì 409 "cần lập chỉ mục lại" (mất thông điệp đúng
    cho người vận hành; chatbot vẫn từ chối chạy — an toàn dữ liệu không đổi).
  - `test_api_chat.py` không có test cho 409 / 503 nên test vẫn xanh.
- Đề xuất nhỏ nhất: một cách import duy nhất cho mọi module trong `backend/` (ví dụ chỉ `core.*` / `retrieval.*` vì API và CLI đều chạy
  từ `backend/`; hoặc chỉ `backend.*`), bỏ mẫu `try / except ModuleNotFoundError`. Sửa nhiều file — cần A / User duyệt phạm vi.
- Cách kiểm khi sửa: lệnh `sys.modules` ở trên ⇒ không còn module `backend.core.*` song song; so `is` các lớp lỗi; test liệt kê file
  (không paid); T1 retrieval giống byte `cefb2d1a…` (cách import không được đổi kết quả).
- Rủi ro khi sửa: đụng nhiều file + harness 8.1 / notebook import theo `backend.*`; pytest rootdir là gốc repo (`Project_Status.md` §8) nên
  test đang import cả hai kiểu — phải chạy lại đủ file test thuần.

### B-02 — kiểm hợp lệ chồng lớp khi dựng điểm Qdrant (vừa)
- Vị trí: `vectorstore/points.py:36-65` (`validate_full_corpus_point_inputs`) và `:68-107` (`build_full_corpus_point_batch`); gọi ở
  `ingestion/full_corpus_pipeline.py:194-209`.
- Loại: 2 (validator chồng lớp — `Session_Prompt.md` §7 ghi là cơ chế đã loại).
- Quan sát: hàm thứ nhất kiểm cả kho: ma trận dense, trùng `chunk_id` / point id, `validate_chunk_id`, point id = UUID5, đủ 7 field payload,
  **mã hóa sparse** từng chunk + kiểm. Ngay sau đó, mỗi lô 64 chunk lại: kiểm ma trận dense, trùng `chunk_id`, `validate_chunk_id`, point id,
  **mã hóa sparse lần hai** + kiểm, kiểm 7 field. Tập 7 field viết hai lần (`:52-55`, `:92-95`). `upsert.py` còn kiểm lại sau upsert.
- *Suy ra*: không đổi kết quả, chỉ tốn đọc + gấp đôi mã hóa sparse lúc build (8.459 chunk — nhanh, không phải vấn đề tốc độ).
- Đề xuất: giữ một lần kiểm (trước khi tạo collection — đúng mục đích "không tạo collection dở"), lô chỉ dựng `PointStruct`.
- Kiểm khi sửa: build vào collection thử `hue_*` (cần quyền ghi Qdrant cho đích thử) ⇒ point / payload / vector giống collection runtime
  (so mẫu), build record giống trừ tên. Rủi ro: thấp, nhưng chạm luồng build — làm cùng lần build lại index.

### B-03 — `settings.yaml` nhóm sinh câu trả lời là bản sao hằng số (vừa; đã biết một phần)
- Vị trí: `core/settings_loader.py:24-78` (`validate_phase6_settings`): mọi key của `full_corpus_generation` / `full_corpus_runtime` bị so
  `!=` một hằng (model, token encoding, 2048, 256, 45, 16384, 2048, 512, 5…).
- Đã biết: inventory 8.1 §6 mục 6 ("loader chỉ cho một tổ hợp", X.1). **Điều mới:** B1 8.2 phải sửa 3 chỗ cho một tham số (yaml, loader,
  test ghim) — đúng như lo ngại; mọi thí nghiệm sau (E1, E2…) đụng tham số sinh sẽ lặp lại.
- Đề xuất: chọn một trong hai — (a) hằng số sống trong code, yaml bỏ nhóm đó; (b) yaml là nguồn, loader chỉ kiểm kiểu / miền giá trị.
  Quyết định thiết kế ⇒ A / User. Kiểm khi sửa: test settings + khởi động API + T1 byte.

### B-04 — `ingestion/preview.py` trộn hàm production và CLI lịch sử (vừa)
- Vị trí: `preview.py:52-118` (`resolve_local_model_path`, `load_tokenizers`, `count_tokens_for_chunk` — chunker production dùng qua
  lazy import ở `full_corpus_chunker.py:302-310`); `preview.py:121-342` (`partition_for_source` "seven P7 partitions",
  `generate_preview`, `main`, mặc định ghi `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`).
- Loại: 1 + 2. Quan sát: `generate_preview` / `partition_for_source` / `main` không có nơi gọi production (AST + grep: chỉ
  `tests/test_full_corpus_chunker.py:50-52, 886, 933, 1037`, và prompt lịch sử trong `handoff_prompt/`); `reports/` là lịch sử, không thêm
  file (`WORKFLOW.md` §6). Chunker ↔ preview import vòng, phải lazy import.
- Đề xuất: chuyển 3 hàm tokenizer sang module của chunker (hoặc `ingestion/tokenizers.py`), CLI preview + test của nó: giữ hay xóa — A / User
  chọn (giá trị duy nhất: kiểm "không đoạn nào vượt token" toàn kho; `chunk_full_corpus` đã fail-closed điều đó).
  Kiểm khi sửa: danh sách chunk sha giống hệt (8.459), T1 byte.

### B-05 — hàm freshness cũ không còn dùng (thấp)
- `ingestion/source_state.py:99-133` `verify_build_record_freshness` đọc `build_record["sources"]` (schema cũ); AST: không gọi trong file,
  `grep` ngoài: chỉ `tests/test_full_corpus_chunker.py:63`. Bản runtime: `verify_full_corpus_record_freshness` (`:217`, đọc
  `corpus.sources`) — cùng logic. Đề xuất: xóa hàm cũ + test của nó. Kiểm: grep 0 nơi gọi; test thuần đạt.

### B-06 — ghim lặp hằng số ở luồng build (thấp; đã biết một phần)
- `full_corpus_pipeline.py:96-103` ghim `url == "http://localhost:6335"`, `timeout == 30` (đã có trong `settings.yaml:36-38`);
  `:66-69` tên collection theo candidate; `vectorstore/qdrant.py:30` `dimension not in {384, 4096}` (đã có trong `DENSE_MODEL_SPECS`).
- Đã biết: bảng G5 §4 dòng Ingestion (tự đọc settings / tự tạo client). Điều mới: ba chỗ ghim lặp của cùng một sự thật. Đề xuất: lấy từ một
  nguồn (spec model / settings). Kiểm: build thử như B-02.

### B-07 — nhánh phòng xa không có đường chạy (thấp)
- `embedding/full_corpus.py:203-210, 240`: nhánh `cuda` + float16 — không spec nào có `device="cuda"` (`DENSE_MODEL_SPECS:41-66`).
- `vectorstore/qdrant.py:84-142`: trạng thái `empty` được `require_fresh_full_corpus_target` chấp nhận, nhưng caller duy nhất
  (`full_corpus_pipeline.py:186`) chỉ cho `absent`.
- `scoring/bm25.py:19-90` lớp `BM25`: production chỉ dùng `tokenize`, `K1`, `B`; lớp chỉ `tests/test_bm25.py`, `test_full_corpus_sparse.py`
  dùng (làm "đáp án" để so sparse — có giá trị test, nhưng là bản thứ hai của công thức trong `embedding/sparse.py:64-135`).
- `embedding/full_corpus.py:125-186`: hai hàm kiểm vector (`validate_vectors` vòng Python, `validate_vector_matrix` numpy) cùng việc.
- Đề xuất: gỡ khi đụng file đó; không mở việc riêng.

### B-08 — câu hỏi đầu tiên chậm thêm ~1 s (thấp; giả thuyết)
- Đo (`/tmp/b25/startup.py`, CPU, chỉ đọc): import ~4,4 s; discover + hash 205 file 0,02 s; nạp sparse state 0,004 s; nạp e5 2,45 s;
  **câu đầu** `embed_queries` 1,05 s, các câu sau ~15 ms; `encode_sparse_query` 0,27 ms (dựng lại bảng từ vựng mỗi câu — không đáng kể).
- *Giả thuyết*: một câu "làm nóng" lúc khởi động bỏ được ~1 s ở câu đầu của người dùng. Cách thử: đo độ trễ `/api/chat` câu đầu có / không
  làm nóng (không paid nếu chỉ đo tới bước tìm kiếm).

### B-09 — lệch chữ cấu hình (thấp)
- `docker-compose.yml:1` "Local Qdrant server for Hue Foods RAG MVP" (Foods đã gỡ).
- `config/logging.yaml` định nghĩa logger `ingestion`, `embedding`, `scoring`, `vector_database`, `llm`, `retrieval`, `reranking`,
  `evaluation`, `chat`; code dùng `getLogger("api")`, `"chat"`, `"llm.full_corpus"`, `__name__` (một chỗ), `"full_corpus_smoke"`,
  `"phase6_live_smoke"` ⇒ logger `api` và `__name__` khi import theo `backend.*` không vào handler file. Chưa kiểm hết tác động.

### B-10 — dependency không có `import` (chỉ ghi; User giữ thư viện thừa)
- `grep` import trong `backend/`, `notebooks/`, `frontend/`: 0 file cho `beautifulsoup4`, `polars`, `pyarrow`, `scikit-learn`, `nltk`,
  `gradio`, `python-dotenv`, `requests`, `python-multipart`; nhóm `evaluation` `underthesea` 0. `sentencepiece` không import trực tiếp
  nhưng cần cho tokenizer M2 (8.1). `pytest`, `pytest-cov`, `jupyter`, `ipykernel` nằm ở dependency chính thay vì nhóm dev.

## Không rà được / chưa chắc

- B-01: tác động 500 / 503 là *suy ra* từ code + kiểm lớp lỗi; chưa tái tạo bằng lỗi thật (không được tắt Qdrant / sửa kho). Có thể tái tạo
  không phá: gọi `search` với client trỏ collection không tồn tại trong một app thử ở port khác — cần A duyệt.
- Phần "chưa rà" ở đầu file. Hai sub-agent bị dừng giữa chừng, không có kết quả.
- Không chạy build index (cần quyền ghi Qdrant).
