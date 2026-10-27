# Plan: Phase 8.2 §10 — R1, mức suy luận `none` cho lượt sinh, trên mốc context 10

Người viết: C (Claude Opus 5.5, `hue-rag-5b`) · 2026-10-27 08:52 +0700 (`date`) · Việc: C46. Trạng thái: **bản nháp chờ B review**, rồi A ghi
"duyệt bản sha" (`WORKFLOW.md` §9.1). **Chưa code, chưa gọi API; 0 USD lúc viết.**

Plan không chép câu hỏi, đáp án hay câu trả lời. Repo public: chỉ có `case_index` và số đếm.

## Căn cứ để review

1. `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` **§10.2–§10.4** (bản A duyệt hiện hành `cd910c4c4169`): mốc, luật (a),
   dòng R1 ở bảng §10.3 (chỉ số quyết User 22:03), "Đo tốc độ theo khâu", sàn chung, Holm (R1 không vào họ), thứ tự, tiền.
2. `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g2_implementation.md` **§4.5** (G2.4: `none` ở context 5 — Completeness, từ chối nhầm, citation,
   token ra, USD).
3. `report_agent/2026-10-26_cai_tien_tung_khau/de_xuat_khau_tra_loi_C.md` **§1.4, §3 dòng R1, §4** (đề xuất R1 của C37, cách đo mức tụt luật (a)) và
   `phan_loai_loi_C.md` **§3** (9 câu `under-answer`; 120 / 168 từ chối đúng).
4. `skills/run-experiment/SKILL.md` §1, §3, §4.

Người review được chạy lệnh chỉ đọc và tính lại từ `data/phase_8_2/b1/` (câu trả lời + `judge/`) và `data/phase_8_1/g2/` (`g20_baseline`, `g24_none`).
Script C dùng để ra số ở §1–§2: `data/phase_8_2/r1_plan/c46_base.py`, `c46_aa.py` (chạy từ `backend/`, `PYTHONPATH=. uv run python …`; `c46_aa.py`
cần `git show 811d25d:backend/experiments/phase_8_2/b1.py > /tmp/c46mod/b1_811.py` trước, vì `b1.py` chỉ có trên `p82-b1`).

## 1. Lớp bài toán và giả định

**Lớp:** khâu sinh tốn token ra cho phần suy luận ẩn. Runtime không gửi tham số `reasoning` ⇒ model dùng mức mặc định (`medium`). Phần suy luận tính
vào `output_tokens` (giá 0,5 USD / 1M, gấp 5 lần token vào) và kéo dài thời gian sinh. R1 hỏi: bỏ suy luận có làm câu trả lời **rẻ / nhanh hơn rõ**
mà **chất lượng giữ** không (luật (a); "chất lượng cần thiết trước" ⇒ R1 đo sau cùng nhánh trả lời, spec §10.3).

**Đổi đúng một thứ:** `OpenAIFullCorpusGenerator.from_environment(settings, reasoning_effort="none")` — tham số đã có sẵn cho harness
(`backend/llm/generator_openai_full_corpus.py:94-118` ở `811d25d`, 8.1 G2.4 đã dùng). Prompt, context 10, retrieval, model, validator giữ nguyên.

| Giả định | Kiểm bằng máy (0 USD, đã chạy 08:4x 27/10) | Kết quả |
|---|---|---|
| G1. `none` không đổi đầu vào | 8.1 G2.4: `g24_none` ↔ `g20_baseline` | `input_tokens` và `top_chunk_ids` bằng nhau **120 / 120** ⇒ kiểm tất định ở §3 bước 3 có nghĩa |
| G2. Mốc B1 có bao nhiêu chỗ để giảm | `b1_dev` 120 câu (mọi câu có gọi model) | TB `output_tokens` **76,96**; `input_tokens` 1.658; USD / câu **0,000204316**; token ra chiếm **18,8 %** USD |
| G3. Ngưỡng USD ≤ 0,95× có với tới không | từ G2: giảm 5 % USD cần bớt ≥ 20,4 token ra / câu ⇒ TB ≤ **56,5** (0,735×) | *ước*: ở context 5 `none` cho 78,8 → 54,3 (0,689×) ⇒ ở context 10 ≈ 53 token, USD ≈ **0,94×** — **sát ngưỡng** |
| G4. Ngưỡng `output_tokens` ≤ 0,9× | ≤ 69,3 token / câu | *ước* 0,69× ⇒ **dễ qua** nếu tỉ lệ context 5 giữ |
| G5. Nhiễu của hai chỉ số quyết | A/A B1 ↔ G2.1a dev 120 (cùng cấu hình, hai ngày) | USD: SD chênh theo câu 1,41e-5 ⇒ **±1,24 %**; `output_tokens`: SD 28,3 ⇒ **±6,6 %** (1,96 × SE / TB). TB hai lượt bằng nhau (76,96 / 76,96) |
| G6. Rủi ro sàn: `none` từ chối ít hơn | G2.4 context 5: từ chối nhầm 13 → 4, OOS bị trả lời 0 | ở mốc B1 dev chính còn 7 câu từ chối (48, 67, 68, 113, 120, 167, 168); **120, 168 là từ chối đúng** (context không có fact, C36) ⇒ sàn |
| G7. Rủi ro trả lời gọn hơn | G2.4: token ra −31 %; C36: 9 câu `under-answer` ở mốc (28, 38, 41, 51, 65, 66, 93, 141, 173) | theo dõi riêng 9 câu này + mức tụt Completeness |
| G8. Citation | G2.4: lỗi citation 4 → 8 theo định nghĩa cũ; validator v2: 0 → 2 (`sua_3c_citation_v2.md`) | mốc B1 v2: **0** lỗi (dev + test); mức tụt ≤ +2 câu |

## 2. Tiêu chí ghi trước

```yaml
experiment_id: p82_r1_reasoning_none
baseline: p82-b1 811d25d — context 10 + NFC, ANSWER_SYSTEM_INSTRUCTIONS, không gửi reasoning (= medium); câu trả lời mốc data/phase_8_2/b1/b1_{dev,test}.jsonl
changed_variable: reasoning_effort None -> "none" (tham số harness của OpenAIFullCorpusGenerator.from_environment)
unchanged: [corpus, chunker, e5-small, index, retrieval dense_bm25_rrf pool 30, context 10, prompt, gpt-6-luna, answer_max_output_tokens 2048, validator, judge prompt]
data: {split: split.json e2b1788dfbbc, dev: 120 (12 OOS), test: 56 (6 OOS), realism: 0b65d1c138d2 -> dev chính 88 / test chính 41}
noise_AA: "B1 ↔ G2.1a chấm cùng lượt mù data/phase_8_2/b1/judge/ (C tính lại 27/10, c46_aa.py) — dev chính: Completeness 1/86/1, Accuracy 1/86/1;
  test chính: Completeness 3/38/0, Accuracy 2/38/1; từ chối đổi 0 (dev + test); citation v2 0 vs 0. 'A/A' của một chỉ số = max(thắng, thua) của B1 − G2.1a"
metrics:
  # sàn (spec §10.2 sàn chung)
  - {name: OOS bị trả lời, fn: "category == out_of_scope and not row['refusal']", set: dev 12 + test 6, role: floor, floor: 0}
  - {name: 120 / 168 vẫn từ chối, set: dev, role: floor, floor: "cả hai refusal"}
  - {name: câu không citation mà không phải câu từ chối chuẩn (API 500), fn: "citation_error == 'Grounded answer has no citation'", set: 176, role: floor, floor: 0}
  - {name: lỗi kỹ thuật, fn: "row['error'] is not None", set: 176, role: floor, floor: 0}
  # quyết (luật (a), dòng R1 spec §10.3 — User 22:03)
  - {name: USD / câu, def: "TB usd R1 ÷ TB usd B1, dev 120 (usd = cost_usd(input_tokens, output_tokens) từ usage provider)", role: decide}
  - {name: output_tokens / câu, def: "TB output_tokens R1 ÷ TB B1, dev 120", role: decide}
  - rule: "R1 qua khi (USD ≤ 0,95 HOẶC output_tokens ≤ 0,9) VÀ chỉ số còn lại ≤ 1,00 (ước lượng điểm). Báo kèm CI 95 % của chênh theo câu
          (bootstrap_mean_diff, seed 20261024) quy ra % mốc — chỉ báo, không đổi luật"
  # mức tụt — Completeness theo spec §10.2 luật (a); các dòng còn lại C thêm (chặt hơn spec, mượn từ mức tụt luật (i)) — A chốt khi duyệt
  - {name: Completeness dev chính, set: 88, role: tolerance, max: "chênh TB ≥ −0,1 VÀ số câu tụt ≤ A/A + 3 = 4"}
  - {name: Accuracy dev chính, set: 88, role: tolerance, max: "số câu tụt ≤ A/A + 3 = 4"}                       # C thêm
  - {name: từ chối nhầm dev chính (false_refusal), fn: "paired_stats(b1, r1, 'false_refusal')", role: tolerance, max: "số câu từ chối mới ≤ A/A + 1 = 1"}   # C thêm
  - {name: lỗi citation v2, fn: "g2_generate.citation_error(answer, context_sources, single_source_policy=False) cho CẢ mốc và R1", set: 176, role: tolerance, max: "tăng ≤ 2 câu"}   # C thêm
  - {name: Completeness test chính, set: 41, role: tolerance, max: "chênh TB ≥ −0,1 VÀ số câu tụt ≤ A/A + 3 = 6"}
  - {name: Accuracy test chính, set: 41, role: tolerance, max: "số câu tụt ≤ A/A + 3 = 5"}
  - {name: từ chối nhầm test chính, role: tolerance, max: "số câu từ chối mới ≤ 1"}
  # theo dõi
  - {name: Completeness / Accuracy / Relevance chênh TB + CI + theo loại câu, set: dev chính, test chính, role: watch}
  - {name: 9 câu under-answer C36 (28, 38, 41, 51, 65, 66, 93, 141, 173), def: "số câu Completeness tụt / tăng", role: watch}
  - {name: câu đổi từ chối -> trả lời (dev + test), def: "liệt kê case_index; câu trả lời có câu không citation kiểu 'nguồn không có…' (đếm máy như R2)", role: watch}
  - {name: R4 số không có trong đoạn được trích, fn: "experiments.phase_8_2.r4_numbers (main 2c7ecfd) trên r1_dev / r1_test", role: watch}
  - {name: latency sinh p50 / p95 (latency_ms của lượt sinh), def: "R1 so B1, kèm CI chênh theo câu; B1 đo ngày 26/10 ⇒ khác phiên", role: watch}
  - {name: USD / câu và output_tokens / câu trên test 56, role: watch}            # A/A test ±22 % token ra ⇒ không quyết được
result: null
conclusion: null   # tốt hơn / không đổi / kém hơn / chưa rõ — dựa judge ⇒ TẠM tới khi B0 xong (spec §10.2)
```

**Luật giữ** (spec §10.2 luật (a), `run-experiment` §4): dev đủ sàn, không vượt mức tụt nào, chỉ số quyết qua ⇒ chạy test. Test đủ sàn và mức tụt
("không làm hỏng", User đồng ý Q2 §10.6 sáng 27/10) ⇒ **"tốt hơn" theo luật (a)** (rẻ / nhanh hơn, chất lượng giữ). Chỉ số quyết không qua mà chất
lượng giữ ⇒ "không đổi". Phạm sàn hoặc vượt mức tụt ⇒ "kém hơn".

**Cỡ mẫu / độ phân giải** (luật (a) không cần CI > 0 cho chất lượng — chỉ cần không tụt quá mức):
- Mức tụt Completeness dev chính: 4 câu tụt 1 điểm ⇒ chênh TB −0,045; 4 câu tụt 2 điểm ⇒ −0,091 (vẫn ≥ −0,1); 5 câu tụt ⇒ trượt điều kiện "số câu".
  Điều kiện "số câu ≤ 4" là điều kiện chặt hơn trong hai điều kiện ở hầu hết trường hợp.
- Chỉ số quyết đo trên **dev 120** (cả 120 câu có gọi model, OOS cũng gọi): USD phân giải ±1,24 %, nên ngưỡng 0,95× cách nhiễu ~4 lần;
  `output_tokens` ±6,6 %, ngưỡng 0,9× cách nhiễu ~1,5 lần. Ngưỡng là ước lượng điểm (spec); CI chỉ báo.
- **Ghi trước:** USD ≤ 0,95× **sát ngưỡng** (ước 0,94×, G3) — có thể chỉ qua nhờ nhánh `output_tokens`; nếu `output_tokens` cũng > 0,9× ⇒ "không đổi".
  Sàn 120 / 168 **có thể vỡ** (G6) ⇒ "kém hơn" là kết quả hợp lệ.
- Test (56 câu) chỉ kiểm "không làm hỏng"; tiền / token trên test chỉ theo dõi (A/A test: `output_tokens` 113,4 vs 84,1, ±22 %).
- **Holm:** R1 không vào họ (spec §10.2).

## 3. Cách chạy (khi plan được duyệt)

Harness mới `backend/experiments/phase_8_2/r1.py` (C viết, B review cùng report). Nhánh `p82-r1` tạo từ `811d25d`, worktree `/tmp/c_r1`
(bẫy worktree: `Project_Status.md` §8 — chạy bằng `uv run --project /home/minhhieu/hue_rag`, gỡ symlink + worktree khi xong).
Khung giống `r2.py` (`origin/p82-r2`): tập câu, `generate` qua `full_corpus_eval.answer_case` production, `check`, lô judge mù, `analyze`. Khác duy nhất
ở `generate`: `OpenAIFullCorpusGenerator.from_environment(settings, reasoning_effort="none")`. `r2.py` không có trên `811d25d` ⇒ phần khung chép sang
`r1.py` (~150 dòng), không import từ nhánh đã gác. Từ chối ghi đè mọi file kết quả (`raise SystemExit('exists')`, `run-experiment` §3.8).

1. **Sàn trước: 12 câu OOS dev.** ≥ 1 câu bị trả lời ⇒ **kém hơn (phạm sàn)**, dừng.
2. **Pilot trong phạm vi: 120, 168 + 9 câu under-answer** (11 câu). 120 hoặc 168 bị trả lời ⇒ **kém hơn (phạm sàn)**, dừng. 9 câu U chỉ để xem sớm
   (không dừng). **Pilot tiền = bước 1 + 2 (23 câu)**; ước lại phần còn lại theo USD / câu của 11 câu trong phạm vi. Lượt đủ > 1,5 × ước ⇒ dừng, báo A.
3. Phần dev còn lại (97 câu) ⇒ gộp `r1_dev.jsonl` 120 câu. **Kiểm tất định:** `top_chunk_ids`, `context_sources`, `input_tokens` = B1 ở 120 / 120 (G1).
   Lệch ⇒ dừng, tìm nguyên nhân. Tính chỉ số quyết (dev 120) bằng script, in bảng.
4. **Judge cùng lượt mù:** câu trả lời R1 dev + **B1 dev chấm lại** trong cùng lô, id mờ; câu giống hệt chữ trong cùng câu hỏi chấm một lần.
   Sub-agent judge Claude mới (ghi model id) chỉ Read `full_corpus_judge_prompt.md` + lô. Không gắn `answer_type` (từ chối đếm bằng máy).
5. Kết luận dev theo §2. Chỉ khi dev đạt: test 56 (pilot 10 seed ⇒ phần còn lại), judge mù test (R1 + B1 test), xác nhận "không làm hỏng" theo §2.
6. R4 trên `r1_dev` / `r1_test` từ working tree chung (`main`), theo dõi.
7. Report `phase_8_2_r1_implementation.md` (bảng do script in), commit + push `p82-r1` (không merge) ⇒ B review.

## 4. Tiền và dừng

- *Ước* (B1 thật: 0,000204 USD / câu dev, 0,000221 / câu test; token ra *ước* 0,69×): ≈ 0,000192 / câu dev, ≈ 0,000204 / câu test.
  - dev 120 ≈ 0,023;
  - test 56 ≈ 0,011;
  - **tổng ≈ 0,034 USD** (khớp spec §10.3 "≈ 0,034"). Dừng ở bước 1 ⇒ ≈ 0,002.
- **Trần R1 đề xuất: 0,05 USD** (A chốt). Pilot vượt ước > 50 % ⇒ dừng, báo A. Trong trần 8.2 0,5 USD (đã dùng 0,0396; K3 giữ 0,20).
- **Dừng thêm:** lỗi kỹ thuật > 0 ⇒ tìm nguyên nhân, không fallback; kiểm tất định bước 3 lệch ⇒ dừng; đổi mức khác (`low`) = biến thể mới, plan mới
  (spec §10.3 "không chạy `low` / `high`").
- Judge: quota Claude Code, 0 USD. Không ghi Qdrant, không sửa corpus / Golden / split / đoạn đúng, không mở câu kín.

## 5. Khi R1 đạt — điều A cần biết trước khi đưa vào chatbot

- **R1 vào chatbot phải sửa code và hợp đồng, không chỉ đổi config:** `settings_loader.py:43-55` (`811d25d`) **cấm** khóa `reasoning_effort` trong
  `full_corpus_generation`; amendment Phase 6 `2026-10-23-phase-6-gpt-6-luna-amendment.md:54` và `2026-10-01-…-openai-baseline-amendment.md:32` ghi
  "không cấu hình / không truyền reasoning"; test `test_openai_full_corpus_generator.py:33` ghim `reasoning is None`. Spec §10.4 cho A tự đưa biến
  thể luật (a); C **đề nghị A trình User** vì đổi một điều cấm của hợp đồng Phase 6 (A quyết).
- Kết luận dựa judge là **tạm** tới khi B0 xong. R1 chỉ vào chatbot sau khi context 10 đã vào (spec §10.2). Ghép với biến thể khác (K3 nếu nhận) =
  lượt xác nhận riêng so mốc B1 (spec §10.3 "Ghép").
- Report ghi đủ "hiệu suất = tiền + tốc độ": USD / câu, `output_tokens` / câu, latency p50 / p95 (kèm CI, khác phiên).

## 6. Câu hỏi cho A (trả lời khi duyệt)

- **Q1 — mức tụt C thêm** (Accuracy ≤ 4, từ chối nhầm ≤ +1, citation v2 ≤ +2, cùng mức test): spec §10.2 luật (a) chỉ ghi Completeness. C thêm vì G2.4
  cho thấy `none` đổi đúng các mặt này (từ chối −9, citation +4 theo định nghĩa cũ). Giữ hay bỏ?
- **Q2 — quyền:** nhánh `p82-r1` (tạo + commit + push, không merge), worktree `/tmp/c_r1`, paid `gpt-6-luna` ≤ 0,05 USD, sub-agent judge Claude.
  Quyền phiên 27/10 hiện chưa có dòng cho C (`CURRENT_HANDOFF.md` mục Quyền).
- **Q3 — thời điểm:** spec §10.3 xếp R1 sau cùng nhánh trả lời ("chất lượng trước"); R2 đã dừng, R3 NOT RUN ⇒ R1 chạy được ngay sau khi duyệt, song
  song với K3 (file không chồng: `r1.py` / `data/phase_8_2/r1/` so với `k3`). C đề nghị chạy sau khi B54 xong pilot K3 để hai lượt paid không chồng
  trần cùng lúc — A chọn.
