# Báo cáo cho bạn: Tìm kiếm — tìm đoạn liên quan (Phase 5)

**Cập nhật lần cuối: 19:58 24/10/2026 — bản 4: cập nhật sau khi dọn code món ăn (Qdrant còn 1 collection,
code ba chế độ món ăn đã gỡ, số dòng `settings.yaml` mới); kết quả tìm kiếm không đổi.**
Người viết: C · Review: A. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** nhận câu hỏi, trả về 10 đoạn trong kho tri thức có khả năng chứa câu trả lời,
  xếp theo thứ tự. Bước sinh câu trả lời chỉ đọc những đoạn này, nên tìm sai thì trả lời sai hoặc từ
  chối.
- **Đang chạy cách nào:** e5-small (chạy trên máy) tìm 30 đoạn gần nghĩa nhất trong Qdrant → BM25
  (khớp từ khóa) chấm lại 30 đoạn đó → trộn hai thứ hạng (RRF) → 10 đoạn. Reranker đang tắt. Trạng
  thái: đã đóng (bản món ăn 12/08/2026; bản toàn kho 14/09/2026).
- **Đo được (Phase 7B, 158 câu có trong kho):** điểm xếp hạng MRR@10 0,72, nDCG@10 0,76; 92% câu có
  đoạn chứa keyword đáp án lọt top-10. Chạy lại hai lần giống hệt từng byte.
- **Giới hạn chính:** yếu ở câu so sánh (MRR 0,53) và câu cần nhiều nguồn (0,54); dòng bảng giá khó
  tìm vì bảng bị tách từng dòng; BM25 tách từ theo âm tiết; chưa có reranker tiếng Việt.
- **Chi phí / tốc độ:** không tốn tiền API (model và Qdrant chạy trên máy).
- **Bạn cần quyết gì:** chưa có ở khâu này; các hướng sửa sẽ bàn khi brainstorm Phase 8.1.

## 2. Hoạt động thế nào (bản đang chạy)

```text
câu hỏi
 → e5-small biến câu hỏi thành vector → lấy 30 đoạn gần nghĩa nhất trong Qdrant
 → BM25 (khớp từ khóa) chấm lại 30 đoạn đó
 → RRF trộn hai thứ hạng → 10 đoạn
 → (tùy chọn) MiniLM xếp hạng lại — đang TẮT
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
| Tìm độc lập theo nghĩa và từ khóa rồi trộn (`native_hybrid_rrf`) | **Đã thử, chưa áp dụng** | MRR 0,726 vs 0,721 của cách đang chạy — chênh rất nhỏ, chưa đáng đổi |
| Báo lỗi rõ khi Qdrant/model lỗi, không tự đổi cách | **Đã xử lý** | `backend/retrieval/full_corpus.py` |
| Câu so sánh | **Xử lý một phần** | MRR 0,53 |
| Câu cần nhiều nguồn | **Xử lý một phần** | MRR 0,54 |
| Dòng trong bảng giá (ví dụ giá vé + miễn giảm Đại Nội) | **Chưa thực hiện** | Đoạn bảng giá đứng hạng ~191 theo nghĩa, ngoài top-30 theo từ khóa; Phase 8: nhóm dòng bảng |
| Từ ghép tiếng Việt trong BM25 ("Đại Nội") | **Chưa thực hiện** | BM25 tách theo âm tiết; Phase 8 thử ghép cặp âm tiết |
| Xếp hạng lại bằng MiniLM (tiếng Anh) | **Đã thử, chưa áp dụng** | **Chỉ thử trên bản món ăn**: MiniLM làm điểm giảm. Trên toàn kho chỉ đo tốc độ, chưa đo chất lượng; `settings.yaml:43` (`reranker: none`) |
| Reranker tiếng Việt | **Chưa thực hiện** | Phase 8, sau khi chắc đoạn đúng đã nằm trong 30 ứng viên |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

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
| Reranker MiniLM (tiếng Anh) | **có code nhưng đang tắt** | `settings.yaml:43` (`reranker: none`); `backend/reranking/cross_encoder.py:13` |
| 4 kho vector toàn kho của Phase 4–5 | **đã thay** bởi một kho `hue_full_corpus_7a2_e5_small_384` (Phase 7A2) | Qdrant chỉ còn collection này (kiểm 24/10 sau dọn) |
| Model e5-small, e5-base, HuyDang, Qwen3-0.6B trong ma trận thử | **đã thay** bởi e5-small + Qwen3-8B (Phase 7A2); 8B chưa có chỉ mục | `backend/embedding/full_corpus.py:41–66` |
| Ba chế độ bản món ăn (`dense_only`/`hybrid_*`) | **đã bỏ**: code đã gỡ khi dọn sau Phase 7 | commit `1832201`; [R2] |
| Chọn cách tìm/model thắng | **chưa làm** → Phase 8 | `Project_Status.md` §2 |

## 6. Việc còn lại / cần quyết

- Bảng giá bị tách thành từng dòng → dòng giá khó tìm (Phase 8: nhóm dòng bảng).
- BM25 tách theo âm tiết ("Đại", "Nội" riêng) → Phase 8 thử ghép cặp âm tiết.
- Chưa có reranker tiếng Việt → Phase 8 thử, sau khi chắc đoạn đúng đã nằm trong 30 ứng viên.
- Thứ tự thử ở Phase 8: [R1] §8.4.

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
