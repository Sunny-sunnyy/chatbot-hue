# Báo cáo cho bạn: Phase 5 — Tìm đoạn liên quan (truy xuất)

```text
Trạng thái: Đã đóng (bản Foods 12/08/2026; bản toàn corpus 14/09/2026)
Cập nhật lúc: 24-10-2026 +07
Người viết: C · Review: A
```

## 1. Bạn nhận được gì

Phase 5 là bước **tìm đoạn**: nhận câu hỏi, trả về 10 đoạn trong kho tri thức có khả năng chứa câu
trả lời, xếp theo thứ tự. Bước sinh câu trả lời (Phase 6) chỉ đọc những đoạn này, nên tìm sai thì
trả lời sai hoặc từ chối.

Phase 5 có hai đời:

- **Đời Foods (08/2026):** chỉ kho món ăn, ba chế độ `dense_only` / `hybrid_no_rerank` /
  `hybrid_rerank`. Nay không còn được chatbot dùng.
- **Đời toàn corpus (09/2026):** cả 5 mảng dữ liệu, hai cách kết hợp "theo nghĩa" và "theo từ khóa",
  có thể bật reranker MiniLM. Đây là bước tìm đoạn chatbot đang chạy hôm nay.

## 2. Hệ thống hoạt động như thế nào (đời toàn corpus)

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

## 3. Đã chạy và quan sát gì

| Nội dung | Kết quả | Ý nghĩa |
|---|---|---|
| Kiểm kỹ thuật lúc đóng (09/2026) | 8/8 tổ hợp model × cách tìm chạy đúng trên Qdrant thật; 23 test đạt | Bước tìm đoạn chạy đúng thiết kế |
| Chất lượng tìm đoạn (đo ở Phase 7B, 158 câu) | MRR@10 0,72 · nDCG@10 0,76 · đoạn có keyword đáp án lọt top-10: 92% | Khá tốt; yếu ở câu so sánh (MRR 0,53) và câu nhiều nguồn (0,54) |
| So hai cách tìm (Phase 7B) | `native_hybrid_rrf` 0,726 vs đang chạy 0,721 (MRR) | Chênh rất nhỏ, chưa đáng đổi |
| Chạy lại hai lần | Giống hệt từng byte | Kết quả tìm đoạn ổn định, không ngẫu nhiên |
| Lỗi đã biết: câu "giá vé + miễn giảm Đại Nội" | Đoạn bảng giá đứng hạng ~191 theo nghĩa, ngoài top-30 theo từ khóa | Bảng giá bị tách từng dòng nên khó tìm (Phase 8 xử lý) |

Lúc đóng Phase 5 chưa đo chất lượng; số chất lượng ở trên là của Phase 7B (24/10/2026), đo trên chỉ
mục hiện tại.

## 4. Cách bạn kiểm tra thêm nếu cần

Không bắt buộc. Muốn xem điểm tìm đoạn từng loại câu: report Phase 7B
`report_agent/user_reports/phase_07b_danh_gia_baseline.md`.

## 5. Hôm nay còn đúng không

Kiểm với code và `session_prompt/Project_Status.md` §4 ngày 24/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ |
|---|---|---|
| Hai cách tìm `dense_bm25_rrf`, `native_hybrid_rrf` | **còn dùng** (chatbot chạy `dense_bm25_rrf`) | `backend/retrieval/full_corpus.py:111`; `backend/config/settings.yaml:112` |
| 30 ứng viên, RRF k=60, trả top-10 | **còn dùng** | `backend/retrieval/full_corpus.py:465,608,627` |
| Reranker MiniLM (tiếng Anh) | **có code nhưng đang tắt** | `settings.yaml:113` (`reranker: none`); `backend/reranking/cross_encoder.py:13`. Benchmark Foods cũ: MiniLM làm điểm giảm |
| 4 kho vector toàn corpus của Phase 4–5 | **đã thay** bởi một kho `hue_full_corpus_7a2_e5_small_384` (Phase 7A2) | Qdrant hiện còn 3 collection; `Project_Status.md` §4 |
| Model e5-small, e5-base, HuyDang, Qwen3-0.6B trong ma trận thử | **đã thay** bởi e5-small + Qwen3-8B (Phase 7A2); 8B chưa có chỉ mục | `backend/embedding/full_corpus.py:41–66` |
| Ba chế độ Foods (`dense_only`/`hybrid_*`) | **không còn dùng** (API không gọi); nằm trong danh sách dọn | `backend/core/startup.py`, `backend/retrieval/service.py`; `reports/phase_7_cleanup_inventory_2026_10_24.md` |
| Chọn cách tìm/model thắng | **chưa làm** → Phase 8 | `Project_Status.md` §2 |

## 6. Giới hạn và bước tiếp theo

- Bảng giá bị tách thành từng dòng → dòng giá khó tìm (Phase 8: nhóm dòng bảng).
- BM25 tách theo âm tiết ("Đại", "Nội" riêng) → Phase 8 thử ghép cặp âm tiết.
- Chưa có reranker tiếng Việt → Phase 8 thử, sau khi chắc đoạn đúng đã nằm trong 30 ứng viên.

Thứ tự thử ở Phase 8: `reports/phase_8_candidate_hypotheses_2026_10_24.md` §8.4.

## Lệch phát hiện

- `settings.yaml` vẫn giữ khối `profiles`/`active_profile`/`retrieval`/`reranking` của đời Foods; code
  đời toàn corpus không đọc các khối này (reranker lấy tên model mặc định trong code), nhưng
  `load_settings` vẫn bắt buộc `active_profile` hợp lệ (`backend/core/settings_loader.py:15–21`).
  Đã ghi trong danh sách dọn C2.
