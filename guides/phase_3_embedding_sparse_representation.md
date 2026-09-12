# Phase 3 — Full-corpus dense embedding và sparse representation

> **Canonical Phase 3 closure — 2026-09-12:** User đã xác nhận Phase 3 sau
> implementation, hai correction và independent final review `PASS`. Fresh
> evidence: 205 files/8.460 chunks, sparse deterministic và bốn bounded dense
> candidates PASS; Qwen chạy GTX 1650/CUDA FP16/eager/native 1024D.

## Trạng thái

```text
Status: approved/completed — User-confirmed on 2026-09-12 +07
Owner: Codex Reviewer
Implementer: DeepSeek
Foods baseline: completed and User-confirmed on 2026-08-25 +07
Full-corpus Phase 3 design: approved by User on 2026-09-12 +07
Full-corpus Phase 3 implementation: authorized only through CURRENT_HANDOFF.md
Git authorization: none
Sub-agent authorization: user-standing; Implementer decides under workflow
```

Canonical full-corpus package:

```text
docs/superpowers/specs/2026-09-12-phase-3-full-corpus-embedding-sparse-written-spec.md
docs/superpowers/plans/2026-09-12-phase-3-full-corpus-embedding-sparse-implementation-plan.md
```

Review Contract nằm trong implementation plan. Guide này là entrypoint
canonical của Phase 3; spec khóa behavior, plan khóa paths/commands/quyền và
Review Contract khóa evidence cùng independent review.

Closure evidence:

```text
reports/full_corpus_phase_3_embedding_sparse_correction_2_codex_review_2026_09_12.md
reports/user_reports/full_corpus_phase_3_embedding_sparse_user_report_2026_09_12.md
```

## Full-corpus Phase 3 target đã duyệt

Phase 3 nhận fresh ordered Representation A chunks từ Phase 2. Nó tokenize toàn
corpus bằng exact native preprocessing của bốn candidates nhưng chỉ dense-encode
một mẫu deterministic 10–15 chunks. Dense encoding toàn corpus và mọi Qdrant
schema/write thuộc Phase 4.

| Candidate | Exact revision | Dimension | Execution | Input contract |
|---|---|---:|---|---|
| `intfloat/multilingual-e5-small` | `614241f622f53c4eeff9890bdc4f31cfecc418b3` | 384 | CPU/FP32 | document `passage: `, query `query: ` |
| `intfloat/multilingual-e5-base` | `d128750597153bb5987e10b1c3493a34e5a4502a` | 768 | CPU/FP32 | document `passage: `, query `query: ` |
| `CODE4LIFEOFFICIAL/huydang-dek21-embedding` | `517f1af7dd04a57194f1de2990f0c6ede0a3109b` | 768 | CPU/FP32 | PyVi 0.1.1 cho document/query |
| `Qwen/Qwen3-Embedding-0.6B` | `97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3` | native 1024 | GTX 1650/CUDA FP16, batch 1 | raw Representation A document; custom English query instruction |

Qwen query input phải đúng:

```text
Instruct: Given a Vietnamese question about Hue culture, heritage,
festivals, performing arts, food, and travel, retrieve relevant
Vietnamese passages that answer the question.
Query: {question}
```

Không dùng instruction cho Qwen documents. Không dùng CPU fallback,
quantization, FlashAttention, `device_map=auto`, `truncate_dim`, slicing/PCA,
batch auto-shrink hoặc revision khác. Phase 3 chỉ PASS khi Qwen chạy thật trên
GTX 1650 bằng CUDA FP16, eager attention, batch 1 và output 1024D normalized.

### Representation A và dense evidence

Input document giữ nguyên `FullCorpusChunk.search_text`:

```text
title
heading path nối bằng " > " khi có
evidence parts theo thứ tự nguồn
```

Không thêm `Tiêu đề:`/`Nội dung:` hoặc renderer thứ hai. Mẫu dense phải phủ cả
bảy P7, paragraph/list/table/condition và per-model longest chunks; nếu coverage
không nằm trong 10–15 chunks thì fail closed. Mọi model output phải đúng order,
count, dimension, finite và L2 norm xấp xỉ 1. Cosine/timing chỉ là diagnostic,
không có quality threshold hoặc winner trong Phase 3.

### Sparse state

Sparse state fit một lần trên ordered full-corpus `search_text` và dùng chung
cho Phase 4 document vectors cùng Phase 5 query vectors:

```text
tokenizer = backend.scoring.bm25.tokenize
k1 = 1.5
b = 0.75
vocabulary = mọi corpus term sắp lexicographic, index từ 0
idf(term) = ln(1 + (N - df + 0.5) / (df + 0.5))
document value = idf × BM25 TF saturation
known query value = 1.0, một lần mỗi term
```

Dot product sparse phải bằng BM25 hiện hành. Artifact chỉ lưu corpus identity,
counts, constants, tokenizer, ordered vocabulary và aligned IDF; không lưu
8.460 document vectors hoặc lặp metadata ở mỗi point. Cùng exact input/config
phải tạo byte-identical artifact.

### Artifacts, Notebook và failure

Generated sparse state:

```text
data/full_corpus_builds/phase_3_sparse_state.json
```

Versioned summary evidence:

```text
reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json
```

JSON không chứa dense vectors, corpus text, secrets hoặc absolute cache path.
`notebooks/03_embedding_models.ipynb` gọi backend Phase 3 trên bounded sample;
canonical outputs rỗng/execution counts null, Run All chỉ trên copy `/tmp`.

GPU unavailable, Qwen OOM, wrong device/dtype/dimension, snapshot mismatch,
tokenizer over-limit hoặc Phase 2 identity mismatch đều giữ trạng thái observed
và block/fail Phase 3. Không có fallback. Nếu Windows passthrough đã hoạt động
nhưng locked Torch không dùng CUDA, Implementer báo exact versions/evidence và
xin User duyệt một lệnh `uv` cụ thể trước dependency change.

### Quyền và handoff

Implementer được sửa đúng code/tests/notebook/artifacts/report trong approved
plan và tải bốn public snapshots ở exact revisions sau khi CUDA readiness đạt.
Implementer được tự quyết dùng sub-agent theo standing User authorization trong
`session_prompt/IMPLEMENTER_WORKFLOW.md`; mọi sub-agent giữ nguyên exact scope,
allowed paths, stop conditions và không có quyền Git rộng hơn task cha. User tự
thực hiện Windows/Administrator actions. Không Git write, Qdrant, dense
full-corpus encoding, Foods mutation, Golden/evaluation, paid API hoặc Phase 4
implementation. Sau self-review, Implementer bàn giao Reviewer; chỉ User mới
xác nhận Phase 3 closure và mở design Phase 4.

## Foods baseline lịch sử đã đóng

Simplicity design được người dùng phê duyệt ngày `2026-08-24 +07`:

```text
docs/superpowers/specs/2026-08-24-phase-3-embedding-sparse-representation-simplicity-design.md
```

Implementation plan:

```text
docs/superpowers/plans/2026-08-24-phase-3-embedding-sparse-representation-simplicity-implementation.md
```

Guide này thay contract lịch sử đã dùng provider abstraction, OpenRouter
adapter, batching hai tầng và mock-only tests. Implementation mới phải theo
thiết kế simplicity đã duyệt và bằng chứng chạy thật.

> **Downstream update `2026-08-25 +07`:** Coordinated simplicity review Phase
> 4–5 đã xóa `SparseEmbedder` và stored sparse vectors khỏi target code và
> dense-only candidate. Các đoạn về sparse TF-IDF bên dưới ghi acceptance lịch
> sử tại thời điểm Phase 3 được review, không phải runtime requirement hiện
> hành. Dense E5 contract của Phase 3 vẫn được giữ.

## Foods history — mục tiêu

Phase 3 biến 572 canonical food chunks thành:

- dense vectors bằng local `intfloat/multilingual-e5-small` để
  `DenseRetriever` truy vấn ngữ nghĩa;
- sparse TF-IDF vectors deterministic để giữ compatibility với Phase 4 hiện
  vẫn lưu named sparse vector.

Code phải đủ chi tiết để người học theo được data flow, nhưng không giữ
abstraction, validation hoặc provider code cho nhu cầu chưa tồn tại.

## Foods history — dependency và ranh giới

- Phase 1–2 đã `approved`.
- Input là output ổn định của `chunk_foods_markdown()` gồm 572 chunks.
- Local E5 đã có trong cache và chạy trên CPU.
- Active collection `hue_foods_e5_small_384` luôn read-only.
- Existing tests chỉ được mutate collection cô lập có prefix
  `hue_rag_live_test_` và phải cleanup rõ ràng.

Trong scope:

```text
backend/embedding/base.py                         # delete
backend/embedding/batch_embed.py                  # delete
backend/embedding/openrouter_embedder.py          # delete
backend/embedding/embedder.py
backend/embedding/sparse_embedder.py
backend/config/settings.yaml
backend/ingestion/pipeline.py                     # compatibility wiring
backend/core/startup.py                           # compatibility wiring
backend/tests/conftest.py
backend/tests/test_embedder.py
backend/tests/test_sparse_embedder.py
backend/tests/test_startup.py                     # stale class name only
notebooks/03_embedding_models.ipynb
```

Ngoài scope:

- thay Qdrant schema hoặc active collection;
- bỏ stored sparse vectors;
- đổi BM25, fusion, candidate depth hoặc reranker;
- chọn retrieval profile/model winner;
- OpenRouter embedding implementation hoặc paid run;
- Phase 7 evaluation rerun khi real verification xác nhận behavior được giữ.

## Foods history — local E5 baseline

```text
Model: intfloat/multilingual-e5-small
Execution: local CPU
Dimension: 384
Batch size: 64
Document prefix: passage:
Query prefix: query:
```

Chỉ giữ một concrete class:

```python
class E5Embedder:
    model_id: str
    dimension: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...
    def embed_query(self, query: str) -> list[float]: ...
```

Không giữ `BaseEmbedder`, `EmbeddingError`, provider factory/protocol hoặc
compatibility wrapper.

### Model lifecycle

Model được lazy-load vào chính `E5Embedder` instance:

- API startup tạo một instance, warm-up thật và giữ nó trong
  `DenseRetriever` cho mọi request;
- ingestion là process riêng và dùng một instance cho toàn bộ corpus;
- health endpoint chỉ đọc readiness đã cache ở startup.

Không cần module-global singleton hoặc `lru_cache`.

### Dense data flow

Document path:

```text
572 ordered chunk texts
-> prepend passage:
-> SentenceTransformer.encode(batch_size=64, normalize_embeddings=True)
-> 572 ordered vectors x 384 dimensions
```

Query path:

```text
non-empty query
-> prepend query:
-> same loaded model
-> one normalized 384-dimensional vector
-> DenseRetriever
```

SentenceTransformer xử lý batching trực tiếp. Xóa outer `embed_in_batches()`;
không chia cùng một workload ở hai tầng.

### Validation tối thiểu

Fail bằng `ValueError` rõ ràng khi:

- query không phải non-empty string;
- dimension thật của model khác config;
- số output vectors khác số input texts;
- một output vector sai dimension.

Không normalize lần hai bằng NumPy. Phase 4 tiếp tục kiểm tra finite values tại
index boundary. Không pad/truncate, silent fallback hoặc tự sửa config.

## Foods history — cấu hình

Phase 3 chỉ giữ cấu hình được local runtime sử dụng:

```yaml
embedding:
  model: intfloat/multilingual-e5-small
  vector_size: 384
  device: cpu
  batch_size: 64
```

Xóa:

```text
embedding.provider
embedding.remote
embedding.document_prefix
embedding.query_prefix
```

Hai E5 prefixes thuộc concrete `E5Embedder`. Phase 8 sẽ thiết kế provider và
instruction config mới dựa trên exact candidate/API thật. OpenAI configuration
cho answer generation là subsystem khác và không thay đổi ở Phase 3.

## Foods history — sparse representation

Giữ deterministic TF-IDF contract hiện tại:

```text
lowercase Unicode text
-> replace non-word/non-space characters with spaces
-> split on whitespace
-> ordered vocabulary + document frequency
-> term frequency x IDF
-> aligned indices/values
```

```text
idf(term) = log((num_documents + 1) / (document_frequency + 1)) + 1
value = term_frequency * idf(term)
```

Invariants:

- vocabulary index theo first occurrence trong ordered corpus;
- DF đếm một token tối đa một lần trong mỗi document;
- `fit()` lần hai reset toàn bộ state;
- cùng corpus/order tạo cùng vectors;
- unknown và empty text trả empty indices/values;
- `encode()` trước fit bị reject;
- indices/values aligned và values positive finite.

Runtime code dùng type hints, tên biến đầy đủ, docstring ngắn và comment giải
thích lý do ở chỗ không hiển nhiên. Ví dụ tính tay dài nằm trong Notebook 03,
không nhồi vào source.

Tại thời điểm Phase 3 được duyệt, BM25 chỉ import chung `tokenize()` và không
phụ thuộc class `SparseEmbedder`; class này được giữ tạm cho Phase 4. Coordinated
simplicity review Phase 4–5 sau đó đã chuyển tokenizer sang BM25 ownership và
xóa `SparseEmbedder` cùng stored sparse schema khỏi target code.

## Foods history — retrieval compatibility

Hue RAG đã có cả hai retriever:

```text
E5Embedder
-> DenseRetriever
-> optional HybridRetriever with Python BM25
-> optional CrossEncoder
```

`HybridRetriever` composition trên `DenseRetriever`, không tự embed query lần
nữa. Nó chỉ chấm BM25 trên dense candidate set và không query named sparse
vector.

Ba profile giữ nguyên:

```yaml
profiles:
  dense_only:
    retrieval_mode: dense
    use_bm25: false
    use_reranker: false
  hybrid_no_rerank:
    retrieval_mode: hybrid
    use_bm25: true
    use_reranker: false
  hybrid_rerank:
    retrieval_mode: hybrid
    use_bm25: true
    use_reranker: true
```

`dense_only` tiếp tục là active MVP. Existing benchmark không chứng minh hybrid
luôn tốt hơn; Phase 8 mới so sánh quality, latency, reliability và cost rồi để
user chọn winner.

## Foods history — test contract

Focused tests bảo vệ distinct behavior, không chạy theo số lượng.

Dense tests dùng E5 thật:

- empty documents và invalid query;
- vector count/order/dimension/norm;
- query/document roles khác nhau;
- wrong configured dimension fail với model thật.

Sparse tests dùng corpus nhỏ tính tay được:

- Vietnamese tokenization;
- known TF-IDF/DF;
- deterministic output;
- repeated-fit reset;
- empty/unknown text;
- encode-before-fit rejection.

Xóa test cho OpenRouter adapter, outer batching, custom prefixes và shared
process cache. Không dùng mock/fake SentenceTransformer, HTTP hoặc provider làm
evidence.

Existing ingestion/startup/hybrid-index tests chỉ là downstream wiring smoke.
Full backend suite chạy một lần trước handoff vì Phase 3 API được nhiều phase
dùng. Test pass không thay Notebook và live query.

## Foods history — Notebook 03

`notebooks/03_embedding_models.ipynb` phải:

- giải thích dense E5 và sparse TF-IDF bằng tiếng Việt;
- import public Phase 2/3 APIs, không copy algorithms;
- embed toàn bộ 572 chunks thật trên CPU, batch size 64;
- hiển thị model, shape `572 x 384`, norm và elapsed time;
- minh họa query/document roles;
- giải thích sparse bằng mini corpus và public output;
- không truy cập private state;
- không chứa OpenRouter code;
- giữ repository outputs rỗng và execution counts null.

Reviewer chạy Run All trên temporary copy. Elapsed time là observed result,
không phải flaky pass threshold.

## Foods history — real verification

```text
compile affected modules
-> focused real E5/sparse tests
-> Notebook 03 over 572 real chunks
-> active Qdrant count read-only = 572
-> one real query through E5 and active collection
-> affected ingestion/startup/hybrid-index tests
-> one final full backend suite
-> diff/deleted-import/config audit
```

Active collection không được mutate. Test collection mutation chỉ hợp lệ khi
tên bắt đầu bằng `hue_rag_live_test_`, existing guards còn nguyên và cleanup
được báo cáo.

Không cần exact float hash. Batching có thể tạo sai số float nhỏ; compatibility
được chứng minh bằng same model/dimension/instructions và successful real query.

## Foods history — Phase 8 handoff

OpenRouter embedding vẫn là roadmap thật nhưng không có code dự phòng ở Phase
3. Khi Phase 8 được mở, phải xác minh lại:

- actual embeddings API và response schema;
- exact catalog model ID;
- dimension/instruction/input limits/batching;
- pricing, rate limit, timeout và reliability;
- collection/index transition cho vector space mới.

Phase 8 dùng API/model/data thật và so sánh local E5 với approved remote
candidates trên ba retrieval profiles. Không mock/fake, silent fallback hoặc
leaderboard-only winner.

## Foods history — acceptance

Technical review chỉ đạt khi:

1. ba module thừa đã xóa, không có wrapper thay thế;
2. `E5Embedder` direct flow đúng prefixes, native batching và instance lifecycle;
3. sparse behavior deterministic, rõ ràng và vẫn tương thích Phase 4;
4. config chỉ chứa local settings được dùng;
5. focused tests, Notebook 03, read-only active query và affected/full suite đạt;
6. active collection còn nguyên 572 points và test collections cleanup hết;
7. implementation report ghi observed evidence và limitations;
8. Reviewer audit độc lập, sau đó user xác nhận.

Commit/push cần yêu cầu riêng. Implementer không tự approve hoặc sửa guide này.
