# Hue RAG Project Document Registry và Audit Contract

```text
Status: audit_in_progress
Owner: Reviewer
Approved location: repository root
Audit scope: reports/**/*.md và handoff_prompt/**/*.md
Observed inventory on 2026-09-12: 152 + 28 = 180 Markdown files
Repository mutation by audit workers: none
Final retention/deletion authority: User
```

## 1. Mục đích

File này là điểm vào duy nhất cho đợt audit tài liệu và sau đó trở thành registry
hợp nhất của các Markdown quan trọng trong dự án. Nó giải quyết bốn câu hỏi:

1. File quan trọng nào tồn tại và chủ đề của nó là gì?
2. Vai trò, authority và thời điểm cần đọc của file là gì?
3. File cần hiện tại, cần cho tương lai, chỉ cần audit history hay đã bị thay thế?
4. Nếu đề xuất xóa, canonical replacement và bằng chứng không còn consumer là gì?

Trong thời gian audit, các directory README chỉ làm entrypoint ngắn:

- `reports/README.md` định tuyến evidence;
- `handoff_prompt/README.md` định tuyến prompt/context;
- `session_prompt/CURRENT_HANDOFF.md` vẫn là nguồn task/authority hiện hành.

Audit worker không sửa file registry này. Reviewer hợp nhất kết quả sau khi User
gửi lại các batch report.

## 2. Taxonomy retention

Mỗi file được gán đúng một retention class chính:

| Class | Ý nghĩa | Xử lý mặc định |
|---|---|---|
| `ACTIVE_CONTROL` | Điều khiển task, role, authority hoặc trạng thái hiện tại | Giữ, full-read khi bootstrap phù hợp |
| `CANONICAL_CONTRACT` | Guide/spec/plan/contract đã duyệt, khóa behavior hoặc acceptance | Giữ lâu dài |
| `CANONICAL_EVIDENCE` | Final result, independent review hoặc User closure cần để tin kết quả | Giữ lâu dài |
| `FUTURE_REFERENCE` | Chưa cần hiện tại nhưng có consumer/Phase tương lai cụ thể | Giữ, reference-only đến khi consumer active |
| `HISTORICAL_AUDIT` | Có nội dung unique cần khi truy vết quyết định/finding | Giữ có chọn lọc, không đọc mặc định |
| `SUPERSEDED` | Đã có exact source mới thay thế, không còn authority hiện hành | Không dùng; đánh giá xóa |
| `DELETE_CANDIDATE` | Không còn nội dung unique/consumer hoặc chỉ lặp nguồn tốt hơn | Chờ Reviewer kiểm và User duyệt exact path |
| `REVIEW_PENDING` | Bằng chứng chưa đủ hoặc quan hệ thay thế chưa rõ | Giữ tạm thời |

Retention class khác document type. Ví dụ một `IMPLEMENTATION_REPORT` có thể là
`CANONICAL_EVIDENCE`, `HISTORICAL_AUDIT` hoặc `DELETE_CANDIDATE` tùy chain và
final review; chữ “final”, “approved” hay “correction” trong tên không tự quyết
định class.

## 3. Trường bắt buộc cho mỗi file

Mỗi batch report phải có một dòng cho từng file đã audit với các trường:

| Field | Nội dung bắt buộc |
|---|---|
| `path` | Exact repository-relative path |
| `git_state` | `tracked` hoặc `untracked` |
| `document_type` | Prompt, implementation report, Codex review, user report, survey, context, index hoặc loại khác |
| `topic_chain` | Chủ đề và correction chain sở hữu file |
| `role_summary` | 1–3 câu: file làm gì, không làm gì |
| `authority` | Có/không khóa requirement, implementation, review hoặc User closure |
| `current_use` | Ai dùng hiện tại và khi nào |
| `future_use` | Exact Phase/consumer tương lai; không ghi “có thể hữu ích” chung chung |
| `unique_content` | Nội dung/evidence nào không có ở nguồn khác |
| `canonical_replacement` | Exact path thay thế, hoặc `none` với lý do |
| `inbound_references` | Exact active paths/link quan trọng; phân biệt historical reference |
| `retention_class` | Một class trong §2 |
| `recommendation` | `KEEP`, `DELETE`, `MERGE_THEN_DELETE` hoặc `REVIEW_PENDING` |
| `deletion_risk` | Điều gì mất/hỏng nếu xóa |
| `confidence` | `high`, `medium`, `low` và lý do ngắn |
| `evidence` | Exact headings/lines/paths chứng minh kết luận |

Không được kết luận `DELETE` chỉ từ filename, tuổi file, độ dài, việc đã
completed hoặc vì có chữ correction. Phải đọc đủ file, xác định chain, tìm
replacement và kiểm inbound references.

## 4. Cách User giao một topic

User chỉ cần gửi file này và một câu:

```text
Thực hiện document audit topic: <exact topic name trong §6>.
```

Implementer phải tự tìm toàn bộ Markdown liên quan topic trong `reports/` và
`handoff_prompt/`, không yêu cầu User liệt kê file. Dùng filename inventory trước,
sau đó đọc header/summary và full-read các candidate thuộc topic. Khi file có vẻ
thuộc hai topic, ghi `possible_overlap` trong report; không bỏ qua hoặc tự chuyển
ownership.

## 5. Workflow bắt buộc cho Implementer

### 5.1 Bootstrap và scope

1. Full-read file này.
2. Đọc `session_prompt/IMPLEMENTER_WORKFLOW.md`.
3. Ghi exact topic User giao và exact output path từ §6.
4. Tạo thư mục output tạm và chạy inventory read-only:

```bash
mkdir -p /tmp/hue_rag_document_audit
rg --files reports handoff_prompt -g '*.md' | sort
git status --short
git ls-files reports handoff_prompt
```

5. Lập candidate list theo topic rồi đọc đủ từng candidate; dùng `rg` để tìm
   inbound references trong active Markdown/code.

Audit này không phải implementation hiện hành trong `CURRENT_HANDOFF.md`.
Không thực hiện Phase 3, không đổi handoff, không sửa code/corpus/docs/README,
không chạy model/API/test suite và không đọc `.env` hoặc secrets.

### 5.2 Dùng sub-agent

User đã cấp standing authorization cho Implementer tự quyết dùng sub-agent khi
hữu ích, gồm task audit này và các task tương lai. Với audit song song:

- lead Implementer chịu trách nhiệm cuối cùng về completeness và report;
- giao cho sub-agent các tập file không chồng lấn;
- sub-agent chỉ đọc và trả findings cho lead;
- chỉ lead ghi exact batch report;
- sub-agent không có authority rộng hơn parent task, không Git write, destructive
  action, network, secret access hoặc scope expansion.

### 5.3 Quy tắc chạy nhiều Implementer đồng thời

- Mỗi Implementer chỉ xử lý topic User giao.
- Không sửa `PROJECT_DOCUMENT_REGISTRY.md`, directory README,
  `CURRENT_HANDOFF.md` hoặc file trong repository.
- Chỉ tạo một report ở exact `/tmp` path của topic; không tạo report trong
  `reports/` hoặc `handoff_prompt/`.
- Không commit, stage, push, reset, clean, rename, move hoặc delete.
- Không sửa report của topic khác. Nếu thấy overlap, ghi exact path để Reviewer
  reconcile sau.
- Existing dirty/untracked files thuộc User/agent khác; chỉ đọc nếu chúng nằm
  trong topic, tuyệt đối không cleanup.

### 5.4 Report format

Mỗi report phải gồm:

1. topic, timestamp, HEAD và worktree snapshot;
2. discovery method và candidate-file list;
3. bảng per-file đủ trường trong §3;
4. correction-chain map: prompt → implementation report → review → correction →
   final review/User closure;
5. danh sách `KEEP`;
6. danh sách `DELETE`/`MERGE_THEN_DELETE`, mỗi dòng có replacement và risk;
7. `REVIEW_PENDING` cùng exact câu hỏi còn thiếu;
8. possible overlaps với topic khác;
9. files đã inventory nhưng không đọc, kèm lý do;
10. self-check: không repository mutation và report nằm đúng `/tmp` path.

Không sửa file để thêm banner hoặc link trong lúc audit. Đề xuất mọi required
reference repair trong report để Reviewer lập một cleanup plan hợp nhất.

## 6. Mười topic và output không xung đột

| Exact topic name User giao | Phạm vi logic | Exact report output |
|---|---|---|
| `Phase 0–2 Foods` | Foundation, backend skeleton, Foods Markdown/chunking và correction/evidence liên quan; loại full-corpus Phase 2 | `/tmp/hue_rag_document_audit/01_phase_0_2_foods.md` |
| `Phase 3–5 Foods` | Foods embedding/sparse, Qdrant, retrieval, reranking và simplicity chains | `/tmp/hue_rag_document_audit/02_phase_3_5_foods.md` |
| `Phase 6–7` | Generation/API, retrieval-answer evaluation, Milestone 6.1 và correction chains | `/tmp/hue_rag_document_audit/03_phase_6_7.md` |
| `Phase 8 Golden và 08a` | Golden V2/V3, Gate 0/common contracts và embedding benchmark 08a | `/tmp/hue_rag_document_audit/04_phase_8_golden_08a.md` |
| `Phase 8 08b–08c` | Retrieval/fusion/sparse benchmark 08b và reranker benchmark 08c | `/tmp/hue_rag_document_audit/05_phase_8_08b_08c.md` |
| `Full-corpus parser, locator, token và chunking` | Parser/source locator surveys, VN/QT token checks, chunking research/evidence | `/tmp/hue_rag_document_audit/06_full_corpus_parser_token_chunking.md` |
| `Full-corpus Golden, evaluation và schema` | Golden/evaluation reference, schema deep-dive và correction chains; loại `rag_old_0` | `/tmp/hue_rag_document_audit/07_full_corpus_golden_evaluation_schema.md` |
| `rag_old_0` | Toàn bộ simplicity survey/prompts/reviews về `/home/minhhieu/rag_old_0` | `/tmp/hue_rag_document_audit/08_rag_old_0.md` |
| `llm_rag` | Full-project survey, complexity reset, verified architecture extraction và reviews | `/tmp/hue_rag_document_audit/09_llm_rag.md` |
| `Full-corpus design, Phase 2 và cross-cutting` | Brainstorming/umbrella contracts, full-corpus Phase 2 implementation/corrections, user closure và file cross-cutting/chưa được topic 1–9 sở hữu rõ | `/tmp/hue_rag_document_audit/10_full_corpus_design_phase_2_cross_cutting.md` |

Các topic là logic ownership, không phải quota cứng. Mục tiêu khoảng 15–20 file
mỗi topic; nếu một correction chain vượt quota thì giữ nguyên chain và báo số
file thật, không cắt đôi chain chỉ để đạt quota.

## 7. Tiêu chí Reviewer hợp nhất

Reviewer không chấp nhận recommendation chỉ vì nhiều Implementer đồng ý. Với
mỗi đề xuất xóa, Reviewer phải kiểm độc lập ít nhất:

- exact path và Git state;
- canonical replacement thực sự chứa thông tin cần giữ;
- active/future inbound references;
- User closure hoặc authority có bị mất không;
- correction chain có còn truy vết được không;
- link/index nào phải sửa cùng batch;
- deletion có thể phục hồi qua Git history hay không.

Sau khi reconcile overlap và unassigned files, Reviewer cập nhật §8 thành
registry retained-file chính thức, lập exact cleanup plan và xin User duyệt danh
sách xóa. Implementer không tự xóa từ recommendation của batch report.

## 8. Registry retained-file — seed trước audit

Bảng này chỉ chứa các entry đã đủ rõ trước audit; Reviewer sẽ mở rộng sau khi
nhận đủ mười report.

| Path | Role | Lifecycle/read mode | Retention |
|---|---|---|---|
| `session_prompt/CURRENT_HANDOFF.md` | Exact active role, task, authority và next action | Current; full-read đúng role | `ACTIVE_CONTROL` |
| `session_prompt/Project_Status.md` | Snapshot trạng thái project và routing | Current; bootstrap/targeted-read | `ACTIVE_CONTROL` |
| `session_prompt/Session_Prompt.md` | Shared source hierarchy và governance | Stable; full-read khi bootstrap yêu cầu | `ACTIVE_CONTROL` |
| `session_prompt/REVIEWER_WORKFLOW.md` | Hành vi Reviewer | Stable; Reviewer full-read | `ACTIVE_CONTROL` |
| `session_prompt/IMPLEMENTER_WORKFLOW.md` | Hành vi Implementer | Stable; Implementer full-read | `ACTIVE_CONTROL` |
| `reports/README.md` | Entry point định tuyến evidence | Current; targeted-read | `ACTIVE_CONTROL` |
| `handoff_prompt/README.md` | Entry point phân biệt active task với historical prompt | Current; targeted-read | `ACTIVE_CONTROL` |
| `handoff_prompt/FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md` | Lịch sử thiết kế full-corpus quan trọng | Reference-only; spec/plan đã duyệt có precedence | `FUTURE_REFERENCE` |
| `reports/llm_rag_verified_architecture_extraction_2026_09_11.md` | Verified architecture evidence của `llm_rag` | Targeted/reference theo topic | `CANONICAL_EVIDENCE` |
| `reports/llm_rag_verified_architecture_extraction_codex_review_2026_09_11.md` | Independent review và closure chain của extraction | Targeted/reference theo topic | `CANONICAL_EVIDENCE` |
| `reports/full_corpus_rag_old_0_evaluation_simplicity_survey_2026_09_10.md` | Kết quả simplicity survey `rag_old_0` | Reference-only đến khi evaluation design cần | `CANONICAL_EVIDENCE` |
| `reports/full_corpus_rag_old_0_evaluation_simplicity_survey_codex_review_2026_09_10.md` | Independent review của survey `rag_old_0` | Reference-only đến khi evaluation design cần | `CANONICAL_EVIDENCE` |

## 9. `_source-dumps` — cleanup track riêng

User xác nhận curated Markdown không được tạo dựa trên `_source-dumps`, thư mục
không còn cần thiết và hướng xử lý mong muốn là xóa, không chuyển vào
`khoi_phuc_moi_truong`.

Observed state ngày 2026-09-12:

- `knowledge-base-hue/_source-dumps/`: 34 files, khoảng 5.7 MiB;
- bị loại khỏi RAG discovery/config và không phải answer corpus;
- hai script cũ còn khai báo output vào thư mục:
  `backend/scripts/convert_huegov_department_raw_to_md.py` và
  `backend/scripts/convert_huegov_culture_raw_to_md.py`.

Hai script trên chỉ chứng minh code có output target cũ, không chứng minh script
đang chạy hoặc raw dumps có đóng góp vào curated corpus. Trước deletion batch,
Reviewer/Implementer phải kiểm exact references rồi đề xuất retire/remove hoặc
đổi behavior của hai script để thư mục không bị tái tạo. Các exclude rules có
thể giữ như defensive boundary nếu vẫn đúng và có test bảo vệ.

Không xóa trong document-audit sessions. Việc xóa 34 files và xử lý hai scripts
là một cleanup plan riêng với exact targets, reference repair và User approval.
