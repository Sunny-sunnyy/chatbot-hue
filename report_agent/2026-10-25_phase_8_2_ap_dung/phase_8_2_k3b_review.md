# Review: Phase 8.2 §10 K3b — `gpt-6-luna` chọn 10 từ 30 đoạn RRF, nhánh n / m (report B59)

Decision: **ready_for_user_confirmation** — nhánh n **kém hơn** (sàn lỗi kỹ thuật), nhánh m **tầng tìm tốt hơn (tạm)** đúng tiêu chí ghi trước; 0 blocker / 0 major / 3 minor
Người kiểm: C (Claude Opus 5.5, `hue-rag-5b`) · Việc: C52 (A giao 27/10)
Date: 2026-10-27 10:04 +0700 (`date`)
Canonical guide: plan `phase_8_2_k3b_plan.md` bản 2 sha `57dad7150322` (A duyệt `765f45a`; C tính lại từ file: khớp); spec 8.2 §10.2 bản `cd910c4c4169`
Implementation report: `origin/p82-k3b` `806e8ad` — `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3b_implementation.md`

File này không chép câu hỏi, đáp án, nội dung kho hay đầu ra luna — chỉ `case_index`, số đếm, sha.

## 1. Phạm vi đã review

- **Git:** `git diff --stat 80e7329..origin/p82-k3b` = 3 file (`backend/experiments/phase_8_2/k3b.py` mới, `backend/tests/test_k3b_contract.py` mới, report). Không
  production, không `k3.py` / `g4_rerank.py`. `git diff --check` sạch. sha `k3b.py` = `658e381c8c37` (khớp report).
- **Code** `k3b.py` (đọc hết) + diff riêng `7c0467d..f4d3225`. Prompt `LUNA_TOP10_INSTRUCTIONS` = nguyên văn plan §1 (meta mọi lượt ghi `instructions_sha12`
  `4717583a1489`); `apply_contract` = plan §2 bản 2 (đúng 10 số khác nhau trong 1..30 ⇒ dùng; sai ⇒ nguyên top-10 RRF, không ghép); `compare` = luật hai lượt trên
  `context_gold_all`, sàn mất đoạn đúng ở context **và** top-10, Holm họ cố định `[K1 0,798, K3 1, nhánh này, nhánh kia]`; trần sai hợp đồng `MAX_VIOLATIONS = 4`
  đếm tuyệt đối cộng dồn theo nhánh (`arm_rows`; bản `.merged` bỏ trường `arm` nên không đếm hai lần — C đếm: 95 lần gọi nhánh m = 10 + 30 + 40 + 15).
- **Dữ liệu** `data/phase_8_2/k3b/`: sha 12 của 9 file JSONL + `tools/k3b_watch.py` khớp bảng report §4; 5 `.meta.json` lượt luna.
- **Không đọc:** câu test theo từng câu, câu kín, `.env`. Không dùng `k3b_watch.py` / `compare_m_*.json` của B để kiểm — tự tính (mục 3).

## 2. Findings

Không có blocker hoặc major.

### m-1 — "cận trên 0,0105 USD" của lượt `n_l1_rest` không phải cận trên chặt

- **Vị trí:** report đầu file ("cận trên 0,0105") và §4.2.
- **Bằng chứng:** 0,0105 = 30 lần × 0,000350 (USD / lần TB của pilot n). Lần gọi lỗi lại chính là lần model **viết thêm chữ** sau JSON, nên token ra của nó (và có
  thể của lần khác) lớn hơn 33 token của pilot. Cận chặt theo `max_output_tokens` 2048 và token vào lớn nhất của pilot (4.293): 30 × (4.293 × 0,1 + 2.048 × 0,5) / 1M
  ≈ **0,0436 USD** ⇒ cả K3b tệ nhất ≈ **0,103 USD**, sát / quá trần 0,10. *Suy ra*: thực tế gần ước 0,0074 hơn nhiều (một lần gọi lỗi, các lần khác như pilot).
- **Tác động:** không đổi kết luận; chỉ là ghi số tiền trung thực. Tổng 8.2 vẫn xa trần 0,5.
- **Tiêu chí đóng:** đổi chữ "cận trên" thành "cận trên nếu mọi lần như pilot", ghi thêm cận chặt ≈ 0,044; nếu cần số thật, User / A xem usage trên trang OpenAI
  cho khung 09:30:04–09:30:53 27/10.

### m-2 — bằng chứng lỗi kỹ thuật của nhánh n không nằm trong dữ liệu

- **Vị trí:** §4.2 (đoạn raw "…LunaTop10 format only." và thông điệp "Invalid JSON: trailing characters").
- **Bằng chứng:** harness `7c0467d` không ghi gì khi crash (không `n_l1_rest.jsonl`, không meta); report §6 ghi "không có dòng", nhưng không nói đoạn raw trích lấy từ
  đâu (C hiểu là output terminal).
- **Tác động:** kết luận "kém hơn" là hướng bảo thủ (dừng, không nhận lợi gì) nên không bị ảnh hưởng; nhưng người khác không tái lập được bằng chứng sàn từ `data/`.
- **Tiêu chí đóng:** ghi một câu "raw và thông điệp lỗi lấy từ output terminal lúc 09:30:53"; nếu còn bản output, lưu private vào `data/phase_8_2/k3b/` (không commit).

### m-3 — luật dừng pilot "sai hợp đồng ≥ 3 / 10" của plan §6.2 không có trong harness

- **Vị trí:** `k3b.py` `retrieval` chỉ dừng khi `violations > MAX_VIOLATIONS` (4).
- **Bằng chứng / tác động:** cả hai pilot có **0 / 10** sai hợp đồng ⇒ không ảnh hưởng lượt đã chạy. Với lượt sau (nếu có K3c), pilot 3–4 / 10 sẽ không tự dừng.
- **Tiêu chí đóng:** ghi trong report là luật này được kiểm bằng tay sau pilot (B đã đọc meta), hoặc thêm điều kiện vào harness ở biến thể sau. Không cần sửa cho K3b.

## 3. Cách người kiểm chạy lại thật

0 USD. Từ `backend/` working tree chính, script tạm `/tmp/c52_check.py` (`PYTHONPATH=. HF_HUB_OFFLINE=1 uv run python /tmp/c52_check.py`):
- **tính lại `context_gold_all` / `top10_gold_all` từ đầu** cho mốc (`data/phase_8_2/k3/base_{dev,test}.jsonl`) và mọi lượt m: lấy `context_chunk_ids` / `top_chunk_ids` →
  payload Qdrant (đọc, `g1_retrieval.load_payloads`) → `g1_retrieval.gold_coverage` trên đoạn đúng `bab707b9ab22`; so với trường đã lưu;
- thắng / thua / A/A, `bootstrap_mean_diff` + `holm_adjust` (seed 20261024, 10.000 vòng), Clopper–Pearson (`scipy.stats.beta`);
- tiền: tổng `luna.usd`, tính lại từ token (`cost_usd`), so `.meta.json`; giờ chạy từ meta.

Thêm: worktree tạm `/tmp/c52_wt` (detached `origin/p82-k3b`, đã gỡ) chạy `HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest
tests/test_k3b_contract.py -q` ⇒ **4 passed**. `git diff 7c0467d f4d3225`; `sha256sum` dữ liệu / plan / harness.

## 4. Kết quả quan sát — năm điểm A hỏi

**(1) 9 thắng / 0 thua ổn định qua L1 + L2; CI và Holm đúng họ cố định — ĐẠT.**
- `context_gold_all` C tính lại **bằng đúng** trường đã lưu ở mọi câu, mọi lượt; context = top-10 ở mọi câu mọi lượt (nên hai chỉ số trùng).
- Dev 40: mốc **22**, L1 (`m_l1_pilot` + `m_l1_rest`) **31**, L2 **31**. Thắng ổn định **9** = 17, 38, 48, 67, 70, 85, 156, 159, 167 (đúng 9 câu trần); thua context **0**, thua
  top-10 **0**; câu đổi `context_gold_all` giữa L1 ↔ L2: **0**.
- Vector +1 / −1 / 0: TB **+0,225**, CI 95 % **[+0,10; +0,35]**, p bootstrap **0** (không vòng nào trong 10.000 ≤ 0, tức p < 0,0001); Holm `[0,798, 1, p, 1]` ⇒ **0** < 0,05.
  Ngưỡng ghi trước ≥ 5 / 0 — qua với dư địa lớn.

**(2) Test 3 / 3, sàn mất đoạn đúng = 0 — ĐẠT.**
- Test 15 (một lượt `m_test`): mốc 7 → **10**; thắng **20, 95, 130** (= 3 câu trần); thua context **0**, top-10 **0**; lỗi kỹ thuật 0. (Một lượt, 3 / 0: CI [0,0; 0,4], p 0,068 —
  đúng vai "không làm hỏng", không phải "tốt hơn"; report ghi đúng vai này.)
- Hợp đồng nhánh m: **0 / 95** sai (mọi lần trả đúng 10 số khác nhau trong 1..30), 0 lỗi kỹ thuật; Clopper–Pearson [0; 3,81 %] — khớp report. Trần ≤ 4 ✓.

**(3) Tiền: log và ước tách rõ; dời trần con đúng tin A — ĐẠT** (kèm m-1).
- Log: `n_l1_pilot` 0,0035036; `m_l1_pilot` 0,0051211; `m_l1_rest` 0,0183023; `m_l2` 0,0239509; `m_test` 0,0083397 — mỗi lượt: tổng `luna.usd` = tính lại từ token = meta.
  Nhánh m **0,0557140**, cộng **0,0592176** — khớp. Phần ước `n_l1_rest` (≈ 0,0074) ghi tách riêng, nói rõ là ước — đúng; cận trên xem m-1.
- Dời trần con: cộng dồn nhánh m sau L2 = 0,0473743 (< 0,055); vượt 0,055 chỉ xảy ra **trong lượt test**, bắt đầu **09:55:36** (meta) — sau tin A **09:51:39** mà report ghi.
  Pilot m dự phóng 0,000512 × 85 + 0,00512 ≈ 0,049 < 0,055 ⇒ luật dừng pilot §6.2 không bị phạm. Tổng K3b log 0,0592 + ước 0,0074 ≈ 0,067 ≤ 0,10.

**(4) `f4d3225` không đổi tiêu chí — ĐẠT.**
- Diff `7c0467d..f4d3225` chỉ: (a) thêm `except ValidationError` ⇒ trả `error` (plan §2 loại 1 "parse hỏng" — cùng loại với `output_parsed is None`), `usage_unknown`;
  (b) ghi từng dòng ngay sau mỗi câu, meta luôn được ghi (`crashed`). Không đổi prompt, hợp đồng, luật thắng / thua, Holm, trần, dừng. Mọi lượt nhánh m chạy bằng
  `f4d3225` (sau 09:35); nhánh n pilot bằng `7c0467d` — phần đổi không chạm đường đi của pilot (0 lỗi).

**(5) Kết luận n và câu "bản nhanh có thể giữ chất lượng" ghi đúng mức — ĐẠT.**
- "n kém hơn" dựa trên một lỗi kỹ thuật quan sát được (xem m-2 về nơi lưu bằng chứng) — đúng sàn loại 1, dừng không gọi lại.
- Câu "bản nhanh có thể giữ cùng chất lượng nếu sửa được lỗi chữ thừa" được gắn *Suy ra, chưa chứng minh* và "mới có 10 câu cho n" — đúng. C kiểm: trên 10 câu pilot,
  `context_gold_all` n **9**, m **9**, K3 **9** (mốc 6; 3 câu thắng đều là câu trần trong pilot); token vào n = m ở 10 / 10 câu (nên chênh giá chỉ đến từ token ra 33 so với ~381).
  Mục "Cho bạn" nói "chờ thêm khoảng 1,8 giây" cho bản n — là số pilot 10 câu; ổn vì cùng đoạn đã nói bản này dừng.

Số theo dõi khác khớp: `rerank_ms` nhánh m p50 **5.021** / p95 **7.007** ms; token luna vào TB 3.958, ra TB 381, max 702; USD / lần 0,000586 ⇒ USD / câu đầu–cuối ước
0,00079 (**3,9×** mốc 0,000204); pilot n p50 1.760 / p95 2.092 ms, 0,000350 USD / lần.

## 5. Giới hạn hoặc phần chưa chạy

- C không gọi lại luna; không tái lập được lỗi nhánh n từ dữ liệu (m-2).
- Đoạn đúng do agent gắn (User duyệt ~10 câu) — thước tầng tìm duy nhất; 9 câu trần chọn trên chính dev (B42), test một lượt. Report §6 đã ghi.
- **Cho A khi trình User:** đây là kết quả **tầng tìm** (đoạn đúng vào context), chưa phải câu trả lời — lượt sinh + judge NOT RUN; B42 đã thấy câu tự nhiên không lợi từ
  context 10, nên lợi ở tầng tìm có thể không thành lợi ở câu trả lời. Giá: +5,0 s p50 / +7,0 s p95, USD ≈ 3,9× — p95 vượt mức theo dõi 5 s.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** K3b-m qua luật giữ plan §4 bước 1–2 ở tầng tìm; K3b-n kém hơn. Plan §4 bước 3: thêm lần gọi API ⇒ A trình User kèm số giá; phụ lục lượt
sinh (B ước ≈ 0,11 USD) cần trần riêng do A / User duyệt trước khi chạy. 3 minor không chặn — m-1, m-2 nên sửa chữ trong report trước khi A dùng số tiền / bằng chứng n để
trình User (commit tiếp trên `p82-k3b`); m-3 ghi cho biến thể sau.
