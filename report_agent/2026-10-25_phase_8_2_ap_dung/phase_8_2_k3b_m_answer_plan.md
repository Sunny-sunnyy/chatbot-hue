# Plan (phụ lục K3b): lượt sinh + judge cho K3b-m — đo khâu trả lời trước khi trình User

Người viết: B (Claude Opus 5.5, `hue-rag-31`) · 2026-10-27 10:03 +0700 (`date`) · Việc: B60 (A gọi "B59", giao 10:0x 27/10). Trạng thái: **bản 3** (10:27 27/10/2026; chỉ đổi T8, xem
"Đổi sau khi thấy số — nói thẳng"; bản 2 `92a8a7eb4177` đã chạy pilot và dừng; bản 1 `84d4aaf0ad04`) — chờ C kiểm phần sửa, rồi A ghi "duyệt bản sha"
(`WORKFLOW.md` §9.1).

Plan không chép câu hỏi, đáp án, câu trả lời hay đoạn kho. Repo public: chỉ có `case_index` và số đếm.

## Căn cứ để review

1. `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3_plan.md` (sha `0a6370204c7d`):
   - **§4 dòng 86–92 và 98** (tiêu chí tầng trả lời — phụ lục **giữ nguyên**);
   - **dòng 85** (120 / 168 là theo dõi);
   - **§4 "Luật giữ" bước 3**;
   - **§3 gạch "Phát lại thứ tự đã ghi"**.
2. `phase_8_2_k3b_plan.md` bản 2 (sha `57dad7150322`) **§2, §4 đoạn "Tầng trả lời"**, và report K3b
   `git show origin/p82-k3b:report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3b_implementation.md` **§4.3–§4.4**:
   - hợp đồng đầu ra;
   - tiêu chí tầng tìm đã qua;
   - giá đo thật.
3. `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` **§10.2** (bản `cd910c4c4169`): sàn chung, luật (i), "tốn hơn ⇒ trình User",
   test = "không làm hỏng" (Q2 §10.6 User đồng ý 27/10). Kèm code `backend/api/routes/chat.py:124-135` và `backend/llm/citations.py:25,29,33`
   (`811d25d`): khi nào API trả 500.
4. `skills/run-experiment/SKILL.md` **§1.6, §3.1, §3.5, §3.6, §3.8** (đếm trên đúng mốc, A/A, phát lại đầu ra model, judge cùng lượt, từ chối ghi đè).

Người review được chạy lệnh chỉ đọc và tính lại từ:
- `data/phase_8_2/b1/` (`b1_{dev,test}.jsonl`, `judge/`);
- `data/phase_8_2/k3b/` (`m_l1.merged`, `m_test`, `compare_m_*.json`);
- `data/phase_8_1/golden_realism_final.jsonl` (qua `g1_retrieval.load_realism`).

## 1. Câu hỏi

K3b-m làm tầng tìm tốt hơn (tạm):
- dev 9 thắng / 0 thua ổn định qua hai lượt, test 3 / 0;
- giá +5,0 s p50 / +7,0 s p95, USD / câu ≈ 3,9×.

Câu hỏi của phụ lục: khi chatbot dùng 10 đoạn luna chọn, **câu trả lời có hỏng ở chỗ nào không** (sàn + mức tụt của K3 plan), và **lợi ở tầng tìm có
hiện ra ở câu trả lời không** (theo dõi)? Có số này thì A mới trình User đánh đổi chất lượng ↔ giá.

**Đổi đúng một thứ so với mốc B1:** retrieval trả 10 đoạn K3b-m thay vì 10 đoạn RRF. Prompt, `gpt-6-luna` sinh, reasoning (không gửi), validator và
context builder đều là production ở `811d25d`.

## 2. Tiêu chí — lấy nguyên K3 plan §4 (không đổi)

| # | K3 plan | Tiêu chí | Vai |
|---|---|---|---|
| T1 | dòng 87 | out_of_scope bị trả lời, 18 câu (dev 12 + test 6) = **0** | sàn |
| T2 | dòng 88 | lỗi kỹ thuật / 500, 176 câu = **0**. Bằng máy: `row["error"] is not None` **hoặc** `row["citation_error"] is not None` (bản 2, C53 M-1) | sàn |
| T3 | dòng 89 | số câu Completeness tụt: dev chính 88 **≤ 4**, test chính 41 **≤ 6** (A/A + 3) | mức tụt |
| T4 | dòng 90 | số câu Accuracy tụt: dev chính **≤ 4**, test chính **≤ 5** | mức tụt |
| T5 | dòng 91 | từ chối nhầm trong phạm vi: dev chính **≤ +1**, test chính **≤ +1** | mức tụt |
| T6 | dòng 92 | lỗi citation v2 (tính lại cả hai lượt), 176 câu — **bản 2: theo dõi theo dạng** (`citations.py:25` từ chối kèm citation / `:29` không citation / `:33` id lạ) | theo dõi |
| T7 | dòng 98 | `output_tokens` sinh / câu: **≤ +20 %** | mức tụt |
| T8 | dòng 85 | 120 / 168 — **bản 3: theo dõi** (về như K3 plan gốc; bản 2 đặt 120 là sàn — xem "Đổi sau khi thấy số") | theo dõi |

**Luật giữ** (K3 plan §4 bước 3): đạt T1, T2 và mọi mức tụt T3–T5, T7 trên **dev chính và test chính** ⇒ K3b-m **"chất lượng tốt hơn (tạm)"** (tầng tìm
qua + khâu trả lời không hỏng). Kết luận cuối luôn là **trình User kèm số giá** (spec §10.2). Dựa judge nên **tạm tới B0**.

**Chỗ phụ lục khác K3 plan §4 — nói thẳng (bản 2, A duyệt cùng sha):**
- **T5 — chỉ ghi rõ cách đếm:** "từ chối nhầm +1" = số câu chính có `refusal` B1 = false và K3b-m = true (như R1 bản 2, B55 m-3).
  `paired_stats(…, 'false_refusal')` chỉ để theo dõi.
- **T2 / T6 — sửa cho khớp spec §10.2** (C53 M-1; B tự báo 10:1x). `api/routes/chat.py:124-135` trả **500 cho mọi** `CitationIntegrityError`. Hàm này ném ở
  `citations.py:25` (câu từ chối kèm citation), `:29` (không citation) và `:33` (id citation lạ). Hệ quả:
  - mọi lỗi citation v2 đều là một câu người dùng nhận 500, nên thuộc T2 (sàn 0, như sàn chung spec "0 câu lỗi kỹ thuật / 500");
  - K3 plan dòng 88 (sàn 0) và dòng 92 (+2) chồng nhau; đọc dòng 92 theo nghĩa "cho phép 2 câu 500" là trái spec, mà spec đứng trên plan;
  - ⇒ T6 thành **theo dõi theo dạng**, để biết vì sao nếu T2 phạm.

  Mốc B1: 0 lỗi v2 (dev + test), nên sàn 0 có nghĩa. Cùng hiểu lầm có ở R1 bản 2 / B55 M-1 (4). R1 đã dừng vì sàn khác, nên kết luận không đổi.
- **120 / 168 (T8): theo dõi** (bản 3; bản 2 đặt 120 là sàn). Lý do ở mục "Đổi sau khi thấy số — nói thẳng".

**Nhiễu A/A judge — đếm trên đúng mốc B1** (W23; B tính lại 27/10 trong B55, khớp C46; lượt mù `data/phase_8_2/b1/judge/` chấm B1 ↔ G2.1a):
- dev chính: Completeness 1 / 86 / 1, Accuracy 1 / 86 / 1, từ chối đổi 0;
- test chính: Completeness 3 / 38 / 0, Accuracy 2 / 38 / 1, từ chối đổi 0;
- citation v2: 0 so với 0.

Ngưỡng T3 / T4 = max(thắng, thua) + 3, đúng số K3 plan ghi.

**Theo dõi thêm** (không quyết; để trả lời câu "lợi có hiện ra ở câu trả lời không"):
- **W1 — Completeness / Accuracy chênh TB + CI 95 %** (dev chính, test chính), theo loại câu, và trên **các câu thắng ở tầng tìm**. Đếm trên mốc B1
  (B tính 10:0x):
  - 9 câu dev thắng: 2 câu không tự nhiên (17, 85), nên ngoài dev chính. Trong 7 câu chính, **156 đã 5 / 5 ở B1**. Vậy **chỗ tăng được = 6 câu**:
    38 (C4), 48 (từ chối, C1), 67 (từ chối, C1), 70 (C3), 159 (C3), 167 (từ chối, C1).
  - 3 câu test thắng: 20, 130 không tự nhiên; 95 đã 5 / 5. Vậy chỗ tăng trên test chính = **0**.

  ⇒ **Ghi trước:** 6 câu này là câu **có lý do biết trước để tăng** (đoạn đúng mới vào context). Câu khác cũng có thể đổi theo cả hai chiều: luna đổi
  tập top-10 ở mọi câu có đoạn đúng, và 18 câu dev chính đang < 5 ở B1 (C53 m-1). "Completeness tăng vượt nhiễu" khó thấy với n 88 (CI > 0 cần
  ≈ 5 / 0, C38 M-1). Lợi có thể không thấy được
  dù có thật. Kết quả đó **không** làm K3b-m "kém hơn" (luật giữ chỉ đòi không hỏng).
- W2 — câu đổi từ chối ↔ trả lời (`case_index`). Đếm câu trả lời có câu không citation kiểu "nguồn không có…". Lý do: dạng "trả lời vòng" đã chặn
  R2 / R1.
  - Cách tách câu: ở khoảng trắng sau dấu kết câu, **giữ các `[n]` đứng ngay sau dấu chấm ở câu trước** — `re.split(r"([.!?](?:\[(?:Nguồn )?\d+\])*)\s+")`
    rồi ghép phần đuôi vào câu trước (bài học B58 m-1).
  - Bản 1 ghi regex lookbehind; regex đó **nuốt `[n]`** vào phần ngăn cách, nên câu có trích bị đếm thành không trích. B bắt được khi kiểm harness
    0 USD.
  - Kiểm bằng chuỗi tự viết + câu trả lời thật R1 168 / R2 160: 1 câu không trích mỗi câu, đúng như B đọc.
- W3 — R4 (`experiments.phase_8_2.r4_numbers`, bản trên `main`) trên câu trả lời K3b-m: số không có trong đoạn được trích.
- W4 — giá (§4).

## 3. Cách chạy (khi duyệt)

**Harness `backend/experiments/phase_8_2/k3b_answer.py`** trên nhánh `p82-k3b` (worktree `/tmp/b_k3b`). Không sửa `k3b.py`, `k3.py`, production.
- **`K3bService`** — lớp bọc retrieval cùng khuôn `g2_generate.DocOrderService`:
  - `search(q)` gọi `service.search` production (pool 30);
  - lấy 30 đoạn `stages["rrf"]`;
  - lấy thứ tự luna (phát lại hoặc gọi mới, xem dưới);
  - qua `k3b.apply_contract`;
  - trả `RetrievalResult` với `documents` = 10 đoạn đã chọn, theo thứ tự đó.

  `full_corpus_eval.answer_case` chạy nguyên (context builder, generator, validator production).
- **Phát lại thứ tự đã ghi** (K3 plan §3; `run-experiment` §3.5 cho phát lại đầu ra model thật để đo khâu sau):
  - 40 câu dev có đoạn đúng phát lại thứ tự từ **`m_l1.merged.jsonl`** (L1; ghi trước, không chọn lượt sau khi thấy số);
  - 15 câu test có đoạn đúng phát lại từ **`m_test.jsonl`**;
  - 121 câu còn lại (dev 80, test 41) **gọi luna mới** bằng `k3b.luna_top10(effort=None)`, cùng prompt sha `4717583a1489`.
  - Kiểm phát lại: `top_chunk_ids` của câu phát lại = file gốc ở **55 / 55**. Lệch ⇒ dừng.
- **Hợp đồng đầu ra và sàn lỗi rerank** ở 121 lần gọi mới: giữ nguyên plan K3b §2.
  - Lỗi kỹ thuật (API / không completed / parse hỏng, gồm `pydantic.ValidationError`) ⇒ sàn T2, dừng.
  - Sai hợp đồng ⇒ top-10 RRF cho câu đó. **Trần ≤ 4 / 121**, số tuyệt đối. Báo k / n + CI Clopper–Pearson.
- **Ghi từng dòng ngay sau mỗi câu, luôn ghi `.meta.json` kể cả khi crash** (bài học `f4d3225`); từ chối ghi đè.
- Mỗi dòng ghi: các trường của `answer_case` + `replayed` (bool) + `luna` (usage, raw, order, contract) + `rerank_ms` + `e2e_ms` (đo bao quanh cả
  `answer_case`: retrieval + rerank + context + sinh).
- **Song song:** `CONCURRENCY` của evaluator (4, như B1), để thời gian chạy ≈ 176 × 7,5 s / 4 ≈ 6 phút. Latency từng lần gọi vẫn đo riêng.
  Ghi rõ đây là đo khi gọi đồng thời 4 (§6).
- **Judge cùng lượt mù** (như B1 / R1):
  - câu trả lời K3b-m + **B1 chấm lại** trong cùng lô, id mờ; câu giống hệt chữ trong cùng câu hỏi chấm một lần;
  - sub-agent judge Claude mới (ghi model id) chỉ Read `full_corpus_judge_prompt.md` + lô;
  - không gắn `answer_type` (từ chối đếm bằng máy).
- Lệnh: `run`, `merge`, `check` (sàn, tất định phát lại, citation, hợp đồng), `export-judge`, `check-judge`, `analyze` (T3–T7, W1–W2).

**Bước** (bản 3: **chạy lại từ đầu, tên lượt mới tiền tố `v3_`**; không dùng 9 câu pilot của bản 2 — `dev_pilot.jsonl` giữ làm hồ sơ; harness từ chối ghi đè):
1. **Pilot 10 câu dev** (seed 20261024, như `g2_generate.select('pilot')`: rút trong 120 câu dev, có thể gồm OOS):
   - đo USD / câu đầu–cuối thật, `e2e_ms`;
   - kiểm T1 / T2 sớm.
2. Dev còn lại 110 ⇒ gộp `answer_dev.jsonl` 120 câu ⇒ `check` (T1, T2, T6 theo dõi, phát lại 40 / 40, hợp đồng).
3. Judge mù dev (K3b-m dev + B1 dev) ⇒ `analyze` dev (T3, T4, T5, T7, W1, W2). Dev hỏng bất kỳ dòng nào ⇒ dừng, **kém hơn**.
4. Chỉ khi dev đạt: test (pilot 10 ⇒ 46 còn lại) ⇒ `check` ⇒ judge mù test (K3b-m + B1 test) ⇒ `analyze` test.
5. W3 (R4) trên dev + test từ working tree `main`.

## 4. Giá đo thật (W4) và tiền

- **USD / câu đầu–cuối** = `luna.usd` (gọi mới) + `cost_usd` của lượt sinh, theo usage log từng dòng. Báo TB dev / test và tỉ lệ so mốc B1 (0,000204 /
  0,000221).
- Câu phát lại có usage rerank lấy từ file gốc (lượt L1 / test của K3b, đã trả tiền). Báo riêng "tiền lượt này" và "tiền / câu nếu chạy thật".
- **Latency đầu–cuối:** `e2e_ms` p50 / p95 + CI bootstrap trên **121 câu gọi mới** (câu phát lại không có rerank thật trong lượt này). So mốc =
  retrieval B1 (p50 27 ms) + `latency_ms` sinh B1 (đo 26/10, khác phiên ⇒ chỉ theo dõi).
- `output_tokens` sinh (T7) so B1 trên dev 120.

*Ước* (số thật K3b-m: 0,000586 USD / lần rerank; B1: sinh 0,000204 dev / 0,000221 test; context đổi đoạn nên token vào sinh có thể đổi ±):

| Bước | Rerank mới | Sinh | Ước USD |
|---|---:|---:|---:|
| 1 Pilot dev 10 | ~7 | 10 | 0,006 |
| 2 Dev còn lại 110 | ~73 | 110 | 0,065 |
| 4 Test 56 | 41 | 56 | 0,036 |
| **Cộng** | 121 | 176 | **≈ 0,107** |
| Dừng sau dev (bước 3 trượt) | 80 | 120 | ≈ 0,071 |

**Trần: 0,13 USD** (A chốt) cho cả phụ lục, **tính cả 0,0047854 USD đã dùng ở pilot bản 2** ⇒ còn ≈ 0,125 cho lượt bản 3 (ước 0,107). Pilot vượt ước > 50 % ⇒ dừng, báo A. Trần 8.2 (0,5): trước phụ lục đã dùng ≈ 0,137:
- B1 + R2 0,0396;
- K3 0,0251;
- R1 0,0049;
- K3b log 0,0592 + ước 0,0074.

Thêm 0,13 ⇒ ≈ 0,27. Judge: quota Claude Code, 0 USD.

**Tập nhỏ hơn có đủ quyết không** (A hỏi) — B **không đề xuất** cắt:
- Luna đổi tập top-10 ở 40 / 40 câu có đoạn đúng (K3b §4.3), nên gần như mọi câu trả lời có thể đổi. Không có tập "câu chắc không đổi" để bỏ.
- T1 cần đủ 18 OOS. T3 / T4 / T5 tính trên đủ dev chính 88 / test chính 41, như A/A. Cắt thì ngưỡng A/A + 3 không còn đúng nghĩa.
- Chỉ bỏ được 29 câu không tự nhiên (20 dev + 9 test). Chúng chỉ góp vào T2 / T6 (176). Tiết kiệm ≈ 29 × 0,00079 ≈ **0,023 USD**, nhưng phải đổi
  tập của T2 / T6 so K3 plan (đổi tiêu chí). B khuyên giữ 176; A chọn (Q2).

## 5. Dừng

1. Phát lại lệch (`top_chunk_ids` ≠ file gốc) ⇒ dừng.
2. Pilot: USD / câu > 1,5 × ước, hoặc tiền dự kiến vượt trần ⇒ dừng, báo A.
3. Lỗi kỹ thuật ≥ 1 (sinh hoặc rerank, gồm 500 / parse) ⇒ phạm T2 ⇒ **kém hơn**, dừng. Không gọi lại. **429 / timeout cũng là lỗi kỹ thuật** (C53 m-3;
   gọi đồng thời 4, `max_retries=0`): dừng, ghi nguyên văn, **không chạy lại cả lượt khi chưa có A**.
4. OOS bị trả lời ≥ 1 ⇒ phạm T1 ⇒ **kém hơn**, dừng.
5. Sai hợp đồng rerank > 4 trong lượt ⇒ **kém hơn**, dừng.
6. Không ghi Qdrant, không sửa corpus / Golden / split / đoạn đúng, không mở câu kín, không đọc câu test theo từng câu. Câu trả lời test chỉ đi qua
   judge và đếm máy.

## 6. Giới hạn biết trước

- Kết luận dựa judge Claude ⇒ **tạm tới B0** (User đọc cặp mù).
- Câu có đoạn đúng dùng **một** mẫu thứ tự luna (L1). Hai lượt K3b-m giống nhau ở `context_gold_all` 40 / 40 nhưng tập top-10 chỉ giống 15 / 40.
  Vì vậy câu trả lời có thể khác nếu dùng L2. Đây là nhiễu luna ở khâu sau, chưa đo được trong ngân sách này.
- Latency đo khi gọi đồng thời 4, trên máy User. Production 1 người dùng có thể nhanh hơn.
- Lợi ở câu trả lời có trần 6 câu dev chính (W1) ⇒ "chưa thấy lợi" là kết quả có thể xảy ra, không có nghĩa là "không có lợi".

## 7. Đầu ra

Report `phase_8_2_k3b_m_answer_implementation.md` trên `p82-k3b` (B commit + push, lệnh push riêng) ⇒ C review. Report gồm:
- bảng T1–T7 dev / test;
- W1–W4;
- giá thật;
- 3–5 dòng lời thường cho User.

Dữ liệu `data/phase_8_2/k3b/answer/`.

## 8. Câu hỏi cho A

A đã chốt (tin A 10:2x, trước bản 2):
1. Trần **0,13 USD**.
2. Giữ **176 câu**.
3. W1 **chỉ theo dõi**.
4. Quyền: B commit + push `p82-k3b` (không merge), paid `gpt-6-luna` trong trần mục 1, sub-agent judge Claude.

## Sửa sau review C53 (10:11 27/10/2026 +0700, `date`)

| Finding / quyết định A | Sửa |
|---|---|
| M-1 T2 / T6 chồng nhau (API 500 cho mọi `CitationIntegrityError`) | T2 = `error` **hoặc** `citation_error` ≠ null, sàn 0, kèm `chat.py:124-135`, `citations.py:25,29,33` (căn cứ mục 3); T6 thành theo dõi theo dạng; đoạn "Chỗ phụ lục khác K3 plan — nói thẳng" ghi lý do |
| m-1 "trần 6 câu" | W1: "6 câu có lý do biết trước để tăng; câu khác cũng có thể đổi theo cả hai chiều (18 câu dev chính < 5 ở B1)" |
| m-2 120 thành sàn (A chọn) | T8: 120 = sàn "vẫn từ chối"; 168 theo dõi; luật giữ + dừng 3b |
| m-3 429 / timeout | §5.3: lỗi kỹ thuật, dừng, ghi nguyên văn, không chạy lại khi chưa có A |
| B tự thấy khi kiểm harness 0 USD | W2: regex bản 1 nuốt `[n]` ⇒ thay bằng cách tách giữ `[n]`, đã kiểm trên chuỗi tự viết + câu R1 168 / R2 160 |
| A chốt §8 | ghi vào §8 |

Không đổi: T1, T3, T4, T5 (ngưỡng), T7, mốc B1, A/A, cách phát lại (L1 / `m_test`), trần 0,13, 176 câu, judge cùng lượt mù.

## Đổi sau khi thấy số — nói thẳng (bản 3, 10:27 27/10/2026 +0700, `date`)

Bản 3 đổi đúng **một** chỗ: T8 "120 vẫn từ chối" từ **sàn** về **theo dõi**, như K3 plan gốc (dòng 85). Bốn ý:

1. **Sàn này do A thêm ở bản 2** (theo C53 m-2), dựa trên tiền đề "context K3b-m của câu 120 có 0 fact". Tiền đề đó lấy từ nhãn đoạn đúng (`top10_gold_frac`
   0 ở L1, L2) và **chưa được kiểm** bằng nội dung kho trước khi đặt sàn (A nhận đây là lỗi gốc).
2. **Lượt bản 2 dừng ở pilot** (10:16:36–10:16:52, `data/phase_8_2/k3b/answer/dev_pilot.jsonl`, 9 câu, 0,0047854 USD log), vì câu 120 được trả lời.
   **Kết luận của lượt đó giữ nguyên: phạm sàn T8 theo luật bản 2.** Bản 3 không viết lại kết luận đó.
3. **Bằng chứng để đổi lấy từ nội dung kho, không từ điểm số** (không có judge nào được chạy):
   - B kiểm tay: câu trả lời 120 khớp đáp án tham chiếu. Cả hai fact (tên gọi khác, độ cao) có trong context K3b-m, ở hai chunk khác của cùng file,
     diễn đạt lại.
   - Quét B61 (`data/phase_8_2/k3b/gold_scan/`): nhãn chỉ đánh dấu một chỗ cho mỗi fact. Mức loose bắt được 120 ở K3b-m (2 / 2 fact) và không bắt
     được ở mốc B1 (0 / 2).
   - ⇒ Tiền đề của sàn sai vì nhãn thiếu, không vì model bịa.
4. **User duyệt** phương án (1) "đưa 120 về theo dõi". A báo, B nhận tin lúc **10:27:20 27/10/2026** (`date` của B; giờ User nói do A ghi).

Không đổi gì khác:
- T1–T7 (gồm T2 = `error` hoặc `citation_error`, sàn 0);
- mức tụt;
- mốc B1, A/A, cách phát lại;
- 176 câu;
- trần 0,13 USD (đã dùng 0,0048);
- judge cùng lượt mù.

168 vẫn theo dõi như bản 2. Harness: bỏ điều kiện dừng ở câu 120 (`MUST_REFUSE`). Commit riêng sau khi A duyệt sha bản 3.
