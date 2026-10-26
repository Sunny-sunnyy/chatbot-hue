# Plan: Phase 8.2 §10 — R3, câu prompt "nêu đủ chi tiết có trong bằng chứng" (nhánh khâu trả lời)

Người viết: B (Claude Opus 5.5, `hue-rag-23`) · 2026-10-26 22:15 +0700 (`date`) · Việc: B51 (A giao 22:2x) · Trạng thái: **bản nháp chờ C review**,
rồi A ghi "duyệt bản sha" (`WORKFLOW.md` §9.1). **Chưa code, chưa gọi API; 0 USD lúc viết.**

Plan không chép câu hỏi, đáp án hay câu trả lời. Repo public, nên chỉ ghi `case_index` và số đếm.

## Căn cứ để review

1. `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` **§10.2–§10.4** (bản A duyệt `cd910c4c4169`, commit `ce8b310`):
   luật (i), "đo tốc độ theo khâu", sàn, Holm {R2, R3}, dòng R3 bảng §10.3, tiền.
2. `report_agent/2026-10-26_cai_tien_tung_khau/de_xuat_khau_tra_loi_C.md` **§3 (dòng R3, R4), §4 (`R3_detail` + cỡ mẫu), §5 (thứ tự)**: đề xuất R3,
   rủi ro, cỡ mẫu C37.
3. `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_C.md` **§5**: 9 câu `under-answer` (U).
4. `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r2_plan.md` (bản A duyệt `b70ea775efb2`) **§2 YAML, §3**: khuôn harness / judge / A/A
   dùng chung với R3.

Người review được chạy lệnh chỉ đọc và tính lại từ `data/phase_8_2/b1/` (`b1_*.jsonl`, `judge/`) và `backend/llm/full_corpus_prompt.py`.

## 1. Lớp bài toán và giả định

- **Lớp:** câu trả lời đúng ý chính nhưng **bỏ chi tiết phụ đã có trong đoạn được trích**: giờ đóng cửa, năm, tên riêng, người thực hiện, lựa
  chọn thứ hai, giá gốc. Judge chấm 4 thay vì 5 Completeness. C36 §5 tìm được **9 câu** loại này trên mốc G2.1a context 10: 28, 38, 41, 51, 65, 66,
  93, 141, 173. Ở cả 9 câu, ít nhất một chi tiết bị bỏ nằm ngay trong đoạn model đã trích.
- **Đổi đúng một thứ:** chèn **một câu** vào `ANSWER_SYSTEM_INSTRUCTIONS`, đặt **ngay trước** luật từ chối (`_REFUSAL_RULE` của
  `g2_generate.py:57`). Cách chèn: `replace(_REFUSAL_RULE, R3_SENTENCE + "\n" + _REFUSAL_RULE)` + `assert` chuỗi gốc có mặt — như P1 / P2 8.1.
  **Chữ ghi trước, không sửa sau khi thấy số:**

```text
Nêu đủ mọi chi tiết trong bằng chứng liên quan trực tiếp tới điều được hỏi (ví dụ giờ, giá, năm, tên riêng, điều kiện, lựa chọn khác), không chỉ ý chính; mỗi chi tiết kèm citation; không thêm chi tiết ngoài điều được hỏi.
```

  - Vì sao có vế cuối: rủi ro chính của R3 là **lan man** (Relevance giảm) và **tự suy ra** (như câu 155) — C37 §3. Vế cuối giữ biến thể
    trong đúng một ý ("đủ nhưng không thừa"), không thêm luật mới về tính toán.
  - Ví dụ trong ngoặc lấy theo **loại chi tiết** C36 thấy bị bỏ, không lấy chữ từ câu nào. Đây là chỉnh theo dev ⇒ test (41 câu chính) là phép
    kiểm "không làm hỏng" độc lập; câu kín B3 là phép kiểm cuối.

| Giả định | Kiểm bằng máy (0 USD) | Kết quả |
|---|---|---|
| G1. Chuỗi `_REFUSAL_RULE` có trong prompt runtime ở `811d25d` | `assert` trong harness (bước 0) | sẽ kiểm; `g2_generate.py:58` đã `assert` như vậy |
| G2. 9 câu U có ở mốc B1 (không chỉ G2.1a) | B1 ↔ G2.1a cùng đầu vào; A/A dev chính đổi Completeness 2 / 88 câu | *giả định*: phần lớn 9 câu còn điểm 4 ở B1; harness in điểm B1 của 9 câu ở bước judge (chỉ đếm) |
| G3. P2 8.1 (ngược chiều: "đoạn văn ngắn") không khác chất lượng, token ra −12 % | `phase_8_1_g2_implementation.md` §4.2 (C37 trích) | độ dài câu trả lời không tự kéo Completeness ⇒ R3 phải thắng ở đúng câu U |
| G4. Câu R3 không đụng luật từ chối | câu chèn **trước** `_REFUSAL_RULE`, luật từ chối giữ nguyên chữ | sàn OOS / 120 / 168 kiểm như R2 |

## 2. Tiêu chí ghi trước

```yaml
experiment_id: p82_r3_complete_details
baseline: p82-b1 811d25d — context 10 + NFC, ANSWER_SYSTEM_INSTRUCTIONS, reasoning mặc định; câu trả lời mốc data/phase_8_2/b1/b1_{dev,test}.jsonl
changed_variable: chèn R3_SENTENCE (§1) ngay trước _REFUSAL_RULE
unchanged: [corpus, chunker, e5-small, index, retrieval dense_bm25_rrf pool 30, context 10, gpt-6-luna, reasoning, validator, judge prompt]
data: {split: split.json e2b1788dfbbc, dev: 120 (12 OOS), test: 56 (6 OOS), realism: 0b65d1c138d2 -> dev chính 88 / test chính 41}
noise_AA: "B1 ↔ G2.1a chấm cùng lượt mù data/phase_8_2/b1/judge/ — dev chính C 1/86/1, A 1/86/1, R 1/84/3, đổi từ chối 0; test chính C 3/38/0, A 2/38/1, đổi từ chối 0;
           output_tokens dev 120: TB 77,0 / 77,0, SD chênh 28 token (±6,6 %)"
metrics:
  # sàn (spec §10.2)
  - {name: OOS bị trả lời, set: dev 12 + test 6, role: floor, floor: 0}
  - {name: 120 / 168 vẫn từ chối, set: dev, role: floor, floor: "cả hai is_refusal"}
  - {name: câu không citation mà không phải câu từ chối chuẩn (API 500) + lỗi kỹ thuật, set: 176, role: floor, floor: 0}
  # quyết
  - {name: Completeness dev chính, fn: "full_corpus_eval.paired_stats(a_values=B1, b_values=R3, 'completeness'), cùng thứ tự case_index", set: 88,
     better: up, role: decide,
     rule: "CI 95% > 0 VÀ Holm họ {R2, R3} CỐ ĐỊNH (p × 2 < 0,05, dù R2 kết quả thế nào)", ceiling: "9 câu U × +1"}
  # mức tụt (spec §10.2 luật (i))
  - {name: số câu Accuracy tụt, set: "dev chính 88 / test chính 41", role: tolerance, max: "4 / 5 (A/A + 3)"}
  - {name: số câu Completeness tụt, set: test chính 41, role: tolerance, max: "6 (A/A + 3)"}
  - {name: từ chối nhầm trong phạm vi, set: "dev chính / test chính", role: tolerance, max: "+1 / +1 (A/A + 1)"}
  - {name: lỗi citation v2, fn: "tính lại cho CẢ B1 và R3 bằng cùng hàm (như k1.citation_v2)", set: 176, role: tolerance, max: "+2 câu"}
  - {name: USD / câu (usage log), role: tolerance, max: "+20 %; 0 lần gọi API thêm"}
  - {name: output_tokens / câu (tốc độ khâu sinh, spec §10.2 'đo tốc độ theo khâu'), def: "TB R3 ÷ TB B1, dev 120 câu có gọi model", role: tolerance, max: "+20 %"}
  # theo dõi
  - {name: Relevance chênh TB + số câu tụt (rủi ro lan man), set: dev chính, role: watch}
  - {name: điểm Completeness của 9 câu U (28, 38, 41, 51, 65, 66, 93, 141, 173) ở B1 / R3, role: watch}
  - {name: R4 — số câu có số không ở đoạn được trích (experiments.phase_8_2.r4_numbers), set: "dev / test, cả B1 và R3", role: watch,
     note: "R4 chỉ là danh sách đọc lại (precision ngoài mẫu thấp); tăng > 2 câu ⇒ ghi rõ trong report"}
  - {name: Completeness / Accuracy theo loại câu; latency p50 / p95 kèm CI (B1 đo phiên khác); output_tokens TB theo loại câu, role: watch}
result: null
conclusion: null   # tốt hơn / không đổi / kém hơn / chưa rõ — dựa judge ⇒ TẠM tới khi B0 xong (§10.2)
```

**Luật giữ** (`run-experiment` §4, spec §10.2 luật (i)):
1. Dev: đủ sàn, không vượt mức tụt nào, chỉ số quyết qua ⇒ chạy test.
2. Test: đủ sàn và mức tụt ("không làm hỏng"; spec §10.6 Q2) ⇒ **"tốt hơn" (tạm)**.

**Ghi trước về tốc độ:** R3 làm câu trả lời dài hơn, nên `output_tokens` / câu có thể vượt +20 %. Vượt ⇒ luật (i) không tự nhận ⇒ **A trình User
kèm số** (chất lượng tăng bao nhiêu, token ra / USD / latency tăng bao nhiêu). Chất lượng trước (spec §10.2): nếu R3 thắng mà tốn hơn, bước sau là
tìm cách gọn hơn (ví dụ bỏ ví dụ trong ngoặc). Đó là biến thể mới, plan riêng.

**Cỡ mẫu** (`bootstrap_mean_diff`, seed 20261024, n 88, mỗi câu ±1 điểm; B tính 22:1x):

| Thắng / thua | p | × 2 (Holm họ 2) | Qua? |
|---|---|---|---|
| 4 / 0 | 0,031 | 0,062 | không |
| **5 / 0** | 0,013 | 0,026 | **qua** |
| 5 / 1, 6 / 1, 7 / 1 | 0,131 / 0,063 / 0,036 | > 0,05 | không |
| **8 / 1** | 0,015 | 0,030 | **qua** |
| 9 / 2 | 0,036 | 0,072 | không |

A/A dev chính có khoảng 1 câu tụt do nhiễu judge ⇒ thực tế cần **≥ 8 thắng / 1 thua**, trong khi trần là 9 câu U.
**Ghi trước: "chưa rõ" rất có thể** — đó là kết quả hợp lệ. Câu ngoài 9 câu U cũng có thể thắng, nên trần thật có thể lớn hơn 9 một chút.

## 3. Cách chạy (khi plan được duyệt)

- **Harness mới** `backend/experiments/phase_8_2/r3.py` trên nhánh **`p82-r3`** tạo từ `811d25d`, worktree `/tmp/b_r3`. Theo khuôn
  `phase_8_2/b1.py` + `k1.py`:
  - `run`: `full_corpus_eval.answer_case` + `OpenAIFullCorpusGenerator.from_environment(settings, answer_instructions=R3_INSTRUCTIONS)`;
    retrieval / context production của mốc;
  - các lệnh `merge`, `check`, `export-judge`, `check-judge`, `analyze`;
  - từ chối ghi đè; ghi `data/phase_8_2/r3/`.
  Không sửa production.
- **R4** chạy từ working tree `main` (`r4_numbers.py` ở `2c7ecfd`, chưa có trên `811d25d`) trên file câu trả lời đã lưu của B1 và R3. Thước
  dựng lại context bằng builder `max_documents=10`, giống mốc.

1. **Bước 0:** `assert` chèn đúng; in sha `R3_INSTRUCTIONS`.
2. **Pilot 10 câu dev** (`g2_generate.select("pilot")`, seed 20261024) ⇒ USD / câu và `output_tokens` thật ⇒ ước lại mọi bước sau.
3. **Sàn sớm:** 12 câu OOS dev + 120 / 168 (trừ câu đã có trong pilot). Phạm sàn ⇒ **kém hơn**, dừng.
4. **Phần dev còn lại** ⇒ gộp 120 câu. Kiểm tất định: `top_chunk_ids`, `context_sources` = B1 ở 120 / 120 (chỉ prompt đổi).
5. **Judge cùng lượt mù:** câu trả lời R3 dev + **B1 dev chấm lại** trong cùng lô, id mờ. Câu giống hệt chữ thì chấm một lần. Sub-agent judge
   Claude mới (ghi model id) chỉ Read `full_corpus_judge_prompt.md` + lô.
6. **Kết luận dev** theo §2. Chỉ khi dev đạt: test 56 câu ⇒ judge mù test (R3 + B1 test) ⇒ xác nhận.
7. **R4** trên B1 + R3 (dev / test). Đếm câu bị cờ ở mỗi bên; câu R3 mới bị cờ thì liệt kê `case_index`.

## 4. Tiền và dừng

- *Ước* (B1 thật 0,000204 USD / câu dev; câu prompt thêm khoảng 60 token vào; token ra có thể +20–40 %): ≈ 0,00022 USD / câu.
  - dev 120 ≈ 0,027;
  - test 56 ≈ 0,013;
  - **tổng ≈ 0,040 USD**.
  - Dừng ở bước 3 ⇒ ≈ 0,005.
- **Trần R3: 0,05 USD.** Pilot: USD / câu × số câu còn lại vượt trần, hoặc vượt ước > 50 % ⇒ dừng, báo A.
- **Dừng thêm:**
  - lỗi kỹ thuật > 0 ⇒ tìm nguyên nhân, không fallback;
  - kiểm tất định bước 4 lệch ⇒ dừng;
  - đổi chữ R3 sau khi thấy số = biến thể mới, cần plan mới. Tối đa 3 vòng (`run-experiment` §4).
- Judge: quota Claude Code, 0 USD. Không ghi Qdrant, không sửa corpus / Golden / split / đoạn đúng, không mở câu kín.

## 5. Quan hệ với R2 và ghép

- R2 và R3 **cùng so với mốc B1**, mỗi biến thể một lượt riêng (spec §10.2: không so nối tiếp).
- Họ Holm {R2, R3} cố định: ngưỡng p × 2 không đổi dù R2 thắng hay thua.
- Hai câu prompt chạm hai luật khác nhau: R2 thay luật từ chối, R3 thêm câu trước luật từ chối. Ghép R2 + R3 là cấu hình mới, chạy một lượt xác nhận
  riêng (§10.3 "Ghép"), không thuộc plan này.

## 6. Cần A xác nhận

1. Chữ R3 ở §1 (một câu, có vế "không thêm chi tiết ngoài điều được hỏi").
2. Trần 0,05 USD.
3. Quyền: nhánh `p82-r3` (tạo + commit + push, không merge); paid `gpt-6-luna` theo trần; sub-agent judge Claude.

## 7. Đầu ra

`phase_8_2_r3_implementation.md`, gồm:
- bước 0 – pilot (USD / câu, `output_tokens` thật);
- sàn;
- chỉ số quyết, kèm câu thắng / thua theo `case_index`;
- mức tụt;
- tốc độ: `output_tokens`, latency kèm CI;
- tiền thật;
- R4;
- 9 câu U;
- kết luận;
- 3–5 dòng lời thường cho User.

Dữ liệu ở `data/phase_8_2/r3/`. Nếu R3 không được nhận, report vẫn ghi đủ số.
