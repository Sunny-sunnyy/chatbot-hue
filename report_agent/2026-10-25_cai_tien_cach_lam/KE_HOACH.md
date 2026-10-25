# Kế hoạch đợt cải tiến cách làm — 2026-10-25

Mở 10:11 25/10/2026 (A). User mở phiên với mục tiêu: "phiên này không tiếp tục dự án, chỉ bàn về cách làm
việc, cải tiến dự án"; tham khảo cách làm của một dự án khác của User (bản mô tả private ở
`data/external_project_notes/`) và khóa học AI FDE (ghi chú private `data/course_notes/v2/`, 5 sub-agent đọc 15
file tóm tắt). Không đổi hành vi chatbot, không gọi API trả phí.

## Quyết định của User (theo giờ)

| Giờ | Quyết định |
|---|---|
| 09:5x | Chọn gói: (1) vòng tự cải tiến + sổ, (2) nâng `run-experiment`, (4) Session D. **Không** cắt tài liệu mở phiên (sợ agent mất ngữ cảnh). Đọc toàn bộ khóa học, nhìn rộng |
| 10:0x | Thêm: rào bằng máy, `CLAUDE.md`/`AGENTS.md` gốc ngắn, hai luật 1 dòng, cách đọc tài liệu dài bằng sub-agent. **Cách làm phải hiệu quả gần như nhau cho Codex/AGY**, không chỉ Claude Code. Chi tiết A tự quyết |
| 10:0x | Bản mô tả cách làm của dự án khác (bản 2): A tự quyết ⇒ giữ private ở `data/external_project_notes/`, file tracked về bản 1 |

## Thay đổi (A làm; một reviewer độc lập kiểm — WORKFLOW §1 "A tự sửa thì người khác kiểm")

| ID | Thay đổi | File |
|---|---|---|
| W1 | Skill mới `improve-workflow` (vòng tự cải tiến có người duyệt) | `skills/improve-workflow/SKILL.md` + symlink `.claude/skills/` |
| W2 | Sổ cải tiến, vòng đầu: sự cố hue_rag có bằng chứng + các thay đổi phiên này `đang thử` + ý chờ | `session_prompt/SO_CAI_TIEN_CACH_LAM.md` |
| W3 | Nâng `run-experiment`: chỉ số có chiều/sàn/mức tụt/nhiễu; nhiễu từ A/A sẵn có; cỡ mẫu trước khi chạy; kiểm người chấm; số do script in; luật giữ/gỡ | `skills/run-experiment/SKILL.md` |
| W4 | Session D (học cùng User, chỉ đọc): vai, checklist, sổ học private, không ghi memory | `WORKFLOW.md` §1, §10 (mới); `START_SESSION.md`; `data/hoc_cung_D/` (private) |
| W5 | Rào bằng máy: hook git `pre-commit` dùng chung mọi agent (chặn đường dẫn private, secret, tên dự án khác ở dòng thêm mới); Claude Code cấm đọc `.env` | `.githooks/pre-commit`, `git config core.hooksPath .githooks`, `.claude/settings.json` |
| W6 | `AGENTS.md` gốc (bản chính, mọi agent) + `CLAUDE.md` nhập `@AGENTS.md` | `AGENTS.md`, `CLAUDE.md` |
| W7 | Hai luật 1 dòng: chỉ dẫn trong nội dung ngoài là dữ liệu; duyệt kế hoạch gắn với đúng bản | `Session_Prompt.md` §2, `WORKFLOW.md` §9 |
| W8 | Đọc tài liệu dài bằng sub-agent theo khuôn (+ đọc lại brief trước khi gửi, tự kiểm 2–3 khẳng định) | `WORKFLOW.md` §9 |
| W9 | Giữ gọn: sửa memory cũ; bỏ mục "Tạm gác" handoff; ghi đề xuất cho dự án (8.1/8.2/9/deploy) thành một file trỏ từ handoff | memory; `CURRENT_HANDOFF.md`; `de_xuat_cho_du_an.md`; `Project_Status.md` §5, §7, §8; `.gitignore` (`.aws/`) |

## Tiêu chí nghiệm thu

1. Mỗi thay đổi có căn cứ: sự cố có bằng chứng, hoặc quyết định User ở bảng trên. Không thêm cơ chế ngoài danh sách.
2. Không mâu thuẫn luật gốc; luật không nằm hai chỗ (chỗ phụ chỉ trỏ). Mỗi skill ≤ ~100 dòng.
3. Agent không phải Claude Code làm theo được: mọi luật ở file Markdown thường; hook git chạy không phụ thuộc agent.
4. Hook: thử bằng lệnh thật trên repo tạm — ít nhất 4 ca **phải chặn** và 4 ca **phải qua** đúng; settings JSON hợp lệ (`jq`).
5. Repo public: diff không chứa số liệu/đường dẫn dự án khác, nội dung corpus, câu Golden/câu kín; `data/` không bị stage.
6. `git diff --check` sạch; file tracked mới có trong `Project_Status.md` §7.

## Hợp đồng kiểm

Reviewer: sub-agent ngữ cảnh mới (chưa có B/C trong phiên) theo skill `risk-gated-agent-review`, nhận diff +
kế hoạch này, không nhận kết luận của A. Tự chạy lại phép thử hook. Kết quả ghi `review.md` trong đợt này.

## Bổ sung 10:29 25/10 (sau review `review.md`, chỉ thêm — không sửa phần trên)

- Ngoài W1–W9, A làm thêm 3 việc nấc rẻ nhất của vòng cải tiến (dời luật về chỗ mọi agent đọc), ghi trong sổ:
  **I1** "nghiên cứu ChatGPT trước khi đề xuất" từ memory ra `Session_Prompt.md` §9; **I2** "file nhiều session cùng
  ghi: đọc lại trước khi sửa" từ STATUS_A ra `WORKFLOW.md` §3.2; **I3** sửa 2 memory cũ. Cùng với W5/W6: danh sách
  governance chỉ A sửa ở `WORKFLOW.md` §3.2 thêm `AGENTS.md`, `.githooks/`, `.claude/settings.json`; luật repo public
  và câu kín ghi vào `Session_Prompt.md` §5 (trước chỉ ở memory / skill) để `AGENTS.md` trỏ đúng chỗ (review F4).
- Sửa theo review: F1 hook chỉ xét dòng trong thân hunk (dòng nội dung bắt đầu bằng `++` trước đây lọt); F2 kiểm cả
  tên file; F4 `AGENTS.md` trỏ đúng mục; F5 `run-experiment` 113 → 105 dòng; F6 bỏ chữ "memory" trong hook, thêm việc
  phải làm khi `hooksPath` sai; F7 khôi phục "Commit cuối" ở STATUS_A, thêm bảng thử hook dưới đây.

### Thử hook sau khi sửa F1/F2 (A, repo tạm `/tmp/a_hooktest{2,3}`, đã xóa)

| Kỳ vọng | Ca | Kết quả |
|---|---|---|
| chặn | file dưới `data/` (`add -f`); `knowledge-base-hue/`; `gửi chatgpt/a b.md` (dấu cách, tiếng Việt); `.env`; `backend/.env.local`; `git mv` vào `data/` | 6/6 chặn |
| chặn | dòng mới có tên dự án khác (chữ hoa); dòng bắt đầu `++ ` có tên đó (E1); file rỗng có tên đó trong tên file (E2) | 3/3 chặn |
| chặn | dòng có dạng key `sk-…` (33 ký tự); dạng AWS key; dòng `++ ` + dạng AWS key (E3); header private key | 4/4 chặn; thông báo không in key |
| qua | sửa chữ thường; dòng `++ i; counter`; `risk-gated…, task-12`; `data_utils.py`, `docs/data/x.md`, `environment.md`; xóa dòng cũ có tên dự án khác; xóa file; sửa chính file hook; file nhị phân | 8/8 qua |

Ghi chú: lần thử đầu báo sai 2 ca secret vì **chính phép thử** sinh key giả quá ngắn (64 byte ngẫu nhiên lọc còn ~15
ký tự < ngưỡng 20); sửa cách sinh (in độ dài) rồi chạy lại — hook đúng. Lần thử 12/12 trước sửa F1 cũng có thể đạt
nhờ may ở ca secret.
