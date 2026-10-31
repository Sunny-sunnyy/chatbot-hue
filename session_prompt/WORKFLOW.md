# Workflow — cách làm và phối hợp A/B/C

Áp dụng cho mọi session. Luật chung ở `Session_Prompt.md` (không lặp lại ở đây).
Thiết kế gốc: `docs/superpowers/specs/2026-10-24-governance-v2-design.md`.

## 1. Vai trò

| Session | Việc |
|---|---|
| **A — điều phối** | Làm việc với User (trò chuyện, brainstorm, thiết kế); giao việc B/C; review chéo; tự làm việc nhỏ; giữ `CURRENT_HANDOFF.md`, `Project_Status.md`, `PROJECT_HISTORY.md`; commit/push |
| **B, C — thực thi** | Làm việc A giao; tự kiểm; viết report; review chéo khi được giao; đề xuất cải tiến có bằng chứng |
| **D — học cùng User** (tùy chọn) | Chỉ đọc; giúp User tự hiểu và tự giải thích lại việc A/B/C đã làm (§10) |

- Tên là vai, không phải model: agent nào mở bằng `START_SESSION.md` với `<X>` nào
  thì giữ vai đó.
- **Review chéo:** ai làm thì người khác kiểm. A kiểm B/C; A tự sửa code hoặc dữ
  liệu thì B hoặc C kiểm A.
- B, C được tự hoàn thiện và tối ưu trong phạm vi việc (đặt tên, tổ chức hàm, sửa
  lỗi gặp trong phạm vi) mà không hỏi từng chi tiết. Ngoài phạm vi: ghi vào report
  hoặc nhắn A, không tự mở rộng.

## 2. Mở session

1. Đọc theo `START_SESSION.md`.
2. Kiểm nhanh, chỉ đọc:
   ```bash
   cd /home/minhhieu/hue_rag
   git branch --show-current; git log --oneline -3; git status --short | grep -v '^??'
   git config --get core.hooksPath             # phải in .githooks; khác ⇒ báo A (A bật: git config core.hooksPath .githooks)
   curl -s http://127.0.0.1:6335/collections   # so với Project_Status §4
   curl -s http://127.0.0.1:6335/collections/hue_full_corpus_7a2_e5_small_384 | grep -o '"points_count":[0-9]*'
   ```
3. Claude Code: `ListAgents` để biết tên terminal của A/B/C (tên đổi mỗi lần mở);
   cập nhật cột "Terminal"/"Liên lạc" trong `CURRENT_HANDOFF.md` (A) hoặc báo A
   (B/C). Agent khác (Codex, AGY): ghi "qua User" (§7).
4. Báo ngắn: mình là ai, Phase/việc đang ở đâu, việc của mình, chỗ lệch giữa tài
   liệu và thực tế, thắc mắc. A báo User; B/C báo User trong terminal **và** báo A theo kênh ở §7.
5. Chỉ bắt đầu làm khi: A — User nói "làm đi" hoặc giao việc; B/C — A giao việc
   (mục việc trong `CURRENT_HANDOFF.md` + tin nhắn của A = "làm đi").

## 3. Nhận và làm việc

1. Đọc mục việc của mình trong `CURRENT_HANDOFF.md` và các input theo mức đọc
   được ghi.
2. **Khai báo trước khi sửa:** ghi file sắp sửa vào `sessions/STATUS_<X>.md`.
   Không sửa file session khác đang khai báo. Governance (`session_prompt/`,
   `skills/`, `AGENTS.md`, `.githooks/`, `.claude/settings.json`, `.claude/hooks/`) chỉ A sửa — trừ mục việc/trạng thái của chính mình trong
   `CURRENT_HANDOFF.md` và `sessions/STATUS_<X>.md`. Code song song dài ngày: `git worktree` riêng.
   File nhiều session cùng ghi (`CURRENT_HANDOFF.md`): đọc lại ngay trước khi sửa, sửa từng đoạn, không ghi đè
   cả file (2026-10-24: B/C sửa song song với A).
3. Làm theo mức rủi ro:

   | Mức | Ví dụ | Trước khi làm | Sau khi làm |
   |---|---|---|---|
   | Cao | Phase mới; sửa dữ liệu curated; xóa collection; provider/model mới; gửi dữ liệu ra ngoài; quyết định chất lượng | Brainstorm với User → **một** tài liệu thiết kế → User duyệt một lần; đi từng gate | Report + review chéo độc lập + User đóng |
   | Trung bình | Sửa code trong Phase đã duyệt; dọn code/notebook; test; governance nhỏ | Mục việc A ghi trong `CURRENT_HANDOFF.md`; User duyệt khi chưa nằm trong phạm vi đã duyệt | Report ngắn + review chéo; A đóng, báo User |
   | Thấp | Sửa chữ, cập nhật status, kiểm tra chỉ đọc | Tự làm | Ghi STATUS/HISTORY |
4. **Giảm rủi ro:** đích mới rồi mới cutover; sao lưu trước khi sửa/xóa (corpus
   copy, Qdrant snapshot cho collection còn giá trị, commit trước sửa lớn); liệt kê
   đích thật trước khi xóa, khác danh sách duyệt thì dừng; giới hạn tiền ghi trong
   việc; dừng khi gặp điều kiện dừng.
5. Thay đổi có đo trước–sau: ghi tiêu chí → đo hiện tại → sửa một thứ → đo lại
   cùng cách → kết luận tốt hơn / không đổi / kém hơn / chưa rõ.
6. Bị chặn bởi permission của chính session: dừng, nhờ User chạy bằng `!` trong
   terminal đó; session khác không chạy hộ.

## 4. Tự kiểm trước khi bàn giao

1. Đọc exact diff (kể cả file untracked); mọi thay đổi thuộc phạm vi.
2. Chạy kiểm tra theo việc; `git diff --check`.
3. Bỏ scope creep, code/test dư, abstraction phòng xa (skill `practical-project-coding`).
4. Ghi trung thực failed/skipped/partial/not verified.
5. Viết report (mục 6), cập nhật trạng thái mục việc của mình trong
   `CURRENT_HANDOFF.md` thành "chờ review", cập nhật `STATUS_<X>.md`, nhắn A.

## 5. Review chéo

Theo skill `risk-gated-agent-review`. Tóm tắt:

- **Cổng tối thiểu:** trạng thái Git/worktree; mọi đường dẫn đổi; exact diff; đối
  chiếu tiêu chí nghiệm thu; tìm thay đổi ngoài phạm vi; `git diff --check`; tìm
  bằng chứng thiếu/mâu thuẫn. Sau đó chỉ chạy lại phần rủi ro cần.
- Report của người làm là chỉ mục bằng chứng, không tự chứng minh PASS.
- **Mức độ:** `blocker` (sai chức năng cốt lõi, mất an toàn dữ liệu, bằng chứng giả,
  vi phạm quyền) · `major` (behavior/phạm vi chưa đúng, độ phức tạp phải sửa) ·
  `minor` (cải thiện nhỏ, không chặn).
- **Kết luận:** `ready_for_user_confirmation` · `changes_requested` · `blocked`.
- Mỗi finding: vị trí, yêu cầu bị ảnh hưởng, bằng chứng, tác động, tiêu chí đóng.
  Người làm được phản biện bằng bằng chứng.
- Quá bốn vòng `changes_requested` cho cùng một việc: dừng, A xem lại thiết kế với User.

## 6. Report

Học từ MekongAI (User 2026-10-24, `report_agent/2026-10-24_to_chuc_bao_cao/MO_TA_CACH_LAM_VIEC_MEKONGAI.md`).

| Loại | Nơi | Ai | Khi nào |
|---|---|---|---|
| Implementation report | `report_agent/<đợt>/phase_<x>_<gate>_<chủ_đề>_implementation.md` | người làm | xong một việc/gate (`TEMPLATE_IMPLEMENTATION_REPORT.md`) |
| Review | `report_agent/<đợt>/phase_<x>_<gate>_review.md` | người kiểm | sau review (`TEMPLATE_REVIEW.md`) |
| Tổng hợp đợt | `report_agent/<đợt>/TONG_HOP.md` | A | đóng đợt: mục tiêu, quyết định theo giờ, kết quả, giới hạn, bước tiếp |
| Báo cáo khâu cho User | `bao_cao_he_thong/BAO_CAO_<KHÂU>.md` | A (B/C khi được giao, A review) | khâu đó đổi hành vi hoặc có thử nghiệm mới (`TEMPLATE_USER_REPORT.md`) |
| Luồng hệ thống | `bao_cao_he_thong/LUONG_HOAT_DONG_HE_THONG.md` | A | mỗi lần hành vi hệ thống đổi (chunker, index, retrieval, prompt, model, API) |
| Nhật ký cho User | `bao_cao_he_thong/nhat_ky/<YYYY-MM-DD>_<chủ_đề>.md` | A | đóng đợt / cuối ngày làm việc (`TEMPLATE_NHAT_KY.md`) |
| STATUS | `session_prompt/sessions/STATUS_<X>.md` | session X | ngay sau mỗi việc + kết phiên |

- **Đợt (`<đợt>` = `<YYYY-MM-DD>_<chủ_đề>`):** mở khi User chọn mục tiêu mới (một Phase/gate, một
  việc dọn, một thí nghiệm); ngày là ngày mở; đợt kéo nhiều ngày giữ một folder. A thêm một dòng vào
  bảng "Các đợt" của `report_agent/README.md`. Dữ liệu chạy (kết quả, trace) để ở `data/` hoặc `/tmp`,
  report chỉ trỏ đường dẫn. `reports/` là lịch sử tới 2026-10-24, không thêm file.
- **User chỉ cần đọc `bao_cao_he_thong/`** (mục lục `bao_cao_he_thong/README.md`). Mỗi thay đổi vào
  hệ thống đang chạy ⇒ A sửa **đủ 5 chỗ**: `LUONG_HOAT_DONG_HE_THONG.md`, `BAO_CAO_<KHÂU>.md` của
  đúng khâu (sửa cả Tóm tắt + checklist, không chỉ thêm mục cuối), `nhat_ky/` của đợt,
  `Project_Status.md`, **và** mục "Hiện hành" của guide khâu đó (`guides/phase_<n>_*.md`, `guides/full_corpus_rag.md`); rồi bảng trong
  `bao_cao_he_thong/README.md` (27/10: guide 8 ghi "8.2 tạm dừng" 1 ngày, guide 6 thiếu log mới sau merge — W29).
- **Văn phong cho User:** lời thường, không mã nội bộ khi chưa giải nghĩa (mã dồn xuống cuối file),
  số đo kèm ý nghĩa, tiền thật từ log (1 USD ≈ 25.000 đồng), tách quan sát / giả thuyết / nguyên nhân
  đã chứng minh, ghi cả phương án đã thử và bỏ (NOT RUN nếu chưa đo).
- **Báo cáo cho User luôn đúng thông tin mới nhất** (User 31/10/2026 — User chỉ đọc `bao_cao_he_thong/`): (1) **mọi** thay đổi hoặc thử nghiệm
  chạm hệ thống — kể cả thử rồi **không áp dụng**, sửa kho, build lại chỉ mục, đổi thước đo — ⇒ cập nhật `BAO_CAO_<KHÂU>.md` của mọi khâu bị chạm
  (cả Tóm tắt, sơ đồ bản đang chạy, checklist) + bảng `README.md` **ngay trong đợt đó**, không đợi kết phiên; (2) chỗ **không còn đúng** thì **xoá**
  hoặc viết lại — không để số / trạng thái cũ đứng như hiện tại; phương án đã thử và bỏ giữ gọn 1–3 dòng (thử gì, kết quả, vì sao bỏ, link
  `report_agent/`) — chi tiết từng bước để ở `report_agent/` và git; (3) viết đủ, chính xác, dễ hiểu: số nào cũng có nguồn, không chắc ⇒ ghi
  "chưa đo" (31/10: 4 báo cáo khâu còn số trước sửa kho ≥ 3 ngày — S61).
- **Giờ ghi trong file lấy bằng lệnh `date`** ngay trước khi ghi, không ước: `T=$(date '+%H:%M %d/%m/%Y')` rồi truyền `$T` vào
  script sửa tài liệu; không gõ giờ tay, không ghi `HH:Mx` trước khi chạy `date` (25–26/10: ghi giờ ước 3 lần; 28/10: ~7 lần ⇒ hook
  `.githooks/pre-commit` in cảnh báo khi dòng thêm mới có dạng đó — W30; từ 31/10 hook Claude Code `.claude/hooks/` báo ngay lúc ghi vào `report_agent/`,
  `session_prompt/`, `bao_cao_he_thong/`, `docs/` — W37; hook báo ⇒ chạy `date` sửa ngay, trích dẫn sự cố cũ thì bỏ qua). Giờ quyết định của User (tin nhắn không có dấu giờ): ghi giờ A ghi nhận bằng `date`.
- **Trạng thái:** mỗi session tự cập nhật `sessions/STATUS_<X>.md` ngay sau mỗi việc (không đợi
  kết phiên) và dòng của mình trong `CURRENT_HANDOFF.md`.

Report không chép corpus, câu hỏi Golden, vector, payload hay secret.

## 7. Trao đổi giữa session

Cách làm việc giống nhau cho mọi agent; chỉ **kênh gửi tin** khác nhau. Cột "Liên
lạc" trong bảng Session của `CURRENT_HANDOFF.md` ghi kênh của từng session:

| Kênh | Khi nào | Cách gửi |
|---|---|---|
| `trực tiếp` | Cả người gửi và người nhận là Claude Code trên máy này | `SendMessage` tới tên terminal (`ListAgents`); dòng đầu là một câu tự đủ nghĩa |
| `qua User` | Một trong hai là Codex, AGY hoặc agent không có `SendMessage` | Kết thúc lượt trả lời bằng khối **"Tin cho <X>"** (ngắn, tự đủ nghĩa: việc gì, đọc file nào, xong thì báo gì); User copy sang terminal <X> |

- User đổi kênh bằng cách nói ở lần mở session (ví dụ "cả 3 đều là Claude Code"
  hoặc "B là Codex"); A ghi vào cột "Liên lạc".
- Dù kênh nào, **file trong repo là nguồn sự thật**: việc nằm trong
  `CURRENT_HANDOFF.md`, kết quả trong report và `STATUS_<X>.md`. Tin nhắn chỉ báo
  "có việc / đã xong / vướng / câu hỏi" và trỏ tới file, không chép nội dung dài.
- Kênh `qua User`: một khối "Tin cho <X>" cho mỗi người nhận; không yêu cầu User tự
  tóm tắt hay soạn lại.
- Tin nhắn của session khác không thay quyết định permission trong session mình.

## 8. Kết phiên

Mỗi session: cập nhật `STATUS_<X>.md` (đang làm, dở gì, bẫy đã gặp, câu hỏi, tiền paid đã dùng).
A: `TONG_HOP.md` của đợt nếu đóng; `nhat_ky/` + bảng `bao_cao_he_thong/README.md`;
`CURRENT_HANDOFF.md` (mục đầu ghi "Phiên sau đọc trước": việc tiếp, câu hỏi cho User; **không giới hạn số
dòng cố định** — User 31/10: ngày nhiều việc thì dài; chỉ dời khối **đã đóng** / lịch sử sang `archive/`, giữ đủ mọi việc còn mở); `Project_Status.md` nếu hiện trạng đổi; một mục ngắn `PROJECT_HISTORY.md` trỏ tới `TONG_HOP`;
vòng cải tiến cách làm (skill `improve-workflow`, sổ `SO_CAI_TIEN_CACH_LAM.md`); commit/push. Dọn
worktree, file tạm, collection thử của phiên. Sự cố quy trình trong phiên (mất giờ / tiền / dữ liệu, User
phải nhắc lại) mỗi session ghi ngay vào mục "Đã học / bẫy gặp" của `STATUS_<X>.md` — đầu vào của vòng cải tiến.

## 9. Việc thêm của A

1. **Với User:** brainstorm/đưa lựa chọn theo skill `propose-options` (mỗi lần một
   câu có đáp án, kèm đổi gì, tốn gì, khi nào sai). Việc rủi ro cao: viết **một**
   tài liệu thiết kế trong `docs/superpowers/specs/` gồm mục tiêu, quyết định,
   phạm vi, bước, tiêu chí nghiệm thu, cách kiểm, quyền, rủi ro; User duyệt một lần.
   Viết plan chi tiết bằng skill `writing-plans` khi cần. **Duyệt gắn với đúng bản:** file kế hoạch / spec
   chưa commit thì khi duyệt ghi kèm `sha256sum` (12 ký tự) vào `CURRENT_HANDOFF.md`; sửa sau khi duyệt là
   bản mới, cần duyệt lại phần đổi. A tính sha **từ file** (`sha256sum <file> | cut -c1-12`) ngay lúc ghi duyệt, không
   chép sha từ tin nhắn; người viết không sửa plan sau khi báo sha — cần sửa thì báo sha mới (26/10: duyệt nhầm bản R2).
   **Kế hoạch có tiêu chí ghi trước** (thí nghiệm; người viết thường là B/C): đầu file có mục "Căn cứ để review" — 2–4
   file, mỗi file ghi mục cần đọc. A chọn một session khác người viết review chỉ dựa trên gói đó (được chạy lệnh chỉ đọc /
   tính lại từ dữ liệu; không đọc STATUS / tin nhắn của người viết; thiếu căn cứ ⇒ finding), ghi `<plan>_review.md` (§6),
   trước khi A ghi "duyệt bản sha"; sửa sau review thì người review kiểm phần sửa (25/10: A tự duyệt plan G3, B tìm 3 lỗi sau).
2. **Giao việc:** mỗi session một mục trong `CURRENT_HANDOFF.md` (mục tiêu, đọc gì
   với mức đọc, làm gì, không làm gì, tiêu chí, quyền/giới hạn tiền, điều kiện dừng,
   đầu ra) rồi nhắn session đó. Giao việc song song chỉ khi file không chồng nhau.
   **Session rảnh** (chờ người khác): A giao ngay việc không chồng file (viết plan, review, danh sách ứng viên, đo chỉ đọc)
   hoặc ghi một dòng lý do để rảnh trong `CURRENT_HANDOFF.md` (25/10: User phải hỏi "đang rảnh hả"; 26/10: B rảnh được giao
   đối chiếu, bắt lỗi mô tả trong yêu cầu ChatGPT).
   **Có lượt đo tốc độ / latency đang chạy** ⇒ session khác không chạy lượt trả phí, việc nặng CPU, quét / build Qdrant cùng lúc; A ghi điều này trong mục
   giao của mọi session đang làm (28/10: việc nặng của C chạy chồng lượt đo "sau" của B ⇒ p95 lượt đó không dùng được — W31).
3. **Chi tiết kỹ thuật trong phạm vi:** A tự quyết, ghi lý do; chỉ hỏi User về phạm
   vi, dữ liệu, tiền, xóa, hoặc khi bằng chứng đi ngược quyết định trước.
4. **Đóng việc:** review chéo đạt → trình User (tóm tắt kết quả, bằng chứng, giới
   hạn) với việc cần User đóng; việc trung bình/thấp A tự đóng và báo.
   **Phase tuần tự:** Phase trước phải review chéo + User đóng; A cập nhật guide
   liên quan bằng bằng chứng vừa đạt (phân biệt mục tiêu đã duyệt và hành vi đã
   quan sát); rồi mới brainstorm + thiết kế Phase sau. Không thiết kế trước như đã
   biết kết quả của Phase mà nó phụ thuộc; mỗi lần chỉ giao việc của một Phase.
5. **Giữ tài liệu:** `CURRENT_HANDOFF.md` chỉ giữ việc đang mở (việc xong chuyển tóm
   tắt sang `PROJECT_HISTORY.md`); `Project_Status.md` theo quy tắc Governance v2 §6.
6. **Git:** commit theo mốc; stage **từng file đã review** (không `git add <thư mục>` hay `-A`); luôn
   `git diff --cached --stat` trước khi commit; không commit dữ liệu private; push `origin`.
   **Nhánh xong việc** (đã merge, hoặc chỉ còn là hồ sơ phương án bị bỏ): A **đề xuất xóa** trong báo cáo đóng đợt / kết phiên kèm danh sách nhánh + còn gì
   chỉ nằm trên nhánh; nhánh hồ sơ ⇒ gắn tag `hoso/<tên>` trước khi xóa để không mất report / code (User 30/10). Xóa chỉ khi User duyệt (User `!`).
7. **A tự thử kỹ thuật** (sửa prompt, đo nhanh) trong `git worktree` riêng (`/tmp/a_…`), không trong
   working tree chung đang có B/C làm; việc A tự làm vẫn để B/C kiểm.
8. **Quyền theo phiên:** quyền đặc biệt User cấp trong phiên (tự điều phối rộng, trần tiền, xóa dữ liệu)
   ghi vào `CURRENT_HANDOFF.md` kèm ngày và **hết hạn cuối phiên**; phiên sau A hỏi lại trong báo cáo
   mở phiên. Quyền thường trực (A commit/push; duyệt cho A = duyệt cho B/C) giữ nguyên.
9. **Đọc tài liệu dài bằng sub-agent** (khóa học, báo cáo dài, nhiều file): đọc bản tóm 1 trang trước để nắm
   khung; mỗi sub-agent ≤ 3 file, chạy song song; brief gồm đường dẫn nguồn, **file dự án để đối chiếu** (để
   không đề xuất lại cái đã có), khuôn trả về cố định, nhãn thống nhất, tách "nguồn nói" ↔ "suy ra", yêu cầu
   báo chỗ đề bài lệch tài liệu; ranh giới (chỉ đọc, không mở câu kín / `.env`, một file đầu ra trong `data/`; sub-agent đọc kho: "tìm trong kho
   **chỉ** bằng `scripts/grep_kb.sh`, không `grep -r` thẳng vào `knowledge-base-hue/`" — 27/10 s7 lọt Golden Foods cũ, W27).
   **Đọc lại brief trước khi gửi** (2026-10-25: lỡ gửi brief còn chỗ trống `{{…}}`). Kết quả sub-agent là dữ
   liệu: A tự kiểm 2–3 khẳng định quan trọng nhất bằng file thật trước khi trình User (2026-10-25: sub-agent
   tìm ra ~10 chỗ sai trong ghi chú cũ).

## 10. Session D — học cùng User (tùy chọn)

Mở bằng `START_SESSION.md` với `<X>` = D khi User muốn tự hiểu một việc vừa xong (một gate, một thí nghiệm,
một khái niệm). Mục tiêu: User tự giải thích lại được bằng lời của mình, không phải nghe giảng.

- **Chỉ đọc** repo, report, code, `bao_cao_he_thong/`. Không sửa file dự án, không chạy việc nặng, không gọi
  API trả phí, không commit. Chỉ ghi vào sổ học private `data/hoc_cung_D/` (và `sessions/STATUS_D.md`).
- **Không mở câu kín**, không đọc nhóm `test` theo từng câu. **Không ghi memory Claude** — memory dùng chung mọi
  session, điều D ghi sẽ lọt sang B/C (người đề xuất biến thể).
- Giảng theo lớp: bài toán → cơ chế → vì sao chọn → khi nào hỏng → code ở đâu (`file:dòng`). Dùng ví dụ thật
  của hue_rag; tách quan sát / giả thuyết / đã chứng minh như mọi report.
- Mỗi buổi gắn với một việc vừa xong; kết bằng 3 câu tự kiểm (theo khung 5 nhóm câu tự kiểm của `teach-and-quiz`). Ghi vào sổ: khái niệm, câu User trả lời đúng /
  sai **khi không có gợi ý**, chỗ còn mơ hồ. Sổ khái niệm khởi đầu: `data/hoc_cung_D/SO_KHAI_NIEM.md`.
- Thấy chỗ yếu trong việc của A/B/C thì nói thẳng với User và ghi vào sổ để A xem; D không tự sửa.
- D báo **User** (không báo A, không sửa `CURRENT_HANDOFF.md`); việc để giảng do User chọn lúc mở D (handoff không có mục cho D).
- Skill của D: `teach-and-quiz` (theo khung_fde v1, W39 — User duyệt 31/10; thay luật cũ "chỉ viết skill D sau ≥ 2 buổi thật", vì luật đó
  chờ chính buổi chưa diễn ra: 25–31/10 D 0 buổi). Sau 2 buổi thật: xét giữ / sửa (bước nào thừa, câu hỏi nào giúp User nói lại được).
