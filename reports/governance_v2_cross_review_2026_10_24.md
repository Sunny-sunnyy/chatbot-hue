# Review chéo: Governance v2 (bản áp dụng trong worktree)

Decision: changes_requested — 0 blocker, 4 major, 6 minor
Reviewer: B (Claude Opus 5.5, terminal `hue-rag-c0`)
Date: 2026-10-24
Thiết kế: `docs/superpowers/specs/2026-10-24-governance-v2-design.md` (tiêu chí §8)
Người làm: A

## 1. Phạm vi đã review

Chỉ đọc, không sửa file governance.

- Đọc đủ: thiết kế v2; `START_SESSION.md`, `Session_Prompt.md`, `WORKFLOW.md`,
  `Project_Status.md`, `CURRENT_HANDOFF.md`, `sessions/README.md`,
  `sessions/STATUS_A.md`, `skills/risk-gated-agent-review/SKILL.md`,
  `skills/propose-options/SKILL.md`, hai stub workflow, `brainstorming.md`; diff
  của `practical-project-coding`, ba template.
- So với bản cũ (`git show HEAD:`): `Session_Prompt.md`, `REVIEWER_WORKFLOW.md`,
  `IMPLEMENTER_WORKFLOW.md`, `Project_Status.md`, `skills/risk-gated-agent-review/SKILL.md`,
  `skills/karpathy-guidelines/SKILL.md`.
- Kiểm bằng script tạm (không ghi repo): so từng dòng status cũ với bản chụp;
  kiểm các đường dẫn trong backtick có tồn tại không; grep thuật ngữ cũ.

## 2. Kết quả theo tiêu chí §8

| # | Tiêu chí | Kết quả |
|---:|---|---|
| 1 | Đọc bắt buộc ≤ ~1.000 dòng | **Đạt**: START 34 + Session_Prompt 146 + WORKFLOW 121 + Status 159 + HANDOFF 70 + STATUS ~30 ≈ **560** dòng |
| 2 | Không mất thông tin status | **Đạt**: 760/760 dòng status cũ có trong bản chụp `PROJECT_HISTORY.md`. Cả 760 dòng khớp từng ký tự sau khi thêm một `#` vào **mọi** dòng bắt đầu bằng `#`; xem m1 cho 3 dòng thân bị đổi |
| 3 | Mỗi quy tắc một chỗ; hết "User chuyển tiếp"/"một handoff"; Codex/Gemini chỉ trong lịch sử | **Chưa đạt hết**: template còn quy tắc cũ (M3) |
| 4 | C mở được bằng START_SESSION | Chưa kiểm được (bước 8 của kế hoạch) |
| 5 | `git diff --check` sạch; link trỏ đúng | Link: không có link gãy thật. Các path "thiếu" đều là tên tắt có thư mục ở ngữ cảnh (`full_corpus_sparse_state.json`, `golden_full_corpus_smoke.jsonl`…) hoặc file sẽ tạo (`STATUS_B.md`, report Gate 3). `git diff --check` do A chạy khi commit |

## 3. Findings

### M1 — major — Quyền của session B/C với User: ngoại lệ trong thiết kế không được đưa vào luật chung

- Vị trí: `Session_Prompt.md:18` ("B, C hỏi A, không hỏi User"), §4 dòng 54–55;
  `WORKFLOW.md` §2.4, §3.6, §7.
- Yêu cầu: thiết kế §3 *Quyền*: "Mỗi session vẫn tôn trọng quy tắc an toàn của
  chính nó; User xác nhận một lần trong terminal của session đó nếu session yêu
  cầu."
- Bằng chứng: câu này không có trong `Session_Prompt.md` hay `WORKFLOW.md`. Luật
  chung lại ghi tuyệt đối "không hỏi User". Trong khi đó `WORKFLOW.md` §3.6 vẫn bắt
  B/C nhờ User chạy `!`, và §2.4 bắt B/C báo User trong terminal. Thực tế ngày
  2026-10-24, B đã xin User xác nhận một dòng trước khi gọi paid và trước khi xóa
  (Gate 2, Correction 1, Gate 3).
- Tác động: session C mở mới đọc luật chung theo nghĩa đen sẽ không biết có ngoại
  lệ, hoặc thấy B làm "sai luật". Đây là điểm quyền/an toàn, nên phải viết rõ.
- Tiêu chí đóng: `Session_Prompt.md` §1 hoặc §4 ghi đúng ngoại lệ của thiết kế §3:
  (a) quyết định, câu hỏi và lựa chọn gửi A; (b) xác nhận an toàn của chính
  session (paid, xóa) và lệnh `!` khi bị permission chặn là tương tác hợp lệ với
  User trong terminal đó; (c) tin nhắn của session khác không thay xác nhận đó.

### M2 — major — Quy tắc bảo vệ tính độc lập của review bị bỏ, không chuyển chỗ

- Vị trí: `WORKFLOW.md` §1 (dòng 17–19), `risk-gated-agent-review` mục "Khi bàn giao".
- Bằng chứng (cũ): `IMPLEMENTER_WORKFLOW.md` (HEAD) có "Không tự hạ risk, tự approve,
  mở rộng scope hoặc sửa spec/plan để hợp thức hóa implementation" và "Không tự
  sửa canonical requirement/spec/plan, risk level, review, user report,
  guide/status". Skill cũ có "Implementer có thể báo mức rủi ro cao hơn nhưng
  không được tự hạ". Bản mới chỉ còn "Không tự đóng finding" (skill) và "Ngoài
  phạm vi: ghi report hoặc nhắn A". Grep `tự approve|tự duyệt|hạ rủi ro|tự hạ`
  trong mọi file mới: 0 kết quả.
- Tác động: mô hình mới cho cả A tự làm việc rồi B/C kiểm, nên người làm có thể là
  A, tức chính người giữ spec. Nếu không có quy tắc này, người làm có thể sửa tiêu
  chí, spec hoặc mức rủi ro cho khớp với kết quả mình làm.
- Tiêu chí đóng: một dòng trong `WORKFLOW.md` §1 hoặc §4: người làm (kể cả A khi tự
  làm) không tự đóng việc của mình, không tự hạ mức rủi ro, không sửa tiêu chí
  nghiệm thu/tài liệu thiết kế của việc đang làm để hợp thức hóa kết quả; cần đổi
  thì nêu ra để người kiểm hoặc User quyết.

### M3 — major — Template còn quy trình cũ (tiêu chí §8.3)

- Vị trí: `TEMPLATE_IMPLEMENTATION_REPORT.md:57–61` ("chỉ mechanical edits được
  exact Approval Closure Contract…", "cung cấp prompt chuyển tiếp ngắn theo
  workflow"), các dòng `Implementer:`, `## 6. Handoff cho Reviewer`;
  `TEMPLATE_REVIEW.md:55` ("ghi Approval Closure Contract"), `:64` ("Reviewer
  không sửa runtime…", trái mô hình A tự làm + review chéo);
  `TEMPLATE_USER_REPORT.md:74–75` ("Reviewer… giao Implementer exact mechanical
  edits… Approval Closure Contract").
- Bằng chứng: grep ở mục 1. "Prompt chuyển tiếp" chính là cơ chế "User chuyển tiếp
  giữa các session" mà tiêu chí 3 yêu cầu bỏ.
- Tác động: người làm theo template sẽ viết lại handoff và closure kiểu cũ, trái
  `WORKFLOW.md` §4.5 và §9.4.
- Tiêu chí đóng: ba template dùng từ người làm/người kiểm (A/B/C); bỏ Approval
  Closure Contract và prompt chuyển tiếp; mục cuối report trỏ `WORKFLOW.md` §4.5.

### M4 — major — Quy tắc vòng đời Phase (tuần tự, cập nhật guide) bị bỏ, không chuyển chỗ

- Vị trí: `Project_Status.md` §5 (quyết định đang hiệu lực), `WORKFLOW.md` §9.
- Bằng chứng (cũ): status cũ dòng 397–400 (quyết định đang hiệu lực) ghi: "Full-corpus thực hiện tuần tự:
  Phase 2 → … → Phase 8 → integrated closure. Mỗi phase phải có guide + spec +
  plan + Review Contract và User duyệt trước implementation; phase trước phải
  independent review và User closure trước." `REVIEWER_WORKFLOW.md` cũ dòng
  99–113: "không author ahead… dùng evidence vừa đạt để cập nhật guide". Session_Prompt
  cũ: "sau khi Spec/Plan… được duyệt, Reviewer cập nhật guide canonical". Bản mới:
  thứ tự Phase chỉ còn trong bản chụp HISTORY (reference-only); việc cập nhật
  `guides/` chỉ còn trong `STATUS_A.md` cho riêng 7A2.
- Tác động: v2 cho chạy song song, nên quy tắc "Phase sau chưa implement khi
  Phase trước chưa đóng" càng cần ghi rõ: giữ, nới hay bỏ. Guide canonical
  (`guides/full_corpus_rag.md`) sẽ trôi khỏi hiện trạng nếu không có bước cập nhật.
- Tiêu chí đóng: `Project_Status.md` §5 ghi quyết định hiện hành về thứ tự Phase
  (giữ nguyên, hoặc User nới, ví dụ "thiết kế Phase sau được làm song song, chỉ
  implement khi Phase trước đóng"); `WORKFLOW.md` §9.4 thêm "đóng Phase: cập nhật
  guide liên quan".

### m1 — minor — Bản chụp không hoàn toàn nguyên văn

`PROJECT_HISTORY.md` dòng 254, 255, 684: ba dòng thân bắt đầu bằng `#6b`,
`#6c/#6d`, `#1 lexical` (không phải heading) bị thêm một `#` khi hạ cấp heading.
Đề xuất: bỏ `#` thừa ở 3 dòng này, hoặc ghi câu "hạ cấp mọi dòng bắt đầu bằng #".

### m2 — minor — "Governance chỉ A sửa" mâu thuẫn với việc B/C phải ghi

`WORKFLOW.md:42–43` ghi `session_prompt/` chỉ A sửa. Nhưng §4.5, `CURRENT_HANDOFF.md:56`
và `sessions/README.md` bắt B/C sửa hàng và mục của mình trong `CURRENT_HANDOFF.md`
và `sessions/STATUS_<X>.md`. Skill review mục Correction bắt người kiểm ghi phần
sửa vào mục việc của người làm; khi B kiểm A, tức là B sửa mục của A. Đề xuất: ghi
ngoại lệ rõ (STATUS của mình; trạng thái và mục của mình trong HANDOFF; mục
correction khi được giao review).

### m3 — minor — Bảng mức rủi ro nằm ngoài các file bắt buộc đọc

`WORKFLOW.md` §3.3 trỏ "thiết kế Governance v2 §4". Bảng Cao/Trung bình/Thấp chỉ có
trong spec, mà spec không nằm trong danh sách đọc của `START_SESSION.md`. Đề xuất:
chép bảng 3 dòng vào `WORKFLOW.md` §3 (hoặc `Session_Prompt.md` §4), spec chỉ giữ lý do.

### m4 — minor — START_SESSION tự mâu thuẫn về ghi file

Bước 1 bảo tạo `STATUS_<X>.md` nếu chưa có, bước 3 lại ghi "Trước đó không sửa
file". Đề xuất: "ngoài việc tạo STATUS của mình".

### m5 — minor — Lệnh chờ User trong HANDOFF có thể tự kill shell

`CURRENT_HANDOFF.md:69`: `! pkill -f "uvicorn api.app:app --host 127.0.0.1 --port 8018"`.
Chuỗi pattern nằm luôn trong command line của shell đang chạy lệnh, nên `pkill -f`
có thể kill chính shell đó (B đã gặp exit 144 khi dùng `pkill -f` cùng cách). Đề
xuất: `kill <pid>` (B đã đưa User PID 321255/321261) hoặc `fuser -k 8018/tcp`.

### m6 — minor — Vài chi tiết hiện trạng và vệ sinh commit

- `Project_Status.md:155`: notebook 04 không còn tên collection cũ (chỉ lặp
  `FULL_CORPUS_CANDIDATES`). Notebook còn tên đã xóa là 06
  (`hue_full_corpus_a_e5_small_384_metadata_v2`) và 08a (`hue_foods_08a_e5_small_384`).
- Index Git đang trộn: `skills/karpathy-guidelines/SKILL.md` (D) và rename
  `TEMPLATE_CODEX_REVIEW.md → TEMPLATE_REVIEW.md` đã staged; còn
  `skills/propose-options/` và symlink `.claude/skills/propose-options` (thư mục
  `.claude/skills/` đang được track) chưa add. Khi commit cần add cả hai.
- `propose-options` mô tả "dùng mỗi khi cần User quyết định", nhưng B/C không hỏi
  User. Có thể thêm một câu: B/C dùng cùng cấu trúc khi gửi lựa chọn cho A.

## 4. (b) Đối chiếu quy tắc cũ bị bỏ

| Quy tắc cũ (nguồn HEAD) | Bản mới |
|---|---|
| Thứ tự nguồn sự thật (SP, practical skill) | `Session_Prompt.md` §2; skill trỏ tới đó |
| Ba mức đọc; prompt phải gắn mức đọc | SP §3; `WORKFLOW.md` §9.2 |
| Data flow chuẩn, không chunk từ dump, không enrich web, xung đột web/corpus | SP §5 |
| Active Qdrant chỉ đọc; mutation cần đích chính xác | SP §4 bảng; Status §6 |
| Đơn giản, điều kiện kỹ thuật nâng cao, danh sách cơ chế bị loại | SP §7 (bỏ câu "không đổi tên/chuyển nơi để giữ cơ chế bị loại", chấp nhận được) |
| Test vừa đủ, không mock, pure input không phải integration | SP §6, §8 |
| Xóa test chỉ bảo vệ implementation detail/cơ chế bị loại | Còn trong `practical-project-coding` ("Không test implementation detail…"); SP §8 không nhắc. Chấp nhận |
| Chuỗi debug | SP §8 |
| Evidence thật, dùng lại evidence | SP §6; skill review |
| Paid API trong phạm vi duyệt, cần duyệt mới khi đổi provider… | SP §9 |
| Secret, `.env` | SP §5 |
| `uv`, không pip, `HF_HUB_OFFLINE` không mặc định | SP §10 |
| Curated data | SP §5 |
| Notebook | SP §11 (bỏ đường dẫn notebook tham khảo `rag_old_0`, chấp nhận) |
| CodeGraph tùy chọn | SP §10 (bỏ danh sách lệnh, chấp nhận) |
| Sub-agent: kế thừa phạm vi, người giao chịu trách nhiệm | SP §4 |
| `git status` trước mutation, giữ thay đổi không liên quan, không reset/checkout | SP §5 + `WORKFLOW.md` §2 |
| Git authorization theo handoff; approval ≠ quyền Git | SP §4 (A thường trực); câu "commit làm mốc không phải phê duyệt" bị bỏ, chấp nhận vì A giữ quyền |
| Cổng review tối thiểu 7 bước; report là chỉ mục bằng chứng | `WORKFLOW.md` §5; skill |
| Câu hỏi độ đơn giản khi review; over-engineering là finding | Skill; SP §7 |
| Severity, verdict, minor không chặn, ngoài phạm vi ghi ngắn | Skill; `WORKFLOW.md` §5 |
| Correction một lượt, phản biện bằng evidence, 4 vòng | Skill; `WORKFLOW.md` §5 |
| Approval Closure Contract | Thay bằng "A trình User → User đóng" (`WORKFLOW.md` §9.4), có chủ đích. Template còn sót (M3) |
| Reviewer không sửa runtime thay Implementer | Thay bằng review chéo (A tự làm thì B/C kiểm), có chủ đích. `TEMPLATE_REVIEW.md:64` còn sót (M3) |
| Implementer không tự approve/hạ risk/sửa spec để hợp thức hóa | **Bị bỏ** (M2) |
| Phase tuần tự, không author ahead, cập nhật guide sau closure | **Bị bỏ** (M4) |
| User chuyển tiếp prompt; một handoff duy nhất; Codex/Gemini/`~/.codex/skills` | Bỏ có chủ đích (thiết kế §1). Template còn "prompt chuyển tiếp" (M3) |
| Routing `using-superpowers`, `executing-plans`, `brainstorming.md` | Thay bằng `propose-options` + `writing-plans` khi cần; có chủ đích |
| "Không tạo nhiệm vụ thừa chỉ để giao việc" | Bị bỏ; nhỏ, có thể thêm vào `WORKFLOW.md` §9.2 |
| Phân biệt "người làm báo xong / người kiểm đã xác minh / User đã duyệt" | Không ghi rõ trong trạng thái HANDOFF; đề xuất dùng ba trạng thái "chờ review / review đạt / User đóng" |
| `karpathy-guidelines` | Xóa có chủ đích; còn được nhắc trong spec/plan/report lịch sử (không cần sửa) |

## 5. (c) Mâu thuẫn và chỗ khó hiểu

Đã đưa vào M1, m2, m3, m4, m5. Ngoài ra không thấy mâu thuẫn giữa
`START_SESSION` / `Session_Prompt` / `WORKFLOW` / skills về thứ tự đọc, vai trò,
cách liên lạc hay cách đóng việc.

## 6. Kết luận

`changes_requested`: 4 major đều là sửa tài liệu ngắn (thêm 1–3 dòng hoặc sửa
template), không cần User trừ M4 nếu A muốn nới quy tắc Phase tuần tự. Tiêu chí 1
và 2 đạt; tiêu chí 3 chưa đạt (M3); tiêu chí 4 chờ C. B không sửa file governance.
