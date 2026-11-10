# Review: spec Phase 9 bản 13 (§12 "Sửa đổi 08/11/2026") — vòng 1

Người kiểm: B (Claude Code, `hue-rag-a1`) · Date: 10:53 08/11/2026 (`date`)
Đối tượng: `docs/superpowers/specs/2026-11-02-phase-9-design.md` §12 (dòng 491–608), sha256 **`0845b1caefbc`** (B tính từ file working tree chính, chưa commit).
Căn cứ dùng: gói căn cứ của spec — `CURRENT_HANDOFF.md` mục 2d (quyết định User 08/11) + `data/phase_9/dinh_tuyen_2/bo_do_nhap.md` (nháp bộ đo + 4 quyết định A)
+ code `main` `56b8baa` (chỉ đọc). Không đọc `STATUS_C.md` hay tin nhắn của C.

## 1. Phạm vi đã review

- §12.1–§12.8: việc + thứ tự, 5 dòng khám phá, sàn S1–S6, bộ đo / bộ kín, thiết kế G / T1–T4, bảng rà AI FDE, tiền + luật cắt, User xác nhận.
- Đối chiếu quyết định User 08/11 (handoff 2d): bỏ tuyến khẩn cấp · cổng 2 nhóm chạy mọi câu, giữ #6 · ngoài phạm vi ⇒ agent Huế tự từ chối, sàn 0 · 4 công cụ ·
  trần 3,5 (quỹ B7 0,35) · thứ tự đợt 1 / đợt 2 · A quyết: ngoài phạm vi = câu cố định riêng ⇒ code đóng cổng web; "hỏi về trợ lý" = xã giao; `tuyen_sealed` = đã dùng.
  **Khớp** cả 8 điểm.
- Đối chiếu `file:dòng` với code `main` `56b8baa`: `_pick_route` `assistant.py:742-768` ✓ · `web_gate_open` `:777-785` (chỉ mở với `INSUFFICIENT_ANSWER`) ✓ ·
  `MODEL_SEARCH_LIMIT = 2` `:52` ✓ · `OUT_OF_SCOPE_ANSWER` + `REFUSAL_ANSWERS` `full_corpus_prompt.py:49-50` ✓ · `today_line: false` `settings.yaml:62` ✓ ·
  sha `ROUTER_INSTRUCTIONS` trên `main` = **`164bd4a254e9`** (B tính) ⇒ dùng lại mốc B143 hợp lệ.

## 2. Findings

### M-1 (major) — G: câu ngoài phạm vi do agent trả sẽ **mất `outcome = "out_of_scope"`** ⇒ giao diện, gợi ý (5), log đổi theo mà spec không nói

- Vị trí: §12.5 G ("`ROUTE_NGOAI_PHAM_VI` thành nhãn lịch sử", "Agent Huế: thêm một câu lời dặn … trả **đúng** `OUT_OF_SCOPE_ANSWER`").
- Bằng chứng (code `main`): `outcome "out_of_scope"` **chỉ** được đặt ở nhánh định tuyến `assistant.py:766-767` (`_set_fixed(trace, OUT_OF_SCOPE_ANSWER, "out_of_scope")`)
  — đúng nhánh G gỡ. Các chỗ đang dựa vào outcome này:
  - giao diện: 3 câu gợi ý dưới câu ngoài phạm vi (`frontend/src/chat.jsx:322` `turn.outcome === "out_of_scope"`);
  - gợi ý cách hỏi (5) vừa merge: `api/routes/chat.py:466` gắn `tu_choi_kho` khi `refusal` ∧ outcome ≠ `out_of_scope`;
  - log `chat_metrics.outcome` (đếm S2 / S6 "báo USD / câu ngoài phạm vi").
- Tác động: sau G, câu ngoài phạm vi (agent trả `OUT_OF_SCOPE_ANSWER`) ra `outcome = "success"` + `refusal` ⇒ **mất** 3 câu gợi ý cũ, **hiện** gợi ý "gõ đúng tên nơi, món…"
  của câu kho thiếu (sai ngữ cảnh — trái tiêu chí (5) "không dưới câu ngoài phạm vi"), log không còn tách được câu ngoài phạm vi.
- Tiêu chí đóng: §12.5 G ghi một dòng — **code** nhận chữ câu trả lời = `OUT_OF_SCOPE_ANSWER` (so sau `strip()`, như cờ `refusal`) ⇒ đặt outcome `out_of_scope`
  (cùng đường như câu cố định cũ: không kiểm citation, cổng web đóng, nhớ như cũ); plan G thêm test cho cả 3 chỗ trên. Không thêm lần gọi model.

### M-2 (major) — G: thiếu sàn cho lỗi **mới** do chính G sinh ra: agent trả `OUT_OF_SCOPE_ANSWER` cho câu **về Huế**

- Vị trí: §12.3 (S1–S6), §12.2 dòng G.
- Lý do: trước G, quyết "ngoài phạm vi" là định tuyến (có sàn S3 cho chiều Huế ⇒ xã giao). Sau G, quyết đó chuyển vào **lời dặn agent Huế** ("câu không về văn hoá /
  du lịch Huế ⇒ `OUT_OF_SCOPE_ANSWER`"). Lỗi mới có thể có: câu về Huế ở rìa (đi Huế từ tỉnh khác, so Huế với nơi khác, câu chỉ hỏi kèm một ý ngoài Huế) bị agent trả
  "Mình chỉ hỗ trợ thông tin về Huế" ⇒ người dùng mất câu trả lời, **và** cổng web cũng đóng (S2c chỉ bắt ở 17 câu web).
  - S3 chỉ đo định tuyến; S4 (chấm mù 30 câu) có thể bắt một phần nhưng không đếm; S2c chỉ 17 câu web.
- Tiêu chí đóng: thêm **S3b** "câu về Huế ⇒ agent trả `OUT_OF_SCOPE_ANSWER`": **0** trên các lượt cả-câu-trả-lời đã có trong kế hoạch (an toàn 32 · mẫu Golden 30 ·
  7 + 10 câu S2c · phần "về Huế" của bộ (a) · Huế 30 nếu chạy cả câu), ×2. Đếm bằng code (so chuỗi) ⇒ **0 USD thêm**.

### m-1 (minor) — T3 "0 câu model tự diễn đạt điều kiện" chưa nói cách đếm và điều kiện có đi vào model không

- §12.2 T3 + §12.5 T3: "điều kiện miễn giảm do code nối nguyên văn"; "câu miễn giảm **luôn** nhận khối điều kiện do code nối khi có dòng bảng".
- Chưa rõ: (a) kết quả công cụ cho model có chứa chữ điều kiện không — nếu có, model sẽ diễn đạt lại (đúng lỗi B5c); (b) "câu miễn giảm" do code dò thế nào, hay mọi lượt
  có dòng bảng đều nối; (c) đếm "model tự diễn đạt" bằng code hay sub-agent đọc.
- Đóng: plan T3 ghi (a)(b)(c). Gợi ý đơn giản nhất: kết quả công cụ cho model **không** chứa chữ điều kiện (chỉ "có điều kiện miễn giảm — hiện bên dưới"), code nối khối khi
  dòng bảng có điều kiện ⇒ đếm "model nêu tuổi / đối tượng miễn giảm" bằng code + sub-agent đọc câu khớp.

### m-2 (minor) — T1: tiêu chí "0 ngày / thứ sai (L2) **do code**" bỏ ngỏ chữ model; bộ test âm lịch nên có năm Việt Nam ≠ Trung Quốc

- Model vẫn có thể không gọi công cụ và tự viết ngày / thứ ⇒ sàn nên là **0 ngày / thứ sai trong chữ trả lời** (đối chiếu đáp án theo ngày chạy), không chỉ phần code.
- "Test ≥ 10 ngày Tết / rằm công khai": nên có **≥ 1 ngày mà lịch Việt Nam (UTC+7) khác lịch Trung Quốc (UTC+8)** — vd Tết Đinh Hợi 2007 (VN 17/02, TQ 18/02) — để test chứng
  minh đúng lý do chọn UTC+7; không thì test vẫn đạt với thư viện lịch Trung Quốc. B chưa kiểm nguồn công khai cho ngày cụ thể — người viết plan kiểm.

### m-3 (minor) — số đo chưa khớp nhau

- G yêu cầu "S1, S2, S2b, S3 đạt **×2**" (§12.2) nhưng S3 ghi "Golden 176 (chỉ định tuyến, **1 lượt**)" (§12.3) ⇒ ghi rõ Golden 1 lượt hay ×2.
- T2 "câu kho trả lời được mà vẫn tra web **≤ 2 %**" trên mẫu Golden 30 ⇒ 2 % của 30 = 0,6 ⇒ ghi bằng số câu (≤ 0 / 30, hoặc nêu bộ lớn hơn).

### m-4 (minor) — T2: câu cố định trả cho model không được khiến câu kho "hứa" mục web

- §12.5 T2: kết quả công cụ "mục web sẽ hiện riêng — đừng nêu nội dung web". Model có thể viết "xem mục web bên dưới" trong khi tra web có thể lỗi / rỗng (B6 D3 câu cố định).
- Đóng: plan T2 viết câu cố định trung tính ("đã ghi nhận — viết câu trả lời từ kho như bình thường") + một ca test / đếm "câu kho nhắc mục web".

### m-5 (minor) — G đổi 2 lời dặn trong một bậc ⇒ plan ghi thứ tự đo

- G đổi lời dặn định tuyến (4 ⇒ 2 nhãn) **và** lời dặn agent Huế (câu ngoài phạm vi). Nháp `bo_do_nhap.md` §4 ghi "1 thứ đổi một lần (định tuyến trước, rồi lời dặn agent)".
  Hai thứ gắn nhau (bỏ nhãn ngoài phạm vi thì agent phải tự từ chối) nên không tách được hẳn ⇒ plan G ghi: vòng chỉnh định tuyến chỉ đo S3 / chỉ-định-tuyến; S2 / S2b / S3b
  đo trên bản có cả hai.

### Cần A / User xác nhận (không phải finding)

- **T2 — "agent tự gọi" theo nghĩa của spec:** agent chỉ **quyết lúc** tra; code tra **sau** câu kho; chữ web không bao giờ vào agent chính (mục web tách riêng như B6).
  Đây là cách **an toàn** (không mở bộ ba chết người, giữ closed-world) và khớp "Không đổi" của §12. Nhưng User nói "tra web thành công cụ agent tự gọi" — nếu User hình dung
  agent **đọc** kết quả web rồi viết chung vào câu trả lời thì khác hẳn. Đề nghị A hỏi User một câu trước khi duyệt: "agent quyết khi nào tra, nhưng chữ web vẫn hiện thành
  mục riêng 'Từ web (chưa kiểm)', agent không đọc — đúng ý bạn?".

### Ba quyết định C tự đặt (A nhờ xem kỹ)

1. **T2 `yeu_cau_tra_web()` không tham số, code tra sau câu kho, agent không thấy chữ web** — đúng khung AI FDE (§3 tham số do code điền; bộ ba chết người không mở); một
   chỗ luật cổng (`web_gate_open`). Đồng ý (kèm m-4 + câu xác nhận User ở trên).
2. **T3 không cộng / nhân, khối miễn giảm code nối nguyên văn** — đúng bài học B5c (âm 2 lần) + luật "phép tính / điều kiện ⇒ code". Đồng ý (kèm m-1).
3. **T1 âm lịch Việt Nam UTC+7, test ≥ 10 ngày công khai** — đúng (lịch Trung Quốc lệch ở vài năm). Đồng ý (kèm m-2).

### Câu hỏi về độ đơn giản

- Không thấy over-engineering chặn: mỗi công cụ một bậc + phương án B một dòng; cờ mới chỉ `tra_web_cong_cu`; bộ kín chỉ cho G (đúng luật cắt giảm 05/11 (2): chỉnh lời dặn
  qua nhiều vòng). S2 / S2b / S2c là 3 sàn khác nhau thật (trả lời · có web · mất web), giữ.
- G gỡ đúng phần cờ âm (`emergency_rule`, `is_emergency`, `EMERGENCY_ANSWER`, `ROUTE_KHAN_CAP`, PA1, giao diện khẩn cấp) — giảm code, khớp User.

## 3. Cách người kiểm chạy lại thật

Review tài liệu, 0 USD. Lệnh chỉ đọc: `sha256sum` spec; `grep` / `sed` đọc `assistant.py`, `full_corpus_prompt.py`, `api/routes/chat.py`, `frontend/src/chat.jsx`,
`settings.yaml` trên `main` `56b8baa`; tính sha `ROUTER_INSTRUCTIONS` bằng `uv run python` (`hashlib.sha256(...)[:12]`).

## 4. Kết quả quan sát

- 8 / 8 quyết định User 08/11 + A có trong spec, đúng nghĩa.
- 6 / 6 tham chiếu `file:dòng` đúng với `main`; mốc định tuyến `164bd4a254e9` còn nguyên.
- Tiền: G 0,25 + T1 0,11 + T3 0,10 + T2 0,19 + T4 0,14 ≈ **0,79** — B cộng lại khớp "≈ 0,8"; còn ≈ 1,1 (3,5 − 2,05 − 0,35) ⇒ **trong trần**. Phép tính từng dòng hợp lý
  với giá ghi (định tuyến ≈ 0,00008, lượt agent 0,0005–0,0008, mục web +0,0012).
- Sàn S1–S6 đo được bằng code (so chuỗi, đếm số, `chat_metrics`) trừ phần "câu không khớp ⇒ sub-agent đọc" (đã ghi); thiếu S3b (M-2).

## 5. Giới hạn hoặc phần chưa chạy

- Không mở bộ kín nào; không đọc nội dung câu trong các bộ (chỉ tên + cỡ ở `bo_do_nhap.md`).
- Ngày Tết 2007 VN / TQ ở m-2 là ví dụ B biết, **chưa kiểm nguồn** trong review này.
- Không kiểm lại các số đếm log ở `bo_do_nhap.md` §3 (247 lượt, 2 % hết giờ) — dùng như căn cứ của spec.

## 6. Decision và bước tiếp theo

**`changes_requested`** — 0 blocker · **2 major** (M-1 outcome ngoài phạm vi; M-2 sàn S3b) · 5 minor. Cả 2 major đóng bằng **thêm chữ vào spec** (một dòng G + một dòng sàn),
không đổi thiết kế, 0 USD thêm. Minor: plan từng việc xử lý, không cần vòng spec riêng. Vòng 2: B kiểm M-1 / M-2 bằng diff §12.

---

## Vòng 2 — B, 10:59 08/11/2026 (`date`)

Đối tượng: §12 sha256 **`89a48ca72cbd`** (B tính từ file working tree chính). Cách kiểm: `git diff HEAD -- docs/superpowers/specs/2026-11-02-phase-9-design.md` (HEAD
`5d5edde` chứa bản 13 vòng 1) — đọc mọi dòng đổi; 0 USD. Diff chỉ chạm §12 + dòng trạng thái đầu file.

| Finding vòng 1 | Phần sửa (§12) | Kết luận |
|---|---|---|
| **M-1** outcome ngoài phạm vi | §12.5 G: code nhận chữ = `OUT_OF_SCOPE_ANSWER` (so sau `strip()`) ⇒ outcome `out_of_scope` như câu cố định cũ; nêu đủ 3 chỗ phụ thuộc (gợi ý cũ, `tu_choi_kho`, log) + test cả 3 đường (`/api/chat`, stream, #6) | **đóng** |
| **M-2** sàn S3b | §12.3 thêm dòng **S3b** = 0, đếm bằng code trên các lượt cả-câu đã có, ×2, 0 USD thêm | **đóng** (kèm n-1) |
| m-1 T3 miễn giảm | §12.5 T3 (a) chữ điều kiện không vào model (b) code nối mỗi khi dòng bảng có điều kiện (c) đếm bằng code + sub-agent | đóng |
| m-2 T1 | §12.2: "0 ngày / thứ sai **trong chữ trả lời** … cả khi model không gọi công cụ"; §12.5: test có ngày VN ≠ TQ — Tết Ất Sửu 1985 (VN 21/01, TQ 20/02); B WebFetch en.wikipedia "Vietnamese calendar" 08/11: **khớp** (đông chí Hà Nội 21/12 / Bắc Kinh 22/12; miền Bắc đổi UTC+8 ⇒ UTC+7 ngày 08/08/1967) | đóng |
| m-3 số đo | S3 Golden **×2** (đã tính trong tiền G); T2 "**0 / 34**" (mẫu 30 + 4 câu "kho có" của B6, ×2) | đóng |
| m-4 T2 câu cố định | câu trung tính "đã ghi nhận — viết câu trả lời từ kho như bình thường" + plan đếm "câu kho nhắc mục web" = 0 | đóng |
| m-5 thứ tự đo G | §12.5 G: vòng chỉnh định tuyến chỉ đo S3 / chỉ-định-tuyến; S2 / S2b / S3b đo trên bản có cả hai lời dặn | đóng |
| Câu xác nhận User (T2) | §12.8 thêm: agent **chỉ quyết lúc** tra; code dựng câu tra, tra, viết mục web riêng; agent **không** đọc chữ web (User xác nhận 08/11/2026, A hỏi) | đã ghi |

### Finding mới vòng 2

- **n-1 (minor)** — dòng G ở §12.2 (cột tiêu chí) vẫn ghi "S1, S2, S2b, S3 (§12.3) đạt ×2", **chưa có S3b**. §12.3 có S3b và tiêu đề "Sàn chung … áp cho mọi việc có lượt
  trả lời" nên ý vẫn rõ ⇒ không chặn. Đóng: plan G liệt kê S3b trong luật ghi trước (hoặc C thêm "S3b" vào dòng G khi tiện — sửa chữ, không cần vòng review).

Không có thay đổi ngoài phạm vi trong diff; không đổi tiền (≈ 0,8) hay luật cắt.

### Decision vòng 2

**`ready_for_user_confirmation`** — 0 blocker · 0 major · 1 minor (n-1). Theo luật 2 vòng (`Session_Prompt.md` §7): vòng 2 chỉ còn minor ⇒ A duyệt sha; n-1 sửa lúc
viết plan G.
