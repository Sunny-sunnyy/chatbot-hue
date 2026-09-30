# Codex Review: Full-corpus Phase 5 Retrieval and Reranking

Decision: ready_for_user_confirmation
Reviewer: Codex
Date: 2026-09-13 +07
Closure: User-confirmed 2026-09-14 +07
Canonical guide: `guides/phase_5_retrieval_profiles_reranking.md`
Implementation report: `reports/full_corpus_phase_5_retrieval_reranking_implementation_2026_09_13.md`

## 1. Phạm vi đã review

Reviewer đã đọc toàn bộ Written Spec, Implementation Plan + Review Contract,
canonical guide, implementation report và `CURRENT_HANDOFF.md`; đọc trực tiếp
toàn bộ ba file mới cùng exact diff của `backend/reranking/cross_encoder.py`.
Reviewer cũng kiểm ignored private artifacts ở mức aggregate, không mở hoặc
chép nội dung câu hỏi/corpus.

Minimum gate đã kiểm:

- base `41b638642caf432fc7484d08444ba609a0368708` khớp `HEAD` hiện tại;
- inventory có đúng bốn implementation paths, report và handoff đã khai báo;
- các thay đổi Reviewer/User-owned và 264 cached corpus removals vẫn tồn tại;
- `git diff --check` sạch;
- không thấy Qdrant write/delete/recreate call trong changed runtime;
- questions và detailed trace đều được `.gitignore` match qua rule `data/`.

## 2. Findings

### P5-R1 — Major — Selector không hợp lệ có thể tạo bằng chứng `PASS` với 0 cell

- Vị trí: `backend/retrieval/full_corpus_smoke.py:178-180,330-356`.
- Requirement: CLI `--select` phải chạy explicit configuration qua cùng
  production path; mọi cell phải được phân loại trung thực và chỉ PASS khi ma
  trận được yêu cầu thực sự chạy.
- Evidence: command với `--treatment typo --select P5-Q01` thoát mã `0`, ghi
  `total_cells: 0`, `cells: {}` và `overall_classification: PASS`.
- Tác động: typo hoặc selector unsupported có thể tạo false-positive evidence,
  làm Review Contract không đáng tin.
- Tiêu chí đóng: validate toàn bộ candidate/treatment/reranker/query selector,
  reject giá trị lạ và reject zero-cell selection bằng non-zero exit; thêm
  focused deterministic check cho chính nhánh này.

### P5-R2 — Major — Retrieval chưa fail closed với payload sai kiểu

- Vị trí: `backend/retrieval/full_corpus.py:239-250,323-335,367-449`.
- Requirement: Task 2 yêu cầu validate returned IDs, finite scores và exact five
  payload field types; strict readiness/failure policy phải trả typed dependency
  error, không để malformed payload đi tiếp.
- Evidence: code chỉ kiểm field có tồn tại. `search_text`, `source`, `title`,
  `heading_path` và `evidence_parts` không được kiểm theo Phase 4 payload
  contract trước BM25/reranker/result construction. Ví dụ `search_text` không
  phải string sẽ đi vào tokenizer; `heading_path` sai kiểu có thể bị `list(...)`
  chuyển thành dữ liệu hợp lệ giả hoặc ném raw exception.
- Tác động: live data hiện tại hợp lệ nên smoke PASS, nhưng required fail-closed
  behavior không được triển khai và lỗi dependency có thể rò thành exception
  không đúng contract.
- Tiêu chí đóng: một validation trực tiếp, dùng chung cho dense/sparse returned
  points, kiểm exact five keys/types theo payload Phase 4 và raise typed
  `RetrievalDependencyError`; có focused pure checks cho malformed values và
  bảo toàn normal-path behavior.

### P5-R3 — Major — Failure trace có thể vi phạm privacy allowlist

- Vị trí: `backend/retrieval/full_corpus.py:503-510,543-550` và
  `backend/retrieval/full_corpus_smoke.py:315-325,337-350`.
- Requirement: detailed trace không chứa absolute path/private configuration;
  point-level evidence chỉ được ghi vào ignored local destination.
- Evidence: readiness errors đưa absolute `Path` vào message, rồi smoke runner
  ghi nguyên `str(exc)` vào field tự do `error`. Đồng thời `--output` chấp nhận
  mọi repo path mà không xác minh destination ignored, nên detailed point IDs có
  thể bị ghi dưới tracked scope.
- Tác động: failure path — chính lúc diagnostics cần được lưu — có thể làm lộ
  filesystem/config detail hoặc đặt private trace ở vị trí có thể được commit.
- Tiêu chí đóng: persisted failure record dùng allowlisted code/message đã
  sanitize, không có absolute path/query/payload/secret; output destination phải
  fail closed nếu không phải safe local ignored target; thêm focused checks cho
  failure serialization và unsafe output target, không dựng fake provider.

### P5-R4 — Minor — Implementation report mô tả evidence chính xác hơn thực tế

- Vị trí: implementation report mục `RED/GREEN`, `Determinism`, `MiniLM cold
  and warm latency`; handoff phần test/latency.
- Evidence: file mới có 10 test functions, không phải 11; determinism so score
  sau khi round 6 chữ số (`full_corpus_smoke.py:244-245`), không phải “trùng
  khớp tuyệt đối”; latency gate đang lấy `trace.timings_ms.total_ms`
  (`full_corpus_smoke.py:265-269`), tức warm end-to-end request latency chứ không
  phải riêng reranker-stage latency.
- Tác động: không phủ định normal-path PASS vì end-to-end p95 còn nghiêm ngặt
  hơn reranker-only gate, nhưng report đang overstate precision/coverage.
- Tiêu chí đóng: sửa report/handoff để ghi đúng 10 tests, rounded-score
  determinism và end-to-end p95; hoặc đổi implementation/evidence rồi báo đúng
  behavior thực tế. Minor này được sửa cùng batch major, không tạo vòng riêng.

Không phát hiện blocker, Qdrant mutation, Foods behavior regression hoặc
complexity framework ngoài scope trong changed source.

## 3. Cách Reviewer chạy lại thật

```bash
git status --short
git diff --check
UV_CACHE_DIR=/tmp/hue-rag-phase5-review-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_retrieval.py backend/tests/test_retrieval_service.py -q --tb=short
UV_CACHE_DIR=/tmp/hue-rag-phase5-review-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke run --candidate e5-small-384 e5-base-768 huydang-dek21-768 qwen3-embedding-0.6b-1024 --treatment dense_bm25_rrf native_hybrid_rrf --reranker none minilm --select P5-Q01 P5-Q02 --output /tmp/full_corpus_phase5_reviewer_trace.json
UV_CACHE_DIR=/tmp/hue-rag-phase5-review-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke run --treatment typo --select P5-Q01 --output /tmp/full_corpus_phase5_invalid_selector.json
```

## 4. Kết quả quan sát

- Lượt pytest đầu trong sandbox: `9 passed`, `1 failed`, `8 errors`; nguyên nhân
  quan sát là network/DNS bị chặn khi thư viện kiểm Hugging Face cache. Không
  dùng lượt này để kết luận code fail.
- Chạy lại cùng exact pytest command với network access: `18 passed, 1 warning
  in 64.37s`.
- Fresh read-only selection trên Qdrant local, đủ 4 candidates × 2 treatments ×
  2 rerankers, hai query IDs: `16/16 PASS`, không anomaly, bốn candidates/hai
  treatments/hai modes đều có mặt; MiniLM end-to-end warm p95 từ `1123.53` đến
  `1532.28 ms`.
- Negative selector probe: process exit `0`, `total_cells=0`,
  `overall_classification=PASS`; đây là reproduction trực tiếp của P5-R1.
- Implementer trace cũ được đọc ở aggregate: 16 cells, bảy queries/cell,
  16 PASS, không anomaly, tám MiniLM cells có 21 observations. Đây là prior
  implementation evidence, không được gọi là fresh Reviewer run.

## 5. Giới hạn hoặc phần chưa chạy

- Reviewer không lặp full seven-question/16-cell matrix theo đúng Review
  Contract; selected live run đã phủ toàn bộ bốn candidates, hai treatments và
  hai reranker modes.
- Reviewer không mutate collection hoặc dựng malformed live payload. P5-R2 được
  kết luận từ exact required branch và source; correction dùng pure payload
  values rồi rerun normal live selection.
- Quality metrics, winner/finalist, Phase 6/8 và Qwen reranker vẫn ngoài scope.

## 6. Decision và bước tiếp theo

Decision: `changes_requested` vì P5-R1, P5-R2 và P5-R3 là required
fail-closed/privacy behaviors chưa đạt. Implementer xử lý một correction batch
theo `session_prompt/CURRENT_HANDOFF.md`, cập nhật implementation report và trả
handoff về Reviewer. Không commit/push; bốn canonical collections và Foods tiếp
tục read-only.

## 7. Correction 1 review

Decision: `changes_requested`

Reviewer đã review exact Correction 1 delta và chạy lại independent evidence.
P5-R1 đã đóng: selector sai thoát mã `1` và không tạo trace. Phần safe-output
của P5-R3 đã đóng: output dưới `backend/trace.json` bị chặn trước execution.
P5-R4 đã đóng bằng wording đúng trong implementation report. Hai required
behaviors còn thiếu và một scope violation được phát hiện như sau.

### P5-C1-R1 — Major — Failure trace vẫn persist raw exception text

- Vị trí: `backend/retrieval/full_corpus_smoke.py:88-99,419-429` và
  `backend/retrieval/full_corpus.py:260-273,625-637`.
- Requirement: persisted trace dùng allowlisted code/message và không chứa
  query, payload, secret, private configuration, raw exception detail hoặc
  absolute path.
- Evidence mới: `sanitize_error_detail()` chỉ regex đường dẫn rồi giữ nguyên
  `str(exc)`. Probe với
  `RuntimeError("query=PRIVATE_Q api_key=SECRET_MARKER config=PRIVATE_CFG")`
  trả lại nguyên cả ba giá trị trong `error_message`. Runtime cũng bọc raw
  dependency exceptions vào message ở các nhánh embedding/Qdrant/readiness, nên
  đây là reachable failure-path risk chứ không chỉ giả định regex.
- Tác động: P5-R3 chưa đóng; detailed trace có thể persist chính dữ liệu bị
  allowlist cấm khi dependency failure xảy ra.
- Tiêu chí đóng: failure record không derive persisted field nào từ raw
  `str(exc)`; chỉ persist fixed/allowlisted error code và safe type/category.
  Các logger ở failure path cũng không interpolate raw exception detail.
  Thêm focused test tiêm exception chứa query/secret/config/absolute path và
  chứng minh mọi marker đều vắng khỏi serialized record.

### P5-C1-R2 — Major — Nested `evidence_parts` validation chưa đúng schema Phase 4

- Vị trí: `backend/retrieval/full_corpus.py:181-220` và
  `backend/tests/test_full_corpus_retrieval.py:192-240`.
- Requirement: returned point phải fail closed theo exact Phase 4 payload
  contract; mỗi evidence part có schema
  `{role: body|header|condition, start: int, end: int, text: string}`.
- Evidence mới: validator hiện chỉ dùng `.get()`, chấp nhận nested extra/missing
  distinctions, mọi string làm `role`, và dùng `isinstance(x, int)` nên chấp
  nhận boolean offsets. Probe có `role="INVALID"`, `start=False`, `end=True` và
  `extra="accepted"` được trả về thành công.
- Tác động: malformed Qdrant payload vẫn có thể đi vào result/reranker dù
  Correction 1 tuyên bố strict contract; P5-R2 mới chỉ đóng ở top-level.
- Tiêu chí đóng: validate exact four nested keys, role allowlist và integer
  offsets không chấp nhận bool; giữ các invariant offset đã có và thêm focused
  negative checks cho ba trường hợp trên. Cả dense/sparse tiếp tục dùng chung
  validator.

### P5-C1-R3 — Major — Implementer sửa Reviewer-owned project status ngoài quyền

- Vị trí: `session_prompt/Project_Status.md`.
- Requirement: Reviewer sở hữu requirements/status/verdict; Implementer chỉ
  được sửa Reviewer-owned file khi exact Approval Closure Contract cho phép.
- Evidence mới: Correction 1 handoff không cấp quyền này, nhưng Implementer sửa
  current snapshot và tự ghi rằng correction/live probes đã được kiểm chứng;
  implementation report inventory cũng không khai báo file này. Phase table
  đồng thời vẫn ghi `ready_for_implementation`, mâu thuẫn với `final_review`.
- Tác động: lifecycle snapshot không còn trustworthy và role boundary bị phá.
- Tiêu chí đóng: Reviewer khôi phục/cập nhật status thuộc ownership của mình;
  Implementer không sửa lại `Project_Status.md` trong Correction 2 và phải khai
  báo đầy đủ mọi path thực sự sửa trong implementation report/handoff.

### Independent evidence sau Correction 1

- Focused suite: `21 passed, 1 warning in 63.22s`.
- Invalid-selector probe: exit `1`, không tạo output.
- Unsafe tracked-output probe: exit `1`, không tạo `backend/trace.json`.
- Fresh live read-only matrix: 4 candidates × 2 treatments × 2 rerankers × 2
  selected queries = `16/16 PASS`; determinism `16/16`, anomaly `0`; MiniLM
  warm end-to-end p95 `1007.95–1331.49 ms`.
- `git diff --check`: sạch.

Live normal path và P5-R1/P5-R4 không cần làm lại toàn bộ trong Correction 2.
Correction 2 chỉ sửa hai fail-closed validators, tests/report tương ứng và tuân
thủ lại ownership boundary theo `CURRENT_HANDOFF.md`.

## 8. Session stop and restart

User xác nhận giữ verdict `changes_requested` và kết thúc cả Reviewer lẫn
Implementer sessions ngày 2026-09-13 +07. Correction 2 đã được đóng gói trong
`session_prompt/CURRENT_HANDOFF.md` nhưng chưa được kích hoạt.

Ở session mới, mỗi role chỉ đọc đầy đủ bốn file bootstrap chuẩn và kiểm cấu trúc
thư mục theo prompt của User, sau đó dừng để báo đã nạp ngữ cảnh. Implementer chỉ
bắt đầu Correction 2 khi User ra lệnh tiếp theo; Reviewer chỉ tiếp tục khi nhận
handoff `final_review`. Không có approval, closure, commit hoặc push phát sinh từ
việc kết thúc session này.

## 9. Correction 2 review

Decision: `changes_requested`

Reviewer đã đọc toàn bộ implementation report và exact Correction 2 handoff,
kiểm changed/untracked paths, đối chiếu lại Written Spec cùng Review Contract,
đọc focused source anchors và chạy independent checks. P5-C1-R1 đã đóng: failure
record chỉ còn fixed code/category và exception type, không derive persisted
field từ `str(exc)`; failure loggers không interpolate raw exception detail;
privacy marker probe đạt. Ownership boundary P5-C1-R3 cũng được giữ trong lượt
Correction 2. P5-C1-R2 vẫn còn một trường hợp malformed JSON chưa fail bằng
typed dependency error.

### P5-C2-R1 — Major — Non-string `role` có thể thoát ra raw `TypeError`

- Vị trí: `backend/retrieval/full_corpus.py:227-230` và
  `backend/tests/test_full_corpus_retrieval.py:243-317`.
- Requirement: mỗi `evidence_parts[].role` chỉ nhận `body`, `header` hoặc
  `condition`; mọi payload sai schema phải raise `RetrievalDependencyError`.
- Evidence mới: validator thực hiện `role not in ALLOWED_EVIDENCE_ROLES` trước
  khi kiểm kiểu. Pure probe với JSON-compatible `role=[]` trả
  `TypeError: unhashable type: 'list'`, không phải `RetrievalDependencyError`.
  Test hiện tại chỉ phủ invalid string nên không bắt được nhánh này.
- Tác động: payload Qdrant malformed dạng array/object vẫn phá typed
  fail-closed boundary trước BM25/RRF/reranker; vì vậy P5-C1-R2 chưa đóng.
- Tiêu chí đóng: kiểm `role` là string trước membership (hoặc logic trực tiếp
  tương đương); invalid string và các non-string JSON values, tối thiểu array và
  object, đều raise `RetrievalDependencyError`. Giữ validator dùng chung cho
  dense/sparse và không thêm abstraction mới.

### P5-C2-R2 — Minor — Implementation report còn hai lỗi inventory/evidence wording

- Vị trí: implementation report mục 4 P5-C1-R3 và mục 5 Evidence Reused.
- Evidence: report ghi “chỉ chỉnh sửa 4 tệp” nhưng liệt kê năm path của
  Correction 2; đồng thời ghi latency prior evidence là `1.007–1.893 ms`, không
  khớp Correction 1 independent evidence `1007.95–1331.49 ms` và handoff hiện
  hành.
- Tác động: không đổi runtime verdict nhưng làm evidence index thiếu nhất quán.
- Tiêu chí đóng: sửa count thành năm path và dùng đúng prior evidence/source,
  đơn vị milliseconds. Minor được sửa cùng batch major, không tạo vòng riêng.

### Independent evidence sau Correction 2

- `git diff --check`: sạch trước khi Reviewer cập nhật report/handoff/status.
- Focused suite: `23 passed, 1 warning in 63.38s`.
- Pure privacy probe: marker query/secret/config/absolute path vắng khỏi
  serialized failure record; unknown exception vẫn được phân loại fixed
  `ERR_INTERNAL/internal_error`.
- Pure malformed-role probe: `role=[]` trả raw `TypeError`, tái tạo P5-C2-R1.
- Selected read-only live matrix lần đầu trong sandbox thất bại 8/8 với
  `ResponseHandlingException` do không truy cập được Qdrant local; không dùng
  lượt này làm code verdict. Chạy lại ngoài sandbox trên exact target thật đạt
  `8/8 PASS`, determinism `8/8`, anomaly `0`, phủ bốn candidates × hai
  treatments × `reranker=none` cho `P5-Q01`.
- Không thấy create/upsert/delete/update collection call trong changed runtime.

Correction 3 chỉ cần sửa một type guard trực tiếp, focused negative tests và hai
lỗi wording trong implementation report. Selected live matrix vừa đạt được phép
reuse vì fix này không đổi input, dependency, environment hoặc normal data flow.
Không commit/push; bốn canonical collections và Foods tiếp tục read-only.

## 10. Correction 3 final review

Decision: `ready_for_user_confirmation`

### Phạm vi và findings

Reviewer đã đọc toàn bộ implementation report và final-review handoff cập nhật,
kiểm exact type guard, toàn bộ focused negative probes, inventory, evidence
wording và role/safety boundaries. Không còn blocker hoặc major trong Phase 5.
P5-C2-R1 đã đóng bằng một type guard trực tiếp, không thêm abstraction hay đổi
normal retrieval data flow. P5-C2-R2 đã đóng bằng count và latency wording đúng.

### Independent checks

```bash
git diff --check
UV_CACHE_DIR=/tmp/hue-rag-phase5-review-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_retrieval.py backend/tests/test_retrieval_service.py -q --tb=short
UV_CACHE_DIR=/tmp/hue-rag-phase5-review-uv-cache uv run --env-file .env python -c '<direct malformed-role probe>'
```

Fresh observed result:

- `git diff --check`: sạch;
- focused suite: `23 passed, 1 warning in 63.14s`;
- direct probe: list, dict, int, `True`, `False`, `None` và invalid string đều
  raise `RetrievalDependencyError`;
- không có disallowed collection mutation call trong changed runtime.

Reused evidence: Correction 2 selected read-only run đạt `8/8 PASS`,
determinism `8/8`, anomaly `0` trên bốn candidates × hai treatments ×
`reranker=none` × `P5-Q01`. Evidence này được reuse vì Correction 3 chỉ thêm
type guard cho malformed `role` và không đổi input, dependencies, environment
hay normal live path. Full 16-cell/MiniLM evidence, selector/safe-output và
privacy evidence từ cùng implementation series cũng không bị delta ảnh hưởng.

### Giới hạn

- Reviewer không lặp live matrix sau Correction 3 theo đúng evidence-reuse
  contract; normal live path không thay đổi.
- Phase 5 chứng minh contract/integration/determinism/latency, không chứng minh
  retrieval quality, không chọn winner và không cutover production.
- Bốn canonical collections cùng Foods collection vẫn read-only; Phase 6/8,
  Qwen reranker và remote-GPU research tiếp tục ngoài scope.

### Approval Closure Contract

User có thể xác nhận chính xác: `Tôi xác nhận closure Full-corpus Phase 5.`

Sau xác nhận, Reviewer được thực hiện các cập nhật cơ học sau:

1. đổi Full-corpus Phase 5 sang `approved` trong
   `session_prompt/Project_Status.md` và canonical guide;
2. đổi user report sang trạng thái đã xác nhận và ghi ngày xác nhận;
3. cập nhật file review này với User confirmation;
4. đặt `session_prompt/CURRENT_HANDOFF.md` thành `State: completed`, không có
   execution authority và chờ User giao phase tiếp theo.

Không có Git authorization: closure không cho phép commit/push. Phase 6 vẫn
đóng cho tới khi User giao exact design task mới.

## 11. User confirmation và closure

User đã phản hồi chính xác `Tôi xác nhận closure Full-corpus Phase 5.` ngày
2026-09-14 +07. Phase 5 được chuyển sang `approved`; technical evidence và các
giới hạn tại mục 10 giữ nguyên. Confirmation này không cấp quyền commit/push,
không kích hoạt Phase 6/8, Qwen reranker, remote-GPU research, production
cutover hoặc collection cleanup.
