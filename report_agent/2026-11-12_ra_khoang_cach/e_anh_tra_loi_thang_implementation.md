# Hỏi kèm ảnh: một tên thì trả lời thẳng, 2–3 tên thì chọn (phương án lai)

E, 21:05 15/11/2026 (`date`). User thử bản "ảnh đính kèm" tối 15/11 và coi bước bắt bấm tên là lỗi; sau khi xem số đếm (bước nhận ảnh trả 1 tên: đúng 31 / 33; trả 2–3 tên: tên đầu đúng ~65 % — số của B, E không tính lại) User chọn phương án lai. Nhánh `p9-anh-tra-loi-thang` từ origin/main `c0e6c94`. Chỉ `frontend/` (3 file); route + lời dặn server không đổi — **model trả lời vẫn không nhìn ảnh**, câu trả lời từ kho theo TÊN, có nguồn.

## Hành vi

| Bước nhận ảnh trả | Trước (main) | Sau |
|---|---|---|
| Đúng 1 tên | thẻ "chọn đúng tên" — phải bấm | **tự hỏi ngay** câu ghép (`<câu đã gõ> (Trong ảnh: <tên>)`; ô rỗng ⇒ "Giới thiệu về <tên>") ⇒ câu trả lời hiện như thường. Trên ô nhập có thẻ gọn "Mình đoán trong ảnh là **<tên>** — có thể sai." + nút "Không đúng — tôi gõ tên"; thẻ không chặn: gõ câu kế + Hỏi thì thẻ tự đóng |
| 2–3 tên | thẻ chọn tên | **giữ** thẻ chọn tên (bấm Hỏi lúc thẻ mở ⇒ dòng nhắc) |
| 0 tên / lỗi | lời báo, gỡ ảnh, giữ chữ | như cũ |

Thêm: bong bóng câu hỏi của lượt hỏi bằng ảnh hiện **ảnh nhỏ + đúng chữ người dùng gõ** (không còn đuôi "(Trong ảnh: …)"; câu gửi server vẫn là câu ghép). Chọn / dán ảnh vẫn 0 yêu cầu mạng trước khi bấm Hỏi.

## Kiểm [đã chạy] — Playwright 1440, server tạm của nhánh; số tên dựng bằng chặn route ảnh trong trình duyệt, câu hỏi đi server thật

| Ca | Kết quả |
|---|---|
| Trước khi bấm Hỏi | 0 lần gọi route ảnh |
| 1 tên + "đây là đâu?" | đúng 1 lần gọi route ảnh; **không bấm gì thêm** ⇒ có câu trả lời + 1 nguồn; câu gửi có đuôi tên; bong bóng hiện ảnh + "đây là đâu?"; thẻ "Mình đoán…" hiện, 0 thẻ chọn tên; ô nhập trống, ảnh đính kèm đã gỡ |
| Gõ câu kế lúc thẻ "Mình đoán…" còn mở | thẻ đóng, câu đi như câu thường, bong bóng không ảnh |
| 1 tên, ô rỗng | câu gửi + bong bóng "Giới thiệu về <tên>", có ảnh; "Không đúng — tôi gõ tên" đóng thẻ |
| 2 tên | 0 lượt tự hỏi; thẻ có 2 nút tên; chữ giữ trong ô; bấm Hỏi ⇒ dòng nhắc, vẫn 0 lượt; bấm tên thứ hai ⇒ câu gửi mang tên đó, bong bóng ảnh + chữ gõ |
| 0 tên | lời báo "chưa nhận ra", ảnh gỡ, chữ còn, 0 lượt hỏi |
| Ảnh THẬT (không chặn), 1 lượt | bước nhận ảnh trả 1 tên ⇒ tự hỏi ⇒ có câu trả lời — **nhưng tên SAI** (xem dưới) |
| Console | 0 lỗi |
| `npm run build` · `test_static_ui.py` | đạt · 4 passed (7 s) |

Tiền ≈ 0,005 USD (7 lượt hỏi 0,0028 theo `git_sha` + 4 lượt nhận ảnh thật ≈ 0,002). Script + ảnh (private): `data/anh_tra_loi_thang_2026-11-15/` — `pw_lai.py`, `ra_lai/`. Ảnh cho User: `ra_lai/A_mot_ten_tra_loi_luon.png`, `ra_lai/C_hai_ten_the_chon.png`.

## Rủi ro đã thấy thật (báo A / User)

Lượt ảnh thật duy nhất của bộ thử: ảnh thu nhỏ một cổng trong Hoàng thành ⇒ bước nhận ảnh trả **đúng một tên nhưng là tên một lăng** ⇒ trợ lý trả lời thẳng "Đây là <lăng đó>" kèm ảnh + nguồn của lăng — nhìn rất chắc chắn mà sai nơi. Lưới còn lại chỉ là dòng "Mình đoán… — có thể sai" phía trên ô nhập. Cùng ảnh này tối nay qua 4 lượt nhận ảnh trước đó: 1 lượt đúng một tên, 1 lượt hai tên, 2 lượt lỗi model ⇒ bước nhận ảnh **dao động theo lượt**; số "1 tên đúng 31 / 33" đo trên bộ ảnh khác. Đây là một quan sát (n = 1, ảnh nhỏ 480 px), không phải tỉ lệ. **Đã làm thêm (A duyệt):** dòng "Mình đoán trong ảnh là <tên> — có thể sai." nay hiện ngay ĐẦU câu trả lời của lượt mà hệ thống tự chọn tên (giao diện chèn, không vào chuỗi gửi model; lượt người dùng tự bấm chọn tên thì không có dòng này); thẻ gọn trên ô nhập + nút "Không đúng — tôi gõ tên" vẫn giữ. Chạy lại cả bộ ca: dòng đứng ngay trước chữ trả lời ở ca 1 tên và ca ảnh thật (lượt thật lần này vẫn ra tên lăng sai — nay có dòng cảnh báo ngay trên câu trả lời); ca 2 tên: 0 dòng. Hai câu chữ còn tả luồng cũ (cột trái trang Trợ lý, trang Giới thiệu) đã viết lại theo phương án lai. Ảnh mới: `ra_cuoi/A_luot.png`, `ra_cuoi/E_luot_anh_that.png`.

## Giới hạn

- Đang "Đang xem ảnh…" mà người dùng bấm một câu gợi ý ⇒ lượt gợi ý chạy, lượt ảnh tự hỏi bị bỏ lặng (không gặp trong bộ thử).
- URL ảnh của bong bóng câu hỏi sống tới khi tải lại trang (không thu hồi) — vài trăm KB mỗi ảnh.
- Mới chụp khổ 1440.
