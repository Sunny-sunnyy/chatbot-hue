# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 14:52 02/11/2026 (A, **kết phiên 02/11**: giao diện mới vào `main` `ed8e6e8`; Phase 9 đổi hướng agent; **spec Phase 9 bản 9 User duyệt sha `169c2dd5f86a`**; vòng cải tiến 14).
Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở. Lịch sử phiên 02/11 (mọi mục việc B121–B124 / C118–C121, quyết định theo giờ, trạng thái review) dời **nguyên văn** sang
`session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-11-02.md`; 01/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-01.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-02_giao_dien_moi_va_spec_phase_9.md`.

## PHIÊN SAU ĐỌC TRƯỚC (đọc trước nhất)

**Hệ thống (`main`):** chatbot RAG mức 1 như 01/11 (streaming, 10 đoạn, `gpt-6-luna`) + **giao diện mới React + Vite + Tailwind** (merge `ed8e6e8` 02/11): bản build `frontend/dist/` **không commit** —
clone / worktree mới hoặc sửa `frontend/src/` ⇒ `cd frontend && npm ci && npm run build` (thiếu ⇒ `/` 404). Kho 204 file / 8.424 đoạn; Golden md5 `6331e88fb171`; T1 `4d5bbe9e0edc`. Qdrant chạy bằng Docker Desktop —
`curl :6335` không trả lời ⇒ báo User, không tự bật.

**Phase 9 = trợ lý agent có công cụ — SPEC DUYỆT** `docs/superpowers/specs/2026-11-02-phase-9-design.md` **bản 9 sha `169c2dd5f86a`** (User duyệt, A ghi nhận 14:48 02/11/2026; review 3 vòng
`…_review_v6.md`; bản 5 hướng cũ ở `077e3cb`). Sửa spec sau duyệt = bản mới, duyệt lại phần đổi. Tóm tắt:
- **Agent dưới chính sách**, OpenAI Agents SDK **0.19.4** (giữ — B123 + C121): agent **định tuyến** đầu ra có cấu trúc ⇒ trò chuyện / trợ lý Huế / ngoài phạm vi / khẩn cấp; trợ lý gọi công cụ tìm thêm kho · hỏi lại ·
  lịch trình; **code giữ** ngày hôm nay (vào lời dặn), tra web Serper (khi kho từ chối, mục "Từ web" [w n], nhãn chưa kiểm), lần tìm đầu (thí nghiệm). Nhớ hỏi + đáp trong cuộc trò chuyện (server RAM, 30 phút).
- **8 bậc** B0 nền ⇒ B1 định tuyến + trò chuyện + ngày ⇒ B2 tìm kho + thí nghiệm câu tìm ⇒ B3 nhớ ⇒ B4 hỏi lại ⇒ B5 lịch trình ⇒ B6 web ⇒ B7 so RAG cũ (cùng tuần). Mỗi bậc: plan nhỏ ⇒ session khác review ⇒ A duyệt sha ⇒
  nhánh riêng ⇒ review cả nhánh + cổng ổn định ⇒ A merge.
- **Chất lượng trước** — sàn tiền / tốc độ chỉ theo dõi; **bắt buộc log USD + ms** mỗi lần gọi LLM / Serper / câu / tuyến. Trần Phase **2,0 USD**, mỗi phiên ≤ 1 USD. Đóng code ~20/12/2026.

**Thứ tự việc phiên sau:**
1. Mở A / B / C; `ListAgents`; **hỏi lại quyền phiên** (quyền 02/11 hết hạn); kiểm Qdrant; `cd frontend && npm ci && npm run build` nếu chưa có `dist/`.
2. **Giao B0** (spec §5): người viết plan B0 + người review khác người viết; A duyệt sha (tính từ file). Việc song song không chồng file (vd C soạn bộ câu tuyến / chuỗi hỏi tiếp cho B1–B3 theo spec §4; phần kín do người không code giữ).
3. Đặt mốc kiểm mọi việc > 30 phút (W47); brief việc Phase 9 kèm mọi tài liệu cũ cùng Phase (W46); trước khi đề xuất cơ chế an toàn / bộ đo thêm: "đã quan sát chưa · ai dùng · bao giờ deploy" (W48).

**Kế hoạch chi tiết tuần 02–08/11 (A soạn 15:09 02/11/2026; theo spec §5, §6 — phiên sau giao, chưa ai làm):**
- **B0 — nền (≈ 0,003 USD), người làm đề xuất: B** (đã dò SDK ở B123, code giao diện B121):
  bọc RAG 1–8 thành công cụ `tim_kho` (gọi `retrieval_service.search`, `backend/retrieval/full_corpus.py:419`; top-k + collection do code điền); lõi chung `backend/llm/assistant.py` cho route stream + `/api/chat` + `answer_case`;
  sổ nguồn (kho `[n]` / web `[w n]`); log USD + ms mỗi lần gọi model (`RunHooks.on_llm_start/end` — `b123_sdk_probe.md`), mỗi câu, mỗi tuyến.
  **Tiêu chí B0 (spec §5):** S-T1 mới giống byte; `answer_case` qua lõi chung ra đúng câu trả lời đường RAG 1–8; test ranh giới (chỉ một module gọi mạng ngoài; không công cụ nào nhận URL); log đủ trường;
  grep chữ câu hỏi / mã phiên trong log = 0. Quy trình: B viết plan B0 ⇒ **C review plan** (chỉ dựa "Căn cứ để review") ⇒ A duyệt sha ⇒ nhánh `p9-b0` (worktree) ⇒ review cả nhánh ⇒ cổng ổn định ⇒ A merge.
- **Bước 0 khẩn cấp (User chọn Q1 (a) của spec bản 5, A ghi nhận 11:03 02/11/2026):** ~10 câu khẩn cấp **tự viết** (cháy, trẻ lạc, đuối nước, cấp cứu…) qua chatbot hôm nay (≈ 0,003 USD) ⇒ **User đọc** 10 câu trả lời ⇒ có lỗi ⇒ luật code + câu soạn sẵn ở B1;
  không ⇒ ghi "không cần". Người soạn câu + chạy: C (song song B0, không chồng file — chỉ gọi `/api/chat` qua server tạm cổng riêng; nếu B đang đo latency thì chờ, W31).
- **Viết bộ đo cho B1 (song song, người viết: C — không phải người code B1):** bộ tuyến (~40 đã thấy + phần kín; có 5 ca lái tuyến), bộ ngày (dùng lại 15 câu `data/do_cuoi_2026-11-01/ngay/`; 12 câu quyết), bộ khẩn cấp;
  mẫu Golden cố định ~30 câu cho B3–B6 (seed ghi trước, khoá ở B0 — spec §4). Phần kín: B (người code) **không mở**.
- **Mốc tuần:** B0 đạt trước 09/11 ⇒ tuần 09–15/11 làm B1. Luật cắt đầu tiên **16/11** (B1 chưa đóng ⇒ B2 chỉ làm B2a). A kiểm luật cắt mỗi thứ Hai (spec §6).
- **Chú ý khi viết plan các bậc** (minor còn lại từ review spec, sửa trong plan): m17 nếu B2a giữ V2 thuần thì A/A đường có công cụ chạy ngay ở B2a; lượt `hoi_lai` + `StopAtTools` có `final_output` khác `AnswerOutput`
  (`backend/llm/generator_openai_full_corpus.py:269`) ⇒ cần nhánh riêng; cổng web chỉ mở khi `outcome` thường; danh sách "trước khi deploy" ở spec §7 (soát chữ web, điều khoản Serper, lưu phiên, R1 C106).

**Mã hay gặp:** B0–B7 = bậc Phase 9 (spec §5); P1–P5 = câu User đã chọn 14:42 02/11 (spec §10); V0–V3 = phương án câu tìm kho (B2a); [w n] = trích dẫn web; T1 = kết quả tìm 158 câu (so "giống byte");
S / W / I = sự cố / đề xuất / dời luật trong `SO_CAI_TIEN_CACH_LAM.md`; M-n / m-n = finding major / minor; Bxx / Cxx = mã việc A giao B / C.

## Câu hỏi cho User (hỏi mỗi lần một câu)

1. **Quyền phiên.** A khuyên: như 02/11 (A tự điều phối + tự thử trong luật; ≤ 1 USD / phiên; A tự commit / push; B / C push nhánh riêng).
2. ~~**Xoá nhánh `giao-dien-moi`**~~ **XONG 15:15 02/11/2026** (User `!` xoá local + origin). Cũ: (local + origin): đã merge `ed8e6e8`; `git log main..giao-dien-moi` rỗng (A kiểm 14:52 02/11/2026) — User `!`
   (`git branch -d giao-dien-moi` + `git push origin --delete giao-dien-moi`).
3. **Rà bảo mật C106 còn chờ User** (`report_agent/2026-10-31_streaming_spec/c106_bao_mat_dong_goi.md` bản 2): R4 cắt 22 dòng log cũ chứa nguyên câu hỏi thử; các mục deploy để lúc deploy.
4. **Sổ cải tiến chờ User:** W35 (kiểm điều khoản trước công cụ / tài khoản ngoài mới — 02/11 đã làm thực tế với Serper), W42, W43.
5. Không gấp: 4 worktree AGY cũ (`~/.gemini/antigravity-cli/…`, nhánh `subagent-Monuments-Reviewer-*`) giữ hay gỡ (User `!`)? Xoá sao lưu kho đợt 1 + 2?

## Câu hỏi A còn nợ (không cần User)

- **Câu C hỏi A (C, kết phiên 02/11; A trả lời sẵn 15:12 02/11/2026 — kỹ thuật trong phạm vi):**
  1. Phân công người code B1–B3 ⇒ **A quyết lúc giao**, giữ luật "người viết bộ đo ≠ người code bậc đó" (vd B code B0–B2, C viết bộ tuyến / ngày / nhớ; nếu C code B3 thì B viết bộ nhớ).
  2. Mẫu Golden ~30 câu ⇒ **đồng ý: lấy từ cả 176**, 6 câu / loại × 5 loại, seed ghi trước (chỉ hồi quy, không dùng chọn biến thể).
  3. 10 câu bước 0 khẩn cấp ⇒ **đồng ý dùng lại làm bộ khẩn cấp "đã thấy" của B1** (phần kín viết thêm riêng).
- **Câu B hỏi A (B, kết phiên 02/11; A trả lời sẵn — kỹ thuật trong phạm vi):**
  1. B0 giữ đường RAG 1–8 y nguyên qua lõi mới (code gọi `tim_kho`, sinh 1 lần, `max_turns=1`); vòng công cụ do model gọi để B2b (hoặc B2a nếu đo V2) ⇒ **đúng ý spec** (§5 B1: `tro_ly_hue` = đường RAG 1–8, chưa công cụ).
  2. "Chỉ một module gọi mạng ngoài" ⇒ **mỗi nhà cung cấp một module** (OpenAI: generator hiện có; Serper: module mới ở B6) + test kiểm **danh sách module cho phép** import client mạng (`openai`, `httpx`, `requests`…); ghi rõ câu này trong plan B0.
  3. Chọn + khoá mẫu Golden ~30 câu ở B0 ⇒ **C** (người không code), seed ghi trước.
  - **Rủi ro B ghi cho plan B0:** đã có lõi chung `backend/llm/grounded_answer.py` ⇒ `assistant.py` bọc / thay, **không để hai lõi**; S-T1 qua `tim_kho` so danh sách chunk bên trong, không so chữ đã định dạng.
  - **Ghi cho plan B0 (rủi ro C thấy trước):** tiêu chí "`answer_case` ra đúng câu trả lời đường RAG 1–8" phải đo bằng **chuỗi gửi model giống byte + T1 giống byte**, không so chữ trả lời (model không tất định).

- Bảng sổ cải tiến: S41–S44 thiếu 1 cột từ trước. W39 hạn 07/11 (0 buổi D ⇒ đề xuất gỡ W4 + W39).
- Log `FileHandler` không xoay vòng — xem lại khi deploy. Hạn mức tín dụng phía OpenAI cho key — chưa kiểm. Hạn mức trả trước phía Serper — đặt khi tới B6.

## Session

| Vai | Terminal (02/11 — kết phiên 14:52) | Agent | Liên lạc | Phiên 02/11 | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-7e` | Claude Opus 5.5 | trực tiếp | điều phối; merge giao diện; 3 sub-agent khoá FDE; yêu cầu ChatGPT; review spec bằng sub-agent; vòng cải tiến 14 | `STATUS_A.md` |
| B — thực thi | `hue-rag-d6` | Claude Opus 5.5 | trực tiếp | B121 giao diện, B122 tra web, B123 dò SDK, B124 review governance | `STATUS_B.md`; ≈ 0,002 USD |
| C — thực thi | `hue-rag-29` | Claude Opus 5.5 | trực tiếp | C118 / C120 spec Phase 9 (bản 1–9), C119 review giao diện, C121 thử SDK 0.24 | `STATUS_C.md`; ≈ 0,0006 USD |

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C lúc mở phiên sau: không việc đang chạy ⇒ kiểm nhanh ⇒ báo A ⇒ chờ.

## Quyền

- **Phiên 02/11 — HẾT HẠN cuối phiên** (User, A ghi nhận 09:48 02/11/2026): như 01/11 — A tự điều phối + tự thử; ≤ 1 USD; A tự commit / push; B / C push nhánh riêng. Tiền phiên 02/11 ≈ **0,003 USD** paid
  (B ≈ 0,002 · C ≈ 0,0006 · A 0; sub-agent + judge dùng quota Claude).
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
- **Cổng ổn định:** (1) test file chạm; (2) chạm giao diện ⇒ `cd frontend && npm ci && npm run build`; `cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port <cổng trống>`:
  `/` 200, `/health` 5 / 5, 1 câu trong kho + 1 câu ngoài kho (câu tự viết); đếm `chat_metrics` mới = số câu; grep câu hỏi trong log = 0; tắt server (TaskStop — **không `pkill -f`**, bẫy §8);
  (3) chạm tìm / chia đoạn: T1 giống byte; (4) đủ 5 chỗ (`WORKFLOW.md` §6); (5) hook tự chạy.
- **Có lượt đo latency ⇒ session khác không chạy lượt trả phí / việc nặng CPU / Qdrant** (W31). Việc chạy nền: `run_in_background`, không vòng chờ `pgrep -f`.
- Test cần key: `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan`, `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`,
  `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`. `test_static_ui.py` cần bản build.
- Đọc kho: **chỉ** `scripts/grep_kb.sh`; report tracked tả câu ở mức loại câu. Giờ trong file: chạy `date` trước; tin nhắn không cần giờ (W45). `rm` với biến: `"${X:?}"/…` hoặc đường dẫn cố định.

## Hồ sơ đã đóng (chỉ tra cứu)

- Phiên 02/11 nguyên văn (B121 giao diện, B122 / B123, C118–C121, các quyết định agent theo giờ): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-02.md`.
- Giao diện mới: `report_agent/2026-11-02_giao_dien_moi_code/` (`b121_giao_dien_implementation.md`, `b121_review.md`); hướng chọn B116 `report_agent/2026-11-01_giao_dien_moi/`.
- Nghiên cứu Phase 9: `report_agent/2026-11-01_nghien_cuu_phase_9/` + `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md`.
- Streaming + lượt đo cuối Phase 1–8 (01/11): `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`. Phase 8.2: `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
