# Báo cáo cho bạn: Vector nghĩa và từ khóa — embedding + BM25 (Phase 3, thử nghiệm Phase 8)

**Cập nhật lần cuối: 17:10 31/10/2026 — bản 5: rà lại cho đúng hiện trạng, xoá phần không còn đúng (User 31/10).**
Các bản trước: xem `git log` file này. Người viết: agent con của A (bản 5) · Review: A. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** biến mỗi đoạn tri thức thành hai dạng để tìm. **Vector nghĩa** (dense) tìm được câu cùng ý dù khác chữ.
  **Từ khóa** (sparse, BM25) giữ tín hiệu tên riêng như tên món, tên di tích. Đã đóng (bản toàn kho 12/09/2026, chỉnh ở Phase 7A2).
- **Đang chạy cách nào:** model `e5-small` (chạy trên máy, CPU, 384 số mỗi vector) cho cả đoạn và câu hỏi. BM25 dùng danh sách
  **5.631 từ** lập từ **8.424 đoạn** (kho sau hai đợt sửa, build lại 30/10), tách từ theo âm tiết. Câu hỏi được chuẩn hóa Unicode
  (NFC — gộp dấu tách rời thành ký tự có dấu) trước khi tìm (từ 28/10).
- **Đo được:** chưa có số chất lượng riêng cho khâu này; chất lượng tìm đoạn chung (vector + từ khóa) ở `BAO_CAO_TIM_KIEM.md`. Kiểm kỹ
  thuật: danh sách từ khóa build lại ra giống hệt từng byte (test đạt sau build lại 30/10).
- **Đã thử để cải thiện (Phase 8):**
  - **model vector lớn Qwen3-Embedding-8B** thay e5-small (30/10): **kém hơn** — 3 / 40 câu mất đoạn đúng (luật: không được mất câu
    nào), chậm hơn ~100 lần ở bước này (2,2 s / câu hỏi qua mạng) ⇒ **không chọn**, giữ e5-small;
  - 5 cách đổi phần từ khóa (25/10: ghép cặp âm tiết, tách từ `pyvi`, giữ mã số, bỏ dấu cả kho, chỉnh tham số): không cách nào tốt hơn
    ⇒ giữ tách theo âm tiết.
- **Giới hạn chính:** BM25 tách theo âm tiết ("Đại", "Nội" tách rời); câu gõ **không dấu** gần như không tìm được (8.1: 1 / 32 câu còn
  đủ đoạn đúng, so với 13 / 32 khi có dấu) — **ngoài phạm vi** (bạn quyết 25/10); nhãn đoạn đúng chỉ 40 + 15 câu ⇒ chỉ thấy khác biệt lớn.
- **Chi phí / tốc độ:** 0 đồng (chạy trên máy); tạo vector câu hỏi ~0,02 s.
- **Bạn cần quyết gì:** không.

## 2. Hoạt động thế nào (bản đang chạy)

```text
đoạn tài liệu -> thêm "passage: " -> e5-small -> vector 384 số, độ dài 1
mọi đoạn -> chữ thường, cắt theo chữ/số -> danh sách từ + độ hiếm của từ (IDF)
         -> lưu một lần vào data/full_corpus_builds/full_corpus_sparse_state.json
khi hỏi: câu hỏi -> chuẩn hóa NFC -> thêm "query: " -> e5-small -> vector 384 số
         -> vector lấy 30 đoạn gần nghĩa -> BM25 chấm lại 30 đoạn đó
         -> trộn hai thứ hạng (RRF, k = 60) -> 10 đoạn đầu vào ngữ cảnh cho model trả lời
```

- Danh sách từ khóa ghi một lần; build sau phải ra đúng từng byte như file đang có, nếu không build dừng ⇒ kho đổi thì phải xoá file
  cũ trước khi build lại.
- Code: `backend/embedding/full_corpus.py` (e5-small `:43`; thêm tiền tố `:82`, `:96`), `backend/embedding/sparse.py:19-20`,
  `backend/scoring/bm25.py:6-19`, `backend/retrieval/full_corpus.py` (NFC `:97-102`; 30 ứng viên, k = 60 `:401-402`),
  `backend/ingestion/full_corpus_pipeline.py:137-146` (ghi một lần / kiểm giống byte).

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Vector nghĩa bằng e5-small (chạy trên máy) | **Đã xử lý, đóng gói** | 8.424 vector trong chỉ mục đang chạy (dựng lại 30/10); `embedding/full_corpus.py:43` |
| Từ khóa BM25 cho toàn kho | **Đã xử lý, đóng gói** | 5.631 từ (30/10), k1 1,5, b 0,75; build lại giống từng byte; `scoring/bm25.py:15-16` |
| Từ ghép tiếng Việt trong BM25 | **Đã thử, chưa áp dụng** | 8.1: ghép cặp âm tiết và `pyvi` đều kém hơn (mất 1–4 câu đoạn đúng); vẫn tách theo âm tiết (`scoring/bm25.py:6`, `:9-12`) |
| Mã số / số nguyên cụm (ví dụ số nhà, giá) | **Đã thử, chưa áp dụng** | 8.1: không khác (0 câu đổi) |
| Câu hỏi gõ không dấu | **Chưa thực hiện** — ngoài phạm vi (bạn quyết 25/10) | 8.1 đo: gần như hỏng (1 / 32). Bỏ dấu cả kho giúp câu không dấu nhưng hại câu có dấu |
| Tham số BM25 (b) và trộn thứ hạng (k) | **Đã thử, chưa áp dụng** | 8.1: k 10 / 30, b 0,5 / 1,0, không cái nào tốt hơn; giữ k1 1,5, b 0,75, k 60 |
| Chuẩn hóa Unicode câu hỏi (NFC) | **Đã xử lý, đóng gói** (28/10) | 8.1 đo: câu dạng tách dấu làm điểm thứ hạng (MRR) tụt 0,20; `retrieval/full_corpus.py:97-102` |
| Model lớn Qwen3-Embedding-8B qua mạng thay e5-small | **Đã thử, chưa áp dụng** (30/10) | 3 / 40 câu mất đoạn đúng (sàn 0), nhóm kiểm cũng mất 3 / 15; +2,2 s mỗi câu hỏi (cho phép +0,05 s); 0,0089 USD ⇒ **kém hơn**; chỉ mục thử đã xoá. Code gọi model vẫn ở `embedding/full_corpus.py:55`, `:278-379` |
| Bốn model so trên mẫu nhỏ (e5-small, e5-base, huydang, Qwen-0.6B) | **Đã thử, chưa áp dụng** | chỉ chạy mẫu 12 đoạn (12/09), chưa chọn model thắng; Phase 7A2 thu về 2 model (e5-small + Qwen3-8B) |
| Qwen-0.6B trên GPU máy (GTX 1650) | **Đã thử, chưa áp dụng** | chạy được (đỉnh VRAM ~1,23 GB) nhưng bị loại ở 7A2; nhánh GPU trong bộ tạo vector đã gỡ 26/10 (nay chỉ CPU, `embedding/full_corpus.py:197-230`) |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 30/10/2026 — Thử Qwen3-Embedding-8B thay e5-small (B chạy, C kiểm)
- **Thử gì:** chỉ đổi model vector sang model lớn (4.096 số, gọi qua OpenRouter, ghim một nhà cung cấp, không cho lưu dữ liệu); từ khóa,
  cách trộn, 10 đoạn, prompt, model trả lời giữ nguyên. Luật ghi trước: phải thắng rõ, **sàn 0 câu mất đoạn đúng**.
- **Kết quả:** chỉ mục thử đủ 8.424 đoạn (~31 phút, 0 lỗi). 40 câu thử: 2 tốt hơn / 35 như cũ / **3 mất đoạn đúng** (đo lại: đúng 3 câu
  đó); 15 câu kiểm: 2 / 10 / 3. Tạo vector câu hỏi 21 ms ⇒ **2,2 s** (câu chậm 6,5–7,2 s) ⇒ cả câu ước ~11 s, gấp đôi trần 5 s. Tiền 0,0089 USD.
- **Bỏ vì:** vỡ sàn và quá chậm. Phần còn thiếu lớn hơn là **xếp hạng** (9 / 40 câu có đoạn đúng trong 30 ứng viên nhưng rơi khỏi 10
  đoạn) — việc của khâu tìm, không phải model vector. Chỉ mục thử đã xoá; bộ đệm vector: bạn quyết không giữ ("kém hơn thì chỉ cần ghi lại
  kết quả", 30/10). Report: `report_agent/2026-10-27_phan_ton_phase_cu/qwen3_8b_implementation.md`.

### 28/10 và 30/10/2026 — Build lại sau hai đợt sửa kho
Danh sách từ khóa tính lại trên kho mới: 5.660 ⇒ **5.631 từ** (28/10, 8.426 đoạn), giữ 5.631 sau đợt 2 (30/10, 8.424 đoạn). Không đổi
cách tạo vector hay tách từ. Report: `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md`.

### 28/10/2026 — Chuẩn hóa NFC câu hỏi vào chatbot
Một dòng chuẩn hóa trước khi tìm; câu đã NFC giữ nguyên từng byte. Vào chatbot cùng thay đổi "đưa 10 đoạn" (Phase 8.2).

### 25/10/2026 — Phase 8.1: thử phần từ khóa (B làm, C kiểm)
Đo trên 32 câu có đoạn đúng, cả hai cách trộn (đang chạy: BM25 chỉ chấm lại 30 đoạn của vector; mở rộng: BM25 tự tìm 100 đoạn trong cả
kho). Luật ghi trước: không câu nào mất đoạn đúng, điểm từ khóa không tụt quá 2 điểm %, phải tốt lên có ý nghĩa. Tính trong bộ nhớ, đã
kiểm khớp code đang chạy (108 / 108 câu giống hệt). Tiền: 0.

| Thử | Kết quả | Giữ / bỏ |
|---|---|---|
| Ghép cặp âm tiết | mất 1 câu (đang chạy), 3 câu (mở rộng) | bỏ |
| Tách từ `pyvi` | mất 1 câu / 4 câu | bỏ |
| Giữ mã số nguyên cụm | không đổi câu nào | không cần |
| Bỏ dấu cả kho + câu hỏi | câu có dấu: mất 2 / 4 câu. Câu không dấu (máy bỏ dấu từ câu có sẵn), cách mở rộng: 2 / 32 ⇒ 5 / 32 câu đủ đoạn đúng — chưa đủ gọi là tốt hơn | bỏ; câu không dấu sau đó bạn xếp ngoài phạm vi |
| Chỉnh b (0,5 / 1,0) và k trộn (10 / 30) | tốt nhất chỉ +1 câu; vài cách mất 1–2 câu | giữ mặc định |

Report: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g4_keyword_implementation.md`.

### 24/10/2026 — Thu về 2 model, gỡ code cũ (Phase 7A2 + dọn code)
Bỏ e5-base, huydang, Qwen-0.6B khỏi code toàn kho; thêm Qwen3-8B qua OpenRouter (ghim nhà cung cấp Nebius — không ghim thì vector lệch
giữa các lần gọi); chỉ mục 8B hoãn tới Phase 8 (gặp lỗi 504). Gỡ bộ tạo vector, benchmark và notebook bản món ăn; kết quả tìm giống
từng byte · **PASS** · 0 USD.

### 12/09/2026 — Bản toàn kho
205 file, 8.460 đoạn; vector chỉ chạy trên mẫu 12 đoạn cho 4 model; danh sách từ khóa 5.662 từ, chạy lặp giống từng byte · **PASS**
kỹ thuật; chưa chọn model thắng.

### 25/08/2026 — Bản món ăn (đã gỡ 24/10)
572 đoạn × 384 số, 26,13 giây trên CPU · **PASS**; từ khóa TF-IDF bản món ăn bỏ ở Phase 4–5.

## 5. Hôm nay còn đúng không

Kiểm với code `main` (commit `1985a81`) ngày 31/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| e5-small 384, tiền tố `passage: ` / `query: `, chạy CPU | **còn dùng** | `backend/embedding/full_corpus.py:43`, `:82`, `:96`, `:197-230` |
| Model vector trong code: e5-small + Qwen3-8B | **còn** cả hai trong code; chatbot dùng e5-small; 8B đã thử 30/10 và bỏ | `backend/config/settings.yaml:42`; `backend/embedding/full_corpus.py:55`, `:278-379` |
| e5-base, huydang, Qwen-0.6B, nhánh GPU, code bản món ăn | **đã gỡ** khỏi bộ tạo vector (7A2 24/10; nhánh GPU 26/10, commit `9f7ad43`); tên e5-base / huydang chỉ còn ở phần kiểm token khi chia đoạn | grep `backend/embedding/` không còn (chỉ còn lệnh dọn bộ nhớ GPU khi đóng, `full_corpus.py:274-275`, vô hại); `settings.yaml:28-35` |
| Định dạng danh sách từ khóa `phase_3_sparse_state:v1` | **còn dùng**; lúc chạy từ chối định dạng khác | `backend/embedding/sparse.py:19`; `backend/retrieval/full_corpus.py:380-381` |
| Tách từ BM25 theo chữ / số, chữ thường | **còn dùng**; 8.1 thử cách khác, không tốt hơn | `backend/scoring/bm25.py:6`, `:9-12` |
| BM25 k1 1,5 / b 0,75, trộn thứ hạng k 60 | **còn dùng**; 8.1 thử b 0,5 / 1,0 và k 10 / 30, không tốt hơn | `backend/scoring/bm25.py:15-16`; `backend/retrieval/full_corpus.py:402` |
| Danh sách từ khóa | **5.631 từ** trên 8.424 đoạn từ 30/10 (trước: 5.660 từ 24/10, 5.662 ngày 12/09) | `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` (`sparse.vocabulary_size`) |
| Danh sách từ khóa ghi một lần, build sau phải giống hệt | **còn dùng** | `backend/ingestion/full_corpus_pipeline.py:137-146` |

## 6. Việc còn lại / cần quyết

- Không đề xuất lại Qwen3-8B làm model vector chính nếu không có lý do mới (ví dụ bộ câu có nhãn lớn hơn nhiều, hoặc chạy được trên máy).
- BM25 tiếng Việt (ghép cặp âm tiết, `pyvi`): đã đo ở 8.1, không tốt hơn — không đề xuất lại nếu không có lý do mới.
- Câu gõ không dấu: ngoài phạm vi (bạn quyết 25/10); nếu mở lại, hướng đã thấy là chỉ bật bản bỏ dấu khi câu hỏi không có dấu nào,
  đo bằng câu không dấu thật của người dùng.
- Kho đổi thì phải xoá danh sách từ khóa cũ trước khi build lại (bẫy đã biết).
- Đoạn dài nhất 255 / 256 token theo tokenizer huydang (đo 30/10, `BAO_CAO_CHIA_DOAN.md`) — sát trần của ràng buộc cũ, chatbot không dùng model đó.

## Phụ lục — hồ sơ kỹ thuật

- Report lịch sử: `reports/user_reports/phase_3_embedding_sparse_representation_user_report.md`;
  7A2 `reports/phase_7a2_gate_2_reindex_implementation_2026_10_24.md`.
- Tên kỹ thuật: vector nghĩa = dense; từ khóa = sparse / BM25; danh sách từ khóa = sparse state (sha `c8134c49a648` từ 30/10); model
  8B = `qwen3-embedding-8b-4096`; model đang chạy = `e5-small-384` (`intfloat/multilingual-e5-small`); trộn thứ hạng = RRF; cách trộn
  "đang chạy" = `dense_bm25_rrf`, "mở rộng" = `native_hybrid_rrf` pool 100.
- **Qwen3-8B (30/10, harness B92, review C88 / C95):** plan `report_agent/2026-10-27_phan_ton_phase_cu/qwen3_8b_plan.md` (A duyệt `d6d6c7d51584`), report
  `qwen3_8b_implementation.md` (review C95 `qwen3_8b_review.md`); harness ở tag `hoso/b92-qwen3-harness` (không merge). Chỉ số quyết
  `context_gold_all` 0,600 ⇒ 0,575 [−0,125; +0,075]; `pool_dense_gold_all` 33 ⇒ 31 / 40; nhãn gold v5.
- **8.1 phần từ khóa** (B18, review C): plan `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g4_keyword_plan.md`, report
  `phase_8_1_g4_keyword_implementation.md`, review `phase_8_1_g4_keyword_review.md`, harness `backend/experiments/phase_8_1/g4_keyword.py`.
  Mã biến thể: T1 = ghép cặp âm tiết, T2 = mã nguyên cụm, T3 = `pyvi`, E = bỏ dấu, P = tham số. Số 8.1 tính bằng nhãn v1 trên kho cũ.
- NFD / NFC câu hỏi: G1.4 (`phase_8_1_g1_implementation.md` §4); vào chatbot ở B1 (`510e1a8`, 28/10).
- Dọn code: B9 (24/10, commit `1832201`); nhánh GPU / float16 gỡ ở `9f7ad43` (26/10, rà code).
