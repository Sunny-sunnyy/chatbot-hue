# Báo cáo cho bạn: Tìm kiếm — tìm đoạn liên quan (Phase 5)

**Cập nhật lần cuối: 10:49 27/10/2026 — bản 8: cho `gpt-6-luna` chọn 10 đoạn trong 30 ứng viên (K3, K3b) — bước tìm tốt lên rõ, nhưng theo luật
chưa nhận (lỗi kỹ thuật ở hai bản; bản còn lại làm 5 câu trả lời bị chấm thấp hơn); phát hiện nhãn "đoạn đúng" đếm thiếu; chatbot không đổi.** Bản 7
(22:31 26/10): thử nới nhóm ứng viên 30 → 100 (K1) — kém hơn; chỗ nghẽn là xếp hạng. Bản 6 (16:0x 26/10): đợt 3 rà code — gỡ nhánh MiniLM khỏi chatbot, gỡ bộ kiểm khói Phase 5; kết quả tìm 158 câu
giống từng byte.** Bản 5 (14:04 25/10): kết quả Phase 8.1; chatbot không đổi.
Người viết: B (bản 5, 8; bản 1–4: C) · Review: C (bản 8: A review). Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** nhận câu hỏi, trả về 10 đoạn trong kho tri thức có khả năng chứa câu trả lời,
  xếp theo thứ tự. Bước sinh câu trả lời chỉ đọc những đoạn này, nên tìm sai thì trả lời sai hoặc từ
  chối.
- **Đang chạy cách nào:** e5-small (chạy trên máy) tìm 30 đoạn gần nghĩa nhất trong Qdrant → BM25
  (khớp từ khóa) chấm lại 30 đoạn đó → trộn hai thứ hạng (RRF) → 10 đoạn. Không reranker. Trạng
  thái: đã đóng (bản món ăn 12/08/2026; bản toàn kho 14/09/2026).
- **Đo được (Phase 7B, 158 câu có trong kho):** điểm xếp hạng MRR@10 0,72, nDCG@10 0,76; 92% câu có
  đoạn chứa keyword đáp án lọt top-10. Chạy lại hai lần giống hệt từng byte.
- **Giới hạn chính:** yếu ở câu so sánh (MRR 0,53) và câu cần nhiều nguồn (0,54). Đoạn đúng hay bị xếp ngoài 10 đoạn đầu:
  ở 40 câu thử, 31 câu có đủ đoạn đúng trong 30 ứng viên, nhưng chỉ 22 câu lọt 10 đoạn đầu. Câu gõ không dấu gần như không tìm được
  (ngoài phạm vi). Chưa có cách xếp hạng lại nào được nhận.
- **Chi phí / tốc độ:** không tốn tiền API (model và Qdrant chạy trên máy).
- **Phase 8.1 đã thử (25/10, 0,0088 USD):** đo xem đoạn đúng rơi ở đâu, thử 10 cách trộn kết quả, 5 cách xếp hạng lại
  (2 model chạy trên card đồ họa, `gpt-6-luna`) và lấy rộng 100 ứng viên. **Kết luận: giữ cách đang chạy** — không cách
  nào qua được luật ghi trước. Phát hiện chính: **đoạn đúng phần lớn đã có trong nhóm ứng viên, nhưng bị xếp xuống
  thấp** (lấy 100 thì 97% câu có đủ; chỉ 55–60% lọt 10 đoạn đầu); và câu hỏi **gõ không dấu** làm tìm kiếm gần như hỏng.
- **Thử 27/10 — cho `gpt-6-luna` chọn 10 đoạn trong 30 ứng viên (chưa đưa vào chatbot):**
  - **Quan sát:** bước tìm tốt lên rõ. Số câu thử có đủ đoạn đúng trong 10 đoạn đầu tăng **22 → 31 / 40**: cứu cả 9 câu có thể cứu, không câu nào
    mất, lặp lại y hệt ở lần chạy thứ hai. Nhóm kiểm: 7 → 10 / 15, không mất câu nào.
  - **Câu trả lời cuối:** nhìn chung tốt lên (điểm đủ ý +0,22 / 5, điểm đúng +0,25 / 5; câu bị từ chối nhầm 7 → 2 / 88). Nhưng **5 câu bị chấm thấp hơn
    1–2 điểm đủ ý**, quá mức cho phép (4 câu) ⇒ theo luật ghi trước: **kém hơn, chưa nhận**.
  - **Giá:** mỗi câu chờ thêm khoảng 5 giây; tiền mỗi câu gấp khoảng 3,8 lần (≈ 0,0008 USD ≈ 20 đồng).
  - Hai bản rẻ / nhanh hơn dừng vì lỗi kỹ thuật (model trả danh sách thiếu, hoặc viết thêm chữ sau kết quả).
- **Bạn cần quyết gì:**
  - (1) Với cách "luna chọn 10 đoạn": dừng; hay đo thêm độ dao động của chính nó (≈ 0,025 USD) để biết 5 câu tụt có phải nhiễu không; hay đặt luật nhận
    khác cho trường hợp "tốt lên chung nhưng vài câu tụt". Đổi luật là quyết định của bạn.
  - (2) Mức chờ thêm ~5 giây / câu có chấp nhận được không.
  - Chuẩn hóa NFC câu hỏi đã nằm trong bản context 10 chờ đưa vào chatbot sau khi bạn đọc cặp mù (B0).

## 2. Hoạt động thế nào (bản đang chạy)

```text
câu hỏi
 → e5-small biến câu hỏi thành vector → lấy 30 đoạn gần nghĩa nhất trong Qdrant
 → BM25 (khớp từ khóa) chấm lại 30 đoạn đó
 → RRF trộn hai thứ hạng → 10 đoạn
 (không xếp hạng lại — nhánh MiniLM đã gỡ khỏi chatbot 26/10)
```

- Cách đang chạy là `dense_bm25_rrf`: BM25 chỉ chấm lại **30 đoạn vector đã tìm được**.
- Cách thứ hai `native_hybrid_rrf`: vector và BM25 **tìm độc lập** trong cả kho rồi mới trộn.
- Mọi đoạn trả về đều được kiểm cấu trúc; Qdrant hay model lỗi thì báo lỗi rõ, không âm thầm đổi cách
  khác.
- Code: `backend/retrieval/full_corpus.py` (cách tìm, số ứng viên, RRF); cấu hình
  `backend/config/settings.yaml` khối `full_corpus_runtime`.

Muốn xem điểm tìm đoạn từng loại câu (không bắt buộc): `BAO_CAO_DANH_GIA.md`.

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Tìm đoạn theo nghĩa + từ khóa cho câu hỏi thường | **Đã xử lý, đóng gói** | MRR@10 0,72 · nDCG@10 0,76 · 92% lọt top-10; chạy lại giống từng byte; `full_corpus.py:111`, `settings.yaml:42` |
| Tìm độc lập theo nghĩa và từ khóa rồi trộn (`native_hybrid_rrf`) | **Đã thử, chưa áp dụng** | 8.1 so theo cặp trên 40 câu có đoạn đúng: không khác (+3 / −1 câu); làm mất 1–2 câu |
| Lấy rộng 100 ứng viên (pool 100) | **Đã thử, chưa áp dụng** | 8.1: thêm 4 câu nhưng mất 1 câu (30 câu thử). **26/10 (K1, giữ cách trộn hiện tại, mốc 10 đoạn):** đoạn đúng có trong nhóm ứng viên 31 → 37 / 40 câu nhưng vào 10 đoạn đầu chỉ 22 → 23; mất 1 câu ⇒ **kém hơn**. Chỗ nghẽn là **xếp hạng**, không phải tìm thấy |
| Đổi hệ số trộn RRF k (2, 10, 30) / trộn kiểu DBSF | **Đã thử, chưa áp dụng** | 8.1: không cách nào qua luật; mức đổi MRR ≤ 0,01 |
| Tìm gần đúng (HNSW) so với tìm chính xác | **Đã xử lý, đóng gói** | 8.1: giống hệt 108/108 câu ⇒ giữ HNSW |
| Báo lỗi rõ khi Qdrant/model lỗi, không tự đổi cách | **Đã xử lý** | `backend/retrieval/full_corpus.py` |
| Câu so sánh | **Xử lý một phần** | MRR 0,53 |
| Câu cần nhiều nguồn | **Xử lý một phần** | MRR 0,54 |
| Dòng trong bảng giá (ví dụ giá vé + miễn giảm Đại Nội) | **Đã thử, chưa áp dụng** | 8.1 thử gộp dòng bảng khi chia đoạn: không khác — xem `BAO_CAO_CHIA_DOAN.md` |
| Từ ghép tiếng Việt trong BM25 ("Đại Nội") | **Đã thử, chưa áp dụng** | 8.1 thử cặp âm tiết / tách từ `pyvi`: làm rơi đoạn đúng của 1–4 câu — xem `BAO_CAO_EMBEDDING_TU_KHOA.md` |
| Câu hỏi gõ **không dấu** | **Chưa thực hiện** — ngoài phạm vi (bạn quyết 15:15 25/10) | 8.1 đo (dev số chính: 32 câu có đoạn đúng, 88 câu keyword): chỉ 1/32 câu còn đủ đoạn đúng trong 5 đoạn (có dấu: 13/32); MRR 0,72 → 0,16 |
| Câu hỏi dạng Unicode NFD (gõ từ một số máy) | **Chưa thực hiện** | 8.1 đo: MRR giảm 0,20; chuẩn hóa NFC phục hồi giống hệt ⇒ đề xuất 8.2 |
| Xếp hạng lại bằng MiniLM (tiếng Anh) | **Đã thử, chưa áp dụng** | **Chỉ thử trên bản món ăn**: MiniLM làm điểm giảm. Toàn kho: 0/158 câu vượt giới hạn độ dài 512; `settings.yaml:43` (`reranker: none`) |
| Reranker đa ngôn ngữ / tiếng Việt chạy trên card đồ họa (bge-reranker-v2-m3, Vietnamese_Reranker) | **Đã thử, chưa áp dụng** | 8.1: thứ tự tốt hơn chút ít nhưng đẩy đoạn đúng của 1–3 câu ra khỏi 5 đoạn đưa model; ~1 s/câu (10 đoạn), 11–14 s/câu (~150 đoạn: hợp hai nhánh, mỗi nhánh 100) |
| Xếp hạng lại bằng `gpt-6-luna` | **Đã thử, chưa áp dụng** | 8.1 (10 ứng viên): 0 câu mất, MRR +0,17, nhưng chỉ cứu được tối đa 3 câu ⇒ chưa rõ. **27/10 (chọn 10 trong 30 ứng viên):** bản xếp đủ 30 — dừng (1 / 40 lần trả danh sách thiếu); bản "chỉ trả 10 số, không suy nghĩ" — nhanh (~1,8 s) nhưng dừng (viết thêm chữ sau kết quả); bản "chỉ trả 10 số, suy nghĩ bình thường" — **bước tìm tốt hơn** (22 → 31 / 40, 0 câu mất, ổn định 2 lượt; kiểm 7 → 10 / 15), **câu trả lời theo luật kém hơn** (5 câu tụt điểm đủ ý > 4; chung +0,22) ⇒ chưa đưa vào; +5,0 s p50 / +7,0 s p95 tìm, ≈ 3,8× tiền mỗi câu |
| Thước "đoạn đúng" (nhãn vị trí đáp án) | **Xử lý một phần** | 27/10: mỗi thông tin chỉ được đánh dấu **một chỗ**; kho viết lại cùng thông tin ở chỗ khác thì thước đếm thiếu. Quét 55 câu: lặp nguyên văn 1 câu (không đổi số); lặp bằng lời khác (ước): mốc 22 → 24, bản luna 31 → 33 / 34 — kết luận bước tìm không đổi. Nhãn là dữ liệu bạn duyệt: chưa sửa |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 27/10/2026 — Cho `gpt-6-luna` chọn 10 đoạn trong 30 ứng viên (bản 8)

**Vì sao thử:** 9 câu thử có đủ đoạn đúng trong 30 ứng viên nhưng cách trộn hiện tại không đưa chúng vào 10 đoạn đầu (bản 7: chỗ nghẽn là xếp hạng).
Thử cho model sinh câu trả lời (`gpt-6-luna`) đọc 30 đoạn và chọn ra 10. Mọi luật thắng / thua ghi **trước** khi đo; so với chatbot hiện tại (mốc 10
đoạn). Chatbot **không đổi**.

| Bản | Kết quả bước tìm | Câu trả lời | Giá | Kết luận |
|---|---|---|---|---|
| Xếp đủ 30 đoạn | 1 / 40 lần model trả danh sách thiếu một đoạn ⇒ dừng. Theo dõi (39 lần hợp lệ, không dùng quyết): cứu 9 / 9, mất 0 | chưa đo | +5,6 s p50 / +8,6 s p95; ≈ 4× tiền | **kém hơn** (lỗi kỹ thuật) |
| Chỉ trả 10 số, không cho model suy nghĩ trước | 10 câu thử: tốt như bản dưới; rồi 1 lần model viết thêm chữ sau kết quả ⇒ dừng | chưa đo | **+1,8 s** p50 / +2,1 s p95; ≈ 2,7× tiền | **kém hơn** (lỗi kỹ thuật) |
| Chỉ trả 10 số, suy nghĩ như bình thường | **22 → 31 / 40**, cứu cả 9, mất 0, giống hệt ở lần chạy thứ hai; kiểm **7 → 10 / 15**, mất 0; 0 / 95 lần trả sai | 120 câu thử: điểm đủ ý **+0,22**, đúng **+0,25**, trọng tâm +0,23 (cả ba có khoảng tin cậy > 0 — chỉ báo); từ chối nhầm 7 → 2 / 88; không câu "trả lời vòng"; **nhưng 5 câu tụt điểm đủ ý** (4 câu −1, 1 câu −2) > mức cho phép 4 | tìm +5,0 s p50 / +7,0 s p95; cả câu (gọi đồng thời 4) **6,5 s p50 / 9,1 s p95**; ≈ **3,8×** tiền (≈ 0,0008 USD / câu) | bước tìm **tốt hơn (tạm)**; câu trả lời **kém hơn theo luật** ⇒ **chưa đưa vào**; nhóm kiểm câu trả lời không chạy |

- **Quan sát:** trong 9 câu cứu được ở bước tìm có 5 câu cần ghép nhiều nguồn, 3 câu so sánh và 1 câu có điều kiện, đúng hai loại yếu nhất ở §1. Ba câu trước bị từ chối giờ được chấm 5 / 5.
- **Suy ra (chưa đo):** 4 trong 5 câu tụt có context gần như giống hiện tại (7–9 / 10 đoạn trùng). Một phần có thể là dao động khi model viết lại.
  Mức cho phép lấy từ độ dao động của chatbot hiện tại (1 câu). Muốn biết chắc phải đo độ dao động của chính bản này (≈ 0,025 USD, cần bạn duyệt).
- **Phát hiện về thước đo:** câu 120 được bản luna trả lời **đúng như đáp án**, trong khi nhãn nói "context không có thông tin". Lý do: nhãn chỉ đánh dấu
  một chỗ cho mỗi thông tin, còn kho viết lại cùng thông tin ở chỗ khác. Quét lại 55 câu: ảnh hưởng nhỏ, kết luận bước tìm không đổi (§3). Bạn đã
  chọn đưa câu 120 về "chỉ theo dõi" trong lần đo câu trả lời (27/10). Lần đo trước đó dừng vì câu này; kết luận lần đó giữ nguyên.
- **Tiền thật:** 0,159 USD theo log + ≈ 0,0087 USD ước (một lượt mất số liệu do lỗi code thí nghiệm, đã sửa; cận trên ≈ 0,014) ⇒ **≈ 0,168 USD (≈ 4.200 đồng)**.
  - xếp đủ 30: 0,0251;
  - hai bản "chỉ trả 10 số": 0,0592 + ≈ 0,0087 ước;
  - đo câu trả lời: 0,0749.

### 26/10/2026 (tối) — Phân loại lỗi tìm kiếm + thử nới nhóm ứng viên (bản 7)

- **Phân loại lỗi (B42, 0 USD):** 40 câu có đoạn đúng, mốc 10 đoạn: đủ đoạn đúng 22 / 40; 18 câu thiếu — gần nửa đoạn đúng **ngoài** 30 ứng viên
  (phần lớn tìm theo từ khóa trên cả kho thấy được, nhưng hiện tìm theo từ khóa chỉ xếp lại 30 ứng viên của tìm theo nghĩa), nửa còn lại **trong** 30
  ứng viên nhưng bị xếp ngoài 10 đầu. Câu tự nhiên không lợi từ 10 đoạn (6 / 12 ở cả hai mức).
- **K1 — nới 30 → 100 ứng viên (0 USD):** kém hơn (thêm 2, mất 1 câu; chậm thêm ~9 ms). Cách "lấy thêm từ khóa trên cả kho" (K2) không chạy lại vì
  8.1 đã thử và không qua luật khi so nhiều cách. Bước tiếp: **K3** cho model xếp lại 30 ứng viên (phiên sau).
- Hồ sơ: `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_B.md`, nhánh `p82-k1`, `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k1_review.md`.

### 25/10/2026 — Phase 8.1: tìm chỗ nghẽn và thử xếp hạng lại (bản 5)

Chatbot không đổi; chỉ thí nghiệm. Mọi luật thắng/thua ghi **trước** khi đo; so theo cặp từng câu, có hiệu chỉnh khi thử
nhiều cách cùng lúc. Đo bằng **đoạn đúng** (vị trí đáp án trong file nguồn, gắn tay cho 40 câu thử + 15 câu kiểm), không
chỉ keyword.

**1. Đoạn đúng rơi ở đâu (0 USD).** Lấy 100 ứng viên thì 97,5% câu có đủ đoạn đúng; nhưng chỉ 55–60% lọt 10 đoạn đầu và
42–50% lọt 5 đoạn đưa model ⇒ **nghẽn ở xếp hạng**, không phải ở tìm ứng viên. Cả **22 câu bot từ chối nhầm** ở 7B đều thiếu
ít nhất một đoạn đúng trong 5 đoạn đưa model. Tìm gần đúng (HNSW) cho kết quả giống hệt tìm chính xác.

**2. Đổi cách trộn (0 USD).** 10 cách (tìm độc lập, hệ số RRF 2/10/30, kiểu trộn DBSF): **không cách nào thắng** theo luật
(tốt nhất +4 câu, chưa đủ chắc với 40 câu; vài cách làm mất 1–2 câu) ⇒ **giữ**.

**3. Dạng câu hỏi (0 USD).** Gõ không dấu (108 câu dev): MRR 0,73 → 0,19, gần như hỏng. Dạng Unicode NFD: tụt, nhưng chuẩn hóa NFC là hết.

**4. Xếp hạng lại (30 câu thử; luật: thứ tự đoạn đúng tốt lên rõ **và** 0 câu mất đoạn đúng khỏi 5 đoạn đưa model).**

| Cách | Kết quả | Kết luận |
|---|---|---|
| bge-reranker-v2-m3 / Vietnamese_Reranker, chấm đoạn hoặc cả mục, 10 ứng viên | thứ tự tốt hơn chút ít, nhưng mất 1–3 câu | **bỏ** |
| `gpt-6-luna` tự xếp 10 ứng viên | 0 câu mất, cứu đủ 3/3 câu có thể cứu, MRR +0,17 | **chưa rõ** (bộ thử chỉ cho cứu tối đa 3 câu) — tín hiệu cho 8.2 |
| bge-reranker trên 100 ứng viên | thêm 5 câu nhưng mất 1 câu; không hơn "lấy 100 ứng viên, không xếp lại" | **bỏ** — phần lợi đến từ việc lấy rộng |
| Chấm "cả mục chứa đoạn" trên 100 ứng viên | 165 s cho một câu trên GTX 1650 | **bỏ** (quá chậm) |

**Tiền:** 0,0088 USD (≈ 220 đồng, chỉ phần `gpt-6-luna`); model chạy trên card đồ họa và Qdrant: 0. **Giữ** cách tìm đang
chạy; ý đáng thử ở 8.2 ghi ở §6.

### 24/10/2026 — Dọn code món ăn sau Phase 7 (bản 4)
Gỡ code/test/notebook bản món ăn và xóa 2 collection món ăn. Kiểm lại sau dọn: kết quả tìm kiếm 158
câu **giống hệt từng byte** so với mốc Phase 7B · **PASS** · tiền: 0. Hành vi tìm kiếm không đổi.

### 24/10/2026 — Đính chính về reranker MiniLM (bản 3)
Khi rà quyết định Phase 8.1: bằng chứng "MiniLM làm điểm giảm" chỉ có trên bản món ăn (bộ câu và
chunk khác); trên toàn kho mới đo tốc độ. Bản 2 không nói rõ điều này. Không đổi số đo nào.

### 24/10/2026 — Đo chất lượng tìm đoạn trên 158 câu có trong kho (Phase 7B)
Cách đo: đoạn chứa keyword đáp án có lọt top-10 không, trên chỉ mục hiện tại · kết quả: đo mốc (chưa
đặt ngưỡng) — MRR@10 0,72, nDCG@10 0,76, 92% lọt top-10; câu so sánh 0,53, nhiều nguồn 0,54 · so hai
cách tìm: `native_hybrid_rrf` 0,726 vs đang chạy 0,721 → **giữ** cách đang chạy vì chênh rất nhỏ ·
chạy lại hai lần giống hệt từng byte · lỗi đã biết: câu "giá vé + miễn giảm Đại Nội" — đoạn bảng giá
hạng ~191 theo nghĩa, ngoài top-30 theo từ khóa · tiền: 0 (tìm đoạn chạy trên máy).

### 14/09/2026 — Đóng bản toàn kho (5 mảng dữ liệu)
Cách đo: kiểm kỹ thuật trên Qdrant thật · kết quả: **PASS** kỹ thuật — 8/8 tổ hợp model × cách tìm chạy
đúng; 23 test đạt · lúc đóng **chưa đo chất lượng** (số chất lượng ở trên là của 24/10).

### 12/08/2026 — Đóng bản món ăn
Ba chế độ `dense_only` / `hybrid_no_rerank` / `hybrid_rerank`, chỉ kho món ăn · reranker MiniLM làm
điểm giảm ở benchmark → **bỏ** (tắt) · bản này nay không còn được chatbot dùng.

## 5. Hôm nay còn đúng không

Kiểm với code (commit `1832201`, sau dọn) và `session_prompt/Project_Status.md` §4 ngày 24/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Hai cách tìm `dense_bm25_rrf`, `native_hybrid_rrf` | **còn dùng** (chatbot chạy `dense_bm25_rrf`) | `backend/retrieval/full_corpus.py:111`; `backend/config/settings.yaml:42` |
| 30 ứng viên, RRF k=60, trả top-10 | **còn dùng** | `backend/retrieval/full_corpus.py:465,608,627` |
| Reranker MiniLM (tiếng Anh) | **đã gỡ khỏi chatbot** 26/10 (trước đó tắt) | `settings.yaml:43` (`reranker: none` — giá trị duy nhất); lớp `backend/reranking/cross_encoder.py` giữ cho bộ thử 8.1 (G1, G4) |
| 4 kho vector toàn kho của Phase 4–5 | **đã thay** bởi một kho `hue_full_corpus_7a2_e5_small_384` (Phase 7A2) | Qdrant chỉ còn collection này (kiểm 24/10 sau dọn) |
| Model e5-small, e5-base, HuyDang, Qwen3-0.6B trong ma trận thử | **đã thay** bởi e5-small + Qwen3-8B (Phase 7A2); 8B chưa có chỉ mục | `backend/embedding/full_corpus.py:41–66` |
| Ba chế độ bản món ăn (`dense_only`/`hybrid_*`) | **đã bỏ**: code đã gỡ khi dọn sau Phase 7 | commit `1832201`; [R2] |
| Chọn cách tìm/model thắng | **đã đo ở 8.1: giữ cách đang chạy** (không cách trộn / xếp hạng lại nào qua luật) | `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_implementation.md`, `phase_8_1_g4_implementation.md` |
| "BM25 chỉ chấm lại 30 đoạn vector" là cách tốt | **còn đúng ở 8.1** — nhưng chỉ vì các cách khác chưa chắc hơn; đoạn đúng hay bị xếp thấp | như trên |
| Cho `gpt-6-luna` chọn 10 trong 30 ứng viên | **chưa đưa vào** (27/10): bước tìm tốt hơn, câu trả lời theo luật kém hơn; chờ bạn quyết | Phụ lục bản 8 |

## 6. Việc còn lại / cần quyết

Đề xuất cho Phase 8.2 (mỗi việc cần đo riêng; đổi chatbot cần bạn duyệt):
- **Câu gõ không dấu:** **Bạn quyết 15:15 25/10: ngoài phạm vi** — thiết kế giả định người dùng gõ có dấu; không làm ở 8.2. Ghi chú cũ: lỗ hổng lớn nhất ở khâu này. Thử dùng bản từ khóa đã bỏ dấu **chỉ khi câu hỏi không có dấu**
  (8.1 thấy bản bỏ dấu tìm lại được nhiều, nhưng làm hại câu có dấu nếu dùng cho mọi câu) — xem `BAO_CAO_EMBEDDING_TU_KHOA.md`.
- **Chuẩn hóa NFC câu hỏi:** sửa một dòng, phục hồi hoàn toàn câu dạng NFD.
- **Lấy rộng 100 ứng viên:** có tín hiệu (+4 / −1 câu); thử cùng context 10 đoạn (`BAO_CAO_SINH_CAU_TRA_LOI_API.md`).
- **`gpt-6-luna` chọn 10 trong 30 ứng viên (27/10, chưa đưa vào):** bước tìm tốt rõ (22 → 31 / 40), câu trả lời chung tốt lên nhưng 5 câu tụt ⇒ theo luật
  chưa nhận. Bạn quyết: dừng / đo độ dao động của chính bản này (≈ 0,025 USD) / đặt luật nhận khác. Nếu sau này nhận, cần tìm cách nhanh hơn
  (bản không suy nghĩ chỉ +1,8 s nhưng hay viết thừa chữ).
- Reranker chạy trên card đồ họa: đã thử ở 8.1, không dùng.

## Phụ lục — hồ sơ kỹ thuật

- Mã lỗi: lỗi bảng giá = **F2**.
- [R1] giả thuyết Phase 8: `reports/phase_8_candidate_hypotheses_2026_10_24.md` (C1, C7).
- [R2] danh sách dọn sau Phase 7: `reports/phase_7_cleanup_inventory_2026_10_24.md` (C2).
- Số đo 7B: `bao_cao_he_thong/BAO_CAO_DANH_GIA.md`; report `reports/phase_7b_*`.
- Bản 1 (C8, 24/10/2026, commit `4426ed0`). Bản 3 (C12): đính chính theo `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_decision_inventory.md` dòng 5.5 và §6 mục 13.
- **Lệch phát hiện (24/10) — đã xử lý:** `settings.yaml` từng giữ khối `profiles`/`active_profile`/
  `retrieval`/`reranking` của bản món ăn mà code bản toàn kho không đọc. Việc dọn B9 (commit `1832201`,
  C review `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_review.md`) đã gỡ các khối này và
  bỏ kiểm `active_profile` trong `load_settings`.
- Bản 4 (C13): cập nhật sau B9; kiểm so byte tìm kiếm ở review B9 §4.
- Bản 5 (B20, 25/10/2026): Phase 8.1 G1 (chẩn đoán, `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_implementation.md`
  §4, §7; review `phase_8_1_g1_review.md`) và G4 (rerank M1 `BAAI/bge-reranker-v2-m3`, M2 `AITeamVN/Vietnamese_Reranker`,
  luna listwise, G4-B pool 100; `phase_8_1_g4_implementation.md` §4; review `phase_8_1_g4_review.md`). Câu không dấu / NFD:
  G1.4; BM25 (G4K): `phase_8_1_g4_keyword_implementation.md`. Luật quyết: plan `phase_8_1_g2_g4_plan.md` (sha
  `a4adfc8eedd9`). Mốc tìm kiếm runtime giống byte `cefb2d1a…` suốt 8.1.
- Bản 8 (B66, 27/10/2026):
  - K3: plan `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3_plan.md` (`0a6370204c7d`); report trên nhánh `p82-k3`
    (`phase_8_2_k3_implementation.md`); review `phase_8_2_k3_review.md`.
  - K3b-n / K3b-m: plan `phase_8_2_k3b_plan.md` bản 2 (`57dad7150322`); report `phase_8_2_k3b_implementation.md` trên `p82-k3b`.
  - Khâu trả lời K3b-m: plan `phase_8_2_k3b_m_answer_plan.md` bản 3 (`2a3b22b38ab6`; bản 2 `92a8a7eb4177` dừng ở sàn câu 120); report
    `phase_8_2_k3b_m_answer_implementation.md` trên `p82-k3b` (`a6f609c`).
  - Quét nhãn đoạn đúng B61: `data/phase_8_2/k3b/gold_scan/` (private).
  - Mã: T3 = mức tụt "số câu Completeness tụt ≤ A/A + 3"; A/A = độ dao động đo bằng hai lượt cùng cấu hình.
