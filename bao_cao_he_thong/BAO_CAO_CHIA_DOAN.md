# Báo cáo cho bạn: Chia tài liệu thành đoạn (Phase 2)

**Cập nhật lần cuối: 17:10 31/10/2026 — bản 6: rà lại cho đúng hiện trạng, xoá phần không còn đúng (User 31/10).**
Các bản trước: xem `git log` file này. Người viết: agent con của A (bản 6) · Review: A. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** chatbot không tìm trên cả file dài mà trên các đoạn nhỏ, mỗi đoạn một ý. Khâu này chia **204 file
  Markdown** của kho thành đoạn và ghi chính xác vị trí từng phần trong file gốc, để câu trả lời trích dẫn được đúng chỗ.
  Đã đóng từ 12/09/2026; **cách chia không đổi từ đó** (hai đợt sửa kho 28/10 và 30/10 chỉ đổi nội dung kho; đợt rà code 26/10
  chỉ thêm kiểm, không đổi đoạn nào).
- **Đang chạy cách nào:** chia theo cấu trúc Markdown (tiêu đề, đoạn văn, bảng, danh sách, trích dẫn), không cắt theo số ký
  tự, không gối đầu có chủ đích. Khối quá dài thì bảng tách từng hàng (kèm dòng tiêu đề bảng), danh sách tách từng mục, đoạn
  văn tách ở ranh giới câu. **Hôm nay** (kho sau hai đợt sửa, 30/10): 204 file → **8.424 đoạn**, 0 lỗi, đúng bằng số đoạn trong
  chỉ mục đang chạy.
- **Đo được:** chạy lại ra cùng đoạn, cùng ID (test so với bản ghi build đang chạy — đạt sau build lại 30/10); mọi đoạn vừa
  giới hạn token của cả 3 tokenizer — dài nhất 366 / 512, 366 / 512, 255 / 256 (đo 30/10). Trung vị 85 token và 1.787 đoạn
  dưới 50 token ("đoạn vụn"): **đo trên kho cũ (8.459 đoạn, 24/10), chưa đo lại.**
- **Giới hạn chính:**
  - nhiều đoạn rất ngắn — 8.1 thử gộp lại: không giúp (§4);
  - bảng dài bị tách từng hàng nên dòng giá đứng riêng, khó tìm (gốc ở khâu tìm, `BAO_CAO_TIM_KIEM.md`); bảng ngắn giữ nguyên;
  - 3 cặp đoạn lặp một phần nội dung (đếm trên kho cũ, chưa đếm lại);
  - ID đoạn dạng `file#số` dồn số khi xoá / thêm dòng giữa file (gặp 30/10 ở 2 file) ⇒ so trước ↔ sau phải theo nội dung;
  - đoạn dài nhất sát trần tokenizer huydang (255 / 256) — model này chatbot không dùng, code vẫn kiểm (xem §2).
- **Chi phí / tốc độ:** 0 đồng (chạy trên máy).
- **Đã thử để cải thiện (Phase 8.1, 25/10):** 12 cách chia khác, đo với cùng một hạn mức chữ đưa model ⇒ không cách nào tốt
  hơn; đoạn to hơn còn làm mất đoạn đúng của 4–8 câu ⇒ **giữ cách chia hiện tại** (§4).
- **Bạn cần quyết gì:** không.

## 2. Hoạt động thế nào (bản đang chạy)

```text
204 file Markdown (danh sách file + file loại trừ trong cấu hình)
-> đọc theo cấu trúc (tiêu đề, đoạn văn, bảng, danh sách, trích dẫn)
-> mỗi khối thành một đoạn nếu vừa giới hạn token
-> khối quá dài: bảng tách từng hàng (kèm dòng tiêu đề bảng), danh sách tách từng mục con,
   đoạn văn tách ở ranh giới câu
-> gắn "điều kiện" theo 3 quy tắc khai báo ngoài kho (ví dụ: ghi chú áp dụng cho một bảng giá)
-> ghi vị trí chính xác của từng phần trong file gốc
-> vòng kiểm cuối mọi đoạn: vừa token? từng phần cắt đúng chữ trong file gốc? -> lỗi nào cũng làm dựng kho dừng
-> danh sách đoạn theo thứ tự cố định
```

- Mỗi đoạn mang danh sách **phần bằng chứng** (thân đoạn, tiêu đề bảng, điều kiện) kèm vị trí bắt đầu / kết thúc trong file
  gốc. Trích dẫn đọc phần này, không đọc text ghép.
- **Text để tìm kiếm** = tên tài liệu + đường tiêu đề + các phần bằng chứng. Đây là text được biến thành vector và đếm từ khóa.
- **ID đoạn** = `<đường dẫn file>#<số thứ tự>`; ID điểm trong Qdrant suy ra từ ID đoạn, nên chạy lại ra cùng ID.
- **Giới hạn token:** mỗi đoạn phải vừa cả 3 tokenizer (e5-small 512, e5-base 512, huydang 256), đếm bằng tokenizer thật. Đoạn
  vượt, hoặc quy tắc điều kiện không khớp đúng một chỗ ⇒ báo lỗi, **dựng kho dừng** (một vòng kiểm cuối cho mọi nhánh, từ
  26/10). Chatbot chỉ dùng e5-small; hai tokenizer kia còn trong cấu hình (8.1 thử bỏ: không đổi đoạn đúng).
- Code: `backend/ingestion/chunking/full_corpus_chunker.py` (`chunk_document` `:327-559`, `chunk_full_corpus` `:562`),
  `backend/ingestion/chunking/markdown_blocks.py`; cấu hình `backend/config/settings.yaml:3-35` (file loại trừ `:18-21`, tokenizer
  `:23-35`); quy tắc điều kiện `knowledge-base-hue/meta/full_corpus_conditions.json` (private — chứa nguyên văn kho).

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Đoạn văn, tiêu đề thường | **Đã xử lý, đóng gói** | 8.424 đoạn (30/10), 0 lỗi; chỉ mục đang chạy dùng đúng các đoạn này |
| Đoạn văn quá dài | **Đã xử lý, đóng gói** | tách ở ranh giới câu; `full_corpus_chunker.py:482` |
| Bảng (bảng giá, lịch) | **Xử lý một phần** | bảng dài tách từng hàng kèm dòng tiêu đề (`full_corpus_chunker.py:400`); dòng giá đứng riêng nên khó tìm — xem `BAO_CAO_TIM_KIEM.md`. 144 đoạn là bảng (đếm 26/10 trên kho cũ). 8.1 thử gộp các dòng liền nhau của cùng bảng: **không khác** |
| Danh sách dài | **Đã xử lý, đóng gói** | tách từng mục con; `full_corpus_chunker.py:450` |
| Trích dẫn (blockquote) lồng trong mục danh sách | **Xử lý một phần** | 3 cặp đoạn lặp một phần thân đoạn (3 file di tích; đếm 24/10 trên kho cũ); `markdown_blocks.py:228-245`. 8.1 thử bỏ đoạn lặp: không khác |
| Khối code (```) trong 2 file di tích | **Đã thử, chưa áp dụng** | bộ đọc Markdown bỏ qua không báo (~360 ký tự; đếm trên kho cũ); 8.1 thử giữ lại thành đoạn: không khác |
| File danh mục nghệ thuật biểu diễn (inventory, không phải nội dung cho khách) | **Đã xử lý, đóng gói** | loại khỏi kho trong đợt sửa kho 28/10 (`settings.yaml:21`): 205 → 204 file, bỏ 33 đoạn |
| Ghi chú áp dụng cho bảng (điều kiện) | **Đã xử lý, đóng gói** | 3 quy tắc, mỗi quy tắc khớp đúng một chỗ (build 30/10: 0 lỗi điều kiện); 13 phần điều kiện ở 9 đoạn (đếm 24/10 trên kho cũ); `full_corpus_chunker.py:118-282` |
| Vị trí chính xác để trích dẫn | **Đã xử lý, đóng gói** | `backend/core/schema.py:89`, `:107`; kiểm cắt đúng chữ `full_corpus_chunker.py:552-557` |
| Chạy lại ra cùng đoạn, cùng ID | **Đã xử lý, đóng gói** | test so với bản ghi build đang chạy: số đoạn, dấu vân tay nội dung và danh sách từ khóa từng byte; đạt 30/10 (`tests/test_full_corpus_chunker.py:943-964`) |
| Đoạn vụn (dưới 50 token) | **Đã thử, chưa áp dụng** | 1.787 đoạn (kho cũ). 8.1 gộp đoạn cùng mục tới 128 token: không khác; tới 256 / 384 / 512: **kém hơn** (mất 4 / 6 / 6 câu đoạn đúng) |
| Tiền tố tiêu đề trong text tìm kiếm | **Đã xử lý, đóng gói** | `full_corpus_chunker.py:57-85`. 8.1 thử chỉ giữ tiêu đề mục gần nhất / bỏ hẳn: **kém hơn** (mất 7 / 8 câu) ⇒ giữ đầy đủ |
| Thêm ngữ cảnh do model viết vào đoạn | **Đã thử, chưa áp dụng** | chỉ gọi thử ở Phase 6, chưa từng vào chỉ mục; code đã gỡ 26/10 (bạn duyệt 25/10) |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 28/10 và 30/10/2026 — Hai đợt sửa kho (cách chia không đổi)
Đợt 1 (28/10): sửa nội dung 65 file + loại file danh mục nghệ thuật biểu diễn ⇒ 205 → 204 file, 8.459 → 8.426 đoạn. Đợt 2 (30/10):
sửa 40 file, xoá 2 dòng ⇒ **8.424 đoạn**; ID đoạn dồn số ở 2 file. Cả hai đợt: 0 lỗi chia đoạn, dài nhất vẫn 366 / 512, 255 / 256;
đo trước ↔ sau: không làm hỏng câu trả lời. Report: `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md`.

### 26/10/2026 — Sửa code sau rà soát (cách chia không đổi)
Đoạn vượt token ở **mọi** nhánh ⇒ dựng kho dừng (trước có một nhánh lọt kiểm, chưa gây hại vì kho chưa có đoạn vượt); test
"kho khớp bản ghi" so cả nội dung (trước chỉ số đoạn); gọn code; file quy tắc điều kiện ra khỏi repo public. Kết quả: 8.459 đoạn
giống hệt từng byte trước ↔ sau · **PASS** · 0 USD. Report: `report_agent/2026-10-25_ra_soat_code/sua_dot3_implementation.md`.

### 25/10/2026 — Phase 8.1: thử 12 cách chia đoạn (chatbot không đổi)

**Luật ghi trước:** chỉ số quyết = đoạn đúng (vị trí đáp án trong file, 32 câu thử) có đủ trong phần đưa model, với **cùng hạn
mức chữ** cho mọi cách (750 token) để đoạn to không "tự thắng"; rào chắn 0 câu mất đoạn đúng. Mỗi cách dựng một chỉ mục thử riêng,
xoá ngay sau khi đo. Tiền: 0.

| Cách | Kết quả (32 câu) | Kết luận |
|---|---|---|
| Chỉ kiểm tokenizer e5-small (bỏ 2 tokenizer cũ) | 0 câu đổi đoạn đúng; 61 đoạn ít hơn; 1 câu tụt điểm từ khóa quá mức cho phép | không khác ⇒ chưa làm |
| Gộp dòng liền nhau của cùng bảng | 0 câu đổi | không khác ⇒ bỏ |
| Gộp đoạn cùng mục tới 128 token | 0 câu đổi | không khác ⇒ bỏ |
| Gộp tới 256 / 384 / 512 token | mất 4 / 6 / 6 câu (512: tụt có ý nghĩa thống kê sau hiệu chỉnh nhiều phép so) | **kém hơn** ⇒ bỏ |
| Sau khi tìm, mở rộng ra cả mục chứa đoạn | mất 8 câu | **kém hơn** ⇒ bỏ |
| Tiền tố chỉ tiêu đề gần nhất / không tiền tố | mất 7 / 8 câu | **kém hơn** ⇒ bỏ |
| Bỏ file danh mục / giữ 2 khối code / bỏ 3 đoạn lặp | 0 câu đổi | không khác (an toàn); file danh mục sau đó bị loại ở đợt sửa kho 28/10 |
| Gộp 384 / 512 với hạn mức gấp đôi (cỡ 10 đoạn) | mất 6 câu so với đoạn hiện tại cùng hạn mức | **kém hơn** ⇒ bỏ |

Vì sao: đoạn to **tìm thấy** nhiều hơn, nhưng mỗi đoạn chiếm nhiều chỗ nên chỉ ~4–5 đoạn vừa hạn mức thay vì ~9 đoạn nhỏ trỏ tới
nhiều chỗ khác nhau. Cách cải thiện có bằng chứng nằm ở bước sinh (đưa 10 đoạn — đã vào chatbot 28/10, `BAO_CAO_SINH_CAU_TRA_LOI_API.md`).
Giới hạn: 32 câu có nhãn; chỉ đo bước tìm / đưa đoạn. Report: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g3_implementation.md`.

### 24/10/2026 — Gỡ bộ chia đoạn bản món ăn, sửa test mốc cũ
Gỡ bộ chia đoạn món ăn (400 ký tự) cùng notebook / test đi kèm; test chạy lại so với bản ghi build đang chạy thay vì file mẫu cũ.
Không đổi bộ chia đoạn toàn kho; kết quả tìm giống từng byte · **PASS** · 0 USD.

### 24/10/2026 — Kiểm lại hiện trạng (chỉ đọc, kho cũ)
205 file → 8.459 đoạn, 0 lỗi; dài nhất 366 / 512, 366 / 512, 255 / 256; trung vị 85 token e5; 1.787 đoạn dưới 50 token; 3 cặp đoạn
lặp một phần. Các số "kho cũ" ở §1 và §3 lấy từ lần kiểm này.

### 12/09/2026 — Đóng bản toàn kho
205 file, 8.460 đoạn, 3 quy tắc điều kiện, 0 lỗi · **PASS**.

### 09/08 và 24/08/2026 — Bản món ăn (đã gỡ 24/10)
91 file ẩm thực → 572 đoạn, cắt theo 400 ký tự, bảng giữ nguyên · **PASS**; đơn giản hoá 24/08: 572 đoạn khớp tuyệt đối.

## 5. Hôm nay còn đúng không

Kiểm với code `main` (commit `1985a81`) ngày 31/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Bộ chia đoạn toàn kho là đường build duy nhất của chỉ mục | **còn dùng** | `backend/ingestion/full_corpus_pipeline.py:29`, `:126` |
| Chia theo cấu trúc, tách bảng / danh sách / câu khi quá dài; "không gộp đoạn" | **còn dùng**; 8.1: 12 cách khác không cách nào tốt hơn | `full_corpus_chunker.py:400`, `:450`, `:482` |
| Số đoạn | **8.424** từ 30/10 (trước: 8.426 từ 28/10, 8.459 từ 24/10, 8.460 ngày 12/09) | `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` (`corpus.chunk_count`, `file_count` 204) |
| 3 quy tắc điều kiện, khớp đúng một chỗ | **còn dùng** | `knowledge-base-hue/meta/full_corpus_conditions.json` (private); `full_corpus_chunker.py:157-209` |
| Ràng buộc 3 tokenizer (e5 512, huydang 256) | **còn dùng** trong code, dù chatbot chỉ dùng e5-small | `backend/config/settings.yaml:23-35`; `full_corpus_chunker.py:288-324`, `:550` |
| Phần bằng chứng có vị trí chính xác; ID điểm suy từ ID đoạn | **còn dùng** | `backend/core/schema.py:49-51`, `:89`, `:107` |
| Dữ liệu mỗi đoạn trong Qdrant: 7 trường | **còn dùng** | `backend/core/schema.py:126-136` |
| Text để tìm kiếm (tên tài liệu + tiêu đề + bằng chứng) | **còn dùng** | `full_corpus_chunker.py:57-85`; `full_corpus_pipeline.py:193` |
| Test "chạy lại ra đúng bản ghi build" | **còn dùng**; đạt 30/10 | `backend/tests/test_full_corpus_chunker.py:943-964` |

## 6. Việc còn lại / cần quyết

- Hai sửa nhỏ còn lại từ 8.1 (giữ 2 khối code, bỏ 3 đoạn lặp) và bỏ kiểm 2 tokenizer cũ: **chưa làm**. 8.1 đo: không đổi đoạn đúng
  nhưng cũng không làm tốt lên ⇒ chỉ là lựa chọn nếu sau này build lại vì lý do khác.
- Gộp đoạn vụn / gộp dòng bảng: 8.1 đo không giúp hoặc làm hại — không đề xuất.
- Bảng giá khó tìm vẫn còn; gốc ở khâu tìm / xếp đoạn (`BAO_CAO_TIM_KIEM.md`).
- Thống kê đoạn (trung vị token, đoạn vụn, số đoạn bảng, đoạn lặp, phần điều kiện) chưa đo lại trên kho 8.424 đoạn.
- ID đoạn `file#số` không bền khi sửa giữa file — đã biết, chưa có kế hoạch đổi.

## Phụ lục — hồ sơ kỹ thuật

- Report lịch sử: `reports/user_reports/phase_2_foods_markdown_chunking_user_report.md`,
  `reports/user_reports/phase_2_foods_markdown_chunking_simplicity_user_report.md`,
  `reports/user_reports/full_corpus_rag_wave_1_user_report_2026_09_12.md`; file mẫu `full_corpus_rag_wave_1_preview_2026_09_11.json`
  ở `data/reports_artifacts_private_2026-10-26/` (private, chứa nguyên văn kho).
- Tên kỹ thuật: phần bằng chứng = `evidence_parts` (`body`, `header`, `condition`); text để tìm kiếm = `search_text`
  (Representation A); ID đoạn = `chunk_id`; ID điểm = UUID5; "thêm ngữ cảnh do model viết" = Representation B (gỡ commit `c6e130c`).
- Phase 8.1 G3 (C29, review B): `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g3_implementation.md`, `phase_8_1_g3_review.md`,
  plan `phase_8_1_g3_plan.md`. Mã biến thể: H1 = chỉ tokenizer e5-small, H3 = gộp dòng bảng, H2 = gộp 128 / 256 / 384 / 512,
  small-to-big = mở rộng cả mục, p_nearest / p_none = tiền tố, S1–S3 = 3 sửa nhỏ, B10 = hạn mức 1.500 token. Hạn mức đếm bằng
  `o200k_base` trên khối bằng chứng; 512 token tụt có p Holm 0,018.
- Rà code 26/10 (đợt 3, C làm, B review): `report_agent/2026-10-25_ra_soat_code/sua_dot3_implementation.md`, `sua_dot3_review.md`.
- Dọn code 24/10 (B9): `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md` (commit `1832201`).
- Sửa kho: đợt 1 `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_b1_6_implementation.md` (B81; build record `574b5d02088b`);
  đợt 2 `sua_kho_dot2_implementation.md` (build record `51fb1ec63cbc`).
- **Lệch đã ghi và trạng thái hôm nay:**
  1. Tài liệu ghi chia đoạn "không gối đầu", nhưng `markdown_blocks.py:228-245` tách blockquote ở mọi cấp nên có 3 cặp đoạn lặp —
     **còn** (đếm trên kho cũ); 8.1 S3: bỏ đoạn lặp không đổi kết quả.
  2. Lý do của ràng buộc 3 tokenizer trong spec 2026-09-11 ("ba dense candidates") đã cũ: chatbot chỉ dùng e5-small (Qwen3-8B đã
     thử 30/10 và bỏ); code vẫn kiểm e5-base và huydang — **còn**; 8.1 H1: bỏ không đổi đoạn đúng.
