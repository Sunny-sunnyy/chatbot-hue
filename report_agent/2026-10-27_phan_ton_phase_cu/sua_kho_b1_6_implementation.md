# Implementation Report: đợt sửa kho — bước 1–6 (B81)

Người làm: B (Claude Opus 5.5, `hue-rag-ac`) · Date: 11:09 28/10/2026 (`date`) · Việc: `CURRENT_HANDOFF.md` mục B81 (A giao 10:29 28/10; Phase 8.2 User đóng 10:23).
Spec: `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (User duyệt `937cf8969810`) §5 bước 1–6. Người kiểm: C (C75).
File tracked này **không chép nội dung kho**: chỉ số đếm, sha, đường dẫn private. Code đổi ở working tree, **chưa commit** (A commit sau C75).

## Tóm tắt cho User (lời thường)

- **Đã làm:** sửa 40 mục lỗi kho có căn cứ + 11 chỗ tên phường cũ (123 chỗ thay chữ trong 65 file), bỏ file danh mục nghệ thuật biểu diễn khỏi index, rồi dựng lại
  index. Chatbot chạy lại bình thường: kiểm sức khỏe 5 / 5, hỏi thử câu trong kho có trả lời kèm nguồn, câu ngoài kho từ chối đúng.
- **Số:** 205 → 204 file, 8.459 → 8.426 đoạn. Kết quả tìm của 158 câu thử: 118 câu y hệt; 40 câu đổi danh sách 10 đoạn (26 câu chỉ đổi thứ tự) — 36 câu chạm đúng
  file đã sửa / file bị bỏ, 4 câu còn lại chỉ đổi chỗ 2–3 đoạn — C kiểm bằng thí nghiệm (C75): 1 câu do từ điển từ khóa tính lại trên kho mới; 3 câu chủ yếu vì
  đoạn của file đã sửa nằm trong nhóm 30 ứng viên (ngoài top-10), cộng thêm từ điển mới.
- **Tiền:** ≈ 0,00045 USD (2 câu thử). Có bản sao lưu đủ để quay lại nếu cần.
- **Chưa làm (bước 7–9):** nhãn "đoạn đúng" bản mới, sửa Golden lệch kho (bạn duyệt từng mục), đo chất lượng "sau" để so với bộ "trước".

## 1. Bước và kết quả

| Bước | Làm gì | Kết quả |
|---|---|---|
| 1a | Kiểm "còn hiệu lực" của bộ "trước" (plan B78 §1) | runtime `backend/` = `510e1a8` (diff rỗng, trừ tests / experiments); T1 chạy lại `cefb2d1ad609`; build record `03829ed641f7`; Qdrant 1 collection 8.459 ⇒ **đạt**, không chạy lại bộ "trước" |
| 1b | Lưu bảng đoạn cũ (cho luật câu chạm (b) — bản chỉ mục cũ sẽ bị xóa) | `eval_truoc/chunks_truoc.json` 8.459 đoạn, sha `ff41ab4ee0ec` (lệnh mới `truoc_sau.py dump-chunks`) |
| 1c | Sao lưu | 65 file kho + `meta/chunker_acceptance_samples.json` ⇒ `knowledge-base-hue/meta/backup_sua_kho_2026-10-28/` (66 / 66 giống byte); build record + sparse state ⇒ `data/sua_kho_2026-10-27/backup/` (sha giữ nguyên); **snapshot Qdrant** `hue_full_corpus_7a2_e5_small_384-2406466428880772-2026-10-28-03-35-41.snapshot` (51.273.216 byte) — tải bản sao về `backup/`, sha256 khớp checksum Qdrant |
| 2 | Áp sửa (`tools/apply_edits.py`, thay chuỗi theo thứ tự `make_diffs_them.py` đã kiểm: edits B73 "sửa" trừ **K091**, rồi `diffs_them`) | 123 edit / 51 mục / 65 file; mỗi `old` khớp đúng 1 lần lúc áp; đọc / ghi theo byte (0 / 66 file có `\r`); 65 / 65 file khác backup; mọi `new` có trong file; 65 / 65 file vẫn bắt đầu bằng `#`; `applied_edits.jsonl` sha `ca9e647f4af4` |
| 3 | `exclude_files` + test + docstring | `backend/config/settings.yaml` +1 dòng (`performing_arts/performing-arts-entities-inventory.md`); `backend/tests/test_full_corpus_chunker.py` +1 assert, docstring 205 ⇒ 204; `backend/ingestion/chunking/full_corpus_chunker.py:567` docstring 205 ⇒ 204 |
| 4 | Chia đoạn thử (chỉ đọc) + test mẫu | `chunk_full_corpus()`: 204 file, 8.426 đoạn, **0 lỗi**; token lớn nhất: e5-small 366 / 512, e5-base 366 / 512, huydang **255 / 256** (như trước sửa). Test mẫu: đúng **1** chuỗi lệch (`me_keo` mục 2 — chứa trọn `old` của edit 106, mục K125) ⇒ sửa bằng **đúng phép thay của edit đó**; file mẫu đổi 1 dòng (sha `3013c24fd8f4` ⇒ `5d5ee8116bd9`). Test chunker: 42 pass, 2 fail dự kiến (so với build record cũ) |
| 5 | Xóa đủ 3 đích rồi build tại chỗ | liệt kê trước khi xóa: đúng 1 collection + 2 file như spec. **Auto mode chặn lệnh xóa của B ⇒ User chạy `!`** (collection DELETE `true`, 2 file `rm`, Qdrant trống). Build `python -m ingestion.full_corpus_pipeline build --candidate e5-small-384` 10:57:11–11:02:49: 204 file, 8.426 đoạn, `verification` payload 8.426 / point 8.426 / vector mẫu 5; build record `574b5d02088b`; sparse state `1bae9e0f3c49` (từ vựng 5.660 ⇒ **5.631**); `corpus_identity` `625b2b8e19bf…`. Log `eval_sau/build.log` |
| 6 | Kiểm sau build | test chunker **44 / 44 pass**; test settings / retrieval / context / API (không key): 42 pass, 1 fail + 1 error = đúng 2 test cần key (như mốc); **T1 mới** 158 dòng sha **`23c58c47635d`**; cổng ổn định đạt (dưới); `eval_sau/chunks_sau.json` sha `7392734a512c` |

**T1 cũ ↔ mới theo câu** (158 câu, top-10): 118 giống; **40 đổi** — 26 chỉ đổi thứ tự (cùng tập 10 đoạn), 18 đổi top-5. Giải thích: 33 câu có đoạn (cũ hoặc mới) thuộc
file đã sửa; 3 câu có đoạn của file danh mục bị loại; **4 câu** (case 31, 96, 117, 154) không chạm file nào — cả 4 giữ nguyên tập 10 đoạn, chỉ đổi chỗ 2–3 vị trí ⇒ khớp
giả thuyết **IDF BM25 tính lại trên kho mới** (từ vựng 5.660 ⇒ 5.631, số đoạn đổi). **C75 đã tách bằng thí nghiệm** (`data/sua_kho_2026-10-27/review_c75_tools/idf_check.py`:
giữ index mới, chỉ thay sparse state + vocabulary index bằng bản cũ trong `backup/`): **case 96 trở về đúng T1 cũ ⇒ do IDF (đã chứng minh)**; case 31, 117, 154 không trở về —
30 ứng viên dense của chúng có 3 / 8 / 9 đoạn của file đã sửa ở hạng 11–30 (`c75_pool.py`) ⇒ thứ tự đổi chủ yếu vì các đoạn đó (BM25 chấm lại trong 30 ứng viên), cộng với IDF.
Tức là 3 câu này vẫn "chạm file đã sửa", chỉ không qua top-10 (luật đếm ở trên chỉ xét top-10).

**Cổng ổn định** (`tools/gate_b81.py`, `eval_sau/gate_b81.json`; API `uvicorn api.app:app --port 8016`, đã tắt bằng TaskStop, cổng trống lại; câu tự viết, không từ Golden):

| Kiểm | Kết quả |
|---|---|
| `/` · `/health` | 200 · 200, 5 / 5 thành phần `ready` / `alive` |
| câu trong kho | 200, có `[n]`, 1 nguồn trích; log `n_context_sources` 10; client 3.485,9 ms |
| câu ngoài kho | 200, từ chối chuẩn, 0 nguồn; client 2.109,5 ms |
| dòng `chat_metrics` mới · câu hỏi trong log | **2** (= số câu) · **0** |
| tiền (token log) | vào 2.092 + 1.881, ra 52 + 52 ⇒ **≈ 0,000449 USD** |

## 2. Lệch / ghi chú

- **Bước 5 do User chạy lệnh xóa** (`!` trong terminal B) vì auto mode chặn; B liệt kê đích trước, kiểm trạng thái trước / sau. Không ai chạy hộ khác.
- **Lệnh mới `dump-chunks`** trong `truoc_sau.py` (sha `e59b4ac8380b`): plan B78 §3 luật (b) cần vị trí đoạn cũ, mà spec bước 5 xóa collection cũ ⇒ phải lưu trước bước 5. Plan không
  ghi bước này (sót); B thêm, chỉ đọc Qdrant.
- File mẫu chunker: chỉ sửa 1 chuỗi bằng đúng edit đã review (không chọn chữ mới).
- `full_corpus_conditions.json`: 0 edit chạm (C68) — build 0 lỗi điều kiện xác nhận.
- Chỗ tracked đang trỏ T1 `cefb2d1ad609` (handoff, `Project_Status`, guide) và số file / đoạn / từ vựng ở `Project_Status.md` §4: **A cập nhật** (spec bước 6, 10; file của A).
- Lần đầu chạy lại T1 ở bước 1 không tạo file (lệnh của B nối `| tail -0`); chạy lại sạch, sha đúng.

## 3. Dừng + khôi phục (spec §5) — đã chuẩn bị, **không dùng**

Kho: chép lại 65 file + file mẫu từ `knowledge-base-hue/meta/backup_sua_kho_2026-10-28/`; code: `git checkout -- backend/config/settings.yaml backend/tests/test_full_corpus_chunker.py
backend/ingestion/chunking/full_corpus_chunker.py`; Qdrant: khôi phục snapshot (`backup/*.snapshot`); build record + sparse state từ `backup/`.

## 4. Bàn giao cho người kiểm (C75)

- **Diff kho với backup** từng mục: `diff -r knowledge-base-hue/meta/backup_sua_kho_2026-10-28/<file> knowledge-base-hue/<file>` cho 65 file trong `applied_edits.jsonl`
  (mỗi dòng: `order`, `source` = mã mục, `file`, `old`, `new`); đối chiếu `edits/*.jsonl` + `diffs_them/edits_them.jsonl` đã review (C66, C67); K091 không có trong danh sách.
  Chạy lại thử (free): `uv run python -I data/sua_kho_2026-10-27/tools/apply_edits.py` trên kho **đã sửa** sẽ dừng ở edit 1 ("old found 0 times") — đúng (đã áp).
- **Chunk / token / build:** chạy lại `chunk_full_corpus` (0 lỗi, 8.426) ; `build.log` summary; sha build record `574b5d02088b`, sparse state `1bae9e0f3c49`.
- **T1 mới** `eval_sau/t1_sau.jsonl` (`23c58c47635d`) — chạy lại `python -m evaluation.full_corpus_eval retrieval` phải giống byte; bảng câu đổi ở §1.
- **Code:** `git diff -- backend/` (3 file, +4 / −2); test chunker 44 pass.
- **Cổng:** đọc `eval_sau/gate_b81.json`; chạy lại cần key + ≈ 0,0005 USD (tùy C).
- Hết bước 6: chatbot khởi động lại được. Bước 7 (gold v4), 8 (Golden, User duyệt), 9 (bộ "sau") chưa làm.
