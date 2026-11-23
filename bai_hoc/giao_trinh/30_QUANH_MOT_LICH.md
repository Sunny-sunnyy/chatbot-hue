# Bài 30 — Quanh một lịch: chỗ ở, quán ăn, ảnh, bản đồ, xuất file

*Cập nhật 17:03, ngày 23/11/2026 · khớp hệ thống 16:21 23/11 (51 tính năng mở, 7 tắt, kho 267 bài); chưa gồm các bản gộp từ 16:38 (chờ phiếu; cỡ chữ bản in gắn mốc "tới 16:58") · "Giới hạn đã biết": quán trưa sau lệnh "thêm" (bài 31), đã áp biên bản kiểm · lần sửa trước: Nguồn.*

**Bài trước đã biết:** chương trình xếp lịch, kiểm khung, model viết mỗi mục một mô tả (bài 27–29).
**Bài này thêm:** những thứ đi kèm một lịch: khối "Nơi ở", quán cho bữa trưa và bữa tối, ảnh từng điểm, bản đồ có ghim, và năm nút xuất (sao chép, tải chữ, thêm vào lịch điện thoại, in, PowerPoint). Mọi thứ trong bài đều do chương trình chọn; model không thấy tên quán, tên khách sạn hay toạ độ nào.

## Ý chính

- **Chỗ ở** chỉ hiện khi người dùng đã chọn hạng sao: một khu cho cả chuyến, rồi tối đa 5 trong 136 cơ sở. Luật chọn khu nhìn **buổi tối trước**: tối nào cũng ở trung tâm thì ở trung tâm. Không có giá phòng.
- **Quán ăn**: mỗi bữa nhiều nhất 2 quán, cùng cụm, cách điểm không quá 2 km, quán có bài trong kho trước; từ 23/11, 6 quán mà bài kho ghi rõ giờ không phủ bữa trưa hay bữa tối không còn được gợi ý vào bữa đó (quán khác như cũ). Phần lớn 467 quán của bảng lấy từ bản đồ mở, mang nhãn "chưa kiểm".
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

Lịch ví dụ 3 ngày của bài 27–28 không chọn hạng sao, nên dưới lịch chỉ có một dòng: "Cần chỗ ở? Xem gợi ý theo khu, hoặc nhắn trợ lý hạng sao bạn muốn (ví dụ “ở khách sạn 3 sao”)." Bấm vào là sang trang Chỗ ở. Khối "Nơi ở" chỉ hiện khi người dùng đã chọn hạng ở biểu mẫu, hoặc đã nói hạng bằng lời (bài 31). Lịch "Ví dụ" dựng sẵn của trang thì có chọn hạng, nên có khối "Nơi ở".

**Chọn khu.** Chương trình xét ba khu theo thứ tự:

1. Lịch có hoạt động buổi tối và mọi buổi tối đều ở trung tâm ⇒ ở trung tâm, lý do "Khu trung tâm — các buổi tối của lịch đều ở trung tâm, về chỗ ở gần."
2. Không thì đếm cụm của các điểm ban ngày (bỏ các điểm đi trong ngày ở phía nam xa). Từ 60 % điểm ở ven biển ⇒ ven biển. Hơn 50 % ở phía tây ⇒ phía tây, trừ khi có trẻ em hay người lớn tuổi thì về trung tâm.
3. Còn lại ⇒ trung tâm.

Bộ xếp chỉ đặt buổi tối ở hai cụm trung tâm (bài 28), nên bậc 1 gần như luôn quyết (mô phỏng 3.840 tổ hợp: bảng "Đã so").

**Chọn cơ sở.** Trong khu đã chọn, chương trình lấy tối đa 5 cơ sở của đúng hạng người dùng chọn (hạng đó trống thì trải đều các hạng), gần cụm có nhiều điểm nhất trước, có ảnh trước. Mỗi cơ sở có tên, hạng, địa chỉ, link tìm phòng trên một trang đặt phòng công khai (chỉ mở khi bấm), link bản đồ, và nhãn chung "Gợi ý theo vị trí và hạng — chưa kiểm giá, phòng trống." Bảng lưu trú có 136 cơ sở từ danh mục công khai có nguồn và ngày (chia theo khu: "Chi tiết để tra").

## Quán ăn: hai quán mỗi bữa, cùng cụm, trong 2 km

Với mỗi ngày, chương trình tìm quán cho hai bữa:

- **Bữa trưa** gần điểm cuối buổi sáng. Không có quán trong 2 km thì xét các điểm sáng còn lại, rồi điểm đầu buổi chiều.
- **Bữa tối** gần hoạt động buổi tối; ngày không có hoạt động tối thì gần điểm cuối buổi chiều.

Một quán được chọn khi cùng cụm với điểm và cách điểm không quá 2 km đường chim bay. Bữa chính chỉ gợi ý quán ăn; chỉ khi trong 2 km không có quán ăn nào mới gợi ý quán cà phê. Trong cùng loại: quán có bài trong kho trước, rồi dữ liệu mở của thành phố, rồi bản đồ mở; sau đó gần nhất trước. Không lặp quán trong cả chuyến.

**Bữa không hợp giờ quán (từ 23/11).** Bảng quán đánh dấu sẵn bữa nào không hợp cho 6 quán mà bài kho ghi giờ không phủ bữa trưa hay bữa tối; bộ chọn bỏ quán khỏi bữa đó. Trước đó, lịch 2 ngày mặc định và lịch ví dụ dựng sẵn (nhãn "Ví dụ") gợi ý Bún bò Bà Nga (kho ghi 18h – 23h) cho bữa trưa gần Đại Nội; nay ở lịch mặc định quán này sang bữa tối gần chợ Đông Ba. Quán không ghi giờ thì vẫn như cũ ("Giới hạn đã biết").

Quán có bài trong kho có link "Đọc bài". Cuối khối có câu "Gợi ý theo vị trí — chưa kiểm giờ mở cửa, giá; quán có thể đã đổi." Sáu nơi xa có một câu ghi chú cố định thay cho tên quán khi không chọn được quán.

## Ảnh và bản đồ: lấy từ bảng, không đoán

**Ảnh.** Mỗi điểm nhiều nhất một ảnh, gắn theo mã điểm. 40 trên 41 điểm có ảnh, phần lớn từ Wikimedia Commons (giấy phép mở); nguồn từng ảnh và phép kiểm lúc bật ở "Chi tiết để tra". Mọi ảnh nằm trên máy của dự án. Trang không hiện dòng ghi công (chủ dự án yêu cầu 14/11, nhắc lại 19/11).

**Bản đồ.** Trên trang Lên kế hoạch ở màn từ 1.200 px, khung bản đồ đứng cạnh lịch và đi theo khi cuộn; màn hẹp hơn, và trong khung trò chuyện, nó nằm dưới lịch. Mỗi lần khung hiện một ngày; nút "Ngày 1 / Ngày 2…" đổi ngày. Ghim có số theo thứ tự đi trong ngày, khớp danh sách đánh số dưới bản đồ. Bấm ghim thì hiện tên điểm và link mở Google Maps. Toạ độ do chương trình lấy từ bảng toạ độ; model không tạo toạ độ, và toạ độ không vào tin gửi model. Điểm không có toạ độ thì không có ghim. Bản đồ không vẽ đường nối giữa các ghim, vì hệ thống không có đường đi thật.

## Năm nút xuất: bốn ở trình duyệt, một ở máy chủ

| Nút | Dựng ở đâu | Từ đâu | Điều cần biết |
|---|---|---|---|
| Sao chép lịch | trình duyệt | bản chữ của lịch máy chủ gửi kèm (như thẻ; từ 23/11 bỏ đuôi "— sai thì bấm Sửa.", đuôi này chỉ còn trên màn hình; file .txt mới tải thử một lần, trên nhánh thử, 13:11 23/11; sao chép chưa ai thử lại) | báo "Đã sao chép lịch."; trình duyệt chặn thì "Trình duyệt không cho sao chép — dùng nút Tải về." |
| Tải về (.txt) | trình duyệt | như trên | file chữ thường, bỏ dấu in đậm |
| Thêm vào lịch (.ics) | trình duyệt | khung lịch đang hiện | chỉ khi đã chọn ngày đi ("Chọn ngày đi ở biểu mẫu để thêm lịch vào lịch điện thoại."); mục không có giờ thì bỏ; câu an toàn bão lũ (nếu có) đứng đầu phần mô tả |
| In / Lưu PDF | khung in của trình duyệt | bố cục in riêng của thẻ lịch | chỉ có ở trang Lên kế hoạch |
| Tải PowerPoint | máy chủ | lịch đã lưu của cuộc trò chuyện | báo "Đang tạo file…", rồi "Đã tải lich-trinh-hue.pptx (lịch mới nhất của cuộc trò chuyện)." |

**Bản in** có luật bố cục riêng, giữ tỉ lệ và chỗ ngắt trang cũ (mục "Quyết định nhỏ hơn"); từ 23/11 đường nối các điểm in thành vạch thẳng, không còn nét cong đè lên khối quán ("Đã so").

Bấm "Tải PowerPoint", trình duyệt chỉ báo "tôi muốn tải lịch của cuộc trò chuyện này"; không gửi nội dung lịch. Máy chủ dựng lại lịch từ khung và câu mô tả đã lưu bằng đúng các hàm dựng thẻ (không xếp lại, không gọi model), rồi vẽ file. Không có lịch đã lưu thì người dùng nhận "Chưa có lịch để tải hoặc lịch đã hết hạn — bấm Lên kế hoạch để tạo lại rồi tải."

## Quyết định và lý do

### 1. Vì sao chỗ ở, quán, ảnh, toạ độ đều do chương trình chọn, và model không thấy chúng?

- **Đã chọn:** chương trình chọn khu, cơ sở, quán, ảnh, toạ độ từ các bảng. Những khối này không vào tin gửi model; lượt lập lịch và lượt sửa lịch cũng không được giữ làm "câu trả lời liền trước" cho lượt sau.
- **Vì sao:** luật thiết kế của trang: model không chọn ảnh, không bịa quán, không nói giá phòng. Tên quán từ bản đồ mở là chữ người ngoài viết: chương trình ghi rõ model không được thấy, và lọc ký tự lạ, đường link trong tên trước khi hiện.
- **Cách khác:** để model gợi ý quán, khách sạn từ kho: không làm.
- **Cái giá:** gợi ý chỉ tốt bằng bảng. Hỏi "trưa ăn gì gần X" thì công cụ "gần một điểm" (bài 24) đọc cùng bảng nhưng không bỏ quán theo bữa, chỉ đưa giờ kho cho model đọc; hai bên có thể gợi ý khác nhau.

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
- **Vì sao:** bốn nút đầu chỉ đổi cách hiện thứ trình duyệt đã có (bài 5), không cần gửi gì đi (điều thấy được; chưa thấy ghi lý do riêng). Chủ dự án chọn thư viện Python cho PowerPoint ngày 19/11, sau một lần tra cứu công khai, không có số đo. Kế hoạch viết sau đó có bảng so với thư viện chạy trong trình duyệt; lợi được nêu: test bằng Python sẵn có; máy chủ dựng lại từ bản đã lưu nên mọi chữ trong file là chữ của bảng hoặc câu đã kiểm.
- **Cách khác:** dựng PowerPoint trong trình duyệt: nêu trong bảng so, không chọn. Bên đó tải được cả khi lịch hết hạn, và máy chủ không tốn gì.
- **Cái giá:** chỉ tải được trong 30 phút từ lượt cuối; nút ở thẻ lịch cũ vẫn tải lịch mới nhất của cuộc; mỗi lần bấm máy chủ dựng file; số lượt tải chỉ bị giới hạn (30 mỗi địa chỉ mỗi ngày) khi bộ giới hạn lượt được bật, mặc định tắt (bài 37).

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
- **"Bản đồ vẽ đường đi giữa các điểm."** Không. Chỉ có ghim theo thứ tự; hệ thống không có đường đi thật. Nét sông nối các điểm trong thẻ lịch (bài 27) chỉ là hình theo thứ tự đi, không phải đường đi.

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

*Theo cấu hình và chương trình trưa 22/11/2026; hàng `ban_do_lich` theo nhánh chính sáng 23/11/2026; hàng `lich_trinh_bang_quan` theo nhánh chính trưa 23/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| `luu_tru_lich` | đang mở (từ 14/11) | khối "Nơi ở"; chỉ chương trình, không thêm lần gọi model | — |
| `lich_trinh_bang_luu_tru` | bảng bản 6: 136 cơ sở, 67 có ảnh | danh mục công khai có nguồn và ngày | bản 3: 137 cơ sở; các bản rà ảnh 15/11 |
| ngưỡng khu ven biển / phía tây | ≥ 60 % / > 50 % điểm ban ngày | ngày ra biển thường là đi trong ngày | bậc "buổi tối ở trung tâm" đứng trước |
| số cơ sở | ≤ 5; trải 2 (4–5 sao) · 2 (2–3 sao) · 1 (1 sao) | để khách tự chọn hạng | trước: xếp theo tên trong cả mức làm 5 sao không bao giờ hiện (0 / 6.108); đã sửa |
| `quan_lich` | đang mở (từ 14/11) | quán mỗi bữa; chỉ chương trình | — |
| `lich_trinh_bang_quan` | bản 4 (23/11): 467 quán | kho 41 + dữ liệu mở 4 + bản đồ mở 422; 6 quán có bài trong kho được ghi sẵn bữa nào quán không bán (ghi từ bản 3 của bảng); 30 quán kho mang dòng giờ chép từ kho, chỉ công cụ "gần một điểm" đọc (bài 24) | bản 1 có thêm một quán đã đóng cửa; bản 2 chưa có dấu bữa (766 / 960 tổ hợp có quán lệch bữa) |
| số quán / khoảng cách | ≤ 2 quán; ≤ 2 km chim bay, cùng cụm | mục "Quyết định nhỏ hơn" | không giới hạn: bỏ |
| `anh_lich` | đang mở (từ 14/11) | ảnh từng điểm | — |
| `lich_trinh_bang_anh` | bản 7: 40 / 41 điểm | 26 Commons + 13 web + 1 ảnh chủ dự án | bản 6 đổi ảnh đèo Hải Vân; bản 7 đổi ảnh lăng Thiệu Trị |
| `ban_do_lich` | đang mở (từ tối 16/11) | bản đồ dưới lịch, hoặc cạnh lịch ở trang Lên kế hoạch từ 1.200 px (giao diện 23/11); chủ dự án chọn bật | — |
| `lich_trinh_toa_do` | bảng toạ độ 41 dòng, 40 có vị trí | ghim | bản cũ 18 điểm |
| ô nền bản đồ | máy chủ cộng đồng bản đồ mở ở Đức | máy chủ chính lỗi bắt tay ở mạng đã thử (16/11); chủ dự án chọn | — |
| dòng ghi nguồn bản đồ | tắt | chủ dự án chọn 21/11; phải xem lại trước khi công khai | — |
| `xuat_pptx` | đang mở (từ 21:30 19/11) | nút in và nút PowerPoint; chủ dự án chọn bật | — |
| giới hạn số lượt tải PowerPoint | 30 mỗi địa chỉ mỗi ngày, chỉ khi bộ giới hạn lượt bật (mặc định tắt) | một lịch thường tải một hai lần; chặn vòng lặp tải (bài 37) | — |

## Đã so

**Khu ở theo buổi tối (14/11, chỉ chương trình, 0 USD; người chấm là các phiên làm việc, mỗi lượt một người mới):**

| Luật | Người chấm, cùng 10 lịch (sàn 9 / 10) | Mô phỏng 3.840 khung | Kết luận |
|---|---|---|---|
| đếm cụm điểm ban ngày (bản đầu) | 9 / 10, rồi 10 / 10 — bảng chấm thiếu cột buổi tối | có khung gợi ý phía tây dù tối ở trung tâm | thay |
| đếm điểm tối như điểm ngày | 8 / 10 | — | bỏ |
| buổi tối ở trung tâm ⇒ ở trung tâm | 10 / 10 | trung tâm 3.036 · ven biển 36 · phía tây 0 | giữ |

**Quán ăn (mô phỏng mọi tổ hợp, 0 USD):** bữa có dòng gợi ý 86,4 % ⇒ 94,5 % (22.752 bữa) sau khi thêm ghi chú cho nơi xa; bữa có tên quán 75,2 %. Ngày không có bữa trưa 52 ⇒ 0 trên 1.890 ngày mô phỏng sau khi bữa trưa được xét thêm các điểm sáng khác và điểm đầu buổi chiều (17/11); 101 / 960 khung đổi quán bữa tối vì luật không lặp quán.

**Quán lệch bữa (23/11, chỉ chương trình, 0 USD).** Vấn đề thật: lượt dùng như người thật trên trình duyệt sáng 23/11 thấy lịch ví dụ dựng sẵn của trang gợi ý Bún bò Bà Nga cho bữa trưa, trong khi kho ghi quán mở buổi tối. Người viết code đếm và sửa; một phiên khác (không viết code của bản này) chấm.

| Phép | Bảng bản 2 (trước) | Bảng có dấu bữa (sau) |
|---|---|---|
| tổ hợp biểu mẫu (960, không ngày đi) có ít nhất một quán ở bữa kho ghi đóng | 766 / 960 (riêng Bà Nga ở bữa trưa: 756) | 0 / 960 |
| phép đếm độc lập của phiên chấm: khung lịch (960 tổ hợp × 4 kiểu ngày đi = 3.840) có quán ở bữa kho ghi đóng | 3.066 / 3.840 | 0 / 3.840; số bữa có quán không đổi (17.660) |
| trình duyệt (do công cụ tự lái): lịch mặc định 3 lần, lịch ví dụ dựng sẵn (nút "Xếp lịch như ví dụ"), 3 tổ hợp khác, một lượt sửa bằng lời | Bà Nga ở bữa trưa | 0 quán lệch bữa |

**Đọc bảng thế nào:** hai hàng đầu là hai phép đếm khác mẫu số, mỗi hàng so trước ⇒ sau trên cùng một phép. Người viết bài chạy lại hàng đầu trên bảng bản 2 và bảng đang chạy (bản 4): 766 ⇒ 0. **Giới hạn:** phép chỉ tính 6 quán kho có giờ rõ; quán không ghi giờ không đếm được.

**Bản in, vạch thẳng (23/11).** Nét cong của đường nối các điểm được đo trên bố cục màn hình; bản in có bố cục khác nên nét lệch dần rồi đè hai khối quán cuối ngày (trang 2 của lịch mặc định, có cả ở bản in cũ 22/11). Bản in nay dùng vạch thẳng: phiên chấm mở trang 2 thấy vạch mảnh sau các ảnh, dừng ở điểm cuối; PDF vẫn 2 trang.

**Ảnh (14/11):** một người xem mù kiểm 10 lịch, ảnh đúng điểm 10 / 10, một ảnh lăng ghi "đúng loại, không chắc đúng lăng".

**Tệp lịch điện thoại:** kiểm trên 44 lịch đã lưu, 33 lịch có ngày đi cho ra 288 sự kiện; một trình đọc độc lập báo 0 lỗi. Chưa thử mở trên Google Calendar.

**Bản đồ (16/11):** ba lịch thật 1, 2, 3 ngày, số ghim bằng số điểm có toạ độ, số trên ghim đúng thứ tự; ảnh chụp màn hình lộ thêm ba lỗi phép đếm không bắt (số lệch góc ghim, ghim thấp bị dòng ghi công che, hai ghim gần nhau che nhau), đều đã sửa.

**Giới hạn của phép đo:** các phép trên đếm khung lịch và bảng, không đo người dùng thật có thấy gợi ý hữu ích không.

## Quyết định nhỏ hơn

**Vì sao "gần" là 2 km, và bữa chính chỉ gợi ý quán ăn?** **Đã chọn:** cùng cụm và không quá 2 km đường chim bay; quán ăn trước, cà phê chỉ khi không có quán ăn nào. **Vì sao:** lần mô phỏng đầu không giới hạn khoảng cách: quán "gần" ở mức 95 % là 9,3 km, vì có cụm rất rộng (phá, biển, lăng xa), nên dòng "ăn gần X" sai nghĩa. Luật quán ăn trước có sau khi phiên điều phối thấy bữa tối gợi ý một quán cà phê có bài kho đứng trước quán ăn (14/11). **Cách khác:** không giới hạn khoảng cách: đã đo, bỏ. **Cái giá:** nơi xa ít quán thì bữa không có tên quán: trên mọi tổ hợp, chỉ 75,2 % bữa có tên quán (bảng ở nửa để tra).

**Vì sao ảnh nằm trên máy của dự án, và không hiện ghi công?** Trang web của dự án có một luật an toàn: chỉ hiện ảnh nằm trên chính máy chủ của mình. Ảnh tự lưu thì không phải nới luật đó, và trình duyệt của người xem không phải gọi tới trang nguồn của ảnh. Không hiện ghi công là lựa chọn của chủ dự án (14/11, nhắc lại 19/11); tác giả, giấy phép vẫn giữ trong bảng ảnh. Cái giá: một số giấy phép mở đòi ghi công; trước khi công khai nên xem lại (lập luận của người viết, chưa có ghi chép).

**Vì sao ô nền bản đồ lấy từ máy chủ ở Đức?** Ngày 16/11 máy chủ chính của bản đồ mở lỗi bắt tay ở mạng đã thử; máy chủ thay do chủ dự án chọn. Trang Giới thiệu nói rõ máy chủ đó nhận địa chỉ mạng của người xem.

**Vì sao nút "Thêm vào lịch" chỉ có khi đã chọn ngày đi?** Tệp lịch điện thoại cần ngày thật cho từng sự kiện; chú thích chương trình ghi "không đoán ngày", nên chưa có ngày đi thì nút chỉ nhắc chọn ngày.

**Vì sao tỉ lệ bản in được ghim bằng luật (22/11)?** Chú thích trong chương trình: trước đó tỉ lệ có do tình cờ. Khi in, thanh menu bị giấu đi nhưng vẫn giữ chỗ, dài 1.019 px, rộng hơn phần in được của trang A4 (688 px); trình duyệt thấy trang không vừa giấy nên tự thu nhỏ cả trang còn 688 / 1.019 = 67,5 %. Cỡ chữ in và chỗ ngắt trang trước nay có được là nhờ lần thu nhỏ tình cờ đó. Giao diện mới làm thanh menu ngắn lại (832 px) thì chữ in to lên 22 %, lịch ví dụ từ 2 trang thành 3; lỗi này lộ ra khi in thử ra PDF trước khi gộp. **Đã chọn:** khi in, thanh menu ra khỏi bố cục, bề rộng 1.019 px đặt thẳng cho cả trang; cỡ chữ của bản in (tới 16:58 23/11) giữ các giá trị trước khi gom cỡ chữ về một thang (thang mới đổi 15,5 ⇒ 15, 18 ⇒ 19, 24 ⇒ 22 px…). **Kết quả ghi trong chương trình:** lịch ví dụ in 2 trang, 76 / 76 dòng nằm đúng chỗ bản in cũ (so hai file PDF); không giữ cỡ chữ cũ thì vẫn 2 trang nhưng dòng chữ xê dịch tới 2 pt. **Cách khác:** để tỉ lệ theo thanh menu như trước: bỏ, vì mỗi lần đổi thanh trên bản in lại đổi cỡ. Đặt một tỉ lệ thu nhỏ khác: chưa thử. **Cái giá:** muốn chữ in to hơn phải giảm con số 1.019 và soát lại chỗ ngắt trang; đổi thanh trên, cỡ chữ hay bề rộng thì phải in thử ra PDF, so số trang.

**Vì sao lệch bữa được chữa bằng dấu "bữa không hợp" trong bảng quán, mà không cho chương trình đọc giờ lúc xếp?** **Đã chọn:** một lần dựng bảng, ghi sẵn bữa nào không hợp cho từng quán có giờ rõ trong bài kho; bộ chọn chỉ đọc dấu đó. Quán không ghi giờ thì không đoán. **Vì sao:** sổ bàn giao ghi "không bịa giờ cho quán kho không ghi". Vì sao chọn dấu dựng sẵn thay vì đọc giờ lúc xếp: chưa thấy ghi lý do. Điều thấy được: phiên chấm tự đọc lại dòng giờ của 41 quán kho và ra đúng 6 quán đã đánh dấu. **Cách khác:** đọc giờ mở cửa lúc xếp: chưa thử. **Cái giá:** thêm một quán phải dựng một bản bảng mới; quán không ghi giờ vẫn có thể ra ở bữa quán không bán.

**Vì sao nút in chỉ ở trang Lên kế hoạch?** Ngày 20/11, in từ khung trò chuyện ra 5 trang giống nhau không có ngày nào, in từ trang Trợ lý mất ngày 2: khung trò chuyện là hộp có cuộn nên bản in bị cắt. Nút in ở hai chỗ đó được ẩn.

## Giới hạn đã biết

- File PowerPoint không có mục "Nơi ở" (thẻ lịch và bản in có); không có trang chi phí, không có bản đồ nền.
- Nút PowerPoint ở thẻ lịch cũ tải lịch mới nhất; người dùng chỉ được báo sau khi tải.
- Chưa giới hạn số lượt tải PowerPoint; khi đưa lên mạng phải chép cả thư mục ảnh, không thì file mất ảnh.
- Tệp lịch điện thoại: khung giờ qua nửa đêm sẽ mất sự kiện (bảng hiện chưa có điểm như vậy).
- Quán và khách sạn từ nguồn mở chưa kiểm giờ mở cửa, giá; có thể đã đổi.
- Dấu "bữa không hợp" chỉ có ở 6 quán kho có giờ rõ. 11 quán kho không ghi giờ và 426 quán ngoài kho vẫn có thể được gợi ý vào bữa quán không bán; Cơm Tấm Okla (kho chỉ ghi phục vụ buổi trưa) vẫn có thể ra ở bữa tối. Ba quán sát mép giờ (một quán bánh canh ở bữa tối, một quán hủ tiếu ở bữa trưa, Huyền Anh ở bữa tối) phiên chấm không tính là lỗi.
- Bản đồ không có dòng ghi nguồn của bản đồ mở; phải xem lại trước khi công khai.
- Chưa có cặp bản in "cùng một lịch, từng chữ" cũ ↔ mới: hai bản đem so cùng khung lịch nhưng câu mô tả khác.
- Từ 15:38 23/11 lệnh "thêm" có thể làm một ngày dày hơn nhịp đã chọn (bài 31). Quán trưa đi theo điểm cuối buổi sáng mới (điểm đó không có quán trong 2 km thì theo điểm sáng khác), nên trên 319 lịch đã thêm của phép đếm (bảng điểm trước 16:38 23/11), 265 đổi quán trưa và 41 mất hết quán có bài kho (chỉ còn quán "từ bản đồ mở, chưa kiểm" hoặc không còn quán) — số của sổ việc, không có file kết quả. Dòng "Ngày N dày hơn nhịp…" có trong file tải về; bản in của lịch có ngày dày chưa ai nhìn.
- In bằng tay (bấm "In / Lưu PDF" trên trình duyệt thật, ra giấy hoặc PDF) chưa ai thử với giao diện mới; các bản in kể trên do trình duyệt tự động in ra PDF.

## Chi tiết để tra

- Ở lịch ví dụ 3 ngày của bài 27–28 (không phải lịch "Ví dụ" dựng sẵn của trang), bữa trưa ngày 3 gần Bao Vinh chỉ có một quán, nhãn "(từ bản đồ mở, chưa kiểm)" (chuyển từ thân bài trong đợt áp biên bản 23/11; chưa chạy lại bộ xếp sau bảng quán bản 4, bảng này chỉ đổi 6 quán kho).
- Lịch 1 ngày không có đêm nào nên không có khối "Nơi ở"; người đã chọn hạng thì đọc thấy "Lịch đi trong ngày (không có đêm nào) nên mình chưa gợi ý chỗ ở." (chuyển từ thân bài ở lượt áp cuối 23/11).
- Chuyển từ thân bài 23/11 (số đếm và chi tiết, không đổi nội dung): bảng lưu trú 136 cơ sở chia theo khu: 121 ở trung tâm, 5 phía tây, 10 ven biển; 67 cơ sở có ảnh. Bảng quán 467 quán: 41 có bài trong kho, 4 từ dữ liệu mở của thành phố, 422 từ bản đồ mở. Mô phỏng chọn khu trên 3.840 tổ hợp: trung tâm 3.036 khung, ven biển 36, phía tây 0 (còn lại là lịch 1 ngày). Ảnh 40 / 41 điểm: 26 từ Wikimedia Commons, 13 ảnh web (phần lớn dùng lại ảnh của mục Khám phá), 1 ảnh chủ dự án tự tìm; lúc bật, máy chủ kiểm từng dòng của bảng ảnh: file có thật, ảnh Commons có tác giả và giấy phép, ảnh web có trang nguồn. Trên bản đồ, hai ghim sát nhau thì ghim sau được vẽ lệch sang một chút để khỏi che số.
- Bản in sau giao diện mới, chuyển từ thân bài 23/11: giao diện mới làm thanh menu ngắn lại thì chữ in to lên 22 %, lịch ví dụ từ 2 trang thành 3; luật riêng cho bản in ghim lại tỉ lệ cũ (mục "Quyết định nhỏ hơn").
- Phần vẽ bản đồ là một thư viện chạy trong trình duyệt, chỉ tải khi có lịch. Ô nền tải từ một máy chủ của cộng đồng bản đồ mở ở Đức. Bản đồ không hiện dòng ghi nguồn của bản đồ mở: chủ dự án chọn ngày 21/11, sau khi được báo điều khoản đòi dòng đó; phải xem lại trước khi công khai.
- Ba khu: trung tâm hai bờ sông Hương · phía tây yên tĩnh (Kim Long, Thủy Xuân) · ven biển, đầm phá (chia phía bắc và phía nam). Trang Chỗ ở chia thành 4 nhóm.
- Lý do chọn khu do chương trình viết, ví dụ "Cùng khu với {n} / {m} điểm tham quan ban ngày của lịch." hoặc "Khu trung tâm — đi cùng trẻ em hoặc người lớn tuổi nên ở gần dịch vụ, đường đi ngắn."
- Câu ghi chú của sáu nơi xa (chuyển từ thân bài 23/11): năm câu dựa trên kho, một câu chỉ nói chưa có gợi ý.
- Giao diện mới (23/11) không chạm chương trình dựng file (chuyển từ thân bài trưa 23/11): ở lượt kiểm trước khi gộp, một lịch 2 ngày tải ra file chữ 29 dòng và PowerPoint 4 slide, bằng bản cũ.
- Quán ngoài kho có ảnh: 5; quán có bài kho dùng ảnh của mục Khám phá; ảnh không chắc đúng quán thì không hiện.
- Lịch ví dụ "Ví dụ" của trang chỉ dùng quán có bài trong kho.
- Dấu "bữa không hợp" (23/11): một quán bị đánh dấu khi giờ trong bài riêng của nó không phủ khung bữa trưa 11:00 – 13:30 hay bữa tối 18:00 – 20:30. Sáu quán: Bún bò Bà Nga, Bánh mì Trường Tiền O Tho, Quán Bánh Chi (bỏ khỏi bữa trưa); Bún bò O Nhơn, Cơm hến - bún hến Lành, Quán Nhỏ (bỏ khỏi cả hai bữa). Ở lịch mặc định sau sửa, bữa trưa gần Đại Nội là Bánh Ướt - Bún Thịt Nướng Huyền Anh và Ẩm thực chay Tịnh Tâm Đinh Vũ. Kho tự lệch một chỗ: một bài tổng hợp ẩm thực gợi ý Quán Nhỏ cho bữa trưa, bài riêng của quán ghi mở 06:00 – 10:00.
- File .txt của lịch bản hiện nay không có mục "Bản đồ từng điểm".
- Tệp lịch điện thoại ghi giờ theo giờ quốc tế (đổi từ giờ Việt Nam).
- Bảng so thư viện PowerPoint (19/11) còn nêu lợi "khuôn làm tay, dễ đẹp", nhưng chương trình hiện vẽ bằng toạ độ, không dùng khuôn.
- Bản in từ 23/11, so hai file PDF thật của cùng một khung lịch 2 ngày (bản cũ chạy 20:43 22/11, bản mới 09:32 23/11; câu mô tả khác chữ vì model viết lại mỗi lượt): cùng 2 trang, cùng chỗ ngắt trang, cùng bố cục thẻ điểm, ảnh, khối quán. Khác hai chỗ: dòng nguồn in theo kiểu mới ("Nguồn đã dùng (8 bài)", mỗi bài một nút có chấm màu, một vạch sông mảnh phía trên) thay cho dòng chữ gạch chân; "Ghi chú của lịch" có lại chấm đầu dòng (một lỗi có sẵn ở bản cũ, chữa cùng đợt). Nét đứt chạy giữa dòng sông và nét sông ở dải đầu trang chỉ có trên màn hình, không in. (Phép so này có trước bản vạch thẳng trưa 23/11; từ đó đường nối các điểm in thành vạch thẳng.)
- File chữ: bỏ phần câu mô tả do model viết (sau dấu "—" của từng dòng), file .txt của lượt kiểm mới và của lượt cũ 20:43 22/11 trùng nhau từng dòng (người viết so). Từ trưa 23/11 bản sao chép và file .txt bỏ đuôi "— sai thì bấm Sửa." của dòng "Mình hiểu" (thay bằng dấu chấm). File .txt mới được tải thử một lần (13:11 23/11, lượt tự lái của một phiên khác trên nhánh thử có phần giao diện giống nhánh chính): dòng "Mình hiểu" không còn đuôi; nút sao chép chưa ai thử lại. Bản in vốn đã giấu cả dòng "Mình hiểu", PowerPoint vốn đã cắt đuôi đó. Tệp lịch điện thoại: chương trình không đổi; lượt kiểm sau gộp không tải tệp này.
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
- Giao diện mới, bản in và file xuất (thêm 23/11/2026, đọc main `20f998f4`): chương trình dựng file không đổi — `git diff --stat bedfa091 e7193bd0 -- frontend/src/lich_ics.js backend/api/routes/xuat.py backend/api/lich_pptx.py` rỗng; trong `frontend/src/LichV2.jsx` lần gộp chỉ đổi hàm vẽ `SongNgay` [code, đã chạy lệnh]. File thật: `data/giao_dien_2026-11-22/kich_ban_du_sau_gop_10c30bc5/KET_QUA.md` hàng XUAT (09:32 23/11: .txt 29 dòng, PowerPoint 4 slide, PDF 2 trang) và `…/in_dung_cach_cu/KET_QUA.md` hàng XUAT (20:43 22/11, cổng 8010, giao diện cũ — người viết mở `XUAT_lich_1440.png` của thư mục đó: thanh trên nền sẫm, ba kiểu đi ba cột: giao diện cũ; .txt 29 dòng, PowerPoint 4 slide, PDF 2 trang) [riêng tư; đã mở]. So .txt: `diff <(sed 's/ — .*//' in_dung_cach_cu/XUAT_lich.txt) <(sed 's/ — .*//' kich_ban_du_sau_gop_10c30bc5/XUAT_lich.txt)` không ra dòng nào [đã chạy]. So PDF: người viết mở trang 2 của `kich_ban_du_sau_gop_10c30bc5/XUAT_ban_in.pdf` và của `in_dung_cach_cu/XUAT_ban_in.pdf` [đã mở ảnh]. Bản đồ cạnh lịch: `frontend/src/lkh.css` khối `@media screen and (min-width: 1200px)` (`.lich-v2:has(> .bd)`, `position: sticky`) [code]; ảnh `sau_gop_10c30bc5/L02_lich_xong_1536x695_man.png` [đã mở ảnh].
- Tỉ lệ in "đúng nhờ may", 1.019 / 688 / 67,5 %, 832 px, 22 %, 2 ⇒ 3 trang, 76 / 76 dòng, 2 pt, cỡ chữ in giữ cũ: `frontend/src/lkh.css` khối `@media print` (chú thích "Tỉ lệ bản in — ghim bằng luật (22/11/2026)…" và "Cỡ chữ của BẢN IN giữ đúng các giá trị…"), lời commit `e27398dc` [code; chép]; mọi luật nhìn mới trong `@media screen`: `lkh.css` chú thích khối "Hướng Dòng sông dẫn đường", lời commit `22e4694f` [code]. Dòng nguồn in kiểu mới: luật `.nguon*` ở `frontend/src/song/song.css` không nằm trong khối chỉ cho màn hình [code; thấy trên PDF]. Chấm đầu dòng "Ghi chú của lịch": lời commit `10c30bc5`, `lkh.css` (`list-style: disc`, chú thích "bộ đặt lại của Tailwind bỏ chấm đầu dòng") [code].
- Ba giới hạn bản in (giới hạn nét cong đã chữa trưa 23/11 và đã gỡ khỏi "Giới hạn đã biết", xem dòng "Bản in vạch thẳng"; hai giới hạn còn lại giữ): `session_prompt/HIEN_TRANG.md` mục 1 gạch "Giao diện mới…" ("bản in trang 2 nét cong dòng thời gian đè hai khối quán"; "bản in 2 trang đúng kiểu in (chưa có cặp 'cùng một lịch, cũ ↔ mới')") [chép]; "in bằng tay chưa ai thử": lời giao đợt 23/11 sự việc A, khớp với `KET_QUA.md` (PDF do trình duyệt tự động in) [chép; suy từ hồ sơ]. Nét cong đè ở cả bản cũ: người viết mở trang 2 của hai PDF [đã mở ảnh].
- Quyết định nhỏ "ảnh không ghi công, giấy phép mở đòi ghi công": phần "nên xem lại trước khi công khai" là lập luận của người viết, đã ghi nhãn trong bài.

- Bài đã qua một lượt đối chiếu độc lập (người kiểm chỉ đọc, tự chạy lại bộ xếp và phần áp lệnh), trưa 22/11/2026: `data/hoc_cung_D/kiem/bai_27_32.md` [riêng tư]; các dòng SAI / LỆCH đã áp, dòng không áp ghi ở `data/hoc_cung_D/viet/viet_27_32.md` mục "Sau lượt kiểm" [riêng tư].

- Quán lệch bữa (thêm 12:17 23/11/2026): `git show 90df7bb3` — `backend/llm/quan_lich.py` (`BUA`, `nap_bang_quan` kiểm `khong_bua`, `_chon(…, bua)` bỏ quán có `bua` trong `khong_bua` + chú thích "Bún bò Bà Nga mở 18h–23h… 756 / 960 tổ hợp"); bảng đang chạy: `backend/config/settings.yaml` dòng `lich_trinh_bang_quan` = `bang_quan_lich_v4.json` (bản 4 = bản 3 + `gio_kho` cho 30 quán kho, chỉ `gan_diem_gio` đọc) [code]. Người viết đếm bảng bản 4: 467 quán, 41 kho, 30 có `gio_kho`, 6 có `khong_bua` (đúng sáu tên ở "Chi tiết để tra") [đã chạy, riêng tư]. Khung bữa 11:00–13:30 / 18:00–20:30: docstring `data/thu_bedrock_2026-11-21/harness/c_quan_lech_bua_2311/dung_bang_v3.py` [riêng tư; đã mở]. Giờ Bà Nga trong kho: `scripts/grep_kb.sh "Giờ hoạt động"` ⇒ bài `bun bo ba nga.md` "- Giờ hoạt động: 18h - 23h" [đã chạy]. Công cụ "gần một điểm" đọc cùng bảng, chỉ dòng có bài kho, không xét `khong_bua`: `backend/llm/gan_diem.py` (docstring; `ket_qua`, `_chu_gio`) [code].
- 766 / 960 ⇒ 0, 756 riêng Bà Nga bữa trưa, lịch mặc định sau sửa (Huyền Anh + Tịnh Tâm trưa ngày 1; Bà Nga tối ngày 1 gần chợ Đông Ba): người viết chạy lại vòng đếm của `data/thu_bedrock_2026-11-21/harness/c_quan_lech_bua_2311/dem_to_hop.py` (cùng danh sách `quan_dong_bua.json`, cùng 960 tổ hợp) với bảng bản 2 và bảng bản 4, `uv run --no-sync python`, chỉ chương trình, 12:14 23/11/2026 [đã chạy, riêng tư] — khớp lời commit `90df7bb3` (766 / 960, 0 after) và `HIEN_TRANG.md` mục 1 gạch "Ba bản sửa trên ĐƯỜNG DEMO". 3.066 / 3.840 ⇒ 0 / 3.840, 17.660 bữa, lượt trình duyệt (mặc định ×3, "Lịch ví dụ", tổ hợp A / B / C, một lượt sửa bằng lời), sáu quán tự đọc lại, ba quán sát mép, kho tự lệch Quán Nhỏ: `data/thu_bedrock_2026-11-21/harness/e_cham_quan_bua_2311/CHAM_E.md` mục 1, mục 4 điểm 2–3 [riêng tư; chép, đã mở nguồn; phiên đo, không viết code của nhánh]. Lượt tìm ra lỗi: `data/playwright_mcp/luot_2311/NHAT_KY.md` hàng 10:49, 10:50 [riêng tư; đã mở]. Còn lại 11 quán kho không ghi giờ, 426 ngoài kho, Cơm Tấm Okla, "Không bịa giờ cho quán kho không ghi": `guides/RUNBOOK_BAN_GIAO.md` mục 10.2 hàng "Quán gợi ý cho bữa trưa / tối của lịch và giờ mở cửa" [chép].
- Bản in vạch thẳng: `git show 23d4e363` — `frontend/src/lkh.css` khối in (`.lkh-song-ngay { display: none }`, `.lkh-dong::before` hiện lại; chú thích "nét cong lệch dần khỏi các điểm rồi chạy xuống đè hai khối quán ăn cuối ngày… trang 2") [code]; `CHAM_E.md` mục 3 ("PDF 2 trang… vạch thẳng mảnh sau các ảnh, dừng ở điểm cuối, không còn nét cong chạy qua hai khối") [chép]; người viết mở ảnh `…/e_cham_quan_bua_2311/xuat/in_trang-2.png` [đã mở ảnh, riêng tư].
- Bản chữ bỏ đuôi: `git show 0210487d` — `frontend/src/LichV2.jsx` `vanBanLich` (`.replace(/\s*—\s*sai thì bấm Sửa\.?/, ".")`, chú thích "chỉ có nghĩa trên màn hình") [code]; đuôi trên màn hình: `backend/llm/lich_trinh_v2.py` dòng 632 [code]; bản in giấu `.lich-hieu`: `frontend/src/lkh.css` chú thích "không in: … dòng \"sai thì bấm Sửa\"" [code]; PowerPoint cắt đuôi: `backend/api/lich_pptx.py` dòng 62 [code]. Mức kiểm lúc 12:10: chỉ đọc code, chưa ai xuất file sau bản sửa (phiên viết code trả lời D 12:10 23/11, chép trong lời giao V1) [chép]. Trước bản sửa file .txt có câu đó: `NHAT_KY.md` hàng 10:58 [riêng tư; đã mở].
- Lịch sử sửa bài (chuyển từ dòng "Cập nhật" 23/11): 16:11 22/11 phân xử chỗ lệch giữa các bài; trước đó sửa theo một lượt đối chiếu độc lập; 10:27 23/11 thêm phần giao diện mới (vì sao tỉ lệ in cũ "đúng nhờ may"); 11:14 23/11 áp biên bản kiểm độc lập `data/hoc_cung_D/kiem/dot_2311_k1_kiem.md` bài 30 (thêm "Cách khác" cho quyết định nhỏ tỉ lệ in — căn cứ chú thích `@media print` của `frontend/src/lkh.css` "Muốn chữ in to hơn: giảm số này (và soát lại chỗ ngắt trang)"; chuyển số đếm của bảng lưu trú, quán, ảnh và đoạn bản in xuống "Chi tiết để tra") [riêng tư; chép biên bản]; 11:14 23/11 thêm file xuất không đổi, chỗ đứng mới của bản đồ, ba giới hạn của bản in; 12:17 23/11 khớp hệ thống trưa 23/11 (quán lệch bữa, bản in vạch thẳng — bỏ giới hạn "nét cong đè hai khối quán", bản chữ bỏ đuôi "sai thì bấm Sửa", câu "gần X" của quyết định 1).

- Đợt áp biên bản kiểm độc lập (12:45 23/11/2026; `data/hoc_cung_D/kiem/dot_2311_trua_k1_kiem.md` mục "Bài 30" hàng 1, 5, 13 + câu khó hiểu [riêng tư]). Ý chính và dòng Cập nhật: câu cũ "từ 23/11 không gợi ý quán vào bữa mà kho ghi quán đóng" nói rộng hơn code (Cơm Tấm Okla ở "Giới hạn đã biết") — luật chỉ áp cho quán có `khong_bua`: `backend/llm/quan_lich.py` dòng 100 (`bua not in q.get("khong_bua", ())`) [code, đã mở]; 6 quán có `khong_bua` trong `data/phase_9/lich_trinh/bang_quan_lich_v4.json` (biên bản tự đếm; người áp đếm lại 41 quán kho, 30 có `gio_kho`, Okla không có `gio_kho` / `khong_bua`) [riêng tư; tự đếm]. Nhãn mức kiểm ô "Sao chép lịch": như gạch "Bản chữ bỏ đuôi" ở trên [chép]. Nhãn "(do công cụ tự lái)" cho hàng trình duyệt: `CHAM_E.md` mục 1 hàng "Trình duyệt" (Playwright MCP, cổng 8012) theo biên bản [chép]. Câu Bao Vinh chuyển xuống "Chi tiết để tra" để giữ độ dài. Ghi kèm cho lần sửa sau: chỗ "kho tự lệch" ở Chi tiết có bản sửa một dòng chờ gộp (`session_prompt/VIEC_DANG_MO.md`, commit `51258eae`) — khi gộp phải sửa câu đó.

- Lượt áp cuối (13:25 23/11/2026; biên bản `data/hoc_cung_D/kiem/dot_2311_trua_k2_sau_bien_ban_kiem.md` mục "Bài 30" hàng 7, 8 + ghi kèm "Lịch ví dụ (bài 27) không chọn hạng sao" [riêng tư]). Lịch "Ví dụ" dựng sẵn của trang: `backend/api/routes/cong.py` `TRUONG_MAU` (`"so_ngay": "2"`, `"ngan_sach": "vua"`, chú thích "có hạng ⇒ ví dụ có khối nơi ở"), `dung_lich_mau` (chỉ quán `nguon == "kho"`) [code, đã mở]; lịch ví dụ 3 ngày của bài 27–28: `data/hoc_cung_D/vi_du_lap_lich_vet.json` (`lich.truong` = `so_ngay` "3", không có `ngan_sach`) [riêng tư; người áp đã mở]; Bao Vinh ngày 3: bài 28 mục "Ngày 3" [chép]. File .txt tải về: `data/playwright_mcp/luot_2311_toi_nhe/NHAT_KY.md` bước "D (xuất)" 13:11 + `D_lich_da_sua.txt`, `D_lich_goc_the_chat.txt` (dòng "Mình hiểu: 2 ngày · 2 người lớn · 1 trẻ em · đi cân bằng."; 0 dòng có "sai thì bấm"; file tải trước bản sửa chữ 13:47 23/11 — nay đoàn có trẻ em ghi "đi nhẹ nhàng", bài 28 [ghi kèm 14:12 23/11/2026, `backend/llm/lich_trinh_v2.py` `dung_lich`, commit `048bd76d`]) — nhánh thử `p9-c-toi-nhe` `58e08a33` (có `0210487d`; `git diff main...58e08a33 -- frontend/src` rỗng), server tạm cổng 8061, lượt còn đang ghi lúc người áp đọc 13:12 [riêng tư; đã chạy, phiên khác; người áp đã mở]. Câu "chưa ai xuất file sau bản sửa" ở gạch "Bản chữ bỏ đuôi" là của lúc viết 12:17.

- Đợt V2 đầu chiều 23/11/2026: chỉ thêm ghi kèm ở gạch "Lượt áp cuối" (file .txt của đoàn có trẻ em tải trước bản sửa chữ 13:47). Dòng Cập nhật trước bắt đầu bằng "Cập nhật 13:25 … (49 tính năng mở, 5 tắt, kho 267 bài); đã áp hai lượt kiểm". Số tính năng 50: `session_prompt/HIEN_TRANG.md` mục 1 [chép].

- Đợt cuối chiều 23/11/2026 (Việc 1 của lời giao đợt): gạch "Từ 15:38 23/11 lệnh thêm…" — 319 lịch, 265, 41: `guides/RUNBOOK_BAN_GIAO.md` mục 10.2 hàng 'Sửa lịch bằng lời: "thêm X" SAU KHI lịch đã xếp' và `session_prompt/VIEC_DANG_MO.md` gạch "[14:51 23/11/2026]" [chép, CHƯA mở file thô — `data/thu_bedrock_2026-11-21/harness/b_day_them_2311/dem_quan.py`, `dem_bua_trua.py` không lưu đầu ra; riêng tư]; quán trưa theo điểm cuối buổi sáng: gạch "Bữa trưa" của mục "Quán ăn" bài này [đã có]; dòng ghi chú trong file tải về: `data/playwright_mcp/luot_2311_them_day_2/G_lich_A_da_day.txt` dòng 20 [riêng tư; đã chạy, phiên khác]; bản in chưa ai nhìn: cả hai nhật ký `luot_2311_them_day*/NHAT_KY.md` mục "CHƯA LÀM" ghi không bấm "In / Lưu PDF" [riêng tư, đã mở]. Dòng Cập nhật trước: "Cập nhật 14:12, ngày 23/11/2026 · khớp hệ thống 13:52 23/11 (50 tính năng mở, 5 tắt, kho 267 bài); chỉ ghi kèm một dòng Nguồn · 6 quán kho ghi rõ giờ không còn được gợi ý vào bữa quán đóng; bản in dùng vạch thẳng; bản chữ sao chép / tải về bỏ đuôi "sai thì bấm Sửa" · luật chọn và lời báo đọc từ chương trình trưa 23/11; người viết chạy lại phép đếm quán, không chạy lượt có model · lần sửa trước: Nguồn."
- Áp biên bản kiểm độc lập (`data/hoc_cung_D/kiem/dot_2311_chieu2_k1_kiem.md` mục "Bài 30" dòng 1, 2 [riêng tư]): điều kiện 2 km — `backend/llm/quan_lich.py` dòng 3, 120–121 (theo biên bản) và gạch "Bữa trưa" của bài; nhật ký `luot_2311_them_day_2/NHAT_KY.md` hàng 14:23 B (thêm Điện Hòn Chén cuối sáng, bữa trưa vẫn "gần Lăng Đồng Khánh") [code; riêng tư]. Mốc "tới 16:58 23/11" của cỡ chữ bản in: gộp `c25c3717` 16:58 (commit `a71a4b62`, chữ in 7,8 ⇒ 9,3 pt) — chưa viết vào bài, chờ phiếu [code]. Dòng Cập nhật trước: "Cập nhật 16:37, ngày 23/11/2026 · khớp hệ thống 16:23 23/11 (51 tính năng mở, 7 tắt, kho 267 bài) · "Giới hạn đã biết" thêm một gạch: quán trưa sau lệnh "thêm" điểm khi lịch đã xếp (bài 31); số chép từ sổ, người viết không đếm lại · lần sửa trước: Nguồn."
</details>
