# Implementer — correction lượt 2 khảo sát toàn bộ project `llm_rag`

Bạn là **Implementer** tại `/home/minhhieu/hue_rag`.

Sửa đúng các finding RR1–RR4 trong §6 của:

```text
reports/llm_rag_full_project_reference_survey_codex_review_2026_09_11.md
```

Report đích:

```text
reports/llm_rag_full_project_reference_survey_2026_09_11.md
```

Đây là correction Markdown/read-only hẹp. Không khảo sát lại toàn project,
không mở lại C3/C4 đã đóng và không tự thay quyết định canonical Hue.

## 1. Bootstrap và mức đọc

Đọc theo đúng thứ tự và mức sau; file `full-read` bị cắt phải đọc tiếp tới EOF:

1. `full-read` — `session_prompt/Session_Prompt.md`.
2. `targeted-read` — `session_prompt/Project_Status.md`: `Project overview`,
   `Current runtime and data`, `Thiết kế full-corpus hiện hành`, `Decisions
   currently in force`, `Safety and authorization boundaries`, và đoạn survey
   `llm_rag` trong `Workstream và roadmap`.
3. `full-read` — `session_prompt/IMPLEMENTER_WORKFLOW.md`.
4. `full-read` — `skills/risk-gated-agent-review/SKILL.md`.
5. `full-read` — `skills/practical-project-coding/SKILL.md`.
6. `full-read` — `session_prompt/CURRENT_HANDOFF.md`.
7. `full-read` — prompt correction này.
8. `full-read` — Codex review nêu trên; tập trung §6, dùng §§2–4 để giữ phần đã
   đóng và truy nguyên acceptance.
9. `full-read` — report đích hiện hành.
10. `targeted-read` — `guides/full_corpus_rag.md`: `Quyết định đã chốt`, `Nội
    dung chưa chốt`, `Chuỗi tài liệu và điểm duyệt`.
11. `targeted-read` —
    `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md`: `Trả
    đáp án và nguồn`, `Qdrant collection strategy`, `Thứ tự quyết định sau khi
    survey đóng`.

Original survey prompt là `reference-only`: chỉ mở §§4–8 khi cần kiểm exact 22
deliverables. Source `/home/minhhieu/llm_rag` là `reference-only`; chỉ đọc lại
exact anchors/config/tests cần sửa RR1–RR4. Không mở `.env`, logs, generated/
binary state, raw `rag_old_0`, notebooks hoặc toàn bộ source tree lần nữa.

## 2. Phần phải giữ đóng

- Một configured collection mặc định `nmk_chatbot_collection`, override bằng
  `QDRANT_COLLECTION_NAME`; static source không chứng minh live inventory.
- Dense+sparse cùng point/collection; runtime chỉ query named dense; BM25 chỉ
  rescore dense pool; reranker/fusion/scoring in-memory.
- Hue giữ 3 isolated baseline/6 A-B collections; đây là User design choice,
  không phải giới hạn Qdrant. Foods targets read-only.
- Batch 64, timeout 30, sparse formula raw-count × smoothed IDF, BM25 formula
  riêng, project overview/context/specs, `split_paragraphs(max_len=400)`, startup
  scroll batch 100, rate 60, shutdown chỉ log, nested health, context dừng
  `remaining <= 0` và không tính separator, `SparseIndexParams()` không đối số.
- Sparse mapping drift là dormant inference; existing schema/stale/random UUID
  ingestion và E5 prefix là risks không copy.

## 3. Correction bắt buộc

### D1 — Coverage và đúng 22 deliverables

- Sửa inventory thành 53 Python = 40 non-`__init__` source/tests + 13
  `__init__.py`; 20 backend `README*.md`. Inventory đầy đủ root first-party
  files, gồm `.gitignore` và `brainstorming.md`, hoặc phân loại exact reason nếu
  excluded/reference-only.
- Coverage appendix phải auditable: exact path hoặc glob + danh sách đầy đủ cho
  mỗi group, status từng group/file, full-read/sampled/skipped reason. Với JSON,
  ghi file nào full-read; file nào sampled; exact sampling rule và record/table
  indices/selection; counts/sizes là static hay documented.
- Sắp report theo đúng nội dung và thứ tự 22 deliverables tại §5 original survey
  contract, không chỉ tạo 22 số heading. Có riêng config/dependencies,
  core/data models, recommendations tối giản + open decisions + evidence gaps,
  source index/glossary/self-review.
- Bổ sung dependency versions trực tiếp quan trọng từ manifests/locks và exact
  source. Không cần inventory vendor/generated dependency files.

### D2 — Facts, anchors, config/core/API/logging

- Audit toàn bộ clickable anchors theo source HEAD hiện hành. Tối thiểu sửa:
  UUID ở `make_metadata.py:6`; direct embed ở `hybrid_index.py:30`; raw question
  log ở `chat_openai.py:87`; Agent construction ở
  `generator_openai.py:59-67`; reranker mutation ở `reranker.py:23-32`.
- Config table phải ghi đúng default/source/env override/consumer/effect/
  required cho app/data/chunking/embedding/vectorstore/retrieval/reranking/
  context/LLM, query/rate, logs và frontend URL. Đối chiếu toàn bộ env names ở
  `core/settings_loader.py:22-79`; chỉ ghi tên, không đọc values/secrets. Ghi rõ
  context budget hard-coded nếu không từ config.
- Field flow phải nêu reranker chỉ thêm `metadata["rerank_score"]` và sort;
  không ghi đè `RetrievedDocument.score`, nên API source `score` vẫn là hybrid
  score.
- Health schema dùng placeholder/dynamic description; không trình 1.486/48,84/
  collection count như fresh response. Nếu nhắc số lịch sử, gắn
  `[Documented historical result]` ngay tại chỗ và nêu live value not verified.
- Bổ sung/đính chính API: không authentication trong source; wildcard CORS;
  request/response/error objects; `X-Response-Time` và timing log; logger names,
  sinks/levels/session IDs. FileHandler không rotation chỉ chứng minh config
  không có rotation, không chứng minh retention “vĩnh viễn”. Rate-limit prune
  timestamps cũ nhưng không xóa IP keys; sessions không TTL/cleanup.
- SSE `error` có thể đến từ bất kỳ exception thoát trong toàn
  `event_generator`, không chỉ retrieval/reranker/context.

### D3 — Frontend, tests và matrix

- Sửa exact consumer: `onDone` chỉ cập nhật `session_id`; `isLoading` được tắt
  trong `finally` sau khi stream function return/EOF. `error` là alternative
  event path, không đứng sau `done` trong một chuỗi thành công.
- Mô tả HTTP error, malformed SSE, EOF-without-done và reader exception đúng
  source; phân biệt callback error với outer catch/finally.
- Map đủ 20 backend test functions (có thể nhóm hàng khi cùng contract nhưng
  phải liệt kê exact test names), behavior và mock/fake/monkeypatch boundary.
  Không thêm gap suy đoán không gắn user behavior như Unicode multibyte.
- Hoàn thiện frontend evidence về framework/routes, component/state, Markdown/
  HTML handling, sources UI, accessibility/responsive và absence of tests.
- Matrix JSON→Markdown giữ đúng sáu cột/stages nhưng không biến candidate lesson
  thành thiết kế Hue đã duyệt.

### D4 — Evidence tone và canonical Hue boundaries

- Xóa hoặc hạ mọi praise/causal/unsupported claim, gồm “chuẩn mực”, “phương pháp
  tuyệt vời”, “giải quyết triệt để”, startup bảo đảm latency thấp/ổn định và
  khoảng BM25 1–15 chưa đo. Self-review chỉ claim điều thực sự audit được.
- Không dùng health example hay ingestion prose để biến 450/1.486/48,84 thành
  current runtime fact; đây chỉ là documented historical results.
- Bỏ count “86 Markdown”. Nếu cần mô tả Hue, dùng canonical five-domain curated
  corpus mà không tự tạo count mới từ meta/inventory.
- Giữ quyết định Hue trả answer + sources hoàn chỉnh một lần, **không streaming**.
  SSE chỉ là observed reference/lesson cần đổi, không là recommendation cho Hue.
- Không bắt buộc trước quyết định: exact deterministic ID formula,
  Underthesea/PyVi cho lexical retrieval, min-max/RRF, generator tokenizer,
  alias/cutover manifest hoặc cleanup framework. Nêu chúng là option/open
  question khi có căn cứ. Không thêm alias/manifest/checksum/migration trước
  consumer/risk và không nói chi tiết sẽ vào plan trước written spec approval.
- Recommendations phải tối giản, evidence-bounded và tách rõ `Observed`,
  `Documented historical result`, `Inference`, `Candidate lesson`, `Not
  verified`, `Canonical Hue decision` khi dùng.

## 4. Quyền, verification và output

Chỉ được sửa:

1. `reports/llm_rag_full_project_reference_survey_2026_09_11.md`;
2. `session_prompt/CURRENT_HANDOFF.md`.

Không sửa Codex review, correction prompt, guide/spec/notes/status, runtime,
tests, corpus, Golden, index, dependencies hoặc `/home/minhhieu/llm_rag`.
Không chạy/import Python/Node/project code, test, model, API, Qdrant, notebook,
browser, build hay benchmark; không network, đọc `.env`/logs, Git write hoặc
spawn subagent. Chỉ dùng read-only text/file/Git utilities.

Trước bàn giao: kiểm 22 sections theo canonical list, inventory/counts/sampling,
all anchors/env overrides, 20 test names, banned/causal language, Hue decisions,
`git diff --check` và `wc -l -c`. Không tự claim PASS/approval/closure.

Cập nhật `CURRENT_HANDOFF.md` về `reviewer`/`final_review`, giữ base commit,
`Head commit: worktree`, risk low, Git/subagent none. Next action duy nhất:
Reviewer re-review correction lượt 2 RR1–RR4.
