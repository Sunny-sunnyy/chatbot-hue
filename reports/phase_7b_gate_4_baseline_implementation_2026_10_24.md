# Implementation Report: Phase 7B Gate 4 — baseline full-corpus 176 case (B6)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-64`)
Date: 2026-10-24
Spec: `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md` §4.2, §4.4, §7

Report chỉ ghi số tổng hợp. Không chép câu hỏi, đáp án, câu trả lời hay feedback.

## 1. Phạm vi

Việc B6 trong `session_prompt/CURRENT_HANDOFF.md`: tổng hợp baseline từ dữ liệu Gate 1–3.
Không đặt ngưỡng đạt/không đạt, không kết luận cho Phase 8. Phần so với điểm User để
`NOT RUN` vì User chưa chấm. Không gọi paid; không đổi code.

**Hệ thống được đo** (runtime API hiện hành, `Project_Status.md` §4):

- collection `hue_full_corpus_7a2_e5_small_384` (e5-small, 8.459 chunk);
- retrieval `dense_bm25_rrf`, reranker `none`, top-10;
- context 5 chunk;
- sinh bằng `gpt-6-luna`.

**Điểm chính thức** là Claude chấm Run 1 (spec D3).

## 2. Nguồn dữ liệu (private, `data/evaluation/phase_7b/`)

| Dữ liệu | File | Làm ở |
|---|---|---|
| Retrieval 158 case, 2 lần + native | `retrieval_dense_bm25_rrf_{1,2}.jsonl`, `retrieval_native_hybrid_rrf_1.jsonl` | Gate 1 (B) |
| Câu trả lời Run 1 / Run 2 | `run{1,2}_answers.jsonl` | Gate 2 (B) |
| Judge luna Run 1 + chấm lại 30 | `run1_judge_luna.jsonl`, `run1_judge_luna_rerun30.jsonl` | Gate 2 (B) |
| Judge Claude Run 1, chấm lại 30, Run 2 | `claude_run1.jsonl`, `claude_run1_rerun30.jsonl`, `claude_run2.jsonl` | Gate 3 (C) |
| Tập con | `subsets.json` (`rerun_30`, `user_20`; hai tập rời nhau) | A |

Kiểm đầu vào: 3 file Claude có đủ 176 / 30 / 176 dòng, schema đúng 5 field,
`validate_score_rows` rỗng. File chấm User (`user_scoring.md`) gồm đúng 20 case `user_20`;
cả 20 câu trả lời là của **Run 1**.

## 3. Cách đã chạy

Chạy từ `backend/`, đều free:

```bash
E="uv run python -m evaluation.full_corpus_eval"
$E summarize --retrieval retrieval_dense_bm25_rrf_1.jsonl --answers run1_answers.jsonl --scores claude_run1.jsonl
$E summarize --answers run2_answers.jsonl --scores claude_run2.jsonl
$E summarize --answers run1_answers.jsonl --scores run1_judge_luna.jsonl
$E compare --a claude_run1.jsonl      --b claude_run1_rerun30.jsonl      --cases <rerun_30>
$E compare --a run1_judge_luna.jsonl  --b run1_judge_luna_rerun30.jsonl  --cases <rerun_30>
$E compare --a claude_run1.jsonl      --b claude_run2.jsonl
$E compare --a claude_run1.jsonl      --b run1_judge_luna.jsonl
uv run python /tmp/phase7b_b6/extra.py     # phân bố điểm, trung bình khi bỏ từ chối nhầm (script phân tích, ngoài repo)
```

## 4. Baseline (chính thức: Claude, Run 1)

### 4.1 Sáu metric, tổng và theo category

| Category | n (answer) | Accuracy | Completeness | Relevance | n (retrieval) | MRR@10 | nDCG@10 | Keyword Cov.@10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Tổng** | **176** | **4,426** | **4,284** | **4,455** | **158** | **0,721** | **0,755** | **92,35** |
| direct_fact | 75 | 4,867 | 4,840 | 4,893 | 75 | 0,818 | 0,846 | 98,00 |
| conditional | 29 | 4,724 | 4,414 | 4,759 | 29 | 0,816 | 0,816 | 94,83 |
| comparative | 25 | 3,680 | 3,440 | 3,600 | 25 | 0,527 | 0,583 | 82,00 |
| multi_source | 29 | 3,276 | 3,000 | 3,414 | 29 | 0,543 | 0,604 | 84,20 |
| out_of_scope | 18 | 5,000 | 5,000 | 5,000 | — | — | — | — |

- Retrieval bỏ qua `out_of_scope`, theo 7A §8. Hai lần chạy `dense_bm25_rrf` giống hệt từng
  byte (Gate 1).
- Answer metric là macro-average theo case, thang số nguyên 1–5, không gộp thành composite.

### 4.2 Từ chối và lỗi citation (Run 1)

| Chỉ số | Giá trị |
|---|---:|
| Từ chối đúng (`out_of_scope`) | 18/18 = **1,000** |
| Từ chối nhầm (trong phạm vi) | 22/158 = **0,139** — multi_source 11, comparative 8, direct_fact 2, conditional 1 |
| Lỗi citation (User thấy lỗi 500), tổng | 4/176 = **0,023** — direct_fact 2/75, conditional 1/29, multi_source 1/29; comparative 0, out_of_scope 0 |

Run 2 có cùng 22 case từ chối nhầm (0 case đổi quyết định) và 6/176 lỗi citation.

### 4.3 Phân bố điểm (Claude Run 1)

| Bộ ba (A/C/R) | Số case |
|---|---:|
| 5/5/5 | **121** |
| 1/1/1 | **22** |
| Khác | 33 |

| Metric | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| Accuracy | 22 | 0 | 2 | 9 | 143 |
| Completeness | 22 | 2 | 6 | 20 | 126 |
| Relevance | 22 | 0 | 0 | 8 | 146 |

**22 case 1/1/1 trùng đúng 22 case từ chối nhầm**: mọi case từ chối nhầm đều bị chấm
1/1/1, và không có case 1/1/1 nào khác. Cả luna lẫn Claude Run 2 đều như vậy.

### 4.4 Trung bình khi bỏ 22 case từ chối nhầm

| Tập | n | Accuracy | Completeness | Relevance |
|---|---:|---:|---:|---:|
| Mọi case | 176 | 4,426 | 4,284 | 4,455 |
| Bỏ từ chối nhầm | 154 | **4,916** | **4,753** | **4,948** |
| — comparative | 17 | 4,941 | 4,588 | 4,824 |
| — multi_source | 18 | 4,667 | 4,222 | 4,889 |
| — conditional | 28 | 4,857 | 4,536 | 4,893 |
| — direct_fact | 73 | 4,973 | 4,945 | 5,000 |
| Chỉ case trong phạm vi được trả lời | 136 | 4,904 | 4,721 | 4,941 |
| Case có lỗi citation | 4 | 5,000 | 4,750 | 5,000 |

Phần lớn khoảng mất điểm từ trần 5 đến mức hiện tại đến từ 22 case từ chối nhầm. Ví dụ ở
Accuracy: (4,916 − 4,426) chiếm khoảng 85% của (5 − 4,426). Khi đã trả lời, điểm gần trần:
103/136 case trong phạm vi được trả lời đạt 5/5/5. Phần còn lại chủ yếu là Completeness
thấp hơn ở multi_source và comparative.

Đây là **phân tích quan sát**. Nguyên nhân của từ chối nhầm xem B4
(`reports/phase_7b_false_refusal_diagnosis_2026_10_24.md`): 8 retrieval miss, 10 có một
phần bằng chứng, 4 có đủ keyword.

## 5. Độ tin của thước đo (spec §4.4)

Chênh = B − A. "Trùng" = cùng điểm; "≤1" = lệch tối đa 1; "≥2" = lệch từ 2 điểm.

| Phép so | n | Metric | Chênh TB | Trùng | ≤1 | ≥2 |
|---|---:|---|---:|---:|---:|---:|
| **Nhiễu judge Claude** (Run 1, lần 1 → chấm lại) | 30 | Accuracy | 0,000 | 1,000 | 1,000 | 0 |
| | | Completeness | +0,033 | 0,967 | 1,000 | 0 |
| | | Relevance | −0,033 | 0,967 | 1,000 | 0 |
| **Nhiễu judge luna** (Run 1, lần 1 → chấm lại) | 30 | Accuracy | 0,000 | 1,000 | 1,000 | 0 |
| | | Completeness | 0,000 | 0,933 | 1,000 | 0 |
| | | Relevance | −0,067 | 0,933 | 1,000 | 0 |
| **Nhiễu cả đường** (Claude, Run 1 → Run 2: sinh lại + chấm lại) | 176 | Accuracy | +0,006 | 0,983 | 1,000 | 0 |
| | | Completeness | +0,011 | 0,955 | 1,000 | 0 |
| | | Relevance | −0,006 | 0,960 | 1,000 | 0 |
| **Khớp Claude → luna** (Run 1) | 176 | Accuracy | +0,057 | 0,949 | 0,994 | 0,006 |
| | | Completeness | +0,080 | 0,892 | 0,994 | 0,006 |
| | | Relevance | −0,006 | 0,960 | 1,000 | 0 |

Thêm về nhiễu cả đường:

- 16/176 case đổi ít nhất một metric giữa Run 1 và Run 2.
- 64/176 câu trả lời giống hệt chữ giữa hai run. Trong 64 case đó có 1 case Claude chấm
  khác nhau, tức là chỉ do judge.
- Chênh trung bình tổng của cả đường ≤0,011 điểm ở mọi metric. Không case nào lệch ≥2.

Claude–luna: luna chấm cao hơn Claude một chút ở Accuracy và Completeness (+0,06 / +0,08).
Lệch ≥2 điểm chỉ có ở 1 case (0,6%).

**Khớp với User (User–Claude, User–luna, Claude–luna trên `user_20`): NOT RUN — chờ User
chấm.** Khi User chấm xong `user_scoring.md`, chạy từ `backend/`:

```bash
E="uv run python -m evaluation.full_corpus_eval"
U="<20 case_index của user_20 trong subsets.json>"
$E parse-user-scores                       # → user_scores.jsonl; exit 1 nếu còn câu thiếu điểm
$E compare --a user_scores.jsonl --b claude_run1.jsonl     --cases $U
$E compare --a user_scores.jsonl --b run1_judge_luna.jsonl --cases $U
$E compare --a claude_run1.jsonl --b run1_judge_luna.jsonl --cases $U
```

Theo spec §4.4: nếu Claude lệch User có hệ thống (chênh trung bình ≥1 điểm ở một metric)
thì A báo User trước khi coi điểm Claude là chính thức. Hiện điểm Claude là chính thức
**có điều kiện**, chờ bước này.

### 5.1 So retrieval phụ (Gate 1, quan sát)

`native_hybrid_rrf`: MRR 0,726 / nDCG 0,761 / Coverage 93,41, so với runtime 0,721 / 0,755 /
92,35. Chênh nhỏ, chạy một lần, chưa có ngưỡng nhiễu cho retrieval. Ghi lại để Phase 8 xem.

## 6. Tiền thật toàn Phase 7B

| Mục | Calls | Input | Output | USD |
|---|---:|---:|---:|---:|
| Smoke Gate 1 (sinh + judge luna) | 20 | 19.107 | 1.816 | 0,00282 |
| Run 1 sinh | 176 | 166.713 | 14.392 | 0,02387 |
| Run 2 sinh | 176 | 166.713 | 14.848 | 0,02410 |
| Judge luna Run 1 | 176 | 164.655 | 20.092 | 0,02651 |
| Judge luna chấm lại 30 | 30 | 27.937 | 3.885 | 0,00474 |
| Judge Claude (C, sub-agent Claude Code) | 382 lượt | — | — | 0 API |
| **Tổng 7B** | | | | **0,08203** (giới hạn 0,6) |

Ngoài 7B, trong cùng session: probe Phase 8 B5 tốn 0,00495 USD, và 1 request lỗi 400 ở B1
ước tính ~0 USD. Tiền tính từ usage token với giá User đưa, chưa đối chiếu dashboard; không
trừ giảm giá cache, nên đây là cận trên.

## 7. Giới hạn (spec §7.6)

- **Golden do LLM viết** (7A). Reference answer và keyword có thể thiên về cách diễn đạt của
  corpus.
- **Keyword là proxy** cho retrieval (substring), không phải nhãn liên quan đầy đủ.
- **Judge là LLM.** Claude và luna khớp nhau cao, nhưng cả hai cùng là LLM. Mốc người (User
  20 case) chưa có; xem mục 5.
- **Mẫu User nhỏ** (20 case) và đều là câu trả lời Run 1.
- **Hiệu ứng trần:** 121/176 case đạt 5/5/5; khi đã trả lời thì điểm trung bình khoảng 4,9.
  Thang 1–5 ít chỗ để thấy cải thiện chất lượng câu trả lời. Điểm tổng bị chi phối bởi số câu
  từ chối nhầm (mỗi câu là 1/1/1). Phase 8 nên đọc cùng tỉ lệ từ chối nhầm và Completeness theo
  category, không chỉ trung bình tổng.
- **Nhiễu đo trên một cặp run** và trên 30 case chấm lại. Đây là ước lượng, chưa phải phân phối.
- Lỗi citation không làm giảm điểm answer (theo quyết định A ở Gate 1). Chỉ số này đứng riêng.

## 8. Bàn giao cho người kiểm (C5)

- Chạy lại toàn bộ số ở mục 4–5 bằng các lệnh ở mục 3 (free, vài giây); `extra.py` là
  script chỉ đọc ở `/tmp/phase7b_b6/`.
- Tiêu chí spec §7: 1–4 và 6–7 có bằng chứng trong report này và các report Gate 1–3. Tiêu
  chí 5 (User chấm xong, mức khớp với User) là **NOT RUN**.
- Không commit (B không có quyền).
