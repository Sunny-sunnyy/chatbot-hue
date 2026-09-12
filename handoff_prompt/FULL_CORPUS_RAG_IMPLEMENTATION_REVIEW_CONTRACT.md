# Full-corpus RAG Implementation Review Contract

```text
Status: approved by User 2026-09-11
Written Spec: approved 2026-09-11
Implementation authorization: Wave 1 only through active handoff
Sequential wave workflow amendment: approved by User 2026-09-11
```

## 1. Phạm vi contract

Contract này điều khiển implementation handoff, Implementer self-verification và
Reviewer final review cho
[Implementation Plan](../docs/superpowers/plans/2026-09-11-full-corpus-rag-implementation-plan.md).
Approved Written Spec là nguồn behavior/data contract; Plan là nguồn sequencing,
file scope và execution gates. Working decision notes không được dùng để mở rộng
scope khi Spec/Plan đã rõ.

Mỗi wave là một task độc lập. `CURRENT_HANDOFF.md` phải nêu exact wave, role,
allowed paths, commands và live authority. Implementer không tự bắt đầu wave sau.

Trước mọi wave sau Wave 1, Reviewer phải đóng review/closure wave trước, cập
nhật guide phase liên quan và trình User duyệt exact wave spec, implementation
plan cùng Review Contract. Thiếu một artifact hoặc approval thì verdict chỉ áp
dụng cho wave đã review; không tạo handoff triển khai tiếp. Guide phải phân biệt
`approved target` với `observed/implemented`, không mô tả dự kiến như kết quả.

## 2. Evidence hierarchy

Reviewer đánh giá theo thứ tự:

1. approved Written Spec;
2. approved Implementation Plan và active wave handoff;
3. source code/config/data artifact hiện hành;
4. Implementer report và machine-readable outputs;
5. historical reports chỉ làm reference.

Report Implementer là evidence index, không phải proof và không tự tạo PASS.
Claim về behavior phải được kiểm bằng source/artifact; claim live phải có exact
command, target/config, timestamp và output có thể đối chiếu.

Không dùng report survey `llm_rag` 885 dòng, correction cũ hoặc hai tài liệu
reference repository làm primary evidence. Chỉ targeted-read exact source khi
approved extraction thiếu chi tiết.

## 3. Handoff contract của Implementer

Mỗi report phải có:

- wave/subwave, base/head worktree state và danh sách task paths;
- acceptance criterion → source/test/artifact evidence mapping;
- commands đã chạy, exit status, counts và failures;
- live targets/model/provider/settings nếu được phép;
- các mục chưa chạy/chưa kiểm chứng;
- pre-existing modified/untracked files tách khỏi task changes;
- deviations, assumptions và follow-up cần Reviewer/User quyết định.

Không dán toàn bộ source, test output hoặc secrets. Không sửa report lịch sử.
`git diff --check` phải sạch. Handoff chỉ chuyển Reviewer/final_review khi mọi
deliverable bắt buộc của active wave tồn tại.

## 4. Reviewer authority và phương pháp

Reviewer:

- đọc full active report và mọi artifact được contract đánh dấu full-read;
- kiểm `git status --short`, task paths và `git diff --check`;
- đọc source/config/data thay đổi liên quan, không chỉ report;
- kiểm mapping với Spec/Plan và tìm overengineering/silent fallback;
- không sửa implementation report thay Implementer;
- không triển khai runtime hoặc sửa code/data để “giúp PASS”;
- không chạy model/API/Qdrant/tests/frontend/notebook/benchmark theo authority
  hiện hành; chỉ dùng read-only/static checks;
- không đọc `.env`/logs, không Git write và không dùng subagent.

Nếu User sau này cấp quyền Reviewer chạy một check cụ thể, handoff phải ghi exact
command/target. Quyền đó không suy rộng sang check khác.

## 5. Severity / verdict

Severity:

- **Blocker:** mất dữ liệu, sai target/authority, secret exposure, active Foods
  mutation, partial index được coi complete hoặc official metric từ incomplete
  run.
- **Major:** vi phạm Spec có ảnh hưởng behavior/evidence; silent truncation/
  fallback; locator/citation sai; treatment không độc lập; metric/schema sai;
  thiếu test/evidence bắt buộc; overengineering làm đổi contract.
- **Minor:** lỗi cục bộ không đổi contract/result, tài liệu hoặc naming cần sửa.

Verdict:

- `approved`: không còn Blocker/Major; required evidence đủ;
- `changes_requested`: còn Blocker/Major;
- `approved_with_minor` chỉ khi minor rõ, bounded và không cần correction wave.

Correction phải là delta hẹp cho findings còn mở. Không mở lại artifact đã
approved nếu không có evidence mới. Reviewer không tự đánh dấu User closure.

## 6. Review Wave 1 — parser/locator

Reviewer kiểm:

- dependency chỉ thêm `markdown-it-py`, lockfile nhất quán;
- include/exclude paths đúng Plan và sorted discovery;
- LF normalization trước hash/locator;
- Markdown tokens dùng cho structure nhưng evidence slice từ source LF;
- `heading_path`, intro, nested list/table/blockquote và image-only behavior;
- condition selector exact-one-match, mismatch thật sự chặn output;
- zero-based code-point ranges và mọi sampled/all-artifact exact-match checks;
- deterministic chunk IDs/UUID5 và duplicate detection;
- tokenizer checks không truncate; preview lỗi chặn toàn output;
- six named corpus samples có assertions, không chỉ snapshot dễ update.

Acceptance artifact phải báo total files/chunks, domain/P7 breakdown,
zero-error preview và oversized groups. Không dump corpus text rộng.

## 7. Review Wave 2 — index/retrieval

### 2A static/code review

- dense candidate IDs/dimensions/preprocessing explicit, không generic plugin;
- point có named `dense`/`sparse` và payload đúng năm field;
- sparse vocabulary lexicographic, BM25 k1/b/IDF/TF formula parity và query
  không mutate vocabulary;
- build identity ở file/index level, không lặp per-point;
- fresh-target guard chạy trước upsert; build complete chỉ sau verification;
- baseline chỉ BM25-rescore dense pool; native hybrid có sparse query thật;
- cả hai dùng depth 30, RRF `1/(60+rank)` và fixed tie-break; không weighted
  legacy fusion trá hình;
- failure không fallback;
- reranker overlong pair skip toàn request và giữ order.

### 2B live-index review

Reviewer đối chiếu exact collection names với User-approved preflight, chứng cứ
target mới/rỗng, schema, point counts và build records. Bất kỳ target Foods hoặc
target không approved là Blocker. Partial upsert không được đánh complete.

## 8. Review Wave 3 — generation/API/UI

Reviewer kiểm:

- concrete OpenRouter path, exact Qwen slug, temperature/budgets/timeout;
- upstream bắt buộc explicit; không auto-route/retry/failover;
- representation B cap 256 và không nhiễm evidence/citation;
- token budget trừ mọi overhead, pack whole chunks đúng rank/Top-5;
- no-evidence success khác technical error;
- exact HTTP/error envelope; public success chỉ `answer`/`sources`;
- citation validation dùng backend evidence, không tin model-supplied source;
- không lộ path/chunk/hash/model/offset/vector/score/debug/token;
- safe Markdown; keyboard citation focus; source cards inline;
- duplicate submit disabled và manual retry không thành automatic retry;
- không session/streaming/agentic UI hoặc new frontend framework.

Live smoke chỉ PASS nếu call list/upstream được User approve, report chứng minh
pinning và không chứa secret. Smoke không là official quality benchmark.

## 9. Review Wave 4 — P7 Golden

Reviewer full-read mọi row của partition hiện hành. Với mỗi case kiểm:

- question tự nhiên, closed-world và không template spam;
- reference answer được corpus hỗ trợ;
- keywords nhỏ nhất nhưng đủ, nguyên văn, specific, không duplicate/padding;
- đúng một category theo thao tác chính;
- `partition` đúng nhánh; không field thừa;
- không trùng câu trong partition hoặc approved partitions trước.

Findings phải chỉ exact row và correction cần thiết. Không approve partition nếu
còn required correction. User closure là điều kiện sang bắt đầu partition sau.

Merge review kiểm bảy input đã approved, strip partition, field duplicate,
field order, seed 42 và byte determinism evidence. Smoke review full-read 10 rows,
deep-equal canonical, P7 coverage và relative order.

## 10. Review Wave 5 — evaluator/live benchmark

### 5A evaluator

- formulas và cutoff K=10 đúng per case;
- judge model `gpt-5.4-mini`, temperature 0, cap 600, đúng input fields;
- three scores integer 1–5 + feedback; không groundedness claim;
- macro-average overall/category; không composite/micro;
- empty-result 0/1 semantics;
- any technical failure làm run incomplete và chặn official aggregate;
- outputs giữ exact config/count/error, không secret.

### 5B live benchmark

Reviewer đối chiếu User-approved call/cost/target preflight. Mỗi stage phải giữ
control variables và đúng order:

1. A: 3 dense × 2 retrieval;
2. User-approved finalists mới vào reranker;
3. User-approved finalists mới tạo B;
4. end-to-end full Golden mới dùng generator/judge;
5. failed cases rerun trước official aggregate.

Không accept smoke/partial/mock như official evidence. Reviewer chỉ báo exact
metrics và đề xuất; winner, thresholds, cutover, replacement và cleanup cần User
decision riêng.

## 11. Final integrated review

Sau Wave 5 complete, Reviewer kiểm xuyên suốt:

- config → discovery → chunk/evidence → point/build record;
- query → retrieval treatment → reranker → context packing;
- generator → citation validation → API → UI;
- Golden → evaluator → report → finalist/cutover proposal.

Reviewer xác nhận no dead fields, no unused abstraction, no duplicate source of
truth và no historical behavior accidentally promoted. `git diff --check` sạch;
task changes/pre-existing worktree state được phân định.

Technical readiness không tự là product approval. Reviewer tạo closure contract
cho User; chỉ User mới approve runtime cutover/cleanup và completed state.

Sau mỗi wave/subwave, closure phải ghi exact guide/spec/plan/status updates và
đưa `CURRENT_HANDOFF.md` về Reviewer design gate cho dependency kế tiếp. Không
đợi Wave 6 mới sửa guide đã bị implementation làm thay đổi; Wave 6 chỉ làm lượt
đối chiếu tích hợp cuối.

## 12. Plan approval effect

User đã duyệt đồng thời Implementation Plan và Review Contract ngày 2026-09-11.
Reviewer đã chuyển `CURRENT_HANDOFF.md` sang Implementer/implementation cho duy
nhất Wave 1. Không có quyền ngầm cho wave sau, paid calls, Qdrant targets,
cleanup hoặc Agentic RAG.
