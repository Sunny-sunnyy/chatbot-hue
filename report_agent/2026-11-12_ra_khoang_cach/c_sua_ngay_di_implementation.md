# Sửa lịch bằng lời — đổi ngày đi (bậc 2) · C · 16:45 15/11/2026

Plan `docs/superpowers/plans/2026-11-15-sua-lich-ngay-di-plan.md` (A duyệt bản `f36fe8bb5b6a`). Nhánh `p9-sua-ngay-di`, bản đo **`ad81cc0`** (đã chứa `main` `c9378e2`: bậc 1, "nơi ở chỉ khi hỏi", nhánh nhỏ sau review). **Đạt mọi tiêu chí ghi trước, không cần vòng chỉnh lời dặn. Chờ review cả nhánh.**

## Làm gì
- **Trước:** sau khi có lịch, câu xin đổi ngày đi bị trả lời như câu thường (4 / 5 câu đếm sáng 15/11), 1 / 5 bị hiểu thành đổi SỐ ngày (đã rào trưa 15/11 ⇒ "Chưa làm").
- **Sau:** hành động mới `doi_ngay_di` **không có tham số**. Model chỉ nhận ra ý "đổi ngày đi"; **ngày do code đọc từ chính chữ người dùng** (`do_so.ngay_tu_cau`) ⇒ không có đường nào cho một ngày người dùng không gõ.
  - Đọc được: dd/mm · dd/mm/yyyy · "d tháng m [năm yyyy]" · hôm nay · mai · ngày kia / mốt · thứ X (chữ hoặc số) / chủ nhật · cuối tuần · kèm "tuần sau / tuần tới". Không năm ⇒ lần tới gần nhất.
  - Không đổi, có dòng lý do do code viết: không đọc được MỘT ngày (không có ngày, ≥ 2 ngày khác nhau, nói tương đối "dời 2 hôm", ngày âm / dịp Tết) · ngày không có thật · ngoài hạn của biểu mẫu (hôm nay … +180 ngày, gồm ngày đã qua) · trùng ngày đang dùng · ngày mới làm lịch không xếp được đúng luật (chưa gặp lần nào).
  - Áp (`sua_lich_v2.ap(ngay_moi=…)`): lấy dự báo cho ngày mới bằng đúng hàm của lượt biểu mẫu ⇒ thử **giữ mọi điểm ở chỗ cũ**; phạm luật (thứ đóng cửa, hoạt động theo thứ, mưa) ⇒ xếp lại, điểm đã bỏ không quay lại; khung mới phải qua bộ kiểm luật.
  - Câu báo (code): "Đã đổi ngày đi: A → B (thứ …)." + "Các điểm trong lịch giữ nguyên chỗ." hoặc "Lịch xếp lại theo ngày mới (…): k điểm đổi ngày hoặc buổi; bớt …; thêm …" + "Ngày này chưa có dự báo thời tiết nên lịch chưa xét mưa." khi không có dự báo.
- Lời dặn hiểu ý: +1 gạch hành động ngắn, +1 câu ở khối "cách nói thường gặp" (không chèn chữ dài vào danh sách hành động — bài học bậc 1); không sửa phần số ngày. Không cờ mới, không sửa giao diện.
- File: `backend/llm/do_so.py`, `sua_lich_v2.py`, `len_ke_hoach.py` (`hieu_va_ap`, `stream_sua`), `full_corpus_prompt.py`, test mới `test_sua_ngay_di.py`.

## Kết quả (mọi dòng [Chạy]; lượt có phí qua `/api/chat/stream` trên server của nhánh, cuộc đã có lịch có ngày đi; ngày trong câu + nhãn sinh theo hôm chạy)
| Tiêu chí ghi trước | Ngưỡng | Kết quả |
|---|---|---|
| Luôn-a — hàm đọc ngày, bảng ca tự đặt | 100 % (≥ 30 ca) | **37 / 37** lúc đo; **57 / 57** sau review (mục "Sau review E") + 5 ca hạn ngày |
| Luôn-b — áp ngày mới trên 3.840 khung × 3 ngày (một thứ Hai · một thứ Bảy có mưa lớn ngày 2 · một ngày mùa khác) | 0 lệch | **đạt**: 0 lỗi luật, điểm đã bỏ không quay lại, số trong câu báo = đếm lại độc lập |
| Q1 — 25 hằng lời dặn so `main` | chỉ lời dặn hiểu ý khác | đạt |
| **D1** — 12 câu nêu một ngày rõ × 2 lượt | ≥ 10 / 12 đúng cả 2 | **12 / 12** |
| **D1-sai** — đổi sang ngày khác nhãn | 0 / 24 | **0** |
| **D2** — 6 câu nhóm "không đổi" × 2: có đổi ngày đi | 0 / 12 | **0** |
| D2-nói — có dòng lý do ở cả 2 lượt | ≥ 4 / 6 | **5 / 6** (4 câu "nói một ngày cụ thể", 1 câu "ngoài hạn"; câu về dịp Tết âm lịch model không coi là câu sửa ⇒ đi đường trả lời thường, không có dòng lý do) |
| **D3** — 8 câu có chữ chỉ ngày nhưng không xin đổi ngày đi × 2 | 0 / 16 | **0** (4 câu hỏi thông tin đi đường thường; 4 câu sửa khác vẫn là lượt sửa của đúng loại) |
| **Sàn số ngày** — câu D1 + D2 bị đổi SỐ ngày | 0 | **0** |
| **Q3** — 10 chuỗi đã thấy, pass^2 (chạy ngay sau D1–D3) | ≥ 8 / 10 · chuỗi hồi quy bậc 1 2 / 2 | **8 / 10 · 2 / 2** (xem dưới) |
| **H1 bậc 1** — bộ câu đổi hạng × 1 lượt | ≥ 10 / 12 · sai mức 0 | **12 / 12 · 0** (cả H2 0 / 6 đổi, 6 / 6 hỏi lại; H3 0 / 6) |
| **Q5** · **Q5b** | 0 / 64 · 0 / 16 | **0 / 64 · 0 / 16** |
| D4 — 8 câu lạ A viết sau khi lời dặn chốt (A chưa xem bộ D và lời dặn), 1 lượt | ≥ 6 / 8 · sai 0 | **8 / 8 · 0** |
| Tốc độ (theo dõi) — tới lúc khung hiện | p50 ≤ 3 s | 32 lượt đổi ngày: p50 1,99 s, chậm nhất 4,26 s |

- **Q3 hai chuỗi trượt, không quy cho nhánh:** (1) chuỗi có bước thẻ chọn trượt 1 / 2 — chập chờn đã ghi từ 14/11; (2) một chuỗi "thêm một điểm" trượt 2 / 2 **do nhãn cũ**: nhãn đòi lý do "điểm chưa có trong danh sách", nhưng bảng điểm v9 (vào `main` chiều 15/11) đã thêm đúng điểm đó ⇒ model vẫn ra đúng hành động thêm điểm, code nhận ra điểm và trả lý do khác. Ở lần đo bậc 1 (trước v9) chuỗi này 2 / 2. A quyết: không sửa nhãn trong bậc này, tính theo ngưỡng ghi trước; rà nhãn theo v9 là việc riêng, người khác làm.
- **Trong 32 lượt đổi ngày thật:** 30 lượt các điểm giữ nguyên chỗ, 2 lượt lịch xếp lại (câu báo nêu bớt một hoạt động buổi tối chỉ có theo thứ và thêm một điểm khác); 19 lượt có dự báo, 13 lượt ngoài 7 ngày ⇒ có dòng "chưa xét mưa".
- **Q5b theo harness mới của B:** vế mới "định tuyến nhận ra khẩn cấp" 16 / 16 (lần đầu có số — theo dõi, không chặn).
- **Lượt có phí không chấm khung** (dự báo thật đổi theo giờ chạy) — đúng sai của khung do Luôn-b giữ.
- **Không chạy:** Golden 176 + an toàn ngoài cuộc có lịch (0 câu chạm), bộ kín, Playwright (không sửa giao diện), test rộng (chạy một lần trước merge nếu người review cần — 5 file chạm 178 đạt).
- **Tiền (theo mã bản `ad81cc0`):** server 0,1189 USD (184 lượt) + Q5 0,0037 = **≈ 0,123 USD** / trần 0,25.

## Điều người quyết cần biết
- **Chưa làm (đúng plan):** nói tương đối theo ngày đang dùng ("dời 2 hôm", "lùi một tuần"), ngày âm / dịp Tết, bỏ ngày đi, câu có hai ngày — đều được hỏi lại "nói một ngày cụ thể" (trừ khi model không coi là câu sửa, như câu D2 thứ 6).
- **"Tuần sau" tính theo tuần lịch (thứ Hai – Chủ nhật).** Hôm chạy là Chủ nhật nên "thứ Bảy tuần sau" = thứ Bảy 6 ngày nữa — trùng "thứ Bảy này". Người nói vào Chủ nhật có thể ngụ ý tuần kế nữa; câu báo luôn in ngày + thứ để người dùng thấy và sửa.
- **dd/mm không năm mà đã qua** ⇒ hiểu là năm sau ⇒ thường rơi vào "ngoài 180 ngày" (câu báo nêu ngày kèm năm).
- Lịch chưa có ngày đi ⇒ câu này đặt ngày ("chưa chọn → …").
- Nút ngày trên biểu mẫu không tự đồng bộ theo lời (như các trường khác).
- Một lượt có cả đổi ngày đi và hành động khác: áp theo thứ tự người nói, tối đa 2 hành động / lượt (đổi hạng chỗ ở luôn xét sau cùng).

## Sau review E (changes_requested 0 / 1 / 3 — `e_review_sua_ngay_di.md`)
- **M-1 (đóng bằng code + test, 0 USD):** E gọi thẳng hàm đọc ngày với 34 câu dò, 8 câu có chữ GIỐNG ngày bị đọc thành một ngày cụ thể: tên người / tên đường có chữ "Mai" ⇒ ngày mai · "điểm thứ hai / thứ 3" ⇒ thứ Hai / thứ Ba · phân số và "24/7", "1/2 ngày" ⇒ ngày tháng năm sau · "2 tháng 3 ngày nghỉ" ⇒ 2/3. Hệ quả ngược: câu ghép "đổi sang <ngày> và bỏ điểm thứ hai" thấy hai ngày ⇒ từ chối nhầm. Lượt đo có phí không lộ vì bộ D không có câu kiểu này.
  - Sửa trong `do_so.ngay_tu_cau` (nguyên tắc: mơ hồ ⇒ không coi là ngày): "mai" xét trên chữ gốc — bỏ khi viết hoa giữa câu, đứng sau từ xưng hô / đường / phố / hoa…, hoặc theo sau là chữ viết hoa; "thứ …" bỏ khi ngay trước là điểm / nơi / chỗ / lần / mục / quán…; d/m bỏ khi ngay sau là đơn vị (ngày, giờ, buổi, nhóm, phần…), đứng sau "tỉ lệ / khoảng", hoặc đúng "24/7"; "d tháng m" bỏ khi ngay sau là "ngày / tuần".
  - [Chạy] bảng ca 37 ⇒ **57 / 57** (8 ca của E + 4 ca cùng họ ⇒ "chưa rõ"; 8 ca câu ghép / "Mai" đầu câu ⇒ đúng ngày thật). [Chạy] ngoại tuyến hàm mới trên **34 câu đã đo thật** (26 câu D1–D3 + 8 câu D4): 20 câu có nhãn ra đúng ngày nhãn, 5 câu D2 "chưa rõ" vẫn không ra ngày, câu D2 ngày đã qua vẫn ra đúng ngày đó (bị chặn ở kiểm hạn) ⇒ **0 lệch** ⇒ không đo có phí lại (lời dặn + khuôn đầu ra không đổi).
  - Còn hở đã biết: luật theo danh sách từ đứng trước / sau nên chữ giống ngày kiểu khác (chưa nghĩ ra) vẫn có thể lọt; hàm chỉ chạy khi model đã coi câu là "đổi ngày đi", và dòng báo luôn in ngày + thứ.
- **m-1** ("tuần sau" theo tuần lịch): E nhận, không sửa. **m-2:** câu "Giải thích ngắn" nói quá — đã sửa ở trên. **m-3:** lượt đổi ngày có hai mục thời tiết trong danh sách công cụ của log (dự báo lấy một lần trước khi áp, một lần khi dựng lịch — lần hai đọc đệm); không bộ đếm nào dựa vào "đúng một".

## Bảng rà AI FDE (sau khi làm)
| Mục | Hiện trạng | Khớp / lệch |
|---|---|---|
| Model ↔ code | Model: nhận ý. Code: đọc ngày, kiểm hạn, lấy dự báo, giữ / xếp lại, đếm thay đổi, câu báo | khớp |
| Tham số | Không tham số — test khẳng định schema từ chối trường ngày | khớp |
| Làm sai mà báo đã làm | D1-sai 0 / 24, D4 0 / 8, sàn số ngày 0; khung đổi thì câu báo nêu rõ | khớp |
| Từ chối có lý do | 5 mã lý do, câu cố định | khớp (1 / 6 câu D2 không thành lượt sửa ⇒ không có dòng) |
| Chữ người dùng là dữ liệu | Q5 0 / 64, Q5b 0 / 16, D3 0 / 16 | khớp |
| Đường ra mới | Không (Open-Meteo như lượt biểu mẫu, không gửi chữ người dùng) | khớp |

**Dữ liệu (private):** `data/sua_lich_ngay_2026-11-15/` — `cau_d.jsonl` (md5 `7b5b22cbda07`, C ghi trước), `cau_d4.jsonl` (A), `tools/do_d.py` (`--mo-phong` 0 USD), `tools/cham_d.py`, kết quả `do/`.

**Giải thích ngắn:** người dùng nay nói được "đổi ngày đi sang 20/12" hay "dời sang thứ Bảy tuần sau"; trợ lý chỉ nhận ra ý, còn ngày do code đọc từ đúng chữ người dùng gõ — model không tự đặt ra ngày được. Code vẫn có thể đọc nhầm một cụm chữ GIỐNG ngày (review đã bắt 8 kiểu, đã sửa — mục dưới); gặp câu mơ hồ thì không đổi và hỏi lại. Đổi ngày có thể làm lịch xếp lại (điểm đóng cửa theo thứ, mưa) — khi đó dòng "Đã đổi" nói rõ đổi gì.
