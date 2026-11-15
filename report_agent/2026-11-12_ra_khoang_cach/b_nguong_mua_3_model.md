# Ngưỡng mưa cho lịch + so 3 model Codex — B · 10:21 15/11/2026 · 0 USD API

A giao (User 15/11): tra công khai về ngưỡng "ngày mưa", đồng thời so 3 model Codex trên cùng một đề. Yêu cầu: `data/nguong_mua_2026-11-15/yeu_cau.md`
(4 câu: phân loại mưa VN / WMO · nghĩa 2 biến Open-Meteo · ngưỡng thực tế để đổi hoạt động · độ đúng dự báo 1–7 ngày). Kết quả thô:
`data/tra_cuu_cli/2026-11-15_mua-{sol,terra,luna}/`; chấm mù: `data/nguong_mua_2026-11-15/cham/ket_qua_cham.md` (khoá tên `khoa_model.json`).

## (a) Ngưỡng đề xuất — kèm nguồn

**Sự thật đã kiểm** (agent con mở trang bằng WebFetch, ba bản cùng nói, khớp nguồn):
1. **Việt Nam — QCVN 84:2024/BTNMT** (Thông tư 46/2024/TT-BTNMT, 30/12/2024, hiệu lực 30/6/2025; Phụ lục B), lượng 24 giờ: không đáng kể ≤ 0,6 mm ·
   mưa nhỏ 0,6–6 · **"Mưa" 6–16** · mưa vừa 16–50 · mưa to 50–100 · rất to > 100. Nguồn: Công báo
   <https://congbao.chinhphu.vn/tai-ve-van-ban-so-46-2024-tt-btnmt-44116-54768?format=pdf>; cùng văn bản có bản đăng trên cổng thông tin tỉnh / thành phố Huế (A mở bản đó, Phụ lục B khớp).
   ⇒ 5 mm / ngày vẫn là **mưa nhỏ**; mốc chính thức gần nhất là 6 mm (bắt đầu cấp "Mưa").
2. **Open-Meteo** (<https://open-meteo.com/en/docs>, mã `VariableDaily.swift`): xác suất theo giờ = xác suất có **> 0,1 mm trong giờ đó** (ensemble);
   `precipitation_probability_max` = **giờ có xác suất cao nhất trong ngày** — không phải "xác suất mưa ≥ X mm trong ngày". `precipitation_sum` = tổng
   mưa + mưa rào + tuyết theo ngày của `timezone` (code mình đặt `Asia/Ho_Chi_Minh` — đúng, `backend/llm/thoi_tiet.py:166`).
   ⇒ Luật hiện hành "≥ 60 %" thực chất là "có một giờ ≥ 60 % khả năng mưa lấm tấm" — giải thích vì sao ở Huế chạm 222 / 365 ngày (C, `c_dem_mua.md`).
3. **Ngưỡng thực tế:** không có chuẩn chung "bao nhiêu % / mm thì đổi lịch"; hướng dẫn sự kiện (Oxford, Boroondara, NWS) bảo tự đặt ngưỡng theo tác động.
   Gần nhất với việc mình cần: **Đài Thiên văn Hồng Kông** dự báo xác suất **tổng mưa ngày ≥ 10 mm** (mưa "đáng kể"), 5 bậc
   (<https://www.weather.gov.hk/en/wxinfo/currwx/fnd.htm>). Khảo sát Morss 2008 (1.520 người Mỹ): chỉ 19 % hiểu đúng "60 % khả năng mưa".
4. **Độ đúng dự báo miền Trung** (bài CRESS, hạn 24 giờ): ngưỡng 5 mm bắt được 44 % ngày mưa, 57 % lần báo là thừa; 10 mm: 40 % / 66 %.
   Nhiệt đới kém hơn ôn đới ở vài ngày đầu (Dias 2018). ⇒ dự báo lượng mưa ngày ở Huế **không chắc** ngay cả ngày mai; xếp trước 1–7 ngày còn kém hơn.

**Đề xuất (suy ra — cần nhóm bàn, User quyết vì đổi spec):**
- **Giữ phương án 3** (B, C, E đã đồng ý 14/11): xếp lại lịch (điểm trong nhà trước) khi ≥ 60 % **VÀ** lượng mưa ≥ ngưỡng mm; dòng "Nếu mưa" vẫn hiện từ ≥ 60 %.
  Nguồn ủng hộ việc ghép hai điều kiện: biến xác suất chỉ nói "có mưa lấm tấm trong một giờ", không nói mưa nhiều; cả 3 bản tra độc lập đều gợi ý ghép xác suất + mm.
- **Ngưỡng mm: 5 hay 6.** 6 mm có mốc chính thức (đầu cấp "Mưa" của QCVN 84) ⇒ dễ giải thích cho User / hội đồng; 5 mm là số C đã đếm
  (ERA5: báo 111 ngày, đúng 86 %, sót 23 %). Chênh nhỏ ⇒ đề xuất **6 mm**, C đếm lại bằng `dem_nguong.py` (0 USD) trước khi chốt; số khác xa 5 mm ⇒ giữ 5.
- **Không lên 10 mm:** sót ~1 / 2 ngày mưa thật (C: 63 / 124).
- Vì dự báo ≥ 5 mm ở miền Trung chỉ đúng khoảng một nửa, lịch nên nói "dự báo" chứ không hứa; dòng "Nếu mưa" (rẻ, không đổi lịch) giữ vai bắt phần sót.
- Ý phụ (ngoài phạm vi, ghi để bàn): chữ "khả năng mưa X %" giao diện thời tiết đang hiện (`thoi_tiet.py:199`) là giờ cao nhất ⇒ người dùng dễ hiểu nhầm là cả ngày.

## (b) So 3 model Codex (cùng đề, cùng script, chạy lần lượt, mức `medium`)

Chấm mù: agent con thấy 3 bản tên X / Y / Z, kiểm URL bằng WebFetch (khoá mở sau khi chấm: X = sol, Y = luna, Z = terra).

| Model | Thời gian | Trang mở được (mở lỗi) | Câu tìm | URL tự khai | Ý đúng / sai đã kiểm | URL khớp / mở thử | Đủ 4 câu | Nhận xét |
|---|---|---|---|---|---|---|---|---|
| `gpt-6.1-sol` | 293 s | 32 (8) | 52 | 2 | 12 / 0 (6 chưa kiểm được) | 7 / 10 | câu 4 thiếu miền Trung | rộng; có nguồn HKO ≥ 10 mm, gợi ý tính xác suất trong giờ tham quan |
| `gpt-6.1-terra` | **151 s** | 20 (9) | 24 | **0** | **13 / 0** | **9 / 11** | đủ cả 4 (câu 2 và 4 tốt nhất) | chính xác nhất; dẫn mã nguồn Open-Meteo; có số POD / FAR miền Trung đúng ngưỡng 5 / 10 mm |
| `gpt-6-luna` | 197 s | 15 (8) | 35 | 4 | 12 / **2** | 8 / 13 (2 không khớp) | đủ, câu 3 mỏng | rộng nhất ở câu 1; sai năm một bài báo và sai tên tác giả một bài |

- Cả 3 chạy được với tài khoản ChatGPT của User (0 báo lỗi model, 0 lệnh shell); log Codex không ghi tên model ⇒ tên lấy theo tham số gửi.
- Đọc: một đề, một lượt / model ⇒ **chưa đủ để chốt model mặc định** (2026-10-31 cũng thấy đổi thứ hạng theo đề). Lượt này `terra` vừa nhanh nhất vừa đúng nhất,
  `sol` mở nhiều trang nhất nhưng chậm gấp đôi. Gợi ý: thử `terra` làm mặc định cho câu tra kỹ thuật cụ thể ở 2–3 đề tiếp; giữ `sol` cho đề sâu nhiều tầng.
- Tiền: 0 USD API (lượt ChatGPT của User: 3 lượt); agent con: quota Claude. Thời gian cả việc: 10:01–10:21.

## (c) Bàn nhóm + khuyến nghị chốt (10:23 15/11/2026)

- **E:** đồng ý phương án 3, nghiêng 6 mm; điều kiện: so 5 ↔ 6 trên **cùng một thước "mưa thật"** (không đổi thước cùng lúc với ngưỡng); nói thẳng với User là ngưỡng mm
  chủ yếu **bớt báo thừa**, không làm lịch "đúng mưa"; không thêm luật "chỉ xếp lại khi còn ≤ 3 ngày" (chưa có số cần).
- **C** đếm lại 0 USD (`data/dem_mua_2026-11-14/so_mua_that_qcvn.py`), sửa thiên vị của bảng cũ (thước ERA5 ≥ 5 mm trùng ngưỡng thử), thước theo mốc QCVN:

| Thước "mưa thật" (ERA5) | Luật | Báo | Đúng | Sót |
|---|---|---|---|---|
| ≥ 6 mm (cấp "Mưa", 114 ngày) | hiện hành ≥ 60 % | 218 | 51 % | — |
| | ≥ 60 % và ≥ 5 mm | 111 | 80 % | 22 % |
| | ≥ 60 % và ≥ 6 mm | 97 | 85 % | 28 % |
| ≥ 16 mm (mưa vừa, 56 ngày) | ≥ 5 mm / ≥ 6 mm | — | báo thừa 59 / 45 | 4 / 56 cả hai |

  Chuyến 2–5 ngày có ≥ 1 ngày xếp lại: hiện hành 80,4 % · 5 mm 52,8 % · **6 mm 50,0 %** · 10 mm 38,3 %. Ngày mưa thật 6 mm bỏ sót vẫn có dòng "Nếu mưa": 30 / 32 (≥ 6 mm), 4 / 4 (≥ 16 mm).
- **Khuyến nghị (B, C, E đồng ý):** phương án 3 với **6 mm** — xếp lại lịch khi `precipitation_probability_max` ≥ 60 % **và** `precipitation_sum` ≥ 6 mm (từ cấp "Mưa" QCVN 84);
  dòng "Nếu mưa" giữ từ ≥ 60 %. Với mưa vừa trở lên 6 mm không sót thêm ngày nào mà ít báo thừa hơn 5 mm. Đổi spec đã duyệt ⇒ **User quyết**. Code nếu duyệt: dict `mua` đưa vào `xep_v2`
  (`backend/llm/len_ke_hoach.py:88`) chỉ giữ ngày đạt cả hai điều kiện; dòng "Nếu mưa" (`:57`) không chạm; 0 USD.
- **Việc riêng, nhỏ:** nhãn "khả năng mưa X %" (`thoi_tiet.py:199`) ⇒ ghi rõ là lúc cao nhất trong ngày.
- **Giới hạn:** dự báo lịch sử là bản tầm ngắn nhất, ERA5 ô ~25 km ⇒ số thật ở hạn 1–7 ngày kém hơn bảng.
