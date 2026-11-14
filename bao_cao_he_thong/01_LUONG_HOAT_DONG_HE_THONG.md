# Chatbot Huế chạy thế nào — dòng chảy dữ liệu

Cập nhật 16:19 14/11/2026 (thêm chiều 14/11: kho 216 bài, câu hỏi nhiều ý, nơi ở gợi ý trong lịch, lịch mẫu, ảnh dưới câu trả lời, bỏ chữ ghi công ảnh; trước: "Lên kế hoạch" bản 2, sửa lịch bằng lời, giao diện mới; bản cũ xem trong lịch sử phiên bản — git). Tả bản **đang chạy**. Số đo (tốc độ, tiền, điểm) không ghi ở đây — xem bảng
"Số chính" và "Từ hay gặp" trong [README](README.md).

Hệ thống có hai phần: **chuẩn bị kho** (chạy một lần, mỗi khi kho đổi) và **trả lời** (mỗi câu hỏi).

```text
CHUẨN BỊ (một lần):  224 bài ─► cắt thành đoạn ─► mỗi đoạn: vector nghĩa + từ khoá ─► cất vào Qdrant (kèm "phiếu" ghi dấu từng bài)

TRẢ LỜI (mỗi câu):
  [cuộc đã có lịch "Lên kế hoạch"] ─► cùng lúc với phân loại: model đọc xem câu có phải yêu cầu sửa lịch ─► có (và không khẩn cấp) ⇒ code sửa lịch
  câu hỏi ─► phân loại (model, một lần gọi ngắn) ──┬─ xã giao ───────► model đáp ngắn, không tìm kho
                                                   ├─ ngoài phạm vi ─► câu từ chối cố định (không gọi thêm model)
                                                   └─ về Huế / khẩn cấp
                                                        │
              tìm 10 đoạn trong kho ◄───────────────────┘
                 │  (+ code tính sẵn ngày nếu câu có từ chỉ ngày)
                 ▼
              model đọc ngữ cảnh, viết câu trả lời ─ có thể nhờ công cụ: tìm thêm (≤ 2 lần) · dự báo thời tiết · đổi ngày
                 │
                 ▼
              code kiểm nguồn ─► hiện câu trả lời + dòng "Nguồn"
                 │
                 └─ nếu câu trả lời là "không đủ thông tin" ⇒ tra web một lần ⇒ mục riêng "Từ web (chưa kiểm)"
```

## Chuẩn bị kho

1. **Kho** là 224 bài Markdown tiếng Việt (5 chủ đề, 8.644 đoạn) đã được biên soạn và sửa qua nhiều đợt (14/11: 5 bài lưu trú theo danh mục Cục Du lịch Quốc gia; 4 bài cầu Trường Tiền, Ga Huế, chùa Từ Hiếu, nhà vườn An Hiên + giờ Đại Nội theo mùa); chatbot không đọc gì ngoài kho (trừ web, thời tiết — dưới).
2. **Cắt đoạn** theo cấu trúc bài: mỗi đoạn văn, mỗi mục danh sách, mỗi dòng bảng (kèm hàng tiêu đề) là một đoạn. Đoạn mang theo tên bài và đường tiêu đề
   (vd "Bún bò Huế > Quán nổi tiếng") để dễ tìm.
3. Mỗi đoạn được tính **vector nghĩa** (model e5-small chạy ngay trên máy, không tốn tiền) và **từ khoá** (BM25), rồi cất vào **Qdrant**.
4. Một **phiếu dựng** ghi dấu từng bài. Mỗi lần khởi động, chatbot so dấu với kho hiện tại; kho đã sửa mà chưa dựng lại ⇒ **chatbot từ chối chạy** (để không trả
   lời bằng dữ liệu cũ).

## Trả lời một câu hỏi

1. **Nhận câu hỏi** từ trang web (≤ 500 ký tự), đưa dấu tiếng Việt về một dạng chuẩn. Nếu đang trong một cuộc trò chuyện, kèm theo **3 câu hỏi trước** (chỉ câu hỏi,
   không kèm câu trả lời cũ).
2. **Phân loại** — một lần gọi model ngắn xếp câu vào 4 loại. Câu khẩn cấp (bị cướp, tai nạn, ốm nặng…) đi đúng đường câu về Huế. Phân loại lỗi hoặc quá 10 giây
   ⇒ coi là câu về Huế. Để đỡ chờ, phần "về Huế" (bước 3–4) **chạy luôn cùng lúc** với phân loại; nếu hoá ra không phải câu về Huế thì bỏ phần đó, người dùng không
   thấy chữ nào của nó (đổi lại: câu không phải về Huế tốn thêm một ít tiền cho phần bị bỏ).
3. **Tìm** — câu hỏi được so với mọi đoạn theo nghĩa (lấy 30 đoạn gần nhất), chấm lại 30 đoạn đó theo từ trùng (BM25), gộp hai bảng xếp hạng (RRF) ⇒ giữ **10 đoạn đầu** làm ngữ cảnh.
   Câu có từ chỉ ngày ("hôm nay", "cuối tuần", "rằm", "Tết"…) ⇒ **code** tính sẵn hôm nay, các ngày được hỏi, đổi ngày âm ↔ dương (cả ngày âm nhắc trong 10 đoạn)
   và thêm thành một nguồn "Lịch hệ thống".
4. **Viết câu trả lời** — model đọc lời dặn + ngữ cảnh, viết tiếng Việt, mỗi ý ghi số nguồn. Thiếu bằng chứng ⇒ phải trả đúng câu "Tôi không tìm thấy đủ thông tin
   trong nguồn dữ liệu để trả lời câu hỏi này." Trong lúc viết, model được nhờ **công cụ**: tìm thêm trong kho bằng câu tìm nó tự đặt (tối đa 2 lần), lấy dự báo thời
   tiết Huế, đổi một ngày chưa có trong nguồn "Lịch hệ thống". Mọi con số ngày / thời tiết do code tính, model chỉ chép.
   **Câu hỏi nhiều ý (từ 14/11):** code đếm được ≥ 2 vế hỏi (tách theo dấu phẩy / chấm phẩy / chấm hỏi, và "và / còn / với" khi cả hai phần có từ hỏi) ⇒ model trả lời
   ý nào có bằng chứng, ý thiếu ghi đúng một dòng "Tư liệu chưa có thông tin về: …" (trước: thiếu một ý là từ chối cả câu). Chỉ còn dòng ý thiếu ⇒ code đổi về câu
   từ chối chuẩn. Câu đếm được một vế ⇒ như cũ.
5. **Hiện dần + kiểm** — chữ hiện dần trên trang trong lúc model viết. Viết xong, **code kiểm nguồn**: mỗi số nguồn phải trỏ tới đoạn có thật. Không qua ⇒ trang rút
   lại chữ và báo lỗi (rất hiếm — chưa gặp trong các lượt đo). Qua ⇒ hiện dòng **"Nguồn: tên bài · tên bài"**, bấm vào xem đoạn gốc hoặc cả bài. Câu trả lời trích bài về vé, địa điểm
   tham quan, lễ hội hoặc lưu trú (từ 14/11) có thêm dòng "thông tin có thể đã thay đổi". Mọi nguồn được trích thuộc **một** bài về một nơi / món có ảnh "chắc"
   ⇒ trang hiện **một ảnh** của bài đó dưới câu trả lời (code quyết; không ảnh khi từ chối, có mục web hay có lịch).
6. **Tra web (chỉ khi kho không có)** — câu về Huế mà câu trả lời là "không đủ thông tin", hoặc (từ 14/11) có dòng ý thiếu ⇒ code gửi câu hỏi tới Serper (máy tìm Google) **một lần**, model viết một
   mục riêng **"Từ web (chưa kiểm)"** ghi link; câu nhiều ý ⇒ model chỉ viết mục web cho vế thiếu (code chọn vế từ chữ người dùng). Code chặn trước khi hiện: link không có trong kết quả tìm, mã trang web thô, số tiền không có trong đoạn trích, giờ / ngày ở câu cần tin "ngay lúc này" (vd giá hôm nay); câu về bão, lũ ⇒
   câu cố định "xem trung tâm dự báo / chính quyền, khẩn cấp gọi 112".
7. **Ghi số đo** — mỗi câu ghi đúng một dòng log: loại câu, thời gian từng bước, số token, tiền. **Không ghi chữ câu hỏi hay câu trả lời.**

## Ví dụ trọn vẹn (câu tự viết)

Người dùng gõ: *"Cuối tuần này mình ở Huế, nên ăn bún bò ở đâu?"*

| Bước | Chuyện gì xảy ra |
|---|---|
| Phân loại | model xếp "về Huế"; cùng lúc phần tìm + viết đã bắt đầu chạy |
| Tìm | 10 đoạn gần nhất — chủ yếu từ bài món bún bò và các bài quán bún bò trong kho |
| Lịch | có "cuối tuần này" ⇒ code thêm nguồn "Lịch hệ thống": hôm nay là thứ mấy, các ngày trong tuần này (dương + âm) |
| Viết | model kể vài quán có trong kho kèm địa chỉ / giờ mở như bài ghi, mỗi ý một số nguồn; nhắc ngày cuối tuần đúng như nguồn lịch; không thêm quán ngoài kho |
| Kiểm + hiện | số nguồn hợp lệ ⇒ dòng "Nguồn: …" gồm các bài quán (bài quán ăn không kèm dòng "thông tin có thể đã thay đổi" — dòng đó chỉ cho bài vé, địa điểm, lễ hội) |
| Không tra web | vì kho đã trả lời được |
| Log | một dòng: loại "về Huế", 1 lần phân loại + 1 lần viết, có nguồn "Lịch hệ thống" (code tính sẵn), thời gian, tiền — không có chữ câu hỏi |

Hỏi tiếp *"Còn chè thì nên ăn ở đâu?"* ⇒ câu hỏi trước được gửi kèm, nên model hiểu vẫn là chuyện ăn uống ở Huế dịp cuối tuần. Nhưng *"Quán thứ hai mở
mấy giờ?"* thì **chưa hiểu được**: chatbot không nhớ câu trả lời trước nên không biết "quán thứ hai" là quán nào (giới hạn đã chọn — nhớ cả câu trả lời từng
làm lọt câu sai ở lượt đo).

## Các đường khác

| Người dùng làm gì | Đường đi |
|---|---|
| Chào / cảm ơn / hỏi chatbot là ai | phân loại "xã giao" ⇒ model đáp ngắn, không tìm kho, không nguồn |
| Hỏi chuyện ngoài Huế (code, giá vàng, nơi khác…) | phân loại "ngoài phạm vi" ⇒ câu từ chối cố định + vài câu gợi ý hỏi được |
| Điền biểu mẫu "Lên kế hoạch" (bản 2, từ 14/11) | **không** phân loại; biểu mẫu 4 nhóm (ai đi · bao lâu, ngày đi · kiểu đi · thích gì); **code xếp** theo chuỗi luật (an toàn nhóm có trẻ em / người lớn tuổi ⇒ giờ mở cửa, mùa ⇒ cụm gần ⇒ mưa theo dự báo ⇒ sở thích ⇒ kiểu đi) với quỹ phút, giờ gợi ý, "khoảng N phút đi" giữa hai điểm; khung hiện ngay, model chỉ viết mỗi điểm một câu tả (câu trượt kiểm ⇒ code thay câu dự phòng); ảnh 24 / 34 điểm (Commons, ghi công); link Google Maps do code dựng; nút tải lịch `.ics` dựng trong trình duyệt (cần ngày đi). Lịch hiện ngay ở trang Lên kế hoạch (bản đồ cả lịch trình chưa bật) . Từ 14/11 chiều: lịch ≥ 2 ngày có thẻ **"Nơi ở gợi ý"** (code chọn một khu cho cả chuyến + ≤ 5 cơ sở theo hạng + link tìm phòng, không giá); chưa xếp ⇒ trang hiện **lịch mẫu "Ví dụ"** do chính bộ xếp dựng, không gọi model |
| Nhắn sửa lịch khi cuộc đã có lịch (từ 14/11) | một lần gọi model chỉ để **hiểu ý** ⇒ danh sách hành động có tên (bỏ / thêm / thay / dời buổi / đổi số ngày / đổi kiểu, sở thích, trẻ em, người lớn tuổi; gửi ≤ 3, áp ≤ 2), chạy **song song** với phân loại; phân loại ra khẩn cấp ⇒ khẩn cấp thắng, đi đường thường. **Code** khớp tên điểm, xếp lại giữ chỗ các điểm không chạm, kiểm luật; khối đầu lịch "Đã đổi / Không đổi được / Chưa làm" do code viết; "thay" không nói thay bằng gì ⇒ thẻ chọn ≤ 3 điểm. Câu không phải câu sửa ⇒ đường thường |
| Gửi ảnh | ảnh được thu nhỏ, gửi model kèm danh sách 42 điểm / món dễ nhận ra bằng ảnh (lập từ kho; model chỉ được chọn tên trong danh sách này); model gợi ≤ 3 tên (có thể "không nhận ra"); người dùng bấm đúng tên ⇒ thành câu hỏi thường. Không bấm ⇒ không trả lời |
| Đọc "Khám phá", xem ô thời tiết trang chủ | đọc thẳng bài kho / dự báo, **không gọi model**; từ 14/11: **184 / 216** bài có ảnh; giao diện **không hiện chữ ghi công ảnh** (bạn yêu cầu; nguồn từng ảnh giữ trong bảng dữ liệu); thẻ "Thông tin nhanh" bên bài |
| Bấm 👍 / 👎, "Cuộc trò chuyện mới", "Dừng" | ghi một dòng đánh giá (không chữ) · xoá nhớ cuộc hiện tại · máy chủ huỷ lần gọi model đang chạy |

## Code quyết, model không quyết

Model hay tính sai hoặc tự thêm con số, nguồn, giờ giấc (các lần thử chỉ dặn model "đừng làm" đều không đủ) ⇒ những việc này do code: câu từ chối cố định · kiểm số nguồn · tính ngày, đổi âm ↔ dương · số dự báo thời tiết · xếp lịch, áp lệnh sửa lịch, chọn nơi ở gợi ý · đếm vế câu nhiều ý, đổi câu chỉ còn ý thiếu về câu từ chối · chọn ảnh dưới câu trả lời ·
chặn link / số tiền lạ ở mục web · câu bão lũ · giới hạn số lần tìm. Model chỉ phân loại câu, chọn khi nào nhờ công cụ, và diễn đạt.

## Dữ liệu người dùng gửi đi đâu

| Đi tới | Gửi gì | Khi nào |
|---|---|---|
| OpenAI (model `gpt-6-luna`) | câu hỏi + tối đa 3 câu hỏi trước + đoạn kho + nguồn lịch / thời tiết; ảnh đã thu nhỏ (khi hỏi bằng ảnh) | mọi câu cần model |
| Serper (tìm Google) | chữ câu hỏi | chỉ khi câu về Huế mà kho không có |
| Open-Meteo (thời tiết) | **chỉ** toạ độ Huế + số ngày — không có chữ người dùng | câu hỏi thời tiết, ô thời tiết trang chủ |
| Google Maps | không gì từ máy chủ — chỉ khi người dùng tự bấm link | lịch trình |
| Máy chủ (RAM) | 3 câu hỏi gần nhất của cuộc trò chuyện + (từ 14/11) lịch mới nhất của cuộc — chỉ dữ liệu code dựng (khung, ngày đi, điểm đã bỏ, câu tả đã kiểm), không chữ người dùng; xoá sau 30 phút không hỏi hoặc khi bấm "Cuộc trò chuyện mới"; ảnh **không** lưu | — |
| Trình duyệt (cookie) | một mã cuộc trò chuyện ngẫu nhiên, 30 phút, trang web không đọc được | — |
| Log của chatbot (file trên máy chủ) | số đo, loại câu, tiền, đánh giá 👍 / 👎 — **không** chữ câu hỏi / câu trả lời, không IP; file xoay vòng (≤ 10 MB × 3) | mọi câu |
| Log truy cập của máy chủ web | phép thử 15:04 11/11/2026: cấu hình log của chatbot (nạp lúc khởi động) **tắt** log truy cập mặc định của uvicorn ⇒ nhiều khả năng **không** in IP; chưa kiểm trên máy chủ thật đang chạy | — |

## Khi có lỗi, người dùng thấy gì

Model lỗi / mạng đứt giữa chừng ⇒ chữ đã hiện bị xoá, có lời báo tiếng Việt + nút "Thử lại" · kho chưa dựng lại sau khi sửa ⇒ chatbot không chạy (người vận hành dựng
lại) · Qdrant tắt ⇒ báo lỗi tạm thời · khi đưa lên mạng có giới hạn số lượt hỏi mỗi máy mỗi ngày ⇒ quá lượt nhận câu báo.

## Giới hạn chính (đang chạy)

- Câu khẩn cấp: phân loại nhận ra, nhưng trợ lý Huế thường từ chối (kho không có bài khẩn cấp) và không có số 112–115 — đo lại 14/11 trên main: từ chối 10 / 12, có số 0 / 12; giới hạn đã nhận (bạn quyết 12/11 không làm dòng số khẩn cấp).
- Chỉ một nhà cung cấp model, không dự phòng. Không đăng nhập. Chưa có câu hỏi của người dùng thật — mọi số đo trên câu tự viết / Golden.
- Kiểm nguồn chỉ kiểm **số nguồn có thật**, không kiểm câu chữ có đúng với nguồn — "có nguồn" chưa phải "đã kiểm nghĩa".
- Từ chối nhầm còn là lỗi nhiều nhất: đoạn chứa đáp án xếp hạng 11–30 (không lọt vào 10 đoạn đưa model), hoặc nằm ngoài cả 30 ứng viên (khoảng một nửa số ca) ⇒ model không thấy nên nói "không đủ thông tin".
- Câu xã giao chờ phân loại xong mới viết ⇒ có lúc chậm (cách chạy song song đã thử 10/11, chưa đạt — không áp dụng).
- Mục web có thể cũ / sai dù đã ghi "chưa kiểm"; với ý ngoài kho, mục web hay chỉ nói "chưa xác minh được".
- Câu hai ý mà code chỉ đếm được một vế (không dấu phẩy, một vế không có từ hỏi, kiểu "A hay B") ⇒ vẫn bị từ chối cả câu.

## Đọc chi tiết (báo cáo kỹ thuật)

Muốn hiểu từng khâu: đọc tiếp các file theo thứ tự trong [README](README.md). Dưới đây là báo cáo kỹ thuật của agent, cho khi cần kiểm sâu.


- Tìm + 10 đoạn ngữ cảnh: `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md` · các cách đã thử ở khâu tìm / trả lời: `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`
- Chữ hiện dần, lượt đo cuối Phase 8: `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`
- Trợ lý Phase 9 (thiết kế, từng bậc): `docs/superpowers/specs/2026-11-02-phase-9-design.md` · `report_agent/2026-11-02_phase_9_code/` · `report_agent/2026-11-08_phase_9_ban_13/TONG_HOP.md`
- Cổng du lịch + biểu mẫu: `report_agent/2026-11-06_giao_dien_cong/c_s3_q_f_implementation.md` · hỏi bằng ảnh: `report_agent/2026-11-05_phase_10_anh/`
- Ngày tính sẵn: `report_agent/2026-11-02_phase_9_code/e_t1_nhanh_implementation.md` · chạy thử bản Docker: `report_agent/2026-11-08_phase_9_ban_13/b_deploy_cuc_bo_implementation.md`
- Dựng lại kho / chạy máy: `guides/full_corpus_rag.md` · mọi phương án đã thử: [91_BAO_CAO_SO_SANH_PHUONG_AN.md](91_BAO_CAO_SO_SANH_PHUONG_AN.md)
