# Post-closure Audit — Qwen Full-corpus A Collection

Decision: `PASS` — không phát hiện lỗi collection/data/runtime
Reviewer: Codex
Date: 2026-09-13 +07
Target: `hue_full_corpus_a_qwen3_06b_1024`

## Mục tiêu và ranh giới

User yêu cầu kiểm tra lại vì dense inference local kéo dài khoảng 65–70 phút.
Audit chỉ đọc collection Qdrant hiện có, tái dựng canonical corpus/sparse state
và tái encode một mẫu nhỏ bằng exact Qwen snapshot. Không rebuild, upsert,
delete/reset collection, sửa build record hoặc access Foods collections.

Audit áp dụng bottom-up context building: đối chiếu lần lượt schema, identity,
toàn bộ point/payload/vector invariants, exact sparse recomputation, model
runtime và sampled dense provenance trước khi kết luận.

## Fresh observed evidence

### Toàn bộ 8.460 points

- Qdrant status `green`, optimizer `ok`, update queue `0`.
- Exact count và scroll count cùng bằng `8460`; expected count `8460`.
- Missing IDs `0`, foreign IDs `0`, duplicate IDs `0`.
- Payload mismatch `0` so với fresh canonical chunks.
- Dense dimension mismatch `0`, non-finite `0`, zero vector `0`, exact duplicate
  dense vector `0`.
- Dense stored norm nằm trong
  `[0.9999995671997459, 1.000000443818983]`.
- Sparse invalid index `0`, non-finite/length mismatch `0`.
- Tái tính sparse từ canonical `search_text` và Phase 3 state cho cả `8460`
  points: mismatch `0`.
- Corpus identity khớp
  `0e5c059516cd942b151286cf597f785c65e642cacd1b0421124fe50fe574f223`.
- Sparse state SHA-256 khớp
  `5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be`.
- Final build record SHA-256 vẫn là
  `2faa9d4f102127093c0ebd5c14c19eef3bd7743ca0e34d434beb5aa40919bdd5`.

### Tái encode 12 mẫu bằng exact model

Fresh runtime:

```text
model: Qwen/Qwen3-Embedding-0.6B
revision: 97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3
device: cuda:0
dtype: torch.float16
attention: eager
dimension: 1024
```

So sánh dense vectors tái tạo với vectors đang lưu:

- sample count `12`;
- minimum cosine similarity `0.9998792409896851`;
- maximum per-component absolute difference `3.841519355773926e-05`.

Sai khác rất nhỏ phù hợp với numeric variation của một lần chạy lại
CUDA/FP16 và storage/normalization; không phải evidence của nhầm model, nhầm
input hoặc corrupt vectors.

### Qdrant log

Log ghi collection được tạo và các upsert request đều trả HTTP `200`. Sau khi
container restart, shard của collection recover `1/1 (100%)`. Fresh filter
không tìm thấy `error`, `warning`, `panic`, `failed` hoặc `corrupt` trong log
Qdrant liên quan.

## Giải thích thời gian và warnings

Implementer ghi nhận khoảng `3900` giây cho `8460` passages, tương đương khoảng
`2,17 passages/giây`, trên GTX 1650 4 GB với batch size `1`. Đây là throughput
chậm nhưng nhất quán với cấu hình đã quan sát; không phải dấu hiệu tiến trình bị
treo.

Warnings `265 > 256` và `598 > 512` xuất hiện khi tái dựng corpus qua các
tokenizer candidate có cửa sổ ngắn hơn. Chúng không phải Qwen inference error:
exact Qwen snapshot có `max_position_embeddings=32768`, trong khi max observed
Qwen tokens là `560`.

Task 7 từng có một `TypeError` ở completion verification của Candidate 1. Lỗi
đó không thuộc Qwen dense inference, đã được correction trước khi Qwen target
được build, và không còn ảnh hưởng collection hiện tại.

## Giới hạn

Reviewer không tái encode toàn bộ `8460` Qwen dense vectors vì thao tác đó sẽ
lặp lại chính workload 65–70 phút mà không tương xứng với nghi vấn. Full scan
đã kiểm mọi dense structural/numeric invariant và mọi sparse vector; exact
model provenance được kiểm bằng 12 deterministic samples.

Audit này xác nhận integrity và provenance có chọn mẫu, không thay Phase 5
retrieval-quality benchmark. Chất lượng ranking trên câu hỏi thực tế phải được
đo theo design/metrics của Phase 5 sau khi User khởi động brainstorming.
