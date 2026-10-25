# Review: Plan đợt 3 (gói 2 + gói 5 + B-12) — `sua_dot3_plan.md` sha `8bbe98640c80`

Decision: **changes_requested** — 1 major (B-12 dùng `git mv` sẽ đưa nội dung kho vào index), 6 minor; còn lại plan đúng và đủ chi tiết
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-c3`)
Date: 2026-10-25 21:36 +0700 (`date`) · đọc trên working tree = `main` `47a4e32` + gói 1b (chưa commit, B làm) · chỉ đọc · **0 USD**
Căn cứ (WORKFLOW §9.1): đúng 4 mục "Căn cứ để review" của plan; chạy lệnh chỉ đọc (`git grep`, đọc code, một repo git tạm trong `/tmp`). Không đọc `STATUS_C.md`.

## 1. Phạm vi đã review

Toàn bộ plan (136 dòng, sha khớp). Kiểm lại bằng lệnh riêng: số nơi gọi của 19 tên sẽ gỡ (`git grep` ngoài / trong `tests/`); nơi dựng service `minilm`
(`grep reranker=` trong `experiments/`, `retrieval/`, `api/`, `evaluation/`); `make_fits_all_checker`; test dùng `DenseModelSpec`; đường `conditions_file` trong
`settings_loader.py:111-116`; hook `.githooks/pre-commit:15`; hành vi `git mv` sang thư mục bị ignore (repo tạm); tài liệu hiện hành còn nhắc Representation B /
`parse-user-scores`; số dòng các chỗ plan trỏ tới **sau gói 1b**.

## 2. Findings

### M-1 (major) — B-12: `git mv` sang `knowledge-base-hue/meta/` **đưa file vào index** dù thư mục bị gitignore
- Vị trí: plan §4 gạch 2 ("`git mv` sang `knowledge-base-hue/meta/full_corpus_conditions.json`").
- Bằng chứng (repo tạm `/tmp/b31/gitmv`: `.gitignore` = `private/`, `git mv cfg/c.json private/meta/c.json`): exit 0, `git status` ⇒ `R  cfg/c.json ->
  private/meta/c.json`, `git ls-files` liệt kê `private/meta/c.json` ⇒ file ở thư mục ignore **thành tracked**. Với repo này, commit đó sẽ đưa 5.324 ký tự
  nguyên văn kho vào **đường mới** của repo public — ngược mục tiêu B-12. Lưới an toàn hiện có: hook `.githooks/pre-commit:15` chặn đường staged bắt đầu
  `knowledge-base-hue/` (diff-filter ACMR gồm R) ⇒ commit sẽ bị chặn, nhưng plan không nên dựa vào hook để sửa một bước sai.
- Tiêu chí đóng: thay bằng `cp backend/config/full_corpus_conditions.json knowledge-base-hue/meta/full_corpus_conditions.json` + `git rm
  backend/config/full_corpus_conditions.json` (xóa khỏi index **và** working tree sau khi đã có bản ở `meta/` + backup); kiểm `git ls-files knowledge-base-hue`
  = rỗng và `git diff --cached --name-status` chỉ có `D backend/config/full_corpus_conditions.json` + `M backend/config/settings.yaml` (+ chunker). Áp cùng
  cách cho `chunker_acceptance_samples.json` (file mới, chỉ tạo trong `meta/`, không `git add`).

### m-1 — C-07: còn một tài liệu hiện hành nhắc `parse-user-scores`
- Bằng chứng: `guides/full_corpus_rag.md:91` (danh sách CLI evaluator — B26 vừa đối chiếu `--help`) có `parse-user-scores`; plan §3 ghi "CLI hiện hành: 0".
- Tiêu chí đóng: commit 8 sửa dòng đó (10 lệnh); D6 thêm `guides/full_corpus_rag.md` vào vùng quét.

### m-2 — C-05: thiếu tài liệu hiện hành phải sửa khi gỡ Representation B, và một hàm trở thành thừa
- Bằng chứng: `notebooks/06_generation_and_api.ipynb` ô 0 ("Representation B: có trong code … runtime không dùng"); `guides/phase_6_generation_api.md:54, 79` (mục
  "Hiện hành": "Representation B cap 256", "một call Representation B"); `bao_cao_he_thong/BAO_CAO_SINH_CAU_TRA_LOI_API.md`, `guides/full_corpus_rag.md` cũng nhắc —
  plan chỉ ghi `BAO_CAO_CHIA_DOAN.md:136`. `llm/phase6_live_smoke.py:104` `make_fits_all_checker` chỉ được gọi ở `:311` trong nhánh Attempt 1 Representation B
  (`:328`) ⇒ gỡ C-19b Attempt 1 thì hàm này 0 nơi gọi.
- Tiêu chí đóng: commit 7 gỡ cả `make_fits_all_checker`; sửa chữ notebook 06 ô 0 + guide 6 mục Hiện hành (`:54`, `:79`); A sửa 2 báo cáo.

### m-3 — Thứ tự commit 3 (B-04) ↔ 4 (B-20): test determinism gọi `generate_preview`
- Bằng chứng: `test_full_corpus_determinism_and_preview_byte_equality` gọi `generate_preview` 2 lần (plan §2 B-20 "bỏ phần preview"); commit 3 gỡ `generate_preview`
  trước commit 4 ⇒ commit 3 phải tự cắt phần preview của test đó, nếu không suite đỏ ở commit 3.
- Tiêu chí đóng: ghi rõ commit 3 gồm cắt phần preview của test determinism (commit 4 chỉ thêm identity / sparse bytes / discovery), **hoặc** đổi thứ tự 4 trước 3.

### m-4 — C-21: test nên assert đúng lý do dừng, không chỉ "raise + không có file sparse"
- Bằng chứng: sau sửa, mọi lỗi trước bước ghi sparse (ví dụ Qdrant tắt ⇒ `inspect_full_corpus_target` lỗi kết nối) cũng cho "raise + không file" ⇒ test xanh giả
  (cùng kiểu P2 của 1b). Hiện `full_corpus_pipeline.py:186-187` raise `ValueError("Target collection already exists: …")`.
- Tiêu chí đóng: test assert thông điệp `"Target collection already exists"` (hoặc kiểm Qdrant có collection runtime làm điều kiện trước như T-C của 1b). Phần còn lại
  của C-21 đúng: hôm nay ghi sparse ở `:170`, kiểm đích ở `:183-187` (số dòng **không đổi** sau 1b); test dừng trước `create_collection` ⇒ Qdrant chỉ đọc; trên `main`
  đỏ (file sparse đã ghi) — đúng "test viết trước".

### m-5 — D1–D8 thiếu hai kiểm của cổng ổn định / "mọi điểm vào chạy được"
- Bằng chứng: plan nêu rủi ro "harness import (6 file 8.1)" (§7) nhưng không có dòng D; notebook 03 / 04 / 06 gọi code bị sửa (03: `DENSE_MODEL_SPECS` — B-07 đổi
  `Literal`; 04: pipeline / upsert — B-02, B-06; 06: generator — C-05) nhưng D không có Run All.
- Tiêu chí đóng: thêm D9 — import 6 harness 8.1 + `--help` CLI còn lại (pipeline, evaluator, `phase6_live_smoke`) + 3 notebook Run All bản tạm (không `--env-file`),
  sau commit 6, 7, 8, 11 và cuối đợt; thêm T-C (`test_startup_model_missing.py`, User chạy `!`) vào D4 sau commit 6 (đụng builder `retrieval/full_corpus.py`).

### m-6 — B-14: `REPO_ROOT` không ai dùng ở `retrieval/full_corpus.py:68`; dòng import thừa chỉ còn một chỗ sau 1b
- Bằng chứng: `grep -c REPO_ROOT retrieval/full_corpus.py` = 1 (chỉ định nghĩa; có từ trước 1b). Sau 1b, `point_id_for_chunk_id`, `load_settings` thừa chỉ còn ở
  `full_corpus_chunker.py:14-15` (không còn bản `:29-30`).
- Tiêu chí đóng: B-14 (hoặc commit 8) gỡ `REPO_ROOT` thừa; sửa vị trí import.

## 3. Trả lời 5 điểm A hỏi

1. **Bảng gỡ / giữ — bằng chứng 0 nơi gọi:** B đếm lại trên working tree (đã có 1b): `record_generation_success` 0 / 0 (ngoài / trong test); `build_representation_b_messages`
   0 / 0; `verify_build_record_freshness` 0 / 1 (chỉ import test); `apply_chat_template` chỉ 2 dòng chính nhánh đó; `generate_preview` 1 (`main`) + 5 test;
   `partition_for_source` 2 + 2 test; `full_corpus_smoke` ngoài chính file chỉ có 2 dòng **báo cáo** (`BAO_CAO_NEN_TANG.md:45, 116` — plan đã ghi A sửa) + 3 test;
   dịch vụ `reranker="minilm"` chỉ `retrieval/full_corpus_smoke.py:244` (harness g1 / g4 dựng service mặc định `none`; g1 / g4_rerank dùng `CrossEncoderReranker` trực
   tiếp — plan **giữ** lớp, đúng; `g4_rerank` chạy `--device cuda` cho CrossEncoder, không đụng nhánh cuda của `embedding/full_corpus.py` mà B-07 gỡ — đúng);
   `DenseModelSpec` trong test chỉ `device="cpu"` (`test_full_corpus_embedding.py:85-95`) ⇒ B-07 không làm hỏng test. **Gỡ được mà plan giữ:** `make_fits_all_checker`
   (m-2), `REPO_ROOT` thừa (m-6). **Giữ mà nên gỡ / gỡ mà nên giữ:** không thấy mục nào khác — lý do giữ của plan (`CrossEncoderReranker`, `native_hybrid_rrf`,
   `BM25`, trạng thái `empty`, `validate_vectors` + `validate_vector_matrix`, ghim URL Qdrant, `ConditionManager` hai lượt, `evidence_recorder`) đều có nơi gọi hoặc
   có lý do ghi rõ. C-17: bỏ `require_openai_key` ở 3 test là đúng — test budget đi qua context builder trước bước kiểm generator (`api/routes/chat.py`: context
   ⇒ `generator_ready`), test `:403` tự đặt `generator_ready=False`.
2. **Thứ tự 12 commit:** an toàn, trừ m-3. Phần chunker đúng thứ tự: B-11 (commit 2) trước B-04 (3, gỡ phép kiểm token của preview), B-12 (5) đổi đường conditions
   trước B-14 / B-15 (10) cùng hàm `chunk_document`; D1 (sha đoạn + identity) sau 2, 3, 5, 10 — đủ, vì chỉ các commit đó chạm chia đoạn. B-11 thêm một lượt đếm
   token cho mỗi đoạn ⇒ ghi thời gian (plan đã có). B-15 đổi hành vi cho kho tương lai — plan có test input 3 cấp, đúng.
3. **C-21 và test viết trước:** đúng chỗ, đúng đỏ / xanh; cần assert lý do (m-4).
4. **B-12 sang `meta/`:** hướng đúng (A đã duyệt); `settings_loader.py:114` neo `BACKEND_DIR`, nên `conditions_file: ../knowledge-base-hue/meta/full_corpus_conditions.json`
   chạy được và `validate_private_paths` kiểm tồn tại như cũ; build record không lưu đường / sha file conditions ⇒ freshness không đổi. **Cách chuyển sai** (M-1).
5. **D1–D8 cho cổng ổn định:** D1 / D2 / D3 / D5 / D6 / D8 đủ cho (1)–(3) của cổng; thiếu harness / CLI / notebook (m-5). D4 nên ghi số error C-17 **trước** đợt
   (sau 1b: 1 failed + 7 error trên 15 file) để "giảm đúng 3" kiểm được.

## 4. Số dòng sau gói 1b (để người làm tìm nhanh; vẫn tìm theo tên trước mỗi lần gỡ)

| Chỗ plan trỏ (`47a4e32`) | Sau 1b (working tree) |
|---|---|
| `full_corpus_pipeline.py:170` ghi sparse; `:183-187` kiểm đích | **không đổi** (`:170`, `:183`, `:186`) |
| `full_corpus_chunker.py:15-16, 29-30` import thừa | `:14-15` (một chỗ) |
| `full_corpus_chunker.py:399, 463, 529, 600` `is not None` | `:381, 445, 511, 582` |
| `full_corpus_chunker.py:568` "so preview can detect it"; `:630-641` vòng kiểm | `:550`; `:612-` |
| `retrieval/full_corpus.py` `RerankerMode` / nhánh `minilm` trong `search` / kiểm `reranker not in` / khối "5. MiniLM" | `:63` / `:602-` / `:711` / `:779-` (khối MiniLM nay ném `RetrievalDependencyError` — 1b) |
| `retrieval/full_corpus.py` `REPO_ROOT` thừa | `:68` |
| `full_corpus_context.py:41-46` `apply_chat_template` | không đổi (`:41-`) |
| `source_state.py:99-133` `verify_build_record_freshness` | `:95-` |
| `points.py:24`, `upsert.py:19` `FULL_CORPUS_BATCH_SIZE` | `points.py:15`, `upsert.py:14` |
| `phase6_live_smoke.py:336-375` Attempt 1 Rep B | `:328-` (+ `make_fits_all_checker` `:104`, gọi `:311`) |
| `full_corpus_eval.py:689, :972` `parse_user_scores` / CLI | `:685`, `:877` (parser), `:966` (nhánh) |
| `retrieval/full_corpus_smoke.py` | 524 dòng (1b bỏ khối import kép); vẫn chỉ `full_corpus_smoke.py:244` dựng `minilm` |
| `ingestion/preview.py` | 329 dòng; 1b đã sửa docstring + neo `--output` — gỡ `main` ở B-04 thì hai thay đổi đó đi theo |
| `api/routes/chat.py` nhánh 409 lúc hỏi; `cross_encoder.py` `rerank()` | **đã gỡ ở 1b** (C-11) |

## 5. Giới hạn

- Không chạy test / build / notebook (review plan, không cần). Số nơi gọi đếm trên working tree có 1b chưa commit — khi người làm bắt đầu, chạy lại `usage.py HEAD …`
  như plan đã dặn.
- Không đánh giá D7 (ước số dòng giảm) — chỉ là số theo dõi.

## 6. Decision và bước tiếp theo

**changes_requested** — C sửa M-1 (bắt buộc: cách chuyển file sang `meta/`) và m-1…m-6 trong một lượt, ra sha mới; B kiểm lại đúng phần đổi; rồi A duyệt sha. Không cần
User quyết thêm (M-1 là sửa cách làm, không đổi hướng A đã duyệt).

## 7. Kiểm lại bản 3 (sha `7c8c660558e5`, 2026-10-25 21:5x) — chỉ phần đổi

| Finding | Chỗ sửa trong plan bản 3 | Kết luận |
|---|---|---|
| M-1 | §4 "File conditions": `cp` sang `meta/` + `git rm backend/config/full_corpus_conditions.json`; kiểm `git ls-files knowledge-base-hue` = rỗng + `git diff --cached --name-status` chỉ `D` conditions / `M` settings / `M` chunker (+ test); hook là lưới cuối. "Test mẫu": chỉ tạo file trong `meta/`, không `git add`. Commit 5 + D8 thêm kiểm index | **đóng** |
| m-1 | §3 C-07 thêm dòng `guides/full_corpus_rag.md:91`; `--help` 10 lệnh = guide; D6 quét tài liệu hiện hành | **đóng** |
| m-2 | §3 C-05: notebook 06 ô 0, guide 6 `:54`, `:79` sửa cùng commit; A sửa 2 báo cáo; C-19b gỡ `make_fits_all_checker` (`:104` / `:311`); commit 7 | **đóng** |
| m-3 | §2 B-20 + §5 commit 3: cắt phần preview của test determinism ngay ở commit 3, "suite đạt ngay ở commit này" | **đóng** |
| m-4 | §2 C-21: assert `ValueError` "Target collection already exists" + điều kiện trước Qdrant có collection runtime | **đóng** |
| m-5 | D4: mốc 198 / 1 / 7 sau 1b, sau commit 9 còn 1 failed + 4 error; T-C sau commit 6 + cuối đợt. D9 mới: 6 harness, `--help` 3 CLI, 3 notebook Run All (md5 repo không đổi) sau commit 6, 7, 8, 11, cuối | **đóng** |
| m-6 | §3 B-14 + commit 8 gỡ `REPO_ROOT` thừa; import thừa ghi vị trí sau 1b `:14-15`; đầu file trỏ bảng số dòng §4 review | **đóng** |

Không có điểm mới. **Decision bản 3: ready_for_user_confirmation** (A duyệt sha). Ghi chú: gói 1b đã commit (`1e4acd0`) — số dòng ở §4 review là số trên `HEAD` hiện
tại; người làm vẫn chạy `usage.py HEAD …` trước mỗi lần gỡ.
