# Implementation Report: Phase 7B — chuẩn bị Gate 4 + chẩn đoán từ chối nhầm (B4)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-64`)
Date: 2026-10-24
Spec: `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md` §4.4

## 1. Phạm vi

Việc B4 trong `session_prompt/CURRENT_HANDOFF.md`, không tốn tiền:

- (a) so hai file điểm (nhiễu, mức khớp) và đọc điểm User;
- (b) chẩn đoán 22 câu Run 1 bị từ chối nhầm.

Không gọi paid; không sửa runtime/prompt. Không mở file `claude_*`, vì C chưa báo xong.

## 2. Thay đổi chính

Trong `backend/evaluation/full_corpus_eval.py` có thêm 3 lệnh CLI:

| Lệnh | Hàm | Việc |
|---|---|---|
| `compare --a A --b B [--cases …]` | `compare_scores` | So nguồn B với nguồn A trên các case cả hai đều có điểm hợp lệ. Mỗi metric cho: chênh trung bình có dấu (B − A), tỉ lệ trùng, tỉ lệ lệch ≤1, tỉ lệ lệch ≥2. Mặc định so trên phần giao; có `--cases` thì báo thêm case thiếu ở từng nguồn |
| `parse-user-scores` | `parse_user_scores` | Đọc dòng `Điểm: a / c / r` (và `Ghi chú:`) dưới mỗi `## Câu N` của `user_scoring.md`, map sang `case_index` qua `user_scoring_map.json`, rồi ghi `user_scores.jsonl` theo schema điểm (Gate 1 §2.1). Nếu có câu thiếu điểm hoặc điểm sai thì in lỗi, exit 1 và không ghi file |
| `diagnose-refusals --answers … --out …` | `diagnose_false_refusals` | Với mỗi câu trong phạm vi bị từ chối, dựng lại đúng context mà model đã thấy (retrieval local + context builder như `answer_case`, không gọi sinh), rồi đếm keyword nằm trong context và trong top-10 |

Hàm thuần mới: `valid_score_map`, `answer_keywords` (keyword mang đáp án: có trong
reference, không có trong câu hỏi — cùng luật Golden 7A), `classify_refusal_evidence`,
`count_by_category`. Thêm 3 test vào `backend/tests/test_full_corpus_eval.py`
(tổng 14 passed).

Cách dùng ở Gate 4 (một lệnh `compare` cho mỗi cặp nguồn):

| Mục spec §4.4 | `--a` | `--b` | `--cases` |
|---|---|---|---|
| Nhiễu judge luna | `run1_judge_luna.jsonl` | `run1_judge_luna_rerun30.jsonl` | `rerun_30` |
| Nhiễu judge Claude | file điểm Claude Run 1 | file điểm Claude chấm lại 30 | `rerun_30` |
| Nhiễu cả đường | điểm Claude Run 1 | điểm Claude Run 2 | (176) |
| Khớp với User | `user_scores.jsonl` | điểm Claude hoặc luna Run 1 | `user_20` |
| Claude–luna | điểm Claude Run 1 | `run1_judge_luna.jsonl` | `user_20`, rồi 176 |

## 3. Cách đã chạy thật

Chạy từ `backend/`:

```bash
HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_full_corpus_eval.py -q -p no:cacheprovider   # 14 passed
uv run python -m evaluation.full_corpus_eval compare --a run1_judge_luna.jsonl --b run1_judge_luna_rerun30.jsonl --cases <rerun_30>
uv run python -m evaluation.full_corpus_eval parse-user-scores --out /tmp/…     # file thật, User chưa chấm
HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m evaluation.full_corpus_eval diagnose-refusals \
  --answers run1_answers.jsonl --out run1_false_refusal_diagnosis.jsonl
```

`diagnose-refusals` chỉ dùng e5 local và đọc Qdrant; không dựng generator, không gọi OpenAI.
`--env-file` trong lệnh là thừa, nhưng không gây ra lượt gọi nào.

## 4. Kết quả quan sát

### 4.1 Nhiễu judge luna (cùng 30 câu trả lời Run 1, chấm hai lần)

| Metric | Chênh TB (lần 2 − lần 1) | Trùng | Lệch ≤1 | Lệch ≥2 |
|---|---:|---:|---:|---:|
| Accuracy | 0,000 | 30/30 = 1,000 | 1,000 | 0 |
| Completeness | 0,000 | 28/30 = 0,933 | 1,000 | 0 |
| Relevance | −0,067 | 28/30 = 0,933 | 1,000 | 0 |

Luna gần như tất định khi chấm lại: không case nào lệch quá 1 điểm. Đây chỉ là nhiễu
**judge**, chưa phải nhiễu cả đường. Nhiễu cả đường cần điểm Claude Run 1 và Run 2 (Gate 3).

### 4.2 Parser điểm User

Chạy trên `user_scoring.md` thật (User chưa chấm): báo đúng 20/20 câu "điểm chưa đủ",
exit 1, không ghi file. Đường đọc điểm đã chấm mới được kiểm bằng test logic thuần
(mục 2), vì chưa có điểm thật. Khi User chấm xong, chạy lại một lệnh là có
`user_scores.jsonl`.

### 4.3 Chẩn đoán 22 từ chối nhầm (Run 1)

Context dựng lại trùng lần sinh ở **22/22** case (top-10 chunk id giống hệt, vì retrieval
tất định).

| Category | n | Retrieval miss | Có một phần bằng chứng | Có đủ keyword đáp án |
|---|---:|---:|---:|---:|
| multi_source | 11 | 2 | 5 | 4 |
| comparative | 8 | 3 | 5 | 0 |
| direct_fact | 2 | 2 | 0 | 0 |
| conditional | 1 | 1 | 0 | 0 |
| **Tổng** | **22** | **8** | **10** | **4** |

Định nghĩa (theo keyword mang đáp án, trong 5 chunk context):

- *retrieval miss*: không có keyword nào;
- *một phần*: có một số, thiếu một số;
- *đủ*: có hết.

Quan sát thêm:

- **12/22** case có nhiều keyword trong top-10 hơn trong 5 chunk context. Nghĩa là một phần
  bằng chứng đã được truy xuất (hạng 6–10) nhưng bị cắt khi đóng gói top-5.
- Nhóm "một phần" (10) tập trung ở comparative và multi_source. Mẫu điển hình: có bằng
  chứng cho một vế, thiếu vế còn lại, và model từ chối cả câu thay vì trả lời phần có
  nguồn. Dữ liệu này phù hợp giả thuyết H8 (prompt "tất cả hoặc không"), nhưng chưa chứng
  minh được.
- Nhóm "đủ" (4, đều multi_source) là ứng viên rõ nhất cho việc model từ chối dù context có
  keyword đáp án.

**Giới hạn của cách đo:** keyword là proxy substring. Có keyword trong context chưa có
nghĩa là context đủ ý để trả lời; không có keyword cũng chưa chắc là thiếu bằng chứng (có
thể diễn đạt khác). Vì vậy bảng trên là **phân loại quan sát**, không phải nguyên nhân đã
chứng minh. Muốn kết luận về prompt hay context size thì cần thí nghiệm ở Phase 8: đổi một
thứ, đo lại trên 176 case.

## 5. Lỗi và giới hạn

- `compare` cho nguồn Claude/User chưa chạy, vì chưa có file. Code đã kiểm bằng test và
  bằng chạy thật với nguồn luna.
- Chẩn đoán dùng Run 1. Run 2 có đúng cùng 22 case từ chối (A đã kiểm), nên không chạy lại.
- Không có lỗi nào khác trong phạm vi này.

## 6. Bàn giao cho người kiểm

- Đọc trước `compare_scores`, `parse_user_scores` và `diagnose_false_refusals` trong
  `full_corpus_eval.py`.
- Chạy lại nhanh (free): pytest file test, rồi lệnh `compare` luna ở mục 3.
  `diagnose-refusals` mất khoảng 30 giây và ghi đè `run1_false_refusal_diagnosis.jsonl`
  (private).
- Gợi ý cho brainstorm Phase 8 (đề xuất, chưa phải quyết định): hai hướng tách được bằng
  thí nghiệm là (1) prompt cho phép trả lời một phần có nguồn và (2) context lớn hơn top-5
  hoặc truy xuất theo từng vế cho câu so sánh/đa nguồn.
- Không commit (B không có quyền).
