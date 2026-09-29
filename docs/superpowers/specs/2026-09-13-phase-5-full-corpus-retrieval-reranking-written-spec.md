# Phase 5 — Full-corpus retrieval, RRF và reranking

```text
Status: approved by User 2026-09-13 +07
Date: 2026-09-13 +07
Owner: Codex Reviewer
Risk: high
Runtime authorization: none
Dependency: Full-corpus Phase 4 User-approved closure
```

## 1. Mục tiêu

Phase 5 tạo một đường retrieval local cho bốn collection Representation A đã
đóng ở Phase 4. Mỗi dense model phải chạy được hai retrieval treatments và có
thể bật hoặc tắt cùng một MiniLM reranker, để Phase 8 về sau có các cấu hình
thực sự tương đương để đánh giá.

Phase này chỉ chứng minh contract, integration, tính deterministic, latency và
khả năng quan sát kỹ thuật. Phase 5 không đo retrieval quality, không chọn
finalist/winner và không đổi production API/config.

## 2. Dependency và bốn collection canonical

Phase 5 dùng read-only bốn completed Phase 4 collections:

| Candidate | Collection | Dense dimension |
|---|---|---:|
| `e5-small-384` | `hue_full_corpus_a_e5_small_384` | 384 |
| `e5-base-768` | `hue_full_corpus_a_e5_base_768` | 768 |
| `huydang-dek21-768` | `hue_full_corpus_a_huydang_dek21_768` | 768 |
| `qwen3-embedding-0.6b-1024` | `hue_full_corpus_a_qwen3_06b_1024` | 1024 |

Mỗi collection hiện có `8.460` points, named vectors `dense` và `sparse`, cùng
exact five-field payload:

```text
search_text
source
title
heading_path
evidence_parts
```

Sparse query và BM25 dùng đúng Phase 3 sparse state:

```text
path: data/full_corpus_builds/phase_3_sparse_state.json
schema: phase_3_sparse_state:v1
SHA-256: 5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be
document_count: 8460
vocabulary_size: 5662
k1: 1.5
b: 0.75
```

Các count và hash trên là closed dependency evidence. Service phải đối chiếu
chúng với build record của collection đã chọn; không refit vocabulary, không
scroll toàn corpus để dựng BM25 và không sửa collection canonical.

## 3. Phạm vi và ranh giới Phase

Trong scope:

- một canonical Full-corpus composition root;
- hai retrieval treatments `dense_bm25_rrf` và `native_hybrid_rrf`;
- hai reranker modes `none` và `minilm`;
- deterministic Python RRF;
- Top-10 `RetrievedDocument` cùng `RetrievalTrace` nội bộ;
- strict readiness và fail-explicit behavior;
- pure checks nhỏ cùng real local Qdrant/model verification;
- isolated Qdrant experiment collections khi cần điều tra hoặc so sánh;
- implementation report đã làm sạch dữ liệu riêng tư.

Ngoài scope:

- ContextBuilder, generation, API, frontend và production cutover;
- Golden retrieval metrics, answer metrics, finalist hoặc winner selection;
- Representation B;
- tuning candidate depth, RRF constant, model instruction hoặc index settings;
- remote reranker/provider;
- cleanup, replacement hoặc mutation bốn canonical collections;
- cải tiến hoặc mở rộng Foods runtime;
- Git commit/push và purge lịch sử GitHub.

Phase 5 trả ranked Top 10. Phase 6 mới chọn tối đa Top 5 để pack context.

## 4. Cấu hình và composition

Hai axes độc lập:

```text
retrieval_treatment = dense_bm25_rrf | native_hybrid_rrf
reranker = none | minilm
```

Mỗi collection có bốn tổ hợp, tổng cộng `4 collections × 4 combinations = 16`
logical configurations.

Một service/run chỉ bind đúng:

- một candidate/collection;
- một `retrieval_treatment`;
- một `reranker` mode.

Verification có thể lặp tuần tự 16 cấu hình. Không load cả bốn dense models vào
một service, không tạo multi-collection query semantics và không cho component
internals tự đọc arbitrary overrides.

Full-corpus path được triển khai riêng, chỉ tái sử dụng primitive hiện hữu khi
contract thực sự khớp. Không chồng conditional support lên Foods classes và
không tạo plugin/provider/framework tổng quát.

## 5. Dense + BM25-local baseline

`dense_bm25_rrf` chạy:

```text
query
-> exact dense query preprocessing của candidate
-> Qdrant dense Top 30
-> BM25 local score trên search_text của chính 30 candidates
-> dense rank + positive-only BM25 rank
-> Python RRF
-> deterministic pre-rerank Top 30
```

BM25 không tìm candidate độc lập. Chỉ document có raw BM25 score `> 0` đi vào
nhánh BM25 rank. Score bằng `0` không được xếp tùy ý theo point ID rồi tạo RRF
contribution giả.

Nếu có 30 dense candidates nhưng mọi BM25 score bằng `0`, nhánh BM25 là rỗng;
RRF một nhánh giữ đúng dense order. Đây không phải dependency error và không
fallback sang treatment khác, nhưng phải ghi anomaly `REVIEW_REQUIRED` trong
Phase 5 verification.

## 6. Native dense/sparse hybrid

`native_hybrid_rrf` chạy:

```text
query
-> exact dense query preprocessing của candidate
-> Qdrant dense Top 30

query
-> exact Phase 3 sparse query encoding
-> Qdrant sparse Top 30

two ranked lists
-> deduplicate by Qdrant point UUID
-> Python RRF
-> deterministic pre-rerank Top 30
```

Hai Qdrant branches phải độc lập; sparse không chỉ chấm dense candidates. Query
sparse dùng cùng vocabulary/state với document sparse vectors và query values
theo Phase 3 contract; không bật Qdrant IDF modifier.

Nếu sparse query không có token trong vocabulary, sparse branch hợp lệ là rỗng
và dense order được giữ. Runtime không biến trạng thái này thành fallback/error,
nhưng Phase 5 verification phải đánh dấu `REVIEW_REQUIRED`.

## 7. RRF và deterministic ordering

Hai treatments dùng cùng exact formula:

```text
rrf_score(document) = sum(1 / (60 + rank_in_branch))
```

- rank bắt đầu từ `1`;
- một document đóng góp tối đa một lần cho mỗi branch;
- deduplicate bằng Qdrant point UUID string;
- sort theo RRF score giảm dần, sau đó point ID tăng dần;
- giữ tối đa 30 documents trước reranker;
- không dùng Qdrant server fusion hoặc qdrant-client RRF helper vì semantics
  mặc định không phải exact contract trên và không giữ đầy đủ tie-break/trace;
- không min-max normalization, weighted fusion hoặc tuning weights trong đường
  Full-corpus mới.

RRF là một pure function nhỏ, trực tiếp; không tạo fusion framework.

## 8. Reranker contract

Reranker Phase 5 là:

```text
model: cross-encoder/ms-marco-MiniLM-L-6-v2
device: CPU
input pair: (query, RetrievedDocument.search_text)
input depth: at most 30
output depth: at most 10
```

Behavior:

- `reranker=none`: cắt RRF Top 30 thành Top 10;
- `reranker=minilm`: score cùng pre-rerank Top 30 rồi trả Top 10;
- validate số score, numeric type và finite values;
- tie theo rerank score giảm dần rồi point ID tăng dần;
- model/scoring failure là explicit failure, không dùng RRF result như silent
  fallback;
- model chỉ load/warm-up khi cấu hình chọn `minilm`.

Trước scoring, dùng tokenizer/input limit thực của MiniLM để kiểm toàn bộ pairs
không truncate. Nếu chỉ một pair vượt limit, bỏ reranking cho cả request, giữ
nguyên pre-rerank order/score và ghi `rerank_status=skipped_overlength`. Không
truncate, không rerank một phần và không tự giảm depth.

Sau warm-up, p95 của reranker stage trên Top 30 phải không quá `3 giây`; cold
load được đo riêng. Implementation Plan khóa exact bounded sampling command.
Nếu không đạt, báo observed failure; không đổi model/device/depth để làm PASS.

### Qwen reranker deferred candidate

`Qwen/Qwen3-Reranker-0.6B` không được triển khai hoặc tự fallback trong Phase 5.
Sau Phase 8 comparison giữa MiniLM và no-rerank trên retrieval finalists, nếu
MiniLM không có lợi ích rõ ràng, làm giảm metric quan trọng hoặc không đạt
resource/coverage contract, Reviewer trình evidence cho User. Chỉ sau một scope
research/design/spec/plan riêng được duyệt mới được triển khai Qwen reranker.

Không tự thay MiniLM bằng Qwen và không gọi model này từ Phase 5 runtime.

## 9. RetrievalResult và score semantics

Canonical Full-corpus service trả một typed value:

```text
RetrievalResult
  documents: list[RetrievedDocument]
  trace: RetrievalTrace
```

Không lưu trace bằng mutable `service.last_trace` và không trả tuple không tên.
Mỗi request sở hữu đúng một result/trace nên không ghép nhầm giữa concurrent
requests.

Logical `RetrievedDocument` contract:

```text
id: Qdrant point UUID string
score: final score của stage cuối thực sự chạy
text/search_text: private retrieval representation dùng nội bộ
metadata: source, title, heading_path, evidence_parts
```

Stage scores/ranks không được trộn vào document metadata:

| Request outcome | `RetrievedDocument.score` |
|---|---|
| no rerank | RRF score |
| MiniLM success | rerank score |
| MiniLM skipped overlength | RRF score |

Final rank bắt đầu từ `1`. Score chỉ mô tả thứ tự trong đúng một cấu hình; không
so sánh raw numeric value giữa RRF/MiniLM hoặc giữa các models để kết luận chất
lượng.

## 10. RetrievalTrace tối thiểu

`RetrievalTrace` là bằng chứng kỹ thuật nội bộ, không phải API/public schema.
Nó chỉ cần đủ để giải thích một request:

- candidate/collection, treatment và reranker mode;
- build-record/sparse-state identity;
- dense, BM25 hoặc sparse candidate counts;
- sparse in-vocabulary/non-zero count;
- union/pre-rerank/final counts;
- per-point ranks và numeric scores của các stages đã chạy;
- timings theo stage và cold/warm distinction khi đo latency;
- reranker status;
- anomaly codes và verification classification.

Trace không chứa query text, `search_text`, `evidence_parts`, corpus excerpt,
absolute path hoặc secret. Không tạo trace database, global audit service,
retention manager hoặc telemetry framework.

Detailed trace của live verification chỉ lưu dưới ignored local `data/`. Tracked
report chỉ được chứa aggregate/count/hash/config/latency/status đã làm sạch.
Phase 6 chỉ lấy `documents`; trace không mặc định được serialize ra API.

## 11. Readiness và failure behavior

Trước khi nhận query, composition root kiểm đúng components cấu hình cần dùng:

- selected collection tồn tại;
- exact dense/sparse names, dimension và point count khớp build record;
- collection/build record thuộc cùng candidate và Representation A;
- corpus identity và sparse-state SHA/count/vocabulary khớp;
- dense query encoder đúng model revision/preprocessing/device contract;
- sparse encoder/BM25 state sẵn sàng cho treatment đã chọn;
- MiniLM load và warm-up thành công khi `reranker=minilm`.

`reranker=none` không load MiniLM. Không có component nào được tự thay bằng
component khác.

Failure policy:

- invalid/empty query: typed input error;
- model, encoder, Qdrant hoặc reranker failure: typed dependency error;
- schema/build/state mismatch hoặc component thiếu: not-ready/configuration
  error;
- retrieval thực sự thành công nhưng không có candidate: trả documents rỗng;
- không catch broad exception rồi trả `[]`;
- không silent fallback giữa treatments, collections, models hoặc reranker
  modes.

Với bảy fixed domain questions, dense trả rỗng hoặc count bất thường cũng phải
được đánh dấu để Reviewer xem xét, dù empty successful retrieval vẫn là runtime
state hợp lệ cho query tùy ý.

## 12. Anomaly và Reviewer escalation

Verification phân biệt:

- `PASS`: mọi required contract/invariant đạt, không có bất thường chưa giải
  quyết;
- `FAIL`: có vi phạm contract chắc chắn;
- `REVIEW_REQUIRED`: pipeline chạy nhưng có kết quả khó hiểu hoặc đáng ngờ và
  chưa đủ evidence kết luận nguyên nhân.

Ví dụ `FAIL`: sai schema/dimension/hash, missing required payload, duplicate
point ID trong result, non-finite score, model/Qdrant failure, reranker trả sai
số score hoặc non-deterministic tie-break.

Ví dụ `REVIEW_REQUIRED`: BM25 toàn `0`, sparse query không có vocabulary token,
hai branches có overlap bất thường, đồng hạng bất thường, candidate count khó
giải thích, latency tăng đột biến hoặc dấu hiệu private data sắp đi vào tracked
artifact.

Danh sách trên không đóng. Bất kỳ thành phần/hành vi nào Implementer thấy khó
hiểu, trái kỳ vọng hoặc chỉ có thể tiếp tục bằng phỏng đoán/fallback đều phải
được báo Reviewer. Implementer:

1. giữ nguyên observed result;
2. đánh dấu affected matrix cell `REVIEW_REQUIRED` hoặc `FAIL`;
3. không tự đổi contract, che bằng fallback hoặc kết luận PASS;
4. gửi evidence đã redacted cho Reviewer;
5. có thể tiếp tục các cells độc lập nhưng không được đóng Phase.

Reviewer kiểm code, query preprocessing, model, collection/build record, sparse
state và dữ liệu local cần thiết rồi mới phân loại/đưa correction. Không bắt
Implementer xây trước một anomaly engine hoặc danh sách heuristic phức tạp;
structured trace và nhận xét có bằng chứng là đủ.

## 13. Private corpus và Git boundary

`knowledge-base-hue/` là dữ liệu cá nhân, chỉ giữ local và phải nằm trong
`.gitignore`. Qdrant storage, Phase 3 state/build records, detailed traces và
fixed live questions cũng ở local ignored paths.

Phase 5:

- chỉ dùng local corpus-derived Qdrant/state; không upload payload ra external
  service;
- không ghi verbatim `search_text`, `evidence_parts`, query hoặc full excerpt
  vào tracked test/report/doc/log artifact;
- tracked report được ghi collection/model names, counts, hashes, P7 labels,
  timings, statuses và limitations;
- thiếu local input cần cho command nào thì command đó fail explicit, không tự
  download/thay bằng corpus khác;
- không commit/push nếu chưa có exact Git authorization.

Việc ignore và `git rm --cached` chỉ ngăn corpus xuất hiện trong commit mới sau
khi staged change được commit. Nó không xóa bản đã public trong Git history,
clone/fork/cache. History purge và force-push là một destructive scope riêng,
không thuộc Phase 5.

## 14. Isolated experiment collections

Sau khi Plan được duyệt, Phase 5 có thể tạo thêm Qdrant collection để điều tra
hoặc so sánh mà không xin lại từng target, với các điều kiện:

- target phải absent, isolated và không trùng four canonical/Foods names;
- không replace, reconcile, delete hoặc mutate collection hiện có;
- mỗi target có local manifest tối thiểu gồm semantic name, source candidate,
  corpus/sparse identity, vector schema, thay đổi đang thử và expected count;
- mỗi phép so sánh nêu baseline và một biến chính được thay đổi;
- report exact commands, observed counts/schema/latency/status và limitation;
- manifest/report không chứa per-source path list hoặc corpus content;
- cleanup chỉ sau Reviewer inspection và exact User authorization cho targets.

Không tạo central experiment registry, lifecycle service hoặc automatic naming
framework. Nếu không có observed need, implementation chỉ query bốn canonical
collections và không tạo experiment collection.

## 15. Verification vừa đủ

Pure deterministic checks chỉ bảo vệ behavior thực:

- exact RRF formula, one-branch result và point-ID tie-break;
- positive-only BM25 rank;
- dedup/union của dense và sparse lists;
- final score semantics và Top30/Top10 bounds;
- trace không chứa private text fields;
- error/classification behavior quan trọng đã quan sát hoặc khóa trong spec.

Database/model behavior phải có real local integration evidence; mock/fake/stub
không thay được Qdrant, dense model, sparse state hoặc MiniLM evidence.

Live smoke dùng bảy fixed private questions, mỗi câu đại diện một P7:

```text
foods
heritages
festivals
performing_arts
travel_places
travel_services
travel_tickets
```

Chạy đủ bốn collections × hai treatments; trên mỗi kết quả kiểm cả `none` và
`minilm`, tức đủ 16 logical configurations. Kiểm contract, stage execution,
metadata/trace, deterministic order, latency, failures và anomalies. Không tính
MRR, nDCG, Recall, coverage, answer score hoặc tuyên bố model/treatment tốt hơn.

Tracked implementation report phải ghi:

- exact environment/commands và configuration matrix;
- readiness results;
- candidate/final counts và latency summaries;
- `PASS`/`FAIL`/`REVIEW_REQUIRED` cho từng matrix cell;
- reranker skipped/failure details;
- experiment collection manifests/comparisons nếu có;
- mọi deviation, limitation và phần chưa verify.

Detailed per-query/per-point trace và fixed question text chỉ nằm local ignored.
Không cần notebook mới cho Phase 5; notebook cũ thuộc Foods history và không
được mở rộng chỉ để duplicate runtime/report.

## 16. Phase acceptance

Phase 5 chỉ đạt technical verdict `ready_for_user_confirmation` khi:

1. canonical Full-corpus composition không sửa behavior/config của Foods path;
2. bốn canonical collections vượt strict readiness bằng exact local records;
3. cả hai treatments chạy đúng Top30/RRF contract trên bốn candidates;
4. `none` và real MiniLM modes trả deterministic Top10 đúng score semantics;
5. MiniLM Top30 warm p95 đạt `≤ 3 giây`, cold load được báo riêng;
6. `RetrievalResult`/private `RetrievalTrace` đủ giải thích stages mà không làm
   lộ corpus qua tracked artifacts;
7. live seven-question matrix được chạy đủ và báo trung thực;
8. không còn `FAIL` hoặc `REVIEW_REQUIRED` chưa được Reviewer giải quyết;
9. tests/checks chỉ bảo vệ required behavior, không có fake integration
   evidence hoặc abstraction phòng xa;
10. independent Reviewer review không còn blocker/major;
11. User xác nhận closure Phase 5.

Technical smoke chỉ chứng minh hệ thống chạy đúng contract. Nó không chứng minh
retrieval quality và không được dùng chọn winner/cutover.

## 17. Downstream boundary

Sau User closure Phase 5, Phase 6 mới được thiết kế/triển khai để:

- dùng canonical Full-corpus `RetrievalResult.documents`;
- pack tối đa Top 5 evidence chunks;
- nối generation/API/UI;
- thay Foods runtime rồi audit và xóa Foods-only code/config/profile trong
  exact approved scope.

Phase 8 mới dùng Golden metrics để chọn retrieval finalists, so MiniLM với
no-rerank, quyết định có mở Qwen3-Reranker research hay không, chọn winner,
cutover và đề xuất collection cleanup.

Written Spec này không tự cấp implementation, Qdrant write, delete, Git commit
hoặc push authority. Exact Implementation Plan và Review Contract phải được
User duyệt trước khi giao Implementer.
