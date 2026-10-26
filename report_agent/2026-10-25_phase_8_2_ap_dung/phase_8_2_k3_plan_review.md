# Review: plan Phase 8.2 §10 — K3, `gpt-6-luna` xếp lại pool 30 → top-10

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 2 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-b5`)
Date: 2026-10-26 22:17 +0700 (`date`)
Bản được kiểm: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3_plan.md` sha `ae2b94d35c84` (B, untracked)
Căn cứ: đúng mục "Căn cứ để review" của plan, gồm:
1. spec §10.2–§10.4 bản `cd910c4c4169`;
2. K1 report §4–§5 (`origin/p82-k1` `870a5d5`, có tồn tại);
3. G4 §4.2 / §5 + `g4_rerank.py:63-96`;
4. B42 §3.4.

Tính lại từ dữ liệu plan cho phép, `uv run`, chỉ đọc, 0 USD. C không dùng tin nhắn của B. Câu A trả lời ở plan §7 được coi là quyết định của A.

## 1. Phạm vi đã review

Toàn bộ plan: lớp bài toán, đổi một thứ, mốc M1 / M2, harness, YAML, luật giữ, cỡ mẫu, tiền / trần, dừng, §7. Đối chiếu với spec §10.2
(luật (i), sàn, Holm, đo tốc độ theo khâu, chất lượng trước) và dòng K3 ở §10.3.

## 2. Findings

Không có blocker, không có major.

### m-1 (minor) — Chưa ghi trước `max_output_tokens` cho luna xếp 30 đoạn

- **Vị trí:** plan §3 ("dùng lại nguyên `g4_rerank.luna_rank`") và §5.
- **Bằng chứng:** `luna_rank(client, model, max_output_tokens, …)` (`g4_rerank.py:74`) nhận trần token ra làm tham số. 8.1 truyền
  `answer_max_output_tokens` (`g4_rerank.py:186`), bằng **2048** ở `811d25d` (`settings.yaml:50`). Ở 8.1, với 10 đoạn, luna ra trung bình
  300,8 token, **tối đa 541** (`a_luna_plain.jsonl`, C tính lại), gồm cả phần suy luận. Với 30 đoạn, hoán vị dài gấp 3 và phần suy luận có thể
  dài hơn. Nếu chạm trần thì `status != completed`, `luna_rank` báo lỗi, và theo sàn §4 / §6.3 K3 dừng vì lý do kỹ thuật, không phải vì chất
  lượng.
- **Tiêu chí đóng:** plan ghi giá trị `max_output_tokens` dùng cho K3 (2048, lấy như 8.1) và thêm dòng theo dõi "token ra luna max" ở pilot.
  Nếu muốn đổi trần thì phải ghi **trước** pilot, không đổi sau khi thấy lỗi.

### m-2 (minor, số) — p95 `rerank_ms` 8.1

- Plan §5 ghi "p95 5,3 s". C tính từ `a_luna_plain.jsonl` ra **5,19 s** (p50 3,49 s đúng). Đây chỉ là khác cách làm tròn hoặc khác cách tính
  percentile, không đổi gì.
- **Tiêu chí đóng:** ghi 5,2 s, hoặc ghi rõ cách tính.

## 3. Đã kiểm, đạt

- **Đổi đúng một thứ:** chỉ thêm bước luna xếp lại 30 đoạn sau RRF. Pool 30, `rrf_k` 60, context 10, prompt sinh giữ nguyên. "Pool 100 + luna"
  tách ra plan riêng vì đổi hai thứ. Khớp A §7.1.
- **Trần tính lại** (`b42_per_case.jsonl`; câu thiếu ở context 10 mà mọi fact thiếu đều trong pool 30, bỏ fact thước đo):
  - dev **9** (17, 38, 48, 67, 70, 85, 156, 159, 167); test **3** (20, 95, 130). Khớp plan.
  - Mốc `base_dev.jsonl`: 22 / 40 câu đủ. Khớp con số "sàn đo trên cả 22 câu đang đủ".
- **Chỉ số quyết + Holm:** họ {K1 p 0,798, K3}, Holm step-down ⇒ K3 cần p < 0,025.
  - Trên vector ±1, n 40: 5 / 0 cho p 0,008, 4 / 0 cho p 0,026 (C38).
  - Thua bất kỳ là phạm sàn, nên "≥ 5 thắng / 0 thua" đúng là ngưỡng.
  - Luật hai lượt (thắng phải ổn định, thua tính ở bất kỳ lượt nào) là cách xử lý nhiễu LLM chặt hơn A/A thông thường. Khớp A §7.3.
- **Sàn:**
  - 0 câu mất trên dev L1 + L2 + test;
  - 0 lỗi đầu ra luna, không thay bằng thứ tự RRF, không gọi lại (`luna_rank` trả `error` cho thiếu / lặp / id lạ / bị cắt / lỗi API —
    `g4_rerank.py:80-94`);
  - OOS 0 / 18; 0 lỗi 500.
  - Khớp spec §10.2.
- **Mức tụt tầng trả lời** (4 / 6, 4 / 5, +1 / +1, citation v2 +2, `output_tokens` sinh +20 %): khớp spec §10.2 và bảng A/A ở plan K1 (C đã tính lại
  độc lập ở C41).
- **Tốc độ / tiền:** K3 thêm một lần gọi API, nên biết trước là không đạt "không tốn thêm". Plan ghi sẵn "trình User kèm số", đúng spec §10.2 luật
  (i). `rerank_ms` và USD đầu–cuối chỉ theo dõi.
- **Số 8.1 làm căn cứ ước** (C tính lại): token vào TB 1.428,4; ra TB 300,8; USD 0,000293 / lần; 0 / 30 lỗi. Khớp plan.
- **Tiền:**
  - Tầng tìm 95 lần × ~0,0006 ≈ 0,057, sát trần con 0,06. Có luật dừng sau pilot (§6.2) nên chấp nhận được.
  - Bước 5: 121 × 0,0006 + sinh ≈ 0,113.
  - Tổng ≈ 0,17 ≤ 0,20. Trong trần 8.2.
- **Phát lại thứ tự luna đã ghi ở lượt sinh:** đúng `run-experiment` §3.5 (đo khâu **sau** bằng đầu ra model đã ghi thật). Plan ghi rõ câu nào phát
  lại, và dùng thứ tự L1.
- **Harness:** chỉ thêm `k3.py`, dùng lại `k1.py` / `g4_rerank.luna_rank` / `answer_case` qua lớp bọc retrieval kiểu `DocOrderService`. Từ chối
  ghi đè; không sửa production. M2 so với `base_dev.jsonl` (tất định).

## 4. Cách người kiểm tính lại

`uv run python -` (inline, chỉ đọc):
- thống kê `data/phase_8_1/g4/a_luna_plain.jsonl` (token vào / ra / max, USD, `rerank_ms` p50 / p95, lỗi);
- trần dev / test từ `b42_per_case.jsonl`;
- số câu đủ của `data/phase_8_2/k1/base_dev.jsonl`;
- đọc `g4_rerank.py:55-100` và `settings.yaml` ở `811d25d`.

## 5. Giới hạn

- `k3.py` chưa có, nên C mới chỉ kiểm thiết kế.
- Ước token 30 đoạn (≈ 4.000 vào, 350–600 ra) là *suy ra*. Pilot sẽ đo thật; m-1 lo phần trần token ra.

## 6. Decision

**ready_for_user_confirmation:** m-1 nên sửa trước khi A ghi sha, vì chỉ thêm một con số và một dòng theo dõi. m-2 tùy B. Sửa xong ⇒ sha mới ⇒ A
duyệt. C không cần kiểm lại nếu chỉ đổi đúng hai chỗ này; B báo rõ diff cho A.
