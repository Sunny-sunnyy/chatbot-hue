# Review — `p9-anh-chat-hoi` (C, `4993b06`) · E · 12:41 15/11/2026 (`date`)

- **Kết luận: `ready_for_user_confirmation`, 0 finding.** Nhánh nhỏ (luật 15/11): đọc diff, không chạy lại test; `git diff --check` sạch; dựng đúng trên main `5ae2a81`. Đúng plan bản 2 `6c8973b89ebd`: ngoài chữ trả lời, tên cũng được khớp trên câu hỏi; bài vẫn phải được trích, vẫn ranh giới từ, ≤ 3.
- Đã kiểm trường dữ liệu thật: `turn.question` có trong `newTurn` (`chat.jsx:71–73`) và là chữ người dùng gõ. Không phải chỉ có trong test. Câu hỏi chỉ dùng để `RegExp.test` với tên bài kho, không hiện ra, không gửi đi.
- Hai ca hụt E thấy lúc dò hệ thống (`e_do_he_thong.md`) đều được luật mới phủ: hỏi đích danh một di tích (tên chỉ trong câu hỏi) và so sánh hai quán (tên đủ chỉ có trong câu hỏi; chữ đầu không phân biệt hoa / thường nên khớp). Đây là E suy từ luật, chưa chạy lại giao diện.
- 2 ca test mới có ca đối chứng (tên trong câu hỏi nhưng bài không được trích ⇒ không ảnh). Mô phỏng C: 103 ⇒ 106 / 154, 0 ảnh cũ mất, 3 ảnh thêm đã nhìn lại.
