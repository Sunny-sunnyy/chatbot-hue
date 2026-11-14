# Review nhánh `p9-luu-tru-lich` `9624215` (B — nơi ở gợi ý trong lịch) · E · 15:40 14/11/2026

Plan `docs/superpowers/plans/2026-11-14-luu-tru-trong-lich-plan.md` (sha `15529d97b6c7`); report `b_luu_tru_lich_implementation.md`. E là chủ bảng 140 cơ sở
(`data/luu_tru_2026-11-14_lich/bang_luu_tru_lich.json`, md5 `a4c97df36c7c`). Mức nhẹ, một review cả nhánh, 0 USD.

## Kết luận: `ready_for_user_confirmation` — A merge được (cờ `luu_tru_lich` tắt); 2 minor không chặn

## Đã kiểm
- **Phạm vi:** 9 file, đúng bảng "Đổi gì" của report; không chạm file ngoài plan. Gộp với nhánh điểm nhấn của E (`p9-lkh-nhan` `7e12f6b`) **sạch** ⇒ merge lưu trú trước, E rebase sau.
- **Code quyết, model không chạm:** `o_dau` gán sau `dung_lich`; `tin_nhan_model` chỉ đọc `id_muc / ten / nguon` của mục ⇒ tin nhắn gửi model không đổi (B có test). Cờ tắt ⇒ `o_dau` không có ⇒ `ghep_chu` giống bản trước. Khởi động: cờ bật mà thiếu bảng / cụm không có khu / cơ sở thiếu tên–hạng–nguồn–khu ⇒ không khởi động (lỗi lộ, không im lặng).
- **Không hứa điều không có:** 0 giá, 0 "còn phòng"; nhãn "chưa kiểm giá, phòng trống" luôn có; link chỉ là trang TÌM của Booking do code dựng, giao diện kiểm lại gốc link, mở tab mới, `noopener`. Lượt sửa lịch tính lại nơi ở theo khung mới (đúng).
- **Luật khu đối chiếu bảng của E:** khu trong bảng 122 trung tâm · 10 ven biển · 5 phía tây · 3 ngoài ba khu (không bao giờ được chọn). Hai sửa của B (tách ven biển theo phía bằng chữ địa chỉ; cụm đi trong ngày `nam_xa` không đếm) đúng với dữ liệu: bảng không có cụm gần cho cơ sở ven biển, và ven biển gộp hai phía cách ~40 km. Ven biển phía đó không có cơ sở ⇒ về trung tâm, nói lý do — đúng.
- **Test:** `test_luu_tru_lich` + `test_cong_dot_1` + `test_len_ke_hoach_v2` 116 đạt (worktree sạch, không khoá). Không chạy lại 3.840 khung / người xem (số của B; bảng của E không đổi từ lúc B đo — md5 khớp).

## Finding
- **m-1 (theo dõi, B đã ghi):** lý do kiểu "Cùng khu với n / m điểm" không nhắc trẻ em / người lớn tuổi dù đoàn có — khi bật, nên thêm một vế "…, gần dịch vụ cho trẻ em / người lớn tuổi" do code (cùng luật `han_che`). Không chặn.
- **m-2:** trong một mức hạng xếp theo tên ⇒ nhiều lịch trung tâm ra cùng 5 cơ sở. Đúng plan (tất định); nếu User thấy lặp, cách rẻ: xoay theo ngày đi / số ngày (vẫn tất định). Không chặn.
