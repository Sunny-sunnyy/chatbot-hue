# Rà code Phase 0–7 — luồng dựng index + nền (B25)

**XONG — chờ kiểm chéo (C kiểm top 5).** Người làm: B (Claude Opus 5.5) · bắt đầu 2026-10-25 chiều (terminal `hue-rag-de`), làm tiếp tối
(terminal `hue-rag-c3`), chốt **2026-10-25 18:39 +0700** (`date`) · chỉ đọc, **0 USD** · rà trên `main` **`1e8cf8f`** (phần rà chiều trên `bc568f1`;
`git diff --stat bc568f1..HEAD -- backend notebooks guides frontend pyproject.toml docker-compose.yml` rỗng ⇒ code không đổi). Code B1 ở nhánh
`p82-b1`, không rà ở đây. **Chỉ đề xuất, chưa sửa** (User 18:3x): mục có nhiều cách sửa ghi phương án + cách so sánh, không kết luận.

- **Đã rà (B tự đọc):** `backend/ingestion/` (`full_corpus_pipeline.py`, `source_state.py`, `preview.py`, `chunking/full_corpus_chunker.py`,
  `chunking/markdown_blocks.py`), `embedding/full_corpus.py`, `embedding/sparse.py`, `scoring/bm25.py`, `vectorstore/` (`qdrant.py`, `points.py`,
  `upsert.py`), `core/` (`settings_loader.py`, `schema.py`, `logging_setup.py`), `config/` (`settings.yaml`, `logging.yaml`,
  `full_corpus_conditions.json`), `backend/scripts/`, `pyproject.toml`, `docker-compose.yml`. Quét code thừa bằng AST + grep (`/tmp/b25/usage.py`);
  đo khởi động (`/tmp/b25/startup.py`); đếm đoạn vượt token toàn kho (`/tmp/b25/oversize.py`), input nhỏ (`/tmp/b25/oversize_unit.py`), khối Markdown
  bị bỏ / mục con chồng (`/tmp/b25/dropped*.py`).
- **Qua sub-agent (B kiểm lại 2–4 khẳng định chính mỗi cái bằng file thật — ✔ trong finding):** SA1 guide `phase_0`–`phase_2` + `guides/README.md`;
  SA2 guide `phase_3`, `phase_4` + phần index `full_corpus_rag.md`; SA3 test (`test_bm25`, `test_full_corpus_chunker`, `_embedding`,
  `_qdrant_ingestion`, `_sparse`, `test_phase6_settings`, `conftest`) + notebook 03, 04. Chi tiết từng dòng (private):
  `data/ra_soat_code/sa{1,2,3}_*.md`. SA2 có gọi một lệnh scroll Qdrant (POST, chỉ đọc) ngoài brief "chỉ GET" — không ghi gì.
- **Test đã chạy (SA3):** 6 file luồng index, liệt kê file, không paid / không ghi Qdrant: **97 passed in 115,43 s**; một test chiếm 101,65 s.
- ~~`scripts/` không tồn tại~~ — **sai, B tìm ở gốc repo** (C báo 25/10 tối): `backend/scripts/` có 2 file tracked ⇒ B-13.
- **B-04 phiên chiều có một câu sai** ("`chunk_full_corpus` đã fail-closed" việc chặn đoạn vượt token) — B và SA3 tìm độc lập ⇒ B-11.

## Top 10 (theo mức: tác động × rủi ro khi để nguyên)

| # | id | Mức | Một dòng |
|---:|---|---|---|
| 1 | B-01 | **cao** | Cùng một module nạp hai lần (`core.schema` và `backend.core.schema`) ⇒ API bắt sai lớp lỗi: lỗi Qdrant khi đang hỏi ra 500 thay 503; corpus đổi lúc khởi động ra 503 thay 409 |
| 2 | B-11 | **cao** | Build không chặn đoạn vượt giới hạn token (e5 cắt im lặng ở 512); test "chặn" chỉ kiểm bản sao trong CLI preview + một file kết quả tĩnh từ 09/2026 ⇒ PASS bất kể code. Hôm nay 0 / 8.459 vượt, nhưng sắp build lại với kho sửa |
| 3 | B-12 | vừa | Repo public chứa nguyên văn kho: `config/full_corpus_conditions.json` (5.324 ký tự) + 7 test mẫu của chunker — lệch luật dữ liệu §5 (A / User quyết) |
| 4 | B-16 | vừa | Guide phase 0–4 + `guides/README.md` tả hệ thống Foods / 4 collection / profile đã gỡ như đang chạy; không trỏ tới code chunker / index hiện hành |
| 5 | B-20 | vừa | Test luồng index: so "khớp build record" chỉ bằng số đoạn (không so identity); ~một nửa thời gian test dành cho CLI preview lịch sử; ghim hằng số kho |
| 6 | B-17 | vừa | Lệnh trong guide / notebook thiếu `uv run` / `--env-file`; `pytest tests/ -q` trong guide chạy cả test cần key OpenAI (có `POST /api/chat` thật) |
| 7 | B-18 | vừa | Không có quy trình "build lại index khi kho đổi" (xóa collection + record + sparse state chung) trong guide — cần ngay cho đợt build lại |
| 8 | B-03 | vừa | `settings_loader` ghim cứng mọi giá trị sinh câu trả lời ⇒ `settings.yaml` thành bản sao hằng số; đổi một tham số phải sửa 2–3 chỗ |
| 9 | B-04 | vừa | `ingestion/preview.py` trộn hàm đếm token production + CLI "Wave 1 preview" lịch sử; chunker ↔ preview import vòng. **Phụ thuộc B-11** |
| 10 | B-02 | vừa | Kiểm hợp lệ chồng lớp khi build điểm Qdrant: cùng chunk được kiểm + mã hóa sparse hai lần |

Các finding còn lại: B-21 (vừa — notebook 04 một cell năm việc), B-05, B-06, B-07, B-08, B-09, B-13, B-14, B-15, B-19 (thấp), B-10 (chỉ ghi).

**Gợi ý thứ tự nếu User chọn sửa** (đề xuất, không kết luận): B-11 trước mọi lần build lại index (nhỏ, chặn rủi ro thật) → B-01 (bug HTTP thật,
chạm nhiều file) → B-18 + B-16/B-17 (tài liệu cho đợt build lại) → các mục dọn (B-02, B-04, B-14, B-15, B-20) gộp **một** lần sửa chunker / build lại,
kiểm bằng "danh sách sha đoạn toàn kho giống hệt". B-12, B-13, B-03 là câu hỏi cho User trước.

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
- Phương án (A / User chọn; sửa nhiều file):
  (a) **chỉ `backend.*`** ở mọi nơi; `app.py` / `conftest.py` chỉ chèn gốc repo vào `sys.path` — khớp harness 8.1, notebook, CLI build
  (`python -m backend.ingestion…`), nhưng lệnh API / pytest đang chạy từ `backend/` phải đổi; (b) **chỉ `core.*` / `retrieval.*`** (chạy từ
  `backend/`) — lệnh API / pytest giữ nguyên, nhưng harness / notebook / CLI build (import `backend.*`) phải đổi; (c) giữ mẫu kép, chỉ sửa
  `chat.py` / `app.py` bắt lỗi theo cùng nguồn với `retrieval` — ít file nhất nhưng giữ gốc lỗi (lần sau lại hụt ở chỗ khác).
  So sánh: (1) số module nạp đôi trong `sys.modules` sau `import api.app` và sau một lượt pytest (trước: > 0; đích: 0); (2) số file / lệnh trong
  guide, notebook, harness phải đổi (đếm bằng `grep`); (3) T1 retrieval giống byte (không đổi kết quả); (4) tái tạo 503 / 409 bằng app thử.
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
  Quyết định thiết kế ⇒ A / User. So sánh: số chỗ phải sửa để đổi một tham số (B1 hôm nay: 3) — đếm lại bằng một thay đổi thử trên worktree;
  cái gì chặn giá trị sai (a: code review; b: kiểm kiểu + khởi động API). Kiểm khi sửa: test settings + khởi động API + T1 byte.
  Liên quan (SA3-08): `OPENAI_GENERATION_MODEL` (`llm/openai_tokenizer.py:5`) không nơi production nào dùng, chỉ test ghim (phạm vi C).

### B-04 — `ingestion/preview.py` trộn hàm production và CLI lịch sử (vừa)
- Vị trí: `preview.py:52-118` (`resolve_local_model_path`, `load_tokenizers`, `count_tokens_for_chunk` — chunker production dùng qua
  lazy import ở `full_corpus_chunker.py:302-310`); `preview.py:121-342` (`partition_for_source` "seven P7 partitions",
  `generate_preview`, `main`, mặc định ghi `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`).
- Loại: 1 + 2. Quan sát: `generate_preview` / `partition_for_source` / `main` không có nơi gọi production (AST + grep: chỉ
  `tests/test_full_corpus_chunker.py:50-52, 886, 933, 1037`, và prompt lịch sử trong `handoff_prompt/`); `reports/` là lịch sử, không thêm
  file (`WORKFLOW.md` §6). Chunker ↔ preview import vòng, phải lazy import.
- Đề xuất: chuyển 3 hàm tokenizer sang module của chunker (hoặc `ingestion/tokenizers.py`), CLI preview + test của nó: giữ hay xóa — A / User
  chọn (giá trị duy nhất: kiểm "không đoạn nào vượt token" toàn kho). **Sửa (phiên tối):** câu cũ "`chunk_full_corpus` đã fail-closed
  điều đó" **sai** — chunker không báo lỗi khi đoạn cuối vượt giới hạn, CLI preview là chỗ duy nhất kiểm ⇒ xem B-11; bỏ CLI thì phải
  chuyển phép kiểm đó vào luồng build trước. Phương án sau B-11: (a) bỏ CLI + test của nó, 3 hàm tokenizer sang module riêng; (b) giữ CLI như
  công cụ báo cáo, chỉ tách 3 hàm tokenizer (hết import vòng). So sánh: thời gian 6 file test (hôm nay 115 s, một test 101,65 s — SA3-02 ước ~một nửa
  là phần preview); có ai cần báo cáo phân bố đoạn toàn kho cho đợt build lại không (A hỏi).
  Kiểm khi sửa: danh sách chunk sha giống hệt (8.459), T1 byte.

### B-05 — hàm freshness cũ không còn dùng (thấp)
- `ingestion/source_state.py:99-133` `verify_build_record_freshness` đọc `build_record["sources"]` (schema cũ); AST: không gọi trong file,
  `grep` ngoài: chỉ `tests/test_full_corpus_chunker.py:63`. Bản runtime: `verify_full_corpus_record_freshness` (`:217`, đọc
  `corpus.sources`) — cùng logic. **Sửa (SA3-09 ✔):** test chỉ **import**, không gọi ⇒ 0 lời gọi ở đâu cả (`grep -rn` chỉ ra dòng `def` và dòng
  import). Test chunker còn ~15 import thừa khác (SA3 đếm, B chưa đếm lại). Đề xuất: xóa hàm cũ + dòng import. Kiểm: grep 0 nơi gọi; test thuần đạt.

### B-06 — ghim lặp hằng số ở luồng build (thấp; đã biết một phần)
- `full_corpus_pipeline.py:96-103` ghim `url == "http://localhost:6335"`, `timeout == 30` (đã có trong `settings.yaml:36-38`);
  `:66-69` tên collection theo candidate; `vectorstore/qdrant.py:30` `dimension not in {384, 4096}` (đã có trong `DENSE_MODEL_SPECS`).
- Đã biết: bảng G5 §4 dòng Ingestion (tự đọc settings / tự tạo client). Điều mới: ba chỗ ghim lặp của cùng một sự thật. Đề xuất: lấy từ một
  nguồn (spec model / settings). Kiểm: build thử như B-02. Thêm (SA3 ✔): `FULL_CORPUS_BATCH_SIZE = 64` định nghĩa hai lần (`points.py:24`,
  `upsert.py:19`); notebook 04 ghim lại timeout 30.

### B-07 — nhánh phòng xa không có đường chạy (thấp)
- `embedding/full_corpus.py:203-210, 240`: nhánh `cuda` + float16 — không spec nào có `device="cuda"` (`DENSE_MODEL_SPECS:41-66`).
- `vectorstore/qdrant.py:84-142`: trạng thái `empty` được `require_fresh_full_corpus_target` chấp nhận, nhưng caller duy nhất
  (`full_corpus_pipeline.py:186`) chỉ cho `absent`.
- `scoring/bm25.py:19-90` lớp `BM25`: production chỉ dùng `tokenize`, `K1`, `B`; lớp chỉ `tests/test_bm25.py`, `test_full_corpus_sparse.py`
  dùng (làm "đáp án" để so sparse — có giá trị test, nhưng là bản thứ hai của công thức trong `embedding/sparse.py:64-135`). **Sửa (SA3-13 ✔):**
  notebook 03 cũng dùng lớp `BM25` (`03_embedding_models.ipynb` dòng JSON 103, 119) để minh họa ⇒ không phải "chỉ test".
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

### B-11 — luồng build không chặn đoạn vượt giới hạn token; test chặn là PASS giả (cao)
- Khâu: chia đoạn → embedding. Vị trí: `full_corpus_chunker.py:402` (bảng không tách được / hàng đơn), `:423-445` (từng hàng không kiểm
  lại), `:490-512` (từng mục con không kiểm lại), `:567-580` (khối không tách câu được), `:585` (nhóm luôn nhận câu đầu dù câu đó đã vượt);
  `full_corpus_pipeline.py:126-128` chỉ dừng khi `errors` của chunker khác rỗng.
- Loại: 1 + 3 (khâu kiểm nằm sai chỗ). Quan sát:
  - Input nhỏ (`/tmp/b25/oversize_unit.py`, bộ kiểm giả "≤ 60 ký tự" chỉ để thử logic): một câu dài ⇒ 1 đoạn vượt, `errors == []`; bảng có
    một hàng dài ⇒ 2 đoạn, 1 vượt, `errors == []`.
  - Kiểm token duy nhất trên đoạn cuối nằm ở CLI `preview.py:195-205` (B-04: không đường production nào gọi). `grep max_tokens` trong
    `ingestion/`, `embedding/`, `vectorstore/`: không có phép kiểm nào khác sau chunker.
  - Kho hiện tại (`/tmp/b25/oversize.py`, chunker production + 3 tokenizer, offline): 8.459 đoạn, **0 vượt**; lớn nhất e5 366 / 512,
    huydang **255 / 256**.
  - **Test (SA3-01, tìm độc lập, cùng kết luận ✔):** 2 test "oversized / error preview" (`test_full_corpus_chunker.py:852-940`) gọi
    `generate_preview` ⇒ kiểm hàm kiểm token **riêng của preview** (`preview.py:150-165`), không phải checker production
    (`full_corpus_chunker.py:302`); `test_canonical_preview_pass` (`:945-973`) đọc file tĩnh
    `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json` (`status == "PASS"`, `oversized_groups_count == 0`) ✔ — file có 8.460 đoạn,
    record hiện hành 8.459 ⇒ PASS bất kể code / kho hôm nay.
- *Suy ra*: kho đổi (đợt build lại index đã có 139 mục C32 chờ sửa) có thể sinh đoạn vượt mà build vẫn xanh; e5 (SentenceTransformer) cắt
  im lặng ở 512 ⇒ vector dense chỉ phản ánh phần đầu, BM25 vẫn thấy đủ ⇒ lỗi tìm kiếm khó lần ra.
- Đề xuất nhỏ nhất: trong `chunk_document`, khi phát một đoạn mà `is_fits_tokenizer_fn(search_text)` sai thì thêm vào `errors` (checker đã có
  sẵn, đã cache) ⇒ build fail-closed như mọi lỗi chunker khác. Không cần CLI preview cho việc này nữa. Đổi 2 test synthetic sang gọi
  `chunk_document` (bỏ `generate_preview`); bỏ `test_canonical_preview_pass` (kiểm file tĩnh, không kiểm code).
- Cách kiểm khi sửa: 2 input nhỏ trên ra lỗi; toàn kho vẫn 8.459 đoạn, 0 lỗi, danh sách sha đoạn giống hệt (chunker không đổi đầu ra);
  6 file test luồng index đạt.
- Rủi ro: thấp (chỉ thêm lỗi; đầu ra kho hiện tại không đổi).

### B-12 — file tracked chứa nguyên văn đoạn kho (vừa; ranh giới dữ liệu — A / User quyết)
- Vị trí: `backend/config/full_corpus_conditions.json` (tracked từ `071b113`, 2026-09-12; repo `chatbot-hue` public); và
  `backend/tests/test_full_corpus_chunker.py:549-848` — 7 test mẫu ghim câu / địa chỉ / giá / heading nguyên văn của kho (SA3-04; chưa đếm ký tự).
- Quan sát (chỉ đếm, không in): 3 rule, 6 target, 2 file kho (domain `travel`); 9 selector `exact_text` = **5.324 ký tự nguyên văn** của kho
  (dài nhất 1.050). `Session_Prompt.md` §5: `knowledge-base-hue/` private, không commit nội dung.
- *Suy ra*: không phải bí mật (nguồn là trang công khai), nhưng lệch luật dữ liệu của dự án và hook `.githooks/pre-commit` không bắt được kiểu
  này. Đồng thời ghép cứng cấu hình ↔ câu chữ kho: sửa một chữ ở 9 đoạn đó là build dừng (fail-closed — đúng ý, nhưng phải sửa cả JSON).
- Phương án (A / User chọn): (a) để nguyên, ghi nhận; (b) chuyển file sang chỗ private (`knowledge-base-hue/meta/`) và
  `full_corpus.conditions_file` trỏ tới đó; (c) selector bằng hash đoạn thay cho văn bản. Với test: (a') để nguyên; (b') test mẫu chỉ giữ phần
  cấu trúc (vai trò condition / header, lát cắt khớp, hai ý tách hai đoạn), bớt chuỗi nguyên văn. Gỡ khỏi lịch sử git là thao tác phá hủy — chỉ khi
  User yêu cầu. So sánh phương án: không phải thí nghiệm chất lượng — tiêu chí là (1) số ký tự nguyên văn kho trong file tracked (đếm trước / sau),
  (2) danh sách sha đoạn toàn kho giống hệt, (3) test vẫn bắt được lỗi cũ mà nó bảo vệ (thử bằng input nhỏ, không sửa kho).

### B-13 — `backend/scripts/`: 2 converter dùng một lần, chép code của nhau (thấp)
- Vị trí: `backend/scripts/convert_huegov_culture_raw_to_md.py` (615 dòng), `convert_huegov_department_raw_to_md.py` (352 dòng); chỉ có ở
  `2830f58` (initial commit, 2026-08-05).
- Quan sát: đọc `backend/data/<nguồn>/raw` (8 MB, gitignored) ⇒ ghi `knowledge-base-hue/_source-dumps/` — thư mục mà discovery **loại**
  (`settings.yaml:14-16` `exclude_parts`). 14 hàm trùng tên giữa hai file (`comm` danh sách `def`: `slugify`, `render_record`, `frontmatter`,
  `main`…). Đường dẫn tương đối ⇒ chỉ chạy đúng khi cwd là gốc repo. `grep` trong `backend/`, `guides/`, `notebooks/`, `pyproject.toml`:
  không nơi nào gọi / nhắc.
- *Suy ra*: công cụ lịch sử của bước raw → source dump, không nằm trên đường raw → curated → chunk đang chạy.
- Phương án (A / User chọn): (a) giữ nguyên + một dòng trong guide "lịch sử, không chạy lại"; (b) chuyển ra khỏi `backend/` (ví dụ
  `data/tools/` private, cùng chỗ với raw 8 MB); (c) xóa (git còn lịch sử). Không gộp hai file (không ai chạy lại). So sánh: có cần tái tạo
  `_source-dumps` từ raw không (User biết) — nếu không, (b)/(c) bớt 967 dòng khỏi phạm vi rà code mà không đổi hành vi nào (grep 0 nơi gọi).

### B-14 — chunker / parser: kiểm chồng, trạng thái chết, dữ liệu tính hai lần (thấp)
- `ConditionManager` (~165 dòng, `full_corpus_chunker.py:114-296`) cho **3 rule / 6 target**: `validate_corpus_rules` (`:171-223`) và
  `validate_and_resolve_for_doc` (`:225-296`) cùng kiểm "khớp đúng một khối" ⇒ một selector hỏng bị báo **hai lần**, và lượt hai đánh số rule
  theo chỉ số trong file (`:244`), khác lượt một (chỉ số toàn cục `:184`).
- `markdown_blocks.py:126-127, 179, 198, 234, 238`: `in_table` / `in_blockquote` bật rồi tắt trong cùng một nhánh ⇒ ở `:316` luôn `False`.
- `ListItemInfo.parent_start/end/text` (`markdown_blocks.py:283-290`) chỉ test đọc (`test_full_corpus_chunker.py:229-230`); chunker tự tính lại
  nhãn cha theo cách khác (`full_corpus_chunker.py:481-483`, `rstrip`) ⇒ hai định nghĩa "nhãn cha". `ParsedDocument.lines / offsets`: không ai
  đọc ngoài parser (`grep`).
- Kiểm lát cắt nguồn sau khi dựng (`markdown_blocks.py:335-353`, `full_corpus_chunker.py:630-639`): văn bản vốn lấy từ chính lát cắt ⇒ luôn đúng
  (rẻ, giữ hay bỏ đều được).
- `is_fits_tokenizer_fn is not None` kiểm sau khi đã gán mặc định (`:399, 463, 529, 600`) ⇒ luôn đúng; import thừa `point_id_for_chunk_id`,
  `load_settings` (`:15-16, 29-30`); 7 bản chép khối dựng `FullCorpusChunk(...)` (`grep -c`); docstring "Wave 1" (`:1`).
- Đề xuất: dọn cùng lần sửa chunker khi build lại index (bảng G5 §3 dòng 8 "dọn chunker"); một hàm dựng đoạn; một lượt kiểm selector.
  Kiểm: danh sách sha đoạn toàn kho giống hệt.

### B-15 — mục con lồng ≥ 3 cấp bị lặp khi mục cha phải tách (thấp, tiềm ẩn)
- `markdown_blocks.py:260-270`: mọi `list_item_open` sâu hơn cấp 1 đều vào `sub_items` ⇒ mục cấp 3 nằm cả trong mục cấp 2 chứa nó lẫn thành mục
  riêng ⇒ nếu khối cha quá dài phải tách (`full_corpus_chunker.py:490`), văn bản cấp 3 xuất hiện ở hai đoạn.
- Kho hiện tại (`/tmp/b25/dropped2.py`): 7 mục cấp ≥ 3; **1** khối có `sub_items` chồng nhau, khối đó **không** phải tách ⇒ 0 tác động hôm nay.
- Liên quan đã biết: 3 cặp đoạn lặp do blockquote lồng trong list item (`Project_Status.md` §4, B8); code fence bị bỏ (inventory 8.1 §3 dòng
  0.7, G3 S2) — B đếm lại khớp: 2 fence cấp khối, cùng domain, ngoài mục "Nguồn dữ liệu".
- Đề xuất: chỉ lấy mục con trực tiếp (cấp 2); làm cùng lần dọn chunker. Kiểm: sha đoạn toàn kho giống hệt.

### B-16 — guide phase 0–4 + `guides/README.md` tả hệ thống đã gỡ như đang chạy (vừa)
- Nguồn: sub-agent SA1 (phase 0–2 + README), SA2 (phase 3–4 + phần index `full_corpus_rag.md`); chi tiết từng dòng ở
  `data/ra_soat_code/sa1_guides_phase0_2.md`, `sa2_guides_phase3_4_index.md` (private vì có đường dẫn ngoài repo). B tự kiểm lại 6 khẳng định
  (đánh dấu ✔).
- Loại 5. Quan sát (gom theo kiểu):
  - **File / lệnh không còn** ✔: `phase_2_foods_markdown_chunking.md:153-160` ("Files canonical": `helpers/split_text.py`,
    `chunking/markdown_chunker.py`, `test_markdown_chunker.py`, notebook 02 — `ls` không có, gỡ ở `1832201`) và lệnh kiểm `:306-311`;
    `phase_4_qdrant_ingestion.md:449-455` (`vectorstore/reset.py`, `ingestion/pipeline.py`, `test_qdrant_schema.py`, `test_ingestion_pipeline.py`
    — không có); `phase_1_backend_skeleton.md` giao sửa `ingestion/pipeline.py`, `evaluation/evaluator.py` (không có).
  - **Hiện trạng sai** ✔: `phase_0_mvp_foundation.md:100-101` "Collection hiện hành: `hue_foods_e5_small_384`, 572 points";
    `README.md:21` "Phase 4 collections là read-only" (đã xóa); `phase_4_qdrant_ingestion.md:40, 55-58` 8.460 chunk + 4 collection
    `hue_full_corpus_a_*` (`grep -rn hue_full_corpus_a_ backend` = 0); port 6333 (`:224, :332`) — code ép 6335 (`full_corpus_pipeline.py:99`).
  - **Cấu hình / schema cũ**: `phase_1:83-116`, `phase_0:160-172` bắt `load_settings()` kiểm `active_profile` / `profiles` — thực tế 4 nhóm
    `full_corpus`, `full_corpus_generation`, `full_corpus_runtime`, `vector_database`; model `gpt-5.4-*` thay `gpt-6-luna`; 3 profile cũ thay
    `dense_bm25_rrf`; phase 3 tả 4 dense candidate (có Qwen3-0.6B CUDA), code còn 2; payload "năm field" (thực tế 7; `full_corpus_rag.md:182` gọi
    năm field là "hiện hành"); sparse state `phase_3_sparse_state.json` (thật: `full_corpus_sparse_state.json`).
  - **Không trỏ tới code đang chạy**: cả 4 guide phase 0–2 + README không nhắc `full_corpus_chunker.py`, `markdown_blocks.py`, `source_state.py`;
    README dừng ở 2026-10-01 (Phase 6 `implementation_active`, không có 7A–8.2; còn vai "Codex Reviewer", report vào `reports/`).
  - Các đoạn có nhãn lịch sử rõ (ví dụ "Foods as-built history") **không** tính là lỗi, nhưng heading đó rỗng và mục con cùng cấp ⇒ nhãn yếu.
- *Suy ra*: người / agent mới đọc guide theo `README.md` sẽ đi theo kiến trúc Foods (collection, profile, file) đã gỡ; nguồn đúng hiện chỉ
  nằm ở `Project_Status.md` §4 và mục "Cập nhật 7A2 / 7B" đầu `full_corpus_rag.md`.
- Phương án (A / User chọn; không phải thí nghiệm chất lượng — đo bằng "số tham chiếu chết" trước / sau):
  (a) **banner lịch sử** đầu mỗi guide phase 0–4 ("tả hệ thống Foods / thiết kế 09/2026; hiện hành: `full_corpus_rag.md` + `Project_Status.md`
  §4") + sửa `README.md` — nhỏ nhất; (b) viết lại phần "hiện hành" của từng guide theo code; (c) chuyển phase 0–4 vào `guides/history/`, README
  chỉ trỏ guide hiện hành. Cách kiểm: script quét mọi đường dẫn `backend/…` / tên collection / lệnh trong guide **ngoài** đoạn có nhãn lịch sử ⇒
  0 đường dẫn không tồn tại (đếm hôm nay để có số trước).

### B-17 — lệnh trong guide / notebook thiếu `uv run` / `--env-file`, hoặc chạy cả test cần key OpenAI (vừa)
- `full_corpus_rag.md:114-115` lệnh build `python -m backend.ingestion.full_corpus_pipeline build --candidate <id>` (thiếu `uv run`, thiếu
  `--env-file .env` mà candidate 8B OpenRouter cần) ✔; cùng lệnh lặp ở `notebooks/03_embedding_models.ipynb` (SA2).
- `phase_2:309` `uv run python -m pytest tests/ -q`: chạy cả `test_api_chat.py` (3 test `require_openai_key`, một test `POST /api/chat` thật
  `:86-93`), `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py` ✔ (`grep -ln require_openai_key tests/`). Có tốn tiền thật hay
  chỉ fail khi thiếu key: **chưa đo** (không chạy — luật paid). Mâu thuẫn `Project_Status.md` §8 (liệt kê file, không chạy cả thư mục).
- Đề xuất: sửa lệnh theo `Session_Prompt.md` §10 + `Project_Status.md` §8 (một dòng mỗi chỗ). Kiểm: `grep -n "python -m" guides/*.md
  notebooks/*.ipynb | grep -v "uv run"` = 0.

### B-18 — guide không nói cách build lại khi corpus đổi (vừa)
- SA2-02: build lại cùng candidate cần xóa collection + build record + sparse state chung (`Project_Status.md` §8 bẫy "sparse state chỉ ghi một
  lần"), code không có lệnh reset (`build_candidate` "không ghi đè", `full_corpus_pipeline.py:149-160`); guide phase 4 / `full_corpus_rag.md`
  không có quy trình này. SA2-05 / SA2-06: guide còn dạy target "absent hoặc empty" (code chỉ nhận absent — phía code là B-07) và mẫu kiểm 12 point
  Phase 3 (thật: chunk đầu mỗi domain, `full_corpus_pipeline.py:172-175`).
- *Suy ra*: đợt build lại index (C32 139 mục kho, B-11, B-14, B-15) sẽ phải tự dò lại quy trình — đúng chỗ đã gây bẫy trước đây.
- Đề xuất: một mục "Build lại index khi corpus đổi" trong `full_corpus_rag.md` (các bước, quyền ghi / xóa cần duyệt, sao lưu snapshot trước);
  không thêm CLI reset (xóa là việc cần User duyệt, để thao tác tay có kiểm). Kiểm: lần build lại tới làm đúng theo mục đó, ghi chỗ lệch.

### B-19 — linh tinh guide / logging (thấp)
- SA1-03: guide nói 3 entrypoint gọi `setup_logging()`; thực tế chỉ `api/app.py:43`; ingestion dùng `basicConfig`
  (`full_corpus_pipeline.py:271`) ⇒ `config/logging.yaml` chỉ áp cho API (bổ sung B-09).
- 7 guide chứa **48** đường dẫn tuyệt đối tới một repo khác trong home của User (`grep -oh "/home/minhhieu/[^/]*" guides/*.md`), phần lớn ở
  `llm_rag_reference_for_hue_rag.md` (phạm vi C); hook pre-commit không chặn mẫu đường dẫn home. *Có thể* trùng câu hỏi User mục 6 trong
  `CURRENT_HANDOFF.md` (tên dự án khác trong file đã commit) — A đối chiếu.
- SA2-11: mục "Tài liệu hiện hành" của `full_corpus_rag.md` không trỏ spec 7A2 / build record v3.

### B-20 — test luồng index: kiểm sai chỗ, chậm vì CLI lịch sử, ghim hằng số kho (vừa)
- Nguồn: SA3-02, -03, -04, -05 (`data/ra_soat_code/sa3_tests_notebooks_index.md`); B kiểm lại ✔ phần identity.
- **Không so identity** ✔: `test_full_corpus_determinism_and_preview_byte_equality` (`test_full_corpus_chunker.py:978-1048`) — docstring "chunks match
  the runtime build record" nhưng chỉ `len(chunks) == record["corpus"]["chunk_count"]` (`:993, :997`). Runtime không chia lại lúc khởi động (chỉ so hash
  file nguồn + sparse state) ⇒ đổi code chunker mà vẫn ra 8.459 đoạn thì index cũ **không bị phát hiện ở đâu**. SA3 đo hôm nay:
  `compute_corpus_identity(chunks) == record` True, sparse state khớp byte ⇒ thêm assert là đạt ngay.
- **Chậm**: test đó 101,65 s / 115 s của 6 file; chạy chunker 4 lần (2 trực tiếp + 2 trong `generate_preview`) ⇒ ~một nửa là phần preview lịch sử
  (SA3 ước từ một lần chunk 21,8 s).
- **Ghim hằng số kho**: test discovery ghim 205 file + số file từng domain (`:69-106`) trong khi test determinism lấy số từ build record — hai nguồn
  cho cùng sự thật; sửa kho (C32) làm test đỏ dù code đúng; clone public không có kho ⇒ lỗi không có thông điệp rõ.
- Marker `live` đăng ký (`conftest.py:23-28`) nhưng 0 test dùng ⇒ không tách được test paid / Qdrant bằng `-m` (lý do `Project_Status.md` §8 phải
  liệt kê file).
- Đề xuất: (1) thêm assert identity (+ sparse bytes) — nhỏ, giá trị cao; (2) bỏ phần preview theo quyết định B-04; (3) discovery so
  `set(files) == set(record sources)`; (4) gắn `@pytest.mark.live` cho test cần key / Qdrant thật **hoặc** bỏ đăng ký marker — A chọn.
  Kiểm: chạy 6 file trên `main` ⇒ đạt; trên nhánh `p82-b1` (nếu đổi chunker) assert identity phải đỏ; `--durations` trước / sau.

### B-21 — notebook 04 một cell làm năm việc, chép luật của pipeline (vừa); notebook 03 lệch chữ (thấp)
- SA3-12: `04_qdrant_ingestion.ipynb` cell 3 chia lại toàn kho (~22 s, intro chỉ nói "đọc build record"), dựng mẫu bằng luật **chép** từ
  `full_corpus_pipeline.py:172-175`, kiểm freshness, gọi `validate_full_corpus_collection_info` rồi `verify_full_corpus_collection` (hàm sau đã gọi
  hàm trước — `upsert.py:86` ✔), `raise` như validator ⇒ trái `Session_Prompt.md` §11. Đạt: outputs rỗng, `execution_count: null`, port từ settings.
- SA3-13: notebook 03 cell 2 ghi "E5-base, HuyDang … đã bỏ khỏi code" — vẫn là tokenizer kiểm token của chunker (`settings.yaml:22-34`); cell 6 lệnh build
  thiếu `uv run` (B-17); 2 import thừa.
- Đề xuất: tách cell; đưa luật chọn mẫu thành một hàm trong pipeline để build và notebook gọi chung; sửa câu cell 2. Kiểm: Run All trên bản tạm
  (Qdrant chỉ đọc) ⇒ `point_count` 8.459; repo giữ outputs rỗng.

## Không rà được / chưa chắc

- B-01: tác động 500 / 503 là *suy ra* từ code + kiểm lớp lỗi; chưa tái tạo bằng lỗi thật (không được tắt Qdrant / sửa kho). Có thể tái tạo
  không phá: gọi `search` với client trỏ collection không tồn tại trong một app thử ở port khác — cần A duyệt.
- B-11: tác động "e5 cắt im lặng" là *suy ra* từ hành vi mặc định SentenceTransformer (`max_seq_length` 512), chưa đo vector của một đoạn vượt
  thật (kho hôm nay không có đoạn nào vượt).
- B-17: `pytest tests/ -q` có tốn tiền thật hay chỉ fail khi thiếu key — **NOT RUN** (luật paid).
- B-12: chưa đếm số ký tự nguyên văn kho trong test chunker; chưa quét các test khác (phạm vi C) theo cùng tiêu chí.
- Guide: B tự kiểm lại 6 khẳng định của SA1 / SA2 (✔); các dòng còn lại trong file sub-agent là của sub-agent, chưa kiểm từng dòng.
- Chưa rà: guide phase 5–9, `llm_rag_reference_for_hue_rag.md`, test / code luồng trả lời (phạm vi C34). Không chạy build index (cần quyền ghi
  Qdrant), không chạy notebook (chỉ đọc JSON).
- Ước "~một nửa thời gian test là phần preview" (B-20) là của SA3 từ một lần chunk đo riêng, chưa đo trực tiếp bằng cách bỏ phần đó.
