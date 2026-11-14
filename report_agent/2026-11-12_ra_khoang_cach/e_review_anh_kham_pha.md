# Review nhánh ảnh Khám phá của C (`p9-anh-kp` @ `7351bb0`, từ main `cfb5d99`) · E, 13:19 14/11/2026

A giao. Phạm vi:
- `anhBai.js` (sinh lại bằng script);
- 143 ảnh mới trong `frontend/public/anh/kp/`;
- `KhamPha.jsx` (nhãn "Ảnh minh hoạ", ghi công ảnh web);
- `GioiThieu.jsx` + `App.jsx` + `gt.css` (sửa xô lệch);
- `kp.css`.

Cách kiểm:
- Đọc diff.
- Đếm `anhBai.js` bằng code.
- Build lại trong worktree tạm.
- Playwright trên bản build do FastAPI 8897 của C phục vụ: chụp lưới 3 chủ đề rồi nhìn ảnh so với tên bài; đo CLS 3 trang × 2 khổ.
- 0 USD.

## Kết luận: `changes_requested` (nhẹ) — 0 blocker · 0 major · 3 minor · 1 câu cần User xác nhận

**Đạt:**
- *Ảnh hiện đúng bài.* E nhìn 16 thẻ (8 quán cà phê, 4 bãi biển, 4 chợ) trên bản build: ảnh khớp tên bài. Biển hiệu / logo đọc được ở các quán chuỗi và ở 3 chợ. Bài không có ảnh vẫn là ô màu + biểu tượng.
  - Lưới 3 chủ đề: 11 / 12 thẻ có ảnh mỗi chủ đề.
  - 0 lỗi console, 0 ảnh tải hỏng.
- *Số đếm khớp commit:*
  - 167 dòng (35 Commons + 132 web), **29 `minhHoa`**.
  - 0 file ảnh thiếu.
  - 143 ảnh mới, lớn nhất 40 KB, tổng 5,0 MB.
  - Mọi link đều https.
- *CSP không đổi* (`img-src 'self' blob:`). Nhánh không sửa backend. Ảnh nằm ở `public/`, không vào JS.
- *Repo public:* `anhBai.js` không có tên bài hay đường dẫn kho. Trang Giới thiệu lấy tên bài từ `/api/kham_pha` lúc chạy. Script sinh có chạy quét trùng kho.
- *Sửa xô lệch trang Giới thiệu.* E đo lại, CLS:

  | | `#/gioi-thieu` | `#/gioi-thieu/nguon-anh` | `#/kham-pha` |
  |---|---|---|---|
  | 390 px | 0,027 | 0,027 | 0,007 |
  | 1440 px | 0,032 | 0,009 | 0,009 |

  Không cuộn ngang. Mục "Nguồn ảnh" mở sẵn bằng `open` lúc vẽ lần đầu, thay cho mở bằng code sau khi vẽ: đúng cách.

**m-1 — câu trên trang sai sau khi thêm ảnh web.**
- `KhamPha.jsx:112` vẫn ghi "Ảnh chỉ có ở bài đã có ảnh giấy phép mở."
- Nay 132 / 167 ảnh lấy từ web, không phải giấy phép mở.
- Đóng khi đổi câu, ví dụ: "Ảnh lấy từ Wikimedia Commons hoặc trang web ghi ở phần nguồn; ảnh có nhãn 'Ảnh minh hoạ' có thể không chụp đúng chính nơi đó."

**m-2 — bundle JS tăng thêm +6,5 KB gzip** (main 122,61 ⇒ nhánh 129,08 KB).
- Phần tăng là bảng ghi công 167 dòng trong `anhBai.js`, có URL dài.
- Cộng với đợt giao diện thì nay vượt ngưỡng 8 KB của plan khoảng 17 KB.
- Đóng khi chọn một trong hai:
  - (a) Chuyển bảng sang `public/anh/kp/bang.json`, tải cùng lúc với `/api/kham_pha`. Trang nào dùng thì chờ danh sách bài như hiện tại.
  - (b) Ghi lý do và để A nhận.

**m-3 — 33 ảnh web ghi nguồn bằng trang chủ của tên miền, không phải trang chứa ảnh.**
- Commit ghi 31; E đếm theo link dạng `https://tên-miền/` được 33.
- Lý do: trang chứa ảnh đồng thời là link nguồn của bài kho, mà hook chặn chuỗi trùng kho.
- Người xem bấm "Nguồn ảnh" thì không tới được trang có ảnh.
- Đóng khi: ghi lại là chấp nhận; hoặc cho phép riêng cặp link này đi qua hook. Link là URL công khai, không phải câu của kho.

**Câu cần User xác nhận (không phải lỗi code):**
- Nhánh này đưa 132 ảnh lấy từ trang web (có ảnh quảng cáo của quán, có logo thương hiệu) **vào repo GitHub public**.
- "Đồ án không thương mại, cứ lấy" (User 14/11) là cho phép dùng trong đồ án. Đẩy ảnh lên repo public là phát tán lại công khai, rộng hơn việc dùng.
- E đề nghị A hỏi User một câu trước khi merge / push lên main:
  - (a) Đẩy cả ảnh lên repo public.
  - (b) Giữ ảnh web ngoài repo (`data/` hoặc thư mục bị bỏ qua), chỉ commit code + ảnh Commons. Máy khác clone về thì bài không có ảnh web sẽ hiện ô màu.

## Kiểm phần sửa `3c5350f` (13:29 14/11/2026)
- **m-1:** câu cuối Khám phá nay ghi "Ảnh lấy từ Wikimedia Commons và các trang web, ghi nguồn từng ảnh ở trang bài và ở Giới thiệu." **Đóng.**
- **m-2:** ghi công chuyển sang `public/anh/kp/ghi_cong.json` (167 dòng, 29 `minhHoa`). `taiGhiCong` tải một lần, lưu lại; lỗi ⇒ `{}`, nên trang bài vẫn hiện, chỉ không có ảnh bên. E build lại: JS gzip **123,42 KB** (main 122,61, +0,8 KB). **Đóng.**
- **m-3:** 33 link về trang chủ tên miền — A chốt giữ. **Đóng (chấp nhận).**
- Ảnh web vào repo public: A chốt push và báo User.
- **Kết luận: `ready_for_user_confirmation`, 0 finding mở.**
