# Review: Phase 8.2 §10 K3b-m — lượt sinh + judge (report phụ lục, B60–B65)

Decision: **ready_for_user_confirmation** — kết luận **kém hơn (vượt mức tụt T3: 5 câu Completeness tụt > 4)** đúng theo tiêu chí ghi trước; 0 blocker / 0 major / 2 minor
Người kiểm: C (Claude Opus 5.5, `hue-rag-5b`) · Việc: C54 (A giao 27/10)
Date: 2026-10-27 10:50 +0700 (`date`)
Canonical guide: plan phụ lục bản 3 `phase_8_2_k3b_m_answer_plan.md` sha `2a3b22b38ab6` (A duyệt `c46019f`; C tính lại từ file: khớp); K3 plan `0a6370204c7d` §4; spec 8.2 §10.2
Implementation report: `origin/p82-k3b` `a6f609c` — `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3b_m_answer_implementation.md`

File này không chép câu hỏi, đáp án, câu trả lời hay nội dung kho — chỉ `case_index`, số đếm, sha.

## 1. Phạm vi đã review

- **Git:** `git diff --stat 806e8ad..origin/p82-k3b` = 3 file (`backend/experiments/phase_8_2/k3b_answer.py`, `backend/tests/test_k3b_answer_text.py`, report). Không production.
  `git diff --check` sạch. `6b4114e` (bản 3) chỉ đổi 10 dòng của `k3b_answer.py` (bỏ dừng ở 120, đưa 120 về `WATCH_CASES`).
- **Code** `k3b_answer.py` (đọc hết): `K3bService` bọc `service.search` production → 30 đoạn `stages["rrf"]` → phát lại thứ tự luna (55 câu có đoạn đúng) hoặc
  `k3b.luna_top10` mới → `k3b.apply_contract` → 10 đoạn; lỗi rerank ném `RuntimeError` để `answer_case` ghi `error` (sàn T2); `api_500` = `error` hoặc `citation_error`
  (đúng T2 bản 2–3); `pooled_items` gộp K3b-m + B1, câu giống hệt chữ chấm một lần, id mờ xáo seed; `analyze` đếm thua = `k3b < b1` trên dev chính (`keep_realism` main,
  bỏ OOS). Bộ tách câu W2 nhận `. [1]` và không phân biệt hoa thường (m-4 vòng 2 đã sửa).
- **Dữ liệu** `data/phase_8_2/k3b/answer/` (`v3_dev_pilot`, `v3_dev_rest`, `answer_dev`, `judge_dev/` 9 lô + 9 tệp điểm + `map.json`, meta, hồ sơ bản 2 `dev_pilot`).
- **Không đọc:** câu test, câu kín, `.env`. Không dùng `analyze_dev.json` / `check_dev.json` / `c51_dev.json` của B để kiểm — tự tính (mục 3).

## 2. Findings

Không có blocker hoặc major.

### m-1 — một trong 5 câu tụt (66) có dấu hiệu nhiễu judge; nên ghi khi trình User

- **Bằng chứng (C đọc trong terminal 5 câu tụt + phản hồi judge):** 26, 93, 134 — câu trả lời K3b-m bỏ một chi tiết nhỏ có trong đáp án tham chiếu (−1 hợp lý); **112** — bỏ ý
  chính của đáp án (5 → 3, Accuracy 5 → 4: tụt thật); **66** — câu trả lời B1 và K3b-m **cùng thiếu đúng một ý** (phản hồi judge nêu cùng ý đó cho cả hai), nhưng B1 được 5
  còn K3b-m được 4.
- **Tác động:** không đổi kết luận — luật ghi trước đếm số câu thua, và nhiễu judge đã nằm trong cách đặt ngưỡng A/A + 3. Nhưng khi A trình User, "5 câu tụt" nên kèm
  phân loại: 1 tụt rõ (112), 3 tụt nhỏ (một chi tiết), 1 nhiều khả năng do judge (66). Phân loại do **một người** (C) đọc.
- **Tiêu chí đóng:** A ghi phân loại này vào văn bản trình User (hoặc B thêm một dòng vào report §4.2 ở commit kế). Không cần chạy gì.

### m-2 — "3,8×" gộp tiền rerank đã trả ở K3b cho câu phát lại — nên tách khỏi "tiền lượt này"

- **Bằng chứng:** tiền log của lượt v3 = 0,0701443 (sinh 120 câu + 80 lần rerank mới), cộng pilot bản 2 0,0047854 = **0,0749297** — khớp. Tỉ lệ "3,8×" ở §4.4 tính **cả** tiền
  rerank đã trả ở K3b cho 40 câu phát lại (để ra USD / câu nếu chạy thật) — đúng ý plan §4 ("báo riêng tiền lượt này và tiền / câu nếu chạy thật"), nhưng report chỉ ghi một
  con số; người đọc dễ lẫn với tiền lượt này.
- **Tiêu chí đóng:** ghi hai dòng: "tiền lượt này 0,0701 (v3) + 0,0048 (bản 2)" và "USD / câu nếu chạy thật 0,00078 (3,8×)". Không bắt buộc.

## 3. Cách người kiểm chạy lại thật

0 USD. Từ `backend/` working tree chính: `/tmp/c54_check.py` (`PYTHONPATH=. uv run python /tmp/c54_check.py`) — đọc `answer_dev.jsonl`, hai phần `v3_*`, `b1_dev.jsonl`,
`judge_dev/{batch,scores}_*.jsonl` + `map.json`; ghép điểm theo `map` (không dùng `analyze`); `keep_realism`, `bootstrap_mean_diff` (seed 20261024), `validate_score_rows`,
`g2_generate.citation_error`, `cost_usd`. `/tmp/c54_read.py` in câu hỏi / đáp án / hai câu trả lời / điểm + phản hồi judge để đọc tay (terminal). W2 tính lại bằng
`c51_scan.check` (`data/cai_tien_tung_khau_2026-10-26/c51/`).

## 4. Kết quả quan sát — năm điểm A hỏi

**(1) T3 = 5 câu tụt trên đúng tập, đúng cách đếm, đúng ngưỡng — ĐẠT.**
- Dev chính = `keep_realism(dev, "main")` bỏ OOS = **88** câu — cùng tập với A/A. Thua = Completeness K3b-m < B1 cùng lượt mù: **5** câu (26, 66, 93, 112, 134); thắng 8, hòa 75.
- Ngưỡng: A/A B1 ↔ G2.1a dev chính Completeness 1 / 86 / 1 (`data/phase_8_2/b1/judge/`, C tính lại ở C46) ⇒ max(1, 1) + 3 = **4** — đúng K3 plan dòng 89 và phụ lục T3.
  5 > 4 ⇒ **vượt mức tụt** ⇒ "kém hơn" theo luật giữ (đạt T1, T2 **và mọi** mức tụt). Dừng sau dev, test NOT RUN — đúng plan §3 bước 3.

**(2) T1 / T2 / T5 / T7 — ĐẠT.** T1: 0 / 12 OOS bị trả lời. T2: 0 câu `error` hoặc `citation_error`; C tính lại citation v2 trên 120 câu: 0. T5: 0 câu chính B1 trả lời
mà K3b-m từ chối (từ chối trong dev chính 7 → 2). T7: `output_tokens` sinh 0,968× (≤ 1,2). Thêm: phát lại `top_chunk_ids` = `m_l1.merged` **40 / 40**, tập phát lại = đúng 40
câu dev có đoạn đúng; 80 lần rerank mới, **0** sai hợp đồng; `answer_dev` = hai phần v3 (120 / 120, không dùng hồ sơ bản 2).

**(3) Judge mù, cùng model, 0 lỗi schema; điểm hợp lý — ĐẠT** (kèm m-1).
- Lô chỉ có 4 khóa `case_index` (số mờ), `question`, `reference_answer`, `answer` — không có tên lượt; mọi câu trả lời trong lô **bằng đúng** câu trả lời của lượt mà
  `map` trỏ tới; 215 item = 240 câu trả lời (25 item là câu trả lời giống hệt chữ của hai bên, chấm một lần — cùng cách A/A B1 ↔ G2.1a). 215 / 215 có điểm,
  `validate_score_rows` 0 lỗi.
- Model: report ghi `global.anthropic.claude-opus-5-5`, B1 ghi cùng id (report B1 dòng 47). C không xác minh được sub-agent đã Read gì ngoài lô (giới hạn chung của judge
  sub-agent).
- Đọc tay 5 câu tụt + 5 câu khác (70, 159 thắng; 153, 120, 34 seed 20261024): phản hồi judge bám đáp án tham chiếu, điểm đi đúng chiều nội dung; một chỗ không nhất
  quán (66, m-1).

**(4) TB / CI ba chỉ số ghi đúng là chỉ báo — ĐẠT.** C tính lại (dev chính 88): Completeness **+0,216** [+0,023; +0,443], Accuracy **+0,250** [+0,068; +0,466], Relevance
**+0,227** [+0,045; +0,443] — khớp. Report §4.2 ghi "Chênh TB [CI] là chỉ báo, không quyết", §5 tách "Chỉ báo, không quyết" khỏi kết luận — đúng; không có câu nào dùng CI > 0
để nói "tốt hơn".

**(5) Tiền log, e2e p50 / p95 — ĐẠT** (kèm m-2). Tiền: mỗi dòng `usd_answer + usd_rerank` = tính lại từ token = meta: v3 pilot 0,0052245, v3 rest 0,0649198, bản 2 0,0047854,
cộng **0,0749297** / trần 0,13. `e2e_ms` trên 80 câu gọi rerank mới: p50 **6.502**, p95 **9.126** ms — khớp; USD / câu nếu chạy thật 0,000780 = **3,82×** B1. Giờ chạy theo meta:
v3 pilot 10:35:19–10:35:35, rest 10:36:33–10:38:53 — sau duyệt bản 3.

**W2 / C51 (theo dõi):** từ chối → trả lời: 48, 67, 85, 120, 167, 168; mỗi câu **0** câu báo thiếu không citation; trả lời → từ chối: 0. `c51_scan.check` trên 105 câu trả lời K3b-m:
L1 0, L2 0 — khớp report.

## 5. Hướng mở "A/A của chính biến thể" (≈ 0,025 USD) — đánh giá của C

- **Hợp lệ về hình thức** nếu ghi trước là **chẩn đoán**, không thay kết luận "kém hơn" (report §5 đã ghi đúng ý này). Không có nó thì là "chạy lại cho qua".
- **Nhưng giá trị thông tin thấp** (*suy ra*): A/A đề xuất = sinh lại trên **cùng context K3b-m** ⇒ đo nhiễu sinh + judge ở context cố định — đúng loại nhiễu mà A/A B1 ↔ G2.1a đã đo
  (cùng model, cùng prompt, cùng judge; chỉ khác context). Kết quả nhiều khả năng lại ~1–2 câu đổi, tức xác nhận ngưỡng 4. Nó **không** đo được điều đáng hỏi: một biến thể đổi context
  ở hầu hết câu (luna đổi tập top-10) thì tất yếu có câu tụt **thật** đi kèm câu tăng — luật "chỉ đếm câu thua" phạt loại biến thể này dù TB tăng.
- **C khuyên:** không chạy A/A này. Câu hỏi thật là **luật nhận** (hướng (2) của report): có chấp nhận "8 tăng / 5 tụt, TB tăng có CI > 0, 4 câu hết từ chối, 1 tụt rõ" với giá 3,8× và
  +6,5 s không. Đó là quyết định User, trình kèm số; nếu User muốn luật khác thì **ghi trước cho biến thể sau**, không áp ngược để đổi kết luận K3b-m.

## 6. Giới hạn

- Judge Claude ⇒ mọi kết luận **tạm tới B0**. Một lượt sinh; 80 câu dùng một mẫu luna. Đọc tay judge chỉ 10 câu, một người.
- C không chạy lại lệnh có phí; tiền từ usage log.

## 7. Decision và bước tiếp theo

**ready_for_user_confirmation.** K3b-m: tầng tìm tốt hơn (tạm), khâu trả lời **kém hơn** theo luật ghi trước (T3 5 > 4); mọi sàn và mức tụt khác đạt; chỉ báo chất lượng tăng.
Không đưa vào chatbot. A trình User: kết luận theo luật + số chỉ báo + phân loại 5 câu tụt (m-1) + giá (3,8×, e2e p50 6,5 s / p95 9,1 s ở song song 4) + câu hỏi luật nhận
(mục 5). 2 minor không chặn.
