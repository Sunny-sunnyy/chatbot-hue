# Bài 14 — Xếp lại bằng model (reranking): đã thử ba cách, không dùng

*Cập nhật 10:30, ngày 22/11/2026 · cấu hình đọc từ hệ thống đang chạy; số của các phép so lấy từ báo cáo đo ngày 25/10 và 27/10, model gpt-6-luna, kho của thời điểm đó; người viết không chạy lại phép đo nào.*

**Bài trước đã biết:** trên 40 câu khó, 9 câu có đoạn đúng nằm trong 30 ứng viên nhưng đứng dưới hạng 10, nên model viết không thấy.
**Bài này thêm:** cách chữa quen thuộc cho chuyện đó là dùng một model đọc kỹ từng ứng viên rồi xếp lại. Bài này kể ba lần thử, kết quả của từng lần, và vì sao hệ thống đang chạy không xếp lại.

## Ý chính

- **Xếp lại** là thêm một bước sau bước tìm: một model đọc câu hỏi **cùng với** từng ứng viên, chấm mức liên quan, rồi xếp lại thứ tự.
- Hệ thống đang chạy **không có bước này**. Nó đã được thử ba cách và không cách nào qua được điều kiện ghi trước.
- Hai model xếp lại chạy trên máy: mọi bản đều làm mất đoạn đúng ở 1 tới 3 câu.
- Để model viết tự chọn 10 trong 30 ứng viên: bước tìm tốt hơn hẳn (số câu có đủ đoạn đúng từ 22 lên 31 trên 40), điểm trung bình tăng, nhưng 5 câu tệ đi (điều kiện cho phép 4). Bản này bị gác vì 5 câu đó; ngoài ra nó chậm (cả câu 6,5 giây) và đắt gần gấp 4.
- Bài học: xếp đúng hơn chưa chắc trả lời tốt hơn, và trung bình tốt hơn vẫn có thể giấu vài câu tệ đi.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| xếp lại | **reranking** | bước chấm lại và đổi thứ tự các ứng viên sau khi tìm |
| model xếp lại | **reranker**, **cross-encoder** | model nhận một cặp (câu hỏi, đoạn) và trả về một điểm liên quan |
| câu tệ đi | **regression** | câu mà bản mới trả lời kém hơn bản đang chạy |

## Model xếp lại đọc câu hỏi và đoạn cùng một lúc

Ở bước tìm theo nghĩa, vector của câu hỏi và vector của đoạn được tính riêng rẽ rồi mới so (bài 10). Cách đó nhanh, nhưng chưa có model nào đọc câu hỏi và đoạn cùng nhau.

Một model xếp lại nhận cả hai trong một lần đọc và cho một điểm "đoạn này liên quan tới câu hỏi tới đâu". Đọc chung thì sát hơn, nhưng phải đọc từng cặp một: 30 ứng viên là 30 lần đọc. Vì vậy bước này chỉ chạy trên vài chục ứng viên, không chạy trên cả kho. Ở các lần thử dưới đây nó được chạy trên 10 đoạn đầu, và một lần trên 100 ứng viên.

## Lần thử 1 và 2: hai model xếp lại chạy trên máy đều làm mất đoạn đúng

Hai model được thử, đều chạy trên card đồ hoạ của máy phát triển: một model xếp lại đa ngữ dùng phổ biến, và một model xếp lại riêng cho tiếng Việt. Mỗi model thử hai kiểu: đọc thân đoạn, và đọc thân đoạn kèm tên mục. Lúc đó hệ thống còn đưa 5 đoạn cho model viết.

Kết quả: model đa ngữ với thân đoạn xếp đúng hơn rõ nếu nhìn điểm thứ hạng, nhưng ở 1 câu nó đẩy đoạn đúng ra khỏi phần đưa cho model viết. Ba bản còn lại mỗi bản làm mất đoạn đúng ở 3 câu. Điều kiện ghi trước là không câu nào được mất đoạn đúng, nên cả bốn bản bị loại.

## Lần thử 3: để model viết tự chọn 10 trong 30 ứng viên

Ý thứ ba: đưa cả 30 ứng viên cho gpt-6-luna và nhờ nó chọn 10 đoạn hợp nhất, thay cho 10 đoạn đứng đầu theo thứ hạng. Bản này được đo ở cả hai tầng: bước tìm, và câu trả lời.

Ở tầng bước tìm nó tốt hơn hẳn: số câu có đủ đoạn đúng trong phần đưa cho model viết từ 22 lên 31 trên 40, không câu nào mất. Gần như chữa đúng chỗ hỏng về thứ tự.

Ở tầng câu trả lời, điểm trung bình cũng tăng. Nhưng khi đếm từng câu thì có **5 câu tệ đi**, trong khi điều kiện ghi trước chỉ cho phép nhiều nhất 4. Bản này bị gác lại vì lý do đó. Ngoài ra bước chọn đoạn làm cả câu mất 6,5 giây (câu ở giữa) và tốn gần gấp 4; hai điều này lúc đó chỉ được theo dõi, mức chờ 3 giây được chốt sau phép đo.

## Xếp đúng hơn chưa chắc trả lời tốt hơn

Ba điều rút ra từ ba lần thử:

- **Thước của bước tìm và thước của câu trả lời khác nhau.** Điểm thứ hạng thưởng cho việc đưa **một** đoạn đúng lên đầu. Câu trả lời tốt lại cần **đủ mọi mảnh**: câu hỏi cần ghép nhiều nguồn cần ba bốn đoạn khác nhau cùng có mặt. Một model xếp lại có thể đưa đoạn tốt nhất lên đầu mà làm rơi mảnh thứ ba.
- **Trung bình tốt lên vẫn có thể giấu vài câu tệ đi.** Người dùng gặp câu tệ đi, không gặp con số trung bình. Điều kiện "không quá mấy câu tệ đi" được ghi trước để bắt đúng chuyện này (bài 20).
- **Thời gian và tiền cũng là giới hạn.** Một bước thêm 4 tới 7 giây làm cả câu vượt mức chờ 3 giây (mức này được chốt sau phép đo, không phải lý do gác lúc đó).

Hệ thống đi hai đường khác để model có đủ đoạn hơn, rẻ hơn và đã đo là giúp điểm "đủ ý": đưa 10 đoạn thay vì 5 (bài 13), và cho trợ lý tự tìm thêm khi thiếu (bài 21). Hai đường này chưa được đo riêng trên đúng 9 câu hỏng về thứ tự.

## Dễ nhầm

- **"Thêm bước xếp lại thì kết quả luôn tốt hơn."** Ở đây thì không: bốn bản chạy trên máy đều làm mất đoạn đúng, bản dùng model viết làm 5 câu tệ đi.
- **"Điểm thứ hạng tăng là câu trả lời tốt hơn."** Không hẳn. Lần thử 3 tăng mạnh ở bước tìm mà vẫn không qua được ở tầng câu trả lời.
- **"Không dùng tức là chưa biết tới."** Bước này đã được thử ba cách và có số đo cho từng cách; nó bị bỏ vì số đo.

## Những điều cần nhớ

- Hệ thống không xếp lại. Đã thử ba cách: hai model xếp lại chạy trên máy, và để model viết chọn đoạn.
- Model xếp lại trên máy: mất đoạn đúng ở 1 tới 3 câu ⇒ loại.
- Model viết chọn 10 trong 30: bước tìm từ 22 lên 31 trên 40 câu đủ đoạn đúng, nhưng 5 câu tệ đi (cho phép 4) ⇒ gác; nó cũng chậm (6,5 giây) và đắt gần gấp 4.
- Thước của bước tìm khác thước của câu trả lời; trung bình tốt hơn có thể giấu câu tệ đi.
- Thay cho xếp lại, hệ thống đưa 10 đoạn và cho trợ lý tìm thêm.

## Cấu hình đang chạy

*Chép từ hệ thống đang chạy sáng 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Xếp lại bằng model (`reranker`) | `none` (không) | ba cách đã thử đều không qua điều kiện ghi trước | đã thử ba cách (mục "Đã so") |
| Thứ tự 10 đoạn đưa cho model viết | theo kết quả trộn hai bảng xếp hạng (bài 13) | — | — |

Phần chương trình của bước xếp lại vẫn còn trong kho mã, chỉ dùng cho các lần thử.

## Đã so

**Vấn đề.** Ở 9 trên 40 câu khó, đoạn đúng đã được lấy về nhưng đứng ở hạng 11 tới 30.

**So gì, trên bộ nào.** Ba cách xếp lại so với "không xếp lại". Lần thử 1 và 2 trên 30 câu khó có đánh dấu đoạn đúng; lần thử 3 trên 40 câu, kiểm lại trên 15 câu khác, và còn đo câu trả lời trên 88 câu của bộ câu mẫu, người chấm cho điểm 1 tới 5. Model viết gpt-6-luna.

| Cách thử | Tầng bước tìm | Tầng câu trả lời | Thời gian, tiền | Kết luận |
|---|---|---|---|---|
| Model xếp lại đa ngữ, chạy trên máy (2 kiểu) | điểm thứ hạng tăng khoảng 0,1 ở kiểu tốt nhất; mất đoạn đúng ở 1 câu (kiểu kia: 3 câu) | không đo | khoảng 1 giây cho 10 đoạn (kiểu kèm tên mục: 2,7 tới 4,8 giây) | bỏ |
| Model xếp lại tiếng Việt, chạy trên máy (2 kiểu) | mất đoạn đúng ở 3 câu mỗi kiểu | không đo | không ghi riêng | bỏ |
| Lấy 100 ứng viên rồi cho model xếp lại chọn 10 | không khác so với lấy 100 mà không xếp lại | không đo | 11 tới 14 giây | bỏ |
| gpt-6-luna chọn 10 trong 30 ứng viên | câu có đủ đoạn đúng: 22 lên 31 trên 40; nhóm kiểm lại: 7 lên 10 trên 15; không câu nào mất | điểm "đủ ý" tăng 0,22; **5 câu tệ đi** (cho phép 4) | cả câu 6,5 giây (câu ở giữa), 9,1 giây (câu chậm); tiền khoảng 3,8 lần | gác, giữ hồ sơ |

**Đọc bảng này thế nào.**
- Các model chạy trên máy bị loại ngay ở tầng bước tìm: chúng làm rơi đoạn đúng.
- Dùng model viết để chọn đoạn là cách duy nhất chữa được thứ tự. Nó bị loại ở tầng câu trả lời (5 câu tệ đi).
- Dòng thứ ba cho thấy phần lợi (nếu có) của việc lấy rộng đến từ lấy rộng, không đến từ xếp lại.

**Giới hạn của phép đo.** Hai dòng đầu đo khi hệ thống còn đưa 5 đoạn và trên kho cuối tháng 10; với 10 đoạn như hiện nay, model xếp lại chạy trên máy có thể không còn làm rơi đoạn đúng. **Chưa đo lại.** Không dòng nào được đo với model đang chạy.

## Giới hạn đã biết

- Không có bước xếp lại nên chỗ hỏng về thứ tự vẫn còn: đoạn đúng đứng hạng 11 tới 30 thì model viết không thấy ở lần tìm đầu.
- Kết luận "không dùng" đứng trên các phép đo cũ. Đổi máy (có card đồ hoạ mạnh hơn) hoặc đổi model thì thời gian và kết quả có thể khác.

## Vì sao không làm cách khác

**Vì sao không dùng dịch vụ xếp lại trả tiền của các hãng?** Chưa thử.

**Vì sao không thử lại model xếp lại ở cấu hình 10 đoạn?** Chưa thử. Nó được ghi trong danh sách "đáng thử lại" của bảng tổng các phép so.

**Vì sao không nhận bản model viết chọn đoạn, khi trung bình của nó tốt hơn?** Đã đo: 5 câu tệ đi, vượt mức 4 ghi trước. Quyết định đã ghi: gác lại vì lý do đó.

## Chi tiết để tra

- Lần thử 1 và 2 làm ngày 25/10; điểm thứ hạng của kiểu tốt nhất tăng 0,105; thời gian 0,85 tới 1,19 giây cho 10 đoạn.
- Lần thử 3 làm ngày 27/10: điểm "đủ ý" tăng 0,22 (khoảng tin cậy từ +0,02 tới +0,44), điểm "đúng" tăng 0,25, từ chối nhầm từ 7 xuống 2 trên 88 câu; riêng bước chọn đoạn mất 4,6 giây (câu ở giữa) và 6,9 giây (câu chậm).
- Trước lần thử 3 có một bản nhỏ hơn: model viết xếp lại 10 đoạn đã chọn; điểm thứ hạng tăng 0,17, không câu nào mất, nhưng bộ câu chỉ có tối đa 3 câu có thể cải thiện nên kết luận là "chưa rõ". Hai biến thể khác của lần thử 3 hỏng vì model trả sai dạng đầu ra.
- Số 22 trên 40 ở bài này và số 24 trên 40 ở bài 13 là hai lần gắn nhãn đoạn đúng khác nhau trên cùng 40 câu.

**Bài sau (bài 15):** 10 đoạn đã chọn xong. Bài 15 giảng lời gọi gửi model viết: lời dặn, cách 10 đoạn được trình bày, và số nguồn.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- `reranker: none`: `backend/config/settings.yaml` mục `full_corpus_runtime`; phần chương trình xếp lại chỉ còn cho bộ thử: `backend/reranking/` [code].
- Ba lần thử, các con số của bảng và của "Chi tiết để tra": `bai_hoc/07_RERANKING.md` (thân bài và mục Nguồn) và `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 8, 9; nguồn gốc `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` thẻ T3-08, T3-09 và `bao_cao_he_thong/06_BAO_CAO_TIM_KIEM.md` [đã chạy 25/10 và 27/10; chép qua hai bài cũ đã qua kiểm độc lập].
- Lần thử 3 so với mốc "10 đoạn theo thứ hạng": `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 9 và ghi chú sửa 14:41 11/11/2026 ở mục Nguồn của bài đó.
- "Đáng thử lại": `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` mục "Nhìn cả bảng thấy gì" ý 4.
- 9 trên 40 câu: bài 13 và nguồn của nó.

</details>
