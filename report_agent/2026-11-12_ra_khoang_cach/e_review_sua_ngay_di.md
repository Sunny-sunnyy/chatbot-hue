# Review nhánh `p9-sua-ngay-di` (C) — E · 16:48 15/11/2026 (`date`) · 0 USD

Bản review: origin `40d97e5` (C báo sau đó gộp thêm `main` chỉ có tài liệu ⇒ `276e328`; E không đọc lại). Căn cứ: plan `docs/superpowers/plans/2026-11-15-sua-lich-ngay-di-plan.md`, diff `origin/main...origin/p9-sua-ngay-di` (4 file code +144 / −11, 1 file test mới, report), report của C. E không chạy lại lượt có phí; test rộng C đang chạy.

**Kết luận: `changes_requested`** — 0 blocker · **1 major** · 3 minor. M-1 là sửa regex + ca test (0 USD), không cần đo có phí lại nếu 12 câu D1 + 8 câu D4 vẫn đọc ra đúng ngày khi chạy hàm ngoại tuyến.

## Cổng tối thiểu
- Phạm vi đúng plan; `git diff --check` sạch. Hành động mới không có tham số ⇒ model không viết ngày (đúng nguyên tắc "phép tính ⇒ code").
- Tiêu chí ghi trước ↔ report: D1 12 / 12 (≥ 10), D1-sai 0 / 24, D2 0 / 12 + lý do 5 / 6 (≥ 4), D3 0 / 16, số ngày 0, Q3 8 / 10 (ngưỡng ghi trước đúng là ≥ 8) + 2 / 2, Q5 0 / 64, Q5b 0 / 16, D4 8 / 8 — report không đổi ngưỡng nào. Hai chuỗi Q3 trượt có giải thích; chuỗi do nhãn cũ lệch bảng điểm v9 là hệ quả việc của E chiều nay — E xác nhận điểm đó đúng là vừa vào bảng.

## Năm chỗ C nhờ soi
1. **`ngay_tu_cau` đọc SAI ngày — CÓ, xem M-1.**
2. **"Tuần sau" theo tuần lịch:** nhận như C làm (m-1).
3. **`ap` sau khi đổi ngày:** `luu` và `khung` được gán lại, `vt` tính lại đầu mỗi vòng ⇒ hành động sau trong cùng lượt dùng đúng lịch + dự báo của ngày mới; điểm đã bỏ (`loai`) không quay lại; lượt dừng ở thẻ chọn trả trước khi áp gì ⇒ ngày không đổi nửa chừng. Đọc code, không thấy lỗi.
4. **Hai mục thời tiết trong `trace.tools` ở lượt đổi ngày:** E grep nơi dùng — chỉ có danh sách tên công cụ của log, không có bộ đếm "đúng một lần" ⇒ không phá gì (lần hai lấy từ bộ nhớ đệm). m-3.
5. Test rộng: chờ số của C.

## Finding
**M-1 (major) — có chữ GIỐNG ngày mà không phải ngày ⇒ hàm trả một ngày cụ thể, lịch bị đổi sang ngày người dùng không nói.**
- Vị trí: `backend/llm/do_so.py` `ngay_tu_cau` (`_MAI`, `_THU_CN`, `_DMY`, `_D_THANG_M`).
- Bằng chứng: ca dò của E gọi thẳng hàm trên code nhánh, hôm nay giả là Chủ nhật 15/11/2026, 34 câu tự đặt (26 câu kỳ vọng thông thường đều đúng). **8 / 34 lệch — cả 8 đều là "phải trả chưa rõ" nhưng trả một ngày:**

| Loại | Câu có gì | Hàm trả |
|---|---|---|
| tên người / tên đường có chữ "Mai" (2 câu) | xin dời ngày, không nêu ngày | ngày mai |
| số thứ tự "điểm thứ hai", "điểm thứ 3" (2 câu) | xin đổi ngày + nhắc một điểm theo thứ tự | thứ Hai / thứ Ba tới |
| phân số / kiểu "24/7": "1/2 ngày", "3/4 nhóm", "24/7" (3 câu) | xin dời chuyến, không nêu ngày | 1/2, 3/4, 24/7 năm sau |
| "2 tháng 3 ngày nghỉ" (1 câu) | khoảng thời gian | 2/3 năm sau |

- Vì sao đáng sửa trước merge: hành động này chạy ngay khi vào `main` (cờ sửa lịch đang bật); sai ngày kéo theo xếp lại cả lịch theo thứ / mùa / dự báo. Giảm nhẹ: hàm chỉ chạy khi model đã nhận ra ý đổi ngày, và câu báo in ngày + thứ nên người dùng nhìn thấy — nhưng report đang viết "không thể đổi sang một ngày họ không nói" (m-2). Ngoài ra khi câu CÓ ngày thật kèm một chữ như trên ("đổi sang 20/12 và bỏ điểm thứ hai") hàm thấy hai ngày ⇒ "chưa rõ" — an toàn nhưng là từ chối nhầm một câu ghép rất tự nhiên (đổi ngày + bỏ điểm cùng lượt).
- Tiêu chí đóng: 8 câu trên (hoặc câu tương đương C tự đặt) trả mã "chưa rõ"; câu "đổi sang 20/12 và bỏ điểm thứ hai" trả 20/12; thêm vào `test_sua_ngay_di.py`; 12 câu D1 + 8 câu D4 chạy lại qua hàm (0 USD) vẫn ra đúng ngày như lượt đo. Gợi ý cách hẹp nhất (C tự quyết): (a) "thứ …" không tính khi ngay trước là "điểm / nơi / chỗ / lần / mục / người" (như đã làm với "ngày "); (b) "mai" không tính khi ngay trước là từ xưng hô hoặc "đường / phố / hoa / chợ", hoặc xét trên chữ gốc: chỉ "mai" viết thường / đứng đầu câu; (c) d/m không tính khi ngay sau là một đơn vị ("ngày", "giờ", "buổi", "tiếng", "nhóm", "phần", "chặng") hoặc đúng "24/7"; "d tháng m" không tính khi ngay sau là số + "ngày".
- Giới hạn còn lại sau khi sửa nên ghi vào report: bộ lọc theo danh sách từ không bao giờ đủ — ghi số ca dò đã thử.

**m-1 — "tuần sau" theo tuần lịch: nhận.** Nói vào Chủ nhật "thứ Bảy tuần sau" ra thứ Bảy cách 6 ngày là cách hiểu theo lịch (tuần mới bắt đầu thứ Hai); câu báo in cả ngày lẫn thứ. Không sửa; giữ dòng giới hạn trong report.

**m-2 — câu "Giải thích ngắn" của report nói quá:** "không thể đổi sang một ngày họ không nói" ⇒ sửa theo M-1 ("ngày lấy từ chữ người dùng gõ; chữ giống ngày có thể bị đọc nhầm — đã chặn các dạng …").

**m-3 — ghi chú:** lượt đổi ngày có hai mục thời tiết trong log công cụ (một lần trước khi áp, một lần lúc dựng lịch — lần hai từ bộ nhớ đệm); ai đếm "số lần gọi thời tiết" từ log cần biết.

## Bất biến (E đọc code, không chạy)
Lượt không có hành động đổi ngày: `ngay_moi` là None, `ap` đi đúng các nhánh cũ; `stream_sua` lấy ngày từ `kq["luu"]` — bằng ngày cũ khi không đổi. Phần lời dặn đổi (+1 hành động, +1 câu) đã được C đo trên Q3 / H1 / Q5 / Q5b.

## Kiểm phần sửa — 16:52 15/11/2026 (`date`), bản origin `0463bf2` (so `276e328`: 3 file — `do_so.py`, test, report)
**M-1 ĐÓNG ⇒ kết luận: `ready_for_user_confirmation`** (còn 3 minor ghi nhận dưới; không mở vòng 3).
- Chạy lại đúng bộ câu dò của vòng 1 (`data/review_sua_ngay_di_2026-11-15/do_34.py`, 34 câu + câu ghép "đổi sang 20/12 và bỏ điểm thứ hai"): **35 / 35 đúng kỳ vọng** — 8 câu sai trước nay trả "chưa rõ", câu ghép trả 20/12.
- C báo [Chạy]: hàm mới trên 34 câu đã đo thật (D1–D3 + D4) 0 lệch nhãn ⇒ không đo có phí lại; E không chạy lại phần này. Test rộng trên bản sửa: C đang chạy — A xem số của C trước khi merge.
- E thử thêm 19 câu MỚI (0 USD): 12 đúng, 7 lệch:
  - **Vẫn ra sai ngày (4)** — n-1: "tuần thứ hai của tháng" ⇒ thứ Hai tới; "tỷ lệ 1/2" (chữ "tỷ") và "vé 1/2 giá" ⇒ 1/2 năm sau; "hôm 20 tháng 12 ngày chủ nhật" ⇒ luật mới bỏ "20 tháng 12" (vì theo sau là "ngày") nhưng giữ "chủ nhật" ⇒ ra Chủ nhật gần nhất thay vì 20/12.
  - **Từ chối nhầm, an toàn (3)** — n-2: "20/12 ngày đẹp", "3/12 giờ nào cũng được" (đơn vị đứng sau ngày thật), "MAI ĐI LUÔN" (viết hoa cả câu) ⇒ "chưa rõ".
- Nhận định: đúng như C ghi — luật theo danh sách từ không bao giờ kín; phần còn lại là câu hiếm, người dùng vẫn thấy ngày + thứ trong câu báo và sửa lại được bằng một câu. E **không** yêu cầu vòng sửa nữa (đã 2 vòng). n-1 có 3 ca rẻ nếu C tiện tay: thêm "tuần" vào nhóm từ đứng trước "thứ …", "tỷ lệ" cạnh "tỉ lệ", d/m ngay trước "giá". Ca "20 tháng 12 ngày chủ nhật": đề xuất khi một ngày tháng bị loại vì mơ hồ mà câu còn một ngày khác ⇒ trả "chưa rõ" thay vì lấy ngày còn lại — C / A quyết, không chặn.
- n-3 (theo dõi sau merge): đếm trong log số lượt đổi ngày đi và lượt người dùng đổi lại ngay sau đó — tín hiệu rẻ nhất cho "đọc sai ngày" ngoài đời.

### Kiểm commit thêm `add3186` (= `0463bf2` + sửa các ca vòng 2) — 16:55 15/11/2026 (`date`), A nhờ, 0 USD
- Diff `0463bf2..add3186`: `do_so.py` +19 / −7 (luật phân số chuyển từ regex sang code: "tử < mẫu + đơn vị đi sau"; cụm mơ hồ ⇒ cả câu "chưa rõ"; cả câu viết hoa ⇒ hạ thường; thêm "tuần / tháng" trước "thứ …", "tỷ lệ", "giá"), test +5 dòng, report +1.
- Bộ vòng 1 (`do_34.py`, 35 câu): **35 / 35 đúng** — không hồi quy.
- Bộ vòng 2 (`do_19.py`, 19 câu): **17 đúng · 1 ra SAI ngày · 1 từ chối nhầm** (trên `0463bf2`: 12 · 4 · 3).
  - 4 câu sai ngày cũ ⇒ cả 4 nay "chưa rõ"; 2 / 3 câu từ chối nhầm cũ ⇒ nay đúng ngày; còn "3/12 giờ nào cũng được" bị từ chối (3 < 12 + đơn vị đi sau — an toàn).
  - **HỒI QUY 1 câu:** "lùi ngày đi, hẹn 5/5 người" — trên `0463bf2` trả "chưa rõ" (đúng), trên `add3186` trả 5/5 năm sau. Gốc: điều kiện phân số mới đòi tử **nhỏ hơn** mẫu, nên "5/5 + đơn vị" (kiểu "đủ 5/5 người") không còn bị coi là mơ hồ.
- **Chưa đạt điều kiện A đặt (0 câu sai ngày, không hồi quy).** Đóng: đổi "tử < mẫu" thành "tử ≤ mẫu" (1 ký tự) + 1 ca test ⇒ kỳ vọng 35 / 35 và 18 đúng · 0 sai ngày · 1 từ chối nhầm; E chạy lại hai file dò (10 giây).

### Kiểm commit `b7b47f1` (= `add3186` + `<` ⇒ `<=`, 1 ca test, 1 câu report) — 16:57 15/11/2026 (`date`), 0 USD
- E tự chạy lại hai bộ dò trên `b7b47f1`: vòng 1 **35 / 35**; vòng 2 **18 đúng · 0 ra sai ngày · 1 từ chối nhầm** ("3/12 giờ nào cũng được" — an toàn). Câu hồi quy "hẹn 5/5 người" nay trả "chưa rõ". Không câu nào trước đúng nay hỏng.
- Diff `add3186..b7b47f1` phần code đúng 1 dòng điều kiện (E đọc).
- **Đạt điều kiện A đặt (0 câu sai ngày trên 54 câu dò, không hồi quy) ⇒ `ready_for_user_confirmation` trên `b7b47f1`.** Còn lại là giới hạn đã ghi: luật theo danh sách từ không kín; theo dõi lượt đổi ngày bị người dùng đổi lại ngay.
