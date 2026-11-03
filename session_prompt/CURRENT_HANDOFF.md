# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 13:26 03/11/2026 (A, **kết phiên 03/11**: B1 merge `f01c032`, B2 merge `00d670e`; B3 code trên `p9-b3` `46008ed` chưa merge; vòng cải tiến 16). Trước: 20:47 02/11/2026 (A, kết phiên tối 02/11).
Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở. Phiên 03/11 nguyên văn (mọi mục B131–B136 / C133–C145, quyết định theo giờ) ở `session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-11-03.md`;
02/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-02.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-03_phase_9_b1_va_b2.md`.

## PHIÊN SAU ĐỌC TRƯỚC (đọc trước nhất)

**Hệ thống (`main` `00d670e` + docs):** chatbot = RAG 1–8 + **trợ lý Phase 9**: định tuyến 4 tuyến (trò chuyện / trợ lý Huế / ngoài phạm vi / khẩn cấp — câu soạn sẵn 113 / 114 / 115 / 112) + dòng nhắc "có thể đã thay đổi" (B1)
+ **trợ lý tự gọi `tim_kho` thêm ≤ 2 lần** (B2b; câu tìm đầu = câu gốc — B2a viết lại câu tìm không giữ). Giao diện React (`frontend/dist/` không commit ⇒ `cd frontend && npm ci && npm run build`). Kho 204 file / 8.424 đoạn; Golden md5 `6331e88fb171`; T1 `4d5bbe9e0edc`.
Qdrant chạy bằng Docker Desktop — `curl :6335` không trả lời ⇒ báo User. Chữ đầu câu về Huế 3,50 / 5,33 s (10 câu) — chỉ theo dõi.

**Phase 9** — spec bản 9 `169c2dd5f86a` (`docs/superpowers/specs/2026-11-02-phase-9-design.md`). Bậc: B0 ✓ · B1 ✓ · B2 ✓ · **B3 đang code** · B4–B7. Đi trước lịch ~2 tuần (luật cắt spec §6). Tiền Phase ≈ **0,66 / 2,0 USD**; mỗi phiên ≤ 1 USD.

**Phiên sau làm theo thứ tự:**
1. Mở A / B / C; `ListAgents`; **hỏi lại quyền phiên** (quyền 03/11 hết hạn) — đề xuất một câu: như 03/11 (A tự điều phối + tự quyết trong kế hoạch, A tự commit / push cả phiên, ≤ 1 USD). Kiểm Qdrant; worktree `/tmp/b_p9b3` mất sau khởi động lại ⇒ B tạo lại.
2. **B3 hoàn tất** (plan bản 2 `cd099ec0a00e`; report `report_agent/2026-11-02_phase_9_code/b136_b3_implementation.md`; review sớm `b136_review.md`; trần **0,40 USD**, dừng > 0,37; đã tiêu ≈ 0,255). Đã có:
   - D6 bản hẹp ("không tự thêm lời khuyên / lưu ý an toàn mà Bằng chứng không nêu; giữ lời khuyên có trong Bằng chứng") **giữ** — vòng 2 đạt cả 5 luật (từ chối nhầm 4, P0_sai 0, S20 hết lỗi, S10 / S04 đọc chữ đúng 4 / 4 · 3 / 4);
   - chuỗi đã thấy (25 × 3 bên): nhớ tên 6 / 6; **hỏi tiếp có nhớ ↔ câu gõ không lịch sử +0,65 [+0,15; +1,25]**; ngoài kho 0; đổi chủ đề tụt 0; usage − builder max 167 < 512; định tuyến đúng mọi lượt. **Khoá 13:17 03/11/2026 trên `46008ed`.**
   Còn lại theo thứ tự: (a) **C chạy + chấm phần kín** (`chuoi … --khong-in-chu`, `cham_chuoi.py`; brief judge phải dặn ghi `item` — bẫy B) ⇒ luật giữ / gỡ; (b) Q10 cổng ổn định; (c) **bước 8 giao diện nhiều lượt theo Bản 1 — Huế hiện đại** (User chọn 13:11 03/11; `data/giao_dien_v2/mau/1.html` `2952d57f3a92`; CSP giữ, đánh lại số trích dẫn 1..k, nút "Cuộc trò chuyện mới", ảnh Playwright laptop + điện thoại); bật `nho_hoi_thoai` khi giao diện xong; (d) C review cả nhánh ⇒ A merge ⇒ 5 chỗ báo cáo. Lệnh chạy tiếp: `STATUS_B.md` "PHIÊN SAU — B3".
3. **B4 (hỏi lại)**: bộ đo C143 sẵn (`data/phase_9/bo_do_b4/`, 30 câu 20 / 10 kín; luật trường ghi trước `luat_ghi_truoc.md`). **User chọn chi phí Cách A** (13:13 03/11: liệt kê giá có nguồn + ngày, không cộng tổng). B viết plan B4 sau khi B3 merge; người review: C.
4. **Viết plan B5 (lịch trình)** — người viết đọc: nháp bảng điểm C144 (`data/phase_9/lich_trinh/diem.json` 28 điểm / 8 cụm + `diem_cho_user.md`, 3 câu cho User cuối file) · nghiên cứu thời tiết C139 (`data/phase_9/thoi_tiet/nghien_cuu.md` — đề xuất Open-Meteo, CC BY 4.0, phi thương mại; A WebFetch kiểm 03/11) ⇒ quyết gộp thời tiết vào B5 hay bậc nhỏ sau B5 (User chọn 10:52 03/11) · `data/nghien_cuu_phase_9_2026-11-01/báo cáo nghiên cứu github.txt` §4 "Khuyến nghị" của 3 báo cáo (chưa ai đọc nội dung).
5. Theo dõi: router đưa câu cảnh báo S20 sang `khan_cap` 2 lần (B2 sinh lại, B3 Q2 lượt chính) — đếm ở B3 / B4; > 0 nữa ⇒ xét sửa lời dặn định tuyến (đổi lời dặn chung ⇒ hồi quy đủ 208). Tốc độ chữ đầu ⇒ xét tối ưu ở B7. `tim_kho` tới lần 3 ở 1–4 / 176 câu (chỉ đo).
6. ~~Xoá nhánh `p9-b1`, `p9-b2`~~ **XONG 13:29 03/11/2026** (User `!`, local + origin).

**Mã hay gặp:** B0–B7 = bậc Phase 9 (spec §5); D… / Q… / m-… = quyết định / câu đo / finding minor trong plan & review từng bậc; S20, S10, S04 = mã câu bộ an toàn 32 (nội dung private); P0_sai / P0_thieu = sai điều kiện / thiếu cảnh báo;
N_AA = số câu tụt giữa hai lượt cùng cấu hình (nhiễu); Bxx / Cxx = mã việc A giao B / C; S / W / I = sự cố / đề xuất / dời luật trong `SO_CAI_TIEN_CACH_LAM.md`.

## Câu hỏi cho User (hỏi mỗi lần một câu)

1. **Quyền phiên** (xem mục trên).
2. Khi rảnh: đọc 10 câu mẫu B4 `data/phase_9/bo_do_b4/mau_cho_user.md` — câu nào không giống người thật hỏi ⇒ báo A.
3. Không gấp: 4 worktree AGY cũ (`~/.gemini/antigravity-cli/…`) giữ hay gỡ; xoá sao lưu kho đợt 1 + 2?
4. File báo cáo tiến độ cho giáo viên (`gửi chatgpt/2026-11-03/báo cáo tiến độ giáo viên/TONG_HOP_TIEN_DO_DO_AN_03_11_2026_CHO_CHATGPT.md`, cập nhật tới B2) — User gửi ChatGPT; không nhắc coding agent (User 03/11); không link repo.

## Câu hỏi A còn nợ (không cần User)

- Câu B / C hỏi A kết phiên 02/11 (phân công, mẫu Golden, câu khẩn cấp) đã trả lời và áp ở B0–B3 — nguyên văn: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-03.md`.
- **Ứng viên tối ưu tiền (giả thuyết, C124 phát hiện, A kiểm 19:07 02/11/2026):** SDK 0.19.4 gán `prompt_cache_key` = `agents-sdk:run:<ngẫu nhiên>` mỗi `Runner.run` (`agents/run_internal/prompt_cache_key.py:124-129`); 40 dòng `chat_metrics` gần nhất `cached_tokens` = 0, `cache_write_tokens` ≈ 1.872 / câu ⇒ mỗi câu trả giá ghi đệm (0,125 / 1M, đắt hơn vào thường 0,10) mà không đọc lại. Phần chung giữa các câu chỉ là lời dặn (10 đoạn kho khác nhau mỗi câu) ⇒ lợi có thể nhỏ. Làm **thí nghiệm riêng sau B0** (`run-experiment`: key cố định ↔ hiện tại, đo USD / câu + chữ đầu), không trong B0.
- Bảng sổ cải tiến: S41–S44 thiếu 1 cột từ trước. W39 hạn 07/11 (0 buổi D ⇒ đề xuất gỡ W4 + W39).
- Log `FileHandler` không xoay vòng — xem lại khi deploy. Hạn mức tín dụng phía OpenAI cho key — chưa kiểm. Hạn mức trả trước phía Serper — đặt khi tới B6.

## Phiên tối 03/11 — việc đang giao (A ghi 18:01 03/11/2026)

- **B137 — hoàn tất B3 phần không phụ thuộc số kín** (B, `hue-rag-32`): `git worktree prune` ⇒ tạo lại `/tmp/b_p9b3` (nhánh `p9-b3`, symlink `data/` + `knowledge-base-hue/`) ⇒ **bước 8 giao diện Bản 1** theo `STATUS_B.md` "PHIÊN SAU — B3" mục 4.
  Chỉ sửa `frontend/` (+ test giao diện); **không** sửa lời dặn / `settings.yaml` / `assistant.py` / code backend đã khoá ở `46008ed` khi chưa có số kín (cần sửa backend ⇒ hỏi A). Không thêm gói npm. Commit lên `p9-b3`, push nhánh riêng.
  Q10 cổng + bật `nho_hoi_thoai` **sau** khi C báo số kín. Đầu ra: phần bước 8 trong `b136_b3_implementation.md` + ảnh Playwright (private `data/`).
- **C146 — chạy + chấm phần kín B3** (C, `hue-rag-40`): worktree riêng `/tmp/c_p9b3` `--detach 46008ed` (không đụng worktree của B), theo `STATUS_B.md` "PHIÊN SAU — B3" mục 1 + plan B3 bản 2 `cd099ec0a00e` (luật giữ / gỡ §4).
  Ước tiền trước khi chạy; trần chung B3 0,40 USD (đã ≈ 0,255), tổng sắp > 0,37 ⇒ báo A trước. Gửi B / A **chỉ số đếm Q3–Q6 + sha**. Xong ⇒ chờ B xong bước 8 + Q10 ⇒ review cả nhánh (C, mục 2 `STATUS_C.md`).
- Không có lượt đo latency trong lúc này (W31 không chặn). B báo A trước khi đo latency ở Q10.

## Session

**Phiên tối 03/11 (mở 17:56):** A `hue-rag-9e` · B `hue-rag-32` · C `hue-rag-40` — cả ba Claude Code, trực tiếp.

**Phiên 03/11 (mở 08:36, kết 13:26 03/11/2026):** A `hue-rag-5e` · B `hue-rag-52` · C `hue-rag-d8` — cả ba Claude Code, trực tiếp. B: B131 hoàn tất B1, B132 plan B2, B134 code B2, B135 plan B3, B136 code B3 (≈ 0,513 USD). C: C133 bộ đo B2, C134 review B1, C135 review plan B2, C136 bộ đo B3, C137 / C141 review B2, C138 câu hai ý, C139 thời tiết, C140 mẫu giao diện, C142 review plan B3, C143 bộ đo B4 + chi phí, C144 bảng điểm B5, C145 review sớm B3 (≈ 0,0006 USD). A: điều phối, merge B1 + B2, 5 chỗ báo cáo × 2, README repo, báo cáo cho giáo viên, vòng cải tiến 16.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C lúc mở phiên sau: không việc đang chạy ⇒ kiểm nhanh ⇒ báo A ⇒ chờ.

## Quyền

- **Phiên tối 03/11 (User chọn "như trưa 03/11", A ghi nhận 18:01 03/11/2026):** A tự điều phối + tự quyết trong kế hoạch; A tự commit / push cả phiên; ≤ 1 USD / phiên; B / C push nhánh riêng. Hết hạn cuối phiên.
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
