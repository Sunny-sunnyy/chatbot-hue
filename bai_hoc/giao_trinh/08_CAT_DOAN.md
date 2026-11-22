# Bài 8 — Cắt bài thành đoạn (chunking)

*Cập nhật 15:13, ngày 22/11/2026 · cách cắt đọc từ chương trình đang chạy; số đoạn đếm sáng 22/11, khớp bản ghi hiện trạng lúc 13:33; số của phép so lấy từ báo cáo đo cuối tháng 10; người viết không chạy lại phép đo nào.*

**Bài trước đã biết:** kho là 266 bài viết về Huế, mỗi bài là một file chữ có tiêu đề và các mục.
**Bài này thêm:** bước đầu tiên của giai đoạn chuẩn bị: cắt 266 bài thành 9.458 đoạn. Cắt ở đâu, mỗi đoạn dài bao nhiêu, vì sao đoạn to hơn lại cho kết quả tệ hơn, và một đoạn hỏng thì sao.

## Ý chính

- Model viết không đọc cả bài, chỉ đọc các **đoạn**: 10 đoạn ở lần tìm đầu; trợ lý được tìm thêm tối đa 3 lần; tin nhiều ý được nối thêm 2 đoạn mỗi ý. Vì vậy bài phải được cắt sẵn thành đoạn, và mỗi đoạn phải tự đủ nghĩa.
- hue_rag cắt **theo cấu trúc của bài**: mỗi đoạn văn, mỗi mục danh sách, mỗi bảng ngắn là một đoạn. Không cắt theo số ký tự, không cắt giữa câu.
- Bảng dài được tách **từng dòng**, và mỗi dòng mang theo **dòng tiêu đề của bảng**, để một con số giá luôn đi cùng tên cột của nó.
- Không đoạn nào được dài quá giới hạn mà model embedding đọc được (512 token; giới hạn thật lúc cắt còn chặt hơn). Chương trình kiểm mọi đoạn; một đoạn sai là cả bước chuẩn bị dừng.
- Đã thử 12 cách cắt khác. Gộp thành đoạn to (từ 256 token trở lên) làm mất đáp án ở 4 tới 6 trên 32 câu; gộp nhỏ (tới 128 token) thì không khác. Cách giải thích của nhóm, chưa đo riêng: cùng một lượng chữ thì ít đoạn hơn, model viết thấy ít chỗ của kho hơn.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| đoạn | **chunk** | một mẩu của bài sau khi cắt; đơn vị nhỏ nhất mà hệ thống tìm và đưa cho model viết |
| cắt đoạn | **chunking** | việc chia mỗi bài thành các đoạn |
| khối | **block** (của Markdown) | một phần tự nhiên của bài: một đoạn văn, một mục danh sách, một bảng, một đoạn trích |
| token | **token** | đơn vị model dùng để đếm độ dài chữ (bài 1) |
| gối đầu | **overlap** | cách cắt cho hai đoạn liền nhau lặp lại vài câu của nhau; hue_rag không dùng |
| mã đoạn | **chunk_id** | tên riêng của mỗi đoạn: đường dẫn file của bài kèm số thứ tự của đoạn trong bài (đếm từ 0) |

## Model viết chỉ đọc vài đoạn, nên mỗi đoạn phải tự đủ nghĩa

Ở ví dụ chính, câu hỏi về giá vé Đại Nội được trả lời từ 10 đoạn lấy ra ở 3 bài khác nhau. Model viết không thấy phần còn lại của 3 bài đó. Nó chỉ thấy đúng 10 mẩu chữ.

Từ đó có hai yêu cầu cho việc cắt. Thứ nhất, đoạn phải **nhỏ**, để 10 đoạn trỏ tới được nhiều chỗ khác nhau của kho. Thứ hai, mỗi đoạn phải **đọc riêng vẫn hiểu**: một con số không được rời khỏi thứ nói nó là số gì.

## Chương trình cắt theo cấu trúc của bài, không cắt theo số ký tự

Chương trình đọc từng bài và nhận ra các **khối** tự nhiên: đoạn văn, mục danh sách, bảng, đoạn trích. Tiêu đề các mục không thành đoạn riêng; chúng được ghi lại để gắn vào các đoạn nằm dưới (bài 9). Rồi chương trình theo bốn luật:

1. **Mỗi khối là một đoạn**, nếu khối đó không dài quá giới hạn. Một đoạn văn là một đoạn. Một mục danh sách là một đoạn. Một bảng ngắn là một đoạn.
2. **Bảng dài quá giới hạn thì tách từng dòng**, mỗi dòng mang theo dòng tiêu đề của bảng.
3. **Mục danh sách có mục con mà dài quá giới hạn** thì tách từng mục con, mỗi mục con giữ lại nhãn của mục cha.
4. **Đoạn văn dài quá giới hạn** thì tách ở ranh giới giữa hai câu. Không bao giờ cắt giữa câu.

**Không gối đầu.** Gối đầu là cách chữa cho lối cắt theo số ký tự: vì có thể cắt ngang một ý nên người ta cho hai đoạn liền nhau lặp lại vài câu. Ở đây chương trình cắt đúng ở những ranh giới mà người soạn bài đã đặt, không cắt ngang ý nào, nên không cần lặp.

## Dòng bảng luôn mang theo dòng tiêu đề của bảng

Ví dụ thật, ngay trong 10 đoạn của ví dụ chính. Bài về vé tham quan Quần thể Di tích Cố đô có một bảng giá vé gộp nhiều điểm. Bảng dài quá giới hạn nên được tách từng dòng. Đoạn số 5 mà model viết nhận được trông như sau (đã rút gọn tên cột):

```text
| Tên loại vé … | Các điểm … | Thời hạn … | Giá người lớn | Giá trẻ em 7–12 tuổi | Mức tiết kiệm … |
| Gộp 3 điểm: Tuyến A | Đại Nội, Minh Mạng, Khải Định | trong ngày | 420.000 đ | 80.000 đ | 80.000 đ |
```

Đoạn số 6 là một dòng khác của cùng bảng (vé gộp 4 điểm), cũng mang đúng dòng tiêu đề đó. Nhờ vậy khi đọc "420.000", model biết đó là giá người lớn của vé gộp 3 điểm, và câu trả lời viết đúng: "Tuyến A gồm Đại Nội, Lăng Minh Mạng và Lăng Khải Định, dùng trong ngày. Giá là 420.000 đồng/người lớn…".

Nếu cắt theo số ký tự, dòng tiêu đề có thể rơi vào một đoạn khác, và ba con số 420.000, 80.000, 80.000 đứng cạnh nhau mà không ai biết số nào là gì.

## Không đoạn nào dài quá giới hạn của model embedding

"Dài quá giới hạn" được đo bằng token. Model embedding (bài 10) đọc được tối đa 512 token một lần; phần vượt quá bị bỏ đi mà không báo. Vì vậy chương trình đếm độ dài mỗi đoạn bằng chính bộ đếm token của model, không ước theo số chữ.

Giới hạn thật lúc cắt còn chặt hơn 512. Trong cấu hình còn hai model ứng viên từ thời chọn model, và mỗi đoạn phải vừa giới hạn của **cả ba**; chặt nhất là 256 token của một model tiếng Việt. Đã thử chỉ giữ giới hạn 512 của model đang dùng: số đoạn ít đi 61 và kết quả tìm không khác. Tức hai giới hạn cũ bỏ được; chúng chưa được dọn vì dọn là phải lập lại cả chỉ mục.

Trên thực tế phần lớn đoạn ngắn hơn giới hạn nhiều. Số đo trên kho cuối tháng 10 (cách cắt từ đó tới nay không đổi): một nửa số đoạn ngắn hơn khoảng 85 token, tức cỡ một hai câu; đoạn dài nhất là 366 token theo bộ đếm của model đang dùng, và 255 trên 256 theo bộ đếm của model có giới hạn chặt nhất.

## Mỗi đoạn mang vị trí trong bài gốc và một mã cố định, và một lỗi là dừng

Mỗi đoạn mang theo ba thứ:

- **Phần bằng chứng:** các mảnh chữ làm nên đoạn (thân đoạn, dòng tiêu đề bảng nếu có), mỗi mảnh kèm vị trí bắt đầu và kết thúc chính xác trong bài gốc. Khi người dùng bấm xem nguồn, hệ thống lấy đúng mảnh chữ trong bài, không phải chữ đã ghép lại.
- **Chữ để tìm:** tên bài, tên các mục chứa đoạn, và phần bằng chứng, ghép lại. Đây là thứ được đổi thành vector và từ khoá (bài 9, 10, 11).
- **Mã đoạn:** đường dẫn file của bài kèm số thứ tự của đoạn. Cắt lại trên cùng một kho thì ra đúng các đoạn cũ với đúng mã cũ.

Cắt xong, chương trình kiểm lại **mọi** đoạn: đoạn nào vượt giới hạn, hoặc mảnh bằng chứng nào không khớp từng chữ với bài gốc ở đúng vị trí đã ghi, là lỗi. Chỉ cần một lỗi thì cả bước chuẩn bị dừng lại; không có chuyện bỏ qua đoạn lỗi rồi chạy tiếp.

## Quyết định và lý do

### 1. Vì sao cắt theo các khối của bài, không cắt đều theo số ký tự có gối đầu?

- **Đã chọn:** mỗi khối của bài là một đoạn; khối dài thì tách ở ranh giới dòng bảng, mục con hoặc câu; không gối đầu.
- **Vì sao:** lý do thiết kế ghi ở hồ sơ chia đoạn: bài trong kho soạn theo mẫu, có mục và bảng rõ ràng, nên ranh giới ý đã có sẵn; cắt theo số ký tự có thể tách con số khỏi dòng tiêu đề bảng. Gối đầu chỉ cần khi có thể cắt ngang một ý.
- **Cách khác:** cắt đều 400 ký tự (một bản thử hồi tháng 8): chưa so trực tiếp với cách hiện nay. Gối đầu: chưa so.
- **Cái giá:** nhiều đoạn rất ngắn: gần 1.800 đoạn dưới 50 token (kho cuối tháng 10), ít chữ để so nghĩa.

### 2. Vì sao giữ đoạn nhỏ, không gộp thành đoạn to cho model có đủ ý?

- **Đã chọn:** giữ đoạn nhỏ như khối của bài.
- **Vì sao:** đã đo (mục "Đã so"): cùng một lượng chữ, gộp tới 256, 384, 512 token làm mất đáp án ở 4 tới 6 trên 32 câu; mở rộng ra cả mục mất 8 câu.
- **Cách khác:** gộp tới 128 token: không khác, nên không đổi. Đưa cả bài thay cho từng đoạn (19/11): dừng sớm vì đắt gấp 5,5 lần và lấy nhầm dòng cảnh báo của một hoạt động khác trong cùng bài (bài 13).
- **Cái giá:** một ý trải dài nhiều khối phải được tìm ra từng mảnh.

### 3. Vì sao dòng bảng dài được tách riêng, và mỗi dòng mang theo dòng tiêu đề?

- **Đã chọn:** bảng vừa giới hạn thì là một đoạn; bảng dài thì mỗi dòng một đoạn, kèm dòng tiêu đề của bảng.
- **Vì sao:** lý do ghi ở hồ sơ chia đoạn: con số phải luôn đi cùng tên cột của nó (ví dụ "420.000" ở mục trên).
- **Cách khác:** gộp các dòng bảng liền nhau: đã đo, không khác.
- **Cái giá:** mỗi dòng giá là một đoạn rất ngắn; câu hỏi viết khác chữ với dòng đó thì bước tìm dễ bỏ sót.

### 4. Vì sao giới hạn lúc cắt là 256 token, khi model đang dùng đọc được 512?

- **Đã chọn:** mỗi đoạn phải vừa giới hạn của cả ba model ghi trong cấu hình; chặt nhất là 256 token.
- **Vì sao:** hai giới hạn kia còn lại từ thời chọn model. Đã thử chỉ giữ 512: ít đi 61 đoạn, kết quả tìm không khác. Chưa dọn, vì dọn là phải lập lại cả chỉ mục.
- **Cách khác:** chỉ giữ 512: đã đo, bỏ được.
- **Cái giá:** 61 đoạn ở 14 bài bị tách thêm mà không cần.

### 5. Vì sao một đoạn sai là dừng cả bước chuẩn bị, không bỏ qua đoạn đó mà chạy tiếp?

- **Đã chọn:** cắt xong kiểm mọi đoạn; một đoạn vượt giới hạn, hoặc một mảnh bằng chứng không khớp bài gốc, là dừng.
- **Vì sao:** lý do ghi trong chương trình: model embedding cắt im lặng phần vượt 512 token, nên một đoạn quá dài sẽ bị tính vector thiếu mà không ai biết. Với mảnh bằng chứng: chưa thấy ghi lý do. Điều thấy được: khi người dùng bấm xem nguồn, hệ thống lấy chữ theo đúng vị trí đã ghi.
- **Cách khác:** bỏ qua đoạn lỗi: không làm.
- **Cái giá:** sửa kho mà tạo ra một đoạn sai thì không cập nhật được chỉ mục cho tới khi sửa xong bài.

### 6. Vì sao chương trình cắt theo luật, mà không nhờ model cắt theo nghĩa?

- **Đã chọn:** chương trình cắt theo bốn luật, lúc chuẩn bị kho.
- **Vì sao:** chưa thấy ghi lý do. Điều thấy được: cắt lại trên cùng một kho thì ra đúng các đoạn cũ với đúng mã cũ, và có một bài test kiểm điều đó; việc cập nhật riêng vài bài (bài 12) dựa vào chính điều này để biết đoạn nào giữ nguyên.
- **Cách khác:** model cắt theo nghĩa: chưa thử.
- **Cái giá:** chất lượng đoạn phụ thuộc cách người soạn chia mục; bài đặt mục kém thì đoạn kém.

## Nếu… thì sao

Đọc từ chương trình và hồ sơ; người viết chưa thử lại.

| Nếu | Hệ thống làm gì | Người dùng thấy gì | Đã có chưa / ai làm gì |
|---|---|---|---|
| một khối cắt xong vẫn vượt giới hạn, hoặc một mảnh bằng chứng lệch bài gốc | bước chuẩn bị dừng trước khi ghi gì vào chỉ mục | máy chủ đang chạy: không đổi gì. Khởi động lại trước khi sửa xong: lời báo cần lập chỉ mục lại (bài 7) | người sửa bài viết lại khối đó cho ngắn rồi chạy lại |
| sửa đúng một câu mà quy tắc gắn lưu ý đang chép nguyên văn (3 câu ở 2 bài) | lệnh cập nhật dừng ở bước cắt, chưa ghi gì | không đổi gì | sửa file quy tắc cho khớp rồi chạy lại (bài 12) |
| thêm một dòng giữa bài | các đoạn phía sau của chính bài đó đổi mã và được tính lại vector | thường không thấy gì khác. Riêng bài có điểm trong bảng điểm của trang Lên kế hoạch: mã đoạn mô tả dịch số thì máy chủ không bật được ở lần bật sau | đã có; với bài có điểm trong bảng thì phải sửa bảng điểm (bài 6). Khi so trước và sau phải so theo nội dung, không theo mã |
| câu hỏi viết khác chữ với một dòng bảng ngắn | bước tìm dễ bỏ sót dòng đó | có thể nhận câu từ chối dù kho có | gốc ở bước tìm (bài 13); gộp dòng bảng đã thử, không giúp |
| đổi model embedding | đổi qua file cấu hình: máy chủ không bật, vì chương trình chỉ nhận đúng model đang dùng. Giới hạn lúc cắt lấy theo danh sách ba model trong cấu hình, không theo model đang chạy | — | phải sửa chương trình kiểm, sửa danh sách giới hạn, rồi cắt lại và dựng lại toàn bộ chỉ mục (bài 10); chưa ai làm |
| kho lớn gấp mười | mỗi lần cập nhật vẫn cắt lại cả kho | — | bước cắt (khoảng 21 giây hiện nay) thành phần chính của lần cập nhật (bài 7) |

## Dễ nhầm

- **"Đoạn càng to thì model càng có đủ ý."** Không. Đã đo: gộp thành đoạn to làm mất đáp án ở 4 tới 6 trên 32 câu.
- **"Cắt đoạn thì phải gối đầu."** Không bắt buộc. Gối đầu chỉ cần khi cắt có thể rơi vào giữa một ý. Cắt theo cấu trúc bài thì không.
- **"Một đoạn là một đoạn văn."** Không hẳn. Một đoạn có thể là một đoạn văn, một mục danh sách, một bảng ngắn, hoặc một dòng bảng kèm dòng tiêu đề.

## Câu hỏi tự kiểm

<details>
<summary>1. Bốn luật cắt là gì?</summary>

Mỗi khối là một đoạn nếu vừa giới hạn. Bảng dài tách từng dòng, mỗi dòng kèm dòng tiêu đề. Mục danh sách dài tách từng mục con, giữ nhãn mục cha. Đoạn văn dài tách ở ranh giới câu, không cắt giữa câu.

</details>

<details>
<summary>2. Vì sao đưa cho model nhiều đoạn nhỏ tốt hơn ít đoạn to, cùng một lượng chữ?</summary>

Đã đo: gộp to làm mất đáp án ở 4 tới 6 trên 32 câu. Cách giải thích của nhóm (chưa đo riêng): đoạn to chiếm chỗ, đẩy đoạn đúng của ý khác ra ngoài; nhiều đoạn nhỏ trỏ tới nhiều chỗ của kho hơn.

</details>

<details>
<summary>3. Vì sao một đoạn quá dài lại làm dừng cả bước chuẩn bị?</summary>

Model embedding bỏ im lặng phần vượt 512 token, nên vector của đoạn đó sẽ thiếu mà không ai biết. Dừng hẳn thì lỗi lộ ra ngay, trước khi chỉ mục bị ghi gì.

</details>

<details>
<summary>4. Thêm một dòng vào giữa một bài thì mã đoạn đổi thế nào?</summary>

Mã là đường dẫn bài kèm số thứ tự đoạn, nên các đoạn phía sau của chính bài đó dịch số và được tính lại vector. Bài khác không bị ảnh hưởng.

</details>

## Cấu hình đang chạy

*Chép từ hệ thống đang chạy sáng 22/11/2026. Cấu hình đổi thì mục này phải chép lại.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Đơn vị cắt | khối của bài (đoạn văn, mục danh sách, bảng, đoạn trích) | giữ nguyên ranh giới ý mà người soạn đã đặt | đã thử 12 cách khác (mục "Đã so") |
| Gối đầu | không | không cắt ngang ý nên không cần | chưa so: bản thử chỉ có nhóm món ăn hồi tháng 8 từng cắt theo 400 ký tự, nhưng chưa được đặt cạnh cách hiện nay trên cùng một bộ đo |
| Bảng | cả bảng nếu vừa giới hạn; không thì từng dòng kèm dòng tiêu đề | con số luôn đi cùng tên cột | đã thử gộp các dòng liền nhau: không khác |
| Đoạn văn dài | tách ở ranh giới câu | không cắt giữa câu | — |
| Giới hạn độ dài | mỗi đoạn phải vừa cả ba: 512 token của model đang dùng, 512 token và 256 token (có tách từ tiếng Việt) của hai model ứng viên cũ | mức chặt nhất (256) khiến một số khối dài bị tách thêm (61 đoạn ở 14 bài, đếm trên kho cuối tháng 10) | đã thử chỉ giữ giới hạn 512 của model đang dùng: ít đi 61 đoạn, kết quả tìm không khác; bỏ được nhưng chưa dọn |
| Kết quả | 266 bài ⇒ 9.458 đoạn | — | — |
| Độ dài trung bình một "chữ để tìm" | khoảng 67 âm tiết | số của bộ từ khoá (bài 11) | — |
| Thư mục của kho không đưa vào | bộ câu hỏi chấm, bản thô tải từ trang nguồn, thư mục mẫu bài và ghi chú soạn | không phải nội dung cho người dùng | — |
| File bị loại đích danh | 3 file danh mục dùng lúc soạn | chỉ là danh sách tên, không phải nội dung để trả lời | phép đo lúc loại: kết quả tìm không khác |
| Quy tắc gắn lưu ý | 3 quy tắc ở 2 bài: câu lưu ý chung của bài được gắn kèm vào đúng những đoạn đã khai trong quy tắc | các đoạn giá đó được tìm ra thì mang theo lưu ý | — |

## Đã so

**Vấn đề.** Cách cắt là lựa chọn làm từ rất sớm. Cuối tháng 10 nhóm rà lại mọi lựa chọn cũ: có cách cắt nào khiến đoạn chứa đáp án lọt vào phần đưa cho model viết nhiều hơn không?

**So gì, trên bộ nào.** 12 cách cắt khác, trên 32 câu hỏi đã biết chắc đáp án nằm ở đoạn nào của kho. Thước: đoạn chứa đáp án còn nằm trong phần đưa cho model viết không. Để công bằng, mọi cách đều chỉ được đưa **cùng một lượng chữ** (750 token); nếu không, đoạn to tự thắng chỉ vì chở nhiều chữ hơn. Luật ghi trước khi đo: một cách mới chỉ được nhận nếu không làm câu nào mất đáp án.

| Cách thử | Số câu tốt lên / số câu mất đáp án (trên 32) | Kết luận |
|---|---|---|
| Gộp đoạn ngắn tới 128 token; gộp các dòng bảng liền nhau | 0 / 0 | không khác, đổi cũng không được gì |
| Gộp tới 256 token | 0 / 4 | bỏ |
| Gộp tới 384 token | 1 / 6 | bỏ |
| Gộp tới 512 token | 0 / 6 | bỏ; mức tụt này được phép thử thống kê xác nhận là thật |
| Tìm xong thì mở rộng ra cả mục chứa đoạn | 0 / 8 | bỏ; tệ nhất |
| Bỏ tên bài và tên mục khỏi "chữ để tìm" | 3–4 / 7–8 | bỏ (bài 9 kể kỹ) |

**Đọc bảng này thế nào.**
- Đoạn to chiếm nhiều chỗ. Số đo ở một lượng chữ gấp đôi (1.500 token, cỡ 10 đoạn nhỏ): chỉ vừa khoảng 4–5 đoạn to, so với khoảng 9 đoạn nhỏ trỏ tới 9 chỗ khác nhau. Ở lượng chữ đó, gộp tới 384 và 512 token vẫn làm mất 6 câu.
- Báo cáo đo ghi lý do: đoạn to đẩy đoạn đúng của câu khác ra khỏi phần đưa cho model.
- Mở rộng ra cả mục là tệ nhất: các đoạn cùng mục với một hai đoạn đứng đầu chiếm gần hết chỗ.

**Đã chọn: giữ cách cắt theo khối, đoạn nhỏ.** Cùng đợt rà, một phép đo khác (đo câu trả lời, không đo cách cắt) cho thấy đưa 10 đoạn thay vì 5 làm câu trả lời đủ ý hơn (bài 13). Hai kết quả cùng chỉ một hướng: cho model thấy **nhiều chỗ hơn** thì giúp, cho mỗi chỗ to hơn thì không.

**Giới hạn của phép đo.** 32 câu là bộ nhỏ, đo trên kho cuối tháng 10. Kết luận "đoạn to tệ hơn" khá chắc: ba mức gộp to nhất (256, 384, 512) đều làm mất câu, và vẫn mất khi nâng lượng chữ lên cỡ 10 đoạn. Kết luận "gộp nhỏ không khác" chỉ có nghĩa là trên 32 câu này chưa thấy khác.

## Quyết định nhỏ hơn

**Vì sao không mở rộng ra cả mục chứa đoạn sau khi tìm?** Đã đo hai lần: ở lượng chữ nhỏ thì mất 8 câu (bảng trên); ngày 19/11, thay mỗi đoạn bằng cả mục thì không khác về chất lượng và phát sinh lỗi (bài 13).

**Vì sao không bỏ ba cặp đoạn lặp một phần?** Đã thử bỏ: không khác, nên để nguyên.

## Giới hạn đã biết

- **Dòng bảng là đoạn rất ngắn.** Mỗi dòng giá đứng riêng, ít chữ; câu hỏi viết khác chữ với dòng đó thì bước tìm dễ bỏ sót. Gốc của lỗi ở bước tìm; thử gộp dòng bảng không giúp.
- **Nhiều đoạn rất ngắn.** Gần 1.800 đoạn ngắn hơn 50 token (đếm trên kho cuối tháng 10). Đoạn quá ngắn có ít chữ để so nghĩa.
- **Mã đoạn dồn số khi sửa giữa bài.** Mã đánh theo thứ tự trong bài, nên thêm hay bớt một dòng giữa bài thì các đoạn phía sau đổi số. Hệ thống vẫn chạy đúng; nhưng khi so "trước và sau khi sửa kho" phải so theo nội dung, không theo mã.
- **Ba cặp đoạn lặp một phần** ở 3 bài di tích (đoạn trích nằm trong mục danh sách). Đã thử bỏ phần lặp: không khác, nên để nguyên.

## Chi tiết để tra

- Số 366 token, "một nửa dưới khoảng 85 token" và "gần 1.800 đoạn dưới 50 token" đếm trên kho cuối tháng 10 (khoảng 8.400 đoạn); chưa đếm lại trên 9.458 đoạn hiện nay.
- Lần chuẩn bị nào cũng chạy vòng kiểm cuối; bản ghi của lần chuẩn bị đang dùng ghi trạng thái hoàn tất với 9.458 đoạn.
- Có một bài test chạy lại việc cắt trên cùng kho và so kết quả với bản ghi, để bảo đảm mã đoạn không đổi giữa hai lần chạy.
- Bảng dài tách từng dòng chỉ khi cả bảng không vừa giới hạn; bảng vừa thì giữ nguyên một đoạn.
- Lượng chữ 750 token trong phép so là mức của thời hệ thống còn đưa 5 đoạn cho model viết.

**Bài sau (bài 9):** mỗi đoạn mang theo tên bài và tên các mục chứa nó. Bài 9 giảng phần thông tin gắn kèm này, và chuyện gì xảy ra khi thử bỏ nó đi.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Bốn luật cắt, không gối đầu, phần bằng chứng kèm vị trí, vòng kiểm cuối: `backend/ingestion/chunking/full_corpus_chunker.py` (hàm `chunk_document`), `markdown_blocks.py` [code]; chép qua `bai_hoc/02_CHUNKING.md` (bài đã qua kiểm độc lập), mình đọc lại phần kiểm giới hạn token ngày 22/11/2026.
- Ba giới hạn token (512 / 512 / 256 có tách từ): `backend/config/settings.yaml` mục `full_corpus.embedding_models`; hàm kiểm lặp qua cả ba: `full_corpus_chunker.py` [code, đọc 22/11/2026]. Thử chỉ giữ giới hạn của model đang dùng (8.398 đoạn, ít đi 61, không khác): `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` thẻ N2-05 [đã chạy, kho cũ; theo biên bản kiểm độc lập `data/hoc_cung_D/kiem/bai_02_10.md`].
- Đoạn số 5 và số 6 của ví dụ chính (hai dòng của cùng một bảng, cùng dòng tiêu đề) và câu trả lời về Tuyến A: `data/hoc_cung_D/vi_du_di_suot_vet.json`, trường `ngu_canh`, `tra_loi` [đã chạy, riêng tư]. Khối chữ trong bài là bản rút gọn của đoạn thật: tên các cột và tên các điểm được viết tắt, bỏ dòng kẻ bảng, gạch đầu dòng và dấu in đậm (kho mã của dự án có một bước kiểm tự động không cho chép nguyên một dòng dài của kho vào tài liệu).
- 266 bài, 9.458 đoạn, trạng thái hoàn tất: `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json`, đọc 10:02 22/11/2026 [đã chạy]. Độ dài trung bình 66,63: `data/full_corpus_builds/full_corpus_sparse_state.json` (`average_document_length`).
- Thư mục và file bị loại, file quy tắc gắn lưu ý: `backend/config/settings.yaml` (`exclude_parts`, `exclude_files`, `conditions_file`) [cấu hình]. "3 quy tắc": `bai_hoc/01_KHO_DU_LIEU.md` [chép; chưa đếm lại ngày 22/11].
- 366 token, trung vị 85, 1.787 đoạn dưới 50 token, 3 cặp lặp: `bao_cao_he_thong/03_BAO_CAO_CHIA_DOAN.md` qua `bai_hoc/02_CHUNKING.md` [đã chạy, kho cũ].
- 12 cách cắt, 32 câu, 750 token, bảng kết quả: `bao_cao_he_thong/03_BAO_CAO_CHIA_DOAN.md` mục 4 qua `bai_hoc/02_CHUNKING.md` [đã chạy 25/10].
- Lần thử 19/11 đưa nhiều chữ nguồn hơn: `bai_hoc/VIEC_MOI_XONG.md` mục 14 [đã chạy].
- Mã đoạn và mã cất trong Qdrant suy ra cố định; test chạy lại: `backend/core/schema.py`, `backend/tests/test_full_corpus_chunker.py` [code].
- Mục "Quyết định và lý do", "Nếu… thì sao", "Quyết định nhỏ hơn", "Câu hỏi tự kiểm" (thêm 13:44 22/11/2026 theo khuôn mới; gom từ "Đã so", bảng cấu hình, mục "Vì sao không làm cách khác" cũ). Lý do dừng khi đoạn vượt giới hạn ("e5 sẽ cắt im lặng ở 512"): chú thích vòng kiểm cuối trong `backend/ingestion/chunking/full_corpus_chunker.py` [code]. Lý do kiểm mảnh bằng chứng và lý do cắt bằng luật thay vì model: người viết dò chú thích trong cùng file, không thấy. Lý do "cắt theo khối", "con số đi cùng tên cột": `bai_hoc/02_CHUNKING.md` và bảng cấu hình của bài này [chép]. Lệnh cập nhật dừng ở bước cắt khi sửa câu bị quy tắc gắn lưu ý chép nguyên văn; thêm dòng giữa bài làm các đoạn sau đổi số; 21 giây cắt đoạn: `bai_hoc/VIEC_MOI_XONG.md` mục 32 [đã chạy]. Cập nhật riêng dựa vào việc cắt lại ra đúng đoạn cũ: chú thích đầu `backend/ingestion/cap_nhat_rieng.py` [code]. Giới hạn lúc cắt đổi theo danh sách model trong cấu hình: `full_corpus.embedding_models` [cấu hình; dòng "đổi model" là suy từ code, chưa thử].
- Các mục mới đã qua một lượt đối chiếu độc lập (một agent khác chỉ đọc, 22/11/2026), các dòng sai / lệch đã sửa lúc 14:17: `data/hoc_cung_D/kiem/muc_moi_02_07_11_va_phu_luc.md` [riêng tư]. Máy chủ không bật khi đoạn mô tả của bảng điểm không còn: `backend/llm/lich_trinh_v2.py` (`kiem_doan_mo_ta`), gọi trong `backend/api/app.py` ngoài khối bắt lỗi [code]. `candidate_id` chỉ nhận `e5-small-384`: `backend/core/settings_loader.py` (`validate_phase6_settings`) [code].

- Cập nhật theo bộ thay đổi mở 14:47 22/11/2026: `bai_hoc/VIEC_MOI_XONG.md` mục 42, 43; `guides/RUNBOOK_BAN_GIAO.md` mục 10.1; `backend/config/settings.yaml` (`so_lan_tim_kho: 3`) [code; người viết không chạy lại].

</details>
