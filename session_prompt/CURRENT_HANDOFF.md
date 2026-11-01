# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 13:36 01/11/2026 (A, **kết phiên 01/11**). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở. Lịch sử phiên 01/11 (mọi mục việc B / C, quyết định theo giờ, trạng thái review) dời
**nguyên văn** sang `session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-11-01.md`; 31/10: `archive/CURRENT_HANDOFF_LICH_SU_2026-10-31.md`. Tổng hợp đợt: `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`;
nhật ký User `bao_cao_he_thong/nhat_ky/2026-11-01_streaming_va_dong_goi.md`.

## PHIÊN SAU ĐỌC TRƯỚC (đọc trước nhất)

**Hệ thống (`main`, sau merge `a80e12d` 01/11):** chatbot có **chữ hiện dần** — `POST /api/chat/stream` (SSE) + giao diện JS thuần đọc luồng (allowlist DOMPurify, CSP mọi trang HTML); `/api/chat` giữ;
API + bộ đánh giá dùng chung lõi `backend/llm/grounded_answer.py`; `cost_usd` theo giá đủ, `chat_metrics` ghi token đệm. Kho 204 file / 8.424 đoạn; record `51fb1ec63cbc`; sparse `c8134c49a648`; T1 `4d5bbe9e0edc`;
Golden md5 `6331e88fb171`; gold v5. Qdrant chạy bằng Docker Desktop — `curl :6335` không trả lời ⇒ báo User, không tự bật.
**Số cuối Phase 1–8 (lượt đo cuối 01/11, mọi sàn đạt; `report_agent/2026-10-31_streaming_spec/do_cuoi_implementation.md` + `do_cuoi_review.md`):** Golden "không làm hỏng" (2 câu tụt / ≤ 5; Đúng 4,71 · Đủ 4,58 ·
Trúng ý 4,72; từ chối nhầm 12 / 158); bộ an toàn đạt (A2 vế 1 đúng ngưỡng 2); câu theo ngày 0 đoán sai; **bộ kín mới** 0 / 6 ngoài kho, Đủ 4,18 ↔ 4,58 (câu được trả lời 4,60 ↔ 4,82 ⇒ số dev lạc quan thật);
chữ đầu trên trình duyệt 1,23 / 2,61 s (một lần đo; hôm đó model gần như không suy luận); ≈ 0,00025 USD / câu.
**Mới 01/11 (governance):** hook `.githooks/pre-push`; `scripts/tra_web_codex.sh` rào (không shell / file / trình duyệt); `WORKFLOW.md` §4 4b (W36), §6 (W45 — tin nhắn không cần giờ), §9.6 (I8).

**Thứ tự việc phiên sau:**
1. Mở A / B / C; `ListAgents`; **hỏi lại quyền phiên** (quyền 01/11 hết hạn — gồm "A tự commit / push không hỏi"); kiểm Qdrant.
2. **B0** (chỉ User làm được, ~30–45 phút): User đọc 20 cặp mù `data/phase_8_2/b0/nhan_xet_user.md` (không mở `khoa.json` / `mau.json`). Xong ⇒ A đối chiếu `khoa.json` (chỉ A), áp luật dừng spec 8.2 §3.4
   (≥ 5 cặp quyết; User ngược judge nhiều hơn cùng chiều ⇒ A trình giữ 10 đoạn / về 5); ghi vào `BAO_CAO_DANH_GIA.md` + báo cáo so sánh (khối context 10). Giới hạn: câu trả lời trên kho cũ, 1 câu nhiều nguồn.
3. **Đóng Phase 8 (User):** A trình tóm tắt (số cuối, giới hạn, B0) ⇒ User đóng ⇒ `Project_Status.md` bảng Phase (**thêm** dòng "8 — đóng gói Phase 1–8" ⇒ approved; bảng hiện chỉ có 8.1, 8.2, 9), `PROJECT_HISTORY.md` một mục trỏ TONG_HOP, guide Phase 8 "Hiện hành".
4. **Sau Phase 8:** (a) **giao diện mới** — đọc `report_agent/2026-10-31_streaming_spec/yeu_cau_cho_giao_dien_moi.md` (17 yêu cầu phải giữ); A sơ bộ nghiêng React + Vite build tĩnh, FastAPI phục vụ — chưa nghiên cứu,
   chưa chốt; **cân mức công** (User 01/11 nhắc over-engineer — S64): giao diện là đồ án, làm một lần, review cả nhánh một lần. (b) **Phase 9 — nghiên cứu rộng trước** (User 31/10), gồm **hội thoại nhiều lượt / nhớ
   lịch sử** (nháp tư liệu `docs/superpowers/specs/2026-11-01-multi-turn-design.md`) và **câu cần nhiều nguồn** (Q3a: Đủ 3,50; agent tách câu con) — `agent-design-review` + `agent-security-review` đầy đủ.

**Mã hay gặp:** T1 = kết quả tìm 158 câu (so "giống byte"); B0 = User đọc cặp câu trả lời mù làm mốc người; PA1 / PA3 = chữ hiện dần ↔ chỉ hiện tiến độ; D1–D5 / Q1 = câu quyết định
streaming (D5: xem lại PA3 nếu lợi < 0,5 s); Q3a = đo lại theo loại câu (01/11); F1–F4 / T1–T3 (plan đo) = sàn ngoài kho / bịa / lỗi kỹ thuật / lỗi trích dẫn và mức tụt Đủ / Đúng / từ chối nhầm; A1 / A2 = sàn bộ an toàn
(ngoài kho bị trả lời / nói sai điều kiện mới); `delta_matches_final` = cờ log "chữ ghép từ luồng = chữ cuối"; S / W / I = sự cố / đề xuất / dời luật trong `SO_CAI_TIEN_CACH_LAM.md`; CA / R = rủi ro trong
rà bảo mật C106; M-n / m-n = finding major / minor; Bxx / Cxx = mã việc A giao B / C.

## Câu hỏi cho User (hỏi mỗi lần một câu)

1. **Quyền phiên.** A khuyên: như 01/11 (A tự điều phối + tự thử trong luật; ≤ 1 USD; A tự commit / push; B / C push nhánh riêng).
2. **Xoá 4 nhánh đã merge** (`s1-loi-chung`, `s3-giao-dien`, `dg-cost-usd`, `streaming-final` — mọi commit đã có trong `main` qua merge `a80e12d`; không còn gì chỉ nằm trên nhánh) — User `!`
   (`git branch -d …` + `git push origin --delete …`). Nhánh cũ khác: `git branch -a` lúc mở phiên.
3. **Rà bảo mật C106 còn chờ User** (`report_agent/2026-10-31_streaming_spec/c106_bao_mat_dong_goi.md` bản 2): R4 xoá / cắt 22 dòng log cũ (08–10/2026) chứa nguyên câu hỏi thử trong `backend/logs/application.log`
   (gitignore); CA2 (`uv run *` / `python3 *` tự duyệt — khuyên giữ); R1 kiểm `Host` + giới hạn lượt khi deploy; R11 gỡ `gradio` không dùng (User 24/10: chỉ gỡ khi xung đột) — các mục deploy để lúc deploy.
4. **Sổ cải tiến chờ User:** W35 (kiểm điều khoản trước công cụ / tài khoản ngoài mới), W42 (hook cảnh báo "dự án khác"), W43 (script kiểm báo cáo khâu khớp hiện trạng). W44 User không chọn 01/11.
5. (Không gấp) `báo cáo nghiên cứu github.txt` (gốc repo, untracked): giữ ngoài git hay dời `data/`? 4 worktree AGY cũ (`~/.gemini/antigravity-cli/…`, nhánh `subagent-Monuments-Reviewer-*`): giữ hay gỡ (User `!`)?
   Xoá sao lưu kho đợt 1 + 2 khi đóng gói?

## Câu hỏi A còn nợ (không cần User)

- Ghi chú `delta_matches_final` vào spec streaming §4.6 nếu mở lại spec (đã ghi ở TONG_HOP "Giới hạn khi đóng"). 6 minor review cả nhánh ⇒ giới hạn (không sửa — giao diện làm lại).
- Bảng sổ cải tiến: S41–S44 thiếu 1 cột từ trước (B 01/11) — sửa khi tiện. W39 hạn 07/11 (0 buổi D ⇒ đề xuất gỡ W4 + W39).
- Log `FileHandler` không xoay vòng — xem lại khi deploy. Hạn mức tín dụng phía OpenAI cho key — chưa kiểm.

## Session

| Vai | Terminal (01/11) | Agent | Liên lạc | Phiên 01/11 | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-27` | Claude Opus 5.5 | trực tiếp | điều phối; review S1, B108; merge streaming; 5 chỗ báo cáo; CA1 / CA3; vòng cải tiến 13 | `STATUS_A.md` |
| B — thực thi | `hue-rag-da` | Claude Opus 5.5 | trực tiếp | S1–S4, B107, B108, review plan / runbook / governance, đo §6–§8 | `STATUS_B.md`; ≈ 0,055 USD |
| C — thực thi | `hue-rag-6a` | Claude Opus 5.5 | trực tiếp | báo cáo so sánh, nháp nhiều lượt, plan + runbook đo cuối, bảo mật C106, review S3, đo §1–§5 | `STATUS_C.md`; ≈ 0,095 USD |

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C lúc mở phiên sau: không việc đang chạy ⇒ kiểm nhanh ⇒ báo A ⇒ chờ.

## Quyền

- **Phiên 01/11 — HẾT HẠN cuối phiên** (như 31/10 + A tự commit / push không hỏi; ≤ 1 USD). Tiền phiên 01/11 ≈ **0,15 USD** paid (B ≈ 0,055 · C ≈ 0,095 · agent con A ≈ 0,001).
- **Thường trực:** A commit / push — **hỏi User trước** (luật chung của User), rồi A tự chạy; chỉ khi bị chặn / lỗi mới đưa `!` (I8, `WORKFLOW.md` §9.6); B / C không commit trừ khi việc ghi rõ; duyệt cho A =
  duyệt cho B / C; thư viện nhỏ cần cho việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage + tiền; code luôn `uv run`.
- **Tra web:** `scripts/tra_web_codex.sh` (đã rào 01/11 — chỉ thông tin công khai); **không bao giờ gọi `agy`**.
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
| `knowledge-base-hue/evaluation/final_2026-11-01/final_sealed.jsonl` | **bộ kín mới 40 câu — ĐÃ DÙNG** ở lượt đo cuối 01/11 (A / B / C chưa đọc nội dung); mẫu User `final_sealed_user_sample.md` | `7f97d4c10b2b` |
| `data/do_cuoi_2026-11-01/` | lượt đo cuối: runbook, tools, golden/ (analyze `13fccf9bab68`), an_toan/, ngay/, kin/ (B chạy, chỉ số đếm) | — |
| `data/so_sanh_phuong_an/` | nháp + review báo cáo so sánh phương án (R1 / R2), nháp thêm 01/11 | — |
| `data/s4_2026-11-01/` | đo S4 trên trình duyệt (`run_main.jsonl` `77c7a1b0ef16`) | — |

## Việc đang mở — luật chung khi sửa code / dữ liệu

- A commit + push `main` **trước** khi B / C sửa code; khai báo file trong `STATUS_<X>.md` trước khi sửa; skill `practical-project-coding`; test liệt kê file; report
  `<việc>_implementation.md`; review chéo (W32: ca dò khác cách + câu bất biến); plan có tiêu chí ghi trước ⇒ session khác review **trước** khi A duyệt sha (sha tính từ file).
- **Cổng ổn định:** (1) test file chạm; (2) `cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port <cổng trống>`: `/` 200, `/health` 5 / 5,
  1 câu trong kho + 1 câu ngoài kho (câu tự viết); đếm `chat_metrics` mới = số câu; grep câu hỏi trong log = 0; tắt server (TaskStop); (3) chạm tìm / chia đoạn: T1 giống byte; (4) đủ
  5 chỗ (`WORKFLOW.md` §6); (5) hook tự chạy.
- **Có lượt đo latency ⇒ session khác không chạy lượt trả phí / việc nặng CPU / Qdrant** (W31).
- Test cần key: `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan`, `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`,
  `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`.
- Đọc kho: **chỉ** `scripts/grep_kb.sh`; report tracked tả câu ở mức loại câu. Giờ trong file: chạy `date` trước; tin nhắn không cần giờ (W45 01/11) (S49). `rm` với biến: dùng `"${X:?}"/…` hoặc
  đường dẫn cố định (tầng an toàn chặn `$X/*`).

## Hồ sơ đã đóng (chỉ tra cứu)

- Streaming + lượt đo cuối Phase 1–8 (01/11): `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`.
- Phase 8.2 (User đóng 28/10): `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
- Đợt sửa kho 1 + 2, thước lỗi nặng, đo ngày hôm nay, Qwen3-8B: `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md` §7–§8.
- Tra web bằng Codex (31/10): `report_agent/2026-10-31_tra_web_codex/TONG_HOP.md`.
