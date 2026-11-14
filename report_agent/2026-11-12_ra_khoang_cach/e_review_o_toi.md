# Review nhánh `p9-o-toi` `b52de6b` (B — khu ở theo buổi tối) · E · 17:06 14/11/2026

Mục cuối `b_luu_tru_lich_implementation.md`. Mức nhẹ, 0 USD.

## Kết luận: `ready_for_user_confirmation` — A merge được; 1 minor đề xuất (rẻ), 1 ghi nhận

## Đã kiểm
- **Phạm vi:** 3 file (`len_ke_hoach.gan_o_an` thêm `co_toi`, `luu_tru_lich.o_dau(co_toi)`, test). Không chạm tin nhắn gửi model (`o_dau` không vào `tin_nhan_model`). Lịch mẫu đi qua cùng `gan_o_an` ⇒ tự theo.
- **Đúng dữ liệu hiện tại:** E đếm bảng điểm v8 — 5 / 5 điểm có buổi tối (chợ Đông Ba, phố Nguyễn Đình Chiểu, phố Tây, phố Hai Bà Trưng, ca Huế trên sông) đều thuộc cụm của khu trung tâm ⇒ câu lý do "các buổi tối của lịch đều ở trung tâm" đúng.
- **Lịch mẫu trên nhánh:** khu "trung tâm, hai bờ sông Hương", 5 cơ sở, lý do nhắc buổi tối (trước: phía tây).
- **Cách chọn thử 1 ↔ thử 2:** bỏ thử 1 (8 / 10) giữ thử 2 (10 / 10, người xem mới, bảng có buổi tối) — đúng thứ tự "thước ghi trước, đổi một thứ". Bài học của B về bảng người xem thiếu buổi tối: đúng, nên vào sổ cải tiến.
- **Test:** `test_luu_tru_lich` + `test_len_ke_hoach_v2` + `test_cong_dot_1` 119 đạt (worktree sạch, không khoá).

## Finding
- **m-1 (đề xuất, rẻ):** `co_toi` dựa vào giả định "bộ xếp chỉ đặt buổi tối ở trung tâm" — đúng với bảng hôm nay nhưng không được kiểm. Thêm một điểm buổi tối ngoài trung tâm (vd sau này có điểm tối ở biển) thì lịch vẫn bị gợi ý trung tâm với câu lý do sai. Cách sửa 1 dòng: `co_toi` = có điểm buổi tối **và** mọi điểm buổi tối thuộc khu trung tâm (tra `cum_ve_khu`); không thì về luật cũ. Không chặn merge.
- **Ghi nhận:** mô phỏng 3.840 khung ⇒ khu phía tây 0 lần (lịch người lớn nào cũng có buổi tối). Nhánh luật phía tây gần như không còn dùng — B đã ghi để User biết; không cần gỡ.
