# C37 — Bản nháp phần khâu trả lời cho tài liệu thiết kế đợt cải tiến

Người làm: C (Claude Opus 5.5, `hue-rag-b5`) · 2026-10-26 21:21 +0700 (`date`) · Việc: `CURRENT_HANDOFF.md` dòng C37 (A giao 21:17) ·
**0 USD**. C chỉ đọc report và tính lại từ file G2 đã có (`data/phase_8_1/g2/*.jsonl`, `uv run`); không gọi API, không chạy thí nghiệm mới.
Đây là **đầu vào** cho tài liệu thiết kế của A, cùng khuôn với B43 (`de_xuat_khau_tim_B.md`), không phải plan để duyệt.

## 1. Bốn điều cần biết trước

1. **Ở mốc context 10, lỗi do riêng khâu trả lời là phần nhỏ** (C36 `phan_loai_loi_C.md` §1). Trên 88 câu dev chính, Completeness mất
   46 điểm:
   - 20 điểm (5 câu) do từ chối khi context có một phần fact;
   - 9 điểm (9 câu) do trả lời gọn, bỏ chi tiết có sẵn;
   - 17 điểm do thiếu bằng chứng, khâu trả lời không cứu được.

   Trần của mọi biến thể khâu trả lời khoảng **+0,33 Completeness** (29 / 88), và chỉ đạt khi sửa được cả hai nhóm.
2. **Mọi số 8.1 về khâu trả lời đều đo ở context 5** (G2.2 P1, G2.4 mức suy luận). Chỉ G2.1a đo ở context 10. Tín hiệu cũ không chuyển
   thẳng sang mốc mới: ở context 10 chỉ còn 7 câu từ chối, so với 13 ở context 5. Trong 7 câu đó, **2 câu từ chối đúng** (120, 168: context
   không có fact nào), nên phần còn cứu được là **5 câu**.
3. **Luật nào áp cho biến thể nào:**
   - Luật (a) (giữ chất lượng, rẻ / nhanh hơn rõ) hợp với **R1** (mức suy luận `none`).
   - Luật (i) (chất lượng tăng vượt nhiễu, ≤ +50 ms, **0 USD thêm**) áp cho R2 / R3. Nhưng hai biến thể này làm câu trả lời dài hơn, nên
     **tốn thêm chút ít** (P1 ở context 5: USD / câu ×1,11, p95 +36 %). **Cần A / User nói rõ** "0 USD thêm" nghĩa là không thêm lần gọi
     API, hay đúng là không thêm đồng nào. Hiểu theo nghĩa sau thì R2 / R3 luôn rơi vào nhánh "tốn hơn ⇒ trình User".
4. **Luật (a) "Completeness ≥ −0,1" cần nói rõ đo bằng gì.** Với cùng một số câu tụt, đo bằng **chênh trung bình** và đo bằng **cận dưới
   CI 95 %** cho kết quả khác hẳn (tính bằng `bootstrap_mean_diff` của harness, mỗi câu tụt 1 điểm):

   | Tập | Số câu tụt 1 điểm (0 câu tăng) | Chênh TB | CI 95 % | Qua nếu xét chênh TB | Qua nếu xét cận dưới CI |
   |---|---:|---:|---|---|---|
   | dev 88 | 4 | −0,045 | [−0,091; −0,011] | ✓ | ✓ |
   | dev 88 | 5 | −0,057 | [−0,114; −0,011] | ✓ | ✗ |
   | dev 88 | 8 | −0,091 | [−0,159; −0,034] | ✓ | ✗ |
   | test 41 | 2 | −0,049 | [−0,122; 0,000] | ✓ | ✗ |
   | test 41 | 4 | −0,098 | [−0,195; −0,024] | ✓ | ✗ |

   Xét cận dưới CI thì trên test chỉ cần **2 câu tụt** là trượt. Nhiễu A/A ở dev đã là 1 câu tụt (B1 §4). C đề xuất: **chênh TB ≥ −0,1
   và số câu tụt ≤ A/A + 3**. A / User chốt.

## 2. Nhóm câu C36 mà khâu trả lời nhắm tới (dev chính 88)

| Nhóm (C36) | Câu | Điểm Completeness mất |
|---|---|---:|
| P. từ chối khi context có một phần fact | 48, 67, 68, 113, 167 (multi_source 4, comparative 1) | 20 |
| U. trả lời gọn, bỏ chi tiết có trong context (điểm 4) | 28, 38, 41, 51, 65, 66, 93, 141, 173 (conditional 5) | 9 |
| S. nhận định tự suy ra sai / citation lệch nhẹ | 155; 51 | (Accuracy 1) |
| — từ chối đúng, thiếu bằng chứng (không đụng) | 120, 168 — **phải vẫn từ chối** | — |

## 3. Biến thể (không ghi Qdrant, không đổi khâu tìm)

| # | Biến thể (đổi đúng một thứ) | 8.1 / rà code đã đo gì | Nhóm nhắm · trần dev | Luật | Tốn (ước) | Rủi ro |
|---|---|---|---|---|---|---|
| R1 | **Mức suy luận `none`** (gửi `reasoning_effort="none"`; hiện không gửi, nghĩa là `medium`) | Context 5, dev 120: Completeness **+0,136** [+0,034; +0,261], p Holm 0,031; từ chối nhầm 13 → 4; USD / câu **0,91×**; p50 1,53 s so với 1,66 s, p95 2,07 s so với 2,79 s; token ra 54 so với 79 (`phase_8_1_g2_implementation.md:125`, tính lại từ `g24_none.jsonl`). Bị loại vì citation 4 → 8 theo định nghĩa cũ; định nghĩa v2 là **0 → 2**, nằm trong nhiễu, nên **lý do loại đã hết** (`sua_3c_citation_v2.md:36`, `:52`). Lợi chỉ ở câu `capability_only`; nhóm natural (45 câu): −0,022 [−0,111; +0,044] (`:129-131`) | P (giảm từ chối) · 5 câu; có thể **làm U nặng thêm** vì câu trả lời ngắn hơn 31 % | **(a)** | dev + test 176 × ≈ 0,000192 ≈ **0,034 USD** (ở context 10 tiền chủ yếu nằm ở token vào, nên chỉ tiết kiệm ~6 %, *suy ra*) | Câu trả lời ngắn ⇒ under-answer tăng; từ chối đúng (120, 168) có thể thành trả lời |
| R2 | **E1b trả lời phần có căn cứ** (thay đúng câu luật từ chối; chữ ghi trước ở plan E1 §3) = **E1 của spec 8.2** | P1 context 5: từ chối nhầm 13 → 1, nhưng **phạm sàn**: 2 câu out_of_scope bị trả lời (`phase_8_1_g2_implementation.md` §4.2). Plan E1 (`phase_8_2_e1_plan.md` sha `f86240418ca1`) đã phân tích vì sao P1 phạm sàn và viết chữ E1b chặn hai dạng lỗi đó. Ở context 5, P1 cứu 6 / 7 câu đang còn từ chối ở context 10 (plan E1 `:40`, `:75`) | P · **5 câu** (plan E1 ghi 7; C36 cho thấy 2 câu là từ chối đúng) | **(i)** + User duyệt (đổi hợp đồng Phase 6 §10, spec 8.2 D4) | ≈ 0,00022 × 176 ≈ **0,04 USD** (plan E1 §8); token ra +25 %, USD ×1,11 so mốc | Rào thêm "nguồn không có…" ở câu đã đủ (P1: 3 / 5 câu tụt); câu ngoài phạm vi bị trả lời |
| R3 | **Thêm một câu prompt "nêu đủ các chi tiết có trong bằng chứng liên quan tới câu hỏi"** (đặt trước luật từ chối; chữ ghi trước trong plan) | **Chưa đo.** P2 (G2.2) đi chiều ngược lại ("đoạn văn ngắn"): không khác, token ra −12 % (`phase_8_1_g2_implementation.md` §4.2) | U · 9 câu, mỗi câu tối đa +1 (+0,10) | **(i)** | ≈ 0,036 USD; token ra tăng (chưa ước được, pilot) | Lan man / tự suy ra, như câu 155 (Accuracy giảm); Relevance giảm |
| R4 | **Kiểm citation bằng code** ở chế độ **theo dõi**, không chặn: mọi con số / giá / giờ trong câu trả lời phải có trong đoạn được trích | C36 thử tay trên 20 câu trả lời: 5 câu bị cờ, 2 đúng lỗi (155 tính sai, 51 năm nằm ở đoạn không trích), 3 nhầm (30 số tự tính đúng, 143 số lấy từ câu hỏi, 93 số viết khác dạng "3–5" / "3 đến 5") ⇒ precision 2 / 5 (`phan_loai_loi_C.md` §5). Báo cáo ChatGPT C1 / P0 đề xuất chế độ "cảnh báo", không chặn | không tăng điểm; là **thước** để bắt `unsupported claim` khi chạy R1–R3 | thước đo, không phải biến thể | 0 USD, chạy trên file đã có | Báo nhầm số tự tính / số trong câu hỏi / số viết khác dạng; cần bỏ số có trong câu hỏi và chuẩn hóa khoảng số trước khi đếm |
| — | E2 (spec 8.2: sửa lỗi thiếu `[n]`) | Theo định nghĩa v2, mốc G2.0 và B1 đều còn **0** lỗi citation (`sua_3c_citation_v2.md:59`) | không còn câu để nhắm | — | 0 | **Đề xuất NOT RUN** theo luật bỏ sớm (không đủ câu để CI > 0) |

**Không đề xuất** (đã đo hoặc lợi nhỏ):
- `low`: v2 vẫn kém hơn, 0 → 4 câu lỗi citation (`sua_3c_citation_v2.md:37`).
- `high`: không khác, USD ×1,11.
- Xếp context theo tài liệu (G2.1b): không khác.
- Khớp nhãn `[Nguồn n]` ↔ `[n]` (C-09): lỗi v2 đã bằng 0.
- Streaming (C5): đổi hợp đồng, chỉ làm khi độ trễ thành vấn đề.
- Tách câu hỏi (C3): thuộc khâu tìm (đổi truy vấn), để B / A xếp cùng B43.

**Trùng với spec 8.2:**
- R2 **chính là E1**. Plan E1 phải sửa trước khi chạy, cụ thể:
  - mốc = B1 rebase `811d25d`;
  - dùng `paired_stats` và `false_refusal` (gói 3a);
  - citation đếm theo v2;
  - trần cứu được = 5 câu, không phải 7.
  Sửa xong là sha mới, B review lại.
- E2 → NOT RUN, như trên.
- E3a / E3b là khâu tìm, nằm ở B43: E3a ≈ V1 / V2 (pool rộng); E3b ≈ V3 (luna trên pool).
- R1, R3, R4 **không có trong spec 8.2**.

## 4. Tiêu chí đề xuất ghi trước (A chốt trong spec)

```yaml
baseline: chatbot context 10 + NFC sau B1 (p82-b1 811d25d); câu trả lời mốc data/phase_8_2/b1/b1_{dev,test}.jsonl
compare: mỗi biến thể so với CÙNG mốc B1 (luật User 20:4x, không so nối tiếp); judge Claude chấm mốc + biến thể cùng lượt mù
unchanged: [corpus, chunker, embedding, retrieval dense_bm25_rrf, context 10, model gpt-6-luna, validator, judge prompt]
data: {split: split.json, dev: 120 (12 OOS), test: 56 (6 OOS), số chính: bỏ unnatural -> dev 88 / test 41 trong phạm vi}
noise_AA: {nguồn: phase_8_2_b1_implementation.md §4 (B1 ↔ G2.1a), completeness dev chính: 1/86/1, accuracy: 1/86/1,
           đổi từ chối: 0/176, citation v2: 0 vs 0, judge-only (G2.4): 2/88}
floors (mọi biến thể):
  - {oos_answered dev+test: 0/18}
  - {từ chối đúng 120, 168 vẫn từ chối}            # C36: context không có fact
  - {uncited_non_refusal (API trả 500): 0}
R1_none:  # luật (a)
  - {name: completeness dev chính, role: tolerance, rule: "chênh TB ≥ −0,1 VÀ số câu tụt ≤ A/A + 3"}   # §1.4, A chốt
  - {name: usd_per_case, role: decide, rule: "≤ 0,95 × mốc"}; {name: latency p50 sinh, role: decide (một trong hai), rule: "≤ 0,9 × mốc"}
  - {name: under-answer (số câu U của C36 tụt điểm), role: watch}
R2_E1b:   # luật (i) + User duyệt hợp đồng
  - {name: false_refusal dev chính, role: decide, rule: "paired_stats CI95 cận trên < 0 VÀ thắng − thua > 0 (A/A)", ceiling: 5 câu}
  - {name: completeness_losses / accuracy_losses, role: tolerance, max: 3}   # như plan E1 §4
R3_detail: # luật (i)
  - {name: completeness dev chính, role: decide, rule: "CI95 cận dưới > 0", ceiling: 9 câu × +1}
  - {name: accuracy_losses, role: tolerance, max: "A/A + 2"}; {name: relevance, output_tokens, latency p95, role: watch}
R4_meter: {kiểm thước trước: 5 ca C36 đã biết (2 lỗi thật, 3 báo nhầm); dùng làm chỉ số watch cho R1–R3}
```

**Cỡ mẫu** (tính trước bằng `bootstrap_mean_diff`, mỗi câu thắng / thua 1 điểm):
- **R3:** dev 88 cần **≥ 4 thắng / 0 thua** (CI [+0,011; +0,091]); 5 / 1 hay 6 / 1 thì CI chạm 0. Trần 9 câu nên đủ chỗ, nhưng hẹp.
- **R2:** cần ≥ 4 / 0 câu hết từ chối trên trần 5. Tính theo Completeness (mỗi câu cứu +4 điểm): 3 / 0 vẫn có CI [0; +0,318], phải 4 / 1
  mới qua. **Ghi trước: kết quả "chưa rõ" rất có thể xảy ra.**
- **R1 (luật a):** không cần thắng; chỉ cần không tụt quá mức ở §1.4, và rẻ / nhanh hơn. Ở context 5, USD là 0,91× và p50 0,92×, nên với
  ngưỡng 0,95 / 0,9 thì R1 sát ngưỡng ở context 10. Phải đo pilot.
- **Test 41:** quá nhỏ để CI cho kết quả "tốt hơn" (3 / 0 vẫn [0; +0,171]). Xác nhận trên test nên là **"không làm hỏng"** (sàn + tụt
  theo §1.4), như Q1 của plan E1. Lệch `run-experiment` §4, nên A / User cần chấp nhận.
- **Holm:** R1 / R2 / R3 có chỉ số quyết khác nhau (USD, từ chối, Completeness), nên mỗi biến thể là một họ riêng, không Holm chung.
  *Đề xuất*; A chốt.

## 5. Thứ tự C đề xuất

1. **R4 thước** (0 USD): viết hàm đếm (số trong câu trả lời ⊆ đoạn được trích, bỏ số có trong câu hỏi), kiểm trên 5 ca C36, chạy trên
   G2.1a / B1. Có thước trước thì R1–R3 mới bắt được `unsupported claim`.
2. **R1 `none`** (~0,034 USD): rẻ nhất; luật (a) rõ; tín hiệu 8.1 có sẵn. Pilot 10 câu đo USD / p50 trước. Chạy cả hai lượt dev + test
   trước khi quyết.
3. **R2 = E1b** (~0,04 USD): đòn bẩy lớn nhất (20 điểm) nhưng trần 5 câu. Plan E1 sửa theo §3, B review, A duyệt sha. Thắng thì vẫn trình
   User đọc mẫu.
4. **R3** (~0,036 USD): plan mới, chữ prompt ghi trước. Chỉ chạy khi R1 không làm U nặng thêm. Nếu R1 được nhận, R3 vẫn so với mốc B1
   theo luật User. Ghép R1 + R3 là cấu hình mới, cần thêm một lượt xác nhận.

**Tổng ước:** R1 + R2 + R3 ≈ **0,11 USD**, cộng pilot. Trong trần 1 USD / phiên; spec 8.2 còn 0,46 / 0,5. Judge = quota Claude.

## 6. Giới hạn

- Mọi tín hiệu R1 / R2 đo ở **context 5**. Trần nhóm P / U theo C36 là do **một người gắn nhãn**, chưa có người thứ hai kiểm.
- "Tiết kiệm ~6 %" của R1 ở context 10 là *suy ra* từ cơ cấu token (vào 1,3k / ra 77), chưa đo. Latency lấy từ harness
  (concurrency 4, mạng thay đổi): B1 so với G2.1a cùng cấu hình mà p95 đã khác 2,9 s / 4,0 s. Vậy ngưỡng latency của luật (a) cần ≥ 2 lượt,
  hoặc dựa vào token ra.
- R3 chưa có số nào. Chữ prompt phải ghi trước trong plan.
- Số tính lại ở §1.4, §3 (USD, p50 / p95, token ra) và §4: đoạn `uv run python` inline trên `data/phase_8_1/g2/{g20_baseline,g24_none,
  g24_low,g2_context10,g2_p1_partial}.jsonl` và `bootstrap_mean_diff` (seed 20261024). Không lưu file mới.
