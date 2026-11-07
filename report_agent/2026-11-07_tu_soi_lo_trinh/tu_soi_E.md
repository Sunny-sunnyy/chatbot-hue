# Tự soi over-engineering — E (12:32 07/11/2026)

Việc A giao: vòng tự soi (`Session_Prompt.md` §7), ≤ 15 phút, 0 USD. Nhãn: **[Thấy]** = E tự làm / đọc file; **[Suy]** = suy luận; **[Đề xuất]**.

## (1) Tốn mà lợi ít

- **Lịch trình câu gõ tự do (B5 → B5c → kín v1 → kín v2 → E20 → E21) [Thấy]:** plan lên bản 7; bảng điểm 6 bản (`data/phase_9/lich_trinh/diem_v*.json`), chỉ **v3** từng vào runtime, v4 / v5 / v6 chưa User duyệt. Kín v2 vẫn 3 / 5 ⇒ cờ `lich_trinh` vẫn tắt; User đã chuyển sang biểu mẫu. Phần lớn giờ + ~0,02 USD của phiên tối 06/11 (E) đi vào đường không bật.
- **Cờ tắt mang theo [Thấy]:** `settings.yaml` còn `emergency_rule`, `today_line` (âm từ 03/11), `lich_trinh`, `thoi_tiet`, `anh.bat` tắt. Mỗi cờ tắt = một nhánh code + test "cờ tắt giống byte" (228 / 228) phải giữ ở mọi thay đổi lời dặn sau này.
- **Spec / plan nhiều bản [Thấy]:** spec Phase 9 bản 9 + 3 file review (`…_review_v6`, `_v10`); plan B5 bản 7. Luật "≤ 2 vòng" (05/11) đã giảm — spec cổng đợt 1 dừng ở 2 vòng.
- **Giọng nói Phase 10 [Thấy]:** spec 373 dòng + review 126 + plan G2 201 dòng + 3 công cụ; G1 chờ User thu 40 câu từ 06/11, chưa có số đo nào; `.venv` lệch `uv.lock` (bẫy `uv sync`) chỉ vì nhánh này.
- **Chính E hôm nay [Thấy]:** `kiem_v6.py` thử 8 ca giả cho 3 ô tick — vừa đủ dùng một lần, nhưng 8 ca là hơi nhiều cho file sống vài ngày.

## (2) Bỏ / làm nhẹ [Đề xuất]

- **Đóng hẳn đường lịch trình câu tự do tới sau bảo vệ:** chỉ biểu mẫu. E20 Sửa 1 / 2, dò K2, sửa lịch trên câu tự do, `p9-sua-lich` ⇒ backlog sau 01/2027, không giữ "hoãn" trong handoff (đỡ đọc mỗi phiên).
- **Bảng điểm:** chốt **một** bản (v6 theo ô tick của User) rồi xoá v4 / v5 / nháp khỏi tầm mắt (giữ trong `data/`, không nhắc trong handoff).
- **Gỡ cờ âm lâu:** `emergency_rule`, `today_line` — gỡ code + test ở B7 (một commit), đỡ test giống byte. `thoi_tiet`: bật cùng biểu mẫu (Q-U4) hoặc gỡ; không để tắt sang tháng 12.
- **Giọng nói:** xem mục (4).

## (3) Giữ vì đã bắt lỗi thật [Thấy]

- **Bộ kín cho bậc chỉnh lời dặn:** kín v2 B5 bắt 3 / 5 trong khi bộ đã thấy đạt ⇒ ngăn bật một tính năng hỏng.
- **Test theo từng loại lượt (4c):** đã bắt lượt ghép thiếu luật ở B4 (04/11).
- **Review harness trước lượt có phí:** review harness sửa lịch của C bắt "Q4 đạt khi rỗng" (major, 06/11) trước khi tốn tiền.
- **Bộ an toàn 32 câu đủ 4 số, hook quét trùng Golden / câu kín, build record chặn index lệch kho, `grep_kb.sh`:** rẻ, chạy tự động, giữ an toàn + private.

## (4) Nhìn tới đóng code 25–30/12 và bảo vệ 04–10/01/2027

- **Giọng nói — E đề xuất cắt khỏi phạm vi đồ án** (đưa vào "hướng phát triển"), lý do [Suy]: (a) chưa có số đo nào sau 2 ngày, chặn ở việc User thu 40 câu; (b) đề tài là RAG văn hoá / du lịch — giọng nói không làm mạnh phần RAG khi trình bày; (c) thêm model ~300 MB + RAM lên máy AWS, thêm một đường lỗi lúc demo; (d) giữ nhánh ⇒ bẫy `uv sync` kéo dài. Nếu User muốn giữ: **bản nhẹ nhất** = G2 trên **10 câu** User thu (không 40), một cấu hình model, cờ tắt mặc định, chỉ demo trên máy User — không deploy.
- **Thứ tự E đề xuất:** cổng đợt 1 (S1 → S2, biểu mẫu) ⇒ **Phase 12 deploy thử sớm** (một bản chạy được trên AWS ngay khi S1 merge, trước đợt 2) ⇒ B7 đóng gói ⇒ đợt 2 bản đồ / lưu trú chỉ nếu còn ≥ 2 tuần trước 25/12.
- **Rủi ro đang bị bỏ quên [Thấy + Suy]:**
  1. **Deploy chưa bắt đầu**, mà "đóng code = đã chạy trên AWS". Spec Phase 9 review v10 M-1 ghi các việc bắt buộc trước deploy: giới hạn lượt, kiểm `Host`, xem lại điều khoản Serper, lưu phiên. Endpoint công khai gọi OpenAI + Serper mà không giới hạn lượt ⇒ có thể bị đốt tiền khi đưa link cho hội đồng.
  2. **Quyển báo cáo đồ án + slide** không có trong lộ trình (handoff / Project_Status không nhắc). Viết cần nhiều tuần, cạnh tranh giờ với code tháng 12 ⇒ nên có mốc riêng (vd bắt đầu viết song song từ giữa tháng 11; `bao_cao_he_thong/` là nguồn).
  3. **Phương án dự phòng lúc demo** (mạng / provider lỗi khi bảo vệ): video quay sẵn + chạy cục bộ trên máy User.
  4. **Số đo cuối để trình bày:** cần một lượt đo chốt (Golden + an toàn + độ trễ) trên **bản deploy**, không chỉ trên máy User.
