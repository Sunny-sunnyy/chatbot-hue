# Review nhánh `p9-lkh-nhan` `7e12f6b` (E): điểm nhấn Lên kế hoạch

- **Người kiểm:** B, 15:42 14/11/2026.
- **Mức:** nhẹ, một review cả nhánh (A giao qua E).
- **Kết luận: `ready_for_user_confirmation`.** 0 blocker, 0 major, 1 minor.

## Cổng tối thiểu
- **Diff:** 6 file, +142 / −54.
  - Server: `lich_trinh_v2.dung_lich` thêm `loai_diem` (mỗi mục) + `chang` (mỗi ngày); `cong.dung_lich_mau` bỏ câu "Điểm …", trả `truong`.
  - Giao diện: `LichV2` (sông theo từng ngày `SongNgay`, `NgayLich`, nhãn loại); `LenKeHoach` (dải "xem lịch ví dụ", nút "Xếp lịch như ví dụ"); `lkh.css`.
  - Không có gì ngoài phạm vi.
- **Chuỗi gửi model:** hai trường mới chỉ nằm trong `lich` (giao diện). B kiểm hai đường dựng tin nhắn gửi model:
  - `tin_nhan_model` chỉ đọc `id_muc`, `ten`, `nguon`;
  - `sua_lich_v2.tin_nhan_hieu` dựng từ `khung` + bảng, không từ `lich`.
  - ⇒ không trường mới nào vào model. Không cần Q1 228 (luật §8).
- **Màu theo loại điểm luôn kèm nhãn chữ** (`NHAN_LOAI_DIEM`) ⇒ đáp phản biện vòng 1 của C ("màu cần chú giải").

## Kiểm [Chạy] (0 USD, worktree tách ở `7e12f6b`)
- `tests/test_len_ke_hoach_v2.py` không khoá: 89 đạt (25 s).
- **Nút "Xếp lịch như ví dụ":** `TRUONG_MAU` qua `TruongInput` và `loi_v2` với sở thích đang hiện ⇒ hợp lệ (`None`, không lỗi). Nút gửi đúng hợp đồng biểu mẫu bản 2.
- **Ảnh chụp của E** (`data/ui_mau_2026-11-14/anh_chup/lkh_nhan_1411/`):
  - lịch 1440: sông nối đúng tâm chấm từng mục, tên chặng ("Kinh thành → Đầm phá và biển"), nhãn loại;
  - 390: dải "Xem một lịch ví dụ 2 ngày ↓" đầu trang, nút "Xếp lịch như ví dụ".
- Không chạy Playwright riêng: E đã chụp đủ 2 khổ; luật RAM 14/11 giới hạn mỗi người 1 server.

## Finding
- **m-1 (minor) — ảnh `sau_len_ke_hoach_390.png` chưa khớp code cuối.**
  - Ảnh vẫn hiện câu "Điểm di tích." dưới từng mục của lịch ví dụ, nhưng `dung_lich_mau` của `7e12f6b` trả câu rỗng (`""`); test cũng khoá `c == ""`.
  - Có thể ảnh chụp trước lần sửa cuối.
  - Tiêu chí đóng: chụp lại 390 (và 1440 nếu cũng chụp trước) trước khi A trình User.

## Ghi chú gộp
- Nhánh lưu trú của B (`p9-luu-tru-lich`) cũng sửa `LichV2.jsx` + `lkh.css`, chỉ thêm thẻ `NoiO` cuối lịch.
- E báo hai nhánh gộp sạch. Sau khi E rebase lên lưu trú: thẻ "Nơi ở gợi ý" vẫn phải nằm sau danh sách ngày (`.lkh-ngay-ds`) và trước dòng nguồn.
