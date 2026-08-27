# Phase 8 — Benchmark và lựa chọn model/pipeline

## Trạng thái

`not_ready`

Phase 8 chưa có implementation authorization. Chỉ mở sau khi:

1. Phase 7 đơn giản được `approved`;
2. Phase 0 đến Phase 6 đã được review và đơn giản hóa bằng Repo, live system và
   tài liệu bổ sung thực sự hữu ích nếu có;
3. affected Phase 7 evaluation đã được chạy lại.

Ngoài các gate trên, user đã xác nhận golden dataset correction là một scope
riêng phải hoàn tất trước mọi Phase 8 benchmark. Session Phase 8 hiện tại chỉ
thiết kế khung, thứ tự thí nghiệm và tiêu chí lựa chọn; không sửa dataset, cài
GPU/CUDA, viết code benchmark hoặc chạy model.

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

Phase 8 còn bắt buộc một end-to-end reference baseline mang exact flow đang
dùng trong `llm_rag`, nhưng chạy trên Hue corpus/golden data để comparison hợp
lệ:

```text
Name: llm_rag_reference_on_hue
Embedding: intfloat/multilingual-e5-small, 384D
Candidate generation: dense top 30
Lexical scoring: BM25 chỉ trên 30 dense candidates
Fusion: raw 0.6 * dense_score + 0.4 * bm25_score, không normalize
Pre-rerank output: top 10
Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2, input 10 -> output 5
Context: tối đa 5 whole chunks và 3000 ký tự
Generator: qwen/qwen3.5-9b qua OpenRouter
Judge: gpt-5.4-mini
```

Baseline này giữ cả raw-score fusion dù dense/BM25 khác scale vì mục tiêu là
tái hiện đúng reference flow, không tuyên bố nó là phương pháp fusion tốt. Source
runtime là chuẩn: `llm_rag` lấy dense 30, cắt hybrid còn 10 rồi mới rerank còn 5;
một câu mô tả rerank 30 trong deep-dive không override runtime source.

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

### Retrieval capability set đã xác nhận

Phase 8 phải tạo real evidence cho toàn bộ các retrieval paths sau:

| Path | Candidate generation/fusion semantics | Embedding dependency |
|---|---|---|
| Dense-only | Qdrant dense retrieval | Chạy cho cả bảy dense configurations |
| BM25-only | Python BM25 sinh candidates độc lập trên toàn corpus | Chạy một lần; không phụ thuộc dense embedding |
| Dense → BM25 rescoring | Dense candidates trước, BM25 chỉ chấm lại candidate set hiện hành | Chạy cho cả bảy dense configurations |
| True hybrid dense + BM25 | Dense và full-corpus BM25 sinh candidates độc lập rồi fusion | Chạy cho cả bảy dense configurations |
| TF-IDF sparse-only | Custom `SparseEmbedder` sinh/query sparse candidates độc lập | Experimental control chạy một lần |
| True hybrid dense + TF-IDF | Dense và custom TF-IDF sparse sinh candidates độc lập rồi fusion | Chạy cho cả bảy dense configurations |
| BGE-M3 learned sparse-only | Learned sparse output của BGE-M3 sinh/query candidates | Chỉ áp dụng cho BGE-M3 |
| BGE-M3 dense + learned sparse | Dense và learned sparse BGE-M3 sinh candidates độc lập rồi fusion | Chỉ áp dụng cho BGE-M3 |

Coverage đầy đủ nghĩa là mọi component/path và mọi tổ hợp tương thích ở trên có
kết quả thật, không phải lặp cùng một computation dưới tên cấu hình khác. BM25-
only và TF-IDF sparse-only không chạy lại sáu lần theo embedding; BGE-M3 learned
sparse không gắn giả tạo vào model không sinh representation đó.

`08b_retrieval_fusion_benchmark.ipynb` giải thích và đo từng path. Sau đó
`08d_full_pipeline_matrix.ipynb` kết hợp từng valid pre-rerank pipeline với
no-rerank và ba reranker candidates để quan sát interaction trước khi chọn
end-to-end finalists.

### Fusion methods đã xác nhận

True-hybrid paths bắt đầu với đúng hai fusion methods:

| Fusion | Vai trò |
|---|---|
| Reciprocal Rank Fusion (RRF) | Primary rank-based comparison; không cộng trực tiếp các score khác scale |
| Independent min-max rồi weighted sum `0.6 dense / 0.4 sparse` | Giữ baseline weighting hiện hành để so sánh |

Không grid-search thêm weights trong initial matrix. Chỉ mở targeted weight
tuning nếu observed evidence cho thấy weighted fusion tạo lợi ích thật và tuning
có khả năng thay đổi quyết định cuối. Quy tắc này áp dụng cho dense+BM25,
dense+TF-IDF và BGE-M3 dense+learned-sparse; mỗi path phải ghi rõ fusion method
trong bảng kết quả.

### Candidate, rerank và context depth đã xác nhận

```text
Dense candidate depth: 30
BM25/sparse candidate depth: 30
Fusion/pre-rerank output: top 10
Reranker input: 10
Reranker output: top 5
No-rerank final comparison: top 5 của pre-rerank ranking
Generator context: tối đa 5 whole chunks và 3000 ký tự
```

Top 10 là input cho reranker, không phải số chunks đưa vào LLM. Retrieval report
tách tầng: candidate Recall@30, fusion/pre-rerank Recall@10, và final
MRR@5/nDCG@5/Recall@5. Nhờ đó no-rerank và rerank được so công bằng ở cùng final
depth 5, đồng thời vẫn biết relevant chunk bị mất ở candidate generation hay
fusion. Character budget có thể làm context thực tế chứa ít hơn 5 chunks.

## Experiment groups

Mỗi experiment chỉ thay đổi một nhóm biến:

| Group | Có thể thay đổi | Giữ cố định |
|---|---|---|
| Dense embedding | provider, model, dimension, instruction | chunks, evaluation data, retrieval settings |
| BM25/fusion | tokenizer, parameters, weights, candidate depth | dense model, corpus, reranker off |
| True-hybrid candidate generation | sparse representation, sparse candidate depth, fusion | dense model, corpus, evaluation data |
| Reranker | provider/model/top-k | pre-rerank candidates |
| Context | fixed maximum 5 whole chunks/3000 characters | retrieval output và generator |
| Generator | provider/model/prompt/settings | context, questions và judge |

Chỉ mở một group khi Phase 7 hoặc user cho thấy vấn đề thật cần giải quyết.

### Tokenizer tiếng Việt đã xác nhận cho Notebook 08b

BM25 chạy một controlled comparison giữa:

- control hiện hành: lowercase rồi tách token bằng Unicode `\w+`;
- Underthesea: `word_tokenize(..., format="text")` để phân đoạn từ tiếng Việt.

Hai biến thể dùng cùng corpus, BM25 parameters, questions, candidate depth và
metrics; báo cáo quality theo category cùng tokenization/query latency.
Underthesea chỉ trở thành dependency runtime nếu kết quả thật chứng minh lợi ích
tương xứng latency và maintenance cost. Initial scope không thêm PyVi,
VnCoreNLP hoặc tokenizer grid.

## Dense embedding candidates và OpenRouter

Local E5 là control baseline. OpenRouter embedding chỉ được implement khi user
duyệt một dense-embedding experiment group cụ thể ở Phase 8.

### Candidate set và thứ tự chạy đã xác nhận

Các local open-source embedding được chạy tuần tự từ nhẹ đến nặng/mạnh hơn.
Thứ tự là execution order để giảm rủi ro tài nguyên và tạo baseline sớm; nó
không phải xếp hạng chất lượng được giả định trước.

| Thứ tự | Model | Vector/đặc điểm cần giữ trong manifest | Trạng thái tiếng Việt |
|---:|---|---|---|
| 1 | `intfloat/multilingual-e5-small` | 384D; control hiện hành | multilingual; benchmark domain vẫn quyết định |
| 2 | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | 384D; candidate nhẹ | multilingual; benchmark domain vẫn quyết định |
| 3 | `intfloat/multilingual-e5-base` | 768D | multilingual; benchmark domain vẫn quyết định |
| 4 | `intfloat/multilingual-e5-large` | 1024D | multilingual; benchmark domain vẫn quyết định |
| 5 | `BAAI/bge-m3` | 1024D; hỗ trợ dense, learned sparse và multi-vector | multilingual; benchmark dense và sparse/hybrid tách group |
| 6a | `Qwen/Qwen3-Embedding-0.6B` | 384D MRL variant; instruction-aware | multilingual; lightweight/storage trade-off |
| 6b | `Qwen/Qwen3-Embedding-0.6B` | native 1024D; instruction-aware | multilingual; maximum-quality variant |

Đây là sáu embedding model families nhưng bảy dense configurations. Không chạy
Qwen3 768D trong initial scope: 384D đo trade-off nhẹ và 1024D đo native quality
đã đủ trả lời quyết định. Hai Qwen dimensions dùng isolated indexes riêng; Qwen
384D không được ghi vào E5-small collection chỉ vì có cùng dimension.

Không loại một candidate chỉ vì model card không ghi riêng tiếng Việt. Mọi
candidate phải được đo trên corrected Vietnamese golden dataset. Language claim
chỉ là risk indicator; observed retrieval quality, latency và regression theo
category mới quyết định giữ/bỏ.

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
- Cùng một bảng xếp hạng latency không trộn kết quả CPU của model này với GPU
  của model khác; hardware/device, dtype, batch size và cold/warm state phải
  được ghi rõ.
- Ghi riêng indexing/embedding latency, query embedding latency, retrieval,
  reranking và generation; latency online báo ít nhất warm p50/p95 và cold
  start được tách riêng.

Một comparison có thể được hiểu và chạy lại bằng input path, model/profile
settings và command/notebook đơn giản; không cần immutable run package.

## Trình tự

0. Hoàn tất và phê duyệt golden dataset correction ở scope riêng.
1. Chạy lại local baseline qua Phase 7 evaluation.
2. Chạy dense embedding candidates theo thứ tự nhẹ đến mạnh đã khóa ở trên.
3. Trên cùng fixed dense evidence, so sánh BM25/fusion và true-hybrid candidate
   generation, gồm BM25 độc lập, custom TF-IDF sparse chỉ như experimental
   control, và learned sparse của BGE-M3.
4. Chạy reranker candidates từ nhẹ đến mạnh trên cùng pre-rerank candidate
   artifacts.
5. Chạy end-to-end finalists với fixed generator/judge đã xác nhận.
6. So sánh quality tiếng Việt, latency, reliability/stability, actual cost và
   độ phức tạp vận hành.
7. Áp dụng selection rule, trình evidence để user chọn cấu hình cuối.

Local retrieval/reranking dùng full compatibility-aware matrix: mọi valid pre-
rerank path được ghép với no-rerank và ba reranker candidates. Staged selection
chỉ áp dụng sau matrix này để chọn số ít finalists chạy paid generation/judge;
không chạy paid answer evaluation cho mọi local combination.

### Reranker candidates và thứ tự chạy

| Thứ tự | Model | Language claim trên model card | Vai trò Phase 8 |
|---:|---|---|---|
| 1 | `cross-encoder/ms-marco-MiniLM-L-6-v2` | English | baseline rất nhẹ/nhanh; đo đầy đủ bằng tiếng Việt |
| 2 | `BAAI/bge-reranker-base` | Chinese, English | candidate trung bình; chỉ giữ nếu evidence tiếng Việt đạt gate |
| 3 | `Qwen/Qwen3-Reranker-0.6B` | multilingual | candidate nặng hơn và là ứng viên tiếng Việt chính |

Code hoạt động và trả score với text tiếng Việt không tự chứng minh model cải
thiện ranking. `llm_rag` dùng MiniLM thành công ở mức integration, nhưng không có
quality benchmark riêng cho reranker thật; Hue RAG vì vậy giữ MiniLM làm
lightweight baseline và quyết định bằng corrected golden evidence.

### Generator và judge đã xác nhận

```text
Generator: qwen/qwen3.5-9b qua OpenRouter
Judge: gpt-5.4-mini
```

Generator/judge được giữ cố định khi so retrieval và reranking. Generator chỉ
được gọi ở end-to-end group sau khi retrieval evidence đã được khóa, tránh dùng
answer quality để che regression retrieval.

### Selection rule đã xác nhận

Nếu chênh lệch chất lượng tiếng Việt giữa các candidates không đáng tin cậy,
chọn model/pipeline nhẹ hơn, nhanh hơn và đơn giản hơn. Chỉ chọn candidate nặng
hơn khi nó tạo cải thiện chất lượng rõ ràng, không gây regression ở category
quan trọng và latency/độ phức tạp vẫn chấp nhận được. Không chọn winner chỉ vì
mean score cao hơn rất nhỏ.

Exact statistical comparison và category gates tiếp tục được thiết kế sau khi
corrected golden dataset được duyệt.

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

GPU không phải điều kiện bắt buộc: mọi local embedding/reranker phải có CPU
fallback. GTX 1650/WSL2 enablement được tách sang session khác và không nằm
trong authorization của design này. Nếu GPU được bật trước benchmark, tất cả
candidates trong cùng latency comparison phải chạy trên cùng device policy;
không cài CUDA/PyTorch hoặc đổi lockfile trong session brainstorming này.

## Notebook 08

Phase 8 dùng notebook theo experiment group, không tạo một notebook vật lý cho
mỗi pipeline combination:

```text
notebooks/08a_embedding_benchmark.ipynb
notebooks/08b_retrieval_fusion_benchmark.ipynb
notebooks/08c_reranker_benchmark.ipynb
notebooks/08d_full_pipeline_matrix.ipynb
notebooks/08e_generation_finalists.ipynb
notebooks/08_benchmark_model_selection.ipynb
```

Năm notebook `08a` đến `08e` chạy và giải thích từng experiment group. Notebook
`08_benchmark_model_selection.ipynb` chỉ tổng hợp các kết quả thật, giải thích
trade-off và hỗ trợ user chọn winner; không chạy lại toàn bộ matrix.

Mỗi notebook phải:

- giải thích candidates và biến được giữ cố định;
- có heading và markdown ngắn trước mỗi phần/model để nói mục đích, điều sắp
  chạy, thời gian/tài nguyên cần chú ý và cách đọc output;
- mỗi cell làm một việc;
- gọi backend/evaluation functions rõ ràng;
- chạy approved real comparison;
- hiển thị metrics, latency, failures và ý nghĩa;
- dùng code trực tiếp, dễ hiểu; chỉ tạo helper nhỏ khi nó thực sự giảm lặp;
- không là validator, audit package, test suite, run registry hoặc resume engine;
- giữ repository outputs rỗng và execution counts null.

Phong cách trình bày bắt buộc tham khảo:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/*.ipynb
/home/minhhieu/llm_rag/tai_lieu/notebook_simple/**/*.ipynb
```

Chỉ kế thừa cách dạy theo section, giải thích trước code, cell ngắn và output dễ
đọc. Không kế thừa fake/demo data hoặc abstraction vượt nhu cầu; Phase 8 vẫn
chạy actual Hue data, Qdrant, local models và approved APIs.

### Kết quả và restart kernel

Mỗi notebook group giữ đúng một cumulative CSV đơn giản:

```text
evaluation/results/phase8_embedding_results.csv
evaluation/results/phase8_retrieval_results.csv
evaluation/results/phase8_reranker_results.csv
evaluation/results/phase8_pipeline_matrix.csv
evaluation/results/phase8_generation_results.csv
```

Không tạo run ID, timestamp package, checksum manifest, JSON song song hoặc
opaque `configuration_id`. Các cột dễ đọc như `embedding`, `retrieval`,
`reranker`, `device`, `dtype`, `top_k` đủ nhận diện một cấu hình. Chỉ giữ
`status` và `error` tối thiểu để không silently drop một real failure. Category
table được giữ vì aggregate mean có thể che regression ở nhóm câu hỏi quan
trọng.

Sau mỗi model/configuration chạy thành công, notebook hiển thị kết quả, cập nhật
dòng tương ứng trong CSV rồi giải phóng model, tensor/embedding lớn, chạy Python
garbage collection và clear CUDA cache nếu có. Không cần memory manager. Khi
restart kernel, cell setup đọc lại cumulative CSV để hiển thị tiến độ; không
dựa vào in-memory variables hoặc saved notebook output làm checkpoint.

Trong lúc chạy tương tác, user có thể thấy và lưu output cục bộ. Trước commit,
canonical notebooks phải được làm sạch outputs/execution counts; CSV là kết quả
bền vững dùng cho notebook tổng hợp và review.

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

## Gate 0 Golden Dataset V3 đã duyệt về thiết kế

Canonical files:

```text
session_prompt/phase_8_golden_dataset_v3_implementer_prompt.md
session_prompt/phase_8_golden_dataset_v3_reviewer_prompt.md
docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md
docs/superpowers/plans/2026-08-27-phase-8-golden-dataset-v3-implementation-plan.md
```

V2 dừng ở historical `changes_requested` sau ba vòng. V3 là complexity reset đã
được user duyệt: Implementer tạo full `golden_v3.jsonl` ở mức cao nhất đạt chất
lượng trong đúng `40`, `45`, `50` và exact 10-row smoke subset. Không còn quota
category, source family hoặc ma trận chéo. Mọi case vẫn dùng binary exact
source/section relevance và Phase 7/V2 files phải giữ nguyên.

Không chạy Phase 8 benchmark cho tới khi Reviewer kiểm tra direct evidence,
deterministic validator, real retrieval metadata, toàn bộ câu hỏi/reference và
user chấp nhận Gate 0 trên dữ liệu đã triển khai.

## Backlog brainstorming sau Gate 0 implementation

Sau khi Golden Dataset V3 được Reviewer/user chấp nhận, tạo handoff brainstorming
mới dựa trên final 40/45/50 distribution. Handoff V2 cũ không còn canonical.

Tiếp tục theo thứ tự:

1. category regression blockers, uncertainty và clear-quality-gain rule dựa
   trên final V3 distribution đã duyệt;
2. exact embedding query/document instructions, pooling, normalization,
   truncation, dimension, dtype và batch size;
3. exact reranker input format, truncation và batch size; depth đã khóa 10→5;
4. BGE-M3 learned-sparse representation, isolated Qdrant schema/query path,
   collection names và retention/cleanup policy;
5. BM25 parameters cho comparison tokenizer Unicode versus Underthesea;
6. exact non-duplicate matrix manifest và execution order;
7. warm-up/repetition, cold/warm p50/p95, memory, failure/OOM và device policy;
8. paid finalist gate/count, Qwen generation settings, GPT judge rubric và
   repetition policy;
9. exact readable CSV columns/category views, notebook update/cleanup behavior,
   focused tests và Reviewer Run All commands;
10. final winner rerun, report/handoff và proposal production riêng. Không tự
   cutover, mutate active collection hoặc cleanup candidate data.

GPU/WSL2 GTX 1650 remediation vẫn ở session riêng. Ngay trước implementation/
execution phải kiểm tra lại model availability, IDs, licenses, dimensions,
provider schemas/limits và resource compatibility từ nguồn chính thức; không
dùng việc kiểm tra này để tự mở rộng candidate scope.

## Acceptance

Phase 8 chỉ `approved` khi:

1. candidate scope được user duyệt;
2. comparisons dùng real system và cùng data/metrics;
3. Reviewer xác minh kết quả độc lập;
4. winner hoặc quyết định giữ baseline có lý do dễ hiểu;
5. configuration cuối được chạy lại;
6. nhóm notebook 08 giúp user hiểu, học và tự chạy lại từng experiment;
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
Open design details: physical sparse representation/schema, exact BM25
parameters cho tokenizer comparison và exact candidate collection names sẽ
được brainstorming trước implementation;
quyết định này chưa authorize code, paid run hoặc mutation.
Revisit trigger: Candidate experiment không còn cần thiết do evaluation evidence,
hoặc user thay đổi benchmark scope trước implementation authorization.
```

```text
Decision: Phase 8 thử local open-source embedding và reranker tuần tự từ nhẹ
đến mạnh; đánh giá bằng corrected Vietnamese golden dataset, quality theo
category và latency thật. Model không bị loại chỉ vì thiếu Vietnamese claim,
nhưng chỉ được giữ khi evidence tiếng Việt đạt gate. Khi quality không khác
biệt đáng tin cậy, ưu tiên model/pipeline nhẹ, nhanh và đơn giản hơn.
Approved by: User
Approval date +07: 2026-08-26
Evidence: User xác nhận thứ tự nhẹ đến mạnh, yêu cầu chú ý latency/tiếng Việt và
đồng ý selection rule do Reviewer đề xuất.
Affected scope: Phase 8 candidate ordering, evaluation dimensions và final
model/pipeline selection.
```

```text
Decision: Phase 8 end-to-end finalists dùng `qwen/qwen3.5-9b` qua OpenRouter;
judge giữ `gpt-5.4-mini`. GPU/WSL2 GTX 1650 enablement được xử lý ở session khác;
CPU vẫn là fallback được chấp nhận.
Approved by: User
Approval date +07: 2026-08-26
Affected scope: Phase 8 generation boundary, judge consistency và execution
environment documentation.
Revisit trigger: Provider/model availability thay đổi trước real execution hoặc
GPU session xác minh một device policy khác cần user phê duyệt.
```

```text
Decision: Phase 8 tạo real comparison evidence cho tám retrieval paths:
dense-only, BM25-only toàn corpus, dense->BM25 rescoring hiện hành, true hybrid
dense+BM25, TF-IDF SparseEmbedder-only, true hybrid dense+TF-IDF, BGE-M3 learned
sparse-only và BGE-M3 dense+learned-sparse hybrid. Full local matrix bao phủ mọi
tổ hợp tương thích với no-rerank và ba rerankers, nhưng không nhân bản retrieval
không phụ thuộc embedding hoặc tạo capability pairing không có thật.
Approved by: User
Approval date +07: 2026-08-26
Evidence: User yêu cầu đầy đủ, đa dạng kết quả và xác nhận exact retrieval set.
Affected scope: Notebook 08b, Notebook 08d, local result matrix và final
comparison evidence.
```

```text
Decision: Initial true-hybrid matrix so sánh đúng hai fusion methods: RRF và
independent min-max weighted sum với `0.6 dense / 0.4 sparse`. Không grid-search
weights trước khi real evidence cho thấy targeted tuning là cần thiết.
Approved by: User
Approval date +07: 2026-08-26
Evidence: User xác nhận Reviewer recommendation để giữ comparison đa dạng nhưng
không over-engineer.
Affected scope: Notebook 08b/08d, fusion result columns và local matrix size.
```

```text
Decision: Bắt buộc `llm_rag_reference_on_hue` exact baseline và depth contract:
dense/sparse generation top 30, fusion top 10, reranker input 10/output 5,
no-rerank final slice top 5, generator context tối đa 5 whole chunks/3000 ký tự.
Retrieval report tách Recall@30, Recall@10 và final metrics @5.
Approved by: User
Approval date +07: 2026-08-26
Evidence: User yêu cầu baseline đúng flow runtime của llm_rag và xác nhận revised
depth/context proposal sau khi Reviewer đối chiếu source với rag_old_0.
Affected scope: Baseline table, Notebooks 08b–08e, retrieval metrics và context.
```

```text
Decision: `Qwen/Qwen3-Embedding-0.6B` chạy hai dimension variants: 384D để đo
lightweight/storage trade-off và native 1024D để đo maximum quality. Không thêm
768D vào initial scope. Mỗi vector space dùng isolated index và không trộn với
model khác có cùng dimension.
Approved by: User
Approval date +07: 2026-08-26
Affected scope: Notebook 08a/08d, dense configuration count và candidate indexes.
```

```text
Decision: Notebook 08b so sánh tokenizer Unicode hiện hành với đúng một
Vietnamese word-segmentation candidate là Underthesea
`word_tokenize(..., format="text")`. Chỉ giữ Underthesea nếu quality tiếng Việt
tăng đủ để biện minh latency và dependency; không thêm tokenizer grid ban đầu.
Approved by: User
Approval date +07: 2026-08-26
Affected scope: Notebook 08b, BM25 evidence và dependency decision.
```

Commit/push cần yêu cầu riêng.
