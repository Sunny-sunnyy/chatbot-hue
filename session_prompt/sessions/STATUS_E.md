# STATUS E — PHIÊN 14/11 (mở 09:43 14/11/2026, `date`) · terminal `hue-rag-c4` · Claude Opus 5.5 · vai thực thi

- 09:43 14/11/2026 — mở phiên, kiểm nhanh xong (main `a400f7f`, sạch, hooksPath `.githooks`, Qdrant 2 collection / 8.435 điểm; `/tmp/b_lkh` prunable; `/tmp/e_*` không còn ⇒ bảng tra người chấm phải dựng lại). Lệnh dọn của User chưa chạy (`hue_anh_siglip2` còn, 4 worktree Antigravity còn). **Chờ A giao việc**; việc theo handoff: gói ghi kho một lần (K1 + K2 trước ⇒ sao lưu ⇒ ghi ⇒ dựng lại ⇒ T1 ⇒ K1 / K2 sau). Chưa sửa file nào khác.
- 09:53 14/11/2026 — A giao gói ghi kho (A tự điều phối; **trần gói 0,22 USD** — A sửa từ 0,15; không bài lưu trú). Pilot Golden 10 câu 0,0021 USD (đường trợ lý thật) ⇒ đang chạy nền K1 Golden 166 còn lại + K2 an toàn 32 "trước". Đã dựng (chưa ghi kho): `data/sua_kho_2026-11-14_ghi_kho/` — `tools/ghi_kho.py` (diff / backup / write / lui), `kho.diff`, `tools/chay.sh` (bước 0 khoá ⇒ sao lưu ⇒ ghi ⇒ chia thử ⇒ xoá 3 đích ⇒ build ⇒ T1; lỗi ⇒ tự lùi). C đang review diff. File sẽ ghi: thư mục trên, `knowledge-base-hue/` (2 bài vé + 3 bài mới, sau khi C ok), chỉ mục Qdrant, `data/full_corpus_builds/`, report `report_agent/2026-11-12_ra_khoang_cach/e_ghi_kho_diem_mong_di_lai_implementation.md`, file này. W69 vòng 1: E phiếu "hook chỉ cảnh báo + câu brief".
- 09:56 14/11/2026 — Mốc "trước" XONG (Golden 176 + an toàn 32, 0 lỗi, 0,096 USD). C ready diff (thêm sửa 15A ⇒ 17 bài phố đi bộ, C M-1). Đã báo cả nhóm; **đang chạy `chay.sh`** (sao lưu 3 file ⇒ ghi kho ⇒ chia thử ⇒ dựng ⇒ T1). W69: User BỎ (A báo).
- **VIỆC LẦN GHI KHO KẾ (A giao 09:56 14/11/2026, cùng bài lưu trú):** giờ Đại Nội theo mùa (User tra — trang Vinpearl theo quy định Trung tâm BTDT): hè 16/03–15/10 06h30–17h30, đông 16/10–15/03 07h00–17h00, đêm 19h00–22h00 chỉ theo chương trình ⇒ sửa bài Đại Nội + bài Bảo tàng Cổ vật (đang ghi một khung 07h00–17h30); kiểm thêm các bài khác dùng khung chung.
- 10:24 14/11/2026 — **GÓI GHI KHO XONG, A chốt GIỮ.** 207 file / **8.474 đoạn**, record `efbf748c2195`, sparse `79aa34a6a68d`, T1 `a105229f1902`, nhãn đoạn đúng **v6** `2c7f9bf22341` (C kiểm). K1 đạt trừ từ chối nhầm 3 ⇒ 5 (nhiễu, chạy lại); K3 phạm 1 câu theo nhãn (nội dung không mất, K1 không tụt); K2 S-AT không âm; X03 đổi nhãn "trong kho" (A chốt, C kiểm). Đi lại 2/6 ⇒ 4/6; ăn gần cụm Thủy Xuân (OSM có phủ) vẫn hỏng. Tiền **0,229 / 0,24**. Report `report_agent/2026-11-12_ra_khoang_cach/e_ghi_kho_diem_mong_di_lai_implementation.md` — chờ C review. Đã giao 2 người chấm mù bộ quyết 12 cho B (bảng tra `data/len_ke_hoach_v2_2026-11-13/bang_tra_cham_1411.md`). Tiếp: review nhánh B `p9-len-ke-hoach-v2` (505b53d) + bảng quán OSM của C (hỏi A thứ tự).
- 10:28 14/11/2026 — C review report ghi kho: ready (2 minor đã sửa). **Review nhánh B `p9-len-ke-hoach-v2` 505b53d: changes_requested** (`e_review_len_ke_hoach_nhanh_1411.md`): 2 người chấm mù bộ quyết 12 cùng gắn 4/24 trượt ý 6 (ngày mưa không dòng "nếu mưa", không có điểm ngoài trời) ⇒ 10/12 mỗi lượt theo chữ — chờ A quyết (E viết thước, nghiêng sửa code + kiểm bằng code); M-1 sáng chồng chiều 52/3.840 khung (ca dò `data/len_ke_hoach_v2_2026-11-13/e_ca_do_chong_buoi.py`). Tiếp: review bảng quán OSM của C.
- 10:30 14/11/2026 — A chốt (c) cho nhánh B: giữ thước; B sửa code (dòng ngày mưa luôn in + kiểm 3.840 khung) + M-1 ⇒ B chạy bộ 20 + chấm code bộ quyết ⇒ **E giao 2 người chấm mù CHỈ cho lịch đổi ở ý 6 / khung, rồi kiểm phần sửa** (không review lại cả nhánh). **Review bảng quán OSM v1 của C XONG — ready** (0/0/2 minor; `e_review_bang_quan_osm_v1.md`; tính lại 488 giống hệt). Đang chờ B.
- 10:36 14/11/2026 — **User giao THẲNG E (terminal E): làm lại giao diện cả 5 trang** (Trang chủ, Khám phá, Lên kế hoạch, Trợ lý Huế, Giới thiệu) — "đẹp mắt, sinh động, thu hút, hiện đại"; được nhờ Codex tra trang đẹp / repo / skill; dựng HTML xem trước; bàn cùng nhóm. Đã báo A. Đang làm: 2 lượt Codex (`data/ui_mau_2026-11-14/yeu_cau/a_trang_mau.md`, `b_repo_skill.md` ⇒ `data/tra_cuu_cli/2026-11-14_e-ui-*`); bàn nhóm vòng 1 về 3 hướng (H1 Sông Hương · H2 Men lam Hoàng cung · H3 Hoàng hôn tím). File sẽ ghi: `data/ui_mau_2026-11-14/` (bản mẫu HTML, ảnh chụp) — KHÔNG chạm repo / frontend. 0 USD API.
- 10:50 14/11/2026 — Kiểm M-2 nhánh B (16374fc): ĐÓNG ⇒ review nhánh `ready_for_user_confirmation` (m-3 minor). **Trang chủ 3 hướng XONG** (`data/ui_mau_2026-11-14/h1|h2|h3/trang_chu.html`, ảnh `anh_chup/`, trang so sánh `index.html`; xem qua server tĩnh của A http://127.0.0.1:8895/). C dựng `gioi_thieu.html` mỗi hướng + đo tương phản. Font tự host `chung/fonts/` (@fontsource 5.2.5, OFL), CSS chung `chung/co_so.css`, công cụ chụp `tools/chup.py`. Chờ User chọn hướng ⇒ E làm Lên kế hoạch (ưu tiên) + Trợ lý, C làm Khám phá.
- 11:00 14/11/2026 — **User chọn H1 Sông Hương** (muốn sinh động hơn). Bàn nhóm hiệu ứng: A chốt — CSS thuần + ~30 dòng JS, không thư viện, không Codex. Đã làm: lớp hiệu ứng chung `chung/hieu_ung.css` + `hieu_ung.js` (ảnh trôi chậm, sóng dâng, hiện dần khi cuộn, thẻ nhấc theo số TRIPO, View Transitions; tắt khi reduced-motion), H1 trang chủ thêm nền xen kẽ (`chung/song_chim.svg` — không dùng data: vì CSP) + biểu tượng màu; **mẫu `h1/len_ke_hoach.html` XONG** (form 4 nhóm theo hợp đồng B, lịch dòng thời gian có ảnh, xương lấp lánh). Ảnh lịch ở `data/ui_mau_2026-11-14/anh/lich/` (= `/anh/lich/`). Tiếp: Trợ lý Huế H1 (sau phản hồi User / B). Trường backend mới cần: `ngay` cho ghi chú du_bao + `phut_di` (A giao B).
- 11:06 14/11/2026 — **Đủ 5 trang mẫu H1** (`data/ui_mau_2026-11-14/h1/`: trang_chu · kham_pha + kham_pha_bai (C) · len_ke_hoach · tro_ly · gioi_thieu (C)); menu nối đủ, chuyển trang mượt. Lên kế hoạch sửa theo B (ghi công ảnh từng mục + mục thu gọn ảnh biểu mẫu, ô 'chưa có ảnh', phút đi 15 chỉ cùng buổi) + C (tương phản 390 đạt, chữ ≥ 14 px, min-height chống CLS). Trợ lý mới: 5 lượt mẫu từ câu trả lời thật 14/11. Emoji 👍 thay SVG (font không có emoji). Chờ C đo Trợ lý + User xem. Khi code thật: tiền tố lớp theo trang (C gặp trùng `.nhanh`).
- 11:21 14/11/2026 — User: trang chủ 'vẫn không có hiệu ứng gì đặc biệt' (A nghi máy User tắt Animation effects ⇒ reduced-motion). **Hiệu ứng bản 2**: bật theo lớp `html.hieu-ung` (JS), bản mẫu có dải báo + nút 'Xem hiệu ứng' khi máy giảm chuyển động; mạnh hơn (hiện lần lượt lúc tải, hero 1⇒1,12 + parallax, menu đổi nền khi cuộn, trượt 40 px lệch nhịp, thẻ lớp màu trượt, nút lún). Thử Playwright 2 chế độ: 28 / 0 + dải báo / bấm nút ⇒ 28. `co_so.css` đổi chặn chuyển động theo `html:not(.hieu-ung)`. C áp cho trang của C + đo. B / C đang tra thư viện (Motion, GSAP…) ⇒ sau đó dựng bản trang chủ 'có thư viện' để User so. Công cụ: `tools/thu_hieu_ung.py`, `GHI_CHU_KHI_CODE.md`.
- 11:29 14/11/2026 — User: hiệu ứng bản 2 'đã ổn hơn'; rồi 'làm đi, bắt đầu ngay' ⇒ A giao E chuyển mẫu H1 thành code (mức nhẹ). **Plan** `docs/superpowers/plans/2026-11-14-giao-dien-h1-plan.md` — chờ A duyệt + B trả lời câu chuyển trang. File E SẼ sửa (đợt 0, nhánh `p9-gd-h1` từ main): `frontend/src/index.css`, `App.jsx`, `main.jsx`, `route.js`, `pages.jsx` ⇒ tách `TrangChu.jsx` / `KhamPha.jsx` / `LenKeHoach.jsx` / `GioiThieu.jsx`, tách `LichV2.jsx` khỏi `chat.jsx`, mới `hieuUng.js` + `hieu_ung.css`, `package.json` / lock (@fontsource/noto-serif-display), `public/hoa_tiet/`. Đợt 1: E giữ `TrangChu.jsx`, `LenKeHoach.jsx`, `LichV2.jsx`.
- 11:37 14/11/2026 — A duyệt plan (sha a45a2b386dcd; lịch ở lại #/len-ke-hoach; bật anh_lich đợt 1). **Đợt 0 push** `p9-gd-h1` @ `848eafa` (worktree `/tmp/e_gd`, symlink data/ + kho; server thử cổng 8871 chạy nền): tách file trang + LichV2/SourceLine, font serif, đầu / chân trang nước sâu, lớp hiệu ứng (`.noi`⇒`.nang`), View Transitions. 114 test đạt; 8 route × 2 chế độ 0 lỗi; JS +0,38 KB gzip. C review đợt 0. **Đang làm đợt 1**: TrangChu.jsx, LenKeHoach.jsx, LichV2.jsx, App.jsx (luồng submitPlan), settings anh_lich.
- 12:01 14/11/2026 — **Đợt 1 phần E push**: trang chủ `4118069`, Lên kế hoạch `db8c875` (lịch ở lại trang, thẻ dòng thời gian, ảnh + ghi công, phut_di, dự báo theo ngày, sông vẽ dần, chỗ `lich.thay_doi` cho B; `anh_lich: true`; test pin anh_lich). 114 test đạt 2 chế độ; 3 lượt chạy thật ≈ 0,006 USD. JS 116,10 KB gzip. Server nhánh cổng 8871. Chờ C đo + B chạy pw_nghiem_thu. **Tiếp theo (A chốt):** plan ½ trang + code xuất lịch .ics ⇒ bài kho lưu trú (script, ghi kho kế + K1/K2/K4 + giờ Đại Nội) ⇒ review câu nhiều ý (C) + trang Trợ lý (B). Ngân sách: không trần cứng (User).
- 12:07 14/11/2026 — Review trang Trợ lý của B: `d6bc51e` changes_requested (M-1 theo cờ + 3 minor) ⇒ sửa `0afcebd` ĐÓNG (`e_review_gd_h1_tro_ly_b.md`). **Xuất lịch .ics XONG** `9f086d2` (plan `2026-11-14-xuat-lich-ics-plan.md`, A duyệt): 44 lịch thật ⇒ 288 sự kiện, trình đọc Python độc lập 0 lỗi; UI thật tải được file; không ngày ⇒ dòng nhắc. Chờ C review. Công cụ: `data/ui_mau_2026-11-14/tools/chay.mjs`, `kiem.py`. **Tiếp: bài kho lưu trú** (`data/sua_kho_2026-11-13_luu_tru/`, script `tools/dung_bai_luu_tru.py`).
- 12:22 14/11/2026 — Đo của C chỉ ra CLS 390 + bộ chọn VT ⇒ sửa `6f37756` (ô thời tiết absolute + chừa chỗ, giữ ghi công Open-Meteo; khung giữ chỗ Lên kế hoạch tới khi có cờ) ⇒ C đo lại ĐẠT. **Review đợt 1 của C** (`d72e7f0`, `e_review_gd_h1_dot1_c.md`): 2 major (thẻ Thông tin nhanh làm mất dòng ở 51/207 bài; Giới thiệu không theo cờ) + 2 minor (ảnh không bay khi chuyển trang; Khám phá thiếu loi) ⇒ C sửa `ff2ebe9` ⇒ E kiểm lại: 0 mất dòng, VT có 1 ảnh mang tên ⇒ **ready**. **Bài lưu trú nháp sửa theo review C**: gộp 2 cặp trùng (141 ⇒ 139, luật `BO_TRUNG`, trang chi tiết danh mục ở `trang_chi_tiet/`), thêm câu về địa chỉ trước 07/2025, tiêu đề = tên file; đối chiếu tin thành phố: 5 sao khớp 10/10, 4 sao khớp 10 (thành phố có 1 cơ sở mới 23/01/2026 mà danh mục không có, danh mục có 3 cơ sở tin không nêu) ⇒ chờ C kiểm lại; thêm cơ sở mới hay không = A chọn. 48 đoạn, 0 lỗi. Chưa ghi kho.
- 12:59 14/11/2026 — **GHI KHO LẦN 2 XONG (bài lưu trú)**: 212 file / **8.522 đoạn**, record `38b3ca3eb323`, sparse `47f4b88b1309`, T1 `356a742f09a1`. Thêm 1 khách sạn 4 sao theo tin thành phố (A chốt (b)). Bảo tàng Cổ vật thêm câu giờ đổi theo mùa. Giờ Đại Nội theo mùa GIỮ LẠI (số User chép có thể là giờ bán vé; A hỏi User). Đo theo `data/sua_kho_2026-11-14_ghi_kho_2/TIEU_CHI.md`: K1 từ chối 23 = 23 (8 câu đổi là nhiễu), 2 câu có đoạn mới chấm mù 5/5 cả hai bên; K2 0 câu chạm đoạn mới; K4 trả lời 4 ⇒ 11/12, 0 giá, 0 tên bịa (minor: câu homestay chưa nói không gồm homestay). 0,225 USD. Report `e_ghi_kho_luu_tru_implementation.md`; JS +10,5 KB theo trang ở `e_giao_dien_h1_implementation.md`. **Chờ A cho commit**: `backend/llm/assistant.py` + `backend/tests/test_assistant.py` (chưa commit, ở cây main) + 3 report + STATUS_E.

### Bẫy / đã học phiên 14/11
- **Không grep cả thư mục có file `*sealed*`** (14/11: grep `data/phase_9/dinh_tuyen_2/*.jsonl` để xem khuôn bộ câu ⇒ lỡ in 2 dòng bị cắt của `a_ranh_gioi_sealed.jsonl`; không dùng, đã báo A). Tìm trong kho: `scripts/grep_kb.sh`; thư mục khác: `ls` xem tên file trước, loại `*sealed*` rồi mới đọc.
- Codex trích "nguyên văn" giờ mở cửa khác số User chép (giờ mở cửa ↔ giờ bán vé) ⇒ số giờ ghi kho phải mở trang gốc đọc; trang chặn (Cloudflare 403) ⇒ giữ lại, hỏi User.
- Sửa code / test thì làm trên nhánh / worktree riêng, không trên cây main chung (14/11: 2 file sửa ở main suýt lẫn vào commit merge giao diện của A; A nhắc).
- Thẻ / khối UI rút gọn nội dung bài ("Thông tin nhanh") phải đo trên đủ 207 bài qua API thật: mẫu 2–3 bài không lộ dòng con bị mất.

---

# STATUS E — KẾT PHIÊN 22:39 13/11/2026 (`date`) · terminal `hue-rag-e8` (A `hue-rag-43`, B `hue-rag-83`, C `hue-rag-eb`) · Claude Opus 5.5 · vai thực thi

## PHIÊN SAU ĐỌC TRƯỚC (viết 22:39 13/11/2026)

**E không còn tiến trình, server, trình duyệt nào.** File tạm `/tmp/e_*` (xoá được). Không worktree của E.

### Việc của E phiên sau (theo thứ tự)
1. **GÓI GHI KHO một lần** (User duyệt 13/11; A ghi ở handoff "User duyệt gói 10 câu" + mục ghi kho): 2 bài `data/sua_kho_2026-11-13_diem_mong/` (⇒ `heritages/heritage/`, `travel/places/`; C review ready) + bài `data/sua_kho_2026-11-12_dot_3/bai_nhap_di_lai_o_hue.md` (⇒ `travel/services/`; C review ready) + **bài lưu trú nếu xong + C review kịp** + sửa 3 chỗ kho: người lập không gian lưu niệm (theo trang chính thức) · số nhà khu Lê Bá Đảng trên Lê Lợi (theo Sở Du lịch) · bài vé gộp: bảo tàng không thuộc "Nam sông Hương"; Ga Huế GIỮ. **Thứ tự:** mốc "trước" K1 Golden 176 + K2 an toàn 32 trên kho hiện tại (TRƯỚC khi ghi) ⇒ sao lưu file sửa vào `knowledge-base-hue/meta/` + build record + sparse state ⇒ ghi + chia đoạn thử ⇒ xoá sparse state cũ, dựng lại tại chỗ (`guides/full_corpus_rag.md` "Build lại index") ⇒ `/health` ⇒ đếm đoạn mỗi file mới = số chia thử (bảo tàng 12 · không gian lưu niệm 15 · đi lại 12) ⇒ T1 158 so `64656a87c109` ⇒ K1 / K2 "sau", chấm cùng lượt mù. Trần 0,15 USD. A báo B / C dừng có phí + server. Report `report_agent/2026-11-12_ra_khoang_cach/e_ghi_kho_diem_mong_di_lai_implementation.md` (không tên cơ sở). Dừng nếu dựng lỗi / K1 / K2 vỡ ⇒ báo A, không tự lùi.
2. **Bài lưu trú nháp — DỞ:** `data/sua_kho_2026-11-13_luu_tru/BIEN_BAN_DANG_DO.md` (phiếu User đã áp, số thật 141 cơ sở có hạng / 100 % gán khu; chưa viết script sinh bài). Nếu không kịp gói 1 ⇒ ghi ở lần ghi kho sau.
3. **Sau K1 / K2:** đếm lại 6 câu "ăn gì gần X" (mốc 1 / 6, lượt đếm 12/11) + vài câu cụm Thủy Xuân / Kim Long (≈ 0,01 USD) ⇒ còn hỏng ở cụm OSM phủ ⇒ báo A (lần ghi sau thêm bản nhẹ quán OSM, rào C gộp); hỏng ở cụm OSM không phủ ⇒ cần nguồn khác (A chốt "Quán OSM — chốt").
4. Bảng tra cho người chấm bộ quyết 12 (`/tmp/e_cham/bang_tra.md` — mất khi khởi động lại; dựng lại từ `diem_v8.json`): **sửa** thêm điểm có buổi tối mà không ghi giờ (vd chợ có phố ẩm thực đêm) trước khi dùng.

### Kết quả phiên 13/11 (E)
- Kho 3 lưu trú: gán khu bằng OSM 54 % ⇒ 98 %; ĐÍNH CHÍNH đếm theo cơ sở (151 dòng = 142 ⇒ sau phiếu 141); bài nháp "Đi lại ở Huế" (C ready).
- Review: kho 3 ăn uống của C (ready, 3 minor) · nghiệm thu đợt 1 lịch trình của B (ready cho "trượt, không bật"; 4 minor; ca dò 13.176 khung) — `e_review_len_ke_hoach_dot_1.md`.
- TRIPO vòng 6 XONG (k3–k6 + mọi tính năng; report mục 5 `b_tripo_v6_lap_ke_hoach.md`).
- 13 ca phụ nghiệm thu (`bo_do_v2/ca_phu_13_11.jsonl` `223b8768fa68`) — cặp D4 thiết kế sai (có trẻ em).
- 2 bài kho nháp cho điểm mỏng (C ready).
- Bàn nhóm quán OSM: A chốt theo "đổi một thứ" của E.

### Tiền E phiên 13/11
**0 USD API** (Codex 1 lượt tra web, WebFetch, Playwright TRIPO, agent con 0).

### Bẫy / đã học phiên 13/11
- **Đếm theo dòng lần thứ 3** (151 dòng ⇒ 142 cơ sở; C bắt): khử trùng là bước ĐẦU của mọi phép đếm trên danh mục ngoài, kể cả danh mục chính thức. Gộp trùng phải giữ dòng hạng cao nhất (E tự bắt lỗi giữ dòng không hạng).
- **Tên quán + địa chỉ từ kho lọt vào report tracked đã push** (`e_review_kho3_c.md`, commit `e74c6df`): repo public ⇒ trong report dùng nhãn (Q-a…), tên / địa chỉ để ở `data/`. Hook không bắt (chỉ bắt chép ≥ 40 ký tự).
- Script thử trang ngoài: dò một lượt TRƯỚC (k3 cần 101,8 s, vượt mức 85 s ghi hôm trước); 3 tab TRIPO không có ô gõ tự do — đọc DOM trước khi viết thao tác.
- Đếm câu dự phòng / khung bằng cách KHÁC người làm (mẫu câu, không dùng `tom_tat`); ca dò bất biến trên hàng nghìn khung rẻ hơn đọc code.
- Thiết kế ca kiểm: kiểm xem ràng buộc khác (nhóm hạn chế) có khoá kết quả không trước khi ghi kỳ vọng (cặp D4).
- Mâu thuẫn kho ↔ nguồn ngoài: ghi cả hai + báo A; không tự sửa kho.

---

# (nhật ký trong phiên) STATUS E — PHIÊN 13/11 (mở 19:47 13/11/2026, `date`) · terminal `hue-rag-e8` · Claude Opus 5.5 · vai thực thi

- 19:47 13/11/2026 — mở phiên, kiểm nhanh xong (main `d5ea552`, sạch, hooksPath `.githooks`, Qdrant 2 collection / 8.435 điểm). Worktree `/tmp/b7_moc`, `/tmp/b_lkh` báo prunable (thư mục `/tmp` đã mất). **Chờ A giao việc**; việc theo handoff: kho 3 lưu trú (gán khu 22 đường bằng OSM) + bài "Đi lại ở Huế" ⇒ rồi TRIPO vòng 6. Chưa sửa file nào khác.
- 19:49 13/11/2026 — A giao (User: việc A giao = "làm đi"): kho 3 lưu trú + bài đi lại ⇒ TRIPO vòng 6. **Đang làm: gán khu 22 đường bằng OSM.** File sẽ ghi: `data/luu_tru_2026-11-12/tools/gan_khu_v3.py` (mới), `data/luu_tru_2026-11-12/luu_tru_theo_cum_nhap_v3.json` (mới), `data/luu_tru_2026-11-12/phieu_khu_luu_tru_cho_user.md`, file này. Luật ghi TRƯỚC khi chạy: mỗi đoạn đường OSM cùng tên (trong khung Huế) ⇒ điểm tham quan gần nhất ≤ 2 km ⇒ cụm ⇒ khu; mọi đoạn có khu cùng một khu ⇒ gán; khác khu ⇒ "cần xem"; không đoạn nào ≤ 2 km / không có tên trong OSM ⇒ không gán.
- 19:52 13/11/2026 — **gán khu bằng OSM XONG: 149 / 151 (98 %)** (54 % trước). Bảng C phiếu viết lại (23 đường) + bảng D (2 cơ sở User chọn). Biên bản `buoc_0_gan_khu.md` mục "Bản 3". Phiếu sẵn sàng đưa User (qua A). **Tiếp: bài nháp "Đi lại ở Huế".** File sẽ ghi: `data/sua_kho_2026-11-12_dot_3/bai_nhap_di_lai_o_hue_DANG_DO.md`.
- 19:55 13/11/2026 — **bài nháp "Đi lại ở Huế" XONG** (`data/sua_kho_2026-11-12_dot_3/bai_nhap_di_lai_o_hue.md`, CHƯA vào kho): 6 mục, chia đoạn thử 12 đoạn / 0 lỗi (dài nhất 537 ký tự); mỗi ý có nguồn chính thức E đã mở hoặc đoạn kho; 0 giá / số điện thoại / giờ tàu. Bài "Thuê xe ở Huế" KHÔNG viết (chưa đủ ≥ 2 nguồn / ý). Chờ C review + User xem lướt (spec bước 2). **Tiếp: TRIPO vòng 6** (đọc report B mục 4 trước).
- 19:56 13/11/2026 — **TRIPO vòng 6 đang làm.** Sửa `data/tripo_v6_2026-11-12/tools/lap_ke_hoach.py` (chờ nút Bỏ qua / Xác nhận ≤ 150 s, ảnh mỗi 30 s; không thấy nút ⇒ dừng, không bấm chặng); 4 thư mục k3–k6 hỏng đổi tên `_hong_k3…k6`. Chạy dò k3 trước (Playwright một trình duyệt, timeout 600 s). File sẽ ghi: `data/tripo_v6_2026-11-12/` (k3–k6 mới, tính năng khác), `report_agent/2026-11-12_ra_khoang_cach/b_tripo_v6_lap_ke_hoach.md` (phần E viết tiếp), file này.
- 20:02 13/11/2026 — A chen việc: **review kho 3 ăn uống của C XONG — ready** (0 blocker / 0 major / 3 minor: một quán in mét khi căn cứ yếu · mức `osm` ngoài spec · một quán: số kiệt ghi nhầm số nhà) — `report_agent/2026-11-12_ra_khoang_cach/e_review_kho3_c.md`. TRIPO: **k3 dò XONG đủ luồng 13 bước** (phương án sau 101,8 s); đang chạy nền k4 → k6 → `tinh_nang_khac.py` (log `/tmp/e_k456.log`).
- 20:05 13/11/2026 — **Sửa theo review của C** (`c_review_kho3_e.md`): M-1 đúng — mình lại đếm theo dòng ⇒ khử trùng trong `gan_khu_v3.py`: **142 cơ sở có hạng, 140 / 142 (98 %)**; cả danh mục 292; phiếu sửa dòng 3–4, bảng A (Hương An cần xem), bảng C (63 cơ sở), thêm bảng E (2 cặp tên gần trùng); biên bản thêm mục ĐÍNH CHÍNH. Bài đi lại: m-4, m-5 sửa; m-2 thêm bài Đèo Hải Vân; m-3 giữ (E đã mở trang ĐSVN 13/11 thấy các chặng bán vé — ghi vào Nguồn). Chia đoạn lại: 12 / 0 lỗi.
- 20:06 13/11/2026 — C kiểm lại: **ready_for_user_confirmation** (M-1, m-1…m-5 đóng). md5: v3 `d736f5a6c21e` · phiếu `2f4772b5f3c3` · bài đi lại `1ccfc5f639d6`. Phiếu + bài chờ A đưa User.
- 20:27 13/11/2026 — **TRIPO vòng 6 XONG** — report `report_agent/2026-11-12_ra_khoang_cach/b_tripo_v6_lap_ke_hoach.md` mục 5 (đầu file đổi DỞ ⇒ XONG). Lập kế hoạch 6 / 6 đủ luồng (k3–k6 E chạy; phương án sau 62–102 s); 7 chặng quá giờ đóng cửa ở 4 / 6 lịch; 3 tab tìm + bản đồ + đổi ngôn ngữ + trang chủ / chân trang + 7 danh mục đã chạy, lưu `data/tripo_v6_2026-11-12/tinh_nang/`. Lỗi script của E lần 1 (gõ vào ô ngày ở 3 tab) đã sửa, chạy lại. Bảng so hue_rag + đề xuất học / bỏ qua ở mục 5c. Tiền 0 USD. Không còn trình duyệt / tiến trình nào. **Tiếp: chờ A (review nghiệm thu đợt 1 khi B xong).**
- 20:29 13/11/2026 — A giao: **ca kiểm PHỤ cho nghiệm thu đợt 1 XONG** — `data/phase_9/lich_trinh/bo_do_v2/ca_phu_13_11.jsonl` (sha256 `223b8768fa68`, 13 dòng: 4 ca Nhị Hồ mùa mưa + 1 đối chứng mùa khô · 4 cặp dày ↔ thong thả) + `ca_phu_13_11.md` (`b109869ca065`). 3 file đã băm không đổi. Không trùng dòng nào với bộ 20 / bộ quyết 12. Báo riêng, không vào luật đạt. **Rảnh — chờ review nghiệm thu khi B xong (c)–(e).**
- 21:31 13/11/2026 — A giao: **review nghiệm thu đợt 1 XONG — ready** cho kết luận "trượt, không bật" (0 blocker / 0 major / 4 minor: chấm thiếu điều kiện tên ngoài bảng · 3 / 80 tổ hợp 1 ngày ba kiểu đi trùng khung không ghi chú · ghi chú bậc thang lặp · chữ "theo plan §5"; + lỗi bộ đo E: cặp D4 có trẻ em). Mọi số tính lại độc lập khớp. Ca dò 13.176 khung: điểm tạm dừng 0 lần trong tháng dừng. `report_agent/2026-11-12_ra_khoang_cach/e_review_len_ke_hoach_dot_1.md`. **Sự cố dữ liệu riêng tư (E tự phát hiện):** `e_review_kho3_c.md` (đã push trong `e74c6df`) ghi tên quán + địa chỉ từ kho ⇒ E đã viết lại file (nhãn Q-a … Q-e); lịch sử git vẫn còn — A / User quyết. `c_review_kho3_e.md` của C có tên cơ sở lưu trú (báo A).
- 21:40 13/11/2026 — A giao (User duyệt vòng sửa lịch trình + bài kho 2 điểm thiếu): **viết 2 bài NHÁP** (bảo tàng cổ vật cung đình · không gian lưu niệm họa sĩ) — chưa ghi kho. File sẽ ghi: `data/sua_kho_2026-11-13_diem_mong/` (mới: 2 bài nháp + bảng dữ kiện nguồn), `data/tra_cuu_cli/` (Codex), file này.
- 21:47 13/11/2026 — **2 bài nháp XONG** (`data/sua_kho_2026-11-13_diem_mong/`: 2 bài + `BIEN_BAN.md`): chia đoạn 12 + 15, 0 lỗi; đích đề xuất `heritages/heritage/` + `travel/places/`; 6 mâu thuẫn ghi ở biên bản (3 với kho: người lập Không gian lưu niệm · số nhà Lê Lợi · bảo tàng xếp nhầm bờ Nam). Chờ C review. Tiền 0 USD (Codex 1 lượt).
- 21:50 13/11/2026 — C review 2 bài: **ready** (0 / 0 / 3 minor). E sửa m-1 ("Tấn tuồng nhân loại" là loạt tác phẩm, không phải tên phòng); m-2, m-3 giữ (đã ghi một nguồn ở biên bản). Chờ A / User ghi kho.
- 22:02 13/11/2026 — A giao ghi kho (User duyệt gói) rồi **DỪNG NGAY** (User: "mai rồi đo"). E **chưa làm bước nào**: chỉ đọc spec kho 3 §4; 0 sao lưu, 0 sửa kho, 0 lượt có phí, 0 server.
- **VIỆC ĐẦU PHIÊN SAU (gói User đã duyệt 13/11, A ghi ở handoff):** MỘT lần ghi kho gồm (1) 2 bài `data/sua_kho_2026-11-13_diem_mong/` ⇒ `heritages/heritage/` + `travel/places/`; (2) bài `data/sua_kho_2026-11-12_dot_3/bai_nhap_di_lai_o_hue.md` ⇒ `travel/services/`; (3) sửa 3 chỗ kho theo nguồn: người lập không gian lưu niệm (theo trang chính thức) · số nhà khu Lê Bá Đảng trên Lê Lợi (theo Sở Du lịch) · bài vé gộp: bảo tàng không thuộc "Nam sông Hương"; Ga Huế GIỮ. Thứ tự: mốc "trước" K1 Golden 176 + K2 an toàn 32 trên kho hiện tại (TRƯỚC khi ghi) ⇒ sao lưu file sửa vào `knowledge-base-hue/meta/` + build record + sparse state ⇒ ghi + chia đoạn thử ⇒ xoá sparse state cũ, dựng lại tại chỗ (`guides/full_corpus_rag.md` "Build lại index") ⇒ `/health` ⇒ đếm đoạn mỗi file mới = 12 / 15 / 12 ⇒ T1 158 so `64656a87c109` ⇒ K1 / K2 "sau", chấm cùng lượt mù. Trần 0,15 USD. A báo B / C dừng có phí + server. Report `report_agent/2026-11-12_ra_khoang_cach/e_ghi_kho_diem_mong_di_lai_implementation.md`. Dừng nếu dựng lỗi / K1 / K2 vỡ ⇒ báo A, không tự lùi.
- **Thêm vào gói đầu phiên sau (A chốt bàn quán OSM 13/11, handoff "Quán OSM — chốt"):** SAU K1 / K2 ⇒ đếm lại 6 câu "ăn gì gần X" (lượt đếm 12/11, mốc 1 / 6) + vài câu cụm Thủy Xuân / Kim Long (≈ 0,01 USD) ⇒ còn hỏng ở cụm OSM phủ thì báo A để lần ghi sau thêm bản nhẹ (≤ 6 quán OSM / cụm thiếu, rào C gộp); hỏng ở cụm OSM không phủ ⇒ báo cần nguồn khác.

---

# (lịch sử) STATUS E — KẾT PHIÊN 22:23 12/11/2026 (`date`) · terminal `hue-rag-33` (A `hue-rag-7d`, B `hue-rag-1b`, C `hue-rag-e1`) · Claude Fable 5.2 · vai thực thi

## (cũ) PHIÊN SAU ĐỌC TRƯỚC (viết 22:23 12/11/2026)

**E không còn tiến trình, server, worktree nào.** File tạm `/tmp/e_*` đã xoá. Nhánh Exa lưu ở tag `hoso/p9-tra-web-exa` (`76e976e`).

### Việc dở của E (theo thứ tự làm tiếp)
1. **Đợt bổ sung kho 3 — phần (a) lưu trú + (b) đi lại** (spec `docs/superpowers/specs/2026-11-12-bo-sung-kho-dot-3-design.md`, A đã ghi duyệt; User chốt Q1–Q5 theo khuyến nghị; trần 0,35 USD). **Chưa chạm kho.**
   - Đã có (private): `data/luu_tru_2026-11-12/` — `co_so_luu_tru_hue.csv` (316 cơ sở; 151 có hạng / đạt chuẩn), `bien_ban.json`, `html_tho/` (73 trang), `luu_tru_theo_cum_nhap.json` (bảng nháp), `buoc_0_gan_khu.md`, `tools/gan_khu_v2.py`, `osm/duong_co_ten_hue.json` (1.652 đoạn đường có tên, tải 22:22 12/11 — **chưa dùng**), `phieu_khu_luu_tru_cho_user.md` (**chưa đưa User**).
   - **Bước kế:** dùng file OSM gán khu cho các tên đường (toạ độ giữa đường ⇒ điểm tham quan gần nhất ⇒ cụm ⇒ khu; đường cắt hai khu ⇒ "cần xem") ⇒ cập nhật bảng C của phiếu (User chỉ xem dòng "cần xem") ⇒ báo A tỉ lệ gán (hiện **54 % = 83 / 151**) ⇒ User xem phiếu ⇒ sinh bài lưu trú nháp bằng script (đoạn văn ≤ 6 cơ sở / đoạn, đặt trong `travel/services/`, không giá / liên hệ) + `luu_tru_theo_cum.json`.
   - (b) Đi lại: `data/sua_kho_2026-11-12_dot_3/bai_nhap_di_lai_o_hue_DANG_DO.md` = **mới có bảng dữ kiện có nguồn + dàn ý**, chưa viết bài. Nguồn tra `data/tra_cuu_cli/2026-11-12_e-di-lai-hue/`.
   - (c) Ăn gần: C đã làm tới trước bước ghi kho (`data/sua_kho_2026-11-12_an_gan/`); E đề nghị C rút ngắn tiêu đề mục (dài tới 305 ký tự).
   - Ghi kho + dựng lại chỉ mục: **chờ A xếp lịch** sau khi User xem phiếu (quán / mốc của C + khu lưu trú của E). Trước khi ghi kho: A chốt lại ngưỡng K6.
2. **Plan lưu trú "khu nên ở + link"** (`docs/superpowers/plans/2026-11-12-luu-tru-khu-va-link-plan.md`, A duyệt; có 2 mục "sửa sau duyệt"): **code chưa làm**; bước 0 đếm (theo nguồn · từ khoá · hợp) chưa chạy; bảng `khu_v1.json` chưa lập (lấy từ bảng A + B của phiếu khi User xác nhận).
3. **Biểu mẫu "Lên kế hoạch"**: bộ đo đợt 1 xong — `data/phase_9/lich_trinh/bo_do_v2/`: `yeu_cau_20.jsonl` `8f89c1b341ca` · `bo_quyet_12.jsonl` `f715aac06ddc` · `dinh_nghia_cham.md` **`253d6d9f9910`** (mã `b837…` đã gửi A / B lúc đầu là mã CŨ). E là người viết bộ đo ⇒ **không** code đợt 1; có thể review.

### Việc chờ User / A
- User: xem phiếu khu lưu trú (sau khi E gán bằng OSM); câu "bỏ câu chứa số sai thay vì bỏ cả mục web" (A ghi danh sách chờ); bật cờ `het_luot_bo_cong_cu` (E khuyến nghị bật kèm phép theo dõi).
- Tra toạ độ quán bằng Photon: E **không làm** (việc C bị chặn + nơi nhận mới); A báo máy chủ Photon không trả lời.

### Kết quả phiên 12/11 (E)
- Review: plan B7 (2 vòng) · kết quả B7 giữa kỳ (+ kiểm chẩn đoán S1 của C) · nhánh `p9-het-luot-tim` (ready, đã merge) · spec biểu mẫu của C (bản 1 → 3.2, 4 lượt).
- Báo cáo: khoảng cách agentic RAG (`e_khoang_cach_agentic.md`) · tìm web Serper ↔ Exa (`e_tim_web_serper_exa.md`, mục 1–7) · nguồn lưu trú (`e_nguon_luu_tru.md`) · bộ đo biểu mẫu (`e_bo_do_len_ke_hoach.md`) · kiểm giờ mở cửa Đại Nội (`data/tripo_v5_2026-11-12/kiem_gio_mo_cua.md` — kết luận chưa rõ).
- **Exa: KHÔNG bật.** Thí nghiệm chỉ-bước-tra: Exa 25 ↔ Serper 17 / 42 (đạt luật); đo qua server thật: **14 ↔ 13** (không đạt +3). Hồ sơ `data/exa_2026-11-12/`, plan `2026-11-12-tra-web-exa-plan.md`, tag `hoso/p9-tra-web-exa`.

### Tiền E phiên 12/11 (thật, từ log / trường tiền)
Thí nghiệm Exa 0,069 + X2–X6 ≈ 0,126 ⇒ **≈ 0,195 USD thật**; tín dụng miễn phí Exa đã dùng ≈ 0,82 USD (không phải tiền thật). Mọi việc khác 0 USD API (Codex 6 lượt, agent con chấm 6 lượt, WebFetch = quota).

### Bẫy / đã học phiên 12/11
- **Đọc nhầm trường tiền:** `turn_usd` của trace = tiền cả lượt (model + tra) — E báo "0,049 / bên" là tiền model, xin nâng trần không cần. Tách tiền tra ↔ model trước khi báo.
- **Ước tiền thiếu:** plan ghi 0,05 cho lượt "qua server thật" trong khi mỗi câu qua server là cả lượt (≈ 0,0013) ⇒ thật ≈ 0,13. Ước theo đường đo thật, không theo bước con.
- **Đếm trên dòng lặp:** dữ liệu mở 6.794 dòng chỉ có 208 dòng khác nhau ⇒ E báo tỉ lệ gán khu 71 %, thật là 54 % (C bắt). Bỏ trùng trước mọi phép đếm trên dữ liệu ngoài.
- **Kết quả ở bước con không chuyển sang đường thật:** Exa hơn rõ khi chỉ đo bước tra, mất lợi thế khi qua cổng thật + luật kiểm ⇒ thí nghiệm chọn nhà cung cấp phải đo trên đường người dùng đi ngay từ đầu.
- **Ghi trước phải vào git trước lượt có phí** (C nêu: cấu hình Exa vào git sau khi có kết quả).
- Review plan so hai bên: hỏi "mỗi sàn 'mới so với mốc' có cùng mẫu số ở hai bên không" (bỏ sót ở plan B7). Kiểm "harness dùng lại được" phải mở xem nó dựng cho mấy bên ở cả hai bản code.
- Log `application.log` trộn pytest ⇒ lọc lượt thành công có `usd`; ghép theo `turn_id`.
- Script sửa file bằng heredoc Python: `\`` trong chuỗi thường thành `\\`` thừa — kiểm `grep` sau khi ghi.

---

# (nhật ký trong phiên) STATUS E — PHIÊN 12/11 (mở 18:40 12/11/2026, `date`) · terminal `hue-rag-33` (A `hue-rag-7d`, B `hue-rag-1b`, C `hue-rag-e1`) · Claude Fable 5.2 · vai thực thi

- 18:45 12/11/2026 — A giao: **review plan B7 nháp** (người viết C), 0 USD, chỉ đọc. **Vòng 1 XONG 18:49 12/11/2026 — changes_requested** (plan sha `5413ae469c5e`): M-1 bản sao `do_cuoi.py` "chỉ đổi hằng số" không chạy được (tool dựng cho 3 bên cố định, bên mốc chép từ file 30/10, cần bên A/A; `generate` ở `p9-moc` không nhận file câu tuỳ ý) · M-2 kết luận (i) chưa ghi chỉ số / đơn vị / cách tính CI · M-3 S2 / S2b + vế "0 truy vấn chứa tên" không có lượt đo, Golden qua `generate` không đi cổng web · 6 minor (đề xuất cắt 3 lượt phía RAG). Cờ plan §2 ↔ `settings.yaml` hôm nay: khớp 14 / 14. File: `docs/superpowers/plans/2026-11-10-phase-9-b7-plan_review.md` (mới), file này, dòng E trong `CURRENT_HANDOFF.md`. Tiền: 0 USD. **Vòng 2 XONG 19:02 12/11/2026 — ready** (bản 2 sha `da7bff5d0c4e`: 0 major, 5 minor n-1…n-5; `ngay_moi_sealed` không mở ở lượt giữa kỳ — đạt). Chờ A duyệt sha.
- Bẫy / đã học 12/11: log `application.log` trộn pytest (outcome lỗi) ⇒ đếm phải lọc lượt thành công có `usd`; Codex trích câu "nguyên văn" không có trong tóm tắt bài (kiểm ra) ⇒ câu trích luôn mở trang đối chiếu.
- Bẫy / đã học 12/11 (review): kiểm "harness dùng lại được" phải mở xem nó dựng cho mấy bên và nhận đầu vào gì ở **cả hai** bản code, không chỉ kiểm file tồn tại.
- 18:59 12/11/2026 — A giao (User giao 18:58): **rà khoảng cách tới agentic RAG + nghiên cứu repo / paper**, 0 USD API, không spec / code. **XONG 19:12 12/11/2026** — report `report_agent/2026-11-12_ra_khoang_cach/e_khoang_cach_agentic.md`: không nguồn nào đặt ngưỡng "agentic RAG"; hue_rag = luồng code + một vòng agent có công cụ; thiếu lập kế hoạch / tự soát bằng model / nhiều agent (chưa có lỗi đòi); 8 ứng viên, 3 hạng đầu là phép đếm 0 USD trên kết quả B7 giữa kỳ (độ ổn định · tách tìm trượt ↔ model không dùng đoạn đúng · số trong câu trả lời ⊂ đoạn trích). github.txt: 9 / 9 nguồn đã đọc 04/11. Chờ A. File sẽ ghi: `data/nghien_cuu_agentic_2026-11-12/` (mới), `report_agent/2026-11-12_ra_khoang_cach/e_khoang_cach_agentic.md` (mới), `data/tra_cuu_cli/` (kết quả Codex), file này. Ngắt để review plan B7 bản 2 khi C nhắn (kiểm thêm: `ngay_moi_sealed` 7 câu KHÔNG mở ở lượt giữa kỳ).
- 19:12 12/11/2026 — **rảnh — chờ B báo xong B7 giữa kỳ** ⇒ E review cả việc (report + harness `data/phase_9/b7/tools/` + tính lại vài số từ dữ liệu). Ba phép đếm 0 USD trên B7 do C làm — E không làm trùng.
- 19:55 12/11/2026 — A giao: **review kết quả B7 giữa kỳ** (0 USD, không mở kín). **XONG 20:02 12/11/2026 — ready** (0 major, 5 minor): E tính lại độc lập mọi số chính, khớp (câu tụt 4 = ngưỡng; từ chối nhầm 3 ↔ 13; Holm 3 / 3; S2b 2 / 44 và S1 thiếu cảnh báo 3 / 6 ↔ 1 / 6 là phạm thật; tiền 0,288); sai 1 số ở report (nhiều nguồn 6 / 11 / 1, không phải 5 / 12 / 1); vòng S-AT thêm ngoài plan; 12 tổ hợp biểu mẫu còn nợ. Mục 7: đồng ý chẩn đoán của C về S1 (đoạn chứa điều kiện có 8 / 8 lần trợ lý, 0 / 7 lần mốc) + đề xuất thước cho lượt cuối. Script tính lại: `/tmp/e_b7_review/` (xoá được). File sẽ ghi: `report_agent/2026-11-08_phase_9_ban_13/b7_review.md` (mới), file này.
- 20:05 12/11/2026 — vòng tự soi 1 xong (A chốt ở handoff): bỏ phần kín giữa kỳ; lượt cuối chỉ review phần đổi thước an toàn. **Rảnh — chờ User chọn việc (qua A).** Đã học: review plan so hai bên phải hỏi "mỗi sàn kiểu 'mới so với mốc' có cùng mẫu số ở hai bên không" (E bỏ sót ở 2 vòng plan B7); ngưỡng đếm "câu đổi kết luận" phải tách nhiễu người chấm.
- 20:08 12/11/2026 — A giao: kiểm giờ mở cửa một di tích lệch 30 phút (kho ↔ TRIPO ↔ trang chính thức), 0 USD, KHÔNG sửa kho. **XONG 20:12 12/11/2026 — kết luận CHƯA RÕ**: trang đơn vị quản lý không mở được (E + Codex); không nguồn nào ngoài TRIPO ghi giờ mở 07:30; kho khớp nguồn mở được gần chính thức nhất. Rảnh — chờ A. File sẽ ghi: `data/tripo_v5_2026-11-12/kiem_gio_mo_cua.md` (mới), file này.
- 20:38 12/11/2026 — A giao (User hỏi): **rà tìm web Serper ↔ Exa + nguồn lưu trú**, 0 USD, KHÔNG gọi Exa. **XONG 20:51 12/11/2026** — `e_tim_web_serper_exa.md` (Serper 0 / 73 lần lỗi; 37 % lượt không ra mục do luật kiểm, đoạn trích ~147 ký tự, 32 % kết quả là facebook; Exa đáng thử nhưng chưa đủ căn cứ bật; nháp plan thí nghiệm ≈ 0,11 USD chờ User), `e_nguon_luu_tru.md` (dữ liệu mở không có lưu trú; nguồn đủ nhất = cơ sở dữ liệu du lịch quốc gia ~340 trang HTML; sàn đặt phòng có điều khoản cấm thu thập), plan nháp `docs/superpowers/plans/2026-11-12-luu-tru-khu-va-link-plan.md` (chờ C review + User chọn (a) / (b) về link mang ngày / số người). File sẽ ghi: `report_agent/2026-11-12_ra_khoang_cach/e_tim_web_serper_exa.md` (mới), `data/nghien_cuu_agentic_2026-11-12/yeu_cau_codex_exa.md`, file này. Sau đó: review nhánh `p9-het-luot-tim` của B.
- 20:43 12/11/2026 — A thêm (User chốt lưu trú (c)): (1) phần nguồn dữ liệu lưu trú viết đủ trong report tìm web (khảo sát công khai, KHÔNG cào thử); (2) plan mức nhẹ `docs/superpowers/plans/2026-11-12-luu-tru-khu-va-link-plan.md` (mới) — code CHƯA làm, chờ nhánh `p9-het-luot-tim` merge; C review. **Plan nháp xong; code chưa làm.**
- 20:55 12/11/2026 — A giao (User chốt "TRIPO hơn chỗ nào thì học; cần dữ liệu thì tìm, cào, bổ sung"): (1) review `p9-het-luot-tim` khi B push; (2) tải danh sách cơ sở lưu trú TP Huế từ cơ sở dữ liệu du lịch quốc gia ⇒ `data/luu_tru_2026-11-12/` (private; ≥ 2 s / trang, một luồng; chỉ tên · loại · hạng · địa chỉ; CHƯA vào kho) — **chờ B nhắn "đo xong" mới chạy**; (3) spec `docs/superpowers/specs/2026-11-12-bo-sung-kho-dot-3-design.md` (mới) cho User duyệt, C review. **Đang làm (3) + soạn script (2).**
- 21:16 12/11/2026 — **Thí nghiệm Serper ↔ Exa XONG** (A giao, User duyệt Exa): 42 câu × 3 bên, chấm mù 2 người (khớp 77 / 80) ⇒ mục đúng + trả lời được: Serper 17 · **Exa 25** · Exa lọc mạng xã hội 20 ⇒ Exa cấu hình 1 đạt luật ghi trước (≥ +5, sàn 0, p95 2,2 s). Tiền thật **0,069 USD** (+ 0,581 tín dụng miễn phí Exa). Report mục 5–6 `e_tim_web_serper_exa.md`; plan nháp `docs/superpowers/plans/2026-11-12-tra-web-exa-plan.md` (`570805aa2a78`) chờ A; dữ liệu `data/exa_2026-11-12/`. **Lỗi E:** báo nhầm tiền model 0,049 / bên (là tiền cả lượt) ⇒ xin nâng trần không cần — đã đính chính.
- 21:16 12/11/2026 — **Tải danh sách lưu trú XONG:** 316 cơ sở TP Huế, 73 trang, 21:12–21:15, `data/luu_tru_2026-11-12/` (HTML thô + `co_so_luu_tru_hue.csv` + `bien_ban.json`); chỉ tên · loại · hạng · địa chỉ · nguồn nhập; CHƯA vào kho. Danh mục gần như chỉ khách sạn (0 homestay).
- 21:16 12/11/2026 — **Spec đợt bổ sung kho 3 nháp bản 1 XONG:** `docs/superpowers/specs/2026-11-12-bo-sung-kho-dot-3-design.md` — chờ C review + User duyệt (5 câu Q1–Q5).
- 21:16 12/11/2026 — Plan lưu trú bản 2 `d2b4bc486480` A đã duyệt; code chờ nhánh `p9-het-luot-tim` merge. **Chưa làm:** review nhánh B (chờ push); việc tra toạ độ quán bằng Photon (xem "Câu hỏi cho A").
- Bẫy / đã học thêm 12/11: trường `turn_usd` của trace = tiền cả lượt (model + tra) — tách trước khi báo; trang chi tiết của nguồn lưu trú không có thêm trường, loại / hạng lấy qua bộ lọc.
- 21:17 12/11/2026 — A giao (qua handoff, C nhắn): **review spec "Lên kế hoạch bản 2"** của C (`aeac8c589822`), 0 USD, chỉ đọc. **Vòng 1 XONG 21:19 12/11/2026 — changes_requested** (2 major: ngưỡng "đổi lịch" chốt sau khi code không phải ghi trước; đợt 2 lệch plan lưu trú + spec kho 3; 6 minor). File sẽ ghi: `docs/superpowers/specs/2026-11-12-len-ke-hoach-ban-2-design_review.md` (mới).
- 21:26 12/11/2026 — spec "Lên kế hoạch bản 2" **vòng 2 XONG — ready** (bản 2 `8969c7275346`). Plan lưu trú sửa sau duyệt (L7: lịch biểu mẫu ≥ 2 ngày có thẻ) `b24020ed9dc9`.
- 21:26 12/11/2026 — **Exa: review của C xong** (kết quả đứng; F-1: 7 / 109 nguồn là trang của chính Exa, 5 / 25 mục đạt có dùng ⇒ bỏ 5 mục thì 20 < 22 — đã ghi report mục 6b). Plan Exa **bản 2** `21e620888bee` (hạn riêng Exa 3 s, trần 40 lượt / ngày, tham số loại tên miền, đối chiếu sàn 0,0005, X6 đủ 42 câu) chờ A duyệt. **Code phần 0 USD xong:** nhánh `p9-tra-web-exa` commit `4b37051` (worktree `/tmp/e_exa`, CHƯA push, chưa đo có phí, chưa merge); test: `test_b6_tra_web` + `test_tra_web_exa` + `test_settings_env` + `test_assistant_boundary` 116 passed (không key), 27 passed (có `--env-file`, 2 file chạm cờ). **Còn nợ:** trường `nguon` trong log (`assistant.py`, sau khi nhánh B merge); rebase `settings.yaml`; X2–X6 có phí. Worktree có 2 symlink `data`, `knowledge-base-hue` — gỡ khi xong.
- 21:32 12/11/2026 — nhánh `p9-tra-web-exa` `4b37051` **đã push** (A duyệt plan Exa bản 2; B review; phần có phí chờ nhánh B kết luận). Spec kho 3 **bản 2** (sửa theo review C 3 major + mức lịch "đủ 4 phần" User chốt: Q3 đổi sang thêm quán dữ liệu mở có nhãn; lưu trú đặt trong `travel/services/`, đoạn văn ≤ 6 cơ sở — đã probe chunker; địa chỉ danh mục không có phường ⇒ gán cụm bằng ước toạ độ). Review nhánh `p9-het-luot-tim` `ab66f5e` của B **XONG 21:37 12/11/2026 — ready** (merge cờ tắt; 5 minor; E tính lại khớp; khuyến nghị bật kèm phép theo dõi) — `report_agent/2026-11-12_ra_khoang_cach/b_het_luot_tim_review.md`. Spec kho 3: C vòng 2 ready, User chốt 5 quyết định; E sửa chữ bước 6 / K3 + nhận giữ bảng cụm ⇒ khu. **Tiếp:** các bước 0 USD không chạm kho của spec kho 3; kiểm phần đổi spec biểu mẫu bản 3 của C; rebase nhánh Exa sau khi nhánh B merge.
- 22:02 12/11/2026 — **TÌNH TRẠNG (đọc dòng này trước):**
  - **Exa X2–X6 ĐANG CHẠY** (A duyệt trần 0,20 USD thật; ghi trước ở cuối plan `2026-11-12-tra-web-exa-plan.md`): nhánh `p9-tra-web-exa` đã rebase lên `main` có nhánh B, commit `76e976e` (CHƯA push lại — push sau khi đo); worktree `/tmp/e_exa` (2 symlink). Lượt Exa qua server cổng 8891 xong ⇒ `data/exa_2026-11-12/server/exa.jsonl` (42 câu: 15 có mục · 13 không tin cậy · 2 chưa xác minh · 12 không tra); **lượt Serper đang chạy nền** ⇒ `server/serper.jsonl`; server nền task `bwzuez7so` — **TẮT bằng TaskStop khi xong**. Còn: chấm mù 2 người (lô từ hai file server), X3 an toàn 32 ×1 cờ exa (chấm phần mục web), X5 (khoá Exa sai ⇒ `exa>serper`), report mục 7 + push + B kiểm + báo A "bật được / không". Nhắn B "đo xong" khi hết lượt đo.
  - **Kho 3:** spec bản 2 A đã duyệt (sha `132b820a7763` sau mục "sửa sau duyệt"); bước 0 gán khu 71 % (`data/luu_tru_2026-11-12/buoc_0_gan_khu.md`); Codex "Đi lại ở Huế" đã về (`data/tra_cuu_cli/2026-11-12_e-di-lai-hue/` — CHƯA đọc). Còn (0 USD, không chạm kho): bảng tay đường ⇒ khu, `quan_theo_cum.json` nháp, bài nháp trong `data/`, phiếu User. Ghi kho + dựng lại: chờ A xếp lịch.
  - **Biểu mẫu:** kiểm 5c bản 3.2 xong (2 mâu thuẫn số S-1, S-2 — cuối file review); **bộ đo đợt 1 xong** `data/phase_9/lich_trinh/bo_do_v2/` (`8f89c1b341ca` · `f715aac06ddc` · `b837ecbb044e`) + `report_agent/2026-11-12_ra_khoang_cach/e_bo_do_len_ke_hoach.md`.
  - Plan lưu trú `8a8601518f27` (đã duyệt + 2 sửa sau duyệt); code chưa làm.
  - Tiền E hôm nay (thật): thí nghiệm Exa 0,069 + lượt server Exa (chưa cộng) — cộng lại ở report.
- 22:16 12/11/2026 — **Exa X2–X6 XONG — X6 KHÔNG ĐẠT (Exa 14 ↔ Serper 13 qua server thật; cần +3) ⇒ không bật Exa.** X1, X2, X4, X5 đạt; X3 một phần. Tiền thật X2–X6 ≈ 0,126 (cả việc Exa ≈ 0,195 + ≈ 0,82 tín dụng Exa). Report mục 7 `e_tim_web_serper_exa.md`. Nhánh `p9-tra-web-exa` `76e976e` đã push (cờ mặc định Serper) — merge sau cờ hay lưu hồ sơ: A / User quyết. Server 8891 đã tắt. Worktree `/tmp/e_exa` còn (gỡ khi A quyết: `rm` 2 symlink + `git worktree remove`). Mã băm mới của `dinh_nghia_cham.md`: `253d6d9f9910`.
- 22:20 12/11/2026 — Exa: A quyết LƯU HỒ SƠ (tag `hoso/p9-tra-web-exa`), worktree `/tmp/e_exa` đã gỡ. **Kho 3:** ĐÍNH CHÍNH tỉ lệ gán khu = **54 %** (71 % sai vì dữ liệu mở lặp dòng — C phát hiện); phiếu `data/luu_tru_2026-11-12/phieu_khu_luu_tru_cho_user.md` (3 bảng, 22 đường) chờ User; C làm xong phần (c) (`data/sua_kho_2026-11-12_an_gan/`); Codex đi lại đã đọc + E kiểm 3 ý (xe buýt sân bay dừng 01/04/2024; luật GPLX 36/2024 Điều 57, 59, hiệu lực 01/01/2025). **Còn:** bài nháp đi lại + bài nháp lưu trú (sau khi User xem phiếu) trong `data/sua_kho_2026-11-12_dot_3/`; rồi báo A xếp lịch ghi kho. Bẫy: đếm trên dữ liệu mở phải bỏ dòng lặp trước.

# (lịch sử) STATUS E — KẾT PHIÊN 22:40 10/11/2026 (`date`) · terminal `hue-rag-e4` (A `hue-rag-55`, B `hue-rag-05`, C `hue-rag-4f`) · Claude Opus 5.5 · vai thực thi

## PHIÊN SAU ĐỌC TRƯỚC (viết 22:40 10/11/2026)

**E không có code dở, không worktree, không server.** `/tmp/e_do_dtl/` (ca dò review, xoá được). **Tiền E phiên 10/11 ≈ 0,0357 USD** (T1 nhanh 0,030857 = mốc
0,009263 + nhánh 0,006859 + an toàn × 2 0,004354 + Golden 9 0,004587 + lượt lại 0,003420 + an toàn 0,002374 · bộ H 0,002623 · ca dò review 0,002213 — `chat_metrics.usd`
/ dòng in của harness; chấm bằng sub-agent 0 USD API).

### Kết quả phiên 10/11 (việc của E)
- **T1 nhanh — câu ngày: code tính sẵn ngày trước lần gọi model đầu — MERGE `1633c18`** (User duyệt). Chữ đầu p50 5,60 ⇒ 2,35 s, p95 10,14 ⇒ 4,56 s; 0,00049 ⇒ 0,00036 USD;
  model gọi `ngay_lich` 0 lần. Report `report_agent/2026-11-02_phase_9_code/e_t1_nhanh_implementation.md`; review C `e_t1_nhanh_review.md` (M-1 "mùng N tháng <số>" ⇒ đã sửa).
  Báo cáo User: SINH bản 48 + LUONG bản 35 (A commit `3e0607b`; sau đó A đổi tên file theo số thứ tự đọc `f380d76`).
- **Bộ giữ mù H cho B** (định tuyến lịch): `data/phase_9/dinh_tuyen_lich/giu_mu_sealed.jsonl` sha `5ef0d41b62f2` — E viết + chạy một lần trên bản khoá `8cd30cbb359a` ⇒ 3 sàn đạt. **Đã dùng.**
- **Review nhánh B `p9-dinh-tuyen-lich` `e8e07c9`** ⇒ ready (0 / 0 / 2 minor), `report_agent/2026-11-08_phase_9_ban_13/b_dinh_tuyen_lich_review.md`. Sửa nhãn R11 trong
  `data/phase_9/t1/bo_sau_g.jsonl` (refuse ⇒ trả lời; nhãn cũ ở `nhan_cu_truoc_10_11`).
- Brainstorm sắp xếp `bao_cao_he_thong/` (với C) — A chốt: C viết mẫu README + LUONG ⇒ User duyệt ⇒ A chia file khâu cho C + E.

### Việc mở liên quan E (chờ A / User)
- **Sắp xếp báo cáo:** khi User duyệt mẫu, A giao E một phần file khâu (luật đã chốt: mỗi số / định nghĩa một nơi — README; thân bài không mã; phần "đang chạy" ≤ ~40 dòng).
- **Theo dõi (từ review B, m-1):** câu lịch thuần đi trợ lý có thể bị rút vì model không ghi [n] (1 / 9) — đếm trên ≥ 20 câu trước khi sửa; không tự gắn [n] bằng code.
- Bộ ngày gốc 30/10 `data/ngay_hien_tai_2026-10-30/questions.jsonl` R11 còn nhãn "từ chối" — A quyết.
- Giọng nói: chờ User thu 40 câu (`data/phase_10/giong_noi/thu/` vẫn rỗng). Bảng điểm v7: chờ User. Nhánh `p9-t1-nhanh` đã merge — xoá khi User / A muốn.

### Bẫy / đã học (phiên 10/11)
- **Gỡ worktree xoá luôn `backend/logs/` của nó** ⇒ mất dòng `chat_metrics` lượt nhánh (số đã vào report kịp). **Trước `git worktree remove`: chép log cần giữ ra `data/`.**
- **Dò ngày âm bằng chữ: "mùng N tháng <số>" thường là ngày DƯƠNG** (Quốc khánh) — chỉ tính âm khi có chữ "âm"; "rằm", tháng chữ (Giêng, Chạp, Tư…) mới ngầm hiểu âm.
- **Có đủ hai lần (đã qua / sắp tới) chưa đủ:** câu "năm nay" model vẫn chọn lần sắp tới ⇒ ghi thẳng dòng của đúng năm âm được nói (code).
- **Dao động định tuyến** làm lệch so sánh câu ngày (cùng chuỗi gửi, khác tuyến) ⇒ báo tách nhóm "câu đi trợ lý" và kiểm chuỗi gửi định tuyến giống byte trước khi đổ lỗi cho thay đổi.
- **Đo tốc độ khi session khác chạy pytest / docker** ⇒ không dùng số đó cho tốc độ (nhắn "bắt đầu đo" / "đo xong" giữ được lượt chính sạch).
- Hook pre-commit chặn câu test chép gần nguyên văn kho (≥ 40 ký tự) — câu thử tự đặt ("Hội làng A…").

## (lịch sử) STATUS E — KẾT PHIÊN 22:29 09/11/2026 (`date`) · terminal `hue-rag-ea` (A `hue-rag-87`, B `hue-rag-99`, C `hue-rag-6a`) · Claude Opus 5.5 · vai thực thi

## PHIÊN SAU ĐỌC TRƯỚC (viết 22:29 09/11/2026)

**E không có code dở, không worktree, không server.** File thử còn ở `/tmp/e_g_probe/` (ca dò review, xoá được). **Tiền E phiên 09/11 ≈ 0,352 USD** (T1 xác nhận 0,025622 · T1 sau G 0,019393 · T2 0,171397 · T4 0,136074 — `chat_metrics.usd` / `usd` từng lượt; chấm bằng sub-agent 0 USD API).

### Kết quả phiên 09/11 (việc của E)
- **T1 ngày + âm lịch — BẬT** (`99ea59a` + `7eb1f12`, User duyệt). Report `report_agent/2026-11-02_phase_9_code/e_t1_ngay_implementation.md` §4e, §4f. Giới hạn: câu lịch thuần không nhắc Huế ⇒ định tuyến xếp ngoài phạm vi (A chọn giữ); "tháng tới / cuối tuần" model tự cộng.
- **T2 tra web thành công cụ — ÂM ⇒ hồ sơ** `hoso/p9-t2-web` (`e_t2_web_implementation.md` §4–5). Bộ hỏi kèm 10 E viết: `data/phase_9/t2_web/hoi_kem_10.jsonl` md5 `04aa82399972`.
- **T4 lịch trình câu gõ — ÂM ⇒ hồ sơ** `hoso/p9-t4-lich` (`e_t4_lich_implementation.md`). Gốc lỗi ở luật xếp / bảng B5; áp cả cho biểu mẫu: "dày lịch" gần như không tác dụng (bảng 1 / 28 điểm `ngan`), nhóm hạn chế không có buổi tối, không nói được lo mưa.
- **Review:** G 2 nhóm phần code (`g_cong_branch_review.md`, hồ sơ); G phương án B `p9-g-b` `2deec02` ready ⇒ merge `3b52017` (`g_b_branch_review.md`).
- **Báo cáo User (nháp, A commit):** `07_BAO_CAO_SINH_CAU_TRA_LOI_API.md` bản 45 ⇒ 46; `01_LUONG_HOAT_DONG_HE_THONG.md` bản 33; nhật ký `bao_cao_he_thong/nhat_ky/2026-11-09_ngay_am_lich_g_phuong_an_b_chot_deploy.md`. Chỗ số S5 để trống cho A (B đo: câu ngày p50 ~5,2 s — B báo).

### Việc mở liên quan E (không gấp, chờ A / User)
- Bảng điểm v7 (cột thời lượng) — User duyệt ⇒ "dày lịch" của biểu mẫu mới có tác dụng.
- Giọng nói: User thu 40 câu (`data/phase_10/giong_noi/bo_40_cau/huong_dan_thu_cho_user.md`) ⇒ G1 → G2 (plan `92ec551531fd`).
- Nhánh hồ sơ có thể xoá khi User muốn: `p9-t2-web`, `p9-t4-lich` (đã có tag); `p9-t1-sang-nam` đã merge.

### Bẫy / đã học (phiên 09/11)
- **Tiêu chí ghi trước phụ thuộc nền chưa có** (T1 tiêu chí 3 giả định G 2 nhóm) ⇒ phải xin "không áp dụng". Ghi nền giả định vào tiêu chí.
- **Pilot rẻ trước giả thuyết hành vi model:** T2 âm vì model từ chối cả câu — 10 câu hỏi kèm một bên (≈ 0,02) đã đủ thấy.
- **Đọc giới hạn cũ của khâu trước khi viết plan đo** (T4 âm vì giới hạn B5 ghi từ 06/11).
- **Phiếu chấm có phán đoán cần ngưỡng ghi trước** (Q3 (ii) hai người 21 vs 15).
- **Harness: chạy thử 0 USD với khoá giả** bắt được lỗi đếm lượt lỗi thành "từ chối" (`do_t4.py`).
- **Bộ "golden" trùng id** giữa `mau30` và `s2` (Golden OOS) ⇒ đếm theo bộ phải tách nguồn (T2 "3 / 38" thô).
- **Push từ worktree / lệnh ghép push + worktree remove** bị auto mode chặn ⇒ push từ working tree chung, tách lệnh.
- `chay_t1.py` ghi `turn_id`; `doc_metrics.py` đọc `chat_metrics` theo `turn_id`; log xoay vòng 10 MB (từ `ccc9f4f`) ⇒ lượt dài có thể cần đọc cả `application.log.1`.

## (lịch sử) STATUS E — KẾT PHIÊN 12:50 08/11/2026 (`date`) · terminal `hue-rag-22` (A `hue-rag-a8`, B `hue-rag-a1`, C `hue-rag-e9`) · Claude Opus 5.5 · vai thực thi

## PHIÊN SAU ĐỌC TRƯỚC (viết 12:50 08/11/2026)

**E không có code dở, không worktree, không server, không file `/tmp` của E.** Nhánh của E đều đã merge.

### 1. T1 ngày + âm lịch — ĐÃ Ở `main`, CỜ `ngay_lich: false`

- **Merge:** `e401c71` (T1) + `7ee12f1` (bộ dò bỏ số thứ tự / phân số; test stream, song song #6, biểu mẫu). `lunar-vn==1.4.0` có trong `uv.lock` của `main`.
- **Tài liệu:**
  - plan `docs/superpowers/plans/2026-11-08-phase-9-t1-ngay-plan.md` bản 2 `cdf2c061381a`;
  - report `report_agent/2026-11-02_phase_9_code/e_t1_ngay_implementation.md` (3 lượt đo, 4d sau review nhánh, đoạn lời thường cho `07_BAO_CAO_SINH_CAU_TRA_LOI_API`);
  - review `report_agent/2026-11-02_phase_9_code/t1_ngay_branch_review.md`.
- **Số đo (lượt 3, bộ ngày 27 câu, 2 người chấm mù khớp 27 / 27):** từ chối nhầm −8 · L1 / L3 0 · ngày / thứ sai 0 · chạm `max_turns` 0; an toàn 16 / 16; R8 kém ổn định (A chấp nhận).
- **Còn TRƯỚC KHI BẬT cờ:**
  1. **Lượt xác nhận trên câu ngày MỚI** (review m-5: "đạt" là trên chính bộ đã dùng để chỉnh qua 3 lượt) — gồm ca **1/1 – Tết** của M-1 (không nêu năm ⇒ code trả lần gần nhất + lần sắp tới). Server không dùng giờ giả được ⇒ viết câu kiểu "Tết năm sau" / "rằm tháng Giêng tới", hoặc đợi đúng mùa. Dùng `data/phase_9/t1/tools/chay_t1.py` (thêm bộ mới) + `kiem_l2.py` + brief `data/phase_9/t1/cham/brief_cham.md` + `dung_cap_mu.py`.
  2. **S5 tốc độ** (A xếp lượt, thứ tự B ⇒ E ⇒ C; **một server một lúc**):
     ```bash
     # (a) server nhánh = main với cờ bật TẠM: sửa backend/config/settings.yaml của một worktree từ main: ngay_lich: true
     git worktree add --detach /tmp/e_s5 main && ln -s /home/minhhieu/hue_rag/data /tmp/e_s5/data && ln -s /home/minhhieu/hue_rag/knowledge-base-hue /tmp/e_s5/knowledge-base-hue
     sed -i 's/^  ngay_lich: false /  ngay_lich: true  /' /tmp/e_s5/backend/config/settings.yaml
     cd /tmp/e_s5/backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port 8862   # nền
     cd /home/minhhieu/hue_rag && .venv/bin/python data/phase_9/t1/tools/chay_t1.py http://127.0.0.1:8862 chon:R1,R2,R3,R4,R6,R7,R8,R9,R10,R11,R12,E1,E2,E3,N1,N2,N3,A1,A2,A6 nhanh 5 data/phase_9/t1/ket_qua/s5_nhanh.jsonl
     # (b) tắt server ⇒ server main (cờ tắt) từ backend/ thư mục chính, cổng 8861, cùng lệnh với "moc" ⇒ s5_moc.jsonl
     # (c) đọc chat_metrics.first_text_ms THEO turn_id (log thư mục chính lẫn session khác); sàn p50 ≤ 3 s / p95 ≤ 5 s, không chậm hơn mốc quá nhiễu
     # (d) gỡ /tmp/e_s5 (rm 2 symlink + git worktree remove); ≈ 0,03 USD
     ```
     (`chay_t1.py` hiện chưa ghi `turn_id` vào file ⇒ thêm đọc `done.turn_id` từ SSE trước khi chạy.)
  3. **Sau khi G (B) vào `main`:** đo lại 5 câu ngày bị định tuyến xếp ngoài phạm vi — R11, A3, A4, A5, A10 (`data/phase_9/t1/bo_am_lich.jsonl`, bộ 15 cũ).
  4. **Giới hạn ghi khi bật:** "tháng tới / tháng sau / cuối tuần" vẫn do model tự cộng (code chỉ ghi tuần này / tuần sau / tháng này); chỉ năm 1976–2100; R8 "dịp lễ sắp tới" cần dữ liệu lịch sự kiện theo ngày (đợt 2 cổng).

### 2. Việc chờ User

- **Giọng nói — User GIỮ, sẽ thu 40 câu.**
  - Hướng dẫn: `data/phase_10/giong_noi/bo_40_cau/huong_dan_thu_cho_user.md` + tóm tắt cuối `data/ra_soat_tinh_nang_2026-11-08/E.md`.
  - `data/phase_10/giong_noi/thu/` còn rỗng.
  - Thu xong ⇒ G1 → G2 theo plan `92ec551531fd` (mục 4 dưới); 0 USD, chạy máy ⇒ hỏi A trước.
- **Phiếu bảng điểm v6** (`data/phase_9/lich_trinh/diem_cho_user_v6.md`, 4 ô) ⇒ E chốt `diem_v6.json` + `kiem_v6.py`.
- **17 link Maps theo toạ độ** (`data/phase_11/lich_nho/kiem_17_link.md`, B soạn) — User mở, tick đúng chỗ. Điểm nghi: "Kinh thành (Ngọ Môn – Kỳ Đài)" lệch ~0,6 km đông Đại Nội.

### 3. Bẫy hôm nay (chi tiết mục 3)

- **`uv sync` thường ở `main` gỡ `sherpa-onnx`** (giọng nói, chưa có trong lock) ⇒ chỉ dùng `uv sync --inexact`. `lunar-vn` nay đã ở lock nên không bị gỡ.
- **Một server thử một lúc** mỗi session (RAM); chạy mốc ⇒ tắt ⇒ chạy nhánh.
- **Đếm `chat_metrics` theo `turn_id`**, không theo mốc dòng (log thư mục chính dùng chung).
- **Token của lần gọi bị huỷ không đo được** (SDK `cancel()` không trả usage) — đừng gọi lần đã xong là "lần bị dừng".
- **Tách commit và push** thành 2 lệnh (auto mode chặn lệnh ghép).

### 4. Tiền

**E 08/11 ≈ 0,128 USD (cận trên).** Chi tiết ở mục Tiền.

### 5. Câu hỏi cho A

- T1 bật cờ khi nào (sau lượt xác nhận + S5)?
- Ghi R8 (cần lịch sự kiện theo ngày) vào backlog đợt 2 cổng?
- `chay_t1.py` dùng tiếp cho lượt xác nhận hay A muốn harness chung với T3 / G?

## 0a. Nhật ký việc 08/11 (theo giờ, lịch sử)

- 09:22 08/11/2026 — A giao: rà "Câu hỏi A còn nợ" (C211 rel, log xoay vòng, hạn mức OpenAI / Serper, mục deploy) — chỉ đọc, 0 USD. **XONG 09:23 08/11/2026**: (1) `rel` đã sửa (`markdown.js:36-46`); (2) log chưa xoay; (3) hạn mức chưa đặt, code không có trần tổng; checklist E-dep còn thiếu #1a / #5 / #6 / #7. **File:** `data/phase_12/deploy_nhap/ra_soat_no_A_2026-11-08.md` (mới), file này.
- 09:30 08/11/2026 — A giao: rà `.md` tìm tính năng đã ghi mà chưa làm (phần E: `bao_cao_he_thong/`, `docs/superpowers/specs` + `plans`, `guides/`, `README.md`) + hướng dẫn User thu 40 câu. Chỉ đọc, 0 USD. **XONG 09:37 08/11/2026**: (A) 22 ý · (B) 21 ý; 2 agent phụ quét specs / plans + guides, E kiểm 9 khẳng định (đúng 9 / 9); hướng dẫn thu trỏ phiếu C `bo_40_cau/huong_dan_thu_cho_user.md`. **File:** `data/ra_soat_tinh_nang_2026-11-08/E.md` (mới), file này.
- 09:38 08/11/2026 — A giao (1): sửa `README.md` phần tính năng theo `main` + sửa mâu thuẫn bộ kín. **XONG 09:40 08/11/2026** (chờ A commit): README phần tính năng + sơ đồ + API + giới hạn; Golden bản 9 (bộ kín 40 câu đã dùng 01/11 — DANH_GIA đúng) + dòng README `bao_cao_he_thong/`. **File:** `README.md`, `bao_cao_he_thong/09_BAO_CAO_BO_CAU_HOI_GOLDEN.md` hoặc `bao_cao_he_thong/10_BAO_CAO_DANH_GIA.md` (đoạn bộ kín). A commit.
- 09:38 08/11/2026 — A giao (2) (làm sau (1)): kiểm bật hỏi bằng ảnh trên cổng — worktree `/tmp/e_anh_bat`, nhánh `p10-anh-bat` từ `main`; sửa nhỏ giao diện nếu cần + câu ở trang Giới thiệu (`frontend/src/pages.jsx`); ≤ 0,01 USD (Phase 10). Report `report_agent/2026-11-05_phase_10_anh/e_bat_anh_implementation.md`. **XONG 09:51 08/11/2026 — chờ review:** nhánh `p10-anh-bat` `ce89e42` (đã push; 3 file giao diện: cuộn đáy khi thẻ ảnh hiện — trước sửa thẻ đè cuối câu trả lời ở 1440 + 390; câu Giới thiệu khi cờ bật). Test 59 passed; cờ tắt 0 USD đạt; 0 CSP / console. Tiền thật **0,008346 USD** (Phase 10 ⇒ ≈ 0,107 / 0,15). Worktree đã gỡ. Ngoài phạm vi: dòng "Nguồn" lặp cùng tên bài (8 lần) — báo A.
- 09:56 08/11/2026 — A giao: việc nhỏ Nhóm 1 + 2 (User duyệt 08/11) — (2) ô chat maxLength 500 + đếm; (5) gợi ý cách hỏi dưới câu từ chối; (7) nút Dừng + backend huỷ gọi model; (12) lỗi stream khác cũng huỷ gọi model; (9) khẩn cấp số `tel:` + ẩn 👍/👎; (+) dòng Nguồn gộp theo bài. **XONG 10:28 08/11/2026 — chờ review:** nhánh `p11-viec-nho-e` `45b3710` (đã push; (9) GÁC theo A — đã gỡ khỏi nhánh). Thêm: sửa đường song song mất USD trong `chat_metrics` khi người dùng ngắt (tái tạo trước). Test 520 passed + 1 hỏng sẵn trên `main` (B sửa ở `p11-ban-do`); Q1 giống byte. Tiền ≈ 0,0055 USD. Report `report_agent/2026-11-06_giao_dien_cong/e_viec_nho_implementation.md`. Worktree đã gỡ. Worktree `/tmp/e_viec_nho`, nhánh `p11-viec-nho-e` từ `main` `c9931be`. **File sẽ sửa:** `frontend/src/chat.jsx`, `frontend/src/stream.js`, `frontend/src/index.css`, `backend/llm/assistant.py`, `backend/api/routes/chat.py` (nếu cần), test liên quan; report `report_agent/2026-11-06_giao_dien_cong/e_viec_nho_implementation.md`. ≤ 0,01 USD.
- 10:28 08/11/2026 — A giao (giữa việc nhỏ): rebase `p10-anh-bat` ⇒ **`9800eeb`** (push, 60 passed) · review `p11-ban-do` `d0adf31` ⇒ **ready** (`report_agent/2026-11-06_giao_dien_cong/e_ban_do_review.md`; cờ tắt: Q1 byte, CSP byte, 0 host lạ; 432 tổ hợp 0 sai; 0,00038 USD).
- 10:37 08/11/2026 — A giao: review `p11-lich-nho` `a43cd14` (B) ⇒ **ready** (`report_agent/2026-11-06_giao_dien_cong/e_lich_nho_review.md`; 864 tổ hợp: 48 khác đúng dạng; link 28 / 28; Q1 byte; sao chép / tải 0 request, 0 HTML thô; ghim khớp; m-1 link toạ độ mất thẻ địa điểm — A / User chọn; m-2 toạ độ Kinh thành nghi lệch). 0,001028 USD. Worktree đã gỡ.
- 10:48 08/11/2026 — review B `p11-viec-nho-e` ready 2 minor ⇒ m-2 sửa (`607902a`, rebase `b50d9c0`, push); m-1 sửa report. **Bẫy E tự gây:** gọi lần gọi 56 / 89 token là "lần bị dừng" — thật là lần đã xong; SDK `cancel()` mặc định không trả usage ⇒ token lần bị huỷ không đo được. Từ nay: khẳng định "lần X" phải khớp loại / thứ tự lần gọi, không suy từ vị trí cuối danh sách.
- 10:56 08/11/2026 — A giao: review `p11-viec-nho-c` `2c2c1bf` (C) ⇒ **ready sau rebase** (`report_agent/2026-11-06_giao_dien_cong/e_viec_nho_c_review.md`; m-1 luật số so theo chữ số; m-2 máy chính thiếu `rieng/lv_festivals_nho.jpg` ⇒ chạy `anh_nho.py` trước build; m-3 xung đột `App.jsx` / `pages.jsx`). 0,0004 USD. Việc kế: đọc trước công cụ ngày + âm lịch (chưa cài gì).
- 11:02 08/11/2026 — A giao (User duyệt spec bản 13 `5557f0fd7650`): **T1 ngày + âm lịch** — plan trước. **File sẽ ghi:** `docs/superpowers/plans/2026-11-08-phase-9-t1-ngay-plan.md` (mới); sau khi A duyệt plan: nhánh `p9-t1-ngay`, worktree `/tmp/e_t1`. Tra cứu thư viện âm lịch xong: `data/tra_cuu_cli/2026-11-08_e-am-lich-python/` (E WebFetch kiểm 4 nguồn).
- 11:23 08/11/2026 — **T1 đang làm.** Plan bản 2 `cdf2c061381a` (mức nhẹ, sửa review vòng 1) **chờ A duyệt** ⇒ lượt có phí. Nhánh `p9-t1-ngay` `0357d80` (chưa push): `ngay_lich.py` + công cụ + cờ `ngay_lich: false` + 38 test passed; Q1 cờ tắt 228 / 228 giống byte. `lunar-vn==1.4.0` A duyệt 11:06, E đọc hết mã wheel, hash = lock, cài `--inexact` (sherpa còn). Đối chiếu: khớp bảng Hồ Ngọc Đức 1966–2099 ⇒ chỉ nhận 1976–2100. Harness `data/phase_9/t1/tools/chay_t1.py` (server thật; bộ ngày 27 · an toàn 4 · Golden 2 · pilot 5), `kiem_l2.py` (tự thử: bắt 3 / 3 sai, 0 nhầm), `dem_bo_do.py`, `so_tet.py`; bộ âm lịch mới `bo_am_lich.jsonl` `30f16e5a329d`. **Kế tiếp:** A duyệt ⇒ server `main` (cờ tắt) + server nhánh (cờ bật, sửa tạm settings worktree) ⇒ pilot 5 ⇒ lượt đo ⇒ sub-agent chấm L1 / L3 + S4 ⇒ report `report_agent/2026-11-02_phase_9_code/e_t1_ngay_implementation.md`. **Bẫy:** `uv sync` thường ở `main` gỡ `lunar-vn` + `sherpa-onnx` — chỉ `--inexact`.
- 11:45 08/11/2026 — **T1 đo xong (PARTIAL)**, report `report_agent/2026-11-02_phase_9_code/e_t1_ngay_implementation.md`, nhánh `p9-t1-ngay` `2c6cd46` (push). 2 người chấm mù khớp 29 / 29: từ chối nhầm −8 (đạt); L1 / L3 mới 0; **L2 1 câu (A2: "Chưa … đã qua")** ⇒ tiêu chí 3 trượt; `max_turns` 4 + 1 khi có công cụ (A chọn) ⇒ R8 hết chạm trần nhưng vẫn từ chối; S1 16 / 16; S4 sát. Tiền ≤ 0,076 USD. **Chờ A quyết** (a) merge cờ tắt / (b) code ghi "đã qua / còn N ngày" + đo lại bộ ngày ≈ 0,03 / (c) phương án B. **S5 NOT RUN** — A xếp lượt B ⇒ E ⇒ C; lệnh: cờ bật tạm trong `/tmp/e_t1/backend/config/settings.yaml` ⇒ `cd /tmp/e_t1/backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port 8862` ⇒ `.venv/bin/python data/phase_9/t1/tools/chay_t1.py http://127.0.0.1:8862 chon:<20 mã câu ngày> nhanh 3 <out>` ⇒ tắt ⇒ server `main` 8861 cùng lệnh `moc` ⇒ `chat_metrics.first_text_ms` theo `turn_id`. Worktree `/tmp/e_t1` giữ (cờ đã trả về tắt).
- 12:00 08/11/2026 — T1 lượt 2 (sửa (b), `f536dfe` push): 2 người chấm mới khớp 27 / 27 — R→OK **9** (A2 hết lỗi), L1 / L3 0, **L2 1 (R7: model tự viết "tuần này giữa tháng 9 âm")**, max_turns 0, kém đi R8 + E2. Tiền T1 ≤ 0,094 USD. Report mục 4b. **Chờ A quyết:** merge cờ tắt / (i) công cụ trả ngày âm của tuần này. S5 chưa chạy (lệnh ở dòng trên).
- 12:09 08/11/2026 — **T1 lượt 3** (sửa (i), `9f08d91` push): 2 người chấm khớp 27 / 27 — **tiêu chí 1–4 đạt** (R→OK 8, L1 / L3 0, L2 0, max_turns 0); kém đi R8 (ổn định 3 lượt) + E3 (dao động). Tiền T1 ≤ 0,112 / 0,13. Report mục 4c. **Chờ A:** merge cờ tắt + review cả nhánh (phiên sau); S5 chưa chạy (lệnh ở trên). Worktree `/tmp/e_t1` giữ, sạch.
- 12:14 08/11/2026 — A giao: sửa test `test_weather_and_feature_routes` (hỏng khi có `--env-file` vì `anh.bat` bật) ⇒ nhánh `p9-sua-test-cong` `35c93ec` (push): test đặt rõ `app.state.anh = None` + trả lại. Tái tạo trên `main` trước: có env 1 failed / không env passed ⇒ sau sửa `test_cong_dot_1.py` 22 / 22 cả hai. Chờ A merge. Worktree đã gỡ.

## 0. Đã làm 07/11 (A giao; A commit phần tracked) — tiền E 07/11: **0,000953 USD**

| Giờ xong | Việc | Kết quả | File |
|---|---|---|---|
| 11:59 | Script kiểm v5 ↔ v6 theo ô tick | 8 ca giả: 2 đúng OK, 6 sai đều bắt. Lệnh (từ `backend/`): `PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python ../data/phase_9/lich_trinh/tools/kiem_v6.py <phiếu> <diem_v6.json>`; lúc chốt bỏ chữ "ĐỀ XUẤT, chờ User" ở căn cứ Đại Nội nếu User chọn A | `data/phase_9/lich_trinh/tools/kiem_v6.py` |
| 12:30 | Ảnh Commons bộ 1 (27) | **User bắt 2 nhãn sai** ⇒ thay bằng bộ vi.wiki | `data/nghien_cuu_giao_dien_2026-11-06/anh/commons/` |
| 12:32 | Tự soi over-engineering | đóng hẳn câu tự do tới sau bảo vệ; gỡ cờ âm; giọng nói đề xuất cắt; deploy sớm; rủi ro bỏ quên (giới hạn lượt, quyển báo cáo + slide, dự phòng demo) | `report_agent/2026-11-07_tu_soi_lo_trinh/tu_soi_E.md` |
| 12:38 | E-dep chuẩn bị deploy | RSS app 1,49 → 1,51 GB, Qdrant 378 MiB ⇒ máy 4 GB; Lightsail 4 GB 24 USD / tháng; checklist 9 mục. Nháp Docker B nhận và sửa tiếp | `report_agent/2026-11-07_tu_soi_lo_trinh/e_dep_chuan_bi_deploy.md`; `data/phase_12/deploy_nhap/` |
| 12:56 | S4 review cổng đợt 1 | backend `0cb0b0a` ready (Q1 228 / 228 E tự chạy; API bài kho chặn 20 kiểu id lạ; m-5 bớt ngày 3 / 120); giao diện `f20fd28` ready (m-f1 link `//`, m-f2 `<title>` — B sửa `27ed091`) | `report_agent/2026-11-06_giao_dien_cong/s4_review_{backend,frontend}.md` |
| 12:58 | Bảng bằng chứng đồ án | theo khâu, nhãn ai đo, lỗ hổng trước bảo vệ (A kiểm 3 số khớp) | `report_agent/2026-11-07_tu_soi_lo_trinh/e_tb_bang_bang_chung.md` |
| 13:00 | Nháp demo 5 phút | 7 bước + dự phòng; câu mẫu **chưa chạy thử** | `…/e_demo_5_phut.md` |
| 13:06 → 13:26 | Review B-dep (biến môi trường + Docker) | vòng 1 changes_requested (M-1 ảnh chứa 16 file `*/evaluation/` + sao lưu Golden) ⇒ vòng 2 **ready** (E đếm riêng ảnh `nhap2`); m-6 cache uv 1,9 GB | `…/e_review_b_dep.md` |
| 13:22, 15:28 | Báo cáo User sau merge cổng + bật biểu mẫu | LUONG bản 31 → 32, SINH bản 40 → 41, README; **A sửa 1 câu sai của E** (dòng dự báo) | `bao_cao_he_thong/` (A commit `7cad6ac`, `bdde1d9`) |
| 16:14 → 16:22 | Ảnh theo bài vi.wikipedia | 30 ảnh (#1–#7 đợt 1 + 23 thẻ), 30 / 30 URL Commons, E mở từng ảnh đối chiếu chú thích (30 «có»); Nhã nhạc: bài không có ảnh ⇒ ảnh «Đội nhạc cung đình Huế» bài Festival Huế; ⚠ Đại Nội / Kinh thành = Ngọ Môn (trùng đầu trang), thẻ Phá Tam Giang trùng ô du lịch, Lăng Tự Đức bưu thiếp cũ. Theo User: #1 = cầu Trường Tiền (226 KB); #2 Ngọ Môn cắt 16:7, 249 KB | `data/nghien_cuu_giao_dien_2026-11-06/anh/viwiki/` (`muc_7.json`, `muc_the.json`, `ung_vien_*.json`, `tai_ve*.json`) |

## 1. Đã xong phiên tối 06/11 (lịch sử) (mọi việc A giao; A commit)

| Việc | Kết quả | File |
|---|---|---|
| Bộ kín B5 v2 — User duyệt độ tự nhiên | 3 vòng bàn thẳng với User ở terminal E (A cho): K1 đạt vòng 1; K4, K5 vòng 2; K2, K3 vòng 3 (E viết lại theo ý User: ngắn, một nhu cầu thật, không cài ý thử tính năng). Khoá md5 **`de95ff85e491`**; bản bỏ `cd552f7cf7cb` ⇒ `cau_sealed_v1_bo.jsonl` | `data/phase_9/b5_v2/duyet_tu_nhien_user.md` |
| Chạy + chấm kín v2 | n 5 · lỗi 0 · 0,003029 USD. 2 sub-agent khớp 15 / 15 ⇒ **Q3 không đạt 3 / 5** (i 4/5 · ii 3/5 · iii 4/5). K2 hỏi lại thừa (model gửi số ngày khác số code dò); K3 "đi dày" không dày; K4 / K5 đạt nhờ lời do code dựng khi model từ chối ⇒ `lich_trinh` giữ tắt. User chọn "biểu mẫu trước" | `report_agent/2026-11-06_b5_cau_tu_nhien/e19_kin_v2.md`; phiếu `data/phase_9/b5_v2/cham_agent_{1,2}.md` |
| E20 — từ chối khi hỏi kèm | 10 câu tự viết (cặp có / không hỏi kèm), ghi trước. Từ chối 3 / 4 ↔ 0 / 4; cả 3 lượt từ chối đều gọi `tim_kho` sau lịch và bị chặn (`TOOL_DA_DU_LICH`). 0,008092 USD. A: Sửa 1 / Sửa 2 chỉ làm khi xét bật đường câu gõ tự do | `report_agent/2026-11-06_b5_cau_tu_nhien/e20_tu_choi_hoi_kem.md`; `data/phase_9/b5_v2/e20/` (bộ `d79ffecd2c0b`, công cụ `tools/chay_e20.py` ghi thêm câu tìm + tham số số ngày) |
| E21 — cột thời lượng | v6 nháp từ v5 (đổi 2 điểm). Kho có thời lượng 7 / 33 ⇒ chạy `xep` thật: **đi dày = thong thả** ⇒ cột từ kho không sửa được K3 | `data/phase_9/lich_trinh/diem_v6_thoi_luong_nhap.json` (sha256 `58453c1fa560`) + phiếu v6 |
| Plan G2 giọng nói | sửa theo review vòng 1 + 3 minor vòng 2; **A duyệt**. Bản chạy: plan `92ec551531fd`; công cụ `chuan_hoa` `190a9d4dfde3` · `doi_wav` `7986adebde78` · `g2_do` `a3a32eba4f94` | `data/phase_10/giong_noi/plan_g2.md`, `plan_g2_review.md` |
| Review harness sửa lịch của C | vòng 1 changes_requested (1 major: Q4 đạt rỗng) ⇒ vòng 2 ready ⇒ vòng 3 (rebase C208 `79b3d9c`) ready, 0 finding mới | `report_agent/2026-11-02_phase_9_code/c207_harness_review.md` |
| Review spec giao diện cổng đợt 1 | vòng 1 changes_requested (1 major: Q-F chưa đo được) ⇒ vòng 2 ready. A sửa n-1 ⇒ sha `ff3c317ec88b`, chờ User duyệt | `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design_review.md` |

## 2. Lệnh / công cụ dùng lại

- Chạy một bộ câu đơn qua lõi thật, cờ `lich_trinh` bật trong tiến trình (từ `backend/`):
  ```bash
  PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run python ../data/phase_9/b5/tools/chay_b5.py kiem <bo.jsonl>                    # 0 USD
  PYTHONPATH=$PWD HF_HUB_OFFLINE=1 OPENAI_API_KEY=sk-fake OPENAI_BASE_URL=http://127.0.0.1:9 uv run python … chay <bo> /tmp/x.jsonl   # chạy thử 0 USD
  PYTHONPATH=$PWD HF_HUB_OFFLINE=1 timeout 900 uv run --env-file /home/minhhieu/hue_rag/.env python … chay <bo> <out>   # CÓ PHÍ — auto mode chặn ⇒ User `!`
  ```
- Muốn biết model gửi tham số gì / tìm câu gì: dùng `data/phase_9/b5_v2/e20/tools/chay_e20.py` (cùng khuôn lệnh).
- Chấm bằng 2 sub-agent: brief ghi file `/tmp` (đề chấm nguyên văn + câu + đường dẫn dữ liệu + "không xem phiếu kia"), dùng `general-purpose` ngữ cảnh mới (không `fork`), mỗi agent ghi một file `cham_agent_<N>.md`.

## 3. Bẫy / đã học

### 08/11

- **Gọi sai lần gọi model trong log (E tự gây, B bắt):** E ghi "lần bị dừng ra 89 token" — đó là lần **đã xong**; SDK `cancel()` mặc định không trả usage ⇒ token lần bị huỷ không đo được.
  - Từ nay khẳng định "lần X" phải khớp loại / thứ tự lần gọi, không suy từ vị trí cuối danh sách.
- **Chạy 2 server một lúc** khi A vừa ra luật "1 server / session" (RAM) ⇒ phải dừng, bỏ 3 câu đã chạy (≈ 0,003 USD).
  - Từ nay chạy mốc ⇒ tắt ⇒ chạy nhánh.
  - Đếm `chat_metrics` theo `turn_id`: log thư mục chính dùng chung, mốc dòng lẫn dòng session khác.
- **Ghép commit + push một lệnh** ⇒ auto mode chặn ⇒ tách 2 lệnh.
- **Sửa chuỗi bằng `str.replace` khi đoạn xuất hiện 2 lần trong file** (assert `count == 1` trượt) ⇒ tìm đúng vị trí trong hàm đích (`index(a, start)`).
- **Bộ kiểm L2 bằng regex chỉ bắt sai ngày / thứ**, không bắt sai lập luận trước / sau ("Chưa … đã qua") hay mô tả "tuần này giữa tháng 9 âm" — người chấm bắt.
  - Cách sửa đúng là **code tính luôn** (khoảng cách tới hôm nay, đầu / cuối tuần), không viết thêm regex.
- **Định nghĩa nhãn cũ (L1 bộ 30/10) sai khi hệ thống biết ngày** ⇒ chỉnh định nghĩa trong brief **trước** khi xem câu trả lời, ghi giờ.
- **`python -I` bỏ qua `PYTHONPATH`** ⇒ script import `backend/` không chạy `-I`; `-I` chỉ cho script đọc file tải về.
- **Thư viện ngoài:** đọc đúng file sẽ cài (wheel từ PyPI + hash), không đọc bản trên GitHub.

- **07/11 — nhãn ảnh không đối chiếu mô tả (User bắt 2 lỗi trong 27 ảnh Commons):** ô ẩm thực đặt nhãn "Bún bò Huế" theo **tên danh mục** Commons, ảnh thật là bún riêu; ô di tích ghi "Điện Thái Hòa" trong khi mô tả Commons ghi rõ là Đại Cung môn. E có mở ảnh nhưng chỉ soát "đúng nơi / có người", không so ảnh với **mô tả của chính file** + nhãn mình đặt. Ảnh "chắc: vừa" vẫn đưa vào danh sách chính. ⇒ Từ nay: nhãn = đúng chủ thể trong mô tả / chú thích bài (copy nguyên), mở ảnh đối chiếu từng cái, ghi "khớp chú thích: có / không"; ảnh không chắc ⇒ để mục riêng, không vào danh sách dùng.
- **07/11 — câu về hành vi lấy từ ghi chú, không từ số đếm:** E viết "thời tiết bật ⇒ lịch biểu mẫu có dòng dự báo" theo ghi chú điều kiện trong report C; S3 đếm 0 / 24 (biểu mẫu chưa có ô ngày đi). A sửa.

### Phiên tối 06/11

- **Auto mode chặn agent ghi file `*sealed*`** (đọc thì được) ⇒ viết script `/tmp` dựng file, User chạy `!`. Xong thì xoá script `/tmp`.
- **Câu kín agent viết hay "cố tự nhiên"**: cài ý để thử tính năng (giờ ra ga, tiền vé), câu dài, chi tiết lạ. User bắt 2 vòng. Cách đạt: mỗi câu **một nhu cầu thật**, có chủ ngữ, ngắn vừa đủ.
- User đổi ý giữa chừng ("bạn tự làm đi, sao lại là tôi làm") khi E đề xuất User tự gõ câu ⇒ với việc soạn nội dung, mặc định E làm, User duyệt.
- **Lượt `!` dài hơn 120 s** bị chuyển nền ⇒ đọc file output khi có thông báo; `| tail -1` giữ đầu ra tới khi xong.
- **Gõ giờ tay khi viết review** ⇒ hook bắt (22:41 ≠ `date` 22:39) ⇒ luôn chạy `date` ngay trước khi ghi, dán đúng chuỗi.
- Harness B5 cũ (`chay_b5.py`) không lưu tham số công cụ ⇒ không biết model gửi số ngày nào ở K2. Bản E20 đã ghi thêm.
- Trước: `.venv` chung có `sherpa-onnx` nhưng `uv.lock` của `main` chưa có ⇒ **không `uv sync` ở `main`** (cài lại: từ worktree `p10-giong-noi` chạy `UV_PROJECT_ENVIRONMENT=/home/minhhieu/hue_rag/.venv uv sync --inexact --frozen`).
- Codex tra web tiếng Việt: phải nêu nơi tìm cụ thể (VOZ…, "mở trang 1 của chủ đề").

## 4. Giọng nói — khi User thu xong 40 câu (G1 ⇒ G2)

1. Kiểm `thu/nguoi_doc.md` (mã người đọc, vùng giọng, "đã đồng ý", không tên thật).
2. `uv run python -I data/phase_10/giong_noi/tools/doi_wav.py`. Thiếu câu / trùng / > 10 s ⇒ báo A **trước** G2.
3. Xoá file gốc `thu/<MA>/`; `rm` bị chặn ⇒ User `!`.
4. Đo theo plan `92ec551531fd` §3–§6: kiểm RAM ≥ 5 GB; mỗi cấu hình một lệnh `timeout 600`.
5. Report `report_agent/2026-11-05_phase_10_anh/e<số>_g2_giong_noi.md` ⇒ A.

- Worktree khi cần code G3: `git worktree add /tmp/e_giong p10-giong-noi` (nhánh `93bbc63`).

## Tiền

- **E 08/11 ≈ 0,128 USD (cận trên):**
  - T1 ≤ 0,112 (nhánh 0,061 + mốc ≤ 0,051, log mốc lẫn session khác);
  - bật ảnh 0,0083;
  - việc nhỏ ≈ 0,0055;
  - review lịch nhỏ 0,0010 / bản đồ 0,0004 / việc nhỏ C 0,0004.
  - Codex tra cứu, sub-agent chấm = quota, 0 USD.
  - Phase 9 (T1 + việc nhỏ + review) + Phase 10 (ảnh 0,0083 ⇒ ≈ 0,107 / 0,15).

- **E 07/11: 0,000953 USD** (3 câu đo RAM ở E-dep; ảnh Commons / vi.wiki, Codex tra AWS, review, ca dò: 0).
- **E phiên tối 06/11: 0,011121 USD** (kín v2 0,003029 + E20 0,008092; đều Phase 9). Chấm agent = quota Claude. Codex / Playwright / giọng nói: 0.
- E phiên sáng 06/11: 0 USD. Phase 10 tổng vẫn 0,098380 / 0,15.

## Câu hỏi cho A (treo)

- 08/11: T1 bật cờ khi nào (sau review nhánh + S5)? Câu R8 (kém ổn định) cần dữ liệu lịch sự kiện theo ngày (đợt 2 cổng) — ghi vào backlog?

- ~~Ai chốt `diem_v6`~~ — **đã trả lời** (handoff bước 5 + A 07/11): User tick ⇒ **E chốt** `diem_v6.json`; A đổi `lich_trinh_bang` khi merge S1. Chưa tick ⇒ S1 dùng v3.
- Mục (e) trên: có cho dò K2 bằng `chay_e20.py` (≈ 0,002 USD) không, hay để B / C?
- `p10-giong-noi` (`93bbc63`) chưa merge ⇒ `uv.lock` của `main` chưa có `sherpa-onnx`. Bẫy `uv sync` còn tới khi merge (G3).
