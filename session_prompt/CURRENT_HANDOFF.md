# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 10:28 01/11/2026 (A, **mở phiên 01/11** — quyền phiên, Q1 chốt, spec bản 5, giao C việc 1b, B Vòng 3). Trước: 16:46 31/10/2026 (A, phiên chiều 31/10 — chỉ AI FDE; mục "PHIÊN SAU" viết lại lúc kết phiên chiều). Trước: 12:36 31/10/2026 (A, **kết phiên 31/10** — User: "các nhiệm vụ, câu hỏi để session tiếp theo"). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở.
Lịch sử phiên 31/10 (mục việc B99–B106, C97–C100, quyết định theo giờ, mọi trạng thái review) dời **nguyên văn** sang `session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-10-31.md`
(I7); phiên 28–30/10: `archive/CURRENT_HANDOFF_LICH_SU_2026-10-28_30.md`. Tổng hợp đợt: `report_agent/2026-10-31_streaming_spec/TONG_HOP.md` (mở),
`report_agent/2026-10-31_tra_web_codex/TONG_HOP.md` (đóng); nhật ký User `bao_cao_he_thong/nhat_ky/2026-10-31_spec_streaming_tra_web_codex.md`.

## PHIÊN SAU ĐỌC TRƯỚC (đọc trước nhất)

**Phiên 01/11 (mở 10:16, A ghi 10:28 01/11/2026):** quyền phiên = như 31/10 (mục "Quyền"); **Q1 chốt** (sàn giữ 3 / 5 s + mục tiêu báo cáo 1,5 / 3 s) ⇒ spec bản 5 ⇒ B Vòng 3 ready ⇒
**User duyệt spec `00fb57ee01b2` (10:42 01/11/2026)** ⇒ B code S1, C review. **B0 hôm nay** (User chọn — A hướng dẫn). **C làm việc 1b** (mục "C — việc 1b" dưới). User (terminal B, 10:19): việc A giao B = "làm đi".

**Hệ thống (`main`; chatbot KHÔNG đổi trong phiên 31/10 — chỉ tài liệu + governance):**
- Chatbot: context 10 + query NFC, reasoning mặc định, không rerank, validator v2; `/api/chat` ghi `chat_metrics` mỗi câu; giao diện trang đơn giản `frontend/` (JS thuần, một lượt,
  **chưa stream**). Kho 204 file / 8.424 đoạn; collection `hue_full_corpus_7a2_e5_small_384` 8.424 point (A kiểm 10:23 31/10); record `51fb1ec63cbc`; sparse `c8134c49a648`; T1 `4d5bbe9e0edc`.
- Thước: gold v5 (`33d16fd6b8f4`); Golden md5 `6331e88fb171`; bộ an toàn 32 câu; bộ ngày tương đối 15 câu. Số 30/10: p50 2,19 / p95 4,90 s cả câu (harness); từ chối nhầm 12 / 158;
  lỗi citation 0 / 489; ≈ 0,00025 USD / câu (`cost_usd` ghi thiếu ~20 % — việc đóng gói).
- Qdrant chạy bằng **Docker Desktop** (Windows): lúc mở phiên 31/10 tắt ⇒ User bật rồi `docker compose up -d qdrant`. Mở phiên mà `curl :6335` không trả lời ⇒ báo User, không tự bật.
- **Mới chiều 31/10 (`f34cb7f`, `32d4b68`, `0d69376` + commit kết phiên):** áp khung_fde (khung cá nhân của User) — W37 hook giờ ước `.claude/hooks/` (báo lúc ghi), W38 mỗi vòng xét mọi mục đang thử (vòng 12: 40 ⇒ 7), W39 skill `teach-and-quiz` cho D, W40 (`propose-options` §4b khám phá 5 dòng, §4c; `practical-project-coding` `git grep` + "Giải thích ngắn"), W41 skill `agent-design-review` + `agent-security-review` (Phase 9; security một lần lúc đóng gói).
- **Mới 31/10 (`1a9dca4`):** tra web bằng `scripts/tra_web_codex.sh` (§9 `Session_Prompt.md`); **cấm gọi `agy` từ agent** (AGENTS.md luật 7, `.claude/settings.json` chặn).

**Thứ tự việc phiên sau (User 30/10 PA2, giữ nguyên 31/10):**
1. Mở A / B / C; `ListAgents`; **hỏi lại quyền phiên** (quyền 31/10 hết hạn); kiểm Qdrant.
1b. **Gom báo cáo so sánh phần đã đóng** (Phase 0 → 8.2, sửa kho, Qwen3-8B — khung đã chốt ở mục 4; User 17:39 31/10: dời phiên này, chạy song song streaming được).
   A đề xuất: 5 agent con theo nhóm khâu đọc `bao_cao_he_thong/BAO_CAO_*`, `report_agent/*/TONG_HOP.md` + report gốc, `reports/` (Phase 0–7), `docs/superpowers/specs/`,
   `guides/` ⇒ nháp `data/so_sanh_phuong_an/` ⇒ A ghép bản public ⇒ 1–2 agent con ngữ cảnh mới kiểm ⇒ commit (~1–2 giờ, 0 USD). Hỏi User: mở B / C cho việc này không.
2. **Spec streaming — còn 1 câu User + duyệt sha** (chi tiết mục "Streaming" dưới): A hỏi **câu Q1** (mục tiêu chữ đầu tiên) ⇒ A điền `TBD` ở spec §2 + §6 C1 ⇒ B kiểm phần
   đổi (không chạy Codex lần 2) ⇒ A trình User duyệt **bản sha tính từ file** ⇒ A commit spec + review ⇒ giao code S1 (gom lõi chung) trước.
3. ~~Hội thoại nhiều lượt~~ — **DỜI SANG PHASE 9** (User 11:20 01/11/2026: "nghiên cứu về vấn đề lịch sử cuộc trò chuyện, tiếp tục trò chuyện với người dùng ở vấn đề trợ lý / agent, không cần làm ở các phase này"). Tư liệu: nháp spec C102 `docs/superpowers/specs/2026-11-01-multi-turn-design.md` (`45d159e09636`, Q1 User nghiêng PA1 trình duyệt giữ lịch sử — chỉ là ý, Phase 9 nghiên cứu lại) + C91.
4. **Đóng gói Phase 1–8** (A hỏi lại nghĩa "đóng gói" khi tới): bảng giới hạn `data/dong_goi_2026-10-30/gioi_han_da_biet_nhap.md` (`8211d5d6eb7f`) ⇒ `LUONG` §5; báo cáo
   "đã thử / chọn / bỏ"; sửa `cost_usd` + log `cache_write_tokens`; lệnh kiểm sạch; bộ kín mới trước bảo vệ; tắt ghi đệm nếu API cho (tra Codex trước).
   **Báo cáo tổng so sánh + nhìn lại Phase 1–8 (User chốt 17:13–17:39 31/10, brainstorm 5 câu):** một file `bao_cao_he_thong/BAO_CAO_SO_SANH_PHUONG_AN.md` (public,
   mức loại câu); hai phần — theo khâu (chính, đủ số đo) + theo Phase (khung khoá, chỉ trỏ về) + chỉ mục chéo; người đọc = User + Claude + ChatGPT (không phải hội đồng) ⇒
   tự đọc được; mỗi so sánh: vấn đề · ngày / Phase · mọi phương án + mốc · cách đo · tiêu chí ghi trước · kết quả số (CI, thắng / hoà / thua) · tiền + tốc độ · quyết định
   + lý do · giới hạn · bằng chứng (report, commit, sha); **nhãn độ tin** ([rà lại 8.1] / [kho, cấu hình cũ] / [chưa kiểm lại Phase 0–7] / [một lần chạy] / [xác nhận nhóm
   kiểm]); gom phần đã đóng trước (việc 1b), phần mới ghi khi làm. Trước báo cáo: **đo cuối + thử có giới hạn** (lượt đo cuối cùng một commit: Golden 176 + an toàn 32 +
   15 câu theo ngày + tốc độ trình duyệt + **bộ kín mới** + B0; thử thêm chỉ cho từ chối nhầm 12 / 158, câu so sánh / nhiều nguồn, bảng giá — nghiên cứu ngoài trước).
   Thêm 31/10 chiều: **nhìn lại Phase 1–8 theo khung khoá AI FDE** (chương "đánh giá" đồ án — User 31/10 đồng ý làm ở bước này, sau streaming + nhiều lượt
   vì số đổi): mỗi Phase một hàng — vấn đề đo được · mốc · tiêu chí ghi trước · kết quả so tiêu chí · lỗi nặng · phương án đã bỏ · tiền / tốc độ · chỗ hở (khung:
   ghi chú private trong `data/external_project_notes/`, Phần VIII; số lấy từ các `TONG_HOP.md`); bảng giới hạn gom từ mục giới hạn của từng spec; review cả nhánh / cả backend bằng sub-agent ngữ cảnh mới; bộ kín mới so SHA256 với mọi file thử cũ;
   rà `agent-security-review` (khung_fde, mục 1, 2, 5, 7, 8) ⇒ "giả định an toàn"; hạn mức tín dụng phía nhà cung cấp cho key đang dùng (chưa kiểm OpenAI có không).
5. **Sau Phase 8:** bàn **giao diện mới** (React / Next…) **gộp áp nội dung AI FDE** — User 31/10: chờ bản AI FDE — nay đã có khung_fde v1.2 (31/10 chiều; khung cá nhân của User). A sơ bộ nghiêng React + Vite build
   tĩnh, FastAPI phục vụ (một server) — chưa nghiên cứu, chưa chốt. Rồi **Phase 9 — mở bằng nghiên cứu rộng** (User 31/10): chủ đề / đề tài, dự án, paper, ứng dụng đang dùng thật (du lịch / văn hoá / di sản), công việc thật của
   du khách / người dân — **trước** khi chọn hướng; không khoá vào gợi ý lịch trình. Cách: Codex `scripts/tra_web_codex.sh` + ChatGPT web (§9), mỗi hướng ứng viên
   viết 5 dòng khám phá (`propose-options` §4b) + `agent-design-review`. Ý cũ: `data/course_notes/v3/TONG_HOP_A_2026-10-30.md` §3.
6. Khi rảnh (User): **B0** (mốc người) — `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b0_prep_implementation.md` (B đã thấy khóa — không tóm nhãn); 20 câu mẫu lỗi nặng.

**Mục tiêu sản phẩm:** đồ án tốt nghiệp (bảo vệ ~1/2027), càng giống sản phẩm thật càng tốt; người dùng = User, du khách, người dân; AWS 10–50 USD / tháng chỉ khi local ổn.

**Mã hay gặp:** T1 = kết quả tìm 158 câu; PA0–PA3 = kiểu hiện chữ streaming (nháp v3 §1); D1–D5 = câu quyết định streaming; C1–C7 = tiêu chí nghiệm thu spec streaming §6;
S1–S4 = bước làm spec §5; cách (b) = lỗi trước luồng trả JSON như cũ, luồng mở bằng `StreamingResponse` tự dựng; TTFT / "chữ đầu tiên" = thời gian tới chữ trả lời đầu tiên;
Bxx / Cxx = việc A giao (31/10: B99–B106, C97–C100); M-n / m-n = finding major / minor; S / W / I = sổ cải tiến. **D0** = streaming trước hay sau hội thoại nhiều lượt (đã chốt:
streaming trước). **"PA2" của thứ tự việc 30/10** = giữ thứ tự cũ — khác PA0–PA3 của streaming. **Y1 / Y2 / Y3** = 3 bài thử tra web 31/10 (streaming / thước đo sản phẩm / Claude gọi CLI).
**B0** = lượt User đọc cặp câu trả lời mù làm mốc người. **158 câu** (T1, từ chối nhầm) = phần Golden 176 có đáp án trong kho. `answer_case` = hàm bộ đánh giá gọi lõi trả lời (không qua API).

## Streaming — trạng thái chi tiết (việc số 2)

- **User đã chốt 31/10** (giờ A ghi nhận): **D1 = PA1** (11:26) — chữ hiện ngay khi model viết + tiến độ thật, kiểm citation cuối như hôm nay; **D2 = (a)** (11:44) — sàn p50 ≤ 3 s /
  p95 ≤ 5 s cho "tới chữ trả lời đầu tiên hiện trên **trình duyệt**" (Playwright), "tới đủ câu" chỉ theo dõi; **D3 = phương án 1** (11:48) — bộ kiểm cuối hỏng ⇒ rút lại, lỗi / đứt giữa
  chừng ⇒ xóa hết, cả hai thay bằng lời báo + "Thử lại". Phạm vi: API + sửa tối thiểu `frontend/` (giao diện mới sau Phase 8 — User 10:23).
- **A tự quyết (kỹ thuật trong phạm vi):** D5 = xem lại khi > 1 % câu bị xóa / tuần (hoặc ≥ 3 lần / ≥ 100 câu); không nút "Dừng" bản này; lỗi trước luồng = cách (b); ép
  `response.incomplete` bằng `answer_max_output_tokens` nhỏ **không** phải lỗi giả (trần ≤ 0,001 USD); không chỗ nối chỉ dùng khi test (D3 (a) giao diện + luồng đứt = giới hạn); không
  test dựng 503 "chưa sẵn sàng" (giới hạn); câu từ chối dùng cùng sàn 3 / 5 s, đo tới lúc biết chắc là từ chối, báo riêng (C2); xem lại PA3 nếu lợi đo trên trình duyệt < 0,5 s.
- **Spec:** `docs/superpowers/specs/2026-10-31-streaming-design.md` bản 4 **`cf1ae9ef6c2c`** (202+ dòng; quét trùng 0; đã commit `f34cb7f`); **bản 5 `0b2679cfccd6`** ⇒ sửa m-1 / n-1 / n-2 (B Vòng 3 + R3.4 ready) ⇒ **User DUYỆT bản sha `00fb57ee01b2` (A ghi nhận 10:42 01/11/2026, sha tính từ file)**; commit cùng `b105_review.md`. Review: B105 vòng 1 changes_requested
  (M-1 hủy khi ngắt: ghi log trước mọi `await` + `CancelScope(shield=True)` + `move_on_after`) ⇒ vòng 2 ready (`report_agent/2026-10-31_streaming_spec/b105_review.md` `96bcc907886b`);
  **Codex review một lần (W33) xong** trên bản 3 `cd44744ea3d7` — 2 finding đúng, mới, hạ minor (bắt riêng `CancelledError`; 422 trước handler không có dòng log) ⇒ C sửa ⇒ bản 4,
  B kiểm phần đổi ready (`b106_codex_review.md` `cab2ca485750` mục 5). Kết quả thô Codex (private): `data/tinh_nang_moi_2026-10-27/2026-10-31-streaming-design_review_codex/`.
- **Q1 đã chốt (User, A ghi nhận 10:28 01/11/2026):** PA1 — sàn giữ p50 ≤ 3 / p95 ≤ 5 s tới chữ đầu trên trình duyệt + **mục tiêu báo cáo** p50 ≤ 1,5 / p95 ≤ 3 s (không chặn); đã điền spec bản 5 (§2 + §6 C1). Căn cứ cũ: Căn cứ: Codex tra `data/tra_cuu_cli/2026-10-31_ttft-chuan-nganh/ket_qua.md` — **không có chuẩn ngành**;
  Nielsen 1 s; API công khai p50 vài trăm ms – ~1,1 s; Codex **suy ra** mục tiêu p50 ≤ 1,5 s / p95 ≤ 3 s. A WebFetch kiểm 2 ý (arXiv 2604.06183: 2 / 9 / 20 s, 2 s bị chấm "kém chu đáo" ✓;
  llmlatency.dev đo token đầu API từ Đức ✓). Lưu ý: `gpt-6-luna` suy luận mặc định (trung vị 81 token suy luận, C73) ⇒ chữ trả lời đầu ra muộn hơn token đầu; chưa đo trên trình duyệt.
- Căn cứ nền: nháp v3 bản 3 `data/tinh_nang_moi_2026-10-27/c98_phuong_an_streaming_v3.md` (`3b6a9ba09149`); C97 bản 3 `c97_doi_chieu_code_streaming.md` (`702cc7ed8af4`); B99
  `b99_kiem_nguon_streaming.md` (`44644b22d9ef`); kết quả ChatGPT `gửi chatgpt/2026-10-28/kết quả nghiên cứu/NGHIEN_CUU_SAU_STREAMING_CITATION_HUE_RAG_2026-10-31.md` (`6bbfd2166721`);
  gói Codex review B104 `data/tinh_nang_moi_2026-10-27/b104_codex_review_spec.md` (`a8ba02fc2a59`).
- **Khi code (sau duyệt):** S1 gom lõi chung trước, T1 giống byte; giữ đúng các khác biệt `answer_case` ↔ route (spec §4.8 — không chuẩn hóa `[Nguồn n]`, giữ chữ khi citation hỏng, …);
  trần tiền cả việc 0,02 USD (spec §8); cổng ổn định dưới; FastAPI cận dưới `>=0.135` trong `pyproject.toml` (A tự duyệt — dependency nhỏ).
  **Thêm 31/10 chiều** (đối chiếu khoá ver4, `data/external_project_notes/HUE_RAG_DOI_CHIEU_KHUNG_FDE_2026-10-31.md` mục a): (a1) trước khi merge nhánh S1–S4: review **cả nhánh**
  bằng một sub-agent ngữ cảnh mới, chỉ nhận diff + `practical-project-coding` (mục "Ranh giới theo khâu pipeline") + tiêu chí (khoá W1D5·43; bản 30/10 bỏ sót đề xuất này);
  S1 đổi hàm dùng chung ⇒ `git grep` mọi nơi gọi trước khi sửa; (a6) đóng spec ⇒ ghi luôn mục "giới hạn đã biết" của streaming (không dồn tới đóng gói).

## Câu hỏi cho User (báo cáo mở phiên sau — hỏi mỗi lần một câu)

1. **Quyền phiên.** A khuyên: như 31/10 (A tự điều phối + tự thử trong luật; ≤ 1 USD; B / C push nhánh riêng theo việc).
2. **Q1 — mục tiêu "chữ đầu tiên"** (điền `TBD` spec): **PA1 (A khuyên)** sàn giữ 3 s / 5 s (D2 đã chốt) + **mục tiêu báo cáo** 1,5 s / 3 s; đo xong đạt dễ ⇒ A đề xuất nâng sàn.
   PA2: đổi sàn ngay 1,5 s / 3 s — có thể trượt vì phần suy luận của model ⇒ phải giảm suy luận (rủi ro chất lượng). (Đã trình 31/10 nhiều lần, User chưa chọn — để phiên sau.)
3. **Duyệt spec streaming** (sau Q1): A đưa sha bản cuối tính từ file.
4. **Sổ cải tiến — đề xuất chờ duyệt** (`SO_CAI_TIEN_CACH_LAM.md`): **W42** (hook git cảnh báo dòng có "dự án khác" — S60) và **W43** (script + bước kết phiên
   kiểm báo cáo khâu khớp hiện trạng — S61, User 31/10 nhắc) từ chiều 31/10; vòng 11: **W35** (kiểm điều khoản dùng tự động trước khi agent gọi công cụ / tài khoản bên ngoài mới), **I8**
   (dời luật "A tự chạy lệnh, chỉ đưa `!` khi bị chặn" vào `WORKFLOW.md` §9.6), **W36** (khẳng định về hành vi thư viện / định dạng log / rào script ⇒ chạy probe nhỏ thật trước khi bàn giao); và **W33** đã chạy ⇒ A đề xuất giữ làm tuỳ chọn (Codex review song song review Claude cho spec / plan lớn).
4b. ~~Golden lệch kho 1 câu~~ — **User 11:04 01/11/2026: giữ nguyên** (B107 `data/golden_sua_2026-11-01/b107_de_xuat.md`: chỉ `check` báo lỗi hoa / thường, chấm không sai).
5. (Khi bàn spec nhiều lượt) lưu câu hỏi người dùng? (PA1 C91 không lưu.) (Khi rảnh) B0; 20 câu mẫu lỗi nặng; xoá sao lưu đợt 1 + 2 khi đóng gói.
6. (Không gấp) File untracked `báo cáo nghiên cứu github.txt` (gốc repo, 82 KB, 01/10 — khảo sát đồ án gợi ý địa điểm / lịch trình): giữ ngoài git, hay dời vào `data/`?
   4 worktree AGY cũ (`~/.gemini/antigravity-cli/…`, nhánh `subagent-Monuments-Reviewer-*`, commit `c725987` 05/09): giữ hay gỡ (User `!`)?

## Câu hỏi A còn nợ (không cần User)

- Khung AI FDE (khung cá nhân của User, ngoài repo): A đọc `CHANGELOG.md` 10:29 01/11/2026 — khung lên v2.2; v2 / v2.1 chủ yếu là phần **lấy từ hue_rag** (skill review, các mục run-experiment / propose-options / improve-workflow), v2.2 chỉ ẩn tên ⇒ **không có gì mới cần đối chiếu**; 4.10 / 7.1 (v1.2) đã có ở hue_rag (lỗi kỹ thuật ⇒ lượt incomplete, spec 7A; ghi giới hạn khi đóng spec — a6).
  W39 hạn 07/11 (0 buổi D ⇒ đề xuất gỡ W4 + W39); theo dõi W37 báo đúng / nhầm; I3 memory.

- Sổ: theo dõi W32 (31/10 có tác dụng: B103 M-1, B105 M-1 đều từ ca dò khác cách), I7, W30 (hook bắt 2 giờ ước 31/10), W31; W33 đã chạy — kết luận ở sổ.
- Ý chờ từ B106 §3: cho Codex review đọc mã nguồn thư viện / `.venv` chỉ đọc (đổi phạm vi — cần User nếu muốn).
- Lần chấm tra web sau (C99 nêu): đếm riêng "403 trang thật" + kiểm tiêu đề trang mỗi URL (6 khẳng định không bắt link trỏ sai bài). Ca 503 / 502 route stream: A đã quyết = giới hạn.
- Thử mở phiên vai B (sub-agent, 31/10 kết phiên): tài liệu đủ; đã sửa 7 chỗ (tên mục, mã chưa giải nghĩa, việc soạn sẵn cho B, dòng cũ Project_Status §2, sàn cả câu ↔ D2,
  luật hỏi commit, WebSearch thử ⇒ lỗi 400). Lưu ý: phiên Claude mở **trước** `1a9dca4` nạp `AGENTS.md` cũ (thiếu luật 7) — phiên mới thì đủ.
- Log `FileHandler` không xoay vòng — xem lại khi deploy. C65: G2.1a chưa đếm lại bằng validator hiện tại.

## Session

| Vai | Terminal (01/11) | Agent | Liên lạc | Phiên 31/10 | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-27` | Claude Opus 5.5 | trực tiếp | điều phối; thử 6 lượt Codex / AGY; script tra web + chặn `agy` + §9; 3 câu User streaming; tra Codex TTFT | `STATUS_A.md`; 0 USD |
| B — thực thi | `hue-rag-da` | Claude Opus 5.5 | trực tiếp | B99 kiểm nguồn, B100 review C97, B101 mốc Y2, B102 review v3, B103 review governance, B104 gói Codex, B105 review spec, B106 chạy Codex review | `STATUS_B.md`; 0 USD |
| C — thực thi | `hue-rag-6a` | Claude Opus 5.5 | trực tiếp | C97 đối chiếu code, C98 nháp v3, C99 chấm 6 bản tra web, C100 spec streaming (4 bản) | `STATUS_C.md`; 0 USD |

Tên terminal đổi mỗi lần mở: `ListAgents`. Cả ba Claude Code ⇒ `trực tiếp`. **B / C lúc mở phiên sau:** không có việc đang chạy; mở phiên ⇒ kiểm nhanh ⇒ báo A ⇒ chờ.

**Việc soạn sẵn (A giao bằng tin nhắn khi tới bước):**
- **Trạng thái 11:22 01/11/2026:** S2 xong (B, `830df0e`, report `s2_stream_route_implementation.md`) ⇒ **review bằng agent con ngữ cảnh mới** (A giao; có thể chạy server cổng 8791 trong `/tmp/b_s1`, ≤ 0,002 USD) ⇒
  A tự kiểm 2–3 khẳng định. **B108** (B): sửa `cost_usd` giá đủ + token đệm, nhánh `dg-cost-usd` từ `830df0e`, worktree mới. **C:** sửa báo cáo so sánh theo review R1 / R2 (`data/so_sanh_phuong_an/review_r*.md`)
  ⇒ cập nhật plan C103 bỏ nhiều lượt ⇒ B review plan. B0: User đang đọc.
- **S1 review XONG (A, 11:01 01/11/2026):** `report_agent/2026-10-31_streaming_spec/s1_loi_chung_review.md` — **ready**, 0 blocker / 0 major, 2 minor không chặn (m-1 một `try` ⇒ S2 `git grep raise` lại; m-2 nghĩa `citation_ms` ⇒ ghi BAO_CAO khi merge). Ca dò A 200.000 chuỗi: kiểm citation chữ gốc = sau chuẩn hóa. S1 đóng bước; **không merge `main`** tới hết S4 (a1).
- **B — S2 streaming (GIAO 11:01 01/11/2026, sau khi xong B107):**
  - **Trạng thái (11:19 01/11/2026, B): chờ review** — nhánh `s1-loi-chung` `830df0e` (push); 82 test; T1 `4d5bbe9e0edc`; C4 cả hai route; C5 5 / 5; ngắt 2 thời điểm; pilot `incomplete` cả hai ca; ≈ 0,0041 USD (cận trên). Report `s2_stream_route_implementation.md`. A xét: trường log thêm `delta_matches_final`. generator stream + bộ bóc chữ JSON từng phần + chuẩn hóa `[Nguồn n]` từng phần + route `POST /api/chat/stream` (SSE) + log `chat_metrics`,
  **trên cùng nhánh `s1-loi-chung`** (nối sau `9c83003`; đổi tên nhánh nếu muốn, ghi report). Đọc (full): spec §4.1–§4.6, §4.8, §5 hàng S2, §6 C4 / C5 / C7, §7 (logic thuần + đường thật phần server), §8, §10;
  review S1 (m-1). Kiểm: test logic §7 (không stub model); cổng ổn định **cả hai route**; pilot `incomplete` (chọn trần `answer_max_output_tokens`, ghi cả ca hết token trước / sau chữ đầu);
  ngắt thật 2 thời điểm bằng curl (một dòng log, `outcome = client_disconnected`); C5 trên ≥ 5 câu (chữ ghép từ `delta` = chữ cuối đã chuẩn hóa); T1 giống byte. **Không** giao diện (S3), không đo
  tốc độ D2 (S4). Tiền ≤ 0,005 USD (pilot ≤ 0,001 + cổng ổn định + C5; ghi usage + tiền). Dependency `fastapi>=0.135` (A tự duyệt, spec §8). Đầu ra `s2_stream_route_implementation.md`, push nhánh.
  Dừng + báo A: thư viện không cho stream JSON như C97 đã probe; cần đổi spec; vượt tiền.
- **B — B107 đề xuất sửa câu Golden lệch kho (GIAO 10:57 01/11/2026):** chạy `cd backend && HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus.jsonl`
  ⇒ câu lỗi (dòng 128); tìm đoạn kho mới tương ứng **chỉ** bằng `scripts/grep_kb.sh`, đối chiếu sao lưu đợt 1 / 2 trong `knowledge-base-hue/meta/` để biết kho đổi chữ gì. Viết đề xuất (keyword mới nguyên văn
  trong kho; đáp án mẫu có cần đổi không; ảnh hưởng: md5 Golden, gold v5, số chấm cũ) vào `data/golden_sua_2026-11-01/b107_de_xuat.md` (private, được chép nội dung câu). **Không sửa Golden** (User duyệt
  trước). Report tracked nếu có: mức loại câu. 0 USD. Xong nhắn A.
  - **Trạng thái (11:00 01/11/2026, B): xong — chờ A trình User.** Nguyên nhân: đợt 2 đổi `Số 102` ⇒ `số 102` trong kho; `check` so nguyên văn phân biệt hoa / thường (chấm thì không). B khuyên PA1: keyword đổi `S` ⇒ `s`, đáp án mẫu giữ; md5 ⇒ `2d761710af31`; số chấm / gold v5 / T1 không đổi. `data/golden_sua_2026-11-01/b107_de_xuat.md` (`16ebb5224c98`). Golden chưa sửa.
- **B — S1 streaming: gom lõi chung (GIAO 10:43 01/11/2026; spec duyệt `00fb57ee01b2`, commit `74a6082`):**
  - **Trạng thái (10:56 01/11/2026, B): chờ review (C)** — nhánh `s1-loi-chung` `9c83003` (đã push); T1 giống byte `4d5bbe9e0edc`; test file chạm đạt; cổng ổn định C4 đạt; `answer_case` 3 câu dev nhánh ↔ `main` cùng luật; ≈ 0,0018 USD. Report `report_agent/2026-10-31_streaming_spec/s1_loi_chung_implementation.md`.
  - Mục tiêu: một lõi chung "tìm → dựng ngữ cảnh → sinh → kiểm citation" mà `POST /api/chat` (`backend/api/routes/chat.py`) và `answer_case` (`backend/evaluation/full_corpus_eval.py:322`) cùng gọi;
    **chưa** có stream, **hành vi không đổi**. Đọc (full): spec §4.1, §4.8 (5 khác biệt phải giữ), §5 hàng S1, §6 C4–C5, §7, §8; `chat.py`, `full_corpus_eval.py` (đoạn `answer_case` + chỗ gọi).
  - Làm: nhánh `s1-loi-chung` từ `main` `74a6082` (worktree riêng nếu tiện — bẫy worktree `Project_Status.md` §8); `git grep` mọi nơi gọi hàm sắp đổi **trước** khi sửa; skill `practical-project-coding`;
    khai báo file ở STATUS_B. Tên / chỗ đặt hàm B chọn, ghi trong report. Không thêm abstraction phòng xa cho S2 (chỉ thứ S1 cần + thứ spec §4.8 ghi).
  - Kiểm (spec §5 S1): T1 158 câu **giống byte** `4d5bbe9e0edc` (cách chạy như các lần trước — `guides/full_corpus_rag.md`); test file chạm; cổng ổn định §6 C4 trên `/api/chat` (1 câu trong kho + 1 ngoài kho tự viết,
    `chat_metrics` mới = số câu, grep câu hỏi trong log = 0, tắt server); `answer_case` chạy 2–3 câu dev (không câu kín / nhóm test) ⇒ trường ra cùng luật như hôm nay; 5 khác biệt §4.8 còn nguyên
    (đọc diff + test logic: lỗi `answer_case` vẫn ra `row["error"]`); `test_phase6_live_smoke.py` cần key ⇒ chạy được thì chạy, không thì ghi **NOT RUN**. `git diff --check`; hook tự chạy.
  - Không làm: route stream, giao diện (S2–S3); sửa `cost_usd` (việc đóng gói, sau S1 merge — cùng file); đổi prompt / model / settings; ghi Qdrant.
  - Tiền: ≤ 0,005 USD (cổng ổn định + 2–3 câu `answer_case`; ghi usage token + tiền). Vượt ⇒ dừng báo A.
  - Đầu ra: `report_agent/2026-10-31_streaming_spec/s1_loi_chung_implementation.md` (`TEMPLATE_IMPLEMENTATION_REPORT.md`) + nhánh push `origin` (được phép, nhánh riêng); không commit `main`.
    Dừng + báo A khi: T1 lệch; một khác biệt §4.8 buộc phải đổi; cần đổi spec. Xong ⇒ "chờ review", nhắn A (C review, W32 ca dò khác cách).
- **B — kiểm phần đổi spec sau Q1 (GIAO 01/11, bản 5 `0b2679cfccd6`):** căn cứ: `git diff` (hoặc `diff`) spec bản mới ↔ `cf1ae9ef6c2c` + câu trả lời Q1 User (A ghi vào mục Streaming); chỉ kiểm chỗ `TBD` §2 + §6 C1 và mọi
  chỗ nhắc tới nó; không đổi chỗ khác; không chạy Codex. Đầu ra: mục "Vòng 3" cuối `report_agent/2026-10-31_streaming_spec/b105_review.md` + sha bản kiểm. 0 USD.
- **Báo cáo so sánh (1b) ĐÃ GHÉP 11:29 01/11/2026:** `bao_cao_he_thong/BAO_CAO_SO_SANH_PHUONG_AN.md` bản 3 (từ nháp C `f1722077fc48` + 3 sửa nhỏ của A); review R1 / R2 vòng 2 ready (`data/so_sanh_phuong_an/review_r*.md`). Phần streaming + đo cuối thêm khi làm.
- **Trạng thái 11:35 01/11/2026:** B review plan C103 ⇒ changes_requested (1 major / 6 minor, `c103_plan_review.md`) ⇒ C sửa trước C106. **B — S3 giao diện** bắt đầu song song (nhánh `s3-giao-dien` từ `830df0e`, cổng 8793, ≤ 0,003 USD) — **không bàn giao tới khi S2 review đóng** (A cho phép lệch thứ tự "review trước bước sau" vì hợp đồng sự kiện cố định trong spec §4.4; S2 có finding ⇒ sửa S2 trước, rebase S3).
- **12:02 01/11/2026:** Q3a (B) xong — chỉ **câu nhiều nguồn** còn lớn (18 câu: Đủ 3,50 ↔ 4,92 câu một dữ kiện; 8 câu yếu đều thiếu bằng chứng tầng tìm; 8 / 12 từ chối nhầm); bảng giá không còn lớn; so sánh không qua luật ⇒ **User: câu nhiều nguồn để Phase 9** (agent tách câu con), không mở plan. **S3 review (C107) changes_requested** M-1 lọt `background` / `input image` + `/static/index.html` thiếu CSP ⇒ B sửa ⇒ C kiểm.
- **12:07 01/11/2026:** S3 M-1 sửa `716ba4d` (danh sách cho phép DOMPurify + CSP mọi trang dưới `/static`; probe C 0 request ở cả hai đường) ⇒ C kiểm phần sửa. **B:** nhánh gộp `streaming-final` (= `s3-giao-dien` + `dg-cost-usd`) + chuẩn bị S4 (chưa chạy — chờ S3 đóng + W31).
  **Bộ kín mới:** agent viết xong 40 câu (`final_sealed.jsonl` `c2a2c9df8169`; 12 / 6 / 6 / 10 (6 + 4 cảnh báo) / 6 ngoài kho; A giao 12 / 6 / 6 / 6 — lệch nhỏ so với tỉ lệ Golden 14 / 6 / 5 / 5, ghi giới hạn); giữ 5 khoá (lệnh `check --authoring` đòi `partition` không dùng ở bộ này — dùng `check` thường trên bản 4 khoá); agent kiểm (mới) đang chạy; A không đọc nội dung.
- **C106 R9 (11:56 01/11/2026):** User chạy `! chmod 600` cho file khoá, không lỗi; A không tự kiểm được (quyền chặn mọi lệnh nhắc tới file đó — đúng thiết kế). C106 review: changes_requested (`c106_bao_mat_review.md`) ⇒ C sửa sau review S3. **Bộ kín mới:** agent con viết 40 câu (A không đọc; trả số đếm + sha).
- **Plan đo cuối C103 DUYỆT bản sha `ae8d42d520d4` (A, 11:53 01/11/2026, sha tính từ file):** B review 3 vòng ready (`c103_plan_review.md`); 4 câu User đã điền; n-6 (2 chỗ chữ "nếu Q2" ⇒ đọc là Q2 = PA1) không sửa để giữ bản duyệt. **B chạy Q3a** (đo lại L2 / L3 theo loại câu, 0 USD).
- **S3 bàn giao (11:52 01/11/2026):** nhánh `s3-giao-dien` `9374212` + `fc10873` (giao diện đọc luồng + C106 R2: chặn ảnh / media / style khi render + CSP cho `/`); B ≈ 0,0030 USD (chạm trần 0,003). **C review S3** (≤ 0,002 USD, cổng 8795). Plan C103 bản 4 `ae8d42d520d4` (C điền 4 câu User) ⇒ B Vòng 3.
- **Plan C103 — User Q4 = trần 0,20 USD** (A ghi nhận 11:47 01/11/2026); đủ Q1–Q4 ⇒ C điền `TBD` ⇒ B kiểm ⇒ A duyệt sha ⇒ C chạy Q3 (đo lại theo loại câu, 0 USD). C106 ⇒ review agent con. S3 thêm chặn ảnh / link ngoài khi render (C106 R2, A quyết).
- **S2 ĐÓNG (11:45 01/11/2026):** m-1 sửa `887cbc5`, A kiểm bằng ca dò reviewer 0 / 16.000. Plan C103: User Q2 = **thêm A/A cùng ngày**, Q3 = **đo lại theo loại câu trước** (0 USD) rồi mới quyết thử. C106 bảo mật xong (`c106_bao_mat_dong_goi.md` `2ef499b91a59`, 11 rủi ro, 0 blocker) — chờ review + User quyết R4 / R9 / R10.
- **S2 review XONG (11:40 01/11/2026):** agent con ngữ cảnh mới — `s2_stream_route_review.md` **ready**, 0 blocker / 0 major, 2 minor: **m-1** emoji (ngoài BMP) cắt giữa cặp surrogate khi model thoát ASCII ⇒ nửa ký tự ⇒ lỗi luồng
  (hiếm — 7 / 7 lần thật model gửi UTF-8 thô) ⇒ **B sửa trên `s1-loi-chung` + 1 test** rồi rebase S3; **m-2** trường log `delta_matches_final` (cờ, không nội dung) ⇒ **A quyết giữ** (đo C5 từ log; ghi vào spec §4.6
  khi đóng spec — a6, không mở bản spec mới lúc này). Ghi cho S4: một câu có `first_text_ms` server 4,08 s (một lần) — sát sàn p95. Plan C103 bản 3 `4d653544fb73`: B vòng 2 ready; User Q1 = **chỉ agent 40 câu** (11:40 01/11/2026).
- **A tự duyệt 11:35 01/11/2026 (báo User sau, `Session_Prompt.md` §4):** thêm `playwright` (Python) nhóm **dev** (`uv add --group dev`, nhánh `s3-giao-dien`) — spec streaming §7 / S4 đo bằng Playwright; chọn bản khớp trình duyệt có sẵn trong cache (không tải).
- **C — C106 rà bảo mật một lần lúc đóng gói (GIAO 11:33 01/11/2026):** skill `agent-security-review` mục 1, 2, 5, 7, 8 (+ 3, 4 nếu thấy liên quan) cho chatbot **như sẽ vào `main` sau streaming**: `main` + nhánh
  `s1-loi-chung` `830df0e` + `dg-cost-usd` `bbbdbf9` (đọc nhánh, không sửa). Kê bộ ba (dữ liệu riêng tư runtime đọc được · nội dung không tin cậy vào ngữ cảnh: câu người dùng + kho lấy từ web · đường ra:
  phản hồi API, log, gọi OpenAI); log có lộ chữ người dùng / khoá không (`chat_metrics`, route stream); route stream có đường ra mới không; dữ liệu gửi nhà cung cấp; chính coding agent (mục 7: hook,
  `.claude/settings.json`, `scripts/tra_web_codex.sh`). Đầu ra: `report_agent/2026-10-31_streaming_spec/c106_bao_mat_dong_goi.md` (bảng rủi ro · hiện trạng `file:dòng` · mức · đề xuất) + đoạn
  **"giả định an toàn"** đề xuất cho `LUONG` (A ghép). Chỉ đọc; được chạy probe nhỏ 0 USD (grep log, đọc cấu hình) — không gọi API, không chạy server, không mở `.env` (chỉ kiểm `.gitignore` / quyền file
  bằng `ls -l`). Không sửa code / governance. Xong báo A sha; review: B hoặc agent con.
- **C105 XONG + ĐÃ GHÉP 11:33 01/11/2026:** bảng giới hạn bản 4 `f1a7c4cad145` (private); khối giới hạn ⇒ `LUONG` §5 bản 15 (A kiểm 3 số với nguồn). **B108 review ready** (A, `b108_cost_usd_review.md`).
- **C — C105 bảng giới hạn đã biết bản 4 + nháp `LUONG` §5 (GIAO 11:27 01/11/2026):** 0 USD, chỉ tài liệu. (1) Cập nhật `data/dong_goi_2026-10-30/gioi_han_da_biet_nhap.md` (bản 3 `8211d5d6eb7f`, C viết) theo
  hiện trạng 01/11: kho sau đợt 2, Qwen3-8B, streaming spec §10 giới hạn (S1–S2 đã làm), nhiều lượt dời Phase 9, tốc độ qua API (p95 6,0 s chưa đạt), Golden 127 giữ nguyên, `cost_usd` (B108 đang sửa) —
  dòng không còn đúng thì sửa / xoá; mỗi dòng có nguồn `file:dòng`. (2) Nháp mục "Giới hạn đã biết" cho `bao_cao_he_thong/LUONG_HOAT_DONG_HE_THONG.md` §5 (lời thường cho User, mức loại câu, mức nặng
  M1–M5 / PCN / ĐO / VH giải nghĩa) vào `data/dong_goi_2026-10-30/luong_muc5_de_xuat.md` — **không sửa `LUONG`** (A ghép). Đối chiếu bản public báo cáo so sánh (§6 "Giới hạn chung") để không mâu thuẫn.
  Xong ⇒ báo A sha; review: agent con ngữ cảnh mới (A giao).
- **C — C103 kế hoạch lượt đo cuối Phase 1–8 (bản 2 `ba70843a4652`, B review; GIAO 11:12 01/11/2026):** 0 USD, chỉ tài liệu. Nháp `docs/superpowers/plans/2026-11-01-do-cuoi-phase-1-8-plan.md` — kế hoạch có **tiêu chí ghi trước**
  (`WORKFLOW.md` §9.1: đầu file "Căn cứ để review" 2–4 file). Nội dung (theo `CURRENT_HANDOFF.md` mục 4 "Đóng gói" + `Project_Status.md` §1 mục tiêu / thứ tự lỗi / yêu cầu phi chức năng): đo gì
  (Golden 176 + an toàn 32 + 15 câu theo ngày + tốc độ trên trình duyệt + **bộ kín mới** + kết quả B0), **cùng một commit** (sau khi streaming + nhiều lượt vào `main`), thước + sàn + mức tụt cho phép mỗi bộ,
  cỡ mẫu, ước tiền / giờ (từ log thật), thứ tự chạy (W31: không việc nặng song song lúc đo tốc độ), **bộ kín mới**: ai viết / ai kiểm / ai không được đọc (giữ mù — người đề xuất biến thể, A), mức loại câu, so SHA256
  với mọi file thử cũ; "thử thêm có giới hạn" chỉ cho 3 lỗi đã biết (từ chối nhầm 12 / 158, câu so sánh / nhiều nguồn, bảng giá) — mỗi cái: nghiên cứu ngoài trước, luật giữ / bỏ. Chỗ cần User chọn ⇒ `TBD`
  + khối "Câu hỏi cho User" (`propose-options`). Đọc thêm: skill `run-experiment`; bảng giới hạn `data/dong_goi_2026-10-30/gioi_han_da_biet_nhap.md`; số hiện trạng từ `bao_cao_he_thong/` (đã sửa 01/11).
  Không: chạy đo, viết câu kín, mở `*sealed*`, gọi API. Xong ⇒ báo A sha.
- **C — C102 nháp spec hội thoại nhiều lượt (XONG 11:11, bản 1 `45d159e09636`; **dời Phase 9** — User 11:20 01/11/2026, không hỏi Q2–Q4, không review; GIAO 11:05 01/11/2026):** C101 (1b) xong 11:04 — A ghép + cho kiểm. Việc mới, 0 USD, **chỉ tài liệu** (không code):
  nháp `docs/superpowers/specs/2026-11-01-multi-turn-design.md` theo khuôn spec streaming (mục tiêu, quyết định, phạm vi, thiết kế, bước, tiêu chí bằng số, cách kiểm, quyền / tiền, rủi ro,
  giới hạn, "Căn cứ để review"). Gốc: nháp C91 `data/tinh_nang_moi_2026-10-27/c91_phuong_an_nhieu_luot.md` (PA1 trình duyệt giữ lịch sử, server không lưu) + **code thật sau S1**
  (`backend/llm/grounded_answer.py` trên nhánh `s1-loi-chung` `9c83003` — đọc nhánh, không sửa) + spec streaming đã duyệt (route stream sẽ có). Chỗ cần User chọn ⇒ để `TBD` + một khối
  "Câu hỏi cho User" (mỗi câu 2–3 phương án, hệ quả, khi nào sai, khuyên gì — skill `propose-options`); mọi khẳng định về code kèm `file:dòng`. Câu dùng làm ví dụ: tự viết, mức loại câu.
  Không làm: code; sửa spec streaming / handoff mục khác; tra web (nếu cần nguồn ngoài ⇒ ghi câu cần tra, A quyết). Xong ⇒ báo A sha; A trình User từng câu rồi cho session khác review.
- **C — việc 1b (XONG 11:04, C101; GIAO 10:28 01/11/2026; User chọn "giao C ngay"):** gom báo cáo so sánh **phần đã đóng** (Phase 0 → 8.2, sửa kho đợt 1 + 2, Qwen3-8B, thước lỗi nặng / ngày hôm nay).
  - Mục tiêu: nháp đủ để A ghép `bao_cao_he_thong/BAO_CAO_SO_SANH_PHUONG_AN.md` theo khung mục 4 "Báo cáo tổng so sánh" (đọc full mục 4 trên). Phần **theo khâu** là chính (đủ số đo);
    phần **theo Phase** chỉ bảng một hàng / Phase trỏ về phần khâu + chỉ mục chéo; "nhìn lại theo khung khoá AI FDE" để bước đóng gói (không làm ở 1b). Streaming / nhiều lượt chưa có ⇒ để chỗ trống ghi "chưa làm".
  - Đọc (targeted): `bao_cao_he_thong/BAO_CAO_*.md` (9 khâu) + `LUONG_HOAT_DONG_HE_THONG.md`; `report_agent/*/TONG_HOP.md` + report gốc khi cần số; `reports/` (Phase 0–7, lịch sử); `docs/superpowers/specs/`;
    `guides/`; `Project_Status.md` §5; bảng giới hạn `data/dong_goi_2026-10-30/gioi_han_da_biet_nhap.md` (để không lặp, trỏ chéo).
  - Làm: dùng agent con theo nhóm khâu (gợi ý ~5, chạy song song; mỗi agent đọc file dài ≤ 3 cái — `WORKFLOW.md` §9.9: brief có khuôn trả về cố định, tách "nguồn nói" ↔ "suy ra",
    báo chỗ tài liệu mâu thuẫn nhau). Mỗi so sánh: vấn đề · ngày / Phase · mọi phương án + mốc · cách đo · tiêu chí ghi trước · kết quả số (CI, thắng / hoà / thua) · tiền + tốc độ ·
    quyết định + lý do · giới hạn · bằng chứng (report, commit, sha) · **nhãn độ tin** (5 nhãn ở mục 4). Số nào cũng có nguồn; không chắc ⇒ "chưa đo" / "chưa kiểm".
    C tự kiểm 2–3 số quan trọng mỗi nhóm bằng file thật trước khi gộp.
  - Không làm: không sửa `bao_cao_he_thong/`, guide, spec, governance (A ghép + sửa); không chạy đo / API trả phí; không mở câu kín, `split.json` theo từng câu, `.env`; tìm trong kho **chỉ**
    `scripts/grep_kb.sh` (thường không cần đọc kho). Agent con kế thừa đúng các ranh giới này (ghi vào brief).
  - Đầu ra: `data/so_sanh_phuong_an/` (private): `nhap_theo_khau.md`, `nhap_theo_phase.md`, `cho_mau_thuan.md` (số / kết luận lệch giữa các tài liệu, kèm `file:dòng`), `brief_agent_con.md`;
    **bản đề xuất public** `data/so_sanh_phuong_an/BAO_CAO_SO_SANH_PHUONG_AN_de_xuat.md` — mức loại câu (`Session_Prompt.md` §5: không chủ đề cụ thể cạnh `case_index`, không chi tiết dự án
    khác, không nguyên văn kho / Golden). Báo A kèm sha các file. STATUS_C khai báo.
  - Tiền: 0 USD. Dừng + báo A khi: thấy tài liệu mâu thuẫn làm đổi một quyết định đã chốt; khối lượng vượt ~3 giờ; cần mở thứ ngoài danh sách đọc.
  - Sau: A ghép + B (hoặc agent con ngữ cảnh mới) kiểm độc lập; A commit sau khi hỏi User.

## Quyền

- **Phiên 01/11 (User chọn "như 31/10", A ghi nhận 10:28 01/11/2026):** A tự điều phối B / C + tự thử trong luật; paid ≤ 1 USD cả phiên (A, B, C); B / C push nhánh riêng khi việc ghi rõ;
  commit `main`: A hỏi User trước. User nói ở terminal B (10:19): việc A giao B = "làm đi". **Hết hạn cuối phiên 01/11.**
  **User 11:26 01/11/2026: A tự commit + push không cần hỏi** (phiên 01/11; hết hạn cuối phiên — vẫn stage từng file đã review, hook chạy, không commit dữ liệu private).
  **User 10:30 01/11** (A ghi 10:32 01/11/2026): "tiếp tục điều phối, phát triển, cải thiện, tối ưu, so sánh đánh giá, viết báo cáo"; đóng phiên **~16:20**; hỏi "hôm nay xong Phase 8 được không" — **chỉ hỏi, không yêu cầu làm nhanh rồi bỏ sót**.
- **Phiên chiều 31/10 — HẾT HẠN (User, A ghi nhận 15:59 31/10/2026):** phiên này **chỉ làm AI FDE** (khung `khung_fde/`, đối chiếu, harness); **chưa làm tiếp dự án**
  (spec streaming Q1 / duyệt sha, code S1… để phiên sau). A được commit + push. Không cấp trần tiền paid (việc AI FDE 0 USD). Hết hạn cuối phiên.
- **Thường trực:** A commit / push — **hỏi User trước** (luật chung của User `~/.claude/CLAUDE.md`, thắng "quyền thường trực" ở `Session_Prompt.md` §4), rồi **A tự chạy**; chỉ khi lệnh bị chặn / lỗi mới đưa User lệnh `!` (User 31/10 11:44; S50 đóng — 31/10 commit `1a9dca4`, `16f482a`
  A tự chạy được); B/C không commit trừ khi việc ghi rõ (nhánh riêng); duyệt cho A = duyệt cho B/C; thư viện nhỏ cần cho việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích
  ghi trong việc; paid ghi usage token + tiền; code luôn `uv run`; luôn thử + so baseline trước khi chọn.
- **Tra web:** mọi session tự chạy `scripts/tra_web_codex.sh` (chỉ thông tin công khai; 0 USD — gói tài khoản ChatGPT của User); **không bao giờ gọi `agy`** (điều khoản Google).
- **Phiên 31/10 — HẾT HẠN** (như 30/10; ≤ 1 USD). Tiền phiên 31/10: **0 USD** paid API (A, B, C); Codex / AGY theo gói tài khoản.
- Giá `gpt-6-luna` (User 30/10): vào 0,10 · ra 0,50 · đọc đệm 0,01 · ghi đệm 30 phút 0,125 USD / 1M.

## File private quan trọng (không commit)

| File | Nội dung | sha256 (12) / md5 |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_v5.jsonl` | nhãn đoạn đúng mặc định (kho đợt 2) | `33d16fd6b8f4` |
| `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` | Golden 176 | md5 `6331e88fb171` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` | 36 câu kín — đã dùng (B3); không chép nội dung | md5 `ddc59587b502` |
| `data/phase_8_2/b0/` | đọc cặp mù (`khoa.json` chỉ A) | — |
| `data/loi_nang_2026-10-28/` | thước lỗi nặng; `an_toan/questions.jsonl` 32 câu | `9fa81b0fcec4` |
| `data/tinh_nang_moi_2026-10-27/` | nháp streaming v2 / v3, C97, B99, B104, kết quả thô Codex review, nhiều lượt C91 | — |
| `data/tra_cuu_cli_2026-10-31/` | thử 6 lượt Codex / AGY: `tieu_chi.md`, `yeu_cau/`, `ket_qua/`, `log/`, chấm `c99_cham.md` (`514ea908654b`), mốc Y2 `b101_cham.md` | — |
| `data/tra_cuu_cli/<ngày>_<tên>/` | đầu ra `scripts/tra_web_codex.sh` (31/10: `thu-script`, `thu-script-json`, `ttft-chuan-nganh`) | — |
| `data/dong_goi_2026-10-30/` | bảng giới hạn Phase 0–8 (nháp) | `8211d5d6eb7f` |
| `gửi chatgpt/2026-10-31/` | yêu cầu Y3 (`b51687978f9f`) + kết quả (`kết quả/…`, `02f7735fa2b7`) | — |

## Việc đang mở — luật chung khi sửa code / dữ liệu

- A commit + push `main` **trước** khi B / C sửa code; khai báo file trong `STATUS_<X>.md` trước khi sửa; skill `practical-project-coding`; test liệt kê file; report
  `<việc>_implementation.md`; review chéo (W32: ca dò khác cách + câu bất biến); plan có tiêu chí ghi trước ⇒ session khác review **trước** khi A duyệt sha (sha tính từ file).
- **Cổng ổn định:** (1) test file chạm; (2) `cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port <cổng trống>`: `/` 200, `/health` 5 / 5,
  1 câu trong kho + 1 câu ngoài kho (câu tự viết); đếm `chat_metrics` mới = số câu; grep câu hỏi trong log = 0; tắt server (TaskStop); (3) chạm tìm / chia đoạn: T1 giống byte; (4) đủ
  5 chỗ (`WORKFLOW.md` §6); (5) hook tự chạy.
- **Có lượt đo latency ⇒ session khác không chạy lượt trả phí / việc nặng CPU / Qdrant** (W31).
- Test cần key: `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan`, `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`,
  `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`.
- Đọc kho: **chỉ** `scripts/grep_kb.sh`; report tracked tả câu ở mức loại câu. Giờ trong file **và trong tin nhắn**: chạy `date` trước (S49). `rm` với biến: dùng `"${X:?}"/…` hoặc
  đường dẫn cố định (tầng an toàn chặn `$X/*`).

## Hồ sơ đã đóng (chỉ tra cứu)

- Phase 8.2 (User đóng 28/10): `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
- Đợt sửa kho 1 + 2, thước lỗi nặng, đo ngày hôm nay, Qwen3-8B: `report_agent/2026-10-27_phan_ton_phase_cu/` — `TONG_HOP.md` §7–§8.
- Tra web bằng Codex (31/10, đóng): `report_agent/2026-10-31_tra_web_codex/TONG_HOP.md`.
