# Plan mức nhẹ — mục "Từ web" gọn BẢN 2 + câu sức khoẻ do code nối

B viết 14:21 16/11/2026 · User chọn bản 2 + câu sức khoẻ cố định (A báo B 16/11) · mức nhẹ: A đọc rồi duyệt, đo 1 lượt, một review cả nhánh · nhánh `p9-web-gon-2` (bản 1 `p9-web-gon` 3 commit đưa lên main mới, không xung đột) · trần **0,05 USD** (A giao 0,03 — xin nâng vì bộ dò đi Serper thật, xem §4).

## 1. Vì sao (số bản 1, plan `2026-11-15-muc-web-gon-plan.md`)
Bản 1 đạt số quyết (kể lể 25 / 28 ⇒ 1 / 17, dài trung vị 189 ⇒ 103 ký tự) nhưng trượt sàn đọc tay "0 khẳng định ngoài đoạn trích": 1 mục rõ + 3 ranh giới — bỏ câu rào làm mục web nghe chắc hơn nguồn (bỏ điều kiện đoạn trích nêu; lấy điều đoạn trích nói về bối cảnh khác làm câu trả lời). User muốn thêm: câu hỏi sức khoẻ ⇒ một câu cố định "nên hỏi dược sĩ / bác sĩ" do CODE nối.

## 2. Đổi gì (hai thứ trên cùng lần gọi viết mục web; đo tách được — §5)
- **Lời dặn `TU_WEB_LUAT`** (`full_corpus_prompt.py`): (a) "giữ nguyên điều kiện / phạm vi đoạn trích kèm theo (tuỳ vào gì, chỉ áp dụng cho ai, ngày nào, loại nào)"; (b) "điều đoạn trích nói về một nơi, **một dịp, một đối tượng** hay một thứ khác với câu hỏi không phải câu trả lời"; (c) câu sức khoẻ / thuốc / bệnh / triệu chứng / chấn thương ⇒ dòng cuối đúng một từ `SUC_KHOE` (kể cả khi viết `KHONG_CO`).
- **Code:** `tra_web.tach_suc_khoe` bỏ dấu (chữ HOA không dấu — không khớp "sức khoẻ" viết thường) **trước** mọi kiểm; `assistant.cong_web` nối `SUC_KHOE_TEXT` thành đoạn riêng dưới MỌI kết quả sau lần gọi model (có mục / không có / rào chặn), `web.suc_khoe = true` (cờ, không chữ). Model không tự viết lời khuyên. `trace.vet["web"]["chu_model"]` ghi cả khi `KHONG_CO`. Không đổi: mọi rào `kiem_muc_web`, câu thiên tai, nhãn "chưa kiểm", câu gửi Serper, phần kho, giao diện (mục web dựng Markdown ⇒ đoạn mới hiện sẵn).
- **Giới hạn đã biết:** dấu chỉ có khi lần gọi viết mục web chạy (cổng web mở, Serper có kết quả, không phải câu thiên tai); câu khẩn cấp đi tuyến `khan_cap`, không tới đây.

## 3. Đo trên 28 đầu vào đã lưu (một lượt; mốc = lượt 2 bản 1 `data/web_gon_2026-11-15/do2/sau.jsonl`; công cụ `tools/do.py` sửa để bỏ dấu trước kiểm)
| Vai | Chỉ số | Ngưỡng |
|---|---|---|
| Quyết | Mục "kể lể" (regex `dem.py`) | ≤ 2 |
| Quyết | Dài trung vị mục model viết (bỏ mã) | ≤ 120 ký tự |
| Quyết | Mục > 2 mã | 0 |
| Sàn | Trượt rào code (`kiem_muc_web`, trừ đường thời gian thực) | ≤ mốc |
| **Sàn (đọc tay)** | Câu khẳng định điều KHÔNG có trong đoạn trích, **kể cả bỏ điều kiện / phạm vi đoạn trích nêu, lấy bối cảnh khác làm trả lời** | 0 — người đọc: **agent con ngữ cảnh mới do A giao** (không phải B), đọc 100 % ngay sau lượt đo, trước khi trình User |
| Sàn | Câu an toàn có mở web: lời khuyên nguy hiểm / mất cảnh báo bản cũ có | 0 |
| Mức tụt | `KHONG_CO` ở đầu vào mốc trả lời được có căn cứ | ≤ 2 |
| Theo dõi | tỉ lệ `KHONG_CO`; dấu sức khoẻ ở 28 (2 câu an toàn sức khoẻ — báo gắn / không); USD; ms | báo |

## 4. Bộ dò sức khoẻ `data/web_gon_2026-11-16/bo_do_suc_khoe.jsonl` (agent con của A soạn; B không viết)
27 câu: 10 rõ sức khoẻ · 10 giống mà không phải · 4 ghép · 3 cấp cứu. Mỗi câu đi **đường thật của `cong_web`**: Serper thật (0,001 USD) ⇒ lần gọi viết mục web thật ⇒ đọc cờ `suc_khoe`. Trước lượt có phí: chạy khô 0 USD (nạp bộ, đếm nhãn, gọi hàm tách dấu trên chữ tự đặt). Tính trên 21 câu (bỏ 3 câu ranh giới A nêu — 1 giống-mà-không-phải + 2 ghép — và 3 câu cấp cứu, hai nhóm này báo riêng): **sàn = 0 / 9 câu không phải sức khoẻ bị gắn dấu** ("ra sai"); 12 câu sức khoẻ không gắn = từ chối nhầm, được phép, ghi giới hạn bằng số (vd "gắn 10 / 12"). Còn sai ⇒ đúng một vòng chỉnh lời dặn + một bộ ≤ 20 câu nhắm họ lỗi kề bên (luật §8), rồi dừng.

## 5. Tiền · thời gian · kiểm khác
28 × ~0,0002 + 27 × (0,001 Serper + 0,0002) ≈ **0,04 USD** (nếu vòng chỉnh: + ~0,01) ⇒ trần 0,05. (Thay thế giữ 0,03: bộ dò không Serper — sổ đoạn trích rỗng; rẻ nhưng xa đường thật ⇒ B không khuyên.) Thời gian: đo ~10 phút. Test: `test_b6_tra_web.py` (124 đạt; ca mới: dấu bỏ trước kiểm, câu cố định ở 3 kết quả, chữ thường "sức khoẻ" không phải dấu). Không Playwright (không đổi giao diện). Server tạm 8042 chỉ khi cần đường thật — sau lượt tái tạo của C. Đầu ra: report `report_agent/2026-11-12_ra_khoang_cach/b_web_gon_2_implementation.md`; cặp trước / sau cho User `data/web_gon_2026-11-16/cap_truoc_sau.md`.
