# Báo cáo cho bạn: Tìm kiếm — tìm đoạn liên quan (Phase 5)

**Cập nhật lần cuối: 17:14 31/10/2026 — bản 11: rà lại cho đúng hiện trạng, xoá phần không còn đúng (User 31/10).** Các bản trước: xem `git log` file này.
Người viết: A (bản 9–11; bản 11 qua sub-agent), B (bản 5, 8), C (bản 1–4) · Review: C (bản 8: A review); bản 11 chưa review. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** nhận câu hỏi, trả về 10 đoạn trong kho tri thức có khả năng chứa câu trả lời, xếp theo thứ tự. Bước sinh câu trả lời chỉ
  đọc 10 đoạn này (từ 28/10; trước đó 5), nên tìm sai thì trả lời sai hoặc từ chối.
- **Đang chạy cách nào:** câu hỏi đổi về dạng Unicode NFC (một cách viết chuẩn của chữ có dấu) → e5-small (model biến câu thành vector, chạy trên
  máy) lấy 30 đoạn gần nghĩa nhất trong Qdrant (cơ sở dữ liệu vector) → BM25 (chấm theo khớp từ khóa) chấm lại 30 đoạn đó → RRF (cách trộn hai
  bảng xếp hạng) → 10 đoạn đầu. Không có bước xếp hạng lại. Chỉ mục dựng lại 30/10 trên kho đã sửa hai đợt (204 file, 8.424 đoạn) — **cách tìm
  không đổi**.
- **Đo được trên kho hiện tại** (30/10, nhãn "đoạn đúng" bản 5 — vị trí đáp án trong file nguồn, gắn tay cho 40 câu thử + 15 câu kiểm):
  - **24 / 40** câu thử có đủ đoạn đúng trong 10 đoạn đưa model; **33 / 40** có đủ trong 30 ứng viên ⇒ 9 câu có đoạn đúng trong ứng viên nhưng bị xếp
    ngoài 10 đầu. Nhóm kiểm: 9 / 15.
  - Điểm xếp hạng MRR (đoạn chứa keyword đáp án đứng càng cao càng tốt, tối đa 1): **0,731** trên 108 câu thử, **0,700** trên 50 câu kiểm.
  - Chạy lại cho kết quả giống hệt (tất định).
- **Giới hạn chính:**
  - Chỗ nghẽn là **xếp hạng**: đoạn đúng phần lớn đã có trong ứng viên nhưng bị xếp thấp. Chưa cách xếp hạng lại nào được nhận (§3, §4).
  - Yếu ở câu so sánh và câu cần nhiều nguồn (MRR 0,53 / 0,54 — đo 24/10 trên kho cũ; **chưa đo lại** theo loại câu).
  - Câu gõ không dấu gần như không tìm được — ngoài phạm vi (bạn quyết 25/10).
- **Chi phí / tốc độ:** không tốn tiền API (model và Qdrant chạy trên máy); tạo vector câu hỏi 21–28 ms (p50 / p95, đo 30/10).
- **Đã thử, không đưa vào chatbot** (chi tiết §3, §4): đổi cách trộn, lấy rộng 100 ứng viên, reranker chạy trên card đồ họa, cho `gpt-6-luna` xếp lại /
  chọn 10 trong 30 ứng viên, đổi model vector sang Qwen3-Embedding-8B (30/10: kém hơn ⇒ giữ e5-small).
- **Bạn cần quyết gì:** hiện không có việc nào cần bạn quyết ở khâu này.

## 2. Hoạt động thế nào (bản đang chạy)

```text
câu hỏi
 → chuẩn hóa Unicode NFC (câu đã NFC giữ nguyên từng byte)
 → e5-small biến câu hỏi thành vector → lấy 30 đoạn gần nghĩa nhất trong Qdrant
 → BM25 (khớp từ khóa) chấm lại 30 đoạn đó
 → RRF trộn hai thứ hạng (k = 60) → 10 đoạn đầu
 (không xếp hạng lại)
```

- Cách đang chạy là `dense_bm25_rrf`: BM25 chỉ chấm lại **30 đoạn vector đã tìm được**.
- Cách thứ hai có trong code, không dùng: `native_hybrid_rrf` — vector và BM25 **tìm độc lập** trong cả kho rồi mới trộn.
- Mọi đoạn trả về đều được kiểm cấu trúc; Qdrant hay model lỗi thì báo lỗi rõ, không âm thầm đổi cách khác.
- Code: `backend/retrieval/full_corpus.py` — chuẩn hóa câu hỏi `:97–102` (gọi ở `:420`), số ứng viên 30 và k = 60 `:401–402`, hai cách tìm `:482`, `:521`,
  trộn `:585`, lấy 10 đầu `:602`. Cấu hình `backend/config/settings.yaml:41–44` (khối `full_corpus_runtime`).

Muốn xem điểm tìm đoạn từng loại câu (không bắt buộc): `BAO_CAO_DANH_GIA.md`.

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Tìm đoạn theo nghĩa + từ khóa cho câu hỏi thường | **Đã xử lý, đóng gói** | Kho hiện tại (30/10): 24 / 40 câu đủ đoạn đúng trong 10 đoạn; MRR 0,731 (108 câu) / 0,700 (50 câu). Kho cũ (24/10, 158 câu): MRR@10 0,72 · nDCG@10 0,76 · 92% lọt top-10. `full_corpus.py:482`, `settings.yaml:43` |
| Tìm độc lập theo nghĩa và từ khóa rồi trộn (`native_hybrid_rrf`) | **Đã thử, chưa áp dụng** | 24/10: MRR 0,726 so với 0,721 (chênh rất nhỏ); 8.1 trên 40 câu có đoạn đúng: không khác (+3 / −1 câu). `full_corpus.py:521` |
| Lấy rộng 100 ứng viên | **Đã thử, chưa áp dụng** | 26/10 (kho cũ, nhãn bản 1): đủ đoạn đúng trong ứng viên 31 → 37 / 40 nhưng trong 10 đoạn đầu chỉ 22 → 23, mất 1 câu ⇒ **kém hơn**. Chỗ nghẽn là xếp hạng |
| Đổi hệ số trộn RRF k (2, 10, 30) / trộn kiểu DBSF | **Đã thử, chưa áp dụng** | 8.1: không cách nào qua luật; MRR đổi ≤ 0,01 |
| Tìm gần đúng (HNSW) so với tìm chính xác | **Đã xử lý, đóng gói** | 8.1: giống hệt 108 / 108 câu ⇒ giữ HNSW |
| Báo lỗi rõ khi Qdrant / model lỗi, không tự đổi cách | **Đã xử lý** | `backend/retrieval/full_corpus.py` |
| Câu so sánh | **Xử lý một phần** | MRR 0,53 (24/10, kho cũ; chưa đo lại) |
| Câu cần nhiều nguồn | **Xử lý một phần** | MRR 0,54 (24/10, kho cũ; chưa đo lại) |
| Dòng trong bảng giá (giá vé, miễn giảm) | **Đã thử, chưa áp dụng** | 8.1 thử gộp dòng bảng khi chia đoạn: không khác — xem `BAO_CAO_CHIA_DOAN.md` |
| Từ ghép tiếng Việt trong BM25 | **Đã thử, chưa áp dụng** | 8.1 thử cặp âm tiết / tách từ `pyvi`: làm rơi đoạn đúng của 1–4 câu — xem `BAO_CAO_EMBEDDING_TU_KHOA.md` |
| Câu hỏi gõ **không dấu** | **Chưa thực hiện** — ngoài phạm vi (bạn quyết 15:15 25/10) | 8.1 (kho cũ, lúc đưa 5 đoạn; 32 câu có đoạn đúng, 88 câu keyword): chỉ 1 / 32 câu còn đủ đoạn đúng trong 5 đoạn (có dấu: 13 / 32); MRR 0,72 → 0,16 (88 câu keyword) |
| Câu hỏi dạng Unicode NFD (gõ từ một số máy) | **Đã xử lý, đóng gói** (28/10) | 8.1 đo: NFD làm MRR giảm 0,20; chuẩn hóa NFC phục hồi giống hệt. Câu NFD đã lưu cho đúng 10 đoạn như câu NFC. `full_corpus.py:97–102`, `:420` |
| Xếp hạng lại bằng MiniLM (tiếng Anh) | **Đã thử, chưa áp dụng** | Chỉ thử trên bản món ăn: điểm giảm. `settings.yaml:44` (`reranker: none`); lớp `backend/reranking/cross_encoder.py` chỉ còn cho bộ thử 8.1 |
| Reranker đa ngôn ngữ / tiếng Việt chạy trên card đồ họa (bge-reranker-v2-m3, Vietnamese_Reranker) | **Đã thử, chưa áp dụng** | 8.1 (lúc đưa 5 đoạn): thứ tự tốt hơn chút ít nhưng đẩy đoạn đúng của 1–3 câu ra khỏi 5 đoạn đưa model; ~1 s / câu (10 đoạn), 11–14 s / câu (~150 đoạn) |
| Xếp hạng lại / chọn đoạn bằng `gpt-6-luna` | **Đã thử, chưa áp dụng** | 8.1 (10 ứng viên): 0 câu mất, MRR +0,17, nhưng chỉ cứu được tối đa 3 câu ⇒ chưa rõ. 27/10 (chọn 10 trong 30): bản tốt nhất bước tìm 22 → 31 / 40, nhưng 5 câu trả lời tụt điểm (> 4 cho phép), cả câu p50 6,5 / p95 9,1 s (vượt sàn 3 / 5 s bạn chốt 28/10), ≈ 3,8× tiền ⇒ gác làm hồ sơ (bạn chốt đợt 27/10) |
| Đổi model vector sang Qwen3-Embedding-8B | **Đã thử, chưa áp dụng** | 30/10: dev 24 → 23 / 40 câu đủ đoạn đúng; 3 câu dev + 3 câu kiểm mất đoạn đúng (vỡ sàn "0 câu mất"); vector câu hỏi p50 2,2 s qua mạng (e5: 21 ms) ⇒ giữ e5-small; chỉ mục thử đã xoá — `BAO_CAO_EMBEDDING_TU_KHOA.md` |
| Thước "đoạn đúng" (nhãn vị trí đáp án) | **Xử lý một phần** | Mỗi thông tin chỉ đánh dấu một chỗ; kho viết lại cùng thông tin ở chỗ khác thì thước đếm thiếu. Quét 55 câu (27/10): ảnh hưởng nhỏ, kết luận bước tìm không đổi. Bản 2 (bạn duyệt 27/10) thêm chỗ cho 2 câu; đang dùng bản 5 (30/10, theo kho sau đợt 2) |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 30/10/2026 — Kho sửa đợt 2, chỉ mục dựng lại; thử Qwen3-Embedding-8B
- **Kho sửa đợt 2:** cách tìm không đổi; kết quả tìm 158 câu có 25 câu đổi danh sách 10 đoạn (11 chỉ đổi thứ tự; 24 có đoạn của file đã sửa). Đo lại mốc
  trên kho mới: số ở §1. Đo "không làm hỏng" câu trả lời: `BAO_CAO_KHO_DU_LIEU.md`.
- **Qwen3-Embedding-8B thay e5-small:** kém hơn (số ở §3) · dựng chỉ mục thử ~31 phút, 0,0089 USD · chỉ mục thử đã xoá; code giữ làm hồ sơ, không vào
  chatbot. Hồ sơ: `report_agent/2026-10-27_phan_ton_phase_cu/qwen3_8b_implementation.md`.

### 28/10/2026 — Chuẩn hóa NFC vào chatbot; kho sửa đợt 1
- **NFC:** đi cùng việc đưa 10 đoạn vào ngữ cảnh (bạn chọn không chờ đọc cặp mù). Kết quả tìm 158 câu **giống từng byte** mốc cũ; câu NFD đã lưu cho đúng 10
  đoạn như câu NFC · 0 USD.
- **Kho sửa đợt 1, chỉ mục dựng lại:** 40 / 158 câu đổi danh sách 10 đoạn, giải thích được bằng phần sửa và từ điển từ khóa mới (C kiểm).

### 27/10/2026 — Cho `gpt-6-luna` chọn 10 đoạn trong 30 ứng viên (3 bản)
- **Xếp đủ 30 đoạn:** 1 / 40 lần model trả danh sách thiếu ⇒ dừng, **kém hơn** (lỗi kỹ thuật); +5,6 s p50.
- **Chỉ trả 10 số, không cho suy nghĩ:** nhanh (+1,8 s p50) nhưng model viết thừa chữ sau kết quả ⇒ dừng, **kém hơn** (lỗi kỹ thuật).
- **Chỉ trả 10 số, suy nghĩ bình thường:** bước tìm 22 → 31 / 40 (nhãn bản 2: 24 → 33), nhóm kiểm 7 → 10 / 15, 0 câu mất; câu trả lời chung tốt lên (đủ ý +0,22 / 5,
  từ chối nhầm 7 → 2 / 88) nhưng 5 câu tụt điểm đủ ý > 4 cho phép ⇒ **kém hơn theo luật ghi trước**; cả câu p50 6,5 / p95 9,1 s, ≈ 3,8× tiền ⇒ **gác** (bạn chốt
  đợt 27/10, chatbot không đổi). Tiền cả ba bản ≈ 0,168 USD. Hồ sơ: `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md` §3.

### 26/10/2026 — Phân loại lỗi tìm kiếm + thử lấy rộng 100 ứng viên
- **Phân loại lỗi (0 USD):** 40 câu có đoạn đúng, mốc 10 đoạn: thiếu ở 18 câu — gần nửa đoạn đúng **ngoài** 30 ứng viên, nửa còn lại trong ứng viên nhưng bị xếp
  ngoài 10 đầu.
- **Lấy rộng 100 ứng viên (0 USD):** **kém hơn** (số ở §3). Hồ sơ: `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_B.md`,
  `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k1_review.md`.

### 25/10/2026 — Phase 8.1: tìm chỗ nghẽn, thử cách trộn và xếp hạng lại (kho cũ, lúc đưa 5 đoạn)
- **Chỗ nghẽn (0 USD):** lấy 100 ứng viên thì 97,5% câu có đủ đoạn đúng, nhưng chỉ 55–60% lọt 10 đoạn đầu ⇒ **nghẽn ở xếp hạng**. Tìm gần đúng (HNSW) giống
  hệt tìm chính xác.
- **10 cách trộn (0 USD):** không cách nào thắng theo luật ghi trước ⇒ **giữ**.
- **Dạng câu hỏi (0 USD):** gõ không dấu (108 câu): MRR 0,73 → 0,19; dạng NFD tụt, chuẩn hóa NFC là hết (đưa vào chatbot 28/10).
- **Xếp hạng lại (30 câu thử):** hai reranker chạy card đồ họa — **bỏ** (mất 1–3 câu); `gpt-6-luna` xếp 10 ứng viên — **chưa rõ** (MRR +0,17, chỉ cứu tối đa 3 câu)
  ⇒ thử lại 27/10; reranker trên 100 ứng viên — **bỏ** (lợi đến từ lấy rộng); chấm cả mục — **bỏ** (165 s / câu). Tiền 0,0088 USD.
  Hồ sơ: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_implementation.md`, `phase_8_1_g4_implementation.md`.

### 24/10/2026 — Đo chất lượng tìm đoạn Phase 7B; dọn code món ăn
- **Đo 158 câu có trong kho (kho cũ):** MRR@10 0,72, nDCG@10 0,76, 92% câu có đoạn chứa keyword lọt top-10; câu so sánh 0,53, nhiều nguồn 0,54; chạy lại hai lần
  giống từng byte · lỗi đã biết: đoạn bảng giá vé xếp rất thấp theo nghĩa (hạng ~191), ngoài top-30 theo từ khóa · 0 USD.
- **Dọn code / chỉ mục món ăn:** kết quả tìm 158 câu giống từng byte · **PASS**. Đính chính: "MiniLM làm điểm giảm" chỉ đo trên bản món ăn.

### 14/09/2026 — Đóng bản toàn kho; 12/08/2026 — đóng bản món ăn
- Toàn kho: **PASS** kỹ thuật (8 / 8 tổ hợp model × cách tìm chạy đúng; 23 test đạt); lúc đóng chưa đo chất lượng.
- Món ăn: reranker MiniLM làm điểm giảm ⇒ **bỏ** (tắt); bản này nay không còn trong chatbot.

## 5. Hôm nay còn đúng không

Kiểm với code trên `main` (số dòng kiểm lúc 17:14 31/10/2026), build record và `session_prompt/Project_Status.md` §4 (17:00 31/10/2026).

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Cách tìm `dense_bm25_rrf` (cách `native_hybrid_rrf` có trong code, không dùng) | **còn dùng** | `backend/retrieval/full_corpus.py:482`, `:521`; `backend/config/settings.yaml:43` |
| 30 ứng viên, RRF k = 60, trả 10 đoạn | **còn dùng** | `backend/retrieval/full_corpus.py:401–402`, `:585`, `:602` |
| Chuẩn hóa NFC câu hỏi trước khi tìm | **còn dùng** (từ 28/10) | `backend/retrieval/full_corpus.py:97–102`, `:420` |
| Không xếp hạng lại | **còn dùng** (MiniLM đã gỡ khỏi chatbot 26/10) | `backend/config/settings.yaml:44` |
| Model vector e5-small | **còn dùng**; Qwen3-8B đã thử 30/10 — kém hơn, chỉ mục thử đã xoá | `backend/embedding/full_corpus.py:41–66` |
| Chỉ mục tìm trên 204 file / 8.424 đoạn | **còn dùng** (dựng lại 30/10) | `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` (private) |
| "BM25 chỉ chấm lại 30 đoạn vector" là cách tốt nhất đã thử | **còn đúng** — nhưng chỉ vì các cách khác không chắc hơn; đoạn đúng hay bị xếp thấp | §3, §4 |
| Cho `gpt-6-luna` chọn 10 trong 30 ứng viên | **gác làm hồ sơ** (bạn chốt 27/10) | §4 27/10 |

## 6. Việc còn lại / cần quyết

- **Không có việc cần bạn quyết** ở khâu này.
- **Chỗ yếu còn mở:** 9 / 40 câu thử có đoạn đúng trong ứng viên nhưng bị xếp ngoài 10 đầu; câu so sánh / nhiều nguồn. Các hướng đã thử đều không qua luật.
  Hướng để ngỏ (hồ sơ, chưa lên lịch): bản "luna chọn đoạn" nhanh hơn, chỉ khi có luật nhận mới cho loại thay đổi này và vừa sàn tốc độ; sửa nhãn đoạn đúng
  để đếm cả chỗ kho viết lại cùng thông tin.
- **Chưa đo lại** điểm theo loại câu (so sánh, nhiều nguồn) trên kho hiện tại — số 0,53 / 0,54 là của kho cũ.
- Câu gõ không dấu: ngoài phạm vi (bạn quyết 25/10).

## Phụ lục — hồ sơ kỹ thuật

- **Mã:** T1 = mốc kết quả tìm 158 câu (dấu vân tay `4d5bbe9e0edc` từ 30/10; `23c58c47635d` 28/10; `cefb2d1a…` suốt 8.1); K1 = lấy rộng 100 ứng viên; K2 = tìm
  từ khóa độc lập (NOT RUN, đã trượt ở 8.1); K3 = luna xếp đủ 30; K3b-n / K3b-m = luna chỉ trả 10 số, không suy nghĩ / suy nghĩ mặc định; B42 = phân loại lỗi;
  F2 = lỗi bảng giá; T3 = mức tụt "số câu Completeness tụt ≤ A/A + 3" (A/A = độ dao động đo bằng hai lượt cùng cấu hình); PA3 = phương án bạn chọn 28/10
  (đưa 10 đoạn + NFC vào chatbot, không chờ đọc cặp mù).
- **Nhãn đoạn đúng:** đang dùng `gold_v5.jsonl` `33d16fd6b8f4` (30/10); số "22 → 31" của 27/10 tính bằng nhãn bản 1, kho cũ.
- **Mốc kho hiện tại** (dev 40 / test 15 / MRR 108 + 50 câu): `report_agent/2026-10-27_phan_ton_phase_cu/qwen3_8b_implementation.md` §1–2 (phần e5); review
  `qwen3_8b_review.md`; code thí nghiệm tag `hoso/b92-qwen3-harness`.
- **NFC + 10 đoạn:** merge `510e1a8` (28/10); hồ sơ `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
- **Bản 8 (B66, 27/10):** K3 plan `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3_plan.md` (`0a6370204c7d`), review `phase_8_2_k3_review.md`, code tag
  `hoso/p82-k3`; K3b plan `phase_8_2_k3b_plan.md` bản 2 (`57dad7150322`), report `phase_8_2_k3b_implementation.md` trên tag `hoso/p82-k3b`; khâu trả lời K3b-m
  plan `phase_8_2_k3b_m_answer_plan.md` bản 3 (`2a3b22b38ab6`), report `phase_8_2_k3b_m_answer_implementation.md` trên `hoso/p82-k3b`. Quét nhãn B61:
  `data/phase_8_2/k3b/gold_scan/` (private).
- **K1 (26/10):** code tag `hoso/p82-k1`; review `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k1_review.md`.
- **Bản 5 (B20, 25/10):** Phase 8.1 G1 (`report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_implementation.md` §4, §7; review `phase_8_1_g1_review.md`), G4
  (M1 `BAAI/bge-reranker-v2-m3`, M2 `AITeamVN/Vietnamese_Reranker`, luna listwise, G4-B pool 100; `phase_8_1_g4_implementation.md` §4; review
  `phase_8_1_g4_review.md`); câu không dấu / NFD: G1.4; BM25 (G4K): `phase_8_1_g4_keyword_implementation.md`; luật quyết: plan `phase_8_1_g2_g4_plan.md`
  (`a4adfc8eedd9`).
- **Số 7B:** `bao_cao_he_thong/BAO_CAO_DANH_GIA.md`; report `reports/phase_7b_*`.
- [R1] giả thuyết Phase 8: `reports/phase_8_candidate_hypotheses_2026_10_24.md` (C1, C7). [R2] danh sách dọn sau Phase 7:
  `reports/phase_7_cleanup_inventory_2026_10_24.md` (C2); dọn B9 commit `1832201` (gỡ khối `profiles` / `active_profile` / `retrieval` / `reranking` của bản món
  ăn khỏi `settings.yaml`; review `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_review.md`).
- Bản 1 (C8, 24/10/2026, commit `4426ed0`). Bản 3 (C12): đính chính MiniLM theo `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_decision_inventory.md`
  dòng 5.5 và §6 mục 13.
