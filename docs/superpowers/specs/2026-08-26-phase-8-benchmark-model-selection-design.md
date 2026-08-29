# Phase 8 Benchmark Model Selection Design

**Status:** `gate_1_common_contracts_approved`; Notebook 08a implementation,
independent review and user confirmation are complete. Notebook 08b is the next
research/brainstorming checkpoint; later execution remains pending.

**Purpose:** Khóa các quyết định Phase 8 đã được user xác nhận trong khi tiếp
tục brainstorming những biến thí nghiệm còn lại. Bản master này tự nó không
authorize code, dataset correction, model download, CUDA/PyTorch changes, paid
runs, Qdrant mutation, commit hoặc push; exact 08a authorization nằm trong hai
tài liệu 08a đã duyệt và yêu cầu mới nhất của user.

## Boundary và prerequisite

- Golden Dataset V3 là scope riêng tại
  `docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md`.
  Reviewer đã xác minh và user phê duyệt Gate 0 ngày `2026-08-28 +07` với
  `45` câu full và `10` câu smoke. Approval này khóa input benchmark nhưng không
  authorize implementation hoặc execution Phase 8.
- Phase 8 master framework và thứ tự experiment groups đã khóa; exact 08a work
  package đã `ready`, còn later groups vẫn ở design checkpoints.
- Active Qdrant collection tiếp tục read-only; candidate indexes/collections
  phải isolated.
- Mỗi comparison chính chỉ thay đổi một experiment group.

## Fixed end-to-end boundary

```text
Generator: qwen/qwen3.5-9b qua OpenRouter
Judge: gpt-5.4-mini
Primary language: Vietnamese
Local execution: GPU khi session riêng enable thành công; CPU fallback bắt buộc
```

## Mandatory llm_rag reference baseline

`llm_rag_reference_on_hue` ports the exact current `llm_rag` runtime flow onto
the Hue corpus and corrected golden data:

```text
E5-small dense top 30
→ raw 0.6 dense + 0.4 BM25 rescoring on those same candidates
→ top 10
→ current MiniLM reranker input 10/output 5
→ at most 5 whole chunks and 3000 context characters
→ qwen/qwen3.5-9b via OpenRouter
→ gpt-5.4-mini judge
```

Raw unnormalized fusion is preserved only to reproduce the reference. Runtime
source, which truncates to 10 before reranking, overrides an inconsistent prose
sentence in the deep-dive document that says reranking sees 30.

Generator và judge giữ cố định khi so retrieval/reranking. Answer generation
chỉ chạy cho end-to-end finalists sau khi retrieval evidence được khóa.

## Dense embedding candidate order

Thứ tự dưới đây đi từ nhẹ đến nặng/mạnh hơn để tạo baseline sớm và kiểm soát
tài nguyên. Nó không giả định trước winner.

| Thứ tự | Model | Dimension/capability | Vietnamese policy |
|---:|---|---|---|
| 1 | `intfloat/multilingual-e5-small` | 384D; current control | benchmark corrected Vietnamese gold |
| 2 | `CODE4LIFEOFFICIAL/huydang-dek21-embedding` | native 768D; PyVi segmentation | benchmark corrected Vietnamese gold; legal-domain transfer risk |
| 3 | `intfloat/multilingual-e5-base` | 768D | benchmark corrected Vietnamese gold |

The local scope contains three dense configurations. MiniLM-L12 was measured and
then removed because of quality regression and truncation; its CSV rows remain
historical evidence. The 1024D candidates are governed only by the remote-only
amendment below.

## Sparse and hybrid capabilities in scope

Phase 8 must create controlled real comparisons for:

| Retrieval path | Required compatible coverage |
|---|---|
| Dense-only | All three local dense configurations |
| Independent full-corpus BM25-only | Once; embedding-independent |
| Current dense-candidate then BM25 rescoring | All three local dense configurations |
| True hybrid dense + independent full-corpus BM25 | All three local dense configurations |
| Custom TF-IDF `SparseEmbedder`-only | Once as an experimental control |
| True hybrid dense + custom TF-IDF sparse | All three local dense configurations |

Notebook 08d combines every valid pre-rerank pipeline with no reranker and each
of the three reranker candidates. Complete coverage means every real component,
path and compatible interaction is measured. It does not mean repeating an
embedding-independent result under six embedding labels or inventing a learned-
sparse pairing for a model that cannot produce that representation.

Compatibility-aware local matrix, initial fusion methods and depth contract have
been locked. The finalist gate before paid generation continues through
brainstorming before implementation authorization.

Initial true-hybrid comparisons use exactly two fusion methods:

- Reciprocal Rank Fusion (RRF) as the primary rank-based method;
- independent min-max normalization followed by `0.6 dense / 0.4 sparse`
  weighted sum, preserving the current baseline weighting.

No initial weight grid is allowed. Targeted weight tuning can be proposed only
after real results show that weighted fusion is beneficial and tuning could
change the final decision.

## Depth and context contract

- Dense, BM25 and sparse candidate generators each retrieve up to 30.
- Fusion retains the top 10 as the common pre-rerank input.
- Every reranker scores the same 10 and returns top 5.
- No-rerank final comparison uses the top 5 of the same pre-rerank ranking.
- Generation receives at most 5 whole chunks and 3000 characters; it may receive
  fewer when the character budget is reached.
- Report candidate Recall@30, fusion Recall@10 and final MRR@5/nDCG@5/Recall@5.

This keeps final retrieval comparisons at the same depth. Ten documents are
never passed directly to the generator under this contract.

## Reranker candidate order

| Thứ tự | Model | Published language scope | Design treatment |
|---:|---|---|---|
| 1 | `cross-encoder/ms-marco-MiniLM-L-6-v2` | English | lightweight current baseline; full Vietnamese measurement |
| 2 | `BAAI/bge-reranker-base` | Chinese, English | retain only if Vietnamese evidence passes quality gates |
| 3 | `Qwen/Qwen3-Reranker-0.6B` | multilingual | heavier primary multilingual candidate |

Model code producing scores for Vietnamese input is integration evidence, not
quality evidence. Models without an explicit Vietnamese claim are not rejected
before measurement, but cannot win without corrected-gold Vietnamese evidence.

## Approved common model execution profile

Các thiết lập dưới đây là baseline chung đã được user duyệt. Trước notebook chứa
model tương ứng vẫn phải kiểm tra lại model card/API/dependency hiện hành; chỉ
reopen quyết định khi có exact evidence về incompatibility hoặc resource limit.

- Dùng native query/document contract và native pooling của từng embedding:
  E5 dùng `query:`/`passage:` cùng attention-mask mean pooling; multilingual
  MiniLM dùng raw text cùng mean pooling; Huydang dùng PyVi segmentation và
  native mean pooling.
- L2-normalize mọi dense query/document vector sau pooling.
- Truncation bật với maximum 512 tokens cho E5, native 128 cho multilingual
  MiniLM và native 256 cho Huydang; ghi `truncated_document_count`.
- Main local profile là CPU FP32, không quantization. Document batch size là 8,
  query batch size là 1 và không silent auto-shrink. CUDA/dtype GPU chỉ được
  thiết kế trong session GPU riêng.
- MiniLM/BGE reranker nhận raw `(question, chunk_text)`. Qwen reranker dùng
  official chat/template cùng task instruction tiếng Việt:
  `Với một câu hỏi du lịch ẩm thực Huế, hãy đánh giá liệu tài liệu có chứa thông tin liên quan để trả lời câu hỏi hay không.`
  Mọi pair cap 512 tokens bằng `longest_first`, ghi `truncated_pair_count`, CPU
  pair batch size 4. Giữ native score để xếp hạng trong từng model; exact tie
  giữ nguyên pre-rerank order.
- BGE-M3 learned sparse/ColBERT không còn thuộc local experiment matrix. Một
  OpenRouter dense response trong future proposal không được coi là equivalent
  hoặc evidence cho các representation này.

## Measurement contract

Every candidate records:

- corrected-gold retrieval quality, including aggregate and category slices;
- failures and stability across repeated runs where applicable;
- model load/cold-start latency separately from warm inference;
- indexing/corpus embedding time;
- query embedding, dense retrieval, sparse retrieval/fusion, reranking and
  generation latency separately;
- warm online latency with at least p50 and p95;
- device, dtype, batch size, candidate depth and top-k;
- memory/resource observations, provider cost and operational complexity when
  applicable.

CPU and GPU measurements are separate execution profiles. A model running on
CPU is not directly ranked against another model running on GPU for latency.

Mỗi local configuration đo cold model load riêng một lần, chạy một warm-up bị
loại khỏi thống kê, rồi chạy ba full repetitions trên đủ 45 cases. Warm latency
báo `p50`/`p95`; quality lấy từ một deterministic run, còn ba repetitions dùng
để phát hiện instability. Finalist phải thành công `3/3`. Nếu ranking khác nhau
giữa các lần, báo exact variation và review thay vì che bằng mean.

Memory observation giữ nhẹ: process RSS trước/sau load và observed peak RSS;
nếu một GPU session sau này được duyệt thì thêm PyTorch peak allocated/reserved.
Không thêm profiler hoặc sampling timeline.

Khi failed/OOM, ghi `status=failed` cùng exact error, giải phóng model/tensors/
cache rồi tiếp tục configurations độc lập. Không auto-retry, shrink batch, đổi
device hoặc fallback. Mọi changed rerun phải quay lại research/brainstorming.
Failure, OOM hoặc dưới `3/3` là technical blocker; chưa có arbitrary latency SLA.

## Approved selection rule

Mọi candidate phải bảo vệ cả chín category trong final Golden Dataset V3.

- Với category lớn `n >= 6` (`relationship`, `direct_fact`, `food_knowledge`,
  `comparative`): trước hết số cases có ít nhất một exact relevant
  `source + section` trong Top 5 không được giảm. Khi hit count bằng nhau,
  category `nDCG@5` là gate và `MRR@5` là supporting metric. Candidate bị block
  nếu `delta nDCG@5 < -0.02`.
- Với category nhỏ `n <= 3` (`holistic`, `spanning`, `guide_planning`,
  `numerical`, `temporal`): dùng exact per-case guardrail. Nếu baseline có ít
  nhất một exact relevant evidence trong Top 5, candidate không được làm mất
  toàn bộ relevant evidence khỏi Top 5. Rank movement bên trong Top 5 không tự
  động là blocker.

Uncertainty dùng paired bootstrap trên 45 candidate-baseline case pairs: 10.000
resamples, fixed seed và 95% percentile CI cho delta Recall@5/nDCG@5/MRR@5.
Small-category guardrail vẫn exact per-case, không dùng bootstrap.

`clear quality gain` chỉ tồn tại khi candidate vượt mọi category guardrail,
aggregate `delta nDCG@5 >= +0.03`, đồng thời lower bound của bootstrap 95% CI
cho `delta nDCG@5` lớn hơn 0. Recall@5 và MRR@5 được báo để đối chiếu nhưng không
thay thế hai điều kiện này.

Trong mỗi group, mọi candidate so với fixed control. Survivor/heavier candidate
còn phải clear gain so với best lighter finalist. Controls là E5-small
dense-only cho embedding, Unicode `\w+` cho tokenizer, same-embedding dense-only
cho lexical/sparse/hybrid, same pre-rerank ranking với no-rerank cho reranker,
và cả production baseline lẫn `llm_rag_reference_on_hue` làm reference rows cho
full pipeline.

Nếu quality không clear, chọn pipeline nhẹ, nhanh và đơn giản hơn. Complexity
không dùng composite score: chỉ `low`/`medium`/`high` kèm rationale theo models,
dependencies, extra collections/indexes và retrieval stages.

## GPU boundary

The available GPU is NVIDIA GTX 1650 under Windows/WSL2. Current Hue environment
has a CUDA-enabled PyTorch build but WSL reports GPU access blocked by the
operating system. Diagnosis and remediation belong to a separate session.
Phase 8 design neither installs `cu132` nor changes dependencies. CPU execution
remains accepted as fallback.

## Notebook experience

Phase 8 uses notebooks by experiment group rather than one notebook per
configuration:

| Notebook | Human-facing responsibility |
|---|---|
| `notebooks/08a_embedding_benchmark.ipynb` | Learn and compare all dense embedding candidates |
| `notebooks/08b_retrieval_fusion_benchmark.ipynb` | Learn and compare lexical, sparse and fusion paths |
| `notebooks/08c_reranker_benchmark.ipynb` | Compare no-rerank and all reranker candidates on fixed inputs |
| `notebooks/08d_full_pipeline_matrix.ipynb` | Run the approved local embedding × retrieval × reranker matrix |
| `notebooks/08e_generation_finalists.ipynb` | Generate and judge answers for approved finalists |
| `notebooks/08_benchmark_model_selection.ipynb` | Read group results, explain trade-offs and select the final pipeline |

Notebook design follows the teaching style of the required references:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/*.ipynb
/home/minhhieu/llm_rag/tai_lieu/notebook_simple/**/*.ipynb
```

Each section starts with a clear heading and short explanation of what will run,
why it matters, what stays fixed, expected resource/time considerations and how
to read the result. Cells remain short and direct. Helpers are allowed only when
they visibly remove repetition. Real Hue data/services/models are mandatory;
fake data or mocked execution cannot be implementation or evidence.

Markdown trình bày bằng tiếng Việt; function, variable và configuration
identifiers dùng tiếng Anh. Mỗi cell chỉ làm một việc, Markdown ngắn đứng ngay
trước code, bản đơn giản được giới thiệu trước rồi mới thêm bước theo trình tự
tự nhiên. Notebook import backend functions thay vì duplicate runtime logic và
không nhồi validator, package matching, audit logic hoặc test suite vào cells.
Mỗi canonical notebook phải Run All thật trên temporary copy để review, sau đó
repository copy giữ outputs rỗng và `execution_count: null`.

Trước khi implement hoặc chạy từng notebook group `08a`–`08e`, bắt buộc:

1. research primary/current sources, hardware và dependency contracts;
2. brainstorm exact settings với user;
3. nhận user approval cho group đó;
4. sau đó mới implement và Run All.

Evidence mới, failure/OOM hoặc scope conflict đưa group trở lại brainstorming.

## Minimal persistence and memory cleanup

Each experiment notebook writes one cumulative CSV:

| Notebook group | Durable result |
|---|---|
| Embedding | `evaluation/results/phase8_embedding_results.csv` |
| Retrieval/fusion | `evaluation/results/phase8_retrieval_results.csv` |
| Reranker | `evaluation/results/phase8_reranker_results.csv` |
| Full local matrix | `evaluation/results/phase8_pipeline_matrix.csv` |
| Generation finalists | `evaluation/results/phase8_generation_results.csv` |

No run ID, timestamped package, checksum manifest, duplicate JSON artifact or
opaque `configuration_id` is needed. Human-readable setting columns identify
results. CSV dùng long format: một row `category=overall` và các category rows
cho mỗi setting. Approved rerun upsert theo human-readable setting key, thay thế
row của lần được duyệt trước và lưu ngay sau configuration; không giữ history
registry. Minimal `status` và `error` phản ánh approved attempt mới nhất.

After each model/configuration, save or update its CSV row before releasing the
model and large temporary tensors/embeddings. Run Python garbage collection and
clear the CUDA cache when CUDA is active. A kernel restart then reloads the
cumulative CSV; no resume framework is introduced.

Canonical notebooks are committed with null execution counts and empty outputs.
Interactive outputs may remain visible while the user is running locally, but
they are not the durable checkpoint or committed evidence.

## Notebook-specific decisions

Gate 1 common contracts đã được user duyệt ngày `2026-08-28 +07`. Notebook 08a
đã hoàn tất research/brainstorming và có exact approved documents:

```text
docs/superpowers/specs/2026-08-28-phase-8-08a-embedding-benchmark-design.md
docs/superpowers/plans/2026-08-28-phase-8-08a-embedding-benchmark-implementation-plan.md
```

User đã authorize implementation và real local Run All trong isolated 08a
scope. Không viết chi tiết giả định cho các notebook còn lại trước checkpoint
tương ứng.

- `08b`: BM25 parameters, Vietnamese tokenizer and exact TF-IDF isolated Qdrant
  schema/query/fusion behavior. BGE learned sparse is no longer local scope.
- `08c`: exact current-library reranker integration compatibility.
- `08d`: exact non-duplicate matrix manifest và lightweight-to-heavy run order.
- `08e`: exact Qwen generation settings, GPT judge rubric/repetitions và paid
  call protocol.
- Từng notebook: exact readable CSV columns/setting key và Reviewer Run All
  command sau khi structure đã được brainstorm.

Paid stage giữ hai fixed reference rows và tối đa ba new finalists. Nếu chỉ một
hoặc hai candidates pass thì không fill quota. Nếu nhiều hơn ba candidates đủ
điều kiện, chọn quality leader, fastest/simplest passing leader và balanced
Pareto leader; một configuration giữ nhiều vai trò không bị nhân bản.

Sau khi user chọn winner, chạy clean-kernel full 45-case confirmation cho winner
và nearest simpler comparator; nếu winner là baseline/lightest thì chỉ chạy
winner. Cập nhật benchmark summary nhưng không production cutover. Transition
production luôn là proposal riêng cần user approval.

## Focused verification contract

Automated tests chỉ bao phủ reusable deterministic behavior: metric/gate logic,
paired bootstrap, category aggregation và cumulative CSV upsert. Model, Qdrant
và provider integration phải được xác minh bằng real temporary-notebook Run All;
mock, fake vector, replay output hoặc synthetic result không phải completion
evidence.

## BM25 Vietnamese tokenizer decision

Notebook 08b must compare exactly two tokenization variants on the same
full-corpus BM25 path:

1. the current lowercase Unicode `\w+` tokenizer as control;
2. Underthesea word segmentation using `word_tokenize(..., format="text")`.

The comparison records retrieval quality by category and tokenization/query
latency. Underthesea is an experiment dependency, not a predetermined runtime
dependency. Keep it only if observed Vietnamese quality gain justifies its
latency and maintenance cost. Do not add PyVi, VnCoreNLP or a tokenizer grid to
the initial scope.

## Approved Gate 0: Golden Dataset V3

Implementation plan:
`docs/superpowers/plans/2026-08-27-phase-8-golden-dataset-v3-implementation-plan.md`.

Plan đã tạo `golden_v3.jsonl` gồm `45` cases và exact 10-case smoke subset.
Reviewer đã xác minh độc lập và user phê duyệt final content/size ngày
`2026-08-28 +07`. Gate 0 đã hoàn tất; Phase 8 benchmark vẫn không được chạy cho
tới khi exact notebook group hoàn tất research/brainstorming và được user duyệt.

### Locked dataset decisions

- Preserve Phase 7 and V2 datasets unchanged; V3 may reuse, rewrite, or reject
  good V2 candidates but writes a separately named dataset.
- Keep the nine approved category names for diagnostics without category or
  source-family quotas and without a cross-matrix.
- Keep only six row fields: `case_id`, `question`, `keywords`,
  `reference_answer`, `category`, `evidence`.
- Use binary exact `source + section` relevance; no keyword proxy, LLM labeling
  or stored chunk IDs for Phase 8 retrieval ground truth.
- Smoke contains 10 exact full-dataset rows selected simply, without coverage
  quotas.
- Questions are natural Vietnamese tourist questions. Stop and ask the user
  when a useful case requires absent/conflicted corpus knowledge; never force a
  weak question to make 50, 45, a category, or a source count pass.
- Web research may inform naturalness and identify missing knowledge, but an URL
  is not evidence. Missing knowledge requires an approved/indexed Markdown
  update before the case can enter V3.

### Benchmark-grade ground truth decisions resolved by Gate 0

The new evidence mapping is stable across embedding-specific isolated indexes
because it labels canonical source/section pairs rather than chunk IDs. The
user-approved full 45 cases support final local retrieval selection; the
10-case subset is smoke only. Gate 1 common winner/uncertainty contracts above
use the actual V3 distribution and do not restore historical V2 quotas.

## Current handoff after Notebook 08a approval

Global contracts and Notebook 08a are approved. Implementation, independent
review and user confirmation completed on `2026-08-29 +07`. Continue with
Notebook 08b research/brainstorming; its implementation/run still requires an
exact approved design.

Before each real group, reverify current model/provider availability, model IDs,
licenses, dimensions, API schemas, limits and machine compatibility from primary
sources. That verification may trigger a user-reviewed refinement but cannot
silently expand scope or authorize execution.

## Resource-bound execution amendment (2026-08-29 +07)

This amendment supersedes the earlier local matrices and BGE learned-sparse
coverage. Local execution is limited to E5-small 384D, Huydang DEk21 native
768D and E5-base 768D. MiniLM-L12, E5-large 1024D, BGE-M3 1024D and every Qwen3
Embedding variant must not be downloaded or executed locally. Historical
MiniLM-L12 and Qwen3 384D CSV rows remain rejection evidence only.

After the three local settings complete, a separate paid proposal may cover
OpenRouter `intfloat/multilingual-e5-large` and `baai/bge-m3` dense embeddings.
The proposal is not implementation/run authorization and must reverify current
catalog, schema, pricing, provider behavior and exact preprocessing. OpenRouter
dense embeddings do not authorize or provide evidence for BGE learned sparse or
ColBERT, so those paths are removed from the local 08b/08d matrix.

The MiniLM-L12/Qwen model caches and isolated collections were deleted with user
authorization on `2026-08-29 +07`. Reviewer evidence covers all three retained
models at 3/3 repetitions. Notebook 08a is approved; 08b is the next design
checkpoint.
