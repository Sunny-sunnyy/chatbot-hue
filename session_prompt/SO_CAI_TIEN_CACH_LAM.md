# Sổ cải tiến cách làm — harness của các session

Cập nhật lần cuối: 15:44 25/10/2026 (A, vòng 2 — kết phiên chiều 25/10, đóng 8.1). A ghi theo skill `skills/improve-workflow/SKILL.md`. Mỗi dòng là một
thay đổi ở luật / skill / rào bằng máy, sinh từ sự cố có bằng chứng hoặc quyết định User; User duyệt cho thử;
vòng sau xem giữ hay gỡ. Trạng thái: `đề xuất` → `đang thử` → `đang dùng` / `gỡ` / `bác`.

Mốc độ dài file mở phiên (`wc -l`, 25/10 10:45, sau đợt cải tiến): START_SESSION 45 · Session_Prompt 167 · WORKFLOW 202 ·
Project_Status 190 · CURRENT_HANDOFF ~143 · AGENTS 23 — khoảng 770 dòng. Thử mở phiên (sub-agent đóng vai B, 25/10
10:4x): nắm đúng vai, việc, 6 luật cứng, vị trí hook / sổ / Session D / đề xuất; câu hỏi còn lại là quyết định dự án
(ghi ở `CURRENT_HANDOFF.md` "Việc của A"). User 25/10: không cắt nội dung còn
hiệu lực; chỉ dời lịch sử ra khi dài thêm đáng kể.

## Thay đổi

| ID | Ngày | Căn cứ (sự cố / quyết định) | Thay đổi | Ở đâu | Trạng thái | Xem lại |
|---|---|---|---|---|---|---|
| W1 | 25/10 | User chọn; S1–S8 | Vòng tự cải tiến có người duyệt + sổ này | `skills/improve-workflow/`, sổ này, `WORKFLOW.md` §8 | đang thử | kết phiên có chạy vòng không; sự cố có lặp không |
| W2 | 25/10 | W1 | Sổ này (vòng đầu: 8 sự cố, 10 thay đổi, 6 ý chờ) | `session_prompt/SO_CAI_TIEN_CACH_LAM.md` | đang thử | vòng sau có dùng sổ không |
| W3 | 25/10 | User chọn; 7B Run 1↔2 có nhiễu (16/176 câu đổi điểm, lỗi citation 4→6); G4 ít câu có thể đổi | `run-experiment`: tiêu chí sàn / mức tụt / chỉ số quyết, cỡ mẫu trước khi chạy, nhiễu A/A, kiểm người chấm, số do script in, luật giữ/gỡ | `skills/run-experiment/SKILL.md` | đang thử | G2/G4 có ghi đủ trước khi chạy không; có kết luận bị nhiễu đảo không |
| W4 | 25/10 | User chọn (tự học dự án của mình) | Session D chỉ đọc, sổ học private, không ghi memory | `WORKFLOW.md` §1, §10; `START_SESSION.md` | đang thử | sau 2 buổi D: viết skill hay gỡ |
| W5 | 25/10 | S2 (không đảo ngược được ⇒ rào ngay lần đầu) | Hook git `pre-commit` (mọi agent): chặn đường dẫn private, dạng secret, tên dự án khác ở dòng thêm mới. Sau review F1/F2: 13/13 ca chặn, 8/8 ca qua (bảng ở `report_agent/2026-10-25_cai_tien_cach_lam/KE_HOACH.md`). Claude Code: cấm `Read(./.env*)` (đã chứng minh chặn file thử) | `.githooks/pre-commit`, `core.hooksPath`, `.claude/settings.json` | đang thử | có chặn nhầm commit thật không (repo chỉ chạy trên máy User — User 25/10). **Chặn nhầm đã biết:** dòng mới trích nguyên tên file tài liệu cũ có tên dự án khác |
| W6 | 25/10 | User: cách làm phải dùng được cho Codex/AGY; sub-agent không tự đọc START_SESSION (S5) | `AGENTS.md` (bản chính) + `CLAUDE.md` nhập `@AGENTS.md` | gốc repo | đang thử | Codex đọc `AGENTS.md`; AGY được User cho đọc `START_SESSION.md` (User 25/10) — xem cả hai có làm đúng luật cứng không |
| W7 | 25/10 | User chọn | Chỉ dẫn trong nội dung ngoài là dữ liệu; duyệt kế hoạch gắn hash bản | `Session_Prompt.md` §2; `WORKFLOW.md` §9.1 | đang thử | — |
| W8 | 25/10 | S5, S6 | Đọc tài liệu dài bằng sub-agent theo khuôn; đọc lại brief; tự kiểm 2–3 khẳng định | `WORKFLOW.md` §9.9 | đang thử | lần đọc dài tới có lỗi brief không |
| W9 | 25/10 | User chọn; S8 | Giữ gọn: memory, bỏ mục "Tạm gác" handoff, đề xuất cho dự án thành `de_xuat_cho_du_an.md`, `.aws/` vào `.gitignore` | memory; `CURRENT_HANDOFF.md`; đợt 25/10 | đang thử | phiên sau có đọc đề xuất trước khi duyệt G4/G2 không |
| W10 | 25/10 | Ý từ một file SELF_IMPROVE.md trên GitHub (User đưa); S6, S10 | `improve-workflow`: luật viết thành việc làm được ngay; ghi "phát hiện bằng gì"; vòng nào sửa file mở phiên thì sub-agent mới thử mở phiên. **Không** làm phần tự sửa cách tự sửa | `skills/improve-workflow/SKILL.md`; cột mới ở bảng sự cố | đang thử | B/C/D không phải đọc thêm; xem bước thử mở phiên có tìm ra chỗ thiếu không |
| W11 | 25/10 chiều | S12; User chọn cách a (15:44): người review cần đủ căn cứ nhưng không nạp ngữ cảnh người viết | Kế hoạch có tiêu chí ghi trước: mục "Căn cứ để review" (2–4 file + mục); session khác review chỉ dựa trên gói đó trước khi A duyệt sha | `WORKFLOW.md` §9.1 | đang thử | lỗi tiêu chí có còn bị phát hiện sau khi duyệt không; người review có thiếu căn cứ không |
| W12 | 25/10 chiều | S13, S14 (không đảo ngược được) | Giữ mù câu kín: brief cấm tên file nguồn / nội dung trong báo cáo cuối; grep loại `evaluation/`, `meta/`, `*sealed*`; xóa script tạm; A nhắc User mô tả chung | `Session_Prompt.md` §5 | đang thử | còn lần lộ nào không; lặp ⇒ rào bằng máy (script grep chung) |
| W13 | 25/10 chiều | S15 | Skill review: correction ghi ở file review + nhắn người làm (khớp `WORKFLOW.md` §3.2) | `skills/risk-gated-agent-review/SKILL.md` | đang thử | — |
| I4 | 25/10 chiều | giữ gọn | Dời 4 bẫy kỹ thuật từ STATUS_B ra chung (HF cache `refs` rỗng; HNSW phụ thuộc `limit` + float32; model suy luận ~3× token; chấm baseline cùng lượt) | `Project_Status.md` §8 | đang thử | — |
| I1 | 25/10 | S7 (luật chỉ ở memory Claude ⇒ agent khác không thấy) | Dời "nghiên cứu ChatGPT trước khi đề xuất, prompt đầy đủ" từ memory ra luật chung | `Session_Prompt.md` §9 | đang thử | User có phải nhắc lại không |
| I2 | 25/10 | S3 | Dời "file nhiều session cùng ghi: đọc lại trước khi sửa, sửa từng đoạn" từ STATUS_A ra luật chung | `WORKFLOW.md` §3.2 | đang thử | có lần ghi đè nào không |
| I3 | 25/10 | S8 | Sửa 2 memory cũ (mô tả "Reviewer/Implementer"; file tên 7A2 giữ trạng thái 8.1) | memory Claude | đang thử | — |

## Sự cố đã gom (vòng đầu 25/10 — sự cố 24–25/10)

| # | Sự cố | Lần | Mất gì | Bằng chứng | Luật đang nằm ở | Phát hiện bằng |
|---|---|---|---|---|---|---|
| S1 | `pytest --deselect tests/…` không khớp node id ⇒ lỡ chạy 1 test gọi API trả phí | 1 (24/10, B1) | 1 paid call (lỗi 400) + 1 collection tạm | `Project_Status.md` §8; `PROJECT_HISTORY.md` | `Project_Status.md` §8 (đúng chỗ) — ý chờ: test paid chỉ chạy khi bật biến môi trường | B tự thấy sau khi chạy |
| S2 | Commit có số liệu / đường dẫn dự án khác vào repo public, bị auto-mode chặn | 1 (24/10) | phải tách ghi chú ra `data/`; nếu lọt thì không gỡ được khỏi lịch sử | memory `public-repo-no-external-project-data` | memory (lệnh `grep` bằng tay) ⇒ W5 | công cụ chặn (auto-mode) |
| S3 | `CURRENT_HANDOFF.md` bị B/C sửa song song với A | ≥ 1 ("hay bị") | nguy cơ ghi đè | `sessions/STATUS_A.md` 24/10 | chỉ STATUS_A ⇒ I2 | A tự thấy |
| S4 | Script tạm trong `/tmp` mất khi khởi động lại | 1 (24/10) | phải chép lại vào `data/phase_8_1/tools/` | `sessions/STATUS_A.md` 24/10 | chưa có — ý chờ | A tự thấy (sau khởi động lại) |
| S5 | Brief sub-agent gửi đi còn chỗ trống `{{…}}` | 1 (25/10, A) | gửi bổ sung; agent có thể đã đoán | phiên 25/10 | chưa có ⇒ W8 | A tự thấy sau khi gửi |
| S6 | Ghi chú khóa học phiên trước có ~10 chỗ sai / đã cũ (sub-agent lần 2 tìm ra) | 1 (25/10) | đề xuất có thể dựa trên điều sai | `data/course_notes/v2/*` mục "chỗ lệch" | chưa có ⇒ W8 | sub-agent đọc lại |
| S7 | User phải nhắc "nghiên cứu ChatGPT trước, prompt đầy đủ" | 1 (24/10) | User phải nhắc | memory `research-via-chatgpt-relay` | chỉ memory ⇒ I1 | User |
| S8 | Memory cũ / sai tên | 2 file | session mới đọc gợi ý sai | `two-claude-sessions-setup.md`, `phase-7a2-implementer-state.md` | ⇒ I3 | A rà memory |
| S9 | Phép thử hook sinh key giả quá ngắn ⇒ tưởng hook lỗi | 1 (25/10, A) | chẩn đoán nhầm 1 lượt | `report_agent/2026-10-25_cai_tien_cach_lam/KE_HOACH.md` mục thử hook | chưa có — ý chờ (lỗi của công cụ / phép thử, loại trừ trước khi kết luận code hỏng) | A tự thấy khi xem lại phép thử |
| S10 | Hook lọt dòng nội dung bắt đầu bằng `++` (cả secret) | 1 (25/10, A viết) | lỗ hổng trong rào chặn lộ dữ liệu | `review.md` F1 | đã sửa; review chéo là bước bắt | **review chéo** (12 ca tự thử của A không bắt) |
| S11 | A dùng `python3` hệ thống (không `uv run`) cho script sửa tài liệu | 2 lần trong 1 phiên (25/10, A) | không (chỉ sửa chữ) | phiên 25/10 | đã có ở `Session_Prompt.md` §10 — không thêm luật; lặp ở phiên sau thì xem lại câu chữ §10 | A tự thấy |
| S12 | A tự duyệt plan G3 không chờ review; viết sai "cận dưới" ở điều kiện phụ §10 | 1 (25/10 chiều, A) | B tìm 3 lỗi tiêu chí sau khi duyệt; 2 lượt sửa plan | `phase_8_1_g3_plan.md` §9, §10; STATUS_A | ⇒ W11 | **review chéo** (sau khi duyệt) |
| S13 | Sub-agent câu kín lộ một phần: báo cáo ghi tên file nguồn (C24); grep in 1 dòng file mẫu (C26) | 2 (25/10, sub-agent của C) | C biết chủ đề câu kín | `phase_8_1_g0_4_sealed_review.md` §8, §10; STATUS_C | ⇒ W12 | C tự thấy khi đọc báo cáo |
| S14 | User dán nguyên câu kín cho A khi hỏi | 2 (25/10) | A thấy 3 câu kín | STATUS_A | ⇒ W12 (A nhắc) | A |
| S15 | Skill review bảo ghi correction vào mục người làm ↔ WORKFLOW §3.2 cấm | 1 (25/10, C báo) | không (C làm đúng WORKFLOW) | `risk-gated-agent-review` | ⇒ W13 | C đọc thấy lệch |
| S16 | Heredoc `<<EOF` không quote: backtick bị chạy như lệnh; f-string gặp `{}` | 2 lỗi cùng loại (25/10, A) | 1 lượt sửa; không hại | STATUS_A | ý chờ | A thấy lỗi in ra |
| S17 | Ghi giờ ước thay vì `date` (A 12:40↔12:20; C review B20) | 2 (25/10, A + C) | đính chính | handoff; STATUS_C | luật đã có `WORKFLOW.md` §6 — lặp nữa ⇒ rào (mẫu lệnh ghi giờ) | A / C tự thấy |
| S18 | Báo "xong" trước khi lệnh ghi file trả kết quả (C); danh sách "chưa commit" cũ (B) | 1 + 1 (25/10) | đính chính | STATUS_B, STATUS_C | ý chờ | B / C tự thấy |

**Kết vòng 2 — 15:44 25/10:** 7 sự cố mới (S12–S18), 3 thay đổi `đang thử` + 1 dời bẫy (User duyệt W11 cách a, W12; cho A sửa
W13). Vòng trước: W1–W10, I1–I3 được dùng trong phiên (sổ, `run-experiment` có tiêu chí ghi trước + cỡ mẫu + nhiễu A/A ở
mọi plan; hook không chặn nhầm commit nào; brief sub-agent không còn `{{…}}`). S4 (`/tmp`) không lặp — script G0.6 để ở
`data/phase_8_1/tools/` từ đầu.

**Thử mở phiên vòng 2 (15:47, sub-agent mới đóng vai B):** nắm đúng vai, Phase, việc ("không"), luật cứng, viết lại đúng W11 /
W12. Chỗ chưa rõ đã sửa: W11 thêm trỏ ở `run-experiment` §1 (người viết plan là B/C), ghi rõ mục từng file, người review
được chạy lệnh chỉ đọc, A chọn người review, file `<plan>_review.md`; W12 ghi rõ áp cho mọi người chưa được giao, "tên file
corpus", grep **nội dung corpus** (không phải mọi grep), script tạm vs dùng lại, `rm` bị chặn; handoff: B/C được review
bản nháp spec 8.2; WORKFLOW §2 thêm lệnh đếm point. Lúc thử, governance chưa commit (đã commit `c8f08e4` ngay sau).

**Kết vòng 25/10 11:05:** 11 sự cố, 11 thay đổi `đang thử`, 7 ý chờ. Không đề xuất thêm; phiên sau xem các mục `đang thử`
có được dùng không, sự cố có lặp không.

## Ý chờ (chưa có sự cố đủ — chưa thành luật)

- Test có paid call chỉ chạy khi bật biến môi trường (S1 lặp thì lên luật / rào).
- Script dùng lại để trong `data/<đợt>/tools/` ngay từ đầu, không để `/tmp` (S4 lặp thì thêm luật).
- Quyền Claude Code theo khả năng đảo ngược: chặn ghi/xóa collection runtime ở tầng quyền (hiện chỉ có luật chữ + code harness).
- Siết `settings.local.json` (đang cho phép rộng `git add`, `git push`) — file cá nhân của User, chỉ khi User muốn.
- Review kế hoạch rủi ro cao bằng họ model khác (Codex / ChatGPT) trước khi làm (khóa FDE tuần 3).
- Phép thử báo lỗi ⇒ loại trừ lỗi của chính phép thử / công cụ trước khi kết luận code hỏng (S9 lặp thì lên luật ở `practical-project-coding`).
- Đếm sẵn số vòng `changes_requested` / finding mỗi review làm chỉ số theo dõi cho vòng cải tiến.
