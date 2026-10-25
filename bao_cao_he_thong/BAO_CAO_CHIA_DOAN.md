# Báo cáo cho bạn: Chia tài liệu thành đoạn (Phase 2)

**Cập nhật lần cuối: 14:14 25/10/2026 — bản 3: thêm kết quả thử nghiệm Phase 8.1 (12 cách chia đoạn khác, do C chạy);
chatbot không đổi.**
Người viết: B (bản 3, theo report của C) · Review: C. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** chatbot không tìm trên cả file dài mà trên các đoạn nhỏ, mỗi đoạn một ý. Khâu
  này chia 205 file Markdown thành đoạn và ghi chính xác vị trí từng phần trong file gốc, để câu trả lời
  trích dẫn được đúng chỗ. Đã đóng (bản toàn kho 12/09/2026).
- **Đang chạy cách nào:** chia theo cấu trúc Markdown (tiêu đề, đoạn văn, bảng, danh sách, trích dẫn),
  không cắt theo số ký tự, không gối đầu có chủ đích. Khối quá dài thì bảng tách từng hàng (kèm dòng tiêu
  đề bảng), danh sách tách từng mục, đoạn văn tách ở ranh giới câu. Kết quả hôm nay: 8.459 đoạn, đúng
  bằng số đoạn trong chỉ mục đang chạy.
- **Đo được:** chạy lại ra cùng đoạn, cùng ID; mọi đoạn vừa giới hạn token của cả 3 tokenizer (dài nhất
  366/512, 366/512, 255/256). Trung vị 85 token; 1.787 đoạn dưới 50 token ("đoạn vụn").
- **Giới hạn chính:** nhiều đoạn rất ngắn (8.1 cho thấy gộp lại **không** giúp với hạn mức hiện tại); bảng giá bị tách
  từng hàng nên dòng giá khó tìm (gộp dòng bảng: không khác); 3 cặp đoạn lặp một phần nội dung.
- **Chi phí / tốc độ:** không tốn tiền (chạy trên máy).
- **Phase 8.1 đã thử (25/10, 0 USD, ~1 giờ máy):** 12 cách chia đoạn khác — gộp đoạn cùng mục tới 128 / 256 / 384 / 512
  token, gộp dòng bảng, mở rộng sau khi tìm, đổi tiền tố tiêu đề, bỏ kiểm tokenizer cũ, 3 sửa nhỏ — đo với **cùng một hạn
  mức chữ** đưa model. **Kết luận: giữ cách chia hiện tại.** Đoạn to tìm thấy nhiều hơn nhưng chiếm chỗ, nên ít đoạn lọt
  phần đưa model và 4–8 câu bị mất đoạn đúng — đúng cả khi nâng hạn mức lên cỡ "10 đoạn". Ba sửa nhỏ và bỏ kiểm tokenizer
  cũ an toàn (không đổi đoạn đúng; bỏ tokenizer cũ có 1 câu tụt keyword vượt mức cho phép).
- **Bạn cần quyết gì (8.2):** khi build lại chỉ mục, có gộp kèm 3 sửa nhỏ + bỏ kiểm tokenizer cũ không (không đổi đoạn đúng nhưng
  không làm tốt lên; §6).

## 2. Hoạt động thế nào (bản đang chạy)

```text
205 file Markdown -> đọc theo cấu trúc (tiêu đề, đoạn văn, bảng, danh sách, trích dẫn)
-> mỗi khối thành một đoạn nếu vừa giới hạn token
-> khối quá dài: bảng tách từng hàng (kèm dòng tiêu đề bảng), danh sách tách từng mục con,
   đoạn văn tách ở ranh giới câu
-> gắn "điều kiện" theo 3 quy tắc khai báo ngoài corpus (ví dụ: ghi chú áp dụng cho một bảng giá)
-> ghi vị trí chính xác của từng phần trong file gốc -> danh sách đoạn theo thứ tự cố định
```

- Mỗi đoạn mang danh sách **phần bằng chứng** (thân đoạn, tiêu đề bảng, điều kiện) kèm vị trí bắt
  đầu/kết thúc trong file gốc. Trích dẫn đọc phần này, không đọc text ghép.
- **Text để tìm kiếm** = tên tài liệu + đường tiêu đề + các phần bằng chứng. Đây là text được biến thành
  vector.
- **ID đoạn** = `<đường dẫn file>#<số thứ tự>`; ID điểm trong Qdrant suy ra từ ID đoạn, nên chạy lại ra
  cùng ID.
- **Giới hạn token:** mỗi đoạn phải vừa cả 3 tokenizer (e5-small 512, e5-base 512, huydang 256), đo bằng
  tokenizer thật. Đoạn vượt, hoặc quy tắc điều kiện không khớp đúng một chỗ, thì báo lỗi.
- Code: `backend/ingestion/chunking/full_corpus_chunker.py`, `backend/ingestion/chunking/markdown_blocks.py`;
  cấu hình `backend/config/settings.yaml:3-34`, `backend/config/full_corpus_conditions.json`.

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Đoạn văn, tiêu đề thường | **Đã xử lý, đóng gói** | 8.459 đoạn, 0 lỗi; chỉ mục đang chạy dùng đúng các đoạn này |
| Đoạn văn quá dài | **Đã xử lý, đóng gói** | tách ở ranh giới câu; `full_corpus_chunker.py:546` |
| Bảng (bảng giá, lịch) | **Xử lý một phần** | bảng dài tách từng hàng kèm dòng tiêu đề (`full_corpus_chunker.py:385`); dòng giá đứng riêng nên khó tìm — xem `BAO_CAO_TIM_KIEM.md`. 8.1 thử gộp các dòng liền nhau của cùng bảng (≤ 256 token): **không khác** |
| Danh sách dài | **Đã xử lý, đóng gói** | tách từng mục con; `full_corpus_chunker.py:450` |
| Trích dẫn (blockquote) lồng trong mục danh sách | **Xử lý một phần** | 3 cặp đoạn lặp một phần thân đoạn (3 file di tích); `markdown_blocks.py:233-250`. 8.1 thử bỏ đoạn lặp: không khác (an toàn) |
| Khối code (```) trong 2 file di tích | **Đã thử, chưa áp dụng** | parser bỏ không báo (~360 ký tự); 8.1 thử giữ lại thành đoạn: không khác (an toàn) |
| File danh mục nghệ thuật biểu diễn (inventory) | **Đã thử, chưa áp dụng** | vẫn được đưa vào chỉ mục (33 đoạn); 8.1 thử bỏ: không khác (an toàn) |
| Ghi chú áp dụng cho bảng (điều kiện) | **Đã xử lý, đóng gói** | 3 quy tắc, 13 phần điều kiện ở 9 đoạn; `full_corpus_conditions.json`; `full_corpus_chunker.py:197-221` |
| Vị trí chính xác để trích dẫn | **Đã xử lý, đóng gói** | `backend/core/schema.py:89`, `:107`; `full_corpus_chunker.py:403` |
| Chạy lại ra cùng đoạn, cùng ID | **Đã xử lý, đóng gói** | test determinism so với build record đang chạy, đạt 24/10 (`tests/test_full_corpus_chunker.py:978-1041`) |
| Đoạn vụn (dưới 50 token) | **Đã thử, chưa áp dụng** | 1.787 đoạn. 8.1 gộp đoạn cùng mục tới 128 token: không khác; tới 256 / 384 / 512: **kém hơn** (mất 4 / 6 / 6 câu đoạn đúng); mở rộng cả mục sau khi tìm: kém hơn (mất 8 câu) |
| Tiền tố tiêu đề trong text tìm kiếm | **Đã xử lý, đóng gói** | 8.1 thử chỉ giữ tiêu đề mục gần nhất / bỏ hẳn: **kém hơn** (mất 7 / 8 câu) ⇒ giữ đầy đủ |
| Thêm ngữ cảnh do model viết vào đoạn ("Representation B") | **Đã thử, chưa áp dụng** | chỉ gọi thử ở Phase 6; chưa vào chỉ mục |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 25/10/2026 — Phase 8.1: thử 12 cách chia đoạn (bản 3; C chạy, B review)

Chatbot không đổi. Mỗi cách chia dựng một chỉ mục thử riêng (xóa ngay sau khi đo; cuối cùng Qdrant chỉ còn chỉ mục đang
chạy). **Luật ghi trước:** chỉ số quyết = đoạn đúng (vị trí đáp án trong file, 32 câu thử) có đủ trong phần đưa model, với
**cùng hạn mức chữ** cho mọi cách (750 token — trung vị của 5 đoạn hiện tại) để đoạn to không "tự thắng"; rào chắn 0 câu
mất đoạn đúng; mỗi bước đổi đúng một thứ so với bước trước.

| Cách | Kết quả (32 câu) | Kết luận |
|---|---|---|
| Chỉ kiểm tokenizer e5-small (bỏ 2 tokenizer cũ) | 0 câu đổi; 61 đoạn ít hơn | không khác |
| Gộp dòng liền nhau của cùng bảng | 0 câu đổi | không khác |
| Gộp đoạn cùng mục tới 128 token | 0 câu đổi | không khác |
| Gộp tới 256 / 384 / 512 token | mất 4 / 6 / 6 câu (512: tụt có ý nghĩa thống kê, p Holm 0,018) | **kém hơn** |
| Mở rộng cả mục sau khi tìm (small-to-big) | mất 8 câu | **kém hơn** |
| Tiền tố chỉ tiêu đề gần nhất / không tiền tố | mất 7 / 8 câu | **kém hơn** |
| Bỏ file danh mục / giữ 2 khối code / bỏ 3 đoạn lặp | 0 câu đổi | không khác (an toàn) |
| Gộp 384 / 512 với hạn mức 1.500 token (cỡ 10 đoạn) | mất 6 câu so với đoạn hiện tại cùng hạn mức | **kém hơn** |

Đọc kết quả: đoạn to **tìm thấy** nhiều hơn (ở 512 token, top-10: +5 / −1 câu), nhưng mỗi đoạn chiếm nhiều chỗ nên chỉ
~4–5 đoạn vừa hạn mức thay vì ~9 đoạn nhỏ trỏ tới nhiều chỗ khác nhau. **Giữ cách chia hiện tại**; cách cải thiện đã có bằng
chứng nằm ở bước sinh (đưa 10 đoạn — `BAO_CAO_SINH_CAU_TRA_LOI_API.md`). **Tiền:** 0. Giới hạn: 32 câu có nhãn đoạn đúng; chỉ
đo bước tìm / đưa đoạn, chưa đo câu trả lời; hạn mức chữ là xấp xỉ (chỉ đếm phần bằng chứng).

### 24/10/2026 — Gỡ bộ chia đoạn món ăn, sửa test mốc cũ (bản 2)
Gỡ `markdown_chunker.py` (bản món ăn 400 ký tự), `ingestion/helpers/`, notebook 02 và test đi kèm. Test
determinism trước đây so với file mẫu 12/09 (8.460 đoạn) nên fail; nay so với build record đang chạy
(8.459). Không đổi bộ chia đoạn. Tiêu chí ghi trước: kết quả tìm kiếm giống từng byte, test bản toàn kho
đạt · kết quả **PASS**: test chia đoạn đạt, 191 test toàn bộ đạt, tìm kiếm giống từng byte · tiền: 0.

### 24/10/2026 — Kiểm lại hiện trạng (bản 1, chạy trên máy, chỉ đọc)
205 file → 8.459 đoạn, 0 lỗi; 8.459 ID khác nhau; theo mảng: du lịch 3.322, ẩm thực 1.670, di tích
1.613, lễ hội 1.130, nghệ thuật biểu diễn 724; phần bằng chứng 8.459 thân đoạn, 180 tiêu đề bảng,
13 điều kiện; dài nhất 366/512, 366/512, 255/256; trung vị 85 token e5 (62 token huydang); 1.787 đoạn
dưới 50 token; 3 cặp đoạn lặp một phần · test chia đoạn lúc đó 56/57 đạt (1 test so mốc 8.460 cũ).

### 12/09/2026 — Đóng bản toàn kho ("wave 1")
Bản xem trước **PASS**: 205 file, 8.460 đoạn, 3 quy tắc, 0 lỗi; dài nhất 366/512, 366/512, 255/256.
Người làm báo `39 passed, 1 warning`; người kiểm chỉ đọc code. Sau khi sửa corpus ở Phase 7A2, cùng bộ
chia đoạn cho 8.459 đoạn.

### 24/08/2026 — Đơn giản hóa bản món ăn
572 đoạn khớp tuyệt đối trước/sau · **PASS**.

### 09/08/2026 — Đóng bản món ăn
91 file ẩm thực → 572 đoạn, cắt theo 400 ký tự, bảng giữ nguyên; 0 đoạn thường vượt 400 ký tự; 8 bảng
dài giữ nguyên · **PASS**. Bản này nay đã gỡ (24/10).

## 5. Hôm nay còn đúng không

Kiểm với code (commit `1832201`) ngày 24/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Bộ chia đoạn toàn kho là đường build duy nhất của chỉ mục | **còn dùng** | `backend/ingestion/full_corpus_pipeline.py:29`, `:111`, `:162` |
| Chia theo cấu trúc, tách bảng/danh sách/câu khi quá dài | **còn dùng** (User giữ nguyên tới khi có baseline 7B; baseline đã có) | `full_corpus_chunker.py:385`, `:450`, `:546` |
| Số đoạn 8.460 | **đã thay** bởi 8.459 (Phase 7A2, sửa corpus) | `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` (`corpus.chunk_count`) |
| 3 quy tắc điều kiện, khớp đúng một chỗ | **còn dùng** | `backend/config/full_corpus_conditions.json:3`, `:34`, `:57`; `full_corpus_chunker.py:197-221` |
| Ràng buộc 3 tokenizer (huydang 256, e5 512) | **còn dùng** trong code, dù e5-base/huydang không còn là model ứng viên; 8.1: bỏ đi không đổi kết quả (1 câu tụt keyword) | `backend/config/settings.yaml:22-34`; `full_corpus_chunker.py:333-338`; `backend/embedding/full_corpus.py:43`, `:55` |
| "Không gộp đoạn" (1 khối = 1 đoạn) | **còn đúng ở 8.1**: 12 cách gộp / chia khác không cách nào tốt hơn | `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g3_implementation.md` §3.8 |
| Phần bằng chứng có vị trí chính xác, ID đoạn, ID điểm suy từ ID đoạn | **còn dùng** | `backend/core/schema.py:49-51`, `:89`, `:107`; `full_corpus_chunker.py:403` |
| Payload 5 field (spec wave 1) | **đã thay** bởi 7 field, thêm `chunk_id`, `domain` (metadata v2, 09/2026) | `backend/core/schema.py:126-136` |
| Text để tìm kiếm (Representation A) | **còn dùng** | `full_corpus_pipeline.py:162`; `full_corpus_chunker.py:71-99` |
| Representation B (model viết thêm ngữ cảnh) | **chưa vào build**, chỉ có ở lượt thử Phase 6 | `backend/llm/phase6_live_smoke.py:352` |
| Bộ chia đoạn món ăn 400 ký tự | **đã bỏ** (gỡ ở B9, 24/10) | file `backend/ingestion/chunking/markdown_chunker.py` không còn |
| File mẫu 8.460 đoạn làm mốc test | **đã thay** bởi build record đang chạy (B9); test đạt | `backend/tests/test_full_corpus_chunker.py:978-982` |

## 6. Việc còn lại / cần quyết

- **Khi build lại chỉ mục ở 8.2 (bạn duyệt):** có thể gộp kèm 3 sửa "vệ sinh dữ liệu" (bỏ file danh mục, giữ 2 khối code,
  bỏ 3 đoạn lặp) và bỏ kiểm 2 tokenizer cũ — 8.1 đo: không đổi đoạn đúng câu nào (bỏ tokenizer cũ có 1 câu tụt keyword vượt mức cho phép), nhưng cũng **không** làm tốt lên.
- Gộp đoạn vụn / gộp dòng bảng: 8.1 đo không giúp (hoặc làm hại) với hạn mức chữ hiện tại — không đề xuất.
- Bảng giá khó tìm vẫn còn; gốc ở khâu tìm / xếp đoạn (`BAO_CAO_TIM_KIEM.md`).

## Phụ lục — hồ sơ kỹ thuật

- Report lịch sử: `reports/user_reports/phase_2_foods_markdown_chunking_user_report.md`,
  `..._simplicity_user_report.md`, `reports/user_reports/full_corpus_rag_wave_1_user_report_2026_09_12.md`;
  file mẫu `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`.
- Tên kỹ thuật: phần bằng chứng = `evidence_parts` (`body`, `header`, `condition`); text để tìm kiếm =
  `search_text` (Representation A); ID đoạn = `chunk_id`; ID điểm = UUID5.
- Bản 3 (B20, 25/10/2026): Phase 8.1 G3 — `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g3_implementation.md`
  (C29; H1, H3, H2 128/256/384/512, small-to-big, tiền tố p_nearest / p_none, S1–S3, B10), review B
  `phase_8_1_g3_review.md` (ready); plan `phase_8_1_g3_plan.md` (§1–9 `9f00c460c3e9`, §10 `d89a919067ba`). Ngân sách B =
  750 / B10 = 1.500 token `o200k_base` của khối bằng chứng. Mốc tìm kiếm runtime giống byte `cefb2d1a…`.
- Bản 1: B8, 24/10/2026. Bản 2: B10, sau dọn B9 (commit `1832201`; report
  `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md`).
- **Lệch đã ghi ở bản 1 và trạng thái hôm nay:**
  1. Tài liệu ghi chunker "không overlap", nhưng `markdown_blocks.py:233-250` tách blockquote ở mọi cấp
     nên có 3 cặp đoạn lặp — **còn**; `Project_Status.md` §4 đã ghi; 8.1 S3: bỏ đoạn lặp không đổi kết quả.
  2. Test determinism so với mốc 8.460 cũ nên fail — **đã sửa ở B9** (so với build record).
  3. Lý do của ràng buộc 3 tokenizer trong spec 2026-09-11 (`:142-144`, "ba dense candidates") đã cũ:
     model ứng viên nay là e5-small và qwen3-8b; code vẫn kiểm e5-base và huydang — **còn**; 8.1 H1: bỏ không đổi kết quả.
