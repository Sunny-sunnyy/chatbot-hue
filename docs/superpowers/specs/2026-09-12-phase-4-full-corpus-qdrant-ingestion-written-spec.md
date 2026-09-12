# Phase 4 — Full-corpus Qdrant ingestion

Date: `2026-09-12 +07`
Status: `approved by User 2026-09-12 +07`
Owner: Codex Reviewer
Risk: `high`

## 1. Mục tiêu

Phase 4 tạo bốn Qdrant candidate collections cho Representation A của toàn bộ
curated Hue corpus. Mỗi collection dùng một dense model đã đóng ở Phase 3,
đồng thời lưu cùng sparse representation deterministic để Phase 5 có thể triển
khai cả dense retrieval và native dense/sparse hybrid retrieval.

Phase chỉ đạt khi bốn collections đều được ingest và kiểm chứng trên cùng exact
corpus/sparse identity. Phase 4 không triển khai retrieval, benchmark, chọn
winner hoặc cutover runtime.

## 2. Dependency và nguồn sự thật

Phase 4 phụ thuộc closure Phase 2–3:

- `205` canonical source files;
- `8.460` deterministic Representation A chunks;
- corpus identity
  `0e5c059516cd942b151286cf597f785c65e642cacd1b0421124fe50fe574f223`;
- Phase 3 sparse state tại
  `data/full_corpus_builds/phase_3_sparse_state.json`;
- sparse state SHA-256
  `5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be`;
- sparse vocabulary size `5.662`, document count `8.460`, `k1=1.5`, `b=0.75`;
- bốn exact dense model contracts đã qua bounded real preflight.

Phase 4 luôn rediscover và chunk fresh từ canonical Markdown. Nó không dùng
Phase 2 preview hoặc output cũ làm runtime input. Trước mỗi dense model load,
fresh file/chunk counts, corpus identity và sparse-state identity phải khớp các
giá trị trên. Mismatch dừng trước model execution và Qdrant mutation.

## 3. Ranh giới quyền

Written Spec này chỉ khóa behavior. Nó không tự cấp quyền implementation hoặc
live execution.

Phase 4 phải có exact Implementation Plan và Review Contract được User duyệt.
Implementation sau đó có hai checkpoint trong cùng một Phase:

1. code, pure checks và read-only preflight đúng bốn targets;
2. live-write gate chỉ sau khi Reviewer kiểm preflight và User xác nhận bốn
   exact targets bằng văn bản.

Live-write approval không bao gồm:

- mutation/query/delete hai Foods collections;
- replacement hoặc cleanup collection;
- runtime cutover;
- Phase 5 retrieval, Phase 8 benchmark hoặc Representation B;
- API, frontend, generation, Golden/evaluation hoặc paid services;
- Git commit/push.

## 4. Candidate registry và collection names

Phase 4 có một explicit registry. CLI chọn bằng candidate ID; caller không được
truyền model ID, dimension hoặc arbitrary collection override.

| Candidate ID | Model/revision | Dimension | Execution | Collection |
|---|---|---:|---|---|
| `e5-small-384` | `intfloat/multilingual-e5-small@614241f622f53c4eeff9890bdc4f31cfecc418b3` | 384 | CPU/FP32, batch 8 | `hue_full_corpus_a_e5_small_384` |
| `e5-base-768` | `intfloat/multilingual-e5-base@d128750597153bb5987e10b1c3493a34e5a4502a` | 768 | CPU/FP32, batch 8 | `hue_full_corpus_a_e5_base_768` |
| `huydang-dek21-768` | `CODE4LIFEOFFICIAL/huydang-dek21-embedding@517f1af7dd04a57194f1de2990f0c6ede0a3109b` | 768 | CPU/FP32 + PyVi 0.1.1, batch 8 | `hue_full_corpus_a_huydang_dek21_768` |
| `qwen3-embedding-0.6b-1024` | `Qwen/Qwen3-Embedding-0.6B@97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3` | 1024 | CUDA/FP16/eager, batch 1 | `hue_full_corpus_a_qwen3_06b_1024` |

Model/revision/dimension/preprocessing/batch contract được lấy trực tiếp từ
`backend.embedding.full_corpus.DENSE_MODEL_SPECS`. Phase 4 không tạo bản sao
model configuration. Collection mapping thuộc Phase 4 và không sửa active
Foods `settings.yaml`.

## 5. Qdrant runtime và schema

Phase 4 dùng cùng Hue RAG Qdrant instance hiện hành:

```text
REST: http://localhost:6333
gRPC: localhost:6334
storage: ./qdrant_storage:/qdrant/storage
server: qdrant/qdrant v1.18.3
digest: sha256:0bd98fa7977f1e75694779359ca4e212822e5a71334e28421182f72f209d5286
client: qdrant-client 1.19.0 from current uv.lock
```

Không tạo Qdrant instance, ports hoặc storage thứ hai. Foods collections cùng
tồn tại trên server nhưng luôn read-only.

Mỗi candidate collection có đúng hai named vector spaces:

```text
dense:
  size: exact candidate dimension
  distance: cosine

sparse:
  SparseVectorParams()
  modifier: none/default
```

Phase 3 document sparse values đã gồm IDF nhân BM25 TF saturation, còn query
values là `1.0`. Vì vậy Qdrant `Modifier.IDF` không được bật; bật thêm sẽ phá
contract sparse dot product bằng BM25 score.

Phase 4 không override Qdrant default storage/index configuration: không
quantization, explicit on-disk placement, custom HNSW hoặc payload index. Các
tuning này chỉ được mở lại khi evidence benchmark/resource cho thấy nhu cầu.

## 6. Point contract

Mọi collection có cùng exact set `8.460` points; pipeline tạo chúng theo cùng
canonical chunk order nhưng không phụ thuộc thứ tự Qdrant trả về. Point ID dùng
contract hiện hành:

```python
uuid.uuid5(uuid.NAMESPACE_URL, f"hue-rag:{chunk_id}")
```

Point ID không chứa model hoặc representation; collection boundary sở hữu
vector-space identity. Original `chunk_id` không lặp trong payload vì point ID
và source locator đã có nguồn chuẩn riêng.

Mỗi point có:

```text
id: deterministic UUID5
vector:
  dense: finite unit vector with the candidate's exact dimension
  sparse:
    indices: strictly increasing Phase 3 vocabulary indices
    values: aligned finite Phase 3 document weights
payload:
  search_text: string
  source: canonical relative POSIX path
  title: string
  heading_path: list[string]
  evidence_parts: list[{role: body|header|condition, start: int, end: int, text: string}]
```

Payload có đúng năm top-level fields trên. Không thêm domain/subdomain,
chunk/model/build IDs, source hash, token count, timestamp, version, score,
absolute path hoặc vector metadata.

Trước upsert, implementation phải kiểm toàn bộ:

- chunk IDs unique và point IDs unique;
- dense row count bằng chunk count;
- mỗi dense vector đúng dimension, finite và L2 norm xấp xỉ `1` với
  `rel_tol=1e-3`, `abs_tol=1e-3`, đúng validator Phase 3 và sai số FP16 đã được
  chấp nhận;
- sparse indices/values aligned, indices unique/tăng dần và values finite;
- point/payload count đúng `8.460`;
- payload field set và values khớp exact `FullCorpusChunk`.

Phase 4 load sparse state đã đóng; không refit vocabulary và không lưu toàn bộ
sparse document vectors thành artifact trung gian.

## 7. Fresh-target contract

Preflight xử lý target theo ba trạng thái:

- absent: hợp lệ để build; collection chỉ được tạo sau dense validation;
- existing empty: chỉ hợp lệ khi exact schema khớp và final build record chưa
  tồn tại;
- existing non-empty: fail closed trước dense encoding và mọi write.

Final build-record path cũng phải chưa tồn tại. Ingestion không có `--replace`,
delete, reset, resume, reconcile hoặc automatic target suffix. Không tự xóa
stale/foreign points.

Vì dense encoding tạo một khoảng thời gian giữa preflight và write, pipeline
phải recheck target state, exact schema và build-record absence ngay trước
create/upsert. Nếu observed state đã đổi, candidate fail closed; không coi một
target do tiến trình khác vừa tạo là target của run hiện tại.

Nếu một batch đã ghi rồi batch sau lỗi:

- giữ failed target nguyên trạng;
- không ghi final build record;
- report exact target, completed batch/point count và observed error;
- dừng candidate sequence;
- rerun bị non-empty guard chặn.

Recovery chỉ diễn ra sau independent review và exact User approval để guarded
delete failed target, verify absent rồi chạy lại cùng semantic name. Initial
four-target live approval không cấp sẵn recovery deletion.

## 8. Per-candidate data flow và memory contract

Bốn candidates chạy tuần tự theo registry order. Mỗi candidate:

```text
fresh discover/chunk
-> verify corpus + sparse state identity
-> read-only Qdrant/build-record preflight
-> load exact dense model
-> encode all 8.460 chunks to one NumPy matrix
-> validate complete matrix
-> recheck unchanged target/build-record state
-> create collection when absent
-> build dense+sparse PointStruct objects for one batch of 64
-> upsert wait=True
-> repeat until complete
-> completion verification
-> atomic final build-record write
-> close/unload model
```

Không tạo toàn bộ Python vector lists hoặc `PointStruct` graph cùng lúc. Chỉ
dense NumPy matrix của một candidate tồn tại xuyên ingestion; point objects và
sparse vectors chỉ tồn tại theo batch 64. Không persist dense matrix và không
gọi `.tolist()` trên toàn matrix.

`FullCorpusDenseRunner.embed_documents()` hiện hữu của Phase 3 trả về nested
Python lists. Phase 4 cần một dedicated NumPy-returning full-corpus path dùng
cùng exact preprocessing/model/runtime/validation contract, đồng thời giữ
nguyên behavior của API Phase 3 hiện hữu. Chỉ từng row/batch được chuyển sang
Qdrant wire values khi dựng tối đa 64 points.

Model phải được close trong `finally`. Qwen giữ exact CUDA/FP16/eager/native
1024D contract; không CPU fallback, quantization, auto batch reduction hoặc
alternate dimension. Provider/model/resource failure được báo đúng và dừng.

RAM WSL2 hiện quan sát khoảng `15.51 GiB`, trong đó khoảng `12.97 GiB` available
tại design time. Dense matrix lớn nhất khoảng `33 MiB` raw float32. Đây là
observed design evidence, không phải hard runtime invariant; live preflight vẫn
phải báo RAM/swap/disk/GPU state và mọi OOM phải giữ nguyên outcome.

## 9. Completion verification

Sau upsert cuối và trước build-record write, mỗi collection phải qua:

1. exact dense/sparse schema validation;
2. exact point count `8.460`;
3. scroll toàn bộ points không lấy vectors để đối chiếu exact expected point-ID
   set và exact five-field payload values;
4. retrieve vectors cho exact deterministic 12-point sample đã ghi trong Phase
   3 preflight artifact;
5. với sample, kiểm có cả `dense`/`sparse`, dense dimension/finite/norm và sparse
   indices/values structure;
6. read-only rerun preflight trên completed target phải bị non-empty guard chặn
   trước model load/write.

Không đọc lại toàn bộ dense/sparse matrices từ Qdrant. Toàn bộ vectors đã được
validate trước write; sampled readback chứng minh storage path mà không lặp
hàng trăm MB dữ liệu.

## 10. Build record contract

Mỗi collection có đúng một final-only record:

```text
data/full_corpus_builds/<collection_name>.json
```

Record được serialize deterministic và ghi atomically qua adjacent temporary
file rồi replace. Nó chỉ xuất hiện sau completion verification; không có
`building`, `failed` hoặc resume state.

Required logical content. Mẫu cụ thể dưới đây dùng candidate `e5-small-384`;
`sources` trong record thật là mapping đủ đúng `205` entries, không phải giá trị
mẫu rút gọn:

```text
schema_version: phase_4_full_corpus_build:v1
status: complete
collection_name: hue_full_corpus_a_e5_small_384
representation: A
corpus:
  identity: 0e5c059516cd942b151286cf597f785c65e642cacd1b0421124fe50fe574f223
  file_count: 205
  chunk_count: 8460
  sources: map[canonical_relative_posix_path, lf_text_sha256] with 205 entries
dense:
  candidate_id: e5-small-384
  model_id: intfloat/multilingual-e5-small
  revision: 614241f622f53c4eeff9890bdc4f31cfecc418b3
  dimension: 384
sparse:
  schema_version: phase_3_sparse_state:v1
  state_sha256: 5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be
  vocabulary_size: 5662
qdrant:
  dense_vector_name: dense
  sparse_vector_name: sparse
  distance: cosine
  point_count: 8460
```

Mỗi record tự chứa 205 relative source paths và LF hashes để startup Phase 6 có
thể xác định added/deleted/changed sources và yêu cầu reingest. Không tạo shared
registry/manifest/checksum package. Record không chứa timestamp, run ID,
endpoint, secret, vectors, full payload hoặc absolute path.

## 11. Component ownership

Thiết kế dự kiến:

- `backend/ingestion/full_corpus_pipeline.py`: candidate mapping, CLI và direct
  orchestration; không retrieval/delete;
- `backend/embedding/full_corpus.py`: existing exact dense contracts/runners;
- `backend/embedding/sparse.py`: existing sparse-state load/document encoding;
- `backend/vectorstore/qdrant.py`: full-corpus schema, exact validation và
  fresh-target inspection bên cạnh Foods behavior;
- `backend/vectorstore/points.py`: batch full-corpus point construction bên
  cạnh Foods behavior;
- `backend/vectorstore/upsert.py`: bounded exact-target writes và verification;
- `backend/ingestion/source_state.py`: source hashes/freshness và final record
  serialization;
- `notebooks/04_qdrant_ingestion.ipynb`: read-only learning/inspection path.

Plan có thể điều chỉnh tên hàm/helper nội bộ nếu responsibility và public
behavior trên không đổi. Không tạo service class, provider adapter, collection
manager, registry framework hoặc config hierarchy mới.

## 12. Test và live evidence

Trước live gate chỉ dùng pure deterministic inputs để kiểm behavior thuần:

- registry uniqueness và không trùng Foods names;
- dense+sparse schema construction/validation;
- deterministic point IDs và exact payload;
- dense/sparse shape/value guards;
- fresh-target decision logic;
- deterministic build-record serialization và freshness comparison.

Không dùng fake/mock/stub client làm Qdrant integration evidence, không dùng
embedded Qdrant và không tạo collection chỉ để test deletion/schema failure.

Live candidate builds là integration evidence thật cho availability, schema
creation, dense+sparse point writes, batch behavior và completion checks. Report
phải ghi exact commands, targets, collection actions, model/runtime/resource
observations, counts, schema, build-record paths, failures/skips và giới hạn.

Phase 4 chỉ kiểm index contract. Phase 5 phải có real integration evidence riêng
cho dense retrieval, dense + BM25-local baseline và native dense/sparse + RRF.
Phase 8 mới đánh giá chất lượng trên canonical full-corpus Golden; Phase 4
không dùng technical smoke để tuyên bố retrieval quality.

## 13. Notebook 04

Notebook 04 được cập nhật thành read-only inspector:

- giải thích bốn isolated candidates và named dense/sparse schema;
- đọc candidate registry và final build records;
- inspect schema, point count, payload projection và deterministic sample trên
  Qdrant thật;
- không load dense model, encode corpus, create/upsert/delete/reset collection;
- không có fake fallback;
- canonical outputs rỗng và execution counts `null`.

Temporary Run All chỉ sau live builds và chỉ query exact full-corpus candidate
collections read-only. Foods không được query.

## 14. Phase acceptance

Phase 4 technical verdict chỉ có thể đạt `ready_for_user_confirmation` khi:

1. code/diff đúng scope và Foods runtime/config/collections không đổi;
2. fresh source/chunk/corpus/sparse identities khớp closed Phase 2–3 evidence;
3. bốn exact model contracts chạy full-corpus không truncate/fallback;
4. bốn exact target collections có schema `dense` + `sparse` đã khóa;
5. mỗi target có đúng `8.460` expected points và exact five-field payloads;
6. completion verification và deterministic 12-point vector readback đạt;
7. bốn final build records atomic, complete và cùng corpus/sparse identity;
8. non-empty guard được quan sát fail trước model/write;
9. Notebook 04 temporary Run All read-only đạt và canonical notebook sạch;
10. reports phân biệt fresh results, reused evidence, failed/skipped/not
    verified; không gọi partial build là PASS;
11. independent Reviewer review không còn blocker/major;
12. User xác nhận closure Phase 4.

Nếu chỉ một đến ba candidates hoàn tất, records của chúng vẫn là evidence hợp
lệ nhưng Phase 4 giữ trạng thái incomplete. Không hạ Qwen thành optional.

## 15. Explicit exclusions và next boundary

Phase 4 không:

- triển khai dense/sparse retrieval, BM25-local, RRF hoặc reranker;
- chọn default/winner hoặc chạy quality metrics;
- tạo Representation B;
- sửa active Foods settings, data, code path hoặc collection contents;
- cutover, replace hoặc cleanup bất kỳ collection nào;
- thêm retry/resume/rollback/alias/manifest/collection registry framework;
- thêm quantization, on-disk tuning, custom HNSW hoặc payload indexes;
- chạy API/frontend/generation/Golden/evaluation/paid services;
- commit/push khi chưa có exact Git authorization.

Sau User closure Phase 4, exact next boundary là Reviewer design gate cho Phase
5 retrieval/fusion/reranker. Phase 5 dùng bốn completed Phase 4 indexes làm
dependency và phải kiểm cả dense retrieval lẫn native dense/sparse retrieval.

## 16. Design decisions đã được User duyệt

Trong brainstorming ngày `2026-09-12 +07`, User đã duyệt:

- semantic fixed names cho bốn Representation A collections;
- one final-only atomic build record per collection;
- fresh-target absent/empty only, không replacement/reconcile trong ingestion;
- giữ Foods collections read-only tới post-winner cutover cleanup gate;
- sequential one-candidate execution và stop on first failure;
- một exact live-write approval cho cả bốn targets;
- full ID/payload verification cùng deterministic sampled vector readback;
- không fake/embedded Qdrant test collections;
- static candidate registry tách active Foods config;
- sparse indexing ở Phase 4, sparse retrieval/fusion ở Phase 5;
- fresh canonical regeneration và exact Phase 3 identity gate;
- one NumPy dense matrix per candidate, batch-64 point construction/upsert;
- Phase PASS chỉ khi đủ bốn collections;
- cùng Hue RAG Qdrant instance, isolated collection names;
- Qdrant defaults, không resource/index tuning trước evidence;
- Notebook 04 read-only;
- no Qdrant IDF modifier;
- exact-approval recovery cho failed partial target.
