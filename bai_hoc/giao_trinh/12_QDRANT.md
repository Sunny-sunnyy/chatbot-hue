# Bài 12 — Cất vào Qdrant, cập nhật khi kho đổi, và vì sao kho lệch chỉ mục thì không câu hỏi nào được trả lời

*Cập nhật 20:46, ngày 23/11/2026 · số kho / số tính năng / mức test theo hệ thống lúc code đứng yên tối 23/11 (kho 269 bài / 9.533 đoạn) · bản 17:11 22/11: phân xử chỗ lệch giữa các bài · trước đó: cơ chế đọc từ chương trình và cấu hình đang chạy; số của lần cập nhật chỉ mục lấy từ lần chạy thật sáng 22/11 và phép kiểm độc lập của một phiên khác; ba tình huống Qdrant tắt / ngừng lấy từ lần thử thật trưa 22/11 (bài 6); người viết không chạy lại. · 09:55 24/11/2026: số đoạn của kho trong thân bài 9.533 ⇒ 9.536 (sáng 24/11 ba bài kho được thêm câu; chỉ mục cập nhật 07:30 và 07:49; bản ghi chỉ mục và Qdrant cùng ghi 9.536 — phiên D mở lúc 09:55); các câu có mốc giờ cũ và khối Nguồn giữ nguyên.*

**Bài trước đã biết:** mỗi đoạn có chữ, thông tin gắn kèm, một vector, và phần từ khoá.
**Bài này thêm:** 9.536 đoạn (từ 07:49 24/11) được cất ở đâu; bài trong kho đổi thì cập nhật thế nào; và bước kiểm khiến hệ thống thà không trả lời còn hơn trả lời bằng dữ liệu cũ.

## Ý chính

- **Qdrant** là cơ sở dữ liệu chuyên tìm vector. hue_rag cất cả 9.536 đoạn vào một **collection** duy nhất của nó; phần này gọi chung là **chỉ mục**.
- Mỗi lần lập chỉ mục, chương trình ghi một **bản ghi chỉ mục**: danh sách bài của kho kèm "dấu vân tay" của từng bài. Dấu vân tay đổi khi bài đổi dù chỉ một chữ.
- Mỗi lần bật, máy chủ so bản ghi đó với kho hiện có. **Lệch thì máy chủ vẫn chạy, nhưng mọi câu hỏi nhận lời báo "Dữ liệu tra cứu cần được lập chỉ mục lại."** Phép so chỉ chạy lúc bật: sửa kho khi máy chủ đang chạy thì nó vẫn trả lời theo chỉ mục cũ tới lần khởi động sau.
- Sửa vài bài thì không phải lập lại cả chỉ mục (khoảng 225 giây). Một lệnh **cập nhật riêng** chỉ tính lại vector cho đoạn có thay đổi: lần chạy thật đầu tiên mất 37,7 giây cho 105 đoạn, kết quả giống một lần lập lại toàn bộ. Lệnh tự dừng nếu máy chủ đang chạy; xong phải bật lại máy chủ.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| Qdrant | **Qdrant**, một **vector database** | cơ sở dữ liệu cất vector và tìm vector gần nhất |
| collection | **collection** | một "bảng" của Qdrant; hue_rag dùng đúng một collection |
| điểm | **point** | một bản ghi trong collection; mỗi đoạn của kho là một điểm |
| chỉ mục | **index** | toàn bộ dạng đã xử lý của kho để tìm: collection, file thống kê từ khoá, bản ghi chỉ mục |
| bản ghi chỉ mục | **build record** | file ghi lần lập chỉ mục: những bài nào, dấu vân tay từng bài, bao nhiêu đoạn, model nào |
| dấu vân tay | **hash** (SHA-256) | chuỗi ký tự tính từ nội dung một file; sửa một chữ là chuỗi đổi |
| hộp | **container** (của Docker) | một chương trình đang chạy cách ly trong Docker, mang sẵn mọi thứ nó cần; bản đóng gói để dựng ra hộp gọi là ảnh đóng gói (bài 36) |
| bản chụp | **snapshot** | bản sao của cả collection ở một thời điểm, để khôi phục khi cần |

## Mỗi đoạn là một điểm trong một collection của Qdrant

Qdrant chạy trên cùng máy với hệ thống, trong một hộp riêng, ở một phiên bản được ghi cố định. Dữ liệu của nó nằm trong một thư mục của dự án, nên tắt rồi bật lại vẫn còn nguyên. Máy tính mở lại thì Qdrant tắt (bài 36).

hue_rag dùng đúng một collection; tên của nó ghi luôn model embedding đã dùng. Collection có 9.536 điểm, bằng đúng số đoạn. Mỗi điểm gồm:

- một **mã** cố định, suy ra từ mã đoạn (bài 8);
- **vector** 384 con số của đoạn (bài 10);
- phần **từ khoá** của đoạn (bài 11);
- **hồ sơ 7 trường**: chữ để tìm, tên bài, đường tiêu đề, phần bằng chứng, nguồn, mã đoạn, chủ đề (bài 9).

Lúc trả lời, hệ thống gửi vector của câu hỏi cho Qdrant và nhận về 30 điểm gần nhất kèm hồ sơ của chúng. Mọi việc sau đó dùng hồ sơ vừa nhận, kể cả chữ đưa cho model; không hỏi lại Qdrant, không đọc lại file bài viết.

## Bản ghi chỉ mục ghi lại kho lúc chỉ mục được lập

Mỗi lần lập chỉ mục, chương trình ghi một file gọi là bản ghi chỉ mục: danh sách 269 bài của kho kèm **dấu vân tay của từng bài**; số đoạn (9.536) và số điểm đã cất; tên, phiên bản, số chiều của model embedding; dấu vân tay của file thống kê từ khoá (bài 11); cách đo độ gần và dạng hồ sơ của collection. Lúc bật máy chủ, file này là căn cứ để trả lời câu hỏi "chỉ mục có khớp với kho không".

## Bật máy chủ thì kiểm; lệch thì mọi câu hỏi nhận lời báo

Mỗi lần bật, trước khi nhận câu hỏi đầu tiên, máy chủ kiểm năm điều: bản ghi chỉ mục hợp lệ, **kho không đổi** (tính lại dấu vân tay từng bài, bắt được cả bài thêm, bài mất, bài sửa một chữ), file thống kê từ khoá khớp, collection khớp, model embedding chạy được (danh sách đầy đủ ở nửa để tra).

Sai ở điều 1 tới 4: máy chủ vẫn chạy, nhưng mọi câu hỏi nhận lời báo "Dữ liệu tra cứu cần được lập chỉ mục lại." Sai ở điều 5, hoặc không nối được tới Qdrant: mọi câu hỏi nhận "Hệ thống tra cứu tạm thời không khả dụng." Trong cả hai trường hợp, các trang không cần tìm trong kho (Bản đồ, Chỗ ở, Giới thiệu) vẫn dùng được.

Năm điều chỉ được kiểm một lần lúc bật. Trang kiểm tình trạng (địa chỉ người vận hành mở để xem hệ thống có ổn không) chỉ nhắc lại kết quả của lần kiểm đó, nên Qdrant ngừng giữa chừng thì nó vẫn báo "đủ" (bài 6).

## Sửa vài bài thì chỉ tính lại vector cho những đoạn đổi chữ

Lập lại cả chỉ mục mất khoảng 225 giây, khoảng 195 giây trong đó là tính vector cho cả kho; sửa một hai bài thì phần lớn công đó là thừa. Từ 22/11 có lệnh **cập nhật riêng**. Thấy máy chủ đang chạy thì nó dừng ngay, chưa đọc hay ghi gì; nếu không, nó cắt đoạn lại cả kho, **giữ nguyên vector** của đoạn không đổi (cả chữ lẫn số thứ tự), chụp collection rồi tính vector chỉ cho đoạn đổi, ghi lại phần từ khoá của **mọi** điểm, kiểm lại cả collection, và ghi bản ghi chỉ mục mới sau cùng (sáu bước đủ ở nửa để tra).

Hai điều đáng nhớ về lệnh này:

- **Đơn vị là đoạn, không phải bài.** Đổi 7 con số giá ở 7 đoạn thì đúng 7 đoạn được tính lại. Nhưng đoạn đánh số theo thứ tự trong bài, nên thêm dòng vào giữa bài làm các đoạn phía sau đổi số, và chúng cũng được tính lại.
- **Phần từ khoá của cả kho được ghi lại**, vì điểm từ khoá của mỗi đoạn phụ thuộc hai con số của cả kho: mỗi từ hiếm tới đâu, và một đoạn trung bình dài bao nhiêu. Ở một ca sửa giá, 69 điểm đổi phần từ khoá; ở ca thêm một bài mới, mọi điểm đổi.

Lần chạy thật đầu tiên, sáng 22/11, sau khi sửa hai bài về giá (giá thuê thuyền, vé cho người địa phương; bài 7): lệnh nhận ra đúng 2 bài, tính lại vector cho 105 đoạn, giữ nguyên 9.337 đoạn, mất 37,7 giây; kho từ 9.436 lên 9.442 đoạn (sau đó thêm một bài, thành 9.458).

Sau lệnh phải khởi động lại máy chủ; lúc bật nó nạp thống kê mới và bỏ các câu trả lời đang nhớ sẵn, trong đó có thể còn giá cũ.

## Quyết định và lý do

### 1. Vì sao cất chỉ mục trong Qdrant chạy trên cùng máy?

- **Đã chọn:** Qdrant trong một hộp riêng của dự án, phiên bản ghi cố định, chỉ nhận yêu cầu từ chính máy đó.
- **Vì sao:** quyết định đã ghi (12/08/2026, chủ dự án duyệt): Qdrant chạy trong một hộp riêng của dự án, dữ liệu riêng, ghi cố định đúng một phiên bản; không nhúng thẳng vào chương trình, không dùng bản trên mây, không lấy "bản mới nhất". Vì sao chọn Qdrant chứ không phải một cơ sở dữ liệu vector khác: chưa thấy ghi lý do. Điều thấy được: một điểm giữ được cả vector, phần từ khoá và hồ sơ của một đoạn.
- **Cách khác:** bản Qdrant nhúng thẳng trong chương trình, hoặc bản trên mây: chủ dự án đã loại ở quyết định 12/08, không đo. Một cơ sở dữ liệu vector khác: chưa thử, không có phép so.
- **Cái giá:** Qdrant là một thứ nữa phải bật. Nó tắt lúc máy chủ được bật thì phải bật Qdrant rồi khởi động lại máy chủ (mục "Nếu… thì sao").

### 2. Vì sao kho lệch chỉ mục thì máy chủ không trả lời câu nào?

- **Đã chọn:** máy chủ vẫn chạy, mọi câu hỏi nhận "Dữ liệu tra cứu cần được lập chỉ mục lại."; các trang không cần kho vẫn dùng được.
- **Vì sao:** đặc tả lúc dựng hệ thống ghi: kho đổi thì chưa phục vụ hỏi đáp, báo phải lập lại chỉ mục. Luật của sản phẩm là chỉ trả lời từ kho. Lập luận đứng sau: chỉ mục cũ cho câu trả lời trôi chảy, có số nguồn, mà có thể là giá cũ.
- **Cách khác:** chạy tiếp với chỉ mục cũ rồi báo "dữ liệu có thể đã cũ": không làm. Không cho máy chủ bật: không làm; tiêu chí nghiệm thu khâu viết ghi rằng lỗi thì máy chủ vẫn chạy ở tình trạng "thiếu" và từ chối hỏi đáp.
- **Cái giá:** sửa kho mà quên cập nhật chỉ mục thì từ lần khởi động sau, ô hỏi đáp ngừng hẳn.

### 3. Vì sao chỉ kiểm lúc bật, không kiểm ở mỗi câu hỏi?

- **Đã chọn:** năm điều chỉ kiểm một lần, khi máy chủ bật.
- **Vì sao:** chưa thấy ghi lý do. Điều thấy được: đặc tả ghi phép tính lại dấu vân tay là việc của lúc bật; phép đó đọc lại cả 269 file bài viết.
- **Cách khác:** kiểm ở mỗi câu hỏi, hoặc kiểm theo giờ: chưa thử.
- **Cái giá:** hai dòng đầu và dòng 4 của bảng "Nếu… thì sao" dưới đây.

### 4. Vì sao cập nhật riêng sửa ngay trong collection đang dùng, không lập sang collection mới?

- **Đã chọn:** sửa tại chỗ, chụp collection trước lần ghi đầu tiên.
- **Vì sao:** đã đo (mục "Đã so"): hai cách chỉ chênh khoảng 2,4 giây; lập sang collection mới phải sửa nhiều chỗ đang đọc tên collection, sửa tại chỗ thì không. Bản cũ được giữ bằng bản chụp.
- **Cách khác:** lập sang collection mới rồi chuyển: đã đo, không chọn. Lập lại toàn bộ (cách trước 22/11): vẫn dùng được khi cần.
- **Cái giá:** lệnh bị ngắt giữa lúc ghi thì collection đang dùng ở dạng dở dang. Chương trình dời bản ghi chỉ mục đi trước lần ghi đầu tiên, nên máy chủ bật sau đó thấy lệch và báo, không trả lời từ chỉ mục dở. Đặc tả lúc dựng hệ thống cấm ghi lẫn vào collection đang có; cách này đổi luật đó theo phương án chủ dự án chọn tối 21/11, bù bằng phép kiểm "giống hệt một lần lập lại toàn bộ".

### 5. Vì sao cập nhật là một lệnh chạy tay, và vì sao nó dừng khi máy chủ đang chạy?

- **Đã chọn:** người vận hành gõ lệnh (có chế độ chỉ xem trước); lệnh duyệt một đề xuất sửa giá thì tự gọi nó. Thấy máy chủ đang chạy thì cả hai lệnh dừng trước khi ghi.
- **Vì sao:** chủ dự án chọn cách "lệnh chạy tay sau khi duyệt" tối 21/11. Bản thiết kế ghi lý do: chưa có đường nào ghi kho tự động; số lấy từ web phải qua người đọc rồi mới vào kho. Đặc tả lúc dựng hệ thống đã ghi việc lập chỉ mục làm khi máy chủ dừng; việc lệnh tự dừng có từ một lần soát của model khác hãng 22/11: máy chủ đang chạy không kiểm lại, sẽ trả lời trên collection ghi dở.
- **Cách khác:** máy chủ tự cập nhật khi thấy kho đổi: không làm. Chỉ nhắc mà không chặn: cách cũ, bỏ 22/11.
- **Cái giá:** mỗi lần cập nhật kho, máy chủ tắt khoảng nửa phút cộng lúc bật lại.

Ba quyết định nhỏ hơn nằm ở nửa để tra.

## Nếu… thì sao

Dòng **(đã thử)**: thử thật trưa 22/11 (bài 6); các dòng khác đọc từ chương trình. Lời báo trong ngoặc kép là nguyên văn.

| Nếu | Hệ thống làm gì | Người dùng thấy gì | Đã có chưa / ai làm gì |
|---|---|---|---|
| kho đã sửa, chỉ mục chưa cập nhật, rồi máy chủ khởi động lại | máy chủ vẫn chạy, không trả lời câu nào | "Dữ liệu tra cứu cần được lập chỉ mục lại." ở mọi câu hỏi | người vận hành tắt máy chủ, chạy lệnh cập nhật riêng, bật lại |
| sửa kho trong lúc máy chủ đang chạy | trả lời theo chỉ mục cũ, kể cả câu đã nhớ | câu trả lời theo bản cũ, không lời báo | tắt máy chủ, cập nhật chỉ mục, bật lại |
| Qdrant chưa chạy lúc máy chủ được bật **(đã thử)** | máy chủ vẫn bật; không nối lại Qdrant sau đó | "Hệ thống tra cứu tạm thời không khả dụng." ở mọi câu hỏi | bật Qdrant, rồi **khởi động lại máy chủ**; lệnh bật một phát làm đúng thứ tự này |
| Qdrant ngừng giữa lúc máy chủ đang chạy **(đã thử)** | câu hỏi mới lỗi sau khoảng 2 giây; câu đã nhớ vẫn được trả lại; đường báo tình trạng vẫn báo đủ | "Hệ thống tra cứu tạm thời không khả dụng." và nút "Thử lại" | bật lại Qdrant; hỏi lại được ngay, không cần khởi động lại máy chủ |
| lệnh cập nhật bị ngắt giữa lúc ghi | máy chủ bật sau đó thấy lệch | "Dữ liệu tra cứu cần được lập chỉ mục lại." | chạy lại chính lệnh đó; nó kéo về đúng (đã thử hai ca trên bản chép) |
| sau khi cập nhật, một đoạn mà bảng điểm trang Lên kế hoạch dùng đã đổi mã | máy chủ không bật, báo đoạn nào thiếu | không vào được trang nào | người vận hành sửa bảng điểm cho khớp mã mới rồi bật lại (bài 6, 7) |

## Dễ nhầm

- **"Sửa bài trong kho là câu trả lời đổi ngay."** Không. Phải tắt máy chủ, cập nhật chỉ mục rồi bật lại.
- **"Qdrant chứa kho."** Qdrant chứa dạng đã xử lý của kho. Kho gốc là 269 file bài viết; mất Qdrant thì lập lại được từ kho, mất kho thì không.
- **"Cập nhật riêng chỉ đụng tới bài đã sửa."** Đúng với vector; phần từ khoá thì mọi điểm được ghi lại.

## Câu hỏi tự kiểm

<details>
<summary>1. Kho đã sửa mà chưa cập nhật chỉ mục. Máy chủ đang chạy thì sao, khởi động lại thì sao?</summary>

Đang chạy: máy chủ không biết, vẫn trả lời theo chỉ mục cũ. Khởi động lại: phép so lúc bật thấy lệch, máy chủ vẫn chạy nhưng mọi câu hỏi nhận "Dữ liệu tra cứu cần được lập chỉ mục lại."

</details>

<details>
<summary>2. Vì sao không cho máy chủ trả lời tiếp bằng chỉ mục cũ, kèm một dòng "dữ liệu có thể đã cũ"?</summary>

Luật của sản phẩm là chỉ trả lời từ kho; chỉ mục cũ cho câu trả lời có số nguồn hẳn hoi mà có thể là giá đã sửa.

</details>

<details>
<summary>3. Sửa 7 con số giá trong một bài thì lệnh cập nhật riêng tính lại những gì?</summary>

Vector: chỉ đoạn đổi chữ hoặc đổi số thứ tự (ca thử: đúng 7). Phần từ khoá: mọi điểm, vì nó phụ thuộc thống kê của cả kho.

</details>

<details>
<summary>4. Qdrant tắt lúc bật máy chủ và Qdrant ngừng giữa chừng: cách chữa khác nhau thế nào?</summary>

Tắt lúc bật: máy chủ chỉ nối tới Qdrant lúc bật, nên phải bật Qdrant rồi khởi động lại máy chủ. Ngừng giữa chừng: bật lại Qdrant là hỏi được ngay.

</details>

## Cấu hình đang chạy

*Chép từ hệ thống đang chạy sáng 22/11/2026. Cấu hình đổi thì mục này phải chép lại.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Phần mềm | Qdrant, chạy trong một hộp Docker, ghi cố định một phiên bản | bật lại vẫn đúng phiên bản đó | chưa so với cơ sở dữ liệu vector khác |
| Địa chỉ | chỉ nghe trên chính máy đó, cổng 6335 | máy khác không gọi thẳng vào được | — |
| Nơi giữ dữ liệu | thư mục `qdrant_storage/` của dự án | tắt hộp không mất dữ liệu | — |
| Tên collection | `hue_full_corpus_7a2_e5_small_384` | tên ghi luôn model embedding và số chiều | — |
| Số điểm | 9.536 | bằng số đoạn | — |
| Vector trong mỗi điểm | 384 con số, đo bằng cosine | bài 10 | bài 10 |
| Cách Qdrant tìm | gần đúng (HNSW), cấu hình mặc định | nhanh | đã so với tìm chính xác: giống hệt ở 108 trên 108 câu (kho cuối tháng 10) |
| Chỉ mục phụ để lọc theo trường | không có | đường tìm câu trả lời không lọc theo trường (bài 9); riêng trang Lên kế hoạch có lấy đoạn theo mã đoạn | chưa thử |
| Hạn chờ một lời gọi Qdrant | 30 giây | — | chưa so |
| Số điểm ghi mỗi lô lúc lập chỉ mục | 64 | chỉ ảnh hưởng tốc độ lập | chưa so |
| Bản ghi chỉ mục và file thống kê | hai file cạnh nhau, hệ thống đọc lúc khởi động | căn cứ của phép kiểm lúc khởi động | — |

## Đã so

**Vấn đề thật đã gặp.** Trước 22/11, sửa một chữ trong kho là phải tắt hệ thống, xoá collection và lập lại toàn bộ, khoảng 4 phút. Chủ dự án nêu yêu cầu: khi một bài đổi thì chỉ tính lại phần của bài đó.

**So gì.** Hai cách làm cùng mục tiêu, đo thời gian từng bước trên một bản chép của collection thật (9.436 điểm lúc đó):

| Bước | Giây |
|---|---|
| Cắt đoạn cả kho và lập thống kê từ khoá (cách nào cũng phải làm) | 21,1 |
| Tính vector cho cả kho (cách cũ) | ước khoảng 195 |
| Ghi lại phần từ khoá của mọi điểm (cách sửa tại chỗ) | 1,8 |
| Chép mọi điểm sang một collection mới (cách "lập sang collection mới rồi chuyển") | 4,2 |

**Đọc bảng này thế nào.**
- Cả hai cách mới đều bỏ được 195 giây tính vector thừa. Chúng chỉ chênh nhau khoảng 2,4 giây, nên thời gian không phải lý do chọn.
- Cách chuyển collection giữ được bản cũ nguyên vẹn, nhưng phải sửa nhiều chỗ của hệ thống đang đọc tên collection. Cách sửa tại chỗ không đụng dòng nào của hệ thống.
- Thứ cách sửa tại chỗ thiếu (bản cũ còn nguyên) được bù bằng một bản chụp collection trước mỗi lần ghi.

**Đã chọn: sửa tại chỗ.**

**Kiểm kết quả.** Một phiên khác, bằng chương trình riêng, so chỉ mục sau lần cập nhật thật với một bản lập lại toàn bộ từ cùng kho. Bốn phép đều đạt:

| Phép kiểm | Kết quả |
|---|---|
| Cùng số điểm; chữ và phần từ khoá giống hệt; vector lệch lớn nhất | 9.442 điểm; giống hệt; 0,00000015 |
| So với chỉ mục trước khi sửa | 9.337 điểm không đổi chữ giữ nguyên vector từng byte; mọi điểm đổi thuộc đúng 2 bài đã sửa |
| File thống kê từ khoá và bản ghi chỉ mục | giống bản lập lại |
| 176 câu hỏi mẫu | cùng 10 đoạn, cùng thứ tự; 0 câu lệch |

**Giới hạn của phép đo.** Phép kiểm độc lập mới làm cho lần chạy thật đầu tiên (2 bài). Lần chạy thật thứ hai, lúc 10:02 ngày 22/11 khi kho thêm một bài mới, chưa có phép so như vậy. Trước đó có sáu ca thử trên một bản chép của collection và của kho, gồm hai ca cố ý ngắt lệnh giữa chừng rồi chạy lại.

## Quyết định nhỏ hơn

**Vì sao tên collection ghi luôn tên model embedding?** Chủ dự án chọn cách đặt tên này từ 12/08; đặc tả lúc dựng hệ thống ghi thêm: mỗi model embedding ứng viên có một collection riêng, để chỉ mục của các model không lẫn nhau khi so. Cái giá: đổi model là lập một collection mới và lập lại toàn bộ.

**Vì sao ghi lại phần từ khoá của mọi điểm, khi cách tìm đang chạy không đọc nó?** Cách tìm đang chạy tự tính điểm từ khoá lúc hỏi, từ chữ của đoạn và file thống kê; với câu trả lời, thứ phải đúng là file thống kê. Để collection sau cập nhật giống hệt một lần lập lại toàn bộ (đó là phép kiểm bắt buộc chủ dự án chọn cùng phương án), và để cách tìm thứ hai đang không dùng vẫn đúng nếu được bật. Tốn khoảng 2 giây.

**Vì sao Qdrant tìm gần đúng mà không tìm chính xác?** Đã so trên kho cuối tháng 10: giống hệt ở 108 trên 108 câu; giữ cấu hình mặc định.

## Giới hạn đã biết

- **Phải tắt máy chủ trước khi cập nhật** và bật lại sau. Lệnh tự dừng nếu thấy cổng của máy chủ đang mở; nó chỉ kiểm một cổng cố định, nên máy chủ chạy ở cổng khác thì không bị bắt (đọc từ chương trình).
- **Lệnh bị ngắt từ lúc bắt đầu ghi vào Qdrant trở đi thì máy chủ bật sau đó không trả lời câu nào** cho tới khi lệnh được chạy lại. Đây là cố ý. Ngắt trước đó (lúc cắt đoạn, lúc chụp) thì chưa có gì bị đổi.
- **Sửa đúng một câu mà quy tắc gắn lưu ý đang ghi nguyên văn** (3 câu ở 2 bài, bài 8) thì lệnh dừng ngay ở bước cắt đoạn; phải sửa quy tắc cho khớp rồi chạy lại.
- **Bản chụp trước khi ghi nằm bên trong hộp Qdrant;** tạo lại hộp là mất. Đường lùi cuối cùng vẫn là lập lại toàn bộ từ kho.
- **Bản ghi chỉ mục giữ dấu vân tay của bài, không giữ dấu của chương trình cắt đoạn.** Đổi cách cắt đoạn mà không lập lại chỉ mục thì phép kiểm không bắt được (suy ra từ chương trình).
- **Kho lớn gấp nhiều lần** thì bước cắt đoạn lại cả kho (21 giây hiện nay) sẽ thành phần chính của lệnh cập nhật.

## Chi tiết để tra

- Năm điều kiểm lúc bật, theo thứ tự: (1) bản ghi chỉ mục có tồn tại, đã hoàn tất, đúng tên collection, đúng model và phiên bản, số điểm bằng số đoạn; (2) tính lại dấu vân tay của từng bài trong kho, so với bản ghi; (3) file thống kê từ khoá khớp; (4) collection có tồn tại, đúng cấu trúc, đúng số điểm; (5) nạp model embedding và tính thử một vector.
- Sáu bước của lệnh cập nhật riêng: (1) cắt đoạn lại cả kho, không cần model, khoảng 21 giây; (2) so từng đoạn với điểm trong collection, đoạn giống hệt giữ nguyên vector; (3) chụp collection, tính vector mới cho đoạn đổi, xoá điểm không còn ứng với đoạn nào; (4) ghi lại phần từ khoá của mọi điểm, khoảng 2 giây; (5) kiểm lại cả collection bằng phép kiểm của lúc lập chỉ mục; (6) ghi file thống kê từ khoá, rồi bản ghi chỉ mục sau cùng.

- Các ca thử trên bản chép: không sửa gì, 22,9 giây · đổi 7 con số giá, 7 đoạn, 25,5 giây · thêm một bài mới, 36 đoạn, 28,2 giây · bỏ một mục ở giữa bài, 84 đoạn tính lại và 8 điểm bị xoá, 27,2 giây · hai ca ngắt lệnh giữa chừng rồi chạy lại, về đúng.
- Trong lần chạy thật, 105 đoạn gồm 6 đoạn mới và 99 đoạn đổi chữ hoặc đổi số thứ tự (bài giá thuê thuyền thêm nhiều dòng nên các đoạn phía sau dịch số).
- Vector lệch 0,00000015 giữa hai cách là do model tính theo lô; mức này không đổi thứ hạng tìm.
- Bản chụp collection: khoảng 0,2 giây, 63 MB; khôi phục từ bản chụp đã thử: 0,3 giây.
- Cách lùi một lần sửa kho: hoàn lại bài rồi chạy lại chính lệnh cập nhật; nó kéo chỉ mục về khớp kho cũ.
- Lệnh có chế độ "chỉ xem": in bài nào khác chỉ mục và số đoạn sẽ tính lại, không ghi gì; chế độ này chạy được cả khi máy chủ đang bật.
- Hai mã lỗi của hệ thống khi không sẵn sàng: 409 (kho lệch chỉ mục) và 503 (Qdrant hoặc model embedding không chạy). Trang kiểm tình trạng vẫn trả lời, báo trạng thái "degraded".
- Lệnh soạn bản đề xuất khi một giá đổi (tìm mọi chỗ trong kho còn ghi giá cũ) là bước đứng trước lệnh cập nhật này; nó thuộc bài 7.

**Bài sau (bài 13):** hết chặng chuẩn bị. Chặng 3 bắt đầu từ lúc người dùng gõ câu hỏi: 30 ứng viên và hai bảng xếp hạng được trộn thành 10 đoạn như thế nào.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Qdrant trong Docker, ghi cố định bằng mã băm của ảnh, cổng `127.0.0.1:6335`, thư mục `qdrant_storage/`: `docker-compose.yml` [đọc 22/11/2026]. Địa chỉ và hạn 30 giây: `backend/config/settings.yaml` mục `vector_database`.
- Tên collection, 9.479 điểm, cosine, tên vector, dạng hồ sơ: `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` và số điểm Qdrant, đọc 16:35 22/11/2026 [đã chạy]. Cấu trúc collection (không chỉ mục phụ, HNSW mặc định): `backend/vectorstore/qdrant.py` [code].
- Hồ sơ nhận về khi tìm và việc chấm từ khoá dùng hồ sơ đó: `backend/retrieval/full_corpus.py`, hàm `search` [code].
- Năm điều kiểm lúc khởi động, mã 409 `corpus_reingest_required` / 503, trạng thái "degraded": `backend/retrieval/full_corpus.py` (`build_full_corpus_retrieval_service`, `verify_full_corpus_record_freshness`), `backend/api/app.py`, `backend/api/health.py` [code; thứ tự năm điều chép qua `bai_hoc/05_QDRANT.md`, bài đã qua kiểm độc lập].
- Lệnh cập nhật riêng (sáu việc, sửa tại chỗ, đơn vị là đoạn, ghi lại từ khoá cả kho, bản chụp, ngắt giữa chừng, chế độ chỉ xem): `backend/ingestion/cap_nhat_rieng.py`; `guides/RUNBOOK_BAN_GIAO.md` mục 5b; `report_agent/2026-11-22/c_cap_nhat_rieng.md` [code + đã chạy, phiên khác].
- Bảng thời gian từng bước (21,1 · 195 · 1,8 · 4,2 giây) và lý do chọn sửa tại chỗ: `report_agent/2026-11-22/c_cap_nhat_rieng.md` mục 2 [đã chạy 08:27 22/11].
- Lần chạy thật (2 bài, 105 đoạn = 6 + 99, giữ 9.337, 37,7 giây, 9.436 ⇒ 9.442), bốn phép kiểm độc lập, sáu ca trên bản chép: `bai_hoc/VIEC_MOI_XONG.md` mục 32 [máy kiểm + người thứ hai kiểm, 22/11].
- HNSW giống tìm chính xác 108 / 108: `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` thẻ N2-15 = T3-04 [đã chạy, kho cũ].
- Lô 64 điểm lúc lập chỉ mục: `backend/ingestion/full_corpus_pipeline.py` qua `bai_hoc/05_QDRANT.md` [chép].
- Yêu cầu của chủ dự án và quyết định "lệnh chạy tay sau khi duyệt": `session_prompt/HIEN_TRANG.md` mục 4, gạch 22:22 và 22:45 21/11/2026. Luật "chỉ trả lời từ kho": cùng file, phần "Sản phẩm".
- Hai giới hạn "sửa kho lúc đang chạy" và "đổi chương trình cắt đoạn": suy ra từ chương trình, chưa thử (theo `bai_hoc/05_QDRANT.md`); câu "máy chủ đang chạy chỉ kiểm bản ghi một lần lúc bật" có ghi trong chú thích đầu `backend/ingestion/cap_nhat_rieng.py` [code].
- Mục "Quyết định và lý do", "Nếu… thì sao", "Câu hỏi tự kiểm", "Quyết định nhỏ hơn" (thêm 13:53 22/11/2026 theo khuôn mới): lời báo nguyên văn `backend/api/app.py` (`retrieval_error_message`) và `backend/api/routes/chat.py` (`_retrieval_not_ready`) [code]; đặc tả "kho đổi ⇒ chưa phục vụ hỏi đáp", "số nguồn dùng bằng chứng cất cùng chỉ mục", "kiểm lúc bật", "mỗi model một collection", "không ghi lẫn vào collection đang có; lập lại khi máy chủ dừng": `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md` mục 3 và 6 [chép]; quyết định 12/08/2026 (hộp Docker riêng, ghi cố định phiên bản, không nhúng / không bản trên mây / không "mới nhất"; tên collection mang tên model): `guides/phase_4_qdrant_ingestion.md` dòng 746–759 [chép]; tiêu chí "lỗi thì máy chủ chạy ở tình trạng thiếu, hỏi đáp báo 503": `guides/phase_6_generation_api.md` dòng 912 [chép]; bảng điểm Lên kế hoạch kiểm lúc bật, ngoài khối bắt lỗi: `backend/api/app.py` khoảng dòng 153–156 [code]; lệnh dừng khi cổng 8010 mở (`ServerDangChay`), bản ghi dời sang tên `.dang_cap_nhat` trước lần ghi đầu: `backend/ingestion/cap_nhat_rieng.py`, `backend/ops/duyet_sua_kho.py`, commit `cb2c2988` [code]; lý do duyệt tay: `data/phase_12_agent_sua_kho_2026-11-21/NHAP_THIET_KE.md` bảng rủi ro, dòng "đầu độc kho" [riêng tư, chép]; ba ca Qdrant **(đã thử)**: `06_KIEN_TRUC.md` mục "Mọi tình huống hỏng của bài này" và chú thích đầu `scripts/bat_he_thong.sh` [đã chạy 12:07–12:16 22/11, phiên đo]. "Chưa thấy ghi lý do" ở quyết định 1 (chỉ cho việc chọn Qdrant thay vì cơ sở dữ liệu khác) và 3: đã dò `docs/superpowers/specs/`, `guides/phase_4_qdrant_ingestion.md`, `HIEN_TRANG.md`, chú thích `backend/api/app.py`. Các mục mới đã qua một lượt đối chiếu độc lập 14:28 22/11/2026 và được sửa theo: `data/hoc_cung_D/kiem/muc_moi_12_16.md` [riêng tư].
- Quét số cũ 20:46 23/11/2026: các câu nói số kho hiện tại ("Bài này thêm", Từ dùng, cấu tạo collection, bản ghi chỉ mục, "Vì sao" của bước kiểm lúc bật, "Dễ nhầm", hàng "Số điểm"): 267 ⇒ 269 bài, 9.479 ⇒ 9.533 đoạn / điểm; số của lần cập nhật chỉ mục sáng 22/11 giữ nguyên. Lệnh: `corpus.file_count` / `corpus.chunk_count` / `qdrant.point_count` của `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` (269 / 9533 / 9533), đọc 20:40–20:45 23/11/2026 [đã chạy].

</details>
