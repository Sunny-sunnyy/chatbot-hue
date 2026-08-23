# Hue Foods RAG — Model và benchmark summary

Last updated: `2026-08-23 +07`

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
| Sparse representation | Custom TF-IDF-style `SparseEmbedder` | Baseline đã dùng |
| Lexical scoring | Python BM25 | Dùng trong hybrid profiles |
| Local reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2`, CPU | Baseline đã dùng; có giới hạn tiếng Việt |
| Answer generation | OpenAI `gpt-5.4-nano` | Phase 6/7 baseline |
| Answer judge | OpenAI `gpt-5.4-mini` | Phase 7 baseline |

Candidates cho Phase 8 chỉ được chạy sau khi exact provider/model và experiment
scope được user duyệt:

- OpenRouter Qwen3 embedding family;
- OpenRouter native reranker candidates;
- local Vietnamese embedding/reranker candidates;
- future answer model qua OpenRouter.

Không tự đổi provider/model hoặc silent fallback.

## Pipeline baseline

| Component | Hiện hành |
|---|---|
| Chunking | H2 sections; regular content tối đa 400 characters; tables giữ nguyên |
| Corpus | 572 curated food chunks |
| Dense | E5 small, normalized 384-dimensional vectors |
| Qdrant | `hue_foods_e5_small_384`, 572 points, cosine, read-only |
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

Stored sparse vectors không có nghĩa là native sparse retrieval đã chạy.

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

1. Implement và approve Phase 7 đơn giản.
2. Review và đơn giản hóa Phase 0 đến Phase 6.
3. Chạy lại affected Phase 7 evaluation sau thay đổi liên quan.
4. Chỉ Phase 8 mới so sánh đầy đủ profiles/models và đề xuất winner.

## Guide liên quan

```text
guides/phase_3_embedding_sparse_representation.md
guides/phase_4_qdrant_ingestion.md
guides/phase_5_retrieval_profiles_reranking.md
guides/phase_7_retrieval_answer_evaluation.md
guides/phase_8_benchmark_model_selection.md
```
