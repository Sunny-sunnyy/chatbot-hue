# Báo cáo cho bạn: Sinh câu trả lời, API và giao diện (Phase 6, cải tiến ở Phase 8 và 9)

**Cập nhật lần cuối: 16:17 14/11/2026 — bản 51:** chiều 14/11: câu nhiều ý trả lời phần kho có; sửa lịch bằng lời bật lại sau bản sửa tốc độ; nơi ở gợi ý trong lịch; lịch mẫu "Ví dụ"; ảnh dưới câu trả lời; giao diện không còn chữ ghi công ảnh. **Bản 50 (14:05):** "Lên kế hoạch" bản 2 bật (code xếp theo chuỗi luật, ảnh, phút đi, `.ics`); **sửa lịch bằng lời bật** (hiểu ý chạy song song với phân loại, code áp); giao diện mới 5 trang. Bản 49: câu chỉ hỏi ngày tháng được trả lời.
Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (đúng hiện trạng 14/11/2026)

- **Mới 14/11 chiều — người dùng thấy:**
  - **Câu hỏi nhiều ý BẬT** (`cau_nhieu_y: true`, merge `f13d083`, bạn chọn bật). Trước: một ý kho không có ⇒ từ chối cả câu. Nay khi code đếm được ≥ 2 vế hỏi (`so_y`: tách theo dấu `, ; ?` và theo "và / còn / với" khi chính phần đó có từ hỏi — merge `6a9701d`), lời dặn đổi sang "trả lời ý có bằng chứng, ý thiếu ghi đúng một dòng `Tư liệu chưa có thông tin về: …`"; chỉ còn dòng ý thiếu ⇒ code đổi về câu từ chối chuẩn; dòng ý thiếu mở cổng web, và **mục web chỉ viết cho vế thiếu** (merge `5f9c9ae`; vế do code chọn từ chữ người dùng, Serper vẫn nhận cả câu).
    - Đo: hỏi kèm 10 câu 10 / 10 (cờ tắt 4 / 10); Golden 176 ngoài kho 1 / 18 ở câu 161 — đường không đổi, chuỗi gửi model giống byte ⇒ bạn nhận là nhiễu; an toàn 32 × 2 đạt. Câu nối bằng "và" (5 câu × 2): 10 / 10 luật chạy, 0 từ chối cả câu, ý ngoài kho 0 lần trả lời bằng kho. Mục web nêu lại ý kho **0 / 11** (trước 4 / 4). Tiền đo ≈ 0,37 USD (vòng 1 + vòng 2 + tách "và" + mục web). Log `chat_metrics` có `nhieu_y` / `chi_y_thieu` khi luật chạy.
    - **Giới hạn:** câu hai ý không dấu phẩy, không từ hỏi ở một vế, hoặc kiểu "A hay B" ⇒ đếm 1 ⇒ vẫn từ chối cả câu như cũ; "với" làm giới từ có thể bị đếm thừa (không tệ hơn). Mục web cho ý ngoài kho phần lớn là "chưa xác minh được". Report `c_cau_nhieu_y_do_v2.md`, `c_so_y_va_implementation.md`, `c_web_y_thieu_implementation.md`.
  - **Sửa lịch bằng lời BẬT LẠI** (merge `69e4397`): sau lần bật đầu, câu thường trong cuộc có lịch chờ lần hiểu ý ⇒ chữ đầu 4,17 s (vượt sàn 3 s) ⇒ tắt tạm; bản sửa chạy câu trả lời thường song song với lần hiểu ý (không phải câu sửa ⇒ không chờ) + khoá đệm cố định. Đo n = 20: câu thường có lịch p50 2,65 / p95 4,01 s ↔ không lịch 2,58 / 4,14 s; lượt sửa 2,30 / 2,59 s.
  - **Nơi ở gợi ý trong lịch BẬT** (`luu_tru_lich: true`, merge `fe55d2f`): lịch ≥ 2 ngày có thẻ "Nơi ở gợi ý" — **code** chọn một khu cho cả chuyến theo cụm điểm (trẻ em / lớn tuổi ⇒ trung tâm), ≤ 5 cơ sở trải theo hạng từ bảng 140 cơ sở, lý do + link tìm phòng Booking do code dựng; không giá phòng. Đo 3.840 khung mô phỏng: 3.072 / 3.072 lịch ≥ 2 ngày có thẻ, 0 cơ sở ngoài bảng; người xem 10 lịch 10 / 10. Report `b_luu_tru_lich_implementation.md`.
  - **Lịch mẫu "Ví dụ"** trên trang Lên kế hoạch khi chưa xếp (merge `f59b0c3`): `GET /api/lich_mau` dựng bằng chính bộ xếp (2 ngày · 2 người lớn · cân bằng · di tích), câu mỗi điểm do code, không gọi model.
  - **Ảnh dưới câu trả lời** (merge `4be483e`, chỉ giao diện): code hiện **một** ảnh khi mọi nguồn được trích thuộc đúng một bài về một nơi / món có ảnh "chắc" (38 ảnh gắn "không chắc" ⇒ không hiện); không ảnh khi từ chối, có mục web, có lịch.
  - **Giao diện:** bỏ mọi chữ ghi công ảnh (bạn yêu cầu; nguồn ảnh chỉ giữ ở bảng dữ liệu); Khám phá **184 / 216** bài có ảnh; Giới thiệu thêm dải "Kho tư liệu", màn "Huế qua các thời kỳ", ba bước thành ba bến trên dòng sông kèm ví dụ thật; Lên kế hoạch có dòng sông qua từng điểm + tên chặng.
  - **Kho lần ghi 3:** 216 bài / 8.603 đoạn (4 bài mới + giờ Đại Nội theo mùa) — `02_BAO_CAO_KHO_DU_LIEU.md`.

- **Mới 14/11 sáng — người dùng thấy:**
  - **"Lên kế hoạch" bản 2 BẬT** (`len_ke_hoach_v2: true`, A bật 11:00, bạn quyết D4 10:46). Biểu mẫu 4 nhóm; **code xếp** theo chuỗi luật (an toàn nhóm trẻ em / người lớn tuổi: không xếp buổi tối, ≤ 1 điểm / buổi ⇒ giờ mở cửa, ngày, mùa ⇒ ≤ 2 cụm kề / ngày ⇒ điểm ưu tiên ⇒ mưa (≥ 60 % trong 7 ngày) ⇒ sở thích ⇒ kiểu đi), quỹ phút (75 / 150 phút; đi 15 / 30 phút; buổi 210 / 240 phút), giờ gợi ý. Khung hiện ngay (`lich_khung`), model một lần gọi viết mỗi điểm một câu ≤ 30 từ (`lich_cau`); câu trượt `kiem_cau` ⇒ câu dự phòng của riêng điểm đó.
    - Nghiệm thu: bộ 20 lần đầu 16 / 20 (sàn 18) ⇒ gốc: bài kho mỏng ⇒ sửa **dữ liệu** (lần ghi kho 1 + cột đoạn mô tả 10 điểm) ⇒ 20 / 20; bộ để dành 12 tổ hợp × 2, hai người chấm mù: 10 / 12 ⇒ sửa 3 lỗi code (dòng "Nếu mưa" luôn có; sáng chồng chiều 52 / 3.840 ⇒ 0; chặn câu "tài liệu không có…") ⇒ 12 / 12 × 2. Đủ câu 4,56 s ↔ bản cũ 5,12 s. Report `report_agent/2026-11-12_ra_khoang_cach/b_len_ke_hoach_dot_1_implementation.md`.
    - Kèm: ảnh 24 / 34 điểm (`anh_lich: true`; chữ ghi công đã bỏ chiều 14/11); "khoảng N phút đi" giữa hai điểm liền nhau (= số bộ xếp dùng); nhãn "kiểm lịch diễn" chỉ cho điểm có suất (228 / 960 ⇒ 0); nút tải `.ics` dựng trong trình duyệt (44 lịch ⇒ 288 sự kiện, trình đọc độc lập 0 lỗi; cần ngày đi).
  - **Sửa lịch bằng lời BẬT** (`sua_lich_v2: true`, merge `e572330`, bật `e0cb02e`; tắt tạm vì tốc độ rồi bật lại chiều — mục trên). Cuộc có lịch đã lưu (RAM, 30 phút, chỉ dữ liệu code) ⇒ mỗi lượt có **một lần gọi hiểu ý** (`SuaLichOutput`: ≤ 3 hành động có tên, `extra="forbid"`) **chạy song song với phân loại**; phân loại ra khẩn cấp ⇒ khẩn cấp thắng, đi đường thường. Code khớp tên điểm (nguyên văn / tên khác / tên ngắn chỉ khi khớp đúng một điểm), áp ≤ 2 hành động bằng xếp lại giữ chỗ, kiểm `kiem_khung_v2`; khối "Đã đổi / Không đổi được / Chưa làm" do code viết; "thay" không nói điểm ⇒ thẻ chọn ≤ 3 (hành động khác của lượt vào "Chưa làm"). Đo: bộ đã thấy pass^2 9 / 10, bộ kín 4 / 5, an toàn 0 / 64, câu trộn sửa + khẩn cấp 0 / 16. Review E ready (B-1 khẩn cấp bị nuốt ⇒ sửa bằng chạy song song). Report `b_sua_lich_v2_implementation.md`, review `e_review_sua_lich_v2.md`.
  - **Giao diện mới "Sông Hương" 5 trang** (merge `55f48fe`) + **ảnh Khám phá 167 / 207 bài** (merge `ef8bc46`; chiều: 184 / 216): hiệu ứng CSS + ~30 dòng JS dưới `html.hieu-ung` (tắt khi máy giảm chuyển động), View Transitions, trang Trợ lý hiện bước công cụ thật; đo Playwright 1440 + 390: tương phản 0 trượt, CLS ≤ 0,05, giảm chuyển động 0 animation; JS 123,48 KB gzip. Report `e_giao_dien_h1_implementation.md`, `e_review_anh_kham_pha.md`.
  - **Bài lưu trú** vào kho (lần ghi kho 2): câu trả lời trích bài `travel/services/Lưu trú ở Huế — …` có dòng "thông tin có thể đã thay đổi" (`NOTICE_SOURCE_PREFIXES`).
- **Đo lại 14/11 — giới hạn đã nhận:** câu khẩn cấp đi trợ lý Huế từ chối 10 / 12, có số 112–115 0 / 12 (`report_agent/…/e_kiem_khan_cap_main.md`; bạn quyết 12/11 không làm dòng số khẩn cấp).


- **Mới 10/11 — người dùng thấy: câu chỉ hỏi về ngày tháng được trả lời dù không nhắc Huế** (bạn đồng ý 21:43 10/11/2026; review E đạt).
  - Câu như "hôm nay là ngày mấy âm lịch", "Tết năm sau là thứ mấy", "còn bao nhiêu ngày tới rằm" trước bị bước phân loại câu coi là "không liên quan Huế" và từ chối.
    Nay bước phân loại được dặn thêm hai câu: câu **chỉ hỏi về chính ngày tháng** thì chuyển cho trợ lý; câu hỏi **việc khác diễn ra vào ngày đó** mà không gắn Huế
    (giá vàng, tỷ giá, kết quả xổ số, thời tiết hay sự kiện nơi khác, lịch nghỉ) vẫn từ chối. Phép tính ngày vẫn do code; câu trả lời dặn như cũ.
  - Đo (chỉ lần phân loại, bản cũ và mới mỗi bản 2 lượt trên hơn 160 câu rủi ro + 176 câu Golden): 9 / 9 câu lịch từng bị từ chối nay đi trợ lý (bản cũ 0 / 9);
    0 câu khẩn cấp, 0 câu an toàn, 0 câu về Huế bị xếp sai thêm; 0 / 10 câu ngoài phạm vi có từ chỉ ngày lọt vào trợ lý. Bộ 25 câu do người khác viết, người sửa
    không đọc: 12 / 12 câu lịch đi trợ lý, 0 / 10 câu ngoài phạm vi lọt, 3 / 3 câu khẩn cấp đúng. Trả lời thật: **8 / 9** câu lịch đúng ngày (người chấm tự đổi lịch kiểm lại).
    Bản dặn đầu viết rộng quá, kéo nhầm 1 câu hỏi việc diễn ra vào một ngày lễ ⇒ thu hẹp ở bản thứ hai. Tiền đo ≈ 0,17 USD.
  - **Giới hạn:** câu thứ 9 có nội dung đúng lịch nhưng không ghi nguồn ⇒ bị luật kiểm nguồn rút lại (giao diện báo lỗi) — luật có từ trước; câu hỏi nghỉ lễ / Tết
    mấy ngày (lịch nghỉ chung) vẫn từ chối.
- **Mới 10/11 — người dùng thấy: câu hỏi về ngày trả lời nhanh hơn** (merge `1633c18`, bạn duyệt 20:47 10/11/2026; review C đạt).
  - Trước: với câu như "Tết năm nay vào ngày nào", trợ lý phải xin công cụ lịch rồi mới viết — 2–4 lần gọi model, chữ đầu chờ ~5–6 giây. Nay **code tự tính sẵn** hôm nay,
    ngày mai, các ngày trong tuần được hỏi, và đổi sẵn các ngày âm có trong câu hỏi hoặc trong tài liệu vừa tìm được (lần đã qua, lần sắp tới, và đúng năm âm khi câu nói
    "năm nay / năm sau"), đưa cho model **ngay lần đầu**. Công cụ lịch cũ chỉ còn dự phòng (dạng ngày ít gặp).
  - Đo 19 câu ngày (1 lượt, so bản trước cùng giờ; chữ đầu đo ở máy chủ — `first_text_ms`, chưa qua trình duyệt, thường nhanh hơn trình duyệt một chút): chữ đầu trung vị **5,60 ⇒ 2,35 s**, 95 % câu **10,14 ⇒ 4,56 s** (đạt sàn 3 / 5 s); tiền **0,00049 ⇒ 0,00036 USD / câu**
    (đạt ≤ 0,0005); số lần gọi model 52 ⇒ 31; model không gọi công cụ lịch lần nào. Số câu sai ngày **không tăng** (chấm mù + bộ kiểm bằng code); bộ an toàn 12 / 12 đạt;
    9 câu Golden có từ chỉ ngày 9 / 9 đạt; câu không nói về ngày: chuỗi gửi model giống hệt bản trước. Lần đo đầu có 1 câu "năm nay" bị model gọi nhầm lần năm sau ⇒
    sửa bằng code, đo lại đúng. Tiền đo ≈ 0,031 USD.
  - **Giới hạn:** dạng ít gặp ("ngày kia",
    "tháng tới"…) vẫn đi đường cũ. Hồ sơ `report_agent/2026-11-02_phase_9_code/e_t1_nhanh_implementation.md`.
- **Mới 09/11 — người dùng thấy:**
  - **Câu có ngày trả lời được — công cụ ngày + âm lịch BẬT** (merge `99ea59a`, cờ `ngay_lich: true` `7eb1f12`, bạn duyệt). Câu có từ chỉ ngày ("hôm nay", "tuần sau", "rằm", "Tết", "năm sau", "sang năm"…) ⇒ **code** tính hôm nay là ngày nào và đổi dương ↔ âm theo lịch Việt Nam (UTC+7, năm 1976–2100) — 09/11 qua một công cụ model gọi; **từ 10/11 code tính sẵn trước** (mục trên), công cụ chỉ còn dự phòng. Câu không nêu năm / nói "năm nay" với ngày âm ⇒ code đưa cả lần đã qua lẫn lần sắp tới, nhắc ghi rõ năm.
    - Đo (2 lượt, câu chưa dùng để chỉnh, chấm mù): 14 câu mới — **bớt 9 câu từ chối nhầm, 0 câu sai ngày / thứ**; sau khi sửa "năm nay" + "sang năm": 3 câu ngày có ngữ cảnh Huế nhánh đúng 3 / 3 ↔ bản cũ 1 / 3, 0 sai ngày, bộ an toàn 4 câu có ngày 0 lỗi. Tiền đo 0,045 USD.
    - Thử trên server thật sau khi bật (A): câu "rằm tháng Giêng" gọi công cụ, ra đúng thứ Bảy 20/02/2027; câu ngoài phạm vi vẫn từ chối.
    - **Giới hạn:** "tháng tới / cuối tuần" model tự cộng; "dịp lễ sắp tới" cần lịch sự kiện theo ngày (đợt 2 cổng).
  - **Câu khẩn cấp không còn câu soạn sẵn** (định tuyến phương án B, merge `3b52017`, review E đạt): giữ định tuyến 4 nhóm; câu bị xếp "khẩn cấp" đi trợ lý Huế như câu về Huế (bạn chấp nhận 08/11) ⇒ có thể nhận câu trả lời từ kho, câu "không đủ thông tin" kèm mục "Từ web (chưa kiểm)", hoặc câu cố định NCHMF / 112 nếu là thiên tai. Bản "2 nhóm" (G) dừng: 2 / 44 câu ngoài phạm vi đã thấy có mục web (bản cũ 0 / 44) — hồ sơ `hoso/p9-g-cong`.
  - **4 chốt trước deploy vào `main`** (merge `ccc9f4f`): `HUE_LUOT_MOI_NGAY=<n>` ⇒ mỗi IP tối đa n lượt / ngày (quá ⇒ 429 + câu tiếng Việt; không ghi IP); `HUE_COOKIE_SECURE=1` ⇒ cookie chỉ qua https; `HUE_TAT_DOCS=1` ⇒ tắt `/docs`; log xoay vòng 10 MB × 3. **Không đặt biến ⇒ như trước.**
  - Tốc độ chung sau các thay đổi hôm nay (một lượt đo trên `main`, B): một lượt trên trình duyệt thật, 65 câu, 0,0197 USD: câu về Huế tới chữ đầu p50 2,16 s / p95 4,32 s (đạt sàn 3 / 5 s), 0,00047 USD / câu (đạt ≤ 0,0005); câu ngoài phạm vi 1,62 / 2,97 s; **câu xã giao 3,46 / 7,73 s (p95 vượt sàn — đường cũ, không đổi hôm nay)**; câu có từ chỉ ngày lúc đó (5 câu) vượt sàn ⇒ **đã tối ưu 10/11** (2,35 / 4,56 s, 0,00036 USD — mục "Mới 10/11").
- **Thử 09/11 rồi KHÔNG áp dụng (đóng hồ sơ, người dùng không thấy):**
  - **Trợ lý tự yêu cầu tra web (T2):** câu hỏi kèm có phần web 4 / 10 = bản đang chạy 4 / 10 ⇒ không lợi. Lý do: 26 / 29 lần trợ lý yêu cầu web thì chính lượt đó nó từ chối cả câu (luật "thiếu bằng chứng ⇒ từ chối cả câu"), mà câu từ chối thì cổng web cũ đã mở sẵn. Tag `hoso/p9-t2-web`. 0,171 USD.
  - **Lịch trình từ câu gõ tự do (T4):** 27 / 27 câu xin lịch có lịch, 0 hỏi lại thừa, 0 từ chối thay cả lịch — nhưng **"lịch hợp người đi cùng" 21 / 27 và 15 / 27** (2 người chấm; cần ≥ 26) ⇒ âm; lịch trình vẫn chỉ qua biểu mẫu. Tag `hoso/p9-t4-lich`. 0,136 USD.
  - **Bảng vé + giờ có cấu trúc (T3):** đóng hồ sơ — lợi đo được ≈ 0 (tag `hoso/p9-t3-bang`).
- **Giới hạn của biểu mẫu "Lên kế hoạch" bản đầu (09/11 — ĐÃ THAY bằng bản 2 ngày 14/11, mục trên; giữ để tra):**
  - nút **"dày lịch" gần như không có tác dụng**: code chỉ thêm điểm thứ hai trong buổi khi điểm ghi thời lượng "ngắn" — bảng 28 điểm mới có 1 điểm như vậy (24 điểm chưa có thời lượng) ⇒ **chờ bạn duyệt bảng điểm v7** (cột thời lượng);
  - nhóm **có người lớn tuổi / trẻ em không bao giờ có buổi tối**, kể cả điểm kho ghi hợp người lớn tuổi;
  - **không nói được "lo mưa"** (biểu mẫu không có ô, cũng không có ngày đi ⇒ không có dòng dự báo); không có giờ tới / về.

- **Mới 07/11 — người dùng thấy:**
  - **Cổng du lịch đợt 1** thay trang hỏi đáp (merge `dbfc925`): trang chủ (ô hỏi, 5 câu gợi ý, 5 lĩnh vực, ô thời tiết), Khám phá đọc 204 bài kho (nút "Hỏi trợ lý về điểm này"), **Trợ lý Huế** nổi mọi trang + trang riêng (một cuộc trò chuyện qua các trang), Giới thiệu, thanh dưới điện thoại.
  - Câu trả lời **không còn số [n] trong chữ** — dưới câu có dòng **"Nguồn: <tên> · <tên>"**, bấm tên ⇒ đoạn gốc + "Đọc cả bài" (tầng máy vẫn giữ và kiểm [n]; mục web cũng bỏ [w n] khỏi chữ, link web vẫn do code dựng).
  - **Thời tiết bật** (`0dab4e5`): trợ lý trả lời câu dự báo bằng số Open-Meteo do code dựng; ô "Huế hôm nay" ở trang chủ.
  - Kiểm:
    - review cả nhánh đạt; 228 / 228 chuỗi gửi model giống byte khi cờ mới tắt;
    - Playwright: 7 / 7 đích tới được trong ≤ 2 lần bấm, 0 lỗi CSP / console, tương phản ≥ 4,5 : 1, 10 / 10 câu dòng "Nguồn" khớp nguồn API;
    - cổng sau merge: 352 test; 3 câu thật (trong kho có nguồn · ngoài phạm vi từ chối · thời tiết gọi đúng công cụ, ghi Open-Meteo + giờ); 0 câu hỏi trong log; ≈ 0,001 USD.
  - Chữ đầu trên cổng mới (10 câu, đồng hồ trình duyệt, một lần): trung vị **2,03 s**, chậm nhất 4,22 s.
- **Biểu mẫu "Lên kế hoạch" bản đầu — BẬT 07/11 (bạn duyệt; thay bằng bản 2 ngày 14/11):**
  - Code xếp lịch bằng giá trị nút (số ngày, đi cùng, sở thích), model chỉ viết lời theo khung; link bản đồ + ghi chú do code nối; "Sửa" ⇒ điền lại biểu mẫu.
  - Bộ quyết Q-F (12 tổ hợp ghi trước ×2 = 24 lượt):
    - sàn code **24 / 24** (0 từ chối, 0 lỗi kiểm cuối / khung, tham số = nút, 0 thẻ hỏi lại);
    - 2 agent chấm lời khớp khung **12 / 12 mỗi lượt**, 0 bất đồng;
    - chữ đầu p50 2,14 / **p95 4,25 s**;
    - **0,0087 USD** (0,00036 / lượt).
  - Tiêu chí "lời phù hợp người đi cùng": lời model trung tính ở 24 / 24 lượt. **Bạn chốt cách hiểu "không có lời trái với nhóm đã chọn" là đủ.**
  - Cổng sau khi bật (A): 352 test, một lượt biểu mẫu thật model tự viết lời, có sự kiện lịch trình. Chữ đầu một lượt ngay sau khởi động 5,77 s ⇒ đo lại 07/11 (C, 10 lượt biểu mẫu): 2,30 / 4,22 s — dưới sàn 5 s, không tái tạo được lượt chậm.
  - Đường tới V5 — lượt biểu mẫu hay bị model trả câu từ chối. X1 trên bộ phát triển 8 tổ hợp ×2:
    - luật nằm trong phần tài liệu ⇒ 10 / 16 từ chối;
    - luật lên lời dặn hệ thống ⇒ 0–1 / 16, nhưng chữ đầu p95 8,8 s;
    - thêm mức suy luận "low" cho riêng lượt biểu mẫu (V5) ⇒ **0 / 16 từ chối, chữ đầu p95 4,7 s, 0,00039 USD / lượt — khả thi**.

- **Khâu này làm gì:** chatbot Huế trả lời câu hỏi trên toàn bộ kho (món ăn, di tích, lễ hội, nghệ thuật, du lịch) qua một API và cổng du lịch
  trên web (từ 07/11). Dưới mỗi câu trả lời có dòng "Nguồn" trỏ tới đoạn nguồn thật (bên trong, máy vẫn đánh số `[n]` từng ý để kiểm); thiếu thông tin thì trả đúng một câu từ chối cố định, không bịa.
- **Đang chạy cách nào:** chuẩn hóa chữ câu hỏi (NFC — gộp dấu tiếng Việt về một dạng) → **từ 03/11 (B1):** `gpt-6-luna` phân loại câu hỏi (một lần gọi ngắn ~1,5 s): chào hỏi ⇒ đáp ngắn không tìm kho;
  ngoài phạm vi ⇒ câu soạn sẵn (**từ 10/11** câu chỉ hỏi về ngày tháng không tính là ngoài phạm vi); khẩn cấp ⇒ **từ 09/11 đi trợ lý Huế như câu về Huế** (trước: câu soạn sẵn 5 dòng 113 / 114 / 115 / 112); **từ 09/11 câu có từ chỉ ngày ⇒ thêm công cụ ngày + âm lịch (code tính)**; hỏi về Huế ⇒ tìm đoạn (từ 03/11 trưa, B2: model được gọi tìm thêm ≤ 2 lần bằng câu tự viết, đoạn mới đánh số tiếp) → lấy tối đa **10 đoạn** nguyên vẹn vừa
  ngân sách 16.384 token → `gpt-6-luna` (OpenAI, để mức suy luận mặc định) viết câu trả lời chỉ từ các đoạn đó → backend kiểm từng `[n]` →
  trả câu trả lời + nguồn. Mỗi lần hỏi, API ghi **một dòng số đo** (token, thời gian từng khâu, **tiền USD của câu và của từng lần gọi model, tuyến, công cụ đã chạy** — từ Phase 9 B0; không ghi nội dung câu hỏi / trả lời).
  **Từ B3 (03/11 tối, merge `a3dabba`):** câu dặn trả lời thêm một ý hẹp — không tự thêm lời khuyên / lưu ý an toàn mà nguồn không nêu, giữ lời khuyên có trong nguồn. **nhớ hội thoại BẬT từ B3b (merge `9e2ecd9`)**: server giữ **câu hỏi** của 3 lượt gần nhất (không giữ câu trả lời — `nho_cau_tra_loi: false`), cookie 30 phút; câu dặn thêm cho đường có lịch sử: mọi nhận định và trích dẫn chỉ từ đoạn nói đúng đối tượng được hỏi.
  Trang web: React + Vite + Tailwind (**làm lại 02/11**, merge `ed8e6e8`), **từ 07/11 thành cổng du lịch đợt 1** (mục đầu: trang chủ, Khám phá, Trợ lý Huế nổi mọi trang, Giới thiệu); trò chuyện **nhiều lượt từ 03/11 tối (B3)**: các lượt hỏi–đáp nối nhau, nút "Cuộc trò chuyện mới"; dưới mỗi câu là dòng **"Nguồn"** (thay số nhỏ bấm được trong chữ của 02/11–06/11; tầng máy vẫn `[n]`); nhãn "Trợ lý AI… có thể sai"; lỗi luôn báo bằng tiếng Việt; máy chạy cần build một lần `cd frontend && npm ci && npm run build`. Một lượt hỏi – đáp, **chữ hiện dần (streaming) từ 01/11** qua `POST /api/chat/stream`: kiểm trích dẫn ở cuối, hỏng thì rút lại, lỗi / đứt thì xoá + "Thử lại"; `/api/chat` (JSON một lần) vẫn giữ.
- **Đo được trên bản đang chạy** (10 đoạn, kho đã sửa hai đợt; 176 câu Golden; 30/10 trừ dòng ghi ngày khác; tốc độ / tiền hiện hành: lượt đo chung 09/11 ở mục đầu):
  - từ chối nhầm câu có trong kho **4–6 / 158** sau B2 (03/11; 30/10 là 12 / 158); **0** câu ngoài kho bị trả lời; câu sai điều kiện (giờ, vé, cảnh báo) trên bộ 32 câu an toàn: **0**;
  - lỗi trích dẫn (người dùng nhận lỗi 500): **0 / 489** lần sinh, đếm trên mọi lượt đo đã lưu;
  - so với chatbot đầu Phase 8.2 (5 đoạn) trên 33 câu kín: điểm Đủ **+0,82**, Đúng **+0,70** (thang 1–5), 0 câu tụt (28/10);
  - **tới chữ trả lời đầu tiên, sau B1 (03/11, 10 câu tự viết, đường stream):** cả 10 trung vị **3,05 s** / p95 **5,64 s**; câu về Huế **3,57 / 6,57 s**; trò chuyện 2,63 / 2,82 s; ngoài phạm vi 1,82 / 1,93 s; khẩn cấp 1,63 s — mẫu nhỏ;
    trước B1 (01/11, 38 câu, trình duyệt): 1,23 / 2,61 s; phần thêm là lần gọi phân loại (~1,5 s, chủ yếu chờ mạng / OpenAI — model chỉ suy luận ~14 token);
    **sau B2 (03/11 trưa, cùng 10 câu):** cả 10 3,33 / 5,20 s, câu về Huế 3,50 / 5,33 s;
  - **B2 tìm thêm (03/11):** 18 câu nhiều nguồn đủ ý **+1,17** [+0,44; +2,00]; Golden đủ ý / đúng +0,22; từ chối nhầm 12 ⇒ 4–6 / 158; bộ an toàn: **1 câu sai điều kiện mới thật** (thêm lời khuyên chung không có trong nguồn) — luật cho ≤ 2 cả Phase, đã dùng 1; tiền ≈ 0,00031 USD / câu;
  - tiền (giá đủ, lượt đo chung 09/11): câu về Huế **≈ 0,00047 USD / câu** (đạt trần 0,0005, sát trần); câu có ngày **0,00036 USD** (10/11, 19 câu, sau khi code tính sẵn ngày; trước 0,00049–0,00063 — vượt). Trước Phase 9 (01/11): ≈ 0,00025 USD / câu. Công cụ đo **tính giá đủ từ 01/11** (trước ghi thiếu ≈ 20 %, số USD cũ trong báo cáo đếm giá phẳng).
  - Điểm Đúng / Đủ / Trúng ý trung bình tuyệt đối chỉ có ở mốc cũ 7B (5 đoạn, 24/10): **4,43 / 4,28 / 4,45**; các lượt đo sau báo chênh theo cặp, không báo lại điểm tuyệt đối.
- **So với yêu cầu** (bạn chốt 28/10, đổi thước 31/10 D2: sàn trung vị ≤ 3 s / p95 ≤ 5 s **tới chữ trả lời đầu tiên trên trình duyệt**; ≤ 0,0005 USD / câu): theo lượt đo chung 09/11, **câu về Huế đạt** (2,16 / 4,32 s; 0,00047 USD); **câu xã giao (p95 7,73 s) vượt**; **câu có ngày đạt từ 10/11** (2,35 / 4,56 s; 0,00036 USD — trước 5,19–5,60 s, vượt).
  Trước đó: từ B1 (03/11) câu về Huế từng vượt sàn (3,57 / 6,57 s); song song #6 (bật 05/11) nhanh hơn ~1,37 s; trước B1 (01/11): 1,23 / 2,61 s. Bạn chọn giữ sàn 3 / 5 s (không nâng — mức dư nhỏ, hôm đo model gần như không suy luận trước) và giữ cách hiện chữ dần dù lợi chỉ ~0,44 s.
  Trước streaming (cả câu qua API, 27/10): 3,1 / 6,0 s — chưa đạt.
- **Giới hạn chính:** từ chối nhầm vẫn là chỗ mất điểm lớn nhất (gốc ở khâu tìm: đoạn có đáp án không vào 10 đoạn); câu hỏi theo ngày tương đối
  từng bị từ chối (6 / 14 câu, 30/10) ⇒ **từ 09/11 công cụ ngày bật** (mục đầu; từ 10/11 cả câu chỉ hỏi ngày tháng không nhắc Huế); bảng giá và câu tổng hợp nhiều nguồn còn yếu;
  10 đoạn được chọn bằng người chấm Claude; mốc người B0 (01/11) chỉ tham khảo — phần lớn cặp như nhau, 3 cặp bản 5 đoạn từ chối nhầm còn bản 10 trả lời được ⇒ bạn giữ 10.
- **Tối ưu tốc độ (04/11):** thí nghiệm #1 (tắt suy luận khi định tuyến) **âm** — nhanh hơn ~0,2–0,35 s nhưng phạm sàn an toàn ⇒ bỏ (mục 04/11). #6 (viết câu trả lời song song với định tuyến) **bật từ 05/11** (mục 4).
- **Hỏi lại người dùng (B4, 04–05/11) — không áp dụng:** thử cho trợ lý một công cụ "hỏi lại" (thẻ có nút chọn số ngày, số người…); hai vòng đo đều **âm** (mục 4, 05/11) ⇒ **công cụ này đã gỡ ở B5** (05/11), không còn cờ. Chỉ giữ thẻ nút do **code** bật khi lịch trình câu gõ thiếu số ngày — mà lịch trình câu gõ đang tắt ⇒ người dùng hiện không thấy thẻ này. Câu chi phí: thử **B5c (code tính tiền)** cũng âm, dừng.
- **Lịch trình từ câu gõ tự do (B5, 05–06/11; T4 09/11) — không áp dụng, cờ `lich_trinh` tắt:** bộ kín đầu 3 / 5 lịch "hợp người đi cùng" (câu đo không tự nhiên ⇒ không dùng để quyết); sửa 2 loại lỗi code vào `main` 06/11 (merge `dbb4004`, cờ vẫn tắt: sáng ưu tiên điểm hợp sở thích, buổi tối để trống có lý do, model từ chối ⇒ code dựng lịch tối thiểu); bộ kín v2 3 / 5 (dòng dưới); thử lại 09/11 (T4) vẫn âm (mục đầu) ⇒ lịch trình chỉ qua biểu mẫu.
- **Thời tiết (B5b) — merge `db77f32` 06/11 tối, BẬT 07/11 (`0dab4e5`, bạn chọn khi merge cổng):** công cụ `thoi_tiet` (Open-Meteo; số do code dựng, ghi giờ số liệu; ngoài 7 ngày ⇒ câu cố định; bão / lũ ⇒ NCHMF + 112). Review cả nhánh đạt sau sửa 4 lỗi; cổng sau merge: 196 test đạt, build giao diện, server thật 1 câu trong kho + 1 câu ngoài kho đúng, log 2 dòng số đo, 0 câu hỏi trong log (≈ 0,0006 USD).
- **Lịch trình đo bộ kín v2 (22:10 06/11/2026) — KHÔNG ĐẠT:** 5 câu tự nhiên bạn duyệt; 2 agent chấm độc lập khớp 15 / 15 ô: đúng luật xếp 4 / 5 · có nguồn / hợp người đi cùng 3 / 5 · không thêm sai 4 / 5 ⇒ 3 / 5 câu đạt cả 3 tiêu chí (cần ≥ 4 / 5) ⇒ cờ `lich_trinh` giữ **tắt**. Loại lỗi: hỏi lại số ngày thừa dù câu đã ghi (dạng viết tắt); "đi dày" mà lịch thưa (bảng điểm thiếu thời lượng); **2 / 5 câu model từ chối khi câu có kèm câu hỏi phụ (chỗ ở / cách đi)** — lịch vẫn hiện nhờ code tự dựng, nhưng câu hỏi phụ bị bỏ qua im lặng. Tiền 0,003 USD. Hồ sơ `report_agent/2026-11-06_b5_cau_tu_nhien/e19_kin_v2.md`.
  Sau đó bạn chọn **lịch trình qua biểu mẫu, code quyết** (mục đầu tóm tắt); câu gõ tự do giữ tắt.

## 2. Hoạt động thế nào (bản đang chạy)

```text
trang web / POST /api/chat/stream (từ 01/11) hoặc /api/chat {"query": "..."}   (1–500 ký tự; hai route dùng chung lõi backend/llm/assistant.py — tên cũ grounded_answer.py tới B0)
 → chuẩn hóa NFC → tìm đoạn (dense + từ khóa, trộn RRF) → lấy tối đa 10 đoạn nguyên vẹn, vừa ngân sách 16.384 token
 → gpt-6-luna viết câu trả lời, chỉ dùng các đoạn đó, đặt [n] sau mỗi ý (hoặc trả đúng câu từ chối)
 → backend đổi [Nguồn n] về [n], kiểm từng [n] có trỏ đúng nguồn đã đưa không
 → trả {answer, sources (kèm bai_id khi là bài kho)}; lỗi có mã rõ ràng: 422 câu hỏi không hợp lệ · 409 chỉ mục lệch kho · 503 tìm kiếm tạm lỗi · 500 trích dẫn hỏng · 429 hết lượt hỏi trong ngày (chỉ khi đặt `HUE_LUOT_MOI_NGAY`, từ 09/11)
 → ghi một dòng chat_metrics (backend/logs/application.log)
Stream: lỗi trước khi model viết = JSON như trên; sau đó sự kiện status → delta… → (kiểm trích dẫn) sources → done, hoặc error{after_text} → done
(Phase 9 thêm trước / quanh bước trên: định tuyến 4 tuyến · công cụ tim_kho ≤ 2 lần · thoi_tiet (từ 07/11) · lịch tính sẵn (từ 10/11: câu có từ chỉ ngày ⇒ code đổi ngày, thêm nguồn "Lịch hệ thống" trước lần gọi model đầu; công cụ ngay_lich chỉ dự phòng) · tra web khi kho từ chối · biểu mẫu "Lên kế hoạch" {bieu_mau} không qua định tuyến (từ 07/11; bản 2 từ 14/11: sự kiện lich_khung → lich_cau… → lich_xong) · sửa lịch bằng lời (từ 14/11): cuộc có lịch đã lưu ⇒ hiểu ý + định tuyến chạy song song (asyncio.gather), khẩn cấp thắng; lượt sửa ⇒ cùng luồng sự kiện lịch bản 2, hoặc sự kiện sua_the (thẻ chọn); POST thêm trường sua_chon {cu, moi} khi bấm thẻ — mục 1, mục 4.)
Hỏi bằng ảnh (từ 08/11): POST /api/anh/ung_vien → ảnh thu nhỏ gửi gpt-6-luna gợi ≤ 3 tên → người dùng bấm tên ⇒ thành câu hỏi thường ở trên (máy chủ không lưu ảnh). "Cuộc trò chuyện mới": POST /api/conversation/new.
Trang khác, không gọi model (từ 07/11): GET /api/kham_pha · /api/kham_pha/bai?id= (chỉ mã trùng nguyên văn một file của chỉ mục) · /api/thoi_tiet · /api/tinh_nang
```

- Khi khởi động, hệ thống so "dấu vân tay" kho với hồ sơ chỉ mục; kho đổi mà chưa dựng lại chỉ mục thì từ chối chạy.
- Trang web (từ 07/11) bỏ số `[n]` khỏi chữ, hiện dòng "Nguồn: <tên> · …" dưới câu; bấm tên ⇒ tiêu đề, mục, đoạn trích nguyên văn + "Đọc cả bài" (`frontend/src/chat.jsx` `SourceLine`, `markdown.js`).
- Code: `backend/api/routes/chat.py` (API; kiểm câu hỏi `:36–38`, route `:60`, kiểm trích dẫn `:177–188`), `backend/retrieval/full_corpus_context.py`
  (chọn đoạn theo ngân sách), `backend/config/settings.yaml:48` (model), `:53` (ngân sách), `:56` (`max_context_documents: 10`),
  `backend/llm/full_corpus_prompt.py:7–16` (prompt), `backend/llm/generator_openai_full_corpus.py` (gọi model), `backend/llm/citations.py:11` (mẫu bắt
  `[n]` và `[Nguồn n]`), `frontend/src/` (trang web React; bản build `frontend/dist/` phục vụ ở `backend/api/app.py:159–166`).

Tự hỏi chatbot (không bắt buộc): bật Docker Desktop, `docker compose up -d qdrant`; từ `backend/` chạy
`HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8000`; mở `http://localhost:8000`. Mỗi câu hỏi gọi `gpt-6-luna` (phí rất nhỏ).

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Câu có đủ bằng chứng → trả lời kèm `[n]` | **Đã xử lý, đóng gói** | mốc 7B (5 đoạn) 4,43 / 4,28 / 4,45; câu kín 28/10 (10 đoạn) Đủ +0,82, Đúng +0,70 so với 5 đoạn |
| Câu ngoài kho → từ chối, không bịa | **Đã xử lý, đóng gói** | 30/10: 0 câu ngoài kho bị trả lời (Golden; bộ an toàn 0 / 4); câu từ chối cố định `full_corpus_prompt.py:3–5,14–15` |
| Kiểm `[n]` trỏ đúng nguồn, lỗi thì trả mã rõ ràng | **Đã xử lý, đóng gói** | nhận cả `[Nguồn n]`, đổi về `[n]` (từ 25/10); bản đang chạy 0 / 489 lần sinh lỗi; dạng lỗi còn thấy ở bản cũ chỉ là "không gắn `[n]` nào"; `citations.py:11`, `chat.py:177–188` |
| Hiển thị nguồn cho người đọc | **Đã xử lý, đóng gói** (07/11, cổng đợt 1 — thay số nhỏ bấm được của 02/11) | chữ bỏ `[n]` / `[Nguồn n]` / `[w n]` (cả mã dở khi chữ đang hiện); dòng "Nguồn" = `title` của sự kiện `sources` (10 / 10 câu khớp); `frontend/src/markdown.js`, `chat.jsx` `SourceLine` |
| Đọc bài kho trên giao diện (Khám phá) | **Đã xử lý, đóng gói** (07/11; làm lại 14/11 — ảnh **184 / 216** bài, không chữ ghi công, thẻ "Thông tin nhanh" chỉ tách khi không mất dòng) | `/api/kham_pha` = danh sách file của chỉ mục (204 / 204 lúc làm 07/11; 216 từ lần ghi kho 3 ngày 14/11); `/api/kham_pha/bai` chỉ mã trùng nguyên văn (`..`, `evaluation/`, câu kín, mã hoá lạ ⇒ 404 — review E thử 20 kiểu); Markdown qua DOMPurify; `backend/api/routes/cong.py` |
| Câu dự báo thời tiết | **Đã xử lý, đóng gói** (bật 07/11) | công cụ `thoi_tiet`, số do code dựng; cổng sau khi bật: 1 câu thật gọi đúng công cụ; `backend/llm/thoi_tiet.py` |
| Lịch trình qua biểu mẫu (nút chọn) | **Đã xử lý, đóng gói** (bản 2 bật 14/11, bạn duyệt D4; bản đầu 07/11) | biểu mẫu 4 nhóm; code xếp theo chuỗi luật + quỹ phút + giờ gợi ý + mưa theo dự báo; model chỉ câu tả từng điểm; bộ 20 20 / 20 (≤ 1 câu dự phòng), bộ để dành 12 / 12 × 2 (2 người chấm mù); ảnh 24 / 34 điểm; `.ics`; nơi ở gợi ý (từ 14/11 chiều, code chọn khu + cơ sở, không giá); lịch mẫu "Ví dụ" khi chưa xếp. **Giới hạn:** chưa có ô giờ tới / về; bảng 34 điểm; khung > 1 s ở lượt đầu có dự báo (bạn nhận); chưa có quán ăn trong lịch; bản đồ cả lịch chưa bật. `backend/llm/lich_trinh_v2.py`, `len_ke_hoach.py` |
| Sửa lịch bằng lời (nhiều lượt) | **Đã xử lý, đóng gói** (bật 14/11, `e0cb02e`) | hiểu ý ⇒ hành động có tên, code áp + kiểm; song song định tuyến, khẩn cấp thắng; đã thấy 9 / 10 pass^2, kín 4 / 5, an toàn 0 / 64, câu trộn khẩn cấp 0 / 16. **Tốc độ (bật lại 14/11 chiều):** câu thường có lịch p50 2,65 / p95 4,01 s ≈ không lịch. **Giới hạn:** câu chỉ chỗ bằng ngày / buổi để model chọn điểm (minor review); bộ kín đạt đúng sàn. `backend/llm/sua_lich_v2.py` |
| Kho lệch chỉ mục → từ chối khởi động | **Đã xử lý, đóng gói** | API báo 409 "cần lập chỉ mục lại"; `retrieval/full_corpus.py:383–385`; test `test_api_chat.py` |
| Qdrant / model tìm kiếm lỗi → báo lỗi tạm | **Đã xử lý, đóng gói** | 503 `retrieval_unavailable` (`chat.py:96–119`); test `test_startup_model_missing.py` (bạn chạy `!`) |
| Đưa 10 đoạn thay vì 5 + chuẩn hóa NFC | **Đã xử lý, đóng gói** (từ 28/10) — B0 01/11: bạn giữ 10 (tham khảo) | 8.1: Đủ +0,26 (thử) / +0,27 (kiểm); câu kín +0,82; trung vị / p95 2,19 / 4,90 s. Đổi ngược về 5: sửa `settings.yaml:56` **và** chốt kiểm ở `core/settings_loader.py:75` (đang ép đúng 10) |
| Câu có một vế có bằng chứng, vế kia thiếu | **Đã xử lý, đóng gói** (14/11 chiều, `cau_nhieu_y` bật) | code đếm ≥ 2 vế hỏi ⇒ lời dặn theo ý, ý thiếu ghi một dòng cố định, chỉ còn dòng thiếu ⇒ câu từ chối chuẩn; mục web chỉ viết cho vế thiếu. Hỏi kèm 10 / 10 (cũ 4 / 10); câu "và" 10 / 10; nêu lại ý kho ở mục web 0 / 11. **Giới hạn:** câu đếm được 1 vế ⇒ luật cũ (từ chối cả câu). Trước: hai lần thử "trả lời phần có căn cứ" trả lời câu ngoài kho; T2 09/11 không lợi (`hoso/p9-t2-web`). `backend/llm/assistant.py` `so_y`, `ve_y_thieu` |
| Đoạn chứa đáp án nằm ngoài các đoạn đưa model | **Xử lý một phần** | mọi câu từ chối nhầm đo ở 8.1 đều thiếu ít nhất một đoạn đúng — gốc ở khâu tìm; 10 đoạn giảm gần một nửa; phần còn lại: `06_BAO_CAO_TIM_KIEM.md` |
| Mức suy luận của model | **Đã thử, chưa áp dụng** | giữ mặc định (không gửi tham số: `generator_openai_full_corpus.py:98–99,120`); `none` kém hơn (trả lời vòng câu lẽ ra từ chối), lợi tiền chỉ 3–6 % (mục 4) |
| Câu trả lời quá gọn, bỏ chi tiết có trong nguồn | **Chưa thực hiện** | 26/10: 9 / 88 câu mất điểm vì bỏ chi tiết; thử "nêu đủ chi tiết" không chạy được (chỉ 6 câu đổi được, quá ít để kết luận) |
| Câu trả lời ghi sai con số (giá, giờ, năm) | **Xử lý một phần** (đo được, chưa có rào chặn) | 27/10, 10 đoạn: 0 / 68 câu có số bị thấy sai; chưa đo sai về chữ (tên, sự kiện) |
| Kiểm bằng code sau khi sinh để chặn "trả lời vòng" | **Đã thử, chưa áp dụng** | 7 / 10 câu bị cờ là câu có ích ⇒ gác |
| Để model chọn 10 / 30 đoạn trước khi trả lời | **Đã thử, chưa áp dụng** | trung bình tốt lên nhưng 5 câu tụt > 4 cho phép; chờ ~6,5 s, tiền ×3,8 (mục 4) |
| Xếp đoạn gom theo tài liệu; 2 luật cũ của prompt Phase 6; "một nguồn thì gán nguồn đó" | **Đã thử, chưa áp dụng** | 8.1: không khác (mục 4) |
| Câu tổng hợp nhiều nguồn | **Xử lý một phần** | lúc đóng Phase 6 chỉ dùng 1 nguồn; 8.1: lợi của 10 đoạn nằm nhiều ở câu nhiều nguồn / so sánh; chưa có phép đo riêng "tổng hợp đúng" |
| Câu hỏi giá vé + miễn giảm (bảng giá) | **Đã thử, chưa áp dụng** | không tìm ra dòng bảng giá; 8.1 thử gộp dòng bảng khi chia đoạn: không khác (`06_BAO_CAO_TIM_KIEM.md`); chưa đo lại riêng ở 10 đoạn |
| Tách câu hỏi hai ý | **Đã xử lý** (14/11, cùng dòng trên) | code đếm vế (`so_y`), model trả lời theo ý trong một lần viết — không tách thành hai lần tìm |
| Câu hỏi theo ngày tương đối ("tối nay", "tháng sau", "rằm tháng Giêng") | **Đã xử lý, đóng gói** (09/11: merge `99ea59a`, **bật** `7eb1f12`, bạn duyệt; **10/11 nhanh hơn**: code tính sẵn ngày, merge `1633c18` — chữ đầu 2,35 / 4,56 s, 0,00036 USD) | công cụ ngày (code tính, lịch âm Việt Nam UTC+7, năm 1976–2100): 14 câu mới bớt 9 từ chối nhầm, 0 sai ngày; sau sửa "năm nay" / "sang năm": câu ngày có ngữ cảnh Huế 3 / 3 ↔ bản cũ 1 / 3; an toàn 0 lỗi; server thật sau khi bật: "rằm tháng Giêng" ⇒ thứ Bảy 20/02/2027. Giới hạn: câu lịch thuần không nhắc Huế ⇒ ngoài phạm vi; "tháng tới / cuối tuần" model tự cộng. `backend/llm/ngay_lich.py` |
| Hiện chữ dần (streaming) | **Đã xử lý, đóng gói** (01/11, merge `a80e12d`) — 4 bước + review cả nhánh đạt; S4 đạt sàn + mục tiêu | bạn duyệt spec 01/11 (`00fb57ee01b2`); cả 4 bước (gom lõi chung, luồng chữ, giao diện, đo) xong 01/11 (mục 6) |
| Câu khẩn cấp (đang gặp nguy / vừa bị cướp, tai nạn…) | **Đo lại 14/11: từ chối 10 / 12, có số 112–115 0 / 12 — giới hạn đã nhận (bạn quyết 12/11)** · **Đã đổi 09/11** (định tuyến phương án B, merge `3b52017`): không còn câu soạn sẵn 113 / 114 / 115 / 112 — đi trợ lý Huế như câu thường (bạn chấp nhận 08/11) | trợ lý từ chối ⇒ cổng web mở (mục "Từ web (chưa kiểm)"); thiên tai ⇒ câu cố định NCHMF / 112 (B6). Lượt đo B (92 câu): ngoài phạm vi bị trả lời 0, câu Huế ra ngoài phạm vi 0; 1 câu y tế ngoài phạm vi bị xếp khẩn cấp ⇒ có mục web (A nhận). Trước: B143 03/11 sửa câu "vừa bị cướp" ra câu khẩn cấp |
| Người dùng đánh giá câu trả lời (👍 / 👎) | **Đã xử lý, đóng gói** (03/11 tối, B142 merge `6817897`) | `POST /api/feedback` {mã lượt, up / down}; mỗi lần bấm một dòng log `chat_feedback` (mã lượt ngẫu nhiên, tuyến, kết quả, số nguồn, đánh giá) — không chữ câu hỏi / trả lời, không mã cuộc; đổi ý được; cổng: 200 / 422 đúng, log 0 nội dung. Từ 08/11 dòng số đo `chat_metrics` cũng ghi mã lượt ⇒ nối được đánh giá với số đo của đúng lượt đó |
| Câu ngoài phạm vi kèm gợi ý | **Đã xử lý, đóng gói** (03/11 tối, B142) | 3 nút câu gợi ý cố định có trong kho (chỉ giao diện, không đổi model / lời dặn); bạn chọn web chỉ cho câu **về Huế** (B6) |
| Hội thoại nhiều lượt — giao diện | **Đã xử lý, đóng gói** (03/11 tối, B3 merge `a3dabba`) | Bản 1 bạn chọn; Playwright server thật: CSP 0 vi phạm, 0 request ra ngoài, điện thoại không cuộn ngang; review C147 `ready` |
| Hội thoại nhiều lượt — trợ lý nhớ câu trước | **Đã xử lý, đóng gói** (03/11 tối, B3b merge `9e2ecd9`; chỉ nhớ câu hỏi) — trước đó cờ tắt vì sàn kín phạm | đã thấy: nhớ tên 6 / 6, hỏi tiếp đủ ý +0,65; kín: nhớ tên cộng 10 / 10, hỏi tiếp +0,60 (không ngược chiều), 0 đảo cảnh báo; **1 / 2 lượt ngoài kho kín bị trả lời bằng đoạn nguồn của đối tượng khác** ⇒ sàn phạm ⇒ không bật (luật ghi trước); bạn chọn sửa lời dặn, đo trên bộ chuỗi mới |
| Không tự thêm lời khuyên an toàn thiếu nguồn | **Đã xử lý, đóng gói** (03/11 tối, B3) | câu dặn hẹp; 208 câu: từ chối nhầm 4, Đủ / Đúng không tụt, 0 câu sai điều kiện; câu an toàn lỗi của B2 hết lỗi |
| Giao diện web mới (React + Vite + Tailwind) | **Đã xử lý, đóng gói** (02/11, merge `ed8e6e8`; **thành cổng đợt 1 07/11**, merge `dbfc925`; **làm lại "Sông Hương" 14/11**, merge `55f48fe` — hiệu ứng CSS, đo tương phản / CLS / giảm chuyển động, JS 123,48 KB) | 02/11: 19 yêu cầu, CSP không nới, 0 gói Radix / shadcn. 07/11: bản mẫu "Sông Hương", điều hướng `#/…` (0 gói router), 0 gói npm mới, CSP không đổi, JS 106 KB gzip; Playwright Q-G / Q-N đạt (C); review cả nhánh đạt (E); `report_agent/2026-11-06_giao_dien_cong/` |
| Lịch trình từ câu gõ tự do (B5 / T4) | **Đã thử, chưa áp dụng** (cờ `lich_trinh` tắt; T4 đóng hồ sơ 09/11, tag `hoso/p9-t4-lich`) | 09/11, 31 câu: có lịch 27 / 27, hỏi lại thừa 0, từ chối thay lịch 0; **hợp người đi cùng 21 / 27 · 15 / 27** (cần 26) — gốc ở luật xếp / bảng điểm (đi dày, sở thích nói bằng lời, buổi tối nhóm hạn chế, lo mưa); lịch trình chỉ qua biểu mẫu |
| Giá vé / giờ mở cửa từ bảng có cấu trúc (T3) | **Đã thử, chưa áp dụng** (đóng hồ sơ 09/11, tag `hoso/p9-t3-bang`) | vòng 3: đúng 19 / 20; sàn "không tự nêu điều kiện ngoài khối do code nối" trượt 6 / 10 (model chép điều kiện từ đoạn kho); phương án B (bảng chỉ để kiểm số) lợi đo được ≈ 0 ⇒ bạn đóng. Câu giá / giờ vẫn trả lời như cũ từ đoạn kho |
| Chốt trước khi đưa link công khai (giới hạn lượt / IP / ngày, cookie `Secure`, tắt `/docs`, log xoay vòng) | **Đã xử lý** (09/11, merge `ccc9f4f`; bật bằng biến môi trường lúc deploy) | không đặt biến ⇒ như cũ; quá lượt ⇒ 429 + câu tiếng Việt; không ghi IP vào log; `backend/api/gioi_han.py`, `api/app.py`, `config/logging.yaml`; test `test_chot_deploy.py` |
| Ảnh trên cổng | **Đã có** (08/11, `c9931be`; 14/11: ảnh Khám phá 184 / 216) | ảnh đầu trang + ảnh bài; **từ 14/11 chiều không hiện chữ ghi công ở đâu** (bạn yêu cầu) — nguồn từng ảnh giữ ở bảng dữ liệu `data/anh_kham_pha_2026-11-14/` |
| Ảnh dưới câu trả lời | **Đã xử lý, đóng gói** (14/11 chiều, merge `4be483e`, chỉ giao diện) | code quyết: một ảnh khi mọi nguồn trích thuộc một bài về một nơi / món, ảnh không gắn "không chắc"; không ảnh khi từ chối / mục web / lịch / nhiều bài. `frontend/src/anhTraLoi.js`, test `test_anh_tra_loi.py` |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (mới ở trên)

### 14/11/2026 — "Lên kế hoạch" bản 2 bật; sửa lịch bằng lời bật; giao diện mới + ảnh Khám phá
- **Bản 2** (merge `86c093d`, bật 11:00): nghiệm thu lần đầu trượt (bộ 20 16 / 20) ⇒ sửa dữ liệu ⇒ 20 / 20; người chấm mù bắt 3 lỗi (dòng mưa, sáng chồng chiều, câu nội bộ) ⇒ sửa code ⇒ 12 / 12 × 2. Report `b_len_ke_hoach_dot_1_implementation.md`, review `e_review_len_ke_hoach_nhanh_1411.md`.
- **Sửa lịch bằng lời** (merge `e572330`, bật `e0cb02e`): review E lần 1 changes_requested (B-1 câu trộn sửa + khẩn cấp mất phần khẩn cấp, đo thật 2 / 2; M-1 thẻ chọn làm mất hành động khác) ⇒ sửa `2bc020d` (song song định tuyến, khẩn cấp thắng) ⇒ ready; một vòng chỉnh lời dặn hiểu ý `0501094` (Q3 đã thấy 7 ⇒ 9 / 10; kín 4 / 5 chạy sau) ⇒ E kiểm nhẹ ready (2 minor).
- **Giao diện** (merge `55f48fe`) + **ảnh Khám phá** (merge `ef8bc46`): review chéo C / E / B; lỗi lớn đã sửa: thẻ "Thông tin nhanh" mất dòng 51 / 207 bài ⇒ 0; trang hứa tính năng không theo cờ ⇒ theo `/api/tinh_nang`.
- **Đo lại đường khẩn cấp trên main** (E, 0,027 USD): giới hạn đã nhận, không làm.

### 10/11/2026 — câu chỉ hỏi về ngày tháng đi trợ lý (sửa lời dặn bước phân loại)

- **Thử gì:** thêm 2 câu vào lời dặn bước phân loại (bạn chọn cách này 21:00 10/11 thay cho luật từ khoá: "nhiều cách viết, code không bắt hết"). Luật ghi trước: plan
  định tuyến lịch bản 2 (2 vòng review). Đo rẻ: chỉ chạy lần phân loại cũ ↔ mới; chỉ câu đổi loại mới sinh câu trả lời và chấm.
- **Kết quả:** bản dặn 1 kéo nhầm 1 câu ngoài phạm vi ⇒ bản 2 thu hẹp ⇒ đạt mọi tiêu chí (mục đầu). 1 câu Golden đổi loại ở một lượt nhưng không có từ chỉ ngày; chạy lại
  5 lần mỗi bản đều đúng ⇒ nhiễu.
- **Giữ:** merge (bạn đồng ý). Hồ sơ ở phụ lục.

Mỗi dòng: thử gì · kết quả · giữ / bỏ vì sao · hồ sơ. Thí nghiệm chọn / bỏ phương án có luật ghi trước khi chạy và người khác kiểm lại; các lượt **đo hiện trạng** (tốc độ, giá, token) chỉ đo — không có luật giữ / bỏ ghi trước.

### 10/11/2026 — câu ngày nhanh hơn: code tính sẵn ngày (merge `1633c18`)

- **Thử gì:** câu có từ chỉ ngày ⇒ code tính hôm nay / mai / các ngày trong tuần được hỏi + đổi các ngày âm thấy trong câu hỏi và trong đoạn kho lần tìm đầu (≤ 6),
  thành một nguồn "Lịch hệ thống" trước lần gọi model đầu; công cụ `ngay_lich` giữ làm dự phòng (chỉ đổi mô tả). Luật ghi trước: plan `2026-11-10-phase-9-t1-nhanh-plan.md`.
- **Kết quả (1 lượt, 19 câu ngày, mốc = bản đang chạy cùng giờ):** chữ đầu 5,60 / 10,14 ⇒ **2,35 / 4,56 s**; 0,00049 ⇒ **0,00036 USD / câu**; lần gọi model 52 ⇒ 31.
  Lượt đầu tụt 1 câu đúng ngày ("năm nay" ⇒ model chọn lần năm sau) ⇒ dừng, sửa bằng code (ghi thẳng ngày của năm âm được nói) ⇒ đo lại 8 câu "năm nay / năm sau":
  số câu sai ngày bằng bản trước. An toàn 12 / 12, Golden có từ chỉ ngày 9 / 9, câu không nói về ngày giống byte (215 / 228; 13 khác = đúng câu có từ chỉ ngày).
  Review C: 1 lỗi "mùng N tháng <số>" bị coi là ngày âm (vd ngày dương 2/9) ⇒ chỉ tính khi có chữ "âm"; số đo không đổi.
- **Giữ:** đạt mọi tiêu chí ghi trước ⇒ merge (bạn duyệt). 2 câu bị xếp ngoài phạm vi ở bản mới mà bản cũ trả lời: dao động định tuyến (chuỗi gửi định tuyến giống byte).
  Hồ sơ `report_agent/2026-11-02_phase_9_code/e_t1_nhanh_implementation.md`; review `report_agent/2026-11-02_phase_9_code/e_t1_nhanh_review.md`.

### 09/11/2026 — công cụ ngày đo xác nhận; T3 đóng hồ sơ; G chuyển phương án B; 4 chốt trước deploy vào `main`

- **T1 ngày + âm lịch — lượt xác nhận** (luật ghi trước `data/phase_9/t1/xac_nhan/tieu_chi.md`, 14 câu mới, 1 lượt mỗi bên, 2 người chấm mù khớp 14 / 14): từ chối nhầm −9 (sàn ≥ 3 — đạt) · sai ngày 0 (đạt) · trần vòng 0 (đạt) · **1 câu nói sai thời điểm mới ("Tết năm nay" — trượt 2 / 5 tiêu chí)** ⇒ không đổi tiêu chí sau khi thấy kết quả; A chọn sửa bằng code (lần đã qua + lần sắp tới + dòng nhắc ghi năm), thêm "sang năm" vào bộ dò; nhánh `p9-t1-sang-nam` `ff65510`, 824 test đạt, cờ tắt. Đo lại cùng lượt "sau định tuyến mới" (luật ghi trước mục 2 của file trên). Thay lượt đo tốc độ riêng bằng số chữ đầu của lượt này (A chốt). 0,026 USD. Hồ sơ `report_agent/2026-11-02_phase_9_code/e_t1_ngay_implementation.md` §4e.
- **T3 bảng vé + giờ — đóng hồ sơ** (tag `hoso/p9-t3-bang`): xem checklist. Hồ sơ `report_agent/2026-11-06_giao_dien_cong/c_t3_bang_implementation.md`.
- **G cổng 2 nhóm — dừng, phương án B:** S1 âm rồi chỉnh một vòng; bản cuối trượt S2b trên bộ đã thấy 2 / 44 (bản cũ 0 / 44) ⇒ quá số vòng chỉnh ⇒ A chốt phương án B spec (giữ 4 tuyến, bỏ câu khẩn cấp soạn sẵn). Tag `hoso/p9-g-cong`; review code bản 2 nhóm (E): 0 lỗi chặn. Hồ sơ `report_agent/2026-11-08_phase_9_ban_13/b_g_cong_implementation.md`, `g_cong_branch_review.md`.
- **4 chốt trước deploy** (merge `ccc9f4f`): xem checklist.
- **Sau đó trong ngày:** định tuyến phương án B merge `3b52017` (review E đạt); T1 lượt sau định tuyến đạt ⇒ merge `99ea59a` + **bật** `7eb1f12` (bạn duyệt); **T2 âm** (hỏi kèm có web 4 / 10 = mốc; 26 / 29 lần yêu cầu web trùng câu từ chối cả câu) ⇒ tag `hoso/p9-t2-web`; **T4 âm** (Q3 hợp người đi cùng 21 / 27 · 15 / 27, cần 26) ⇒ tag `hoso/p9-t4-lich`. Hồ sơ `report_agent/2026-11-08_phase_9_ban_13/e_t2_web_implementation.md`, `e_t4_lich_implementation.md`; `report_agent/2026-11-02_phase_9_code/e_t1_ngay_implementation.md` §4f.

### 07/11/2026 chiều — biểu mẫu "Lên kế hoạch" BẬT (V5 merge `312ad9f`, cờ `a884de4`)
- **S3 — bộ quyết** (C; 12 tổ hợp ghi trước, khác 8 tổ hợp X1; ×2; luật ghi trước ở spec cổng §6 Q-F):
  - sàn code **24 / 24**;
  - F-a 2 sub-agent **12 / 12** lần 1 và lần 2, 0 bất đồng;
  - chữ đầu p95 **4,25 s** (sàn 5 s);
  - **0,008702 USD** ⇒ **đạt**.
  - Người chấm nêu: lời trung tính, không câu riêng cho nhóm đi cùng ⇒ **bạn chốt "không trái nhóm là đủ"** ⇒ bật cờ.
- **Kèm theo:** B ghim test mốc "cờ tắt" (vì `settings.yaml` nay bật cờ).
- **Cổng sau khi bật** (A): 352 test; `/health` 5 / 5; `/api/tinh_nang` biểu mẫu = true; lượt biểu mẫu thật (2 ngày · người lớn tuổi · ẩm thực) model tự viết lời; câu kho + ngoài phạm vi đúng; 0 câu hỏi trong log.
- Chữ đầu 1 lượt ngay sau khởi động 5,77 s ⇒ C **đang đo** 10 lượt.
- Hồ sơ `report_agent/2026-11-06_giao_dien_cong/c_s3_q_f_implementation.md` §5.

### 07/11/2026 — cổng du lịch đợt 1 vào chatbot (merge `dbfc925`), thời tiết bật (`0dab4e5`); thử chỗ đặt luật của lượt biểu mẫu (X1)
- **Cổng:**
  - B làm backend (S1: đường biểu mẫu sau cờ, 4 API chỉ đọc, `bai_id`) + giao diện (S2).
  - E review cả nhánh: đạt, 0 lỗi lớn — Q1 228 / 228 giống byte; API bài kho chặn mọi mã lạ; chữ gõ ở biểu mẫu không vào model; DOMPurify ở cả 3 chỗ hiện HTML.
  - 3 lỗi nhỏ đã sửa trước merge: link `//máy` thiếu `rel`, tên tab cũ, câu "bạn hỏi thêm" ở lịch bị cắt ngày.
  - C đo Q-G / Q-N: đạt.
  - Cổng ổn định sau merge (A): đạt. Tiền S1 + S2 + đo ≈ 0,01 USD.
- **Thời tiết bật** theo lựa chọn của bạn (Q-U4) khi merge cổng.
- **X1 — vì sao lượt biểu mẫu bị từ chối** (C; bộ phát triển 8 tổ hợp ×2, không phải bộ quyết; luật ghi trước "0 / 16 từ chối, kiểm cuối 16 / 16, chữ đầu p95 ≤ 5 s"):
  - **V0** (luật viết lời nằm trong phần tài liệu): từ chối 10 / 16.
  - **V1** (giả một lượt công cụ): 12 / 16 — không giúp.
  - **V2** (luật lên lời dặn hệ thống): 1 / 16 ở X1, 0 / 16 ở X1b, nhưng chữ đầu p95 8,8 s.
  - **V3** (code tự dựng lời, không model): 0 USD, 0,16 s, nhưng chữ đọc như trích máy.
  - **V4** (V2 + câu dặn "luôn viết lời"): 2 / 16 — phản tác dụng, bỏ.
  - **V5** (V2 + mức suy luận "low" chỉ cho lượt biểu mẫu): **0 / 16, kiểm cuối 16 / 16, chữ đầu p95 4,7 s, 0,00039 USD / lượt — khả thi**.
  - V6 ("minimal"): API từ chối.
  - Kết luận: giả thuyết "model coi luật nằm trong tài liệu là dữ liệu không đáng tin" được ủng hộ, **chưa phải chứng minh**.
  - Bước tiếp (đã làm chiều 07/11): V5 vào nhánh ⇒ bộ quyết đạt ⇒ bật (mục trên).
  - Tiền X1 + X1b + X1c = 0,024689 + 0,017425 + 0,014332 ≈ **0,056 USD**. Hồ sơ `report_agent/2026-11-06_giao_dien_cong/c_x1_luot_bieu_mau.md`, `c_s3_q_f_implementation.md`, `s4_review_backend.md`, `s4_review_frontend.md`.

### 06/11/2026 — lịch trình B5: chấm bằng agent, câu đo không tự nhiên ⇒ làm lại bộ câu; sửa lỗi lịch trình + thời tiết (trên nhánh)
- **Chấm 5 lịch kín (bạn chọn 10:03 06/11/2026: agent chấm trước, bạn đọc chỗ lệch):** 2 sub-agent Claude ngữ cảnh mới, chưa từng làm B5, chấm riêng không xem của nhau — khớp **15 / 15 ô**. Đúng luật xếp 5 / 5 · có nguồn 5 / 5 · **hợp người đi cùng 3 / 5**: một lịch bỏ qua sở thích / kiểu đi người dùng nói (lỗi ở code xếp + bảng điểm thiếu thời lượng; độ chắc cao), một lịch lời trả lời nói "được" với buổi tối trong khi code không xếp buổi tối vì có trẻ nhỏ (lỗi model + code thiếu câu báo; độ chắc vừa). 0 USD (quota Claude). Lý do chi tiết: `data/phase_9/b5/kin/cham_agent_{1,2}.md` (private).
- **Bạn đọc phiếu: câu hỏi kín không tự nhiên** ⇒ theo luật "câu đo phải giống người thật hỏi" (24/10), kết quả trên không dùng để quyết bật / không bật. Bài học: người viết bộ, người review plan, 2 người chấm đều không bắt lỗi này ⇒ phiên sau thêm bước bạn duyệt độ tự nhiên **trước** khi khoá bộ kín.
- **Làm lại bộ câu (E19):** Huế TRIPO vòng 4 (biểu mẫu lập kế hoạch, tab lưu trú / ăn uống / dịch vụ, bộ lọc, bản đồ) + 20 lượt hỏi thật trên diễn đàn VOZ 2023–2026 (E tự mở kiểm 3 chủ đề) ⇒ người thật kể hoàn cảnh trước, ràng buộc rải trong câu, hỏi kèm đi lại / chỗ ở / giờ tới, có ý né, viết tắt "3N2Đ" / "ko". Phát hiện: công cụ lịch trình chỉ hiểu 4 loại (số ngày, đi cùng ai, kiểu đi, sở thích) ⇒ bộ mới đo cả việc chatbot **nói thật phần không làm được**. Bạn duyệt giọng 8 câu mẫu (06/11); A chốt: bộ kín không có câu hai lượt, ≥ 2 / 5 câu có phần ngoài lịch. Hồ sơ `report_agent/2026-11-06_b5_cau_tu_nhien/e19_implementation.md`.
- **Sửa lỗi lịch trình bằng code (B171, nhánh `p9-b5-sua`, chưa vào chatbot):** (1) buổi sáng ưu tiên điểm hợp sở thích, câu giải thích "lấp chỗ trống" nói đúng sự thật; (2) người dùng xin buổi tối mà luật không xếp ⇒ code tự nối câu lý do + kiểm cuối bắt lời nói ngược. Review (C): kiểm (2) **bắt nhầm** 5 / 10 câu đúng ("Buổi tối: tự do") ⇒ đang sửa; thêm: câu "tối có … được không?" với người lớn tuổi ⇒ model từ chối cả lịch ⇒ A chọn code dựng lời lịch tối thiểu khi model từ chối. Tiền ≈ 0,018 USD.
- **Tối 06/11 — B171 (21:33 06/11/2026):** merge `dbb4004` vào `main`, cờ `lich_trinh` tắt; C review vòng 2 ready (`report_agent/2026-11-06_b5_cau_tu_nhien/b171_review.md` §8); tiền B171 ≈ 0,029 / 0,04 USD.
- **Tối 06/11 (21:03 06/11/2026):** B5b merge `db77f32` vào `main`, cờ tắt (không cần đưa lại lên `main` mới — `main` chỉ đổi tài liệu); cổng ổn định đạt (mục 1).
- **Thời tiết B5b:** review cả nhánh (C) bắt 1 lỗi lớn — 4 / 20 lượt câu dự báo hiện câu từ chối rồi ngay sau là bảng số ⇒ code thay bằng câu dẫn cố định (đo lại 0 / 4) — + 3 lỗi nhỏ, sửa xong, kiểm lại đạt. Tiền B5b ≈ 0,054 / 0,07 USD. Hồ sơ `report_agent/2026-11-02_phase_9_code/b168_b5b_implementation.md` §12–§13, `b168_b5b_review.md`.

### 05/11/2026 tối — Phase 9 B6: tra web khi kho không có — ĐẠT luật ghi trước, merge `7ff8e5a`, **BẬT 21:15 05/11/2026** (bạn duyệt)
- **Làm gì:** khi kho trả câu "không đủ thông tin" cho câu về Huế, code tra web một lần (Serper) ⇒ model viết mục **"Từ web (chưa kiểm)"** tách khỏi câu trả lời kho, có mã [w n] trỏ tới link; code kiểm: link phải nằm trong sổ kết quả tra, số tiền phải có trong đoạn trích, câu lưu trú 0 số tiền, câu thời gian thực (cúp điện, tuần này…) 0 chữ số / ngày giờ, câu thiên tai (lũ, lụt, bão, áp thấp…) ⇒ **không** chữ do model viết, chỉ câu cố định "xem nguồn chính thức / gọi 112" + link.
- **Đo:** bộ đã thấy ×2 — vòng đầu phạm 1 sàn (2 câu khẳng định thông tin chưa xác minh: lịch cúp điện, mức lũ) ⇒ vòng chỉnh 1 bằng **code** (luật thiên tai / thời gian thực) ⇒ đạt; kín ×2 đạt (0 / 7 khẳng định, 7 / 7 trả lời được); hồi quy: 0 câu từ chối nhầm thêm, 0 / 11 mục web nói "an toàn / được phép" sai; server thật + trình duyệt đạt. Review E 2 vòng bắt 2 lỗi code (link HTML thô lọt qua; thiếu "lụt" / "áp thấp") — đã sửa trước merge.
- **Giới hạn:** mục web tới sau **~13 s** (trung vị, kín) vì chờ kho từ chối ⇒ tra ⇒ viết; ~0,0018 USD / câu đường web; địa chỉ / số điện thoại trong mục web chưa kiểm là có trong đoạn trích; thêm "đang" vào luật thời gian thực sẽ chặn nhầm 1 câu đúng ⇒ chưa thêm. Tiền B6 ≈ 0,19 / 0,22 USD. **Bật 21:15 05/11/2026**; cổng sau khi bật (server thật, 3 câu tự viết): câu quán ăn kho không có ⇒ mục web 1 nguồn, 18,2 s, 0,0018 USD; câu "đang lụt" ⇒ câu cố định thiên tai, 9,1 s; câu giờ mở cửa kho có ⇒ không tra web, 3,1 s; log 0 chữ câu hỏi, 0 khoá. Hồ sơ `report_agent/2026-11-02_phase_9_code/b165_b6_implementation.md`, `b165_review.md`.

### 05/11/2026 tối — thử tắt ghi đệm của OpenAI (C202) — ÂM, giữ như cũ
- **Thử gì:** tham số `prompt_cache_options` chế độ `explicit` (không điểm ngắt) ⇒ OpenAI không ghi đệm, khỏi trả giá ghi đệm 1,25× cho phần đọc vào. Ý từ đo 02/11 (khi đó 0 lần đọc đệm). Tiêu chí ghi trước: 0 ghi đệm, cờ tắt giống byte, tiền / câu giảm, chữ đầu không chậm hơn.
- **Kết quả:** tắt ghi đệm được, nhưng tiền / câu **tăng** (0,000315 so với 0,000305 USD). Lý do (C đếm lại 78 lượt đã lưu, 0 USD): từ khi trợ lý tự tìm thêm (B2), **45 % lượt gọi model ≥ 2 lần** và **mọi lần gọi sau đều đọc lại đệm** của lần đầu ⇒ 81 % phần đọc vào tính giá đọc đệm rẻ. Ghi đệm lần đầu là cái giá để các lần sau rẻ; tắt đi đắt hơn ~21 % phần vào. Định tuyến vốn không ghi đệm (lời nhắc < 1.024 token).
- **Giữ như hiện nay.** Xét lại nếu tắt tìm thêm. Tiền thử 0,0031 USD. Hồ sơ `report_agent/2026-11-02_phase_9_code/c202_ghi_dem.md`.

### 05/11/2026 — Phase 9 B5c: tính tiền bằng code — ÂM hai vòng, dừng (nhánh lưu bằng tag `hoso/p9-b5c`, không vào `main`)
- **Làm gì:** câu chi phí ("2 người đi 3 ngày hết bao nhiêu", "vé Đại Nội cho 2 người lớn 1 trẻ em") ⇒ công cụ `tinh_tien`: **code** đọc bảng dự toán (tính cho một người) + bảng vé lẻ Quần thể trong kho, tự hỏi số người / ngày khi thiếu, tự nhân / cộng theo luật nhóm của kho, nối bảng có `[n]` + ngày nguồn; model chỉ viết lời, không nhận con số nào; code kiểm mọi số tiền trong chữ model.
- **Đạt:** phép tính khớp đáp án C tính tay **8 / 8**; câu ngoài phạm vi dữ liệu ra câu cố định 4 / 4; chuỗi gõ số người không bị hỏi lần hai; 62 câu thường không bị gọi nhầm công cụ, không rút lại nhầm.
- **Phạm (luật ghi trước ⇒ âm):** (1) câu giá vé một suất biểu diễn (giá có trong kho nhưng **ngoài** bảng vé lẻ) ⇒ luật "không tự viết số tiền" làm model bỏ luôn giá có nguồn ⇒ thiếu ý (lỗi thiết kế); (2) bộ an toàn: 1 câu về miễn giảm vé thiếu cảnh báo nhiều hơn bản đang chạy (1 / 3 ↔ 0 / 3; câu này không gọi công cụ — chỉ việc có thêm công cụ làm model tìm kho khác đi, giống B4b). Tiền ≈ 0,079 USD.
- **Vòng 2 (A quyết, thí nghiệm mới, không sửa kết quả cũ):** sửa (1) — ngoài bảng thì nêu giá có trong tài liệu kèm `[n]`; và **chỉ đưa công cụ khi code thấy dấu hiệu chi phí** ⇒ câu khác (gồm câu an toàn) gửi model **y hệt** bản đang chạy — chặn đúng kiểu lỗi (2). **Vòng 2 (14:20 05/11/2026) — âm:** câu không dấu hiệu chi phí gửi model y hệt bản đang chạy (21 / 32 câu an toàn) ⇒ sạch; Golden 30 sạch (câu giá vé biểu diễn nay nêu giá kho). Nhưng câu **miễn vé trẻ nhỏ khi nghe ca Huế** (có chữ "vé" nên được đưa công cụ) bỏ điều kiện chiều cao / ngồi cùng người lớn **3 / 3** lần ↔ bản đang chạy 1 / 3 ⇒ âm. Tổng tiền B5c ≈ 0,128 USD. **Dừng B5c** (lần thử thứ 3 thì dừng theo luật tự soi); hướng cho lần sau: **code nối dòng điều kiện miễn giảm** của bảng vé vào kết quả công cụ (điều kiện bắt buộc ⇒ code). Câu chi phí hiện vẫn đi như bản đang chạy (liệt kê giá có nguồn). Bài học chung (B4b, B5c): **mỗi công cụ thêm vào mọi câu đều làm đổi cách model trả lời câu an toàn** ⇒ công cụ nào chỉ cần cho một loại câu thì code bật theo loại câu (như B5b thời tiết). Hồ sơ: `report_agent/2026-11-02_phase_9_code/b162_b5c_implementation.md`.

### 05/11/2026 — Tốc độ #6: viết câu trả lời song song với định tuyến — ĐẠT, bật trên `main` (13:22 05/11/2026)
- **Đổi gì:** trước, định tuyến (~1,5 s) xong mới tìm kho + viết câu trả lời; nay đường stream chạy phần "trợ lý Huế" **cùng lúc** với định tuyến; định tuyến ra khẩn cấp / ngoài phạm vi / trò chuyện ⇒ bỏ phần đã chạy, trả đúng câu như trước.
- **Đo (04/11, luật ghi trước):** chữ đầu câu về Huế nhanh hơn trung vị **1,37 s** [0,34; 2,14] (15 / 20 cặp nhanh hơn; hôm đo provider chậm: p50 5,36 ⇒ 3,53 s, p95 8,69 ⇒ 7,72 s — vẫn trên sàn 3 / 5 s); an toàn 90 lượt 0 vi phạm, khẩn cấp không đổi (1,83 ↔ 1,80 s); 228 / 228 chuỗi gửi model giống byte cả cờ tắt lẫn bật. Review (B) 2 vòng đạt — vòng 1 bắt lỗi mất trường nút bấm khi đưa lên bản có B4b / B5, đã sửa + test.
- **Đánh đổi:** câu không về Huế tốn thêm một lần viết bị bỏ (~+0,00023 USD; cả câu ≈ 0,0003 ≤ 0,0005); câu khẩn cấp / ngoài phạm vi cũng gửi kèm đoạn kho tới OpenAI. Cổng `main` (13:22 05/11/2026): câu về Huế chữ đầu 2,75 s · câu khẩn cấp ra đúng câu soạn sẵn · câu ngoài phạm vi đúng · log không có chữ câu hỏi. Hồ sơ: `report_agent/2026-11-02_phase_9_code/c172_toc_do_song_song.md`, `c172_review.md`.

### 05/11/2026 — Phase 9 B5: gợi ý lịch trình — đạt sàn máy, code vào cờ tắt (merge `d66f6a3`), chờ bạn chấm
- **Làm gì:** câu "lên lịch Huế 2 ngày…" ⇒ trợ lý gọi công cụ `lich_trinh`: **code** chọn điểm từ bảng 28 điểm bạn duyệt (cột tên khác), xếp theo buổi (≤ 2 cụm / ngày, buổi cấm theo người đi cùng), gắn giờ có nguồn, dựng link Google Maps; thiếu số ngày ⇒ **code** bật thẻ hỏi lại (không lời dặn thêm); "Trả lời luôn" ⇒ tạm 1 ngày + dòng giả định; model chỉ viết lời theo khung; **code kiểm cuối** (điểm ngoài khung, giờ ngoài tập, giá, trích dẫn) — sai ⇒ rút lại + "Thử lại"; giao diện hiện dòng tiến độ **chỉ bước code đã làm** + nút "Sửa".
- **Đo:** đã thấy 13 câu gọi công cụ 10 / 10, kiểm cuối 0 lỗi, ngoài Huế từ chối 3 / 3; kín 5 câu gọi công cụ 5 / 5, nội dung 0 điểm ngoài khung (1 / 5 bị rút lại **nhầm** — bộ kiểm tưởng tên điểm nhắc trong câu lịch sử là điểm thêm ⇒ sửa B5.1 bằng câu tự viết; review bắt 5 kẽ hở của bản sửa ⇒ sửa tiếp, thử thêm 5 kẽ hở mới đều bắt); hồi quy Golden 30 sạch (theo dõi: 1 câu từ chối mới), an toàn 32 thủ tục kiểm lại **đạt** (bản mới ≤ bản đang chạy ở mọi câu). Theo dõi: qua server 1 / 4 câu lịch bị rút lại (model ghi sai số nguồn — kiểm cuối bắt đúng). Tiền ≈ 0,104 USD. Review cả nhánh (C) 2 vòng đạt.
- **Cập nhật 06/11:** bộ kín này bị gác (câu không tự nhiên) — xem mục 06/11 ở trên. Hồ sơ: `report_agent/2026-11-02_phase_9_code/b160_b5_implementation.md`, `b160_review.md`.

### 04–05/11/2026 — Phase 9 B4: trợ lý hỏi lại người dùng — ÂM hai vòng, code vào với cờ tắt (merge `b019aab`)
- **Thử gì:** câu lịch trình / chi phí thiếu số ngày, số người ⇒ trợ lý gọi công cụ `hoi_lai` ⇒ giao diện hiện thẻ có nút chọn ⇒ người dùng bấm ⇒ câu đủ ý đi đường trả lời thường. Câu chi phí theo **Cách A** (bạn chọn 03/11): liệt kê giá có nguồn, không cộng tổng — dặn bằng lời trong lời dặn.
- **Vòng 1 (khoá 3, 04–05/11) — âm:** hỏi lại đúng đạt (đã thấy 8 / 10, kín 4 / 5), câu đủ không bị hỏi thừa, 60 câu thường không bị hỏi sai chỗ, 30 câu Golden không ảnh hưởng. **Phạm:** (a) 1 / 2 câu chi phí kín, sau khi chọn "2 người", trợ lý **tự ghi dòng "Tổng"** bằng số tự tính (phép ×2 khớp luật kho — bảng tính cho một người — nhưng luật đo cấm con số tổng); (b) người dùng **gõ** "3 người, đi 3 ngày" thay vì bấm ⇒ bị hỏi lại lần nữa (4 / 4 lần). Kết luận: lời dặn không giữ được model khỏi tự tính.
- **Vòng 2 (B4b, bạn chọn "Tách — giữ lịch trình", khoá `990825e`) — âm:** chỉ hỏi lại câu lịch trình. Đạt: lịch trình đã thấy 4 / 5, kín 3 / 3; câu chi phí không bị hỏi 0 / 12; câu đủ 0 / 10; 60 câu thường 0 / 60; Golden 30 sạch; an toàn các lượt ghép 0 ý sai giá / giờ / điều kiện. **Phạm:** bộ an toàn 32 câu — **2 câu mới bị chấm "thiếu cảnh báo"** (ngưỡng ≤ 1) ⇒ thủ tục kiểm lại ghi trước (mỗi câu 3 lần bản mới ↔ 3 lần bản đang chạy, 2 judge chấm mù): bản mới thiếu nhiều hơn ở cả hai câu (2 / 3 ↔ 1 / 3; 3 / 3 ↔ 2 / 3) ⇒ âm. Giới hạn: mỗi bên chỉ 3 lần, chênh 1 lần mỗi câu, bản đang chạy cũng thiếu 3 / 6 ⇒ không chứng minh tệ hơn, cũng không loại được. **Giả thuyết** (chưa chứng minh): đoạn dặn "khi nào hỏi lại" thêm vào lời dặn **mọi** câu làm model lơ phần cảnh báo (1 câu: bản mới tìm thêm 3 / 3 lần, câu trả lời ngắn hơn).
- **Bạn chọn (05/11): "Merge cờ tắt + code tự hỏi"** ⇒ code vào `main` với `hoi_lai: false` (sau đó B5 gỡ hẳn công cụ này, khoá `hoi_lai` không còn trong cấu hình) (cổng: 228 câu giống byte, test 64 đạt, câu thật trong / ngoài kho đúng, log không chứa câu hỏi); **B5** dùng lại thẻ + nút, nhưng **code** quyết hỏi khi công cụ lịch trình thiếu số ngày (khung AI FDE: trường bắt buộc ⇒ code). Câu chi phí ⇒ **B5c tính tiền bằng code**.
- Tiền: vòng 1 ≈ 0,205 · vòng 2 ≈ 0,088 USD. Hồ sơ: `report_agent/2026-11-02_phase_9_code/b144_b4_implementation.md` (§2e–§2g), review nhánh `b157_b4b_review.md`; plan `docs/superpowers/plans/2026-11-03-phase-9-b4-plan.md` bản 8.

### 04/11/2026 — thử tắt suy luận ở bước định tuyến (thí nghiệm tốc độ #1) — ÂM, không áp dụng
- **Thử gì:** bước định tuyến (chọn trò chuyện / về Huế / ngoài phạm vi / khẩn cấp) chạy `gpt-6-luna` với mức suy luận "none" thay mặc định. Luật ghi trước: không câu khẩn cấp, không câu an toàn nào đổi tuyến sai; đạt mới đo chữ đầu.
- **Kết quả:** 123 câu × 2 lượt + 50 lượt có lịch sử: khẩn cấp đúng hết, nhưng **2 câu an toàn về Huế bị xếp "ngoài phạm vi"** (một câu 2 / 2 lượt, một câu 1 / 2; bản hiện tại đúng 2 / 2) ⇒ phạm sàn ⇒ bỏ, chữ đầu không đo (NOT RUN). Theo dõi: định tuyến trung vị 1,7 ⇒ 1,3–1,5 s, tiền / lần −16 %. Giả thuyết (chưa chứng minh): phần suy luận giúp phân biệt câu an toàn về Huế với câu ngoài phạm vi. Tiền 0,057 USD. Review B155 đạt. `report_agent/2026-11-02_phase_9_code/c156_toc_do_dinh_tuyen.md`; code giữ bằng tag `hoso/p9-toc-do-1`.

### 04/11/2026 — dòng mở câu khẩn cấp soạn sẵn (merge `4e3cb4e`)
- **Đổi gì:** chỉ dòng mở của câu khẩn cấp thành "Nếu bạn hoặc người bên cạnh đang gặp nguy hiểm **hoặc vừa gặp chuyện (bị cướp, tai nạn, cháy, ốm nặng)**, hãy gọi ngay số khẩn cấp (miễn phí):"; 4 dòng còn lại (4 số, "nói rõ bạn đang ở đâu", "không gọi hộ được", dòng tiếng Anh) giữ nguyên. Bạn chọn PA1 trong 3 phương án chữ (C162). Không đổi định tuyến.
- **Kiểm:** test khoá đủ 5 dòng (12 / 12 đạt); định tuyến không đổi ⇒ dùng lại đo hôm nay (mốc thí nghiệm tốc độ: 24 / 24 câu khẩn cấp + 6 / 6 lượt có lịch sử vào đúng nhánh khẩn cấp cả 2 lượt); cổng `main` (A): câu tự viết "vừa bị giật túi xách" ⇒ chữ mới; câu trong kho ⇒ trả lời có nguồn; câu ngoài kho ⇒ từ chối (≈ 0,001 USD). Review C168 đạt (`report_agent/2026-11-02_phase_9_code/b154_review.md`).

### 03/11/2026 tối — sửa an toàn định tuyến khẩn cấp (merge `e3cdb96`)
- **Phát hiện** khi đo mốc cho thí nghiệm tốc độ (luật dừng "mốc phạm sàn khẩn cấp"): câu tự viết "vừa bị giật túi xách có hộ chiếu, báo công an ở đâu" đi trợ lý thường ⇒ câu từ chối, không có số 113. Bộ 10 câu khẩn cấp tự viết (02/11) chưa từng vào bộ đo định tuyến ⇒ lỗ hổng có từ B1 (sáng 03/11). Ca cùng loại trên lời dặn cũ chỉ đúng 4 / 6 ⇒ lỗi theo loại, không riêng một câu.
- **Sửa:** chỉ dòng định nghĩa `khan_cap` trong lời dặn định tuyến — thêm "vừa bị cướp / giật / trộm / móc túi / hành hung / đe doạ, cần báo công an — dù việc đã xảy ra"; không luật từ khoá, không đổi câu soạn sẵn. Luật ghi trước đạt hết (mục 3). Cổng `main` (A): câu đó ⇒ câu khẩn cấp; câu thường ⇒ trả lời có nguồn. ≈ 0,042 USD. `report_agent/2026-11-02_phase_9_code/b143_khan_cap_implementation.md`, `b143_review.md`.
- **Còn mở:** ~~câu soạn sẵn chưa sát người vừa bị giật đồ~~ (đã sửa 04/11, mục trên); định tuyến quá 10 s ⇒ đi trợ lý thường — nếu rơi vào câu khẩn cấp sẽ mất câu soạn sẵn (hiếm: 1 / 246 lần, câu ngoài phạm vi).

### 03/11/2026 tối — nút 👍 / 👎 + gợi ý dưới câu ngoài phạm vi (merge `6817897`)
- Từ nghiên cứu sản phẩm thật (Tokyo EDO có nút báo sai; Huế TRIPO không có). Bạn chọn "chỉ lưu đánh giá". B code, C review 0 finding (mã lượt ngẫu nhiên riêng, không lộ mã cuộc; lượt lỗi / rút lại không có mã), cổng trên `main` (A) đạt. Tiền ≈ 0,002 USD. `report_agent/2026-11-02_phase_9_code/b142_phan_hoi_implementation.md`.

### 03/11/2026 tối — Phase 9 B3b: nhớ hội thoại bật (merge `9e2ecd9`)
- **Vòng 1** (câu dặn "nhận định chỉ từ đoạn nói đúng đối tượng", nhớ cả câu trả lời): đã thấy đạt mọi sàn nhưng **hỏi tiếp +0,50 [−0,15; +1,20] — không đạt luật** (cận dưới phải > 0) ⇒ đường kết quả âm ghi trước:
- **Vòng (a) — chỉ nhớ câu hỏi** + câu dặn: đã thấy nhớ tên 6 / 6, hỏi tiếp **+0,80 [+0,25; +1,50]**, 0 câu ngoài kho bị trả lời, 0 đảo cảnh báo ⇒ đạt; **bộ chuỗi mới** (C viết, B không xem; 12 chuỗi nhắm đúng lỗi): bên có nhớ **từ chối đúng 6 / 6** lượt bẫy (bên không lịch sử dính 3 / 6), từ chối nhầm 0 / 19 ↔ 5 / 19 ⇒ **bật** (bạn chọn "đạt ⇒ bật"). Review C154 `ready`. Tiền B3 + B3b ≈ 0,47 USD (trần 0,50).
- **Giới hạn:** bộ mới chỉ 6 lượt bẫy; chưa thấy ca "bác tiền đề bằng đúng nguồn"; không nhớ câu trả lời ⇒ câu "ý thứ hai bạn vừa nói…" chưa hỗ trợ; cookie hết 30 phút thì âm thầm bắt đầu cuộc mới. `report_agent/2026-11-02_phase_9_code/b138_b3b_implementation.md`.

### 03/11/2026 tối — Phase 9 B3 vào chatbot (merge `a3dabba`), nhớ hội thoại tắt (đã bật ở B3b)
- **Phần kín** (C chạy 15 chuỗi, 3 bên, 0,032 USD): nhớ tên 4 / 4 (cộng 10 / 10, sàn ≥ 9); hỏi tiếp có nhớ ↔ câu gõ không lịch sử +0,60 [0,00; +1,40] (luật: không ngược chiều — đạt); câu điều kiện 0 đảo cảnh báo; đổi chủ đề tụt 0. **Câu ngoài kho: 1 / 2 lượt bên có nhớ bị trả lời** — chạy lại có lưu ngữ cảnh: bot mượn đoạn của **đối tượng khác** để trả lời câu hỏi tiếp mang tiền đề sai (hai bên không lịch sử từ chối đúng) ⇒ sàn phạm ⇒ **cờ nhớ không bật** (luật ghi trước). Lúc đầu nghi nhãn bộ đo sai — kiểm có ngữ cảnh bác bỏ.
- **Bạn chọn (18:31 03/11/2026):** merge code + giao diện với nhớ tắt; vòng sửa **B3b** — C viết bộ chuỗi mới nhắm đúng loại lỗi (B không xem), B thêm một câu vào lời dặn đường có lịch sử ("mỗi ý về một đối tượng phải từ đoạn nói đúng đối tượng đó"), đo lại; đạt ⇒ bật. Trần B3 0,40 ⇒ 0,50 USD.
- **Giao diện nhiều lượt + cổng:** Playwright server thật đạt (CSP 0, ngoài 0); cổng có nhớ bật trên bản sao cấu hình (cookie thật, "cuộc mới" xoá nhớ, log 0 nội dung) đạt; câu gợi ý "tháng này…" đổi thành câu không cần ngày hôm nay (A quyết). Cổng sau merge trên `main` (A): `/` 200, `/health` 5 / 5, 1 câu trong kho (6 nguồn) + 1 câu ngoài phạm vi đúng, log +2 dòng, 0 chữ câu hỏi. Tiền B3 ≈ 0,30 USD.

### 03/11/2026 chiều — Phase 9 B3 (nhớ hội thoại) thử trên nhánh `p9-b3`
- **Câu dặn mới chống "thêm lời khuyên chung"** (sửa lỗi an toàn của B2): bản 1 "chỉ nêu điều có trong bằng chứng…" sửa được lỗi nhưng **trượt** sàn từ chối nhầm (4 ⇒ 7) + đọc chữ thấy mở "Có." rồi nói ngược, bỏ lời khuyên có nguồn ⇒ **bản hẹp** (chỉ chặn lời khuyên / lưu ý an toàn không có nguồn, giữ lời khuyên có nguồn) **đạt cả 5 luật**: từ chối nhầm 4, Đủ / Đúng không tụt, 0 câu sai điều kiện, câu an toàn của B2 hết lỗi ⇒ **giữ** (≈ 0,19 USD cả hai vòng).
- **Nhớ hội thoại** (đo 25 chuỗi đã thấy): nhớ tên 6 / 6; câu hỏi tiếp có nhớ ↔ gửi câu gõ không lịch sử: đủ ý **+0,65** [+0,15; +1,25]; 0 câu ngoài kho bị trả lời; đổi chủ đề 0 câu tụt. Còn: phần kín, cổng ổn định, giao diện nhiều lượt (Bản 1 bạn chọn) ⇒ mới bật.
  `report_agent/2026-11-02_phase_9_code/b136_b3_implementation.md`.

### 03/11/2026 trưa — Phase 9 B2 vào chatbot (merge `00d670e`)
- **B2a — model viết lại câu tìm đầu** (3 cách, 2 lượt × 61 câu, ≈ 0,069 USD): không cách nào qua luật ⇒ **không giữ**, tìm bằng câu gốc (`06_BAO_CAO_TIM_KIEM.md` mục 4).
- **B2b — trợ lý tự gọi `tim_kho` thêm ≤ 2 lần** (luật ghi trước; nhiễu đo bằng 2 lượt của chính đường công cụ): đủ ý câu nhiều nguồn +1,17, Golden không tụt quá nhiễu, 0 câu ngoài kho bị trả lời ⇒ **giữ**;
  1 câu an toàn sai mới thật (2 / 3 lần sinh lại, bản cũ 0 / 3) — bạn chọn giữ + sửa lời dặn ở B3 (11:16 03/11). Cổng ổn định: 2 ca ngắt thật (giữa vòng công cụ / giữa chữ), log đúng. Review C137 + C141 `ready`. Tiền B2 ≈ 0,255 USD.
  `report_agent/2026-11-02_phase_9_code/b134_b2_implementation.md`, `b134_review.md`.

### 03/11/2026 — Phase 9 B1 vào chatbot (merge `f01c032`)
- **B131 hoàn tất + review C134** (`ready`, 0 blocker / 0 major): bộ an toàn 32 câu — lần gọi trả lời giống từng byte bản trước ⇒ dùng lại kết quả 01/11; sửa log khi người dùng ngắt giữa chừng (đóng lõi trước rồi mới ghi, +1 test); bật mặc định định tuyến + dòng nhắc;
  cổng ổn định 2 ca ngắt thật; chữ đầu 10 câu (mục 1). 0,0029 + 0,0006 USD · **giữ** · `b129_b1_implementation.md` §4b, `b129_review.md` "Vòng cuối".
- Lưu ý đo (C134 m-3): `evaluation generate` không truyền `--flags` nay chạy theo `settings.yaml` (có định tuyến) ⇒ muốn đo đường RAG 1–8 thuần phải truyền `--flags` rỗng.

### 02/11/2026 tối — Phase 9 (B0 vào chatbot; B1 đo xong phần lớn — vào chatbot 03/11)
- **B0** (merge `1c10111`): một lõi `assistant.py`, `tim_kho`, log USD + ms mỗi lần gọi model · câu trả lời không đổi (giống byte) · **giữ** · `report_agent/2026-11-02_phase_9_code/b127_*`.
- **Câu khẩn cấp, chatbot hiện tại** (10 câu tự viết, 0,0025 USD): 10 / 10 chỉ từ chối, không chỉ số gọi · **bạn: lỗi** ⇒ B1 trả câu soạn sẵn 113 / 114 / 115 / 112 (số kiểm nguồn chính thức) · `c122_khan_cap_buoc0.md`.
- **B1, nhánh `p9-b1`** (luật ghi trước, phần kín do C giữ; ≈ 0,142 USD): **định tuyến** 4 tuyến đúng 253 / 253 đã thấy + 20 / 20 kín ⇒ **bật**; dòng nhắc "có thể đã thay đổi" (vé / nơi / lễ hội) ⇒ **bật**;
  **luật từ khoá khẩn cấp**: đã thấy 14 / 14, kín **0 / 8 + chặn nhầm 2 / 8** ⇒ **bỏ** (câu khẩn cấp vẫn ra câu soạn sẵn nhờ định tuyến bắt 10 / 10 kín; thêm 1 lần gọi phân loại);
  **dòng ngày hôm nay**: từ chối nhầm 5,0 ⇒ 4,5 (cần giảm ≥ 3) ⇒ **bỏ** (gốc ở tầng tìm / model, như 30/10). Hồi quy 176 câu: sàn đạt, từ chối nhầm 12 = 12; Đủ 6 câu tụt (ngưỡng 5) nhưng lần gọi trả lời giống byte
  bản cũ ⇒ coi là nhiễu, dùng lại số cũ (spec §4). **Tốc độ:** định tuyến thêm ~1,7 s (p95 2,7 s) mỗi câu ⇒ chữ đầu có thể vượt 5 s — chỉ theo dõi (chất lượng trước). Merge 03/11.
  `b129_b1_implementation.md`, `b129_review.md`, `c131_kin_b1.md`.

### 30/10/2026
- **Câu hỏi theo ngày tương đối** (15 câu tự viết + 11 câu bộ an toàn, 2 người chấm Claude không biết ngày chạy; 0,0037 USD): 0 câu tự đoán ngày rồi nói chắc,
  0 câu tính sai thứ / âm lịch; nhưng 6 / 14 câu có trong kho bị từ chối, cùng thông tin hỏi không kèm ngày thì trả lời đúng. **Bạn quyết (14:44):** không sửa prompt ở
  Phase 8; Phase 9 thêm công cụ "hôm nay là ngày nào", bộ câu này làm mốc. `report_agent/2026-10-27_phan_ton_phase_cu/ngay_hien_tai_implementation.md`.
- **Đếm lại lỗi trích dẫn** trên mọi lượt đo đã lưu (0 USD): bản đang chạy 0 / 489 lần sinh; bản 5 đoạn cũ 2 / 528. Lỗi còn lại chỉ là câu không gắn `[n]` nào, chỉ
  biết khi câu đã viết xong ⇒ căn cứ cho streaming "hiện chữ trước, kiểm cuối". `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md` §8.2.
- **Giá đủ của `gpt-6-luna` (đo 30/10, trước khi có tìm thêm):** mỗi câu bị tính giá **ghi đệm** cho gần hết phần đọc vào, không được giảm giá đọc đệm ⇒ tiền thật ≈ 0,00025 USD / câu (từ Phase 9 B2, các lần gọi sau trong cùng câu đọc lại đệm — xem thử 05/11 tối ở mục 4), công cụ đo ghi
  thiếu ≈ 20 %; mọi số USD cũ trong báo cáo này đếm theo giá phẳng. Sửa công thức: việc đóng gói Phase 1–8. `Project_Status.md` §5 (30/10 15:07).

### 28/10/2026
- **Đưa 10 đoạn + chuẩn hóa NFC vào chatbot** (merge `510e1a8`): bạn chọn đưa vào theo người chấm Claude, đọc cặp mù làm sau. Kiểm trên `main`: 51 test đạt, kết quả
  tìm 158 câu giống từng byte, câu gõ dấu tách rời cho đúng ngữ cảnh như câu thường, chạy thật 2 câu đạt (≈ 0,0004 USD). **Giữ.**
  `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_merge_implementation.md`.
- **Đo thử "chữ đầu tiên" nếu có streaming** (đo trong script, chưa trên trình duyệt; 7–8 câu tự viết, phần lớn trả lời dài): chữ đầu hiện sớm hơn lúc xong câu
  ~**1,9 s** (trung vị); tới chữ đầu p50 2,4 / p95 4,8 s, so với chờ đủ câu 4,6 / 7,6 s ⇒ lý do làm streaming.
  `report_agent/2026-10-27_phan_ton_phase_cu/streaming_ttft_implementation.md`.

### 27/10/2026
- **Thời gian chờ thật qua API** (22 câu tự viết, bản 5 đoạn lúc đó): trung vị 3,3 s / p95 5,7 s tuần tự; ~98 % là lúc model viết (tăng theo số chữ model viết ra: ≈ 11,5 ms mỗi token, tương quan 0,97 — `report_agent/2026-10-26_cai_tien_tung_khau/c58_latency_theo_khau.md`), tìm ~40 ms, dựng ngữ cảnh ~2 ms;
  thời gian viết đi theo số token viết ra. Số này của cấu hình cũ — số hiện hành ở mục 1. `report_agent/2026-10-26_cai_tien_tung_khau/b65_latency_dau_cuoi.md`, `c58_latency_theo_khau.md`.
- **API ghi số đo mỗi câu** (bạn duyệt; merge `5100b90`): một dòng log mỗi lần hỏi, không chứa câu hỏi. **Giữ.** `report_agent/2026-10-26_cai_tien_tung_khau/c59_log_token_implementation.md`.
- **Trả lời ngay, không suy luận** (mốc 10 đoạn): một câu lẽ ra phải từ chối bị trả lời vòng ⇒ phạm sàn, dừng ở 24 câu (0,0049 USD); lợi nhỏ (token viết ra ~0,72×,
  tiền ~0,94–0,97×). **Bỏ.** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r1_plan.md`.
- **Model chọn 10 / 30 đoạn rồi mới trả lời** (120 câu thử): đủ ý +0,22, đúng +0,25 trung bình, từ chối nhầm 7 → 2 / 88, nhưng **5 câu đủ ý tụt** > 4 cho phép ⇒ kém
  hơn theo luật; chờ p50 6,5 / p95 9,1 s, tiền ×3,8 (0,0749 USD). **Bỏ.** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3b_m_answer_review.md`.
- **Sai số liệu trong câu trả lời** (đo hiện trạng, 0 USD): 0 / 68 câu có số bị thấy sai (máy nghi 4 câu, đều là phép tính đúng). Không cần rào chặn lúc này.
  `report_agent/2026-10-26_cai_tien_tung_khau/c48_so_trong_cau_tra_loi.md`.
- **Luật kiểm sau sinh chặn "trả lời vòng"** (0 USD): không tách được câu lạc đề với câu trả lời một phần có ích (7 / 10 cờ là câu có ích). **Bỏ.**
  `report_agent/2026-10-26_cai_tien_tung_khau/c51_kiem_sau_sinh_kha_thi.md`.
- Bạn chốt đợt cải tiến từng khâu: không cách nào vào chatbot. Tổng hợp: `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`.

### 26/10/2026
- **Phân loại lỗi** (88 câu, mốc 10 đoạn): 10 câu kém đều thiếu thông tin trong 10 đoạn; model không bịa. `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_C.md`.
- **Trả lời phần có căn cứ, chữ prompt siết hơn:** vẫn trả lời 1 / 12 câu ngoài kho ⇒ dừng ngay bước đầu (0,0027 USD). **Bỏ.**
- **Nêu đủ chi tiết:** không chạy (chỉ 6 câu đổi được). **Thước kiểm số liệu có trong nguồn:** chỉ dùng chọn câu đọc lại. `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r3_plan.md`, `phase_8_2_r4_implementation.md`.

### 25/10/2026
- **API báo đúng loại lỗi** (rà code): một module bị nạp hai lần làm Qdrant lỗi ra 500 thay 503, kho đổi ra 503 thay 409 ⇒ sửa về một cách import, chạy mọi lệnh từ
  `backend/`. **PASS.** `report_agent/2026-10-25_ra_soat_code/TONG_HOP.md`.
- **Lỗi trích dẫn `[Nguồn n]`:** model đôi khi trích đúng nhãn ngữ cảnh "[Nguồn n]", bộ kiểm chỉ hiểu "[n]" ⇒ người dùng nhận 500. Sửa: nhận cả hai dạng, đổi về `[n]`.
  Trên 1.600 câu đã sinh: lỗi 69 → 14, 0 câu đạt bị đổi. **PASS, giữ.** Số "lỗi trích dẫn" trước ngày này đếm theo bộ kiểm cũ.
- **Phase 8.1 — thử 5 cách trả lời** (120 câu thử, chấm mù bằng Claude, so theo cặp; "tốt hơn" phải xác nhận trên 56 câu kiểm; 0,157 USD):

  | Cách | Điểm Đủ (thử) | Rào chắn | Kết luận |
  |---|---|---|---|
  | **10 đoạn ngữ cảnh** | **+0,26** | đạt; tiền ×1,5 | **tốt hơn**, bộ kiểm +0,27 ⇒ **đã đưa vào 28/10** |
  | Xếp 5 đoạn gom theo tài liệu | −0,02 | đạt | không khác ⇒ bỏ |
  | Prompt "trả lời phần có căn cứ" | +0,11 | trả lời 2 câu ngoài kho | kém hơn ⇒ bỏ |
  | Prompt thêm 2 luật cũ | 0,00 | đạt | không khác ⇒ bỏ |
  | Mức suy luận `none` / `low` / `high` | +0,14 / +0,02 / +0,02 | `none`, `low`: lỗi trích dẫn tăng (đếm theo bộ kiểm cũ) | không dùng; `none` thử lại 27/10 vẫn kém |
  | "Một nguồn thì gán nguồn đó" | — | — | 0 câu đổi ⇒ bỏ |

  Đính chính: chẩn đoán 7B "4 / 22 câu có đủ bằng chứng mà vẫn từ chối" (theo từ khóa) — đo bằng đoạn đúng thì **0 câu**. `report_agent/2026-10-24_phase_8_1_ra_soat/TONG_HOP.md`.

### 24/10/2026 và trước
- **Phase 7B — mốc 176 câu** (5 đoạn): Đúng / Đủ / Trúng ý 4,43 / 4,28 / 4,45; từ chối đúng 18 / 18 câu ngoài kho; từ chối nhầm 22 / 158; lỗi trích dẫn 4 / 176
  (bộ kiểm cũ); ~0,024 USD. `reports/phase_7b_false_refusal_diagnosis_2026_10_24.md`.
- **Dọn code sau Phase 7:** gỡ đường sinh câu trả lời bản món ăn (đã hỏng: gửi `temperature` ⇒ lỗi 400) cùng code / test món ăn; đường toàn kho không đổi.
  `reports/phase_7_cleanup_inventory_2026_10_24.md`.
- **23/10 — đóng Phase 6 trên `gpt-6-luna`:** 5 câu thật, 4 đạt / 1 không (câu giá vé + miễn giảm: không tìm ra bảng giá); câu nhiều nguồn đạt nhưng chỉ dùng 1 nguồn.
- **Đổi model sinh:** Qwen 3.5-9B (OpenRouter) → `gpt-5.4-nano` → `gpt-6-luna` (23/10). Hai model đầu **đã bỏ**.
  `docs/superpowers/specs/2026-10-23-phase-6-gpt-6-luna-amendment.md`.

## 5. Hôm nay còn đúng không

Bảng lập 31/10 (code `main` `1985a81`), thêm dòng tới 14/11 (cờ 14/11 kiểm với `settings.yaml` trên `main` `e0cb02e`). **Cờ, route và file trong cột trạng thái kiểm lại 10/11/2026** với `backend/config/settings.yaml`, `backend/api/` và `session_prompt/Project_Status.md` §4 (code `main` `1bcc830`); số dòng code (file:dòng) ngoài `settings.yaml` chưa kiểm lại, có thể lệch vài dòng.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| API `POST /api/chat`, trả `{answer, sources}`, câu hỏi 1–500 ký tự | **còn dùng** | `backend/api/routes/chat.py:36–38,48–50,60` |
| Model sinh `gpt-6-luna`, không gửi mức suy luận | **còn dùng** | `settings.yaml:48`; `generator_openai_full_corpus.py:98–99,120` |
| Tối đa 10 đoạn, ngân sách 16.384 token (thay 5 đoạn từ 28/10) | **còn dùng** — B0 01/11: bạn giữ 10 | `settings.yaml:53,56`; `core/settings_loader.py:69–76` |
| Chuẩn hóa NFC câu hỏi trước khi tìm | **còn dùng** (từ 28/10) | `backend/retrieval/full_corpus.py:97–102` |
| Prompt "thiếu bằng chứng thì từ chối cả câu" | **còn dùng** | `full_corpus_prompt.py:14` |
| Kiểm trích dẫn nhận cả `[n]` và `[Nguồn n]` | **còn dùng** (từ 25/10) | `citations.py:11–16`; `chat.py:177–188` |
| Ghi `chat_metrics` mỗi câu, không ghi nội dung | **còn dùng** (từ 27/10); **từ B0 02/11 ghi thêm** `route`, `usd`, `n_llm_calls`, `llm_calls`, `tools` (trước đó không ghi USD) | `chat.py:38–45,216`; `generator_openai_full_corpus.py` `CallLog` |
| Câu bị ngắt giữa stream, hoặc `/api/chat` lỗi sau khi model đã trả lời: `usd` ghi rỗng (có tốn tiền thật) | **sửa ở B1** (03/11): log ghi sau khi đóng lõi, có `llm_calls`; lần gọi bị huỷ giữa chừng vẫn không có usage ⇒ `usd` lượt đó hơi thấp hơn thật | `b127_review.md`, `b129_review.md` |
| Trợ lý tự gọi tìm thêm ≤ 2 lần (`tim_them`) | **còn dùng** (từ 03/11 trưa, merge `00d670e`); câu tìm đầu vẫn là câu gốc | `backend/llm/assistant.py` `tool_for_turn`; `settings.yaml` `tim_them` |
| Hết lượt tìm thì dừng (`het_luot_bo_cong_cu`) | **còn dùng — BẬT từ 13/11** (merge `cd1f6ef` 12/11 cờ tắt; bật `9d6a0f7`, User: bật kèm theo dõi câu kho thiếu bị trả lời bằng kho, ≥ 1 câu bịa ⇒ tắt): sau 2 lần model tìm thật, lượt gọi kế không còn `tim_kho`; đo 12/11: 8 / 8 câu kho thiếu bớt ≥ 1 lượt gọi, trung vị cả câu 22,85 ⇒ 16,15 s; 3 câu bớt từ chối, 0 / 6 bịa (mẫu nhỏ) | `backend/llm/assistant.py`, `llm/generator_openai_full_corpus.py`; `report_agent/2026-11-12_ra_khoang_cach/b_het_luot_tim_implementation.md`, `c_review_bat_co_het_luot.md` |
| Công cụ hỏi lại `hoi_lai` cho model + thẻ nút | **công cụ đã gỡ** ở B5 (05/11; B4 âm hai vòng) — `settings.yaml` không còn khoá `hoi_lai`; chỉ còn thẻ nút do **code** bật khi lịch trình câu gõ thiếu số ngày (cờ `lich_trinh` tắt ⇒ người dùng không thấy) | `backend/llm/hoi_lai.py` (danh sách trường + dữ liệu nút); `settings.yaml` dòng `lich_trinh` |
| Giao diện hiện số `[n]` bấm được trong chữ | **đã thay** 07/11 bởi dòng "Nguồn" (cổng đợt 1, merge `dbfc925`) | `frontend/src/markdown.js` `renderAnswerHtml`, `chat.jsx` `SourceLine` |
| Công cụ thời tiết `thoi_tiet` | **còn dùng — BẬT từ 07/11** (`0dab4e5`) | `settings.yaml` `thoi_tiet: true`; `backend/llm/thoi_tiet.py` |
| 4 API chỉ đọc của cổng (`/api/kham_pha`, `/api/kham_pha/bai`, `/api/thoi_tiet`, `/api/tinh_nang`) | **còn dùng** (từ 07/11) | `backend/api/routes/cong.py` |
| Đường biểu mẫu `bieu_mau` | **còn dùng — BẬT từ 07/11** (`lich_trinh_bieu_mau: true`); **từ 14/11 đi bản 2** (`len_ke_hoach_v2: true`: `lich_trinh_v2.xep_v2` + `len_ke_hoach.stream_v2`); cờ tắt ⇒ API 404, giao diện ẩn | `backend/api/routes/chat.py` `_bieu_mau_off`; `backend/llm/len_ke_hoach.py`; `settings.yaml:73,79` |
| Sửa lịch bằng lời `sua_lich_v2` | **còn dùng — BẬT từ 14/11** (`e0cb02e`); cần `len_ke_hoach_v2` | `backend/llm/sua_lich_v2.py`; `len_ke_hoach.py` `hieu_va_ap` / `stream_sua` / `luu_sau_luot`; `assistant.py` `answer_turn_stream_parallel`; `api/conversations.py` `luu_lich`; `settings.yaml:83` |
| Ảnh từng điểm lịch `anh_lich` | **còn dùng — BẬT từ 14/11** | `settings.yaml:82`; `frontend/public/anh/lich/` |
| Định tuyến 4 tuyến trước khi trả lời; dòng nhắc "có thể đã thay đổi" | **còn dùng** (từ 03/11, merge `f01c032`); dòng ngày hôm nay: code giữ, **tắt** (`today_line: false`). 09/11: bản "2 nhóm" (G) dừng ⇒ **giữ 4 tuyến**; phương án B (merge `3b52017`): tuyến khẩn cấp đi trợ lý Huế; câu soạn sẵn + luật từ khoá khẩn cấp (`emergency.py`) **đã gỡ code** | `backend/llm/assistant.py` `_pick_route`; `settings.yaml` khối `assistant:` |
| Công cụ ngày + âm lịch `ngay_lich` | **còn dùng — BẬT từ 09/11** (`7eb1f12`); **từ 10/11 (merge `1633c18`) code tính sẵn ngày trước lần gọi model đầu (`lich_san`), công cụ chỉ còn dự phòng** — đo 10/11: model gọi 0 lần | `backend/llm/ngay_lich.py` `lich_san`; `backend/llm/assistant.py` `_before_model`; `settings.yaml` `ngay_lich: true` |
| Biến môi trường chốt deploy (`HUE_LUOT_MOI_NGAY`, `HUE_COOKIE_SECURE`, `HUE_TAT_DOCS`) + log xoay vòng | **còn dùng** (từ 09/11, merge `ccc9f4f`); không đặt ⇒ như cũ | `backend/api/gioi_han.py`; `api/app.py`; `config/logging.yaml` |
| Từ chối khởi động khi kho lệch chỉ mục | **còn dùng** | `retrieval/full_corpus.py:383–385` |
| Chỉ mục đang dùng | **còn dùng**: `hue_full_corpus_7a2_e5_small_384`, 216 file / 8.603 đoạn (dựng lại 16:09 14/11, record `82abd97169cd`), Qdrant cổng 6335 | `Project_Status.md` §4; `settings.yaml:38` |
| `cost_usd` của công cụ đo | **Đã sửa 01/11** — giá đủ (ghi đệm 0,125 · đọc đệm 0,01 · thường 0,10 · ra 0,50 USD / 1M); `chat_metrics` ghi token đệm | `backend/evaluation/full_corpus_eval.py` `cost_usd`; review `b108_cost_usd_review.md` |
| Chẩn đoán 7B "4 / 22 câu đủ bằng chứng vẫn từ chối" | **đã thay** bởi số đo theo đoạn đúng của 8.1: 0 / 22 | `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_implementation.md` |
| "Representation B" (LLM viết thêm ngữ cảnh cho đoạn) | **đã gỡ** 26/10 | commit `c6e130c` |

## 6. Việc còn lại / cần quyết

- **Streaming — xong, chạy từ 01/11** (spec `00fb57ee01b2`, merge `a80e12d`). Giới hạn ghi lại (không sửa ở Phase 8, giao diện sẽ làm lại): một vài lỗi hiếm ngoài SDK chưa huỷ lần gọi model; route stream ghi bản ghi bằng chứng nửa chừng; rút lại / luồng đứt chỉ kiểm bằng phát lại. Yêu cầu cho giao diện mới:
  `report_agent/2026-10-31_streaming_spec/yeu_cau_cho_giao_dien_moi.md`; review cả nhánh `streaming_final_branch_review.md`; đo `s4_do_d2_implementation.md`.
- **Hội thoại nhiều lượt:** dời sang Phase 9 (bạn chọn 01/11) ⇒ **đã làm, bật từ 03/11** (B3 / B3b — chỉ nhớ câu hỏi 3 lượt; mục 3).
- **Đóng gói Phase 1–8 — xong:** lượt đo cuối mọi sàn đạt; B0 (01/11): bạn đọc 20 cặp mù 5 ↔ 10 đoạn — phần lớn như nhau; 3 cặp bản 5 đoạn từ chối nhầm, bản 10 trả lời được; luật dừng "chưa rõ" (0 cặp quyết) ⇒ bạn chọn giữ 10. Mốc người tham khảo (kho cũ, không chọn bên theo cặp). **Phase 8 bạn đóng 14:29 01/11/2026.**
- **Từ nhận xét B0:** câu dự trù chi phí theo mức ⇒ thử hỏi lại (B4) và tính tiền bằng code (B5c) — cả hai âm, không áp dụng; `[n]` chen trong câu khó đọc ⇒ 02/11 thành số nhỏ bấm được ⇒ **07/11 bỏ hẳn khỏi chữ, thay bằng dòng "Nguồn"** (vẫn giữ `[n]` ở tầng kiểm).
- **Giao diện — giới hạn (cập nhật 09/11):** lưu trú / ăn uống / sự kiện để đợt 2; bản đồ lịch trình có code, cờ tắt (chờ bạn tick phiếu toạ độ); ca "rút lại" / luồng đứt giữa chừng vẫn kiểm bằng luồng tự dựng. (Link "Nguồn ảnh", ảnh nhỏ cho điện thoại, thẻ "Tên chính thức" đã sửa 08/11.)
- **Phase 9 (cập nhật 09/11):**
  - đang chạy: B0–B3b, 👍 / 👎, sửa khẩn cấp, #6 song song, B6 tra web, thời tiết, cổng đợt 1, **biểu mẫu Lên kế hoạch (07/11)**, hỏi bằng ảnh (08/11 — ảnh thu nhỏ gửi OpenAI để đoán tên, máy chủ không lưu ảnh);
  - **bật 09/11:** T1 ngày + âm lịch; định tuyến phương án B (khẩn cấp đi trợ lý Huế); **10/11:** câu ngày nhanh hơn (code tính sẵn ngày, merge `1633c18`); câu chỉ hỏi ngày tháng đi trợ lý (merge `89571d7`);
  - cờ tắt: lịch trình câu gõ tự do (`lich_trinh`), bản đồ lịch trình (`ban_do_lich`, chờ phiếu toạ độ), dòng ngày hôm nay (`today_line`); công cụ hỏi lại B4 đã gỡ (không còn cờ);
  - chờ bạn: bảng điểm v7 (cột thời lượng — để nút "dày lịch" có tác dụng);
  - dừng / đóng hồ sơ (tag): B5c, **T3 bảng vé + giờ**, **G cổng 2 nhóm**, **T2 tra web thành công cụ**, **T4 lịch trình câu gõ**.
  - Còn: **B7** so sánh cuối / đóng gói.
  - Phase 10 (hỏi bằng ảnh **bật từ 08/11**; giọng nói chờ thu câu), 11 (đợt 2 cổng: bản đồ, lưu trú…), 12 (deploy AWS — đã thử build Docker trên máy; **4 chốt trước khi đưa link công khai đã có code từ 09/11**, bật bằng biến môi trường lúc deploy; còn hạn mức OpenAI / Serper).
- **Còn mở, không gấp:** câu trả lời quá gọn (cần thêm câu tự nhiên để đo); bảng giá và câu nhiều nguồn (gốc ở khâu tìm); sai về chữ (tên, sự kiện) chưa có cách đo rẻ.
- Hướng đã gác (chỉ mở lại khi có ý mới đã kiểm trước): trả lời phần có căn cứ; trả lời không suy luận; luật kiểm sau sinh; model chọn 10 / 30 đoạn.

## Phụ lục — hồ sơ kỹ thuật

- **Mã việc ở mục 4:** ngày tương đối = C93 (plan B96); đếm lại trích dẫn = C89; giá đủ = B95; 10 đoạn + NFC = Phase 8.2 B1 (nhánh `p82-b1` `c3d5607`, spec 8.2 §11 "PA3"
  — đưa vào không chờ B0, commit `d922bf7`); đo chữ đầu = probe TTFT; latency 27/10 = B65 / C58; log số đo = C59 / C60 (review B70); không suy luận = **R1**
  (plan sha `8e76e77e0448`, nhánh `p82-r1` `63a472f`); model chọn đoạn = **K3b-m** khâu trả lời (plan bản 3 sha `2a3b22b38ab6`, nhánh `p82-k3b` `a6f609c`, review C54;
  5 câu tụt theo chỉ số T3); sai số liệu = C48; luật kiểm sau sinh = C51; phân loại lỗi = C36; trả lời một phần = **R2** (nhánh `p82-r2`) / H8; nêu đủ chi tiết = **R3**
  (NOT RUN); thước số = **R4**; API báo đúng lỗi = rà code gói 1b (`1e4acd0`); `[Nguồn n]` = gói 1a (`9e6d371`); 8.1 = G2 (`report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g2_implementation.md`
  §4, luật ghi trước `phase_8_1_g2_g4_plan.md` §2.1 sha `a4adfc8eedd9`).
- **B0** = lượt bạn đọc cặp câu trả lời mù (mốc người); luật dừng ở spec 8.2 §11 (`docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md`).
- Mã giới hạn: tổng hợp nhiều nguồn = **F1**; bảng giá = **F2**; tách câu hai ý = giả thuyết **H13**.
- Thử 10 đoạn đầu tiên (24/10, 22 câu từ chối nhầm, 10 / 22 hết từ chối, chưa chấm): `reports/phase_8_probe_context_top10_2026_10_24.md`.
- **Lệch tài liệu đã biết (24/10, còn đúng 31/10):**
  - Spec umbrella `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md` §1 cho phép "trả phần có căn cứ"; spec Phase 6 và prompt bắt từ chối cả câu.
    Code theo spec Phase 6.
  - `guides/full_corpus_rag.md:500` (đoạn lịch sử) còn ghi "direct `AsyncOpenAI`, không Agent/Runner"; code dùng OpenAI Agents SDK một lượt, không tool — đúng theo
    `docs/superpowers/specs/2026-10-01-phase-6-openai-baseline-amendment.md`. Không phải lỗi code.
- Câu chỉ hỏi ngày tháng đi trợ lý (10/11, merge `89571d7`, lời dặn phân loại `164bd4a254e9` → `8cd30cbb359a`): plan `docs/superpowers/plans/2026-11-10-phase-9-dinh-tuyen-lich-plan.md`; report `report_agent/2026-11-08_phase_9_ban_13/b_dinh_tuyen_lich_implementation.md`; review `b_dinh_tuyen_lich_review.md` (E); dữ liệu `data/phase_9/dinh_tuyen_lich/`.
