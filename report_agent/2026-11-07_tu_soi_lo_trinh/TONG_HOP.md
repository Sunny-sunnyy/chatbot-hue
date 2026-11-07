# Tổng hợp tự soi + lộ trình (A, 12:50 07/11/2026)

Đầu vào: `tu_soi_A.md`, `tu_soi_B.md`, `tu_soi_C.md`, `tu_soi_E.md` (bốn session viết độc lập, B / C / E đọc được bản của nhau sau khi viết), `e_dep_chuan_bi_deploy.md` + review nháp deploy (B, `tu_soi_B.md` §5). Việc gốc: User 07/11 trước khi nghỉ — "xem xét lại tối ưu và các vấn đề over-engineer, A / B / C / E thảo luận, đánh giá, đề xuất lẫn nhau".

## 1. Bốn session cùng thấy (đồng thuận)

| # | Điều | Ai nêu | Bằng chứng chính |
|---|---|---|---|
| 1 | **Deploy chưa thử lần nào = rủi ro lớn nhất**; "đóng code = chạy trên AWS" | C, E, A, B | `docker-compose.yml` chỉ có Qdrant; app 1,5 GB + Qdrant 0,38 GB RAM [Chạy, E]; review nháp tìm 3 major chưa cần build (B) |
| 2 | **Dựng đồ đo / rào trước khi biết tính năng sống** là chỗ tốn nhất | C, E, B, A | sửa lịch ~1.000 dòng, 0 lượt đo (C); B viết 20 test + 3 lần Q1 trước lượt thật đầu tiên ⇒ lỗi từ chối lộ trễ ~40 phút (B) |
| 3 | **Cờ tắt kết quả âm** nên gỡ ở B7 (`emergency_rule`, `today_line`, `nho_cau_tra_loi`) | C, E, A, B | mỗi cờ = nhánh code + test "giống byte" phải giữ |
| 4 | **Lịch trình câu tự do + sửa lịch** ⇒ đóng tới sau bảo vệ, chỉ biểu mẫu | E, C (sửa lịch), A | kín v2 3 / 5; bảng điểm 6 bản, chỉ v3 từng chạy |
| 5 | **Giọng nói** — cắt hoặc làm nhẹ | E (cắt), C (cắt nếu chưa có 40 câu trước ~20/11), B, A (User chọn) | 0 số đo sau 2 ngày; +300 MB RAM khi deploy |
| 6 | **Đợt 2 chỉ P1** (bản đồ từ toạ độ kho), cắt dữ liệu "chưa kiểm" | C, A | dữ liệu OSM / dữ liệu mở thiếu kiểm dễ bị hỏi vặn |
| 7 | **Quyển báo cáo + slide chưa có mốc** | E, A | không có trong handoff / Project_Status |

## 2. Giữ (đã bắt lỗi thật)
Review chéo · hook pre-commit / pre-push + `grep_kb.sh` · tiêu chí ghi trước + "dừng khi trượt" · Q1 giống byte + test mỗi loại lượt · `kiem_cuoi` do code · bộ an toàn 32 câu · "tái tạo trước khi sửa" · đo 0 USD trước khi tốn thêm.

## 3. Bất đồng
- C đề xuất cập nhật báo cáo khâu **một lần lúc đóng đợt**; B phản biện: User 31/10 dặn báo cáo luôn mới nhất ⇒ **giữ**, chỉ làm nhẹ (sửa Tóm tắt + 1 dòng). A theo B (đổi luật User đặt ⇒ phải hỏi User; chưa có lý do hỏi).

## 4. Đề xuất cho User (A sẽ hỏi mỗi lần một câu khi User dậy)

1. **Lộ trình tới đóng code** (A đề xuất): cổng đợt 1 ⇒ **deploy lát mỏng ngay sau** (Lightsail 4 GB ≈ 24 USD / tháng, User tạo tài khoản + khoá OpenAI riêng có hạn mức; ⚠ gói miễn phí AWS tự đóng tài khoản sau 6 tháng / hết tín dụng — A WebFetch kiểm) ⇒ B7 gọn (gỡ cờ âm, dự phòng demo, kịch bản 5 phút) ⇒ đợt 2 P1 nếu còn ≥ 2 tuần ⇒ đo chốt trên bản deploy.
2. **Giọng nói:** (a) cắt khỏi đồ án (hướng phát triển) · (b) bản nhẹ 10 câu, chỉ máy User · (c) giữ plan 40 câu, mốc cắt 20/11.
3. **Đóng hồ sơ lịch trình câu tự do + sửa lịch** tới sau bảo vệ (tag nhánh, gỡ khỏi việc đang mở).
4. **Mốc quyển báo cáo + slide** (đề xuất bắt đầu dàn ý giữa 11; nguồn `bao_cao_he_thong/` + bảng "đo gì · thước · kết quả · phương án bỏ").
5. Luật nhỏ cho vòng cải tiến: "đường mới có gọi model ⇒ 1 lượt thật ≤ 0,001 USD ngay khi chạy được, trước bộ test" (B) + "đồ đo dựng sau khi spec duyệt **và** code chạy được một bản" (C).

## 5. A tự làm được (không đổi luật / phạm vi)
- Giảm tài liệu đọc mở phiên: Project_Status §5 chỉ giữ quyết định đang hiệu lực (cũ ⇒ archive); STATUS_* chỉ giữ phiên gần nhất. Làm lúc kết phiên.
- Đang làm ngay (0 USD, không chờ User): B thử `docker build` cục bộ (sửa M1–M3); C đo V4 lượt biểu mẫu; E review giao diện S2.
