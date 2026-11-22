# Bài 34 — Người dùng chờ bao lâu, một câu tốn bao nhiêu tiền

*Cập nhật 15:11, ngày 22/11/2026 · thêm thời gian chờ của tin dài nhiều ý sau bộ thay đổi mở 14:47 22/11 (một tin, 6 lần, Claude Sonnet 5.5) · thời gian từng lời gọi lấy từ một lượt người dùng mô phỏng chạy đơn trưa 21/11 (Claude Sonnet 5.5, mức suy luận cao, 49 lượt hỏi đáp; so với gpt-6-luna 43 lượt); thời gian chờ tới chữ đầu lấy từ ba lượt tối 21/11 (153 lượt trả lời xong); lịch sử làm nhanh đo với gpt-6-luna từ 01/11 tới 10/11; cơ chế đọc từ chương trình trưa 22/11. Người viết không chạy lại phép đo nào; bài đã qua một lượt đối chiếu độc lập và sửa theo đó.*

**Bài trước đã biết:** ở ví dụ chính, gần như toàn bộ 3,7 giây là model viết (bài 6); Claude viết dài hơn gpt-6-luna khoảng ba lần, chữ tới một lần, giá mỗi token gấp 20 lần (bài 33).
**Bài này thêm:** thời gian chờ của một lượt đi vào những phần nào và phần nào đáng cắt; các lần làm nhanh đã có; một câu tốn bao nhiêu tiền và tiền được ghi ở đâu; trang theo dõi; và bộ nhớ câu trả lời 24 giờ, thứ duy nhất làm một câu vừa nhanh vừa không tốn tiền.

## Ý chính

- **Lượt hỏi đáp đứng giữa chờ khoảng 13 giây** với Claude ở mức cao (49 lượt, 21/11). **Lần viết cuối chiếm 9,7 giây, tức 72 %**; các vòng công cụ 3,1 giây (25 %), khoảng 2,2 giây một vòng; phần của chương trình 3 %. Xếp loại câu chạy song song, không cộng thêm.
- **Lượt chậm là lượt có câu trả lời dài**, không phải lượt gọi nhiều công cụ: 15 trên 16 lượt quá 15 giây có phần lớn thời gian nằm ở lần viết cuối.
- **Tin dài nhiều ý chờ 25–34 giây** từ 14:47 ngày 22/11 (trước khoảng 20 giây), đổi lấy hết màn hình "Thử lại" và đủ ý hơn (bài 21, 23); lượt phải viết lại một lần lâu thêm khoảng 10 giây. Số đo trên một tin 4 ý, 6 lần hỏi.
- **Hạ mức suy luận chỉ mua khoảng 0,3 giây.** Hai cách lợi lớn (chữ chạy dần, câu trả lời ngắn hơn) đều là thứ chủ dự án đã quyết, nên nhóm không mở.
- **Tiền theo model:** ví dụ chính 0,018 USD trên Claude; câu một dữ kiện khoảng 0,0004 USD trên gpt-6-luna. Mỗi lượt một dòng số trong sổ số đo.
- **Bộ nhớ câu trả lời 24 giờ:** người sau gõ đúng câu người trước đã hỏi, ở lượt đầu một cuộc mới, thì nhận lại câu trả lời cũ trong khoảng 0,1 giây, không gọi model. Khớp đúng chữ, không khớp theo nghĩa.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| chờ tới chữ đầu | **time to first text** | từ lúc bấm gửi tới lúc chữ đầu tiên của câu trả lời hiện ra |
| lần viết cuối | **final generation call** | lời gọi model viết ra câu trả lời người dùng đọc |
| vòng công cụ | **tool round** | một lời gọi model chỉ để xin tìm thêm hay xin một công cụ, chưa viết câu trả lời (bài 21) |
| trung vị | **median**, **p50** | số đứng giữa khi xếp các lượt từ nhanh tới chậm; một nửa nhanh hơn, một nửa chậm hơn |
| bộ nhớ câu trả lời | **answer cache** | chỗ máy chủ giữ câu trả lời đã viết để trả lại cho người sau hỏi đúng câu đó |
| trang theo dõi | **monitoring page** | trang riêng của chủ dự án, bảng số lượt, kết cục, thời gian, tiền theo ngày |

## Thời gian chờ đi vào lần viết cuối

Số dưới đây tách từng lời gọi model của 49 lượt hỏi đáp thường (bỏ lượt lập và sửa lịch), lượt người dùng mô phỏng chạy một mình trưa 21/11.

| Phần của một lượt (trung vị) | Claude Sonnet 5.5, mức cao | gpt-6-luna |
|---|---|---|
| cả lượt | **13,0 giây** | 10,1 giây |
| lần viết cuối | **9,7 giây — 72 %** | 4,2 giây — 51 % |
| các vòng công cụ | 3,1 giây — 25 % (2 vòng, 2,2 giây một vòng) | 4,3 giây — 46 % (2 vòng, 2,0 giây một vòng) |
| tìm kho và công cụ của chương trình | 0,7 giây — 3 % | 0,2 giây — 3 % |
| xếp loại câu | 0,5 giây, chạy song song, không cộng | 1,5 giây, chạy song song, không cộng |
| token viết ra ở lần viết cuối · tốc độ | 1.075 (204 để suy luận) · 114 token mỗi giây | 449 (211 để suy luận) · 101 token mỗi giây |

Đọc bảng:

- **Claude không sinh chữ chậm hơn**; nó viết nhiều chữ hơn. Phần chữ người dùng đọc khoảng 870 token so với khoảng 240 (3,6 lần).
- **Lượt chậm là lượt viết dài.** Ở 16 lượt quá 15 giây, lần viết cuối là phần lớn nhất ở 15 lượt, ra trung vị 1.562 token. Số vòng công cụ của lượt chậm vẫn là 2. Vì vậy đếm "lượt có tìm thêm thì chậm hơn bao nhiêu" là đọc sai: lượt tìm nhiều cũng thường là lượt trả lời dài.
- **Phần của chương trình không có gì để cắt**: tìm kho, công cụ, xếp loại cộng lại chưa tới 1,5 giây.

**Chờ tới chữ đầu.** Với Claude, chữ tới một lần khi model viết xong (bài 33), nên chờ tới chữ đầu gần bằng thời gian tới lúc câu trả lời xong. Trên 153 lượt trả lời xong của ba lượt tối 21/11: trung vị khoảng 13,0 giây, 56 lượt quá 15 giây; riêng lượt hỏi đáp thường, bỏ 11 lượt sửa lịch (142 lượt): khoảng 13,5 giây. Điều kiện: hai model chạy cùng lúc trên một máy, mỗi lượt dài thêm khoảng 2,5 tới 4,5 giây so với chạy một mình. Tối hôm đó mục "Từ web" còn chạy thêm sau câu trả lời ở 67 trên 153 lượt; từ 22:20 21/11 tin nhiều ý đã trả lời được một phần không còn mục đó.

## Các lần làm nhanh đã giữ đều là bớt một chỗ phải đợi

Với gpt-6-luna (01/11–10/11), ba lần làm nhanh được giữ: chữ hiện dần, chạy xếp loại câu song song với việc tìm và viết (sớm hơn 1,37 giây ở trung vị), và chương trình tính sẵn ngày cho câu có ngày (bảng ở nửa để tra). Với Claude, chữ hiện dần không còn tác dụng vì chữ tới một lần. Lần làm nhanh lớn nhất với Claude là **bỏ mục "Từ web" ở tin nhiều ý đã trả lời được một phần** (bật 22:20 21/11, sau một lượt thật 11 tin): mục web chỉ còn mở khi cả câu bị từ chối; 11 trên 11 tin nhanh hơn, trung vị nhanh hơn 5,8 giây, bớt một lời gọi model mỗi lượt.

## Một câu tốn bao nhiêu, và tiền được ghi ở đâu

Tiền một lần gọi = token vào nhân giá vào, cộng token viết ra (kể cả suy luận) nhân giá ra, theo bảng giá của đúng hãng đã gọi (bài 33); chương trình cộng cả lượt.

| Lượt | Model | Tiền |
|---|---|---|
| ví dụ chính (2 lần gọi) | Claude, mức cao | 0,0178 USD |
| câu một dữ kiện, trung bình 66 câu | Claude, mức cao · gpt-6-luna | 0,0146 USD · 0,00039 USD |
| lượt của người dùng mô phỏng (phần lớn tin hai ý), 156 lượt, tối 21/11 | Claude, mức cao | khoảng 0,057 USD một lượt |
| lượt trúng bộ nhớ câu trả lời | — | 0 USD |

**Sổ số đo, mỗi lượt một dòng.** Sau mỗi lượt, máy chủ ghi một dòng số: kết cục, tuyến, model, token, tiền, từng lần gọi model, công cụ, thời gian từng bước, có trúng bộ nhớ không, mã bản chương trình. Không có chữ câu hỏi hay câu trả lời (bài 37). Sổ dùng chung cho mọi bản đã chạy và cho bộ test, nên khi đếm phải chọn đúng các dòng của bản chương trình đang hỏi (mỗi dòng có ghi mã bản).

**Trang theo dõi** chỉ dành cho chủ dự án: một địa chỉ không có trong menu, mở bằng một khoá đặt lúc bật máy chủ. Nó cộng sổ số đo theo ngày, tối đa 14 ngày: số lượt theo kết cục, tiền, thời gian chờ. Không có dòng của từng lượt.

## Bộ nhớ câu trả lời: trả lại câu đã viết, khi gõ đúng chữ

Một người hỏi một câu về Huế và được trả lời từ kho. Trong 24 giờ sau, người sau (kể cả chính người đó ở một cuộc mới) gõ **đúng câu đó** làm câu đầu tiên của một cuộc mới thì máy chủ trả lại câu trả lời đã lưu: cùng chữ, cùng nguồn, cùng dòng ghi chú, không tìm kho, không gọi model. Lần thử thật 20/11 trên trình duyệt (gpt-6-luna): lượt đầu 7,5 giây, lượt trúng 0,11 giây.

- **"Đúng câu"** nghĩa là giống từng chữ, chỉ bỏ qua chữ hoa thường và khoảng trắng thừa. Khác một dấu thanh, thiếu dấu "?" là không trúng.
- **Chỉ lượt đầu của một cuộc.** Câu thứ hai trở đi mang nghĩa phụ thuộc câu trước. Lượt bấm nút, gửi biểu mẫu hay chọn thẻ cũng không tra và không lưu.
- **Chỉ lưu lượt trả lời thuần từ kho.** Không lưu: câu từ chối, lượt có mục web, lượt dùng thời tiết, ngày, khoảng cách, lịch (đổi theo giờ hay theo người), lượt có câu cảnh báo an toàn, lượt bị chương trình gỡ câu, hỏi bằng ảnh, lượt lỗi, và tin nhiều ý mà câu trả lời còn dòng "Tư liệu chưa có thông tin về…".
- **Nhiều nhất 500 câu**, đầy thì bỏ câu lưu sớm nhất; nằm trong bộ nhớ máy chủ, khởi động lại là mất. Kho, lời dặn, model, tính năng hay bản chương trình đổi thì bản cũ không còn trúng (các thứ đó chỉ đổi khi khởi động lại, mà lúc đó bộ nhớ cũng mất).

Vì việc trả lại không cần model hay Qdrant, nó chạy cả khi hai khối đó hỏng. Đã thử 22/11: Qdrant ngừng, câu mới nhận lời báo lỗi, câu đã nhớ vẫn được trả lại (bài 6).

## Quyết định và lý do

### 1. Vì sao không cắt thêm thời gian chờ, khi lượt đứng giữa vẫn 13 giây?

- **Đã chọn:** không mở thêm hướng làm nhanh nào cho Claude lúc này.
- **Vì sao:** hai hướng lợi lớn đều là thứ chủ dự án đã quyết. Chữ chạy dần cần thêm quyền cho bộ khoá Bedrock, và khi đổi tạm chủ dự án ghi "không cần stream thật" (ước: chờ tới chữ đầu còn khoảng 5,5 tới 6 giây). Câu trả lời ngắn hơn: chủ dự án đã chọn nhận độ dài (ước: bớt một phần ba chữ được khoảng 2,5 giây). Hạ mức suy luận chỉ mua khoảng 0,3 giây trên 66 câu, một lượt.
- **Cách khác:** cho công cụ tìm kho nhận hai ba câu tìm trong một lần gọi, bớt một vòng khoảng 2,2 giây ở lượt model tìm thêm hai lần (64 trên 153 lượt): chưa thử; phép đếm trưa 22/11 cho thấy tin ngắn gần như không còn vòng tìm thêm để bớt, tin dài lợi dưới 10 %, nên ý này đã hạ xuống hàng thấp. Bớt số lần tìm: không làm, vì 47 trên 49 lượt tìm thêm một lần và 55 trên 61 lượt tìm thêm hai lần có trích đúng đoạn của lần tìm thêm đó.
- **Cái giá:** người dùng nhìn dòng "Đã tìm trong kho, đang chuẩn bị câu trả lời… (10 đoạn)" khoảng 10 giây ở lượt đứng giữa (ở lượt có công cụ, "Đang viết câu trả lời…" chỉ được gửi ngay trước chữ đầu, nên với Claude gần như không thấy); khi chạy một mình, một phần ba số lượt quá 15 giây.

### 2. Vì sao xếp loại câu chạy song song với việc tìm và viết?

- **Đã chọn:** câu về Huế được tìm và viết ngay, cùng lúc với bước xếp loại; chữ được giữ lại cho tới khi biết tuyến.
- **Vì sao:** đã đo ngày 04/11 (gpt-6-luna, 20 cặp): chữ đầu sớm hơn 1,37 giây ở trung vị, 90 lượt an toàn không lỗi; chủ dự án duyệt bật.
- **Cách khác:** chạy lần lượt, xếp loại xong mới tìm: là bản trước đó, chậm hơn. Chạy song song cả câu chào hỏi: đã đo, bỏ.
- **Cái giá:** câu không về Huế cũng đã được gửi kèm đoạn kho tới model trước khi biết tuyến. Với Claude, số 1,37 giây chưa đo lại.

### 3. Vì sao bộ nhớ câu trả lời chỉ khớp đúng chữ, không khớp theo nghĩa?

- **Đã chọn:** so từng chữ sau khi bỏ chữ hoa thường và khoảng trắng thừa.
- **Vì sao:** nghiên cứu ngày 05/11: khớp theo nghĩa trả nhầm khoảng 8 % số lần trúng, ví dụ câu của "lăng A" trả cho người hỏi "lăng B". Đó là lỗi nói chắc mà sai.
- **Cách khác:** khớp theo nghĩa bằng vector của câu hỏi: đã nghiên cứu, không làm.
- **Cái giá:** tỉ lệ trúng ngoài đời có thể thấp; chưa có số vì chưa có người dùng thật. Sổ số đo ghi mỗi lượt trúng hay trượt để sau này đếm.

### 4. Vì sao chỉ nhớ lượt đầu của một cuộc mới, chỉ lượt trả lời từ kho, trong 24 giờ?

- **Đã chọn:** chỉ tra và chỉ lưu ở lượt đầu; chỉ lượt mà mọi công cụ đã chạy đều là tìm kho; 24 giờ; 500 câu.
- **Vì sao:** chủ dự án yêu cầu ngày 20/11: người khác hỏi lại câu đó ít phút sau thì phải lấy được câu trả lời cũ. Lượt đầu: câu sau phụ thuộc câu trước. Chỉ lượt từ kho: thời tiết, ngày, khoảng cách, lịch đổi theo giờ hay theo người (lý do ghi trong chương trình). Con số 24 giờ và 500 câu: chưa thấy ghi lý do. Điều thấy được: kế hoạch đặt hai số đó từ đầu.
- **Cách khác:** ghi bộ nhớ ra đĩa để sống qua lần khởi động lại: không làm.
- **Cái giá:** câu trả lời đầu tiên mà kém thì mọi người gõ đúng câu đó nhận lại bản kém ấy trong 24 giờ, tới khi khởi động lại máy chủ. Qua tốc độ trả lời, người ngoài đoán được "câu này đã có người hỏi" (mức thấp, câu du lịch chung).

## Nếu… thì sao

Một tình huống kể trọn. Lúc 9 giờ, người thứ nhất hỏi giá vé Đại Nội; Claude viết khoảng 4 giây, tốn 0,018 USD; câu được lưu. Lúc 9 giờ 20, người thứ hai gõ đúng câu đó: câu trả lời hiện gần như ngay, 0 USD. Người thứ ba gõ thiếu dấu "?": không trúng, chờ như thường. Trưa đó có người sửa giá trong kho rồi khởi động lại máy chủ: mọi câu đã lưu mất.

Lời báo là nguyên văn; các dòng đọc từ chương trình, trừ dòng có chữ **(đã thử)**.

| Nếu | Người dùng thấy gì | Đã có chưa / ai làm gì |
|---|---|---|
| tin dài nhiều ý (ba bốn việc trong một tin) **(đã thử, một tin, 6 lần)** | chờ khoảng 25–34 giây; lượt phải viết lại một lần tới 25–37 giây; dòng tiến độ đứng lâu | đúng thiết kế từ 14:47 22/11: đổi thời gian lấy câu trả lời đủ ý (bài 21) |
| câu trả lời rất dài | chờ lâu hơn, chữ tới một lần; quá 45 giây thì "Không thể tạo câu trả lời vào lúc này." | lượt chạy một mình lâu nhất 28 giây; trong ba lượt tối 21/11 (hai model chạy cùng lúc) có 1 lượt chạm 45 giây |
| Qdrant ngừng, câu đã nhớ **(đã thử)** | câu đã nhớ vẫn được trả lại; câu mới nhận "Hệ thống tra cứu tạm thời không khả dụng." | bật lại Qdrant (bài 6) |
| câu trả lời đầu tiên kém mà được nhớ | người sau gõ đúng câu nhận lại bản kém trong 24 giờ | khởi động lại máy chủ, hoặc tắt tính năng bộ nhớ câu trả lời |
| nhiều người hỏi cùng lúc | mỗi lượt gọi model riêng; chưa có giới hạn số lượt chạy cùng lúc | chưa đo với Claude; mới đo một lần (27/10) |

## Dễ nhầm

- **"Mỗi vòng tìm thêm làm chậm khoảng 5 giây."** Sai cách đọc. Một vòng công cụ khoảng 2,2 giây; lượt tìm nhiều trông chậm hơn hẳn vì nó thường cũng là lượt trả lời dài.
- **"Bộ nhớ câu trả lời hiểu câu gần giống."** Không. Khác một chữ là không trúng, cố ý.

## Câu hỏi tự kiểm

<details>
<summary>1. Thời gian chờ của lượt đứng giữa nằm chủ yếu ở đâu?</summary>

Lần viết cuối: 9,7 trên khoảng 13 giây (72 %); các vòng công cụ 25 %; phần của chương trình 3 %.

</details>

<details>
<summary>2. Vì sao không hạ mức suy luận cho nhanh?</summary>

Chỉ mua khoảng 0,3 giây ở câu thường; thời gian chủ yếu là số chữ viết ra.

</details>

<details>
<summary>3. Khi nào một câu được trả lại từ bộ nhớ, khi nào không?</summary>

Gõ đúng chữ, ở lượt đầu một cuộc mới, trong 24 giờ, câu gốc là lượt trả lời thuần từ kho. Không: khác một chữ, câu thứ hai của cuộc, lượt có thời tiết, ngày, lịch, web, câu an toàn.

</details>

<details>
<summary>4. Trang theo dõi lấy số từ đâu, và vì sao không lộ gì của người dùng?</summary>

Từ sổ số đo, mỗi lượt một dòng số không có chữ. Trang chỉ trả tổng theo ngày, cần khoá mới mở được.

</details>

## Cấu hình đang chạy

| Mục | Giá trị | Dùng để làm gì, vì sao | Đã thử giá trị khác chưa |
|---|---|---|---|
| `song_song_tra_loi` | bật | quyết định 2 | đã so với chạy lần lượt (gpt-6-luna) |
| `cache_cau_tra_loi` | bật (từ 20/11) | bộ nhớ câu trả lời | — |
| Bộ nhớ câu trả lời: hạn · trần | 24 giờ · 500 câu | quyết định 4 | — |
| `timeout_seconds` | 45 giây cho cả phần viết của một lượt | bài 6 | — |
| `bedrock.reasoning_default` | cao | bài 33 | bốn mức trên 66 câu |
| Sổ số đo | 10 MB mỗi file, giữ 3 file cũ | — | — |
| Trang theo dõi | 14 ngày; mở bằng `HUE_KHOA_THEO_DOI` | quyết định 5 | — |

## Đã so

**Hướng làm nhanh với Claude, ước từ số đã tách** (chưa đo hướng nào; bảng tính trưa 21/11):

| Hướng | Lượt đứng giữa | Lượt quá 15 giây | Ai quyết |
|---|---|---|---|
| chữ chạy dần thật | cả lượt không đổi; chờ tới chữ đầu 13 ⇒ khoảng 5,5–6 giây | khoảng 19 ⇒ 9 giây | cần quyền Bedrock; chủ dự án |
| hạ mức suy luận, riêng lần viết cuối | tối đa 1,8 giây (đo thật trên 66 câu một lượt: khoảng 0,3 giây) | tối đa 3,8 giây | nhóm; đã đo một phần |
| hạ mức suy luận, riêng các vòng công cụ | tối đa 1,1 giây | tối đa 1,6 giây | nhóm |
| hạ mức suy luận, riêng xếp loại câu | 0 (vốn không suy luận, chạy song song) | 0 | — |
| bớt một vòng công cụ | khoảng 2,2 giây | khoảng 2,4 giây | nhóm; chưa thử |
| câu trả lời ngắn hơn | mỗi 100 token bớt khoảng 0,9 giây; bớt một phần ba ≈ 2,5 giây | khoảng 3,3 giây | chủ dự án đã chọn nhận độ dài |

Giới hạn của các số: 49 lượt do model đóng vai du khách gõ, phần lớn tin hai ý nên câu trả lời dài hơn câu một ý; đo trên bản chương trình trưa 21/11.

## Quyết định nhỏ hơn

**Vì sao số đo nằm trong một file sổ, mà không có cơ sở dữ liệu?**

- **Đã chọn:** mỗi lượt một dòng số trong file sổ của máy chủ; trang theo dõi đọc lại file đó mỗi lần xem.
- **Vì sao:** kế hoạch trang theo dõi ghi: dựng từ các dòng đã có, không thêm gì vào sổ, không cơ sở dữ liệu, không model. Điều thấy được: một máy chủ, một người xem.
- **Cách khác:** một cơ sở dữ liệu số đo: không làm.
- **Cái giá:** mỗi lần bấm "Xem", máy chủ đọc lại tới khoảng 40 MB sổ. Trên máy phát triển, sổ lẫn lượt thử của nhóm; lưu lượng lớn thì sổ xoay vòng nhanh, không còn đủ 14 ngày.

**Vì sao hạn 45 giây cho cả phần viết của một lượt?** Chưa thấy ghi lý do (bài 6). Điều thấy được: hạn đã chạm một lần trong 156 lượt người dùng mô phỏng của Claude tối 21/11, lúc hai model chạy cùng lúc.

## Giới hạn đã biết

- **Lượt đứng giữa khoảng 13 giây, một phần ba số lượt quá 15 giây**, chữ tới một lần.
- **Tin dài nhiều ý 25–34 giây** (từ 14:47 22/11): mới đo trên một tin, 6 lần; chưa đo ở cuộc đã có lịch lưu, chưa đo trên model cũ. Lần viết lại và lần chạy lại mỗi lần có hạn 45 giây riêng, nên một lượt có thể chờ quá 45 giây.
- **Số chờ tới chữ đầu (khoảng 13,0 giây trên 153 lượt; 13,5 giây trên 142 lượt hỏi đáp thường) đo khi hai model chạy cùng lúc trên một máy**, nên dài hơn chạy một mình khoảng 2,5 tới 4,5 giây; lúc đó tin nhiều ý còn mục "Từ web".
- **Chưa đo lại với Claude** lợi của chạy song song và của chương trình tính sẵn ngày.
- **Bộ nhớ câu trả lời** chỉ nằm trong bộ nhớ của đúng một máy chủ đang chạy (chạy hai máy chủ thì mỗi cái nhớ riêng); trúng thì không hiện dòng tiến độ; tỉ lệ trúng ngoài đời chưa có số.
- **Tiền ghi sổ của Claude chưa đối chiếu hoá đơn** (bài 33).
- **Trang theo dõi trên máy phát triển lẫn lượt thử của nhóm.**

## Chi tiết để tra

- Số đo mới nhất, lúc máy không chạy việc khác: ở lượt kiểm chốt trưa 22/11, 41 tin gõ qua trình duyệt (phần lớn là tin ngắn) có thời gian cả câu ở lượt đứng giữa là 6,9 giây, 95 % số lượt dưới 13,1 giây, không lượt nào ra màn hình lỗi. Con số này thấp hơn số 13,0 giây ở trên vì hai lý do: máy rảnh, và tin ngắn hơn.
- **Số vòng tìm thêm đi theo số ý của tin**, đếm trên hai lượt thật trưa 22/11 (Claude, sau khi mở tính năng tìm theo từng ý): tin một ý 10 trên 10 lượt không cần vòng tìm thêm nào, 1,8 tới 3,5 giây; tin hai ý ngắn 13 trên 20 lượt không cần; tin bốn ý dài 17 trên 17 lượt dùng hết 2 lần tìm thêm (lúc đó trần là 2), trung vị 21,7 giây. Tin dài nhiều ý vừa tìm nhiều vừa viết dài; hai thứ đi cùng nhau. Từ 14:47 22/11 trần là 3, mở cùng hai thay đổi ở khâu tìm và bước viết lại: tin 4 ý của một gia đình (6 lần) chờ 25–34 giây, lần tìm thứ ba thêm khoảng 2 giây, lượt có viết lại thêm khoảng 10 giây; ngữ cảnh dựng theo cách xấu nhất tới khoảng 70 đoạn, đo được trung vị 16 nguồn.
- Trang theo dõi: khoá ít nhất 16 ký tự; cột: số lượt, trả lời từ kho, từ chối, ngoài phạm vi, có mục web, lịch, trúng bộ nhớ, người dùng ngắt, lỗi, tiền, thời gian chờ trung vị và lượt chậm, bản chương trình; sai khoá năm lần liền thì địa chỉ đó bị khoá 15 phút (bài 37).
- Tiền "khoảng 0,057 USD một lượt" của người dùng mô phỏng tối 21/11 gồm cả lời gọi viết mục web ở 67 lượt; bản đang chạy không còn lời gọi đó ở tin nhiều ý.
- Bảng ba lần làm nhanh với gpt-6-luna:

| Lúc | Đổi gì | Kết quả đo | Giữ hay bỏ |
|---|---|---|---|
| 01/11 | **chữ hiện dần**: gửi từng mẩu chữ ngay khi model viết | chữ đầu tới sau 1,23 giây ở câu đứng giữa (38 câu, trình duyệt), sớm hơn chờ cả câu 0,44 giây | giữ (chủ dự án chọn) |
| 04–05/11 | **chạy song song** việc tìm và viết của câu về Huế với bước xếp loại câu | chữ đầu sớm hơn 1,37 giây ở trung vị (20 cặp; nếu đo lại nhiều lần, mức sớm hơn gần như chắc nằm giữa 0,34 và 2,14 giây) | giữ |
| 10/11 | **chương trình tính sẵn ngày** cho câu có ngày, khỏi một vòng công cụ (bài 24) | 19 câu: trung vị 5,60 xuống 2,35 giây | giữ |


- Hai lần làm nhanh bị bỏ (gpt-6-luna): tắt phần suy luận ở bước xếp loại câu (04/11: nhanh hơn 0,2 tới 0,35 giây, nhưng 2 câu an toàn về Huế bị xếp "ngoài phạm vi") · chạy song song cả câu chào hỏi (10/11: trung vị 3,46 xuống 1,85 giây, nhưng câu chậm vẫn 5,7 giây).

- Ví dụ chính (21/11, Claude): xếp loại 0,74 giây song song, tìm 0,04, ghép 0,004, viết 3,63, tổng 3,69 giây; 0,0034 USD lần xếp loại, 0,0144 USD lần viết (bài 6).
- Lượt người dùng mô phỏng chạy một mình: cả lượt 90 % số lượt dưới 20,8 giây, lâu nhất 28,0 giây (Claude); 21,1 và 37,0 giây (gpt-6-luna). Lượt quá 15 giây: 16 trên 49 (33 %) và 11 trên 43 (26 %). Với gpt-6-luna, 4 trên 11 lượt chậm là do vòng công cụ (chạm trần vòng).
- Tiền ba lượt người dùng mô phỏng tối 21/11, phía sản phẩm: Claude 11,18 USD (gồm cả 4 vai để riêng), gpt-6-luna 0,39 USD.
- Lượt trúng bộ nhớ: phía máy chủ khoảng 1 phần nghìn giây. Trên gpt-6-luna mỗi lần trúng tiết kiệm khoảng 0,0008 USD; trên Claude, cỡ một câu có nguồn [ước của người viết] (khoảng 0,015 USD).
- Câu một dữ kiện trên Claude: cả câu trung vị 2,6 giây không qua giao diện (66 câu, mức cao); qua giao diện có thêm dòng trạng thái và lượt có lịch sử dài hơn.
- Lượt người dùng bấm "Dừng": tiền ghi sổ là cận dưới, vì không có số token cuối.
- Tiền mỗi lần gọi tính theo hãng của đúng lần gọi đó, nên bộ đo có thể chạy hai model trong một tiến trình mà tiền không lẫn.

**Bài sau (bài 35):** trang web và máy chủ gửi cho nhau những gì.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Bảng thời gian đi đâu, 72 %, 25 %, 2,2 giây một vòng, lượt chậm = lượt dài (15/16, 1.562 token), các hướng và ước: `data/thu_bedrock_2026-11-21/b_toc_do/THOI_GIAN_DI_DAU.md` mục 1–3 [riêng tư; máy đếm, phiên làm việc đo 21/11, người viết không chạy lại].
- Chờ tới chữ đầu: đếm lại trên `do/moc_12vai/r1–r3/luot_s_high.jsonl` (trường `so_do`, 22/11): 153 lượt `success` ⇒ trung vị 12,95 giây, 56 lượt > 15 giây; bỏ 11 lượt có `sua_lich` ⇒ 142 lượt, 13,47 giây, 55 lượt [đã chạy, đếm thô; người kiểm độc lập ra cùng số]; 67/153 lượt có `tra_web`, `web_chi_khi_tu_choi` bật 22:20 21/11 (`settings.yaml`, nhanh hơn 5,8 giây trên 11 tin) [code]. Các số khác: 64/153 tìm thêm hai lần, 47/49 và 55/61: `session_prompt/Y_CHUA_THU.md` dòng 42 [chép]; file thô `data/thu_bedrock_2026-11-21/do/moc_12vai/r1–r3/luot_s_high.jsonl` [riêng tư]. Người viết đếm thô lại trên ba file đó (trường `so_do.first_text_ms`): 155 lượt có mốc chữ đầu, trung vị 12,9 giây, 56 lượt > 15 giây — chênh với 13,5 do cách lọc lượt, chưa tra cách lọc gốc. Hai model chạy song song: `do/moc_12vai/KET_QUA_MOC.md` dòng 2; thêm 2,5–4,5 giây: `THOI_GIAN_DI_DAU.md` mục 2.
- Số vòng tìm thêm theo số ý (10/10 · 13/20 · 17/17, 1,8–3,5 giây, 21,7 giây): phiên đo đếm trưa 22/11, hai lượt thật, tin của phiên điều phối gửi phiên D [chép từ tin, chưa tự mở file thô].
- Đính chính "mỗi vòng tìm thêm 5 giây" là đọc sai: tin của phiên điều phối 12:20 22/11, `data/hoc_cung_D/BAN_VOI_A_VA_D_BEN_KIA.md` [riêng tư].
- 0,3 giây trên 66 câu: `data/thu_bedrock_2026-11-21/do/bac_2a/KET_QUA_2A.md` ("high chậm hơn low / medium 0,3 s ở p50") [riêng tư].
- Ba lần làm nhanh và hai lần bỏ: `bai_hoc/17_GIAO_DIEN_VA_TOC_DO.md` phần 3 và nguồn của bài đó (`report_agent/2026-10-31_streaming_spec/s4_do_d2_implementation.md`, `report_agent/2026-11-02_phase_9_code/c172_toc_do_song_song.md`, `e_t1_nhanh_implementation.md`) [chép].
- Tiền: ví dụ chính `data/hoc_cung_D/vi_du_di_suot_vet.json` (qua bài 6); 66 câu `KET_QUA_2A.md`; 156 lượt ba lượt mốc: `KET_QUA_MOC.md` (2,83 + 3,06 + 2,96 USD cho 52 lượt mỗi lượt; chia là của người viết) [riêng tư]; cách tính `backend/llm/pricing.py`, `generator_openai_full_corpus.py` (`call_entry`) [code].
- Sổ số đo: `backend/api/routes/chat.py` (`METRIC_FIELDS` và chú thích) [code]; 10 MB × 3: `backend/config/logging.yaml` [code]; lọc theo bản: `guides/RUNBOOK_BAN_GIAO.md` mục 7.
- Trang theo dõi: `backend/api/theo_doi.py` (khoá ≥ 16 ký tự, 14 ngày, cột, bỏ model giả, 5 lần sai ⇒ 15 phút) [code]; 40 MB, lẫn lượt thử, không có dòng từng lượt: `bai_hoc/VIEC_MOI_XONG.md` mục 33 [chép]; không cơ sở dữ liệu: chú thích đầu `theo_doi.py` [code].
- Bộ nhớ câu trả lời: `backend/api/cache_tra_loi.py` (`SONG_GIAY`, `TRAN_SO_MUC`, `chuan_hoa`, `luot_luu_duoc`), `backend/api/app.py` (dấu phiên bản và chú thích về ghi ra đĩa) [code]; 7,5 ⇒ 0,11 giây, 8 % khớp theo nghĩa, 0,0008 USD, đoán qua tốc độ: `bai_hoc/VIEC_MOI_XONG.md` mục 21 [chép, đã chạy 20/11]; yêu cầu chủ dự án 20/11: cùng chỗ; 24 giờ / 500 không có lý do: `report_agent/2026-11-20/b_cache_cau_tra_loi_plan.md` dòng 3, 8 [đã đọc]; Qdrant ngừng vẫn trả câu đã nhớ: bài 6 [đã chạy 22/11].
- Quyết định 1: "không cần stream thật" `session_prompt/HIEN_TRANG.md` mục 4 gạch 09:41 21/11; chủ dự án nhận độ dài: `THOI_GIAN_DI_DAU.md` hàng E ("11:24 21/11") [chép].
- Quyết định 2: `bai_hoc/17_GIAO_DIEN_VA_TOC_DO.md`; `settings.yaml` (`song_song_tra_loi`, chú thích "User duyệt 05/11") [code]; câu không về Huế vẫn gửi đoạn kho: bài cũ `bai_hoc/21_DU_LIEU_NGUOI_DUNG_VA_BAO_MAT.md` bảng dữ liệu [chép].
- Tình huống 9 giờ sáng: [suy từ code, chưa thử thật]; lâu nhất 28 giây khi chạy một mình: `THOI_GIAN_DI_DAU.md` mục 1; 1 lượt chạm 45 giây: `KET_QUA_MOC.md` bảng r1 [riêng tư]. Nhiều người cùng lúc: bài 6.

- Bài đã qua một lượt đối chiếu độc lập 22/11: `data/hoc_cung_D/kiem/bai_33_38.md` [riêng tư]; dòng không áp ở `data/hoc_cung_D/viet/viet_33_38.md` mục "Sau lượt kiểm".

- Kết quả lượt kiểm chốt buổi trưa 22/11 (phiên điều phối báo, phiên đo chạy; người viết chép từ tin, chưa tự mở file kết quả) [đã chạy].

- Cập nhật theo bộ thay đổi mở 14:47 22/11/2026: `bai_hoc/VIEC_MOI_XONG.md` mục 42 (ý 1 "từ khoảng 20 giây lên 25–34 giây", ý 3 "lượt có viết lại lâu hơn khoảng 10 giây"), 43; `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 hàng "Tin DÀI nhiều ý" (25–34 giây, 25–37 giây khi viết lại, khoảng 70 đoạn xấu nhất, trung vị 16 nguồn); `backend/config/settings.yaml` [đã chạy, phiên đo; người viết không chạy lại]. Hạn 45 giây riêng của lần viết lại / chạy lại: `backend/llm/assistant.py` `_viet_lai_het_luot` (gọi `generate_answer` ⇒ `_execute_agent` với `self.timeout`), `answer_turn_stream_parallel` [code].

</details>
