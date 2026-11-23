# Bài 35 — Trang web và máy chủ: ai gửi gì cho ai

*Cập nhật 14:33, ngày 23/11/2026 · khớp hệ thống 13:52 23/11 (50 tính năng mở, 5 tắt, kho 267 bài) · thẻ "Hôm nay ở Huế", nhãn lượt trình duyệt trưa (nửa để tra) · số kiểm từ hồ sơ cổng gộp · người viết không chạy máy chủ · lần sửa trước: Nguồn.*

**Bài trước đã biết:** giao diện chạy trong trình duyệt, máy chủ chạy trên máy của dự án, chữ được gửi dần, cuộc trò chuyện nằm trong bộ nhớ của máy chủ (bài 6); model viết gửi chữ một lần (bài 33).
**Bài này thêm:** giao diện gọi máy chủ qua những đường nào; trên đường gửi dần có những loại tin gì và giao diện làm gì với từng loại; máy chủ nhận ra "cùng một cuộc trò chuyện" bằng cách nào; hai lớp chặn để chữ model viết không làm trang tải thứ lạ; và lớp nhìn mới của trang được dựng, được kiểm thế nào.

## Ý chính

- Giao diện nói chuyện với máy chủ qua **khoảng 18 đường gọi**; chỉ ba đường gọi model (hai cho ô chat, một cho ảnh), còn lại chỉ đọc dữ liệu đã có. Đường báo tình trạng **chỉ biết tình trạng lúc bật** (đã thử: Qdrant ngừng giữa chừng thì nó vẫn báo đủ).
- Trên đường gửi dần, máy chủ gửi **từng loại tin có tên**: trạng thái, chữ, thay chữ, nguồn, ghi chú, mục web, các tin của lịch, thẻ hỏi lại, lỗi, xong. Tin "lỗi" làm giao diện xoá chữ đã hiện (nếu có) và hiện nút "Thử lại".
- Máy chủ nhận ra một cuộc trò chuyện nhờ **một mã ngẫu nhiên trong cookie** mà chương trình của trang không đọc được. Lịch sử nằm ở máy chủ, không ở trình duyệt. Mỗi lần tải trang, giao diện xin một cuộc mới.
- Chữ model viết đi qua **hai lớp chặn**: giao diện lọc chữ theo một danh sách nhãn HTML cho phép trước khi vẽ, và trang có một chính sách cấm tải bất cứ thứ gì từ máy khác (trừ ô nền bản đồ).
- Giao diện "Dòng sông dẫn đường" (từ 10:00 23/11) **chỉ đổi lớp nhìn**: một bảng màu và một thang cỡ chữ (mỗi giá trị đặt tên một lần rồi mọi trang gọi theo tên), con sông vẽ bằng đường cong, màn đầu cao theo khung nhìn, chuyển động tắt khi máy yêu cầu. Trước khi gộp, bản gộp thử qua 761 ảnh chụp tự động ở tám cỡ khung nhìn, một kịch bản 50 bước, in thử ra PDF và cả bộ test; bản dựng tối 22/11 được so cặp ảnh cũ ↔ mới. Bốn lỗi chặn chỉ lộ ra trên ảnh hoặc bản in thử, bộ test không báo lỗi nào.

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
| kết nối mã hoá | **https** | trình duyệt và máy chủ nói chuyện bằng chữ đã mã hoá; địa chỉ bắt đầu bằng https. Trên máy phát triển trang mở bằng địa chỉ không mã hoá |
| tab | **browser tab** | mỗi trang đang mở trong một cửa sổ trình duyệt; các tab dùng chung cookie |
| bảng kiểu | **CSS** | phần của trang quy định màu, cỡ chữ, khoảng cách, vị trí từng khối; chữ và nút nằm ở HTML |
| khung nhìn | **viewport** | phần cửa sổ trình duyệt đang hiện trang, đo bằng điểm ảnh (px) rộng × cao |
| hình vẽ bằng đường cong | **SVG** | hình mô tả bằng toạ độ và đường cong; trình duyệt tự vẽ, phóng to không vỡ |
| giảm chuyển động | **prefers-reduced-motion** | tuỳ chọn của hệ điều hành; trang đọc được và tự tắt chuyển động |
| tương phản | **contrast ratio** (chuẩn **WCAG**) | tỉ lệ sáng tối giữa chữ và nền ngay dưới chữ; chữ thường cần từ 4,5 : 1, chữ lớn từ 3 : 1 |

## Một đường gọi là một địa chỉ trên máy chủ

Mỗi khi trang cần gì, nó gửi một yêu cầu tới một đường gọi của máy chủ rồi chờ; câu trả lời thường là JSON, riêng ô chat là một luồng tin gửi dần. Chỉ ba đường gọi model (ô chat gửi dần, ô chat trả cả câu, hỏi bằng ảnh); các đường còn lại đọc dữ liệu đã có cho trang hoặc làm việc khác (bảng đủ ở nửa để tra). Đường nào gửi lên dữ liệu thì chỉ nhận đúng khuôn đã định (ví dụ ở "Quyết định nhỏ hơn").

## Trên đường gửi dần, mỗi tin có một tên, và giao diện vẽ theo tên

Khi người dùng gửi câu hỏi, trang mở một yêu cầu gửi lên đường ô chat gửi dần, rồi đọc liên tục cho tới tin "xong". Ví dụ chính (*"Giá vé tham quan Đại Nội Huế là bao nhiêu?"*) nhận lần lượt: ba bốn tin trạng thái, một tin chữ, một tin nguồn, một tin ghi chú ("có thể đã thay đổi"), một tin xong.

| Tin | Máy chủ gửi khi | Giao diện làm gì |
|---|---|---|
| trạng thái | mỗi bước bắt đầu: xếp loại câu, tìm, tìm xong; từ 23/11 tin "tìm xong" mang thêm tên các bài đã tìm thấy; ở lượt có công cụ, "đang viết" chỉ gửi ngay trước chữ đầu | thẻ chờ (khúc sông có con đò) đổi dòng bước và hiện tên các bài đã tìm thấy (chữ nguyên văn, số tên theo cỡ màn: "Chi tiết để tra") |
| chữ | model gửi một mẩu chữ (với Claude: một mẩu duy nhất) | nối mẩu vào ô chữ, vẽ lại tối đa mỗi lần màn hình làm mới; bỏ số nguồn [n] khi vẽ |
| thay chữ | chữ đã hiện cần đổi: model trả chữ dần mà một câu có con số không có nguồn bị gỡ (bài 16), hoặc lượt chạy lại / viết lại (chi tiết ở nửa để tra) | thay cả ô chữ bằng bản cuối |
| nguồn | chữ đã qua bước kiểm số nguồn | vẽ bản cuối, rồi mới hiện khối "Nguồn đã dùng (N bài)": mỗi bài một nút có chấm màu theo chủ đề, bấm mở đoạn trích |
| ghi chú | có dòng "có thể đã thay đổi", hoặc câu an toàn bão lũ | hiện dưới câu trả lời; câu an toàn in đậm, trong khung nền vàng ("Chi tiết để tra") |
| mục web | kho đã từ chối và đã tra web (bài 25) | hiện mục "Từ web (chưa kiểm)" |
| các tin của lịch; thẻ hỏi lại, thẻ chọn điểm thay | lượt lập hay sửa lịch (bài 27, 29, 31); câu thiếu thông tin, lệnh sửa cần người dùng chọn | hiện khung lịch ngay, đổ câu vào từng mục; vẽ các nút, nút chỉ mang giá trị do máy chủ đưa |
| lỗi | lượt hỏng, kể cả khi kiểm số nguồn hỏng sau khi chữ đã hiện | xoá mọi thứ đã hiện; hiện lời báo của máy chủ và nút "Thử lại" |
| xong | lượt kết thúc | ghi kết cục; nếu kho không đủ thì hiện gợi ý cách hỏi |

Luồng đứt mà chưa có tin "xong" thì giao diện coi như lỗi. Bấm "Dừng" hoặc đóng trang thì trang huỷ yêu cầu, và máy chủ dừng lần gọi model.

## Máy chủ nhận ra một cuộc trò chuyện nhờ một mã trong cookie

Để biết câu "còn chỗ đó thì sao?" thuộc cuộc nào, ở lượt hỏi đầu máy chủ tạo một mã ngẫu nhiên dài, cất cuộc trò chuyện dưới mã đó trong bộ nhớ, và gửi mã cho trình duyệt dưới dạng cookie. Từ lượt sau, trình duyệt tự gửi lại cookie; máy chủ tìm đúng cuộc theo mã.

Cookie này có ba giới hạn đặt sẵn: chương trình của trang **không đọc được** nó; trình duyệt chỉ gửi nó cho các đường gọi dữ liệu của chính máy chủ này (các địa chỉ bắt đầu bằng /api), không gửi khi yêu cầu đến từ trang khác; nó hết hạn sau 30 phút. Cookie chỉ mang mã, không mang chữ nào của cuộc trò chuyện.

Mỗi lần trang được tải (hay tải lại), giao diện gọi đường "cuộc trò chuyện mới": máy chủ xoá cuộc cũ khỏi bộ nhớ và đặt một mã mới (mã chỉ thành một cuộc khi có lượt hỏi đầu: "Quyết định nhỏ hơn").

## Chữ model viết đi qua hai lớp chặn trước khi lên màn hình

Câu trả lời là chữ có định dạng (Markdown: in đậm, danh sách, bảng, link) do model viết; trang đổi nó thành HTML để vẽ. Nếu model, vì một chữ lạ chen vào lời dặn (bài 37), viết ra một nhãn ảnh trỏ tới máy khác, trình duyệt sẽ tự tải ảnh đó, và địa chỉ ảnh có thể mang chữ của cuộc trò chuyện ra ngoài (lập luận, không phải số đo).

- **Lớp một, ở giao diện:** trước khi vẽ, chữ được lọc theo một **danh sách cho phép**: chỉ các nhãn Markdown thường tạo ra (đoạn, đậm, nghiêng, danh sách, bảng, tiêu đề, link…). Không có nhãn ảnh. Chỗ duy nhất được mang địa chỉ là địa chỉ của link, và link chỉ mở khi người dùng bấm, ở tab mới. Mục web lọc chặt hơn ("Quyết định nhỏ hơn").
- **Lớp hai, ở trình duyệt:** máy chủ gửi kèm trang một chính sách chặn tải: chương trình, kiểu chữ, ảnh chỉ được tải từ chính máy chủ; không chương trình viết lẫn trong trang; không trang nào được nhúng trang này vào trong nó. Hai ngoại lệ có ghi lý do (nửa để tra): ảnh xem trước của ảnh người dùng vừa chọn, và ô nền bản đồ.

## Lớp nhìn mới chỉ đổi bảng kiểu và hình vẽ, và được kiểm bằng ảnh chụp

Trình duyệt vẽ trang từ ba thứ: HTML (chữ, nút, ô nhập), chương trình của trang (quyết định trang hiện gì, bài 5) và bảng kiểu (màu, cỡ, vị trí). Giao diện "Dòng sông dẫn đường" (vì sao chọn: bài 5) gần như chỉ đổi bảng kiểu và thêm hình vẽ. Chữ của câu trả lời, các nút cũ, luồng và đường xuất file giữ nguyên; chữ mới chỉ có ở thẻ chờ, ở nhãn nguồn và nút "Dừng chuyển động" ở màn đầu (nguyên văn: "Chi tiết để tra"). Máy chủ chỉ đổi một chỗ: tin "tìm xong" mang thêm tên bài.

- **Một bộ biến dùng chung:** mỗi màu, bo góc, bóng, cỡ chữ đặt tên một lần; các trang gọi theo tên. Cỡ chữ trên màn hình lấy từ một thang chín bậc.
- **Con sông và bố cục theo khung nhìn:** con sông là hình vẽ bằng đường cong nhóm tự vẽ, ảnh sông Hương nằm trong dải sông, sáu bến và con đò đặt theo đường cong đó. Màn đầu cao bằng khung nhìn trừ thanh trên (không thấp hơn 520, không cao hơn 800 điểm ảnh), nét sông co theo; màn hẹp thì xếp dọc. Thấp hơn 869 px (gồm máy demo 1536 × 695) thì bến chỉ còn tên, vì dòng mô tả chạm ảnh sông.
- **Giảm chuyển động:** máy bật tuỳ chọn này thì nét sông đứng yên, không có con đò; không bật thì có nút "Dừng chuyển động".

Cách kiểm trước khi gộp (ảnh, kịch bản, tương phản) và cách lùi về giao diện cũ: quyết định 4 và mục "Đã so".

## Quyết định và lý do

### 1. Vì sao mã cuộc trò chuyện nằm trong một cookie mà trang không đọc được?

- **Đã chọn:** máy chủ giữ lịch sử; trình duyệt chỉ giữ một mã ngẫu nhiên trong cookie, với ba giới hạn ở mục trên.
- **Vì sao:** máy chủ giữ lịch sử vì nếu trình duyệt gửi lại "trợ lý đã nói thế này", người dùng sửa được câu đó để cài mệnh lệnh (lý do ghi trong chương trình, bài 6). Ba giới hạn của cookie: chưa thấy ghi lý do riêng. Điều thấy được: giới hạn thứ tư, "chỉ gửi qua kết nối mã hoá", đang tắt khi chạy trên máy (nửa để tra; bài 37).
- **Cách khác:** trang tự giữ mã và gửi kèm câu hỏi: chưa thử.
- **Cái giá:** cookie chung cho mọi tab của cùng một trình duyệt: mở trang ở tab thứ hai thì máy chủ xoá cuộc của tab thứ nhất, kể cả lịch đã lập (bảng "Nếu… thì sao"; chi tiết ở nửa để tra).

### 2. Vì sao chặn chữ model bằng hai lớp, và lớp lọc là danh sách cho phép?

- **Đã chọn:** lớp lọc ở giao diện chỉ giữ đúng các nhãn Markdown thường tạo ra, mọi thứ khác bị bỏ; cộng một chính sách chặn tải ở trình duyệt.
- **Vì sao:** lý do ghi trong chương trình, từ một vòng rà bảo mật: ngoài chặn chương trình lạ, trang không được tự tải gì từ máy khác khi hiện chữ. Danh sách cấm dễ sót một nhãn; danh sách cho phép thì nhãn lạ nào cũng bị bỏ. Chính sách chặn tải là để chặn mọi tải từ máy khác **kể cả khi** chữ lọt qua bộ lọc (lý do ghi trong chương trình).
- **Cách khác:** bộ lọc với danh sách cấm: là bản trước vòng rà đó, đã thay. Chỉ dựa vào bộ lọc: không làm.
- **Cái giá:** model không chèn được ảnh vào câu trả lời; ảnh dưới câu trả lời (bài 26, 30) do chương trình gắn riêng. Thêm thứ gì từ ngoài (một kiểu chữ, một bản đồ khác) đều phải sửa chính sách trên máy chủ.

### 3. Vì sao đường báo tình trạng chỉ đọc trạng thái lúc bật, không hỏi thử Qdrant hay hãng model?

- **Đã chọn:** đường báo tình trạng trả trạng thái máy chủ ghi lại lúc bật: Qdrant, bước tìm, bộ đếm token, model viết; đủ cả thì "ok", thiếu một thì báo thiếu phần nào.
- **Vì sao:** chưa thấy ghi lý do. Điều thấy được: kế hoạch lúc dựng máy chủ ghi "không thêm lần gọi thử hay kiểm nhà cung cấp" cho đường này.
- **Cách khác:** mỗi lần được hỏi thì gọi thử Qdrant và hãng model: không làm (quyết định đã ghi).
- **Cái giá:** đã thử 22/11: Qdrant ngừng giữa chừng mà nó vẫn báo "ok"; khoá model hết hạn cũng vậy. Muốn biết còn trả lời được không, phải hỏi thử một câu thật.

### 4. Vì sao giao diện mới chỉ được gộp sau khi chụp ảnh ở tám cỡ khung nhìn?

- **Đã chọn:** một chương trình điều khiển trình duyệt chụp mọi trang và trạng thái chính ở tám cỡ, từ điện thoại 390 px tới máy demo 1536 × 695; máy đo chỗ tràn, chỗ bị cắt; người mở ảnh. Gộp khi màn đầu trọn ở bốn cỡ máy xách tay và bảng so cặp không còn điểm hỏng mới.
- **Vì sao:** chủ dự án khi giao việc (17:16 22/11) dặn kiểm bằng trình duyệt tự động, có ảnh chụp màn hình làm bằng chứng, thao tác mọi trang, mọi tính năng; cỡ 1536 × 695 là màn hình máy demo. Lớp nhìn đổi ở mọi trang mà bộ test của máy chủ không thấy màn hình. Cả bốn lỗi chặn chỉ lộ trên ảnh hoặc bản in thử; lỗi cuối lộ ra khi nhóm tự mở ảnh 1280 px và hai bản phê bình của model khác hãng cùng nêu.
- **Cách khác:** gộp tối 22/11 sau khi chữa ba lỗi chặn đầu: không làm, nhóm hoãn sang 23/11 (quyết định đã ghi).
- **Cái giá:** giao diện vào nhánh chính chậm một đêm. Ảnh vẫn là trình duyệt tự động trên máy: chưa ai thử điện thoại thật, chưa ai in bằng tay.

## Nếu… thì sao

Một tình huống kể trọn. Người dùng đang chờ thì mạng chập; luồng đứt trước tin "xong". Giao diện xoá phần đã hiện, hiện "Kết nối bị gián đoạn. Vui lòng thử lại." và nút "Thử lại". Máy chủ dừng lần gọi model, không nhớ lượt này. Bấm "Thử lại" thì trang gửi lại đúng câu đó, vẫn cùng cuộc.

Lời báo là nguyên văn; các dòng đọc từ chương trình, chưa thử thật, trừ dòng có chữ **(đã thử)** (bài 6).

| Nếu | Người dùng thấy gì | Muốn hết lỗi thì ai làm gì |
|---|---|---|
| không kết nối được máy chủ (máy chủ tắt) | "Không kết nối được máy chủ. Vui lòng thử lại." | người vận hành bật máy chủ (bài 36) |
| luồng đứt giữa chừng | "Kết nối bị gián đoạn. Vui lòng thử lại." | người dùng bấm "Thử lại" |
| người dùng bấm "Dừng" | "Đã dừng. Phần trả lời chưa xong nên không hiện (chưa kiểm nguồn)." | — |
| không tải được danh sách tính năng lúc mở trang | trang chạy như mọi tính năng đều tắt: không biểu mẫu lập lịch, không dòng thời tiết, không nút gửi ảnh | tải lại trang |
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
<summary>4. Mở trang trên máy demo 1536 × 695, các bến ở màn đầu chỉ còn tên. Vì sao?</summary>

Khung nhìn thấp hơn 869 px thì hình sông bị nén dọc; dòng mô tả của hai bến cuối chạm ảnh sông, tương phản còn 1,8 : 1. Bảng kiểu ẩn dòng mô tả ở các khung nhìn đó; nhóm nhận cách này khi gộp.

</details>

## Cấu hình đang chạy

*Theo chương trình trưa 22/11/2026; bảng thứ hai theo nhánh chính sáng 23/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Hạn cookie và hạn cuộc trò chuyện | 30 phút từ lượt cuối | bài 23 | — |
| Kho cuộc trò chuyện | nhiều nhất 500 cuộc, quá thì bỏ cuộc cũ nhất | trần bộ nhớ | — |
| Cookie: không cho trang đọc · chỉ gửi trong cùng trang · chỉ gửi cho `/api` | bật | quyết định 1 | — |
| `HUE_COOKIE_SECURE` | chưa đặt (tắt) | cookie chỉ đi qua kết nối mã hoá; bật khi đưa lên mạng | — |
| Danh sách nhãn HTML cho phép khi lọc chữ | đoạn, xuống dòng, kẻ ngang, đậm, nghiêng, gạch, mã, khối trích, danh sách, tiêu đề, link, bảng | quyết định 2 | thay bộ lọc danh sách cấm |
| Chính sách chặn tải | mọi thứ từ chính máy chủ; thêm ảnh xem trước, và ô bản đồ vì tính năng bản đồ đang bật | quyết định 2 | — |
| Vẽ lại ô chữ | nhiều nhất một lần mỗi khung hình | theo bản đặc tả chữ hiện dần (01/11); chỉ có tác dụng khi model gửi nhiều mẩu | — |
| `HUE_TAT_DOCS` | chưa đặt | tắt trang mô tả các đường gọi tự sinh của thư viện máy chủ; bật khi đưa lên mạng (bài 37) | — |

**Lớp nhìn "Dòng sông dẫn đường":**

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Thang cỡ chữ | 13 · 14 · 15 · 17 (điện thoại 16) · 19 · 22 · 28 · 34 · 44 px; tiêu đề màn đầu 40–62 px theo bề rộng | một thang cho cả sản phẩm; 13 px giữ cho nhãn chật (thanh đáy điện thoại, số trong chấm bản đồ), 15 px là chữ phụ của khoảng 30 chỗ (chú thích trong chương trình) | trước 22/11: 39 cỡ gõ tay; bản in giữ cỡ cũ (bài 30) |
| Màu chính | nền sương, chữ mực, xanh ngọc (nút), nước sâu (mục đang chọn), sen (nút trợ lý nổi), nắng chiều (chỉ con đò và gạch chân, không làm chữ) | giữ tên biến của giao diện trước để các trang cũ không phải đổi | trước 22/11: 16 biến, nhưng 68 mã màu khác nhau gõ tay |
| Màu chủ đề | năm màu: ẩm thực · di tích · lễ hội · đi lại · nghệ thuật (+ một màu "khác") | chấm trước tên nguồn và tên bài lúc chờ; màu theo thư mục đầu của mã bài | — |
| Bo góc, bóng | 4 cỡ bo góc, 3 kiểu bóng | trước 22/11: 20 kiểu bo góc, 18 kiểu bóng gõ tay | — |
| Chiều cao màn đầu | khung nhìn trừ thanh trên, không thấp hơn 520 và không cao hơn 800 px | sáu bến, ô hỏi, dòng thời tiết nằm trọn màn đầu máy xách tay; bề dày nét sông = 250 px × (chiều cao / 800) | trước: cố định 800 px, bến cuối và dòng thời tiết bị cắt |
| Bố cục dọc | bề rộng ≤ 1.140 px | dưới mốc này cột chữ và con sông chữ S không đủ chỗ đứng cạnh nhau | trước: ép bố cục rộng, nhãn bị cắt / đè (mục "Đã so") |
| Bến chỉ còn tên | khung nhìn thấp hơn 869 px, hoặc rộng 1.141–1.360 px | dòng mô tả chạm ảnh sông hoặc dòng thời tiết (đo 1,8 : 1 ở 1536 × 695; 3,0 : 1 ở 1141 × 900) | ba cách giữ dòng mô tả ở màn thấp đã thử, đều không dùng được: hai cách để lọt chỗ chạm, cách thứ ba tắt mô tả ở mọi cỡ |
| Câu gợi ý ở màn đầu | 5; khung nhìn cao tới 720 px: 4 | dòng thời tiết kết thúc trên mép đáy | — |
| Thẻ chờ | tối đa 6 tên bài, phần còn lại gộp thành "+k bài"; điện thoại và khung trợ lý nổi: 3 tên, mỗi tên một dòng; khung nhìn cao tới 700 px (máy demo 1536 × 695): 3 tên, xếp nối nhau như màn rộng; ở cả hai nhóm này không có dòng "+k bài", tổng số bài vẫn ghi ở dòng nhãn | ô nhập và nút "Dừng" còn trong màn đầu suốt lúc chờ | trước: 6 tên, mỗi tên hai dòng (mục "Đã so") |
| Giảm chuyển động | máy bật ⇒ không bật lớp hiệu ứng, mọi chuyển động tắt, không vẽ con đò, không có nút dừng | — | — |
| Nút "Dừng chuyển động" | có khi máy không bật giảm chuyển động | con đò và nét chạy là chuyển động tự chạy quá 5 giây (chú thích trong chương trình) | — |

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
| thời tiết | lấy về | không | dòng thời tiết ở màn đầu Trang chủ (dưới các câu gợi ý); lỗi thì dòng ẩn |
| tính năng đang mở | lấy về | không | mọi trang, một lần lúc mở |
| lịch mẫu | lấy về | không | trang Lên kế hoạch lúc chưa xếp |
| bản đồ · chỗ ở | lấy về | không | trang Bản đồ, trang Chỗ ở, thẻ khách sạn |
| theo dõi | lấy về | không | trang theo dõi của chủ dự án, cần khoá (bài 34) |
| tình trạng | lấy về | không | người vận hành, bộ bật hệ thống (bài 36) |
| trang và file của giao diện | lấy về | không | trình duyệt, khi mở trang |

## Đã so

**Vấn đề thật:** giao diện mới đổi lớp nhìn ở mọi trang (22/11), còn bộ test của máy chủ không thấy màn hình. Câu cần trả lời trước khi gộp: người dùng có còn thấy đủ chữ, nút, nguồn, câu cảnh báo, lịch, file xuất như bản cũ không, ở các cỡ màn hình thật hay dùng.

**Cổng gộp** (bản gộp thử của giao diện mới với nhánh chính, chạy trên máy, server thật, model Claude Sonnet 5.5; 22/11 tối và 23/11 sáng; phiên đo chạy, nhóm tự mở ảnh; hàng nào đo trên bản khác thì ô "Trên gì" hoặc "Kết quả" ghi rõ):

| Phép kiểm | Trên gì | Kết quả |
|---|---|---|
| Ảnh chụp tự động | 49 cảnh (trang tĩnh, hỏi đáp, lúc chờ, hỏi bằng ảnh, lịch, sửa lịch, màn lỗi, trang theo dõi) × tám khung nhìn: 1440 × 900, 1536 × 695, 1536 × 730, 1366 × 650, 1280 × 620, 1024 × 768, 768 × 1024, 390 × 844 | 761 ảnh, 0 cảnh không chụp được; máy dò tràn ngang và chữ bị cắt gắn cờ 1 ô: thẻ chọn tên ảnh ở 390 px, chữ thò ra mép phải (có từ giao diện cũ; sửa sau gộp, vào nhánh chính 11:26 23/11: tên dài xuống dòng; chụp lại nhóm hỏi bằng ảnh ở 390 px (3 cảnh): 0 ô tràn; khoảng trắng phía trên thẻ vẫn còn — bài 26) |
| Màn đầu nằm trọn khung nhìn (máy đo từng bến, ô hỏi, dòng thời tiết) | tám khung nhìn | trọn ở 1440 × 900, bốn cỡ máy xách tay và 390 × 844; không trọn ở 1024 × 768, 768 × 1024 (ngoài điều kiện gộp) |
| Kịch bản thao tác đủ | 50 bước: hỏi, hỏi tiếp, từ chối, thời tiết, khoảng cách, xếp lịch, sửa lịch, tải file, in, mở từng trang, màn lỗi | 49 đạt, 1 bước để người xem ảnh (trang Chỗ ở), 0 trượt |
| File xuất | một lịch 2 ngày: .txt, PowerPoint, PDF in | .txt 29 dòng, PowerPoint 4 slide (bằng bản cũ); PDF 2 trang |
| So cặp ảnh cũ ↔ mới | bốn nhóm (trang tĩnh, hỏi đáp, lịch; lúc chờ + tin dài), ba agent con chỉ đọc ảnh và phiên đo, ghép cũ cạnh mới; so với các bản dựng tối 22/11, trước các lần sửa cuối, không trên bản gộp | các điểm "hỏng mới" ghi được đều đã chữa trước gộp (bảng dưới) |
| Tương phản chữ / nền | 24 màn ở bốn bề rộng (19:56 22/11) | 1.523 phép, 0 dưới ngưỡng (13 phép thuộc ô đang khoá, chuẩn không đòi) — trên bản dựng 19:56 22/11; đo lại trên bản đã gộp, có thêm sáu cỡ máy xách tay: 1.850 phép, 0 dưới ngưỡng |
| Cả bộ test | 86 file, từng file, không nạp khoá (09:41–09:59 23/11) | 4 file bỏ (cần khoá OpenAI), 82 file chạy đều thoát 0, 2.218 ca đạt |

**Lỗi bắt được trước khi gộp** (bốn dòng đầu là lỗi chặn):

| Lỗi | Thấy bằng gì | Chữa thế nào |
|---|---|---|
| Màn đầu vỡ ở khổ giữa: 1280 px một nhãn bến bị cắt ở mép màn, 1024 px nhãn đè câu dẫn, 768 px ô hỏi đè sông | ảnh; sau đó một chương trình kiểm 20 bề rộng 360–2560 px | ≤ 1.140 px chuyển sang bố cục dọc; 1.141–1.340 px nhãn tự xuống dòng theo chỗ còn lại |
| Bản in đổi tỉ lệ: chữ in to lên 22 %, lịch ví dụ từ 2 trang thành 3 | in thử ra PDF | ghim tỉ lệ in bằng luật, giữ cỡ chữ in cũ (bài 30) |
| Kiểu chữ của câu trả lời rò sang trang một bài của Khám phá: bài bị bó cột 64 ký tự, bảng giá 5 cột vỡ thành từng ký tự, mất chấm đầu dòng; một cụm đậm giữa câu bị vẽ như tiêu đề | ảnh trang bài | luật mới chỉ áp cho câu trả lời; tiêu đề phần chỉ khi cả đoạn là một cụm đậm |
| Màn đầu không vừa một khung nhìn máy xách tay: cao cố định 800 px, bến cuối và dòng thời tiết bị cắt ở đáy (1280 px) | nhóm tự mở ảnh; hai bản phê bình khác hãng | màn đầu cao theo khung nhìn, kẹp 520–800 px |
| Năm nhóm cặp chữ / nền dưới ngưỡng (lần đo đầu báo sáu, một là báo nhầm của phép đo), ví dụ cuối dòng mô tả bến "Đi lại" chạm ảnh sông (1,0 : 1); ba nhóm có sẵn ở bản cũ | phép đo tương phản | dời nhãn bến; phủ đều một lớp màu trên ảnh đầu trang Lên kế hoạch, Khám phá ở màn ≤ 1.040 px; số đếm trên nút lọc bớt mờ |
| Điện thoại: thẻ chờ sáu tên bài, mỗi tên hai dòng, đẩy ô nhập và nút "Dừng" ra khỏi màn đầu suốt 25–34 giây chờ | ghi chung một lần sửa với các điểm từ bản phê bình khác hãng | ba tên bài, mỗi tên một dòng |
| Lên kế hoạch: cột biểu mẫu thu hẹp làm nút "Xếp lịch" tụt khoảng 400 px; khối "Đã sửa theo lời bạn" lấn sang cột bản đồ; quán không ảnh lệch hàng | so cặp ảnh | bài 27 |

**Đọc bảng thế nào:** theo lời các lần sửa, mỗi lỗi ở bảng thứ hai được thấy trên ảnh, bản in thử, phép đo trên trang đã dựng hoặc bản phê bình; không lỗi nào do bộ test báo. Kịch bản thao tác đủ và file xuất cho biết luồng và chữ không đổi; ảnh cho biết chỗ đặt.

**Đã chọn:** gộp lúc 10:00 23/11, sau khi màn đầu trọn ở bốn cỡ máy xách tay, bảng so cặp không còn điểm hỏng mới, và nhóm nhận "bến chỉ còn tên" ở khung nhìn thấp. Lùi về giao diện cũ (chuyển từ thân bài 23/11): hoàn tác đúng lần gộp, dựng lại file giao diện, bật lại máy chủ.

**Giới hạn của phép đo:** trình duyệt tự động trên máy, không phải điện thoại thật; trình duyệt chụp chạy tiếng Anh nên ô ngày hiện kiểu tháng / ngày / năm (suy luận của nhóm); chưa ai in bằng tay; tương phản chưa đo thẻ lịch đã xếp, khung trợ lý nổi, màn lỗi; bản in chưa có cặp cùng một lịch cũ ↔ mới (bài 30). Ảnh chụp (09:25) và kịch bản (09:32) chạy trên bản gộp thử dựng từ nhánh chính lúc mở phiên sáng 23/11, trước khi ba bản sửa nhỏ của lõi sáng hôm đó vào nhánh chính; ba bản sửa đó không chạm giao diện, và lượt cả bộ test có đủ cả ba.

## Quyết định nhỏ hơn

**Vì sao tải lại trang thì máy chủ quên cuộc cũ?** (trước 23/11 là quyết định 2 của bài) **Đã chọn:** mỗi lần trang được tải, giao diện xin một cuộc mới; lỗi mạng ở bước này thì bỏ qua, vẫn cho hỏi. **Vì sao:** lý do ghi trong chương trình: trước đây sau khi tải lại trang, câu đầu được model đọc như câu hỏi tiếp của cuộc cũ; chủ dự án gặp ngày 15/11, một câu vừa trả lời đúng bị từ chối. **Cách khác:** giữ cuộc qua lần tải lại, vẽ lại các lượt cũ: chưa thử. **Cái giá:** tải lại trang là mất cuộc và lịch đang giữ. Trước trưa 22/11, mỗi lần tải trang còn chiếm một chỗ trong kho 500 cuộc (đã sửa; đoạn dưới).

**Vì sao hai yêu cầu cùng một cuộc không phải xếp hàng?** Chú thích trong chương trình: kho cuộc trò chuyện không khoá; hai yêu cầu cùng cuộc chạy song song thì lượt xong sau ghi sau, vì thiết kế cho một người dùng mỗi cuộc. Cái giá: hai tab dùng chung một cuộc (quyết định 1) có thể ghi đè lượt của nhau.

**Vì sao mục web lọc chặt hơn câu trả lời chính?** Mục web dùng một danh sách cho phép không có nhãn link: link của mục web chỉ lấy từ sổ nguồn do chương trình dựng (bài 25). Câu trả lời chính vẫn cho link (bài 37).

**Vì sao mở cuộc mới không còn chiếm chỗ trong kho 500 cuộc?** Đợt rà bảo mật trước khi đưa lên mạng (22/11) thấy: giao diện gọi "cuộc mới" ở mỗi lần tải trang, mỗi lần chiếm một chỗ, nên 500 lần gọi của bất kỳ ai đẩy mọi cuộc đang có, kèm lịch đã lưu, ra khỏi kho. Nay mã mới chỉ thành một cuộc khi có lượt hỏi đầu tiên. Cái giá: không có.

**Vì sao lỗi luôn hiện bằng một câu tiếng Việt cố định?** Lý do ghi trong chương trình: lỗi mạng hay lỗi đọc dữ liệu mang chữ kỹ thuật tiếng Anh của trình duyệt; giao diện không hiện chữ đó mà đổi sang một câu cố định. Lỗi do máy chủ gửi thì giữ nguyên lời của máy chủ.

**Vì sao trang danh sách bài chỉ nhận mã bài trùng nguyên chuỗi?** Lý do ghi trong chương trình: không ghép đường dẫn file từ chữ người dùng gửi lên, nên không đọc được file nào ngoài danh sách bài đã kiểm lúc bật; mã có chữ "sealed" hay trỏ vào thư mục không phải bài bị chặn thêm một lớp. Đường "báo thông tin chưa đúng" cũng vậy: chỉ nhận mã một bài trùng nguyên chuỗi một bài có thật, không nhận chữ tự do.

**Vì sao lớp nhìn mới không dùng hình nhúng thẳng trong bảng kiểu?** Chú thích trong chương trình: chính sách chặn tải (quyết định 2) không cho dạng đó, nên các hình nhỏ (vạch sông trên khối nguồn, hình khối "chưa có", hình sông ở trang Trợ lý lúc trống) là file nằm trên chính máy chủ. Cái giá: không có; chính sách không phải nới.

**Vì sao luật mới nằm trong một file nạp sau cùng, thay vì sửa từng file cũ?** Chú thích trong chương trình: file mới thắng luật cũ cùng tên mà không phải sửa mọi file gốc trong một lần; khi bản mới đứng yên thì gộp dần về file gốc. Cái giá: một số luật cũ còn nằm đó nhưng bị đè.

**Vì sao dòng thời tiết ở Trang chủ lỗi thì ẩn, không hiện số cũ?** Cùng luật của công cụ thời tiết: lỗi thì không bao giờ đưa ra con số (bài 24).

## Giới hạn đã biết

- **Đường báo tình trạng không biết hệ thống có đang trả lời được không** (quyết định 3; đã thử với Qdrant).
- **Hai tab cùng trình duyệt dùng chung một cuộc**, và tab mở sau xoá cuộc cùng lịch của tab trước (đã xác nhận bằng một lượt thử thật trưa 22/11).
- **Tải lại trang là mất cuộc và lịch đang giữ**; không có lời báo.
- **Đường đánh giá một lượt có ở máy chủ nhưng giao diện chưa dùng.**
- **Ở khung nhìn thấp hơn 869 px (gồm máy demo 1536 × 695) các bến màn đầu chỉ còn tên, mất dòng mô tả**; nhóm nhận khi gộp, không vẽ lại (bài 5).
- **Ở 1024 × 768 và 768 × 1024 màn đầu không trọn một khung nhìn**: bến cuối hoặc dòng thời tiết nằm dưới đáy (ngoài điều kiện gộp).
- **Giao diện mới chưa ai thử trên điện thoại thật**; ảnh 390 px là trình duyệt tự động đặt cỡ điện thoại.
- **Ảnh và kịch bản của cổng gộp chạy trước ba bản sửa nhỏ của lõi sáng 23/11**; ba bản đó không chạm giao diện, lượt cả bộ test có đủ cả ba.

## Chi tiết để tra

- Việc tab mở sau xoá cuộc trò chuyện và lịch của tab mở trước đã được xác nhận bằng một lượt thử thật ở lượt kiểm chốt trưa 22/11.
- Mã cuộc trò chuyện: 16 byte ngẫu nhiên viết thành chữ; mã lạ hoặc hết hạn thì máy chủ cấp mã mới và đặt lại cookie. Cookie đi theo cả phản hồi lỗi, để lượt đầu lỗi không để lại cuộc mồ côi.
- Đường ô chat gửi dần: lỗi trước khi mở luồng (bước tìm hay model viết chưa sẵn sàng) thì trả JSON lỗi; từ lúc mở luồng, xếp loại câu và tìm chạy bên trong luồng, nên Qdrant lỗi giữa lượt thành một tin "lỗi" mang câu "Hệ thống tra cứu tạm thời không khả dụng.".
- Tin "chữ" có số thứ tự; giao diện bỏ mẩu có số cũ hơn mẩu đã nhận. Chữ đang tới có thể dừng giữa một mã nguồn ("… [1"), nên phần mã dở ở cuối cũng bị bỏ khi vẽ.
- Thứ tự số ở dòng "Nguồn" đánh theo lần xuất hiện đầu tiên của mã trong câu trả lời.
- Đường đánh giá một lượt (khi được gọi) chỉ ghi một dòng sổ: mã lượt ngẫu nhiên, tuyến, kết cục, số nguồn, đánh giá; không chữ, không mã cuộc. Đường báo thông tin chưa đúng chỉ ghi mã bài.
- Trang mô tả các đường gọi tự sinh (`/docs`) còn mở khi chạy trên máy; thiết lập lúc chạy `HUE_TAT_DOCS` tắt nó.
- Khi bộ giới hạn lượt bật, ba đường gọi model và đường tải PowerPoint bị đếm theo địa chỉ mạng (bài 37).
- Hai tab (chi tiết của quyết định 1): mở trang ở tab thứ hai thì câu hỏi tiếp ở tab thứ nhất được trả lời như câu đầu của một cuộc mới (không còn nhớ câu trước, lịch đã lập cũng mất, nút tải PowerPoint báo hết hạn); từ đó hai tab dùng chung một cuộc (suy từ chương trình).
- Giới hạn thứ tư của cookie, "chỉ gửi qua kết nối mã hoá", để tắt khi chạy trên máy vì trang trên máy mở bằng địa chỉ không mã hoá; bật bằng thiết lập lúc chạy `HUE_COOKIE_SECURE` (bài 37).
- Hai ngoại lệ của chính sách chặn tải: ảnh người dùng vừa chọn để gửi (trình duyệt tự tạo bản xem trước, không tải từ đâu) và, vì tính năng bản đồ đang bật, ô nền bản đồ từ một máy chủ bản đồ công cộng. Danh sách thứ trang không được tự tải từ máy khác khi hiện chữ, theo vòng rà bảo mật: ảnh, nền, kiểu chữ có địa chỉ, ô nhập dạng ảnh, biểu mẫu.
- Tin "thay chữ" với model đang chạy: từ 22:06 22/11 phép kiểm số (bài 24) không còn làm trang nhận tin này, vì chữ chỉ được gửi sau khi đã gỡ câu sai (bài 6). Ở lượt có công cụ, chữ được giữ tới khi qua kiểm, nên khi có tin "lỗi" thường chưa có chữ nào trên màn hình.
- Tên bài trong thẻ chờ là bài đã có đoạn vào ngữ cảnh của lượt, chưa chắc được trích trong câu trả lời (nhãn ghi "Đã tìm thấy", không ghi "đã dùng"); không tính nguồn do chương trình dựng (thẻ nơi, mục lục, gần một điểm, khoảng cách, lịch, thời tiết). Bấm tên mở bài ở tab mới. Dòng bước không còn kèm số đoạn như bản cũ. Lý do thêm tên bài (lời lần sửa phía máy chủ): tin dài chờ 22–30 giây, các tin trạng thái dồn vào 5–10 giây đầu, lần viết cuối im 17–20 giây.
- Nét sông dùng chung ở ba nơi: màn đầu Trang chủ (dải sông chứa ảnh, sáu bến, con đò đi hết đường trong 44 giây), thẻ chờ (khúc sông nằm ngang có con đò), đường nối các điểm trong ngày của thẻ lịch (bài 27). Trang Trợ lý lúc chưa hỏi gì có hình một khúc sông bốn bến và lời chào ở giữa.
- Sáu bến ở màn rộng được đặt tay theo hình sông (vị trí dọc dòng, bờ nào, nhãn nằm phía nào), chọn sao cho chữ nằm trên nền sương, không đè ảnh và không đè cột chữ.
- Chữ trong câu trả lời: chương trình của trang (sau bộ lọc) gắn kiểu riêng cho khối "Tư liệu chưa có thông tin về…", cho đoạn tiêu đề phần, và vẽ đậm, đều cột các con số giá, giờ; chữ không đổi. Câu từ chối nằm trong thẻ nền sương viền đứt.
- Phép đo tương phản: trình duyệt không đầu mở bản dựng tĩnh với dữ liệu mẫu; với mỗi đoạn chữ đang hiện, lấy màu chữ đã tính (nhân cả độ mờ), chụp lại trang với chữ trong suốt để lấy nền thật từng điểm ảnh dưới chữ, ghi tỉ lệ thấp nhất. Chạy lại trên đúng bản đã gộp, có thêm sáu cỡ máy xách tay: 1.850 phép, 0 dưới ngưỡng (phiên giao diện tự báo).
- Kiểu chữ tải từ chính máy chủ (đóng gói cùng giao diện), nên chính sách chặn tải không phải nới.
- Biểu tượng trang (hình nhỏ trên thẻ của trình duyệt, cạnh tên trang): từ 11:45 23/11 là một hình tròn xanh với hai nét sóng trắng, file nằm trên chính máy chủ, nên chính sách chặn tải không phải nới. Trước đó trang không khai biểu tượng; trình duyệt tự xin một file không có và máy chủ báo không thấy ở mỗi lần tải trang (lượt "dùng như người thật" sáng 23/11 thấy trong nhật ký của trình duyệt; bài 38). Bằng chứng: đọc chương trình, máy kiểm bản dựng có file biểu tượng cùng dòng trang trỏ tới nó; và lượt trình duyệt do công cụ tự lái 12:34–12:41 23/11 trên nhánh chính: trình duyệt tải được file biểu tượng (6 lần, không lần nào lỗi), console 0 lỗi — lượt đó đã đi đủ các bước, do một agent con chạy, chưa có người thứ hai kiểm; chưa ai chạy lại, chưa ai nhìn hình bằng mắt.
- Thẻ "Hôm nay ở Huế" ở Trang chủ (từ 13:32 23/11; bài 5, quyết định 5): không có đường gọi mới. Trang chủ dùng lại danh sách bài mà giao diện đã lấy từ đường gọi danh sách bài (bảng "Mọi đường gọi", hàng "danh sách bài"); phép chọn bài của ngày chạy trong trình duyệt: lấy thời điểm hiện tại theo đồng hồ của máy người dùng, tính theo giờ quốc tế rồi cộng 7 giờ — máy đặt múi giờ nào cũng ra ngày Việt Nam; chỉ máy chạy sai đồng hồ mới thấy bài của ngày khác. Bài được chọn khi Trang chủ hiện ra; trang để mở qua nửa đêm giữ bài cũ tới khi tải lại hoặc rời Trang chủ rồi quay lại (đọc từ chương trình, chưa thử). Phép chọn nằm trong một file riêng, không lẫn vào trang, để chạy thử được bằng Node mà không phải dựng giao diện. Danh sách chưa tới hay lỗi thì không vẽ thẻ.
- Chuyển từ thân bài 23/11 (chi tiết của lớp nhìn mới, không đổi nội dung):
  - Thẻ chờ, chữ nguyên văn: với Claude, phần lớn lúc chờ là "Đã tìm trong kho, đang chuẩn bị câu trả lời…", dưới đó "Đã tìm thấy N bài — bấm tên để đọc trong lúc chờ" và tối đa 6 tên bài; ở điện thoại, khung trợ lý nổi và cửa sổ cao tới 700 điểm ảnh (như máy demo): 3 tên. Ở điện thoại và khung nổi, dòng nhãn chỉ ghi "Đã tìm thấy N bài" và mỗi tên một dòng; ở máy demo ba tên xếp nối nhau như màn rộng; ở cả hai chỗ không có dòng "+k bài" (bảng "Lớp nhìn" ở "Cấu hình đang chạy").
  - Chữ mới trên màn hình, nguyên văn: thẻ chờ "Đã tìm thấy N bài — bấm tên để đọc trong lúc chờ" và "+k bài"; nhãn nguồn "Nguồn đã dùng (N bài)" (trước là "Nguồn:"); nút "Dừng chuyển động" / "Chạy tiếp" ở màn đầu.
  - Năm chủ đề của kho có năm màu cho chấm trước tên nguồn; trước đó trang có 39 cỡ chữ gõ tay (bảng "Lớp nhìn").
  - Hình sông: chương trình đo điểm trên đường cong để đặt sáu bến lên mép bờ (ở màn rộng; ở bố cục dọc, từ 1.140 px trở xuống, bến nằm giữa dòng), đo lại khi cửa sổ đổi cỡ; con đò đi dọc đường cong. Hẹp từ 1.140 px trở xuống thì màn đầu xếp dọc.
  - Câu an toàn bão lũ: in đậm, trong khung nền vàng có vạch cam bên trái.
  - Các đường gọi không gọi model làm: mở cuộc mới, tải PowerPoint, báo sai, theo dõi, tình trạng, và đọc dữ liệu cho trang (bảng "Mọi đường gọi của máy chủ"). Mã cuộc mới chỉ thành một cuộc trong kho 500 cuộc khi có lượt hỏi đầu tiên. Mục web lọc chặt hơn câu trả lời chính: không cho cả link.
  - Tương phản đo trên trang đã dựng, với nền thật dưới từng đoạn chữ; lần đo trên bản đã gộp có 1.850 phép, 0 dưới ngưỡng, lần đầu có đủ sáu cỡ máy xách tay (cách đo: gạch "Phép đo tương phản" bên dưới; lần đo trước đó: bảng "Cổng gộp").

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
- Hàng "thay chữ" (sửa 22:25 22/11/2026, bản trước chỉ có ví dụ phép kiểm số): nguồn của tin `thay_chu` — `backend/api/routes/chat.py` `finish` dòng 730–747 (chữ cuối không phải tiền tố của chữ đã phát), dòng 792 (lượt chạy lại sau khi bị rút); `backend/llm/assistant.py` dòng 2110–2116 (bản viết lại khi không gom chữ: `"thay_chu" if cho_kiem is None`), dòng 2121–2125 (từ commit `70ba72d5`, gộp `dc43cc93` 22:06: chữ gom phát ở dạng đã gỡ ⇒ không còn khác chữ cuối) [code, đọc main `404448a8`; không chạy test]. Giao diện thay cả ô: `frontend/src/chat.jsx` dòng 152–156 [code].

- Kết quả lượt kiểm chốt buổi trưa 22/11 (phiên điều phối báo, phiên đo chạy; người viết chép từ tin, chưa tự mở file kết quả) [đã chạy].

- Đợt 12:19 23/11/2026 (khớp hai bản sửa sau gộp; nửa để hiểu không đổi chữ ngoài dòng Cập nhật — dòng cũ: "11:17, ngày 23/11/2026 · khớp hệ thống sáng 23/11 (giao diện mới, 48 tính năng, kho 267 bài) · thêm lớp nhìn mới: dựng bằng gì, kiểm thế nào, lỗi nào bắt được trước khi gộp; …"): (1) hàng "Ảnh chụp tự động" của "Đã so": commit `e4c41d3e` (11:15, `frontend/src/index.css` khối ≤ 760 px, `.hoi-anh-the` cột `minmax(0, 1fr)`, nút xuống dòng), gộp `5bddb089` 11:26 [code; đã chạy lệnh git]; chấm `data/thu_bedrock_2026-11-21/harness/e_cham_quan_bua_2311/CHAM_E.md` mục 3, mục 4 điểm 4 + ảnh `anh_390/A01_the_chon_ten_anh_390_man.png` [riêng tư; đã mở ảnh]. (2) biểu tượng trang: commit `0210487d` (11:44: `frontend/index.html` thêm `<link rel="icon" type="image/svg+xml" href="/favicon.svg">`, file `frontend/public/favicon.svg` — hình tròn màu `#0E6B66`, hai đường sóng trắng; có cả ở `frontend/dist/`), gộp `e2dca9ee` 11:45 23/11/2026 [code; người viết đọc file]; 404 trước sửa: `data/playwright_mcp/luot_2311/NHAT_KY.md` dòng 10:36 và 11:08 ("console: 1 lỗi (`favicon.ico` 404)") [riêng tư; đã mở]; mức kiểm "chỉ đọc code; máy kiểm bản dựng có file và trang trỏ tới nó; chưa ai mở trình duyệt": lời phiên viết code 12:10 23/11 chuyển qua phiên D [chép]. Biểu tượng KHÔNG vào nửa để hiểu: bài đang vượt đích độ dài và đây không phải hành vi người dùng cần giải thích.

**Nguồn của phần giao diện mới (thêm 23/11/2026, đọc main `20f998f4`; người viết không chạy server, không dựng giao diện):**
- Lịch sử sửa bài (chuyển từ dòng "Cập nhật" 23/11): bản 22/11 (bản cuối 22:25) — đường gọi, loại tin, cookie đọc từ chương trình; thử thật đường báo tình trạng lấy từ bài 6; phần viết 22/11 đã qua một lượt đối chiếu độc lập. 10:22 23/11 thêm lớp nhìn mới, thẻ chờ, khối nguồn theo giao diện mới. 11:17 23/11 áp biên bản kiểm độc lập `data/hoc_cung_D/kiem/dot_2311_k1_kiem.md` bài 35 (sửa 1.523 ⇒ 1.850 phép là lần đo trên bản đã gộp, 0 ⇒ 1 ô gắn cờ, thẻ chờ ở máy demo, lời chủ dự án 17:16 22/11 ở quyết định 4 — `session_prompt/HIEN_TRANG.md` mục 4 gạch "17:19 22/11/2026 — GIAO DIỆN" (nguyên văn "…test thì dùng playwright… có ảnh chụp màn hình bằng chứng, thao tác toàn bộ các trang, các tính năng…"), người sửa đã mở; chuyển chi tiết lớp nhìn xuống "Chi tiết để tra" / "Đã so") [riêng tư; chép biên bản; người sửa đã mở `STATUS_C.md` dòng 44, `STATUS_E.md` dòng 19, `TRAN_NGANG_ANH.md` dòng 8, `song.css` 59–88, `Song.jsx` 48, 73].
- Gộp 10:00 23/11, commit gộp `e7193bd0` (nhánh `p13-c-man-dau-cao` `10c30bc5`); lùi: `git revert -m 1 e7193bd0` rồi dựng lại `frontend/dist` (cùng lùi đổi phía máy chủ `a76eb962`, vì đổi đó chỉ vào main qua lần gộp này — `git merge-base --is-ancestor a76eb962 e7193bd0^1` trả "không") [code; chép `session_prompt/HIEN_TRANG.md` mục 1 gạch "Giao diện mới…"]. Chỉ đổi lớp nhìn, không đổi chữ / luồng / xuất file: lời commit `4c1e6b7f`, `22e4694f`; `git diff --stat bedfa091 e7193bd0 -- frontend/src/lich_ics.js backend/api/routes/xuat.py backend/api/lich_pptx.py` rỗng [code, đã chạy lệnh].
- Đổi phía máy chủ: `git show a76eb962` — `backend/llm/assistant.py` `bai_da_tim` (docstring: bài đã tìm thấy, chưa chắc được trích; bỏ nguồn do code dựng; lý do 22–30 s, 17–20 s), `backend/api/routes/chat.py` `StreamEvents.status` (trường `bai`: `title`, `bai_id`) [code]. Thẻ chờ: `frontend/src/song/Song.jsx` `ChoSong` (trần 6 tên, nhãn "Đã tìm thấy {n} bài — bấm tên để đọc trong lúc chờ", `+k bài`, link `target="_blank"`), `frontend/src/chat.jsx` dòng 22–31 (`STATUS_TEXT`), 141–143 (`daTim`), 415–419 (`ChoSong` thay dòng cũ có "(n đoạn)" — bản cũ `git show bedfa091:frontend/src/chat.jsx` dòng 491); `song/song.css` dòng 71–88 (3 tên ở `.chat`, ≤ 760 px, ≤ 700 px cao) [code]. Chú thích đầu `ChoSong` ("server chưa gửi") đã cũ so với `a76eb962` — ghi ở báo cáo.
- Khối nguồn: `frontend/src/SourceLine.jsx` dòng 22–27 ("Nguồn đã dùng ({n} bài)", `data-lv`); màu chủ đề `frontend/src/song/nhin.js` `linhVuc`; `index.css` `@theme` `--color-lv-*` [code]. Câu an toàn: `song/song.css` dòng 38, `index.css` dòng 276 [code].
- Bộ biến + thang cỡ chữ: `frontend/src/index.css` `@theme` (dòng 5–58: màu, `--radius-*` 4 cỡ, `--shadow-*` 3 kiểu, `--ease-song`, `--text-*` chín bậc + `--text-h1` `clamp(40px, 4.6vw, 62px)`, chú thích "trước đó 39 cỡ khác nhau gõ tay", "trước đó 20 kiểu bo góc, 18 kiểu bóng"; dòng 60 chữ thân 16 px ở ≤ 760 px) [code]; lời commit `d9733aa9`, `85dc321c`, `36c23c94` [chép]. 68 mã màu / 16 biến trước 22/11: `data/giao_dien_2026-11-22/KIEM_KE.md` mục 2 [riêng tư; chép, đã mở]. Cỡ chữ in giữ cũ: `frontend/src/lkh.css` khối `@media print` (bài 30) [code].
- Hình sông: `frontend/src/song/Song.jsx` (`HeroSong`: `TAM_RONG`, `T_RONG`, `BO`, `NHAN` đặt tay; `tinh()` đo `getPointAtLength`, lùi nửa bề rộng sông theo pháp tuyến, đo lại khi `resize`; `RONG` 250 × chiều cao / 800; `MAN_DOC` = `(max-width: 1140px)`; nút "Dừng chuyển động" / "Chạy tiếp", chú thích "chuyển động tự chạy quá 5 giây ⇒ có nút dừng"; con đò `giay={44}`), `frontend/src/song/hinh.jsx` (`SONG_NGANG`, `SONG_DOC`, `Do`: "máy bật giảm chuyển động: không vẽ con đò"; chú thích "Hình tự vẽ giản lược, không lấy hình học bản đồ"), `frontend/src/LichV2.jsx` `SongNgay` [code].
- Bố cục theo khung nhìn: `frontend/src/song/song.css` dòng 109–112 (`--cao: clamp(520px, calc(100vh - var(--h1-tren, 69px)), 800px)`), 165–171 (bến chỉ còn tên: `(min-width: 1141px) and (max-height: 868px), (min-width: 1141px) and (max-width: 1360px)`, chú thích 1,8 : 1 ở 1536 × 695; 3,0 : 1 ở 1141 × 900), 172–175 (4 câu gợi ý ở ≤ 720 px cao), 179–207 (bố cục dọc) [code]; lời commit `da8bff00`, `ae870154` [chép]. Ba cách giữ dòng mô tả đã thử: `session_prompt/sessions/STATUS_C.md` mục 1 gạch "Bến chỉ còn TÊN" [chép].
- Giảm chuyển động: `frontend/src/hieuUng.js` (`giamChuyenDong`, `batHieuUng` chỉ thêm lớp `hieu-ung` khi không giảm), `frontend/src/index.css` khối `@media (prefers-reduced-motion: reduce)` (tắt mọi animation / transition), `song/song.css` (chuyển động chỉ dưới `.hieu-ung`), `lkh.css` (nét đứt chạy chỉ dưới `.hieu-ung`) [code].
- File nạp sau cùng, bộ chọn `html`, không `url("data:…")` vì CSP, hình nhỏ ở `frontend/public/hoa_tiet/`: `song/song.css` dòng 1–3, `frontend/src/main.jsx` (nạp `song/song.css` sau cùng; kiểu chữ `@fontsource`) [code].
- Tương phản: `data/giao_dien_2026-11-22/TUONG_PHAN.md` (19:56 22/11, nhánh `e98c42f`: 1.523 phép trên 24 màn, 0 dưới ngưỡng, 13 phép ô đang khoá; mục 3: sáu nhóm trượt lần đầu, một báo nhầm, ba có ở main; mục 1: chưa đo thẻ lịch, khung nổi, màn lỗi) [riêng tư; đã mở]; 1.850 phép trên `10c30bc5`: `session_prompt/sessions/STATUS_C.md` mục 2 [chép]; lời commit `e98c42f1` [chép].
- Cổng gộp: `data/giao_dien_2026-11-22/sau_gop_10c30bc5/MUC_LUC.md` (09:25 23/11, 49 cảnh, 0 không chụp được, tám cỡ) — người viết đếm 761 file `.png` [riêng tư; đã chạy `ls | wc -l`]; `…/TRAN_NGANG_*.md` (1 ô gắn cờ: A01 ở 390 px, có từ bản cũ — `TRAN_NGANG_ANH.md` dòng 8, `session_prompt/sessions/STATUS_E.md` dòng 19); `…/MAN_DAU_TINH_THEODOI_HOI_ANH_LICH_LOI_NGUON.md` (trọn / không trọn từng cỡ) [riêng tư; đã mở]; `…/kich_ban_du_sau_gop_10c30bc5/KET_QUA.md` (09:32 23/11: 50 bước, 49 "ĐẠT", 1 "xem ảnh" ở `CO`, .txt 29 dòng, PowerPoint 4 slide, PDF 2 trang) [riêng tư; đã mở, đã đếm]; `…/so_cap/NHOM_1…3` (so với `e98c42f`, trước bản gộp) + `NHOM_4` [riêng tư; mở `NHOM_3`]; ảnh đã mở: `sau_gop_10c30bc5/T01_trang_chu_1536x695_man.png`, `C01_cho_05s_1440_man.png`, `L02_lich_xong_1536x695_man.png`, `L02_lich_xong_390_man.png`, `L04_tro_ly_noi_1280x620_man.png`, `L04_tro_ly_noi_1536x695_man.png` [đã mở ảnh]. Cả bộ test: `data/test_rong_2026-11-22/KET_QUA_e8d02143.tsv` — người viết đếm: 86 dòng file, 82 thoát 0, 4 "bo", cộng cột `tong` = 2.218 passed, 0 failed [riêng tư; đã chạy `awk`]; `HIEN_TRANG.md` mục 1 gạch "Lượt cả bộ test MỚI NHẤT" [chép].
- Lỗi bắt trước gộp: lời commit `ae870154` (khổ giữa; 20 bề rộng), `e27398dc` (in: 22 %, 2 ⇒ 3 trang), `551d02fc` (`.answer` rò sang trang bài, 64 ký tự, bảng 5 cột), `da8bff00` (cao 800 px), `e98c42f1` (tương phản), `ec8fb7a0` (thẻ chờ điện thoại, 25–34 s), `10c30bc5` + `6b1e4fde` (Lên kế hoạch) [chép, đã mở]; bốn lỗi chặn: `session_prompt/VIEC_DANG_MO.md` khối A hàng X13 ("ba lỗi chặn đã chữa trước đó — màn đầu vỡ ở khổ giữa, bản in đổi tỉ lệ, trang một bài bị luật `.answer` rò sang"; "LỖI CHẶN CÒN LẠI… màn đầu Trang chủ không vừa MỘT khung nhìn máy xách tay") và `HIEN_TRANG.md` mục 4 gạch "20:44 22/11/2026" (hoãn gộp, hai bản phê bình khác hãng, phiên điều phối tự mở ảnh) [chép]. "Nhận bến chỉ còn tên": `VIEC_DANG_MO.md` khối A "QUYẾT ĐỊNH của phiên điều phối sáng 23/11 (a)" [chép]. Ô ngày `mm/dd/yyyy` do trình duyệt chụp chạy tiếng Anh: cùng hàng X13 ("[suy luận]") [chép].
- Giờ chạy so với ba bản sửa lõi: ảnh 09:25 (`MUC_LUC.md`), kịch bản 09:32 (`KET_QUA.md`), cả hai trên bản gộp thử nhánh chính `34b002d8` + `10c30bc5` — `session_prompt/sessions/STATUS_E.md` mục 1 gạch "CỔNG GỘP GIAO DIỆN MỚI" [chép]; `34b002d8` là nhánh chính lúc mở phiên, trước cả ba bản sửa (câu lưu ý gộp 09:10 `c2579fad`; "câu nhờ làm thay" và "gọi lại một lần" gộp 09:31 `97d4e85d`, `cb711bc4`) [đã chạy `git log`, phiên D]; lượt cả bộ test chạy trên cây gộp thử `e8d02143` có code bằng nhánh chính sau gộp: cùng gạch [chép].

- Đợt áp biên bản kiểm độc lập (12:45 23/11/2026; `data/hoc_cung_D/kiem/dot_2311_trua_k1_kiem.md` mục "Bài 35" hàng 2 [riêng tư]): ô "Ảnh chụp tự động" của "Đã so" — lượt chụp lại sau bản sửa thẻ chọn tên chỉ chạy nhóm hỏi bằng ảnh ở 390 px: `data/thu_bedrock_2026-11-21/harness/e_cham_quan_bua_2311/anh_390/` có đúng ba cảnh A00, A01, A02 (mỗi cảnh hai ảnh) + `TRAN_NGANG_ANH.md` [riêng tư; người áp liệt kê thư mục và mở `TRAN_NGANG_ANH.md`: "['390×844'] ·3 cảnh · 0 ô (cảnh × bề rộng) bị gắn cờ"].

- Lượt áp cuối (13:25 23/11/2026; biên bản `data/hoc_cung_D/kiem/dot_2311_trua_k2_sau_bien_ban_kiem.md` mục "Bài 35" hàng 3 + ghi kèm [riêng tư]): lời trích `TRAN_NGANG_ANH.md` chép nguyên; biểu tượng trang — `data/playwright_mcp/luot_2311_trua/F_mang.txt` (6 dòng `GET http://127.0.0.1:8013/static/favicon.svg => [200] OK`, 0 dòng mã 4xx / 5xx) và `NHAT_KY.md` bước F ("Console … 0 lỗi, 0 cảnh báo"), server 8013 = main `b4931a6b`; "dở": `session_prompt/VIEC_DANG_MO.md` gạch "[12:48 23/11/2026]" [riêng tư; đã chạy, phiên đo; người áp đã mở].

- Đợt V2 đầu chiều 23/11/2026 (đọc cây chính `64f188fa`). Dòng Cập nhật trước: "Cập nhật 13:25, ngày 23/11/2026 · khớp hệ thống 13:25 23/11 (49 tính năng mở, 5 tắt, kho 267 bài); đã áp hai lượt kiểm · thẻ chọn tên ảnh hết cắt chữ, trang có biểu tượng (nửa để tra) · số kiểm từ hồ sơ cổng gộp · người viết không chạy máy chủ · lần sửa trước: Nguồn.". Nhãn lượt 12:34–12:41: bản trước "sổ việc ghi lượt đó là dở, chưa ai chạy lại" (`session_prompt/VIEC_DANG_MO.md` gạch "[12:48 23/11/2026]"; ở `origin/main` `6089f8bd` vẫn ghi "DỞ"); nay "đã đi đủ các bước, do một agent con chạy, chưa có người thứ hai kiểm" — phiên điều phối chốt 13:5x 23/11 (lời giao V2 của phiên D) [chép]; `data/playwright_mcp/luot_2311_trua/NHAT_KY.md` mục "ĐÃ LÀM / CHƯA LÀM": A–F "ĐÃ LÀM" [riêng tư; đã mở]. Thẻ "Hôm nay ở Huế": danh sách bài lấy một lần ở `frontend/src/App.jsx` dòng 43 (`getJson("/api/kham_pha")`), truyền vào `TrangChu.jsx` (`baiHomNay(bai)`); `frontend/src/homNay.js` (`soNgayVN` = `Math.floor((luc + LECH_VN_MS) / MOT_NGAY_MS)`, `luc = Date.now()` của trình duyệt; chú thích "File riêng (không nằm trong TrangChu.jsx) để phép chọn chạy được bằng Node khi kiểm"; `return null` khi tập rỗng) [code]; câu "máy đặt múi giờ nào cũng ra ngày Việt Nam; chỉ máy chạy sai đồng hồ…" (`Date.now()` là mili giây theo giờ quốc tế, không theo múi giờ của máy) và "trang để mở qua nửa đêm giữ bài cũ" (`TrangChu.jsx` dòng 60 `useMemo(…, [bai])`; `App.jsx` dòng 41–44 lấy danh sách một lần, dòng 146 chỉ vẽ Trang chủ khi đang ở trang đó) [suy từ code, chưa thử; áp biên bản `data/hoc_cung_D/kiem/dot_2311_chieu_k2_kiem.md` bài 35 hàng 4, 14:33 23/11].

</details>
