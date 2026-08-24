# Codex Review: Phase 7 Retrieval và Answer Evaluation

Decision: `ready_for_user_confirmation`
Reviewer: Codex
Date: 2026-08-24 09:18 +07
Canonical guide: `guides/phase_7_retrieval_answer_evaluation.md`
Implementation report:
`reports/phase_7_retrieval_answer_evaluation_implementation_report.md`

## 1. Phạm vi đã review

Reviewer vòng 2 đã đọc exact correction diff ở bảng Gradio, retrieval score
readability, judge rubric/schema và test hiện hành. Reviewer đối chiếu lại công
thức MRR/nDCG với `rag_old_0`, kiểm tra trực tiếp Pydantic/Agents output schema,
Notebook 07, hai CSV và implementation report cập nhật.

Reviewer chạy lại active Qdrant collection read-only, profile `dense_only`,
local E5, production generator `gpt-5.4-nano`, judge `gpt-5.4-mini`, hai UI
handlers, Notebook 07 và full 104-question batches. Không dùng mock, fake,
replay hoặc prior output làm evidence.

## 2. Findings

Không còn blocker hoặc major.

Finding major vòng 1 đã được giải quyết: adapter nhỏ `format_table()` đưa real
rows thành đúng named headers và matrix data mà Gradio 6.25.0 hiển thị thành
bảng 9 cột cho cả retrieval và answer.

Các correction còn lại đúng scope đã được user duyệt:

- `score_retrieval()` dùng biến trung gian rõ nghĩa nhưng không đổi công thức;
- rubric nêu rõ mốc điểm 1, 3 và 5;
- `AnswerScores` giữ integer bounds 1–5 và có descriptions đúng dữ liệu judge
  thực sự nhận;
- giữ `temperature=0`, `max_tokens=600`;
- không thêm metric, groundedness, dependency hay abstraction mới.

## 3. Cách Reviewer chạy lại thật

Từ `backend/`, với `UV_CACHE_DIR=/tmp/hue-rag-review2-uv-cache`:

```bash
uv run --env-file ../.env python -c '<đọc collection count và model settings>'
uv run --env-file ../.env python -m pytest tests/test_evaluation.py -q --tb=short -s
uv run --env-file ../.env python -c '<chạy run_retrieval_ui và run_answer_ui trên test2.jsonl rồi Gradio postprocess>'
uv run --env-file ../.env python -c '<run_retrieval_batch trên tests.jsonl, concurrency=3>'
uv run --env-file ../.env python -c '<run_answer_batch trên tests.jsonl, concurrency=3>'
```

Từ repo root:

```bash
uv run --env-file .env jupyter nbconvert --execute --to notebook \
  notebooks/07_evaluation.ipynb \
  --output /tmp/07_evaluation-review2-live.ipynb \
  --ExecutePreprocessor.timeout=1800
uv run python -m py_compile backend/evaluation/test.py \
  backend/evaluation/template.py backend/evaluation/eval.py \
  backend/evaluation/evaluator.py backend/tests/test_evaluation.py
git diff --check
```

## 4. Kết quả quan sát

- Qdrant: `hue_foods_e5_small_384`, 572 points, read-only.
- Cấu hình: `dense_only`, `gpt-5.4-nano`, `gpt-5.4-mini`.
- Test: 8 passed trong 28.63 giây bằng Qdrant và OpenAI thật.
- Real retrieval UI: 20 rows x 9 named columns; 20/20 thành công; MRR 0.7917,
  nDCG 0.8020, coverage 96.67%.
- Real answer UI: 20 rows x 9 named columns; lần chạy này 20/20 thành công;
  accuracy 4.45, completeness 4.00, relevance 4.35.
- Retrieval 104: 104/104 thành công; MRR 0.8250, nDCG 0.8263, coverage 95.83%.
- Answer 104: 103/104 thành công; accuracy 4.37, completeness 4.02,
  relevance 4.19.
- Câu `Quán nào mở cửa buổi tối, Mệ Kéo hay Bà Nga?` có lỗi
  `model referenced unknown source IDs`; row lỗi được giữ, batch tiếp tục và
  thứ tự không đổi.
- Hai CSV cuối có 104 rows đúng thứ tự và Gradio postprocess thành 104x9.
- Temporary Notebook 07 Run All thành công; repository notebook có 22 cells,
  execution counts null và outputs rỗng.
- `py_compile` và `git diff --check` đạt.

Sự khác nhau giữa 20/20 ở UI run và lỗi một row ở full run là biến thiên model
thật. Error handling đang hoạt động đúng contract; không có retry hoặc fallback
giả.

## 5. Giới hạn hoặc phần chưa chạy

Reviewer không thao tác bằng browser GUI, nhưng đã chạy trực tiếp cả hai UI
handlers qua production path và đưa outputs qua postprocessor của đúng Gradio
6.25.0. App wiring, labels và components cũng đã được kiểm tra từ source/config.
User sẽ kiểm tra trải nghiệm cuối bằng Notebook 07 và giao diện local.

## 6. Decision và bước tiếp theo

Decision: `ready_for_user_confirmation`.

User đã xác nhận Phase 7 ngày 2026-08-24 +07; canonical guide, phase index, user
report và project status đã được chuyển sang `approved`. Bước tiếp theo là
review và đơn giản hóa Phase 0–6 theo dependency order. Phase 8 vẫn đóng và
không có quyền commit/push được suy ra từ xác nhận này.
