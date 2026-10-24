# Project History

Lịch sử dự án `hue_rag`, mục mới ở trên cùng. Chỉ thêm, không sửa mục cũ.
Hiện trạng nằm ở `Project_Status.md`; file này là tra cứu (`reference-only`),
không cấp quyền và không tạo việc phải làm.

## 2026-10-24 — Governance v2 và Phase 7A2 Gate 1–2

- Governance v2 được User duyệt
  (`docs/superpowers/specs/2026-10-24-governance-v2-design.md`): A điều phối +
  review chéo B/C (cả ba Opus 5.5), quy trình theo rủi ro, gộp spec + plan, file
  STATUS riêng mỗi session, `PROJECT_HISTORY.md` (file này), skill
  `propose-options`; bỏ `karpathy-guidelines`. Lịch sử trước đây nằm trong
  `Project_Status.md` được chuyển nguyên văn xuống mục "Bản chụp" bên dưới.
- Phase 7A2 Gate 1 (sửa 25 mục corpus) User-closed; m1 đồng bộ Golden authoring.
  Review `reports/phase_7a2_gate_1_review_2026_10_23.md`. Commit `5e8aff1`.
- Phase 7A2 Gate 2 User-closed với giới hạn: index
  `hue_full_corpus_7a2_e5_small_384` + cutover runtime; index 8B hoãn sang Phase 8
  (build không pin trộn 3 provider, cos 0,9954; build pin Nebius lỗi 504). Review
  `reports/phase_7a2_gate_2_review_2026_10_24.md`. Commit `b781af8`.
- User quyết: giữ hai collection Foods qua Phase 7; Phase 8 là đợt ổn định trước
  Phase 9 (chunk, reranker, bảng giá F2, đa nguồn F1, BM25 tiếng Việt, rà lại các
  Phase trước).
- Gate 3 (xóa 13 collection cũ) đang làm: 13 collection đã xóa; 9 file build
  record cũ chờ User chạy lệnh xóa trong terminal B.

---

## Bản chụp `Project_Status.md` trước Governance v2 (nguyên văn, 2026-10-24)

## Project Status

Last updated: `2026-10-24 +07`

### Project overview

`hue_rag` xây dựng hệ thống RAG về văn hóa và du lịch Huế. Baseline đã có là
Hue Foods RAG MVP. Curation/taxonomy toàn corpus đã hoàn tất. Full-corpus Phase
2–6 và Phase 7A (Golden) đã User-closed; dự án đang làm **Phase 7A2 — Sửa corpus
+ tạo lại index** (Gate 1 và Gate 2 User-closed 2026-10-24; Gate 3 đang implement). Hybrid Recommender
và Agentic RAG là roadmap, chưa có implementation scope.

Project ưu tiên code/data flow dễ hiểu, complexity tương xứng nhu cầu và bằng
chứng từ dữ liệu, database, model cùng API thật.

### Current active handoff snapshot

**Phase 7A2 — Sửa corpus + tạo lại index (cập nhật 2026-10-24, phiên Reviewer
Claude):** brainstorming xong; Written Spec
`docs/superpowers/specs/2026-10-23-phase-7a2-corpus-correction-reindex-design.md`
và Implementation Plan + Review Contract
`docs/superpowers/plans/2026-10-23-phase-7a2-corpus-correction-reindex-implementation-plan.md`
được User duyệt cùng ngày. Ba gate tuần tự, mỗi gate cần User closure:

- **Gate 1 — sửa corpus:** User xác nhận đóng 2026-10-24 (m1 đồng bộ dòng
  authoring giao Implementer làm cơ học). 25 mục (21 nhóm A + 4 nhóm B) trong 27
  file; backup private `knowledge-base-hue/meta/backup_7a2_2026_10_23/`; Golden
  chỉ sửa `reference_answer` dòng 139 (K44). Reviewer review độc lập
  `reports/phase_7a2_gate_1_review_2026_10_23.md`: `ready_for_user_confirmation`,
  một minor m1 (đồng bộ dòng authoring). Fresh: Golden `check` 176/10 exit 0;
  chunker 205 file, **8.459 chunk** (trước 8.460), 0 error.
- **Gate 2 — build index + cutover runtime:** User-closed 2026-10-24 **với giới
  hạn**: `hue_full_corpus_7a2_e5_small_384` (8.459 point) build/verify đạt,
  runtime cutover, health 200, live smoke 4/5 như Phase 6. Index 8B **hoãn sang
  Phase 8** (build 1 không pin trộn 3 provider, cos 0,9954; build 2 pin Nebius lỗi
  504). Review `reports/phase_7a2_gate_2_review_2026_10_24.md`. `e5-small-384` local và
  `qwen/qwen3-embedding-8b` qua OpenRouter (survey thật
  `reports/phase_7a2_openrouter_embedding_survey_2026_10_23.md`: 4096 chiều, đã
  normalize, batch 64/128 OK, ~92 token/chunk, một query ~10 s).
- **Gate 3 — xóa 13 collection cũ + build record cũ:** handoff giao B 2026-10-24.

Hệ quả hiện tại: corpus đã sửa nên mọi collection full-corpus cũ (4 legacy + 4
metadata-v2) đều **stale**; runtime full-corpus (API Phase 6) sẽ từ chối khởi
động vì freshness — đã hết từ Gate 2 (runtime dùng index e5 7a2). API (`backend/api/app.py`)
chỉ phục vụ full-corpus; collection Foods `hue_foods_e5_small_384` (còn "An
Đông" ở 5 quán AEON, K11) không đứng sau API nào, chỉ còn được settings/tests/
benchmark Foods cũ tham chiếu. Dữ liệu foods đã sửa được embed lại trong index
e5 7a2. **User 2026-10-24:** giữ hai collection Foods qua Phase 7; sau Phase 7
Reviewer đề xuất xóa mọi collection không còn dùng. Reviewer được commit/push
(User 2026-10-24); Implementer Git `none`. Việc hiện hành trong `CURRENT_HANDOFF.md`.

Lịch sử các phase đã đóng (giữ để tra cứu; trạng thái hiện hành ở trên):

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

Reviewer đã hoàn tất independent final review Phase 4 Tasks 1–8 ngày
2026-09-13 với verdict `PASS WITH LIMITATIONS`; User xác nhận closure cùng ngày.
Fresh read-only Notebook 04 xác minh trên cả bốn
exact targets: schema đúng, 8.460 points, 8.460 exact ID/payloads và 12 sampled
dense+sparse vectors; bốn final records cùng corpus/source/sparse identity.
Final review:
`reports/full_corpus_phase_4_final_codex_review_2026_09_13.md`.

Hai minor không chặn của Phase 4 là cleanup fixture dư và lỗi documentation
trong Qwen auxiliary report. Report phụ đã được sửa sau closure; fresh audit
quét đủ 8.460 Qwen points và không tìm thấy ID/payload/dense/sparse anomaly; 12
mẫu tái encode bằng exact Qwen revision khớp stored vectors với minimum cosine
`0.99987924`.

User đã hoàn tất brainstorming và duyệt Full-corpus Phase 5 Written Spec,
Implementation Plan cùng Review Contract ngày 2026-09-13. Correction 3 đã đóng
typed fail-closed behavior cuối cùng cho nested `evidence_parts`; independent
focused suite đạt `23 passed, 1 warning`, direct malformed-role probe đạt và
selected live evidence đủ điều kiện reuse đạt `8/8 PASS`. Technical verdict
ngày 2026-09-14 là `ready_for_user_confirmation`; User đã xác nhận closure cùng
ngày và Phase 5 hiện `approved`. Remote-Qwen GPU research và
`Qwen/Qwen3-Reranker-0.6B` đều deferred, không thuộc active implementation.

Full-corpus Phase 6 brainstorming đã hoàn tất ngày 2026-09-14; Written Spec,
Implementation Plan và Review Contract đã được User duyệt. Ngày 2026-09-29,
trước khi implementation bắt đầu, User yêu cầu dừng Phase 6 để đánh giá lại
metadata xuyên Phase 2/4/5/6. Package Phase 6 được giữ làm lịch sử đã duyệt nhưng
không còn authority thực thi. Metadata v2 Written Spec, Implementation Plan và
Review Contract đã được User duyệt ngày 2026-09-29. Gate 1 đã đóng sau
correction 3. Gate 2 / Task 5 đã tạo và independent-verify bốn metadata-v2
targets, mỗi target 8.460 points, rồi được User xác nhận closure cùng ngày. User
đã mở riêng Gate 3 / Task 6 cho strict runtime retrieval cutover, focused tests
và selected read-only retrieval smoke. Sau Correction 1, independent review đạt
và User xác nhận closure ngày 2026-09-30. Task 7 final regression/report/handoff
sau đó qua independent final review với `158 passed`, complete verification đủ
33.840 points và được User xác nhận closure cùng ngày. Metadata v2 Tasks 1–7
hiện `approved`. Phase 6 Qwen scope được duyệt ngày 2026-09-30 nhưng bị
supersede trước implementation. Ngày 2026-10-01, User duyệt OpenAI baseline
amendment, revised Implementation Plan, separate Review Contract và exact GPT
Implementer handoff. Implementer hoàn tất Tasks 1–6 với non-paid suite đạt và
five-call artifact `3 PASS / 2 FAIL`; independent review ngày 2026-10-01 có
verdict `CHANGES REQUESTED` do production startup blocker cùng runner/evidence
deviations. Sau bốn correction batches, independent Correction 4 review đạt
`READY FOR USER CONFIRMATION`: fresh suite `141 passed, 1 warning`, Metadata v2
`VERIFIED` đủ 33.840 points, exact production health PASS và không còn open
non-paid finding. User đã cấp authority ngày 2026-10-01 cho đúng một bounded
replacement invocation tối đa 5 attempted calls, nhưng yêu cầu hoãn execution
đến phiên tiếp theo (authority này sau đó bị thay bởi `gpt-6-luna`, xem dưới).

**Cập nhật 2026-10-23:** sau ba tuần tạm dừng, User quyết định đổi toàn bộ model
OpenAI (Phase 6 generation, Foods answer, evaluation answer/judge) sang
`gpt-6-luna` và đổi host port Qdrant hue sang `127.0.0.1:6335/6336` để chạy song
song `mekongai-template`. Paid authority `gpt-5.4-nano` ngày 2026-10-01 chưa bị
tiêu thụ (0 calls) và đã bị thay. Cả Reviewer và Implementer hiện là Claude Opus
5.5; quy trình giữ nguyên. Delta tại
`docs/superpowers/specs/2026-10-23-phase-6-gpt-6-luna-amendment.md`.

User xác nhận closure Phase 6 ngày 2026-10-23 (Option A, PASS WITH
LIMITATIONS): live run 5 calls `gpt-6-luna`, 4 PASS / 1 FAIL. `conditional_evidence`
FAIL do retrieval không đưa chunk bảng giá vé lẻ vào top-30 (root cause đã chứng
minh, chuyển Phase 8). Synthesis đa nguồn chưa được chứng minh (đo ở Phase 7).
Review: `reports/full_corpus_phase_6_gpt_6_luna_review_2026_10_23.md`. Phase 7A đã
brainstorming với User ngày 2026-10-23 (tham khảo `rag_old_0` + phiên âm bài học, survey
`reports/phase_7a_golden_reference_rag_old_0_survey_2026_10_23.md`). Spec
`docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md` và plan
`docs/superpowers/plans/2026-10-23-phase-7a-golden-full-corpus-implementation-plan.md`
được User duyệt; chúng supersede các bullet Golden thời Codex bên dưới (category,
quota, review, thứ tự P7, shuffle, keyword rule, Foods V3 copy). Phase 7A đã
User-closed 2026-10-23: Golden 176 case + smoke 10, private tại
`knowledge-base-hue/evaluation/` (review `reports/phase_7a_golden_review_2026_10_23.md`).

### System and data map

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

### Current runtime and data

Production baseline hiện dùng:

- local embedding `intfloat/multilingual-e5-small`, 384 dimensions;
- active Qdrant collection `hue_foods_e5_small_384`, 572 points;
- profiles `dense_only`, `hybrid_no_rerank`, `hybrid_rerank`;
- Python BM25 và concrete local MiniLM cross-encoder reranker;
- bounded whole-chunk context;
- grounded generation bằng `gpt-6-luna` (đổi 2026-10-23; trước là `gpt-5.4-nano`);
- answer-only JSON API và startup warm-up.

Full-corpus runtime (API Phase 6): candidate `e5-small-384`, collection
`hue_full_corpus_7a2_e5_small_384` (cutover Gate 2 Phase 7A2, 2026-10-24),
profile `dense_bm25_rrf`, reranker `none`, generation `gpt-6-luna`.

Foods active collection còn legacy sparse vector state từ các phase trước nhưng là
read-only trong implementation/review thông thường. Dense-only candidate
`hue_foods_e5_small_384_dense` tồn tại làm blue-green evidence; production chưa
cutover.

Notebooks 08a/08b/08c đã có evidence benchmark trên Foods; kết quả và artifact
chi tiết nằm trong canonical map phía dưới. Evidence này không chứng minh chất
lượng trên toàn bộ dữ liệu đang bổ sung. Baseline trên được giữ từ trạng thái
đã ghi nhận, không được chạy lại ngoài exact approved gate.

### Thiết kế full-corpus hiện hành

Khảo sát parser/source locator đã được user **approved** sau correction lượt 3
ngày 2026-09-09; closure tại
`reports/full_corpus_parser_locator_codex_review_2026_09_09.md`, mục 9–10.
Chọn markdown-it-py 4.2.0/table enabled cho thiết kế locator trên source LF.
Đây là evidence mẫu, chưa là runtime full-corpus approved. Hai composites VN/QT
đã sửa ranh giới; counts input sai không dùng làm PASS.

Full-corpus đã có Written Spec, Implementation Plan và Review Contract umbrella
được User duyệt ngày 2026-09-11. Phase 2 discovery/parser/chunker/locator/
Representation A preview đã được User xác nhận closure ngày 2026-09-12. Phase 5
đã được User xác nhận closure ngày 2026-09-14. Phase 6 package đã bị pause trước
implementation ngày 2026-09-29 để mở lại thiết kế metadata. Guide umbrella hiện hành là
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
Decision #3 lịch sử chốt payload 5 fields cho bốn legacy collections. Metadata
v2 amendment ngày 2026-09-29 supersede target tương lai bằng exact seven-field
payload: năm field cũ cộng `chunk_id` và five-value `domain`; build/payload
schema version cùng vector-copy lineage ở build level. Decision #4 chốt staged
retrieval/fusion/reranker matrix,
đo bằng metrics hiện hành và báo kết quả thực nghiệm. Decision #5 chốt
representation B theo staged finalists với API/index/full-corpus runs thật.
Decision #6a chốt strict minimal public response/citation/error contract;
#6b chốt budget linh hoạt theo generator profile nhưng cố định trong từng run.
#6c/#6d Qwen/OpenRouter là lịch sử bị supersede ngày 2026-10-01: Phase 6 dùng
alias `gpt-5.4-nano` qua tool-less OpenAI Agents SDK, không pin snapshot và
không cấu hình/truyền reasoning hoặc sampling parameters; `o200k_base`, answer/B caps 2048/256,
context 16384/2048/512, timeout 45, client retries 0 và Runner max turns 1.
`gpt-5.4-mini` từng là evaluation judge (từ 2026-10-23 mọi model, kể cả judge, là `gpt-6-luna`); Qwen là mandatory Phase 8
candidate, không fallback. #6e giữ static UI inline citation/source cards. Decision
Queue tiền-spec đã hoàn tất; Written Spec đã được User duyệt ngày 2026-09-11.
Implementation Plan + Review Contract đã được User duyệt ngày 2026-09-11;
Phase 3 guide, Written Spec, Implementation Plan và Review Contract đã được User
duyệt ngày 2026-09-12; implementation qua hai correction đã independent review
PASS và được User xác nhận closure cùng ngày. Phase 4 design/spec/plan/Review
Contract đã được User duyệt; latest read-only state cho thấy bốn full-corpus
targets và final records đã tồn tại sau live sequence. Independent final review
đã đạt `PASS WITH LIMITATIONS` và User đã xác nhận closure. Remote GPU research
được queue nhưng chưa được kích hoạt. Phase 5 design, Written Spec,
Implementation Plan và Review Contract đã được User duyệt ngày 2026-09-13;
implementation qua ba correction đã independent review đạt và được User xác
nhận closure ngày 2026-09-14.
Phase 6 Written Spec và Implementation Plan kèm Review Contract đã được hoàn
tất ngày 2026-09-14 nhưng User dừng trước implementation ngày 2026-09-29 để
đánh giá lại metadata. Package Qwen ngày 2026-09-30 giữ Metadata v2/API/UI
behavior nhưng bị supersede trước implementation. OpenAI baseline amendment,
revised plan và Review Contract ngày 2026-10-01 giữ các behavior đó và thay
generation/tokenizer/provider contract.
Metadata v2 design package đã được User duyệt ngày 2026-09-29. Gate 1 và Gate 2
đã User-closed; bốn metadata-v2 targets đã independent-verify đủ 33.840 points,
payload/vector equality, lineage và legacy immutability. Gate 3 / Task 6 qua một
correction, independent review và được User xác nhận closure ngày 2026-09-30.
Task 7 final review cũng được User xác nhận closure cùng ngày; toàn workstream
Metadata v2 Tasks 1–7 đã đóng. Phase 6 paid execution handoff ngày
2026-10-01 (lịch sử): Correction 4 đã independent review đạt;
User đã cấp quyền riêng cho đúng một replacement five-call invocation và hoãn
thực thi sang phiên tiếp theo; authority đó đã bị thay bởi `gpt-6-luna` và Phase 6
đã User-closed ngày 2026-10-23.
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

### Phase status

| Phase | Status | Current result / next boundary |
|---:|---|---|
| 0 | `approved` | MVP foundation và simplicity governance |
| 1 | `approved` | Backend foundation |
| 2 | `approved` | Foods Markdown chunking |
| 3 | `approved` | Full-corpus embedding/sparse preflight User-closed; Qwen CUDA FP16 PASS trên GTX 1650 |
| 4 | `approved` | User-closed 2026-09-13 với final review PASS WITH LIMITATIONS |
| 5 | `approved` | User-closed 2026-09-14 sau Correction 3 final review |
| 6 | `approved` | User-closed 2026-10-23, PASS WITH LIMITATIONS trên `gpt-6-luna` (4/5 live calls); limitation: retrieval miss bảng giá (F2), synthesis chưa chứng minh (F1) |
| 7 | `approved` | Retrieval/answer evaluation baseline |
| 7A | `approved` | User-closed 2026-10-23: Golden 176 case + smoke 10 (private), review `reports/phase_7a_golden_review_2026_10_23.md` |
| 7A2 | `in_progress` | Sửa corpus + tạo lại index. Gate 1 và Gate 2 User-closed 2026-10-24 (Gate 2 với giới hạn: chỉ index e5, 8B hoãn sang Phase 8); Gate 3 (xóa 13 collection) đang implement |
| 7B | `not_ready` | Evaluator full-corpus; chờ Phase 7A2 đóng |
| 8 | `not_ready` | Foods Notebooks 08a/08b/08c approved (lịch sử). Candidate full-corpus đã đổi thành e5-small + qwen3-embedding-8b (Phase 7A2) nên spec/plan Phase 8 phải thiết kế lại; remote-Qwen research và Qwen3-Reranker vẫn deferred |
| 9 | `not_ready` | Agentic RAG roadmap chưa có approved scope |

Git và canonical artifacts giữ lifecycle history; file này chỉ mô tả trạng thái
đang có hiệu lực.

### Decisions currently in force

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
- **Phase 7A2 (User 2026-10-23) supersede matrix 4 candidate bên dưới:** dense
  full-corpus chỉ còn `e5-small-384` (local) và `qwen/qwen3-embedding-8b`
  (OpenRouter, 4096 chiều, batch 64, **pin Nebius** từ 2026-10-24 — build không
  pin đầu tiên trộn 3 provider, cos mẫu 0,9954 —, mọi request gửi
  `provider.data_collection: "deny"`, không retry/fallback/resume). Bỏ e5-base,
  huydang, qwen-0.6B. Build thẳng schema metadata v2 vào
  `hue_full_corpus_7a2_e5_small_384` và `hue_full_corpus_7a2_qwen3_8b_4096`;
  build record là nguồn sự thật duy nhất, bỏ hằng số cứng corpus identity/chunk
  count/sparse SHA/vocab và preflight Phase 4. Chunker giữ nguyên, kể cả
  `full_corpus.embedding_models` (tokenizer e5-small/e5-base/huydang quyết định
  ranh giới chunk). Runtime mặc định e5-small; cutover sang 8B chờ bằng chứng
  7B/8. Chi tiết trong spec/plan 7A2.
- (Lịch sử, bị Phase 7A2 supersede) Full-corpus benchmark dùng isolated Qdrant collection theo dense embedding
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
  và approval riêng; Foods read-only. Metadata-v2 schema/names đã được khóa;
  benchmark winner, cutover và mọi cleanup vẫn chưa được chốt.
- Metadata v2 có exact payload bảy field: `search_text`, `source`, `title`,
  `heading_path`, `evidence_parts`, `chunk_id`, `domain`. Domain canonical là
  first source component trong năm product domains; không có subdomain,
  document type hoặc tags. Không payload index/filter/router trong baseline.
  Bốn target names, build/payload schema versions và vector-copy migration được
  khóa trong approved metadata v2 Plan. Tasks 1–7 đã independent review và
  User-closed; cleanup vẫn cần lifecycle/authority riêng.
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
  `Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7A Golden → Phase 7A2 Sửa corpus + reindex → Phase 7B Evaluator → Phase 8 Benchmark → integrated closure`.
  Mỗi phase phải có guide + spec + plan + Review Contract và User duyệt trước
  implementation; phase trước phải independent review và User closure trước.
- Correction 2 đã loại khỏi acceptance việc chạy toàn bộ `backend/tests` và
  `test_ingestion_pipeline.py`, vì các suite đó gọi real embedder/Qdrant và mâu
  thuẫn hard boundary offline của Phase 2. Chỉ chạy exact offline checks ghi trong
  Correction 2; không dùng full-suite failure làm Phase 2 evidence.
- Phase 6 đã User-closed 2026-10-23 (4/5 live calls `gpt-6-luna`). Replacement/
  cleanup collection chỉ theo Phase 7A2 Gate 3 đã duyệt; Git và Agentic RAG vẫn
  cần exact approval riêng.
- Corpus `knowledge-base-hue/` không có Git (`.gitignore`). Mọi đợt sửa corpus
  phải backup file gốc vào `knowledge-base-hue/meta/` (thư mục bị discovery loại
  trừ) và review bằng diff với backup.
- User ưu tiên lựa chọn mặc định, đơn giản (ví dụ không pin provider
  OpenRouter); Reviewer không thêm cấu hình/cơ chế khi User chưa cần.
- **Phase 8 (User 2026-10-24) là đợt ổn định trước Phase 9:** sau baseline 7B
  (176 case, chunker hiện hành giữ nguyên), thử nghiệm chunk size/gộp chunk vụn,
  reranker đa ngôn ngữ, truy xuất bảng giá (F2), tổng hợp đa nguồn (F1), BM25
  tiếng Việt (tách từ/bigram) và rà lại lựa chọn của các phase trước; spec/plan
  Phase 8 phải thiết kế lại.
- **Điều phối (User 2026-10-24):** A = Reviewer/điều phối (User chỉ làm việc với
  A), B = Implementer, C = session thứ ba; cả ba dùng Opus. Đồng ý hướng
  Governance v2: quy trình theo rủi ro, gộp spec+plan, review chéo, file ngữ
  cảnh riêng từng session, skill `propose-options`, lịch sử sang
  `PROJECT_HISTORY.md`; chi tiết chờ tài liệu Governance v2.

### Safety and authorization boundaries

- Active `hue_foods_e5_small_384` chỉ read-only nếu không có exact user approval.
- Bốn canonical Full-corpus Phase 4 collections và bốn metadata-v2 targets là
  immutable/read-only (và stale từ Gate 1 Phase 7A2). Chỉ được xóa ở Phase 7A2
  Gate 3, đúng 13 tên trong spec §6.1, Gate 2 đã User-closed 2026-10-24; handoff
  Gate 3 cấp xóa đúng 13 tên đó.
- Data egress: User cho phép gửi chunk corpus và query tới OpenRouter cho
  `qwen/qwen3-embedding-8b` trong Phase 7A2 Gate 2 (spec §2, §5.6).
- `knowledge-base-hue/`, Qdrant storage, fixed smoke questions và detailed trace
  là local/private; tracked artifacts không được chứa corpus/query/payload dump.
- Không expose secret hoặc đọc raw `.env` content.
- Không dùng fake provider/data/artifact hoặc old output làm fresh PASS evidence.
- Provider/model/dataset mới, paid run ngoài approved guide, deploy, active
  mutation, destructive cleanup và production cutover cần authority mới.
- Commit/push chỉ thực hiện khi latest user instruction hoặc current handoff ghi
  exact Git authorization.
- Implementer không tự approve; Reviewer không sửa runtime thay Implementer.

### Canonical document map

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
docs/superpowers/specs/2026-09-29-full-corpus-metadata-v2-written-spec.md
docs/superpowers/plans/2026-09-29-full-corpus-metadata-v2-implementation-plan.md
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

Full-corpus Phase 4 closure và Qwen post-closure integrity evidence:

```text
reports/full_corpus_phase_4_qdrant_ingestion_implementation_2026_09_12.md
reports/full_corpus_phase_4_final_codex_review_2026_09_13.md
reports/full_corpus_phase_4_qwen_post_closure_audit_2026_09_13.md
reports/qwen3_gtx1650_embedding_execution_report_2026_09_13.md
reports/qwen3_remote_gpu_offloading_research_context_2026_09_13.md  # deferred, not approved
```

Completed Full-corpus Phase 5 package:

```text
guides/phase_5_retrieval_profiles_reranking.md
docs/superpowers/specs/2026-09-13-phase-5-full-corpus-retrieval-reranking-written-spec.md
docs/superpowers/plans/2026-09-13-phase-5-full-corpus-retrieval-reranking-implementation-plan.md
reports/full_corpus_phase_5_retrieval_reranking_codex_review_2026_09_13.md
reports/user_reports/full_corpus_phase_5_retrieval_reranking_user_report_2026_09_14.md
```

Active Phase 7A2 package (sửa corpus + tạo lại index):

```text
docs/superpowers/specs/2026-10-23-phase-7a2-corpus-correction-reindex-design.md
docs/superpowers/plans/2026-10-23-phase-7a2-corpus-correction-reindex-implementation-plan.md
reports/phase_7a2_openrouter_embedding_survey_2026_10_23.md
reports/phase_7a2_gate_1_corpus_correction_implementation_2026_10_23.md
reports/phase_7a2_gate_1_review_2026_10_23.md
gửi chatgpt/kết quả nghiên cứu/TONG_HOP_REVIEWER_2026_10_23.md  # private input, untracked
```

Completed Phase 7A Golden package:

```text
docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md
docs/superpowers/plans/2026-10-23-phase-7a-golden-full-corpus-implementation-plan.md
reports/phase_7a_golden_review_2026_10_23.md
```

Completed Full-corpus Phase 6 package (User-closed 2026-10-23):

```text
guides/phase_6_generation_api.md
docs/superpowers/specs/2026-10-01-phase-6-openai-baseline-amendment.md
docs/superpowers/plans/2026-10-01-phase-6-openai-baseline-implementation-plan.md
handoff_prompt/PHASE_6_OPENAI_BASELINE_REVIEW_CONTRACT.md
```

Historical Phase 6 packages retained for approved behavior/base contract
referenced by the active delta:

```text
docs/superpowers/specs/2026-09-14-phase-6-full-corpus-generation-api-ui-written-spec.md
docs/superpowers/plans/2026-09-14-phase-6-full-corpus-generation-api-ui-implementation-plan.md
docs/superpowers/specs/2026-09-30-phase-6-full-corpus-generation-api-ui-amendment.md
docs/superpowers/plans/2026-09-30-phase-6-full-corpus-generation-api-ui-metadata-v2-implementation-plan.md
```

Completed Full-corpus Metadata v2 Tasks 1–7 package:

```text
docs/superpowers/specs/2026-09-29-full-corpus-metadata-v2-written-spec.md
docs/superpowers/plans/2026-09-29-full-corpus-metadata-v2-implementation-plan.md
reports/full_corpus_metadata_v2_final_codex_review_2026_09_29.md
reports/user_reports/full_corpus_metadata_v2_final_user_report_2026_09_30.md
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

### Workstream và roadmap

**Dữ liệu:** curation `knowledge-base-hue` đã hoàn tất và được review; Phase 7A2
Gate 1 (2026-10-23) đã sửa 25 mục mâu thuẫn có căn cứ (danh sách trong file tổng
hợp private). Các mâu thuẫn còn lại ngoài phạm vi ghi trong
`reports/phase_7a2_gate_1_review_2026_10_23.md` §2 và 28 mục nhóm C chưa đủ căn
cứ. (Lịch sử:) user đã cung cấp ba paths reference Golden/evaluation,
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
được User chốt; #6a strict minimal response/citation/error và #6b context budget
vẫn áp dụng. #6c/#6d Qwen/OpenRouter là lịch sử; OpenAI baseline revision ngày
2026-10-01 khóa GPT alias, Agents SDK, `o200k_base`, model/SDK-default reasoning
và sampling, no retry/fallback cùng bounded five-call runner. #6e giữ
static UI inline citation/source cards. Phase 3 đã independent review
PASS và User-confirmed closure. Phase 4 design/spec/plan/Review Contract đã được
User duyệt; latest read-only state cho thấy cả bốn target và final records đã
tồn tại; independent final review đã đạt `PASS WITH LIMITATIONS` và User đã xác
nhận closure. Remote GPU research vẫn queued, chưa có active authority. Exact
state nằm trong CURRENT_HANDOFF.

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
   independent final review đã đạt `PASS WITH LIMITATIONS` trên cả bốn target
   và được User xác nhận closure ngày 2026-09-13. Phase 5 implementation qua ba
   correction đã independent review đạt và được User xác nhận closure ngày
   2026-09-14. Phase 6 bị pause trước implementation ngày 2026-09-29; sau khi
   Metadata v2 Tasks 1–7 được independent review và User-closed, Qwen package
   ngày 2026-09-30 được duyệt rồi supersede trước execution. User đã duyệt
   OpenAI baseline amendment/revised plan/Review Contract và mở exact GPT
   implementation handoff ngày 2026-10-01. Gate 3 runtime cutover đóng sau
   Correction 1.
   Future Qwen remote-GPU
   research và Qwen3-Reranker vẫn chưa active; mọi cloud, external corpus
   upload, benchmark chất lượng và production cutover cần approval riêng. Các
   phase/live gate sau tiếp tục cần đúng closure/approval trong Plan. Hai working
   notes ngày 2026-09-09 không phải các artifact đã duyệt này.

Chi tiết tiến độ và các artifact nghiệm thu nằm tại:

- `knowledge-base-hue/travel/services/services-research-and-entities-inventory.md`;
- `knowledge-base-hue/travel/tickets/tickets-research-and-entities-inventory.md`;
- `knowledge-base-hue/meta/tourism-research-evidence.md`;
- `reports/tourism_guides_implementation_report_2026_09_07.md`;
- `reports/services_batches_01_03_minimal_reset_implementation_report_2026_09_08.md`;
- `reports/tickets_codex_review_2026_09_08.md`;
- `reports/tickets_codex_rereview_2026_09_08.md`;
- `session_prompt/CURRENT_HANDOFF.md`.
