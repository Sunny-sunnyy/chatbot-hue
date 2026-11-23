# Bài 5 — Người dùng thấy gì: các trang của ứng dụng

*Cập nhật 11:10, ngày 23/11/2026 · khớp hệ thống sáng 23/11 (giao diện mới, 48 tính năng, kho 267 bài) · tả lại màn hình theo giao diện "Dòng sông dẫn đường"; thêm quyết định 4 và cách thử 2 phút; hai quyết định cũ chuyển xuống nửa để tra · chữ trên màn hình đọc từ chương trình 23/11 và ảnh chụp tự động của bản đã gộp; người viết không chạy lại hệ thống; đã áp biên bản kiểm độc lập 11:05 23/11.*

**Bài trước đã biết:** sản phẩm làm ba loại việc: hỏi đáp có nguồn, việc cần tính, và lên kế hoạch.
**Bài này thêm:** ba loại việc đó nằm ở đâu trên màn hình: một vòng qua các trang, một lượt hỏi, một lượt lập lịch; rồi vì sao giao diện làm như vậy, và khi có thứ hỏng thì người dùng thấy gì.

## Ý chính

- Ứng dụng là một **trang web nhiều trang**, không chỉ là một khung chat. Thanh điều hướng có sáu mục: Trang chủ, Khám phá, Bản đồ, Lên kế hoạch, Trợ lý Huế, Giới thiệu. Trên máy tính, ở mọi trang khác còn có nút "Trợ lý Huế" ở góc dưới bên phải, mở khung trò chuyện ngay tại chỗ; trên điện thoại, Trợ lý Huế là mục giữa của thanh dưới.
- Lý do làm nhiều trang: nếu chỉ có một khung chat, người dùng không biết hệ thống làm được gì cho tới khi gõ đúng câu. Từ 23/11 lớp nhìn là "Dòng sông dẫn đường" (quyết định 4): luồng hỏi, lập lịch, xuất file không đổi; thêm một thứ nhỏ là thẻ chờ hiện tên các bài đã tìm thấy, bấm được.
- **Trợ lý Huế** là nơi hỏi đáp. Trong lúc chờ có một thẻ chờ ghi bước đang chạy và tên các bài đã tìm thấy; dưới câu trả lời có khung "Nguồn đã dùng", bấm một tên là xem đoạn gốc.
- **Lên kế hoạch** là nơi bấm nút để có một lịch, xem bản đồ, tải về. Muốn sửa lịch bằng lời thì nhắn ở khung Trợ lý Huế; lịch trên trang đổi theo.
- **Khám phá** cho đọc thẳng các bài của kho; chữ trên mỗi thẻ bài lấy từ chính bài đó.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| trình duyệt | **browser** | chương trình trên máy của người dùng để mở trang web (Chrome, Safari…) |
| giao diện | **frontend**, **UI** | phần của ứng dụng chạy trong trình duyệt của người dùng: các trang, nút bấm, ô gõ |
| máy chủ | **backend**, **server** | chương trình chạy trên máy của dự án; nhận yêu cầu từ giao diện, tìm trong kho, gọi model, gửi kết quả về (bài 6) |
| thanh điều hướng | **navigation bar** | hàng mục ở đầu trang để chuyển giữa các trang |
| dòng trạng thái | **status line** | dòng chữ báo hệ thống đang làm bước nào ("Đang hiểu câu hỏi…") |
| thẻ chờ | **loading state** | khung đứng thay câu trả lời trong lúc chờ |
| bến | — | chấm tròn trên nét sông ở màn đầu Trang chủ; mỗi bến là một lối vào |
| khung nhìn | **viewport** | phần trang thấy được trong cửa sổ trình duyệt khi chưa cuộn |
| tính năng đang mở | **feature flag** | một dòng trong cấu hình của máy chủ, ghi một tính năng đang được dùng hay đang tắt |

## Sáu mục trên thanh điều hướng

| Trang | Người dùng làm gì ở đó |
|---|---|
| **Trang chủ** | màn đầu: tiêu đề, ô hỏi lớn (gõ rồi gửi là khung Trợ lý mở ra và trả lời), câu gợi ý, dòng thời tiết; bên phải là ảnh sông Hương trong hình khúc sông với sáu **bến** là sáu lối vào. Phần cuộn xuống: "Chi tiết để tra" |
| **Khám phá** | chọn một chủ đề, xem danh sách bài dạng thẻ có ảnh, mở một bài để đọc; ở mỗi bài có nút "Hỏi trợ lý về điểm này" và nút "Báo thông tin chưa đúng" |
| **Bản đồ** | xem các điểm tham quan trên một bản đồ, lọc theo loại |
| **Lên kế hoạch** | chọn bằng nút: số ngày, số người lớn, trẻ em, có người lớn tuổi không, kiểu đi, sở thích, ngày đi, hạng sao của chỗ ở; nhận một lịch theo buổi; tải về. Khi chưa xếp lịch nào, trang có sẵn một lịch ví dụ |
| **Trợ lý Huế** | gõ câu hỏi, hoặc gửi một tấm ảnh để hệ thống đoán tên nơi hoặc món trong ảnh (bài 26); đọc câu trả lời, nguồn, và mục "Từ web (chưa kiểm)" nếu có. |
| **Giới thiệu** | đọc hệ thống làm được gì, giới hạn ở đâu, dữ liệu của người dùng được giữ thế nào; xem phần "Huế qua các thời kỳ" (sáu mốc lịch sử, kèm ảnh) |

Trên điện thoại, thanh ở cuối màn hình có năm mục; mục Giới thiệu vào từ chân trang.

Ngoài sáu mục này còn hai trang không nằm trên thanh điều hướng (tả ở "Chi tiết để tra"). Mục Bản đồ và mục Lên kế hoạch chỉ có khi tính năng tương ứng đang mở ở máy chủ (mục "Quyết định nhỏ hơn"); hai bến "Lên kế hoạch" và "Hỏi bằng ảnh" ở Trang chủ cũng vậy.

## Một lượt hỏi trên trang Trợ lý

Người dùng gõ *"Giá vé tham quan Đại Nội Huế là bao nhiêu?"* rồi gửi. Trên màn hình lần lượt có:

1. **Thẻ chờ**: khúc sông có con đò chạy; dòng trạng thái đổi theo từng bước máy chủ báo ("Đang hiểu câu hỏi…", rồi "Đã tìm trong kho, đang chuẩn bị câu trả lời…"); sau mỗi lần tìm, thêm tên các bài đã tìm thấy ("Đã tìm thấy N bài — bấm tên để đọc trong lúc chờ"; trên điện thoại và trong khung trợ lý nổi, nhãn chỉ ghi "Đã tìm thấy N bài"), bấm là mở bài ở thẻ trình duyệt mới. Đó là bài đã tìm thấy, chưa chắc được trích. Lúc model viết câu cuối, chữ trên thẻ đứng yên; chỉ con đò và nét đứt trên khúc sông còn chạy.
2. **Câu trả lời.** Với model đang chạy (Claude Sonnet 5.5), chữ hiện ra một lần khi model viết xong, thay chỗ thẻ chờ. Với model dùng trước đó (gpt-6-luna), chữ hiện dần trong lúc model viết.
3. **Ảnh**, chỉ khi câu trả lời nói về một nơi hoặc một món có ảnh chắc là đúng. Lượt ví dụ này trích ba bài khác nhau nên không có ảnh.
4. **Khung "Nguồn đã dùng (3 bài)"**: mỗi bài được trích là một nút, chấm màu theo chủ đề của bài. Bấm một nút thì mở ra đoạn gốc, kèm đường "Đọc cả bài …". Các số [n] mà model viết trong câu trả lời không hiện ra; giao diện bỏ chúng và chỉ giữ khung nguồn.
5. **Dòng ghi chú**, nếu có: ở lượt này là "Giờ mở cửa, giá vé, lịch lễ hội có thể đã thay đổi — hãy kiểm lại với nơi đến trước khi đi."

Kho không trả lời được cả câu hỏi thì có thể có thêm mục **"Từ web (chưa kiểm)"** (bài 25; "Chi tiết để tra").

Trong lúc chờ có nút **Dừng**. Tải lại trang là bắt đầu một cuộc trò chuyện mới; cũng có nút "Cuộc trò chuyện mới".

## Một lượt lập lịch trên trang Lên kế hoạch

Ví dụ lập lịch của cả bộ: người dùng chọn 3 ngày, 2 người lớn, đi kiểu cân bằng, sở thích di tích, rồi bấm xếp lịch. Sau khoảng 0,2 giây khung lịch đã hiện: ba ngày, mỗi ngày chia sáng, chiều, tối, các điểm đã có tên và giờ. Ở mỗi điểm lúc đó có hai vạch xám chờ chữ; khoảng 9 giây sau thì đủ câu mô tả cho mọi điểm.

Mỗi điểm có giờ, câu mô tả lấy từ kho và ảnh; trong ngày có gợi ý quán cho bữa trưa, bữa tối; đường nối các điểm là cùng nét sông. Ở màn rộng, bản đồ ghim các điểm đứng cạnh lịch; màn hẹp thì nằm dưới lịch. Dưới lịch là khung nguồn, ô chỗ ở, các nút sao chép, tải về, in, tải PowerPoint ("Chi tiết để tra"; bài 27, 30).

Muốn sửa, người dùng nhắn ở khung Trợ lý Huế, ví dụ "đổi chỗ ngày 1 với ngày 2". Lịch trên trang đổi theo, hoặc hệ thống nói vì sao không đổi được (bài 31).

## Quyết định và lý do

### 1. Vì sao làm một trang web nhiều trang, mà không chỉ làm một khung chat?

- **Đã chọn:** sáu trang, trong đó khung chat là một, cộng một nút mở khung chat ở mọi trang.
- **Vì sao:** quyết định đã ghi lúc thiết kế giao diện (chủ dự án chọn hướng "trang du lịch nhiều mục" ngày 06/11). Đề tài là ứng dụng hỗ trợ trải nghiệm; chỉ có khung chat thì người dùng không biết hệ thống có lên lịch, có thời tiết, có hỏi bằng ảnh cho tới khi gõ đúng câu.
- **Cách khác:** chỉ một khung chat: bản đầu tiên của hệ thống làm vậy; đã bỏ.
- **Cái giá:** nhiều màn hình phải làm và giữ cho đúng; trang Bản đồ và Lên kế hoạch cần thêm bảng dữ liệu riêng (bài 27).

### 2. Vì sao việc nào làm ngay trong trình duyệt, việc nào phải gửi về máy chủ?

- **Đã chọn:** việc chỉ đổi cách hiện thứ trình duyệt đã có thì làm tại trình duyệt, ví dụ ô tìm của trang Khám phá, bỏ số [n] khỏi chữ (đủ ở "Chi tiết để tra"). Việc nào quyết câu trả lời nói gì, có đúng nguồn không, lịch có hợp lệ không thì làm ở máy chủ: tìm trong kho, gọi model, kiểm số nguồn, xếp lịch, kiểm các ô của biểu mẫu.
- **Vì sao:** lập luận, không phải số đo. Thứ chạy trong trình duyệt thì người dùng sửa được; luật đặt ở đó là luật ai cũng tắt được. Việc chỉ đổi cách hiện thì không cần model, không cần khoá bí mật, và thấy kết quả ngay.
- **Cách khác:** đưa mọi việc về máy chủ, kể cả việc chỉ đổi cách hiện: chưa thử.
- **Cái giá:** vài giới hạn phải viết hai lần. Ví dụ câu hỏi dài nhất 500 ký tự: giao diện chặn để người dùng thấy ngay, và máy chủ chặn lại lần nữa vì không thể tin giao diện.

### 3. Vì sao khi lỗi giữa chừng hay bấm Dừng, chữ đã hiện bị xoá hết, không giữ nửa câu?

- **Đã chọn:** bước kiểm số nguồn ở cuối hỏng thì rút lại chữ đã hiện (với model đang chạy, từ 15:42 22/11 chữ được giữ tới khi qua kiểm nên không có gì để rút); lỗi hay đứt kết nối giữa chừng thì xoá hết; cả hai thay bằng một lời báo và nút "Thử lại". Bấm "Dừng" cũng xoá chữ đã hiện.
- **Vì sao:** chủ dự án chọn ngày 31/10, khi thiết kế phần chữ hiện dần. Lý do ghi trong chương trình: chữ đã hiện chưa qua bước kiểm số nguồn (bài 16).
- **Cách khác:** không hiện chữ nào trước khi kiểm xong: đã ghi là cách quay về nếu số lần rút lại vượt 1 % số câu mỗi tuần dùng thật. Từ 15:42 22/11 cách này được dùng cho model đang chạy, vì lý do khác ngưỡng đó ("Chi tiết để tra"; bài 6); với model trả chữ dần thì chưa dùng.
- **Cái giá:** người dùng mất phần đã đọc, phải hỏi lại.

### 4. Vì sao giao diện đổi sang hướng "Dòng sông dẫn đường", và vì sao chỉ đổi lớp nhìn?

Lớp nhìn là những thứ chỉ đổi cách trang trông ra sao: màu, cỡ chữ, chỗ đặt các khối, hình vẽ, chuyển động; chữ, nút và việc hệ thống làm nằm ở lớp khác.

- **Đã chọn:** từ 10:00 23/11, một nét sông Hương dùng ở ba chỗ: màn đầu Trang chủ (sáu lối vào là sáu bến), thẻ chờ, trục thời gian của lịch. Kèm theo: nguồn thành hàng nút có chấm màu, giá và giờ in đậm. Tính năng, luồng, chữ cảnh báo an toàn, cách xuất file giữ nguyên.
- **Vì sao:** ngày 22/11 chủ dự án muốn "một giao diện đẹp mắt, thu hút, hiện đại, sinh động" và giao nhóm tự chọn hướng. Kiểm kê thấy chỗ yếu nhất là trang hỏi đáp: lúc chờ một dòng chữ đứng yên tới 20–30 giây ở tin dài, nguồn là một dòng chữ nhỏ. Hướng này chữa cả hai bằng cùng một hình (máy chủ gửi thêm tên các bài đã tìm thấy) và giữ màu xanh ngọc chủ dự án đã chọn. Nhóm chốt bằng phiếu của ba phiên làm việc, sau khi dựng thử ba hướng trên ảnh. Ranh giới "chỉ lớp nhìn" do nhóm tự đặt khi nhận việc và đã nói với chủ dự án; chưa thấy ghi lý do riêng. Điều thấy được: nó được ghi cùng lúc với việc giữ giao diện cũ ở bản chính cho buổi chủ dự án tự thử.
- **Cách khác:** "Pháp lam" (ô màu ghép lệch cỡ) và "Huế theo giờ" (cảnh vẽ đổi màu trời theo giờ thật): đã dựng thử trên ảnh, bỏ (mục "Đã so").
- **Cái giá:** ở khung nhìn thấp hơn 869 điểm ảnh, gồm máy demo 1536 × 695, các bến chỉ còn tên, mất dòng mô tả; nhóm nhận, không vẽ lại. Mỗi lần đổi lớp nhìn phải chụp lại ảnh mọi trang (bài 35).

Sáu quyết định nhỏ hơn ở nửa để tra, gồm: chữ hiện một lần với model đang chạy; React.

## Nếu… thì sao

Sáu tình huống của ô chat; bảng đủ ở nửa để tra. Tất cả **đọc từ chương trình**, chưa thử thật, trừ dòng ghi **(đã đo 22/11)**. Lời báo trong ngoặc kép là nguyên văn.

| Nếu | Hệ thống làm gì | Người dùng thấy gì | Đã có chưa |
|---|---|---|---|
| không nối được tới máy chủ khi gửi câu hỏi | báo lỗi; câu hỏi vẫn nằm trong khung trò chuyện | "Không kết nối được máy chủ. Vui lòng thử lại." và nút "Thử lại" | đã có |
| đang nhận câu trả lời thì đứt kết nối | xoá chữ và nguồn đã hiện | "Kết nối bị gián đoạn. Vui lòng thử lại." và nút "Thử lại" | đã có |
| máy chủ báo lỗi giữa lượt (model lỗi, kho không tìm được) | xoá chữ đã hiện, hiện lời báo của máy chủ | lời báo tương ứng (bài 6) và nút "Thử lại" | đã có |
| bước kiểm số nguồn hỏng | model trả chữ dần: rút lại chữ đã hiện; model đang chạy: chữ chưa hề hiện (giữ tới khi kiểm) | "Câu trả lời không đáp ứng yêu cầu trích dẫn." và nút "Thử lại" (bài 16) | đã có |
| như dòng trên, nhưng ở ô chat, ở lượt hỏi tiếp đang kèm câu trả lời liền trước (ví dụ "sửa lại thứ bạn vừa viết") **(đã đo 22/11)** | máy chủ gỡ chữ đã hiện (nếu có), chạy lại cả lượt một lần mà không đưa câu trả lời cũ cho model | với model đang chạy: dòng trạng thái lặp lại một nhịp, chậm hơn khoảng 5 giây, không thấy chữ nào hiện rồi mất; lần hai vẫn hỏng thì như dòng trên | đã có từ 22/11 (số đo ở bảng đủ) |
| người dùng bấm "Dừng" | cắt đường nối; máy chủ bỏ lần gọi model đang chờ, không nhớ lượt đó | "Đã dừng. Phần trả lời chưa xong nên không hiện (chưa kiểm nguồn)." và nút "Hỏi lại" | đã có |

## Dễ nhầm

- **"Đây là một chatbot."** Chatbot chỉ là một trong sáu trang. Trang Lên kế hoạch và trang Khám phá dùng được mà không cần gõ câu nào.
- **"Số [1], [2] hiện trong câu trả lời."** Không. Chúng có ở tầng chương trình để kiểm; màn hình chỉ có khung "Nguồn đã dùng".
- **"Bấm một bến ở Trang chủ là gửi một câu hỏi."** Không. Bến là lối vào sang một trang; muốn hỏi thì gõ vào ô hỏi hoặc bấm câu gợi ý.

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
<summary>3. Bước kiểm số nguồn hỏng thì người dùng thấy gì? Có ngoại lệ nào?</summary>

Một lời báo "Câu trả lời không đáp ứng yêu cầu trích dẫn." và nút "Thử lại". Với model đang chạy, chữ hỏng chưa hề hiện; với model trả chữ dần, chữ đã hiện bị rút lại. Ngoại lệ từ 22/11: ở ô chat, lượt hỏi tiếp đang kèm câu trả lời liền trước thì máy chủ chạy lại cả lượt một lần trước khi báo lỗi (bài 16).

</details>

<details>
<summary>4. Vì sao với Claude Sonnet 5.5 chữ không hiện dần?</summary>

Tài khoản AWS đang dùng chưa có quyền gọi model kiểu trả chữ dần. Cái giá: có lượt người dùng chờ hơn 15 giây chỉ với thẻ chờ.

</details>

## Cấu hình đang chạy

*Theo chương trình giao diện sáng 23/11/2026 (giao diện mới, bản chính từ 10:00).*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Công nghệ giao diện | React (thư viện dựng trang web), đóng gói bằng Vite thành các file tĩnh; máy chủ gửi các file đó cho trình duyệt | không cần một máy chủ riêng cho giao diện | đã cân ba hướng lúc chọn (mục "Quyết định nhỏ hơn") |
| Bản đồ | thư viện Leaflet; ô nền bản đồ lấy từ máy chủ bản đồ của nhóm OpenStreetMap Đức | không cần khoá; máy chủ đó dành cho ứng dụng nhỏ, phi thương mại | chưa so thư viện khác; nguồn ô nền đang là lựa chọn tạm |
| Chuyển trang | bằng phần sau dấu `#` của địa chỉ | tải lại hay chia sẻ đường link vẫn vào đúng trang, không cần thêm thư viện | — |
| Các ô của biểu mẫu Lên kế hoạch đang hiện | số ngày · người lớn · trẻ em · người lớn tuổi · kiểu đi · sở thích · ngày đi · hạng sao chỗ ở | ô nào không đủ dữ liệu để xếp lịch tử tế thì ẩn | — |
| Độ dài câu hỏi | nhiều nhất 500 ký tự, chặn ở cả giao diện và máy chủ | — | — |
| Nút in | "In / Lưu PDF", chỉ ở trang Lên kế hoạch | bài 30 | — |
| Nút tải PowerPoint | ở mọi thẻ lịch, kể cả trong khung Trợ lý | — | — |
| Dòng ghi công ảnh, giấy phép ảnh | không hiện | quyết định của chủ dự án | — |
| Lớp nhìn | "Dòng sông dẫn đường", ở bản chính từ 10:00 23/11 | quyết định 4 | giao diện trước đó: quay về được bằng một lệnh hoàn tác lần gộp rồi đóng gói lại giao diện |
| Dòng mô tả dưới tên bến | chỉ hiện khi cửa sổ rộng từ 1.361 và cao từ 869 điểm ảnh; hẹp hơn 1.141 điểm ảnh thì màn đầu xếp dọc (tiêu đề, ô hỏi, sông, câu gợi ý), bến chỉ có tên | ở cửa sổ thấp, dòng mô tả chạm ảnh sông: đo tương phản 1,8 : 1 ở 1536 × 695 (ngưỡng 4,5 : 1) | vẽ lại vị trí bến: chưa làm, nhóm nhận (khác với ba cách giữ dòng mô tả đã thử, bài 35) |
| Câu gợi ý ở màn đầu | 5; cửa sổ rộng mà cao tới 720 điểm ảnh thì 4 | để dòng thời tiết còn trong màn đầu | — |
| Tên bài trong thẻ chờ | nhiều nhất 6, phần còn lại gộp thành "+k bài". Ở điện thoại và khung trợ lý nổi: 3 tên, mỗi tên một dòng. Ở cửa sổ cao tới 700 điểm ảnh (máy demo 1536 × 695 thuộc nhóm này): 3 tên, xếp nối nhau như ở màn rộng. Ở cả hai nhóm này không có dòng "+k bài"; tổng số bài vẫn ghi ở dòng nhãn | ô nhập và nút "Dừng" không bị đẩy khỏi màn | trước khi gộp: sáu tên, mỗi tên hai dòng, đẩy ô nhập khỏi màn điện thoại — đã sửa |
| Chuyển động | màn đầu: sông tự vẽ lúc tải, bến hiện lần lượt, con đò chạy vòng; nút "Dừng chuyển động" / "Chạy tiếp". Máy bật chế độ giảm chuyển động: mọi thứ đứng yên sẵn, không vẽ con đò, không có nút | chuyển động tự chạy quá 5 giây phải có nút dừng | bài 35 |

## Thử trong 2 phút

Bật lại hệ thống như mọi lần, mở trang trong trình duyệt.

1. **Trang chủ:** thấy nét sông có sáu bến bên phải, ô hỏi bên trái. Ở máy 1536 × 695 bến chỉ có tên (đúng như thiết kế, mục "Giới hạn đã biết").
2. Bấm mục **Trợ lý Huế** trên thanh điều hướng (hoặc bến "Hỏi bằng ảnh"). Gõ "Lăng Tự Đức có gì đặc biệt?" rồi bấm **Hỏi**. Nhìn thẻ chờ: con đò chạy, dòng trạng thái đổi, rồi "Đã tìm thấy … bài" với tên bài. Khi có câu trả lời, bấm một tên trong khung "Nguồn đã dùng" để mở đoạn gốc.
3. Bấm mục **Lên kế hoạch**. Chọn số ngày rồi bấm **Xếp lịch N ngày** (hoặc **Xếp lịch như ví dụ** ở đầu lịch ví dụ, ngay dưới dòng "Ví dụ"). Khung lịch hiện gần như ngay, câu mô tả đầy dần trong khoảng 10 giây.
4. Cuối lịch bấm **In / Lưu PDF**: hộp in của trình duyệt mở ra (bài 30).

Thấy khác bốn bước này thì tra bảng "Mọi tình huống hỏng" bên dưới, rồi bài 6.

## Đã so

**Hình thức (giữa tháng 11; giao diện trước 23/11).** Ba bản mẫu; chủ dự án chọn một bản. Bản đó được đo trên trình duyệt tự động ở hai khổ màn hình (rộng 1440 và 390 điểm ảnh):

| Đo gì | Ngưỡng | Lần đầu | Sau khi sửa |
|---|---|---|---|
| Tương phản giữa chữ và nền | ít nhất 4,5 : 1 | trên bản mẫu, mục trên thanh điều hướng chỉ 1,83 tới 2,71 | trên bản mẫu thấp nhất 6,07; trên chương trình thật 0 lần trượt trong 12 lần đo |
| Độ xô lệch của trang khi nội dung tải dần (trang danh sách bài) | nhiều nhất 0,1 | 0,23 tới 0,34 | nhiều nhất 0,045 |

**Giới hạn của phép đo.** Đo bằng trình duyệt tự động trên máy phát triển. Chưa ai thử trên một chiếc điện thoại thật. Giao diện mới đo tương phản lại từ đầu (bài 35).

**Hướng giao diện (22/11).** Vấn đề thật: chủ dự án muốn giao diện "đẹp mắt, thu hút, hiện đại, sinh động"; kiểm kê thấy trang hỏi đáp phẳng và lúc chờ chỉ một dòng chữ đứng yên. Một phiên dựng thử ba hướng ở màn đầu Trang chủ và một câu trả lời có thẻ chờ, ở bề rộng 1440 và 390 điểm ảnh; các phiên khác nhìn ảnh, xem 12 trang web du lịch và trợ lý thật, rồi bỏ phiếu.

| Hướng | Ý chính | Cái giá ghi lúc đề xuất | Phiếu | Giữ / bỏ |
|---|---|---|---|---|
| Dòng sông dẫn đường | một nét sông dùng ở màn đầu, thẻ chờ, trục lịch; giữ màu xanh ngọc đã có | nét sông vẽ vụng thì thành trang trí | người dựng thử đề nghị; người xem tham khảo xếp đầu | **giữ** |
| Huế theo giờ | cảnh sông – núi – cầu vẽ bằng chương trình, màu trời đổi theo giờ thật | đắt và rủi ro nhất; bốn bộ màu phải kiểm bốn lần | xếp hai: "bắt mắt nhất trong tích tắc đầu nhưng mất ảnh Huế thật" | bỏ |
| Giao diện cũ | — | — | xếp ba | thay |
| Pháp lam | ô màu men ghép lệch cỡ quanh ô hỏi | đổi hẳn nhận diện; nhiều màu dễ loè loẹt | xếp cuối: "thành bảng ô màu" | bỏ; mượn màu theo chủ đề cho chấm nguồn |

**Đọc bảng thế nào.** Cột "Phiếu" là thứ hạng một phiên ghi lại ở bề rộng 1440; phiên dựng thử đề nghị hướng 1 trước khi dựng; phiếu thứ ba không có thứ hạng ghi lại. Phiên điều phối chốt hướng 1 theo các phiếu.

**Giới hạn của phép so.** Đây là nhận xét bằng mắt của các phiên làm việc trên ảnh dựng thử, không phải phép đo trên người dùng; chưa người dùng thật nào được hỏi. Chủ dự án xem ảnh trước / sau và có thể nói đổi.

## Quyết định nhỏ hơn

**Vì sao với model đang chạy, chữ hiện một lần mà không hiện dần?** (Trước 23/11 là quyết định 4 của nửa để hiểu; chuyển xuống đây khi thêm quyết định về lớp nhìn.) Đã chọn: với Claude Sonnet 5.5 qua Amazon Bedrock, máy chủ gọi model trọn một lần rồi gửi cả câu trả lời về giao diện một lần. Vì sao: tài khoản AWS đang dùng chưa có quyền gọi model theo kiểu trả chữ dần. Khi đổi tạm sang Claude (21/11), chủ dự án ghi "không cần stream thật" (bài 33); việc AWS đang gác ("Chi tiết để tra"). Cách khác: cấp thêm quyền đó cho tài khoản để chữ hiện dần như với gpt-6-luna: chưa làm, nằm trong phần việc AWS đang gác. Cái giá: có lượt phần chữ trống hơn 15 giây, chỉ có thẻ chờ (bài 34). Cái lợi "đọc sớm" không còn, nên từ 15:42 22/11 chữ được giữ tới khi qua bước kiểm nguồn: người dùng không còn thấy chữ rồi mất, đổi lại thẻ chờ đứng lâu hơn ở lượt phải viết lại (bài 6).

**Vì sao giao diện làm bằng React và đóng thành file tĩnh?** (Trước 23/11 là quyết định 5 của nửa để hiểu; chuyển xuống đây cùng lúc.) Đã chọn: giao diện viết bằng JavaScript (ngôn ngữ trình duyệt chạy được), dựng bằng React, đóng gói bằng Vite thành file tĩnh — file không đổi theo người hỏi, máy chủ chỉ gửi nguyên file đi; chính máy chủ Python của dự án gửi các file đó cho trình duyệt. Vì sao: đã so ba hướng ngày 01–02/11. Viết bằng JavaScript thuần thì các đợt sau có nhiều màn hình sẽ phải làm lại. React đóng thành file tĩnh thì máy chủ Python gửi luôn, không cần một máy chủ riêng cho giao diện. Cách khác: JavaScript thuần: bỏ (lý do trên). Thêm một bộ linh kiện có sẵn: đã thử thật, bỏ vì vi phạm rào an toàn của trình duyệt ("Chi tiết để tra"). Cái giá: các linh kiện (nút, thẻ, khung) phải tự viết. Sửa giao diện xong phải đóng gói lại thì trình duyệt mới thấy bản mới.

**Vì sao giao diện hỏi máy chủ "tính năng nào đang mở", mà không ghi sẵn trong giao diện?** Danh sách tính năng đang mở nằm ở một chỗ là cấu hình của máy chủ; giao diện hỏi lúc tải trang. Vì sao: lập luận của người viết, hồ sơ chỉ ghi cách làm (tính năng tắt thì mục tương ứng ẩn): mở hay tắt một tính năng chỉ cần sửa một dòng cấu hình rồi khởi động lại máy chủ, không phải đóng gói lại giao diện. Điều có thật trong chương trình: nút gửi ảnh chỉ hiện khi máy chủ đã dựng được phần hỏi bằng ảnh, nên không có cảnh có nút mà bấm vào không chạy. Cách khác: chưa thử. Cái giá: thêm một lần gọi máy chủ mỗi lần tải trang; hai mục Bản đồ và Lên kế hoạch hiện chậm hơn các mục khác một nhịp; lúc chưa có trả lời, trang Lên kế hoạch phải để trống chỗ, vì vẽ biểu mẫu cũ rồi đổi làm trang xô lệch 0,22 (một lần đo của đợt làm lại giao diện; ngưỡng là 0,1).

**Vì sao không hiện số [1], [2] trong chữ như nhiều hệ thống hỏi đáp?** Giao diện bỏ số trong chữ, thay bằng tên các nguồn dưới câu trả lời (từ 23/11 là khung "Nguồn đã dùng"). Vì sao: chủ dự án chọn khi duyệt thiết kế giao diện (06/11); lý do không được ghi lại. Cách khác: hiện số trong chữ (bản trước đó làm vậy). Cái giá: người đọc không thấy ý nào đến từ nguồn nào. Số [n] vẫn có ở tầng chương trình và vẫn được kiểm (bài 16).

**Vì sao sửa lịch bằng lời lại nhắn ở khung Trợ lý, mà trang Lên kế hoạch không có ô chat riêng?** Có ghi một nửa. Thiết kế giao diện đợt đầu chọn một khung trợ lý nổi trên mọi trang và một cuộc trò chuyện dùng chung qua các trang, theo cách các trang du lịch thật đã xem làm. Sửa lịch bằng lời đi qua khung đó là hệ quả: lịch được máy chủ giữ trong chính cuộc trò chuyện, nên nhắn ở khung Trợ lý là nhắn về đúng lịch đang hiện. Không tìm thấy hồ sơ nào cân riêng việc đặt một ô chat trên trang Lên kế hoạch. Cái giá: người dùng phải biết bấm nút "Trợ lý Huế"; trang có một dòng chỉ dẫn: "Muốn sửa lịch bằng lời (ví dụ "bỏ điểm đầu ngày 2"): bấm Trợ lý Huế rồi nhắn — lịch ở đây đổi theo."

**Vì sao tải lại trang là bắt đầu một cuộc trò chuyện mới?** Đã gặp thật: trước đây cuộc cũ vẫn sống 30 phút ở máy chủ, nên tải lại trang rồi hỏi lại câu đầu thì model đọc nó như câu hỏi tiếp của cuộc cũ; chủ dự án gặp ngày 15/11, một câu vừa được trả lời đúng bị từ chối. Nay mỗi lần tải trang, giao diện báo máy chủ quên cuộc cũ. Cái giá: không xem lại được cuộc cũ.

## Mọi tình huống hỏng của bài này

Sáu dòng của ô chat ở nửa để hiểu, cộng các dòng dưới. Tất cả đọc từ chương trình, chưa thử thật.

| Nếu | Hệ thống làm gì | Người dùng thấy gì | Đã có chưa |
|---|---|---|---|
| tin dài nhiều ý, model đã tự tìm (thường là đã hết lượt) mà chữ nộp không có số nguồn nào | máy chủ cho model viết lại một lần, không công cụ, từ các đoạn đã gom (bài 21) | từ 15:42 22/11: chỉ thẻ chờ với dòng "Đang viết câu trả lời…" đứng lâu hơn (17–25 giây ở lượt đo trước khi mở), rồi câu trả lời thật (hoặc câu từ chối); đoạn chữ giữ chỗ không còn hiện | có từ 14:47 22/11; theo test và một lượt thật, chưa nhìn trên trình duyệt. Trước 15:42 đoạn chữ giữ chỗ hiện khoảng 15–17 giây rồi bị thay ("Chi tiết để tra") |
| số đo của dòng chạy lại (ở nửa để hiểu) | — | — | trước khi có: 3 trong 7 lần đo ra màn hình lỗi; sau: 0 trong 5 (chạy lại thật 2 lần), đo 22/11 |
| lúc tải trang không hỏi được máy chủ "tính năng nào đang mở" | coi các tính năng đó là đang tắt | không có mục Bản đồ, Lên kế hoạch; không có hai bến "Lên kế hoạch", "Hỏi bằng ảnh"; không có nút gửi ảnh; không có dòng thời tiết ở Trang chủ | đã có |
| không tải được danh sách bài | báo ngay tại trang Khám phá | "Chưa tải được danh sách bài — thử tải lại trang." | đã có |
| không lấy được số thời tiết cho Trang chủ | ẩn dòng thời tiết | không có dòng thời tiết dưới câu gợi ý; không bao giờ hiện số cũ | đã có |
| luồng chữ kết thúc mà thiếu tin báo "xong" | xử lý như đứt kết nối | "Kết nối bị gián đoạn. Vui lòng thử lại." | đã có |
| model viết vào câu trả lời thứ không phải chữ (mã chạy được, ảnh lấy từ máy khác) | chỉ vẽ các kiểu chữ trong một danh sách cho phép (đoạn, chữ đậm, bảng, danh sách, đường link, và vài kiểu nữa) | chữ thường; đường link chỉ mở khi bấm; mục "Từ web" không có đường link nào trong chữ | đã có (bài 37) |
| người dùng tải lại trang giữa cuộc trò chuyện | bắt đầu một cuộc mới | khung trò chuyện trống | đã có; chưa có cách xem lại cuộc cũ |
| người dùng mở trên điện thoại | đổi bố cục theo bề rộng màn hình | thanh năm mục ở cuối màn hình; màn đầu xếp dọc, bến chỉ có tên; thẻ chờ ba tên bài | đã có; chưa thử trên một chiếc điện thoại thật |
| cửa sổ trình duyệt thấp hơn 869 điểm ảnh (gồm máy demo 1536 × 695) | ẩn dòng mô tả dưới tên bến | sáu bến chỉ có tên; màn đầu vẫn trọn, không phải cuộn | nhóm nhận (quyết định 4) |
| máy bật chế độ giảm chuyển động | lớp nhìn tắt chuyển động | sông không tự vẽ, không có con đò, không có nút "Dừng chuyển động"; chữ và nút như thường | đã có (bài 35) |
| đang ở trang Lên kế hoạch có lịch, bấm mở khung trợ lý nổi (cửa sổ rộng 1280 tới 1536 điểm ảnh) | khung nổi đứng đè lên mép phải trang | ở 1280 điểm ảnh khung che hết cột bản đồ, mép phải cột lịch và khối "Đã sửa theo lời bạn"; ở máy demo 1536 × 695 che gần hết cột bản đồ (bài 27); đóng khung là thấy lại | chưa sửa (danh sách sau cổng gộp) |

Nút "Thử lại" khi không nối được máy chủ gửi lại đúng câu vừa hỏi. Dòng trạng thái mỗi lúc chỉ có một dòng. Lần chạy lại vì thiếu số nguồn không áp cho lượt sửa lịch; từ 16:08 22/11 cuộc trò chuyện đang giữ một lịch cũng được chạy lại cho câu hỏi thường (trước đó thì không). Tiền của lượt chạy lại tính cả hai lần gọi.

## Giới hạn đã biết

- **Chưa thử trên điện thoại thật**, mới thử ở bề rộng màn hình điện thoại trên máy tính.
- **Người đọc không thấy ý nào đến từ nguồn nào**, vì số [n] không hiện (bài 16).
- **Với model đang chạy, có lượt phần chữ trống hơn 15 giây** rồi mới hiện một lần; trong lúc đó chỉ có thẻ chờ; lúc model viết câu cuối, chữ trên thẻ đứng yên, chỉ con đò và nét đứt trên khúc sông còn chạy (bài 34).
- **Trang Bản đồ chỉ có điểm tham quan**, chưa có quán ăn hay chỗ ở.
- **Số lượt tải PowerPoint chỉ bị giới hạn khi bộ giới hạn lượt được bật** (30 lượt mỗi địa chỉ mỗi ngày, bài 37); trên máy phát triển bộ này đang tắt. Các file dựng trong trình duyệt không đi qua máy chủ nên không đếm.
- **Ở cửa sổ thấp hơn 869 điểm ảnh, gồm máy demo 1536 × 695, các bến ở Trang chủ chỉ còn tên**, mất dòng mô tả. Nhóm nhận, không vẽ lại; vẽ lại vị trí bến là một ý chưa thử, chỉ mở nếu chủ dự án thấy màn đầu thiếu chữ.
- **Trên trang Lên kế hoạch, khung trợ lý nổi mở ra che cột bản đồ:** ở 1280 điểm ảnh che hết cột bản đồ và mép phải cột lịch, ở máy demo 1536 × 695 che gần hết cột bản đồ (bài 27). Chưa sửa.
- **Ô "Ngày đi" hiện kiểu tháng/ngày/năm (`mm/dd/yyyy`) trên ảnh chụp tự động.** Nhóm suy luận đó là do trình duyệt chụp chạy tiếng Anh; chưa ai kiểm trên trình duyệt tiếng Việt.
- **Bản in và thẻ chọn tên ảnh trên điện thoại còn lỗi nhỏ** (bài 30, bài 26). Chưa có cặp "cùng một lịch, cũ ↔ mới" cho bản in.
- **Lớp nhìn mới chưa ai thử trên điện thoại thật, chưa ai in bằng tay.** Lượt thao tác tự động của cổng gộp chạy trước ba bản sửa nhỏ của lõi sáng 23/11; ba bản đó không chạm giao diện.
- **Chưa có ứng dụng điện thoại riêng;** chưa có quyết định nào được ghi về việc này. Trang web chạy được trong trình duyệt của điện thoại.

## Chi tiết để tra

- Trước 15:42 22/11 (lịch sử): ở lượt phải viết lại một lần, sau khoảng 14 giây chỉ có dòng tiến độ, màn hình có thể hiện một đoạn chữ ngắn chưa phải câu trả lời ("cần tìm thêm về…") khoảng 15–17 giây rồi bị thay bằng câu trả lời thật; ở lượt bị rút, chữ đã hiện bị xoá. Tính năng giữ chữ tới khi kiểm (mở 15:42) bỏ cả hai cảnh đó cho model đang chạy.
- Nút "Hỏi trợ lý về điểm này" ở trang Khám phá điền sẵn một câu hỏi vào ô; người dùng tự bấm gửi. Phần "Huế qua các thời kỳ" ở trang Giới thiệu kể sáu mốc bằng chữ viết lại từ các bài của kho.
- Quyết định nhỏ "React", bộ linh kiện có sẵn: đã thử thật, 2 linh kiện vi phạm rào an toàn của trình duyệt (tự chèn khối định dạng vào trang); chỉ giữ bộ định dạng.
- Hỏi bằng ảnh ở trang Trợ lý: đoán ra một tên thì hỏi luôn, kèm dòng báo là có thể đoán sai; đoán ra hai ba tên thì người dùng bấm chọn (bài 26).
- Lúc tải trang, giao diện vẽ thanh điều hướng ngay, đồng thời hỏi máy chủ "những tính năng nào đang mở"; có trả lời thì các mục đang mở được thêm vào.
- Ngày 1 của lịch ví dụ: sáng Đại Nội (8:00 – 10:30), chiều chùa Thiên Mụ rồi Kinh thành, tối chợ Đông Ba.
- Quyết định nhỏ "chữ hiện một lần": ngày 22/11 chủ dự án gác mọi việc về AWS tới khi tự xem lại, và dặn làm tiếp trên máy như hiện tại.
- React là một thư viện giúp viết giao diện thành từng mảnh dùng lại được (nút, thẻ, khung). Đóng gói là bước gom cả chương trình giao diện thành vài file sẵn để trình duyệt tải về; công cụ làm việc này tên là Vite (quyết định nhỏ "React").
- Dưới một lịch đã lập: ô chỗ ở khi người dùng đã chọn hạng sao (chưa chọn thì là một đường link sang trang Chỗ ở); các nút sao chép lịch, tải về dạng chữ, thêm vào ứng dụng lịch (khi đã chọn ngày đi), in hoặc lưu PDF, tải PowerPoint.
- Lượt lập lịch ví dụ là lượt thật ngày 21/11/2026 với Claude Sonnet 5.5: khung lịch sau 0,2 giây, xong sau 9,3 giây, một lần gọi model (để viết câu mô tả), 11 điểm trong 3 ngày, trong đó 3 điểm buổi tối (chợ, phố đi bộ); điểm buổi tối cũng có giờ, ví dụ chợ Đông Ba 18:00 – 23:00.
- Luật chọn ảnh cạnh câu trả lời: một ảnh khi mọi nguồn được trích thuộc cùng một bài về một nơi hoặc một món; trích nhiều bài thì chỉ lấy bài có tên xuất hiện trong câu hỏi hoặc câu trả lời, nhiều nhất 3 ảnh; lượt có mục web hoặc có lịch thì không hiện ảnh.
- Dưới câu trả lời có trích bài về chỗ ở còn có thẻ chỗ ở, đứng giữa ảnh và khung "Nguồn đã dùng".
- Từ tối 21/11, bước kiểm con số (thời tiết, khoảng cách) ở lượt không có lịch không rút cả câu: chương trình gỡ câu chứa số lạ, không có nút "Thử lại" (bài 24). Với model đang chạy, chữ được giữ tới khi kiểm xong nên từ 22:06 22/11 người dùng chỉ thấy bản đã gỡ; với model trả chữ dần thì chữ trên màn hình bị thay (bài 6).
- Tin hỏi nhiều ý mà kho trả lời được một phần thì không có mục web; chỉ có dòng "Tư liệu chưa có thông tin về: …" (bài 23).
- Việc làm tại trình duyệt, đủ danh sách: ô tìm của trang Khám phá lọc trong danh sách bài đã tải về, gõ thiếu dấu vẫn ra, và xếp bài khớp đúng dấu lên trước (sửa sau một lỗi thật ngày 16/11: tìm "lăng" ra các bài "làng" trước); bỏ số [n] khỏi chữ; chọn ảnh cạnh câu trả lời; dựng file lịch dạng chữ và file cho ứng dụng lịch từ lịch đang hiện. File PowerPoint thì dựng ở máy chủ, từ lịch máy chủ đang giữ.
- Trang Khám phá: 262 trên 265 bài có ảnh (đếm ngày 16/11; kho nay 267 bài, chưa đếm lại).
- Trang Bản đồ: 40 điểm tham quan.
- Phần mã của giao diện tải về nặng khoảng 124 KB sau khi nén (đo ngày 14/11 trên giao diện cũ; chưa đo lại trên giao diện mới).
- Trang chủ, phần cuộn xuống dưới màn đầu: "Khám phá theo chủ đề" (năm chủ đề của kho, có số bài), "Điểm nên đến" (sáu điểm, mỗi điểm có nút "Đọc bài" và "Hỏi trợ lý"), lối sang Lên kế hoạch, "Trợ lý trả lời thế nào" (ba bước).
- Sáu bến ở màn đầu và nơi mỗi bến dẫn tới: "Ăn gì ở Huế" (Khám phá, ẩm thực) · "Đi đâu hôm nay" (Khám phá, di tích) · "Lễ hội và ngày âm" (Khám phá, lễ hội) · "Lên kế hoạch" · "Hỏi bằng ảnh" (trang Trợ lý) · "Đi lại" (Khám phá, đi lại). Màn rộng và đủ cao thì dưới mỗi tên có một dòng mô tả ngắn.
- Trang Trợ lý lúc chưa hỏi gì: một khúc sông có bốn bến và con đò, lời chào ở giữa; cột trái có năm câu gợi ý và danh sách trợ lý làm được gì.
- Thẻ chờ, chi tiết: tên bài lấy từ tin "đã tìm" của máy chủ, cộng dồn qua các lần tìm, không trùng, theo thứ tự vào ngữ cảnh; chỉ tính bài của kho, không tính các nguồn do chương trình dựng (thẻ nơi, mục lục, khoảng cách, lịch, thời tiết). Nhãn ghi "Đã tìm thấy", không ghi "đã dùng", vì chú thích trong chương trình máy chủ dặn giao diện ghi đúng như vậy: đây là bài đã tìm thấy, chưa chắc được trích; bài được trích thật là các tên ở khung "Nguồn đã dùng", nên hai danh sách có thể khác nhau. Ảnh chụp câu "Lăng Tự Đức có gì đặc biệt?" sau khoảng 2,5 giây: "Đã tìm thấy 3 bài" — Lăng Tự Đức, Lăng Dục Đức, Cẩm nang du lịch di sản Huế. Với model trả chữ dần, chữ đầu tiên tới là thẻ chờ nhường chỗ cho bong bóng trả lời, dòng trạng thái thu nhỏ ở đầu bong bóng.
- Khung nguồn, chi tiết: chấm màu theo chủ đề (ẩm thực, di tích, lễ hội, đi lại, nghệ thuật biểu diễn); bấm lại nút đang mở thì đóng; đường "Đọc cả bài" chỉ có khi nguồn là một bài của kho.
- Mục web: khi kho không có câu trả lời cho cả câu hỏi và việc tra web có kết quả, phần chữ là một câu dẫn sang mục "Từ web (chưa kiểm)" ngay bên dưới, có danh sách trang web làm căn cứ (bài 25). Tra web không ra gì thì người dùng thấy câu từ chối kèm gợi ý cách hỏi.
- Lịch: 40 trên 41 điểm tham quan có ảnh. Đã có lịch thì ở màn rộng trang chia ba cột: biểu mẫu, lịch, bản đồ (bản đồ có nút chọn từng ngày và đi theo khi cuộn); điện thoại xếp chồng (bài 27).
- Quyết định 3, cách quay về "không hiện chữ trước khi kiểm" dùng cho model đang chạy từ 15:42 22/11 không phải vì ngưỡng 1 % bị vượt, mà vì chữ tới một lần nên hiện trước không còn lợi, trong khi cảnh chữ giữ chỗ hiện rồi bị thay vẫn còn (9 trên 114 lượt, 17–25 giây; bài 6). Ở lượt chạy lại (bảng "Nếu… thì sao"), từ 15:42 chữ lần đầu không được gửi; trước đó nó chưa kịp hiện.
- Hai trang không nằm trên thanh điều hướng: trang **Chỗ ở** (mở từ đường link dưới một lịch đã lập), và một trang **theo dõi** dành riêng cho chủ dự án, phải có khoá mới mở được.
- Trang theo dõi của chủ dự án (có từ 21/11) cho xem mỗi ngày có bao nhiêu lượt hỏi, kết cục ra sao, chờ bao lâu, tốn bao nhiêu tiền.

**Bài sau (bài 6):** phía sau các trang này là những khối nào, làm bằng công nghệ gì, và câu hỏi về giá vé đi qua chúng theo thứ tự nào.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Sáu mục, tên "Trợ lý Huế", thanh năm mục trên điện thoại, nút tròn mở khung trò chuyện, vẽ thanh điều hướng ngay rồi thêm mục khi có trả lời, lỗi thì coi tính năng là tắt: `frontend/src/App.jsx` (dòng 20, 32–47, 108–119, 165–189), `frontend/src/route.js` [code, đọc 22/11/2026]. Đường `GET /api/tinh_nang`: `backend/api/routes/cong.py`.
- Trang chủ, Khám phá (nút hỏi trợ lý điền sẵn câu, nút báo sai), Bản đồ, biểu mẫu (tên ô "Chỗ ở theo hạng sao", lịch ví dụ, dòng chỉ dẫn sửa bằng lời): `TrangChu.jsx`, `KhamPha.jsx`, `TrangBanDo.jsx`, `LenKeHoach.jsx`; `backend/config/settings.yaml` (`len_ke_hoach_o_hien`).
- Một lượt hỏi: dòng trạng thái (một dòng mỗi lúc, chữ nguyên văn), thứ tự chữ → ảnh → thẻ chỗ ở → Nguồn → ghi chú, nút Dừng và lời "Đã dừng…", nút "Thử lại": `frontend/src/chat.jsx`; dòng "đang viết" gần như không hiện với Claude: `backend/llm/assistant.py`, `backend/llm/bedrock_model.py` (theo biên bản kiểm `data/hoc_cung_D/kiem/bai_05_06.md` dòng 19) [code; đã nhìn trên trình duyệt 16:21 22/11 ở lượt thường của tin dài: chỉ MỘT dòng "Đã tìm trong kho, đang chuẩn bị câu trả lời…" rồi cả câu trả lời hiện một lần, "Đang viết câu trả lời…" gần như không hiện — `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 hàng "Lưới viết lại", `bai_hoc/VIEC_MOI_XONG.md` mục 44; phiên đo chạy, người viết chép].
- Luật chọn ảnh: `frontend/src/anhTraLoi.js`. Bỏ số [n], danh sách kiểu chữ cho phép: `frontend/src/markdown.js`. Câu dẫn sang mục web: `frontend/src/moDauWeb.js`; điều kiện "cả câu bị từ chối": `settings.yaml` (`web_chi_khi_tu_choi`).
- Lời báo khi mất kết nối, đứt giữa chừng: `frontend/src/stream.js`. Lời báo khi kiểm số nguồn hỏng: `backend/api/routes/chat.py` (`_loi_trich_dan`). Giới hạn 500 ký tự ở hai nơi: `chat.jsx` (`MAX_QUERY`), `chat.py` (`ChatRequest.query`). Kiểm các ô biểu mẫu ở máy chủ: `chat.py` (`_kiem_truong_v2`).
- Việc làm tại trình duyệt: ô tìm trang Khám phá `frontend/src/timBai.js`; file lịch dạng chữ và file cho ứng dụng lịch `frontend/src/lich_ics.js`, `LichV2.jsx`. File PowerPoint dựng ở máy chủ: `backend/api/routes/xuat.py`.
- Ví dụ chính: `data/hoc_cung_D/vi_du_di_suot_vet.json` (dòng ghi chú; ba bài được trích). Ví dụ lập lịch (3 ngày, 2 người lớn, cân bằng, di tích; 219 ms khung, 9.320 ms xong; 11 điểm): `data/hoc_cung_D/vi_du_lap_lich_vet.json` [đã chạy 21/11].
- Ba hướng công nghệ, lý do nhiều trang, lựa chọn bỏ số [n]: `bai_hoc/17_GIAO_DIEN_VA_TOC_DO.md` phần 1. Tương phản, độ xô lệch, hai khổ màn hình, 124 KB, 262 / 265 bài có ảnh, 40 / 41 điểm có ảnh: `bai_hoc/24_GIAO_DIEN_H1.md` [đã chạy 14–16/11].
- Ô nền bản đồ: `backend/api/routes/cong.py` (địa chỉ máy chủ ô) và `session_prompt/HIEN_TRANG.md`. 40 điểm trên trang Bản đồ; chưa thử điện thoại thật; lượt tải PowerPoint: `TRAN_TAI_FILE = 30` trong `backend/api/gioi_han.py`, chỉ đếm khi đặt `HUE_LUOT_MOI_NGAY` hoặc `HUE_LUOT_TONG_MOI_NGAY` (thêm 12:48 22/11, commit `7024636e`) [code]; nút in chỉ ở trang Lên kế hoạch, nút PowerPoint ở mọi thẻ lịch: `bai_hoc/BAN_DO_DU_AN.md`, `guides/RUNBOOK_BAN_GIAO.md` mục 10.
- Trang theo dõi: `frontend/src/TheoDoi.jsx`; `bai_hoc/VIEC_MOI_XONG.md` mục 33.
- Mục "Quyết định và lý do", "Quyết định nhỏ hơn", "Nếu… thì sao", "Mọi tình huống hỏng" (sửa theo biên bản `data/hoc_cung_D/kiem/muc_moi_05_06_17_20.md` phần bài 05 [riêng tư]): nhiều trang, chủ dự án chọn "mức 2" và bỏ số [n] ngày 06/11: `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` (D1, D2) [quyết định đã ghi]; xoá chữ khi lỗi / rút lại (chủ dự án 31/10 11:48), cách quay về "chỉ tiến độ" khi rút > 1 %: `docs/superpowers/specs/2026-10-31-streaming-design.md` (D3, D5), lý do "chưa qua kiểm trích dẫn": `frontend/src/chat.jsx` (chú thích ở nhánh `AbortError`); chữ hiện một lần với Bedrock: `backend/llm/bedrock_model.py` (`stream_response` "stream giả"), thiếu quyền gọi trả chữ dần và AWS gác 22/11: `session_prompt/HIEN_TRANG.md` mục 3; ba hướng công nghệ 01–02/11: `bai_hoc/17_GIAO_DIEN_VA_TOC_DO.md` phần 1; máy chủ gửi file đóng gói: `backend/api/app.py` (`FRONTEND_DIR = frontend/dist`) [code]; tính năng đang mở, nút ảnh theo `app.state.anh`: `backend/api/routes/cong.py` (`tinh_nang`), xô lệch 0,22: chú thích `App.jsx` (`daCoTinhNang`); một cuộc trò chuyện qua các trang (D8): spec cổng đợt 1 và chú thích đầu `App.jsx`; dòng chỉ dẫn sửa lịch: `LenKeHoach.jsx`; tải lại trang là cuộc mới (lỗi 15/11): chú thích `chat.jsx` trước lời gọi `/api/conversation/new`; chạy lại một lần (từ 10:50 22/11; 3 / 7; không áp lượt sửa lịch; cuộc có lịch đã lưu được chạy lại cho câu hỏi thường từ 16:08 22/11 — `settings.yaml` dòng 76 `nho_dap_cuoc_co_lich`, `assistant.py` dòng 2114–2131; tiền tính cả hai lần): `backend/llm/assistant.py` (`answer_turn_stream_parallel`), giao diện gỡ chữ qua sự kiện `thay_chu` ở `chat.jsx` [code, chưa thử trên trình duyệt]; Dừng không nhớ lượt: chú thích `chat.jsx` nhánh `AbortError`, `routes/chat.py` (`client_disconnected`).

- Phần "Huế qua các thời kỳ" (sáu mốc, chữ viết lại từ bài trong kho, nằm trong trang Giới thiệu; chủ dự án chọn làm ngày 14/11): `frontend/src/HueQuaCacThoiKy.jsx` (chú thích đầu file), `frontend/src/GioiThieu.jsx` [code].

- Dòng chạy lại ở lượt đang kèm câu trả lời liền trước đổi nhãn "đọc từ chương trình" ⇒ "đã đo 22/11" (sửa chỗ lệch với bài 16): `report_agent/2026-11-22/b_nho_dap_chay_lai.md` dòng 32 (0 / 5, trước 3 / 7, chạy lại thật 2 / 5) và dòng 36 (đã nhìn trên trình duyệt: dòng tiến độ lặp một nhịp, chậm khoảng 5 giây); `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 ("KHÔNG có chữ nào hiện rồi mất", lý do đọc code giao diện) [đã chạy, phiên đo; người thứ hai kiểm; người viết không chạy lại]. Cập nhật theo bộ thay đổi mở 14:47 22/11/2026: `bai_hoc/VIEC_MOI_XONG.md` mục 42, 43; `guides/RUNBOOK_BAN_GIAO.md` mục 10.1; `backend/config/settings.yaml`.

- Đã qua một lượt kiểm chéo sau lượt cập nhật 14:47 (`data/hoc_cung_D/kiem/cap_nhat_14h47.md`) [riêng tư]. Theo đó thêm dòng viết lại một lần vào bảng đủ: `bai_hoc/VIEC_MOI_XONG.md` mục 42, đính chính 15:14 ("khoảng 14 giây đầu chỉ có một dòng trạng thái; rồi có thể hiện một đoạn chữ ngắn CHƯA phải câu trả lời… khoảng 15–17 giây"); `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 hàng "Lưới viết lại" [suy từ chương trình và sổ máy chủ, chưa chụp màn hình].

- Câu "kiểm con số … chỉ thấy bản đã gỡ" (sửa 22:25 22/11/2026; bản trước ghi "thay chữ trên màn hình" cho mọi model): commit `70ba72d5` (gộp `dc43cc93` 22:06) — `backend/llm/assistant.py` dòng 2121–2125 (chữ gom phát dạng `chu_cua_model(trace)` khi `trace.kiem_so_go` có); đường chữ chạy dần (không gom): chữ đã hiện ⇒ `backend/api/routes/chat.py` `finish` dòng 730–747 gửi `thay_chu`, `frontend/src/chat.jsx` dòng 152–156 thay cả ô chữ [code, đọc main `404448a8`; không chạy test]. Phần đủ: bài 6, "Chi tiết để tra".
- Giữ chữ tới khi qua bước kiểm nguồn (mở 15:42 22/11/2026; chỉ lượt có công cụ trên model trả chữ một lần; đường chữ chạy dần không giữ; đo trước khi mở: viết lại 9 / 114 lượt, chữ giữ chỗ đứng 17–25 giây): `backend/config/settings.yaml` dòng `giu_chu_toi_kiem`, `backend/llm/assistant.py` (chú thích `giu_chu_toi_kiem`, biến `cho_kiem` trong luồng gửi chữ), `backend/tests/test_giu_chu_toi_kiem.py` (tên ca: lượt qua kiểm hiện như cũ, chữ giữ chỗ không bao giờ hiện, chữ bị rút không bao giờ hiện, đường chữ chạy dần không đổi) [code, đọc 22/11; không chạy test]; `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 hàng "Lưới viết lại" ("Đang viết câu trả lời…" đứng 17–25 giây ở ca viết lại — ca này chưa trúng trên trình duyệt; lượt thường đã nhìn trên trình duyệt 22/11) [chép]. Câu "cách quay về… không phải vì ngưỡng bị vượt" và lý do "chữ tới một lần" ở quyết định 3: biên bản `data/hoc_cung_D/kiem/phan_xu_va_cap_nhat_15h42.md` Phần 1 bảng hai dòng 3 [riêng tư]; `settings.yaml` dòng 99 (`giu_chu_toi_kiem`) [chép biên bản, đã mở nguồn].


- Đợt 23/11 (giao diện mới, ở bản chính từ 10:00 23/11, commit gộp `e7193bd0`; người viết đọc main `20f998f4`, không chạy server, không mở trình duyệt):
  - Màn đầu Trang chủ (tiêu đề, ô hỏi, năm câu gợi ý — bốn ở cửa sổ cao tới 720 px, dòng thời tiết, sáu bến và nơi dẫn tới, bến "Lên kế hoạch" / "Hỏi bằng ảnh" theo tính năng, nút "Dừng chuyển động" / "Chạy tiếp", không có nút khi máy giảm chuyển động): `frontend/src/TrangChu.jsx` (`NHANH`, `HeroSong`), `frontend/src/song/Song.jsx` (`HeroSong`, `OHoi`, `MAN_DOC`), `frontend/src/song/song.css` (khối màn đầu: `@media (min-width: 1141px) and (max-height: 868px), (min-width: 1141px) and (max-width: 1360px)` ẩn dòng mô tả, chú thích "1,8 : 1" ở 1536 × 695; `max-height: 720px` ẩn câu gợi ý thứ năm; `max-width: 1140px` xếp dọc) [code]; phần dưới màn đầu: `TrangChu.jsx` (`LINH_VUC`, `DIEM`, khối "Trợ lý trả lời thế nào") [code]; chuyển động chỉ chạy dưới lớp `hieu-ung`: `frontend/src/hieuUng.js`, con đò không vẽ khi giảm chuyển động: `song/hinh.jsx` (`Do`) [code]. Ảnh: `data/giao_dien_2026-11-22/sau_gop_10c30bc5/T01_trang_chu_1536x695_man.png` (sáu bến chỉ tên, bốn câu gợi ý, dòng thời tiết, nút "Dừng chuyển động", nút "Trợ lý Huế" góc dưới phải) [riêng tư; đã mở ảnh]; màn đầu trọn ở 1536 × 695: `…/MAN_DAU_TINH_THEODOI_HOI_ANH_LICH_LOI_NGUON.md` [riêng tư; đã chạy, phiên đo].
  - Thẻ chờ (khúc sông + con đò, dòng trạng thái = nhãn của bước cuối trong các tin `status`, "Đã tìm thấy N bài — bấm tên để đọc trong lúc chờ", tối đa 6 tên + "+k bài", tên mở ở thẻ mới, không còn số đoạn trong ngoặc): `frontend/src/chat.jsx` dòng 22–31 (`STATUS_TEXT`), 139–143 (`daTim`), 415–419; `song/Song.jsx` (`ChoSong`); ba tên một dòng ở `.chat`, `max-width: 760px`, `max-height: 700px`: `song/song.css` khối "Lúc chờ" [code]; bản cũ có "(n đoạn)": `git show bedfa091:frontend/src/chat.jsx` dòng 491 [code]. Máy chủ gửi tên bài trong tin "đã tìm": commit `a76eb962` (`backend/llm/assistant.py` `bai_da_tim`, `backend/api/routes/chat.py` `StreamEvents.status`, `backend/tests/test_su_kien_ten_bai.py`); "im 17–20 giây lúc viết cuối" là lời commit đó [chép, đã mở nguồn]. Ảnh: `sau_gop_10c30bc5/H01_dang_cho_1536x695_man.png` (3 bài, câu Lăng Tự Đức), `C01_cho_09s_1440_man.png` (6 bài, tin dài) [riêng tư; đã mở ảnh].
  - Khung "Nguồn đã dùng (n bài)", chấm màu theo chủ đề: `frontend/src/SourceLine.jsx`, `song/nhin.js` (`linhVuc`), `song/song.css` (`.nguon-so`); bản cũ là "Nguồn:" (`git diff bedfa091 origin/main -- frontend/src/SourceLine.jsx`) [code]. Ảnh `H03_mo_doan_trich_1536x695_man.png` [đã mở ảnh]. Giá, giờ in đậm, tiêu đề phần: `song/nhin.js` (`trangTriTraLoi`) [code].
  - Trang Trợ lý trống (khúc sông bốn bến, lời chào, cột trái): `song/song.css` khối "Trang Trợ lý lúc chưa hỏi gì", `chat.jsx` (`TrangTroLy`); ảnh `T05_tro_ly_trong_1536x695_man.png` [code; đã mở ảnh]. Nút "Trợ lý Huế" ở mọi trang trừ trang Trợ lý: `frontend/src/App.jsx` (`!onTroLy && !panelOpen`); nút nổi ẩn ở bề rộng ≤ 760 px (`.noi { display: none }`), trên điện thoại lối vào là mục giữa thanh dưới: `frontend/src/index.css` dòng 453 [code]. Đuôi "— bấm tên…" của nhãn thẻ chờ ẩn ở `.chat` và ≤ 760 px (`.cho-nhan-them`); nét đứt `.net-song-chay` vẫn chạy dưới `.hieu-ung` lúc chờ: `song/song.css` dòng 74, 80, 158–159; khối `max-height: 700px` chỉ ẩn tên thứ tư trở đi, không đổi cách xếp (ảnh H01 1536 × 695: ba tên nối nhau) [code; theo biên bản `data/hoc_cung_D/kiem/dot_2311_k1_kiem.md`, người viết đã mở `song.css`]. Vị trí nút "Xếp lịch như ví dụ" (sau dòng "Ví dụ…", trước thẻ lịch ví dụ): `LenKeHoach.jsx` dòng 105–110 [code, theo biên bản]. Ranh giới "chỉ lớp nhìn" do phiên điều phối tự đặt, đã nói với chủ dự án: `session_prompt/HIEN_TRANG.md` mục 4 gạch "17:19 22/11/2026 — GIAO DIỆN" ("[Cách phiên điều phối đọc + ranh giới tự đặt, đã nói với chủ dự án:]") [chép, người sửa đã mở 23/11].
  - Trang Lên kế hoạch (ba cột khi có lịch, bản đồ có nút từng ngày, nét sông nối điểm, khung nguồn chung, nút "Xếp lịch N ngày", "Xếp lịch như ví dụ", "In / Lưu PDF"): `frontend/src/LenKeHoach.jsx` dòng 110, 256; `LichV2.jsx` dòng 210, 364; `BanDoLich.jsx` dòng 79; lời commit `22e4694f`, `10c30bc5` [code; chép lời commit]. Ảnh `L02_lich_xong_1536x695_man.png` (ba cột, ô ngày `mm/dd/yyyy`) [đã mở ảnh].
  - Quyết định 4: lời chủ dự án 17:16 22/11 và việc nhóm tự chọn hướng, ranh giới "chỉ lớp nhìn" ghi cùng lúc với việc giữ giao diện cũ ở bản chính: `session_prompt/HIEN_TRANG.md` mục 4 gạch "17:19 22/11/2026 — GIAO DIỆN" [chép, đã mở nguồn]; ba hướng, cái giá từng hướng, đề nghị hướng 1, mượn màu theo chủ đề: `data/giao_dien_2026-11-22/HUONG_DE_XUAT.md` [riêng tư; đã mở]; chỗ yếu của giao diện cũ (lúc chờ đứng yên 20–30 giây, nguồn một dòng nhỏ), màu chủ dự án chọn 07/11 và 14/11: `…/KIEM_KE.md` mục 1, 3 [riêng tư; đã mở]; phiếu xếp hạng ở 1440 và 12 trang đã nhìn: `…/THAM_KHAO.md` mục 0, 6 [riêng tư; đã mở]; "chốt bằng ba phiếu": `session_prompt/VIEC_DANG_MO.md` khối A hàng X13 [chép]; phiên điều phối chốt theo phiếu: `HIEN_TRANG.md` mục 4 cùng gạch. Phiếu thứ ba: CHƯA tìm thấy file ghi thứ hạng.
  - Giới hạn và tình huống mới: bến chỉ tên dưới 869 px, nhóm nhận, ý 64: `session_prompt/VIEC_DANG_MO.md` khối A (QUYẾT ĐỊNH của phiên điều phối sáng 23/11, (a)) và `HIEN_TRANG.md` mục 1 gạch "Giao diện mới…" [chép]; khung trợ lý nổi ở 1280 px, bản in trang 2, thẻ chọn tên ảnh ở điện thoại, ô ngày `mm/dd/yyyy` (suy luận "trình duyệt chụp chạy tiếng Anh"), chưa có cặp bản in cũ ↔ mới: `HIEN_TRANG.md` mục 1 cùng gạch; `VIEC_DANG_MO.md` khối A hàng X13 và danh sách SAU CỔNG [chép]; "đóng khung là thấy lại" [suy luận của người viết]. Cổng gộp 761 ảnh, tám cỡ khung nhìn: `HIEN_TRANG.md` mục 1 [chép]. Lùi bằng `git revert -m 1 e7193bd0` + dựng lại `dist`: cùng gạch [chép]. Ba bản sửa lõi sáng 23/11 không chạm `frontend/`: `git show --stat 63ccf07c 2ba8d394 f5cf10b5` [đã chạy, người viết]; lượt thao tác tự động chạy trước ba bản đó: lời giao đợt + `HIEN_TRANG.md` mục 1 [chép].
  - Cách thử 2 phút: tên nút và tên bến chép từ code ở trên. Lời giao đợt ghi "bấm một bến ⇒ trang Trợ lý"; trong code chỉ bến "Hỏi bằng ảnh" dẫn sang trang Trợ lý (các bến khác sang Khám phá / Lên kế hoạch) ⇒ bài ghi mục "Trợ lý Huế" trên thanh điều hướng, kèm bến "Hỏi bằng ảnh" [code].
  - Bảng "Hướng giao diện" ở "Đã so": `HUONG_DE_XUAT.md`, `THAM_KHAO.md` mục 6 (câu trích nguyên văn của phiếu) [riêng tư; đã mở]. Tương phản của giao diện mới: bài 35 (`…/TUONG_PHAN.md`) [riêng tư; đã mở phần kết luận].

</details>
