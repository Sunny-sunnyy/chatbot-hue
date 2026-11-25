# TỔNG HỢP NGÀY 25/11/2026

Ghi lúc `22:11 25/11/2026` (giờ `date`).

## 1. Diễn biến chính trong ngày
- **Sáng – trưa (`a8ca8758`):** chuyển quy trình làm việc của nhóm từ Claude Code sang Gemini (`agy` CLI) + `/swarm`: chuyển 32 file bộ nhớ sang `data/bo_nho_agent/` (riêng tư, ngoài git), nối symlink `.agents/skills -> ../skills`, cấu hình Playwright MCP, cập nhật `AGENTS.md`, `START_SESSION.md`, `WORKFLOW.md`, `HIEN_TRANG.md`, dọn sổ chuyển giao.
- **Chiều (`c2d0ee68` + `bc1dbbbf` + `3abd261a` + `f67e8bfe`):**
  - Mở tính năng **Hoàn tác lần sửa này** (`sua_lich_hoan_tac: true`) và **Dải "Hồ sơ theo chủ đề" ở Trang chủ** (`chu_de_trang_chu: true` + đổi tiêu đề 5 ô thành `"Khám phá theo lĩnh vực"`, bản deploy tự ẩn theo `ho_so_chu_de: false`); giữ quyết định không thêm tính năng từ 25 repo ngoài.
  - Hoàn tất 4 việc bộ `deploy/` (`USER hue` + `cap_drop`/`no-new-privileges`, nhắc loại `/api/so_tay` & `/api/ho_so` ở Caddy, kiểm giả `X-Forwarded-For`, đoạn "Vì sao không CI/CD").
  - Đổi cấu hình model viết mặc định của máy local từ `bedrock` về `openai` / **`gpt-6-luna`** (theo lời chủ dự án `15:41`); giữ nguyên việc gác thuê GPU nhận ảnh (`15:17`).
  - Chạy đủ **cả bộ test** trên `c2d0ee68`: **101 file · 4 bỏ (cần khoá OpenAI) · 97 chạy · 2.397 ca đạt · 0 file đỏ**, kiểm Playwright trên bản ghép (17 lượt = `0,008213 USD`) + live `main` (`0,000572 USD`), đồng bộ 19 file giáo trình và đóng vòng cải tiến 3 ngày (`improve-workflow`, 0 luật mới).
- **Chiều tối (`ea96e47c`, sau buổi chủ dự án tự test `16:44–17:10`):**
  - Gỡ sạch nút/route/test/cấu hình **`"Vì sao trả lời vậy?"`** (`vi_sao`, bài 42 cũ) theo quyết định của chủ dự án (**62 tính năng mở, 6 tắt**).
  - Ẩn bong bóng `"Tư liệu của mình chưa có thông tin này…"` phía trên khi khung `"Từ web (chưa kiểm)"` có nội dung (`moDauWeb.js`, `chat.jsx`, `test_mo_dau_web.py`).
  - Khử lặp khung hỏi tên ngắn mơ hồ (`"bỏ lăng"`) trong `sua_lich_v2.py` + test hồi quy (`test_sua_lich_hoi_truoc.py`).
  - 8 file test liên quan **111 passed**, dựng lại `frontend/dist`, `0 USD`.
- **Tối (`ea96e47c` → `e981b3a4`, `19:21–20:50`):**
  - Kiểm khói `gpt-6-luna` qua giao diện trên cổng `8035` đạt sạch (`Sổ tay` 8,95 s, `Hồ sơ Biển và đầm phá` 12,45 s, `Chùa Thiên Mụ mở cửa mấy giờ?`, `Đà Lạt`, `bỏ lăng`; `0,0051 USD` cho `/api/chat`).
  - Chuẩn bị `/tmp/b7_moc` (`p9-moc`), chạy 28 câu `N`, chủ dự án chạy `user_chay_kin.sh` 1 lần bộ câu kín trên `ea96e47c` (`0,0665833 USD`):
    - **K kín:** **7 / 7** (RAG mốc 5 / 7), đồng thuận chấm mù `e` ↔ `b` **14 / 14 (100%)**.
    - **N (28 câu đã thấy):** **27 / 28** (RAG mốc 12 / 28).
    - **S kín ×2:** lộ `b_kin_10` (cả 2 lượt) và `b_kin_09` (lỗi nhà cung cấp lượt 2 sau 1 lần thử lại).
    - **T kín:** xã giao **8 / 8 (100%)**; lộ `a_kin_08`, `s15`, và `3 / 12` câu trong kho mở sang cổng web.
    - **C kín (15 chuỗi / 33 lượt):** `nho_ten` **4 / 4 (100%)**, 5 cặp hỏi tiếp thắng **5,00 vs 3,40** (đủ ý & chính xác), **4,80 vs 3,20** (liên quan), lộ `K-N2` (câu ngoài kho).
    - **L kín:** **`NOT RUN`** (`4 / 5` khớp mô phỏng trên `diem_v16.json`, dừng đúng luật ghi trước).
  - Báo cáo duyệt chéo [E_BO_CAU_KIN_LUNA_2511.md](E_BO_CAU_KIN_LUNA_2511.md), đồng bộ 9 file giáo trình (`PL_C 250`, `PL_F 191`, `PL_I 222`), dọn sạch `/tmp/b7_moc`.
  - **20:50:** Chủ dự án chốt **Phương án 2** — **dừng phần xây ở local** tại `ea96e47c`, tiếp tục gác việc thuê GPU nhận ảnh.
- **Đêm (`21:07–22:11`, `0 USD` API, đều qua review chéo `b` = `READY`):**
  - Rút gọn trang Giới thiệu theo Phương án 1 (`bad77d14` — còn 7 thẻ tính năng có Sổ tay & Hồ sơ, `Huế qua các thời kỳ`, hộp `"Lưu ý khi dùng"` 3 gạch, chân trang; Playwright 1536 px & 390 px 0 lỗi / 0 tràn ngang).
  - Ghép **7 / 8 ảnh mới** chủ dự án gửi (`bee77a0a`): Khám phá **268 / 269**, Thẻ lịch **`bang_anh_v10.json` 47 / 47 (100%)**, Lưu trú **`bang_luu_tru_lich_v7.json` 70 / 136** với nhóm 4–5 sao **24 / 24 (100%)**; `99 passed` (`test_anh_tra_loi.py` + `test_the_khach_san.py` + `test_len_ke_hoach_v2.py`); kiểm sống cổng `8036` (9 URL `/static/anh/...` HTTP 200 + 4 thẻ Khám phá xanh); dựng lại `frontend/dist`. Riêng tấm *Lễ Kỳ yên đình làng Huế* (chụp Đình Tân Lân, Biên Hòa, Đồng Nai) tạm giữ lại chờ ảnh đình làng ở Huế theo lựa chọn `21:49`.
  - Cập nhật [README.md](../../README.md) và [bai_hoc/README.md](../../bai_hoc/README.md) (`d2ebb8f8`, đủ 21 route API, bảng bộ câu kín, `gpt-6-luna`, `269 bài / 9.536 đoạn`).

## 2. Chỉ số & Tài nguyên cuối ngày
- **Kho & Chỉ mục:** `269 bài / 9.536 đoạn` (Qdrant `hue_full_corpus_7a2_e5_small_384` cổng `6335` đang bật đủ `9.536` điểm).
- **Model viết:** `gpt-6-luna` (`provider: openai`), streaming bật.
- **Tính năng:** `62 mở / 6 tắt`.
- **Chi phí OpenAI nhóm agent:** lũy kế ~**0,74 USD** / trần **2–2,5 USD** (phần chủ dự án tự test không tính vào trần; các đợt rút gọn Giới thiệu, ghép 7 ảnh và cập nhật tài liệu cuối buổi dùng `0 USD`).
- **Cổng `8010`, `8035`, `8036`, `888x`:** đều trống.

## 3. Việc nhỏ gác sang phiên sau (`session_prompt/VIEC_DANG_MO.md`)
1. Review chéo và gộp nhánh `origin/p15-d-don-giao-trinh-2511` (`06670463`) — `d` đã dọn xong 4 nhóm chỗ lệch trong 8 file `bai_hoc/giao_trinh/` (`00, 05, 30, 37, 41, PL_G, PL_H, PL_I`) ngay trước lệnh kết phiên `21:58`.
2. Đổi ảnh bài *Lễ Kỳ yên đình làng Huế* sang ảnh đình làng ở Huế khi chủ dự án cung cấp để trang Khám phá đạt `269 / 269`.
