# CURRENT_HANDOFF — việc đang mở của A/B/C/E

Cập nhật: 12:16 06/11/2026 (A, **kết phiên 06/11** — User dừng giữa ngày, việc còn lại làm phiên sau). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở.
Nguyên văn phiên tối 05/11 (mọi việc giao + quyết định theo giờ): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05_toi.md`; sáng–chiều 05/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-05.md`. Nhật ký User: `bao_cao_he_thong/nhat_ky/2026-11-05_b4_am_chia_phase_10_12.md`.

## PHIÊN 06/11 (09:54 – kết 12:17 06/11/2026) — nguyên văn việc giao + trạng thái từng session

**Session:** A `hue-rag-f7` · B `hue-rag-85` · C `hue-rag-a4` · E `hue-rag-99` — cả bốn Claude Code, trực tiếp. Máy khởi động lại 09:50 ⇒ 4 worktree `/tmp` mất (nhánh còn đủ); `git worktree prune` được (không đụng 4 worktree AGY).
**Quyền phiên 06/11 (User chọn "như tối 05/11", A ghi nhận giữa 09:54 và 10:03 06/11/2026):** A tự điều phối; A commit / push `main`; B / C / E push nhánh riêng; ≤ 1 USD / phiên; trần Phase 9 2,5, Phase 10 0,15. Hết hạn cuối phiên.
**Quyết định User 06/11:**
- (10:03) Q3 B5: **agent chấm trước, User đọc chỗ lệch / không đạt** (thay "User chấm cả 5"; đổi trước khi có kết quả). Đã chạy: 2 sub-agent Claude ngữ cảnh mới, độc lập ⇒ khớp 15 / 15 ô: (i) 5 / 5, (iii) 5 / 5, **(ii) 3 / 5** (L3 cao, L5 vừa) — file private `data/phase_9/b5/kin/cham_agent_{1,2}.md`. A không đọc nội dung.
- (A ghi nhận 10:47 06/11/2026) User đọc phiếu: **câu kín B5 không tự nhiên** ⇒ kết quả Q3 trên bộ này **không dùng để quyết** (luật 24/10 câu đo phải tự nhiên). Chọn: **TRIPO vòng 4 + nghiên cứu cách người thật hỏi (giọng tự nhiên, không máy móc) ⇒ câu mẫu User duyệt ⇒ bộ kín B5 mới 5 câu (session chưa thấy B5 viết, User duyệt độ tự nhiên) ⇒ sửa 2 loại lỗi code (đo trên bộ đã thấy) ⇒ chạy kín mới ⇒ 2 agent chấm ⇒ User đọc chỗ không đạt.** Ước 0,01–0,03 USD. `lich_trinh` vẫn tắt; sửa lịch lùi theo.

**Việc giao 06/11:**
- **E — E19 (làm trước giọng nói):** (1) TRIPO vòng 4 bằng Playwright (`.venv` có 1.58, chromium sẵn; script mẫu `data/nghien_cuu_tinh_nang_2026-11-04/tripo_v3/tools/`): phần chưa thử — biểu mẫu "Lên kế hoạch chuyến đi" (bấm chip / chọn số người, ngày, ngân sách, kiểu đi, dịch vụ đi kèm; ghi đủ danh sách lựa chọn), tab Lưu trú / Ăn uống / Dịch vụ, bộ lọc trang Điểm tham quan (nhóm + "Bộ lọc"), bản đồ (lớp, nút xe / bán kính — không cấp vị trí). Luật như vòng 1–3: một trình duyệt, không đăng nhập, không nhập thông tin cá nhân, không bấm đặt / gọi / chia sẻ / gửi báo lỗi, nghỉ ≥ 7 s giữa lượt chat. (2) **Cách người thật hỏi về lịch trình Huế:** nguồn công khai (diễn đàn du lịch, hỏi đáp báo, review, Reddit…) qua `scripts/tra_web_codex.sh` + WebFetch kiểm; rút **mẫu cách nói** (độ dài, từ lóng, thiếu dấu câu, ràng buộc hay gặp: ngày, đi cùng ai, ngân sách, sở thích, mưa) — chỉ ghi loại / mẫu, không chép dài bài người khác. (3) Viết `data/phase_9/b5_v2/mau_cau_tu_nhien.md`: 6–8 câu mẫu (không dùng làm câu kín) + bảng loại ràng buộc ⇒ A đưa User duyệt. (4) Sau khi User duyệt mẫu: E viết bộ kín mới 5 câu `data/phase_9/b5_v2/cau_sealed.jsonl` (không trùng mẫu; không cho B / C / A xem) ⇒ User duyệt độ tự nhiên. Report `report_agent/2026-11-06_b5_cau_tu_nhien/e19_implementation.md`. Tiền: 0 USD (Codex dùng gói ChatGPT). Không sửa code. Xong (1)–(3) ⇒ nhắn A. Sau đó: giọng nói (script đổi WAV + plan G2, 0 USD).
  - **Trạng thái E19 (E, 12:15 06/11/2026, kết phiên):** (1)–(3) xong; User duyệt giọng 8 câu mẫu; A chốt không câu hai lượt + ≥ 2/5 câu ngoài lịch. **(4) bộ kín đã viết** `data/phase_9/b5_v2/cau_sealed.jsonl` 5 câu md5 `cd552f7cf7cb` (4/5 ngoài lịch; mã ràng buộc từng câu ở `STATUS_E.md`). **Bước kế phiên sau:** E viết `duyet_tu_nhien_user.md` ⇒ A đưa User duyệt độ tự nhiên. Giọng nói: plan G2 `555a35af92ab` chờ review sub-agent (`data/phase_10/giong_noi/plan_g2_review.md`); G1 chờ User thu 40 câu. 0 USD.
- **B — B5b trước, rồi B171:** (a) handoff mục 3 (worktree `p9-b5b`, áp patch `182904f45888`, test, commit + push nhánh) ⇒ nhắn A. (b) **B171 sửa 2 loại lỗi B5 bằng code** (nhánh mới `p9-b5-sua` từ `main`; mô tả ở mức loại, B **không** đọc `data/phase_9/b5/kin/` và `data/phase_9/b5_v2/`): **L-a** điểm lấp chỗ trống ngoài sở thích dù bảng còn điểm hợp sở thích (trái điều kiện lấp D2, có dính luật cụm kề) + câu lý do do code nối không đúng sự thật; **L-b** người dùng xin một buổi (vd buổi tối) mà luật code không xếp (vd đi cùng trẻ nhỏ) ⇒ code phải nối câu báo "không xếp … vì …", và kiểm cuối bắt lời model nói ngược khung ("được" khi khung không có). Ghi nhận (không sửa): "đi dày" ít tác dụng vì bảng điểm thiếu thời lượng. Tái tạo bằng ca tự viết / bộ đã thấy trước, sửa, test; lượt có phí chỉ bộ đã thấy (≤ 0,02 USD). Report `report_agent/2026-11-06_b5_cau_tu_nhien/b171_implementation.md` ⇒ review C. **Trạng thái B (kết phiên 06/11):** (a) B5b XONG phía B — `p9-b5b` `1610155` rebase lên `main` `23ea0f9`, Q1 228 / 228, C ready ⇒ A merge cờ tắt; (b) B171 `p9-b5-sua` `d5028d4` — **chưa sửa** review C (M-1 thu hẹp kiểm tối theo tên điểm + 16 ca dò, m-1, m-2) + T3 = (b) code dựng lời lịch từ khung; trần 0,04 (đã 0,0179). Bước kế chi tiết: `sessions/STATUS_B.md`.
- **C — C207 + review (kết phiên 12:14 06/11/2026 `date`):** (a) **C207 xong** — `p9-sua-lich` `6543f82` → **`09ddaf9`** trên `main` `0a9e0f3` (push `--force-with-lease`, A cho); Q1 / Q1m 228/228, 239 + 3 test, mô phỏng 10/10, `kiem_bo --pha` OK (`report_agent/2026-11-02_phase_9_code/c207_rebase_sua_lich.md`). (b) **Review `p9-b5b`: ready_for_user_confirmation** trên `0380345` (vòng 1 `18d1cec` changes_requested, 4 finding đóng — `b168_b5b_review.md` §7) ⇒ chờ B rebase ⇒ A merge. (c) **Review B171 `d5028d4`: changes_requested** (M-1 kiểm nói ngược buổi tối bắt nhầm 5/10 câu hợp khung; m-1; m-2; T3 (b) sau M-1 — `report_agent/2026-11-06_b5_cau_tu_nhien/b171_review.md`) ⇒ chờ B sửa ⇒ C kiểm. (d) **Harness lượt có phí sửa lịch (A đồng ý): CHƯA viết code** — thiết kế `data/phase_9/sua_lich/tools/HARNESS_GHI_CHU.md`. C **không** đọc `data/phase_9/b5_v2/`. Tiền C 06/11: 0 USD.
- Đo latency: không có hôm nay. Máy dùng chung với một dự án khác (~4–5 GB) ⇒ một việc nặng một lúc.

## PHIÊN SAU ĐỌC TRƯỚC (đọc trước nhất — viết lại 12:16 06/11/2026)

**Hệ thống (`main` = `origin/main`, chatbot KHÔNG đổi ngày 06/11 — mọi sửa nằm trên nhánh):** RAG 1–8 + trợ lý Phase 9: định tuyến 4 tuyến (trò chuyện / trợ lý Huế / ngoài phạm vi / khẩn cấp, dòng mở PA1) + dòng "có thể đã thay đổi" + tìm thêm `tim_kho` ≤ 2 lần + nhớ câu hỏi 3 lượt + câu dặn hẹp + giao diện nhiều lượt + 👍 / 👎 + **#6 song song BẬT** + **tra web B6 BẬT** (`7ff8e5a` + `b7c024e`). **Cờ tắt:** hỏi lại do code (`hoi_lai`), **B5 lịch trình** (`lich_trinh` — Q3 làm lại bằng bộ kín v2), **ảnh Phase 10** (`anh.bat`). Kho 204 file / **8.435 đoạn**; build record `9921888f2030`; T1 `64656a87c109`; Golden md5 `6331e88fb171`. `frontend/dist/` không commit ⇒ `cd frontend && npm ci && npm run build`. Qdrant: Docker Desktop; collection chatbot + collection thử `hue_anh_siglip2` (172 điểm, chờ User quyết xoá).

**Tiền:** Phase 9 ≈ **1,89 / 2,5 USD** (06/11: B ≈ 0,021 — B5b 0,0036 · B171 0,0179; A / C / E 0; chấm agent = quota Claude). Phase 10 ≈ **0,098 / 0,15**. B5b ≈ 0,054 / 0,07; B171 0,018 / trần nâng **0,04**.

**Diễn biến 06/11 (chi tiết mục "PHIÊN 06/11" ở trên):** (1) Q3 B5 — User chọn agent chấm trước: 2 sub-agent khớp 15 / 15, (ii) 3 / 5 ⇒ User đọc phiếu thấy **câu kín không tự nhiên** ⇒ gác, làm **bộ kín v2** (E19: TRIPO vòng 4 + 20 lượt hỏi thật VOZ ⇒ 8 câu mẫu, **User duyệt giọng**; bộ kín v2 5 câu md5 `cd552f7cf7cb` đã viết). (2) B171 sửa 2 loại lỗi B5 (code) ⇒ review C changes_requested. (3) B5b sửa 4 finding ⇒ C ready. (4) C207 `p9-sua-lich` rebase `09ddaf9`. (5) Plan G2 giọng nói `555a35af92ab` ⇒ sub-agent review: changes_requested (1 major + 8 minor). (6) Luật mới: User cấp "A tự điều phối" ⇒ A giao ngay việc có sẵn + A tự kiểm B / C / E rảnh (`WORKFLOW.md` §2.5, §9.2).

**Phase 9 — bậc còn lại:** B5 bộ kín v2 ⇒ chạy + chấm ⇒ bật ⇒ **sửa lịch** đo có phí (`p9-sua-lich` `09ddaf9`, trần 0,20, harness chưa code) ⇒ **B5b** merge + bật (User) + phần lịch "nếu mưa" (bảng v5) ⇒ **B7** đóng gói (quỹ 0,35). B5c dừng (tag `hoso/p9-b5c`).
**Phase 10:** ảnh xong (cờ tắt, User quyết bật); giọng nói: G0 xong (`p10-giong-noi` `93bbc63`), plan G1 + G2 chờ review ⇒ A duyệt sha ⇒ **G1 chờ User thu 40 câu** ⇒ G2 đo ⇒ G3 code.
**Phase 11 / 12:** backlog (lưu trú, bản đồ toạ độ, dữ liệu mở; Phase 12 deploy AWS = điều kiện đóng code; cache câu trả lời).

### Phiên sau làm theo thứ tự (A giao ngay sau câu quyền phiên — không chờ "làm đi")

1. Mở A / B / C / E; `ListAgents`; **hỏi quyền phiên** (quyền 06/11 hết hạn; đề xuất như 06/11) ⇒ **cùng lượt** nhắn B / C / E việc dưới (kèm `notify_when_idle`). Máy khởi động lại ⇒ worktree `/tmp` mất (dựng lại theo `STATUS_<X>.md`). **Bẫy:** `.venv` có sherpa-onnx nhưng `uv.lock` của `main` chưa có ⇒ `uv sync` ở `main` gỡ mất (xem `STATUS_E.md`).
2. **E:** viết `data/phase_9/b5_v2/duyet_tu_nhien_user.md` (5 câu kín v2 để User duyệt **độ tự nhiên**) ⇒ A đưa User. Rồi sửa plan G2 theo review: **review xong 06/11 — changes_requested, 0 blocker · 1 major · 8 minor** (`data/phase_10/giong_noi/plan_g2_review.md`; M-1: luật vòng chỉnh hotwords còn hở — mức 4 đạt V-e mà 8 không vẫn thử 12, chọn mức chỉ theo V-a, chưa ghi mọi chỉ số quyết đạt trên **cùng một cấu hình**; m-1 thiếu mục "Căn cứ để review"; m-2…m-8 nhỏ) ⇒ E sửa ⇒ người review kiểm phần sửa (vòng 2, tối đa 2 vòng) ⇒ A duyệt sha.
3. **A (đầu phiên):** `p9-b5b` **`1610155`** đã rebase lên `main` `23ea0f9` (Q1 228/228, 190 test, B push 06/11; C ready trên nội dung `0380345`) ⇒ main mới hơn thì B rebase lại + Q1 ⇒ **A merge cờ `thoi_tiet` tắt + cổng ổn định** ⇒ hỏi User bật. **B:** B171 (`p9-b5-sua` `d5028d4`; phần sửa review + T3 chưa làm, không có code dở): sửa M-1 / m-1 / m-2 theo `report_agent/2026-11-06_b5_cau_tu_nhien/b171_review.md` ⇒ **T3 = (b)** (A chốt: code dựng lời lịch tối thiểu khi chữ model = câu từ chối) ⇒ C kiểm ⇒ A merge cờ tắt.
4. **C:** kiểm phần sửa B171 khi B xong; viết harness lượt có phí sửa lịch theo `data/phase_9/sua_lich/tools/HARNESS_GHI_CHU.md` (0 USD, chạy thử bằng khoá giả). **Câu E hỏi (A quyết phiên sau):** bộ kín v2 chạy bằng harness B5 cũ (đổi đường dẫn bộ câu) hay cần thêm trường cho 2 agent chấm — người chạy kín (không phải B / C đã đọc lý do chấm cũ? — B / C chưa đọc `data/phase_9/b5/kin/`; người chạy = C hoặc E) chuẩn bị lệnh `!` chỉ in số đếm.
5. **Khi User duyệt độ tự nhiên + B171 merge:** chạy kín v2 trên `main` (cờ `lich_trinh` bật trong worktree) ⇒ 2 sub-agent mới chấm độc lập ⇒ User đọc ô không đạt ⇒ đạt ≥ 4 / 5 cả 3 tiêu chí ⇒ A bật `lich_trinh` ⇒ sửa lịch lượt có phí NGAY (C).
6. **Câu hỏi cho User** (mục dưới).

### Nhánh

`main`; **đang mở:** `p9-b5b` `1610155` (B; C ready, đã rebase — chờ A merge), `p9-b5-sua` (B171, B), `p9-sua-lich` `09ddaf9` (C), `p10-giong-noi` `93bbc63` (E), `p9-b5c` (hồ sơ, đã tag). **Đã merge ⇒ chờ User xoá (User `!`):** `p9-b4`, `p9-b5`, `p9-toc-do-6`, `p9-toc-do-6b`, `p10-anh`, `p10-anh-mobile`, `p9-b6` (local + origin). 4 worktree AGY cũ `c725987` (User quyết).

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

1. **Quyền phiên** (đề xuất như 06/11: A tự điều phối — giao ngay việc có sẵn, A tự commit / push, ≤ 1 USD / phiên, B / C / E push nhánh riêng, trần Phase 9 2,5).
2. **(gấp nhất)** Duyệt **độ tự nhiên** 5 câu kín B5 v2 (E đưa file `data/phase_9/b5_v2/duyet_tu_nhien_user.md`) — chỉ xem câu có giống người thật hỏi không.
3. Bật **thời tiết B5b** khi A merge xong? (câu dự báo ⇒ số từ Open-Meteo do code dựng, ghi giờ số liệu; ngoài 7 ngày ⇒ câu cố định; bão / lũ ⇒ NCHMF + 112; 06/11 sửa thêm: câu từ chối không còn đứng trước bảng số.)
4. Phiếu bảng điểm v5 — `data/phase_9/lich_trinh/diem_cho_user_v5.md` (giữ / bỏ dòng "Bảo tàng Mỹ thuật"; ô tick "trong nhà").
5. Thu 40 câu nói — `data/phase_10/giong_noi/bo_40_cau/huong_dan_thu_cho_user.md`.
6. Bật **hỏi bằng ảnh** (`anh.bat`)? Xoá collection thử `hue_anh_siglip2`?
7. Vòng cải tiến: gỡ W4 / W39 (Session D 0 buổi, hạn 07/11) hay giữ; W57; luật "gói Python phát hành ≥ 2 tuần"; **mới 06/11:** bước User / người ngoài duyệt độ tự nhiên trước khi khoá mọi bộ kín (bộ B5 cũ không tự nhiên mà không ai bắt).
8. Xoá 7 nhánh đã merge (mục Nhánh) — User `!`.
9. Không gấp: câu thiên tai vẫn gọi Serper chỉ để lấy link; vị trí Bảo tàng Cổ vật kho tự mâu thuẫn (C204); đọc 10 câu mẫu B4 / B6; 4 worktree AGY cũ; xoá sao lưu kho đợt 1 + 2; báo cáo tiến độ cho giáo viên.

## Câu hỏi A còn nợ (không cần User)

- **06/11:** quyết cách chạy bộ kín v2 (harness B5 cũ + đường dẫn mới, hay thêm trường cho người chấm — câu E); quan sát B5b "model gọi `thoi_tiet` 2 lần rồi từ chối" (theo dõi); "đi dày" ít tác dụng vì bảng điểm thiếu thời lượng (ghi nhận, chưa sửa); `do_so_ngay` không dò "4n3d" / "2 hôm" / "cuối tuần" / "đi trong ngày" (dựa vào model — đo ở kín v2); B171 thêm `hoi_toi` + `chon_sang` vào tham_so ⇒ `p9-sua-lich` phải tôn trọng khi merge.
- Link Google Maps của B5 đổi sang toạ độ cho 17 điểm có toạ độ (C197; v5 thêm 1 toạ độ) — A quyết khi bật B5.
- B6 giới hạn: địa chỉ / số điện thoại trong mục web chưa kiểm ⊂ đoạn trích (đề xuất "mọi chuỗi số ⊂ đoạn trích" — việc sau); chữ đầu mục web p50 ~13 s (theo dõi; ý tối ưu: tra web song song khi kho có dấu hiệu thiếu); thêm "đang" vào luật thời gian thực sẽ chặn nhầm 1 câu đúng.
- B5b giới hạn: câu "tuần sau" không có số dự báo (luật ngoài 7 ngày); câu không dấu không có công cụ (ngoài phạm vi, User 25/10).
- Cách đếm token (`_token_count`) không tính kết quả tìm thêm + mô tả công cụ ⇒ chênh tới ~900 token; ngữ cảnh 1,7–4k ≪ 16k.
- Ghi đệm OpenAI: C202 05/11 tối âm — giữ như cũ; xét lại nếu tắt tìm thêm. Bảng sổ cải tiến: S41–S44 thiếu 1 cột. Log `FileHandler` không xoay vòng (deploy). Hạn mức OpenAI / Serper — đặt trước deploy (B6 đã bật).
- B7: dự phòng demo khi mất mạng; đề cương "trợ lý RAG có công cụ"; ý #15–#17.
- Theo dõi: router đưa S20 sang `khan_cap`; định tuyến > 10 s ⇒ `tro_ly_hue`; `chat_feedback` chưa nối `chat_metrics`; case Golden 67 từ chối ngẫu nhiên sau tìm thêm (C192).

## Session

**Phiên 06/11 (09:54 – kết 12:17 06/11/2026):** A `hue-rag-f7` · B `hue-rag-85` · C `hue-rag-a4` · E `hue-rag-99` — cả bốn Claude Code, trực tiếp. Mỗi session đã viết lại `sessions/STATUS_<X>.md` cho phiên sau.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C / E lúc mở phiên sau: kiểm nhanh ⇒ đọc `STATUS_<X>.md` + mục "PHIÊN SAU ĐỌC TRƯỚC" ⇒ báo A ⇒ chờ (việc A giao = User nói "làm đi").

## Quyền

- **Phiên 06/11 — HẾT HẠN lúc kết phiên (12:16 06/11/2026)** (User chọn "như tối 05/11"). Tiền phiên ≈ 0,021 USD. **B171 trần nâng 0,04** (A, trong trần Phase).
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
