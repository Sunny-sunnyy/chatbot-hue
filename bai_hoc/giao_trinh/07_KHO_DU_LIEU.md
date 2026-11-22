# Bài 7 — Kho dữ liệu: 266 bài viết về Huế, ai soạn, lấy từ đâu, kiểm thế nào

*Cập nhật 10:21, ngày 22/11/2026 · số bài đếm từ bản ghi chỉ mục sáng 22/11; các số đo lấy từ báo cáo của những lần sửa và bổ sung kho từ 25/10 tới 22/11; người viết không chạy lại phép đo nào.*

**Bài trước đã biết:** hệ thống gồm những khối nào, và một câu hỏi đi qua chúng ra sao. Mọi câu trả lời chỉ được lấy từ kho.
**Bài này thêm:** mở chính kho ra xem. Trong đó có gì, bài được viết theo luật nào, và kho được giữ đúng bằng cách nào.

## Ý chính

- Kho là **266 bài viết tiếng Việt**, mỗi bài một file chữ có tiêu đề và các mục, chia theo 5 chủ đề: món ăn, di tích, lễ hội, nghệ thuật biểu diễn, du lịch.
- Bài được **soạn riêng cho hệ thống**, theo mẫu, từ các nguồn công khai; phần lớn bài ghi nguồn ở cuối bài. Câu trả lời từ kho không đọc trang web; chỉ khi kho từ chối, hệ thống mới tra web một lần và để riêng.
- Bài phải viết sao cho **từng câu đọc riêng vẫn hiểu**, vì model viết chỉ đọc vài đoạn nhỏ, không đọc cả bài.
- Mỗi lần thêm bài mới hoặc sửa nhiều là một lần **đo trước và sau** trên cùng bộ câu hỏi, với điều kiện ghi sẵn: câu đang trả lời tốt không được tệ đi. Sửa nhỏ thì hỏi thử các câu chạm chỗ sửa.
- Chất lượng câu trả lời có trần là kho. Kho thiếu thì hệ thống từ chối; kho cũ thì hệ thống trả lời cũ.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| kho | **knowledge base**, **corpus** | tập 266 bài viết; thứ duy nhất phần hỏi đáp được trả lời từ đó |
| file Markdown | **Markdown** | file chữ thường, tiêu đề đánh dấu bằng `#`, bảng và danh sách viết bằng ký hiệu đơn giản |
| mẫu bài | **template** | khung các mục mà mọi bài cùng chủ đề phải theo |
| trả lời trong phạm vi kho | **closed-world**, **grounded answering** | chỉ nói điều kho có; kho không có thì từ chối |

## Kho có 266 bài, chia theo 5 chủ đề

| Chủ đề | Số bài | Gồm |
|---|---:|---|
| Món ăn | 111 | đặc sản, quán ăn, nhà hàng, quán cà phê |
| Di tích | 39 | Đại Nội, Kinh thành, các lăng, chùa, di sản như Nhã nhạc |
| Lễ hội | 40 | lễ hội, ngày hội, lễ tế trong năm |
| Nghệ thuật biểu diễn | 15 | ca Huế, các chương trình biểu diễn |
| Du lịch | 61 | 45 bài địa điểm (biển, đầm phá, chợ, phố đi bộ…), 11 bài dịch vụ (đi lại, lưu trú…), 5 bài vé |

Cả kho cắt ra thành 9.458 đoạn (bài 8).

Phần hỏi đáp không biết gì ngoài 266 bài này. Có bốn thứ không lấy từ kho, và đều được ghi rõ khi hiện ra: ngày tháng và ngày âm lịch (chương trình tính), dự báo thời tiết (lấy từ một dịch vụ thời tiết), khoảng cách và "gần một điểm có gì" (chương trình tính từ một bảng vị trí riêng), và mục "Từ web (chưa kiểm)" (chỉ có khi kho từ chối). Trang Lên kế hoạch dùng thêm vài bảng dữ liệu riêng: bảng điểm tham quan, bảng chỗ ở, bảng quán ăn (chặng 6).

## Bài được soạn riêng, theo mẫu, có ghi nguồn

Kho không phải bản sao của các trang web. Mỗi bài được viết lại từ các nguồn công khai (cổng thông tin của địa phương, báo, trang du lịch, văn bản quy định giá) theo một **mẫu bài** của chủ đề đó. Ví dụ bài về một món ăn luôn có: món là gì, ăn ở đâu, giá, giờ mở cửa. Vài luật viết áp cho mọi bài:

- bài bắt đầu bằng tên bài, rồi chia mục;
- **không có mục rỗng:** thông tin nào không có thì bỏ hẳn mục đó, không ghi "đang cập nhật";
- cuối bài có mục **"Nguồn dữ liệu"** ghi thông tin lấy từ đâu (phần lớn bài có mục này; một số bài chưa có).

Vì bài đã là chữ sạch có cấu trúc, hệ thống đọc thẳng các file này. Nó không cần bước rút chữ từ PDF hay từ trang web.

Lý do soạn riêng: trên mạng, cùng một quán có thể có ba giờ mở cửa khác nhau, lẫn quảng cáo và bài cũ nhiều năm. Nếu hệ thống đọc thẳng những trang đó mỗi lần có câu hỏi, không ai biết trước nó sẽ nói gì. Soạn một lần thì kiểm được trước: bài nào nói gì, lấy từ đâu, chỗ nào mâu thuẫn. Cái giá là công soạn, và kho phải được giữ đúng theo thời gian.

## Mỗi câu trong bài phải đọc riêng vẫn hiểu

Lúc trả lời, model viết không đọc cả bài. Nó đọc các đoạn nhỏ (10 đoạn ở lần tìm đầu), thường cắt từ nhiều bài khác nhau. Nếu một đoạn viết "Quán này mở từ 6 giờ sáng" mà không nói quán nào, model không biết "quán này" là quán nào, và có thể gán nhầm sang quán khác.

Vì vậy bài được viết sao cho từng câu, từng dòng mang đủ tên và bối cảnh của nó. Ở ví dụ chính, đoạn số 1 ghi giá vé vào cổng Đại Nội, 200.000 đồng cho người lớn, trong cùng một câu: con số đứng cạnh tên nơi và loại vé. Bước chuẩn bị còn hai cách giữ bối cảnh nữa: dòng tiêu đề bảng đi kèm mỗi dòng giá (bài 8), và tên bài cùng tên mục đi kèm mỗi đoạn (bài 9).

## Mỗi lần thêm hay sửa kho là một lần đo trước và sau

Kho đã đổi nhiều lần. Cách làm chung:

1. **Có căn cứ.** Sửa khi có căn cứ ngay trong kho hoặc ở nguồn công khai; chỗ không chắc thì viết nhẹ đi chứ không đoán. Từ 22/11 có thêm một luật cho con số: chỉ đổi khi một nguồn đáng tin nói rõ; các nguồn nói khác nhau, hoặc không nguồn nào nói, thì giữ nguyên.
2. **Ghi trước điều kiện "không làm hỏng".** Ví dụ: không thêm câu ngoài kho nào bị trả lời, không thêm lỗi ở các câu về vé, giờ, cảnh báo an toàn.
3. **Đo trước và sau** trên cùng bộ câu hỏi (chặng 4) khi thêm bài mới hoặc sửa nhiều; sửa nhỏ thì hỏi thử các câu chạm chỗ sửa.
4. **Cập nhật chỉ mục.** Quên bước này thì hệ thống vẫn bật nhưng từ chối mọi câu hỏi (bài 12).

Các lần đổi chính:

| Khi nào | Việc | Kết quả đo |
|---|---|---|
| cuối tháng 10 | rà mọi dòng có con số hoặc mốc thời gian: 139 điểm đáng ngờ; hai đợt sửa, khoảng 250 chỗ (phần lớn là tên phường xã mới sau lần sắp xếp 01/07/2025) | điểm chấm gần như không đổi (điểm "đủ ý" chênh chưa tới 0,01 trên thang 5); điều kiện "không làm hỏng" đạt ở cả hai đợt |
| đầu tháng 11 | thêm một dòng giờ mở cửa cho 11 bài điểm tham quan, lấy từ bài vé đã có trong kho | hỏi thử trả đúng giờ, có nguồn; 1 câu của bộ câu mẫu lần đầu bị từ chối, chạy lại hai lần đều đúng |
| 14–16/11 | thêm 61 bài (204 lên 265): khách sạn, quán ăn, địa điểm, lễ hội, những thứ hệ thống từng từ chối | câu về khách sạn trả lời được 11 trên 12 (trước đó 4); đo bù 65 câu cũ: không câu nào tệ đi |
| 22/11 | sửa hai bài về giá (giá thuê thuyền ghi theo từng nhà thuyền; vé một điểm tham quan cho người địa phương); thêm một bài gom những gì kho đã nói về bậc thang, dốc và đi bộ ở các điểm tham quan (265 lên 266 bài) | chỉ mục cập nhật riêng trong 37,7 giây cho lần sửa giá (bài 12) |

Một điều rút ra từ dòng đầu: kho đúng hơn mà điểm không tăng. Điểm chấm chỉ nhìn thấy những gì bộ câu hỏi có hỏi; chỉ khoảng 1 trên 6 câu của bộ chạm vào chỗ sửa. Sửa kho cho đúng vẫn phải làm, kể cả khi điểm không phản ánh.

## Dễ nhầm

- **"Hệ thống đọc Internet để trả lời."** Không. Nó đọc 266 bài đã soạn. Web chỉ là đường phụ sau khi kho từ chối, và luôn để riêng.
- **"Kho càng nhiều bài thì trả lời càng tốt."** Không hẳn. Thêm bài có thể đẩy đoạn đúng của câu khác ra khỏi 10 đoạn. Vì vậy mỗi lần thêm đều đo lại các câu cũ.
- **"Kho đúng hơn thì điểm tăng."** Không hẳn. Hai đợt sửa khoảng 250 chỗ không làm điểm đổi, vì bộ câu hỏi ít chạm vào chỗ sửa.

## Những điều cần nhớ

- 266 bài, 5 chủ đề (món ăn 111, di tích 39, lễ hội 40, nghệ thuật biểu diễn 15, du lịch 61); soạn theo mẫu, phần lớn có nguồn ở cuối bài.
- Phần hỏi đáp chỉ trả lời từ kho; ngày tháng, thời tiết, khoảng cách và mục web là những thứ ngoài kho, đều ghi rõ.
- Mỗi câu trong bài phải đọc riêng vẫn hiểu, vì model viết chỉ thấy vài đoạn nhỏ.
- Thêm bài hay sửa nhiều: có căn cứ, ghi trước điều kiện "không làm hỏng", đo trước và sau, cập nhật chỉ mục. Sửa nhỏ: có căn cứ, hỏi thử, cập nhật chỉ mục.
- Kho là trần của chất lượng: thiếu thì từ chối, cũ thì trả lời cũ.

## Cấu hình đang chạy

*Chép từ hệ thống đang chạy sáng 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Thư mục kho | `knowledge-base-hue/`, được theo dõi cùng mã của dự án từ 20/11 | mọi lần sửa bài đều có lịch sử và lùi lại được | trước 20/11 thư mục kho nằm cạnh mã nhưng không được theo dõi lịch sử |
| Các thư mục được đưa vào | món ăn · di tích · lễ hội · nghệ thuật biểu diễn · du lịch / địa điểm · du lịch / dịch vụ · du lịch / vé | 7 thư mục, 266 bài | — |
| Thư mục bị loại | bộ câu hỏi chấm · bản thô tải từ trang nguồn · mẫu bài và ghi chú soạn | không phải nội dung cho người dùng | — |
| File bị loại đích danh | 3 file danh mục dùng lúc soạn | chỉ là danh sách tên, không phải nội dung để trả lời | hai file loại từ đầu tháng 9, file thứ ba loại cuối tháng 10; phép đo lúc loại: kết quả tìm không khác |
| Dạng bài | file Markdown, bắt đầu bằng tên bài | đọc thẳng, không cần bước rút chữ | — |
| Quy tắc gắn lưu ý | 3 quy tắc ở 2 bài (bài 8) | câu lưu ý chung của bài đi kèm từng đoạn giá | — |

## Đã so

**Vấn đề thật đã gặp.** Hệ thống từ chối những câu rất thường: hỏi khách sạn, hỏi một cây cầu hay nhà ga nổi tiếng, hỏi một lễ hội chưa có bài. Đếm trên các câu "về Huế mà kho không có" cho thấy kho thiếu thật ở các mảng đó. Câu hỏi: thêm bài thì các câu này có trả lời được không, và các câu đang tốt có bị tệ đi không?

**So gì, trên bộ nào.** Trước và sau mỗi lần ghi thêm bài (sáu lần ngày 14/11, một lần 16/11), model viết là gpt-6-luna. Hai nhóm câu: nhóm câu nhắm vào bài mới, và các câu cũ có 10 đoạn đầu bị đổi vì bài mới (đo bù ngày 15/11 cho ba lần ghi sau).

| Đo gì | Trước | Sau |
|---|---|---|
| Câu về khách sạn trả lời được (chấm mà không biết bản nào) | 4 trên 12 | 11 trên 12 |
| Câu về đi lại trả lời được (người viết báo cáo tự đọc) | 2 trên 6 | 4 trên 6 |
| Bữa ăn trong lịch có quán thuộc kho (chương trình đếm trên 3.840 lịch mô phỏng, không dính model) | 49,3 % | 69,1 % |
| 65 câu cũ có 10 đoạn đầu bị đổi vì bài mới | — | 8 câu ra đúng chữ cũ; 57 câu khác chữ, trong đó 56 câu cùng ý và 1 câu tốt lên (hết bị từ chối) |

**Đọc bảng này thế nào.**
- Thêm bài đúng chỗ thiếu làm các câu từng bị từ chối trả lời được.
- Mỗi lần ghi có điều kiện "không làm hỏng" ghi trước. Lượt 65 câu là đo bù sau khi ghi, để chắc không câu nào tệ đi.
- Dòng "đi lại" do chính người viết báo cáo tự đọc, độ chắc thấp hơn các dòng khác.

**Giới hạn của phép đo.** Bộ câu do nhóm soạn. Các số trên đo với gpt-6-luna, chưa đo lại với model đang chạy.

## Giới hạn đã biết

- **Kho thiếu.** Lượt đo trợ lý ngày 21/11 chỉ ra bốn thứ kho không có: mức phải leo bậc ở các điểm tham quan, đường từ Huế đi Hội An, chỗ đậu ô tô, quy định chụp ảnh ở chùa và lăng. Ví dụ "kho không có" của cả bộ (chỗ đậu ô tô ở chùa Thiên Mụ) thuộc nhóm này. Bài về leo bậc đã vào kho sáng 22/11; ba thứ còn lại chưa có.
- **Kho cũ dần.** Giá và giờ đổi theo thời gian. Câu trả lời trích bài về vé, điểm đến, lễ hội, lưu trú luôn kèm dòng "Giờ mở cửa, giá vé, lịch lễ hội có thể đã thay đổi…". Giá trong kho được coi là tương đối. Phần lớn mức giá không ghi ngày; vài bảng ghi tháng khảo sát, và bài sửa từ 22/11 ghi ngày đối chiếu ở mục nguồn.
- **Kho còn chỗ chưa phân xử được.** Vài con số mà các nguồn nói khác nhau được giữ nguyên và ghi vào một danh sách riêng.
- **Kho có mà tìm không ra.** Đây là lỗi của bước tìm, và là lỗi hay gặp hơn cả (bài 13).

## Vì sao không làm cách khác

**Vì sao không cho hệ thống đọc thẳng các trang web thay vì soạn kho?** Quyết định đã ghi: sản phẩm chỉ trả lời từ kho đã soạn và kiểm. Web chỉ được dùng ở một đường phụ: tra một lần khi kho từ chối, kèm các luật chặn bằng chương trình (bài 25).

**Vì sao không để một agent tự cập nhật giá trong kho theo web?** Quyết định đã ghi: giá trong kho chỉ cần tương đối, chỉ sửa chỗ tự mâu thuẫn hoặc thiếu. Bài mới và việc đổi cấu trúc kho cần chủ dự án duyệt; chỗ kho tự mâu thuẫn hoặc thiếu thì nhóm được tra nguồn rồi sửa và báo lại. Hệ thống có sẵn hai lệnh chạy tay: một lệnh tìm mọi chỗ trong kho còn ghi một mức giá cũ và soạn bản đề xuất, một lệnh duyệt. Chưa lệnh nào được dùng trên kho thật.

**Vì sao không dùng dữ liệu có cấu trúc (bảng giá vé, bảng giờ mở cửa) thay cho bài viết?** Đã đo một lần: một bảng vé và giờ có cấu trúc cho 60 điểm đúng 19 trên 20 câu nhưng không qua được điều kiện về cách model nêu điều kiện đi kèm, và khi chỉ dùng bảng để kiểm số thì không bắt được số sai nào trên 52 câu thật. Bảng bị bỏ.

## Chi tiết để tra

- Số bài theo thư mục, đếm lúc 10:02 ngày 22/11: món ăn 111 · di tích 39 · lễ hội 40 · nghệ thuật biểu diễn 15 · địa điểm 45 · dịch vụ 11 · vé 5. Kho còn được bổ sung nên số có thể lớn hơn khi anh đọc.
- Hai đợt sửa cuối tháng 10: 123 chỗ ở 65 bài, rồi 123 chỗ ở 40 bài.
- Lệnh soạn bản đề xuất khi một giá đổi, thử trên một bản chép của kho với Claude Sonnet 5.5: con số 200.000 có ở 37 chỗ trong 14 bài, chỉ 9 chỗ là vé vào cổng Đại Nội; lệnh chọn đúng 9 chỗ đó, để 1 chỗ cho người xem, bỏ qua 27 chỗ. Chương trình tìm chỗ và thay con số; model chỉ trả lời "con số này có phải mức giá vừa mô tả không"; người duyệt bằng lệnh thứ hai.
- Bảng vé và giờ có cấu trúc (đã bỏ): thêm khoảng 120 dòng chương trình và một bảng phải giữ khớp với kho.
- Khoảng 76 trang web nguồn khác nhau, đếm lúc kho có 204 bài; chưa đếm lại.
- Một phép đếm thô ngày 22/11: khoảng 39 bài không có tiêu đề mục nào mang chữ "Nguồn" (chưa đọc tay từng bài).
- Trong bốn thứ kho thiếu, phần quy định chụp ảnh chưa soạn được nháp vì chưa tìm ra nguồn.

**Bài sau (bài 8):** bước đầu tiên của giai đoạn chuẩn bị: cắt 266 bài thành 9.458 đoạn.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- 266 bài và số bài theo thư mục: đếm từ danh sách file của `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json`, 10:02 22/11/2026 [đã chạy]. Thư mục đưa vào / loại, file loại: `backend/config/settings.yaml` mục `full_corpus.knowledge_base`.
- Luật viết bài, mẫu bài, "đọc riêng vẫn hiểu", lý do soạn riêng, rà 139 điểm, hai đợt sửa (123 + 123 chỗ; 65 và 40 bài; điểm đủ ý ±0,008; khoảng 1 / 6 câu chạm), giờ mở cửa 11 bài, khoảng 76 trang nguồn: `bai_hoc/01_KHO_DU_LIEU.md` và nguồn gốc `bao_cao_he_thong/02_BAO_CAO_KHO_DU_LIEU.md` [đã chạy; chép qua bài 1 cũ].
- Các lần bổ sung 14–16/11 (61 bài; khách sạn 4 ⇒ 11 / 12 chấm mù; đi lại 2 ⇒ 4 / 6 tự đọc; bữa có quán 49,3 ⇒ 69,1 %; 65 câu đo bù: 56 cùng ý, 1 tốt lên): `bai_hoc/22_BO_SUNG_SO_TAY.md` mục "Ba điều chính" và mục Nguồn [đã chạy].
- Sửa hai bài giá ngày 22/11, luật "có nguồn đáng tin nói rõ mới sửa", danh sách "chưa phân xử được": `session_prompt/HIEN_TRANG.md` mục 4, gạch 08:40 22/11/2026; `session_prompt/VIEC_DANG_MO.md` khối A; lần cập nhật 37,7 giây: `bai_hoc/VIEC_MOI_XONG.md` mục 32.
- Giá trong kho chỉ cần tương đối; hai lệnh đề xuất + duyệt, ca 37 chỗ / 9 chỗ, chưa dùng trên kho thật: `bai_hoc/VIEC_MOI_XONG.md` mục 30 [đã chạy trên bản chép].
- Kho nằm trong kho mã từ 20/11: `AGENTS.md` luật cứng 2.
- Bốn thứ kho thiếu; bài bổ sung đang soạn nháp: `session_prompt/HIEN_TRANG.md` mục 3 và mục 4 (gạch 22:06 21/11/2026).
- Bảng vé và giờ có cấu trúc (19 / 20; 52 câu; khoảng 120 dòng): `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 31.
- Đoạn số 1 của ví dụ chính: `data/hoc_cung_D/vi_du_di_suot_vet.json`.
- "Quán này mở từ 6 giờ sáng" là ví dụ tự đặt.

</details>
