# Bài 1 — Dữ liệu vào: vì sao không cần loader

*Cập nhật lần cuối: 09:40, ngày 11/11/2026 · viết lại theo xương sống mới (bám sơ đồ RAG anh đã biết).*

## Bảng từ — tên mình dùng và tên gốc

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Kho (sổ tay) | *knowledge base* / *corpus* | 204 bài viết về Huế (đã gặp ở bài 0). |
| Bộ rút chữ | *loader* | Bước đọc PDF, Word, trang web… để lấy ra chữ (anh đã biết). |
| File Markdown | *Markdown* (*.md*) — **mới** | File chữ thường, tiêu đề đánh dấu bằng dấu `#`. Mỗi bài trong kho là một file như vậy. |
| Bản chuẩn bị để tìm | *index*, cất trong *Qdrant* | Các đoạn đã có embedding, sẵn sàng để tìm (bài 5 kể kỹ). |

---

*Ở bài 0, giai đoạn 1 bắt đầu bằng "204 bài Markdown tự soạn (không loader)". Bài này giải thích vì sao.*

## Bản cơ bản làm gì, hue_rag làm gì

Trong bản RAG cơ bản anh đã học, dữ liệu vào là **file người dùng đưa**: PDF, Word, trang web. Loader rút chữ ra. Đây là chỗ hay hỏng âm thầm: bảng bị vỡ
thành chữ rời, đầu trang lẫn vào giữa đoạn, hai cột chữ bị đọc trộn.

hue_rag **không có bước đó**. Kho là **204 bài viết tiếng Việt đã được soạn sẵn** thành file Markdown, chia làm năm phần: món ăn (91 bài), di tích (29), lễ hội
(27), nghệ thuật biểu diễn (12) và du lịch (45). Mỗi chủ đề có một **mẫu bài riêng**. Ví dụ bài món ăn luôn có mô tả món, ăn ở đâu, giá, giờ mở cửa. Cuối bài
ghi thông tin lấy từ đâu, phần lớn là trang của tỉnh, báo và trang du lịch.

## Vì sao tự soạn kho mà không để chatbot đọc thẳng trên mạng

Trên mạng, cùng một quán có thể có ba giờ mở cửa khác nhau, lẫn quảng cáo và bài cũ nhiều năm. Nếu chatbot đọc thẳng như vậy, không ai biết trước nó sẽ nói
gì. Soạn kho một lần thì kiểm được trước: bài nào nói gì, lấy từ đâu, chỗ nào mâu thuẫn. Từ đó có luật chính của hue_rag: **chatbot chỉ nói điều kho có**. Ngoài
kho chỉ có ba thứ, đều ghi rõ: ngày tháng và thời tiết do code tính hoặc lấy về, và mục "Từ web (chưa kiểm)" tách riêng khi kho không có.

Cái giá phải trả: soạn kho tốn công, và kho phải được giữ đúng theo thời gian. Bù lại, câu trả lời tốt tới đâu thì trước hết phụ thuộc vào thứ mình kiểm soát
được.

## Vì sao mỗi câu trong kho phải "đọc riêng vẫn hiểu"

Đây là điều dễ bỏ qua nhất. Khi trả lời, người viết **không đọc cả bài**. Nó chỉ đọc 10 đoạn nhỏ cắt ra từ nhiều bài khác nhau. Nếu một đoạn viết "Quán này
mở từ 6 giờ sáng" mà không nói quán nào, người viết không biết "quán này" là quán nào. Vì vậy các bài được viết sao cho từng câu, từng dòng mang đủ tên và bối
cảnh của nó. Bài 2 (chunking) và bài 3 (metadata) sẽ kể thêm hai cách hue_rag giữ bối cảnh cho từng đoạn.

## Kho được giữ đúng như thế nào

- **Sửa có kiểm.** Ví dụ: từ tháng 7/2025, Huế sắp xếp lại phường xã, nên nhiều tên phường trong kho thành sai. Kho đã được rà và sửa theo tên mới, tên cũ để
  trong ngoặc. Chỗ nào không chắc thì **viết nhẹ đi** (bỏ con số không chắc) chứ không đoán. Trước khi sửa thì sao lưu bài gốc, sửa xong thì chấm lại.
- **Sửa kho mà quên chuẩn bị lại thì chatbot không chạy.** Mỗi lần chuẩn bị bản để tìm, máy ghi lại "dấu" của từng bài. Lúc khởi động, chatbot so dấu đó với
  kho hiện tại. Lệch là nó từ chối chạy, để không trả lời bằng thông tin cũ. Giống thủ thư không cho mượn sách khi mục lục chưa cập nhật.

## Một chuyện thật: kho đúng hơn mà điểm không tăng

Cuối tháng 10, hai đợt sửa kho đã sửa khoảng 250 chỗ (đợt đầu chạm 65 bài, đợt sau 40 bài), chủ yếu là tên phường mới và vài con số mâu thuẫn giữa hai bài. Chấm lại trên bộ câu
hỏi mẫu, điểm **gần như không đổi** (chênh chưa tới 0,01 trên thang 5). Thoạt nghe thì như phí công, nhưng đó lại đúng là kết quả mong muốn:
- **Mục tiêu của đợt sửa là "đúng hơn mà không làm hỏng"**, không phải tăng điểm. Mốc tối thiểu ghi trước khi sửa là không câu nào bị hỏng thêm, và mốc đó đạt.
- Điểm không tăng vì chỉ khoảng 1/6 câu hỏi mẫu chạm vào chỗ sửa, và đáp án mẫu hầu như không hỏi đúng tên phường.

Điều rút ra: điểm chấm chỉ nhìn thấy những gì bộ câu hỏi mẫu có hỏi. Sửa kho cho đúng vẫn cần làm, kể cả khi điểm không phản ánh.

## Tốt tới đâu, khi nào hỏng

Kho đủ cho phần lớn câu khách hay hỏi: ăn gì, đi đâu, vé, lễ hội. Có ba chỗ hỏng cần biết:

- **Kho thiếu thật.** Ví dụ khách sạn, nhà nghỉ; giờ và giá của chợ hay chùa ngoài khu di tích; lễ hội đúng một ngày cụ thể. Khi đó chatbot nói "không đủ
  thông tin", rồi tra web một lần và hiện riêng mục **"Từ web (chưa kiểm)"**.
- **Kho cũ dần.** Giá và giờ thay đổi theo thời gian. Câu trả lời về vé, điểm tham quan và lễ hội luôn kèm dòng "thông tin có thể đã thay đổi".
- **Kho có mà tìm không ra.** Đây không phải lỗi của kho mà của bước tìm. Đó lại là lỗi hay gặp nhất (bài 6).

## Ba điều chính

1. hue_rag **bỏ bước loader** vì kho là 204 bài Markdown tự soạn theo mẫu. Đổi công soạn lấy kho sạch và kiểm được.
2. **Chatbot chỉ nói điều kho có**, và mỗi câu trong kho phải **đọc riêng vẫn hiểu**, vì người viết chỉ đọc vài đoạn nhỏ.
3. Sửa kho để **đúng hơn mà không làm hỏng**. Điểm có thể không tăng, vì điểm chỉ nhìn thấy những gì bộ câu hỏi mẫu có hỏi.

## Bài sau

**Bài 2 — Chunking:** bài được cắt thành đoạn thế nào, vì sao cắt theo cấu trúc bài, và vì sao đoạn to hơn lại tệ hơn.

<details>
<summary>Nguồn (anh không cần đọc)</summary>

- Số bài theo chủ đề: đếm file trong kho ngày 11/11, đã trừ 3 file danh mục dùng lúc soạn [đã chạy]
- Mẫu bài theo chủ đề: `knowledge-base-hue/meta/*-template.md` (riêng tư) [đã xem tên file]
- Chatbot không chạy khi kho lệch: `backend/retrieval/full_corpus.py` hàm `verify_full_corpus_record_freshness` [code]
- Hai đợt sửa kho 28/10 và 30/10 (123 + 123 chỗ, 65 + 40 bài; Đủ ý −0,008 / +0,008, Đúng không đổi; khoảng 1/6 câu chạm chỗ sửa): `bao_cao_he_thong/02_BAO_CAO_KHO_DU_LIEU.md` [đã chạy]
- Những chỗ kho thiếu thật: đếm trên 15 câu "về Huế mà kho không có" của bộ đo tra web, theo sổ ghi việc 02 [đã chạy]
- "Quán này mở từ 6 giờ sáng" là ví dụ tự đặt.

</details>
