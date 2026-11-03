# Implementation Report: Phase 9 B4 — bộ đo hỏi lại + hai cách trình bày chi phí (C143)

Người làm: C (Claude Opus 5.5) — không code B4
Date: 11:54 03/11/2026 (`date`)
Mục việc: tin A 03/11 (C143). Spec Phase 9 bản 9 `169c2dd5f86a` §4, §5 B4; spec bản 5 §5.4 (`077e3cb`). 0 USD. Mục lục (private): `data/phase_9/bo_do_b4/README.md`.
Report tracked: chỉ số đếm, md5, cách làm — không câu, không giá.

## 1. Phạm vi

(1) 30 câu đo "hỏi lại khi thiếu trường" + script kiểm; (2) tra web cách trợ lý du lịch trình bày chi phí + soạn 2 cách mẫu để User chọn (spec B4 "trước khi code phần chi phí"). Không code, không gọi API.

## 2. Thay đổi chính (private, `data/phase_9/bo_do_b4/`)

| File | md5 / sha256 (12) | Việc |
|---|---|---|
| `luat_ghi_truoc.md` | sha `ec0fec8ebe64` | trường, giá trị cho phép, trường bắt buộc mặc định, cách gán nhãn — ghi trước câu |
| `cau_da_thay.jsonl` | md5 `25aa9aef0bc4` | 20 câu: thiếu 10 / đủ 7 / gần giống 3 |
| `cau_sealed.jsonl` | md5 `ebf6e9e68220` | 10 câu: thiếu 5 / đủ 3 / gần giống 2 — B không mở |
| `tools/kiem_bo.py` | sha `0dbf963ea0ad` | kiểm luật + số đếm |
| `chi_phi_hai_cach.md` | sha `cad3697d014e` | tra web (3 ý đã kiểm) + cách A (liệt kê có nguồn) / cách B (cộng tạm phần có nguồn + ghi rõ phần chưa gồm) |

## 3. Kết quả quan sát

- Số câu khớp spec bản 5 §5.4 (10 / 7 / 3 đã thấy, 5 / 3 / 2 kín); câu đủ trường 10 ⇒ đúng mẫu cho sàn "hỏi lại nhầm ≤ 1 / 10".
- `kiem_bo.py` OK; lần chạy đầu bắt 2 lỗi nhãn của chính người viết (đã sửa); ca thử phá dừng đúng lỗi.
- Tra web: Codex mở 0 trang ⇒ C WebFetch kiểm 3 ý (Google AI Mode 27/08/2026 chỉ hiện giá từng lựa chọn; Triply tách giá lấy trực tiếp ↔ ước tính, không tổng cả chuyến; Luật Giá 16/2023 Điều 29 — giá niêm yết của người bán đã gồm thuế, phí). Các sản phẩm khác: tự khai.
- C khuyên **cách A** cho bản đầu (khớp mặc định spec bản 5 Q4 (a)); chọn B ⇒ plan B4 thêm phép cộng bằng code + sàn "0 tổng không ghi phần chưa gồm".

## 4. Giới hạn

Trường bắt buộc là mặc định của người viết bộ đo (plan B4 chốt). Mẫu 10 câu cho User chưa làm. Ví dụ chi phí dùng số minh hoạ.

## 5. Tiền

0 USD.
