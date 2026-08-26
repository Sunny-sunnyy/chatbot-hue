# Phase 7 Post-Simplicity Correction Design

Date: `2026-08-26 +07`

Status: `approved_by_user`

Canonical guide:

```text
guides/phase_7_retrieval_answer_evaluation.md
```

## 1. Mục tiêu

Giữ nguyên Phase 7 đơn giản đã được duyệt, đồng bộ nó với contract Phase 0–6
sau simplicity review và loại bỏ một public collection override vượt quá scope.
Correction không redesign Phase 7, không đổi evaluation semantics và không sửa
golden dataset.

## 2. Hiện trạng đã xác minh

- Phase 7 đã dùng labeled context string từ `ContextBuilder.build(documents)`.
- Generator nhận question/context string và trả answer string.
- Judge chỉ nhận question, reference answer và generated answer.
- Agents SDK tracing giữ disabled.
- `run_answer_batch()` và `run_answer_ui()` vẫn nhận optional
  `collection_name`, trái contract retrieval-only override trong guide.
- Canonical Notebook 07 hiện có 9 execution counts và 8 code cells có outputs.
- Hai CSV hiện mỗi file có 20 data rows; full-run 104 rows là historical
  evidence trong reports cũ.

## 3. Thiết kế được duyệt

### 3.1. Code

Public answer paths không được chọn collection:

```python
async def run_answer_batch(
    test_path: str | Path = DEFAULT_TEST_FILE,
    concurrency: int = 3,
    profile: str = "dense_only",
    progress=None,
) -> tuple[list[dict], dict]:
    services = build_services(profile)
```

```python
async def run_answer_ui(test_path, concurrency, progress=gr.Progress()):
    rows, summary = await run_answer_batch(
        test_path, concurrency, "dense_only", progress
    )
```

`build_services(profile, collection_name=None)` được giữ vì retrieval-only
comparison và guarded real verification đang dùng composition root này.
`run_retrieval_batch()` và `run_retrieval_ui()` tiếp tục nhận optional exact
collection override.

Không tách thêm answer/retrieval service builders. Không thêm wrapper,
validation layer hoặc signature test chỉ bảo vệ implementation detail.

### 3.2. Notebook và artifacts

- Xóa execution counts và outputs khỏi canonical Notebook 07.
- Run All thật ghi vào `/tmp`, không lưu live outputs vào repository notebook.
- Smoke run dùng 20 câu để kiểm tra pipeline nhanh.
- Không chạy paid full 104-answer batch trong correction này.
- Không sửa `test2.jsonl`, `tests.jsonl` hoặc validator.

### 3.3. Evidence

- Focused Phase 7 integration suite dùng real guarded Qdrant và real OpenAI.
- Source/signature inspection chứng minh answer batch/UI không còn override.
- Retrieval-only path vẫn giữ override.
- Notebook structural check và temporary Run All đạt.
- Hai CSV sau smoke run có đúng 20 rows và đúng thứ tự input.
- Implementation report ghi exact commands, observed results và mọi lỗi thật.

## 4. Ngoài phạm vi

- Không đổi metric, judge rubric, prompt, provider hoặc model.
- Không đổi generation/retrieval semantics.
- Không thêm retry, fallback, cost accounting, resume hoặc artifact framework.
- Không sửa hoặc tạo golden dataset.
- Không chạy Phase 8 comparison hay chọn winner.
- Không mutate active Hue Qdrant collection.
- Implementer không sửa guide/status/user report và không commit/push.

## 5. Acceptance

Correction sẵn sàng cho Reviewer khi:

1. `run_answer_batch()` và `run_answer_ui()` không còn `collection_name`;
2. retrieval-only override vẫn được giữ và focused suite pass;
3. Phase 6 string contracts và tracing-disabled behavior không đổi;
4. canonical Notebook 07 sạch execution counts/outputs và temporary Run All
   hoàn thành;
5. smoke outputs có 20 ordered rows hoặc report ghi trung thực lỗi thực tế;
6. không có dataset, provider/model, architecture hoặc active-Qdrant mutation;
7. implementation report mới đầy đủ để Reviewer chạy lại độc lập.
