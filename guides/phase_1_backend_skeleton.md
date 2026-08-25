# Phase 1: Backend skeleton và configuration

## Mục tiêu

Phase 1 giữ nền tảng Python nhỏ và dễ đọc cho Hue Foods RAG:

- package layout rõ theo data flow;
- một file YAML cấu hình tập trung;
- một hàm đọc settings và kiểm tra profile đang dùng;
- một cấu hình logging chung được các runtime entrypoint gọi thật;
- một shared `RetrievedDocument` cho retrieval, reranking và context.

## Trạng thái

```text
Status: approved
Previous approval +07: 2026-08-09
Simplicity design approval +07: 2026-08-24
Simplicity confirmation +07: 2026-08-24
Implementer: Antigravity
Reviewer: Codex
```

Phase 1 từng được approve và đã làm nền cho Phase 2–7. User đã duyệt design
đơn giản hóa mới, implementation đã hoàn tất technical review độc lập và được
user xác nhận ngày `2026-08-24 +07`. Phase đã trở lại `approved`. Phase 2–5
simplicity review cũng đã hoàn tất; bước tiếp theo của campaign là Phase 6.

Tài liệu bắt buộc:

```text
docs/superpowers/specs/2026-08-24-phase-1-backend-foundation-simplicity-design.md
docs/superpowers/plans/2026-08-24-phase-1-backend-foundation-simplicity-implementation.md
reports/phase_1_backend_skeleton_simplicity_review.md
reports/phase_1_backend_skeleton_simplicity_implementation_report.md
reports/phase_1_backend_skeleton_simplicity_codex_review.md
reports/user_reports/phase_1_backend_skeleton_simplicity_user_report.md
guides/llm_rag_reference_for_hue_rag.md
```

## Baseline cần giữ

- Ba profiles: `dense_only`, `hybrid_no_rerank`, `hybrid_rerank`.
- Settings groups hiện tại và mọi value downstream đang dùng.
- Logging ra console và `backend/logs/application.log`.
- `RetrievedDocument(id, score, text, metadata)`.
- Mọi hành vi ingestion, embedding, Qdrant, retrieval, generation, API và
  evaluation đang hoạt động.
- Full backend baseline lịch sử trước review: `222 passed, 4 warnings`; số test
  không phải acceptance target hoặc bằng chứng rằng mọi test đều cần thiết.

Active Hue Qdrant collection giữ read-only.

## Package và file nền tảng

Giữ package layout hiện tại của:

```text
api
core
embedding
evaluation
ingestion
llm
reranking
retrieval
scoring
vectorstore
```

Files nền tảng được giữ:

```text
backend/config/settings.yaml
backend/config/logging.yaml
backend/core/settings_loader.py
backend/core/logging_setup.py
backend/core/schema.py
```

Không tạo package, interface hoặc factory mới trong Phase 1.

## Configuration contract

`load_settings()` phải:

1. đọc `backend/config/settings.yaml` bằng `yaml.safe_load`;
2. kiểm tra `active_profile` nằm trong `profiles`;
3. trả về settings mapping;
4. ném `ValueError` có danh sách profile hợp lệ khi profile sai.

Validation được viết trực tiếp trong `load_settings()`. Không giữ helper chỉ có
một caller, không tạo typed/nested settings model và không thêm environment
override dài.

Ba profiles giữ nguyên:

| Profile | `retrieval_mode` | `use_bm25` | `use_reranker` |
|---|---|---:|---:|
| `dense_only` | `dense` | `false` | `false` |
| `hybrid_no_rerank` | `hybrid` | `true` | `false` |
| `hybrid_rerank` | `hybrid` | `true` | `true` |

Phase 1 chỉ sở hữu loader và profile validation. Các settings groups được
review ở phase sở hữu chúng:

| Group | Phase |
|---|---:|
| `knowledge_base` | 2 |
| `embedding` | 3 |
| `vector_database` | 4 |
| `retrieval`, `reranking` | 5 |
| `llm` | 6 |
| `evaluation` | 7 impact assessment |

Implementer không xóa hoặc kết nối field downstream trong scope Phase 1.

## Logging contract

`setup_logging()` tiếp tục:

- tạo `backend/logs/` khi cần;
- đọc `backend/config/logging.yaml`;
- áp dụng config bằng `logging.config.dictConfig`;
- pin log file theo backend path để không phụ thuộc cwd.

Ba runtime entrypoint phải gọi hàm này:

```text
FastAPI lifespan -> setup_logging() -> build runtime
ingestion main() -> setup_logging() -> run_ingestion()
evaluation main() -> setup_logging() -> launch Gradio
```

Không gọi `setup_logging()` ở import time. Module con chỉ dùng
`logging.getLogger(...)`. Không thêm wrapper, decorator, middleware, retry,
rotation hoặc remote logging.

Log được phép chứa identifiers, counts, startup state và non-sensitive summary.
Không log secrets, environment values, full settings, raw question/context/
answer, vectors hoặc knowledge-base body. Logging config lỗi phải fail rõ ràng;
không có fallback âm thầm.

## Shared schema và errors

`RetrievedDocument` là data contract Phase 1 cần giữ:

```text
id
score
text
metadata
```

Các retrieval/generation error classes hiện có trong `core/schema.py` do Phase
5–6 thêm vào nên Phase 1 không sửa chúng. Coordinated Phase 4–5 review đã xử lý
retrieval ownership; các class thuộc generation/API được audit trong simplicity
review Phase 6 tiếp theo.

## Scope của Implementer

Sửa:

```text
backend/core/settings_loader.py
backend/api/app.py
backend/ingestion/pipeline.py
backend/evaluation/evaluator.py
```

Xóa:

```text
notebooks/01_backend_foundation.ipynb
backend/config/README_config.md
```

Không sửa config values, logging YAML structure, schema errors, tests hoặc
module downstream ngoài thay đổi import/call tối thiểu đã nêu. Nếu cần mở rộng
scope, dừng và báo user/Reviewer.

Implementer viết implementation report mới, không sửa guide, simplicity
review, Project Status hoặc reports lịch sử; không stage, commit hay push.

## Notebook

Phase 1 không cần notebook. Notebook 01 hiện là smoke/validation suite cho
package, config, logging và dataclass; code và guide đã đủ để con người hiểu.

Notebook chỉ được tạo cho phase có giá trị học tập thật. Khi một phase giữ
notebook, bắt buộc tham khảo:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/*.ipynb
/home/minhhieu/llm_rag/tai_lieu/notebook_simple/**/*.ipynb
```

## Verification

Implementer và Reviewer phải dùng bằng chứng thật:

1. compile các module bị ảnh hưởng;
2. load canonical settings và kiểm tra cả ba profiles;
3. gọi logging thật, quan sát console và `application.log`;
4. start API với real Qdrant và local E5, kiểm tra startup/health;
5. start evaluation UI đủ để xác nhận logging setup;
6. xác nhận active collection và Phase 7 CSV không đổi;
7. chạy `git diff --check` và scan conflict marker.

Không dùng mock/fake hoặc prior output làm completion evidence. Không mutation
active collection. Phase 1 không cần automated test: exact live paths trên đủ
để chứng minh logging/settings wiring. Affected `74` tests và full `222` tests
đã chạy trong review chỉ là observed history quá rộng, không phải requirement
cho lần chạy lại.

Không cần chạy lại full 104-question Phase 7 evaluation vì scope này không đổi
RAG quality. Nếu implementation chạm chunk, vector, retrieval, context, prompt,
model hoặc metric, dừng và mở rộng verification.

## Acceptance

Phase 1 chỉ trở lại `approved` khi:

- code đúng exact scope, trực tiếp và user đọc được;
- logging chạy qua cả ba real entrypoints;
- settings/profile và `RetrievedDocument` không regression;
- Notebook 01 và config README trùng lặp đã bị xóa;
- API, Gradio, logging, settings và Qdrant live checks đạt;
- không conflict hoặc thay đổi ngoài phạm vi;
- simplicity review có After state và Reviewer conclusion;
- user xác nhận kết quả.

## Bước tiếp theo

Phase 1–5 simplicity review đã hoàn tất và được user xác nhận. Bước tiếp theo
của simplicity campaign là Phase 6 theo `guides/README.md`.
