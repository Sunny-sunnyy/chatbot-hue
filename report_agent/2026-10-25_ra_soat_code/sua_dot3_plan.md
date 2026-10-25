# Plan: rà code — đợt 3 (gói 2 + gói 5 + B-12) — chạy **sau** khi gói 1b commit

Người viết: C (Claude Opus 5.5, terminal `hue-rag-7f`) · bản 1 2026-10-25 21:28, bản 2 21:31 (ghi 2 quyết định của A: `meta/` được, không fixture), **bản 3 21:50** (sửa theo `sua_dot3_plan_review.md` của B: M-1, m-1…m-6) · A giao 21:0x · **chỉ plan, chưa sửa code**, 0 USD.
Đếm trên `main` **`47a4e32`** bằng `git grep` / `git show` trên commit (working tree đang có sửa dở của gói 1b — không đọc). Người review: B (sau 1b).
Duyệt: A (sha vào `CURRENT_HANDOFF.md`, `WORKFLOW.md` §9.1).

## Căn cứ để review

| File | Mục cần đọc |
|---|---|
| `report_agent/2026-10-25_ra_soat_code/ra_soat_code_B.md` | B-02, B-04, B-05, B-06, B-07, B-09, B-11, B-12, B-13, B-14, B-15, B-18, B-20 |
| `report_agent/2026-10-25_ra_soat_code/ra_soat_code_C.md` | C-04, C-05, C-06, C-07, C-10, C-17, C-18, C-19; `sua_4_review.md` o1 (= C-21) |
| `session_prompt/CURRENT_HANDOFF.md` | "Luật chung mọi gói", "Cổng ổn định sau mỗi gói", User 19:4x mục (2) "gỡ code không dùng nếu không ảnh hưởng hệ thống", (4) public / private |
| Code tại `47a4e32` | `ingestion/chunking/full_corpus_chunker.py:344-642`, `ingestion/full_corpus_pipeline.py:137-215`, `ingestion/preview.py`, `retrieval/full_corpus.py:640-700, 820-840`, `llm/generator_openai_full_corpus.py:100-150, 250-265`, `tests/test_full_corpus_chunker.py:60-110, 850-1050` |

Mọi số tính lại được bằng `data/ra_soat_code_2026-10-25/tools/dot3_plan/usage.py <rev> <tên…>` (git grep trên commit; tách def / code / test /
harness / notebook) và `test_deps.py` (phân loại test theo phụ thuộc). **Số dòng sẽ lệch sau 1b:** 1b đổi khối import đầu các file `ingestion/`,
`retrieval/`, `embedding/`, `vectorstore/`, `reranking/`, `api/`, `tests/`, `conftest.py` (khối `try / except ModuleNotFoundError` ~5–45 dòng mỗi file
⇒ `retrieval/full_corpus.py` lệch nhiều nhất), gỡ `CrossEncoderReranker.rerank()` và nhánh 409 lúc hỏi trong `chat.py` (C-11). Người làm **tìm lại
theo tên hàm**, không theo số dòng; chạy lại `usage.py HEAD …` ngay trước mỗi lần gỡ. **Bảng số dòng sau 1b:** `sua_dot3_plan_review.md` §4 (B đo trên
working tree có 1b) — dùng bảng đó khi bắt đầu.

## 1. Mục tiêu và nguyên tắc

1. **Gói 2 — an toàn đường build:** chunker báo lỗi khi đoạn vượt token (B-11); test so **danh tính** đoạn với build record (B-20); build không
   ghi gì trước khi kiểm đích sạch (C-21); guide build lại khớp code sau sửa (B-18).
2. **Gói 5 — dọn code không dùng**, theo luật User 19:4x: **chỉ gỡ khi 0 nơi gọi** (code, CLI `python -m`, notebook, harness 8.1 trên `main`,
   harness 8.2 trên `p82-b1`, test) **và không đổi hành vi** (sha đoạn toàn kho, T1 retrieval, chuỗi gửi model, mã HTTP giữ nguyên). Mục có gọi
   động / chưa chắc ⇒ **giữ**, ghi lý do.
3. **B-12 — public / private:** nội dung kho ra khỏi file tracked (User 19:4x mục 4), không xóa lịch sử git.
4. Không đổi chất lượng: không mục nào là thí nghiệm; mọi mục phải cho đầu ra giống hệt (ngoại trừ B-11 thêm lỗi cho đầu vào mà kho hôm nay không có).

## 2. Gói 2

| Mục | Sửa (nhỏ nhất) | Test viết trước (đỏ trên `main`) | Bằng chứng không đổi hành vi |
|---|---|---|---|
| **C-21** | `build_candidate` (`full_corpus_pipeline.py:170`): dời `_write_or_check_sparse_state` xuống **sau** `require_fresh_full_corpus_target` (`:183-187`); sparse sha vẫn vào record như cũ | `test_full_corpus_qdrant_ingestion.py`: `build_candidate("e5-small-384", collection_name=<collection runtime>, sparse_state_path=tmp_path/…, record_path=tmp_path/…)` ⇒ raise `ValueError` với thông điệp **`"Target collection already exists"`** (`full_corpus_pipeline.py:186-187` — assert đúng lý do, để Qdrant tắt không thành xanh giả; điều kiện trước: Qdrant `:6335` có collection runtime, như T-C của 1b) **và** file sparse trong `tmp_path` **không** được tạo. Qdrant chỉ đọc (dừng ở bước kiểm đích, trước `create_collection`); chia kho ~20 s. Trên `main`: đỏ (file sparse đã ghi) | không chạy build thật (ghi Qdrant cần duyệt); đường đúng (đích `absent`) chỉ đổi thứ tự hai lệnh độc lập — đọc diff |
| **B-11** | Vòng "Verify each chunk" cuối `chunk_document` (`full_corpus_chunker.py:630-641`): `if not is_fits_tokenizer_fn(ch.search_text): errors.append(f"Chunk exceeds tokenizer limit: {ch.chunk_id}")`. Bỏ comment "so preview can detect it" (`:568`). Một chỗ kiểm cho mọi nhánh phát đoạn (bảng không tách, từng dòng, mục con, khối không tách câu, nhóm câu đầu) | `test_full_corpus_chunker.py`: thay 2 test synthetic gọi `generate_preview` (`:852-940`) bằng test gọi **`chunk_document` thật** + checker thật (3 tokenizer HF cache): (a) một câu 900 chữ không dấu chấm, (b) bảng có một hàng 900 chữ ⇒ `errors` có "exceeds tokenizer limit"; đối chứng 400 câu ngắn ⇒ 0 lỗi (đúng input C đã chạy ở `kiem_cheo_C.md` B-11: 906 / 927 token, `errors == 0` trên `main`) | kho: 8.459 đoạn, 0 lỗi, **sha danh sách đoạn giống hệt**; thời gian `chunk_full_corpus` trước / sau (thêm một lượt đếm token mỗi đoạn — ghi số giây) |
| **B-20** | Test, không sửa code: `test_full_corpus_determinism_and_preview_byte_equality` thêm `compute_corpus_identity(chunks) == record["corpus"]["identity"]` và `serialize(fit_sparse_state(chunks)) == bytes file sparse state` (dùng hàm ghi có sẵn, đọc file, không ghi). **Phần preview của test này cắt ở commit 3** (cùng lúc gỡ `generate_preview` — m-3), commit 4 chỉ thêm identity / sparse bytes / discovery. `test_full_corpus_discovery_and_inventory_exclusions` (`:69-106`): thay ghim 205 / số file từng domain bằng `set(files) == set(record["corpus"]["sources"])` | trên `main` hôm nay **xanh ngay** (C đo `kiem_cheo_C.md`: identity True) — test bảo vệ, không phải test đỏ; kiểm "biết đỏ": chạy trên nhánh `p82-b1` không được (B1 không đổi chunker) ⇒ thử bằng input nhỏ: identity của danh sách bỏ 1 đoạn ≠ record | `--durations` trước / sau (mốc C: test determinism 83,45 s / 42 passed 94,4 s) |
| **B-18** | Không sửa code. Sau C-21: `guides/full_corpus_rag.md` mục build lại — bỏ cảnh báo "build ghi sparse state trước bước kiểm đích" (B26, `:168-170` tại `1b9c126`), ghi "C-21 đã sửa ở `<sha>`"; lệnh build theo quy ước 1b (`cd backend && …`) — 1b đã sửa phần lệnh | — | đối chiếu từng gạch "Code làm gì" với code sau đợt 3 |

## 3. Gói 5 — bảng gỡ / giữ (đếm trên `47a4e32`; `p82-b1:backend/experiments/phase_8_2/` = 0 lời gọi cho **mọi** tên dưới — đã grep)

Cột "nơi gọi" = kết quả `usage.py` (ngoài dòng `def`). "CLI" = `python -m` trong tài liệu hiện hành (`guides/`, `session_prompt/`, `bao_cao_he_thong/`,
`AGENTS.md`, `skills/`, notebook): **0** cho mọi CLI dưới, **trừ** `parse-user-scores` còn 1 dòng ở `guides/full_corpus_rag.md:91` (m-1 — sửa ở C-07).

| Mã | Gỡ | Giữ (lý do) | Nơi gọi hôm nay | Rủi ro / cách kiểm |
|---|---|---|---|---|
| **C-19a** smoke Phase 5 | `retrieval/full_corpus_smoke.py` (548 dòng) + 3 test (`test_full_corpus_retrieval.py:354-430`: `validate_selectors`, `validate_safe_output_path`, `sanitize_error_detail`) | trace `data/full_corpus_phase_5_smoke_trace.json` (bằng chứng lịch sử, private) | `full_corpus_smoke`: chỉ 3 test; không CLI hiện hành; từ `backend/` còn hỏng import (S3-04) | thấp; `grep full_corpus_smoke` (trừ `golden_full_corpus_smoke`) = 0 |
| **C-06** nhánh `minilm` của service | `retrieval/full_corpus.py`: nhánh `elif self.reranker == "minilm"` trong `search` (`:649-693`), khối "5. MiniLM reranker" trong builder (`:825-834`), `RerankerMode` còn `"none"`, kiểm `reranker not in ("none","minilm")` ⇒ chỉ `"none"` | lớp `CrossEncoderReranker` (harness 8.1 g1 `:169` đếm token, g4_rerank — G4; test primitives `:186-206`); nhánh `native_hybrid_rrf` (g1 / g4_rerank / g4_keyword, E3a spec 8.2) | dựng service với `reranker="minilm"`: **chỉ** `full_corpus_smoke.py:86, 265-271` (gỡ ở C-19a); loader runtime đã cấm (`settings_loader.py:36`) | thấp; làm **sau** C-19a; T1 byte |
| **C-05** Representation B | `llm/representation_b.py` (34); `full_corpus_prompt.py` `REPRESENTATION_B_SYSTEM_INSTRUCTIONS`, `build_representation_b_messages`; generator `search_context_agent`, `SearchContextOutput`, `generate_search_context`, tham số `representation_b_max_output_tokens`; `settings.yaml:51` + `settings_loader.py:67-68` + `test_phase6_settings.py:20`; test Rep B trong `test_openai_full_corpus_generator.py` (`:54-56, 59-90, 109-125` phần SearchContext); **tài liệu hiện hành:** notebook 06 ô 0 (câu "Representation B: có trong code … runtime không dùng"), `guides/phase_6_generation_api.md` mục Hiện hành `:54`, `:79` ("Representation B cap 256", "một call Representation B") — sửa chữ cùng commit; A sửa `bao_cao_he_thong/BAO_CAO_SINH_CAU_TRA_LOI_API.md`, `BAO_CAO_CHIA_DOAN.md:136` và câu nhắc trong `guides/full_corpus_rag.md` nếu thuộc báo cáo User | — | `generate_search_context`: `phase6_live_smoke.py:351` (Attempt 1 — gỡ ở C-19b) + test; notebook 06 chỉ nhắc chữ (B26 đã ghi "runtime không dùng") | vừa (đụng settings + generator); chuỗi gửi model của câu trả lời **giống byte** (dùng lại `snap_3b.py` gói 3, 25 câu); `/health` vẫn 5 thành phần |
| **C-19b** smoke Phase 6 (giữ, bỏ phần thừa) | Attempt 1 Representation B (`phase6_live_smoke.py:336-375`; sau 1b `:328-`), "exact_five_attempts" ⇒ 4 câu; **`make_fits_all_checker`** (`:104`, chỉ gọi ở `:311` trong nhánh Attempt 1 — 0 nơi gọi sau khi gỡ; m-2) | **giữ file** — kiểm live duy nhất qua route HTTP; `evidence_recorder` (C-10) vì runner này dùng | `run_smoke_async`: CLI `main` + 6 test | thấp; test logic của file (không key) đạt; lượt paid 4 câu chỉ khi A duyệt |
| **C-10** recorder | `EvidenceRecorder.record_generation_success` (0 lời gọi), field `packed_text` (ghi, không ai đọc) | lớp + `record_evidence` + các nhánh `if recorder:` trong `chat.py` (runner Phase 6 dùng) | như trái | thấp |
| **C-04** + C-18 phần context | `retrieval/full_corpus_context.py:41-46` nhánh `apply_chat_template`; test hiển nhiên đúng `test_full_corpus_context.py:82-85, 88-93` | — | `apply_chat_template`: chỉ chính nhánh đó; mọi nơi dựng builder truyền tokenizer tiktoken | thấp; `input_tokens` 25 câu giống (snap_3b) |
| **C-07** | `parse_user_scores` + lệnh CLI `parse-user-scores` (`full_corpus_eval.py:689`, `:972`; sau 1b `:685`, `:877`, `:966`) + test `test_full_corpus_eval.py:187`; **dòng `parse-user-scores` trong danh sách CLI `guides/full_corpus_rag.md:91`** (m-1) | — | chỉ CLI chính nó + test + 1 dòng guide; User 15:44 25/10 "không chấm điểm" | thấp; `--help` còn 10 lệnh = guide |
| **B-04** CLI preview | `preview.py`: `partition_for_source`, `generate_preview`, `main` + test của chúng (`test_full_corpus_chunker.py` các test gọi `generate_preview`, `test_canonical_preview_pass` đọc file tĩnh) — **sau** B-11 (phép kiểm token đã vào chunker) | 3 hàm tokenizer `resolve_local_model_path`, `load_tokenizers`, `count_tokens_for_chunk` **tại chỗ** (chunker lazy-import; harness 8.1 `g3_chunking.py:46, 89, 94` import — không sửa harness 8.1 đã đóng); `reports/artifacts/…json` (lịch sử) | `generate_preview`: `main` + 5 dòng test; `partition_for_source`: chính nó + 2 test | thấp; sha đoạn giống; `g3_chunking` import được |
| **B-05** | `source_state.py:99-133` `verify_build_record_freshness` + dòng import ở `test_full_corpus_chunker.py:63` | `verify_full_corpus_record_freshness` (runtime) | chỉ 1 dòng import test | thấp |
| **B-07** | nhánh `cuda` / `float16` trong `embedding/full_corpus.py:203-210, 240` + `Literal["cpu","cuda"]` ⇒ chỉ CPU | trạng thái `empty` ở `vectorstore/qdrant.py` (phân loại đích, test dùng — không có lợi khi gỡ); `validate_vectors` **và** `validate_vector_matrix` (cả hai có code gọi: `:282, 381` / `:263, 374`, `points.py`); lớp `BM25` (test + notebook 03 dùng làm đáp án so sparse; harness g4_keyword) | không spec nào `device="cuda"` (`DENSE_MODEL_SPECS`) | thấp; e5 nạp CPU như cũ (`/health`) |
| **B-06** | `FULL_CORPUS_BATCH_SIZE` định nghĩa 2 lần (`points.py:24`, `upsert.py:19`) ⇒ một nơi | ghim URL / timeout trong `full_corpus_pipeline.py:96-103` (chặn build nhầm Qdrant khác — cố ý); `dimension in {384, 4096}` | — | thấp |
| **B-09** | `docker-compose.yml:1` "Hue Foods RAG MVP" ⇒ tên đúng; `config/logging.yaml` thêm logger `api` (code dùng `getLogger("api")`) | logger khác (đúng tên đang dùng) | — | thấp; cổng ổn định: log `api` ra đúng handler |
| **B-13** | `backend/scripts/` 2 converter (967 dòng) — **chép bản sao sang `data/tools/huegov_converters/` (private) trước**, rồi xóa khỏi repo | raw `backend/data/` (gitignored, không đụng) | 0 (grep `backend/`, `guides/`, notebook, `pyproject.toml`) | thấp; không ai chạy; git còn lịch sử |
| **B-14** | `full_corpus_chunker.py`: import thừa `point_id_for_chunk_id`, `load_settings` (`:15-16, 29-30`; sau 1b chỉ còn `:14-15`); **`REPO_ROOT` thừa ở `retrieval/full_corpus.py:68`** (0 nơi dùng; m-6 — gỡ ở commit 8); `is_fits_tokenizer_fn is not None` luôn đúng (`:399, 463, 529, 600`); 7 khối `FullCorpusChunk(...)` ⇒ một hàm dựng; `markdown_blocks.py` cờ `in_table` / `in_blockquote` bật-tắt trong cùng nhánh; docstring "Wave 1" | `ConditionManager` hai lượt kiểm (gộp đổi thông báo lỗi — không có lợi đo được, để nguyên); `ListItemInfo.parent_*` (có code đọc: `markdown_blocks.py:83, 349` — kiểm lát cắt); kiểm lát cắt sau dựng (rẻ) | — | vừa (chạm chunker) ⇒ **sha đoạn toàn kho giống hệt** bắt buộc |
| **B-15** | `markdown_blocks.py:260-270`: chỉ lấy mục con **trực tiếp** khi dựng `sub_items` | — | kho hôm nay: 1 khối có mục con chồng, khối đó không phải tách ⇒ 0 tác động | vừa (đổi hành vi cho kho tương lai); sha giống hệt hôm nay + test input nhỏ 3 cấp phải tách ⇒ văn bản cấp 3 xuất hiện **một** lần |
| **B-02** | `vectorstore/points.py`: bỏ phần kiểm lặp trong `build_full_corpus_point_batch` (giữ kiểm một lần ở `validate_full_corpus_point_inputs` trước khi tạo collection) | `upsert.py` kiểm sau upsert | `build_full_corpus_point_batch`: pipeline + 3 test | vừa (đường build) ⇒ so **toàn bộ** `PointStruct` (id, payload, sparse, dense) của 8.459 đoạn trước / sau bằng dense e5 thật (CPU, ~vài phút, 0 USD, không ghi Qdrant) |
| **C-17** | fixture `require_openai_key` khỏi 3 test không tới generator (`test_api_chat.py:47, :88`, `test_phase6_live_smoke.py:403`); marker `live` (`conftest.py:23-28`) — **gỡ** (0 test dùng; đơn giản hơn dùng thật) | `require_openai_key` cho test thật cần generator; `test_phase6_settings.py:66` (kiểm env — giữ, ghi chú) | — | thấp; 15 file không key ⇒ số error giảm đúng 3 |
| **C-18** phần smoke | `test_phase6_live_smoke.py:229, :315` `confirm_paid=True` ⇒ test hàm kiểm health tách riêng (hoặc `confirm_paid=False`), để test không có đường tới lượt paid khi mock trượt; assert hiển nhiên `:388-391` | 3 test thoát ở guard (`:158, 173, 191`) | — | thấp |
| **C-11** | — (gói 1b đã gỡ `rerank()` + nhánh 409 lúc hỏi) | — | — | — |

## 4. B-12 — nội dung kho ra khỏi file tracked

- **Ghi vào `knowledge-base-hue/meta/`: A duyệt 21:3x** (đúng lựa chọn User 19:4x câu 4 — B-12 phương án (b); `meta/` không phải curated corpus,
  discovery loại). **Trước khi chuyển:** sao lưu bản gốc (`backend/config/full_corpus_conditions.json` từ git `HEAD` + bản ở `meta/` nếu đã có) vào
  `knowledge-base-hue/meta/backup_b12_<YYYY-MM-DD>/`, ghi sha256 bản gốc và bản mới vào report (hai sha phải bằng nhau — chỉ chuyển chỗ, không sửa nội dung).
- **File conditions:** `backend/config/full_corpus_conditions.json` (9 selector `exact_text`, 5.324 ký tự nguyên văn kho) ⇒ **`cp` (không `git mv`)** sang
  `knowledge-base-hue/meta/full_corpus_conditions.json` rồi **`git rm backend/config/full_corpus_conditions.json`** — `git mv` sang thư mục bị gitignore vẫn đưa file
  vào index (B thử trên repo tạm, M-1). Kiểm ngay sau bước này: `git ls-files knowledge-base-hue` = **rỗng**; `git diff --cached --name-status` chỉ có
  `D backend/config/full_corpus_conditions.json`, `M backend/config/settings.yaml`, `M …/full_corpus_chunker.py` (+ test); hook `.githooks/pre-commit:15` là lưới cuối,
  không phải bước của plan. Đích (private, `meta/` đã bị discovery loại — `settings.yaml:14-17`); `settings.yaml`
  `conditions_file: ../knowledge-base-hue/meta/full_corpus_conditions.json` (đường neo `BACKEND_DIR` như `root_dir`); mặc định trong
  `ConditionManager` (`full_corpus_chunker.py:142`) đổi theo. Build record **không** lưu đường / sha file conditions (đã kiểm) ⇒ freshness không đổi.
  Kiểm: sha danh sách đoạn toàn kho giống hệt; runtime khởi động không 409.
- **Test mẫu chunker** (`test_full_corpus_chunker.py:549-848`, 7 test, **37 chuỗi / 1.327 ký tự** nguyên văn kho — `kiem_cheo_C.md` B-12): giữ logic
  (đường file, heading, vai trò điều kiện / header, số đoạn, lát cắt `lf_text[start:end] == text`, "hai ý tách hai đoạn"); chuyển **chuỗi kỳ vọng**
  sang `knowledge-base-hue/meta/chunker_acceptance_samples.json` (private — **chỉ tạo file trong `meta/`, không `git add`**), test đọc file đó. Kiểm: quét lại `b12_scan_all.py` ⇒ test chunker 0 chuỗi
  ≥ 20 ký tự nguyên văn kho; 7 test vẫn đạt; thử "biết đỏ": sửa 1 chuỗi kỳ vọng trong bản sao tạm ⇒ đỏ.
- **Clone public:** hôm nay đã không chạy được test cần kho (16 test, `test_deps.py`) và `load_settings()` mặc định (kiểm `root_dir` + file conditions tồn
  tại) — B-12 **không làm xấu hơn**. **A quyết 21:31: không thêm fixture `private_corpus`** (chưa có nhu cầu quan sát được — không ai chạy test trên
  clone public; `Session_Prompt.md` §7): thiếu file kho thì để lỗi tự nhiên có tên file. Test thuần (128 theo `test_deps.py`, heuristic) không đổi.
- 2 converter `backend/scripts/` (72 chuỗi riêng / 3.693 ký tự): xử lý ở B-13.

## 5. Thứ tự commit (nhỏ, an toàn; mỗi commit: A commit + push **trước** khi sửa tiếp — luật chung)

| # | Commit | Mục | Kiểm riêng của commit |
|---:|---|---|---|
| 1 | `fix(build)`: không ghi sparse state trước khi kiểm đích | C-21 + test | test mới đỏ → xanh |
| 2 | `fix(chunker)`: báo lỗi đoạn vượt token | B-11 + 2 test `chunk_document` | sha đoạn giống; thời gian chunk |
| 3 | `refactor`: gỡ CLI preview + cắt phần preview của test determinism | B-04 (sau 2), phần cắt của B-20 (m-3) | sha; `g3_chunking` import; suite đạt ngay ở commit này |
| 4 | `test`: identity + sparse bytes + discovery theo record | B-20 | `--durations` |
| 5 | `chore(privacy)`: conditions + chuỗi test sang `meta/` (`cp` + `git rm`) | B-12 | sha; quét chuỗi = 0; `git ls-files knowledge-base-hue` = rỗng |
| 6 | `refactor`: gỡ smoke Phase 5 + nhánh `minilm` | C-19a, C-06 | T1 byte |
| 7 | `refactor`: gỡ Representation B (+ `make_fits_all_checker`, chữ notebook 06 / guide 6); smoke Phase 6 còn 4 câu; recorder bớt phần thừa | C-05, C-19b, C-10 | chuỗi gửi model 25 câu giống byte; `/health` |
| 8 | `refactor`: gỡ `apply_chat_template`, `parse-user-scores` (+ dòng guide), hàm freshness cũ, nhánh cuda, batch size một nơi, `REPO_ROOT` thừa; chữ docker / logging | C-04, C-07, B-05, B-07, B-06, B-09, B-14 (m-6) | `input_tokens`; `--help` = guide; log `api` |
| 9 | `test`: fixture key / marker / smoke không có đường paid / assert rỗng | C-17, C-18 | số error không key giảm 3 |
| 10 | `refactor(chunker)`: dọn chunker + mục con trực tiếp | B-14, B-15 | sha giống hệt; test 3 cấp |
| 11 | `refactor(build)`: kiểm điểm Qdrant một lần | B-02 | so 8.459 `PointStruct` |
| 12 | `chore`: chuyển 2 converter ra `data/tools/` | B-13 | grep 0 |
| — | `docs`: B-18 guide build lại; A sửa 4 chỗ `bao_cao_he_thong/` nếu cần (B-11 đổi hành vi build: đoạn vượt ⇒ build dừng) | B-18 | đọc |

Gộp 6–12 thành ít commit hơn nếu B / A muốn; giữ 1, 2, 5, 10, 11 riêng (chạm build / chunker / dữ liệu).

## 6. Tiêu chí nghiệm thu (ghi trước) và cổng ổn định

| # | Tiêu chí | Cách đo | Đạt khi |
|---|---|---|---|
| D1 | Danh sách đoạn toàn kho không đổi | `chunk_full_corpus()` ⇒ 8.459 đoạn, 0 lỗi; sha danh sách (`chunk_id`, `search_text`, `evidence_parts`) + `compute_corpus_identity` = build record | giống hệt sau **mỗi** commit 2, 3, 5, 10 và cuối đợt |
| D2 | Tìm kiếm không đổi | T1: `cd backend && HF_HUB_OFFLINE=1 uv run python -m evaluation.full_corpus_eval retrieval --out <file>` | 158 dòng, sha256 `cefb2d1ad609…` |
| D3 | Chuỗi gửi model không đổi | `data/ra_soat_code_2026-10-25/tools/sua_3/snap_3b.py` (25 câu tự viết, 0 lời gọi mạng) | giống byte `3b_before.json` (gói 3) |
| D4 | Test | 15 file liệt kê từng file, không `--env-file`; **mốc trước đợt (sau 1b, C đo 21:4x): 198 passed · 1 failed · 7 error** (đều C-17); **T-C** `test_startup_model_missing.py` (User chạy `!`) sau commit 6 (đụng builder `retrieval/full_corpus.py`) và cuối đợt | đạt; sau commit 9 error `require_openai_key` giảm đúng 3 (còn 1 failed + 4 error); test của code đã gỡ bị gỡ cùng commit; T-C `1 passed` |
| D5 | Cổng ổn định | `cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8011` (script `sua_3/gate.py`): `/` 200, `/health` 5 / 5 ready, 1 câu trong kho (marker = `sources`) + 1 câu ngoài kho (từ chối), tự viết; log 0 `ERROR`; tắt server | như mốc gói 3 |
| D6 | Không còn nơi gọi | `usage.py HEAD <tên đã gỡ>` + grep tên lệnh / hàm trong tài liệu hiện hành (`guides/` gồm `full_corpus_rag.md`, `session_prompt/`, notebook) | 0 ngoài lịch sử (`docs/`, `reports/`, `handoff_prompt/`) |
| D7 | Số dòng code | `wc -l` file `.py` tracked `backend/` trừ `tests/`, `experiments/` | trước `47a4e32`: **8.518** dòng (tests 4.278) — ghi số sau từng commit; ước giảm ~1.700 (smoke Phase 5 548 + converter 967 + Rep B ~80 + preview CLI ~150 + phần khác) |
| D8 | Public | `b12_scan_all.py` + `git ls-files knowledge-base-hue` | 0 chuỗi ≥ 20 ký tự nguyên văn kho trong `.py` / notebook tracked; 0 file `knowledge-base-hue/` trong index |
| D9 | Mọi điểm vào chạy được (m-5) | import 6 harness 8.1 (`g1…g5`, g5 bằng import) + `--help` CLI còn lại (`ingestion.full_corpus_pipeline`, `evaluation.full_corpus_eval`, `llm.phase6_live_smoke`) + 3 notebook Run All bản tạm (không `--env-file`; md5 file repo không đổi) | 0 lỗi; chạy sau commit 6, 7, 8, 11 và cuối đợt (notebook 03: `DENSE_MODEL_SPECS` — B-07; 04: pipeline / upsert — B-02, B-06; 06: generator — C-05) |

Cổng D5 chạy **sau mỗi nhóm** (sau commit 2, 5, 7, 11 và cuối đợt) — 2 câu mỗi lần, ~0,0004 USD / lần ⇒ ~0,002 USD cả đợt (trong trần chung 0,05).
D1–D4, D6 chạy sau **mỗi** commit (free); D9 theo lịch ghi ở dòng D9. Lệch D1–D3 ⇒ **dừng**, tìm nguyên nhân, báo A; không sửa tiêu chí.

## 7. Quyền, tiền, rủi ro, dừng

- Sửa code rủi ro trung bình (Phase đã duyệt, gỡ theo luật User). B-12 chuyển file sang `knowledge-base-hue/meta/` là ghi vào thư mục private (không phải
  sửa nội dung kho) — **A duyệt 21:31**, sao lưu + sha trước khi chuyển (§4). Không build index, không ghi Qdrant (C-21 test dừng trước `create_collection`; B-02 so `PointStruct` trong bộ nhớ).
- Tiền: chỉ D5 (~0,002 USD). Người làm không commit.
- Rủi ro: (1) chạm chunker (B-11, B-14, B-15) ⇒ D1 sau mỗi commit; (2) gỡ nhầm thứ có gọi động ⇒ D6 + test + harness import (6 file 8.1); (3) 1b đổi
  dòng ⇒ tìm theo tên; (4) B-11 làm build dừng khi kho đổi sinh đoạn vượt (cố ý — guide B-18 ghi cách xử lý, giới hạn huydang 256).
- Dừng khi: D1 / D2 / D3 lệch; phải đụng harness 8.1 ngoài import; phải sửa file session khác đang khai báo; vượt tiền.

## 8. Đầu ra

`report_agent/2026-10-25_ra_soat_code/sua_dot3_implementation.md` (D1–D8 trước / sau từng commit, lệnh, tiền); `STATUS_<người làm>.md`; nhắn A. A cập nhật
`Project_Status.md` (§4 số dòng / file, §8 bẫy B-11 "build dừng khi đoạn vượt") + 4 chỗ `bao_cao_he_thong/` (B-11, Rep B gỡ khỏi `BAO_CAO_CHIA_DOAN.md:136`,
smoke Phase 5 trong `BAO_CAO_NEN_TANG.md:116`).

## 9. Sửa theo review của B (`sua_dot3_plan_review.md`, bản 3 — 21:50)

| Finding | Sửa ở |
|---|---|
| **M-1** `git mv` đưa file vào index | §4 gạch "File conditions" (`cp` + `git rm`, kiểm `git ls-files knowledge-base-hue` rỗng + `git diff --cached --name-status`); gạch "Test mẫu" (chỉ tạo trong `meta/`, không `git add`); §5 commit 5; D8 |
| m-1 `parse-user-scores` trong guide | §3 dòng C-07 + câu đầu §3; §5 commit 8; D6 quét tài liệu hiện hành |
| m-2 Rep B: `make_fits_all_checker`, notebook 06, guide 6 | §3 dòng C-05, C-19b; §5 commit 7 |
| m-3 commit 3 ↔ test determinism | §2 dòng B-20; §5 commit 3 |
| m-4 C-21 assert lý do | §2 dòng C-21 (thông điệp "Target collection already exists" + điều kiện trước Qdrant) |
| m-5 D thiếu harness / CLI / notebook; T-C | §6 D4 (mốc 198 / 1 / 7 sau 1b; T-C sau commit 6 + cuối đợt), D9 mới |
| m-6 `REPO_ROOT` thừa; vị trí import sau 1b | §3 dòng B-14; §5 commit 8; câu "Bảng số dòng sau 1b" ở đầu file trỏ §4 review |
