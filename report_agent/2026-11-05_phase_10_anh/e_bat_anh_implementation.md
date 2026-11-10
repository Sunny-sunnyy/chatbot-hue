# Implementation Report: Phase 10 — kiểm bật hỏi bằng ảnh trên cổng mới

Người làm: E (Claude Code, `hue-rag-22`) · Date: 09:50 08/11/2026 · Nhánh `p10-anh-bat` `ce89e42` (từ `main` `129ef30`, đã push origin)

## 1. Phạm vi

A giao (User 08/11 chọn bật hỏi bằng ảnh trước đóng gói):
- kiểm nút ảnh trên giao diện cổng đợt 1 (code ảnh vào `main` trước cổng), cờ `anh.bat` bật **chỉ ở server thử**;
- Playwright 1440 + 390: nút ở đâu, thẻ gợi ý có che câu trả lời không, 0 lỗi CSP / console;
- 3–5 ảnh thật từ bộ đo cũ, trần 0,01 USD (tiền Phase 10), ghi thời gian đoán tên mỗi ảnh;
- lỗi giao diện nhỏ thì E tự sửa;
- trang Giới thiệu thêm câu về ảnh.

**Không làm:** bật cờ trên `main`. `settings.yaml` vẫn `anh.bat: false`; A bật khi merge.

## 2. Thay đổi chính (3 file giao diện, +11 / −3 dòng)

- `frontend/src/HoiBangAnh.jsx` — **sửa lỗi che câu trả lời.**
  - Lỗi: trên trang trợ lý, khung nhập dính đáy màn hình (`.tro-ly-trang .chat-form { position: sticky }`). Thẻ ảnh nằm trong khung đó, nên khi thẻ hiện khung cao lên và đè vào cuối câu trả lời đang đọc.
  - Sửa: khi thẻ hiện / đổi trạng thái, nếu đang ở trang trợ lý thì cuộn trang xuống đáy. Khung về đúng chỗ của nó, cuối cuộc trò chuyện nằm ngay trên thẻ. Khung nổi (máy tính) không có `.tro-ly-trang` nên không cuộn.
- `frontend/src/pages.jsx` + `App.jsx` — trang Giới thiệu nhận `anh` từ `/api/tinh_nang`. **Chỉ khi cờ bật** mới hiện:
  - mục "Hỏi bằng ảnh: trợ lý gợi ý tên … (có thể sai), bạn bấm chọn đúng tên rồi mới hỏi";
  - câu "Ảnh bạn gửi được thu nhỏ, bỏ thông tin vị trí, gửi tới OpenAI để đoán tên, không lưu".
  - Đã đối chiếu câu này với code: `backend/llm/nhan_anh.py:56-65` — `exif_transpose`, `thumbnail(1024)`, lưu JPEG không truyền `exif`, không ghi đĩa.

## 3. Cách đã chạy thật

- Worktree `/tmp/e_anh_bat` (đã gỡ). `npm ci && npm run build` (bundle 106 KB gzip). Server thật `uvicorn api.app:app` cổng 8851, `--env-file .env`; cờ `anh.bat: true` chỉ trong file của worktree, đã trả lại trước commit.
- Playwright `data/phase_10/anh/e_bat/ui_bat.py` (private) với ảnh từ bộ **đã thấy** `data/phase_10/bo_do_anh/da_thay/khong_tin_cay/`. Không mở bộ kín. Ba lượt:
  - lượt 1: dừng ở ca 5 vì trên điện thoại không có nút trợ lý nổi (đúng thiết kế, xem mục 4); ảnh chụp ở `ket_qua_luot1_dung/`;
  - lượt 2 trước sửa: 5 ca, `ca.json`;
  - lượt 3 sau sửa: 4 ca, `ca_sau_sua.json` — 2 ca có phí trên 390, rồi 2 ca 0 USD chọn file không phải ảnh, đổi khổ 390 ⇒ 1440 trên cùng trang đã có câu trả lời.
- Cờ tắt, 0 USD: `data/phase_10/anh/e_bat/co_tat.py` trên server cổng 8852 (cờ mặc định).
- Test: `cd backend && HF_HUB_OFFLINE=1 uv run --project … python -m pytest tests/test_static_ui.py tests/test_cong_dot_1.py tests/test_p10_anh.py -q` ⇒ **59 passed**. Hook `pre-commit`: 0 trùng.

## 4. Kết quả quan sát

**Nút ảnh nằm ở đâu:**
- Máy tính (1440): trang trợ lý và khung trợ lý nổi, ngay trên ô hỏi. Nút luôn nằm trong màn hình.
- Điện thoại (390): **chỉ có ở trang trợ lý**. Ở khổ ≤ 760 px, nút trợ lý nổi bị ẩn (`index.css:315`); người dùng vào trợ lý bằng nút giữa thanh dưới. Đây là thiết kế của cổng đợt 1, không phải lỗi.

**Thẻ gợi ý có che câu trả lời không** (đo bằng hộp bao của thẻ ↔ các bong bóng hội thoại):

| Khi | 1440 | 390 |
|---|---|---|
| Trước sửa, chọn ảnh khi đã có câu trả lời | **đè 1 bong bóng** (khung nhập + thẻ cao khoảng 530 / 900 px) | **đè 1 bong bóng** — câu trả lời bị cắt giữa câu, còn khoảng 130 px để đọc |
| Sau sửa | 0 bong bóng bị đè; cuối hội thoại nằm trên thẻ (cả lúc báo lỗi) | 0 bong bóng bị đè; cuối hội thoại (cả dòng Nguồn + 👍/👎) nằm trên thẻ |

**Đoán tên — 9 ca; 11 lần gọi đoán tên kể cả lượt 1 bị dừng** (tên đúng / sai theo nhãn `nhan.jsonl`):

| Loại ảnh | Kết quả | Thời gian trên trình duyệt |
|---|---|---|
| Công trình Huế (2 ảnh, 3 lượt) | đúng tên 3 / 3 (1 gợi ý / lượt) | 9,1 · 5,1 · 3,6 s |
| Món Huế (1) | đúng tên | 2,2 s |
| Công trình **ngoài Huế** giống Ngọ Môn (1) | "chưa nhận ra" — không gán nhầm | 3,5 s |
| Ảnh không liên quan (1, 2 lượt) | "chưa nhận ra" | 1,7 · 1,9 s |

- Server ghi 11 lần đoán tên (`anh_metrics`, cả lượt 1): `ms_tong` p50 **3,5 s**, cao nhất 9,1 s. Gần hết thời gian là chờ model: `ms_model` chiếm 96–99,5 %, phần xử lý ảnh 40–80 ms. Cùng mức đo 05/11 (6–9 s / ảnh ở bộ lớn).
- Sau khi bấm tên: câu ghép "Giới thiệu về <tên>" đi đúng đường hỏi thường. Đủ câu trả lời 4,8–8,6 s (n = 3 lượt bấm).

**Khác:**
- 0 lỗi CSP, 0 lỗi console, không cuộn ngang ở mọi ca, kể cả trang Giới thiệu cả 2 khổ.
- Câu về ảnh ở Giới thiệu: có khi cờ bật, **không** có khi cờ tắt.
- Cờ tắt: `/api/tinh_nang` `anh: false`, `POST /api/anh/ung_vien` ⇒ 404, 0 nút ảnh ở 2 khổ.
- Log: 16 dòng số đo (11 `anh_metrics` + 5 `chat_metrics`), 0 dòng chứa chữ câu hỏi. Đã chép sang `data/phase_10/anh/e_bat/log_metrics.txt`.

**Tiền thật (log): 0,008346 USD** — đoán ảnh 0,004627 (11 lần) + trả lời 0,003720 (5 câu). Trần 0,01. Ghi vào Phase 10: 0,098 ⇒ ≈ 0,107 / 0,15.

## 5. Lỗi và giới hạn

- **Ngoài phạm vi, gặp khi chụp ảnh (cổng đợt 1, không phải ảnh):** dòng "Nguồn" lặp cùng một tên bài nhiều lần. Một câu về lăng ra 8 lần cùng tên, vì mỗi đoạn trích của cùng bài là một nguồn và giao diện in tên bài cho từng đoạn. Đề xuất: gộp theo bài, mỗi bài một tên, bấm tên thì hiện các đoạn của bài đó. Chưa sửa — báo A.
- Cổng ổn định với cờ tắt **chưa hỏi 2 câu có phí** (trong kho / ngoài kho). Lý do: thay đổi chỉ ở 3 file giao diện, `HoiBangAnh` trả `null` khi cờ tắt, đường chat không đổi; 5 câu có phí ở lượt bật cờ đã đi đúng đường hỏi thường trên cùng bản build. Đây là **dùng lại**, không phải lượt mới — A quyết có cần 2 câu không (≈ 0,0015 USD).
- Cỡ mẫu nhỏ (5 ảnh khác nhau), chỉ để kiểm giao diện; chất lượng nhận ảnh vẫn theo số đo 05/11 (`08_BAO_CAO_HOI_BANG_ANH.md`).
- Khung nổi trên máy tính: thẻ ảnh làm vùng hội thoại của khung thấp đi (khung có chiều cao cố định), nhưng không đè lên nội dung. Ca đo khung nổi chưa có câu trả lời trước đó.
- Nhánh B `p11-ban-do` chạm `pages.jsx` / `index.css` ⇒ bên merge sau rebase. Nhánh này chỉ chạm `GioiThieu` + `App.jsx` 1 dòng.

## 6. Bàn giao cho người kiểm

- Đọc `git diff main...p10-anh-bat` (3 file), rồi xem ảnh chụp trước / sau: `data/phase_10/anh/e_bat/ket_qua/01_1440_trang_b_goi_y.png`, `04_390_trang_b_goi_y.png` ↔ `ket_qua_sau_sua/01_390_trang_b_goi_y.png`, `03_1440_trang_b_goi_y.png`.
- Chạy lại (có phí khoảng 0,002 USD):
  - build ⇒ server có `anh.bat: true` ⇒ `uv run python -I data/phase_10/anh/e_bat/ui_bat.py <BASE> <OUT> data/phase_10/bo_do_anh/da_thay/khong_tin_cay data/phase_10/anh/e_bat/ca_sau_sua.json`;
  - cờ tắt, 0 USD: `co_tat.py <BASE>`.
- Khi merge để bật: đổi `settings.yaml` `anh.bat: true` + build lại giao diện; báo cáo `08_BAO_CAO_HOI_BANG_ANH.md` (Tóm tắt: "đã bật") + `01_LUONG_HOAT_DONG_HE_THONG.md` (người dùng thấy đổi).
