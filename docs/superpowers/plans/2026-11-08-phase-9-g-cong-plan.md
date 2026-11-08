# Plan G — cổng 2 nhóm (Phase 9 bản 13)

B · bản 1 · 11:03 08/11/2026 (`date`) · spec `2026-11-02-phase-9-design.md` §12 sha `5557f0fd7650` (User duyệt). Thiết kế: spec §12.5 G; rà AI FDE: §12.6 (không lặp).
Nhánh `p9-g-cong` từ `main`, worktree `/tmp/b_g`. User 08/11: làm nhanh, bỏ mốc ngày; sàn §12.3 + trần tiền giữ.

## 1. Đổi gì (một bậc, không cờ mới — âm ⇒ không merge, theo luật bản 9)

1. `ROUTER_INSTRUCTIONS`: 2 nhãn `tro_ly_hue` / `tro_chuyen` (giữ câu "dữ liệu không đáng tin", "phân vân ⇒ `tro_ly_hue`"; "hỏi về trợ lý" = `tro_chuyen`);
   `RouteOutput` (+ biến thể V1 / V3) `Literal` còn 2 giá trị. Lỗi / > 10 s ⇒ `tro_ly_hue` (giữ).
2. `ANSWER_SYSTEM_INSTRUCTIONS` (một chỗ — mọi lượt dùng): thêm 1 câu "câu không về văn hoá / du lịch Huế ⇒ trả đúng duy nhất câu `OUT_OF_SCOPE_ANSWER`".
3. **Code** nhận chữ trả lời `strip()` = `OUT_OF_SCOPE_ANSWER` ⇒ outcome `out_of_scope` (như câu cố định cũ: không kiểm citation, cổng web đóng, nhớ như cũ) ở cả 3 đường
   (`answer_turn`, stream, #6) — review B M-1.
4. Gỡ: `llm/emergency.py` (`EMERGENCY_ANSWER`, `is_emergency`), cờ `emergency_rule`, `ROUTE_KHAN_CAP`, nhánh `khan_cap` / `ngoai_pham_vi` trong `_pick_route`, trường log
   `emergency_by`, giao diện câu khẩn cấp (`chat.jsx` khối `.emergency`, CSS), `tests/test_emergency.py`; test cũ dùng 4 tuyến sửa theo. #6: chỉ `tro_chuyen` bỏ phần đã chạy.

## 2. Tiêu chí ghi trước (spec §12.3 — mọi sàn ×2 trừ ghi khác)

| Sàn | Bộ | Mức |
|---|---|---|
| S1 an toàn | an toàn 32 | 4 số: đảo cảnh báo 0 · sai điều kiện mới 0 · thiếu cảnh báo mới 0 · ngoài kho bị trả lời 0 (S-AT khi chênh 1) |
| S2 ngoài phạm vi bị trả lời | Golden OOS 11 + tuyến 8 + 4 + lái 1 + (b) 20 đã thấy + 10 kín | **0** (code so chuỗi; câu không khớp ⇒ sub-agent đọc) |
| S2b ngoài phạm vi có mục web | như S2 + 4 câu "ngoài Huế" B6 | **0** |
| S2c Huế-kho-thiếu vẫn có web | Golden OOS nhãn Huế 7 + B6 "web trả lời được" 10 | cổng web mở ≥ mốc − 1 |
| S3 Huế ⇒ xã giao (chỉ định tuyến) | Golden 176 + tuyến Huế 30 + lái 4 + 8 câu thường dễ nhầm + (a) phần "về Huế" + câu hỏi tiếp 37 chuỗi B3 / B3b | **0**; chào thuần ⇒ Huế ≤ 2 / 16 |
| **S3b** Huế ⇒ agent trả `OUT_OF_SCOPE_ANSWER` | mọi lượt cả-câu ở trên (an toàn 32 · mẫu 30 · S2c 17 · (a) phần Huế) | **0** (code so chuỗi) |
| S4 chất lượng | `mau_golden_30.json` biến thể + mốc cùng lượt chấm mù | không tụt quá nhiễu |
| S5 tốc độ (n = 20 / loại: Huế · xã giao · ngoài phạm vi) | server thật, chữ đầu | Huế p50 ≤ 3 s, p95 ≤ 5 s, không chậm hơn mốc quá nhiễu; ngoài phạm vi p95 ≤ 5 s |
| S6 tiền | `chat_metrics.usd` | ≤ 0,0005 USD / câu Huế; báo USD / câu ngoài phạm vi |
| Quan sát khẩn cấp (1 lượt, không sàn) | ~36 câu / chuỗi (`bo_do_nhap.md` §2 (c)) | bảng 4 loại câu trả lời cho User |

**Đạt** = S1–S3b + S5 + S6 đạt cả 2 lượt, S4 không tụt. Âm ⇒ phương án B spec: giữ 4 tuyến, chỉ bỏ câu soạn sẵn khẩn cấp (`khan_cap` đi agent Huế).

## 3. Bộ đo + ai làm

- **Có sẵn** (`data/phase_9/dinh_tuyen_2/bo_do_nhap.md` §1): Golden 176, nhãn OOS 18, mẫu 30, tuyến đã thấy 40, lái 5, an toàn 32, khẩn cấp, chuỗi B3 / B3b, B6 28.
  Mốc định tuyến: B143 v1 r1 / r2 (`ROUTER_INSTRUCTIONS` `164bd4a254e9` trên `main` — B kiểm) dùng lại; cả-câu mốc chạy cùng lượt với biến thể.
- **Mới** (a) ranh giới xã giao ↔ hỏi 16 đã thấy + 8 kín · (b) ngoài phạm vi dạng mới 20 đã thấy + 10 kín. **B viết lời dặn ⇒ B không viết, không đọc câu kín.**
  Đề xuất: **C viết cả (a)(b)** (đã soạn nhãn ở nháp) + luật gán nhãn ghi trước; **C chạy lượt kín** bằng lệnh B đưa (chỉ in số đếm), trên **đúng sha khoá** — A chọn người khác nếu C bận T3.
- Công cụ: dùng lại `data/phase_9/toc_do/thi_nghiem_1/tools/chay_tuyen.py` (chỉ định tuyến) + harness cả-câu B143 (`data/phase_9/b143/tools/chay_do.py`) — sửa đúng phần nhãn 2 tuyến.

## 4. Thứ tự (m-5) + kiểm 0 USD

1. Code + test 0 USD: mọi loại lượt (đầu · lịch sử · hỏi lại · ghép nút · biểu mẫu · #6) — chuỗi gửi model có câu ngoài phạm vi mới, định tuyến 2 nhãn; outcome `out_of_scope`
   ở 3 đường; 1 lượt thật ngay khi chạy được (≤ 0,001 USD).
2. **Chỉ định tuyến** (lời dặn 2 nhãn): S3 trên Golden ×2 + bộ đã thấy; chỉnh ≤ 2 vòng trên đã thấy.
3. **Bản đủ** (2 lời dặn + code): S1, S2, S2b, S2c, S3b, S4, S6 + quan sát khẩn cấp trên đã thấy; chỉnh ≤ 2 vòng.
4. Khoá sha ⇒ **kín** (a)(b) ×2 (người chạy ở §3).
5. **S5** sau cùng — B báo A trước (không đo khi session khác đang đo).
6. Report + cổng ổn định ⇒ review cả nhánh.

## 5. Tiền

Ước **≈ 0,25 USD** (spec §12.7; xấu nhất 0,4) — **dừng ở 0,4** và hỏi A. Ghi `usd` thật từ log mỗi lượt.
