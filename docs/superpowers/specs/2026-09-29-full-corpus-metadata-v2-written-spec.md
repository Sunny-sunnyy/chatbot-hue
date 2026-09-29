# Full-corpus Metadata Contract v2 — Written Spec Amendment

```text
Status: approved by User 2026-09-29 +07
Date: 2026-09-29 +07
Design direction: approved by User 2026-09-29 +07
Implementation Plan + Review Contract: approved for Gate 1 by User 2026-09-29 +07
Live Qdrant write/cutover authorization: none
Base commit: 92f2e2cce0e85c9b4f733aaab038bc99cad314c0
Owner: Codex Reviewer
Risk: high
```

## 1. Mục tiêu và ranh giới quyền

Amendment này định nghĩa metadata contract v2 cho toàn bộ Full-corpus Hue RAG,
không chỉ riêng Phase 6. Mục tiêu là bổ sung định danh chunk và taxonomy tối
thiểu có consumer thật, làm rõ freshness/build lineage, đồng thời giữ nguyên
evidence provenance và các ranh giới public đã duyệt.

“Toàn bộ” ở đây bao phủ canonical Full-corpus path end-to-end: chunking,
ingestion, bốn candidate collections, retrieval, evaluation dependency và
Phase 6 consumer. Foods MVP pipeline/collections có trước Full-corpus là legacy
artifacts riêng, tiếp tục read-only và không bị migrate bởi amendment này.

Đây là Written Spec đã được User duyệt. Approval của riêng artifact này không
tự cấp implementation authority. Implementation Plan và embedded Review
Contract sau đó đã được User duyệt cho riêng Gate 1/Tasks 1–4: exact code/tests,
local corpus reads và read-only preflight bốn legacy collections. Gate 1 không
cho phép Qdrant create/upsert, build-record v2 write, runtime cutover,
embedding, benchmark, paid API/model hoặc Phase 6 implementation.

Live Qdrant writes và runtime cutover vẫn là Gate 2 và Gate 3 riêng trong
approved Plan, mỗi gate cần User approval mới.

## 2. Kết luận audit

Metadata hiện hành không sai về nền tảng. Năm field `search_text`, `source`,
`title`, `heading_path`, `evidence_parts` đang tạo một contract nhỏ, nhất quán
và giữ exact evidence provenance. Build records hiện hành cũng đã đặt source
hashes, corpus/model/sparse identity đúng ở cấp build thay vì lặp trên từng
point.

Hai thiếu hụt có consumer trực tiếp:

1. Qdrant payload không giữ original logical `chunk_id`, nên retrieval hiện
   chỉ trả point UUID và làm tracing/evaluation lệch với chunk contract ở các
   pipeline khác.
2. Product domain chỉ được suy ngầm từ `source`, nên không có một field đã
   validate để retrieval diagnostics hoặc future approved filter experiment
   sử dụng.

Một thiếu hụt vận hành độc lập với số field payload: startup có build record
chứa đủ source hashes nhưng chưa so sánh chúng với corpus hiện tại. Điều này có
thể cho phép phục vụ collection stale và làm `evidence_parts.start/end` không
còn tương ứng với source đang có trên filesystem.

Không có evidence để thêm `subdomain`, generic document type/tags, source URL,
timestamps, per-point source/content hashes, token count, model/build IDs trên
từng point hoặc một permanent document registry.

## 3. Metadata ownership theo layer

Metadata không phải một object duy nhất được sao chép qua mọi layer.

| Layer | Canonical responsibility |
|---|---|
| Curated document/chunk | logical chunk identity, domain, source locator, title/heading và exact evidence parts |
| Qdrant point | retrieval representation cùng phần metadata tối thiểu cần để validate và dựng retrieval result |
| Build/collection record | corpus/source hashes, dense model/revision/dimension, sparse state, schema versions và vector-copy lineage |
| Runtime retrieval | rank/score/stage timings, logical chunk identity, domain và private evidence metadata |
| Public citation/API | response-local citation ID, title, heading path và exact excerpts |
| Evaluation | canonical Golden schema và category metric đã duyệt; không kế thừa tự động Qdrant metadata |

Field thuộc build không được lặp trên 8.460 points. Field nội bộ không được tự
động xuất hiện trong public response hoặc Golden.

## 4. Canonical chunk identity và domain

### 4.1 `chunk_id`

Contract hiện hành được giữ nguyên:

```text
chunk_id = <canonical relative POSIX source path>#<zero-based chunk ordinal>
point_id = uuid.uuid5(uuid.NAMESPACE_URL, f"hue-rag:{chunk_id}")
```

`chunk_id` là logical identity dễ đọc và deterministic khi source path cùng
chunking output không đổi. Nó không phải permanent entity ID: rename/move file,
edit làm thay đổi chunk boundaries hoặc đổi chunking algorithm có thể làm ID
đổi. Amendment không thêm document registry, random ID hoặc content-addressed
ID để che đặc tính này.

Mỗi point phải thỏa đồng thời:

- `payload.chunk_id` là string không rỗng và đúng `source#ordinal` của chunk;
- ordinal là integer không âm;
- top-level Qdrant point ID bằng UUID5 được tính lại từ `payload.chunk_id`;
- `chunk_id` và point ID đều unique trong full corpus.

`corpus_identity` vẫn băm ordered canonical `{chunk_id, search_text}` như
contract hiện hành. Vì metadata-only change không nhất thiết làm hash này đổi,
`corpus_identity` không được dùng thay payload schema version.

### 4.2 `domain`

`domain` là enum có đúng năm giá trị:

```text
foods
heritages
festivals
performing_arts
travel
```

Nguồn canonical duy nhất là first path component của `source`. `travel/places`,
`travel/services` và `travel/tickets` đều map thành `travel`; chúng không trở
thành subdomain trong canonical metadata.

Canonical `FullCorpusChunk` materialize `domain` một lần từ `source`; payload
dùng chính value đã validate đó. Downstream không có một taxonomy mapping thứ
hai cạnh tranh với chunk contract.

Baseline tại commit được pin có 205 files:

| Domain | File count |
|---|---:|
| `foods` | 91 |
| `heritages` | 29 |
| `festivals` | 27 |
| `performing_arts` | 13 |
| `travel` | 45 |

Chunking/preflight phải fail nếu source root không thuộc enum hoặc `domain`
không khớp source. Không dùng LLM, filename keyword hoặc web enrichment để suy
domain.

## 5. Qdrant payload schema v2

Mỗi point trong bốn collection v2 có cùng dense/sparse vector schema hiện hành
và payload đúng bảy top-level fields:

```text
search_text: non-empty string
source: non-empty canonical relative POSIX path
title: string
heading_path: list[string]
evidence_parts: list[{role: body|header|condition, start: int, end: int, text: string}]
chunk_id: non-empty string
domain: foods|heritages|festivals|performing_arts|travel
```

Năm field cũ giữ nguyên value semantics. `evidence_parts` tiếp tục thỏa exact LF
source slicing contract; `search_text` vẫn là private retrieval representation
và không phải answer evidence.

Validator canonical v2 yêu cầu exact field set: thiếu hoặc thừa field đều fail
closed. Nó còn kiểm:

- exact types và evidence roles/offset constraints hiện hành;
- relation giữa `source`, `chunk_id`, `domain` và point UUID;
- không có absolute path;
- `chunk_id`/domain của các result không được silently derive để bù payload
  malformed.

Runtime v2 không có compatibility mode nhận đồng thời payload 5 và 7 fields.
Migration reader có validator riêng cho exact legacy five-field payload; nó
không nới canonical runtime validator.

Không tạo payload index cho `domain` trong amendment này. Baseline tiếp tục
search toàn corpus và hiện không có approved filter consumer. Payload index chỉ
được mở lại cùng một filter/facet experiment có metric và scope riêng.

## 6. Build record schema v2

Mỗi collection v2 có một final-only deterministic build record mới tại:

```text
data/full_corpus_builds/<new_collection_name>.json
```

Record giữ các field v1 đang có consumer và thêm version/lineage tối thiểu:

```text
schema_version: phase_4_full_corpus_build:v2
status: complete
collection_name: <new exact collection name>
representation: A
corpus:
  identity: <canonical corpus identity>
  file_count: 205
  chunk_count: 8460
  sources: map[relative POSIX path, normalized-LF UTF-8 SHA-256]
dense:
  candidate_id: <candidate ID>
  model_id: <pinned model ID>
  revision: <pinned revision>
  dimension: <candidate dimension>
sparse:
  schema_version: phase_3_sparse_state:v1
  state_sha256: <pinned sparse-state SHA-256>
  vocabulary_size: 5662
qdrant:
  payload_schema_version: full_corpus_qdrant_payload:v2
  dense_vector_name: dense
  sparse_vector_name: sparse
  distance: cosine
  point_count: 8460
migration:
  mode: copy_verified_vectors
  source_collection: <matching legacy collection>
  source_build_record_sha256: <SHA-256 of exact legacy record bytes>
```

Build record `schema_version` mô tả record contract; `payload_schema_version`
mô tả stored payload contract. Cả hai phải được startup kiểm riêng. Record
không thêm timestamp, run ID, endpoint, secret, vectors, full payload, absolute
path hoặc per-point hashes.

Collection name cùng deterministic build-record content/hash là đủ để nhận diện
artifact. Amendment không thêm generic `build_id` hoặc collection registry.

## 7. Bốn fresh collections và vector-copy migration

Tạo đúng bốn fresh isolated collections v2, mỗi collection tương ứng một-một
với legacy Representation A collection:

- `hue_full_corpus_a_e5_small_384`;
- `hue_full_corpus_a_e5_base_768`;
- `hue_full_corpus_a_huydang_dek21_768`;
- `hue_full_corpus_a_qwen3_06b_1024`.

Bốn exact target names mới phải được khóa trong Implementation Plan trước live
write approval. Không sinh suffix tự động và không nhận arbitrary target từ
caller.

Legacy collections và build records là immutable sources. Migration không
patch payload in place, reconcile, rename, alias, replace hoặc delete chúng.

### 7.1 Pre-write gates

Mỗi source/target pair phải fail closed trước write nếu bất kỳ điều kiện nào
không đạt:

1. target collection chưa tồn tại và target build-record path chưa tồn tại;
2. legacy collection/build record là exact expected candidate;
3. current discovery + normalized-LF source hashes khớp đủ legacy record;
4. fresh chunking không lỗi và khớp exact file/chunk counts, corpus identity và
   sparse-state identity;
5. fresh point-ID set bằng legacy point-ID set;
6. legacy collection có exact dense/sparse names, dimension, distance, count và
   exact five-field payload contract;
7. mọi legacy point có cả dense và sparse vector hợp lệ.

Không load hoặc gọi dense embedding model. Dense và sparse vectors đều được
đọc nguyên từ matching legacy collection; payload v2 được tái tạo từ fresh
canonical chunks rồi ghép bằng deterministic point ID.

### 7.2 Write và completion verification

Migration xử lý bounded batches; không lưu full vector matrices thành tracked
artifact. Mỗi target dùng Qdrant vector/index defaults giống legacy contract và
không có payload index.

Trước khi ghi final build record, implementation phải xác minh toàn bộ target:

- exact vector schema và point count `8.460`;
- exact expected point-ID set;
- exact seven-field payload values từ fresh chunks;
- dense vector values bằng values đã đọc từ matching source point;
- sparse indices, ordering và values bằng matching source point;
- không có missing/extra/duplicate point;
- read-only retrieval smoke hoàn thành cho contract cần kiểm.

Vector comparison được thực hiện streaming/batched trên toàn point set; không
thay bằng chỉ kiểm dimension hoặc deterministic sample. Không cần lưu per-point
vector hash trong payload/build record.

Collection mới có cùng vectors không bảo đảm ANN index mới trả thứ tự tuyệt đối
giống mọi query. Vì vậy smoke phải báo ranking differences/anomalies quan sát
được; không tự diễn giải difference là embedding change.

Nếu write dở dang hoặc verification fail, giữ target failed để điều tra, không
ghi final build record và không tự rollback/delete. Recovery cần exact target
và User approval riêng.

## 8. Runtime readiness, retrieval và trace

### 8.1 Startup freshness

Composition root v2 phải:

1. đọc build record của selected collection;
2. yêu cầu exact build schema v2 và payload schema v2;
3. kiểm candidate/model/revision/dimension, representation, vector names/count,
   corpus identity và sparse-state identity như hiện hành;
4. rediscover current source paths, đọc UTF-8 strict, normalize LF và tính
   SHA-256;
5. so sánh exact path/hash mapping với `corpus.sources` trong build record.

Bất kỳ file thêm, xóa, rename hoặc content-hash mismatch nào cũng làm retrieval
not ready. Runtime không cảnh báo rồi tiếp tục phục vụ stale collection. Phase
6 giữ public `409 corpus_reingest_required` cho trường hợp này.

Startup không rechunk toàn corpus và không recompute embeddings. Fresh
chunking/corpus-identity recomputation thuộc ingestion/migration preflight.

### 8.2 Retrieval identity và metadata

Canonical logical result v2:

```text
RetrievedDocument
  id: payload.chunk_id
  score: final stage score theo Phase 5 contract
  text: private search_text
  metadata:
    source
    title
    heading_path
    evidence_parts
    domain
```

Không lặp `chunk_id` trong `metadata` vì `id` đã là canonical logical ID.
Qdrant point UUID tiếp tục là internal storage/query/fusion key và có thể xuất
hiện trong low-level private trace để reconcile Qdrant operations. Ranking,
RRF/reranker semantics và Phase 5 point-ID tie-break không đổi chỉ vì result ID
đổi ở boundary.

Private `RetrievalTrace` bổ sung logical `chunk_id` và `domain` cho per-result
diagnostics. Trace không chứa query text, search text, evidence text, source
path, absolute path hoặc public-facing source objects. `domain` không được dùng
ngầm để filter, boost, fuse hoặc rerank.

Query-time payload validation fail closed nếu một returned point vi phạm exact
schema hoặc identity/domain relation. Không synthesize missing metadata từ path
để tiếp tục trả result.

## 9. Filtering, evaluation và public boundary

### 9.1 Retrieval behavior

Baseline tiếp tục query toàn collection. Amendment không thêm:

- automatic question router hoặc hard domain filter;
- optional public/internal domain filter parameter;
- domain boost hoặc domain-aware reranking;
- fallback từ filtered sang unfiltered retrieval.

Một domain-filter experiment về sau phải định nghĩa query classification,
cross-domain behavior, pre/post-filter semantics, recall/quality metrics và
payload-index decision trước implementation.

### 9.2 Evaluation

Canonical Full-corpus Golden tiếp tục có đúng bốn fields:

```text
question
keywords
reference_answer
category
```

Không thêm `domain`, `domains`, retained authoring partition, expected chunk ID
hoặc source span. Official aggregate/category breakdown không đổi. Domain trong
retrieval trace có thể hỗ trợ diagnostics ad hoc về returned results nhưng
không tạo official benchmark grouping theo intended question domain.

### 9.3 Context, citation và API

Phase 6 ContextBuilder tiếp tục chỉ dùng `title`, `heading_path` và
`evidence_parts` làm answer context; không dùng `search_text`, `domain`, point
ID hoặc chunk ID làm evidence.

Public source schema giữ nguyên:

```json
{
  "id": 1,
  "title": "Tên tài liệu",
  "heading_path": ["Mục"],
  "excerpts": ["Đoạn bằng chứng nguyên văn"]
}
```

Public API không trả `domain`, source path, point/chunk ID, build identity,
score, rank, search text hoặc retrieval trace.

## 10. Explicit exclusions

Amendment không thêm:

- `subdomain`, `document_type`, tags hoặc LLM-generated classifications;
- `document_id`, generic payload `id`, per-point content/source hash;
- `created_at`, `updated_at`, freshness timestamp hoặc source URL;
- model ID, revision, representation, build ID/version hoặc collection name
  trên từng point;
- payload indexes, aliases, registry, dual-read/dual-write hoặc automatic
  migration framework;
- re-embedding, sparse refit, Representation B hoặc corpus enrichment;
- Golden/evaluator schema change, public API field hoặc UI filter;
- old-collection mutation, cutover, replacement hoặc cleanup;
- migration hoặc behavior change cho Foods MVP legacy pipeline/collections.

## 11. Supersession và lịch sử

Khi được User duyệt, amendment này supersede có mục tiêu:

- Full-corpus master Written Spec mục 5 chỉ ở phát biểu exact five-field
  payload và việc không materialize domain/chunk ID;
- Phase 4 Written Spec các mục 6, 9, 10, 14 và 16 chỉ ở point payload/build
  schema/completion checks được thay bằng v2 cho bốn fresh collections;
- Phase 5 Written Spec các mục 2, 9, 10, 11 và 16 chỉ ở exact payload,
  `RetrievedDocument.id`, metadata/trace và freshness readiness;
- Phase 6 dependency/readiness chỉ ở chỗ phải consume retrieval v2 trước khi
  implementation tiếp tục.

Nó không retroactively làm mất hiệu lực closure/evidence của Phase 2–5 hoặc
thay đổi contents của tám legacy artifacts gồm bốn collections và bốn v1 build
records. Các artifact đó phản ánh đúng contract tại thời điểm được duyệt và
được giữ read-only làm migration source/audit history.

Mọi requirement khác của các spec trên tiếp tục có hiệu lực, gồm exact evidence
provenance, retrieval algorithms/scores, citation mapping, public response,
privacy và failure behavior.

## 12. Acceptance criteria cho metadata v2 workstream

Workstream chỉ có thể được Reviewer đề xuất PASS khi có evidence cho toàn bộ:

1. code/diff chỉ triển khai approved metadata scope và không sửa corpus;
2. canonical chunk có validated `chunk_id` và five-value `domain`;
3. point IDs vẫn là deterministic UUID5 và khớp payload chunk ID;
4. canonical payload validator yêu cầu đúng bảy fields; legacy reader bị giới
   hạn trong migration path;
5. build record v2 tách build schema và payload schema, giữ model/source/sparse
   identity ở build level và ghi exact vector-copy lineage;
6. source freshness mismatch fail closed trước retrieval availability;
7. đủ bốn fresh target collections, mỗi target có exact 8.460 point IDs,
   seven-field payloads và source-equal dense+sparse vectors;
8. bốn legacy collections/build records không bị mutate;
9. không dense embedding execution, sparse refit hoặc paid model/API call;
10. `RetrievedDocument.id` là logical chunk ID; domain có trong private
    metadata/trace nhưng không ảnh hưởng ranking;
11. không payload index, domain filter/router, Golden change hoặc public API
    expansion;
12. pure tests, integration tests, complete migration verification và
    read-only retrieval smoke đạt theo approved Review Contract;
13. collection creation và cutover chỉ xảy ra sau đúng từng User approval gate;
14. reports phân biệt reused evidence, fresh evidence, failed/skipped/not-run
    và không chứa private corpus text.

## 13. Next gate

Reviewer phải viết Implementation Plan và Review Contract riêng để User duyệt,
trong đó khóa:

- exact four source-to-target collection name mappings;
- code/docs/test paths và task order;
- preflight evidence trước live write;
- exact live-write checkpoint cho bốn targets;
- post-build independent review;
- runtime cutover checkpoint riêng;
- correction/recovery authority nếu có partial target.

Không suy diễn approval Written Spec thành approval implementation hoặc Qdrant
write.

## 14. Research references

- Qdrant points/payload model:
  <https://qdrant.tech/documentation/concepts/points/>
- Qdrant filtering semantics:
  <https://qdrant.tech/documentation/search/filtering/>
- Qdrant payload indexing and resource trade-offs:
  <https://qdrant.tech/documentation/manage-data/indexing/>

Các reference trên chỉ hỗ trợ storage/filter/index decisions. Contract của Hue
RAG được quyết định từ consumers, corpus và lifecycle thực tế của repository;
không sao chép schema của một framework/reference project khác.
