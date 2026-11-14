# Plan (mức nhẹ) — Mức suy luận "low" cho lần viết mục web · B · 16:01 14/11/2026

**Vì sao** (đếm 0 USD, `report_agent/2026-11-12_ra_khoang_cach/b_dem_toi_uu_tro_ly.md`): lượt có mục web cả câu p50 **20,9 s**. Lần viết mục web chiếm p50 **4,94 s** (~214 token suy luận, agent `hue_web_section` không đặt mức suy luận ⇒ mặc định). Lợi nhắm tới là **cả câu**, không phải chữ đầu (chữ đầu là câu từ chối kho, có trước lần viết này).

**Đổi một thứ:** cờ `assistant.web_suy_luan_thap` (TẮT). Bật ⇒ `cong_web` gọi bản clone của `web_agent` với `reasoning=Reasoning(effort="low")` (như lượt biểu mẫu, lịch, hiểu ý sửa). Lời dặn, tin nhắn, kiểm cuối bằng code, Serper đều **không đổi**. Cờ tắt ⇒ chuỗi gửi model giống byte (test).

**Đo theo cặp, đúng chỗ đổi** (W70):
- **Câu chạm** = câu đi qua cổng web: hỏi kèm 10 + câu ngoài kho của Golden (18) + câu an toàn có tra web (đếm từ lượt chạy, dự kiến ~4–6).
- **Bước 1 — lấy đầu vào thật:** mỗi câu chạy một lượt thật (cờ tắt), lưu đúng tin nhắn gửi lần viết mục web (câu + sổ kết quả Serper) vào `data/web_suy_luan_2026-11-14/`.
- **Bước 2 — so trên cùng đầu vào:** mỗi đầu vào gọi **cả hai** bản (mặc định ↔ low), mỗi bản 2 lần, xen kẽ thứ tự. Chạy đúng kiểm cuối bằng code của `cong_web` (mã [w n], link, tiền ⊂ đoạn trích, lưu trú 0 tiền, thời gian thực, thiên tai).
- Trước lượt có phí: một lượt khô 0 USD trên đầu vào đã lưu (đọc file, dựng tin nhắn, so byte với lượt thật).

**Tiêu chí ghi trước** (bản low so với bản mặc định, cùng đầu vào):

| Mã | Tiêu chí | Sàn |
|---|---|---|
| K | Kiểm cuối bằng code: tỉ lệ ra `co_muc` | không thấp hơn mặc định quá 1 đầu vào |
| S | Số / tiền không có trong đoạn trích lọt qua | 0 |
| T | ms lần viết mục web p50 | giảm ≥ 1,5 s |
| D | Đọc tay 8 cặp ngẫu nhiên (B + 1 agent con mù bên): bản low nói chắc hơn nguồn | 0 cặp |
| A | Câu an toàn có tra web: mục web không bỏ / đảo cảnh báo (đọc tay) | 0 |

- Đạt cả 5 ⇒ đề xuất A bật.
- Trượt ⇒ ghi số, cờ giữ tắt, không vòng chỉnh.

**Tiền ước:** bước 1 ~34 lượt × ~0,003 ≈ 0,10 · bước 2 ~34 × 4 lần gọi × ~0,0006 ≈ 0,08 ⇒ **≈ 0,2 USD**.

**Không làm:** đổi lời dặn web, đổi truy vấn Serper, đổi hạn 5 s.

**Không chạy lúc E dựng chỉ mục** (A dặn). Mỗi người tối đa 1 server tạm.

## Bảng AI FDE
| Mục | Thiết kế | Khớp / lệch |
|---|---|---|
| Có cần model? | Đã có model viết mục web; chỉ đổi mức suy luận | khớp |
| Phép tính / luật tiền ⇒ code | Kiểm cuối mục web vẫn do code, không đổi | khớp |
| Đường ra ngoài | Không đổi (Serper nhận đúng câu như cũ) | khớp |
| Nói chắc sai | Tiêu chí D + S | khớp |
| Đổi một thứ | Chỉ `reasoning.effort` của một agent | khớp |
