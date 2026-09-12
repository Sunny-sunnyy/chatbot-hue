# Full-corpus RAG Wave 1 — Correction 1

Target role: implementer
Authored by: reviewer
Handoff kind: correction
State: active
Base commit: ea87d3ed52851f6b6ab5c47b138540ebc8ff8340
Head commit: worktree
Risk level: medium
Git authorization: none
Sub-agent authorization: none

## Objective và nguồn điều khiển

Đóng đúng năm Major W1-R1..W1-R5 tại
`reports/full_corpus_rag_wave_1_codex_review_2026_09_12.md`. Đây là correction
delta hẹp của Wave 1; approved Written Spec, Plan, Review Contract và Wave 1
prompt vẫn giữ hiệu lực. Không bắt đầu Wave 2.1.

Sau bootstrap Implementer, áp dụng mức đọc sau. Với mọi file `full-read`, nếu
output bị cắt/truncate phải tiếp tục từ dòng dừng đến EOF.

### Full-read

1. `reports/full_corpus_rag_wave_1_codex_review_2026_09_12.md`;
2. `handoff_prompt/FULL_CORPUS_RAG_WAVE_1_CORRECTION_1_PROMPT.md`;
3. `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md`;
4. `docs/superpowers/plans/2026-09-11-full-corpus-rag-implementation-plan.md`;
5. `handoff_prompt/FULL_CORPUS_RAG_IMPLEMENTATION_REVIEW_CONTRACT.md`;
6. `handoff_prompt/FULL_CORPUS_RAG_WAVE_1_IMPLEMENTATION_PROMPT.md`;
7. `reports/full_corpus_rag_wave_1_implementation_report_2026_09_11.md`;
8. `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`;
9. `pyproject.toml`;
10. `backend/config/settings.yaml`;
11. `backend/config/full_corpus_conditions.json`;
12. `backend/core/settings_loader.py`;
13. `backend/core/schema.py`;
14. `backend/ingestion/source_state.py`;
15. `backend/ingestion/chunking/markdown_blocks.py`;
16. `backend/ingestion/chunking/full_corpus_chunker.py`;
17. `backend/ingestion/preview.py`;
18. `backend/tests/conftest.py`;
19. `backend/tests/test_full_corpus_chunker.py`;
20. `backend/tests/test_markdown_chunker.py` và
    `backend/tests/test_ingestion_pipeline.py` nếu correction sửa hoặc dùng chúng
    làm acceptance evidence.

### Targeted-read

Chỉ đọc exact Option A tại
`docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md:420-496`.
Đọc exact `markdown-it-py` package/project entries và correction diff trong
generated `uv.lock`; không mở rộng generated lockfile ngoài dependency check.

### Reference-only

Các guide/status, survey/correction/report lịch sử khác, raw source dumps,
notebooks, `.env`, logs, caches, Qdrant state và wave sau không đọc mặc định.

## Required correction delta

1. Giải quyết exact oversized item `heritages/heritage/Điện Hòn Chén.md`, dòng
   nguồn LF chứa nhãn “Bước ngoặt thời vua Đồng Khánh…” ngay trong Wave 1:
   - không sửa corpus, model, 256-token limit hoặc evidence text;
   - chia ở ranh giới câu nguồn thành các nhóm còn đủ nghĩa; giữ toàn bộ câu,
     thứ tự và lặp exact leading label bằng source-sliced evidence part;
   - mỗi full representation phải vừa cả ba tokenizer;
   - nếu không thể đạt mà không đổi contract, dừng và trả Reviewer, không đẩy
     ngoại lệ sang Wave 2.1.
2. Sửa table/list/paragraph/grouping behavior W1-R2 bằng logic trực tiếp:
   - table tbody rows dùng token state đúng, không trộn source-line index với
     token index;
   - split nested list không bỏ parent label/body;
   - paragraph dài split tại source sentence boundary;
   - không greedily merge mọi sibling cùng heading chỉ để lấp token budget.
3. Validate condition rules toàn corpus: schema nhỏ hợp lệ, source discovered,
   condition và từng target exact-one; mọi configured rule được accounted;
   actual counts derive từ config/resolution và settings truyền vào được dùng.
4. Bỏ tokenizer fail-open. Dùng một nguồn trực tiếp cho ID/limit/prefix,
   local-only resolution, `truncation=False`; thiếu bất kỳ tokenizer nào là
   blocker ở canonical entry points. Không hard-code absolute home snapshot path.
5. Bổ sung/siết tests và artifact theo W1-R5:
   - CRLF/CR locator + repeated text;
   - H1/intro/H2+, nested list/table/blockquote/image/separator;
   - condition source/condition/target missing, duplicate, mismatch;
   - paragraph/list/table split giữ exact evidence;
   - đúng sáu named corpus files, với content/range/relationship assertions;
   - synthetic any-error/oversized fail-closed;
   - canonical full-corpus preview PASS;
   - repeated full corpus chunks/IDs/UUID5 và preview bytes deep-equal;
   - preview có deterministic five-domain và seven-P7 breakdown.

Không thêm framework, NLP dependency, rule DSL, generic registry, retry/resume,
fallback, partial success hoặc test chỉ khóa implementation detail.

## Allowed paths

Chỉ sửa lại exact Wave 1 task paths đã được active prompt cho phép:

- `backend/config/settings.yaml`, `backend/config/full_corpus_conditions.json`;
- `backend/core/settings_loader.py`, `backend/core/schema.py` khi thật sự cần;
- Wave 1 modules dưới `backend/ingestion/`;
- `backend/tests/conftest.py`, `backend/tests/test_markdown_chunker.py`,
  `backend/tests/test_ingestion_pipeline.py`, `backend/tests/test_full_corpus_*.py`;
- `pyproject.toml`, `uv.lock` chỉ nếu correction thật sự cần, nhưng không thêm
  dependency mới;
- preview artifact hiện hành;
- một correction implementation report mới;
- `session_prompt/CURRENT_HANDOFF.md`.

Không sửa corpus, guides/status, approved spec/plan/Review Contract, review report,
implementation report cũ, API/embedding/vectorstore/retrieval/generation/frontend,
Golden/evaluation/notebook hoặc pre-existing unrelated paths.

## Acceptance và checks phải chạy lại

Acceptance chỉ đạt khi:

- canonical preview `PASS`, exit 0, zero errors, zero oversized groups;
- mọi full representation vừa cả ba tokenizer, không truncate;
- all evidence parts exact slice source LF, không mất/đảo content;
- condition rules exact-one toàn corpus và counts được derive;
- no duplicate chunk ID/UUID5; full repeated outputs và artifact byte-identical;
- table/list/paragraph/blockquote/image/heading behavior và sáu exact samples có
  tests có ý nghĩa;
- artifact đủ total/domain/P7 counts và không chứa excerpts/absolute paths;
- không có silent fallback/partial output, Qdrant/API/model inference/live access;
- `git diff --check` sạch.

Implementer phải chạy fresh:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-correction1-uv-cache uv run python -m pytest backend/tests/test_full_corpus_chunker.py backend/tests/test_markdown_chunker.py backend/tests/test_ingestion_pipeline.py -q --tb=short
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-correction1-uv-cache uv run python -m pytest backend/tests -q --tb=short
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-correction1-uv-cache uv run python -m backend.ingestion.preview --output reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json
git diff --check
```

Không gọi model/API, embedding inference, Qdrant, frontend, notebook hoặc
benchmark. Full-suite failure phải ghi exact failing/error test groups và nguyên
nhân quan sát được; không quy toàn bộ cho live dependencies nếu không có index.

Tạo `reports/full_corpus_rag_wave_1_correction_1_implementation_report_2026_09_12.md`
với acceptance mapping, exact commands/status/counts, changed paths, evidence
reuse và mọi failed/skipped/not verified. Không sửa report cũ.

## Next action duy nhất

Implementer thực hiện correction trên, self-review exact diff, regenerate preview,
tạo correction report và chuyển `CURRENT_HANDOFF.md` sang Reviewer với handoff
kind exact `correction`. Không bắt đầu Wave 2.1.
