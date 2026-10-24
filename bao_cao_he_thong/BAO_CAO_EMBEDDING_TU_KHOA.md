# Báo cáo cho bạn: Vector nghĩa và từ khóa — embedding + BM25 (Phase 3)

**Cập nhật lần cuối: 19:58 24/10/2026 — bản 2: đưa về mẫu mới; sau khi gỡ code bản món ăn (24/10):
bộ nhúng và benchmark bản món ăn đã gỡ, notebook 03 sửa đúng 2 model ứng viên.**
Người viết: B · Review: A. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** biến mỗi đoạn tri thức thành hai dạng để tìm. **Vector nghĩa** (dense) tìm được
  câu cùng ý dù khác chữ. **Từ khóa** (sparse, BM25) giữ tín hiệu tên riêng như tên món, tên di tích.
  Đã đóng (bản toàn kho 12/09/2026, chỉnh ở Phase 7A2).
- **Đang chạy cách nào:** model `e5-small` (chạy trên máy, 384 số mỗi vector) phục vụ chatbot. Model thứ
  hai `qwen3-embedding-8b` (gọi qua OpenRouter) có trong code nhưng chưa có chỉ mục. BM25 dùng danh sách
  5.660 từ lập từ toàn bộ 8.459 đoạn, tách từ theo âm tiết.
- **Đo được:** chưa có số chất lượng riêng cho khâu này; chất lượng tìm đoạn chung (vector + từ khóa)
  nằm ở `BAO_CAO_TIM_KIEM.md`. Kiểm kỹ thuật: 33 test vector/từ khóa đạt; danh sách từ khóa build lại
  ra giống hệt từng byte.
- **Giới hạn chính:** BM25 tách theo âm tiết ("Đại", "Nội" tách rời); model 8B chưa build được chỉ mục ổn
  định (nhà cung cấp trả lỗi 504/429).
- **Chi phí / tốc độ:** e5-small không tốn tiền. Model 8B tính tiền theo token khi build.
- **Bạn cần quyết gì:** không ở khâu này; các hướng (tách từ tiếng Việt, 8B) bàn ở Phase 8.

## 2. Hoạt động thế nào (bản đang chạy)

```text
đoạn tài liệu -> thêm "passage: " -> e5-small -> vector 384 số, độ dài 1
câu hỏi      -> thêm "query: "   -> e5-small -> vector 384 số
mọi đoạn -> chữ thường, cắt theo chữ/số -> danh sách từ + độ hiếm của từ (IDF)
         -> lưu một lần vào data/full_corpus_builds/full_corpus_sparse_state.json
khi hỏi: vector lấy 30 đoạn gần nghĩa -> BM25 chấm lại 30 đoạn -> trộn thứ hạng (RRF, k=60) -> 10 đoạn
```

- Danh sách từ khóa ghi một lần; build sau phải ra đúng từng byte như file cũ, nếu không build dừng.
- Code: `backend/embedding/full_corpus.py` (2 model ứng viên `:43`, `:55`; thêm tiền tố `:82`, `:96`),
  `backend/embedding/sparse.py:23-24`, `backend/scoring/bm25.py:6-19`.

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Vector nghĩa bằng e5-small (chạy trên máy) | **Đã xử lý, đóng gói** | 8.459 vector trong chỉ mục đang chạy; `embedding/full_corpus.py:43` |
| Từ khóa BM25 cho toàn kho | **Đã xử lý, đóng gói** | 5.660 từ, k1 1,5, b 0,75; build lại giống từng byte; `scoring/bm25.py:15-16` |
| Từ ghép tiếng Việt trong BM25 | **Chưa thực hiện** | tách theo âm tiết (`scoring/bm25.py:6`, `:9-12`); Phase 8 thử ghép cặp âm tiết / tách từ |
| Model 8B qua OpenRouter | **Đã xử lý** (có code, chưa có chỉ mục) | pin nhà cung cấp Nebius, không cho lưu dữ liệu (`embedding/full_corpus.py:323`); build gặp 504; hoãn Phase 8 |
| Bốn model so trên mẫu nhỏ (e5-small, e5-base, huydang, Qwen-0.6B) | **Đã thử, chưa áp dụng** | chỉ chạy mẫu 12 đoạn (12/09); chưa chọn model thắng; Phase 7A2 thu về 2 model |
| Qwen-0.6B trên GPU máy (GTX 1650) | **Đã thử, chưa áp dụng** | chạy được (đỉnh VRAM ~1,23 GB) nhưng bị loại ở 7A2; nhánh GPU còn sót trong code (`embedding/full_corpus.py:203-210`) |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 24/10/2026 — Gỡ bộ nhúng và benchmark bản món ăn (bản 2)
Gỡ `embedding/embedder.py` (bản món ăn), `embedding/dense_benchmark.py` (trỏ collection đã xóa), các
benchmark trong `evaluation/`, notebook 08a/08b/08c; bỏ 2 hàm BM25 chỉ bản món ăn dùng. Notebook 03 chỉ
sửa phần chữ cho đúng 2 model hiện hành. Tiêu chí ghi trước: tìm kiếm giống từng byte, test bản toàn kho
đạt · kết quả **PASS**: 191 test đạt, giống từng byte, notebook 03 chạy hết không lỗi · tiền: 0.

### 24/10/2026 — Kiểm lại hiện trạng (bản 1, chỉ đọc)
Danh sách từ khóa: 8.459 đoạn, 5.660 từ, k1 1,5, b 0,75 (trước 8.460 / 5.662). Build record khớp danh
sách từ khóa. Qdrant: chỉ mục e5 8.459 point, có cả vector nghĩa và từ khóa. 33 test vector/từ khóa đạt.

### 24/10/2026 — Thu về 2 model, build lại chỉ mục (Phase 7A2)
Bỏ e5-base, huydang, Qwen-0.6B khỏi code toàn kho; thêm 8B qua OpenRouter (pin Nebius, không cho lưu dữ
liệu); build lại danh sách từ khóa trên corpus đã sửa (5.660 từ). Không pin nhà cung cấp thì vector lệch
(cos ~0,996); pin Nebius thì 10–30 giây mỗi lô và gặp 504 → **hoãn** chỉ mục 8B sang Phase 8.

### 12/09/2026 — Bản toàn kho
205 file, 8.460 đoạn; vector chỉ chạy trên mẫu 12 đoạn cho 4 model; Qwen-0.6B chạy GPU FP16 trên GTX
1650, đỉnh VRAM ~1,23 GB; danh sách từ khóa 5.662 từ, chạy lặp giống từng byte · **PASS** kỹ thuật; chưa
chọn model thắng.

### 25/08/2026 — Bản món ăn
572 đoạn × 384 số, độ dài 1, 26,13 giây trên CPU · **PASS** · từ khóa TF-IDF bản món ăn sau đó bỏ (Phase
4–5). Bản này nay đã gỡ (24/10).

## 5. Hôm nay còn đúng không

Kiểm với code (commit `1832201`) ngày 24/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| e5-small 384, tiền tố `passage: ` / `query: ` | **còn dùng** | `backend/embedding/full_corpus.py:43`, `:82`, `:96` |
| Bốn model ứng viên | **đã thay** bởi e5-small + Qwen3-8B qua OpenRouter (7A2) | `backend/embedding/full_corpus.py:43`, `:55` |
| e5-base, huydang, Qwen-0.6B trong code | **đã bỏ** (7A2); benchmark món ăn còn nhắc e5-base/huydang **đã gỡ ở B9** | grep `backend/*.py` không còn |
| Qwen-0.6B trên GPU | **đã bỏ** (lịch sử); nhánh GPU còn sót trong code | `backend/embedding/full_corpus.py:203-210`, `:240` |
| Module preflight embedding | **đã bỏ** (7A2 Gate 2) | grep `backend/` không còn |
| Định dạng danh sách từ khóa `phase_3_sparse_state:v1` | **còn dùng**; runtime từ chối định dạng khác | `backend/embedding/sparse.py:23`; `backend/retrieval/full_corpus.py:411-413` |
| Tách từ BM25 `\w+` chữ thường | **còn dùng**, chưa tách từ tiếng Việt | `backend/scoring/bm25.py:6`, `:9-12` |
| File danh sách từ khóa 5.662 từ | **đã thay** bởi `full_corpus_sparse_state.json`, 5.660 từ (7A2) | `backend/ingestion/full_corpus_pipeline.py:55` |
| Danh sách từ khóa ghi một lần, build sau phải giống hệt | **còn dùng** | `backend/ingestion/full_corpus_pipeline.py:122-131` |
| "OpenRouter embedding chưa làm" (25/08) | **đã thay** bởi bộ gọi OpenRouter pin Nebius (7A2) | `backend/embedding/full_corpus.py:323` |
| Từ khóa TF-IDF bản món ăn | **đã bỏ** (Phase 4–5) | report Phase 3 |
| Bộ nhúng `E5Embedder` bản món ăn | **đã bỏ** (gỡ ở B9) | file `backend/embedding/embedder.py` không còn |
| `dense_benchmark.py` và benchmark trong `evaluation/` | **đã bỏ** (gỡ ở B9) | các file không còn; notebook 08a/b/c đã xóa |

## 6. Việc còn lại / cần quyết

- Chỉ mục 8B hoãn sang Phase 8; build lại cần cách gọi chịu được 504/429.
- BM25 tiếng Việt (ghép cặp âm tiết hoặc tách từ) là giả thuyết đo ở Phase 8.
- Gỡ nhánh GPU còn sót trong `embedding/full_corpus.py` — Phase 8.1.
- Corpus đổi thì phải xóa danh sách từ khóa cũ trước khi build lại (bẫy đã biết).
- Câu "mỗi đoạn vừa e5-base 512 / huydang 256" đã kiểm lại trên 8.459 đoạn ở báo cáo Chia đoạn (dài nhất
  366/512, 255/256).

## Phụ lục — hồ sơ kỹ thuật

- Report lịch sử: `reports/user_reports/phase_3_embedding_sparse_representation_user_report.md`;
  7A2 `reports/phase_7a2_gate_2_reindex_implementation_2026_10_24.md`.
- Tên kỹ thuật: vector nghĩa = dense; từ khóa = sparse/BM25; danh sách từ khóa = sparse state; model 8B
  = `qwen3-embedding-8b-4096`; model đang chạy = `e5-small-384` (`intfloat/multilingual-e5-small`).
- Bản 1: B8, 24/10/2026. Bản 2: B10, sau dọn B9 (commit `1832201`).
- **Lệch đã ghi ở bản 1 và trạng thái hôm nay:**
  1. Notebook 03 còn tả 4 model và preflight — **đã sửa ở B9** (chỉ phần chữ; chạy hết không lỗi).
  2. `embedding/dense_benchmark.py` trỏ collection `hue_foods_08a_*` đã xóa — **đã gỡ ở B9**.
  3. Nhánh GPU/FP16 chỉ phục vụ Qwen-0.6B đã bỏ vẫn còn (`embedding/full_corpus.py:203-210`) — **còn**, Phase 8.1.
