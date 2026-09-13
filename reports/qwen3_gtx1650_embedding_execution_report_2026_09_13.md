# Báo cáo Kết quả Thực thi Embedding Qwen3 trên GPU NVIDIA GeForce GTX 1650 (4GB VRAM)

- **Thời gian thực thi hoàn tất:** 2026-09-13
- **Đối tượng:** Candidate 4 — `qwen3-embedding-0.6b-1024`
- **Mô hình:** `Qwen/Qwen3-Embedding-0.6B` (Revision: `97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3`)
- **Tập dữ liệu:** Full Corpus A (205 tài liệu markdown, 8.460 chunks)
- **Target Collection Qdrant:** `hue_full_corpus_a_qwen3_06b_1024`
- **Final Build Record:** `data/full_corpus_builds/hue_full_corpus_a_qwen3_06b_1024.json`

---

## 1. Trạng thái tổng quan

**KẾT QUẢ: ĐÃ HOÀN TẤT 100% (SUCCESS)**

Quá trình embedding mô hình `Qwen/Qwen3-Embedding-0.6B` trên GPU local NVIDIA GeForce GTX 1650 (4GB VRAM) đã chạy xong hoàn toàn trong phiên làm việc Task 7:
- Toàn bộ **8.460 chunks** đã được vector hóa thành công sang dense vectors 1024 chiều.
- Đã hoàn tất upsert toàn bộ **8.460 points** (kết hợp vector dense 1024D và vector sparse BM25 5662 terms) vào Qdrant.
- Đã vượt qua 100% các bài kiểm tra nghiêm ngặt về số lượng điểm, tính toàn vẹn của payload và chuẩn hóa vector (L2 norm).
- File build record cuối cùng đã được xuất bản nguyên tử (atomic exclusive write qua hardlink `os.link`).

---

## 2. Thông số phần cứng & Môi trường thực thi thực tế

| Tiêu chí | Thông số quan sát thực tế | Ghi chú |
| :--- | :--- | :--- |
| **GPU phần cứng** | NVIDIA GeForce GTX 1650 (Turing TU117) | Không có Tensor Cores |
| **Tổng VRAM khả dụng** | 4.0 GB (4.294.967.296 bytes) | VRAM thực tế khả dụng cho CUDA |
| **Backend & PyTorch** | CUDA (`cuda:0`), Torch 2.x, CUDA 12.x | Sentence-Transformers |
| **Precision / Data type** | `float16` (FP16) | Tiết kiệm 50% bộ nhớ so với FP32 |
| **Attention Mechanism** | `eager` | Eager PyTorch attention |
| **Batch size** | **1** | Bắt buộc batch 1 để chống tràn 4GB VRAM |
| **Tiền xử lý document** | Representation A thô (không gán tiền tố) | Đúng hợp đồng kiến trúc của Qwen |
| **Độ dài token lớn nhất** | 560 tokens | Nằm trọn vẹn trong context length 32k |

---

## 3. Thống kê hiệu năng & Bộ nhớ (GTX 1650 4GB)

### 3.1. Bộ nhớ VRAM
- **Model Parameters VRAM:** ~1,20 GB.
- **CUDA Reserved VRAM:** ~1,41 GB.
- **Peak VRAM đo được:** **~1,26 GB** (chính xác: `1.323.238.400 bytes`).
- **Headroom VRAM còn lại:** ~2,74 GB trống trên GTX 1650.
- **Hiện tượng OOM:** **Không xảy ra** (Zero Out-of-Memory). An toàn tuyệt đối ở batch size 1.

### 3.2. Tốc độ tính toán (Throughput & Latency)
- **Tổng thời gian chạy dense inference:** **~65 phút** (khoảng 3.900 giây).
- **Tốc độ xử lý trung bình:** **~2,17 passages/giây** (~0,46 giây / passage).
- **Nguyên nhân GPU load ~0% - 15% trên Task Manager:**
  - Kiến trúc chip GTX 1650 (TU117) **không có Tensor Cores**, toàn bộ phép tính FP16 được thực hiện trên FP32 ALU hoặc INT32 shared pipeline.
  - Khi chạy batch size 1, GPU bị bottleneck bởi kernel launch overhead và memory bandwidth giữa CPU <-> VRAM chứ không bão hòa các CUDA cores. Do đó, Task Manager của Windows hiển thị GPU Compute/3D Utilization ở mức rất thấp (hoặc 0-5%), trong khi VRAM đã lock 1.26 - 1.4 GB.

---

## 4. Dữ liệu nghiệm thu trên Qdrant (`hue_full_corpus_a_qwen3_06b_1024`)

1. **Số lượng vector (Point count):**
   - Kỳ vọng: `8.460`
   - Thực tế trong Qdrant: `8.460` (Khớp 100%).
2. **Kiểm tra Payload (5 trường cốt lõi):**
   - Đã đối chiếu toàn bộ 8.460 payloads bao gồm đúng năm trường canonical:
     `search_text`, `source`, `title`, `heading_path`, `evidence_parts`.
   - Kết quả: Khớp 100% với dữ liệu canonical ban đầu.
3. **Kiểm tra chuẩn hóa L2 Norm (12 Sample Points ngẫu nhiên cố định):**
   - Chuẩn Cosine yêu cầu vector có norm xấp xỉ 1.0.
   - Dung sai cho phép đối với FP16: `1e-3` (tức `[0.9990, 1.0010]`).
   - Kết quả quan sát:
     - **Min norm:** `0.999755871925492`
     - **Max norm:** `1.000481951573514`
     - **Đánh giá:** Đạt chuẩn tuyệt đối, không có giá trị `NaN`, `Inf` hoặc drift vector.
4. **Final Build Record:**
   - File: `data/full_corpus_builds/hue_full_corpus_a_qwen3_06b_1024.json`
   - SHA-256: `2faa9d4f102127093c0ebd5c14c19eef3bd7743ca0e34d434beb5aa40919bdd5`
   - Trạng thái: `complete`

---

## 5. Remote GPU là workstream deferred

Google Colab, Lightning AI và Vast.ai chỉ là các phương án cần nghiên cứu cho
re-indexing hoặc experiment tương lai. Chưa có benchmark remote nào được chạy,
vì vậy không có evidence để khóa batch size, throughput, thời gian hoặc chi phí.
Không dùng các estimate remote cũ làm kết quả quan sát.

Context và authority boundary nằm tại
`reports/qwen3_remote_gpu_offloading_research_context_2026_09_13.md`. Tài liệu
đó không phê duyệt thuê GPU, upload corpus, triển khai worker/service hay mutate
Qdrant.

---

## 6. Kết luận & Đề xuất

1. **Đối với Phase 4 hiện tại:**
   - Toàn bộ công việc tạo collection và embedding cho `qwen3-embedding-0.6b-1024` trên GTX 1650 **đã hoàn thành 100%**.
   - Cả 4 candidate (`e5-small-384`, `e5-base-768`, `huydang-dek21-768`, `qwen3-embedding-0.6b-1024`) đều đã nằm hoàn chỉnh trong Qdrant với đầy đủ build records.
   - **Không cần chạy lại hay dừng bất kỳ tiến trình nào** vì không có tiến trình nào còn đang treo.

2. **Đối với các Phase sau:**
   - Phase 5 có thể dùng collection đã hoàn thành để thiết kế và đánh giá
     retrieval; không cần rebuild chỉ vì lần encode local mất khoảng 65 phút.
   - Nếu một re-index hoặc experiment mới thật sự cần remote GPU, Reviewer phải
     hoàn tất research/design và nhận exact User approval trước mọi cloud/paid
     action.
