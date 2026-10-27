# Review: Phase 8.2 §10 K3 — `gpt-6-luna` xếp lại pool 30 → top-10 (report B54)

Decision: **ready_for_user_confirmation** — kết luận **kém hơn (phạm sàn: 1 lỗi đầu ra luna / 40 lần gọi)** đúng theo tiêu chí ghi trước; 0 blocker / 0 major / 3 minor
Người kiểm: C (Claude Opus 5.5, `hue-rag-5b`) · Việc: C49 (A giao 27/10)
Date: 2026-10-27 09:12 +0700 (`date`)
Canonical guide: plan `phase_8_2_k3_plan.md` sha `0a6370204c7d` (A duyệt; C tính lại từ file trên `main`: khớp); spec 8.2 §10.2 bản `cd910c4c4169`
Implementation report: `origin/p82-k3` `80e7329` — `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3_implementation.md`

File này không chép câu hỏi, đáp án, nội dung kho hay đầu ra luna — chỉ `case_index`, số đếm, sha.

## 1. Phạm vi đã review

- **Git:** `git diff --name-only 811d25d..origin/p82-k3` = đúng 2 file (`backend/experiments/phase_8_2/k3.py` mới, report). Không file production, không
  `settings.yaml`, không `g4_rerank.py` / `k1.py`. `git diff --check` sạch. sha `k3.py` trên nhánh = `e58a0a33848f` (khớp report).
- **Code `k3.py`** (đọc hết): 30 đoạn lấy từ `trace.stages["rrf"]` của `service.search` production theo thứ tự RRF; payload qua `g1_retrieval.load_payloads`
  (đọc Qdrant); `--rerank luna` gọi nguyên `g4_rerank.luna_rank` (`811d25d`: lỗi API / `status` khác `completed` / không phải hoán vị ⇒ trả `error`, không gọi
  lại, không thay thứ tự gốc); lỗi đầu tiên ⇒ ghi dòng rồi `break`; context builder production (context 10 ở `811d25d`); mọi file ghi qua `new_file` (từ
  chối ghi đè). Không ghi Qdrant. Khác plan §3 (không import `k1.py`, chưa viết phần lượt sinh) đã ghi ở report §2 — hợp lý, không code cho bước chưa chạy.
- **Dữ liệu** `data/phase_8_2/k3/`: sha 12 của 5 file JSONL + `tools/k3_watch.py` khớp bảng report §4; hai `.meta.json` của lượt luna.
- **Không đọc:** câu test theo từng câu, câu kín, `.env`. Không dùng `k3_watch.py` để kiểm bảng §4.4 — tự viết script (mục 3).

## 2. Findings

Không có blocker hoặc major.

### m-1 — "0 câu mất" là trên 39 câu; câu không đo được (173) đúng là câu có rủi ro sàn

- **Vị trí:** report §4.4 dòng "Câu mất đoạn đúng khỏi top-10 / khỏi context — 0 / 0".
- **Bằng chứng:** câu 173 (lần gọi lỗi) ở mốc có **đủ đoạn đúng ở top-10 và context** (`base_dev.jsonl`: `top10_gold_all` 1, `context_gold_all` 1); luna trả 29 số,
  thiếu đoạn 5. Report §4.3 có ghi "Ở mốc, câu 173 có đủ đoạn đúng ở top-10", nhưng bảng §4.4 không nhắc mẫu số 39 loại đúng câu này.
- **Tác động:** A sẽ đưa số 9 / 0 cho User khi bàn K3b. Đọc riêng bảng, người đọc dễ hiểu "luna không làm mất câu nào trên 40". Thật ra câu duy nhất luna "làm
  hỏng" là một câu mốc đang đủ — đúng dạng rủi ro sàn của plan §1 (câu 154).
- **Tiêu chí đóng:** khi trình User, A ghi "0 mất / **39** câu đo được; câu 173 (mốc đủ) không đo được vì luna trả thiếu". Không cần sửa report nếu A ghi vào
  văn bản cho User; sửa report nếu có commit tiếp trên `p82-k3`.

### m-2 — giờ A cho chạy tiếp sau pilot không lấy bằng `date`

- **Vị trí:** report §4.2 "A nhận số pilot lúc 09:0x, cho chạy tiếp".
- **Yêu cầu:** `WORKFLOW.md` §6 (giờ trong file lấy bằng `date`, không ghi `HH:Mx`).
- **Bằng chứng / tác động:** meta cho biết pilot xong 09:00:28, lượt còn lại bắt đầu 09:00:57 — đủ để thấy thứ tự đúng (pilot trước, kiểm trần, rồi chạy). Chỉ là
  chuẩn ghi; không đổi kết luận.
- **Tiêu chí đóng:** ghi giờ từ tin A hoặc từ meta (09:00:28 → 09:00:57) ở lần sửa kế; A tự quyết có cần không.

### m-3 — `rerank_ms` p50 / p95 ở §4.5 tính trên 40 lần gọi (gồm lần lỗi), meta tính trên lần hợp lệ

- **Bằng chứng:** C tính lại: 40 lần p50 **5.613** / p95 **8.565** ms (= bảng §4.5); 39 lần hợp lệ p50 **5.632** / p95 **8.584** ms (= cách tính của meta). Chênh ≤ 20 ms.
- **Tác động:** không đáng kể; chỉ để người đọc biết mẫu số.
- **Tiêu chí đóng:** ghi "n = 40 lần gọi, gồm lần lỗi" cạnh bảng ở lần sửa kế, hoặc bỏ qua.

**Ghi chú (không phải finding):** câu 173 là câu **cuối** của lượt `rest` (thứ tự 168, 172, 173), nên nhánh "dừng ở lỗi đầu tiên" chưa bị thử giữa chừng
trong lượt thật. Đọc code: `break` ngay sau khi ghi dòng lỗi, meta ghi `stopped` — đúng plan §6.3. Không có lần gọi nào sau lỗi (40 = 10 + 30).

## 3. Cách người kiểm chạy lại thật

Không lệnh có phí. Từ `backend/` của working tree chính, script tạm `/tmp/c49_check.py` (`PYTHONPATH=. uv run python /tmp/c49_check.py`) đọc
`data/phase_8_2/k3/{base_dev,l1_pilot,l1_rest}.jsonl` + `data/phase_8_2/k1/base_dev.jsonl`, dùng `full_corpus_eval.cost_usd` / `bootstrap_mean_diff` và
`scipy.stats.beta`. Thêm: `sha256sum` các file dữ liệu và plan; `git diff --name-only|--check 811d25d..origin/p82-k3`; đọc `g4_rerank.luna_rank` ở `811d25d`.

Không chạy lại `check-base` bằng harness (lệnh chỉ đọc hai file): C so lại trực tiếp hai file theo cùng ba trường.

## 4. Kết quả quan sát

Ba điểm A yêu cầu kiểm kỹ:

**(1) Dừng đúng plan §6.3, sàn đúng như ghi trước — ĐẠT.**
- Sàn plan §4: "lỗi đầu ra luna (không phải hoán vị 1..30 / API lỗi / bị cắt) — floor 0"; §6.3: "lỗi ≥ 1 ⇒ dừng, ghi nguyên văn, không gọi lại, không thay bằng
  thứ tự RRF".
- Dòng câu 173 trong `l1_rest.jsonl`: `status` `completed`, 401 token ra (xa trần 2048 ⇒ không bị cắt), `error` "order is not a permutation of 1..n"; C parse `raw`:
  **29 số, thiếu 5, 0 lặp** — khớp report §4.3. Không trường `order` ⇒ không dùng thứ tự nào thay thế. Lần gọi: pilot 10 + rest 30 = **40**, không gọi lại.
- Kết luận "kém hơn (phạm sàn)" theo luật giữ / gỡ (`run-experiment` §4: phạm sàn ⇒ không thể "tốt hơn"), cùng cách gọi như R2. Các bước L2, test, lượt sinh **NOT RUN**
  ghi đúng.
- Cổng trước pilot: **M1** T1 `cefb2d1ad609` (C tính sha `m1_t1.jsonl`: khớp); **M2** C so `base_dev.jsonl` với `k1/base_dev.jsonl`: cùng 40 câu, **0 lệch** ở
  `top_chunk_ids`, `top10_gold_all`, `top10_gold_frac`. Trần trên đúng mốc (W23): mốc đủ ở top-10 **22 / 40**, pool đủ **31 / 40** ⇒ 9 câu có thể thắng — khớp.
- Pilot (§6.2): USD / lần 0,000564 (ước 0,0006, không vượt > 50 %); ước tầng tìm 95 lần ≈ 0,054 ≤ trần con 0,08 (A nâng khi giao; vẫn ≤ 0,06 của plan); p95
  `rerank_ms` 8,2 s < 15 s. Pilot là đúng 10 câu dev có đoạn đúng, `pilot ∪ rest` = 40 câu gold, không chồng.

**(2) Tiền tính từ usage log — ĐẠT.**
- Tổng trường `luna.usd` 40 lần = **0,0251129 USD**; tính lại từ token (160.514 vào, 18.123 ra, giá 0,1 / 0,5 USD / 1M) = **0,0251129** — khớp; bằng tổng hai meta
  (0,0056416 + 0,0194713). Lần lỗi cũng tính tiền (0,0007035) — đúng, provider đã tính.
- USD / lần 0,000628 (40) / 0,000626 (39 hợp lệ); token luna vào TB 4.013, ra TB 453, max 818 — khớp §4.5. "≈ 0,000832 USD / câu đầu–cuối (≈ 4,1×)" = 0,000628 +
  0,000204 (sinh mốc B1) — là **ước**, report ghi đúng là ước (lượt sinh NOT RUN).
- Clopper–Pearson 1 / 40: [0,063 %; 13,16 %] — khớp "[0,06 %; 13,2 %]".

**(3) Số theo dõi 39 câu tính đúng và ghi rõ là không dùng để kết luận — ĐẠT** (kèm m-1).
- C tính lại độc lập trên 39 lần gọi hợp lệ: top-10 đủ đoạn đúng **21 → 30 / 39**; thắng **9** (17, 38, 48, 67, 70, 85, 156, 159, 167 = đúng 9 câu trần), thua **0**;
  mất khỏi context **0**; `top10_gold_frac` TB 0,736 → 0,878 (11 tăng / 0 giảm); MRR@10 0,442 → 0,706; nDCG 0,514 → 0,744; đổi tập top-10 39 / 39; 120 / 168:
  0 → 0 / 0 → 0,5. Mọi số khớp bảng §4.4.
- Tiêu đề §4.4 ghi "**không dùng để kết luận**", nêu lý do (một lượt, không L2, thắng phải giữ ở cả hai lượt) và §5 tách rõ "kết luận chưa được dùng" — đúng.
- Tốc độ: `rerank_ms` p50 / p95, tìm đầu–cuối p50 5.681 / p95 8.618 ms, mốc 27 / 33 ms, `retrieval_ms` lượt luna 32 / 86 ms — khớp §4.5.

## 5. Giới hạn hoặc phần chưa chạy

- C không gọi lại luna (không cần: kết luận chốt bằng một lỗi quan sát được, có nguyên văn trong file).
- Đoạn đúng 40 câu là nhãn agent (User duyệt ~10) — giới hạn chung của thước tầng tìm, report §6 đã ghi.
- **Cho A khi đưa số 9 / 0 cho User** (không phải finding của report): (a) một lượt của model không tất định — 8.1 chưa có A/A cho luna xếp 30 đoạn; (b) 9 câu thắng là
  đúng 9 câu trần được chọn trên **chính dev này** (dev đã thấy), chưa có test; (c) MRR / nDCG ở đây chấm theo **keyword** (`score_retrieval`), chỉ `*_gold_*` mới là
  đoạn đúng; (d) mẫu số 39, xem m-1; (e) tỉ lệ lỗi 1 / 40 có CI tới 13 % — K3b cần ghi trước cách đo tỉ lệ lỗi luna như một chỉ số, không chỉ cách xử lý.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** K3 dừng đúng luật ghi trước; sàn, tiền, số theo dõi đều tái lập được từ dữ liệu thật. Kết luận **kém hơn (phạm sàn)**; không đưa vào
chatbot. 3 minor không chặn: m-1 A mang vào văn bản trình User; m-2, m-3 sửa ở lần commit kế trên `p82-k3` nếu có. Việc trung bình ⇒ A đóng, báo User kèm số tốc
độ / tiền và giới hạn §5. Hướng K3b (plan mới, review lại) là quyết định của A / User; trong ba ý report §5 nêu, ý (1) "đoạn thiếu xếp cuối theo RRF" là fallback —
`Session_Prompt.md` §7 cần lý do được ghi trước.
