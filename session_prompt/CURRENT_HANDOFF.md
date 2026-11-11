# CURRENT_HANDOFF — việc đang mở của A/B/C/E

Cập nhật: 10:43 11/11/2026 (A, kết phiên 11/11). Trước: 22:41 10/11/2026 (A, kết phiên 10/11).
Nguyên văn handoff trong phiên 10/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-10.md`; 09/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-09.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-10_toc_do_xa_giao_cau_ngay.md`.

## PHIÊN SAU ĐỌC TRƯỚC (viết lại 10:43 11/11/2026, kết phiên 11/11)

**Phiên 11/11 đã kết** (mở 08:18, chỉ A mở; User: "đọc sau"). Quyền phiên 11/11 **hết hạn** ⇒ A mới hỏi lại User một câu. **Dự án chưa xong** — Phase 9 tiếp tục.
Khối kết phiên 10/11 nguyên văn: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-11.md`.

**Hệ thống:** không đổi so với 10/11 (`main` chỉ thêm tài liệu). **Qdrant tắt lúc mở phiên 11/11** (không container; dữ liệu `qdrant_storage/` còn đủ) ⇒ việc cần chatbot: `docker compose up -d qdrant` trước.
**Tiền 11/11:** 0 USD API (5 agent con chỉ đọc = quota Claude). Phase 9 ≈ 3,88 / 4,2.

### Xong 11/11 — bài học cho User (VIỆC SỐ 1 của 10/11)
- **`bai_hoc/` ở gốc repo, 17 bài (0–16)** + `README.md` (dàn bài + trạng thái). User **chỉ đọc folder này**; `bao_cao_he_thong/` = sổ ghi việc (quá khứ) của agent, vẫn cập nhật theo luật. Khuôn + luật: `WORKFLOW.md` §6 "Bài học cho User" (User chốt từng câu 11/11: bảo vệ đồ án, không phần dự án công ty; bám RAG 2 giai đoạn User đã biết; **kể thẳng, không so "bản cơ bản ↔ hue_rag"**; đủ chi tiết kỹ thuật; hình ảnh nền hướng dẫn viên + sổ tay; bảng từ đầu bài; mình / anh; "chuyện thật"; mỗi số kèm mốc + tốt tới đâu; mermaid khi cần).
- Ghi chú private cách đọc của User (gồm 2 tin của A dự án khác): `data/hoc_cung_user_2026-11-10/ghi_chu_cach_doc_cua_user.md`.

### Làm tiếp (theo thứ tự)
1. **Hỏi User quyền phiên** (một câu).
2. **Góp ý bài học:** User đọc dần ⇒ sửa ngay theo góp ý; câu sai ⇒ sửa + ghi ở mục Nguồn của bài + báo User. Không viết thêm bài khi User chưa yêu cầu. **Hệ thống đổi ⇒ sửa bài bị chạm trong `bai_hoc/` cùng đợt** với sổ ghi việc.
3. **Phase 9 tiếp (như 10/11):** **B7** lượt đo cuối (nháp plan `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md` + A chốt Q1–Q4; quỹ B7 thiếu ≈ 0,03 — hỏi User lúc chạy) · bản đồ (chờ phiếu toạ độ) · giọng nói (chờ 40 câu, nhánh `p10-giong-noi`) · deploy AWS (câu Q-DP dưới). Đợt 2 cổng (lưu trú, ăn gần, sự kiện): trước khi xây ⇒ lượt đếm rẻ (W61).
4. **Ứng viên từ bài 16 "chỗ còn yếu"** (đề xuất, chưa duyệt — trình User khi bàn việc mới; mỗi cái cần lượt đếm rẻ trước): thử lại model xếp lại ở cấu hình 10 đoạn; kiểm số tiền / giờ trong câu trả lời kho phải có trong đoạn được trích; thu câu người dùng thật khi deploy.
5. **User khi rảnh (không chặn):** đọc `bai_hoc/` · bảng điểm v7 `data/phase_9/lich_trinh/diem_cho_user_v7.md` · phiếu toạ độ `data/phase_11/ban_do/phieu_toa_do_11_diem.md` · thu 40 câu giọng nói `data/phase_10/giong_noi/bo_40_cau/huong_dan_thu_cho_user.md`.
6. Giới hạn biết (như 10/11): biểu mẫu "dày lịch" gần như không tác dụng; người lớn tuổi / trẻ em không có buổi tối; câu lịch bị rút khi thiếu `[n]` (1 / 9); log truy cập uvicorn ghi IP. Lệch nhỏ fact sheet thấy 11/11 (sửa khi chạm): chú thích `settings.yaml` cạnh `ngay_lich: true` và `anh.bat: true` còn ghi "TẮT tới khi đạt"; `07_BAO_CAO…` checklist còn dòng "câu lịch thuần ⇒ ngoài phạm vi" (sai từ 10/11); vài số dòng `file:dòng` cũ trong 05 / 06 / 07 / 10.

**Vòng tự soi 11/11:** chỉ A ⇒ tự soi một mình (STATUS_A): không test / đo nào chạy; agent con lập fact sheet đáng (bắt 3 câu sai). Sổ vòng 25 (S118–S120), không luật mới.

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

(1) Quyền phiên. (2) Góp ý `bai_hoc/` (khi User đã đọc). (Q-DP, **khi tới deploy AWS** — không hỏi sớm): tra web trên bản công khai · ảnh #5 riêng (mặc định không lên) · số lượt / IP / ngày (mặc định 50) · khoá OpenAI riêng + tài khoản AWS + tên miền (HUE_SITE phải là tên miền https, không thì cookie Secure làm mất nhớ hội thoại) · log truy cập uvicorn ghi IP ⇒ `--no-access-log`? (**15:04 11/11/2026 A probe 0 USD:** `setup_logging()` trong lifespan tắt logger `uvicorn.access` — `disable_existing_loggers` mặc định — ⇒ nhiều khả năng không in IP; xác nhận bằng một lần chạy server thật trước khi bỏ câu này) · xoá ảnh docker cũ — report `report_agent/2026-11-08_phase_9_ban_13/b_deploy_cuc_bo_implementation.md` §3. (B7) quỹ thiếu ≈ 0,03 USD. **Vòng cải tiến cũ còn chờ** (gom một lần, không hỏi lẻ): W60 / W58 / W57 / W4 + W39 + vòng 24 (sổ). **Mới (15:18 11/11/2026, review agent con bắt):** tên công ty nơi anh thực tập còn trong 11 file tracked đã public từ 23–24/10 (`WORKFLOW.md` §6 dòng "Học từ…", 2 file `report_agent/2026-10-24_to_chuc_bao_cao/*` có tên công ty trong tên file, `report_agent/README.md`, 2 spec, 4 file `reports/`, 1 nhật ký) — sửa tiến (đổi chữ / dời file sang `data/`) hay để nguyên? lịch sử git vẫn giữ. **Không gấp:** xoá collection thử `hue_anh_siglip2`; vị trí Bảo tàng Cổ vật kho tự mâu thuẫn (C204); 4 worktree AGY cũ; xoá sao lưu kho đợt 1 + 2; ảnh `hue-rag-app:nhap` có file private (User `! docker image rm hue-rag-app:nhap`); báo cáo tiến độ cho giáo viên; mốc quyển báo cáo + slide + kịch bản demo; nhãn cũ câu "hôm nay âm lịch" trong bộ 30/10 (`data/ngay_hien_tai_2026-10-30/questions.jsonl`) còn ghi từ chối.

## Câu hỏi A còn nợ (không cần User)

- **09/11:** T1 đã bật (xong lượt xác nhận + lượt sau G); giới hạn T1: "tháng tới / cuối tuần" còn do model tự tính (giới hạn). G: S1 đủ 3 số cần chạy lại an toàn có ngữ cảnh (harness đã sửa, `data/phase_9/g_cong/tools/do_g.py`). T3: lưu ý gắn điểm cũ khi đổi chủ đề (lỗi thiết kế, chưa sửa). Luật kiểm số mục web so theo dãy chữ số ("1:23" trùng "123"; "8/11" ≠ "08/11") — theo dõi `web_kiem`. Lần gọi model bị Dừng giữa chừng không có usage ⇒ USD log là cận dưới.
- **Checklist trước deploy (gom):** 4 chốt **đã có code** (`ccc9f4f`, bật bằng biến môi trường; đặt 3 biến trong `compose.yml`; uvicorn sau Caddy cần `--proxy-headers --forwarded-allow-ips <ip Caddy>`, không thì cả nước chung một sổ đếm; log xoay vòng giữa lượt đo ⇒ harness đếm hụt — hiếm) — `data/phase_12/deploy_nhap/ra_soat_no_A_2026-11-08.md`; hạn mức OpenAI / Serper; `tra_web` tắt trên AWS; allow-list `dung_dockerignore.py` thêm `data/phase_9/lich_trinh/diem_toa_do_v5.json` (khi bật bản đồ) + bảng T3 (nếu bật); **ảnh #5 riêng không lên bản công khai** (A mặc định — hỏi User lúc deploy); build cần `dong_anh.py` + `anh_nho.py` trước `npm run build` (thiếu ⇒ ô Lễ hội tự dùng ảnh Commons).
- **Cũ còn mở:** E20 Sửa 1 / Sửa 2 + C210 (khi xét bật lịch trình câu tự do — giờ là T4); giờ tới / về bị bỏ qua im lặng; quan sát "model gọi `thoi_tiet` 2 lần rồi từ chối"; "đi dày" ít tác dụng (bảng thiếu thời lượng — phiếu v7); `do_so_ngay` không dò "4n3d" / "2 hôm" / "cuối tuần"; `p9-sua-lich` phải tôn trọng `hoi_toi` + `chon_sang` khi merge; chữ đầu mục web p50 ~13 s; B5b "tuần sau" không có số dự báo; `_token_count` chênh ~900 token; ghi đệm OpenAI giữ như cũ; bảng sổ S41–S44 thiếu 1 cột; B7: dự phòng demo mất mạng + đề cương + ý #15–#17; theo dõi case Golden 67 từ chối ngẫu nhiên.

## Session

**Phiên chiều 11/11 (mở 13:39 11/11/2026):** A `hue-rag-2f` — chỉ A (B / C / E không mở; 8 terminal khác là dự án khác). Qdrant tắt. Việc: bàn `bai_hoc/` với User.

**Phiên 11/11 (mở 08:18 11/11/2026):** A `hue-rag-96` — chỉ A (B / C / E không mở). Qdrant tắt lúc mở.

**Phiên 10/11 (mở 19:02 10/11/2026):** A `hue-rag-55` · B `hue-rag-05` · C `hue-rag-4f` · E `hue-rag-e4` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn (2 collection, 8.435 điểm); không worktree `/tmp`.

**Phiên 09/11 (mở 20:09 09/11/2026):** A `hue-rag-87` · B `hue-rag-99` · C `hue-rag-6a` · E `hue-rag-ea` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn lúc mở (2 collection, 8.435 điểm). Worktree `/tmp/b_g`, `/tmp/b_moc_g`, `/tmp/c_t3` mất (prunable) ⇒ dựng lại từ nhánh.

**Phiên 08/11 (mở 09:16 08/11/2026):** A `hue-rag-a8` · B `hue-rag-a1` · C `hue-rag-e9` · E `hue-rag-22` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

**Phiên 07/11 (mở 11:53 07/11/2026):** A `hue-rag-7a` · B `hue-rag-10` · C `hue-rag-a0` · E `hue-rag-81` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

Phiên tối 06/11: A `hue-rag-cc` · B `hue-rag-1a` · C `hue-rag-42` · E `hue-rag-28`.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C / E lúc mở phiên sau: kiểm nhanh ⇒ đọc `STATUS_<X>.md` + mục "PHIÊN SAU ĐỌC TRƯỚC" ⇒ báo A ⇒ chờ (việc A giao = User nói "làm đi").

## Quyền

- **Phiên chiều 11/11 (User chọn "như sáng 11/11", A ghi nhận 13:41 11/11/2026):** A sửa `bai_hoc/` theo góp ý, tự commit / push; trần Phase 9 4,2; việc cần User duyệt thì gác. Hết hạn cuối phiên.
- **Quyền phiên 11/11 (sáng) HẾT HẠN (10:43 11/11/2026, kết phiên).**
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
