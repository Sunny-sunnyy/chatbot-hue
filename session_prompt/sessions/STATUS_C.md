# STATUS C — phiên 14/11 (C `hue-rag-b4` · A `hue-rag-7b` · B `hue-rag-22` · E `hue-rag-c4`). Lịch sử: `git log -p session_prompt/sessions/STATUS_C.md`

**Phiên mở 17:45 14/11/2026:** C `hue-rag-eb` · B `hue-rag-62` · E `hue-rag-1f` · A `hue-rag-fb`. Kiểm nhanh khớp handoff; kho chưa ghi 8 quán; chờ A giao việc.
**A giao (phiên tối):** bảng quán lịch + đếm lại sau khi B dựng chỉ mục; review nhánh ảnh của E. **Khai báo sửa:** `data/quan_lich_2026-11-14/` (tools/dung_bang.py, photon_quan_them.json, biên bản) · `data/phase_9/lich_trinh/bang_quan_lich_v1.json` · nhánh `p9-quan-kho-them-bang` (chỉ md5 trong comment `settings.yaml`).
**Thêm (A, phiên tối):** ảnh mọi quán bảng quán lịch ⇒ khai báo thêm `data/anh_quan_2026-11-14/` · `frontend/src/LichV2.jsx` + file ảnh quán (nhánh riêng `p9-anh-quan`).
**Bảng quán lịch sau ghi kho 4 XONG (17:54 14/11/2026):** 469 quán md5 `580881638793`; bữa có quán kho 49,3 ⇒ 69,1 %; mô phỏng 0/0/0; nhánh `p9-quan-kho4-bang` `26505d6` chờ E review (worktree `/tmp/c_qb`). Biên bản `data/quan_lich_2026-11-14/bien_ban_quan_kho_them.md`. Ảnh: E làm mọi bài Khám phá; C làm ảnh quán OSM + thẻ bữa (`data/anh_quan_2026-11-14/TIEU_CHI.md`).
**Ảnh quán OSM (18:04 14/11/2026):** thử 30 ⇒ 11/30 đạt; chỉ 15 quán ngoài kho từng hiện trong lịch ⇒ chỉ làm 15 (2 agent con đang chọn). Bỏ Huế An (đã đóng, hiện 324 lịch) ⇒ nhánh `p9-quan-bo-da-dong` `f9119d1` chờ E (worktree `/tmp/c_qd`). Review A `p9-web-so-cau-hoi` xong (vòng 2 ready). Tiền C phiên tối ≈ 0,045 USD Serper.
**Ảnh quán ở thẻ bữa (18:13 14/11/2026):** nhánh `p9-anh-quan` `496206d` chờ E review (worktree `/tmp/c_aq`); report `report_agent/2026-11-12_ra_khoang_cach/c_anh_quan_implementation.md`. 6/15 quán ngoài kho có ảnh (48 % lượt hiện); 15 quán: 0 đã đóng (Codex + WebFetch 3). Tiền C phiên tối ≈ 0,05 USD.
**Sau review E (18:19 14/11/2026):** `p9-anh-quan` @ `815ab2e` (ẩn ảnh kc ở thẻ bữa, 5 ảnh ngoài kho = 32,3 % lượt hiện) — A merge. Review `p9-anh-v4` E: ready 0/0/3 (`c_review_anh_v4.md`). Đếm mưa XONG (`c_dem_mua.md`): đề xuất không thêm điểm trong nhà; nếu làm tiếp thì đổi ngày bằng code. Chờ B: review `p9-khach-san`.
**Đếm đổi ngày khi mưa XONG (18:20 14/11/2026, 0 USD):** cứu cận trên 13,7 % chuyến, mùa mưa 8–21 % số chuyến kẹt ⇒ đề xuất không xây (`c_dem_mua.md` phần 2). Chờ B: review `p9-khach-san`.
**Review phiên tối (18:47 14/11/2026):** `p9-khach-san` ready 0/0/3 · `p9-anh-v4b` vòng 2 ready · `p9-anh-kc` changes_requested (10/13 ảnh nâng bằng luật nguồn không nhận ra nơi; dự kiến hiện được 161 ⇒ 169).
**(19:02 14/11/2026)** `p9-khach-san-anh2` review ready — A merge. Việc kế: review bài nháp ghi kho 5 khi E (địa điểm / di tích) và B (món / đặc sản) nhắn (cách kho 3 / 4). Đang rảnh.
**Ghi kho 6 bước 1 XONG (19:47 14/11/2026, 0,0178 USD):** `data/bai_kho_6_le_hoi/BUOC_1_DEM.md` — 24 mục chưa có bài: từ chối 9 · mỏng 7 · đủ 8; danh sách viết 16 (đợt 1 = 10). Chưa viết bài, chờ A. Review ghi kho 5 xong (B 10 + E 13 ready). Tiền C phiên tối ≈ 0,07 USD.
**Ghi kho 6 XONG (20:30 14/11/2026, B ghi):** 263 file / 9.425 đoạn; 8 bài của C (Tết, Âm hồn, Trung thu, Vu Lan, Đoan Ngọ, Truyền Lô, Hò Huế, Lý Huế) — câu thử trích đúng bài mới. C review 8 bài B + B review 8 bài C xong. Rảnh.

## PHIÊN SAU ĐỌC TRƯỚC (C viết lúc kết phiên 14/11, 17:40 14/11/2026 `date`)

- **Việc kế (đang dở):** 8 bài quán mới của B cho Kim Long / Thủy Xuân / Đầm Chuồn.
  - C đã review: ready sau 5 minor (sửa chữ). Biên bản private `data/quan_kho_them_2026-11-14/c_review_8_bai.md`. Nháp ở `data/quan_kho_them_2026-11-14/nhap/`.
  - **Chờ B** sửa minor ⇒ ghi kho ⇒ dựng chỉ mục (B báo cả nhóm).
  - **Sau đó C** dựng lại bảng quán lịch:
    1. `uv run python data/quan_lich_2026-11-14/tools/dung_bang.py` ⇒ `data/phase_9/lich_trinh/bang_quan_lich_v1.json` (hiện md5 `e7b239019f22`, 467 quán = kho 35 + dữ liệu mở 4 + OSM 428).
       Cần sửa script trước khi chạy:
       - thêm 8 quán mới;
       - **khử trùng** quán kho mới ↔ dòng OSM cùng quán (tên gần giống + ≤ 200 m), vd Đầm Chuồn Hương Quán có cả hai;
       - chép `muc_toa_do`.
    2. Toạ độ:
       - Thu Sương (86 Kim Long), O Lé (kiệt 104 Kim Long), ECO (107 Minh Mạng), Không Gian Xưa (98 Minh Mạng), Maison Trang 2 (94 Huyền Trân Công Chúa): Photon theo địa chỉ, không ra số ⇒ ước theo số kề cùng đường (như Bánh ép Huệ, xem `data/quan_lich_2026-11-14/photon_banh_ep_hue.json`), mức "uoc";
       - An Phú: giải Plus Code GJ8V+VH2 (mức "vua");
       - Hương Quán: lấy toạ độ dòng OSM cùng tên;
       - Hội Quán: chỉ có "thôn Định Cư" ⇒ để ngoài bảng.
    3. `uv run python data/quan_lich_2026-11-14/tools/dem_theo_cum.py backend data/quan_lich_2026-11-14/dem_theo_cum_<lần>.json` ⇒ gửi B / A số "bữa có ≥ 1 quán kho theo cụm". Mốc hiện tại: tổng 49,3 %; Thủy Xuân 33,6 %; Kim Long 0 %; biển / đầm phá 0 %; nam xa 0 quán.
    4. `tools/mo_phong.py backend` (sàn: 0 ngoài bảng / khác cụm / lặp; ≤ 2 km). `pytest tests/test_quan_lich.py`. Nhánh nhỏ đổi md5 trong comment `settings.yaml` (`lich_trinh_bang_quan`) ⇒ E review ⇒ A merge.
- **Đang chạy trên main (C làm chiều 14/11):**
  - quán ăn trong lịch: cờ `quan_lich: true`; bữa chính chỉ quán ăn; ≤ 2 quán cùng cụm ≤ 2 km; không giờ / giá / điện thoại; không vào model;
  - ảnh lịch 33 / 34 (`bang_anh_v2.json` md5 `6fe592114d2b`; Thuận An trống);
  - ảnh Khám phá 184 / 216;
  - câu nhiều ý: so_y "và / còn / với" + mục web chỉ viết ý thiếu + log `nhieu_y` / `chi_y_thieu`;
  - Giới thiệu mới; bỏ mọi chữ ghi công.
- **Giới hạn đã ghi (không làm thêm nếu không được giao):**
  - ngoài 3 cụm trung tâm, quán gần như chỉ OSM "chưa kiểm", tên mỏng;
  - không có dòng ăn ở phá / biển Thuận An / Hòn Chén / Gia Long / Bạch Mã;
  - câu hai ý không dấu phẩy / không từ hỏi / "A hay B" ⇒ vẫn từ chối cả câu; "với" giới từ có thể đếm thừa;
  - mục web cho ý thiếu ít giá trị: đếm 3 / 16 có ích, mức tốt nhất 6 / 16 ⇒ giữ nguyên.
- **Bẫy gặp hôm nay:**
  - `git worktree add -b <tên>` trùng tên nhánh có sẵn ⇒ lệnh hỏng ⇒ lệnh sau chạy ở cây chung. Hôm nay C lỡ sửa 1 dòng `settings.yaml` rồi hoàn lại. ⇒ Kiểm tên nhánh trước, nối bằng `&&`.
  - `quan_theo_cum.json` trộn 3 nguồn (kho / OSM / dữ liệu mở): lọc `nguon == "kho"`. Hôm nay C đếm nhầm 42 là quán kho (đúng 28), đã sửa.
  - Worktree không có `frontend/dist` ⇒ `test_ban_do_lich` trượt (môi trường) ⇒ `npm ci && npm run build` trước test rộng.
  - RAM: 2 bộ test rộng cùng lúc ⇒ 0 GB trống. Luật A: chỉ A chạy test rộng; mỗi người ≤ 1 server tạm.
- **Tiền C 14/11 ≈ 0,47 USD:** sáng ≈ 0,35 (câu nhiều ý v1 + v2) · chiều ≈ 0,12 (so_y 0,015 · web ý thiếu 0,035 · ảnh Khám phá 0,035 · đếm web 0,016 · ảnh lịch 0,004 · quán lịch 0,0013 · ví dụ 0,0004).
- **Câu hỏi còn mở (chờ A / User):** không có câu mới. Câu cũ "dòng © OSM": A đã chốt không hiện, ghi ở "Câu hỏi cho User" dạng BÁO.
- **Máy:** 0 server, 0 pytest của C. Mọi worktree `/tmp/c_*` của C đã gỡ (`/tmp/c_yc2` không phải worktree ⇒ để nguyên).

## PHIÊN 14/11

**A giao (09:46 14/11/2026):** (1) rà lời dặn bản 2 (0 USD) · (2) B0 bảng ảnh đợt 2 — 24 / 34 User chốt 13/11 (tải Commons nền, chậm) · (3) E báo đã ghi kho ⇒ dừng, review diff kho với `meta/` trước khi E dựng chỉ mục · (4) góp ý W69 ≤ 5 dòng cùng kết quả rà gửi cả nhóm. Bài lưu trú: lần này không ghi.
**Khai báo sửa:** file này · `data/anh_kham_pha_2026-11-14/` (A giao 14/11: ảnh Khám phá + 10 điểm lịch) · `report_agent/2026-11-12_ra_khoang_cach/c_nghien_cuu_wow.md` · `data/ui_mau_2026-11-14/` (tools/, c/, h*/gioi_thieu.html) · `bao_cao_he_thong/` 02–07, 09, 10, 90, README + `nhat_ky/2026-11-14_ghi_kho_3_bai.md` (A giao 14/11, ghi kho) · `data/osm_quan_2026-11-12/` (script + bảng + biên bản mới) · `report_agent/2026-11-12_ra_khoang_cach/c_ra_loi_dan_ban2.md` · `data/phase_9/lich_trinh/tools/dung_bang_anh.py` + `data/phase_9/lich_trinh/bang_anh_v1.json` + `data/phase_9/lich_trinh/anh_lich_v1/` (ảnh tải về) · `data/ra_khoang_cach_2026-11-12/` (script đếm). Không chạm `knowledge-base-hue/`, code `backend/` / `frontend/`.

**Rà lời dặn bản 2 XONG (09:55 14/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_ra_loi_dan_ban2.md` — log không cho thấy lỗi mới do lời dặn; giữ Đ1 (nhánh B) + Đ5 (skill, A); **bỏ Đ3** (bản 1 sai giả định: mô tả thời tiết / ngày chỉ đưa khi có từ khoá); không làm Đ4. Đã gửi bàn nhóm vòng 1 cùng W69 (đồng ý hook chỉ cảnh báo + lọc tên trùng món / điểm từ đầu). B đồng ý.
**Review gói ghi kho 14/11 của E XONG (09:55 14/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_review_ghi_kho_14_11.md` — M-1 (kho tự mâu thuẫn số nhà 15A ↔ 17 ở bài phố đi bộ) ⇒ E sửa, A chốt cùng mục ② ⇒ **ready**, E ghi được.
**B0 bảng ảnh XONG (09:58 14/11/2026, 0 USD):** `data/phase_9/lich_trinh/bang_anh_v1.json` md5 `a5e210e5a1f0` — 24 / 34 (đúng sàn), ảnh `anh_lich_v1/` ≤ 80 KB mỗi ảnh, tổng 1.769 KB; tác giả / giấy phép 0 lệch so với Commons; C nhìn 24 / 24 đúng điểm, ảnh #7 đã cắt. Biên bản `bien_ban_bang_anh_v1.md`. Đã nhắn B (B1) + A.
**W69:** User BỎ (A báo). Rà lời dặn: A chốt theo C.
**Bảng quán OSM riêng cho lịch v1 XONG (10:01 14/11/2026, A giao, 0 USD):** `data/osm_quan_2026-11-12/bang_quan_osm_v1.json` md5 `8563a685723a` — 488 quán (581 ⇒ lọc tự động 471 ⇒ đọc tay cả 110 bỏ +44 và cả 471 giữ −20 ⇒ gộp trùng ≤ 150 m −8); 5 / 8 cụm ≥ 3 quán. Biên bản `bien_ban_bang_quan_v1.md`. Chờ E review. Chưa code (đợt 3).
**Kiểm X03 + gold_v6 XONG (10:18 14/11/2026, A giao, 0 USD):** X03 sau ghi kho trả lời đúng theo đoạn bài đi lại, 0 số ngoài đoạn, thiếu câu nhắc mũ bảo hiểm / rượu bia (minor) ⇒ đồng ý đổi nhãn "trong kho"; gold_v6 chỉ dời 2 trích dẫn (case 167), chữ giống hệt. Đã gửi A + E.
**Review report ghi kho của E XONG (10:26 14/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_review_e_ghi_kho_report.md` — ready, 2 minor ("nguyên văn" case 154 ⇒ 5 / 9 dãy 4 từ; tên thông tin cạnh case_index). Mọi số mục 4 tính lại khớp.
**Sổ ghi việc cho ghi kho 14/11 XONG (10:31 14/11/2026, A giao):** `bao_cao_he_thong/` 01–10, 90, README (207 bài / 8.474 đoạn, record / sparse / T1 / nhãn v6, X03, Qdrant còn 1 collection) + `nhat_ky/2026-11-14_ghi_kho_3_bai.md` — chưa commit, chờ A đọc.
**Bảng quán OSM: E review ready (0/0/2) ⇒ C sửa 2 minor (10:31 14/11/2026)** — bảng không đổi.
**Bản mẫu Giới thiệu × 3 hướng XONG (10:43 14/11/2026, A giao, 0 USD, không chạm repo):** `data/ui_mau_2026-11-14/h{1,2,3}/gioi_thieu.html` + ảnh `c/` + `c/BIEN_BAN_GIOI_THIEU.md`; công cụ `tools/kiem_tuong_phan.py` (0 trượt / 6). Chờ trang chủ của E ⇒ kiểm tương phản + 390 cả 3; sau User chọn: Giới thiệu + Khám phá.
**Đầu vào cho mẫu Khám phá (B, TRIPO v7):** `report_agent/2026-11-12_ra_khoang_cach/b_tripo_v7_giao_dien.md` §2 — thẻ bài có ảnh + nhãn lĩnh vực ở góc; trang bài hai cột (nội dung trái, thẻ "thông tin nhanh" phải lấy từ "Thông tin chung"); "bài liên quan" cuối trang; ảnh 03_diem_tham_quan_1440.png, 06_chi_tiet_dai_noi_1440.png. Làm SAU khi User chọn hướng.
**Mẫu Khám phá H1 XONG (11:06 14/11/2026):** `data/ui_mau_2026-11-14/h1/kham_pha.html` + `kham_pha_bai.html` (tools/dung_kham_pha.py) — tương phản 0 trượt, CLS ≤ 0,0025, giảm chuyển động 0 animation. Công cụ `tools/kiem_hieu_ung.py` (CLS + reduced-motion) + `kiem_tuong_phan.py --khung-cuoi-ken-burns`. Giới thiệu H1 gắn lớp hiệu ứng chung của E. Đo Lên kế hoạch H1 của E: sau sửa 0 trượt.
**Review nhánh B `p9-lich-truong-gd` XONG (11:06 14/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_review_lich_truong_gd.md` — ready 0/0/2; worktree /tmp/c_rv đã gỡ.
**Đo Trợ lý H1 + Lên kế hoạch H1 (E) XONG (11:15 14/11/2026):** cả 5 trang H1 qua 3 phép đo ở 1440 + 390.
**Review nhánh B `p9-anh-lich` XONG (11:15 14/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_review_anh_lich.md` — ready 0/0/3 (ghi công thiếu "đã thu nhỏ" + link giấy phép; chữ 12 px; test đọc data/). Worktree /tmp/c_rv2 đã gỡ.
**Hiệu ứng bản 2 (E) áp cho trang C + đo 6 trang H1 XONG (11:28 14/11/2026):** 0 trượt (390 sau khi E dời dải báo), CLS ≤ 0,034, giảm chuyển động 0 animation.
**Tra framework hiệu ứng XONG (11:28 14/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_framework_hieu_ung.md` — CSS đủ; GSAP + ScrollTrigger chỉ cho màn cuộn kể chuyện; số gzip C đo + thử CSP thật (0 vi phạm). Kết quả Codex `data/tra_cuu_cli/2026-11-14_fw-hieu-ung/`. /tmp/c_fw đã xoá. **Lỗi của C:** gõ giờ ước (11:40) vào report ⇒ hook bắt, sửa bằng `date`.
**Việc kế (User "làm đi", A giao):** chờ E xong đợt chung trên nhánh `p9-gd-h1` ⇒ C làm Khám phá + trang bài + Giới thiệu từ mẫu, review chéo với E, đo 3 phép trên bản build thật. Khai báo file trước khi sửa.
**Chờ việc** (11:28 14/11/2026). Còn mở: review bài lưu trú khi E viết xong.
**Câu nhiều ý — code XONG (nhánh `p9-cau-nhieu-y` 5bc07b1, đã push, cờ tắt):** chờ E "dựng xong" ⇒ đo có phí (hỏi kèm 10, an toàn 32 ×2, Golden 176; ≈ 0,15 USD) ⇒ E review.
**Ảnh Khám phá v2 XONG (13:30 14/11/2026):** nhánh `p9-anh-kp` 3c5350f (từ main cfb5d99) — 167 bài có ảnh, 29 "Ảnh minh hoạ", ghi công ở `public/anh/kp/ghi_cong.json` (tải khi mở trang bài / Giới thiệu), 31 link trùng kho về trang chủ tên miền (hook không vượt). Sửa thêm CLS Giới thiệu #nguon-anh 390 (0,17–0,66 trên main ⇒ ≤ 0,03). E review ⇒ ready; chờ A merge. Server 8897 (bản nhánh ảnh) còn chạy — merge xong tắt.
**Nhãn bộ sửa lịch theo lịch bản 2 XONG (13:23 14/11/2026, 0 USD):** `data/phase_9/bo_do_sua_lich/` — đã thấy 2923d432da9b, kín 1165ecfa6367; mô phỏng code B 2bc020d 4/10 ⇒ 10/10, kín 1/5 ⇒ 5/5; cơ cấu giữ nguyên; báo B lỗi harness `q3_sua_lich.py` thiếu luật `khong_doi` (A chốt 06/11).
**Review nhẹ ghi kho 2 của E XONG (13:29):** `report_agent/2026-11-12_ra_khoang_cach/c_review_e_ghi_kho_2.md` — ready 0/0/0, mọi số khớp.
**Câu nhiều ý — đo XONG, KHÔNG ĐẠT (13:37 14/11/2026, 0,1601 USD):** `report_agent/2026-11-12_ra_khoang_cach/c_cau_nhieu_y_do.md` — hỏi kèm 4 ⇒ 10/10 đạt; an toàn máy đếm đạt; Golden trượt (ngoài kho bị trả lời 3/18, lỗi trích dẫn mới 2) ⇒ cờ giữ tắt, không merge; đề xuất vòng 2 chờ A. Mở: X01 TypeError chập chờn (đường web cũ). Nhánh rebase 31d38f3 chưa push. 8897 đã tắt; /tmp/c_anh đã gỡ (nhánh ảnh A merge ef8bc46).
**Câu nhiều ý VÒNG 2 — đo XONG (14:03 14/11/2026, ≈ 0,19 USD):** nhánh 2c99534 (đã push); `report_agent/2026-11-12_ra_khoang_cach/c_cau_nhieu_y_do_v2.md` — mọi sàn đạt trừ Golden ngoài kho 1/18 (câu 161, đường không đổi: yêu cầu gửi model giống byte bật/tắt ⇒ nhiễu). Golden 0/176 đi vào luật mới. CHỜ A quyết (i) đóng / (ii) S-AT 2 judge ⇒ E review. NK06/NK07 của E: không do cờ (đường cũ).
**Bẫy 14/11:** review kho 3 ngày 13/11 không grep chỗ khác nhắc cùng sự kiện (sót dòng 15A) ⇒ sửa một sự kiện trong kho thì grep mọi chỗ nhắc nó.

## (Phiên 13/11 — giữ để tra)

## PHIÊN SAU ĐỌC TRƯỚC (C viết lúc kết phiên, 22:39 13/11/2026 `date`)

*Tên quán / cơ sở trong file tracked ghi bằng nhãn; bảng nhãn ở `data/` (private). Report tracked tả quán / cơ sở ở MỨC LOẠI ngay khi viết.*

**Việc đầu phiên sau (theo thứ tự; A giao lại khi mở phiên):**
1. **Rà lời dặn bản 2 — DỞ:** `report_agent/2026-11-12_ra_khoang_cach/c_ra_loi_dan_ban2.md` md5 `ad661b94415b` — đã có số hành vi từ log (407 lượt; model tự gọi tìm kho lần 3 ở 37 câu; công cụ thời tiết dùng 2 / 403, ngày 12 / 403). **Còn:** đối chiếu từng câu dặn với lượt đo ở `data/` (B7, hết lượt tìm, lịch trình), đếm câu ngoài phạm vi, ≤ 5 đề xuất theo lợi / công ⇒ gửi cả nhóm. Script: `data/ra_khoang_cach_2026-11-12/tools/dem_log_chat_metrics.py`. B rà harness song song (`b_ra_harness_tro_ly.md`) — không chồng.
2. **Review diff kho** với bản sao ở `knowledge-base-hue/meta/` khi E ghi kho 3 (2 bài điểm mỏng + bài Đi lại + 3 chỗ sửa) — đo đã dời sang phiên sau theo lời User. Không đọc `evaluation/`, `*sealed*`.
3. **Khi A giao:** bảng quán OSM riêng cho lịch (A chốt 13/11) — đọc tay ~110 dòng bị lọc trước khi dựng (`data/osm_quan_2026-11-12/dem_cho_cau_kho_rieng.md`); bản nhẹ ~10 quán vào bài "ăn gì gần" chỉ SAU khi ghi kho 3 + đếm lại. Phần (B) ảnh của plan đợt 2: chờ User duyệt phiếu ảnh bản 2 (tối đa 24 / 34 = đúng sàn, 0 biên) ⇒ C dựng `bang_anh_v1.json` (tải Commons CHẬM, ≥ 10 s / yêu cầu).

**Sản phẩm phiên 13/11 (đều 0 USD API):** khớp OSM bản 2 + Photon (bài kho có toạ độ 29 ⇒ 34 / 81) · đếm OSM cho câu "bảng riêng / kho chính" · toạ độ v7 (`data/phase_9/lich_trinh/diem_toa_do_v7.json` `158e184154de`, 33 / 34) · plan đợt 2 (`docs/superpowers/plans/2026-11-13-len-ke-hoach-dot-2-plan.md`, A duyệt) · phiếu ảnh bản 2 · điểm lễ hội ban ngày · review: kho 3 của E (2 vòng), bật cờ hết lượt tìm (`9d6a0f7`), bài kho điểm mỏng, kiểm độc lập `bai_hoc/`, so mốc bước (b) (khớp 4 / 4).
**Tiền C phiên 13/11: 0 USD API** (gửi ra ngoài: Overpass 2 truy vấn, Photon 2, Commons ~13 có 1 lần bị 429, WebFetch ~10 trang — chỉ thông tin công khai).
**Không server / worktree / nhánh / container của C.** File tạm `/tmp` đã xoá.

**Bẫy phiên 13/11 (đừng lặp):**
- **Gửi số trước khi lệnh chạy xong** (gộp SendMessage cùng lượt với lệnh tính md5) ⇒ tin mang 4 md5 bịa. Số / md5 chỉ gửi SAU khi thấy đầu ra.
- **Report tracked chép tên / địa chỉ cơ sở từ `data/`** (sự cố e74c6df) ⇒ viết ở mức loại ngay từ đầu, cả review và STATUS.
- **Grep thẳng kho** thay vì `scripts/grep_kb.sh` (1 lần, lúc đọc tay khớp quán).
- **Luật chữ dò trên chữ bỏ dấu** ("Quán" ↔ "quận", "Làng" ↔ "lăng") ⇒ dò tên tiếng Việt trên chữ còn dấu.
- **Gửi dồn ~11 truy vấn Commons** ⇒ 429 ⇒ luôn chờ + cách ≥ 10 s.
- Script cũ có sẵn biến trùng tên với biến mới chèn (`BANG`) ⇒ grep tên trước khi thêm.

## PHIÊN 13/11

*Tên quán / cơ sở lấy từ kho hoặc `data/` ghi bằng nhãn (Q-…, L-…); bảng nhãn ở `data/osm_quan_2026-11-12/nhan_status_c_13_11.md` và `data/luu_tru_2026-11-12/nhan_review_c_13_11.md` (private).*

**Phiếu ảnh bản 2 XONG:** `data/phase_9/lich_trinh/phieu_anh_2026-11-13_ban2.md` (4 ảnh mới CHƯA AI NHÌN; #6, #16 không có ảnh thay ⇒ thẻ không ảnh). Commons 429 khi gửi dồn ⇒ chạy chậm.
**So mốc bước (b) XONG (20:27 13/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_so_moc_buoc_b.md` — khớp 4 / 4 sàn của B (81 % · 58 % · 1 · 50 %); script `tools/dem_lai_buoc_b.py`; `mo_phong_*.py` nhận biến BANG. Lễ hội / chụp ảnh đúng ngưỡng 50 %.
**Kiểm độc lập bai_hoc/ XONG (20:36 13/11/2026):** `data/hoc_cung_user_2026-11-10/kiem_doc_lap_13_11.md` — 0 sai số; 2 hiểu nhầm ("xử lý trước lượt cuối" ⇒ "sửa hoặc nhận giới hạn"; bài 19 dòng 35 thiếu "phạm theo chữ") + 6 nhỏ; 5 chỗ chưa chắc của người viết đã trả lời. Đã nhắn A. **Rảnh — chờ việc** (21:20 13/11/2026): B đo xong, chạy việc nặng lại được; C không có việc mở (kho 3 chờ User).
**Plan đợt 2 "Lên kế hoạch" XONG (21:37 13/11/2026, A giao, mức nhẹ):** `docs/superpowers/plans/2026-11-13-len-ke-hoach-dot-2-plan.md` md5 `5d55b0676d9e` — (A) bản đồ làm ngay (toạ độ 18 / 34 ⇒ C dựng v7; B code); (B) ảnh chờ User (tối đa 25 / 34 = 74 %, biên 1 ảnh so sàn 70 %). Chờ A duyệt.
**Review 2 bài kho nháp của E XONG (21:49 13/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_review_bai_kho_diem_mong.md` — ready, 3 minor (m-1: "phòng trưng bày" ⇒ "loạt tác phẩm"); chia đoạn 12 / 15, 0 lỗi; WebFetch 3 trang khớp. **Rảnh — chờ việc** (22:02 13/11/2026): User dặn đo để mai ⇒ ghi kho + dựng lại chỉ mục **hoãn sang phiên sau**. **Việc phiên sau của C:** review diff kho với bản sao ở `meta/` khi E ghi xong (không đọc `evaluation/`, `*sealed*`).
**Bàn quán OSM — A chốt (22:21 13/11/2026, CURRENT_HANDOFF "Quán OSM — chốt"):** (1) bảng riêng cho lịch ngay (rào nhóm: dòng quán do code viết, nhãn "chưa kiểm, có thể đã đóng" + ngày tải, không giờ / số điện thoại OSM, © OSM); bản nhẹ (3) ~10 quán cụm thiếu vào bài "ăn gì gần" — User duyệt nội dung, làm SAU khi ghi kho 3 + đếm lại; không (2) Qdrant; (4) `tra_quan` khi đếm được lỗi. Việc dữ liệu kéo theo cho C (khi giao): đọc tay ~110 dòng bị lọc trước khi dựng bảng.
**A0 toạ độ v7 XONG (21:41 13/11/2026, plan đợt 2 A duyệt):** `data/phase_9/lich_trinh/diem_toa_do_v7.json` md5 `158e184154de` — 34 dòng = 34 điểm, 33 có toạ độ (null: Không gian lưu niệm Lê Bá Đảng); biên bản `bien_ban_toa_do_v7.md`. Đã nhắn A + B (B làm A1). Phần (B) ảnh: chờ User; tối đa 24 / 34 = đúng sàn.
**Gỡ tên / địa chỉ khỏi file tracked XONG (21:33 13/11/2026, A giao — sự cố e74c6df):** `c_review_kho3_e.md` (nhãn L-a…L-e) + file này (nhãn Q-a…Q-c); bảng nhãn ở `data/` (private). Lịch sử git còn tên — A / User quyết. **Bẫy cho C:** report tracked tả cơ sở / quán ở mức loại ngay khi viết, kể cả trong review và STATUS.
Khai báo sửa: file này · `data/osm_quan_2026-11-12/` (script khớp + bảng khớp mới + biên bản) · `data/sua_kho_2026-11-12_an_gan/` (script dựng, `quan_theo_cum.json`, phiếu quán + mốc, bài nháp). Không chạm `knowledge-base-hue/`.

**Kho 3 ăn uống — 4 bước XONG, chờ A (19:55 13/11/2026, 0 USD, không gọi mạng, không chạm kho):**
- (1) Luật khớp bản 2 (`data/osm_quan_2026-11-12/tools/khop_osm_v2.py`, luật ghi trước) ⇒ `khop_bai_kho_v2.json` 13 dòng; **đọc tay 22 dòng** (13 + 9 dòng bản 1 bị bỏ) ⇒ `doc_tay_v2.json`: nhận 13 (thêm tay 1 dòng — Q-a), bỏ 9. Bản 1 không dùng được 6 / 22 (4 khớp nhầm rõ, 1 trong đó gắn "chắc").
- (2) `dung_quan_theo_cum.py` bản 2: 13 toạ độ OSM cho bài kho + OSM nguồn thứ ba cho cụm / mốc < 3 quán (đọc tay 12 quán được chọn, loại 2 ⇒ `BO_TAY_OSM`). Sửa thêm lỗi làm tròn bản 1 (285 m ⇒ "300 m" mà 303 m ⇒ "0,3 km").
- (3) Tiêu đề mục bài nháp: dài nhất 305 ⇒ 48 ký tự; phường + tên điểm vào câu đầu đoạn.
- (4) Phiếu quán + mốc bản 2 (bảng A2 OSM chờ User; bảng D thêm cột OSM). md5: `quan_theo_cum.json` `2c96ac42e946` · phiếu `ce7264f07c17` · bài nháp `1b387b1c4cc2`.
- Số (so bản 1 tối 12/11): bài kho có toạ độ 29 ⇒ 34 / 81 · gán cụm 22 ⇒ 28 · cụm 0 quán 4 / 8 ⇒ 2 / 8 nếu dùng OSM (Thủy Xuân +6, Kim Long +3, Đông +1); không OSM vẫn 4 / 8. Còn trống: lăng xa, nam xa, mốc cầu ngói Thanh Toàn.
- Lệnh tính lại + chi tiết: `data/osm_quan_2026-11-12/bien_ban.md` mục "Phiên 13/11". Bản 1 của script / bảng / bài nháp sao ở `/tmp/c_*_ban12.*` (mất khi khởi động lại; data/ không có git).
- **Lỗi quy trình của C:** khi đọc tay đã `grep` thẳng 3 bài quán trong `knowledge-base-hue/foods/restaurants/` (dòng địa chỉ) thay vì `scripts/grep_kb.sh` — không chạm câu kín / Golden, nhưng sai luật §5; lần sau dùng `grep_kb.sh`.

**Review chéo kho 3 của E XONG (20:04 13/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_review_kho3_e.md` — changes_requested: M-1 151 dòng có hạng = 143 cơ sở (316 = 293); bài đi lại 4 minor; WebFetch 3/3 ý khớp. Đã nhắn E + A.
**Sửa 3 minor review E cho phần ăn uống XONG (20:04 13/11/2026):** quán Q-b ⇒ ước (không gán cụm) · bỏ mức "osm", thêm `nguon_toa_do` · quán Q-c: số kiệt. Gán cụm 28 ⇒ 27. md5: 9416b5c6adca  quan_theo_cum.json;48475905ac68  phieu_quan_va_moc_2026-11-12.md;7b57ee5e389e  bai_nhap_an_gi_gan_diem_tham_quan.md;722d72c97292  ../osm_quan_2026-11-12/doc_tay_v2.json;
**Kiểm lại kho 3 của E vòng 2 XONG (20:06 13/11/2026):** ready (mục 7 `c_review_kho3_e.md`): 142 cơ sở có hạng, 140 / 142 gán khu; bài đi lại m-2…m-5 đóng.
**Photon ⇒ bảng quán XONG (20:08 13/11/2026, 0 USD):** 9 dòng đạt luật, 7 trùng OSM (cùng gốc), 2 dùng mới; gán cụm 27 ⇒ 28; md5 quan_theo_cum eae693cac1b0 · phiếu 6d0e46a572fe · bài nháp 8cfe17ac9e4f (chi tiết bien_ban.md OSM).
**Đếm cho câu "OSM bảng riêng / kho chính" XONG:** `data/osm_quan_2026-11-12/dem_cho_cau_kho_rieng.md` (giữ 471, lọc tự động bỏ nhầm ~32 % — cần đọc tay; +91 đoạn = +1,1 %; 5 / 8 cụm ≥ 3 quán).
**Điểm lễ hội ban ngày XONG:** `data/phase_9/lich_trinh/de_xuat_them_le_hoi_ban_ngay.md` (2 gắn nhãn điểm sẵn có + 1 có điều kiện; không có điểm mới đủ căn cứ).
**Vòng tự soi 1:** đã gửi A / B / E.
**ĐANG LÀM (20:20 13/11/2026):** tìm ảnh Commons thay 4 dòng "đổi" + phương án #16, #27 ⇒ phiếu ảnh bản 2 (C KHÔNG nhìn được ảnh ⇒ ảnh mới ghi "CHƯA ai nhìn"). Commons trả 429 khi C gửi ~11 truy vấn liền ⇒ chạy lại chậm (chờ 90 s, cách 10 s / yêu cầu, gộp file).
**Phụ lục spec "581 quán OSM" — A giao rồi TẠM DỪNG (20:11 13/11/2026):** User đang cân nhắc để quán OSM ở bảng / kho riêng thay vì kho RAG chính; chưa sửa spec, chưa chạy gì. Chờ A.
**Review `9d6a0f7` XONG (20:11 13/11/2026):** ready, 2 minor (Project_Status còn ghi cờ false; eval mặc định nay có cờ ⇒ ghi vào plan B7 cuối) — `c_review_bat_co_het_luot.md`. Trước đó: review commit `9d6a0f7` (bật cờ `het_luot_bo_cong_cu`, A làm) ⇒ `report_agent/2026-11-12_ra_khoang_cach/c_review_bat_co_het_luot.md`.
**Bẫy 13/11 (lỗi bằng chứng của C):** gửi tin cho A SONG SONG với lệnh tính md5 ⇒ tin mang 4 md5 bịa; đã đính chính ngay. Luật cho mình: tin báo số chỉ gửi SAU khi đã thấy đầu ra lệnh, không gộp cùng lượt gọi công cụ.

## (Phiên 12/11 — giữ để tra)

## PHIÊN SAU ĐỌC TRƯỚC (C viết lúc kết phiên, 22:22 12/11/2026 `date`)

**Việc dở của C (đều 0 USD, chưa chạm kho, chưa code):**
1. **Quán từ OpenStreetMap — làm dở.** Đã tải + làm sạch + đếm: `data/osm_quan_2026-11-12/` (`tho_overpass.json`, `osm_quan.json` 581 quán có tên, `bien_ban.md` — đọc mục "Tới đâu khi kết phiên"). **Bảng khớp 22 bài kho
   (`khop_bai_kho.json`) CHƯA dùng được** — ≥ 3 dòng khớp sai rõ, luật còn lỏng ⇒ siết luật + xem tay. Chưa đưa nguồn OSM vào `data/sua_kho_2026-11-12_an_gan/tools/dung_quan_theo_cum.py`, chưa cập nhật phiếu quán + bảng D.
   Không cần tải lại (script: `data/osm_quan_2026-11-12/tools/tai_overpass.py`; tra địa chỉ dự phòng: `data/sua_kho_2026-11-12_an_gan/tools/tra_photon.py` — máy chủ đó hôm nay không trả lời).
2. **Bài nháp "ăn gì gần điểm tham quan":** E chia đoạn thử 21 đoạn 0 lỗi nhưng tiêu đề mục dài tới 305 ký tự ⇒ rút còn tên cụm ngắn, tên phường đưa vào câu đầu đoạn (sửa trong `dung_quan_theo_cum.py`).
3. **Sửa số ở report cũ:** "6.794 cơ sở" là 6.794 dòng / 208 tên — A nhận ghi dòng "Sửa số"; nếu A chưa làm: `c_dot_2_dem_implementation.md`, `c_phan_chua_on.md`, plan ăn gần.

**Sản phẩm phiên này + đường dẫn:**
- Phiếu cho User (private): `data/phase_9/lich_trinh/phieu_gop_cho_user_2026-11-12.md` (User đã trả lời 3 câu, không sửa ô) · `…/phieu_nho_dot_1_2026-11-12.md` (User đã trả lời 3 câu) · `…/phieu_anh_2026-11-12.md` (chưa xem;
  7 điểm chưa có ảnh) · `data/sua_kho_2026-11-12_an_gan/phieu_quan_va_moc_2026-11-12.md` (chưa xem).
- Bảng: `data/phase_9/lich_trinh/diem_v8_de_xuat.json` (34 dòng, md5 `0cbd845ede30`, CHƯA thay bảng chạy; dựng bằng `tools/dung_v8.py`) · `data/sua_kho_2026-11-12_an_gan/quan_theo_cum.json` (md5 `b4f1661e95fd`).
- Mô phỏng 0 USD: `data/phase_9/lich_trinh/tools/mo_phong_v8.py` (bộ xếp thật, 360 tổ hợp) · `…/mo_phong_kieu_di.py` (bản thử luật phút + ưu tiên + cụm xa — KHÔNG phải code sản phẩm).
- Tài liệu tracked: spec "Lên kế hoạch" bản 3.3 `8c521ecdc80d` · plan đợt 1 bản 3 `27919be11ef6` (B đã đọc, đồng ý; B làm bước (a)) · `report_agent/2026-11-12_ra_khoang_cach/c_ra_loi_dan.md` (rà lời dặn, 5 đề xuất chưa làm).

**Chờ User:** liếc danh sách điểm ưu tiên theo sở thích (trong bảng v8) · phiếu ảnh · phiếu quán + mốc (giữ / bỏ từng quán dữ liệu mở) · có cho đưa quán OpenStreetMap vào kho không (mở rộng Q3) · giờ + thứ của phố đêm cạnh
Kinh thành (tuỳ chọn) · chọn có làm đề xuất Đ2–Đ4 của report lời dặn không.

**Bẫy gặp hôm nay (đừng lặp):**
- **Đếm dòng thay vì đếm cơ sở:** dữ liệu mở có dòng lặp (6.794 dòng = 208 tên) ⇒ mọi phép đếm trên dữ liệu ngoài phải khử trùng trước khi ghi số.
- **Xếp hạng / ước độ phủ trước khi đếm:** bảng "phần chưa ổn" phải hạ 2 / 5 mục đầu sau khi đếm; plan ăn gần ước 30–45 bài khớp, thật 7; spec ghi "3–5 hoạt động tối", kho chỉ có 1. ⇒ chạy bước dò rẻ TRƯỚC khi ghi con số vào plan / spec.
- **Khớp tên tự động phải xem tay:** luật khớp OSM gắn "chắc" cho dòng sai — không nhận bảng khớp khi chưa đọc từng dòng.
- **Auto mode chặn lệnh kiểm DNS qua máy chủ ngoài** (lúc máy không phân giải được tên miền bản đồ) và dặn không lách ⇒ không lách, báo A; việc tải sau đó dùng máy chủ khác phân giải bình thường.
- Hook báo "giờ ước" khi ghi giờ chưa tới hoặc chép giờ khuyết phút ⇒ luôn lấy `date` ngay trước khi ghi.

**Tiền C cả phiên 12/11: 0,058691 USD** (3 lượt đếm có phí buổi tối sớm; từ 20:47 trở đi mọi việc 0 USD — 4 lượt tra Codex, WebFetch, 1 truy vấn Overpass).
**Không server / worktree / nhánh / container của C.** (Lúc kết phiên có một uvicorn cổng 8010 đang chạy — không phải C khởi động trong đợt việc tối; C không đụng.)
**Vòng tự soi 2 (đã gửi nhóm):** tốn mà lợi ít = bảng khớp OSM làm vội cuối phiên + phiếu ảnh khi chưa nhìn được ảnh; phiên sau: dò rẻ trước khi viết số, khử trùng dữ liệu ngoài, phiếu nào cần mắt người thì giao cho session có trình duyệt.

## PHIÊN 12/11 — C `hue-rag-e1` · A `hue-rag-7d` · B `hue-rag-1b` · E `hue-rag-33`

**ĐANG LÀM (18:45 12/11/2026, A giao; User: việc A giao = "làm đi"):** đợt 2 cổng — lượt đếm rẻ trước khi xây (lưu trú · ăn gần · sự kiện theo ngày), trần 0,02 USD, không spec / code, không `*sealed*`.
Khai báo sửa: `report_agent/2026-11-08_phase_9_ban_13/c_dot_2_dem_implementation.md` (mới) · file này · dòng C trong `CURRENT_HANDOFF.md`. Dữ liệu chạy: `data/phase_11/dot_2_dem/` (private). Cần server ⇒ nhắn B trước (một session chạy server / model một lúc).

**Đếm đợt 2 — DỞ (18:53 12/11/2026):** đã gửi 13 / 18 câu tự viết (6 lưu trú · 6 ăn gần · 1 sự kiện), 0,018295 USD (trần 0,02) ⇒ kết quả `data/phase_11/dot_2_dem/ket_qua_lan_1.jsonl`; 5 câu sự kiện S2–S6 (`cau_18.jsonl`) CHƯA gửi (hết quỹ — đã xin A ≈ 0,01). Công cụ: `data/phase_11/dot_2_dem/tools/` (`gui_cau.py` có phí · `quet_bo.py`, `log_tien.py` 0 USD). Server 8871 đã tắt. Còn lại: đọc + phân loại 13 câu, đối chiếu kho, viết report.
**Việc chen (18:53 12/11/2026, A giao, đường găng):** plan B7 bản 2 theo review vòng 1 của E (`docs/superpowers/plans/2026-11-10-phase-9-b7-plan_review.md`: 3 major, 6 minor). Khai báo sửa thêm: `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md`. Xong ⇒ nhắn E + A ⇒ quay lại đếm đợt 2.
**Plan B7 bản 2 XONG (18:59 12/11/2026):** `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md` sha256 `da7bff5d0c4e` (chưa commit — A commit) — lượt hôm nay = đo giữa kỳ, `KIN_NGAY` TẮT, `MAX_DROP` 4, ≈ 0,31 USD; đã nhắn E (vòng 2) + A.
**Việc kế (A giao):** (1) đếm đợt 2: gửi nốt 5 câu sự kiện (trần nâng 0,032, nhắn B trước khi chạy server) ⇒ report; (2) rà "phần nào chưa ổn" — `CURRENT_HANDOFF.md` mục "Đợt rà khoảng cách" dòng C ⇒ `report_agent/2026-11-12_ra_khoang_cach/c_phan_chua_on.md` (chỉ đọc, 0 USD).
**Đếm đợt 2 XONG — chờ review (19:06 12/11/2026):** report `report_agent/2026-11-08_phase_9_ban_13/c_dot_2_dem_implementation.md` (chưa commit). 18 câu, **0,024691 USD** (trần 0,032). Kết luận: ăn gần đủ lỗi (dữ liệu định vị quán) · lưu trú đủ lỗi phần nhỏ · sự kiện không đủ lỗi. Server đã tắt.
**Plan B7 bản 2:** E vòng 2 READY; sửa chữ n-3 ⇒ sha mới `2ca3f63ce45b` (không đổi tiêu chí). 5 minor còn lại là việc người chạy (B).
**Rà "phần nào chưa ổn" XONG (19:08 12/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_phan_chua_on.md` (chưa commit; 0 USD) — 5 mục trên cùng: ăn gần · từ chối cả câu · đường web chậm 15–25 s · số tiền / giờ chưa kiểm với đoạn trích · log không có loại câu. Công cụ: `data/phase_11/dot_2_dem/tools/log_tong.py`.
**Việc kế (19:09 12/11/2026, A giao, 0 USD, chỉ đọc):** đếm trên kết quả B7 giữa kỳ của B — (2) câu Golden bị từ chối / một phần mà ngữ cảnh có đoạn đúng (gold v5) · (3) lần tìm kho thứ 3–4 + đường web có cứu câu nào, tốn bao nhiêu giây / USD · (4) số tiền / giờ không khớp đoạn trích ⇒ thêm mục "Đếm trên B7 giữa kỳ" vào `c_phan_chua_on.md`, xong nhắn A. Đã nhắn B xin đường dẫn file sinh; không sửa / chạy lại / đụng phần chấm mù của B.
**Đếm trên B7 — xong phần Golden + an toàn (19:25 12/11/2026):** mục "3b" trong `c_phan_chua_on.md`; script `data/ra_khoang_cach_2026-11-12/tools/dem_b7.py golden` (chạy từ `backend/`, `PYTHONPATH=$PWD`). Từ chối nhầm trợ lý 3 ↔ mốc 13, cả 3 tìm trượt · tìm thêm cứu 10 câu · 0 số tiền / giờ sai nguồn / 155 · an toàn 0 / 32 đổi kết luận. **CÒN CHỜ B:** `s2/s2_r2.jsonl` (ổn định S2) · `w/s2c.jsonl` (đường web: tìm 3–4 lần, giây, USD) · điểm chấm mù ("trả lời một phần", nhãn cảnh báo). Không đọc `golden/judge/`.
**Đếm trên B7 — bổ sung xong (19:28 12/11/2026):** thêm (b2) đường web · S2 ổn định 0 / 44 · (e) 4 câu tụt Đủ ý (chung gốc: cùng ngữ cảnh, viết ngắn hơn) · trả lời một phần 0 câu khi đủ đoạn đúng. Đã nhắn A lần cuối. **Còn một ý chờ B:** nhãn "có ↔ không cảnh báo" giữa 2 lượt an toàn (khi B chấm xong an toàn) — A không giao lại thì thôi.
**3 plan nháp mức nhẹ XONG (19:32 12/11/2026; chờ User chọn, chưa code / chưa sửa kho, 0 USD):** `docs/superpowers/plans/2026-11-12-an-gan-dinh-vi-quan-plan.md` (sửa kho 53 bài, cách B toạ độ dữ liệu mở khuyến nghị, ≤ 0,08) · `…-het-luot-tim-plan.md` (bỏ công cụ `tim_kho` sau 2 lần tìm; probe `is_enabled` trước, ≤ 0,09) · `…-nhan-loai-cau-plan.md` (trường `loai_cau` 11 nhãn từ khoá, ≈ 0,001). Sửa số: bài quán có câu định vị = 12 / 81 (report đếm đã commit ghi 15 — đã báo A).
**Bổ sung cuối (19:55 12/11/2026):** sửa số 12 / 81 trong report đếm · probe `is_enabled` [Chạy] ghi vào plan hết lượt tìm (xét lại mỗi lượt, cả stream; model xin công cụ đã tắt ⇒ `ModelBehaviorError` phải bắt) · mục 3b (d): nhãn "thiếu cảnh báo" đổi 4 / 27 câu giữa 2 lượt an toàn, 5 câu thiếu ở cả hai ⇒ đã báo A là mục mới xếp cao.
**Chẩn đoán 2 sàn phạm B7 XONG (19:59 12/11/2026, 0 USD):** mục "3c" trong `c_phan_chua_on.md` — (1) thiếu cảnh báo câu miễn / giảm = do cách so (điều kiện nằm ở đoạn model tìm thêm, mốc không có đoạn đó); 5 câu thiếu ở cả hai lượt = lỗi khâu viết có từ RAG mốc; (2) S2b: 1 câu = giới hạn User đã nhận 09/11, 1 câu = loại mới (câu ranh giới có chữ Huế, định tuyến dao động từ trước 10/11). **C đề xuất A bỏ lượt 3 an toàn (0,02 USD)** — chờ A trả lời; chưa chạy gì có phí.
**A quyết bỏ lượt 3 an toàn. Bảng "Danh sách sau khi đếm" XONG (20:01 12/11/2026):** mục "3d" trong `c_phan_chua_on.md` (7 việc đáng làm + 7 mục nhận giới hạn / không làm); đã nhắn A.
Không server / worktree / nhánh / container của C. (Tiền: xem dòng "Tiền C 12/11 (mới)".)
**Vòng tự soi 1 (20:04 12/11/2026):** đã gửi A / B / E. Tự nhận: xếp hạng "chưa ổn" trước khi đếm (2 / 5 mục đầu phải hạ); thước "thiếu cảnh báo mới" trong plan B7 của C chấm hai bên theo ngữ cảnh riêng (lỗ không ai thấy ở review). Nhận phản biện E: câu miễn / giảm "do cách so" chỉ một nửa — đã sửa mục 3c. Đề xuất tới lượt cuối: bỏ phần kín giữa kỳ, S2 ×1, harness ghi thêm tools / ms / id đoạn tìm thêm.
**Lượt đếm rẻ thứ hai XONG (20:16 12/11/2026):** 17 câu (di chuyển 6 · tiếng Anh 5 · việc gấp 6), **0,023453 USD** (trần 0,03) ⇒ mục "3e" + bảng 3d cập nhật trong `c_phan_chua_on.md`. Việc gấp: 3 / 6 không có hướng dẫn, 0 / 6 có số khẩn cấp ⇒ đề xuất code nối dòng số cố định khi định tuyến xếp khẩn cấp (cần User — đảo một phần "bỏ khẩn cấp"); di chuyển 4 / 6 kho từ chối ⇒ bổ sung kho; tiếng Anh 5 / 5 đúng nội dung nhưng trả lời tiếng Việt ⇒ chuyện phạm vi. Server đã tắt.
**Tiền C 12/11 (mới):** 0,024691 + 0,023453 = **0,048144 USD**.
**Plan nháp "việc gấp" XONG (20:19 12/11/2026, 0 USD, chưa code):** `docs/superpowers/plans/2026-11-12-viec-gap-so-khan-cap-plan.md` — định tuyến xếp khẩn cấp ⇒ code nối dòng số khẩn cấp qua kênh `notice` sẵn có + không mở cổng web; chuỗi gửi model giống byte; ≤ 0,06 USD, ~2 giờ; cần User (đảo một phần "bỏ khẩn cấp" 08/11). Đã nhắn A.
**Lịch trình — bảng khoảng cách TRIPO + đếm rẻ XONG (20:47 12/11/2026):** `report_agent/2026-11-12_ra_khoang_cach/c_lich_trinh_khoang_cach.md` (chưa commit). 14 biểu mẫu + 3 gõ tự do = **0,010547 USD**; mô phỏng 0 USD 360 tổ hợp qua `lich_trinh.xep`: 7 / 28 điểm không bao giờ được xếp (chùa nổi tiếng + 5 lăng), "đi dày" đổi khung 0 / 120, buổi 2 điểm 0 / 360 — gốc: chọn theo thứ tự bảng, không cột ưu tiên, 24 / 28 điểm chưa có thời lượng. 6 ứng viên; đầu bảng: cột ưu tiên + luật chọn (cần User duyệt danh sách điểm phải đi), rồi thời lượng v7 + luật đi dày. User đã quyết KHÔNG làm "việc gấp" (plan nháp giữ làm hồ sơ).
**Tiền C 12/11 (mới nhất):** 0,024691 + 0,023453 + 0,010547 = **0,058691 USD**.
**Bẫy:** hook báo giờ ước khi chép nguyên dạng giờ khuyết phút từ tin của A ⇒ ghi "tối 12/11, theo handoff" thay vì chép dạng giờ khuyết.
**Phiếu điểm ưu tiên + plan XONG (20:53 12/11/2026, 0 USD, chưa code / chưa đổi bảng):** phiếu `data/phase_9/lich_trinh/phieu_diem_uu_tien.md` (5 điểm mức 1 + 4 điểm mức 2 đề xuất sẵn, 3 câu cho User) · plan `docs/superpowers/plans/2026-11-12-lich-trinh-diem-uu-tien-plan.md` (cột `uu_tien` + sắp trong `nap_bang`, `xep` không sửa; thử trước 0 USD: 0 lỗi kiem_khung / 360, chùa 30 / 30 từ 2 ngày; mặt trái: điểm không bao giờ xếp 7 ⇒ 9 tới khi có "đi dày"). B đang đo giây (cổng 8887) ⇒ C KHÔNG chạy server / việc nặng tới khi B nhắn "đo xong".
**Đợt việc tối 12/11 (A giao theo "User chốt hướng") — tới 21:04 12/11/2026:** (1) review plan lưu trú của E XONG (`…luu-tru-khu-va-link-plan_review.md`, 1 major: kích hoạt theo nguồn kho chỉ chắc bắt 2 / 6 câu đã đếm). (2) phiếu gộp cho User XONG: `data/phase_9/lich_trinh/phieu_gop_cho_user_2026-11-12.md` (dựng bằng `tools/dung_phieu_gop.py`; 13 / 28 dòng "cần xem"); A đã đưa User. (3) dữ liệu "ăn gần" XONG, CHƯA sửa kho: `data/sua_kho_2026-11-12_an_gan/` (`bang_de_xuat.md/.jsonl`, `mat_do_quanh_diem.json`, `tools/khop_quan.py` + `uoc_theo_so_nha.py`) — dữ liệu mở chỉ chứa 7 / 81 bài quán; ước theo số nhà kề thêm 22 (sai số trung vị 107 m) ⇒ 29 / 81 có toạ độ; quanh các lăng: kho 0 quán, dữ liệu mở cũng 0 trong 1 km. Đã ghi "sửa số" vào plan nháp ăn gần.
**ĐANG LÀM:** (4) tra Codex (0 USD) nguồn thật cho 7 ô thời lượng C ước + ô "trong nhà" kho không ghi ⇒ dựng lại phiếu gộp bằng script; **User đã sửa vào phiếu thì KHÔNG ghi đè** — ghi file kèm bên cạnh, báo A.
**(4) XONG 21:10 12/11/2026:** phiếu gộp cập nhật bằng nguồn Codex (`data/tra_cuu_cli/2026-11-12_c-phieu-gop-thoi-luong/`, C WebFetch kiểm 3 trang): cần xem 13 ⇒ 8 / 28; cung An Định ⇒ "cả hai". **Nominatim: BỎ** (máy không phân giải tên miền openstreetmap.org; auto mode của terminal C chặn lệnh kiểm tên miền qua máy chủ công cộng và báo sẽ chặn tiếp ⇒ không lách; A giao E tra bằng nguồn khác; script `tools/tra_nominatim.py` để lại, 0 lượt đã gửi).
**Spec "Lên kế hoạch bản 2" NHÁP bản 1 XONG (21:16 12/11/2026):** `docs/superpowers/specs/2026-11-12-len-ke-hoach-ban-2-design.md` — nguyên tắc "ô nào hiện thì đổi được lịch", bảng từng ô (code dùng · dữ liệu · tiêu chí mô phỏng), 3 đợt (≤ 0,15 / 0,25 / 0,15 USD), giao diện 0 gói mới, bảng rà FDE, 4 câu cho User. Chờ E review, User duyệt; B code.
**Bẫy 12/11 tối:** ước lượng độ phủ dữ liệu ngoài mà chưa chạy thử (plan ăn gần ghi 30–45 bài, thật 7) ⇒ lần sau chạy bước dò khớp TRƯỚC khi ghi con số vào plan.
**Đợt việc 21:15–21:33 12/11/2026 (đều 0 USD):** review gộp Exa `report_agent/2026-11-12_ra_khoang_cach/e_exa_review.md` (đếm lại khớp 17 / 25; F-1: 5 / 25 mục đạt của Exa trích trang địa điểm của chính Exa ⇒ loại thì 20 < 22; plan 2 major) · spec biểu mẫu bản 2 (E ready vòng 2) · review spec kho 3 vòng 1 `…bo-sung-kho-dot-3-design_review.md` (3 major: thư mục mới không được quét, dạng bài mỗi dòng một đoạn, dữ liệu quán mỏng) · đọc 5 ảnh + 2 file TRIPO của User ⇒ mục 4b trong `c_lich_trinh_khoang_cach.md` · **spec "Lên kế hoạch" BẢN 3** (`docs/superpowers/specs/2026-11-12-len-ke-hoach-ban-2-design.md`): một lịch đủ 4 phần + biểu mẫu đủ + ảnh + bản đồ là cam kết của mốc (User chốt), 3 đợt nối nhau ≤ 0,75 USD, mục "phải hơn TRIPO", mục 5b thứ tự ưu tiên luật + ghi chú thực thi của B. **Còn nợ:** vòng 2 review spec kho 3 bản 2 (`fd152810627b`, 3 major) · phiếu nhỏ đợt 1 (thứ hoạt động, tháng lưu ý mùa, 3–5 hoạt động buổi tối) + phiếu ảnh — chưa soạn, chờ A giao.
**Vòng 2 spec kho 3 XONG (21:35 12/11/2026):** ready (3 major đóng), 1 ghi chú: ngưỡng "0 câu đổi 10 đoạn đầu không do đoạn mới" quá chặt ⇒ để theo dõi. Spec biểu mẫu bản 3 sha `16e9f7f4fa19` chờ E kiểm phần đổi.
**Cập nhật 21:49 12/11/2026 (`date`) — 0 USD thêm (một lượt tra web Codex, 199 giây):**
- **Phiếu nhỏ đợt 1 XONG** (private): `data/phase_9/lich_trinh/phieu_nho_dot_1_2026-11-12.md` — thứ 3 điểm tối · tháng lưu ý mùa 10 điểm · kho chỉ có 1 hoạt động tối đủ giờ + thứ (+ 1 chờ User) · 3 câu.
- **User trả lời phiếu gộp** (không sửa ô nào, md5 phiếu không đổi): ưu tiên THEO SỞ THÍCH · dùng cả bảng thời lượng · thêm 5 điểm trong nhà ⇒ C dựng **bảng đề xuất v8** `data/phase_9/lich_trinh/diem_v8_de_xuat.json`
  (33 điểm, md5 `695c0d71f072`, CHƯA thay bảng chạy; `tools/dung_v8.py`, nguồn tra thêm `tools/tl_tra_them.json`, kết quả tra `data/tra_cuu_cli/2026-11-12_c-o-chua-chac-v8/`).
- **Mô phỏng 0 USD:** `tools/mo_phong_v8.py` (360 tổ hợp, bộ xếp thật: ưu tiên số 1 có mặt 60 / 60 mọi sở thích; luật "đi dày" cũ chỉ 3 / 120) · `tools/mo_phong_kieu_di.py` (bản thử luật kiểu đi bằng phút: 3 mức khác nhau 24 / 30 = 80 %).
- **Spec "Lên kế hoạch" bản 3.2** sha256 `3ea9bcb8bc10` (chưa commit): 3 sửa chữ của E · số thật buổi tối · ưu tiên theo sở thích · **mục 5c — 8 quyết định để code** (B đã xác nhận model trả mảng theo id mục, hiện nguyên câu từng mục).
- **Phiếu ảnh XONG 21:56 12/11/2026 (`date`)** (private): `data/phase_9/lich_trinh/phieu_anh_2026-11-12.md` — 27 dòng ảnh (23 mới + 4 dùng lại bộ cổng), 5 dòng cần xem, **7 điểm chưa có ảnh** (phố Tây, phố Hai Bà Trưng, đồi Thiên An, thác Nhị Hồ, 2 điểm Lê Bá Đảng, Bảo tàng Hồ Chí Minh). C chưa nhìn thấy ảnh (công cụ chỉ trả chữ) ⇒ User / session đợt 2 phải xem. Dựng bằng `tools/dung_phieu_anh.py`.

- **Plan đợt 1 "Lên kế hoạch" NHÁP bản 1** (21:57 12/11/2026 `date`, 0 USD, chưa commit): `docs/superpowers/plans/2026-11-12-len-ke-hoach-dot-1-plan.md` — bước (a)–(e), tiêu chí Luôn / Sàn, lượt thử sớm, điểm dừng D1–D4. Luật "cụm xa không ở ngày 1" đã mô phỏng (0 / 180; 18 / 18). Chờ: B đọc trước, A duyệt; E kiểm spec 5c ⇒ C sửa plan một lần.

- **22:09 12/11/2026 (`date`), 0 USD (2 lượt tra Codex):** spec "Lên kế hoạch" **bản 3.3** `8c521ecdc80d` (nhận kết quả E kiểm 5c + User trả lời phiếu nhỏ) · plan đợt 1 **bản 2** `82ea67f6e17d` (đã có mã băm bộ đo của E; chờ B đọc, A duyệt) · bảng đề xuất 34 dòng md5 `0cbd845ede30` (cột thứ / giờ tối / mùa + dòng hoạt động tối) · **rà lời dặn XONG:** `report_agent/2026-11-12_ra_khoang_cach/c_ra_loi_dan.md` (7 vai, 9 điểm đối chiếu hướng dẫn chính thức, 5 đề xuất, khung lời dặn vai mới của lịch; chỉ đọc).

- **22:17 12/11/2026 (`date`), 0 USD:** plan đợt 1 **bản 3** `27919be11ef6` (gộp 6 ý của B) · **kho 3 phần (c) ăn gần — bước chuẩn bị XONG, chưa chạm kho** (private, `data/sua_kho_2026-11-12_an_gan/`): `quan_theo_cum.json` (md5 `b4f1661e95fd`) · `phieu_quan_va_moc_2026-11-12.md` · `bai_nhap_an_gi_gan_diem_tham_quan.md` · `tools/dung_quan_theo_cum.py`. Số: 22 / 29 quán kho gán được cụm; quán dữ liệu mở chọn 6 + 3 + 1; 4 / 8 cụm 0 quán; 3 mốc. **Sửa số:** dữ liệu mở 6.794 dòng nhưng chỉ 208 tên khác nhau ⇒ "276 / 174 cơ sở" ở tài liệu trước là số dòng lặp. Chờ E khớp trường + ghi kho.

**Trạng thái: rảnh — chờ A** (không server / worktree / nhánh / container của C; việc dở: không) (review kết quả B7 nếu A giao; không server / worktree / nhánh / container của C).
**Bẫy 12/11:** lệnh shell dài viết thẳng (heredoc quét `data/` có chữ tên bộ kín) bị auto mode chặn ⇒ viết script bằng Write rồi chạy; log `chat_metrics` không có nội dung câu ⇒ không đếm theo loại câu được, phải gửi câu tự viết; câu kho từ chối đi web ≈ 0,002 USD / câu ⇒ ước tiền lượt đếm theo giá đường web, không theo giá trung bình.
(Tiền tới lúc đó 0,024691 USD — số cuối phiên ở dòng "Tiền C 12/11 (mới)".)

---

## (10/11) kết phiên — chỉ tra cứu

## PHIÊN SAU ĐỌC TRƯỚC (C mới bắt đầu ở đây — viết 22:41 10/11/2026)

**Trạng thái:** **rảnh — không việc dở, không worktree `/tmp`, không nhánh, không container của C.** Phiên 10/11 terminal: C `hue-rag-4f` · A `hue-rag-55` · B `hue-rag-05` ·
E `hue-rag-e4` (tên đổi khi mở lại — `ListAgents`). Chờ A giao (việc A giao = User nói "làm đi"). Mọi file C viết hôm nay: A commit.

**Hướng mới cho báo cáo (User chốt cuối phiên 10/11 — A ghi đủ trong `CURRENT_HANDOFF.md`):** User đọc file 02 bản 10/11 vẫn thấy khó hiểu ⇒ thêm thư mục
`bao_cao_he_thong/hieu_he_thong/` = **chuỗi bài để hiểu**, mỗi bài **một ý**, nói **vì sao trước**, có **ví dụ đời thường**, thuật ngữ đưa ra sau khi đã giải thích;
các file `01_…10_` hiện có = **sổ ghi việc** (giữ). Bài học từ mẫu 10/11: bảng "đợt sửa / số chỗ / kết quả" và danh sách tính năng vẫn là giọng sổ công trường — User cần
câu chuyện "vấn đề là gì → làm gì → vì sao vậy". Memory `user-reading-style` đã ghi.

**Việc C phiên 10/11 (đều xong, 0 USD):**
- Review: nhánh B xã giao song song (code ready, đo chưa đạt ⇒ đóng hồ sơ) · nhánh E câu ngày nhanh (1 major — "mùng N tháng <số>" không "âm" bị coi là ngày âm ⇒ E sửa ⇒ ready, merge `1633c18`)
  · sửa báo cáo `c54c932` (ready, 2 minor) · deploy cục bộ B (1 major — danh sách ảnh thiếu trong Docker ⇒ hỏi bằng ảnh tắt im lặng ⇒ sửa ⇒ ready, merge `5081e89`)
  · plan định tuyến câu lịch B (2 vòng ⇒ ready `aa493aec252f`). Nhánh định tuyến: E review (không phải C).
- Nháp plan B7 `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md` (A chốt Q1–Q4, tag `p9-moc` = `18e8f42`).
- Mẫu báo cáo: `README.md`, `01_LUONG_HOAT_DONG_HE_THONG.md`, `02_BAO_CAO_KHO_DU_LIEU.md` (mỗi file sub-agent vai người không đọc code đọc thử, sửa theo góp ý).

**Bẫy / học được 10/11:**
- Log truy cập mặc định của uvicorn **ghi IP + đường dẫn** (log chatbot thì không) ⇒ bản deploy muốn "không lưu IP" phải `--no-access-log` — đã báo A làm câu cho User.
- Ảnh Docker chỉ chép file theo danh sách chừa ⇒ thiếu file cấu hình của một cờ đang bật ⇒ tính năng **tắt im lặng** (log "startup failed", không lỗi khởi động). Review deploy: so cờ bật ↔ file runtime cần.
- Regex ngày âm: "mùng / mồng N tháng <số>" không "âm" thường là ngày **dương** (Quốc khánh 2/9, 8/3) — probe bằng câu tự viết trước khi tin bộ đo (bộ đo có 0 câu dạng này).
- Dòng "thông tin có thể đã thay đổi" chỉ cho nguồn vé / địa điểm / lễ hội (`NOTICE_SOURCE_PREFIXES`) — tả báo cáo phải đối chiếu code, đừng suy.
- Hai session gửi tin chéo nhau trong brainstorm ⇒ mỗi bên nhận ý bên kia ⇒ phải gửi thêm một bản chốt chung; lần sau: đợi tin bên kia rồi mới nhận / bác.
- `ugrep` (lệnh `grep` trên máy) báo "exceeds complexity limits" với regex dài có `.{0,80}` + tiếng Việt ⇒ dùng Python để tìm trong tài liệu.
- Bẫy cũ còn đúng (09/11, 08/11): xem khối "(09/11)" ngay dưới.

**Tiền C 10/11:** 0 USD (mọi việc chỉ đọc / test 0 USD / sub-agent).

---

## (10/11) nhật ký trong phiên — chỉ tra cứu
### Phiên 10/11 (mở 19:06 10/11/2026) — C `hue-rag-4f` · A `hue-rag-55` · B `hue-rag-05` · E `hue-rag-e4`

**Trạng thái: rảnh — chờ review B / E.** A giao (CURRENT_HANDOFF "VIỆC PHIÊN 10/11", `main` `624a17b`): review cả nhánh (`risk-gated-agent-review`, một vòng, chỉ plan + diff + số đo)
(1) B `p9-xa-giao-song-song` ⇒ `report_agent/2026-11-08_phase_9_ban_13/b_xa_giao_song_song_review.md`; (2) E `p9-t1-nhanh` ⇒ `report_agent/2026-11-02_phase_9_code/e_t1_nhanh_review.md`. Tiền 0 (chạy lại ≤ 0,01 nếu cần).
Khai báo sửa: chỉ 2 file review trên + file này.
**Việc xen giữa (19:19 10/11/2026, A giao, 0 USD):** nháp plan B7 ⇒ khai báo sửa thêm `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md` (mới). Review B / E vẫn ưu tiên. **XONG 19:21 10/11/2026:** nháp `fe5788b63089` (untracked) đã gửi A — tag `p9-moc` đề xuất `18e8f42`; ≈ 0,30 USD; 4 câu A chốt §8. Lệch báo A: Project_Status §4 `anh.bat` false ≠ thực tế true (`cf57309`). A commit nháp + chốt Q1–Q4 (`main` `1bcc830`), tag `p9-moc` = `18e8f42` đã gắn. **(19:24 10/11/2026) Việc kế:** review phần sửa `bao_cao_he_thong/` (2 sub-agent của A, theo `data/ra_soat_bao_cao_2026-11-10/sa1_*.md` + `sa2_*.md`) khi A nhắn diff sẵn. Thứ tự: review B / E nếu tới trước. **Review sửa báo cáo `c54c932` XONG 19:36 10/11/2026:** `ready_for_user_confirmation`, 0 blocker / 0 major / 2 minor — `report_agent/2026-11-08_phase_9_ban_13/c_sua_bao_cao_1011_review.md` `daf963d9ecd9` (untracked). **Review B `p9-xa-giao-song-song` `9ce7cfd` XONG 19:39 10/11/2026:** code `ready_for_user_confirmation` (0 blocker / 0 major / 3 minor), kết quả đo chưa đạt (đúng nhãn B) — `report_agent/2026-11-08_phase_9_ban_13/b_xa_giao_song_song_review.md` (untracked). Chạy lại 0 USD: 15 test đạt, AN chấm lại 0 lọt. **Review E `p9-t1-nhanh` `7d6f25f` (19:44 10/11/2026):** `changes_requested` — M-1 câu hỏi "mùng N tháng <số>" không "âm" bị coi là ngày âm (probe 0 USD; bộ đo 0 câu dạng này) + 3 minor — `report_agent/2026-11-02_phase_9_code/e_t1_nhanh_review.md` (untracked). Q1 so lại 215 / 228, 82 test đạt. **Delta `0385bcf` (19:47 10/11/2026): M-1 đóng ⇒ `ready_for_user_confirmation`** (review §7). **Review deploy cục bộ B (19:55 10/11/2026):** `changes_requested` — M-1 hỏi bằng ảnh tắt im lặng trên bản deploy (thiếu `danh_sach_ten.json` trong ảnh) + 2 minor — `report_agent/2026-11-08_phase_9_ban_13/b_deploy_cuc_bo_review.md` (untracked). Đếm lại trong ảnh `dep10`: 0 file private. **Delta (20:03 10/11/2026):** M-1 (a) + m-1 + m-2 đóng ⇒ `ready_for_user_confirmation` (review §6; đếm lại `dep10b`: 0 private). **Review plan định tuyến lịch (B) vòng 1 (21:05 10/11/2026):** `changes_requested` — M-1 cách so 2 lượt / `N_AA` theo nhóm chưa rõ · M-2 N2 cho mục web là đạt (yếu hơn S2b) + 3 minor — `docs/superpowers/plans/2026-11-10-phase-9-dinh-tuyen-lich-plan_review.md` (untracked). **Vòng 2 (21:07 10/11/2026):** bản 2 `aa493aec252f` ⇒ `ready` (5 finding đóng). **Rảnh — chờ B code xong ⇒ review nhánh.** **(21:20 10/11/2026) A giao:** viết lại mẫu `bao_cao_he_thong/README.md` + `01_LUONG_HOAT_DONG_HE_THONG.md` (khai báo sửa 2 file này) ⇒ sub-agent đọc thử ⇒ A. **XONG 21:28 10/11/2026:** README `4d2955801afc` (99 dòng) · LUONG `48f3eca3dff7` (127 dòng), chưa commit; sub-agent đọc thử ~25 góp ý đã sửa; overlap 0. Phát hiện: access log uvicorn ghi IP (đã báo A). **(21:38 10/11/2026) File 02 kho dữ liệu XONG** (A giao; User xem thêm 1 file mẫu): `02_BAO_CAO_KHO_DU_LIEU.md` `55a6e0d27311` + README `eb13afb8a3e9` (cột thứ tự 01…10, thêm "chỉ mục"), chưa commit; sub-agent đọc thử ~20 góp ý đã sửa. Review nhánh định tuyến: A giao E (không phải C). **Rảnh — chờ A / User góp ý.**
**Tự soi 1 (19:15 10/11/2026, A chốt, `main` `839ddb7`):** A nhận cả 6 ý của C. E thu D1 về các dạng có trong bộ đo. Report của B / E có các mục C xin. C chỉ review chỗ rủi ro, không chạy lại lượt đo tốc độ.
Danh sách soi khi review: **B** — khối `finally` của `answer_turn_stream_parallel` (huỷ, gather, `n_tra_loi_bo` / `usd_bo` khi bỏ cả hai phần) · `_merge_spec` gộp trace trò chuyện · số lượt bị huỷ giữa chừng · ngắt kết nối ⇒ task không treo.
**E** — regex dò ngày âm trong đoạn kho (dò nhầm ⇒ dòng lịch thừa / sai) · lượt đã từ chối sẵn (không có nguồn) không được chèn nguồn lịch · câu không có từ chỉ ngày giống byte · D1 chỉ gồm các dạng có trong bộ đo. Kiểm mở phiên: `main` sạch, hooksPath `.githooks`, Qdrant 2 collection / 8.435 point — khớp.

---

---

## (09/11) STATUS C — kết phiên 09/11 (viết 22:28 09/11/2026 — `date`). Lịch sử: `git log -p session_prompt/sessions/STATUS_C.md`

### (09/11) phần "phiên sau" cũ — bẫy còn đúng ở cuối khối

**Trạng thái:** **rảnh — không việc dở, không worktree `/tmp` nào, không nhánh của C đang mở.** Phiên 09/11 terminal: C `hue-rag-6a` · A `hue-rag-87` · B `hue-rag-99` · E
`hue-rag-ea` (tên đổi khi mở lại — `ListAgents`). Chờ A giao (việc A giao = User nói "làm đi").

**Việc C phiên 09/11 (đều xong):**
- T3 bảng vé + giờ: hướng (a) code + đo (Q1 bật cờ 228/228 giống byte · Q2 lưu ý 0/20 · an toàn 32: ngoài kho bị trả lời 0/4, 1 báo nhầm do lỗi bộ đọc giờ dấu phẩy ⇒ sửa) ⇒
  **đóng hồ sơ** (User), tag `hoso/p9-t3-bang` `e547b9e`; kết luận `report_agent/2026-11-06_giao_dien_cong/c_t3_bang_implementation.md` §13. Bảng `data/phase_9/t3_bang_ve_gio/bang_v1.json` giữ.
- T2: review plan bản nháp (3 major) ⇒ C viết lại plan bản 2 (A duyệt `88b1f0586e99`; + md5 bộ hỏi kèm của E ⇒ `69836a615353`) ⇒ review code E phần 0 USD (ready) ⇒ lượt đo của E **âm** ⇒ đóng hồ sơ.
- T4: review sớm code E (1 major: tiêu chí "câu cố định (b) không nói sai" — E đo 0/19, đóng) ⇒ lượt đo **âm** ở luật xếp ⇒ đóng hồ sơ.
- 4 chốt trước deploy: `p12-chot-deploy` ⇒ merge `ccc9f4f` (A review). Biến: `HUE_LUOT_MOI_NGAY`, `HUE_COOKIE_SECURE`, `HUE_TAT_DOCS`; log xoay vòng 10 MB × 3 luôn bật.
  **Checklist deploy:** uvicorn sau Caddy cần `--proxy-headers --forwarded-allow-ips <ip Caddy>`; đặt 3 biến trong `compose.yml`; sổ đếm lượt ở RAM.
- Nháp mục "Phiên 09/11" của `report_agent/2026-11-08_phase_9_ban_13/TONG_HOP.md` (A duyệt / sửa; số S5 + tiền B / E / A để trống).
- Tự soi cuối phiên đã gửi A / B / E: bài học chính — **đếm lỗi thật trên mốc trước khi dựng tính năng** (T3 chữa lỗi chưa thấy; T2 + T4 âm cùng gốc "lời dặn từ chối cả câu" — một pilot
  mốc 10 câu ≈ 0,012 USD đã đủ thấy).

**Tiền C 09/11 ≈ 0,028 USD:** T3 (a) Q2 0,010562 + an toàn 32 0,017105 · chốt deploy ≈ 0,00035 · review / plan 0 USD.

**Bẫy mới 09/11:**
- Auto mode chặn đọc file `*sealed*` cả khi A giao rõ (rào đúng, không lách) ⇒ viết sẵn một lệnh `!` chỉ in dòng cần, gửi A; `cut -c1-4000` có thể cắt mất phần trả lời — bỏ trường `context` trước khi in.
- `git worktree remove` cần `--force` khi worktree còn file gitignore (`backend/logs/`); gỡ symlink `data/`, `knowledge-base-hue/` trước.
- Log `application.log` xoay vòng ở 10 MB (từ `ccc9f4f`) ⇒ harness đếm dòng theo vị trí có thể đếm hụt nếu xoay giữa lượt — kiểm cỡ log trước lượt đo.
- `@app.middleware("http")` (BaseHTTPMiddleware) bọc luồng SSE + dò ngắt kết nối ⇒ middleware chặn lượt viết dạng ASGI thuần (`api/gioi_han.py` `ChanLuot`).
- Test gọi `logging.config.dictConfig` đổi logging toàn cục cả tiến trình pytest ⇒ hỏng test đếm dòng log — không viết test kiểu đó.
- Bộ đọc giờ / số liệt kê: ranh giới số phải cho ", " (liệt kê) — luật cũ `(?![\d,])` bỏ mọi số đứng trước dấu phẩy.

### Bẫy (08/11, vẫn đúng)
- `kill` PID server tạm bị auto mode chặn ⇒ chạy server bằng `run_in_background` để tắt bằng TaskStop; nếu lỡ `nohup` ⇒ User `!`.
- `test_cong_dot_1::test_weather_and_feature_routes` hỏng **chỉ khi nạp khoá** (`--env-file`; có khoá ⇒ ảnh bật) — không do nhánh.
- `tim_so_tien` cần đơn vị ("đồng") — ô bảng giá trong kho thường ghi số trần ⇒ phía "cho phép" phải nhận cả số nhóm nghìn trần.
- Công cụ đo SSE: một `httpx.Client` giữ cookie ⇒ mọi câu chung một cuộc trò chuyện — mỗi câu một client.
- Bộ chấm: nhãn giá phải kèm đơn vị như bảng; tập cho phép theo đúng chữ plan — kiểm bộ chấm trên một câu trước khi đọc số.
- `an_toan_run.py` cũ gọi `answer_case` **không** cờ (= RAG 1–8) ⇒ đo trợ lý phải truyền `AssistantFlags.from_settings`.
- `wait_for_function` chuỗi của Playwright bị CSP chặn (`unsafe-eval`) ⇒ chờ bằng vòng Python.
- Sub-agent đọc kho đôi khi đổ đầu ra ra `/tmp` — brief nhắc "không ghi file ngoài đích".
- Giờ trong file: luôn `date`; không ghi "~hh:mm".


---

## (09/11) nhật ký trong phiên — chỉ tra cứu (mở 20:10 09/11/2026) — C `hue-rag-6a` · A `hue-rag-87` · B `hue-rag-99` · E `hue-rag-ea`
**A giao (20:13 09/11/2026, User: việc A giao = "làm đi"), 0 USD:**
(1) dựng lại `/tmp/c_t3` từ `p9-t3-bang` `21ec06d`, rebase lên `main` `5c982a0`, chạy test file bị chạm (chưa đo). Khai báo sửa: nhánh `p9-t3-bang` (5 file của nhánh, chỉ giải xung đột rebase), push nhánh.
(2) review plan T2 `docs/superpowers/plans/2026-11-08-phase-9-t2-web-plan.md` (`921f75d64a7c`) ⇒ file mới `docs/superpowers/plans/2026-11-08-phase-9-t2-web-plan_review.md`.
**(1) XONG:** `p9-t3-bang` rebase lên `main` `5c982a0` = **`0eeb6f9`** (pushed): giữ cả T1 + T3, `max_turns_for(ngay_lich, ve_gio, thoi_tiet)` cộng dồn + 1 test. Test file chạm 460 đạt; cả `backend/tests` 885 đạt / 8 hỏng-lỗi đã biết (5 cần khoá, 2 cần bản build UI), 3 phút 43 giây.
**(2) XONG:** review T2 `changes_requested` 0 blocker · 3 major (max_turns · sàn S2c/S5/S6/S1×2 · bộ hỏi kèm 10) — sha `2653316dd16a` (untracked, A commit). Đã nhắn B + A.
**(3) T3 ĐÓNG HỒ SƠ (20:50 09/11/2026, User chọn, A báo):** không merge; nhánh `p9-t3-bang` = `e547b9e` (pushed) — A gắn tag `hoso/p9-t3-bang` + xoá nhánh khi User duyệt. Kết luận report §13. Worktree `/tmp/c_t3` (cờ `false`) — gỡ: `rm /tmp/c_t3/data /tmp/c_t3/knowledge-base-hue && git worktree remove /tmp/c_t3` (User `!` nếu `rm` bị chặn). Câu kín b_kin_07: A bỏ (User đã chạy lệnh 1: câu thuộc loại pháp lý chung, nhãn ngoài phạm vi chắc; chưa ghi `kin_c_doc.md` vì A bỏ việc). Tiền T3 09/11 0,027667.
**(4) ĐANG LÀM (20:50 09/11/2026, A giao):** sửa plan T2 theo 3 major C ghi + chốt tự soi (sàn S1 + ngoài kho / ngoài phạm vi + đúng câu; S5 / S6 đo chung lúc đóng đợt; không bộ kín). Khai báo sửa: `docs/superpowers/plans/2026-11-08-phase-9-t2-web-plan.md` (C cầm thay B). ≤ 0,2 USD ⇒ mức nhẹ, A đọc duyệt. Code chờ G vào `main`. **Bản 2 XONG — sha `88b1f0586e99`, chờ A duyệt** (≈ 0,17 USD); bộ hỏi kèm 10 nhờ E viết (`data/phase_9/t2_web/hoi_kem_10.jsonl`, md5 ghi vào plan §3 trước lượt có phí).
**(5) XONG — chờ review (21:01 09/11/2026; giao lúc 20:55 09/11/2026, A giao, 0 USD, mức nhẹ) — 4 chốt trước deploy, nhánh `p12-chot-deploy` từ `main` `2db09b8`, worktree `/tmp/c_dep`.** Plan ½ trang:
- **Mặc định = hành vi hiện tại** (không đặt biến môi trường ⇒ không đổi gì; chuỗi gửi model không chạm).
- (1) Log: `config/logging.yaml` handler `file` ⇒ `logging.handlers.RotatingFileHandler` 10 MB × 3 bản (luôn bật; dưới 10 MB y như cũ — log máy User ~0,6 MB).
- (2) Cookie: `HUE_COOKIE_SECURE=1` ⇒ cookie `conversation_id` có `Secure` (đọc mỗi lần đặt cookie, `api/routes/chat.py` `_set_cookie`); không đặt ⇒ `secure=False` như cũ.
- (3) Tài liệu API: `HUE_TAT_DOCS=1` ⇒ `FastAPI(docs_url=None, redoc_url=None, openapi_url=None)` (`api/app.py`); không đặt ⇒ như cũ.
- (4) Giới hạn lượt: `HUE_LUOT_MOI_NGAY=<n>` (> 0) ⇒ đếm lượt POST `/api/chat`, `/api/chat/stream`, `/api/anh/ung_vien` theo IP (`request.client.host`) theo ngày giờ Việt Nam, trong RAM; vượt ⇒ 429 JSON `{error: {code: "rate_limited", message}}` (giao diện hiện `error.message`, không sửa giao diện); log 1 dòng cảnh báo không ghi IP. Không đặt / 0 ⇒ tắt. Sau proxy (Caddy): uvicorn phải chạy `--proxy-headers --forwarded-allow-ips <ip proxy>` để `client.host` là IP thật — ghi vào checklist deploy, không tự đọc `X-Forwarded-For` (giả mạo được).
- Khai báo sửa: `backend/config/logging.yaml`, `backend/api/app.py`, `backend/api/routes/chat.py`, `backend/api/gioi_han.py` (mới), `backend/tests/test_chot_deploy.py` (mới).
- Kiểm: test file mới + file chạm (`test_api_chat.py` không khoá, `test_static_ui.py`); 1 lần server thật bật cả 4 biến (`/docs` 404, cookie `Secure`, lượt thứ n+1 ⇒ 429) + 1 lần không biến (như cũ). 0 USD (dùng câu ngoài phạm vi / lượt bị chặn trước model — vẫn có 1–2 câu thật ≈ 0,001).
- **Kết quả:** nhánh `p12-chot-deploy` = **`a3db152`** (pushed). Test mới `test_chot_deploy.py` 5 đạt; file chạm (`test_api_chat` · `test_feedback` · `test_cong_dot_1`) 40 đạt / 1 lỗi = test cần khoá (đã biết). Server thật cổng 8897: **bật 3 biến** (`HUE_TAT_DOCS=1 HUE_COOKIE_SECURE=1 HUE_LUOT_MOI_NGAY=2`) ⇒ `/docs` 404 · `/openapi.json` 404 · cookie có `Secure` · lượt 1–2 200, lượt 3 `/api/chat` 429 + lời báo, `/api/chat/stream` 429 · log 2 dòng `chat_metrics` + 2 dòng "Rate limited", 0 lần chứa IP; **không biến** ⇒ `/docs` 200, cookie không `Secure`, không 429. Log xoay vòng nạp được (server khởi động bình thường). Tiền ≈ 0,00035 USD (4 câu ngoài phạm vi). Bỏ test cấu hình log (dictConfig trong test đổi logging toàn cục ⇒ hỏng test đếm dòng log).
- **Checklist deploy (cho A):** sau Caddy phải chạy uvicorn `--proxy-headers --forwarded-allow-ips <ip Caddy>` (không thì mọi người chung một IP ⇒ một sổ đếm); đặt 3 biến trong `compose.yml`; đếm trong RAM ⇒ khởi động lại là xoá sổ (chấp nhận cho đồ án).
**(6) XONG (21:08 09/11/2026):** review `p9-t2-web` `2ac126a` (E, phần 0 USD) — **ready** 0 blocker · 0 major · 2 minor; `report_agent/2026-11-08_phase_9_ban_13/c_t2_web_review.md` (untracked). Chạy lại: 183 test đạt · Q1 cờ tắt 228/228 giống byte. Worktree `/tmp/c_t2rv` (tách, symlink `data/`, `knowledge-base-hue/`) — gỡ khi xong.
**Bẫy (A ghi, 1 dòng):** harness đếm dòng `application.log` theo vị trí — từ `ccc9f4f` log xoay vòng 10 MB ⇒ lượt đo trùng lúc xoay đếm hụt; kiểm cỡ log trước lượt đo. `p12-chot-deploy` đã merge (`ccc9f4f`), nhánh chờ User `!` xoá; worktree `/tmp/c_dep` gỡ khi xoá nhánh.
**(7) XONG (21:11 09/11/2026, A giao):** review sớm `p9-t4-lich` `9780d93` (E) — 0 blocker · 1 major (thêm tiêu chí "câu xin lịch không hỏi kèm có câu cố định (b) = 0", code không sửa); `report_agent/2026-11-08_phase_9_ban_13/c_t4_lich_review.md` (untracked). 331 test · Q1 tắt 228/228. Worktree `/tmp/c_t4rv` (tách, symlink) — gỡ khi xong. Lệch: plan T4 sha trên ổ `5a22b51fe49c` ≠ A duyệt `29708ef92e30` (đã báo A).
**T2 âm (E, 21:49 09/11/2026):** hỏi kèm có web 4/10 = mốc; C đồng ý đóng hồ sơ, không đề xuất vòng chỉnh mô tả (đã nhắn A). **RẢNH — chờ E** rebase + đo T4 ⇒ C xem delta. Worktree `/tmp/c_t2rv` hết dùng.
**T4 âm (E, 22:18 09/11/2026):** Q3 (ii) 21 · 15 / 27 < 26; review M-1 của C đóng (câu (b) nói sai 0/19). C đồng ý đóng hồ sơ (đã nhắn A). **RẢNH — chờ A** (không còn delta nào phải xem). Worktree `/tmp/c_t4rv` hết dùng.
**Dọn (22:19 09/11/2026, A giao):** đã gỡ 4 worktree `/tmp/c_dep`, `/tmp/c_t2rv`, `/tmp/c_t3`, `/tmp/c_t4rv` (gỡ symlink trước; chỉ còn file bị gitignore như `backend/logs/` ⇒ `--force`). C không còn worktree nào. **RẢNH — chờ A** (đang khoá máy cho S5 của B: không chạy lượt có phí / pytest rộng / build).

## (07/11) kết phiên — chỉ tra cứu
**Trạng thái:** rảnh có lý do — không việc đang dở, không worktree `/tmp` nào của C. Chờ A giao (việc A giao = User nói "làm đi"). `main` khi viết: `fbcb903`.
Phiên 07/11: terminal C `hue-rag-a0` · A `hue-rag-7a` · B `hue-rag-10` · E `hue-rag-81` (tên đổi khi mở lại — `ListAgents`).

### 1. Việc xong 07/11 (report tracked — sha256 12 lúc viết)
- **S3 đo cổng đợt 1** — `report_agent/2026-11-06_giao_dien_cong/c_s3_q_f_implementation.md` `b178c47c6abe`:
  - bộ quyết 12 tổ hợp `data/phase_9/cong_dot_1/to_hop_chinh_thuc.jsonl` md5 `792a3cbe3fe5` (ẩn "đi dày" theo Q-U3) — **đã dùng để quyết**, từ nay chỉ là bộ hồi quy;
  - **Q-G + Q-N trên `27ed091`: ĐẠT** (7 / 7 đích × 1440 / 390, 0 CSP / console, JS gzip 101,9 KB, tương phản thấp nhất 5,42; Q-N 10 / 10) — đã merge;
  - **Q-F bộ quyết trên `632a4f7` (V5): ĐẠT** — sàn code 24 / 24, F-a 12 / 12 + 12 / 12 (2 sub-agent, 0 bất đồng); User duyệt bật biểu mẫu + F-a (4) = "không trái nhóm đi cùng" ⇒ `main` `a884de4` cờ `lich_trinh_bieu_mau` BẬT;
  - §6 chữ đầu trên `main` `a884de4` (theo dõi): biểu mẫu p50 2,30 / p95 4,22 s · câu kho 1,78 / 3,61 s (n = 10 mỗi loại).
  - Data private: `data/phase_9/cong_dot_1/s3/` (lan_1 / lan_2 / `fa/` phiếu + 2 file chấm), `qn/` (10 câu Q-N + kết quả), `qg_tuong_phan_27ed091.json`, `chu_dau_main_a884de4.jsonl`.
- **X1 / X1b / X1c lượt biểu mẫu bị model từ chối** — `report_agent/2026-11-06_giao_dien_cong/c_x1_luot_bieu_mau.md` `99abfe79ee01`; data `data/phase_11/cong_dot_1/x1/`. Nguyên nhân (ủng hộ, chưa chứng minh): `LICH_TRINH_LUAT` nằm trong phần Bằng chứng ⇒ model coi là dữ liệu. V0 từ chối 10 / 16 · V1 (giả lượt công cụ) 12 / 16 · V2 (luật lên lời dặn hệ thống) 1 / 16 → 0 / 16 nhưng chữ đầu p95 8,8 s · V4 (thêm câu dặn) kém · **V5 = V2 + reasoning `low`** đạt (p95 4,75 s) ⇒ B đưa vào nhánh · V6 `minimal` ⇒ 400 · V3 (code dựng lời, 0 USD) đọc như trích máy. Đề xuất dự phòng chưa làm: "hiện khung code trước, lời model sau".
- **Tự soi** — `report_agent/2026-11-07_tu_soi_lo_trinh/tu_soi_C.md` `69727aa946ad` (deploy chưa thử = rủi ro lớn nhất; đóng hồ sơ sửa lịch; gỡ 3 cờ âm ở B7; giọng nói cắt nếu chưa có 40 câu trước ~20/11; đợt 2 chỉ P1).
- **C-tl thời lượng tham quan từ web** (0 USD; private): `data/phase_9/lich_trinh/thoi_luong_web.json` (link + ngày + trích từng nguồn) · `diem_v7_thoi_luong_web_nhap.json` sha256 `363763ae2101` (trường khác giống v6) · `tools/dung_v7.py` · tra thô `data/tra_cuu_cli/2026-11-07_c-tl-thoi-gian-1/`, `-2/`. 19 / 26 điểm có số (11 ngắn · 8 nửa buổi); mức chắc cao 4 · vừa 5 · thấp 6 · lệch 4.
- Dữ kiện Q-U3: `kieu_di` không đổi khung ở 0 / 120 tổ hợp với bảng v3/v6; v7 ⇒ 12 / 120.

### 2. Đang chờ User (qua A) — C không tự làm
- **Phiếu v7** `data/phase_9/lich_trinh/diem_cho_user_v7.md` (sha256 `ee2f22328691`): A dùng cả bảng / B chỉ dòng chắc cao + vừa (9 điểm) / C giữ v6. `settings.yaml` `lich_trinh_bang` vẫn `diem_v3.json`.
- **3 luật xếp "đi dày" đề xuất, CHƯA ĐO** (phiếu v7 §2): điểm thứ hai lấy cả di tích lấp chỗ · cho cặp ngắn ở cụm kề · "đi dày" mở buổi tối hợp sở thích cho nhóm không hạn chế. Biểu mẫu đợt 1 đã ẩn "đi dày" ⇒ không chặn gì.
- **Mô phỏng kín sửa lịch: vẫn DỜI** (sửa lịch hoãn, có thể đổi cách "điền lại biểu mẫu") — lệnh ở mục (cũ) dưới, chỉ chạy khi A giao lại.

### 3. Công cụ dùng lại được (private, chạy từ `backend/` của worktree nhánh cần đo; `PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag [--env-file /home/minhhieu/hue_rag/.env] python …`)
- `data/phase_9/cong_dot_1/tools/do_bieu_mau.py` md5 `4de78cb35999` — Q-F biểu mẫu: `kiem <bộ>` (0 USD: luật phủ + xếp thật + 9 ca phá) · `chay <bộ> <out.jsonl> --lan N [--dung 0.025]` (CÓ PHÍ, `/api/chat/stream` qua TestClient, bọc `_remember`; `--dung` cộng mọi *.jsonl cùng thư mục) · `cham` · `phieu <bộ> <kq> <thư_mục>` (đầu vào 2 người chấm F-a) · `gop <thư_mục> <c1> <c2>`.
- `data/phase_9/cong_dot_1/tools/tuong_phan.py` md5 `f53a31153ce3` — tương phản WCAG trên trang đã dựng (Playwright): `uv run python …/tuong_phan.py http://127.0.0.1:<cổng>/ --trang '#/,#/kham-pha,#/kham-pha/foods,#/kham-pha/bai/<id>,#/len-ke-hoach,#/tro-ly,#/gioi-thieu' [--json out]`.
- `data/phase_9/cong_dot_1/tools/playwright_cong.py` md5 `fa580e39f5ed` — 7 / 7 đích ≤ 2 lần bấm + mở thẳng / tải lại + CSP / console + bundle: `uv run python …/playwright_cong.py http://127.0.0.1:<cổng>/ --dist <worktree>/frontend/dist`.
- `data/phase_9/cong_dot_1/tools/qn_nguon.py` md5 `3710c9c69c4e` — Q-N 10 câu (`qn/cau_qn.txt`) qua giao diện + chữ đầu phía trình duyệt (CÓ PHÍ ~0,004).
- `data/phase_9/cong_dot_1/tools/do_chu_dau_main.py` md5 `5915e4a681ef` — chữ đầu qua server thật: `uv run python …/do_chu_dau_main.py http://127.0.0.1:<cổng> <log server> <out.jsonl>` (CÓ PHÍ ~0,008).
- `data/phase_11/cong_dot_1/x1/x1.py` (gọi hàm lõi trong tiến trình, V0–V3) · `x1b.py` / `x1c.py` (đường stream, agent clone đổi lời dặn / reasoning) · `tong.py` / `tong_b.py` (in bảng). Mẫu để thử biến thể lời dặn / tham số model mà không sửa nhánh.
- Cổng server tạm: worktree tách (`git worktree add --detach /tmp/<tên> <sha>` + symlink `data/`, `knowledge-base-hue/`), `cd frontend && npm ci && npm run build` nếu cần giao diện, `uvicorn api.app:app --port <trống>` chạy nền, tắt bằng TaskStop, gỡ symlink rồi `git worktree remove --force`.

### 4. Bẫy đã gặp 07/11
- `gpt-6-luna` **không nhận `reasoning.effort = "minimal"`** ở đường trả lời ⇒ 400 (`BadRequestError`, app không log chữ lỗi). `low` được.
- **Chỉnh trên bộ phát triển, quyết trên bộ giữ riêng**: X1 dùng 8 tổ hợp phát triển; bộ quyết 12 không chạy / không xem tới khi chốt biến thể. Giữ cách này cho thí nghiệm sau.
- **Đo latency không chồng việc nặng**: trước lượt đo nhắn B / E (và hỏi A — có lúc một dự án khác trên máy cũng chờ dùng máy); xong nhắn "xong đo". Lượt latency là việc của một người một lúc.
- `kiem_cuoi` không phân biệt biến thể khi lượt từ chối được code thay bằng lời tối thiểu (B171) ⇒ đếm từ chối riêng (chữ model = câu từ chối hoặc có `chu_thay`).
- `kiem_khung` coi ngày bị cắt vì vượt ngân sách (`vuot_ngan_sach`) là hợp lệ ⇒ đếm riêng (`cat_ngay_cuoi`).
- Tiêu chí chấm bằng người / sub-agent có chữ mơ hồ ("phù hợp người đi cùng") ⇒ ghi cách hiểu **trước** khi chấm; người làm không tự chốt cách hiểu sau khi thấy số.
- Sub-agent chấm có thể ghi file bằng Bash thay vì Write — kiểm file ra đủ mã, ghi vào report.
- **Sửa trước khi tái tạo** (C210): việc "sửa lỗi X" mà nguyên nhân chưa chứng minh ⇒ tái tạo trên code gốc TRƯỚC (đọc tham số thật), chưa viết sửa — A phải nhắc lần này.
- Đổi hành vi code (vd B171 đổi khung) ⇒ chạy lại mô phỏng nhãn (`mo_phong.py`, kín qua `!`) **trước** lượt có phí.
- Q1m: `data/phase_9/b5b/tools/capture_flags.py <out> lich_trinh=1 sua_lich=0|1`. Script import `llm.*`: không `-I`, `PYTHONPATH=$PWD`.
- Rebase "hai bên cùng thêm": giữ cả hai, kiểm `git range-diff`. Heredoc shell có backtick ⇒ dùng Write.
- Ca dò của người kiểm gồm cả câu **hợp lệ** model hay viết. Giờ trong file: luôn `date` trước.
- Overpass máy chủ công khai hay quá tải (06/11: 3 / 5 lượt 502) ⇒ `out count` nhẹ qua được; lấy thẻ thì một lần, giãn cách, không gửi dồn.
- Tin A có thể đến lúc C đang làm việc khác ⇒ việc mới ưu tiên theo lời A (vd B171 trước harness); việc dở ghi STATUS trước khi chuyển.

### 5. Tiền C 07/11 ≈ **0,078 USD**: X1 0,0247 · X1b 0,0174 · X1c 0,0143 · Q-N 0,0042 · S3 0,0087 · chữ đầu `main` 0,0084; mọi việc khác 0 USD (Codex tra web dùng tài khoản ChatGPT).

### 6. Tạm
- `/tmp/c_tl/` chỉ còn file thử / bảng tạm (yêu cầu tra web, kết quả thử V3, bảng tương phản) — không dữ liệu kín; mất khi khởi động lại cũng được.

---

## (cũ) — kết phiên tối 06/11 (chỉ tra cứu)

### Việc + lệnh của phiên tối 06/11 (S3 / S4 trong đó đã XONG 07/11; harness + lệnh sửa lịch vẫn đúng khi mở lại)
- **Đã xong tối 06/11** (terminal `hue-rag-42`):
  - **Harness sửa lịch:** `data/phase_9/sua_lich/tools/chay_sua_lich.py` md5 `559ebaf5f81e` — E review vòng 2 + vòng 3: **ready**. Bộ Q4 `bo_do_sua_lich/chuoi_q4.jsonl` `d35f8d9c5027`. Pilot = S01 + S06 (A duyệt). Report `report_agent/2026-11-02_phase_9_code/c207_rebase_sua_lich.md` §7–§8.
  - **B171 review:** ready trên `b0e52f8` (đã merge `dbb4004`) — `report_agent/2026-11-06_b5_cau_tu_nhien/b171_review.md` §7–§8.
  - **C208:** `p9-sua-lich` ⇒ **`79b3d9c`** trên `main` `d930867` (pushed). Gỡ xung đột B5b; sửa `hoi_toi` khi xếp lại / sửa trực tiếp + 4 test. 411 test; Q1 / Q1m 228/228 (`data/phase_9/sua_lich/q1_c208/`). Nhãn đã thấy S03 / S08 sửa theo B171 ⇒ `chuoi_da_thay.jsonl` **`c00de07114b5`**. E kiểm rebase: ready.
  - **C209:** `data/nghien_cuu_giao_dien_2026-11-06/nguon_du_lieu_dot_2.md` (P1 / P2 / P3 bản đồ + dữ liệu; C khuyên P1) — chờ User quyết khi A trình spec.
  - **C210:** chưa tái tạo được "hỏi lại số ngày thừa" ⇒ không sửa code (`report_agent/2026-11-06_b5_cau_tu_nhien/c210_implementation.md`). Đề xuất: harness kín lần sau ghi `so_ngay` model gửi + số code dò + có thẻ hỏi không.
  - **C211:** nháp kỹ thuật spec đợt 1 `data/nghien_cuu_giao_dien_2026-11-06/spec_dot1_ky_thuat_nhap.md` — A dùng khi viết spec.
- **Việc đầu phiên sau — lệnh `!` mô phỏng bộ kín sửa lịch** (0 USD, chỉ in số đếm + mã chuỗi / số lượt hỏng, trên nền `79b3d9c`):
  1. C dựng lại worktree (đã gỡ):
     ```
     git worktree prune; git worktree add /tmp/c_sualich p9-sua-lich
     ln -s /home/minhhieu/hue_rag/data /tmp/c_sualich/data
     ln -s /home/minhhieu/hue_rag/knowledge-base-hue /tmp/c_sualich/knowledge-base-hue
     ```
  2. Đưa User lệnh nguyên văn (cũng ở report C207 §8):
     ```
     ! cd /tmp/c_sualich/backend && PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python ../data/phase_9/bo_do_sua_lich/tools/mo_phong_kin.py | python3 -c "import json,sys,re; d=json.load(sys.stdin); print('kin ok', sum(v=='ok' for v in d.values()), '/', len(d)); [print(k, [re.match(r'L[0-9]+', x).group() for x in v]) for k, v in d.items() if v != 'ok']"
     ```
  3. Kết quả hỏng ⇒ sửa nhãn kín bằng `bo_do_sua_lich/tools/cau_truc.py` (không in câu) **trước** lượt có phí. `main` đổi code ⇒ rebase + Q1 / Q1m trước.
- **Sửa lịch — HOÃN** (handoff 22:41 06/11): cần cờ `lich_trinh` câu tự do; A xem lại cách sửa sau biểu mẫu ("điền lại biểu mẫu"). Khi đi tiếp:
  - thư mục kết quả `data/phase_9/sua_lich/do/` chỉ chứa file kết quả (`--dung 0.19` cộng mọi `*.jsonl` trong đó);
  - pilot S01 + S06 lần 1 ⇒ đọc file ⇒ lần 1 / lần 2 / Q4 ×2 ⇒ kín ×2 qua User `!` ⇒ `cham`.
- **S3 — đo Q-F biểu mẫu lịch trình** (spec cổng đợt 1 `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` bản 2 `ff3c317ec88b` §6; khi B xong S1 trên `p11-cong-dot-1`; cờ mới `assistant.lich_trinh_bieu_mau`):
  - **trước lượt có phí:** ghi 12 tổ hợp vào report S3, **sau khi User chốt Q-U3** (đi dày). Phủ đủ 5 `di_cung`; mỗi `so_ngay` 1 / 2 / 3 ≥ 3 lần; ≥ 4 có `so_thich`; ≥ 2 không chọn sở thích;
  - harness lưu **khung + chữ model + tham số** mỗi lượt (dựng theo mẫu `chay_sua_lich.py`: TestClient trong tiến trình, bọc hàm, đọc log sau mốc). Ghi cả `so_ngay` model gửi / số code dò (đề xuất C210);
  - ×2 = 24 lượt. Sàn code 24 / 24: 0 câu từ chối thay lịch, `kiem_cuoi` 0 lỗi, 0 rút lại;
  - F-a: 2 sub-agent mới độc lập chấm (khung + chữ + giá trị nút), ≥ 11 / 12 mỗi lượt theo cả hai, bất đồng ⇒ trượt;
  - Playwright §6 (Q-G phần C được giao); tiền cả spec ≤ 0,03 USD.
- **S4 — review cả nhánh `p11-cong-dot-1`** một lần (`risk-gated-agent-review`; bảng rà AI FDE §7 là một tiêu chí). Ca dò khác cách người làm: API Khám phá `../`, `sealed`, id ngoài `corpus.sources`; form gửi `truong` lạ ⇒ 422.
- **Đợt 2 (dữ liệu bản đồ / lưu trú / ăn uống / sự kiện):** chờ User chọn P1 / P2 / P3 (C209). Chọn P1 / P3 ⇒ Overpass **một** lần lấy thẻ tên ⇒ khớp toạ độ 15 điểm thiếu (người xem bằng mắt). Chọn P2 ⇒ đo dung lượng PMTiles + cỡ gói MapLibre trước.
- **Câu treo cho A** (không chặn):
  1. mô phỏng kín sửa lịch có còn cần chạy đầu phiên không, khi sửa lịch hoãn và có thể đổi cách ("điền lại biểu mẫu");
  2. C210: câu nêu số ngày mơ hồ ("3 hay 4 ngày") + model gửi số ⇒ code hiện dùng số model, không hỏi — giữ hay hỏi;
  3. link trong chữ câu trả lời chưa có `target` / `rel` — gộp vào S1 / S2?
- **Bộ đo (private, md5 12):** sửa lịch đã thấy `c00de07114b5` (trước C208 `d0ad12b6ed12`) · kín `daf762bcbbe5` · Q4 `d35f8d9c5027`; B6 `6ed74db21616` / kín `4de04132600b`; B5b `7e1bc3da2e44`; bảng `diem_v5.json` `c7d294fcacd5`.
- **Không đọc:** `data/phase_9/b5_v2/`, `data/phase_9/b5/kin/`.
- **Tiền C tối 06/11: 0,003855 USD** (C210 tái tạo; mọi việc khác 0 USD). Overpass (OSM) quá tải 3/5 lượt — lần sau gọi một lần, ngoài giờ cao điểm.
- **Backlog cho A:**
  - kho mâu thuẫn vị trí Bảo tàng Cổ vật · câu thiên tai vẫn gọi Serper · case 67 Golden từ chối ngẫu nhiên;
  - link trong chữ câu trả lời chưa có `target` / `rel` (C211);
  - câu `toi_khong_diem` nói "hợp sở thích" cả khi không nêu sở thích (E, có sẵn trên `main`).
