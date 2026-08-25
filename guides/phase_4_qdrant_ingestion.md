# Phase 4: Qdrant ingestion và deterministic dense points

## Mục tiêu và giá trị cho người dùng

Phase 4 đưa canonical food chunks cùng dense representations vào một active
Qdrant collection có schema kiểm chứng được. Kết quả là một index tái lập, an
toàn khi reset và sẵn sàng cho cả ba retrieval profiles. Hai profile hybrid dùng
Python BM25 sau dense candidate generation; chúng không cần Qdrant sparse
vectors.

## Trạng thái

```text
Status: approved
Owner: Codex Reviewer
Implementer: DeepSeek
```

> **Lưu ý governance hiện hành:** Các đoạn bên dưới mô tả implementation và
> test contract lịch sử của Phase 4, bao gồm mocked validation và per-run
> approval. Chúng không áp dụng cho công việc mới. Shared governance hiện hành
> yêu cầu real execution, không mock/fake và chỉ giữ approval riêng cho active
> mutation hoặc destructive action. Coordinated simplicity review Phase 4–5
> đã hoàn tất và được user xác nhận ngày `2026-08-25 +07`.

> **Kết quả simplification ngày 2026-08-25 +07:** Target production baseline là
> Qdrant dense-only. Stored custom TF-IDF sparse vectors đã được loại khỏi point
> construction, ingestion code và dense-only candidate; Python BM25 và
> CrossEncoder được giữ. Active collection cũ vẫn có sparse vectors lịch sử vì
> candidate chưa được cutover. Cutover hoặc mutation active vẫn cần user
> approval riêng.

> Phase 4 và phần lexical/startup liên quan trực tiếp của Phase 5 được
> brainstorming cùng một lần để tránh thiết kế hai nửa không khớp. Scope chung
> không tự mở rộng sang context, generation hoặc API nếu consumer audit không
> chứng minh bị ảnh hưởng.
>
> Thiết kế coordinated Phase 4–5 đã được user duyệt ngày `2026-08-25 +07` tại
> `docs/superpowers/specs/2026-08-25-phase-4-5-qdrant-retrieval-simplicity-design.md`.
> Implementation, independent review và user confirmation đã hoàn tất. Approval
> đó không tự cho phép cutover/delete collection, commit hoặc push.

Brainstorming được người dùng phê duyệt ngày 2026-08-12 +07. Codex đã
kiểm tra notebook ở default mode và real read-only mode; người dùng xác nhận
Phase 4 ngày 2026-08-12 +07 và chọn không tự chạy notebook trước khi phê duyệt.
Phase 4 được approved.

## Dependency

- Phase 3 phải được người dùng xác nhận và có status `approved`.
- Dense model ID, actual dimension và normalization contract đã khóa.
- Canonical lexical path là Python BM25 thuộc Phase 5, không phải stored Qdrant
  sparse vectors.
- Qdrant chạy riêng cho `hue_rag` bằng Docker Compose local; availability vẫn
  phải preflight trước mọi mutation.
- User approval bắt buộc trước collection deletion/reset.

## Chức năng phải tạo

- Tạo một Qdrant client tại composition root theo config và truyền xuống các
  consumer trong vòng đời tiến trình.
- Kiểm tra Qdrant availability và collection metadata.
- Tạo collection với một named dense vector schema.
- Build deterministic Qdrant points từ chunks.
- Batch upsert và kiểm tra point count.
- Ingestion pipeline kết nối Phase 2–4.
- Reset guard fail closed và chỉ xóa exact expected collection.
- Notebook inspect collection thật ở read-only, không có mutation path.

## Files dự kiến

```text
docker-compose.yml
pyproject.toml
uv.lock
backend/config/settings.yaml
backend/config/README_config.md
backend/vectorstore/qdrant.py
backend/vectorstore/points.py
backend/vectorstore/upsert.py
backend/vectorstore/reset.py
backend/ingestion/pipeline.py
backend/tests/test_qdrant_schema.py
backend/tests/test_ingestion_pipeline.py
notebooks/04_qdrant_ingestion.ipynb
reports/phase_4_qdrant_ingestion_implementation_report.md
```

`qdrant_storage/` là ignored local artifact, không phải deliverable. Không sửa
`llm_rag`, không xóa `nmk_chatbot_collection` và không copy module thừa từ repo
tham khảo.

## Qdrant local runtime contract

Phase 4 dùng Qdrant server riêng cho `hue_rag`:

```text
REST: http://localhost:6333
gRPC: localhost:6334
storage: ./qdrant_storage:/qdrant/storage
image version: v1.18.3
image: qdrant/qdrant@sha256:0bd98fa7977f1e75694779359ca4e212822e5a71334e28421182f72f209d5286
```

Không dùng `latest`, embedded mode hoặc Qdrant Cloud. `llm_rag` đã ngừng chạy
nhưng storage cũ được giữ nguyên. Hai Docker Compose projects dùng cùng host
ports nên không chạy đồng thời; Phase 4 không thêm port configurability ngoài
scope local MVP.

## Active collection invariant

- Hue Foods chỉ có một active collection tại một thời điểm.
- Một embedding model dùng cùng collection cho `dense_only`, `hybrid_no_rerank` và `hybrid_rerank`.
- Migration không xóa active trước. Tạo candidate collection mới, ingest và
  verify thật; chỉ đổi configured active name sau user-approved cutover.
- Trong migration có thể tạm tồn tại active cũ, candidate mới và sau cutover là
  rollback collection cũ. Đây là lifecycle hữu hạn, không phải framework quản
  lý nhiều production collections.
- Phase 8 experiment candidate là lifecycle riêng và cũng không trở thành active
  chỉ vì nó tồn tại.
- Active hiện tại là `hue_foods_e5_small_384`; dense-only candidate cố định là
  `hue_foods_e5_small_384_dense`.
- Collection name không thay thế schema/payload validation; runtime vẫn kiểm tra
  exact model `intfloat/multilingual-e5-small`, dimension `384`, distance và
  vector name.

## Collection schema contract

Dense named vector:

```text
name: dense
size: actual embedder dimension
distance: cosine
```

Trước upsert, runtime phải kiểm tra:

- collection name;
- dense vector name, dimension và distance;
- payload identity fields trên mọi existing point;
- embedding model identity trong payload;
- embedding dimension từ Qdrant schema/config, không lặp trong payload.

Nếu existing schema khác expected schema và reset chưa được phép, pipeline phải dừng với actionable error; không tự recreate.
Nếu collection đã có points, existing point IDs phải là tập con của 572 expected
UUID5 IDs và payload identity phải khớp. Point lạ, count lớn hơn 572 hoặc payload
không tương thích đều fail closed trước upsert.

## Point contract

Mỗi Qdrant point:

```python
{
    "id": "UUID5 derived from hue-rag:<chunk_id>",
    "vector": {
        "dense": [0.01, 0.02],
    },
    "payload": {
        "text": "...",
        "chunk_id": "...",
        "source": "foods/...",
        "title": "...",
        "section": "...",
        "category": "foods",
        "subcategory": "...",
        "chunk_type": "section",
        "embedding_model": "...",
    },
}
```

Point ID dùng `uuid.uuid5(uuid.NAMESPACE_URL, f"hue-rag:{chunk_id}")`. Original
`chunk_id` luôn được giữ trong payload. Không có random fallback; missing/invalid
`chunk_id` phải fail trước upsert.

Dense vector array phải cùng số lượng với chunks. `zip()` không được phép che
giấu length mismatch; kiểm tra lengths trước khi build points.

## Ingestion pipeline contract

```text
load settings
  -> resolve active embedding provider/model
  -> discover and chunk curated foods Markdown
  -> validate chunk count and IDs
  -> embed all chunk texts with document instructions
  -> validate vector count/dimension/finiteness
  -> preflight Qdrant, expected schema and existing point identity
  -> create collection only when absent
  -> build deterministic dense points
  -> batch upsert 64 points with wait=true
  -> verify collection schema and exact point count
  -> emit non-sensitive summary
```

Expected baseline point count là 572 khi curated corpus/chunking không đổi. Nếu count khác, implementation report phải giải thích input diff; không cập nhật expected count âm thầm.

## Reset và deletion safety

Ingestion không bao giờ delete/recreate collection. Canonical config là:

```yaml
vector_database:
  url: http://localhost:6333
  collection_name: hue_foods_e5_small_384
  vector_size: 384
  distance: cosine
  timeout: 30
  upsert_batch_size: 64
```

Không có `reset_collection` config flag. Reset là exact command riêng với target
bắt buộc, không thể được bật tình cờ qua runtime config; ingestion lần sau chịu
trách nhiệm tạo lại nếu target còn cần được dùng.

Trước destructive command phải có:

```text
exact target collection name
current point count
explicit user approval
exact confirmation string
```

Guard rules:

- không dùng glob, prefix-only match hoặc list-delete;
- không xóa collection khác target;
- collection phải tồn tại và point count phải đọc được để hiển thị trước xóa;
- log action summary nhưng không log key/header;
- command yêu cầu `--collection <name>` và confirmation string phải đúng
  `DELETE <name>` cho cùng exact target;
- sau delete phải xác minh exact collection không còn tồn tại;
- reset không yêu cầu collection khớp expected schema/payload vì schema mismatch
  có thể chính là lý do migration;
- reset failure không tự chạy ingestion hoặc follow-up mutation nào.

Phase 4 validation không chạy live reset trên active collection chỉ để chứng
minh guard. Reset safety được kiểm tra trên exact guarded test collection; mọi
active deletion vẫn cần approval riêng.

## Sparse storage boundary

Active baseline Phase 4 là dense-only. Current hybrid runtime ở Phase 5 lấy
dense candidates rồi dùng Python BM25; lưu sparse vectors nhưng không query
chúng không cải thiện retrieval.

Phase 8 giữ nguyên ba canonical profiles và có thể đánh giá true hybrid retrieval
như một candidate experiment riêng. Experiment đó phải dùng isolated candidate
collection có sparse vectors, không mutate active baseline và so sánh trên cùng
canonical corpus, evaluation questions, metric definitions và các biến được giữ
cố định. Stored sparse chỉ được đưa trở lại production khi real results chứng
minh lợi ích tương xứng complexity và user duyệt exact transition.

## Kiến trúc đã phê duyệt

Phase 4 dùng các module chức năng nhỏ thay vì một stateful service class hoặc
module ingestion gộp lớn:

- `qdrant.py`: tạo client, availability, collection create/inspect/schema validation;
- `points.py`: pure chunk/vector validation, UUID5 và deterministic dense point
  construction;
- `upsert.py`: bounded batch upsert và count verification;
- `reset.py`: destructive command riêng;
- `ingestion/pipeline.py`: điều phối Phase 2–4, không có deletion path.

Mỗi batch có 64 points và timeout 30 giây. Mọi lỗi upsert được trả thẳng; không
phân loại exception để manual retry. Nếu batch trước đã thành công rồi batch sau
thất bại, pipeline ghi safe completed count và dừng; không rollback bằng
collection deletion. Rerun toàn ingestion an toàn nhờ deterministic IDs và
idempotent upsert, sau khi existing IDs/payload được xác nhận thuộc expected
corpus.

## Nhiệm vụ của DeepSeek Implementer

- Dùng pure-function tests hoặc real guarded Qdrant/model execution; không dùng
  mock/fake làm system evidence.
- Giữ/tạo test chỉ cho exact dense schema, deterministic point contract,
  canonical ingestion/idempotency và destructive guard thật sự cần thiết.
- Không dùng deprecated/destructive collection helper khi behavior không rõ; chọn API hiện hành sau local dependency inspection.
- Không ghi API key vào settings/report.
- Giữ ingestion deterministic, bounded batches và actionable errors.
- Tạo implementation report liệt kê exact collection action; redact endpoint nếu private.

## Notebook bắt buộc

`notebooks/04_qdrant_ingestion.ipynb` phải:

- import Phase 2–4 modules;
- giải thích named dense vector, payload và one-active-collection lifecycle;
- Run All inspect read-only collection thật đã được ingestion tạo, kiểm tra
  schema/count/payload projection và không có fake fallback;
- không chứa reset/delete cell;
- committed outputs rỗng và `execution_count=null`.

## Tests và validation dự kiến

Test chỉ được giữ hoặc tạo khi bảo vệ hành vi người dùng cần. Không đặt target
theo số lượng, không dùng mock/fake làm system evidence và không tách nhiều file
chỉ để phủ lỗi kỹ thuật hiếm. Mỗi test phải trả lời được hành vi nào sẽ hỏng nếu
test bị bỏ.

Target evidence tối thiểu, còn được tinh chỉnh sau mechanism audit:

- pure behavior check cho deterministic point identity, dense vector count/
  dimension/finiteness và payload cần thiết;
- real guarded-Qdrant check cho dense-only schema create/validate và fail trước
  write khi existing schema không tương thích;
- real guarded ingestion của canonical 572 chunks, exact count và idempotent
  rerun;
- real exact-target reset guard trên guarded collection, không đụng active
  collection;
- real read-only query/startup smoke cho các profile bị ảnh hưởng sau coordinated
  Phase 4–5 change.

Client-cache và exact retry-call tests bị loại cùng cơ chế. Fingerprint internals,
redundant schema permutations và sparse-vector validation không phải test
requirement mặc định. Chỉ giữ khi cơ chế được duyệt giữ lại và failure thực tế
chứng minh test có giá trị.

Commands:

```bash
cd backend
uv run python -m py_compile vectorstore/qdrant.py vectorstore/points.py vectorstore/upsert.py vectorstore/reset.py ingestion/pipeline.py
uv run python -m pytest tests/test_qdrant_schema.py tests/test_ingestion_pipeline.py -q --tb=short
```

Live validation trong approved implementation scope dùng pinned local Qdrant,
actual E5 và guarded test collection để tạo schema/upsert 572 points. Không cần
approval theo từng run; chỉ active mutation/destructive action cần approval
riêng. Không dùng fake fallback khi dependency hoặc model unavailable.

Live evidence phải ghi:

```text
collection name
schema
embedding model/dimension
chunk count
point count
reset action/confirmation và approval evidence nếu có destructive run
```

## Security, data safety, reliability và performance

- Không log credentials, raw headers hoặc full vectors.
- Chỉ index curated answer-facing chunks.
- Upsert idempotent nhờ deterministic IDs.
- Partial upsert không được báo thành công; final count là gate.
- Upsert batch 64, `wait=True`; lỗi trả thẳng và rerun toàn ingestion bằng
  deterministic idempotent points.
- Collection deletion là destructive action được kiểm tra hai lớp.
- Với 572 chunks, tránh concurrency hoặc retry framework phức tạp chưa cần thiết.

## Tiêu chí phê duyệt Phase 4

- Pure behavior và real guarded-system tests chứng minh schema, ingestion và
  reset safety.
- Docker Compose pin đúng Qdrant `v1.18.3` digest và dùng storage riêng.
- Approved real preflight xác nhận Qdrant reachable.
- Collection chỉ có named `dense`, dimension đúng model và không có stored
  sparse vector.
- Dense-only candidate `hue_foods_e5_small_384_dense` có exact count 572. Active
  cũ không bị mutate trong candidate verification.
- Payload không có absolute private path hoặc secret.
- Ingestion không có deletion path hoặc reset config flag; reset chỉ qua exact
  command riêng.
- Rerun idempotent và partial failure không được báo thành công.
- Notebook Run All chỉ đọc Qdrant thật, kiểm tra đúng schema/count/payload
  projection và report ghi đúng collection actions; không có live deletion.
- User report phản ánh đúng collection actions/limitations và được người dùng xác nhận cùng notebook.
- Không gọi Python BM25 reranking trên dense candidates là native Qdrant sparse
  retrieval.

## Reports và cập nhật trạng thái

Current coordinated simplicity evidence:

```text
reports/phase_4_5_qdrant_retrieval_simplicity_implementation.md
reports/phase_4_5_qdrant_retrieval_simplicity_codex_review.md
reports/user_reports/phase_4_5_qdrant_retrieval_simplicity_user_report.md
```

Historical Phase 4 evidence trước simplicity review:

```text
reports/phase_4_qdrant_ingestion_implementation_report.md
reports/phase_4_qdrant_ingestion_codex_review.md
reports/user_reports/phase_4_qdrant_ingestion_user_report.md
```

Model/collection metadata và kết quả thật cần thiết nằm trong
`reports/hue_foods_rag_benchmark.md`. Cả Phase 4 gốc và coordinated simplicity
review Phase 4–5 đã được người dùng xác nhận.

## Quyết định đã phê duyệt

```text
Decision: Active production baseline dùng Qdrant dense-only. Xóa custom TF-IDF
sparse vector khỏi active collection schema, point construction và ingestion;
giữ Python BM25 và CrossEncoder capabilities cho ba canonical Phase 8 profiles.
Approved by: User
Approval date +07: 2026-08-25
Evidence: Sau khi đối chiếu source llm_rag và Phase 8, user chọn phương án A.
Current runtime chỉ query named dense vector rồi tính Python BM25; stored sparse
vectors không được query và không tạo retrieval benefit.
Affected scope: Phase 4 schema/point/upsert/ingestion/tests/notebook; coordinated
Phase 5 lexical ownership; Phase 8 baseline profiles và candidate isolation.
Coordination choice: Trong cùng implementation scope, chuyển shared tokenize()
sang BM25/scoring ownership và chỉ xóa SparseEmbedder sau consumer audit sạch.
Migration choice: Blue-green. Giữ active hue_foods_e5_small_384 read-only, tạo
dense-only candidate tên mới, ingest/verify 572 chunks và ba profiles bằng dữ
liệu/dịch vụ thật. Sau technical review, dừng xin user approval trước config
cutover. Giữ collection cũ làm rollback; xóa cũ cần approval riêng sau đó.
Không xây multi-collection framework hoặc auto-cutover.
Phase 8 boundary: Nếu đánh giá true hybrid retrieval, tạo isolated candidate
collection có sparse vectors và so sánh công bằng. Chỉ đưa sparse storage trở
lại production khi real observed results chứng minh lợi ích tương xứng complexity
và user duyệt exact transition.
Revisit trigger: Phase 7 evidence cho thấy dense candidate recall là limitation,
hoặc approved Phase 8 true-hybrid experiment chứng minh lợi ích thực tế.
```

```text
Decision: Brainstorm Phase 4 và phần Phase 5 liên quan trong cùng design; cho
phép test khi test bảo vệ hành vi thật hoặc lỗi thực tế quan trọng. Không có test
count target, mock/fake system evidence, nhiều file cho rare mechanics hoặc test
không giải thích được user behavior được bảo vệ.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn migration phương án A, cho phép joint Phase 4–5 brainstorming
và nêu explicit test principles.
Affected scope: Phase 4–5 design, existing-test audit, acceptance evidence và
implementation plan.
Revisit trigger: Một mechanism có production failure evidence cần test riêng,
hoặc blast radius thật mở rộng sang downstream phase.
```

```text
Decision: Giữ separate reset CLI nhưng đơn giản hóa. Ingestion không có deletion
path hoặc reset config flag. Reset yêu cầu explicit `--collection <name>`, exact
matching `--confirm "DELETE <name>"`, collection tồn tại, đọc/hiển thị point
count, delete và verify absent. Target không phụ thuộc active config để cùng
command có thể cleanup guarded test, failed candidate hoặc retired rollback
collection. Không validate expected schema/toàn bộ payload trước delete vì schema
mismatch có thể chính là lý do cleanup.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn reset phương án A và nhắc lại simplicity/real-execution
principles.
Affected scope: settings, ingestion reset rejection, vectorstore/reset.py,
guarded reset test, config docs và migration runbook.
Safety boundary: Active reset vẫn cần exact user approval riêng; implementation
tests chỉ delete guarded test collection.
Revisit trigger: Real guarded execution cho thấy exact-target/confirmation/post-
delete verification không đủ ngăn wrong-target deletion.
```

```text
Decision: Reset target là required explicit argument, không bị khóa vào configured
active collection. Exact confirmation phải chứa cùng target. Không tạo cleanup
script riêng hoặc tạm sửa config để xóa old blue-green collection.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn reset-target phương án A.
Affected scope: reset CLI signature, guarded test, migration cleanup runbook và
operator-facing error messages.
Safety boundary: Exact target/confirmation không thay thế explicit user approval
trước khi xóa active hoặc rollback collection.
Revisit trigger: Real CLI ergonomics cho thấy target có thể bị hiểu sai hoặc
Qdrant endpoint chứa collections ngoài project cần isolation khác.
```

```text
Decision: Giữ pre-upsert scan đơn giản cho rerun vào candidate đã có points.
Existing point IDs phải là tập con của 572 deterministic UUID5 IDs và payload
embedding_model phải khớp trước mutation; dimension lấy từ collection schema.
Sau upsert phải có exact count 572. Candidate absent/empty không bị cản.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn preflight phương án A.
Affected scope: upsert existing-point validation, payload projection, idempotent
rerun và focused real-Qdrant tests.
Test boundary: Một valid rerun và một foreign/model-mismatch behavior đủ bảo vệ
contract; không nhân nhiều test permutations.
Revisit trigger: Corpus lớn đến mức bounded scan gây observed ingestion problem
hoặc Qdrant cung cấp simpler atomic ownership constraint được dùng thật.
```

```text
Decision: Đổi hybrid_index.py thành vectorstore/points.py. points.py chỉ giữ pure
chunk/dense-vector validation, deterministic UUID5 và PointStruct construction;
upsert.py chỉ giữ existing-point scan, bounded Qdrant write và count gate. Không
thêm class/interface. Xóa test_hybrid_index.py và chuyển behavior tests còn giá
trị vào test_ingestion_pipeline.py.
Approved by: User
Approval date +07: 2026-08-25
Evidence: Caller audit xác nhận chỉ ingestion pipeline dùng module; user chọn
module-boundary phương án A.
Affected scope: vectorstore module/import names, ingestion pipeline, focused
tests, notebook/report references.
Revisit trigger: points.py không còn pure hoặc một second real consumer cần
public contract khác.
```

```text
Decision: Dùng blue-green Phase 4 migration. Tạo dense-only candidate collection
mới và chạy real ingestion/retrieval verification trong khi active collection cũ
read-only. Candidate chỉ thành active sau explicit user-approved config cutover;
collection cũ được giữ làm rollback và chỉ xóa bằng approval riêng.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User thay thế same-name migration bằng phương án A blue-green và nhắc
lại code phải đơn giản, real-data/real-service, không fake evidence.
Success meaning: Vì dense model/vectors không đổi, Phase 4 cần chứng minh quality
tương đương, schema/code đơn giản hơn và không regression latency/reliability;
không tuyên bố quality gain chỉ vì bỏ sparse storage.
Affected scope: candidate naming/config, ingestion target, real verification,
cutover/rollback runbook, reset cleanup và reports.
Revisit trigger: Candidate verification không tương đương active baseline hoặc
temporary rollback lifecycle đòi framework phức tạp.
```

```text
Decision: Blue-green cutover evidence dùng 104 canonical retrieval questions trên
cả dense_only, hybrid_no_rerank và hybrid_rerank. Chạy fresh active baseline
trước implementation và fresh dense-only candidate sau implementation với cùng
data/settings; so sánh metrics, latency, failures và per-query IDs/scores khi cần.
Không chạy generator/judge vì blast radius chỉ thuộc ingestion/retrieval.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn real-comparison phương án A.
Meaning: Đây là equivalence/regression evidence cho cutover, không chọn Phase 8
winner và không tái sử dụng historical output làm fresh evidence.
Affected scope: implementation checkpoints, Phase 7 retrieval evaluator,
benchmark summary và cutover approval report.
Revisit trigger: Retrieval run phát hiện output change cần answer-level impact
investigation hoặc generator/context contract bị thay đổi ngoài approved scope.
```

```text
Decision: Blue-green commands dùng explicit optional collection_name override ở
composition roots. run_ingestion và retrieval evaluation copy settings trong
memory rồi thay đúng vector_database.collection_name; settings.yaml và API
runtime không bị mutate trước cutover. Không tạo candidate YAML, environment
global hoặc collection manager.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn candidate-targeting phương án A.
Affected scope: ingestion entry point, Phase 7 retrieval-only evaluation call,
Notebook 04/05 và verification commands.
Revisit trigger: More than one real simultaneous candidate workflow cần explicit
configuration design.
```

```text
Decision: Dense-only blue-green candidate có fixed name
hue_foods_e5_small_384_dense. Ephemeral tests tiếp tục dùng guarded prefix
hue_rag_live_test_ và không dùng production-candidate name. Không dùng timestamp,
run ID hoặc collection registry.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn naming phương án A.
Affected scope: Phase 4 settings override/runbook, real verification reports,
Phase 5 cutover config và rollback documentation.
Revisit trigger: Embedding model/dimension đổi hoặc exact name đã tồn tại với
schema/data không tương thích trước candidate creation.
```

```text
Decision: Bỏ Qdrant client lru_cache và manual upsert retry. Mỗi composition root
tạo đúng một client rồi truyền xuống. Upsert failure trả thẳng; rerun toàn
ingestion an toàn nhờ deterministic UUID5 và idempotent upsert. Bỏ retry config
và tests chỉ kiểm call count/cache identity.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn client/retry phương án A theo simplicity và real-execution
principles.
Affected scope: vectorstore/qdrant.py, upsert.py, settings/config docs,
ingestion/startup composition và affected tests.
Revisit trigger: Real repeated transient failures cho thấy fail-and-rerun không
đáp ứng nhu cầu vận hành của corpus nhỏ.
```

```text
Decision: Giữ embedding_model trong mỗi point payload nhưng xóa
embedding_dimension. Model identity bảo vệ lỗi query/index dùng hai embedding
models cùng dimension; Qdrant dense schema là nguồn chuẩn cho dimension và
distance. Chỉ giữ một model-mismatch behavior test dễ hiểu.
Approved by: User
Approval date +07: 2026-08-25
Evidence: Sau khi đối chiếu llm_rag (không lưu cả hai fields), user chọn phương
án A cân bằng simplicity với model-space safety.
Affected scope: point payload, existing-point validation, Phase 5 corpus startup,
API/debug metadata ownership và affected tests/notebook.
Revisit trigger: Qdrant có collection-level model metadata đơn giản được dùng
thật, hoặc Phase 8 collection lifecycle thay đổi model-identity contract.
```

```text
Decision: Dùng 572 canonical chunks và giới hạn 400 ký tự cho nội dung thường; bảng Markdown là ngoại lệ được giữ nguyên.
Approved by: User
Approval date +07: 2026-08-12
Evidence: Phase 2 đã approved và user xác nhận sửa contract cũ trước brainstorming Phase 4.
Affected scope: Phase 4 point count, batch planning, ingestion validation và benchmark ledger.
Revisit trigger: Curated corpus hoặc Phase 2 chunking contract được user phê duyệt thay đổi.
```

```text
Decision: Dùng Qdrant Docker Compose riêng cho hue_rag, storage riêng và pin image local v1.18.3 bằng exact digest; không dùng embedded, Cloud hoặc latest.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User chọn phương án Docker riêng sau khi đối chiếu llm_rag và xác nhận exact image pin trong Phase 4 brainstorming.
Affected scope: docker-compose.yml, local Qdrant lifecycle, ports 6333/6334 và Phase 4 live validation.
Revisit trigger: Image/client incompatibility, cần chạy đồng thời llm_rag hoặc chuyển sang remote Qdrant.
```

```text
Decision: Active collection là hue_foods_e5_small_384; point ID là UUID5 từ hue-rag:<chunk_id> và original chunk_id được giữ trong payload.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User chọn collection naming chứa embedding identity và UUID5 trong Phase 4 brainstorming.
Affected scope: collection schema validation, point identity, idempotent upsert, payload và Phase 5 retrieval IDs.
Revisit trigger: Embedding model/dimension hoặc chunk ID contract được phê duyệt thay đổi.
Superseded in part: `hue_foods_e5_small_384` vẫn là current active nhưng approved
blue-green migration sẽ cut over sang exact dense-only candidate name; UUID5 và
payload chunk_id contract không đổi.
```

```text
Decision: Upsert dùng batch 64, timeout 30 giây và một retry chỉ cho connection/timeout; ingestion không delete, reset là exact-target command riêng.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User xác nhận batch/retry policy, separate reset command và failure policy trong Phase 4 brainstorming.
Affected scope: vectorstore/upsert.py, vectorstore/reset.py, ingestion pipeline, config và tests.
Revisit trigger: Live evidence cho thấy batch/timeout không phù hợp hoặc Qdrant client error taxonomy thay đổi.
Superseded for retry/reset policy: Quyết định 2026-08-25 chỉ giữ batch 64 và
timeout 30; bỏ toàn bộ manual retry/retry config, bỏ `reset_collection` flag và
đưa deletion sang exact-target reset command. Không triển khai lại “một retry”.
```

```text
Decision: Dùng kiến trúc module chức năng nhỏ; notebook Run All Qdrant read-only, live preflight và live ingestion cần approval riêng, không live-delete để test.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User phê duyệt năm phần thiết kế và toàn bộ exact scope/acceptance của Phase 4.
Affected scope: Phase 4 modules, tests, notebook, implementation report và Reviewer validation.
Revisit trigger: Implementation cần file ownership mới, notebook không đủ evidence hoặc acceptance không thể kiểm chứng trong local environment.
```

```text
Decision: Gỡ dependency PyPI vectorstore 0.0.0 vì shadow local backend/vectorstore package; dùng uv run python -m pytest làm canonical test command.
Approved by: User
Approval date +07: 2026-08-12
Evidence: Reviewer tái hiện uv run pytest import nhầm site-packages/vectorstore và user phê duyệt mở rộng allowlist sau non-live checkpoint review.
Affected scope: pyproject.toml, uv.lock, Phase 4 import reliability và validation commands.
Revisit trigger: Project được đóng gói lại với package layout hoặc test runner configuration mới.
```

## Bước tiếp theo

Phase 4 đã hoàn thành coordinated simplicity review cùng Phase 5 và giữ
`approved`. Dense-only candidate chưa cutover; cutover vẫn là quyết định riêng.
Bước tiếp theo của simplicity campaign là Phase 6 theo `guides/README.md`.
Shared governance hiện hành áp dụng cho mọi correction mới.
