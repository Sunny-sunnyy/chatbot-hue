# Phụ lục B — Mọi tính năng đang mở và đang tắt: làm gì, một con số, bài nào giảng

*Cập nhật 21:47, ngày 22/11/2026 · khớp các bài lúc 21:45 22/11: hai dòng sửa lịch bằng lời (lệnh thêm vào buổi tối; lệnh thêm khi lịch đã xếp) · trước đó (18:17): khớp các bài lúc tối 22/11 (48 tính năng, kho 267 bài): thêm `the_noi` (17:15) · trước đó: thêm `nho_dap_cuoc_co_lich` (16:08); chép từ cấu hình và chương trình; hệ thống đổi thì phụ lục phải chép lại.*

**Đếm lúc 17:21, ngày 22/11/2026, trên cấu hình hiện tại của máy chủ:** **48 tính năng đang mở, 3 đang tắt** (47 + 3 ở mục `assistant`, cộng 1 đang mở ở mục `anh`; từ 17:15 22/11 thêm `the_noi`; từ 16:08 là 47 (thêm `nho_dap_cuoc_co_lich`); từ 15:42 là 46 (thêm `giu_chu_toi_kiem`); từ 14:47 là 45; trước 14:47 là 42). Lệnh đếm: `sed -n '/^assistant:/,$p' backend/config/settings.yaml | grep -cE '^  [a-z_0-9]+: true'` ra `48`; cùng lệnh với `false` ra `3`. Ngoài 51 dòng bật / tắt đó còn 7 dòng **chọn chế độ** (mục 11) và 7 công tắc đặt **lúc bật máy chủ** chứ không nằm trong file cấu hình (mục 12).

**Đọc bảng thế nào.**
- *Tên* là điều người dùng thấy đổi khi tính năng mở. Tên trong dấu `…` là tên dòng trong file cấu hình, để tra.
- *Một con số làm căn cứ* chép từ chú thích ngay tại dòng cấu hình (hoặc trang tổng của dự án, có ghi rõ). Mọi phép đo trước 09:41 ngày 21/11/2026 là với model viết **gpt-6-luna**; từ lúc đó model viết là **Claude Sonnet 5.5** (ghi "model đang chạy"). Phép đếm chỉ chạy chương trình, không gọi model, ghi "không qua model". Không có số thì ghi "không ghi số".
- *Ai quyết*: "chủ dự án" chỉ khi chú thích hoặc hồ sơ ghi rõ lời chủ dự án; còn lại "nhóm". Từ 21:50 ngày 21/11, chủ dự án dặn: tính năng trong phạm vi đã chốt mà đạt tiêu chí thì nhóm tự mở rồi báo; các dòng mở sau giờ đó ghi "nhóm (theo lời dặn 21/11)".
- *Bài*: số bài theo mục lục 41 bài. Bài 1–38 đã có trong thư mục giáo trình lúc soát; bài 39–41 đang viết, trỏ theo tên trong mục lục.

## 1. Hỏi đáp cơ bản (chặng 3)

| Tên (người dùng thấy gì đổi khi mở) | Dòng cấu hình | Trạng thái | Một con số làm căn cứ | Ai quyết | Bài |
|---|---|---|---|---|---|
| Dưới câu trả lời có trích bài vé, bài địa điểm, bài lễ hội hoặc bài "Lưu trú ở Huế" hiện dòng "giờ mở cửa, giá vé, lịch lễ hội có thể đã thay đổi" | `may_have_changed_notice` | mở từ 03/11 | không ghi số | nhóm | 9, 16, 21 (nhắc ở 2, 4, 7) |
| Nguồn đã trích có câu "tạm ngừng khi lũ / lệnh cấm / thời tiết xấu" mà câu trả lời chưa nêu thì chương trình chép câu đó vào dòng ghi chú | `noi_dong_tam_ngung` | mở từ 19/11 | lượt thật 2 / 3 có dòng, dữ liệu cũ 7 / 7, 0 lần gán nhầm cảnh báo của nơi khác (gpt-6-luna) | chủ dự án ("bật ngay, ghi giới hạn") | 15 |
| Nhờ trợ lý tự làm (đặt chỗ, gửi thư, xem còn phòng) thì nhận một câu nói thật rằng hệ thống chưa làm thay được, theo loại việc, thay cho câu từ chối chung | `noi_that_lam_thay` | mở từ 21:24, 19/11 | 11 / 12 lượt đích ra đúng câu theo loại; 5 / 5 lượt từ chối đúng giữ nguyên (lượt thật, gpt-6-luna) | chủ dự án | 4, 16 |
| Câu xin một danh sách ("những quán … nào") có thêm dòng ghi chú nói danh sách có thể chưa đủ | `danh_sach_noi_that` | mở từ 20/11 | bộ dò mù: nhận 19 / 20 câu xin danh sách, hiện nhầm 2 / 32 câu khác (không qua model) | nhóm (chủ dự án chọn làm phần nhỏ này 20/11) | **chưa có bài** |
| Người sau gõ đúng câu người trước đã hỏi ở lượt đầu một cuộc mới thì nhận lại câu trả lời đã lưu, không tìm kho, không gọi model | `cache_cau_tra_loi` | mở từ 16:16, 20/11 | lần đầu 7,5 giây và 0,00076 USD; người sau 0,11 giây và 0 USD (một câu, ba cuộc; gpt-6-luna) | nhóm | 34 |
| Tin nhiều ý: lần tìm đầu nối thêm 2 đoạn của lần tìm riêng từng vế hỏi (nhiều nhất 6 vế) | `tim_theo_ve` | mở từ 09:47, 22/11 | trợ lý nêu được dữ kiện có trong kho 3 / 24 ⇒ 15 / 24 lượt-tin (8 tin × 3 lượt, model đang chạy); bỏ hai tin đã khá hơn nhờ công cụ khác còn 3 ⇒ 9 trên 18 | nhóm (theo lời dặn 21/11) | 13, 23 |
| Tin nhiều ý: vế cụt không có chủ thể ("giờ mở cửa ko?", "mất bao lâu?") không được tìm riêng; vế có chủ thể, kể cả "taxi", "chợ đêm", vẫn được tìm | `tim_ve_bo_cut` | mở từ 14:47, 22/11 (mở cùng `tach_cau_tim_model`, `het_luot_viet_lai`, trần tìm 3) | trước khi mở: 327 / 1.240 vế tìm (26 %) là vế cụt, đọc tay 20 / 28 đoạn chúng kéo về không liên quan (không qua model); tin 4 ý của một gia đình, 6 lần: nguồn trung vị 20 ⇒ 16, không kém ở tin nào khác (model đang chạy) | nhóm (theo lời dặn 21/11) | 23 |
| Tin nhiều ý có chữ hỏi hẹp (giờ, mở cửa, địa chỉ, ở đâu…): sau mỗi lần tìm, nơi được nhắc đúng tên mà bài riêng chưa có trong nguồn được gắn "thẻ nơi" — dòng địa chỉ / giờ chép nguyên từ bài đó, và hàng vé lẻ trong một nguồn riêng của bài vé — nên ở các tin đã đo trợ lý thôi ghi dòng "Tư liệu chưa có thông tin về: …" cho giờ, vé mà kho có | `the_noi` | mở từ 17:15, 22/11 | tin 4 ý của một gia đình: dòng "chưa có" sai về giờ ba điểm phụ 4, 3, 1 / 9 ⇒ 0 / 12, về vé lẻ An Định 7 / 9 ⇒ 0 / 12 (hai lượt thật, phiên đo chấm; trước đó 8 / 9 câu trả lời có ít nhất một dòng sai); nêu đúng giờ Cung An Định 11 / 12, vé lẻ An Định 11 / 12; nơi kho không có giờ, vé: 0 / 12 lượt bịa; câu trả lời tin đó dài hơn khoảng 11–18 %, ba tin đối chứng không dài hơn; đã nhìn một lần trên trình duyệt tối 22/11 (model đang chạy) | nhóm (theo lời dặn 21/11; lượt 1 trượt một điều theo chữ ⇒ để tắt, lượt 2 đạt tiêu chí ghi trước ⇒ mở) | 23, 40 |
| Dòng "hôm nay là ngày…" ở đầu tin gửi model viết | `today_line` | **tắt** (chưa từng mở) | không ghi số; chú thích: từ chối nhầm không giảm | nhóm | 15, 24 |

## 2. Trợ lý hỏi đáp (chặng 5)

| Tên | Dòng cấu hình | Trạng thái | Một con số làm căn cứ | Ai quyết | Bài |
|---|---|---|---|---|---|
| Câu chào được đáp ngay, câu ngoài chủ đề được từ chối lịch sự; câu về Huế và câu khẩn cấp đi tìm kho (xếp loại bốn tuyến) | `router` | mở từ 03/11 | không ghi số | nhóm | 22 |
| Câu về Huế được trả lời cùng lúc với bước xếp loại, không phải chờ xếp loại xong | `song_song_tra_loi` | mở từ 05/11 | chữ đầu câu về Huế nhanh hơn 1,37 giây [0,34; 2,14]; 90 lượt an toàn, 0 vi phạm (gpt-6-luna) | chủ dự án ("User duyệt 05/11") | 22, 34 |
| Sau lần tìm đầu, trợ lý được tự tìm kho thêm tối đa 3 lần (trước 14:47 22/11: 2; số lần là tham số, phụ lục A) | `tim_them` | mở từ 03/11 | 18 câu nhiều nguồn, lúc trần là 2: điểm đủ ý +1,17 [+0,44; +2,00] (gpt-6-luna) | chủ dự án ("User giữ 03/11") | 21, 23 |
| Đã tìm thêm đủ số lần thì lượt gọi model kế không còn công cụ tìm kho, phải trả lời hoặc nói không có | `het_luot_bo_cong_cu` | mở từ 13/11 | lúc trần là 2: 8 / 8 câu kho không có bớt ít nhất một lần gọi model, nhanh hơn khoảng 6,7 giây cả câu (trang tổng dự án; gpt-6-luna) | chủ dự án ("bật kèm theo dõi") | 21 |
| Câu tìm do model viết mà gộp nhiều nơi / nhiều ý ("giá vé Đại Nội và Lăng Tự Đức") thì ngoài lần tìm cả câu, mỗi phần được tìm riêng, 2 đoạn đầu nối thêm | `tach_cau_tim_model` | mở từ 14:47, 22/11 (cùng bộ với `tim_ve_bo_cut`) | 231 / 396 câu tìm của model là câu gộp; đoạn giá vé Đại Nội vào kết quả 16 ⇒ 27 / 32 câu gộp (không qua model); tin 4 ý, 6 lần: đoạn đó vào bằng chứng 2 ⇒ 6 / 6 (model đang chạy) | nhóm (theo lời dặn 21/11) | 23 |
| Model đã tự tìm ít nhất một lần mà chữ nộp không có số nguồn nào ⇒ viết lại MỘT lần, không công cụ, từ bằng chứng đã gom; vẫn không có ⇒ câu từ chối cố định, thay cho màn hình "Thử lại". Từ 15:42 22/11 chữ giữ chỗ không còn hiện (dòng dưới; trước đó hiện khoảng 15–17 giây rồi bị thay) | `het_luot_viet_lai` | mở từ 14:47, 22/11 (cùng bộ; đứng riêng trưa 22/11 đã đo và không mở) | tin 4 ý, 6 lần mỗi bên: màn hình "Thử lại" 5 · 3 · 0 / 6 (bản đang chạy · thêm hai thay đổi khâu tìm · thêm viết lại); cả bộ với trần tìm 3: đủ hai ý kho có 6 / 6 (model đang chạy). Chỉ một tin; điều kiện "ít nhất một lần" chưa gặp lượt thật | nhóm (theo lời dặn 21/11) | 21, 16 |
| Với model đang chạy (trả cả câu một lần), ở ô chat, mọi lượt hỏi đáp về Huế (trên cấu hình đang chạy, các lượt này đều đi vòng công cụ) giữ chữ tới khi qua bước kiểm nguồn rồi mới hiện: đoạn chữ giữ chỗ và chữ sắp bị rút không còn hiện rồi mất; lượt qua kiểm hiện như cũ. Model trả chữ dần không giữ | `giu_chu_toi_kiem` | mở từ 15:42, 22/11 | trước khi mở: bước viết lại chạy ở 9 / 114 lượt, chữ giữ chỗ đứng 17–25 giây (model đang chạy); sau khi mở: test và 3 lượt thật trong tiến trình; lượt thường đã nhìn trên trình duyệt 22/11 (lúc chờ chỉ một dòng trạng thái rồi cả câu hiện một lần; tin bốn ý 29,5 giây); ca phải viết lại theo test và một lượt thật, chưa nhìn trên trình duyệt | nhóm (theo lời dặn 21/11) | 6, 16, 21 |
| Trợ lý nhớ 3 câu hỏi gần nhất trong một cuộc trò chuyện | `nho_hoi_thoai` | mở từ 03/11 | câu hỏi tiếp bị từ chối nhầm 5 / 19 ⇒ 0 / 19 (gpt-6-luna) | nhóm (theo lời chủ dự án "đạt thì bật") | 23 |
| Trợ lý nhớ thêm câu trả lời của lượt liền trước (bỏ số nguồn, cắt 4.000 ký tự) để hiểu "quán thứ hai bạn vừa kể" | `nho_cau_tra_loi` | mở từ 09:40, 22/11 | 4 chuỗi × 3 lượt: chuỗi trỏ vào câu trả lời trước thì bên tắt không hiểu, bên bật trả đúng; 0 lỗi / 24 lượt (model đang chạy) | nhóm (theo lời dặn 21/11) | 23 |
| Cuộc đã lập lịch: câu hỏi thường cũng được nhớ câu trả lời liền trước ("Bỏ quán đầu đi rồi viết lại danh sách" được hiểu), và lượt bị rút được chạy lại một lần; không nhớ / không chạy lại: lượt thật sự sửa lịch, câu trả lời có trích nguồn của lịch | `nho_dap_cuoc_co_lich` | mở từ 16:08, 22/11 | 9 lượt thật: lịch không đổi 3 / 3, danh sách bỏ đúng quán đầu và đủ các quán còn lại 3 / 3 (2 khớp đúng danh sách cũ, 1 thêm một mục có nguồn); bên tắt: câu "không xác định được quán đầu"; trên trình duyệt 22/11 một cuộc sáu tin, lịch đổi / đứng yên đúng (model đang chạy) | nhóm (theo lời dặn 21/11) | 23, 31, 16 |
| Hỏi tiếp "địa chỉ quán đó" thì trợ lý biết tên nơi lượt trước đã gợi ý (chương trình ghi tên bài đã trích) | `nho_ten_goi_y` | mở từ 21:30, 19/11 | nói đúng nơi vừa nêu 15 / 17 chuỗi ↔ 2 / 17 khi tắt; 0 lượt nói chắc về sai nơi (lượt thật, gpt-6-luna) | chủ dự án | 23 |
| Câu hỏi nhiều ý: ý nào kho có thì trả lời, ý thiếu ghi dòng "Tư liệu chưa có thông tin về…" | `cau_nhieu_y` | mở từ 14/11 | không ghi số | chủ dự án ("User chọn bật") | 23 |

## 3. Công cụ do chương trình tính (bài 24)

| Tên | Dòng cấu hình | Trạng thái | Một con số làm căn cứ | Ai quyết | Bài |
|---|---|---|---|---|---|
| Câu có từ chỉ ngày: trợ lý được dùng công cụ ngày và đổi âm ↔ dương lịch do chương trình tính | `ngay_lich` | mở từ 09/11 | câu theo ngày "dùng được" 27 / 28 ↔ 11 / 28 ở bản chưa có trợ lý (đo 12/11, trang tổng dự án; gpt-6-luna) | chủ dự án ("User approved 09/11") | 24 |
| Hỏi thời tiết: số dự báo 7 ngày của Huế do chương trình lấy và dựng; lịch có dòng dự báo | `thoi_tiet` | mở từ 07/11 | không ghi số | chủ dự án | 24 |
| Câu bão / lũ: model không nhận con số nào, chương trình nối một khối chỉ dẫn cố định | `bao_lu_cong_cu` | mở từ 17/11 | không ghi số | chủ dự án ("User chọn bật, ghi giới hạn") | 24 |
| Hỏi khoảng cách giữa hai điểm: km và phút tra từ bảng dựng sẵn, lúc chạy không gọi mạng | `khoang_cach` | mở từ 16/11 | không ghi số (chú thích: "đo đạt + review 2 vòng") | chủ dự án ("User chọn bật cho lượt thử tối") | 24 |
| Câu nêu đúng hai tên điểm có trong bảng: chương trình tra khoảng cách sẵn trước lần gọi model đầu | `khoang_cach_tinh_san` | mở từ tối 16/11 | chữ đầu trung vị 3,7 ⇒ 1,9 giây, 13 câu, mẫu nhỏ (trang tổng dự án; gpt-6-luna) | chủ dự án | 24 |
| "Gần X có gì ăn": chương trình tính quán có bài kho trong 2 km hoặc các điểm tham quan gần nhất | `gan_diem` | mở từ 08:33, 22/11 | 6 tin lượt thật: 0 lỗi, gọi đúng điểm và loại 5 / 5, nêu đủ tên chương trình đưa 25 / 25 (model đang chạy) | nhóm (theo lời dặn 21/11) | 24 |
| Câu xin danh sách / "nơi nào có đặc điểm X": chương trình liệt kê bài của kho theo nhóm hoặc cụm từ | `liet_ke_bai` | mở từ 09:20, 22/11 | 8 tin / 8 cuộc: 0 lỗi, 0 lần chạm trần vòng; hai câu sàn vẫn bị từ chối (model đang chạy). Công cụ liệt kê bài được đưa ở mọi lượt hỏi đáp, nên trần thực tế mỗi lượt là từ 5 vòng trở lên (phụ lục A, `so_vong_cong_cu`) | nhóm (theo lời dặn 21/11) | 24, 21 |
| Câu vừa nêu khoảng ngày vừa hỏi lễ hội: chương trình tra bảng 27 dòng chép từ kho, đổi âm ⇒ dương | `su_kien_theo_ngay` | mở từ 22:04, 21/11 | 10 câu: bị từ chối 4 / 10 khi tắt ⇒ 0 / 10 khi bật; 40 ngày dương trong câu trả lời, 0 sai (model đang chạy) | nhóm (theo lời dặn 21/11) | 24 |

## 4. Tra web (bài 25)

| Tên | Dòng cấu hình | Trạng thái | Một con số làm căn cứ | Ai quyết | Bài |
|---|---|---|---|---|---|
| Kho không đủ thì tra web một lần, hiện ở mục riêng "Từ web (chưa kiểm)" | `tra_web` | mở từ tối 05/11 | không ghi số (chú thích: "đạt luật ghi trước + kín ×2 + review") | chủ dự án ("User duyệt") | 25 |
| Câu hỏi tiếp ("mở cửa mấy giờ") đi tra web bằng câu tìm có tên nơi của lượt trước, không bằng câu trần | `web_cau_noi_tiep` | mở từ 17:50, 15/11 | 8 / 8 nêu đúng nơi, 0 lạc nơi; tên người dùng 0 / 4 lượt chạm (gpt-6-luna) | chủ dự án ("User chọn sau khi nghe") | 25 |
| Mục web chỉ mở khi CẢ câu trả lời là câu từ chối; tin nhiều ý đã trả lời được một phần thì không tra web | `web_chi_khi_tu_choi` | mở từ 22:20, 21/11 | 11 tin nhiều ý: đi tra web 11 / 11 ⇒ 0 / 11, nhanh hơn trung vị 5,8 giây (model đang chạy) | nhóm (theo lời dặn 21/11) | 23, 25 |

## 5. Hỏi bằng ảnh (bài 26)

| Tên | Dòng cấu hình | Trạng thái | Một con số làm căn cứ | Ai quyết | Bài |
|---|---|---|---|---|---|
| Nút gửi ảnh ở trang Trợ lý; hệ thống đoán tên nơi hoặc món trong danh sách đã duyệt rồi hỏi kho | `anh.bat` | mở từ 08/11 | sai nơi 6 / 66 lượt ↔ 14 / 66 nếu lượt nào cũng trả lời thẳng (33 ảnh × 2 lượt; trang tổng dự án) | chủ dự án ("User 08/11") | 26 |

## 6. Lên kế hoạch (chặng 6, bài 27–29)

| Tên | Dòng cấu hình | Trạng thái | Một con số làm căn cứ | Ai quyết | Bài |
|---|---|---|---|---|---|
| Trang Lên kế hoạch: bấm nút xong thì chương trình xếp lịch bằng giá trị các nút, model chỉ viết câu mô tả | `lich_trinh_bieu_mau` | mở từ 07/11 | bộ quyết đạt 24 / 24; F-a 12 / 12, hai lần (gpt-6-luna) | chủ dự án | 27 |
| Biểu mẫu bốn nhóm và bộ xếp lịch bản 2 (theo buổi, bảng 41 điểm) | `len_ke_hoach_v2` | mở từ 14/11 | không ghi số (chú thích: "nghiệm thu đợt 1 đạt") | chủ dự án ("User D4") | 27, 28, 29 |
| Gõ "lên lịch giúp mình … ngày" trong ô chat thì có dòng chỉ sang trang Lên kế hoạch | `len_lich_dan_trang` | mở từ 21:54, 21/11 | bộ dò mù: nhận 17 / 20, nhận nhầm 0 / 20 (không qua model) | nhóm (theo lời dặn 21/11) | 27 |
| Xếp lịch từ câu gõ tự do trong ô chat (bản đầu) | `lich_trinh` | **tắt** (chưa từng mở) | không ghi số tại dòng; bài 27 ghi: đã đo hai lần, không đạt | nhóm | 27, 28 |

## 7. Sửa lịch bằng lời (bài 31)

| Tên | Dòng cấu hình | Trạng thái | Một con số làm căn cứ | Ai quyết | Bài |
|---|---|---|---|---|---|
| Cuộc có lịch đã lưu: nhắn "đổi…" thì model hiểu ý, chương trình áp và kiểm lịch | `sua_lich_v2` | mở lại 14/11 | câu thường có lịch: chữ đầu trung vị 2,65 giây, 95 % số câu dưới 4,01 giây, 20 câu (trước khi sửa tốc độ 4,17 giây; gpt-6-luna) | chủ dự án (lần bật đầu); nhóm bật lại sau khi sửa tốc độ | 31 |
| Lệnh sửa mà bộ lệnh chưa làm được thì lịch giữ nguyên, kèm một câu cố định | `sua_lich_chua_ho_tro` | mở từ 11:00, 17/11 | Q3 8 / 10; S1, S2 = 0 (gpt-6-luna) | chủ dự án ("vòng 2 trượt ⇒ bật bản vòng 1") | 31 |
| "Dời hai điểm, mỗi điểm một buổi": chương trình tự đọc câu khi model báo chưa làm được | `sua_lich_doi_cho_code` | mở từ 19/11 | 10 chuỗi × 2 lần: đạt 9 / 10 (trước 7 / 10), 0 lượt sửa sai (gpt-6-luna) | chủ dự án ("User duyệt") | 31 |
| Xin dời một điểm sang "buổi tối": hệ thống hiểu được và trả lời thật; lịch không đổi — chương trình chưa tự đặt điểm vào buổi tối (điểm ban ngày thì nói lý do và chỗ dời được). Từ 19:01, 22/11: xin THÊM vào buổi tối một điểm ban ngày đang có trong lịch cũng nhận lý do thật về buổi tối, không còn câu "… đã có trong lịch." (một ca test; chưa có lượt thật) | `sua_lich_buoi_toi` | mở từ 09:45, 22/11 | không ghi số tại dòng (chú thích: 7 tin × 2 khổ màn hình đạt đúng tiêu chí ghi trước; model đang chạy) | nhóm | 31 |
| "Đổi chỗ ngày 1 với ngày 2": chương trình hoán đổi nội dung hai ngày rồi kiểm luật xếp | `sua_lich_doi_cho_ngay` | mở từ 22:04, 21/11 | 15.360 cặp ngày: đổi được 90 %, 0 lỗi văng (không qua model); 5 / 5 lượt thật (model đang chạy) | nhóm (theo lời dặn 21/11) | 31, 32 |
| Tin vừa sửa lịch vừa hỏi: lịch được sửa, kèm dòng nói phần câu hỏi chưa được trả lời và mời gửi riêng | `sua_lich_kem_hoi` | mở từ 21:54, 21/11 | dòng hiện 24 / 24 ở tin sửa + hỏi, hiện nhầm 0 / 24 ở tin chỉ sửa (model đang chạy) | nhóm (theo lời dặn 21/11) | 31 |
| "Thêm điểm X" khi lịch đã kín: lịch giữ nguyên, hệ thống nói điểm nào thay được; "ok thay đi" thì thay thật. Lịch vừa xếp kín giờ nên gần như không lệnh thêm nào làm được mà giữ đủ điểm cũ (liệt kê 22/11 trên 108 lịch mẫu: 0 trên 14.725 lệnh) | `sua_lich_them_khong_the` | mở từ 09:39, 22/11 | 39.509 lệnh thêm mô phỏng: 0 lệnh làm mất điểm (không qua model); hai lượt trình duyệt, 14 lần gọi model: đạt | nhóm | 31 |

## 8. Quanh một lịch (bài 30)

| Tên | Dòng cấu hình | Trạng thái | Một con số làm căn cứ | Ai quyết | Bài |
|---|---|---|---|---|---|
| Dưới lịch có bản đồ, ghim đánh số theo thứ tự trong ngày; thêm trang Bản đồ trên thanh điều hướng | `ban_do_lich` | mở từ tối 16/11 | không ghi số | chủ dự án ("User chọn bật cho lượt thử") | 30, 5 |
| Mỗi điểm của lịch có ảnh | `anh_lich` | mở từ 14/11 | không ghi số | nhóm | 30 |
| Chọn hạng sao thì lịch gợi ý một khu ở cả chuyến và tối đa 5 cơ sở | `luu_tru_lich` | mở từ 14/11 | 3.840 khung lịch, người xem 10 / 10 (không qua model) | nhóm | 30 |
| Mỗi bữa trong lịch có quán gợi ý cùng cụm | `quan_lich` | mở từ 14/11 | 3.840 khung sạch, người xem 10 / 10 (không qua model) | nhóm | 30 |
| Nút "In / Lưu PDF" và "Tải PowerPoint" cho lịch đã lưu | `xuat_pptx` | mở từ 21:30, 19/11 | không ghi số (chú thích: file 4 trang mở được bằng PowerPoint thật; bản in 2 và 3 ngày đủ ảnh) | chủ dự án | 30 |
| Hỏi tiếp về lịch vừa lập ("ngày 2 đi đâu", "mấy giờ xong"): trợ lý thấy đúng lịch đã lưu, số giờ do chương trình tính | `lich_vao_hoi_thuong` | mở từ 19/11 | 3 kịch bản từng nói chắc mà sai nay đúng; 0 lượt bị rút / 57 (gpt-6-luna) | chủ dự án ("bật riêng lịch + số giờ") | 27 |

## 9. Giao diện

Không có dòng bật / tắt riêng cho giao diện. Giao diện hỏi máy chủ "tính năng nào đang mở" lúc tải trang và ẩn mục của tính năng đang tắt (bài 5). Các thứ người dùng thấy mà không có dòng bật / tắt: mục 14.

## 10. Máy móc bên dưới

| Tên | Dòng cấu hình | Trạng thái | Một con số làm căn cứ | Ai quyết | Bài |
|---|---|---|---|---|---|
| Sổ vết có ghi cả chữ câu hỏi và câu trả lời, chỉ để tìm lỗi trên máy phát triển | `so_vet` | **tắt** (bật tạm bằng biến lúc chạy, mục 12) | không ghi số | nhóm | 37 |

## 11. Bảy dòng chọn chế độ

| Chế độ (lời thường) | Dòng cấu hình | Đang chọn | Các lựa chọn | Một con số làm căn cứ | Ai quyết | Bài |
|---|---|---|---|---|---|---|
| Model viết | `full_corpus_generation.provider` | `bedrock` (Claude Sonnet 5.5) từ 09:41, 21/11 — đổi tạm | `openai` (gpt-6-luna) · `bedrock` | không ghi số | chủ dự án ("đổi TẠM, User 21/11") | 33 |
| Cách tìm | `full_corpus_runtime.retrieval_treatment` | `dense_bm25_rrf` (nghĩa + từ khoá, trộn hai bảng xếp hạng) | chương trình chỉ nhận đúng giá trị này | xem bài 13 | nhóm | 11, 13 |
| Xếp lại bằng model | `full_corpus_runtime.reranker` | `none` | chương trình chỉ nhận `none` | xem bài 14 (ba cách đã thử, không dùng) | nhóm | 14 |
| Bản chỉ mục đang dùng | `full_corpus_runtime.candidate_id` | `e5-small-384` | chương trình chỉ nhận đúng giá trị này | xem bài 10 | nhóm | 10, 13 |
| Câu dùng cho lần tìm đầu | `assistant.lan_tim_dau` | `v0` (câu người dùng gõ) | `v1`, `v3` (câu tìm do bước xếp loại viết) · `v2` (trợ lý tự tìm) | không ghi số tại dòng; bài 21 ghi đã thử ba cách | nhóm | 21, 22 |
| Khi nào đưa công cụ thời tiết / ngày / khoảng cách / gần một điểm cho trợ lý (đường Claude) | `full_corpus_generation.bedrock.cong_cong_cu` | `tu_khoa` (chỉ khi câu có từ khoá) | `tu_khoa` · `luon` (mọi lượt) | cổng từ khoá bỏ sót 4 / 60 câu cần công cụ (đếm sổ vết 21/11; chú thích trong code) | nhóm | 21, 24 |
| Như dòng trên, cho đường gpt-6-luna | `assistant.cong_cong_cu` | `tu_khoa` | như trên | như trên | nhóm | 24 |

Ba dòng trên (`retrieval_treatment`, `reranker`, `candidate_id`) cùng 5 tham số ở phụ lục A là 8 giá trị chương trình chỉ nhận đúng một giá trị (5 ở A, 3 ở B); ghi khác thì máy chủ không bật.

Hai mức suy luận của Claude (`reasoning_default`, `reasoning_sua_lich`) là giá trị chọn trong bốn mức; chúng nằm ở phụ lục A.

## 12. Bảy công tắc đặt lúc bật máy chủ (không nằm trong file cấu hình)

Đây là biến môi trường: một giá trị đặt trước lệnh bật máy chủ, đổi theo từng máy. Không đặt thì hệ thống chạy như cột "Mặc định".

| Công tắc (lời thường) | Tên biến | Mặc định | Dùng để làm gì | Bài |
|---|---|---|---|---|
| Bật sổ vết có chữ | `HUE_SO_VET` | không đặt ⇒ theo `so_vet` (tắt) | chỉ máy phát triển | 37 |
| Bật / tắt tra web khi đóng gói | `HUE_TRA_WEB` | không đặt ⇒ theo `tra_web` (mở) | chú thích code: bản công khai tắt tới khi chủ dự án quyết | **chưa có bài** (hợp nhất: bài 36) |
| Trần lượt gọi model mỗi địa chỉ mạng mỗi ngày | `HUE_LUOT_MOI_NGAY` | không đặt ⇒ không giới hạn | chốt trước khi đưa lên mạng | 37 |
| Trần tổng lượt gọi model mỗi ngày của cả máy chủ | `HUE_LUOT_TONG_MOI_NGAY` | không đặt ⇒ không giới hạn | như trên | 37 |
| Mở trang theo dõi của chủ dự án | `HUE_KHOA_THEO_DOI` | không đặt ⇒ trang báo không tồn tại | chỉ người có khoá xem được | 34, 37 |
| Tắt trang mô tả các đường gọi của máy chủ | `HUE_TAT_DOCS` | không đặt ⇒ trang đó còn mở | bản công khai không lộ sơ đồ đường gọi | 35, 37 |
| Cookie chỉ đi qua kết nối mã hoá | `HUE_COOKIE_SECURE` | không đặt ⇒ tắt (máy phát triển chạy kết nối thường) | bật khi đưa lên mạng | 35, 37 |

Thêm một biến chỉ đổi địa chỉ, không bật / tắt gì: `HUE_QDRANT_URL` (địa chỉ Qdrant khi chạy trong Docker; bài 36 giảng đóng gói nhưng chưa nhắc tên biến này).

## 13. Tính năng đang TẮT và vì sao

| Tính năng | Dòng cấu hình | Vì sao tắt | Muốn mở thì cần gì |
|---|---|---|---|
| Dòng "hôm nay là ngày…" đầu tin gửi model | `today_line` | đo xong thấy từ chối nhầm không giảm; việc về ngày đã chuyển sang công cụ ngày và nguồn "Lịch hệ thống" do chương trình tính (bài 24) | không có kế hoạch mở |
| Xếp lịch từ câu gõ tự do | `lich_trinh` | đo hai lần, chưa đạt luật ghi trước; lịch chỉ làm qua biểu mẫu nút, câu gõ "lên lịch giúp mình" được chỉ sang trang Lên kế hoạch | một lần đo mới đạt luật ghi trước |
| Sổ vết có chữ | `so_vet` | có chữ câu hỏi và câu trả lời; trang Giới thiệu hứa máy chủ không lưu chữ vào nhật ký (bài 37) | chỉ bật tạm ở máy phát triển; bản công khai không bật |

## 14. Tính năng KHÔNG tìm được bài nào giảng (để bổ sung)

Soát bằng cách tìm tên dòng cấu hình và cụm chữ người dùng thấy trong 38 bài đã có (1–38) và mục lục 41 bài.

| Tính năng | Tình trạng | Bài hợp nhất để thêm |
|---|---|---|
| Dòng ghi chú danh sách có thể chưa đủ (`danh_sach_noi_that`) | đang mở; không bài nào nhắc tên dòng hay câu ghi chú | bài 16 (cùng nhóm các dòng chương trình nối thêm) hoặc bài 24 (cạnh công cụ liệt kê bài) |
| "Huế qua các thời kỳ" (sáu mốc lịch sử cuộn kể chuyện ở trang Giới thiệu) | không có dòng bật / tắt; không bài nào nhắc | bài 5 |
| Công tắc tra web lúc đóng gói (`HUE_TRA_WEB`) | không bài nào nhắc, kể cả bài 36 (đóng gói) | bài 36 |

**Có bài nhắc nhưng mỏng** (chỉ một dòng bảng, chưa có cơ chế hay quyết định):

| Tính năng | Bài đang nhắc | Thiếu gì |
|---|---|---|
| Chép câu "tạm ngừng khi lũ…" (`noi_dong_tam_ngung`) | 15 (một dòng bảng) | khi nào hiện, số đo 2 / 3 và 7 / 7, giới hạn "chỉ khi câu trả lời trích bài có cảnh báo" |
| Câu nói thật rằng hệ thống chưa làm thay được (`noi_that_lam_thay`) | 4 (một quyết định), 16 | bài 16 trỏ "bài 23" cho ba câu này, nhưng bài 23 không nhắc ⇒ sửa chỗ trỏ của bài 16 thành bài 4, hoặc thêm vào bài 23 |
| Câu dùng cho lần tìm đầu (`lan_tim_dau`) | 21, 22 (dòng bảng cấu hình) | đủ để tra |

## 15. Thứ người dùng thấy mà KHÔNG có dòng bật / tắt

| Thứ người dùng thấy | Ở đâu | Bài |
|---|---|---|
| Trang chủ: ô hỏi lớn, câu gợi ý, ô thời tiết nhỏ, năm chủ đề | thanh điều hướng | 5 |
| Trang Khám phá: năm lĩnh vực, danh sách bài, đọc một bài, nút "Hỏi trợ lý về điểm này" | thanh điều hướng | 5 |
| Nút "Báo thông tin chưa đúng" ở mỗi bài (máy chủ chỉ ghi mã bài) | trang bài của Khám phá | 5, 35 |
| Trang Giới thiệu: làm được gì, giới hạn, dữ liệu người dùng | thanh điều hướng | 5, 37 |
| "Huế qua các thời kỳ" | trong trang Giới thiệu | **chưa có bài** |
| Trang Chỗ ở (lọc theo khu) | chỉ mở từ ô "Nơi ở" của lịch | 30, 5 |
| Trang Bản đồ (40 điểm, lọc theo loại) | thanh điều hướng; hiện theo `ban_do_lich` | 5, 30 |
| Lịch ví dụ trên trang Lên kế hoạch (dựng bằng chính bộ xếp, câu do chương trình viết) | trang Lên kế hoạch | 27 |
| Nút "Thêm vào lịch (.ics)", sao chép, tải chữ | thẻ lịch | 30 |
| Dời một điểm không được thì hệ thống nói lý do và gợi ý chỗ dời được (có từ 20/11) | khung Trợ lý, cuộc có lịch | 31 |
| Nút Dừng, Thử lại, cuộc trò chuyện mới; câu hỏi tối đa 500 ký tự | khung Trợ lý | 5 |
| Trang theo dõi của chủ dự án (số lượt, kết cục, thời gian chờ, tiền mỗi ngày) | không có trong menu, cần khoá | 34, 35 |
| Lệnh đề xuất sửa kho khi một giá đổi, và lệnh duyệt đề xuất | dòng lệnh của người giữ kho | 7 (nhắc ở 3, 12) |
| Lệnh cập nhật chỉ mục riêng khi sửa một bài | dòng lệnh | 12 |
| Lệnh bật cả hệ thống | dòng lệnh | 36 |
| Lời báo khi kho lệch chỉ mục ("máy chủ vẫn chạy, mọi câu hỏi nhận lời báo") | khung Trợ lý | 6, 12 |

<details>
<summary>Nguồn (để giữ phụ lục đúng — anh không cần đọc)</summary>

- Mọi dòng bật / tắt, ngày mở, số đo, lời "User …": chú thích tại từng dòng của `backend/config/settings.yaml` (lần sửa cuối của file: commit `e4e06f9d`, 10:25 22/11/2026; đọc 13:20 22/11/2026 trên cây chính, HEAD `f359d89f`) [code].
- Đếm 45 / 3: lệnh ở `guides/RUNBOOK_BAN_GIAO.md` mục 0, chạy 15:10 22/11/2026 trên cây chính, main `2ddd6dc2` [đã chạy]; tách theo mục: `assistant` 44, `anh` 1. Runbook ghi `45` lúc 14:47 22/11 trên main `993480ed` — khớp. (Đếm trước: 42 / 3 lúc 13:20.)
- Cập nhật theo bộ thay đổi mở 14:47 22/11/2026: `bai_hoc/VIEC_MOI_XONG.md` mục 42, 43; `guides/RUNBOOK_BAN_GIAO.md` mục 10.1; `backend/config/settings.yaml` dòng `tim_ve_bo_cut`, `tach_cau_tim_model`, `het_luot_viet_lai` và chú thích (giờ mở trong chú thích: 14:33 — giờ nhánh đạt tiêu chí; giờ tới người dùng: 14:47 theo runbook mục 0 và mục 42) [code; số đo: đã chạy, phiên đo; người viết không chạy lại].
- Ngày mở của các dòng chú thích không ghi ngày (`router`, `may_have_changed_notice`, `tim_them`, `nho_hoi_thoai`, `ngay_lich`, `het_luot_bo_cong_cu`, `danh_sach_noi_that`, `anh.bat`…): commit đầu tiên đặt dòng đó thành `true`, `git log --reverse -G "^  <tên>: *(true)" -- backend/config/settings.yaml` [đã chạy]. "Chưa từng mở" của `today_line`, `lich_trinh`, `so_vet`: cùng lệnh không ra commit nào [đã chạy].
- "User approved 09/11" (`ngay_lich`), "User 08/11" (`anh.bat`): lời commit `7eb1f129`, `cf57309c` [chép].
- Số không có tại dòng cấu hình, lấy từ trang tổng `bai_hoc/BAN_DO_DU_AN.md` mục "Cái gì ĐANG chạy": `het_luot_bo_cong_cu` (8 / 8, 6,7 giây), `cache_cau_tra_loi`, `danh_sach_noi_that`, `ngay_lich` (27 / 28 ↔ 11 / 28), `khoang_cach_tinh_san` (3,7 ⇒ 1,9 giây), `anh.bat` (6 / 66 ↔ 14 / 66), `lich_vao_hoi_thuong` [chép].
- `danh_sach_noi_that`: chủ dự án chọn làm phần nhỏ trước, 20/11: `bai_hoc/VIEC_MOI_XONG.md` mục 22; mở cùng `cache_cau_tra_loi` trong commit `051e954f` [chép]. Chú thích tại dòng vẫn còn câu cũ "TẮT tới khi … chủ dự án chọn bật" dù giá trị là `true`.
- Giờ đổi model viết 09:41 21/11 và lời dặn 21:50 21/11 ("đạt thì mở rồi báo, không hỏi chủ dự án về bật"): `session_prompt/HIEN_TRANG.md` mục 4 [chép].
- Phụ thuộc giữa các tính năng và các chế độ chỉ nhận một giá trị: `backend/llm/assistant.py` (`AssistantFlags.__post_init__`, `from_settings`), `backend/core/settings_loader.py` (`validate_phase6_settings`, `apply_env_overrides`) [code].
- Biến môi trường: `backend/core/settings_loader.py`, `backend/api/gioi_han.py`, `backend/api/theo_doi.py`, `backend/api/app.py` (`TAT_DOCS_ENV`), `backend/api/routes/chat.py` (`COOKIE_SECURE_ENV`) [code]. `HUE_GIT_SHA` (dấu phiên bản), `HUE_BEDROCK_CREDS_FILE` (đường tới file khoá) không bật / tắt gì nên không vào bảng.
- Thứ người dùng thấy không có dòng bật / tắt: `frontend/src/route.js` (danh sách trang), `GioiThieu.jsx` (gọi `HueQuaCacThoiKy`), `KhamPha.jsx` (nút báo thông tin chưa đúng), `LenKeHoach.jsx` (lịch ví dụ), `LichV2.jsx` (.ics), `backend/ops/de_xuat_sua_kho.py` [code].
- Cột "Bài": tìm tên dòng cấu hình và cụm chữ người dùng thấy trong các file bài 1–38 ở thư mục giáo trình bằng `grep`, 13:20–13:32 22/11/2026 [đã chạy]; bài 39–41 chưa có thì trỏ theo tên trong mục lục.
- Các mục mới đã qua một lượt đối chiếu độc lập (một agent khác chỉ đọc, 22/11/2026), các dòng sai / lệch đã sửa lúc 14:17: `data/hoc_cung_D/kiem/muc_moi_02_07_11_va_phu_luc.md` [riêng tư]. Bài "Lưu trú ở Huế" là nhóm thứ tư của dòng nhắc: `backend/llm/assistant.py` (`NOTICE_SOURCE_PREFIXES`); câu khẩn cấp đi tìm kho: cùng file (`_pick_route`); chế độ `luon` đưa cả công cụ gần một điểm: cùng file (`_lich_extra`) [code].

- Đã qua một lượt kiểm chéo sau lượt cập nhật 14:47 (`data/hoc_cung_D/kiem/cap_nhat_14h47.md`) [riêng tư]. Hàng `het_luot_viet_lai` thêm thứ người dùng thấy: `bai_hoc/VIEC_MOI_XONG.md` mục 42, đính chính 15:14; runbook 10.1 hàng "Lưới viết lại".

- Hàng `giu_chu_toi_kiem` (thêm 22/11): chú thích dòng đó trong `backend/config/settings.yaml` (dòng 99); `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 hàng "Lưới viết lại" [code]. Phạm vi "mọi lượt hỏi đáp về Huế ở ô chat" và nhãn trình duyệt theo ca: bài 6 quyết định 4; `bai_hoc/VIEC_MOI_XONG.md` mục 44; `data/test_cuoi/chay_2026-11-22_e_nhin_gom/KET_QUA.md` [riêng tư, chưa mở; đã chạy, phiên đo].
- Hàng `nho_dap_cuoc_co_lich` và số 47 (thêm 17:00 22/11): chú thích `backend/config/settings.yaml` dòng 76 ("MỞ 16:08"); `guides/RUNBOOK_BAN_GIAO.md` mục 10.2 hàng `nho_dap_cuoc_co_lich` (9 lượt thật, lần nhìn trình duyệt 16:21; runbook ghi giờ 16:13 là giờ đếm lại); bài 23 bảng Cấu hình và "Đã so" dòng 12 [code + chép]. Đếm: lệnh runbook mục 0 (runbook: `47`, 16:13 22/11, main `2a221e5`); người cập nhật chạy lại 16:57 22/11 trên main `c23e17ba`: `47` mở, `3` tắt, mục `anh` 1 mở [đã chạy]. Trước đó 46 lúc 15:51 (main `15cd5985`). Số "48 dòng bật / tắt" ở bản trước đã cũ từ 15:42 (lúc đó là 49); nay 50.
- Hàng `the_noi` và số 48 (thêm 17:29 22/11/2026): chú thích `backend/config/settings.yaml` dòng 100 ("BẬT 17:15 22/11/2026 (phiên điều phối; lượt thật thứ hai đạt đủ tiêu chí ghi trước…"); `backend/llm/the_noi.py` (chú thích đầu file, `HOI_HEP`); `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 hàng "Thẻ nơi" và mục 0 dòng 26 (`48` lúc 17:18 trên main `2a9c9e9c`); bài 23 "Đã so" dòng 13 [code + chép]. Đếm: lệnh mục 0 tự chạy 17:21 22/11/2026 trên main `4e2746c0` ra `48`; `false` ra `3`; `true|false` ra `51` [tự chạy lệnh đếm]. Bảng từ 89 thành 90 hàng.

</details>
