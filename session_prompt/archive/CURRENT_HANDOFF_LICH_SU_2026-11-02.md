# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 10:36 02/11/2026 (A, **giao diện mới vào `main`** `ed8e6e8`; C118 review vòng 3). Trước: 09:53 02/11/2026 (A, **mở phiên 02/11**: quyền như 01/11; User duyệt gói npm; giao B121 giao diện mới + C118 spec Phase 9 song song). Trước: 16:32 01/11/2026 (A, **kết phiên chiều 01/11**: B0 xong ⇒ giữ 10; **User đóng Phase 8 14:29**; giao diện chốt hướng; mở nghiên cứu Phase 9). Trước: 14:30 01/11/2026. Trước: 13:36 01/11/2026 (A, **kết phiên 01/11**). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở. Lịch sử phiên 01/11 (mọi mục việc B / C, quyết định theo giờ, trạng thái review) dời
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

**Thứ tự việc phiên sau** (viết 15:26 01/11/2026, kết phiên chiều 01/11 — Phase 8 **đã đóng** 14:29; B0 xong ⇒ giữ 10; 4 nhánh đã xoá):
1. Mở A / B / C; `ListAgents`; **hỏi lại quyền phiên** (quyền chiều 01/11 hết hạn); kiểm Qdrant.
2. **Nghiên cứu Phase 9 — XONG bản 2** (16:15 01/11/2026): ChatGPT đã về + C117 kiểm 9 ý; thử Huế TRIPO xong (B119); báo cáo `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md` bản 2 (B120 review).
   Brainstorm đã chốt B1 = (b) + lịch (mục "Brainstorm Phase 9"). **B3 = (a) song song (User 16:28 01/11/2026):** song song (B code giao diện, C viết **một spec Phase 9** — an toàn + hỏi lại + nhớ ngắn +
   lịch trình nhỏ + thử câu nhiều nguồn, tiêu chí ghi trước — để User duyệt) — đầu phiên sau giao ngay. User "làm đi" (sau câu hỏi B3, trước 16:13) chỉ cho bản 2 + kết phiên. Nghiên cứu thêm: User nói "muốn nghiên cứu thêm cứ nói".
3. ~~Thử Huế TRIPO~~ — xong (B119; lặp lại có tiêu chí ghi trước nếu đưa vào luận văn).
4. **Code giao diện mới** (hướng đã chốt — mục B116): **User duyệt gói npm** (React, Vite, Tailwind, marked, DOMPurify, font) lúc giao; bước đầu dò CSP shadcn; một nhánh, review cả nhánh một lần;
   18 yêu cầu (`yeu_cau_cho_giao_dien_moi.md` + yêu cầu 18 trong `b116_so_sanh_giao_dien.md`). Thứ tự 2 ↔ 4: **song song** (User 16:28 01/11/2026). **02/11: giao B121 + C118** (mục dưới).

**Mã hay gặp:** T1 = kết quả tìm 158 câu (so "giống byte"); B0 = User đọc cặp câu trả lời mù làm mốc người; PA1 / PA3 = chữ hiện dần ↔ chỉ hiện tiến độ; D1–D5 / Q1 = câu quyết định
streaming (D5: xem lại PA3 nếu lợi < 0,5 s); Q3a = đo lại theo loại câu (01/11); F1–F4 / T1–T3 (plan đo) = sàn ngoài kho / bịa / lỗi kỹ thuật / lỗi trích dẫn và mức tụt Đủ / Đúng / từ chối nhầm; A1 / A2 = sàn bộ an toàn
(ngoài kho bị trả lời / nói sai điều kiện mới); `delta_matches_final` = cờ log "chữ ghép từ luồng = chữ cuối"; S / W / I = sự cố / đề xuất / dời luật trong `SO_CAI_TIEN_CACH_LAM.md`; CA / R = rủi ro trong
rà bảo mật C106; M-n / m-n = finding major / minor; Bxx / Cxx = mã việc A giao B / C.

## Câu hỏi cho User (hỏi mỗi lần một câu)

1. ~~**Quyền phiên.**~~ **XONG 09:48 02/11/2026** — User chọn như 01/11 (mục Quyền).
2. ~~**Xoá 4 nhánh đã merge**~~ **XONG 15:21 01/11/2026** (User `!` xoá local + origin). Cũ: (`s1-loi-chung`, `s3-giao-dien`, `dg-cost-usd`, `streaming-final` — mọi commit đã có trong `main` qua merge `a80e12d`; không còn gì chỉ nằm trên nhánh) — User `!`
   (`git branch -d …` + `git push origin --delete …`). Nhánh cũ khác: `git branch -a` lúc mở phiên.
3. **Rà bảo mật C106 còn chờ User** (`report_agent/2026-10-31_streaming_spec/c106_bao_mat_dong_goi.md` bản 2): R4 xoá / cắt 22 dòng log cũ (08–10/2026) chứa nguyên câu hỏi thử trong `backend/logs/application.log`
   (gitignore); CA2 (`uv run *` / `python3 *` tự duyệt — khuyên giữ); R1 kiểm `Host` + giới hạn lượt khi deploy; R11 gỡ `gradio` không dùng (User 24/10: chỉ gỡ khi xung đột) — các mục deploy để lúc deploy.
4. **Sổ cải tiến chờ User:** W35 (kiểm điều khoản trước công cụ / tài khoản ngoài mới), W42 (hook cảnh báo "dự án khác"), W43 (script kiểm báo cáo khâu khớp hiện trạng). W44 User không chọn 01/11.
5. ~~`báo cáo nghiên cứu github.txt`~~ **dời vào `data/nghien_cuu_phase_9_2026-11-01/`** (User 16:28 01/11/2026). Còn (không gấp): 4 worktree AGY cũ (`~/.gemini/antigravity-cli/…`, nhánh `subagent-Monuments-Reviewer-*`): giữ hay gỡ (User `!`)?
   Xoá sao lưu kho đợt 1 + 2 khi đóng gói?

## Câu hỏi A còn nợ (không cần User)

- Ghi chú `delta_matches_final` vào spec streaming §4.6 nếu mở lại spec (đã ghi ở TONG_HOP "Giới hạn khi đóng"). 6 minor review cả nhánh ⇒ giới hạn (không sửa — giao diện làm lại).
- Bảng sổ cải tiến: S41–S44 thiếu 1 cột từ trước (B 01/11) — sửa khi tiện. W39 hạn 07/11 (0 buổi D ⇒ đề xuất gỡ W4 + W39).
- Log `FileHandler` không xoay vòng — xem lại khi deploy. Hạn mức tín dụng phía OpenAI cho key — chưa kiểm.

## Session

| Vai | Terminal (02/11, mở 09:46) | Agent | Liên lạc | Phiên 02/11 | Trạng thái |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-7e` | Claude Opus 5.5 | trực tiếp | điều phối; giao B121 / C118 | `STATUS_A.md` |
| B — thực thi | `hue-rag-d6` | Claude Opus 5.5 | trực tiếp | B121 giao diện mới | `STATUS_B.md` |
| C — thực thi | `hue-rag-29` | Claude Opus 5.5 | trực tiếp | C118 spec Phase 9 | `STATUS_C.md` |

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C lúc mở phiên sau: không việc đang chạy ⇒ kiểm nhanh ⇒ báo A ⇒ chờ.

## Quyền

- **Phiên 02/11 (User chọn, A ghi nhận 09:48 02/11/2026):** như 01/11 — A tự điều phối B / C + tự thử trong luật; ≤ 1 USD; A tự commit / push không hỏi từng lần; B / C push nhánh riêng. Hết hạn cuối phiên.
  **Gói npm (User duyệt, A ghi nhận 09:53 02/11/2026):** `react`, `react-dom`, `vite`, `@vitejs/plugin-react`, `tailwindcss`, `@tailwindcss/vite`, `marked`, `dompurify`, `@fontsource/be-vietnam-pro`
  + shadcn / Radix **chỉ** linh kiện dò CSP trên bản build ra 0 vi phạm (vi phạm ⇒ bỏ, tự viết; không nới CSP). Gói ngoài danh sách (kể cả phụ thuộc trực tiếp của shadcn như tiện ích class) ⇒ B hỏi A; A tự duyệt nếu nhỏ, phổ biến (§4), báo User sau.
- **Phiên 01/11 chiều — HẾT HẠN** (User, A ghi nhận 14:00 01/11/2026; mở 13:51, kết ~16:30): như phiên sáng 01/11 — A tự điều phối B / C + tự thử trong luật; ≤ 1 USD; A tự commit / push không hỏi từng lần; B / C push nhánh riêng. Hết hạn cuối phiên.
- **Phiên 01/11 sáng — HẾT HẠN cuối phiên** (như 31/10 + A tự commit / push không hỏi; ≤ 1 USD). Tiền phiên 01/11 ≈ **0,15 USD** paid (B ≈ 0,055 · C ≈ 0,095 · agent con A ≈ 0,001).
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

## Phase 9 đổi hướng: trợ lý agent có công cụ (User, A ghi nhận 11:21 02/11/2026)

- **User (sau Q1–Q5):** Phase 9 đi hướng **trợ lý / agent / agentic cho mọi câu** — model tự quyết gọi công cụ (tìm kho, ngày hôm nay, tra web khi kho không có…); RAG Phase 1–8 thành **công cụ** để agent gọi.
  Lý do User: "lên trợ lý mà không có gì khác RAG mức 1 thì gọi thẳng LLM cần gì trợ lý". User có `SERPER_API_KEY` trong `.env` (**không đọc / in**; chưa dùng — kiểm điều khoản Serper trước lượt đầu).
  **A quyết framework:** giữ **OpenAI Agents SDK** đang dùng (`openai-agents` **0.19.4** cài trong `.venv` — `pyproject.toml` ghi `>=0.18.3`; hôm nay `Agent` không công cụ, `max_turns=1` — `backend/llm/generator_openai_full_corpus.py:133,185–188`); không LangChain / DeepAgents (thêm hệ thư viện, chưa cần).
- **Spec C118 bản 5 `03cb538cf00c` TẠM GIỮ** (Q1–Q5 User đã chọn vẫn dùng — thành công cụ / luật của agent). Viết lại sau nghiên cứu.
- **Nghiên cứu trước (User "làm đi" 11:21 02/11/2026):** (1) A — 3 sub-agent chỉ đọc khoá AI FDE (tóm tắt ver4 + khung `NGUYEN_TAC_FDE.md` [agent] + code tham khảo khoá) ⇒ `data/nghien_cuu_phase_9_2026-11-01/agent/a_sa{1,2,3}.md`;
  (2) **B122** (dưới) tra web; (3) yêu cầu ChatGPT web (A viết, User gửi); (4) A tổng hợp ⇒ `BAO_CAO_NGHIEN_CUU_PHASE_9.md` bản 3 + câu hỏi User (trần tiền / tốc độ cho agent, cắt phần nào) ⇒ C viết lại spec.

- **Quyết định sau nghiên cứu (User, A ghi nhận 13:29 02/11/2026):**
  - **Framework: giữ OpenAI Agents SDK + mẫu của khoá** (User: chọn nếu không cần người duyệt; A: không cần người duyệt lúc chạy — không hành động ghi ra ngoài; người duyệt chỉ ở việc cập nhật kho từ web, ngoài chatbot).
    Mẫu khoá: trần lượt, từng công cụ một, lời từ chối về model, nhớ chỉ hỏi + đáp (không kết quả công cụ), soát chữ web, test ranh giới, thẻ công cụ trên giao diện, tracing tại máy (tắt gửi nội dung).
  - **Cổng vào = agent định tuyến, đầu ra có cấu trúc** (ý User): định tuyến ⇒ model trò chuyện (chào hỏi, không tìm kho / công cụ) / agent trợ lý Huế (có công cụ) / ngoài phạm vi / khẩn cấp (Q1: thử 10 câu trước).
  - **Câu tìm kho: User cho thử nghiệm + so sánh** nhiều phương án (định tuyến viết câu tìm ↔ trợ lý tự viết ↔ viết lại + chia thành nhiều câu nhỏ…), chọn theo số đo, tiêu chí ghi trước (`run-experiment`).
  - **Nhớ hội thoại là bắt buộc** (User: vd người dùng đã nêu tên thì các lượt sau phải nhớ) ⇒ Q5 cũ "3 câu hỏi gần nhất" **không đủ** — cần lịch sử hỏi + đáp trong cuộc trò chuyện (tên là dữ liệu cá nhân: không log, xoá được). Nhớ **giữa các lần mở trang** (dài hạn): chưa chốt.
  - **Tiền / tốc độ (User, A ghi nhận 13:36 02/11/2026):** "chạy trước đi" — **chất lượng ổn định trước, tối ưu tốc độ / chi phí sau** (đúng `Session_Prompt.md` §7). Sàn 0,0005 USD / câu + p50 3 / p95 5 s ⇒ **theo dõi, không chặn** ở Phase 9 cho tới khi chất lượng ổn;
    **bắt buộc log tiền** mỗi lần gọi LLM / mỗi lần Serper / mỗi câu / mỗi tuyến (định tuyến, trò chuyện, trợ lý, web) + latency. Trần tiền phiên (≤ 1 USD) và trần cả Phase vẫn là giới hạn cứng.
  - **Bỏ sót của A:** `guides/phase_9_agentic_rag_roadmap.md` (Codex viết, User duyệt hướng 13/08, 25/08, 01/10: rule router ⇒ LLM hiểu câu hỏi có cấu trúc ⇒ RAG-first + cổng đủ bằng chứng ⇒ web có provenance; lịch trình = model trích điều kiện + code xếp) **không** được giao đọc cho C118 / sub-agent — User nhắc. Dùng làm tư liệu (phần "bộ điều khiển Python cố định, không agent" đã lỗi thời).

## C120 — viết lại spec Phase 9 hướng agent (giao 13:36 02/11/2026 qua tin nhắn; A ghi mục 13:43 02/11/2026)

- **Đầu vào:** mục "Quyết định sau nghiên cứu" ở trên; `a_sa{1,2,3}.md`; kết quả ChatGPT 02/11; `guides/phase_9_agentic_rag_roadmap.md`; B122 khi xong. Bản 5 `03cb538cf00c` giữ trong git (`077e3cb`).
- **Trạng thái:** bản 6 xong (C) — `fbb2853aa90c`, 383 dòng; **chờ review** (A giao sub-agent ngữ cảnh mới). **Bản 7 (C, 13:57 02/11/2026) — sửa theo review v6 vòng 1 (10 major + 9 minor đều sửa, 0 phản biện): `37e306ef40f7`** (447 dòng); `tra_web` thành cổng code sau câu trả lời kho; B2 tách B2a / B2b; tiền ước ≈ 1,2 USD; câu hỏi User P1–P4. **Bản 8 (C, 14:17 02/11/2026) — sửa theo review vòng 2 (M11–M13 + m10–m16; M13 theo User chọn 14:12): `82127aabcb5b`** (450 dòng); thêm P5 (điều khoản Serper chưa đủ — B122). **Bản 9 (C, 14:45 02/11/2026) — chỉ ghi lựa chọn User P1–P5 + A quyết bộ hồi quy + m17 / m18: `169c2dd5f86a`** (415 dòng), chờ User duyệt sha. **XONG — User DUYỆT bản 9 `169c2dd5f86a`** (C ghi 14:49 02/11/2026).
- **Ý A giao trong tin nhắn 13:36 (ghi lại theo m5 review):** S-OOS định nghĩa lại khi có web ("0 câu không có bằng chứng hợp lệ bị trả lời khẳng định", giữ chỉ số cũ cho đường chỉ-kho); 6 rào `a_sa2.md` §3 trước khi bật web; Serper chưa gọi tới khi đọc xong ToS;
  cuối Phase so RAG cũ ↔ agent trên cùng bộ câu; mỗi công cụ một bậc giữ / gỡ; ≤ ~450 dòng; ≤ 5 câu hỏi User.
- **Review bản 6 vòng 1 (A ghi 13:53 02/11/2026):** `changes_requested` — 0 blocker / 10 major / 9 minor (`…_review_v6.md`, sub-agent ngữ cảnh mới). A kiểm M1 (luật kết luận B7 luôn thoả) + M3 (lịch sử lưu mục "Từ web" ⇒ chữ web quay lại prompt): đúng. C sửa, ưu tiên cắt hơn thêm luật; C121 tạm dừng. Câu hỏi User: nhớ dài hạn · cách hiện web · giới hạn tên miền · trần Phase (C khuyên 1,2 USD) + câu "kết quả web cố định qua model thật có hợp §6 không mock".
- **Bản 7 `37e306ef40f7`** (447 dòng; C sửa 10 major + 9 minor) ⇒ review vòng 2 đang chạy (A gửi 13:59 02/11/2026). Lệch cần User chọn: `tra_web` **không còn là công cụ model** — code gọi Serper khi trợ lý trả câu từ chối chuẩn (lý do M2 / M3: cổng code thấy được; web không lái công cụ / lượt sau). C121 làm tiếp.
- **B rảnh từ 13:59 02/11/2026:** B123 xong (0,00023 USD); việc tiếp của B (bậc B0 / B1) cần spec duyệt.
- **A quyết (14:02 02/11/2026, kỹ thuật trong phạm vi):** **giữ `openai-agents` 0.19.4** cho Phase 9 (B123: 3 việc spec cần làm được; C121: 0.24.0 kéo `openai` 3.x + HTTPX2, test không khoá giống nhau, đường mạng thật NOT RUN). Nâng = bước riêng khi một bậc cần. Venv tạm của worktree C121 (lệch §10) do brief A — đã gỡ.
- **Review bản 7 vòng 2 (A ghi 14:12 02/11/2026):** `changes_requested` — 19 finding vòng 1 đóng; còn M11 (B7 sinh lại RAG 1–8 cùng tuần), M12 (B4 / B5 khi B2b bị gỡ), M13 (3 chỗ bớt tự chủ, chỉ ghi 1) + m10–m16.
  **User chọn M13 (A ghi nhận 14:12 02/11/2026):** code giữ 3 chỗ — ngày luôn vào lời dặn; web do code gọi khi kho từ chối; **lần tìm đầu là thí nghiệm** giữ cả "code tìm trước" ↔ "trợ lý tự quyết có tìm không" (V2 thuần), chọn theo số. User thêm: **hiện chỉ vài công cụ; khi hệ thống ổn định thì nghiên cứu, tạo thêm công cụ mới** (ghi vào spec phần sau Phase / mở rộng).
- **Bản 8 `82127aabcb5b` — review vòng 3: `ready_for_user_confirmation`** (0 blocker / 0 major; m17 A/A ở B2a nếu giữ V2; m18 sửa phương án câu hỏi).
- **User chọn P1–P5 (A ghi nhận 14:42 02/11/2026):** P1 (a) chỉ nhớ trong cuộc trò chuyện (server RAM, 30 phút) · P2 (a) model viết mục "Từ web" [w n], code kiểm mã + dựng link · P3 (a) không giới hạn tên miền + câu an toàn theo kho + nhãn ·
  P4 (a) **trần Phase 9 = 2,0 USD** (mỗi phiên ≤ 1 USD) · P5 **dùng Serper luôn, không email** (User chấp nhận rủi ro điều khoản B2B chưa rõ — ghi vào spec; vẫn theo thứ tự bậc B6 sau rào code + cờ).
  **Bỏ bộ kết quả web xấu cố định + model soát chữ web + đo hai chiều riêng cho web** (User: "over-engineer quá" — người dùng chỉ hỏi du lịch / thời tiết thì tra thôi); giữ rào dạng code (gọi model riêng không công cụ / lịch sử, link do code, nhãn, câu an toàn theo kho); đo web chỉ trên Serper thật.
  **A quyết bộ hồi quy** (User hỏi "có cần đủ 176 + 32 không"): đủ 176 + 32 ở B1, B2, B7 và ở bậc nào sửa lời dặn chung / lõi chung; B3–B6: bộ riêng + 32 an toàn + mẫu Golden cố định ~30 câu.
  ⇒ C ghi vào spec bản 9 (chỉ các chỗ này + m17 / m18) ⇒ A đọc diff ⇒ User duyệt sha.
- **SPEC PHASE 9 DUYỆT — bản 9 sha `169c2dd5f86a`** (A tính từ file; User duyệt, A ghi nhận 14:48 02/11/2026). Sửa sau duyệt = bản mới, duyệt lại phần đổi. Phiên sau: giao **B0** (plan nhỏ ⇒ review ⇒ A duyệt sha).

## C121 — thử nâng OpenAI Agents SDK 0.19.4 ⇒ 0.24.0 (giao 13:47 02/11/2026; việc trong lúc chờ review spec)

- **Vì sao:** spec bản 6 để "nâng SDK chốt lúc tới bậc"; bản mới có `tool_output_guardrails`, `agents.testing`, sửa streaming + tool-use (0.23), nhưng từ 0.21 đổi sang `openai>=3,<4` (HTTPX2) ⇒ cần biết **trước** B0 có vỡ gì không.
- **Làm (0 USD, không gọi API):** worktree `/tmp/c_sdk024` từ `main`; ở đó nâng `openai-agents==0.24.0` (kéo `openai` 3.x) bằng `uv` — **chỉ trong worktree**, không sửa `pyproject.toml` / `uv.lock` của working tree chung;
  (1) đọc release notes 0.20 ⇒ 0.24 (GitHub, WebFetch), liệt kê thay đổi chạm cách repo dùng SDK (`backend/llm/generator_openai_full_corpus.py`: `Agent`, `Runner.run`, `Runner.run_streamed`, `max_turns`, `ModelSettings`, `Reasoning`, `AgentsException`; `backend/api/routes/chat.py`);
  (2) chạy test không cần key liên quan generator / API / streaming (liệt kê file, `HF_HUB_OFFLINE=1`) trên bản nâng ↔ bản hiện tại; (3) `import` + dựng generator không gọi mạng.
- **Không làm:** gọi OpenAI / Serper; sửa code `main`; merge. Gỡ worktree khi xong (rm bị chặn ⇒ nhờ User `!`).
- **Đầu ra:** `data/nghien_cuu_phase_9_2026-11-01/agent/c121_sdk_024.md` — bảng thay đổi chạm repo (nguồn release + `file:dòng`), test trước ↔ sau ([Chạy]), khuyên nâng ngay ở B0 / giữ 0.19.4 kèm lý do. Xong ⇒ nhắn A. Spec review về thì ưu tiên sửa spec.
- **Trạng thái:** giao 13:47 02/11/2026. **Xong (C, 14:02 02/11/2026):** `c121_sdk_024.md` `3bc2c212cc69` — test 8 file trước ↔ sau giống nhau (68 passed + cùng 4 lỗi cần khoá); dò API giống nhau; nâng kéo `openai` 2.53 ⇒ 3.42 + HTTPX2 (đường mạng thật chưa chạy). **Khuyên giữ 0.19.4 ở B0**, nâng thành bước riêng khi một bậc cần (`agents.testing`, sửa stream + guardrail). Worktree + venv tạm đã gỡ; 0 USD.

## B123 — dò OpenAI Agents SDK 0.19.4 cho 3 việc spec cần (giao 13:52 02/11/2026; việc trong lúc chờ review spec)

- **Vì sao:** spec bản 6 cần (1) **log USD + ms mỗi lần gọi model** trong một lượt agent nhiều lần gọi (User bắt buộc); (2) **streaming khi có công cụ**: chỉ đẩy chữ của câu trả lời cuối, không đẩy lượt gọi công cụ (B122: SDK không tách sẵn); (3) **định tuyến đầu ra có cấu trúc** (`output_type` Pydantic, strict).
- **Làm:** đọc mã SDK đang cài (`.venv/…/agents/`, bản 0.19.4) + tài liệu chính thức: lấy usage từng lần gọi ở đâu (`RunResult.raw_responses`, `context_wrapper.usage`, hooks…), sự kiện stream nào báo "đang gọi công cụ" ↔ "chữ trả lời cuối", `output_type` + streaming có đi cùng nhau không.
  Probe thật **nhỏ** được phép: ≤ 0,005 USD, câu tự viết (không kho thật / Golden / câu kín), một công cụ giả trả chuỗi cố định chỉ để xem thứ tự sự kiện (đây là probe hành vi thư viện — W36, không phải bằng chứng chất lượng); script tạm ở `/tmp`, giữ bản dùng lại ở `data/nghien_cuu_phase_9_2026-11-01/agent/b123/`.
- **Không làm:** sửa code `main`; nâng SDK (C121 làm); gọi Serper.
- **Đầu ra:** `data/nghien_cuu_phase_9_2026-11-01/agent/b123_sdk_probe.md` — mỗi việc: cách làm trên 0.19.4 (`file:dòng` SDK), [Chạy] / [Đọc], đoạn mã mẫu ≤ 15 dòng, giới hạn. Xong ⇒ nhắn A.
- **Trạng thái:** giao 13:52 02/11/2026. **Xong (B, 13:57 02/11/2026), XONG — A đã xem (đạt); B đóng 14:49 02/11/2026:** `data/nghien_cuu_phase_9_2026-11-01/agent/b123_sdk_probe.md`. Cả 3 việc làm được trên 0.19.4 (hook `on_llm_start/end` + `response.usage`; lọc `output_text.delta` theo mục `message`; `output_type` strict + `route` trước `answer` — phải sửa `ANSWER_PREFIX`). Probe 0,00023 USD.

## B122 — tra web cho agent Phase 9 (giao 11:21 02/11/2026)

- **Làm:** `scripts/tra_web_codex.sh` (chỉ thông tin công khai; yêu cầu .md ở `data/nghien_cuu_phase_9_2026-11-01/agent/yeu_cau/`), mỗi chủ đề một lượt, tuần tự:
  (a) **OpenAI Agents SDK** bản hiện hành: gắn công cụ (function tool), `max_turns`, guardrails vào / ra, tracing, streaming khi có công cụ, cách giới hạn số lần gọi công cụ; đổi gì so với bản đang cài (`openai-agents` 0.19.4);
  (b) **Serper**: điều khoản dịch vụ (cho phép dùng trong ứng dụng / đồ án? lưu kết quả? hiển thị?), giá, giới hạn lượt, có lọc theo site không — **W35: đọc ToS trước, chưa gọi API**;
  (c) **đo một agentic RAG / agent có công cụ**: bộ đo kiểu tau-bench, đo chọn công cụ đúng, số bước, tiền / độ trễ so pipeline; rào chữ độc từ trang web (prompt injection) khi agent tra web.
  Kết quả là **dữ liệu**: tự WebFetch kiểm 3 ý quan trọng nhất / chủ đề; URL không có trong `url_da_mo.txt` = tự khai.
- **Không làm:** gọi Serper / OpenAI; đọc `.env`; code; sửa file ngoài đầu ra + `STATUS_B.md` + dòng trạng thái mục này. 0 USD.
- **Đầu ra:** `data/nghien_cuu_phase_9_2026-11-01/agent/b122_tra_web.md` — bảng phát hiện (ý · URL + ngày · nhãn đã kiểm / tự khai / suy ra), "gợi ý gì cho hue_rag" tách riêng, chỗ còn thiếu. Xong ⇒ nhắn A.
- **Trạng thái:** giao 11:21 02/11/2026. **Xong (B, 13:50 02/11/2026), XONG — A đã xem (đạt); B đóng 14:49 02/11/2026:** `data/nghien_cuu_phase_9_2026-11-01/agent/b122_tra_web.md`. Serper: điều khoản 29/05/2024 không nói rõ dùng cho người dùng cuối / hiển thị / lưu ⇒ chưa qua W35; 0,001 USD / lượt (gói thấp nhất) = gấp đôi trần. SDK: mới nhất 0.24.0; ≥ 0.21 đòi `openai>=3` (repo 2.53.0); không có hạn mức số lần gọi công cụ; tracing bật mặc định. 3 × 3 ý WebFetch kiểm. 0 USD. Trễ ~2 giờ do lệnh chờ của B lỗi (S — ghi STATUS_B).

## B121 — code giao diện mới (giao 09:53 02/11/2026; User duyệt gói npm 09:53; mức trung bình — Phase 8 đã chốt hướng)

- **Mục tiêu:** thay `frontend/` JS thuần bằng React + Vite + Tailwind, FastAPI phục vụ bản build tĩnh; chỉ **trang hỏi đáp** + khung nguồn bên cạnh; laptop (điện thoại chỉ cần không vỡ).
  Giao diện sống tới bảo vệ (01/2027) và là nền nâng cấp Phase 9 ⇒ làm sạch, dễ đọc; **không** làm trước tính năng Phase 9 (nhiều lượt, trang số đo…).
- **Đọc:** `report_agent/2026-11-01_giao_dien_moi/b116_so_sanh_giao_dien.md` (full — quyết định, bố cục, 12 token màu, font, 6 trạng thái, mục dò CSP);
  `report_agent/2026-10-31_streaming_spec/yeu_cau_cho_giao_dien_moi.md` (full — 17 yêu cầu); `frontend/` + `backend/api/app.py` (phục vụ tĩnh + CSP, dòng ~28–40, ~155–170) + `backend/api/chat.py` (luồng SSE) + `backend/tests/test_static_ui.py` (targeted).
- **Làm:**
  1. Nhánh `giao-dien-moi` từ `main` `411bbc5`, trong **worktree riêng** `/tmp/b_giao_dien` (C viết tài liệu trên working tree chung; bẫy worktree `Project_Status.md` §8: `uv run --project /home/minhhieu/hue_rag`, gỡ symlink khi xong, push từ working tree chung).
  2. **Bước đầu: dò CSP** shadcn / Radix (mục "Bước đầu khi code" B116) trên bản build với CSP thật của `app.py`; ghi linh kiện nào đạt / vi phạm.
  3. Code trang: 17 yêu cầu + **18** (link nguồn bắt cả `[n]` lẫn `[Nguồn n]`; nguồn = số nhỏ nâng lên bấm được + danh sách khung bên, giữ `[n]` ở tầng máy) + **19** (nhãn "Trợ lý AI, câu trả lời dựa trên kho, có thể sai" — Luật AI 134/2025 Đ.11.1, C117); streaming giữ **PA1**.
  4. FastAPI phục vụ bản build (giữ đường `/static`, CSP mọi trang HTML **không nới**). `node_modules/`, bản build: **không commit** (gitignore) trừ khi B có lý do rõ — báo A; lockfile commit; khoá phiên bản. Lệnh build ghi vào guide.
  5. Sửa / thay `test_static_ui.py` theo giao diện mới (test bảo vệ CSP + phục vụ tĩnh; không đặt mục tiêu số test).
- **Kiểm:** cổng ổn định (mục "Luật chung" dưới) trên bản build; Playwright (`uv run`, chromium headless) mở trang thật: 0 vi phạm CSP trong console, 1 câu trong kho chữ hiện dần + link nguồn bấm được, 1 câu ngoài kho từ chối, 1 đường lỗi thật (vd câu > 500 ký tự ⇒ server trả lỗi; **không** dựng lỗi giả — `Session_Prompt.md` §8) — câu tự viết, không Golden / câu kín.
- **Không làm:** đổi API / thân SSE; nới CSP / thêm nonce; CDN / Google Fonts; gói ngoài danh sách đã duyệt (hỏi A); trang khác ngoài hỏi đáp; tối ưu hiệu năng phòng xa.
- **Tiền:** chỉ cổng ổn định + Playwright, trần **0,02 USD**. **Dừng:** phải nới CSP / đổi API ⇒ dừng, báo A.
- **Đầu ra:** nhánh `giao-dien-moi` (push origin); `report_agent/2026-11-02_giao_dien_moi_code/b121_giao_dien_implementation.md` (kết quả dò CSP, khớp 19 yêu cầu từng dòng [Chạy] / [Code, chưa chạy], ảnh chụp Playwright để `data/giao_dien_moi_2026-11-01/`). Review **một lần cả nhánh** (A chọn người khi B xong). A merge + 5 chỗ báo cáo.
- **Trạng thái:** giao 09:53 02/11/2026. **Dò CSP xong** (B báo, A ghi 10:00 02/11/2026): mốc React + Tailwind 0 vi phạm; Radix Collapsible / Tooltip / Popover 0; Dialog 1 + ScrollArea 1 (chèn `<style>` lúc chạy); 0 request ra ngoài; bundle 0 `eval`. **Xong, chờ review cả nhánh (B, 10:19 02/11/2026):** `giao-dien-moi` `11a0f3a` (đã push); report `report_agent/2026-11-02_giao_dien_moi_code/b121_giao_dien_implementation.md` (trên nhánh). 0 gói Radix; server thật + Playwright: 0 vi phạm CSP luồng thường, 0 request ra ngoài, link chỉ bật sau `sources`, `client_disconnected` khi rời trang; 19 yêu cầu từng dòng [Chạy] / [Tự dựng]; < 0,002 USD. A cần: thêm `cd frontend && npm ci && npm run build` vào `session_prompt/chạy_môi_trường.md` (governance).
  **A đồng ý: 0 gói Radix / shadcn** (thẻ HTML gốc + Tailwind; ít gói hơn danh sách duyệt); `.npmrc` `ignore-scripts` + `save-exact` + `before=2026-10-19` commit vào repo. Phase 9 cần hộp thoại ⇒ tự viết.
  **ĐÓNG (10:36 02/11/2026, A):** m-1 B sửa `deaa605` (A đọc diff: đạt); **merge `ed8e6e8` vào `main`**; A build trên `main` + `test_static_ui.py` 3 passed + `/health` 5 / 5, `/` 200 (0 câu hỏi, 0 USD); 5 chỗ báo cáo + `chạy_môi_trường.md` + bẫy §8 (m-2). Worktree B đã gỡ. Nhánh `giao-dien-moi` giữ — A đề xuất xoá lúc kết phiên (User `!`). **B rảnh: chờ spec Phase 9 duyệt** (phần đầu Phase 9 cần spec).

## C119 — review cả nhánh `giao-dien-moi` (B121) (giao 10:19 02/11/2026)

- **Mục tiêu:** review **một lần cả nhánh** `origin/giao-dien-moi` `11a0f3a` (19 file, +2.236 / −523) theo skill `risk-gated-agent-review`; kết luận `ready_for_user_confirmation` / `changes_requested`.
- **Đọc:** report `report_agent/2026-11-02_giao_dien_moi_code/b121_giao_dien_implementation.md` (trên nhánh — mục "Căn cứ để review" là chỉ mục, không tự chứng minh PASS); exact diff `git diff main...origin/giao-dien-moi`;
  `yeu_cau_cho_giao_dien_moi.md` (17 yêu cầu) + B116 (yêu cầu 18) + mục B121 (yêu cầu 19, gói duyệt, `.npmrc`). Không đọc `STATUS_B.md`.
- **Kiểm theo rủi ro:** CSP không nới (`app.py`), lọc HTML đúng allowlist 25 thẻ / 4 thuộc tính, không CDN, gói đúng danh sách + lockfile + `.npmrc`; `node_modules/` / bản build không lọt commit; link nguồn `[n]` / `[Nguồn n]`; luồng lỗi / đứt xoá hết;
  độ phức tạp tương xứng (một trang hỏi đáp). Chạy lại phần rủi ro cần: build từ lockfile sạch (`npm ci` trong worktree / bản sao của C, **không** dùng `/tmp/b_giao_dien`), test file chạm, cổng ổn định 1 câu trong kho + 1 ngoài kho, Playwright 0 vi phạm CSP — ca dò khác cách B (W32).
- **Không làm:** sửa code của B (finding ⇒ B sửa); paid ngoài cổng ổn định; Golden / câu kín. **Tiền:** trần 0,01 USD.
- **Đầu ra:** `report_agent/2026-11-02_giao_dien_moi_code/b121_review.md` (`TEMPLATE_REVIEW.md`) + nhắn A. Spec C118 vòng 2 về ⇒ C xen sửa được (không chồng file).
- **Trạng thái:** giao 10:19 02/11/2026. **Review xong (C, 10:27 02/11/2026): ready_for_user_confirmation** — 0 blocker / 0 major / 2 minor (m-1 lỗi mạng / 502 / JSON hỏng hiện chữ kỹ thuật tiếng Anh — có từ bản cũ; m-2 việc A lúc merge: báo cáo User trỏ `app.py:141–146`, `chạy_môi_trường.md`, bẫy test cần build). `b121_review.md` (untracked). ≈ 0,0006 USD; server 8823 tắt; worktree `/tmp/c119` gỡ.
  **ĐÓNG (10:36 02/11/2026, A):** m-1 sửa + merge `ed8e6e8`; m-2 A làm.

## C118 — spec Phase 9 (giao 09:53 02/11/2026; User chốt hướng 16:01–16:28 01/11/2026; mức cao ⇒ một spec, User duyệt một lần)

- **Mục tiêu:** **một** tài liệu thiết kế Phase 9 để User duyệt: "trợ lý di sản Huế đáng tin" — H4 thông tin theo ngày + chặn câu an toàn trước model · H2 hỏi lại (danh sách trường trong code) · H3 nhớ ngắn 3–5 lượt ·
  lịch trình gợi ý nhỏ (thứ tự điểm theo khu vực, có nguồn; không giờ / giá chính xác; không đặt chỗ) · H1 câu nhiều nguồn (thử 1 lần; không vượt nhiễu ⇒ kết quả âm, dừng — chỗ cắt đầu tiên).
  Không: agent tổng quát, đặt chỗ, giọng nói / ảnh / nhiều ngôn ngữ. Đóng code tạm ~20/12/2026; bảo vệ 04–10/01/2027.
- **Đọc:** `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md` (full); mục "Brainstorm Phase 9" ở dưới (full); `Project_Status.md` §1 "Mục tiêu sản phẩm" + thứ tự lỗi (targeted);
  `data/nghien_cuu_phase_9_2026-11-01/tripo/b119_kham_pha.md` + `c117_kiem_chatgpt.md` (targeted — câu từ chối nhầm 2 ý, câu theo ngày); `docs/superpowers/specs/2026-11-01-multi-turn-design.md` + `data/tinh_nang_moi_2026-10-27/c91_phuong_an_nhieu_luot.md`
  (tư liệu H3 — chỉ là ý cũ, xét lại); `report_agent/2026-10-31_streaming_spec/q3a_theo_loai_cau_implementation.md` (câu nhiều nguồn); skill `agent-design-review`, `agent-security-review`, `run-experiment`, `propose-options`; code (targeted, ghi `file:dòng` cho mọi khẳng định về hệ thống).
- **Làm:** spec `docs/superpowers/specs/2026-11-02-phase-9-design.md`, gồm: mục tiêu + phạm vi + không làm; **thứ tự + mốc ngày** tới 20/12 (A đề xuất: H4 ⇒ H2 ⇒ H3 ⇒ lịch trình ⇒ H1 — C được đề xuất khác kèm lý do);
  mỗi phần: vấn đề quan sát được (số, nguồn), cách làm **nhỏ nhất** (code ↔ model chia việc; có cần "agent" không — theo `agent-design-review`), bộ đo + cỡ mẫu + ai viết câu (mới, tự nhiên; phần kín nếu cần),
  **tiêu chí ghi trước** (sàn không phạm: 0 ngoài kho bị trả lời, bộ an toàn, Golden không làm hỏng; chỉ số quyết; mức tụt cho phép; luật cắt khi trễ), tiền ước; rủi ro bảo mật mỗi phần (`agent-security-review`: chữ người dùng là dữ liệu, lịch sử hội thoại, egress);
  đầu file mục **"Căn cứ để review"** (2–4 file + mục cần đọc, `WORKFLOW.md` §9.1); cuối file **câu hỏi cho User** (mỗi câu có phương án + hệ quả, theo `propose-options`).
- **Mức công (S64 / proportional-effort):** spec gọn — chi tiết code để plan nhỏ của từng phần khi tới lượt; không thiết kế trước như đã biết kết quả phần trước (H2 phụ thuộc kết quả H4 thì ghi "chốt lúc tới lượt").
- **Không làm:** code; mở câu kín / đọc nhóm `test` theo từng câu; grep thẳng kho (chỉ `scripts/grep_kb.sh`); paid API; sửa file ngoài spec + `STATUS_C.md` + mục C118 này. Tra web khi cần: `scripts/tra_web_codex.sh` (chỉ thông tin công khai).
- **Tiền:** 0 USD. **Dừng:** thấy hướng đã chốt mâu thuẫn bằng chứng (vd một phần không khả thi trước 20/12) ⇒ ghi vào spec + nhắn A, không tự đổi phạm vi.
- **Đầu ra:** spec bản 1 + `sha256sum | cut -c1-12` báo A. Review: A chọn session khác chỉ dựa trên "Căn cứ để review" ⇒ User duyệt sha.
- **Trạng thái:** giao 09:53 02/11/2026. **Bản 1 xong (C, 10:02 02/11/2026) — chờ review:** `docs/superpowers/specs/2026-11-02-phase-9-design.md` `e5be02400646` (351 dòng; quét trùng 0; 0 USD). Lệch đề xuất A: H1 bậc 1 (tầng tìm, 0 USD) lên tuần 1 — Q1; H4b chỉ làm sau phép thử 10 câu — Q2; H3 mang đoạn 1 lượt + 3 câu hỏi — Q4. **Bản 2 (C, 10:18 02/11/2026) — sửa theo review vòng 1 (4 major + 8 minor đều sửa, 0 phản biện), chờ người review kiểm phần sửa:** `d819918c2f2e` (557 dòng; quét trùng 0); thêm H4c (năm nguồn trên thẻ nguồn), H1b (câu hai ý thiếu một ý); câu hỏi Q1–Q8. **Bản 3 (C, 10:32 02/11/2026) — sửa theo review vòng 2 (N1 major + N2–N5 đều sửa, 0 phản biện), chờ kiểm phần sửa:** `7c67656f0ff8` (507 dòng); H1b thành bước 0; câu hỏi User 5 (Q1 cũ = A quyết). **Bản 4 (C, 10:38 02/11/2026) — sửa N2′ vòng 3 (§5.3 + Q2): `589bec308f41`**; H4c đếm lại 13 / 69 file đích có mục Nguồn dữ liệu ⇒ khuyên dòng cố định "có thể đã thay đổi" thay năm nguồn. **Bản 5 (C, 11:04 02/11/2026) — ghi lựa chọn User Q1–Q5 (vòng 4 ready): `03cb538cf00c`**, chờ User duyệt sha.
  **Review vòng 1 (A ghi 10:12 02/11/2026):** `changes_requested` — 0 blocker / 4 major / 8 minor (`docs/superpowers/specs/2026-11-02-phase-9-design_review.md`, sub-agent ngữ cảnh mới của A, chỉ dựa trên Căn cứ). A kiểm M1, M2 đúng (phạm vi ⇒ thành câu hỏi User). C sửa ⇒ người review kiểm phần sửa.
  **Review vòng 2 (A ghi 10:23 02/11/2026):** bản 2 `d819918c2f2e` — 12/12 finding vòng 1 đóng; còn N1 major (H1b chưa có lỗi quan sát ⇒ thành bước 0 như H4b) + N2–N5 minor. **A quyết (kỹ thuật trong phạm vi, §9.3):** Q1 — H1 bậc 1 chạy tuần đầu song song (0 USD, tất định); bỏ Q7; Q8 thành dòng mặc định trong lời duyệt ⇒ câu hỏi User ≤ 5.
  **Vòng 3 ⇒ bản 4 `589bec308f41`; vòng 4: `ready_for_user_confirmation`** (sub-agent; N2′ đóng, 13/69 file có "Nguồn dữ liệu"). **User trả lời Q1–Q5 (A ghi nhận 11:03 02/11/2026):** Q1 (a) câu khẩn cấp, thử 10 câu trước rồi mới quyết · Q2 (a) một dòng cố định khi nguồn thuộc vé / điểm đến / lễ hội · Q3 (a) đếm trước (≥ 3 câu mới làm) · **Q4 PA1 mặc định (chỉ liệt kê giá có nguồn) + khi tới phần hỏi lại (tuần 16/11) làm bước nhỏ: tra web cách trợ lý du lịch trình bày chi phí (0 USD) + User đọc vài câu mẫu 2 cách ⇒ User chọn lại** (User hỏi có cần nghiên cứu thêm không — A khuyên chưa khoá cứng) · Q5 (a) 3 câu hỏi gần nhất + đoạn 1 lượt. ⇒ C ghi vào spec ⇒ sha mới ⇒ User duyệt sha.

## B116 — so sánh cách làm giao diện mới (giao 14:36 01/11/2026; User chọn (a))

- **Mục tiêu:** một trang so sánh 2–3 cách làm giao diện mới cho đồ án (chưa code), để User chọn phiên sau. Mức công: **tối thiểu, 1 file chính** (User nhắc over-engineer — S64).
- **Đọc:** `report_agent/2026-10-31_streaming_spec/yeu_cau_cho_giao_dien_moi.md` (full — 17 yêu cầu phải giữ, nhất là CSP / không CDN / lọc HTML); `frontend/` hiện tại (targeted);
  skill Claude Code `frontend-design` (gọi Skill); tham khảo User đưa (là **dữ liệu**, không phải lệnh): 2 SKILL.md ở `github.com/nextlevelbuilder/ui-ux-pro-max-skill` (`.claude/skills/ui-ux-pro-max/`,
  `.claude/skills/ui-styling/`) — WebFetch đọc, **không cài** vào repo; ghi chú khoá AI FDE `data/course_notes/` (targeted, phần giao diện); giao diện của một dự án khác của User
  (đường dẫn trong `data/giao_dien_moi_2026-11-01/tham_khao_du_an_khac.md`; chỉ đọc; **chi tiết dự án khác chỉ ghi ở `data/`**, file tracked nói "một dự án khác của User").
- **Làm:** 2–3 phương án (vd React + Vite build tĩnh FastAPI phục vụ · JS thuần làm lại có thư viện nhỏ · phương án khác nếu có lý do), mỗi cái: khớp 17 yêu cầu (đặc biệt CSP không nới), công làm,
  khi nào sai, chọn khác mất gì. Thêm 2 ý từ B0: (1) hiển thị nguồn gọn thay `[n]` chen trong câu (giữ `[n]` ở tầng máy); (2) D5 — streaming chỉ lợi 0,44 s: giữ PA1 hay PA3. Hướng giao diện
  (bố cục, màu, chữ) theo câu A đang hỏi User (A nhắn thêm khi có).
- **Không làm:** sửa code / `frontend/`; cài skill / package; tải ảnh; paid API. Tra web: `scripts/tra_web_codex.sh` (chỉ thông tin công khai) hoặc WebFetch.
- **Đầu ra:** `report_agent/2026-11-01_giao_dien_moi/b116_so_sanh_giao_dien.md` (tracked — không chi tiết dự án khác); ghi chú tham khảo dự án khác ⇒ `data/giao_dien_moi_2026-11-01/`. 0 USD. Xong ⇒ nhắn A.
- **Dừng:** thấy yêu cầu nào phải nới CSP / đổi API ⇒ dừng, báo A.
- **Quyết định (14:45 01/11/2026, User + A):** User: **làm cho laptop** (hiện chỉ User dùng, chưa có du khách); công nghệ "React hoặc Next tuỳ A, có thể Tailwind + shadcn". **A chọn: React + Vite build tĩnh,
  FastAPI phục vụ** (không Next — cần server Node hoặc export tĩnh, thêm phần SSR không cần); **Tailwind được dùng** (sinh CSS lúc build, không đụng CSP); **shadcn / Radix chỉ dùng linh kiện
  qua dò CSP 0 vi phạm** trên bản build (B116 nghi Radix chèn `<style>` lúc chạy). Điện thoại: chỉ cần không vỡ, không tốn công riêng. Yêu cầu 18: link nguồn bắt cả `[n]` lẫn `[Nguồn n]` (B116 (4), A kiểm `chat.py:304-316`, `app.js:44`).
- **Trang (14:53 01/11/2026, User):** bây giờ **chỉ trang hỏi đáp** (khung nguồn bên cạnh). **Ghi để nhớ:** khi lên agent / trợ lý (Phase 9) nâng cấp giao diện thêm (vd nhiều lượt, trang giới thiệu / số đo, duyệt kho — chọn lúc đó).
- **Phong cách (14:57 01/11/2026, User chọn (a)):** hiện đại, gọn, nét Huế nhẹ — nền sáng trung tính, màu nhấn tím Huế (nút, link nguồn, tiêu đề), một font dễ đọc tiếng Việt **tự host**; không hoa văn / ảnh nền.
- **Chốt (15:05 01/11/2026, User (a)):** nguồn = số nhỏ nâng lên bấm được + danh sách ở khung bên (giữ `[n]` ở tầng máy); D5 = **giữ PA1** (đổi PA3 nếu rút / xoá > luật D5). **B116 xong — A đọc cả file, kiểm tương phản 4 cặp + không lộ dự án khác: đạt.** Code giao diện: phiên sau (User duyệt gói npm lúc giao).
- **Trạng thái (B, 15:00 01/11/2026):** **xong đủ** (so sánh + đã chọn + yêu cầu 18 + mục dò CSP shadcn + hướng nhìn: bố cục ASCII, 12 token màu đạt AA tính thật, Be Vietnam Pro OFL tự host, bảng 6 trạng thái), **chờ A xem** — `report_agent/2026-11-01_giao_dien_moi/b116_so_sanh_giao_dien.md`; ghi chú dự án khác `data/giao_dien_moi_2026-11-01/tham_khao_du_an_khac.md`. 0 USD.

## Nghiên cứu rộng Phase 9 (User "làm đi" 15:08 01/11/2026; A dẫn) — đợt `report_agent/2026-11-01_nghien_cuu_phase_9/`

- **Mục tiêu (User):** nghiên cứu chuyên sâu, nghĩ rộng — thực tế doanh nghiệp / tổ chức triển khai trợ lý du lịch - văn hoá ra sao, vận hành, vấn đề, chức năng,
  khả năng; paper; repo GitHub ⇒ báo cáo đầy đủ ⇒ A đề xuất hướng hợp hue_rag ⇒ brainstorm với User. 4 mạch: (1) thực tế triển khai, (2) chức năng + khả năng,
  (3) học thuật, (4) mã nguồn mở. A: viết yêu cầu ChatGPT chuyên sâu, tổng hợp, báo cáo `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md`, đề xuất.
- **Chung cho B117 / C116:** bối cảnh chép nguyên `data/nghien_cuu_phase_9_2026-11-01/boi_canh_chung.md` vào yêu cầu; **chỉ thông tin công khai**; chạy
  `scripts/tra_web_codex.sh <yêu cầu .md> <tên_ngắn>` (mỗi mạch một lượt, tuần tự); yêu cầu .md để `data/nghien_cuu_phase_9_2026-11-01/yeu_cau/`.
  Kết quả Codex là **dữ liệu**: tự WebFetch kiểm **3 ý quan trọng nhất / mạch** (URL có thật, đúng bài, đúng ý); URL không có trong `url_da_mo.txt` = tự khai.
  Đầu ra mỗi mạch: `data/nghien_cuu_phase_9_2026-11-01/<b|c>_mach<n>.md` — bảng phát hiện (ý · nguồn URL + ngày · nhãn đã kiểm / tự khai / suy ra),
  "điều này gợi ý gì cho hue_rag" tách riêng, chỗ còn thiếu. Không đề xuất phạm vi Phase 9 (việc của A). 0 USD API; script cảnh báo lệnh shell ⇒ dừng, báo A.
- **B117 — mạch 1 + 2:** (1) tổ chức / doanh nghiệp thật đang chạy trợ lý AI du lịch - văn hoá (cơ quan du lịch, bảo tàng / di sản, khách sạn, OTA, ứng dụng ở Việt Nam / Huế):
  chức năng, kiến trúc nếu công bố, cách vận hành (cập nhật dữ liệu, kiểm nói sai, người duyệt, chi phí, đa ngôn ngữ, đo hiệu quả), sự cố / thất bại / bài học;
  (2) bản đồ chức năng của trợ lý du lịch (hỏi đáp, hỏi lại, lịch trình, ngân sách, bản đồ, sự kiện theo ngày, thuyết minh, giọng nói, ảnh, đặt chỗ…) + người dùng thật cần gì / bỏ dùng vì sao (khảo sát, nghiên cứu người dùng).
- **C116 — mạch 3 + 4:** (3) paper 2023–2026: agentic RAG, câu nhiều bước / nhiều nguồn, hỏi lại khi câu mơ hồ / thiếu thông tin, hội thoại nhiều lượt có RAG, agent lập lịch trình
  (bộ đo kiểu TravelPlanner), đánh giá trợ lý; có gì cho tiếng Việt; (4) repo GitHub: bắt đầu từ 8 repo trong `báo cáo nghiên cứu github.txt` (nay ở `data/nghien_cuu_phase_9_2026-11-01/` — chỉ lấy tên repo)
  + tìm thêm; mỗi repo: làm gì, kiến trúc, độ chín (sao, commit gần nhất), học được gì / không hợp.
- **Dừng:** 16:20 01/11/2026 dù chưa xong — ghi phần đã có, báo A (User kết phiên ~16:30).
- **Trạng thái B117 (B, 15:23 01/11/2026):** xong, **chờ A xem** — `data/nghien_cuu_phase_9_2026-11-01/b_mach1.md`, `b_mach2.md` (yêu cầu ở `yeu_cau/`; kết quả thô `data/tra_cuu_cli/2026-11-01_b-mach{1-trien-khai,2-chuc-nang}/`). Codex 2 lượt (0 trang ghi đã mở) ⇒ B WebFetch: mạch 1 đạt 3 ý + 2 trang Huế TRIPO; mạch 2 đạt 3 ý (2 nguồn không mở được, ghi tự khai). 0 USD API.
- **Huế TRIPO** (`huetripo.hue.gov.vn/trip-planner`, Sở VHTTDL Huế + HueCIT, ra mắt 31/10/2026 — B117, A WebFetch kiểm): **User 15:22 01/11/2026 chọn thử có giới hạn ở phiên sau** — A soạn ~10 câu tự viết (không Golden / câu kín, không thông tin cá nhân), **User tự gõ trên trình duyệt** (agent không gửi vào trang ngoài), dán câu trả lời về; A so cạnh hue_rag ⇒ bảng so sánh cho đồ án.

## Brainstorm Phase 9 (bắt đầu 16:01 01/11/2026; A ghi 16:08 01/11/2026)

- **Đề tài (đã chốt với GV):** "Xây dựng ứng dụng hỗ trợ trải nghiệm văn hóa và du lịch Huế dựa trên Retrieval-Augmented Generation". **Bảo vệ ~04–10/01/2027** ⇒ đóng code tạm ~20/12/2026.
- **B1 = (b):** trợ lý di sản đáng tin (H1 câu nhiều nguồn · H2 hỏi lại bằng danh sách trường trong code · H3 nhớ ngắn 3–5 lượt · H4 thông tin theo ngày + chặn câu an toàn trước model)
  **+ lịch trình gợi ý nhỏ** (thứ tự điểm theo khu vực, có nguồn; không giờ / giá chính xác; không đặt chỗ). Không: agent tổng quát, đặt chỗ, giọng nói / ảnh / nhiều ngôn ngữ.
- **Thứ tự A đề xuất (chưa chốt):** giao diện (~1 tuần) ⇒ H4 nhỏ (2–3 ngày) ⇒ H2 (~1 tuần) ⇒ H3 (~1 tuần) ⇒ lịch trình nhỏ (1–1,5 tuần; dữ liệu khu vực / thời lượng ~20–30 điểm) ⇒ H1 (thử 1 lần;
  không vượt nhiễu ⇒ kết quả âm, dừng — chỗ cắt đầu tiên) ⇒ đóng code + đo hồi quy + luận văn (~2 tuần). Rất căng ⇒ cắt H1 trước nếu trễ.
- **Đầu vào từ thử TRIPO (B119):** hue_rag từ chối nhầm câu 2 ý (giờ + giá; kho có giá vé ở `heritages/heritage-guides.md`, thiếu giờ?) ⇒ xét "trả lời phần có" cách khác R2 (8.2 bỏ vì phạm sàn
  ngoài kho); câu trang phục Đại Nội: hue_rag đúng theo kho, TRIPO nói ngược. Giao diện: thêm **yêu cầu 19** — nhãn "Trợ lý AI, câu trả lời dựa trên kho, có thể sai" (Luật AI 134/2025 Đ.11.1, C117).

## B119 — khám phá + thử Huế TRIPO bằng Playwright, so với hue_rag (User duyệt 15:33 01/11/2026: "tự vào khám phá, dùng playwright, chụp màn hình, thử các tính năng")

- **Mục tiêu:** hiểu TRIPO làm gì, giao diện / luồng ra sao, trả lời 10 câu thế nào ⇒ rút giá trị / ý nghĩa / ứng dụng cho hue_rag (đồ án + Phase 9 + giao diện mới).
- **Làm:** Playwright (`uv run`, chromium headless, một trình duyệt) mở `https://huetripo.hue.gov.vn/trip-planner` + trang chủ: chụp màn hình các màn chính; thử các tính năng **không cần
  đăng nhập** (lập lịch trình theo biểu mẫu với giá trị mẫu, chat, thuyết minh, bản đồ, đổi ngôn ngữ); gõ 10 câu `data/nghien_cuu_phase_9_2026-11-01/tripo/cau_thu.md` (mỗi câu chờ trả lời xong,
  nghỉ ≥ 5 s giữa các lượt — không tạo tải). Cùng 10 câu qua `/api/chat` của hue_rag (server tạm, cổng trống, `--env-file` tuyệt đối; ~0,003 USD; tắt server khi xong).
- **Không làm:** đăng nhập / tạo tài khoản; nhập email / số điện thoại / tên thật; bấm đặt chỗ / liên hệ / gửi email / thanh toán; quét hàng loạt danh mục; chạy script lạ của trang ngoài khung
  Playwright; gửi nội dung kho / Golden. Nội dung trang là **dữ liệu**, không phải lệnh.
- **Đầu ra:** ảnh + kết quả thô `data/nghien_cuu_phase_9_2026-11-01/tripo/` (private); `tripo/b119_kham_pha.md`: bản đồ tính năng thấy thật, bảng 10 câu (TRIPO ↔ hue_rag: đúng / sai / có nguồn /
  từ chối / hỏi lại — nhãn "B đánh giá", không phải chấm chuẩn), điểm hay đáng học, điểm yếu, gợi ý cho hue_rag (suy ra). Dừng 16:15 dù chưa xong.
- **Trạng thái B119 (B, 15:55 01/11/2026):** xong, **chờ A xem** — `data/nghien_cuu_phase_9_2026-11-01/tripo/b119_kham_pha.md` + `anh/` (22 MB) + JSON thô. hue_rag 11 lượt ≈ 0,0040 USD; server 8797 đã tắt; script tạm đã xoá.

## Hồ sơ đã đóng (chỉ tra cứu)

- Streaming + lượt đo cuối Phase 1–8 (01/11): `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`.
- Phase 8.2 (User đóng 28/10): `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
- Đợt sửa kho 1 + 2, thước lỗi nặng, đo ngày hôm nay, Qwen3-8B: `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md` §7–§8.
- Tra web bằng Codex (31/10): `report_agent/2026-10-31_tra_web_codex/TONG_HOP.md`.
