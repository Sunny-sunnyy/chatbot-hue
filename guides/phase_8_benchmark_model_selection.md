# Phase 8 — Benchmark và lựa chọn model/pipeline

## Trạng thái

`not_ready`

Phase 8 chưa có implementation authorization. Chỉ mở sau khi:

1. Phase 7 đơn giản được `approved`;
2. Phase 0 đến Phase 6 đã được review và đơn giản hóa bằng Repo, live system và
   tài liệu bổ sung thực sự hữu ích nếu có;
3. affected Phase 7 evaluation đã được chạy lại.

## Mục tiêu

So sánh các lựa chọn Hue Foods RAG bằng cùng dữ liệu và metric để user chọn
trade-off giữa quality, latency, reliability và simplicity.

Không chọn winner theo leaderboard ngoài domain hoặc cảm tính. Không xây
benchmark orchestration trước khi user duyệt candidates và phép so sánh thật sự
cần chạy.

## Baseline

Local baseline:

```text
Dense: intfloat/multilingual-e5-small, CPU, 384 dimensions
Sparse: custom TF-IDF-style SparseEmbedder
Lexical: Python BM25
Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2, CPU
Generator: gpt-5.4-nano
Judge: gpt-5.4-mini
```

Ba retrieval profiles:

- `dense_only`;
- `hybrid_no_rerank`;
- `hybrid_rerank`.

## Experiment groups

Mỗi experiment chỉ thay đổi một nhóm biến:

| Group | Có thể thay đổi | Giữ cố định |
|---|---|---|
| Dense embedding | provider, model, dimension, instruction | chunks, evaluation data, retrieval settings |
| BM25/fusion | tokenizer, parameters, weights, candidate depth | dense model, corpus, reranker off |
| Reranker | provider/model/top-k | pre-rerank candidates |
| Context | document/character limits | retrieval output và generator |
| Generator | provider/model/prompt/settings | context, questions và judge |

Chỉ mở một group khi Phase 7 hoặc user cho thấy vấn đề thật cần giải quyết.

## So sánh công bằng

- Dùng cùng canonical corpus và evaluation questions.
- Giữ metric definition và k giống nhau.
- Chỉ đổi variables thuộc experiment group đang xét.
- Ghi rõ actual provider, model, profile và settings cần để hiểu kết quả.
- Không silent fallback.
- Không gộp metrics từ dữ liệu hoặc ground truth khác nhau.
- Giữ failed/skipped/partial outcome đúng như quan sát.
- Không dùng run ID, checksum, package matching hoặc artifact audit.

Một comparison có thể được hiểu và chạy lại bằng input path, model/profile
settings và command/notebook đơn giản; không cần immutable run package.

## Trình tự

1. Chạy lại local baseline qua Phase 7 evaluation.
2. Xác định failure hoặc limitation thật.
3. User duyệt candidate và một experiment group.
4. Chạy candidate bằng cùng dữ liệu/metric.
5. So sánh quality, latency, reliability và độ phức tạp.
6. Loại candidate không tạo lợi ích tương xứng.
7. User chọn trade-off cuối.

Remote embedding có dimension khác cần exact reindex design. Active collection
không bị xóa hoặc thay đổi nếu user chưa duyệt exact transition.

## Real execution

Reviewer và Implementer được dùng online, model download và paid API nằm trong
approved Phase 8 guide/design. Không cần consent gate, cost cap hoặc code tính
chi phí.

Không dùng mock/fake, replay output hoặc synthetic benchmark làm evidence. Dùng
actual backend, canonical data, Qdrant, models và APIs.

## Notebook 08

`notebooks/08_benchmark_model_selection.ipynb` phải:

- giải thích candidates và biến được giữ cố định;
- mỗi cell làm một việc;
- gọi backend/evaluation functions rõ ràng;
- chạy approved real comparison;
- hiển thị metrics, latency, failures và ý nghĩa;
- không là validator, audit package hoặc test suite;
- giữ repository outputs rỗng và execution counts null.

## Reports

Implementation report ghi:

- comparison đã được duyệt;
- exact real commands/notebook;
- observed metrics và latency;
- failures/limitations;
- handoff cho Reviewer.

Codex review chạy lại comparison cần thiết và kiểm tra:

- cùng data/metrics;
- chỉ một experiment group thay đổi;
- actual provider/model/profile đúng;
- không fallback hoặc fabricated result;
- complexity có tương xứng lợi ích.

Benchmark summary cập nhật tại
`reports/hue_foods_rag_benchmark.md`.

## Acceptance

Phase 8 chỉ `approved` khi:

1. candidate scope được user duyệt;
2. comparisons dùng real system và cùng data/metrics;
3. Reviewer xác minh kết quả độc lập;
4. winner hoặc quyết định giữ baseline có lý do dễ hiểu;
5. configuration cuối được chạy lại;
6. notebook 08 giúp user hiểu và tự kiểm tra;
7. user xác nhận kết quả.

Commit/push cần yêu cầu riêng.
