# Bài 38 — Bộ test: chương trình tự kiểm những gì

*Cập nhật 15:43, ngày 22/11/2026 · số file, số ca và thời gian chạy lấy từ lần chạy đủ cuối buổi sáng (10:58–11:14 22/11; lần mới nhất 14:48–15:03 ghi ở Ý chính và Chi tiết để tra, phiên đo chạy, người viết không chạy lại); các loại test đọc từ tên và chú thích đầu file trong thư mục test của máy chủ; những lần test không bắt được lỗi lấy từ các báo cáo 01/11, 20/11, 21/11; bài đã qua một lượt đối chiếu độc lập và sửa theo đó.*

**Bài trước đã biết:** các bộ câu và người chấm đo chất lượng câu trả lời (bài 17–20); thước "làm trợ lý" và người dùng mô phỏng (bài 32); hai rào của git trước khi lưu code (bài 37).
**Bài này thêm:** test tự động là gì; bộ test của máy chủ gồm những loại nào, kiểm gì và không kiểm gì; nó khác các phép đo chất lượng ở đâu; những lỗi thật nó đã không bắt được; và vì sao chạy cả bộ mất khoảng mười lăm phút, từng file một.

## Ý chính

- **Test tự động là một đoạn chương trình kiểm một đoạn chương trình khác**: đưa vào một đầu vào đã biết, so đầu ra với điều phải đúng. Máy chạy được hàng nghìn ca trong vài phút, không cần người ngồi bấm.
- **Lần chạy đủ mới nhất, 14:48–15:03 22/11, trên bản đã mở bộ thay đổi cho tin dài (45 tính năng mở): 78 file, 2.119 ca đạt, 2 ca hỏng** — đều là ca test cũ so nguyên một bảng nay có thêm tên nhà cung cấp model của trang Giới thiệu, không phải sản phẩm sai. Trước đó, lượt kiểm chốt trưa 22/11: 76 file, 2.060 ca. Các số chi tiết trong bài là của lần chạy cuối buổi sáng: 75 file, 1.961 ca đạt, 0 file hỏng, 4 file bỏ cả file vì cần khoá OpenAI, mà tài khoản đó đang gác; trong số đó có file kiểm đường chat chính, nên các ca không cần model của file đó cũng không chạy.
- Bộ test kiểm **chương trình làm đúng việc của nó** (cắt đoạn, tìm, kiểm số nguồn, xếp lịch, đường gọi, giao diện). Nó **không** kiểm model viết hay hay dở: các ca có model đều dùng một model giả trả lời theo kịch bản. Chất lượng câu trả lời đo ở chỗ khác, bằng model thật (bài 17–20, 32).
- Đã có lỗi thật mà bộ test không bắt: lỗi "xin công cụ mãi" của lớp nối Claude (bài 33) chỉ lộ khi gọi model thật.
- Cả bộ chạy khoảng 16 phút, **từng file một**, không song song: máy phát triển ít bộ nhớ: chạy cả bộ trong một lượt đã tốn khoảng 4,4 GB.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| test tự động | **automated test** | đoạn chương trình kiểm một đoạn chương trình khác, chạy bằng một lệnh |
| ca test | **test case** | một lần kiểm: một đầu vào, một điều phải đúng; đạt hoặc hỏng |
| file test | **test file** | một file gom các ca test của cùng một phần |
| bộ chạy test | **pytest** | chương trình chạy mọi ca trong các file test và báo bao nhiêu ca đạt, bao nhiêu hỏng |
| hàm thuần | **pure function** | phần chương trình chỉ nhận đầu vào và trả đầu ra, không gọi mạng, không đọc ghi gì bên ngoài; dễ test nhất |
| model giả | **fake model**, **stub** | một đoạn chương trình đóng vai model, trả lời theo kịch bản viết sẵn, không gọi hãng nào |
| đỏ, xanh | **failing**, **passing** | ca hỏng, ca đạt |
| tiến trình | **process** | một chương trình đang chạy trên máy (bài 36); mỗi file test chạy trong một tiến trình riêng |

## Một ca test đưa đầu vào đã biết và so với điều phải đúng

Ví dụ bằng lời: bước kiểm số nguồn (bài 16) phải rút một câu trả lời có số [7] khi chỉ có 5 nguồn. Một ca test tự dựng câu trả lời đó, gọi bước kiểm, và đòi kết quả là "rút". Nếu một ngày ai đó sửa bước kiểm làm nó cho qua, ca này đỏ ngay lần chạy sau, trước khi người dùng gặp.

Hai thói quen của nhóm gắn với cách viết test:

- **Mỗi bản sửa lỗi kèm một ca mới đã thấy đỏ trên code cũ**, rồi xanh sau khi sửa. Ca chưa từng đỏ thì không chứng minh được nó bắt lỗi. Một file test ghi thẳng: "một phép kiểm không bao giờ đỏ thì không kiểm gì".
- **Có ca khoá những thứ không được lọt.** Ví dụ: mỗi dòng sổ số đo phải có đúng các ô trong danh sách của chương trình, không thừa ô nào, và một ca kiểm chữ câu hỏi không lọt vào sổ (bài 37). Thêm một ô vào chính danh sách đó thì test vẫn đạt; và file chứa hai ca này bị bỏ ở lần chạy đủ gần nhất. Hay: khi một tính năng tắt, chuỗi gửi model phải giống từng byte bản trước.

## Bộ test của máy chủ có bốn loại

| Loại | Kiểm gì | Ví dụ |
|---|---|---|
| hàm thuần | một bước tính, không mạng | cắt đoạn; chấm từ khoá; chuẩn hoá số nguồn; đọc ngày âm lịch; bộ xếp lịch; bộ đọc lệnh "đổi chỗ ngày 1 với ngày 2"; con số trong câu trả lời phải có trong nguồn |
| phần thật, chỉ đọc | bước tìm trên chỉ mục thật trong Qdrant, model embedding thật trên máy | tìm ra đúng đoạn; trộn hai cách tìm; các bài trong kho đúng là các bài đã chia đoạn và cất vào Qdrant |
| đường gọi với model giả | bật cả máy chủ ngay bên trong chương trình test (không trình duyệt, không cần cổng mạng), gửi yêu cầu thật vào đường gọi, model thay bằng kịch bản | chuỗi tin trên đường gửi dần đúng thứ tự; lỗi model thành đúng lời báo; dòng sổ số đo có đúng các ô; cookie; giới hạn lượt; trang theo dõi; lớp nối Claude với phản hồi dựng sẵn |
| giao diện bằng node | chạy chương trình của giao diện bằng node (bộ chạy JavaScript ngoài trình duyệt) trên dữ liệu thật | khi nào có ảnh dưới câu trả lời; khi nào hiện thẻ khách sạn; dòng mở đầu mục web. Một số ca khác chỉ đọc chữ của file giao diện, ví dụ danh sách thẻ cho phép của bộ lọc không có thẻ ảnh |

**Trình duyệt tự động không nằm trong bộ test.** Khi cần thấy đúng thứ người dùng thấy (bấm nút, màn hình hẹp, file tải về), phiên đo lái một trình duyệt thật bằng chương trình, trên máy chủ thật, model thật, mỗi lần một lượt, và đọc ảnh chụp màn hình. Bài 6 dùng cách đó cho bốn ca hỏng ngày 22/11.

Ngoài bốn loại trên, có một nhóm test cần khoá OpenAI thật: chúng kiểm máy có khoá, hoặc gọi gpt-6-luna thật. Bốn file đó bị bỏ ở lần chạy gần nhất (mục "Chi tiết để tra").

## Test kiểm chương trình; phép đo kiểm câu trả lời

Hai việc này dễ lẫn.

- **Bộ test** trả lời: chương trình có làm đúng điều nó được viết để làm không? Nó chạy không tốn tiền, cho kết quả giống nhau mỗi lần, và chạy (các file bị chạm) trước khi gộp code; cả bộ chạy ở mốc.
- **Phép đo** (bộ câu mẫu, người chấm, thước làm trợ lý, người dùng mô phỏng; bài 17–20, 32) trả lời: với model thật, người dùng có nhận câu trả lời đúng, đủ, có nguồn không? Nó tốn tiền, kết quả dao động giữa hai lần chạy (nên phải đo mức nhiễu), và chạy khi một thay đổi chạm câu trả lời.

Một file test của bước chạy song song ghi rõ ranh giới này: model được thay bằng kịch bản có độ trễ cho trước, "không phải bằng chứng hành vi model, chỉ kiểm thứ tự / giữ / bỏ / gộp của code". Bộ test xanh không nói được câu trả lời tốt; một lượt đo tốt không nói được mọi nhánh của chương trình còn đúng.

## Quyết định và lý do

### 1. Vì sao ca có model dùng model giả, không gọi model thật?

- **Đã chọn:** mọi ca có model trong bộ test dùng model giả trả lời theo kịch bản; chỉ nhóm test cần khoá mới gọi model thật.
- **Vì sao:** chú thích trong các file test: kiểm thứ tự, giữ, bỏ, gộp của chương trình, không kiểm hành vi model. Điều thấy được: kết quả giống nhau mỗi lần, không tốn tiền, chạy được khi không có mạng.
- **Cách khác:** gọi model thật trong test: chỉ còn ở bốn file cần khoá; các phép đo bằng model thật là việc riêng (bài 17–20).
- **Cái giá:** model giả chỉ trả lời đúng cái người viết kịch bản nghĩ ra. Lớp nối Claude có khoảng 20 ca test với phản hồi dựng sẵn, đều xanh, mà lỗi "xin công cụ mãi" vẫn chỉ lộ khi gọi Claude thật (bài 33).

### 2. Vì sao một số test dùng Qdrant và model embedding thật, không giả cả hai?

- **Đã chọn:** các ca của bước tìm chạy trên chỉ mục thật trong Qdrant (chỉ đọc) và model embedding thật trên máy.
- **Vì sao:** chú thích đầu bộ test ghi các phần dùng chung chạy trên hệ thống thật (Qdrant chỉ đọc, model embedding trên máy) và không phần nào tạo hay ghi dữ liệu trong Qdrant. Một file test cách bật máy chủ khi thiếu model embedding ghi: "Đầu vào thật, không mock". Luật cứng của dự án: bằng chứng từ hệ thống thật.
- **Cách khác:** giả Qdrant bằng một bảng nhỏ trong bộ nhớ: chưa thử.
- **Cái giá:** muốn chạy cả bộ phải bật Qdrant và có chỉ mục đúng; sửa kho mà chưa cập nhật chỉ mục thì các ca này đỏ. Cũng vì vậy bộ test tốn bộ nhớ (quyết định 4).

### 3. Vì sao chỉ chạy cả bộ test ở mốc, còn lúc sửa chỉ chạy file bị chạm?

- **Đã chọn:** khi sửa, chạy các file test chạm phần đã sửa; cả bộ chạy một lần trước khi gộp một nhánh lớn hoặc ở một mốc.
- **Vì sao:** chủ dự án chọn ngày 20/11 (theo sổ ghi): "test vừa đủ, cả bộ test chỉ ở mốc", sau nhiều lần nhắc nhóm test quá nhiều.
- **Cách khác:** chạy cả bộ sau mỗi lần sửa: là cách trước đó.
- **Cái giá:** một bản sửa có thể làm hỏng một file khác mà tới mốc mới thấy.

### 4. Vì sao chạy từng file một, không chạy song song?

- **Đã chọn:** cả bộ chạy từng file, lần lượt, không nạp file khoá, không chạy cùng lúc với máy chủ.
- **Vì sao:** máy phát triển dùng chung, khoảng 15 GB bộ nhớ. Ghi trong hướng dẫn vận hành: chạy rộng tốn khoảng 4,4 GB; ngày 21/11 một phiên bật 13 tiến trình cùng lúc làm cạn bộ nhớ. Không nạp file khoá vì nạp là có khoá OpenAI, và test cần khoá sẽ gọi model cũ, trái lệnh tạm gác của chủ dự án.
- **Cách khác:** chạy nhiều file song song cho nhanh: đã gặp sự cố, không làm.
- **Cái giá:** cả bộ mất khoảng 16 phút; bốn file cần khoá không chạy được cho tới khi có lại tài khoản OpenAI.

## Nếu… thì sao

Một tình huống kể trọn. Ngày 01/11, giao diện chữ hiện dần có bộ lọc chữ và chính sách chặn tải, cả hai có test. Người kiểm thử bằng trình duyệt 16 kiểu thẻ có thể tải đồ từ máy khác, trên cả hai đường vào trang. Đường chính chặn hết; nhưng cùng trang mở qua một đường thứ hai không có chính sách chặn, và bộ lọc lúc đó thiếu hai thứ ít ai để ý: 3 trên 16 ca lọt. Test không bắt vì không ai viết ca cho đường thứ hai. Sửa: đổi bộ lọc sang danh sách cho phép, gắn chính sách cho mọi trang, và thêm ca test cho cả hai (bài 35).

| Đã gặp | Vì sao test không bắt | Bắt bằng gì |
|---|---|---|
| Claude xin công cụ mãi, 0 trên 8 lần viết được (21/11) | phản hồi dựng sẵn không cư xử như Claude thật | phát lại yêu cầu thật tới Bedrock (bài 33) |
| câu hỏi cũ dính vào câu đang hỏi trên đường Claude (21/11) | chưa có ca hai câu hỏi liền nhau | bộ chuỗi nhớ tên chạy với model thật |
| bản in từ khung trò chuyện ra 5 trang giống nhau (20/11) | in là việc của trình duyệt | AI khác hãng nêu, nhóm mở file in thật |
| 3 trên 16 ca lọt chính sách chặn tải (01/11) | thiếu ca cho đường vào thứ hai | người kiểm bằng trình duyệt |
| chạy riêng một ca của file đường chat thì đỏ, chạy cả file thì xanh | ca phụ thuộc thứ tự chạy | ghi giới hạn: chạy cả file |

## Dễ nhầm

- **"Bộ test xanh là câu trả lời đúng."** Không. Bộ test dùng model giả; chất lượng câu trả lời đo bằng model thật ở bài 17–20.
- **"1.961 ca là 1.961 câu hỏi."** Không. Đó là số lần kiểm chương trình; phần lớn không có câu hỏi nào, chỉ là đầu vào dựng tay cho một hàm.
- **"Test bỏ qua là test hỏng."** Không. Bốn file bỏ vì cần khoá OpenAI; trong lúc tạm gác model cũ, các ca của chúng không chạy, kể cả những ca không gọi model nằm chung một file. Bỏ không phải hỏng, nhưng cũng không phải đã kiểm.

## Câu hỏi tự kiểm

<details>
<summary>1. Bộ test và phép đo chất lượng khác nhau thế nào?</summary>

Bộ test kiểm chương trình làm đúng việc của nó, bằng model giả, không tốn tiền, kết quả giống nhau mỗi lần. Phép đo kiểm câu trả lời của model thật, tốn tiền, có nhiễu.

</details>

<details>
<summary>2. Vì sao lớp nối Claude có khoảng 20 ca test xanh mà vẫn có lỗi lớn?</summary>

Các ca dùng phản hồi dựng sẵn. Lỗi nằm ở cách Claude thật cư xử khi nhận cùng lúc công cụ và khuôn đầu ra; chỉ gọi thật mới thấy.

</details>

<details>
<summary>3. Vì sao không chạy các file test song song cho nhanh?</summary>

Máy ít bộ nhớ, một lượt chạy rộng tốn khoảng 4,4 GB, và đã có lần bật nhiều tiến trình làm cạn bộ nhớ. Chạy từng file mất khoảng 16 phút.

</details>

<details>
<summary>4. Một bản sửa lỗi tốt kèm ca test như thế nào?</summary>

Một ca mới đã thấy đỏ trên code cũ, rồi xanh sau khi sửa. Ca chưa từng đỏ thì không chứng minh được nó bắt lỗi.

</details>

## Cấu hình đang chạy

| Mục | Giá trị | Dùng để làm gì, vì sao | Đã thử giá trị khác chưa |
|---|---|---|---|
| Lệnh chạy một file | bộ chạy test, từ thư mục máy chủ, ở chế độ không tải model từ mạng | chỉ dùng model embedding đã có trên máy | — |
| Cả bộ | từng file một, không nạp file khoá, không cùng lúc với máy chủ | quyết định 4 | chạy cùng lúc nhiều tiến trình: cạn bộ nhớ (21/11) |
| File test của giao diện | cần bản dựng giao diện có sẵn | các ca chạy chương trình thật của trang | — |
| Đổi một tính năng trong cấu hình | chạy file test chạm tính năng đó cả có và không nạp file khoá | bắt ca phụ thuộc khoá | — |

## Quyết định nhỏ hơn

**Vì sao bỏ cả file khi file đó cần khoá model cũ, thay vì tách riêng ca cần khoá?** Chưa thấy ghi lý do. Điều thấy được: bộ chạy cả bộ có một danh sách bốn file bỏ, ghi "cần khoá OpenAI (model cũ tạm gác)". Cái giá: các ca không cần khoá trong cùng file (vòng đời máy chủ, khuôn đường chat, sổ số đo không lọt câu hỏi) không chạy trong lúc gác gpt-6-luna.

## Chi tiết để tra

- Lần chạy đủ mới nhất: 14:48–15:03 22/11, trên bản đã mở bộ thay đổi cho tin dài (45 tính năng mở, trần tìm 3): 78 file, 2.119 ca đạt, 4 file bỏ (cần khoá OpenAI), 2 file mỗi file 1 ca hỏng — hai ca test cũ so nguyên bảng tính năng của trang Giới thiệu, lệch đúng một khoá mới (tên nhà cung cấp model) khi người chạy có đặt biến file khoá Bedrock; bỏ biến thì xanh; phiên đo đang sửa hai ca test, không đụng code sản phẩm. Trước đó: lượt kiểm chốt trưa 22/11 (13:19–13:34), 76 file, 2.060 ca. Các con số 75 file và 1.961 ca trong bài là của lần chạy cuối buổi sáng.
- Lần chạy cuối buổi sáng: 10:58–11:14 22/11, trên cây chính (bản main cuối buổi sáng cho phần máy chủ), 42 tính năng mở, kho 266 bài, 9.458 đoạn, không nạp file khoá: 75 file, 1.961 ca đạt, 0 file hỏng, 4 file bỏ. Bốn file bỏ: đường chat có khoá, bộ sinh câu trả lời OpenAI, lượt thử trực tiếp, kiểm cấu hình có khoá.
- Tiến qua các lần chạy: 68 file, 1.827 ca, 1 đỏ (tối 21/11) ⇒ 72 file, 1.900 ca (09:23–09:38 22/11) ⇒ 73 / 1.941 ⇒ 74 / 1.951 ⇒ 75 / 1.961, 0 đỏ.
- Lúc viết bài, thư mục test có 76 file (một file thêm sau lần chạy đủ gần nhất); trong thư mục có 938 hàm test, nhiều hàm chạy thành nhiều ca với các đầu vào khác nhau.
- Một file test cách bật máy chủ khi thiếu model embedding phải chạy riêng, vì nó đặt một thư mục model rỗng cho tiến trình con.
- Đổi model viết sang Claude: các test thôi khoá giá trị của dòng chọn hãng, để đổi một dòng không làm đỏ test; các ca cần khoá OpenAI đỏ khi không nạp khoá là đúng thiết kế, nên lần chạy đủ bỏ hẳn bốn file đó (bài 33).
- Ngoài bộ test của máy chủ: phép kiểm "cập nhật riêng chỉ mục giống dựng lại toàn bộ" chạy trên collection thật (bài 12); kịch bản demo 10 bước chạy lặp qua đường gọi thật với model thật (bài 32).
- Rào trước khi lưu code (bài 37) không chạy bộ test; nó chỉ kiểm thứ được lưu.

**Bài sau (bài 39):** đồ án được làm thế nào: một người quyết định và nhiều coding agent.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Bốn file bỏ cả file: `data/test_rong_2026-11-22/chay_tren_cay.sh` dòng 7, 15 ("cần khoá OpenAI (model cũ tạm gác)") [riêng tư]; ca sổ số đo trong `backend/tests/test_api_chat.py` dòng 102–109 [code].
- Bài đã qua một lượt đối chiếu độc lập 22/11: `data/hoc_cung_D/kiem/bai_33_38.md` [riêng tư]; dòng không áp ở `data/hoc_cung_D/viet/viet_33_38.md` mục "Sau lượt kiểm".
- Lần chạy đủ gần nhất, 75 file / 1.961 / 4 bỏ, tiến qua các lần chạy: `session_prompt/HIEN_TRANG.md` mục 1 (gạch "Cả bộ test") [đã chạy, phiên đo; người viết không chạy lại]. Lời giao ghi "72 file, 1.900 ca" — đó là lần 09:23–09:38; HIEN_TRANG có lần mới hơn, bài dùng lần mới.
- 76 file, 938 hàm: `ls backend/tests/test_*.py | wc -l`, `grep -h "def test_" backend/tests/*.py | wc -l` [đã chạy, 13:14 22/11].
- Bốn loại: chú thích đầu file — hàm thuần `test_citations.py`, `test_r4_numbers.py`, `test_doi_cho_ngay.py`…; phần thật chỉ đọc `backend/tests/conftest.py` ("Fixtures dùng runtime thật… không có fixture nào tạo hay ghi collection"), `test_full_corpus_retrieval.py`; đường gọi `test_api_chat.py` ("Real FastAPI lifecycle"), `test_chat_stream.py`, `test_chot_deploy.py`, `test_theo_doi.py`, `test_bedrock_model.py`; model giả tên "probe" `test_cau_nhieu_y.py`, `backend/api/theo_doi.py` (`MODEL_GIA`); node `test_anh_tra_loi.py` ("chạy bằng node thật"), `test_the_khach_san.py`, `test_mo_dau_web.py`, `test_tim_bai.py`; bộ lọc không thẻ ảnh `test_static_ui.py::test_answer_sanitizer_is_an_allowlist_without_fetching_tags` (đọc chữ của `markdown.js`, không chạy node) [code].
- "không phải bằng chứng hành vi model": `test_toc_do_song_song.py` dòng 1–3 [code]. "một phép kiểm không bao giờ đỏ thì không kiểm gì": `test_kiem_cap_nhat_rieng.py` dòng 1 [code]. "Đầu vào thật, không mock": `test_startup_model_missing.py` [code]. Ô sổ số đo khoá: `test_api_chat.py` dòng 104 [code].
- Ca mới phải đỏ trên code cũ: `bai_hoc/VIEC_MOI_XONG.md` mục 17, 23 [chép].
- Trình duyệt tự động ngoài bộ test: `report_agent/2026-11-21/b_bedrock_sonnet.md` mục 3b ("trình duyệt tự động"); bài 6 (bốn ca hỏng 22/11) [chép]. Kịch bản demo chạy qua route thật trong tiến trình: `data/thu_bedrock_2026-11-21/do/demo/chay_demo.py` dòng 1–5 [riêng tư].
- Quyết định 3: `session_prompt/HIEN_TRANG.md` mục 4 (gạch 15:56 20/11, điều (1)) [chép]; `guides/RUNBOOK_BAN_GIAO.md` mục 3.
- Quyết định 4: 4,4 GB `guides/RUNBOOK_BAN_GIAO.md` mục 3; 13 tiến trình 11:44 21/11, không nạp env, từng file: `HIEN_TRANG.md` mục 1 (gạch "Bẫy RAM", "Cả bộ test"); 15 GB: hồ sơ máy của chủ dự án [chép].
- Bảng "đã gặp": xin công cụ mãi, dính lịch sử `bai_hoc/VIEC_MOI_XONG.md` mục 23; bản in 5 trang `VIEC_MOI_XONG.md` mục 17 ý 3; CSP 3/16 `bai_hoc/21_DU_LIEU_NGUOI_DUNG_VA_BAO_MAT.md` (trỏ `report_agent/2026-10-31_streaming_spec/s3_giao_dien_review.md`); ca phụ thuộc thứ tự `guides/RUNBOOK_BAN_GIAO.md` mục 10.3 [chép].
- Test thôi khoá dòng chọn hãng: `report_agent/2026-11-21/b_bedrock_sonnet.md` mục 1 [chép].

- Kết quả lượt kiểm chốt buổi trưa 22/11 (phiên điều phối báo, phiên đo chạy; người viết chép từ tin, chưa tự mở file kết quả) [đã chạy].

- Đã qua một lượt kiểm chéo sau lượt cập nhật 14:47 (`data/hoc_cung_D/kiem/cap_nhat_14h47.md`) [riêng tư]. Lần chạy đủ mới nhất 14:48–15:03 22/11 (78 file, 2.119 ca đạt, 4 file bỏ, 2 ca hỏng do ca test cũ): `session_prompt/HIEN_TRANG.md` mục 1 gạch "Cả bộ test — lần đủ MỚI NHẤT"; `bai_hoc/VIEC_MOI_XONG.md` mục 42 dòng trạng thái (ghi cả lượt kiểm 14:48–15:05, gồm lần gõ qua trình duyệt) [đã chạy, phiên đo; người viết không chạy lại].

</details>
