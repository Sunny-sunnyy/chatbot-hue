# Project Status

Last updated: `2026-08-29 +07`

## Mục tiêu

`hue_rag` xây dựng:

- RAG Chatbot về văn hóa và du lịch Huế;
- Hue Foods RAG MVP;
- Hybrid Recommender + LLM;
- Agentic RAG sau khi MVP ổn định.

Trọng tâm hiện tại là hoàn thành Hue Foods RAG theo hướng code đơn giản, dễ
hiểu và được chạy bằng dữ liệu, database, model và API thật.

## Dữ liệu và thành phần hiện có

Luồng dữ liệu:

```text
raw -> Markdown source dumps -> curated Markdown
-> chunks -> embeddings/index -> retrieval -> context -> answer
```

Dữ liệu foods:

- 57 restaurants;
- 24 cafes;
- 9 local specialties;
- `food-guides.md` gồm 17 sections;
- `knowledge-base-hue/foods/evaluation/tests.jsonl` gồm 104 câu thật;
- Phase 7 dùng thêm `test2.jsonl` gồm 20 câu được chọn nguyên vẹn từ bộ 104.

Runtime hiện có:

- 572 chunks từ curated foods Markdown;
- local dense embedding `intfloat/multilingual-e5-small`, 384 dimensions;
- deterministic sparse representation hiện còn trong runtime để giữ Phase 4
  compatibility;
- Qdrant collection `hue_foods_e5_small_384`, 572 points, hiện vẫn có stored
  sparse vectors và chỉ được inspect read-only;
- profiles `dense_only`, `hybrid_no_rerank`, `hybrid_rerank`;
- local BM25 và MiniLM reranker;
- bounded context;
- grounded generation bằng `gpt-5.4-nano`;
- JSON API và startup warm-up.

Active Hue Qdrant collection chỉ read-only trong implementation, test và review
thông thường.

## Trạng thái Phase 0–9

| Phase | Trạng thái | Kết quả hiện có / việc còn lại |
|---:|---|---|
| 0 | `approved` | Simplicity review đã approved; docs-only, không đổi runtime hoặc active collection |
| 1 | `approved` | Backend foundation đã đơn giản hóa, chạy thật, review và được user xác nhận |
| 2 | `approved` | Foods Markdown chunking đã đơn giản hóa, chạy thật, review và được user xác nhận |
| 3 | `approved` | Embedding/sparse đã được đơn giản hóa, chạy thật, review và được user xác nhận |
| 4 | `approved` | Simplicity implementation đã chạy thật, review và được user xác nhận; candidate chưa cutover |
| 5 | `approved` | Ba profiles, notebooks và full non-paid suite đã đạt và được user xác nhận |
| 6 | `approved` | Answer-only API và notebooks đã chạy thật, đạt Codex review vòng 2 và được user xác nhận |
| 7 | `approved` | Baseline và post-simplicity correction đã chạy thật, đạt independent review và được user xác nhận |
| 8 | `not_ready` | Notebook 08a đã approved với ba local dense models; bước kế tiếp là research/brainstorming exact 08b |
| 9 | `not_ready` | Roadmap Agentic RAG, chưa có implementation scope được duyệt |

Milestone 6.1 Baseline Lifecycle Hardening thuộc Phase 6 và đã được user xác
nhận.

Phase 6 simplicity design và implementation plan được user xác nhận ngày
`2026-08-25 +07`:

```text
docs/superpowers/specs/2026-08-25-phase-6-generation-api-simplicity-design.md
docs/superpowers/plans/2026-08-25-phase-6-generation-api-simplicity-implementation.md
```

Phase 6 simplicity implementation đã đơn giản hóa context/prompt/generator/API/
logging và migrate direct Phase 7/notebook consumers. Scope không mở
conversation memory, streaming, retry, source response hoặc provider mới.

## Trạng thái hiện tại

Phase 6 simplicity implementation đã đạt Codex review vòng 2 và được user xác
nhận ngày `2026-08-26 +07`. Public chat response chỉ còn `answer`; context là
labeled string; generator trả string và gom known SDK/provider failures thành
HTTP 503. Fresh Reviewer run đạt 10 tests, Notebook 05–06 Run All thật, active
collection vẫn 572 points và scoped diff sạch. Broad suite và batch 20 câu
không chạy lại ở correction vì correction không đổi success path.

Governance đơn giản hóa toàn dự án đã được user thiết kế, phê duyệt, review và
cập nhật vào các tài liệu hiện hành. Phase 7 giữ trạng thái `approved` theo
`guides/phase_7_retrieval_answer_evaluation.md`: baseline đã chạy real Qdrant,
nano/mini, 20/104 questions và Notebook 07; correction vòng 1 đã được user xác
nhận ngày 2026-08-24 +07. Post-simplicity correction sau Phase 0–6 cũng đã được
Implementer hoàn tất, Reviewer chạy lại độc lập và user xác nhận sau khi chạy
Notebook 07 ngày 2026-08-26 +07. Approval này không cấp quyền sửa dataset.

Phase 7 mới phải đi theo luồng:

```text
question -> retrieve -> build context -> generate -> judge -> report
```

Hai CSV cố định hiện mỗi file giữ 20 ordered rows từ lần Reviewer chạy gần nhất:
retrieval 20/20 và answer 20/20 không có row error. Full-run 104 rows và một
answer row lỗi model tham chiếu source ID không hợp lệ vẫn được giữ như
historical evidence trong implementation/Codex review reports, không phải nội
dung hiện tại của CSV. Canonical Notebook 07 có 22 cells, đã được làm sạch
execution counts/outputs sau lần user kiểm tra; Reviewer Run All evidence nằm ở
`/tmp/07_evaluation-phase7-review.ipynb`.

Phase 7 code tương thích đúng Phase 6 context-string/generator-string. Public
answer batch/UI không còn `collection_name`; override được giữ ở retrieval-only
path mà không thêm abstraction. Fresh Reviewer run đạt 9 tests, Notebook 07 Run
All thật, active collection vẫn 572 points và user đã xác nhận correction. Audit
và design golden dataset được tách sang session riêng:

```text
reports/phase_7_golden_dataset_audit.md
```

Phase 8 vẫn đóng. Golden Dataset V2 đã được Implementer xây đủ 100 full cases và
20 smoke cases, nhưng manual review trả `changes_requested` ba vòng do câu hỏi
gượng, trùng ý, quota-shaped, keyword/evidence issues. User đã chọn complexity
reset thay vì correction vòng 4/5 và duyệt Golden Dataset V3 ngày
`2026-08-27 +07`.

V3 là Gate 0 canonical hiện hành:

```text
docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md
docs/superpowers/plans/2026-08-27-phase-8-golden-dataset-v3-implementation-plan.md
reports/phase_8_golden_dataset_v3_implementation_report.md
reports/phase_8_golden_dataset_v3_codex_review.md
```

V3 final có `45` câu và smoke có `10` row deep-equal. Reviewer đã đọc toàn bộ
question/category/keywords/reference/evidence, mở mọi declared Markdown H2,
chạy validator, V2 regression và real retrieval metadata trên collection cô
lập. Technical verdict là `ready_for_user_confirmation`; user xác nhận final
content/size ngày `2026-08-28 +07`, vì vậy Gate 0 đã `approved`.

Web search được phép để nghiên cứu naturalness, tourist needs và conflict. URL
web không phải evidence. Kiến thức mới chỉ được dùng sau một exact curated
Markdown proposal được Reviewer/user duyệt và index.

Phase 8 Gate 1 common contracts đã được user phê duyệt ngày `2026-08-28 +07`.
Notebook 08a đã hoàn tất research, implementation, real Run All, independent
review và được user xác nhận ngày `2026-08-29 +07`. Final executable local dense
catalog có E5-small, Huydang DEk21 và E5-base; MiniLM-L12/Qwen bị loại sau
observed regression, còn CSV rows được giữ làm historical evidence. Phase 8
tổng thể vẫn `not_ready`; bước kế tiếp là research/brainstorming exact 08b và
chưa authorize implementation/run 08b–08e.

Common gates bảo vệ cả chín V3 categories, dùng hierarchical large-category và
exact small-category guardrails, paired bootstrap 10.000 lần với fixed seed và
95% percentile CI. Clear gain yêu cầu mọi guardrail, aggregate
`delta nDCG@5 >= +0.03` và lower CI bound lớn hơn 0. Mỗi candidate so fixed
control rồi survivor/heavier candidate so best lighter finalist.

Main local profile là CPU FP32, không quantization; document batch 8, query batch
1, reranker pair batch 4. Mỗi configuration đo cold load riêng, bỏ một warm-up
và chạy ba full 45-case repetitions; finalist phải đạt `3/3`. Failed/OOM được
ghi đúng và không auto retry/shrink/change device/fallback. GTX 1650 WSL2 GPU
enablement vẫn là session riêng.

Paid stage giữ production baseline và `llm_rag_reference_on_hue`, cộng tối đa ba
role-deduplicated finalists. Complexity dùng `low`/`medium`/`high` với rationale.
Canonical documents:

```text
docs/superpowers/specs/2026-08-26-phase-8-benchmark-model-selection-design.md
docs/superpowers/plans/2026-08-26-phase-8-benchmark-model-selection-experiment-plan.md
docs/superpowers/specs/2026-08-28-phase-8-08a-embedding-benchmark-design.md
docs/superpowers/plans/2026-08-28-phase-8-08a-embedding-benchmark-implementation-plan.md
```

Master design/plan giữ sequencing toàn Phase 8. Exact 08a documents authorize
code, pinned local model downloads và isolated candidate writes chỉ cho 08a;
chúng không authorize dataset edit, CUDA/PyTorch change, paid run, active Qdrant
mutation, production cutover hoặc later notebook groups.

User cũng đã duyệt notebook theo group ngày `2026-08-26 +07`: `08a` embedding,
`08b` retrieval/fusion, `08c` reranker, `08d` full local matrix, `08e`
generation finalists và `08_benchmark_model_selection` tổng hợp. Style bắt buộc
tham khảo `rag_old_0/*.ipynb` và `notebook_simple/**/*.ipynb`. Canonical
notebooks giữ sạch. Markdown notebook dùng tiếng Việt, code identifiers dùng
tiếng Anh; mỗi cell một việc, Markdown ngắn trước code và backend functions được
reuse thay vì duplicate runtime logic. Mỗi experiment group dùng một long-format
cumulative CSV (`overall` và category rows), upsert theo human-readable setting
key; không run ID, timestamp package, JSON song song, opaque configuration ID,
audit/resume engine hoặc memory manager. Repository outputs rỗng/
`execution_count: null`; Reviewer Run All thật trên temporary copy.

Current local retrieval coverage: dense-only, independent BM25-only, current
dense→BM25 rescoring, true hybrid dense+BM25, custom TF-IDF SparseEmbedder-only
và true hybrid dense+TF-IDF. BGE-M3 learned sparse cùng dense+learned-sparse đã
bị user loại khỏi local execution do giới hạn tài nguyên. Notebook 08d ghép mọi
valid local pre-rerank path với no-rerank và ba rerankers, không lặp
BM25/TF-IDF-only theo embedding label.

Initial true-hybrid fusion đã khóa ở hai phương pháp: RRF và independent min-max
weighted sum `0.6 dense / 0.4 sparse`. Không grid-search weights; chỉ đề xuất
targeted tuning nếu real evidence cho thấy weighted fusion có lợi và tuning có
khả năng thay đổi quyết định.

User đã khóa `llm_rag_reference_on_hue` làm mandatory baseline đúng runtime
flow: E5-small dense top 30 → raw `0.6 dense + 0.4 BM25` trên cùng candidates →
top 10 → current MiniLM input 10/output 5 → context tối đa 5 whole chunks/3000
ký tự → Qwen3.5-9B OpenRouter → GPT-5.4-mini judge. Mọi local path dùng generator
depth 30, fusion top 10, reranker 10→5 và no-rerank final top 5; report
Recall@30, Recall@10 và final MRR/nDCG/Recall@5. Top 10 không đi vào LLM.

Qwen3 Embedding 0.6B và MiniLM-L12 đã bị user loại khỏi local scope ngày
`2026-08-29 +07` do quality regression; Qwen còn quá chậm trên CPU, MiniLM bị
truncate 83/572 chunks ở max length 128. Exact local dense catalog chỉ còn
E5-small 384D, Huydang DEk21 768D và E5-base 768D. Historical CSV rows được giữ,
nhưng hai model không được chạy lại hoặc đưa vào 08b/08d.

Notebook 08b đã khóa một comparison tokenizer tiếng Việt: Unicode `\w+` hiện
hành versus Underthesea `word_tokenize(..., format="text")`. Underthesea chỉ
được giữ nếu quality theo corrected Vietnamese gold tăng đủ để biện minh latency
và dependency; initial scope không thêm tokenizer thứ ba.

Phase 0 simplicity review đã được user duyệt ngày `2026-08-24 +07`. Review giữ
nguyên capability của MVP, đặt concrete code làm mặc định, chỉ giữ abstraction
cho nhiều implementation thật hoặc provider boundary thật, và yêu cầu mỗi
Phase 1–6 có một hồ sơ Before/After. Không có runtime change; baseline mới nhất
vẫn là full backend `222 passed, 4 warnings`.

Phase 1 simplicity implementation đã được review và user xác nhận ngày
`2026-08-24 +07`. YAML/settings/schema/package layout được giữ; logging chung
đã kết nối tại API lifespan, ingestion main và evaluation main; active-profile
validation đã inline; Notebook 01 và config README trùng lặp đã xóa. Live
settings/logging/Uvicorn/Gradio/Qdrant checks đạt và active collection vẫn 572
points. Hai suite 74/222 tests đã chạy là observed history quá rộng, không phải
acceptance target hoặc bằng chứng rằng mọi test đều cần thiết.

Phase 2 simplicity implementation đã được review và user xác nhận ngày
`2026-08-24 +07`. Parser và metadata helper đã được hấp thụ vào chunker, text
splitter được giữ riêng, Notebook 02 chỉ gọi public API và ordered corpus vẫn
khớp tuyệt đối 572 chunks từ 91 files. Focused suite 15 tests bảo vệ distinct
Phase 2 behaviors; downstream 79 và full 206 test runs chỉ là observed evidence
theo blast radius của refactor, không phải acceptance target hoặc checkpoint
mặc định cho các lần chạy sau.

Phase 3 simplicity implementation đã được review và user xác nhận ngày
`2026-08-25 +07`. Dense runtime nay chỉ còn concrete `E5Embedder` với
instance-owned lazy model, E5 prefixes cố định và native batching; provider
abstraction, outer batching và OpenRouter adapter/config/tests đã bị xóa. Sparse
TF-IDF được làm rõ hơn và tạm giữ để Phase 4 compatibility; user đã chốt ngày
`2026-08-25 +07` rằng coordinated Phase 4–5 simplification sẽ bỏ stored sparse
khỏi active baseline nhưng giữ Python BM25 và CrossEncoder cho benchmark.

Observed Phase 3 result:

- Notebook 03 Run All: 572 x 384, norm 1.0, 26.13 giây;
- active `dense_only` query trả 10 results với top chunk Bún bò Huế;
- focused 10, affected 59 và full backend 190 tests đã pass;
- active `hue_foods_e5_small_384` vẫn 572 points và không còn guarded
  test collection;
- không chạy lại Phase 7 evaluation vì model, dimension, instructions và
  retrieval behavior được giữ; real active query đã pass.

## Coordinated Phase 4–5 đã được user xác nhận

Correction revision 2 đã được Codex review độc lập và user xác nhận ngày
`2026-08-25 +07`. Design, plan và review canonical là:

```text
docs/superpowers/specs/2026-08-25-phase-4-5-qdrant-retrieval-simplicity-design.md
docs/superpowers/plans/2026-08-25-phase-4-5-qdrant-retrieval-simplicity-implementation.md
reports/phase_4_5_qdrant_retrieval_simplicity_codex_review.md
```

Candidate `hue_foods_e5_small_384_dense` có 572 dense-only points và artifact giữ
104/104 ordered-ID parity cho cả ba profiles. Active/candidate startup, Notebook
03–05, focused 27 tests và full non-paid 90 tests đã đạt trong independent
Reviewer run. Candidate chưa cutover; approval cutover vẫn là quyết định riêng.
Active cũ tiếp tục read-only và được giữ làm rollback.

Simplicity/test audit cuối trước bàn giao đã xác nhận:

- target code chỉ còn direct dense PointStruct/Qdrant ingestion, Python BM25,
  concrete instance-owned MiniLM và direct RetrievalService composition;
- không thêm provider abstraction, registry, cache layer, retry framework,
  fingerprint, hot reload, compatibility wrapper hoặc dependency mới;
- bỏ đề xuất test private reranker helper/fabricated model output; finite/count
  validation vẫn nằm trong production code và real MiniLM run là evidence;
- không giữ service-level dead-Qdrant test trùng lặp; real API 503 khi Qdrant
  unavailable/collection biến mất bảo vệ user-visible failure;
- một pure report-calculation test nhỏ được phép nhưng không phải system
  evidence; fresh active/candidate 104 questions x 3 profiles mới là evidence;
- mỗi affected old test chỉ được giữ khi report trả lời rõ hành vi người dùng
  mà nó bảo vệ; duplicate hoặc mechanism-only test phải xóa;
- không có test-count target, không chia thêm test files cho rare cases, không
  dùng mock/fake cho implementation hoặc evidence;
- active `hue_foods_e5_small_384` phải read-only; chỉ guarded
  `hue_rag_live_test_` collections và fixed candidate
  `hue_foods_e5_small_384_dense` được phép mutate trong approved plan;
- không cutover, xóa long-lived collection, chạy paid generation/judge, commit
  hoặc push. Các hành động đó cần approval riêng theo plan.

## Quyết định hiện hành

- Mỗi phase có một guide canonical.
- Code phải rõ ràng, dễ hiểu và không kỹ thuật hơn nhu cầu thật.
- Reviewer phải yêu cầu bỏ over-engineering.
- Chỉ tạo test cho hành vi thật và lỗi quan trọng; không chạy theo số lượng.
- Audit test theo ownership của phase; xóa và không chạy test không bảo vệ nhu
  cầu người dùng, chỉ dựng lỗi giả định hoặc chỉ phục vụ cơ chế bị loại bỏ.
- Exact live path là bằng chứng chính; một phase có thể không cần automated
  test.
- Full backend suite chỉ chạy cho shared runtime/data contract có blast radius
  rộng hoặc final Phase 0–6 check.
- Evaluation 20 câu chỉ chạy khi thay đổi có thể ảnh hưởng chất lượng RAG;
  không mặc định chạy bộ 104 câu trong simplicity review.
- Không dùng mock/fake trong test, implementation hoặc evidence.
- Completion evidence đến từ dữ liệu và hệ thống thật.
- Reviewer/Implementer được dùng online và paid API trong approved phase.
- Không có consent gate, cost cap hoặc cost-estimation code cho run đã nằm
  trong guide.
- Provider/model/scope mới, deploy, active mutation và destructive action cần
  user approval.
- Chỉ phase có giá trị học tập thật mới có notebook; canonical guide quyết định.
- Xác nhận phase không tự cấp quyền commit/push.
- Sau lần `changes_requested` thứ 4, dừng để audit lại design/guide/plan trước
  vòng sửa thứ 5.
- CodeGraph được giữ như công cụ discovery tùy chọn, không phải blocker.
- Chỉ giữ abstraction khi có nhiều implementation thật hoặc provider boundary
  thật; internal wrappers không phải compatibility requirement.
- Mỗi Phase 0–6 có một simplicity review ghi Before/After, capability được giữ,
  ảnh hưởng downstream, verification, bug và cách xử lý.
- Verification đi theo blast radius; chỉ chạy lại Phase 7 evaluation khi thay
  đổi có thể ảnh hưởng chất lượng RAG.
- Active production target đã được user chốt là Qdrant dense-only. Coordinated
  Phase 4–5 simplification bỏ custom TF-IDF sparse vectors khỏi active schema,
  point construction và ingestion; trong cùng implementation scope chuyển
  shared tokenization sang BM25/scoring ownership và chỉ xóa `SparseEmbedder`
  sau consumer audit sạch. Python BM25 và CrossEncoder được giữ nguyên.
- Ba canonical Phase 8 profiles giữ exact path: Qdrant dense candidates ->
  optional Python BM25 fusion -> optional CrossEncoder.
- Phase 8 đánh giá true hybrid retrieval bằng isolated candidate collection có
  sparse vectors và fair controlled comparison. Chỉ đề xuất đưa sparse storage
  trở lại production khi real results chứng minh lợi ích tương xứng complexity;
  exact active transition cần user approval riêng.
- Joint Phase 4–5 design dùng blue-green migration: giữ
  `hue_foods_e5_small_384` read-only, tạo dense-only candidate
  `hue_foods_e5_small_384_dense`, chạy real ingestion/retrieval verification,
  rồi dừng xin approval trước config cutover. Collection cũ được giữ làm rollback
  và cleanup cần approval riêng.
- Test Phase 4–5 chỉ bảo vệ hành vi thật/lỗi quan trọng, không có count target,
  mock/fake system evidence, rare-mechanics test sprawl hoặc test không giải
  thích được user need.
- Reset giữ thành exact command riêng nhưng bỏ runtime config flag và các
  schema/payload pre-delete guards tự khóa migration. Safety dựa trên exact
  required `--collection`, matching `--confirm "DELETE <name>"`, displayed point
  count, explicit active/rollback approval và post-delete absence verification;
  target không phụ thuộc active config.
- Qdrant client cache và manual upsert retry bị loại: mỗi composition root tạo
  một client; lỗi trả thẳng và rerun ingestion dựa trên deterministic UUID5/
  idempotent upsert. Batch 64 và timeout 30 giây vẫn giữ.
- Point payload giữ `embedding_model` để bảo vệ same-dimension model mismatch,
  nhưng bỏ `embedding_dimension`; dimension/distance lấy từ Qdrant schema/config.
- Phase 5 giữ small immutable runtime status cho API/health/debug nhưng bỏ
  corpus/config fingerprints, `verify_snapshot()` và tests chỉ phục vụ chúng;
  collection/config đổi thì restart process.
- Candidate rerun giữ pre-upsert scan 572 points: existing UUID5 IDs phải thuộc
  canonical set và `embedding_model` phải khớp trước mutation; exact count 572
  được kiểm sau upsert. Không giữ payload dimension check hoặc test permutations.
- `vectorstore/hybrid_index.py` được thay bằng pure `vectorstore/points.py`;
  Qdrant I/O ở `upsert.py`. Xóa test file hybrid riêng và nhập các behavior tests
  còn cần vào ingestion tests.
- Phase 5 reranker được gộp thành một concrete
  `reranking/cross_encoder.py` với instance-owned real MiniLM; xóa base/scorer/
  model wrappers, module cache và fake seam nhưng giữ finite/count validation,
  deterministic non-mutating output và fail-explicit profile semantics.
- MiniLM được load/download thật chỉ cho `hybrid_rerank` trong approved run;
  dùng library cache bình thường nhưng không app cache, cache-only gate, preload
  script hoặc missing-cache tests. Failure fail explicit.
- `scoring/bm25.py` nhận tokenizer và tự sở hữu DF/IDF; xóa `SparseEmbedder`/
  test riêng sau consumer audit, không thêm `rank_bm25`. BM25 tests được gom theo
  Vietnamese tokenization, known ranking, fusion validity và real retrieval.
- Giữ concrete DenseRetriever, HybridRetriever và RetrievalService nhưng xóa
  optional `RetrievalStack`; startup tạo service trực tiếp với đúng components
  và small runtime status. Xóa tests chỉ dựng missing/invalid stack thủ công.
- Giữ ContextBuilder JSON whole-chunk contract vì API/evaluation/prompt dùng
  thật; chỉ gom 10 tests thành vài behavior tests về budget, structural source
  mapping và empty/non-mutation, đồng thời xóa generator-test overlap.
- Bỏ `vector_database.scroll_batch_size`, startup override và test seam; giữ
  bounded Qdrant payload pagination bằng constant nội bộ 128, verify real đủ 572
  unique payloads.
- Blue-green evidence chạy fresh 104 retrieval questions × 3 profiles trên
  active baseline trước refactor và dense-only candidate sau refactor; so sánh
  metrics/latency/failures/diffs, không gọi generator/judge và không chọn Phase 8
  winner.
- Candidate ingestion/retrieval evaluation nhận optional exact collection name
  tại composition root và dùng in-memory settings copy; API/settings.yaml giữ
  active cũ tới cutover approval, không candidate YAML/env/global manager.
- OpenRouter embedding không còn là Phase 3 runtime boundary. Phase 8 mới xác
  minh exact API/model/dimension/limits/pricing và tạo adapter/config theo
  candidate được duyệt.

Các cơ chế cost accounting, consent gate, calibration, resume, run identity,
timestamp package, checksum, package matching, tamper detection, partial
artifact, complex artifact audit, layered validators và tests chỉ phục vụ chúng
phải được loại bỏ trong đúng approved scope, không đổi tên hoặc di chuyển để
giữ lại.

## Worktree và an toàn

Gate 1 và exact Notebook 08a documentation sync được user yêu cầu commit/push
ngày `2026-08-28 +07`. Agent tiếp theo vẫn phải coi working tree là shared state
và:

- chạy `git status --short` trước khi sửa;
- đọc diff của exact files trong scope;
- giữ nguyên thay đổi không liên quan;
- không reset, checkout, broad-delete, stage, commit hoặc push ngoài quyền;
- không mở hoặc expose secret values;
- giữ active Hue Qdrant collection read-only.

## Next action

```text
Phase 0–6 simplicity review đã approved
-> Phase 7 post-simplicity correction đã approved
-> Golden Dataset V2 dừng ở historical changes_requested sau 3 vòng
-> user đã duyệt complexity reset và Golden Dataset V3 design/plan
-> Implementer đã tạo V3; Reviewer kiểm tra toàn bộ 45 câu, smoke 10 và evidence
-> user đã chấp nhận final content/size; Gate 0 approved ngày 2026-08-28 +07
-> Gate 1 common contracts approved ngày 2026-08-28 +07
-> Notebook 08a đã triển khai, review độc lập và được user xác nhận
-> MiniLM-L12/Qwen bị loại khỏi executable catalog; historical CSV giữ lại
-> research + brainstorm exact Notebook 08b
```

Session tiếp theo research và brainstorm exact Notebook 08b. Gate 1/08a handoff
đã hoàn tất; lịch sử vẫn truy xuất được qua Git.
Nguồn canonical hiện hành:

```text
docs/superpowers/specs/2026-08-26-phase-8-benchmark-model-selection-design.md
docs/superpowers/plans/2026-08-26-phase-8-benchmark-model-selection-experiment-plan.md
docs/superpowers/specs/2026-08-28-phase-8-08a-embedding-benchmark-design.md
docs/superpowers/plans/2026-08-28-phase-8-08a-embedding-benchmark-implementation-plan.md
guides/phase_8_benchmark_model_selection.md
```

Thứ tự bắt buộc từ trạng thái hiện tại:

1. giữ nguyên Golden Dataset V3 đã approved gồm 45 full + 10 smoke cases;
2. giữ Notebook 08a và ba-model catalog đã approved;
3. research/brainstorm exact Notebook 08b và chờ user duyệt trước implementation.

V3 là complexity reset đã được user duyệt và Gate 0 đã approved. Các
prompt/handoff V2 đã được retire khỏi cây hiện hành ngày `2026-08-27 +07`;
hai prompt Implementer/Reviewer V3 cũng được retire sau Gate 0 approval ngày
`2026-08-28 +07`. Gate 1 brainstorming handoff đã được loại khỏi cây hiện hành
sau khi exact 08a design/plan được approved. Không khôi phục các handoff đã hoàn
tất; dùng exact Notebook 08a Implementer/Reviewer handoff dựa trên canonical
design/plan hiện hành.

GPU/WSL2 remediation vẫn là session riêng. Production cutover hoặc active
collection mutation không nằm trong Phase 8 benchmark authorization.

Khi review Phase 0–6, Repo và live system là nguồn đối chiếu chính: guide,
reports, source code, notebook và real run đủ để bắt đầu. Tài liệu ngoài do
user cung cấp chỉ dùng khi thực sự hữu ích. Nếu không có và vẫn còn lựa chọn
quan trọng, Reviewer brainstorm với user trước khi duyệt design thay đổi.
Không dùng Phase 7 reference làm blueprint cho phase khác.

## Tài liệu đọc tiếp

Mọi coding agent:

```text
session_prompt/Session_Prompt.md
session_prompt/Project_Status.md
workflow đúng với vai trò
guides/README.md
guides/phase_0_mvp_foundation.md
guide canonical của phase đang làm
```

Review đơn giản hóa Phase 1–6:

```text
docs/superpowers/specs/2026-08-24-phase-0-simplicity-review-design.md
reports/phase_0_mvp_foundation_simplicity_review.md
guides/llm_rag_reference_for_hue_rag.md
docs/superpowers/specs/2026-08-24-phase-1-backend-foundation-simplicity-design.md
docs/superpowers/plans/2026-08-24-phase-1-backend-foundation-simplicity-implementation.md
reports/phase_1_backend_skeleton_simplicity_review.md
docs/superpowers/specs/2026-08-24-phase-2-foods-markdown-chunking-simplicity-design.md
docs/superpowers/plans/2026-08-24-phase-2-foods-markdown-chunking-simplicity-implementation.md
reports/phase_2_foods_markdown_chunking_simplicity_review.md
docs/superpowers/specs/2026-08-24-phase-3-embedding-sparse-representation-simplicity-design.md
docs/superpowers/plans/2026-08-24-phase-3-embedding-sparse-representation-simplicity-implementation.md
reports/phase_3_embedding_sparse_representation_simplicity_review.md
guides/phase_3_embedding_sparse_representation.md
docs/superpowers/specs/2026-08-25-phase-4-5-qdrant-retrieval-simplicity-design.md
docs/superpowers/plans/2026-08-25-phase-4-5-qdrant-retrieval-simplicity-implementation.md
guides/phase_4_qdrant_ingestion.md
guides/phase_5_retrieval_profiles_reranking.md
```

Phase 7:

```text
guides/phase_7_retrieval_answer_evaluation.md
docs/superpowers/specs/2026-08-23-phase-7-simple-evaluation-design.md
docs/superpowers/plans/2026-08-23-phase-7-simple-evaluation-implementation.md
docs/superpowers/specs/2026-08-26-phase-7-post-simplicity-correction-design.md
docs/superpowers/plans/2026-08-26-phase-7-post-simplicity-correction.md
reports/phase_7_golden_dataset_audit.md
reports/hue_foods_rag_benchmark.md
```

## Phase 8 local resource amendment — 2026-08-29 +07

User đã hủy local execution cho MiniLM-L12, toàn bộ Qwen3 Embedding,
`e5-large-1024` và `bge-m3-dense-1024` trên máy hiện tại. Exact local dense
catalog chỉ còn E5-small 384D, Huydang DEk21 768D và E5-base 768D. Mọi
runtime/notebook boundary phải reject settings đã loại trước download, model
load hoặc Qdrant write.

Sau khi ba local models hoàn tất, có thể research/propose paid OpenRouter dense
benchmark cho `intfloat/multilingual-e5-large` và `baai/bge-m3`; chưa authorize
adapter, key access, API call hoặc budget. BGE learned sparse/ColBERT không được
OpenRouter dense output thay thế và bị loại khỏi local 08b/08d matrix. Phase 8
vẫn `not_ready`.

User đã authorize cleanup E5-large artifact từ Reviewer run trước. Collection
`hue_foods_08a_e5_large_1024` và 10 `e5-large-1024` CSV rows đã được xóa ngày
2026-08-28 +07; active production collection không thuộc cleanup target.

E5-small, Huydang DEk21 và E5-base đều có 3/3 evidence trên 45 cases và 572
chunks. Cache/isolated collections của MiniLM-L12 và Qwen đã bị xóa; historical
CSV rows của cả hai được giữ. Reviewer xác minh catalog ba-model, tests, lockfile,
notebook và Qdrant read-only; user chạy notebook thành công và xác nhận 08a ngày
`2026-08-29 +07`.
