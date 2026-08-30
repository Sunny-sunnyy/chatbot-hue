# Hue Foods RAG — Model và benchmark summary

Last updated: `2026-08-30 +07`

## Mục đích

File này giữ:

- model và pipeline baseline hiện hành;
- kết quả chạy thật còn hữu ích;
- giới hạn so sánh;
- quyết định benchmark hiện tại.

File không quản lý run package, identity, checksum, cost, resume hoặc artifact
audit. Kết quả chi tiết do chương trình Phase 7 ghi vào hai CSV đơn giản.

Chưa có model/profile winner được user và Reviewer phê duyệt.

## Baseline hiện hành

| Vai trò | Provider/model | Trạng thái |
|---|---|---|
| Dense embedding | Local `intfloat/multilingual-e5-small`, CPU, 384 dimensions | Baseline đã dùng |
| Sparse representation | Không còn `SparseEmbedder` trong runtime hiện hành | Legacy active collection có thể còn sparse fields vật lý; production target và dense candidate không dùng chúng |
| Lexical scoring | Python BM25 | Dùng trong hybrid profiles |
| Local reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2`, CPU | Baseline đã dùng; có giới hạn tiếng Việt |
| Answer generation | OpenAI `gpt-5.4-nano` | Phase 6/7 baseline |
| Answer judge | OpenAI `gpt-5.4-mini` | Phase 7 baseline |

Candidates cho Phase 8 chỉ được chạy sau khi exact provider/model và experiment
scope được user duyệt:

- local E5-small, Huydang DEk21 768D và E5-base;
- future paid OpenRouter `intfloat/multilingual-e5-large` và `baai/bge-m3`
  dense proposal sau khi local three hoàn tất;
- current local `cross-encoder/ms-marco-MiniLM-L-6-v2` reranker only;
- future answer model qua OpenRouter.

Không tự đổi provider/model hoặc silent fallback.

## Pipeline baseline

| Component | Hiện hành |
|---|---|
| Chunking | H2 sections; regular content tối đa 400 characters; tables giữ nguyên |
| Corpus | 572 curated food chunks |
| Dense | E5 small, normalized 384-dimensional vectors |
| Qdrant | `hue_foods_e5_small_384`, 572 points, cosine, hiện read-only; blue-green target là `hue_foods_e5_small_384_dense` |
| BM25 | `k1=1.5`, `b=0.75` |
| Hybrid fusion | Dense/BM25 normalized weighted sum |
| Reranker | Local MiniLM |
| Context | Tối đa 5 documents và 3,000 characters |
| Generator | `gpt-5.4-nano` |
| Judge | `gpt-5.4-mini` |

## Retrieval profiles

| Profile | Dense search | Python BM25 | Reranker |
|---|---:|---:|---:|
| `dense_only` | Có | Không | Không |
| `hybrid_no_rerank` | Có | Có | Không |
| `hybrid_rerank` | Có | Có | Có |

Stored sparse vectors còn tồn tại trong legacy active collection không có nghĩa
là native sparse retrieval đang chạy. `SparseEmbedder` đã bị loại khỏi runtime
sau Phase 4–5 simplicity implementation. User đã chốt production target
dense-only; Python BM25 và CrossEncoder vẫn được giữ cho ba profile.

Phase 8 sẽ đánh giá true hybrid retrieval bằng isolated candidate collection có
sparse vectors, không mutate active baseline. Candidate phải dùng cùng corpus,
questions và metrics, chỉ thay đổi approved candidate-generation/fusion group.
Sparse storage chỉ được đề xuất quay lại production nếu real results chứng minh
lợi ích tương xứng complexity và user duyệt exact transition.

## Kết quả retrieval thật đã quan sát

Ba kết quả dưới đây được chạy trước Phase 7 simplicity reset trên cùng 104 câu,
572-point E5 collection và ba profiles. Chúng là baseline tham khảo cho Phase 8,
không phải winner và không phải acceptance evidence của implementation Phase 7
mới.

| Profile | Cases | Recall@1/3/5/10 | MRR@10 | nDCG@5/10 | Macro Recall@5 | Keyword coverage @5/@10 | Median/p95 latency |
|---|---:|---|---:|---:|---:|---:|---|
| `dense_only` | 104/104 | 0.389 / 0.623 / **0.721** / 0.790 | 0.571 | 0.586 / 0.610 | **0.725** | 0.939 / 0.971 | 29 / 50 ms |
| `hybrid_no_rerank` | 104/104 | 0.366 / 0.632 / **0.712** / 0.813 | 0.566 | 0.577 / 0.610 | 0.700 | 0.942 / 0.984 | 28 / 40 ms |
| `hybrid_rerank` | 104/104 | 0.275 / 0.542 / **0.645** / 0.645 | 0.464 | 0.492 / 0.491 | 0.641 | 0.925 / 0.925 | 293 / 652 ms |

Ý nghĩa quan sát:

- `dense_only` có Recall@5 và macro Recall@5 cao nhất trong ba run cũ.
- `hybrid_no_rerank` có Recall@10 cao nhất và latency gần `dense_only`.
- MiniLM reranker làm giảm các retrieval metrics quan sát được và tăng latency
  rõ rệt.
- Kết quả chưa đủ để tuyên bố winner vì Phase 8 chưa chạy controlled model
  selection theo governance mới.

Các run answer/judge cũ dùng architecture và rubric đã bị Phase 7 reset thay
thế, nên không được giữ làm comparison baseline hiện hành.

## Phase 7 evaluation hiện hành

Phase 7 dùng luồng:

```text
question -> retrieve -> build context -> generate -> judge -> report
```

Đầu tiên chạy:

- 20 real questions trong `test2.jsonl`;
- profile `dense_only`;
- keyword-based MRR, nDCG và coverage;
- generation thật bằng `gpt-5.4-nano`;
- judge thật bằng `gpt-5.4-mini`;
- accuracy, completeness, relevance và feedback.

Sau khi ổn định, chỉ đổi input path sang bộ 104 câu. Output cố định:

```text
backend/evaluation/retrieval_results.csv
backend/evaluation/answer_results.csv
```

Hai CSV hiện mỗi file có 20 rows từ lần chạy gần nhất. Kết quả full-run 104 câu
đã được ghi như historical evidence trong Phase 7 implementation/Codex review
reports; không được mô tả chúng là nội dung hiện tại của CSV.

Golden Dataset V3 Gate 0 hiện hành đã được Reviewer và user phê duyệt với 45
full cases cùng exact 10-row smoke subset. Canonical lifecycle evidence:

```text
docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md
docs/superpowers/plans/2026-08-27-phase-8-golden-dataset-v3-implementation-plan.md
reports/phase_8_golden_dataset_v3_implementation_report.md
reports/phase_8_golden_dataset_v3_codex_review.md
```

Không có calibration, resume, run identity, checksum, package matching,
tamper detection, partial artifact, consent gate hoặc cost accounting.

## Quy tắc evidence

- Chỉ ghi kết quả từ exact real run.
- Dùng canonical data và actual service state.
- Không dùng mock/fake, replay hoặc prior output làm fresh evidence.
- Giữ đúng failed, skipped và partial outcome.
- Ghi model/profile/data cần thiết để hiểu kết quả, không tạo audit package.
- Paid API trong approved guide được phép.
- Active Hue collection chỉ read-only.

## Bước tiếp theo

1. Giữ baseline Phase 7 đã approved như historical state.
2. Giữ nguyên Golden Dataset V3 đã approved; không tối ưu dataset theo candidate.
3. Notebook 08a đã hoàn tất bằng real local models, canonical data và isolated
   Qdrant targets; Reviewer xác minh độc lập và user xác nhận.
4. Notebook 08b đã hoàn tất 20 settings, 70 calibration rows, 200 result rows
   và 900 per-case records; Reviewer xác minh độc lập và user xác nhận ngày
   `2026-08-30 +07`.
5. Unicode tokenizer được giữ. BM25 finalist và TF-IDF finalist đều là `None`
   vì category `relationship` có `delta nDCG@5=-0.0279273`, thấp hơn guardrail
   `-0.02`. Aggregate gain không override regression này.
6. Exact Notebook 08c written spec so sánh no-rerank với current MiniLM trên ba
   immutable Top-10 Foods inputs đã được user duyệt. Implementation plan/Review
   Contract đang chờ user review; implementation/run chưa được authorize.

## Giới hạn Foods-only và kế hoạch đánh giá lại đa lĩnh vực

Toàn bộ kết quả Phase 7 và Phase 8 hiện tại chỉ dựa trên corpus và Golden
Dataset của Foods. Vì vậy chúng có giá trị để so sánh có kiểm soát trong domain
Foods, nhưng chưa phải bằng chứng khách quan cho toàn bộ Hue RAG.

Sau khi 08c đóng, dự án sẽ mở scope riêng để hoàn thiện curated Markdown trong
toàn bộ `knowledge-base-hue/`: Foods, Festivals, Heritage, Tourism, Performing
Arts và các domain answer-facing được duyệt khác. Sau bước review dữ liệu sẽ cập
nhật chunking/metadata theo domain, tạo embedding mới, xây isolated full-corpus
index và tạo Combined Golden Dataset có quota/evidence cho tất cả domain.

Baseline evaluation bắt đầu lại từ Phase 7 trên corpus/Golden mới, sau đó chạy
lại các thí nghiệm Phase 8 bị ảnh hưởng. Báo cáo này tiếp tục được giữ làm
Foods historical baseline; không tự động carry forward model winner hoặc
production recommendation sang benchmark đa lĩnh vực.

Active Phase 8 không còn BGE/Qwen reranker candidates. Chúng bị loại vì
resource/integration complexity không cần thiết khi nhu cầu thật là đo current
lightweight MiniLM so với no-rerank. Historical references không phải execution
authorization.

Qwen3 Embedding 0.6B 384D đã được chạy đủ để tạo historical evidence nhưng bị
user loại khỏi local scope ngày `2026-08-29 +07`: chất lượng thấp hơn E5-small,
không đạt category guardrails và CPU indexing quá chậm. Không chạy lại Qwen,
không đưa nó vào 08b/08d hoặc finalist selection. Mười CSV rows của Qwen được
giữ làm historical evidence; cache model và isolated collection
`hue_foods_08a_qwen3_06b_384` đã được Reviewer xóa theo authorization riêng.

MiniLM-L12 384D cũng đã bị user loại khỏi local scope ngày `2026-08-29 +07`:
nDCG@5 chỉ `0.4709`, trượt 7/9 guardrails và truncate 83/572 chunks ở max length
128. Mười CSV rows được giữ làm historical evidence; cache và isolated
collection `hue_foods_08a_minilm_l12_384` đã bị xóa. Final local dense catalog
cho 08b/08d chỉ còn E5-small, Huydang DEk21 và E5-base.

Canonical Notebook 08a contract:

```text
docs/superpowers/specs/2026-08-28-phase-8-08a-embedding-benchmark-design.md
docs/superpowers/plans/2026-08-28-phase-8-08a-embedding-benchmark-implementation-plan.md
```

Canonical Notebook 08b evidence:

```text
docs/superpowers/specs/2026-08-29-phase-8-08b-retrieval-fusion-benchmark-design.md
reports/phase_8_08b_retrieval_fusion_benchmark_codex_review.md
evaluation/results/phase8_sparse_manifest.json
evaluation/results/phase8_sparse_results.csv
evaluation/results/phase8_sparse_cases.jsonl
```

Exact Notebook 08c written specification:

```text
docs/superpowers/specs/2026-08-30-phase-8-08c-reranker-benchmark-design.md
```

Approved Phase 4–5 blue-green checkpoint trước Phase 8: chạy fresh 104-question
retrieval-only comparison cho cả ba profiles trên current active baseline và
`hue_foods_e5_small_384_dense`. Run này chứng minh equivalence/regression cho
cutover; không dùng generator/judge và không tuyên bố profile winner.

## Guide liên quan

```text
guides/phase_3_embedding_sparse_representation.md
guides/phase_4_qdrant_ingestion.md
guides/phase_5_retrieval_profiles_reranking.md
guides/phase_7_retrieval_answer_evaluation.md
guides/phase_8_benchmark_model_selection.md
reports/phase_7_golden_dataset_audit.md
```
