# Bài 32 — Đo một trợ lý: hội thoại nhiều lượt, người dùng mô phỏng, kịch bản chạy lặp

*Cập nhật 14:48, ngày 22/11/2026 · đã sửa theo một lượt đối chiếu độc lập · các thước, cách chấm và số chép từ hồ sơ đo các ngày 14–22/11 (phần lớn ngày 21/11, hai model: gpt-6-luna và Claude Sonnet 5.5 mức suy luận cao); số đếm loại câu của bộ 41 câu đếm lại bằng máy, không đọc câu; người viết không chạy lại phép đo nào.*

**Bài trước đã biết:** bộ 176 câu mẫu đo bước tìm và câu trả lời, mỗi câu một lượt (bài 17–19); một thí nghiệm đổi một thứ, đo theo cặp, so với nhiễu (bài 20); trợ lý tự tìm thêm, gọi công cụ, nhớ cuộc trò chuyện, sửa lịch (bài 21–31).
**Bài này thêm:** những thứ trợ lý làm qua nhiều lượt thì bộ 176 câu không thấy. Bài giảng năm thước của phần trợ lý (chuỗi hội thoại, người dùng mô phỏng, bộ câu khó, kịch bản demo, bộ dò mù), ai chấm từng thước, mức nhiễu của thước nhỏ, luật "ít nhất ba lượt mỗi bên", và các số chính hiện có.

## Ý chính

- Bộ 176 câu hỏi **mỗi câu một lượt**, nên không thấy chuyện xảy ra khi người dùng hỏi tiếp, hỏi cụt, hỏi ba ý một lúc, hay nhờ sửa lịch rồi hỏi thêm. Phần trợ lý cần thước nhiều lượt.
- **Người dùng mô phỏng**: một model thứ ba (Claude Opus 5.5) đóng 12 vai du khách, mỗi vai nói chuyện với hệ thống tối đa 5 lượt qua đường chat thật. Thước này tìm ra các lỗi mà mọi thước cũ đều sạch, ví dụ phần hỏi trong một tin "vừa sửa lịch vừa hỏi" bị bỏ im 4 trên 4 lần.
- Người chấm **đọc mù**: một agent con ngữ cảnh mới đọc bản ghi đã giấu tên model (gọi là hệ X, hệ Y). Bộ 41 câu khó và kịch bản demo thì chấm bằng luật máy.
- Thước nhỏ **nhiễu lớn**: cùng một hệ thống chạy hai lần, bộ 41 câu lệch tới 3 mục, 12 vai lệch 1 phiên. Vì vậy luật của nhóm: thước nhỏ cần ít nhất ba lượt mỗi bên, và chỉ gọi là "tốt hơn" khi mọi cặp lượt cùng chiều và chênh lớn hơn nhiễu.
- Số chính (21/11): 12 vai, phiên đạt 7 · 7 · 8 trên 12 với Claude Sonnet 5.5, so với 6 · 5 · 6 với gpt-6-luna; bộ 41 câu khó, lượt mới nhất 39 trên 41 đạt máy; kịch bản demo 0 trên 10 lần hỏng ở cả hai model.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| thước | **benchmark**, **eval** | một bộ câu hoặc kịch bản cố định, cùng cách chấm, dùng để so hai bản của hệ thống |
| chuỗi hội thoại | **multi-turn chain** | một kịch bản nhiều tin liền nhau, mỗi tin có nhãn điều đúng phải xảy ra |
| người dùng mô phỏng | **simulated user** | một model được dặn đóng vai một du khách và tự nghĩ tin tiếp theo theo câu trả lời nhận được |
| vai | **persona** | mô tả một kiểu khách: ai đi, muốn gì, hay nói thế nào |
| đọc mù | **blind grading** | người chấm không biết bản ghi nào của hệ thống nào |
| bộ dò mù | **blind probe set** | bộ câu thử cho một tính năng, do một phiên **khác** người làm soạn theo lời tả, chưa đọc chương trình |
| đạt máy | **automatic pass** | đạt theo luật máy kiểm (không lỗi, không chạm trần, có đủ chữ phải có); thô hơn đọc tay |
| phép thử khói | **smoke test** | một lượt chạy ngắn ngay sau khi gộp thay đổi, chỉ để thấy chỗ vỡ rõ ràng |

## Bộ 176 câu đo một lượt; trợ lý hỏng ở chỗ nhiều lượt

Bộ 176 câu (bài 17) gửi mỗi câu như tin đầu của một cuộc mới. Nó đo tốt việc tìm đúng đoạn và viết đúng nguồn. Nhưng ba nhóm việc của phần trợ lý không có trong nó:

- **nhớ cuộc trò chuyện**: "còn chỗ đó thì sao?", "quán thứ hai bạn vừa kể ở đường nào?";
- **công cụ và vòng tìm thêm**: câu cần thời tiết, khoảng cách, ngày âm, nhiều lần tìm;
- **lịch**: lập lịch, sửa bằng lời, hỏi tiếp về lịch.

Chiều ngược lại cũng đúng: độ đúng sự thật của từng câu vẫn do bộ 176 câu và bước kiểm số nguồn giữ, vì người chấm các thước nhiều lượt không có kho trong tay.

## Năm thước của phần trợ lý

| Thước | Đo gì | Cỡ | Ai chấm | Dùng khi nào |
|---|---|---|---|---|
| **Chuỗi hội thoại** | hỏi tiếp đúng ngữ cảnh: nhớ tên, hỏi tiếp ý cũ, ý mới, ngoài kho, có điều kiện, đổi chủ đề | 25 chuỗi, 56 lượt (20 chuỗi 2 lượt, 4 chuỗi 3 lượt, 1 chuỗi 4 lượt) | máy đếm (tuyến đúng, trả lời / từ chối đúng nhãn, câu tìm có tên nơi của lượt trước); người đo đọc tay lượt lệch | mỗi khi đổi phần nhớ hội thoại hay lời dặn |
| **12 vai người dùng mô phỏng** | một du khách thật sự có đạt được việc mình muốn không | 12 vai × tối đa 5 lượt; 38 ý cần đạt | agent con đọc mù | mốc trước / sau một đợt sửa lớn, hoặc đổi model |
| **41 câu khó** | các ca khó rút từ 24 phiên mô phỏng, phát lại cả lịch sử | 41 mục, 17 loại | luật máy | so theo cặp một bản sửa nhỏ, hay hai model |
| **Kịch bản demo** | 10 việc một người demo sẽ làm, câu cố định: 6 ở ô hỏi đáp, 4 ở trang Lên kế hoạch | 10 bước | luật máy, đọc tay vài bước | phép thử khói sau mỗi lần gộp |
| **Bộ dò mù** | một tính năng nhận đúng câu cần nhận, không nhận nhầm câu giống mà không phải | thường 20 câu phải nhận + 20 câu đối chứng | máy đếm, người khác người làm soạn | trước khi mở một tính năng dựa vào khuôn chữ |

Ngoài năm thước này còn một **thước 29 câu** cho công cụ (15 câu dùng công cụ, 6 câu ở rìa phạm vi Huế, 8 câu ghép nhiều công cụ), kèm hai bộ sàn: 10 câu an toàn, 10 câu ngoài phạm vi.

## Người dùng mô phỏng: một model đóng vai, một model khác đọc mù

**Cách chạy.** Mỗi vai có một đoạn tả và một tin mở đầu cố định. Người mô phỏng nhận câu trả lời của hệ thống, tự viết tin tiếp theo, tối đa 5 lượt; xong việc thì tự dừng. Nó không có kho, không có bộ câu mẫu, không có nhãn. Hệ thống được gọi qua đúng đường chat của người dùng thật, trong cùng tiến trình máy chủ. Mười hai vai, ví dụ: gia đình có bé và bà đau gối; hai sinh viên ít tiền; khách chỉ có một buổi chiều; người mê ăn; người thích lịch sử cố đưa một điều sai; khách mùa mưa; người lên lịch bằng biểu mẫu rồi sửa trong ô chat; người hỏi cụt, hay đổi ý; người nhờ việc ngoài phạm vi; người dân địa phương; người đi lễ.

**Cách chấm.** Mỗi vai có 3–4 ý cần đạt, cả bộ 38 ý. Phiên "đạt" khi người chấm thấy vai đạt được việc mình muốn. Lượt đầu (trưa 21/11), phiên làm việc đọc tay, không mù. Lượt mốc (tối 21/11) đổi sang đọc mù: mỗi lượt một agent con ngữ cảnh mới đọc bản ghi đã đổi tên thành hệ X, hệ Y theo luật chấm ghi trước; lượt thứ nhất của mốc có hai người đọc độc lập, khớp nhau ở mọi vai.

**Thước này tìm ra gì.** Ở lượt đầu, các lỗi mà bộ thước cũ không thấy:

- chạm trần số vòng của trợ lý ⇒ câu từ chối trống (gpt-6-luna, 6 lượt);
- câu trả lời bị rút lại 7 lượt (gpt-6-luna 3, Claude 4); phát lại được 6 lượt thì 5 lượt là vì người dùng nhắc lại một con số dự báo trong câu hỏi;
- Claude từ chối khi người dùng dẫn "con số bạn vừa đưa" (3 lượt);
- tin vừa sửa lịch vừa hỏi: phần hỏi bị bỏ im (4 trên 4) — sau đó thành tính năng "phần câu hỏi chưa trả lời" (bài 31);
- "thêm X" vào lịch ⇒ chương trình tự thế chỗ ⇒ người dùng xin trả lại, lặp ba lượt — sau đó thành tính năng "thêm không tự thế chỗ" (bài 31);
- lớp dịch sang Claude gộp các câu hỏi cũ liền nhau thành một tin.

## Mức nhiễu: vì sao thước nhỏ cần ít nhất ba lượt mỗi bên

Model không trả lời giống hệt nhau hai lần (bài 20). Với bộ 176 câu, phép so theo cặp và khoảng tin cậy lo việc này. Với thước nhỏ, nhóm đo nhiễu trực tiếp: chạy **cùng một bản** hai hay ba lần rồi xem các lần lệch nhau bao nhiêu.

| Thước | Cùng một bản, các lần chạy lệch nhau | Đọc thế nào |
|---|---|---|
| 41 câu khó (Claude, hai cặp lượt) | đạt máy 33 ↔ 30 và 32 ↔ 33; lỗi hiện ra 5 ↔ 8; thời gian trung vị lượt cuối lệch tới khoảng 3 giây | chênh ≤ 3 mục là nhiễu |
| 12 vai (ba lượt) | phiên đạt lệch 1; ý đạt lệch 1–2; lượt hỏng lệch 5–9 | chênh 1 phiên chưa nói gì |
| chuỗi hội thoại (bản đầu) | Claude 0 ↔ 2 lượt bị từ chối; gpt-6-luna 1 ↔ 1 | chênh ≤ 2 lượt là nhiễu |
| thước 29 câu | 0 câu đổi giữa hai lượt mỗi model | chênh từ 2 câu mới đáng kể |

Từ chiều 21/11 luật đo của nhóm ghi: "thước nhỏ / nhiều lượt: ít nhất BA lượt lặp mỗi bên, "tốt hơn" khi mọi cặp lượt cùng chiều VÀ chênh gộp lớn hơn chênh lớn nhất giữa hai lượt không đổi gì; không đạt ⇒ "chưa rõ"." Bảng mốc 12 vai là một ví dụ áp luật: Claude hơn gpt-6-luna ở cả ba cặp lượt (7 · 7 · 8 so với 6 · 5 · 6 phiên đạt), và chênh gộp lớn hơn mức nhiễu 1. Nghĩa là: cộng chênh của các cặp lượt lại, con số đó phải lớn hơn độ lệch lớn nhất từng thấy khi chạy cùng một bản hai lần.

## Quyết định và lý do

### 1. Vì sao để một model đóng vai người dùng, mà không chỉ viết sẵn các chuỗi?

- **Đã chọn:** một model thứ ba (Claude Opus 5.5) đóng 12 vai, tự nghĩ tin tiếp theo; chạy qua đường chat thật.
- **Vì sao:** chuỗi viết sẵn chỉ hỏi điều người viết đã nghĩ tới. Hồ sơ đo ghi mục tiêu là tìm chỗ hỏng mà thước đang có không thấy, và lượt đầu đã tìm ra tám loại câu mới mà bộ thước cũ không phủ (danh sách ở mục trên).
- **Cách khác:** chỉ dùng 25 chuỗi viết sẵn: vẫn giữ, cho phần nhớ hội thoại. Để chủ dự án tự dùng thử 20 phút làm phép đối chiếu với người thật: đã đề xuất, chưa làm.
- **Cái giá:** người mô phỏng cùng họ model với hệ thống đang chạy (Opus và Sonnet đều là Claude), nên có thể dễ tính với nhau; điều này được ghi trước khi đo. Người dùng do model đóng thường dễ hơn người thật. Mốc ba lượt 12 vai × hai model tốn khoảng 14 USD.

### 2. Vì sao người chấm 12 vai phải đọc mù?

- **Đã chọn:** bản ghi giấu tên model, gọi hệ X / hệ Y, khoá đổi theo từng lượt; người chấm là agent con ngữ cảnh mới, chấm theo luật ghi trước.
- **Vì sao:** lượt đầu do phiên làm việc đọc tay, biết bên nào là model nào; số đó (6 và 9 trên 12) mới là một lượt, một người đọc, nên chưa dùng làm mốc được. Đọc mù và nhiều lượt là cách tách ý kiến của người chấm khỏi chênh thật.
- **Cách khác:** model chấm (Opus) đọc không mù: đã thử ở lượt đầu, không tách được hai model ⇒ chỉ để tham khảo.
- **Cái giá:** mỗi lượt cần một agent con mới đọc 24 phiên; chưa có số khớp với người dùng thật.

### 3. Vì sao thước nhỏ cần ít nhất ba lượt mỗi bên?

- **Đã chọn:** luật ở mục trên, có từ 17:33 ngày 21/11.
- **Vì sao:** nhiễu đo được lớn so với cỡ thước: 3 trên 41 mục, 1 trên 12 phiên. Một lượt mỗi bên thì chênh 1–2 không phân được thật hay may. Cùng chiều, một tra cứu công khai về người dùng mô phỏng cũng khuyên chạy mỗi vai ba lượt mỗi bản.
- **Cách khác:** một lượt mỗi bên (cách làm trước 21/11): dùng ở nhiều phép đo cũ; các phép đó nay đọc là "chưa rõ" khi chênh nhỏ.
- **Cái giá:** tốn gấp ba. Tối 21/11 chủ dự án nhắc lần nữa về chuyện đo quá nhiều; nhóm chốt dùng ba lượt **chỉ** khi phải chọn thật giữa hai bản chênh nhỏ, và đề xuất (chưa thành luật) mặc định một lượt, thước chạm trần ngay lượt đầu thì dừng lặp. Chữ trong luật chưa sửa theo.

### 4. Vì sao giữ một kịch bản demo chạy lặp, khi nó đã ở trần?

- **Đã chọn:** 10 bước cố định, chạy 10 lần mỗi model lúc lập mốc; sau đó chạy một lần trên model đang chạy sau mỗi lần gộp thay đổi.
- **Vì sao:** kịch bản chạm 23 trên 31 tính năng đang mở lúc đó, nên một lần chạy là một phép thử khói rẻ cho cả hệ thống. Lời giao ghi trước: hỏng do bản gộp thì tắt lại dòng cấu hình vừa mở. Ba lần thử khói sau gộp (tối 21/11, sáng 22/11 hai lần) đều 0 bước hỏng.
- **Cách khác:** chỉ chạy lúc lập mốc: không làm.
- **Cái giá:** nhóm tự ghi rằng chạy 10 lần × hai model là đo thừa, vì thước ở trần ngay lần đầu. Ở trần thì nó không phân biệt được bản tốt với bản tốt hơn.

## Nếu… thì sao

Bài này về cách đo, không có thứ hỏng ở phía người dùng. Ba điều kiện đổi:

| Nếu | Điều đã biết | Làm gì |
|---|---|---|
| đổi model viết | mọi số của phần trợ lý phải đo lại; người chấm 176 câu cũng đã đổi sang Claude từ tối 21/11, nên số mới không so thẳng với số cũ | lập mốc lại trên mỗi thước dùng tới |
| một thước chạm trần (demo 0 / 10 lần hỏng) | nó không còn phân biệt được hai bản | chỉ dùng làm phép thử khói |
| chênh giữa hai bản nhỏ hơn nhiễu | luật ghi "chưa rõ" | không gọi là tốt hơn; chạy thêm lượt chỉ khi lựa chọn thật sự phụ thuộc vào nó |

## Dễ nhầm

- **"12 vai đạt 8 / 12 nghĩa là 4 vai lỗi hệ thống."** Trong bốn vai chưa đạt, ba vai vướng một ý mà kho chưa có thông tin (một ý khác vì tính năng đang tắt); vai còn lại vướng phần sửa lịch. Trần của thước với Claude khoảng 8–9 trên 12.
- **"Bộ dò mù là người chấm không biết bên nào."** Đó là đọc mù. Bộ dò mù là bộ câu do người khác người làm soạn, chưa đọc chương trình.

## Câu hỏi tự kiểm

Thử trả lời bằng lời của mình trước khi bấm mở đáp án.

<details>
<summary>1. Vì sao bộ 176 câu không thấy lỗi "phần hỏi bị bỏ im" của tin vừa sửa lịch vừa hỏi?</summary>

Bộ 176 câu gửi mỗi câu như tin đầu của một cuộc mới; nó không có lịch đã lưu, không có lượt sửa. Lỗi chỉ lộ khi có người dùng (thật hay mô phỏng) đi qua nhiều lượt.

</details>

<details>
<summary>2. Bộ 41 câu khó: bản sửa ra 33, bản cũ ra 30. Có nói bản sửa tốt hơn được không?</summary>

Không: cùng một bản chạy hai lần đã lệch 33 ↔ 30. Chênh 3 mục nằm trong nhiễu; cần ít nhất ba lượt mỗi bên, mọi cặp cùng chiều và chênh gộp lớn hơn nhiễu.

</details>

<details>
<summary>3. Ai đóng vai người dùng, ai chấm, và vì sao phải tách?</summary>

Claude Opus 5.5 đóng vai; agent con ngữ cảnh mới đọc mù chấm. Người chấm biết bên nào là model nào thì ý kiến lẫn vào số; tách và giấu tên để chênh còn lại là chênh của hệ thống.

</details>

## Cấu hình đang chạy

Bài này không có cấu hình của hệ thống; bảng dưới là cấu hình của các thước.

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| model đóng vai người dùng | Claude Opus 5.5 | khác model đang chạy, nhưng cùng họ (giới hạn ghi trước) | chưa thử model khác họ |
| số lượt mỗi phiên mô phỏng | ≤ 5 | — | — |
| số vai | 12, cộng 4 vai để riêng chấm bằng mẫu chữ | — | — |
| số lượt mốc 12 vai | 3 mỗi model | luật "ít nhất ba lượt" | lượt đầu 1 lượt: chưa dùng làm mốc |
| bộ 41 câu khó | đóng băng 13:01 21/11; bộ đã thấy | so theo cặp | — |
| chuỗi hội thoại | 25 chuỗi / 56 lượt đã thấy; thêm một bộ kín 15 chuỗi / 33 lượt | — | — |
| kịch bản demo | 10 bước; lúc mốc 10 lần × 2 model, sau đó 1 lần sau mỗi lần gộp | — | 10 × 2: nhóm tự ghi là thừa |
| tiêu chí ghi trước | ghi vào hồ sơ đo TRƯỚC khi chạy, kèm giờ | để không chỉnh luật sau khi thấy số | — |

## Đã so

**12 vai, mốc ba lượt (tối 21/11, đọc mù, cùng một bản hệ thống):**

| | lượt 1 | lượt 2 | lượt 3 | mức nhiễu |
|---|---|---|---|---|
| gpt-6-luna — phiên đạt / 12 | 6 | 5 | 6 | 1 |
| Claude Sonnet 5.5 — phiên đạt / 12 | 7 | 7 | 8 | 1 |
| gpt-6-luna — ý đạt / 38 | 29 | 28 | 30 | 2 |
| Claude Sonnet 5.5 — ý đạt / 38 | 31 | 32 | 32 | 1 |
| gpt-6-luna — lượt hỏng | 22 | 19 | 13 | 9 |
| Claude Sonnet 5.5 — lượt hỏng | 11 | 10 | 6 | 5 |

Cột máy cùng lượt: gpt-6-luna chạm trần số vòng 7 · 8 · 3 lần, Claude 0 · 0 · 0.

**41 câu khó (21/11, luật máy):**

| Lượt | gpt-6-luna | Claude Sonnet 5.5 |
|---|---|---|
| lượt đầu: đạt máy / 41 | 24 | 31 |
| lượt đầu: lỗi hoặc từ chối trống | 16 (39 %) | 8 (20 %) |
| mới nhất (15:26 21/11, bản đang chạy trên main lúc đó) | 25 | **39** (người dùng nhận lỗi 1, chạm trần 0, trung vị lượt cuối 14,1 giây) |

**Thước 29 câu:** Claude 29 / 29, gpt-6-luna 28 / 29; nhóm ghép công cụ 8 / 8 và 7 / 8; 10 câu an toàn và 10 câu ngoài phạm vi: 0 câu bị từ chối nhầm, 0 câu bị trả lời bằng kho ở cả hai model; chấm mù riêng bộ an toàn thì thiếu cảnh báo 5 / 8 (gpt-6-luna) và 1 / 8 (Claude), không câu nào đảo cảnh báo.

**Kịch bản demo (21/11):** 0 / 10 lần hỏng mỗi model, 0 / 100 bước hỏng. Đọc tay thêm: bước "nhờ đặt phòng", Claude chỉ 1 / 10 lần có link sang trang Chỗ ở; bước hỏi số giờ của ngày 1 trên lịch vừa lập có trung vị 12–14 giây, lâu nhất 18 giây. Ba lần thử khói sau gộp (22:20 21/11, 08:22 và 10:29 22/11) đều 0 bước hỏng.

**Chuỗi hội thoại (21/11, bản đầu):** lượt phải trả lời mà bị từ chối trên 43 lượt: gpt-6-luna 1, Claude mức vừa 6, Claude mức cao 4. Tuyến khác nhãn trên 56 lượt: 0, 6, 5.

**Bộ dò mù của các tính năng:** dòng chỉ sang trang Lên kế hoạch 17 / 20 nhận đúng, 0 / 20 nhận nhầm; tin sửa lịch kèm hỏi 24 / 24 và 0 / 24; đổi chỗ hai ngày 0 / 10 đọc nhầm; câu xin danh sách 19 / 20, nối nhầm 2 / 32; câu "gần X" 0 / 12 lỗi.

**Đọc bảng thế nào:** ở 12 vai, Claude hơn ở mọi cặp lượt và chênh lớn hơn nhiễu, nên theo luật là "tốt hơn". Ở 41 câu khó, lượt đầu hai model đều một lượt; số 39 / 41 là sau các sửa trong ngày, trên bộ mà người sửa đã thấy.

**Giới hạn của phép đo:** người mô phỏng cùng họ với model đang chạy; chưa có phép đối chiếu với người thật; mọi bộ của phần trợ lý là bộ đã thấy (trừ các bộ dò mù và bộ chuỗi kín); thời gian chờ ở mốc ba lượt không so được vì hai model chạy song song trên cùng máy.

## Quyết định nhỏ hơn

**Vì sao bộ 41 câu khó chấm bằng luật máy?** **Đã chọn:** "đạt máy" = lượt cuối không hiện lỗi, không chạm trần vòng, từ chối hay trả lời đúng như mong đợi, có đủ các cụm chữ phải có. **Vì sao:** chưa thấy ghi lý do riêng. Điều thấy được: bộ được dùng để so theo cặp nhiều bản trong một buổi (mỗi bản một lượt 41 mục phát lại cả lịch sử), và chính tài liệu của bộ ghi máy chấm "thô hơn đọc tay"; các loại "bỏ im", "báo chưa có", "quên câu trước" phải đọc tay theo mong đợi đã ghi. **Cách khác:** model chấm từng mục: chưa thử cho bộ này. **Cái giá:** bộ là bộ "đã thấy" (rút từ chính các phiên mà người sửa đã đọc), nên dễ bị sửa cho vừa nó; điểm đạt máy cao không chắc là câu trả lời hay.

## Giới hạn đã biết

- Chưa có đối chiếu với người dùng thật cho thước nhiều lượt; đề xuất để chủ dự án tự dùng thử 20 phút chưa làm.
- Ba trong bốn vai chưa đạt ở 12 vai vướng ý kho thiếu; trần thước với Claude khoảng 8–9 / 12.
- Người mô phỏng hay tự kết sớm (6 / 12 phiên gpt-6-luna, 5 / 12 phiên Claude kết trước lượt 5), nên phiên ngắn có thể đạt dễ hơn; chưa ai tách số này.
- Bộ 176 câu chưa chạy đủ trên Claude (mới 85 câu đầu và 54 câu so sánh, nhiều nguồn).
- Lượt 12 vai đo lại sau các sửa buổi sáng 22/11 (một lượt, 14:13): 8 trên 12 phiên, 33 trên 38 ý, vẫn trong khoảng nhiễu của mốc ba lượt (7, 7, 8). Thước có một điểm mù vừa lộ ra: người dùng mô phỏng không thấy dòng báo của lượt sửa lịch; công cụ đã được chữa, chưa đo lại.
- Luật "ba lượt" chưa được sửa chữ cho khớp lựa chọn tối 21/11 (chỉ khi phải chọn giữa hai bản chênh nhỏ).

## Chi tiết để tra

- Thời gian chờ mỗi lượt ở 12 vai lượt đầu: gpt-6-luna trung vị 10,0 giây (lâu nhất 37 giây), Claude trung vị 12,5 giây (lâu nhất 28 giây).
- Một lượt có tìm thêm cụ thể (ví dụ "phải tìm thêm", gpt-6-luna, 20/11): xếp loại 2,3 giây, ba vòng viết 1,1 · 2,7 · 3,3 giây, cả lượt 7,5 giây (bài 21). Trên model đang chạy (49 lượt, 21/11): lần viết cuối chiếm khoảng 72 % thời gian của lượt (trung vị 9,7 giây); các vòng công cụ thường là 2 vòng, khoảng 2,2 giây mỗi vòng (model cũ 2,0 giây).
- Lượt đầu 12 vai (trưa 21/11): lượt nhận từ chối trống hoặc lỗi gpt-6-luna 12 / 48 (25 %), Claude 7 / 53 (13 %); phiên đạt (phiên làm việc đọc tay, không mù) 6 và 9 / 12.
- Bốn vai để riêng (chấm bằng mẫu chữ) không tính trong 12 vai.
- Bộ 41 câu khó theo loại: chạm trần số vòng 6 mục, câu bị rút vì nhắc lại số dự báo 5, sửa lịch kèm câu hỏi 4, kho có mà báo chưa có 3, quên câu trả lời trước 3, nói thật năng lực 3, mười một loại còn lại 1–2 mục mỗi loại. Số lượt lịch sử trước câu cuối: 0 lượt 6 mục, 1 lượt 13, 2 lượt 10, 3 lượt 7, 4 lượt 5.
- Người chấm 176 câu: gpt-6-luna, thêm Claude mức cao từ trưa 21/11, chuyển hẳn sang Claude tối 21/11 (bài 19). Kiểm người chấm bằng phiếu đã biết mức: gpt-6-luna 11 / 12, Claude 12 / 12.
- Kết quả an toàn: `data/thu_bedrock_2026-11-21/do/agent/KET_QUA_AGENT.md` dòng 40 (thiếu cảnh báo 5 / 8, 1 / 8; người viết đã mở); bị rút 7 lượt, 5 / 6 lượt phát lại vì số dự báo: `c_nguoi_dung_mo_phong/KET_QUA.md` dòng 10, 38 (người viết đã mở).
- Chấm an toàn của thước: hai agent con đọc mù; phép đối chứng bắt 10 / 10 câu chèn sai, báo nhầm 0 / 5.

**Bài sau (bài 33):** model viết, mức suy luận, và đổi model bằng một dòng cấu hình.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Bộ 176 câu không đủ cho phần trợ lý: `bai_hoc/VIEC_MOI_XONG.md` dòng 363–364; `bai_hoc/giao_trinh/17_BO_CAU_HOI_MAU.md` (dòng "đo bằng các bộ khác (bài 32)"); `data/thu_bedrock_2026-11-21/c_nguoi_dung_mo_phong/THIET_KE.md` dòng 3; `KET_QUA.md` dòng 24–32 (tám loại câu mới); độ đúng sự thật vẫn do bộ 176 câu giữ: `VIEC_MOI_XONG.md` dòng 398 [chép; riêng tư cho `data/`].
- Người dùng mô phỏng: `THIET_KE.md` (dòng 7–8 đường chat thật, giới hạn cùng họ; 11–23 mười hai vai; 25–27 Opus, không kho, `<XONG>`; 31–32 người chấm), `c_nguoi_dung_mo_phong/chay.py` (`SO_LUOT = 5`, model) [riêng tư; code]. Lỗi tìm ra, 12 / 48, 7 / 53, 6 / 9, Opus không tách được: `KET_QUA.md` dòng 7–22, 36–45 [riêng tư; đã chạy]. Vòng lặp "thêm X": chú thích `backend/llm/sua_lich_v2.py` (người dùng mô phỏng 21/11) [code].
- Mốc ba lượt, đọc mù, hệ X / Y, r1 hai người đọc khớp: `data/thu_bedrock_2026-11-21/do/moc_12vai/doc_mu/TONG_HOP_MOC.md` dòng 1–11 (người viết đã mở), `LUAT_CHAM.md`; chạm trần 7 · 8 · 3 / 0 · 0 · 0: `do/moc_12vai/KET_QUA_MOC.md` [riêng tư; đã chạy]. 14 USD, trần 8–9 / 12, ba trong bốn ý do kho thiếu: `VIEC_MOI_XONG.md` dòng 401–423 [chép].
- 41 câu khó: `c_nguoi_dung_mo_phong/bo_cau_kho.json` (17 loại, số mục mỗi loại, số lượt lịch sử — agent con đếm bằng máy trường `loai_kho`, không đọc câu) [riêng tư; đã chạy]; luật "đạt máy" và "THÔ hơn đọc tay": `data/thu_bedrock_2026-11-21/tools/e_thuoc_kho.py` dòng 7–8, 182–187 [code]; nhiễu 33 ↔ 30, 32 ↔ 33, 5 ↔ 8, 13,9 ↔ 13,7 và 16,7 ↔ 14,1 giây, kết quả 39 / 41 lúc 15:26: `data/thu_bedrock_2026-11-21/TIEU_CHI_DO.md` mục 21–23 (người viết đã mở) [riêng tư; đã chạy]; lượt đầu 24 / 31, 16 / 8: `VIEC_MOI_XONG.md` dòng 526–527 [chép].
- Chuỗi hội thoại: `data/phase_9/bo_do_b3/README.md` dòng 10–11, 34–45 (25 / 56; bộ kín 15 / 33, người viết và agent con không mở bộ kín); số theo loại và độ dài đếm bằng máy; kết quả 1 / 6 / 4, 0 / 6 / 5: `data/thu_bedrock_2026-11-21/do/agent/KET_QUA_AGENT.md` dòng 20–29; nhiễu 0 ↔ 2, 1 ↔ 1: `TIEU_CHI_DO.md` dòng 170 [riêng tư; đã chạy].
- Kịch bản demo: `data/thu_bedrock_2026-11-21/do/TIEU_CHI_BUOC_0_VA_3.md` dòng 19–39 (10 bước, 23 / 31 tính năng), `do/demo/chay_demo.py`, `do/demo/KET_QUA_DEMO.md` dòng 4–19, các file `do/demo/khoi_main_*.log`; lời giao "hỏng do bản gộp ⇒ tắt lại một dòng": `report_agent/2026-11-22/TONG_HOP.md` dòng 18; ba log thử khói đều `so_lap_co_buoc_hong: 0` (người viết đã mở); tự ghi "đo thừa": `session_prompt/SO_CAI_TIEN_CACH_LAM.md` dòng 399 [riêng tư; chép qua agent con].
- Thước 29 câu: `VIEC_MOI_XONG.md` dòng 511–513; nhiễu 0 câu đổi: `TIEU_CHI_DO.md` dòng 170 [chép].
- Bộ dò mù (định nghĩa và số): `VIEC_MOI_XONG.md` dòng 229, 325, 330, 338–341, 572, 583; `settings.yaml` (`sua_lich_doi_cho_ngay`: 0 / 10) [chép].
- Luật "ít nhất BA lượt": `skills/run-experiment/SKILL.md` dòng 100–101 (người viết đã mở, chép nguyên văn); có từ commit `f2dc556c` 17:33 21/11/2026 (agent con dò bằng `git log -S`); lý do: `session_prompt/HIEN_TRANG.md` dòng 70 (số đầu một lượt, một người đọc), `report_agent/2026-11-21/TONG_HOP.md` dòng 27 (tra cứu công khai: "chạy mỗi vai ba lượt mỗi bản"); nới tối 21/11: `session_prompt/SO_CAI_TIEN_CACH_LAM.md` dòng 390, 403, `report_agent/2026-11-22/TONG_HOP.md` dòng 26; chữ luật chưa sửa: `session_prompt/sessions/STATUS_A.md` dòng 11 [chép qua agent con].
- Người chấm 176 câu và kiểm người chấm 11 / 12, 12 / 12: `TIEU_CHI_DO.md` dòng 62, 114, 118, 130; chuyển hẳn sang Claude: `HIEN_TRANG.md` dòng 65; 176 câu chưa chạy đủ trên Claude: `VIEC_MOI_XONG.md` dòng 554 [chép]. Chấm an toàn 10 / 10, 0 / 5: `KET_QUA_AGENT.md` dòng 40 [riêng tư].
- Đối chiếu người thật chưa có, đề xuất 20 phút: `report_agent/2026-11-21/TONG_HOP.md` dòng 27 [chép].
- Thời gian 10,0 / 37 và 12,5 / 28 giây: `KET_QUA.md` dòng 18; thời gian không so được ở mốc: `VIEC_MOI_XONG.md` dòng 399. Lượt "phải tìm thêm" 2,3 + 1,1 · 2,7 · 3,3 = 7,5 giây: bài 21 của giáo trình. 72 %, 9,7 giây, 2 vòng × 2,2 giây (model cũ 2,0): `data/thu_bedrock_2026-11-21/b_toc_do/THOI_GIAN_DI_DAU.md` dòng 12–16 (người viết đã mở) [riêng tư; đã chạy].
- Bài này chủ yếu dựa vào bảng sự thật của một agent con đọc-chỉ; người viết đã tự mở `skills/run-experiment/SKILL.md`, `TONG_HOP_MOC.md`, `TIEU_CHI_DO.md` mục 21–23 để đối chiếu.

- Bài đã qua một lượt đối chiếu độc lập (người kiểm chỉ đọc, tự chạy lại bộ xếp và phần áp lệnh), trưa 22/11/2026: `data/hoc_cung_D/kiem/bai_27_32.md` [riêng tư]; các dòng SAI / LỆCH đã áp, dòng không áp ghi ở `data/hoc_cung_D/viet/viet_27_32.md` mục "Sau lượt kiểm" [riêng tư].

</details>
