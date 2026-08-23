# Reviewer Workflow

## Vai trò

Reviewer kiểm tra độc lập implementation của một phase, tập trung vào kết quả
thật, độ dễ hiểu và việc bám đúng thiết kế người dùng đã duyệt. Reviewer không
mặc định sửa runtime code thay Implementer.

## Đọc trước khi review Phase 7

```text
/home/minhhieu/hue_rag/session_prompt/Session_Prompt.md
/home/minhhieu/hue_rag/session_prompt/REVIEWER_WORKFLOW.md
/home/minhhieu/hue_rag/session_prompt/Project_Status.md
/home/minhhieu/hue_rag/guides/phase_7_retrieval_answer_evaluation.md
/home/minhhieu/hue_rag/docs/superpowers/specs/2026-08-23-phase-7-simple-evaluation-design.md
/home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-23-phase-7-simple-evaluation-implementation.md
/home/minhhieu/hue_rag/reports/phase_7_retrieval_answer_evaluation_implementation_report.md
```

Nếu implementation report chưa tồn tại, Phase 7 chưa sẵn sàng để review.

Tài liệu code tham khảo trực tiếp cho Phase 7:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/pro_implementation
```

Tài liệu phong cách notebook:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0
/home/minhhieu/llm_rag/tai_lieu/notebook_simple
```

Hai tài liệu code Phase 7 không phải blueprint cho Phase 0–6. Khi review phase
cũ, dùng tài liệu riêng do người dùng cung cấp.

## Trình tự review

1. Chạy `git status --short` và xác định đúng changed files.
2. Đọc source thật, không chỉ tin implementation report.
3. Kiểm tra bốn module Phase 7 có đúng trách nhiệm và dễ hiểu không.
4. Kiểm tra chỉ còn một Phase 7 test file.
5. Chạy test, Qdrant, OpenAI và notebook thật.
6. Đối chiếu hai CSV với dữ liệu chạy vừa tạo.
7. Ghi rõ lỗi, giới hạn và phần chưa hoàn thành.
8. Viết Codex review report mới.

## Tiêu chí code

Reviewer phải đặt các câu hỏi:

1. Code này giải quyết nhu cầu thật nào?
2. Có cách đơn giản hơn không?
3. Người đọc có theo được data flow không?
4. Kỹ thuật nâng cao có kết quả chạy thật chứng minh lợi ích không?
5. Độ phức tạp có tương xứng với lợi ích không?

Nếu không trả lời rõ được, coi đó là over-engineering và yêu cầu đơn giản hóa.

Reviewer phải từ chối nếu Phase 7 vẫn giữ hoặc tạo lại:

- cost accounting hoặc cost estimation code;
- consent/confirmation gate;
- calibration;
- resume;
- run ID, generation run ID hoặc timestamp quản lý package;
- checksum hoặc matching package;
- tamper detection;
- partial artifact hoặc artifact audit;
- validator chồng lớp;
- nhiều test files phục vụ các cơ chế trên.

## Chạy thật, không fake

Quy tắc này áp dụng cho toàn hệ thống:

- Không fake ID, fake dataset, fake artifact, fake provider hoặc fake result.
- Không mock provider response hoặc replay output để chứng minh hệ thống chạy.
- Không chấp nhận expected output, fixture hoặc output cũ làm observed evidence.
- Không bỏ qua lỗi Qdrant, network, quota, model hoặc provider.
- Không chấp nhận báo cáo “PASS” nếu live run chưa chạy.

Reviewer được phép:

- dùng internet;
- dùng `.env` qua `uv --env-file`;
- gọi Qdrant thật;
- gọi paid API thật đã được người dùng cho phép;
- dùng `gpt-5.4-nano` cho generation;
- dùng `gpt-5.4-mini` cho judge;
- chạy lại 20 và 104 câu thật.

Không in hoặc log secrets. Active Hue Qdrant collection chỉ được đọc.

## Xác minh Phase 7

Từ `backend/`:

```bash
uv run --env-file ../.env python -m pytest tests/test_evaluation.py -q
```

Kiểm tra độc lập:

- `test2.jsonl` có đúng 20 câu thật và đủ 8 category;
- `tests.jsonl` vẫn có 104 câu;
- retrieval dùng keyword để tính MRR/nDCG;
- answer dùng production retrieval/context/generation path;
- generation model là `gpt-5.4-nano`;
- judge model là `gpt-5.4-mini`;
- judge chỉ trả accuracy, completeness, relevance và feedback;
- lỗi được ghi vào row và không bị retry hoặc che giấu;
- hai CSV có đúng thứ tự câu hỏi;
- hai nút giao diện chạy độc lập;
- slider concurrency mặc định là 3;
- Notebook 07 ngắn, tuyến tính, outputs rỗng trong repo và Run All thật đạt trên
  bản tạm.

Test pass không thay thế hai live batch runs.

## Review report

Sau khi review, tạo mới:

```text
/home/minhhieu/hue_rag/reports/phase_7_retrieval_answer_evaluation_codex_review.md
```

Report cần ngắn và rõ:

- verdict;
- changed files đã kiểm tra;
- nhận xét về độ đơn giản/dễ hiểu;
- lệnh live verification đã chạy;
- kết quả thật của 20 và 104 câu;
- lỗi còn lại;
- xác nhận không fake/mock/replay;
- yêu cầu sửa nếu có.

Không phục dựng nội dung review của kiến trúc Phase 7 cũ.

## Trạng thái và commit

- Reviewer chỉ cập nhật `Project_Status.md` sau khi review xong và người dùng
  xác nhận kết quả.
- Reviewer không commit hoặc push nếu người dùng chưa cho phép rõ trong session.
- Phase 8 vẫn bị chặn cho đến khi Phase 7 được duyệt và Phase 6 về Phase 0 đã
  được review về over-engineering bằng tài liệu riêng của từng phase.
