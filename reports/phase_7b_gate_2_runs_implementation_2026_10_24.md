# Implementation Report: Phase 7B Gate 2 — Run 1, Run 2, judge luna (B3)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-64`)
Date: 2026-10-24
Spec: `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md` §5 Gate 2

## 1. Phạm vi

Việc B3 trong `session_prompt/CURRENT_HANDOFF.md`: sửa m1 (finding minor A review Gate 1),
rồi chạy Run 1, Run 2 (176 case mỗi run), judge luna cho Run 1 (đủ 176 case, cộng 30 case
chấm lại trong `rerun_30`), và export 3 file đầu vào cho judge Claude (C, Gate 3).
Không tổng hợp cuối (Gate 4). Không sửa runtime, prompt sinh, prompt judge hay Golden.

## 2. Thay đổi chính

- **m1** (`backend/evaluation/full_corpus_eval.py`): thêm hàm `answered_cases(cases,
  answer_rows, case_indexes)`, dùng chung cho `judge-luna` và `export-judge-input`.
  Quy ước: `None` = mọi case đã có câu trả lời; `[]` = không case nào; case lỗi kỹ thuật
  bị bỏ. Trước đây `--cases` không kèm giá trị cho ra `[] or …`, tức mọi case (paid).
  `judge-luna` thoát sớm ("no case to judge") khi không có case nào, không dựng client.
- Test hồi quy `test_cases_flag_without_values_selects_no_case_to_judge` trong
  `backend/tests/test_full_corpus_eval.py`.

## 3. Cách đã chạy thật

Mọi lệnh chạy từ `backend/` bằng `HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m
evaluation.full_corpus_eval …`. File nằm trong `data/evaluation/phase_7b/` (private).

```bash
python -m pytest tests/test_full_corpus_eval.py -q -p no:cacheprovider          # 11 passed
# m1 trên CLI thật, không có env (không thể gọi paid):
judge-luna --answers smoke_answers_1.jsonl --cases --out /tmp/…                   # "no case to judge"
export-judge-input --answers smoke_answers_1.jsonl --cases --seed 1 --out /tmp/…  # 0 rows
export-judge-input --answers smoke_answers_1.jsonl --seed 1 --out /tmp/…          # 10 rows, byte-identical với file trước sửa
# Gate 2 (paid):
generate --golden full --out run1_answers.jsonl
generate --golden full --out run2_answers.jsonl
judge-luna --answers run1_answers.jsonl --out run1_judge_luna.jsonl
judge-luna --answers run1_answers.jsonl --cases <rerun_30 từ subsets.json> --out run1_judge_luna_rerun30.jsonl
# Export (free):
export-judge-input --answers run1_answers.jsonl --seed 1 --out judge_input_run1.jsonl
export-judge-input --answers run1_answers.jsonl --cases <rerun_30> --seed 2 --out judge_input_run1_rerun30.jsonl
export-judge-input --answers run2_answers.jsonl --seed 3 --out judge_input_run2.jsonl
summarize --answers <run> [--scores <judge>]
```

Không có dòng lỗi kỹ thuật nào, nên không cần chạy `retry`.

## 4. Kết quả quan sát

### 4.1 Run 1 và Run 2

| Mục | Run 1 | Run 2 |
|---|---|---|
| Case / lỗi kỹ thuật | 176 / 0 (`complete`) | 176 / 0 (`complete`) |
| Từ chối đúng (`out_of_scope`, n=18) | 18/18 = 1,000 | 18/18 = 1,000 |
| Từ chối nhầm (trong phạm vi, n=158) | 22/158 = 0,139 | 22/158 = 0,139 |
| — theo category | multi_source 11, comparative 8, direct_fact 2, conditional 1 | giống Run 1 |
| Lỗi citation (User gặp 500), tổng | 4/176 = 0,023 | 6/176 = 0,034 |
| — direct_fact (75) / conditional (29) / multi_source (29) | 0,027 / 0,034 / 0,034 | 0,053 / 0,034 / 0,034 |
| — comparative (25) / out_of_scope (18) | 0 / 0 | 0 / 0 |
| Context đóng gói | 176/176 case đủ 5 source; 0 case fallback không gọi model | như Run 1 |
| Output token lớn nhất / giới hạn | 316 / 2.048 | 369 / 2.048 |

Số từ chối nhầm giống hệt nhau theo từng category ở cả hai run. Lỗi citation chênh 4 so
với 6. Đây mới là quan sát; nhiễu cả đường được tính ở Gate 4.

### 4.2 Judge luna (judge phụ, không phải điểm chính thức)

| Phạm vi | n | Accuracy | Completeness | Relevance |
|---|---:|---:|---:|---:|
| Run 1, tổng | 176 | 4,483 | 4,364 | 4,449 |
| direct_fact | 75 | 4,880 | 4,867 | 4,867 |
| conditional | 29 | 4,862 | 4,621 | 4,724 |
| comparative | 25 | 3,720 | 3,560 | 3,680 |
| multi_source | 29 | 3,414 | 3,103 | 3,414 |
| out_of_scope | 18 | 5,000 | 5,000 | 5,000 |
| Chấm lại `rerun_30` (lần 2, cùng câu trả lời Run 1) | 30 | 4,300 | 4,167 | 4,233 |

- 176 + 30 dòng đều hợp lệ (`score_errors` rỗng). Output token lớn nhất 364, dưới giới
  hạn 1.024: không bị cắt, không lỗi parse.
- Điểm 30 case chấm lại là trung bình trên tập con, nên không so trực tiếp với 176 được.
  So lần 1 với lần 2 trên cùng 30 case (nhiễu judge) là việc của Gate 4.

### 4.3 File cho judge Claude (Gate 3)

| File | Dòng | Seed | Kiểm |
|---|---:|---:|---|
| `judge_input_run1.jsonl` | 176 | 1 | đúng 4 field, `case_index` không trùng, không có answer rỗng |
| `judge_input_run1_rerun30.jsonl` | 30 | 2 | như trên; đúng `rerun_30` |
| `judge_input_run2.jsonl` | 176 | 3 | như trên |

Schema điểm C ghi theo report Gate 1 §2.1. A đã được nhắn ngay khi có 3 file.

### 4.4 Usage và tiền (giá luna: 0,1 / 0,5 USD cho 1M token)

| Bước | Calls | Input | Output | USD |
|---|---:|---:|---:|---:|
| Run 1 sinh | 176 | 166.713 | 14.392 | 0,02387 |
| Run 2 sinh | 176 | 166.713 | 14.848 | 0,02410 |
| Judge luna Run 1 | 176 | 164.655 | 20.092 | 0,02651 |
| Judge luna `rerun_30` | 30 | 27.937 | 3.885 | 0,00474 |
| **Gate 2** | 558 | 526.018 | 53.217 | **0,07921** |
| Smoke Gate 1 (đã báo) | 20 | 19.107 | 1.816 | 0,00282 |
| **Tổng B trong Phase 7B** | 578 | | | **0,08203** (giới hạn cứng 0,6) |

Dự báo Gate 1 là ~0,077 USD; số thật 0,0792 (+3%). Ngoài ra B1 có 1 request trả 400,
ước tính ~0 USD (B1 §5.1).

## 5. Lỗi và giới hạn

- Không có lỗi kỹ thuật; không chạm điều kiện dừng nào (tiền, tỉ lệ lỗi, freshness).
- Tiền tính từ usage token với giá User đưa, chưa đối chiếu dashboard OpenAI. Không trừ
  phần giảm giá cho input cache, nên số này là cận trên.
- Điểm luna là judge phụ. Điểm chính thức của baseline là điểm Claude (Gate 3, C).
- Chưa tính nhiễu judge, nhiễu cả đường hay mức khớp giữa các nguồn: thuộc Gate 4.
- Từ chối nhầm 13,9% (tập trung ở multi_source và comparative) là hành vi runtime quan sát
  được, liên quan F1 của Phase 6. 7B không sửa.

## 6. Bàn giao cho người kiểm

- Kiểm m1: hàm `answered_cases` và hai nhánh CLI trong `full_corpus_eval.py`, cộng test mới.
- Đối chiếu số: chạy `summarize --answers run1_answers.jsonl --scores run1_judge_luna.jsonl`
  (free) rồi so với mục 4.
- Gate 3 (C) có thể bắt đầu với 3 file ở mục 4.3.
- Không commit (B không có quyền).
