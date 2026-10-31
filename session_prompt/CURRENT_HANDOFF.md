# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 16:46 31/10/2026 (A, phiên chiều 31/10 — chỉ AI FDE; mục "PHIÊN SAU" viết lại lúc kết phiên chiều). Trước: 12:36 31/10/2026 (A, **kết phiên 31/10** — User: "các nhiệm vụ, câu hỏi để session tiếp theo"). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở.
Lịch sử phiên 31/10 (mục việc B99–B106, C97–C100, quyết định theo giờ, mọi trạng thái review) dời **nguyên văn** sang `session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-10-31.md`
(I7); phiên 28–30/10: `archive/CURRENT_HANDOFF_LICH_SU_2026-10-28_30.md`. Tổng hợp đợt: `report_agent/2026-10-31_streaming_spec/TONG_HOP.md` (mở),
`report_agent/2026-10-31_tra_web_codex/TONG_HOP.md` (đóng); nhật ký User `bao_cao_he_thong/nhat_ky/2026-10-31_spec_streaming_tra_web_codex.md`.

## PHIÊN SAU ĐỌC TRƯỚC (đọc trước nhất)

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
3. **Hội thoại nhiều lượt:** nháp `data/tinh_nang_moi_2026-10-27/c91_phuong_an_nhieu_luot.md` (`1c0313aafd25`; PA1 trình duyệt giữ lịch sử, server không lưu) ⇒ spec **sau** streaming
   (cùng sửa `chat.py` + `app.js` ⇒ làm tuần tự — spec streaming §2 D0).
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
- **Spec:** `docs/superpowers/specs/2026-10-31-streaming-design.md` bản 4 **`cf1ae9ef6c2c`** (202+ dòng; quét trùng 0; commit kết phiên nếu User đồng ý — xem mục "A còn nợ"). Review: B105 vòng 1 changes_requested
  (M-1 hủy khi ngắt: ghi log trước mọi `await` + `CancelScope(shield=True)` + `move_on_after`) ⇒ vòng 2 ready (`report_agent/2026-10-31_streaming_spec/b105_review.md` `96bcc907886b`);
  **Codex review một lần (W33) xong** trên bản 3 `cd44744ea3d7` — 2 finding đúng, mới, hạ minor (bắt riêng `CancelledError`; 422 trước handler không có dòng log) ⇒ C sửa ⇒ bản 4,
  B kiểm phần đổi ready (`b106_codex_review.md` `cab2ca485750` mục 5). Kết quả thô Codex (private): `data/tinh_nang_moi_2026-10-27/2026-10-31-streaming-design_review_codex/`.
- **Còn mở:** `TBD` ở spec dòng ~46 (§2) và §6 C1 = **câu Q1 cho User** (dưới). Căn cứ: Codex tra `data/tra_cuu_cli/2026-10-31_ttft-chuan-nganh/ket_qua.md` — **không có chuẩn ngành**;
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
4b. **Golden lệch kho 1 câu** (A chạy `golden_full_corpus check` 17:17 31/10/2026: 176 đọc được, 1 lỗi "keyword not verbatim in corpus" ở dòng 128 — không in nội dung): duyệt sửa
   keyword / đáp án mẫu theo kho mới? (Golden md5 sẽ đổi ⇒ ghi lại mốc.)
5. (Khi bàn spec nhiều lượt) lưu câu hỏi người dùng? (PA1 C91 không lưu.) (Khi rảnh) B0; 20 câu mẫu lỗi nặng; xoá sao lưu đợt 1 + 2 khi đóng gói.
6. (Không gấp) File untracked `báo cáo nghiên cứu github.txt` (gốc repo, 82 KB, 01/10 — khảo sát đồ án gợi ý địa điểm / lịch trình): giữ ngoài git, hay dời vào `data/`?
   4 worktree AGY cũ (`~/.gemini/antigravity-cli/…`, nhánh `subagent-Monuments-Reviewer-*`, commit `c725987` 05/09): giữ hay gỡ (User `!`)?

## Câu hỏi A còn nợ (không cần User)

- Khung AI FDE (khung cá nhân của User, ngoài repo) đã lên v2 phía dự án kia: mở phiên đọc `CHANGELOG.md` của khung; mục nào đổi mà hue_rag cần ⇒ đối chiếu lại (vòng cải tiến).
  W39 hạn 07/11 (0 buổi D ⇒ đề xuất gỡ W4 + W39); theo dõi W37 báo đúng / nhầm; I3 memory.

- Sổ: theo dõi W32 (31/10 có tác dụng: B103 M-1, B105 M-1 đều từ ca dò khác cách), I7, W30 (hook bắt 2 giờ ước 31/10), W31; W33 đã chạy — kết luận ở sổ.
- Ý chờ từ B106 §3: cho Codex review đọc mã nguồn thư viện / `.venv` chỉ đọc (đổi phạm vi — cần User nếu muốn).
- Lần chấm tra web sau (C99 nêu): đếm riêng "403 trang thật" + kiểm tiêu đề trang mỗi URL (6 khẳng định không bắt link trỏ sai bài). Ca 503 / 502 route stream: A đã quyết = giới hạn.
- Spec + `report_agent/2026-10-31_streaming_spec/`: A xin User commit lúc kết phiên 31/10 — mở phiên kiểm `git log --oneline -3` / `git status`; còn untracked ⇒ A commit sau khi hỏi (bản nháp chờ duyệt; duyệt vẫn gắn sha tính từ file).
- Thử mở phiên vai B (sub-agent, 31/10 kết phiên): tài liệu đủ; đã sửa 7 chỗ (tên mục, mã chưa giải nghĩa, việc soạn sẵn cho B, dòng cũ Project_Status §2, sàn cả câu ↔ D2,
  luật hỏi commit, WebSearch thử ⇒ lỗi 400). Lưu ý: phiên Claude mở **trước** `1a9dca4` nạp `AGENTS.md` cũ (thiếu luật 7) — phiên mới thì đủ.
- Log `FileHandler` không xoay vòng — xem lại khi deploy. C65: G2.1a chưa đếm lại bằng validator hiện tại.

## Session

| Vai | Terminal (31/10) | Agent | Liên lạc | Phiên 31/10 | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-1a` (chiều 31/10: `hue-rag-d5`) | Claude Opus 5.5 | trực tiếp | điều phối; thử 6 lượt Codex / AGY; script tra web + chặn `agy` + §9; 3 câu User streaming; tra Codex TTFT | `STATUS_A.md`; 0 USD |
| B — thực thi | `hue-rag-3b` | Claude Opus 5.5 | trực tiếp | B99 kiểm nguồn, B100 review C97, B101 mốc Y2, B102 review v3, B103 review governance, B104 gói Codex, B105 review spec, B106 chạy Codex review | `STATUS_B.md`; 0 USD |
| C — thực thi | `hue-rag-69` | Claude Opus 5.5 | trực tiếp | C97 đối chiếu code, C98 nháp v3, C99 chấm 6 bản tra web, C100 spec streaming (4 bản) | `STATUS_C.md`; 0 USD |

Tên terminal đổi mỗi lần mở: `ListAgents`. Cả ba Claude Code ⇒ `trực tiếp`. **B / C lúc mở phiên sau:** không có việc đang chạy; mở phiên ⇒ kiểm nhanh ⇒ báo A ⇒ chờ.

**Việc soạn sẵn (A giao bằng tin nhắn khi tới bước):**
- **B — kiểm phần đổi spec sau Q1:** căn cứ: `git diff` (hoặc `diff`) spec bản mới ↔ `cf1ae9ef6c2c` + câu trả lời Q1 User (A ghi vào mục Streaming); chỉ kiểm chỗ `TBD` §2 + §6 C1 và mọi
  chỗ nhắc tới nó; không đổi chỗ khác; không chạy Codex. Đầu ra: mục "Vòng 3" cuối `report_agent/2026-10-31_streaming_spec/b105_review.md` + sha bản kiểm. 0 USD.
- **C — rảnh có lý do** cho tới khi spec duyệt (người viết spec không tự kiểm); sau duyệt A giao code S1 cho một session, session kia review.

## Quyền

- **Phiên chiều 31/10 (User, A ghi nhận 15:59 31/10/2026):** phiên này **chỉ làm AI FDE** (khung `khung_fde/`, đối chiếu, harness); **chưa làm tiếp dự án**
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
