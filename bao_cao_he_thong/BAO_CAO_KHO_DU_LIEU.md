# Báo cáo cho bạn: Kho dữ liệu — sửa dữ liệu và tạo lại chỉ mục (Phase 7A2)

**Cập nhật lần cuối: 19:04 24/10/2026 — bản 2: đưa về mẫu mới (Tóm tắt đầu file, checklist 5 mức, mã
nội bộ xuống Phụ lục); nội dung kỹ thuật và số đo giữ nguyên bản 1.**
Người viết: C · Review: A. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** giữ kho tri thức Huế đúng và đảm bảo chỉ mục chatbot dùng luôn khớp kho. Kho
  **đã sửa 25 chỗ mâu thuẫn** có căn cứ (ngày tháng, số liệu, địa chỉ, số văn bản…) trong 27 file; bộ
  câu hỏi Golden chỉ phải sửa 1 đáp án mẫu.
- **Đang chạy cách nào:** chatbot chạy trên **chỉ mục mới** `hue_full_corpus_7a2_e5_small_384` (8.459
  đoạn) dựng từ dữ liệu đã sửa bằng **một lệnh build duy nhất**; "phiếu build" ghi dấu vân tay từng file,
  dữ liệu lệch thì chatbot từ chối khởi động. Trạng thái: đã đóng 24/10/2026 (kèm giới hạn: chỉ mục
  Qwen3-8B hoãn sang Phase 8).
- **Đo được:** chỉ mục 8.459 / 8.459 đoạn, không lỗi; chatbot khởi động HTTP 200; 5 câu thật 4 đạt / 1
  chưa đạt — giống hệt trước khi sửa. Qdrant dọn từ 16 xuống 3 collection. Kiểm lại 24/10: hiện trạng
  đúng như lúc đóng.
- **Giới hạn chính:** Qwen3-8B chưa có chỉ mục; bộ chia đoạn vẫn kiểm cả tokenizer của model đã bỏ nên
  đoạn bị giữ nhỏ; còn 2 collection món ăn không dùng (đang dọn).
- **Chi phí:** build chỉ mục e5-small chạy trên máy, không tốn tiền API.
- **Bạn cần quyết gì:** không có ở khâu này (xóa 2 collection món ăn bạn đã duyệt 24/10; đang làm).

## 2. Hoạt động thế nào (bản đang chạy)

```text
Markdown đã sửa → chia đoạn (không đổi so với Phase 2) → e5-small (chạy trên máy) + BM25
 → Qdrant (chỉ mục mới) → "phiếu build" ghi dấu vân tay từng file dữ liệu
khi chatbot khởi động: so dấu vân tay với dữ liệu hiện tại → khác thì từ chối chạy
```

"Phiếu build" (build record) là nguồn sự thật duy nhất cho câu hỏi "chỉ mục có khớp dữ liệu không".
Sửa một chữ trong kho mà chưa build lại thì chatbot không khởi động — để không trả lời bằng chỉ mục cũ.
Sửa dữ liệu về sau chỉ cần chạy lại lệnh build, không phải sửa code.

Code: `backend/ingestion/full_corpus_pipeline.py` (lệnh build), `backend/ingestion/source_state.py`
(phiếu build), `backend/retrieval/full_corpus.py` (kiểm khi khởi động).

Tự kiểm (không bắt buộc): hỏi chatbot một câu về thông tin vừa sửa (ví dụ diện tích đầm Cầu Hai), hoặc
mở `http://localhost:6335/dashboard` để xem các collection.

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Sửa mâu thuẫn có căn cứ trong kho | **Đã xử lý, đóng gói** | 25 chỗ / 27 file; Golden sửa 1 đáp án; Golden 176 + smoke 10 đạt sau khi sửa |
| Chỉ mục e5-small trên dữ liệu đã sửa | **Đã xử lý, đóng gói** | 8.459 / 8.459 đoạn (dense + sparse); HTTP 200; kiểm lại 24/10 |
| Phiếu build: dữ liệu lệch → từ chối khởi động | **Đã xử lý, đóng gói** | Phiếu `v3`, `complete`, 205 file (kiểm 24/10); `source_state.py:133`; `full_corpus.py:353,415` |
| Một lệnh build cho mọi lần sửa dữ liệu | **Đã xử lý, đóng gói** | `full_corpus_pipeline.py:232–244` |
| Build lại sau khi sửa kho (từ điển BM25) | **Xử lý một phần** | Từ điển ghi một lần: phải xóa file cũ trước khi build, không thì build báo lỗi; `full_corpus_pipeline.py:121–131` |
| Chỉ mục Qwen3-8B qua OpenRouter | **Đã thử, chưa áp dụng** | Lần 1 trộn 3 nhà cung cấp (vector không đồng nhất); lần 2 chỉ Nebius lỗi 504; bạn chọn hoãn sang Phase 8 |
| Dọn collection cũ trong Qdrant | **Đã xử lý, đóng gói** | 16 → 3 collection, đúng danh sách duyệt |
| Xóa 2 collection món ăn không dùng | **Chưa thực hiện** (lúc 19:04 24/10) | Bạn duyệt 24/10; việc dọn đang làm |
| Đoạn bị giữ nhỏ vì kiểm tokenizer model đã bỏ | **Chưa thực hiện** | 6 bảng bị tách chỉ vì HuyDang 256; Phase 8 xử lý |
| Notebook 03, 04, 06 mô tả/gọi tên cũ | **Xử lý một phần** | Việc dọn đã sửa trong working tree, chưa review/commit |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 24/10/2026 — Kiểm lại hiện trạng (C, chỉ đọc)
Kết quả: **PASS** — Qdrant 3 collection; chỉ mục 7A2 có 8.459 điểm (dense + sparse); phiếu build `v3`,
`complete`, 205 file · hiện trạng đúng như lúc đóng · tiền: 0.

### 24/10/2026 — Đóng Phase 7A2
Golden 176 + smoke 10 sau khi sửa kho: **PASS** · chỉ mục mới 8.459 / 8.459, không lỗi: **PASS** ·
chatbot khởi động HTTP 200 · 5 câu thật với `gpt-6-luna`: 4 đạt / 1 chưa đạt — giống hệt trước khi sửa
(câu chưa đạt là lỗi bảng giá cũ) · dọn Qdrant còn đúng 3 collection · code dựng chỉ mục cũ (kiểm thử
trước, migration metadata…) **đã bỏ**; backup kho **đã xóa** khi đóng.
Chỉ mục Qwen3-8B qua OpenRouter: lần 1 trộn 3 nhà cung cấp → vector không đồng nhất; lần 2 chỉ Nebius
→ lỗi 504 · **FAIL** (chưa có chỉ mục dùng được) · bạn chọn **hoãn** sang Phase 8.

## 5. Hôm nay còn đúng không

Kiểm với code (commit `54670a0`), Qdrant (GET) và `session_prompt/Project_Status.md` §4 ngày 24/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Chỉ mục `hue_full_corpus_7a2_e5_small_384`, 8.459 đoạn, là chỉ mục chatbot dùng | **còn dùng** | `backend/ingestion/full_corpus_pipeline.py:66–69`; `backend/config/settings.yaml:111`; Qdrant GET |
| Phiếu build `full_corpus_build:v3` là nguồn sự thật; dữ liệu lệch thì từ chối chạy | **còn dùng** | `backend/ingestion/source_state.py:133`; `backend/retrieval/full_corpus.py:353,415` |
| Một lệnh build `python -m backend.ingestion.full_corpus_pipeline build --candidate <id>` | **còn dùng** | `backend/ingestion/full_corpus_pipeline.py:232–244` |
| Sparse state (từ điển BM25) chung, ghi một lần; dữ liệu đổi thì phải xóa file cũ trước khi build | **còn dùng** (bẫy đã ghi ở `Project_Status.md` §8) | `full_corpus_pipeline.py:121–131` |
| Hai model dense: e5-small (chạy máy) và Qwen3-Embedding-8B (OpenRouter, pin Nebius) | **còn trong code**; 8B **chưa có chỉ mục** → Phase 8 | `backend/embedding/full_corpus.py:41–66` |
| Chia đoạn giữ nguyên từ Phase 2 | **còn dùng**, tới khi Phase 8 đổi (có số liệu ủng hộ đổi) | `backend/ingestion/chunking/full_corpus_chunker.py`; [R1] |
| Payload 7 trường (metadata v2) | **còn dùng** | `backend/retrieval/full_corpus.py` `REQUIRED_PAYLOAD_FIELDS` |
| 13 collection cũ (4 legacy, 4 metadata v2, 3 món ăn 08a, 2 TF-IDF 08b) | **đã xóa** | Qdrant GET 24/10 |
| Hai collection món ăn (572 điểm mỗi cái) | **còn** (lúc 19:04 24/10), không đứng sau API nào; bạn đã duyệt xóa, việc dọn đang làm | [R2] §2.1 |
| Backup Gate 1 của kho | **đã xóa** khi đóng Phase | `Project_Status.md` §4 |

## 6. Việc còn lại / cần quyết

- **Qwen3-8B chưa có chỉ mục**; khi làm lại ở Phase 8 cần cách gọi chịu được lỗi 504/429.
- Lỗi bảng giá và tổng hợp nhiều nguồn vẫn còn — đã được đo kỹ ở Phase 7B (`BAO_CAO_DANH_GIA.md`).
- Bộ chia đoạn vẫn kiểm cả 3 tokenizer (gồm HuyDang 256 đã bỏ) → đoạn bị giữ nhỏ; Phase 8 xử lý.
- Notebook 03, 04, 06 và 2 collection món ăn: việc dọn sau Phase 7 đang làm; khi xong, A cập nhật các
  dòng tương ứng ở §3 và §5.

## Phụ lục — hồ sơ kỹ thuật

- Mã: lỗi bảng giá = **F2**; tổng hợp nhiều nguồn = **F1**; việc dọn sau Phase 7 = **B9** (B làm, C
  review); 8B hoãn theo review Gate 2 (`reports/phase_7a2_gate_2_review_2026_10_24.md` §6).
- [R1] giả thuyết Phase 8: `reports/phase_8_candidate_hypotheses_2026_10_24.md` (C1, C7).
- [R2] danh sách dọn sau Phase 7: `reports/phase_7_cleanup_inventory_2026_10_24.md` (C2).
- Bản 1 (C8, 24/10/2026, commit `4426ed0`).
- **Lệch phát hiện (24/10):**
  - `Project_Status.md` §4 ghi "mỗi chunk vừa cả 3 tokenizer e5-small / e5-base / huydang" — đúng với
    code (`backend/config/settings.yaml:48–60`), nhưng e5-base và HuyDang không còn là model ứng viên
    từ 7A2; ràng buộc này chỉ còn tác dụng làm đoạn nhỏ đi (6 bảng bị tách chỉ vì HuyDang). Đã báo ở C1.
  - Notebook `04_qdrant_ingestion.ipynb` (bản commit `54670a0`) lặp qua cả 2 model trong code và gọi
    một trường không còn tồn tại (`prepared.sample_chunk_ids`), nên sẽ lỗi khi chạy (đọc code, chưa
    chạy). Đã ghi ở C2 §2.4; B9 đang sửa.
