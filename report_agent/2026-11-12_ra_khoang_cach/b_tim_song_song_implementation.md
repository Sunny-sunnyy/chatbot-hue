# Tìm thêm song song (tốc độ) — KHÔNG ĐẠT, không bật · B · 11:46 15/11/2026

Plan `docs/superpowers/plans/2026-11-15-toc-do-tim-song-song-plan.md` bản 2 (`86d295b16017`, User duyệt). Nhánh `p9-tim-song-song` `379605b`
(cờ `tim_song_song`, mặc định **tắt** — giữ làm hồ sơ, không merge bật). Số: `data/tim_song_song_2026-11-15/` (`tom_tat.json`, `tools/so.py`).

## Đã làm

- Cờ `tim_song_song`: agent trợ lý gửi `parallel_tool_calls: true` ⇒ model **được phép** gọi 2 `tim_kho` trong một lượt. Trần 2 lần tìm, sổ nguồn, lời dặn không đổi.
- Kiểm 0 USD: (a') 50 cặp search đồng thời trên Qdrant thật ⇒ 0 lỗi, kết quả = chạy lần lượt (không cần khoá); test `tests/test_tim_song_song.py`: cờ tắt ⇒ yêu cầu như cũ,
  bật ⇒ chỉ đổi `parallel_tool_calls`; hai lần tìm trong một phản hồi ⇒ bớt 1 lần gọi, mọi `[Nguồn k]` khớp sổ nguồn (cả đường stream); lần thứ 3 vẫn bị chặn. 20 test đạt.
- Đo ×1 (11:37–11:45, máy sạch): mốc Golden 176 (cờ tắt) · biến thể Golden 176 + an toàn 32 (cờ bật tạm trong worktree, đã trả về tắt).

## Kết quả theo tiêu chí ghi trước

| Tiêu chí | Mốc | Biến thể | |
|---|---|---|---|
| Lỗi kỹ thuật | 0 | 0 | đạt |
| Từ chối nhầm (158 câu trong kho) | 5 | 5 (2 mới, 2 hết) | đạt |
| **18 câu ngoài kho bị trả lời** | 0 | **1** | **TRƯỢT sàn** |
| Lỗi trích dẫn mới | — | 0 | đạt |
| An toàn 32: đổi lớp so với kho 6 | — | 0 (29 / 3 như mốc), 0 lỗi | đạt |
| Chỉ số quyết: số lần gọi giảm trên câu mốc tìm 2 lần | 7 câu (không phải 14 như plan — kho đổi từ lượt cũ) | 7 / 7 giảm | đạt hình thức |
| **Model có gọi song song không** | — | **1 / 176 câu** | gần như không |

- **Vì sao 7 / 7 giảm:** cả 7 câu ở biến thể chỉ **tìm 1 lần** (mốc 2 lần) — model tìm ít hơn, **không** phải gọi song song. Bật `parallel_tool_calls` làm model đổi cách dùng công cụ
  (tìm ít đi) thay vì gộp hai lần tìm. Cả câu trên 7 câu: trung vị −2,3 s; trên mọi câu có tìm thêm −0,9 s — lợi đến từ bớt tìm, cùng loại với "hạ trần 2 ⇒ 1" mà plan đã gác vì rủi ro thiếu ý.
- **Câu ngoài kho bị trả lời** (loại câu hỏi giá vé đi lại từ tỉnh khác): mốc từ chối chuẩn; biến thể viết "nguồn không nêu giá… tra trên kênh chính thức" kèm 2 trích dẫn —
  không nói chắc sai, nhưng không phải câu từ chối chuẩn ⇒ theo sàn là "bị trả lời". **Tra sau (0 USD):** 6 lượt Golden đủ đã lưu đều cờ tắt; câu này bị "trả lời" ở
  `ghi_kho_2/truoc`, từ chối ở 5 lượt còn lại ⇒ cờ tắt cũng trượt 1 / 6 ⇒ nhiều khả năng là **nhiễu**, không do biến thể. Sàn ghi trước không có mức nhiễu ⇒ kết luận giữ nguyên.
- Chấm mù 140 câu đổi chữ: **NOT RUN** — kết luận đã âm theo sàn + cơ chế không xảy ra; chấm không đổi quyết định.

## Kết luận

**Không đạt — không bật cờ.** Theo plan §2 ("model hầu như không gọi song song ⇒ không đổi, gỡ cờ, ghi kết quả âm; không thêm lời dặn ép gọi song song ở bậc này").
Tiền: mốc 0,0748 + biến thể 0,0712 + an toàn 0,0217 = **0,168 USD** (trần 0,2).

**Hướng kế (chưa làm, cần chọn):** (1) thêm lời dặn "cần nhiều thông tin ⇒ gửi các câu tìm trong cùng một lượt" (đổi lời dặn ⇒ đo Golden + an toàn, rủi ro như mọi đổi lời dặn);
(2) đo thẳng "hạ trần 2 ⇒ 1" có chấm mù ý thiếu trên câu nhiều nguồn — số ở đây gợi ý −2,3 s trên câu tìm 2 lần; (3) để tốc độ sau, vì ~13 % lượt và mục web chưa có cách.
Sự cố quy trình: 11:29 lỡ gọi lượt mốc không `DRY` ⇒ lỗi khởi tạo cờ (`--flags` không dựng hàm dự báo) trước mọi lần gọi API, 0 USD; script đã đổi sang bật cờ trong settings worktree.
