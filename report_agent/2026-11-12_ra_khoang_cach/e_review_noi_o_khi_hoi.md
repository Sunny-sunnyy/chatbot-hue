# Review nhánh `p9-o-khi-hoi` (C) — E · 16:23 15/11/2026 (`date`) · 0 USD

Bản review: origin `6058298` (đã gộp `main`; phần code của việc này giống hệt `2456c2f` mà E đọc trước — so `git diff` 5 file: 0 khác). Căn cứ: plan `docs/superpowers/plans/2026-11-15-noi-o-chi-khi-hoi-plan.md`, diff `origin/main...origin/p9-o-khi-hoi` (6 file code / test, +53 / −7, + report), report của C, ảnh + số Playwright của C (private).

**Kết luận: `ready_for_user_confirmation`** — 0 blocker · 0 major · 2 minor (không chặn).

## Cổng tối thiểu
- Phạm vi đúng plan; `git diff --check` sạch; lời dặn / khuôn đầu ra model không đổi (diff không chạm file lời dặn, generator).
- E merge thử nhánh vào `origin/main` trong worktree tạm (không push): sạch; `npm run build` đạt; `test_luu_tru_lich` + `test_len_ke_hoach_v2` + `test_static_ui` 113 đạt.

## Bốn chỗ C nhờ soi
1. **Đường dựng khối nơi ở:** chỉ có `gan_o_an` ghi `o_dau` vào lịch — gọi ở hai chỗ: `chuan_bi` (lịch mới **và** lượt sửa đều đi qua đây) và lịch mẫu. `sua_lich_v2` chỉ gọi hàm dựng để THỬ mức, không ghi vào lịch. Lịch đã lưu trong bộ nhớ hội thoại trước khi triển khai (có khối, không mức) sẽ còn khối tới lượt sửa kế — bộ nhớ chỉ 30 phút ⇒ bỏ qua.
2. **.ics / Sao chép / .txt:** `lich_ics.js` không đọc `o_dau`; chữ thuần chỉ in khối khi lịch có `o_dau`. Ca dò dưới: 0 lượt có chữ "nơi ở" khi chưa hỏi.
3. **Dòng link:** chữ + vị trí hợp lý (ngay dưới "Ghi chú của lịch", trên dòng Nguồn; ảnh sau gộp của C). Xem m-1.
4. **Giao với "bỏ buổi để trống" của E ở `LichV2.jsx`:** hai đoạn khác nhau, git tự gộp; bản gộp build + test đạt (trên).

## Ca dò riêng của E (khác cách của C; 0 USD; trên bản merge thử, cờ như `settings.yaml`)
3.840 khung (không ngày đi + một ngày đi) × 4 trạng thái hạng = 7.680 lượt qua `dung_lich` + `gan_o_an`:
- chưa hỏi ⇒ có khối: **0**; khoá link sai (phải có đúng khi ≥ 2 ngày): **0**; chữ chép có "nơi ở": **0**;
- đã hỏi ⇒ khối khác hàm dựng gốc: **0**; còn khoá link: **0**.
- Nói một hạng trên lịch CHƯA có khối (5.760 phép thử): 4.608 được nhận, 1.152 "không có mục chỗ ở" — đúng bằng số lịch 1 ngày; **0** lần "khu này chưa có hạng đó" ⇒ câu "giữ nguyên" không xuất hiện khi chưa có khối.
- Câu báo: chưa có mức ⇒ "Đã thêm gợi ý chỗ ở hạng …"; đã có mức ⇒ "Đã đổi hạng chỗ ở: … → …" (gọi thẳng `thay_doi`).
- **Bất biến đã kiểm:** lịch có mức hạng ⇒ khối giống hệt bản trước (so với hàm dựng gốc, 5.760 lượt).

## Finding
**m-1 (gợi ý, không chặn) — dòng link không nói cho người dùng biết còn cách "nói hạng".** Người không chọn ô hạng sao chỉ thấy link sang trang Chỗ ở; đường "nhắn hạng sao để thêm gợi ý vào lịch" (điểm chính của bậc 1) không lộ ra. Đóng (tuỳ A / User): thêm nửa câu vào dòng link, hoặc nhận như hiện tại.

**m-2 (tài liệu, khi merge):** các số "ô Nơi ở có ảnh" và "lượt đổi ô Nơi ở" trong bài 25 / sổ 07 (kể cả số 8.962 / 15.360 E đo chiều nay cho ảnh khách sạn) là đo trên lịch LUÔN có khối — nay chỉ đúng cho lịch có chọn hạng; ghi chú một dòng khi cập nhật tài liệu (plan đã nêu).

## E không làm
Không chạy lại Playwright / lượt có phí của C (số "khối 0 · link 1 · mở đúng trang" và "khối 1 · 5 cơ sở 4–5 sao" là của C; E chỉ xem ảnh sau gộp).
