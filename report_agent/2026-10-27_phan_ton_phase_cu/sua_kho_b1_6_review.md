# Review: đợt sửa kho bước 1–6 (B81)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 1 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-32`) · việc C75
Date: 11:19 28/10/2026 (`date`)
Canonical guide: spec `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (User duyệt `937cf8969810`) §5 bước 1–6 + "Dừng + khôi phục";
`guides/full_corpus_rag.md` "Build lại index khi corpus đổi"
Implementation report: `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_b1_6_implementation.md` (B, 11:09 28/10)

File tracked này không chép nội dung kho: chỉ số đếm, sha, tên file / mã mục.

## 1. Phạm vi đã review

- Report B81 (đọc hết); spec §5; guide build lại index; `data/sua_kho_2026-10-27/README.md`.
- Kho ↔ backup cho 65 file; `applied_edits.jsonl` ↔ danh sách đã review (C66 / C67); file mẫu chunker.
- `git diff -- backend/` (3 file); build record + sparse state mới; Qdrant; T1 mới; cổng 8016 qua log thật.
- Giả thuyết của B về 4 câu đổi thứ tự (A dặn xét riêng).
- C tự viết script kiểm độc lập (không dùng `apply_edits.py` của B), chỉ đọc, chỉ in số / tên file:
  `data/sua_kho_2026-10-27/review_c75_tools/{check_apply,idf_check,c75_pool,c75_chunks}.py`.

## 2. Findings

Không có blocker hay major.

**m-1 — Giải thích "4 câu không chạm file nào, đổi thứ tự do IDF" chỉ đúng với 1 / 4 câu.** Vị trí: report "Tóm tắt" (dòng "do từ điển từ khóa tính lại") và §1 đoạn "T1 cũ ↔ mới".
Yêu cầu bị ảnh hưởng: spec bước 6 ("câu đổi đoạn có giải thích bằng file đã sửa không"); `Session_Prompt.md` §1 (tách giả thuyết / nguyên nhân đã chứng minh).
B đã ghi đây là *giả thuyết*. C kiểm bằng `idf_check.py`: giữ index mới, chỉ thay `sparse_state` + `vocabulary_index` bằng bản cũ trong `backup/`.
- Đối chứng: chạy như runtime ⇒ 40 / 40 câu đổi ra đúng T1 mới.
- Thay IDF cũ:
  - **case 96** ⇒ trở về **đúng** T1 cũ ⇒ do IDF (đã chứng minh);
  - **case 31, 117, 154** ⇒ **không** trở về T1 cũ ⇒ IDF không đủ giải thích.
- `c75_pool.py` đếm đoạn của file đã sửa trong 30 ứng viên dense (index mới) của 4 câu: 31 có **3**, 96 có **0**, 117 có **8**, 154 có **9**. Các đoạn này ở hạng 11–30.

⇒ Ba câu đó **có** chạm file đã sửa, ở hạng 11–30. Thứ tự top-10 đổi chủ yếu vì những đoạn đó đổi chữ / đổi điểm trong tập ứng viên (cộng với IDF), không phải chỉ IDF. Câu
"không chạm file nào" chỉ đúng nếu xét riêng top-10.

Tác động:
- Không đổi kết quả build hay T1: T1 mới tái lập giống byte.
- Ảnh hưởng tới cách đọc ở bước 9. Luật "câu chạm" của plan B78 xét theo context (top-10), nên 3 câu này vẫn tính "không chạm" — đúng luật ghi trước, không đổi.
  Nhưng nếu một câu như vậy tụt điểm và được gắn nhãn "nhiễu", người đọc nên biết sửa kho vẫn có thể góp phần.

Tiêu chí đóng: sửa hai chỗ trong report thành "1 câu (96) do IDF — đã kiểm bằng đổi lại IDF cũ; 3 câu (31, 117, 154) có 3 / 8 / 9 đoạn của file đã sửa trong 30
ứng viên ⇒ đổi thứ tự do các đoạn đó + IDF", dẫn `review_c75_tools/idf_check.py`.

Ghi nhận (không phải finding):
- **huydang 255 / 256 sát trần, như trước sửa.** C chia đoạn lại: 3 đoạn cách trần ≤ 5 token. Đợt sửa sau chạm các đoạn này thì dễ vượt trần ⇒ bước 4 của lần sau phải đếm
  lại (A đã dặn ghi rõ).
- **Lệnh xóa ở bước 5 do User chạy bằng `!`** (auto mode chặn B). B liệt kê đích trước; Qdrant nay đúng 1 collection. Đúng luật permission (`WORKFLOW.md` §3.6).
- **Lệnh mới `dump-chunks`** (lưu bảng đoạn cũ trước khi xóa index) — plan B78 sót, B thêm, chỉ đọc. Cần cho luật câu chạm (b). Hợp lý.

## 3. Cách người kiểm chạy lại thật

Từ `backend/` repo chính, Qdrant `:6335` thật (chỉ đọc), e5-small CPU, không key, 0 USD:

```bash
PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/sua_kho_2026-10-27/review_c75_tools/check_apply.py   # chạy 2 lần: 11:0x (record cũ) và 11:11 (record mới)
PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/sua_kho_2026-10-27/review_c75_tools/c75_chunks.py    # chia đoạn lại + token + file mẫu
PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/sua_kho_2026-10-27/review_c75_tools/idf_check.py
PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/sua_kho_2026-10-27/review_c75_tools/c75_pool.py
HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_full_corpus_chunker.py -q
HF_HUB_OFFLINE=1 uv run python -m evaluation.full_corpus_eval retrieval --out ../data/sua_kho_2026-10-27/eval_sau/c75_t1_recheck.jsonl
```

Thêm:
- `git diff -- backend/` và `git diff --check`;
- sha256 các file record / sparse / backup;
- đọc `gate_b81.json` (in đã che trường chữ), các dòng `chat_metrics` 11:06 của `backend/logs/application.log`, cuối `build.log`;
- đếm lại bảng T1 cũ ↔ mới bằng script inline.

## 4. Kết quả quan sát

| Khẳng định của report | C thấy (lần chạy mới, trừ khi ghi "đọc file") | Khớp |
|---|---|---|
| 1a "còn hiệu lực" | `t1_truoc` = `t1_truoc_recheck` = `cefb2d1ad609`; record cũ (`backup/`) `03829ed641f7`, sparse cũ `dbd5f7bc538d` (đọc file) | ✓ |
| 1c sao lưu | 66 file trong `meta/backup_sua_kho_2026-10-28/` = 65 file sửa + file mẫu chunker; 66 / 66 giống hash trong record cũ; snapshot 51.273.216 byte | ✓ |
| 2 áp sửa | `applied_edits.jsonl` (`ca9e647f4af4`) **== đúng danh sách đã review** (123 edit, thứ tự, file, `old`, `new`; K091 không có); áp lần lượt lên backup trong bộ nhớ: mỗi `old` đúng 1 lần, **65 / 65 file kho giống byte**; trong 205 file runtime cũ, 65 đổi hash = đúng 65 file sửa, **0 file khác đổi** | ✓ |
| 3 `exclude_files` + test + docstring | `settings.yaml` +1 dòng file danh mục; test +1 assert; 2 docstring 205 ⇒ 204; `git diff --check` sạch | ✓ |
| 4 chia đoạn | 204 file, **8.426** đoạn, **0 lỗi**; token lớn nhất e5-small 366 / 512, e5-base 366 / 512, huydang **255 / 256** | ✓ |
| 4 file mẫu chunker | bản hiện tại == backup với đúng phép thay của edit 106 (mục K125; `old` có 1 lần trong backup); 1 dòng đổi | ✓ |
| 5 build | (đọc `build.log`) record `574b5d02088b`, sparse `1bae9e0f3c49`, 204 file, 8.426 đoạn, verification 8.426 / 8.426 / 5; tính lại sha file: khớp. Qdrant: 1 collection, 8.426 point. Record mới: 204 nguồn, 0 hash lệch kho, chỉ mất đúng file danh mục, từ vựng **5.631** | ✓ |
| 6 test chunker | **44 passed** | ✓ |
| 6 T1 mới | chạy lại: sha **`23c58c47635d`**, 158 dòng = file của B | ✓ |
| 6 bảng T1 cũ ↔ mới | 118 giống / 40 đổi / 26 chỉ đổi thứ tự / 18 đổi top-5; chạm file sửa 35, file danh mục 3 (2 câu chạm cả hai ⇒ hợp 36); không chạm (xét top-10): 31, 96, 117, 154 | ✓ (giải thích: m-1) |
| 6 cổng 8016 | log thật: server khởi động 11:06:21 trên index mới (retrieval / tokenizer / generator ready — qua kiểm hash kho ↔ record); đúng **2** dòng `chat_metrics` 11:06:42 / :44 (`n_context_sources` 10 / 10, `refusal` false / true, `n_cited_sources` 1 / 0); dừng 11:06:53; `gate_b81.json`: `/` 200, `/health` 5 / 5, câu hỏi trong log 0; cổng 8016 nay trống | ✓ |
| tiền | (2.092 + 1.881) × 0,1 / 1M + (52 + 52) × 0,5 / 1M = **0,0004493 USD** | ✓ |

Ý nghĩa: bước 1–6 làm đúng spec. Kho đổi đúng và chỉ đúng các edit đã review. Index dựng lại khớp kho, chatbot khởi động và trả lời được. Sao lưu đủ để quay lại.

## 5. Giới hạn hoặc phần chưa chạy

- Không đọc nội dung từng edit (đã review ở C66 / C67). Lần này chỉ kiểm bằng máy rằng phần áp **đúng bằng** danh sách đã review.
- Không chạy lại cổng sống (tốn key + ≈ 0,0005 USD); dùng log thật của B, đủ trường, đúng giờ.
- Không thử khôi phục từ snapshot (spec không yêu cầu khi không dừng). Chỉ kiểm file snapshot có và đúng cỡ.
- Bước 7–9 chưa làm (ngoài phạm vi).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** A commit 3 file `backend/` và cập nhật các chỗ trỏ T1 `cefb2d1ad609` ⇒ `23c58c47635d`, số file / đoạn / từ vựng (spec bước 6, 10).
B sửa m-1 khi tiện; không chặn bước 7–9.
