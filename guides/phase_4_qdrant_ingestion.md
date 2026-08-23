# Phase 4: Qdrant ingestion và hybrid points

## Mục tiêu và giá trị cho người dùng

Phase 4 đưa canonical food chunks cùng dense/sparse representations vào một active Qdrant collection có schema kiểm chứng được. Kết quả là một index tái lập, an toàn khi reset và sẵn sàng cho cả ba retrieval profiles.

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
> mutation hoặc destructive action. Phase 4 sẽ được review lại sau Phase 7.

Brainstorming được người dùng phê duyệt ngày 2026-08-12 +07. Codex đã
kiểm tra notebook ở default mode và real read-only mode; người dùng xác nhận
Phase 4 ngày 2026-08-12 +07 và chọn không tự chạy notebook trước khi phê duyệt.
Phase 4 được approved.

## Dependency

- Phase 3 phải được người dùng xác nhận và có status `approved`.
- Dense model ID, actual dimension, normalization và sparse state contract đã khóa.
- Qdrant chạy riêng cho `hue_rag` bằng Docker Compose local; availability vẫn
  phải preflight trước mọi mutation.
- User approval bắt buộc trước collection deletion/reset.

## Chức năng phải tạo

- Tạo/cache Qdrant client theo config.
- Kiểm tra Qdrant availability và collection metadata.
- Tạo collection với named dense/sparse vector schema.
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
backend/vectorstore/hybrid_index.py
backend/vectorstore/upsert.py
backend/vectorstore/reset.py
backend/ingestion/pipeline.py
backend/tests/test_qdrant_schema.py
backend/tests/test_hybrid_index.py
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
- Khi đổi embedding model/dimension: lưu artifacts của model cũ, xin user approval, xóa exact collection, tạo lại với model mới, reindex toàn corpus.
- Không giữ nhiều experiment collections trong MVP.
- Active collection cho baseline local là `hue_foods_e5_small_384`.
- Collection name không thay thế schema/payload validation; runtime vẫn kiểm tra
  exact model `intfloat/multilingual-e5-small`, dimension `384`, distance và
  vector names.

## Collection schema contract

Dense named vector:

```text
name: dense
size: actual embedder dimension
distance: cosine
```

Sparse named vector:

```text
name: sparse
type: Qdrant sparse vector
index: enabled
```

Trước upsert, runtime phải kiểm tra:

- collection name;
- dense vector name, dimension và distance;
- sparse vector name;
- payload identity fields trên mọi existing point;
- embedding model identity và dimension trong payload/config evidence.

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
        "sparse": {
            "indices": [1, 7],
            "values": [1.3, 2.1],
        },
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
        "embedding_dimension": 384,
    },
}
```

Point ID dùng `uuid.uuid5(uuid.NAMESPACE_URL, f"hue-rag:{chunk_id}")`. Original
`chunk_id` luôn được giữ trong payload. Không có random fallback; missing/invalid
`chunk_id` phải fail trước upsert.

Dense/sparse arrays phải cùng số lượng với chunks. `zip()` không được phép che giấu length mismatch; kiểm tra lengths trước khi build points.

## Ingestion pipeline contract

```text
load settings
  -> resolve active embedding provider/model
  -> discover and chunk curated foods Markdown
  -> validate chunk count and IDs
  -> fit sparse embedder on all chunk texts
  -> embed all chunk texts with document instructions
  -> validate vector count/dimension/finiteness
  -> preflight Qdrant, expected schema and existing point identity
  -> create collection only when absent
  -> build deterministic dense+sparse points
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
  reset_collection: false
  vector_size: 384
  distance: cosine
  timeout: 30
  upsert_batch_size: 64
  upsert_max_retries: 1
```

Nếu `reset_collection: true`, ingestion phải từ chối chạy và hướng dẫn dùng
`vectorstore.reset` sau khi có user approval. Reset là command riêng và chỉ
xóa collection; ingestion lần sau chịu trách nhiệm tạo lại.

Trước destructive command phải có:

```text
exact target collection name
current embedding model
current dense dimension
current point count
target embedding model/dimension
completed benchmark artifact paths của collection cũ nếu là model transition
explicit user approval
```

Guard rules:

- không dùng glob, prefix-only match hoặc list-delete;
- không xóa collection khác target;
- không recreate khi Qdrant preflight không trả exact metadata;
- log action summary nhưng không log key/header;
- reset failure dừng pipeline, không tiếp tục upsert vào schema không rõ;
- confirmation string phải đúng `DELETE hue_foods_e5_small_384`;
- sau delete phải xác minh exact collection không còn tồn tại;
- `reset_collection: false` tuyệt đối không gọi delete/recreate.

Phase 4 validation không chạy live reset chỉ để chứng minh guard. Reset safety
được kiểm tra bằng mock; mọi live deletion vẫn cần approval riêng.

## Sparse storage boundary

Phase 4 lưu named sparse vectors nhưng không chứng minh native sparse retrieval. Current MVP hybrid ở Phase 5 vẫn là dense candidates + Python BM25. Benchmark ledger phải mô tả đúng retrieval path; không gọi run là dense+sparse hybrid chỉ vì points có sparse field.

## Kiến trúc đã phê duyệt

Phase 4 dùng các module chức năng nhỏ thay vì một stateful service class hoặc
module ingestion gộp lớn:

- `qdrant.py`: cache client, availability, collection create/inspect/schema validation;
- `hybrid_index.py`: validate chunks/vectors và build deterministic points;
- `upsert.py`: bounded batch upsert, transient retry và count verification;
- `reset.py`: destructive command riêng;
- `ingestion/pipeline.py`: điều phối Phase 2–4, không có deletion path.

Mỗi batch có 64 points, timeout 30 giây và tối đa một retry chỉ cho lỗi
connection/timeout. Validation, schema, bad request và data errors không retry.
Nếu batch trước đã thành công rồi batch sau thất bại, pipeline ghi safe completed
count và dừng; không rollback bằng collection deletion. Rerun chỉ tiếp tục khi
existing IDs/payload là tập con hợp lệ của expected corpus.

## Nhiệm vụ của DeepSeek Implementer

- Mock Qdrant client trong unit tests.
- Viết tests cho exact schema, existing-ID subset, vector length mismatch,
  missing ID, retry boundary, reset false/true, wrong target và point-count
  verification.
- Không dùng deprecated/destructive collection helper khi behavior không rõ; chọn API hiện hành sau local dependency inspection.
- Không ghi API key vào settings/report.
- Giữ ingestion deterministic, bounded batches và actionable errors.
- Tạo implementation report liệt kê exact collection action; redact endpoint nếu private.

## Notebook bắt buộc

`notebooks/04_qdrant_ingestion.ipynb` phải:

- import Phase 2–4 modules;
- giải thích named vectors, payload và one-active-collection lifecycle;
- Run All inspect read-only collection thật đã được ingestion tạo, kiểm tra
  schema/count/payload projection và không có fake fallback;
- không chứa reset/delete cell;
- committed outputs rỗng và `execution_count=null`.

## Tests và validation dự kiến

Mocked tests:

- client caching/config;
- create expected dense+sparse schema;
- existing matching schema không recreate;
- mismatched schema + no approval fail closed;
- `reset_collection=false` không delete;
- deterministic point IDs;
- exact payload fields;
- vector count/dimension/non-finite/sparse mismatch;
- batch boundaries `64 * 8 + 60` cho 572 points;
- connection/timeout retry đúng một lần, lỗi khác không retry;
- partial upsert và idempotent rerun;
- reset command exact-target/confirmation guards;
- batch upsert và final point count.

Commands:

```bash
cd backend
uv run python -m py_compile vectorstore/qdrant.py vectorstore/hybrid_index.py vectorstore/upsert.py vectorstore/reset.py ingestion/pipeline.py
uv run python -m pytest tests/test_qdrant_schema.py tests/test_hybrid_index.py tests/test_ingestion_pipeline.py -q --tb=short
```

Live validation có hai approval riêng: (1) khởi động pinned local Qdrant và
availability/schema preflight read-only; (2) chạy local E5 offline từ cache,
tạo collection mới và upsert 572 points. Nếu model cache không đủ và cần
download, dừng để xin approval mới.

Live evidence phải ghi:

```text
collection name
schema
embedding model/dimension
chunk count
point count
reset flag và approval evidence
```

## Security, data safety, reliability và performance

- Không log credentials, raw headers hoặc full vectors.
- Chỉ index curated answer-facing chunks.
- Upsert idempotent nhờ deterministic IDs.
- Partial upsert không được báo thành công; final count là gate.
- Upsert batch 64, `wait=True`; chỉ transient connection/timeout retry một lần.
- Collection deletion là destructive action được kiểm tra hai lớp.
- Với 572 chunks, tránh concurrency hoặc retry framework phức tạp chưa cần thiết.

## Tiêu chí phê duyệt Phase 4

- Mocked tests chứng minh schema và reset safety.
- Docker Compose pin đúng Qdrant `v1.18.3` digest và dùng storage riêng.
- Approved real preflight xác nhận Qdrant reachable.
- Collection có named `dense` và `sparse`, dense dimension đúng model.
- Collection là `hue_foods_e5_small_384`; upsert count bằng canonical chunk count 572.
- Payload không có absolute private path hoặc secret.
- `reset_collection=false` bảo vệ collection.
- Rerun idempotent và partial failure không được báo thành công.
- Notebook Run All chỉ đọc Qdrant thật, kiểm tra đúng schema/count/payload
  projection và report ghi đúng collection actions; không có live deletion.
- User report phản ánh đúng collection actions/limitations và được người dùng xác nhận cùng notebook.
- Không tuyên bố sparse query behavior chưa implement.

## Reports và cập nhật trạng thái

```text
reports/phase_4_qdrant_ingestion_implementation_report.md
reports/phase_4_qdrant_ingestion_codex_review.md
reports/user_reports/phase_4_qdrant_ingestion_user_report.md
```

Model/collection metadata và kết quả thật cần thiết nằm trong
`reports/hue_foods_rag_benchmark.md`. User report và notebook Phase 4 đã được
người dùng xác nhận.

## Quyết định đã phê duyệt

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
```

```text
Decision: Upsert dùng batch 64, timeout 30 giây và một retry chỉ cho connection/timeout; ingestion không delete, reset là exact-target command riêng.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User xác nhận batch/retry policy, separate reset command và failure policy trong Phase 4 brainstorming.
Affected scope: vectorstore/upsert.py, vectorstore/reset.py, ingestion pipeline, config và tests.
Revisit trigger: Live evidence cho thấy batch/timeout không phù hợp hoặc Qdrant client error taxonomy thay đổi.
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

Phase 4 đã hoàn thành và `approved`. Sau Phase 7, Phase 4 sẽ được review lại
trong chuỗi Phase 0 đến Phase 6 theo nguồn đối chiếu chung trong
`guides/README.md`. Shared governance hiện hành áp dụng cho mọi correction mới.
