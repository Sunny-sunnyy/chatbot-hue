# Báo cáo dành cho người dùng: Giai đoạn 2 - Chia tài liệu thành đoạn (chunking)

```text
Trạng thái: Đã đóng (lịch sử) — viết lại 2026-10-24
```

## 1. Bạn nhận được gì

Chatbot không tìm trên cả một file dài. Nó tìm trên các đoạn nhỏ (`chunk`), mỗi đoạn nói về một ý.
Phase 2 tạo bước chia đoạn đó và giữ được đường dẫn về đúng chỗ trong file gốc để trích dẫn.

Phase 2 có hai đợt:

- **Foods (tháng 8/2026, lịch sử):** 91 file ẩm thực → 572 đoạn, cắt theo 400 ký tự, bảng giữ nguyên.
  User xác nhận 09-08-2026; bản đơn giản hóa xác nhận 24-08-2026.
- **Toàn corpus "wave 1" (tháng 9/2026, đang dùng):** 205 file của 5 domain → 8.460 đoạn lúc đóng
  (12-09-2026). Sau khi sửa corpus ở Phase 7A2, cùng chunker cho ra 8.459 đoạn. Index đang chạy
  dùng đúng 8.459 đoạn này.

## 2. Hệ thống hoạt động như thế nào

```text
205 file Markdown -> đọc theo cấu trúc (tiêu đề, đoạn văn, bảng, danh sách, trích dẫn)
-> mỗi khối thành một đoạn nếu vừa giới hạn token
-> khối quá dài: bảng tách từng hàng (kèm dòng tiêu đề bảng), danh sách tách từng mục con,
   đoạn văn tách ở ranh giới câu
-> gắn "điều kiện" theo 3 quy tắc khai báo ngoài corpus (ví dụ: ghi chú áp dụng cho một bảng giá)
-> ghi vị trí chính xác của từng phần trong file gốc -> danh sách đoạn theo thứ tự cố định
```

- **Không cắt theo số ký tự, không gối đầu (overlap).** Ranh giới là ranh giới tự nhiên của Markdown.
- **`evidence_parts`:** mỗi đoạn mang danh sách phần bằng chứng (`body`, `header`, `condition`) với
  vị trí bắt đầu/kết thúc trong file gốc. Citation đọc phần này, không đọc text ghép.
- **`search_text`** (gọi là Representation A): tên tài liệu + đường tiêu đề + các phần bằng chứng.
  Đây là text được nhúng vector.
- **`chunk_id`** = `<đường dẫn file>#<số thứ tự>`; ID điểm Qdrant là UUID5 suy từ `chunk_id`. Chạy lại
  ra cùng ID.
- **Giới hạn token:** mỗi đoạn phải vừa cả 3 tokenizer: e5-small 512, e5-base 512, huydang 256. Đo bằng
  tokenizer thật, không đoán theo ký tự. Đoạn vượt hoặc quy tắc điều kiện không khớp đúng một chỗ → báo lỗi.

## 3. Agent đã chạy và quan sát gì

**Theo report cũ (không chạy lại các bước này):**

| Nội dung | Kết quả lúc đóng | Nguồn |
|---|---|---|
| Foods | 572 đoạn; 0 đoạn thường vượt 400 ký tự; 8 bảng dài giữ nguyên (09-08-2026) | `reports/user_reports/phase_2_foods_markdown_chunking_user_report.md` |
| Foods đơn giản hóa | 572 đoạn khớp tuyệt đối trước/sau (24-08-2026) | `..._simplicity_user_report.md` |
| Wave 1 preview | `PASS`, 205 file, 8.460 đoạn, 3 quy tắc, 0 lỗi; max token 366/512, 366/512, 255/256 (12-09-2026) | `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json` |
| Wave 1 test | Implementer báo `39 passed, 1 warning`; reviewer chỉ đọc code, không chạy | `reports/user_reports/full_corpus_rag_wave_1_user_report_2026_09_12.md` |

**Fresh — tôi chạy hôm nay 2026-10-24 (offline, chỉ đọc; preview ghi ra `/tmp`):**

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| `chunk_full_corpus()` | 205 file, 8.459 đoạn, 0 lỗi | Khớp con số Phase 7A2 |
| ID | 8.459 `chunk_id` và 8.459 UUID5 khác nhau | Không trùng ID |
| Theo domain | travel 3.322, foods 1.670, heritages 1.613, festivals 1.130, performing_arts 724 | Đủ 5 domain |
| Phần bằng chứng | 8.459 `body`, 180 `header`, 13 `condition` (9 đoạn có điều kiện) | Quy tắc điều kiện vẫn được áp |
| Preview mới | `PASS`, 8.459 đoạn, 0 lỗi, 0 nhóm quá dài; max 366/512, 366/512, 255/256 | Mọi đoạn vẫn vừa 3 tokenizer |
| Trung vị token | e5 85; huydang 62. Đoạn dưới 50 token e5: 1.787 | Nhiều đoạn rất ngắn ("chunk vụn") |
| Gối đầu | 3 cặp đoạn lặp một phần text (trích dẫn lồng trong mục danh sách, 3 file `heritages/heritage/`) | Xem mục Lệch |
| Qdrant (GET) | `hue_full_corpus_7a2_e5_small_384` 8.459 point; build record ghi 8.459 đoạn | Index khớp chunker hôm nay |
| Test chunker | 57 test: 56 đạt, 1 **không đạt** (`test_full_corpus_determinism_and_preview_byte_equality`: 8.459 ≠ 8.460) | Test còn so với artifact cũ; chunker không hỏng |
| Foods | `chunk_foods_markdown()` vẫn ra 572; 2 collection Foods vẫn 572 point | Code Foods còn chạy nhưng không đứng sau API |

## 4. Hôm nay còn đúng không

| Kết quả/quyết định Phase 2 | Hôm nay | Bằng chứng (file:dòng) |
|---|---|---|
| Chunker full-corpus là đường build duy nhất của index | *còn dùng* | `backend/ingestion/full_corpus_pipeline.py:29`, `:111`, `:162`; `guides/full_corpus_rag.md:114` |
| Chia theo cấu trúc, tách bảng/danh sách/câu khi quá dài | *còn dùng* (User giữ nguyên tới baseline 7B) | `backend/ingestion/chunking/full_corpus_chunker.py:385`, `:450`, `:546`; `session_prompt/Project_Status.md:107` |
| Số đoạn 8.460 | *đã thay bởi 8.459 (Phase 7A2, sửa corpus)* | fresh run; `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` (`corpus.chunk_count`); `guides/full_corpus_rag.md:112` |
| 3 quy tắc điều kiện, khớp đúng một chỗ | *còn dùng* | `backend/config/full_corpus_conditions.json:3`, `:34`, `:57`; `full_corpus_chunker.py:197-221` |
| Ràng buộc 3 tokenizer (huydang 256, e5 512) | *còn dùng* trong code, dù e5-base/huydang không còn là candidate | `backend/config/settings.yaml:48-60`; `full_corpus_chunker.py:333-338`; `backend/embedding/full_corpus.py:43`, `:55`; `guides/full_corpus_rag.md:132` |
| `evidence_parts` vị trí chính xác, `chunk_id`, UUID5 | *còn dùng* | `backend/core/schema.py:49-51`, `:88-95`, `:126-136`; `full_corpus_chunker.py:403`, `:630-639` |
| Payload 5 field (spec wave 1) | *đã thay bởi 7 field, thêm `chunk_id`, `domain` (metadata v2, 09/2026)* | `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md:130`; `backend/core/schema.py:126-136` |
| Representation A là text nhúng vector | *còn dùng* | `full_corpus_pipeline.py:162`; `full_corpus_chunker.py:71-99` |
| Representation B (LLM viết thêm ngữ cảnh) | *chưa vào build*: chỉ có trong live smoke Phase 6 | `backend/llm/phase6_live_smoke.py:352`; spec `...-written-spec.md:147-152` |
| Foods chunker `chunk_foods_markdown` (400 ký tự) | *đã bỏ khỏi runtime* (API dùng full-corpus từ Phase 6/7A2); code còn, chỉ test/benchmark/notebook 02 gọi; đề xuất xóa | `backend/ingestion/chunking/markdown_chunker.py:72`; `backend/ingestion/pipeline.py:8`; `backend/tests/conftest.py:108`; `notebooks/02_foods_data_and_chunking.ipynb:54`; `reports/phase_7_cleanup_inventory_2026_10_24.md:41` |
| Preview artifact 8.460 làm mốc test | *lỗi thời*: test so với nó đang fail | `backend/tests/test_full_corpus_chunker.py:984`, `:996`; `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json` |

## 5. Giới hạn và bước tiếp theo

- Chunker giữ nguyên tới khi có baseline 7B (`Project_Status.md:107`). Baseline 7B đã có.
- Phase 8 dự kiến thử chunk size / gộp chunk vụn và bỏ ràng buộc huydang 256 (`guides/full_corpus_rag.md:131-132`).
  Số đo hôm nay: 1.787 đoạn dưới 50 token e5.
- Cần sửa nhỏ: cập nhật hoặc bỏ mốc 8.460 trong test, để bộ test chunker xanh lại.
- 3 cặp đoạn gối đầu ảnh hưởng nhỏ (cùng một phần text nằm trong 2 đoạn). Nên xử lý cùng đợt Phase 8.
- Không cần bạn xác nhận lại Phase 2. Đây là bản viết lại để đọc hiện trạng.

## Lệch phát hiện

1. `session_prompt/Project_Status.md:87` nói chunker "không overlap". Code
   `backend/ingestion/chunking/markdown_blocks.py:233-250` tách khối trích dẫn (`blockquote`)
   ở mọi cấp, kể cả khi nó nằm trong mục danh sách đã thành một khối. Lần chạy hôm nay cho
   3 cặp đoạn có phần `body` lặp nhau.
2. `guides/full_corpus_rag.md:195` nói 8.460 "không phải product invariant". Nhưng
   `backend/tests/test_full_corpus_chunker.py:984-996` lấy 8.460 từ artifact cũ làm kỳ vọng, nên
   hôm nay fail (8.459 ≠ 8.460). `Project_Status.md` §8 (`:153-171`) và mục 7A2 của guide (`:112-113`)
   không nhắc test này đang fail. `reports/phase_7_cleanup_inventory_2026_10_24.md:147` còn đề xuất
   chạy file test này để kiểm sau khi dọn.
3. Lý do của ràng buộc 3 tokenizer trong spec (`docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md:142-144`:
   "ba dense candidates") không còn đúng. Candidate hiện là e5-small và qwen3-8b
   (`backend/embedding/full_corpus.py:43`, `:55`). Code vẫn kiểm e5-base và huydang
   (`backend/config/settings.yaml:53-60`). `Project_Status.md:87-88` mô tả đúng code;
   chỉ lý do gốc đã cũ.
