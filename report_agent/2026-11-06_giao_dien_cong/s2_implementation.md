# Implementation Report: S2 — giao diện cổng du lịch đợt 1

Người làm: B (Claude Code, Opus 5.5)
Date: 12:43 07/11/2026 (`date`)
Canonical guide: spec `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` §2 D1, D5, D8–D12, §3 (User chọn 07/11: Q-U1 = bản mẫu 2 "Sông Hương", không thêm font; Q-U2 (b) ảnh Commons — E đang tìm; Q-U3 ẩn "đi dày"; Q-U4 thời tiết bật khi merge; Q-U5 tên cổng).
Nhánh `p11-cong-dot-1`, commit `f20fd28`.

## 1. Phạm vi

Đã làm D1, D5, D8–D12 trong `frontend/src/`; 0 gói npm mới; 0 đổi server / CSP.

Chưa làm:
- ảnh thật: chỉ chừa chỗ bằng khối hoa văn, chờ User kiểm ảnh;
- Q-G / Q-N chính thức (S3 — C đo).

## 2. Thay đổi chính

- **`App.jsx` — khung cổng:**
  - đầu trang "Huế · Trải nghiệm văn hóa & du lịch" (điện thoại: "Trải nghiệm Huế") + menu;
  - nút nổi "Trợ lý Huế": laptop là khung 400 × 600 góc phải, không rời trang; điện thoại phủ cả màn;
  - thanh dưới trên điện thoại, nút trợ lý ở giữa;
  - cờ đọc một lần từ `/api/tinh_nang`: Lên kế hoạch / thời tiết / ảnh ẩn khi cờ tắt.
- **`route.js` — điều hướng hash (D5):**
  - `#/`, `#/kham-pha`, `#/kham-pha/<mã lĩnh vực = tên thư mục kho>`, `#/kham-pha/bai/<id>`, `#/len-ke-hoach`, `#/tro-ly`, `#/gioi-thieu`;
  - hash lạ ⇒ trang chủ.
- **`chat.jsx` — trợ lý (code cũ của `App.jsx` chuyển sang):**
  - `useChat` giữ **một** cuộc trò chuyện qua mọi trang (D8): chuyển trang không ngắt lượt; `ChatView` dùng chung cho khung nổi và trang `#/tro-ly`.
  - **D1:** chữ hiện không có số `[n]`; dưới câu có dòng "Nguồn: <tên> · <tên>"; bấm tên ⇒ đoạn gốc + link "Đọc cả bài" (khi có `bai_id`). Bỏ khung nguồn bên phải.
  - Mục web: bỏ `[w n]` khỏi chữ, nguồn web vẫn liệt kê dưới.
  - Lượt từ biểu mẫu: nút "Sửa — điền lại biểu mẫu" đưa về biểu mẫu, chọn sẵn lựa chọn cũ.
- **`pages.jsx` — các trang:**
  - **Trang chủ (D9):** hero sông, ô hỏi lớn ⇒ mở trợ lý, 5 câu gợi ý cũ đã kiểm có trong kho (không Golden / kín), 5 "bến" lĩnh vực có số bài, thẻ Lên kế hoạch, ô thời tiết hôm nay, dải "có thể sai".
  - **Danh sách (D10):** chip lọc theo loại con; thẻ chỉ có tên, loại, tóm tắt; "Xem thêm" 12 bài mỗi lần.
  - **Bài (D11):** Markdown kho qua `marked` + DOMPurify; nút "Hỏi trợ lý về điểm này" điền sẵn câu; "Bài khác cùng loại".
  - **Lên kế hoạch:** biểu mẫu số ngày (bắt buộc) / đi cùng / sở thích; không có kiểu đi (Q-U3).
  - **Giới thiệu (D12):** có ghi câu hỏi gửi OpenAI, và gửi dịch vụ tìm kiếm khi tra web.
- **`markdown.js`:**
  - link ngoài thêm `target="_blank" rel="noopener noreferrer"` (sửa trên HTML đã lọc, bằng DOM);
  - `renderArticleHtml` cho bài kho;
  - bỏ mã dở ở cuối khi chữ đang hiện dần.
- **`stream.js`:** gửi thêm `bieu_mau`.
- **`HoiBangAnh.jsx`:** nhận cờ từ `/api/tinh_nang` thay vì dò `GET /api/anh/ung_vien`. Lý do: cờ tắt thì dò ra 404 thành lỗi console mỗi lần mở trợ lý.
- **`index.css`:**
  - token bản mẫu 2 (giữ tên token cũ);
  - 2 gợi ý tương phản của C: placeholder dùng `muted`; chip trên hero nền đặc `#1E4D4F`.

## 3. Cách đã chạy thật

- Build: `cd frontend && npm ci && npm run build` (worktree).
- Server thật: cổng 8862 (`data/phase_11/cong_dot_1/tools/app_bieu_mau.py`, cờ biểu mẫu bật trên bản sao settings), phục vụ bản build.
- `data/phase_11/cong_dot_1/tools/chup_s2.py`: 11 hash × 1440 / 390, mỗi trang mở rồi tải lại; ghi lỗi console + pageerror; ảnh ở `data/phase_11/cong_dot_1/anh_s2/`.
- `tools/thu_s2_that.py`: 1 câu hỏi tự viết + 1 lượt biểu mẫu qua giao diện (Playwright, lượt thật).
- `tests/test_static_ui.py`.

## 4. Kết quả quan sát

- **Bundle JS:** 105,99 KB gzip (trần 200).
- **11 trang × 2 cỡ màn:** mở thẳng được, tải lại vẫn đúng hash, `h1` khác rỗng; **0 lỗi console / pageerror**. Lần đầu có 5 lỗi 404 mỗi cỡ (dò nút ảnh + mã bài lạ) ⇒ đã sửa, đo lại ra 0.
- **Câu hỏi thật:**
  - 0 mã `[n]` trong chữ trên trang;
  - tập tên ở dòng Nguồn = tập `title` của sự kiện `sources` (6 / 6, cả 6 có `bai_id`);
  - bấm tên ⇒ hiện đoạn gốc; "Đọc cả bài" ⇒ mở đúng trang bài.
- **Lượt biểu mẫu thật:**
  - chuyển sang `#/tro-ly`; log `lich_trinh_ok` = True;
  - "Sửa — điền lại biểu mẫu" ⇒ về `#/len-ke-hoach`, chọn sẵn đúng 2 giá trị cũ.
  - Số đếm "có link bản đồ / có nút Sửa" lúc chụp ra 0 là **lỗi của script**: script chờ nút 👍 / 👎 của lượt câu hỏi trước nên đếm sớm; nút Sửa vẫn bấm được ngay sau đó. Ghi là chưa đo sạch.
- **Tiền S2:** 0,0018 USD (2 lần chạy script thật; lần đầu dừng giữa vì script chọn nút trùng tên).
- **`test_static_ui`:** 3/3 đạt.

## 5. Lỗi và giới hạn

- Chưa có ảnh: khối hoa văn giữ chỗ trên thẻ và trang bài.
- Tóm tắt thẻ lấy "đoạn đầu" của bài; ở nhiều bài, đoạn đầu là dòng kiểu "Tên chính thức: …" — đúng dữ liệu kho nhưng chưa đẹp.
- Chưa đo bằng script tương phản trên bản build (để C đo ở S3).
- Font: chỉ nạp Be Vietnam Pro 400 / 600; chỗ CSS ghi 500 / 700 thì trình duyệt dùng mặt chữ gần nhất.
- Lượt biểu mẫu vẫn phụ thuộc kết quả X1 (xem `s1_implementation.md` §4).

## 6. Bàn giao cho người kiểm

- Đọc: `frontend/src/App.jsx` → `chat.jsx` → `pages.jsx`; diff `markdown.js`.
- Chạy lại: build; server thật; `playwright_cong.py` của C (hash và mã lĩnh vực đúng giả định của C).
- Ảnh tham khảo: `data/phase_11/cong_dot_1/anh_s2/`.

**Giải thích ngắn:** giao diện chuyển từ một trang hỏi đáp thành cổng du lịch kiểu bản mẫu 2: trang chủ có ô hỏi, 5 chủ đề, Lên kế hoạch; đọc được bài gốc của kho; trợ lý nổi dùng chung một cuộc trò chuyện qua mọi trang; câu trả lời không còn số trong chữ, thay bằng dòng "Nguồn" bấm được.
