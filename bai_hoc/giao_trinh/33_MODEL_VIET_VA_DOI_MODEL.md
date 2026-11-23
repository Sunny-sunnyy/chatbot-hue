# Bài 33 — Model viết, mức suy luận, và đổi model bằng một dòng cấu hình

*Cập nhật 21:06, ngày 23/11/2026 · đã áp biên bản kiểm độc lập tối 23/11 · khớp hệ thống lúc code đứng yên tối 23/11 (57 tính năng mở, 6 tắt, kho 269 bài / 9.533 đoạn) · thêm lượt đo bù trên model cũ, gọi lại một lần trên đường OpenAI · cả bộ test 20:09 23/11: 2.307 ca đạt, một file đỏ ở phép kiểm, đã sửa, chạy lại riêng: đạt (bài 38) · người viết không chạy lại phép đo · mốc cũ: Nguồn.*

**Bài trước đã biết:** một câu hỏi đi qua sáu bước, gần như toàn bộ thời gian chờ là model viết (bài 6); model viết được gọi nhiều lần trong một lượt: xếp loại câu, tìm thêm, viết (bài 21, 22).
**Bài này thêm:** hai model khác nhau ở đâu, vì sao mức suy luận để cao, vì sao đổi model chỉ sửa một dòng mà vẫn phải viết lớp nối và đo lại (lượt đo bù cho bản deploy).

## Ý chính

- **Một model viết làm mọi việc có model** (xếp loại câu, trả lời, mục web, câu thẻ lịch, hiểu lệnh sửa lịch, nhận ảnh…; hồ sơ đếm là chín loại lời gọi). Cả chín vai dùng chung một đối tượng model: đổi model là đổi tất cả cùng lúc, không đổi lẻ được.
- **Hai model, hai nơi chạy.** gpt-6-luna của OpenAI chạy tới trưa 21/11; từ đó máy chủ dự án chạy Claude Sonnet 5.5 qua Amazon Bedrock, **đổi tạm**. Bản deploy sẽ chạy lại gpt-6-luna (chủ dự án chốt sáng 23/11). Đổi qua lại: một dòng cấu hình.
- Claude **viết dài hơn khoảng ba lần**, **đắt hơn 20 lần mỗi token**, **chữ tới một lần**; đúng ngang, đủ ý nhỉnh hơn, gọn kém hơn. **Mức suy luận để cao**: ở câu một lượt bốn mức ngang nhau, ở việc khó mức thấp hơn hỏng rõ.
- **Đổi model không chỉ là đổi tên.** Claude đi qua một lớp nối tự viết; lỗi lớn nhất nằm ở chỗ nối: Claude xin công cụ mãi không viết; sửa xong, câu chạm trần vòng 6 xuống 0 trên 29.
- **Mọi thứ mở từ 21/11 chỉ đo trên Claude, nên tối 23/11 có một lượt đo bù trên model cũ**, mỗi ô một lượt: 41 câu khó đạt 37 (mốc 21/11 trên code cũ: 20–21), demo 10 bước không bước nào hỏng, 16 / 16 ca tính năng chạy được đều đạt; lộ hai lỗi thật, đã sửa (bài 31). Các ô đó chạy trước khi gắn đoạn dặn câu tỉnh khác cho model cũ; bản cuối chưa chạy lại 41 câu khó.

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
| lượt đo bù | — | đo lại trên model cũ những thứ trước đó chỉ đo trên model đang chạy |

## Hai model đã chạy, khác nhau ở bốn chỗ người dùng thấy

Sáng 21/11 chủ dự án đổi tạm model viết sang Claude, với điều kiện giữ nguyên thư viện đang dùng và nói "chuyển về luna" là về được ngay.

| Người dùng thấy | gpt-6-luna | Claude Sonnet 5.5 (mức cao) |
|---|---|---|
| Độ dài câu trả lời (ký tự, câu đứng giữa; 85 câu đầu bộ câu mẫu, 21/11) | 90 | 236–258 |
| Chữ hiện thế nào | chạy dần | **một lần**, khi model viết xong |
| Lên lịch 3 ngày bằng biểu mẫu (một lượt qua trình duyệt, 21/11) | 5,6 giây | 11,2 giây |
| Tiền một câu trả lời có nguồn (66 câu, 21/11) | 0,0004 USD | 0,0146 USD |

Đọc bảng: **chậm hơn vì viết dài hơn**, không phải vì sinh chữ chậm (bài 34); **đắt hơn ở hai tầng**: giá mỗi token gấp 20 lần, câu lại dài hơn. **Chất lượng** (66 câu tính điểm, thang 1–5, 21/11; số ở "Đã so"): "đúng" ngang nhau, "đủ ý" Claude nhỉnh hơn, "trọng tâm" Claude thấp hơn rõ vì thêm chi tiết sau câu trả lời chính. Chủ dự án đã nhận độ dài đó.

## Đổi model không chỉ là đổi tên: lớp nối, và lỗi đã gặp ở đó

Claude được gọi theo cách riêng, khác OpenAI ở nhiều chỗ nhỏ; lớp nối lo hết, nên thư viện và chín vai không biết phía sau là ai.

**Lỗi đắt nhất: Claude xin công cụ mãi, không viết.** Ở lượt có công cụ, thư viện gửi cùng lúc danh sách công cụ và khuôn đầu ra bắt buộc; Claude đủ kết quả mà vẫn xin tới hết vòng, người dùng nhận câu từ chối (**viết được 0 trên 8 lần** ở mỗi mức suy luận). Sửa: lớp nối thay khuôn bằng một công cụ nội bộ "trả lời"; câu chạm trần vòng **6 xuống 0** trên 29. Lỗi thứ hai (câu hỏi cũ dính vào câu đang hỏi) ở "Chi tiết để tra". Cả hai đều do Claude hiểu cùng một yêu cầu khác gpt-6-luna, không phải do model kém.

## Bản deploy chạy model cũ, nên tối 23/11 có một lượt đo bù

Hai model dùng chung một harness: cùng lời dặn gốc, trần, tính năng. Tối 21/11 tài khoản OpenAI hết tiền, chủ dự án gác gpt-6-luna; từ đó thứ mở mới chỉ được đo trên Claude, và nhóm ghi một món nợ: phải đo bù trước khi tin bản chạy model cũ. Sáng 23/11 chủ dự án chốt bản deploy dùng model của OpenAI; khoảng 17:58 anh nạp tiền, dặn không test quá mức, trần 2 đến 2,5 USD (nguyên văn: "Chi tiết để tra").

Lượt đo bù trả lời hai câu: bản deploy dùng được harness hôm nay không, và công tắc nào phải bật / tắt riêng cho nó. Mỗi ô ghi trước ngưỡng; không dùng model chấm (phép kiểm bằng chương trình, cộng người đo đọc tay). Số chính (đủ ở "Đã so"):

| Ô | Model cũ trên harness hôm nay | Đọc thế nào |
|---|---|---|
| 41 câu khó | đạt 37 / 41, cả khi bật lẫn tắt hai công tắc "hết vòng" | mốc 21/11: 20–21; công tắc để tắt (bài 21) |
| câu về tỉnh khác | bị trả lời bằng kho 13 / 40 ⇒ 0 / 20 khi gắn đoạn dặn | còn hở một kiểu câu (bài 16) |
| 17 ca tính năng | 16 / 16 ca chạy được đều đạt; ca "có bão + sửa lịch" văng lỗi | lỗi thật, đã sửa (bài 31) |
| hỏi bằng ảnh, 55 tên | tên cũ 23 / 25, tên mới 29 / 30 | dùng được 55 tên (bài 26) |
| demo 10 bước · trình duyệt | 0 bước hỏng · chữ chạy dần bắt đầu ở 3,1 giây; một câu kể sai ngay sau lệnh bỏ điểm | demo đạt; câu kể sai đã sửa (bài 31) |

Đọc bảng: 37 so với 20–21 là phép so **gộp** (giữa hai lần: trần vòng 4 ⇒ 5, số lần tìm 2 ⇒ 3, kho 263 ⇒ 269 bài, thêm tính năng). Chỉ số 0 / 20 đo trên bản đã gắn đoạn dặn câu tỉnh khác; các ô khác chạy trước đó, mà đoạn dặn vào lời dặn của mọi lượt trả lời, nên lời dặn của bản deploy khác bản đã đo ở đoạn này.

## Quyết định và lý do

### 1. Vì sao giữ thư viện của OpenAI mà chạy Claude qua một lớp nối tự viết?

- **Đã chọn:** giữ thư viện OpenAI Agents SDK; viết một lớp nối khoảng 300 dòng, không thêm thư viện nào.
- **Vì sao:** chủ dự án đặt điều kiện "giữ nguyên bộ khung đang dùng" khi đổi tạm; vì sao đặt điều kiện này: chưa thấy ghi lý do. Điều thấy được: chín vai, vòng công cụ, sổ tiền và test cũ không phải sửa; mọi loại lời gọi gửi OpenAI chụp trước và sau khi có lớp nối giống nhau từng byte.
- **Cách khác:** trỏ thư viện sang địa chỉ của Bedrock nhận yêu cầu kiểu OpenAI: đã thử, Bedrock trả "không có" cho model này. Viết lại chín vai bằng thư viện của Anthropic, hoặc dùng thư viện trung gian gọi được nhiều hãng: không làm (quyết định đã ghi: giữ bộ khung).
- **Cái giá:** mọi khác biệt giữa hai hãng dồn vào lớp nối và chỉ lộ ra khi chạy thật; hai lỗi lớn ở mục trên đều nằm ở đây. Thêm hãng thứ ba thì viết thêm một lớp nối.

### 2. Vì sao mức suy luận để cao, khi ở câu thường bốn mức ngang nhau?

- **Đã chọn:** với Claude, mức cao cho mọi vai không tự đặt mức và cho hiểu lệnh sửa lịch; mức thấp, đặt cứng trong chương trình, cho lượt biểu mẫu và câu thẻ lịch.
- **Vì sao:** đo ngày 21/11. Ở hỏi đáp một lượt (66 câu), bốn mức ngang nhau và mức cao chỉ chậm hơn mức vừa khoảng 0,3 giây; chủ dự án chọn mức cao "vì không mất gì đáng kể". Ở lệnh sửa lịch khó, mức cao đúng 5 trên 6, mức thấp 2, mức vừa 0.
- **Cách khác:** mức vừa hoặc thấp ở câu một lượt: đã đo (ngang nhau). Mức vừa cho lượt tin nhiều ý: đã đo 22/11 trên một tin, nhanh hơn 8 giây nhưng bỏ sót dữ kiện kho có ⇒ bỏ ("Đã so"). Mức thấp hay vừa ở lượt có công cụ, sau khi sửa lớp nối: chưa đo.
- **Cái giá:** chậm hơn một chút và tốn token suy luận ở mọi lượt (tin dài nhiều ý: khoảng 8 giây so với mức vừa).

### 3. Vì sao Claude có những đoạn dặn riêng, và đổi model thì phải đo lại những gì?

- **Đã chọn:** lời dặn gửi gpt-6-luna giữ như trước khi có Claude, trừ một đoạn. Khi chạy Claude, chương trình nối thêm các đoạn dặn ngắn: cho xếp loại câu (bài 22), cho câu thẻ lịch, cho hiểu lệnh sửa lịch. Đoạn dặn câu tỉnh khác ở lời viết câu trả lời (chiều 23/11, bài 16) là đoạn duy nhất gắn cho cả hai model, từ tối 23/11. Claude còn đọc hai thứ riêng ("Chi tiết để tra"; nguyên văn ở phụ lục D).
- **Vì sao:** mỗi đoạn có một ca đo làm lý do. Ví dụ ở bước xếp loại câu: cùng lời dặn, gpt-6-luna xếp nhầm 0 trên 56 lượt, Claude 2 trên 56 ở mức cao. Đoạn câu tỉnh khác gắn thêm cho model cũ sau khi lượt đo bù thấy nó hở câu đó; kế hoạch đo định để chủ dự án chọn nhận giới hạn hay chữa, nhóm đã chốt chữa (bài 16).
- **Cách khác:** đoạn dặn thứ tư "nói thẳng, không lặp ý": đã thử trên 85 câu, câu dài thêm, trọng tâm 4,39 xuống 4,26 ⇒ gỡ.
- **Cái giá:** mỗi lần đổi model phải đo lại ít nhất bước xếp loại câu, lệnh sửa lịch khó, lượt có công cụ, độ dài và điểm câu trả lời (model cũ: quyết định 4); hãng mới thì thêm năm chỗ cách gọi hay khác nhau ("Chi tiết để tra").

### 4. Vì sao lượt đo bù chỉ có ít ô, mỗi ô một lượt, và bỏ ô 12 vai?

- **Đã chọn:** bảng ô ghi trước lúc 18:05 23/11, ô quyết nhiều nhất chạy trước; mỗi ô một lượt mỗi bên, chỉ lặp khi số sát ngưỡng; ô nào không đổi một quyết định thì bỏ. Bảng đó vẫn giữ ô 12 vai (người dùng mô phỏng), chạy nếu tiền thật sau bảy ô đầu dưới 1,2 USD; điều kiện đạt, nhưng sau đó nhóm đã chốt bỏ ô này.
- **Vì sao:** lời dặn "không được test quá mức" và trần tiền của chủ dự án; nhóm đặt trần cứng 2,0 USD. Lý do ghi cho việc bỏ ô 12 vai: không đổi quyết định nào, hai câu chờ đã có số từ ô khác (nhóm đã chốt). Lúc phiên tối vừa mở (19:34), chủ dự án nhắc lại: "test vừa phải, không test quá mức, không over-engineer nhé".
- **Cách khác:** bản kế hoạch đầu (12:20 23/11) nặng hơn, gọt trước khi chạy ("Chi tiết để tra"). Chấm 176 câu mẫu bằng model cũ: không thuộc lượt này.
- **Cái giá:** không biết độ ổn giữa các lượt. Món nợ ghi tối 21/11 gồm ba thứ (12 vai, 41 câu khó, sàn); lượt này trả hai, nên chưa có số "phiên đạt mục tiêu" trên model cũ (mốc 12 vai 21/11: 6, 5, 6 trên 12). 41 câu khó chưa chạy lại sau khi gắn đoạn dặn câu tỉnh khác: nhóm đã chốt chạy một bên trước khi deploy, trên bản đã đứng yên sau buổi chủ dự án tự test. Tin dài bốn ý và điện thoại chưa nhìn trên trình duyệt với model cũ. Tiền OpenAI thật: 0,66 USD, dưới trần 2,0 (cách cộng: "Chi tiết để tra").

## Nếu… thì sao

Lời báo là nguyên văn; các dòng đọc từ chương trình, chưa thử thật, trừ chỗ ghi khác (dòng lỗi tạm thời: mới có ca test với lỗi dựng sẵn, chưa gặp lỗi thật).

| Nếu | Người dùng thấy gì | Muốn hết lỗi thì ai làm gì |
|---|---|---|
| khoá Bedrock hết hạn, hoặc thiếu chỗ trỏ tới file khoá lúc bật | "Không thể tạo câu trả lời vào lúc này." ở mọi câu hỏi | hết hạn: chủ dự án làm mới file khoá; thiếu chỗ trỏ: bật lại máy chủ cho đúng (bài 36) |
| nhà cung cấp model trả lỗi tạm thời ở một lời gọi | lượt đó chậm hơn, rồi câu trả lời như thường; lần gọi lại cũng lỗi thì lời báo trên | tự gọi lại một lần: đường Claude từ 09:31 23/11, đường OpenAI từ 18:01 23/11 ("Quyết định nhỏ hơn") |
| chạy gpt-6-luna (bản deploy, hoặc máy chủ dự án đổi về) | chữ chạy dần, câu ngắn hơn; câu kiểu "ở Đà Nẵng nên đi chơi những đâu" có lúc vẫn được trả lời bằng kho (bài 16) | sửa một chữ ở dòng chọn hãng, có khoá OpenAI, khởi động lại máy chủ; đã đo bù tối 23/11 |
| đường OpenAI mà khoá sai hoặc tài khoản hết tiền | "Không thể tạo câu trả lời vào lúc này." ở mọi câu; đường báo tình trạng vẫn báo bình thường | sau khi bật, hỏi một câu thật (bài 36); đã thử với khoá giả, chưa thử với OpenAI thật |

## Dễ nhầm

- **"Đổi model chỉ là đổi tên model trong cấu hình."** Dòng cấu hình là một dòng, nhưng lần đổi sang Claude cần một lớp nối, ba đoạn dặn riêng, và lộ hai lỗi chỉ thấy khi chạy thật.
- **"Bản deploy chạy đúng như hệ thống đã đo ở máy."** Harness là một, nhưng gần như mọi số từ 21/11 đo trên Claude; model cũ chỉ có một lượt đo bù, và nó cư xử khác ở vài chỗ (chữ chạy dần, một kiểu câu tỉnh khác, ảnh lạ).

## Câu hỏi tự kiểm

<details>
<summary>1. Vì sao không trỏ thẳng thư viện sang Bedrock mà phải viết lớp nối?</summary>

Đã thử: Bedrock không phục vụ model này ở địa chỉ nhận yêu cầu kiểu OpenAI. Phải gọi theo cách riêng của Claude; lớp nối đổi qua lại để thư viện và các vai giữ nguyên.

</details>

<details>
<summary>2. Vì sao mức suy luận để cao dù ở câu thường bốn mức ngang nhau?</summary>

Ở câu thường mức cao chỉ chậm hơn khoảng 0,3 giây, mà ở lệnh sửa lịch khó đúng 5 trên 6 (mức thấp 2); chủ dự án chọn mức cao.

</details>

<details>
<summary>3. Bản deploy chạy gpt-6-luna. Hệ thống hôm nay đã được đo trên model đó chưa, và ra sao?</summary>

Một lượt đo bù tối 23/11, mỗi ô một lượt: 41 câu khó đạt 37 (mốc 21/11 trên code cũ: 20–21), demo không bước nào hỏng, 16 / 16 ca tính năng chạy được đều đạt, lộ hai lỗi thật, đều đã sửa. Phần lớn các ô chạy trước khi gắn đoạn dặn câu tỉnh khác, nên chưa có lượt 41 câu khó trên bản cuối. Ô 12 vai bị bỏ.

</details>

## Cấu hình đang chạy

*Theo cấu hình trưa 22/11/2026; ba hàng `provider`, `noi_khac_tu_choi` và hàng hai công tắc "hết vòng" đối chiếu lại lúc code đứng yên tối 23/11.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| `full_corpus_generation.provider` | `bedrock` ở máy chủ dự án; bản deploy: `openai` (tệp cấu hình đi kèm gói tải lên máy, nằm ngoài ảnh Docker; khoá OpenAI ở file khoá trên máy) | chọn hãng cho cả chín vai; `openai` là gpt-6-luna | đã chạy cả hai; harness hôm nay trên `openai`: lượt đo bù tối 23/11 ("Đã so") |
| `assistant.noi_khac_tu_choi` | bật | đoạn dặn câu tỉnh khác; từ 19:49 23/11 gắn cho cả hai hãng (trước đó chỉ Claude) | đo bật ↔ tắt trên cả hai model (bài 16) |
| `assistant.vong_cuoi_chi_viet` · `assistant.khoang_cach_trang_thai` | tắt (cả bản deploy) | hai công tắc "hết vòng", viết cho model cũ | đo bật ↔ tắt trên model cũ tối 23/11: để tắt (bài 21) |
| `full_corpus_generation.model` | `gpt-6-luna` | model của đường OpenAI; chỉ đọc khi chọn `openai` | khoá cứng trong chương trình kiểm cấu hình: có 8 giá trị cấu hình chương trình chỉ nhận đúng một giá trị, ghi khác thì máy chủ không bật (phụ lục A, B) |
| `bedrock.model` · `bedrock.region` | Claude Sonnet 5.5 · Singapore | model và vùng của Bedrock | — |
| `bedrock.max_tokens` | 128.000 | trường bắt buộc của Claude; để mức tối đa = coi như không trần | không đặt nhỏ hơn ("Quyết định nhỏ hơn") |
| `bedrock.reasoning_default` | cao | mức suy luận cho vai không tự đặt mức | đã đo bốn mức ở câu một lượt; mức vừa cho cả lượt tin nhiều ý (22/11, một tin): bỏ |
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

**Mức vừa cho cả lượt tin nhiều ý** (22/11, Claude Sonnet 5.5, sau khi sửa lớp nối). Vấn đề thật: tin dài nhiều ý chờ 25–34 giây (bài 34). Cách thử: không sửa chương trình; trong tiến trình đo, mọi lời gọi model của lượt tin nhiều ý (kể cả lời gọi quyết định tìm thêm) chạy mức vừa, lượt một ý không đổi. Bộ câu: MỘT tin gia đình bốn ý (tổng vé Đại Nội + Lăng Tự Đức cho cả nhà, bà có được giảm không, điểm nào khác ít bậc kèm giá và giờ), 6 lượt. Mốc: 6 lượt mức cao của đúng tin đó, cùng bản chương trình, chạy trước khoảng một giờ (lượt 2 của phép đo thẻ nơi, bài 23). Tiêu chí ghi trước khi chạy; phiên đo chấm chữ.

| Điều ghi trước | Mức cao (mốc) | Mức vừa | Kết |
|---|---|---|---|
| trung vị thời gian cả lượt ≤ 23,3 giây (giảm ít nhất 4 giây) | 27,3 (21,7–29,4) | 19,3 (17,7–21,3) | đạt |
| tổng tiền vé đúng | 6 / 6 | 6 / 6 | đạt |
| nêu vé lẻ Đại Nội và mức giảm 50 % cho người từ đủ 60 tuổi | 6 / 6 | 6 / 6 | đạt |
| 0 dòng "chưa có" sai về giờ, vé lẻ của Cung An Định, Lăng Dục Đức, Bảo tàng Cổ vật | 0 / 6 | 1 / 6 | **trượt** |
| tổng số lần model tự tìm của 6 lượt ≤ 10 | 8 | 6 (mỗi lượt đúng 1) | đạt |
| 0 màn hình lỗi · nêu ít nhất 1 điểm ít bậc khác kèm giá và giờ | 0 · 6 / 6 | 0 · 6 / 6 | đạt |
| *(ngoài tiêu chí)* nêu "trẻ dưới 7 tuổi miễn phí" (kho có) | 6 / 6 | 3 / 6 | — |

Đọc bảng: mức vừa nhanh thật — cả 6 lượt nhanh hơn trung vị 26,9 giây của 12 lượt mức cao cùng tin trong ngày, nên khoảng 8 giây không phải dao động. Nó trượt một điều ghi trước: một lượt ghi chưa có giá vé riêng của Bảo tàng Cổ vật rồi tự nêu giá ngay trong ngoặc. Chỗ nặng hơn nằm ngoài tiêu chí: ba lượt nói kho không có vé cho bé dưới 7 tuổi, trong khi kho có và tin hỏi thẳng tổng tiền cho nhà có bé. Gốc đọc từ sổ vết: ở mức vừa model chỉ tự tìm đúng một lần; lượt nào câu tìm đó không nhắc trẻ em thì đoạn "dưới 7 tuổi miễn phí" không vào ngữ cảnh, và model không tìm bù. Điều "số lần tìm không tăng" đạt chính vì model tìm ít hơn mức cần. Khoảng 8 giây bớt được gồm ba phần không tách được: bớt lần tìm thứ hai ở các lượt mức cao có tìm hai lần, viết ngắn hơn (trung vị 2.028 so với 2.257 ký tự), và ít token suy luận hơn.

Đã chọn: bỏ hẳn theo tiêu chí ghi trước, không thử lại (nhóm đã chốt). Giới hạn: một tin, 6 lượt mỗi bên; mốc không chạy xen kẽ; chưa đo tin nhiều ý kiểu khác, mức thấp, hay mức vừa kèm một vế tìm bù cho dữ kiện còn thiếu (bài 23, "Đã so" dòng 14).
**Các thứ đã thử với Claude ngày 21/11 mà không đưa vào:** đoạn dặn "nói thẳng" (gỡ, xem quyết định 3); cho gọi công cụ 8 vòng thay 4, tìm kho 4 lần thay 2 (thước 28 và 28 trên 29, không đổi; lúc đó trần là 2 lần tìm, 4 vòng — từ 14:47 ngày 22/11 là 3 và 5, mở cùng hai thay đổi ở khâu tìm, bài 21); trả lại phần suy nghĩ giữa các vòng công cụ (24 trên 24 cả hai bên); đệm lời dặn (không nhanh hơn).

**Lượt đo bù trên model cũ** (gpt-6-luna qua đường OpenAI, harness của nhánh chính tối 23/11; 18:10–19:44 23/11). Vấn đề thật: bản deploy chạy model cũ, mà mọi thứ mở từ tối 21/11 chỉ được đo trên Claude. Hai câu chờ: (a) bản deploy dùng được harness hôm nay không, công tắc nào bật / tắt riêng cho nó; (b) giới hạn nào phải ghi trước deploy. Cách làm: một cây chương trình tạm, chỉ dòng chọn hãng đổi sang `openai`; bảng ô và ngưỡng ghi trước khi gọi OpenAI lần nào (ô câu tỉnh khác ghi trước lúc 19:33, trước khi chạy); mỗi ô một lượt; người chấm là phép kiểm bằng chương trình ("đạt máy": không lỗi, không chạm trần, từ chối đúng / sai như mong đợi, có đủ chuỗi phải có) cộng người đo đọc tay, không dùng model chấm. Mốc là số của chính model cũ ngày 21/11, trên code cũ (4 vòng, 2 lần tự tìm, kho 263 bài). Bản chương trình của từng ô: năm ô đầu (chạy được, sàn, hai công tắc, ca tính năng, ảnh) trên nhánh chính lúc 18:10; demo trên bản 18:59; trình duyệt trên bản 19:35 (đã có bản sửa lỗi văng); ô câu tỉnh khác sau đoạn dặn trên bản gắn đoạn dặn (19:36). Không ô nào chạy trên bản cuối 20:14, vốn có thêm đoạn dặn đó và bản sửa lượt kế sau lệnh sửa lịch.

| Ô | Đo gì · bao nhiêu lượt · đường nào | Kết quả | Mốc | Theo ngưỡng ghi trước |
|---|---|---|---|---|
| chạy được không | bốn file test cần khoá OpenAI; 3 lượt qua máy chủ (một câu hỏi, một lượt xếp lịch, một lệnh sửa lịch) | bốn file đạt; 3 lượt 0 lỗi; lượt hỏi đáp chữ chạy dần thành 41 mảnh, 2–7 giây. Lần chạy đầu đỏ hai ca do người đo dựng lệnh sai (cây tạm còn chọn Bedrock); sửa lệnh thì đạt | — | đạt ⇒ đi tiếp |
| sàn + câu tỉnh khác (trước khi gắn đoạn dặn) | câu đối chứng "Từ Huế vào Hội An…" × 20 mỗi bên, gọi thẳng lõi; 17 ca phải từ chối × 1 mỗi bên, qua máy chủ | bị trả lời bằng kho: tắt 6 / 20, bật 7 / 20 (hai công tắc "hết vòng"); ca phải từ chối: tắt phạm 1 (chính câu đối chứng qua máy chủ), bật 0 | 21/11: 5 / 15 | công tắc không làm hở thêm (+1, ngưỡng +3). Mức hở ≈ một phần ba: kế hoạch để chủ dự án chọn nhận giới hạn hay chữa; nhóm đã chốt chữa bằng đoạn dặn, không hỏi (lý do ghi: điều kiện không được nới, cách chữa có sẵn; bài 16) |
| hai công tắc "hết vòng" | 41 câu khó, tắt ∥ bật, qua máy chủ (230 lượt vì nhiều mục là chuỗi) | đạt máy 37 / 41 cả hai bên; chạm trần vòng 2 ↔ 0; lỗi hiện ra 0 ↔ 0 | 21/11: đạt 20 · 21 · 21, chạm trần 5 · 6 · 7 | bên tắt chạm trần 2, chỉ hơn mức "≤ 1" một mục, trong mức dao động giữa các lượt (mốc 21/11: 5 · 6 · 7) ⇒ để tắt (bài 21) |
| 17 ca tính năng mở từ 21/11 | mỗi ca một lượt, qua máy chủ; 15 ca có đường chương trình rẽ theo model + 2 chuỗi soạn trước (thêm điểm sang khu khác; bỏ hoạt động tối rồi trả lời "để trống") | 16 ca chạy được: đạt máy 16 / 16, 0 chạm trần, 0 chữ hiện rồi bị thay hay xoá; ca "có bão + bỏ điểm" văng lỗi | — | ca an toàn hỏng ⇒ sửa trước deploy (bài 31) |
| hỏi bằng ảnh, 55 tên | 76 ảnh × 1 + 18 ảnh "giống mà không phải" với danh sách 42 tên | tên cũ 23 / 25, tên mới 29 / 30; ảnh ngoài danh sách bị gán tên 7 / 10 | ngưỡng: tên cũ ≥ 22, tên mới ≥ 80 % | đạt ⇒ dùng 55 tên (bài 26) |
| demo 10 bước | × 1, qua máy chủ | 0 bước hỏng (máy kiểm), đọc tay 10 / 10 đúng; 1,7–7,7 giây mỗi lượt | 21/11: 0 / 10 lần có bước hỏng | đạt |
| câu tỉnh khác, sau khi gắn đoạn dặn | câu đối chứng × 20 + mặt trái (đường đi Hội An, món mang tên nơi khác bán tại Huế, rìa Huế), chỉ bên bật, gọi thẳng lõi | câu đối chứng 0 / 20; còn hở "đi chơi ở Đà Nẵng" 1 / 5 · mặt trái: câu "mì Quảng ở Huế" bị từ chối 2 / 2 (bên tắt 1 / 2 — model cũ vốn chập chờn ở câu này) | bên tắt cùng buổi: 13 / 40 | đạt ở câu đo chính; một hàng giới hạn (bài 16) |
| trình duyệt | máy chủ tạm, một lượt Playwright, 19:37–19:42 | chữ chạy dần đọc được (bắt đầu 3,1 giây, dài dần tới 4,5 giây, không lần nào bị thay); ca "có bão + bỏ điểm" sau bản sửa: đúng; thẻ ảnh một tên đúng; 0 lỗi console; một câu kể sai ngay sau lệnh bỏ điểm, đã sửa (bài 31) | — | bản sửa lỗi văng đạt trên lượt thật |
| 12 vai | — | không chạy | 21/11: 6 · 5 · 6 / 12 phiên | bảng ghi trước: chạy nếu tổng tiền sau bảy ô dưới 1,2 USD (đạt); sau đó nhóm đã chốt bỏ: không đổi quyết định nào |

Đọc bảng: số "0 / 20" đo trên bản có đoạn dặn câu tỉnh khác; số "37 / 41", 16 / 16 ca tính năng và demo đo trên cây 18:10 (demo: 18:59), trước khi đoạn dặn được gắn cho đường OpenAI và trước hai bản sửa tối 23/11. Đoạn dặn vào lời dặn của mọi lượt trả lời, nên 41 câu khó chưa được đo lại trên đúng bản sẽ deploy; nhóm đã chốt chạy ô này một bên trước khi deploy, trên bản đã đứng yên sau buổi chủ dự án tự test (chưa chạy). Cấu hình công tắc như bản deploy. Mỗi ô chỉ một lượt; ở câu đối chứng, chênh 6 ↔ 7 trên 20 giữa tắt và bật là nhiễu (mức nền khoảng một phần ba). Bước nhảy 20–21 ⇒ 37 là gộp nhiều thay đổi từ 21/11, không quy cho một thứ. Ô câu tỉnh khác bên bật không chạy lại bên tắt: dùng số cùng buổi của ô sàn, vì từ cây đó tới bản có đoạn dặn đường hỏi đáp không đổi. Đã chọn: bản deploy dùng harness hôm nay, hai công tắc để tắt, đoạn dặn câu tỉnh khác gắn cả đường OpenAI, danh sách ảnh 55 tên, lỗi văng sửa trước deploy (nhóm đã chốt). Giới hạn: một lượt mỗi ô; 41 câu khó chưa chạy lại sau khi gắn đoạn dặn câu tỉnh khác cho đường OpenAI; không có người dùng thật; tính năng không có ca đại diện thì không được chạm; tin dài bốn ý, bản in, điện thoại chưa nhìn trên trình duyệt với model cũ.

## Quyết định nhỏ hơn

**Vì sao chấp nhận chữ tới một lần với Claude?** (Tới 20:22 23/11 là quyết định 3 của nửa để hiểu; chuyển xuống đây để giữ độ dài khi thêm lượt đo bù.)

- **Đã chọn:** gọi Claude trọn một lần, gửi cả câu trả lời một lần. Trong lúc chờ, dòng trạng thái của thẻ chờ (bài 5) đổi qua "Đang hiểu câu hỏi…", "Đang tìm trong kho…", rồi đứng ở "Đã tìm trong kho, đang chuẩn bị câu trả lời…" cho tới khi cả câu hiện ra ("Chi tiết để tra").
- **Vì sao:** bộ khoá Bedrock bị từ chối khi xin chữ chạy dần; khi đổi tạm, chủ dự án ghi "không cần stream thật"; ngày 22/11 chủ dự án gác việc cấp quyền AWS tới khi tự xem lại (bài 5).
- **Cách khác:** xin thêm quyền và viết đường chữ chạy dần: chưa làm; ước (chưa đo) chờ tới chữ đầu từ khoảng 13 giây còn 5,5–6 giây. Bản deploy chạy gpt-6-luna nên có chữ chạy dần sẵn (lượt trình duyệt 23/11: chữ bắt đầu ở 3,1 giây).
- **Cái giá:** thẻ chờ đứng ở bước đó khoảng 10 giây ở lượt đứng giữa (bài 34); lợi của "hiện trước, kiểm sau" (bài 6) mất, nên từ 15:42 22/11 ở lượt hỏi đáp về Huế trong ô chat chữ được giữ tới khi qua bước kiểm nguồn (bài 6, quyết định 4; đã nhìn trên trình duyệt 22/11).

**Vì sao không đặt trần số token model được viết ra?**

- **Đã chọn:** không đặt trần ở lời gọi nào. Với Claude, trần là bắt buộc nên gửi mức tối đa của model; không vai nào hạ được.
- **Vì sao:** chủ dự án quyết ngày 19/11 ("chất lượng trước, tiền và tốc độ sau"). Lý do ghi trong chương trình: trần tính cả token suy luận, và đã cắt một lời gọi xếp loại câu khi model nghĩ hết 512 trên 512 token. Rào còn lại: hạn 45 giây mỗi lượt, trần số vòng công cụ.
- **Cách khác:** trần 512 token như trước 19/11: đã dùng, đếm 3.974 lần gọi thì 2 lần chạm trần, cả hai ở bước xếp loại câu.
- **Cái giá:** chỉ hạn giờ chặn một câu quá dài. Thực tế lời gọi dài nhất trên 85 câu viết 684 token (21/11).

**Vì sao người chấm của bộ đo đổi sang chính model đang chạy?** Chủ dự án quyết tối 21/11 khi gác gpt-6-luna: mọi phép đo chỉ chạy trên model đang chạy, kể cả người chấm. Cái giá ghi kèm quyết định: người chấm cùng họ với model viết có thể chấm dễ hơn, và số chấm bằng người chấm mới không so thẳng với số cũ (24/10–19/11 Claude chấm chính trên file đã che tên, gpt-6-luna chấm phụ một lần; ban ngày 21/11 gpt-6-luna chấm — bài 19); cần một lượt mốc mới.

**Vì sao lời gọi model gặp lỗi tạm thời phía nhà cung cấp được gọi lại đúng một lần?**

- **Đã chọn:** từ 09:31 23/11, khi Amazon Bedrock trả một lỗi tạm thời phía máy của họ cho một lời gọi model, lớp nối chờ 1 giây rồi gửi lại đúng lời gọi đó một lần. Lần hai được thì lượt chạy tiếp như thường; lần hai vẫn lỗi thì người dùng thấy "Không thể tạo câu trả lời vào lúc này." và nút "Thử lại" như trước. Không gọi lại khi khoá bị từ chối hay hết hạn, khi quá hạn mức, khi yêu cầu sai, khi rớt mạng hay hết giờ.
- **Vì sao:** hai lượt thật đã gặp loại lỗi này, không phụ thuộc câu hỏi: một lần ở lần viết cuối của một tin bốn ý sáng 23/11 (lượt kế, 26 giây sau, bình thường), một lần ở một lượt đo 22/11; khoảng 1 trên 500 lượt (ước từ hai lần gặp). Trước đó lớp nối không gọi lại, nên người dùng thấy màn "Thử lại" cho một lỗi tự hết. Các lỗi kia không gọi lại vì gọi lại không chữa được (khoá, hạn mức), hoặc chưa thấy ở lượt thật (rớt mạng), hoặc làm người dùng chờ gấp đôi (hết giờ) — lý do ghi trong chương trình.
- **Cách khác:** gọi lại cả khi hết giờ: không làm, theo lý do trên. Gọi lại hơn một lần: không làm; chưa thấy ghi lý do. Điều thấy được: ca test khoá đúng "hai lỗi liền thì không có lần gọi thứ ba".
- **Cái giá:** lượt đó chậm hơn. Lời gọi lỗi tự nó có thể đã mất nhiều giây (lượt thật sáng 23/11: khoảng 15 giây rồi mới báo lỗi), nên có thể chờ gần gấp đôi, tin dài tới khoảng 50 giây (phiên đo tính từ sổ vết). Bằng chứng mới là ca test với phản hồi dựng sẵn (lỗi rồi được; hai lỗi liền; các lỗi không gọi lại; đường ô chat không phát chữ hai lần); chưa thấy chạy trên một lỗi thật, vì không ép được nhà cung cấp trả lỗi. Mỗi lần gọi lại, sổ máy chủ ghi một dòng để đếm tần suất về sau.

**Trên đường OpenAI (bản deploy), gọi lại một lần khác đường Claude ở đâu?** (Có từ 18:01 23/11; đặt cạnh mục trên, không lặp phần chung.)

- **Đã chọn:** một lớp mỏng quanh model OpenAI của thư viện gọi lại đúng lời gọi hỏng một lần khi OpenAI trả lỗi phía máy của họ hoặc rớt kết nối; gọi lại ngay, không chờ. Không gọi lại khi hết giờ, khi khoá sai, khi hết hạn mức hay hết tiền. Ở đường chữ chạy dần, chỉ gọi lại khi lỗi tới ngay lúc mở yêu cầu, trước mọi tín hiệu từ OpenAI; một khi luồng đã bắt đầu (kể cả trước chữ đầu), lỗi đi ra như cũ. Mọi lời gọi hỏng để lại một dòng sổ máy chủ ghi loại lỗi và mã lỗi (trước đó sổ chỉ ghi tên một lỗi chung, không biết là lỗi gì). Yêu cầu gửi model không đổi.
- **Vì sao:** ghi trong chương trình: lưới cho ngày demo, không phải chữa lỗi đang gặp (phiên đo đếm 0 lỗi nhà cung cấp trên 2.169 lượt thật trước 21/11); thư viện được dựng để không tự gọi lại, vì cách gọi lại sẵn có của nó gọi lại cả khi hết giờ và khi hết hạn mức. Không gọi lại khi luồng đã bắt đầu, vì gọi lại lúc đó là phát trùng chữ người dùng đã thấy (lý do ghi trong chương trình).
- **Cách khác:** dùng cách gọi lại sẵn có của thư viện: không làm, theo lý do trên. Chờ 1 giây như đường Claude: chưa thấy ghi lý do. Điều thấy được: chương trình gọi lại ngay.
- **Cái giá:** lỗi kết nối tới chậm thì lượt đó có thể chờ gần gấp đôi rồi mới ra kết quả hoặc hết giờ (hạn 45 giây chung của lượt); lần thử hỏng chỉ để lại dòng sổ, không có mục trong bảng đếm lời gọi của lượt. Bằng chứng là ca test với lỗi dựng sẵn; lượt đo bù tối 23/11 (hơn 1.400 lời gọi model ở năm ô đầu) không gặp lời gọi hỏng nào, nên chưa thấy chạy trên lỗi thật.

## Giới hạn đã biết

- **Đổi tạm, chưa có quyết định giữ lâu dài** ở máy chủ dự án; bản deploy chạy gpt-6-luna. Tới tối 23/11 các tính năng mở từ tối 21/11 chưa đo trên gpt-6-luna; nay có một lượt đo bù, mỗi ô một lượt, phần lớn chạy trước khi đoạn dặn câu tỉnh khác được gắn cho đường OpenAI ("Đã so"); 41 câu khó chưa chạy lại sau đoạn dặn đó.
- **Giới hạn riêng của đường model cũ, đo được tối 23/11:** câu "đi chơi ở <tỉnh giáp Huế>" có lúc vẫn được trả lời bằng bài về nơi giáp ranh (1 / 5; bài 16) · câu nhiều ý có thể chạm trần vòng và nhận câu từ chối (2 / 41, hai công tắc để tắt; bài 21) · ảnh nội thất một bảo tàng khác có thể bị đoán là một nơi trong danh sách (1 / 1 ảnh; bài 26). Chưa đo trên model cũ: 12 vai, tin dài bốn ý và điện thoại qua trình duyệt, độ ổn giữa các lượt.
- **Mức thấp ở lượt có công cụ chưa đo lại** sau khi sửa lớp nối; mức vừa mới đo lại trên MỘT tin dài nhiều ý (bỏ sót dữ kiện, "Đã so"), các lượt có công cụ khác chưa đo lại.
- **Chữ tới một lần**, chờ trắng có lượt quá 15 giây (bài 34).
- **Câu thẻ lịch của Claude** có thể ghép sai ý của một câu nguồn dài (một mục, 12 lượt: sai 1, nói lỏng 4); bộ kiểm của chương trình không bắt được loại lỗi này (bài 29).
- **Phụ thuộc một khoá tạm** do chủ dự án giữ; hết hạn là ô hỏi đáp ở máy chủ dự án ngừng cho tới khi làm mới. Không có model dự phòng tự chuyển: đổi sang gpt-6-luna là người sửa một dòng cấu hình rồi khởi động lại (tài khoản OpenAI có tiền từ khoảng 17:58 23/11). Bản deploy phụ thuộc khoá OpenAI theo cùng cách.
- **Người chấm của bộ đo nay là chính model đang chạy** (từ 21/11 tối); người chấm cùng họ với model viết có thể chấm dễ hơn (quyết định nhỏ ở trên).

## Chi tiết để tra

- Tốc độ đo thẳng ở Bedrock (không qua sản phẩm, 21/11): xếp loại câu 0,8–0,9 giây; trả lời khoảng 6.800 token vào, 400 ra: 3,5–3,9 giây; lượt có suy luận thật và khoảng 2.000 token ra: 15–20 giây; 0 lần bị giới hạn tần suất trong 46 lời gọi.
- Tắt hẳn suy luận ở Claude: hai cách "tắt" thẳng đều bị từ chối; lớp nối dùng chế độ "chỉ nghĩ giữa các lần gọi công cụ", đo được 0 token suy luận 6 trên 6 lần.
- Ép model gọi đúng một công cụ: Claude chỉ nhận "tự chọn" hoặc "không công cụ", nên lớp nối không ép.
- Ở vòng mà mọi công cụ đã bị ẩn (hết lượt tìm), ép khuôn làm Claude viết rác vào khuôn (tên công cụ, chữ giữ chỗ, rỗng) 14 trên 22 lần; chỉ đưa công cụ "trả lời": đúng câu từ chối 20 trên 22, 0 rác.
- Lời lỗi của lớp nối không mang thân phản hồi của Amazon (thân đó có mã tài khoản); chỗ đọc file khoá lỗi chỉ ghi tên loại lỗi, không ghi đường dẫn.
- Tối 21/11 chủ dự án gác hẳn gpt-6-luna vì tài khoản OpenAI hết tiền; từ đó tới chiều 23/11 mọi phép đo chỉ chạy trên Claude. Lời chủ dự án lúc đó: "…một harness chỉ đo trên sonnet, sau này bảo vệ có thể sẽ dùng luna, nhưng hiện tại do đã hết tiền bên openai nên cứ dùng tạm sonnet đã nhé, lúc bảo vệ có thể dùng luna". Khoảng 17:58 23/11 anh nạp tiền OpenAI; lượt đo bù chạy 18:10–19:44 cùng tối. Hệ thống ở máy chủ dự án vẫn chạy Claude.
- Khoá Bedrock hết hạn, kể trọn (tới 20:22 23/11 là đoạn mở đầu mục "Nếu… thì sao"): khoá là khoá tạm do chủ dự án giữ; hết hạn giữa buổi thì máy chủ vẫn chạy, đường báo tình trạng vẫn báo đủ (bài 6); mọi câu hỏi nhận "Không thể tạo câu trả lời vào lúc này." và nút "Thử lại", bấm lại vẫn vậy. Không có cơ chế tự làm mới khoá (chủ dự án dặn không xây); chương trình đọc lại file khoá ở mỗi lần gọi, nên làm mới file xong là hỏi được ngay, không cần khởi động lại máy chủ.
- Một model viết làm chín loại việc: mỗi vai có lời dặn, khuôn đầu ra, công cụ riêng, nhưng không có cách cho Claude viết câu trả lời mà gpt-6-luna xếp loại câu. Với Claude, chương trình luôn gửi rõ một mức suy luận, vì không gửi gì thì Claude tự nghĩ cỡ mức cao; mức cao dùng cho xếp loại câu, trả lời, trợ lý, trò chuyện, mục web, nhận ảnh và hiểu lệnh sửa lịch. Lệnh sửa lịch khó: 3 lượt mỗi lệnh. Mỗi chỗ khác nhau của lớp nối đều được đo thật trước khi viết.
- Quyết định 3, ba đoạn dặn riêng của Claude: xếp loại câu (địa bàn Huế gồm cả vùng ven), câu thẻ lịch (một hai câu, giữ con số đi đúng vật), hiểu lệnh sửa lịch. Xếp nhầm ở mức vừa: 4 trên 56. Năm chỗ cách gọi hay khác nhau giữa các hãng: khuôn có ràng buộc, ép gọi công cụ, quyền chữ chạy dần, cách tắt suy luận, cách đếm token.
- Bảng hai model, dòng độ dài: 85 câu đầu bộ câu mẫu, không lọc theo loại câu.
- Tiền mỗi câu của Claude gấp khoảng 37 lần gpt-6-luna (66 câu, mức cao: 0,0146 so với 0,00039 USD): giá mỗi token gấp 20 lần, câu lại dài hơn.
- Lỗi thứ hai (câu hỏi cũ dính vào câu đang hỏi) lộ ra vì lịch sử lúc đó chỉ giữ câu hỏi, nên nhiều tin của người dùng đứng liền nhau. Claude đòi tin của người dùng và tin của trợ lý xen kẽ nhau, nên bản nối đầu gộp hai câu hỏi liền nhau làm một, và câu "bạn còn nhớ tôi tên gì" dính vào câu giá vé lượt trước. Sửa: chèn một tin giữ chỗ giữa hai câu hỏi; sau sửa 0 lỗi trên 18 lượt đo. (Tới 20:22 23/11 đoạn này nằm ở nửa để hiểu.)
- Quyết định 2, nhóm lịch giữ mức thấp: đo trên 4 kiểu lịch, ba mức cho cùng kết quả.
- Quyết định 1: phép chụp "giống từng byte" gồm mười loại lời gọi gửi OpenAI, vì vài vai có hai biến thể.
- Tiền một câu ví dụ chạy thẳng qua code sản phẩm (không qua máy chủ, 21/11): khoảng 0,018 USD trên Claude so với khoảng 0,0007 USD trên gpt-6-luna (khoảng 25 lần); lượt hỏi tiếp có tìm thêm 0,048 USD. Mức suy luận của các lượt đó: báo cáo gốc không ghi; hướng dẫn đổi model ghi "mức thấp".
- Chữ tới một lần với Claude ("Quyết định nhỏ hơn"), dòng trạng thái: ở lượt có công cụ, "Đang viết câu trả lời…" chỉ được gửi ngay trước chữ đầu, nên với Claude gần như không thấy (đã nhìn trên trình duyệt 22/11, giao diện cũ: lúc chờ chỉ một dòng "Đã tìm trong kho, đang chuẩn bị câu trả lời…", tin bốn ý 29,5 giây); trừ lượt phải viết lại: dòng đó đứng suốt lần viết lại (bài 21). Từ 23/11 dòng trạng thái nằm trong thẻ chờ, kèm tên các bài đã tìm thấy; nó không còn kèm số đoạn như "(10 đoạn)" của giao diện cũ (bài 35).
- Lớp nối, ví dụ một chỗ khác nhau: khuôn có ràng buộc kiểu "nhiều nhất 3 mục" bị Bedrock từ chối, nên lớp nối gỡ ràng buộc khỏi khuôn gửi đi; chương trình vẫn kiểm đủ khi nhận về.
- Lỗi "xin công cụ mãi", diễn biến: gpt-6-luna gọi công cụ xong thì viết vào khuôn; Claude thì không. Phát lại một yêu cầu đã đủ dữ liệu: viết được 0 trên 8 lần ở mỗi mức suy luận; bỏ khuôn thì 14 trên 14. Bản sửa: ở lượt có công cụ, lớp nối không gửi khuôn mà thêm một công cụ nội bộ "trả lời" mang đúng khuôn đó; Claude gọi nó để nộp câu trả lời. Trên thước 29 câu làm trợ lý (bài 32): chạm trần vòng 6 xuống 0; nhóm 8 câu cần nhiều công cụ đạt 2 lên 7.
- Quyết định 3, hai thứ Claude đọc mà gpt-6-luna không đọc: mô tả của công cụ nộp câu trả lời (ở mọi lượt có công cụ) và một câu giữ chỗ trong lịch sử, đặt giữa hai câu hỏi liền nhau khi câu trả lời lượt trước không được lưu.
- Người chấm của bộ đo: 24/10–19/11 là Claude (chấm chính, đọc file đã che tên), gpt-6-luna chấm phụ một lần để đối chiếu; ban ngày 21/11, lúc đổi model viết, là gpt-6-luna; từ tối 21/11, khi gác gpt-6-luna, chấm bằng model đang chạy, và số mới không so thẳng với số cũ (bài 19).
- Lớp nối có khoảng 20 ca test bằng phản hồi dựng sẵn, không gọi mạng (20 ca đếm 21/11; 21 ca đếm 22/11; bài 38).
- Mức suy luận của gpt-6-luna: chương trình không gửi mức nào (trừ nhóm lịch, kể cả hiểu lệnh sửa lịch), tức model chạy mức vừa mặc định. Ngày 19/11 đã đo mức thấp: chất lượng không khác, nhưng một lần nói trái nguồn ở bộ câu an toàn, nên giữ mức vừa.
- Bảng hai model, tốc độ sinh chữ: khoảng 114 token mỗi giây (gpt-6-luna) và 101 (Claude).
- Quyết định 2, thêm hai điều: ở lượt có công cụ thời tiết, ngày (12 lượt), mức vừa và thấp chạm trần vòng 8–9 lượt, mức cao 1 — số đo **trước** khi sửa lớp nối, có thể đã không còn đúng. Cách khác "hạ mức chỉ ở lần viết cuối của tin dài": không làm (bài 34).
- Quyết định 3, ví dụ thứ hai: ở lệnh sửa lịch sau đoạn dặn riêng của Claude, 27 trên 27 lượt đúng ý.
- Lời chủ dự án lúc nạp tiền OpenAI (khoảng 17:58 23/11): "à tôi vừa nạp tiền vào api cho luna rồi nhé, các bạn có thể dùng lại gpt 6 luna với harness mới nhé, à lưu ý là không được test quá mức nhé, trần các bạn chỉ là 2$ đến 2,5$".
- Quyết định 4, bản kế hoạch đầu (12:20 23/11): thêm một lớp gác nữa cho cùng hai công tắc, lặp nhiều lần hơn, 36 ca tính năng; bản đó còn ghi con số "phiên đạt mục tiêu" của chính bản sẽ deploy là một quyết định chờ. Tiền OpenAI thật, cộng từ sổ máy chủ và file kết quả: 0,65 USD cho các ô, 0,66 USD khi cộng ba lần chạy lại một chuỗi sau bản sửa lượt kế.
- Lượt đo bù, lỗi văng ở ca "có bão + sửa lịch": lỗi nằm ở chương trình dùng chung, lộ ra vì model cũ gọi công cụ thời tiết ở lượt đó, Claude thì không.
- Hai tình huống không còn trong bảng "Nếu… thì sao": phần viết của một lượt quá 45 giây ⇒ cùng lời báo "Không thể tạo câu trả lời vào lúc này."; người dùng bấm "Thử lại"; đã gặp 1 trong 156 lượt người dùng mô phỏng của Claude tối 21/11, lúc hai model chạy cùng lúc (bài 34). Đổi sang model thứ ba ⇒ chưa biết người dùng thấy gì; hãng mới thì viết lớp nối mới, đo lại các mục ở quyết định 3.

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
- Chữ tới một lần, "không cần stream thật": `bedrock_model.py` (`stream_response`), `HIEN_TRANG.md` mục 4 gạch 09:41; ước 5,5–6 giây: `THOI_GIAN_DI_DAU.md` mục 3 hàng A [ước, chưa đo]. Bốn dòng trạng thái: `frontend/src/chat.jsx` `STATUS_TEXT` [code]; từ 10:00 23/11 hiện trong thẻ chờ `frontend/src/song/Song.jsx` `ChoSong` (`dongBuoc`, không kèm `n_sources`) [code].
- Đoạn dặn riêng Claude: `backend/llm/full_corpus_prompt.py` (hằng `SONNET_*`), hàm `kem` trong `generator_openai_full_corpus.py`; số 0/56, 2/56, 4/56: `data/thu_bedrock_2026-11-21/c_harness/RA_HARNESS.md` dòng 22 [riêng tư]; 27/27: `guides/DOI_MODEL_VIET.md` mục 1; đoạn "nói thẳng" gỡ: cùng chỗ.
- Bảng giá: `backend/llm/pricing.py` (`PRICES_PER_M`) [code]. Tiền 0,00039 ↔ 0,0146 USD: `KET_QUA_2A.md`; 0,018 ↔ 0,0007: `report_agent/2026-11-21/b_bedrock_sonnet.md` mục 3 dòng 44 (hàng "LƯỢT THẬT qua code sản phẩm… (không qua server)", không ghi mức suy luận; mục 3b "qua giao diện" là lượt khác, mức `low`, không có số 0,018 ↔ 0,0007); "mức `low`" và 0,048 USD: `guides/DOI_MODEL_VIET.md` dòng 186 [chép, mở 16:52 22/11; sửa theo biên bản `data/hoc_cung_D/kiem/phan_xu_va_cap_nhat_15h42.md` Phần 3 dòng 3 — riêng tư]. "Không lọc theo loại câu" (thay "đủ các loại câu", suy luận của người sửa trước): biên bản cùng file, Phần 1 bảng hai dòng 12. Trình duyệt 22/11: `bai_hoc/VIEC_MOI_XONG.md` mục 44 [chép].
- Giữ một phiên chụp 10 loại lời gọi giống từng byte: `guides/DOI_MODEL_VIET.md` mục 1; `report_agent/2026-11-21/b_bedrock_sonnet.md` dòng 75 [người thứ hai kiểm].
- Lời báo "Không thể tạo câu trả lời vào lúc này.": `backend/api/routes/chat.py` (`GENERATION_FAILURE_MESSAGE`); mọi lỗi Bedrock là `GenerationError`: lớp `BedrockError` [code]. Tình huống khoá hết hạn [đọc từ chương trình, chưa thử thật]; đọc lại file khoá mỗi lần gọi: `BedrockClaudeModel._invoke` [code]. 12,6 giây là lời gọi dài nhất trên thước 29 câu (`guides/DOI_MODEL_VIET.md` mục 3), không phải lượt dài nhất.
- Cách đổi về luna: `guides/DOI_MODEL_VIET.md` mục 2. Đường luna khoá cứng `gpt-6-luna`: cùng trang mục 6.
- Thứ đã thử mà không đưa vào: `bai_hoc/VIEC_MOI_XONG.md` mục 23 bảng cuối.
- Người chấm đổi sang model đang chạy, có thể chấm dễ hơn; không model dự phòng: `HIEN_TRANG.md` mục 4 gạch 21:43 [chép].
- Lượt chạm 45 giây: `data/thu_bedrock_2026-11-21/do/moc_12vai/KET_QUA_MOC.md` (r1, V01 lượt 3) [riêng tư]. Dòng trạng thái ở lượt có công cụ: `backend/llm/assistant.py` (`pending_generating`, "đang viết" phát ngay trước chữ đầu) [code].
- Đợt 23/11/2026. Gọi lại một lần khi lỗi tạm thời: commit `f5cf10b5` (gộp `cb711bc4` 09:31 23/11/2026) — `backend/llm/bedrock_model.py` (`MA_GOI_LAI` = 500 / 502 / 503 / 504, `CHO_GOI_LAI_GIAY = 1.0`, khối gọi lại trong `_invoke`, ký lại vì chữ ký mang giờ gửi, dòng sổ `bedrock_goi_lai`; chú thích trên `MA_GOI_LAI`: hai lượt thật, không gọi lại 4xx / lỗi mạng / hết giờ và lý do); ca test `backend/tests/test_bedrock_model.py` (`test_a_5xx_from_bedrock_is_retried_once_and_the_answer_comes_back`, `test_a_second_5xx_is_not_hidden_and_4xx_is_never_retried`, `test_a_retried_5xx_on_the_stream_path_sends_the_text_once`) [code; không chạy test]. "Khoảng 1 / 500 lượt", "khoảng 15 giây rồi mới trả lỗi", "có thể chờ gấp đôi, tin dài tới khoảng 50 giây [phiên đo tính từ sổ vết]", "CHƯA thấy trên lỗi 5xx thật — không ép được": `guides/RUNBOOK_BAN_GIAO.md` mục 10.3 hàng "Bedrock trả lỗi 5xx thoáng qua" (sửa ở commit `6e9c1a84`) [chép, đã mở]; lời commit `f5cf10b5` [chép]. Lời báo nguyên văn: `GENERATION_FAILURE_MESSAGE` trong `backend/api/routes/chat.py` [code]. Hạ mức chỉ ở lần viết cuối: bài 34 khối Nguồn.
- Bài đã qua một lượt đối chiếu độc lập 22/11: `data/hoc_cung_D/kiem/bai_33_38.md` [riêng tư]; dòng không áp ghi ở `data/hoc_cung_D/viet/viet_33_38.md` mục "Sau lượt kiểm".

- Phép thử mức vừa cho cả lượt tin nhiều ý (đợt 21:37 22/11/2026): tiêu chí ghi trước (sáu điều + bổ sung E1–E4, mốc lượt 2 thẻ nơi 17:10 = 27,3 giây, trung vị gộp 26,9 của 12 lượt high, cách thay hai agent `assistant_agent_nhieu_y` / `assistant_history_agent_nhieu_y` trong tiến trình đo): `data/thu_bedrock_2026-11-21/b_medium_nhieu_y/luot_1/TIEU_CHI.md` dòng 4–24; số máy (19,3 giây, 1 / 6 ở điều 4, 6 lần tìm, 2.028 ↔ 2.257 ký tự, token suy luận): `KET_QUA_SO_MAY.md` dòng 3–21; bản chấm (điều 4 TRƯỢT, "dưới 7 tuổi" 3 / 6, gốc là chỉ một lần tìm): `CHAM_E.md` dòng 5–21 [riêng tư; đã chạy, phiên khác, 22/11; Claude Sonnet 5.5]. Trung vị 19,3 · 27,3, khoảng thời gian, số lần tìm 1×6 ↔ 2·1·2·1·1·1: người viết đếm lại từ `tho.jsonl` của `b_medium_nhieu_y/luot_1` và `b_x10_the_noi/luot_2` [tự đếm, 0 đồng]. "Bỏ hẳn, không thử lại": `session_prompt/Y_CHUA_THU.md` hàng ý 56 [chép]. Hai agent tin nhiều ý có thật trong code: `backend/llm/generator_openai_full_corpus.py` dòng 388–389, 568–569; mức đang chạy `reasoning_default: high`: `backend/config/settings.yaml` dòng 59 [code]. Mức thấp sau khi sửa lớp nối chưa đo: không thấy trong `Y_CHUA_THU.md`, `VIEC_DANG_MO.md`, `HIEN_TRANG.md` (grep "low", "medium", "mức thấp") [đã grep].
- Để giữ độ dài nửa để hiểu: chuyển xuống "Chi tiết để tra" câu "37 lần", câu "lịch sử lúc đó chỉ giữ câu hỏi", "mười loại lời gọi", "4 kiểu lịch", câu "tối 21/11 gác hẳn gpt-6-luna" (21:37 22/11/2026).
- Cập nhật theo bộ thay đổi mở 14:47 22/11/2026: `bai_hoc/VIEC_MOI_XONG.md` mục 42, 43; `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 (hàng "Trần tìm 3 lần / 5 vòng là khoá CHUNG cho cả hai đường model"); `backend/config/settings.yaml` [code; người viết không chạy lại]. Người chấm 24/10–19/11 là Claude (chính), gpt-6-luna phụ: `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` dòng 34 ("Judge chính là Claude (xem E1)") [chép; sửa theo bài 19]. 8 giá trị khoá: `backend/core/settings_loader.py` `validate_phase6_settings` [code, đọc 22/11].

- Đợt đầu chiều 23/11/2026 (viết khoảng 13:53, giờ `date`): quyết định 4 (nay 3) "Đã chọn" và "Cái giá". Đoạn dặn câu tỉnh khác `SONNET_NOI_KHAC` (công tắc `noi_khac_tu_choi`, "MỞ 13:11 23/11/2026"), chỉ nối khi `bedrock_model` có (`kem`, `them_noi_khac` trong `backend/llm/generator_openai_full_corpus.py`) [code]. Đường gpt-6-luna hở câu đối chứng ngày 21/11: 2 / 10 (`san_30cd_luna_x10.jsonl`) và 3 / 5 (`s2_luna_tat_x5.jsonl`) ở `data/thu_bedrock_2026-11-21/do/thuoc/r06_lap/` [riêng tư; tự đếm]. Gạch "Dễ nhầm" "ba đoạn dặn riêng" giữ nguyên: nó nói về lần đổi sang Claude ngày 21/11. `guides/DOI_MODEL_VIET.md` mục 1 vẫn ghi "ba đoạn dặn" [lệch, chưa sửa ở đó].

- Lượt áp biên bản 23/11/2026 (`data/hoc_cung_D/kiem/dot_2311_chieu_k1_kiem.md` hàng 33.1) [riêng tư]: bỏ cách gọi "đoạn thứ tư" cho đoạn câu tỉnh khác (trùng với đoạn "nói thẳng" ở "Cách khác" của quyết định 4 lúc đó, nay quyết định 3); giờ "chiều 23/11" (dòng cấu hình ghi mở 13:11, vào nhánh chính 13:28) [code].

- **Đợt cuối tối 23/11/2026 (viết 20:22–20:32, giờ `date`; code đứng yên ở `73dae1f3`, tài liệu `b5e82bec`).** Dòng Cập nhật trước: "Cập nhật 14:17, ngày 23/11/2026 · khớp hệ thống 13:41 23/11 (50 tính năng mở, 5 tắt, kho 267 bài): thêm đoạn dặn câu tỉnh khác (khác đoạn "nói thẳng" đã gỡ) · 11:13: gọi lại một lần khi nhà cung cấp lỗi tạm thời; thẻ chờ · cơ chế đọc từ chương trình và cấu hình 22/11; số đo từ các báo cáo 19/11 (gpt-6-luna) và 21/11 (cả hai model); người viết không chạy lại phép đo nào." Số tính năng 57 mở / 6 tắt: lệnh đếm của lời giao chạy trên `backend/config/settings.yaml` cây chính 20:2x 23/11 [tự chạy]; kho 269 bài / 9.533 đoạn: `session_prompt/HIEN_TRANG.md` mục 1 ("máy kiểm 19:30 23/11") [chép]. Cả bộ test 20:09: `session_prompt/HIEN_TRANG.md` mục 1 gạch "Mức kiểm hiện tại" và `session_prompt/sessions/STATUS_E.md` mục 4 [chép; bảng `data/test_rong_2026-11-22/KET_QUA_c475f5e0.tsv` không mở — bài 38 kể đủ].
- Để giữ nửa để hiểu ≤ 13.790 ký tự (trước 13.790, sau 13.787): quyết định 3 cũ (chữ tới một lần với Claude) chuyển xuống "Quyết định nhỏ hơn" (thêm một câu về chữ chạy dần của bản deploy); mục thân bài "Mức suy luận đang để cao…" gộp vào quyết định 2 (danh sách vai, câu "luôn gửi rõ một mức" chuyển xuống "Chi tiết để tra"); mục "Một model viết làm chín loại việc" gộp vào Ý chính gạch 1 (ví dụ "không cho Claude viết mà luna xếp loại" chuyển xuống); đoạn mở đầu "Nếu… thì sao" (khoá Bedrock hết hạn), đoạn "Lỗi thứ hai", năm chỗ cách gọi hay khác nhau, nội dung ba đoạn dặn riêng, "4 / 56 ở mức vừa", "3 lượt mỗi lệnh", "không lọc theo loại câu" chuyển xuống "Chi tiết để tra"; câu hỏi tự kiểm 2 cũ ("xin công cụ mãi", lặp thân bài) bỏ; quyết định 4 cũ thành 3, quyết định 5 mới thành 4.
- Hai model, hai nơi chạy; bản deploy dùng OpenAI: lời chủ dự án "đúng rồi nhé, mà deploy là sẽ dùng của openai nhé" (`data/loi_user/2026-11-23.md`, giờ ghi 11:01) [riêng tư; chép]; `session_prompt/HIEN_TRANG.md` mục 4 gạch "MODEL CỦA BẢN DEPLOY (11:01 23/11)" (một đường model `provider: openai` ở thư mục cấu hình ngoài ảnh + một khoá OpenAI) [chép]. Hệ thống ở máy chủ dự án vẫn chạy Claude: cùng trang, gạch "OPENAI ĐÃ NẠP TIỀN"; `backend/config/settings.yaml` dòng 47 `provider: bedrock` [code].
- Lời chủ dự án 21/11 ("một harness chỉ đo trên sonnet…"): `git show 678f0b16:session_prompt/HIEN_TRANG.md` gạch "21:50 21/11/2026 — MỘT HARNESS…" [chép]; nợ đo bù: `session_prompt/HIEN_TRANG.md` mục 4 gạch "MỘT HARNESS (21:50 21/11)" [chép]. Lời nạp tiền, nguyên văn tới "2,5$" (phần sau là đường dẫn trang giá, bỏ): `data/loi_user/2026-11-23.md` dòng giờ ghi 18:07, "chủ dự án gõ khoảng 17:58" [riêng tư; chép]. Trần cứng nhóm tự đặt 2,0 USD: `data/thu_bedrock_2026-11-21/do/do_bu_model_cu/KE_HOACH.md` mục 8 [riêng tư; chép].
- Lượt đo bù — kế hoạch và ngưỡng ghi trước: `data/thu_bedrock_2026-11-21/do/do_bu_model_cu/KE_HOACH.md` mục 2 (mốc 21/11: 41 câu khó 20 · 21 · 21, chạm trần 5 · 6 · 7; 12 vai 6 · 5 · 6; demo 0 / 10; R06 5 / 15), mục 4 (luật công tắc), mục 8 (bảng gọt 18:05, luật gọt, phần đã bỏ so với mục 3), mục 9 (ô câu tỉnh khác, ghi 19:33) [riêng tư; đã mở trọn]. Kết quả: `KET_QUA.md` cùng thư mục, bảng "Từng ô" và khối "PHẦN TỐI" [riêng tư; đã mở trọn; đã chạy, phiên đo]. Người viết tự đếm lại từ file thô [tự đếm, `python3 -I`, 0 đồng]: `ket_qua/gS_r06_tat_x20.jsonl` 6 / 20 và `gS_r06_bat_x20.jsonl` 7 / 20 (không từ chối và có `nguon_trich`); `ket_qua/g2b_a_r06_bat.jsonl` 0 / 20 (11 tuyến `ngoai_pham_vi`, 9 `tro_ly_hue`); `g2b_b_ngoai_tinh_bat.jsonl` B2 1 / 5; `b1c_tat.log` / `b1c_bat.log`: 37 dòng "ĐẠT" mỗi bên, bên tắt K01 và K19 kết `max_turns`; `gS_man_hinh.txt` (ca phải từ chối: trượt máy tắt T1, N1 — bật T1; T1 là kỳ vọng cũ của ca, không phải lỗi, theo `KET_QUA.md`); `gT_tinh_nang/luot.jsonl` 12 ca (C7 cuối) + `ket_qua/nhat_ky.txt` dòng "ô T (phần 2) — năm ca còn lại K1, K3, K4, T1, T2"; `ca_tinh_nang_gon.json` 17 ca; `gD_demo.log` dòng TỔNG "so_lap_co_buoc_hong": 0. Ảnh 23 / 25, 29 / 30, 7 / 10: `KET_QUA.md` ô 5 [chép]. Trình duyệt: `data/playwright_mcp/luot_2311_luna_o7/NHAT_KY.md` hàng 1, 4, 5, 6 [riêng tư; đã mở trọn; người chạy: phiên đo, chưa có người thứ hai kiểm].
- Quyết định bỏ ô 12 vai "không đổi quyết định nào": `KET_QUA.md` đầu khối "PHẦN TỐI"; `session_prompt/sessions/STATUS_E.md` mục 2 ("BỎ theo quyết định của phiên điều phối") [chép]. Liều test chủ dự án nhắc lại 19:34 ("test vừa phải, không test quá mức, không over-engineer nhé"): `data/loi_user/2026-11-23.md` [riêng tư; chép — bài không trích câu này].
- Tiền OpenAI thật 0,65 USD (các ô) và 0,66 (cộng 0,0065 của ba chuỗi chạy lại): `KET_QUA.md` dòng "Tiền OpenAI THẬT cả lượt đo bù: 0,65 USD"; `session_prompt/sessions/STATUS_E.md` mục 2; `HIEN_TRANG.md` mục 1 gạch "ĐO BÙ" ghi 0,66 [chép]. Cách cộng: `cong_tien.py` (dòng `chat_metrics` / `anh_metrics` của sổ cây tạm + file kết quả gọi thẳng lõi) [đã mở code, không chạy — sổ của cây tạm ở `/tmp/hr_e_dobu`]. "Ước ô 41 câu khó thấp hơn thật 2,5 lần (230 lượt, không phải 82)": `KET_QUA.md` dưới bảng tiền [chép; không đưa vào thân bài].
- Lỗi thật lộ nhờ model cũ (ca "có bão + bỏ điểm", `KeyError`): `KET_QUA.md` mục "Lỗi thật tìm ra"; bản sửa `5f740370` (gộp `02dd855d` 19:34) [`git show --stat`] — kể đủ ở bài 31. Câu kể sai sau lệnh bỏ điểm (một lượt trình duyệt): `NHAT_KY.md` hàng 5; bản sửa gộp `73dae1f3` — kể đủ ở bài 31 (bản trên `origin/main` `63cc7a36`, bảng "Nếu… thì sao" hàng "sau 'bỏ điểm đầu tiên của ngày 2'…") [đã mở].
- Đoạn dặn câu tỉnh khác gắn cả đường OpenAI: commit `bc167e40` 19:36, gộp `c475f5e0` 19:49 23/11 — `backend/llm/generator_openai_full_corpus.py` hàm `them_noi_khac` (nối `SONNET_NOI_KHAC` khi `noi_khac` bật, không còn qua `kem`), `from_environment` đọc `noi_khac_tu_choi` cho cả nhánh OpenAI; chú thích trên `SONNET_NOI_KHAC` trong `backend/llm/full_corpus_prompt.py` [code, đọc tối 23/11, trước 20:32]. Ba đoạn `SONNET_*` khác vẫn chỉ qua `kem` (chỉ khi có `bedrock_model`) [code].
- Hai công tắc "hết vòng" để tắt cho cả bản deploy: `backend/config/settings.yaml` dòng 89–90 (`false`) [code]; `HIEN_TRANG.md` mục 1 gạch "ĐANG TẮT (6)" [chép].
- Gọi lại một lần trên đường OpenAI: commit `cf0c79fa` 17:48, gộp `06eaaa7d` 18:01 23/11 — `backend/llm/openai_goi_lai.py` (chú thích đầu file: hai việc, lý do không gọi lại khi hết giờ / 4xx, `max_retries=0`, "0 lỗi nhà cung cấp / 2.169 lượt thật trước 21/11 ⇒ lưới cho ngày demo"; `goi_lai_duoc`, `OpenAIGoiLaiModel.get_response` / `stream_response` với `da_phat`; không có lệnh chờ); `generator_openai_full_corpus.py` dòng 356 (`OpenAIGoiLaiModel` khi không có `bedrock_model`), dòng 515 `max_retries=0` [code]. Chờ gần gấp đôi khi lỗi kết nối chậm, lần thử hỏng không vào bảng đếm lời gọi: `guides/RUNBOOK_BAN_GIAO.md` mục 10.3 hàng "Đường OpenAI (`provider: openai` — bản deploy)…" (thêm `04153fde` 17:57) [chép]; hàng đó còn ghi "chưa có lượt thật — tài khoản OpenAI đang hết tiền" (đã cũ, xem báo cáo). 0 lời gọi hỏng trong các ô đo; 1.411 lời gọi model ở ô 1–5: `KET_QUA.md` bảng tiền (17 + 130 + 142 + 940 + 182) và dòng "Lời gọi hỏng" [chép, người viết cộng].
- Khoá OpenAI sai / hết tiền ⇒ lời báo ở mọi câu, đường báo tình trạng vẫn `ok`: `deploy/docker/README.md` dòng 114 và dòng 180 (thử với khoá GIẢ, lỗi là lỗi kết nối; "khoá sai thật / hết tiền cho CÙNG câu báo theo code, chưa chạy với OpenAI thật") [chép, đã mở]; mọi lỗi model là `GenerationError` ⇒ `GENERATION_FAILURE_MESSAGE` (`backend/api/routes/chat.py`) [code].

- **Lượt áp biên bản kiểm độc lập tối 23/11/2026 (21:03–21:16, giờ `date`)** — biên bản `data/hoc_cung_D/kiem/dot_2311_cuoi_k1_do_bu_kiem.md` mục 33.1 [riêng tư]; báo cáo `data/hoc_cung_D/viet/dot_2311_cuoi_a1_ap_do_bu.md` [riêng tư]. Dòng Cập nhật trước: "Cập nhật 20:32, ngày 23/11/2026 · khớp hệ thống lúc code đứng yên tối 23/11 (…) · thêm lượt đo bù trên model cũ, gọi lại một lần trên đường OpenAI · cả bộ test 20:09 … · mốc cũ: Nguồn." Người viết tự mở lại nguồn của mỗi hàng: cây của từng ô — `KET_QUA.md` dòng 3 (ô 1–5 trên `0ce3fe4f`, main 18:10; commit 18:03), dòng 47 (demo `f6ab7daa` 18:59), 48 (ô 2b nhánh `bc167e40` 19:36), 49 (trình duyệt `a372742b` 19:35); đoạn dặn vào main `c475f5e0` 19:49, bản cuối `73dae1f3` 20:14 (`git log 0ce3fe4f..73dae1f3`); đoạn dặn nối vào `tra_loi` ⇒ `answer_agent`, `assistant_instructions` (⇒ bản lịch sử), `ny` (bản nhiều ý): `backend/llm/generator_openai_full_corpus.py` dòng 345–352, 397–412 [code]. Việc chạy lại 41 câu khó một bên trước deploy (không chạy bây giờ — "chạy bây giờ thì sau buổi test lại phải chạy lần nữa"): `session_prompt/HIEN_TRANG.md` mục 1 gạch "ĐO BÙ" (khối "GIỚI HẠN CỦA CHÍNH LƯỢT ĐO BÙ … NỢ TRƯỚC DEPLOY", có cả "xét có chạy 12 vai không") và mục 2 hàng 8, `origin/main` `e6a6fa6e` 21:03 [chép, đã mở; việc chưa làm]. Ô 12 vai: `KE_HOACH.md` dòng 84 (ô 8 "chỉ khi tổng thật sau ô 1–7 dưới 1,2 USD"), dòng 3 (kế hoạch 12:20, quyết định chờ (4)); bỏ sau đó: `KET_QUA.md` dòng 44, `session_prompt/sessions/STATUS_E.md` dòng 5, 16; món nợ ba thứ: `git show 678f0b16:session_prompt/HIEN_TRANG.md` dòng 143 ("12 vai, 41 câu khó, sàn"); lời 19:34 "test vừa phải, không test quá mức, không over-engineer nhé" (giờ ghi 19:34, "chủ dự án gõ lúc phiên tối vừa mở"): `data/loi_user/2026-11-23.md` [riêng tư; chép]. Hồ sơ không ghi lời nhắc đó là lý do bỏ ô; bài đặt hai việc cạnh nhau. Gắn đoạn dặn cho đường OpenAI: kế hoạch định trình chủ dự án "nhận giới hạn hay chữa" (`KE_HOACH.md` dòng 47, 88); `KET_QUA.md` dòng 7 "phiên điều phối đã quyết"; lý do: `git show 6c1e9a4c:session_prompt/HIEN_TRANG.md` gạch "ĐO BÙ" ("⇒ CHỮA (không trình chủ dự án: sàn không nới, cách chữa có sẵn)") [chép]. Quyết định bỏ ô 12 vai ghi 19:35 23/11 trong sổ việc (commit `a372742b`, khối "[19:35 23/11/2026] SAU LỜI NHẮC CỦA CHỦ DỰ ÁN lúc phiên tối vừa mở … — phiên điều phối quyết", mục (3): "không nêu được nó đổi quyết định nào") [chép; hồ sơ đặt hai việc theo thứ tự giờ, không ghi lời nhắc là lý do]. Gọi lại trên đường chữ chạy dần: `backend/llm/openai_goi_lai.py` `stream_response` — `da_phat = True` ở sự kiện ĐẦU TIÊN của luồng (bất kỳ loại nào), chú thích đầu file "chỉ gọi lại khi CHƯA sự kiện nào đi ra" [code]. Tệp cấu hình của bản deploy: `deploy/docker/README.md` dòng 181 ("`cau_hinh/settings.yaml` của GÓI ghi `provider: openai` (bản trong ảnh vẫn `bedrock`)"); `HIEN_TRANG.md` mục 4 gạch "MODEL CỦA BẢN DEPLOY" [chép]. Câu kể sai sau lệnh bỏ điểm: `data/playwright_mcp/luot_2311_luna_o7/NHAT_KY.md` hàng 5 [đã mở]. Mì Quảng 2 / 2 ↔ 1 / 2: `KET_QUA.md` dòng 48 [chép]. "Trong mức dao động": `KE_HOACH.md` dòng 42 ("Bên tắt = 2 ⇒ trong nhiễu của CHÍNH NÓ (mốc dao động 5 · 6 · 7)"); cách diễn lại "chỉ hơn ≤ 1 một mục" là cách người viết đọc luật [lập luận]. Lời chủ dự án 21/11 trích đủ câu: `git show 678f0b16:…HIEN_TRANG.md` dòng 143. Để giữ nửa để hiểu ≤ 13.787 (sau 13.780): chuyển xuống "Chi tiết để tra" lời nạp tiền nguyên văn, số điểm 66 câu của bảng hai model (có ở bảng bốn mức), tốc độ 114 / 101 token, hai điều của quyết định 2, ví dụ 27 / 27, chi tiết bản kế hoạch 12:20, tiền tách 0,65 / 0,66, câu "lỗi nằm ở chương trình dùng chung", hai dòng "Nếu… thì sao" (quá 45 giây; model thứ ba). Không đụng các dòng cũ có số tiền Bedrock.

</details>
