# Implementer — correction lượt 1 khảo sát toàn bộ project `llm_rag`

Bạn là **Implementer** tại `/home/minhhieu/hue_rag`.

Sửa đúng các findings trong:

```text
reports/llm_rag_full_project_reference_survey_codex_review_2026_09_11.md
```

Report cần sửa:

```text
reports/llm_rag_full_project_reference_survey_2026_09_11.md
```

Đây là correction Markdown/read-only hẹp. Không khảo sát lại từ đầu, không mở
lại kết luận đã được Reviewer xác nhận và không tự đổi quyết định canonical Hue.

## 1. Bootstrap bắt buộc

Đọc đầy đủ theo thứ tự; nếu output bị cắt, đọc tiếp tới EOF:

1. `session_prompt/Session_Prompt.md`
2. `session_prompt/Project_Status.md`
3. `session_prompt/IMPLEMENTER_WORKFLOW.md`
4. `session_prompt/CURRENT_HANDOFF.md`
5. `skills/risk-gated-agent-review/SKILL.md`
6. `skills/practical-project-coding/SKILL.md`
7. `handoff_prompt/LLM_RAG_FULL_PROJECT_REFERENCE_SURVEY_PROMPT.md`
8. `reports/llm_rag_full_project_reference_survey_codex_review_2026_09_11.md`
9. `reports/llm_rag_full_project_reference_survey_2026_09_11.md`

Chỉ đọc lại đúng source/docs/config/data samples cần cho C1–C7. Không mở `.env`,
generated logs, binary Qdrant state, vendor/cache hoặc raw `rag_old_0`.

## 2. Phần đã đạt — giữ nguyên, không khảo sát lại

- Active source path dùng một configured Qdrant collection, default
  `nmk_chatbot_collection`, với named dense `dense` và sparse `sparse` cùng
  points.
- Runtime Qdrant retrieval chỉ query `using="dense"`; sparse named vector hiện
  không có query consumer.
- BM25 chỉ rescoring dense candidates trong memory; CrossEncoder cũng in-memory;
  không thành phần nào cần collection riêng.
- `batch_embed.py`, `vectorstore/index.py`, `retrieval/retriever.py` không có
  active caller hiện hành.
- Architecture Types 0 chunk theo code + processed data đã khảo sát;
  `news.part_index` bị rơi khỏi Qdrant payload.
- Backend/frontend thống nhất SSE delta key `delta`.
- Quyết định Hue đã chốt: ba isolated full-corpus baseline collections, tối đa
  sáu khi giữ đồng thời A/B cho ba model; sparse của candidate có thể cùng
  collection; BM25/reranker/fusion/scoring không nhân collection; hai Foods
  collections giữ read-only.

Không chuyển các phần đã đạt thành claim live-Qdrant mới và không chạy lại để
“xác nhận”.

## 3. Correction bắt buộc

### C1 — Coverage map, method và output structure

- Bổ sung file count theo nhóm và coverage appendix auditable:
  `full-read`, `inventory + sampled`, `skipped/excluded`, lý do và giới hạn.
- Với raw/processed JSON: ghi path/count/size/role, schema keys/nesting/optional
  fields từ representative records, sampling rule và file nào thực sự full-read.
- Inventory lock/generated/vector/log state nhưng không mở binary/live state.
- Thêm data-flow diagram ngắn tách ba đường: offline ingestion, startup và
  request-time frontend/API.
- Sắp report theo đúng 22 deliverable sections của prompt gốc. Có source index,
  glossary, self-review completeness/unsupported claims/skips/not-verified.
- Không claim “đã đọc toàn bộ” nếu appendix không chứng minh đủ first-party
  backend/frontend/source/config/test/doc.

### C2 — Sửa factual errors và exact anchors

Sửa tối thiểu toàn bộ lỗi Reviewer đã chỉ ra:

- `embedding.batch_size` default là 64; active ingestion không dùng wrapper
  batching.
- Qdrant timeout default là 30.
- Sparse encode là `frequency * (log((N+1)/(df+1)) + 1)`; không dùng normalized
  TF hay BM25 IDF. Tách rõ công thức BM25 trong `scoring/bm25.py`.
- Project overview chỉ có tên; context/specs giữ các field khác.
  `split_paragraphs` dùng `max_len=400`; không có `min_length=50/100`.
- Startup scroll theo batch 100 trong loop; rate-limit mặc định 60/phút.
- Lifespan shutdown chỉ log, không release resource. Health trả nested
  `status/services`, không phải schema phẳng report cũ mô tả.
- Context truncation dừng khi remaining `<=0`, không phải `<=100`; separator
  không được cộng vào budget.
- Source chỉ gọi `SparseIndexParams()`; không ghi `on_disk=False` như explicit
  config nếu không có evidence version-specific.
- Sửa mọi stale file:line, gồm model/provider/reranker config anchors. Tự rà tất
  cả anchors còn lại, không chỉ các ví dụ trên.

### C3 — Collection/index answer và ranh giới bằng chứng

- Trả lời đúng: active code/config tham chiếu **một configured collection**,
  default `nmk_chatbot_collection`; tên có thể bị override bởi
  `QDRANT_COLLECTION_NAME`. Không suy ra live Qdrant chỉ chứa một collection.
- Giữ nguyên Hue 3 baseline/6 A-B vì User đã chọn isolated-per-candidate. Nêu rõ
  đây là design choice để cách ly benchmark/schema/lifecycle/cutover, không phải
  giới hạn kỹ thuật tuyệt đối rằng Qdrant không thể chứa nhiều named vectors.
- Tách persisted Qdrant state, startup in-memory lexical state và stateless
  scoring/reranking trong bảng inventory.
- Collection names trong report chỉ là ví dụ; exact naming, schema chi tiết,
  recreate/update/delete, aliases/manifest/cutover/cleanup còn open.

### C4 — Retrieval, sparse, scoring và ingestion lifecycle

Bổ sung bằng nhãn evidence đúng:

- BM25 chỉ rescoring dense candidate pool, không tăng lexical recall ngoài pool.
- Dense cosine và raw BM25 được weighted-sum mà không normalize/calibrate; không
  diễn giải `0.6/0.4` thành tỷ lệ đóng góp bảo đảm.
- Candidate depth 30, final retrieval top 10, rerank top 5; dedup/filter/tie và
  failure behavior thực tế.
- Sparse vocabulary indices xây từ `set(tokens)`, mapping không persist; fit
  riêng ở ingestion/startup có nguy cơ index mismatch qua process nếu sau này
  dùng Qdrant sparse query. Ghi đây là inference/dormant risk, không nói lỗi active.
- Existing collection không được schema verify/migrate; upsert không delete
  stale points; UUID và `created_at` làm rerun không idempotent.
- `chunk_size`/`chunk_overlap` YAML không có active chunker consumer;
  `batch_size` chỉ có consumer trong dead wrapper.
- E5 code không thêm `query:`/`passage:` prefix và dùng chung embed function cho
  query/document. Không copy behavior này sang Hue vì Hue đã có model-specific
  preprocessing contract.

### C5 — Core/config/API/LLM/context/citation/logging

- Thêm config table: setting/default/env override/consumer/effect/required;
  bao phủ data/chunking/embedding/vectorstore/retrieval/reranking/context/LLM,
  rate/query limits, logs và frontend API URL. Chỉ ghi env names.
- Thêm field-flow table: JSON source -> chunk text/metadata -> Qdrant payload ->
  `RetrievedDocument` -> rerank metadata -> context -> API source -> frontend.
- Mô tả `/api/chat` chính xác: provider mismatch trả error text từ generator;
  broad exception có thể đổi intended HTTPException trong try thành 500.
- Mô tả streaming errors chính xác: generator thường yield provider error như
  normal delta rồi route có thể gửi sources/done; SSE `error` chỉ khi exception
  thoát khỏi generator/route stream block.
- Ghi `sources[].text` bị cắt 200 chars và chỉ là retrieved-source display,
  không phải claim-level citations/groundedness proof.
- Ghi system prompt bị lặp qua `Agent.instructions` và `build_prompt`; retry và
  provider fallback không có trong active OpenRouter path.
- Thêm logs/observability: logger names, console/file sinks, levels, timing,
  session identifiers; raw question/session/exception được log; in-memory
  sessions/rate limits per-process, không cleanup. Đánh giá secret/PII/context
  exposure chỉ từ source, không đọc log file.
- Bỏ/hạ mọi claim latency, cost, “triệt để”, causal effectiveness không có test
  hay benchmark trong scope.

### C6 — Frontend, tests và JSON-to-Markdown matrix

- Tạo bảng exact consumer:
  `meta.session_id`, `delta.delta`, `sources.sources`,
  `done.answer/session_id`, `error.message` -> API callback -> UI state/render.
- Nêu HTTP error parsing, malformed SSE behavior, EOF không có `done`, loading/
  error state, không có retry/cancel và không có frontend tests nếu inventory xác
  nhận như vậy.
- Ghi metadata mismatch: frontend đọc `news_title`/`news_image_url`, nhưng news
  chunker dùng `news_item_title` và không persist image URL trong base metadata.
- Map từng backend test tới behavior và mock/fake boundary; nêu meaningful gaps,
  không gọi toàn bộ suite hermetic vượt evidence.
- Viết lại ma trận đúng cột:
  `Thành phần | Observed llm_rag | Reuse idea | Adapt for Hue Markdown |
  Do not copy | Evidence`.
- Matrix phải bao phủ discovery, chunking, source locator/metadata, embedding
  input, payload, lifecycle, dense/sparse/BM25/hybrid, scoring/fusion,
  reranking, context, citation, API, logs, evaluation và frontend.

### C7 — Evidence labels, historical numbers và tone

- Các số 450 chunks, vocabulary 1.486 và avg document length 48,84 là saved/
  documented historical results từ README/Project_status, không phải fresh
  runtime observation của correction này. Gắn exact source và limitation.
- Với record/file counts, ghi rõ static count hay documented count. Không gọi
  persisted local Qdrant state là current live fact.
- Mỗi claim quan trọng phải mang đúng ranh giới `Observed`, `Documented intent`,
  `Documented historical result`, `Inference`, `Candidate lesson`, hoặc
  `Not verified`.
- Dùng giọng trung tính; bỏ “xuất sắc”, “sống còn”, “triệt để” và mọi claim hiệu
  quả/latency/reproducibility không có evidence.

## 4. Quyền và output

Chỉ được sửa:

1. `reports/llm_rag_full_project_reference_survey_2026_09_11.md`
2. `session_prompt/CURRENT_HANDOFF.md`

Không tạo report/review/prompt khác. Không sửa review này, prompt correction,
guide, specs, decision/context notes, Project Status, Hue runtime/tests/corpus/
Golden/index/dependencies hoặc bất kỳ file nào trong `/home/minhhieu/llm_rag`.

Không chạy/import Python/Node/project code, server, test, notebook, model,
tokenizer, embedding, LLM/API, Qdrant, browser, build hay benchmark. Không đọc
`.env`/secret, không dùng network/web search, không Git write và không spawn
subagent. Chỉ dùng read-only text/file/Git utilities đã cho phép trong prompt gốc.

## 5. Self-review và bàn giao

Trước khi bàn giao:

- đối chiếu từng C1–C7 và ghi mapping trong `CURRENT_HANDOFF.md`;
- kiểm đủ 22 sections, anchors, coverage counts/status và evidence labels;
- liệt kê exact files changed, read-only methods, skipped/not-verified và phần
  đã giữ nguyên;
- không tự claim PASS, approval, closure hoặc giao runtime implementation.

Cập nhật `CURRENT_HANDOFF.md` thành:

```text
Target role: reviewer
Authored by: implementer
Handoff kind: final_review
State: active
Base commit: ea87d3ed52851f6b6ab5c47b138540ebc8ff8340
Head commit: worktree
Risk level: low
Git authorization: none
Sub-agent authorization: none
```

Next action duy nhất: Reviewer re-review correction C1–C7.
