# Báo cáo cho bạn: Vector nghĩa và từ khóa — embedding + BM25 (Phase 3, thử nghiệm 8.1)

**Cập nhật lần cuối: 15:59 30/10/2026 — bản 4: đã thử model lớn Qwen3-Embedding-8B thay e5-small — kém hơn, không chọn; số đoạn / từ khóa theo
kho sau hai đợt sửa; chuẩn hóa NFC câu hỏi đã vào chatbot (28/10); chatbot không đổi.** Trước đó: 14:04 25/10/2026 — bản 3 (thử từ khóa 8.1).
Người viết: B (bản 1–2, 4), C (bản 3) · Review: A (bản 1–2, 4), B (bản 3). Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** biến mỗi đoạn tri thức thành hai dạng để tìm. **Vector nghĩa** (dense) tìm được
  câu cùng ý dù khác chữ. **Từ khóa** (sparse, BM25) giữ tín hiệu tên riêng như tên món, tên di tích.
  Đã đóng (bản toàn kho 12/09/2026, chỉnh ở Phase 7A2).
- **Đang chạy cách nào:** model `e5-small` (chạy trên máy, 384 số mỗi vector) phục vụ chatbot — **giữ nguyên** sau thí nghiệm 30/10. BM25 dùng
  danh sách **5.631 từ** lập từ **8.424 đoạn** (kho sau hai đợt sửa), tách từ theo âm tiết. Câu hỏi được chuẩn hóa Unicode NFC trước khi tìm (từ 28/10).
- **Mới (30/10) — thử Qwen3-Embedding-8B** (model lớn, 4.096 số mỗi vector, gọi qua mạng, bạn duyệt 29/10):
  - dựng chỉ mục thử đầy đủ trên kho hiện tại: 8.424 đoạn, ~31 phút, 0 lỗi, chỉ dùng một nhà cung cấp đã ghim (vector ổn định);
  - **kết quả: kém hơn** — trên 40 câu thử có nhãn đoạn đúng, 2 câu tốt hơn nhưng **3 câu mất đoạn đúng** (luật ghi trước: không được mất câu nào); đo lại lần
    hai mất đúng 3 câu đó; nhóm kiểm 15 câu cũng 2 tốt / 3 mất;
  - **chậm hơn nhiều:** biến câu hỏi thành vector mất trung vị **2,2 s** (e5: 0,02 s), câu chậm 6,5–7,2 s ⇒ cả câu ước ~11 s, gấp đôi trần 5 s bạn chốt;
  - **không đưa vào chatbot**; chỉ mục thử đã xóa; tiền **0,0089 USD**.
- **Đo được:** chưa có số chất lượng riêng cho khâu này; chất lượng tìm đoạn chung (vector + từ khóa)
  nằm ở `BAO_CAO_TIM_KIEM.md`. Kiểm kỹ thuật: 33 test vector/từ khóa đạt; danh sách từ khóa build lại
  ra giống hệt từng byte.
- **8.1 (25/10) đã thử phần từ khóa:**
  - ghép cặp âm tiết, giữ nguyên mã số, tách từ tiếng Việt bằng `pyvi`, bỏ dấu cả kho, chỉnh hai tham số BM25;
  - **không cách nào tốt hơn cách đang chạy** ⇒ giữ tách theo âm tiết; vài cách còn làm rơi đoạn đúng của 1–4 câu.
- **Phát hiện đáng giá:**
  - câu hỏi **gõ không dấu** làm phần tìm đoạn gần như hỏng: chỉ 1/32 câu còn đủ đoạn đúng, so với 13/32 khi có dấu;
  - bản bỏ dấu tìm lại được nhiều hơn hẳn với câu không dấu, nhưng làm hại câu có dấu.
- **Giới hạn chính:** BM25 tách theo âm tiết ("Đại", "Nội" tách rời); câu gõ không dấu gần như không tìm được (ngoài phạm vi, bạn
  quyết 25/10); nhãn đoạn đúng chỉ 40 + 15 câu ⇒ chỉ thấy khác biệt lớn.
- **Chi phí / tốc độ:** e5-small không tốn tiền, ~0,02 s / câu hỏi. Model 8B: dựng chỉ mục ~0,009 USD, mỗi câu hỏi phải gọi mạng (~2,2 s).
- **Bạn cần quyết gì:** có xóa **bộ đệm vector 8B** (133 MB, private) không — giữ thì thử lại 8B ở khâu khác (vd xếp hạng lại) không tốn tiền nhúng kho, khi
  kho chưa đổi.

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
| Vector nghĩa bằng e5-small (chạy trên máy) | **Đã xử lý, đóng gói** | 8.424 vector trong chỉ mục đang chạy (dựng lại 30/10, đợt 2 sửa kho); `embedding/full_corpus.py:43` |
| Từ khóa BM25 cho toàn kho | **Đã xử lý, đóng gói** | 5.631 từ (28/10, giữ sau đợt 2), k1 1,5, b 0,75; build lại giống từng byte; `scoring/bm25.py:15-16` |
| Từ ghép tiếng Việt trong BM25 | **Đã thử, chưa áp dụng** | 8.1: ghép cặp âm tiết và `pyvi` đều kém hơn (mất 1–4 câu đoạn đúng); vẫn tách theo âm tiết (`scoring/bm25.py:6`, `:9-12`) |
| Mã số / số nguyên cụm (ví dụ biển số đường, giá) | **Đã thử, chưa áp dụng** | 8.1: không khác (0 câu đổi) |
| Câu hỏi gõ không dấu | **Chưa thực hiện** — ngoài phạm vi (bạn quyết 15:15 25/10) | 8.1 đo: gần như hỏng (1/32). Bỏ dấu cả kho giúp câu không dấu nhưng hại câu có dấu ⇒ chưa dùng |
| Tham số BM25 (b) và trộn thứ hạng (k) | **Đã thử, chưa áp dụng** | 8.1: k 10 / 30, b 0,5 / 1,0, không cái nào tốt hơn; giữ k1 1,5, b 0,75, k 60 |
| Chuẩn hóa Unicode câu hỏi (NFC) | **Đã xử lý, đóng gói** (28/10, Phase 8.2 B1) | 8.1 đo: câu dạng NFD làm MRR tụt 0,20; nay chuyển về NFC trước khi tìm (`retrieval/full_corpus.py` `normalize_query`) |
| Model 8B qua OpenRouter thay e5-small | **Đã thử, chưa áp dụng** (30/10) | chỉ mục thử 8.424 đoạn, 0 lỗi, pin Nebius; đoạn đúng trong ngữ cảnh: 2 câu tốt / **3 câu mất** (sàn 0) trên 40 câu thử, ổn định 2 lượt; nhóm kiểm 2 / 3 ⇒ **kém hơn**; câu hỏi +2,2 s (trần cho phép +0,05 s); 0,0089 USD; chỉ mục thử đã xóa. Code gọi 8B vẫn trong `embedding/full_corpus.py:55`, `:282-372` |
| Bốn model so trên mẫu nhỏ (e5-small, e5-base, huydang, Qwen-0.6B) | **Đã thử, chưa áp dụng** | chỉ chạy mẫu 12 đoạn (12/09); chưa chọn model thắng; Phase 7A2 thu về 2 model |
| Qwen-0.6B trên GPU máy (GTX 1650) | **Đã thử, chưa áp dụng** | chạy được (đỉnh VRAM ~1,23 GB) nhưng bị loại ở 7A2; nhánh GPU còn sót trong code (`embedding/full_corpus.py:203-210`) |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 30/10/2026 — Thử Qwen3-Embedding-8B thay e5-small (B chạy, C kiểm)

- **Câu hỏi:** model vector lớn (4.096 số, gọi qua OpenRouter, pin nhà cung cấp Nebius, không cho lưu dữ liệu) có đưa đoạn có đáp án vào 10 đoạn ngữ cảnh nhiều
  hơn e5-small không, với giá nào về tiền và độ trễ? Chỉ đổi đúng model vector; từ khóa, cách trộn, 10 đoạn, prompt, model trả lời giữ nguyên.
- **Tiêu chí ghi trước** (plan duyệt + review): chỉ số quyết = số câu (40 câu thử có nhãn) mà 10 đoạn ngữ cảnh chứa **đủ mọi đoạn đúng**, so theo cặp, phải
  thắng có ý nghĩa (≥ 4 thắng / 0 thua…); **sàn: 0 câu mất đoạn đúng**; nhóm kiểm 15 câu chỉ để "không làm hỏng"; độ trễ / tiền báo kèm.
- **Mốc e5** đo lại trên kho đợt 2 (2 lần, giống hệt): 24 / 40 câu đủ đoạn đúng; 16 câu còn thiếu — 9 câu đoạn đúng có trong 30 ứng viên theo nghĩa nhưng rơi khỏi
  10 đoạn, 7 câu thiếu ngay ở 30 ứng viên (chỗ model vector tốt hơn có thể giúp).
- **Dựng chỉ mục 8B:** thử nhỏ trước (2 lô + nhúng lại 20 đoạn: vector lần hai giống lần một, cos ≥ 0,9999 — khác lần 7A2 khi chưa ghim nhà cung cấp) ⇒ cả kho
  8.424 đoạn 14:57–15:28 (~31 phút), 0 lỗi, 0 lần thử lại.
- **Kết quả tìm:** 40 câu thử: **2 thắng / 35 hòa / 3 thua** (3 câu mất đoạn đúng — sàn vỡ); đo lần hai cùng chỉ mục: đúng 3 câu đó; 15 câu kiểm: 2 / 10 / 3. Các
  chỉ số theo dõi (30 ứng viên theo nghĩa, MRR) "không khác". Vector câu hỏi giữa hai lần gọi hơi khác (cos ~0,9999) làm thứ tự top-10 đổi ở 27 / 108 câu.
- **Độ trễ:** bước biến câu hỏi thành vector: e5 21 ms ⇒ 8B **2.228 ms** (trung vị), 6.487–7.240 ms (câu chậm, p95); cả câu ước ~11,4 s so với trần 5 s.
  Lượt nhóm kiểm còn chậm hơn: 1 lần lỗi 504 sau ~62 s, 17 lần gọi thành công > 5 s (chậm nhất 75 s) — đuôi chậm do phía nhà cung cấp.
- **Kết luận: kém hơn** · không chạy phần sinh câu trả lời · chatbot giữ e5-small · chỉ mục thử **đã xóa** · tiền **0,0089 USD** (trần 0,10).
- **Ý nghĩa cho bạn:** với kho tiếng Việt này và 10 đoạn ngữ cảnh, model nhỏ chạy trên máy vừa đủ tốt vừa nhanh hơn ~100 lần ở bước này; model lớn qua mạng không
  đáng đổi. 8B cũng không kéo thêm đoạn đúng vào 30 ứng viên (33 ⇒ 31 / 40 câu). Phần thiếu lớn hơn còn lại là **xếp hạng** (9 câu có đoạn đúng trong
  30 ứng viên nhưng rơi khỏi 10 đoạn) — đó là việc của khâu tìm kiếm / xếp hạng lại, không phải của model vector.

### 25/10/2026 — Phase 8.1: thử phần từ khóa (B làm, C kiểm)

- **Câu hỏi:** đổi cách tách từ / bỏ dấu / tham số của BM25 có giúp đoạn có đáp án lọt vào 5 đoạn đưa model không?
- **Cách đo:** đo trên cả hai cách trộn:
  - đang chạy: BM25 chỉ chấm lại 30 đoạn của vector;
  - mở rộng: BM25 tự tìm 100 đoạn trong cả kho.

  Tính trong bộ nhớ, công thức kiểm khớp code đang chạy: 195/200 cặp điểm giống từng bit, 5 cặp lệch ≤ 8,9e-16 (sai số làm
  tròn); kết quả tìm của cách đang chạy giống hệt 108/108 câu. Không tạo chỉ mục mới.
- **Tập đo:** 32 câu thử có đoạn đúng.
- **Tiêu chí ghi trước:**
  - sàn: không câu nào mất đoạn đúng;
  - keyword không tụt quá 2 điểm %;
  - phải tốt lên có ý nghĩa sau hiệu chỉnh nhiều phép so.

| Thử | Kết quả | Giữ / bỏ |
|---|---|---|
| Ghép cặp âm tiết | mất 1 câu (đang chạy), 3 câu (mở rộng) | bỏ |
| Tách từ `pyvi` | mất 1 câu / 4 câu | bỏ |
| Giữ mã số nguyên cụm | không đổi câu nào | không cần |
| Bỏ dấu cả kho + câu hỏi | câu có dấu: mất 2 / 4 câu ⇒ kém hơn. Câu không dấu, cách mở rộng: đoạn đúng lọt nhóm 100 đoạn từ khóa 25% → 81%, top-10 13% → 34%, 5 đoạn 2/32 → 5/32 (chưa đủ để gọi là tốt hơn) | bỏ ở dạng này; tín hiệu cho 8.2 |
| Chỉnh b (0,5 / 1,0) và k trộn (10 / 30) | tốt nhất chỉ +1 câu; b 1,0 (cả hai cách trộn) và b 0,5 (cách mở rộng) làm mất 1–2 câu | giữ mặc định |

- Kết quả: **PASS** cho cổng kiểm khớp; **không biến thể nào tốt hơn**; xác nhận trên bộ kiểm NOT RUN (không có gì để xác
  nhận).
- Tiền: **0 USD**.

**Ý nghĩa cho bạn:**
- Cách tách từ đơn giản đang chạy là đủ tốt với bộ câu hiện có.
- Điểm yếu thật là người dùng gõ không dấu. Bỏ dấu giúp nhóm câu đó, nhưng chỉ nên bật khi câu hỏi không có dấu nào.
- Việc đó cần đo riêng ở 8.2, bằng câu không dấu thật của người dùng. Câu không dấu trong lần thử này do máy bỏ dấu từ câu có
  sẵn.

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

Kiểm với code (commit `1832201`) ngày 24/10/2026; các dòng 8.1 kiểm ngày 25/10/2026 (chatbot không đổi); dòng 8B, NFC, số đoạn / từ khóa kiểm ngày
30/10/2026 (commit `bfb0b41`).

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| e5-small 384, tiền tố `passage: ` / `query: ` | **còn dùng** | `backend/embedding/full_corpus.py:43`, `:82`, `:96` |
| Bốn model ứng viên | **đã thay** bởi e5-small + Qwen3-8B qua OpenRouter (7A2) | `backend/embedding/full_corpus.py:43`, `:55` |
| e5-base, huydang, Qwen-0.6B trong code | **đã bỏ** (7A2); benchmark món ăn còn nhắc e5-base/huydang **đã gỡ ở B9** | grep `backend/*.py` không còn |
| Qwen-0.6B trên GPU | **đã bỏ** (lịch sử); nhánh GPU còn sót trong code | `backend/embedding/full_corpus.py:203-210`, `:240` |
| Module preflight embedding | **đã bỏ** (7A2 Gate 2) | grep `backend/` không còn |
| Định dạng danh sách từ khóa `phase_3_sparse_state:v1` | **còn dùng**; runtime từ chối định dạng khác | `backend/embedding/sparse.py:23`; `backend/retrieval/full_corpus.py:411-413` |
| Tách từ BM25 `\w+` chữ thường | **còn dùng**; 8.1 đã thử các cách tách khác, không cách nào tốt hơn | `backend/scoring/bm25.py:6`, `:9-12`; `phase_8_1_g4_keyword_implementation.md` |
| BM25 k1 1,5 / b 0,75, trộn thứ hạng k 60 | **còn dùng**; 8.1 thử b 0,5 / 1,0 và k 10 / 30, không tốt hơn | `backend/scoring/bm25.py:15-16`; như trên |
| File danh sách từ khóa 5.662 từ | **đã thay** bởi `full_corpus_sparse_state.json`, 5.660 từ (7A2) | `backend/ingestion/full_corpus_pipeline.py:55` |
| Danh sách từ khóa ghi một lần, build sau phải giống hệt | **còn dùng** | `backend/ingestion/full_corpus_pipeline.py:122-131` |
| "OpenRouter embedding chưa làm" (25/08) | **đã thay** bởi bộ gọi OpenRouter pin Nebius (7A2) | `backend/embedding/full_corpus.py:323` |
| "8B hoãn sang Phase 8, chưa có chỉ mục" (7A2) | **đã thay** 30/10: đã dựng chỉ mục thử + đo ⇒ kém hơn, không chọn; chỉ mục thử đã xóa | `report_agent/2026-10-27_phan_ton_phase_cu/qwen3_8b_implementation.md` |
| Danh sách từ khóa 5.660 từ / 8.459 đoạn (7A2) | **đã thay** bởi 5.631 từ (28/10) / 8.424 đoạn (30/10) | `data/full_corpus_builds/` (build record `51fb1ec63cbc`) |
| Từ khóa TF-IDF bản món ăn | **đã bỏ** (Phase 4–5) | report Phase 3 |
| Bộ nhúng `E5Embedder` bản món ăn | **đã bỏ** (gỡ ở B9) | file `backend/embedding/embedder.py` không còn |
| `dense_benchmark.py` và benchmark trong `evaluation/` | **đã bỏ** (gỡ ở B9) | các file không còn; notebook 08a/b/c đã xóa |

## 6. Việc còn lại / cần quyết

- ~~Chỉ mục 8B hoãn sang Phase 8~~ — **đã thử 30/10, kém hơn** (§4). Không đề xuất lại 8B làm model vector chính nếu không có lý do mới (vd bộ câu có nhãn lớn hơn
  nhiều, hoặc chạy được trên máy). Bộ đệm vector 8B (133 MB, private) giữ / xóa: bạn quyết.
- BM25 tiếng Việt (ghép cặp âm tiết, `pyvi`): **đã đo ở 8.1, không tốt hơn**. Không đề xuất lại nếu không có lý do mới.
- **Đề xuất 8.2:**
  - ~~bật bản bỏ dấu chỉ khi câu hỏi không có dấu~~ — **Bạn quyết 15:15 25/10: ngoài phạm vi** — thiết kế giả định người dùng gõ có dấu; không làm ở 8.2. Ghi chú cũ: (phát hiện đơn giản), câu có dấu giữ như cũ; đo bằng câu không dấu thật
    của người dùng;
  - chuẩn hóa NFC câu hỏi (một dòng) — **đã vào chatbot 28/10** (Phase 8.2 B1).
- Gỡ nhánh GPU còn sót trong `embedding/full_corpus.py`: 8.1 không đổi code chatbot, nên dời sang 8.2.
- Corpus đổi thì phải xóa danh sách từ khóa cũ trước khi build lại (bẫy đã biết).
- Câu "mỗi đoạn vừa e5-base 512 / huydang 256" đã kiểm lại trên 8.459 đoạn ở báo cáo Chia đoạn (dài nhất
  366/512, 255/256).

## Phụ lục — hồ sơ kỹ thuật

- Report lịch sử: `reports/user_reports/phase_3_embedding_sparse_representation_user_report.md`;
  7A2 `reports/phase_7a2_gate_2_reindex_implementation_2026_10_24.md`.
- Tên kỹ thuật: vector nghĩa = dense; từ khóa = sparse/BM25; danh sách từ khóa = sparse state; model 8B
  = `qwen3-embedding-8b-4096`; model đang chạy = `e5-small-384` (`intfloat/multilingual-e5-small`).
- Bản 1: B8, 24/10/2026. Bản 2: B10, sau dọn B9 (commit `1832201`). Bản 3: C30, 25/10/2026. Bản 4: B98, 30/10/2026.
- **Qwen3-8B (30/10):** plan `report_agent/2026-10-27_phan_ton_phase_cu/qwen3_8b_plan.md` (A duyệt `d6d6c7d51584`; review B84, C88, C §8), report
  `qwen3_8b_implementation.md` (+ review C95); harness nhánh hồ sơ (tag `hoso/b92-qwen3-harness`); dữ liệu private `data/qwen3_8b_2026-10-28/`, `data/phase_8_1/g1/c78_*`.
- **8.1 phần từ khóa** (B18):
  - plan `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g4_keyword_plan.md` (bản duyệt `d7e53186b364`);
  - report `phase_8_1_g4_keyword_implementation.md` (`5e8c847df34e`);
  - review C `phase_8_1_g4_keyword_review.md`;
  - harness `backend/experiments/phase_8_1/g4_keyword.py`.
  - Tên biến thể: T1 = ghép cặp âm tiết, T2 = mã nguyên cụm, T3 = `pyvi`, E = bỏ dấu, P = tham số.
  - Cách trộn "đang chạy" = `dense_bm25_rrf`; "mở rộng" = `native_hybrid_rrf` pool 100.
- NFD / NFC câu hỏi: G1.4 (`phase_8_1_g1_implementation.md` §4).
- **Lệch đã ghi ở bản 1 và trạng thái hôm nay:**
  1. Notebook 03 còn tả 4 model và preflight — **đã sửa ở B9** (chỉ phần chữ; chạy hết không lỗi).
  2. `embedding/dense_benchmark.py` trỏ collection `hue_foods_08a_*` đã xóa — **đã gỡ ở B9**.
  3. Nhánh GPU/FP16 chỉ phục vụ Qwen-0.6B đã bỏ vẫn còn (`embedding/full_corpus.py:203-210`) — **còn**; 8.1 không đổi code chatbot nên dời sang 8.2.
