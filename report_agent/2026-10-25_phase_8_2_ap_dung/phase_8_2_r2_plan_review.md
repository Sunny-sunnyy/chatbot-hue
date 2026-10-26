# Review: plan Phase 8.2 §10 — R2, trả lời phần có căn cứ (E1b)

Decision: **changes_requested** (0 blocker / 1 major / 2 minor)
Người kiểm: B (Claude Opus 5.5, `hue-rag-23`)
Date: 2026-10-26 22:00 +0700 (`date`)
Bản được kiểm: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r2_plan.md` sha **`61a6aa78c6b8`** (C, chưa commit)
Căn cứ dùng: đúng mục "Căn cứ để review" của plan: spec §10.2–§10.4 (bản `09e8f3932ede`); plan E1 §2, §3, §6, §7; `phan_loai_loi_C.md` §3; K1
plan §4 (bảng A/A); `run-experiment` §1, §3, §4. Tính lại từ `data/phase_8_2/b1/`, `data/phase_8_1/g2/`. B không đọc STATUS / tin nhắn của C.

## 1. Phạm vi đã review

Toàn bộ plan (165 dòng): lớp bài toán, chữ E1b, giả định G1–G6, YAML, luật giữ, cỡ mẫu, cách chạy, tiền / dừng, trình User, bảng đối chiếu E1.
Từng tiêu chí được đối chiếu với spec §10.2 (luật (i), sàn, Holm), §10.3 (cỡ mẫu R2), §10.4 (tiền, R2 chờ User).

## 2. Findings

### M-1 (major) — Ngưỡng latency "+50 ms" ở khâu sinh không phân xử được với 30 câu

- **Vị trí:** YAML dòng `latency sinh … 30 câu dev, xen kẽ … max: "+50 ms"`; §2 "Vì sao latency đo trên 30 câu xen kẽ"; §3 bước 6.
- **Yêu cầu:** `run-experiment` §1 mục 6 — tính **cỡ mẫu trước khi chạy**. Nếu không đủ câu thì ghi trước, hoặc đổi câu hỏi thí nghiệm.
  Spec §10.2 luật (i) — latency thêm ≤ 50 ms / câu.
- **Bằng chứng** (B tính 22:0x từ `latency_ms` đã lưu; B1 ↔ G2.1a cùng đầu vào từng token, 120 câu dev):
  - chênh theo câu có trung bình +193 ms, **SD 808 ms**;
  - với n = 30, sai số chuẩn ≈ 148 ms, **nửa khoảng CI 95 % ≈ ±289 ms**, gấp gần 6 lần ngưỡng;
  - muốn nửa khoảng ±50 ms cần khoảng (1,96 × 808 / 50)² ≈ 1.000 lần gọi.

  Số này lấy từ hai phiên khác nhau. Trong cùng phiên, xen kẽ, có thể nhỏ hơn nhưng chưa ai đo, và độ dao động mỗi lần gọi provider vẫn còn.
- **Tác động:** 0,012 USD cho một phép đo mà kết quả "đạt" hay "trượt" +50 ms gần như do may. Nếu đọc số này như một tiêu chí, có thể ghi
  "đạt latency" sai (hoặc ngược lại) trong báo cáo trình User. Điều này đi ngược đúng ý User 22:0x: "để ý tốc độ".
- **Tiêu chí đóng** (C chọn, ghi trước; nếu đổi luật thì A / User chốt):
  - (a) Giữ 30 câu nhưng đổi vai thành **theo dõi**: ghi chênh trung bình **kèm CI 95 %**, và ghi rõ "độ phân giải ≈ ±0,3 s, không kết luận
    ±50 ms". Thêm một chỉ số đo được thay cho latency: **`output_tokens` theo câu (R2 − mốc) trên 120 câu dev** (không tốn thêm tiền, có sẵn
    trong usage). Latency khâu sinh tăng theo token ra. Ngưỡng do A ghi; ví dụ `output_tokens` TB ≤ +20 %, khớp mức USD.
  - Hoặc (b) chuyển câu hỏi cho A / User: ngưỡng "+50 ms / câu" của luật (i) viết cho khâu tìm (ms), có áp nguyên cho khâu sinh (giây,
    provider dao động) không. R2 đằng nào cũng trình User (§5), nên hướng (a) không đổi luồng.

### m-1 (minor) — Pilot tiền là 12 câu OOS, không đại diện token ra

- **Vị trí:** §3 bước 1 ("lượt này cũng là pilot tiền"); §4 "pilot vượt ước > 50 % ⇒ dừng".
- **Bằng chứng:** OOS ở mốc B1 bị từ chối 12 / 12. Câu từ chối ngắn, nên token ra thấp hơn câu trả lời một phần. Token vào thì như nhau
  (context 10). Ước tiền từ pilot OOS sẽ **thấp** hơn thật, và rủi ro vượt ước dồn vào phần sau.
- **Tiêu chí đóng:** tính lại ước tiền sau bước 2 (7 câu trong phạm vi, có câu trả lời một phần), rồi mới chạy phần dev còn lại. Hoặc ghi
  "pilot tiền = bước 1 + 2 (19 câu)".

### m-2 (minor) — `paired_stats` gọi theo chữ ký giá trị, không phải theo lượt

- **Vị trí:** YAML `fn: "full_corpus_eval.paired_stats(base, r2, 'false_refusal') …"`.
- **Bằng chứng:** `full_corpus_eval.py:634` nhận `a_values, b_values` là **danh sách giá trị theo câu cùng thứ tự**, không nhận hai lượt.
  `false_refusal` nằm trong `LOWER_IS_BETTER` (`:58`), nên thắng / thua đúng chiều.
- **Tiêu chí đóng:** ghi `paired_stats([base[i].refusal for i in dev_main], [r2[i].refusal for i in dev_main], "false_refusal")`. Chỉ sửa chữ
  để người viết harness không truyền nhầm.

## 3. Đã kiểm, đạt

| Mục | Kiểm | Kết quả |
|---|---|---|
| Đổi một thứ, chữ E1b ghi trước | so với khối chữ trong plan E1 §3 | **nguyên văn**; cách thay `replace` + `assert` như P1 |
| G1 câu từ chối mốc | `b1_{dev,test}` + `keep_realism(main)` bỏ OOS | dev chính 88: **[48, 67, 68, 113, 120, 167, 168]**; test chính 41: [136] ✓ |
| G2 trần 5, 120 / 168 = 0 fact | `phan_loai_loi_C.md` §3; chéo với B42 (`b42_per_case`): 120, 168 `top10_gold_frac` = 0 ở mốc | ✓ khớp hai nguồn |
| Cỡ mẫu | `bootstrap_mean_diff` (10.000, seed 20261024), n 88 nhị phân | 5 / 0 p **0,0128** (× 2 = 0,026 qua); 4 / 0 p **0,0312** (× 2 trượt) ✓ |
| Sàn | spec §10.2 | OOS 0 / 18; 120 / 168 vẫn từ chối; 0 lỗi 500 / kỹ thuật ✓ |
| Holm | spec §10.2: họ {R2, R3} cố định | ✓ (p × 2, dù R3 có chạy hay không) |
| Mức tụt luật (i) | spec §10.2 + A/A (bảng K1 plan §4, B tính lại khớp) | dev C / A ≤ 4; test C ≤ 6, A ≤ 5; từ chối test ≤ +1; citation v2 ≤ +2, tính lại cho cả hai lượt; USD ≤ +20 % ✓ |
| Mốc + chấm cùng lượt mù | `run-experiment` §3.1, §3.6 | kiểm tất định `top_chunk_ids` / `context_sources` 120 / 120; B1 chấm lại cùng lô ✓ |
| Tiền | spec §10.4 | ước 0,052, trần 0,06 (A đã trả lời Q2), trong trần 8.2 ✓ (xem m-1) |
| Trình User / hợp đồng Phase 6 §10 | spec D4, §10.4 | R2 luôn chờ User; file đọc private; kết luận tạm tới B0 ✓ |
| Theo dõi rủi ro G5 (rào thêm ở câu đủ) | P1 8.1: 3 / 5 câu đủ bị giảm Completeness | có dòng watch đếm máy + 3 câu mẫu cho User ✓ |

## 4. Cách người kiểm chạy lại

Từ `backend/`, `HF_HUB_OFFLINE=1 uv run python -` (inline, chỉ đọc, 0 USD):
- `keep_realism(…, "main")` trên `b1_{dev,test}` ⇒ danh sách từ chối;
- `bootstrap_mean_diff` cho vector −1 × k (k = 4, 5), n 88;
- chênh `latency_ms` theo câu B1 ↔ G2.1a trên 120 câu dev ⇒ trung bình, SD, nửa khoảng CI với n 30;
- `grep` chữ E1b trong plan E1 §3; đọc `paired_stats` (`full_corpus_eval.py:634-653`).

## 5. Giới hạn

- SD latency lấy giữa hai phiên. SD trong cùng phiên (thiết kế xen kẽ của plan) chưa đo, có thể nhỏ hơn. Dù nhỏ đi một nửa, nửa khoảng CI với n
  30 vẫn ≈ ±145 ms, gấp gần 3 lần ngưỡng.
- B chưa xem harness `r2.py` (chưa có, ngoài căn cứ).

## 6. Decision

**changes_requested** — sửa M-1 (chọn (a) hoặc (b), ghi trước). m-1, m-2 sửa cùng lượt. Ra sha mới ⇒ B kiểm phần sửa ⇒ A ghi "duyệt bản sha".
Phần còn lại của plan chặt và khớp spec.
