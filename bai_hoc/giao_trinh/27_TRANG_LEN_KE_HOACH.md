# Bài 27 — Trang Lên kế hoạch: từ mấy nút chọn tới một lịch, và bảng điểm tham quan đứng sau

*Cập nhật 17:19, ngày 28/11/2026 · khớp hệ thống Đợt 6 (**`71` tính năng mở, `9` tắt**, kho 269 bài / **9.540 đoạn**, bảng điểm bản 16; `gpt-6-luna`) · bổ sung tách **2 nút PowerPoint** (*Tải PowerPoint nhanh* <1s / 0đ và *Tải PowerPoint AI ~15–20s*, tự ẩn nút AI khi tắt AI) và tái sử dụng bảng 136 cơ sở lưu trú + 3 link đặt phòng cho công cụ chat gợi ý lưu trú (bài 24, 30) · mốc trước: Nguồn.*

**Bài trước đã biết:** trợ lý trả lời câu hỏi từ kho; việc phải đúng (ngày âm lịch, thời tiết, khoảng cách) do chương trình tính (bài 24). Bài 5 đã tả trang Lên kế hoạch trông ra sao.
**Bài này thêm:** người dùng bấm "Xếp lịch" thì máy chủ nhận gì, kiểm gì, và đi qua những bước nào cho tới khi có một lịch. Bài cũng mở bảng điểm tham quan, thứ mà mọi lịch được xếp từ đó, và nói ô chat liên quan tới trang này ra sao.

## Ý chính

- Người dùng chọn bằng nút, không gõ câu. Máy chủ nhận **tám giá trị** và kiểm lại từng giá trị; sai một giá trị thì cả yêu cầu bị từ chối.
- Mọi lịch được xếp từ **một bảng 41 điểm tham quan** cùng 6 mục chỉ dùng buổi tối (bài 28), không xếp thẳng từ kho. Mỗi ô của bảng (thời lượng, giờ mở cửa…) có ghi căn cứ: từ kho, từ web, hay ước.
- Một lượt lập lịch có **một lần gọi model**, chỉ để viết câu mô tả. Việc chọn điểm, chia ngày, tính giờ là của chương trình. Ở ví dụ: khung lịch hiện sau 0,2 giây, đủ câu mô tả sau 9,3 giây.
- Gõ "lên lịch giúp mình 2 ngày" trong ô chat thì **không** ra một lịch: trợ lý trả lời bằng chữ từ kho, kèm một dòng chỉ sang trang này. Xếp lịch từ câu gõ tự do đã thử hai lần, không đạt, đang tắt.
- Đã có lịch thì câu hỏi tiếp trong ô chat được trả lời trên **đúng lịch đó**: chương trình in lịch và số giờ thành một nguồn cho model đọc.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| biểu mẫu | **form** | nhóm ô và nút để người dùng chọn giá trị rồi gửi một lần |
| kiểm khuôn | **validation**, **schema** | máy chủ đối chiếu mỗi giá trị gửi lên với một danh sách giá trị được phép; lạ là từ chối |
| bảng điểm tham quan | **itinerary table** | 47 dòng (41 điểm tham quan, 6 mục chỉ dùng buổi tối), mỗi dòng có các cột dùng để xếp lịch; nằm ngoài kho bài viết |
| cụm | **cluster** | nhóm các điểm nằm cùng một khu (ví dụ Kinh thành, bờ nam sông Hương, khu lăng Thủy Xuân); có 8 cụm |
| khung lịch | **itinerary frame** | phần lịch do chương trình dựng: ngày, buổi, tên điểm, giờ, ghi chú; chưa có câu mô tả |
| lịch đã lưu | **saved itinerary** | bản khung lịch mới nhất của một cuộc trò chuyện, máy chủ giữ trong bộ nhớ để sửa và hỏi tiếp |

## Người dùng chọn tám ô, máy chủ kiểm lại cả tám

Biểu mẫu có bốn nhóm (ai đi, đi bao lâu và khi nào, đi kiểu nào, thích gì) và một ô hạng sao chỗ ở. Chỉ số ngày là bắt buộc.

| Ô | Giá trị được phép | Làm đổi lịch thế nào |
|---|---|---|
| Số ngày | 1 tới 5 | số ngày của lịch |
| Người lớn | 1 tới 10 | **không** làm đổi lịch; chỉ hiện ở dòng "Mình hiểu…" |
| Trẻ em | 0 tới 6 | có trẻ em ⇒ lịch nhẹ: mỗi buổi một điểm, buổi tối chỉ một hoạt động nhẹ (từ 17:29 23/11; trước đó không buổi tối), tránh điểm nhiều bậc thang; đầu thẻ ghi "nhẹ nhàng" dù ô kiểu đi chọn gì (bài 28) |
| Có người lớn tuổi | có / không | như trẻ em |
| Kiểu đi | nhẹ nhàng · cân bằng · khám phá nhiều | số điểm mỗi buổi (bài 28) |
| Sở thích | tối đa 2 trong 5 loại | điểm nào được xét trước |
| Ngày đi | từ hôm nay tới 180 ngày sau; được bỏ trống | thứ trong tuần, mùa, dự báo mưa |
| Hạng chỗ ở | 1 sao · 2–3 sao · 4–5 sao; được bỏ trống | chỉ đổi khối "Nơi ở" (bài 30) |

Bấm nút "Xếp lịch N ngày" (N theo số ngày đang chọn), trang gửi lên máy chủ đúng các giá trị đã chọn, kèm một ghi chú cho máy chủ biết đây là yêu cầu từ biểu mẫu. Máy chủ kiểm lại từng giá trị theo tập được phép ở bảng trên, chặt tới kiểu dữ liệu: không nhận chữ "2" thay cho số 2, không nhận ô lạ (đủ danh sách ở "Chi tiết để tra"). Sai một chỗ thì cả yêu cầu bị từ chối với lời báo "Yêu cầu không hợp lệ." và không có lịch nào được xếp.

Qua bước kiểm, máy chủ ghép các giá trị thành một câu cố định cho lịch sử cuộc trò chuyện, ở ví dụ là *"Lên kế hoạch tham quan Huế (Thông tin thêm: 3 ngày; 2 người lớn; đi cân bằng; thích di tích.)"*. Lượt biểu mẫu đi đường riêng: không qua bước xếp loại câu (bài 22), không tra web, không đưa công cụ nào cho model, không dùng câu trả lời đã nhớ.

## Bảng điểm tham quan: 41 điểm và 6 mục tối, mỗi ô có căn cứ

Lịch không xếp thẳng từ 269 bài của kho: bài viết là văn xuôi, còn xếp lịch cần con số và nhãn đặt sẵn. Mỗi dòng có tên và tên khác, cụm, loại điểm, thời lượng ("ngắn" 75 phút hoặc "nửa buổi" 150 phút), buổi đi được, giờ mở cửa, trong nhà hay ngoài trời, có nhiều bậc thang không, thứ tự ưu tiên theo từng sở thích, thứ và mùa hoạt động, giờ của hoạt động buổi tối, và bài nguồn trong kho. 18 điểm có thêm một đoạn kho được chọn tay để model tả. Bảng đủ các cột, kèm số đếm từng cột, ở nửa để tra.

Hầu như mọi ô có thêm một dòng **căn cứ**: câu trích từ bài kho, trang web, hoặc ghi là ước. Ví dụ giờ 7:00 – 17:00 của Đại Nội là phần chung của giờ mùa hè và mùa đông, chủ dự án tra ngày 14/11.

Bảng được kiểm lúc bật máy chủ (quyết định 4). Ba bảng nhỏ đứng cạnh (toạ độ, ảnh, khoảng cách): nửa để tra.

## Một lượt lập lịch thật: năm bước, khung lịch tới trước

Ví dụ lập lịch của cả bộ, lượt thật ngày 21/11/2026: 3 ngày, 2 người lớn, cân bằng, thích di tích, không chọn ngày đi.

| Bước | Ai làm | Ở ví dụ |
|---|---|---|
| 1. Kiểm tám giá trị | máy chủ | đạt |
| 2. Xếp | chương trình, từ bảng điểm | 8 điểm ban ngày, 3 hoạt động tối (bài 28) |
| 3. Lấy nguồn | chương trình, mỗi điểm một đoạn của chính bài về điểm đó | 11 đoạn |
| 4. Gửi khung lịch | máy chủ gửi tên, buổi, giờ, ảnh, ghi chú, quán; giao diện vẽ ngay | 0,22 giây |
| 5. Viết câu mô tả | model, một lần gọi, không công cụ; chương trình kiểm từng câu (bài 29) | 9,1 giây; 0 câu bị thay |

Cả lượt 9,3 giây. Lúc câu mô tả chưa tới, mỗi điểm hiện hai vạch xám chờ chữ.

**Trang hiện lịch thế nào** (giao diện từ 23/11; vì sao đổi: bài 5). Ở màn từ 1.200 px, khi đã có lịch thật, trang chia ba cột: biểu mẫu (hẹp lại), thẻ lịch, và bản đồ đứng yên cạnh lịch khi cuộn; từ 21:49 23/11, cuộn sang ngày khác thì bản đồ tự chuyển sang ngày đang đọc (nút "Ngày N" vẫn bấm được). Mỗi ngày là một khung: các điểm theo buổi, có giờ, ảnh, nhãn loại, nối nhau bằng một dải nước nhạt có nét đứt; từ 21:49 tên điểm bấm được để mở bài kho của điểm đó, như tên quán. Màn hẹp xếp mọi khối thành một cột. Lịch ví dụ, ba kiểu đi, khung trợ lý nổi: "Chi tiết để tra".

**Bấm xếp xong, trang tự cuộn về đầu lịch** (từ 23/11). Khi khung lịch tới, trang cuộn để đầu lịch nằm ngay dưới thanh trên; lịch vừa sửa bằng lời trong khung trợ lý thì không cuộn; cột biểu mẫu thôi ghim ("Chi tiết để tra"). Mức kiểm: "Đã so", "Giới hạn đã biết".

Xong lượt, máy chủ lưu lịch vào cuộc trò chuyện, để sửa bằng lời (bài 31), tải PowerPoint mới kèm chọn bảng màu, tải tệp lịch `.ics` bản nâng cao hay in (bài 30) và trả lời câu hỏi tiếp. Bản lưu nằm trong bộ nhớ của máy chủ, hết hạn sau 30 phút không nhắn, mất khi khởi động lại máy chủ (bài 6); mỗi khi lịch đổi hoặc hoàn tác, bộ nhớ đệm bố cục slide cũ cũng được xoá theo để file tải về luôn khớp lịch mới nhất. Lịch trượt bước kiểm khung vẫn hiện nhưng không được lưu (bài 29).

**Sửa bằng lời thấy gì trên trang này** (bài 31 kể đủ). Khối chữ trên cùng cột lịch chép lại câu của lượt sửa, kèm đúng các nút như ở khung trợ lý. Từ 00:17 24/11, lệnh thiếu ngày hay buổi thì lịch đứng yên, có câu hỏi lại, các nút chỗ đặt được và nút "Xếp giúp mình"; lệnh "bỏ" làm một buổi trống thì có nút "Gợi ý điểm thay: …". Sáng 24/11 thêm ba loại nút cùng chỗ đó: thêm trước một điểm đang có, dời khi bị luật chặn, dời vào chỗ đang có điểm khác (nhãn: "Chi tiết để tra"; bài 31, quyết định 2). Buổi trống có dòng "Buổi … ngày N để trống — bạn đã bỏ điểm của buổi này." ở cuối thẻ ngày; từ 08:19 24/11, bỏ hết điểm ban ngày của một ngày thì thẻ ngày đó chỉ còn mục tối, bữa tối và dòng "Ban ngày của ngày N để trống — bạn đã bỏ các điểm của ngày này." (bài 31, quyết định 3). Từ 00:13 24/11, việc chưa làm được hiện như tin thường, không khung đỏ, kể cả khi tắt tính năng hỏi lại.

## Ô chat không tự lập lịch: chỉ đường, và đọc lịch đã lưu

Có ba tình huống ô chat chạm tới lịch.

**Gõ "lên lịch giúp mình 2 ngày ở Huế".** Trợ lý trả lời như câu hỏi thường, từ kho. Dưới câu trả lời, chương trình nối một dòng: "Muốn lịch có giờ từng điểm, bản đồ và sửa được bằng lời, bạn mở trang Lên kế hoạch." Bấm cụm "trang Lên kế hoạch" là sang trang có biểu mẫu. Câu được nhận ra bằng một khuôn chữ hẹp ("Chi tiết để tra").

**Xếp lịch thật từ câu gõ tự do** (model đọc câu rồi gọi một công cụ xếp lịch) đã thử hai lần, cả hai dưới sàn, đang tắt (bảng "Đã so"). Bộ xếp hiện nay (bài 28) có từ 14/11 và chỉ chạy qua biểu mẫu.

**Hỏi tiếp khi đã có lịch** (trên giao diện), ví dụ "lịch này ngày 1 đi mấy tiếng?". Chương trình in lịch đã lưu thành một nguồn tên "Lịch bạn đang có": từng buổi, giờ, tên điểm, và các con số do chương trình tính (giờ bắt đầu, giờ kết thúc, tổng thời lượng, ngày dài nhất). Model đọc và trích nguồn này như một đoạn kho. Nguồn không chứa câu mô tả model viết lúc trước, và nói thẳng tiền vé cả lịch chưa tính được.

## Quyết định và lý do

### 1. Vì sao người dùng chọn bằng nút, mà không gõ một câu rồi để hệ thống đọc ý?

- **Đã chọn:** trang có biểu mẫu tám ô; lịch chỉ được xếp từ giá trị của các ô.
- **Vì sao:** xếp từ câu gõ đã thử hai lần, cả hai dưới sàn ghi trước. Với nút, máy chủ nhận đúng một giá trị trong tập cho phép, không còn bước đoán "người dùng có nói số ngày không".
- **Cách khác:** model đọc câu rồi gọi công cụ xếp lịch: đã đo hai lần, đang tắt. Một bản nhẹ hơn (chỉ dẫn sang trang) đang mở.
- **Cái giá:** người quen gõ phải chuyển trang và bấm nút. Những gì biểu mẫu không có ô (giờ tới, giờ về, "chỉ đi buổi sáng") thì không nói được khi lập lịch; một phần nói được sau, bằng lời sửa (bài 31).

### 2. Vì sao xếp lịch là việc của chương trình, còn model chỉ viết câu mô tả?

- **Đã chọn:** chương trình chọn điểm, chia ngày và buổi, tính giờ, chọn quán, gắn ảnh, viết ghi chú. Model chỉ viết mô tả cho từng điểm của khung đã xếp.
- **Vì sao:** thiết kế ghi một luật chung: phép tính, luật, giờ, chọn quán, chọn ảnh do chương trình làm; model chỉ diễn đạt. Luật này rút từ các lần để model tính bị âm: model dặn "đừng cộng tổng tiền" vẫn tự cộng (bài 24), và ở bản lịch đầu, khi khuôn lịch đổi thì model viết lệch khung, tự thêm giờ.
- **Cách khác:** để model tự xếp lịch từ các đoạn kho: không làm. Bản đầu đã cho model viết cả lời lịch theo khung (07/11); bản hiện nay thu lại còn mỗi câu mô tả.
- **Cái giá:** lịch chỉ hay bằng luật và bảng. Điểm ngoài bảng không bao giờ được xếp; luật thiếu một tình huống thì lịch sai lặp lại được (bài 28).

### 3. Vì sao máy chủ kiểm lại các giá trị, khi giao diện đã chỉ cho bấm giá trị đúng?

- **Đã chọn:** máy chủ kiểm khuôn từng giá trị và từ chối cả yêu cầu khi có một chỗ sai.
- **Vì sao:** chương trình ghi rõ: giá trị gửi từ trình duyệt là dữ liệu không tin cậy. Thứ nằm ở giao diện thì người dùng sửa được (bài 6); một yêu cầu cũng có thể được gửi thẳng tới máy chủ mà không qua trang.
- **Cách khác:** tin giao diện, chỉ kiểm số ngày: không làm.
- **Cái giá:** giao diện và máy chủ phải khớp tập giá trị; lệch thì người dùng bấm đúng mà vẫn bị từ chối. Để hai bên khớp nhau, lúc mở trang, trang hỏi máy chủ những ô nào đang dùng rồi mới vẽ biểu mẫu.

### 4. Vì sao bảng điểm có một chỗ sai thì máy chủ không bật lên?

- **Đã chọn:** lúc bật, máy chủ kiểm bảng điểm và bảng ảnh: đủ cột, giá trị trong tập được phép, không trùng mã, điểm ưu tiên đúng sở thích, đoạn mô tả chọn tay thuộc đúng bài và còn trong chỉ mục. Sai ⇒ dừng hẳn, báo đúng chỗ sai.
- **Vì sao:** chú thích trong chương trình ghi bài học ngày 10/11: có lần thiếu file thì tính năng tự tắt mà không ai biết. Với đoạn mô tả: không lặng lẽ quay về một đoạn kém hơn.
- **Cách khác:** bật máy chủ, tắt riêng trang Lên kế hoạch và báo lỗi: chưa thử.
- **Cái giá:** một lỗi nhỏ ở bảng (hay dựng lại chỉ mục mà quên cập nhật đoạn mô tả) làm cả hệ thống không vào được, kể cả ô hỏi đáp (bài 6).

## Nếu… thì sao

Lời báo trong ngoặc kép là nguyên văn trong chương trình. Đọc từ chương trình, chưa thử thật, trừ hai dòng cuối (đã thử: bài 6; thấy trên ảnh chụp 23/11).

| Nếu | Hệ thống làm gì | Người dùng thấy gì | Muốn hết thì ai làm gì |
|---|---|---|---|
| một giá trị sai khuôn (ngày đi quá 180 ngày, sở thích đang ẩn) | từ chối cả yêu cầu | "Yêu cầu không hợp lệ." | người dùng chọn lại |
| trang Lên kế hoạch đang tắt | giao diện ẩn mục này | mở thẳng địa chỉ trang: "Tính năng này chưa bật." | người vận hành bật lại |
| bảng điểm sai, hoặc đoạn mô tả không còn trong chỉ mục | máy chủ không bật | không vào được trang nào | người vận hành sửa bảng hoặc chỉ mục |
| hỏi tiếp sau hơn 30 phút không nhắn | lịch đã hết hạn | câu trả lời không dựa trên lịch, không lời báo | xếp lại lịch; chưa có lời báo |
| máy chủ khởi động lại giữa cuộc **(đã thử)** | mất lịch đã lưu | thẻ lịch vẫn hiện; lệnh sửa bị coi như câu hỏi thường | tải lại trang, xếp lại |
| mở khung trợ lý nổi trên cửa sổ rộng 1280 px **(đã thấy trên ảnh chụp)** | khung nổi đè lên phần phải trang | mép phải cột lịch và cột bản đồ bị che; ghim trên bản đồ đổi theo lệnh sửa (suy từ chương trình) nhưng không thấy | đóng khung, hoặc bấm "Mở trang đầy đủ"; đổi chỗ đứng là việc nhóm để sau |

## Dễ nhầm

- **"Lịch được xếp từ kho 269 bài."** Không. Lịch xếp từ bảng 41 điểm (và 6 mục buổi tối); kho chỉ cho mỗi điểm một đoạn để model tả.
- **"Model đọc ý người dùng rồi lên lịch."** Ở trang này model không đọc ý gì: người dùng bấm nút, chương trình xếp, model chỉ viết câu mô tả.

## Câu hỏi tự kiểm

Thử trả lời bằng lời của mình trước khi bấm mở đáp án.

<details>
<summary>1. Biểu mẫu đã chỉ cho bấm giá trị đúng, sao máy chủ còn kiểm?</summary>

Giá trị từ trình duyệt là dữ liệu không tin cậy: người dùng sửa được giao diện, hoặc gửi thẳng yêu cầu tới máy chủ.

</details>

<details>
<summary>2. Một lượt lập lịch gọi model mấy lần, để làm gì?</summary>

Một lần, không công cụ, chỉ để viết câu mô tả. Phần còn lại do chương trình, nên khung lịch hiện sau 0,2 giây, câu mô tả tới sau khoảng 9 giây.

</details>

<details>
<summary>3. Người dùng gõ "lên lịch giúp mình 3 ngày" trong ô chat thì thấy gì?</summary>

Câu trả lời bằng chữ từ kho, kèm một dòng chỉ sang trang Lên kế hoạch. Xếp lịch thật từ câu gõ đã thử hai lần, đang tắt.

</details>

## Cấu hình đang chạy

*Theo cấu hình và chương trình trưa 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| `len_ke_hoach_v2` | đang mở (từ 14/11) | biểu mẫu bốn nhóm và bộ xếp hiện nay; chủ dự án quyết bật sau nghiệm thu | bản đầu (07/11) chạy tới 14/11 |
| `lich_trinh_bieu_mau` | đang mở (từ 07/11) | đường riêng cho lượt biểu mẫu: không xếp loại câu, không công cụ, không tra web | — |
| `len_ke_hoach_o_hien` | 8 ô (số ngày, người lớn, trẻ em, người lớn tuổi, kiểu đi, sở thích, ngày đi, hạng chỗ ở) | ô nào dưới sàn mô phỏng thì bỏ khỏi đây | — |
| số ngày tối đa | 5 | chủ dự án chốt khi duyệt thiết kế | bản đầu nhận tới "4+" |
| sở thích tối đa | 2 | thiết kế; hai sở thích được xét xen kẽ (bài 28) | bản đầu nhận 1 |
| ngưỡng hiện một loại sở thích | ≥ 4 điểm trong bảng | chủ dự án chốt; hiện cả 5 loại đều đủ | — |
| ngày đi xa nhất | 180 ngày | thiết kế ghi, chưa thấy lý do riêng | — |
| `len_ke_hoach_so_thich_an` | rỗng | ẩn loại sở thích dưới sàn "≥ 50 % suất của từng lịch 2 ngày"; ngày 13/11 lễ hội chỉ 43 %, nhóm gắn thêm nhãn cho Cung An Định (có căn cứ kho) thì lên 50 % | — |
| `lich_trinh_bang_v2` | bảng điểm bản 16 (từ 21:46 23/11) = bản 15 từng dòng + tên gọi tắt một chữ cho ba quán cà phê tối (HANOK, MoKa, TIME; bài 29 kể đủ): 41 điểm + 6 mục chỉ dùng buổi tối (4 quán cà phê, AEON Mall Huế, công viên ven sông Hương) = 47 dòng, kèm thứ tự chọn buổi tối và danh sách 8 mục tối nhẹ (bài 28); lịch xếp ra không đổi so với bản 15 | thiếu file hay thiếu cột ⇒ máy chủ không bật | bản 34 điểm tới 15/11; bản 10 (41 điểm) tới 14:56 23/11; bản 12 (dựng 12:43, vào nhánh chính 14:56) tới 16:38; bản 13 16:38 – 17:14; bản 14 (45 dòng) 17:14 – 18:43; bản 15 18:43 – 21:46 ("Chi tiết để tra") |
| `len_lich_dan_trang` | đang mở (từ 21:54 21/11) | dòng chỉ sang trang khi gõ câu nhờ lập lịch | — |
| `lich_trinh` | **đang tắt** | xếp lịch từ câu gõ tự do (bản đầu) | đã đo hai lần, không đạt |
| `lich_vao_hoi_thuong` | đang mở (từ 19/11) | nguồn "Lịch bạn đang có" cho câu hỏi tiếp; chủ dự án chọn bật riêng phần lịch và số giờ | bản có tổng tiền vé do chương trình tính: thử, chưa bật (giới hạn đã biết) |
| hạn lưu lịch | 30 phút từ lượt cuối, cùng cuộc trò chuyện | bài 6 | — |
| mức suy luận của lần viết câu mô tả | thấp | ghi trong chương trình | — |

## Đã so

**Vấn đề thật:** người dùng muốn một lịch đi Huế; cần biết cách nào cho lịch đúng luật và hợp người đi cùng.

| Cách | Đo trên gì | Kết quả | Kết luận |
|---|---|---|---|
| Model đọc câu gõ, gọi công cụ xếp lịch (lần 1, 05–06/11, gpt-6-luna) | bộ câu kín 5 câu | 3 / 5 | tắt |
| Như trên, sửa ba lỗi bằng chương trình (lần 2, 09/11, gpt-6-luna) | 27 câu, hai người chấm ý "hợp người đi cùng" | 27 / 27 câu ra lịch; hợp người đi cùng 21 / 27 và 15 / 27 (sàn 26) | đóng hồ sơ; gốc lỗi ở luật xếp và bảng điểm dùng chung |
| Biểu mẫu bản đầu, chương trình xếp, model viết lời theo khung (07/11, gpt-6-luna) | sàn kiểm bằng chương trình 24 phép; lời khớp khung 12 lịch × 2 lượt | 24 / 24; 12 / 12 hai lượt; chữ đầu của câu chậm (p95) 4,25 giây | bật 07/11 |
| Biểu mẫu bản hiện nay (bài 28, 29) | nghiệm thu 13–14/11 | bài 29 | bật 14/11 |
| Dòng chỉ sang trang trong ô chat (20–21/11) | bộ câu mù 20 câu phải nhận + 20 câu giống mà không phải; lượt trình duyệt 21/11 | nhận 17 / 20, nhận nhầm 0 / 20; lượt trình duyệt đạt ở màn rộng và màn hẹp | mở 21/11 |
| Lịch đã lưu vào câu hỏi tiếp (19/11, gpt-6-luna) | 3 kịch bản từng nói chắc mà sai; 57 lượt | cả 3 nay trả lời trên đúng lịch; 0 lượt bị rút / 57 | mở 19/11 |

**Đọc bảng thế nào:** hai lần xếp từ câu gõ hỏng ở cùng một chỗ là lịch không hợp người đi cùng, không phải ở việc đọc câu. Bản biểu mẫu hiện nay đổi cả luật xếp lẫn bảng điểm, nhưng **chưa ai đo lại** đường câu gõ với luật mới.

**Giới hạn của phép đo:** các phép so ở bảng đều đo với gpt-6-luna; với Claude Sonnet 5.5 mới có lượt thật lẻ (như lượt ví dụ).

**Vị trí trang sau khi bấm xếp (23/11, trình duyệt do công cụ tự lái).** Vấn đề thật: lượt dùng như người thật sáng 23/11 bấm "Xếp lịch 2 ngày" ở màn 1536 × 695 thì trang đứng ở cuối lịch hoặc đáy trang, đầu lịch nằm 2.282 và 3.257 px phía trên. Người viết code sửa; một phiên khác (không viết code của bản này) đo bằng đúng phép của lượt tìm ra lỗi.

| Cỡ màn | Trước sửa | Sau bản sửa đầu (cuộn ngay khi lượt mở) | Sau bản sửa thứ hai (chờ khung lịch tới) |
|---|---|---|---|
| 1536 × 695 | 2 / 2 lần đầu lịch ngoài khung nhìn | 7 / 7 lần đầu lịch trong khung nhìn (3 mặc định, 3 tổ hợp, 1 "như ví dụ"; khối "Tổng quan" cách mép trên 303–449 px); lượt sửa bằng lời: trang đứng yên | 1 lần (12:35 23/11): khối "Tổng quan" cách mép trên 303 px |
| 390 × 844 | đầu lịch trong khung nhìn, ngay dưới nút (biểu mẫu không ghim ở cỡ này) | không đổi: trang không cuộn, vì lúc lượt mở trang một cột còn quá ngắn | 1 lần (12:38 23/11): trang cuộn xuống, "Tổng quan" cách mép trên 299 px (trước: 675 px) |

**Đọc bảng thế nào:** ở màn hẹp người dùng vẫn thấy đầu lịch ngay dưới nút cả trước lẫn sau; bản sửa thứ hai chỉ để trang cuộn hẳn lên dưới thanh trên. **Giới hạn:** mọi lượt do công cụ lái trình duyệt chạy, chưa ai bấm tay trên trình duyệt có màn hình; bản sửa thứ hai (bản đang chạy) mới có một lần đo ở mỗi cỡ màn, bấm nút "Xếp lịch 2 ngày", trong một lượt tự lái đã đi đủ các bước, do một agent con chạy, chưa có người thứ hai kiểm (phiên đo thoát đột ngột lúc 12:43, chưa kịp ghi sổ); chưa ai chạy lại.

## Quyết định nhỏ hơn

**Vì sao có ô không làm đổi lịch (số người lớn), và có loại sở thích bị ẩn?** Luật thiết kế của biểu mẫu là "ô nào hiện thì phải đổi được lịch". Loại sở thích nào có dưới 4 điểm trong bảng thì ô đó không hiện (hiện cả 5 loại đều đủ); ngưỡng 4 do chủ dự án chốt khi duyệt thiết kế. Lý do của chính con số 4: chưa thấy ghi lý do. Điều thấy được: lúc chốt, hai loại chụp ảnh và lễ hội đứng đúng ngưỡng 4. Ô số người lớn là ngoại lệ được ghi là "có chủ ý": chủ dự án đã chốt biểu mẫu có số người, ô này để dành cho lúc làm phần chi phí. Cái giá: người dùng có thể nghĩ đi 6 người thì lịch khác đi 2 người; thật ra khung giống hệt.

**Vì sao ô chat chỉ dẫn sang trang, mà không tự lập lịch?** Đo ngày 20/11 qua giao diện thật: câu nhờ lập lịch gõ trong ô chat nhận một lịch bằng chữ chung chung lấy từ bài lịch trình mẫu của kho, không nhắc tới trang có giờ, bản đồ, sửa bằng lời. Dòng chỉ đường là bản nhỏ nhất sửa được việc đó, không thêm lời gọi model. Cách khác (lập lịch ngay trong ô chat) đã thử hai lần, đang tắt. Cái giá: người dùng phải bấm thêm và chọn lại bằng nút những gì đã gõ; khuôn nhận câu hẹp (bộ câu mù của một phiên khác: nhận 17 / 20, nhận nhầm 0 / 20).

## Các cột của bảng điểm

| Cột | Ví dụ ở dòng Đại Nội | Cả bảng |
|---|---|---|
| tên và tên khác | Đại Nội Huế; Hoàng thành Huế, Đại Cung… | 41 điểm |
| cụm | Kinh thành | 8 cụm; một cụm "phía nam xa" (khoảng 40 km trở lên) chỉ xếp khi đi từ 3 ngày |
| loại | di tích | 5 loại: di tích 19 điểm, thiên nhiên 10, chụp ảnh 9, ẩm thực 7, lễ hội – nghệ thuật 6 (một điểm có thể mang hai loại) |
| thời lượng | nửa buổi (150 phút) | 21 điểm "ngắn" (75 phút), 20 điểm "nửa buổi" |
| buổi hợp | sáng, chiều | 37 điểm đi được ban ngày; 5 điểm có hoạt động buổi tối (từ 16:38 23/11 Chợ Đông Ba chỉ còn ban ngày; trước đó 6), cộng 6 mục chỉ dùng buổi tối (4 quán cà phê từ 16:38; AEON Mall, công viên ven sông từ 18:43) |
| giờ mở cửa | 7:00 – 17:00 | 21 điểm có khung giờ; 20 điểm kho không ghi giờ ⇒ không ràng buộc |
| trong nhà hay ngoài trời | ngoài trời | 29 ngoài trời, 6 trong nhà, 6 cả hai |
| nhiều bậc thang | không | 11 điểm |
| ưu tiên theo sở thích | số 1 của "di tích" và của "chung" | mỗi sở thích 3–4 điểm ưu tiên |
| thứ, mùa | — | 1 điểm đóng cửa một ngày trong tuần, 1 điểm chỉ mở vài tối, 1 điểm tạm dừng theo mùa (thác Nhị Hồ, tháng 9 tới tháng 2) |
| đoạn mô tả chọn tay | — | 18 điểm có một đoạn kho được chọn sẵn để model tả |
| bài nguồn trong kho | bài Đại Nội Huế | mọi điểm |

## Giới hạn đã biết

- Bảng chỉ 41 điểm (và 6 mục chỉ dùng buổi tối). Điểm ngoài bảng không bao giờ vào lịch, dù kho có bài.
- Tên Trung tâm Nghệ thuật Lê Bá Đảng trên thẻ lịch không bấm được (dòng đó dùng chung bài với phố đi bộ Nguyễn Đình Chiểu); 46 / 47 dòng bảng có link.
- Bản đồ tự theo ngày đang đọc chỉ ở màn rộng, khi bản đồ đứng cạnh lịch; chưa có lượt trình duyệt nào trên nhánh chính sau gộp nhìn việc này.
- Biểu mẫu giữ lựa chọn khi rời trang rồi quay lại (từ 17:15 23/11): thấy một lần trên trình duyệt chiều 23/11 (3 ngày, 1 trẻ em, có người lớn tuổi, "Cân bằng" còn nguyên sau khi sang Trang chủ rồi về; agent con, chưa có người thứ hai kiểm). CÒN: lịch đã đổi tham số bằng lời ("thêm một trẻ em") thì biểu mẫu vẫn theo lần gửi biểu mẫu gốc, như nút "Sửa"; tải lại trang hay mở tab thứ hai thì cả lịch lẫn biểu mẫu mất.
- Thời lượng của 31 điểm dựa vào web, 2 điểm là ước; sai thì giờ gợi ý sai theo.
- Ô số người lớn chưa làm đổi lịch.
- Chưa có ô giờ tới, giờ về: ngày đầu và ngày cuối vẫn xếp đủ buổi.
- Lịch đã lưu mất sau 30 phút không nhắn hoặc khi máy chủ khởi động lại; người dùng không được báo.
- Hỏi tổng tiền vé của lịch: model tự cộng giá vé từ kho trên đúng lịch (lượt thật 19/11: đúng 3 / 3), không phải số chương trình tính.
- Ở cửa sổ rộng 1280 px, khung trợ lý nổi mở ra che hết cột bản đồ và mép phải cột lịch; ở 1536 px nó che gần hết cột bản đồ. Vì vậy lúc sửa lịch bằng lời không thấy ghim đổi theo. Nhóm để sau lượt gộp giao diện (đổi chỗ đứng của thứ người dùng thấy), chưa chữa.
- Tự cuộn về đầu lịch theo bản đang chạy (bản sửa thứ hai, 23/11) mới được nhìn một lần ở mỗi cỡ màn, bằng trình duyệt do công cụ tự lái, trong một lượt đã đi đủ các bước, do một agent con chạy, chưa có người thứ hai kiểm; chưa ai chạy lại, chưa ai bấm tay.
- Trên ảnh chụp của lượt kiểm trước khi gộp, ô ngày đi hiện kiểu mm/dd/yyyy (tháng / ngày / năm). Nhóm ghi là vết của phép chụp, vì trình duyệt chụp chạy tiếng Anh (suy luận, chưa chụp lại trên trình duyệt tiếng Việt); không sửa. Ngày gửi lên máy chủ luôn ở dạng năm-tháng-ngày.

## Chi tiết để tra

- **Sửa lịch trên trang này, sáng 24/11 (chuyển từ thân bài khi viết đợt này).** Khối đầu cột lịch mở bằng "Đã sửa theo lời bạn:" rồi các câu của những việc đã làm, kèm dòng "Biểu mẫu vẫn là bản gốc — xếp lại từ biểu mẫu sẽ thay bản đã sửa."; các câu hỏi lại và nút đứng ngay dưới. Ba loại nút mới (bài 31, quyết định 2): "Đặt X trước Y" (từ bản gộp chèn-trước) · "Dời sang buổi … ngày N", thêm "(đổi chỗ với Y)" khi chỗ đích đang có đúng một điểm (lệnh dời bị luật chặn) · "Dời X sang buổi … ngày N (đổi chỗ với Y)" (lệnh dời gõ tay vào chỗ đang có điểm khác; lịch đứng yên tới khi bấm). Ngày bị bỏ hết điểm ban ngày (từ 08:19 24/11), thấy trên trình duyệt ở lịch ví dụ 2 ngày sau "bỏ Lăng Tự Đức", "bỏ Lăng Khải Định": phần "Tổng quan" ghi "Ngày 2 Bến Trăng Café & Bar"; khung ngày 2 chỉ có thẻ tối Bến Trăng (19:00 – 20:30), khối "Ăn tối gần Bến Trăng Café & Bar", không có khối ăn trưa, rồi dòng "Ban ngày của ngày 2 để trống — bạn đã bỏ các điểm của ngày này."; bản đồ lúc chụp đang ở "Ngày 1", 4 ghim (ba điểm ban ngày và phố đi bộ của ngày 1). Ngày đi xa bị bỏ hết điểm thì khung ngày không còn thẻ nào; dưới khung có hai dòng, "Tối tự do — buổi tối của ngày này để trống." và dòng ban ngày để trống (người viết chạy hàm, chưa thấy trên trình duyệt).
- Chuyển từ thân bài lúc áp biên bản 01:14 24/11 (không đổi nội dung): cột biểu mẫu cuộn theo trang, không còn ghim (từ 23/11): biểu mẫu cao khoảng 1.900 px, ghim thì nút "Xếp lịch" chỉ với tới được ở đáy trang.

- Lượt ví dụ (21/11/2026, Claude Sonnet 5.5): khung lịch 219 ms; lời gọi viết câu 9.096 ms; cả lượt 9.320 ms; 5.592 token vào, 1.137 token ra, 0 token suy luận; 0,022554 USD; 11 nguồn được trích; 0 câu dự phòng; không có dự báo (không chọn ngày đi). Lịch: ngày 1 Đại Nội (sáng), chùa Thiên Mụ và Kinh thành (chiều), chợ Đông Ba (tối); ngày 2 lăng Tự Đức, lăng Khải Định, phố đi bộ Nguyễn Đình Chiểu; ngày 3 phố cổ Bao Vinh, Quốc Học, cung An Định, phố Tây. Từ 16:38 23/11 cùng biểu mẫu giữ nguyên ban ngày, ba buổi tối là phố đi bộ Nguyễn Đình Chiểu, quán Bến Trăng, Ca Huế trên sông Hương; bảng bản 15 (18:43) ra y như vậy (bài 28; người viết tự chạy hàm, không qua model).
- Trên đường gửi dần, lượt biểu mẫu có các tin: trạng thái "đang xếp", khung lịch, từng câu mô tả, "lịch xong", rồi chữ thuần của cả lịch (dùng cho lịch sử và nút sao chép).
- Lượt biểu mẫu, lượt sửa lịch và việc nạp lịch đã lưu chỉ chạy trên đường gửi dần (đường giao diện dùng); đường trả cả câu một lần không nạp lịch đã lưu. Vì sao: chưa thấy ghi lý do. Điều thấy được: giao diện chỉ dùng đường gửi dần.
- Khi chưa xếp lịch nào, trang hiện một lịch **ví dụ** 2 ngày do chính bộ xếp dựng từ một tổ hợp cố định; câu mỗi điểm của lịch ví dụ do chương trình viết, không gọi model.
- Chuyển từ thân bài 00:44 24/11 (không đổi nội dung): rời trang rồi quay lại khi đã có lịch: từ 17:15 23/11 biểu mẫu điền lại theo lịch đang hiện (trước đó về mặc định, bấm xếp lại ra lịch của đoàn khác, không báo) · bảng điểm soạn qua nhiều bản (gạch "Bảng điểm qua các bản"); chủ dự án chọn thêm 7 nơi ngày 15/11; các điểm ưu tiên và các ca khó (thác Nhị Hồ bỏ khỏi lịch những tháng nào, giờ của Đại Nội) do chủ dự án chốt · tự cuộn về đầu lịch: bản đang chạy đã được nhìn một lần ở mỗi cỡ màn, trên trình duyệt do công cụ tự lái trưa 23/11 (đầu lịch nằm trong màn hình; agent con chạy, chưa có người thứ hai kiểm).
- Tên điểm bấm mở bài (từ 21:49 23/11; chủ dự án lúc tự thử: "nên để cho người dùng click vào được các bài như đại nội huế, đầm chuồn, phố đi bộ chứ, hiện tại chỉ click vào được các món ăn"): máy chủ gửi kèm mỗi mục của khung lịch đường dẫn bài kho của điểm (lấy từ cột bài nguồn của bảng điểm; không vào tin gửi model), giao diện biến tên thành link như tên quán. Từ 22:00 23/11, hai dòng bảng dùng chung một bài thì chỉ dòng đứng trước giữ link: Trung tâm Nghệ thuật Lê Bá Đảng lấy tư liệu từ bài phố đi bộ Nguyễn Đình Chiểu, bấm tên trung tâm từng mở ra bài phố đi bộ (người đọc code bắt được trước khi tới người dùng); nay 46 / 47 dòng có link. Mục "Tối nghỉ" không có link. Bản in bỏ gạch chân của link. Lịch ví dụ dựng bằng cùng bộ dựng nên cũng có link (suy từ code, chưa thử).
- Bản đồ theo ngày đang đọc (từ 21:49 23/11; chủ dự án: "sau khi lướt từ ngày 1 xuống ngày 2 thì bản đồ lịch trình phía bên phải có tự chuyển sang ngày 2 được không ?"): "ngày đang đọc" là ngày có phần đầu đã cuộn lên quá gần nửa trên màn hình (ngày cuối cùng có mép trên đã lên tới vạch 40 % chiều cao khung nhìn, tính từ trên xuống, hoặc cao hơn, kể cả đã cuộn khuất); bản đồ chỉ đổi khi người đọc SANG một ngày khác, nên bấm tay "Ngày N" rồi cuộn trong cùng ngày thì không bị giật lại. Chỉ chạy khi bản đồ đang đứng cạnh lịch (màn rộng của trang Lên kế hoạch); màn hẹp và thẻ lịch trong khung trợ lý thì không. Người viết code nhìn ở 1536 × 695 và 390 (lời commit); chưa có lượt trình duyệt trên nhánh chính sau gộp.
- Nút tải bản chữ (.txt) đã bỏ từ 21:49 23/11 ở mọi chỗ hiện lịch (bài 30); không có đường máy chủ nào cho file này — file từng được dựng trong trình duyệt. Từ Đợt 5A (28/11/2026), dưới thẻ lịch thêm bộ chọn 3 bảng màu cho PowerPoint mới, nút `.ics` gọi máy chủ khi đã chọn ngày đi, và dưới mỗi khách sạn gợi ý có 3 link `Booking`, `Agoda`, `Traveloka` kèm nút **"Chép mẫu hỏi phòng"** 6 trường (`0 đồng`).
- Lịch đã lưu không ghi ra đĩa; câu an toàn bão lũ (nếu lượt đó có) được giữ cùng bản lưu để file tải về còn câu đó.
- Giao diện trang này từ 23/11 (sửa trước khi gộp, so với bản dựng thử đầu tối 22/11): cột biểu mẫu chỉ hẹp lại 300 px khi đã có lịch thật kèm bản đồ (ở 300 px với lịch ví dụ, nhiều mục xuống dòng và nút "Xếp lịch" tụt khoảng 400 px); thẻ lịch dùng hết cột ở mọi bề rộng; dòng "Đã sửa theo lời bạn" dừng ở mép cột lịch, không lấn sang cột bản đồ; mỗi quán gợi ý một hàng, quán không ảnh thụt vào cho thẳng cột tên; bản đồ thấp lại ở khung nhìn thấp (cao 240–400 px) để nút ngày, bản đồ, danh sách điểm nằm trọn màn khi đi theo lúc cuộn; ba kiểu đi mỗi kiểu một hàng ở mọi bề rộng (trước: ba cột hẹp, một hai chữ mỗi dòng ở điện thoại và 1.024–1.152 px); nhãn "Ngày đi (không bắt buộc)" nằm trên ô ngày. Hai lỗi có sẵn ở giao diện cũ được chữa cùng đợt: ảnh điểm gần đáy màn bị cắt thành một dải hẹp khi dừng cuộn (gỡ hiệu ứng ảnh lộ dần theo cuộn), và "Ghi chú của lịch" mất chấm đầu dòng.
- Dải đầu trang có nét sông chạy dọc mép dưới, hết bề ngang màn (chỉ trên màn hình). Nét đứt trên đường nối các điểm chạy khi máy không bật giảm chuyển động; dải nước nhạt vẫn vẽ dần khi cuộn như bản cũ.
- Bảng điểm qua các bản: bản 8 (13/11, 34 điểm), bản 9 (15/11, thêm 7 điểm: chùa Từ Hiếu, cầu Trường Tiền, đèo Hải Vân, chợ Bến Ngự, làng nón Tây Hồ, nhà vườn An Hiên, đầm Lập An), bản 10 (17/11, giờ tối chợ Đông Ba 18:00 – 23:00). Ba nơi khác bị loại khi thêm vì thiếu căn cứ. Bản 11 (19/11) có cột giá vé, chưa dùng. Bản 12 (dựng 12:43, vào nhánh chính 14:56 23/11) = bản 10 + danh sách hoạt động tối nhẹ. Bản 13 (vào nhánh chính 16:38 23/11): Chợ Đông Ba bỏ buổi tối, thêm 4 quán cà phê có bài kho chỉ dùng buổi tối (ở cuối bảng), thêm thứ tự chọn buổi tối. Bản 14 (17:14 23/11): giờ ghé cho cầu Trường Tiền buổi tối và cho quán, chữ ghi chú tối của phố Tây, Ca Huế đứng trước phố Tây trong thứ tự chọn. Bản 15 (vào nhánh chính 18:43 23/11): thêm AEON Mall Huế (cụm An Cựu) và công viên ven sông Hương ở cuối bảng, chỉ dùng buổi tối, cả hai vào danh sách tối nhẹ; ban ngày không đổi (bài 28). Bản 16 (21:46 23/11): bản 15 từng dòng, thêm tên gọi tắt HANOK, MoKa, TIME để lệnh "thay HANOK bằng MoKa Kafe" chủ dự án gõ lúc tự thử được nhận; lịch xếp ra không đổi (bài 29).
- Ba bảng nhỏ cạnh bảng điểm, đều ngoài kho: bảng toạ độ (bản 11: 46 dòng, 45 có vị trí; AEON Mall không có) và bảng ảnh (bản 9: 45 ảnh cho 47 dòng), bài 30; và bảng khoảng cách giữa 40 điểm (không gồm 6 mục buổi tối), dựng một lần ngày 16/11 bằng một dịch vụ chỉ đường. Trợ lý dùng bảng khoảng cách khi được hỏi "từ A sang B bao xa" (bài 24); bộ xếp lịch không dùng.
- Bảng khoảng cách: 40 điểm × 39 chiều; km và phút theo đường ô tô, không tính kẹt xe; lúc trả lời không gọi mạng.
- Căn cứ của cột thời lượng (chuyển từ thân bài 23/11): đây là cột dựa vào web nhiều nhất, 31 điểm lấy từ web, 8 từ kho, 2 điểm ước. Có ngày đi trong 7 ngày tới thì bước xếp lấy thêm dự báo thời tiết một lần (chuyển từ thân bài 23/11).
- Khuôn nhận câu nhờ lập lịch trong ô chat (chuyển từ thân bài 23/11): lời nhờ, chữ "lịch / lịch trình / kế hoạch", và số ngày; không nêu số ngày thì không có dòng.
- Máy chủ kiểm lại lượt biểu mẫu, đủ danh sách (chuyển từ thân bài 23/11): các ô số người phải là số thật (không nhận chữ "2" thay cho số 2), số ngày chỉ nhận đúng một trong năm giá trị 1–5, không nhận ô lạ, sở thích không trùng nhau và không quá hai, ngày đi đúng dạng năm-tháng-ngày và nằm trong 180 ngày tính theo ngày Việt Nam, sở thích gửi lên phải là loại đang hiện trên biểu mẫu.
- Trang hiện lịch, phần chi tiết (chuyển từ thân bài 23/11): lúc chỉ có lịch ví dụ, biểu mẫu giữ bề rộng cũ và không có cột bản đồ (lịch ví dụ dựng không kèm toạ độ). Nét đứt trên đường nối các điểm đứng yên khi máy bật giảm chuyển động; bản in không có nét đứt (bài 30). Ba kiểu đi mỗi kiểu một hàng, có 2, 3 hoặc 4 chấm và một câu như "khoảng 2 điểm một ngày". Khung trợ lý nổi mở đè lên phần phải trang: ở 1536 px che gần hết cột bản đồ, ở 1280 px che hết cột bản đồ và mép phải cột lịch (bảng "Nếu… thì sao", "Giới hạn đã biết").
- Tự cuộn về đầu lịch (từ 23/11): chỉ khi lịch ĐỔI sau lúc trang đã mở (vào lại trang đang có lịch thì không cuộn), không phải bản vừa sửa bằng lời; cả nút "Xếp lịch N ngày" lẫn "Xếp lịch như ví dụ". Khung lịch dừng cách mép trên màn hình 96 điểm ảnh, tức nằm ngay dưới thanh menu (thanh này cao 69 điểm ảnh). Từ lịch về biểu mẫu: nút "Sửa — điền lại biểu mẫu". Máy bật giảm chuyển động thì nhảy thẳng, không trượt. Bản sửa đầu cuộn ngay lúc lượt mở; bản thứ hai chờ khung lịch tới, vì lúc lượt mới mở cột lịch chỉ có ba chấm chờ và ở bố cục một cột trang còn quá ngắn để cuộn (phiên đo thấy đầu lịch đứng ở 472 px thay vì dưới thanh trên).
- Bản đồ đứng cạnh lịch chỉ ở trang Lên kế hoạch; thẻ lịch trong khung trợ lý nổi và trang Trợ lý nằm ngoài bố cục ba cột nên bản đồ vẫn nằm dưới lịch. Vì sao: chú thích bảng kiểu của trang ghi rõ phần đó "không đổi"; chưa thấy ghi lý do riêng.

**Bài sau (bài 28):** chương trình xếp lịch theo luật nào, đi từng bước trên chính lịch ví dụ này.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Ô biểu mẫu, giá trị cho phép, kiểm khuôn: `backend/llm/hoi_lai.py` (`TruongInput`: `extra="forbid"`, số kiểu chặt, `so_thich` ≤ 2 không trùng; `loi_v2`: ngày đi trong `NGAY_DI_TOI_DA` = 180 ngày theo `nl.hom_nay()`, sở thích phải đang hiện; `ghep_cau_v2`); `backend/api/routes/chat.py` (`_kiem_truong_v2`, `_model_query`, `CAU_BIEU_MAU`, lời báo 422 "Yêu cầu không hợp lệ.", `_bieu_mau_off` "Tính năng này chưa bật.", `_tra_cache` bỏ qua lượt biểu mẫu); `frontend/src/LenKeHoach.jsx` (các ô, nhãn kiểu đi, `NGAN_SACH`, ngày đi tối đa 180, lời "Tính năng này chưa bật. Bạn vẫn có thể hỏi Trợ lý Huế…") [code].
- Lượt biểu mẫu không định tuyến, không web, không công cụ: `backend/llm/assistant.py` (`answer_bieu_mau`, các chỗ `if trace.bieu_mau`), `backend/llm/len_ke_hoach.py` (docstring đầu file) [code].
- Bảng điểm: `backend/config/settings.yaml` (`lich_trinh_bang_v2` = `diem_v10.json`); đếm cột trên `data/phase_9/lich_trinh/diem_v10.json` trưa 22/11 [riêng tư; đã chạy, `python3` đếm]: 41 điểm; loại 19/10/9/7/6; thời lượng 21 ngắn / 20 nửa buổi; buổi sáng 37, chiều 37, tối 6; `gio_mo` 21; trong nhà 29/6/6; bậc thang nhiều 11; `doan_mo_ta` 18; `thoi_luong_nguon` web 31, kho 8, ước 2; `dong_cua_thu` 1, `ngay_hoat_dong` 1, `mua_luu_y` 1 (thác Nhị Hồ, tháng 9–2); giờ Đại Nội và lời "User tra 14/11/2026" ở `gio_mo_can_cu`; lịch sử bản ở trường `ghi_chu` của bảng.
- Kiểm bảng lúc bật: `backend/llm/lich_trinh_v2.py` (`nap_bang_v2` — chú thích "bài học 10/11: thiếu file ⇒ tính năng tắt im lặng"; `kiem_doan_mo_ta` — "không lặng lẽ quay về đoạn kém"; `nap_bang_anh`); `backend/api/app.py` (gọi ngoài khối bắt lỗi ⇒ máy chủ không bật) [code; bài 6].
- Bảng toạ độ 41 dòng, 1 dòng không có vị trí (`kg_le_ba_dang`): `data/phase_9/lich_trinh/diem_toa_do_v9.json` [riêng tư; đã đếm]. Bảng khoảng cách: `settings.yaml` (`khoang_cach_bang`, "40 điểm có toạ độ × 39 chiều"), trường `ghi_chu` của `khoang_cach_v1.json` (OSRM, một lần, 16/11, không tính kẹt xe) [riêng tư]. Bộ xếp không đọc bảng này: `lich_trinh_v2.py` (`_phut_di` theo cụm) [code].
- Lượt ví dụ: `data/hoc_cung_D/vi_du_lap_lich_vet.json` (`so_do.lich_khung_ms` 219,3; `generation_ms` 9.098,9; `total_ms` 9.320,3; `usd` 0,022554; token 5.592 / 1.137; `n_cited_sources` 11; `lich_v2.so_cau_du_phong` 0; `cau_gui_model`) [riêng tư; đã chạy, người viết không chạy lại].
- Luồng sự kiện, phát khung trước lời gọi model, lưu sau lượt: `backend/llm/len_ke_hoach.py` (`chuan_bi`, `stream_v2`, `luu_sau_luot` — không lưu khi `loi_khung`); `backend/api/routes/chat.py` (`luu_lich_cua_luot`, câu an toàn vào bản lưu); `backend/api/conversations.py` (`TTL_SECONDS` 30 phút, `luu_lich`, `lay_lich`) [code]. Mức suy luận thấp: `generator_openai_full_corpus.py` (`lich_v2_agent`, `BIEU_MAU_REASONING`) [code].
- Lịch ví dụ: `backend/api/routes/cong.py` (`dung_lich_mau`, `/api/lich_mau`); `frontend/src/LenKeHoach.jsx` (`LichMau`) [code].
- Dòng chỉ sang trang: `backend/llm/len_lich.py` (docstring: lý do đo 20/11, khuôn hẹp, `CAU_DAN_TRANG`); `settings.yaml` (`len_lich_dan_trang`: 17 / 20, 0 / 20, lượt trình duyệt 21/11); `bai_hoc/VIEC_MOI_XONG.md` mục 26 [code; chép].
- Xếp từ câu gõ tự do: lần 1 3 / 5 và hai lỗi: `docs/superpowers/plans/2026-11-09-phase-9-t4-lich-trinh-plan.md` mục 1; lần 2: `report_agent/2026-11-08_phase_9_ban_13/TONG_HOP.md` (T4: 21 / 27, 15 / 27, cần 26; gốc lỗi ở luật xếp / bảng điểm dùng chung; cờ `lich_trinh` tắt); `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng 22 [chép].
- Bản đầu 24 / 24, 12 / 12 × 2, 4,25 giây: `bai_hoc/14_VIEC_DE_NHAM_THI_CODE_LAM.md` mục "Biểu mẫu Lên kế hoạch"; hàng 21 của bảng tổng [chép].
- Luật "phép tính, luật, giờ, chọn quán, chọn ảnh ⇒ code" (N2), "ô nào hiện thì phải đổi được lịch" (N1), ngoại lệ số người lớn, ngưỡng < 4 chủ dự án chốt, số ngày tối đa 5, "rút từ các lần để model tính bị âm", "hai lần trước model viết lệch khung / tự thêm giờ khi khuôn đổi": `docs/superpowers/specs/2026-11-12-len-ke-hoach-ban-2-design.md` (bảng N1–N2, dòng ô người lớn, mục 5c.5, bảng "Có cần model không", dòng 351 "User chốt cả 4 khuyến nghị") [chép]. Lễ hội 43 % ⇒ 50 %: `settings.yaml` (`len_ke_hoach_so_thich_an`).
- Nguồn "Lịch bạn đang có": `lich_trinh_v2.py` (`dong_lich_dang_co`, `DONG_TIEN_VE_CHUA_CO`, chú thích "KHÔNG in câu tả do model viết"); `assistant.py` (`_nguon_lich_dang_co`, điều kiện đường thường); `settings.yaml` (`lich_vao_hoi_thuong`: 3 kịch bản, 0 / 57, đo với model lúc đó là gpt-6-luna) [code; chép]. Tổng tiền vé do model cộng, 3 / 3: `guides/RUNBOOK_BAN_GIAO.md` mục 10.2 [chép].
- Hết hạn 30 phút thì trả lời như cuộc chưa có lịch: `guides/RUNBOOK_BAN_GIAO.md` mục 10.2 [chép]; khởi động lại giữa cuộc: bài 6 (đã thử trưa 22/11).
- Nhãn "đọc từ chương trình, chưa thử thật": các dòng của bảng "Nếu… thì sao", trừ hai dòng cuối.
- Giao diện từ 23/11 (thêm 23/11/2026, đọc main `20f998f4`): nút "Xếp lịch {n} ngày", `KIEU_DI` ba câu, `SO_CHAM` 2 / 3 / 4, nhãn ngày đi: `frontend/src/LenKeHoach.jsx` (`LenKeHoachV2`, dòng 47–48, 82, 205–210, 256) [code]; ba cột ở ≥ 1.200 px chỉ khi `.lich-v2 > .bd`, cột biểu mẫu 300 px, bản đồ `position: sticky`, `height: clamp(240px, calc(100vh - 360px), 400px)`, "Đã sửa" dừng ở `margin-right: 330px`, mỗi quán một hàng, mọi luật mới trong `@media screen`: `frontend/src/lkh.css` dòng 217–275 [code]; đường nối các điểm hai lớp (`lkh-song-nen` vẽ dần, `lkh-song-chay` nét đứt chỉ trên màn hình): `frontend/src/LichV2.jsx` `SongNgay` [code]; lời commit `22e4694f`, `6b1e4fde`, `10c30bc5` (hai lỗi có sẵn ở main: `VIEC_DANG_MO.md` khối A hàng X13 "hai điểm CÓ SẴN Ở MAIN") [chép, đã mở]. Ảnh đã mở: `data/giao_dien_2026-11-22/sau_gop_10c30bc5/L02_lich_xong_1536x695_man.png` (ba cột, biểu mẫu, thẻ lịch, bản đồ, ô ngày "mm/dd/yyyy"), `L02_lich_xong_390_man.png` (một cột, đường nối nét đứt), `L04_tro_ly_noi_1280x620_man.png` (khung nổi che mép phải cột lịch), `L04_tro_ly_noi_1536x695_man.png` (khung nổi che cột bản đồ) [riêng tư; đã mở ảnh]. So cặp: `…/so_cap/NHOM_3_lich.md` mục L02, L04, L05 (so với `e98c42f`, trước bản gộp; các điểm HỎNG-MỚI ở đó đã chữa ở `10c30bc5`) [riêng tư; đã mở].
- Bản đồ trong khung trợ lý nổi / trang Trợ lý vẫn nằm dưới lịch; lịch ví dụ không bản đồ nên cột biểu mẫu giữ bề rộng cũ: chú thích `frontend/src/lkh.css` dòng 247–250 [code, người sửa đã mở 23/11]. Khung nổi ở 1280 px che trọn cột bản đồ: biên bản `data/hoc_cung_D/kiem/dot_2311_k1_kiem.md` bài 27 hàng 7 (ảnh `L04_tro_ly_noi_1280x620_man.png`) [riêng tư; chép]. "Ghim đổi theo lệnh sửa" ở bảng "Nếu…": suy từ chương trình (cột lịch hiện lượt lịch mới nhất của cuộc), không thấy trên ảnh.
- Hai giới hạn mới: `session_prompt/HIEN_TRANG.md` mục 1 gạch "Giao diện mới…" ("1280 px: khung trợ lý nổi mở ra che mép phải cột lịch · ô ngày hiện `mm/dd/yyyy` trên ảnh chụp"); `VIEC_DANG_MO.md` khối A hàng X13 ("ĐỂ SAU cổng gộp… khung trợ lý nổi che cột bản đồ ở ≥ 1200 px"; "Không sửa: ô ngày hiện `mm/dd/yyyy` (trình duyệt chụp chạy tiếng Anh — vết của phép chụp [suy luận])") [chép]. Dòng "Nếu…" khung nổi: thấy trên ảnh, link "Mở trang đầy đủ" ở `frontend/src/App.jsx` dòng 181 [đã mở ảnh; code].

- Tự cuộn về đầu lịch, cột biểu mẫu thôi ghim (thêm trưa 23/11/2026): `git show e4c41d3e` — `frontend/src/LenKeHoach.jsx` `CotLich` (`khungRef`, `khoaTruoc`, `khoa` = `lichTurn.key` khi không `daSua`; `scrollIntoView({ block: "start" })`; `prefers-reduced-motion` ⇒ `auto`), `frontend/src/lkh.css` (bỏ `position: sticky` của `.lkh-cot .lc` + chú thích "nó cao khoảng 1.900 px… nút "Xếp lịch" chỉ với tới được ở đáy trang"; `.lkh-lich { scroll-margin-top: 96px }` "thanh ghim cao 69 px") [code]. `git show 0210487d` — `khoa` thêm điều kiện `lichTurn.lichV2` + chú thích "ở bố cục một cột (màn hẹp) trang còn quá ngắn để cuộn… 472 px" [code]. Nhãn nút "Xếp lịch {n} ngày", "Xếp lịch như ví dụ": `LenKeHoach.jsx` dòng 110, 270; nút "Sửa — điền lại biểu mẫu": `frontend/src/LichV2.jsx` dòng 221, cuộn tới biểu mẫu: `frontend/src/App.jsx` `editPlan` [code].
- Số đo vị trí cuộn: trước sửa 2 / 2, 2.282 / 3.257 px, 390 px đầu lịch ngay dưới nút: `data/playwright_mcp/luot_2311/NHAT_KY.md` hàng 10:50 và 11:03 [riêng tư; chép, đã mở]; sau bản sửa đầu 7 / 7 ở 1536 × 695, lượt sửa bằng lời đứng yên, 390 × 844 "675 px — KHÔNG đổi… đầu cột lịch ở 472 px", "chưa kiểm: bấm tay trên Chrome có màn hình": `data/thu_bedrock_2026-11-21/harness/e_cham_quan_bua_2311/CHAM_E.md` mục 2 và dòng "Chưa kiểm" [riêng tư; chép, đã mở nguồn; phiên đo, không viết code của nhánh]; người viết mở ảnh `…/e_cham_quan_bua_2311/1536_sau_xep.png` (biểu mẫu trôi theo trang, không đè cột lịch) [đã mở ảnh]. Bản sửa thứ hai (`0210487d`) vào SAU lượt chấm: phiên viết code trả lời D 12:10 23/11 "chỉ đọc code, chưa ai nhìn trên trình duyệt" (chép trong lời giao V1) [chép].
- Lịch sử sửa bài (chuyển từ dòng "Cập nhật" 23/11): 17:11 22/11 sửa theo một lượt đối chiếu độc lập; 10:26 23/11 thêm lời tả trang theo giao diện mới (ba cột, đường nối các điểm, ba kiểu đi, khung trợ lý nổi); 11:13 23/11 áp biên bản kiểm độc lập `data/hoc_cung_D/kiem/dot_2311_k1_kiem.md` bài 27 và chuyển vài đoạn chi tiết của thân bài xuống "Chi tiết để tra" [riêng tư]; trưa 23/11 thêm tự cuộn về đầu lịch và cột biểu mẫu thôi ghim, gộp câu ba bảng nhỏ của thân bài vào một dòng (chi tiết đã có ở "Chi tiết để tra").
- Bài đã qua một lượt đối chiếu độc lập (người kiểm chỉ đọc, tự chạy lại bộ xếp và phần áp lệnh), trưa 22/11/2026: `data/hoc_cung_D/kiem/bai_27_32.md` [riêng tư]; các dòng SAI / LỆCH đã áp, dòng không áp ghi ở `data/hoc_cung_D/viet/viet_27_32.md` mục "Sau lượt kiểm" [riêng tư].

- Đợt áp biên bản kiểm độc lập (12:45 23/11/2026; `data/hoc_cung_D/kiem/dot_2311_trua_k1_kiem.md` mục "Bài 27" hàng 6, 9, 12 + câu khó hiểu [riêng tư]): mức kiểm của tự cuộn — `CHAM_E.md` mục 2 đo trên nhánh `e4c41d3` (tiêu đề file "Phiên đo chấm nhánh `origin/p13-c-sau-cong` `e4c41d3`"; 1536 × 695: 7 / 7, "Tổng quan" cách mép trên 303–449 px; 390 × 844: 675 px không đổi) [riêng tư; chép, đã mở]; bản đang chạy là `0210487d` 11:44 23/11 (`khoa` thêm `lichTurn.lichV2`, áp cho mọi cỡ màn — không có điều kiện bề rộng trong `CotLich`) [code, đã mở `git show 0210487d -- frontend/src/LenKeHoach.jsx`]; tới 12:45 người áp chưa thấy lượt trình duyệt nào ghi sau 11:44 — câu này đã cũ, xem gạch "Lượt áp cuối" dưới [chép]. Câu "Màn rộng đã nhìn trên trình duyệt; màn hẹp mới đọc từ chương trình" (bản 12:19) đã thay. Câu nút "Sửa — điền lại biểu mẫu" chuyển từ thân bài xuống "Chi tiết để tra" để giữ độ dài.

- Lượt áp cuối (13:25 23/11/2026; biên bản `data/hoc_cung_D/kiem/dot_2311_trua_k2_sau_bien_ban_kiem.md` mục "Bài 27" hàng 2, 4, 5, 6, 11 [riêng tư]): lượt trình duyệt đầu tiên sau bản 11:44 — lượt Playwright MCP ngắn 12:34–12:41 23/11 trên server tạm cổng 8013 = main `b4931a6b` (`data/playwright_mcp/luot_2311_trua/NHAT_KY.md`: bước A 12:35, 1536 × 695, bấm "Xếp lịch 2 ngày" ⇒ scrollY 219, "Tổng quan" top 303; bước D 12:38, 390 × 844 ⇒ scrollY 1553, "Tổng quan" top 299; mục "Số đo › Cuộn sau khi lịch xong (+1,5 giây)") [riêng tư; đã chạy, phiên đo; người áp đã mở]; sổ việc ghi lượt này "DỞ" (phiên đo thoát đột ngột 12:43): `session_prompt/VIEC_DANG_MO.md` gạch "[12:48 23/11/2026]" [chép] — nhãn đổi 14:12 23/11/2026 thành "đã đi đủ các bước, do một agent con chạy, chưa có người thứ hai kiểm": phiên điều phối xem lại, chốt 13:5x 23/11 (lời giao V2 của phiên D; sổ ở `origin/main` `6089f8bd` vẫn ghi "DỞ") [chép]; người viết mở `NHAT_KY.md` mục "ĐÃ LÀM / CHƯA LÀM": bước A–F đều "ĐÃ LÀM" [đã mở]. Bộ chụp nhóm LICH tám cỡ 12:33–12:37 (`data/giao_dien_2026-11-22/sau_main_b4931a6b/MUC_LUC.md`) KHÔNG phải phép đo cuộn ở từng cỡ: hỏi một lần ở 1440 rồi thu khung nhìn (chữ của `MUC_LUC.md`) — người áp mở `L02_lich_xong_390_man.png` nhưng không dùng làm số đo [riêng tư]. "Trước: 675 px" ở 390: `CHAM_E.md` mục 2 [chép].

- Đợt 14:12 23/11/2026 (V2 đầu chiều; đọc cây chính `64f188fa`). Dòng Cập nhật trước: "Cập nhật 13:25, ngày 23/11/2026 · khớp hệ thống 13:25 23/11 (49 tính năng mở, 5 tắt, kho 267 bài); đã áp hai lượt kiểm · trang tự cuộn về đầu lịch, biểu mẫu thôi ghim · các ô, phép kiểm, đường đi đọc từ chương trình; bảng điểm đếm lại trưa 22/11; thời gian từ một lượt thật 21/11 (Claude Sonnet 5.5); người viết không chạy lượt nào · lần sửa trước: Nguồn.". Ô trẻ em ⇒ đầu thẻ "nhẹ nhàng": `backend/llm/lich_trinh_v2.py` `dung_lich` (khối `if ts["tre_em"] >= 1 or ts["lon_tuoi"]`, commit `048bd76d`, gộp `9c7196b2` 13:47) [code]; kể đủ ở bài 28 "Chi tiết để tra". Gợi ý trên biểu mẫu khi chọn kiểu đi khác "nhẹ nhàng" cho đoàn có trẻ em: `frontend/src/LenKeHoach.jsx` dòng 241–242 ("Có trẻ em hoặc người lớn tuổi: lịch giữ mức nhẹ nhàng, mỗi buổi một điểm.") [code; có từ trước, không đổi].

- Lượt áp biên bản (14:33 23/11/2026; `data/hoc_cung_D/kiem/dot_2311_chieu_k2_kiem.md` bài 27 hàng 4 [riêng tư]): vế "(phiên đo thoát trước khi tự kiểm lại và báo)" là suy luận ⇒ thay bằng điều sổ ghi: `session_prompt/VIEC_DANG_MO.md` dòng 27 ("ĐÃ THOÁT ĐỘT NGỘT 12:43 (không ghi sổ…)") [chép].

- **Đợt tối 23/11/2026 (bảng điểm bản 13 / 14, tối nhẹ, biểu mẫu giữ lựa chọn).** Người viết đọc cây chính `2017e5e7` (17:41), không chạy test, không chạy server. Dòng Cập nhật trước: "Cập nhật 14:33, ngày 23/11/2026 · khớp hệ thống 13:52 23/11 (50 tính năng mở, 5 tắt, kho 267 bài) · nâng nhãn lượt trình duyệt trưa 23/11; ô trẻ em trỏ sang chữ "nhẹ nhàng" ở đầu thẻ (bài 28) · các ô, phép kiểm, đường đi đọc từ chương trình; thời gian từ một lượt thật 21/11 (Claude Sonnet 5.5); người viết không chạy lượt nào · lần sửa trước: Nguồn."
  - Biểu mẫu giữ lựa chọn: `git show 179e503e -- frontend/src/LenKeHoach.jsx` (`useState(() => tuTruong(prefill ?? lichTurn?.truong))` + chú thích "Rời trang rồi quay lại…"), gộp `d1b0f52e` 17:15 [code]; giới hạn CÒN: runbook 10.2 hàng "Rời trang Lên kế hoạch rồi quay lại khi đã có lịch" [chép runbook]; thấy trên trình duyệt: `data/playwright_mcp/luot_2311_cum_toi_2/NHAT_KY.md` cảnh C9 + mục (2) điểm 6 [riêng tư; agent con, chưa có người thứ hai kiểm].
  - Bảng điểm bản 14: `settings.yaml` dòng 112 (chú thích lịch sử bản 10 ⇒ 12 ⇒ 13 ⇒ 14; bản 11 giá vé "chưa dùng"); đếm 41 dòng không phải quán / 37 ban ngày / 5 có buổi tối trên `data/phase_9/lich_trinh/diem_v14.json` bằng `python3` [riêng tư; tự đếm]. Mốc: bản 13 `56a09365` 16:38, bản 14 `5044f3e9` gộp `d589ccc0` 17:14 [code].
  - Ô trẻ em, buổi tối nhẹ từ 17:29: `toi_nhe: true`, commit bật `32a7aeb4` [code]; buổi tối của lịch ví dụ trên bảng đang chạy: người viết chạy `xep_v2` (bài 28 khối Nguồn, script `/tmp/d_v3_xl/chay.py`) [riêng tư; tự chạy hàm, không qua model].
- **Đợt đêm 23/11/2026 (cụm X: bảng điểm bản 15, kho 269 bài; X5).** Người viết đọc cây chính `07bbf67b` / `5a11e3f0`, không chạy test, không chạy server. Dòng Cập nhật trước: "Cập nhật 18:32, ngày 23/11/2026 · khớp hệ thống 17:35 23/11 (55 tính năng mở, 7 tắt, kho 267 bài) · bảng điểm thêm 4 quán cà phê (từ 16:38), đoàn có trẻ nhỏ có tối nhẹ (từ 17:29), biểu mẫu giữ lựa chọn (từ 17:15) · chưa có lượt cả bộ test sau các bản gộp từ 16:20 · thời gian từ một lượt thật 21/11 (Claude Sonnet 5.5) · lần sửa trước: Nguồn." Đếm 57 mở / 6 tắt: lệnh của lời giao [tự đếm].
  - Bảng bản 15, 47 dòng = 41 điểm + 6 mục chỉ có buổi tối; danh sách nhẹ 8 mục: `settings.yaml` dòng `lich_trinh_bang_v2` = `diem_v15.json`; người viết đếm bằng `python3` (47 dòng; 11 mục có `"toi"`: 5 trong 41 điểm — hai phố đi bộ, phố Tây, Ca Huế, cầu Trường Tiền — và 6 dòng thêm ở cuối bảng: bốn quán, `aeon_mall`, `cong_vien_song_huong`) [riêng tư; tự đếm]. Mốc 18:43: gộp `bc70bf78` (commit `7fe74669` 18:33) [code]. Bản 14 = 45 dòng: Nguồn gạch "Đợt tối" dưới [chép trong bài].
  - **X5 (bài 27 bảng "Từ dùng" 41 dòng ↔ "Cấu hình" 45 dòng):** phân xử theo cấu hình đang chạy — cả hai chỗ nay ghi bản 15, 47 dòng; "41" vẫn đúng cho số ĐIỂM THAM QUAN (cột "tên và tên khác") [tự đếm].
  - Bảng toạ độ bản 11 (46 dòng, 45 có vị trí, không có dòng AEON), bảng ảnh bản 9 (45 dòng; thiếu biển Thuận An, MoKa): `settings.yaml` dòng `lich_trinh_toa_do`, `lich_trinh_bang_anh`; đếm `diem_toa_do_v11.json`, `bang_anh_v9.json` [riêng tư; tự đếm]; kể ở bài 30. Bảng khoảng cách 40 điểm, không gồm mục buổi tối: `settings.yaml` dòng `khoang_cach_bang` ("40 điểm có toạ độ × 39 chiều"); lời commit `7fe74669` ("The two rows stay out of the place list of the distance / nearby tools") [code; chép].
  - Lịch ví dụ trên bảng bản 15, ba tối phố đi bộ / Bến Trăng / Ca Huế: `/tmp/d_dem_xl/chay.py` [người viết tự chạy hàm, không qua model].
  - Kho 269 bài: bài 7 (Nguồn) [tự đếm].
- Quét số cũ 20:46 23/11/2026: chỉ câu về mức test ở dòng Cập nhật ("chưa có lượt cả bộ test sau các bản gộp từ 16:20" ⇒ lượt 20:09); thân bài không đổi. Nguồn: `session_prompt/HIEN_TRANG.md` mục 1 và bảng `data/test_rong_2026-11-22/KET_QUA_c475f5e0.tsv` (95 file · 4 bỏ · 91 chạy · 2.307 ca đạt · một file đỏ, 1.171 giây; tự đếm 20:40–20:45 23/11/2026) [riêng tư]; số kho / tính năng của dòng Cập nhật khớp lệnh chạy 20:40 23/11/2026 (269 / 9533; 57 / 6) [đã chạy].
- **Đợt 00:44 24/11/2026 (cụm G4 + tóm cụm S; người viết đọc cây chính `origin/main` `429b2046`, không chạy server, không mở trình duyệt).**
  - Bản đồ theo ngày, tên điểm mở bài, bỏ .txt: `git show f340c859` (21:26; gộp `8702829b` 21:49 23/11) — `frontend/src/BanDoLich.jsx` (`dangDoc`: mốc `window.innerHeight * 0.4`; chỉ đổi khi `n !== truoc`; chỉ khi `getComputedStyle(goc.current).position === "sticky"`; chú thích lời chủ dự án), `frontend/src/LichV2.jsx` (`lich-ten`: `typeof m.bai_id === "string" ? <a href={baiHref(m.bai_id)}>`), `frontend/src/lkh.css` (link tên điểm; bản in `text-decoration: none`), `backend/llm/lich_trinh_v2.py` (`"bai_id"` trong mục khung, chú thích "không vào tin nhắn gửi model"); lời commit ("There was no server route for .txt — the file was built in the browser"; kiểm ở 1536x695 và 390 trên máy chủ tạm của nhánh) [code; chép]. Dòng dùng chung bài: `git show 1162249e` (21:51; gộp `0161beba` 22:00) — `bai_cua_diem` (chỉ dòng đứng trước giữ link; docstring Lê Bá Đảng ↔ phố đi bộ; "B đọc code"), lời commit "46 of 47 rows are linked" [code; chép]. Lịch ví dụ dùng `lt2.dung_lich`: `backend/api/routes/cong.py` `dung_lich_mau` [code; suy từ code]. Lời chủ dự án: `data/loi_user/2026-11-23.md` dòng 21:10 [riêng tư; chép từng chữ].
  - Bảng điểm bản 16: `backend/config/settings.yaml` dòng `lich_trinh_bang_v2` (`diem_v16.json`, chú thích "= v15 từng dòng + tên gọi tắt MỘT chữ cho ba quán cà phê tối: HANOK, MoKa, TIME") [code]; gộp `ef276a5e` 21:46 23/11 (`git show --stat`) [đã chạy lệnh git]; "lịch xếp ra không đổi": `HIEN_TRANG.md` mục 1 gạch "Buổi tối của lịch" [chép]. Bài 29 kể đủ (agent khác giữ).
  - Tóm cụm S trên trang này: khối đầu cột lịch có nút — chú thích `NutDoi` / `ThayDoi` trong `frontend/src/LichV2.jsx` ("khối đầu thẻ lịch ở cột Lên kế hoạch") [code]; nhãn "Xếp giúp mình", "Gợi ý điểm thay: …": `backend/llm/sua_lich_v2.py` `nut_them`, `nut_bo_trong`; dòng "Buổi … ngày … để trống — bạn đã bỏ điểm của buổi này.": `backend/llm/lich_trinh_v2.py` dòng 909 [code]; cột lịch chép lại đoạn câu + nút, dòng ghi chú nằm cuối thẻ Ngày 1: `data/playwright_mcp/luot_2411_muc1_lai/NHAT_KY.md` cảnh 1 [riêng tư; lượt trình duyệt 00:04 24/11, người viết đã mở]. Bài 31 kể đủ.
  - Bỏ "0,0226 USD" khỏi thân bài (số vẫn ở "Chi tiết để tra", gạch "Lượt ví dụ"); chuyển xuống "Chi tiết để tra": đoạn "Rời trang rồi quay lại…", đoạn "Bảng soạn qua nhiều bản…", câu mức kiểm của tự cuộn (đã có ở "Giới hạn đã biết"); rút gọn lời dẫn của "Nếu… thì sao". Nửa để hiểu 14.053 ⇒ 14.005. Số quyết định không đổi.
  - Dòng Cập nhật trước: "Cập nhật 20:46, ngày 23/11/2026 · mức test theo hệ thống lúc code đứng yên tối 23/11 · bản 19:51: khớp hệ thống 19:49 23/11 (57 tính năng mở, 6 tắt, kho 269 bài / 9.533 đoạn) · bảng điểm bản 15 (47 dòng, có AEON Mall và công viên ven sông, từ 18:43) · lượt cả bộ test xong 20:09 23/11: một file đỏ vì lỗi của chính phép kiểm, đã sửa (bài 38) · thời gian từ một lượt thật 21/11 (Claude Sonnet 5.5) · lần sửa trước: Nguồn."
- **Áp biên bản kiểm độc lập 01:14 24/11/2026** (`data/hoc_cung_D/kiem/dot_2411_k2_giao_dien_anh_kiem.md` mục "Bài 27" hàng 27.6 + câu khó hiểu; báo cáo `data/hoc_cung_D/viet/dot_2411_a1_ap_giao_dien_anh.md` [riêng tư]). Hai mốc của sửa lịch: hành vi hỏi lại từ commit bật `39a4bbd4` 00:17:08 24/11 (`git show --stat`: chỉ `settings.yaml` `sua_lich_hoi_truoc: false` ⇒ `true` + runbook); phần hiển thị (tin thường, không khung đỏ, không « », nút) từ gộp `2f509805` 00:13:42 24/11 (lời gộp: công tắc "still off in this commit"; commit hiển thị `9c813279` 22:14 23/11 trên nhánh), không nằm sau công tắc — lùi bằng `git revert -m 1 2f509805` (`session_prompt/HIEN_TRANG.md` mục 1 gạch "24/11 (1)") [đã chạy lệnh git; chép]. "Khối đầu cột lịch" viết lại thành "khối chữ trên cùng cột lịch". Câu mốc 40 % ở "Chi tiết để tra" viết lại theo câu khó hiểu của biên bản, đối với `frontend/src/BanDoLich.jsx` `dangDoc` (`moc = window.innerHeight * 0.4`; ngày cuối cùng có `getBoundingClientRect().top <= moc`) [code]. Chuyển xuống "Chi tiết để tra": câu "cột biểu mẫu cuộn theo trang, không còn ghim…". Dòng Cập nhật bỏ "thời gian từ một lượt thật 21/11 (Claude Sonnet 5.5)" (vẫn ở "Chi tiết để tra", gạch "Lượt ví dụ"). Nửa để hiểu 14.005 ⇒ 13.996 ký tự. Dòng Cập nhật trước: "Cập nhật 00:44, ngày 24/11/2026 · khớp hệ thống 00:30 24/11 (58 tính năng mở, 6 tắt, kho 269 bài / 9.533 đoạn, bảng điểm bản 16) · bản đồ lịch theo ngày đang đọc, tên điểm bấm mở bài, bỏ nút tải .txt (từ 21:49 23/11); sửa lịch hỏi lại bằng nút thấy trên trang này (tóm; bài 31 kể đủ) · lượt cả bộ test gần nhất 20:09 23/11, TRƯỚC các bản gộp này · thời gian từ một lượt thật 21/11 (Claude Sonnet 5.5) · lần sửa trước: Nguồn."
- **Áp biên bản kiểm độc lập của đợt gom 24/11/2026** (`data/hoc_cung_D/kiem/dot_2411_k3_gom_ABDEF_00.md` [riêng tư], mục "Bài gốc trái code" 1; 06:35 24/11): câu vạch 40 % ở "Chi tiết để tra" gạch "Bản đồ theo ngày đang đọc" — "nằm trong 40 %" thành "đã lên tới vạch 40 % … hoặc cao hơn, kể cả đã cuộn khuất", đối với `frontend/src/BanDoLich.jsx` dòng 37–50 (`moc = window.innerHeight * 0.4`; lấy ngày CUỐI CÙNG có `getBoundingClientRect().top <= moc`, mép trên âm khi đã cuộn khuất vẫn tính) [code]; dòng Cập nhật: cụm lượt cả bộ test 20:09 23/11 thay bằng lượt xong 01:00 24/11 (bài 38 dòng 11). Các câu áp sau biên bản chưa có người thứ hai đọc.
- **Đợt "sửa lịch sau 00:17 24/11" (phần bài 27; đọc cây chính `fdadd3de`, 08:40 24/11; không chạy test, không gọi model, không bật server).** Dòng Cập nhật trước: "Cập nhật 00:44, ngày 24/11/2026 · khớp hệ thống 00:30 24/11 (58 tính năng mở, 6 tắt, kho 269 bài / 9.533 đoạn, bảng điểm bản 16) · bản đồ theo ngày đang đọc, tên điểm mở bài, bỏ nút .txt (từ 21:49 23/11); sửa lịch hỏi lại bằng nút (tóm) · lượt cả bộ test gần nhất xong 01:00 24/11 trên đúng bản code này: 96 file, 4 bỏ vì cần khoá OpenAI, 92 chạy, 2.325 ca đạt, không file nào đỏ (bài 38) · lần sửa trước: Nguồn · đã áp biên bản kiểm độc lập 01:14 24/11 · 06:35 24/11: áp biên bản kiểm độc lập của đợt gom (cụm lượt cả bộ test, câu vạch 40 % của bản đồ)." [chép]. Đoạn "Sửa bằng lời thấy gì trên trang này" trước đợt: cùng ý đến nút "Gợi ý điểm thay" và dòng buổi để trống, cộng câu về hiển thị "chưa làm" [tả bằng lời; bản cũ ở `/tmp/d_s28b/27_dong74_cu.txt`].
  - Nhãn nút: `backend/llm/sua_lich_v2.py` các dòng dựng nút (`"Đặt {x} trước {…}"`, `"Dời sang buổi … ngày …"` + `" (đổi chỗ với …)"`, `"Dời {x} sang buổi … ngày … (đổi chỗ với …)"`, `nut_bo_trong`) [code]. Bản gộp: `2d29fbc4` (chèn trước), `bcbadb86` (nút dời), `336a2623` (08:19, ngày để trống), `fdadd3de` (08:40, dời hỏi trước) [đã chạy lệnh git cho `336a2623`; ba mã kia chép lời giao đợt, chưa `git log` từng mã]. Khối đầu cột: `frontend/src/LenKeHoach.jsx` dòng 144–145 [code]; cùng nút như khung trợ lý: `frontend/src/LichV2.jsx` `ThayDoi` / `NutDoi` [code].
  - Ngày trống trên trang: `lich_trinh_v2.py` `dung_lich` (mã `ngay_trong`), `LichV2.jsx` `NgayLich` (chỉ vẽ mục `tham_quan` / `hoat_dong_toi`; ghi chú theo ngày là phần tử cuối), `quan_lich.py` `an_uong` (không có bữa trưa khi ngày không còn điểm) [code]. Lượt trình duyệt của phiên viết code 07:56–07:59 24/11: `data/thu_bedrock_2026-11-21/harness/c_luot_that_abc_2411/trinh_duyet_ra.txt` (dòng báo, chữ thẻ ngày 2, "ghim bản đồ: 4", "lỗi console / trang: 0") và ảnh `e1_ke_hoach_ngay_trong_1536.png` (người viết mở xem) [riêng tư; chép, đã xem ảnh; một lượt do công cụ lái, một người chạy]. Ngày đi xa: `/tmp/d_s28b/ngay_trong_ra.txt` (08:45 24/11) [đã chạy, người viết].
  - Đếm tính năng 08:45 24/11 (lệnh `guides/RUNBOOK_BAN_GIAO.md` mục 0): 59 mở, 6 tắt [tự đếm]. Độ dài nửa để hiểu 14.186 ⇒ 14.184 (nhãn ba nút mới chuyển xuống "Chi tiết để tra").
- **Đợt 5 — Phần A (28/11/2026):** đồng bộ mốc **70 mở / 8 tắt**, `9.540` đoạn và `gpt-6-luna`; cập nhật các nút quanh thẻ lịch (`frontend/src/LichV2.jsx`, `frontend/src/ChoO.jsx`), đường gọi xuất mới (`backend/api/routes/xuat.py`), và xoá `slide_cache` khi đổi / hoàn tác lịch trong `backend/api/conversations.py` (chi tiết ở bài 30).
- **Đợt 6 (28/11/2026):** đồng bộ **71 mở / 9 tắt** (`goi_y_luu_tru: true`), tách **2 nút PowerPoint Nhanh / AI** ở `frontend/src/LichV2.jsx` theo `slide_designer_ai` từ `GET /api/tinh_nang` (`cong.py`, `App.jsx`), tái sử dụng bảng 136 cơ sở & 3 link sàn cho ô chat (`goi_y_luu_tru.py`), kiểm Playwright 2 khổ `1536×695` & `390×844` sạch `0` lỗi (`data/thu_dot6_2026-11-28/KET_LUAN_DOT6.md`).
</details>
