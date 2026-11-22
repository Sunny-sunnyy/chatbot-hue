# Bài 30 — Quanh một lịch: chỗ ở, quán ăn, ảnh, bản đồ, xuất file

*Cập nhật 13:16, ngày 22/11/2026 · đã sửa theo một lượt đối chiếu độc lập · luật chọn và lời báo đọc từ chương trình trưa 22/11; số cơ sở, số quán, số ảnh đếm lại từ các bảng đang chạy; số đo cũ chép từ báo cáo các ngày 14–20/11; người viết không chạy lại lượt nào.*

**Bài trước đã biết:** chương trình xếp lịch, kiểm khung, model viết mỗi mục một mô tả (bài 27–29).
**Bài này thêm:** những thứ đi kèm một lịch: khối "Nơi ở", quán cho bữa trưa và bữa tối, ảnh từng điểm, bản đồ có ghim, và năm nút xuất (sao chép, tải chữ, thêm vào lịch điện thoại, in, PowerPoint). Mọi thứ trong bài đều do chương trình chọn; model không thấy tên quán, tên khách sạn hay toạ độ nào.

## Ý chính

- **Chỗ ở** chỉ hiện khi người dùng đã chọn hạng sao: một khu cho cả chuyến, rồi tối đa 5 trong 136 cơ sở. Luật chọn khu nhìn **buổi tối trước**: tối nào cũng ở trung tâm thì ở trung tâm. Không có giá phòng.
- **Quán ăn**: mỗi bữa nhiều nhất 2 quán, cùng cụm, cách điểm không quá 2 km, quán có bài trong kho trước. Phần lớn 467 quán của bảng lấy từ bản đồ mở, mang nhãn "chưa kiểm".
- **Ảnh** của 40 trên 41 điểm nằm sẵn trên máy của dự án; trang không hiện dòng ghi công. **Bản đồ** ghim điểm theo thứ tự đi của từng ngày, toạ độ lấy từ bảng; không vẽ đường đi.
- Sao chép, tải chữ, thêm vào lịch điện thoại và in đều dựng **trong trình duyệt**, không gửi gì đi. PowerPoint dựng **ở máy chủ**, từ lịch đã lưu của cuộc trò chuyện; máy chủ không nhận lịch nào từ trình duyệt.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| khu ở | **lodging zone** | một trong ba vùng để gợi ý chỗ ở: trung tâm hai bờ sông Hương, phía tây yên tĩnh (Kim Long, Thủy Xuân), ven biển – đầm phá |
| cơ sở lưu trú | **lodging** | khách sạn, nhà nghỉ, homestay trong danh mục công khai có hạng sao |
| bản đồ mở | **OpenStreetMap** | bản đồ do cộng đồng soạn, ai cũng dùng được; cũng là nơi lấy ô nền của bản đồ |
| ô nền bản đồ | **map tile** | các mảnh ảnh vuông ghép thành nền bản đồ, trình duyệt tải từ một máy chủ bản đồ |
| ghim | **marker** | dấu tròn có số trên bản đồ, đánh dấu một điểm của lịch |
| tệp lịch điện thoại | **.ics** | một dạng file mà ứng dụng lịch của điện thoại và máy tính đọc được để thêm sự kiện |

## Chỗ ở: chọn một khu theo buổi tối, rồi tối đa năm cơ sở

Lịch ví dụ (bài 27) không chọn hạng sao, nên dưới lịch chỉ có một dòng: "Cần chỗ ở? Xem gợi ý theo khu, hoặc nhắn trợ lý hạng sao bạn muốn (ví dụ “ở khách sạn 3 sao”)." Bấm vào là sang trang Chỗ ở. Khối "Nơi ở" chỉ hiện khi người dùng đã chọn hạng ở biểu mẫu, hoặc đã nói hạng bằng lời (bài 31). Lịch 1 ngày không có đêm nào nên không có khối; người đã chọn hạng thì đọc thấy "Lịch đi trong ngày (không có đêm nào) nên mình chưa gợi ý chỗ ở."

**Chọn khu.** Chương trình xét ba khu theo thứ tự:

1. Lịch có hoạt động buổi tối và mọi buổi tối đều ở trung tâm ⇒ ở trung tâm, lý do "Khu trung tâm — các buổi tối của lịch đều ở trung tâm, về chỗ ở gần."
2. Không thì đếm cụm của các điểm ban ngày (bỏ các điểm đi trong ngày ở phía nam xa). Từ 60 % điểm ở ven biển ⇒ ven biển. Hơn 50 % ở phía tây ⇒ phía tây, trừ khi có trẻ em hay người lớn tuổi thì về trung tâm.
3. Còn lại ⇒ trung tâm.

Bộ xếp chỉ đặt buổi tối ở hai cụm trung tâm (bài 28), nên bậc 1 gần như luôn quyết: mô phỏng 3.840 tổ hợp ra trung tâm 3.036 khung, ven biển 36, phía tây 0 (còn lại là lịch 1 ngày).

**Chọn cơ sở.** Trong khu đã chọn, chương trình lấy tối đa 5 cơ sở của đúng hạng người dùng chọn (hạng đó trống thì trải đều các hạng), gần cụm có nhiều điểm nhất trước, có ảnh trước. Mỗi cơ sở có tên, hạng, địa chỉ, link tìm phòng trên một trang đặt phòng công khai (chỉ mở khi bấm), link bản đồ, và nhãn chung "Gợi ý theo vị trí và hạng — chưa kiểm giá, phòng trống." Bảng lưu trú có 136 cơ sở từ danh mục công khai có nguồn và ngày: 121 ở trung tâm, 5 phía tây, 10 ven biển; 67 cơ sở có ảnh.

## Quán ăn: hai quán mỗi bữa, cùng cụm, trong 2 km

Với mỗi ngày, chương trình tìm quán cho hai bữa:

- **Bữa trưa** gần điểm cuối buổi sáng. Không có quán trong 2 km thì xét các điểm sáng còn lại, rồi điểm đầu buổi chiều.
- **Bữa tối** gần hoạt động buổi tối; ngày không có hoạt động tối thì gần điểm cuối buổi chiều.

Một quán được chọn khi cùng cụm với điểm và cách điểm không quá 2 km đường chim bay. Bữa chính chỉ gợi ý quán ăn; chỉ khi trong 2 km không có quán ăn nào mới gợi ý quán cà phê. Trong cùng loại: quán có bài trong kho trước, rồi dữ liệu mở của thành phố, rồi bản đồ mở; sau đó gần nhất trước. Không lặp quán trong cả chuyến.

Ở lịch ví dụ, bữa trưa ngày 3 gần Bao Vinh chỉ có một quán, nhãn "(từ bản đồ mở, chưa kiểm)". Quán có bài trong kho có link "Đọc bài". Cuối khối có câu "Gợi ý theo vị trí — chưa kiểm giờ mở cửa, giá; quán có thể đã đổi." Bảng có 467 quán: 41 có bài trong kho, 4 từ dữ liệu mở của thành phố, 422 từ bản đồ mở. Sáu nơi xa có một câu ghi chú cố định thay cho tên quán khi không chọn được quán (năm câu dựa trên kho, một câu chỉ nói chưa có gợi ý).

## Ảnh và bản đồ: lấy từ bảng, không đoán

**Ảnh.** Mỗi điểm nhiều nhất một ảnh, gắn theo mã điểm. 40 trên 41 điểm có ảnh: 26 từ Wikimedia Commons (giấy phép mở), 13 ảnh web (phần lớn dùng lại ảnh của mục Khám phá), 1 ảnh chủ dự án tự tìm. Mọi ảnh nằm trên máy của dự án. Lúc bật, máy chủ kiểm từng dòng của bảng ảnh: file có thật, ảnh Commons có tác giả và giấy phép, ảnh web có trang nguồn. Trang không hiện dòng ghi công (chủ dự án yêu cầu 14/11, nhắc lại 19/11).

**Bản đồ.** Dưới lịch có một khung bản đồ, mỗi lần hiện một ngày; nút "Ngày 1 / Ngày 2…" đổi ngày. Ghim có số theo thứ tự đi trong ngày, khớp danh sách đánh số dưới bản đồ. Bấm ghim thì hiện tên điểm và link mở Google Maps. Toạ độ do chương trình lấy từ bảng toạ độ; model không tạo toạ độ, và toạ độ không vào tin gửi model. Điểm không có toạ độ thì không có ghim. Bản đồ không vẽ đường nối giữa các ghim, vì hệ thống không có đường đi thật. Hai ghim sát nhau thì ghim sau được vẽ lệch sang một chút để khỏi che số.

## Năm nút xuất: bốn ở trình duyệt, một ở máy chủ

| Nút | Dựng ở đâu | Từ đâu | Điều cần biết |
|---|---|---|---|
| Sao chép lịch | trình duyệt | bản chữ của lịch máy chủ gửi kèm (cùng nội dung với thẻ) | báo "Đã sao chép lịch."; trình duyệt chặn thì "Trình duyệt không cho sao chép — dùng nút Tải về." |
| Tải về (.txt) | trình duyệt | như trên | file chữ thường, bỏ dấu in đậm |
| Thêm vào lịch (.ics) | trình duyệt | khung lịch đang hiện | chỉ khi đã chọn ngày đi ("Chọn ngày đi ở biểu mẫu để thêm lịch vào lịch điện thoại."); mục không có giờ thì bỏ; câu an toàn bão lũ (nếu có) đứng đầu phần mô tả |
| In / Lưu PDF | khung in của trình duyệt | bố cục in riêng của thẻ lịch | chỉ có ở trang Lên kế hoạch |
| Tải PowerPoint | máy chủ | lịch đã lưu của cuộc trò chuyện | báo "Đang tạo file…", rồi "Đã tải lich-trinh-hue.pptx (lịch mới nhất của cuộc trò chuyện)." |

Bấm "Tải PowerPoint", trình duyệt chỉ báo "tôi muốn tải lịch của cuộc trò chuyện này"; không gửi nội dung lịch. Máy chủ dựng lại lịch từ khung và câu mô tả đã lưu bằng đúng các hàm dựng thẻ (không xếp lại, không gọi model), rồi vẽ file. Không có lịch đã lưu thì người dùng nhận "Chưa có lịch để tải hoặc lịch đã hết hạn — bấm Lên kế hoạch để tạo lại rồi tải."

## Quyết định và lý do

### 1. Vì sao chỗ ở, quán, ảnh, toạ độ đều do chương trình chọn, và model không thấy chúng?

- **Đã chọn:** chương trình chọn khu, cơ sở, quán, ảnh, toạ độ từ các bảng. Những khối này không vào tin gửi model; lượt lập lịch và lượt sửa lịch cũng không được giữ làm "câu trả lời liền trước" cho lượt sau.
- **Vì sao:** luật thiết kế của trang: model không chọn ảnh, không bịa quán, không nói giá phòng. Tên quán từ bản đồ mở là chữ người ngoài viết: chương trình ghi rõ model không được thấy, và lọc ký tự lạ, đường link trong tên trước khi hiện.
- **Cách khác:** để model gợi ý quán, khách sạn từ kho: không làm.
- **Cái giá:** gợi ý chỉ tốt bằng bảng. Hỏi trợ lý "ăn gì gần X" thì trợ lý đọc kho, không đọc bảng quán của lịch, nên có lúc hai bên nói khác nhau.

### 2. Vì sao khu ở được chọn theo buổi tối trước, rồi mới đếm điểm ban ngày?

- **Đã chọn:** lịch có buổi tối và mọi buổi tối ở trung tâm ⇒ ở trung tâm.
- **Vì sao:** chiều 14/11, người review lịch ví dụ thấy lịch gợi ý ở phía tây (3 trên 5 điểm ban ngày ở đó) trong khi mọi buổi tối ở trung tâm. Luật cũ đã qua chấm 10 trên 10, vì bảng đưa người chấm **không có cột buổi tối**. Nhóm thử hai cách, mỗi cách một người chấm mới đọc cùng 10 lịch.
- **Cách khác:** đếm điểm buổi tối như một điểm ban ngày: đã đo, 8 trên 10, dưới sàn 9 ⇒ bỏ. Cách đang dùng: 10 trên 10.
- **Cái giá:** khu phía tây gần như không bao giờ được gợi ý nữa (0 trên 3.840 khung). Một lần chấm đạt chỉ nói được điều bảng chấm cho người chấm thấy.

### 3. Vì sao không hiện giá phòng?

- **Đã chọn:** khối "Nơi ở" và trang Chỗ ở không có giá, không có "còn phòng"; nhãn hạng ghi số sao, không ghi "rẻ / đắt".
- **Vì sao:** luật nhóm đặt từ 05/11 (phần tra web: không nói giá phòng) được giữ khi làm phần chỗ ở. Ngày 14/11 chủ dự án chọn phương án đa số của nhóm cho chỗ ở, phương án đó không có giá; riêng câu "có nên hiện giá phòng không" chưa hỏi chủ dự án (sổ hiện trạng ghi "chưa hỏi, không tự mở"). Giá do trang đặt phòng hiện khi người dùng bấm link. Hạng sao không phải giá, nên ô biểu mẫu ghi "1 sao / 2–3 sao / 4–5 sao".
- **Cách khác:** hiện khoảng giá có nguồn: không làm (luật nhóm đã ghi).
- **Cái giá:** người dùng phải bấm sang trang khác mới biết giá. Câu hỏi chi phí chung ở ô hỏi đáp vẫn nêu khoảng giá có nguồn từ kho.

### 4. Vì sao file chữ, tệp lịch điện thoại và bản in dựng ở trình duyệt, còn PowerPoint dựng ở máy chủ?

- **Đã chọn:** bốn nút đầu dựng trong trình duyệt từ thứ đang hiện. PowerPoint dựng ở máy chủ bằng một thư viện Python, từ lịch đã lưu.
- **Vì sao:** bốn nút đầu chỉ đổi cách hiện thứ trình duyệt đã có (bài 5), không cần gửi gì đi (điều thấy được; chưa thấy ghi lý do riêng). Chủ dự án chọn thư viện Python cho PowerPoint ngày 19/11, sau một lần tra cứu công khai, không có số đo. Kế hoạch viết sau đó có bảng so với thư viện chạy trong trình duyệt; lợi được nêu: test bằng Python sẵn có; máy chủ dựng lại từ bản đã lưu nên mọi chữ trong file là chữ của bảng hoặc câu đã kiểm. Bảng so còn nêu "khuôn làm tay, dễ đẹp", nhưng chương trình hiện vẽ bằng toạ độ, không dùng khuôn.
- **Cách khác:** dựng PowerPoint trong trình duyệt: nêu trong bảng so, không chọn. Bên đó tải được cả khi lịch hết hạn, và máy chủ không tốn gì.
- **Cái giá:** chỉ tải được trong 30 phút từ lượt cuối; nút ở thẻ lịch cũ vẫn tải lịch mới nhất của cuộc; mỗi lần bấm máy chủ dựng file, chưa giới hạn số lượt tải, phải thêm trước khi đưa lên mạng.

Quyết định về ảnh (tự lưu, không ghi công) và về ô nền bản đồ nằm ở nửa để tra.

## Nếu… thì sao

Lời báo trong ngoặc kép là nguyên văn. Các dòng đọc từ chương trình, chưa thử thật, trừ chỗ ghi khác.

| Nếu | Hệ thống làm gì | Người dùng thấy gì |
|---|---|---|
| không có quán nào trong 2 km, cùng cụm | không có dòng cho bữa đó; sáu nơi xa có câu ghi chú từ kho | ví dụ "Chưa có gợi ý quán gần làng (cách trung tâm khoảng 12 km) — nên ăn ở trung tâm trước hoặc sau khi ghé làng." |
| khu ven biển phía đó không có cơ sở | về khu trung tâm | "Khu trung tâm — ven biển phía này chưa có cơ sở trong danh mục." |
| bấm PowerPoint khi lịch đã hết hạn hoặc máy chủ vừa khởi động lại | không dựng file | "Chưa có lịch để tải hoặc lịch đã hết hạn — bấm Lên kế hoạch để tạo lại rồi tải." |
| mất mạng tới máy chủ ô bản đồ | ghim vẫn vẽ trên nền xám | danh sách đánh số dưới bản đồ vẫn đủ (đã thấy nền xám vài giây khi máy chủ đó chậm, 16/11) |
| bấm "Thêm vào lịch" khi chưa chọn ngày đi | không tạo file | "Chọn ngày đi ở biểu mẫu để thêm lịch vào lịch điện thoại." |

## Dễ nhầm

- **"Model gợi ý quán và khách sạn."** Không. Chương trình chọn từ bảng; model không thấy tên quán hay khách sạn nào.
- **"Bản đồ vẽ đường đi giữa các điểm."** Không. Chỉ có ghim theo thứ tự; hệ thống không có đường đi thật.

## Câu hỏi tự kiểm

Thử trả lời bằng lời của mình trước khi bấm mở đáp án.

<details>
<summary>1. Lịch 3 ngày có mọi buổi tối ở trung tâm, phần lớn điểm ban ngày ở phía tây. Gợi ý ở đâu, vì sao?</summary>

Ở trung tâm: luật xét buổi tối trước. Luật này có sau khi người review thấy lịch gợi ý phía tây trong khi tối nào khách cũng về trung tâm; cách đếm cũ đã qua chấm vì bảng chấm thiếu cột buổi tối.

</details>

<details>
<summary>2. Vì sao "gần" là 2 km?</summary>

Mô phỏng đầu không giới hạn ra quán "gần" tới 9,3 km ở mức 95 %, vì có cụm rất rộng. Giới hạn 2 km giữ đúng nghĩa chữ "gần"; cái giá là nơi xa có bữa không có tên quán.

</details>

<details>
<summary>3. Bấm "Tải PowerPoint", trình duyệt gửi gì lên máy chủ?</summary>

Chỉ lời "tải lịch của cuộc trò chuyện này", không có nội dung lịch. Máy chủ dựng lại lịch từ bản đã lưu, nên không nhận chữ nào từ trình duyệt; lịch hết hạn thì không tải được.

</details>

## Cấu hình đang chạy

*Theo cấu hình và chương trình trưa 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| `luu_tru_lich` | đang mở (từ 14/11) | khối "Nơi ở"; chỉ chương trình, không thêm lần gọi model | — |
| `lich_trinh_bang_luu_tru` | bảng bản 6: 136 cơ sở, 67 có ảnh | danh mục công khai có nguồn và ngày | bản 3: 137 cơ sở; các bản rà ảnh 15/11 |
| ngưỡng khu ven biển / phía tây | ≥ 60 % / > 50 % điểm ban ngày | ngày ra biển thường là đi trong ngày | bậc "buổi tối ở trung tâm" đứng trước |
| số cơ sở | ≤ 5; trải 2 (4–5 sao) · 2 (2–3 sao) · 1 (1 sao) | để khách tự chọn hạng | trước: xếp theo tên trong cả mức làm 5 sao không bao giờ hiện (0 / 6.108); đã sửa |
| `quan_lich` | đang mở (từ 14/11) | quán mỗi bữa; chỉ chương trình | — |
| `lich_trinh_bang_quan` | bản 2 (21/11): 467 quán | kho 41 + dữ liệu mở 4 + bản đồ mở 422 | bản 1 có thêm một quán đã đóng cửa |
| số quán / khoảng cách | ≤ 2 quán; ≤ 2 km chim bay, cùng cụm | mục "Quyết định nhỏ hơn" | không giới hạn: bỏ |
| `anh_lich` | đang mở (từ 14/11) | ảnh từng điểm | — |
| `lich_trinh_bang_anh` | bản 7: 40 / 41 điểm | 26 Commons + 13 web + 1 ảnh chủ dự án | bản 6 đổi ảnh đèo Hải Vân; bản 7 đổi ảnh lăng Thiệu Trị |
| `ban_do_lich` | đang mở (từ tối 16/11) | bản đồ dưới lịch; chủ dự án chọn bật | — |
| `lich_trinh_toa_do` | bảng toạ độ 41 dòng, 40 có vị trí | ghim | bản cũ 18 điểm |
| ô nền bản đồ | máy chủ cộng đồng bản đồ mở ở Đức | máy chủ chính lỗi bắt tay ở mạng đã thử (16/11); chủ dự án chọn | — |
| dòng ghi nguồn bản đồ | tắt | chủ dự án chọn 21/11; phải xem lại trước khi công khai | — |
| `xuat_pptx` | đang mở (từ 21:30 19/11) | nút in và nút PowerPoint; chủ dự án chọn bật | — |
| giới hạn số lượt tải PowerPoint | chưa có | phải thêm trước khi đưa lên mạng | — |

## Đã so

**Khu ở theo buổi tối (14/11, chỉ chương trình, 0 USD; người chấm là các phiên làm việc, mỗi lượt một người mới):**

| Luật | Người chấm, cùng 10 lịch (sàn 9 / 10) | Mô phỏng 3.840 khung | Kết luận |
|---|---|---|---|
| đếm cụm điểm ban ngày (bản đầu) | 9 / 10, rồi 10 / 10 — bảng chấm thiếu cột buổi tối | có khung gợi ý phía tây dù tối ở trung tâm | thay |
| đếm điểm tối như điểm ngày | 8 / 10 | — | bỏ |
| buổi tối ở trung tâm ⇒ ở trung tâm | 10 / 10 | trung tâm 3.036 · ven biển 36 · phía tây 0 | giữ |

**Quán ăn (mô phỏng mọi tổ hợp, 0 USD):** bữa có dòng gợi ý 86,4 % ⇒ 94,5 % (22.752 bữa) sau khi thêm ghi chú cho nơi xa; bữa có tên quán 75,2 %. Ngày không có bữa trưa 52 ⇒ 0 trên 1.890 ngày mô phỏng sau khi bữa trưa được xét thêm các điểm sáng khác và điểm đầu buổi chiều (17/11); 101 / 960 khung đổi quán bữa tối vì luật không lặp quán.

**Ảnh (14/11):** một người xem mù kiểm 10 lịch, ảnh đúng điểm 10 / 10, một ảnh lăng ghi "đúng loại, không chắc đúng lăng".

**Tệp lịch điện thoại:** kiểm trên 44 lịch đã lưu, 33 lịch có ngày đi cho ra 288 sự kiện; một trình đọc độc lập báo 0 lỗi. Chưa thử mở trên Google Calendar.

**Bản đồ (16/11):** ba lịch thật 1, 2, 3 ngày, số ghim bằng số điểm có toạ độ, số trên ghim đúng thứ tự; ảnh chụp màn hình lộ thêm ba lỗi phép đếm không bắt (số lệch góc ghim, ghim thấp bị dòng ghi công che, hai ghim gần nhau che nhau), đều đã sửa.

**Giới hạn của phép đo:** các phép trên đếm khung lịch và bảng, không đo người dùng thật có thấy gợi ý hữu ích không.

## Quyết định nhỏ hơn

**Vì sao "gần" là 2 km, và bữa chính chỉ gợi ý quán ăn?** **Đã chọn:** cùng cụm và không quá 2 km đường chim bay; quán ăn trước, cà phê chỉ khi không có quán ăn nào. **Vì sao:** lần mô phỏng đầu không giới hạn khoảng cách: quán "gần" ở mức 95 % là 9,3 km, vì có cụm rất rộng (phá, biển, lăng xa), nên dòng "ăn gần X" sai nghĩa. Luật quán ăn trước có sau khi phiên điều phối thấy bữa tối gợi ý một quán cà phê có bài kho đứng trước quán ăn (14/11). **Cách khác:** không giới hạn khoảng cách: đã đo, bỏ. **Cái giá:** nơi xa ít quán thì bữa không có tên quán: trên mọi tổ hợp, chỉ 75,2 % bữa có tên quán (bảng ở nửa để tra).

**Vì sao ảnh nằm trên máy của dự án, và không hiện ghi công?** Trang web của dự án có một luật an toàn: chỉ hiện ảnh nằm trên chính máy chủ của mình. Ảnh tự lưu thì không phải nới luật đó, và trình duyệt của người xem không phải gọi tới trang nguồn của ảnh. Không hiện ghi công là lựa chọn của chủ dự án (14/11, nhắc lại 19/11); tác giả, giấy phép vẫn giữ trong bảng ảnh. Cái giá: một số giấy phép mở đòi ghi công; trước khi công khai nên xem lại (lập luận của người viết, chưa có ghi chép).

**Vì sao ô nền bản đồ lấy từ máy chủ ở Đức?** Ngày 16/11 máy chủ chính của bản đồ mở lỗi bắt tay ở mạng đã thử; máy chủ thay do chủ dự án chọn. Trang Giới thiệu nói rõ máy chủ đó nhận địa chỉ mạng của người xem.

**Vì sao nút "Thêm vào lịch" chỉ có khi đã chọn ngày đi?** Tệp lịch điện thoại cần ngày thật cho từng sự kiện; chú thích chương trình ghi "không đoán ngày", nên chưa có ngày đi thì nút chỉ nhắc chọn ngày.

**Vì sao nút in chỉ ở trang Lên kế hoạch?** Ngày 20/11, in từ khung trò chuyện ra 5 trang giống nhau không có ngày nào, in từ trang Trợ lý mất ngày 2: khung trò chuyện là hộp có cuộn nên bản in bị cắt. Nút in ở hai chỗ đó được ẩn.

## Giới hạn đã biết

- File PowerPoint không có mục "Nơi ở" (thẻ lịch và bản in có); không có trang chi phí, không có bản đồ nền.
- Nút PowerPoint ở thẻ lịch cũ tải lịch mới nhất; người dùng chỉ được báo sau khi tải.
- Chưa giới hạn số lượt tải PowerPoint; khi đưa lên mạng phải chép cả thư mục ảnh, không thì file mất ảnh.
- Tệp lịch điện thoại: khung giờ qua nửa đêm sẽ mất sự kiện (bảng hiện chưa có điểm như vậy).
- Quán và khách sạn từ nguồn mở chưa kiểm giờ mở cửa, giá; có thể đã đổi.
- Bản đồ không có dòng ghi nguồn của bản đồ mở; phải xem lại trước khi công khai.

## Chi tiết để tra

- Phần vẽ bản đồ là một thư viện chạy trong trình duyệt, chỉ tải khi có lịch. Ô nền tải từ một máy chủ của cộng đồng bản đồ mở ở Đức. Bản đồ không hiện dòng ghi nguồn của bản đồ mở: chủ dự án chọn ngày 21/11, sau khi được báo điều khoản đòi dòng đó; phải xem lại trước khi công khai.
- Ba khu: trung tâm hai bờ sông Hương · phía tây yên tĩnh (Kim Long, Thủy Xuân) · ven biển, đầm phá (chia phía bắc và phía nam). Trang Chỗ ở chia thành 4 nhóm.
- Lý do chọn khu do chương trình viết, ví dụ "Cùng khu với {n} / {m} điểm tham quan ban ngày của lịch." hoặc "Khu trung tâm — đi cùng trẻ em hoặc người lớn tuổi nên ở gần dịch vụ, đường đi ngắn."
- Quán ngoài kho có ảnh: 5; quán có bài kho dùng ảnh của mục Khám phá; ảnh không chắc đúng quán thì không hiện.
- Lịch ví dụ "Ví dụ" của trang chỉ dùng quán có bài trong kho.
- File .txt của lịch bản hiện nay không có mục "Bản đồ từng điểm".
- Tệp lịch điện thoại ghi giờ theo giờ quốc tế (đổi từ giờ Việt Nam).
- PowerPoint: không in tác giả, giấy phép ảnh; điểm không có ảnh thì là một ô hoạ tiết mang tên điểm; trang cuối có link bản đồ từng điểm; câu an toàn bão lũ của lượt (nếu có) nằm trong file.

**Bài sau (bài 31):** sửa lịch bằng lời: model chỉ đọc ý thành một lệnh có khuôn, chương trình áp lệnh và kiểm.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Chỗ ở: `backend/llm/luu_tru_lich.py` (docstring "Không giá, không còn phòng", `KHU_*`, `NGUONG_TAY` 0,5, `NGUONG_BIEN` 0,6, `SO_THEO_MUC`, `MUC_NGAN_SACH`, `CUM_DI_TRONG_NGAY`, `PHIA_CUM`, `LINK_TIM`, `NHAN`, `chon_khu`, `_chon` + chú thích "0 / 6.108", `o_dau` + chú thích "người xem 14/11"), `backend/llm/lich_trinh_v2.py` (`o_dau_khung`), `backend/llm/len_ke_hoach.py` (`gan_o_an` — khối chỉ khi có mức hạng, `CAU_O_MOT_NGAY`), `frontend/src/LichV2.jsx` (dòng "Cần chỗ ở?…") [code]. Đếm bảng `data/anh_user_2026-11-15_ghep/bang_luu_tru_lich_v6.json`: 136 cơ sở, 67 có ảnh, theo khu 121 trung tâm / 5 phía tây / 10 ven biển (= 5 bắc + 5 nam) [riêng tư; đếm bởi agent con đọc-chỉ, khớp chú thích `settings.yaml`].
- 8 / 10, 9 / 10 rồi 10 / 10, bảng chấm thiếu cột buổi tối, mô phỏng 3.036 / 36 / 0: `report_agent/2026-11-12_ra_khoang_cach/b_luu_tru_lich_implementation.md` (dòng 30, 52–63), `e_review_o_toi.md`; `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng 40–41 và dòng 102; file chấm `data/luu_tru_lich_2026-11-14/xem_10_v3.md`, `xem_10_v4.md` [riêng tư]. Model của người chấm: không ghi trong file [chép qua agent con].
- Giá phòng (sửa theo biên bản kiểm: luật của nhóm, không phải chủ dự án chốt): `session_prompt/HIEN_TRANG.md` dòng 55 ("Chưa hỏi, không tự mở: giá phòng"), dòng 88; `docs/superpowers/plans/2026-11-14-luu-tru-trong-lich-plan.md` dòng 3 ("User chọn theo đa số… không giá"), `2026-11-12-luu-tru-khu-va-link-plan.md` dòng 16–17, 72 ("Quyết định giữ từ 05/11… Không nói giá phòng… Giá do trang đích hiện"), `2026-11-14-khach-san-du-lieu-anh-plan.md` dòng 3 ("17:50 14/11/2026… vẫn không nói giá phòng"), `session_prompt/HIEN_TRANG.md` (dòng về giá phòng); `frontend/src/LenKeHoach.jsx` (chú thích "hạng ≠ giá") [chép; code].
- Quán: `backend/llm/quan_lich.py` (docstring, `SO_QUAN`, `KM_TOI_DA` + chú thích "p95 9,3 km", `_chon` + chú thích "A 14/11", `an_uong` + chú thích bữa trưa 16/11, `GHI_CHU_AN`, lọc ký tự lạ "review B m-1", câu cuối khối) [code]; `settings.yaml` (`lich_trinh_bang_quan`: 467 = 41 + 4 + 422, bỏ một quán đóng cửa 21/11) [chép]. 86,4 % ⇒ 94,5 %, 75,2 %, 22.752 bữa, 52 ⇒ 0 / 1.890: `bai_hoc/23_LEN_KE_HOACH_BAN_2.md` mục "Khi nào hỏng" [chép]; 101 / 960: `guides/RUNBOOK_BAN_GIAO.md` mục 10.2 [chép]. Lượt lịch không giữ làm câu trả lời liền trước: `backend/api/conversations.py` (`dap_duoc_nho`, chú thích "chữ lịch có tên quán lấy từ bản đồ mở, model không được thấy") [code]. Quán ví dụ: vết `data/hoc_cung_D/vi_du_lap_lich_vet.json` [riêng tư].
- Ảnh: `lich_trinh_v2.py` (`nap_bang_anh` + chú thích "14/11: User nới luật ảnh, giao diện không hiện ghi công", `ANH_SRC`), `settings.yaml` (`lich_trinh_bang_anh`: 40 / 41 = 26 + 13 + 1; bản 6, 7), `frontend/src/LichV2.jsx` (chú thích "User 14/11"), `backend/api/lich_pptx.py` (chú thích "chủ dự án 14/11/2026… nhắc lại 19/11") [code; chép]. 10 / 10 người xem mù: `bai_hoc/23_LEN_KE_HOACH_BAN_2.md` mục "Phần phụ" [chép].
- Bản đồ: `frontend/src/BanDoLich.jsx` (chú thích đầu file: không đường nối, tải riêng, không dòng ghi nguồn — chủ dự án 21/11; vẽ lệch 16 px; lời "Các điểm ngày này chưa có vị trí trên bản đồ."), `backend/api/routes/cong.py` (ô nền OSM Đức, lý do "bắt tay TLS lỗi… Host cuối do User chọn"), `settings.yaml` (`ban_do_lich`, `lich_trinh_toa_do`) [code]. Ba lỗi ảnh chụp, nền xám: `bai_hoc/23_LEN_KE_HOACH_BAN_2.md` mục "Tối 16/11" và "Khi nào hỏng" [chép].
- Năm nút: `frontend/src/LichV2.jsx` (dòng 209–216 các nút, 287–311 .ics, 315–352 PowerPoint, 364–397 sao chép / tải; các lời báo), `frontend/src/lich_ics.js` (docstring "Không gửi gì đi đâu") [code]; `backend/api/routes/xuat.py` (docstring "Server KHÔNG nhận dữ liệu lịch nào từ trình duyệt", `CAU_HET_HAN`, `lich_tu_luu`), `backend/api/lich_pptx.py` (vẽ bằng toạ độ, không file khuôn; ô hoạ tiết) [code]. Lý do PowerPoint ở máy chủ, bảng so với thư viện trình duyệt, "User đã chọn… PowerPoint = python-pptx": `data/xuat_lich_dep_2026-11-19/PLAN.md` dòng 4, 21–28 [riêng tư; chép]. Nút in chỉ ở trang Lên kế hoạch, 5 trang giống nhau: `guides/RUNBOOK_BAN_GIAO.md` mục 10.2; `bai_hoc/VIEC_MOI_XONG.md` (dòng 804) [chép]. 44 / 33 / 288: `bai_hoc/23_LEN_KE_HOACH_BAN_2.md` mục "Phần phụ" [chép].
- Giới hạn PowerPoint (không "Nơi ở", nút ở thẻ cũ, chưa giới hạn lượt tải, cần thư mục ảnh): `guides/RUNBOOK_BAN_GIAO.md` mục 10.2; `bai_hoc/VIEC_MOI_XONG.md` dòng 811–812 [chép].
- Quyết định nhỏ "ảnh không ghi công, giấy phép mở đòi ghi công": phần "nên xem lại trước khi công khai" là lập luận của người viết, đã ghi nhãn trong bài.

- Bài đã qua một lượt đối chiếu độc lập (người kiểm chỉ đọc, tự chạy lại bộ xếp và phần áp lệnh), trưa 22/11/2026: `data/hoc_cung_D/kiem/bai_27_32.md` [riêng tư]; các dòng SAI / LỆCH đã áp, dòng không áp ghi ở `data/hoc_cung_D/viet/viet_27_32.md` mục "Sau lượt kiểm" [riêng tư].

</details>
