# CURRENT_HANDOFF — việc đang mở của A/B/C/E

Cập nhật: 22:19 05/11/2026 (A, **kết phiên tối 05/11**). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở.
Nguyên văn phiên tối 05/11 (mọi việc giao + quyết định theo giờ): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05_toi.md`; sáng–chiều 05/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-05_b4_am_chia_phase_10_12.md`.

## PHIÊN SAU ĐỌC TRƯỚC (đọc trước nhất)

**Hệ thống (`main` = `origin/main`):** RAG 1–8 + trợ lý Phase 9: định tuyến 4 tuyến (trò chuyện / trợ lý Huế / ngoài phạm vi / khẩn cấp, dòng mở PA1) + dòng "có thể đã thay đổi" + tìm thêm `tim_kho` ≤ 2 lần + nhớ câu hỏi 3 lượt + câu dặn hẹp + giao diện nhiều lượt + 👍 / 👎 + **#6 song song BẬT** + **tra web B6 BẬT** (`7ff8e5a` + bật `b7c024e`: câu về Huế kho từ chối ⇒ mục "Từ web (chưa kiểm)"; thiên tai ⇒ câu cố định NCHMF / 112). **Cờ tắt:** hỏi lại do code (`hoi_lai`), **B5 lịch trình** (`lich_trinh` — chờ User chấm Q3), **ảnh Phase 10** (`anh.bat`, `2ca9937` + giao diện điện thoại `76319e2`). Kho 204 file / **8.435 đoạn** (giờ mở cửa chung 11 điểm Quần thể, 05/11 tối); build record `9921888f2030`; T1 `64656a87c109`; Golden md5 `6331e88fb171`. `frontend/dist/` không commit ⇒ `cd frontend && npm ci && npm run build`. Qdrant: Docker Desktop; collection chatbot + collection thử `hue_anh_siglip2` (172 điểm, chờ User quyết xoá).

**Tiền:** Phase 9 ≈ **1,87 / 2,5 USD** (phiên tối: B ≈ 0,194 — B6 0,143 · B5b 0,051; C ≈ 0,057 — kín B6 0,041 · sửa kho "sau" 0,013 · C202 0,003; A cổng ≈ 0,005). Phase 10 ≈ **0,098 / 0,15** (E tối 0,020). Tiền phiên tối ≈ **0,275 USD**; cả ngày 05/11 ≈ 0,77.

**Phase 9 — bậc còn lại:** B5 bật (chờ Q3) ⇒ **sửa lịch** đo có phí (`p9-sua-lich` `6543f82`, trần 0,20) ⇒ **B5b** review nhánh + merge + bật (User) + phần lịch "nếu mưa" (bảng v5) ⇒ **B7** đóng gói (quỹ 0,35). B5c dừng (tag `hoso/p9-b5c`).
**Phase 10:** ảnh xong (cờ tắt, User quyết bật); **giọng nói nghe** spec bản 4 `784d6f7abd9f` duyệt ⇒ G0 xong (`p10-giong-noi` `93bbc63`) ⇒ **G1 chờ User thu 40 câu** ⇒ G2 đo ⇒ G3 code. Đọc (TTS) để sau.
**Phase 11 / 12:** backlog (lưu trú, bản đồ toạ độ, dữ liệu mở; Phase 12 deploy AWS = điều kiện đóng code; **O5 cache câu trả lời** — User chọn để Phase 12, đo tỉ lệ câu lặp trước, không cache theo nghĩa).

### Phiên sau làm theo thứ tự

1. Mở A / B / C / E; `ListAgents`; **hỏi lại quyền phiên** (quyền tối 05/11 hết hạn) — đề xuất: như tối 05/11. Máy khởi động lại ⇒ worktree `/tmp` mất: B `/tmp/b_b5b`, `/tmp/b_sualich`; C `/tmp/c_sualich`, `/tmp/c_b5b` (tạo lại khi cần, cách ghi trong STATUS từng session). **Bẫy:** `.venv` chung có sherpa-onnx nhưng `uv.lock` của `main` chưa có ⇒ `uv sync` ở `main` gỡ mất (cài lại: xem `STATUS_E.md`).
2. **Đưa User 3 việc chờ** (mỗi lần một câu): (a) chấm 5 lịch kín B5 `data/phase_9/b5/kin/phieu_cham_user.md` (đạt ≥ 4 / 5 cả 3 tiêu chí ⇒ A bật `lich_trinh`); (b) phiếu bảng điểm v5 `data/phase_9/lich_trinh/diem_cho_user_v5.md` (5 dòng mới, 1 ô tick; "Bảo tàng Mỹ thuật" kho không có mục riêng — có thể bỏ); (c) thu 40 câu nói `data/phase_10/giong_noi/bo_40_cau/huong_dan_thu_cho_user.md` (User + ≥ 1 giọng Huế / Trung, file vào `data/phase_10/giong_noi/thu/`).
3. **B5b thời tiết** (`p9-b5b` `8bdeb65` + bản sửa hiển thị CHƯA commit — patch `data/phase_9/b5b/p9-b5b_chua_commit_q8_hien_thi.patch` `182904f45888`): B commit + push bản sửa (chạy lại `test_static_ui` + ảnh Q8 một câu) ⇒ A giao **review cả nhánh** (E — E đã review sớm E17 / E18; hoặc C nếu E bận) ⇒ rebase lên `main` + Q1 ⇒ A merge cờ `thoi_tiet` tắt ⇒ **hỏi User bật**. Đã đạt: đã thấy ×2 (Q3 9 / 10 ×2), vòng chỉnh 1 (ngoài 7 ngày ⇒ không số dự báo + câu cố định; A chốt luật trước lượt chạy), Q4 (S-AT), Q8. Tiền 0,0508 / 0,07. Phần "lịch có ngày + nếu mưa / bậc thang" (D9 / D10) chờ B5 bật + bảng v5 duyệt (settings đang trỏ v3 — v3 không có cột trong nhà).
4. **Khi User chấm Q3 đạt:** A bật `lich_trinh` + cổng (3 câu thật) + báo cáo ⇒ **sửa lịch** lượt có phí NGAY (C chạy đã thấy + kín theo plan `5b68f3cb666a`, pass^2, trần 0,20; `p9-sua-lich` cần rebase lên `main` mới + Q1 trước) ⇒ review ⇒ merge. Không chờ B5b (A trả lời C tối 05/11). Chuyển `lich_trinh_bang` sang v5 (khi User duyệt) ⇒ chạy lại kiểm 0 USD (Q1 / test).
5. **Giọng nói:** khi User thu xong ⇒ E: đổi WAV 16 kHz mono (`ffmpeg`) ⇒ **G2** đo Gipformer / Zipformer theo V-a tên riêng ≥ 90 % · V-c số ≥ 90 % · V-d p95 ≤ 1,5 s (câu ≤ 10 s) + RAM ≤ 1,5 GB · V-e chèn tên sai ≤ 1 / 40 (khi hotwords); WER chỉ theo dõi ⇒ report ⇒ A trình User ⇒ G3 code route + giao diện. Trong lúc chờ: E chuẩn bị script đổi WAV + plan G2 (0 USD).
6. **Câu hỏi cho User** (mục dưới).

### Nhánh

`main`; **đang mở:** `p9-b5b` (B), `p9-sua-lich` (B / C), `p10-giong-noi` (E), `p9-b5c` (hồ sơ, đã tag). **Đã merge ⇒ chờ User xoá (User `!`):** `p9-b4`, `p9-b5`, `p9-toc-do-6`, `p9-toc-do-6b`, `p10-anh`, `p10-anh-mobile`, `p9-b6` (local + origin). 4 worktree AGY cũ `c725987` (User quyết).

### Mã hay gặp

B0–B7 = bậc Phase 9; B5b = thời tiết, B6 = tra web; G0–G4 = bậc giọng nói (spec Phase 10 §8); Q… / D… / V-… = câu đo / quyết định / tiêu chí giọng nói; S-AT = thủ tục sinh lại câu an toàn (luật mới 05/11 tối: chênh đúng 1 ⇒ thêm 3 + 3, âm khi tổng chênh ≥ 2 / 6 — `skills/run-experiment/SKILL.md` §4); Bxx / Cxx / Exx = việc A giao; S / W / I = sổ `SO_CAI_TIEN_CACH_LAM.md`; #1–#18 = ý nghiên cứu 04/11.

## Ý TƯỞNG TỪ NGHIÊN CỨU 04/11 — trạng thái (nguồn `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md` mục 000; hồ sơ `data/nghien_cuu_tinh_nang_2026-11-04/`)

| # | Ý | Trạng thái |
|---|---|---|
| 1–7, 12 | Kiểm giá "…000đ" / "triệu"; không đủ điểm ⇒ câu cố định; `khong_xep` + lý do từ mã luật; dòng giả định do code nối; test cố tình vi phạm; dòng "Mình hiểu…"; cột `ten_khac`; lời dặn không dùng địa danh thật làm ví dụ | vào B5 (`d66f6a3`) |
| 8 | Sửa lịch nhiều lượt (`sua_lich` hành động có tên, khung giữ ở server, Đã đổi / Giữ nguyên, ≤ 2 hành động / lượt) | code B163 `1c53627`, chưa đo |
| 9 | Bộ chuỗi sửa lịch pass^k | bộ `data/phase_9/bo_do_sua_lich/` (10 + 5 kín); plan chọn pass^2 |
| 10 | Cột trong nhà / bậc thang ⇒ phương án ngày mưa | bảng v4 chờ User (chỉ cụm Kinh thành có điểm trong nhà) |
| 11 | `so_ngay` viết lạ ("3N2Đ", "cuối tuần") — theo dõi | chờ lượt đo sửa lịch |
| 13, 14 | Ưu tiên theo lĩnh vực; đoạn gần trùng | đếm 0 USD xong — không mở thí nghiệm (C179) |
| 15–17 | Nhãn lỗi tự động; "0 lỗi trên n ca" + luật ba; dự phòng demo mất mạng | B7 |
| 18 | Router gắn cờ ⇒ code gọi `lich_trinh` | không cần (Q2a đạt) |

**Không làm** (đã cân): lọc cộng tác / rating, TSP, GraphRAG, định tuyến bằng danh sách từ, bảng SQL giá, rerank / sparse mới, nhớ cả câu trả lời, web bật sẵn, công cụ ghi ra ngoài không cần duyệt.


## Câu hỏi cho User (hỏi mỗi lần một câu — đầu phiên sau)

1. **Quyền phiên** (đề xuất như tối 05/11: A tự điều phối, A tự commit / push, ≤ 1 USD / phiên, B / C / E push nhánh riêng, trần Phase 9 2,5).
2. **(gấp nhất)** Chấm 5 lịch kín B5 — `data/phase_9/b5/kin/phieu_cham_user.md`.
3. Phiếu bảng điểm v5 — `data/phase_9/lich_trinh/diem_cho_user_v5.md` (giữ / bỏ dòng "Bảo tàng Mỹ thuật"; ô tick: chỉ ghi "trong nhà" khi kho viết rõ, hay "bảo tàng ⇒ trong nhà").
4. Thu 40 câu nói — `data/phase_10/giong_noi/bo_40_cau/huong_dan_thu_cho_user.md`.
5. Bật **thời tiết B5b** khi review nhánh đạt? (câu dự báo ⇒ số từ Open-Meteo do code dựng, ghi giờ số liệu; ngoài 7 ngày ⇒ câu cố định; bão / lũ ⇒ NCHMF + 112.)
6. Bật **hỏi bằng ảnh** (`anh.bat`)? — ảnh gửi OpenAI, ~0,0004 USD / ảnh, đoán tên p95 6–9 s; đã sửa giao diện điện thoại (`BAO_CAO_HOI_BANG_ANH.md` §6). Xoá collection thử `hue_anh_siglip2`?
7. Vòng cải tiến 19 / 20: gỡ W4 / W39 (Session D 0 buổi, hạn 07/11) hay giữ; **W57** (khẳng định số / hiện trạng báo User ⇒ kiểm bằng dữ liệu sau thay đổi gần nhất, ghi nguồn + ngày — S95, S96); thêm luật "gói Python phải phát hành ≥ 2 tuần" (như npm) không (E hỏi; sherpa-onnx 2.0.1 phát hành ~10 ngày).
8. Xoá 7 nhánh đã merge (mục Nhánh) — User `!`.
9. Không gấp: câu thiên tai vẫn gọi Serper (~0,001 USD) chỉ để lấy link — bỏ lần gọi, dùng link cố định NCHMF? (C206 m-1); backlog sửa kho: vị trí Bảo tàng Cổ vật kho tự mâu thuẫn (C204); đọc 10 câu mẫu B4 / B6; 4 worktree AGY cũ; xoá sao lưu kho đợt 1 + 2; báo cáo tiến độ cho giáo viên.

## Câu hỏi A còn nợ (không cần User)

- Link Google Maps của B5 đổi sang toạ độ cho 17 điểm có toạ độ (C197; v5 thêm 1 toạ độ) — A quyết khi bật B5.
- B6 giới hạn: địa chỉ / số điện thoại trong mục web chưa kiểm ⊂ đoạn trích (đề xuất "mọi chuỗi số ⊂ đoạn trích" — việc sau); chữ đầu mục web p50 ~13 s (theo dõi; ý tối ưu: tra web song song khi kho có dấu hiệu thiếu); thêm "đang" vào luật thời gian thực sẽ chặn nhầm 1 câu đúng.
- B5b giới hạn: câu "tuần sau" không có số dự báo (luật ngoài 7 ngày); câu không dấu không có công cụ (ngoài phạm vi, User 25/10).
- Cách đếm token (`_token_count`) không tính kết quả tìm thêm + mô tả công cụ ⇒ chênh tới ~900 token; ngữ cảnh 1,7–4k ≪ 16k.
- Ghi đệm OpenAI: C202 05/11 tối âm — giữ như cũ; xét lại nếu tắt tìm thêm. Bảng sổ cải tiến: S41–S44 thiếu 1 cột. Log `FileHandler` không xoay vòng (deploy). Hạn mức OpenAI / Serper — đặt trước deploy (B6 đã bật).
- B7: dự phòng demo khi mất mạng; đề cương "trợ lý RAG có công cụ"; ý #15–#17.
- Theo dõi: router đưa S20 sang `khan_cap`; định tuyến > 10 s ⇒ `tro_ly_hue`; `chat_feedback` chưa nối `chat_metrics`; case Golden 67 từ chối ngẫu nhiên sau tìm thêm (C192).

## Session

**Phiên tối 05/11 (19:16–kết 22:20 05/11/2026):** A `hue-rag-4f` · B `hue-rag-4b` · C `hue-rag-3c` · E `hue-rag-bc` — cả bốn Claude Code, trực tiếp. Mỗi session đã viết lại `sessions/STATUS_<X>.md` cho phiên sau (việc dở, bước kế, worktree, tiền, bẫy, câu hỏi).

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C / E lúc mở phiên sau: kiểm nhanh ⇒ đọc `STATUS_<X>.md` + mục này ⇒ báo A ⇒ chờ.

## Quyền

- **Phiên tối 05/11 — HẾT HẠN lúc kết phiên (22:20 05/11/2026)** (User chọn "như sáng 05/11", A ghi nhận 19:19 05/11/2026). Tiền phiên tối ≈ 0,275 USD.
- **Tiền Phase 9: trần 2,5 USD** (User nâng 19:29 05/11/2026; không hết hạn theo phiên; dự phóng vượt ⇒ xin trước). **Phase 10:** trần 0,15 (dừng 0,13).
- **Đã duyệt, không hết hạn theo phiên:** spec Phase 10 bản 4 `784d6f7abd9f` (sherpa-onnx, tải model ≤ 300 MB, thu 40 câu; Web Speech bỏ); tải SigLIP 2 + collection ảnh (11:42 05/11); luật S-AT mới (20:14 05/11); cache câu trả lời ⇒ Phase 12 (20:27 05/11); bật `tra_web` (21:15 05/11).
- **User (09:00 05/11/2026):** cần công cụ / nghiên cứu / tải / khoá mới ⇒ tự nghiên cứu (0 USD, thông tin công khai) + đề xuất; thêm công cụ / thư viện lớn / tải model / khoá / tài khoản mới vẫn trình User trước (`Session_Prompt.md` §4).
- **Phase 9 (spec):** Serper dùng luôn (User chấp nhận rủi ro điều khoản); gói npm giao diện như đã duyệt 02/11; dữ liệu công khai dùng cho học tập, không kiểm giấy phép (05/11).
- **Thường trực:** A commit / push — hỏi User trước (luật chung), rồi A tự chạy; chỉ khi bị chặn / lỗi mới đưa `!` (`WORKFLOW.md` §9.6); B / C / E không commit trừ khi việc ghi rõ; duyệt cho A = duyệt cho B / C / E; thư viện nhỏ cần cho việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage + tiền; code luôn `uv run`.
- **Tra web:** `scripts/tra_web_codex.sh` (chỉ thông tin công khai); **không bao giờ gọi `agy`**. Khoá `SERPER_API_KEY` trong `.env` (không đọc / in).
- Giá `gpt-6-luna` (User 30/10): vào 0,10 · ra 0,50 · đọc đệm 0,01 · ghi đệm 30 phút 0,125 USD / 1M. Serper: 0,001 USD / lượt. Open-Meteo: 0.

## File private quan trọng (không commit)

| File | Nội dung | sha256 (12) / md5 |
|---|---|---|
| `knowledge-base-hue/evaluation/phase_8_1/split.json` | 120 dev / 56 test | `e2b1788dfbbc` |
| `data/phase_8_1/gold/gold_v5.jsonl` | nhãn đoạn đúng mặc định (kho đợt 2) | `33d16fd6b8f4` |
| `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` | Golden 176 | md5 `6331e88fb171` |
| `knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl` | 36 câu kín — đã dùng (B3); không chép nội dung | md5 `ddc59587b502` |
| `knowledge-base-hue/evaluation/final_2026-11-01/final_sealed.jsonl` | bộ kín 40 câu — **đã dùng** 01/11 | `7f97d4c10b2b` |
| `data/loi_nang_2026-10-28/` | thước lỗi nặng; `an_toan/questions.jsonl` 32 câu | `9fa81b0fcec4` |
| `data/do_cuoi_2026-11-01/` | lượt đo cuối Phase 1–8 (mốc của Phase 9) | — |
| `data/phase_9/` | bộ đo B4 / B5 / B5c / B6 / sửa lịch, bảng điểm v3 / v4, toạ độ, kết quả đo | — |
| `data/phase_10/anh/` | bộ ảnh đo, danh sách tên, patch `p10-anh`, E9 | — |
| `data/sua_kho_2026-11-05_gio/` | sửa kho giờ mở cửa: lệnh `tools/chay.sh`, sao lưu record / sparse | — |
| `data/nguon_mo_huegov_2026-08-05/` | dữ liệu mở Huế (có file dữ liệu cá nhân ⚠ — không vào kho / báo cáo) | — |

## Việc đang mở — luật chung khi sửa code / dữ liệu

- A commit + push `main` **trước** khi B / C / E sửa code; khai báo file trong `STATUS_<X>.md` trước khi sửa; skill `practical-project-coding`; test liệt kê file; report `<việc>_implementation.md`; review chéo; plan có tiêu chí ghi trước ⇒ session khác review **trước** khi A duyệt sha (sha tính từ file); review ≤ 2 vòng.
- **Bộ an toàn 32 câu luôn báo đủ 4 số** (đảo cảnh báo · sai điều kiện mới / hết · thiếu cảnh báo mới / hết · ngoài kho bị trả lời).
- **Cổng ổn định:** (1) test file chạm; (2) chạm giao diện ⇒ `cd frontend && npm ci && npm run build`; `cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port <cổng trống>`: `/` 200, `/health` 5 / 5, 1 câu trong kho + 1 câu ngoài kho (tự viết); `chat_metrics` mới = số câu; grep câu hỏi trong log = 0; tắt server bằng TaskStop (không `pkill -f`); (3) chạm tìm / chia đoạn: T1 giống byte; (4) 3 chỗ báo cáo (`WORKFLOW.md` §6); (5) hook tự chạy.
- **Đang dựng chỉ mục / đo latency ⇒ session khác không chạy lượt trả phí / việc nặng CPU / Qdrant.** Việc chạy nền: `run_in_background`, không vòng chờ `pgrep -f`.
- Test cần key: `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan`, `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`, `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`. `test_static_ui.py` cần bản build.
- Đọc kho: **chỉ** `scripts/grep_kb.sh`; report tracked tả câu ở mức loại câu. Giờ trong file: chạy `date` trước; tin nhắn không cần giờ. `rm` với biến: `"${X:?}"/…` hoặc đường dẫn cố định.

## Hồ sơ đã đóng (chỉ tra cứu)

- Phiên tối 05/11 nguyên văn: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05_toi.md`.
- Phiên 05/11 sáng–chiều nguyên văn (C173–C197, B156–B163, E1–E8, quyết định theo giờ, merge B4b / B5 / #6, B5c âm): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05.md`.
- Phiên 04/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-04.md`; 03/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-03.md`, `…_2026-11-03_toi.md`; 02/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-02.md`.
- Giao diện mới: `report_agent/2026-11-02_giao_dien_moi_code/`. Nghiên cứu Phase 9: `report_agent/2026-11-01_nghien_cuu_phase_9/` + `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md`.
- Streaming + đo cuối Phase 1–8: `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`. Phase 8.2: `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
