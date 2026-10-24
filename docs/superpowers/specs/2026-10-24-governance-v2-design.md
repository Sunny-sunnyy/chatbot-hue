# Governance v2 — cách làm việc A/B/C: thiết kế + kế hoạch

**Date:** 2026-10-24 (+07)
**Status:** Approved by User 2026-10-24; review chéo B `reports/governance_v2_cross_review_2026_10_24.md` (4 major + 6 minor đã sửa)
**Owner:** A (điều phối, Claude Opus 5.5)
**Loại:** governance, chỉ đổi tài liệu; không đổi code, dữ liệu, requirement Phase
**Tài liệu gộp:** thiết kế + kế hoạch + tiêu chí nghiệm thu (áp dụng ngay quy tắc
"một tài liệu, duyệt một lần" của chính bản này)

## 1. Vì sao đổi

Quan sát ngày 2026-10-24:

| Vấn đề | Bằng chứng |
|---|---|
| Mỗi session phải đọc quá nhiều | Bootstrap Reviewer: `Session_Prompt.md` 436 + `REVIEWER_WORKFLOW.md` 333 + `Project_Status.md` 760 + 2 skill 492 ≈ **2.000 dòng**; `Project_Status.md` khoảng 2/3 là lịch sử |
| Một quy tắc viết nhiều nơi | Thứ tự nguồn sự thật, cấm mock, đơn giản, dùng lại evidence, chọn verification lặp ở `Session_Prompt`, hai workflow và hai skill |
| Quy tắc phối hợp lỗi thời | "User chuyển tiếp giữa các session, không gửi tool message"; tên Codex/Gemini, `~/.codex/skills`, `TEMPLATE_CODEX_REVIEW` |
| Không chạy song song được | "Tối đa một nhiệm vụ đang hoạt động" trong một `CURRENT_HANDOFF.md` |
| Thủ tục không theo rủi ro | Mọi Phase đều spec riêng + plan riêng, duyệt hai lần |
| Session mới phụ thuộc người điều phối | Không có nơi giữ ngữ cảnh riêng của từng session |

## 2. User đã chốt (2026-10-24)

1. Mô hình **A điều phối + review chéo**. User chỉ làm việc với A; A giao việc, điều
   phối B, C. Cả ba dùng Opus 5.5.
2. **Quy trình theo rủi ro**; gộp spec + plan thành một tài liệu.
3. Lịch sử rút khỏi `Project_Status.md` sang `PROJECT_HISTORY.md` (nguyên văn,
   không xóa); đặt quy tắc viết status.
4. Mỗi session có file ngữ cảnh riêng; vẫn giữ report agent và report cho User;
   giữ `reports/`.
5. Mang skill `propose-options` từ Mekong sang, chỉnh cho hue_rag; xóa
   `karpathy-guidelines`.
6. Duyệt chi phí/dữ liệu cho A đồng nghĩa duyệt cho B, C.
7. A, B, C được tự cải tiến, tự tối ưu, tự đóng gói trong phạm vi đã duyệt.

## 3. Vai trò

| Session | Việc |
|---|---|
| **A — điều phối** | Trò chuyện, brainstorm, thiết kế với User; viết tài liệu thiết kế; giao việc B/C; review chéo; tự làm việc nhỏ; cập nhật status/history/handoff; commit/push |
| **B, C — thực thi** | Làm việc A giao; tự kiểm; viết report; review chéo khi A giao; đề xuất cải tiến có bằng chứng; hỏi A, không hỏi User |

- **Tên là vai, không phải model.** Codex/agy hay Claude đều mở bằng cùng
  `START_SESSION.md`, chỉ đổi `<X>`.
- **Review chéo:** ai làm thì người khác kiểm. A kiểm B/C; khi A tự sửa code hoặc
  dữ liệu, B hoặc C kiểm A. Người được kiểm được phản biện bằng bằng chứng; bất
  đồng không ngã ngũ thì A trình User kèm khuyến nghị.
- **Quyền:** User duyệt qua A. Quyền A ghi trong `CURRENT_HANDOFF.md` hoặc tin nhắn
  là quyền User đã duyệt; B/C không xin lại User. Việc ngoài quyền đã ghi: dừng,
  nhắn A. (Mỗi session vẫn tôn trọng quy tắc an toàn của chính nó; User xác nhận
  một lần trong terminal của session đó nếu session yêu cầu.)
- **Liên lạc:** SendMessage giữa session; file trong repo là nguồn sự thật, tin
  nhắn chỉ báo "có việc / đã xong / vướng".

## 4. Quy trình theo rủi ro

| Mức | Ví dụ | Trước khi làm | Sau khi làm |
|---|---|---|---|
| **Cao** | Phase mới; sửa dữ liệu curated; xóa collection; provider/model mới; gửi dữ liệu ra ngoài; quyết định chất lượng | Brainstorm với User (`propose-options`) → **một** tài liệu thiết kế (mục tiêu, quyết định, phạm vi, bước, tiêu chí, quyền, rủi ro) → User duyệt một lần | Report + review chéo độc lập + User đóng (theo gate nếu có) |
| **Trung bình** | Sửa code trong Phase đã duyệt; dọn code/notebook; test; tài liệu governance nhỏ | A ghi việc trong `CURRENT_HANDOFF.md` (mục tiêu, phạm vi, tiêu chí, quyền); User chỉ cần duyệt khi việc chưa nằm trong phạm vi đã duyệt | Report ngắn + review chéo; A đóng, báo User |
| **Thấp** | Sửa chữ, cập nhật status, chạy kiểm tra chỉ đọc | Tự làm | Ghi vào STATUS/HISTORY |

Chi tiết kỹ thuật trong phạm vi đã duyệt: A tự quyết, ghi lý do. Chỉ hỏi User
về phạm vi, dữ liệu, tiền, thao tác phá hủy, hoặc khi bằng chứng đi ngược quyết
định trước.

### 4.1 Cách giảm rủi ro (áp dụng ở mọi mức)

1. **Đích tách biệt, cutover sau:** build vào tên mới, kiểm xong mới chuyển
   runtime (như 7A2); không sửa tại chỗ dữ liệu đang chạy.
2. **Sao lưu trước khi sửa/xóa:** corpus copy vào `knowledge-base-hue/meta/`;
   collection còn giá trị dùng Qdrant snapshot trước khi xóa; commit Git trước
   khi sửa code lớn.
3. **Liệt kê trước khi xóa:** in danh sách đích thật, đối chiếu với danh sách
   duyệt, khác thì dừng.
4. **Bước nhỏ có điểm dừng:** gate, điều kiện dừng ghi trước; lỗi provider là kết
   quả, dừng và báo.
5. **Giới hạn tiền ghi trong việc:** số build/call tối đa; vượt thì hỏi.
6. **Song song an toàn:** mỗi session khai báo file đang sửa trong STATUS của
   mình; không sửa file session khác đang khai báo; code song song dài ngày dùng
   `git worktree` riêng.
7. **Tiêu chí ghi trước khi chạy**, bằng chứng từ hệ thống thật, review chéo.

## 5. Tài liệu

| File | Chứa gì | Ai ghi | Quy tắc |
|---|---|---|---|
| `session_prompt/START_SESSION.md` (mới) | Prompt mở session chung, thứ tự đọc, kiểm nhanh chỉ đọc | A | Mọi session mở bằng file này |
| `session_prompt/Session_Prompt.md` | **Luật chung duy nhất**: phạm vi, giao tiếp, nguồn sự thật, quyền, an toàn/bí mật, bằng chứng, đơn giản, test, môi trường `uv`, curated data | A | Mỗi quy tắc chỉ viết ở đây; nơi khác trỏ tới |
| `session_prompt/WORKFLOW.md` (mới, thay hai workflow) | Cách làm: mở session, nhận việc, khai báo, làm, tự kiểm, review chéo, report, kết phiên; mục riêng "Việc thêm của A" | A | `REVIEWER_WORKFLOW.md`, `IMPLEMENTER_WORKFLOW.md` thành một dòng trỏ (giữ link lịch sử) |
| `session_prompt/Project_Status.md` | Hiện trạng (mục 6) | A | Chỉ hiện trạng |
| `session_prompt/PROJECT_HISTORY.md` (mới) | Lịch sử chuyển nguyên văn từ status + mục mới theo ngày | A | Mục mới ở trên; chỉ thêm, không sửa mục cũ |
| `session_prompt/CURRENT_HANDOFF.md` | Bảng session (tên terminal, vai, việc, trạng thái), quyền hiện hành, **một mục việc cho mỗi session** (đọc gì, làm gì, không làm gì, tiêu chí, đầu ra, điều kiện dừng) | A viết phần giao; B/C chỉ sửa trạng thái phần của mình | Việc xong chuyển tóm tắt sang HISTORY; file chỉ giữ việc đang mở |
| `session_prompt/sessions/STATUS_A.md`, `STATUS_B.md`, `STATUS_C.md` (mới) | Ngữ cảnh riêng: đang làm, file đang khai báo sửa, vừa xong, điều đã học/bẫy, việc dở, câu hỏi cho A | Chính session đó | Ghi đè, ngắn (≤ ~60 dòng); cập nhật khi xong một việc và trước khi kết phiên |
| `session_prompt/TEMPLATE_*.md` | Implementation report, review (đổi tên từ `TEMPLATE_CODEX_REVIEW.md`), user report | A | Giữ ngắn |
| `reports/` | Report agent (implementation + review mỗi gate), `reports/user_reports/` (report cho User khi đóng Phase), survey | Người làm / người kiểm | Giữ nguyên file cũ, không di chuyển; tên `phase_<x>_<gate>_<loại>_<ngày>.md` |

Memory Claude dùng chung cho cả ba session (cùng thư mục dự án): chỉ ghi điều
lâu dài, không ghi trạng thái việc (trạng thái nằm ở STATUS/HANDOFF).

### 5.1 Skills

| Skill | Thay đổi |
|---|---|
| `practical-project-coding` | Giữ; bỏ phần lặp với `Session_Prompt` (thứ tự nguồn sự thật), giữ phương pháp code/test |
| `risk-gated-agent-review` | Viết lại gọn theo review chéo A/B/C (người làm / người kiểm), bỏ handoff field và quy định Reviewer–Implementer cũ; giữ tên thư mục để không gãy link |
| `propose-options` (mới) | Từ Mekong: phương án bằng lời thường + đổi gì, tốn gì, khi nào sai, chọn khác mất gì, câu tự kiểm; brainstorm mỗi lần một câu có đáp án. Bỏ phần CEO/intern; thay `session_prompt/brainstorming.md` (thành dòng trỏ) |
| `karpathy-guidelines` | Xóa (trùng `practical-project-coding`, không workflow nào dùng) |

Đặt skill dự án trong `skills/`, symlink vào `.claude/skills/` (đã có cho hai
skill; thêm `propose-options`).

## 6. Quy tắc viết `Project_Status.md`

1. **Chỉ hiện trạng.** Mỗi sự thật một chỗ. Quyết định bị thay thì sửa tại chỗ,
   bản cũ chuyển sang HISTORY kèm ngày.
2. **Mục cố định:** (1) tổng quan; (2) Phase hiện tại và mốc kế tiếp; (3) bảng
   Phase; (4) runtime và dữ liệu đang chạy (collection, model, cấu hình); (5)
   quyết định đang hiệu lực, mỗi dòng có ngày + link; (6) ranh giới an toàn;
   (7) bản đồ tài liệu đang dùng; (8) bẫy kỹ thuật đã biết.
3. Không chép report, chỉ link. Không ghi việc kế tiếp (thuộc HANDOFF).
4. Hướng tới 200–300 dòng (định hướng, không cứng).
5. A cập nhật khi đóng gate/Phase hoặc khi quyết định đổi, kèm một mục HISTORY:
   ngày, việc đã đóng, link evidence chính, quyết định đã đổi.

## 7. Kế hoạch thực hiện

| Bước | Ai | Việc |
|---:|---|---|
| 1 | A | Viết bản này; B đọc phản biện (sau Gate 3) |
| 2 | User | Duyệt bản này |
| 3 | A | Tách `Project_Status.md`: hiện trạng giữ lại theo mục 6, phần còn lại chuyển nguyên văn sang `PROJECT_HISTORY.md` |
| 4 | A | Viết `START_SESSION.md`, `WORKFLOW.md`; rút gọn `Session_Prompt.md` thành luật chung duy nhất; hai workflow cũ và `brainstorming.md` thành dòng trỏ |
| 5 | A | Viết lại `risk-gated-agent-review`, tỉa `practical-project-coding`, thêm `propose-options` (+ symlink), xóa `karpathy-guidelines`; đổi tên template review |
| 6 | A | `CURRENT_HANDOFF.md` theo dạng bảng session; tạo `sessions/STATUS_A.md`; B tự viết `STATUS_B.md` |
| 7 | B | Review chéo toàn bộ diff (mục 8) |
| 8 | User mở C | C mở bằng `START_SESSION.md` — đây là kiểm thử cuối; C tự tạo `STATUS_C.md` |
| 9 | A | Commit/push; mục HISTORY "Governance v2" |

Không đổi trong đợt này: code, dữ liệu, spec/plan/report cũ, `handoff_prompt/`.

## 8. Tiêu chí nghiệm thu

1. Tổng số dòng một session bắt buộc đọc khi mở (START_SESSION + Session_Prompt +
   WORKFLOW + Project_Status + CURRENT_HANDOFF + STATUS của mình) **≤ khoảng 1.000
   dòng** (hiện ≈ 2.000).
2. **Không mất thông tin:** mọi dòng bị bỏ khỏi `Project_Status.md` có trong
   `PROJECT_HISTORY.md` hoặc vẫn còn trong status (B kiểm bằng diff).
3. Mỗi quy tắc chung xuất hiện một chỗ; không còn quy tắc "User chuyển tiếp"/"một
   handoff duy nhất"; Codex/Gemini chỉ còn trong lịch sử.
4. C mở bằng `START_SESSION.md`, không cần A giải thích thêm, báo đúng: mình là ai,
   Phase/việc hiện tại, quyền, việc của mình.
5. `git diff --check` sạch; link trong tài liệu mới trỏ đúng file tồn tại.

## 9. Rủi ro

| Rủi ro | Cách xử lý |
|---|---|
| Rút gọn làm mất quy tắc quan trọng | Tiêu chí 2–3; B kiểm diff từng quy tắc bị bỏ: chuyển chỗ hay bỏ có chủ đích |
| Đổi quy trình giữa Gate 3 | Gate 3 chạy theo handoff hiện tại; áp dụng v2 từ việc kế tiếp |
| Ba session sửa cùng file | Khai báo file trong STATUS; tài liệu governance chỉ A sửa |
| `CURRENT_HANDOFF.md` phình như Mekong (707 dòng) | Việc xong chuyển sang HISTORY ngay khi đóng |
