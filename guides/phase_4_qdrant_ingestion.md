# Phase 4: Qdrant ingestion và hybrid points

## Mục tiêu và giá trị cho người dùng

Phase 4 đưa canonical food chunks cùng dense/sparse representations vào một active Qdrant collection có schema kiểm chứng được. Kết quả là một index tái lập, an toàn khi reset và sẵn sàng cho cả ba retrieval profiles.

## Trạng thái

```text
Status: not_ready
Brainstorming level: Level 2 - standard
Owner: Codex Reviewer
Implementer: DeepSeek after Phase 3 approval and Phase 4 readiness
```

## Dependency

- Phase 3 phải được người dùng xác nhận và có status `approved`.
- Dense model ID, actual dimension, normalization và sparse state contract đã khóa.
- Qdrant local availability chưa được giả định; phải preflight.
- User approval bắt buộc trước collection deletion/reset.

## Chức năng phải tạo

- Tạo/cache Qdrant client theo config.
- Kiểm tra Qdrant availability và collection metadata.
- Tạo collection với named dense/sparse vector schema.
- Build deterministic Qdrant points từ chunks.
- Batch upsert và kiểm tra point count.
- Ingestion pipeline kết nối Phase 2–4.
- Reset guard fail closed và chỉ xóa exact expected collection.
- Notebook ingestion an toàn, real mode opt-in.

## Files dự kiến

```text
backend/vectorstore/qdrant.py
backend/vectorstore/hybrid_index.py
backend/vectorstore/upsert.py
backend/vectorstore/reset.py
backend/ingestion/pipeline.py
backend/tests/test_qdrant_schema.py
backend/tests/test_hybrid_index.py
backend/tests/test_ingestion_pipeline.py
notebooks/04_qdrant_ingestion.ipynb
```

File list chỉ thay đổi sau brainstorming nếu có lý do cụ thể về ownership; không copy module thừa từ `llm_rag`.

## Active collection invariant

- Hue Foods chỉ có một active collection tại một thời điểm.
- Một embedding model dùng cùng collection cho `dense_only`, `hybrid_no_rerank` và `hybrid_rerank`.
- Khi đổi embedding model/dimension: lưu artifacts của model cũ, xin user approval, xóa exact collection, tạo lại với model mới, reindex toàn corpus.
- Không giữ nhiều experiment collections trong MVP.
- Collection name phải deterministic và phản ánh Hue Foods cùng embedding identity đủ để ngăn nhầm schema. Exact naming được chốt trong brainstorming.

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
- payload fields/version nếu guide quyết định có schema version;
- embedding model identity được ghi trong collection metadata/config evidence.

Nếu existing schema khác expected schema và reset chưa được phép, pipeline phải dừng với actionable error; không tự recreate.

## Point contract

Mỗi Qdrant point:

```python
{
    "id": "deterministic Qdrant-compatible ID derived from chunk_id",
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

Point ID không được random fallback khi `chunk_id` thiếu. Missing/invalid `chunk_id` phải fail trước upsert. Nếu Qdrant client version không nhận arbitrary string IDs, dùng deterministic UUID5 từ `chunk_id` và giữ original `chunk_id` trong payload.

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
  -> preflight Qdrant and expected collection schema
  -> guarded create/reset
  -> build deterministic dense+sparse points
  -> batch upsert
  -> verify collection schema and exact point count
  -> emit non-sensitive summary
```

Expected baseline point count là 572 khi curated corpus/chunking không đổi. Nếu count khác, implementation report phải giải thích input diff; không cập nhật expected count âm thầm.

## Reset và deletion safety

`reset_collection: true` chỉ là điều kiện cần, không phải quyền đủ để xóa. Trước destructive call phải có:

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
- `reset_collection: false` tuyệt đối không gọi delete/recreate.

## Sparse storage boundary

Phase 4 lưu named sparse vectors nhưng không chứng minh native sparse retrieval. Current MVP hybrid ở Phase 5 vẫn là dense candidates + Python BM25. Benchmark ledger phải mô tả đúng retrieval path; không gọi run là dense+sparse hybrid chỉ vì points có sparse field.

## Brainstorming bắt buộc trước implementation

Codex phải xác nhận với người dùng:

1. Qdrant chạy qua Docker Desktop/WSL, local process hay một endpoint khác đã được user đặt trong scope.
2. Exact active collection naming convention có chứa embedding slug/dimension hay dùng fixed name cùng metadata guard.
3. Qdrant client version và deterministic point-ID format được hỗ trợ.
4. Batch size, timeout và retry policy phù hợp 572 chunks.
5. Cơ chế user approval cho reset trong CLI/config: confirmation flag hay separate command.

Collection đang tồn tại chỉ được inspect read-only trong preflight; không reset khi brainstorming chưa chốt.

## Nhiệm vụ của DeepSeek Implementer

- Mock Qdrant client trong unit tests.
- Viết tests cho exact schema, vector length mismatch, missing ID, reset false, wrong target và point-count verification.
- Không dùng deprecated/destructive collection helper khi behavior không rõ; chọn API hiện hành sau local dependency inspection.
- Không ghi API key vào settings/report.
- Giữ ingestion deterministic, bounded batches và actionable errors.
- Tạo implementation report liệt kê exact collection action; redact endpoint nếu private.

## Notebook bắt buộc

`notebooks/04_qdrant_ingestion.ipynb` phải:

- import Phase 2–4 modules;
- giải thích named vectors, payload và one-active-collection lifecycle;
- safe default chỉ build/inspect sample point hoặc mock client;
- real-mode cells có guard rõ cho Qdrant và reset;
- không chứa auto-delete cell mặc định;
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
- vector count/dimension mismatch;
- batch upsert và final point count.

Commands:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile vectorstore/qdrant.py vectorstore/hybrid_index.py vectorstore/upsert.py vectorstore/reset.py ingestion/pipeline.py
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_qdrant_schema.py tests/test_hybrid_index.py tests/test_ingestion_pipeline.py -q --tb=short
```

Live local Qdrant validation chỉ chạy sau user approval và phải ghi:

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
- Collection deletion là destructive action được kiểm tra hai lớp.
- Với 572 chunks, tránh concurrency hoặc retry framework phức tạp chưa cần thiết.

## Tiêu chí phê duyệt Phase 4

- Mocked tests chứng minh schema và reset safety.
- Approved real preflight xác nhận Qdrant reachable.
- Collection có named `dense` và `sparse`, dense dimension đúng model.
- Upsert count bằng canonical chunk count.
- Payload không có absolute private path hoặc secret.
- `reset_collection=false` bảo vệ collection.
- Notebook an toàn và report có destructive-action evidence.
- User report phản ánh đúng collection actions/limitations và được người dùng xác nhận cùng notebook.
- Không tuyên bố sparse query behavior chưa implement.

## Reports và cập nhật trạng thái

```text
reports/phase_4_qdrant_ingestion_implementation_report.md
reports/phase_4_qdrant_ingestion_codex_review.md
reports/user_reports/phase_4_qdrant_ingestion_user_report.md
```

Model/collection metadata và ingestion run summary được nối vào `reports/hue_foods_rag_benchmark.md`. Sau technical review đạt, Codex tạo user report `pending`; chỉ cập nhật `Project_Status.md` sau khi người dùng xác nhận notebook/report.

## Quyết định đã phê duyệt trước brainstorming

```text
Decision: Dùng 572 canonical chunks và giới hạn 400 ký tự cho nội dung thường; bảng Markdown là ngoại lệ được giữ nguyên.
Approved by: User
Approval date +07: 2026-08-12
Evidence: Phase 2 đã approved và user xác nhận sửa contract cũ trước brainstorming Phase 4.
Affected scope: Phase 4 point count, batch planning, ingestion validation và benchmark ledger.
Revisit trigger: Curated corpus hoặc Phase 2 chunking contract được user phê duyệt thay đổi.
```

## Bước tiếp theo

Sau Phase 4 approval, Phase 5 brainstorm candidate depth, normalization/fusion, reranker behavior, fallback và context limits.
