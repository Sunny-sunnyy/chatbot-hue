# Implementation Report: Phase 7 Retrieval và Answer Evaluation

Implementer: AI Assistant (Implementer Role)
Date: 2026-08-24 +07 (Updated after Correction Vòng 1)
Canonical guide:

```text
guides/phase_7_retrieval_answer_evaluation.md
```

## 1. Phạm vi

Triển khai hoàn chỉnh Phase 7 — Retrieval và Answer Evaluation và thực hiện **Correction Vòng 1** theo đúng finding và scope đã được user phê duyệt:
- Tạo bộ câu hỏi thử nghiệm 20 câu thật [`test2.jsonl`](file:///home/minhhieu/hue_rag/knowledge-base-hue/foods/evaluation/test2.jsonl) từ bộ 104 câu [`tests.jsonl`](file:///home/minhhieu/hue_rag/knowledge-base-hue/foods/evaluation/tests.jsonl).
- Package runtime tinh gọn gồm 4 module: `test.py`, `template.py`, `eval.py`, `evaluator.py`.
- Duy nhất một file test: [`backend/tests/test_evaluation.py`](file:///home/minhhieu/hue_rag/backend/tests/test_evaluation.py).
- Đánh giá retrieval profile `dense_only` trên Qdrant collection `hue_foods_e5_small_384` (572 points, read-only).
- Sinh câu trả lời với `gpt-5.4-nano` và chấm điểm bằng giám khảo `gpt-5.4-mini` theo 3 tiêu chí `accuracy`, `completeness`, `relevance` (1–5) cùng `feedback`.
- Giao diện Gradio (`evaluator.py`) hiển thị bảng chi tiết với đầy đủ các cột có tên rõ ràng.
- Ghi đè 2 file CSV cố định: [`retrieval_results.csv`](file:///home/minhhieu/hue_rag/backend/evaluation/retrieval_results.csv) và [`answer_results.csv`](file:///home/minhhieu/hue_rag/backend/evaluation/answer_results.csv).
- Canonical [`notebooks/07_evaluation.ipynb`](file:///home/minhhieu/hue_rag/notebooks/07_evaluation.ipynb) sạch outputs, 22 cells.

## 2. Thay đổi chính trong Correction Vòng 1

1. **Sửa bảng Gradio (`backend/evaluation/evaluator.py`)**:
   - Thêm helper `format_table(rows, columns)` trả về `{"headers": columns, "data": [[row.get(col, "") for col in columns] for row in rows]}`.
   - Cả hai handlers `run_retrieval_ui` và `run_answer_ui` trả về bảng định dạng đúng cho `gr.Dataframe(interactive=False, wrap=True)`.
   - Bảng Retrieval hiển thị chính xác 9 named columns: `category`, `question`, `keywords`, `mrr`, `ndcg`, `keywords_found`, `total_keywords`, `keyword_coverage`, `error`.
   - Bảng Answer hiển thị chính xác 9 named columns: `category`, `question`, `reference_answer`, `generated_answer`, `accuracy`, `completeness`, `relevance`, `feedback`, `error`.
2. **Làm `score_retrieval()` dễ đọc (`backend/evaluation/eval.py`)**:
   - Tách các bước tính toán thành biến trung gian rõ nghĩa: `mrr_values`, `ndcg_values`, `keywords_found`, `total_keywords`, `avg_mrr`, `avg_ndcg`, `keyword_coverage` trước khi truyền vào `RetrievalScores`. Giữ nguyên 100% công thức chuẩn.
3. **Làm rõ rubric chấm điểm (`backend/evaluation/template.py`)**:
   - `accuracy`: sai thực chất là 1, chấp nhận được là 3, chỉ hoàn toàn chính xác mới là 5.
   - `completeness`: chỉ cho 5 khi có đủ toàn bộ thông tin quan trọng trong câu trả lời tham khảo.
   - `relevance`: chỉ cho 5 khi trả lời trực tiếp và không thêm thông tin ngoài câu hỏi.
   - `feedback`: ngắn gọn, cụ thể, giải thích các điểm số.
   - Không nhắc đến context retrieval hay groundedness trong rubric của giám khảo.
4. **Output schema tự giải thích (`backend/evaluation/eval.py`)**:
   - Thêm docstring và mô tả chi tiết cho từng field trong `AnswerScores` (`accuracy`, `completeness`, `relevance`, `feedback`), giữ nguyên bounds integer 1–5.
   - Giữ nguyên `ModelSettings(temperature=0, max_tokens=600)` trong `build_judge`.
5. **Cập nhật regression test (`backend/tests/test_evaluation.py`)**:
   - Cập nhật test `test_retrieval_handler_returns_named_columns_and_rows` xác minh 9 named headers và 20 rows data.

## 3. Cách đã chạy thật

Mọi bước kiểm tra đều chạy trong môi trường `uv` với `--env-file .env`, dùng database Qdrant và OpenAI APIs thật:

1. **Bộ test đơn lẻ:**
   ```bash
   uv run --env-file ../.env python -m pytest tests/test_evaluation.py -q
   ```
   *Kết quả*: `8 passed in 26.78s`

2. **Kiểm tra trực tiếp Gradio postprocessor:**
   ```bash
   uv run --env-file ../.env python -c '
   import gradio as gr, asyncio
   from evaluation.evaluator import build_app, run_retrieval_ui, run_answer_ui
   from evaluation.test import DEFAULT_TEST_FILE
   df = gr.Dataframe(interactive=False, wrap=True)
   _, t_ret = run_retrieval_ui(str(DEFAULT_TEST_FILE), 3)
   p_ret = df.postprocess(t_ret)
   assert len(p_ret.headers) == 9 and len(p_ret.data) == 20
   _, t_ans = asyncio.run(run_answer_ui(str(DEFAULT_TEST_FILE), 3))
   p_ans = df.postprocess(t_ans)
   assert len(p_ans.headers) == 9 and len(p_ans.data) == 20
   print("Gradio postprocess verification passed")
   '
   ```

3. **Run All Notebook 07 trên bản tạm:**
   ```bash
   uv run --env-file .env jupyter nbconvert --execute --to notebook notebooks/07_evaluation.ipynb --output /tmp/07_evaluation-live.ipynb --ExecutePreprocessor.timeout=1800
   ```

4. **Chạy lại toàn bộ 104 câu thật với rubric mới:**
   - Retrieval (104 câu):
     ```bash
     uv run --env-file ../.env python -c 'from evaluation.eval import run_retrieval_batch; rows, summary = run_retrieval_batch("../knowledge-base-hue/foods/evaluation/tests.jsonl", 3); print(summary)'
     ```
   - Answer Evaluation (104 câu):
     ```bash
     uv run --env-file ../.env python -c 'import asyncio; from evaluation.eval import run_answer_batch; rows, summary = asyncio.run(run_answer_batch("../knowledge-base-hue/foods/evaluation/tests.jsonl", 3)); print(summary)'
     ```

## 4. Kết quả quan sát sau Correction Vòng 1

### Kết quả trên 20 câu (`test2.jsonl`):
- **Retrieval**: 20/20 thành công | `mrr: 0.7917`, `ndcg: 0.8020`, `keyword_coverage: 96.67%`.
- **Answer**: 19/20 thành công (1 câu lỗi `model referenced unknown source IDs`) | `accuracy: 4.63`, `completeness: 4.53`, `relevance: 4.89`.
- **Gradio DataFrame**:
  - Retrieval headers: `['category', 'question', 'keywords', 'mrr', 'ndcg', 'keywords_found', 'total_keywords', 'keyword_coverage', 'error']` (20x9)
  - Answer headers: `['category', 'question', 'reference_answer', 'generated_answer', 'accuracy', 'completeness', 'relevance', 'feedback', 'error']` (20x9)

### Kết quả trên 104 câu (`tests.jsonl`) với Rubric chuẩn:
- **Retrieval**: 104/104 thành công (0 failed) | `mrr: 0.8250`, `ndcg: 0.8263`, `keyword_coverage: 95.83%`.
- **Answer**: 103/104 thành công (1 câu lỗi được ghi nhận trung thực vào cột `error` mà không retry hay ngắt batch) | `accuracy: 4.38`, `completeness: 4.02`, `relevance: 4.19`.
- **CSV Outputs**:
  - `backend/evaluation/retrieval_results.csv`: 104 data rows theo đúng thứ tự.
  - `backend/evaluation/answer_results.csv`: 104 data rows theo đúng thứ tự.

## 5. Lỗi và giới hạn

- **Lỗi model output**: Câu hỏi `Quán nào mở cửa buổi tối, Mệ Kéo hay Bà Nga?` sinh câu trả lời có source ID không thuộc danh sách cho phép (`model referenced unknown source IDs`). Lỗi được lưu đúng vào row và xuất ra CSV.
- **Phạm vi**: Chỉ đánh giá `dense_only` theo đúng quy định của Phase 7; các so sánh đa profile thuộc Phase 8.

## 6. Handoff cho Reviewer

- **Các file đã cập nhật trong correction:**
  - [`backend/evaluation/evaluator.py`](file:///home/minhhieu/hue_rag/backend/evaluation/evaluator.py)
  - [`backend/evaluation/eval.py`](file:///home/minhhieu/hue_rag/backend/evaluation/eval.py)
  - [`backend/evaluation/template.py`](file:///home/minhhieu/hue_rag/backend/evaluation/template.py)
  - [`backend/tests/test_evaluation.py`](file:///home/minhhieu/hue_rag/backend/tests/test_evaluation.py)
- **Kiểm tra nhanh cho Reviewer:**
  ```bash
  uv run --env-file ../.env python -m pytest tests/test_evaluation.py -q
  ```
- **Xác nhận trạng thái:**
  - 2 file CSV cố định chứa đúng 104 rows đã chạy thật.
  - Repository notebook sạch sẽ và hợp lệ.
  - Không stage, commit, push hoặc tự approve Phase 7.
