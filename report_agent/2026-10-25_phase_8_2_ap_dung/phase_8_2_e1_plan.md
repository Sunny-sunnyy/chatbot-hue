# Phase 8.2 E1 — plan: trả lời một phần, vẫn từ chối câu ngoài phạm vi (C33)

Người viết: C (Claude Opus 5.5, terminal `hue-rag-d6`) · 2026-10-25 16:46 +0700 (`date`) · Việc: C33 (A giao 16:41) ·
Spec: `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` (User duyệt 16:21, sha `dabae90b2b60`) §3.5, §5 B2 ·
Trạng thái: **chờ B review (theo `WORKFLOW.md` §9.1) rồi A duyệt sha** — chưa code, chưa gọi API, 0 USD.

Plan không chép câu hỏi, đáp án hay câu trả lời (repo public). Số trong plan do script in ra (§9).

## Căn cứ để review

1. File này — toàn bộ.
2. Spec 8.2 — §3.5 (mỗi thí nghiệm có plan, mốc = chatbot sau B1), §5 B1 (lượt B1 ↔ G2.1a là A/A context 10), §5 B2 (dòng E1,
   gạch đầu "Mỗi thí nghiệm chọn trên dev…" và "E1 thắng ⇒ trình User"), §7 (tiền, pilot).
3. `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g2_implementation.md` §4.2 (P1: từ chối nhầm 13 → 1, 2 câu ngoài phạm vi bị
   trả lời) và `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_implementation.md` §4 (số A/A context 10).
4. `skills/run-experiment/SKILL.md` §1 (khuôn, cỡ mẫu), §3.1 (nhiễu A/A), §4 (luật giữ / gỡ).

Người review được chạy lại hai script chỉ đọc ở §9 (0 USD) và đọc `backend/experiments/phase_8_1/g2_generate.py:55-80` (chữ P1),
`backend/llm/full_corpus_prompt.py` (prompt hiện tại), `backend/llm/citations.py` (validator).

## 1. Lớp bài toán

**Câu trong phạm vi bị từ chối nguyên câu vì context chỉ đủ cho một phần.** Prompt hiện tại có luật "bằng chứng không đủ ⇒ trả
đúng câu từ chối". Model áp luật này cho cả câu hỏi mà context trả lời được một phần (nhiều nhất ở câu nhiều nguồn / so sánh).
Người dùng nhận "không tìm thấy" dù kho có một phần thông tin.

**Ràng buộc:** câu ngoài phạm vi vẫn phải nhận **đúng nguyên văn câu từ chối**. Hợp đồng Phase 6 §10 yêu cầu đúng chuỗi đó, và
validator citation (`llm/citations.py`) chỉ cho câu trả lời không có `[n]` đi qua khi nó **đúng bằng** chuỗi đó. Lệch một chữ thì
API trả HTTP 500 `citation_integrity_error`.

## 2. Bằng chứng từ 8.1 và từ mốc B1 (đếm bằng máy, 0 USD)

| Đếm | Số | Nguồn |
|---|---:|---|
| Context 5 (G2.0) — câu trong phạm vi bị từ chối, dev chính (88) | 13 | `count_p1.py` |
| Context 10 (G2.1a) — như trên, dev chính / dev cả 120 câu (gồm câu không tự nhiên) | **7** / 9 | `count_p1.py` |
| Context 10 (G2.1a) — như trên, test chính (41) / test cả 56 câu | **1** / 3 | `count_p1.py` |
| Mốc B1 (context 10, lượt mới) — câu trong phạm vi bị từ chối, dev / test (cả nhóm) | 9 / 3 (giống G2.1a, 0 câu đổi) | `data/phase_8_2/b1/` |
| 7 câu dev chính context 10 còn từ chối: theo loại | nhiều nguồn 5, so sánh 1, hỏi thẳng 1 | `count_p1.py` |
| … trong đó P1 (context 5, 8.1) trả lời một phần | 6 / 7 | `count_p1.py` |
| P1: câu trả lời một phần (trong phạm vi, dev chính) | 17, cả 17 có `[n]`, 0 lỗi citation | phân tích §9 |
| … đến từ câu mốc từ chối: Completeness tăng / giữ / giảm | 12: 10 / 2 / 0; Accuracy giảm 0 | phân tích §9 |
| … đến từ câu mốc **trả lời đủ**: Completeness giảm | 5 câu, **3 giảm** (model rào thêm "nguồn không có…") | phân tích §9 |
| P1: câu ngoài phạm vi bị trả lời (dev 12) | 2 | `count_p1.py` |

**Vì sao P1 phạm sàn** (C đọc 2 câu, chi tiết private `data/phase_8_2/e1_plan/p1_detail.md`): cả 2 câu đều được sub-agent gắn
`answer_type = refusal`, tức là về ý thì model **có từ chối**, nhưng không theo đúng chuỗi chuẩn:

- câu 115: model **tự viết câu báo thiếu bằng lời khác**, không có `[n]`. Phép so chuỗi đếm là "đã trả lời"; API trả 500;
- câu 160: model trích **một ý chung** (cùng chủ đề, không trả lời điều được hỏi) có `[n]`, rồi nói thiếu phần được hỏi.

Chữ P1 gây ra cả hai: "Chỉ khi không có bằng chứng **liên quan** nào" — một ý chung cũng là "liên quan"; và P1 dạy model viết câu
báo thiếu bằng lời của mình.

## 3. Biến thể và giả định

**Mốc** = chatbot sau B1 (context 10 + NFC; lượt `data/phase_8_2/b1/b1_{dev,test}.jsonl`), prompt `ANSWER_SYSTEM_INSTRUCTIONS`.

**E1b — thay đúng câu luật từ chối** (như cách 8.1 dựng P1: `replace` câu `_REFUSAL_RULE`, có `assert` câu đó tồn tại). Mọi thứ
khác giữ nguyên (retrieval, context 10, model, reasoning mặc định, validator). Chữ ghi trước, không sửa sau khi thấy số:

```text
Nếu bằng chứng trả lời trực tiếp được một phần câu hỏi, trả lời phần đó kèm citation, rồi nói rõ phần nào nguồn dữ liệu không
có thông tin bằng một câu riêng không citation. Thông tin chỉ cùng chủ đề mà không trả lời điều được hỏi thì không tính là trả
lời được. Nếu không trả lời trực tiếp được ý nào của câu hỏi, trả đúng duy nhất câu sau, không thêm citation và không viết câu
báo thiếu nào khác:
Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này.
```

(dòng cuối là `INSUFFICIENT_ANSWER`, ghép bằng f-string như code hiện tại.)

| Giả định | Kiểm bằng máy | Kết quả |
|---|---|---|
| G1. Ở context 10 vẫn còn câu từ chối nhầm để cứu | đếm G2.1a / B1 | dev chính 7, test chính 1 — **ít** (§5) |
| G2. Các câu đó trả lời một phần được | P1 trên đúng 7 câu | 6 / 7 thành "partial" (ở context 5) |
| G3. Câu trả lời một phần vẫn có `[n]` ⇒ validator không chặn | P1 partial | 17 / 17 có `[n]`, 0 lỗi |
| G4. Lỗi sàn của P1 thuộc hai dạng E1b chặn bằng chữ (câu báo thiếu tự viết; ý chung) | đếm `[n]` + C đọc 2 câu | 1 không `[n]`, 1 có `[n]` ý chung — khớp |
| G5. Rủi ro: model rào cả câu đã đủ | P1, câu mốc trả lời đủ | 3 / 5 giảm Completeness ⇒ mức tụt T1 phải bắt được |

**Không chạy E1a (P1 nguyên văn trên context 10).** Lý do: 8.1 đã thấy P1 phạm sàn và đã rõ cơ chế (G4). Thêm E1a thì phải
Holm trên 2 biến thể, khi đó cần thắng ≥ 5 / 0 câu thay vì 4 / 0 (§5) trong khi chỉ có 7 câu để cứu. *Đề xuất*; A quyết (Q2 §10).

## 4. Tiêu chí ghi trước

```yaml
experiment_id: 8_2_e1b_partial_answer
baseline: chatbot sau B1 (context 10 + NFC), commit B1 khi A commit; lượt mốc data/phase_8_2/b1/b1_{dev,test}.jsonl
changed_variable: câu luật từ chối trong ANSWER_SYSTEM_INSTRUCTIONS -> chữ E1b (§3)
unchanged: [corpus, chunker, embedding, retrieval dense_bm25_rrf, context 10, model gpt-6-luna, reasoning mặc định, validator, judge]
data: {split: knowledge-base-hue/evaluation/phase_8_1/split.json, dev: 120 (12 out_of_scope), test: 56 (6 out_of_scope)}
realism: số chính = bỏ câu unnatural (golden_realism_final.jsonl sha 0b65d1c138d2) -> dev 88 / test 41 câu trong phạm vi
metrics:
  - {name: oos_answered, fn: "category == out_of_scope and not evaluation.full_corpus_eval.is_refusal(answer)",
     set: dev 12 + test 6, role: floor, floor: 0}
  - {name: refusal_in_scope, fn: "g2_generate.paired(base, e1b, 'refusal', in_scope) trên dev chính 88", better: down, role: decide,
     rule: "CI95 (bootstrap 10.000, seed 20261024) cận trên < 0 VÀ (thắng − thua) > số câu đổi từ chối ở A/A",
     noise: "A/A B1 ↔ G2.1a: 0 / 176 câu đổi từ chối ↔ trả lời (số B1, chờ A review)"}
  - {name: completeness_losses, fn: "số câu dev chính có Completeness E1b < mốc", role: tolerance, max: 3,
     noise: "A/A dev chính: 1 câu thua (1/86/1)"}
  - {name: accuracy_losses, fn: "như trên với Accuracy", role: tolerance, max: 3, noise: "A/A dev chính: 1 câu thua"}
  - {name: citation_errors, fn: "số câu dev 120 có citation_error (validator production)", role: tolerance, max: "mốc + 3",
     noise: "A/A dev: B1 6, G2.1a 4, 6 câu chỉ lỗi ở một lượt -> ±3"}
  - {name: uncited_non_refusal, fn: "câu không đúng chuỗi từ chối và không có [n] (API trả 500)", set: dev 120, role: watch}
  - {name: answer_type full/partial/refusal, fn: "sub-agent gắn nhãn như 8.1 G2", role: watch}
  - {name: completeness/accuracy/relevance mean diff + theo loại câu, role: watch}
  - {name: usd_per_case, output_tokens_mean, latency_p95, role: watch}
result: {paired_delta: null, ci95: null, wins_ties_losses: null}
conclusion: null   # tốt hơn / không đổi / kém hơn / chưa rõ
```

- **Luật giữ / gỡ** (`run-experiment` §4): "tốt hơn trên dev" khi đủ cả ba điều kiện: sàn 0 / 12; không chỉ số tolerance nào vượt
  mức; `refusal_in_scope` đạt rule trên. Thiếu một điều kiện ⇒ kém hơn (phạm sàn / vượt tụt) hoặc chưa rõ (không đạt chỉ số quyết).
- **Chỉ số theo dõi tụt mạnh** (ví dụ `uncited_non_refusal` tăng, Completeness theo loại câu giảm) ⇒ báo dù luật nói giữ.
- Đổi chữ E1b sau khi thấy số = **biến thể mới** (E1c): sửa plan → review lại → A duyệt sha mới. Tối đa 3 vòng cho bài toán này
  (`run-experiment` §4), rồi dừng và báo A / User.

## 5. Cỡ mẫu (tính trước khi chạy)

Chỉ số quyết là nhị phân theo câu. Ở mốc context 10 chỉ có **7 câu dev chính** có thể đổi theo chiều tốt (và 81 câu có thể đổi theo
chiều xấu). Tính bằng đúng `bootstrap_mean_diff` của harness (`sample_size.py`):

| n | thắng / thua | CI 95% của chênh | loại 0? |
|---:|---|---|---|
| 88 | 3 / 0 | [−0,080; 0,000] | không |
| 88 | **4 / 0** | [−0,091; −0,011] | **có** (p 0,031) |
| 88 | 5 / 1 | [−0,102; 0,000] | không |
| 88 | 7 / 1 | [−0,136; −0,011] | có |
| 41 | 1 / 0 | [−0,073; 0,000] | không |
| 41 | 3 / 0 | [−0,171; 0,000] | không |

- **Dev:** cần ≥ 4 câu hết từ chối và 0 câu mới bị từ chối (hoặc 7 / 1). P1 ở context 5 cứu 6 / 7 câu này ⇒ đủ khả năng, nhưng
  sát ngưỡng. Có thể ra "chưa rõ" — đây là kết quả hợp lệ, ghi trước.
- **Test: không thể cho CI 95% loại 0** (chỉ 1 câu chính, 3 câu cả nhóm có thể đổi). Vì vậy plan đề xuất **xác nhận hướng** trên
  test thay cho CI. Điều kiện: sàn 0 / 6; `refusal_in_scope` test ≤ mốc (không tăng); Completeness / Accuracy thua ≤ A/A test + 2
  (A/A test tính từ `data/phase_8_2/b1/` trước khi đo E1, ghi vào report); citation test ≤ mốc + 5 (A/A test: 10 câu chỉ lỗi ở một
  lượt). Cách này **lệch** `run-experiment` §4 ("xác nhận trên nhóm kiểm") ⇒ Q1 §10. Lớp kiểm cuối là User đọc mẫu (§7) và câu
  kín ở B3.

## 6. Cách chạy và chấm (khi plan được duyệt)

Harness: `backend/experiments/phase_8_2/e1.py` (mới, theo mẫu `g2_generate.py`). Gọi `answer_case` của evaluator production qua
tham số `OpenAIFullCorpusGenerator.from_environment(answer_instructions=E1B)` trên settings runtime sau B1. Logic biến thể chỉ ở
harness, không đổi code production. Người viết code: A giao; code theo `practical-project-coding`.

1. **Thử sàn trước (dev 12 câu ngoài phạm vi)** — rẻ nhất mà bắt được lỗi P1. Có ≥ 1 câu không đúng chuỗi từ chối ⇒ E1b **kém
   hơn (phạm sàn)**, dừng, không chạy tiếp. Lượt này cũng dùng làm pilot tiền (đủ ≥ 10 câu).
2. Pilot trong phạm vi: 10 câu dev rút theo seed 20261024 (như `g2_generate.select("pilot")`, bỏ câu đã chạy ở bước 1). Ước lại
   tiền; lượt đủ > 1,5 × ước ⇒ dừng, báo A.
3. Phần dev còn lại → gộp 120 câu → kiểm tất định: `top_chunk_ids`, `context_sources` bằng B1 120 / 120 (chỉ prompt đổi).
4. **Judge cùng lượt mù:** câu trả lời E1b dev + câu trả lời B1 dev trộn chung, id mờ, câu giống hệt chữ trong cùng câu hỏi chấm
   một lần. Sub-agent judge Claude mới (ghi model id, cùng model với judge B1), chỉ Read `full_corpus_judge_prompt.md` + lô. Gắn
   `answer_type` bằng sub-agent khác, chỉ dẫn cố định như 8.1. Chấm lại B1 trong lượt này, không dùng điểm B1 cũ.
5. Kết luận dev theo §4. Chỉ khi "tốt hơn": chạy test 56 (pilot 10 → phần còn lại), judge mù test (E1b + B1 test), xác nhận theo
   §5.
6. Phân tích theo tầng cho các câu đổi từ chối → trả lời: các `[n]` có trỏ đúng nguồn đóng gói không (validator); Accuracy của
   phần trả lời; câu báo thiếu có đúng là thông tin không có trong 10 đoạn đưa model không (sub-agent đọc, chỉ ở các câu đổi).

## 7. Khi E1b thắng — trình User (spec §5 B2, D4)

Đổi quy ước trả lời là đổi hợp đồng Phase 6 §10 ⇒ **User duyệt** trước khi vào chatbot. File đọc private
`data/phase_8_2/e1/user_read.md` gồm:

- **mọi câu đổi từ "từ chối" sang "trả lời"** ở dev + test (tối đa 7 + 3 = 10 câu theo §2; nhiều hơn thì lấy 10 câu bằng seed
  20261024). Mỗi câu ghi câu hỏi, câu trả lời mốc, câu trả lời E1b, các nguồn được trích. Không mù: User cần thấy cái gì đổi;
- 3 câu (seed) mà mốc trả lời đủ nhưng E1b trả lời có thêm "nguồn không có…" — để User thấy rủi ro rào thêm (G5);
- số đếm sàn / quyết / tụt, viết bằng lời thường.

## 8. Tiền và trần

- *Ước* (từ B1: 0,000204 USD / câu dev, 0,000222 / câu test; P1 tăng token ra +25%, chữ luật thêm ~45 token vào):
  ≈ 0,00022 USD / câu ⇒ dev 120 ≈ 0,026; test 56 ≈ 0,013; **tổng ≈ 0,04 USD** (spec §7: 0,03–0,05). Dừng ở bước 1 thì ≈ 0,003.
- **Trần E1: 0,06 USD**; vượt ước pilot > 50% ⇒ dừng, báo A. Trong trần 0,5 USD cả 8.2 (D5).
- Judge, `answer_type`, đọc tầng: quota Claude Code, 0 USD.

## 9. Script đã chạy cho plan (chỉ đọc, 0 USD; private)

```bash
cd backend
HF_HUB_OFFLINE=1 uv run python -I ../data/phase_8_2/e1_plan/count_p1.py    # §2 bảng; ghi p1_detail.md (private)
uv run python -I ../data/phase_8_2/e1_plan/sample_size.py                  # §5 bảng
```

Phân tích phụ (§2 các dòng "P1 partial", A/A citation dev / test) chạy bằng đoạn `uv run python -I` inline trên
`data/phase_8_1/g2/*.jsonl` và `data/phase_8_2/b1/b1_{dev,test}.jsonl`; người review tái lập bằng `attach_labels` +
`keep_realism(…, "main")` của `g2_generate` / `g1_retrieval`. Không mở câu kín, không đọc `data/phase_8_2/b0/`.

## 10. Câu hỏi cho A (trước khi duyệt)

- **Q1.** Test không đủ câu cho CI 95% (§5). Chấp nhận "xác nhận hướng" trên test thay CI, ghi giới hạn, User đọc mẫu là lớp kiểm
  cuối? Nếu không: E1 chỉ có thể ra "chưa rõ" trên test dù dev thắng.
- **Q2.** Một biến thể (E1b) hay thêm E1a (P1 nguyên văn) với Holm trên 2 (khi đó dev cần ≥ 5 / 0)?
- **Q3.** Số A/A dùng trong §4 / §5 lấy từ report B1 đang **chờ A review**. A review đổi số ⇒ C sửa phần số (không đổi luật), báo
  người review.
