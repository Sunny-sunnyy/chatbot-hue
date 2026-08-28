# Phase 8 — Benchmark và lựa chọn model/pipeline

## Trạng thái

`not_ready`

Phase 8 tổng thể chưa có production/final-selection authorization. Chỉ mở sau khi:

1. Phase 7 đơn giản được `approved`;
2. Phase 0 đến Phase 6 đã được review và đơn giản hóa bằng Repo, live system và
   tài liệu bổ sung thực sự hữu ích nếu có;
3. affected Phase 7 evaluation đã được chạy lại.

Golden Dataset V3 Gate 0 đã được Reviewer kiểm tra và user phê duyệt ở kích
thước `45` câu cùng smoke subset `10` câu ngày `2026-08-28 +07`. Gate 1 common
contracts đã được user phê duyệt cùng ngày. Exact Notebook 08a design/plan cũng
đã được duyệt và work package 08a ở trạng thái `ready`: Implementer được phép
viết đúng scope, tải pinned local models và chạy real Run All trên bảy isolated
Qdrant collections. Authorization này không cho phép sửa dataset, cài GPU/CUDA,
gọi paid API, mutate active collection, cutover production hoặc làm 08b–08e.

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

Exact common statistical/category contract đã được Gate 1 khóa:

- bảo vệ cả chín category;
- category `n >= 6` không được giảm số cases có relevant hit Top 5 và block khi
  hit count bằng nhau nhưng `delta nDCG@5 < -0.02`;
- category `n <= 3` dùng exact per-case guardrail: baseline đã tìm thấy exact
  relevant `source + section` trong Top 5 thì candidate không được làm mất toàn
  bộ relevant evidence khỏi Top 5;
- paired bootstrap 45 pairs, 10.000 resamples, fixed seed, 95% percentile CI;
- clear gain yêu cầu mọi guardrail, aggregate `delta nDCG@5 >= +0.03` và lower
  CI bound cho `delta nDCG@5 > 0`.

Mỗi candidate so fixed control của group; survivor/heavier candidate còn phải
clear gain so với best lighter finalist.

Fixed controls là E5-small dense-only cho embedding, Unicode `\w+` cho
tokenizer, same-embedding dense-only cho lexical/sparse/hybrid, same pre-rerank
ranking với no-rerank cho reranker, và cả production baseline lẫn
`llm_rag_reference_on_hue` cho full pipeline.

### Gate 1 common execution protocol

Main local profile là CPU FP32, không quantization. Dense document batch size 8,
query batch size 1; reranker pair batch size 4. Không silent auto-shrink. Native
instruction/pooling được giữ theo model, dense vectors được L2-normalize và
truncation được ghi nhận. Exact model contracts đã khóa nằm trong master design;
chúng chỉ được reopen tại notebook checkpoint khi có evidence mới.

Mỗi configuration đo cold load một lần, bỏ một warm-up, rồi chạy ba full
repetitions trên đủ 45 cases. Finalist phải thành công `3/3`; warm latency báo
`p50`/`p95`, ranking variation phải được trình bày chính xác. Memory observation
chỉ gồm RSS trước/sau load và observed peak RSS; CUDA metrics chỉ thêm sau một
GPU session được duyệt.

Failure/OOM phải lưu exact `status`/`error`, giải phóng resources và tiếp tục
configuration độc lập. Không tự retry, giảm batch, đổi device hoặc fallback.
Chưa đặt arbitrary latency cutoff.

Paid stage giữ production baseline và `llm_rag_reference_on_hue` làm hai
reference rows, cộng tối đa ba new finalists. Nếu có hơn ba candidate hợp lệ,
chọn và deduplicate quality leader, fastest/simplest passing leader và balanced
Pareto leader. Complexity chỉ dùng `low`/`medium`/`high` kèm rationale, không
dùng composite score.

True-hybrid candidate dùng isolated collection và chạy như experiment group
riêng sau local dense-only baseline. Không trộn kết quả của candidate-generation
experiment với BM25-weight hoặc reranker-model experiment trong cùng comparison.

Remote embedding có dimension khác cần exact reindex design. Active collection
không bị xóa hoặc thay đổi nếu user chưa duyệt exact transition.

## Real execution

Gate 1 common approval tự nó không authorize model download, API call, benchmark
run hoặc Qdrant mutation. Notebook 08a đã vượt checkpoint này bằng exact approved
design/plan và isolated-run authorization; các group còn lại chỉ được
implement/chạy sau exact research, brainstorming và user approval riêng.

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
- dùng Markdown tiếng Việt và code identifiers tiếng Anh;
- giữ repository outputs rỗng và execution counts null.

Phong cách trình bày bắt buộc tham khảo:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/*.ipynb
/home/minhhieu/llm_rag/tai_lieu/notebook_simple/**/*.ipynb
```

Chỉ kế thừa cách dạy theo section, giải thích trước code, cell ngắn và output dễ
đọc. Không kế thừa fake/demo data hoặc abstraction vượt nhu cầu; Phase 8 vẫn
chạy actual Hue data, Qdrant, local models và approved APIs.

Trước từng notebook `08a`–`08e`: research primary sources/hardware/dependencies,
brainstorm exact settings, nhận user approval, rồi mới implement và Run All.
Evidence mới, failure/OOM hoặc scope conflict phải quay lại brainstorming.

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
opaque `configuration_id`. CSV dùng long format với một `category=overall` row
và category rows cho mỗi setting. Approved rerun upsert theo human-readable
setting key, thay thế row trước và lưu ngay sau configuration. `status` và
`error` phản ánh approved attempt mới nhất; không tạo history registry.

Sau mỗi model/configuration, notebook hiển thị observed result, cập nhật dòng
tương ứng trong CSV kể cả khi failed, rồi giải phóng model, tensor/embedding lớn,
chạy Python garbage collection và clear CUDA cache nếu có. Không cần memory
manager. Khi restart kernel, cell setup đọc lại cumulative CSV để hiển thị tiến
độ; không dựa vào in-memory variables hoặc saved notebook output làm checkpoint.

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

## Gate 0 Golden Dataset V3 đã approved

Canonical files:

```text
docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md
docs/superpowers/plans/2026-08-27-phase-8-golden-dataset-v3-implementation-plan.md
reports/phase_8_golden_dataset_v3_implementation_report.md
reports/phase_8_golden_dataset_v3_codex_review.md
```

V2 dừng ở historical `changes_requested` sau ba vòng. V3 là complexity reset:
Reviewer đã đọc đủ `45/45` câu, mở mọi declared evidence, chạy validator,
regression và real retrieval metadata; user xác nhận final content/size ngày
`2026-08-28 +07`. Full `golden_v3.jsonl` có `45` câu và smoke có `10` row
deep-equal. Gate 0 đã `approved`.

Approval này chỉ khóa dữ liệu benchmark. Gate 1 common contracts đã được duyệt,
nhưng không chạy Phase 8 benchmark cho tới khi exact notebook group hoàn tất
research/brainstorming và được user authorize riêng.

Hai prompt Implementer/Reviewer V3 là handoff vận hành một lần và đã được retire
sau approval; lịch sử của chúng vẫn có trong Git. Không dùng lại chúng làm
session entrypoint.

## Notebook 08a đã approved để implementation

Golden Dataset V3 đã được Reviewer/user chấp nhận ở final distribution `45` câu.
Gate 1 brainstorming prompt đã được loại khỏi cây hiện hành sau khi hoàn tất;
lịch sử vẫn có trong Git. Session tiếp theo dùng exact Notebook 08a Implementer
handoff dựa trên:

```text
docs/superpowers/specs/2026-08-28-phase-8-08a-embedding-benchmark-design.md
docs/superpowers/plans/2026-08-28-phase-8-08a-embedding-benchmark-implementation-plan.md
```

Common regression/statistical gates, CPU measurement/reliability, finalist
count/roles, notebook style, long-format CSV/upsert, focused-test boundary và
final confirmation rerun đã được user duyệt ngày `2026-08-28 +07`.

Notebook 08a đã khóa bảy dense configurations, native contracts, isolated
collections, metrics/gates, CSV, notebook cells, focused tests và real Run All.
Sau implementation report, Reviewer mới bắt đầu independent technical review.
Chỉ khi Reviewer đạt và user xác nhận Notebook 08a mới chuyển sang 08b.

Chi tiết còn lại chỉ được giải quyết tại checkpoint của group tương ứng:

1. `08b`: BM25 parameters, BGE-M3 isolated schema/names/query/retention;
2. `08c`: current-library reranker integration;
3. `08d`: exact non-duplicate matrix manifest và execution order;
4. `08e`: exact Qwen generation, GPT judge rubric/repetitions và paid protocol;
5. từng later notebook: exact readable columns/key và Reviewer Run All command.

Sau khi user chọn winner, clean-kernel rerun đủ 45 cases cho winner và nearest
simpler comparator; nếu winner là baseline/lightest thì chỉ chạy winner. Không
tự cutover production.

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

```text
Decision: Golden Dataset V3 Gate 0 được approved với 45 full cases và exact
10-row smoke subset.
Approved by: User
Approval date +07: 2026-08-28
Evidence: Codex technical review `ready_for_user_confirmation` sau manual audit
45/45, declared evidence audit, validator/regression và real retrieval metadata;
User xác nhận nội dung và kích thước 45 câu.
Affected scope: Phase 8 canonical benchmark input và Gate 1 design assumptions.
Boundary: Không authorize benchmark implementation/execution, paid calls,
model download, Qdrant mutation hoặc production cutover.
```

```text
Decision: Phase 8 Gate 1 common contracts được approved: bảo vệ cả chín
categories; hierarchical large-category và exact small-category guardrails;
paired bootstrap 10.000 lần với fixed seed/95% percentile CI; clear-gain
threshold; fixed-control rồi best-lighter comparison; CPU FP32 measurement và
failure protocol; tối đa ba role-deduplicated finalists; notebook learning style;
long-format CSV upsert; focused deterministic tests; final clean-kernel rerun.
Approved by: User
Approval date +07: 2026-08-28
Evidence: User xác nhận consolidated common Gate 1 contract sau brainstorming.
Affected scope: Master guide/design/experiment plan và mọi Notebook 08 group.
Boundary: Exact settings/schema/matrix/generator/judge details vẫn phải research,
brainstorm và được user duyệt tại notebook tương ứng; không authorize code,
model download, API call, benchmark execution, Qdrant mutation hoặc cutover.
```

```text
Decision: Exact Notebook 08a dense embedding design và implementation plan được
approved. Implementer được authorize viết đúng allowlist, tải bảy pinned local
model configurations và chạy real Run All trên bảy isolated Qdrant collections;
E5-small chạy ở một cell riêng, sáu candidates chạy tuần tự ở một cell.
Approved by: User
Approval date +07: 2026-08-28
Evidence: User xác nhận toàn bộ 08a brainstorming sections, sau đó yêu cầu bàn
giao exact spec/plan cho Implementer thực hiện và Reviewer kiểm tra ở session kế.
Affected scope: Notebook 08a dense-only implementation, deterministic tests,
long-format CSV, implementation report và independent review.
Boundary: Không authorize BM25/sparse/fusion/reranker/generation/judge, paid API,
Golden V3 edit, active collection mutation, production cutover hoặc Notebook
08b–08e implementation.
```

Commit/push cần yêu cầu riêng.
