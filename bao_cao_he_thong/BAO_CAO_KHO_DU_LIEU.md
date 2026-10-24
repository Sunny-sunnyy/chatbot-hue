# Báo cáo cho bạn: Phase 7A2 — Kho dữ liệu: sửa dữ liệu và tạo lại chỉ mục

```text
Trạng thái: Đã đóng 24/10/2026 (Gate 2 đóng kèm giới hạn: chỉ mục Qwen3-8B hoãn sang Phase 8)
Cập nhật lúc: 24-10-2026 +07
Người viết: C · Review: A
```

## 1. Bạn nhận được gì

- Kho tri thức Huế **đã sửa 25 chỗ mâu thuẫn** có căn cứ (ngày tháng, số liệu, địa chỉ, số văn
  bản…) trong 27 file. Bộ câu hỏi chuẩn (Golden) chỉ phải sửa 1 đáp án mẫu.
- Chatbot chạy trên **chỉ mục mới** `hue_full_corpus_7a2_e5_small_384` (8.459 đoạn) dựng từ dữ liệu
  đã sửa, nên trả lời theo thông tin mới.
- **Một lệnh build duy nhất**: sửa dữ liệu về sau chỉ cần chạy lại lệnh build, không phải sửa code.
  Code dựng chỉ mục cũ (kiểm thử trước, migration metadata…) đã bỏ.
- Qdrant được dọn từ 16 xuống 3 collection.

Ví dụ: một file từng ghi hai con số khác nhau cho cùng một diện tích, nay chỉ còn một con số thống nhất.

## 2. Hệ thống hoạt động như thế nào

```text
Markdown đã sửa → chia đoạn (không đổi so với Phase 2) → e5-small (chạy trên máy) + BM25
 → Qdrant (chỉ mục mới) → "phiếu build" ghi dấu vân tay từng file dữ liệu
khi chatbot khởi động: so dấu vân tay với dữ liệu hiện tại → khác thì từ chối chạy
```

"Phiếu build" (build record) là nguồn sự thật duy nhất cho câu hỏi "chỉ mục có khớp dữ liệu không".
Sửa một chữ trong kho mà chưa build lại thì chatbot không khởi động — để không trả lời bằng chỉ mục cũ.

## 3. Đã chạy và quan sát gì

| Nội dung | Kết quả | Ý nghĩa |
|---|---|---|
| Golden 176 + smoke 10 sau khi sửa kho (lúc đóng) | Đạt | Đề vẫn khớp kho |
| Chỉ mục mới: số đoạn, cấu trúc, vector | 8.459 / 8.459, không lỗi | Build đầy đủ |
| Chatbot khởi động | HTTP 200 | Chạy được trên chỉ mục mới |
| 5 câu hỏi thật với `gpt-6-luna` | 4 đạt / 1 chưa đạt — giống hệt trước khi sửa | Câu chưa đạt là lỗi cũ (bảng giá vé, F2) |
| Build chỉ mục Qwen3-8B qua OpenRouter | Lần 1 trộn 3 nhà cung cấp (vector không đồng nhất); lần 2 chỉ Nebius bị lỗi 504 | Bạn chọn hoãn sang Phase 8 |
| Dọn Qdrant | Còn đúng 3 collection | Gọn, đúng danh sách duyệt |
| **Kiểm lại hôm nay** (24/10, C, chỉ đọc) | Qdrant: 3 collection; chỉ mục 7A2 có 8.459 điểm (dense + sparse); phiếu build `v3`, `complete`, 205 file | Hiện trạng đúng như lúc đóng |

## 4. Cách bạn kiểm tra thêm nếu cần

Không bắt buộc. Có thể hỏi chatbot một câu về thông tin vừa sửa (ví dụ diện tích đầm Cầu Hai), hoặc
mở `http://localhost:6335/dashboard` để thấy 3 collection.

## 5. Hôm nay còn đúng không

Kiểm với code, Qdrant (GET) và `session_prompt/Project_Status.md` §4 ngày 24/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ |
|---|---|---|
| Chỉ mục `hue_full_corpus_7a2_e5_small_384`, 8.459 đoạn, là chỉ mục chatbot dùng | **còn dùng** | `backend/ingestion/full_corpus_pipeline.py:66–69`; `backend/config/settings.yaml:111`; Qdrant GET |
| Phiếu build `full_corpus_build:v3` là nguồn sự thật; dữ liệu lệch thì từ chối chạy | **còn dùng** | `backend/ingestion/source_state.py:133`; `backend/retrieval/full_corpus.py:353,415` |
| Một lệnh build `python -m backend.ingestion.full_corpus_pipeline build --candidate <id>` | **còn dùng** | `backend/ingestion/full_corpus_pipeline.py:232–244` |
| Sparse state (từ điển BM25) chung, ghi một lần; dữ liệu đổi thì phải xóa file cũ trước khi build | **còn dùng** (bẫy đã ghi ở `Project_Status.md` §8) | `full_corpus_pipeline.py:121–131` |
| Hai model dense: e5-small (chạy máy) và Qwen3-Embedding-8B (OpenRouter, pin Nebius) | **còn trong code**; 8B **chưa có chỉ mục** → Phase 8 | `backend/embedding/full_corpus.py:41–66` |
| Chia đoạn giữ nguyên từ Phase 2 | **còn dùng**, tới khi Phase 8 đổi (có số liệu ủng hộ đổi) | `backend/ingestion/chunking/full_corpus_chunker.py`; `reports/phase_8_candidate_hypotheses_2026_10_24.md` |
| Payload 7 trường (metadata v2) | **còn dùng** | `backend/retrieval/full_corpus.py` `REQUIRED_PAYLOAD_FIELDS` |
| 13 collection cũ (4 legacy, 4 metadata v2, 3 Foods 08a, 2 TF-IDF 08b) | **đã xóa** | Qdrant GET hôm nay |
| Hai collection Foods (572 điểm mỗi cái) | **còn**, không đứng sau API nào; đề xuất xóa sau Phase 7 (chờ bạn) | `reports/phase_7_cleanup_inventory_2026_10_24.md` §2.1 |
| Backup Gate 1 của kho | **đã xóa** khi đóng Phase | `Project_Status.md` §4 |

## 6. Giới hạn và bước tiếp theo

- **Qwen3-8B chưa có chỉ mục**; khi làm lại ở Phase 8 cần cách gọi chịu được lỗi 504/429.
- F2 (bảng giá) và F1 (tổng hợp nhiều nguồn) vẫn còn — đã được đo kỹ ở Phase 7B (`BAO_CAO_DANH_GIA.md`).
- Bộ chia đoạn vẫn kiểm cả 3 tokenizer (gồm HuyDang 256 đã bỏ) → đoạn bị giữ nhỏ; Phase 8 xử lý.
- Notebook 03, 04, 06 còn mô tả/gọi tên cũ; notebook 04 sẽ lỗi vì tìm phiếu build của 8B (chưa có).

## Lệch phát hiện

- `Project_Status.md` §4 ghi "mỗi chunk vừa cả 3 tokenizer e5-small / e5-base / huydang" — đúng với
  code (`backend/config/settings.yaml:48–60`), nhưng e5-base và HuyDang không còn là model ứng viên từ
  7A2; ràng buộc này chỉ còn tác dụng làm đoạn nhỏ đi (6 bảng bị tách chỉ vì HuyDang). Đã báo ở C1.
- Notebook `04_qdrant_ingestion.ipynb` lặp qua cả 2 model trong code và gọi một trường không còn tồn
  tại (`prepared.sample_chunk_ids`), nên sẽ lỗi khi chạy (đọc code, chưa chạy). Đã ghi ở C2 §2.4.
