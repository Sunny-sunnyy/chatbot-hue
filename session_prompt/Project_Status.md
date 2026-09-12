# Project Status

Last updated: `2026-09-12 +07`

## Project overview

`hue_rag` xây dựng hệ thống RAG về văn hóa và du lịch Huế. Baseline đã có là
Hue Foods RAG MVP. Curation/taxonomy toàn corpus đã hoàn tất; dự án đang thiết
kế lại pipeline cho toàn bộ curated corpus. Hybrid Recommender và Agentic RAG
là roadmap, chưa có approved implementation scope.

Project ưu tiên code/data flow dễ hiểu, complexity tương xứng nhu cầu và bằng
chứng từ dữ liệu, database, model cùng API thật.

## Current active handoff snapshot

User đã xác nhận closure **Full-corpus Phase 2** ngày 2026-09-12 sau ba
correction và independent static review. Toàn bộ W1-R1..R5, W1-C1-R1..R3 và
W1-C2-R1 đã đóng; final review là
`reports/full_corpus_rag_wave_1_correction_3_codex_review_2026_09_12.md`.

Observed Phase 2 artifact: `PASS`, 205 sorted/unique files, 8460 chunks, ba
condition rules, zero blocking errors/oversized; max token `366/512`, `366/512`,
`255/256`. Implementer báo fresh offline suite `39 passed, 1 warning` và repeated
preview byte-identical; Reviewer không rerun dynamic checks. `8460` là observed
artifact count, không phải hard-coded product invariant.

User đã xác nhận closure **Full-corpus Phase 3** ngày 2026-09-12 sau hai
correction và independent final review. Fresh offline preflight `PASS`: 205
files, 8.460 chunks, sample 12, zero tokenizer over-limit, sparse deterministic;
Qwen3-Embedding-0.6B chạy GTX 1650 bằng CUDA FP16/eager/native 1024D, batch 1.
Final review:
`reports/full_corpus_phase_3_embedding_sparse_correction_2_codex_review_2026_09_12.md`.

Active handoff thuộc **Implementer**, kind `implementation`, cho Full-corpus
Phase 4 Tasks 1–6. Conceptual design, Written Spec, Implementation Plan và
Review Contract đã được User duyệt ngày 2026-09-12. Handoff cho phép code,
deterministic checks và một read-only preflight chỉ trên bốn exact full-corpus
targets. Chưa có quyền dense-encode toàn corpus hoặc Qdrant mutation; Task 7
live build cần User approval riêng sau khi Reviewer kiểm preflight.

## System and data map

Luồng chính:

```text
raw sources -> curated foods Markdown -> 572 chunks
-> embeddings/Qdrant + optional local lexical scoring
-> retrieval -> optional reranking -> bounded context
-> grounded generation -> answer-only API
```

Foods corpus hiện gồm:

- 57 restaurants;
- 24 cafes;
- 9 local specialties;
- `food-guides.md` với 18 sections;
- 91 curated Markdown files tạo 572 deterministic chunks;
- Golden Dataset V3 canonical có 45 full cases và 10 smoke rows deep-equal.

Không chunk trực tiếp từ source dumps. Curated Markdown là closed-world source
cho retrieval/evaluation; web research không tự trở thành Golden evidence.

## Current runtime and data

Production baseline hiện dùng:

- local embedding `intfloat/multilingual-e5-small`, 384 dimensions;
- active Qdrant collection `hue_foods_e5_small_384`, 572 points;
- profiles `dense_only`, `hybrid_no_rerank`, `hybrid_rerank`;
- Python BM25 và concrete local MiniLM cross-encoder reranker;
- bounded whole-chunk context;
- grounded generation bằng `gpt-5.4-nano`;
- answer-only JSON API và startup warm-up.

Active collection còn legacy sparse vector state từ các phase trước nhưng là
read-only trong implementation/review thông thường. Dense-only candidate
`hue_foods_e5_small_384_dense` tồn tại làm blue-green evidence; production chưa
cutover.

Notebooks 08a/08b/08c đã có evidence benchmark trên Foods; kết quả và artifact
chi tiết nằm trong canonical map phía dưới. Evidence này không chứng minh chất
lượng trên toàn bộ dữ liệu đang bổ sung. Baseline trên được giữ từ trạng thái
đã ghi nhận, không được chạy lại ngoài exact approved gate.

## Thiết kế full-corpus hiện hành

Khảo sát parser/source locator đã được user **approved** sau correction lượt 3
ngày 2026-09-09; closure tại
`reports/full_corpus_parser_locator_codex_review_2026_09_09.md`, mục 9–10.
Chọn markdown-it-py 4.2.0/table enabled cho thiết kế locator trên source LF.
Đây là evidence mẫu, chưa là runtime full-corpus approved. Hai composites VN/QT
đã sửa ranh giới; counts input sai không dùng làm PASS.

Full-corpus đã có Written Spec, Implementation Plan và Review Contract được User
duyệt ngày 2026-09-11. Phase 2 discovery/parser/chunker/locator/Representation A
preview đã được User xác nhận closure ngày 2026-09-12. Chưa có quyền
implementation/live/runtime cho các phase sau ngoài exact active handoff. Guide umbrella hiện hành là
`guides/full_corpus_rag.md`. Khảo sát parser, hai input Ca Huế VN/QT,
Golden/evaluation reference, schema deep-dive và simplicity evaluation
`rag_old_0` đều đã được Reviewer kiểm và User xác nhận `approved/completed`.
Các survey là evidence thiết kế, không phải runtime approval.
Survey toàn project `llm_rag` dài 885 dòng vẫn bị đóng băng
working/non-canonical sau complexity reset. Verified Architecture Extraction
thay thế đã qua hai correction, independent Reviewer review và được User xác
nhận closure ngày 2026-09-11; artifact này là approved evidence companion.
Decision #1 đã chốt baseline A + hybrid candidate có sparse consumer thật;
Decision #2 chốt fresh-by-default và cho phép nhiều experiment collections.
Decision #3 chốt payload 5 fields, còn point ID và dense/sparse vectors dùng
trường Qdrant chuẩn. Decision #4 chốt staged retrieval/fusion/reranker matrix,
đo bằng metrics hiện hành và báo kết quả thực nghiệm. Decision #5 chốt
representation B theo staged finalists với API/index/full-corpus runs thật.
Decision #6a chốt strict minimal public response/citation/error contract;
#6b chốt budget linh hoạt theo generator profile nhưng cố định trong từng run;
#6c chốt Qwen3.5 9B/OpenRouter với upstream pinned cho hai vai trò generation và
giữ GPT-5.4 mini/OpenAI làm evaluation judge. #6d chốt Qwen profile
temperature 0, B output 256, answer 16384/2048/512, timeout 90 giây; Agentic RAG
dùng profile/contract riêng. #6e chốt UI inline citation/source cards. Decision
Queue tiền-spec đã hoàn tất; Written Spec đã được User duyệt ngày 2026-09-11.
Implementation Plan + Review Contract đã được User duyệt ngày 2026-09-11;
Phase 3 guide, Written Spec, Implementation Plan và Review Contract đã được User
duyệt ngày 2026-09-12; implementation qua hai correction đã independent review
PASS và được User xác nhận closure cùng ngày. Phase 4 design/spec/plan/Review
Contract đã được User duyệt; active Implementer handoff chỉ mở Tasks 1–6 và
exact read-only preflight. Dense full-corpus cùng mọi Qdrant write vẫn đóng.
User tiếp tục chốt workflow tuần tự: sau mỗi phase phải review/User closure và
cập nhật detailed phase guide; trước phase kế tiếp Reviewer phải dùng evidence
dependency để hoàn tất guide + phase spec + plan + Review Contract và xin User
duyệt. Không author ahead hoặc giao Implementer liên tục qua nhiều phase.
Quyết định/ngữ cảnh tại
`handoff_prompt/FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md`, snapshot đầu
file và các mục mới nhất. Session mới khởi động bằng bốn file chuẩn
`<ROLE>_WORKFLOW.md`, `Session_Prompt.md`, `Project_Status.md` và
`CURRENT_HANDOFF.md`; prompt Reviewer full-corpus cũ chỉ còn reference-only.
`handoff_prompt/README.md` dẫn các contracts đang hoạt động/đã completed.
Runtime Foods và approvals lịch sử bên dưới giữ nguyên. Nhiệm vụ hiện hành
chỉ ở CURRENT_HANDOFF.md; không chạy lại migration/correction đã completed.

## Phase status

| Phase | Status | Current result / next boundary |
|---:|---|---|
| 0 | `approved` | MVP foundation và simplicity governance |
| 1 | `approved` | Backend foundation |
| 2 | `approved` | Foods Markdown chunking |
| 3 | `approved` | Full-corpus embedding/sparse preflight User-closed; Qwen CUDA FP16 PASS trên GTX 1650 |
| 4 | `approved` | Foods history approved; full-corpus package approved, Tasks 1–6/read-only preflight active; dense/Qdrant write vẫn đóng |
| 5 | `approved` | Retrieval profiles và reranking |
| 6 | `approved` | Context, generation và answer-only API |
| 7 | `approved` | Retrieval/answer evaluation baseline |
| 8 | `not_ready` | Gate 0, Gate 1 và Notebooks 08a/08b/08c approved; full-corpus Phase 4 Tasks 1–6/preflight đang active |
| 9 | `not_ready` | Agentic RAG roadmap chưa có approved scope |

Git và canonical artifacts giữ lifecycle history; file này chỉ mô tả trạng thái
đang có hiệu lực.

## Decisions currently in force

- Tài liệu active và tương lai chỉ dùng `Phase` làm đơn vị lifecycle. Sau khi
  Spec/Plan/Review Contract của Phase được User duyệt, Reviewer cập nhật guide
  canonical và active Markdown trước Implementer handoff. Tên file/report/
  artifact lịch sử đã đóng giữ nguyên để bảo toàn audit trail.
- Mỗi phase có canonical guide; report/status không tự tạo requirement.
- User đã chỉ đạo và hoàn tất Taxonomy Migration ngày 08/09/2026:
  Cấu trúc `knowledge-base-hue/tourism/` đã được di chuyển hoàn toàn sang
  `knowledge-base-hue/travel/` với ba nhánh con: `travel/places/`,
  `travel/services/` và `travel/tickets/`. Toàn bộ 47 file đã được phân bổ
  và đồng bộ đường dẫn; thư mục cũ `tourism/` đã được thu hồi.
- Golden V3 45+10 và benchmark hiện tại thuộc Foods. Tạo Golden mới cho toàn bộ
  dữ liệu cần scope và thiết kế riêng; chưa thay Golden hiện hành.
- Golden mới được author/review theo P7 rồi merge thành một canonical JSONL;
  Foods V3 giữ nguyên. Schema metric-only có bốn required fields `question`,
  `keywords`, `reference_answer`, `category`; không lưu `case_id`, evaluator chỉ
  derive `case_index` từ thứ tự dòng khi cần.
- Official Golden/evaluation không lưu expected claims, evidence groups, source
  spans/chunk IDs, `case_type`, `domain` hoặc `claim_id`. `partition` chỉ dùng
  khi authoring rồi bị strip khi merge.
- Không hard quota; planning target 150–200 sau curation. Không dev/test; smoke
  deep-equal. Retrieval dùng K=10; ba Answer metrics dùng thang số nguyên 1–5;
  rubric mô tả đủ năm mức cho từng metric; điểm tổng dùng macro-average theo
  case. Official aggregate cần đủ mọi canonical case; lỗi kỹ thuật làm run
  incomplete, không bị loại khỏi mẫu số hoặc gán điểm chất lượng giả. Chưa đặt
  metric threshold trước full-corpus baseline.
- Golden `keywords` là các term/phrase quan trọng, chính xác, có dạng chữ nguyên
  văn trong corpus liên quan và được reference answer hỗ trợ; không thêm generic
  words, synonym phòng xa hoặc hard keyword quota.
- Category được Implementer gán sơ bộ theo thao tác chính thể hiện trong câu
  hỏi. Implementer author P7 từ corpus/tài liệu được giao, chỉ dùng web để học
  phương pháp viết tự nhiên; User và Reviewer đọc từng case để giữ, sửa,
  reclassify hoặc xóa trước merge.
- Working Golden dùng `evaluation/golden_full_corpus_authoring.jsonl` trong từng
  nhánh P7. Sau approval tuần tự của cả P7, merge thành
  `knowledge-base-hue/evaluation/golden_full_corpus.jsonl`; smoke nằm cạnh đó.
  Foods V2/V3 giữ nguyên và working files không vào official evaluator path.
- Smoke full-corpus có đúng 10 canonical rows chọn thủ công, mỗi P7 ít nhất một
  case và ưu tiên phủ thêm category; User và Reviewer duyệt, records deep-equal
  và không được sửa độc lập.
- Merge concat approved P7, strip authoring `partition`, rồi deterministic
  shuffle với fixed seed `42`; không ID/manifest/checksum. Sau khi canonical
  merge/xáo được kiểm, phải chạy full cả sáu metrics trên mọi case; smoke không
  thay full evaluation và planning target 150–200 không là quota.
- Full-corpus benchmark dùng isolated Qdrant collection theo dense embedding
  candidate: base matrix có ba baseline collections và có thể lên sáu khi giữ
  representation A/B cho cả ba model; sáu không phải hard cap experiment. Đây là
  lựa chọn cách ly benchmark/schema/lifecycle của User,
  không phải giới hạn tuyệt đối của Qdrant named vectors. Decision #1 chốt mỗi
  candidate collection lưu dense+sparse trên cùng points: baseline A query dense
  rồi BM25 local; hybrid candidate query cả dense và sparse rồi fusion.
  BM25/TF-IDF ở ngoài Qdrant; reranker/fusion/scoring không cần collection riêng.
  Decision #2 không đặt hard cap cho fresh experiment collections khi từng
  candidate/variant đã được duyệt; không in-place reconcile. Sau benchmark đề
  xuất giữ khoảng 1–3 collections tốt nhất. Exact replacement/cleanup cần target
  và approval riêng; Foods read-only. Exact schema/names/cutover chưa chốt.
- Survey dài `llm_rag` không phải canonical reference: sau bốn correction vẫn
  còn RR11 Major và đã bị đóng băng working/non-canonical. Verified Architecture
  Extraction thay thế đã qua hai correction, independent Reviewer review và
  User confirmation; artifact là approved evidence companion, không phải
  approval cho runtime, Spec, Plan hoặc các quyết định còn mở.
- Hai tài liệu `/home/minhhieu/llm_rag/tai_lieu/rag_agent_handoff_current_repo.md`
  và `rag_system_pipeline_deep_dive.md` là snapshot lịch sử `reference-only`,
  không full-read mặc định và không làm primary evidence. Source code hiện hành
  ưu tiên khi cần kiểm claim.
- Simplicity constraint cho spec/plan: một contract chỉ có một nguồn chính;
  không thêm sparse storage, alias/manifest/checksum/migration/cleanup,
  provider/plugin abstraction, representation B hoặc context expansion khi
  chưa có consumer/failure/experiment cụ thể được User duyệt.
- P7 được author/review tuần tự theo thứ tự đã chốt. Mỗi partition phải qua
  Implementer self-review, User + Reviewer full-case review, correction, recheck
  và User confirmation trước khi bắt đầu partition kế tiếp.
- Chi tiết experiment/model/matrix đã duyệt nằm trong guide/spec/plan Phase 8
  được dẫn dưới đây; không chép lại thành requirement độc lập trong status.
- Coding/testing dùng `skills/practical-project-coding/SKILL.md`; điều phối dùng
  `skills/risk-gated-agent-review/SKILL.md` và các workflow.
- Context loading dùng ba mức: `full-read` cho stable role rules, current handoff
  và active contract/report; `targeted-read` cho current snapshot/section liên
  quan; `reference-only` cho history, raw reference và report đã approved.
  Reviewer đọc full report đang review nhưng chỉ focused-check source; Implementer
  đọc full exact source/input trong approved scope. Không dùng câu “đọc toàn bộ
  mọi tài liệu được dẫn”.
- Nhiệm vụ và next action duy nhất nằm trong `session_prompt/CURRENT_HANDOFF.md`.
- Full-corpus thực hiện tuần tự:
  `Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7A Golden → Phase 7B Evaluator → Phase 8 Benchmark → integrated closure`.
  Mỗi phase phải có guide + spec + plan + Review Contract và User duyệt trước
  implementation; phase trước phải independent review và User closure trước.
- Correction 2 đã loại khỏi acceptance việc chạy toàn bộ `backend/tests` và
  `test_ingestion_pipeline.py`, vì các suite đó gọi real embedder/Qdrant và mâu
  thuẫn hard boundary offline của Phase 2. Chỉ chạy exact offline checks ghi trong
  Correction 2; không dùng full-suite failure làm Phase 2 evidence.
- Live Qdrant/API/paid, từng P7, finalist, representation B, winner/cutover/
  replacement/cleanup và Agentic RAG luôn cần exact approval riêng.

## Safety and authorization boundaries

- Active `hue_foods_e5_small_384` chỉ read-only nếu không có exact user approval.
- Không expose secret hoặc đọc raw `.env` content.
- Không dùng fake provider/data/artifact hoặc old output làm fresh PASS evidence.
- Provider/model/dataset mới, paid run ngoài approved guide, deploy, active
  mutation, destructive cleanup và production cutover cần authority mới.
- Commit/push chỉ thực hiện khi latest user instruction hoặc current handoff ghi
  exact Git authorization.
- Implementer không tự approve; Reviewer không sửa runtime thay Implementer.

## Canonical document map

Bootstrap và role governance:

```text
session_prompt/Session_Prompt.md
session_prompt/REVIEWER_WORKFLOW.md
session_prompt/IMPLEMENTER_WORKFLOW.md
session_prompt/CURRENT_HANDOFF.md
skills/risk-gated-agent-review/SKILL.md
skills/practical-project-coding/SKILL.md
```

Project/full-corpus/Phase 8 entrypoints:

```text
guides/README.md
guides/full_corpus_rag.md
guides/llm_rag_reference_for_hue_rag.md
docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md
docs/superpowers/plans/2026-09-11-full-corpus-rag-implementation-plan.md
handoff_prompt/FULL_CORPUS_RAG_IMPLEMENTATION_REVIEW_CONTRACT.md
handoff_prompt/FULL_CORPUS_RAG_WAVE_1_IMPLEMENTATION_PROMPT.md
handoff_prompt/FULL_CORPUS_RAG_WAVE_1_CORRECTION_1_PROMPT.md
handoff_prompt/FULL_CORPUS_RAG_WAVE_1_CORRECTION_2_PROMPT.md
handoff_prompt/FULL_CORPUS_RAG_WAVE_1_CORRECTION_3_PROMPT.md
reports/full_corpus_rag_wave_1_codex_review_2026_09_12.md
reports/full_corpus_rag_wave_1_correction_1_codex_review_2026_09_12.md
reports/full_corpus_rag_wave_1_correction_2_codex_review_2026_09_12.md
reports/full_corpus_rag_wave_1_correction_3_codex_review_2026_09_12.md  # final approved review
reports/full_corpus_rag_wave_1_correction_1_implementation_report_2026_09_12.md  # final evidence index
reports/user_reports/full_corpus_rag_wave_1_user_report_2026_09_12.md
reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json
handoff_prompt/LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_PROMPT.md
handoff_prompt/LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_CORRECTION_1_PROMPT.md
handoff_prompt/LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_CORRECTION_2_PROMPT.md
handoff_prompt/FULL_CORPUS_REVIEWER_NEXT_SESSION_PROMPT.md
reports/llm_rag_full_project_reference_survey_codex_review_2026_09_11.md
reports/llm_rag_verified_architecture_extraction_2026_09_11.md  # approved evidence companion
reports/llm_rag_verified_architecture_extraction_codex_review_2026_09_11.md  # closure
reports/llm_rag_verified_architecture_extraction_implementation_report_2026_09_11.md  # implementation evidence history
reports/llm_rag_verified_architecture_extraction_correction_1_implementation_report_2026_09_11.md  # correction history
reports/llm_rag_verified_architecture_extraction_correction_2_implementation_report_2026_09_11.md  # accepted correction evidence
guides/phase_0_mvp_foundation.md
guides/phase_8_benchmark_model_selection.md
reports/hue_foods_rag_benchmark.md
docs/superpowers/specs/2026-08-26-phase-8-benchmark-model-selection-design.md
docs/superpowers/plans/2026-08-26-phase-8-benchmark-model-selection-experiment-plan.md
```

Historical/non-canonical `llm_rag` artifacts, chỉ dùng khi cần audit lịch sử:

```text
handoff_prompt/LLM_RAG_FULL_PROJECT_REFERENCE_SURVEY_PROMPT.md
handoff_prompt/LLM_RAG_FULL_PROJECT_REFERENCE_SURVEY_CORRECTION_1_PROMPT.md
handoff_prompt/LLM_RAG_FULL_PROJECT_REFERENCE_SURVEY_CORRECTION_2_PROMPT.md
handoff_prompt/LLM_RAG_FULL_PROJECT_REFERENCE_SURVEY_CORRECTION_3_PROMPT.md
handoff_prompt/LLM_RAG_FULL_PROJECT_REFERENCE_SURVEY_CORRECTION_4_PROMPT.md
reports/llm_rag_full_project_reference_survey_2026_09_11.md
```

Golden V3 and completed 08a:

```text
docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md
reports/phase_8_golden_dataset_v3_codex_review.md
docs/superpowers/specs/2026-08-28-phase-8-08a-embedding-benchmark-design.md
docs/superpowers/plans/2026-08-28-phase-8-08a-embedding-benchmark-implementation-plan.md
reports/phase_8_08a_embedding_benchmark_codex_review.md
evaluation/results/phase8_embedding_results.csv
```

Approved 08b work package:

```text
docs/superpowers/specs/2026-08-29-phase-8-08b-retrieval-fusion-benchmark-design.md
docs/superpowers/plans/2026-08-29-phase-8-08b-retrieval-fusion-benchmark-implementation-plan.md
notebooks/08b_retrieval_fusion_benchmark.ipynb
reports/phase_8_08b_retrieval_fusion_benchmark_codex_review.md
reports/user_reports/phase_8_08b_retrieval_fusion_benchmark_user_report.md
evaluation/results/phase8_sparse_manifest.json
evaluation/results/phase8_sparse_calibration.csv
evaluation/results/phase8_sparse_results.csv
evaluation/results/phase8_sparse_cases.jsonl
```

Approved 08c work package, confirmed by the user on `2026-08-30 +07`:

```text
docs/superpowers/specs/2026-08-30-phase-8-08c-reranker-benchmark-design.md
docs/superpowers/plans/2026-08-30-phase-8-08c-reranker-benchmark-implementation-plan.md
notebooks/08c_reranker_benchmark.ipynb
evaluation/results/phase8_reranker_results.csv
evaluation/results/phase8_reranker_cases.jsonl
reports/phase_8_08c_reranker_benchmark_codex_review.md
reports/user_reports/phase_8_08c_reranker_benchmark_user_report.md
```

Governance designs and plans:

```text
docs/superpowers/specs/2026-08-29-risk-gated-agent-review-design.md
docs/superpowers/plans/2026-08-29-risk-gated-agent-review-implementation-plan.md
docs/superpowers/specs/2026-08-29-restore-core-coding-behaviors-design.md
docs/superpowers/plans/2026-08-29-restore-core-coding-behaviors-implementation-plan.md
```

## Workstream và roadmap

**Dữ liệu:** curation `knowledge-base-hue` đã hoàn tất và được review. Đang
thiết kế chunking trước; user đã cung cấp ba paths reference Golden/evaluation,
đã review bản đầu với findings R1–R3 theo
`reports/full_corpus_golden_evaluation_reference_codex_review_2026_09_09.md`.
Correction lượt 2 đã đóng R1–R3. Khi đối chiếu câu hỏi user với canonical Foods
V3, Reviewer phát hiện R4 mới; Implementer đã sửa và Reviewer kiểm độc lập
correction lượt 3 PASS. R1–R4 đều đóng. User xác nhận ngày 2026-09-10; khảo sát
reference Golden/evaluation đã `approved/completed`.
Contract đọc reference:
`handoff_prompt/FULL_CORPUS_GOLDEN_EVALUATION_REFERENCE_HANDOFF.md`.
Thiết kế điều chỉnh embedding, indexing/ingestion, retrieval,
context/generation và evaluation — các phần đã làm từ Phase 2 đến Phase 7,
nhưng áp dụng cho toàn corpus. Spec/Plan/Review Contract đã được User duyệt;
Phase 2 đã qua ba correction, independent review và User closure ngày 2026-09-12.
Chưa có quyền
chạy benchmark, thay Golden, mutate index hoặc thực hiện phase/live gate sau.

Golden organization đã được user chốt theo giai đoạn và theo P7: biên soạn/review
`foods`, `heritages`, `festivals`, `performing_arts`, `travel_places`,
`travel_services`, `travel_tickets`, sau đó merge deterministic thành một
full-corpus JSONL canonical. Official evaluation chỉ dùng full file và smoke
deep-equal. Foods V3 lịch sử giữ nguyên, không bị sửa. Schema canonical đã chốt
bốn required fields (`question`, `keywords`, `reference_answer`, `category`);
không lưu `case_id`; `partition` chỉ ở authoring. Expected claims/evidence/source spans
đã bị loại khỏi official evaluation sau complexity reset.

Khảo sát sâu reference Golden schema từ `rag_old_0` đến Foods V3 đã qua ba lượt
correction và independent Reviewer review. R1–R5 đều đóng; User xác nhận ngày
2026-09-10 nên khảo sát là `approved/completed`. Report này là evidence thiết kế,
không tự chọn schema và không approve written spec/implementation plan. Decision
#1 lexical baseline/sparse consumer, #2 index lifecycle, #3 payload/source
locator, #4 retrieval/fusion/reranker matrix và #5 representation B timing đã
được User chốt; #6a strict minimal response/citation/error, #6b context budget
và #6c generator/provider + judge separation cũng đã chốt. #6d đã khóa exact
generator settings/numeric budgets và tách Agentic RAG sang profile/contract
riêng; #6e chốt UI inline citation/source cards. Phase 3 đã independent review
PASS và User-confirmed closure. Phase 4 design/spec/plan/Review Contract đã được
User duyệt; active Implementer handoff chỉ mở Tasks 1–6 và exact read-only
preflight. Dense full-corpus cùng Qdrant write vẫn đóng. Exact next action nằm
trong CURRENT_HANDOFF.

Simplicity survey `rag_old_0` đã qua hai correction, independent Reviewer review
và User confirmation. Các phiên sau tham khảo hai report survey/review trong
`reports/`; không đọc hay phân tích lại raw `rag_old_0` mặc định và không mở lại
findings đã đóng.

Initial survey toàn project `llm_rag` đã được Reviewer đọc đủ và focused-check
source. Các kết luận một configured collection dense+sparse, runtime dense-only,
BM25/CrossEncoder in-memory và Hue isolated candidates được giữ. Base matrix
3/6 collections không còn là hard cap sau Decision #2. Sau bốn
correction, report vẫn còn RR11 Major nên không được duyệt và đã bị đóng băng
working/non-canonical. Verified Architecture Extraction ngắn đã qua hai
correction, independent Reviewer review và User confirmation ngày 2026-09-11;
artifact là approved evidence companion, không mở lại survey dài.

Dự án đã hoàn tất bước Taxonomy Migration từ `knowledge-base-hue/tourism/`
sang `knowledge-base-hue/travel/` ngày 08/09/2026 với ba nhánh con rõ ràng:
- `travel/places/`: 35 file entity điểm đến + cẩm nang `travel_guides.md` (được đổi tên từ `tourism_guides.md`).
- `travel/services/`: 04 cẩm nang dịch vụ du lịch + 01 inventory.
- `travel/tickets/`: 05 cẩm nang vé du lịch + 01 inventory.
Thư mục cũ `tourism/` đã được dọn sạch hoàn toàn, cố định cấu trúc đường dẫn canonical
trước khi khởi chạy pipeline chunking cho toàn bộ corpus.

Trạng thái biên soạn dữ liệu theo domain tại ngày 08/09/2026:

- `foods`: 91 file Markdown curated, gồm guide và các entity thực phẩm; đây vẫn
  là corpus duy nhất đang được runtime ingestion sử dụng.
- `heritages`: đã hoàn tất 28 entity trong `heritages/heritage/` và
  `heritage-guides.md`.
- `festivals`: đã có 26 entity trong `festivals/festival/` và
  `festival-guides.md`.
- `performing_arts`: có 11 entity trong `performing_arts/arts/`,
  `performing_arts_guides.md` và một inventory; Phase 2 discovery hiện tính cả 13
  file theo approved scope.
- `travel/places`: 35 entity điểm đến và cẩm nang tổng quan `travel_guides.md` đã hoàn tất thẩm định.
- `travel/services`: 04 guide answer-facing và 01 inventory; inventory bị loại
  khỏi Phase 2 discovery.
- `travel/tickets`: 05 file answer-facing và 01 inventory; inventory bị loại
  khỏi Phase 2 discovery. Năm file answer-facing đã hoàn tất biên soạn, thẩm định độc
  lập 2 lượt (reports/tickets_codex_review_2026_09_08.md và
  reports/tickets_codex_rereview_2026_09_08.md), khắc phục 100% (06/06) findings,
  lập User Report và được người dùng chính thức phê duyệt nghiệm thu ngày 08/09/2026.
  Bao gồm 05 cẩm nang answer-facing, 01 danh mục thực thể kiểm soát (inventory) và
  hồ sơ kiểm chứng tại mục XLIV–XLVIII của evidence.

Giai đoạn biên soạn và chuẩn hóa dữ liệu (Data Curation) cùng bước Taxonomy Migration
của toàn bộ kho tri thức `knowledge-base-hue` (gồm 5 domain: `foods`, `heritages`,
`festivals`, `performing_arts`, `travel`) đã HOÀN TẤT 100%.

**Định hướng và lộ trình tiếp theo đã được người dùng xác nhận:**

1. **Thiết kế pipeline toàn corpus xuyên Phase 2–8:**
   Dùng `guides/full_corpus_rag.md` làm entrypoint; kế thừa behavior đã kiểm của
   Foods rồi chốt riêng chunking, embedding, ingestion/indexing, retrieval,
   generation/citation, API/frontend và evaluation cho năm domain. Guide Foods
   Phase 2 vẫn là contract lịch sử, không bị biến thành guide đa domain.

2. **Thiết kế một Golden Dataset toàn corpus:**
   Biên soạn và review qua P7 (`foods`, `heritages`, `festivals`,
   `performing_arts`, `travel_places`, `travel_services`, `travel_tickets`), rồi
   merge deterministic thành một file JSONL canonical cho official evaluation.
   Foods V3 giữ nguyên; các case phù hợp được copy, reclassify và review theo
   schema metric-only mới.

3. **Chuỗi duyệt tài liệu:**
   Các khảo sát trước survey toàn project `llm_rag` đã đóng. Survey dài đã chạm
   correction ceiling và được thay bằng Verified Architecture Extraction theo
   complexity reset User xác nhận. Extraction đã qua hai correction, Reviewer
   review và User closure. Decision Queue đã hoàn tất; Written Spec, Plan và
   Review Contract đã được duyệt. Phase 2 và Phase 3 đã User-closed; Phase 4
   package riêng đã được duyệt và active handoff mở Tasks 1–6/read-only
   preflight, chưa mở dense full-corpus hoặc Qdrant write. Các phase và live gate
   sau tiếp tục cần đúng closure/approval trong Plan. Hai working notes ngày
   2026-09-09 không phải các artifact đã
   duyệt này.

Chi tiết tiến độ và các artifact nghiệm thu nằm tại:

- `knowledge-base-hue/travel/services/services-research-and-entities-inventory.md`;
- `knowledge-base-hue/travel/tickets/tickets-research-and-entities-inventory.md`;
- `knowledge-base-hue/meta/tourism-research-evidence.md`;
- `reports/tourism_guides_implementation_report_2026_09_07.md`;
- `reports/services_batches_01_03_minimal_reset_implementation_report_2026_09_08.md`;
- `reports/tickets_codex_review_2026_09_08.md`;
- `reports/tickets_codex_rereview_2026_09_08.md`;
- `session_prompt/CURRENT_HANDOFF.md`.
