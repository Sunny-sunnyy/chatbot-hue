# Handoff triển khai Full-corpus RAG — Wave 1

Target role: implementer
Authored by: reviewer
Handoff kind: implementation
State: active
Base commit: ea87d3ed52851f6b6ab5c47b138540ebc8ff8340
Head commit: worktree
Risk level: medium (parser/source-locator correctness; no live mutation)
Git authorization: none
Sub-agent authorization: none

User đã duyệt Written Spec, Implementation Plan và Review Contract ngày
2026-09-11. Quyền hiện hành chỉ bao phủ **Wave 1**. Không tự bắt đầu Wave 2 hoặc
bất kỳ live gate nào.

## 1. Objective và stop condition

Triển khai deterministic full-corpus discovery, Markdown parser/chunker,
condition attachment, source locator và preview cho representation A theo Wave
1 của approved Plan. Kết quả phải kiểm được trên toàn curated corpus nhưng chưa
embedding, chưa tạo point và chưa đọc/ghi Qdrant.

Kết thúc khi:

1. code/config/tests và preview artifact Wave 1 đã hoàn tất;
2. mọi required technical check đã chạy hoặc được ghi rõ failed/blocked;
3. implementation report ánh xạ acceptance sang evidence hiện hành;
4. `CURRENT_HANDOFF.md` chuyển sang Reviewer/`final_review`.

Không tự đổi guide/spec/plan/Review Contract hoặc đánh dấu Wave 1 approved.

## 2. Bootstrap và mức đọc

Với mọi file `full-read`, nếu output bị cắt/truncate phải đọc tiếp từ dòng dừng
đến EOF.

### Full-read

Đọc theo thứ tự:

1. `session_prompt/Session_Prompt.md`;
2. `session_prompt/IMPLEMENTER_WORKFLOW.md`;
3. `skills/risk-gated-agent-review/SKILL.md`;
4. `skills/practical-project-coding/SKILL.md`;
5. `session_prompt/CURRENT_HANDOFF.md`;
6. `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md`;
7. `docs/superpowers/plans/2026-09-11-full-corpus-rag-implementation-plan.md`;
8. `handoff_prompt/FULL_CORPUS_RAG_IMPLEMENTATION_REVIEW_CONTRACT.md`;
9. các file hiện hành bị Wave 1 tác động:
   - `pyproject.toml`;
   - `backend/config/settings.yaml`;
   - `backend/core/settings_loader.py`;
   - `backend/core/schema.py`;
   - `backend/ingestion/chunking/markdown_chunker.py`;
   - `backend/ingestion/helpers/split_text.py`;
   - `backend/ingestion/pipeline.py`;
   - `backend/tests/test_markdown_chunker.py`;
   - `backend/tests/test_ingestion_pipeline.py`.

Đọc full sáu input acceptance:

- `knowledge-base-hue/foods/restaurants/quan bun bo me keo.md`;
- `knowledge-base-hue/festivals/festival/Hội xuân Gia Lạc.md`;
- `knowledge-base-hue/heritages/heritage/Đại Nội Huế.md`;
- `knowledge-base-hue/travel/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md`;
- `knowledge-base-hue/performing_arts/arts/Ca Huế trên sông Hương.md`;
- `knowledge-base-hue/travel/services/Chi phí du lịch Huế.md`.

### Targeted-read

- `session_prompt/Project_Status.md`: `Project overview`, `Current runtime and
  data`, `Thiết kế full-corpus hiện hành`, `Phase status`, safety boundaries và
  canonical map.
- `guides/full_corpus_rag.md`: trạng thái, quyết định đã chốt và chuỗi tài liệu.
- `reports/full_corpus_parser_locator_survey_2026_09_09.md`: parser config,
  span/normalization findings và condition-selector recommendation.
- `reports/artifacts/full_corpus_parser_locator_survey_2026_09_09.py` và
  `reports/artifacts/full_corpus_parser_locator_samples_2026_09_09.json`: chỉ
  exact helpers/examples cần đối chiếu; không copy survey script thành runtime.
- Source corpus ngoài sáu mẫu: chỉ file/section cần điều tra một preview error
  hoặc test cụ thể.

### Reference-only

Không đọc mặc định:

- survey `llm_rag` 885 dòng, correction cũ và implementation reports lịch sử;
- hai tài liệu `rag_agent_handoff_current_repo.md` và
  `rag_system_pipeline_deep_dive.md`;
- raw source dumps, notebooks, transcripts, `.env`, logs, model cache,
  `qdrant_storage` và generated/binary state;
- lịch sử brainstorming dài ngoài snapshot/decision exact cần giải quyết.

## 3. Scope implementation bắt buộc

1. Thêm direct dependency duy nhất `markdown-it-py` với range hẹp tương thích
   major 4; cập nhật `uv.lock` nhất quán. Không thêm parser/dependency khác.
2. Khai báo full-corpus discovery đúng include/exclude và hai exact inventory
   exclusions trong approved Plan; output source paths POSIX, relative và sort
   ổn định.
3. Đọc UTF-8 strict, normalize CRLF/CR thành LF trước parse/hash/offset; không
   Unicode-normalize hoặc sửa evidence text.
4. Dùng `markdown-it-py` với table rule để tạo blocks có source spans và
   `heading_path`; evidence luôn slice từ source LF.
5. Thực hiện grouping/splitting tối thiểu cho paragraph, nested list, table,
   blockquote, intro và image-only behavior đúng Spec. Không overlap cố định,
   không cắt giữa sentence/list item/table cell và không tạo NLP framework.
6. Tạo `backend/config/full_corpus_conditions.json` đúng schema selector nhỏ;
   mỗi selector phải match đúng một block. Missing/duplicate/text mismatch gom
   vào blocking preview errors; không match-first, regex DSL hoặc fallback.
7. Tạo schema `EvidencePart`/chunk, representation-A `search_text`, deterministic
   `(source, chunk_ordinal)` ID và UUID5 point-ID helper. Chưa tạo Qdrant point.
8. Tạo source LF/hash/build-record utilities nhưng **không** ghi completion
   record trong Wave 1.
9. Preview toàn corpus phải gom hết H1/empty/duplicate/span/condition/token-limit
   errors rồi fail closed. Không truncate, skip hoặc xuất partial-success.
10. Tokenizer check dùng preprocessing thật của cả ba approved dense candidates
    với `truncation=False`; chỉ load tokenizer local/offline, không inference và
    không download model. Thiếu tokenizer cần thiết là blocker trung thực.

Wave 1 không cutover active Foods ingestion/Qdrant path. Nếu giữ legacy Foods
entry point tạm thời để mainline không bị gãy trước Wave 2, full-corpus preview
vẫn phải có đúng một parser/chunker implementation canonical; không sao chép
logic thành pipeline thứ hai.

## 4. Allowed paths

Implementer chỉ được tạo/sửa:

- `pyproject.toml`, `uv.lock`;
- `backend/config/settings.yaml`;
- `backend/config/full_corpus_conditions.json`;
- `backend/core/settings_loader.py`, `backend/core/schema.py`;
- các module Wave 1 dưới `backend/ingestion/` và các `__init__.py` liên quan;
- `backend/tests/conftest.py`, `backend/tests/test_markdown_chunker.py`,
  `backend/tests/test_ingestion_pipeline.py` và test mới tên
  `backend/tests/test_full_corpus_*.py`;
- `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`;
- `reports/full_corpus_rag_wave_1_implementation_report_2026_09_11.md`;
- `session_prompt/CURRENT_HANDOFF.md`.

Không sửa corpus, API, embedding, vectorstore, retrieval, generation, frontend,
Golden/evaluation, notebook, guide/status/spec/plan/Review Contract hoặc report
lịch sử. Nếu cần path ngoài danh sách để đạt contract, dừng và trả Reviewer.

Preview artifact chỉ chứa schema/version ổn định, relative source paths,
file/chunk counts tổng và theo P7/domain, condition counts, tokenizer limits,
oversized groups và errors. Không chứa corpus excerpts, absolute paths, secret,
timestamp biến động hoặc build-complete claim. Cùng input/config phải tạo bytes
giống nhau.

## 5. Tests và verification được phép

Tests phải bảo vệ behavior, không chỉ snapshot dễ cập nhật. Bắt buộc có:

- include/exclude, deterministic order và hai inventory exclusions;
- CRLF/CR, Unicode code-point offsets, repeated text và exact slicing;
- intro/H1/H2+, nested list, table, blockquote, image-only và separator;
- condition success/missing/duplicate/mismatch;
- assertions có ý nghĩa cho sáu input acceptance;
- oversized minimal group và any-error chặn toàn preview;
- repeated run deep-equal chunks, IDs và preview artifact.

Các lệnh được phép:

```bash
git status --short
UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-uv-cache uv lock
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-uv-cache uv run python -m pytest <exact affected Wave 1 test files> -q --tb=short
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-uv-cache uv run python -m pytest backend/tests -q --tb=short
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-uv-cache uv run python -m backend.ingestion.preview --output reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json
git diff --check
```

Tên module preview trên là public execution contract của Wave 1. Có thể chia
helpers nội bộ nhưng lệnh này phải hoạt động từ repository root. `uv lock`/`uv
run` chỉ được resolve dependency đã duyệt; không nâng dependency ngoài thay đổi
tối thiểu cần cho `markdown-it-py`.

Không gọi model/API, không embedding inference, không kết nối/ghi Qdrant, không
chạy frontend/notebook/benchmark, không đọc `.env`/logs và không Git write.

## 6. Acceptance và report

Wave 1 đạt technical readiness khi:

- preview có toàn bộ curated scope, deterministic và zero blocking errors;
- every evidence part toàn preview exact-match source LF;
- mọi representation A hoàn chỉnh vừa cả ba tokenizer limits, không truncate;
- IDs/UUID5 không duplicate và lặp lại ổn định;
- condition selectors exact-one-match;
- six sample tests kiểm nội dung/range/quan hệ thật, không chỉ count;
- dependency/lockfile tối thiểu và `git diff --check` sạch;
- active Foods collections/data không bị truy cập hoặc mutation.

Report dùng `session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md`, đủ sáu mục và
ghi exact commands/exit status/counts. Phân định task paths với modified/untracked
đã tồn tại trước; không gọi worktree sạch. Nêu rõ failed/skipped/not verified,
không biến expected values thành observed evidence.

Handoff cuối phải target `reviewer`, kind `final_review`, risk `medium`, Git
authorization `none`; trỏ report, preview, exact changed files và acceptance
mapping. Reviewer hiện chỉ được static/read-only review, không được rerun tests,
model/API/Qdrant/frontend/notebook/benchmark.

Wave 1 closure không tự mở Wave 2. Sau Reviewer review và User closure, Reviewer
cập nhật detailed Phase 2 guide/status rồi soạn Wave 2.1 Phase 3 design package
để User duyệt trước một Implementer handoff mới.

## 7. Next action duy nhất

Implementer thực hiện đầy đủ Wave 1, self-verify, tạo report/preview và chuyển
`CURRENT_HANDOFF.md` sang Reviewer `final_review`. Không bắt đầu Wave 2.
