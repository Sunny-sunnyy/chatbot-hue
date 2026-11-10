# CURRENT_HANDOFF — việc đang mở của A/B/C/E

Cập nhật: 12:50 08/11/2026 (A, kết phiên 08/11). Trước: 15:43 07/11/2026 (A, **trước khi User mở lại cả 4 session để reset context — giữa phiên 07/11, chưa kết phiên**). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở.
Nguyên văn phần đầu phiên 07/11 (11:53 → 15:43 07/11/2026): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-07.md`; 06/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-06.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-07_cong_dot_1_tu_soi.md`.

## PHIÊN SAU ĐỌC TRƯỚC (viết lại 12:50 08/11/2026, kết phiên 08/11)

**Phiên 08/11 đã kết** (User: "để các nhiệm vụ, câu hỏi ở session tiếp theo"; User dặn tắt Qdrant bằng `docker compose down`; lúc 12:52 08/11/2026 A chạy thì **Docker không kết nối được** (`/var/run/docker.sock` không có, lệnh `docker` báo lỗi SIGBUS) và Qdrant `127.0.0.1:6335` đã không trả lời ⇒ có vẻ Docker Desktop đã tắt trước đó; **chưa xác nhận được trạng thái container** ⇒ phiên sau: User bật Docker Desktop, `docker compose ps` (nếu còn container cũ thì `docker compose down`), rồi `docker compose up -d qdrant`). Quyền phiên 08/11 **hết hạn** ⇒ A mới hỏi lại User một câu. Nguyên văn phần đầu phiên: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-08.md`. Tổng hợp đợt: `report_agent/2026-11-08_phase_9_ban_13/TONG_HOP.md`; nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-08_pham_vi_dong_goi.md`.

**Hệ thống (`main` = `origin/main`):** như 07/11 + từ 08/11: 7 ảnh cổng · **hỏi bằng ảnh BẬT** (`anh.bat: true`) · bản đồ lịch trình (cờ `ban_do_lich` TẮT) · 14 việc nhỏ (nút Dừng, ô 500 ký tự, gợi ý dưới câu từ chối, Nguồn gộp theo bài, sao chép / tải lịch, thẻ Khám phá, nút báo sai `/api/bao_sai`, ảnh điện thoại, kiểm số mục web ⊂ đoạn trích, `turn_id` trong `chat_metrics`) · README đúng hiện trạng. Định tuyến vẫn 4 tuyến (G chưa merge).
**Quyết định User 08/11 (giờ ở archive / TONG_HOP):** chưa deploy tới khi đủ tính năng + đóng gói + Docker; phạm vi trước đóng gói = bản đồ + ảnh + giọng nói + Nhóm 1 + 2; **spec Phase 9 bản 13 duyệt `5557f0fd7650`** (cổng 2 nhóm, bỏ khẩn cấp, ngoài phạm vi ⇒ agent từ chối; 4 công cụ T1–T4; T2 = agent chỉ quyết lúc tra); trần Phase 9 **3,5**; bỏ mốc ngày; **mức nhẹ cho việc nhỏ** + **5 cách giảm thời gian test** (Session_Prompt §7–§8, WORKFLOW §6); mức dừng G 0,75 + chỉnh lời dặn nhiều vòng; T3 vòng 3.
**Tiền 08/11:** ≈ 0,99 USD (B G ≈ 0,75 + bản đồ / việc nhỏ / review ≈ 0,011 · E ≈ 0,128 · C ≈ 0,096 · A ≈ 0,003). Phase 9 ≈ 3,0 / 3,5 (≈ 2,02 trước 08/11 + ≈ 0,98 hôm nay; số cộng từ report, chưa đối chiếu log tổng) — quỹ B7 0,35 giữ riêng ⇒ còn ≈ 0,15 cho việc mới ⇒ **lượt kín G + S5 + đợt 2 cần User nâng trần**. Phase 10 ≈ 0,107 / 0,15.

### Phiên 09/11 — quyết định + trạng thái (cập nhật 20:50 09/11/2026)
- **User:** quyền như 08/11; trần Phase 9 **4,0**; ưu tiên tốc độ, bỏ test không cần, 4 session tự bàn; "cắt giảm nhưng vẫn đảm bảo chất lượng"; khẩn cấp sau G đóng; **G S2b 1/20 (câu ngoài phạm vi ⇒ mục web) nhận là giới hạn đã biết**; **T3 đóng hồ sơ, không merge** (lợi đo được ≈ 0).
- **Vòng tự soi (A chốt):** S5 đo **một lượt chung trên `main`** lúc đóng đợt (bỏ S5 từng nhánh); T1 lượt sau G: an toàn ×1 + 1 người chấm + `kiem_l2`; chấm lại khi sinh lại chỉ câu sinh lại (đối chứng ở lượt chính); T2 sàn = S1 + ngoài kho / ngoài phạm vi + đúng câu (S5 / S6 lúc đóng đợt); giữ: 2 judge + đối chứng lượt chính, test rộng 1 lần, cổng ổn định 1 + 1, kín cho lời dặn chỉnh nhiều vòng.
- **G (B):** S1 **âm thật** theo S-AT (S11 sai điều kiện 4/6 ↔ 2/6; S09 / S11 thiếu cảnh báo 6/6 ↔ 4/6) ⇒ một vòng chỉnh cuối `cc2d525` (ANSWER `507f891eafec`, ≈ 0,011): S11 sai điều kiện 0/6 ↔ mốc 2/6 đạt; S09 thiếu cảnh báo mưa lũ vẫn âm theo số judge, nhưng B đọc chữ 21/21 lần **cả G lẫn mốc đều không nhắc** ⇒ lỗi có từ RAG 1–8 (nằm ở nguồn [2] lần tìm đầu) ⇒ **User nhận S09 là giới hạn, đi tiếp G (20:55 09/11/2026)** ⇒ B đo bộ 32 ×2 + S2 / S2b + S4 trên `cc2d525` ⇒ review lời dặn (E) ⇒ merge. **Backlog:** câu trả lời bỏ điều kiện tạm ngừng mùa mưa lũ có trong nguồn (cả bản đang chạy). **Sau đó (21:01 09/11/2026):** bản `6956ac0` (ANSWER `507f891eafec`) trượt S2b trên bộ ĐÃ THẤY 2/44 (bản cũ 0/44) ⇒ quá 3 vòng chỉnh ⇒ **A chốt phương án B spec** (giữ định tuyến 4 tuyến, bỏ tuyến / câu khẩn cấp soạn sẵn; ngoài phạm vi do định tuyến quyết); G giữ hồ sơ `hoso/p9-g-cong`; nền T2 / T4 = bản phương án B. Tiền G hôm nay ≈ 0,18. E review code G: 0 blocker / 0 major / 3 minor.
- **T1 (E):** xác nhận 14 câu — L2 0, từ chối ⇒ OK 9, trượt "Tết năm nay" ⇒ sửa bằng code (A chọn (b)) trên `p9-t1-sang-nam` `ff65510`; lượt sau G 14 câu (tiêu chí `data/phase_9/t1/xac_nhan/tieu_chi.md`).
- **T2 (C cầm plan):** review C changes_requested 3 major (`…t2-web-plan_review.md`) ⇒ plan bản 2 **A duyệt `88b1f0586e99` (20:52 09/11/2026, mức nhẹ ≈ 0,17)**; bộ hỏi kèm 10 do E viết; code chờ G vào `main`. **T3:** đóng hồ sơ, tag `hoso/p9-t3-bang` (`e547b9e`). **T4 (E):** plan bản 2a **A duyệt `75dfd272fceb` (21:15 09/11/2026)** (bộ 31 câu, không kín, bỏ mốc câu lịch, S5 chung, + tiêu chí C M-1 "câu (b) không nối nhầm"); code `p9-t4-lich` `9780d93` (C review sớm 0 blocker); đo sau G B + T2. **G phương án B:** `p9-g-b` `4df9427` E review ready 0 / 0 / 2 minor (`g_b_branch_review.md`) — chờ B commit gỡ mã chết ⇒ E xem delta ⇒ merge.

- **(21:49 09/11/2026) Kết quả:** G phương án B merge `3b52017`; T1 merge `99ea59a` + **BẬT** `ngay_lich` (User duyệt, `7eb1f12`); **T2 âm** (câu hỏi kèm có phần web 4/10 = mốc; 26/29 lần gọi công cụ trùng câu từ chối cả câu) ⇒ **đóng hồ sơ** `hoso/p9-t2-web`, giữ cổng B6; T4 đi tiếp trên `main` mới (chạy mốc mới cùng lượt). **(22:18 09/11/2026) T4 âm** ở Q3 (ii) "hợp người đi cùng" (2 người chấm 21/27, 15/27; cần ≥ 26) — 3 sửa của T4 đúng việc (hỏi thừa 0, từ chối thay lịch 0, câu (b) nói sai 0/19), gốc lỗi ở luật xếp / bảng điểm ⇒ **đóng hồ sơ** `hoso/p9-t4-lich`, biểu mẫu là đường lịch trình duy nhất; E rà gốc nào cũng áp cho biểu mẫu đang bật.

### Làm tiếp (theo thứ tự)
1. **G cổng 2 nhóm (B)** — khoá `87d6798` (ROUTER `6b4796f7a35c`, ANSWER `426109d21b13`); G3 đạt mọi sàn trên bộ đã thấy + lượt khoá (S2 / S2b / S3b 0; S1 ngoài kho 0 ×2). S4 đạt (tụt 1/30 < 3), S6 đạt (câu Huế 0,000425 USD). S1 đủ 3 số còn lại cần harness lưu ngữ cảnh + chạy lại an toàn (≈ 0,05). Tiền thêm G phiên sau ≈ 0,12 ⇒ G ≈ 0,87. **Còn:** lượt kín (a 8 + b 10, ≈ 0,011 USD — vượt mức dừng 0,75 ⇒ **A xin User trước**, User chạy `!` 2 lệnh ghi ở `STATUS_B.md`), chấm mù S1 + S4 (0 USD), S5 độ trễ (≈ 0,06) ⇒ review cả nhánh ⇒ merge.
2. **T1 ngày + âm lịch (E)** — **đã merge `main` với cờ `ngay_lich` tắt** (review nhánh vòng 2 ready; 419 test đạt trên `main`; `lunar-vn` vào `uv.lock` ⇒ bẫy `uv sync` còn lại chỉ là `sherpa-onnx`); đạt 4 tiêu chí; review nhánh vòng 1 bắt M-1 (Tết tháng 1) ⇒ đã sửa; vòng 2 xem `report_agent/2026-11-02_phase_9_code/t1_ngay_branch_review.md`. Trước bật: S5 + lượt xác nhận câu ngày mới (gồm ca 1/1 – Tết) + đo lại 5 câu ngày khi G vào `main`. Thư viện `lunar-vn==1.4.0` (A duyệt 11:06). **Bẫy:** đừng `uv sync` thường ở `main` (gỡ `sherpa-onnx` của nhánh giọng nói) — dùng `uv sync --inexact --frozen`.
3. **T3 bảng vé + giờ (C)** — nhánh `p9-t3-bang` `21ec06d`, cờ tắt; vòng 3 Q2 19/20 nhưng Q3 trượt 6/10 ⇒ **User chọn (a) phương án B (20:18 09/11/2026)**: bảng chỉ để kiểm số giá / giờ sau khi model viết, lệch ⇒ câu cố định; bỏ khối điều kiện + bỏ đưa bảng cho model; ≈ 0,05 USD; giao C.
4. **Đợt 2** (sau khi G vào `main`): T2 tra web thành công cụ — **nháp plan** `docs/superpowers/plans/2026-11-08-phase-9-t2-web-plan.md` (B, `921f75d64a7c`; ≈ 0,21 USD > 0,2 ⇒ theo luật nhẹ cần review hoặc giảm tiền; còn chốt bộ 10 câu hỏi kèm) ⇒ T4 lịch trình từ câu gõ (spec §12).
5. **User khi rảnh:** tick phiếu toạ độ bản đồ `data/phase_11/ban_do/phieu_toa_do_11_diem.md` (⇒ bật `ban_do_lich`); thu 40 câu giọng nói (`data/phase_10/giong_noi/bo_40_cau/huong_dan_thu_cho_user.md`); phiếu v6 / v7.
6. **Đo độ trễ (S5):** mỗi lượt đo riêng, lần lượt B ⇒ E ⇒ C (lệnh ở `STATUS_<X>.md`); báo phiên điều phối dự án khác (nếu có trong `ListAgents`) trước.
7. Kết phiên sau: báo cáo khâu (`07_BAO_CAO_SINH_CAU_TRA_LOI_API`, `LUONG`) gộp mọi thay đổi đợt (luật mới: sửa lúc đóng đợt), `Project_Status.md`, vòng cải tiến (W59, W60 chờ User).

### Nhánh
`main`; **đang mở:** `p9-g-cong` (B), `p9-t3-bang` (C), `p12-deploy-nhap` (chờ deploy), `p9-sua-lich` (hoãn), `p10-giong-noi` (E), `p9-b5c` + `p9-toc-do-6` (hồ sơ). **Đã xoá (20:33 09/11/2026, User `!`):** 19 nhánh đã merge (local + origin). Còn: `p9-t1-sang-nam` (E, mới 09/11). Worktree giữ: `/tmp/b_g` (G, `87d6798`), `/tmp/b_moc_g` (mốc G, `442f758`), `/tmp/c_t3` (T3) — mất sau khởi động lại ⇒ dựng lại từ commit (cách ở `STATUS_B` / `STATUS_C`).

### Mã hay gặp
G = cổng 2 nhóm; T1 ngày + âm lịch; T2 web thành công cụ; T3 bảng vé + giờ; T4 lịch trình câu gõ (spec §12); S1–S6 / S2b / S2c / S3b = sàn §12.3; B0–B7 = bậc Phase 9; Bxx / Cxx / Exx = việc A giao; S / W / I = sổ `SO_CAI_TIEN_CACH_LAM.md`.

## Ý TƯỞNG TỪ NGHIÊN CỨU 04/11 — trạng thái (nguồn `bao_cao_he_thong/92_BAO_CAO_NGHIEN_CUU_PHASE_9.md` mục 000; hồ sơ `data/nghien_cuu_tinh_nang_2026-11-04/`)

| # | Ý | Trạng thái |
|---|---|---|
| 1–7, 12 | Kiểm giá "…000đ" / "triệu"; không đủ điểm ⇒ câu cố định; `khong_xep` + lý do từ mã luật; dòng giả định do code nối; test cố tình vi phạm; dòng "Mình hiểu…"; cột `ten_khac`; lời dặn không dùng địa danh thật làm ví dụ | vào B5 (`d66f6a3`) |
| 8 | Sửa lịch nhiều lượt (`sua_lich` hành động có tên, khung giữ ở server, Đã đổi / Giữ nguyên, ≤ 2 hành động / lượt) | code trên `p9-sua-lich` `79b3d9c` (rebase lên B5b + B171, giữ `hoi_toi` / lý do buổi tối — C208); harness đo E review ready; **hoãn** (cần cờ `lich_trinh` câu tự do) |
| 9 | Bộ chuỗi sửa lịch pass^k | bộ `data/phase_9/bo_do_sua_lich/` (10 + 5 kín; nhãn đã thấy S03 / S08 sửa theo B171 — C208); plan chọn pass^2; pilot = S01 + S06 (A đồng ý) |
| 10 | Cột trong nhà / bậc thang ⇒ phương án ngày mưa | phiếu gộp **v6** `data/phase_9/lich_trinh/diem_cho_user_v6.md` chờ User (gồm 2 câu v5 + cột thời lượng E21) |
| 11 | `so_ngay` viết lạ ("3N2Đ", "cuối tuần") — theo dõi | C210 06/11: code không dò "3N2D" / "4n3d" / "2 hôm" / "cuối tuần" nhưng model tự gửi đúng số 5 / 5; biểu mẫu bỏ vấn đề này |
| 13, 14 | Ưu tiên theo lĩnh vực; đoạn gần trùng | đếm 0 USD xong — không mở thí nghiệm (C179) |
| 15–17 | Nhãn lỗi tự động; "0 lỗi trên n ca" + luật ba; dự phòng demo mất mạng | B7 |
| 18 | Router gắn cờ ⇒ code gọi `lich_trinh` | không cần (Q2a đạt) |

**Không làm** (đã cân): lọc cộng tác / rating, TSP, GraphRAG, định tuyến bằng danh sách từ, bảng SQL giá, rerank / sparse mới, nhớ cả câu trả lời, web bật sẵn, công cụ ghi ra ngoài không cần duyệt.


## Câu hỏi cho User (hỏi mỗi lần một câu)

**09/11 (21:14 09/11/2026):** mốc đóng tính năng — User **chưa chốt** (A đề xuất 30/11; hỏi lại khi định tuyến B + T1 / T2 / T4 vào `main`). User: học dự án **sau khi xây xong** (A nhắc: muộn nhất ~15/12 vì bảo vệ 04–10/01); giữ 4 session.

**Mới 08/11 (User nghỉ lúc hỏi):** (0) **Tiền:** Phase 9 ≈ 3,0 / 3,5, quỹ B7 0,35 ⇒ còn ≈ 0,15 — nâng trần để chạy lượt kín G (≈ 0,011, vượt mức dừng G 0,75), S5 các việc (≈ 0,06 mỗi việc), đợt 2 T2 / T4 (≈ 0,33)? (1) **T3 bảng vé + giờ** — vòng 3: đúng 19/20 (đạt), khối điều kiện 4/4, nhưng sàn Q3 "0 câu model tự nêu điều kiện ngoài khối" trượt 6/10 (model chép điều kiện từ đoạn kho của lần tìm đầu) ⇒ chọn: phương án B (bảng chỉ cho kiểm cuối số, cờ tắt) · hay thiết kế lại (code lọc câu điều kiện khỏi chữ model) · hay đổi sàn Q3 (User duyệt). Report `report_agent/2026-11-06_giao_dien_cong/c_t3_bang_implementation.md` §9. **Phiếu chọn hướng 1 trang:** `data/phase_9/t3_bang_ve_gio/phieu_chon_huong.md` (C khuyến nghị (a) phương án B ≈ 0,05 USD; (b) code lọc câu điều kiện ≈ 0,1 nếu muốn trình bày "điều kiện nguyên văn" khi bảo vệ). (2) Bật bản đồ `ban_do_lich` sau khi User tick phiếu toạ độ. (3) Bật `ngay_lich` sau review nhánh + đo S5.

(3b) ~~**Khẩn cấp sau G**~~ — **ĐÓNG 20:20 09/11/2026: User giữ như 08/11, không thêm gì; bỏ bộ quan sát khẩn cấp khỏi các lượt đo** (User: "test những thứ vô nghĩa, over-engineer" — hỏi lại quyết định đã có). Cũ: 28 / 30 câu khẩn cấp nhận "không đủ thông tin" (đa số kèm mục web) — rủi ro User đã chấp nhận 08/11; trước khi bật G hỏi User một câu: giữ vậy hay thêm gì (vd mục web câu khẩn cấp). (4) Lượt kín G: User chạy `!` 2 lệnh (nguyên văn ở `STATUS_B.md`) sau khi duyệt tiền. (5) Vòng cải tiến 22: **W59** (đổi cờ ⇒ test có / không khoá; test tự đặt cờ), **W60** (hook bắt giờ ước "~HH:MM"); cũ W58 / W57 / sửa câu W50 / gỡ W4 + W39. (6) User `!` xoá nhánh đã merge (mục Nhánh). **Không gấp:** xoá collection thử `hue_anh_siglip2`; đợt 2 cổng phần còn lại (lưu trú, ăn gần, sự kiện — danh sách `data/ra_soat_tinh_nang_2026-11-08/`); câu thiên tai vẫn gọi Serper chỉ để lấy link; vị trí Bảo tàng Cổ vật kho tự mâu thuẫn (C204); 4 worktree AGY cũ; xoá sao lưu kho đợt 1 + 2; báo cáo tiến độ cho giáo viên; mốc quyển báo cáo + slide + kịch bản demo (chưa hỏi 08/11).

## Câu hỏi A còn nợ (không cần User)

- **08/11 mới:** T1 trước khi bật: lượt xác nhận câu ngày mới (gồm 1/1 – Tết), S5, đo lại 5 câu ngày khi G vào `main`; "tháng tới / cuối tuần" còn do model tự tính (giới hạn). G: S1 đủ 3 số cần chạy lại an toàn có ngữ cảnh (harness đã sửa, `data/phase_9/g_cong/tools/do_g.py`). T3: lưu ý gắn điểm cũ khi đổi chủ đề (lỗi thiết kế, chưa sửa). Luật kiểm số mục web so theo dãy chữ số ("1:23" trùng "123"; "8/11" ≠ "08/11") — theo dõi `web_kiem`. Lần gọi model bị Dừng giữa chừng không có usage ⇒ USD log là cận dưới.
- **Checklist trước deploy (gom):** 4 chốt (giới hạn lượt, cookie `Secure`, tắt `/docs`, xoay log `FileHandler`) — `data/phase_12/deploy_nhap/ra_soat_no_A_2026-11-08.md`; hạn mức OpenAI / Serper; `tra_web` tắt trên AWS; allow-list `dung_dockerignore.py` thêm `data/phase_9/lich_trinh/diem_toa_do_v5.json` (khi bật bản đồ) + bảng T3 (nếu bật); **ảnh #5 riêng không lên bản công khai** (A mặc định — hỏi User lúc deploy); build cần `dong_anh.py` + `anh_nho.py` trước `npm run build` (thiếu ⇒ ô Lễ hội tự dùng ảnh Commons).
- **Cũ còn mở:** E20 Sửa 1 / Sửa 2 + C210 (khi xét bật lịch trình câu tự do — giờ là T4); giờ tới / về bị bỏ qua im lặng; quan sát "model gọi `thoi_tiet` 2 lần rồi từ chối"; "đi dày" ít tác dụng (bảng thiếu thời lượng — phiếu v7); `do_so_ngay` không dò "4n3d" / "2 hôm" / "cuối tuần"; `p9-sua-lich` phải tôn trọng `hoi_toi` + `chon_sang` khi merge; chữ đầu mục web p50 ~13 s; B5b "tuần sau" không có số dự báo; `_token_count` chênh ~900 token; ghi đệm OpenAI giữ như cũ; bảng sổ S41–S44 thiếu 1 cột; B7: dự phòng demo mất mạng + đề cương + ý #15–#17; theo dõi case Golden 67 từ chối ngẫu nhiên.

## Session

**Phiên 09/11 (mở 20:09 09/11/2026):** A `hue-rag-87` · B `hue-rag-99` · C `hue-rag-6a` · E `hue-rag-ea` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn lúc mở (2 collection, 8.435 điểm). Worktree `/tmp/b_g`, `/tmp/b_moc_g`, `/tmp/c_t3` mất (prunable) ⇒ dựng lại từ nhánh.

**Phiên 08/11 (mở 09:16 08/11/2026):** A `hue-rag-a8` · B `hue-rag-a1` · C `hue-rag-e9` · E `hue-rag-22` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

**Phiên 07/11 (mở 11:53 07/11/2026):** A `hue-rag-7a` · B `hue-rag-10` · C `hue-rag-a0` · E `hue-rag-81` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

Phiên tối 06/11: A `hue-rag-cc` · B `hue-rag-1a` · C `hue-rag-42` · E `hue-rag-28`.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C / E lúc mở phiên sau: kiểm nhanh ⇒ đọc `STATUS_<X>.md` + mục "PHIÊN SAU ĐỌC TRƯỚC" ⇒ báo A ⇒ chờ (việc A giao = User nói "làm đi").

## Quyền

- **Phiên 09/11 (User chọn "như 08/11", A ghi nhận 20:13 09/11/2026):** A tự điều phối, giao ngay việc có sẵn, A tự commit / push, B / C / E push nhánh riêng, vượt 1 USD / phiên được, việc cần User duyệt thì gác. Trần Phase 9 nâng 4,0. Hết hạn cuối phiên.
  **Thêm (20:21 09/11/2026) User:** "thoải mái tiền API cho triển khai, phát triển nhưng phải đảm bảo tốc độ; không làm những thứ vô nghĩa hay test những thứ mất thời gian; 4 bạn trao đổi, thảo luận cùng nhau để đưa ra phương pháp, hướng xử lý phù hợp" ⇒ ưu tiên tốc độ làm; cắt test / đo không phục vụ sàn chất lượng; B / C / E bàn thẳng với nhau, A chốt khi lệch phạm vi.
- Spec Phase 9 file hiện tại sha `01b7476a3eb1` ≠ bản duyệt `5557f0fd7650` do commit `442f758` (bỏ mốc ngày theo User 08/11; sàn + tiền không đổi) ⇒ sửa chữ, không cần duyệt lại (A ghi 20:13 09/11/2026).
- **Quyền phiên 08/11 HẾT HẠN (12:50 08/11/2026, kết phiên).** (User 11:06: ~13:00 dừng; User 12:50 08/11/2026: để nhiệm vụ / câu hỏi cho phiên sau.)
- **Phiên 08/11 (User chọn "như 07/11", A ghi nhận 09:22 08/11/2026):** như 07/11 dưới đây (A tự điều phối, giao ngay việc có sẵn, A tự commit / push, B / C / E push nhánh riêng, vượt 1 USD / phiên được, khoá Serper cho tra cứu, việc cần User duyệt thì gác). Hết hạn cuối phiên. Giao lúc mở: B ảnh cổng (`p11-anh-cong`), C review ảnh, E rà "Câu hỏi A còn nợ" (chỉ đọc).
- **Phiên 07/11 (User chọn "như 06/11", A ghi nhận 11:55 07/11/2026):** A tự điều phối — giao ngay việc có sẵn trong handoff, A tự commit / push, ≤ 1 USD / phiên, B / C / E push nhánh riêng, trần Phase 9 2,5. Hết hạn cuối phiên.
  **Thêm (12:30 07/11/2026, User đi nghỉ):** "tiếp tục nghiên cứu, triển khai, phát triển, đánh giá, viết báo cáo đầy đủ; việc cần User duyệt thì gác lại, khi User nhắn thì đề xuất; làm việc khác; tự do nghiên cứu, gọi Codex tra cứu, nghĩ rộng, xem lại tối ưu + over-engineer; A / B / C / E thảo luận, đánh giá, đề xuất lẫn nhau". Trần tiền như trên (≤ 1 USD / phiên). **(12:31 07/11/2026) User: "trần tiền tôi vẫn duyệt nếu quá 1$, có thể thoải mái thực nghiệm"** ⇒ vượt 1 USD / phiên được; A vẫn ghi tiền thật từ log mỗi việc + báo tổng ở nhật ký.
- Phiên tối 06/11 — hết hạn 22:41 06/11/2026. Tiền phiên ≈ 0,027 USD.
- **Tiền Phase 9: trần 4,0 USD** (User nâng, A ghi nhận 20:15 09/11/2026; dự phóng việc chờ ≈ 0,55: G 0,12 · T1 0,04 · T3 0,05–0,1 · T2 0,21 · T4 0,12; quỹ B7 0,35 giữ riêng). Trước: 3,5 (User nâng 10:38 08/11/2026; trước 2,5) (User nâng 19:29 05/11/2026; không hết hạn theo phiên; dự phóng vượt ⇒ xin trước). **Phase 10:** trần 0,15 (dừng 0,13).
- **Đã duyệt, không hết hạn theo phiên:** spec giao diện cổng đợt 1 bản 2 `ff3c317ec88b` (User 11:56 07/11/2026); plan G2 giọng nói `92ec551531fd` (A duyệt sau review 2 vòng, 06/11 tối); spec Phase 10 bản 4 `784d6f7abd9f` (sherpa-onnx, tải model ≤ 300 MB, thu 40 câu; Web Speech bỏ); tải SigLIP 2 + collection ảnh (11:42 05/11); luật S-AT mới (20:14 05/11); cache câu trả lời ⇒ Phase 12 (20:27 05/11); bật `tra_web` (21:15 05/11).
- **User (09:00 05/11/2026):** cần công cụ / nghiên cứu / tải / khoá mới ⇒ tự nghiên cứu (0 USD, thông tin công khai) + đề xuất; thêm công cụ / thư viện lớn / tải model / khoá / tài khoản mới vẫn trình User trước (`Session_Prompt.md` §4).
- **Phase 9 (spec):** Serper dùng luôn (User chấp nhận rủi ro điều khoản); gói npm giao diện như đã duyệt 02/11; dữ liệu công khai dùng cho học tập, không kiểm giấy phép (05/11).
- **Thường trực:** A commit / push — hỏi User trước (luật chung), rồi A tự chạy; chỉ khi bị chặn / lỗi mới đưa `!` (`WORKFLOW.md` §9.6); B / C / E không commit trừ khi việc ghi rõ; duyệt cho A = duyệt cho B / C / E; thư viện nhỏ cần cho việc đã duyệt: A tự duyệt, báo sau; Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage + tiền; code luôn `uv run`.
- **Tra web:** `scripts/tra_web_codex.sh` (chỉ thông tin công khai); **không bao giờ gọi `agy`**. **(12:32 07/11/2026) User: khoá `SERPER_API_KEY` dùng được cho tra cứu nghiên cứu** (gọi qua `uv run --env-file /home/minhhieu/hue_rag/.env …`, không đọc / in khoá; chỉ câu tra thông tin công khai; 0,001 USD / lượt, ghi số lượt). Khoá `SERPER_API_KEY` trong `.env` (không đọc / in).
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

- Phiên 06/11 sáng + tối nguyên văn: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-06.md`.

- Phiên tối 05/11 nguyên văn: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05_toi.md`.
- Phiên 05/11 sáng–chiều nguyên văn (C173–C197, B156–B163, E1–E8, quyết định theo giờ, merge B4b / B5 / #6, B5c âm): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05.md`.
- Phiên 04/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-04.md`; 03/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-03.md`, `…_2026-11-03_toi.md`; 02/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-02.md`.
- Giao diện mới: `report_agent/2026-11-02_giao_dien_moi_code/`. Nghiên cứu Phase 9: `report_agent/2026-11-01_nghien_cuu_phase_9/` + `bao_cao_he_thong/92_BAO_CAO_NGHIEN_CUU_PHASE_9.md`.
- Streaming + đo cuối Phase 1–8: `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`. Phase 8.2: `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`.
