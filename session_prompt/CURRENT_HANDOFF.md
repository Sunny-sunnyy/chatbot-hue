# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 20:56 03/11/2026 (A, **kết phiên tối 03/11**: B3 `a3dabba` + B3b `9e2ecd9` (nhớ bật) + B142 `6817897` (👍 / 👎, gợi ý) + B143 `e3cdb96` (sửa an toàn khẩn cấp) vào `main`; plan B4 duyệt; vòng cải tiến 17 chờ User). Trước: 13:26 03/11/2026 (A, kết phiên 03/11: B1 merge `f01c032`, B2 merge `00d670e`; B3 code trên `p9-b3` `46008ed` chưa merge; vòng cải tiến 16). Trước: 20:47 02/11/2026 (A, kết phiên tối 02/11).
Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở. Tối 03/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-03_toi.md`; trưa 03/11 (B131–B136 / C133–C145) ở `session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-11-03.md`;
02/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-02.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-03_phase_9_b1_va_b2.md`.

## PHIÊN 04/11 — VIỆC ĐANG GIAO (A ghi 19:38 04/11/2026)

User chọn quyền "như 03/11" + "làm đi theo thứ tự" (A ghi nhận 19:38 04/11/2026). Thứ tự: B review plan tốc độ ⇒ C chạy tốc độ; song song B viết plan B4 bản 3 ⇒ C kiểm phần đổi ⇒ A duyệt sha ⇒ B đo; B review plan B5. Mọi việc: `notify_when_idle`; tiền phiên ≤ 1 USD.

- **B150 (B, 0 USD) — review vòng 3 plan tốc độ bản 4** `docs/superpowers/plans/2026-11-03-phase-9-toc-do-dinh-tuyen-plan.md` `395c79bbe168` (bản 3 đã duyệt `984d67829a34`): chỉ phần đổi (mốc mới sau B143, `ROUTER_INSTRUCTIONS` `164bd4a254e9`, trần 0,085 / dừng 0,08). Đọc: mục "Căn cứ để review" của plan + `git diff` bản 3 ↔ 4 (không đọc STATUS / tin của C). Ghi "Vòng 3" vào `…-toc-do-dinh-tuyen-plan_review.md`. Không chạy lượt có phí. Xong ⇒ nhắn A.
- **B151 (B, 0 USD) — plan B4 bản 3** `docs/superpowers/plans/2026-11-03-phase-9-b4-plan.md` (bản 2 `42fa62d2425f`): chỉ đổi D3 (m-2: code luôn thêm trường bắt buộc còn thiếu) + ghi thước an toàn cho 5 lượt ghép kín (như Q6 đã thấy: sàn 0 ý trái + 0 ý không nguồn về giá / giờ / điều kiện) + m-3 (`usage_tru_builder`); trước đó `git worktree prune` + tạo lại `/tmp/b_b4` (`p9-b4` `c76934c`, symlink `data/`, `knowledge-base-hue/`). Báo sha mới ⇒ C kiểm phần đổi. Không đo trước khi A duyệt sha bản 3.
- **B152 (B, 0 USD) — review plan B5 bản 2** `docs/superpowers/plans/2026-11-03-phase-9-b5-plan.md` `0df068b47df6` theo §9.1 (chỉ gói "Căn cứ để review"); ghi `2026-11-03-phase-9-b5-plan_review.md`. Làm sau B150 + B151.
- **C165 (C) — thí nghiệm tốc độ #1:** chờ A duyệt sha bản 4 (sau B150) ⇒ `git worktree prune` + tạo lại `/tmp/c_toc_do`, rebase `p9-toc-do-1` lên `main` `0adcaf3` ⇒ chạy theo plan (trần 0,085). Đo chữ đầu chỉ khi không session nào chạy server / Playwright / lượt có phí (W31) — B151 / B152 chỉ viết tài liệu nên không chặn; khi C đo, B không chạy lượt có phí.
- **C166 (C, 0 USD) — kiểm phần đổi plan B4 bản 3** khi B báo sha (chỉ D3 + thước an toàn + m-3); ghi vòng mới trong `2026-11-03-phase-9-b4-plan_review.md`.

## PHIÊN SAU ĐỌC TRƯỚC (đọc trước nhất)

**Hệ thống (`main` `e3cdb96` + docs):** chatbot = RAG 1–8 + **trợ lý Phase 9**: định tuyến 4 tuyến (trò chuyện / trợ lý Huế / ngoài phạm vi / khẩn cấp — câu soạn sẵn 113 / 114 / 115 / 112; từ B143 khẩn cấp phủ cả "vừa bị cướp / giật, cần báo công an") + dòng nhắc "có thể đã thay đổi"
+ trợ lý tự gọi `tim_kho` thêm ≤ 2 lần (B2b) + **nhớ hội thoại** (B3b: chỉ nhớ câu hỏi 3 lượt, cookie 30 phút; câu dặn "nhận định chỉ từ đoạn nói đúng đối tượng") + câu dặn hẹp không tự thêm lời khuyên an toàn thiếu nguồn (B3)
+ giao diện nhiều lượt Bản 1 — Huế hiện đại (số nguồn 1..k, "Cuộc trò chuyện mới") + **nút 👍 / 👎** (log `chat_feedback`, không nội dung) + 3 nút gợi ý dưới câu ngoài phạm vi (B142). `frontend/dist/` không commit ⇒ `cd frontend && npm ci && npm run build`.
Kho 204 file / 8.424 đoạn; Golden md5 `6331e88fb171`; T1 `4d5bbe9e0edc`. Qdrant chạy bằng Docker Desktop — `curl :6335` không trả lời ⇒ báo User. Chữ đầu câu về Huế 3,50 / 5,33 s (B2, 10 câu) — **vượt sàn 3 / 5 s**, thí nghiệm tốc độ chờ chạy.

**Phase 9** — spec bản 9 `169c2dd5f86a`. Bậc: B0 ✓ · B1 ✓ · B2 ✓ · **B3 ✓ (+ B3b, 03/11 tối)** · **B4 đang code** · B5 (plan nháp) · B5b thời tiết (User chọn) · B6 · B7. Tiền Phase ≈ **0,97 / 2,0 USD** (phiên tối 03/11 ≈ 0,31); mỗi phiên ≤ 1 USD.

**Phiên sau làm theo thứ tự:**
1. Mở A / B / C; `ListAgents`; **hỏi lại quyền phiên** (quyền tối 03/11 hết hạn) — đề xuất một câu: như 03/11 (A tự điều phối + tự quyết trong kế hoạch, A tự commit / push cả phiên, ≤ 1 USD). Kiểm Qdrant; worktree `/tmp/…` mất sau khởi động lại ⇒ B / C tạo lại.
2. **Hỏi User (mỗi lần một câu):** (a) duyệt vòng cải tiến 17 — **W52** (User có thể vắng ⇒ giao B / C trước rồi mới hỏi User), **W54** (câu an toàn / khẩn cấp mới viết ⇒ vào bộ hồi quy ngay), **I9** (dời bẫy kiểm log) — `SO_CAI_TIEN_CACH_LAM.md`; (b) câu soạn sẵn khẩn cấp mở bằng "đang gặp nguy hiểm" — chọn 1 trong 3 phương án chữ C162 (`data/phase_9/khan_cap_buoc0/chu_moi_phuong_an.md` `a0bc71cbfaff`; C nghiêng PA1 mở rộng dòng mở "…hoặc vừa gặp chuyện (bị cướp, tai nạn, cháy, ốm nặng)"; đổi chữ ⇒ sửa `test_emergency.py`) hay giữ; (c) xoá nhánh đã merge `p9-b3`, `p9-b3b`, `p9-phan-hoi`, `p9-khan-cap` (đã kiểm `git log main..<nhánh>` rỗng lúc kết phiên — User `!`); (d) plan B5 nháp: trần 0,10 + bảng cụm kề + 2 cột `toi` / `luu_y` (khi chốt plan B5).
3. **B4 (hỏi lại)** — plan bản 2 **duyệt `42fa62d2425f`**; trần 0,12; nhãn C158 sẵn (`data/phase_9/bo_do_b4/chon_da_thay.json` `060d62a56e97`, `can_hoi_lai.json` `ef9179c8f266`); B code trên `p9-b4` `c76934c` — **code xong, Q1 đạt, pilot + đã thấy 2 bản ghi chú (chưa khoá)** (`STATUS_B.md` "PHIÊN SAU — B4") ⇒ đo theo plan ⇒ C review ⇒ merge. Mốc định tuyến đã đổi (B143) — đo trên `main` mới.
4. **Thí nghiệm tốc độ #1** (suy luận thấp cho lần định tuyến — `effort none` model nhận, 0 token suy luận): plan bản 4 của C `395c79bbe168` (mốc mới sau B143, trần 0,085) ⇒ B review ⇒ A duyệt sha ⇒ C chạy; đo chữ đầu chỉ khi không session nào chạy server / Playwright / lượt có phí (W31). Code cờ: `p9-toc-do-1` `4c6adc6` (**đã push** — A, kết phiên; rebase lên `main` trước khi chạy). Phân tích: `data/phase_9/toc_do/c150_phan_tich.md`. Bước sau nếu #1 không đủ: #6 (chạy trước lần trả lời song song định tuyến); #4 gộp định tuyến ⇒ User quyết.
5. **Plan B5 bản 2** `0df068b47df6` (C161: khớp 4 trường plan B4 duyệt; D11 link "mở bản đồ" do code dựng, href chỉ nhận gốc maps/search; thời tiết = B5b) — **B review** ⇒ A duyệt sha; User đã chốt Quyết 1 (giờ chung chỉ điểm có tên trong file vé), Quyết 2 (điểm xa chỉ khi ≥ 3 ngày / được hỏi), thời lượng: xếp theo buổi + độ dày theo nhịp đi (B4); thời tiết = B5b sau B5. Thêm link "mở bản đồ" do code dựng (nghiên cứu sản phẩm thật). Reviewer: B.
6. **B6 (web):** User chọn web chỉ cho câu **về Huế** mà kho không có; câu ngoài phạm vi giữ từ chối + nút gợi ý. Bộ đo B6 phải có ca "ở Huế có quán phở Hà Nội nào ngon" (định tuyến đúng `tro_ly_hue`, kho từ chối sau 3 lần tìm ~8 s).
7. Theo dõi: router đưa S20 sang `khan_cap` (2 lần trước); định tuyến quá 10 s ⇒ `tro_ly_hue` (nếu rơi vào câu khẩn cấp ⇒ mất câu soạn sẵn; 1 / 246 lần ở B143, câu ngoài phạm vi) — ứng viên việc sau; `chat_feedback` chưa nối với `chat_metrics` (thêm `turn_id` nếu cần phân tích); câu từ chối sau 3 lần tìm chờ ~8 s.

**Mã hay gặp:** B0–B7 = bậc Phase 9 (spec §5); D… / Q… / m-… = quyết định / câu đo / finding minor trong plan & review; S20, S10, S04 = mã câu bộ an toàn 32 (private); kc08 = câu khẩn cấp tự viết bước 0 (`data/phase_9/khan_cap_buoc0/`); P0_sai / P0_thieu = sai điều kiện / thiếu cảnh báo;
N_AA = số câu tụt giữa hai lượt cùng cấu hình (nhiễu); Bxx / Cxx = mã việc A giao B / C; S / W / I = sự cố / đề xuất / dời luật trong `SO_CAI_TIEN_CACH_LAM.md`.

## Câu hỏi cho User (hỏi mỗi lần một câu)

1. Quyền phiên + mục 2 ở trên.
2. Khi rảnh: đọc 10 câu mẫu B4 `data/phase_9/bo_do_b4/mau_cho_user.md` và 10 câu mẫu B6 `data/phase_9/bo_do_b6/mau_cho_user.md` — câu nào không giống người thật hỏi ⇒ báo A.
3. Không gấp: 4 worktree AGY cũ (`~/.gemini/antigravity-cli/…`) giữ hay gỡ; xoá sao lưu kho đợt 1 + 2?
4. File báo cáo tiến độ cho giáo viên (`gửi chatgpt/2026-11-03/báo cáo tiến độ giáo viên/…`, cập nhật tới B2) — cập nhật thêm B3 / B3b / B142 / B143 nếu User muốn gửi lại.

## Câu hỏi A còn nợ (không cần User)

- Ứng viên tối ưu tiền `prompt_cache_key` (C124 02/11): C150 thấy lần gọi sau trong vòng công cụ đã đọc đệm (159 / 162) — chỉ định tuyến + lần trả lời đầu không đọc ⇒ lợi ≈ 0; xét lại khi lời dặn dài hơn.
- Bảng sổ cải tiến: S41–S44 thiếu 1 cột. W4 / W39 hạn 07/11 (0 buổi D ⇒ đề xuất gỡ).
- Log `FileHandler` không xoay vòng — xem lại khi deploy. Hạn mức OpenAI / Serper — đặt khi tới B6.
- B7 (gợi ý từ báo cáo github.txt): chuẩn bị phương án dự phòng demo khi mất mạng (video / câu trả lời lưu sẵn); đề cương nói "trợ lý RAG có công cụ", không nói quá "Agentic RAG", không nhắc rerank (hệ thống không dùng).

## Trạng thái lúc kết phiên tối 03/11 (21:53 03/11/2026)

- **Không việc nào đang chạy**; không server / tiến trình nền. `main` = `origin/main`. Nhánh còn việc: `p9-b4` (B), `p9-toc-do-1` (C) — cả hai đã push. Nhánh đã merge chờ User xoá: `p9-b3`, `p9-b3b`, `p9-phan-hoi`, `p9-khan-cap`.
- Worktree giữ: `/tmp/b_b4` (B, `p9-b4`), `/tmp/c_toc_do` (C, `p9-toc-do-1`) — **mất khi máy khởi động lại** ⇒ `git worktree prune` + tạo lại (commit nằm trong repo, không mất).

- **User (21:26 03/11/2026):** "tại sao dừng" — làm tiếp tới ~21:50 ⇒ **B145** pilot B4 (≤ 0,01 USD, không khoá / không kín), **C163** review sớm code B4 (0 USD).
- **C163 xong:** `b144_review.md` "Vòng sớm" `1ccb676f475d` — 0B / 0M / 3m. A quyết: m-1 sửa (stream phát "đã tìm" cho kết quả `hoi_lai`); m-3 báo usage − builder max khi đo; **m-2** (model chỉ hỏi trường không bắt buộc ⇒ câu lịch trình thiếu `so_ngay` đi tiếp) ⇒ code luôn thêm trường bắt buộc còn thiếu ⇒ **plan B4 bản 3** (chỉ D3) ⇒ C kiểm phần đổi ⇒ A duyệt sha — phiên sau, trước lượt đo quyết.
- **B145 xong** (21:40 03/11/2026; `p9-b4` `c76934c`, đã push): m-1 sửa (+ test); vòng chỉnh 1 `HOI_LAI_NOTE` `2b62c390f2fa` (chưa khoá). Pilot 4 câu sạch (0,0016 USD). Đã thấy 20: v0 Q2 9/10, Q3 0/7, hỏi thừa 0; v1 Q2 9/10, Q3 1/7 ⇒ **câu đủ bị hỏi lại chập chờn** (1 câu ở pilot, 1 ở v1) ⇒ phiên sau đo câu đủ v0 ↔ v1 × 2–3 lượt trước khi chọn ghi chú, rồi khoá. Tiền B4 ≈ 0,026 / 0,12 (mỗi lượt 20 câu ≈ 0,012 > ước plan 0,008). m-3: harness thêm `usage_tru_builder` phiên sau.
- **C164 xong (0 USD):** lệnh kín B4 chạy thử trên `86c311b` (script `data/phase_9/bo_do_b4/tools/kin_c164.py` `88e06fed8ef3` chỉ in số đếm; giá trị chọn kín `chon_sealed.json` `463e3b5938e7`, B không mở) — STATUS_C việc 6. **A quyết câu C hỏi:** 5 lượt ghép kín **chấm thước an toàn** như Q6 đã thấy (sàn 0 ý trái + 0 ý không nguồn về giá / giờ / điều kiện) — B ghi vào plan B4 bản 3 cùng đổi D3.

- **B144 (B) dừng ở mốc an toàn:** `p9-b4` rebase lên `main` (`c4f2b76` backend + test, `86c311b` giao diện; push, chưa review); cờ `hoi_lai: false`; D1–D10 code xong (`llm/hoi_lai.py`, `StopAtTools`, route clarify / truong, thẻ nút + "Trả lời luôn"); 8 test B4 mới + 66 test đạt; **Q1 PASS** (228 ca × 2 lần gọi giống byte `main`). **0 USD đã chạy.** Còn: pilot ⇒ Q2 / Q3 ⇒ khoá ⇒ Q4–Q7 ⇒ C kín ⇒ Q8 + Playwright — lệnh ở `STATUS_B.md` "PHIÊN SAU — B4". Report `b144_b4_implementation.md` `4a751ef3ad6f`. Worktree `/tmp/b_b4` (mất nếu máy khởi động lại).
- **C160 xong (nháp bộ đo B6):** `data/phase_9/bo_do_b6/` — đã thấy 27 câu `9be5c35dcb29` (9 web trả lời được · 6 không xác minh · 4 ngoài Huế phải từ chối, 0 web · 4 kho có, 0 web · 2 theo ngày · 2 tên trong câu; có ca "phở Hà Nội ở Huế") + kín 10 `b85d5d0351f4` (B không mở) + 3 chuỗi nêu tên (bộ B3); README nháp `83aa15035aa8`; mẫu cho User `mau_cho_user.md` `34253b305cb7`. Chốt khi viết plan B6.
- **Plan tốc độ bản 4** `395c79bbe168` (C; mốc mới trên `ROUTER_INSTRUCTIONS` `164bd4a254e9`, trần 0,085 / dừng 0,08) — **chưa duyệt**: B review phần đổi phiên sau ⇒ A duyệt sha. Code cờ `p9-toc-do-1` `4c6adc6` (worktree `/tmp/c_toc_do`, đã push; rebase lên `main`). C dừng — `STATUS_C.md` "PHIÊN SAU ĐỌC TRƯỚC".
- Chi tiết tối 03/11 (B137–B144, C146–C159, quyết định theo giờ): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-03_toi.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-03_toi_phase_9_b3.md`.

## Session

**Phiên 04/11 (mở 19:34):** A `hue-rag-b7` · B `hue-rag-2d` · C `hue-rag-81` — cả ba Claude Code, trực tiếp.

**Phiên tối 03/11 (mở 17:56):** A `hue-rag-9e` · B `hue-rag-32` · C `hue-rag-40` — cả ba Claude Code, trực tiếp.

**Phiên 03/11 (mở 08:36, kết 13:26 03/11/2026):** A `hue-rag-5e` · B `hue-rag-52` · C `hue-rag-d8` — cả ba Claude Code, trực tiếp. B: B131 hoàn tất B1, B132 plan B2, B134 code B2, B135 plan B3, B136 code B3 (≈ 0,513 USD). C: C133 bộ đo B2, C134 review B1, C135 review plan B2, C136 bộ đo B3, C137 / C141 review B2, C138 câu hai ý, C139 thời tiết, C140 mẫu giao diện, C142 review plan B3, C143 bộ đo B4 + chi phí, C144 bảng điểm B5, C145 review sớm B3 (≈ 0,0006 USD). A: điều phối, merge B1 + B2, 5 chỗ báo cáo × 2, README repo, báo cáo cho giáo viên, vòng cải tiến 16.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C lúc mở phiên sau: không việc đang chạy ⇒ kiểm nhanh ⇒ báo A ⇒ chờ.

## Quyền

- **Phiên 04/11** (User chọn "như 03/11", A ghi nhận 19:38 04/11/2026): A tự điều phối + tự quyết trong kế hoạch; A tự commit / push cả phiên; ≤ 1 USD / phiên; B / C push nhánh riêng. Hết hạn cuối phiên.
- **User 18:05 (A ghi nhận 18:05 03/11/2026):** "tiếp tục điều phối, phát triển, tự nghiên cứu, so sánh, tối ưu, đánh giá, viết báo cáo"; **kết phiên ~22:10** ⇒ A bắt đầu kết phiên ~21:40.
- **Phiên tối 03/11 — HẾT HẠN lúc kết phiên** (User chọn "như trưa 03/11", A ghi nhận 18:01 03/11/2026): A tự điều phối + tự quyết trong kế hoạch; A tự commit / push cả phiên; ≤ 1 USD / phiên; B / C push nhánh riêng. Hết hạn cuối phiên.
- **Phiên 03/11 — HẾT HẠN (kết phiên 13:26 03/11/2026)** (User: "quyền của A như 02/11" 08:46; "đồng ý cả phiên" A tự commit / push ~09:10): A tự điều phối + tự quyết trong kế hoạch; ≤ 1 USD / phiên; B / C push nhánh riêng. Tiền phiên 03/11 ≈ **0,514 USD** (B ≈ 0,513 · C ≈ 0,0006 · A 0). User: C làm trực tiếp với A, việc A giao = "làm đi".
- **Phase 9 (spec duyệt, không hết hạn theo phiên):** trần **2,0 USD** cả Phase; Serper dùng luôn (User chấp nhận rủi ro điều khoản — spec §2, §7); gói npm giao diện như đã duyệt 02/11.
- **Thường trực:** A commit / push — **hỏi User trước** (luật chung của User), rồi A tự chạy; chỉ khi bị chặn / lỗi mới đưa `!` (I8, `WORKFLOW.md` §9.6); B / C không commit trừ khi việc ghi rõ; duyệt cho A =
  duyệt cho B / C; thư viện nhỏ cần cho việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage + tiền; code luôn `uv run`.
- **Tra web:** `scripts/tra_web_codex.sh` (chỉ thông tin công khai); **không bao giờ gọi `agy`**. Khoá `SERPER_API_KEY` trong `.env` (không đọc / in).
- Giá `gpt-6-luna` (User 30/10): vào 0,10 · ra 0,50 · đọc đệm 0,01 · ghi đệm 30 phút 0,125 USD / 1M. Serper (B122, trang giá): 0,001 USD / lượt (gói 50 USD / 50.000; 2.500 lượt thử).

## File private quan trọng (không commit)

| File | Nội dung | sha256 (12) / md5 |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_v5.jsonl` | nhãn đoạn đúng mặc định (kho đợt 2) | `33d16fd6b8f4` |
| `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` | Golden 176 | md5 `6331e88fb171` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` | 36 câu kín — đã dùng (B3); không chép nội dung | md5 `ddc59587b502` |
| `knowledge-base-hue/evaluation/final_2026-11-01/final_sealed.jsonl` | bộ kín 40 câu — **đã dùng** 01/11 | `7f97d4c10b2b` |
| `data/loi_nang_2026-10-28/` | thước lỗi nặng; `an_toan/questions.jsonl` 32 câu | `9fa81b0fcec4` |
| `data/do_cuoi_2026-11-01/` | lượt đo cuối Phase 1–8 (mốc của Phase 9): runbook, tools, golden/, an_toan/, ngay/, kin/ | — |
| `data/nghien_cuu_phase_9_2026-11-01/` | nghiên cứu Phase 9: mạch 1–4, TRIPO; **`agent/`**: `a_sa1–3.md` (khoá FDE), `b122_tra_web.md`, `b123_sdk_probe.md` (+ `b123/`), `c121_sdk_024.md` | — |
| `gửi chatgpt/2026-11-02/` | yêu cầu agent có công cụ (`015467cce3f1`) + kết quả `NGHIEN_CUU_PHASE9_AGENT_CONG_CU_HUE_RAG_2026-11-02.md` | — |
| `data/giao_dien_moi_2026-11-01/` | ghi chú tham khảo, `do_csp/`, `b121/` (script Playwright, ảnh, log) | — |
| `data/tra_cuu_cli/<ngày>_<tên>/` | đầu ra `scripts/tra_web_codex.sh` (02/11: `b122-a-agents-sdk`, `b122-b-serper`, `b122-c-do-agent`) | — |

## Việc đang mở — luật chung khi sửa code / dữ liệu

- A commit + push `main` **trước** khi B / C sửa code; khai báo file trong `STATUS_<X>.md` trước khi sửa; skill `practical-project-coding`; test liệt kê file; report
  `<việc>_implementation.md`; review chéo (W32: ca dò khác cách + câu bất biến); plan có tiêu chí ghi trước ⇒ session khác review **trước** khi A duyệt sha (sha tính từ file).
- **Báo kết quả bộ an toàn 32 câu luôn đủ 4 số** (đảo cảnh báo · sai điều kiện mới / hết · thiếu cảnh báo mới / hết · ngoài kho bị trả lời) — `run-experiment` §4, W51.
- **Cổng ổn định:** (1) test file chạm; (2) chạm giao diện ⇒ `cd frontend && npm ci && npm run build`; `cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port <cổng trống>`:
  `/` 200, `/health` 5 / 5, 1 câu trong kho + 1 câu ngoài kho (câu tự viết); đếm `chat_metrics` mới = số câu; grep câu hỏi trong log = 0; tắt server (TaskStop — **không `pkill -f`**, bẫy §8);
  (3) chạm tìm / chia đoạn: T1 giống byte; (4) đủ 5 chỗ (`WORKFLOW.md` §6); (5) hook tự chạy.
- **Có lượt đo latency ⇒ session khác không chạy lượt trả phí / việc nặng CPU / Qdrant** (W31). Việc chạy nền: `run_in_background`, không vòng chờ `pgrep -f`.
- Test cần key: `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan`, `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`,
  `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`. `test_static_ui.py` cần bản build.
- Đọc kho: **chỉ** `scripts/grep_kb.sh`; report tracked tả câu ở mức loại câu. Giờ trong file: chạy `date` trước; tin nhắn không cần giờ (W45). `rm` với biến: `"${X:?}"/…` hoặc đường dẫn cố định.

## Hồ sơ đã đóng (chỉ tra cứu)

- Phiên 03/11 nguyên văn (B131–B136, C133–C145, quyết định theo giờ, B1 / B2 merge): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-03.md`.
- Phiên 02/11 nguyên văn (B121 giao diện, B122 / B123, C118–C121, các quyết định agent theo giờ): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-02.md`.
- Giao diện mới: `report_agent/2026-11-02_giao_dien_moi_code/` (`b121_giao_dien_implementation.md`, `b121_review.md`); hướng chọn B116 `report_agent/2026-11-01_giao_dien_moi/`.
- Nghiên cứu Phase 9: `report_agent/2026-11-01_nghien_cuu_phase_9/` + `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md`.
- Streaming + lượt đo cuối Phase 1–8 (01/11): `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`. Phase 8.2: `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
