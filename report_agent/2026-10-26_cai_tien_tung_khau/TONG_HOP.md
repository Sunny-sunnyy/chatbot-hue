# TỔNG HỢP đợt "tìm hướng tốt hơn từng khâu" — **ĐÓNG 27/10/2026** (User chọn (1): chốt đợt, chatbot không đổi)

Người viết: A (`hue-rag-2d` 26/10, `hue-rag-5f` 27/10) · cập nhật 11:16 27/10/2026 (`date`; bản trước 22:31 26/10/2026) · Đợt mở 20:0x 25/10 (User). Từ 21:3x 26/10 đợt này **là Bước 2 của
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
| 27/10 08:47 | User | Quyền phiên như tối 26/10 (K3 ≤ 0,20 USD; API ≤ 1 USD); duyệt W21–W23, Q2 §10.6 (test = "không làm hỏng"); mục tiêu sản phẩm: **đồ án tốt nghiệp, xem như sản phẩm kinh doanh thật; người dùng = User, du khách, người dân**; yêu cầu phi chức năng chưa rõ ⇒ "so sánh, đánh giá, chỗ nào tối ưu được thì tối ưu" |
| 27/10 08:5x | A | Đề xuất thứ tự lỗi nặng → nhẹ: nói chắc sai / bịa > trả lời câu ngoài kho > thiếu ý > từ chối nhầm (chờ nghiên cứu ChatGPT để chốt); viết yêu cầu nghiên cứu mục tiêu sản phẩm (C47 đối chiếu code: 1 sai, 2 hiểu lầm, 4 thiếu — W19 có tác dụng) |
| 27/10 09:0x–09:3x | A | Đóng R2 (B53), K3 (C49), R1 (B58) — cả ba kém hơn; gác R1 + luật kiểm sau sinh (C51) |
| 27/10 09:1x–09:5x | A | K3b: tách nhánh n (`none`) / m; nới sàn "hoán vị" thành mức tụt có trần (ghi trước); dời trần con n → m (tổng 0,10 giữ) |
| 27/10 10:1x | A | Sàn "câu 120 phải từ chối" (A thêm, không kiểm nhãn) làm dừng lượt answer K3b-m bản 2 dù câu trả lời đúng đáp án ⇒ trình User |
| 27/10 10:2x | User | Chọn (1): lượt mới, 120 về "theo dõi" như K3 plan gốc (ghi "đổi sau khi thấy số"); không sửa nhãn |
| 27/10 11:0x | User | Sau K3b-m (kém hơn theo luật T3): chọn (1) **chốt đợt**, sang B0 + merge context 10 + tính năng mới |

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
| K3 | luna xếp lại pool 30 → top-10 | **kém hơn** — phạm sàn lỗi đầu ra 1 / 40 (thứ tự thiếu một đoạn); theo dõi 39 câu: 9 thắng / 0 thua; rerank p50 5,6 / p95 8,6 s | 0,0251 | `p82-k3` `80e7329`; `phase_8_2_k3_review.md` (C49 ready) |
| K3b-n | luna chọn 10 / 30, `none` | **kém hơn** — lỗi kỹ thuật (chữ thừa sau JSON dù structured output strict); pilot 9 / 10 như m, rerank p95 2,1 s | ≈ 0,012 (0,0035 log + ước ≈ 0,0087 — token vào thật của 30 câu l1_rest, ~21 lần; cận trên ≈ 0,018 = đủ 30 lần + 1 lần lỗi ra tối đa 2048 token; cận tuyệt đối 0,048) | `p82-k3b` `806e8ad`; `phase_8_2_k3b_review.md` (C52 ready) |
| K3b-m | luna chọn 10 / 30, suy luận mặc định | **tầng tìm tốt hơn (tạm** — nhãn agent, test một lượt, chưa B0**)** (đoạn đúng trong context 22 → 31 / 40, 9 / 0 ổn định 2 lượt, CI [+0,10; +0,35]; test 7 → 10, 0 mất); **khâu trả lời kém hơn theo luật** (T3: 5 câu Completeness tụt > 4; test NOT RUN). Chỉ báo: Completeness +0,216 [+0,023; +0,443], Accuracy +0,250, Relevance +0,227; từ chối nhầm 7 → 2 / 88; sàn OOS / 500 đạt. Giá: e2e p50 6,5 / p95 9,1 s (gọi đồng thời 4; mốc chỉ latency sinh 1,8 / 3,3 s, đo 26/10 — khác phiên), ≈ 3,8× USD / câu | 0,0557 (tầng tìm) + 0,0749 (trả lời) | `p82-k3b` `a6f609c`; `phase_8_2_k3b_m_answer_review.md` (C54 ready) |
| R4 | thước "số trong câu trả lời có trong nguồn được trích" | xong — **chỉ là danh sách đọc lại** (ngoài mẫu đúng 0 / 5) | 0 | `2c7ecfd`; `phase_8_2_r4_review.md` (B47 ready) |
| R2 | trả lời phần có căn cứ (E1b) | **kém hơn** — phạm sàn bước 1 (1 / 12 câu ngoài kho bị trả lời, cùng dạng P1 8.1); **hướng gác** | 0,0027 USD (log) | `origin/p82-r2` `aec9ab8`; `phase_8_2_r2_review.md` (B53 ready) |
| R3 | prompt "nêu đủ chi tiết" | **NOT RUN** — chỉ 6 câu có thể đổi, dưới cỡ mẫu tính trước | 0 | `phase_8_2_r3_plan.md` + `_review.md` (giữ hồ sơ) |
| R1 | `reasoning_effort = none` | **kém hơn** — dừng ở pilot: câu 168 "trả lời vòng" (một câu có `[n]` cùng chủ đề + "nguồn không nêu…" không citation); theo dõi: token ra ~0,72×, USD ~0,95× | 0,0049 | `p82-r1` `63a472f`; `phase_8_2_r1_review.md` (B58 ready) |
| E2 | sửa thiếu `[n]` | **NOT RUN** — validator v2: mốc 0 lỗi | 0 | spec §10.3 |

**Cách làm / rào bằng máy (governance, review chéo):** hook pre-commit quét dòng thêm mới trùng Golden / kho / câu kín (`.githooks/overlap_scan.py`,
W16 + câu kín; C 2 vòng, B 2 vòng); luật W14 + W18, W17, W19, W20; luật chung §7 thêm 3 nguyên tắc User (chất lượng trước; hiệu suất = tiền + tốc độ;
đo theo mục tiêu sản phẩm cuối); `Project_Status.md` §1 "Mục tiêu sản phẩm" (đã chốt + câu chờ User).

**Đo hiện trạng (0 USD):** C48 — mốc B1 dev 68 câu có số: **0 câu sai số** thấy được (4 cờ = phép tính đúng); C51 — luật kiểm sau sinh bắt 160 / 168
(sau khi chỉnh trên chính 2 câu đó), 0 cờ ở chatbot hiện tại, không tách được "lạc đề" với "một phần có ích" ⇒ gác; B61 — nhãn đoạn đúng chỉ đánh dấu
một chỗ / thông tin, kho diễn đạt lại ở chỗ khác ⇒ thước tầng tìm đếm thiếu ít (1 / 55 lặp nguyên văn; kết luận tầng tìm không đổi theo cả cách đếm loose).

**Chatbot không đổi** (vẫn context 5, chưa NFC, reasoning `medium` mặc định). Qdrant 1 collection 8.459, không ghi.

## 4. Tiền

Phiên tối 26/10: **0,0027 USD** thật (R2). Phiên 27/10: **≈ 0,173 USD** (K3 0,0251 + R1 0,0049 + K3b log 0,0592 + ước ≈ 0,0087 + K3b-m answer 0,0749; cận trên ≈ 0,178).
Trần 8.2: 0,5 USD — đã dùng **≈ 0,212 USD** (cận trên ≈ 0,218). Trần phiên 1 USD.

## 5. Giới hạn

- Bộ thử nhỏ (40 câu có đoạn đúng, 88 câu dev chính) ⇒ nhiều "chưa rõ" / NOT RUN là kết quả hợp lệ; đoạn đúng do agent gắn (User duyệt ~10 câu).
- Kết luận dựa judge Claude là **tạm** tới khi có B0 (User đọc cặp mù).
- Mục tiêu sản phẩm đã có (User 27/10) nhưng yêu cầu phi chức năng chưa có số ⇒ thước tạm = Completeness / Accuracy (judge) + sàn closed-world; yêu cầu
  nghiên cứu ChatGPT (thời gian chờ, tiền / câu, mức nặng lỗi) chưa gửi.
- Luật T3 "đếm câu tụt ≤ A/A + 3" (A/A của mốc) phạt nặng biến thể đổi context ở gần mọi câu (K3b-m: TB tăng có CI > 0 nhưng 5 câu tụt) — câu hỏi luật
  nhận cho loại biến thể này **để cho lần sau** (C54), không áp ngược.
- 3 kết luận "kém hơn" hôm 27/10 do lỗi kỹ thuật / sàn (K3, K3b-n, R1) — kết quả hợp lệ; 1 dừng do sàn A đặt sai (K3b-m answer bản 2), đã chạy lại theo User.

## 6. Bước tiếp

1. **B0** — User đọc cặp mù (`data/phase_8_2/b0/nhan_xet_user.md`, 20 câu, ~30–45 phút). Chặn merge B1.
2. Sau B0: merge B1 (context 10 + NFC, nhánh `p82-b1`; B63 thử rebase lên `main` 27/10) + luật dừng B0 + cổng ổn định ⇒ chatbot lên context 10.
3. Phase 8.2 còn: mốc cuối (câu kín, User quyết mở) ⇒ đóng 8.2 ⇒ tính năng mới (User 27/10: "xong sớm thì mới bổ sung được tính năng mới").
4. Hướng mở (hồ sơ, không làm khi chưa có quyết định mới): K3b-m / K3c (bản nhanh `none` chịu chữ thừa) khi có luật nhận cho biến thể đổi context +
   yêu cầu thời gian chờ có số; streaming từng câu đã kiểm (nghiên cứu 26/10 C5); mở rộng bộ câu tự nhiên; sửa nhãn đoạn đúng "một chỗ / thông tin".
