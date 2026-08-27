# Phase 0 — Nền tảng Hue Foods RAG MVP

## Trạng thái

`approved`

Phase 0 đã hoàn thành simplicity review ngày `2026-08-24 +07`. Review chỉ cập
nhật kiến trúc và quy trình tài liệu; không thay đổi runtime, test, notebook,
dữ liệu hoặc active Qdrant collection. Phase 1–5 simplicity review sau đó đã
hoàn tất và được user xác nhận; Phase 6 là simplicity review tiếp theo.

Tài liệu liên quan:

```text
docs/superpowers/specs/2026-08-24-phase-0-simplicity-review-design.md
reports/phase_0_mvp_foundation_simplicity_review.md
guides/llm_rag_reference_for_hue_rag.md
```

## Mục tiêu

MVP nhận curated Markdown tiếng Việt về ẩm thực Huế, tạo chunks, biểu diễn bằng
dense/sparse vectors, index vào một active Qdrant collection, retrieval theo ba
profiles, build bounded context, sinh grounded answer và đánh giá kết quả.

Agentic RAG, frontend và deployment không thuộc MVP hiện tại.

## Data flow

```text
curated foods Markdown
-> semantic Markdown chunks
-> dense embeddings + sparse representations
-> active Qdrant collection
-> retrieval profile
-> bounded context
-> grounded answer
-> simple evaluation
-> benchmark decision
```

Không chunk trực tiếp từ `_source-dumps`. Enrichment chỉ thực hiện khi user
duyệt dữ liệu và nguồn.

## Thư mục chính

| Path | Trách nhiệm |
|---|---|
| `knowledge-base-hue/foods/` | Curated Markdown answer-facing |
| `backend/` | Runtime Python và tests |
| `notebooks/` | Notebook học tập gọi backend |
| `guides/` | Một guide canonical cho mỗi phase |
| `reports/` | Implementation evidence, Codex review và benchmark summary |
| `reports/user_reports/` | Báo cáo dễ hiểu dành cho user |
| `session_prompt/Project_Status.md` | Snapshot bàn giao hiện tại |

## Component boundaries

| Component | Nhận vào | Trả ra |
|---|---|---|
| Markdown chunker | Curated food Markdown | Chunk dictionaries |
| Dense embedder | Text/query | Normalized dense vectors |
| Sparse embedder | Corpus/text | Sparse indices và values |
| Qdrant ingestion | Chunks và vectors | Named-vector points |
| Retrieval service | Query và profile | Ranked `RetrievedDocument` |
| Reranker | Query và candidates | Reranked candidates |
| Context builder | Ranked documents | Bounded evidence context |
| Generator | Question và context | Grounded answer + sources |
| Evaluation | Real questions và backend | Metrics, answer scores và CSV |

Boundary phải giúp người đọc theo được luồng. Không tạo thêm interface hoặc
component chỉ để dự phòng tương lai.

Chỉ giữ abstraction khi có từ hai implementation thật đang dùng hoặc một
provider boundary thật. Vì vậy embedding và generation giữ boundary cho các
provider hiện tại/tương lai đã xác định; ba retrieval profiles dùng một service
nhỏ; MiniLM dùng implementation cụ thể khi chưa có reranker thứ hai. Snapshot,
fingerprint, validator hoặc typed error chỉ được giữ khi có nhu cầu runtime và
caller behavior khác biệt đang tồn tại.

## Model và provider

| Vai trò | Baseline | Quy tắc |
|---|---|---|
| Dense embedding | `intfloat/multilingual-e5-small`, CPU | 384 dimensions, `query:`/`passage:` |
| Sparse representation | Custom TF-IDF-style embedder | Deterministic trên cùng corpus |
| Lexical scoring | Python BM25 | Chỉ chạy trong hybrid profiles |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2`, CPU | Baseline nhẹ, có giới hạn tiếng Việt |
| Answer generation | OpenAI Agents SDK, `gpt-5.4-nano` | Production answer model |
| Answer judge | OpenAI Agents SDK, `gpt-5.4-mini` | Chỉ dùng evaluation/quality judge |

Remote embedding, reranking hoặc future answer model chỉ được mở khi Phase 8 có
guide/design được user duyệt.

API keys chỉ đến từ environment và không được lưu trong YAML, Markdown,
notebook, report hoặc log.

## Qdrant contract

- Một active collection cho Hue Foods runtime/benchmark tại một thời điểm.
- Collection hiện hành: `hue_foods_e5_small_384`, 572 points.
- Dense vector `dense`: 384 dimensions, cosine.
- Sparse vector name: `sparse`.
- Collection gắn với embedding model, dimension, distance và payload schema.
- Đổi model/dimension cần exact reindex scope và user approval.
- Active collection chỉ read-only trong implementation/review thông thường.
- Không wildcard/prefix delete.

MVP hybrid dùng dense candidates kết hợp Python BM25. Việc lưu sparse vectors
không tự có nghĩa là native sparse retrieval đã chạy.

## Retrieval profiles

| Profile | Dense search | Python BM25 | Reranker |
|---|---:|---:|---:|
| `dense_only` | Có | Không | Không |
| `hybrid_no_rerank` | Có | Có | Không |
| `hybrid_rerank` | Có | Có | Có |

Ba profiles dùng cùng corpus, chunk IDs và embedding collection trong một
experiment.

## Data contracts

Chunk:

```python
{
    "text": "...",
    "metadata": {
        "chunk_id": "foods/restaurants/example.md|Tóm tắt|0",
        "source": "foods/restaurants/example.md",
        "title": "Tên tài liệu",
        "section": "Tóm tắt",
        "category": "foods",
        "subcategory": "restaurants",
        "chunk_type": "section",
    },
}
```

Retrieval result dùng shared `RetrievedDocument` và chỉ ghi score của stage
thực sự đã chạy:

```text
id
score
text
metadata.source
metadata.title
metadata.section
metadata.dense_score
metadata.bm25_score
metadata.hybrid_score
metadata.rerank_score
```

Không tạo score giả cho stage không chạy.

## Configuration

```yaml
active_profile: dense_only
profiles: {}
knowledge_base: {}
embedding: {}
vector_database: {}
retrieval: {}
reranking: {}
llm: {}
evaluation: {}
```

Provider/model, dimension, collection target và benchmark variable phải rõ
trong guide/report liên quan. Secrets chỉ đến từ environment.

## Code và test

- Code rõ ràng, nhỏ nhất cần thiết và không implement future flexibility.
- Reviewer phải yêu cầu bỏ over-engineering.
- Chỉ test hành vi thật và lỗi quan trọng.
- Không đặt test-count target.
- Không mock/fake.
- Test pass không thay real-system run.
- Reviewer/Implementer áp dụng `skills/practical-project-coding/SKILL.md`.

Verification đi theo phạm vi ảnh hưởng:

```text
exact live path
-> smallest necessary targeted tests nếu thực sự cần
-> notebook Run All nếu phase có notebook và có giá trị học tập
-> affected downstream flows
-> full backend suite chỉ cho broad shared change hoặc final Phase 0–6 check
-> Phase 7 evaluation 20 câu nếu chất lượng RAG có thể thay đổi
```

Mỗi Phase 0–6 có một simplicity review ghi Before, capability cần giữ, thay đổi
được duyệt, ảnh hưởng downstream, kết quả After, bug và cách xử lý. Không chạy
lại paid 104-question evaluation trong simplicity review thông thường.

Mỗi phase chỉ audit test thuộc ownership và downstream scope bị ảnh hưởng trực
tiếp. Test không bảo vệ nhu cầu người dùng, chỉ dựng lỗi giả định hiếm, trùng
live path hoặc chỉ phục vụ cơ chế cần loại bỏ phải được xóa và không chạy. Một
phase có thể không cần automated test. Failure test chỉ giữ cho lỗi thực tế
quan trọng có nguy cơ tái diễn.

Chi tiết chung thuộc `session_prompt/Session_Prompt.md`.

## Real execution

- Dùng canonical foods data và actual service state.
- Dùng Qdrant, local models và provider APIs thật theo phase guide.
- Online và paid API trong approved phase được phép.
- Không cần consent gate, cost cap hoặc cost-estimation code.
- Không dùng replay hoặc prior output làm fresh evidence.
- Failed/skipped/partial outcome phải được giữ đúng.
- Provider/model/scope mới, deploy hoặc destructive action cần user approval.

## Evaluation và benchmark

Phase 7 bắt đầu bằng evaluation đơn giản:

```text
question -> retrieve -> build context -> generate -> judge -> report
```

- `test2.jsonl`: 20 real questions để chạy đầu tiên.
- `tests.jsonl`: 104 real questions sau khi small run ổn định.
- Initial profile: `dense_only`.
- Retrieval: keyword-based MRR, nDCG và coverage.
- Answer: accuracy, completeness, relevance và feedback.
- Generation: `gpt-5.4-nano`.
- Judge: `gpt-5.4-mini`.

Phase 8 mới so sánh profiles/models và chọn winner. Không tuyên bố winner từ
Phase 7.

## Notebook

Chỉ phase có giá trị học tập thật mới có notebook canonical. Không tạo notebook
để đủ số phase. Notebook được giữ phải:

- giúp con người hiểu hệ thống;
- mỗi cell làm một việc;
- giải thích ngắn trước code;
- gọi backend thay vì duplicate logic;
- không là validator, audit package hoặc test suite;
- sạch outputs/execution counts trong repo;
- được Run All thật trên temporary copy.

Style references:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/*.ipynb
/home/minhhieu/llm_rag/tai_lieu/notebook_simple/**/*.ipynb
```

## Acceptance chung

Một phase implementation chỉ đạt `approved` khi:

1. code đúng guide và dễ hiểu;
2. tests cần thiết bảo vệ hành vi thật;
3. Reviewer đã chạy independent real verification;
4. notebook sạch và Run All được nếu canonical guide yêu cầu notebook;
5. user đã đọc report, kiểm tra kết quả, chạy notebook nếu có và xác nhận.

Commit/push cần yêu cầu riêng.

## Thứ tự tiếp theo

```text
Phase 0–5 simplicity review đã approved
-> Phase 6 simplicity review
-> re-run affected Phase 7 evaluation
-> Phase 8
```

Simplicity review Phase 6 bắt đầu từ Repo và live system: guide, reports,
source code, notebook và real run. Tài liệu ngoài do user cung cấp là tùy chọn khi
thực sự hữu ích; nếu thiếu mà còn lựa chọn quan trọng, brainstorm với user.
Không áp Phase 7 reference như blueprint cho phase khác.

## Quyết định kiến trúc

```text
Decision: Mỗi phase có một guide canonical; reports là evidence và project status là snapshot.
Reason: Tách requirement, bằng chứng và handoff để tránh nhiều nguồn điều hành.
Date +07: 2026-08-09, simplified 2026-08-23.
```

```text
Decision: Dùng local E5, BM25 và MiniLM làm baseline trước remote candidates.
Reason: Baseline đã chạy được trên máy hiện tại và tạo phép so sánh ổn định.
Date +07: 2026-08-09.
```

```text
Decision: Giữ capability của MVP nhưng cho phép đơn giản hóa internal structures.
Reason: Wrapper, validator hoặc compatibility nội bộ không phải chức năng người dùng nếu cùng hành vi có thể được viết trực tiếp và dễ hiểu hơn.
Date +07: 2026-08-24.
```

```text
Decision: Chỉ giữ abstraction cho nhiều implementation thật hoặc provider boundary thật.
Reason: Local/OpenRouter embedding, OpenAI/OpenRouter generation và ba retrieval profiles là biến thể thật; abstraction phòng xa khác không có nhu cầu hiện tại.
Date +07: 2026-08-24.
```

```text
Decision: Quyết định giữ, bỏ hoặc query native sparse vectors được hoãn tới review Phase 3–5.
Reason: Collection hiện tại vẫn đúng với runtime dense candidates + Python BM25 và Phase 0 không có quyền đổi dữ liệu/index.
Date +07: 2026-08-24.
```

```text
Decision: Chỉ phase có giá trị học tập thật mới có notebook; Phase 1 không cần notebook.
Reason: Notebook phải giúp con người hiểu hệ thống, không làm validator hoặc tồn tại chỉ để đủ số phase.
Date +07: 2026-08-24.
```

```text
Decision: Reviewer và Implementer được chạy online và paid APIs trong approved phase.
Reason: Completion evidence phải đến từ hệ thống thật, không từ fake/mock.
Date +07: 2026-08-21, simplified 2026-08-23.
```
