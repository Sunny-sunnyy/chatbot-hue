# Bài 35 — Trang web và máy chủ: ai gửi gì cho ai

*Cập nhật 13:58, ngày 22/11/2026 · các đường gọi, loại tin và cách giao diện xử lý đọc từ chương trình trưa 22/11 (gồm bản sửa "tải trang không chiếm chỗ" vào cây chính trưa 22/11); kết quả thử thật đường báo tình trạng lấy từ bài 6 (thử 22/11); người viết không chạy máy chủ; bài đã qua một lượt đối chiếu độc lập và sửa theo đó.*

**Bài trước đã biết:** giao diện chạy trong trình duyệt, máy chủ chạy trên máy của dự án, chữ được gửi dần, cuộc trò chuyện nằm trong bộ nhớ của máy chủ (bài 6); model viết gửi chữ một lần (bài 33).
**Bài này thêm:** giao diện gọi máy chủ qua những đường nào; trên đường gửi dần có những loại tin gì và giao diện làm gì với từng loại; máy chủ nhận ra "cùng một cuộc trò chuyện" bằng cách nào; và hai lớp chặn để chữ model viết không làm trang tải thứ lạ.

## Ý chính

- Giao diện nói chuyện với máy chủ qua **khoảng 18 đường gọi**; chỉ ba đường gọi model (hai cho ô chat, một cho ảnh), còn lại chỉ đọc dữ liệu đã có.
- Trên đường gửi dần, máy chủ gửi **từng loại tin có tên**: trạng thái, chữ, thay chữ, nguồn, ghi chú, mục web, các tin của lịch, thẻ hỏi lại, lỗi, xong. Tin "lỗi" làm giao diện xoá chữ đã hiện và hiện nút "Thử lại".
- Máy chủ nhận ra một cuộc trò chuyện nhờ **một mã ngẫu nhiên trong cookie** mà chương trình của trang không đọc được. Lịch sử nằm ở máy chủ, không ở trình duyệt. Mỗi lần tải trang, giao diện xin một cuộc mới.
- Chữ model viết đi qua **hai lớp chặn**: giao diện lọc chữ theo một danh sách nhãn HTML cho phép trước khi vẽ, và trang có một chính sách cấm tải bất cứ thứ gì từ máy khác (trừ ô nền bản đồ).
- Đường báo tình trạng **chỉ biết tình trạng lúc bật**. Đã thử: Qdrant ngừng giữa chừng thì nó vẫn báo đủ.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| yêu cầu | **request** | một lần trình duyệt hỏi máy chủ; có hai loại hay dùng: **lấy về** (GET, chỉ xin dữ liệu) và **gửi lên** (POST, gửi kèm dữ liệu, ví dụ câu hỏi) |
| đường gọi | **endpoint**, **route** | một địa chỉ trên máy chủ, ví dụ địa chỉ của ô chat; mỗi đường làm một việc |
| JSON | **JSON** | cách viết dữ liệu thành chữ có cấu trúc (tên ô và giá trị) |
| tin có tên | **SSE event** | trên đường gửi dần, mỗi mẩu máy chủ gửi có một tên (ví dụ "nguồn") và một phần dữ liệu |
| cookie | **cookie** | một mẩu chữ nhỏ máy chủ nhờ trình duyệt giữ hộ; trình duyệt tự gửi lại mẩu đó ở mỗi yêu cầu sau tới cùng máy chủ |
| chính sách chặn tải | **Content-Security-Policy** | dòng máy chủ gửi kèm trang, bảo trình duyệt chỉ được tải chương trình, kiểu chữ, ảnh từ những nơi được liệt kê |
| HTML, nhãn HTML | **HTML**, **tag** | ngôn ngữ trình duyệt dùng để vẽ trang; mỗi phần của trang được đánh dấu bằng một nhãn, ví dụ nhãn đoạn văn, nhãn ảnh, nhãn link |
| lọc chữ | **sanitize** | bỏ khỏi chữ mọi nhãn HTML không nằm trong danh sách cho phép trước khi đưa lên trang |
| kết nối mã hoá | **https** | trình duyệt và máy chủ nói chuyện bằng chữ đã mã hoá, người ở giữa đường không đọc được; địa chỉ bắt đầu bằng https. Trên máy phát triển trang mở bằng địa chỉ không mã hoá |
| tab | **browser tab** | mỗi trang đang mở trong một cửa sổ trình duyệt; các tab dùng chung cookie |

## Một đường gọi là một địa chỉ trên máy chủ

Mỗi khi trang cần gì, nó gửi một yêu cầu tới một đường gọi của máy chủ rồi chờ; câu trả lời thường là JSON, riêng ô chat là một luồng tin gửi dần. Chỉ ba đường gọi model (ô chat gửi dần, ô chat trả cả câu, hỏi bằng ảnh); các đường còn lại đọc dữ liệu đã có cho trang hoặc làm việc khác (mở cuộc mới, tải PowerPoint, báo sai, theo dõi, tình trạng). Bảng đủ ở nửa để tra. Đường nào gửi lên dữ liệu thì chỉ nhận đúng khuôn đã định: đường "báo thông tin chưa đúng" chỉ nhận mã một bài trùng nguyên chuỗi một bài có thật, không nhận chữ tự do.

## Trên đường gửi dần, mỗi tin có một tên, và giao diện vẽ theo tên

Khi người dùng gửi câu hỏi, trang mở một yêu cầu gửi lên đường ô chat gửi dần, rồi đọc liên tục cho tới tin "xong". Ví dụ chính (*"Giá vé tham quan Đại Nội Huế là bao nhiêu?"*) nhận lần lượt: ba bốn tin trạng thái, một tin chữ, một tin nguồn, một tin ghi chú ("có thể đã thay đổi"), một tin xong.

| Tin | Máy chủ gửi khi | Giao diện làm gì |
|---|---|---|
| trạng thái | mỗi bước bắt đầu: xếp loại câu, tìm, tìm xong; ở lượt có công cụ, "đang viết" chỉ gửi ngay trước chữ đầu | đổi dòng trạng thái; với Claude, suốt lúc chờ người dùng nhìn "Đã tìm trong kho, đang chuẩn bị câu trả lời… (10 đoạn)" |
| chữ | model gửi một mẩu chữ (với Claude: một mẩu duy nhất) | nối mẩu vào ô chữ, vẽ lại tối đa mỗi lần màn hình làm mới; bỏ số nguồn [n] khi vẽ |
| thay chữ | chương trình đã gỡ một câu khỏi chữ model (ví dụ câu có con số không có nguồn, bài 16) | thay cả ô chữ bằng bản cuối |
| nguồn | chữ đã qua bước kiểm số nguồn | vẽ bản cuối, rồi mới hiện dòng "Nguồn" |
| ghi chú | có dòng "có thể đã thay đổi", hoặc câu an toàn bão lũ | hiện dưới câu trả lời; câu an toàn in đậm |
| mục web | kho đã từ chối và đã tra web (bài 25) | hiện mục "Từ web (chưa kiểm)" |
| khung lịch, câu lịch, lịch xong, lịch kèm link bản đồ | lượt lập hay sửa lịch (bài 27, 29, 31) | hiện khung ngay, đổ câu vào từng mục; lịch kèm link hiện dưới câu trả lời |
| thẻ hỏi lại, thẻ chọn điểm thay | câu thiếu thông tin, hoặc lệnh sửa lịch cần người dùng chọn (bài 31) | vẽ các nút; nút chỉ mang giá trị do máy chủ đưa |
| lỗi | lượt hỏng, kể cả khi kiểm số nguồn hỏng sau khi chữ đã hiện | xoá mọi thứ đã hiện; hiện lời báo của máy chủ và nút "Thử lại" |
| xong | lượt kết thúc | ghi kết cục; nếu kho không đủ thì hiện gợi ý cách hỏi |

Luồng đứt mà chưa có tin "xong" thì giao diện coi như lỗi. Bấm "Dừng" hoặc đóng trang thì trang huỷ yêu cầu, và máy chủ dừng lần gọi model.

## Máy chủ nhận ra một cuộc trò chuyện nhờ một mã trong cookie

Để biết câu "còn chỗ đó thì sao?" thuộc cuộc nào, ở lượt hỏi đầu máy chủ tạo một mã ngẫu nhiên dài, cất cuộc trò chuyện dưới mã đó trong bộ nhớ, và gửi mã cho trình duyệt dưới dạng cookie. Từ lượt sau, trình duyệt tự gửi lại cookie; máy chủ tìm đúng cuộc theo mã.

Cookie này có ba giới hạn đặt sẵn: chương trình của trang **không đọc được** nó; trình duyệt chỉ gửi nó cho các đường gọi dữ liệu của chính máy chủ này (các địa chỉ bắt đầu bằng /api), không gửi khi yêu cầu đến từ trang khác; nó hết hạn sau 30 phút. Cookie chỉ mang mã, không mang chữ nào của cuộc trò chuyện.

Mỗi lần trang được tải (hay tải lại), giao diện gọi đường "cuộc trò chuyện mới": máy chủ xoá cuộc cũ khỏi bộ nhớ và đặt một mã mới. Từ trưa 22/11, mã mới đó **chưa chiếm chỗ** trong kho 500 cuộc; cuộc chỉ được tạo khi có lượt hỏi đầu tiên.

## Chữ model viết đi qua hai lớp chặn trước khi lên màn hình

Câu trả lời là chữ có định dạng (Markdown: in đậm, danh sách, bảng, link) do model viết; trang đổi nó thành HTML để vẽ. Nếu model, vì một chữ lạ chen vào lời dặn (bài 37), viết ra một nhãn ảnh trỏ tới máy khác, trình duyệt sẽ tự tải ảnh đó, và địa chỉ ảnh có thể mang chữ của cuộc trò chuyện ra ngoài (lập luận, không phải số đo).

- **Lớp một, ở giao diện:** trước khi vẽ, chữ được lọc theo một **danh sách cho phép**: chỉ các nhãn Markdown thường tạo ra (đoạn, đậm, nghiêng, danh sách, bảng, tiêu đề, link…). Không có nhãn ảnh. Chỗ duy nhất được mang địa chỉ là địa chỉ của link, và link chỉ mở khi người dùng bấm, ở tab mới. Mục web lọc chặt hơn: không cho cả link.
- **Lớp hai, ở trình duyệt:** máy chủ gửi kèm trang một chính sách chặn tải: chương trình, kiểu chữ, ảnh chỉ được tải từ chính máy chủ; không chương trình viết lẫn trong trang; không trang nào được nhúng trang này vào trong nó. Ngoại lệ có ghi lý do: ảnh người dùng vừa chọn để gửi (trình duyệt tự tạo bản xem trước, không tải từ đâu) và, vì tính năng bản đồ đang bật, ô nền bản đồ từ một máy chủ bản đồ công cộng.

## Quyết định và lý do

### 1. Vì sao mã cuộc trò chuyện nằm trong một cookie mà trang không đọc được?

- **Đã chọn:** máy chủ giữ lịch sử; trình duyệt chỉ giữ một mã ngẫu nhiên trong cookie mà chương trình của trang không đọc được, chỉ gửi cho các đường gọi dữ liệu, không gửi khi yêu cầu đến từ trang khác.
- **Vì sao:** máy chủ giữ lịch sử vì nếu trình duyệt gửi lại "trợ lý đã nói thế này", người dùng sửa được câu đó để cài mệnh lệnh (lý do ghi trong chương trình, bài 6). Ba giới hạn của cookie: chưa thấy ghi lý do riêng. Điều thấy được: giới hạn thứ tư, "chỉ gửi qua kết nối mã hoá", để tắt khi chạy trên máy vì trang trên máy mở bằng địa chỉ không mã hoá; bật bằng một thiết lập lúc chạy (bài 37).
- **Cách khác:** trang tự giữ mã và gửi kèm câu hỏi: chưa thử.
- **Cái giá:** cookie chung cho mọi tab của cùng một trình duyệt. Mở trang ở tab thứ hai thì máy chủ xoá cuộc của tab thứ nhất: câu hỏi tiếp ở tab thứ nhất được trả lời như câu đầu của một cuộc mới (không còn nhớ câu trước, lịch đã lập cũng mất, nút tải PowerPoint báo hết hạn); từ đó hai tab dùng chung một cuộc (suy từ chương trình, chưa thử).

### 2. Vì sao tải lại trang thì máy chủ quên cuộc cũ?

- **Đã chọn:** mỗi lần trang được tải, giao diện xin một cuộc mới; lỗi mạng ở bước này thì bỏ qua, vẫn cho hỏi.
- **Vì sao:** lý do ghi trong chương trình: trước đây sau khi tải lại trang, câu đầu được model đọc như câu hỏi tiếp của cuộc cũ; chủ dự án gặp ngày 15/11, một câu vừa trả lời đúng bị từ chối.
- **Cách khác:** giữ cuộc qua lần tải lại, vẽ lại các lượt cũ: chưa thử.
- **Cái giá:** tải lại trang là mất cuộc và lịch đang giữ. Trước trưa 22/11, mỗi lần tải trang còn chiếm một chỗ trong kho 500 cuộc (đã sửa; mục "Quyết định nhỏ hơn").

### 3. Vì sao chặn chữ model bằng hai lớp, và lớp lọc là danh sách cho phép?

- **Đã chọn:** lớp lọc ở giao diện chỉ giữ đúng các nhãn Markdown thường tạo ra, mọi thứ khác bị bỏ; cộng một chính sách chặn tải ở trình duyệt.
- **Vì sao:** lý do ghi trong chương trình, từ một vòng rà bảo mật: ngoài chặn chương trình lạ, trang không được tự tải gì từ máy khác khi hiện chữ (ảnh, nền, kiểu chữ có địa chỉ, ô nhập dạng ảnh, biểu mẫu…). Danh sách cấm dễ sót một nhãn; danh sách cho phép thì nhãn lạ nào cũng bị bỏ. Chính sách chặn tải là để chặn mọi tải từ máy khác **kể cả khi** chữ lọt qua bộ lọc (lý do ghi trong chương trình).
- **Cách khác:** bộ lọc với danh sách cấm: là bản trước vòng rà đó, đã thay. Chỉ dựa vào bộ lọc: không làm.
- **Cái giá:** model không chèn được ảnh vào câu trả lời; ảnh dưới câu trả lời (bài 26, 30) do chương trình gắn riêng. Thêm thứ gì từ ngoài (một kiểu chữ, một bản đồ khác) đều phải sửa chính sách trên máy chủ.

### 4. Vì sao đường báo tình trạng chỉ đọc trạng thái lúc bật, không hỏi thử Qdrant hay hãng model?

- **Đã chọn:** đường báo tình trạng trả trạng thái máy chủ ghi lại lúc bật: Qdrant, bước tìm, bộ đếm token, model viết; đủ cả thì "ok", thiếu một thì báo thiếu phần nào.
- **Vì sao:** chưa thấy ghi lý do. Điều thấy được: kế hoạch lúc dựng máy chủ ghi "không thêm lần gọi thử hay kiểm nhà cung cấp" cho đường này.
- **Cách khác:** mỗi lần được hỏi thì gọi thử Qdrant và hãng model: không làm (quyết định đã ghi).
- **Cái giá:** đã thử 22/11: Qdrant ngừng giữa chừng mà nó vẫn báo "ok"; khoá model hết hạn cũng vậy. Muốn biết còn trả lời được không, phải hỏi thử một câu thật.

## Nếu… thì sao

Một tình huống kể trọn. Người dùng đang chờ thì mạng chập; luồng đứt trước tin "xong". Giao diện xoá phần đã hiện, hiện "Kết nối bị gián đoạn. Vui lòng thử lại." và nút "Thử lại". Máy chủ dừng lần gọi model, không nhớ lượt này. Bấm "Thử lại" thì trang gửi lại đúng câu đó, vẫn cùng cuộc.

Lời báo là nguyên văn; các dòng đọc từ chương trình, chưa thử thật, trừ dòng có chữ **(đã thử)** (bài 6).

| Nếu | Người dùng thấy gì | Muốn hết lỗi thì ai làm gì |
|---|---|---|
| không kết nối được máy chủ (máy chủ tắt) | "Không kết nối được máy chủ. Vui lòng thử lại." | người vận hành bật máy chủ (bài 36) |
| luồng đứt giữa chừng | "Kết nối bị gián đoạn. Vui lòng thử lại." | người dùng bấm "Thử lại" |
| người dùng bấm "Dừng" | "Đã dừng. Phần trả lời chưa xong nên không hiện (chưa kiểm nguồn)." | — |
| không tải được danh sách tính năng lúc mở trang | trang chạy như mọi tính năng đều tắt: không biểu mẫu lập lịch, không ô thời tiết, không nút gửi ảnh | tải lại trang |
| Qdrant ngừng giữa chừng **(đã thử)** | câu hỏi lỗi, nhưng đường báo tình trạng vẫn "ok" | bật lại Qdrant; đừng dựa vào đường báo tình trạng |
| mở trang ở tab thứ hai | tab thứ nhất trả lời câu tiếp như câu đầu của cuộc mới, mất lịch đã lập, không có lời báo | người dùng dùng một tab; **chưa có** cách tách cuộc theo tab |

## Dễ nhầm

- **"Lịch sử trò chuyện nằm trong cookie."** Không. Cookie chỉ mang một mã; lịch sử nằm trong bộ nhớ máy chủ.

## Câu hỏi tự kiểm

<details>
<summary>1. Khi kiểm số nguồn hỏng sau khi chữ đã hiện, giao diện biết bằng cách nào và làm gì?</summary>

Máy chủ gửi tin "lỗi" thay cho tin "nguồn". Giao diện xoá chữ đã hiện, hiện lời báo của máy chủ và nút "Thử lại".

</details>

<details>
<summary>2. Cookie của hệ thống mang gì, và vì sao chương trình của trang không đọc được nó?</summary>

Chỉ một mã ngẫu nhiên. Lịch sử nằm ở máy chủ để người dùng không sửa được "trợ lý đã nói gì"; cookie chỉ trình duyệt và máy chủ thấy.

</details>

<details>
<summary>3. Vì sao đã lọc chữ model mà còn cần chính sách chặn tải?</summary>

Hai lớp ở hai nơi: chữ lọt qua bộ lọc thì trình duyệt vẫn không tải gì từ máy khác.

</details>

<details>
<summary>4. Tải lại trang thì cuộc trò chuyện ra sao, và vì sao làm vậy?</summary>

Máy chủ xoá cuộc cũ, cấp mã mới; trước đây câu đầu sau khi tải lại bị đọc như câu hỏi tiếp của cuộc cũ (15/11).

</details>

## Cấu hình đang chạy

*Theo chương trình trưa 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Hạn cookie và hạn cuộc trò chuyện | 30 phút từ lượt cuối | bài 23 | — |
| Kho cuộc trò chuyện | nhiều nhất 500 cuộc, quá thì bỏ cuộc cũ nhất | trần bộ nhớ | — |
| Cookie: không cho trang đọc · chỉ gửi trong cùng trang · chỉ gửi cho `/api` | bật | quyết định 1 | — |
| `HUE_COOKIE_SECURE` | chưa đặt (tắt) | cookie chỉ đi qua kết nối mã hoá; bật khi đưa lên mạng | — |
| Danh sách nhãn HTML cho phép khi lọc chữ | đoạn, xuống dòng, kẻ ngang, đậm, nghiêng, gạch, mã, khối trích, danh sách, tiêu đề, link, bảng | quyết định 3 | thay bộ lọc danh sách cấm |
| Chính sách chặn tải | mọi thứ từ chính máy chủ; thêm ảnh xem trước, và ô bản đồ vì tính năng bản đồ đang bật | quyết định 4 | — |
| Vẽ lại ô chữ | nhiều nhất một lần mỗi khung hình | theo bản đặc tả chữ hiện dần (01/11); chỉ có tác dụng khi model gửi nhiều mẩu | — |
| `HUE_TAT_DOCS` | chưa đặt | tắt trang mô tả các đường gọi tự sinh của thư viện máy chủ; bật khi đưa lên mạng (bài 37) | — |

## Mọi đường gọi của máy chủ

| Đường gọi | Loại | Gọi model? | Ai dùng |
|---|---|---|---|
| ô chat gửi dần | gửi lên | có | khung Trợ lý, trang Lên kế hoạch |
| ô chat trả cả câu | gửi lên | có | lệnh thử của người vận hành, công cụ đo |
| cuộc trò chuyện mới | gửi lên | không | mỗi lần tải trang; nút "Cuộc trò chuyện mới" |
| hỏi bằng ảnh | gửi lên | có | nút gửi ảnh (bài 26) |
| tính năng ảnh có bật không | lấy về | không | có ở máy chủ; giao diện nay đọc danh sách tính năng thay cho đường này |
| tải lịch thành PowerPoint | lấy về | không | thẻ lịch (bài 30) |
| danh sách bài · một bài | lấy về | không | trang Khám phá, Trang chủ |
| báo thông tin chưa đúng | gửi lên | không | nút ở trang bài Khám phá; chỉ ghi mã bài vào sổ |
| đánh giá một lượt (thích, không thích) | gửi lên | không | có ở máy chủ; giao diện hiện không gọi |
| thời tiết | lấy về | không | ô thời tiết Trang chủ; lỗi thì ô ẩn |
| tính năng đang mở | lấy về | không | mọi trang, một lần lúc mở |
| lịch mẫu | lấy về | không | trang Lên kế hoạch lúc chưa xếp |
| bản đồ · chỗ ở | lấy về | không | trang Bản đồ, trang Chỗ ở, thẻ khách sạn |
| theo dõi | lấy về | không | trang theo dõi của chủ dự án, cần khoá (bài 34) |
| tình trạng | lấy về | không | người vận hành, bộ bật hệ thống (bài 36) |
| trang và file của giao diện | lấy về | không | trình duyệt, khi mở trang |

## Quyết định nhỏ hơn

**Vì sao hai yêu cầu cùng một cuộc không phải xếp hàng?** Chú thích trong chương trình: kho cuộc trò chuyện không khoá; hai yêu cầu cùng cuộc chạy song song thì lượt xong sau ghi sau, vì thiết kế cho một người dùng mỗi cuộc. Cái giá: hai tab dùng chung một cuộc (quyết định 1) có thể ghi đè lượt của nhau.

**Vì sao mục web lọc chặt hơn câu trả lời chính?** Mục web dùng một danh sách cho phép không có nhãn link: link của mục web chỉ lấy từ sổ nguồn do chương trình dựng (bài 25). Câu trả lời chính vẫn cho link (bài 37).

**Vì sao mở cuộc mới không còn chiếm chỗ trong kho 500 cuộc?** Đợt rà bảo mật trước khi đưa lên mạng (22/11) thấy: giao diện gọi "cuộc mới" ở mỗi lần tải trang, mỗi lần chiếm một chỗ, nên 500 lần gọi của bất kỳ ai đẩy mọi cuộc đang có, kèm lịch đã lưu, ra khỏi kho. Nay mã mới chỉ thành một cuộc khi có lượt hỏi đầu tiên. Cái giá: không có.

**Vì sao lỗi luôn hiện bằng một câu tiếng Việt cố định?** Lý do ghi trong chương trình: lỗi mạng hay lỗi đọc dữ liệu mang chữ kỹ thuật tiếng Anh của trình duyệt; giao diện không hiện chữ đó mà đổi sang một câu cố định. Lỗi do máy chủ gửi thì giữ nguyên lời của máy chủ.

**Vì sao trang danh sách bài chỉ nhận mã bài trùng nguyên chuỗi?** Lý do ghi trong chương trình: không ghép đường dẫn file từ chữ người dùng gửi lên, nên không đọc được file nào ngoài danh sách bài đã kiểm lúc bật; mã có chữ "sealed" hay trỏ vào thư mục không phải bài bị chặn thêm một lớp.

**Vì sao ô thời tiết lỗi thì ẩn, không hiện số cũ?** Cùng luật của công cụ thời tiết: lỗi thì không bao giờ đưa ra con số (bài 24).

## Giới hạn đã biết

- **Đường báo tình trạng không biết hệ thống có đang trả lời được không** (quyết định 4; đã thử với Qdrant).
- **Hai tab cùng trình duyệt dùng chung một cuộc**, và tab mở sau xoá cuộc cùng lịch của tab trước (đã xác nhận bằng một lượt thử thật trưa 22/11).
- **Tải lại trang là mất cuộc và lịch đang giữ**; không có lời báo.
- **Đường đánh giá một lượt có ở máy chủ nhưng giao diện chưa dùng.**

## Chi tiết để tra

- Việc tab mở sau xoá cuộc trò chuyện và lịch của tab mở trước đã được xác nhận bằng một lượt thử thật ở lượt kiểm chốt trưa 22/11.
- Mã cuộc trò chuyện: 16 byte ngẫu nhiên viết thành chữ; mã lạ hoặc hết hạn thì máy chủ cấp mã mới và đặt lại cookie. Cookie đi theo cả phản hồi lỗi, để lượt đầu lỗi không để lại cuộc mồ côi.
- Đường ô chat gửi dần: lỗi trước khi mở luồng (bước tìm hay model viết chưa sẵn sàng) thì trả JSON lỗi; từ lúc mở luồng, xếp loại câu và tìm chạy bên trong luồng, nên Qdrant lỗi giữa lượt thành một tin "lỗi" mang câu "Hệ thống tra cứu tạm thời không khả dụng.".
- Tin "chữ" có số thứ tự; giao diện bỏ mẩu có số cũ hơn mẩu đã nhận. Chữ đang tới có thể dừng giữa một mã nguồn ("… [1"), nên phần mã dở ở cuối cũng bị bỏ khi vẽ.
- Thứ tự số ở dòng "Nguồn" đánh theo lần xuất hiện đầu tiên của mã trong câu trả lời.
- Đường đánh giá một lượt (khi được gọi) chỉ ghi một dòng sổ: mã lượt ngẫu nhiên, tuyến, kết cục, số nguồn, đánh giá; không chữ, không mã cuộc. Đường báo thông tin chưa đúng chỉ ghi mã bài.
- Trang mô tả các đường gọi tự sinh (`/docs`) còn mở khi chạy trên máy; thiết lập lúc chạy `HUE_TAT_DOCS` tắt nó.
- Khi bộ giới hạn lượt bật, ba đường gọi model và đường tải PowerPoint bị đếm theo địa chỉ mạng (bài 37).

**Bài sau (bài 36):** bật cả hệ thống trên máy bằng một lệnh, và gói hệ thống thành ba hộp Docker.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Các đường gọi: `backend/api/app.py` (`include_router`, `/static`, `/`), `backend/api/routes/chat.py` (`/api/conversation/new`, `/api/chat`, `/api/chat/stream`), `anh.py`, `cong.py` (`/api/kham_pha`, `/api/kham_pha/bai`, `/api/thoi_tiet`, `/api/tinh_nang`, `/api/lich_mau`, `/api/ban_do`, `/api/cho_o`), `xuat.py` (`/api/lich/pptx`), `backend/api/feedback.py` (`/api/feedback`, `/api/bao_sai`), `backend/api/theo_doi.py`, `backend/api/health.py` [code, đọc 22/11]. "Khoảng 18 đường" là người viết đếm (17 đường `/api` + `/health`, chưa tính file tĩnh). Ai dùng: grep `fetch(` trong `frontend/src` — không file nào gọi `/api/feedback` hay `/api/chat` (không stream) [code]; `/api/chat` dùng trong `guides/DOI_MODEL_VIET.md` mục 2 bước 4 và `data/thu_bedrock_2026-11-21/tools/e_phien.py` [riêng tư].
- Các loại tin và việc của giao diện: `chat.py` (`StreamEvents`, các lời gọi `sse_event`), `backend/llm/len_ke_hoach.py` (`lich_khung`, `lich_cau`, `lich_xong`, `sua_the`), `frontend/src/stream.js` (`createSseParser`, `streamAnswer`, ba câu lỗi), `frontend/src/chat.jsx` (`onEvent`, dòng 132–200; dòng trạng thái dòng 21–28; nút "Dừng" và câu "Đã dừng…" dòng 373, 426) [code].
- Cookie: `chat.py` (`CONVERSATION_COOKIE`, `_set_cookie`: `httponly`, `samesite="strict"`, `path="/api"`, `max_age=TTL_SECONDS`, `HUE_COOKIE_SECURE`; chú thích dòng 166–167) [code]. Mã 16 byte: `backend/api/conversations.py` (`secrets.token_urlsafe(16)`) [code].
- Tải trang ⇒ cuộc mới, lý do 15/11: `frontend/src/chat.jsx` dòng 209–213 (chú thích) [code]. Mã mới không chiếm chỗ (R4, 22/11): `conversations.py` (`reset`, chú thích), commit `7024636e` [code]. Hai thẻ chung cookie: [suy từ code, chưa thử].
- Lọc chữ: `frontend/src/markdown.js` (`SANITIZE_OPTIONS`, `withSafeLinks`, `renderAnswerHtml`, chú thích "review C107 M-1") [code].
- Chính sách chặn tải: `backend/api/app.py` (`FRONTEND_CSP`, `FRONTEND_CSP_BAN_DO`, chú thích) [code].
- Đường báo tình trạng: `backend/api/health.py` ("never pings external services") [code]; `docs/superpowers/plans/2026-08-25-phase-6-generation-api-simplicity-implementation.md` dòng 905–906 ("Do not add health pings or provider checks.", không ghi lý do) [đã đọc]; thử thật Qdrant ngừng vẫn "ok": bài 6 của giáo trình, mục "Mọi tình huống hỏng" [đã chạy 22/11, chép].
- Lỗi luôn tiếng Việt: `stream.js` (chú thích lớp `StreamError`, "review C119 m-1") [code]. Mã bài so nguyên chuỗi: `cong.py` (chú thích đầu file, `_bi_chan`), `feedback.py` (chú thích đầu file) [code].
- Không khoá hai yêu cầu cùng cuộc: `backend/api/conversations.py` dòng 6 [code]. Mục web không cho link: `frontend/src/markdown.js` (`WEB_SANITIZE_OPTIONS`) [code]. `GET /api/anh/ung_vien` có ở máy chủ nhưng giao diện đọc `/api/tinh_nang` thay cho nó: `backend/api/routes/anh.py` dòng 62–67, chú thích `frontend/src/HoiBangAnh.jsx` dòng 20 [code]. Hai tab: lần theo `reset` / `ensure` của `conversations.py` và `xuat.py` dòng 44–47 [suy từ code, chưa thử]. Dòng trạng thái ở lượt có công cụ: `backend/llm/assistant.py` (`pending_generating`) [code].
- Bài đã qua một lượt đối chiếu độc lập 22/11: `data/hoc_cung_D/kiem/bai_33_38.md` [riêng tư]; dòng không áp ở `data/hoc_cung_D/viet/viet_33_38.md` mục "Sau lượt kiểm".
- Tính năng lỗi ⇒ tắt hết: `frontend/src/App.jsx` dòng 20, 42 (`TINH_NANG_TAT`) [code].
- Mạng đứt ⇒ máy chủ dừng model, không nhớ lượt: `chat.jsx` chú thích dòng 187–189; `chat.py` (`client_disconnected`, `REMEMBERED_OUTCOMES`) [code]. Tất cả các dòng bảng "Nếu… thì sao" trừ dòng Qdrant: [suy từ code, chưa thử thật].
- `HUE_TAT_DOCS`: `app.py` (`TAT_DOCS_ENV`) [code].

- Kết quả lượt kiểm chốt buổi trưa 22/11 (phiên điều phối báo, phiên đo chạy; người viết chép từ tin, chưa tự mở file kết quả) [đã chạy].

</details>
