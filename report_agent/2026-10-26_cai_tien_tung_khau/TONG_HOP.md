# TỔNG HỢP đợt "tìm hướng tốt hơn từng khâu" (đang mở) — tới hết phiên tối 26/10/2026

Người viết: A (terminal `hue-rag-2d`) · cập nhật 22:31 26/10/2026 (`date`) · Đợt mở 20:0x 25/10 (User). Từ 21:3x 26/10 đợt này **là Bước 2 của
Phase 8.2** (spec `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` §10, bản A duyệt `cd910c4c4169`). Report từng việc ở thư mục
này (phân loại lỗi, đề xuất, review) và ở `report_agent/2026-10-25_phase_8_2_ap_dung/` (plan / implementation / review K1, K3, R2, R3, R4).

## 1. Mục tiêu

User 20:0x 25/10: "thử nghiệm, so sánh, đánh giá xem có hướng nào tốt hơn, tối ưu hơn, ổn định hơn; giữ mốc hiện tại làm base". User 21:1x 26/10
chọn **phạm vi B: khâu trả lời + thí nghiệm khâu tìm, không ghi Qdrant**, và cho A tự đề xuất / thử / so sánh / chọn trong luật ghi trước.

## 2. Quyết định theo giờ (phiên tối 26/10)

| Giờ | Ai | Quyết định |
|---|---|---|
| 20:3x | User | Quyền phiên: A tự điều phối B/C; API ≤ 1 USD cả phiên; B commit + push `p82-b1`. Đồng ý đề xuất A câu 2–7 (sổ cải tiến W14/W16–W20, 80 report để nguyên, giữ commit trước sửa + cổng ổn định, xóa `dot3`) |
| 20:4x | User | Luật (a): nhận thay đổi khi chất lượng không tụt quá mức ghi trước **và** rẻ / nhanh hơn rõ; luôn so **cùng một mốc** (context 10) |
| 20:5x | A | Phân loại lỗi (C36, B42) cho thấy 80 % điểm mất đi kèm thiếu bằng chứng ⇒ trình lại phạm vi (khuyên B) |
| 21:1x | User | Phạm vi **B**; luật (i) cho "chất lượng tăng nhưng tốn hơn"; A tự chọn trong luật; hook quét cả câu kín; `tham khảo 26_10/` không liên quan dự án |
| 21:2x | A | Đợt cải tiến viết thành **§10 của spec 8.2** (một Phase một tài liệu), không spec mới |
| 21:3x | User | "Không tốn thêm tiền" = không thêm lần gọi API, USD / câu ≤ +20 %. **Nguyên tắc: chất lượng cần thiết trước, tối ưu hiệu suất sau** (áp mọi phần) ⇒ `Session_Prompt.md` §7 |
| 21:4x | A | Duyệt spec §10 sau C38 2 vòng; bỏ K2 (đã trượt Holm-10 ở 8.1); cỡ mẫu ≥ 5 / 0 (Holm họ 2) |
| 21:5x | User | Hiệu suất = **tiền và tốc độ** |
| 22:0x | User | Nguyên tắc **"đo theo mục tiêu sản phẩm cuối cùng"** (khóa AI FDE) ⇒ §7; chất lượng trước ⇒ K3 vẫn thử dù chậm; R1 nhận khi USD ≤ 0,95× **hoặc** token ra ≤ 0,9× |
| 22:1x | A | Tốc độ khâu sinh đo bằng `output_tokens` (latency provider SD ~0,8 s / câu không phân giải ±50 ms); gác R2 sau khi phạm sàn; R3 NOT RUN (trần 6 câu) |
| 22:2x | User | Kết phiên (b); K3 để phiên sau |

## 3. Kết quả

**Phân loại lỗi trên mốc context 10** (dev chính 88 câu; A tính lại số chính — `phan_loai_loi_{B,C}_review.md`):
- 10 câu bị cờ, **cả 10 thiếu bằng chứng** trong 10 đoạn; Completeness mất 46 điểm: 20 do từ chối khi có một phần fact (5 câu), 9 do trả lời gọn (9 câu),
  17 do thiếu bằng chứng thuần.
- 40 câu có đoạn đúng: đủ ở pool 30 / top-10 / context 5 = 31 / 22 / 17. 18 câu thiếu ở context 10: ~nửa đoạn đúng ngoài pool 30, ~nửa trong pool nhưng
  bị xếp ngoài top-10. **Câu tự nhiên không lợi từ context 10** (6 / 12 ở cả hai mức).

**Thí nghiệm (so mốc B1 `811d25d`, tiêu chí ghi trước, plan review trước khi duyệt sha):**

| # | Đổi | Kết luận | Tiền | Bằng chứng |
|---|---|---|---|---|
| K1 | pool dense 30 → 100 | **kém hơn** — phạm sàn (câu 154 mất đoạn đúng); 2 / 37 / 1; latency +8,9 ms. Pool đủ đoạn đúng 31 → 37 nhưng top-10 chỉ 22 → 23 ⇒ **chỗ nghẽn là xếp hạng** | 0 | nhánh `p82-k1` `a7710ed`; `phase_8_2_k1_review.md` (C42 ready) |
| K2 | native p30 k = 2 | **NOT RUN** — đã trượt Holm-10 ở 8.1 G1.3; chọn lại trên cùng dev là chọn vì may | 0 | spec §10.3 |
| K3 | luna xếp lại pool 30 → top-10 | **plan duyệt, chưa chạy** (phiên sau) | — | `phase_8_2_k3_plan.md` sha `0a6370204c7d` (C44 ready) |
| R4 | thước "số trong câu trả lời có trong nguồn được trích" | xong — **chỉ là danh sách đọc lại** (ngoài mẫu đúng 0 / 5) | 0 | `2c7ecfd`; `phase_8_2_r4_review.md` (B47 ready) |
| R2 | trả lời phần có căn cứ (E1b) | **kém hơn** — phạm sàn bước 1 (1 / 12 câu ngoài kho bị trả lời, cùng dạng P1 8.1); **hướng gác** | 0,0027 USD (log) | `origin/p82-r2` `aec9ab8`; **chờ B review** |
| R3 | prompt "nêu đủ chi tiết" | **NOT RUN** — chỉ 6 câu có thể đổi, dưới cỡ mẫu tính trước | 0 | `phase_8_2_r3_plan.md` + `_review.md` (giữ hồ sơ) |
| R1 | `reasoning_effort = none` | chưa làm (xếp cuối theo "chất lượng trước") | — | spec §10.3 |
| E2 | sửa thiếu `[n]` | **NOT RUN** — validator v2: mốc 0 lỗi | 0 | spec §10.3 |

**Cách làm / rào bằng máy (governance, review chéo):** hook pre-commit quét dòng thêm mới trùng Golden / kho / câu kín (`.githooks/overlap_scan.py`,
W16 + câu kín; C 2 vòng, B 2 vòng); luật W14 + W18, W17, W19, W20; luật chung §7 thêm 3 nguyên tắc User (chất lượng trước; hiệu suất = tiền + tốc độ;
đo theo mục tiêu sản phẩm cuối); `Project_Status.md` §1 "Mục tiêu sản phẩm" (đã chốt + câu chờ User).

**Chatbot không đổi** (vẫn context 5, chưa NFC, reasoning `medium` mặc định). Qdrant 1 collection 8.459, không ghi.

## 4. Tiền

Phiên tối 26/10: **0,0027 USD** thật (R2, usage log). Trần 8.2: 0,5 USD — đã dùng 0,0369 + 0,0027 = **0,0396 USD**. K3 trần 0,20 USD (đã duyệt).

## 5. Giới hạn

- Bộ thử nhỏ (40 câu có đoạn đúng, 88 câu dev chính) ⇒ nhiều "chưa rõ" / NOT RUN là kết quả hợp lệ; đoạn đúng do agent gắn (User duyệt ~10 câu).
- Kết luận dựa judge Claude là **tạm** tới khi có B0 (User đọc cặp mù).
- Mục tiêu sản phẩm + yêu cầu phi chức năng chưa có số ⇒ thước tạm = Completeness / Accuracy (judge) + sàn closed-world.

## 6. Bước tiếp (phiên sau)

1. A hỏi lại quyền phiên; **B review report R2** trước (B53, 0 USD), rồi **B chạy K3** (B54: plan `0a6370204c7d`; nhánh `p82-k3`; ≤ 0,20 USD, con tầng tìm 0,08 /
   lượt sinh 0,12); C review K3, viết plan R1.
2. Report R2 (`git show origin/p82-r2:report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r2_implementation.md`).
3. Theo kết quả K3: thắng ⇒ tìm cách nhanh / rẻ hơn rồi trình User (thêm một lần gọi API / câu); thua ⇒ ghép / kết luận đợt.
4. R1 (`none`) sau cùng — plan mới, luật (a).
5. User: mục tiêu sản phẩm (4 câu `Project_Status.md` §1), Q2 (test = "không làm hỏng"), B0.
6. Hướng mở đợt sau: mở rộng bộ câu tự nhiên (R3, B42: câu tự nhiên không lợi từ context 10); R2 chỉ khi có cách chặn dạng lỗi câu 160 được kiểm trước.
