# Review nhánh `p9-so-y-va` `a2ff8d5` (C): đếm vế hỏi nối bằng "và / còn / với" + 2 trường log

- **Người kiểm:** B, 15:29 14/11/2026.
- **Mức:** nhẹ, một review cả nhánh (A giao).
- **Kết luận: `ready_for_user_confirmation`.** 0 blocker, 0 major, 1 minor (không chặn merge).

## Cổng tối thiểu
- **Diff:** 3 file, +17 / −3. `llm/assistant.py`: `so_y` + `_la_ve_hoi` + `_LIEN_TU`. `api/routes/chat.py`: 2 khoá log, chỉ có khi `trace.nhieu_y`. `tests/test_cau_nhieu_y.py`: +4 câu. Không có gì ngoài phạm vi.
- **Hành vi ghi trong report:** khớp code. Khi cờ `cau_nhieu_y` tắt, `trace.nhieu_y` = False ⇒ không có khoá log mới, không đổi lời dặn. Câu một vế ⇒ như cũ.
- **Không chạm chuỗi gửi model.** `so_y` chỉ quyết có dùng lời dặn theo ý đã duyệt hay không. C đếm 0 câu đổi số vế trên Golden 176 / an toàn 32 / hỏi kèm 10. Đúng luật "đo đúng chỗ đổi", nên không cần chạy lại các bộ đó.

## Kiểm độc lập [Chạy] (0 USD, worktree `/tmp/b_rv` tách ở `a2ff8d5`)
- `tests/test_cau_nhieu_y.py` không khoá: 29 đạt (19 s).
- **Dò 9 câu biên** B tự viết:
  - "Đại Nội còn mở cửa không?" ⇒ 1 (đúng: "còn" là trạng từ, vế trước không có từ hỏi).
  - "Đi chùa Thiên Mụ với lăng Tự Đức mất bao lâu?" ⇒ 1 (đúng).
  - "Tôi đi với bạn, nên ở đâu?" ⇒ 1 (đúng).
  - Bốn câu hai ý thật ⇒ 2 (đúng): "Vé còn bán không và giá bao nhiêu?" · "Ăn gì và ở đâu…" · "…khác gì… và ăn ở đâu…" · "…tháng mấy đẹp còn tháng nào mưa nhiều?".
- Chưa kiểm lại: lượt có phí 10 / 10 của C (dùng lại số của C; không chạy lại vì không bảo vệ thêm sàn nào); test rộng của C (C đang chạy).

## Finding
- **m-1 (minor) — "với" là giới từ có thể đếm thừa.**
  - Ví dụ: "Nên mua gì làm quà với giá bao nhiêu?" ⇒ 2, trong khi người hỏi chỉ hỏi một ý (món quà trong tầm giá).
  - Hậu quả nhỏ: câu đi luật theo ý. Nếu kho không có giá thì có dòng "Tư liệu chưa có thông tin về: …" + cổng web, không tệ hơn đường cũ (thiếu ý ⇒ từ chối cả câu).
  - Golden / an toàn: 0 câu bị ảnh hưởng (số đếm của C).
  - Tiêu chí đóng: ghi giới hạn này vào report của C; chỉ sửa (bỏ "với" khỏi `_LIEN_TU`) nếu log `nhieu_y` cho thấy câu loại này hay gặp.
- **Ghi nhận cùng C** (ngoài phạm vi): mục web tra cả câu, nên viết lại ý kho đã có với số khác. Hướng "chỉ tra phần ý thiếu" hợp lý, cần mục việc riêng.
