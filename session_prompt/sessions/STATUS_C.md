# STATUS C — 05/11 (gọn lại 11:44 05/11/2026 `date`, luật ≤ 30 dòng — commit `1d1fa77`)

Lịch sử trước khi gọn: `git show 1d1fa77:session_prompt/sessions/STATUS_C.md`. Số liệu nằm trong report, file này chỉ trỏ tới.

**Terminal:** C `hue-rag-52` · A `hue-rag-b0` · B `hue-rag-48` · E `hue-rag-7a`. Việc A giao = User nói "làm đi".

## Đang chờ
- **Kín B5 XONG** (11:51, 0,004612 USD): `data/phase_9/b5/kin/KET_QUA.md` — Q2a 5 / 5; `kiem_cuoi` bắt 1 / 5 (K-L3, D8 (1) báo nhầm: tên bảng làm ngữ cảnh lịch sử). A quyết Q2 đạt theo nội dung (rút lại ⇒ Q5, giới hạn). **Chờ User chấm Q3:** `data/phase_9/b5/kin/phieu_cham_user.md`. Gỡ `/tmp/c_b5kin*` sau khi A chốt.
- **C192 sửa kho giờ (plan `65e7e2b2b68c`):** lệnh xoá collection bị auto mode chặn ⇒ kho đã khôi phục từ bản sao, chỉ mục nguyên 8424. **Chờ User `! bash /tmp/c192/chay.sh`** (`eb101131f146`, bước 0 kiểm backend = `5a8aa5e`; nhắn B / E tắt server trước). Sau đó: Golden 11 + an toàn 10 bên "sau" + 1 câu thật + judge. Dữ liệu `data/sua_kho_2026-11-05_gio/`. Đã tốn 0,010791 (bên "trước").
- **C193 plan sửa lịch:** bản 3 `…/2026-11-05-phase-9-sua-lich-plan.md` `5b68f3cb666a` — E vòng 2 **ready** (review `f03506e4c25e`); chờ A duyệt sha. Code chỉ khi B5 bật.
- **C194 plan B5b:** bản 2 `cc09fda9f634` — E vòng 2 **ready** (`cd94d8384f9e`); chờ A duyệt. **User duyệt bảng v4:** `data/phase_9/lich_trinh/diem_cho_user_v4.md`.
- **C195 plan B6:** bản 2 `…/2026-11-05-phase-9-b6-plan.md` `b6a046e944c0` (trần 0,22 / dừng 0,21) — B review sau B5c.

## Xong hôm nay (chi tiết ở file đầu ra)
- C196 bộ đo: `data/phase_9/bo_do_sua_lich/` (10 + 5 kín, kiem_bo OK 6/6) · bảng `diem_v4.json` (kiem_v4 OK) · B6 + L01 / K-L01 lưu trú. · C197 toạ độ `diem_toa_do.json` 17 / 28 + gợi ý 5 điểm trong nhà (`toa_do_ghi_chu.md`).
- C173–C187: plan / review B4b, B5, B5c, Phase 10 A1; #6 report; #13/#14; bộ B5, B5c (kín không chạy); dữ liệu mở ⇒ `data/nguon_mo_huegov_2026-08-05/`.
- C188 bộ ảnh Phase 10 (kín không chạy) + ảnh minh hoạ 38/42 · C189 kho thiếu gì · rà soát over-engineering · C191 review B5 (ready) · #6 vòng 2 (ready). · C191 review B5 + #6 vòng 2: ready (gỡ `/tmp/c_b5kin`, `/tmp/c_q1main`, `/tmp/c191`, `/tmp/c_toc_do6b_r` khi A merge xong)
- **Tiền C 05/11:** 0,035249 USD (C174 0,019846 + kín B5 0,004612 + C192 "trước" 0,010791).

## Dọn khi xong
- `/tmp/c188/` (script + ảnh tạm C188) — xoá khi A chốt C188. `/tmp/c_b5kin` + `/tmp/c_b5kin_run` — gỡ sau kín B5. `/tmp/c_toc_do6` giữ cho review #6.

## Bẫy (giữ)
- Ảnh tải về: xem lưới thu nhỏ trước khi gắn nhãn — tên file Commons từng sai nội dung 3 / 33.
- Commons 429: tải từng file, giãn 8 s; `tai_anh.py` ghi đè phiếu + đánh số lại mỗi lần chạy ⇒ mỗi file một thư mục rồi gộp (`/tmp/c188/gop.py`).
- Trước khi gọi một số là "sai", đọc cả file nguồn về đơn vị (C174: bảng giá tính theo một người).
- Heredoc không ngoặc có backtick ⇒ file rỗng; Markdown dài viết bằng Write.
