# CURRENT_HANDOFF — việc đang mở của A/B/C/E

Cập nhật: 22:41 10/11/2026 (A, kết phiên 10/11). Trước: 22:27 09/11/2026 (A, kết phiên 09/11).
Nguyên văn handoff trong phiên 10/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-10.md`; 09/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-09.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-10_toc_do_xa_giao_cau_ngay.md`.

## PHIÊN SAU ĐỌC TRƯỚC (viết lại 22:41 10/11/2026, kết phiên 10/11)

**Phiên 10/11 đã kết** (mở 19:02; User đi ngủ: "để các file còn lại cho session mai"). Quyền phiên 10/11 **hết hạn** ⇒ A mới hỏi lại User một câu.

**Hệ thống (`main` = `origin/main`):** như 09/11 + từ 10/11: **câu hỏi ngày nhanh** (`1633c18`: code tính sẵn ngày / ngày âm đưa vào ngữ cảnh trước lần gọi model đầu, công cụ `ngay_lich` chỉ còn dự phòng; chữ đầu p50 5,60 ⇒ 2,35 s, p95 10,14 ⇒ 4,56 s; 0,00049 ⇒ 0,00036 USD / câu) · **câu lịch chung không nhắc Huế đi trợ lý** (`89571d7`: chỉ đổi lời dặn định tuyến `164bd4a254e9` ⇒ `8cd30cbb359a`; câu chỉ hỏi về ngày tháng được trả lời, câu hỏi việc khác vào một ngày vẫn từ chối) · **biến môi trường cho Docker** (`5081e89`: `HUE_QDRANT_URL`, `HUE_TRA_WEB`; không đặt ⇒ như cũ). **Đóng hồ sơ:** xã giao chạy song song (p95 5,74 s > sàn 5; tag `hoso/p9-xa-giao-song-song`). Tag mốc B7 `p9-moc` = `18e8f42`. Deploy cục bộ đạt (ảnh 3,6 GB, 0 file riêng tư, 429 khi quá lượt, Caddy ghim 2.11.7) — chưa AWS.
**Quyết định User 10/11:** quyền như 09/11 + trần Phase 9 **4,2**; **không chốt mốc đóng tính năng** ("xong sớm đóng sớm, vẫn đảm bảo chất lượng"); duyệt W59 + W61 (vào `Session_Prompt.md` §7, §8); "hạn chế test không cần, không over-engineer, đẩy nhanh; chi phí API vẫn duyệt"; câu lịch chung ⇒ giao bước phân loại (model), không luật từ khoá; **khi User vắng không đưa câu hỏi**.
**Tiền 10/11:** ≈ 0,28 USD (B ≈ 0,25 · E ≈ 0,03 · A ≈ 0,002 · C 0). Phase 9 ≈ 3,88 / 4,2; quỹ B7 0,35 ⇒ thiếu ≈ 0,03 — hỏi User lúc chạy B7.

### VIỆC SỐ 1 — báo cáo để User hiểu được dự án (User tâm sự 10/11; quan trọng nhất)
- **11/11 (A + User, hỏi từng câu):** thư mục **`bai_hoc/` ở gốc** (User chỉ đọc folder này; `bao_cao_he_thong/` = sổ ghi việc quá khứ, giữ); đích = **bảo vệ đồ án** (không phần dự án công ty); xương sống = **sơ đồ RAG hai giai đoạn User đã biết** (khoá Ed Donner); dàn 17 bài (`bai_hoc/README.md`); khuôn theo bài mẫu User đã khen ở một dự án khác (bảng từ đầu bài, mình / anh, Nguồn gập, "chuyện thật") — luật ở `WORKFLOW.md` §6 "Bài học cho User". Bài 0–2 viết xong, **chờ User đọc**; dễ hiểu ⇒ viết liền tới 16, báo sau mỗi 2 bài. Ghi chú private cách đọc của User (gồm 2 tin của A dự án khác 11/11): `data/hoc_cung_user_2026-11-10/ghi_chu_cach_doc_cua_user.md`. Các dòng dưới (10/11) về `hieu_he_thong/` đã thay bởi dòng này; `STATUS_C.md` dòng 9 cũ.
- **User nói (tối 10/11, nguyên ý):** README + `01_LUONG…` "tạm chấp nhận, chưa dễ hiểu hẳn" (khó nhất: **từ khó / lạ**, **bảng nhiều số**); `02_BAO_CAO_KHO…` bản 10/11 "đọc không hiểu nổi" — không biết "chỉ mục", "phiếu", "vân tay" là gì; phần "đã sửa những đợt nào", "còn thiếu gì", "khi sửa kho làm gì", "đã thử, không dùng" không cần trên đường đọc. "Tôi đã không đọc code mà bạn còn viết khó hiểu như vậy, sao tôi nắm dự án được."
- **Khó khăn chung User kể** (cả ở một dự án khác; chi tiết **private** `data/hoc_cung_user_2026-11-10/ghi_chu_cach_doc_cua_user.md` — đọc trước khi viết): agent làm hết, User chỉ đọc báo cáo ⇒ "không học được gì"; tài liệu viết như **sổ công trường** (đã làm gì, bao nhiêu, ở đâu) giả định người đọc có bức tranh lớn; một câu nhiều từ lạ / mã; "làm gì" trước "vì sao"; file gói nhiều ý + bảng số + đường dẫn; nhiều bộ tài liệu chồng nhau; **viết nhanh hơn tốc độ đọc**; sợ bị hỏi mà không trả lời được. Hiểu được khi: bài ngắn, mỗi bài một ý, vì sao trước, đi từ đơn giản nhất, giọng gần gũi + ví dụ đời thường (User học RAG qua khoá Udemy + YouTube).
- **User chốt (A hỏi từng câu 10/11):** (1) kiểu viết **kể như giải thích** (văn xuôi ngắn, so sánh đời thường, một ví dụ — mẫu "kho = cuốn sổ tay du lịch; hỏi chùa Thiên Mụ ⇒ chatbot lật sổ tay, tìm vài đoạn, đọc rồi viết, kèm tên bài; sổ không có ⇒ nói không đủ thông tin, không bịa"); (2) mỗi bài trả lời: **nó là gì / làm gì · vì sao làm cách này · tốt tới đâu · khi nào hỏng**; (3) thuật ngữ: **lời thường trước, tên kỹ thuật một lần trong ngoặc sau** khi đã giải thích; (4) ~1 trang / 3 phút, **linh hoạt** — khâu làm kỹ thì dài hơn, không cắt ý quan trọng; (5) **hai thư mục**: `bao_cao_he_thong/hieu_he_thong/` = chuỗi bài để hiểu đánh số (bài 00 "cả hệ thống trong 3 phút", rồi 01 kho, 02 chia đoạn, … theo dòng chảy); file `01_…10_`, `9x_`, `nhat_ky/` hiện có = **sổ ghi việc** để tra. README chỉ trỏ "đọc `hieu_he_thong/` theo số". **Tránh:** câu hỏi kiểm tra, "nói lại bằng lời của bạn", áp lực sếp, mã việc / sha / đường dẫn trong bài, bảng dày số không nói số nào quan trọng / tốt hay xấu.
- **Làm tiếp:** viết **2 bài mẫu** trước (00 + 01 kho) — một người viết cho cùng giọng (A hoặc một session, đọc file private trên + memory `user-reading-style`); mỗi bài ≤ 3 từ mới giải nghĩa tại chỗ, cuối bài "Ba điều chính"; số liệu đúng hiện trạng (README "Số chính", Project_Status §4) ⇒ **User đọc, góp ý** ⇒ mới viết tiếp; không viết hàng loạt. Chưa rõ ⇒ hỏi User từng câu có đáp án tick (User trả lời thật, chi tiết). **Còn dở:** User muốn nói rõ thêm chỗ khó ở README + 01 (đã chọn "từ khó / lạ" + "bảng nhiều số") — hỏi lại đầu phiên.
- Luật viết cho mọi agent đã ghi ở `WORKFLOW.md` §6 "Văn phong cho User" (10/11).

### Làm tiếp (theo thứ tự)
1. **Hỏi User quyền phiên** (một câu) ⇒ VIỆC SỐ 1 (bài mẫu 00 + 01; hỏi nốt chỗ khó README + 01).
2. ~~User `!` xoá 4 nhánh~~ — XONG 08:35 11/11/2026 (local + origin; tag `hoso/p9-xa-giao-song-song` = `22abb2a` giữ).
3. **User khi rảnh (không chặn):** bảng điểm v7 `data/phase_9/lich_trinh/diem_cho_user_v7.md` · phiếu toạ độ bản đồ `data/phase_11/ban_do/phieu_toa_do_11_diem.md` (⇒ bật `ban_do_lich`) · thu 40 câu giọng nói `data/phase_10/giong_noi/bo_40_cau/huong_dan_thu_cho_user.md`.
4. **Còn trong phạm vi trước đóng gói:** bản đồ (chờ phiếu), giọng nói (chờ 40 câu, nhánh `p10-giong-noi`), deploy AWS (câu Q-DP dưới), **B7** (nháp plan `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md` + A chốt Q1–Q4; review khi gần chạy). Đợt 2 cổng (lưu trú, ăn gần, sự kiện): trước khi xây ⇒ lượt đếm rẻ theo W61.
5. Giới hạn biết: biểu mẫu "dày lịch" gần như không tác dụng (chờ v7); người lớn tuổi / trẻ em không có buổi tối; câu lịch bị rút khi trả lời không có mã nguồn `[n]` (1 / 9 — luật cũ, đếm ≥ 20 câu trước khi sửa); log truy cập uvicorn ghi IP.

**B kết phiên (B báo A; auto mode phiên B chặn B ghi `STATUS_B.md` ⇒ STATUS_B cũ — B đầu phiên sau tự viết lại):** không việc dở, không worktree / server / container; tiền B 10/11 ≈ 0,25 USD (xã giao 0,08 · deploy 0,001 · định tuyến lịch 0,169). Tự soi B: sàn p95 trên nhóm 20 câu = câu chậm thứ 2 ⇒ tính trước trước khi đặt sàn p95 nhóm nhỏ; plan nên ước cả mốc + vòng 2 (tiền thật ≈ 1,5× ước); giữ review deploy + rà danh sách chừa + bộ giữ mù (bắt lỗi thật).

**Vòng tự soi 10/11:** vòng 1 (19:14) cắt bộ đo B / E; vòng 2 (22:42 10/11/2026) — chốt: ghi vào sổ vòng 24 (không luật mới ngoài W64 đề xuất); C: gửi review 1 tin; B: tính trước sàn p95 nhóm nhỏ.

### Nhánh
`main`; 4 nhánh 10/11 User xoá 08:35 11/11/2026. Đang mở cũ: `p9-sua-lich` (hoãn), `p10-giong-noi` (E), `p9-b5c` + `p9-toc-do-6` (hồ sơ). Worktree `/tmp`: không còn. Ảnh docker cục bộ: `hue-rag-app:dep10b` (đạt), `dep10`, `nhap2` (cũ, xoá được).

### Mã hay gặp
G = cổng 2 nhóm (đóng); T1 ngày + âm lịch (bật, bản nhanh 10/11); T2 / T3 / T4 đóng hồ sơ 09/11; S1–S6 / S2b = sàn §12.3; B0–B7 = bậc Phase 9; S / W / I = sổ `SO_CAI_TIEN_CACH_LAM.md`.

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

(1) Quyền phiên. (2) VIỆC SỐ 1 (bài mẫu + chỗ khó README / 01). (Q-DP, **khi tới deploy AWS** — không hỏi sớm): tra web trên bản công khai · ảnh #5 riêng (mặc định không lên) · số lượt / IP / ngày (mặc định 50) · khoá OpenAI riêng + tài khoản AWS + tên miền (HUE_SITE phải là tên miền https, không thì cookie Secure làm mất nhớ hội thoại) · log truy cập uvicorn ghi IP ⇒ `--no-access-log`? · xoá ảnh docker cũ — report `report_agent/2026-11-08_phase_9_ban_13/b_deploy_cuc_bo_implementation.md` §3. (B7) quỹ thiếu ≈ 0,03 USD. **Vòng cải tiến cũ còn chờ** (gom một lần, không hỏi lẻ): W60 / W58 / W57 / W4 + W39 + vòng 24 (sổ). **Không gấp:** xoá collection thử `hue_anh_siglip2`; vị trí Bảo tàng Cổ vật kho tự mâu thuẫn (C204); 4 worktree AGY cũ; xoá sao lưu kho đợt 1 + 2; ảnh `hue-rag-app:nhap` có file private (User `! docker image rm hue-rag-app:nhap`); báo cáo tiến độ cho giáo viên; mốc quyển báo cáo + slide + kịch bản demo; nhãn cũ câu "hôm nay âm lịch" trong bộ 30/10 (`data/ngay_hien_tai_2026-10-30/questions.jsonl`) còn ghi từ chối.

## Câu hỏi A còn nợ (không cần User)

- **09/11:** T1 đã bật (xong lượt xác nhận + lượt sau G); giới hạn T1: "tháng tới / cuối tuần" còn do model tự tính (giới hạn). G: S1 đủ 3 số cần chạy lại an toàn có ngữ cảnh (harness đã sửa, `data/phase_9/g_cong/tools/do_g.py`). T3: lưu ý gắn điểm cũ khi đổi chủ đề (lỗi thiết kế, chưa sửa). Luật kiểm số mục web so theo dãy chữ số ("1:23" trùng "123"; "8/11" ≠ "08/11") — theo dõi `web_kiem`. Lần gọi model bị Dừng giữa chừng không có usage ⇒ USD log là cận dưới.
- **Checklist trước deploy (gom):** 4 chốt **đã có code** (`ccc9f4f`, bật bằng biến môi trường; đặt 3 biến trong `compose.yml`; uvicorn sau Caddy cần `--proxy-headers --forwarded-allow-ips <ip Caddy>`, không thì cả nước chung một sổ đếm; log xoay vòng giữa lượt đo ⇒ harness đếm hụt — hiếm) — `data/phase_12/deploy_nhap/ra_soat_no_A_2026-11-08.md`; hạn mức OpenAI / Serper; `tra_web` tắt trên AWS; allow-list `dung_dockerignore.py` thêm `data/phase_9/lich_trinh/diem_toa_do_v5.json` (khi bật bản đồ) + bảng T3 (nếu bật); **ảnh #5 riêng không lên bản công khai** (A mặc định — hỏi User lúc deploy); build cần `dong_anh.py` + `anh_nho.py` trước `npm run build` (thiếu ⇒ ô Lễ hội tự dùng ảnh Commons).
- **Cũ còn mở:** E20 Sửa 1 / Sửa 2 + C210 (khi xét bật lịch trình câu tự do — giờ là T4); giờ tới / về bị bỏ qua im lặng; quan sát "model gọi `thoi_tiet` 2 lần rồi từ chối"; "đi dày" ít tác dụng (bảng thiếu thời lượng — phiếu v7); `do_so_ngay` không dò "4n3d" / "2 hôm" / "cuối tuần"; `p9-sua-lich` phải tôn trọng `hoi_toi` + `chon_sang` khi merge; chữ đầu mục web p50 ~13 s; B5b "tuần sau" không có số dự báo; `_token_count` chênh ~900 token; ghi đệm OpenAI giữ như cũ; bảng sổ S41–S44 thiếu 1 cột; B7: dự phòng demo mất mạng + đề cương + ý #15–#17; theo dõi case Golden 67 từ chối ngẫu nhiên.

## Session

**Phiên 10/11 (mở 19:02 10/11/2026):** A `hue-rag-55` · B `hue-rag-05` · C `hue-rag-4f` · E `hue-rag-e4` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn (2 collection, 8.435 điểm); không worktree `/tmp`.

**Phiên 09/11 (mở 20:09 09/11/2026):** A `hue-rag-87` · B `hue-rag-99` · C `hue-rag-6a` · E `hue-rag-ea` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn lúc mở (2 collection, 8.435 điểm). Worktree `/tmp/b_g`, `/tmp/b_moc_g`, `/tmp/c_t3` mất (prunable) ⇒ dựng lại từ nhánh.

**Phiên 08/11 (mở 09:16 08/11/2026):** A `hue-rag-a8` · B `hue-rag-a1` · C `hue-rag-e9` · E `hue-rag-22` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

**Phiên 07/11 (mở 11:53 07/11/2026):** A `hue-rag-7a` · B `hue-rag-10` · C `hue-rag-a0` · E `hue-rag-81` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

Phiên tối 06/11: A `hue-rag-cc` · B `hue-rag-1a` · C `hue-rag-42` · E `hue-rag-28`.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C / E lúc mở phiên sau: kiểm nhanh ⇒ đọc `STATUS_<X>.md` + mục "PHIÊN SAU ĐỌC TRƯỚC" ⇒ báo A ⇒ chờ (việc A giao = User nói "làm đi").

## Quyền

- **Phiên 11/11 (User chọn "như 10/11", A ghi nhận 08:20 11/11/2026):** như 10/11 dưới đây (A tự điều phối, tự commit / push, B / C / E push nhánh riêng, trần Phase 9 4,2, việc cần User duyệt thì gác, không hỏi khi User vắng). Hết hạn cuối phiên.
- **Phiên 10/11 (User chọn "như 09/11 + trần 4,2", A ghi nhận 19:05 10/11/2026):** như 09/11 dưới đây (A tự điều phối, giao ngay việc có sẵn, A tự commit / push, B / C / E push nhánh riêng, vượt 1 USD / phiên được, việc cần User duyệt thì gác; tiền API thoải mái nhưng ưu tiên tốc độ, không test vô nghĩa). **Trần Phase 9 nâng 4,0 ⇒ 4,2 USD** (cho 2 việc tốc độ, quỹ B7 0,35 giữ riêng). Hết hạn cuối phiên.
  **Thêm (19:12 10/11/2026) User:** "hạn chế test các phần không cần thiết, không over-engineer, muốn đẩy nhanh quá trình; chi phí API vẫn duyệt; các session cùng trao đổi, thảo luận để đề xuất, chốt phương án" ⇒ A mở vòng tự soi 1 ngay (plan B / E là kết quả đầu); tiền không còn là lý do giữ bộ đo — thời gian là thước.
  **Thêm (19:15 10/11/2026) User đi nghỉ:** "tiếp tục điều phối, phát triển, triển khai, ghi báo cáo đầy đủ; câu cần User chốt thì gác lại, triển khai phần khác; **không đưa câu hỏi lúc User vắng** (treo việc)" ⇒ A không mở hộp hỏi tới khi User nhắn; câu cần User ghi "Câu hỏi cho User".
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
