# Đếm trước khi tối ưu trợ lý — tìm thêm và mục web (B, 16:00 14/11/2026, 0 USD)

- **A giao:** đề xuất 1–2 việc tối ưu có số đo thật, đếm rẻ trước khi xây. C và E phản biện vòng 1; A chốt.
- **Dữ liệu:**
  - dòng `chat_metrics` có model `gpt-6-luna` từ 12–14/11, trong `backend/logs/application.log` và log các worktree `/tmp/*/backend/logs/`. Bỏ dòng trùng; chỉ lấy lượt stream (có `first_text_ms`). Log **có lẫn lượt đo của nhóm**, không chỉ người dùng thật;
  - lượt Golden 176 ngày 14/11 `data/sua_kho_2026-11-14_ghi_kho/sau/golden_rest.jsonl` (có `tools` với `by: model`, `n_new`).
- **Cách đếm:** script Python đọc file (chạy inline, không lưu).

## Số
| Nhóm (log, lượt stream) | n | Chữ đầu p50 / p95 | Cả câu p50 | Lần gọi model p50 |
|---|---|---|---|---|
| Trợ lý, chỉ lần tìm đầu do code | 126 | 2,29 / 4,39 s | 3,55 s | 2 |
| Trợ lý, model tìm thêm 1 lần | 37 | 5,20 s | — | 3 |
| Trợ lý, model tìm thêm 2 lần | 46 | ~7,9 s (nhóm đếm theo cách khác, n = 51) | — | 4 |
| Có mục web | 31 | 9,2 s | 20,9 s | 7 |
| Công cụ ngày | 4 | 16,2 s | 16,2 s | 8 |

**(1) Tìm thêm.**
- Golden: 42 / 165 câu trợ lý có tìm thêm. Cả câu p50: 4,40 s (1 lần), 6,28 s (2 lần), 2,23 s (không tìm thêm).
- **Tìm thêm có ích:** 41 / 52 lần đem về đoạn mới. Câu tìm 2 lần thì 10 / 10 cả hai lần đều có đoạn mới. 11 lần không ra đoạn mới, 7 trong số đó kết thúc bằng từ chối.
- **Đoán trước bằng số vế không được:** chỉ 15 / 42 câu tìm thêm là câu nhiều vế / so sánh; 31 câu loại đó không tìm thêm.
- **Thời gian nằm ở model, không ở Qdrant:**
  - một lần tìm Qdrant p50 64–66 ms;
  - lượt model gọi công cụ: p50 2,13 s mỗi câu Golden, 4,22 s tổng mỗi lượt log.
- ⇒ "trả sẵn hạng 11–20 khi model xin tìm" chỉ lợi ~0,06 s ⇒ bỏ.
- Chỉ mở rộng ngữ cảnh (k 10 ⇒ 15) mới bớt được lượt gọi model. Nhưng việc này đụng quyết định 10 đoạn (8.1 + B0), nên phải đo cả chất lượng Golden.
- **A chốt: CHƯA làm.** Nếu sau này mở, cách đếm (≈ 0,02 USD): chạy lại 42 câu Golden có tìm thêm, ghi mã đoạn mỗi lần tìm thêm đem về, rồi so với hạng 11–20 của lần tìm đầu. Đếm theo **lượt** (E): lượt mà mọi đoạn mới đều đã có sẵn ở hạng 11–15. ≥ 50 % lượt mới đáng thử.

**(2) Mục web.**
- 31 / 31 lượt có web đều đã từ chối phần kho trước.
- Chữ đầu p50 9,2 s gồm: 2 lượt model gọi công cụ (p50 tổng 4,94 s) + viết câu từ chối 2,38 s. Định tuyến (p50 3,14 s) chạy song song.
- Serper p50 2,16 s, lâu nhất 5,20 s; chỉ 1 / 31 lần chạm hạn 5 s.
- Viết mục web: 1 lần gọi mỗi lượt, p50 4,94 s, ~640 token vào / 316 ra / 214 token suy luận ⇒ cả câu p50 20,9 s.
- **A chốt:** thử mức suy luận "low" cho lần viết mục web, cờ riêng, B làm sau bài học 25. Lợi là **cả câu**, không phải chữ đầu.
- Sàn (C, E bổ sung): kiểm cuối bằng code vẫn đạt; tỉ lệ `co_muc` không giảm; 0 số ngoài đoạn trích; an toàn (câu có tra web) không tệ hơn; đọc tay vài câu xem có nói chắc hơn nguồn không.

**Câu ngày:** chỉ 4 lượt dùng công cụ ngày ⇒ quá ít ⇒ không xây (luật đếm lỗi trước khi xây; A, C, E đồng ý).
