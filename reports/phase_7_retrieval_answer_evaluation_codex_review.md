# Codex Review: Phase 7 Retrieval & Answer Evaluation

Decision: changes_requested
Reviewer: Codex
Date: 2026-08-23 (revision 9 re-review)

## Tóm tắt quyết định

Revision 9 sửa đúng bốn failures đã được probe ở Revision 8. Consent gate hiện
chặn cả fresh/resume trước Qdrant/budget; parser `all` không còn thiếu fields;
budget reject NaN; calibration partial duplicate raw ID bị reject. Reviewer chạy
lại probe cũ và xác nhận 4/4 pass. Targeted suite 141 tests, validator 104/104,
notebook hygiene, CodeGraph và Qdrant 572 points cũng đạt.

Paid gate vẫn chưa thể mở. Năm probe integration/integrity mới đều fail:

1. Budget state thiếu toàn bộ `totals` vẫn load thành công.
2. Attempt bị sửa sang unknown model vẫn load thành công.
3. State có số attempts vượt frozen `max_calls` vẫn load thành công.
4. Calibration final đi qua đúng `reuse_path` của CLI chấp nhận wrong run ID và
   tampered case ID.
5. Cũng trên đúng nhánh CLI, final calibration tồn tại nhưng summary mất không
   được rebuild; code raise `CalibrationPackageError`.

Ngoài ra “exact attempt linkage” mới chỉ được ghi khi tạo row, chưa được validate
khi resume/notebook. Exact Cell 15 success fixture hiện pass dù cả 56 budget
attempts đều giả làm generation của một case và generation/judge rows không link
attempt ID nào. Vì vậy durable journal chưa thực sự chứng minh 8 calibration +
24 generation + 24 judge calls của package.

Phase 7 tiếp tục `changes_requested`; không chạy paid batch.

## Findings

### Blocker 1 — CLI calibration-final path bypass strict raw validator

Trong `backend/evaluation/evaluator.py:179`, resume truyền
`reuse_path=cal_final_path` nếu final tồn tại. `run_calibration()` xử lý
`reuse_path` tại `answer_eval.py:653-684` trước nhánh strict final validation ở
dòng 700 trở đi.

Hệ quả:

- `raw_validate_calibration_records()` không chạy trên final path thực của CLI;
- `calibration_run_id` expected không được so với run ID trong rows/summary;
- `case_id` và `category` không được `validate_calibration_package()` kiểm;
- final file tên theo linked run nhưng chứa rows + summary của run khác vẫn pass;
- final tồn tại nhưng summary mất bị reject ngay, nên recoverable-summary branch
  ở dòng 700 không reachable từ CLI.

Probe đặt final file dưới `cal-linked.jsonl`, nhưng tất cả rows/summary có
`run_id=cal-other` và một row có `case_id=tampered-case`; resume reuse vẫn trả
gate passed. Probe final-without-summary trên đúng `reuse_path` raise thay vì
rebuild zero-call summary.

Đây là identity và crash-recovery failure tại production entry point, không phải
lỗi helper riêng lẻ.

### Blocker 2 — Durable budget loader vẫn fail-open với state không đầy đủ

`CallBudget.load()` có các gaps sau:

- `stored_totals = data.get("totals", {})` rồi chỉ validate khi truthy
  (`budget.py:395-415`), nên missing/empty totals được chấp nhận;
- attempt `model` không được validate hoặc bind với frozen answer/judge model;
- recomputed `calls` không được assert `<= max_calls`;
- recomputed effective cost không được kiểm với frozen cap theo một policy rõ;
- required attempt fields/status coherence chưa được validate đầy đủ.

Independent probes chứng minh cả missing totals, unknown attempt model và hai
attempts trong state có `max_calls=1` đều load thành công. Một tampered artifact
đã vượt hard cap vì vậy vẫn có thể được notebook coi là paid evidence hợp lệ.

### Major 3 — Attempt linkage chỉ được ghi, chưa được chứng minh

`generation_record()`/`judge_record()` đã có `attempt_ids`, `attempts` và
`cost_usd_total`, nhưng không có shared validator đối chiếu rows với
`budget.attempts`. Search toàn runtime cho thấy các fields này chỉ được tạo; các
resume loaders và Cell 15 không consume/validate chúng.

Các failure modes hiện còn mở:

- row dùng nonexistent hoặc wrong-stage/wrong-case attempt ID;
- hai rows cùng claim một attempt;
- row bỏ failed/unresolved attempt trước retry;
- `attempts != len(attempt_ids)`;
- `cost_usd_total` không bằng exact sum charged/reserved costs;
- journal có orphan attempts không được row nào giải thích.

Đặc biệt, per-call lists hiện khởi tạo rỗng trong mỗi invocation. Sau crash hoặc
resume, row mới chỉ link attempts của process hiện tại, không tự thu thập prior
attempts cùng stage/case từ journal.

### Major 4 — Notebook chưa validate full budget/package linkage

Cell `17ca5224` đã bắt buộc path và checksum, nhưng vẫn thiếu:

- không assert `budget.identity.calibration_run_id == answer_summary.calibration_run_id`;
- không validate summary `budget_schema_version`;
- không freeze/verify expected limits `64` và `$0.50`;
- cost dùng tolerance `< 1e-8` thay vì exact canonical comparison;
- không validate stage distribution và exact row-attempt linkage.

Existing exact-cell success fixture tự tạo 56 attempts đều có stage
`generation`, case `foods-0001`, trong khi 24 generation + 24 judge rows có
`attempt_ids=[]`; Cell 15 vẫn pass. Do đó assertion `56 <= calls <= 64` chỉ kiểm
số lượng tổng, không chứng minh normal package 56-call composition.

### Major 5 — Ma trận test được báo cáo chưa bao phủ contract

Các tests mới chứng minh helpers/happy paths, nhưng thiếu các integration cases
bắt buộc:

- CLI final calibration missing-summary recovery;
- final wrong expected run/case/category trên `reuse_path`;
- missing totals, unknown attempt model, recomputed total vượt cap;
- true persisted near-cost-cap reload (test 13 chỉ reject một reservation quá
  lớn trên budget mới);
- orchestration normal 56 calls và shared slots 57–64/attempt 65;
- row ↔ journal exact linkage và orphan/duplicate attempt rejection;
- notebook missing path/file, wrong calibration link/schema/limits/totals/NaN.

Test `test_cell_15_mandatory_budget_validation_fails_on_tamper` chỉ thực hiện
checksum mismatch dù docstring nói nhiều tamper modes.

## Những phần Revision 9 đã đạt

- Consent fresh/resume trước live dependencies; probe Revision 8 pass.
- `all` delegation không còn `AttributeError` trên no-consent path.
- NaN/Inf/negative validation và `allow_nan=False` đã được thêm.
- Public `cancel()` đã bị xóa; persisted reservations không có refund API.
- Calibration partial raw list được validate trước map và normalize trước
  finalize trên non-reuse path.
- Attempt IDs/totals được ghi cho attempts tạo trong cùng invocation.
- Notebook budget path/checksum đã chuyển từ optional sang mandatory.
- Không có paid provider calls trong re-review.

## Verification độc lập

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-review9-uv-cache uv run python -m pytest \
  tests/test_evaluation_budget.py tests/test_evaluation_loader.py \
  tests/test_evaluation_metrics.py tests/test_evaluation_artifacts.py \
  tests/test_retrieval_evaluation.py tests/test_answer_evaluation.py \
  tests/test_evaluation_controls.py tests/test_evaluator_cli.py -q --tb=short
# PASS: 141 passed, 1 warning in 6.87s

UV_CACHE_DIR=/tmp/hue-rag-review9-uv-cache uv run python -m py_compile \
  evaluation/budget.py evaluation/artifacts.py evaluation/answer_eval.py \
  evaluation/evaluator.py tests/test_evaluation_budget.py \
  tests/test_evaluation_controls.py tests/test_evaluator_cli.py
# PASS

cd ..
UV_CACHE_DIR=/tmp/hue-rag-review9-uv-cache uv run --env-file .env python \
  knowledge-base-hue/foods/evaluation/validate_tests.py
# PASS: 104 tests, all checks green

git diff --check
# PASS

codegraph status .
# PASS: index up to date; 80 files, 1,325 nodes, 3,775 edges
```

Notebook: nbformat 4.5, 8 code cells, zero outputs/execution counts, exact Cell
15 ID xuất hiện một lần. Qdrant read-only:
`hue_foods_e5_small_384 = 572 points`.

Reviewer probes:

```text
Revision 8 regression probes                         4 passed
budget requires totals                              FAIL
budget rejects unknown attempt model                FAIL
budget rejects calls above frozen cap               FAIL
reuse final checks expected run/case identity       FAIL
CLI-path final-without-summary recovery             FAIL
```

## Hướng dẫn triển khai Revision 10

### 1. Loại bỏ dual semantics của calibration final

Vì fresh calibration reuse đã bị cấm, CLI resume không cần `reuse_path` nữa.
Thiết kế đơn giản nhất:

1. Xóa hoặc cô lập legacy `reuse_path` branch khỏi paid CLI.
2. Resume luôn truyền `calibration_run_id`, `resume=True`, `reuse_path=None`.
3. `run_calibration()` tự locate exact partial/final từ `results_dir` + frozen
   run ID.
4. Cả partial và final phải đi qua cùng
   `raw_validate_calibration_records()` trước map/skip/summary.
5. Final missing summary: validate final, derive summary, write atomically, zero
   judge calls.
6. Final + summary tồn tại: validate cả rows lẫn full summary identity/gate;
   không silently ignore tampered summary.

Mở rộng raw validator để always check exact case/category mapping, scores,
attempt metadata và expected run ID. Nếu frozen samples không có category, định
nghĩa canonical expected category rõ ràng thay vì bỏ check có điều kiện.

### 2. Làm budget schema fail-closed hoàn chỉnh

`CallBudget.load()` phải require exact top-level structure tối thiểu:
`schema_version`, `package_id`, `identity`, `limits`, `attempts`, `totals`.
Missing, wrong type hoặc empty required object phải reject.

Mỗi attempt phải validate:

- non-empty ID; unique;
- stage, case ID, generation ID và positive attempt number;
- model thuộc approved pricing table;
- model khớp frozen identity: generation → answer model;
  calibration/judge → judge model;
- finite exact reserved/charged costs;
- status/usage/error consistency;
- optional uniqueness của `(stage, case/generation ID, attempt_number)` theo
  retry policy.

Sau recompute, require exact equality của cả bốn totals. Assert calls không vượt
`max_calls`. Với effective cost vượt cap, chọn/document policy fail closed cho
tampered state nhưng vẫn phân biệt trường hợp unavoidable actual settlement
vượt reservation; conservative reservation phải đủ để trường hợp hợp lệ không
xảy ra.

Không dùng optional `if stored_totals`. Không dùng loose float tolerance. Giữ
canonical Decimal/integer money representation xuyên persist/load/summary.

### 3. Tạo shared exact attempt-linkage validator

Tạo pure helper dùng chung cho answer resume và notebook. Input gồm budget,
calibration rows, generation rows, judge rows và expected manifest/samples.

Với complete package, helper phải chứng minh:

- mỗi row có non-empty `attempt_ids` đúng bằng all journal attempts của
  stage/case/generation ID đó;
- `attempts == len(attempt_ids)`;
- IDs unique trong row và không được claim bởi row khác;
- stage/model/case/generation linkage đúng;
- `cost_usd_total` bằng exact sum effective cost của referenced attempts;
- mọi journal attempt được claim đúng một lần;
- normal no-retry distribution là 8 calibration + 24 generation + 24 judge;
- retry attempts giải thích calls 57..64; attempt 65 bị budget chặn;
- complete package không có unresolved attempt.

Khi tạo/ghi row, không chỉ dùng local `attempt_ids=[]`. Query journal để lấy toàn
bộ prior + current attempts cho identity của row, kể cả unresolved/failed attempt
từ process trước, rồi derive count/cost. Đây là điều kiện để crash-resume giữ
exact evidence.

### 4. Harden Cell 15 bằng shared validators

Cell 15 không nên tự triển khai lại budget rules. Sau safe path + checksum:

1. `CallBudget.load()` với full expected identity gồm `calibration_run_id`.
2. Assert exact supported schema và exact frozen limits 64/0.50.
3. So summary snapshot bằng canonical exact representation.
4. Gọi shared row/journal linkage validator.
5. Validate exact calibration run/path/summary identity.
6. Chỉ sau đó mới tính và hiển thị metrics.

Resolve budget path rồi kiểm `resolved_path.is_relative_to(RESULTS.resolve())`
để chặn cả traversal/symlink escape, thay vì chỉ tìm substring `..`.

### 5. Test matrix bắt buộc

Giữ toàn bộ 141 tests và thêm:

1. CLI resume final + missing summary rebuild zero calls.
2. CLI final wrong run ID/case/category/summary identity reject zero calls.
3. Missing/empty/partial totals reject.
4. Unknown/wrong-stage model và malformed attempt fields reject.
5. Recomputed calls > frozen cap reject.
6. Persisted cost sát cap, reload, next reservation blocked.
7. Normal orchestration fake path tạo đúng 8/24/24 = 56 attempts.
8. Retry slots 57..64 shared across stages; attempt 65 zero provider calls.
9. Crash + resume row links prior unresolved/failed và current retry attempts.
10. Nonexistent, orphan, duplicate, wrong-stage attempt references reject.
11. `cost_usd_total`/attempt count tamper reject.
12. Exact Cell 15 fail cho missing path/file, traversal/symlink, checksum,
    calibration link, schema, limits, totals, NaN và attempt distribution.

Các CLI tests phải gọi đúng production wiring, không gọi helper với
`reuse_path=None` nếu CLI thực tế truyền path khác.

### 6. Scope và stop conditions

Expected scope:

```text
backend/evaluation/budget.py
backend/evaluation/answer_eval.py
backend/evaluation/evaluator.py
backend/evaluation/artifacts.py                 # chỉ nếu cần shared validator
backend/tests/test_evaluation_budget.py
backend/tests/test_evaluation_controls.py
backend/tests/test_evaluator_cli.py
notebooks/07_evaluation.ipynb
reports/phase_7_retrieval_answer_evaluation_implementation_report.md
```

Không đổi dataset, provider/model, pricing, prompt, rubric, collection, retrieval
profile, benchmark hoặc Phase 8. Không chạm unrelated dirty-worktree changes.
Chỉ pure deterministic tests/read-only validation; zero paid calls. Sau khi cập
nhật implementation report Revision 10, dừng để Codex re-review. Không user
report, Project Status, commit hoặc push.

## Prompt copy/paste cho coding agent

```text
Bạn đang triển khai Revision 10 cho Phase 7 tại /home/minhhieu/hue_rag.

Trước khi sửa, đọc TOÀN BỘ:
- session_prompt/Session_Prompt.md
- session_prompt/REVIEWER_WORKFLOW.md
- reports/phase_7_retrieval_answer_evaluation_codex_review.md
- reports/phase_7_retrieval_answer_evaluation_implementation_report.md
- guides/phase_7_retrieval_answer_evaluation.md
- skills/karpathy-guidelines/SKILL.md

Thực hiện đầy đủ mục “Hướng dẫn triển khai Revision 10” trong Codex review.
Paid gate đang khóa; không gọi provider trả phí.

Các lỗi phải sửa đồng thời:
1. CLI resume final đi qua reuse_path nên bypass raw validator, chấp nhận wrong
   run/case identity và không rebuild summary bị mất.
2. Budget loader chấp nhận missing totals, unknown attempt model và state có
   calls vượt frozen max_calls.
3. attempt_ids/cost_usd_total mới chỉ được ghi, chưa validate hoặc giữ đầy đủ
   prior attempts qua crash/resume.
4. Cell 15 chưa bind calibration ID/limits/schema và chưa chứng minh journal có
   đúng 8 calibration + 24 generation + 24 judge attempts.
5. Tests hiện tại gọi helper khác production path và thiếu hard-cap/linkage
   matrix.

Yêu cầu bắt buộc:
- Một canonical calibration resume path: locate final/partial bằng frozen run ID,
  raw-validate trước map, validate summary nếu có, rebuild missing summary zero
  calls. Không để CLI dùng branch khác test.
- Budget schema require complete totals; validate model/stage/case/status và
  exact recomputed totals/caps fail closed.
- Tạo shared pure validator đối chiếu mọi calibration/generation/judge row với
  exact budget attempt IDs, costs và stage distribution. Row sau resume phải
  include prior journal attempts, không chỉ attempts của process hiện tại.
- Cell 15 gọi shared validators, bind full identity gồm calibration_run_id,
  schema, limits và exact totals.
- Thêm toàn bộ 12 nhóm tests trong Codex review, đặc biệt production CLI
  final-without-summary, 56-call composition, slots 57-64, attempt 65, orphan/
  duplicate/wrong-stage links và full notebook tamper matrix.
- Giữ 141 tests hiện tại xanh; chạy py_compile, targeted pytest, validator,
  notebook hygiene, git diff --check, codegraph status và read-only Qdrant count.
- Không đổi scope/model/data/pricing/rubric, không sửa unrelated dirty files,
  không commit/push, không paid calls.

Trước khi tuyên bố hoàn thành, tự audit từng requirement bằng source line và test
name. Cập nhật implementation report thành Revision 10 với output thực và xác
nhận 0 paid calls. Nếu thiếu bất kỳ invariant/test nào, báo blocker thay vì nói
đã hoàn thành. Sau đó dừng để Codex re-review.
```

## Governance

Architect-review đánh giá impact của các findings là High đối với reliability và
auditability của paid evaluation package. Active Qdrant chỉ được đọc; reviewer
không mở/in `.env`. Sau pure re-review đạt mới re-verify official pricing và xin
exact user authorization. Phase 8 tiếp tục `not_ready`.
