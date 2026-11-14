# Review nhánh `p9-web-y-thieu` `c15517a` (C): mục web của câu nhiều ý chỉ viết cho ý thiếu

- **Người kiểm:** B, 15:51 14/11/2026.
- **Mức:** nhẹ, một review cả nhánh (A giao).
- **Kết luận: `ready_for_user_confirmation`.** 0 blocker, 0 major, 1 minor.

## Cổng tối thiểu
- **Diff:** 2 file, +35 / −2 (`assistant.py` `ve_y_thieu` + 3 dòng trong `cong_web`; 5 ca test). Không có gì ngoài phạm vi.
- **Chỉ chạm một chuỗi gửi model:** tin nhắn viết mục web (`dau_vao_model`), và chỉ khi `trace.nhieu_y` + chọn được vế. Câu một ý, hoặc cờ tắt ⇒ `hoi_web = query`, giống trước.
- **Ba đường gọi `cong_web` đều đúng** (B đọc code):
  - không stream: sau `answer_query`;
  - stream: sau `_finish_generated`;
  - song song: sau `_merge_spec`, mà `_merge_spec` chép cả `answer` lẫn `nhieu_y` từ trace chạy trước (không nằm trong `keep_own`).
  - ⇒ `trace.answer` đã có khi chọn vế. Nghĩa là bản sửa chạy cả trên đường giao diện dùng, dù C chỉ đo qua `/api/chat`.
- **Lệch plan "Serper vẫn nhận cả câu": hợp lý.**
  - Đường ra ngoài không đổi gì (vẫn đúng câu người dùng như main); vế tách riêng có thể mất tên nơi nên tìm kém hơn.
  - Lỗi đo được (mục web nhắc lại ý kho với số khác) nằm ở phần model viết, và đã hết: 0 / 11.
- **Không thêm rủi ro chèn lệnh:** vế đưa thêm vào là chữ của chính người dùng, vốn đã có trong câu gửi model.

## Kiểm [Chạy] (0 USD)
- `test_cau_nhieu_y.py` + `test_b6_tra_web.py` có khoá, worktree tách ở `c15517a`: **119 đạt** (24 s).
- **Dò 2 câu B tự viết:**
  - "Vé Đại Nội bao nhiêu còn vé lăng Minh Mạng bao nhiêu?" + ý thiếu "giá vé lăng Minh Mạng" ⇒ chọn đúng vế 2.
  - "Chùa Thiên Mụ ở đâu và có chỗ gửi xe máy không?" + ý thiếu "chỗ gửi xe máy ở chùa Thiên Mụ" ⇒ **hoà 4–4** ⇒ `""` ⇒ mục web viết cho cả câu (như main).

## Finding
- **m-1 (minor) — hoà điểm khi dòng ý thiếu nhắc tên nơi.**
  - Model thường viết ý thiếu kèm tên nơi ("… ở chùa Thiên Mụ"). Tên nơi lại nằm trong vế đã trả lời, nên hai vế hoà điểm ⇒ quay về đường cũ.
  - Không tệ hơn main, nhưng mất lợi ích ở đúng dạng câu hay gặp ("<nơi> ở đâu và có <dịch vụ> không").
  - Đề xuất (chỉ khi log cho thấy hay gặp): điểm của vế = từ chung với dòng ý thiếu − từ chung với phần câu trả lời có trích dẫn. Ở ví dụ trên: vế 1 = 4 − 2, vế 2 = 4 − 0 ⇒ chọn đúng vế 2.
  - Tiêu chí đóng: ghi giới hạn vào report của C, hoặc sửa + thêm ca test này.
