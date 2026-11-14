# CURRENT_HANDOFF — việc đang mở của A/B/C/E

Cập nhật: 17:40 14/11/2026 (A, kết phiên 14/11). Trước: 09:45 14/11/2026 (A, mở phiên 14/11). Trước: 22:40 13/11/2026 (A, kết phiên 13/11).
Nguyên văn handoff trong phiên 13/11 (mọi quyết định theo giờ, bàn nhóm, vòng tự soi 1): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-13.md`; 12/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-12.md`. Nhật ký: `bao_cao_he_thong/nhat_ky/2026-11-13_lich_trinh_kho_3.md`.

## PHIÊN TỐI 14/11 (mở 17:45; A ghi 17:46 14/11/2026)

- Terminal: A `hue-rag-fb` · B `hue-rag-62` · C `hue-rag-eb` · E `hue-rag-1f` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).
- **Quyền (User chọn "như 14/11", A ghi 17:46 14/11/2026):** A tự điều phối, A commit / push, B / C / E push nhánh riêng, tự tra / cào / ghi kho / ingest, không hỏi khi User vắng; **tiền không trần cứng nhưng dùng hiệu quả** (Phase 9 ≈ 6,35 ước). Hết hạn cuối phiên.
- Giao: **B** mục 2 dưới (ghi kho 4: 8 quán + dòng nguồn giờ Đại Nội ⇒ dựng chỉ mục ⇒ đo W70) · **C** chờ B dựng xong ⇒ bảng quán lịch + đếm lại % bữa có quán kho ⇒ nhánh ⇒ E review · **E** sửa 2 lỗi ảnh C bắt ở review (ảnh "đồi Thiên An" thật là hồ Thủy Tiên ⇒ `chu_thich` hoặc đổi ảnh; 2 ảnh web lịch trang nguồn chỉ là trang chủ tên miền ⇒ tìm trang nguồn đúng), 0 USD, nhánh riêng ⇒ C review; rồi review nhánh bảng quán của C. Server 8010 không chạy (0 cổng 80xx) ⇒ B dựng chỉ mục không cần tắt gì; khi B dựng: không ai chạy lượt có phí / server / Qdrant.
- **User duyệt W73–W75 (17:48 14/11/2026)** ⇒ đã áp (worktree nhánh mới + `|| exit 1`; kiểm server đích trước lượt có phí + sàn tốc độ từ ≥ 5 lượt sạch; bài học thêm 1–2 số ⇒ tự đối chiếu; ảnh chụp sau nhánh cuối; nhánh chỉ test ⇒ merge thẳng). User sắp vắng ⇒ không mở hộp hỏi; để khi User về: đợt agent kế (bàn nhóm trước), lệnh dọn nhánh (`!`), 4 worktree AGY.
- **User (17:49 14/11/2026) đi vắng:** "tiếp tục điều phối, trao đổi với các Claude khác để cùng phát triển, triển khai, thử nghiệm, so sánh, tối ưu; thiếu thông tin tự dùng Codex tra web, tự cào, bổ sung; câu cần User gác lại tới khi User về (User sẽ nhắn)" ⇒ A không mở hộp hỏi. **Đợt agent kế (mục 5):** nhóm bàn + đếm lỗi trước khi xây (0 USD) + tra web / cào dữ liệu + plan nháp; ứng viên đa số nhóm đồng ý và không đổi hướng sản phẩm ⇒ được code trên nhánh **cờ tắt** + đo; **bật cờ cho người dùng = chờ User** (hướng sản phẩm). Ý chờ mục 4 (đếm lại mục web bị thay câu cố định) giao E.
- **User (17:50 14/11/2026) — ƯU TIÊN MỚI, trước đợt agent kế:** "để ý dữ liệu ảnh, dữ liệu khách sạn, đề xuất khách sạn; ảnh ở **mọi** địa điểm, món ăn, khách sạn, địa điểm du lịch, di tích… phải tìm **đầy đủ**; được đưa vào Qdrant hoặc tạo collection mới nếu muốn". **Đảo quyết định 14/11 chiều "khách sạn không cào điểm / ảnh"** ⇒ nay cào được (vẫn: không giá phòng trong câu trả lời — quyết định cũ không bị đảo). Chia: **E** ảnh Khám phá còn thiếu (216 − 184 = 32) + xem lại 38 ảnh "không chắc" + biển Thuận An (ảnh lịch 34 / 34) · **C** (sau bảng quán) ảnh mọi quán trong bảng quán lịch, kho trước · **B** (sau đo ghi kho 4) dữ liệu + ảnh khách sạn: bảng 140 cơ sở đủ khu / hạng / mô tả ngắn / ảnh / link, và xem lại cách đề xuất khách sạn trong lịch. Mỗi người: đếm độ phủ hiện tại trước (0 USD), ghi tiêu chí, nguồn ảnh như cách v3 (2 người chọn độc lập, "không chắc" ⇒ `kc`), giữ 0 chữ ghi công trên giao diện. Collection ảnh trong Qdrant chỉ làm khi cần cho tính năng (vd hỏi bằng ảnh) — bàn nhóm trước.
- **Chốt bàn nhóm "đợt agent kế" (17:51 14/11/2026; B, C, E — 3 / 3 cùng hướng):** ảnh + khách sạn (User) trước hết ⇒ **mưa làm bằng dữ liệu**: đếm trên 3.840 khung số buổi mưa mà cụm không có điểm trong nhà / cả hai (bảng 34 điểm: 5 trong nhà + 5 cả hai, 13 / 34 cột `trong_nha` là ước) — nhiều ⇒ thêm điểm trong nhà vào bảng (bảo tàng, nhà vườn, ca Huế…), không xây nút mưa riêng; lễ hội tách riêng, chưa thấy nhu cầu trong log · thẻ chọn chỗ theo ngày / buổi: **gác** (log 20 dòng `sua_lich`, gần hết là đo; thẻ 1, không áp 2) · nhãn xác minh, bản đồ đồng bộ: thấp · nhớ sở thích: **chờ User** (dữ liệu người dùng mới; đụng `nho_cau_tra_loi: false`). Câu cho User khi về: không cần — trừ nhớ sở thích.
- **Mục web bị thay câu cố định** (E đếm, `e_dem_web_thay_cau.md`, chưa review): 21 / 76 = 27,6 % (trước 43,4 %); 16 / 21 chặn nhầm — luật số ngoài đoạn trích chặn năm có sẵn trong câu hỏi ⇒ A sửa nhỏ (số có trong câu hỏi được qua; luật tiền giữ), nhánh `p9-web-so-cau-hoi`, người khác review.
- **Tiến độ (17:58 14/11/2026):** **ghi kho 4 XONG** (B; 224 file / 8.644 đoạn, record `944858b9972a`, sparse `f899fe3ddee0`, T1 `f6bc8d6e4676`; câu chạm 3 / 158 không tụt; ngoài kho 0 / 18, an toàn 32: 0 đổi lớp; 4 / 4 câu thử trích bài mới; ý con "Đầm Chuồn nên hỏi trước" A nhận là giới hạn; ≈ 0,030 USD; dòng nguồn Đại Nội sửa — mục nguồn không thành đoạn ⇒ 0 câu chạm) · cổng ổn định A trên kho mới (server 8790: `/` 200, `/health` 5 / 5, câu kho trích bài mới, câu ngoài kho từ chối, 2 dòng `chat_metrics`, 0 chữ câu hỏi trong log) · **bảng quán kho 4 merge** `1ebc8d3` (bữa có quán kho 49,3 ⇒ 69,1 %; nam xa vẫn 0) · nhánh A `p9-web-so-cau-hoi` `664d4ff` chờ C review (mục web bị thay 21 ⇒ 10 / 76) · E ảnh v4 đang chạy (78 bài) · B khách sạn (140 cơ sở: 0 mô tả / ảnh / link chính thức, 23 không toạ độ) · C thử ảnh 30 quán OSM. `/tmp/b_lkh` đã gỡ ⇒ lệnh dọn của User bỏ phần `worktree remove`.
- **Vòng tự soi 1 phiên tối — A chốt 18:08 14/11/2026** (B, C, E đều gửi): **GIỮ** — đếm "người dùng thấy gì, bao nhiêu lần" trước khi bổ sung dữ liệu cho lịch / giao diện, làm theo thứ tự lượt hiện (lộ quán đã đóng ở 324 lịch; 15 / ~420 quán OSM từng hiện; khách sạn abc 5 sao 0 / 6.108) · **người giao nhìn lại 100 % ảnh sẽ hiện** (bắt 5 ảnh mà cả hai agent con cùng chọn: múa lân không rõ làng, quán không biển tên, chai nước, biển có số điện thoại) · soát tay khớp tên Places (nhận nhầm nhà hàng, chi nhánh "2") · kiểm độc lập bài học (2 số sai) · review chéo nhánh nhỏ (nới quá rộng). **LÀM NHẸ** — ảnh chủ đề / `kc` (không hiện cạnh câu trả lời): 1 lượt agent con; ảnh sẽ hiện: **1 agent con + người giao nhìn lại 100 %** (2 lượt độc lập chỉ khi người giao không nhìn hết được) ⇒ **khách sạn: toạ độ 140 giữ (đã chạy, User "đầy đủ"); ảnh cả 140 bằng 1 lượt agent + B nhìn lại mọi ảnh nhận**, cơ sở từng hiện làm trước; câu thử "trước" khi bài chắc chắn chưa có trong kho ⇒ bỏ; tiêu chí không giữ sàn nào ⇒ không viết. **Bẫy:** `uv run` trong worktree tự tạo `.venv` mới ⇒ `--project /home/minhhieu/hue_rag`; chia việc gửi chéo nhau ⇒ một người đề xuất, người kia chỉ "đồng ý / sửa"; A gửi số trước khi đọc kết quả. **Đề xuất A cho vòng cải tiến (chưa áp, chờ User):** nhánh chỉ đổi một hàm thuần + test của nó ⇒ test file chạm thay test rộng 4 phút.
- **Mưa bằng dữ liệu — đếm xong, KHÔNG xây (18:20 14/11/2026; C, `c_dem_mua.md`, 0 USD):** luật xếp khi mưa + dòng "Nếu mưa" đã có. Mưa mọi ngày trên 3.840 khung: thay được 51,8 % · không thay được 33,3 % (81 % là ngày phá / đầm / Bạch Mã — không có điểm trong nhà thật) ⇒ thêm điểm trong nhà chỉ cứu ~3,6 % ⇒ không ghi kho. Đổi ngày bằng code (Open-Meteo dự báo lưu 12 tháng): 222 / 365 ngày ≥ 60 %; cứu ≤ 13,7 % mọi chuyến, mùa mưa 8–21 % ⇒ không xây. **Câu cho User (khi về, sau khi C đếm lượng mưa):** ngưỡng "mưa" 60 % chạm 222 / 365 ngày — có thêm điều kiện lượng mưa (mm) không? (đổi luật spec đã duyệt).
- Lệch: 4 worktree antigravity-cli (`~/.gemini/antigravity-cli/.../worktrees/subagent-Monuments-Reviewer-*`, `c725987`) trong `git worktree list` — của User dùng AGY trước đây; không ai đụng, A hỏi User khi dọn nhánh.

## PHIÊN SAU ĐỌC TRƯỚC (A viết 17:40 14/11/2026, KẾT PHIÊN 14/11 — User: "việc còn lại làm ở phiên sau")

**Phiên 14/11 đã kết** (mở 09:42; mở lại 2 lần trong ngày). Lần cuối: A `hue-rag-ad` · B `hue-rag-6b` · C `hue-rag-c1` · E `hue-rag-14`, cả bốn Claude Code (Opus 5.5), trực tiếp. **Quyền phiên HẾT HẠN** ⇒ A mới hỏi lại User một câu (14/11 có: A tự điều phối, A commit / push, B / C / E push nhánh riêng, tiền không trần cứng nhưng dùng hiệu quả, tự tra / cào / ghi kho / ingest, không hỏi khi User vắng). Mỗi session: đọc mục đầu `sessions/STATUS_<X>.md` "PHIÊN SAU ĐỌC TRƯỚC". D (học cùng User): chưa mở phiên nào hôm nay; mở khi User muốn hiểu một việc — gợi ý bài để giảng: `bai_hoc/25` (trợ lý làm việc thật), `bai_hoc/22` lần 3 (ghi kho theo câu chạm).
Nguyên văn handoff phiên 14/11 (mọi quyết định theo giờ, vòng tự soi 1, tiến độ từng lượt): `archive/CURRENT_HANDOFF_LICH_SU_2026-11-14.md`. Nhật ký: `bao_cao_he_thong/nhat_ky/2026-11-14_ghi_kho_3_bai.md`.

### Hệ thống lúc kết phiên (main đã push — xem `git log -1`)
- **Cờ BẬT mới 14/11:** `len_ke_hoach_v2` + `anh_lich` (sáng) · `sua_lich_v2` (sửa lịch bằng lời; bật lại sau nhánh tốc độ: câu thường có lịch chữ đầu p50 2,65 / p95 4,01 s, n = 20) · `cau_nhieu_y` (trả lời ý kho có, ý thiếu một dòng "Tư liệu chưa có thông tin về: …"; tách vế theo dấu + "và / còn / với" khi cả hai vế có từ hỏi; mục web chỉ viết cho vế thiếu: nêu lại ý kho 4/4 ⇒ 0/11; log `nhieu_y` / `chi_y_thieu`) · `luu_tru_lich` (khu ở cả chuyến + ≤ 5 cơ sở theo hạng + link tìm phòng do code; không giá; có buổi tối mà mọi điểm tối thuộc trung tâm ⇒ ở trung tâm — hệ quả 0/3.840 lịch phía tây, User nhận) · `quan_lich` (≤ 2 quán / bữa trong 2 km; bữa chính chỉ quán ăn, cà phê chỉ khi 2 km không có quán ăn; quán kho trước, OSM nhãn "từ bản đồ mở, chưa kiểm"; không giá / giờ / điện thoại; KHÔNG dòng © OSM — User chốt; tên quán không vào model vì `nho_cau_tra_loi: false` — bật nhớ câu trả lời thì phải xem lại).
- **Không cờ:** ảnh dưới câu trả lời (code quyết: một nơi / món, 1 bài nguồn, ảnh không `kc`, không từ chối / web / lịch) · lịch mẫu "Ví dụ" đủ đi – ăn – ở (`/api/lich_mau`, chỉ quán kho, không model) · so tiền mục web theo giá trị (43 ⇒ 51/76 mục hiện; số bịa vẫn chặn; "2 triệu rưỡi" = 2.500.000; "150K" là tiền, "10K bước" cũng bị coi là tiền — chặn thừa, an toàn).
- **Giao diện:** 0 chữ ghi công ảnh / dữ liệu trên giao diện (User 14/11; nguồn ở bảng dữ liệu); Giới thiệu: "Huế qua các thời kỳ" (6 mốc) + dải "Kho tư liệu" + sông dọc 3 bến có ví dụ thật; Lên kế hoạch: sông vẽ qua từng điểm, tên chặng, màu loại điểm, lịch ví dụ lên đầu ở màn hẹp + nút "Xếp lịch như ví dụ". E kiểm tổng 5 trang × 1440 / 390 ĐẠT (`data/ui_mau_2026-11-14/anh_chup/tong_1411/`). **User: "giao diện ổn rồi".**
- **Kho:** 216 file / 8.603 đoạn (record `82abd97169cd`, sparse `3404406926f2`, T1 `652da5944fe7`); 4 bài mới (cầu Trường Tiền, Ga Huế, chùa Từ Hiếu, nhà vườn An Hiên) + giờ Đại Nội theo mùa (chỉ bài Đại Nội; đêm viết nhẹ theo trang du lịch). Qdrant 1 collection 8.603 điểm.
- **Ảnh:** Khám phá 184/216 (38 `kc` — không hiện dưới câu trả lời); lịch 33/34 điểm (thiếu biển Thuận An; bảng `bang_anh_v2.json`).
- **Codex tra cứu:** mặc định `gpt-6.1-sol` mức medium (User chọn; tài khoản ChatGPT của User, không dùng khoá `.env`); đổi bằng `CODEX_MODEL` / `CODEX_EFFORT`.
- **Thử rồi bỏ / đếm rồi không làm:** suy luận "low" mục web (−0,87 s < sàn 1,5 s ⇒ nhánh `p9-web-suy-luan` hồ sơ) · đổi câu tìm web cho ý thiếu (6/16 chạm ngưỡng nhưng phải gửi chữ model ra ngoài ⇒ giữ nguyên; 3/16 mục có ích) · mở rộng lần tìm đầu (đụng quyết định 10 đoạn; cách đếm 0,02 USD ở `report_agent/2026-11-12_ra_khoang_cach/b_dem_toi_uu_tro_ly.md`).

### Việc đầu phiên sau — THEO THỨ TỰ
1. **A:** hỏi quyền phiên (một câu) ⇒ cùng lượt giao việc dưới. Trình User vòng cải tiến 30 (`SO_CAI_TIEN_CACH_LAM.md`, W73–W75) — mỗi lần một câu. Đưa User lệnh dọn nhánh (mục "User tự làm" dưới).
2. **B — 8 quán mới vào kho** (Thủy Xuân 3: Maison Trang 2, ECO Restaurant, Không Gian Xưa · Kim Long 2: Bánh O Lé, Bánh khoái Thu Sương · Đầm Chuồn 3 nhà chòi: An Phú, Hương Quán, Hội Quán; nguồn `data/tra_cuu_cli/2026-11-14_quan-thuy-xuan-dam-chuon/`, `…_quan-kim-long-thuan-an/`; đã loại: mọi quán Thuận An — báo 10/11 tin tốc mái sau triều cường, Lá Thông, Vạn Hạnh, Huế An): bài nháp ở `data/` (STATUS_B ghi đường dẫn) — **C review xong: ready sau 5 minor, B ĐÃ sửa cả 5** (nháp `data/quan_kho_them_2026-11-14/nhap/`; gói ghi kho sẵn `data/sua_kho_2026-11-14_ghi_kho_4/` — TIEU_CHI ghi trước, `ghi_kho.py`, `chay.sh` khoá `82abd97169cd` / 8.603, câu hỏi thử + mốc "trước"; **A xác nhận lại quyền ghi kho với User đầu phiên**) ⇒ ghi kho (sao lưu `meta/`) + **sửa luôn dòng nguồn giờ Đại Nội** (ghi "dẫn quy định Trung tâm BTDT" — trang Vinpearl không nói vậy) ⇒ dựng chỉ mục (báo cả nhóm, dừng lượt có phí / server) ⇒ đo W70 (T1 câu chạm + an toàn 32 + vài câu thử quán) ⇒ **C** dựng lại bảng quán lịch (`dung_quan_theo_cum` / `dung_bang`, chép `muc_toa_do`) + đếm lại % bữa có quán kho (trước 49,3 %; Thủy Xuân 33,6 %, Kim Long / biển / nam xa 0 %) ⇒ ảnh cho quán mới (cách v3). ≈ 0,05–0,15 USD.
3. **A sau mục 2:** `bai_hoc/22` hoặc `25` thêm lần ghi kho quán (agent con kiểm độc lập); sổ ghi việc khâu kho + lịch trình (chỉ Tóm tắt + checklist) — gồm cả các thay đổi 16:20–17:40 14/11 chưa vào sổ khâu (`07`, `02`): so tiền theo giá trị + "rưỡi", quán ăn trong lịch (`quan_lich` bật, bữa chính chỉ quán ăn, +7 quán kho), khu ở theo buổi tối, lịch mẫu đi – ăn – ở, ảnh lịch 33/34; nhật ký đã có 1 dòng.
4. **Ý chờ (đếm trước khi xây):** đếm lại tỉ lệ mục web bị thay câu cố định sau khi so tiền theo giá trị (trước ~45 %); tìm thêm là điểm nghẽn tốc độ (chữ đầu 5,2–7,9 s khi model tìm thêm ↔ 2,3 s) — chỉ mở khi User muốn tối ưu tốc độ; theo dõi cờ hết lượt tìm (đếm lại ~21/11, `data/ra_harness_2026-11-13/dem2.py`); chữ đầu mục web p50 ~9 s.
5. **Hướng sản phẩm (User 14/11):** trợ lý / agent, không chatbot thường. Đợt agent sau (đã liệt kê 14/11, chưa chọn): nút đề xuất mưa / lễ hội, bản đồ đồng bộ, nhãn "đã / chưa xác minh", nhớ sở thích có kiểm soát; ý E "chỉ chỗ theo ngày / buổi ⇒ thẻ chọn". Bàn nhóm ⇒ A trình User.

### Tiền 14/11 (ước từ tin báo của session, CHƯA cộng log — số chưa review)
Sáng + trưa ≈ 1,45 USD (ghi kho 2 lần 0,454 · câu nhiều ý ≈ 0,35 · sửa lịch ≈ 0,33 · ảnh Serper ≈ 0,16 · nghiệm thu lịch ≈ 0,09 · khác ≈ 0,05). Chiều ≈ 0,25 USD (B ≈ 0,06: suy luận low ≈ 0,046 + nơi ở / rà ≈ 0,005; tra quán = Codex gói ChatGPT · C ≈ 0,11 · E ≈ 0,07 · A ≈ 0,005). Cả ngày theo STATUS: E ≈ 0,57 · C ≈ 0,47 · B + A phần còn lại ⇒ **ngày ≈ 1,7 USD; Phase 9 ≈ 6,35 USD** (trần 6,0 đã vượt theo lời User "không lo tiền" — phiên sau A xin trần mới / xác nhận "không trần"). Codex tra cứu tính vào gói ChatGPT của User.

### Vòng tự soi 2 (kết phiên 14/11)
B, C, E đều gửi; A chốt (đủ ở `SO_CAI_TIEN_CACH_LAM.md` vòng 30). **GIỮ (bắt lỗi thật):** đếm trước khi xây (6 quán kho bị bỏ sót; 6 câu thử chọn đúng 4 bài; web ý thiếu ít giá trị ⇒ không xây) · mô phỏng 3.840 khung (quán 9 km ghi "gần") · Playwright lịch thật (bữa tối sai điểm) · người xem độc lập (Bạch Mã tính là biển; cà phê gắn "quán ăn") · người khác review luật code (giả định ngầm buổi tối; "2 triệu rưỡi" lọt) · đọc tay mục bị chặn / mới qua (so tiền chặn nhầm 37/37) · agent con kiểm bài học · mở lại nguồn khi review kho (giờ đêm Đại Nội) · kiểm tổng giao diện sau chuỗi merge (0,004 USD). **THỪA / LÀM NHẸ:** Golden 176 khi 0 câu chạm (đã thành W70) · chụp lại ảnh trình User nhiều lần trong một chuỗi nhánh ⇒ chỉ chụp sau nhánh cuối · Playwright 1 khổ cho thay đổi không theo cỡ màn · kiểm độc lập bài học khi chỉ thêm 1–2 số ⇒ chỉ đối chiếu số mới · review nhánh chỉ đổi test ⇒ A merge thẳng · ghi kho chỉ thêm bài ⇒ đo theo câu chạm (0,03 ↔ ~0,22 USD) làm mặc định. **Bẫy:** worktree ghép lệnh rơi xuống cây chung (A, C) · gửi lượt có phí nhầm server người khác (E) · sàn đặt từ số log có lượt đo chồng (B) · số đếm báo trước khi kiểm trường nguồn (C) · A báo "đã commit" trước khi đọc kết quả (3 lần).

### User tự làm (lệnh `!`, chạy khi tiện — xoá nhánh theo luật do User chạy; A đã liệt kê, chạy từ `/home/minhhieu/hue_rag`)
```
git tag hoso/p9-web-suy-luan p9-web-suy-luan && git push origin hoso/p9-web-suy-luan
git worktree prune
git branch -d p9-anh-kho3 p9-anh-kp p9-anh-lich p9-anh-lich-thieu p9-anh-tra-loi p9-anh-tu-hieu p9-anh-v3 p9-cau-nhieu-y p9-gd-anh-e p9-gd-anh-gt p9-gd-h1 p9-gd-h1-b p9-gt-song p9-len-ke-hoach-v2 p9-lich-mau-an-o p9-lich-mau-quan-kho p9-lich-truong-gd p9-lkh-nhan p9-luu-tru-lich p9-o-toi p9-quan-an-truoc p9-quan-kho-cum p9-quan-lich p9-so-y-va p9-sua-lich-tre p9-sua-lich-v2 p9-tien-ruoi p9-tien-web p9-web-y-thieu
git push origin --delete p9-anh-kho3 p9-anh-kp p9-anh-lich p9-anh-lich-thieu p9-anh-tra-loi p9-anh-tu-hieu p9-anh-v3 p9-cau-nhieu-y p9-gd-anh-e p9-gd-anh-gt p9-gd-h1 p9-gt-song p9-len-ke-hoach-v2 p9-lich-mau-an-o p9-lich-mau-quan-kho p9-lich-truong-gd p9-lkh-nhan p9-luu-tru-lich p9-o-toi p9-quan-an-truoc p9-quan-kho-cum p9-quan-lich p9-so-y-va p9-sua-lich-tre p9-sua-lich-v2 p9-tien-ruoi p9-tien-web p9-web-y-thieu
git branch -D p9-web-suy-luan && git push origin --delete p9-web-suy-luan
```
(`git branch -d` từ chối nhánh còn gắn worktree ⇒ session chủ gỡ worktree trước, hoặc `git worktree prune` sau khi `/tmp` mất. Thêm (B xác nhận nội dung đã ở main; gỡ `/tmp/b_lkh` trước): `git worktree remove /tmp/b_lkh && git branch -D p9-hue-thoi-ky p9-quan-kho-them && git push origin --delete p9-hue-thoi-ky`. Giữ: `p10-giong-noi`, `p9-b5c`, `p9-sua-lich`, `p9-toc-do-6` (hồ sơ cũ). Còn từ 13/11: gỡ dòng `EXA_API_KEY` trong `.env`.)

## Ý TƯỞNG TỪ NGHIÊN CỨU 04/11 — trạng thái (nguồn `bao_cao_he_thong/92_BAO_CAO_NGHIEN_CUU_PHASE_9.md` mục 000; hồ sơ `data/nghien_cuu_tinh_nang_2026-11-04/`)

| # | Ý | Trạng thái |
|---|---|---|
| 1–7, 12 | Kiểm giá "…000đ" / "triệu"; không đủ điểm ⇒ câu cố định; `khong_xep` + lý do từ mã luật; dòng giả định do code nối; test cố tình vi phạm; dòng "Mình hiểu…"; cột `ten_khac`; lời dặn không dùng địa danh thật làm ví dụ | vào B5 (`d66f6a3`) |
| 8 | Sửa lịch nhiều lượt (`sua_lich` hành động có tên, khung giữ ở server, Đã đổi / Giữ nguyên, ≤ 2 hành động / lượt) | code trên `p9-sua-lich` `79b3d9c` (rebase lên B5b + B171, giữ `hoi_toi` / lý do buổi tối — C208); harness đo E review ready; **hoãn** (cần cờ `lich_trinh` câu tự do) |
| 9 | Bộ chuỗi sửa lịch pass^k | bộ `data/phase_9/bo_do_sua_lich/` (10 + 5 kín; nhãn đã thấy S03 / S08 sửa theo B171 — C208); plan chọn pass^2; pilot = S01 + S06 (A đồng ý) |
| 10 | Cột trong nhà / bậc thang ⇒ phương án ngày mưa | **User đã trả lời phiếu gộp 12/11** ⇒ vào bảng đề xuất `data/phase_9/lich_trinh/diem_v8_de_xuat.json` + spec "Lên kế hoạch" bản 3.3 (phiếu v6 / v7 cũ không còn chờ) |
| 11 | `so_ngay` viết lạ ("3N2Đ", "cuối tuần") — theo dõi | C210 06/11: code không dò "3N2D" / "4n3d" / "2 hôm" / "cuối tuần" nhưng model tự gửi đúng số 5 / 5; biểu mẫu bỏ vấn đề này |
| 13, 14 | Ưu tiên theo lĩnh vực; đoạn gần trùng | đếm 0 USD xong — không mở thí nghiệm (C179) |
| 15–17 | Nhãn lỗi tự động; "0 lỗi trên n ca" + luật ba; dự phòng demo mất mạng | B7 |
| 18 | Router gắn cờ ⇒ code gọi `lich_trinh` | không cần (Q2a đạt) |

**Không làm** (đã cân): lọc cộng tác / rating, TSP, GraphRAG, định tuyến bằng danh sách từ, bảng SQL giá, rerank / sparse mới, nhớ cả câu trả lời, web bật sẵn, công cụ ghi ra ngoài không cần duyệt.


## Câu hỏi cho User (hỏi mỗi lần một câu — đáp án = đa số nhóm; cập nhật 17:40 14/11/2026)

**Đầu phiên sau:** (1) quyền phiên + trần tiền Phase 9 (≈ 6,3 / 6,0 — "không trần" như 14/11 hay trần mới) · (2) vòng cải tiến 30: W73–W75 (`SO_CAI_TIEN_CACH_LAM.md`) · (3) đợt agent kế tiếp (sau khi bàn nhóm): chọn trong nút đề xuất mưa / lễ hội · bản đồ đồng bộ · nhãn "đã / chưa xác minh" · nhớ sở thích có kiểm soát · thẻ chọn chỗ theo ngày / buổi.
**Đã trả lời 14/11 (không hỏi lại):** câu nhiều ý v2 bật · 132 ảnh web giữ trong repo, gỡ mọi chữ ghi công · giờ Đại Nội ghi cả hai theo mùa · màn "Huế qua các thời kỳ" làm · W70–W72 áp · ảnh dưới câu trả lời + gói dữ liệu đa số nhóm · Codex `gpt-6.1-sol` medium · ghi kho khi User vắng · không dòng © OSM · khu ở giữ luật buổi tối · dọn nhánh: tag + xoá · "giao diện ổn rồi".

**Cũ còn mở:** góp ý `bai_hoc/` (khi User đã đọc). (Q-DP, **khi tới deploy AWS** — không hỏi sớm): tra web trên bản công khai · ảnh #5 riêng (mặc định không lên) · số lượt / IP / ngày (mặc định 50) · khoá OpenAI riêng + tài khoản AWS + tên miền (HUE_SITE phải là tên miền https) · xoá ảnh docker cũ · dòng © OSM nếu bản công khai cần đúng giấy phép. **Không gấp:** vị trí Bảo tàng Cổ vật kho tự mâu thuẫn; lệch năm Tây Sơn đóng đô 1786 ↔ 1788 giữa 2 bài kho (màn thời kỳ chỉ nêu 1788); xoá sao lưu kho đợt 1 + 2; báo cáo tiến độ cho giáo viên; mốc quyển báo cáo + slide + kịch bản demo; nhãn cũ câu "hôm nay âm lịch" trong bộ 30/10.

## Câu hỏi A còn nợ (không cần User)

- **09/11:** T1 đã bật (xong lượt xác nhận + lượt sau G); giới hạn T1: "tháng tới / cuối tuần" còn do model tự tính (giới hạn). G: S1 đủ 3 số cần chạy lại an toàn có ngữ cảnh (harness đã sửa, `data/phase_9/g_cong/tools/do_g.py`). T3: lưu ý gắn điểm cũ khi đổi chủ đề (lỗi thiết kế, chưa sửa). Luật kiểm số mục web so theo dãy chữ số ("1:23" trùng "123"; "8/11" ≠ "08/11") — theo dõi `web_kiem`. Lần gọi model bị Dừng giữa chừng không có usage ⇒ USD log là cận dưới.
- **Checklist trước deploy (gom):** 4 chốt **đã có code** (`ccc9f4f`, bật bằng biến môi trường; đặt 3 biến trong `compose.yml`; uvicorn sau Caddy cần `--proxy-headers --forwarded-allow-ips <ip Caddy>`, không thì cả nước chung một sổ đếm; log xoay vòng giữa lượt đo ⇒ harness đếm hụt — hiếm) — `data/phase_12/deploy_nhap/ra_soat_no_A_2026-11-08.md`; hạn mức OpenAI / Serper; `tra_web` tắt trên AWS; allow-list `dung_dockerignore.py` thêm `data/phase_9/lich_trinh/diem_toa_do_v5.json` (khi bật bản đồ) + bảng T3 (nếu bật); **ảnh #5 riêng không lên bản công khai** (A mặc định — hỏi User lúc deploy); build cần `dong_anh.py` + `anh_nho.py` trước `npm run build` (thiếu ⇒ ô Lễ hội tự dùng ảnh Commons).
- **Cũ còn mở:** E20 Sửa 1 / Sửa 2 + C210 (khi xét bật lịch trình câu tự do — giờ là T4); giờ tới / về bị bỏ qua im lặng; quan sát "model gọi `thoi_tiet` 2 lần rồi từ chối"; "đi dày" ít tác dụng (bảng thiếu thời lượng — phiếu v7); `do_so_ngay` không dò "4n3d" / "2 hôm" / "cuối tuần"; `p9-sua-lich` phải tôn trọng `hoi_toi` + `chon_sang` khi merge; chữ đầu mục web p50 ~13 s; B5b "tuần sau" không có số dự báo; `_token_count` chênh ~900 token; ghi đệm OpenAI giữ như cũ; bảng sổ S41–S44 thiếu 1 cột; B7: dự phòng demo mất mạng + đề cương + ý #15–#17; theo dõi case Golden 67 từ chối ngẫu nhiên.

## Session

**Phiên 14/11 (mở 09:42, mở lại 14:44 + 14:55; kết 17:40 14/11/2026):** sáng A `hue-rag-7b` · B `hue-rag-22` · C `hue-rag-b4` · E `hue-rag-c4`; chiều A `hue-rag-ad` · B `hue-rag-6b` · C `hue-rag-c1` · E `hue-rag-14` — cả bốn Claude Code, trực tiếp.

**Phiên 13/11 (mở 19:46 13/11/2026):** A `hue-rag-43` · B `hue-rag-83` · C `hue-rag-eb` · E `hue-rag-e8` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn (2 collection, 8.435 điểm); `/tmp` mất sau khởi động lại máy (worktree B dựng lại).

**Phiên 12/11 (mở 18:40 12/11/2026):** A `hue-rag-7d` · B `hue-rag-1b` · C `hue-rag-e1` · E `hue-rag-33` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn (2 collection, 8.435 điểm); không worktree `/tmp`.

**Phiên chiều 11/11 (mở 13:39 11/11/2026):** A `hue-rag-2f` — chỉ A (B / C / E không mở; 8 terminal khác là dự án khác). Qdrant tắt. Việc: bàn `bai_hoc/` với User.

**Phiên 11/11 (mở 08:18 11/11/2026):** A `hue-rag-96` — chỉ A (B / C / E không mở). Qdrant tắt lúc mở.

**Phiên 10/11 (mở 19:02 10/11/2026):** A `hue-rag-55` · B `hue-rag-05` · C `hue-rag-4f` · E `hue-rag-e4` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn (2 collection, 8.435 điểm); không worktree `/tmp`.

**Phiên 09/11 (mở 20:09 09/11/2026):** A `hue-rag-87` · B `hue-rag-99` · C `hue-rag-6a` · E `hue-rag-ea` — cả bốn Claude Code, trực tiếp (B / C / E tự báo). Qdrant chạy sẵn lúc mở (2 collection, 8.435 điểm). Worktree `/tmp/b_g`, `/tmp/b_moc_g`, `/tmp/c_t3` mất (prunable) ⇒ dựng lại từ nhánh.

**Phiên 08/11 (mở 09:16 08/11/2026):** A `hue-rag-a8` · B `hue-rag-a1` · C `hue-rag-e9` · E `hue-rag-22` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

**Phiên 07/11 (mở 11:53 07/11/2026):** A `hue-rag-7a` · B `hue-rag-10` · C `hue-rag-a0` · E `hue-rag-81` — cả bốn Claude Code, trực tiếp (B / C / E tự báo).

Phiên tối 06/11: A `hue-rag-cc` · B `hue-rag-1a` · C `hue-rag-42` · E `hue-rag-28`.

Tên terminal đổi mỗi lần mở: `ListAgents`. B / C / E lúc mở phiên sau: kiểm nhanh ⇒ đọc `STATUS_<X>.md` + mục "PHIÊN SAU ĐỌC TRƯỚC" ⇒ báo A ⇒ chờ (việc A giao = User nói "làm đi").

## Quyền

- **Quyền phiên 14/11 HẾT HẠN (17:40 14/11/2026, kết phiên).** Phiên sau A hỏi lại.
**Trần tiền HIỆN HÀNH (đọc dòng này, các con số 4,0 / 4,2 / 4,3 / 4,6 bên dưới là lịch sử):** trần Phase 9 **6,0 USD** (User 13/11, giữ ở 14/11); đã dùng ≈ 4,66 (sửa 09:45 14/11/2026).

- **Quyền phiên 12/11 HẾT HẠN (22:23 12/11/2026, kết phiên).** Trần Phase 9 A ghi tạm 4,6 trong phiên (User "vẫn duyệt chi phí API"); Phase 9 ≈ 4,61 ⇒ phiên sau xin trần mới.
- **Phiên 12/11 (User chọn "như 10/11", A ghi nhận 18:45 12/11/2026):** A tự điều phối, giao ngay việc có sẵn trong handoff, A tự commit / push, B / C / E push nhánh riêng, trần Phase 9 4,2 (≈ 3,88 đã dùng), việc cần User duyệt thì gác. Hết hạn cuối phiên.
  **Thêm (19:01 12/11/2026) User đi nghỉ, trở lại ~20:30:** "cứ tiếp tục làm việc; vẫn duyệt chi phí API; **không hỏi khi User vắng**; làm tiếp không cần hỏi" ⇒ A không mở hộp hỏi tới khi User nhắn; câu cần User ghi "Câu hỏi cho User"; tiền ghi thật từ log, vượt trần 4,3 chỉ khi cần cho việc đã giao và báo lại.
- **Quyền phiên chiều 11/11 HẾT HẠN (16:24 11/11/2026, kết phiên).**
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
