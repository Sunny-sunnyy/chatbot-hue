# Phase 8: Benchmark và lựa chọn model/pipeline

## Mục tiêu và giá trị cho người dùng

Phase 8 so sánh có kiểm soát các thành phần của Hue Foods RAG, bắt đầu bằng baseline local nhẹ rồi mới dùng OpenRouter. Kết quả cuối là cấu hình được chọn từ quality, latency, reliability và cost evidence, không chọn theo cảm tính hoặc leaderboard ngoài domain.

## Trạng thái

```text
Status: not_ready
Brainstorming level: Level 3 - deep
Owner: Codex Reviewer
Implementer: DeepSeek after Phase 7 approval and Phase 8 readiness
```

## Dependency

- Phase 3–7 đã được approve.
- Dataset, relevance definition, metric version và artifact schema đã khóa.
- Active collection lifecycle và exact deletion guard hoạt động.
- `reports/hue_foods_rag_benchmark.md` là ledger canonical.
- Mỗi paid experiment có user approval riêng.

## Thành phần có thể thay đổi

Không chỉ có embedding, sparse representation, hybrid retriever và reranker. Pipeline có các experiment groups:

| Group | Biến có thể thay đổi | Điều giữ cố định khi test group |
|---|---|---|
| Chunking | section rules, max length | corpus version, embedding, retrieval, metrics |
| Dense embedding | provider, model, dimension, instruction | chunks, profiles, evaluation set |
| Sparse representation | tokenizer, TF-IDF weighting | dense candidates, corpus, BM25/fusion |
| Lexical scoring | BM25 k1/b/tokenizer | dense model, candidates, reranker off |
| Hybrid fusion | normalization, weights, candidate depth | embedding, BM25, reranker off |
| Reranker | provider/model/top-k | pre-rerank candidates và hybrid config |
| Context | document/budget/source formatting | retrieval output, generator |
| Generator | provider/model/prompt/settings | context, test subset, judge rubric |
| Judge | model/rubric/version | frozen generated answers |

MVP ưu tiên dense embedding, BM25 hybrid và reranking. Chỉ mở chunking/context/generation/judge group khi evidence cho thấy bottleneck hoặc user yêu cầu.

## Local-first sequence bắt buộc

```text
Dense: intfloat/multilingual-e5-small, CPU, 384 dimensions
Sparse: custom TF-IDF-style SparseEmbedder
Lexical: Python BM25, initial k1=1.5 and b=0.75
Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2, CPU
```

Trên cùng active E5 collection:

1. Chạy `dense_only` trên 104 retrieval cases.
2. Chạy `hybrid_no_rerank` trên cùng cases và collection.
3. Chạy `hybrid_rerank` với cùng hybrid candidates/config.
4. Chạy approved stratified answer subset cho cấu hình cần đánh giá answer.
5. Ghi metrics, latency, failures, resource/cost và decision.

Chỉ sau khi local artifacts hợp lệ và đã review mới chuyển sang OpenRouter.

## OpenRouter sequence

Đối với mỗi verified OpenRouter embedding model:

1. Xác minh exact model ID, endpoint, dimension, input limit, Vietnamese evidence và price snapshot.
2. Xin user approval cho estimated request/token count và cost ceiling.
3. Xác minh artifacts collection cũ; xin approval xóa exact collection.
4. Tạo/reindex một collection cho embedding model mới.
5. Lặp đúng ba profiles với dataset/metrics frozen.
6. Native reranker experiment giữ pre-rerank candidates/config cố định.
7. Ghi failed run; không silent fallback.
8. Chỉ xóa collection khi artifacts/config/result files đã tồn tại và user approve transition.

Qwen3 Embedding là remote priority family. Qwen3-Reranker chỉ là candidate đến khi OpenRouter native support được verify. `cohere/rerank-v3.5` là native candidate cần re-verify catalog, price và Vietnamese suitability.

## Optional local Vietnamese models

DEk21/BKAI/AITeamVN candidates không chen giữa E5 baseline runs. Chúng chỉ mở sau:

- exact model ID/model card verified;
- license và training domain được ghi;
- dimension/pooling/instruction xác nhận;
- CPU RAM/disk/latency preflight chấp nhận;
- user approval cho download/resource use.

Candidate không đạt gate được ghi `skipped_resource_gate`, không gọi kết quả bằng 0.

## One-active-collection lifecycle

```text
verify model and dimension
  -> reset approval
  -> create exact dense+sparse schema
  -> ingest canonical chunks
  -> verify point count
  -> run all approved profiles
  -> verify JSONL and Markdown evidence
  -> transition approval
  -> delete exact collection
  -> next embedding model
```

Embedding không fallback theo request. Reranker có thể fallback ngoài benchmark nếu runtime policy cho phép, nhưng benchmark mode phải fail rõ.

Sau khi chọn winner:

1. Rebuild winner collection từ canonical corpus.
2. Verify model, dimension, schema và point count.
3. Rerun winner smoke/retrieval gate.
4. Set `reset_collection: false`.
5. Update ledger, Phase 8 reports và Project Status sau Codex approval.

## Controlled experiment rules

- Một run ID ánh xạ một immutable config snapshot.
- Chỉ đổi variables thuộc group đang xét.
- Dataset checksum, chunks, relevance version, metric code/version và k giữ giống nhau.
- Warm-up/cache policy và machine context được ghi cho latency.
- Failed/partial runs không bị xóa.
- Không average metrics từ runs có ground truth/corpus khác.
- Manual tuning tạo run mới, không overwrite.

## Selection framework

Trước khi chạy, brainstorming xác định:

- primary retrieval metric và minimum quality;
- answer quality floor cho accuracy/groundedness;
- maximum p95 retrieval/rerank latency;
- remote cost ceiling;
- complete-case rate/provider failure tolerance;
- tie-break order giữa quality, latency, cost và simplicity.

Không dùng composite score nếu weights chưa được user duyệt. Khuyến nghị dùng constraints trước, rồi Pareto comparison. Nếu không có winner tuyệt đối, user chọn trade-off và decision record giải thích.

## Generation experiment sau baseline

Baseline answer vẫn là OpenAI Agents SDK `gpt-5.4-nano`; judge là `gpt-5.4-mini`. Chỉ khi pipeline ổn định mới thử OpenRouter `qwen/qwen3.5-9b` trên cùng frozen answer subset, prompt/context và judge rubric.

Không đổi generator cùng lúc với embedding/reranker nếu mục tiêu là đo tác động retrieval.

## Brainstorming Level 3 bắt buộc

Codex và người dùng phải chốt:

1. Candidate list thực sự chạy trong vòng đầu.
2. Experiment order và stop criteria.
3. Primary metrics, quality floors, latency/cost ceilings và tie-break.
4. Exact paid-call budgets và approval boundaries.
5. Collection deletion checkpoints.
6. Cách xử lý variance/mâu thuẫn và rerun count.
7. Winner runtime config và rollback evidence.

Research phải ưu tiên model hỗ trợ tiếng Việt/multilingual. Giá và availability luôn re-verify.

## Nhiệm vụ của DeepSeek Implementer

- Không tự thay biến ngoài group.
- Trước run, emit safe config summary không chứa secret.
- Kiểm tra collection schema/count và dataset checksum.
- Chạy retrieval 104 cases; answer/judge theo approved subset.
- Ghi JSONL trước Markdown summary.
- Không xóa collection hoặc gọi paid API khi chưa approval.
- Không tuyên bố winner; cung cấp evidence.

## Nhiệm vụ của Codex Reviewer

- Audit comparability, metric math, artifacts, failures và cost.
- Re-run sample metric calculations độc lập.
- Reject uncontrolled comparisons và silent fallback.
- Xác nhận destructive transition evidence.
- Cùng user chọn winner hoặc yêu cầu focused rerun.
- Chỉ approve sau final winner collection được rebuild và protected.

## Notebook bắt buộc

`notebooks/08_benchmark_model_selection.ipynb` phải:

- import evaluation/benchmark readers thay vì duplicate metric hoặc selection logic;
- giải thích experiment groups, controlled variables, metrics, latency, reliability và cost bằng tiếng Việt;
- safe default chỉ đọc sample hoặc existing local artifacts đã được kiểm tra;
- không tự chạy paid benchmark, model download, collection reset/delete hoặc live API;
- hiển thị cách người dùng so sánh candidates và kiểm tra winner decision;
- giữ committed outputs rỗng và mọi `execution_count=null`.

## Validation và evidence

Mỗi run phải có:

```text
config snapshot
dataset checksum
collection metadata and point count
retrieval JSONL
answer/judge JSONL when applicable
summary overall and by category
latency/resource/cost summary
completed/failed case counts
decision and next action
```

Commands thực tế lấy từ approved Phase 4/7 implementation và ghi exact trong run record.

## Security, reliability và performance gates

- Paid calls bounded và approved.
- No secret/header/raw SDK object.
- Exact destructive target verification.
- Resume không duplicate/skip sai cases.
- Actual model/provider luôn được ghi.
- Winner có reproducible rebuild và reset disabled.

## Tiêu chí phê duyệt Phase 8

- Local E5 ba-profile ladder hoàn tất với valid artifacts.
- Approved OpenRouter candidates được chạy cùng protocol hoặc ghi rõ skip/failure.
- Comparisons controlled, metric/version/dataset nhất quán.
- User/Codex decision nêu trade-off dựa trên evidence.
- Winner collection được rebuild, verified và protected.
- Ledger/reports đầy đủ, không fabricated result.
- Notebook Phase 8 giải thích đúng artifacts và giúp người dùng xác nhận trade-off/winner.
- User report phản ánh đúng controlled comparisons, failures, cost và final selection; được người dùng xác nhận cùng notebook.

## Reports và cập nhật trạng thái

```text
reports/phase_8_benchmark_model_selection_implementation_report.md
reports/phase_8_benchmark_model_selection_codex_review.md
reports/hue_foods_rag_benchmark.md
reports/user_reports/phase_8_benchmark_model_selection_user_report.md
```

Sau technical review đạt, Codex tạo user report `pending`; chỉ cập nhật `Project_Status.md` sau khi người dùng xác nhận notebook/report và winner decision.

## Bước tiếp theo

Sau MVP benchmark, hệ thống vận hành với selected pipeline. Phase 9 chỉ mở design session riêng khi user muốn Agentic RAG.
