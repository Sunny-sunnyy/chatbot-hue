# CURRENT_HANDOFF — việc đang mở của A/B/C/E

Cập nhật: 19:19 05/11/2026 (A, **mở phiên tối 05/11** — viết lại mục "PHIÊN SAU" mà kết phiên 16:49 bỏ dở; máy khởi động lại 19:12 ⇒ mọi worktree `/tmp` mất).
Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở. Phiên 05/11 sáng–chiều nguyên văn (việc giao, quyết định theo giờ): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05.md`; 04/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-04.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-05_b4_am_chia_phase_10_12.md`.

## PHIÊN SAU ĐỌC TRƯỚC (đọc trước nhất)

**Hệ thống (`main` = `origin/main`):** RAG 1–8 + trợ lý Phase 9: định tuyến 4 tuyến (trò chuyện / trợ lý Huế / ngoài phạm vi / khẩn cấp, dòng mở PA1) + dòng "có thể đã thay đổi" + tìm thêm `tim_kho` ≤ 2 lần + nhớ câu hỏi 3 lượt + câu dặn hẹp + giao diện nhiều lượt + 👍 / 👎 + **trả lời song song định tuyến #6 (BẬT `5a8aa5e`)** + hỏi lại do code / thẻ nút (`hoi_lai: false`) + **B5 lịch trình (`lich_trinh: false` — chờ User chấm Q3)**. `frontend/dist/` không commit ⇒ `cd frontend && npm ci && npm run build`. Kho 204 file / 8.424 đoạn (build 30/10); Golden md5 `6331e88fb171`; T1 `4d5bbe9e0edc`. Qdrant chạy bằng Docker Desktop.

**Phase 9** — spec bản 12 `77250689e605`. Bậc: B0–B3b ✓ · B4 / B4b âm ⇒ code vào cờ tắt `b019aab` ✓ · **B5** merge `d66f6a3` cờ tắt (chờ User chấm 5 lịch kín) · **B5c** âm 2 vòng ⇒ dừng, tag `hoso/p9-b5c` (hướng sau nếu làm lại: code nối điều kiện miễn giảm từ bảng vé vào kết quả công cụ) · **sửa lịch nhiều lượt** (plan `5b68f3cb666a`, trần 0,20 / dừng 0,19; code B163 `p9-sua-lich` `1c53627` cờ tắt, 0 USD, chưa đo, chưa report) · **B5b** thời tiết (plan `cc09fda9f634`, trần 0,07; cần User duyệt bảng v4; code sau sửa lịch) · **B6** web (plan bản 2 `b6a046e944c0` chờ B review; trần 0,22) · B7 đóng gói (quỹ 0,35). Tiền Phase ≈ **1,61 / 2,5 USD** (trần nâng tối 05/11), dự phóng ≈ 2,4.

**Phase 10 (song song)** — ảnh: spec bản 2 `bf67b90fb6fc`; A1 đạt; A2 P1 luna âm ⇒ User giữ **v1 dạng gợi ý có xác nhận**; code nhánh `p10-anh` **`0632e10`** (đã push tối 05/11, từ patch `9138ca6b1fc3`; 40 test); giao diện chưa Playwright. **E9** SigLIP 2 (User cho tải + collection ảnh mới): tiêu chí ghi trước `data/phase_10/anh/e9/tieu_chi_ghi_truoc.md` `a8524989f221`, model đã tải, ảnh mẫu ~179 ảnh / 34 tên, chưa embed, chưa tạo collection. Giọng nói E1 tạm dừng. Tiền Phase 10 ≈ 0,0785 / 0,15.

**Phase 11 / 12:** backlog (lưu trú — khu nên ở + link Maps; bản đồ toạ độ 17 / 28 điểm `data/phase_9/lich_trinh/diem_toa_do.json`; dữ liệu mở `data/nguon_mo_huegov_2026-08-05/`) · Phase 12 vận hành + **deploy AWS = điều kiện đóng code**; đóng code chỉ khi User nói (dự kiến 25–30/12).

**Nhánh:** `main`; còn mở: `p9-sua-lich` (B163), `p10-anh` (local, chưa commit phần mới), `p9-b5c` (hồ sơ, đã tag). Đã merge ⇒ chờ User xoá: `p9-b4`, `p9-b5`, `p9-toc-do-6`, `p9-toc-do-6b`. Worktree `/tmp/*` prunable (máy khởi động lại) ⇒ `git worktree prune` rồi tạo lại khi cần. 4 worktree AGY cũ `c725987` (User quyết).

**Mã hay gặp:** B0–B7 = bậc Phase 9; Q… / D… / m-… = câu đo / quyết định / finding minor; S-AT = thủ tục sinh lại câu an toàn 3 + 3 lần; S20, S10… = câu bộ an toàn 32 (private); Bxx / Cxx / Exx = việc A giao B / C / E; S / W / I = sổ `SO_CAI_TIEN_CACH_LAM.md`; #1–#18 = ý từ nghiên cứu 04/11 (bảng dưới).

## PHIÊN TỐI 05/11 — VIỆC ĐANG GIAO (A ghi 19:19 05/11/2026)

Lệch phát hiện lúc mở: (1) kết phiên 16:49 chỉ chép handoff sang archive, chưa viết lại mục "PHIÊN SAU" (STATUS_A ghi đã viết) ⇒ A viết lại lúc này; tài liệu kết phiên chưa commit ⇒ A commit. (2) Máy khởi động lại 19:12 ⇒ mọi worktree `/tmp` mất. (3) Lệnh sửa kho thật ở `data/sua_kho_2026-11-05_gio/tools/chay.sh` `eb101131f146` (không phải `/tmp/c192/…`); backend không đổi từ `5a8aa5e` (A kiểm `git diff 5a8aa5e..main -- backend` rỗng) ⇒ bước 0 của lệnh vẫn qua. (4) Nhật ký 05/11 dừng ở 13:02 ⇒ A cập nhật.

- **C192 — sửa kho giờ mở cửa 11 điểm (C):** chờ User gõ ở **terminal C** `! bash data/sua_kho_2026-11-05_gio/tools/chay.sh`. **Trong lúc dựng lại chỉ mục:** không session nào chạy server, lượt có phí, việc nặng CPU / RAM, hay đọc Qdrant. Xong ⇒ C chạy bộ "sau" (Golden 11 + an toàn 10 + 1 câu thật + judge, ≈ 0,011 USD), T1 mới, report ⇒ báo A (A cập nhật 3 chỗ báo cáo + `Project_Status` §4 build record / T1).
  - **C (C192 chờ A quyết, 19:58 05/11/2026):** chỉ mục dựng lại 19:44 — **8.435 point**, record `9921888f2030`, sparse `4a8311a2dfef`, T1 `64656a87c109`. T1 ĐẠT (148 / 158 giống hệt, 10 đổi đều chạm, macro giống 4 chữ số) · an toàn 10 ĐẠT (0 lỗi mới, 2 judge) · câu thật ĐẠT · **Golden 11: phạm sàn ở lượt 1 — case 67 từ chối (5/5 ⇒ 1/1); chạy lại ×2 đều 5/5** ⇒ A quyết giữ (C đề xuất) / lùi. 0,0236 / 0,03 USD. Report `report_agent/2026-11-05_sua_kho_gio/c192_implementation.md` `e794280e8373`.
- **B164 — B163 phần 0 USD (B):** prune + tạo lại `/tmp/b_sualich` từ `p9-sua-lich` `1c53627` (symlink `data/`, `knowledge-base-hue/`); test file chạm; Q1 cờ tắt giống byte `main` (228); viết report `report_agent/2026-11-02_phase_9_code/b163_sua_lich_implementation.md` (phần đã làm, phần chưa đo); cập nhật `STATUS_B.md`. Lượt có phí của sửa lịch **chỉ sau khi `lich_trinh` bật** (User chấm Q3). Không chạy server khi C192 đang dựng chỉ mục. Xong ⇒ **B review plan B6 bản 2** `b6a046e944c0` (≤ 2 vòng, `…b6-plan_review.md`).
  **B (19:29 05/11/2026):** B164 phần không cần Qdrant xong — worktree tạo lại; 72 test thuần qua; `xep` nhánh ↔ `main` giống 12.528 / 12.528 tổ hợp; report `b163_sua_lich_implementation.md` `3bd667c398b1`. **Sau C192 (19:50 05/11/2026): Q1 228 / 228 giống byte · Q1m 228 / 228 · 165 test passed · build xong ⇒ B164 phần 0 USD XONG**; lượt có phí chờ `lich_trinh` bật. **Review B6 vòng 1: changes_requested** 0 / 1 / 5 (`2026-11-05-phase-9-b6-plan_review.md` `96f198855a9d`; M-1 cách tính "mức tụt ≤ 2 %" của Q4 — A chốt). **Vòng 2 (19:33 05/11/2026): ready** trên bản 3 `6e5c3b21065d` — M-1 + m-1…m-5 đóng, B rút ý mã băm của m-5 (C đúng); review `7bb1c21aff9c` ⇒ A duyệt.
- **E10 XONG (19:29 05/11/2026):** `p10-anh` `0632e10` pushed, 40 passed. **Tiếp (E):** prune + tạo lại `/tmp/e_anh` nhánh `p10-anh` từ `268466d`, `git apply` patch, test `test_p10_anh.py` + `test_assistant_boundary.py`; commit + push nhánh `p10-anh` (quyền phiên: B / C / E push nhánh riêng — auto mode chặn ⇒ User xác nhận ở terminal E). Sau C192: Playwright giao diện P1 (cờ bật tạm, 0 USD) ⇒ báo A ⇒ A giao review cả nhánh. Sau đó **E9** (embed SigLIP 2 + collection ảnh mới — việc nặng, **không chạy cùng C192**).
- **A chốt M-1 review B6 (19:30 05/11/2026):** bỏ vế "mức tụt ≤ 2 %" của Q4 (không có mẫu số) ⇒ "từ chối nhầm ≤ mốc + 1" như spec §4; USD / câu đường web chỉ báo riêng (theo dõi, sàn 0,0005 là trung bình). **C** viết plan B6 bản 3 ⇒ B kiểm phần sửa (vòng 2, cuối) ⇒ A duyệt sha.
- **A duyệt plan B6 bản 3 sha `6e5c3b21065d` (19:34 05/11/2026, tính từ file; review B vòng 2 ready `7bb1c21aff9c`)** — trần 0,22 / dừng 0,21, bộ kín có. **B165:** code B6 phần 0 USD trên nhánh mới `p9-b6` từ `main` (worktree riêng); lượt có phí chỉ sau C192 xong; sửa lịch vẫn đi trước khi `lich_trinh` bật.
  **B (19:54 05/11/2026): B165 phần 0 USD XONG** — `p9-b6` `d7ec216` (đã push; code `7873e0f` + sửa lỗi thật test bắt: bản cờ của #6 `replace(router=False)` ném lỗi khi `tra_web` bật ⇒ tắt luôn `tra_web` ở bản đó); 51 test B6 + 216 cùng file chạm; build; **Q1 228 / 228 giống byte `main`, Q1m 228 / 228** (không khoá Serper). Report `b165_b6_implementation.md`. **Đã thấy ×2 (20:35 05/11/2026):** Q3 8 / 10 đạt; Q2 code 0 / 60; Q2 judge phạm (X04 cúp điện, X05 lũ) ⇒ vòng 1 code (A quyết) `cedac73` ⇒ chạy lại judge 0 / 7 đạt; Q1 / Q1m 228 / 228. **KHOÁ `cedac73`** (`TU_WEB_LUAT` `e5f516aa383e`). **Q4 ĐẠT** (từ chối nhầm 0 ≤ 2, F1/F3/F4 sạch, S-OOS 0 / 11) · **Q8 ĐẠT** (API + Playwright, CSP 0, 0 request ngoài). Tiền B6 ≈ 0,144 / 0,22. Kế: C kín ×2 (C203) ⇒ review nhánh ⇒ rebase + Q1 trước merge.
- **C192 dựng chỉ mục XONG (19:44, User `!`; A kiểm 19:45 05/11/2026: 8.435 point):** build record `9921888f2030` (cũ `51fb1ec63cbc`), sparse `4a8311a2dfef` (cũ `c8134c49a648`), T1 sau `64656a87c109`. Hết giai đoạn cấm. C đang so T1 + bộ "sau" (≈ 0,011) ⇒ report ⇒ A sửa `BAO_CAO_KHO_DU_LIEU.md`, nhật ký, README, `Project_Status` §4. B chạy Q1 B164; E Playwright P1; E9 embed sau khi RAM rảnh.
- **B164 XONG** (0 USD): Q1 228 / 228 giống byte `main` (chỉ mục mới), Q1m 228 / 228, 165 test, build; report `b163_sua_lich_implementation.md` §4. Lượt có phí chờ `lich_trinh` bật. **B165** code B6 `p9-b6` `7873e0f` (cục bộ), 48 test thuần.
- **E Playwright P1 ĐẠT** (`p10-anh` `0632e10`, server thật; 0,001634 USD; Phase 10 ≈ 0,0802 / 0,15) ⇒ **C198** review cả nhánh `p10-anh` sau report C192 (`report_agent/2026-11-05_phase_10_anh/e8_review.md`); **E9** embed SigLIP 2 + collection `hue_anh_siglip2` + đo theo tiêu chí `a8524989f221` (A giao 19:51 05/11/2026).
- **User GIỮ sửa kho C192 (20:07 05/11/2026)** (1 câu Golden case 67 phạm sàn lượt 1, chạy lại 2 / 2 đạt ⇒ theo dõi). A sửa báo cáo khâu kho / chia đoạn / Qdrant / từ khoá / tìm / LUONG bản 29 / nền tảng / sinh câu + `Project_Status` §4. **C199** bộ B6 giữ nhãn ⇒ B chạy đã thấy ×2. **C198** review `p10-anh` ready 0 / 0 / 3 (`e8_review.md` `67d64f39b829`) ⇒ E sửa m-1, m-2 ⇒ A merge cờ tắt. Bộ sửa lịch đã thấy 10 / 10 trên `1c53627`; kín chờ User `!` ở terminal C (lệnh trong `STATUS_C.md`; K-S2 thẻ rỗng — A xét khi có số). Kín B6 kiểm nhãn: chờ User `!` ở terminal C.
- **MERGE `p10-anh` `2ca9937` (20:10 05/11/2026, cờ `anh.bat: false`; C198 ready + m-1 / m-2 sửa `973823f`):** cổng A: test 43 passed (3 file), `npm ci && npm run build`, `/` 200, `/health` 5 / 5, `/api/anh/ung_vien` 404, câu trong kho (giờ mở cửa lăng — trả giờ mới có [1]) + câu ngoài phạm vi đúng, `chat_metrics` 2 / 2, câu hỏi trong log 0; ≈ 0,0004 USD. m-3 (Host / DNS rebinding, trần yêu cầu ảnh đồng thời) ⇒ Phase 12. **E** viết `bao_cao_he_thong/BAO_CAO_HOI_BANG_ANH.md` sau khi có kết quả E9 (A review). Nhánh `p10-anh` đã merge ⇒ chờ User xoá.
- **C200** phân tích nhiễu S-AT (`data/phase_9/s_at_nhieu/c200_phan_tich.md`, 0 USD) ⇒ **User duyệt luật S-AT mới (20:14 05/11/2026)** — áp cho B6 Q4, sửa lịch và mọi lượt sau. **C199** kín B6 giữ nhãn (User `!`); bộ B6 sẵn.
- **Kín sửa lịch mô phỏng (User `!`)** trên `1c53627`: 4 / 5 đạt; K-S2 thẻ "chọn điểm thay" rỗng (chỉ nút Bỏ). **A chốt (20:15 05/11/2026): lỗi** ⇒ **B166** (sau lượt B6 đang chạy): hết điểm thay ⇒ khối "Không đổi được" câu cố định, không thẻ; test; mô phỏng đã thấy bỏ luật "thẻ rỗng = Bỏ"; rebase lên `main` + Q1 / Q1m ⇒ C chạy lại kín mô phỏng (User `!`). **C rảnh** tới khi B166 xong (không còn việc 0 USD không chồng file).
- **B6 đã thấy ×2** (`p9-b6`; ≈ 0,0855 / 0,22): Q3 8 / 10 pass^2 ĐẠT; sàn code Q2 0 / 60; **sàn judge Q2 PHẠM** (2 câu × 2 lần khẳng định chưa xác minh: cúp điện tuần này nêu khu / ngày giờ; mức lũ năm nay đưa số mét — câu an toàn). **A quyết vòng chỉnh 1 (20:20 05/11/2026) = luật code:** thiên tai ⇒ không chữ web do model viết, câu cố định kiểu B5b (NCHMF / chính quyền / 112) + link sổ; thời gian thực ⇒ mục web 0 số + 0 ngày giờ, hỏng ⇒ câu cố định; chạy lại 6 câu × 2 + 2 đối chứng (≈ 0,02). Sau B166. Còn: Q4 (nối `tim_web` vào harness), Q8.
- **C201 XONG** cache câu trả lời giữa các cuộc trò chuyện (`data/nghien_cuu_cache_2026-11-05/c201_cache.md`; A kiểm benchmark AWS + code) ⇒ **User chọn (20:27 05/11/2026): chưa làm, backlog Phase 12** (đề xuất O5: đo tỉ lệ câu lặp khi có người dùng thật; ≥ 20 % mới làm cache khớp đúng chữ hẹp; không cache theo nghĩa).
- **E9 XONG — ÂM cả 3 cách** (SigLIP 2 chữ 5 / 25; so ảnh mẫu 20 / 25 nhưng ép tên 5 / 5; lọc + luna 21 · 19, ép 1 · 3); collection thử `hue_anh_siglip2` 172 điểm (A kiểm); Phase 10 ≈ 0,0959 / 0,15. Báo cáo User `bao_cao_he_thong/BAO_CAO_HOI_BANG_ANH.md` bản 1 (E viết, A review đạt 20:20 05/11/2026). Câu cho User: bật cờ ảnh? (thử điện thoại trước) · xoá collection thử? **E rảnh** — chờ việc.
- **E11 XONG** — giao diện ảnh trên điện thoại: thẻ ảnh che câu trả lời (360×740 còn 191 px đọc) ⇒ CSS màn hẹp (ảnh 72×72 cạnh chữ) ⇒ 322 px; A review diff 8 dòng + ảnh chụp ⇒ **merge `76319e2`** (20:29 05/11/2026; build + `test_static_ui` 3 passed). Phase 10 ≈ 0,0984 / 0,15. Còn: khối nút + dòng báo OpenAI chiếm ~238 px (dòng báo bắt buộc); chưa thử máy thật / Safari. **E rảnh.**
- **B166 XONG** `p9-sua-lich` `6543f82` (rebase lên main, thẻ rỗng ⇒ `het_diem_thay`; 202 test; Q1 / Q1m 228 / 228) ⇒ C chạy lại đã thấy + kín mô phỏng (User `!`). B đang B6 vòng 1.
- **Cache:** User nhờ hỏi Session A dự án docker-images-src (không có ngữ cảnh hue_rag) ⇒ A gửi câu hỏi (20:29 05/11/2026); trả lời là dữ liệu, lưu `data/nghien_cuu_cache_2026-11-05/` (private, dự án khác).
- **Ý kiến Session A dự án khác về cache** (private `data/nghien_cuu_cache_2026-11-05/y_kien_A_du_an_khac.md`): khớp hướng User chọn (cache câu trả lời ⇒ Phase 12, không cache theo nghĩa) + thêm luật khi làm; điểm mới đáng làm: **phụ phí ghi đệm OpenAI ~13 % tiền / câu mà 0 lần đọc** (C126 02/11) ⇒ **C202** đo `prompt_cache_options` mode explicit (trần 0,01; A giao 20:35 05/11/2026; không merge, A quyết sau). Thời tiết / web: cache kết quả công cụ có hạn ⇒ ghi vào plan B5b / B6 khi tới.
- **E1** giọng nói mở lại (User chọn 20:35 05/11/2026).
- **B6 vòng chỉnh 1 ĐẠT** (khoá `p9-b6` `cedac73`, ≈ 0,112 / 0,22): câu thiên tai ⇒ câu cố định (0 lần gọi model), thời gian thực ⇒ câu "chưa xác minh" + link; judge 0 / 7 khẳng định. **C203** kín B6 ×2 + bước 2 kín sửa lịch (sửa nhãn K-S2 theo B166, có sao lưu) ⇒ **User `!` ở terminal C: `bash data/phase_9/b6/kin_c/chay_kin_c203.sh`**. B làm Q4 + Q8 B6.
- **E1 giọng nói XONG** (`data/phase_10_nghien_cuu/giong_noi/nghien_cuu_mo_hinh.md` §8 nguồn; A WebFetch kiểm Gipformer card + VieNeu streaming.md). **User chọn (20:45 05/11/2026): thử NGHE trước, đọc sau** ⇒ **E12** viết phần giọng nói vào spec Phase 10 bản 3 (STT chạy máy, xin duyệt sherpa-onnx + ≤ 300 MB model, User thu 40 câu) ⇒ review ⇒ User duyệt sha.
- **Sửa lịch — phần 0 USD XONG (20:53 05/11/2026):** `p9-sua-lich` `6543f82` đã thấy 10 / 10, kín mô phỏng 5 / 5 (nhãn K-S2 sửa theo B166: md5 `34b20600ac00` ⇒ `daf762bcbbe5`, bản cũ `chuoi_sealed.truoc_B166.jsonl`). Lượt có phí khi `lich_trinh` bật.
- **B6:** Q4 ĐẠT (từ chối nhầm 0 ≤ 2; S-OOS 0 / 11), Q8 ĐẠT (server + Playwright); tiền ≈ 0,144 / 0,22; rebase ⇒ **`p9-b6` `9140152`** (code = khoá `cedac73`; 251 test; Q1 228). Giới hạn: địa chỉ / SĐT trong mục web chưa kiểm ⊂ đoạn trích (việc sau). **E13** review nhánh; kín C203 đang chấm judge.
- **E12 XONG:** spec Phase 10 bản 3 `bc246a4ba3d6` (giọng nói STT §8, gói duyệt §12 (7)–(10)) ⇒ **B167** review ⇒ User duyệt sha.
- **Kín B6 ×2 ĐẠT (C203):** 22 lượt 0 lỗi, Q2 judge 0 / 7, Q3 7 / 7; **chữ đầu mục web p50 13,4 s** (nêu khi xét bật); tiền B6 tổng ≈ 0,185 / 0,22.
- **B167** review spec Phase 10 bản 3 ⇒ changes_requested 0 / 1 / 6 (`d2c3b9560672`); **A chốt M-1 (20:57 05/11/2026):** WER thành theo dõi, quyết bằng tên riêng + số + tốc độ / RAM ⇒ E bản 4 sau E13 ⇒ B vòng 2. **B168** code B5b phần 0 USD (`p9-b5b` từ `main`).
- **User chọn bảng điểm v5 (20:57 05/11/2026)** = v4 + 5 điểm trong nhà (Bảo tàng Cổ vật Cung đình, Duyệt Thị Đường, Không gian Lê Bá Đảng, Bảo tàng Mỹ thuật, Bảo tàng Hồ Chí Minh) ⇒ **C204** soạn `diem_v5.json` + phiếu 5 dòng cho User (sau C202). B5 đo trên v3 ⇒ đổi bảng phải chạy lại kiểm 0 USD.
- **C (sau C192):** khi B163 có report ⇒ chạy lại `kiem_bo` / `mo_phong` bộ sửa lịch trên code B (đã thấy 10 + kín 5, chỉ số đếm).

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

## Câu hỏi cho User (hỏi mỗi lần một câu)

1. **(gấp nhất)** Chấm 5 lịch kín B5 — `data/phase_9/b5/kin/phieu_cham_user.md` (đạt ≥ 4 / 5 cả 3 tiêu chí ⇒ A bật `lich_trinh` ⇒ mở đường cho sửa lịch + B5b).
2. Gõ ở **terminal C**: `! bash data/phase_9/b6/kin_c/chay_kin_c203.sh` (kín B6 ×2 + bước 2 kín sửa lịch; chỉ in số đếm).
4. (User chọn v5 20:57 05/11/2026) Xem phiếu 5 điểm trong nhà mới khi C204 xong.
6. Xoá 4 nhánh đã merge `p9-b4`, `p9-b5`, `p9-toc-do-6`, `p9-toc-do-6b` (local + origin, User `!`).
7. Vòng cải tiến 19: gỡ W4 / W39 (Session D 0 buổi, hạn 07/11) — hay giữ để dùng D. (S-AT: User quyết 20:14 05/11/2026 — chênh đúng 1 ⇒ sinh thêm 3 + 3, âm khi tổng chênh ≥ 2 / 6; `skills/run-experiment/SKILL.md` §4.)
8. Không gấp: đọc 10 câu mẫu B4 / B6 (`data/phase_9/bo_do_b4/mau_cho_user.md`, `data/phase_9/bo_do_b6/mau_cho_user.md`); 4 worktree AGY cũ giữ hay gỡ; xoá sao lưu kho đợt 1 + 2?; báo cáo tiến độ cho giáo viên.

## Câu hỏi A còn nợ (không cần User)

- Link Google Maps của B5 đổi sang toạ độ cho 17 điểm có toạ độ (C197 đề xuất; mở kiểm bằng mắt trước) — A quyết khi bật B5.
- Cách đếm token (`_token_count`) không tính kết quả tìm thêm + mô tả công cụ ⇒ chênh tới ~900 token; ngữ cảnh đo 1,7–4k ≪ trần 16k ⇒ xem lại khi lời dặn / công cụ dài thêm.
- `prompt_cache_key`: lợi ≈ 0 hiện tại. Bảng sổ cải tiến: S41–S44 thiếu 1 cột. Log `FileHandler` không xoay vòng (deploy). Hạn mức OpenAI / Serper — đặt khi tới B6.
- B7: dự phòng demo khi mất mạng; đề cương nói "trợ lý RAG có công cụ"; ý #15–#17.
- Theo dõi: router đưa S20 sang `khan_cap`; định tuyến > 10 s ⇒ `tro_ly_hue`; `chat_feedback` chưa nối `chat_metrics`; câu từ chối sau 3 lần tìm ~8–12 s (file lăng không ghi giờ — C192 sửa phần giờ chung).

## Session

**Phiên tối 05/11 (mở 19:16):** A `hue-rag-4f` · B `hue-rag-4b` · C `hue-rag-3c` · E `hue-rag-bc` — cả bốn Claude Code, trực tiếp.

**Phiên 05/11 sáng–chiều (08:43–16:49):** A `hue-rag-b0` · B `hue-rag-48` · C `hue-rag-52` · E `hue-rag-7a`.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C / E lúc mở phiên sau: kiểm nhanh ⇒ báo A ⇒ chờ.

## Quyền

- **Phiên tối 05/11** (User chọn "như sáng 05/11", A ghi nhận 19:19 05/11/2026): A tự điều phối + tự quyết chi tiết trong plan đã duyệt; A tự commit / push cả phiên; ≤ 1 USD / phiên; B / C / E push nhánh riêng; trần Phase 9 **2,5** (nâng tối 05/11) — dự phóng vượt ⇒ A xin User **trước** lượt có phí. Hết hạn cuối phiên.
- **Phiên 05/11 sáng–chiều — HẾT HẠN 16:49 05/11/2026** (gồm "đừng dừng, không cần hỏi lại" + cho vượt trần khi vắng 12:59). Tiền phiên ≈ 0,49 USD (Phase 9 ≈ 0,41 · Phase 10 ≈ 0,08).
- **User (09:00 05/11/2026):** cần công cụ / nghiên cứu / tải / khoá mới ⇒ tự nghiên cứu (0 USD, thông tin công khai) + đề xuất; thêm công cụ / thư viện lớn / tải model / khoá / tài khoản mới vẫn trình User trước khi dùng (`Session_Prompt.md` §4). Đã duyệt: tải SigLIP 2 + collection Qdrant ảnh mới (11:42 05/11/2026).
- **Tiền Phase 9: trần nâng lên 2,5 USD** (User chọn, A ghi nhận 19:29 05/11/2026; trước 2,0 — "khi hết thì xin tôi" 08:55 05/11/2026 vẫn áp: dự phóng vượt 2,5 ⇒ xin trước). **Phase 10:** trần 0,15 (dừng 0,13).
- **Phase 9 (spec, không hết hạn theo phiên):** Serper dùng luôn (User chấp nhận rủi ro điều khoản); gói npm giao diện như đã duyệt 02/11; dữ liệu công khai dùng cho học tập, không kiểm giấy phép (05/11).
- **Thường trực:** A commit / push — hỏi User trước (luật chung), rồi A tự chạy; chỉ khi bị chặn / lỗi mới đưa `!` (`WORKFLOW.md` §9.6); B / C / E không commit trừ khi việc ghi rõ; duyệt cho A = duyệt cho B / C / E; thư viện nhỏ cần cho việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage + tiền; code luôn `uv run`.
- **Tra web:** `scripts/tra_web_codex.sh` (chỉ thông tin công khai); **không bao giờ gọi `agy`**. Khoá `SERPER_API_KEY` trong `.env` (không đọc / in).
- Giá `gpt-6-luna` (User 30/10): vào 0,10 · ra 0,50 · đọc đệm 0,01 · ghi đệm 30 phút 0,125 USD / 1M. Serper: 0,001 USD / lượt.

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

- Phiên 05/11 sáng–chiều nguyên văn (C173–C197, B156–B163, E1–E8, quyết định theo giờ, merge B4b / B5 / #6, B5c âm): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05.md`.
- Phiên 04/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-04.md`; 03/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-03.md`, `…_2026-11-03_toi.md`; 02/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-02.md`.
- Giao diện mới: `report_agent/2026-11-02_giao_dien_moi_code/`. Nghiên cứu Phase 9: `report_agent/2026-11-01_nghien_cuu_phase_9/` + `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md`.
- Streaming + đo cuối Phase 1–8: `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`. Phase 8.2: `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
