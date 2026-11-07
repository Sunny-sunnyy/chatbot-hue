# Tự soi over-engineering + lộ trình — C (12:31 07/11/2026, `date`)

Thước: lợi đo được · phần đó sống bao lâu · lỗi đã quan sát chưa · có ai dùng. [Đếm] = số C đếm bằng lệnh hôm nay.

## (1) Tốn mà lợi ít

1. **Sửa lịch nhiều lượt** (ý #8): code nhánh `p9-sua-lich` (36 file đổi so với `main`), harness + công cụ bộ đo ~1.000 dòng [Đếm], bộ 10 + 5 kín + Q4, 3 vòng review harness, 2 lần rebase (C207, C208) — **chưa chạy một lượt đo nào**, nay hoãn và có thể đổi cách ("điền lại biểu mẫu"). Đây là ca rõ nhất: dựng đồ đo trước khi chắc tính năng còn sống.
2. **Lịch trình câu tự do (B5)**: nhiều vòng chỉnh lời dặn + 2 bộ kín, kín v2 trượt (3 / 5) ⇒ cờ tắt; User chọn biểu mẫu. Phần code tất định (xếp, kiểm khung, kiểm cuối) dùng lại được; phần chỉnh lời dặn qua nhiều vòng thì không.
3. **Tài liệu > code**: 207 / 300 commit gần nhất là `docs:` [Đếm]; 87 file `report_agent/` từ 01/11 [Đếm]; governance + skill 3.365 dòng [Đếm]. Mỗi việc nhỏ kéo theo report + STATUS + handoff + báo cáo khâu.
4. **Cờ tắt có kết quả âm vẫn nằm trong code**: `emergency_rule` (bắt 0 / 8), `today_line` (không giảm từ chối nhầm), `nho_cau_tra_loi` — mỗi cờ thêm nhánh + test "cờ tắt giống byte" phải giữ mãi.
5. **Việc của chính C hôm nay**: C-tl (thời lượng web) chỉ có ích khi mở lại "đi dày" — đợt 1 đã ẩn ⇒ lợi hiện tại ≈ 0 (12 / 120 tổ hợp đổi, +0,05 điểm / ngày).

## (2) Bỏ / làm nhẹ

1. **Đóng hồ sơ sửa lịch**: tag nhánh (`hoso/p9-sua-lich`), ghi 3 dòng vào báo cáo khâu, gỡ khỏi "việc đang mở" và STATUS. Mở lại khi biểu mẫu có sửa lịch; khi đó cách "điền lại biểu mẫu" có lẽ không cần harness riêng.
2. **Luật "dựng đồ đo sau khi tính năng chắc vào"**: harness / bộ kín chỉ viết khi spec đã duyệt **và** code xong một bản chạy được (S3 hôm nay làm đúng: nháp nhỏ, khớp lại sau S1).
3. **Gỡ code 3 cờ âm** (`emergency_rule`, `today_line`, `nho_cau_tra_loi`) trong B7 — giữ kết quả âm 1–3 dòng ở báo cáo khâu + tag hồ sơ. Ít nhánh hơn ⇒ deploy / review dễ hơn.
4. **Report một việc ≤ 1 trang** (tiêu chí · kết quả · bằng chứng · giới hạn); báo cáo khâu cho User cập nhật **một lần lúc đóng đợt**, không mỗi việc nhỏ (luật "cùng đợt" giữ cho thay đổi người dùng thấy).
5. STATUS ≤ 15 dòng, chỉ "đang làm / chờ ai / lệnh phiên sau"; lịch sử để git.

## (3) Giữ vì đã bắt lỗi thật

- Hook pre-commit quét trùng Golden / kho / kín (đã chặn lộ câu nhiều lần, 25–27/10) + `scripts/grep_kb.sh` (grep thẳng từng lọt câu kín).
- Q1 "cờ tắt giống byte" + test mỗi loại lượt (4c): bắt lượt ghép thiếu luật ở B4 trước khi tốn thêm lượt có phí.
- `kiem_cuoi` / kiểm khung do code (D8): luật tiền / giờ / điểm bằng code, không bằng lời dặn (B4 "không cộng tổng" âm).
- "Tái tạo trước khi sửa" (C210): tránh một sửa code cho lỗi chưa tái tạo được.
- Ca phá trong mỗi harness: harness sửa lịch từng không bắt "lượt sau lịch hỏng" (E review M-1) — ca phá rẻ, giữ.
- Bộ an toàn 32 câu báo đủ 4 số.

## (4) Nhìn rộng tới đóng code (25–30/12) + bảo vệ (04–10/01/2027)

**Rủi ro lớn nhất đang bị bỏ quên: deploy chưa thử lần nào.** `docker-compose.yml` chỉ có Qdrant [Đếm]; chưa có image app, chưa thử trên máy AWS. Ẩn số: RAM (e5 + Qdrant 8.435 điểm + uvicorn), latency CPU nhỏ, `frontend/dist`, khoá OpenAI / Serper trên server, xoay log, giới hạn tần suất, `/api/kham_pha/bai` công khai toàn văn kho.
**Đề xuất thứ tự:**
1. Cổng đợt 1 (S1–S5) — cái người xem thấy đầu tiên.
2. **Deploy lát mỏng ngay sau S2 (giữa 11)**, không đợi Phase 12: một máy nhỏ, compose app + Qdrant, một lần thật ⇒ đo RAM / p95 / tiền tháng. Còn ~7 tuần để sửa nếu vỡ.
3. B7 đóng gói gọn: gỡ cờ âm, dự phòng demo mất mạng (video / bản chạy local), kịch bản demo 5 phút.
4. Phase 10 giọng nói: chỉ làm nếu User thu 40 câu trước ~20/11; quá hạn ⇒ cắt khỏi đợt bảo vệ (nêu là hướng phát triển).
5. Đợt 2: chỉ P1 (bản đồ Leaflet từ toạ độ kho đã có); cắt P3 (lưu trú / ăn uống OSM "chưa kiểm") — dữ liệu chưa kiểm dễ bị hỏi vặn khi bảo vệ.
6. Hỏi bằng ảnh: User quyết bật / bỏ một lần; xoá collection thử `hue_anh_siglip2`.
**Cho bài trình bày:** một bảng "đo gì · thước · kết quả · phương án bỏ" từ hồ sơ có sẵn mạnh hơn thêm tính năng.
