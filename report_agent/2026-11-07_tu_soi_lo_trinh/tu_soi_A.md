# Tự soi over-engineering + lộ trình — A (12:34 07/11/2026, `date`)

Thước: lợi đo được · phần đó sống bao lâu · lỗi đã quan sát chưa · có ai dùng. **[Đếm]** = A đếm bằng lệnh hôm nay.

## (1) Tốn mà lợi ít

1. **Tài liệu mở phiên quá nặng cho A** [Đếm]: 6 file A đọc đủ mỗi phiên ≈ 170 KB (START_SESSION, Session_Prompt, WORKFLOW, Project_Status, CURRENT_HANDOFF, STATUS_A). Project_Status §5 có 73 dòng quyết định (nhiều dòng đã bị thay); STATUS_A giữ 10 phiên cũ. Sổ cải tiến còn 28 mục `đang thử`.
2. **Luật có mã sự cố + chuyện dài nằm giữa câu luật** (Session_Prompt §5 câu kín, WORKFLOW §6 giờ `date`, §9.2): đọc khó, luật §7 đã nói "luật mới không kèm mã" nhưng luật cũ chưa gỡ.
3. **A làm trung gian quá nhiều câu nhỏ cho User** (bài học 02/11, 05/11 lặp lại): hôm nay Q-U3 hỏi bằng chi tiết kỹ thuật ⇒ User không hiểu, phải giải thích lại từ đầu.
4. **Đồ đo dựng trước khi tính năng chắc sống** (đồng ý C (1)): sửa lịch ~1.000 dòng, 0 lượt đo.
5. **Cờ tắt kết quả âm** (đồng ý C, E): `emergency_rule`, `today_line`, `nho_cau_tra_loi` + code `lich_trinh` câu tự do; 20 nhánh (local + origin, gộp tên) [Đếm], 9 đã merge chờ xoá.

## (2) Bỏ / làm nhẹ (đề xuất — phần governance chờ User duyệt khi dậy)

1. **Project_Status §5:** chỉ giữ quyết định **đang hiệu lực và chưa bị thay** (ước ~20 dòng); phần còn lại ⇒ `archive/`. STATUS_A chỉ giữ phiên gần nhất (cũ ⇒ archive). ⇒ giảm đọc mở phiên ~30–40 %.
2. **Gỡ mã sự cố khỏi luật cũ khi đụng tới** (đã là luật §7) — làm một lượt cho Session_Prompt §5 + WORKFLOW §6 / §9 (không đổi nghĩa; B / C kiểm).
3. **Sổ cải tiến:** xét 28 mục `đang thử` một lần — mục nào ≥ 1 tuần không bị chạm / không bắt lỗi ⇒ gỡ hoặc `đang dùng`.
4. **Hỏi User bằng lời của sản phẩm** (người dùng thấy gì), không bằng tên cờ / mã; trước câu kỹ thuật thì nói "đang ở đâu, vì sao hỏi".
5. Đồng ý C (2).1–3, E (2): đóng hồ sơ sửa lịch + câu tự do tới sau bảo vệ; gỡ cờ âm ở B7; chốt một bảng điểm.

## (3) Giữ vì đã bắt lỗi thật

- Review chéo (hôm nay: E review spec bắt Q-F chưa đo được; B tự tìm ra nguyên nhân từ chối bằng đếm 0 USD trước khi tốn thêm).
- Rào bằng máy: hook pre-commit / pre-push, `grep_kb.sh`, build record, hook giờ ước (bắt A nhiều lần).
- "Tiêu chí ghi trước" + "dừng khi trượt, không thử thêm cách" (B dừng D3 đúng lúc hôm nay).
- Bộ an toàn 32 câu; Q1 giống byte.

## (4) Nhìn rộng tới đóng code 25–30/12

- **Đồng ý C + E: deploy lát mỏng sớm** (sau S2, giữa tháng 11) — rủi ro lớn nhất, chưa thử lần nào. E đang chuẩn bị (0 USD); deploy thật / tiền tháng chờ User.
- **Quyển báo cáo + slide** chưa có mốc (E (4).2) — đề xuất User: bắt đầu dàn ý giữa tháng 11; `bao_cao_he_thong/` + bảng "đo gì · thước · kết quả · phương án bỏ" (C) là nguồn.
- **Giọng nói:** C "cắt nếu chưa có 40 câu trước ~20/11", E "cắt khỏi đồ án / bản nhẹ 10 câu" ⇒ A đề xuất User chọn một lần (không A tự cắt — phạm vi Phase đã duyệt).
- **Đợt 2:** chỉ P1 (đồng ý C); P3 dữ liệu "chưa kiểm" dễ bị hỏi vặn.
- Thứ tự A đề xuất: cổng đợt 1 ⇒ deploy lát mỏng ⇒ B7 gọn (gỡ cờ âm, dự phòng demo, kịch bản 5 phút) ⇒ đợt 2 P1 nếu còn ≥ 2 tuần ⇒ đo chốt trên bản deploy ⇒ đóng code.
