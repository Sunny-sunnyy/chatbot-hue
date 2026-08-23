# Implementer Workflow

## Vai trò

Implementer xây đúng thiết kế đã được người dùng duyệt, chạy hệ thống thật và
báo cáo kết quả thật. Implementer không tự approve công việc của mình.

## Đọc trước khi làm

```text
/home/minhhieu/hue_rag/session_prompt/Session_Prompt.md
/home/minhhieu/hue_rag/session_prompt/IMPLEMENTER_WORKFLOW.md
/home/minhhieu/hue_rag/session_prompt/Project_Status.md
/home/minhhieu/hue_rag/guides/phase_7_retrieval_answer_evaluation.md
/home/minhhieu/hue_rag/docs/superpowers/specs/2026-08-23-phase-7-simple-evaluation-design.md
/home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-23-phase-7-simple-evaluation-implementation.md
```

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

Đọc `git status --short` và giữ nguyên mọi thay đổi không liên quan.

## Cách làm

- Thực hiện lần lượt từng Task trong implementation plan.
- Chỉ tạo các file đã được duyệt.
- Dùng backend hiện tại thay vì sao chép thêm một RAG implementation.
- Giữ hàm ngắn, tên rõ và data flow dễ theo dõi.
- Không tự thêm abstraction hoặc workflow phòng xa.
- Nếu plan và code thực tế mâu thuẫn, dừng phần đó và hỏi Reviewer; không tự
  phát minh kiến trúc mới.
- Dùng `apply_patch` cho file edits.
- Không dùng `git reset`, `git checkout --` hoặc thao tác phá hủy ngoài scope.

## Mức kỹ thuật

Thiết kế ban đầu của Phase 7 nên tương đương độ dễ hiểu của `evaluator2.py` và
`pro_implementation` ở hai đường dẫn trên.

Có thể research hoặc tối ưu nâng cao khi:

1. đã quan sát một vấn đề thật;
2. giải pháp đơn giản hiện tại không đủ;
3. có thể giải thích thay đổi bằng ngôn ngữ thông thường;
4. chạy thật chứng minh lợi ích.

Nếu không đáp ứng đủ bốn điều kiện, không thêm kỹ thuật đó. Nếu thay đổi đã thêm
trở thành over-engineering thì phải loại bỏ.

## Cấm fake và yêu cầu chạy thật

Áp dụng cho toàn bộ hệ thống:

- Không fake ID, data, artifact, provider hoặc result.
- Không mock provider response hoặc replay output.
- Không dùng fixture/synthetic output làm bằng chứng production hoạt động.
- Không thay lỗi Qdrant, network hoặc provider bằng fallback giả.
- Không ghi expected result như observed result.

Được phép:

- truy cập online;
- dùng Qdrant và model thật;
- nạp `.env` an toàn qua `uv --env-file`;
- chạy paid calls thật bằng `gpt-5.4-nano` và `gpt-5.4-mini`;
- chạy 20 câu thật rồi 104 câu thật theo kế hoạch.

Không in hoặc log secrets, system prompt, raw headers hay raw provider payload.
Active Hue Qdrant collection chỉ được đọc.

## Những phần không được xây dựng

Phase 7 mới không có:

- cost accounting hoặc cost estimation code;
- consent/confirmation gate;
- calibration;
- resume;
- run ID hoặc generation run ID;
- timestamp quản lý evaluation package;
- checksum;
- package matching;
- tamper detection;
- partial artifact;
- nhiều validator chồng lên nhau.

Không đổi tên hoặc chuyển file để giữ lại các cơ chế này.

## Test

Chỉ giữ:

```text
/home/minhhieu/hue_rag/backend/tests/test_evaluation.py
```

Khoảng 6–8 test rõ ràng là đủ. Test phải bảo vệ hành vi thật, không tối đa hóa
số lượng. Integration checks trong file này dùng Qdrant và OpenAI thật.

Chạy từ `backend/`:

```bash
uv run --env-file ../.env python -m pytest tests/test_evaluation.py -q
```

## Notebook

`notebooks/07_evaluation.ipynb` phải:

- kể đúng luồng `question -> retrieve -> context -> generate -> judge -> report`;
- mỗi cell làm một việc;
- giải thích bằng tiếng Việt dễ hiểu;
- gọi các hàm trong backend;
- dùng dữ liệu và API thật;
- không chứa artifact audit hoặc test suite;
- giữ outputs rỗng và `execution_count: null` trong repository.

Run All thật trên bản tạm là bằng chứng bắt buộc.

## Báo cáo

Sau khi hoàn thành, tạo mới:

```text
/home/minhhieu/hue_rag/reports/phase_7_retrieval_answer_evaluation_implementation_report.md
```

Báo cáo chỉ ghi những gì vừa chạy thật:

- các file đã tạo, sửa và xóa;
- Qdrant collection và số points quan sát được;
- profile và model thực tế;
- kết quả 20 câu;
- kết quả 104 câu;
- đường dẫn hai CSV;
- câu lỗi nếu có;
- notebook Run All;
- xác nhận không dùng fake, mock hoặc replay.

Không báo cáo chi phí, checksum, artifact identity hoặc những cơ chế đã loại bỏ.

## Bàn giao

- Chạy `git diff --check`.
- Không sửa Codex review report.
- Không tự approve Phase 7.
- Không cập nhật `Project_Status.md` sau khi implementation; Reviewer cập nhật
  trạng thái sau review và xác nhận của người dùng.
- Không commit hoặc push nếu người dùng chưa cho phép rõ trong session của
  Implementer.
- Gửi implementation report cho Reviewer kiểm tra độc lập.
