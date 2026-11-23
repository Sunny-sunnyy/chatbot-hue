# Bài 16 — Kiểm nguồn bằng chương trình, và câu từ chối cố định

*Cập nhật 14:17, ngày 23/11/2026 · khớp hệ thống 13:41 23/11 (50 tính năng mở, 5 tắt, kho 267 bài): câu hỏi việc ở tỉnh, thành khác được che bằng một đoạn dặn (tính năng thứ 50), số tự đếm lại từ file đo thô · luật kiểm đọc từ chương trình; số khác từ các báo cáo 25/10–22/11, ghi model ở từng số; người viết không chạy lại phép đo nào.*

**Bài trước đã biết:** model viết nhận lời dặn, câu hỏi, 10 đoạn, và trả về một ô chữ có các số nguồn [n].
**Bài này thêm:** chương trình làm gì với ô chữ đó trước khi coi lượt hỏi là xong. Hai việc: kiểm số nguồn, và nhận ra câu từ chối.

## Ý chính

- Chương trình kiểm số nguồn theo **ba luật**: câu trả lời phải có ít nhất một số nguồn; mọi số phải là số của một nguồn đã thật sự được đưa cho model (một đoạn của kho, hoặc một nguồn do chương trình dựng như khối dự báo thời tiết); câu từ chối thì không được kèm số nguồn.
- Phạm luật thì câu trả lời **bị rút lại**: người dùng thấy "Câu trả lời không đáp ứng yêu cầu trích dẫn." và nút "Thử lại", không thấy câu trả lời có nguồn giả. Hai lối đỡ: chạy lại cả lượt một lần (lượt kèm câu trả lời liền trước, ở ô chat); viết lại một lần (từ 14:47 22/11, chữ không số nguồn mà model đã tự tìm; bài 21).
- Câu từ chối là **một câu cố định, đúng từng chữ**. Nhờ vậy chương trình nhận ra chắc chắn một lượt là từ chối, để mở đường tra web và để đếm khi đo.
- Bước kiểm này mới kiểm **số nguồn có thật**, chưa kiểm đoạn được trích có nói đúng điều câu trả lời viết không. Trưa 23/11 câu hỏi việc ở tỉnh, thành khác có lúc qua được nhờ một dòng lạc có thật (câu ví dụ 12 trên 20 lần). Từ chiều 23/11 một đoạn dặn làm model từ chối các câu đó (lượt đo 0 trên 20): lời dặn, không phải bước kiểm.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| kiểm số nguồn | **citation check**, **citation integrity** | kiểm mọi số [n] trong câu trả lời trỏ tới một đoạn có thật |
| rút lại | **retract** | bỏ câu trả lời hỏng và thay bằng lời báo lỗi; chữ đã hiện (nếu có) bị xoá |
| câu từ chối cố định | **fixed refusal**, **fallback answer** | một câu duy nhất, đúng từng chữ, dùng mỗi khi không đủ bằng chứng |
| điều kiện không được vỡ | — (trong hồ sơ dự án gọi là "sàn") | một điều ghi trước mà mọi thay đổi phải giữ; ở đây: 0 câu ngoài kho được trả lời bằng kho |

## Ba luật kiểm số nguồn

Sau khi model viết xong, chương trình đọc ô chữ và kiểm:

1. **Câu trả lời phải có ít nhất một số nguồn.** Một câu trả lời không có số nào thì không ai biết nó dựa vào đâu.
2. **Mọi số nguồn phải có thật.** Ở ví dụ chính, model được đưa các đoạn số 1 tới 10. Nếu câu trả lời ghi [12] thì đó là một nguồn bịa.
3. **Câu từ chối không được kèm số nguồn.** "Tôi không tìm thấy đủ thông tin… [3]" là một câu tự mâu thuẫn.

Câu trả lời thật của ví dụ chính ghi các số 1, 2, 4, 5, 6. Cả năm đều nằm trong 10 đoạn đã đưa, nên nó qua bước kiểm.

Trên màn hình số [n] không hiện (khung "Nguồn đã dùng", bài 5); bước kiểm chạy ở chương trình.

Chương trình chấp nhận hai cách ghi: [3] và [Nguồn 3]. Lý do ở mục "Đã so".

## Phạm luật thì câu trả lời bị rút lại

Với model đang chạy (trả cả câu một lần), ở lượt hỏi đáp về Huế trong ô chat, chữ được giữ tới khi qua bước kiểm nguồn rồi mới hiện; kiểm hỏng thì người dùng không thấy chữ đó. Trong lúc chờ là thẻ chờ (bài 5). Với model trả chữ dần (đường cũ), chữ hiện trước, kiểm sau, kiểm hỏng thì rút lại (bài 6, 21). Cả hai đường đều kết thúc bằng lời báo "Câu trả lời không đáp ứng yêu cầu trích dẫn." và nút "Thử lại".

Lựa chọn ở đây là: thà người dùng phải bấm lại, còn hơn đọc một câu trả lời mang số nguồn không có thật.

Có hai trường hợp chương trình không báo lỗi ngay:

- **Câu từ chối nối ở cuối.** Đôi khi model viết phần trả lời có số nguồn rồi nối thêm nguyên câu từ chối ở cuối. Theo luật 3 thì cả câu hỏng. Chương trình gỡ câu từ chối ở cuối, giữ phần có nguồn, rồi kiểm phần đó như mọi câu.
- **Lượt hỏi tiếp đang kèm câu trả lời liền trước** (từ 22/11, chỉ ở ô chat): chạy lại cả lượt **một lần** (quyết định 4).

## Câu từ chối là một câu cố định, đúng từng chữ

Khi các đoạn được đưa không đủ để trả lời, model phải trả đúng câu này, không thêm bớt:

> Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này.

Để model tự viết lời từ chối thì mỗi lần một kiểu, dễ thành từ chối nửa vời rồi đoán. Một câu cố định cho ba thứ:

- Chương trình **nhận ra chắc chắn** lượt này là từ chối, bằng cách so chữ. Từ đó nó mở đường tra web (bài 25).
- Khi đo, **đếm được chính xác** bao nhiêu câu bị từ chối, bao nhiêu câu từ chối nhầm, bao nhiêu câu ngoài kho lọt qua (chặng 4).
- Người dùng gặp cùng một thông báo mỗi khi kho không đủ (có mục web thì giao diện đổi thành câu dẫn sang mục web, ví dụ ngay dưới).

Ở ví dụ "kho không có" (chỗ đậu ô tô ở chùa Thiên Mụ), model trả đúng câu này. Chương trình nhận ra, tra web một lần, và vì mục web có nội dung nên giao diện thay câu từ chối bằng câu dẫn "Tư liệu của mình chưa có thông tin này — dưới đây là thông tin từ web (chưa kiểm)."

## Điều bước kiểm này chưa làm được

Chương trình biết [4] trỏ tới một đoạn có thật. Nó chưa biết đoạn 4 có thật sự nói điều câu trả lời viết không. Ở ví dụ chính thì có: đoạn 4 ghi đúng giá vé trẻ em. Nhưng đó là do người đọc đối chiếu, không phải do chương trình kiểm.

Vì vậy "có số nguồn" chưa phải "đã kiểm đúng". Phần nghĩa chỉ được đo khi chấm câu trả lời (bài 19); riêng con số thời tiết, khoảng cách có bước kiểm con số (bài 24).

Bước kiểm cũng không biết một danh sách có đủ hay không (dòng "có thể chưa đủ": mục "Quyết định nhỏ hơn").

## Câu về tỉnh khác từng lọt qua bước kiểm; nay một đoạn dặn che

Câu *"Từ Huế vào Hội An thì ở Hội An nên ăn món gì?"* có chữ "Huế", nên bước xếp loại (một lần gọi model, bài 22) thường cho nó đi đường "về Huế" (113 trên 120 lần đo 23/11). Một lượt đo trưa 23/11, model viết: "Món duy nhất được nhắc đến là cơm gà Hội An, gồm thịt gà xé phay dùng cùng cơm vàng [11]." Đoạn 11 có thật: một dòng trong bài một quán cơm tấm ở Huế. Câu qua cả ba luật: một câu ngoài kho được trả lời bằng kho (vì sao: bài 21).

Từ chiều 23/11 (tính năng thứ 50), với model đang chạy, chương trình nối một đoạn dặn sau lời dặn trả lời: kho chỉ viết về Huế; ý hỏi việc diễn ra ở tỉnh, thành khác (ăn gì, chơi gì) coi như bằng chứng không nêu. Vẫn trả lời: đường đi giữa Huế và nơi khác, món mang tên nơi khác mà tìm tại Huế, nơi model không chắc có thuộc Huế không. Model vẫn là bên quyết; nó viết câu từ chối cố định, chương trình nhận ra như mọi lượt.

## Quyết định và lý do

### 1. Vì sao số nguồn sai thì rút cả câu trả lời, không chỉ gỡ số sai?

- **Đã chọn:** phạm một trong ba luật là rút cả câu, hiện lời báo và nút "Thử lại".
- **Vì sao:** luật ghi từ đặc tả lúc dựng hệ thống: số nguồn không khớp là lỗi của cả câu trả lời; không trả một phần, không tự sửa, không tự gọi lại. Lập luận đứng sau (không phải số đo): một số nguồn không có thật nghĩa là không biết ý đó dựa vào đâu. Về sau ba chỗ nới luật này, mỗi chỗ một quyết định riêng: gỡ câu từ chối nối ở cuối, chạy lại hẹp, viết lại một lần (quyết định 5).
- **Cách khác:** chỉ gỡ số sai, hoặc gỡ câu chứa số sai: chưa thử. Cách nhẹ đó đang dùng cho con số thời tiết và khoảng cách (bài 24).
- **Cái giá:** câu trả lời đúng mà quên số nguồn cũng bị rút. Lỗi hiếm ("Ý chính"), nhưng vẫn có lượt bị rút (mục "Giới hạn đã biết").

### 2. Vì sao câu từ chối là một câu cố định, và chương trình so đúng từng chữ?

- **Đã chọn:** một câu ghi sẵn trong lời dặn; chương trình nhận ra lượt từ chối bằng cách so chữ.
- **Vì sao:** quyết định đã ghi: câu từ chối cố định là một phần của điều kiện "chỉ trả lời từ kho", và các phép đo dựa vào nó. Ngày 21/11 chủ dự án ghi nó vào danh sách các sàn không được nới.
- **Cách khác:** để model tự viết lời từ chối cho tự nhiên hơn: không làm. Cho model trả lời phần có bằng chứng: đã đo, bỏ (mục "Đã so").
- **Cái giá:** lời từ chối cứng, giống nhau mọi lần; model viết lệch một chữ thì chương trình không nhận ra là từ chối, và câu đó (không có số nguồn) bị rút như một lỗi.

### 3. Vì sao sửa chuyện "[Nguồn n]" ở chương trình, không dặn model thêm?

- **Đã chọn:** bộ kiểm nhận cả [n] lẫn [Nguồn n], đưa hết về [n].
- **Vì sao:** đã đo (mục "Đã so"): lỗi số nguồn trên 1.600 câu từ 69 xuống 14, 0 câu đang đúng bị đổi, không tốn lần gọi nào. Model chép đúng nhãn nó thấy trong ngữ cảnh.
- **Cách khác:** thêm một câu dặn: không làm; bài 15 cho thấy mỗi câu dặn thêm hay làm hỏng loại câu khác.
- **Cái giá:** không đáng kể.

### 4. Vì sao chạy lại cả lượt một lần, và chỉ ở lượt đang kèm câu trả lời liền trước?

- **Đã chọn:** lượt bị rút ở bước kiểm sau khi viết (số nguồn hay phép kiểm khác), mà lịch sử đang mang câu trả lời liền trước, thì ô chat gỡ chữ đã hiện (nếu có) và chạy lại một lần không kèm câu trả lời cũ. Lượt có câu cố định hoặc lượt sửa lịch thì không (cuộc đã có lịch: "Chi tiết để tra").
- **Vì sao:** đo sáng 22/11 (Claude Sonnet 5.5): sau khi mở việc nhớ câu trả lời, tin kiểu "bỏ chợ Đông Ba đi" ra màn hình lỗi 3 trên 7 lần, vì model chép lại lời cũ không ghi số nguồn. Đo lại sau bản sửa: 0 trên 5 lần ra màn hình lỗi (người thứ hai kiểm).
- **Cách khác:** giữ chữ tới khi kiểm xong: sáng 22/11 không chọn vì đổi cách hiện chữ của mọi lượt; từ 15:42 22/11 đã làm cho model đang chạy (bài 6). Chạy lại ở mọi lượt bị rút: không làm.
- **Cái giá:** chờ thêm vài giây và tiền tính cả hai lần gọi model ở các lượt đó; lần hai cũng hỏng thì người dùng vẫn thấy lời báo lỗi.

### 5. Vì sao bước viết lại một lần bị bỏ trưa 22/11 mà 14:47 cùng ngày lại mở?

- **Đã chọn:** mở bước viết lại với điều kiện "model đã tự tìm ít nhất một lần mà chữ nộp không có số nguồn nào", CÙNG hai thay đổi ở khâu tìm (bài 23) và trần tìm 3 (bài 21). Lần viết lại không có công cụ, chữ mới kiểm như thường; vẫn không có số nguồn thì câu từ chối cố định.
- **Vì sao:** đã đo (Claude Sonnet 5.5, tin của gia đình, 6 lần mỗi bên; "Đã so"). Đứng riêng, nó đổi màn hình lỗi lấy câu trả lời thiếu hai ý kho có; cùng khâu tìm mới và lần tìm thứ ba thì hết màn hình lỗi và đủ hai ý.
- **Cách khác:** bản đứng riêng với điều kiện "đã tìm HẾT lượt": đã đo, không mở, vì còn lọt một tin (mục "Đã so"). Nới bước kiểm để chữ không nguồn tới người dùng: không làm.
- **Cái giá:** lượt có viết lại lâu hơn khoảng 10 giây, thêm một lần gọi model; trong lúc đó người dùng chỉ thấy thẻ chờ; ca viết lại chưa nhìn trên trình duyệt. Các chỗ chưa đo: mục "Đã so", giới hạn.

### 6. Vì sao che câu về tỉnh khác bằng một đoạn dặn, chưa chặn ở bước xếp loại hay chữa ở gốc?

- **Đã chọn:** đoạn dặn, chỉ trên model đang chạy; vẫn giữ công cụ liệt kê bài (bài 21).
- **Vì sao:** tiêu chí ghi trước chọn thử lời dặn trước (rẻ, lùi bằng một dòng cấu hình), bước xếp loại để lùi nếu lời dặn trượt. Lời dặn đạt: câu ví dụ 12 ⇒ 0 trên 20, câu Đà Nẵng 10 ⇒ 0 trên 10, không câu kho có nào thành từ chối.
- **Cách khác:** chặn ở bước xếp loại (cũng do model): chưa thử. Bớt công cụ liệt kê ở câu không xin danh sách: chưa làm, đã ghi. Bỏ dòng thực đơn mang tên tỉnh khác khỏi bằng chứng: hồ sơ có nêu, chưa thử.
- **Cái giá:** xác suất: 0 trên 20 chỉ cho nói mức hở dưới khoảng 14 %. Lời dặn lượt có công cụ dài gần gấp đôi. Đường model cũ chưa có.

## Nếu… thì sao

Đọc từ chương trình, trừ dòng ghi **(đã thử)** hay "đã đo". Lời báo trong ngoặc kép là nguyên văn.

| Nếu | Hệ thống làm gì | Người dùng thấy gì | Đã có chưa / ai làm gì |
|---|---|---|---|
| câu trả lời ghi số nguồn không có, hoặc thiếu hẳn số nguồn mà model chưa tự tìm lần nào | rút lại (model đang chạy: chữ chưa hề hiện; model trả chữ dần: xoá chữ đã hiện) | "Câu trả lời không đáp ứng yêu cầu trích dẫn." và nút "Thử lại" | người dùng bấm "Thử lại" |
| ca trên, ở lượt đang kèm câu trả lời liền trước **(đã thử)** | ô chat gỡ chữ, chạy lại cả lượt một lần | chờ lâu hơn, rồi câu trả lời hoặc lời báo như dòng trên | có từ 22/11; đo lại: 0 trên 5 lần ra màn hình lỗi |
| model đã tự tìm ít nhất một lần (ví dụ tin dài nhiều ý, hết lượt tìm) rồi nộp chữ không có số nguồn nào | viết lại một lần, không công cụ, từ các đoạn đã gom; vẫn không có ⇒ câu từ chối cố định | thẻ chờ đứng lâu hơn (cả lượt thêm khoảng 10 giây), rồi câu trả lời có nguồn; hoặc "Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này." | đã đo trên một tin; có từ 14:47 22/11; chưa nhìn trên trình duyệt (trước đó: "Chi tiết để tra") |
| model viết phần có nguồn rồi nối câu từ chối ở cuối | gỡ câu từ chối, kiểm phần còn lại | câu trả lời phần có nguồn | có từ 21/11 |
| kho không đủ, kể cả câu hỏi việc ở tỉnh, thành khác | model trả câu từ chối; chương trình tra web một lần (bài 25) | câu từ chối; có mục web thì thay bằng câu dẫn sang mục web; tin nhiều ý: ý đó thành dòng "Tư liệu chưa có thông tin về: …" | đúng thiết kế; câu tỉnh khác: lượt đo 0 trên 20, có lúc bị chặn sớm ở bước xếp loại (câu "Mình chỉ hỗ trợ…", không mục web) |
| câu trả lời có con số thời tiết hay khoảng cách không khớp kết quả công cụ | gỡ câu chứa con số đó | câu trả lời thiếu câu đó | có (bài 24) |

## Dễ nhầm

- **"Có số nguồn là đã đúng."** Không. Số nguồn có thật chỉ cho biết đoạn đó tồn tại và đã được đưa cho model.
- **"Câu từ chối là do model tự nghĩ ra lời."** Không. Đó là một câu cố định ghi trong lời dặn; chương trình so đúng từng chữ.

## Câu hỏi tự kiểm

<details>
<summary>1. Ba luật kiểm số nguồn là gì, và luật nào bắt câu "Tôi không tìm thấy đủ thông tin… [3]"?</summary>

Có ít nhất một số nguồn · mọi số là của một nguồn đã thật sự đưa cho model · câu từ chối không kèm số nguồn. Câu đó phạm luật thứ ba.

</details>

<details>
<summary>2. Câu "ở Hội An nên ăn món gì" trưa 23/11 được trả lời kèm số [11] có thật. Như vậy đã đúng chưa, và nay cái gì chặn nó?</summary>

Chưa: chương trình chỉ biết đoạn 11 tồn tại (một dòng trong bài một quán ở Huế), không biết nó có trả lời câu hỏi không. Nay một đoạn dặn bảo model coi ý về tỉnh khác là kho không nêu. Đó là lời dặn: chỉ nói được "lượt đo 0 trên 20", không phải "luôn luôn".

</details>

## Cấu hình đang chạy

*Chép từ hệ thống đang chạy sau 14:47 ngày 22/11/2026; hàng đoạn dặn tỉnh khác chép 13:41 23/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Dạng số nguồn được nhận | [n] và [Nguồn n], không phân biệt hoa thường; đưa hết về [n] khi hiện | model đôi khi chép nguyên nhãn của ngữ cảnh | đã đo trước và sau khi nhận cả hai dạng (mục "Đã so") |
| Câu từ chối khi kho không đủ | "Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này." | chương trình so đúng từng chữ | chưa thử câu khác |
| Câu cho câu hỏi ngoài phạm vi | "Mình chỉ hỗ trợ thông tin về văn hoá và du lịch Huế. Bạn muốn hỏi gì về Huế không?" | do bước xếp loại câu quyết định, không qua model viết (bài 22) | — |
| Các câu được tính là từ chối khi đo | hai câu trên, cộng ba câu "mình không làm thay được" (đặt chỗ, gửi tin, xem tình trạng phòng; bài 4) | thiếu một câu trong danh sách này thì một câu ngoài kho bị thay chữ sẽ bị đếm nhầm là "được trả lời" | — |
| Khi bước tìm không ra đoạn nào dùng được | đặt câu từ chối ngay, không gọi model | đỡ một lần gọi model | — |
| Câu từ chối nối ở cuối một câu trả lời có nguồn | gỡ câu từ chối, giữ phần có nguồn | trước khi có việc này, cả câu bị rút lại | có từ 21/11 |
| Dòng "có thể đã thay đổi" | nối khi câu trả lời trích bài thuộc nhóm vé, địa điểm, lễ hội, hoặc bài lưu trú (kể cả bài chỉ được nêu tên qua nguồn liệt kê, "gần một điểm" hay thẻ nơi; bài 24) | giá và giờ có thể đổi mà kho chưa sửa | — |
| Nguồn hiện dưới câu trả lời | chỉ các đoạn có số được nhắc trong câu trả lời | — | — |
| Viết lại một lần khi chữ nộp không có số nguồn (`het_luot_viet_lai`) | mở 14:47 22/11; chỉ khi model đã tự tìm ít nhất một lần; không ở câu cố định; cả ô chat lẫn đường không hiện chữ dần | thay màn hình lỗi bằng câu trả lời từ bằng chứng đã gom, hoặc câu từ chối | đứng riêng: không mở; cùng bộ: mở (mục "Đã so") |
| Chạy lại cả lượt khi bị rút ở bước kiểm sau khi viết | 1 lần, chỉ ở ô chat, ở lượt đang kèm câu trả lời liền trước; không ở lượt có câu cố định và lượt sửa lịch (từ 22/11; cuộc đã lập lịch: từ 16:08 22/11, trước đó không chạy lại) | người dùng khỏi gặp màn hình lỗi ở tin kiểu "bỏ X đi" | trước khi có: 3 trên 7 lần ra màn hình lỗi; sau: 0 trên 5 (đo 22/11, Claude Sonnet 5.5) |
| Dòng "danh sách có thể chưa đủ" (`danh_sach_noi_that`) | mở từ 20/11; câu xin danh sách có nguồn kho, trừ lượt lịch, lượt có dòng "Tư liệu chưa có…", và câu hỏi về một nơi đã có tên trong nguồn | nói thật giới hạn của việc tìm theo đoạn | — |
| Đoạn dặn câu hỏi việc ở tỉnh, thành khác (`noi_khac_tu_choi`) | dòng cấu hình ghi mở 13:11, vào nhánh chính 13:28 23/11 (tính năng thứ 50); chỉ khi model viết là Claude; nối ngay sau lời dặn trả lời ở lượt trả lời không công cụ, lượt có công cụ (cả bản có lịch sử) và bản tin nhiều ý; lượt biểu mẫu, viết lịch, xếp loại câu, trò chuyện không nhận. Lời dặn lượt có công cụ: 1.233 ⇒ 2.311 ký tự. Máy chủ đọc dòng này lúc khởi động: đổi về false rồi khởi động lại là lùi | ý hỏi việc diễn ra ở tỉnh, thành khác (ăn gì, chơi gì, ở đâu, mua gì, tham quan gì) coi như bằng chứng không nêu; ba ngoại lệ: đường đi giữa Huế và nơi khác, món / quán / sản phẩm / sự kiện mang tên nơi khác mà người dùng muốn tìm tại Huế, nơi model không chắc có thuộc Huế không. Đoạn dặn tả LOẠI tình huống, không nêu tên nơi hay món nào của bộ đo | đã đo mở ↔ tắt cùng buổi (mục "Đã so"); đường model cũ: chưa có đoạn này |

## Đã so

### Nhận cả hai cách ghi số nguồn

**Vấn đề thật đã gặp.** Ngữ cảnh ghi nhãn mỗi đoạn là "[Nguồn 1]", "[Nguồn 2]". Lời dặn bảo model ghi "[1]", "[2]". Phần lớn lần model làm đúng, nhưng thỉnh thoảng nó chép nguyên nhãn "[Nguồn 2]" vào câu trả lời. Bộ kiểm lúc đầu chỉ hiểu "[2]", nên coi đó là "câu trả lời không có nguồn" và báo lỗi, dù câu trả lời đúng.

**So gì.** Trước và sau khi cho bộ kiểm nhận cả hai dạng; model gpt-6-luna.

| Đo gì | Trước | Sau |
|---|---|---|
| Số lần model ghi dạng "[Nguồn n]" | 24 trên 465 lần viết | (không đổi; đây là thói quen của model) |
| Số lỗi số nguồn trên 1.600 câu | 69 | 14 |
| Số câu đang đúng bị đổi | — | 0 |

**Đọc bảng này thế nào.** Model "sai" một cách hợp lý: nó chép đúng thứ nó thấy. Sửa ở chương trình (nhận cả hai dạng) chắc hơn dặn model thêm một câu, và không tốn lần gọi nào.

**Đã chọn: nhận cả hai dạng.**

### Từ chối cả câu, hay trả lời phần có bằng chứng

Đã kể ở bài 15: cho model trả lời một phần làm câu từ chối nhầm giảm từ 13 xuống 1 nhưng để 2 câu ngoài kho được trả lời. Điều kiện "0 câu ngoài kho được trả lời bằng kho" thắng, nên câu từ chối giữ nguyên là từ chối cả câu. Về sau câu hỏi có **nhiều ý** được xử lý bằng một đường riêng (bài 23).

### Câu hỏi về việc ở tỉnh, thành khác: tìm nguyên nhân, rồi che bằng một đoạn dặn

**Vấn đề thật đã gặp.** Điều kiện "0 câu ngoài kho được trả lời bằng kho" có một câu đối chứng: *"Từ Huế vào Hội An thì ở Hội An nên ăn món gì?"* (kho có bài đường đi Huế – Hội An từ 22/11, không có bài nào về món ở Hội An). Mốc 21/11 (Claude Sonnet 5.5, mức cao, chưa có công cụ liệt kê bài): 1 trên 40 lần được trả lời bằng kho — ba lượt mốc tối 21/11 0 trên 30, một lượt 15:49 0 trên 5, một lượt 21:35 1 trên 5 (cùng câu "cơm gà Hội An… [11]"). Cùng ngày, hai lượt thử một bản chưa gộp (báo model "đã hết lượt tìm") hở 4 trên 5 và 2 trên 5. Trưa 23/11 trên nhánh chính: 3 trên 10. Lượt dùng như người thật trên trình duyệt cùng trưa (bản chưa có đoạn dặn), ba cuộc mới cùng câu: lần 1 câu từ chối kèm mục web; lần 2 trả lời từ kho với "cơm gà Hội An"; lần 3 giống hệt lần 2 từng chữ, về sau 0,008 giây vì bộ nhớ câu trả lời đã giữ bản lần 2 (bài 34). "Được trả lời bằng kho" ở mọi số dưới đây = không phải câu từ chối và có ít nhất một nguồn.

**Tìm nguyên nhân.** Mỗi "ô" là một bản thử của hệ thống, hỏi câu đối chứng 20 lần, cùng buổi 23/11, Claude Sonnet 5.5 mức cao, gọi thẳng phần trả lời (không qua trang web), đoạn dặn tắt. Ô đầu bỏ một bài; ô thứ hai tắt cả một nhóm 14 thứ cùng lúc; hai ô sau tách nhóm đó ra. Ngưỡng kết luận ghi trước cho ba ô đầu; ô cuối chạy sau khi đã thấy số, không có ngưỡng ghi trước. Chỉ một câu được đo.

| Ô | Đổi gì so với ô mốc | Khác ô ngay trên ở đâu | Được trả lời bằng kho | Đọc thế nào |
|---|---|---|---|---|
| mốc cùng buổi | không đổi gì | — | 12 / 20 | chỗ hở có thật |
| giả thuyết đầu | bỏ 4 đoạn của bài mới "Đi từ Huế tới Hội An" khỏi lần tìm đầu, không lấy đoạn bù (bài này đứng hạng 2, 4, 5, 10) | hai thứ: mất bài mới và ngữ cảnh ngắn hơn | 11 / 20 | ngưỡng ghi trước "từ 4 trở lên ⇒ không phải nguyên nhân": giả thuyết bị bác |
| tắt cả nhóm | tắt 12 tính năng và đưa hai giới hạn về như 21/11 (tự tìm kho 2 lần thay vì 3, gọi model 4 vòng thay vì 5); kho và phần code không có công tắc giữ như hôm nay | 14 thứ cùng lúc | 1 / 20 | thứ gây hở nằm trong nhóm 14 thứ này |
| chỉ trả hai giới hạn | chỉ hai giới hạn tìm và vòng | còn 2 trong 14 thứ | 8 / 20 | không phải hai giới hạn |
| chỉ tắt công cụ liệt kê bài | công cụ mở 22/11 cho câu xin danh sách; tắt nó thì trần vòng cũng bớt 1 | còn 1 trong 14 thứ | 1 / 20 | mức hở về gần mốc 21/11 ⇒ nghi phạm chính |

Ở cả 12 lần trả lời sai của ô mốc, model không hề dùng công cụ liệt kê bài. Vậy thứ làm model bớt từ chối không phải kết quả của công cụ, mà là việc công cụ có mặt trong danh sách (cùng một vòng gọi nó mang theo). Đây là cách nhóm đang hiểu, chưa phải kết luận chắc: mới thấy trên một câu, ô cuối không có ngưỡng ghi trước, và ngày 21/11, khi chưa có công cụ, câu này đã lọt 1 trên 40 lần. Điều thấy được về vòng: ô "chỉ trả hai giới hạn" (4 vòng + 1 của công cụ) và ô "chỉ tắt công cụ" (5 vòng + 0) cùng 5 vòng mà ra 8 / 20 ↔ 1 / 20. Vì sao có mặt mà đổi cách trả lời: chưa thấy ghi lý do. Phần giảng về harness: bài 21, "Đã so" dòng 8.

**Mở ↔ tắt đoạn dặn.** Cùng buổi 23/11, cùng cây, chỉ đổi một công tắc; câu nhóm 2–6 do phiên đo chọn; một người chấm độc lập đọc tay 100 lượt của nhóm 2–6.

| Nhóm câu | Lần mỗi bên | Tắt | Mở | Ngưỡng ghi trước |
|---|---|---|---|---|
| câu đối chứng | 20 | 12 được trả lời bằng kho | 0 (19 câu từ chối model viết, 1 chặn ở xếp loại) | mở: 0 |
| "Từ Huế ra Hà Nội thì ở Hà Nội nên ăn món gì?" | 10 | 0 | 0 | mở: 0 |
| "Từ Huế vào Đà Nẵng thì ở Đà Nẵng nên đi chơi những đâu?" | 10 | 10 được trả lời bằng kho (dòng lạc trong bài Hải Vân Quan, đèo Hải Vân) | 0 | mở: 0 |
| hai câu đường đi Huế – Hội An | 5 mỗi câu | 10 / 10 có nguồn | 10 / 10 có nguồn, cùng nội dung | không tụt |
| câu ghép "đi Hội An bằng gì tiện nhất, tới rồi nên ăn món gì" | 5 | 5 / 5 trả lời đường đi, kèm "cơm gà Hội An" lạc 5 / 5 | 5 / 5 trả lời đường đi; phần ăn là dòng "Tư liệu chưa có thông tin về: các món nên ăn khi đã tới Hội An." (chữ một lượt) | không tụt |
| ba câu món / quán mang tên nơi khác bán tại Huế (cơm gà Hội An, mì Quảng, cà phê phong cách Nhật / Hàn) | 3 mỗi câu | 9 / 9 trả lời | 9 / 9 trả lời | không tụt |
| sáu câu nhóm rìa Huế | 1 | 4 trả lời, 1 chặn ở xếp loại, 1 từ chối | như bên tắt | không đổi |

Ở mọi lượt bị từ chối bên mở (câu đối chứng, Hà Nội, Đà Nẵng), model không tự tìm kho lần nào: nó quyết từ chữ câu hỏi. Câu đối chứng bên mở nhanh hơn: trung vị 5,0 so với 10,3 giây, 2 so với 4 lời gọi model.

**Đọc bảng này thế nào.** Đoạn dặn tác dụng ở cả ba câu đang hở (câu đối chứng, câu Đà Nẵng, và phần "ăn gì" của câu ghép) và không làm câu kho có nào thành từ chối trên mẫu này. 0 trên 20 chỉ cho nói mức hở thật dưới khoảng 14 %; 10 lần mỗi câu chỉ bắt được mức hở cỡ 25 % trở lên.

**Chỗ hở có rộng hơn chuyện tỉnh khác không** (đo trên nhánh chính, chưa có đoạn dặn): năm câu một ý về thứ ở Huế mà kho không có nhưng có một dòng chạm sượt, ghi trước 6 lần mỗi câu, chạy được 18 lượt. Bệnh viện cho khách nước ngoài, nhà thuốc mở buổi tối, sân tennis: từ chối 11 / 11. Massage chân 2 / 4 và hồ bơi bán vé lẻ 3 / 3 được trả lời từ thứ kho có thật (suối khoáng có bể bơi trong vé cổng, làng du lịch có ngâm chân kèm xoa bóp), kèm câu nói thật là không thấy cơ sở chuyên. Đoạn dặn không nhắm kiểu câu này. Theo tiêu chí ghi trước, chỉ cần một lượt lấy dòng chạm sượt làm câu trả lời là đoạn dặn chưa đủ. Ô này mới chạy 18 trên 30 lượt đã định và CHƯA ai chấm theo tiêu chí đó: năm lượt không từ chối do phiên điều phối đọc tay, xếp vào loại "kho có câu trả lời gần" (người viết bài đọc lại, cùng nhận xét) — không phải người chấm độc lập.

**Đã chọn: mở đoạn dặn (dòng cấu hình ghi mở 13:11, vào nhánh chính 13:28 23/11), giữ công cụ liệt kê bài** (nó chữa câu "những quán nào có…", bài 24).

**Giới hạn của các phép đo.** Gọi thẳng phần lõi. Một lượt qua đường gửi dần của máy chủ tạm với công tắc mở (13:13–13:15 23/11): sổ máy chủ có 7 lượt hỏi, 3 lượt là câu từ chối kèm mục web có nội dung, 4 lượt trả lời có nguồn (2 tới 10 nguồn); sổ không ghi câu hỏi, nên lượt nào là câu nào và chữ câu trả lời theo báo cáo của phiên điều phối (chữ không lưu thành file). Chưa nhìn trên trình duyệt với bản đã mở. Đường model cũ không đo trong đợt này; ngày 21/11 nó đã hở câu đối chứng 2 trên 10 và 3 trên 5 lần, lúc chưa có công cụ liệt kê bài; Claude cùng ngày cũng đã lọt 1 trên 5 lần ở một lượt. Năm câu "chạm sượt" chỉ là 18 lượt.

### Màn hình "Thử lại" ở tin dài nhiều ý: viết lại một lần

**Vấn đề thật đã gặp.** Ở một tin 4 ý của một gia đình, màn hình "Thử lại" hiện ở 3 trên 6 lần. Đọc chữ của 5 câu từng bị gỡ: model đã dùng hết hai lần tìm thêm (lúc đó trần là 2), vẫn muốn tìm tiếp; công cụ tìm lúc đó đã bị cất nên nó nộp một câu giữ chỗ kiểu "tôi cần tìm thêm về …", không có nguồn, nên bị rút.

**So gì.** Bản chữa: gặp đúng ca đó thì gọi model viết thêm một lần từ những gì đã tìm được. Một lượt thật 44 câu (3,77 USD), tin đó hỏi 6 lần mỗi bên, model Claude Sonnet 5.5, ngày 22/11.

| Đo gì | Chưa chữa | Có bản chữa |
|---|---|---|
| Số lần ra màn hình lỗi | 3 trên 6 | 0 trên 6 |
| Con số bịa trong câu viết lại | — | 0 trên 5 (người thứ hai kiểm) |
| Câu nói "tư liệu chưa có" hai ý kho có (giá vé lẻ Đại Nội; người từ 60 tuổi được giảm) | 0 (ba lượt bình thường trả lời đúng cả hai) | 4 trên 5 câu viết lại |

**Đọc bảng này thế nào.** Bản chữa đổi một màn hình lỗi lấy một câu trả lời thiếu ý mà người dùng không biết là thiếu. Gốc của lỗi nằm ở khâu tìm: hai dữ kiện đó chỉ về tới ở lần tìm thứ hai, thứ ba do model tự gọi.

**Đã chọn lúc đó: không mở đứng riêng**, theo tiêu chí ghi trước và thứ tự lỗi chủ dự án đã chốt (thiếu ý nặng hơn một lần "Thử lại").

**Đo tiếp, rồi mở cùng bộ (14:47 22/11).** Nhóm chữa gốc ở khâu tìm (bỏ vế cụt, tách câu tìm gộp của model; bài 23), nâng trần tìm lên 3 (bài 21). Cùng tin đó, 6 lần mỗi bên, Claude Sonnet 5.5 ("lượt ba bên": ba bản chạy cùng lúc trên cùng bộ tin):

| Đo gì | Bản đang chạy | Khâu tìm mới | Khâu tìm mới + viết lại | Cả bộ, trần 3 |
|---|---|---|---|---|
| Màn hình lỗi | 5 trên 6 | 3 trên 6 | 0 trên 6 | 0 trên 6 |
| Đoạn giá vé lẻ Đại Nội có trong bằng chứng | 2 trên 6 | 6 trên 6 | 6 trên 6 | — |
| Đủ cả hai ý kho có | 0 trên 6 | 1 trên 6 | 1 trên 6 | 6 trên 6 |

Ba cột đầu là một lượt (57 câu, 4,46 USD); cột cuối là lượt nối (9 câu, 1,09 USD). Lượt nối lộ một khe (tin phòng gym: model tìm 2 lần rồi tự dừng, chữ không nguồn, lọt lưới), nên điều kiện của bước viết lại đổi từ "đã tìm hết lượt" thành "đã tự tìm ít nhất một lần" và được thử lại ở lần thử cuối. Lần thử cuối trên đúng cấu hình mở (6 câu): không màn hình lỗi; tin phòng gym (kho không có) ra câu từ chối 3 trên 3; tin của gia đình đủ hai ý 2 trên 2. Tin thường, tin kho thiếu, tin nhiều ý khác: không lỗi, không bịa ở mọi bên. **Đã chọn: mở cả bộ.**

**Giới hạn của các phép đo.** Hai phép so đầu đo với gpt-6-luna, cuối tháng 10. Phép so cuối chỉ trên MỘT tin, 6 lần mỗi bên; chính bản đang chạy với tin đó trong ngày tự dao động 3, 4, 5 lần lỗi trên 6, nên lợi "hết màn hình lỗi" chưa chứng minh được ngoài tin này. Điều kiện "ít nhất một lần" chưa gặp lượt thật; cuộc đã có lịch lưu (bước viết lại vẫn chạy ở đó theo chương trình) và model cũ chưa đo.

## Quyết định nhỏ hơn

**Vì sao dòng "danh sách có thể chưa đủ" do chương trình nối, không nhờ model viết?** Câu người dùng khớp khuôn "xin danh sách" (những / các … nào, kể hết, liệt kê) và có nguồn kho thì chương trình nối vào dòng ghi chú câu cố định "Danh sách trên chỉ gồm những nơi có trong các bài tìm được, nên có thể chưa đủ."; mở từ 20/11. Việc nhận ra là phép so khuôn chữ, không gọi model; dòng này không làm danh sách đủ hơn. Vì sao: ghi trong chương trình — trợ lý tìm theo đoạn, không lọc cả kho theo đặc điểm, nên câu "những quán nào có X" thường chỉ ra một phần danh sách mà không nói là có thể thiếu (6 trên 18 câu mẫu dạng này; "kể hết các nơi vừa nêu" thiếu 5 trên 6 lần đo 20/11); nối bằng chương trình thì chữ gửi model không đổi. Cách khác: dặn model tự nói "có thể chưa đủ": không làm; từ 22/11 có thêm công cụ kể theo mục lục của kho (bài 24). Cái giá: khuôn chữ hẹp (cách nói lạ không khớp; câu xin một gợi ý như "quán nào ngon" cố ý không nhận; câu gõ không dấu không được nhận); lượt đã kể theo mục lục kho vẫn nhận dòng này, hai lời rào chồng nhau (đọc từ chương trình, chưa thử).

**Bước viết lại một lần đã hết màn hình "Thử lại" ở tin dài nhiều ý ngay từ trưa 22/11. Vì sao trưa đó không mở, mà 14:47 lại mở?** Đứng riêng, 4 trong 5 câu viết lại nói "tư liệu chưa có" đúng hai ý kho có; theo thứ tự lỗi chủ dự án đã chốt, thiếu ý nặng hơn một lần "Thử lại". Lúc 14:47 nó mở cùng hai thay đổi ở khâu tìm và trần 3: lần tìm thứ ba đem về được ý còn lại, nên tin đó đủ hai ý 6 trên 6 lần; bước viết lại chỉ còn là chỗ đỡ khi model vẫn nộp chữ không nguồn.

**Vì sao "đúng một câu từ chối cố định" quan trọng với phép đo?** Chương trình nhận ra lượt từ chối bằng cách so chữ, nên đếm được chính xác bao nhiêu câu bị từ chối, từ chối nhầm, hay câu ngoài kho lọt qua; nó cũng là tín hiệu để mở mục tra web (quyết định 2).

**Vì sao không dùng một model thứ hai để kiểm câu trả lời có đúng với nguồn không?** Chưa thử trên đường người dùng. Việc đó hiện chỉ có ở phép đo: một model chấm điểm câu trả lời so với đáp án mẫu (bài 19).

**Vì sao chữ lúc hiện trước rồi mới kiểm, lúc được giữ tới khi kiểm xong?** Bài 6, quyết định 4.

**Vì sao không gọi model khi bước tìm không ra đoạn nào dùng được?** Đặt câu từ chối ngay, đỡ một lần gọi model.

## Giới hạn đã biết

- **Chưa kiểm nghĩa** (đã nói ở trên).
- **Thiếu số nguồn chỉ bị phát hiện ở cuối.** Với model trả chữ dần, người dùng thấy chữ rồi thấy nó bị rút. Với model đang chạy, từ 15:42 22/11 chữ được giữ tới khi qua kiểm nên người dùng chỉ thấy lời báo. Lượt qua kiểm đã nhìn trên trình duyệt 22/11 (16 / 16 lượt thành công, không chữ nào hiện trước khi cả câu hiện); ca bị rút và ca viết lại chưa gặp trên trình duyệt.
- **Ở tin dài, phần chữ trống khoảng 20–30 giây** (giá của việc giữ chữ; số đo trên giao diện cũ 22/11, lúc đó chỉ có một dòng trạng thái đứng yên). Từ 23/11 trong lúc đó là thẻ chờ: dòng trạng thái đổi theo từng bước máy chủ báo, tên các bài đã tìm thấy được thêm sau mỗi lần tìm; lúc model viết câu cuối, chữ trên thẻ không đổi; chỉ con đò và nét sông còn chạy (bài 5). Lúc gộp giao diện mới (sáng 23/11), máy chụp tự động thẻ chờ của tin gia đình bốn ý ở giây 2, 5, 9, 14, 20: tên bài tăng từ 3 lên 6 qua các lần tìm. Chưa có số đo thời gian chờ của tin dài trên giao diện mới.
- **Câu trả lời bị rút lại vẫn xảy ra.** Ở một lượt đo với người dùng mô phỏng ngày 21/11: 3 trên 48 lượt hỏi của gpt-6-luna và 4 trên 53 lượt hỏi của Claude Sonnet 5.5 có câu bị rút. Con số này gồm cả câu bị rút do bước kiểm con số thời tiết, không riêng do số nguồn, và đo trước bản sửa 13:51 21/11 (từ đó con số lạ ở lượt thường chỉ bị gỡ câu); mới một người đọc.
- **Dòng "có thể đã thay đổi" chỉ áp cho bốn nhóm bài:** vé, địa điểm, lễ hội, và bài "Lưu trú ở Huế". Ba nhóm đầu do chủ dự án chọn ngày 02/11: giờ, giá vé, ngày lễ hội đổi theo năm mà kho không ghi ngày nguồn. Bài lưu trú được thêm 14/11 vì hạng cơ sở có thể đã đổi. Nhóm khác (món ăn, quán) không có dòng này.
- **Một câu trả lời đúng nội dung mà quên số nguồn cũng bị rút**, vì chương trình không phân biệt được với một câu bịa.
- **Câu hỏi việc ở tỉnh, thành khác chỉ được che bằng lời dặn, và chỉ trên model đang chạy.** Đường model cũ chưa có đoạn dặn và đã hở sẵn (21/11: 2 trên 10, 3 trên 5 lần); Claude ngày 21/11 cũng đã lọt 1 trên 40 lần, khi chưa có công cụ liệt kê bài. Bên mở, lượt đo 0 trên 20 chỉ cho nói mức hở dưới khoảng 14 %. Chưa chữa ở gốc (công cụ liệt kê bài vẫn có mặt ở mọi lượt hỏi đáp). Câu ngoài kho kiểu khác mới thử 18 lượt, chưa ai chấm theo tiêu chí ghi trước. Một lần hở còn sót có thể bị bộ nhớ câu trả lời giữ cho người hỏi sau (bài 34).
- **Người đọc không thấy ý nào đến từ nguồn nào.** Vì số [n] không hiện trong chữ, khung "Nguồn đã dùng" chỉ cho biết cả câu trả lời dựa vào những bài nào. Đây là lựa chọn của chủ dự án về giao diện.

## Chi tiết để tra

- Đếm lỗi số nguồn: 0 trên 489 lần viết (gpt-6-luna, đếm ngày 30/10); 0 trên 93 lượt (một lượt rà ngày 21/11 trên gpt-6-luna và các mức suy luận của Claude Sonnet 5.5).
- Việc nhận cả hai dạng số nguồn được sửa ngày 25/10.
- Trường hợp "câu trả lời có nguồn rồi nối câu từ chối ở cuối" được thấy ở 1 trên 3 lượt của một câu mà kho chỉ có một phần, ngày 21/11.
- Khi mục web có nội dung, máy chủ vẫn giữ nguyên câu từ chối trong kết quả của nó (các phép đo đọc câu này); chỉ giao diện thay bằng câu dẫn sang mục web.
- Câu hỏi nhiều ý: ý nào kho không có thì model ghi một dòng mở đầu bằng "Tư liệu chưa có thông tin về:"; dòng này không có số nguồn và không bị coi là lỗi (bài 23).
- Lần chạy lại hẹp: lời gọi model của cả hai lần đều vào sổ tiền; sổ số đo ghi tên lần chạy lại kèm đầu lời lỗi của lần đầu, không ghi chữ.
- Trên màn hình: khung "Nguồn đã dùng (n bài)" có một nút cho mỗi bài đã được trích; bấm một nút là đọc được mảnh chữ gốc trong bài, kèm đường "Đọc cả bài". Lượt bị rút được ghi trong sổ là "bị rút lại".
- Bốn câu cố định khác được tính là từ chối khi đo: câu cho câu hỏi ngoài phạm vi (bài 22) và ba câu "chưa làm thay được" (đặt chỗ, gửi tin, xem tình trạng phòng; bài 4).
- Lần chạy lại trong cuộc đã lập lịch (từ 16:08 22/11): lần hai đi thẳng đường trả lời thường, không gọi lại bước hiểu ý sửa lịch (lần đầu đã kết luận đây không phải câu sửa; gọi lại là có thể áp một lệnh sửa lần hai). Lần chạy lại này mới có ca test, chưa có lượt thật.
- Quyết định 5, bản "đã tìm hết lượt": lọt một tin hỏi phòng gym (model tìm 2 lần rồi tự dừng). Chữ không số nguồn ở ca viết lại thường là chữ giữ chỗ, hoặc dòng "chưa có" kèm lời không nguồn.
- Bước viết lại, trước khi có (trước 14:47 22/11): lời báo "Câu trả lời không đáp ứng yêu cầu trích dẫn." ở 5 trên 6 lần của một tin 4 ý. Từ 14:47 tới 15:42 22/11 (trước khi giữ chữ), một đoạn chữ ngắn chưa phải câu trả lời hiện khoảng 15–17 giây rồi bị thay.
- Bản viết lại mà hỏng ở phép kiểm khác (ghi số nguồn không có): từ 22:06 22/11 không được gửi ra, người dùng chỉ thấy "Câu trả lời không đáp ứng yêu cầu trích dẫn." và nút "Thử lại"; trước đó chữ của nó được gửi tới trình duyệt rồi mới bị rút. Chưa lượt thật nào gặp (bài 6, "Chi tiết để tra").
- Câu nhờ làm thay (đặt phòng, mua vé…) mà model nộp chữ không nguồn: lần viết lại ra câu từ chối, chương trình đổi thành câu "chưa làm thay được" (bài 4). Trước 09:31 23/11 câu này hiện hai lần liền nhau; nay một lần. Chỗ lặp do hai bản soát của model khác hãng ngày 22/11 nêu, sinh ra từ bản vá 22:06 22/11. Lượt thật từng đi qua đường này: 0; bằng chứng là ca test (đỏ trước, đạt sau; cả khi giữ chữ lẫn khi hiện chữ dần).
- Đã nhìn trên trình duyệt 22/11, giao diện cũ: ở tin dài, lúc chờ chỉ có một dòng trạng thái, rồi cả câu trả lời hiện một lần (tin bốn ý: 29,5 giây). Lần chạy lại hẹp (quyết định 4) đã thật sự xảy ra ở 2 trong 5 lượt đo lại, cả hai ra câu trả lời. Ca viết lại (quyết định 5) theo test và một lượt thật. Câu con số lạ ở lượt có lịch thì vẫn rút cả câu (bài 24).
- Một điều hay nhầm: chữ không phải lúc nào cũng hiện trước rồi mới kiểm. Chỉ với model trả chữ dần; với model đang chạy, ở ô chat, chữ được giữ tới khi qua kiểm (từ 15:42 22/11).
- Câu hỏi việc ở tỉnh, thành khác: câu có chữ "Huế" ("Từ Huế vào Hội An…") thường được bước xếp loại (model theo lời dặn) cho đi đường "về Huế" (câu đối chứng: 113 trên 120 lần ở sáu ô đo 23/11), nên nhóm đặt chỗ chặn ở lời dặn trả lời; chặn ở bước xếp loại là đường lùi đã ghi, chưa thử. Máy chủ đọc cấu hình một lần lúc khởi động, nên một máy chủ đang chạy từ trước 13:28 chưa có đoạn dặn tới khi khởi động lại. Lượt bị từ chối vẫn mở mục tra web như mọi câu từ chối. Bản trả lời lọt mà bộ nhớ câu trả lời đã giữ trước khi mở thì mất khi máy chủ khởi động lại để đọc công tắc; dấu phiên bản của bộ nhớ cũng đổi vì lời dặn đổi.
- Bước viết lại: sổ số đo ghi một mục riêng (tên, thời gian, có ra câu từ chối không), không ghi chữ; ở tin nhiều ý, lần viết lại nhận thêm một dòng dặn "ý nào Bằng chứng có thì trả lời kèm mã nguồn; ý nào không có thì ghi một dòng" để không từ chối cả câu. Lần viết lại có hạn 45 giây riêng.

**Bài sau (bài 17):** hết chặng 3. Đường hỏi đáp đã đủ: tìm, viết, kiểm. Chặng 4 trả lời câu hỏi "lấy gì bảo đảm nó tốt": bộ câu hỏi mẫu và cách chấm.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Ba luật, nhận cả `[n]` và `[Nguồn n]`: `backend/llm/citations.py` (`CITATION_PATTERN`, `normalize_citations`, `select_cited_sources`) [code, đọc 22/11/2026].
- Giao diện bỏ số [n] khỏi chữ và hiện khung "Nguồn đã dùng (n bài)" (từ 10:00 23/11; bản cũ là dòng "Nguồn:"): `frontend/src/markdown.js` (hàm `boMaTrichDan`), `frontend/src/SourceLine.jsx` (nhãn `nguon-nhan`, đường "Đọc cả bài") [code, đọc 23/11]; lựa chọn của chủ dự án: `bai_hoc/17_GIAO_DIEN_VA_TOC_DO.md` mục "Hai lựa chọn đáng nhớ".
- Rút lại ở đường chat (sự kiện báo lỗi kèm cờ "sau khi đã hiện chữ", kết cục "retracted"): `backend/api/routes/chat.py`, hàm `finish` của đường stream [code].
- Gỡ câu từ chối nối ở cuối (21/11, 1 / 3 lượt): `backend/llm/assistant.py`, hàm `bo_cau_tu_choi_cuoi` và chú thích của nó [code].
- Từ chối không gọi model khi không có đoạn nào: `assistant.py`, hàm `prepare_answer` [code].
- Câu từ chối, câu ngoài phạm vi, danh sách câu được tính là từ chối, dòng "có thể đã thay đổi": `backend/llm/full_corpus_prompt.py` (`INSUFFICIENT_ANSWER`, `OUT_OF_SCOPE_ANSWER`, `CAU_LAM_THAY`, `REFUSAL_ANSWERS`, `MAY_HAVE_CHANGED_NOTICE`); nhóm bài có dòng đó: `assistant.py`, `NOTICE_SOURCE_PREFIXES` [code].
- Câu dẫn sang mục web do giao diện thay, máy chủ giữ câu từ chối: `frontend/src/moDauWeb.js` (chú thích đầu file) [code].
- Ví dụ chính (số nguồn 1, 2, 4, 5, 6): `data/hoc_cung_D/vi_du_di_suot_vet.json`; ví dụ chỗ đậu ô tô: `data/hoc_cung_D/vi_du_kho_khong_co_2_vet.json` [đã chạy].
- 24 / 465; 69 ⇒ 14 trên 1.600 câu; 0 câu đúng bị đổi; 0 / 489: `bai_hoc/08_GENERATION.md` (mục "Một chuyện thật" và mục Nguồn) [đã chạy, gpt-6-luna].
- 0 lỗi trích dẫn / 93 lượt với Claude: `data/thu_bedrock_2026-11-21/c_harness/RA_HARNESS.md` dòng 17 [riêng tư, 21/11].
- Câu bị rút 3 / 48 và 4 / 53 (người dùng mô phỏng, một phiên đọc tay, chưa có người thứ hai): `bai_hoc/VIEC_MOI_XONG.md` mục 23, bảng "Người dùng gặp gì".
- Trả lời một phần (13 ⇒ 1; 2 câu ngoài kho): `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 11.
- Điều kiện "0 câu ngoài kho được trả lời bằng kho": `session_prompt/HIEN_TRANG.md` mục 4, phần "Sản phẩm".
- Mục "Quyết định và lý do", "Nếu… thì sao", "Câu hỏi tự kiểm", "Quyết định nhỏ hơn", phần "Đã so" về màn hình "Thử lại" (thêm 14:05 22/11/2026 theo khuôn mới). Lời báo rút lại nguyên văn: `backend/api/routes/chat.py` `_loi_trich_dan` [code]. Lần chạy lại hẹp (điều kiện, không kèm câu trả lời cũ, không chạy lại câu cố định / lượt sửa lịch — cuộc có lịch đã lưu được chạy lại cho câu hỏi thường từ 16:08 22/11, lần hai đi `_answer_core` (`backend/config/settings.yaml` dòng 76 `nho_dap_cuoc_co_lich`; `assistant.py` dòng 2114–2131) [code], 3 / 7 trước khi có, chờ thêm khoảng 5 giây, đường "giữ chữ tới khi kiểm xong" không chọn): `backend/llm/assistant.py` `answer_turn_stream_parallel` và `TEN_CHAY_LAI`; `report_agent/2026-11-22/b_nho_dap_chay_lai.md` mục 1–3 [code + đã chạy, phiên khác]. Dòng "danh sách có thể chưa đủ" (khuôn chữ, lý do, 6 / 18, 5 / 6, câu một gợi ý không nhận): `backend/llm/danh_sach.py` (chú thích đầu file, `CAU_DANH_SACH`), điều kiện nối: `backend/llm/assistant.py` khoảng dòng 1162–1166; mở 16:15 20/11/2026: commit `051e954f`; dòng `danh_sach_noi_that: true` trong `backend/config/settings.yaml` (chú thích cạnh dòng còn ghi "TẮT tới khi…", lệch với giá trị) [code]. Ba câu "chưa làm thay được": `CAU_LAM_THAY` trong `backend/llm/full_corpus_prompt.py`. Bản chữa "viết lại một lần" (3 / 6 ⇒ 0 / 6, 0 / 5 con số bịa, 4 / 5 câu thiếu hai ý, 44 câu, 3,77 USD, thứ tự lỗi chủ dự án đã chốt): `bai_hoc/VIEC_MOI_XONG.md` mục 40, gạch "Đo rồi KHÔNG mở" [người thứ hai kiểm]. Sàn câu từ chối: `session_prompt/HIEN_TRANG.md` mục 4, gạch 11:24 21/11/2026. Luật "không trả một phần, không tự sửa, không tự gọi lại" và lỗi `citation_integrity_error`: `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md` mục 9, dòng 251–273 [chép]. Lần chạy lại: chỉ đường stream (`backend/api/routes/chat.py` khoảng dòng 204–216; đường không stream gọi `answer_turn`), điều kiện `trace.citation_error` bất kỳ (`assistant.py` khoảng dòng 1998), số sau sửa 0 / 5 và 2 / 5 lượt chạy lại thật: `report_agent/2026-11-22/b_nho_dap_chay_lai.md` mục 4 [người thứ hai kiểm]. Bản chữa "viết lại một lần": lúc 14:33 22/11 còn ở nhánh riêng; nay đã gộp và mở — `settings.yaml` của main có `het_luot_viet_lai: true` (MỞ 14:33 trong chú thích; runbook mục 0 đếm 45 lúc 14:47) [code, đọc 15:08 22/11/2026]. Cập nhật theo bộ thay đổi mở 14:47 22/11/2026: `bai_hoc/VIEC_MOI_XONG.md` mục 42, 43; `guides/RUNBOOK_BAN_GIAO.md` mục 10.1; `backend/config/settings.yaml` [code; số đo: đã chạy, phiên đo; người viết không chạy lại]. Điều kiện và hạn giờ: `backend/llm/assistant.py` `_viet_lai_het_luot`, `TEN_VIET_LAI`; dòng dặn tin nhiều ý `VIET_LAI_NHIEU_Y_TEXT` (`backend/llm/full_corpus_prompt.py`); 9 lần kích hoạt thật đều "đã hết lượt": runbook 10.1 hàng "Lưới viết lại một lần" [code + chép]. Dòng chồng nhau với công cụ mục lục: `assistant.py` khoảng dòng 1162–1166 không loại nguồn mục lục [code, chưa thử]. Bốn nhóm bài của dòng "có thể đã thay đổi": `assistant.py` `NOTICE_SOURCE_PREFIXES`; lý do ba nhóm đầu: đặc tả Phase 9 bản 5 (`git show 077e3cb:docs/superpowers/specs/2026-11-02-phase-9-design.md` bảng quyết định Q2 và mục 5.3); bài lưu trú: chú thích cạnh `NOTICE_SOURCE_PREFIXES` [code + chép]. Số 3 / 48 và 4 / 53 đo trước commit `5936d165` (13:51 21/11): `VIEC_MOI_XONG.md` mục 23 ghi lúc 13:48 21/11. Các mục mới đã qua một lượt đối chiếu độc lập 14:28 22/11/2026 và được sửa theo: `data/hoc_cung_D/kiem/muc_moi_12_16.md` [riêng tư].

- Đã qua một lượt kiểm chéo sau lượt cập nhật 14:47 (`data/hoc_cung_D/kiem/cap_nhat_14h47.md`) [riêng tư]. Theo đó: bảng Nếu dòng 1 và dòng viết lại không còn trái nhau (thiếu số nguồn: viết lại khi model đã tự tìm ≥ 1 lần, rút lại khi chưa tìm lần nào — `_viet_lai_het_luot` điều kiện `model_searches >= 1`); thêm thứ người dùng thấy khi viết lại (`bai_hoc/VIEC_MOI_XONG.md` mục 42, đính chính 15:14; runbook 10.1 hàng "Lưới viết lại"; suy từ chương trình và sổ máy chủ, chưa chụp màn hình); đáp án câu tự kiểm 3 sửa ("6 trên 6" là tin đó qua 6 lần hỏi ở lượt nối, không phải câu viết lại — mục 42 ý 2); câu dẫn bảng bốn cột sửa thứ tự (điều kiện đổi SAU lượt nối). Cắt nửa để hiểu: quyết định 5 cũ (dòng "danh sách có thể chưa đủ") và câu hỏi tự kiểm 3 cũ chuyển xuống "Quyết định nhỏ hơn"; quyết định 6 cũ thành quyết định 5.

- Giữ chữ tới khi qua bước kiểm nguồn (mở 15:42 22/11/2026, chỉ lượt có công cụ trên model trả chữ một lần): `backend/config/settings.yaml` dòng `giu_chu_toi_kiem`, `backend/llm/assistant.py`, `backend/tests/test_giu_chu_toi_kiem.py` [code, đọc 22/11]; `guides/RUNBOOK_BAN_GIAO.md` 10.1 hàng "Lưới viết lại" [chép]. Phạm vi "lượt hỏi đáp về Huế trong ô chat": `assistant.py` dòng 352–354 (`uses_tools` = `tim_them`), 1979–1988 [code].

- Bản viết lại hỏng kiểm không còn được gửi (đợt 22:21 22/11/2026): commit `70ba72d5` (gộp `dc43cc93` 22:06); `backend/llm/assistant.py` dòng 2110–2116 (phát bản viết lại chỉ khi `trace.citation_error is None`); ca test `backend/tests/test_phat_ban_da_kiem.py::test_rewrite_that_fails_the_citation_check_is_not_sent` [code; không chạy]; 0 / 537 lượt có lỗi kiểm loại này: `data/thu_bedrock_2026-11-21/harness/dem_gpt_harness_2211/KET_QUA.md` hàng A2 [riêng tư, đã mở; đã chạy, phiên khác]. Phần đủ ở bài 6, khối Nguồn.
- Đã nhìn trên trình duyệt 16:17–16:21 22/11/2026 (16 / 16 lượt thành công, 0 màn hình lỗi; lượt thường của tin dài: một dòng trạng thái rồi cả câu một lần, máy đọc màn hình mỗi 0,25 giây không thấy chữ nào trước; tin gia đình bốn ý 29,5 giây; ca viết lại chưa trúng; dòng trạng thái đứng yên 20–30 giây, ý "đổi dòng theo từng lần tìm" chưa làm): `bai_hoc/VIEC_MOI_XONG.md` mục 44 (dòng 19–45); `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 hàng "Lưới viết lại"; `data/test_cuoi/chay_2026-11-22_e_nhin_gom/KET_QUA.md` [riêng tư; đã chạy, phiên đo; người viết chép, chưa mở file riêng tư đó] — lượt nhìn này là trên giao diện CŨ. Lời trạng thái nguyên văn: `frontend/src/chat.jsx` `STATUS_TEXT` [code].
- Đợt 23/11/2026. Thẻ chờ (khúc sông, con đò, dòng bước lấy từ `STATUS_TEXT` theo sự kiện `status` cuối, "Đã tìm thấy N bài — bấm tên để đọc trong lúc chờ", nhiều nhất 6 tên rồi "+k bài"; ở khung trợ lý nổi, màn ≤ 760 px và khung nhìn cao ≤ 700 px — gồm máy demo 1536 × 695 — chỉ hiện 3 tên, `frontend/src/song/song.css` dòng 73–88): `frontend/src/song/Song.jsx` `ChoSong`, `frontend/src/chat.jsx` (khối `pending && !turn.text`, `daTim` từ trường `bai` của sự kiện `searched`); máy chủ gửi tên bài: commit `a76eb962` (`bai_da_tim` ở `backend/llm/assistant.py`); ở lượt có công cụ với model trả cả câu một lần, sự kiện "đang viết" chỉ phát khi chữ đầu tới (`pending_generating`, `assistant.py` khối `start_tools_stream`) ⇒ lúc model viết câu cuối dòng bước không đổi [code]. Tin dài trên giao diện mới: ảnh `C01_cho_*_1440_man.png` của cổng gộp, `data/giao_dien_2026-11-22/sau_gop_10c30bc5/MUC_LUC.md` hàng `C01_cho_tin_dai` (2–20 giây, 3 ⇒ 6 tên bài) [riêng tư, đã mở ảnh — biên bản kiểm 23/11]; chưa có số đo thời gian. Câu nói thật gửi hai lần: commit `2ba8d394` (gộp `97d4e85d` 09:31 23/11), `backend/llm/assistant.py` `answer_turn_stream` (biến `da_phat_viet_lai`), ca test `backend/tests/test_phat_ban_da_kiem.py::test_rewrite_that_ends_in_the_done_for_you_sentence_is_sent_once`; 0 / 1.967 lượt có trả tiền trong sổ máy chủ và 0 / 1.254 dòng sổ vết có cả dấu viết lại lẫn dấu làm thay; hai bản soát Gemini 4 Neon, Gemini 4 Carbon; chỗ gửi đôi để lại từ `70ba72d5`: lời commit [code; chép lời commit; không chạy test]. Câu nói thật: `CAU_LAM_THAY` (`backend/llm/full_corpus_prompt.py`) [code].

- Đợt đầu chiều 23/11/2026 — tính năng thứ 50 (câu hỏi việc ở tỉnh, thành khác), viết 13:41–13:51 23/11/2026 (giờ `date`). Cơ chế: `backend/llm/full_corpus_prompt.py` hằng `SONNET_NOI_KHAC` và chú thích (5) đứng trước nó; `backend/llm/generator_openai_full_corpus.py` hàm `kem` (chỉ nối khi `bedrock_model` có), `them_noi_khac`, `tra_loi` dùng cho `answer_agent`, `assistant_instructions` (⇒ bản lịch sử) và `ny` (bản nhiều ý), `bieu_mau_agent` / `router_agent` / `chat_agent` / `lich_v2_agent` / `sua_lich_*` không nhận; đọc công tắc trong `from_environment` (chỉ nhánh `provider: bedrock`, lúc dựng generator ⇒ đổi phải khởi động lại); dòng `noi_khac_tu_choi: true` trong `backend/config/settings.yaml` (chú thích ghi "MỞ 13:11 23/11/2026"; commit mở `1b78e2eb` 13:28, gộp `1a28e3c7`; code `5f620c8f`, test `3c1f1978`) [code, đọc 13:36–13:41 23/11]. Câu từ chối cố định do model viết, chương trình so chữ: `INSUFFICIENT_ANSWER`; luật nhiều ý: `ANSWER_SYSTEM_INSTRUCTIONS_NHIEU_Y` [code]. Độ dài 1.233 ⇒ 2.311 ký tự: `len()` của các hằng (664 + 2 + 567; 664 + 2 + 1.076 + 2 + 567) [tự đếm, `uv run --no-sync python`] và dòng "dài 1233 / 2311" trong các file `.log` của `do_e/` [riêng tư, đã mở]. Lượt bị từ chối mở mục web: công tắc `web_chi_khi_tu_choi` (bài 25) [code]. Bước xếp loại cho câu có chữ "Huế" đi đường về Huế: `SONNET_DINH_TUYEN` ("câu không dính gì tới Huế") [code].
- Số của đợt này, ĐẾM LẠI từ file `.jsonl` thô ở `data/thu_bedrock_2026-11-21/harness/b_noi_khac_2311/do_e/` [riêng tư; tự đếm bằng `python3 -I` 13:36–13:41 23/11; "được trả lời bằng kho" = `tu_choi` false và `nguon_trich` khác rỗng, đúng định nghĩa ở `TIEU_CHI.md`]: mốc cùng buổi `5f620c8f_tat_a_r06` 12 / 20 (20 / 20 tuyến `tro_ly_hue`); mở `5f620c8f_bat_a_r06` 0 / 20 (19 câu từ chối, 1 `ngoai_pham_vi`; `goi_model` rỗng 20 / 20; trung vị 4,985 so với 10,29 giây, 2 so với 4 lời gọi); ô giả thuyết đầu `o_n_x20` 11 / 20; ô tắt hết `o_k_x20` 1 / 20 (ghi đè 14 mục trong `o_k_x20.log`: hai trần + 12 công tắc); ô chỉ trả hai trần `o_k1_x20` 8 / 20; ô chỉ tắt liệt kê `o_k2_chi_tat_liet_ke_x20` 1 / 20; 0 / 12 lượt hở của ô mốc có `liet_ke_bai` trong `cong_cu`; Hà Nội `*_b_ngoai_tinh` B1 0 / 10 cả hai bên (4 / 10 chặn ở xếp loại mỗi bên); Đà Nẵng B2 tắt 10 / 10 ⇒ mở 0 / 10; nhóm c 15 / 15 có nguồn cả hai bên, câu ghép bên tắt có "cơm gà" 5 / 5; nhóm e 9 / 9 cả hai bên; nhóm d giống nhau hai bên. Ô độ rộng `o_w_do_rong_x6`: 18 dòng (log không có dòng "xong" — lượt chưa chạy đủ 30 như ghi trước), W1 / W2 / W5 từ chối 4 + 4 + 3, W3 2 / 4, W4 3 / 3 có nguồn [tự đếm]; cách hiểu "trả lời từ thứ kho có thật" [đã đọc chữ thô 5 lượt; khớp `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 hàng "Câu hỏi về việc diễn ra ở TỈNH, THÀNH KHÁC"]. Chữ câu trả lời trích ở thân bài: dòng 1 của `5f620c8f_tat_a_r06.jsonl` (lần 0), chỉ lấy câu thứ hai [tự đọc]; dòng kho: `scripts/grep_kb.sh 'Cơm gà Hội An'` ⇒ bài `com tam okla` dòng 17, mục "Món ăn / trải nghiệm" [đã chạy]. Dòng "Tư liệu chưa có…" của câu ghép: `5f620c8f_bat_c_doi_chung.jsonl`, C3 lần 0 [tự đọc].
- Phần đọc tay (Đà Nẵng dựa vào dòng lạc ở bài "Vé tham quan Hải Vân Quan" và "Đèo Hải Vân"; câu ghép bên tắt kể món lạc; nhóm e "ngang nhau"; nhóm d "không đổi"; 100 lượt, một agent con độc lập): `do_e/CHAM_NHOM_B_C_E_D.md` [riêng tư; chép, đã mở]. Tiêu chí ghi trước, ngưỡng ô giả thuyết đầu (≤ 1 / 2–3 / ≥ 4), "bài mới đứng hạng 2, 4, 5, 10" (máy kiểm của phiên viết code, chỉ khâu tìm), "dưới khoảng 14 %", "10 lần chỉ bắt ≥ 25 %", đường lùi "chặn ở định tuyến": `b_noi_khac_2311/TIEU_CHI.md` [riêng tư; chép, đã mở trọn]. "Dưới khoảng 14 %" người viết tính lại: 1 − 0,05^(1/20) = 0,139 [tự tính]. Mốc 21/11 (bản đầu ghi 0 / 30 — thiếu hai file cùng điều kiện; nay 1 / 40, xem gạch "Lượt áp biên bản" dưới), trưa 23/11 3 / 10 (`san_b4931a6b_s_high_x10`), đường model cũ 21/11 2 / 10 (`san_30cd_luna_x10`) và 3 / 5 (`s2_luna_tat_x5`, file cũ không có trường `nguon_trich` — đếm `tu_choi` false, câu có [n]): `data/thu_bedrock_2026-11-21/do/thuoc/r06_lap/` [riêng tư; tự đếm]. Công cụ liệt kê bài mở 09:20 22/11 (bài 21, khối Nguồn) ⇒ các lượt 21/11 không có công cụ đó (`cong_cu` không có `liet_ke_bai` ở mọi file) [tự đếm].
- Lượt trình duyệt trưa 23/11 trên bản CHƯA mở (ba cuộc mới, 11,6 · 5,7 · 0,008 giây, lần 3 giống lần 2 từng chữ): `data/playwright_mcp/luot_2311_trua/NHAT_KY.md` hàng C và mục "Bước C" [riêng tư; đã chạy, phiên khác; chép, đã mở]. "Một lượt qua đường gửi dần của máy chủ với công tắc mở": `do_e/luot_stream_8014_cong_tac_mo_server.log` (máy chủ tạm cổng 8014 khởi động 13:12:56, tắt 13:15:01; 7 dòng `chat_metrics` 13:13:32–13:14:47: `refusal` true + `has_web_section` true + `web_outcome` "co_muc" ở 3 dòng, `refusal` false với `n_cited_sources` 10, 2, 8, 8 ở 4 dòng; mọi dòng `route` "tro_ly_hue"; ba dòng từ chối cùng `input_tokens` 5.463) [riêng tư; tự đếm, đã mở]; chữ câu trả lời: báo cáo của phiên điều phối [chép, không có file]. Runbook 10.1 ghi "13:13–13:16"; log cho 13:13:32–13:14:47 (máy chủ tắt 13:15:01). Lượt trình duyệt với bản ĐÃ mở: chưa thấy (soát `ls -t data/playwright_mcp/` 13:36 23/11: hai lượt mới hơn `luot_2311_toi_nhe`, `luot_2311_them_day` không có câu về tỉnh khác). Việc chữa ở gốc chưa làm: `session_prompt/Y_CHUA_THU.md` hàng "| 71 |" [chép]. Giữ công cụ vì nó chữa câu "những quán nào có…": `Y_CHUA_THU.md` hàng 71, runbook 10.1 cùng hàng [chép]. Giới hạn: runbook 10.1 hàng trên; `session_prompt/HIEN_TRANG.md` mục 1 gạch 13:30 23/11 [chép]. Bản lọt trong bộ nhớ câu trả lời mất khi khởi động lại / dấu phiên bản đổi: `backend/api/cache_tra_loi.py` (chú thích đầu file), `backend/api/app.py` khối 3b (`dau_phien_ban(record, generator.assistant_instructions, …)`) [code].
- Để giữ nửa để hiểu ≤ 13.944 ký tự (trước 13.644): chuyển xuống "Chi tiết để tra" câu lượt trình duyệt 22/11 (29,5 giây), câu lần chạy lại thật 2 / 5, câu "lượt có lịch vẫn rút cả câu", gạch "Dễ nhầm" về hiện chữ trước; chuyển câu hỏi tự kiểm 3 cũ (bước viết lại) xuống "Quyết định nhỏ hơn"; gộp câu hỏi tự kiểm 2 cũ ("[4] có thật") vào câu hỏi 2 mới; bỏ câu thừa "ngoài câu này còn bốn câu cố định khác" (đã có ở bảng cấu hình và "Chi tiết để tra"); rút gọn chữ (không bỏ ý) ở Ý chính gạch 2 và 5, quyết định 4 và 5, bảng "Nếu" dòng viết lại.

- Lượt áp biên bản 23/11/2026 (`data/hoc_cung_D/kiem/dot_2311_chieu_k1_kiem.md` hàng 16.3, 16.10, 16.17, 16.21, 16.24, 16.26, 16.28, 16.33, 16.34, 16.40) [riêng tư]. Mốc 21/11 người viết tự đếm lại MỌI file câu đối chứng ở `data/thu_bedrock_2026-11-21/do/thuoc/r06_lap/` [riêng tư; tự đếm, "được trả lời bằng kho" = `tu_choi` false và có nguồn — file 21:35 không có `nguon_trich` nên đếm chữ có `[n]`]: cùng điều kiện (Claude mức cao, công tắc như bản chạy lúc đó) — `high_tat_x5` 15:49 (cây mốc `30cd9be0`, `meta.txt`) 0 / 5; `s2_high_tat_x5` 21:35 (cây `3098e169` công tắc mới tắt, bộ nhớ đệm tắt, `do/o_sua2_1.sh`) 1 / 5; `san_30cd_s_high_x10`, `san_cf1a_s_high_x10`, `san_main_s_high_x10` 21:45–21:48 0 / 30 ⇒ 1 / 40. Biến thể khác điều kiện: `high_bat_x5` 4 / 5, `high_bat2_x5` 2 / 5 (cây `d1e8ac93` + `bao_het_luot_tim=true`, bản chưa gộp — không có trong `settings.yaml` hiện tại), `s2_high_c_x5` 0 / 5 (`vong_cuoi_chi_viet` bật). 0 file có `liet_ke_bai` trong `cong_cu`. Phiên đo ghi cùng mốc: `do/san_ngoai_tinh_2311/KET_QUA.md` mục 1 ("0 / 30 + 1 / 5") [chép, đã mở]. Bước xếp loại: trường `route` = `tro_ly_hue` ở `5f620c8f_tat_a_r06` 20, `bat_a` 19, `o_n_x20` 20, `o_k_x20` 20, `o_k1_x20` 18, `o_k2_chi_tat_liet_ke_x20` 16 ⇒ 113 / 120 [tự đếm]; đó là model theo lời dặn `SONNET_DINH_TUYEN` [code]. Ngưỡng ghi trước: ô giả thuyết đầu (`TIEU_CHI.md` bổ sung 1), ô tắt cả nhóm (`session_prompt/VIEC_DANG_MO.md` dòng 19, ghi 12:29, ô chạy 12:29:51), ô chỉ trả hai giới hạn (`TIEU_CHI.md`, ghi trước K1); ô chỉ tắt công cụ (13:01): không thấy ngưỡng ghi trước [đã mở]. 14 thứ của ô tắt cả nhóm: dòng đầu `o_k_x20.log` [đã mở]. Máy chủ đọc cấu hình một lần: `backend/api/app.py` `lifespan` gọi `load_settings` (dòng 93–96) rồi dựng generator [code]. Hướng chặn ở dữ liệu (dòng thực đơn mang tên tỉnh khác): `do/san_ngoai_tinh_2311/KET_QUA.md` mục 2 "Hướng rộng hơn" [chép]. Lý do chọn lời dặn trước: `TIEU_CHI.md` "Kết luận ghi trước" [chép]. Ý chính gạch 5 cũ (lỗi số nguồn hiếm) bỏ khỏi Ý chính vì đã có nguyên ở "Chi tiết để tra" gạch đầu; câu "con số lạ bị gỡ, không rút cả câu" rút ở mục "Điều bước kiểm…" vì đã có ở bảng "Nếu" dòng cuối. Nửa để hiểu 13.936 ⇒ 13.922.

</details>
