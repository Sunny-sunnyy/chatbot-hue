# Báo cáo cho bạn: Tìm kiếm — tìm đoạn liên quan (Phase 5)

**Cập nhật lần cuối: 16:0x 26/10/2026 — bản 6: đợt 3 rà code — gỡ nhánh MiniLM khỏi chatbot, gỡ bộ kiểm khói Phase 5; kết quả tìm 158 câu
giống từng byte.** Bản 5 (14:04 25/10): kết quả Phase 8.1; chatbot không đổi.
Người viết: B (bản 5; bản 1–4: C) · Review: C. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** nhận câu hỏi, trả về 10 đoạn trong kho tri thức có khả năng chứa câu trả lời,
  xếp theo thứ tự. Bước sinh câu trả lời chỉ đọc những đoạn này, nên tìm sai thì trả lời sai hoặc từ
  chối.
- **Đang chạy cách nào:** e5-small (chạy trên máy) tìm 30 đoạn gần nghĩa nhất trong Qdrant → BM25
  (khớp từ khóa) chấm lại 30 đoạn đó → trộn hai thứ hạng (RRF) → 10 đoạn. Không reranker. Trạng
  thái: đã đóng (bản món ăn 12/08/2026; bản toàn kho 14/09/2026).
- **Đo được (Phase 7B, 158 câu có trong kho):** điểm xếp hạng MRR@10 0,72, nDCG@10 0,76; 92% câu có
  đoạn chứa keyword đáp án lọt top-10. Chạy lại hai lần giống hệt từng byte.
- **Giới hạn chính:** yếu ở câu so sánh (MRR 0,53) và câu cần nhiều nguồn (0,54); đoạn đúng hay bị xếp ngoài 5 đoạn
  đưa model; câu gõ không dấu gần như không tìm được; reranker thử ở 8.1 chưa dùng được.
- **Chi phí / tốc độ:** không tốn tiền API (model và Qdrant chạy trên máy).
- **Phase 8.1 đã thử (25/10, 0,0088 USD):** đo xem đoạn đúng rơi ở đâu, thử 10 cách trộn kết quả, 5 cách xếp hạng lại
  (2 model chạy trên card đồ họa, `gpt-6-luna`) và lấy rộng 100 ứng viên. **Kết luận: giữ cách đang chạy** — không cách
  nào qua được luật ghi trước. Phát hiện chính: **đoạn đúng phần lớn đã có trong nhóm ứng viên, nhưng bị xếp xuống
  thấp** (lấy 100 thì 97% câu có đủ; chỉ 55–60% lọt 10 đoạn đầu); và câu hỏi **gõ không dấu** làm tìm kiếm gần như hỏng.
- **Bạn cần quyết gì (ở 8.2):** có thử tiếp "lấy rộng 100 ứng viên" và "cho `gpt-6-luna` xếp hạng lại" (mới có tín hiệu)
  không; có sửa câu không dấu / chuẩn hóa NFC không (§6).

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
| Lấy rộng 100 ứng viên (pool 100) | **Đã thử, chưa áp dụng** | 8.1: thêm 4 câu nhưng mất 1 câu đủ đoạn đúng (30 câu thử) — chưa đủ chắc; có tín hiệu |
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
| Xếp hạng lại bằng `gpt-6-luna` | **Đã thử, chưa áp dụng** | 8.1: không mất câu nào, thứ tự tốt lên rõ (MRR +0,17), nhưng bộ thử chỉ cho cứu tối đa 3 câu ⇒ chưa rõ; +3,5 s và ≈ 0,0003 USD mỗi câu |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

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

## 6. Việc còn lại / cần quyết

Đề xuất cho Phase 8.2 (mỗi việc cần đo riêng; đổi chatbot cần bạn duyệt):
- **Câu gõ không dấu:** **Bạn quyết 15:15 25/10: ngoài phạm vi** — thiết kế giả định người dùng gõ có dấu; không làm ở 8.2. Ghi chú cũ: lỗ hổng lớn nhất ở khâu này. Thử dùng bản từ khóa đã bỏ dấu **chỉ khi câu hỏi không có dấu**
  (8.1 thấy bản bỏ dấu tìm lại được nhiều, nhưng làm hại câu có dấu nếu dùng cho mọi câu) — xem `BAO_CAO_EMBEDDING_TU_KHOA.md`.
- **Chuẩn hóa NFC câu hỏi:** sửa một dòng, phục hồi hoàn toàn câu dạng NFD.
- **Lấy rộng 100 ứng viên:** có tín hiệu (+4 / −1 câu); thử cùng context 10 đoạn (`BAO_CAO_SINH_CAU_TRA_LOI_API.md`).
- **`gpt-6-luna` xếp hạng lại:** tín hiệu tốt (0 câu mất, MRR +0,17), cần bộ có nhiều câu "đoạn đúng ở hạng 6–10" hơn để
  kết luận; đổi lại chậm thêm ~3,5 s/câu.
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
