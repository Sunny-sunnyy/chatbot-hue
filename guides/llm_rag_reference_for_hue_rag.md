# `llm_rag` reference cho quá trình review `hue_rag`

## Vai trò của tài liệu

Tài liệu này ghi những bài học hữu ích từ dự án `llm_rag` để dùng khi review và
đơn giản hóa `hue_rag` từ Phase 0 đến Phase 6.

`llm_rag` là reference baseline về cách tổ chức một RAG pipeline dễ đọc. Nó
không phải canonical guide của `hue_rag`, không tự tạo requirement và không
được sao chép nguyên trạng. Quyết định cuối cùng vẫn theo yêu cầu mới nhất của
user, guide canonical của từng phase, source code và real execution trong
`hue_rag`.

Snapshot reference được đọc và đối chiếu ngày `2026-08-24 +07`.

## Đường dẫn nguồn

Repository tham khảo:

```text
/home/minhhieu/llm_rag
```

Hai tài liệu mô tả toàn hệ thống:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_system_pipeline_deep_dive.md
/home/minhhieu/llm_rag/tai_lieu/rag_agent_handoff_current_repo.md
```

Các báo cáo trạng thái đã đọc:

```text
/home/minhhieu/llm_rag/report/Project_status.md
/home/minhhieu/llm_rag/report/README_report.md
/home/minhhieu/llm_rag/report/Agent_session_prompt.md
```

Source đã đối chiếu gồm toàn bộ pipeline backend trong:

```text
/home/minhhieu/llm_rag/backend
```

Các file frontend chính cũng được đọc để hiểu API streaming end-to-end:

```text
/home/minhhieu/llm_rag/frontend/app/layout.tsx
/home/minhhieu/llm_rag/frontend/app/page.tsx
/home/minhhieu/llm_rag/frontend/lib/api.ts
/home/minhhieu/llm_rag/frontend/components/ChatInterface.tsx
```

Không dùng `.env`, secret, `node_modules`, model cache, `qdrant_storage`, log,
build output hoặc tài liệu khôi phục WSL làm nguồn kiến trúc.

## Hệ thống `llm_rag` dùng làm baseline

`llm_rag` xây chatbot hỏi đáp về dữ liệu NMK Architects với hai luồng rõ ràng.

Luồng ingestion:

```text
raw JSON export
-> processed JSON theo bảng
-> domain-specific semantic chunks
-> dense + sparse representations
-> Qdrant points
```

Luồng query:

```text
question
-> dense candidates từ Qdrant
-> Python BM25 scoring
-> weighted hybrid ranking
-> MiniLM CrossEncoder reranking
-> bounded context
-> OpenRouter qua OpenAI Agents SDK
-> FastAPI SSE
-> Next.js UI
```

Các baseline kỹ thuật chính:

- local dense embedding `intfloat/multilingual-e5-small`, 384 dimensions;
- custom TF-IDF-style `SparseEmbedder`;
- Qdrant collection có named vectors `dense` và `sparse`;
- hybrid runtime lấy dense candidates rồi tính BM25 trong Python;
- reranker `cross-encoder/ms-marco-MiniLM-L-6-v2`;
- context tối đa 5 documents và khoảng 3000 characters;
- OpenAI Agents SDK gọi Qwen qua OpenRouter;
- FastAPI trả streaming SSE cho frontend;
- dữ liệu đã ghi nhận gồm 450 chunks từ JSON records.

## Vì sao `llm_rag` hữu ích cho `hue_rag`

Điểm mạnh lớn nhất của `llm_rag` là người đọc có thể lần theo pipeline theo
thứ tự folder và file. Mỗi module chủ yếu làm một việc cụ thể, dữ liệu trung
gian thường là Python `dict`, `list` hoặc một schema nhỏ, và các bước RAG được
thể hiện trực tiếp trong code.

Những nguyên tắc nên dùng làm chuẩn đọc code cho `hue_rag`:

1. Tổ chức source theo chiều dọc của pipeline.
2. Một entry point rõ cho ingestion và một entry point rõ cho query runtime.
3. Component nhận đầu vào đơn giản và trả đầu ra dễ kiểm tra.
4. Chỉ tạo abstraction khi có ít nhất hai implementation thật hoặc một boundary
   provider thật cần thay thế.
5. Metadata mang thông tin truy nguồn và thông tin domain cần dùng; không biến
   metadata thành nơi chứa trạng thái phòng xa.
6. Retrieval, reranking, context và generation là các bước tách biệt nhưng nối
   với nhau bằng contract nhỏ.
7. Notebook và tài liệu giải thích pipeline; runtime logic nằm trong backend.
8. Đánh giá bằng câu hỏi, database, model và API thật.

## Khác biệt dữ liệu bắt buộc phải giữ

`llm_rag` và `hue_rag` không dùng cùng data model.

| Nội dung | `llm_rag` | `hue_rag` |
|---|---|---|
| Nguồn answer-facing | Processed JSON records | Curated Markdown |
| Cách khám phá cấu trúc | Table và field names | File path, title và Markdown headings |
| Chunk boundary | Domain fields như `specs`, `style`, `context` | Semantic Markdown sections |
| Source identity | Tên JSON table/record | Relative Markdown path + section |
| Chunk ID lịch sử | Random UUID | Deterministic source/section/index |
| Corpus hiện hành | 450 chunks | 572 chunks |

Do đó không sao chép bảy JSON chunker của `llm_rag` sang `hue_rag`. Bài học cần
giữ là semantic chunking theo cấu trúc thật của dữ liệu. Với Markdown, heading
và document hierarchy thay cho JSON field names.

Một chunk của `hue_rag` chỉ cần đủ thông tin để người đọc biết:

```text
text
chunk_id
source
title
section
category/subcategory khi thực sự có ích
```

Không thêm field chỉ vì `llm_rag` từng có `priority`, `created_at`, record ID,
media URL hoặc nhiều metadata domain-specific.

## Ánh xạ reference vào Phase 0–6

### Phase 0 — Kiến trúc MVP

Phần nên học:

- một data flow end-to-end dễ vẽ và dễ trace;
- phân biệt ingestion offline với query online;
- component boundaries nhỏ;
- local E5, BM25, MiniLM và OpenAI Agents SDK là baseline đã chạy được trên máy
  cá nhân;
- frontend, deployment và agentic behavior không cần nằm trong MVP backend.

Phần không sao chép nguyên trạng:

- giữ đồng thời đường dense-only legacy và hybrid runtime;
- giữ cả Ollama route lẫn OpenRouter route dù chỉ một route hoạt động;
- coi mọi bài học lịch sử là capability bắt buộc;
- dùng mock pass làm bằng chứng hệ thống hoạt động.

### Phase 1 — Backend skeleton và configuration

Các reference chính:

```text
/home/minhhieu/llm_rag/backend/core/settings_loader.py
/home/minhhieu/llm_rag/backend/core/logging_setup.py
/home/minhhieu/llm_rag/backend/core/schema.py
/home/minhhieu/llm_rag/backend/config/settings.yaml
```

Phần nên học:

- YAML chứa non-secret defaults;
- environment chỉ override những giá trị cần thiết;
- một shared `RetrievedDocument` nhỏ;
- package layout phản ánh pipeline.

Khi review `hue_rag`, không mặc định rằng nhiều error class, validator, cache,
snapshot hoặc fingerprint tốt hơn skeleton nhỏ của reference. Mỗi cơ chế phải
giải quyết một failure thật còn tồn tại.

### Phase 2 — Markdown loading và chunking

Các reference về ý tưởng semantic chunking:

```text
/home/minhhieu/llm_rag/backend/ingestion/pipeline.py
/home/minhhieu/llm_rag/backend/ingestion/chunking
/home/minhhieu/llm_rag/backend/ingestion/helpers
```

Điều áp dụng là “chunk theo đơn vị ý nghĩa của domain”, không phải code đọc
JSON. `hue_rag` phải tiếp tục đọc curated Markdown, bỏ `_source-dumps`, dùng
heading/section làm boundary và tạo stable chunk IDs.

Các guard chỉ cần bảo vệ dữ liệu thật: file/source hợp lệ, chunk có text,
source đúng, ID không trùng và corpus có thể chạy end-to-end. Không cần tạo
validator cho mọi shape tưởng tượng.

### Phase 3 — Embedding và lexical representation

Các reference chính:

```text
/home/minhhieu/llm_rag/backend/embedding/embedder.py
/home/minhhieu/llm_rag/backend/embedding/batch_embed.py
/home/minhhieu/llm_rag/backend/embedding/sparse_embedder.py
/home/minhhieu/llm_rag/backend/llm/generator_openai.py
```

Phần nên học:

- load local model một lần;
- normalized dense vectors;
- batching trực tiếp;
- vocabulary/DF/IDF dễ đọc cho BM25;
- OpenAI Agents SDK có thể dùng với OpenAI-compatible OpenRouter endpoint.

`hue_rag` có hai nhu cầu OpenRouter khác nhau và phải giữ chúng tách biệt:

1. embedding model candidates để benchmark với local E5;
2. answer model open-source, ví dụ Qwen, dùng qua OpenRouter sau khi hệ thống ổn
   định.

OpenRouter là nhu cầu roadmap thật, nhưng adapter chỉ được coi là hoàn thành
khi code đơn giản và đã chạy API thật với model/dimension được chọn. Mock HTTP
không phải completion evidence.

### Phase 4 — Qdrant ingestion

Các reference chính:

```text
/home/minhhieu/llm_rag/backend/vectorstore/qdrant.py
/home/minhhieu/llm_rag/backend/vectorstore/hybrid_index.py
/home/minhhieu/llm_rag/backend/vectorstore/upsert.py
```

Phần nên học:

- point gồm ID, vector và payload;
- collection schema phải khớp embedding dimension;
- ingestion có một đường chạy rõ ràng;
- không âm thầm migrate collection khác schema.

Một hạn chế lịch sử quan trọng: `llm_rag` lưu sparse vectors trong Qdrant nhưng
query runtime chỉ tìm bằng named dense vector rồi tính BM25 trong Python.
`hue_rag` kế thừa đúng mô hình này. Sparse storage hiện không gây sai kết quả,
nhưng làm schema, ingestion và tests phức tạp hơn mà chưa có query consumer.

Trong lúc review Phase 3–5 phải chốt đúng một lexical path canonical:

- Python BM25 và Qdrant chỉ lưu dense; hoặc
- native sparse retrieval thật trong Qdrant và bỏ đường lexical trùng lặp.

Không giữ cả hai chỉ vì reference từng triển khai cả hai. Active Hue collection
vẫn read-only; mọi collection mới, reindex hoặc mutation phải được user duyệt.

### Phase 5 — Retrieval, BM25, reranking và context

Các reference chính:

```text
/home/minhhieu/llm_rag/backend/retrieval/hybrid_retriever.py
/home/minhhieu/llm_rag/backend/scoring/bm25.py
/home/minhhieu/llm_rag/backend/reranking/reranker.py
/home/minhhieu/llm_rag/backend/reranking/models/cross_encoder.py
/home/minhhieu/llm_rag/backend/retrieval/context_builder.py
```

Phần nên học:

- dense retrieval lấy candidates;
- BM25 chấm exact keyword;
- score từng stage được ghi rõ;
- CrossEncoder chỉ rerank tập candidates nhỏ;
- context có số documents và kích thước hữu hạn.

Phần cần review kỹ trong `hue_rag`:

- score normalization trước weighted fusion;
- ba profiles có thật sự dùng chung một flow dễ đọc;
- abstract base reranker có còn cần thiết;
- startup có thể tạo BM25/reranker trực tiếp mà không cần snapshot, corpus/config
  fingerprint hoặc nhiều typed errors hay không;
- context có cần serialized JSON/source-ID contract hay chỉ cần evidence blocks
  đơn giản.

Ba profiles cần tiếp tục được chạy thật:

```text
dense_only
hybrid_no_rerank
hybrid_rerank
```

Phase 7 cung cấp evaluation engine; việc so sánh profiles và embedding models
thuộc benchmark Phase 8.

### Phase 6 — Generation và API

Các reference chính:

```text
/home/minhhieu/llm_rag/backend/llm/prompt.py
/home/minhhieu/llm_rag/backend/llm/generator_openai.py
/home/minhhieu/llm_rag/backend/api/app.py
/home/minhhieu/llm_rag/backend/api/health.py
/home/minhhieu/llm_rag/backend/api/routes/chat_openai.py
/home/minhhieu/llm_rag/frontend/lib/api.ts
```

Phần nên học:

- prompt nhận context và question trực tiếp;
- Agents SDK được dùng như một model call có structured boundary, không cần
  agent router hoặc tool graph;
- route điều phối retrieval → context → generation theo thứ tự nhìn thấy được;
- streaming chỉ cần khi frontend thật sử dụng nó;
- sources đi cùng answer.

Phần không sao chép nguyên trạng:

- hai chat routes trùng logic cho hai providers;
- legacy Ollama generator không còn consumer hợp lệ;
- session và rate limiting in-memory khi MVP không có requirement hội thoại hoặc
  public deployment;
- health endpoint tự load model hoặc làm dependency work mới;
- broad exception biến mọi lỗi, kể cả `HTTPException`, thành HTTP 500;
- mocked endpoint/generator tests làm bằng chứng chính.

`hue_rag` hiện dùng JSON API thay vì frontend SSE. Không thêm streaming,
session memory, rate limiter hoặc frontend contract trước khi có nhu cầu thật.

## Những phần nên giữ, sửa hoặc loại bỏ

| Nhóm | Hướng áp dụng cho `hue_rag` |
|---|---|
| Pipeline folder layout | Giữ |
| Local E5 baseline | Giữ |
| Semantic domain-aware chunking | Giữ ý tưởng, dùng Markdown implementation |
| Small shared retrieval schema | Giữ, đơn giản hóa nếu đang quá rộng |
| Python BM25 | Giữ cho tới khi có quyết định native sparse khác |
| Three retrieval profiles | Giữ và benchmark thật |
| MiniLM reranker | Giữ baseline, ghi đúng giới hạn tiếng Việt |
| Bounded context | Giữ |
| OpenAI Agents SDK | Giữ |
| OpenRouter capability | Giữ nhu cầu; adapter phải chạy thật và dễ đọc |
| Stored sparse vector không được query | Không mặc định giữ; quyết định ở Phase 3–5 |
| Dense/Ollama legacy paths | Không mang sang chỉ để rollback/học tập |
| Random UUID chunk IDs | Không áp dụng; giữ deterministic IDs của Markdown |
| Mock/fake completion evidence | Không áp dụng |
| Frontend/SSE | Ngoài Phase 0–6 hiện tại |
| Snapshot/fingerprint/tamper machinery | Chỉ giữ nếu một failure thật chứng minh cần |

## Chuẩn review rút ra cho `hue_rag`

Mỗi phase được review riêng theo dependency order. Trước câu hỏi thiết kế của
mỗi phase, Reviewer phải:

1. nêu phase tạo ra gì và nằm ở đâu trong pipeline;
2. đọc guide, source, tests, notebook và reports của phase;
3. đối chiếu phần tương ứng trong `llm_rag` khi hữu ích;
4. trace luồng chạy thật, không chỉ đếm files hoặc tests;
5. chỉ ra code nào phục vụ capability hiện tại, code nào chỉ là legacy/future;
6. đưa ra lựa chọn làm thay đổi scope/design/test/implementation;
7. chờ user duyệt design trước khi giao Implementer sửa code.

Mọi completion claim phải dựa trên dữ liệu Foods thật, Qdrant thật, local model
thật và provider API thật trong đúng approved scope. Failed hoặc partial result
phải được giữ đúng; prior output và mock không thay fresh verification.

## Kết luận áp dụng

`llm_rag` là chuẩn tham khảo tốt về một RAG pipeline có thể đọc tuần tự từ data
đến UI. Giá trị nên mang sang là data flow trực tiếp, module nhỏ, semantic
chunking, hybrid retrieval, bounded context và model call rõ ràng.

Những hạn chế của reference cũng là dữ liệu review quan trọng: code legacy tồn
tại song song, sparse vectors không được query, global startup state, duplicate
routes và tests dựa nhiều vào monkeypatch. `hue_rag` không cần lặp lại các hạn
chế đó để giữ quan hệ với dự án gốc.

Mục tiêu cuối cùng vẫn là một Hue Foods RAG giữ đủ capability thật, nhưng code
ngắn, rõ, dễ trace và đủ gần cách viết của `llm_rag` để user có thể tự đọc và
hiểu toàn bộ hệ thống.
