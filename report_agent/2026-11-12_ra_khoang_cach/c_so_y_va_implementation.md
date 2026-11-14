# Câu nhiều ý: đếm vế nối bằng "và / còn / với" + 2 trường log (C, nhánh `p9-so-y-va` `a2ff8d5`)

Cập nhật: 15:23 14/11/2026 (C). A chốt phương án (i) + m-3 của E. Mức nhẹ, không bộ kín.

## Vì sao
A thử trên main (cờ `cau_nhieu_y` đã bật), câu có hai ý nối bằng "và": một ý kho có, một ý kho không có. Kết quả: **từ chối cả câu**.
- Nguyên nhân: `so_y` chỉ tách câu theo `, ; ?` nên câu này được đếm 1 vế ⇒ luật theo ý không bật ⇒ về luật cũ (thiếu một ý ⇒ từ chối cả câu).
- Đây đúng giới hạn NK07 đã ghi ở vòng 2.

## Đổi gì
- `llm/assistant.py` `so_y`: sau khi tách theo `, ; ?`, tách tiếp theo " và / còn / với ".
  - Mỗi phần chỉ được đếm là một vế khi chính phần đó có từ hỏi (hoặc kết thúc bằng tiểu từ hỏi).
  - Vì vậy "bún bò và bánh khoái giá bao nhiêu" vẫn là 1: "và" nối hai món của một câu hỏi.
- `api/routes/chat.py`: dòng `chat_metrics` có thêm `nhieu_y: true` + `chi_y_thieu`, **chỉ khi luật theo ý đã chạy**.
  - Câu một ý, hoặc cờ tắt ⇒ dòng log như cũ.
  - Đọc log là biết câu có đi luật mới không. Bằng chứng: lượt đo dưới, đọc dòng log thật.
- `tests/test_cau_nhieu_y.py`: thêm 4 câu tự viết cho `so_y` (2 câu thành 2 vế, 2 câu giữ 1 vế).

## Đo
| Bước | Kết quả | Tiền |
|---|---|---|
| Đếm 0 USD trên Golden 176, an toàn 32, hỏi kèm 10 (`data/so_y_va_2026-11-14/tools/dem.py`) | **0 câu đổi số vế.** Golden có 42 câu chứa "và", không câu nào có hai phần cùng có từ hỏi. Theo luật "đo phần đổi": không chạy lại bộ nào trong ba bộ này. | 0 |
| 9 câu tự viết | 8 / 9 đúng kỳ vọng. Câu sai: "A hay B và uống gì" — chữ "hay" không phải từ hỏi trong luật ⇒ đếm 1 ⇒ về luật cũ (không tệ hơn main). | 0 |
| Có phí: 5 câu đổi số vế × 2 lượt qua `/api/chat`, server thật của nhánh (cổng 8874). Câu A gửi + 4 câu tự viết: 3 câu "kho + ngoài kho", 2 câu "kho + kho" | **10 / 10** luật bật (`nhieu_y: true` trong log). **0** câu bị từ chối cả câu. Ý kho có: có trả lời, có trích dẫn. Ý ngoài kho (karaoke, sửa xe, đổi ngoại tệ): **0 lần trả lời bằng kho**, đều là dòng "Tư liệu chưa có thông tin về: …". | 0,0151 USD |
| Test | `test_cau_nhieu_y.py` + `test_api_chat.py`: 39 đạt (64 s). Cả `backend/tests`: xem dưới. | — |

Độ trễ cả câu (n = 10): 5,9–20,4 s. Câu có tra web lâu nhất (10–20 s), vì phải chờ thêm một lượt tra web + một lượt gọi model viết mục web — đường có sẵn trên main, nhánh này không đổi.

## Quan sát ngoài phạm vi (báo A)
- Mục web của câu "kho + ngoài kho" dùng **cả câu hỏi** để tra.
  - Kết quả: mục web viết lại cả ý kho đã có (giờ mở cửa), với số khác kho (6:30 ↔ 7:00).
  - Mục này đã tách riêng dưới nhãn "Từ web (chưa kiểm)", nhưng có thể làm người đọc rối.
  - Hướng sửa (chưa làm): chỉ tra phần ý thiếu (chữ sau "Tư liệu chưa có thông tin về:").

## Giới hạn đã biết (review B m-1)
- "với" dùng như giới từ có thể bị đếm thừa: câu hỏi mua quà kèm "với giá bao nhiêu" được đếm 2 dù chỉ có một ý.
  - Hậu quả: luật theo ý chạy cho câu một ý. Không tệ hơn luật cũ: luật theo ý vẫn trả lời ý kho có.
  - Golden 176 / an toàn 32: 0 câu chạm.
  - Chỉ sửa khi log (`nhieu_y: true`) cho thấy loại câu này hay gặp.
- "hay" (câu chọn A hay B) không phải từ hỏi trong luật ⇒ câu kiểu "A hay B và uống gì" vẫn đếm 1, về luật cũ.

## Test rộng — PARTIAL
- Lần 1: 470 đạt, rồi dừng ở `test_ban_do_lich.py` vì worktree chưa có bản build giao diện (lỗi môi trường, không do code).
- Lần 2 (sau khi build): C tắt giữa chừng. Lý do: RAM máy về 0 GB trống — hai bộ test rộng chạy cùng lúc (của C và của một session khác), thêm 3 server.
- Test file chạm do A chạy lúc merge (`test_cau_nhieu_y` + `test_api_chat`, có / không khoá): đạt.
