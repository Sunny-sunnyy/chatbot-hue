# Implementer — khảo sát toàn bộ project `llm_rag` làm reference cho Hue RAG

Bạn là **Implementer** tại `/home/minhhieu/hue_rag`.

Đây là task khảo sát source/docs **read-only** do User trực tiếp yêu cầu. Mục
tiêu là tạo một report canonical, chi tiết và có source anchors về toàn bộ kiến
trúc `llm_rag`, để Reviewer/User dùng làm reference khi hoàn thiện full-corpus
Hue RAG mà không phải khảo sát lại project từ đầu.

`llm_rag` dùng dữ liệu JSON tiếng Việt; Hue RAG dùng curated Markdown tiếng
Việt. Report phải phân biệt rõ behavior quan sát được trong `llm_rag`, phần có
thể học lại, phần bị khóa vào JSON và adaptation cần thiết cho Markdown. Không
coi reference project là requirement tự động của Hue và không sửa quyết định
canonical Hue.

## 1. Bootstrap bắt buộc

Đọc đầy đủ theo thứ tự; nếu output bị cắt, tiếp tục đúng phần thiếu tới EOF:

1. `session_prompt/Session_Prompt.md`
2. `session_prompt/Project_Status.md`
3. `session_prompt/IMPLEMENTER_WORKFLOW.md`
4. `session_prompt/CURRENT_HANDOFF.md`
5. `skills/risk-gated-agent-review/SKILL.md`
6. `skills/practical-project-coding/SKILL.md`
7. prompt này
8. `guides/full_corpus_rag.md`
9. `guides/llm_rag_reference_for_hue_rag.md`
10. snapshot đầu file và §§62–73 của
    `handoff_prompt/FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md`

Các working notes ngày 2026-09-09 không phải written spec/implementation plan
đã approved. Survey chỉ cung cấp evidence; Implementer không tự thay thiết kế,
không tự approve và không giao implementation runtime.

## 2. Reference bắt buộc và thứ tự đối chiếu

Đọc toàn văn hai tài liệu do User chỉ định:

1. `/home/minhhieu/llm_rag/tai_lieu/rag_agent_handoff_current_repo.md`
2. `/home/minhhieu/llm_rag/tai_lieu/rag_system_pipeline_deep_dive.md`

Sau đó khảo sát source of truth tại:

```text
/home/minhhieu/llm_rag
/home/minhhieu/llm_rag/backend
/home/minhhieu/llm_rag/frontend
```

Tài liệu giải thích intent và lịch sử; source/config hiện hành cho biết project
thực tế đang làm gì. Khi docs mâu thuẫn source, báo cả hai với exact anchors và
coi source hiện hành là observed behavior; không âm thầm hòa giải hoặc sửa file.

Ghi read-only snapshot của reference nếu Git cho phép: `HEAD` SHA, branch và
dirty/untracked summary. Snapshot dùng giới hạn hiệu lực report, không phải
approval và không được thực hiện Git write.

## 3. Coverage bắt buộc

### 3.1 Inventory toàn project

Dùng `rg --files` và read-only Git/file inspection để lập inventory toàn
`/home/minhhieu/llm_rag`. Phân loại từng nhóm thành:

- đọc toàn văn;
- inventory + schema/sample có chủ đích;
- generated/vendor/binary/secret bị loại, kèm lý do.

Report phải cho biết file count theo nhóm và một coverage appendix đủ để phiên
sau biết phần nào thật sự đã đọc. Không claim “toàn bộ” nếu còn first-party
source/config chưa đọc. File dài hoặc tool output bị cắt phải đọc tiếp.

### 3.2 Phần phải đọc toàn văn

Đọc mọi first-party source/config/test/doc cần để hiểu project, tối thiểu:

- toàn bộ `backend/`, gồm API routes/schemas, config/settings, core, ingestion,
  chunking, embedding, LLM, logs, reranking, retrieval, scoring, vectorstore,
  startup/lifecycle, utilities và tests;
- toàn bộ first-party `frontend/` source: routes/pages, components, hooks,
  state/data fetching, API client/types, styling/config và tests;
- root/project READMEs, architecture docs, Docker/compose/deployment files,
  Python/Node dependency manifests, example config và scripts first-party;
- mọi file first-party khác được import hoặc gọi từ backend/frontend dù nằm
  ngoài hai thư mục.

Lock files có thể rất dài: inventory và đọc phần metadata/resolution cần cho
dependency claims; không cần chép hoặc kể lại toàn bộ transitive packages.

### 3.3 JSON data và generated state

Với corpus/data JSON của `llm_rag`:

- inventory toàn bộ path, count, size và vai trò;
- đọc schema thực tế qua loader/models và kiểm representative records đủ để mô
  tả keys, nesting, optional fields, IDs, source metadata và text units;
- nếu file nhỏ/first-party config thì đọc toàn văn;
- không fact-check toàn bộ nội dung nghiệp vụ hoặc chép data dài vào report;
- ghi rõ file nào chỉ inventory/sample, sampling rule và giới hạn.

Inventory vector/database/index artifacts nhưng không mở binary database, không
kết nối live service và không gọi chúng là current live state.

### 3.4 Phần bắt buộc loại

- `.env`, `.env.*` có secrets, credentials, tokens và secret values;
- `.venv`, `node_modules`, vendor code, caches, build/dist output, model weights,
  binary databases/vector indexes và generated runtime logs dung lượng lớn;
- `.git` internals ngoài read-only status/SHA/diff metadata cần cho snapshot.

Được đọc `.env.example` hoặc sample config không chứa secret để lấy **tên biến
môi trường và default công khai**. Không in, grep, log hay suy secret value.

## 4. Các câu hỏi report phải trả lời

### 4.1 Bản đồ kiến trúc và entrypoints

Vẽ data flow hiện hành bằng text/Mermaid ngắn cho cả hai đường:

```text
JSON source -> load/normalize -> chunk -> embedding/index -> stored state
frontend/API request -> retrieval -> scoring/fusion -> rerank -> context
-> LLM -> response/citation/log -> frontend
```

Chỉ rõ entrypoint, module/function/class chính, input/output và side effects.
Phân biệt startup, offline ingestion và request-time path. Nêu synchronous/
asynchronous boundaries, shared state, singleton/cache/lifecycle nếu source có.

### 4.2 API

Phân tích toàn bộ public/internal API có liên quan:

- framework, app factory/startup/shutdown;
- endpoints, HTTP methods, request/response schemas và status/error behavior;
- authentication/CORS/rate limit/streaming nếu thực sự có;
- dependency wiring và đường gọi từ route tới core RAG;
- contract mà frontend thực sự consume;
- citation/source/debug fields được trả hay bị ẩn.

Mỗi claim quan trọng phải có exact path + line. Không đề xuất endpoint mới trong
phần observed behavior.

### 4.3 Config và dependency resolution

Lập bảng cấu hình gồm setting name, source (default/env/config), consumer,
effect và required/optional. Bao phủ model/provider, embedding dimensions,
batching, chunk size/overlap/token limits, retrieval depth, sparse/hybrid,
reranking, scoring weights, context/generation limits, vectorstore path/URL,
collection names, logs và frontend base URL.

Chỉ ghi tên environment variables; không đọc giá trị secret. Nêu dependency
versions trực tiếp quan trọng từ manifests/locks và nơi source dựa vào behavior
version-specific.

### 4.4 Core và data models

Giải thích responsibility và data contracts của các core models/services:

- document/source record;
- chunk/metadata/payload;
- query/retrieval candidate/scored result;
- context/citation/source response;
- API request/response và error objects.

Chỉ rõ field nào bắt nguồn từ JSON, field nào derived, field nào persist, field
nào chỉ tồn tại request-time. Tìm nơi metadata có thể bị mất hoặc đổi tên giữa
loader, chunker, vectorstore, retrieval, reranker, context và API.

### 4.5 Ingestion và chunking

Truy nguyên exact ingestion path:

- discovery và include/exclude rules;
- JSON schema/loading/normalization;
- chunk boundary algorithm, size/overlap/unit/tokenizer;
- deterministic IDs hoặc source IDs;
- embedding input construction và preprocessing;
- batching, upsert/recreate/update/delete behavior;
- validation, partial failure, retry/resume và completion signal nếu có;
- startup stale-index/source-change detection nếu có.

Nêu behavior nào phụ thuộc JSON và cần thay bằng Markdown structure/source
locators trong Hue. Không chạy ingestion và không dùng output cũ làm fresh
evidence.

### 4.6 Embedding

Với từng dense/sparse embedder:

- exact model/provider, dimensions, prefix/tokenization/preprocessing;
- query/document methods, batching/device/cache và normalization;
- sync/async interface, failure behavior và configuration;
- nơi vector được lưu và tên vector/schema tương ứng;
- consumer thật trong ingestion/retrieval.

Phân biệt model được config nhưng không dùng với path đang hoạt động. Không load
tokenizer/model hoặc gọi provider.

### 4.7 Vectorstore, collection và index inventory

Đây là câu hỏi trọng tâm. Lập bảng cho từng persisted/in-memory retrieval state:

- Qdrant/vector DB collection/index name hoặc naming rule;
- dense vector names/dimensions/distance;
- sparse named vectors hoặc sparse index;
- payload schema/filter/index;
- create/recreate/upsert/delete/alias/cutover lifecycle;
- producer và consumers;
- state có thể cùng collection hay bắt buộc tách;
- source evidence và phần chỉ là recommendation.

Trả lời trực tiếp:

1. `llm_rag` thực tế dùng bao nhiêu collection/index theo source/config, không
   suy từ live service;
2. một embedding candidate có cần collection riêng không và vì sao;
3. sparse embedder/hybrid index có nằm cùng dense points hay cần collection riêng;
4. BM25/TF-IDF persist ở đâu, có phải Qdrant collection không;
5. reranker, fusion và scoring có cần collection riêng không;
6. collection count tối thiểu cho Hue baseline ba dense candidates;
7. count khi so representation A/B trên cả ba candidates;
8. lựa chọn nào chỉ phục vụ benchmark và trạng thái nào cần giữ sau winner.

Đối chiếu quyết định Hue hiện hành: dự kiến ba baseline full-corpus collections,
có thể tối đa sáu cho A/B; active Foods và dense-only Foods candidate read-only.
Không tự xác nhận con số Hue nếu evidence `llm_rag` cho thấy schema/lifecycle cần
quyết định mới; nêu trade-off cho Reviewer/User.

### 4.8 Retrieval, sparse/BM25, hybrid, fusion và scoring

Tách rõ từng stage và không dùng “hybrid” như một hộp đen:

- query preprocessing/expansion;
- dense retrieval;
- sparse embedding retrieval;
- BM25 và TF-IDF nếu có;
- candidate depth, dedup và filters;
- score scale/normalization/rescoring;
- fusion algorithm/weights/tie handling;
- final top-k trước và sau rerank;
- fallbacks và failure behavior.

Với mỗi profile/configuration, đưa một bảng exact path qua các stage, state cần
thiết và output contract. Chỉ ra thuật toán/config có code nhưng không có caller.

### 4.9 Reranking

Xác định model/provider, pair construction, max length/truncation, batching,
device, score semantics, ordering/ties, input/output, error/fallback và caller.
Trả lời rõ reranker stateless hay persist state, và vì sao nó có/không cần một
collection riêng.

### 4.10 LLM, context và citations

Phân tích provider/model, prompts, system/user messages, context packing, token/
character budgets, generation settings, structured output/streaming, citation
mapping và groundedness policy thực tế. Chỉ rõ context là raw JSON fields,
rendered text hay object structure và frontend nhận gì.

Nêu retry/fallback/error handling quan sát được, nhưng không coi fallback giả là
PASS evidence. Không gọi API hoặc đánh giá chất lượng model.

### 4.11 Logs và observability

Liệt kê logger/config/sinks/levels/correlation IDs/timing/metrics và nội dung
được log ở ingestion/request path. Kiểm khả năng log secret, raw prompt/context,
PII hoặc provider payload từ source. Phân biệt application logs với generated
log files bị loại khỏi reading scope.

### 4.12 Frontend

Đọc toàn bộ first-party frontend và mô tả:

- framework/build/run entrypoint và routes/pages;
- component hierarchy liên quan chatbot;
- state management và API client/data flow;
- loading, empty, error, retry và streaming/non-streaming UX;
- answer rendering, Markdown/HTML safety và citations/sources UI;
- config/environment fields, types và backend contract coupling;
- tests và accessibility/responsive behavior quan sát được.

Tạo bảng `frontend behavior -> backend field/endpoint -> exact consumers`. Nêu
phần có thể tham khảo cho Hue và phần cần đổi theo answer+sources contract hiện
hành; không thiết kế frontend Hue thay Reviewer/User trong survey.

### 4.13 Tests và evidence hiện có

Đọc tests first-party nhưng không chạy. Map test tới behavior/contract nó bảo vệ,
dependency thật hay mock/fake/stub, và giới hạn. Inventory reports/artifacts
liên quan nhưng không gọi saved output là fresh result. Nêu vùng quan trọng
không có test/evidence mà không biến thành generic checklist.

### 4.14 So sánh `llm_rag` JSON với Hue Markdown

Lập reuse/adaptation matrix tối thiểu gồm:

| Thành phần | Observed `llm_rag` | Có thể reuse ý tưởng | Phải đổi cho Hue Markdown | Không nên copy | Evidence |
|---|---|---|---|---|---|

Bắt buộc bao phủ discovery, chunking, source metadata/locator, embedding input,
payload, ingestion lifecycle, dense/sparse/BM25/hybrid, reranking, context,
citations, API, logs, evaluation và frontend. Giữ ranh giới Hue:

```text
curated Markdown -> structure-aware chunks -> embeddings/index
-> retrieval/rerank -> bounded context -> grounded answer + sources
```

Không đề xuất chunk JSON trực tiếp cho Hue, không mất exact Markdown evidence,
không biến web/reference data thành Hue ground truth và không khôi phục
abstraction chỉ vì project cũ có.

## 5. Output duy nhất

Tạo đúng một report:

```text
reports/llm_rag_full_project_reference_survey_2026_09_11.md
```

Report phải tự đủ để dùng lâu dài và có các mục:

1. executive summary cho User;
2. reference snapshot, method và giới hạn;
3. coverage map/inventory với full-read/sampled/skipped status;
4. kiến trúc tổng thể và entrypoints;
5. API;
6. config/dependencies;
7. core/data models;
8. ingestion;
9. chunking;
10. embedding;
11. vectorstore/collections/index lifecycle;
12. retrieval/sparse/BM25/hybrid;
13. scoring/fusion;
14. reranking;
15. LLM/context/citations;
16. logs/observability/error handling;
17. frontend;
18. tests và evidence hiện có;
19. JSON-to-Markdown reuse/adaptation matrix;
20. direct answer về collection count cho Hue;
21. recommendations tối giản, open decisions và evidence gaps;
22. source index/glossary để phiên sau tra cứu nhanh.

Mỗi technical claim quan trọng có exact absolute hoặc repo-relative path + line;
frontend symbol/component và config cũng phải có anchors. Không chép dài source
hoặc docs. Phân biệt bằng nhãn rõ:

- `Observed in llm_rag`;
- `Documented intent`;
- `Inference`;
- `Candidate lesson for Hue`;
- `Not verified`.

Recommendations phải dựa trên consumer thật, giữ data flow dễ theo dõi và nêu
phần không nên copy. Không tạo implementation plan trá hình hoặc đổi canonical
Hue decisions.

## 6. Quyền và giới hạn

- Chỉ đọc `/home/minhhieu/llm_rag` và các canonical inputs nêu trên.
- Chỉ được tạo/sửa report duy nhất và cập nhật
  `session_prompt/CURRENT_HANDOFF.md` để trả task về Reviewer.
- Không sửa bất kỳ file nào trong `/home/minhhieu/llm_rag`.
- Không sửa guide, design notes, prompt này, Project Status, runtime, tests,
  corpus, Golden, dependencies, index hay artifacts của Hue.
- Không chạy/import project code, Python/Node scripts, servers, tests, notebook,
  model, tokenizer, embedding, LLM/API, Qdrant, browser, build hoặc benchmark.
- Không đọc `.env` hay secret; không network/download/web search.
- Được dùng read-only text/file/Git utilities như `rg`, `sed`, `wc`, `jq`,
  `git status`, `git rev-parse`, `git diff` để inventory và đọc source.
- Không commit, push, checkout, reset hoặc Git write.
- Không spawn subagent.
- Giữ nguyên mọi dirty/untracked changes có trước và không nhận chúng là output.

Nếu một file bắt buộc thiếu/không đọc được, source tree quá lớn vì generated
content chưa được loại, hoặc docs/source mâu thuẫn làm thay đổi kết luận kiến
trúc, ghi exact blocker/evidence vào report; không đoán và không mở rộng quyền.

## 7. Review Contract

Risk: `low` — broad read-only reference survey, chỉ tạo Markdown report/handoff.

Implementer phải cung cấp:

- inventory chứng minh full reading của first-party backend/frontend/source;
- reference SHA/dirty boundary;
- exact anchors cho data flows, config, models và collection claims;
- observed-vs-documented contradictions;
- direct collection/index answer và JSON-to-Markdown adaptation matrix;
- mọi skipped/sampled/not verified item;
- self-review report về completeness, unsupported claims và scope.

Reviewer sẽ kiểm độc lập tối thiểu:

1. report và coverage map có bao phủ toàn bộ first-party backend/frontend không;
2. chọn các entrypoint/call flow chính để đối chiếu source;
3. API/config/core/data contracts và frontend consumers có khớp code không;
4. ingestion/chunking/embedding/vectorstore/retrieval/scoring/reranking/LLM/logs
   có được tách đúng responsibility và không bỏ stage quan trọng không;
5. collection count phân biệt Qdrant, lexical state và stateless components;
6. reuse/adaptation matrix không copy JSON assumptions sang Markdown;
7. report có giữ observed/inference/recommendation/evidence gap riêng và tuân
   thủ mọi safety boundary không.

Không có requirement chạy test/code/model/API. Reviewer không mặc định đọc lại
toàn bộ `llm_rag`; independent review dựa trên coverage inventory, exact anchors
và focused source checks. Nếu report thiếu coverage hoặc claim quan trọng không
có anchor, task nhận correction thay vì coi self-report là approval.

## 8. Handoff khi hoàn tất

Cập nhật `session_prompt/CURRENT_HANDOFF.md` thành:

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

Handoff dẫn tới prompt này và report, tóm tắt coverage, exact files changed,
read-only commands/method, key collection answer, contradictions, skipped/not
verified và exact checks Reviewer cần làm lại. Không tự viết Codex review/user
report, không claim PASS/approval/closure và không tự tiếp tục full-corpus design.
