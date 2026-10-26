# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 20:35 26/10/2026 (A, **mở phiên tối 26/10** — quyền phiên + việc B41 / B42 / C36 ở mục "Việc giao phiên tối 26/10"). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9.

## Việc giao phiên tối 26/10 (A 20:35)

User 20:3x trả lời: câu 1 (quyền, dưới) và câu 2 (đồng ý đề xuất của A: **khâu trả lời trước**; mốc đợt cải tiến = chatbot **context 10** sau B1;
cần B0). **User 20:4x "ok" — câu 3–7 theo khuyến nghị A:** (3) duyệt W14 + W18, W16, W17, W19, W20 (A sửa luật; W16 hook ⇒ B / C kiểm
trước commit); (4) 80 report lịch sử để nguyên; (5) giữ commit trước sửa + cổng ổn định sau mỗi gói; "báo trước, chờ User đồng ý" chỉ áp ngoài
phạm vi đã duyệt; (7) xóa nhánh `dot3` (đã nằm trọn trong `main`). Luật quyết đợt cải tiến (User 20:4x, chọn (a)): **nhận thay đổi khi chất lượng
không tụt quá mức cho phép ghi trước** (ví dụ Completeness ≥ −0,1 thang 5) **và rẻ / nhanh hơn rõ**; luôn so với **cùng một mốc gốc** (context 10), không
so nối tiếp. Còn chờ User: câu 8 (`tham khảo 26_10/`), B0 khi tiện.
- **User 21:1x:** phạm vi đợt cải tiến = **B** (khâu trả lời + thí nghiệm khâu tìm, không ghi Qdrant); **luật nhận (i)** cho thay đổi
  chất lượng tăng nhưng tốn hơn: nhận khi chỉ số quyết vượt nhiễu (CI 95 % > 0) **và** latency thêm ≤ 50 ms / câu, 0 USD thêm; biến thể chậm
  hơn / tốn hơn (ví dụ V3 luna +3–5 s) ⇒ A trình User kèm số. Luật (a) giữ cho thay đổi "chất lượng giữ, rẻ / nhanh hơn". **A được tự đề xuất,
  thử, so sánh, tối ưu và chọn giải pháp** (trong trần 1 USD, review chéo, tiêu chí ghi trước). Đưa context 10 vào chatbot vẫn chờ B0. Hook quét cả
  câu kín: **đồng ý** (B45 review). `tham khảo 26_10/`: của User, không liên quan dự án — bỏ qua.
- **B45 — review phần quét câu kín của hook (B, A giao 21:17, 0 USD).** `git diff .githooks/ session_prompt/Project_Status.md`. Kiểm: chặn nhầm trên mọi
  file tracked (A đo 0 dòng `sealed`), ca dương mù (script tự chép một câu kín vào file thử, chỉ in nhãn + số dòng, gỡ ngay — **không in nội dung**),
  worktree không symlink. Giữ mù: không in / đọc nội dung câu kín, không in tên file tracked nào trùng `sealed`. Đầu ra
  `report_agent/2026-10-26_cai_tien_tung_khau/hook_sealed_review.md`.
- Review: C36 ready (`phan_loai_loi_C_review.md`); B41 ready (`report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_rebase_review.md`) — merge sau B0.

Chung cho B41 / B42 / C36: chỉ đọc dữ liệu private đã có; **không mở câu kín**; nhóm `test` chỉ đếm (không đọc từng câu); report tracked không chép
câu hỏi / đáp án / nội dung kho (chỉ chỉ số câu `case_index`, số đếm, loại lỗi); bảng chi tiết từng câu để `data/cai_tien_tung_khau_2026-10-26/`.
File kết quả ChatGPT (`gửi chatgpt/2026-10-25/kết quả nghiên cứu/HUE_RAG_NGHIEN_CUU_CAI_TIEN_TUNG_KHAU_2026-10-26.md`) **được đọc** (private, không phải câu kín) —
nhãn lỗi theo **§6 mục 5** của file đó: `missed evidence`, `noisy evidence`, `wrong table association`, `unsupported claim`, `incorrect citation ID`,
`under-answer`, `over-refusal`, `format`. Khai báo file trong `STATUS_<X>.md` trước khi ghi. Script tạm để `data/cai_tien_tung_khau_2026-10-26/tools/`.
Xong: report + STATUS + dòng của mình ở bảng Session ⇒ nhắn A. Dừng khi: phải đụng file người kia khai báo; cần gọi API; thấy dữ liệu lệch report gốc.

- **B41 — B1 8.2 lên `main` mới (B, 0 USD).** Làm trong **worktree riêng** `/tmp/b_p82b1` (không `git switch` trong working tree chung — A, C đang
  ở `main`); bẫy worktree: `Project_Status.md` §8 (`uv run --project /home/minhhieu/hue_rag …`, symlink `data/` + `knowledge-base-hue/` gỡ khi xong;
  push từ working tree chung: `git push --force-with-lease origin p82-b1` không cần switch). Rebase `p82-b1` lên `main` mới nhất (`origin/main`), giải xung đột
  (`sua_dot3_review.md` §6, `sua_1b_plan.md` §6), test 4 file của B1, **T1** (158 câu giống byte `cefb2d1ad609`). **T2**: nếu cần lượt sinh mới (gọi
  `gpt-6-luna`) ⇒ **dừng, báo A ước tiền** — User duyệt bước này là 0 USD. Quyền: **B commit + `push --force-with-lease` nhánh `p82-b1`** (User 20:3x).
  Không merge vào `main` (merge sau B0 + A review). Đầu ra: thêm mục "Rebase 26/10" vào `phase_8_2_b1_implementation.md` trên nhánh.
- **B42 — phân loại lỗi tầng tìm (B, sau B41 hoặc xen khi chờ, 0 USD).** 40 câu dev có đoạn đúng (`data/phase_8_1/gold/gold_draft.jsonl` ∩ dev của
  `split.json`); top-10 runtime (`data/phase_8_1/g1/runtime_k10.jsonl` hoặc file B thấy đúng — ghi rõ) + pool 30: câu nào thiếu đoạn đúng ở top-5 / top-10 /
  pool 30, thiếu vì sao (`missed evidence` dense ngoài pool / BM25 chỉ xếp lại; một file chiếm chỗ — nối B40; hàng bảng). Đầu ra
  `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_B.md`.
- **User 22:03:** nguyên tắc "đo theo mục tiêu sản phẩm cuối cùng" (a) ⇒ `Session_Prompt.md` §7; **chất lượng trước, tốc độ / tiền sau** ⇒ K3 được thử
  (trần 5 s chỉ theo dõi); R1 nhận khi USD ≤ 0,95× **hoặc** output_tokens ≤ 0,9×. **Chờ User:** mục tiêu sản phẩm (người dùng là ai, "dùng được" là gì,
  lỗi tệ nhất, yêu cầu phi chức năng: chờ tối đa / tiền tối đa / chạy ở đâu); Q2 (test = "không làm hỏng"); B0.
- **Spec 8.2 §10 "Sửa đổi 26/10" — A duyệt bản sha `09e8f3932ede` (21:36)** sau review C38 2 vòng ready (`spec_8_2_s10_review.md`); User duyệt
  phạm vi + luật (i) + Q1 (21:1x–21:3x) và cho A tự chọn trong luật. **Q2** (test = "không làm hỏng") chờ User — không chặn K1 / R4 (chỉ ảnh hưởng
  bước xác nhận test). Nguyên tắc User 21:3x "chất lượng cần thiết trước, tối ưu hiệu suất sau" ghi `Session_Prompt.md` §7 + `run-experiment` (C kiểm).
- **C41 (trước C39) — review plan K1** (`report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k1_plan.md`, B, sha `ad71594e17e7`) chỉ dựa trên mục
  "Căn cứ để review" của plan (WORKFLOW §9.1); đầu ra `phase_8_2_k1_plan_review.md`. A trả lời §7 của plan: (1) sàn 120 / 168 chỉ của khâu trả lời — với
  K1 chỉ theo dõi; (2) ngưỡng 5 / 0 cố định; (3) quyền B commit + push `p82-k1`, paid ≤ 0,04 USD, judge sub-agent — ghi khi A duyệt sha.
- **C43 — chạy R2 (C, A duyệt plan `phase_8_2_r2_plan.md` bản sha `aa808a85184c` lúc 22:08)** sau B49 2 vòng ready (`phase_8_2_r2_plan_review.md`; ghi chú
  chữ dòng 99 "tất định" không đổi tiêu chí — để nguyên, không đổi sha). Spec hiện hành `cd910c4c4169`. Quyền: **C commit + push nhánh `p82-r2`**
  (worktree `/tmp/c_r2`, từ `811d25d`); **paid ≤ 0,06 USD** (`gpt-6-luna`, pilot trước); judge Claude sub-agent. Không merge `main`. Thắng ⇒ **trình User**
  (đổi hợp đồng trả lời, D4) kèm ~10 câu mẫu. Report `phase_8_2_r2_implementation.md` ⇒ B review.
- **K1 (B48) xong: kém hơn** (phạm sàn câu 154; 2 / 37 / 1) — C42 ready. Báo cáo trên nhánh `p82-k1`.
- **B48 — chạy K1 (B, A duyệt plan `phase_8_2_k1_plan.md` bản sha `b8f1597f6a0f` lúc 21:50)** sau C41 2 vòng ready (`phase_8_2_k1_plan_review.md`).
  Quyền: **B commit + push nhánh `p82-k1`** (worktree `/tmp/b_k1`, từ `811d25d`); **paid ≤ 0,04 USD** (`gpt-6-luna`, chỉ lượt sinh khi qua tầng tìm, pilot
  10 câu trước); judge Claude sub-agent (quota). Không merge `main`, không ghi Qdrant. Report `phase_8_2_k1_implementation.md` ⇒ C review.
- **C39 — R4 thước "số trong câu trả lời có trong đoạn được trích" (C, A giao 21:36, 0 USD).** Spec §10.3 dòng R4. File mới
  `backend/experiments/phase_8_2/r4_numbers.py` (working tree chung, không đụng production / file B khai báo); hàm thuần đọc câu trả lời + nguồn được trích
  đã lưu; bỏ số có trong câu hỏi; chuẩn hóa khoảng số / dạng viết (C37 §3). **Kiểm thước trước** trên 5 ca C36 đã biết (2 lỗi thật, 3 báo nhầm) — ghi
  trước tiêu chí: bắt 2 / 2, báo nhầm ≤ 1 / 3. Rồi chạy trên mốc B1 (`data/phase_8_2/b1/b1_{dev,test}.jsonl`) + G2.1a: đếm câu bị cờ (chỉ số câu). Test
  nhỏ cho logic thuần (practical-project-coding). Report `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r4_implementation.md`; B review. Không commit.
- **C40 (sau C39) — sửa plan E1 thành plan R2** theo C37 §3 / spec §10 (mốc `811d25d`, `paired_stats` / `false_refusal`, citation v2, trần 5, sàn 120 / 168,
  luật (i) + mức tụt §10.2, cỡ mẫu 5 / 5) ⇒ sha mới ⇒ B review ⇒ A duyệt. Chưa chạy lượt có phí.
- **B43 — bản nháp phần khâu tìm cho tài liệu thiết kế đợt cải tiến (B, A giao 20:57, 0 USD, không chạy thí nghiệm mới).** Vì sao: C36 + B42 cho thấy ở
  mốc context 10 phần thiếu còn lại chỉ sửa được ở tầng tìm ⇒ A trình User lại phạm vi (khuyên thêm một thí nghiệm tầng tìm **không ghi Qdrant**).
  Làm: liệt kê ≤ 5 biến thể không ghi Qdrant (ví dụ giới hạn đoạn mỗi file / MMR trên pool 30, trọng số gộp dense–BM25, pool dense ∪ BM25 cả kho
  **kèm** xếp lại, rerank luna trên pool); mỗi biến thể: 8.1 đã đo gì (`file:dòng` trong `report_agent/2026-10-24_phase_8_1_ra_soat/`, không đề xuất
  lại cái đã bác), nhóm câu B42 nó nhắm (theo cơ chế, chưa đo), tốn gì (tiền / latency CPU), rủi ro hỏng câu khác, **tiêu chí đề xuất ghi trước** theo
  `run-experiment` (sàn, mức tụt cho phép theo luật (a) của User — Completeness ≥ −0,1, chỉ số quyết, cỡ mẫu thật dev / test), thứ tự đề xuất.
  Chỉ đọc report + dữ liệu đã có; được tính lại từ `b42_per_case.jsonl` / G1; không gọi API, không chạy retrieval mới. Đầu ra
  `report_agent/2026-10-26_cai_tien_tung_khau/de_xuat_khau_tim_B.md` (≤ ~120 dòng). Đây là **đầu vào** cho tài liệu thiết kế của A, không phải plan duyệt.
- **C37 — bản nháp phần khâu trả lời cho tài liệu thiết kế đợt cải tiến (C, A giao 21:17, 0 USD, không chạy thí nghiệm mới).** Như B43 nhưng cho
  khâu trả lời, trên mốc context 10: ≤ 5 biến thể (ví dụ mức suy luận `none` / `low`; trả lời phần có căn cứ thay vì từ chối cả câu — P1 làm lại có sàn
  out_of_scope; câu prompt "nêu đủ chi tiết có trong bằng chứng"; kiểm citation bằng code). Mỗi biến thể: 8.1 / rà code đã đo gì (`file:dòng`), nhóm câu
  C36 nhắm, luật nhận áp dụng — **(a)** (chất lượng giữ ≥ −0,1 Completeness + rẻ / nhanh hơn rõ) hay **(i)** (chất lượng tăng vượt nhiễu, ≤ +50 ms,
  0 USD thêm; tốn hơn ⇒ trình User), tốn gì (ước USD lượt sinh + judge), nhiễu A/A dùng được (B1 §4), cỡ mẫu thật, tiêu chí YAML ghi trước, thứ tự.
  Nguồn: `phan_loai_loi_C.md`, `ung_vien_cai_tien_C.md`, báo cáo ChatGPT C1–C5, plan E1 (`phase_8_2_e1_plan.md`) + spec 8.2 E1–E3 (không đề xuất lại
  cái đã bác; nói rõ E1 / E3 của 8.2 trùng chỗ nào). Đầu ra `report_agent/2026-10-26_cai_tien_tung_khau/de_xuat_khau_tra_loi_C.md` (≤ ~120 dòng).
- **C36 — phân loại lỗi tầng trả lời (C, 0 USD).** Nguồn: lượt **`g2_context10`** (mốc đợt = context 10) — câu trả lời `data/phase_8_1/g2/g2_context10.jsonl`,
  điểm judge `data/phase_8_1/g2/judge/` (mù: `map.json` sha `33b4c9603f20` nối item ↔ lượt, cách đọc ở `phase_8_1_g2_implementation.md` dòng ~35); so phụ
  `g20_baseline` (context 5) để biết lỗi nào context 10 đã sửa. Phạm vi: dev chính (dev, bỏ `unnatural`, trong phạm vi — 88 câu như B1 §4). Mỗi câu
  Completeness / Accuracy ≤ 3 hoặc từ chối: gắn nhãn §6.5 (nhiều nhãn được), ghi căn cứ ngắn. Đầu ra
  `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_C.md` (bảng đếm theo nhãn × loại câu; kết luận "lỗi nào chiếm tỷ trọng").
Chỉ giữ việc đang mở; việc đã xong: `report_agent/2026-10-25_ra_soat_code/TONG_HOP.md`, `PROJECT_HISTORY.md` (mục 26/10 16:0x).
Bản handoff đầy đủ trước khi rút gọn (chi tiết đợt 1–2, rà code B25 / C34): `git show 76ff419:session_prompt/CURRENT_HANDOFF.md`.

## PHIÊN SAU — ĐỌC TRƯỚC NHẤT

**Hệ thống (16:0x 26/10):** `main` (commit cuối `git log -1 main`). **Sửa code sau rà soát xong cả 5 gói** — đợt 3 merge `421c302` (`--no-ff`, giữ
sha B review), cổng ổn định trên `main` đạt (A 16:0x: 8.459 đoạn sha `60591acff422ece6` + identity = record; T1 158 dòng `cefb2d1ad609`; pytest
197 p / 1 f / 4 e = phần cần key; `/health` 5 / 5, 1 câu trong kho có nguồn, 1 câu ngoài kho từ chối, log 0 lỗi). Chatbot vẫn context 5, chưa NFC,
reasoning mặc định (`medium`, không gửi tham số). Qdrant `:6335` còn **1** collection (8.459). Repo `chatbot-hue` **PUBLIC**. File untracked
`báo cáo nghiên cứu github.txt` ở gốc: của User (Phase 9) — **không đụng**. 8 file `reports/artifacts/` chứa nguyên văn kho ⇒
`data/reports_artifacts_private_2026-10-26/` (User chọn (a) 26/10), gỡ khỏi repo.

**Nhánh đang mở:** `p82-b1` (`f23d396`) — B1 của 8.2 (context 10 + NFC), chưa review; rebase lên `main` mới sẽ xung đột thêm (đợt 3 gỡ Rep B ở
`settings.yaml` / `settings_loader.py` / `test_phase6_settings.py`, `minilm` + `REPO_ROOT` ở `retrieval/full_corpus.py` — `sua_dot3_review.md` §6) — B xử lý
khi A giao (mục Thứ tự, bước 5). `dot3` đã merge (giữ nhánh trên origin tới khi User bảo xóa — câu 7). 4 nhánh / worktree AGY
`subagent-Monuments-Reviewer-*` (dưới `~/.gemini/`, ở `c725987`): không phải của A/B/C — **giữ nguyên, không đụng**.

**Mã hay gặp:** T1 = kết quả tìm 158 câu (mốc sha `cefb2d1ad609`); T1–T5 của B1 = 5 phép kiểm trong `phase_8_2_b1_implementation.md` §4 (nhánh
`p82-b1`); D1–D9 = cổng đợt 3 (`sua_dot3_plan.md` §5); T-C = `test_startup_model_missing.py` (User `!`); B-xx / C-xx = mã phát hiện rà code
(`ra_soat_code_{B,C}.md`); S / W / I = sự cố / thay đổi trong sổ cải tiến; E1–E3, B0, B1 = bước của spec 8.2; A/A = chạy lặp cùng cấu hình đo nhiễu.

**Mạch việc:**
1. **Đợt tìm hướng tốt hơn từng khâu** (User 20:0x 25/10; đợt `report_agent/2026-10-26_cai_tien_tung_khau/`) — kết quả ChatGPT có, A đối chiếu 3 nguồn
   chính (khớp), B40 đối chiếu với code xong. **Chờ User chọn phạm vi** (câu hỏi 2). Mục "Việc đang mở" dưới.
2. **Phase 8.2 — TẠM DỪNG**, nay đủ điều kiện chạy lại (5 gói xong + cổng ổn định). Cần B0 (User đọc cặp mù) trước khi đưa context 10 vào chatbot.

**Thứ tự việc phiên sau:**
1. Mở A / B / C bằng `START_SESSION.md`; A `ListAgents`, cập nhật bảng Session; A **hỏi lại quyền phiên** (§9.8); kiểm `git branch --show-current` =
   `main`, `git status` sạch (trừ file untracked của User), Qdrant 1 collection 8.459.
2. **A trình User** các câu hỏi dưới (gói gọn trong báo cáo mở phiên; mỗi câu có lựa chọn + khuyến nghị — đã nói với User 26/10):
   câu 2 (phạm vi đợt cải tiến + thứ tự B0 ⇒ B1 ⇒ cải tiến), câu 3 (sổ cải tiến), câu 4 (80 report lịch sử), câu 5 (luật sửa code có giữ cho đợt sau).
3. **B, C rảnh trong lúc chờ User ⇒ A giao việc chỉ đọc, 0 USD** (W17), không chồng file. Gợi ý A định sẵn: **phân loại lỗi theo câu** trên kết quả 8.1 đã có
   (`data/phase_8_1/g2/*.jsonl` + điểm judge; loại lỗi theo báo cáo ChatGPT §6.5: thiếu bằng chứng / bằng chứng nhiễu / sai hàng bảng / nhận định không căn cứ /
   sai số citation / trả lời thiếu / từ chối thừa) — B lo tầng tìm (đoạn đúng 55 câu, pool 30 của G1), C lo tầng trả lời; đầu ra
   `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_{B,C}.md`. Chỉ nhóm **dev** (`split.json`; đoạn đúng: 40 câu dev trong 55); nhóm `test` chỉ đếm, không đọc từng câu; không mở câu kín.
4. User chọn phạm vi ⇒ A viết **một** tài liệu thiết kế `docs/superpowers/specs/` (tiêu chí ghi trước theo `run-experiment`, cỡ mẫu thật từ B40, trần tiền,
   mốc) ⇒ B hoặc C review (W11) ⇒ User duyệt một lần ⇒ giao chạy.
5. **8.2 chạy lại** (A quyết khi User trả lời câu 1–2 — điều kiện 5 gói xong + cổng ổn định đã đạt): phần code B1 chạy **song song** với B0 (spec 8.2 mục
   B0) — A giao B rebase `p82-b1` lên `main` + chạy lại T1–T2 (không tốn API: T1 tìm kiếm, T2 so trường đã ghi; B xác nhận khi nhận việc); mục việc ghi rõ
   quyền **B commit + `push --force-with-lease` nhánh `p82-b1`** (cần quyền phiên). A review B1; **merge chỉ sau B0** (User đọc) + áp luật dừng B0 ⇒ chatbot
   lên context 10 + NFC ⇒ cổng ổn định.

## Câu hỏi cho User (phiên sau)

1. **Quyền phiên** (điều phối rộng? trần tiền ≤ 1 USD?) — quyền 26/10 đã hết hạn.
2. **Phạm vi đợt cải tiến** — A khuyên **A. khâu trả lời trước** (mức suy luận `none` / `low` — runtime đang chạy `medium` mặc định; đa dạng nguồn — 56 / 158
   câu có cả 5 đoạn cùng một file; tách câu so sánh; kiểm citation bằng code), ~0,05–0,1 USD, không ghi Qdrant. B. thêm khâu tìm / dựng kho (BM25 trên cả kho,
   trọng số tiêu đề, hàng bảng — cần collection thử). C. thêm model embedding mới (`bge-m3` / `Qwen3-Embedding-0.6B` — ngoài danh sách duyệt; Qwen3-8B
   qua OpenRouter). **Kèm:** mốc của đợt = chatbot context 10 (sau B1) thay vì context 5 — **lệch handoff cũ**, A đề xuất vì đo trên context 5 rồi đổi
   sang 10 thì phải đo lại; cần B0 (câu 6) trước.
3. **Sổ cải tiến** (`session_prompt/SO_CAI_TIEN_CACH_LAM.md`) — A đề xuất: duyệt **W14** (nhắc lại ý User khi câu nhiều nghĩa) + gộp **W18** vào đó (đối
   chiếu spec khi đề xuất thứ tự); duyệt **W16** (quét trùng Golden / kho trong hook pre-commit, bác W15 — sự cố `;` lặp lần 2 ngày 26/10); duyệt **W17**
   (đã dùng thử 26/10: B40 bắt lỗi mô tả trong yêu cầu ChatGPT); mới **W19** (yêu cầu nghiên cứu ngoài: mô tả hệ thống kèm `file:dòng` / nhờ B, C đối
   chiếu trước khi gửi), **W20** (mẫu lệnh `date` cho giờ — ghi giờ ước lần 3).
4. **80 report lịch sử** còn dòng trùng kho ≥ 40 ký tự (`reports/` 70, `docs/superpowers/` 5, `handoff_prompt/` 4, `report_agent/` 1 — file đó 25/10, chỉ
   trùng tên file kho; ~960 dòng, nhiều chỗ là tên file / tiêu đề; 1 dòng trùng cả đáp án Golden — report 06/09, trước khi có Golden). A khuyên **(a) để
   nguyên** (hồ sơ lịch sử, nội dung từ trang công khai, public từ 09/2026); (b) sửa từng file; (c) chuyển cả 80 file sang `data/`.
5. **Luật sửa code phiên 25/10** ("báo cáo nên sửa gì trước, chỉ sửa khi User đồng ý; commit + push trước mỗi lần sửa code; cổng ổn định sau mỗi gói")
   ghi "giữ tới khi xong sửa code" — sửa code đã xong: giữ cho mọi lần sửa code về sau không? (A khuyên giữ cổng ổn định + commit trước sửa.)
6. **Đọc cặp mù (B0)** khi tiện: `data/phase_8_2/b0/nhan_xet_user.md`, 20 câu, ~30–45 phút — chỉ User làm được (mốc người; A giữ khóa) — cần trước B1.
7. (Sẽ hỏi trong tài liệu thiết kế) gửi danh sách mâu thuẫn kho C32 ra ChatGPT tra nguồn (đưa dữ liệu ra ngoài); xác nhận "suy luận none" trên test
   (~0,007 USD); xóa nhánh `dot3` trên origin (đã merge — C hỏi; A khuyên xóa, không mất gì vì commit nằm trong `main`).
8. Giữ từ trước (không gấp): route `/api/chat` chưa ghi số token / tiền (mọi số tiền cổng ổn định là ước — B, C đề xuất log usage); mâu thuẫn kho Hải Vân
   Quan (STATUS_B); rà kho C32 139 mục để đợt build lại index; tên dự án khác trong lịch sử git — để nguyên (gỡ lịch sử là phá hủy);
   3 câu kín A đã thấy — đã ghi trong spec 8.2 §3.7.

## Câu hỏi A còn nợ (phiên sau A trả lời, không cần User)

- Plan E1 (C, `phase_8_2_e1_plan.md` sha `f86240418ca1`) khi 8.2 chạy lại: **phải đổi** sang `paired_stats` + `false_refusal` (gói 3, C-02) và định nghĩa
  citation mới (1a) ⇒ sha mới ⇒ B review; §10 Q1 (test không đủ câu cho CI — "xác nhận hướng"?), Q2 (E1b hay thêm E1a), Q3 (A/A lấy từ B1 sau khi
  rebase + chạy lại).
- E2 (spec 8.2): sau 1a, mốc G2.0 và B1 còn **0** lỗi citation (`sua_3c_citation_v2.md`) ⇒ áp luật bỏ sớm ⇒ có thể NOT RUN — A ghi khi 8.2 chạy lại.
- Ghi chú B (vòng 3 spec 8.2): plan E3b thêm mức tụt Completeness / lỗi citation như E3a.

## Session

| Vai | Terminal | Agent | Liên lạc | Việc | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-2d` (tối 26/10) | Claude Opus 5.5 | trực tiếp | tối 26/10: giao B41 / B42 / C36; review C36 + B41 ready; ghi quyết định câu 3–7; xóa `dot3`; tiếp: sửa luật W14 / W16–W20, tài liệu thiết kế đợt cải tiến | `STATUS_A.md`; 0 USD |
| B — thực thi | `hue-rag-23` (tối 26/10) | Claude Opus 5.5 | trực tiếp | B41 ready (merge sau B0); B42 ready (`a7b61bb`). **B43 xong 21:01 — chờ A:** `report_agent/2026-10-26_cai_tien_tung_khau/de_xuat_khau_tim_B.md` — ở context 10, top-10 = context nên 8.1 G1.3 / G4-B đã đo đúng chỉ số; rerank chỉ trong top-10 vô ích; đề xuất V1 pool dense 100 (chưa đo, 0 USD) → V2 native p30 k=2 xác nhận test → V3 luna pool 30 (có phí, +3–5 s); không chạy V4 cap file (17 / 22 câu đủ có file đúng > 3 chỗ), V5 (latency); **luật (a) chưa phủ thay đổi tốn thêm mà chất lượng tăng — A / User chốt** · **B44** xong (4 file, chờ A commit) · **B45 review hook câu kín: ready; vòng 2 m-1 / m-2 đóng** (`hook_sealed_review.md`) · **B46 plan K1 vòng 2 (sau C41) sha `b8f1597f6a0f` — chờ C kiểm phần sửa**; `k1.py` viết xong trên `p82-k1` (chưa chạy, chưa commit) · **B47 R4 review ready** · **B48 K1 xong: kém hơn** (mất câu 154; nhánh `p82-k1` `a7710ed`, report `phase_8_2_k1_implementation.md`) — chờ C review · **B49 review plan R2: changes_requested 0/1/2** (`phase_8_2_r2_plan_review.md`) | `STATUS_B.md`; 0 USD |
| C — thực thi | `hue-rag-b5` (tối 26/10) | Claude Opus 5.5 | trực tiếp | C36 ready (`2d56193`); review W16 ready (`018c8dc`). **C37 xong 21:22 26/10/2026 — chờ A:** `report_agent/2026-10-26_cai_tien_tung_khau/de_xuat_khau_tra_loi_C.md` (R1 `none` luật (a), R2 = E1b, R3 'nêu đủ chi tiết', R4 thước; E2 NOT RUN); 0 USD | xem `STATUS_C.md` |

Tên terminal đổi mỗi lần mở: dùng `ListAgents`. Cả ba Claude Code ⇒ liên lạc `trực tiếp`.

## Quyền

- **Thường trực:** A commit/push `origin main`; B/C không commit (trừ khi việc ghi rõ — đợt 3: C commit / push **nhánh `dot3`**); duyệt cho A =
  duyệt cho B/C; thư viện nhỏ cần cho việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage token + tiền
  trong report; code luôn `uv run` trong `.venv`; thư viện thừa giữ nguyên; luôn thử + so baseline trước khi chọn (User 24/10 20:49).
- **Luật User phiên đêm 25/10 (giữ cho tới khi xong việc sửa code — sửa code XONG 26/10; phiên sau hỏi User có giữ, câu 5):** báo cáo "nên sửa gì"
  trước, **chỉ sửa khi User đồng ý**; **commit + push trước mỗi lần sửa code**; sau sửa hệ thống phải hoạt động bình thường, ổn định, tối ưu, đóng gói
  đầy đủ (cổng ổn định dưới); được thử nghiệm / so sánh / đánh giá để chọn cách tốt nhất; phase trước ổn định mới sang phase sau.
- **Phiên tối 26/10 (User 20:3x, hết hạn cuối phiên):** A tự điều phối B/C; API ≤ 1 USD cả phiên; **B commit + `push --force-with-lease` nhánh
  `p82-b1`** (rebase B1 lên `main` mới + chạy lại phép kiểm, 0 USD — B41).
- **Phiên 26/10 (User 14:1x) — HẾT HẠN:** A tự điều phối B/C rộng; API ≤ 1 USD cả phiên (dùng ~0,0028 USD ước); C commit / push nhánh `dot3`
  (đợt 3 — đã xong). Trần 8.2: 0,5 USD (spec; đã dùng 0,0369). Luật kỹ thuật giữ: GPU mỗi lượt 20–30 câu, kiểm GPU thật trước khi chạy.
- Giá `gpt-6-luna`: 0,1 USD / 1M token vào, 0,5 USD / 1M token ra (~0,000133 USD / câu context 5; ~0,000204 context 10).

## File private quan trọng (không commit)

| File | Nội dung | sha (12) |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test, seed 20261024 | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_draft.jsonl` | đoạn đúng 55 câu (40 dev / 15 test) | `bab707b9ab22` |
| `data/phase_8_1/golden_realism_final.jsonl` | độ tự nhiên 176 câu (82 / 65 / 29) | `0b65d1c138d2` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` | 36 câu kín chính thức — **không đọc** tới mốc cuối 8.2 | md5 `ddc59587b502` |
| `data/phase_8_1/baseline/g0_6_manifest.json` | manifest khóa G0.6 (hash mọi file mốc) — kiểm lại 22:3x: không đổi | `9ea480d0d083` |
| `data/phase_8_1/{g1,g2,g3,g4,g4k}/`, `data/phase_8_1/tools/` | kết quả từng câu các gate; script dùng lại | — |
| `data/phase_8_2/b0/` | đọc cặp mù: `doc_cap_mu.md` (`37b66efb3499`), `nhan_xet_user.md` (User ghi), **`khoa.json` chỉ A** (`5b9240842b7b`) | — |
| `data/phase_8_2/b1/` | kết quả chạy B1 | — |
| `data/ra_soat_kho_2026-10-25/` | rà kho C32: `danh_sach.md` 139 mục | — |
| `data/ra_soat_code_2026-10-25/citation_v2/` | lỗi citation tính lại theo validator mới, 14 lượt + `summary.json` (3c) | — |
| `data/ra_soat_code_2026-10-25/tools/` (gồm `dot3/`: D1, D4, D7, D8, D9 + mốc `t1_base.jsonl`, `3b_base.json`), `data/ra_soat_code/` | script + ghi chú rà / sửa code của C / B | — |
| `.githooks/overlap_scan.py` (tracked, không chứa dữ liệu; thay `data/tools/overlap_scan.py`) | quét trùng Golden / kho 40 ký tự — **hook pre-commit tự chạy** trên dòng thêm mới (W16); quét cả file: `uv run python .githooks/overlap_scan.py <file>` | — |
| `gửi chatgpt/2026-10-25/tìm thông tin/cai_tien_tung_khau_2026_10_25.md` | yêu cầu nghiên cứu đợt cải tiến (10 câu) | — |
| `gửi chatgpt/2026-10-25/kết quả nghiên cứu/HUE_RAG_NGHIEN_CUU_CAI_TIEN_TUNG_KHAU_2026-10-26.md` | kết quả ChatGPT (C1–C6, D1–D4, ma trận ưu tiên, giao thức đo) | `601b49a025ac` |
| `data/cai_tien_tung_khau_2026-10-26/tools/{counts,cover}.py` | script đếm của B40 (đa dạng nguồn, đoạn bảng, cỡ mẫu theo loại câu) | — |
| `data/reports_artifacts_private_2026-10-26/` | 8 file gỡ khỏi `reports/artifacts/` 26/10 (sha bằng bản trong git `421c302`) | — |
| `knowledge-base-hue/meta/{full_corpus_conditions.json, chunker_acceptance_samples.json, backup_b12_2026-10-26/}` | quy tắc điều kiện chunker (runtime đọc ở đây) + 55 chuỗi mẫu test chunker + sao lưu B-12 | conditions `b84a0a637bfc` |
| `data/tools/huegov_converters/` | 2 converter HueGov gỡ khỏi `backend/scripts/` (B-13) | — |

## Việc đang mở

### Luật chung khi sửa code (User 18:3x, 19:4x, 20:0x 25/10 — đợt 3 đã xong: `TONG_HOP.md` rà code; giữ mục này làm mẫu cổng ổn định)

- A commit + push `main` **trước** khi B / C sửa code; khai báo file trong `STATUS_<X>.md` trước khi sửa; skill `practical-project-coding`; test liệt kê
  file, không `--env-file` trừ khi mục ghi; report `sua_<gói>_implementation.md`; review chéo (người kia); plan có tiêu chí ghi trước ⇒ session khác
  review **trước** khi A duyệt sha (§9.1). Dừng khi: đường thật đổi ngoài dự kiến; phải đụng file người kia đang khai báo; vượt tiền.
- **Cổng ổn định sau mỗi gói:** (1) test các file chạm, lỗi cũ C-17 ghi rõ; (2) chạy thật `cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env
  uvicorn api.app:app --port 8011`: `/` 200, `/health` 5 / 5 ready, 1 câu trong kho (200, marker = `sources`) + 1 câu ngoài kho (từ chối) — câu tự viết,
  không Golden, body `{"query": …}`; log sạch; tắt server; (3) chạm tìm kiếm / chia đoạn: T1 giống byte, sha đoạn giống hệt; (4) 4 chỗ báo cáo nếu
  hành vi đổi; (5) quét trùng Golden / kho: hook pre-commit tự chạy (`.githooks/overlap_scan.py`, W16) — quét cả file người khác viết trước khi stage: `uv run python .githooks/overlap_scan.py <file>`; A commit + push.
- Test cần key OpenAI (không chạy mặc định): `test_api_chat.py` (C-17 đã sửa ở đợt 3: 3 test dừng trước generator chạy không key), `test_openai_full_corpus_generator.py`,
  `test_phase6_live_smoke.py`. Test thiếu model `tests/test_startup_model_missing.py`: auto mode chặn ⇒ User chạy `!` ở terminal session cần.

### Đợt tìm hướng tốt hơn từng khâu (User 20:0x) — chuẩn bị

User: "dựa vào kiến thức, tham khảo, trao đổi với B, C xem có thể thử nghiệm, so sánh, đánh giá để xem có hướng nào tốt hơn, tối ưu hơn, ổn định
hơn; giữ mốc hiện tại làm base; A, B, C được so sánh, thử nghiệm, rồi đưa ra kết luận; có thể nhờ ChatGPT nghiên cứu".
- Ứng viên: `report_agent/2026-10-25_ra_soat_code/ung_vien_cai_tien_{B,C}.md` (C 12 dòng trả lời / đánh giá; B 10 dòng dựng kho; ~0,08–0,09 USD mỗi bên nếu làm phần đầu).
- **Kết quả ChatGPT đã có** (User 14:1x 26/10): `gửi chatgpt/2026-10-25/kết quả nghiên cứu/HUE_RAG_NGHIEN_CUU_CAI_TIEN_TUNG_KHAU_2026-10-26.md`
  (private, 155 dòng; 10 câu C1–C6, D1–D4 + ma trận ưu tiên + giao thức đo). A đã WebFetch đối chiếu: ALCE 85,1 % / 77,6 % (khớp, phụ lục G.5);
  Anthropic contextual 5,7 → 3,7 → 2,9 → 1,9 % (khớp); trang model `gpt-6-luna`: effort `none / low / medium (mặc định) / high / xhigh / max` — không
  có `minimal`; runtime hiện **không gửi** reasoning ⇒ đang chạy `medium`.
- **B40 kết quả** (`doi_chieu_nghien_cuu_B.md`): BM25 runtime chỉ chấm lại 30 đoạn dense (`retrieval/full_corpus.py:479-491` ở `71d2450`; sau đợt 3 vòng lặp ở `:482`) — yêu cầu ChatGPT không nói ⇒
  gợi ý D1 / D3 chỉ đổi thứ tự trong pool dense; retrieval chỉ trả `fused[:10]` (`:594` sau đợt 3) ⇒ chọn đa dạng từ pool 30 phải đổi đầu ra retrieval; 56 / 158 câu có
  5 đoạn context cùng file, 9 câu dev thiếu file đúng khi một file chiếm ≥ 3 chỗ; đoạn bảng 144 / 8.459 (câu có đoạn đúng chạm bảng: dev 8, test 2); cỡ mẫu
  gợi ý > dữ liệu (câu so sánh + nhiều nguồn dev 28 / test 10; claim có nhãn người 0); gợi ý fallback provider 8B ngược pin Nebius (spec 7A2 §5.2).
  Lưu ý A: `LUONG` §3 + `BAO_CAO_TIM_KIEM` §2 **đã** ghi đúng điều BM25 — chỉ yêu cầu ChatGPT thiếu (S31 / W19).
- Bước: User chọn phạm vi ⇒ A **một** tài liệu thiết kế `docs/superpowers/specs/` (tiêu chí ghi trước `run-experiment`, cỡ mẫu, trần tiền, mốc — đề xuất
  context 10 sau B1, chờ User) ⇒ session khác review ⇒ User duyệt một lần.

### Phase 8.2 — TẠM DỪNG (User 16:5x 25/10)

- Spec `dabae90b2b60`. B0 file đọc cặp mù ready (User đọc khi tiện). **B1** (B, T1–T5 đạt, 0,0369 USD; report `phase_8_2_b1_implementation.md` sha
  `bb5fea83aeb6` trên nhánh) **chưa A review**; nhánh `p82-b1` phải **rebase** lên `main` mới (xung đột import ở `retrieval/full_corpus.py`, đổi import
  ở `test_full_corpus_retrieval.py`, comment `b1.py:23` — `sua_1b_plan.md` §6) rồi **chạy lại T1–T2** (không dùng lại bằng chứng cũ).
- Điều mới từ rà code: lỗi citation đếm theo định nghĩa mới ⇒ A/A context 10 = 0 vs 0 (trước 12 vs 8); E2 có thể NOT RUN; plan E1 đổi sang
  `paired_stats` (mục "Câu hỏi A còn nợ"). Tiền 8.2: 0,0369 / 0,5 USD.
- Chi tiết việc 8.2 phiên tối 25/10 (B22, B23, B24, C32, C33): `git show bc568f1:session_prompt/CURRENT_HANDOFF.md`.
