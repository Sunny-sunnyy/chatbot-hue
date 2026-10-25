# Implementation Report: Phase 8.1 G2 — sinh câu trả lời (context / thứ tự / prompt / reasoning) + G2.3 citation

Người làm: B (Claude Opus 5.5, terminal `hue-rag-3f`) · 2026-10-25 13:02, bổ sung G2.4 đủ lúc 13:16 (giờ theo `date`) · Việc: B17 bước 2 · Kế hoạch
duyệt: `phase_8_1_g2_g4_plan.md` sha `a4adfc8eedd9` §2, §2.1 · Spec 8.1 §5 G2 · skill `run-experiment`. Report không chép
câu hỏi, đáp án, câu trả lời, feedback hay điểm từng câu.

## 1. Phạm vi

Đã làm: G2.0 baseline sinh lại; G2.1a context 10; G2.1b xếp 5 đoạn theo tài liệu; G2.2 P1 (trả lời phần có căn cứ) và P2
(2 luật spec Phase 6); G2.3 phát lại validator citation (hiện tại vs chính sách một nguồn A chọn); G2.4 **chỉ pilot** 10
câu rồi chạy đủ 120 câu (none / low / high; A duyệt); xác nhận trên test cho phương án "tốt hơn" duy nhất (G2.1a). Không
đổi chatbot / settings runtime, không ghi Qdrant, không mở câu kín.

## 2. Thay đổi

- `backend/experiments/phase_8_1/g2_generate.py` (mới): harness. Gọi `answer_case` của evaluator production (retrieval
  runtime → context builder → `OpenAIFullCorpusGenerator` → `select_cited_sources`) qua tham số
  (`build_context_builder(settings, max_documents)`, `from_environment(answer_instructions=…, reasoning_effort=…)`).
  Logic biến thể chỉ ở đây: `DocOrderService` (bọc retrieval, giữ tập 5 đoạn, xếp gom theo tài liệu), chữ P1/P2 (dựng
  bằng cách thay đúng câu luật từ chối trong `ANSWER_SYSTEM_INSTRUCTIONS`, có `assert` câu đó tồn tại), gộp câu trả lời mù
  cho judge, phát lại citation, phân tích theo cặp + Holm + guardrail §2.1.
- Không đổi code production.

## 3. Cách đã chạy thật

Từ `backend/`, `uv` trong `.venv`, `HF_HUB_OFFLINE=1`, `--env-file ../.env` cho lượt có phí.

1. Mốc byte retrieval sau khi Golden đổi `reference_answer` 10 câu (md5 Golden `0f7dbf41b422`, A 25/10): `full_corpus_eval
   retrieval --treatment dense_bm25_rrf` → `cefb2d1a…` — **PASS** (retrieval chỉ dùng câu hỏi).
2. Mỗi biến thể: `g2_generate run --variant <v> --cases pilot --name <tên>_pilot` (10 câu dev rút theo seed 20261024) → đo
   USD → `--cases rest` (110 câu) → `merge`. Luật tiền (A 25/10): lượt đủ ≤ 1,5 × ước lại từ pilot, ≤ 0,05 USD, tổng B17 ≤
   0,25 USD — script dừng nếu vượt; không lượt nào vượt (§5).
3. Judge: `export-judge --names <8 lượt dev> --batch-size 20` → 630 câu trả lời, **456 câu trả lời khác nhau** (câu giống
   hệt từng ký tự trong cùng câu hỏi chấm một lần) xáo theo seed, id mờ (không lộ biến thể), 23 lô; map
   `data/phase_8_1/g2/judge/map.json` sha `33b4c9603f20`. 12 sub-agent judge mới (Claude Opus 5.5, kế thừa model session —
   cùng model judge với 7B), mỗi agent 2 lô (1 agent 1 lô), chỉ Read prompt `full_corpus_judge_prompt.md` + lô, Write
   `scores_NN.jsonl`. `answer_type`: 6 sub-agent khác, chỉ dẫn cố định (full / partial / refusal theo điều câu trả lời tự
   nói, bỏ qua đáp án tham chiếu), mỗi agent 3–4 lô. `check-judge`: 456/456 điểm + nhãn, `score_errors` rỗng.
4. Test (chỉ cho G2.1a "tốt hơn"): `--cases test_pilot` / `test_rest` (56 câu test gồm out_of_scope) cho baseline +
   context10; judge mù riêng `judge_test/` (102 câu trả lời khác nhau / 112, map sha `0624491a8d7e`), 3 sub-agent judge + 1
   sub-agent `answer_type`; `check-judge` đủ, không lỗi.
5. `g2_generate analyze --base g20_baseline --b <nhóm Holm> --realism main|natural [--judge judge_test]`;
   `replay-citation --files …`.

Kiểm trước khi trả tiền: biến thể "xếp theo tài liệu" giữ nguyên tập 5 đoạn ở **120/120** câu và đổi thứ tự ở **47/120**;
phát lại validator trên 7B Run 1/2 ra đúng số lỗi đã lưu (4 / 6, `replay_matches_stored: true`).

## 4. Kết quả quan sát

Số chính = dev bỏ câu `unnatural` (88 câu trong kho + 12 out_of_scope), nhãn sha `0b65d1c138d2`; chênh = biến thể − G2.0,
bootstrap 10.000 seed 20261024; "thắng/hòa/thua" theo câu. Nhóm (a) = 13 câu có đủ đoạn đúng trong 5 đoạn runtime; (b) =
75 câu còn lại trong kho.

**Nhiễu đối chứng (A/A gần đúng, 0 USD):** G2.0 so với 7B Run 1 trên 83 câu dev số chính (bỏ 10 câu Golden mới): 10 câu đổi
Completeness, chênh TB +0,048; 24/83 câu trả lời giống hệt chữ, trong đó judge đổi Completeness 2/24; 1 câu đổi quyết định
từ chối. Đây là nhiễu "sinh lại + chấm lại bởi sub-agent khác".

### 4.1 G2.1 — context (Holm trên 2)

| Biến thể | Completeness: chênh [CI], t/h/t, p Holm | Accuracy [CI], p Holm | từ chối nhầm (câu) | lỗi citation (mới / hết) | USD/câu | Kết luận |
|---|---|---|---|---|---|---|
| G2.1a context 10 | **+0,261** [+0,080; +0,477], 9/77/2, **0,007** | +0,273 [+0,091; +0,500], 0,002 | 13 → 7 | 4 → 4 (2 / 2) | 0,000204 (1,53×) | **tốt hơn** → xác nhận test §4.4 |
| G2.1b xếp theo tài liệu | −0,023 [−0,068; +0,023], 1/84/3, 0,432 | −0,011 [−0,057; +0,023] | 13 → 13 | 4 → 6 (6 / 4) | 0,000134 (1,00×) | không khác |

- G2.1a: đủ 4 guardrail §2.1 (0 câu out_of_scope bị trả lời; Accuracy cận trên CI ≥ 0 — thực tế tăng có CI; lỗi citation
  +0 ≤ +2; USD/câu 1,53× ≤ 2×). Lợi nằm ở **nhóm (b) context thiếu** (+0,307 [+0,093; +0,573], 9/64/2); nhóm (a) 0/13/0 —
  context 10 không làm hỏng câu đã đủ bằng chứng. Relevance +0,318 [+0,125; +0,545]. Từ chối nhầm giảm 6 câu (0 câu
  thêm). Chỉ natural (45 câu): Completeness +0,200 [+0,044; +0,422], 5/40/0.
- G2.1b: lỗi citation tổng +2 (đúng ngưỡng, không vượt) nhưng 6 câu lỗi mới / 4 câu hết lỗi (C23 m6) ⇒ đổi thứ tự làm lỗi
  citation xáo trộn theo câu; Relevance +0,057 [+0,011; +0,114] (chỉ số phụ).

### 4.2 G2.2 — prompt (Holm trên 2)

| Biến thể | Completeness: chênh [CI], t/h/t, p Holm | Accuracy [CI] | từ chối nhầm | out_of_scope bị trả lời | lỗi citation (mới / hết) | answer_type full / partial / refusal | Kết luận |
|---|---|---|---|---|---|---|---|
| G2.0 (mốc) | | | 13 | 0 | 4 | 74 / 1 / 13 | |
| P1 trả lời phần có căn cứ | +0,114 [−0,023; +0,250], 12/71/5, 0,227 | +0,170 [+0,000; +0,352] | 13 → 1 | **2** | 4 → 3 (2 / 3) | 70 / **17** / 1 | **kém hơn** (phạm sàn out_of_scope) |
| P2 thêm 2 luật spec Phase 6 | +0,000 [−0,068; +0,068], 2/84/2, 1,0 | +0,023 [−0,045; +0,114] | 13 → 12 | 0 | 4 → **1** (1 / 4) | 74 / 2 / 12 | không khác |

- P1: đúng hướng H8 — từ chối nhầm 13 → 1, 17 câu trả lời một phần — nhưng **2 câu out_of_scope bị trả lời** (mốc 0, nhiễu
  7B = 0 câu đổi) ⇒ phạm sàn; Completeness chưa vượt 0. Relevance +0,330 [+0,136; +0,545] (phụ). Token ra +25% (98,8 so
  78,8/câu). Chỉ natural: Completeness +0,000 [−0,089; +0,089].
- P2: không khác ở mọi chỉ số chính; lỗi citation giảm 4 → 1 (phụ, n nhỏ); token ra −12%.
- Đếm máy "chứa câu từ chối chuẩn như chuỗi con mà không phải từ chối": 0 câu ở mọi biến thể ⇒ câu báo thiếu của P1 không
  dùng nguyên câu từ chối (đúng như prompt dặn); nhãn `answer_type` là cách duy nhất đếm "trả lời một phần".

### 4.3 G2.3 — phát lại validator citation (0 USD)

| Câu trả lời | n | lỗi đã lưu | phát lại validator hiện tại | chính sách một nguồn (A) | câu đổi |
|---|---:|---:|---:|---:|---:|
| 7B Run 1 | 176 | 4 | 4 | 4 | 0 |
| 7B Run 2 | 176 | 6 | 6 | 6 | 0 |
| G2.0 | 120 | 4 | 4 | 4 | 0 |
| G2.1a / G2.1b / P1 / P2 | 120 mỗi lượt | 4 / 6 / 3 / 1 | như lưu | như lưu | 0 |

- **Mọi** lỗi citation quan sát được (7B + G2) là loại "câu trả lời không có `[n]` nào" khi context có **5** nguồn (10 nguồn
  ở G2.1a); không có lỗi id lạ hay câu từ chối kèm citation. Mọi lượt context runtime đều có đủ 5 nguồn (7B Run 1:
  176/176; G2.0: 120/120) ⇒ chính sách "context chỉ có một nguồn thì gán nguồn đó" **không bao giờ áp dụng**. Vế "mọi câu
  thiếu `[n]` thuộc một nguồn duy nhất được trích" cũng không đổi gì: validator chỉ báo lỗi khi không có `[n]` nào.
- Kết luận G2.3: **không khác** (0 câu đổi). Lỗi citation hiện tại là model quên đặt `[n]` khi có nhiều nguồn — chính sách
  này không chạm tới; muốn giảm phải sửa ở bước sinh (P2 giảm 4 → 1 là tín hiệu, chưa qua thước) hoặc chính sách khác
  (ví dụ cho model sinh lại một lần) — ngoài phạm vi 8.1, ghi cho 8.2.

### 4.4 Xác nhận trên test — G2.1a context 10 (56 câu test; số chính 41 câu trong kho)

| | Completeness: chênh [CI], t/h/t | Accuracy [CI] | từ chối nhầm | out_of_scope bị trả lời | lỗi citation (mới / hết) | USD/câu |
|---|---|---|---|---|---|---|
| số chính (41) | **+0,268** [+0,024; +0,585], 6/34/1 | +0,220 [−0,024; +0,537] | 3 → 1 | 0 | 4 → 4 (3 / 3) | 0,000207 vs 0,000139 (1,49×) |
| chỉ natural (25) | +0,240 [+0,000; +0,600], 3/22/0 | +0,160 [+0,000; +0,480] | 1 → 0 | — | — | — |

Luật xác nhận (plan §2.1: cùng dấu + đủ guardrail, không đòi CI): **đạt** — Completeness cùng dấu (CI còn > 0), 0 câu
out_of_scope bị trả lời, Accuracy cận trên ≥ 0, citation +0, USD 1,49×. ⇒ **G2.1a context 10: tốt hơn, đã xác nhận trên
test.** Đưa vào runtime là việc riêng, User duyệt (skill `run-experiment` §4).

### 4.5 G2.4 — reasoning effort (dev 120 câu; Holm trên 3; A duyệt chạy đủ 13:0x)

Pilot 10 câu (12:49–12:50) rồi 110 câu còn lại (13:06–13:09) mỗi mức, gộp thành `g24_<mức>.jsonl`. Chấm mù **cùng một lượt
mới** với G2.0 (`judge_g24/`, 480 câu trả lời → 360 khác nhau, 18 lô, 6 sub-agent judge + 1 sub-agent `answer_type`; map sha
`38d237bc03df`; `check-judge` đủ, không lỗi) để điểm baseline và biến thể cùng người chấm. **Nhiễu judge-only** (G2.0 chấm ở
`judge/` vs `judge_g24/`, cùng chữ): Completeness đổi 2/88 câu, chênh TB 0,000; Accuracy 1/88; Relevance 3/88.

| Mức | Completeness: chênh [CI], t/h/t, p Holm | Accuracy [CI], p Holm | từ chối nhầm | lỗi citation (mới / hết) | token ra TB | USD/câu | Kết luận |
|---|---|---|---|---|---:|---:|---|
| mặc định (không gửi) — G2.0 | | | 13 | 4 | 78,8 | 0,000134 | |
| none | **+0,136** [+0,034; +0,261], 8/78/2, **0,031** | +0,227 [+0,080; +0,398], 0,002 | 13 → 4 | 4 → **8** (7 / 3) | 54,3 | 0,000121 (0,91×) | **kém hơn** (lỗi citation +4 > +2) |
| low | +0,023 [−0,114; +0,148], 5/80/3, 1,0 | +0,102 [−0,057; +0,261], 0,434 | 13 → 7 | 4 → **9** (8 / 3) | 53,6 | 0,000121 (0,91×) | **kém hơn** (lỗi citation +5 > +2) |
| high | +0,023 [+0,000; +0,068], 1/87/0, 1,0 | +0,011 [−0,045; +0,102], 0,965 | 13 → 12 | 4 → 4 (2 / 2) | 107,0 | 0,000148 (1,11×) | không khác |

- `none`: Completeness tăng có CI sau Holm và từ chối nhầm giảm 9 câu (0 câu thêm), nhưng lỗi citation gấp đôi (7 câu lỗi mới)
  ⇒ phạm guardrail §2.1 ⇒ **kém hơn** theo luật đã ghi. Lợi nằm ở nhóm (b) (+0,173 [+0,053; +0,307]); nhóm (a) 0/12/1. Chỉ
  natural (45 câu): Completeness −0,022 [−0,111; +0,044] — không khác. ⇒ Tín hiệu cho 8.2: suy luận ít làm model bớt từ chối
  nhưng hay quên `[n]`; nếu ghép với cách xử lý lỗi citation khác (G2.3 cho thấy chính sách hiện tại không chạm tới) có thể
  đáng thử lại.
- `low`: 2 câu trả lời chứa câu từ chối chuẩn kèm nội dung khác (đếm máy) — dạng "từ chối một phần" làm validator báo lỗi.
- `high`: token ra +36%, không đổi chỉ số nào.
- Mọi mức: 0 câu out_of_scope bị trả lời; API nhận cả `none`, 0 lỗi kỹ thuật.

### 4.6 Kết luận G2 (theo tiêu chí ghi trước)

| Biến thể | Kết luận |
|---|---|
| G2.1a context 10 | **tốt hơn, xác nhận trên test** (Completeness dev +0,26, test +0,27; tiền ×1,5/câu) |
| G2.1b xếp theo tài liệu | không khác |
| G2.2 P1 trả lời một phần | kém hơn — phạm sàn (2 câu out_of_scope bị trả lời); từ chối nhầm 13 → 1 là tín hiệu cho H8 ở 8.2 |
| G2.2 P2 2 luật spec | không khác (lỗi citation 4 → 1: tín hiệu phụ) |
| G2.3 chính sách một nguồn | không khác (không bao giờ áp dụng với context 5 nguồn) |
| G2.4 none | kém hơn — Completeness +0,14 có CI nhưng lỗi citation 4 → 8 (phạm guardrail); tín hiệu cho 8.2 |
| G2.4 low | kém hơn — lỗi citation 4 → 9 |
| G2.4 high | không khác (tốn thêm 11%/câu) |

**Lời thường cho User:** Mình thử năm cách cho model trả lời. Đưa cho model 10 đoạn thay vì 5 giúp câu trả lời đầy đủ hơn rõ
rệt (điểm "đầy đủ" tăng khoảng 0,26 trên thang 5, ở cả bộ thử lẫn bộ kiểm), số câu từ chối nhầm giảm gần một nửa, đổi lại
mỗi câu tốn thêm khoảng 50% tiền (≈ 0,0002 USD ≈ 5 đồng/câu). Cho model "trả lời phần có căn cứ" thì gần như hết từ chối nhầm,
nhưng lại trả lời cả 2 câu hỏi ngoài phạm vi mà lẽ ra phải từ chối, nên theo luật chưa dùng được. Sắp xếp đoạn theo tài liệu
và thêm 2 luật cũ của spec thì không khác. Bảo model suy luận ít ("none") thì câu trả lời đầy đủ hơn một chút nhưng
model hay quên ghi nguồn [n] (lỗi gấp đôi — người dùng sẽ gặp lỗi), nên chưa dùng; suy luận nhiều ("high") không khác mà tốn
hơn. Giới hạn: chưa có mốc người chấm (judge là Claude), bộ thử 88 câu, bộ kiểm 41 câu.

## 5. Tiền (token + USD từ log `data/phase_8_1/g2/*.meta.json`)

| Lượt | biến thể | tập | n | token vào | token ra | USD | giờ |
|---|---|---|---:|---:|---:|---:|---|
| `g20_baseline_pilot` | baseline | pilot | 10 | 8.727 | 736 | 0,0012407 | 12:39:41–12:39:52 |
| `g20_baseline_rest` | baseline | rest | 110 | 104.278 | 8.717 | 0,0147863 | 12:42:23–12:43:20 |
| `g2_context10_pilot` | context10 | pilot | 10 | 15.312 | 689 | 0,0018757 | 12:40:14–12:40:25 |
| `g2_context10_rest` | context10 | rest | 110 | 183.692 | 8.546 | 0,0226422 | 12:43:30–12:44:28 |
| `g2_doc_order_pilot` | doc_order | pilot | 10 | 8.727 | 844 | 0,0012947 | 12:40:34–12:40:45 |
| `g2_doc_order_rest` | doc_order | rest | 110 | 104.281 | 8.618 | 0,0147371 | 12:44:51–12:45:34 |
| `g2_p1_partial_pilot` | p1_partial | pilot | 10 | 9.177 | 915 | 0,0013752 | 12:40:55–12:41:07 |
| `g2_p1_partial_rest` | p1_partial | rest | 110 | 109.228 | 10.935 | 0,0163903 | 12:45:44–12:46:42 |
| `g2_p2_spec_rules_pilot` | p2_spec_rules | pilot | 10 | 9.197 | 575 | 0,0012072 | 12:41:17–12:41:26 |
| `g2_p2_spec_rules_rest` | p2_spec_rules | rest | 110 | 109.448 | 7.773 | 0,0148313 | 12:46:53–12:47:46 |
| `g24_none_pilot` | reasoning none | pilot | 10 | 8.727 | 518 | 0,0011317 | 12:49:12–12:49:22 |
| `g24_low_pilot` | reasoning low | pilot | 10 | 8.727 | 512 | 0,0011287 | 12:49:32–12:49:41 |
| `g24_high_pilot` | reasoning high | pilot | 10 | 8.727 | 1.237 | 0,0014912 | 12:49:50–12:50:02 |
| `t_baseline_pilot` | baseline | test_pilot | 10 | 9.170 | 592 | 0,0012130 | 12:57:24–12:57:35 |
| `t_baseline_rest` | baseline | test_rest | 46 | 44.538 | 4.204 | 0,0065558 | 12:57:45–12:58:25 |
| `t_context10_pilot` | context10 | test_pilot | 10 | 15.482 | 598 | 0,0018472 | 12:58:45–12:58:42* |
| `t_context10_rest` | context10 | test_rest | 46 | 76.783 | 4.110 | 0,0097333 | 12:58:52–12:59:21 |
| `g24_none_rest` | reasoning none | rest | 110 | 104.278 | 6.002 | 0,0134288 | 13:06:19–13:07:09 |
| `g24_low_rest` | reasoning low | rest | 110 | 104.278 | 5.916 | 0,0133858 | 13:07:28–13:08:15 |
| `g24_high_rest` | reasoning high | rest | 110 | 104.278 | 11.600 | 0,0162278 | 13:08:36–13:09:39 |
| **Cộng G2** | | | | 1.147.055 | 83.637 | **0,1565240** | |
| **Cộng B17 (G4 0,0087972 + G2)** | | | | | | **0,1653212** | |

Pilot → lượt đủ (ước lại từ pilot / thật): baseline 0,01365 / 0,01479 (+8%); context10 0,02063 / 0,02264 (+10%); doc_order
0,01424 / 0,01474 (+3%); P1 0,01513 / 0,01639 (+8%); P2 0,01328 / 0,01483 (+12%); test baseline 0,00558 / 0,00656 (+17%);
test context10 0,00850 / 0,00973 (+15%); G2.4 none 0,01245 / 0,01343 (+8%), low 0,01242 / 0,01339 (+8%), high
0,01640 / 0,01623 (−1%). Bản report 13:02 ghi tổng G2 0,1134816 (chưa gồm G2.4 chạy đủ) — C review G2 m1. Không lượt nào > 1,5×, không lượt nào > 0,05 USD. Judge + `answer_type`: quota
Claude Code (29 sub-agent: dev 18, test 4, G2.4 7), 0 USD. \* giờ `finished` sớm hơn `started` vài giây ở một lượt: hai mốc lấy bằng
`time.strftime` lúc bắt đầu / kết thúc tiến trình con — chưa rõ nguyên nhân (đồng hồ WSL?), không ảnh hưởng số đo.

## 6. Lỗi và giới hạn

- Judge là Claude sub-agent (không có mốc người, như 7B). Nhiễu cả đường ước từ G2.0 vs 7B Run 1: 10/83 câu đổi
  Completeness; các kết luận "tốt hơn" dùng CI theo cặp trong cùng một lượt chấm mù.
- Mỗi sub-agent judge chấm 40 câu (7B: 10) để giảm số agent; mọi biến thể trộn lẫn trong cùng lô nên không lệch giữa biến
  thể. `answer_type` do sub-agent gắn theo chỉ dẫn cố định; không có người kiểm nhãn.
- Nhóm (a)/(b) dựa trên đoạn đúng của 40 câu dev có nhãn; câu không có nhãn đoạn đúng đều vào (b).
- 15 câu test đoạn đúng đã nhìn ở G1.6; test G2 (56 câu) mới dùng lần đầu cho sinh câu trả lời.
- Không so điểm 10 câu Golden mới với 7B Run 1 (A); đối chứng nhiễu đã bỏ 10 câu đó.

## 7. Bàn giao cho người kiểm (C)

Đọc §4.1–4.6, §5. Chạy lại free: `analyze` (dev: `--base g20_baseline --b g2_context10 g2_doc_order` và `--b
g2_p1_partial g2_p2_spec_rules`; test: `--base t_baseline --b t_context10 --judge judge_test`), `replay-citation`,
`check-judge [--judge judge_test]`. Diff: `backend/experiments/phase_8_1/g2_generate.py` (mới). Dữ liệu private:
`data/phase_8_1/g2/` (câu trả lời, meta, `judge/`, `judge_test/`).
