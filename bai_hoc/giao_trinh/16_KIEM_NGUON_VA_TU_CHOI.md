# Bài 16 — Kiểm nguồn bằng chương trình, và câu từ chối cố định

*Cập nhật 15:40, ngày 22/11/2026 · luật kiểm đọc từ chương trình đang chạy sau 14:47 22/11 (bước viết lại một lần đã mở); số đếm lấy từ các báo cáo từ 25/10 tới 22/11, ghi rõ model ở từng số; người viết không chạy lại phép đo nào.*

**Bài trước đã biết:** model viết nhận lời dặn, câu hỏi, 10 đoạn, và trả về một ô chữ có các số nguồn [n].
**Bài này thêm:** chương trình làm gì với ô chữ đó trước khi coi lượt hỏi là xong. Hai việc: kiểm số nguồn, và nhận ra câu từ chối.

## Ý chính

- Chương trình kiểm số nguồn theo **ba luật**: câu trả lời phải có ít nhất một số nguồn; mọi số phải là số của một nguồn đã thật sự được đưa cho model (một đoạn của kho, hoặc một nguồn do chương trình dựng như khối dự báo thời tiết); câu từ chối thì không được kèm số nguồn.
- Phạm luật thì câu trả lời **bị rút lại**: người dùng thấy "Câu trả lời không đáp ứng yêu cầu trích dẫn." và nút "Thử lại", không thấy câu trả lời có nguồn giả. Riêng lượt hỏi tiếp đang kèm câu trả lời liền trước, ô chat tự chạy lại cả lượt một lần trước khi báo; và từ 14:47 ngày 22/11, chữ không có số nguồn nào mà model đã tự tìm thì được viết lại một lần (bài 21).
- Câu từ chối là **một câu cố định, đúng từng chữ**. Nhờ vậy chương trình nhận ra chắc chắn một lượt là từ chối, để mở đường tra web và để đếm khi đo.
- Bước kiểm này mới kiểm **số nguồn có thật**. Nó chưa kiểm đoạn được trích có nói đúng điều câu trả lời viết không.
- Lỗi số nguồn hiếm: 0 trên 489 lần viết của gpt-6-luna ở một lần đếm cuối tháng 10; 0 trên 93 lượt ở một lượt rà ngày 21/11 trên cả hai model.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| kiểm số nguồn | **citation check**, **citation integrity** | kiểm mọi số [n] trong câu trả lời trỏ tới một đoạn có thật |
| rút lại | **retract** | xoá câu trả lời đã hiện và thay bằng lời báo lỗi |
| câu từ chối cố định | **fixed refusal**, **fallback answer** | một câu duy nhất, đúng từng chữ, dùng mỗi khi không đủ bằng chứng |
| điều kiện không được vỡ | — (trong hồ sơ dự án gọi là "sàn") | một điều ghi trước mà mọi thay đổi phải giữ; ở đây: 0 câu ngoài kho được trả lời bằng kho |

## Ba luật kiểm số nguồn

Sau khi model viết xong, chương trình đọc ô chữ và kiểm:

1. **Câu trả lời phải có ít nhất một số nguồn.** Một câu trả lời không có số nào thì không ai biết nó dựa vào đâu.
2. **Mọi số nguồn phải có thật.** Ở ví dụ chính, model được đưa các đoạn số 1 tới 10. Nếu câu trả lời ghi [12] thì đó là một nguồn bịa.
3. **Câu từ chối không được kèm số nguồn.** "Tôi không tìm thấy đủ thông tin… [3]" là một câu tự mâu thuẫn.

Câu trả lời thật của ví dụ chính ghi các số 1, 2, 4, 5, 6. Cả năm đều nằm trong 10 đoạn đã đưa, nên nó qua bước kiểm.

Trên màn hình, người dùng không thấy các số [n] trong chữ. Giao diện bỏ chúng đi và hiện một dòng "Nguồn:" dưới câu trả lời, ghi tên các bài đã được trích; bấm vào một tên là đọc được mảnh chữ gốc trong bài. Số nguồn vẫn có ở tầng chương trình, và bước kiểm chạy trên đó.

Chương trình chấp nhận hai cách ghi: [3] và [Nguồn 3]. Lý do ở mục "Đã so".

## Phạm luật thì câu trả lời bị rút lại

Trong ô chat, chữ hiện trước, kiểm sau; kiểm hỏng thì rút lại (bài 6, 21). Giao diện xoá chữ đã hiện, hiện lời báo "Câu trả lời không đáp ứng yêu cầu trích dẫn." và nút "Thử lại". Lượt đó được ghi trong sổ là "bị rút lại".

Lựa chọn ở đây là: thà người dùng phải bấm lại, còn hơn đọc một câu trả lời mang số nguồn không có thật.

Có hai trường hợp chương trình không báo lỗi ngay:

- **Câu từ chối nối ở cuối.** Đôi khi model viết phần trả lời có số nguồn rồi nối thêm nguyên câu từ chối ở cuối. Theo luật 3 thì cả câu hỏng. Chương trình gỡ câu từ chối ở cuối, giữ phần có nguồn, rồi kiểm phần đó như mọi câu.
- **Lượt hỏi tiếp đang kèm câu trả lời liền trước** (từ 22/11, chỉ ở ô chat): lượt bị rút ở bất kỳ phép kiểm nào sau khi viết thì được chạy lại cả lượt **một lần**, không kèm câu trả lời cũ (quyết định 4).

## Câu từ chối là một câu cố định, đúng từng chữ

Khi các đoạn được đưa không đủ để trả lời, model phải trả đúng câu này, không thêm bớt:

> Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này.

Để model tự viết lời từ chối thì mỗi lần một kiểu, dễ thành từ chối nửa vời rồi đoán. Một câu cố định cho ba thứ:

- Chương trình **nhận ra chắc chắn** lượt này là từ chối, bằng cách so chữ. Từ đó nó mở đường tra web (bài 25).
- Khi đo, **đếm được chính xác** bao nhiêu câu bị từ chối, bao nhiêu câu từ chối nhầm, bao nhiêu câu ngoài kho lọt qua (chặng 4).
- Người dùng gặp cùng một thông báo mỗi khi kho không đủ (riêng khi có mục web thì giao diện đổi nó thành câu dẫn sang mục web, như ví dụ ngay dưới).

Khi đo, ngoài câu này còn bốn câu cố định khác được tính là từ chối: câu cho câu hỏi ngoài phạm vi (bài 22) và ba câu "chưa làm thay được" (đặt chỗ, gửi tin, xem tình trạng phòng; bài 4).

Ở ví dụ "kho không có" (chỗ đậu ô tô ở chùa Thiên Mụ), model trả đúng câu này. Chương trình nhận ra, tra web một lần, và vì mục web có nội dung nên giao diện thay câu từ chối bằng câu dẫn "Tư liệu của mình chưa có thông tin này — dưới đây là thông tin từ web (chưa kiểm)."

## Điều bước kiểm này chưa làm được

Chương trình biết [4] trỏ tới một đoạn có thật. Nó chưa biết đoạn 4 có thật sự nói điều câu trả lời viết không. Ở ví dụ chính thì có: đoạn 4 ghi đúng giá vé trẻ em. Nhưng đó là do người đọc đối chiếu, không phải do chương trình kiểm.

Vì vậy "có số nguồn" chưa phải "đã kiểm đúng". Phần nghĩa chỉ được đo khi chấm câu trả lời (bài 19), và với hai loại con số dễ sai nhất (thời tiết, khoảng cách) thì có thêm một bước kiểm con số riêng: câu chứa con số lạ bị gỡ, không rút cả câu trả lời (lượt có lịch thì vẫn rút cả câu; bài 24).

Bước kiểm cũng không biết một danh sách có đủ hay không; câu xin danh sách có nguồn kho thì chương trình nối một dòng "có thể chưa đủ" (mục "Quyết định nhỏ hơn").

## Quyết định và lý do

### 1. Vì sao số nguồn sai thì rút cả câu trả lời, không chỉ gỡ số sai?

- **Đã chọn:** phạm một trong ba luật là rút cả câu, hiện lời báo và nút "Thử lại".
- **Vì sao:** luật ghi từ đặc tả lúc dựng hệ thống: số nguồn không khớp là lỗi của cả câu trả lời; không trả một phần, không tự sửa, không tự gọi lại. Lập luận đứng sau (không phải số đo): một số nguồn không có thật nghĩa là không biết ý đó dựa vào đâu. Ba chỗ về sau nới luật này, mỗi chỗ có quyết định riêng: gỡ câu từ chối nối ở cuối, lần chạy lại hẹp, và bước viết lại một lần (quyết định 5).
- **Cách khác:** chỉ gỡ số sai, hoặc gỡ câu chứa số sai: chưa thử. Cách nhẹ đó đang dùng cho con số thời tiết và khoảng cách (bài 24).
- **Cái giá:** câu trả lời đúng mà quên số nguồn cũng bị rút. Lỗi hiếm (0 trên 489 lần viết của gpt-6-luna cuối tháng 10; 0 trên 93 lượt ngày 21/11), nhưng vẫn có lượt bị rút (mục "Giới hạn đã biết").

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

- **Đã chọn:** lượt bị rút ở bước kiểm sau khi viết (số nguồn hay phép kiểm khác), mà lịch sử đang mang câu trả lời liền trước, thì ô chat gỡ chữ đã hiện và chạy lại một lần không kèm câu trả lời cũ. Lượt có câu cố định hoặc cuộc đã có lịch thì không.
- **Vì sao:** đo sáng 22/11 (Claude Sonnet 5.5): sau khi mở việc nhớ câu trả lời, tin kiểu "bỏ chợ Đông Ba đi" ra màn hình lỗi 3 trên 7 lần, vì model chép lại lời cũ không ghi số nguồn. Đo lại sau bản sửa: 0 trên 5 lần ra màn hình lỗi; lần chạy lại thật sự xảy ra ở 2 lượt, cả hai ra câu trả lời (người thứ hai kiểm).
- **Cách khác:** giữ chữ tới khi kiểm xong rồi mới hiện: không chọn, vì đổi cách hiện chữ của mọi lượt. Chạy lại ở mọi lượt bị rút: không làm.
- **Cái giá:** chờ thêm vài giây và tiền tính cả hai lần gọi model ở các lượt đó; lần hai cũng hỏng thì người dùng vẫn thấy lời báo lỗi.

### 5. Vì sao bước viết lại một lần bị bỏ trưa 22/11 mà 14:47 cùng ngày lại mở?

- **Đã chọn:** mở bước viết lại với điều kiện "model đã tự tìm ít nhất một lần mà chữ nộp không có số nguồn nào", CÙNG hai thay đổi ở khâu tìm (bài 23) và trần tìm 3 (bài 21). Lần viết lại không có công cụ, chữ mới kiểm như thường; vẫn không có số nguồn thì câu từ chối cố định.
- **Vì sao:** đã đo (Claude Sonnet 5.5, tin của gia đình, 6 lần mỗi bên). Đứng riêng, nó đổi màn hình lỗi lấy câu trả lời thiếu hai ý kho có (mục "Đã so"). Khi khâu tìm đã đưa được đoạn đúng vào bằng chứng và có lần tìm thứ ba, cả bộ cho 0 trên 6 màn hình lỗi và 6 trên 6 lần đủ cả hai ý.
- **Cách khác:** bản đứng riêng với điều kiện "đã tìm HẾT lượt": đã đo, không mở; điều kiện đó còn lọt một tin hỏi phòng gym (model tìm 2 lần rồi tự dừng). Nới bước kiểm để chữ không nguồn tới người dùng: không làm.
- **Cái giá:** lượt có viết lại lâu hơn khoảng 10 giây, thêm một lần gọi model; trong ô chat, chữ giữ chỗ của bản đầu hiện khoảng 15–17 giây trước khi bị thay (suy từ chương trình và sổ máy chủ, chưa chụp màn hình). Các chỗ chưa đo: mục "Đã so", giới hạn.

## Nếu… thì sao

Đọc từ chương trình, trừ dòng ghi **(đã thử)** hay "đã đo". Lời báo trong ngoặc kép là nguyên văn.

| Nếu | Hệ thống làm gì | Người dùng thấy gì | Đã có chưa / ai làm gì |
|---|---|---|---|
| câu trả lời ghi số nguồn không có, hoặc thiếu hẳn số nguồn mà model chưa tự tìm lần nào | rút lại chữ đã hiện | "Câu trả lời không đáp ứng yêu cầu trích dẫn." và nút "Thử lại" | người dùng bấm "Thử lại" |
| ca trên, ở lượt đang kèm câu trả lời liền trước **(đã thử)** | ô chat gỡ chữ, chạy lại cả lượt một lần | chờ lâu hơn, rồi câu trả lời hoặc lời báo như dòng trên | có từ 22/11; đo lại: 0 trên 5 lần ra màn hình lỗi |
| model đã tự tìm ít nhất một lần (ví dụ tin dài nhiều ý, hết lượt tìm) rồi nộp chữ không có số nguồn nào (chữ giữ chỗ, hoặc dòng "chưa có" kèm lời không nguồn) | viết lại một lần, không công cụ, từ các đoạn đã gom; vẫn không có ⇒ câu từ chối cố định | một đoạn chữ ngắn chưa phải câu trả lời hiện khoảng 15–17 giây rồi bị thay bằng câu trả lời có nguồn (cả lượt lâu hơn khoảng 10 giây); hoặc "Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này." | đã đo trên một tin; có từ 14:47 22/11; trước đó: lời báo như dòng đầu, 5 trên 6 lần ở một tin 4 ý; thứ người dùng thấy suy từ chương trình và sổ máy chủ, chưa chụp màn hình |
| model viết phần có nguồn rồi nối câu từ chối ở cuối | gỡ câu từ chối, kiểm phần còn lại | câu trả lời phần có nguồn | có từ 21/11 |
| kho không đủ | model trả câu từ chối; chương trình tra web một lần (bài 25) | câu từ chối; có mục web thì thay bằng câu dẫn sang mục web | đúng thiết kế |
| câu trả lời có con số thời tiết hay khoảng cách không khớp kết quả công cụ | gỡ câu chứa con số đó | câu trả lời thiếu câu đó | có (bài 24) |

## Dễ nhầm

- **"Có số nguồn là đã đúng."** Không. Số nguồn có thật chỉ cho biết đoạn đó tồn tại và đã được đưa cho model.
- **"Câu từ chối là do model tự nghĩ ra lời."** Không. Đó là một câu cố định ghi trong lời dặn; chương trình so đúng từng chữ.
- **"Kiểm xong mới hiện."** Trong ô chat thì chữ hiện trước, kiểm sau; hỏng thì rút lại.

## Câu hỏi tự kiểm

<details>
<summary>1. Ba luật kiểm số nguồn là gì, và luật nào bắt câu "Tôi không tìm thấy đủ thông tin… [3]"?</summary>

Có ít nhất một số nguồn · mọi số là của một nguồn đã thật sự đưa cho model · câu từ chối không kèm số nguồn. Câu đó phạm luật thứ ba.

</details>

<details>
<summary>2. Câu trả lời có số [4] và đoạn 4 có thật. Như vậy đã chắc đúng chưa?</summary>

Chưa. Chương trình chỉ biết đoạn 4 tồn tại và đã được đưa cho model; đoạn đó có nói đúng điều câu trả lời viết không thì chỉ đo được khi chấm (bài 19).

</details>

<details>
<summary>3. Bước viết lại một lần đã hết màn hình "Thử lại" ở tin dài nhiều ý ngay từ trưa 22/11. Vì sao trưa đó không mở, mà 14:47 lại mở?</summary>

Đứng riêng, 4 trong 5 câu viết lại nói "tư liệu chưa có" đúng hai ý kho có; theo thứ tự lỗi chủ dự án đã chốt, thiếu ý nặng hơn một lần "Thử lại". Lúc 14:47 nó mở cùng hai thay đổi ở khâu tìm và trần 3: lần tìm thứ ba đem về được ý còn lại, nên tin đó đủ hai ý 6 trên 6 lần; bước viết lại chỉ còn là chỗ đỡ khi model vẫn nộp chữ không nguồn.

</details>

## Cấu hình đang chạy

*Chép từ hệ thống đang chạy sau 14:47 ngày 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Dạng số nguồn được nhận | [n] và [Nguồn n], không phân biệt hoa thường; đưa hết về [n] khi hiện | model đôi khi chép nguyên nhãn của ngữ cảnh | đã đo trước và sau khi nhận cả hai dạng (mục "Đã so") |
| Câu từ chối khi kho không đủ | "Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này." | chương trình so đúng từng chữ | chưa thử câu khác |
| Câu cho câu hỏi ngoài phạm vi | "Mình chỉ hỗ trợ thông tin về văn hoá và du lịch Huế. Bạn muốn hỏi gì về Huế không?" | do bước xếp loại câu quyết định, không qua model viết (bài 22) | — |
| Các câu được tính là từ chối khi đo | hai câu trên, cộng ba câu "mình không làm thay được" (đặt chỗ, gửi tin, xem tình trạng phòng; bài 4) | thiếu một câu trong danh sách này thì một câu ngoài kho bị thay chữ sẽ bị đếm nhầm là "được trả lời" | — |
| Khi bước tìm không ra đoạn nào dùng được | đặt câu từ chối ngay, không gọi model | đỡ một lần gọi model | — |
| Câu từ chối nối ở cuối một câu trả lời có nguồn | gỡ câu từ chối, giữ phần có nguồn | trước khi có việc này, cả câu bị rút lại | có từ 21/11 |
| Dòng "có thể đã thay đổi" | nối khi câu trả lời trích bài thuộc nhóm vé, địa điểm, lễ hội, hoặc bài lưu trú | giá và giờ có thể đổi mà kho chưa sửa | — |
| Nguồn hiện dưới câu trả lời | chỉ các đoạn có số được nhắc trong câu trả lời | — | — |
| Viết lại một lần khi chữ nộp không có số nguồn (`het_luot_viet_lai`) | mở 14:47 22/11; chỉ khi model đã tự tìm ít nhất một lần; không ở câu cố định; cả ô chat lẫn đường không hiện chữ dần | thay màn hình lỗi bằng câu trả lời từ bằng chứng đã gom, hoặc câu từ chối | đứng riêng: không mở; cùng bộ: mở (mục "Đã so") |
| Chạy lại cả lượt khi bị rút ở bước kiểm sau khi viết | 1 lần, chỉ ở ô chat, ở lượt đang kèm câu trả lời liền trước, trừ cuộc có lịch (từ 22/11) | người dùng khỏi gặp màn hình lỗi ở tin kiểu "bỏ X đi" | trước khi có: 3 trên 7 lần ra màn hình lỗi; sau: 0 trên 5 (đo 22/11, Claude Sonnet 5.5) |
| Dòng "danh sách có thể chưa đủ" (`danh_sach_noi_that`) | mở từ 20/11; câu xin danh sách có nguồn kho, trừ lượt lịch, lượt có dòng "Tư liệu chưa có…", và câu hỏi về một nơi đã có tên trong nguồn | nói thật giới hạn của việc tìm theo đoạn | — |

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

**Vì sao "đúng một câu từ chối cố định" quan trọng với phép đo?** Chương trình nhận ra lượt từ chối bằng cách so chữ, nên đếm được chính xác bao nhiêu câu bị từ chối, từ chối nhầm, hay câu ngoài kho lọt qua; nó cũng là tín hiệu để mở mục tra web (quyết định 2).

**Vì sao không dùng một model thứ hai để kiểm câu trả lời có đúng với nguồn không?** Chưa thử trên đường người dùng. Việc đó hiện chỉ có ở phép đo: một model chấm điểm câu trả lời so với đáp án mẫu (bài 19).

**Vì sao chữ hiện trước rồi mới kiểm?** Bài 6, quyết định 4.

**Vì sao không gọi model khi bước tìm không ra đoạn nào dùng được?** Đặt câu từ chối ngay, đỡ một lần gọi model.

## Giới hạn đã biết

- **Chưa kiểm nghĩa** (đã nói ở trên).
- **Thiếu số nguồn chỉ bị phát hiện ở cuối**, sau khi chữ đã hiện. Người dùng thấy chữ rồi thấy nó bị rút.
- **Câu trả lời bị rút lại vẫn xảy ra.** Ở một lượt đo với người dùng mô phỏng ngày 21/11: 3 trên 48 lượt hỏi của gpt-6-luna và 4 trên 53 lượt hỏi của Claude Sonnet 5.5 có câu bị rút. Con số này gồm cả câu bị rút do bước kiểm con số thời tiết, không riêng do số nguồn, và đo trước bản sửa 13:51 21/11 (từ đó con số lạ ở lượt thường chỉ bị gỡ câu); mới một người đọc.
- **Dòng "có thể đã thay đổi" chỉ áp cho bốn nhóm bài:** vé, địa điểm, lễ hội, và bài "Lưu trú ở Huế". Ba nhóm đầu do chủ dự án chọn ngày 02/11: giờ, giá vé, ngày lễ hội đổi theo năm mà kho không ghi ngày nguồn. Bài lưu trú được thêm 14/11 vì hạng cơ sở có thể đã đổi. Nhóm khác (món ăn, quán) không có dòng này.
- **Một câu trả lời đúng nội dung mà quên số nguồn cũng bị rút**, vì chương trình không phân biệt được với một câu bịa.
- **Người đọc không thấy ý nào đến từ nguồn nào.** Vì số [n] không hiện trong chữ, dòng "Nguồn:" chỉ cho biết cả câu trả lời dựa vào những bài nào. Đây là lựa chọn của chủ dự án về giao diện.

## Chi tiết để tra

- Đếm lỗi số nguồn: 0 trên 489 lần viết (gpt-6-luna, đếm ngày 30/10); 0 trên 93 lượt (một lượt rà ngày 21/11 trên gpt-6-luna và các mức suy luận của Claude Sonnet 5.5).
- Việc nhận cả hai dạng số nguồn được sửa ngày 25/10.
- Trường hợp "câu trả lời có nguồn rồi nối câu từ chối ở cuối" được thấy ở 1 trên 3 lượt của một câu mà kho chỉ có một phần, ngày 21/11.
- Khi mục web có nội dung, máy chủ vẫn giữ nguyên câu từ chối trong kết quả của nó (các phép đo đọc câu này); chỉ giao diện thay bằng câu dẫn sang mục web.
- Câu hỏi nhiều ý: ý nào kho không có thì model ghi một dòng mở đầu bằng "Tư liệu chưa có thông tin về:"; dòng này không có số nguồn và không bị coi là lỗi (bài 23).
- Lần chạy lại hẹp: lời gọi model của cả hai lần đều vào sổ tiền; sổ số đo ghi tên lần chạy lại kèm đầu lời lỗi của lần đầu, không ghi chữ.
- Bước viết lại: sổ số đo ghi một mục riêng (tên, thời gian, có ra câu từ chối không), không ghi chữ; ở tin nhiều ý, lần viết lại nhận thêm một dòng dặn "ý nào Bằng chứng có thì trả lời kèm mã nguồn; ý nào không có thì ghi một dòng" để không từ chối cả câu. Lần viết lại có hạn 45 giây riêng.

**Bài sau (bài 17):** hết chặng 3. Đường hỏi đáp đã đủ: tìm, viết, kiểm. Chặng 4 trả lời câu hỏi "lấy gì bảo đảm nó tốt": bộ câu hỏi mẫu và cách chấm.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Ba luật, nhận cả `[n]` và `[Nguồn n]`: `backend/llm/citations.py` (`CITATION_PATTERN`, `normalize_citations`, `select_cited_sources`) [code, đọc 22/11/2026].
- Giao diện bỏ số [n] khỏi chữ và hiện dòng "Nguồn:": `frontend/src/markdown.js` (hàm `boMaTrichDan`), `frontend/src/SourceLine.jsx` [code]; lựa chọn của chủ dự án: `bai_hoc/17_GIAO_DIEN_VA_TOC_DO.md` mục "Hai lựa chọn đáng nhớ".
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
- Mục "Quyết định và lý do", "Nếu… thì sao", "Câu hỏi tự kiểm", "Quyết định nhỏ hơn", phần "Đã so" về màn hình "Thử lại" (thêm 14:05 22/11/2026 theo khuôn mới). Lời báo rút lại nguyên văn: `backend/api/routes/chat.py` `_loi_trich_dan` [code]. Lần chạy lại hẹp (điều kiện, không kèm câu trả lời cũ, không chạy lại câu cố định / cuộc có lịch, 3 / 7 trước khi có, chờ thêm khoảng 5 giây, đường "giữ chữ tới khi kiểm xong" không chọn): `backend/llm/assistant.py` `answer_turn_stream_parallel` và `TEN_CHAY_LAI`; `report_agent/2026-11-22/b_nho_dap_chay_lai.md` mục 1–3 [code + đã chạy, phiên khác]. Dòng "danh sách có thể chưa đủ" (khuôn chữ, lý do, 6 / 18, 5 / 6, câu một gợi ý không nhận): `backend/llm/danh_sach.py` (chú thích đầu file, `CAU_DANH_SACH`), điều kiện nối: `backend/llm/assistant.py` khoảng dòng 1162–1166; mở 16:15 20/11/2026: commit `051e954f`; dòng `danh_sach_noi_that: true` trong `backend/config/settings.yaml` (chú thích cạnh dòng còn ghi "TẮT tới khi…", lệch với giá trị) [code]. Ba câu "chưa làm thay được": `CAU_LAM_THAY` trong `backend/llm/full_corpus_prompt.py`. Bản chữa "viết lại một lần" (3 / 6 ⇒ 0 / 6, 0 / 5 con số bịa, 4 / 5 câu thiếu hai ý, 44 câu, 3,77 USD, thứ tự lỗi chủ dự án đã chốt): `bai_hoc/VIEC_MOI_XONG.md` mục 40, gạch "Đo rồi KHÔNG mở" [người thứ hai kiểm]. Sàn câu từ chối: `session_prompt/HIEN_TRANG.md` mục 4, gạch 11:24 21/11/2026. Luật "không trả một phần, không tự sửa, không tự gọi lại" và lỗi `citation_integrity_error`: `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md` mục 9, dòng 251–273 [chép]. Lần chạy lại: chỉ đường stream (`backend/api/routes/chat.py` khoảng dòng 204–216; đường không stream gọi `answer_turn`), điều kiện `trace.citation_error` bất kỳ (`assistant.py` khoảng dòng 1998), số sau sửa 0 / 5 và 2 / 5 lượt chạy lại thật: `report_agent/2026-11-22/b_nho_dap_chay_lai.md` mục 4 [người thứ hai kiểm]. Bản chữa "viết lại một lần": lúc 14:33 22/11 còn ở nhánh riêng; nay đã gộp và mở — `settings.yaml` của main có `het_luot_viet_lai: true` (MỞ 14:33 trong chú thích; runbook mục 0 đếm 45 lúc 14:47) [code, đọc 15:08 22/11/2026]. Cập nhật theo bộ thay đổi mở 14:47 22/11/2026: `bai_hoc/VIEC_MOI_XONG.md` mục 42, 43; `guides/RUNBOOK_BAN_GIAO.md` mục 10.1; `backend/config/settings.yaml` [code; số đo: đã chạy, phiên đo; người viết không chạy lại]. Điều kiện và hạn giờ: `backend/llm/assistant.py` `_viet_lai_het_luot`, `TEN_VIET_LAI`; dòng dặn tin nhiều ý `VIET_LAI_NHIEU_Y_TEXT` (`backend/llm/full_corpus_prompt.py`); 9 lần kích hoạt thật đều "đã hết lượt": runbook 10.1 hàng "Lưới viết lại một lần" [code + chép]. Dòng chồng nhau với công cụ mục lục: `assistant.py` khoảng dòng 1162–1166 không loại nguồn mục lục [code, chưa thử]. Bốn nhóm bài của dòng "có thể đã thay đổi": `assistant.py` `NOTICE_SOURCE_PREFIXES`; lý do ba nhóm đầu: đặc tả Phase 9 bản 5 (`git show 077e3cb:docs/superpowers/specs/2026-11-02-phase-9-design.md` bảng quyết định Q2 và mục 5.3); bài lưu trú: chú thích cạnh `NOTICE_SOURCE_PREFIXES` [code + chép]. Số 3 / 48 và 4 / 53 đo trước commit `5936d165` (13:51 21/11): `VIEC_MOI_XONG.md` mục 23 ghi lúc 13:48 21/11. Các mục mới đã qua một lượt đối chiếu độc lập 14:28 22/11/2026 và được sửa theo: `data/hoc_cung_D/kiem/muc_moi_12_16.md` [riêng tư].

- Đã qua một lượt kiểm chéo sau lượt cập nhật 14:47 (`data/hoc_cung_D/kiem/cap_nhat_14h47.md`) [riêng tư]. Theo đó: bảng Nếu dòng 1 và dòng viết lại không còn trái nhau (thiếu số nguồn: viết lại khi model đã tự tìm ≥ 1 lần, rút lại khi chưa tìm lần nào — `_viet_lai_het_luot` điều kiện `model_searches >= 1`); thêm thứ người dùng thấy khi viết lại (`bai_hoc/VIEC_MOI_XONG.md` mục 42, đính chính 15:14; runbook 10.1 hàng "Lưới viết lại"; suy từ chương trình và sổ máy chủ, chưa chụp màn hình); đáp án câu tự kiểm 3 sửa ("6 trên 6" là tin đó qua 6 lần hỏi ở lượt nối, không phải câu viết lại — mục 42 ý 2); câu dẫn bảng bốn cột sửa thứ tự (điều kiện đổi SAU lượt nối). Cắt nửa để hiểu: quyết định 5 cũ (dòng "danh sách có thể chưa đủ") và câu hỏi tự kiểm 3 cũ chuyển xuống "Quyết định nhỏ hơn"; quyết định 6 cũ thành quyết định 5.

</details>
