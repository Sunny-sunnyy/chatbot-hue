# Phase 1: Backend skeleton và configuration

## Mục tiêu và giá trị cho người dùng

Phase 1 tạo bộ khung Python ổn định cho toàn bộ Hue Foods RAG MVP: cấu hình tập trung, logging nhất quán, shared retrieval schema và package layout rõ ràng. Phase này giúp các phase sau thêm chức năng mà không phải tự phát minh lại cấu trúc hoặc config contract.

## Trạng thái

```text
Status: approved
Document type: as-built, locked
Brainstorming level: Level 0 - locked
Implementer: DeepSeek
Reviewer: Codex
Approval date +07: 2026-08-09
```

Guide mô tả implementation đã được phê duyệt. Thay đổi mới phải mở scope mới; không sửa lịch sử acceptance.

## Dependency

- Phase 0 architecture foundation đã hoàn tất.
- `pyproject.toml` và `uv.lock` đã tồn tại.
- Phase này không cần Qdrant, embedding model, API key hoặc live service.

## Chức năng đã thực hiện

- Tạo backend package tree cho API, ingestion, embedding, vector store, retrieval, scoring, reranking, LLM và evaluation.
- Tạo `settings.yaml` chứa ba retrieval profiles và các nhóm config dự kiến cho MVP.
- Tạo YAML settings loader và fail-fast validation cho `active_profile`.
- Tạo logging setup ghi console và `backend/logs/application.log` độc lập với current working directory.
- Tạo shared `RetrievedDocument` dataclass cho retrieval pipeline.

## Files canonical

```text
backend/config/settings.yaml
backend/config/logging.yaml
backend/config/README_config.md
backend/core/settings_loader.py
backend/core/logging_setup.py
backend/core/schema.py
backend/api/__init__.py
backend/api/routes/__init__.py
backend/core/__init__.py
backend/embedding/__init__.py
backend/evaluation/__init__.py
backend/ingestion/__init__.py
backend/ingestion/chunking/__init__.py
backend/ingestion/helpers/__init__.py
backend/llm/__init__.py
backend/reranking/__init__.py
backend/reranking/models/__init__.py
backend/retrieval/__init__.py
backend/scoring/__init__.py
backend/vectorstore/__init__.py
```

`backend/data/`, `backend/scripts/` và `backend/test.ipynb` có sẵn trước phase và không thuộc scope.

## Configuration contract đã chấp nhận

Ba profile phải resolve như sau:

| Profile | `retrieval_mode` | `use_bm25` | `use_reranker` |
|---|---|---:|---:|
| `dense_only` | `dense` | `false` | `false` |
| `hybrid_no_rerank` | `hybrid` | `true` | `false` |
| `hybrid_rerank` | `hybrid` | `true` | `true` |

Các nhóm config hiện có:

```text
active_profile
profiles
knowledge_base
embedding
vector_database
retrieval
reranking
llm
evaluation
```

`embedding.vector_size` và `vector_database.vector_size` cùng tồn tại trong as-built config. Chúng phải đồng bộ; thay model/dimension yêu cầu reindex với collection reset được phê duyệt.

## Interface contract

`load_settings()`:

- đọc YAML settings canonical;
- trả về mapping settings;
- xác nhận `active_profile` tồn tại trong `profiles`;
- ném `ValueError` có danh sách profile hợp lệ khi profile sai;
- không đọc environment secret trong Phase 1.

`setup_logging()`:

- tạo `backend/logs/` khi cần;
- áp dụng `backend/config/logging.yaml`;
- log file luôn là `backend/logs/application.log` dù command chạy từ cwd nào;
- không log config secret hoặc environment.

`RetrievedDocument` là shared schema cho các phase retrieval/reranking/context sau này. Phase 1 chỉ định nghĩa schema, không tạo retrieval behavior.

## Brainstorming

Không cần brainstorming lại. Các quyết định sau đã khóa:

- Dùng YAML config tập trung.
- Profile validation fail fast.
- Package markers giữ tối giản.
- Environment override được hoãn đến phase thực sự cần provider credentials.
- Phase 1 không thêm unit test file vì approved gate dùng compile và smoke commands.

Nếu thay config group, schema field hoặc secret-loading policy, phải mở scope mới và phân tích ảnh hưởng đến Phase 3–8.

## Nhiệm vụ của DeepSeek Implementer

Phase đã hoàn tất. Nếu có scope mới:

- không refactor adjacent modules;
- duy trì backward compatibility cho guide phase sau hoặc cập nhật guide qua Codex trước;
- viết test tái hiện nếu sửa logic;
- không tự thay profile semantics;
- tạo implementation report mới theo scope được phê duyệt.

## Nhiệm vụ của Codex Reviewer

- Bảo vệ trạng thái as-built và accepted deviations.
- Khi review scope mới, kiểm tra config drift, logging secret exposure, schema blast radius và import safety.
- Không cho phép thay đổi lịch sử report/verdict để hợp thức hóa behavior mới.

## Notebook

Phase 1 không yêu cầu và không tạo notebook.

## Validation đã được phê duyệt

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "from core.settings_loader import load_settings; print(load_settings()['active_profile'])"
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile core/settings_loader.py core/logging_setup.py core/schema.py
```

Bằng chứng đã chấp nhận:

- `active_profile` trả về `dense_only`.
- Cả ba profiles resolve đúng mode/BM25/reranker flags.
- Profile không hợp lệ ném `ValueError` kèm valid list.
- Ba core modules compile sạch.
- Logging ghi console và đúng log path; smoke-test log được xóa sau validation.
- Không đọc hoặc in secrets.

## Accepted deviations

- Có thêm `backend/config/README_config.md` để khớp directory design.
- `vector_size` xuất hiện trong cả embedding và vector database config cùng cảnh báo sync/reindex.
- Environment-variable override được hoãn đến Phase 6.
- Logging file path được pin theo absolute backend path để không phụ thuộc cwd.

## Known limitations

- OpenAI model IDs trong config thời điểm review là defaults chưa được xác minh; Phase 6 phải dùng quyết định model mới đã được user chốt.
- Qdrant/Docker availability chưa được kiểm tra; Phase 4 chịu trách nhiệm preflight.
- Chưa có runtime ingestion, retrieval, model call, API hoặc evaluation.

## Security, reliability và performance

- Không có secret hoặc live access.
- Settings loading deterministic và invalid profile fail fast.
- Không có model loading hay external service overhead.
- Logging không để lại smoke artifact sau review.

## Reports và bằng chứng

```text
reports/phase_1_backend_skeleton_implementation_report.md
reports/phase_1_backend_skeleton_codex_review.md
```

Codex verdict: `approved`.

## Tiêu chí phê duyệt

- Backend package skeleton đúng phạm vi.
- Settings load và profile validation hoạt động.
- Logging hoạt động độc lập cwd.
- Shared schema import được.
- Không có network/model/Qdrant/data mutation.
- Không có secret exposure.

Tất cả tiêu chí đã đạt ngày 2026-08-09.

## Bước tiếp theo

Phase 2 đã được phép và đã hoàn tất. Không còn action trong Phase 1 nếu người dùng không mở scope mới.
