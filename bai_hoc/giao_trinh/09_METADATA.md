# Bài 9 — Thông tin gắn kèm mỗi đoạn (metadata) và "chữ để tìm"

*Cập nhật 20:46, ngày 23/11/2026 · số kho / số tính năng / mức test theo hệ thống lúc code đứng yên tối 23/11 (kho 269 bài / 9.533 đoạn) · bản 22:43 22/11: thêm một vế cho dòng "có thể đã thay đổi" (bài chỉ được nêu tên) · cơ chế đọc từ chương trình đang chạy; số kho khớp bản ghi hiện trạng lúc 13:33; ví dụ lấy từ lượt hỏi thật ngày 21/11; số của phép so lấy từ báo cáo đo cuối tháng 10; người viết không chạy lại phép đo nào. · 09:56 24/11/2026: số đoạn của kho trong thân bài 9.533 ⇒ 9.536 (ba bài kho được thêm câu sáng 24/11; chỉ mục cập nhật 07:30 và 07:49; bản ghi chỉ mục và Qdrant cùng ghi 9.536).*

**Bài trước đã biết:** 269 bài (từ 18:05 23/11) được cắt thành 9.536 đoạn nhỏ, phần lớn chỉ một hai câu.
**Bài này thêm:** một đoạn nhỏ đứng riêng thì không biết nó nói về cái gì. Bài này giảng những thông tin được gắn kèm mỗi đoạn, chúng được dùng ở đâu, và vì sao chỉ gắn chừng đó.

## Ý chính

- Mỗi đoạn mang theo **tên bài** và **tên các mục chứa nó**. Nhờ đó một đoạn chỉ có một dòng giá vẫn biết mình là giá của cái gì.
- Thông tin gắn kèm được dùng ở **hai chỗ**: lúc tìm (ghép vào "chữ để tìm" của đoạn) và lúc viết (in ở đầu mỗi đoạn đưa cho model).
- Mỗi đoạn cất trong cơ sở dữ liệu kèm đúng **7 trường**. Hai trường từng được nghĩ tới (chủ đề con, thẻ phân loại) bị loại ngay lúc thiết kế vì chưa có chỗ dùng.
- Hệ thống **không lọc theo chủ đề** khi tìm: mọi câu hỏi đều tìm trên cả kho.
- Đã thử bỏ tên bài và tên mục khỏi "chữ để tìm": 3–4 câu tốt lên nhưng 7–8 câu mất đáp án, nên giữ.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| thông tin gắn kèm | **metadata** | những gì đi cùng một đoạn ngoài chính thân chữ của nó |
| tên bài | **title** | tiêu đề lớn nhất của bài |
| đường tiêu đề | **heading path** | chuỗi tên các mục đứng trên đoạn, nối bằng dấu ">" |
| chữ để tìm | **search text** | tên bài + đường tiêu đề + thân đoạn, ghép lại; đây là thứ được đổi thành vector và từ khoá |
| hồ sơ của đoạn | **payload** (của Qdrant) | 7 trường cất cùng mỗi đoạn, để khi tìm ra thì lấy lại được đủ thông tin |
| chủ đề | **domain** | nhóm lớn của bài: món ăn, di tích, lễ hội, nghệ thuật biểu diễn, du lịch |

## Một đoạn đứng riêng không biết mình nói về cái gì

Lấy đoạn số 3 trong 10 đoạn của ví dụ chính. Thân của nó là một danh sách giá: "Gói tham quan 45 phút: 240.000 đồng/xe. Gói tham quan 60 phút: 300.000 đồng/xe…". Đọc riêng thân đoạn thì không biết đây là giá của dịch vụ nào, ở đâu.

Chỗ nói điều đó nằm ở các tiêu đề phía trên nó trong bài: bài nói về vé các điểm tham quan và các trải nghiệm khác, mục lớn là các dịch vụ bổ trợ trong Đại Nội, mục con là "Dịch vụ Xe điện Hoàng Thành". Khi cắt, các tiêu đề này không thành đoạn riêng (bài 8). Chúng được gắn vào từng đoạn nằm dưới.

## Tên bài và tên mục được dùng ở hai chỗ: lúc tìm và lúc viết

**Lúc tìm.** Thứ được đổi thành vector và từ khoá không phải thân đoạn trơn. Đó là **chữ để tìm**, ghép từ ba phần:

```text
Vé các điểm tham quan và trải nghiệm …                                  ← tên bài
6. Các dịch vụ … trong Quần thể Di tích Đại Nội Huế > Dịch vụ Xe điện Hoàng Thành   ← đường tiêu đề
Biểu giá dịch vụ … Gói tham quan 45 phút: 240.000 đồng/xe …             ← thân đoạn
```

Thân đoạn này có "tham quan", có "Đại Nội", nhưng không có chữ "vé" nào. Chữ "vé" nằm ở tên bài. Nhờ tên bài được ghép vào, chữ để tìm của đoạn khớp thêm với chữ "vé" trong câu hỏi *"Giá vé tham quan Đại Nội Huế là bao nhiêu?"*.

**Lúc viết.** Mỗi đoạn đưa cho model viết được trình bày thành một khối có nhãn. Đây là đoạn số 4 trong ví dụ chính:

```text
[Nguồn 4]
Tiêu đề: Cẩm nang nghệ thuật biểu diễn Huế
Mục: Giá vé và cách đặt chỗ … > 1. Vé biểu diễn tại Nhà hát …
Bằng chứng:
- (một câu nói vé xem biểu diễn tách rời với vé vào Đại Nội, và nhắc giá vé vào cổng: người lớn 200.000, trẻ em 7–12 tuổi 40.000, dưới 7 tuổi miễn phí)
```

(Trong khối trên, tên mục được viết tắt và phần bằng chứng được tóm lại chứ không chép nguyên văn.) Model đọc là biết đoạn này thuộc bài nào, mục nào, và phải ghi số [4] nếu dùng nó. Trong câu trả lời thật, giá vé trẻ em được lấy đúng từ đoạn này và mang số [4].

## Mỗi đoạn cất kèm đúng 7 trường

| Trường | Là gì | Dùng để làm gì |
|---|---|---|
| chữ để tìm | tên bài + đường tiêu đề + thân đoạn | đổi thành vector (bài 10) và chấm từ khoá (bài 11) |
| tên bài | tiêu đề lớn nhất của bài | in ở dòng "Tiêu đề" cho model viết; hiện ở danh sách nguồn |
| đường tiêu đề | tên các mục đứng trên đoạn | in ở dòng "Mục" cho model viết |
| phần bằng chứng | các mảnh chữ của đoạn kèm vị trí trong bài gốc (bài 8) | là phần "Bằng chứng" đưa cho model viết; hiện lại cho người dùng khi bấm vào nguồn |
| nguồn | đường dẫn của bài trong kho | biết đoạn thuộc bài nào; quyết định có thêm dòng "thông tin có thể đã thay đổi" không |
| mã đoạn | đường dẫn file của bài kèm số thứ tự của đoạn | gọi tên đoạn; mã cất trong cơ sở dữ liệu suy ra từ mã này |
| chủ đề | lấy từ thư mục đầu của đường dẫn | hiện chỉ dùng để kiểm và ghi vết; chưa có chỗ nào đọc nó khi trả lời |

## Hệ thống không lọc theo chủ đề khi tìm

Có thể gắn thêm nhiều trường nữa (chủ đề con, khu vực, mức giá…) rồi dùng chúng để lọc trước khi tìm, ví dụ "chỉ tìm trong nhóm món ăn". hue_rag không làm vậy: mọi câu hỏi đều tìm trên cả 9.536 đoạn.

Ví dụ chính cho thấy một hệ quả của lựa chọn này: câu hỏi về giá vé được trả lời bằng đoạn của hai bài vé **và** một đoạn của bài nghệ thuật biểu diễn. Nếu hệ thống lọc "chỉ tìm trong nhóm du lịch" (nhóm chứa các bài vé) thì đoạn số 4, nơi có giá vé trẻ em, đã không được xét. Lý do và cái giá: quyết định 3 và 4 dưới đây.

## Quyết định và lý do

### 1. Vì sao ghép tên bài và tên các mục vào chữ để tìm, thay vì chỉ dùng thân đoạn?

- **Đã chọn:** chữ để tìm = tên bài + đường tiêu đề đầy đủ + thân đoạn.
- **Vì sao:** đã đo cuối tháng 10 (mục "Đã so"): bỏ hẳn thì 3 câu tốt lên nhưng 8 câu mất đáp án trên 32 câu; chỉ giữ tên mục gần nhất thì 4 câu tốt lên, 7 câu mất. Luật ghi trước là không mất câu nào.
- **Cách khác:** hai cách bớt trên: đã đo, bỏ.
- **Cái giá:** mọi đoạn của một bài có chung phần đầu. Với đoạn rất ngắn, phần chung đó chiếm gần hết chữ để tìm, nên các đoạn cùng bài trông giống nhau.

### 2. Vì sao mỗi đoạn đưa cho model viết có nhãn "Tiêu đề", "Mục", "Bằng chứng"?

- **Đã chọn:** mỗi đoạn là một khối: số nguồn, tên bài, đường tiêu đề, rồi các mảnh bằng chứng.
- **Vì sao:** chưa thấy ghi lý do. Điều thấy được: model chỉ thấy các khối này, không thấy bài gốc; ở ví dụ chính, giá vé trẻ em được lấy từ khối mang số [4], và số đó là thứ chương trình kiểm sau khi model viết (bài 16).
- **Cách khác:** dạng khối khác: chưa so.
- **Cái giá:** tên bài và tên mục được tính vào số chữ gửi model ở mọi đoạn.

### 3. Vì sao không lọc theo chủ đề khi tìm, ví dụ "chỉ tìm trong nhóm món ăn"?

- **Đã chọn:** mọi câu hỏi tìm trên cả 9.536 đoạn.
- **Vì sao:** lập luận, không phải số đo: câu hỏi hay chạm nhiều chủ đề, và lọc sai một lần là mất đáp án. Ví dụ ở mục trên: đoạn số 4 nằm ngoài nhóm du lịch.
- **Cách khác:** lọc theo chủ đề: chưa đo.
- **Cái giá:** không có cách "chỉ tìm trong lễ hội"; một câu hỏi về món ăn vẫn có thể kéo về đoạn của bài di tích.

### 4. Vì sao hồ sơ của đoạn chỉ có 7 trường?

- **Đã chọn:** 7 trường (bảng ở mục trên); không có trường chủ đề con, thẻ phân loại hay trường để lọc.
- **Vì sao:** quyết định đã ghi: ngày 11/09 chủ dự án chốt nguyên tắc chỉ thêm trường khi đã có chỗ dùng; lúc thiết kế lại hồ sơ (cuối tháng 9), chủ đề con, thẻ và việc lọc bị loại vì chưa có chỗ nào dùng. Lập luận đi kèm, không phải số đo: mỗi trường thêm vào là một thứ phải giữ đúng mỗi lần sửa kho.
- **Cách khác:** hồ sơ 5 trường (bản trước): thay bằng 7. Thêm trường: không làm.
- **Cái giá:** muốn lọc sau này thì phải thêm trường và lập lại chỉ mục.

### 5. Vì sao thông tin gắn kèm do chương trình lấy từ cấu trúc bài, mà không nhờ model viết một câu tóm bối cảnh cho mỗi đoạn?

- **Đã chọn:** chương trình đọc tên bài và các tiêu đề lúc cắt đoạn (bài 8), không gọi model.
- **Vì sao:** lập luận, không phải số đo: tên bài và đường tiêu đề có sẵn trong bài, không tốn lần gọi model nào, và không có rủi ro model viết sai bối cảnh.
- **Cách khác:** model viết câu tóm bối cảnh: đã gọi thử ở giai đoạn đầu, nhưng chưa từng lập thành chỉ mục và chưa đo; phần chương trình đó đã gỡ cuối tháng 10.
- **Cái giá:** bài đặt tên mục nghèo thì đoạn mang nhãn kém; nhãn tốt phụ thuộc người soạn theo mẫu (bài 7).

## Nếu… thì sao

Đọc từ chương trình; người viết chưa thử lại.

| Nếu | Hệ thống làm gì | Người dùng thấy gì | Đã có chưa / ai làm gì |
|---|---|---|---|
| một bài đặt tên mục chung chung ("Thông tin khác") | các đoạn mang nhãn kém, khó khớp câu hỏi | có thể nhận câu từ chối dù kho có | người soạn đặt tên mục theo mẫu của chủ đề (bài 7) |
| bài mới đặt ngoài 7 thư mục được đưa vào kho | bài không vào chỉ mục | hệ thống không biết bài đó | người soạn đặt bài đúng thư mục |
| bài có giá không thuộc nhóm vé, địa điểm, lễ hội, và không phải bài "Lưu trú ở Huế" | dòng nhắc "có thể đã thay đổi" không được thêm | giá hiện ra mà không kèm dòng nhắc kiểm lại | đã có; danh sách nhóm ghi cố định trong chương trình |
| đổi tên file bài hoặc chuyển thư mục | mã của mọi đoạn bài đó đổi theo, các đoạn được tính lại | thường không thấy gì khác sau khi cập nhật chỉ mục. Riêng bài có điểm trong bảng điểm của trang Lên kế hoạch: máy chủ không bật được ở lần bật sau, tới khi sửa bảng. Bài đổi nhóm thì dòng nhắc "có thể đã thay đổi" có thể mất hoặc thêm | đã có (bài 6, 12) |
| một điểm trong Qdrant thiếu trường hoặc sai dạng | bước tìm dừng mỗi khi điểm đó lọt vào ứng viên | "Hệ thống tra cứu tạm thời không khả dụng." và nút "Thử lại" | đã có; chữa bằng dựng lại chỉ mục (lập luận) |

## Dễ nhầm

- **"Metadata là để lọc."** Ở hệ thống này thì không. Nó để đoạn tự nói được mình thuộc bài nào, mục nào, lúc tìm và lúc viết.
- **"Vector được tính từ thân đoạn."** Không. Nó được tính từ chữ để tìm, tức có cả tên bài và tên mục.
- **"Model viết nhìn thấy cả bài."** Không. Nó chỉ thấy từng khối: số nguồn, tên bài, tên mục, và mảnh bằng chứng.

## Câu hỏi tự kiểm

<details>
<summary>1. Thông tin gắn kèm được dùng ở hai chỗ nào?</summary>

Lúc tìm: tên bài và đường tiêu đề được ghép vào chữ để tìm, thứ được đổi thành vector và từ khoá. Lúc viết: chúng đứng ở dòng "Tiêu đề", "Mục" đầu mỗi khối đưa cho model.

</details>

<details>
<summary>2. Đoạn số 3 của ví dụ chính không có chữ "vé" nào. Vì sao nó vẫn khớp câu hỏi về giá vé?</summary>

Chữ "vé" nằm ở tên bài, và tên bài được ghép vào chữ để tìm của mọi đoạn trong bài đó.

</details>

<details>
<summary>3. Thử bỏ tên bài và tên mục khỏi chữ để tìm thì sao, và nói kết quả đó thế nào cho đúng mức?</summary>

Bỏ hẳn: 3 câu tốt lên, 8 câu mất đáp án trên 32 câu, nên giữ. Nói đúng mức: "bỏ thì mất nhiều hơn được"; chưa phải "đã chứng minh tên bài giúp", vì mức chênh chưa đủ để phép thử thống kê khẳng định.

</details>

<details>
<summary>4. Vì sao hệ thống không lọc "chỉ tìm trong nhóm du lịch" cho câu hỏi về vé?</summary>

Câu hỏi hay chạm nhiều chủ đề. Ở ví dụ chính, giá vé trẻ em nằm ở bài nghệ thuật biểu diễn; lọc theo nhóm du lịch thì đoạn đó đã không được xét. Việc không lọc là lập luận, chưa đo.

</details>

## Cấu hình đang chạy

*Chép từ hệ thống đang chạy sáng 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Thành phần của chữ để tìm | tên bài + đường tiêu đề đầy đủ + phần bằng chứng | đoạn nhỏ vẫn khớp được với câu hỏi nêu tên nơi, tên món | đã thử hai cách bớt đi (mục "Đã so") |
| Dấu nối trong đường tiêu đề | " > " | — | — |
| Số trường trong hồ sơ của đoạn | 7 | — | chủ đề con và thẻ phân loại bị loại từ lúc thiết kế vì chưa có chỗ dùng |
| Lọc theo trường khi tìm | không | câu hỏi hay chạm nhiều chủ đề | chưa đo có lọc |
| Số chủ đề | 5 (món ăn, di tích, lễ hội, nghệ thuật biểu diễn, du lịch) | lấy từ thư mục đầu của bài; nhóm du lịch gồm ba thư mục con: địa điểm, dịch vụ, vé | — |
| Dạng khối đưa cho model viết | số nguồn · Tiêu đề · Mục · Bằng chứng | model biết nguồn nào nói gì và phải ghi số nào | chưa so dạng khác |

## Đã so

**Vấn đề.** Tên bài và tên mục làm chữ để tìm dài ra, và mọi đoạn của cùng một bài có chung một phần đầu. Câu hỏi đặt ra trong đợt rà cuối tháng 10: bớt phần này đi thì bước tìm có rõ hơn không?

**So gì, trên bộ nào.** Hai cách bớt, trên cùng 32 câu đã biết đáp án nằm ở đoạn nào, cùng một lượng chữ đưa cho model viết (như ở bài 8). Luật ghi trước: không được làm câu nào mất đáp án.

| Cách thử | Câu tốt lên | Câu như cũ | Câu mất đáp án | Kết luận |
|---|---:|---:|---:|---|
| Chỉ giữ tên mục gần nhất (bỏ tên bài và các mục cấp trên) | 4 | 21 | 7 | bỏ |
| Bỏ hẳn, chỉ còn thân đoạn | 3 | 21 | 8 | bỏ |

**Đọc bảng này thế nào.**
- Có câu tốt lên, nên không thể nói "bỏ đi thì tệ hẳn". Báo cáo đo không ghi vì sao các câu đó tốt lên.
- Nhưng số câu mất gấp đôi số câu được, và luật là không mất câu nào.
- Với 32 câu, mức chênh này chưa đủ để phép thử thống kê khẳng định là thật.

**Đã chọn: giữ tên bài và đường tiêu đề đầy đủ.** Cách nói đúng mức: "thử bỏ thì mất nhiều câu hơn được, nên giữ"; chưa phải "đã chứng minh tên bài giúp tìm tốt hơn".

## Giới hạn đã biết

- **Bài đặt tên mục nghèo** thì các đoạn của nó mang nhãn kém và khó tìm. Vì vậy mỗi nhóm bài có một mẫu với các mục cố định (bài 7).
- **Đoạn rất ngắn:** tên bài và tên mục chiếm phần lớn chữ để tìm, nên các đoạn của cùng một bài trông giống nhau, khó phân biệt đoạn nào đúng.
- **Không có cách "chỉ tìm trong lễ hội".** Sau này cần lọc thì phải thêm.

## Chi tiết để tra

- Phép so làm ngày 25/10/2026, trên kho của thời điểm đó, lượng chữ 750 token (thời còn đưa 5 đoạn). Giá trị p sau hiệu chỉnh của hai cách: 0,457 và 0,317, tức chưa có ý nghĩa thống kê.
- Trong chữ để tìm, đường tiêu đề giữ nguyên số thứ tự của mục nếu bài có đánh số (như "6. Các dịch vụ…").
- Dòng "Giờ mở cửa, giá vé, lịch lễ hội có thể đã thay đổi…" được thêm khi câu trả lời trích một đoạn có trường nguồn thuộc nhóm vé, địa điểm, lễ hội, hoặc là bài "Lưu trú ở Huế", hoặc nêu đúng tên một bài như thế có trong nguồn liệt kê, nguồn "gần một điểm" hay thẻ nơi (bài 16, 24).
- Bước tìm kiểm hồ sơ của từng ứng viên (đủ 7 trường, đúng dạng, mã đoạn khớp mã cất trong Qdrant, chủ đề khớp đường dẫn) mỗi lần tìm.

**Bài sau (bài 10):** chữ để tìm của 9.536 đoạn được đổi thành vector như thế nào.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Chữ để tìm = tên bài + đường tiêu đề + phần bằng chứng: `backend/ingestion/chunking/full_corpus_chunker.py`, hàm `build_representation_a_search_text` [code].
- Hồ sơ 7 trường (đọc lại khi tìm: `search_text`, `source`, `title`, `heading_path`, `evidence_parts`, `chunk_id`, `domain`): `backend/retrieval/full_corpus.py`, hàm `search` (danh sách `with_payload`) [code, đọc 22/11/2026]; `backend/core/schema.py` hàm `to_qdrant_payload` qua `bai_hoc/03_METADATA.md` [chép].
- Khối "[Nguồn n] / Tiêu đề / Mục / Bằng chứng", đoạn số 3 và số 4 của ví dụ chính, câu trả lời trích [4] cho giá vé trẻ em: `data/hoc_cung_D/vi_du_di_suot_vet.json`, trường `ngu_canh`, `tra_loi` [đã chạy, riêng tư]; hàm dựng khối: `backend/retrieval/full_corpus_context.py`.
- 10 đoạn của ví dụ chính thuộc hai bài vé và một bài nghệ thuật biểu diễn: cùng file, trường `tim_kho`.
- Bỏ chủ đề con / thẻ phân loại; không lọc theo trường: `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` thẻ N2-16 qua `bai_hoc/03_METADATA.md` [tài liệu]. Lý do "câu hỏi chạm nhiều chủ đề" là lập luận thiết kế, chưa có phép đo.
- Phép so 4 / 21 / 7 và 3 / 21 / 8, p 0,457 và 0,317: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g3_implementation.md` mục 3.5 qua `bai_hoc/03_METADATA.md` [đã chạy 25/10].
- Bảy thư mục nguồn của kho, 5 chủ đề: `backend/config/settings.yaml` (`include_globs`) [cấu hình].
- Điều kiện thêm dòng "có thể đã thay đổi": `backend/llm/assistant.py`, `NOTICE_SOURCE_PREFIXES`, hàm `set_notice` [code].
- Mục "Quyết định và lý do", "Nếu… thì sao", "Câu hỏi tự kiểm" (thêm 13:46 22/11/2026 theo khuôn mới; gom từ "Đã so", bảng cấu hình, mục "Vì sao không làm cách khác" cũ). Hồ sơ 5 ⇒ 7 trường (29–30/09), chủ đề con / thẻ / lọc "bị loại vì chưa có ai dùng", không có chỉ mục phụ: `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` thẻ N2-16 [quyết định đã ghi, không có số chất lượng]. Lý do của dạng khối "Tiêu đề / Mục / Bằng chứng": người viết dò chú thích trong `backend/retrieval/full_corpus_context.py`, không thấy. Lý do "không tốn model, không rủi ro viết sai" ở quyết định 5 là lập luận, giữ từ bài cũ. Bảy thư mục được đưa vào kho: `include_globs` của `backend/config/settings.yaml` [cấu hình]. Kiểm hồ sơ từng ứng viên lúc tìm, lỗi ⇒ lời báo tra cứu không khả dụng: `backend/retrieval/full_corpus.py` (`validate_point_payload`), `backend/api/routes/chat.py` (`RETRIEVAL_UNAVAILABLE_MESSAGE`) [code, chưa thử]. Mã đoạn theo đường dẫn: `backend/ingestion/chunking/full_corpus_chunker.py` (chú thích `chunk_id`) [code]. Dòng "tên mục chung chung" là ví dụ tự đặt.
- Các mục mới đã qua một lượt đối chiếu độc lập (một agent khác chỉ đọc, 22/11/2026), các dòng sai / lệch đã sửa lúc 14:17: `data/hoc_cung_D/kiem/muc_moi_02_07_11_va_phu_luc.md` [riêng tư]. Nguyên tắc "chỉ thêm trường khi có chỗ dùng" chốt 11/09: `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md` (Decision Queue #3) [quyết định đã ghi]. Bảng điểm trang Lên kế hoạch: `backend/llm/lich_trinh_v2.py` (`kiem_doan_mo_ta`) [code].

- Dòng "có thể đã thay đổi" cũng hiện khi bài chỉ được nêu tên qua nguồn liệt kê, "gần một điểm" hay thẻ nơi (thêm 22:43 22/11/2026): `backend/llm/assistant.py` hàm `set_notice` (`bai_neu`) [code].
- Quét số cũ 20:46 23/11/2026: bốn câu nói số kho hiện tại (267 ⇒ 269 bài, 9.479 ⇒ 9.533 đoạn); dòng Cập nhật cũ ghi "số kho khớp bản ghi hiện trạng lúc 13:33" (22/11) nay thuộc bản 22:43 22/11. Lệnh: `corpus.file_count` / `corpus.chunk_count` của `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` (269 / 9533), đọc 20:40 23/11/2026 [đã chạy].

</details>
