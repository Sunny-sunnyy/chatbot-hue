# Review — nhánh `p9-anh-lich` của B (`6c779ff`, diff `3ba7e9b..6c779ff`) · cờ `anh_lich` tắt

Người kiểm: C (`hue-rag-b4`) · 11:15 14/11/2026 (`date`) · skill `risk-gated-agent-review` · một review cả nhánh · 0 USD.

**Kết luận: ready_for_user_confirmation — 0 blocker, 0 major, 3 minor.**

## Đã kiểm
- **24 ảnh trong `frontend/public/anh/lich/` giống hệt bản B0 của C:** md5 24 / 24 khớp `data/phase_9/lich_trinh/anh_lich_v1/`. Không chép `goc/`. Ảnh vào repo public là đúng: giấy phép mở, giống ảnh cổng.
- **Rào ở server** (`nap_bang_anh`, lúc khởi động): id có trong bảng điểm và không lặp; `src` nằm dưới `/anh/lich/`, không có thư mục con, là `.jpg` và file có thật; đủ tác giả, giấy phép; trang ảnh là Commons. Sai thì không khởi động. Test thử 7 kiểu dòng hỏng.
- **Rào ở giao diện** (`anhHopLe`): kiểm lại `src` và trang Commons trước khi vẽ. Link ngoài có `noopener noreferrer`. Đường ảnh ghép `BASE_URL` như ảnh cổng (bản đầu bị 404, B đã bắt). CSP không đổi.
- **Chuỗi gửi model không đổi:** test so `tin_nhan_model` cờ bật ↔ tắt.
- **Cờ:** cần `len_ke_hoach_v2` + bảng ảnh, có test. `BOOL_FIELDS` đã loại `anh_lich_bang`.
- **Test chạy lại** (worktree từ nhánh): `test_len_ke_hoach_v2.py` 88 / 88 đạt, 24 s.
- **Dùng lại, không chạy lại:** Playwright 1440 + 390 và người xem mù 10 / 10 của B.

## Finding
| # | Mức | Vị trí | Vấn đề | Tiêu chí đóng |
|---|---|---|---|---|
| m-1 | minor | `chat.jsx` `AnhLich` | Dòng ghi công thiếu "đã thu nhỏ" (ảnh nào cũng đã thu nhỏ; ảnh Cung An Định còn bị cắt dải đáy). Ảnh CC BY / BY-SA phải ghi ra khi có chỉnh sửa; ghi công ảnh cổng đã có "đã thu nhỏ". Giấy phép cũng chưa có link như ở ảnh cổng. | thêm "· đã thu nhỏ" (bảng ảnh có thể thêm trường `doi` cho ảnh bị cắt); link giấy phép nếu tiện. Sửa được khi làm giao diện H1. |
| m-2 | minor | `index.css` `.lich-anh figcaption` | Chữ ghi công 12 px. Bản mẫu H1 đã nâng mọi chữ nhỏ lên ≥ 14 px để đọc được trên điện thoại. | 14 px, hoặc theo kiểu H1 khi thay `LichV2`. |
| m-3 | minor | test `BANG_ANH` | Test đọc bảng ảnh trong `data/` (private): clone công khai không có file này sẽ báo lỗi, giống các test đọc dữ liệu private khác. | chấp nhận được theo lệ dự án; nếu muốn, thêm thông báo có tên file khi thiếu. |

## Vòng sửa (11:18 14/11/2026, `date`) — `a192843`
- m-1 **đóng**: ghi công có link giấy phép (bảng `GP` dùng chung với ảnh cổng, phủ đủ 5 loại CC có trong bảng ảnh; "Phạm vi công cộng" không cần link) và "đã thu nhỏ"; riêng Cung An Định ghi "đã thu nhỏ, cắt dải đáy" qua trường `doi`. C đối chiếu bảng ảnh: chỉ khác đúng 1 trường ở 1 dòng so với bản sao.
- m-2 **đóng**: chữ ghi công 14 px.
- m-3 **đóng**: test báo tên file khi thiếu bảng.
**Kết luận: ready**, 0 finding mở.
