# Bài 5 — Người dùng thấy gì: các trang của ứng dụng

*Cập nhật 14:13, ngày 22/11/2026 · danh sách trang, chữ trên màn hình và thứ tự các phần đọc từ chương trình giao diện sáng 22/11 (gồm lần chạy lại thêm lúc 10:50 22/11); số đo giao diện lấy từ các lần đo 14–16/11; người viết không mở ứng dụng trên trình duyệt trong buổi viết này, nên câu nào tả "lúc nào thấy gì" là đọc từ chương trình.*

**Bài trước đã biết:** sản phẩm làm ba loại việc: hỏi đáp có nguồn, việc cần tính, và lên kế hoạch.
**Bài này thêm:** ba loại việc đó nằm ở đâu trên màn hình. Đi một vòng qua các trang, rồi nhìn một lượt hỏi và một lượt lập lịch diễn ra thế nào trước mắt người dùng. Cuối nửa đầu là hai mục mới: vì sao giao diện được làm như vậy, và khi có thứ hỏng thì người dùng thấy gì.

## Ý chính

- Ứng dụng là một **trang web nhiều trang**, không chỉ là một khung chat. Thanh điều hướng có sáu mục: Trang chủ, Khám phá, Bản đồ, Lên kế hoạch, Trợ lý Huế, Giới thiệu. Ở mọi trang còn có một nút tròn "Trợ lý Huế" mở khung trò chuyện ngay tại chỗ.
- Lý do làm nhiều trang: nếu chỉ có một khung chat, người dùng không biết hệ thống làm được gì cho tới khi gõ đúng câu.
- **Trợ lý Huế** là nơi hỏi đáp. Trong lúc chờ có một dòng trạng thái; dưới câu trả lời có dòng "Nguồn:" bấm vào xem được đoạn gốc.
- **Lên kế hoạch** là nơi bấm nút để có một lịch, xem bản đồ, tải về. Muốn sửa lịch bằng lời thì nhắn ở khung Trợ lý Huế; lịch trên trang đổi theo.
- **Khám phá** cho đọc thẳng các bài của kho; chữ trên mỗi thẻ bài lấy từ chính bài đó.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| trình duyệt | **browser** | chương trình trên máy của người dùng để mở trang web (Chrome, Safari…) |
| giao diện | **frontend**, **UI** | phần của ứng dụng chạy trong trình duyệt của người dùng: các trang, nút bấm, ô gõ |
| máy chủ | **backend**, **server** | chương trình chạy trên máy của dự án; nhận yêu cầu từ giao diện, tìm trong kho, gọi model, gửi kết quả về (bài 6) |
| thanh điều hướng | **navigation bar** | hàng mục ở đầu trang để chuyển giữa các trang |
| dòng trạng thái | **status line** | dòng chữ nhỏ báo hệ thống đang làm gì ("Đang hiểu câu hỏi…") |
| tính năng đang mở | **feature flag** | một dòng trong cấu hình của máy chủ, ghi một tính năng đang được dùng hay đang tắt |

## Sáu mục trên thanh điều hướng

| Trang | Người dùng làm gì ở đó |
|---|---|
| **Trang chủ** | thấy một ô hỏi lớn (gõ rồi gửi là khung Trợ lý mở ra và trả lời), vài câu gợi ý bấm được, ô thời tiết nhỏ, và năm chủ đề của kho |
| **Khám phá** | chọn một chủ đề, xem danh sách bài dạng thẻ có ảnh, mở một bài để đọc; ở mỗi bài có nút "Hỏi trợ lý về điểm này" (điền sẵn một câu hỏi vào ô, người dùng tự bấm gửi) và nút "Báo thông tin chưa đúng" |
| **Bản đồ** | xem các điểm tham quan trên một bản đồ, lọc theo loại |
| **Lên kế hoạch** | chọn bằng nút: số ngày, số người lớn, trẻ em, có người lớn tuổi không, kiểu đi, sở thích, ngày đi, hạng sao của chỗ ở; nhận một lịch theo buổi; tải về. Khi chưa xếp lịch nào, trang có sẵn một lịch ví dụ |
| **Trợ lý Huế** | gõ câu hỏi, hoặc gửi một tấm ảnh (hệ thống đoán tên nơi hoặc món trong ảnh: đoán ra một tên thì hỏi luôn, kèm dòng báo là có thể đoán sai; đoán ra hai ba tên thì người dùng bấm chọn; bài 26); đọc câu trả lời, nguồn, và mục "Từ web (chưa kiểm)" nếu có |
| **Giới thiệu** | đọc hệ thống làm được gì, giới hạn ở đâu, dữ liệu của người dùng được giữ thế nào; xem phần "Huế qua các thời kỳ": sáu mốc lịch sử kể bằng chữ viết lại từ các bài của kho, kèm ảnh |

Trên điện thoại, thanh ở cuối màn hình có năm mục; mục Giới thiệu vào từ chân trang.

Ngoài sáu mục này có hai trang không nằm trên thanh điều hướng: trang **Chỗ ở** (mở từ đường link dưới một lịch đã lập), và một trang **theo dõi** dành riêng cho chủ dự án, phải có khoá mới mở được.

Mục Bản đồ và mục Lên kế hoạch chỉ có khi tính năng tương ứng đang mở ở máy chủ. Lúc tải trang, giao diện vẽ thanh điều hướng ngay, đồng thời hỏi máy chủ "những tính năng nào đang mở"; có trả lời thì các mục đang mở được thêm vào.

## Một lượt hỏi trên trang Trợ lý

Người dùng gõ *"Giá vé tham quan Đại Nội Huế là bao nhiêu?"* rồi gửi. Trên màn hình lần lượt có:

1. **Một dòng trạng thái**, đổi dần: "Đang hiểu câu hỏi…", rồi "Đã tìm trong kho, đang chuẩn bị câu trả lời… (10 đoạn)".
2. **Câu trả lời.** Với model đang chạy (Claude Sonnet 5.5), chữ hiện ra một lần khi model viết xong. Với model dùng trước đó (gpt-6-luna), chữ hiện dần trong lúc model viết.
3. **Ảnh**, chỉ khi câu trả lời nói về một nơi hoặc một món có ảnh chắc là đúng. Lượt ví dụ này trích ba bài khác nhau nên không có ảnh.
4. **Dòng "Nguồn:"** ghi tên các bài đã được trích. Bấm vào một tên thì mở ra đoạn gốc của bài đó. Các số [n] mà model viết trong câu trả lời không hiện ra; giao diện bỏ chúng và chỉ giữ dòng nguồn.
5. **Dòng ghi chú**, nếu có: ở lượt này là "Giờ mở cửa, giá vé, lịch lễ hội có thể đã thay đổi — hãy kiểm lại với nơi đến trước khi đi."

Khi kho không có câu trả lời cho cả câu hỏi, và việc tra web có kết quả, phần chữ là một câu dẫn sang mục **"Từ web (chưa kiểm)"** ngay bên dưới, có danh sách trang web làm căn cứ (bài 25). Tra web không ra gì thì người dùng thấy câu từ chối kèm gợi ý cách hỏi.

Trong lúc chờ có nút **Dừng**. Tải lại trang là bắt đầu một cuộc trò chuyện mới; cũng có nút "Cuộc trò chuyện mới".

## Một lượt lập lịch trên trang Lên kế hoạch

Ví dụ lập lịch của cả bộ: người dùng chọn 3 ngày, 2 người lớn, đi kiểu cân bằng, sở thích di tích, rồi bấm xếp lịch. Sau khoảng 0,2 giây khung lịch đã hiện: ba ngày, mỗi ngày chia sáng, chiều, tối, các điểm đã có tên và giờ. Ở mỗi điểm lúc đó có một vạch "đang viết…"; khoảng 9 giây sau thì đủ câu mô tả cho mọi điểm. Ngày 1 của lịch thật đó: sáng Đại Nội (8:00 – 10:30), chiều chùa Thiên Mụ rồi Kinh thành, tối chợ Đông Ba.

Mỗi điểm có giờ và một câu mô tả lấy từ kho và ảnh (40 trên 41 điểm có ảnh). Trong từng ngày có gợi ý quán cho bữa trưa và bữa tối. Dưới lịch có một dòng "Nguồn:" chung, bản đồ ghim các điểm theo thứ tự, ô chỗ ở, và các nút để sao chép, tải về, in, tải PowerPoint (đủ ở mục "Chi tiết để tra").

Muốn sửa, người dùng nhắn ở khung Trợ lý Huế, ví dụ "đổi chỗ ngày 1 với ngày 2". Lịch trên trang đổi theo, hoặc hệ thống nói vì sao không đổi được (bài 31).

## Quyết định và lý do

### 1. Vì sao làm một trang web nhiều trang, mà không chỉ làm một khung chat?

- **Đã chọn:** sáu trang, trong đó khung chat là một, cộng một nút mở khung chat ở mọi trang.
- **Vì sao:** quyết định đã ghi lúc thiết kế giao diện (chủ dự án chọn hướng "trang du lịch nhiều mục" ngày 06/11). Đề tài là ứng dụng hỗ trợ trải nghiệm; chỉ có khung chat thì người dùng không biết hệ thống có lên lịch, có thời tiết, có hỏi bằng ảnh cho tới khi gõ đúng câu.
- **Cách khác:** chỉ một khung chat: bản đầu tiên của hệ thống làm vậy; đã bỏ.
- **Cái giá:** nhiều màn hình phải làm và giữ cho đúng; trang Bản đồ và Lên kế hoạch cần thêm bảng dữ liệu riêng (bài 27).

### 2. Vì sao việc nào làm ngay trong trình duyệt, việc nào phải gửi về máy chủ?

- **Đã chọn:** việc chỉ đổi cách hiện thứ trình duyệt đã có thì làm tại trình duyệt, ví dụ ô tìm của trang Khám phá, bỏ số [n] khỏi chữ, dựng file lịch để tải về. Việc nào quyết câu trả lời nói gì, có đúng nguồn không, lịch có hợp lệ không thì làm ở máy chủ: tìm trong kho, gọi model, kiểm số nguồn, xếp lịch, kiểm các ô của biểu mẫu.
- **Vì sao:** lập luận, không phải số đo. Thứ chạy trong trình duyệt thì người dùng sửa được; luật đặt ở đó là luật ai cũng tắt được. Việc chỉ đổi cách hiện thì không cần model, không cần khoá bí mật, và thấy kết quả ngay.
- **Cách khác:** đưa mọi việc về máy chủ, kể cả việc chỉ đổi cách hiện: chưa thử.
- **Cái giá:** vài giới hạn phải viết hai lần. Ví dụ câu hỏi dài nhất 500 ký tự: giao diện chặn để người dùng thấy ngay, và máy chủ chặn lại lần nữa vì không thể tin giao diện.

### 3. Vì sao khi lỗi giữa chừng hay bấm Dừng, chữ đã hiện bị xoá hết, không giữ nửa câu?

- **Đã chọn:** bước kiểm số nguồn ở cuối hỏng thì rút lại chữ đã hiện; lỗi hay đứt kết nối giữa chừng thì xoá hết; cả hai thay bằng một lời báo và nút "Thử lại". Bấm "Dừng" cũng xoá chữ đã hiện.
- **Vì sao:** chủ dự án chọn ngày 31/10, khi thiết kế phần chữ hiện dần. Lý do ghi trong chương trình: chữ đã hiện chưa qua bước kiểm số nguồn (bài 16).
- **Cách khác:** không hiện chữ nào trước khi kiểm xong: đã ghi là cách quay về nếu số lần rút lại vượt 1 % số câu mỗi tuần dùng thật; chưa dùng.
- **Cái giá:** người dùng mất phần đã đọc, phải hỏi lại.

### 4. Vì sao với model đang chạy, chữ hiện một lần mà không hiện dần?

- **Đã chọn:** với Claude Sonnet 5.5 qua Amazon Bedrock, máy chủ gọi model trọn một lần rồi gửi cả câu trả lời về giao diện một lần.
- **Vì sao:** tài khoản AWS đang dùng chưa có quyền gọi model theo kiểu trả chữ dần. Ngày 22/11 chủ dự án gác mọi việc về AWS tới khi tự xem lại, và dặn làm tiếp trên máy như hiện tại.
- **Cách khác:** cấp thêm quyền đó cho tài khoản để chữ hiện dần như với gpt-6-luna: chưa làm, nằm trong phần việc AWS đang gác.
- **Cái giá:** có lượt phần chữ trống hơn 15 giây, chỉ có dòng trạng thái (bài 34). Việc rút lại chữ vẫn có thể xảy ra, trong khi cái lợi "đọc sớm" không còn (bài 6).

### 5. Vì sao giao diện làm bằng React và đóng thành file tĩnh?

Giao diện là một chương trình viết bằng JavaScript, ngôn ngữ mà trình duyệt chạy được. React là một thư viện giúp viết giao diện thành từng mảnh dùng lại được (nút, thẻ, khung). Đóng gói là bước gom cả chương trình giao diện thành vài file sẵn để trình duyệt tải về; công cụ làm việc này tên là Vite. File tĩnh là file không đổi theo người hỏi: máy chủ chỉ gửi nguyên file đó đi, không phải tính gì.

- **Đã chọn:** React, đóng gói bằng Vite thành file tĩnh; chính máy chủ Python của dự án gửi các file đó cho trình duyệt.
- **Vì sao:** đã so ba hướng ngày 01–02/11. Viết bằng JavaScript thuần thì các đợt sau có nhiều màn hình sẽ phải làm lại. React đóng thành file tĩnh thì máy chủ Python gửi luôn, không cần một máy chủ riêng cho giao diện.
- **Cách khác:** JavaScript thuần: bỏ (lý do trên). Thêm một bộ linh kiện có sẵn: đã thử thật, 2 linh kiện vi phạm rào an toàn của trình duyệt (tự chèn khối định dạng vào trang); chỉ giữ bộ định dạng.
- **Cái giá:** các linh kiện (nút, thẻ, khung) phải tự viết. Sửa giao diện xong phải đóng gói lại thì trình duyệt mới thấy bản mới.

Bốn quyết định nhỏ hơn ở nửa để tra.

## Nếu… thì sao

Sáu tình huống của ô chat; bảng đủ ở nửa để tra. Tất cả **đọc từ chương trình**, chưa thử thật. Lời báo trong ngoặc kép là nguyên văn.

| Nếu | Hệ thống làm gì | Người dùng thấy gì | Đã có chưa |
|---|---|---|---|
| không nối được tới máy chủ khi gửi câu hỏi | báo lỗi; câu hỏi vẫn nằm trong khung trò chuyện | "Không kết nối được máy chủ. Vui lòng thử lại." và nút "Thử lại" | đã có |
| đang nhận câu trả lời thì đứt kết nối | xoá chữ và nguồn đã hiện | "Kết nối bị gián đoạn. Vui lòng thử lại." và nút "Thử lại" | đã có |
| máy chủ báo lỗi giữa lượt (model lỗi, kho không tìm được) | xoá chữ đã hiện, hiện lời báo của máy chủ | lời báo tương ứng (bài 6) và nút "Thử lại" | đã có |
| bước kiểm số nguồn hỏng sau khi chữ đã hiện | rút lại chữ đã hiện | "Câu trả lời không đáp ứng yêu cầu trích dẫn." và nút "Thử lại" (bài 16) | đã có |
| như dòng trên, nhưng ở tin hỏi tiếp ngay sau một câu trả lời mà cuộc trò chuyện đang nhớ (ví dụ "sửa lại thứ bạn vừa viết") | máy chủ gỡ chữ đã hiện, chạy lại cả lượt một lần mà không đưa câu trả lời cũ cho model | chữ biến mất, dòng trạng thái hiện lại, rồi câu trả lời mới; lần hai vẫn hỏng thì như dòng trên | đã có từ 22/11; trước đó 3 trong 7 lần đo ra màn hình lỗi |
| người dùng bấm "Dừng" | cắt đường nối; máy chủ bỏ lần gọi model đang chờ, không nhớ lượt đó | "Đã dừng. Phần trả lời chưa xong nên không hiện (chưa kiểm nguồn)." và nút "Hỏi lại" | đã có |

## Dễ nhầm

- **"Đây là một chatbot."** Chatbot chỉ là một trong sáu trang. Trang Lên kế hoạch và trang Khám phá dùng được mà không cần gõ câu nào.
- **"Số [1], [2] hiện trong câu trả lời."** Không. Chúng có ở tầng chương trình để kiểm; màn hình chỉ có dòng "Nguồn:".

## Câu hỏi tự kiểm

Thử trả lời bằng lời của mình trước khi bấm mở đáp án.

<details>
<summary>1. Vì sao ứng dụng có nhiều trang, không chỉ một khung chat?</summary>

Chỉ có khung chat thì người dùng không biết hệ thống làm được gì (lên lịch, thời tiết, hỏi bằng ảnh) cho tới khi gõ đúng câu.

</details>

<details>
<summary>2. Vì sao luật "câu hỏi dài nhất 500 ký tự" phải đặt ở cả giao diện lẫn máy chủ?</summary>

Giao diện chặn để người dùng thấy ngay; nhưng thứ chạy trong trình duyệt thì người dùng sửa được, nên máy chủ chặn lại lần nữa.

</details>

<details>
<summary>3. Bước kiểm số nguồn hỏng sau khi chữ đã hiện thì người dùng thấy gì? Có ngoại lệ nào?</summary>

Chữ bị rút lại, thay bằng "Câu trả lời không đáp ứng yêu cầu trích dẫn." và nút "Thử lại". Ngoại lệ từ 22/11: tin hỏi tiếp ngay sau một câu trả lời đang được nhớ thì máy chủ chạy lại cả lượt một lần trước khi báo lỗi.

</details>

<details>
<summary>4. Vì sao với Claude Sonnet 5.5 chữ không hiện dần?</summary>

Tài khoản AWS đang dùng chưa có quyền gọi model kiểu trả chữ dần. Cái giá: có lượt người dùng chờ hơn 15 giây chỉ với dòng trạng thái.

</details>

## Cấu hình đang chạy

*Theo chương trình giao diện sáng 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Công nghệ giao diện | React (thư viện dựng trang web), đóng gói bằng Vite thành các file tĩnh; máy chủ gửi các file đó cho trình duyệt | không cần một máy chủ riêng cho giao diện | đã cân ba hướng lúc chọn (mục "Quyết định và lý do") |
| Bản đồ | thư viện Leaflet; ô nền bản đồ lấy từ máy chủ bản đồ của nhóm OpenStreetMap Đức | không cần khoá; máy chủ đó dành cho ứng dụng nhỏ, phi thương mại | chưa so thư viện khác; nguồn ô nền đang là lựa chọn tạm |
| Chuyển trang | bằng phần sau dấu `#` của địa chỉ | tải lại hay chia sẻ đường link vẫn vào đúng trang, không cần thêm thư viện | — |
| Các ô của biểu mẫu Lên kế hoạch đang hiện | số ngày · người lớn · trẻ em · người lớn tuổi · kiểu đi · sở thích · ngày đi · hạng sao chỗ ở | ô nào không đủ dữ liệu để xếp lịch tử tế thì ẩn | — |
| Độ dài câu hỏi | nhiều nhất 500 ký tự, chặn ở cả giao diện và máy chủ | — | — |
| Nút in | chỉ ở trang Lên kế hoạch | — | — |
| Nút tải PowerPoint | ở mọi thẻ lịch, kể cả trong khung Trợ lý | — | — |
| Dòng ghi công ảnh, giấy phép ảnh | không hiện | quyết định của chủ dự án | — |

## Đã so

**Hình thức (giữa tháng 11).** Ba bản mẫu; chủ dự án chọn một bản. Bản đó được đo trên trình duyệt tự động ở hai khổ màn hình (rộng 1440 và 390 điểm ảnh):

| Đo gì | Ngưỡng | Lần đầu | Sau khi sửa |
|---|---|---|---|
| Tương phản giữa chữ và nền | ít nhất 4,5 : 1 | trên bản mẫu, mục trên thanh điều hướng chỉ 1,83 tới 2,71 | trên bản mẫu thấp nhất 6,07; trên chương trình thật 0 lần trượt trong 12 lần đo |
| Độ xô lệch của trang khi nội dung tải dần (trang danh sách bài) | nhiều nhất 0,1 | 0,23 tới 0,34 | nhiều nhất 0,045 |

**Giới hạn của phép đo.** Đo bằng trình duyệt tự động trên máy phát triển. Chưa ai thử trên một chiếc điện thoại thật.

## Quyết định nhỏ hơn

**Vì sao giao diện hỏi máy chủ "tính năng nào đang mở", mà không ghi sẵn trong giao diện?** Danh sách tính năng đang mở nằm ở một chỗ là cấu hình của máy chủ; giao diện hỏi lúc tải trang. Vì sao: lập luận của người viết, hồ sơ chỉ ghi cách làm (tính năng tắt thì mục tương ứng ẩn): mở hay tắt một tính năng chỉ cần sửa một dòng cấu hình rồi khởi động lại máy chủ, không phải đóng gói lại giao diện. Điều có thật trong chương trình: nút gửi ảnh chỉ hiện khi máy chủ đã dựng được phần hỏi bằng ảnh, nên không có cảnh có nút mà bấm vào không chạy. Cách khác: chưa thử. Cái giá: thêm một lần gọi máy chủ mỗi lần tải trang; hai mục Bản đồ và Lên kế hoạch hiện chậm hơn các mục khác một nhịp; lúc chưa có trả lời, trang Lên kế hoạch phải để trống chỗ, vì vẽ biểu mẫu cũ rồi đổi làm trang xô lệch 0,22 (một lần đo của đợt làm lại giao diện; ngưỡng là 0,1).

**Vì sao không hiện số [1], [2] trong chữ như nhiều hệ thống hỏi đáp?** Giao diện bỏ số trong chữ, thay bằng một dòng "Nguồn:" dưới câu trả lời. Vì sao: chủ dự án chọn khi duyệt thiết kế giao diện (06/11); lý do không được ghi lại. Cách khác: hiện số trong chữ (bản trước đó làm vậy). Cái giá: người đọc không thấy ý nào đến từ nguồn nào. Số [n] vẫn có ở tầng chương trình và vẫn được kiểm (bài 16).

**Vì sao sửa lịch bằng lời lại nhắn ở khung Trợ lý, mà trang Lên kế hoạch không có ô chat riêng?** Có ghi một nửa. Thiết kế giao diện đợt đầu chọn một khung trợ lý nổi trên mọi trang và một cuộc trò chuyện dùng chung qua các trang, theo cách các trang du lịch thật đã xem làm. Sửa lịch bằng lời đi qua khung đó là hệ quả: lịch được máy chủ giữ trong chính cuộc trò chuyện, nên nhắn ở khung Trợ lý là nhắn về đúng lịch đang hiện. Không tìm thấy hồ sơ nào cân riêng việc đặt một ô chat trên trang Lên kế hoạch. Cái giá: người dùng phải biết bấm nút "Trợ lý Huế"; trang có một dòng chỉ dẫn: "Muốn sửa lịch bằng lời (ví dụ "bỏ điểm đầu ngày 2"): bấm Trợ lý Huế rồi nhắn — lịch ở đây đổi theo."

**Vì sao tải lại trang là bắt đầu một cuộc trò chuyện mới?** Đã gặp thật: trước đây cuộc cũ vẫn sống 30 phút ở máy chủ, nên tải lại trang rồi hỏi lại câu đầu thì model đọc nó như câu hỏi tiếp của cuộc cũ; chủ dự án gặp ngày 15/11, một câu vừa được trả lời đúng bị từ chối. Nay mỗi lần tải trang, giao diện báo máy chủ quên cuộc cũ. Cái giá: không xem lại được cuộc cũ.

## Mọi tình huống hỏng của bài này

Sáu dòng của ô chat ở nửa để hiểu, cộng các dòng dưới. Tất cả đọc từ chương trình, chưa thử thật.

| Nếu | Hệ thống làm gì | Người dùng thấy gì | Đã có chưa |
|---|---|---|---|
| lúc tải trang không hỏi được máy chủ "tính năng nào đang mở" | coi các tính năng đó là đang tắt | không có mục Bản đồ, Lên kế hoạch; không có nút gửi ảnh; không có ô thời tiết ở Trang chủ | đã có |
| không tải được danh sách bài | báo ngay tại trang Khám phá | "Chưa tải được danh sách bài — thử tải lại trang." | đã có |
| không lấy được số thời tiết cho Trang chủ | ẩn ô thời tiết | không có ô thời tiết; không bao giờ hiện số cũ | đã có |
| luồng chữ kết thúc mà thiếu tin báo "xong" | xử lý như đứt kết nối | "Kết nối bị gián đoạn. Vui lòng thử lại." | đã có |
| model viết vào câu trả lời thứ không phải chữ (mã chạy được, ảnh lấy từ máy khác) | chỉ vẽ các kiểu chữ trong một danh sách cho phép (đoạn, chữ đậm, bảng, danh sách, đường link, và vài kiểu nữa) | chữ thường; đường link chỉ mở khi bấm; mục "Từ web" không có đường link nào trong chữ | đã có (bài 37) |
| người dùng tải lại trang giữa cuộc trò chuyện | bắt đầu một cuộc mới | khung trò chuyện trống | đã có; chưa có cách xem lại cuộc cũ |
| người dùng mở trên điện thoại | đổi bố cục theo bề rộng màn hình | thanh năm mục ở cuối màn hình | đã có; chưa thử trên một chiếc điện thoại thật |

Nút "Thử lại" khi không nối được máy chủ gửi lại đúng câu vừa hỏi. Dòng trạng thái mỗi lúc chỉ có một dòng. Lần chạy lại vì thiếu số nguồn không áp cho cuộc trò chuyện đang giữ một lịch (đường sửa lịch); ở đó vẫn như cũ. Tiền của lượt chạy lại tính cả hai lần gọi.

## Giới hạn đã biết

- **Chưa thử trên điện thoại thật**, mới thử ở bề rộng màn hình điện thoại trên máy tính.
- **Người đọc không thấy ý nào đến từ nguồn nào**, vì số [n] không hiện (bài 16).
- **Với model đang chạy, có lượt phần chữ trống hơn 15 giây** rồi mới hiện một lần; trong lúc đó chỉ có dòng trạng thái (bài 34).
- **Trang Bản đồ chỉ có điểm tham quan**, chưa có quán ăn hay chỗ ở.
- **Số lượt tải file lịch chưa bị giới hạn;** phải làm trước khi đưa lên mạng.
- **Chưa có ứng dụng điện thoại riêng;** chưa có quyết định nào được ghi về việc này. Trang web chạy được trong trình duyệt của điện thoại.

## Chi tiết để tra

- Dưới một lịch đã lập: ô chỗ ở khi người dùng đã chọn hạng sao (chưa chọn thì là một đường link sang trang Chỗ ở); các nút sao chép lịch, tải về dạng chữ, thêm vào ứng dụng lịch (khi đã chọn ngày đi), in hoặc lưu PDF, tải PowerPoint.
- Lượt lập lịch ví dụ là lượt thật ngày 21/11/2026 với Claude Sonnet 5.5: khung lịch sau 0,2 giây, xong sau 9,3 giây, một lần gọi model (để viết câu mô tả), 11 điểm trong 3 ngày, trong đó 3 điểm buổi tối (chợ, phố đi bộ); điểm buổi tối cũng có giờ, ví dụ chợ Đông Ba 18:00 – 23:00.
- Luật chọn ảnh cạnh câu trả lời: một ảnh khi mọi nguồn được trích thuộc cùng một bài về một nơi hoặc một món; trích nhiều bài thì chỉ lấy bài có tên xuất hiện trong câu hỏi hoặc câu trả lời, nhiều nhất 3 ảnh; lượt có mục web hoặc có lịch thì không hiện ảnh.
- Dưới câu trả lời có trích bài về chỗ ở còn có thẻ chỗ ở, đứng giữa ảnh và dòng "Nguồn:".
- Từ tối 21/11, bước kiểm con số (thời tiết, khoảng cách) ở lượt không có lịch không rút cả câu: chương trình gỡ câu chứa số lạ và thay chữ trên màn hình, không có nút "Thử lại" (bài 24).
- Tin hỏi nhiều ý mà kho trả lời được một phần thì không có mục web; chỉ có dòng "Tư liệu chưa có thông tin về: …" (bài 23).
- Việc làm tại trình duyệt, đủ danh sách: ô tìm của trang Khám phá lọc trong danh sách bài đã tải về, gõ thiếu dấu vẫn ra, và xếp bài khớp đúng dấu lên trước (sửa sau một lỗi thật ngày 16/11: tìm "lăng" ra các bài "làng" trước); bỏ số [n] khỏi chữ; chọn ảnh cạnh câu trả lời; dựng file lịch dạng chữ và file cho ứng dụng lịch từ lịch đang hiện. File PowerPoint thì dựng ở máy chủ, từ lịch máy chủ đang giữ.
- Trang Khám phá: 262 trên 265 bài có ảnh (đếm ngày 16/11; kho nay 266 bài, chưa đếm lại).
- Trang Bản đồ: 40 điểm tham quan.
- Phần mã của giao diện tải về nặng khoảng 124 KB sau khi nén (đo ngày 14/11; chưa đo lại).
- Trang theo dõi của chủ dự án (có từ 21/11) cho xem mỗi ngày có bao nhiêu lượt hỏi, kết cục ra sao, chờ bao lâu, tốn bao nhiêu tiền.

**Bài sau (bài 6):** phía sau các trang này là những khối nào, làm bằng công nghệ gì, và câu hỏi về giá vé đi qua chúng theo thứ tự nào.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Sáu mục, tên "Trợ lý Huế", thanh năm mục trên điện thoại, nút tròn mở khung trò chuyện, vẽ thanh điều hướng ngay rồi thêm mục khi có trả lời, lỗi thì coi tính năng là tắt: `frontend/src/App.jsx` (dòng 20, 32–47, 108–119, 165–189), `frontend/src/route.js` [code, đọc 22/11/2026]. Đường `GET /api/tinh_nang`: `backend/api/routes/cong.py`.
- Trang chủ, Khám phá (nút hỏi trợ lý điền sẵn câu, nút báo sai), Bản đồ, biểu mẫu (tên ô "Chỗ ở theo hạng sao", lịch ví dụ, dòng chỉ dẫn sửa bằng lời): `TrangChu.jsx`, `KhamPha.jsx`, `TrangBanDo.jsx`, `LenKeHoach.jsx`; `backend/config/settings.yaml` (`len_ke_hoach_o_hien`).
- Một lượt hỏi: dòng trạng thái (một dòng mỗi lúc, chữ nguyên văn), thứ tự chữ → ảnh → thẻ chỗ ở → Nguồn → ghi chú, nút Dừng và lời "Đã dừng…", nút "Thử lại": `frontend/src/chat.jsx`; dòng "đang viết" gần như không hiện với Claude: `backend/llm/assistant.py`, `backend/llm/bedrock_model.py` (theo biên bản kiểm `data/hoc_cung_D/kiem/bai_05_06.md` dòng 19) [suy từ code, chưa xem trên trình duyệt].
- Luật chọn ảnh: `frontend/src/anhTraLoi.js`. Bỏ số [n], danh sách kiểu chữ cho phép: `frontend/src/markdown.js`. Câu dẫn sang mục web: `frontend/src/moDauWeb.js`; điều kiện "cả câu bị từ chối": `settings.yaml` (`web_chi_khi_tu_choi`).
- Lời báo khi mất kết nối, đứt giữa chừng: `frontend/src/stream.js`. Lời báo khi kiểm số nguồn hỏng: `backend/api/routes/chat.py` (`_loi_trich_dan`). Giới hạn 500 ký tự ở hai nơi: `chat.jsx` (`MAX_QUERY`), `chat.py` (`ChatRequest.query`). Kiểm các ô biểu mẫu ở máy chủ: `chat.py` (`_kiem_truong_v2`).
- Việc làm tại trình duyệt: ô tìm trang Khám phá `frontend/src/timBai.js`; file lịch dạng chữ và file cho ứng dụng lịch `frontend/src/lich_ics.js`, `LichV2.jsx`. File PowerPoint dựng ở máy chủ: `backend/api/routes/xuat.py`.
- Ví dụ chính: `data/hoc_cung_D/vi_du_di_suot_vet.json` (dòng ghi chú; ba bài được trích). Ví dụ lập lịch (3 ngày, 2 người lớn, cân bằng, di tích; 219 ms khung, 9.320 ms xong; 11 điểm): `data/hoc_cung_D/vi_du_lap_lich_vet.json` [đã chạy 21/11].
- Ba hướng công nghệ, lý do nhiều trang, lựa chọn bỏ số [n]: `bai_hoc/17_GIAO_DIEN_VA_TOC_DO.md` phần 1. Tương phản, độ xô lệch, hai khổ màn hình, 124 KB, 262 / 265 bài có ảnh, 40 / 41 điểm có ảnh: `bai_hoc/24_GIAO_DIEN_H1.md` [đã chạy 14–16/11].
- Ô nền bản đồ: `backend/api/routes/cong.py` (địa chỉ máy chủ ô) và `session_prompt/HIEN_TRANG.md`. 40 điểm trên trang Bản đồ; chưa thử điện thoại thật; chưa giới hạn lượt tải; nút in chỉ ở trang Lên kế hoạch, nút PowerPoint ở mọi thẻ lịch: `bai_hoc/BAN_DO_DU_AN.md`, `guides/RUNBOOK_BAN_GIAO.md` mục 10.
- Trang theo dõi: `frontend/src/TheoDoi.jsx`; `bai_hoc/VIEC_MOI_XONG.md` mục 33.
- Mục "Quyết định và lý do", "Quyết định nhỏ hơn", "Nếu… thì sao", "Mọi tình huống hỏng" (sửa theo biên bản `data/hoc_cung_D/kiem/muc_moi_05_06_17_20.md` phần bài 05 [riêng tư]): nhiều trang, chủ dự án chọn "mức 2" và bỏ số [n] ngày 06/11: `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` (D1, D2) [quyết định đã ghi]; xoá chữ khi lỗi / rút lại (chủ dự án 31/10 11:48), cách quay về "chỉ tiến độ" khi rút > 1 %: `docs/superpowers/specs/2026-10-31-streaming-design.md` (D3, D5), lý do "chưa qua kiểm trích dẫn": `frontend/src/chat.jsx` (chú thích ở nhánh `AbortError`); chữ hiện một lần với Bedrock: `backend/llm/bedrock_model.py` (`stream_response` "stream giả"), thiếu quyền gọi trả chữ dần và AWS gác 22/11: `session_prompt/HIEN_TRANG.md` mục 3; ba hướng công nghệ 01–02/11: `bai_hoc/17_GIAO_DIEN_VA_TOC_DO.md` phần 1; máy chủ gửi file đóng gói: `backend/api/app.py` (`FRONTEND_DIR = frontend/dist`) [code]; tính năng đang mở, nút ảnh theo `app.state.anh`: `backend/api/routes/cong.py` (`tinh_nang`), xô lệch 0,22: chú thích `App.jsx` (`daCoTinhNang`); một cuộc trò chuyện qua các trang (D8): spec cổng đợt 1 và chú thích đầu `App.jsx`; dòng chỉ dẫn sửa lịch: `LenKeHoach.jsx`; tải lại trang là cuộc mới (lỗi 15/11): chú thích `chat.jsx` trước lời gọi `/api/conversation/new`; chạy lại một lần (từ 10:50 22/11; 3 / 7; không áp cuộc có lịch đã lưu; tiền tính cả hai lần): `backend/llm/assistant.py` (`answer_turn_stream_parallel`), giao diện gỡ chữ qua sự kiện `thay_chu` ở `chat.jsx` [code, chưa thử trên trình duyệt]; Dừng không nhớ lượt: chú thích `chat.jsx` nhánh `AbortError`, `routes/chat.py` (`client_disconnected`).

- Phần "Huế qua các thời kỳ" (sáu mốc, chữ viết lại từ bài trong kho, nằm trong trang Giới thiệu; chủ dự án chọn làm ngày 14/11): `frontend/src/HueQuaCacThoiKy.jsx` (chú thích đầu file), `frontend/src/GioiThieu.jsx` [code].

</details>
