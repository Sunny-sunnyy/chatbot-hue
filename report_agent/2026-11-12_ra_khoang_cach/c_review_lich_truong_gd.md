# Review — nhánh `p9-lich-truong-gd` của B (`51158d7` + `3ba7e9b`, trên `main` `86c093d`)

Người kiểm: C (`hue-rag-b4`) · 11:06 14/11/2026 (`date`) · skill `risk-gated-agent-review` · một review cả nhánh · 0 USD.

**Kết luận: ready_for_user_confirmation — 0 blocker, 0 major, 2 minor.**

## Đã kiểm
- **Diff** (3 file, +63 / −15): chỉ `len_ke_hoach.py`, `lich_trinh_v2.py`, test. Không chạm giao diện, lời dặn hay cấu hình.
- **`ngay` trên ghi chú dự báo:** `dong_du_bao` nay trả `{cau, ngay}`; dòng nguồn không có `ngay`. Chỉ một nơi gọi (`len_ke_hoach.py` → `dung_lich`). Ghi chú vẫn có `cau`, nên chỗ đang đọc `cau` không đổi.
- **`phut_di`:** bộ xếp giãn giờ bằng chính `_phut_di(trước, sau)` cho điểm kế trong cùng buổi (`lich_trinh_v2.py` dòng 266–272). Bước thay điểm lúc mưa cũng tính lại bằng hàm đó (dòng 375, 398). Vậy số hiện ra khớp đúng số đã dùng để xếp giờ. Lý do B không tính từ toạ độ là đúng: tính từ toạ độ thì giờ và "phút đi" sẽ lệch nhau. Mục đầu buổi, buổi tối và tối nghỉ không có trường này. Test khẳng định giờ mục sau ≥ giờ xong mục trước + `phut_di`.
- **Nhãn "kiểm lịch diễn":** chỉ gắn cho điểm có loại `le_hoi_nghe_thuat`. Trên bảng đang chạy (`diem_v8.json`), 5 điểm có buổi tối: ca Huế là buổi diễn duy nhất; chợ và 3 phố đêm là ẩm thực. Luật đúng với bảng hiện tại. Phố chỉ mở vài tối trong tuần không được xếp khi chưa có ngày (`dung_thu`, đã đọc code), đúng như docstring nói.
- **Chuỗi gửi model, chữ ghép:** test khẳng định không chứa trường mới. Không cần chạy Q1 (so chuỗi gửi model giống byte), đồng ý với B.
- **Test chạy lại** (worktree `/tmp` từ nhánh, `HF_HUB_OFFLINE=1`): `test_len_ke_hoach_v2.py` + `test_ban_do_lich.py` 95 / 96 đạt, 22,8 s. Một test trượt (`test_csp_adds_tile_host…`) vì worktree chưa build giao diện (`frontend/dist`). Cùng test đó chạy trên `main` thì đạt; nhánh không chạm `frontend/`, nên đây là môi trường của C, không phải lỗi nhánh.
- **Dùng lại, không chạy lại:** ca dò 9.600 khung và số đếm nhãn 228 / 960 ⇒ 0 / 3.840 của B.

## Finding
| # | Mức | Vị trí | Vấn đề | Tiêu chí đóng |
|---|---|---|---|---|
| m-1 | minor | `lich_trinh_v2.py` `co_suat_dien` | "Có suất diễn" suy từ **loại sở thích**. Hôm nay đúng (5 / 5 điểm tối), nhưng thêm một điểm tối loại lễ hội – nghệ thuật mà không phải buổi diễn (vd chợ phiên hội) thì sẽ gắn nhãn nhầm và không test nào báo. | ghi điều kiện này vào ghi chú cột bảng; hoặc khi bảng có điểm như vậy thì thêm cột riêng. Không cần sửa bây giờ. |
| m-2 | minor | giao diện sau này | `phut_di` là số ước theo cụm (15 / 30). | giao diện ghi "khoảng N phút", như report đã nói. Ghi để người làm giao diện (E / C) nhớ. |
