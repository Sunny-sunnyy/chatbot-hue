# Màn "Huế qua các thời kỳ": implementation (B, 15:08 14/11/2026)

- **Giao việc:** User chọn "làm luôn chiều nay". A giao B và duyệt plan 5–10 dòng (gửi qua tin nhắn).
- **Nhánh:** `p9-hue-thoi-ky` `67d63a9` (đã push), từ `main` `31e461b`, worktree `/tmp/b_tk`.
- **Tiền:** 0 USD, không gọi model.

## Đã làm
- Thêm 2 file mới: `frontend/src/HueQuaCacThoiKy.jsx` (component `HueQuaCacThoiKy`, không props; xuất cả `MOC`) và `frontend/src/hue_thoi_ky.css`.
- **Chưa gắn vào trang nào:** C gắn vào Giới thiệu, giữa khối "Trợ lý làm được gì" và "Một câu hỏi đi qua ba bước", bên trong `.gt-than`. Component không tự có lề trang, nên phải đặt trong một khối `.khung`.
- **Sáu mốc:** 1306 Thuận Hóa · 1601–1774 chúa Nguyễn · 1788 Quang Trung lên ngôi · 1802–1945 kinh đô nhà Nguyễn · 1884–1945 gặp gỡ Đông – Tây · 1993 – nay di sản thế giới.
  - Chữ do B viết lại từ bài kho; các bài này tìm bằng `scripts/grep_kb.sh`.
  - Hook đã bắt 1 câu trùng ≥ 40 ký tự với kho; B viết lại và lần sau qua hook (0 trùng).
  - Bảng căn cứ (bài + số dòng) ở `data/hue_thoi_ky_2026-11-14/can_cu.json` (private).
- **Ảnh:** dùng 6 ảnh có sẵn ở `public/anh/lich/`, không thêm ảnh mới. Không hiện ghi công (User 14/11); nguồn ảnh chỉ nằm trong bảng ảnh lịch.
- **Cách hiện:**
  - Màn ≥ 900 px: ảnh ghim bên trái bằng CSS `sticky`; một IntersectionObserver (~6 dòng) chọn mốc đang nằm giữa màn hình; ảnh đổi bằng mờ chéo; số năm lớn đè lên ảnh; vạch tiến dần; mốc chưa đọc nhạt đi.
  - Màn hẹp: mỗi mốc ảnh trên chữ dưới, hiện dần bằng lớp `.hien` có sẵn.
  - Máy bật giảm chuyển động: không mờ chéo, mọi mốc rõ.
  - Không thêm thư viện, CSP không đổi.

## Đo [Chạy] — Playwright `data/hue_thoi_ky_2026-11-14/pw_thoi_ky.py`, kết quả `ket_qua.json`: **ĐẠT**
- Màn được gắn **tạm** vào Giới thiệu, chỉ trong worktree; đã trả lại bằng `git checkout`, không commit.
- Chạy 1440 và 390, mỗi khổ cả có hiệu ứng lẫn giảm chuyển động:
  - đủ 6 mốc;
  - cuộn từng mốc vào giữa màn hình thì mốc sáng và ảnh hiện khớp đúng 6 / 6;
  - mốc đang đọc rõ hẳn (độ đậm 1);
  - 0 ảnh lỗi, 0 cuộn ngang, 0 lỗi console.
- **Ảnh cho A trình User** (`data/hue_thoi_ky_2026-11-14/anh/`): `buoc_1440_1..6.png`, `buoc_390_1..6.png` (khung nhìn khi cuộn tới từng mốc), `ca_khoi_{1440,390}_giam_chuyen_dong.png` (cả khối). Ảnh cả khối ở 390 có thanh đầu / thanh dưới cố định đè lên: đây là do cách chụp từng phần tử, không phải lỗi trang.
- **Bản chạy để xem:** server tạm của B ở http://127.0.0.1:8877/#/gioi-thieu (bản build có gắn tạm). B tắt khi A báo xem xong.

## Giới hạn và chỗ lệch
- **Kho lệch năm Tây Sơn đóng đô:** bài Kinh thành ghi 1786–1801, bài Quần thể ghi 1788–1801. Màn chỉ nêu mốc 1788 (lễ lên ngôi, cả hai bài khớp). Cần xem lại ở lần ghi kho sau; B không sửa kho.
- Chữ là tóm tắt do B viết, chưa có người thứ hai đối chiếu với kho. Người review nên so từng câu với `can_cu.json`.
- Chưa đo CLS / thời gian tải trên trang Giới thiệu thật; để C đo sau khi gắn. JS tăng rất ít (component ~3 KB chưa nén); chưa đo gzip riêng.
