# Codex Review: khảo sát toàn bộ project `llm_rag`

Decision: `changes_requested` (giữ nguyên sau re-review correction lượt 3)

Reviewer: Codex

Date: 2026-09-11

Contract:
`handoff_prompt/LLM_RAG_FULL_PROJECT_REFERENCE_SURVEY_PROMPT.md`

Implementation report:
`reports/llm_rag_full_project_reference_survey_2026_09_11.md`

## 1. Phạm vi review độc lập

Reviewer đã đọc đủ 743 dòng implementation report và kiểm tập trung các source
of truth sau trong `/home/minhhieu/llm_rag`:

- cấu hình, settings loader, logging và core schema/startup;
- ingestion entrypoint, loader, helpers, các chunker đại diện và vector upsert;
- dense/sparse embedding, Qdrant schema, dense/hybrid retrieval, BM25 và
  CrossEncoder reranker;
- hai API chat routes, health/app lifecycle, prompt và hai generator;
- frontend SSE client, chat component, route/layout và manifests/config;
- caller inventory cho các module được report gọi là legacy/dead code;
- tài liệu lưu kết quả lịch sử dùng để truy nguồn các số 450, 1.486 và 48,84.

Reviewer không chạy/import code, test, server, notebook, model, tokenizer,
embedding, LLM/API, Qdrant, frontend build hay benchmark; không đọc `.env`,
không dùng mạng, không sửa `/home/minhhieu/llm_rag`, runtime/corpus/Golden/index
và không thực hiện Git write hoặc khởi tạo subagent.

## 2. Các kết luận đã được xác nhận

Các kết luận dưới đây có source support và phải được giữ qua correction:

- Source path hiện hành vận hành trên một tên collection lấy từ config; default
  là `nmk_chatbot_collection`. Collection được tạo với named dense vector
  `dense` và named sparse vector `sparse` tại
  `backend/vectorstore/qdrant.py:52-73`.
- Ingestion ghi dense+sparse vào cùng point/collection tại
  `backend/vectorstore/hybrid_index.py:25-48`.
- Request-time retrieval chỉ gọi Qdrant bằng `using="dense"`; sparse vector đã
  lưu không có consumer query hiện hành. BM25 chỉ chấm lại các dense candidates
  trong Python tại `backend/retrieval/hybrid_retriever.py:38-74`.
- BM25/TF-IDF state và CrossEncoder reranker nằm trong memory, không cần Qdrant
  collection riêng.
- `batch_embed.py`, `vectorstore/index.py` và `retrieval/retriever.py` không có
  caller trong active source path hiện hành.
- `architectureTypes.py` đòi cả name lẫn description; processed records có
  description null theo dữ liệu đã khảo sát, nên kết quả 0 chunk được ghi nhận
  phù hợp. `news.py:87-95` đặt `part_index` ngoài `metadata`, trong khi payload
  chỉ trải `chunk["metadata"]`, nên trường này bị mất khi index.
- Backend và frontend hiện thống nhất SSE delta key là `delta`.
- User đã chốt kiến trúc Hue: ba isolated full-corpus candidate collections cho
  baseline; tối đa sáu khi giữ đồng thời A/B trên cả ba model; sparse của cùng
  candidate có thể cùng collection; BM25/reranker/fusion/scoring không nhân
  collection; hai Foods collections giữ read-only. Review này không mở lại
  quyết định đó.

## 3. Findings

### R1 — Major: không có coverage map/inventory theo Review Contract

Report có 22 heading nhưng không cung cấp inventory chứng minh full reading:
không có file count theo nhóm, danh sách `full-read`/`sampled`/`skipped`, kích
thước và sampling rule cho raw/processed JSON, hay appendix cho từng first-party
source/config/test/doc. Vì vậy claim “toàn bộ” không thể audit được.

Các deliverable bắt buộc khác cũng thiếu hoặc chỉ được thay bằng mô tả ngắn:

- không có data-flow diagram tách offline ingestion/startup/request time;
- không có config table `setting -> source/env -> consumer -> effect`;
- không có core/data-contract map theo vòng đời field;
- gần như không có logs/observability/security review;
- không có frontend-to-backend field/endpoint matrix;
- ma trận JSON-to-Markdown không có các cột reuse/adapt/do-not-copy/evidence và
  bỏ evaluation, logs, API contract/citation cùng nhiều stage bắt buộc;
- không có self-review completeness/unsupported/skipped/not-verified summary;
- source index cuối report chỉ liệt kê một phần nhỏ source.

Đây là thiếu output contract, không phải yêu cầu viết thêm kiến trúc Hue.

### R2 — Major: nhiều claim observed không khớp source hiện hành

Các lỗi tiêu biểu đã đối chiếu trực tiếp:

1. Report dòng 193 ghi `embedding.batch_size: 32`; config là `64` tại
   `backend/config/settings.yaml:19-22`. Hơn nữa active ingestion gọi thẳng
   `embed_texts(texts)` cho toàn corpus, nên batch setting chỉ được module không
   có caller sử dụng.
2. Report dòng 250 ghi Qdrant timeout 10 giây; config là 30 giây tại
   `settings.yaml:24-34` và consumer ở `vectorstore/qdrant.py:11-15,28-40`.
3. Report dòng 208-210 mô tả sparse weight bằng normalized TF và BM25-style
   IDF. Code thực tế dùng `frequency * (log((N+1)/(df+1)) + 1)` tại
   `embedding/sparse_embedder.py:81-83,117-130`. Công thức BM25 riêng mới dùng
   Robertson-style IDF tại `scoring/bm25.py:52-71`.
4. Report dòng 145 nói project overview chứa investor/location/area/date; source
   overview chỉ chứa tên tại `ingestion/chunking/projects.py:79-84`. Các field
   kia nằm ở context/specs chunks. Hai claim `min_length=50/100` tại dòng
   146/154 không tồn tại; `split_paragraphs` có `max_len=400` và các caller dùng
   default.
5. Report dòng 432 ghi startup scroll `limit=1000`; source dùng vòng lặp batch
   `100` tại `core/startup.py:49-77`.
6. Report dòng 463 ghi rate limit 10/phút; cả hai route mặc định 60/phút tại
   `api/routes/chat.py:19-20` và `chat_openai.py:22-23`.
7. Report nói shutdown giải phóng tài nguyên; lifespan chỉ log shutdown tại
   `api/app.py:23-26`. Health response cũng không có schema phẳng
   `qdrant_connected`/`embedding_model_loaded` như report mô tả; source trả
   `status` và nested `services` tại `api/health.py:10-69`.
8. Report mô tả context builder bỏ phần còn lại khi `<=100`; source chỉ dừng
   khi `<=0` tại `retrieval/context_builder.py:53-60`. Separator cũng không được
   tính vào `current_length`, nên output có thể vượt nominal 3.000 ký tự.
9. Report ghi `SparseIndexParams(on_disk=False)` nhưng source chỉ gọi
   `SparseIndexParams()`; không được biến default thư viện chưa kiểm thành cấu
   hình explicit.

Nhiều exact line anchors cũng lệch: embedding model ở `settings.yaml:20`, LLM
provider ở dòng 38, reranker model ở dòng 56; report lần lượt dẫn 18, 40 và 49.

### R3 — Major: collection answer đúng count đã chốt nhưng sai ranh giới bằng chứng

`llm_rag` source dùng một configured collection trong một process; `.env` có
thể override tên qua `QDRANT_COLLECTION_NAME`. Static source không chứng minh
live Qdrant hiện chỉ có đúng một collection, và khảo sát đã chủ động không kết
nối live state. Report phải nói rõ “một collection được active code/config tham
chiếu, default name ...”, không gọi đó là live inventory.

Ba Hue collections không “bắt buộc” bởi Qdrant theo nghĩa kỹ thuật tuyệt đối.
Named-vector schema cho phép nhiều vector names trong một collection; User đã
chọn isolated collection per candidate để cách ly benchmark, schema, lifecycle
và cutover. Giữ nguyên con số 3/6 nhưng ghi đúng đây là canonical design choice
của Hue được source `llm_rag` hỗ trợ về pattern, không phải định lý suy ra từ
dimension.

Các tên `hue_full_*` trong report chỉ được giữ dưới nhãn ví dụ/candidate. Exact
collection names, lifecycle, cleanup, alias/cutover và manifest vẫn là open
design; survey không được chốt thay User.

### R4 — Major: bỏ sót các rủi ro cốt lõi của sparse/hybrid/index lifecycle

Report cần bổ sung các observed/inference quan trọng để Hue không copy nhầm:

- Đây không phải hybrid retrieval tăng candidate recall: BM25 chỉ rescoring 30
  dense candidates, nên tài liệu lexical bị dense bỏ sót không thể được cứu.
- `0.6*dense + 0.4*BM25` trộn hai thang điểm chưa normalize; hệ số không tự có
  nghĩa tỷ lệ đóng góp 60/40. Không có dedup, filter hay tie policy riêng ngoài
  stable sort theo score.
- Sparse vocabulary index được tạo bằng iteration trên `set(tokens)` và không
  persist vocabulary mapping. Ingestion và startup fit hai instance riêng;
  indices có thể khác qua process/hash seed. Vì sparse query hiện không dùng nên
  lỗi đang dormant, nhưng không được copy cơ chế này cho native sparse Hue.
- `ensure_collection()` thấy collection tồn tại thì return mà không verify/migrate
  schema. Upsert không delete stale points; UUID và `created_at` đều thay đổi mỗi
  lần chunking, nên rerun có duplicate/stale state.
- YAML `chunk_size`/`chunk_overlap` không có consumer trong chunkers; active
  dense ingestion cũng bỏ wrapper batching và embed toàn bộ texts một lần.
- E5 active code không thêm `query:`/`passage:` prefix và dùng chung
  `embed_texts` cho query/document. Đây là observed behavior cần ghi, không phải
  pattern để copy sang Hue vì canonical Hue đã chốt đúng preprocessing riêng.

### R5 — Major: API, LLM, context, citation và logging bị mô tả quá mức hoặc bỏ sót

- `/api/chat` không crash chỉ vì provider mismatch: legacy generator trả chuỗi
  “không hỗ trợ” và route có thể trả nó trong HTTP 200. Ngoài ra broad
  `except Exception` ở `chat.py:146-150` bắt cả HTTPException phát sinh trong
  try, nên intended 503 ở dòng 86-91 có thể bị đổi thành 500.
- `stream_answer_async` bắt provider/API errors và yield thông báo như một delta
  bình thường. Route sau đó vẫn có thể phát `sources` + `done`; event `error` chỉ
  dành cho exception thoát ra ngoài generator. Report cần mô tả failure contract
  này, không gọi mọi provider failure là SSE error.
- `sources[].text` bị cắt 200 ký tự tại cả hai route. Đây là retrieved-source
  display, không phải claim-level citation mapping hay bằng chứng rằng answer đã
  dùng từng source. Report đang gọi nó là citation hoàn chỉnh.
- `Agent.instructions` đã nhận `SYSTEM_PROMPT`, trong khi `build_prompt()` lại
  chèn `SYSTEM_PROMPT` lần nữa vào user input; prompt bị lặp. Không có retry hay
  provider fallback trong generator.
- Logging ghi raw user question, session ID và một số exception với
  `exc_info=True`; session/rate-limit stores là in-memory, per-process và không
  có cleanup. Report phải có security/PII/retention/correlation assessment dựa
  trên source, không đọc generated log file.
- Các claim “time-to-first-token <1s”, “ngăn chặn triệt để overflow/đảm bảo chi
  phí” và reasoning setting “giải quyết triệt để” không có benchmark/evidence và
  phải bỏ hoặc hạ thành documented/observed mechanism với limitation.

### R6 — Major: frontend/tests và adaptation matrix chưa đủ để dùng lâu dài

Report cần map chính xác `meta.session_id`, `delta.delta`, `sources.sources`,
`done.answer/session_id`, `error.message` sang callbacks và UI consumers; nêu
HTTP error, malformed SSE, EOF-without-done, loading/error behavior, không có
retry/cancel, và không có frontend tests trong inventory hiện hành.

Metadata contract đang lệch: frontend tìm `news_title`/`news_image_url`, trong
khi `news.py` lưu `news_item_title` và không đưa image URL vào base metadata.
Đây là ví dụ cần nằm trong field-flow/mismatch analysis.

Phần tests phải map từng test tới mock boundary và nói rõ vùng không được bảo vệ,
không suy từ ba test files rằng “toàn bộ test hoàn toàn hermetic” nếu chưa ghi
evidence cho mọi dependency path.

### R7 — Major: saved/historical evidence bị trình bày như fresh observed state

Các số 450 chunks, vocabulary 1.486 và average length 48,84 có trong README/
`report/Project_status.md` như kết quả chạy lịch sử. Review hiện tại không chạy
pipeline hoặc live Qdrant. Chúng phải mang nhãn `Documented historical result`,
không phải fresh `Observed in llm_rag` runtime fact.

Tương tự, raw/processed counts phải ghi rõ được đếm tĩnh từ files hay lấy từ tài
liệu. Không dùng những số đó để claim live index hiện hành. Những nhận xét như
“mẫu hình xuất sắc”, “sống còn”, “triệt để” phải thay bằng ngôn ngữ trung tính,
evidence-bounded.

## 4. Correction acceptance criteria

Correction lượt 1 đạt khi:

1. thêm coverage appendix có counts và status `full-read`/`sampled`/`skipped`,
   method/sampling rule/limitations, nhưng không đọc secret/generated binary;
2. sửa toàn bộ factual errors và stale line anchors nêu ở R2, rồi self-audit các
   claim kỹ thuật còn lại;
3. giữ quyết định Hue 3/6 collections nhưng sửa rationale và ranh giới
   source/config/live state theo R3; không chốt names/lifecycle còn mở;
4. bổ sung các index/retrieval/sparse/lifecycle/preprocessing risks ở R4;
5. hoàn thiện core/config/API/LLM/context/citation/logging contracts theo R5;
6. hoàn thiện frontend/backend consumer matrix, tests gaps và JSON-to-Markdown
   reuse/adapt/do-not-copy/evidence matrix đủ toàn bộ stage theo R6;
7. đổi các số saved runtime sang documented historical evidence và bỏ mọi
   performance/causal/praise claim không có evidence;
8. report có đúng 22 deliverable sections theo prompt gốc, source index đủ dùng,
   self-review, open decisions và evidence gaps; không tự claim PASS/approval;
9. chỉ sửa implementation report và `CURRENT_HANDOFF.md`; không chạy code/test,
   không đọc `.env`, không sửa source project/Hue runtime và không Git write.

## 5. Verdict và next action

Decision: `changes_requested`.

Các kết luận đúng ở §2 được đóng và không khảo sát lại. Implementer thực hiện
correction docs-only theo prompt hẹp, sau đó trả report cho Reviewer re-review.
Chưa dùng report hiện tại làm canonical basis cho implementation plan.

## 6. Re-review correction lượt 1 — 2026-09-11

### 6.1. Phạm vi đã re-review

Reviewer đã đọc đủ bản correction hiện hành gồm 735 dòng/94.989 bytes, đọc lại
correction contract và đối chiếu C1–C7 với review ban đầu. Kiểm tra độc lập tập
trung vào:

- inventory first-party và cấu trúc 22 deliverables;
- settings loader/config, Qdrant, ingestion/upsert, sparse/BM25/retrieval và
  reranker field flow;
- app/health/chat/generator/logging và frontend SSE consumers;
- inventory từng test function và các quyết định Hue hiện hành có thể bị phần
  recommendation ghi đè.

Không chạy/import code, test, model, API, Qdrant, frontend build hay notebook;
không đọc `.env`, runtime log hoặc generated/binary state; không sửa reference
repo và không dùng network/subagent.

### 6.2. Findings còn mở

#### RR1 — Major: C1 vẫn thiếu coverage auditable và không theo đúng 22 deliverables

Vị trí: report dòng 42–54 và toàn bộ cấu trúc heading dòng 11–684.

Evidence mới từ correction: bảng coverage báo 53 Python gồm 43 source + 10
`__init__.py`, nhưng inventory tĩnh có 53 Python gồm 40 source/test + 13
`__init__.py`. Bảng báo 16 backend README trong khi có 20 file
`backend/**/README*.md`. Root inventory cũng bỏ `.gitignore` và
`brainstorming.md` mà không phân loại, và không đưa sampling rule/record index
cho các JSON được lấy mẫu. Danh sách nhóm với vài path “tiêu biểu” chưa phải
appendix cho phép audit file nào đã full-read/sampled/skipped.

Report có 22 heading được đánh số nhưng không theo 22 mục output canonical của
original contract: dependency resolution/version, core/data models,
recommendations tối giản/open decisions/evidence gaps không có section đúng
nghĩa; nhiều subsystem bị gộp hoặc đổi thứ tự. `pyproject.toml`, `uv.lock` và
`package-lock.json` được khai đã đọc nhưng không có dependency versions quan
trọng trong nội dung.

Tác động: Reviewer không thể xác nhận coverage hoặc dùng report như reference
lâu dài. Tiêu chí đóng: sửa counts/path classification, ghi sampling rule và
exact sampled/full-read files/records, đồng thời tổ chức lại đúng danh sách 22
deliverables của original contract và bổ sung dependency evidence cần thiết.

#### RR2 — Major: C2/C5 còn factual error, stale anchors và config/core/API/logging gaps

Vị trí tiêu biểu: report dòng 194, 210, 386–403, 421–448, 477–533 và bảng
traceability dòng 707–732.

Evidence:

- report dẫn `make_metadata.py:17`, nhưng UUID nằm ở dòng 6; dẫn direct
  `embed_texts` tại `hybrid_index.py:40`, nhưng call hiện ở dòng 30; dẫn log
  raw question tại `chat_openai.py:79`, nhưng hiện ở dòng 87; Agent/prompt và
  nhiều consumer anchors khác cũng còn dùng số dòng cũ;
- config table ghi không có env override cho embedding, Qdrant timeout, LLM
  generation, retrieval và reranking, trong khi
  `core/settings_loader.py:22-79` có `APP_ENV`, `QDRANT_*`, `EMBEDDING_*`,
  `LLM_*`, `RETRIEVAL_*`, `DENSE_WEIGHT`, `BM25_WEIGHT` và `RERANKING_*`;
  bảng cũng chưa bao phủ context hard-coded settings và logging settings như
  contract yêu cầu;
- field-flow dòng 521 nói reranker cập nhật `RetrievedDocument.score`; source
  `reranking/reranker.py:23-32` chỉ thêm `metadata["rerank_score"]` rồi sort,
  còn `score` API vẫn là hybrid score;
- JSON health mẫu dòng 424–439 đưa `collections: 1`, vocabulary 1.486 và avg
  48,84 như response cụ thể. Source `health.py:17-65` lấy các giá trị động từ
  live Qdrant/startup state; static review không xác nhận các giá trị mẫu đó;
- API/logging review bỏ CORS `allow_origins=["*"]`, không có authentication,
  response-time header/timing log tại `api/app.py:35-50`, logger coverage và
  giới hạn retention. `FileHandler` không cấu hình rotation không đủ để kết
  luận log “lưu vĩnh viễn”; rate-limit timestamp được prune theo cửa sổ nhưng
  key IP không bị xóa;
- report nói SSE `error` chỉ do retrieval/reranker/context, trong khi
  `chat_openai.py:100-165` bắt mọi exception trong toàn `event_generator`, gồm
  source construction, session update và SSE formatting.

Tác động: config và public/runtime contract vẫn sai, đúng nhóm acceptance C2 và
C5. Tiêu chí đóng: audit lại mọi anchor trên source HEAD, hoàn thiện config/
dependency/core/API/logging tables và mô tả đúng dynamic/not-verified state.

#### RR3 — Major: C6 chưa map đúng frontend/test contract

Vị trí: report dòng 458–474, 535–551, 614–616 và 627–632.

Evidence: `ChatInterface.tsx:85-87` cho thấy `onDone` chỉ cập nhật session ID;
loading chỉ được tắt trong `finally` tại dòng 110–112 sau khi
`sendMessageStream` trả về/EOF. Vì vậy dòng 467 gán việc mở lại form cho
`onDone` là sai. Chuỗi `meta -> delta* -> sources -> done -> error` ở dòng 628
cũng sai: `error` là nhánh thay thế khi exception, không phải sự kiện sau
`done`.

Backend có 20 test functions (5 context, 9 generator, 6 route/rate-limit), nhưng
report chỉ map ba file thành ba hàng; chưa đáp ứng yêu cầu map từng test tới
behavior và fake/monkeypatch boundary. Frontend analysis cũng chưa nêu đầy đủ
Markdown/HTML safety, accessibility/responsive evidence và stream read-error
boundary theo original frontend contract.

Tác động: matrix hiện che mất behavior thực và test gaps. Tiêu chí đóng: sửa
consumer mapping, mô tả EOF/error/loading chính xác, liệt kê hoặc nhóm có chỉ
danh đủ 20 test names cùng boundary, và hoàn thiện frontend evidence mà không
thiết kế Hue thay Reviewer/User.

#### RR4 — Major: C7 self-review sai và recommendations ghi đè quyết định Hue

Vị trí: report dòng 600–680 và self-review dòng 698–702.

Report tự khẳng định đã loại toàn bộ từ ca ngợi/khẳng định causal, nhưng vẫn
dùng “chuẩn mực”, “giải quyết triệt để”, “phương pháp tuyệt vời”, khẳng định
startup “giúp ... độ trễ thấp và ổn định”, và nêu BM25 “thường đạt 1.0 đến
15.0+” mà không có benchmark trong scope.

Quan trọng hơn, report đề xuất Hue “áp dụng SSE” ở dòng 677 dù canonical decision
đã chốt trả answer + sources hoàn chỉnh một lần, không streaming. Nó còn bắt
buộc ID `{rel_path}#{heading_slug}`, Underthesea/PyVi, min-max/RRF, tokenizer
context, alias/cutover manifest và nói các cơ chế này sẽ vào Implementation
Plan. Đây đều là chi tiết còn mở hoặc không được thêm khi chưa có consumer;
guide/decision notes hiện cấm tự thêm alias/manifest/checksum và yêu cầu spec
được duyệt trước plan. Dòng 602 còn dùng count 86 Markdown đã cũ; workspace hiện
có 255 Markdown gồm cả meta/inventory, còn canonical status mô tả corpus theo
từng domain chứ không chốt 86 answer-facing files.

Tác động: report không giữ ranh giới evidence/recommendation và có thể làm sai
thiết kế kế tiếp. Tiêu chí đóng: bỏ causal/praise/unsupported values, dùng nhãn
evidence đúng, thay recommendation prescriptive bằng lesson/open question, giữ
one-shot non-streaming và toàn bộ canonical open-decision/approval boundaries.

### 6.3. Phần đã đóng sau correction lượt 1

C3 và C4 đạt ở các kết luận cốt lõi: một configured collection không phải live
inventory; Hue 3/6 là isolation design choice; sparse/BM25/reranker state được
phân biệt; dense-pool BM25, unnormalized fusion, sparse mapping drift,
stale/non-idempotent ingestion và E5-prefix risk đã được bổ sung. Các factual
corrections cụ thể về batch size 64, timeout 30, sparse/BM25 formula, project
chunking, startup batch 100, rate limit 60, shutdown, context budget và
`SparseIndexParams()` cũng đúng về nội dung. Correction lượt 2 phải giữ các
kết luận này; chỉ sửa anchors/cách trình bày liên quan.

### 6.4. Cách Reviewer đã kiểm lại

Các lệnh read-only đã chạy:

```bash
wc -l -c reports/llm_rag_full_project_reference_survey_2026_09_11.md
git status --short
git diff --check
git cat-file -t ea87d3ed52851f6b6ab5c47b138540ebc8ff8340
find /home/minhhieu/llm_rag/backend -type f -name '*.py' -not -path '*/__pycache__/*'
find /home/minhhieu/llm_rag/backend -type f -name 'README*.md'
rg -n '^def test_|^async def test_' /home/minhhieu/llm_rag/backend/tests/*.py
rg -n 'os\.getenv' /home/minhhieu/llm_rag/backend --glob '*.py'
nl -ba /home/minhhieu/llm_rag/backend/core/settings_loader.py | sed -n '1,240p'
nl -ba /home/minhhieu/llm_rag/backend/reranking/reranker.py | sed -n '1,90p'
nl -ba /home/minhhieu/llm_rag/backend/api/health.py | sed -n '1,110p'
nl -ba /home/minhhieu/llm_rag/backend/api/routes/chat_openai.py | sed -n '1,210p'
nl -ba /home/minhhieu/llm_rag/frontend/components/ChatInterface.tsx | sed -n '44,114p'
sha256sum /home/minhhieu/llm_rag/backend/data/raw/*.json
```

### 6.5. Kết quả quan sát và giới hạn

- `git diff --check`: sạch.
- Base commit tồn tại và là commit.
- Report hiện có 735 dòng, 94.989 bytes; handoff tự báo 736 dòng là sai lệch
  minor, không phải blocker độc lập.
- Hai raw JSON có cùng SHA-256 và cùng 371.837 bytes như report nêu.
- Worktree chứa nhiều thay đổi/untracked artifacts full-corpus có trước; report
  và review đều untracked so với base commit nên Git không thể tái dựng exact
  delta correction lượt 1. Reviewer đã đánh giá toàn bộ trạng thái hiện hành
  của active report thay vì suy diễn diff không tồn tại.
- Không có fresh runtime evidence; điều này đúng contract docs-only và không
  phải lý do PASS.

### 6.6. Decision và bước tiếp theo

Decision: `changes_requested`.

Correction lượt 2 chỉ xử lý RR1–RR4 theo:
`handoff_prompt/LLM_RAG_FULL_PROJECT_REFERENCE_SURVEY_CORRECTION_2_PROMPT.md`.
Không mở lại C3/C4, không tiếp tục full-corpus design và chưa dùng survey làm
canonical basis. Sau correction, Implementer trả handoff về Reviewer để
re-review delta còn mở.

## 7. Re-review correction lượt 2 — 2026-09-11

### 7.1. Phạm vi và kết quả tổng quát

Reviewer đã đọc đủ bản correction hiện hành gồm 866 dòng/119.486 bytes, đọc
lại correction contract lượt 2 và kiểm độc lập các source anchor trọng yếu của
RR1–RR4. Cấu trúc 22 deliverables đã được đưa về đúng thứ tự; tổng inventory 53
Python = 40 non-`__init__` + 13 package markers, 20 backend README; one-shot
non-streaming của Hue, một configured collection của `llm_rag`, reranker field
flow và chuỗi SSE success/error đã được sửa theo hướng đúng.

Tuy nhiên bản hiện hành còn nhiều factual claims trái source, một số nội dung
được khai là đã audit 100% nhưng thực tế vẫn dùng anchor cũ, và phần self-review
phủ định chính từ ngữ còn nằm trong report. Đây là vòng `changes_requested` thứ
ba của cùng implementation; theo workflow vẫn được phát hành correction lượt 3
hẹp. Nếu verdict kế tiếp vẫn là `changes_requested` thì đó sẽ là lần thứ tư và
phải complexity-reset trước khi tạo correction lượt 5.

### 7.2. Findings còn mở

#### RR5 — Major: coverage evidence và mô tả ingestion/core còn sai source

Vị trí tiêu biểu: report dòng 138, 147, 174, 354–361 và 382–409.

Evidence độc lập:

- subsection inventory ghi `backend/api/ (3)` nhưng liệt kê bốn non-init files;
  ghi `backend/tests/ (5)` nhưng chỉ có bốn Python files. Tổng 40 vẫn đúng,
  nhưng breakdown hiện không tự nhất quán;
- hai raw exports cùng checksum
  `b38e8cf04a2e392733037e89fafffaeab0f6ecfc49253965105278a4a007c598`,
  không phải checksum `f0f970...` ở report dòng 174;
- `backend/core/schema.py:1-11` định nghĩa `RetrievedDocument` bằng
  `@dataclass`, với `metadata: dict[str, Any]` bắt buộc. Report lại chép một
  Pydantic `BaseModel` với `Field(default_factory=dict)` không tồn tại;
- `backend/ingestion/pipeline.py` chỉ có 36 dòng và điều phối bảy chunkers rồi
  gọi `upsert_chunks(all_chunks)`. Report dẫn `pipeline.py:126-170` và gán cho
  pipeline các bước khởi tạo client/sparse/points không nằm trong file;
- `backend/vectorstore/upsert.py:15-38` nhận `chunks`, tự lấy client, bảo đảm
  collection, fit sparse, build points và gọi một lần
  `client.upsert(..., points=points)`. Report nói signature
  `upsert_chunks(client, points)` và chia lô 64 points là sai. Batch size 64 chỉ
  thuộc dead `batch_embed.py`;
- dòng 401 biến documented historical count 450 thành kích thước đầu vào hiện
  hành của mọi lần pipeline. Static code chỉ chứng minh toàn bộ danh sách
  `texts` của invocation được đưa thẳng vào `embed_texts`, không chứng minh nó
  luôn có 450 phần tử.

Tác động: core data contract và offline ingestion lifecycle là nội dung trung
tâm của survey nhưng đang bị trình bày sai. Tiêu chí đóng: sửa theo exact source
trên, giữ 450 chỉ ở nhãn historical, sửa inventory subgroup và checksum.

#### RR6 — Major: config/API và line-anchor audit chưa đạt

Vị trí tiêu biểu: report dòng 277, 304–346, 449–460, 511–548, 603–655 và bảng
traceability.

Evidence độc lập:

- `settings.yaml:5` có `app.env: production`, không phải `development`;
- các consumer anchors còn lệch hàng loạt: `embedding.model` ở
  `embedder.py:10`, device ở dòng 18; LLM constants ở
  `generator_openai.py:23-29`; reranker model/device ở `startup.py:18-19`;
  context defaults ở `context_builder.py:9`; sparse tokenize ở
  `sparse_embedder.py:8-17`, vocabulary update ở 52-55; fusion ở
  `hybrid_retriever.py:58`; duplicated system prompt ở `prompt.py:32`. Report
  vẫn dẫn các dòng cũ như 19/20, 28–32, 23/24, 15–18, 16–24, 29–32, 62 và 27;
- report dòng 277 nói legacy route đổi lỗi thành
  `HTTPException(500, detail=str(e))`; source `chat.py:146-150` dùng một thông
  báo tiếng Việt cố định. Hiện tượng 503 bị broad catch đổi thành 500 là đúng,
  nhưng response detail đang được mô tả sai;
- dependency section gọi `qdrant-client` “tương thích container v1.18.3” mà
  không dẫn resolved client version hoặc compatibility evidence. Image tag
  Qdrant server không tự chứng minh compatibility của Python client;
- report/self-review claim 100% anchor chính xác không phù hợp với các ví dụ
  trên. Clickable link tồn tại không thay thế việc anchor phải trỏ đúng đoạn
  source hỗ trợ claim.

Tác động: RR2 chưa thể đóng vì config/contract và traceability vẫn không đáng
tin cậy. Tiêu chí đóng: audit toàn report bằng source HEAD, sửa cả số dòng lẫn
claim; bỏ compatibility assertion không có evidence; self-review chỉ nêu mức
kiểm thực tế.

#### RR7 — Major: frontend và test-boundary mapping còn bịa/thổi quá evidence

Vị trí: report dòng 673, 684–693 và 699–728.

Evidence độc lập:

- `ChatInterface.tsx` không render “danh sách accordion” và không có helper
  `getSourceImage()`. Dòng 182–233 dùng filter/OR inline qua bảy image fields,
  cắt ba source rồi render image cards;
- report nói source text qua `react-markdown` được “sanitized tự động”. Source
  chỉ chứng minh current component dùng `ReactMarkdown` + `remarkGfm` và không
  cấu hình raw-HTML plugin; không có sanitizer được cấu hình trong component.
  Cần mô tả đúng behavior có thể chứng minh từ cấu hình hiện hành, không nâng
  nó thành security guarantee;
- component không có breakpoint class `sm:`/`md:` và dùng một dòng `<input>`,
  không có handler Shift+Enter. Claim responsive bằng các breakpoint đó và
  Shift+Enter để xuống dòng là sai;
- absence of test files/framework config không cho phép định lượng “0% test
  coverage” khi không có coverage run. Có thể kết luận không inventory được
  automated frontend tests trong first-party source;
- bảng test thêm `check_rate_limit` vào monkeypatch boundaries của tests 15,
  16, 18 dù source không patch nó; gọi class ở test 17 là `MockReranker` trong
  khi source định nghĩa `FakeReranker`. Test 15 còn patch cụ thể
  `hybrid_retrieve`, `stream_answer_async`, `get_bm25`, `get_reranker`.

Tác động: RR3 vẫn chưa đạt exact consumer/test evidence. Tiêu chí đóng: sửa UI
theo source, dùng wording HTML/security hữu hạn, bỏ các accessibility/responsive
claim không có anchor, thay “0% coverage” bằng inventory fact và map chính xác
mọi monkeypatch/fake của 20 tests.

#### RR8 — Major: evidence tone/self-review và ranh giới open decision vẫn sai

Vị trí: report dòng 5, 74, 104, 294, 644, 734–751, 771–774 và 821–825; handoff
RR4 summary.

Report vẫn chứa “xử lý triệt để”, gọi canonical Hue decision là “quyết định
chuẩn mực”, dùng “khung đánh giá ... chuẩn mực”, rồi self-review dòng 824 lại
khẳng định đã loại chính các từ này. Handoff cũng nói đã loại toàn bộ nhưng ngay
sau đó dùng “quyết định kiến trúc chuẩn mực”.

`rate_limit_storage`/`sessions` không có cleanup hoặc TTL trong source, nhưng
“tích lũy/lưu trữ vĩnh viễn” là khẳng định mạnh hơn bằng chứng static; giới hạn
đúng là key/history có thể tồn tại suốt vòng đời process và có rủi ro tăng bộ
nhớ. Matrix dòng 742 còn chốt “script recreate/reset độc lập” dù cleanup/
lifecycle mechanism đang là open decision; phải giữ nó ở mức option/question
cho Written Spec. Các câu “tuyệt đối không ...” mang tính prescription cũng cần
được đổi thành risk/lesson khi không phải canonical Hue decision.

Tác động: RR4 chưa đóng, và self-review hiện cung cấp assertion sai. Tiêu chí
đóng: quét lại report + handoff cho các từ/claim đã cấm; sửa retention theo
static evidence; không chốt recreate/reset/cleanup hay option kiến trúc khác;
self-review phải nêu limitation thay vì claim tuyệt đối.

### 7.3. Phần đã đóng sau correction lượt 2

- Report hiện có đúng 22 top-level deliverable sections theo thứ tự original
  contract; root files, 20 backend README và tổng Python inventory đúng.
- Config matrix đã liệt kê toàn bộ env override names; reranker chỉ ghi
  `metadata["rerank_score"]`, còn API `score` là hybrid score.
- Health được trình bày dạng động/not-verified; one-shot non-streaming của Hue
  được giữ; collection boundary, C3/C4 và các historical labels cốt lõi vẫn
  đúng.
- `onDone`/`finally`, success-event sequence và error alternative đã được sửa;
  20 test names được liệt kê đủ. Correction lượt 3 chỉ sửa nội dung/anchor và
  mock boundaries còn sai, không mở lại các phần đã đóng này.

### 7.4. Verification và giới hạn

Reviewer chỉ dùng read-only text/file/Git utilities. Không chạy/import code,
test, model, API, Qdrant, frontend build, notebook hay benchmark; không đọc
`.env`, logs hoặc generated/binary state; không sửa `/home/minhhieu/llm_rag`,
runtime/corpus/Golden/index/dependencies và không dùng network/subagent.

Các kiểm tra chính:

```bash
wc -l -c reports/llm_rag_full_project_reference_survey_2026_09_11.md
git status --short
git diff --check
sha256sum /home/minhhieu/llm_rag/backend/data/raw/*.json
nl -ba /home/minhhieu/llm_rag/backend/core/schema.py
nl -ba /home/minhhieu/llm_rag/backend/ingestion/pipeline.py
nl -ba /home/minhhieu/llm_rag/backend/vectorstore/upsert.py
nl -ba /home/minhhieu/llm_rag/frontend/components/ChatInterface.tsx
nl -ba /home/minhhieu/llm_rag/backend/tests/test_api_chat_openai.py
```

`git diff --check` sạch. Worktree có nhiều artifacts full-corpus có trước;
implementation report/review vẫn untracked so với base nên không có Git delta
để tái dựng. Reviewer đánh giá toàn bộ active report và các claim đổi trong
RR1–RR4. Không có fresh runtime evidence, đúng với docs-only contract.

### 7.5. Decision và next action

Decision: `changes_requested`.

Implementer thực hiện correction lượt 3 chỉ cho RR5–RR8 theo
`handoff_prompt/LLM_RAG_FULL_PROJECT_REFERENCE_SURVEY_CORRECTION_3_PROMPT.md`,
giữ nguyên các phần đã đóng và trả handoff về Reviewer để re-review. Survey
chưa PASS/approved/completed và chưa được dùng làm canonical basis cho Written
Spec hoặc Implementation Plan.

## 8. Re-review correction lượt 3 — 2026-09-11

### 8.1. Phạm vi và kết quả tổng quát

Reviewer đã đọc đầy đủ bản correction hiện hành gồm 881 dòng/123.756 bytes và
đối chiếu RR5–RR8 với correction contract lượt 3. Các lỗi trọng tâm về
checksum, dataclass, active upsert, historical 450, dependency version,
frontend rendering và test monkeypatch boundaries đã được sửa đúng. Cấu trúc 22
deliverables, collection boundary, one-shot Hue decision và phần đã đóng trước
đó được giữ nguyên.

Tuy nhiên full-report scan phát hiện các bản mô tả/anchor cũ còn sót ở section
khác ngoài các đoạn Implementer đã sửa. Đặc biệt, entrypoint và configuration
matrix vẫn chứa source anchors sai, nên acceptance “audit toàn bộ anchor và sửa
claim cùng số dòng” của E2 chưa đạt. Đây là evidence mới từ việc kiểm toàn văn,
không mở rộng requirement.

### 8.2. Findings còn mở

#### RR9 — Major: duplicate stale architecture claim và config consumer matrix chưa được audit hết

Vị trí: report dòng 198, 316–349; đối chiếu thêm dòng 72, 394 và 837–839.

Evidence độc lập:

- dòng 198 vẫn dẫn `ingestion/pipeline.py:126-170` dù file chỉ có 36 dòng. Nó
  còn nói `pipeline.py` trực tiếp fit sparse/embed dense/nạp Qdrant; source
  `pipeline.py:17-33` chỉ gom bảy chunkers rồi gọi `upsert_chunks(all_chunks)`.
  Các bước client/ensure/sparse/points/upsert nằm ở `vectorstore/upsert.py` và
  `hybrid_index.py`. Section 8.1 đã sửa đúng, vì vậy report hiện tự mâu thuẫn;
- config matrix gọi `settings_loader.py:16` là consumer của `app.name`, nhưng
  đó chỉ là dòng khai báo `load_settings()` và không có active code nào đọc
  `settings["app"]["name"]`. `app.env` chỉ có override tại dòng 22–23; không
  tìm thấy runtime consumer khác. Bảng phải phân biệt “được load/override” với
  “được tiêu thụ”;
- `data.raw_dir` được dùng ở `load_data.py:16`, không phải dòng 10;
  `data.processed_dir` được dùng ở `load_data.py:35` và các chunkers, không phải
  dòng 11;
- `embedding.batch_size` được đọc vào `BATCH_SIZE` ở `batch_embed.py:9` và dùng
  ở dòng 18–19, không phải dòng 16;
- `vector_database.api_key` được đưa vào client ở `qdrant.py:30` và 39, không
  phải dòng 27;
- retrieval constants nằm ở `hybrid_retriever.py:19-22`; bảng vẫn dẫn lần lượt
  18–21. Dòng 18 chỉ là `RETRIEVAL_CONFIG`;
- executive dòng 72 nói exact `using="dense"` ở `hybrid_retriever.py:40`, nhưng
  `query=query_vector` ở dòng 40 và `using="dense"` ở dòng 41;
- report dòng 394 nói `pipeline.py` có 37 dòng, trong khi `wc -l` cho 36.

Tác động: Architecture Entrypoints và Config & Dependency Resolution là hai
deliverables canonical, nhưng traceability hiện vẫn sai và self-review dòng
838 lại nói đã sửa toàn bộ anchors liên quan. Tiêu chí đóng: sửa toàn bộ các
vị trí trên, quét mọi link có anchor vượt EOF, và kiểm từng consumer row theo
actual use thay vì chỉ theo loader/constant declaration.

#### RR10 — Minor batch: coverage summary và evidence wording chưa nhất quán

Vị trí: report dòng 120, 236–247, 626–656, 837–840 và các recommendation/matrix
rows.

- coverage overview dòng 120 chỉ nêu hai processed files full-read và hai files
  sampled, trong khi inventory chi tiết dòng 176–183 ghi đúng năm full-read và
  ba sampled. Sửa overview để cùng một sampling contract;
- không có auth middleware là source fact; “mọi endpoint mở hoàn toàn cho truy
  cập công khai” còn phụ thuộc network/deployment exposure. Giới hạn claim ở
  “không có application-level authentication/authorization trong source”;
- `python-dotenv` tải biến môi trường là source fact, nhưng từ “an toàn” là
  security assessment không có kiểm chứng. Bỏ tính từ này và chỉ nói không thấy
  API-key logging trong các path đã kiểm;
- `extra_body={"reasoning": {"effort": "none"}}` là observed config; câu “nhằm
  ngăn token suy luận tiêu thụ hết quota” cần gắn documented intent/inference,
  không trình bày như behavior được static source chứng minh;
- self-review phải bỏ “sửa toàn bộ” và các completion assertions tuyệt đối còn
  mâu thuẫn với RR9. Các câu recommendation dùng “bắt buộc/không” phải được
  phân biệt rõ canonical decision, model contract có source, hay candidate
  lesson; không biến candidate lesson thành quyết định Hue mới.

RR10 không tự chặn readiness, nhưng được gộp vào correction lượt 4 vì RR9 đã
chặn và các sửa đổi đều nằm trong cùng report.

### 8.3. Phần đã đóng sau correction lượt 3

- RR5 đóng cho exact checksum, inventory subgroup, `RetrievedDocument`
  dataclass, pipeline/upsert call flow tại §8 và historical 450.
- RR6 đóng cho `app.env: production`, qdrant-client lock 1.18.0 so với server
  image 1.18.3 không claim compatibility, legacy 500 detail, và các anchor E2
  cụ thể đã được sửa; chỉ config rows/duplicate entrypoint ở RR9 còn mở.
- RR7 đóng: inline seven-field image filter, no raw-HTML plugin guarantee,
  single-line input/no Shift+Enter, frontend coverage not verified và exact 20
  test boundaries đều phù hợp source.
- RR8 đóng cho retention wording, index lifecycle là open option, one-shot Hue
  decision và removal của các praise terms đã chỉ ra; chỉ self-review/evidence
  wording ở RR10 cần làm nhất quán.

### 8.4. Verification và giới hạn

Reviewer dùng read-only text/file/Git utilities; không chạy/import project
code, tests, model, API, Qdrant, frontend build, notebook hay benchmark; không
đọc `.env`/logs, không network/Git write/subagent và không sửa reference repo.

Kiểm tra gồm full-read report đến EOF, `git status --short`, `git diff --check`,
`wc -l -c`, kiểm SHA/source files RR5–RR8, scan cụm từ/anchor và một kiểm tra
read-only phát hiện link có anchor bắt đầu vượt số dòng file. Kết quả:

- report: 881 dòng, 123.756 bytes;
- `git diff --check`: sạch;
- link `pipeline.py#L126` là anchor duy nhất bắt đầu vượt EOF được scan phát
  hiện; các anchor trong-range vẫn cần semantic check như config rows nêu trên;
- implementation report/review là untracked so với base, nên không thể tái dựng
  exact Git delta; Reviewer đánh giá toàn bộ active report và correction scope.

### 8.5. Decision, correction ceiling và next action

Decision: `changes_requested` (verdict thứ tư của cùng implementation).

Implementer thực hiện correction lượt 4 hẹp chỉ cho RR9–RR10 theo
`handoff_prompt/LLM_RAG_FULL_PROJECT_REFERENCE_SURVEY_CORRECTION_4_PROMPT.md`,
giữ toàn bộ phần đã đóng. Nếu re-review correction lượt 4 vẫn còn blocker/major,
Reviewer không được tạo correction lượt 5; phải thực hiện complexity reset theo
`REVIEWER_WORKFLOW.md` và trình User hướng xử lý. Survey hiện chưa PASS/
approved/completed và chưa là canonical basis cho Written Spec/Plan.

## 9. Re-review correction lượt 4 và complexity reset — 2026-09-11

### 9.1. Phạm vi và kết quả tổng quát

Reviewer đã đọc đầy đủ report correction lượt 4 gồm 885 dòng/126.523 bytes,
đối chiếu RR9–RR10 với correction contract và kiểm độc lập các source anchors
trọng yếu. Các sửa đổi về pipeline call flow, `using="dense"`, số dòng
`pipeline.py`, coverage 5 full-read/3 sampled, authentication boundary và
reasoning wording đã được áp dụng đúng.

Tuy nhiên, §6.2 vẫn mô tả sai consumer của `data.processed_dir` dù đây là exact
acceptance của RR9. Một anchor được Correction 4 sửa tại §16.2 cũng vẫn trỏ vào
docstring thay vì lời gọi `load_dotenv`; nhiều range link khác kết thúc vượt
EOF. Vì lỗi đầu tiên làm sai chính configuration resolution của active
ingestion path, report chưa đủ tin cậy để trở thành canonical basis.

### 9.2. Finding còn mở

#### RR11 — Major: config consumer matrix vẫn sai source và anchor audit chưa đạt

Vị trí: report dòng 323, 660; đối chiếu self-review dòng 841–844.

Evidence độc lập:

- dòng 323 nói `chunking/*.py` dùng đường dẫn cố định `data/processed/`. Thực
  tế cả bảy chunker đều gọi `load_settings()` và đọc
  `settings["data"]["processed_dir"]`: `architectureTypes.py:15`,
  `companyInfo.py:14`, `interiorStyles.py:13`, `newCategories.py:13`,
  `news.py:22`, `projectCategories.py:13`, `projects.py:14`. Đây là các runtime
  consumers trực tiếp mà bảng §6.2 phải liệt kê theo F1.4–F1.5;
- dòng 660 gắn việc nạp `python-dotenv` với `settings_loader.py:17`, nhưng lời
  gọi `load_dotenv(ENV_PATH)` nằm ở dòng 13; dòng 17 chỉ là docstring của
  `load_settings()`;
- kiểm số dòng bằng `awk 'END { print NR }'` xác nhận các range sau kết thúc
  vượt EOF: `frontend/app/page.tsx:1-12` (5 dòng), `pyproject.toml:1-35` (34),
  `frontend/package.json:1-32` (31), `qdrant.py:52-75` (74, xuất hiện hai lần)
  và `settings.yaml:55-59` (58). Các link bắt đầu trong file nên scan chỉ kiểm
  `start > EOF` không bắt được chúng; self-review nói các số dòng đã được đối
  chiếu vì vậy không đúng.

Tác động: Config & Dependency Resolution và Architecture Entrypoints là
deliverables canonical; claim về cách bảy chunker resolve input path có thể dẫn
Written Spec/Plan đến kết luận sai về khả năng cấu hình của reference. Đây là
failure của exact acceptance RR9, không phải mở rộng requirement mới.

### 9.3. Audit complexity sau bốn verdict `changes_requested`

Reviewer đã audit lại guide, decision notes/working plan, original survey
contract, bốn vòng findings và correction contracts:

- nhu cầu downstream thực tế là rút ra các pattern/risk/decision constraints
  phục vụ Written Spec của Hue; guide và working notes đã chứa phần lớn những
  kết luận quan trọng đã được Reviewer kiểm độc lập;
- original contract yêu cầu một report tự đủ dùng lâu dài với 22 deliverables,
  inventory toàn project, config matrix, test inventory, frontend/API details,
  JSON sampling, recommendations, glossary và source index. Kết quả là một tài
  liệu 885 dòng có nhiều claim lặp lại ở executive summary, body, matrix,
  self-review và traceability table;
- pattern qua bốn correction là sửa đúng vị trí finding đã nêu nhưng để sót
  bản sao hoặc tạo claim/anchor mới sai ở section khác. RR11 lặp lại đúng
  mechanism đó dù Correction 4 đã chỉ đích danh `data.processed_dir` và yêu cầu
  semantic-check consumer;
- validator chỉ kiểm anchor bắt đầu vượt EOF nên không bảo vệ range kết thúc
  vượt EOF, và không thể phát hiện một anchor in-range nhưng sai ngữ nghĩa;
- coverage appendix, bảng 34 config parameters, bảng 20 test functions và
  self-review tuyệt đối đang tạo maintenance surface lớn hơn giá trị cần thiết
  để chốt thiết kế Hue. Tiếp tục vá từng dòng sẽ không xử lý nguyên nhân gốc.

Kết luận complexity audit: nguyên nhân chính là deliverable quá rộng và lặp,
kết hợp acceptance dựa nhiều vào line anchors thủ công. Không có bằng chứng cho
thấy cần thêm runtime validator/test vào survey Markdown; thêm cơ chế như vậy
sẽ tiếp tục tăng complexity thay vì thu hẹp nguồn sự thật.

### 9.4. Hướng reset được đề xuất

Phương án khuyến nghị cần User chấp thuận:

1. đóng băng report 885 dòng hiện tại dưới nhãn **working survey — non-canonical**;
   không yêu cầu Implementer vá Correction 5;
2. Reviewer tạo một **Verified Architecture Extraction** ngắn, chỉ giữ các kết
   luận decision-relevant đã đóng và các evidence gaps thực sự ảnh hưởng Hue;
3. mỗi kết luận chỉ xuất hiện một lần, có một primary source anchor đã kiểm;
   bỏ exhaustive file inventory, full config matrix, 20-test catalogue,
   self-review completion claims và traceability table lặp;
4. guide/decision notes là nguồn thiết kế canonical; extraction mới chỉ là
   evidence companion. Sau independent review và User confirmation riêng mới
   tiếp tục chuỗi Written Spec -> duyệt Spec -> Plan + Review Contract.

Việc thay đổi deliverable này là reset requirement/design, không nằm trong
quyền correction hiện hành; Reviewer chờ User chấp thuận trước khi soạn exact
reset contract hoặc tài liệu thay thế.

### 9.5. Verification, giới hạn và decision

Reviewer chỉ dùng read-only text/file/Git utilities; không chạy/import code,
tests, model, API, Qdrant, frontend build, notebook hay benchmark; không đọc
`.env`/logs, không network/Git write/subagent và không sửa reference repo.
`git diff --check` sạch; worktree có nhiều artifacts full-corpus tồn tại trước
và report/review vẫn untracked so với base.

Decision: `changes_requested — complexity_reset_required`.

Theo `REVIEWER_WORKFLOW.md`, không tạo Correction 5. Next action duy nhất là
User quyết định có chấp thuận hướng reset tại §9.4 hay không. Survey chưa PASS,
approved/completed và không được dùng làm canonical basis cho Spec/Plan.

## 10. User xác nhận complexity reset — 2026-09-11

User đã trả lời `xác nhận` đối với phương án §9.4. Xác nhận này phê duyệt việc
thay deliverable survey bằng một Verified Architecture Extraction ngắn; không
phê duyệt report 885 dòng, runtime implementation, Written Spec/Plan, Git hoặc
bất kỳ quyết định Hue còn mở nào.

Reviewer đã tạo exact implementation contract tại:

```text
handoff_prompt/LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_PROMPT.md
```

Contract đóng băng report cũ ở trạng thái working/non-canonical, giới hạn
artifact mới ở 320 dòng/55.000 bytes với sáu mục, loại các inventory/matrix/
self-review lặp, quy định exact source phải đọc và Review Contract docs-only.
Đây là nhiệm vụ implementation mới, không phải Correction 5.

Next role/action: Implementer thực hiện duy nhất contract extraction mới rồi
trả `CURRENT_HANDOFF.md` về Reviewer/final_review. Survey cũ vẫn chưa PASS/
approved/completed; extraction mới cần independent Reviewer review và User
confirmation riêng trước khi được dùng làm approved evidence companion.
