# Implementation Report: Phase 7B Gate 3 — Claude judge

Người làm: C (Claude Opus 5.5, terminal `hue-rag-d9`)
Date: 2026-10-24
Spec: `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md` §4.3–4.5

Report không chép câu hỏi, đáp án, câu trả lời, feedback hay điểm; chỉ ghi số lô, số case,
lỗi và thời gian.

## 1. Phạm vi

A giao (tin nhắn 2026-10-24): chấm Claude cho 3 file theo thứ tự ưu tiên, prompt judge
`backend/evaluation/full_corpus_judge_prompt.md` (commit `ea5a1d5`):

| # | Đầu vào (`data/evaluation/phase_7b/`) | Đầu ra | Case |
|---|---|---|---:|
| 1 | `judge_input_run1.jsonl` | `claude_run1.jsonl` | 176 |
| 2 | `judge_input_run1_rerun30.jsonl` | `claude_run1_rerun30.jsonl` | 30 |
| 3 | `judge_input_run2.jsonl` | `claude_run2.jsonl` | 176 |

Đã làm đủ cả 3. Không mở `run*_answers*`, `*_judge_luna*`, `subsets.json`, Golden hay
corpus (trừ việc lệnh `summarize` của B tự đọc `run*_answers.jsonl`; C chỉ lấy `cases`,
`scores.overall.n`, `score_errors` từ output).

## 2. Cách làm

- Chia lô: `/tmp/c_judge/batches.py split` (ngoài repo) — lô ≤10 case, **giữ nguyên thứ tự**
  trong file đầu vào (B đã xáo theo seed), từ chối dòng có key khác
  `{case_index, question, reference_answer, answer}`. Lô ở
  `data/evaluation/phase_7b/claude_batches/<run>/batch_NN.jsonl` (private).
- Chấm: mỗi lô một sub-agent **mới** (`general-purpose`, kế thừa model Claude Opus 5.5 của
  session), prompt chỉ cho phép: Read prompt judge, Read lô của mình, Write
  `scores_NN.jsonl` cùng thư mục; cấm Bash, liệt kê thư mục, file khác, web. Lượt (2) dùng
  sub-agent mới, không thấy kết quả lượt (1). Sub-agent trả về chỉ "xong N".
- Gộp và kiểm: `/tmp/c_judge/batches.py merge` — đủ đúng tập `case_index` của file đầu vào,
  không trùng, `accuracy/completeness/relevance` là số nguyên 1–5, `feedback` không rỗng;
  ghi file đầu ra sắp theo `case_index`, schema `{case_index, accuracy, completeness,
  relevance, feedback}`.
- C (người điều phối) không đọc nội dung lô hay điểm; chỉ kiểm cấu trúc.

## 3. Cách đã chạy thật

```bash
cd data/evaluation/phase_7b
uv run --project /home/minhhieu/hue_rag python /tmp/c_judge/batches.py split judge_input_<run>.jsonl claude_batches/<run> 10
# 39 sub-agent chấm (lô 01..NN)
uv run --project /home/minhhieu/hue_rag python /tmp/c_judge/batches.py merge judge_input_<run>.jsonl claude_batches/<run> claude_<run>.jsonl

cd backend
uv run python -m evaluation.full_corpus_eval summarize --answers run1_answers.jsonl --scores claude_run1.jsonl
uv run python -m evaluation.full_corpus_eval summarize --answers run1_answers.jsonl --scores claude_run1_rerun30.jsonl
uv run python -m evaluation.full_corpus_eval summarize --answers run2_answers.jsonl --scores claude_run2.jsonl
```

## 4. Kết quả quan sát

| File | Lô | Sub-agent | Case gộp | `summarize` `score_errors` | `scores.overall.n` |
|---|---:|---:|---:|---|---:|
| `claude_run1.jsonl` | 18 (17×10 + 1×6) | 18 | 176 | `[]` | 176 |
| `claude_run1_rerun30.jsonl` | 3 (3×10) | 3 | 30 | `[]` | 30 |
| `claude_run2.jsonl` | 18 (17×10 + 1×6) | 18 | 176 | `[]` | 176 |

- Tổng 39 sub-agent, 39 lô, 382 lượt chấm; **0 lô lỗi, 0 lô chạy lại**.
- Thời gian: chia lô 14:56:29 → gộp xong run2 15:04:28 (~8 phút). Mỗi sub-agent 8–34 giây,
  ~27,6k–29,8k token (gồm đọc prompt + lô).
- Kiểm tuân thủ (đọc transcript sub-agent, chỉ trích tên tool và `file_path`, không đọc nội
  dung): 39/39 transcript có đúng 2 Read (prompt judge + đúng lô của mình), 1 Write (đúng
  `scores_NN.jsonl` tương ứng), 0 Bash, 0 file khác.
- Không gọi API trả phí (chấm bằng Claude Code sub-agent). Quota Claude không bị chạm giới hạn.

## 5. Lỗi và giới hạn

- Sub-agent chấm nhanh (8–34 giây / 10 case). Tôi không đọc điểm nên không đánh giá chất lượng
  chấm; độ tin cậy được đo ở bước sau (nhiễu judge trên 30 case, khớp với User/luna — spec §4.4).
- Model sub-agent là model kế thừa của session (Claude Opus 5.5); tool Agent không trả về
  model ID theo từng sub-agent.
- Script chia/gộp nằm ở `/tmp/c_judge/` (ngoài repo, không commit); lô và điểm từng lô giữ ở
  `data/evaluation/phase_7b/claude_batches/` (private) để kiểm lại.

## 6. Bàn giao cho người kiểm

- Đọc: bảng §4; ba file điểm trong `data/evaluation/phase_7b/`.
- Chạy lại kiểm: ba lệnh `summarize` ở §3 (chỉ đọc), `score_errors` phải rỗng; có thể so
  `claude_batches/<run>/batch_*.jsonl` với file đầu vào (nối các lô theo thứ tự = file gốc).
- Không có deviation so với tin giao việc của A.
