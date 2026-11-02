# C131 — chạy phần kín B1: P1 (định tuyến) + P3 (khẩn cấp)

Người làm: C (Claude Opus 5.5, `hue-rag-cc`) · 20:28 02/11/2026 (`date`). Việc A giao theo plan B1 bản 2 `0c9e137b56af` §5 bước 6.
Nhánh `p9-b1` commit **`7e190d7`**, chạy trong worktree riêng của C (`/tmp/c131`, detached, đã gỡ). Không dùng worktree của B.
**Chỉ số đếm**: không chép câu, không chép câu trả lời. Kết quả chi tiết ở `data/phase_9/c131_kin/` (private; B không đọc).

## 1. Kiểm khoá trước khi chạy (plan §5 bước 6, dòng "Khoá" trong `b129_b1_implementation.md` §6)

| Thứ khoá | sha256 (12) ghi trong report B | C tính lại trên `7e190d7` |
|---|---|---|
| `ROUTER_INSTRUCTIONS` (chuỗi, UTF-8) | `fb4e1aa7f8fe` | `fb4e1aa7f8fe` ✔ |
| `CHAT_INSTRUCTIONS` (chuỗi, UTF-8) | `df921574c362` | `df921574c362` ✔ |
| `backend/llm/emergency.py` | `3342783354d0` | `3342783354d0` ✔ |
| `backend/config/settings.yaml` | `0f12087f4d5a` | `0f12087f4d5a` ✔ |
| `data/phase_9/b1/tools/p1_route.py` | `ba7d7bb6bbc6` | `ba7d7bb6bbc6` ✔ |
| `data/phase_9/b1/tools/emergency_check.py` | `f05e25c4975a` | `f05e25c4975a` ✔ |

6 / 6 khớp ⇒ C chạy.

## 2. P3 — khẩn cấp (0 USD, tất định, 1 lượt)

Lệnh: `emergency_check.py --sealed <file kín> <ra câu luật sót>` (B viết), chạy trên `khan_cap_sealed.jsonl` (8 + 8) và trên `tuyen_sealed.jsonl` (2 câu khẩn cấp + 18 câu khác). C chạy lại cả phần đã thấy để đối chiếu.

| Chỉ số (plan P3) | Đã thấy (C chạy lại) | **Kín** |
|---|---|---|
| (b) độ phủ: câu khẩn cấp luật bắt | 14 / 14 | **0 / 8** (bộ khẩn cấp kín) · **0 / 2** (câu khẩn cấp trong bộ tuyến kín) |
| (a) sàn chặn nhầm: câu thường bị chặn | 0 / 249 (36 bộ tuyến + 5 ca lái + 176 Golden + 32 an toàn) | **2 / 8** (câu thường kín dễ nhầm) · 0 / 18 (câu thường bộ tuyến kín) |

- 2 câu thường bị chặn nhầm thuộc hai loại: hỏi để phòng trước, và hỏi lịch sử có từ chỉ tai nạn.
- **Theo luật ghi trước** (plan P3, A quyết M-2):
  - **(a) không đạt** (2 câu thường kín bị chặn) ⇒ **tắt `emergency_rule`**;
  - **(b) sót 8 / 8 + 2 / 2** ⇒ kết quả âm, ghi lại; không sửa luật theo câu kín.
- Đọc kết quả: luật mẫu chữ khớp **đúng** phần đã thấy (14 / 14, 0 / 249), nhưng phần kín cố ý khác loại và khác cách gõ thì nó không bắt được câu nào, lại chặn nhầm câu thường. Đây là dấu hiệu **khớp quá sát phần đã thấy**.

## 3. P1 — định tuyến (có phí, lần gọi model thật)

Lệnh: `p1_route.py <ra> --set tuyen_sealed.jsonl <câu khẩn cấp kín luật sót>` (B viết; `--env-file` tuyệt đối). Định tuyến gọi trực tiếp, không qua luật khẩn cấp, nên 2 câu khẩn cấp của bộ tuyến kín được đo bằng định tuyến.

| Chỉ số (plan P1) | Kín |
|---|---|
| định tuyến đúng (`nhan` ∪ `chap_nhan`), quyết: kín ≥ 16 / 20 | **20 / 20** (trợ lý Huế 10 / 10 · trò chuyện 4 / 4 · ngoài phạm vi 4 / 4, trong đó 1 câu đi `tro_chuyen` thuộc `chap_nhan` · khẩn cấp 2 / 2) |
| sàn 1: câu `tro_ly_hue` (không `chap_nhan`) sang trò chuyện / ngoài phạm vi | **0** |
| lưới thứ hai: câu khẩn cấp kín luật sót ⇒ định tuyến chọn `khan_cap` | **8 / 8** |
| tách "luật bắt / định tuyến bắt" cho 10 câu khẩn cấp kín (8 bộ khẩn cấp + 2 bộ tuyến) | luật bắt **0** · định tuyến bắt **10** · sót cả hai **0** |
| lỗi định tuyến (`route_error`) | 0 / 28 |
| **sàn 2** (judge): câu đi `tro_chuyen` có thông tin Huế cụ thể | **0 / 5** |

**Sàn 2:**
- 5 lời trò chuyện thật, cộng 2 phiếu kiểm biết trước (một có thông tin cụ thể, một không), xáo theo seed ghi trước, đưa cho **2 judge sub-agent độc lập**.
- Brief ghi **trước** khi xem lời trả lời: `data/phase_9/c131_kin/san2_brief.md` `91f0cb07d7d4`. Brief chặt hơn một chút so với định nghĩa sàn 2: gợi ý một tên nơi cụ thể cũng tính là lọt.
- Cả 2 judge đúng 2 / 2 phiếu kiểm; 0 / 5 lọt (luật "một trong hai"); 0 bất đồng.

**Tiền:** 0,002384 USD, gồm 28 lần định tuyến + 5 lời trò chuyện (trần C131 là 0,02).

**Thời gian (chỉ theo dõi, chạy chồng với lượt P2 có phí của B, W31):** mỗi lần gọi model 1,22–2,09 s (33 lần). Số này không dùng để so sánh.

## 4. Gợi ý cho A (không phải quyết định của C)

- Theo luật ghi trước, P3 (a) không đạt ⇒ **tắt `emergency_rule`**.
- Với cờ đó tắt, trên phần kín định tuyến vẫn đưa 10 / 10 câu khẩn cấp sang `khan_cap` ⇒ trả Bản 1 (câu soạn sẵn). Khác biệt là mỗi câu khẩn cấp phải qua **một lần gọi model** (định tuyến, ≈ 1,2–2 s). Sàn spec "0 câu khẩn cấp vào model" vì vậy không giữ được, trừ khi có luật code tốt hơn.
- Muốn giữ sàn đó thì cần luật **mới** viết lại và đo trên một bộ kín **mới**. Bộ kín này đã dùng, không chỉnh rồi đo lại (plan §7). Đó là việc A / User quyết.

## 5. Giới hạn

- Cỡ mẫu nhỏ: 8 + 8 câu khẩn cấp kín và 20 câu tuyến kín. 0 lỗi định tuyến chưa chứng minh tỉ lệ lỗi bằng 0 (plan §4 "Cỡ mẫu").
- Bộ kín do C viết. C cũng là người chạy và gửi số; judge sàn 2 là sub-agent độc lập.
- P2 kín (ngày, 7 câu): **NOT RUN**. Report B ghi chưa có harness.
- Định tuyến chạy 1 lượt mỗi câu (spec: các bậc khác B7 chạy 1 lượt).
