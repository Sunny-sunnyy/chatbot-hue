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
Lexical: Python BM25
Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2, CPU
Generator: gpt-5.4-nano
Judge: gpt-5.4-mini
```

Active production baseline target đã được user chốt là Qdrant dense-only; custom
TF-IDF sparse storage/schema sẽ được loại trong coordinated Phase 4–5
simplification. Canonical lexical path cho ba baseline profiles là dense Qdrant
candidates rồi Python BM25 fusion. Quyết định bỏ stored sparse không xóa BM25
hoặc CrossEncoder capability trước benchmark.

Ba retrieval profiles có exact mapping:

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

`hybrid_no_rerank` lấy dense candidates trước rồi thêm Python BM25. Profile
`hybrid_rerank` dùng đúng output đó và thêm CrossEncoder; nó không mở một
candidate-generation path khác. Không mặc định hybrid luôn tốt hơn
`dense_only`; winner phải đến từ observed metrics.

Ba profile trên không query Qdrant sparse vectors. BM25 chỉ chấm các dense
candidates nên không thể phục hồi tài liệu đã vắng khỏi dense candidate set.
Đây là baseline semantics cần được báo cáo đúng, không được gọi là native
dense+sparse retrieval.

## Isolated true-hybrid candidate

Phase 8 đánh giá true hybrid retrieval trong một controlled experiment riêng,
không thay đổi semantics của ba canonical profiles. Candidate path lấy dense và
sparse candidates độc lập rồi fusion trước optional reranking. Exact sparse
representation, candidate depths, fusion method và reranker setting phải được
user duyệt trong experiment design; guide này không mặc định trước winner hoặc
thuật toán chưa được đo.

Experiment phải:

- tạo exact isolated candidate collection có sparse vectors; không thêm sparse
  vào hoặc mutate active dense-only baseline collection;
- dùng cùng 572 canonical chunks, evaluation questions, metric definitions và
  dense model với run đối chứng;
- thay đổi duy nhất candidate-generation/fusion group trong comparison chính;
- ghi rõ dense candidate depth, sparse candidate depth, fusion và reranker state;
- báo cáo retrieval quality, end-to-end quality, latency, reliability và code/
  operational complexity;
- không coi việc collection chứa sparse vectors là bằng chứng retrieval tốt hơn;
- không chuyển candidate collection thành production hoặc thay đổi active config
  nếu chưa có real observed benefit và exact user-approved transition.

Nếu true-hybrid candidate không tạo lợi ích tương xứng, sparse storage không
được đưa trở lại production. Nếu có lợi ích, kết quả chỉ là evidence cho một
transition proposal; delete/recreate/reindex active collection vẫn là destructive
action cần user approval riêng.

## Experiment groups

Mỗi experiment chỉ thay đổi một nhóm biến:

| Group | Có thể thay đổi | Giữ cố định |
|---|---|---|
| Dense embedding | provider, model, dimension, instruction | chunks, evaluation data, retrieval settings |
| BM25/fusion | tokenizer, parameters, weights, candidate depth | dense model, corpus, reranker off |
| True-hybrid candidate generation | sparse representation, sparse candidate depth, fusion | dense model, corpus, evaluation data |
| Reranker | provider/model/top-k | pre-rerank candidates |
| Context | document/character limits | retrieval output và generator |
| Generator | provider/model/prompt/settings | context, questions và judge |

Chỉ mở một group khi Phase 7 hoặc user cho thấy vấn đề thật cần giải quyết.

## Dense embedding candidates và OpenRouter

Local E5 là control baseline. OpenRouter embedding chỉ được implement khi user
duyệt một dense-embedding experiment group cụ thể ở Phase 8.

Trước khi viết adapter hoặc chạy paid comparison phải xác minh lại bằng API và
catalog hiện hành:

- exact embeddings endpoint và response schema;
- exact provider/model ID;
- output dimension hoặc dimension parameter;
- query/document instructions hoặc input types;
- input/token limits và batching support;
- pricing, rate limits, timeout và observed provider reliability;
- multilingual/Vietnamese relevance đủ để đưa candidate vào controlled run.

Không mang lại `OpenRouterEmbedder`, config hoặc tests lịch sử từ Phase 3.
Adapter/config Phase 8 được viết theo actual candidate đã duyệt, chạy real API
và fail rõ; không mock HTTP, fake vector hoặc silent fallback sang local E5.

Nếu model có dimension hoặc vector space khác baseline, tạo exact isolated
collection/index cho candidate sau khi user duyệt transition. Không trộn vectors
từ hai models và không mutate active baseline collection.

Mỗi embedding candidate chạy trên cùng canonical chunks, evaluation questions,
retrieval settings và metrics. Khi user duyệt đủ scope, candidate được so sánh
trên cùng tập profile trong ba profile ở trên. Báo cáo tách rõ:

- retrieval quality/accuracy;
- embedding và end-to-end latency;
- failures, variance và reliability/stability giữa các run;
- actual API cost/usage quan sát được;
- độ phức tạp vận hành và code phải duy trì.

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
5. So sánh quality/accuracy, latency, reliability/stability, actual cost và độ
   phức tạp.
6. Loại candidate không tạo lợi ích tương xứng.
7. User chọn trade-off cuối.

True-hybrid candidate dùng isolated collection và chạy như experiment group
riêng sau local dense-only baseline. Không trộn kết quả của candidate-generation
experiment với BM25-weight hoặc reranker-model experiment trong cùng comparison.

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

Nếu true-hybrid candidate được mở, Phase 8 còn phải xác minh:

- active dense-only baseline collection không bị mutate;
- candidate collection và query path thực sự có stored/query sparse vectors;
- comparison giữ đúng corpus, questions, metrics và fixed variables;
- quyết định production dựa trên observed benefit lẫn complexity, không dựa trên
  sự tồn tại của sparse schema.

## Quyết định đã phê duyệt

```text
Decision: Giữ ba canonical profiles dense_only, hybrid_no_rerank và
hybrid_rerank với exact semantics dense candidates -> optional Python BM25 ->
optional CrossEncoder. Active production baseline là Qdrant dense-only.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn phương án A sau khi review Phase 8 và source llm_rag.
Affected scope: Phase 4–5 simplification, Phase 7 evaluation compatibility và
Phase 8 baseline comparisons.
Revisit trigger: Approved benchmark evidence yêu cầu thay đổi canonical profile.
```

```text
Decision: Phase 8 đánh giá true hybrid retrieval bằng isolated candidate
collection có sparse vectors và fair controlled comparison. Candidate không
mutate active dense-only baseline. Sparse storage chỉ được đề xuất quay lại
production khi real results chứng minh lợi ích tương xứng complexity; exact
production transition cần user approval riêng.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User yêu cầu ghi rõ candidate-collection experiment sau khi chọn
active-baseline phương án A.
Affected scope: Phase 8 experiment design, candidate collection lifecycle,
evaluation reports và eventual production transition proposal.
Open design details: sparse representation, fusion algorithm, candidate depths,
reranker state và exact candidate collection name sẽ được brainstorming trước
implementation; quyết định này chưa authorize code, paid run hoặc mutation.
Revisit trigger: Candidate experiment không còn cần thiết do evaluation evidence,
hoặc user thay đổi benchmark scope trước implementation authorization.
```

Commit/push cần yêu cầu riêng.
