# Sổ bằng chứng benchmark Hue Foods RAG

Last updated: `2026-08-12 +07`

## Mục đích

File này là model registry và Markdown summary ledger cho các thử nghiệm Hue Foods RAG. Per-question outputs được lưu dạng JSONL trong `backend/evaluation/results/` sau khi Phase 7 implement; file này chỉ lưu protocol, cấu hình, summary, failure và quyết định có bằng chứng.

Tại thời điểm tạo ledger, chưa có Hue Foods retrieval hoặc answer benchmark run nào được ghi nhận. Không có model/profile winner.

## Quy tắc bằng chứng

- Không ghi số liệu ước đoán vào cột kết quả thực tế.
- Không ghi API key, auth header, raw provider payload hoặc chain-of-thought.
- Mỗi run có immutable run ID, config snapshot, dataset checksum và artifact paths.
- Failed/partial runs được giữ với status và safe error type.
- Benchmark mode không silent fallback.
- Paid API, model download và collection deletion cần user approval riêng.
- Model availability/pricing phải re-verify ngay trước run.

## Model registry

| Vai trò | Provider | Exact model ID | Execution | Hỗ trợ tiếng Việt | Dimension | License/cost | Verified +07 | Trạng thái | Evidence và ghi chú |
|---|---|---|---|---|---:|---|---|---|---|
| Dense baseline | Local/Hugging Face | `intfloat/multilingual-e5-small` | CPU | Multilingual | 384 | MIT; local resource | 2026-08-09 | `baseline_approved` | [Model card](https://huggingface.co/intfloat/multilingual-e5-small); dùng `query:`/`passage:` |
| Local reranker | Local/Hugging Face | `cross-encoder/ms-marco-MiniLM-L-6-v2` | CPU | Không thiết kế riêng cho tiếng Việt | N/A | Apache-2.0; local resource | 2026-08-09 | `baseline_approved_with_language_limit` | [Model card](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2); latency baseline từ `llm_rag` |
| Remote embedding | OpenRouter | `qwen/qwen3-embedding-0.6b` candidate | API | Multilingual, cần đo tiếng Việt | Provider dependent | Re-verify price | 2026-08-09 | `candidate_preflight_required` | [Model page](https://openrouter.ai/qwen/qwen3-embedding-0.6b); re-verify availability/dimension |
| Remote embedding lớn | OpenRouter | Qwen3 Embedding 4B/8B family | API | Multilingual | Provider dependent | Re-verify price | 2026-08-09 | `candidate_resource_cost_gate` | Chỉ chạy khi smaller candidate chưa đủ và user approve |
| Native reranker | OpenRouter | `cohere/rerank-v3.5` candidate | API | Cần benchmark tiếng Việt | N/A | Re-verify price | 2026-08-09 | `candidate_preflight_required` | [Rerank docs](https://openrouter.ai/docs/api-reference/reranking); re-verify catalog/model |
| Future reranker | OpenRouter | Qwen3-Reranker exact native ID | API | Multilingual candidate | N/A | Re-verify price | 2026-08-09 | `deferred_until_native_support` | [Qwen3-Reranker card](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B); local card không chứng minh OpenRouter support |
| Vietnamese embedding | Local/Hugging Face | `huyydangg/DEk21_hcmute_embedding_v2` | CPU candidate | Vietnamese | Chưa xác minh | Chưa xác minh | 2026-08-09 | `exact_id_unverified` | Không chạy trước khi exact repository/model card được xác minh |
| Vietnamese embedding | Local/Hugging Face | `bkai-foundation-models/vietnamese-bi-encoder` | CPU candidate | Vietnamese | Re-verify | Re-verify license/resource | 2026-08-09 | `optional_resource_preflight` | [Model card](https://huggingface.co/bkai-foundation-models/vietnamese-bi-encoder) |
| Vietnamese embedding | Local/Hugging Face | `AITeamVN/Vietnamese_Embedding_v2` | CPU candidate | Vietnamese | Re-verify | Re-verify license/resource | 2026-08-09 | `optional_resource_preflight` | [Model card](https://huggingface.co/AITeamVN/Vietnamese_Embedding_v2) |
| Vietnamese reranker | Local/Hugging Face | `AITeamVN/Vietnamese_Reranker` | Resource-preflight candidate | Vietnamese | N/A | Re-verify license/resource | 2026-08-09 | `optional_resource_preflight` | [Model card](https://huggingface.co/AITeamVN/Vietnamese_Reranker) |
| Vietnamese reranker | Local/Hugging Face | `namdp-ptit/ViRanker` | Resource-preflight candidate | Vietnamese | N/A | Re-verify license/resource | 2026-08-09 | `optional_resource_preflight` | [Model card](https://huggingface.co/namdp-ptit/ViRanker) |
| Answer baseline | OpenAI | `gpt-5.4-nano` | Agents SDK/API | Đo trên Hue Foods | N/A | Re-verify OpenAI price | 2026-08-09 | `approved_for_phase_6` | [Official docs](https://platform.openai.com/docs/models/gpt-5.4-nano); dùng `OPENAI_API_KEY` |
| Answer judge | OpenAI | `gpt-5.4-mini` | Agents SDK/API | Cần calibrate tiếng Việt | N/A | Re-verify OpenAI price | 2026-08-09 | `approved_for_phase_7` | [Official docs](https://platform.openai.com/docs/models/gpt-5.4-mini); tách answer model |
| Future answer | OpenRouter | `qwen/qwen3.5-9b` | API | Multilingual/Vietnamese candidate | N/A | Re-verify price | 2026-08-09 | `deferred_until_stable_baseline` | [Model page](https://openrouter.ai/qwen/qwen3.5-9b) |

## Pipeline component registry

| Component | Baseline | Thay đổi được | Primary evidence |
|---|---|---|---|
| Chunking | H2 sections, 400-character regular-content chunks; Markdown tables preserved whole | Rules/limit trong dedicated group | 572 chunks, retrieval, source integrity |
| Dense embedding | `multilingual-e5-small` | Local Vietnamese, OpenRouter Qwen3 | Recall/MRR/nDCG, latency, resource/cost |
| Sparse representation | Custom TF-IDF | Tokenizer/weighting | Vocabulary stability, keyword diagnostic |
| Lexical scoring | BM25 `k1=1.5`, `b=0.75` | k1/b/tokenizer | Retrieval delta, latency |
| Hybrid fusion | Normalized weighted sum | normalization, weights, candidate depth | Retrieval delta by category |
| Reranking | Local MiniLM CrossEncoder | OpenRouter native/Vietnamese candidates | Retrieval delta, p95 latency, cost |
| Context | Bounded ranked evidence | doc/token/character limits | Groundedness/completeness |
| Generator | `gpt-5.4-nano` | future `qwen/qwen3.5-9b` | Answer rubric, latency, cost |
| Judge | `gpt-5.4-mini` | rubric/version unless approved | Calibration consistency |

## Retrieval profiles

| Profile | Dense search | Python BM25 | Reranker | Sparse Qdrant query |
|---|---:|---:|---:|---:|
| `dense_only` | Có | Không | Không | Không |
| `hybrid_no_rerank` | Có | Có | Không | Không |
| `hybrid_rerank` | Có | Có | Có | Không |

Stored sparse vectors không làm thay đổi bảng này. Qdrant native sparse fusion sau này là profile/group mới cần approval.

## Thứ tự benchmark canonical

### Vòng 1: Local baseline

```text
intfloat/multilingual-e5-small collection
  -> dense_only, 104 retrieval cases
  -> hybrid_no_rerank, same collection and cases
  -> hybrid_rerank with cross-encoder/ms-marco-MiniLM-L-6-v2
  -> approved stratified answer/judge subset when required
  -> verify artifacts and record decision
```

### Vòng 2: OpenRouter

Với mỗi verified remote embedding model, reindex một active collection rồi lặp đúng ba profiles. Native reranker chỉ thay trong reranker group, giữ pre-rerank candidates cố định.

### Vòng 3: Optional candidates

Chỉ mở local Vietnamese hoặc larger remote model khi vòng trước không đạt quality floor hoặc có hypothesis rõ. Candidate không đạt resource/exact-ID gate được ghi skipped.

## Run record bắt buộc

```text
run_id
timestamp_utc_plus_7
status
experiment_group
hypothesis
dataset_path_and_checksum
corpus_and_chunk_count
retrieval_profile
embedding_provider_model_dimension_instructions
sparse_tokenizer_and_state_version
bm25_k1_b
qdrant_collection_schema_point_count
candidate_depth_top_k_threshold
normalization_and_fusion_weights
reranker_provider_model_top_k
context_limits
answer_provider_model_prompt_version
judge_provider_model_rubric_version
retrieval_metrics
answer_metrics
latency_resource_usage_cost
completed_failed_case_counts
artifact_paths
decision
next_action
```

## Collection transition checklist

```text
exact collection name
embedding provider and model
dense dimension and distance
sparse vector name/schema
point count
completed retrieval artifact paths
completed answer/judge artifacts when applicable
config snapshot path
user approval evidence
next model and dimension
```

Không dùng wildcard/prefix deletion. Sau winner selection phải rebuild winner và đặt `reset_collection: false`.

## Dataset và metrics contract

- Retrieval dataset: 104 rows từ `knowledge-base-hue/foods/evaluation/tests.jsonl`.
- Proper Recall/MRR/nDCG cần relevance definition đã approve.
- Keyword metrics phải ghi là proxy/diagnostic nếu chưa có gold sources.
- Report overall, per category, median/p95 latency và complete-case rate.
- Judge: accuracy, completeness, relevance, groundedness, scale 1–5.
- Answer/judge chạy stratified subset trước; full 104 cần approval riêng.

## Phase 4 ingestion evidence

Đây là bằng chứng tạo index, không phải retrieval benchmark và không chứng minh
native sparse retrieval hoặc model winner.

| Run ID | Status | Corpus checksum | Embedding | Qdrant | Schema | Points | Evidence | Decision |
|---|---|---|---|---|---|---:|---|---|
| `phase4-ingestion-20260812` | `completed` | SHA-256 `936063a91a69083fe7070096da17656920cff3b93917a3e6fcc4384d697c8fde` trên 572 chunk dictionaries | Local `intfloat/multilingual-e5-small`, 384, `passage:` | Qdrant 1.18.3, `hue_foods_e5_small_384` | `dense` 384 cosine + indexed `sparse` | 572 | `reports/phase_4_qdrant_ingestion_implementation_report.md`; `reports/phase_4_qdrant_ingestion_codex_review.md` | Index đạt schema/count/identity gate; chưa chạy retrieval |

Run dùng `backend/config/settings.yaml`, E5 offline từ cache và Qdrant image pin
bằng digest trong `docker-compose.yml`. Read-only audit xác nhận expected/actual
UUID5 ID sets bằng nhau và toàn bộ payload identity khớp model/dimension.

## Retrieval results

Chưa có retrieval benchmark run nào được ghi nhận.

| Run ID | Status | Profile | Embedding | Reranker | Cases | Recall@k | MRR | nDCG@k | Keyword coverage | Median/p95 latency | Artifact | Decision |
|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|

## Answer và judge results

Chưa có answer hoặc judge benchmark run nào được ghi nhận.

| Run ID | Status | Generation | Judge | Cases | Accuracy | Completeness | Relevance | Groundedness | Latency/cost | Artifact | Decision |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|

## Failed và skipped runs

Không có failed hoặc skipped run nào được ghi nhận.

| Run ID | Status | Stage | Model/profile | Safe error hoặc gate | Completed cases | Artifact | Next action |
|---|---|---|---|---|---:|---|---|

## Final selection

Chưa có final embedding, profile, reranker hoặc generation model được chọn từ Hue Foods benchmark evidence.

Final selection chỉ ghi sau khi candidates vượt quality/reliability floors, user quyết định trade-off, Codex audit comparability, winner collection rebuild/verify và reset đặt `false`.

## Liên kết phase

```text
guides/phase_3_embedding_sparse_representation.md
guides/phase_4_qdrant_ingestion.md
guides/phase_5_retrieval_profiles_reranking.md
guides/phase_7_retrieval_answer_evaluation.md
guides/phase_8_benchmark_model_selection.md
```
