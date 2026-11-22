# Bài 40 — Làm được tới đâu, còn yếu ở đâu, hướng phát triển

*Cập nhật 17:11, ngày 22/11/2026 · khớp hệ thống 16:35 22/11 (47 tính năng, kho 267 bài): bộ câu cất riêng đã có lúc chạy, giữ chữ đã nhìn trên trình duyệt · số chép từ bài gốc (ghi "bài N"), không đo mới.*

**Bài trước đã biết:** hệ thống được làm ra thế nào, ai kiểm ai (bài 39).
**Bài này thêm:** theo từng mảng: làm được gì, chưa làm được gì, chỗ yếu nào nặng nhất, thứ gì chưa đo, hướng phát triển nào có căn cứ.

## Ý chính

- Trên một máy, người dùng làm được trọn **ba loại việc**: hỏi đáp có nguồn từ kho 267 bài; vài việc cần tính (ngày âm lịch, thời tiết, khoảng cách, lễ hội theo ngày); lên một lịch rồi sửa lịch bằng lời. Có 47 tính năng đang mở (đếm 16:13 22/11).
- **Chỗ yếu nặng nhất** xếp theo thứ tự lỗi của bài 4: bước kiểm chỉ kiểm số nguồn có thật, chưa kiểm nghĩa; tin dài nhiều ý dễ thiếu ý; kho có mà tìm không ra thì từ chối nhầm. Ngoài chất lượng là thời gian chờ: lượt hỏi đáp đứng giữa khoảng 13 giây, tin dài nhiều ý 25–34 giây (bài 34).
- **Kho là trần.** Ở ba lượt đo mốc ngày 21/11 với 12 người dùng mô phỏng, mỗi người một mục tiêu (bài 32), một phiên phân loại 19 lần một ý bị trượt: 12 do kho thiếu, 1 do tìm không ra. Lượt đo lại 22/11 còn 5 ý trượt, 2 do kho thiếu, 0 do tìm.
- **Nhiều thứ chưa đo:** chưa có người dùng thật, bộ 176 câu chưa chạy đủ trên model đang chạy, bộ câu cất riêng của phần trợ lý chưa dùng (hai bộ cất riêng của bộ 176 câu đã dùng từ tháng 10, bài 17), mới bốn ca hỏng được thử thật.
- **Hướng phát triển** chỉ ghi những hướng có trong hồ sơ, mỗi hướng kèm chỗ yếu nó nhằm tới và phép đếm rẻ nhất. Đưa lên mạng chưa làm: chủ dự án dặn tập trung hoàn thành ở máy trước.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| vế cụt | — | một vế của tin nhiều ý bị tách ra mà mất tên đối tượng, ví dụ "mấy giờ mở cửa?" |
| chữ chạy dần | **streaming** | model gửi từng mẩu chữ ngay khi viết; hiện nay với Claude, chữ tới một lần khi viết xong (bài 33) |

## Người dùng làm được ba loại việc, trên một máy

Mỗi dòng một mảng, kèm **một con số chính** lấy từ bài giảng mảng đó.

| Mảng | Người dùng làm được | Chưa làm được | Một con số |
|---|---|---|---|
| Hỏi đáp từ kho | hỏi món, di tích, lễ hội, vé, đi lại; câu trả lời có nguồn bấm xem được; kho không có thì nhận câu từ chối cố định | câu kho có mà bước tìm không ra vẫn bị từ chối | từ chối nhầm 3 trên 158 câu kho có (gpt-6-luna, 12/11); 0 trên 78 câu (Claude, 21/11, mẫu nhỏ hơn) (bài 4) |
| Trợ lý nhiều lượt | hỏi tiếp "còn chỗ đó thì sao", "quán thứ hai bạn vừa kể" (cả trong cuộc đã lập lịch); hỏi nhiều ý trong một tin | tin dài 4–5 ý dễ thiếu ý; chỉ nhớ câu trả lời liền trước (bài 23) | 12 vai: 7 · 7 · 8 trên 12 phiên đạt (Claude, 21/11) (bài 32); đo lại 22/11: 8 trên 12 |
| Việc chương trình tính | ngày âm ↔ dương, dự báo 7 ngày, khoảng cách giữa 40 điểm, "gần X có gì", lễ hội theo ngày | tổng tiền vé do model tự cộng; khoảng cách ngoài 40 điểm | công cụ đổi ngày bớt 9 câu từ chối nhầm, 0 câu sai ngày (gpt-6-luna, 09/11) (bài 24) |
| Tra web | kho từ chối thì có mục riêng "Từ web (chưa kiểm)" | mục web chỉ được kiểm con số, không kiểm địa chỉ hay ý | 2 trên 44 câu ngoài phạm vi bị gửi đi tra web vì xếp loại nhầm (bài 25) |
| Hỏi bằng ảnh | gửi ảnh, hệ thống đoán trong 42 tên nơi và món, người dùng xác nhận rồi hỏi | hỏi chi tiết trong ảnh; phân biệt các lăng giống nhau | khi cho trả lời thẳng, model gán tên Huế cho 2 trên 5 ảnh không phải Huế (05/11) (bài 26) |
| Lên kế hoạch | bấm nút, nhận lịch theo buổi kèm chỗ ở, quán ăn, bản đồ; tải về | điểm ngoài bảng 41 điểm; giờ tới, giờ về; xếp lịch từ câu gõ tự do | ở ví dụ: khung lịch sau 0,2 giây, đủ câu mô tả sau 9,3 giây (Claude, 21/11) (bài 27) |
| Sửa lịch bằng lời | bỏ, thêm, thay, dời buổi, đổi số ngày, đổi chỗ hai ngày | thay hoạt động buổi tối; ngày tương đối ("dời 2 hôm") | bộ 10 chuỗi sửa lịch đạt 9 trên 10, đo trước khi đổi sang Claude (bài 31) |
| Giao diện | sáu trang, khung trợ lý ở mọi trang, chạy được ở bề rộng điện thoại | mở ở tab thứ hai thì mất cuộc của tab thứ nhất; chưa thử điện thoại thật | lượt kiểm chốt trưa 22/11: 41 tin qua trình duyệt, 0 màn hình lỗi (bài 34) |
| Máy móc | bật cả hệ thống bằng một lệnh; bộ test tự động | chưa đưa lên mạng; một máy, một bản máy chủ, một hãng model | từ lúc Qdrant tắt, lệnh bật ra "SẴN SÀNG" sau 34 giây (bài 36) |

## Chỗ yếu đã biết, xếp theo mức nặng

Xếp theo thứ tự lỗi của bài 4, từ nặng tới nhẹ.

| Nấc | Chỗ yếu | Con số hay dấu hiệu |
|---|---|---|
| 1. Cảnh báo an toàn | danh sách từ mà chương trình dùng để nhận ra câu về bão, lũ, ngập vẫn sót vài cách nói tự nhiên ("nước có lên nữa không") (bài 24); phần "model tự nhận ra thiên tai" chưa có lượt model thật | không có số |
| 2. Nói chắc mà sai | bước kiểm chỉ biết số nguồn có thật, chưa biết đoạn được trích có nói đúng điều đó không (bài 16) · ảnh gán nhầm một lăng thì trả lời luôn về sai nơi (bài 26) · câu thẻ lịch của Claude có thể ghép sai ý một câu nguồn dài (bài 33) | câu thẻ lịch: một mục, 12 lượt, sai 1, nói lỏng 4 (bài 33) |
| 3. Trả lời câu ngoài kho | nhận xét của một phiên, chưa đếm: câu ngoài tỉnh lọt bước xếp loại thì chỉ còn trông vào model tự từ chối | sàn "0 câu" giữ ở các lượt đo |
| 4. Thiếu ý | tin dài nhiều ý (bài 16, 23) · dòng "Tư liệu chưa có thông tin về…" có lúc sai (kho có) · kho thiếu | dòng "chưa có" sai khoảng 13 % (một phiên đọc tay; "Chi tiết để tra") |
| 5. Từ chối nhầm | kho có mà bước tìm không lấy ra, như câu cởi giày vào chùa (bài 13) | 16 trên 40 câu khó thiếu đoạn đúng trong 10 đoạn (bài 13) |
| ngoài thứ tự lỗi | **chờ lâu**, chữ tới một lần · khởi động lại máy chủ mất cuộc và lịch, không báo (bài 6) · tab thứ hai xoá cuộc của tab thứ nhất (bài 35) · một hãng model, không dự phòng (bài 6) | khoảng 13 giây ở lượt đứng giữa, một phần ba quá 15 giây (Claude, 49 lượt chạy một mình, 21/11) (bài 34) |

## Những thứ chưa đo

- **Chưa có người dùng thật.** Bộ câu do AI soạn hoặc do nhóm gõ; người dùng mô phỏng thường dễ hơn người thật. Trên một bộ cất riêng, điểm "đủ ý" thấp hơn bộ quen khoảng 0,4 trên thang 5 (bài 17).
- **Bộ 176 câu chưa chạy đủ trên model đang chạy:** mới 85 câu đầu và 54 câu so sánh (bài 32).
- **Bộ câu cất riêng của phần trợ lý chưa dùng** cho lượt so sánh cuối (khác hai bộ cất riêng của bộ 176 câu, đã dùng 28/10 và 01/11 — bài 17). Chủ dự án đã chọn (15:57 22/11): chạy đúng một lần sau buổi tự thử hệ thống và các bản sửa của buổi đó, trên model sẽ dùng lúc bảo vệ.
- **Mới bốn ca hỏng được thử thật,** mỗi ca một lượt (bài 6).
- **Các tính năng mở 21–22/11 chưa đo trên gpt-6-luna.** Trên Claude, lượt 12 vai đo lại 22/11 ra 8 trên 12 phiên, 33 trên 38 ý, trong khoảng nhiễu của mốc, chạy trước bốn thay đổi cho tin dài; thước có một điểm mù ("Chi tiết để tra").
- **Nhiều người hỏi cùng lúc** mới đo một lần, ngày 27/10 (bài 6). Điện thoại thật, in bằng tay: chưa ai thử.

## Hướng phát triển có căn cứ

Chỉ ghi hướng đã có trong sổ việc, danh sách ý chưa thử hoặc danh sách giới hạn của dự án. Không có lộ trình ngày tháng.

| Hướng | Nhằm chỗ yếu nào | Đếm hay thử rẻ nhất | Đang ở đâu |
|---|---|---|---|
| Bổ sung kho: quy định chụp ảnh (đường Huế – Hội An đã có bài từ chiều 22/11) | kho thiếu | gom các lượt "kho thiếu" theo chủ đề, ra mười thứ thiếu nhiều nhất | bài Hội An đã vào kho chiều 22/11 sau khi chủ dự án duyệt bản nháp; quy định chụp ảnh chưa tìm được nguồn công khai nói dứt khoát |
| Đo bốn thay đổi cho tin dài trên nhiều tin dài | thiếu ý ở tin dài | một lượt nhiều tin dài khác nhau | đã mở 14:47 22/11; mới đo trên một tin |
| Chữ chạy dần thật | chờ trắng 10–17 giây | ước, chưa đo: chờ tới chữ đầu từ khoảng 13 xuống khoảng 6 giây | cần một quyền ở tài khoản AWS; chủ dự án gác chuyện AWS tới khi tự xem lại |
| Chạy riêng bước tìm cho câu bị từ chối mà kho có đáp án | từ chối nhầm | câu "cởi giày" trên chỉ mục hiện tại; đếm trên 176 câu | chưa đếm |
| Mỗi tab một mã cuộc trò chuyện | tab thứ hai xoá cuộc của tab thứ nhất | đã xác nhận thật một lần | chưa làm |
| Đo bù trên gpt-6-luna; lượt cuối trên bộ câu cất riêng của phần trợ lý | thứ chưa đo | 12 vai, 41 câu khó và các sàn | bộ cất riêng: một lần, sau buổi chủ dự án tự thử (15:57 22/11); gpt-6-luna và phần so với "RAG mốc": cần tiền OpenAI |

**Đưa lên mạng.** Chưa làm. Lời chủ dự án sáng 22/11: "giờ tập trung hoàn thành ở local đi nhé". Các chốt cần cho lúc đó đã có trong chương trình nhưng đang tắt (bài 37); gói ba hộp Docker đã cũ (bài 36).

## Quyết định và lý do

Các quyết định của bài này là về **phạm vi và thứ tự**, phần lớn do chủ dự án chốt.

### 1. Vì sao làm xong ở máy trước, rồi mới tính đưa lên mạng?

- **Đã chọn:** xong hết ở máy ⇒ chủ dự án tự thử một lần ⇒ không phát triển thêm ⇒ đưa lên mạng nếu làm.
- **Vì sao:** chủ dự án chốt thứ tự này ngày 19/11; ngày 21/11 anh nói đưa lên mạng không bắt buộc, là điểm cộng.
- **Cách khác:** đưa lên mạng sớm để có người dùng thật: chủ dự án không chọn.
- **Cái giá:** chưa có số nào từ người dùng thật; các chốt cho lúc đưa lên mạng chưa được thử trên bản thật.

### 2. Vì sao lỗi hiếm chỉ ghi giới hạn mà không sửa?

- **Đã chọn:** lỗi người dùng dễ gặp, lỗi an toàn, lỗi ghi sai kho thì sửa; lỗi hiếm ghi một dòng giới hạn kèm số lượt thật đã gặp.
- **Vì sao:** chủ dự án chọn ngày 20/11, cùng lúc với lời "test vừa đủ".
- **Cách khác:** sửa mọi điểm tìm ra: không làm.
- **Cái giá:** danh sách giới hạn dài; vài chỗ phải biết trước khi chạy thử (bài 41).

### 3. Vì sao không làm bước "viết lại câu hỏi trước khi tìm"?

Chủ dự án hỏi về bước này sáng 22/11. Nó là một lần gọi model viết lại câu hỏi cho rõ (ví dụ thay "chỗ đó" bằng tên nơi) trước khi tìm.

- **Đã chọn:** không làm.
- **Vì sao:** trong 19 lần một ý bị trượt ở ba lượt mốc, chỉ 1 lần là "kho có mà tìm không ra"; lượt đo lại 22/11 không còn lần nào.
- **Cách khác:** model đã tự viết câu tìm khi xin tìm thêm (bài 23); "viết câu trả lời giả rồi tìm theo nó" chưa thử.
- **Cái giá:** các ca như câu cởi giày vẫn bị từ chối.

### 4. Vì sao hai bản chữa đứng riêng thì không mở, mà một bản được mở khi ghép với khâu tìm?

- **Đã chọn:** bản chữa tin hỏi hai ý viết tắt kiểu "vé bn, có giảm ko" để tắt. Bản "viết lại một lần khi không có nguồn" mở từ 14:47 22/11, chỉ cùng ba thay đổi ở khâu tìm.
- **Vì sao:** bản viết tắt: 16 tin, mỗi bên đủ hai ý 10 trên 10, mở lên chỉ thêm 2 dòng "chưa có" sai. Bản viết lại đứng riêng: màn hình lỗi 3 trên 6 xuống 0, nhưng 4 trên 5 câu viết lại ghi "chưa có" cho hai ý kho có; thiếu ý nặng hơn một lần "Thử lại". Ghép với khâu tìm thì nêu đúng cả hai ý 6 trên 6.
- **Cách khác:** mở bản viết lại đứng riêng: đã đo, bỏ.
- **Cái giá:** tin dài lâu hơn (khoảng 20 lên 25–34 giây); lợi mới đo trên một tin.

### 5. Vì sao không thêm nhiều agent phối hợp lúc trả lời?

- **Đã chọn:** một trợ lý có công cụ cộng vài lời gọi model hẹp (đoán ảnh, hiểu lệnh sửa lịch).
- **Vì sao:** nhận định của nhóm, chưa đo: lỗi đang thấy là kho thiếu, tìm trượt, chậm vì viết dài; thêm agent làm lượt chậm hơn và thêm thứ phải giải thích. Chỗ duy nhất có dáng việc nhiều bước độc lập là lên lịch từ câu gõ tự do, đã đo không đạt (06/11, gpt-6-luna).
- **Cách khác:** thử lại lên lịch từ câu gõ trên model mạnh hơn: chưa thử.
- **Cái giá:** ghi lại làm hướng phát triển nếu lỗi đổi loại.

## Nếu… thì sao

| Khi điều kiện đổi | Điều đã biết | Đã có chưa |
|---|---|---|
| có người dùng thật | bộ câu và người dùng mô phỏng thường dễ hơn; điểm có thể thấp hơn | chưa có |
| lúc bảo vệ dùng lại gpt-6-luna | đổi một dòng cấu hình; tính năng mở 21–22/11 chưa đo trên model đó (bài 33) | đường đổi có; lượt đo bù chưa có |
| kho thêm bài | thêm bài là một lần đo trước và sau; một lệnh cập nhật chỉ mục khoảng nửa phút (bài 7, 12) | có |

## Dễ nhầm

- **"8 trên 12 là tỉ lệ người dùng hài lòng."** Đó là tỉ lệ đạt trong mô phỏng: người dùng do một model đóng vai, thường dễ hơn người thật.
- **"Câu trả lời có số nguồn là câu trả lời đúng."** Bước kiểm chỉ biết số nguồn có thật, chưa kiểm đoạn đó có nói đúng điều được viết.
- **"Những thứ cố ý không làm là lỗi còn nợ."** Câu không dấu, tiếng Anh, tình huống khẩn cấp, giá phòng là ranh giới đã chọn (bài 4).

## Câu hỏi tự kiểm

<details>
<summary>1. Lần trượt chủ yếu do đâu, và vì sao điều đó quan trọng khi chọn việc tiếp?</summary>

Do kho thiếu (12 trong 19 lần ở ba lượt mốc; 0 lần do tìm ở lượt đo lại). Nên bổ sung kho nâng được nhiều nhất.

</details>

<details>
<summary>2. Chỗ yếu nặng nhất theo thứ tự lỗi là gì?</summary>

Ở nấc "nói chắc mà sai": bước kiểm chỉ kiểm số nguồn có thật, chưa kiểm nghĩa. Ở nấc cảnh báo an toàn còn vài cách nói tự nhiên chưa được nhận ra.

</details>

<details>
<summary>3. Vì sao bản "viết lại một lần" đứng riêng thì bỏ, ghép với khâu tìm thì mở?</summary>

Đứng riêng, 4 trên 5 câu viết lại thiếu hai ý kho có. Ghép với khâu tìm, cả hai ý được nêu 6 trên 6.

</details>

<details>
<summary>4. Kể hai thứ chưa đo.</summary>

Chưa có người dùng thật; bộ 176 câu chưa chạy đủ trên model đang chạy. Ngoài ra: bộ câu cất riêng của phần trợ lý chưa dùng, mới bốn ca hỏng được thử thật.

</details>

## Chi tiết để tra

- **Tính năng đang mở / tắt:** 47 mở, 3 tắt (đếm 16:13 22/11, sau khi mở việc nhớ câu trả lời liền trước trong cuộc đã lập lịch; lúc 15:51 là 46, sau khi mở việc giữ chữ tới khi qua bước kiểm nguồn; lúc 14:52 là 45, đếm bằng lệnh của phụ lục B; phụ lục B đếm 13:20 ra 42, trước khi ba tính năng khâu tìm được mở). Ba cái tắt: xếp lịch từ câu gõ tự do (đo không đạt), dòng "hôm nay là ngày…" (vô ích), sổ vết từng lượt (chỉ dùng ở máy phát triển).
- **Kho:** 267 bài, 9.479 đoạn (bài 7).
- **Bộ test:** lượt kiểm chốt trưa 22/11: 76 file, 2.060 ca đạt (bài 38, Chi tiết để tra). Sau khi bốn thay đổi được mở, cả bộ test chạy lại 14:48–15:03 22/11: 78 file, 2.119 ca đạt, 2 ca hỏng — đều là ca test cũ so nguyên một bảng nay có thêm tên nhà cung cấp model của trang Giới thiệu, không phải sản phẩm sai (bài 38).
- **Thời gian chờ:** 13 giây là 49 lượt hỏi đáp của người dùng mô phỏng trưa 21/11, tin dài hơn và còn mục web; 6,9 giây là 41 tin phần lớn ngắn ở lượt kiểm chốt trưa 22/11, lúc máy rảnh; 95 % dưới 13,1 giây (bài 34).
- **Phân loại 19 lần trượt:** 12 kho thiếu (đi Hội An, quy định chụp ảnh, sự kiện có ngày, điểm ít leo bậc; nay đi Hội An và điểm ít leo bậc đã có bài, sự kiện có ngày đã có công cụ; còn quy định chụp ảnh), 4 sửa lịch (đã sửa), 2 model không ghép hai dữ kiện có sẵn, 1 tìm không ra; một phiên đếm chiều 22/11, khâu tìm chạy lại trên chỉ mục hôm đó. Lượt đo lại: 5 ý trượt — kho thiếu 2, model không ghép 1, hai ý sửa lịch thước không đọc được, tìm không ra 0.
- **Bốn thay đổi cho tin dài nhiều ý (mở 14:47 22/11):** ba ở khâu tìm, một là bước viết lại — bỏ tìm riêng vế cụt; tách câu tìm model gộp hai nơi; cho tìm thêm 3 lần thay vì 2; viết lại một lần khi chữ nộp không có nguồn. Trước đó, ở một tin 4 ý, màn hình "Thử lại" hiện 3 trên 6 lần (bài 16). Trên chính tin đó, 6 lần: 0 màn hình lỗi, nêu đúng cả hai ý kho có 6 trên 6. Lợi mới đo trên một tin, nên nhóm mở theo cơ chế (đưa đúng đoạn vào), không ghi là "giảm lỗi".
- **Dòng "chưa có" sai khoảng 13 %:** một phiên đọc tay 30 trong 119 dòng của ba lượt mốc; khoảng tin cậy 4–31 %.
- **Điểm mù của thước 12 vai:** người mô phỏng không thấy dòng báo của lượt sửa lịch; công cụ đã chữa, chưa đo lại.
- **Lượt đo bốn thay đổi cho tin dài:** một tin 4 ý, 6 lần mỗi bên; màn hình lỗi bản cũ 5 · lọc và tách 3 · thêm viết lại 0 · thêm lần tìm thứ ba 0; nêu đúng cả hai ý 0 · 1 · 1 · 6 trên 6.
- **Câu bị rút lại sau khi đã hiện:** 3 trên 48 và 4 trên 53 lượt ở một lần đo ngày 21/11 (bài 16). Từ 15:42 22/11, với model đang chạy, ở ô chat, mọi lượt hỏi đáp về Huế giữ chữ tới khi qua kiểm nên không còn cảnh chữ hiện rồi mất (bài 6). Đã nhìn trên trình duyệt 16:17–16:20 22/11 (cả lần nhìn gồm 16 lượt hỏi ở năm phần, 0 màn hình lỗi): ở tin gia đình bốn ý, 29,5 giây, máy đọc màn hình mỗi 0,25 giây không thấy chữ nào hiện trước lúc câu trả lời đủ. Ca "bản viết đầu là chữ giữ chỗ nên được viết lại" chưa trúng lần nào trên trình duyệt (mới một lượt thật chạy bằng chương trình). Chưa đo lại tỉ lệ trên nhiều lượt.
- **Ảnh có chữ ra lệnh:** 1 trên 3 ảnh lừa được model (05/11), hậu quả bị chặn (bài 37).
- **Dời một điểm trong lịch:** làm được 24 trên 176 lần thử; hướng "nới luật xếp" có trong danh sách ý chưa thử, chưa đếm.
- **Vế cụt:** trên 364 tin nhiều ý đã ghi, 236 tin (65 %) có ít nhất một vế cụt; đọc tay 28 đoạn chúng kéo về, 20 không liên quan. Trên 8 dữ kiện kho có của phép đo sáng 22/11: tắt tìm theo vế thì 1 có trong đoạn tìm về, đang chạy 5, lọc vế cụt 4.
- **Chữ chạy dần thật:** số ước dựa trên phép tách thời gian 49 lượt ngày 21/11: lần viết cuối chiếm 72 % (bài 34). Hạ mức suy luận chỉ mua khoảng 0,3 giây (bài 34).
- **Danh sách giới hạn đầy đủ** của từng mảng nằm ở sổ tay bàn giao của dự án, mục 10; mỗi bài 13–38 có mục "Giới hạn đã biết" của mảng đó.

**Bài sau (bài 41):** kể lại toàn bộ trong một phút và năm phút, và kịch bản chạy thử.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Số trong bảng "làm được": bài 4 quyết định 1 (3 / 158, 0 / 78); bài 32 "Ý chính" (7 · 7 · 8); bài 24 mục "Đã so" dòng 2; bài 25 "Ý chính" (2 / 44); bài 26 "Ý chính" (2 / 5, 42 tên); bài 27 "Ý chính" (0,2 và 9,3 giây); bài 31 "Ý chính" và mục "Đã so" (9 / 10, 14–19/11, trước khi đổi sang Claude); bài 34 "Chi tiết để tra" (41 tin, 6,9 giây, 13,1 giây, 0 lỗi); bài 36 "Chi tiết để tra" (34 giây) [chép từ giáo trình].
- 47 tính năng mở, 3 tắt: `sed -n '/^assistant:/,$p' backend/config/settings.yaml | grep -cE '^  [a-z_0-9]+: true'` ra 47 lúc 16:13 22/11 trên main `2a221e5`, sau khi mở `nho_dap_cuoc_co_lich` (`guides/RUNBOOK_BAN_GIAO.md` mục 0 dòng 26; `backend/config/settings.yaml` dòng 76, "MỞ 16:08") [chép; người sửa chạy lại lệnh 22/11 trên main `0430104e` ra 47 — đã chạy]; trước đó 46 lúc 15:51 trên main `15cd5985` sau khi mở `giu_chu_toi_kiem`; người viết chạy lúc 14:52 ra 45; ba tính năng tắt: `HIEN_TRANG.md` dòng 19.
- Bộ câu cất riêng của phần trợ lý: quyết định của chủ dự án `session_prompt/HIEN_TRANG.md` mục 4 gạch "15:57 22/11/2026" (dòng 62) và dòng 48 (G-1 "ĐÃ CÓ TRẢ LỜI 15:57") [lời chủ dự án]; đo bù gpt-6-luna khi có tiền OpenAI: mục 4 gạch 21:50 21/11 và gạch 11:29 21/11 [lời chủ dự án].
- Giữ chữ đã nhìn trên trình duyệt (16 lượt, 0 màn hình lỗi, 29,5 giây, mỗi 0,25 giây) và ca chữ giữ chỗ chưa trúng: `bai_hoc/VIEC_MOI_XONG.md` mục 44 dòng 33, 36, 42 [chép; máy kiểm của phiên đo]; "mọi lượt hỏi đáp về Huế ở ô chat": `backend/llm/assistant.py` 352–354, 1979–1988 theo biên bản kiểm chéo 15:42 Phần 1 [chép biên bản]. Nhớ trong cuộc đã lập lịch, chỉ nhớ câu liền trước: settings dòng 76, mục 44 dòng 40 [code; chép].
- Thứ tự lỗi: bài 4. Chỗ yếu: bài 24, 16, 26, 33, 13, 34, 6, 35 mục "Giới hạn đã biết" [chép]. Một hãng model, không dự phòng: `HIEN_TRANG.md` mục 4 gạch 21:43 21/11 điểm (5); bài 6.
- "Model tự nhận ra thiên tai" chưa có lượt model thật: `bai_hoc/VIEC_MOI_XONG.md` mục 40 ý 2 [chép].
- Nấc 3: nhận xét của một phiên `session_prompt/Y_CHUA_THU.md` ý 3 [chưa đếm]; câu Hội An 20 / 20 bị chặn ở bước xếp loại: `data/thu_bedrock_2026-11-21/do/demo/KET_QUA_DEMO.md` [riêng tư; đã chạy 21/11].
- Dòng "chưa có" sai khoảng 13 %: `Y_CHUA_THU.md` ý 44; `data/review_khac_hang/2026-11-22_moc_sang/c_dem/KET_QUA_DEM.md` [riêng tư; một phiên đọc tay].
- 12 / 19 và phân loại: `HIEN_TRANG.md` mục 3 G-4, `Y_CHUA_THU.md` ý 33, `VIEC_DANG_MO.md` hàng X9; file đếm `KET_QUA_DEM.md` [riêng tư; một phiên, chưa ai tính lại]. Lượt đo lại 12 vai (8 / 12, 33 / 38 ý, 5 ý trượt, điểm mù dòng báo sửa lịch): `VIEC_DANG_MO.md` hàng X3 (14:13 22/11) và `bai_hoc/VIEC_MOI_XONG.md` mục 43 [phiên đo, một lượt; người chấm là agent con].
- Bốn thay đổi khâu tìm (mở cho người dùng 14:47 theo `guides/RUNBOOK_BAN_GIAO.md` mục 0 và `bai_hoc/VIEC_MOI_XONG.md` mục 42; chú thích cấu hình ghi 14:33 — giờ nhánh đạt tiêu chí; số của lượt ba bên và lượt nối; "mở theo cơ chế, không ghi là giảm lỗi"; 20 ⇒ 25–34 giây): `backend/config/settings.yaml` (`tim_ve_bo_cut`, `tach_cau_tim_model`, `het_luot_viet_lai`, `so_lan_tim_kho` 2 ⇒ 3) [code, đọc 14:48]; `VIEC_DANG_MO.md` hàng X7 (14:29); `bai_hoc/VIEC_MOI_XONG.md` mục 42 [người thứ hai kiểm theo nhãn mục đó; phần ghép bốn thứ và cả bộ test sau gộp: chưa kiểm].
- Chưa đo: bài 17 (0,4); bài 32 dòng 208 (85 + 54); `HIEN_TRANG.md` mục 3 G-1, `VIEC_DANG_MO.md` hàng X4 (bộ kín); bài 6 (bốn ca, 27/10); `VIEC_DANG_MO.md` hàng X2 (điện thoại thật, in tay) [tài liệu].
- Hướng: bổ sung kho `HIEN_TRANG.md` mục 3, `Y_CHUA_THU.md` ý 15; vế cụt 327 / 1.240, 236 tin, 28 đoạn, 8 dữ kiện: `KET_QUA_DEM.md` mục 4 [riêng tư] và `VIEC_DANG_MO.md` hàng X9; chữ chạy dần: `Y_CHUA_THU.md` ý 13, `HIEN_TRANG.md` mục 3 (0 (a), 1); câu cởi giày: `Y_CHUA_THU.md` ý 36; mỗi tab một mã cuộc: `VIEC_DANG_MO.md` hàng X2; đo bù gpt-6-luna: `HIEN_TRANG.md` mục 4 gạch 21:50 21/11; lên lịch từ câu gõ: `Y_CHUA_THU.md` ý 6; dời một điểm: ý 4.
- Đưa lên mạng: lời chủ dự án 08:55 22/11 (`HIEN_TRANG.md` mục 3 gạch 1, nguyên văn); thứ tự đóng 19/11, "không bắt buộc, là điểm cộng" 21/11: `HIEN_TRANG.md` mục 2 bước 8, mục 4 [lời chủ dự án]. Chốt đang tắt: bài 37; gói Docker cũ: bài 36.
- Quyết định 2: `HIEN_TRANG.md` mục 4 "Cách làm" điều (2) của tám điều 15:56 20/11 [lời chủ dự án]. Quyết định 3: `Y_CHUA_THU.md` ý 33. Quyết định 4: `bai_hoc/VIEC_MOI_XONG.md` mục 40 ý 3 và mục 42. Quyết định 5: `Y_CHUA_THU.md` ý 34 (nhận định của phiên điều phối).
- Bộ test 2.060 ca: bài 38 "Chi tiết để tra"; `HIEN_TRANG.md` dòng 20 [máy kiểm, phiên đo].
- Số khác ở "Chi tiết để tra": bài 16 (3 / 48, 4 / 53), bài 37 (1 / 3 ảnh), bài 34 (72 %, 0,3 giây, dòng 29 "49 lượt … chạy một mình").
- Bài đã qua một lượt đối chiếu độc lập (14:43 22/11/2026): `data/hoc_cung_D/kiem/bai_39_41.md` [riêng tư]; các dòng đã áp và không áp ghi ở báo cáo của người viết.

- Đã qua một lượt kiểm chéo sau lượt cập nhật 14:47 (`data/hoc_cung_D/kiem/cap_nhat_14h47.md`) [riêng tư]. Theo đó: giờ mở thống nhất 14:47 (ghi chú 14:33 chỉ ở khối Nguồn); "bốn thay đổi ở khâu tìm" ⇒ "bốn thay đổi cho tin dài nhiều ý (ba ở khâu tìm, một là bước viết lại)"; bộ test chạy lại 14:48–15:03: `session_prompt/HIEN_TRANG.md` mục 1 gạch "Cả bộ test" và `bai_hoc/VIEC_MOI_XONG.md` mục 42 dòng trạng thái [đã chạy, phiên đo; người viết không chạy lại].

</details>
