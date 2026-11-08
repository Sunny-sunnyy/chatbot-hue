# Implementation Report: cổng đợt 1 — 7 ảnh (2 đầu trang + 5 lĩnh vực) + ghi công

Người làm: B (Claude Code, terminal `hue-rag-a1`)
Date: 08/11/2026 (bắt đầu 09:23, report 09:31 — `date`)
Nhánh: `p11-anh-cong` = `fb00719` (từ `main` `db6e15d`, đã push). Tiền: **0 USD** (không hỏi trợ lý, không gọi model).

## 1. Phạm vi

A giao "Làm tiếp" mục 1 trong `CURRENT_HANDOFF.md`: đưa 7 ảnh User chốt 17:11 07/11 vào `frontend/`, thêm dòng ghi công (tác giả · giấy phép · link).
Ảnh #5 (khai mạc Festival Huế 2024, nguồn Cục Du lịch Quốc gia Việt Nam, **không giấy phép mở**) để ngoài git; máy không có file đó thì dùng ảnh
Commons dự phòng (đoàn rước qua Phu Văn Lâu, phạm vi công cộng). Dòng ghi công phải khớp ảnh thật sự hiện ra. Ngoài phạm vi: thẻ bài / trang bài
vẫn dùng khối hoa văn (User 07/11: chỉ 7 ảnh).

## 2. Thay đổi chính

| File | Thay đổi |
|---|---|
| `frontend/public/anh/*.jpg` (7 file, 688 KB) | 2 ảnh đầu trang giữ nguyên cỡ (1600 px ngang); 5 ảnh lĩnh vực thu nhỏ cạnh ngắn 360 px (hiện trong vòng tròn ≤ 112 px) |
| `frontend/public/anh/rieng/` + `.gitignore` | ảnh #5 thật — thư mục bị git bỏ qua |
| `frontend/vite.config.js` | quyết **lúc build**: có `public/anh/rieng/lv_festivals.jpg` hay không ⇒ hằng `__CO_ANH_LE_HOI_RIENG__`. Chọn cách này thay vì `onError` vì `onError` làm bản clone tải một ảnh 404 (lỗi console — Q-G đòi 0 lỗi) rồi mới đổi |
| `frontend/src/anh.js` (mới) | danh sách 7 ảnh + ghi công một chỗ; ảnh lễ hội chọn theo hằng ở trên |
| `frontend/src/pages.jsx` | trang chủ: ảnh cầu Trường Tiền làm nền đầu trang; Khám phá: dải đầu trang ảnh Ngọ Môn; 5 "bến" lĩnh vực dùng ảnh tròn thay biểu tượng SVG (bỏ `Icon` + 5 chuỗi `icon` không còn dùng); Giới thiệu: mục "Nguồn ảnh" |
| `frontend/src/index.css` | lớp phủ nước sâu `rgba(10, 61, 64, .78)` trên ảnh đầu trang; ảnh tròn 112 px (điện thoại 64 px) |
| `frontend/src/App.jsx` | chân trang thêm link "Nguồn ảnh" ⇒ `#/gioi-thieu` |
| `backend/tests/test_static_ui.py` | +1 test: mọi ảnh `anh.js` trỏ tới ngoài `rieng/` có trong repo (bản clone build đủ ảnh) + `rieng/` bị git bỏ qua |

Chỗ đặt ảnh #2 Ngọ Môn: handoff / danh sách chỉ ghi "đầu trang", không nói trang nào ⇒ B chọn đầu trang **Khám phá** (trang chủ đã có #1). A / User muốn
chỗ khác thì đổi một dòng trong `pages.jsx`.

Lớp phủ 78 %: tính theo công thức tương phản WCAG cho điểm ảnh **trắng nhất** dưới lớp phủ: chữ phụ `#CFE7E2` 4,75 : 1, chữ trắng 6,17 : 1 (sàn 4,5).
Mức 72 % chỉ đạt 4,0 ⇒ không dùng.

Ghi công: tác giả · giấy phép (link tới văn bản giấy phép CC) · link trang ảnh Commons · "đã thu nhỏ / cắt / phủ màu" (CC BY đòi ghi rõ đã sửa).
Tác giả #1 trong `danh_sach.md` bị cắt dở ⇒ đối chiếu trang Commons (WebFetch 08/11): "Supanut Arunoprayote", CC BY 4.0. Ảnh dự phòng #5: trang
Commons ghi tác giả Lưu Ly, tự nguyện đưa vào phạm vi công cộng. #5 thật: "Ảnh: Cục Du lịch Quốc gia Việt Nam" + link nguồn.

## 3. Cách đã chạy thật

- Đóng ảnh: `uv run python data/phase_11/anh_cong/tools/dong_anh.py /tmp/b_anh/frontend` (chạy 2 lần ⇒ cùng byte, git không thấy đổi).
- Build: `cd frontend && npm ci && npm run build` (worktree `/tmp/b_anh`).
- Test: `cd backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_static_ui.py tests/test_cong_dot_1.py -q`.
- Server thử: `uvicorn api.app:app --port 8871` (từ `backend/` của worktree, `--env-file` tuyệt đối), tắt bằng TaskStop.
- Trình duyệt: `uv run python data/phase_11/anh_cong/tools/kiem_anh.py http://127.0.0.1:8871/ <thư mục>` — Playwright 1440 + 390, trang chủ / Khám phá /
  Giới thiệu: ghi lỗi console + pageerror (gồm CSP) + request lỗi + mã HTTP ≥ 400, kiểm mọi `<img>` đã tải (`naturalWidth > 0`), chụp ảnh.
- Trường hợp bản clone: tạm dời `public/anh/rieng/` ra `/tmp`, build lại, chạy lại `kiem_anh.py`, rồi trả file về và build lại.

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| Test (`test_static_ui` + `test_cong_dot_1`) | **24 passed** (gồm test mới) |
| `/health` | 5 / 5 ready; `/` 200 có CSP `img-src 'self' blob:` (không đổi); `/static/anh/dau_trang_song.jpg` 200 `image/jpeg` |
| Có ảnh riêng (máy này) | 1440 + 390: trang chủ 6 ảnh, Khám phá 6 ảnh, **tất cả đã tải**; ô lễ hội = `rieng/lv_festivals.jpg`; ghi công "Cục Du lịch Quốc gia Việt Nam"; **0 lỗi** console / CSP / request |
| Bản clone (không có ảnh riêng) | ô lễ hội = `lv_festivals.jpg` (Commons), ghi công "Lưu Ly · Phạm vi công cộng"; chuỗi "Cục Du lịch" **không có** trong bundle; **0 lỗi**; không request 404 |
| Git | `git ls-files` chỉ có 7 file trong `frontend/public/anh/`, **0** file `rieng`; `lv_festivals.jpg` đã stage có md5 `4dda4d83…` = ảnh Commons, khác ảnh riêng `f9970dff…`; `git status --ignored` thấy `rieng/` bị bỏ qua |
| Hook pre-commit | chạy, 7 file "0 trùng" |
| Bundle JS gzip | 106,90 KB (trước 105,99 — sàn 200) |
| `git diff --check` | sạch |

Ảnh chụp: `data/phase_11/anh_cong/anh_co_rieng/`, `data/phase_11/anh_cong/anh_ban_clone/` (private).

## 5. Lỗi và giới hạn

- **Deploy:** máy build có `public/anh/rieng/` thì ảnh #5 (không giấy phép mở, User duyệt dùng cho đồ án) **vào `dist/`** và được phục vụ công khai. Khi lên
  link công khai cần quyết: giữ ảnh này hay build không có nó (allow-list `dung_dockerignore.py` của nháp deploy chưa tính `frontend/public/anh/rieng/`).
- Sau khi merge, working tree chính chưa có ảnh riêng ⇒ build ở `main` ra bản dự phòng. Đặt ảnh: `uv run python data/phase_11/anh_cong/tools/dong_anh.py frontend`
  (ghi lại 7 file tracked đúng byte cũ + tạo `rieng/`) rồi `cd frontend && npm run build`.
- Link "Nguồn ảnh" ở chân trang mở đầu trang Giới thiệu (mục ở cuối trang) — điều hướng hash không nhảy tới mục.
- Tương phản: tính bằng công thức cho trường hợp xấu nhất, **chưa** chạy `do_tuong_phan.py` trên bản build (Q-G là việc người kiểm).
- Cổng ổn định "1 câu trong kho + 1 câu ngoài kho": **NOT RUN** theo A (việc 0 USD, không đụng backend ngoài một test).
- Trang chủ tải ~417 KB ảnh (đầu trang 226 KB + 5 ảnh tròn ~190 KB); chưa làm bản ảnh nhỏ riêng cho điện thoại.

## 6. Bàn giao cho người kiểm (C)

- Đọc: `git diff db6e15d..fb00719` (nhánh `p11-anh-cong`), `frontend/src/anh.js` (ghi công đối chiếu `data/nghien_cuu_giao_dien_2026-11-06/anh/viwiki/bay_anh_dot1.json`).
- Rủi ro chính cần chạy lại: (1) `git ls-files` không có ảnh #5 thật; (2) bản clone (không `rieng/`) build ra ảnh dự phòng + ghi công đúng, 0 lỗi console;
  (3) có `rieng/` ⇒ ghi công đổi theo; (4) tương phản chữ trên ảnh đầu trang (`do_tuong_phan.py` hoặc tính lại).
- Script tự kiểm: `data/phase_11/anh_cong/tools/kiem_anh.py`. Worktree `/tmp/b_anh` giữ tới khi review xong.
