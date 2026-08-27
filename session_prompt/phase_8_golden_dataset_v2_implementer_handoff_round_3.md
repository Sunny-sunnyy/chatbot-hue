# New-session Handoff: Implementer — Golden Dataset V2 Correction Round 3

> **Historical — superseded 2026-08-27:** Không dùng handoff này cho session
> mới. User đã duyệt Golden Dataset V3 complexity reset.

Bạn là **Implementer** cho Phase 8 Gate 0. Giao tiếp với user bằng tiếng Việt.
Không tự approve phase, không sửa Codex review/guide/status, không commit/push.

## Nạp context trước khi làm

Đọc đầy đủ theo thứ tự:

1. `session_prompt/Session_Prompt.md`
2. `session_prompt/Project_Status.md`
3. `session_prompt/IMPLEMENTER_WORKFLOW.md`
4. `session_prompt/phase_8_golden_dataset_v2_correction_round_3_prompt.md`
5. `reports/phase_8_golden_dataset_v2_language_quality_audit.md`
6. `reports/phase_8_golden_dataset_v2_codex_review.md`
7. `reports/phase_8_golden_dataset_v2_implementation_report.md`
8. `docs/superpowers/specs/2026-08-26-phase-8-golden-dataset-v2-design.md`
9. `docs/superpowers/plans/2026-08-26-phase-8-golden-dataset-v2-implementation-plan.md`
10. mọi Markdown H2 source dùng hoặc cân nhắc làm evidence cho case được sửa.

Chạy `git status --short` trước khi sửa và giữ nguyên mọi thay đổi ngoài scope.
Implementation hiện đã tồn tại trong dirty worktree; không làm lại từ đầu.

## Trạng thái và mục tiêu

Gate 0 đang `changes_requested` sau Reviewer vòng 3. Validator và runtime tests
đã PASS nhưng manual audit phát hiện pattern chất lượng trên toàn dataset. Hãy
thực hiện **một correction hợp nhất trên đủ 100/100 cases**, không chỉ sửa các ví
dụ user nêu và không tối ưu gold theo retrieval model hiện tại.

Rubric user đã xác nhận:

- câu hỏi phải tự nhiên như một người thật hỏi trợ lý ẩm thực/du lịch Huế;
- mỗi câu có một intent chính, không ghép hai việc không liên quan;
- keywords là 2–4 semantic anchors, không cố đạt đủ bốn;
- câu về quán/entity phải ưu tiên tên quán/entity;
- địa chỉ chỉ nên là keyword khi hỏi trực tiếp địa chỉ, chi nhánh hoặc thông tin
  cần location để phân biệt;
- planning/holistic nên dùng tên món, tên quán hoặc chặng lịch trình thay vì bốn
  địa chỉ;
- giữ tên thương hiệu chính thức như `AEON MALL`, `KOI Thé`, `ANH KAFE` và đơn
  vị chuẩn như `VNĐ`, `g`, `ml`; loại hoặc viết đầy đủ các viết tắt mô tả không
  cần thiết như `CNN`, `BBQ`, `TTTM`, `TP`;
- question, reference, category, keywords và evidence phải rõ ràng, minh bạch,
  đúng trọng tâm và grounded trong closed-world corpus.

Phải xử lý tối thiểu nhóm rewrite/replace:

`foods-0008`, `foods-0023`, `foods-0028`, `foods-0039`, `foods-0040`,
`foods-0044`, `foods-0053`, `foods-0054`, `foods-0059`, `foods-0062`,
`foods-0063`, `foods-0072`, `foods-0073`, `foods-0075`, `foods-0080`,
`foods-0083`, `foods-0084`, `foods-0087`, `foods-0090`, `foods-0098`,
`foods-0100`.

Phải polish tối thiểu:

`foods-0027`, `foods-0036`, `foods-0037`, `foods-0042`, `foods-0055`,
`foods-0056`, `foods-0065`, `foods-0067`, `foods-0079`, `foods-0081`,
`foods-0082`, `foods-0085`, `foods-0086`, `foods-0088`, `foods-0089`,
`foods-0092`, `foods-0095`, `foods-0097`.

Sau đó audit keywords và alternative evidence cho toàn bộ 100 cases. Các ví dụ
quan trọng từ user: `foods-0098` không dùng bốn địa chỉ làm keyword và bỏ giờ
không có source; `foods-0008` không hỏi lại thông tin đã nằm sẵn trong tên quán;
`foods-0087` dùng tên món/quán thay địa chỉ; `foods-0059` bỏ `CNN`; `foods-0084`
không ghép danh sách món với kiến thức nước dùng; `foods-0041` phải có `DeChill`;
`foods-0044` phải hỏi KOI Thé nằm ở đâu trong AEON MALL Huế.

Các lỗi hard-grounding bắt buộc: `foods-0028` là Nhà hàng cơm niêu **Chạn**;
`foods-0063`/`foods-0072` không tuyệt đối hóa mọi bánh nậm dùng bột gạo tẻ;
`foods-0090` phải là food-knowledge case thật và vẫn giữ matrix; recompute
evidence của case này. Audit alternative evidence đầy đủ, tối thiểu xem lại
`foods-0052` và `foods-0062` theo audit canonical.

## Quyền research internet do user cấp

Bạn được phép research quán ăn, quán cà phê, đồ uống, món Huế và nhu cầu của du
khách tại Huế; có thể kiểm tra tên, địa chỉ, giờ mở cửa, giá, menu, lịch sử,
mô tả món và mức phù hợp với lịch trình. Mục đích chỉ là:

1. kiểm tra câu hỏi/thuật ngữ có tự nhiên không;
2. phát hiện ambiguity, mâu thuẫn hoặc thông tin có thể đã cũ;
3. chuẩn bị báo cáo và thảo luận với Reviewer/user.

Phải mở trang thật, ưu tiên nguồn chính thức/primary, ghi direct link,
publisher, publication/update date nếu có và access date. Với conflict quan
trọng, ưu tiên nguồn chính thức hoặc đối chiếu hai nguồn độc lập đáng tin cậy.
Phân biệt fact quan sát được với inference.

Web **không** là Golden evidence và không tự thay thế corpus. Không đưa external
fact vào reference/keywords/evidence nếu user chưa phê duyệt riêng việc cập nhật
curated corpus. Nếu web và corpus mâu thuẫn, dừng checkpoint và báo: case ID,
corpus file + H2 + claim, web links + dates + claim, khả năng khác biệt theo
thời gian, ảnh hưởng, các phương án và đúng một quyết định cần user/Reviewer.

## Scope sửa và nghiệm thu

Chỉ sửa khi cần:

- `knowledge-base-hue/foods/evaluation/golden_v2.jsonl`
- `knowledge-base-hue/foods/evaluation/golden_v2_smoke.jsonl`
- `reports/phase_8_golden_dataset_v2_implementation_report.md`

Không sửa validator/runtime/tests nếu chưa báo một contract defect thật. Giữ IDs,
unique questions, exact category quotas, exact 40/20/20/20 authoring matrix,
smoke deep-equal, Phase 7 JSONLs byte-for-byte và active Qdrant read-only. Không
chạy paid calls, Phase 8 benchmark, model comparison hoặc active mutation.

Thực hiện exact verification trong consolidated correction prompt. Report phải
ghi changed IDs, keyword-pass 100/100, reused/rewritten/new theo counting rule,
conflicts/reallocations, research sources/findings, exact observed commands,
smoke deep-equality, isolated cleanup, Phase 7/active collection/no-fake safety.
Nếu nêu Hit/MRR/NDCG phải có exact reproducible command/script và miss ID.

Kết thúc bằng `git diff --check`, `git status --short` và bàn giao cho Reviewer.
Không tuyên bố Gate 0 approved.
