# Plan: Phase 8.2 §10 — R2, trả lời phần có căn cứ (= E1b) trên mốc context 10

Người viết: C (Claude Opus 5.5, `hue-rag-b5`) · 2026-10-26 21:50 +0700 (`date`) · Việc: C40. Bản này **thay** plan E1
(`phase_8_2_e1_plan.md`, sha `f86240418ca1`). File E1 giữ nguyên để đọc lý do. Trạng thái: **bản nháp chờ B review**, rồi A ghi "duyệt bản sha"
(`WORKFLOW.md` §9.1). **Chưa code, chưa gọi API; 0 USD lúc viết.**

Plan không chép câu hỏi, đáp án hay câu trả lời. Repo public: chỉ có `case_index` và số đếm.

## Căn cứ để review

1. `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` **§10.2–§10.4** (bản A duyệt hiện hành `cd910c4c4169`, commit `ce8b310`; gồm dòng
   §10.2 "Đo tốc độ theo khâu"): mốc, luật (i), mức tụt,
   sàn, Holm, cỡ mẫu, tiền.
2. `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_e1_plan.md` **§2, §3, §6, §7**: bằng chứng P1 8.1, chữ E1b ghi trước, cách chạy, trình User.
3. `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_C.md` **§3** (5 câu nhóm P; 120 / 168 từ chối đúng) và
   `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k1_plan.md` **§4 bảng A/A** (A/A dev chính / test chính, C tính lại độc lập ở C41 vòng 2).
4. `skills/run-experiment/SKILL.md` §1, §3, §4.

Người review được chạy lệnh chỉ đọc và tính lại từ `data/phase_8_2/b1/` và `data/phase_8_1/g2/` (`attach_labels`, `keep_realism`).

## 1. Lớp bài toán và giả định

**Lớp:** câu trong phạm vi bị từ chối nguyên câu, trong khi 10 đoạn đưa model có **một phần** fact. Prompt hiện tại làm đúng luật "không đủ ⇒
từ chối". Người dùng nhận "không tìm thấy" dù kho có một phần câu trả lời.

**Đổi đúng một thứ:** câu luật từ chối trong `ANSWER_SYSTEM_INSTRUCTIONS` được thay bằng chữ E1b. Cách thay giống P1 8.1: `replace` đúng
`_REFUSAL_RULE`, có `assert`. Chữ E1b **giữ nguyên văn plan E1 §3**, ghi trước từ 25/10, không sửa sau khi thấy số:

```text
Nếu bằng chứng trả lời trực tiếp được một phần câu hỏi, trả lời phần đó kèm citation, rồi nói rõ phần nào nguồn dữ liệu không
có thông tin bằng một câu riêng không citation. Thông tin chỉ cùng chủ đề mà không trả lời điều được hỏi thì không tính là trả
lời được. Nếu không trả lời trực tiếp được ý nào của câu hỏi, trả đúng duy nhất câu sau, không thêm citation và không viết câu
báo thiếu nào khác:
{INSUFFICIENT_ANSWER}
```

| Giả định | Kiểm bằng máy (0 USD, đã chạy 21:5x) | Kết quả |
|---|---|---|
| G1. Mốc B1 còn câu từ chối trong phạm vi | `b1_dev` / `b1_test`, bỏ unnatural + OOS | dev chính **7** câu (48, 67, 68, 113, 120, 167, 168); test chính 1 |
| G2. Trong 7 câu đó, bao nhiêu câu có một phần fact trong context | C36 §3 (đoạn đúng × 10 đoạn) | **5** (48, 67, 68, 113, 167: 1/2 – 3/4 fact). 120, 168: **0 fact ⇒ từ chối đúng** |
| G3. Câu trả lời một phần vẫn có `[n]` | P1 8.1 (plan E1 §2) | 17 / 17 có `[n]`, 0 lỗi citation |
| G4. Lỗi sàn của P1 (câu báo thiếu tự viết; ý chung) bị chữ E1b chặn | plan E1 §2 (đọc 2 câu) | khớp hai câu chữ E1b thêm vào |
| G5. Rủi ro: model rào thêm ở câu đã đủ | P1: 3 / 5 câu mốc đủ bị giảm Completeness | phải bắt bằng mức tụt §2 |
| G6. OOS mốc | B1: 0 / 18 bị trả lời | sàn có nghĩa |

## 2. Tiêu chí ghi trước

```yaml
experiment_id: p82_r2_partial_answer_e1b
baseline: p82-b1 811d25d — context 10 + NFC, prompt ANSWER_SYSTEM_INSTRUCTIONS, reasoning mặc định; câu trả lời mốc data/phase_8_2/b1/b1_{dev,test}.jsonl
changed_variable: câu luật từ chối -> chữ E1b (§1)
unchanged: [corpus, chunker, e5-small, index, retrieval dense_bm25_rrf pool 30, context 10, gpt-6-luna, reasoning, validator, judge prompt]
data: {split: split.json e2b1788dfbbc, dev: 120 (12 OOS), test: 56 (6 OOS), realism: 0b65d1c138d2 -> dev chính 88 / test chính 41}
noise_AA: "B1 ↔ G2.1a chấm cùng lượt mù data/phase_8_2/b1/judge/ — dev chính C 1/86/1, A 1/86/1, đổi từ chối 0; test chính C 3/38/0, A 2/38/1, đổi từ chối 0"
metrics:
  # sàn
  - {name: OOS bị trả lời, fn: "category == out_of_scope and not full_corpus_eval.is_refusal(answer)", set: dev 12 + test 6, role: floor, floor: 0}
  - {name: 120 / 168 vẫn từ chối, set: dev, role: floor, floor: "cả hai is_refusal"}      # spec §10.2; context không có fact (C36)
  - {name: câu không citation mà không phải câu từ chối chuẩn (API 500), set: 176, role: floor, floor: 0}
  - {name: lỗi kỹ thuật, set: 176, role: floor, floor: 0}
  # quyết
  - {name: false_refusal, fn: "full_corpus_eval.paired_stats(a_values, b_values, 'false_refusal'): a / b = float(refusal) của B1 / R2, cùng thứ tự case_index, dev chính 88",
     better: down, role: decide,
     rule: "CI 95% nằm hẳn dưới 0 VÀ Holm họ {R2, R3} CỐ ĐỊNH (p × 2 < 0,05, dù R3 có chạy hay không)", noise: "A/A 0 câu đổi", ceiling: 5}
  # mức tụt (spec §10.2 luật (i))
  - {name: số câu Completeness tụt, set: dev chính 88, role: tolerance, max: "A/A + 3 = 4"}
  - {name: số câu Accuracy tụt, set: dev chính 88, role: tolerance, max: "A/A + 3 = 4"}
  - {name: số câu Completeness tụt, set: test chính 41, role: tolerance, max: "A/A + 3 = 6"}
  - {name: số câu Accuracy tụt, set: test chính 41, role: tolerance, max: "A/A + 3 = 5"}
  - {name: false_refusal test chính, role: tolerance, max: "tăng ≤ A/A + 1 = 1 câu"}
  - {name: lỗi citation v2, fn: "select_cited_sources(answer, packed.sources) ném CitationIntegrityError; packed dựng lại như r4_numbers.check_file; áp cho CẢ mốc và R2", set: 176, role: tolerance, max: "tăng ≤ 2 câu"}
  - {name: USD / câu (usage log), role: tolerance, max: "+20 % so mốc; 0 lần gọi API thêm"}
  - {name: output_tokens / câu (tốc độ khâu sinh, spec §10.2 "Đo tốc độ theo khâu"), def: "TB output_tokens R2 ÷ TB B1, dev 120 câu có gọi model", role: tolerance, max: "+20 %"}
  - {name: latency sinh p50 / p95 (latency_ms của chính lượt sinh), def: "R2 so B1, kèm CI bootstrap chênh theo câu; B1 đo phiên khác", role: watch}
  # theo dõi
  - {name: answer_type full / partial / refusal (sub-agent như 8.1), role: watch}
  - {name: Completeness / Accuracy / Relevance chênh TB + theo loại câu, role: watch}
  - {name: R4 số không có trong đoạn được trích (experiments.phase_8_2.r4_numbers), set: dev + test, role: watch}
  - {name: câu mốc trả lời đủ mà R2 thêm câu "nguồn không có…" (đếm máy: có câu không citation trong câu trả lời có citation), role: watch}
  - {name: output_tokens TB theo loại câu, role: watch}
result: null
conclusion: null   # tốt hơn / không đổi / kém hơn / chưa rõ — dựa judge ⇒ TẠM tới khi B0 xong (§10.2)
```

**Luật giữ** (`run-experiment` §4, spec §10.2 luật (i)): dev đủ sàn, không vượt mức tụt nào, và chỉ số quyết qua ⇒ chạy test. Test đủ sàn và
mức tụt ("không làm hỏng", chờ User §10.6 Q2) ⇒ **"tốt hơn" (tạm)**. Kể cả khi đạt luật, **R2 vẫn chờ User duyệt**, vì nó đổi hợp đồng Phase 6
§10 (spec D4, §10.4) — xem §5.

**Cỡ mẫu** (`bootstrap_mean_diff`, seed 20261024; số đã tính ở C37 / C38): `false_refusal` là giá trị nhị phân theo câu.
- n 88, 5 thắng / 0 thua: p 0,013, × 2 = 0,026 < 0,05 ⇒ **qua**.
- 4 / 0: p 0,031, × 2 = 0,062 ⇒ **trượt**.

Trần là 5 câu, nên **phải cứu cả 5 và không thêm câu từ chối mới nào**. Ở context 5, P1 cứu 6 / 7 câu đang còn từ chối (plan E1 §2).
**Ghi trước: "chưa rõ" rất có thể** — đó là kết quả hợp lệ. Test chính chỉ có 1 câu từ chối nên không thể thấy "tốt hơn"; test chỉ dùng để kiểm
"không làm hỏng".

**Vì sao tốc độ đo bằng `output_tokens`, không bằng ms** (B49 M-1; spec §10.2 "Đo tốc độ theo khâu"): latency một lần gọi model dao động
mạnh. B1 ↔ G2.1a cùng đầu vào cho SD chênh theo câu ≈ 808 ms, nên 30 câu chỉ phân giải được ±289 ms, không phân xử được ngưỡng +50 ms.
`output_tokens` / câu đã có trong usage của lượt sinh (0 USD thêm) và nhiễu nhỏ: A/A B1 ↔ G2.1a dev 120 cho TB 77,0 / 77,0, SD chênh theo
câu 28 token ⇒ **±6,6 %** với n 120 (spec §10.2 bản `cd910c4c4169`). Ngưỡng +20 % cách nhiễu khoảng 3 lần. Ở context 5, P1 làm token ra +25 % (78,8 →
98,8), đúng sát ngưỡng +20 %. **Ghi trước: R2 có thể vượt mức tụt này** ⇒ luật (i) không tự nhận ⇒ trình User kèm số. R2 đằng nào cũng trình
User, nên điểm này không đổi luồng. Latency ms vẫn báo (p50 / p95 kèm CI) vì User theo dõi "tiền + tốc độ". **Bỏ lượt latency 30 câu**
(0,012 USD) của bản trước.

## 3. Cách chạy (khi plan được duyệt)

Harness mới `backend/experiments/phase_8_2/r2.py` (C viết, B review). Theo mẫu `phase_8_2/b1.py` + `g2_generate.py`: gọi `answer_case` của
evaluator production, với `OpenAIFullCorpusGenerator.from_environment(answer_instructions=E1B_INSTRUCTIONS)` trên settings mốc `811d25d`. Chạy
trong worktree `/tmp/c_r2` trên nhánh `p82-r2` tạo từ `811d25d` (bẫy worktree: `Project_Status.md` §8). Logic biến thể chỉ ở harness; không
sửa production. Từ chối ghi đè file kết quả.

1. **Sàn trước: 12 câu OOS dev.** Có ≥ 1 câu không đúng chuỗi từ chối ⇒ **kém hơn (phạm sàn)**, dừng.
2. **120 / 168 + 5 câu nhóm P** (7 câu dev): xem sớm sàn 120 / 168. Phạm sàn ⇒ dừng. Lượt này chỉ để dừng sớm; kết luận vẫn tính trên đủ 88 câu.
   **Pilot tiền = bước 1 + 2 (19 câu), ước lại phần còn lại theo USD / câu của 7 câu trong phạm vi** (B49 m-1: câu OOS từ chối ⇒ token ra
   ít, ước thấp). Lượt đủ > 1,5 × ước ⇒ dừng, báo A.
3. Phần dev còn lại ⇒ gộp 120 câu. Kiểm tất định: `top_chunk_ids`, `context_sources` = B1 ở 120 / 120 (chỉ prompt đổi).
4. **Judge cùng lượt mù:** câu trả lời R2 dev + **B1 dev chấm lại** trong cùng lô, id mờ. Câu giống hệt chữ trong cùng câu hỏi thì chấm một lần.
   Sub-agent judge Claude mới (ghi model id) chỉ Read `full_corpus_judge_prompt.md` + lô. `answer_type` do sub-agent khác gắn.
5. Kết luận dev theo §2. Chỉ khi dev đạt: test 56 (pilot 10 ⇒ phần còn lại), judge mù test (R2 + B1 test), xác nhận theo §2.
6. Phân tích theo tầng cho các câu đổi từ chối ⇒ trả lời:
   - `[n]` có trỏ nguồn đóng gói không (validator v2);
   - R4 có cờ không;
   - câu báo thiếu có đúng là phần không có trong 10 đoạn không (C đọc, chỉ ở câu dev đổi).

## 4. Tiền và dừng

- *Ước* (B1 thật: 0,000204 USD / câu dev, 0,000221 / câu test; P1 ở context 5: USD ×1,11): ≈ 0,000227 / câu.
  - dev 120 ≈ 0,027;
  - test 56 ≈ 0,013;
  - **tổng ≈ 0,040 USD** (bỏ lượt latency, B49 M-1).
  - Dừng ở bước 1 ⇒ ≈ 0,003.

  Khớp spec §10.3 (R2 ≈ 0,04).
- **Trần R2: 0,06 USD** (A). Pilot (bước 1 + 2) vượt ước > 50 % ⇒ dừng, báo A. Trong trần 8.2 0,5 USD (đã dùng 0,0369).
- **Dừng thêm:**
  - lỗi kỹ thuật > 0 ⇒ tìm nguyên nhân, không fallback;
  - kiểm tất định bước 3 lệch ⇒ dừng;
  - đổi chữ E1b sau khi thấy số = biến thể mới (E1c): plan mới, review lại. Tối đa 3 vòng (`run-experiment` §4).
- Judge, `answer_type`, đọc tầng: quota Claude Code, 0 USD. Không ghi Qdrant, không sửa corpus / Golden / split / đoạn đúng, không mở câu kín.

## 5. Khi R2 đạt — trình User (spec D4, §10.4)

File đọc private `data/phase_8_2/r2/user_read.md`:
- **mọi câu đổi từ "từ chối" sang "trả lời"** ở dev + test (≤ 5 + 1). Mỗi câu ghi câu hỏi, câu trả lời mốc, câu trả lời R2, nguồn được trích.
  Không mù, vì User cần thấy cái gì đổi;
- 3 câu (seed) mà mốc trả lời đủ nhưng R2 rào thêm "nguồn không có…", để User thấy rủi ro (G5);
- số sàn / quyết / tụt / token ra / latency / tiền, viết bằng lời thường.

Kết luận dựa judge là **tạm** tới khi B0 xong (spec §10.2). R2 chỉ vào chatbot sau khi context 10 đã vào và User duyệt.

## 6. Khác plan E1 (đối chiếu)

| Mục | Plan E1 (`f86240418ca1`) | Plan R2 (bản này) | Lý do |
|---|---|---|---|
| Mốc | B1 trước rebase | `811d25d` (B41) | spec §10.2 |
| Hàm so cặp | `g2_generate.paired` + tên `refusal_in_scope` | `full_corpus_eval.paired_stats(…, 'false_refusal')` (chiều "thấp là tốt") | gói 3a, C-02 |
| Citation | validator lúc đó (nhiễu A/A ±3) | validator v2, tính lại cho **cả hai** lượt (A/A 0 vs 0) | gói 1a / 3c |
| Trần | 7 câu | **5** câu; 120 / 168 thành **sàn** | C36 §3 |
| Ngưỡng | ≥ 4 / 0 (không Holm) | **5 / 5** câu, Holm họ {R2, R3} cố định | spec §10.2–§10.3 |
| Mức tụt | Completeness / Accuracy thua ≤ 3 câu (dev); test "xác nhận hướng" | dev ≤ A/A + 3 (4 / 4); test ≤ A/A + 3 (6 / 5); từ chối nhầm test ≤ +1; citation ≤ +2; USD ≤ +20 %; `output_tokens` / câu ≤ +20 % (latency ms chỉ theo dõi) | spec §10.2 luật (i) + "Đo tốc độ theo khâu" |
| Q2 E1a | đề xuất không chạy | không chạy (spec §10.3 chỉ có R2) | — |
| Theo dõi | — | thêm R4 | spec §10.5 |

## 7. A đã trả lời (22:0x)

- **Q1 — giữ đo tốc độ** (User 22:0x: "ngoài tối ưu tiền thì còn phải để ý tốc độ"). Sau B49 M-1, A 22:2x thêm spec §10.2 "Đo tốc độ theo
  khâu": khâu sinh đo bằng `output_tokens` / câu (≤ +20 %), latency ms chỉ theo dõi ⇒ bỏ lượt 30 câu xen kẽ (§2).
- **Q2 — quyền:** nhánh `p82-r2` (tạo + commit + push, không merge), paid `gpt-6-luna` ≤ 0,06 USD, sub-agent judge Claude — A ghi khi duyệt sha
  sau B review. Trước khi duyệt: C được dựng worktree `/tmp/c_r2` + nhánh `p82-r2` từ `811d25d` và viết harness; **không** chạy lượt có phí,
  kể cả bước 1 (OOS).

## Sửa sau review B49 (22:05 26/10/2026 +0700, `date`)

| Finding | Sửa |
|---|---|
| M-1 latency khâu sinh không phân xử được | Theo spec §10.2 "Đo tốc độ theo khâu": mức tụt tốc độ = `output_tokens` / câu ≤ +20 % (dev 120); latency p50 / p95 chỉ theo dõi, kèm CI; bỏ lượt latency 30 câu; tiền 0,052 → 0,040 |
| m-1 pilot tiền từ câu OOS | Pilot = bước 1 + 2 (19 câu), ước lại theo USD / câu của 7 câu trong phạm vi |
| m-2 chữ ký `paired_stats` | YAML ghi `paired_stats(a_values, b_values, 'false_refusal')`, a / b = refusal của B1 / R2 cùng thứ tự `case_index` |

**B kiểm phần sửa** (tin B 22:4x, không có file review riêng): **ready_for_user_confirmation** — M-1, m-1, m-2 đóng. Ghi chú chữ của B (bỏ chữ
"tất định", ghi A/A ±6,6 % của `output_tokens`) C đã sửa 22:07 26/10/2026 ở §2. Sửa này chỉ là chữ, không đổi tiêu chí.
