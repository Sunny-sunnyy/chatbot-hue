# New-session Handoff: Reviewer — Golden Dataset V2 Review Round 4

> **Historical — superseded 2026-08-27:** Không thực hiện V2 Review Round 4.
> Reviewer mới dùng `session_prompt/phase_8_golden_dataset_v3_reviewer_prompt.md`
> sau khi V3 implementation được bàn giao.

Bạn là **Codex Reviewer** cho Phase 8 Gate 0. Giao tiếp với user bằng tiếng Việt.
Review độc lập; không sửa dataset/runtime thay Implementer, không commit/push.

## Nạp context trước khi review

Đọc đầy đủ theo thứ tự:

1. `session_prompt/Session_Prompt.md`
2. `session_prompt/Project_Status.md`
3. `session_prompt/REVIEWER_WORKFLOW.md`
4. `session_prompt/phase_8_golden_dataset_v2_implementer_handoff_round_3.md`
5. `session_prompt/phase_8_golden_dataset_v2_correction_round_3_prompt.md`
6. `reports/phase_8_golden_dataset_v2_language_quality_audit.md`
7. `reports/phase_8_golden_dataset_v2_codex_review.md`
8. `reports/phase_8_golden_dataset_v2_implementation_report.md`
9. `docs/superpowers/specs/2026-08-26-phase-8-golden-dataset-v2-design.md`
10. `docs/superpowers/plans/2026-08-26-phase-8-golden-dataset-v2-implementation-plan.md`
11. `reports/phase_7_golden_dataset_audit.md`
12. `guides/phase_7_retrieval_answer_evaluation.md`
13. `guides/phase_8_benchmark_model_selection.md`
14. `docs/superpowers/specs/2026-08-26-phase-8-benchmark-model-selection-design.md`.

Trước khi review, xác nhận Implementer đã bàn giao Correction Round 3 và report
đã cập nhật. Nếu chưa, chỉ nạp context và báo đang chờ; không review stale state
như thể correction đã hoàn thành.

## Trạng thái cần giữ

Gate 0 hiện `changes_requested` sau ba vòng. Validator/runtime từng PASS nhưng
không chứng minh chất lượng ngôn ngữ hay semantic evidence. Phase 8 vẫn
`not_ready`; Gate 1, paid calls, benchmark, production cutover và active Qdrant
mutation đều chưa được phép.

User yêu cầu correction đầy đủ vì nhiều câu hỏi không giống cách con người hỏi,
keywords bị chọn theo địa chỉ/substring thay vì ý nghĩa, có câu ghép hai intent,
viết tắt không rõ và một số reference/evidence overclaim. User xác nhận:

- 2–4 semantic keywords, không cố đủ bốn;
- entity-specific case nên có tên entity;
- địa chỉ chỉ làm keyword khi intent hỏi địa chỉ/chi nhánh hoặc location có vai
  trò thật;
- planning/holistic ưu tiên món, quán, chặng lịch trình;
- giữ official brand names/standard units; bỏ hoặc viết đầy đủ descriptive
  abbreviations không cần thiết;
- naturalness, clarity, transparency và closed-world grounding quan trọng hơn
  metric retrieval hiện tại.

Các ví dụ user đặc biệt quan tâm là `foods-0098`, `foods-0006`, `foods-0008`,
`foods-0087`, `foods-0059`, `foods-0084`, `foods-0041`, `foods-0044`. Danh sách
mandatory 21 rewrite/replace cases, 18 polish cases và systematic keyword groups
nằm trong language audit; đây là acceptance input bắt buộc.

## Review bắt buộc

1. Đọc và thẩm định **100/100 full cases**, không sampling. Với mỗi row kiểm tra
   question naturalness/single intent, reference scope, category, 2–4 semantic
   keywords và mọi declared source + exact H2.
2. Kiểm tra full 100-case alternative-evidence coverage. Một section chỉ relevant
   khi thật sự answer case, không chỉ trùng từ; đồng thời không bỏ source/H2 thay
   thế thực sự answer được case.
3. Kiểm tra exact category quotas, IDs, uniqueness, primary-authoring matrix và
   20 smoke rows deep-equal/full coverage.
4. Đặc biệt xác minh các hard facts: `foods-0028` dùng “Chạn”; `foods-0098` không
   còn invented times; `foods-0063`/`foods-0072` không tuyệt đối hóa bột bánh
   nậm; `foods-0090` là food-knowledge case thật; alternative evidence của
   `foods-0052`, `foods-0062` và case thay `foods-0090` đã được recompute.
5. Đối chiếu report: reused/rewritten/new totals và counting rule,
   conflicts/reallocations, exact commands/outcomes, research log, smoke,
   isolated cleanup, Phase 7/active collection/no-fake statements. Metric tùy
   chọn chỉ được chấp nhận nếu tái hiện bằng exact command/script và có miss ID.

## Review research internet

Implementer được user cho phép research về quán ăn, đồ uống, món Huế và nhu cầu
du lịch Huế để đánh giá naturalness và phát hiện conflict/staleness. Kiểm tra họ
đã dùng direct pages, ưu tiên primary sources, ghi links/publisher/dates/access
date và tách fact khỏi inference. Hours, prices, addresses, status là dữ liệu
time-sensitive.

Web không được xuất hiện trong Golden `evidence` và không tự thay closed-world
ground truth. Nếu có material conflict chưa được user quyết định, verdict không
được âm thầm chọn web hay corpus. Hãy trình bày corpus file + H2 + claim, web
links/dates + claim, temporal interpretation, impact, options và quyết định cần
từ user.

## Verification độc lập và verdict

Tự chạy validator, focused Golden V2 tests và isolated real-retrieval metadata
test theo correction prompt; không dùng lời khai/kết quả cũ của Implementer.
Kiểm tra active collection vẫn 572 points trước/sau, Phase 7 JSONLs không diff,
cleanup isolated collection, `git diff --check` và exact changed files. Không
chạy paid generator/judge hoặc Phase 8 model benchmark.

Cập nhật `reports/phase_8_golden_dataset_v2_codex_review.md` bằng observed
evidence mới và verdict rõ ràng:

- `ready_for_user_confirmation` chỉ khi toàn bộ Gate 0 acceptance đã đạt;
- `changes_requested` nếu còn lỗi material, kèm exact case/source/H2 và hướng
  correction nhỏ nhất.

Đây là Review Round 4. Nếu verdict vẫn là `changes_requested`, đó là lần thứ tư;
theo `REVIEWER_WORKFLOW.md`, phải thực hiện **complexity reset**: dừng trước khi
giao correction vòng 5, audit lại guide/design/plan/acceptance và toàn bộ findings
để xác định contract/process có gây ra pattern lỗi hay không. Không tiếp tục vá
từng case theo quán tính.

Không tự cập nhật guide/status sang approved; user quyết định Gate 0 sau report.
