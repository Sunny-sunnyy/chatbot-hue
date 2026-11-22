# Bài 33 — Model viết, mức suy luận, và đổi model bằng một dòng cấu hình

*Cập nhật 15:13, ngày 22/11/2026 · cơ chế đọc từ chương trình và cấu hình trưa 22/11; số đo lấy từ các báo cáo đo ngày 19/11 (gpt-6-luna) và 21/11 (cả hai model), ghi rõ model ở từng dòng; người viết không chạy lại phép đo nào; đã qua một lượt đối chiếu độc lập và sửa theo đó.*

**Bài trước đã biết:** một câu hỏi đi qua sáu bước, gần như toàn bộ thời gian chờ là model viết (bài 6); model viết được gọi nhiều lần trong một lượt: xếp loại câu, tìm thêm, viết (bài 21, 22).
**Bài này thêm:** hai model đã dùng khác nhau ở đâu, mức suy luận là gì và vì sao để mức cao, vì sao đổi model chỉ sửa một dòng mà vẫn phải viết một lớp nối và đo lại.

## Ý chính

- **Một model viết làm mọi việc có model** (xếp loại câu, trả lời, mục web, câu thẻ lịch, hiểu lệnh sửa lịch, nhận ảnh…; hồ sơ đếm là chín loại lời gọi). Đổi model là đổi tất cả cùng lúc.
- **Hai model đã chạy.** gpt-6-luna của OpenAI tới trưa 21/11; từ 21/11 là Claude Sonnet 5.5 qua Amazon Bedrock, **đổi tạm**. Đường quay về gpt-6-luna vẫn là một dòng cấu hình, nhưng tài khoản OpenAI đang ngừng dùng vì hết tiền.
- Claude **viết dài hơn khoảng ba lần**, **đắt hơn 20 lần mỗi token**, và **chữ tới một lần** khi viết xong thay vì chạy dần. Chất lượng: đúng ngang, đủ ý nhỉnh hơn, gọn kém hơn.
- **Mức suy luận để cao.** Ở câu hỏi một lượt, bốn mức ngang nhau và mức cao chỉ chậm hơn khoảng 0,3 giây; ở lệnh sửa lịch khó và lượt có công cụ, mức thấp hỏng rõ.
- **Đổi model không chỉ là đổi tên.** Thư viện gọi model giữ nguyên; Claude đi qua một lớp nối tự viết. Lỗi lớn nhất nằm ở chỗ nối: Claude xin công cụ mãi không viết (0 trên 8 lần ở mỗi mức, bốn mức); sửa xong, câu chạm trần vòng từ 6 xuống 0 trên 29.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| model viết | **generator**, **LLM** | model ngôn ngữ lớn sinh mọi chữ của trợ lý; hệ thống thuê qua mạng, không chạy trên máy |
| nền tảng cho thuê model | **Amazon Bedrock** | dịch vụ của Amazon cho gọi model của nhiều hãng, trong đó có Claude của Anthropic; trả tiền cho Amazon |
| thư viện gọi model | **OpenAI Agents SDK** | đoạn chương trình có sẵn do OpenAI viết, lo việc gọi model, nhận lời xin công cụ, chạy công cụ rồi gọi lại, ép đầu ra đúng khuôn |
| lớp nối | **adapter** | phần chương trình dự án tự viết, đứng giữa thư viện và Claude, đổi cách gọi của bên này sang cách gọi của bên kia ở cả hai chiều |
| mức suy luận | **reasoning effort** | model được "nghĩ thầm" bao nhiêu trước khi viết; bốn nấc: không, thấp, vừa, cao. Người dùng không thấy phần nghĩ thầm, nhưng nó tính tiền như chữ viết ra và tốn giây |
| trần token viết ra | **max output tokens** | số token nhiều nhất một lần gọi được viết; quá thì bị cắt giữa chừng |
| khuôn đầu ra | **output schema**, **JSON schema** | mẫu bắt model trả về đúng các ô đã định (ví dụ ô "câu trả lời", ô "tuyến"), để chương trình đọc được |
| chữ chạy dần | **streaming** | model gửi từng mẩu chữ ngay khi viết, giao diện hiện dần; ngược lại là chờ viết xong mới gửi cả câu |

## Một model viết làm chín loại việc

Chương trình dựng nhiều vai có model: xếp loại câu, trả lời, trò chuyện, mục web, câu cho thẻ lịch, hai lời gọi hiểu lệnh sửa lịch, nhận ảnh… (hồ sơ đếm là chín loại lời gọi; bảng ở nửa để tra là một cách xếp để dễ nhớ). Mỗi vai có lời dặn, khuôn đầu ra, công cụ riêng, nhưng **tất cả dùng chung một đối tượng model**: một dòng cấu hình đổi được tất cả, và không đổi lẻ được (không có cách cho Claude viết câu trả lời mà gpt-6-luna xếp loại câu).

## Hai model đã chạy, khác nhau ở bốn chỗ người dùng thấy

Sáng 21/11 chủ dự án đổi tạm model viết từ gpt-6-luna (OpenAI) sang Claude Sonnet 5.5 qua Amazon Bedrock, với điều kiện giữ nguyên thư viện đang dùng và nói "chuyển về luna" là về được ngay. Tối 21/11 chủ dự án gác hẳn gpt-6-luna vì tài khoản OpenAI hết tiền; từ đó mọi phép đo chỉ chạy trên Claude.

| Người dùng thấy | gpt-6-luna | Claude Sonnet 5.5 (mức cao) |
|---|---|---|
| Độ dài câu trả lời một dữ kiện (ký tự, câu đứng giữa; 85 câu đầu bộ câu mẫu, 21/11) | 90 | 236–258 |
| Chữ hiện thế nào | chạy dần | **một lần**, khi model viết xong |
| Lên lịch 3 ngày bằng biểu mẫu (một lượt qua trình duyệt, 21/11) | 5,6 giây | 11,2 giây |
| Tiền một câu trả lời có nguồn (66 câu, 21/11) | 0,0004 USD | 0,0146 USD |

Đọc bảng:

- **Chậm hơn vì viết dài hơn**, không phải vì sinh chữ chậm: khoảng 114 và 101 token mỗi giây (bài 34).
- **Đắt hơn ở hai tầng:** giá mỗi token gấp 20 lần (bảng ở nửa để tra), câu lại dài hơn, nên tiền mỗi câu gấp khoảng 37 lần (66 câu, mức cao: 0,0146 so với 0,00039 USD).
- **Chất lượng** (66 câu tính điểm, thang 1–5, 21/11): "đúng" ngang nhau (4,97 và 4,94), "đủ ý" Claude nhỉnh hơn (4,83 và 4,88), "trọng tâm" Claude thấp hơn rõ (4,94 và 4,39) vì thêm chi tiết sau câu trả lời chính. Chủ dự án đã nhận độ dài đó.

## Mức suy luận đang để cao, vì mức thấp hỏng ở việc khó

Nghĩ ít thì có lúc bỏ sót điều kiện trong lời dặn. Với Claude, chương trình luôn **gửi rõ một mức**, vì không gửi gì thì Claude tự nghĩ cỡ mức cao. Cấu hình đang ghi:

- Mức **cao** cho mọi vai không tự đặt mức (xếp loại câu, trả lời, trợ lý, trò chuyện, mục web, nhận ảnh), và riêng cho hiểu lệnh sửa lịch.
- Mức **thấp** cho lượt biểu mẫu và câu thẻ lịch, đặt cứng trong chương trình.

Số đo và lý do: quyết định 2.

## Đổi model không chỉ là đổi tên: lớp nối, và lỗi đã gặp ở đó

Claude được gọi theo cách riêng của Claude, khác OpenAI ở nhiều chỗ nhỏ. Lớp nối lo hết các chỗ đó, nên thư viện và chín vai không biết phía sau là ai. Mỗi chỗ đều được đo thật trước khi viết. Ví dụ: khuôn có ràng buộc kiểu "nhiều nhất 3 mục" bị Bedrock từ chối, nên lớp nối gỡ ràng buộc khỏi khuôn gửi đi; chương trình vẫn kiểm đủ khi nhận về.

**Lỗi đắt nhất: Claude xin công cụ mãi, không viết.** Ở lượt trợ lý có công cụ, thư viện gửi cùng lúc danh sách công cụ và khuôn đầu ra bắt buộc. gpt-6-luna gọi công cụ xong thì viết vào khuôn. Claude đã có đủ kết quả mà vẫn xin công cụ tiếp, tới hết số vòng, và người dùng nhận câu từ chối. Phát lại một yêu cầu đã đủ dữ liệu: **viết được 0 trên 8 lần** ở mỗi mức suy luận; bỏ khuôn thì 14 trên 14. Sửa: ở lượt có công cụ, lớp nối không gửi khuôn mà thêm một công cụ nội bộ "trả lời" mang đúng khuôn đó; Claude gọi nó để nộp câu trả lời. Trên thước 29 câu làm trợ lý (bài 32): số câu chạm trần vòng **6 xuống 0**; nhóm 8 câu cần nhiều công cụ đạt 2 lên 7.

**Lỗi thứ hai: câu hỏi cũ dính vào câu đang hỏi.** Lịch sử lúc đó chỉ giữ câu hỏi, nên nhiều tin của người dùng đứng liền nhau. Claude đòi tin của người dùng và tin của trợ lý xen kẽ nhau, nên bản nối đầu gộp hai câu hỏi liền nhau làm một, nên câu "bạn còn nhớ tôi tên gì" dính vào câu giá vé lượt trước. Sửa: chèn một tin giữ chỗ giữa hai câu hỏi; sau sửa 0 lỗi trên 18 lượt đo.

Cả hai lỗi đều do Claude hiểu cùng một yêu cầu khác gpt-6-luna, không phải do model kém.

## Quyết định và lý do

### 1. Vì sao giữ thư viện của OpenAI mà chạy Claude qua một lớp nối tự viết?

- **Đã chọn:** giữ thư viện OpenAI Agents SDK; viết một lớp nối khoảng 300 dòng, không thêm thư viện nào.
- **Vì sao:** chủ dự án đặt điều kiện "giữ nguyên bộ khung đang dùng" khi đổi tạm; vì sao chủ dự án đặt điều kiện này: chưa thấy ghi lý do (cùng lời dặn có yêu cầu "nói chuyển về luna là về được ngay"). Điều thấy được: chín vai, vòng công cụ, phần ghi sổ tiền và test cũ không phải sửa; mọi loại lời gọi gửi OpenAI (mười loại, vì vài vai có hai biến thể) chụp trước và sau khi có lớp nối giống nhau từng byte, nên đường về gpt-6-luna không bị đụng.
- **Cách khác:** trỏ thư viện sang địa chỉ của Bedrock nhận yêu cầu viết theo kiểu OpenAI, khỏi cần lớp nối: đã thử, Bedrock trả "không có" cho model này ở địa chỉ đó. Viết lại chín vai bằng thư viện của Anthropic, hoặc dùng một thư viện trung gian gọi được nhiều hãng: không làm (quyết định đã ghi: giữ bộ khung).
- **Cái giá:** mọi khác biệt giữa hai hãng dồn vào lớp nối và chỉ lộ ra khi chạy thật; hai lỗi lớn ở mục trên đều nằm ở đây. Thêm hãng thứ ba thì viết thêm một lớp nối.

### 2. Vì sao mức suy luận để cao, khi ở câu thường bốn mức ngang nhau?

- **Đã chọn:** mức cao cho mọi vai không tự đặt mức và cho hiểu lệnh sửa lịch; mức thấp cho lượt biểu mẫu và câu thẻ lịch.
- **Vì sao:** đo ngày 21/11. Ở hỏi đáp một lượt (66 câu), bốn mức ngang nhau và mức cao chỉ chậm hơn mức vừa khoảng 0,3 giây; chủ dự án chọn mức cao "vì không mất gì đáng kể". Ở lệnh sửa lịch khó (3 lượt mỗi lệnh), mức cao đúng 5 trên 6, mức thấp 2, mức vừa 0. Ở lượt có công cụ thời tiết, ngày (12 lượt), mức vừa và thấp chạm trần vòng 8–9 lượt, mức cao 1. Nhóm lịch giữ mức thấp: đo trên 4 kiểu lịch, ba mức cho cùng kết quả.
- **Cách khác:** mức vừa hoặc thấp cho câu trả lời: đã đo ở câu một lượt (ngang nhau). Đo lại mức vừa và thấp ở lượt có công cụ sau khi sửa lớp nối: chưa làm, đang nằm trong hàng đo.
- **Cái giá:** chậm hơn một chút và tốn token suy luận ở mọi lượt; lợi của mức cao ở lượt có công cụ là số đo **trước** khi sửa lớp nối, có thể đã không còn đúng.

### 3. Vì sao chấp nhận chữ tới một lần với Claude?

- **Đã chọn:** gọi Claude trọn một lần, gửi cả câu trả lời một lần. Trong lúc chờ, dòng trạng thái đổi qua "Đang hiểu câu hỏi…", "Đang tìm trong kho…", rồi đứng ở "Đã tìm trong kho, đang chuẩn bị câu trả lời… (10 đoạn)" cho tới khi cả câu hiện ra (ở lượt có công cụ, "Đang viết câu trả lời…" chỉ được gửi ngay trước chữ đầu, nên với Claude gần như không thấy).
- **Vì sao:** bộ khoá Bedrock bị từ chối khi xin chữ chạy dần; khi đổi tạm, chủ dự án ghi "không cần stream thật".
- **Cách khác:** xin thêm quyền và viết đường chữ chạy dần: chưa làm; ước (chưa đo) chờ tới chữ đầu từ khoảng 13 giây còn 5,5–6 giây.
- **Cái giá:** người dùng nhìn dòng "Đã tìm trong kho, đang chuẩn bị câu trả lời… (10 đoạn)" khoảng 10 giây ở lượt đứng giữa (bài 34); lợi của "hiện trước, kiểm sau" (bài 6) mất, cái giá của nó còn.

### 4. Vì sao Claude có những đoạn dặn riêng, và đổi model thì phải đo lại những gì?

- **Đã chọn:** lời dặn gửi gpt-6-luna không đổi một chữ. Khi chạy Claude, chương trình nối thêm ba đoạn dặn ngắn: cho xếp loại câu (địa bàn Huế gồm cả vùng ven, bài 22), cho câu thẻ lịch (một hai câu, giữ con số đi đúng vật), cho hiểu lệnh sửa lịch.
- **Vì sao:** mỗi đoạn có một ca đo làm lý do. Ví dụ ở bước xếp loại câu: cùng lời dặn, gpt-6-luna xếp nhầm 0 trên 56 lượt, Claude 2 trên 56 ở mức cao và 4 trên 56 ở mức vừa. Ở lệnh sửa lịch sau đoạn dặn: 27 trên 27 lượt đúng ý.
- **Cách khác:** đoạn dặn thứ tư "nói thẳng, không lặp ý": đã thử trên 85 câu, câu dài thêm, trọng tâm 4,39 xuống 4,26 ⇒ gỡ.
- **Cái giá:** mỗi lần đổi model phải đo lại ít nhất bước xếp loại câu, lệnh sửa lịch khó, lượt có công cụ, độ dài và điểm câu trả lời; nếu là hãng mới thì thêm năm chỗ cách gọi hay khác nhau: khuôn có ràng buộc, ép gọi công cụ, quyền chữ chạy dần, cách tắt suy luận, cách đếm token.

## Nếu… thì sao

Một tình huống kể trọn. Khoá Bedrock là khoá tạm do chủ dự án giữ; giả sử nó hết hạn giữa buổi. Máy chủ vẫn chạy, đường báo tình trạng vẫn báo đủ (bài 6). Mỗi câu hỏi nhận "Không thể tạo câu trả lời vào lúc này." và nút "Thử lại"; bấm lại vẫn vậy. Không có cơ chế tự làm mới khoá (chủ dự án dặn không xây). Chương trình đọc lại file khoá ở mỗi lần gọi, nên có người làm mới file xong là hỏi được ngay, không cần khởi động lại máy chủ.

Lời báo là nguyên văn; các dòng đọc từ chương trình, chưa thử thật ngày 22/11.

| Nếu | Người dùng thấy gì | Muốn hết lỗi thì ai làm gì |
|---|---|---|
| khoá Bedrock hết hạn, hoặc thiếu chỗ trỏ tới file khoá lúc bật | "Không thể tạo câu trả lời vào lúc này." ở mọi câu hỏi | hết hạn: chủ dự án làm mới file khoá; thiếu chỗ trỏ: bật lại máy chủ cho đúng (bài 36) |
| phần viết của một lượt quá 45 giây | cùng lời báo trên | người dùng bấm "Thử lại"; đã gặp một lần trong 156 lượt người dùng mô phỏng của Claude tối 21/11 (lúc hai model chạy cùng lúc trên một máy); lượt dài nhất khi chạy một mình là 28 giây (bài 34) |
| quay về gpt-6-luna | chữ lại chạy dần, câu ngắn hơn | sửa một chữ trong cấu hình, khởi động lại máy chủ; **chưa làm được lúc này** (tài khoản OpenAI ngừng dùng) |
| đổi sang model thứ ba | chưa biết | hãng mới thì viết lớp nối mới; đo lại các mục ở quyết định 5 |

## Dễ nhầm

- **"Đổi model chỉ là đổi tên model trong cấu hình."** Dòng cấu hình là một dòng, nhưng lần đổi sang Claude cần một lớp nối, ba đoạn dặn riêng, và lộ hai lỗi chỉ thấy khi chạy thật.

## Câu hỏi tự kiểm

<details>
<summary>1. Vì sao không trỏ thẳng thư viện sang Bedrock mà phải viết lớp nối?</summary>

Đã thử: Bedrock không phục vụ model này ở địa chỉ nhận yêu cầu kiểu OpenAI. Phải gọi theo cách riêng của Claude; lớp nối đổi qua lại để thư viện và các vai giữ nguyên.

</details>

<details>
<summary>2. Lỗi "xin công cụ mãi" là gì, và sửa thế nào?</summary>

Gửi cùng lúc công cụ và khuôn đầu ra bắt buộc thì Claude cứ xin công cụ, không viết (0 trên 8 lần ở mỗi mức, bốn mức). Sửa: thay khuôn bằng một công cụ nội bộ "trả lời". Câu chạm trần vòng 6 xuống 0 trên 29.

</details>

<details>
<summary>3. Vì sao mức suy luận để cao dù ở câu thường bốn mức ngang nhau?</summary>

Mức cao chỉ chậm hơn khoảng 0,3 giây, mà ở lệnh sửa lịch khó đúng 5 trên 6 (mức thấp 2); chủ dự án chọn mức cao.

</details>

<details>
<summary>4. Muốn quay về gpt-6-luna thì làm gì, và lúc này có làm được không?</summary>

Sửa một chữ trên dòng cấu hình chọn hãng, khởi động lại máy chủ, chạy thử một lượt; không sửa chương trình. Lúc này chưa làm được: tài khoản OpenAI đang ngừng dùng.

</details>

## Cấu hình đang chạy

*Theo cấu hình trưa 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| `full_corpus_generation.provider` | `bedrock` | chọn hãng cho cả chín vai; `openai` là gpt-6-luna | đã chạy cả hai |
| `full_corpus_generation.model` | `gpt-6-luna` | model của đường OpenAI; chỉ đọc khi chọn `openai` | khoá cứng trong chương trình kiểm cấu hình: có 8 giá trị cấu hình chương trình chỉ nhận đúng một giá trị, ghi khác thì máy chủ không bật (phụ lục A, B) |
| `bedrock.model` · `bedrock.region` | Claude Sonnet 5.5 · Singapore | model và vùng của Bedrock | — |
| `bedrock.max_tokens` | 128.000 | trường bắt buộc của Claude; để mức tối đa = coi như không trần | không đặt nhỏ hơn (quyết định 3) |
| `bedrock.reasoning_default` | cao | mức suy luận cho vai không tự đặt mức | đã đo bốn mức ở câu một lượt |
| `bedrock.reasoning_sua_lich` | cao | riêng hiểu lệnh sửa lịch | đã đo ba mức: cao 5/6, thấp 2/6, vừa 0/6 |
| Mức của lượt biểu mẫu và câu thẻ lịch | thấp, đặt cứng | không cần nghĩ ở việc này | đã đo ba mức: cùng kết quả |
| `bedrock.sua_lich_timeout_seconds` | 10 giây | hạn riêng của lời gọi hiểu lệnh sửa lịch trên Claude | lâu nhất đã thấy 7,1 giây |
| `bedrock.creds_file_env` | tên một biến môi trường | trỏ tới file khoá tạm; đường dẫn không ghi vào repo (bài 37) | — |
| `full_corpus_generation.timeout_seconds` | 45 giây | hạn cho cả phần viết của một lượt (bài 6) | chưa so |
| Đệm lời dặn với Claude | chưa bật | tiết kiệm token lời dặn lặp lại | đã thử: thời gian 2,72 và 2,69 giây, không nhanh hơn |

## Các vai dùng chung model viết (cách xếp của người viết, để dễ nhớ)

| Vai | Làm gì | Bài |
|---|---|---|
| xếp loại câu (kèm bản viết câu tìm) | chọn một trong bốn tuyến | 22 |
| trả lời | viết câu trả lời có số nguồn từ 10 đoạn | 15 |
| trợ lý có công cụ | như trên, được xin tìm thêm và gọi công cụ | 21, 24 |
| trò chuyện | đáp câu chào, câu cảm ơn | 22 |
| mục web | viết mục "Từ web (chưa kiểm)" | 25 |
| lượt biểu mẫu lập lịch (kiểu cũ) | viết phần chữ của lượt lập lịch từ biểu mẫu, theo luật lịch trong lời dặn | 27 |
| câu cho thẻ lịch | một hai câu mô tả từng điểm | 29 |
| hiểu lệnh sửa lịch | đổi câu người dùng gõ thành một hành động có tên | 31 |
| nhận ảnh | đoán tên nơi, món trong ảnh | 26 |

## Đã so

**Bảng giá ghi sổ** (USD cho một triệu token; giá Claude chưa đối chiếu hoá đơn):

| | Vào | Vào, đọc lại từ đệm | Vào, ghi vào đệm | Viết ra |
|---|---|---|---|---|
| gpt-6-luna | 0,10 | 0,01 | 0,125 | 0,50 |
| Claude Sonnet 5.5 | 2,00 | 0,10 | 2,50 | 10,00 |

**Bốn mức suy luận của Claude, hỏi đáp một lượt** (85 câu đầu bộ câu mẫu, 66 câu tính điểm, một lượt mỗi mức, người chấm gpt-6-luna; ngày 21/11, trước khi sửa lớp nối):

| | gpt-6-luna | không | thấp | vừa | cao |
|---|---|---|---|---|---|
| Đúng | 4,97 | 4,89 | 4,89 | 4,91 | 4,94 |
| Đủ ý | 4,83 | 4,82 | 4,83 | 4,86 | 4,88 |
| Trọng tâm | 4,94 | 4,44 | 4,39 | 4,36 | 4,39 |
| Cả câu, câu đứng giữa (giây) | 3,1 | 2,4 | 2,3 | 2,3 | 2,6 |
| Tiền một câu (USD) | 0,00039 | 0,0124 | 0,0137 | 0,0138 | 0,0146 |
| Phần trăm lời gọi viết câu trả lời có dùng token suy luận | 34–36 % | 0 % | 2 % | 5 % | 14 % |

Đọc bảng: chênh giữa các mức nằm trong 1–2 câu; hai lượt gpt-6-luna giống hệt nhau đã lệch 0–1 câu ở "đúng", 1–3 câu ở "đủ ý". Theo luật ghi trước, cả bốn mức đều phạm mức tụt ở "trọng tâm" (vì dài), nên tập ứng viên rỗng; chủ dự án quyết nhận độ dài và chọn mức cao. Giới hạn: một lượt mỗi mức, câu một lượt không có công cụ.

**Các thứ đã thử với Claude ngày 21/11 mà không đưa vào:** đoạn dặn "nói thẳng" (gỡ, xem quyết định 5); cho gọi công cụ 8 vòng thay 4, tìm kho 4 lần thay 2 (thước 28 và 28 trên 29, không đổi; lúc đó trần là 2 lần tìm, 4 vòng — từ 14:47 ngày 22/11 là 3 và 5, mở cùng hai thay đổi ở khâu tìm, bài 21); trả lại phần suy nghĩ giữa các vòng công cụ (24 trên 24 cả hai bên); đệm lời dặn (không nhanh hơn).

## Quyết định nhỏ hơn

**Vì sao không đặt trần số token model được viết ra?**

- **Đã chọn:** không đặt trần ở lời gọi nào. Với Claude, trần là bắt buộc nên gửi mức tối đa của model; không vai nào hạ được.
- **Vì sao:** chủ dự án quyết ngày 19/11 ("chất lượng trước, tiền và tốc độ sau"). Lý do ghi trong chương trình: trần tính cả token suy luận, và đã cắt một lời gọi xếp loại câu khi model nghĩ hết 512 trên 512 token. Rào còn lại: hạn 45 giây mỗi lượt, trần số vòng công cụ.
- **Cách khác:** trần 512 token như trước 19/11: đã dùng, đếm 3.974 lần gọi thì 2 lần chạm trần, cả hai ở bước xếp loại câu.
- **Cái giá:** chỉ hạn giờ chặn một câu quá dài. Thực tế lời gọi dài nhất trên 85 câu viết 684 token (21/11).

**Vì sao người chấm của bộ đo đổi sang chính model đang chạy?** Chủ dự án quyết tối 21/11 khi gác gpt-6-luna: mọi phép đo chỉ chạy trên model đang chạy, kể cả người chấm. Cái giá ghi kèm quyết định: người chấm cùng họ với model viết có thể chấm dễ hơn, và số chấm bằng người chấm mới không so thẳng với số cũ (24/10–19/11 Claude chấm chính trên file đã che tên, gpt-6-luna chấm phụ một lần; ban ngày 21/11 gpt-6-luna chấm — bài 19); cần một lượt mốc mới.

## Giới hạn đã biết

- **Đổi tạm, chưa có quyết định giữ lâu dài.** Đường gpt-6-luna nguyên vẹn nhưng tài khoản đang ngừng dùng; các tính năng mở từ tối 21/11 chưa đo trên gpt-6-luna.
- **Chưa đo lại mức vừa và thấp ở lượt có công cụ** sau khi sửa lớp nối.
- **Chữ tới một lần**, chờ trắng có lượt quá 15 giây (bài 34).
- **Câu thẻ lịch của Claude** có thể ghép sai ý của một câu nguồn dài (một mục, 12 lượt: sai 1, nói lỏng 4); bộ kiểm của chương trình không bắt được loại lỗi này (bài 29).
- **Phụ thuộc một khoá tạm** do chủ dự án giữ; hết hạn là ô hỏi đáp ngừng cho tới khi làm mới. Vì gpt-6-luna đang gác, không có model dự phòng.
- **Người chấm của bộ đo nay là chính model đang chạy** (từ 21/11 tối); người chấm cùng họ với model viết có thể chấm dễ hơn (quyết định nhỏ ở trên).

## Chi tiết để tra

- Tốc độ đo thẳng ở Bedrock (không qua sản phẩm, 21/11): xếp loại câu 0,8–0,9 giây; trả lời khoảng 6.800 token vào, 400 ra: 3,5–3,9 giây; lượt có suy luận thật và khoảng 2.000 token ra: 15–20 giây; 0 lần bị giới hạn tần suất trong 46 lời gọi.
- Tắt hẳn suy luận ở Claude: hai cách "tắt" thẳng đều bị từ chối; lớp nối dùng chế độ "chỉ nghĩ giữa các lần gọi công cụ", đo được 0 token suy luận 6 trên 6 lần.
- Ép model gọi đúng một công cụ: Claude chỉ nhận "tự chọn" hoặc "không công cụ", nên lớp nối không ép.
- Ở vòng mà mọi công cụ đã bị ẩn (hết lượt tìm), ép khuôn làm Claude viết rác vào khuôn (tên công cụ, chữ giữ chỗ, rỗng) 14 trên 22 lần; chỉ đưa công cụ "trả lời": đúng câu từ chối 20 trên 22, 0 rác.
- Lời lỗi của lớp nối không mang thân phản hồi của Amazon (thân đó có mã tài khoản); chỗ đọc file khoá lỗi chỉ ghi tên loại lỗi, không ghi đường dẫn.
- Tiền một câu ở mức thấp (lượt thật đầu tiên qua giao diện, 21/11): khoảng 0,018 USD trên Claude so với khoảng 0,0007 USD trên gpt-6-luna; lượt hỏi tiếp có tìm thêm 0,048 USD.
- Người chấm của bộ đo: 24/10–19/11 là Claude (chấm chính, đọc file đã che tên), gpt-6-luna chấm phụ một lần để đối chiếu; ban ngày 21/11, lúc đổi model viết, là gpt-6-luna; từ tối 21/11, khi gác gpt-6-luna, chấm bằng model đang chạy, và số mới không so thẳng với số cũ (bài 19).
- Lớp nối có khoảng 20 ca test bằng phản hồi dựng sẵn, không gọi mạng (20 ca đếm 21/11; 21 ca đếm 22/11; bài 38).
- Mức suy luận của gpt-6-luna: chương trình không gửi mức nào (trừ nhóm lịch, kể cả hiểu lệnh sửa lịch), tức model chạy mức vừa mặc định. Ngày 19/11 đã đo mức thấp: chất lượng không khác, nhưng một lần nói trái nguồn ở bộ câu an toàn, nên giữ mức vừa.

**Bài sau (bài 34):** người dùng chờ bao lâu, thời gian đó đi vào đâu, và một câu tốn bao nhiêu tiền.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Chín vai dùng chung một đối tượng model: `backend/llm/generator_openai_full_corpus.py` (`__init__`: `answer_agent`, `router_agent` + `router_search_agents`, `chat_agent`, `assistant_agent` và bản có lịch sử, `bieu_mau_agent`, `lich_v2_agent`, `sua_lich_agent` và các bản biến thể, `web_agent`; nhận ảnh qua `backend/api/routes/anh.py` dùng cùng `generator`); "chín agent" `report_agent/2026-11-21/b_bedrock_sonnet.md` mục 1; cách người viết xếp chín vai thành bảng là [suy từ code].
- Đổi tạm, ba điều kiện, gác luna: `session_prompt/HIEN_TRANG.md` mục 4 (gạch 09:41 21/11, 21:43 và 21:50 21/11); `bai_hoc/VIEC_MOI_XONG.md` mục 23 [chép].
- Lớp nối và các chỗ khác nhau: `backend/llm/bedrock_model.py` (chú thích đầu file, `build_body`, `to_messages`, `HISTORY_GAP`, `ANSWER_TOOL`, `stream_response`, `_invoke`, `to_usage_dict`) [code]; bảng "luna gửi gì ⇄ Claude cần gì", 404 ở cổng kiểu OpenAI, 687 token suy luận khi không gửi mức, 0/6 token suy luận ở `between_tools`: `guides/DOI_MODEL_VIET.md` mục 4 [đã chạy 21/11, chép].
- Lỗi xin công cụ mãi: 0/8 mỗi mức, bỏ khuôn 14/14, 22 lần phát lại (14 rác, sau sửa 20/22): `guides/DOI_MODEL_VIET.md` mục 4; chạm trần vòng 6 ⇒ 0/29, 8 câu ghép 2 ⇒ 7: `bai_hoc/VIEC_MOI_XONG.md` mục 23 và `data/thu_bedrock_2026-11-21/harness/CHOT_DOT_CAI_THIEN.md` dòng 63 [riêng tư]. Chú thích trong code ghi "0 / 30 lần ở mọi mức suy luận" cho cùng phép phát lại — bài dùng số 0/8 mỗi mức của trang đổi model.
- Lỗi dính lịch sử và 0/18 sau sửa: `bai_hoc/VIEC_MOI_XONG.md` mục 23; `session_prompt/HIEN_TRANG.md` mục 1 [chép].
- So hai model (độ dài 90 ↔ 236–258, 5,6 ↔ 11,2 giây, điểm 66 câu, 114 ↔ 101 token/giây): `bai_hoc/VIEC_MOI_XONG.md` mục 23; `data/thu_bedrock_2026-11-21/b_toc_do/THOI_GIAN_DI_DAU.md` mục 1 [riêng tư; đã chạy 21/11].
- Bảng bốn mức (66 câu), 0,3 giây, tỉ lệ lời gọi có suy luận, 684 token lớn nhất, quyết định của chủ dự án chọn high: `data/thu_bedrock_2026-11-21/do/bac_2a/KET_QUA_2A.md` [riêng tư; đã chạy 21/11].
- Sửa lịch khó 5/6 · 2/6 · 0/6; nhóm lịch giữ low; chạm trần 8–9/12 ở medium/low trước bản sửa: `backend/config/settings.yaml` (chú thích `reasoning_sua_lich`), `guides/DOI_MODEL_VIET.md` mục 3 và 7; `data/thu_bedrock_2026-11-21/do/TONG_HOP_BAN_0.md` dòng 45 [riêng tư].
- Mức của luna (không gửi = mức vừa; đo low ↔ medium 19/11): `bai_hoc/VIEC_MOI_XONG.md` mục 12; `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng 45 [chép].
- Không trần token: chú thích trong `generator_openai_full_corpus.py` (trên `answer_agent`), `settings.yaml` (`max_tokens`); 3.974 lần gọi, 2 chạm trần 512: `bai_hoc/VIEC_MOI_XONG.md` mục 9 [chép].
- Chữ tới một lần, "không cần stream thật": `bedrock_model.py` (`stream_response`), `HIEN_TRANG.md` mục 4 gạch 09:41; ước 5,5–6 giây: `THOI_GIAN_DI_DAU.md` mục 3 hàng A [ước, chưa đo]. Bốn dòng trạng thái: `frontend/src/chat.jsx` dòng 21–24 [code].
- Đoạn dặn riêng Claude: `backend/llm/full_corpus_prompt.py` (hằng `SONNET_*`), hàm `kem` trong `generator_openai_full_corpus.py`; số 0/56, 2/56, 4/56: `data/thu_bedrock_2026-11-21/c_harness/RA_HARNESS.md` dòng 22 [riêng tư]; 27/27: `guides/DOI_MODEL_VIET.md` mục 1; đoạn "nói thẳng" gỡ: cùng chỗ.
- Bảng giá: `backend/llm/pricing.py` (`PRICES_PER_M`) [code]. Tiền 0,00039 ↔ 0,0146 USD: `KET_QUA_2A.md`; 0,018 ↔ 0,0007: `report_agent/2026-11-21/b_bedrock_sonnet.md` mục 3.
- Giữ một phiên chụp 10 loại lời gọi giống từng byte: `guides/DOI_MODEL_VIET.md` mục 1; `report_agent/2026-11-21/b_bedrock_sonnet.md` dòng 75 [người thứ hai kiểm].
- Lời báo "Không thể tạo câu trả lời vào lúc này.": `backend/api/routes/chat.py` (`GENERATION_FAILURE_MESSAGE`); mọi lỗi Bedrock là `GenerationError`: lớp `BedrockError` [code]. Tình huống khoá hết hạn [đọc từ chương trình, chưa thử thật]; đọc lại file khoá mỗi lần gọi: `BedrockClaudeModel._invoke` [code]. 12,6 giây là lời gọi dài nhất trên thước 29 câu (`guides/DOI_MODEL_VIET.md` mục 3), không phải lượt dài nhất.
- Cách đổi về luna: `guides/DOI_MODEL_VIET.md` mục 2. Đường luna khoá cứng `gpt-6-luna`: cùng trang mục 6.
- Thứ đã thử mà không đưa vào: `bai_hoc/VIEC_MOI_XONG.md` mục 23 bảng cuối.
- Người chấm đổi sang model đang chạy, có thể chấm dễ hơn; không model dự phòng: `HIEN_TRANG.md` mục 4 gạch 21:43 [chép].
- Lượt chạm 45 giây: `data/thu_bedrock_2026-11-21/do/moc_12vai/KET_QUA_MOC.md` (r1, V01 lượt 3) [riêng tư]. Dòng trạng thái ở lượt có công cụ: `backend/llm/assistant.py` (`pending_generating`, "đang viết" phát ngay trước chữ đầu) [code].
- Bài đã qua một lượt đối chiếu độc lập 22/11: `data/hoc_cung_D/kiem/bai_33_38.md` [riêng tư]; dòng không áp ghi ở `data/hoc_cung_D/viet/viet_33_38.md` mục "Sau lượt kiểm".

- Cập nhật theo bộ thay đổi mở 14:47 22/11/2026: `bai_hoc/VIEC_MOI_XONG.md` mục 42, 43; `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 (hàng "Trần tìm 3 lần / 5 vòng là khoá CHUNG cho cả hai đường model"); `backend/config/settings.yaml` [code; người viết không chạy lại]. Người chấm 24/10–19/11 là Claude (chính), gpt-6-luna phụ: `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` dòng 34 ("Judge chính là Claude (xem E1)") [chép; sửa theo bài 19]. 8 giá trị khoá: `backend/core/settings_loader.py` `validate_phase6_settings` [code, đọc 22/11].

</details>
