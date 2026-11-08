# Review: cổng đợt 1 — 7 ảnh (2 đầu trang + 5 lĩnh vực) + ghi công

Decision: **ready_for_user_confirmation** (0 blocker · 0 major · 2 minor)
Người kiểm: C (Claude Code, terminal `hue-rag-e9`)
Date: 08/11/2026 (bắt đầu 09:43, viết 09:50 — `date`)
Nhánh: `p11-anh-cong` = `fb00719` (từ `main` `db6e15d`, 1 commit)
Implementation report: `report_agent/2026-11-06_giao_dien_cong/b_anh_cong_implementation.md` (B)
Tiêu chí (A giao): ảnh #5 thật không có trong git (kể cả lịch sử); bản clone sạch ⇒ ảnh dự phòng `5_3` + đúng ghi công; ghi công 7 ảnh khớp
`data/nghien_cuu_giao_dien_2026-11-06/anh/viwiki/danh_sach.md`; CSP 0 vi phạm; build + `test_static_ui.py` đạt; hook. Phần deploy: A quyết, không kiểm.
Tiền: **0 USD** (không hỏi trợ lý, không gọi model).

## 1. Phạm vi đã review

- Cổng tối thiểu: `git diff --stat` + exact diff `db6e15d..fb00719` (14 file: 7 ảnh, `.gitignore`, `test_static_ui.py`, `App.jsx`, `anh.js` mới,
  `index.css`, `pages.jsx`, `vite.config.js`); `git diff --check` sạch; backend chỉ đổi 1 test — không đổi code chạy, CSP giữ nguyên.
- Report B §1–§6 (đối chiếu từng kết quả với lần chạy của C ở dưới).
- Không có thay đổi ngoài phạm vi; không có file untracked lạ trong nhánh.

## 2. Findings

Không có blocker / major.

- **m-1 (minor, B đã tự khai)** — `frontend/src/App.jsx`: link "Nguồn ảnh" ở chân trang trỏ `#/gioi-thieu`, mở **đầu** trang Giới thiệu, mục "Nguồn
  ảnh" nằm cuối trang. Tác động: người xem phải tự cuộn; ghi công vẫn đủ và đúng. Tiêu chí đóng (nếu A muốn sửa): bấm link ⇒ trang cuộn tới
  `#nguon-anh`; hoặc giữ làm giới hạn đã biết.
- **m-2 (minor, số học)** — report B §2 ghi tương phản 6,17 / 4,75; C tính lại cùng công thức WCAG được **6,19 / 4,77** (lệch làm tròn). Kết luận không đổi
  (≥ 4,5). Không cần sửa code; sửa số trong report nếu tiện.

Độ đơn giản: quyết ảnh lễ hội **lúc build** (`vite.config.js` `existsSync` ⇒ hằng `__CO_ANH_LE_HOI_RIENG__`) là cách trực tiếp nhất để ghi công luôn
khớp ảnh hiện ra mà bản clone không tải ảnh 404; `anh.js` là một bảng dữ liệu, không lớp phụ. Không thấy over-engineering. Bảng rà AI FDE: không áp
(không đổi agent / công cụ / nguồn dữ liệu / đường ra).

## 3. Cách người kiểm chạy lại thật

- Quét git: `git rev-list --objects --all` (8.602 đối tượng, mọi nhánh / tag local + origin sau `git fetch`) tìm 2 blob ảnh #5 thật: bản gốc
  `ngoai_git/lv_festivals.jpg` (blob `b2005024230b`) và bản B thu nhỏ trong `/tmp/b_anh/frontend/public/anh/rieng/` (blob `8d0473e4561d`); tìm
  đường dẫn có `rieng`.
- So ảnh trong git với ảnh nguồn **bằng điểm ảnh** (khác cách B dùng md5): trích 5 ảnh lĩnh vực từ `fb00719`, thu nguồn về cùng cỡ, sai khác trung
  bình thang xám. 2 ảnh đầu trang: so blob với file trong `viwiki/`.
- Bản clone sạch: `git worktree add --detach /tmp/c_anh_rv origin/p11-anh-cong` (không có `rieng/`) ⇒ `npm ci && npm run build` ⇒ grep bundle;
  `pytest tests/test_static_ui.py tests/test_cong_dot_1.py` (lần đầu thiếu symlink kho ⇒ 1 test lifespan lỗi môi trường `knowledge base root does
  not exist`; thêm symlink `data/`, `knowledge-base-hue/` rồi chạy lại); `uvicorn api.app:app --port 8893` (tắt bằng TaskStop).
- Trình duyệt, 2 công cụ: (a) công cụ cũ của C `data/phase_9/cong_dot_1/tools/playwright_cong.py` (7 đích, CSP / console, bundle); (b) ca dò mới
  `data/phase_11/anh_cong/c_review/c_anh_probe.py` — nghe sự kiện `securitypolicyviolation` **trong trang**, cuộn hết trang để nạp ảnh lazy, kiểm mọi
  `<img>` giải mã được (`naturalWidth > 0`), ghi mọi response ≥ 400 / request lỗi, đọc chữ + link mục "Nguồn ảnh"; 1440 + 390; trang chủ / Khám phá /
  Giới thiệu. Thêm `curl` 7 link Commons trong ghi công.
- Có ảnh riêng: chép `rieng/lv_festivals.jpg` của B vào worktree ⇒ `git status --ignored` + `git add -n` ⇒ build lại ⇒ server lại ⇒ (a) + (b) + công cụ
  tương phản `tuong_phan.py` (`#/`, `#/kham-pha`, `#/gioi-thieu`) + tính tay tương phản trường hợp xấu nhất (lớp phủ trên điểm ảnh trắng); chụp màn hình.
- Ca phá rào: `git add -f` ảnh riêng (chỉ index của worktree tạm) ⇒ chạy test mới của B ⇒ `git rm --cached` trả lại.
- Hook: trong worktree tạm `git reset --soft db6e15d` (index = cây `fb00719`) ⇒ `sh .githooks/pre-commit` ⇒ `git reset --soft fb00719`.
- Dọn: gỡ symlink + `rieng/` + `git worktree remove --force /tmp/c_anh_rv`. Bằng chứng (private): `data/phase_11/anh_cong/c_review/`.

## 4. Kết quả quan sát

| Tiêu chí | Kết quả | Ý nghĩa |
|---|---|---|
| Ảnh #5 thật trong git | blob gốc **0**, blob thu nhỏ **0** trong 8.602 đối tượng; 0 đường dẫn `rieng` ở mọi commit; `git ls-tree` nhánh: đúng 7 ảnh `frontend/public/anh/*.jpg` | ảnh không giấy phép mở chưa từng vào lịch sử git |
| Ảnh trong git đúng nguồn | 2 ảnh đầu trang **cùng blob** với `viwiki/hero_song.jpg`, `hero_ngo_mon.jpg`; 5 ảnh lĩnh vực sai khác 1,3–4,1 / 255 so với ảnh Commons đã chọn; `lv_festivals.jpg` trong git: **3,2** so với ảnh Commons ↔ **97,6** so với ảnh #5 thật | ảnh lễ hội trong git là ảnh dự phòng Commons, không phải bản thu nhỏ của ảnh riêng |
| Bản clone sạch — build | `dist/anh/` 7 ảnh, không `rieng/`; bundle: "Cục Du lịch" 0, "vietnamtourism" 0, "Festival Huế 2008" có | bản clone dùng ảnh dự phòng, không lộ nguồn ảnh riêng |
| Bản clone sạch — trình duyệt | (a) 7 / 7 đích, CSP 0, console 0 ở 1440 + 390, JS gzip 102,8 KB; (b) trang chủ + Khám phá 6 / 6 ảnh giải mã, 0 sự kiện CSP, 0 request lỗi; `/static/anh/rieng/lv_festivals.jpg` ⇒ 404 | không ảnh vỡ, không lỗi |
| Ghi công 7 ảnh (bản clone) | tác giả · giấy phép · link Commons khớp `danh_sach.md` từng dòng; #1 "Supanut Arunoprayote" (đúng, không chép chuỗi cụt của danh sách); #4 / #5 dự phòng "Phạm vi công cộng" không link giấy phép (đúng — PD không có văn bản CC); mọi link `target=_blank` + `rel="noopener noreferrer"`; 7 / 7 link Commons trả 200; có "đã thu nhỏ / cắt / phủ màu" (CC BY đòi ghi sửa đổi) | ghi công đủ theo giấy phép |
| Có ảnh riêng | `rieng/` bị git bỏ qua (`!!`, `git add -n` từ chối); ô lễ hội = `/static/anh/rieng/lv_festivals.jpg`; ghi công đổi thành "Lễ hội — khai mạc Festival Huế 2024. Ảnh: Cục Du lịch Quốc gia Việt Nam · nguồn ảnh · đã thu nhỏ" + link nguồn; (a) + (b) CSP 0, console 0, 0 request lỗi | ghi công đi theo ảnh thật sự hiện |
| Tương phản | `tuong_phan.py`: 15 cặp chữ / nền, 0 cặp < 4,5; tính tay lớp phủ 78 % trên điểm ảnh trắng: chữ trắng 6,19, chữ `#CFE7E2` 4,77 | đạt sàn WCAG AA kể cả chỗ ảnh sáng nhất |
| Test | `test_static_ui.py` + `test_cong_dot_1.py`: **24 passed** (sau khi có symlink kho — lỗi lần đầu là môi trường worktree, không do nhánh) | — |
| Ca phá rào | `git add -f` ảnh riêng ⇒ test mới **FAILED** (đúng); trả lại ⇒ index sạch | test của B bắt được việc lỡ ép thêm ảnh riêng |
| Hook | 7 file 0 trùng, exit 0 | — |
| CSP header | `img-src 'self' blob:` — giống `main` (backend không đổi) | **bất biến giữ:** không mở ảnh ngoài, không đổi CSP |
| Màn hình | 1440 + 390 trang chủ / Khám phá: ảnh đầu trang dưới lớp phủ, 5 ảnh tròn đúng chủ đề, chữ đọc rõ, không tràn ngang (`c_review/*.png`) | — |

## 5. Giới hạn hoặc phần chưa chạy

- Phần deploy (ảnh #5 vào `dist/` khi máy build có `rieng/`, allow-list `dung_dockerignore.py`): **không kiểm** theo A (A quyết bản công khai mặc định không
  đưa #5).
- Cổng ổn định "1 câu trong kho + 1 câu ngoài kho": **NOT RUN** (A: việc 0 USD; backend không đổi code chạy).
- Chưa thử Firefox / Safari (chỉ Chromium của Playwright).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** Việc mức trung bình (giao diện trong phạm vi spec đã duyệt) ⇒ A đóng + merge, báo User. 2 minor không chặn: m-1 A quyết
sửa hay giữ làm giới hạn; m-2 chỉ là số làm tròn trong report. Sau merge, working tree chính cần đặt lại ảnh riêng bằng lệnh B ghi (report B §5) nếu muốn
bản build cục bộ hiện ảnh #5.
