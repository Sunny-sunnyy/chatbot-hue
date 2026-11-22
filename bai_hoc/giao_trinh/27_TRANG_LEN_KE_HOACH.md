# Bài 27 — Trang Lên kế hoạch: từ mấy nút chọn tới một lịch, và bảng điểm tham quan đứng sau

*Cập nhật 17:11, ngày 22/11/2026 · đã sửa theo một lượt đối chiếu độc lập · các ô, phép kiểm và đường đi của một lượt đọc từ chương trình và cấu hình trưa 22/11; số của bảng điểm đếm lại từ bảng đang chạy trưa 22/11; thời gian lấy từ một lượt lập lịch thật ngày 21/11 (Claude Sonnet 5.5); người viết không chạy lại lượt nào.*

**Bài trước đã biết:** trợ lý trả lời câu hỏi từ kho; việc phải đúng (ngày âm lịch, thời tiết, khoảng cách) do chương trình tính (bài 24). Bài 5 đã tả trang Lên kế hoạch trông ra sao.
**Bài này thêm:** người dùng bấm "Xếp lịch" thì máy chủ nhận gì, kiểm gì, và đi qua những bước nào cho tới khi có một lịch. Bài cũng mở bảng điểm tham quan, thứ mà mọi lịch được xếp từ đó, và nói ô chat liên quan tới trang này ra sao.

## Ý chính

- Người dùng chọn bằng nút, không gõ câu. Máy chủ nhận **tám giá trị** và kiểm lại từng giá trị; sai một giá trị thì cả yêu cầu bị từ chối.
- Mọi lịch được xếp từ **một bảng 41 điểm tham quan**, không xếp thẳng từ kho. Mỗi ô của bảng (thời lượng, giờ mở cửa…) có ghi căn cứ: từ kho, từ web, hay ước.
- Một lượt lập lịch có **một lần gọi model**, chỉ để viết câu mô tả. Việc chọn điểm, chia ngày, tính giờ là của chương trình. Ở ví dụ: khung lịch hiện sau 0,2 giây, đủ câu mô tả sau 9,3 giây.
- Gõ "lên lịch giúp mình 2 ngày" trong ô chat thì **không** ra một lịch: trợ lý trả lời bằng chữ từ kho, kèm một dòng chỉ sang trang này. Xếp lịch từ câu gõ tự do đã thử hai lần, không đạt, đang tắt.
- Đã có lịch thì câu hỏi tiếp trong ô chat được trả lời trên **đúng lịch đó**: chương trình in lịch và số giờ thành một nguồn cho model đọc.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| biểu mẫu | **form** | nhóm ô và nút để người dùng chọn giá trị rồi gửi một lần |
| kiểm khuôn | **validation**, **schema** | máy chủ đối chiếu mỗi giá trị gửi lên với một danh sách giá trị được phép; lạ là từ chối |
| bảng điểm tham quan | **itinerary table** | 41 dòng, mỗi dòng một điểm, với các cột dùng để xếp lịch; nằm ngoài kho bài viết |
| cụm | **cluster** | nhóm các điểm nằm cùng một khu (ví dụ Kinh thành, bờ nam sông Hương, khu lăng Thủy Xuân); có 8 cụm |
| khung lịch | **itinerary frame** | phần lịch do chương trình dựng: ngày, buổi, tên điểm, giờ, ghi chú; chưa có câu mô tả |
| lịch đã lưu | **saved itinerary** | bản khung lịch mới nhất của một cuộc trò chuyện, máy chủ giữ trong bộ nhớ để sửa và hỏi tiếp |

## Người dùng chọn tám ô, máy chủ kiểm lại cả tám

Biểu mẫu có bốn nhóm (ai đi, đi bao lâu và khi nào, đi kiểu nào, thích gì) và một ô hạng sao chỗ ở. Chỉ số ngày là bắt buộc.

| Ô | Giá trị được phép | Làm đổi lịch thế nào |
|---|---|---|
| Số ngày | 1 tới 5 | số ngày của lịch |
| Người lớn | 1 tới 10 | **không** làm đổi lịch; chỉ hiện ở dòng "Mình hiểu…" |
| Trẻ em | 0 tới 6 | có trẻ em ⇒ lịch nhẹ: mỗi buổi một điểm, không buổi tối, tránh điểm nhiều bậc thang |
| Có người lớn tuổi | có / không | như trẻ em |
| Kiểu đi | nhẹ nhàng · cân bằng · khám phá nhiều | số điểm mỗi buổi (bài 28) |
| Sở thích | tối đa 2 trong 5 loại | điểm nào được xét trước |
| Ngày đi | từ hôm nay tới 180 ngày sau; được bỏ trống | thứ trong tuần, mùa, dự báo mưa |
| Hạng chỗ ở | 1 sao · 2–3 sao · 4–5 sao; được bỏ trống | chỉ đổi khối "Nơi ở" (bài 30) |

Bấm "Xếp lịch", trang gửi lên máy chủ đúng các giá trị đã chọn, kèm một ghi chú cho máy chủ biết đây là yêu cầu từ biểu mẫu. Máy chủ kiểm lại: các ô số người phải là số thật (không nhận chữ "2" thay cho số 2), số ngày chỉ nhận đúng một trong năm giá trị 1–5, không nhận ô lạ, sở thích không trùng nhau và không quá hai, ngày đi đúng dạng năm-tháng-ngày và nằm trong 180 ngày tính theo ngày Việt Nam, sở thích gửi lên phải là loại đang hiện trên biểu mẫu. Sai một chỗ thì cả yêu cầu bị từ chối với lời báo "Yêu cầu không hợp lệ." và không có lịch nào được xếp.

Qua bước kiểm, máy chủ ghép các giá trị thành một câu cố định cho lịch sử cuộc trò chuyện, ở ví dụ là *"Lên kế hoạch tham quan Huế (Thông tin thêm: 3 ngày; 2 người lớn; đi cân bằng; thích di tích.)"*. Lượt biểu mẫu đi đường riêng: không qua bước xếp loại câu (bài 22), không tra web, không đưa công cụ nào cho model, không dùng câu trả lời đã nhớ.

## Bảng điểm tham quan: 41 dòng, mỗi ô có căn cứ

Lịch không xếp thẳng từ 267 bài của kho: bài viết là văn xuôi, còn xếp lịch cần con số và nhãn đặt sẵn. Mỗi dòng có tên và tên khác, cụm, loại điểm, thời lượng ("ngắn" 75 phút hoặc "nửa buổi" 150 phút), buổi đi được, giờ mở cửa (21 điểm có khung giờ; 20 điểm kho không ghi giờ thì không ràng buộc), trong nhà hay ngoài trời (29 điểm ngoài trời), có nhiều bậc thang không (11 điểm), thứ tự ưu tiên theo từng sở thích, thứ và mùa hoạt động, giờ của hoạt động buổi tối, và bài nguồn trong kho. 18 điểm có thêm một đoạn kho được chọn tay để model tả. Bảng đủ các cột ở nửa để tra.

Hầu như mọi ô có thêm một dòng **căn cứ**: câu trích từ bài kho, trang web, hoặc ghi là ước. Ví dụ giờ 7:00 – 17:00 của Đại Nội là phần chung của giờ mùa hè và mùa đông, chủ dự án tra ngày 14/11. Thời lượng là cột dựa vào web nhiều nhất: 31 điểm lấy từ web, 8 từ kho, 2 điểm ước.

Bảng do các phiên làm việc soạn qua nhiều bản (34 điểm ngày 13/11; chủ dự án chọn thêm 7 nơi ngày 15/11). Các điểm ưu tiên và các ca khó (thác Nhị Hồ bỏ khỏi lịch những tháng nào, giờ của Đại Nội) do chủ dự án chốt.

Bảng được kiểm lúc bật máy chủ (quyết định 4).

Cạnh bảng điểm có ba bảng nhỏ hơn, cũng nằm ngoài kho: bảng toạ độ và bảng ảnh (40 trên 41 điểm, bài 30), và bảng khoảng cách giữa 40 điểm, dựng một lần ngày 16/11 bằng một dịch vụ chỉ đường. Trợ lý dùng bảng khoảng cách khi được hỏi "từ A sang B bao xa" (bài 24); bộ xếp lịch **không** dùng nó mà ước phút đi theo cụm (bài 28).

## Một lượt lập lịch thật: năm bước, khung lịch tới trước

Ví dụ lập lịch của cả bộ, lượt thật ngày 21/11/2026: 3 ngày, 2 người lớn, cân bằng, thích di tích, không chọn ngày đi.


| Bước | Ai làm | Ở ví dụ |
|---|---|---|
| 1. Kiểm tám giá trị | máy chủ | đạt |
| 2. Xếp | chương trình, từ bảng điểm | 8 điểm ban ngày, 3 hoạt động tối (bài 28) |
| 3. Lấy nguồn | chương trình, mỗi điểm một đoạn của chính bài về điểm đó | 11 đoạn |
| 4. Gửi khung lịch | máy chủ gửi tên, buổi, giờ, ảnh, ghi chú, quán; giao diện vẽ ngay | 0,22 giây |
| 5. Viết câu mô tả | model, một lần gọi, không công cụ; chương trình kiểm từng câu (bài 29) | 9,1 giây; 0 câu bị thay |

Cả lượt 9,3 giây, 0,0226 USD. Lúc câu mô tả chưa tới, mỗi điểm hiện hai vạch xám chờ chữ. Có ngày đi trong 7 ngày tới thì bước 2 lấy thêm dự báo thời tiết một lần.

Xong lượt, máy chủ lưu lịch vào cuộc trò chuyện, để sửa bằng lời (bài 31), tải PowerPoint (bài 30) và trả lời câu hỏi tiếp. Bản lưu nằm trong bộ nhớ của máy chủ, hết hạn sau 30 phút không nhắn, mất khi khởi động lại máy chủ (bài 6). Lịch trượt bước kiểm khung vẫn hiện nhưng không được lưu (bài 29).

## Ô chat không tự lập lịch: chỉ đường, và đọc lịch đã lưu

Có ba tình huống ô chat chạm tới lịch.

**Gõ "lên lịch giúp mình 2 ngày ở Huế".** Trợ lý trả lời như câu hỏi thường, từ kho. Dưới câu trả lời, chương trình nối một dòng: "Muốn lịch có giờ từng điểm, bản đồ và sửa được bằng lời, bạn mở trang Lên kế hoạch." Bấm cụm "trang Lên kế hoạch" là sang trang có biểu mẫu. Câu được nhận ra bằng một khuôn chữ hẹp: lời nhờ, chữ "lịch / lịch trình / kế hoạch", và số ngày; không nêu số ngày thì không có dòng.

**Xếp lịch thật từ câu gõ tự do** đã thử hai lần (05/11 và 09/11) và đang tắt: model đọc câu rồi gọi một công cụ xếp lịch của chương trình. Lần hai, 27 trên 27 câu ra lịch, nhưng lịch hợp người đi cùng chỉ 21 và 15 trên 27 theo hai người chấm, dưới sàn 26 (bảng ở nửa để tra). Bộ xếp hiện nay (bài 28) có từ 14/11 và chỉ chạy qua biểu mẫu.

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
- **Cái giá:** lịch chỉ hay bằng luật và bảng. Điểm ngoài 41 dòng không bao giờ được xếp; luật thiếu một tình huống thì lịch sai lặp lại được (bài 28).

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

Lời báo trong ngoặc kép là nguyên văn trong chương trình. Các dòng đều đọc từ chương trình, chưa thử thật, trừ dòng cuối (đã thử trưa 22/11, bài 6).

| Nếu | Hệ thống làm gì | Người dùng thấy gì | Muốn hết thì ai làm gì |
|---|---|---|---|
| một giá trị sai khuôn (ngày đi quá 180 ngày, sở thích đang ẩn) | từ chối cả yêu cầu | "Yêu cầu không hợp lệ." | người dùng chọn lại |
| trang Lên kế hoạch đang tắt | giao diện ẩn mục này | mở thẳng địa chỉ trang: "Tính năng này chưa bật." | người vận hành bật lại |
| bảng điểm sai, hoặc đoạn mô tả không còn trong chỉ mục | máy chủ không bật | không vào được trang nào | người vận hành sửa bảng hoặc chỉ mục |
| hỏi tiếp sau hơn 30 phút không nhắn | lịch đã hết hạn | câu trả lời không dựa trên lịch, không lời báo | xếp lại lịch; chưa có lời báo |
| máy chủ khởi động lại giữa cuộc **(đã thử)** | mất lịch đã lưu | thẻ lịch vẫn hiện; lệnh sửa bị coi như câu hỏi thường | tải lại trang, xếp lại |

## Dễ nhầm

- **"Lịch được xếp từ kho 267 bài."** Không. Lịch xếp từ bảng 41 điểm; kho chỉ cho mỗi điểm một đoạn để model tả.
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
| `lich_trinh_bang_v2` | bảng điểm bản 10, 41 điểm | thiếu file hay thiếu cột ⇒ máy chủ không bật | bản 34 điểm tới 15/11 |
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
| buổi hợp | sáng, chiều | 37 điểm đi được ban ngày; 6 điểm có hoạt động buổi tối |
| giờ mở cửa | 7:00 – 17:00 | 21 điểm có khung giờ; 20 điểm kho không ghi giờ ⇒ không ràng buộc |
| trong nhà hay ngoài trời | ngoài trời | 29 ngoài trời, 6 trong nhà, 6 cả hai |
| nhiều bậc thang | không | 11 điểm |
| ưu tiên theo sở thích | số 1 của "di tích" và của "chung" | mỗi sở thích 3–4 điểm ưu tiên |
| thứ, mùa | — | 1 điểm đóng cửa một ngày trong tuần, 1 điểm chỉ mở vài tối, 1 điểm tạm dừng theo mùa (thác Nhị Hồ, tháng 9 tới tháng 2) |
| đoạn mô tả chọn tay | — | 18 điểm có một đoạn kho được chọn sẵn để model tả |
| bài nguồn trong kho | bài Đại Nội Huế | mọi điểm |

## Giới hạn đã biết

- Bảng chỉ 41 điểm. Điểm ngoài bảng không bao giờ vào lịch, dù kho có bài.
- Thời lượng của 31 điểm dựa vào web, 2 điểm là ước; sai thì giờ gợi ý sai theo.
- Ô số người lớn chưa làm đổi lịch.
- Chưa có ô giờ tới, giờ về: ngày đầu và ngày cuối vẫn xếp đủ buổi.
- Lịch đã lưu mất sau 30 phút không nhắn hoặc khi máy chủ khởi động lại; người dùng không được báo.
- Hỏi tổng tiền vé của lịch: model tự cộng giá vé từ kho trên đúng lịch (lượt thật 19/11: đúng 3 / 3), không phải số chương trình tính.

## Chi tiết để tra

- Lượt ví dụ (21/11/2026, Claude Sonnet 5.5): khung lịch 219 ms; lời gọi viết câu 9.096 ms; cả lượt 9.320 ms; 5.592 token vào, 1.137 token ra, 0 token suy luận; 0,022554 USD; 11 nguồn được trích; 0 câu dự phòng; không có dự báo (không chọn ngày đi). Lịch: ngày 1 Đại Nội (sáng), chùa Thiên Mụ và Kinh thành (chiều), chợ Đông Ba (tối); ngày 2 lăng Tự Đức, lăng Khải Định, phố đi bộ Nguyễn Đình Chiểu; ngày 3 phố cổ Bao Vinh, Quốc Học, cung An Định, phố Tây.
- Trên đường gửi dần, lượt biểu mẫu có các tin: trạng thái "đang xếp", khung lịch, từng câu mô tả, "lịch xong", rồi chữ thuần của cả lịch (dùng cho lịch sử và nút sao chép).
- Lượt biểu mẫu, lượt sửa lịch và việc nạp lịch đã lưu chỉ chạy trên đường gửi dần (đường giao diện dùng); đường trả cả câu một lần không nạp lịch đã lưu. Vì sao: chưa thấy ghi lý do. Điều thấy được: giao diện chỉ dùng đường gửi dần.
- Khi chưa xếp lịch nào, trang hiện một lịch **ví dụ** 2 ngày do chính bộ xếp dựng từ một tổ hợp cố định; câu mỗi điểm của lịch ví dụ do chương trình viết, không gọi model.
- Lịch đã lưu không ghi ra đĩa; câu an toàn bão lũ (nếu lượt đó có) được giữ cùng bản lưu để file tải về còn câu đó.
- Bảng điểm qua các bản: bản 8 (13/11, 34 điểm), bản 9 (15/11, thêm 7 điểm: chùa Từ Hiếu, cầu Trường Tiền, đèo Hải Vân, chợ Bến Ngự, làng nón Tây Hồ, nhà vườn An Hiên, đầm Lập An), bản 10 (17/11, giờ tối chợ Đông Ba 18:00 – 23:00). Ba nơi khác bị loại khi thêm vì thiếu căn cứ.
- Bảng khoảng cách: 40 điểm × 39 chiều; km và phút theo đường ô tô, không tính kẹt xe; lúc trả lời không gọi mạng.

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
- Nhãn "đọc từ chương trình, chưa thử thật": các dòng của bảng "Nếu… thì sao", trừ dòng cuối.

- Bài đã qua một lượt đối chiếu độc lập (người kiểm chỉ đọc, tự chạy lại bộ xếp và phần áp lệnh), trưa 22/11/2026: `data/hoc_cung_D/kiem/bai_27_32.md` [riêng tư]; các dòng SAI / LỆCH đã áp, dòng không áp ghi ở `data/hoc_cung_D/viet/viet_27_32.md` mục "Sau lượt kiểm" [riêng tư].

</details>
