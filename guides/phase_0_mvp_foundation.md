# Phase 0: Nền tảng kiến trúc Hue Foods RAG MVP

## Mục tiêu và giá trị cho người dùng

Phase 0 xác lập kiến trúc, ranh giới provider, data flow, governance và tiêu chuẩn chất lượng chung cho Hue Foods RAG MVP. Người dùng có thể đọc file này để hiểu hệ thống sẽ xây gì, chưa xây gì và lý do các phase được sắp xếp theo thứ tự hiện tại.

## Trạng thái

```text
Status: completed
Brainstorming level: Level 0 - locked
Owner: Codex Reviewer
Implementation: not applicable
```

Phase 0 đã được người dùng xác nhận. Chỉ mở lại khi một quyết định xuyên phase thay đổi kiến trúc hoặc acceptance contract.

## Chức năng của MVP

MVP nhận dữ liệu Markdown tiếng Việt đã curate về ẩm thực Huế, tạo semantic chunks, biểu diễn chunks bằng dense và sparse vectors, index vào một active Qdrant collection, truy xuất theo ba profile, sinh câu trả lời grounded có nguồn và đánh giá cả retrieval lẫn answer quality.

Agentic RAG, frontend và streaming không thuộc MVP đầu tiên.

## Data flow canonical

```text
raw data
  -> Markdown source dumps
  -> curated Markdown trong knowledge-base-hue/foods/
  -> semantic Markdown section chunks
  -> dense embeddings + sparse representations
  -> một active Qdrant collection
  -> dense candidates
  -> optional Python BM25 fusion
  -> optional reranking
  -> bounded context
  -> grounded answer generation
  -> retrieval metrics + answer judge
  -> benchmark evidence và model selection
```

Không chunk trực tiếp từ `_source-dumps`. Enrichment chỉ thực hiện khi người dùng yêu cầu và nguồn đã được xác minh.

## Quyền sở hữu thư mục

| Đường dẫn | Trách nhiệm |
|---|---|
| `knowledge-base-hue/foods/` | Curated Markdown answer-facing |
| `backend/` | Runtime Python và unit/integration tests |
| `notebooks/` | Notebook học tập, import backend modules |
| `guides/` | Hướng dẫn canonical theo phase |
| `reports/` | Technical implementation evidence, Codex review và benchmark summary dành cho coding agents |
| `reports/user_reports/` | Báo cáo phase dễ hiểu dành cho người dùng, chỉ Codex Reviewer tạo/cập nhật |
| `backend/evaluation/results/` | JSONL outputs chi tiết khi evaluation đã implement |
| `session_prompt/Project_Status.md` | Snapshot bàn giao hiện tại |

## Ranh giới component

| Component | Nhận vào | Trả ra | Không chịu trách nhiệm |
|---|---|---|---|
| Markdown chunker | Curated food Markdown | Chunk dictionaries ổn định | Embedding, Qdrant, generation |
| Dense embedder | List text hoặc query | Normalized dense vectors | Collection lifecycle, ranking fusion |
| Sparse embedder | Corpus và text | Sparse `indices`/`values` | Qdrant query fusion trong MVP |
| Qdrant ingestion | Chunks và vectors | Named-vector points | Retrieval tuning, answer generation |
| Retrieval service | Query và active profile | `RetrievedDocument` list | Prompt hoặc provider API |
| Reranker | Query và candidates | Candidates sắp hạng lại | Vector indexing |
| Context builder | Ranked documents | Bounded evidence context | Retrieval hoặc model call |
| Generator | Query và evidence | Grounded answer + sources | Judge score hoặc index mutation |
| Evaluation | Test cases và pipeline output | Metrics, JSONL evidence, summary | Tự thay config để cải thiện score |

## Model và provider đã chốt

| Vai trò | Baseline hoặc provider | Quy tắc |
|---|---|---|
| Local dense embedding | `intfloat/multilingual-e5-small`, CPU | Baseline đầu tiên, 384 dimensions, benchmark trước remote models |
| Local sparse representation | Custom TF-IDF-style `SparseEmbedder` | Fit trên cùng corpus chunks; deterministic vocabulary/IDF |
| Local lexical scoring | Python BM25 | Baseline theo kỹ thuật từ `llm_rag` |
| Local reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2`, CPU | Baseline nhẹ; phải ghi giới hạn tiếng Việt |
| Remote embedding | OpenRouter embeddings endpoint | Qwen3 Embedding là family ưu tiên sau catalog preflight |
| Remote reranking | OpenRouter native rerank endpoint | Hoãn adapter, exact model preflight và benchmark sang Phase 8; Phase 5 chỉ dùng local MiniLM |
| Answer generation | OpenAI Agents SDK, `gpt-5.4-nano` | Baseline generation trực tiếp qua OpenAI |
| Answer judge | OpenAI Agents SDK, `gpt-5.4-mini` | Tách riêng với answer model |
| Future generation | OpenRouter, `qwen/qwen3.5-9b` | Chỉ benchmark sau khi pipeline baseline ổn định |

`OPENAI_API_KEY` và `OPENROUTER_API_KEY` được quản lý độc lập trong environment. Không lưu value vào YAML, Markdown, notebook hoặc report.

## Qdrant active collection contract

- Tại một thời điểm chỉ có một collection active cho Hue Foods benchmark/runtime.
- Collection gắn chặt với embedding model, vector dimension, distance và payload schema.
- Thay embedding model hoặc dimension luôn yêu cầu reset/reindex; không thể fallback theo request sang vector space khác.
- Trong một embedding experiment, cùng collection được dùng cho cả ba retrieval profiles.
- Chỉ xóa collection sau khi đã kiểm tra exact name, model, dimension, point count, result artifacts và nhận user approval.
- Sau khi chọn winner, reindex winner, kiểm tra count/schema rồi đặt reset thành `false`.

Named vectors dự kiến:

```text
dense
sparse
```

Sparse vector được lưu để sẵn sàng cho nghiên cứu sau này. MVP hybrid hiện tại dùng dense candidates kết hợp Python BM25; việc chỉ lưu sparse vector không được tính là một sparse retrieval run.

## Retrieval profiles canonical

| Profile | Candidate retrieval | BM25 fusion | Reranker |
|---|---|---:|---:|
| `dense_only` | Qdrant dense | Không | Không |
| `hybrid_no_rerank` | Qdrant dense lấy dư candidates | Có | Không |
| `hybrid_rerank` | Cùng hybrid pipeline | Có | Có |

Các profile phải dùng chung corpus, chunk IDs và embedding collection trong cùng model experiment. Candidate depth, fusion weights, `top_k`, rerank depth và context limits phải được ghi vào benchmark record.

## Data contracts

Chunk object:

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

Retrieval result phải dựa trên shared `RetrievedDocument` và có khả năng ghi các score thực sự đã được tính:

```text
id
score
text
metadata.source
metadata.title
metadata.section
metadata.dense_score
metadata.bm25_score       # chỉ khi BM25 đã chạy
metadata.hybrid_score     # chỉ khi fusion đã chạy
metadata.rerank_score     # chỉ khi reranker đã chạy
```

Không tạo score field giả cho stage không chạy.

## Configuration contract

Các nhóm config canonical:

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

Mọi config thay đổi vector dimension, collection reset, live provider hoặc benchmark controlled variable phải được ghi trong report/ledger. API key chỉ đến từ environment.

## Brainstorming và decision gates

Phase 0 không yêu cầu brainstorm lại. Các phase sau phải dừng để hỏi người dùng nếu có:

- provider/model mới hoặc model ID không còn tồn tại;
- dependency mới hoặc model/provider chưa được approved;
- thay đổi dimension, schema hay collection deletion/reset;
- live paid call vượt approved bounded validation/budget hoặc full judge run;
- thay đổi phase boundary, acceptance metric hoặc notebook contract;
- benchmark result mâu thuẫn hoặc không so sánh được;
- privacy, security, data provenance hoặc license concern.

Decision record dùng sáu field trong `guides/README.md`.

## Nhiệm vụ của DeepSeek Implementer

- Đọc Phase 0 trước mọi phase runtime.
- Không copy trực tiếp provider/storage choices từ `llm_rag` hoặc `rag_old`; chỉ tái sử dụng kỹ thuật đã được guide phê duyệt.
- Giữ module nhỏ, interface rõ và không implement future flexibility.
- Chuỗi runtime bắt buộc: `pyproject.toml + uv.lock -> uv -> project .venv -> uv run`; dựng/đồng bộ bằng `uv sync`, chạy bằng `uv run python ...` / `uv run pytest ...`; không dùng `pip` và không chạy project bằng `python`/`python3`/`pytest`/`uvicorn` từ system environment.
- Chạy smallest relevant tests trước, sau đó chạy live validation cần thiết qua
  dependency/external service thật trong approved scope; standing authorization
  ngày 2026-08-21 loại bỏ việc xin lại cho từng bounded run.
- Dùng curated/canonical input và actual service state đúng phase contract;
  fixture, synthetic/sample data hoặc prior output không được dùng làm PASS
  evidence. Ghi fresh actual counts/schema/metrics cùng mọi failed/skipped/
  partial outcome từ exact command/run.
- Tạo notebook bắt buộc cho Phase 1–8 và implementation report đúng phase.
- Không tạo hoặc sửa user report.

## Nhiệm vụ của Codex Reviewer

- Kiểm tra scope, interface, dependency, secret exposure, data mutation và benchmark comparability.
- Xác minh implementation report bằng command độc lập phù hợp.
- Không chấp nhận claim chỉ dựa trên notebook output hoặc lời mô tả.
- Đối chiếu data source/snapshot, actual counts/schema/metrics và raw-safe
  artifacts từ fresh independent run; không chấp nhận fixture, synthetic/sample
  data, prior output hoặc expected value làm observed PASS evidence.
- Không approve nếu silent fallback, fabricated metrics, uncontrolled comparison hoặc destructive action thiếu evidence.
- Khi technical review đạt, tạo user report `pending` và chuyển phase sang `awaiting_user_confirmation`.
- Chỉ sau user confirmation mới chuyển phase sang `approved`, cập nhật `Project_Status.md`, audit approved package, commit và push.

## Notebook contract

- Mọi implementation phase từ Phase 1 đến Phase 8 có đúng một notebook canonical; số notebook trùng số phase.
- Notebook nằm trong `notebooks/` và import backend modules.
- Không duplicate runtime logic.
- Mọi output rỗng; mọi `execution_count` là `null` trong repo.
- Theo quyết định user ngày 2026-08-13, Run All của notebook 01–06 đi qua
  runtime thật: local cached model, Qdrant read-only hoặc full API path tùy
  phase. Không có fake fallback hoặc real-mode guard; thiếu prerequisite fail
  rõ ràng. Notebook 06 giới hạn đúng một OpenAI call mỗi Run All theo ngân sách
  user duyệt.
- Tests và notebook được phép dùng network/dependency thật theo approved scope;
  không đặt offline flags làm mặc định chung. Phase 7–8 vẫn cần guide riêng chốt
  experiment scope, budget và full-run gate trước implementation.
- Không lưu private path, raw headers, raw model payload lớn hoặc stack trace có sensitive data.

Notebook canonical:

```text
notebooks/01_backend_foundation.ipynb
notebooks/02_foods_data_and_chunking.ipynb
notebooks/03_embedding_models.ipynb
notebooks/04_qdrant_ingestion.ipynb
notebooks/05_retrieval_profiles.ipynb
notebooks/06_generation_and_api.ipynb
notebooks/07_evaluation.ipynb
notebooks/08_benchmark_model_selection.ipynb
```

Phase 0 được miễn. Phase 9 chỉ có notebook sau khi rời `design_only` bằng một design và implementation approval riêng.

## Report và user confirmation contract

- DeepSeek viết technical implementation report trong `reports/`.
- Codex viết technical review report trong `reports/`.
- Sau technical review đạt, Codex viết `reports/user_reports/phase_<id>_<short_name>_user_report.md` bằng tiếng Việt dễ hiểu.
- User report phải có trạng thái, mục tiêu, chức năng, luồng, file quan trọng, notebook, lệnh tự kiểm tra, validation thực tế, kỹ thuật, giới hạn, external API/cost, bước tiếp theo và checklist xác nhận.
- Phase chỉ được `approved` sau khi user xác nhận user report và notebook.
- User confirmation cho phép Codex commit/push đúng approved phase package sau staged-scope audit; không bao gồm thay đổi ngoài scope.

## Evaluation và benchmark contract

- Retrieval evaluation chạy toàn bộ 104 câu khi Phase 7 sẵn sàng.
- Answer generation/judge bắt đầu bằng stratified subset để kiểm soát cost.
- Chỉ chạy full 104 answer judge khi người dùng phê duyệt chi phí.
- Markdown ledger chỉ lưu registry, summary và decision; per-question evidence lưu JSONL.
- Không tuyên bố winner trước khi runs có cùng corpus, metric definitions và controlled variables.

## Security, reliability và performance

- Không mở, `cat`, in hoặc log nội dung/giá trị `.env`, token, key, auth header
  hay credential file. Được nạp repo-root `.env` trực tiếp vào approved process
  bằng `uv run --env-file`; chỉ kiểm tra key presence và không dump environment.
- Network/model/API được phép dùng trong approved live validation. Không mặc
  định đặt `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1` hoặc `UV_OFFLINE`; chỉ
  dùng khi exact guide/test yêu cầu cache-only/offline behavior.
- Model local được cache một lần mỗi process; batch operation phải bounded.
- Context có giới hạn document và character/token budget.
- Provider error phải rõ ràng; benchmark không được tự đổi model.
- Collection reset fail closed khi target không khớp exact expected configuration.

## Ngoài scope MVP

- Agentic query router, query rewrite, decomposition và retry judge.
- Parent-child retrieval.
- Frontend, SSE hoặc production deployment.
- Qdrant native sparse fusion như một profile chính thức.
- Automatic multi-provider embedding fallback.
- Data enrichment không được người dùng yêu cầu.

## Tiêu chí hoàn tất Phase 0

- Kiến trúc và phase boundaries được người dùng xác nhận.
- Provider, model baseline và key separation được chốt.
- Ba retrieval profiles có semantics khác nhau rõ ràng.
- One-active-collection lifecycle và deletion gate được chốt.
- Evaluation, benchmark, notebook và report contracts được chốt.
- Dual-report model và hard user-confirmation gate được chốt.
- Phase 9 có hard gate thiết kế riêng.

## Quyết định đã phê duyệt

```text
Decision: Dùng phase guides làm nguồn hướng dẫn canonical, reports làm evidence và Project_Status.md làm snapshot.
Approved by: User
Approval date +07: 2026-08-09
Evidence: Brainstorming trong session reviewer hiện tại.
Affected scope: Phase 0–9 và governance documentation.
Revisit trigger: Người dùng yêu cầu đổi source-of-truth hierarchy.
```

```text
Decision: Benchmark local llm_rag baseline trước OpenRouter models.
Approved by: User
Approval date +07: 2026-08-09
Evidence: User xác nhận intfloat/multilingual-e5-small và CrossEncoder nhẹ chạy trên máy.
Affected scope: Phase 3, 4, 5, 7 và 8.
Revisit trigger: Local resource preflight thất bại hoặc baseline không thể chạy hợp lệ.
```

```text
Decision: Tách technical reports cho coding agents và user reports cho người dùng; Phase 1–8 cần notebook và user confirmation trước approved.
Approved by: User
Approval date +07: 2026-08-09
Evidence: Brainstorming governance trong session reviewer hiện tại.
Affected scope: Phase 1–9, guides, workflows, report templates, notebooks và Project_Status lifecycle.
Revisit trigger: Người dùng yêu cầu thay đổi approval authority, report audience hoặc notebook gate.
```

```text
Decision: Notebook canonical 01–06 chạy runtime thật khi Run All; fake chỉ giữ trong tests. Notebook 03/05 dùng model local cache-only, 04 chỉ Qdrant read-only, 06 gọi đúng một OpenAI call qua full API path.
Approved by: User
Approval date +07: 2026-08-13
Evidence: Yêu cầu redesign notebook và live validation độc lập của Codex.
Affected scope: Notebook 01–06, notebook rules và reviewer/implementer workflows.
Revisit trigger: User yêu cầu khôi phục safe-default, thay đổi budget/call limit hoặc Phase 7–8 được phê duyệt live.
```

```text
Decision: Phase 5 dùng local MiniLM reranker; hoãn OpenRouter reranker adapter, exact model preflight và controlled benchmark sang Phase 8.
Approved by: User
Approval date +07: 2026-08-12
Evidence: Level 3 brainstorming Phase 5 sau khi đối chiếu pipeline llm_rag đã chạy local với contract hue_rag.
Affected scope: Phase 5 retrieval/reranking, Phase 8 benchmark và remote-provider gate.
Revisit trigger: Local reranker không đạt latency gate hoặc Phase 7–8 quality evidence tạo hypothesis rõ cho remote reranker.
```

```text
Decision: Cấp standing authorization cho coding agents và Reviewer chạy online, dùng dependency/provider thật và nạp key đã có trong repo-root .env bằng safe env-file loader cho approved implementation/review/validation scope; offline flags không phải mặc định chung.
Approved by: User
Approval date +07: 2026-08-21
Evidence: User xác nhận các key cần thiết đã có trong .env và cho phép coding agents chạy thật, kiểm tra thật và chạy online.
Affected scope: Shared session prompt, Reviewer/Implementer workflows và Phase 1–8 runtime validation.
Revisit trigger: User thu hồi quyền, provider/model/scope thay đổi, chi phí tăng đáng kể, hoặc exact guide/test yêu cầu cache-only/offline behavior.
```

## Bước tiếp theo

Phase 1–6 và Milestone 6.1 đã được người dùng xác nhận với status `approved`.
Phase 7 có status `not_ready` và cần Level 3 brainstorming trước implementation.
Provider/model mới, scope expansion, chi phí tăng đáng kể hoặc destructive
action vẫn cần user approval riêng.
