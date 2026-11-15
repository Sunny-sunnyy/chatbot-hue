# Plan (mức nhẹ) — Sửa lịch bằng lời: đổi ngày đi (bậc 2) · C · 16:02 15/11/2026

User chọn 15:14 15/11/2026 "làm cả hai, từng bậc". Bậc 1 (hạng chỗ ở) đã đạt, chờ merge — bậc 2 code trên `main` **sau khi** bậc 1 vào. Chưa code.

**Căn cứ để review:** `report_agent/2026-11-12_ra_khoang_cach/c_dem_sua_lich_truong.md` (số đếm) · `c_sua_hang_o_implementation.md` (bài học vòng chỉnh bậc 1) · `backend/llm/sua_lich_v2.py` (`ap`, `_xep`, `loc_hanh_dong`) · `backend/llm/do_so.py` (`do_ngay_di`) · `backend/llm/len_ke_hoach.py` (`du_bao_lich`, `hieu_va_ap`).

## Lỗi đã đếm
- Câu xin đổi ngày đi sau khi có lịch: lần hiểu ý trả rỗng **4 / 5** ⇒ lịch không đổi, không báo gì; **1 / 5 bị hiểu thành đổi SỐ ngày** (đã rào 15/11 ⇒ nay ra "Chưa làm: đổi số ngày"). Câu tự đặt; không có số nhu cầu thật.
- Ngày đi quyết định ba thứ trong lịch: điểm đóng cửa theo thứ, hoạt động chỉ có một số thứ, dự báo mưa 7 ngày (xếp lại khi ≥ 60 % và ≥ 6 mm) ⇒ đổi ngày **có thể đổi khung** — khác bậc 1.

## Thiết kế (model chỉ nói "người dùng muốn đổi ngày đi"; ngày do code đọc từ chữ người dùng)
1. **Hành động mới `doi_ngay_di`, không có trường nào.** Model không viết ngày ⇒ không có đường nào cho một ngày người dùng không gõ (rào có sẵn trong thiết kế, mạnh hơn rào số ngày).
2. **Code tính ngày** từ câu người dùng (hàm thuần mới cạnh `do_so.do_ngay_di`, dùng lại các mẫu dò sẵn có, bỏ giới hạn 0–6 ngày):
   - **Làm:** `dd/mm` · `dd/mm/yyyy` · "ngày d tháng m" · mai · ngày kia / mốt · thứ X / chủ nhật (lần tới gần nhất) · cuối tuần (này) · thêm chữ "tuần sau / tuần tới" ⇒ +7 ngày. `dd/mm` không năm ⇒ lần tới gần nhất.
   - **Không đổi, có dòng lý do:** không thấy ngày / thấy ≥ 2 ngày khác nhau ("bạn nói một ngày cụ thể, vd 20/12") · ngày đã qua · quá 180 ngày (giới hạn của biểu mẫu) · trùng ngày đang dùng · ngày không có thật (30/2).
   - **Chưa làm ở bậc này (cùng dòng "nói một ngày cụ thể"):** tương đối theo ngày đang dùng ("dời 2 hôm", "lùi một tuần", "sớm hơn 1 ngày") · ngày âm lịch / "dịp Tết" · bỏ ngày đi.
3. **Code áp:** lấy dự báo cho ngày mới (đúng hàm `du_bao_lich`, cache 30 phút; lỗi / ngoài 7 ngày ⇒ như không có dự báo) ⇒ thử **giữ nguyên mọi điểm ở chỗ cũ** với ngày mới; đúng luật ⇒ khung không đổi; phạm luật (đóng cửa theo thứ, mưa) ⇒ xếp lại, điểm người dùng đã bỏ không quay lại. Khung sau phải qua `kiem_khung_v2`, không qua ⇒ giữ lịch cũ + lý do.
4. **Nói rõ với người dùng (code viết):** "Đã đổi ngày đi: 20/11 → 27/11 (thứ Sáu)." + một trong: "Các điểm giữ nguyên chỗ." / "Lịch xếp lại theo ngày mới: k điểm đổi ngày hoặc buổi, m điểm thay." (k, m do code đếm) + khi ngày mới ngoài 7 ngày dự báo: "Ngày này chưa có dự báo thời tiết nên lịch chưa xét mưa."
5. Không cờ mới; "Mình hiểu" + dòng dự báo dựng lại bằng đường sẵn có. Lời dặn: 1 gạch hành động ngắn + 1 câu cách nói **đặt ở khối "cách nói thường gặp"** (bài học bậc 1: không chèn chữ dài vào danh sách hành động), không sửa phần số ngày.

## Tiêu chí ghi trước (lượt có phí qua `/api/chat/stream`, cuộc đã có lịch có ngày đi; ngày trong câu sinh theo hôm chạy để nhãn không cũ)
| Mã | Bộ | Tiêu chí | Ngưỡng | Tiền |
|---|---|---|---|---|
| Luôn-a | test hàm tính ngày, ≥ 30 ca tự đặt (mỗi dạng, quá khứ, quá 180 ngày, 2 ngày, 30/2, "ngày 2" của chuyến, "thứ ba" ↔ "ngày thứ ba", "3 ngày") | đúng ngày / đúng mã lý do | 100 % | 0 |
| Luôn-b | test `ap` trên 3.840 khung × 3 ngày mới (kèm dữ liệu mưa nhỏ tự đặt) | khung sau 0 lỗi luật · điểm đã bỏ không quay lại · giữ được thì khung y nguyên · số k, m trong câu báo = số đếm lại độc lập | 0 lệch | 0 |
| Q1 | 25 hằng lời dặn so với `main` | chỉ lời dặn hiểu ý khác | đạt | 0 |
| **D1 (quyết)** | 12 câu nêu một ngày rõ (C viết trước; đủ các dạng "Làm") × 2 lượt | ngày đi lưu đúng nhãn ở cả 2 lượt | ≥ 10 / 12 | ≈ 0,06 (D1–D3) |
| **D1-sai (sàn)** | cùng bộ | đổi sang ngày KHÁC nhãn | 0 / 24 | |
| **D2 (quyết)** | 6 câu thuộc nhóm "không đổi / chưa làm" × 2 | có đổi ngày đi | 0 / 12 | |
| D2-nói | cùng bộ | có dòng lý do ở cả 2 lượt | ≥ 4 / 6 | |
| **D3 (sàn)** | 8 câu có chữ chỉ ngày nhưng KHÔNG xin đổi ngày đi (hỏi thông tin theo ngày; sửa "ngày 2…"; thêm / bớt ngày) × 2 | thành đổi ngày đi | 0 / 16 | |
| **Số ngày (sàn)** | mọi câu D1 + D2 | bị đổi SỐ ngày | 0 | |
| **Q3 (hồi quy, chạy NGAY sau D1–D3)** | 10 chuỗi đã thấy, pass^2 | đạt · riêng chuỗi "chỉ đi một buổi" (hồi quy bậc 1) | ≥ 8 / 10 · 2 / 2 | ≈ 0,05 |
| **H1 bậc 1 (hồi quy)** | 12 câu đổi hạng × 1 lượt | đúng mức · sai mức | ≥ 10 / 12 · 0 | ≈ 0,015 |
| **Q5 · Q5b (sàn)** | an toàn 32 × 2 · 8 câu trộn khẩn cấp × 2 | thành lượt sửa | 0 / 64 · 0 / 16 | ≈ 0,025 |
| D4 | 8 câu lạ A viết sau khi chốt lời dặn, 1 lượt | đúng ngày · sai ngày | ≥ 6 / 8 · 0 | ≈ 0,015 |
| Tốc độ (theo dõi) | lượt đổi ngày trong D1 | tới lúc khung hiện, p50 | ≤ 3 s | — |

- **Đếm câu chạm:** lời dặn hiểu ý đổi ⇒ mọi lượt trong cuộc có lịch chạm (Q3 / H1 / Q5 / Q5b chạy); Golden 176 + an toàn ngoài cuộc có lịch không chạm ⇒ không chạy.
- **Nhãn không chấm khung ở lượt có phí** (dự báo thật đổi theo giờ chạy): lượt thật chấm ngày đi + câu báo; đúng sai của khung do test Luôn-b giữ.
- **Thứ tự:** test 0 USD ⇒ D1–D3 ⇒ **Q3** ⇒ (trượt ⇒ MỘT vòng chỉnh lời dặn, chạy lại D1–D3 + Q3) ⇒ chốt ⇒ H1, Q5, Q5b, D4 một lần. Không đo thêm sau khi thấy số; cần vòng chỉnh hai ⇒ dừng, báo A.
- **Bộ kín: không** (một hành động không tham số, ≤ 1 vòng chỉnh; D4 kiểm quá khớp).
- **Tiền:** ≈ 0,165 USD không vòng chỉnh; có vòng chỉnh ≈ 0,25 ⇒ **trần 0,25**, thấy sắp vượt ⇒ hỏi A trước. **Dừng:** phạm sàn D1-sai / D3 / số ngày / Q5 / Q5b, Q3 dưới ngưỡng, hoặc chuỗi hồi quy bậc 1 < 2 / 2 sau vòng chỉnh ⇒ không merge.
- **Giao diện:** dùng khối "Đã đổi / Không đổi được" sẵn có ⇒ không Playwright. **Review:** một review cả nhánh. Tài liệu: `bai_hoc/25` + sổ 07 khi đạt.

## Bảng rà AI FDE
| Mục | Thiết kế | Khớp / lệch |
|---|---|---|
| Có cần model? | Chỉ để nhận ra ý "đổi ngày đi" giữa các câu có chữ ngày. Đọc ngày, kiểm hạn, lấy dự báo, xếp lại, đếm thay đổi, câu báo: code | khớp |
| Tham số công cụ | Không tham số ⇒ model không thể đưa ngày người dùng không gõ | khớp |
| Phép tính ngày ⇒ code | hàm thuần, test bảng ca; nhiều ngày khác nhau ⇒ không đoán | khớp |
| Từ chối thành kết quả | mỗi trường hợp không đổi một câu lý do cố định; dự báo lỗi ⇒ vẫn đổi ngày, nói rõ chưa xét mưa | khớp |
| Làm sai mà báo đã làm | sàn D1-sai 0 / 24, sàn số ngày 0; khung đổi thì câu báo nêu số điểm đổi (không im lặng xếp lại) | khớp |
| Trí nhớ | `ngay_di` + `mua` trong trạng thái đã lưu của cuộc (trường có sẵn) | khớp |
| Đường ra mới | Không: Open-Meteo đã dùng ở lượt biểu mẫu, không gửi chữ người dùng | khớp |
| Chữ người dùng là dữ liệu | Q5 / Q5b / D3 giữ câu an toàn, khẩn cấp, câu hỏi theo ngày không lạc sang đổi ngày | khớp |
