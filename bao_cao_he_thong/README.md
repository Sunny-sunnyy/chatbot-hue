# Báo cáo hệ thống hue_rag — bắt đầu ở đây

> **Đây là sổ ghi việc (quá khứ) của các agent, không phải bài học.** Muốn hiểu hệ thống: đọc [bai_hoc/](../bai_hoc/) theo số, bắt đầu từ bài 0.

Cập nhật 08:27 20/11/2026 (gộp các thay đổi tối 18/11 và cả ngày 19/11: sáu tính năng bật thêm, bỏ hai trần token, các sửa an toàn cho câu bão / lũ; bảng "Số chính" thêm lượt đo cuối 18/11 và bộ 80 kịch bản 19/11; chuyện từng ngày ở [nhat_ky/](nhat_ky/)). Thư mục này viết cho người **không đọc code**. Báo cáo kỹ thuật
của các agent nằm ở `report_agent/` — mỗi file ở đây có mục "Đọc chi tiết" trỏ sang đó. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## Chatbot này là gì

Trợ lý du lịch – văn hoá Huế trên một trang web (gọi là "chatbot" hay "trợ lý" đều là một hệ thống). Người dùng hỏi bằng tiếng Việt có dấu; chatbot
**trả lời từ kho bài viết đã biên soạn** (265 bài về món ăn, di tích, lễ hội, nghệ thuật biểu diễn, du lịch, lưu trú) và ghi nguồn dưới mỗi câu trả lời. Ngoài kho
chỉ có ba thứ: ngày tháng và dự báo thời tiết (code tính / lấy), và mục "Từ web (chưa kiểm)" tách riêng khi kho không có. Kho không có ⇒ nói "không đủ thông
tin" chứ không bịa; câu ngoài chủ đề Huế ⇒ từ chối bằng một câu cố định.

**Làm được (đang chạy):**
- Hỏi đáp về Huế; nhớ 3 câu hỏi gần nhất trong một cuộc trò chuyện (chỉ câu hỏi, không nhớ chữ câu trả lời; từ 19/11 kèm một dòng do code ghi tên các nơi có bài riêng mà câu trả lời vừa trích — xem gạch "Hỏi tiếp về nơi vừa nêu"); chữ hiện dần; dòng "Nguồn" bấm được để đọc đoạn gốc (từ tối 15/11 hiện sạch: in đậm, gạch đầu dòng, bảng) / cả bài; tải lại trang = cuộc trò chuyện mới (tối 15/11).
- Trò chuyện xã giao (chào, cảm ơn, hỏi chatbot là ai).
- Câu hỏi có ngày (hôm nay, cuối tuần, rằm, Tết, ngày âm của lễ hội): **ngày do code tính**, model chỉ diễn đạt. Câu chỉ hỏi về ngày tháng (âm ↔ dương, thứ mấy,
  lễ / Tết ngày nào) được trả lời cả khi không nhắc Huế; câu hỏi việc khác vào ngày đó mà không về Huế (giá vàng, thời tiết nơi khác…) vẫn từ chối.
- Dự báo thời tiết Huế 7 ngày (số lấy từ Open-Meteo, code dựng câu). Câu hỏi bão / lũ (từ 17/11): model không thấy số, code nối câu nhãn (không có tin bão) + bảng mưa + NCHMF / 112. Từ tối 18/11: từ "dông" cũng được coi là câu thiên tai; hỏi tiếp ngay sau một câu bão / lũ thì mục web là câu cố định do code viết (trước: model viết), hai địa chỉ bản tin chính thức đứng đầu danh sách link; model lỗi giữa lượt bão thì lời báo lỗi vẫn kèm bản tin chính thức + 112; chữ Sao chép / Tải lịch và sự kiện `.ics` giữ câu an toàn. Giới hạn đã ghi: từ lượt thứ ba của chuỗi hỏi tiếp sau câu bão, code chỉ xét câu liền trước.
- Hỏi khoảng cách / thời gian đi giữa hai nơi (từ 16/11): code tra bảng km + phút dựng sẵn từ OSRM cho 40 điểm của bảng lịch; model chỉ chọn hai nơi; nơi ngoài bảng ⇒ "chưa có số". Phút = 1,25 × OSRM + 5 (ước, không tính kẹt xe). Câu nêu rõ hai nơi trong bảng ⇒ code tra sẵn trước lần gọi model đầu (nhanh hơn khoảng 2 giây); không chắc ⇒ model gọi công cụ như cũ.
- Kho không có ⇒ tra web một lần, hiện riêng mục "Từ web (chưa kiểm)". Từ 16/11: câu sức khoẻ ⇒ dưới mục web có câu cố định "…nên hỏi dược sĩ hoặc bác sĩ trước khi dùng." (code nối; có thể thừa ở câu sát chủ đề như giờ nhà thuốc). Từ chiều 17/11: nguồn web có ngày đăng (khi Serper cho ngày) thì ghi "(dd/mm/yyyy)" cạnh tiêu đề; nguồn không ngày vẫn có thể là tin cũ.
- "Lên kế hoạch" bản 2 (từ 14/11; bảng 41 điểm từ chiều 15/11; buổi để trống không hiện thành mục): biểu mẫu 5 nhóm (ai đi · bao lâu, ngày đi · kiểu đi · thích gì · hạng chỗ ở, không bắt buộc) ⇒ **code xếp lịch** theo luật (an toàn, giờ mở cửa, mùa, cụm gần, mưa theo dự báo — từ chiều 17/11 ngày mưa mà không chọn sở thích thì bỏ luật "chiều một điểm thiên nhiên"; điểm thêm buổi sáng chừa 60 phút ăn trưa trước giờ chiều; ngày đi xa chưa có dự báo ⇒ dòng "chưa xét mưa") kèm giờ gợi ý, phút đi, ảnh từng điểm; model chỉ viết câu tả từng điểm; tải lịch `.ics` cho lịch điện thoại.
- Bản đồ dưới lịch (bật tối 16/11): mỗi ngày một bộ ghim đánh số theo thứ tự đi, toạ độ từ bảng của code; ô bản đồ từ máy chủ OpenStreetMap Đức; chỉ ghim điểm tham quan + hoạt động tối. Cùng tối sửa ba lỗi hiển thị (số lệch góc ghim, ghim bị dòng ghi công che ở màn hẹp, ghim chồng nhau). Giới hạn: máy chủ ô có lúc chậm ⇒ đổi ngày khung có thể xám vài giây (chưa đo thành số).
- Sửa lịch bằng lời — từ 19/11: câu nêu HAI điểm đang có trong lịch, mỗi điểm kèm buổi muốn dời tới, do code đọc và áp (trước: trợ lý báo "chưa làm được"); bộ 10 chuỗi sửa lịch đạt 7 ⇒ 9 / 10, 0 lượt sửa sai lịch; chỉ đúng một kiểu câu hẹp này, câu khác như cũ. từ trưa 17/11: bỏ một điểm ⇒ lời báo nêu cả điểm được thêm vào chỗ trống. Từ 17/11: câu xin sửa kiểu chưa làm được (đổi chỗ / gộp ngày…) ⇒ lịch giữ nguyên + câu "Chưa làm…" do code viết (trước: trợ lý tự viết lịch chữ như thể đã đổi). Từ tối 16/11 cột lịch của trang "Lên kế hoạch" vẽ bản mới nhất đã sửa xong (nhãn "Đã sửa theo lời bạn: …"; biểu mẫu vẫn là bản gốc); trước đó lịch đã sửa chỉ hiện trong khung trợ lý. (từ 14/11; chiều 15/11 thêm **đổi hạng chỗ ở** — phải nêu hạng — và **đổi ngày đi** — ngày do code đọc từ chữ người dùng): khi đã có lịch, nhắn "bỏ lăng X", "dời Y sang chiều", "thay Z" ⇒ model chỉ hiểu ý, **code** sửa và kiểm luật; đầu lịch ghi "Đã đổi / Không đổi được"; câu khẩn cấp vẫn đi đường khẩn cấp; câu thường trong cuộc có lịch không phải chờ thêm (bản sửa tốc độ chiều 14/11). Tối 15/11: xin đổi tham số mà không đổi được gì ⇒ có dòng báo; đổi được ⇒ thêm dòng "Lịch xếp lại theo lựa chọn mới…" (quá 6 tên thì chỉ nêu số) hoặc "Các điểm trong lịch giữ nguyên chỗ".
- Nơi ở gợi ý trong lịch — **từ chiều 15/11 chỉ hiện khi người dùng hỏi** (chọn hạng sao ở biểu mẫu hoặc nói hạng bằng lời); chưa hỏi ⇒ một dòng link sang trang Chỗ ở (136 cơ sở, 67 có ảnh) kèm gợi ý nhắn hạng sao. Khi hiện: lịch ≥ 2 ngày có thẻ "Nơi ở gợi ý" — **code** chọn một khu cho cả chuyến + ≤ 5 cơ sở của đúng hạng người dùng đã chọn (bản 14/11 chiều trải cả ba hạng) + link tìm phòng; không nêu giá. Từ 15/11: khách chọn được hạng sao (1 sao / đạt chuẩn · 2–3 · 4–5) ở biểu mẫu; link "Xem thêm chỗ ở khu này" mở trang "Chỗ ở" (136 cơ sở theo khu và hạng). Chưa xếp lịch ⇒ trang hiện lịch mẫu "Ví dụ" do bộ xếp dựng. Từ chiều 17/11: lịch 1 ngày đã chọn hạng ⇒ một dòng "Lịch đi trong ngày… chưa gợi ý chỗ ở".
- Thẻ khách sạn trong trò chuyện (15/11): câu trả lời dựa bài lưu trú nêu tên cơ sở trong danh mục ⇒ tới 3 thẻ (ảnh hoặc ô màu, hạng, Bản đồ / Tìm phòng); code khớp tên, không giá.
- Quán ăn trong lịch (cuối chiều 14/11): mỗi bữa **code** gợi ≤ 2 quán ăn trong 2 km (từ chiều 17/11 bữa trưa xét cả các điểm sáng khác rồi điểm đầu chiều khi điểm cuối buổi sáng không có quán: ngày không có bữa trưa 52 ⇒ 0 / 1.890) (quán có bài kho trước, quán bản đồ mở ghi "chưa kiểm"; cà phê chỉ khi không có quán ăn); không giá / giờ; bữa có quán kho 69,1 % với bảng 34 điểm (sau ghi kho 4; 49,3 % là số trước đó) ⇒ **63,9 %** với bảng 41 điểm (14.545 / 22.752 bữa trên 3.840 khung; E đo, A chạy lại khớp 15/11 tối; tụt vì cụm nam xa — Hải Vân, Lập An — thêm bữa mà chưa có quán kho; bữa có quán hoặc ghi chú ăn 85,5 % ⇒ 86,4 % sau ghi chú Tây Hồ / Hải Vân tối 15/11 ⇒ **94,5 %** sau ghi chú phá Tam Giang 16/11). Nơi ở: lịch có buổi tối ở trung tâm ⇒ ở trung tâm. Lịch mẫu cũng có nơi ở + quán. Tối 15/11 thêm ghi chú ăn cho làng nón Tây Hồ và bữa tối sau đèo Hải Vân ⇒ bữa có quán **hoặc** ghi chú 85,5 ⇒ **86,4 %** (đây không phải độ phủ quán: bữa có quán vẫn 75,2 %, quán kho 63,9 %); ảnh đèo Hải Vân đổi sang cửa ải Hải Vân Quan.
- Câu hỏi nối tiếp khi phải tra web (bật chiều 15/11): hỏi tiếp kiểu "mở cửa mấy giờ" mà kho không có ⇒ nếu model đã tự tìm kho ở lượt đó thì câu đem đi tìm là câu tìm kho model vừa viết (thường đã có tên nơi của câu trước), không phải câu cụt; lượt nhiều ý vẫn dùng câu gõ.
- Câu hỏi nhiều ý (14/11 chiều): câu có ≥ 2 vế hỏi ⇒ trả lời vế kho có, vế thiếu ghi "Tư liệu chưa có thông tin về: …" và tra web riêng cho vế đó (trước: từ chối cả câu).
- Ảnh dưới câu trả lời (14/11 chiều): câu trả lời từ một bài về một nơi / món ⇒ code hiện một ảnh của bài, bấm mở bài. Từ 15/11: câu nhắc nhiều nơi / món được trích ⇒ tới 3 ảnh (từ 2 ảnh trở lên thì có tên nơi dưới mỗi ảnh).
- Giao diện mới "Sông Hương" 5 trang (14/11): hiệu ứng nhẹ (tắt khi máy bật giảm chuyển động), ảnh cho 262 / 265 bài ở Khám phá (tối 16/11: thêm ảnh 2 bài quán Lập An; 3 bài để trống theo bạn); không hiện chữ ghi công ảnh (bạn yêu cầu, nguồn giữ trong bảng dữ liệu); trang Giới thiệu có dải "Kho tư liệu", màn "Huế qua các thời kỳ", ba bước trên dòng sông.
- Hỏi kèm ảnh (luồng mới tối 15/11): dấu cộng trong ô nhập hoặc dán ảnh ⇒ ảnh đính kèm câu hỏi, bấm Hỏi mới xử lý ⇒ model đoán tên trong danh sách 42 mục: **một tên ⇒ trả lời luôn từ kho** kèm dòng "Mình đoán trong ảnh là … — có thể sai"; 2–3 tên ⇒ người dùng chọn; không nhận ra ⇒ lời báo. Model trả lời không nhìn ảnh. Từ 16/11: nút **Huỷ** lúc "Đang xem ảnh…" (ảnh về lại ô nhập).
- Cổng du lịch: trang chủ, "Khám phá" đọc thẳng 265 bài (ảnh 262 bài). Khối đánh giá 👍 / 👎 dưới câu trả lời đã gỡ khỏi giao diện tối 15/11 (bạn yêu cầu; đường nhận đánh giá ở máy chủ còn).
- Sổ vết debug (tối 15/11, **chỉ máy local**, mặc định tắt): bật bằng `HUE_SO_VET=true` ⇒ mỗi lượt ghi một bản ghi có nội dung vào `data/debug_trace/` để tìm lỗi khi thử; log số đo thường không đổi; bản công khai không bật.
- Lịch đã lưu đi vào lượt hỏi thường (bật 19/11): cuộc trò chuyện đã có lịch thì mỗi câu hỏi thường nhận thêm một nguồn "Lịch bạn đang có" do code in — từng ngày, buổi, giờ, tên điểm và các số code tính sẵn (số điểm mỗi ngày, giờ bắt đầu, giờ kết thúc, tổng thời lượng tham quan); model chỉ diễn đạt. Trước đó trợ lý không thấy lịch vừa lập nên trả lời trên một lịch mẫu của kho — nói chắc mà sai ở 3 / 3 kịch bản (lượt đo trưa 19/11). Chưa có: tổng tiền vé do code tính (đã thử, không đạt).
- Nói thật giới hạn (bật 19/11): nhờ trợ lý TỰ đặt phòng / bàn / vé, gửi thư hay tin nhắn, xem còn phòng không ⇒ một câu cố định nói rõ trợ lý không làm được việc đó và người dùng tự làm tiếp bằng cách nào; lượt đó không tra web (trước: câu "không đủ thông tin" kèm một mục web lạc đề). Lượt thật: 11 / 12 lượt đích ra đúng câu (ngưỡng ghi trước ≥ 10); lượt còn lại (nhờ gửi lịch qua thư) bị xếp "ngoài phạm vi" — giới hạn đã ghi. Code nhận câu theo danh sách hẹp: sót một số cách nói thì lượt đó chạy như cũ.
- Xuất lịch (bật 19/11): dưới lịch có hai nút **In / Lưu PDF** (in từ trình duyệt) và **Tải PowerPoint**; lúc tải không gọi model — code điền đúng các chữ đã hiện trên trang (tên điểm, giờ, câu tả, ghi chú, câu an toàn của lượt); không có chữ ghi công ảnh; lịch mẫu không có nút. Giới hạn: nút in mới được bấm bằng máy (trình duyệt không màn hình, lịch 2 và 3 ngày), chưa thử trình duyệt khác; chưa có trang chi phí, bản đồ nền; chưa giới hạn số lượt tải — phải thêm trước khi đưa lên mạng.
- Hỏi tiếp về nơi vừa nêu (bật 19/11): sau một câu trả lời từ kho, code ghi vào phần nhớ MỘT dòng tên các nơi có bài riêng mà câu trả lời đã trích (tối đa 5; không lấy chữ model viết, mục web hay lịch) ⇒ hỏi tiếp "cho địa chỉ quán đó" thì trả đúng nơi: 2 / 17 ⇒ 15 / 17 chuỗi đích; lượt nói chắc về SAI nơi 8 ⇒ 0. Bộ bẫy "hỏi tiếp ý kho không có" đạt 5 / 6 — dưới sàn ghi trước; chủ dự án chọn bật và đọc sàn theo mục đích "không trả lời bằng thông tin nơi khác". Giới hạn thấy sau khi bật: hỏi tiếp "kể hết các chỗ vừa nêu" có lúc ra danh sách thiếu (kể đủ 1 / 3 lượt khi bật, 2 / 3 khi tắt) — đang sửa nhỏ.
- Dòng lưu ý "tạm ngừng" (bật 19/11): hỏi quy định / cách tham gia một hoạt động mà bài kho có câu "tạm ngừng khi mưa lũ, có lệnh cấm, thời tiết xấu" ⇒ dưới câu trả lời có một dòng in đậm chép nguyên câu đó của bài (code nối; chữ câu trả lời không đổi). Chỉ hiện khi câu trả lời đã trích đúng bài có cảnh báo: lượt thật 2 / 3, dữ liệu cũ 7 / 7, 0 ca gán nhầm. Bản thêm một câu vào lời dặn đã thử và bỏ (7 câu tụt "Đủ ý", vượt ngưỡng).
- Không còn trần token đầu ra, ngân sách ngữ cảnh mỗi lượt và trần lịch sử (bỏ 19/11, chủ dự án yêu cầu "chất lượng trước"): đếm lại 3.974 lần gọi cũ — 2 lần gọi phân loại có đầu ra đúng bằng trần 512 (một lần chắc chắn bị cắt), 0 lần ở lời gọi trả lời; ngân sách ngữ cảnh chưa lượt nào từng chạm (đầu vào lớn nhất 6.233 token). Tiền và giây nay chỉ đo và báo, không còn là sàn.

**Chưa làm được / chưa bật:** lịch trình từ câu gõ tự do (chỉ qua biểu mẫu) · câu gõ không dấu (ngoài phạm vi — bạn quyết 25/10) · quán "gần đây" / "gần X", sự kiện theo ngày · câu hai ý mà code chỉ đếm được một vế, và câu kho chỉ có một phần (vẫn từ chối cả câu) · câu "những quán nào có đặc điểm X" trả thiếu mục · tổng tiền vé / ngân sách do code tính · số gọi khẩn cấp trong câu trả lời khẩn cấp (ngoài phạm vi — bạn chốt) · hỏi tiếp theo THỨ TỰ ("chỗ thứ hai") và nơi chỉ được nêu qua bài tổng hợp · chưa đưa lên mạng (đã chạy thử bản đóng gói Docker trên máy; AWS làm sau buổi bạn test ở máy local).

**Đã dẹp, không làm:** giọng nói · so ảnh bằng embedding (hoãn) · nhớ sở thích người dùng.

**Đang ở đâu:** lượt đo cuối phần đã thấy đã chạy 18/11 (bảng dưới; bộ kín chưa chạy). Đợt hoàn thiện ở máy local đã đóng danh sách bốn việc, cả bốn đã bật 19/11: lịch đã lưu vào lượt hỏi thường · nói thật giới hạn · xuất lịch · hỏi tiếp về nơi vừa nêu. Còn lại trước buổi bạn test một lần ở máy local: sửa nhỏ lỗi "kể hết", soát bằng model khác hãng, chạy danh sách test bằng trình duyệt thật. Việc đang mở: `session_prompt/VIEC_DANG_MO.md`.

## Số chính (mỗi số chỉ ghi ở đây — file khác trỏ về)

**Tiền và tốc độ (bạn đổi 19/11):** không còn là sàn — chỉ đo và báo; chất lượng trước. Mức từng dùng làm sàn từ 28/10, nay để so: chữ đầu tiên hiện trên trình duyệt ≤ 3 s ở câu giữa (trung vị), ≤ 5 s ở 95 % câu; tiền ≤ 0,0005 USD / câu. **Thứ tự lỗi
nặng → nhẹ:** sai cảnh báo an toàn > nói chắc sai > trả lời câu ngoài kho > thiếu ý > từ chối nhầm.

| Đo gì | Kết quả | Đo lúc nào, trên gì |
|---|---|---|
| Kho | 265 bài → 9.436 đoạn | chỉ mục dựng lại 18:15 16/11 (thêm 2 bài quán ven đầm Lập An); trước 11:22 15/11 (sửa 2 câu năm Tây Sơn); trước 20:21 14/11 (lần ghi kho 6: 16 lễ hội / nghệ thuật) |
| Điểm chất lượng (thang 1–5) | Đúng **4,71** · Đủ ý **4,58** · Trúng ý **4,72** | **bản cuối Phase 8** (01/11), 129 câu Golden có đáp án trong kho (đã bỏ 29 câu ít giống cách người thật hỏi) |
| … loại câu yếu nhất | câu cần ghép nhiều nguồn: Đủ ý **3,50** | như trên (bản đang chạy: dòng "Lượt đo cuối" dưới) |
| **Lượt đo cuối phần đã thấy** — bản đang chạy so với bản cuối Phase 8 chạy lại cùng buổi | "Đủ ý" trung bình **+0,186**, "Đúng" **+0,248** (129 câu; điểm tuyệt đối và "Trúng ý" của lượt này: xem file 10) · câu nhiều nguồn Đủ ý **4,61** so với 3,39 (18 câu) · câu theo ngày dùng được 27 so với 12 / 28 · từ chối nhầm **3** so với 12 / 158 · 0 đảo cảnh báo mới, 0 nói chắc sai mới, 0 lỗi trích dẫn · 0 / 44 câu ngoài phạm vi bị trả lời · biểu mẫu lịch 12 / 12 hai lượt. **Không đạt sàn ghi trước:** 1 / 18 câu ngoài kho của bộ câu mẫu bị tính "đã trả lời" (từ chối sai khuôn, không bịa số) · 6 câu tụt "Đủ ý" (cho phép 4) · an toàn: 2 câu thiếu cảnh báo mới, 1 câu sai điều kiện mới ở một lượt · sửa lịch bằng lời 7 / 10. **Chưa đo:** các bộ kín; tốc độ theo định nghĩa sàn | 18/11, bộ câu mẫu 176 + bộ an toàn 32 hai lượt + các bộ theo việc; sau lượt này đã sửa bằng code: câu thiếu cảnh báo "tạm ngừng" và sửa lịch 7 ⇒ 9 / 10 (19/11) — **các mục còn lại chưa đo lại** |
| Bộ 80 kịch bản việc phổ thông (đo việc người dùng thật hay làm: hỏi đáp, gợi ý quán / chỗ ở, lịch, nhờ làm thay) | xong việc **51 ⇒ 58 / 80** sau khi bật bốn việc của danh sách đóng; 0 kịch bản có điều sai mới; hai người chấm lệch 1 / 80 | 19/11: một lượt trước và một lượt sau khi bật, cùng bộ 80 kịch bản soạn trong ngày |
| Từ chối nhầm (kho có đáp án mà nói "không đủ thông tin") | **4–6 / 158** câu (mỗi lần chạy lại ra 4–6 vì model viết hơi khác mỗi lần); trước khi có "tìm thêm": 12 / 158 | 158 câu Golden có đáp án trong kho, 03/11 (lượt 18/11: 3 / 158 — dòng "Lượt đo cuối") |
| Câu ngoài kho mà phần trả lời từ kho vẫn trả lời | **0** trên mọi bộ đã đo | 18 câu Golden ngoài kho + bộ an toàn (mục web ghi riêng, không tính ở đây) |
| An toàn (vé, giờ, quy định, cảnh báo) | 0 câu đảo cảnh báo; 2 câu nói sai điều kiện kiểu mới (vd ghi sai giờ) — đúng ngưỡng cho phép ≤ 2, bản trước sinh lại cũng sai y vậy | bộ 32 câu an toàn, lượt đo cuối Phase 8 (01/11); mỗi phần mới của Phase 9 đều đo lại bộ này trước khi bật; số của bản đang chạy: dòng "Lượt đo cuối" |
| Tốc độ tới **chữ đầu tiên** (trung vị / 95 % câu) | câu về Huế **2,16 / 4,32 s** ✓ · câu có ngày **2,35 / 4,56 s** ✓ · ngoài phạm vi 1,62 / 2,97 s ✓ · **xã giao 3,46 / 7,73 s ✗** | trình duyệt thật, chạy một lần trên 65 câu (09/11); câu có ngày: 19 câu (10/11). Thời gian tới lúc xong cả câu chưa đo chung. **Bản 29 tính năng bật: chưa đo lại** theo cách này — chỉ có quan sát 18/11: chữ đầu trung vị 2,5 s, 95 % câu 11,8 s trên 27 câu; 6 / 8 lượt thật câu thời tiết > 5 s |
| Tiền một câu (theo bảng giá OpenAI, gồm cả phí lưu tạm) | câu về Huế **0,00047 USD** (~12 đồng, sát trần) · câu có ngày 0,00036 USD | cùng lượt trên; lượt 18/11: **0,00044 USD** / câu về Huế (158 câu, không có câu tra web). Sau khi bỏ trần token 19/11: **chưa đo lại** |
| Hỏi bằng ảnh | tên đúng nằm trong 3 gợi ý ở **22 / 25** ảnh; đoán mất ~3 s (chậm nhất 6–9 s ✗). Luồng mới 15/11 (đếm lại kết quả đã lưu, 66 lượt): model đưa một tên thì đúng 31 / 33 lượt; cách "một tên trả lời luôn, 2–3 tên hỏi chọn" còn 6 / 66 lượt trả lời sai nơi (trả lời luôn mọi lượt: 14 / 66) | 05/11; đếm lại 15/11 |

**Bản cuối Phase 8 khác bản đang chạy ở đâu:** Phase 8 chỉ có "tìm 10 đoạn → model trả lời". Bản đang chạy thêm bước phân loại câu, tìm thêm, nhớ câu hỏi, tra web,
thời tiết, ngày, biểu mẫu, ảnh. Mỗi phần mới được đo riêng trên bộ câu của nó trước khi bật; cả hệ mới đã đo lại trên bộ 176 câu ngày 18/11 (dòng "Lượt đo cuối"; bản lúc đó chưa có sáu tính năng bật 19/11).

## Từ hay gặp

| Từ | Nghĩa |
|---|---|
| kho | 265 bài Markdown đã biên soạn — nguồn sự thật của câu trả lời |
| đoạn | một mẩu của bài (một đoạn văn, một mục danh sách, một dòng bảng) — đơn vị để tìm và trích nguồn |
| vector nghĩa | dãy 384 con số đại diện cho *ý nghĩa* một đoạn; hai đoạn cùng ý thì gần nhau (tính bằng model nhỏ e5-small, chạy ngay trên máy) |
| BM25 | cách chấm theo **từ trùng** giữa câu hỏi và đoạn |
| RRF | cách gộp hai bảng xếp hạng (theo nghĩa, theo từ): đoạn đứng cao ở cả hai thì lên đầu |
| chỉ mục | các đoạn + vector nghĩa + bảng từ khoá, dựng ra từ kho và cất trong Qdrant — thứ chatbot thật sự tìm trong đó; kho đổi thì phải dựng lại |
| Qdrant | cơ sở dữ liệu cất chỉ mục để tìm nhanh (một "collection" = một chỉ mục trong Qdrant) |
| ngữ cảnh | 10 đoạn tìm được, gửi cho model cùng câu hỏi |
| model | `gpt-6-luna` của OpenAI — đọc ngữ cảnh rồi viết câu trả lời |
| token | đơn vị chữ mà model đếm (một từ tiếng Việt ≈ 1–2 token); tiền tính theo token |
| lời dặn | hướng dẫn cố định gửi kèm mọi câu cho model (cách trả lời, khi nào từ chối) |
| phân loại câu hỏi | một lần gọi model ngắn xếp câu vào 4 loại: xã giao / về Huế / ngoài phạm vi / khẩn cấp. Khẩn cấp được trả lời như câu về Huế, chỉ đánh dấu riêng trong log để theo dõi |
| công cụ | việc code làm khi model yêu cầu: tìm thêm trong kho, đổi ngày, lấy dự báo |
| Golden | bộ 176 câu hỏi chuẩn có đáp án mẫu, dùng để chấm |
| chấm mù | một model khác (Claude) chấm từng câu trả lời so với đáp án mẫu, **không biết** câu đó của bản nào. Đúng = không sai so với đáp án; Đủ ý = có đủ các ý của đáp án; Trúng ý = trả lời thẳng điều được hỏi, không lan man |
| bộ kín | bộ câu người sửa code không được xem, chỉ mở một lần để kiểm cuối |
| sàn | mức tối thiểu ghi **trước** khi đo; không đạt ⇒ không đưa vào chatbot |
| cờ | công tắc bật / tắt một tính năng trong cấu hình |
| trung vị / p95 | trung vị = câu ở giữa; p95 = 95 % câu nhanh hơn số này |
| Docker, AWS | Docker = đóng gói chatbot thành một khối chạy được trên máy khác; AWS = dịch vụ thuê máy chủ của Amazon |
| Phase | giai đoạn của đồ án: 0–8 dựng chatbot hỏi đáp từ kho và chọn cách làm tốt nhất; 9 trợ lý có công cụ; 10–12 ảnh, bản đồ, đưa lên mạng (giọng nói đã dẹp) |

## Thứ tự đọc (theo dòng chảy dữ liệu)

| Số | File | Đọc để biết |
|---:|---|---|
| 01 | [01_LUONG_HOAT_DONG_HE_THONG.md](01_LUONG_HOAT_DONG_HE_THONG.md) | Một câu hỏi đi qua những bước nào; một ví dụ trọn vẹn; dữ liệu người dùng gửi đi đâu |
| 02 | [02_BAO_CAO_KHO_DU_LIEU.md](02_BAO_CAO_KHO_DU_LIEU.md) | Kho lấy từ đâu, đã sửa gì, còn thiếu gì |
| 03 | [03_BAO_CAO_CHIA_DOAN.md](03_BAO_CAO_CHIA_DOAN.md) | Bài được cắt thành đoạn thế nào, vì sao cắt vậy |
| 04 | [04_BAO_CAO_EMBEDDING_TU_KHOA.md](04_BAO_CAO_EMBEDDING_TU_KHOA.md) | Đoạn biến thành vector nghĩa + từ khoá ra sao, vì sao chọn model nhỏ |
| 05 | [05_BAO_CAO_LUU_TRU_QDRANT.md](05_BAO_CAO_LUU_TRU_QDRANT.md) | Cất ở đâu, khi nào phải dựng lại |
| 06 | [06_BAO_CAO_TIM_KIEM.md](06_BAO_CAO_TIM_KIEM.md) | Chọn 10 đoạn nào cho một câu hỏi, vì sao hay từ chối nhầm |
| 07 | [07_BAO_CAO_SINH_CAU_TRA_LOI_API.md](07_BAO_CAO_SINH_CAU_TRA_LOI_API.md) | Trợ lý viết câu trả lời: phân loại, công cụ, kiểm nguồn, giao diện |
| 08 | [08_BAO_CAO_HOI_BANG_ANH.md](08_BAO_CAO_HOI_BANG_ANH.md) | Hỏi bằng ảnh làm gì, đúng tới đâu |
| 09 | [09_BAO_CAO_BO_CAU_HOI_GOLDEN.md](09_BAO_CAO_BO_CAU_HOI_GOLDEN.md) | Bộ câu chuẩn dùng để đo gồm gì, soạn thế nào |
| 10 | [10_BAO_CAO_DANH_GIA.md](10_BAO_CAO_DANH_GIA.md) | Chấm thế nào, tốt tới đâu, yếu ở đâu |

**Hồ sơ tra (ngoài đường đọc):** [91_BAO_CAO_SO_SANH_PHUONG_AN.md](91_BAO_CAO_SO_SANH_PHUONG_AN.md) (mọi cách đã thử / chọn / bỏ) ·
[90_BAO_CAO_NEN_TANG.md](90_BAO_CAO_NEN_TANG.md) (dự án dựng trên gì) · [92_BAO_CAO_NGHIEN_CUU_PHASE_9.md](92_BAO_CAO_NGHIEN_CUU_PHASE_9.md) +
[93_DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md](93_DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md) (vì sao làm Phase 9 – 12) · [94_DE_XUAT_SUA_CODE.md](94_DE_XUAT_SUA_CODE.md)
(đợt dọn code 25–26/10) · [nhat_ky/](nhat_ky/) (chuyện từng ngày).

## Luật cập nhật (cho agent — bạn bỏ qua mục này)

- Thay đổi vào hệ thống đang chạy ⇒ sửa đúng file khâu bị chạm + 1 dòng nhật ký ngày đó; LUONG chỉ khi đường đi của câu hỏi đổi; số chung ⇒ **chỉ** bảng
  "Số chính" ở trên (file khác trỏ về, không chép số). Quy tắc đủ: `session_prompt/WORKFLOW.md` §6.
- Thân bài lời thường: không mã việc, mã commit, tên hàm, file:dòng — gom vào mục "Đọc chi tiết" cuối file. Phương án đã bỏ: 1 dòng + trỏ `91_BAO_CAO_SO_SANH_PHUONG_AN.md`.
- Phần "đang chạy" của file khâu ≤ ~40 dòng; LUONG ≤ ~120 dòng. Không dòng "Trước: …", không khối "Mới ngày …" (git + nhật ký giữ lịch sử). Giờ lấy bằng `date`.
