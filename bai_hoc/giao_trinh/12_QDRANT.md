# Bài 12 — Cất vào Qdrant, cập nhật khi kho đổi, và vì sao hệ thống không chịu chạy khi kho lệch chỉ mục

*Cập nhật 10:21, ngày 22/11/2026 · cơ chế đọc từ chương trình và cấu hình đang chạy; số của lần cập nhật chỉ mục lấy từ lần chạy thật sáng 22/11 và phép kiểm độc lập của một phiên khác; người viết không chạy lại.*

**Bài trước đã biết:** mỗi đoạn có chữ, thông tin gắn kèm, một vector, và phần từ khoá.
**Bài này thêm:** tất cả những thứ đó của 9.458 đoạn được cất ở đâu; khi một bài trong kho đổi thì cập nhật thế nào; và bước kiểm khiến hệ thống thà không chạy còn hơn trả lời bằng dữ liệu cũ.

## Ý chính

- **Qdrant** là cơ sở dữ liệu chuyên tìm vector. hue_rag cất cả 9.458 đoạn vào một **collection** duy nhất của nó; phần này gọi chung là **chỉ mục**.
- Mỗi lần lập chỉ mục, chương trình ghi một **bản ghi chỉ mục**: danh sách bài của kho kèm "dấu vân tay" của từng bài. Dấu vân tay đổi khi bài đổi dù chỉ một chữ.
- Mỗi lần khởi động, hệ thống so bản ghi đó với kho hiện có. **Lệch thì ô hỏi đáp không nhận câu hỏi nào.**
- Khi sửa vài bài, không phải lập lại cả chỉ mục (khoảng 225 giây). Một lệnh **cập nhật riêng** chỉ tính lại vector cho những đoạn có thay đổi (đổi chữ, hoặc đổi số thứ tự trong bài); lần chạy thật đầu tiên mất 37,7 giây cho 105 đoạn của 2 bài.
- Kết quả của lần cập nhật riêng đầu tiên đã được so với một lần lập lại toàn bộ từ cùng kho: giống nhau ở cả 9.442 đoạn (chữ và phần từ khoá giống hệt, vector lệch không quá 0,00000015), và 176 câu hỏi mẫu cho cùng 10 đoạn.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| Qdrant | **Qdrant**, một **vector database** | cơ sở dữ liệu cất vector và tìm vector gần nhất |
| collection | **collection** | một "bảng" của Qdrant; hue_rag dùng đúng một collection |
| điểm | **point** | một bản ghi trong collection; mỗi đoạn của kho là một điểm |
| chỉ mục | **index** | toàn bộ dạng đã xử lý của kho để tìm: collection, file thống kê từ khoá, bản ghi chỉ mục |
| bản ghi chỉ mục | **build record** | file ghi lần lập chỉ mục: những bài nào, dấu vân tay từng bài, bao nhiêu đoạn, model nào |
| dấu vân tay | **hash** (SHA-256) | chuỗi ký tự tính từ nội dung một file; sửa một chữ là chuỗi đổi |
| hộp | **Docker container** | cách đóng một chương trình cùng mọi thứ nó cần để chạy giống nhau trên mọi máy (bài 36) |

## Mỗi đoạn là một điểm trong một collection của Qdrant

Qdrant chạy trên cùng máy với hệ thống, trong một hộp riêng, ở một phiên bản được ghi cố định. Dữ liệu của nó nằm trong một thư mục của dự án, nên tắt rồi bật lại vẫn còn nguyên.

hue_rag dùng đúng một collection. Tên của collection ghi luôn model embedding đã dùng, để không bao giờ lẫn với chỉ mục của model khác. Collection có 9.458 điểm, bằng đúng số đoạn. Mỗi điểm gồm:

- một **mã** cố định, suy ra từ mã đoạn (bài 8);
- **vector** 384 con số của đoạn (bài 10);
- phần **từ khoá** của đoạn (bài 11);
- **hồ sơ 7 trường**: chữ để tìm, tên bài, đường tiêu đề, phần bằng chứng, nguồn, mã đoạn, chủ đề (bài 9).

Lúc trả lời, hệ thống gửi vector của câu hỏi cho Qdrant và nhận về 30 điểm gần nhất kèm hồ sơ của chúng. Mọi việc sau đó (chấm từ khoá, trộn, dựng ngữ cảnh) dùng hồ sơ vừa nhận, không hỏi lại Qdrant.

## Bản ghi chỉ mục ghi lại kho lúc chỉ mục được lập

Mỗi lần lập chỉ mục, chương trình ghi một file gọi là bản ghi chỉ mục. Nó ghi:

- danh sách 266 bài của kho và **dấu vân tay của từng bài**;
- số đoạn (9.458) và số điểm đã cất;
- model embedding đã dùng: tên, phiên bản, số chiều;
- dấu vân tay của file thống kê từ khoá (bài 11);
- cấu hình của collection: cách đo độ gần, dạng hồ sơ.

Lúc khởi động, file này là căn cứ để trả lời câu hỏi "chỉ mục có khớp với kho không".

## Khởi động thì kiểm; lệch thì không nhận câu hỏi

Mỗi lần khởi động, trước khi nhận câu hỏi đầu tiên, hệ thống kiểm năm điều theo thứ tự:

1. **Bản ghi chỉ mục có hợp lệ không:** có tồn tại, đã hoàn tất, đúng tên collection, đúng model và phiên bản, số điểm bằng số đoạn.
2. **Kho có bị sửa không:** tính lại dấu vân tay của từng bài trong kho hiện có, so với bản ghi. Bước này bắt được bài mới thêm, bài bị mất, và bài bị sửa dù chỉ một chữ.
3. **File thống kê từ khoá có khớp không.**
4. **Collection có khớp bản ghi không:** có tồn tại, đúng cấu trúc, đúng số điểm.
5. **Model embedding có chạy không:** nạp model và tính thử một vector.

Sai ở điều 1 tới 4, hệ thống vẫn bật nhưng ô hỏi đáp từ chối mọi câu hỏi và báo lý do "kho đã đổi, phải cập nhật chỉ mục". Các trang không cần tìm trong kho (thời tiết, bản đồ, lịch mẫu) vẫn chạy. Sai ở điều 5, hoặc Qdrant không chạy, nó báo "tạm thời không phục vụ được".

Lý do thiết kế như vậy: nếu kho đã sửa mà chỉ mục còn dữ liệu cũ, hệ thống vẫn trả lời trôi chảy, có số nguồn hẳn hoi, nhưng nội dung là bản cũ. Không ai nhìn ra, kể cả model viết, vì ngữ cảnh đưa vào trông hoàn toàn hợp lý. Một lỗi im lặng kiểu đó tệ hơn một hệ thống báo thẳng "chưa sẵn sàng".

## Sửa vài bài thì chỉ tính lại vector cho những đoạn đổi chữ

Lập lại cả chỉ mục mất khoảng 225 giây, trong đó ước khoảng 195 giây là tính vector cho cả kho. Khi chỉ sửa một hai bài, phần lớn công đó là thừa. Từ ngày 22/11 có một lệnh **cập nhật riêng**. Nó làm sáu việc:

1. Cắt đoạn lại cả kho (không cần model, khoảng 21 giây).
2. So từng đoạn với điểm đang nằm trong collection. Đoạn nào giống hệt (cả chữ lẫn số thứ tự) thì **giữ nguyên vector cũ**.
3. Tính vector mới chỉ cho đoạn có thay đổi; xoá điểm không còn ứng với đoạn nào.
4. Ghi lại phần từ khoá của **mọi** điểm (khoảng 2 giây, không cần model).
5. Kiểm lại cả collection bằng chính phép kiểm của lúc lập chỉ mục.
6. Ghi file thống kê từ khoá và bản ghi chỉ mục mới.

Ba điều đáng nhớ về lệnh này:

- **Nó sửa ngay trong collection đang dùng.** Không tạo collection mới, không xoá collection cũ.
- **Đơn vị là đoạn, không phải bài.** Ở một ca thử, 7 con số giá nằm ở 7 đoạn của một bài được đổi, và đúng 7 đoạn được tính lại. Nhưng đoạn được đánh số theo thứ tự trong bài, nên thêm dòng vào giữa bài làm các đoạn phía sau của chính bài đó đổi số, và chúng cũng được tính lại.
- **Phần từ khoá của cả kho được ghi lại**, vì điểm từ khoá của mỗi đoạn phụ thuộc hai con số của cả kho: mỗi từ hiếm tới đâu, và một đoạn trung bình dài bao nhiêu. Sửa một bài có thể làm hai con số đó nhích đi, và khi đó phần từ khoá của các đoạn khác cũng đổi theo: ở một ca sửa giá, 69 điểm đổi; ở ca thêm một bài mới, mọi điểm đổi. Lệnh ghi lại cho mọi điểm để chỉ mục giống hệt một lần lập lại. (Cách tìm đang chạy không đọc phần từ khoá cất trong Qdrant; nó tự tính lúc hỏi từ chữ của đoạn và file thống kê. Với câu trả lời, thứ phải đúng là file thống kê.)

Lần chạy thật đầu tiên, sáng 22/11, sau khi hai bài về vé được sửa: lệnh tự nhận ra đúng 2 bài, tính lại vector cho 105 đoạn, giữ nguyên 9.337 đoạn, mất 37,7 giây. Số đoạn của kho từ 9.436 lên 9.442. (Sau đó kho thêm một bài mới, nên lúc viết bài này chỉ mục có 9.458 đoạn.)

Sau lệnh phải khởi động lại hệ thống; lúc khởi động nó nạp thống kê mới và bỏ các câu trả lời đang nhớ sẵn, trong đó có thể còn giá cũ.

## Dễ nhầm

- **"Sửa bài trong kho là câu trả lời đổi ngay."** Không. Phải cập nhật chỉ mục rồi khởi động lại. Chưa cập nhật mà khởi động lại thì hệ thống bật nhưng từ chối mọi câu hỏi.
- **"Qdrant chứa kho."** Qdrant chứa dạng đã xử lý của kho. Kho gốc là 266 file bài viết; mất Qdrant thì lập lại được từ kho, mất kho thì không.
- **"Cập nhật riêng chỉ đụng tới bài đã sửa."** Vector thì đúng vậy. Phần từ khoá thì mọi điểm đều được ghi lại.

## Những điều cần nhớ

- Một collection Qdrant, 9.458 điểm; mỗi điểm có mã, vector 384 con số, phần từ khoá, hồ sơ 7 trường.
- Bản ghi chỉ mục giữ dấu vân tay từng bài; khởi động thì kiểm năm điều; kho lệch chỉ mục thì ô hỏi đáp không nhận câu hỏi.
- Lập lại cả chỉ mục: khoảng 225 giây. Cập nhật riêng: khoảng nửa phút (lần chạy thật: 37,7 giây cho 105 đoạn).
- Cập nhật riêng sửa tại chỗ, chỉ tính lại vector cho đoạn có thay đổi, ghi lại phần từ khoá của cả kho.
- Đã kiểm độc lập lần cập nhật đầu tiên: giống một lần lập lại toàn bộ ở cả 9.442 điểm (vector lệch không quá 0,00000015), và 176 câu hỏi mẫu cho cùng 10 đoạn.

## Cấu hình đang chạy

*Chép từ hệ thống đang chạy sáng 22/11/2026. Cấu hình đổi thì mục này phải chép lại.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Phần mềm | Qdrant, chạy trong một hộp Docker, ghi cố định một phiên bản | bật lại vẫn đúng phiên bản đó | chưa so với cơ sở dữ liệu vector khác |
| Địa chỉ | chỉ nghe trên chính máy đó, cổng 6335 | máy khác không gọi thẳng vào được | — |
| Nơi giữ dữ liệu | thư mục `qdrant_storage/` của dự án | tắt hộp không mất dữ liệu | — |
| Tên collection | `hue_full_corpus_7a2_e5_small_384` | tên ghi luôn model embedding và số chiều | — |
| Số điểm | 9.458 | bằng số đoạn | — |
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

## Giới hạn đã biết

- **Phải tắt hệ thống trước khi chạy lệnh cập nhật** và bật lại sau. Khi gõ lệnh cập nhật bằng tay, lệnh có nhắc nhưng không chặn; khi lệnh được gọi từ lệnh duyệt một đề xuất sửa giá thì chỉ có lời nhắc khởi động lại ở cuối. Chưa thử cập nhật trong lúc hệ thống đang phục vụ.
- **Lệnh bị ngắt từ lúc bắt đầu ghi vào Qdrant trở đi thì ô hỏi đáp từ chối mọi câu hỏi** cho tới khi lệnh được chạy lại. Đây là cố ý. Ngắt trước đó (lúc cắt đoạn, lúc chụp) thì chưa có gì bị đổi.
- **Sửa đúng một câu mà quy tắc gắn lưu ý đang ghi nguyên văn** (3 câu ở 2 bài, bài 8) thì lệnh dừng ngay ở bước cắt đoạn; phải sửa quy tắc cho khớp rồi chạy lại.
- **Bản chụp trước khi ghi nằm bên trong hộp Qdrant;** tạo lại hộp là mất. Đường lùi cuối cùng vẫn là lập lại toàn bộ từ kho.
- **Phép kiểm lúc khởi động chỉ chạy lúc khởi động.** Sửa kho khi hệ thống đang chạy thì nó vẫn trả lời bằng chỉ mục cũ cho tới lần khởi động sau (suy ra từ chương trình, chưa thử).
- **Bản ghi chỉ mục giữ dấu vân tay của bài, không giữ dấu của chương trình cắt đoạn.** Đổi cách cắt đoạn mà không lập lại chỉ mục thì phép kiểm không bắt được (suy ra từ chương trình).
- **Qdrant không chạy** thì mọi câu hỏi đều nhận lời báo "tạm thời không phục vụ được".
- **Kho lớn gấp nhiều lần** thì bước cắt đoạn lại cả kho (21 giây hiện nay) sẽ thành phần chính của lệnh cập nhật.

## Vì sao không làm cách khác

**Vì sao dùng Qdrant mà không dùng một cơ sở dữ liệu vector khác?** Quyết định đã ghi (12/08/2026): dùng Qdrant chạy trong một hộp riêng của dự án, ghi cố định phiên bản. Chưa thử cái nào khác; không có phép so.

**Vì sao không để hệ thống tự cập nhật chỉ mục khi thấy kho đổi?** Quyết định đã ghi (21/11): cập nhật là một lệnh chạy tay, có chế độ xem trước bài nào sẽ đổi; lệnh duyệt một đề xuất sửa giá thì tự gọi nó.

**Vì sao không cho hệ thống chạy tiếp với chỉ mục cũ rồi báo "dữ liệu có thể đã cũ"?** Luật đã ghi của sản phẩm: chỉ trả lời từ kho. Việc dừng khi lệch có từ lúc dựng hệ thống; lập luận đứng sau: trả lời từ một chỉ mục không còn khớp kho là trái luật đó.

## Chi tiết để tra

- Các ca thử trên bản chép: không sửa gì, 22,9 giây · đổi 7 con số giá, 7 đoạn, 25,5 giây · thêm một bài mới, 36 đoạn, 28,2 giây · bỏ một mục ở giữa bài, 84 đoạn tính lại và 8 điểm bị xoá, 27,2 giây · hai ca ngắt lệnh giữa chừng rồi chạy lại, về đúng.
- Trong lần chạy thật, 105 đoạn gồm 6 đoạn mới và 99 đoạn đổi chữ hoặc đổi số thứ tự (bài giá thuê thuyền thêm nhiều dòng nên các đoạn phía sau dịch số).
- Vector lệch 0,00000015 giữa hai cách là do model tính theo lô; mức này không đổi thứ hạng tìm.
- Bản chụp collection: khoảng 0,2 giây, 63 MB; khôi phục từ bản chụp đã thử: 0,3 giây.
- Cách lùi một lần sửa kho: hoàn lại bài rồi chạy lại chính lệnh cập nhật; nó kéo chỉ mục về khớp kho cũ.
- Lệnh có chế độ "chỉ xem": in bài nào khác chỉ mục và số đoạn sẽ tính lại, không ghi gì.
- Hai mã lỗi của hệ thống khi không sẵn sàng: 409 (kho lệch chỉ mục) và 503 (Qdrant hoặc model embedding không chạy). Trang kiểm tình trạng vẫn trả lời, báo trạng thái "degraded".
- Lệnh soạn bản đề xuất khi một giá đổi (tìm mọi chỗ trong kho còn ghi giá cũ) là bước đứng trước lệnh cập nhật này; nó thuộc bài 7.

**Bài sau (bài 13):** hết chặng chuẩn bị. Chặng 3 bắt đầu từ lúc người dùng gõ câu hỏi: 30 ứng viên và hai bảng xếp hạng được trộn thành 10 đoạn như thế nào.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Qdrant trong Docker, ghi cố định bằng mã băm của ảnh, cổng `127.0.0.1:6335`, thư mục `qdrant_storage/`: `docker-compose.yml` [đọc 22/11/2026]. Địa chỉ và hạn 30 giây: `backend/config/settings.yaml` mục `vector_database`.
- Tên collection, 9.458 điểm, cosine, tên vector, dạng hồ sơ: `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` và số điểm Qdrant, đọc 10:02 22/11/2026 [đã chạy]. Cấu trúc collection (không chỉ mục phụ, HNSW mặc định): `backend/vectorstore/qdrant.py` [code].
- Hồ sơ nhận về khi tìm và việc chấm từ khoá dùng hồ sơ đó: `backend/retrieval/full_corpus.py`, hàm `search` [code].
- Năm điều kiểm lúc khởi động, mã 409 `corpus_reingest_required` / 503, trạng thái "degraded": `backend/retrieval/full_corpus.py` (`build_full_corpus_retrieval_service`, `verify_full_corpus_record_freshness`), `backend/api/app.py`, `backend/api/health.py` [code; thứ tự năm điều chép qua `bai_hoc/05_QDRANT.md`, bài đã qua kiểm độc lập].
- Lệnh cập nhật riêng (sáu việc, sửa tại chỗ, đơn vị là đoạn, ghi lại từ khoá cả kho, bản chụp, ngắt giữa chừng, chế độ chỉ xem): `backend/ingestion/cap_nhat_rieng.py`; `guides/RUNBOOK_BAN_GIAO.md` mục 5b; `report_agent/2026-11-22/c_cap_nhat_rieng.md` [code + đã chạy, phiên khác].
- Bảng thời gian từng bước (21,1 · 195 · 1,8 · 4,2 giây) và lý do chọn sửa tại chỗ: `report_agent/2026-11-22/c_cap_nhat_rieng.md` mục 2 [đã chạy 08:27 22/11].
- Lần chạy thật (2 bài, 105 đoạn = 6 + 99, giữ 9.337, 37,7 giây, 9.436 ⇒ 9.442), bốn phép kiểm độc lập, sáu ca trên bản chép: `bai_hoc/VIEC_MOI_XONG.md` mục 32 [máy kiểm + người thứ hai kiểm, 22/11].
- HNSW giống tìm chính xác 108 / 108: `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` thẻ N2-15 = T3-04 [đã chạy, kho cũ].
- Lô 64 điểm lúc lập chỉ mục: `backend/ingestion/full_corpus_pipeline.py` qua `bai_hoc/05_QDRANT.md` [chép].
- Yêu cầu của chủ dự án và quyết định "lệnh chạy tay sau khi duyệt": `session_prompt/HIEN_TRANG.md` mục 4, gạch 22:22 và 22:45 21/11/2026. Luật "chỉ trả lời từ kho": cùng file, phần "Sản phẩm".
- Hai giới hạn "sửa kho lúc đang chạy" và "đổi chương trình cắt đoạn": suy ra từ chương trình, chưa thử (theo `bai_hoc/05_QDRANT.md`).

</details>
