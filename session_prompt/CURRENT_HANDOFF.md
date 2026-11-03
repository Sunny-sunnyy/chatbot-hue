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

1. ~~Quyền phiên~~ — User chọn "như trưa 03/11" (phiên tối).
1b. **Khi User quay lại (phiên tối), hỏi mỗi lần một câu:** (a) tính năng mới từ nghiên cứu sản phẩm thật — nút 👍 / 👎 "báo sai" mỗi câu; câu ngoài phạm vi kèm 1–2 gợi ý (`BAO_CAO_NGHIEN_CUU_PHASE_9.md` mục 00); (b) tối ưu tốc độ chữ đầu sớm (sau B3b) — chờ C150 phân tích; (c) plan B5 nháp (C149 `42afc1c7bc64`): trần 0,10 USD, bảng cụm kề + 2 cột `toi` / `luu_y`, thời tiết gộp B5 hay bậc nhỏ B5b sau (C đề xuất B5b).
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
  **C: XONG 18:12 03/11/2026** — số đếm gửi A + B; private `data/phase_9/b3/chuoi_sealed_c146/KET_QUA_C146.md` `16afdf317df0`; 0,0322 USD (B3 ≈ 0,287). **Chờ A quyết** Q5 K-N2 (máy đếm 1 lượt ngoài kho bị trả lời; C kiểm: nhãn bộ đo sai). Sau đó C chờ B ⇒ review nhánh.
  **A quyết K-N2 (C ghi lại):** tính nghiêm ⇒ cờ nhớ không bật. **C147 review sớm `10ec9a2..b156f92` XONG 18:25 03/11/2026:** `b136_review.md` "Vòng sớm 2" — 0B / 0M / 1m (m-3 report). C rảnh: chờ A (bộ chuỗi mới nếu User chọn; review phần B thêm).
  **C148 bộ chuỗi B3b XONG 18:37 03/11/2026:** private `data/phase_9/bo_do_b3b/` (12 chuỗi / 25 lượt, md5 `0f2360466366`, README `cc1b1a707a52`; B không mở). Chờ B báo commit sửa ⇒ C chạy 3 bên có lưu ngữ cảnh ⇒ số đếm.
- **C146 xong** (C báo): Q3 kín 4 / 4 (cộng 10 / 10) · Q4 nhớ ↔ gõ không lịch sử +0,60 [0,00; +1,40] (luật kín TB ≥ 0 đạt) · Q5 điều kiện 0 đảo · Q6 tụt 0 · Q8 max 178 < 512 · 0,0322 USD ⇒ B3 ≈ 0,287 / 0,40. Q5 ngoài kho: 1 lượt máy đếm "trả lời", C kiểm ⇒ nhãn bộ đo sai (câu mang tiền đề sai mà kho có dòng bác) ⇒ **A quyết 18:15 03/11/2026: (1) loại khỏi sàn nếu (3) chạy lại có ngữ cảnh xác nhận trích dẫn trỏ đúng đoạn; sai ⇒ tính nghiêm, báo A**. Kết quả private `data/phase_9/b3/chuoi_sealed_c146/KET_QUA_C146.md` `16afdf317df0`.
- **K-N2 (C chạy lại có ngữ cảnh):** trích dẫn trỏ **sai** (mượn đoạn của đối tượng khác; dòng bác tiền đề 0 / 20 đoạn) ⇒ A 18:27 03/11/2026: tính nghiêm ⇒ sàn Q5 phạm ⇒ cờ nhớ không bật (plan §4). `KET_QUA_C146.md` `0be2f074fba3`. **User chọn 18:27 03/11/2026 — "Sửa trên bộ mới rồi bật"**: merge B3 (code + giao diện) với `nho_hoi_thoai: false`; vòng sửa **B3b** — C viết bộ chuỗi **mới** nhắm lỗi này (B không mở), B sửa `ASSISTANT_HISTORY_NOTE` (chỉ đường có lịch sử), C chạy bộ mới; đạt ⇒ bật. **Trần B3 nâng 0,40 ⇒ 0,50 USD** (User, cùng lựa chọn); dừng > 0,47.
- **C147 review sớm 2** `10ec9a2..b156f92`: 0 blocker / 0 major / 1 minor (m-3 report theo quyết định kín) — `b136_review.md` "Vòng sớm 2" `c0c7f5a12d04`. Q10 B đạt; câu gợi ý đổi (`b156f92`).
- **B5 — User chọn (18:15 03/11/2026):** Quyết 1 = gán 07h00–17h30 **chỉ cho điểm có tên trong file vé** (trích file vé + dòng "có thể đã thay đổi"; điểm khác "kho không ghi giờ"); Quyết 2 = 2 điểm phía nam xa giữ, **chỉ xếp khi ở ≥ 3 ngày hoặc người dùng hỏi** (Thác Nhị Hồ nhắc đóng mùa mưa lũ). Quyết 3 (thời lượng) đang hỏi.
- **B3 merge `a3dabba`** (A 18:38; cổng trên `main` đạt; 5 chỗ báo cáo `9b97ce0`). Nhánh `p9-b3` đã merge ⇒ đề xuất xoá lúc kết phiên.
- **B138 (B):** nhánh `p9-b3b` từ `main`, sửa `ASSISTANT_HISTORY_NOTE` (PA1), đo đã thấy 25 (Q3 6/6, Q4 CI > 0, Q5 0/0, Q6 tụt ≤ 1, Q1 giống byte) ⇒ commit ⇒ báo C.
- **C148 xong:** bộ mới `data/phase_9/bo_do_b3b/` (12 chuỗi / 25 lượt; `chuoi_moi.jsonl` md5 `0f2360466366`, README `cc1b1a707a52`); luật S1 (0 lượt nho trả lời bằng nguồn sai đối tượng), S2 (từ chối nhầm nho ≤ doc_lap + 1); nhãn e (suy luận từ đoạn đúng đối tượng) theo dõi — suy luận không được đoạn đỡ ⇒ tính PHẠM (A). C chạy ở commit B3b.
- **B138 vòng 1** (`p9-b3b` `1ed7b34`, `ASSISTANT_HISTORY_NOTE` `64e347d5df58`): đã thấy Q3 6/6, Q5 0/0, Q6 tụt 0, Q1 giống byte — **Q4 không đạt** +0,50 [−0,15; +1,20] (B3: +0,65 [+0,15; +1,25]); ca dò 9 chuỗi không tái hiện K-N2. A 18:46 03/11/2026: **(a) đường âm ghi trước** — `nho_cau_tra_loi: false` + câu dặn mới, một lần; trần cứng B3 0,50 (cho vượt mức dừng 0,47). Đạt ⇒ C chạy bộ mới; không ⇒ cờ tắt, B3b âm, trình User. Tiền B3 ≈ 0,385.
- **B138 (a) đạt** (18:55 03/11/2026; `p9-b3b` `57f0e0b`, `nho_cau_tra_loi: false`, `settings.yaml` `b730b7af41a0`, câu dặn `64e347d5df58`): đã thấy Q3 6/6 · Q4 +0,80 [+0,25; +1,50] · Q5 0/0 · Q6 tụt 0 · Q1 không đổi. Tiền B3 ≈ 0,446 / 0,50. Chưa đo loại "ý bạn vừa nói" (không nhớ câu trả lời). ⇒ C chạy bộ mới S1 / S2 trên `57f0e0b`.
- **C149 xong:** nháp plan B5 `docs/superpowers/plans/2026-11-03-phase-9-b5-plan.md` sha `42afc1c7bc64` — **nháp**, chốt sau khi plan B4 duyệt (B5 dùng 4 trường của B4); B review sau B3b.
- **C150 xong** (`data/phase_9/toc_do/c150_phan_tich.md` `db2cab1d821c`, 0 USD): chữ đầu tro_ly_hue — định tuyến p50 1,50 s (≈ 46 %), tìm 27 ms, TTFT trợ lý ~1,73 s (RAG 1–8 1,18); router có token suy luận ~100 % lần, code không đặt mức suy luận (A kiểm `generator_openai_full_corpus.py:244–250`); `cached_tokens` = 0 chỉ ở định tuyến + lần trả lời đầu. Phương án: #1 suy luận thấp cho router (≈ −0,35 s), #6 chạy trước lần trả lời song song định tuyến (≈ chữ đầu 1,8 s), #4 gộp (User quyết), #2 / #5 lợi ≈ 0. Bẫy: `latency_ms` dòng harness không gồm định tuyến.
- **C152 (C):** chạy bộ mới B3b trên `57f0e0b` (nho + doc_lap, bỏ tran; mốc dừng B3 0,49, trần cứng 0,50).
- **C152 kết quả:** bộ mới trên `57f0e0b` — S1 đạt (nho từ chối chuẩn 6/6 lượt thiếu; doc_lap dính bẫy 3/6), S2 đạt (từ chối nhầm nho 0/19 ↔ doc_lap 5/19); tiền B3 ≈ 0,466 / 0,50. **A 19:03 03/11/2026: bật nhớ** (User: "đạt ⇒ bật") ⇒ **B141** bật `nho_hoi_thoai: true` + cổng nhỏ (sau B139, trước B140) ⇒ C review delta ⇒ A merge.
- **B139 (B):** review plan tốc độ C151 ⇒ `…-toc-do-dinh-tuyen-plan_review.md`. **B140 (B):** nháp plan B4 `docs/superpowers/plans/2026-11-03-phase-9-b4-plan.md` (review C).
- **Plan tốc độ định tuyến DUYỆT bản `3c5f1bbd3407`** (A 19:22 03/11/2026; review B139 vòng 2 ready `9ea511db2ee6`; m-5 ⇒ A nới **trần 0,065 / dừng 0,062 USD**). C chạy: phần định tuyến (không đo latency) được chạy khi B142 chạy; phần đo chữ đầu chỉ khi không session nào chạy server / Playwright / lượt có phí (W31).
- **B3b merge `9e2ecd9`** (A 19:22 03/11/2026): nhớ hội thoại BẬT (chỉ nhớ câu hỏi); cổng trên `main` đạt (2 lượt cookie, lịch sử 0→1, grep 0). Nhánh `p9-b3b` đã merge ⇒ đề xuất xoá lúc kết phiên.
- **User chọn (19:27 03/11/2026):** B6 — câu ngoài phạm vi Huế **giữ từ chối + nút gợi ý**, web chỉ cho câu về Huế mà kho không có. User nêu ca "phở Hà Nội **ở Huế**": A probe thật — "phở Hà Nội ở đâu ngon" ⇒ `ngoai_pham_vi` (đúng); "ở Huế có quán phở Hà Nội nào ngon" ⇒ `tro_ly_hue`, `tim_kho` × 3, từ chối chuẩn, ~8 s ⇒ **đưa vào bộ đo B6** (đúng loại web phải xử lý) + bộ tuyến. Câu từ chối sau 3 lần tìm chờ ~8 s — ứng viên tốc độ sau.
- **Plan B4 bản 1** (B140 `a6d4140690d9`): review C `…b4-plan_review.md` `9ff89cab1b1d` changes_requested 0B / 2M / 5m; A quyết: chỉ `so_ngay` bắt buộc giữ (+ đếm model hỏi trường không bắt buộc nếu rẻ); "trả lời tạm" không làm ở B4 (đo tỉ lệ "Trả lời luôn"; ứng viên sau B5). Trần B4 0,12. B sửa sau B142.
- **User (20:31):** thời tiết = **bậc nhỏ B5b sau B5**; "bạn tự điều phối, nghiên cứu, phát triển" (User đi nghỉ).
- **Plan B4 bản 2 DUYỆT `42fa62d2425f`** (A 20:31 03/11/2026; review C155 vòng 2 ready `8517a548a565`). A quyết: Lệch Q6 chấp nhận (bộ không có đáp án mẫu ⇒ thước an toàn: 0 ý trái + 0 ý không nguồn về giá / giờ / điều kiện ở lượt ghép); Q-a giữ (đo "hỏi thừa"; ≥ 3/10 ⇒ cắt); Q-b không trả lời tạm ở B4. Trần 0,12. C làm `chon_da_thay.json` + nhãn `can_hoi_lai` trước; B mở `p9-b4` sau merge B142.
- **AN TOÀN — kc08 (C156 phát hiện, 20:31 03/11/2026):** câu khẩn cấp tự viết "bị giật túi xách có hộ chiếu…, báo công an ở đâu" ⇒ định tuyến `tro_ly_hue` cả 2 lượt trên `main` (lỗ hổng chưa đo — bộ 10 câu bước 0 chưa từng qua bộ định tuyến B1); 23 / 24 câu khẩn cấp khác đúng. A chọn (a): **sửa trước**, thí nghiệm tốc độ dừng tới khi có mốc sạch ⇒ B143.
- **C153 (C):** code + chạy thí nghiệm tốc độ #1 — **DỪNG ở mốc** (luật m-1: mốc phạm K); code cờ `4c6adc6` trên `p9-toc-do-1` (probe: `none` nhận, 0 token suy luận). Chạy tiếp sau B143.
- (cũ) C153: (nhánh `p9-toc-do-1`); review code: B sau B142.
- **B142 (B):** nút 👍 / 👎 (chỉ lưu đánh giá, User chọn) + nút gợi ý dưới câu ngoài phạm vi (User chọn) — nhánh `p9-phan-hoi`; review C.
- **C151 (C):** plan ngắn thí nghiệm #1 `docs/superpowers/plans/2026-11-03-phase-9-toc-do-dinh-tuyen-plan.md` — sàn 0 câu khẩn cấp đi tuyến khác; chạy sau B3b (W31), review B. **C: bản 1 XONG 18:55 03/11/2026, sha `eac748b06972`** (47 dòng; mốc dùng lại B1 P1 r1 / r2; ước ≈ 0,055 ⇒ Golden 176 chỉ chạy sau 123 câu rủi ro đạt, dừng > 0,045).
- **C152 (C) — trạng thái:** XONG 19:03 03/11/2026: bộ B3b trên `p9-b3b` `57f0e0b` (nho + doc_lap) — S1 0 / 6, S2 nho 0 ↔ doc_lap 5 ⇒ đạt; 0,0203 USD (B3 ≈ 0,466); private `data/phase_9/b3b/chuoi_moi_c152/KET_QUA_C152.md` `ea5be7210723`.
- **Nghiên cứu sản phẩm thật (User yêu cầu trong phiên tối, tin không có dấu giờ):** Codex `data/tra_cuu_cli/2026-11-03_tinh-nang-the-gioi/` (8 lượt tìm, 0 trang mở ⇒ A WebFetch kiểm 3 nguồn: Tokyo EDO, HelloBC, Beach.com — đúng); agent con A thử TRIPO vòng 2 ⇒ `data/nghien_cuu_tinh_nang_2026-11-03/tripo_v2/` (đang chạy).
- Không có lượt đo latency trong lúc này (W31 không chặn). B báo A trước khi đo latency ở Q10.

## Session

**Phiên tối 03/11 (mở 17:56):** A `hue-rag-9e` · B `hue-rag-32` · C `hue-rag-40` — cả ba Claude Code, trực tiếp.

**Phiên 03/11 (mở 08:36, kết 13:26 03/11/2026):** A `hue-rag-5e` · B `hue-rag-52` · C `hue-rag-d8` — cả ba Claude Code, trực tiếp. B: B131 hoàn tất B1, B132 plan B2, B134 code B2, B135 plan B3, B136 code B3 (≈ 0,513 USD). C: C133 bộ đo B2, C134 review B1, C135 review plan B2, C136 bộ đo B3, C137 / C141 review B2, C138 câu hai ý, C139 thời tiết, C140 mẫu giao diện, C142 review plan B3, C143 bộ đo B4 + chi phí, C144 bảng điểm B5, C145 review sớm B3 (≈ 0,0006 USD). A: điều phối, merge B1 + B2, 5 chỗ báo cáo × 2, README repo, báo cáo cho giáo viên, vòng cải tiến 16.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C lúc mở phiên sau: không việc đang chạy ⇒ kiểm nhanh ⇒ báo A ⇒ chờ.

## Quyền

- **User 18:05 (A ghi nhận 18:05 03/11/2026):** "tiếp tục điều phối, phát triển, tự nghiên cứu, so sánh, tối ưu, đánh giá, viết báo cáo"; **kết phiên ~22:10** ⇒ A bắt đầu kết phiên ~21:40.
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
