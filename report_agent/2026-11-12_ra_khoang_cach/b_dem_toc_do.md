# Đếm tốc độ tới chữ đầu theo loại lượt — B · 11:07 15/11/2026 · 0 USD, không sửa code

A giao (bàn nhóm "việc tiếp", ứng viên (2) tốc độ): đếm trước khi xây. Sàn User đặt 28/10: chữ đầu trên trình duyệt **p50 ≤ 3 s, p95 ≤ 5 s**.
Script: `data/dem_toc_do_2026-11-15/dem.py` (theo loại lượt, theo nguồn), `tach_ms.py` (thời gian từng lần gọi). Chỉ đọc dòng `chat_metrics` (không nội dung).

## Log gồm lượt của ai

- Một file `backend/logs/application.log` (main), 2.290 dòng `chat_metrics` từ 27/10. **Bỏ** 561 dòng pytest (model giả `probe`) và mọi dòng không có
  lần gọi model tính tiền (test API dùng generator giả, lỗi 404 / 409 / 503 do test tạo) ⇒ còn **402 lượt gọi model thật từ 10/11**.
- 402 lượt này là: lượt đo của agent (an toàn 32, hỏi thử trước ghi kho, mô phỏng, Playwright), A chạy cổng server, User / A bấm thử.
  **Không có người dùng thật** (chưa deploy). Không tách được User với agent bấm tay; tách thô theo cụm thời gian: ≥ 8 lượt cách nhau ≤ 90 s ⇒ "đo" (264), còn lại ⇒ "lẻ" (138).
- Chữ đầu (`first_text_ms`) chỉ có ở đường stream (giao diện): **239 / 402** lượt có số. Golden harness không đi qua API ⇒ không có trong log.
- ⇒ **Tỉ lệ loại lượt phản ánh bộ câu đo, không phải người dùng thật**; số ms thì thật (cùng code, cùng provider).

## Kết quả (402 lượt gọi model thật từ 10/11; chữ đầu từ 239 lượt stream)

| Loại lượt | % lượt (402) | Chữ đầu p50 / p95 (n stream) | Cả câu p50 / p95 | So sàn 3 / 5 s |
|---|---|---|---|---|
| Lịch (biểu mẫu / lịch bản 2) | 45,3 % | 2,58 / 6,63 s (152) | 4,43 / 9,30 s | p50 đạt · **p95 trượt** |
| Câu kho thường (1 lần tìm) | 26,9 % | 2,38 / 5,87 s (58) | 3,78 / 7,69 s | p50 đạt · p95 trượt nhẹ |
| **Có tìm thêm** (model gọi `tim_kho` ≥ 1 lần nữa) | **11,4 %** | **8,57 / 14,23 s** (12) | 11,71 / 23,43 s | **trượt cả hai, ×2,9** |
| **Có mục web** | **9,2 %** | **6,78 / 10,14 s** (5) | 17,79 / 26,2 s | **trượt cả hai** |
| Ngoài phạm vi | 6,2 % | 2,90 / 5,92 s (9) | 2,31 / 4,17 s | sát sàn |
| Trò chuyện | 1,0 % | 4,38 / 5,51 s (3) | — | trượt (n = 3) |

Lượt "lẻ" (138, gần với người bấm thử nhất): tìm thêm 9,4 %, web 5,1 % — cùng cỡ.

**Thời gian đi đâu** (`tach_ms.py`, lượt stream):
- Câu thường: định tuyến 1,8 s chạy **song song** với lần gọi trợ lý đầu (2,8 s) ⇒ chữ đầu 2,5 s.
- Tìm thêm: lần gọi 1 (1,98 s) chỉ xin công cụ ⇒ tìm (0,03 s) ⇒ lần gọi 2 (3,09 s) ⇒ có khi lần 3 (2,35 s) / lần 4 (5,91 s). **Chữ chỉ ra ở lần gọi cuối** ⇒ 8,5 s = cộng nối tiếp 2–4 lần gọi.
- Web: kho từ chối sau 2–3 lần gọi trợ lý ⇒ Serper 2,2 s ⇒ lần gọi viết mục web 4,2 s.
- Tìm kho (`tim_kho`) chỉ 0,03 s ⇒ chậm hoàn toàn do **số lần gọi model nối tiếp**, không do tìm kiếm.

## Kết luận

- Hai loại trượt sàn rõ: **tìm thêm + mục web ≈ 20,6 % lượt gọi model thật** — hai nhóm tách nhau (tìm thêm 11,4 % là lượt KHÔNG có mục web; mọi lượt web
  cũng đã tìm thêm ⇒ đường có tìm thêm = 83 / 402; E tính lại 15/11, khớp); lượt lẻ 14,5 % ⇒ **trên ngưỡng 10 %** ⇒ không xếp thấp.
- n chữ đầu nhỏ (12 / 5 lượt stream) ⇒ **p95 của hai nhóm này chưa dùng được**; p50 đủ để thấy trượt (8,6 / 6,8 s so với 3 s).
  Giới hạn: n stream nhỏ (12 và 5 lượt) và tỉ lệ là của bộ câu đo ⇒ % ở người dùng thật chưa biết.
- p95 của lịch (6,6 s) và câu thường (5,9 s; E đếm 5,92 s trên n = 70) cũng trượt sàn 5 s — đuôi do provider / lần gọi dài, ưu tiên sau.

## Hướng sửa (chưa làm — mỗi hướng là một bậc đo `run-experiment`)

1. **Bớt lần gọi nối tiếp ở tìm thêm:** cho lần tìm đầu (code) lấy rộng hơn để model ít phải xin thêm; hoặc hạ trần tìm thêm 2 ⇒ 1. Ước lợi: bỏ 1 lần gọi ≈ −2,4 s ở ~½ lượt tìm thêm
   (lượt có lần 3–4). Sai khi: câu cần nhiều nguồn trả lời thiếu ý ⇒ đo câu chạm Golden (đổi chuỗi gửi model) + an toàn 32. Rủi ro chất lượng — phải đo, không đoán.
2. **Web: gọi Serper sớm** — khi lần gọi trợ lý đầu đã có tín hiệu kho không đủ, chạy Serper song song lần gọi kế thay vì sau cùng. Ước lợi ≈ −2 s chữ đầu mục web. Sai khi: gọi Serper cho câu
   cuối cùng kho trả lời được ⇒ tốn 0,001 USD / lượt thừa + câu hỏi ra ngoài nhiều hơn (đường ra đã chấp nhận, nhưng phải đếm).
- (Không tính là đạt sàn) dòng "đang tìm thêm trong kho…" hiện ngay: người dùng thấy có phản hồi, nhưng không phải chữ trả lời — sàn đo chữ trả lời.

## Đính chính — 12:50 15/11/2026 (B, đọc code + đếm lại 0 USD theo mốc merge)

Bảng trên gộp mọi lượt **từ 10/11**, nên trộn cả lượt **trước** các bản sửa tốc độ đã merge. Tách theo mốc merge:
- **Câu thường:** chỉ lấy lượt sau `1633c18` (câu ngày tính sẵn "Lịch hệ thống", 20:47 10/11) ⇒ chữ đầu **p50 2,10 s · p95 4,32 s** (n = 55 stream) — **đạt sàn 3 / 5 s**.
  Số 5,87–5,92 s cũ do 10 lượt đo "trước" của chính bản sửa đó (19:20–19:22 10/11, model gọi công cụ `ngay_lich` khi chưa có lịch tính sẵn).
- **Cuộc đã có lịch, hỏi câu thường:** "định tuyến 2 lần" chỉ có ở 10 lượt 14:08–14:10 14/11, **trước** `3aef0ca` (14:27 14/11 — dùng lại định tuyến của đường thường); mọi lượt sau: 1 lần.
- **Tìm thêm / mục web, sau khi bật "hết lượt tìm thì dừng"** (`9d6a0f7`, 20:07 13/11): 243 lượt gọi model thật ⇒ tìm thêm **7,8 %**, chữ đầu p50 **5,78 s** (n = 5 stream);
  mục web 3,7 % (n = 1 stream). Vẫn trượt sàn p50 3 s, nhưng phần lượt nhỏ hơn bảng trên (20,6 % ⇒ ~11,5 %), n chữ đầu rất nhỏ.
- ⇒ Hai đề xuất tốc độ B gửi lúc chuẩn bị "việc tiếp" chiều 15/11 (lịch tính sẵn bị thiếu; định tuyến 2 lần) **rút lại**: cả hai đã được sửa trước đó.
