# Bài 1 — Cuốn sổ tay: kho dữ liệu

*Cập nhật lần cuối: 19:45, ngày 14/11/2026 · thêm ghi chú: ngày 14/11 kho có thêm 43 bài qua năm lần ghi, nay 247 bài (bài 22); số 204 trong bài là lúc viết 11/11.*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Kho (cuốn sổ tay) | **knowledge base** / **corpus** (thư mục `knowledge-base-hue/`) | 204 bài viết về Huế. |
| File Markdown — **mới** | **Markdown** (đuôi `.md`) | File chữ thường; tiêu đề đánh dấu bằng `#`, `##`; bảng và danh sách viết bằng ký hiệu đơn giản. |
| Mẫu bài — **mới** | **template** (vd `foods-template.md`) | Khung các mục mà mọi bài cùng chủ đề phải theo. |
| Phiếu chuẩn bị — **mới** | **build record** | Tờ ghi lại lần chuẩn bị kho: gồm những file nào, "dấu" của từng file, bao nhiêu đoạn. |
| Dấu của file — **mới** | **hash** (sha256) | Một chuỗi ký tự tính từ nội dung file; sửa một chữ là dấu đổi. |
| Đóng khi lệch | **freshness check** (trong code: `verify_full_corpus_record_freshness`) | Lúc khởi động, chatbot so dấu trong phiếu với kho hiện tại; lệch thì không chạy. |

---

*Bài 0 nói chatbot giống người hướng dẫn viên tra sổ tay. Bài này mở chính cuốn sổ ra xem: trong đó có gì, được soạn ra sao, và được giữ đúng thế nào.*

## Quay lại người hướng dẫn viên

Cuốn sổ của người hướng dẫn viên không phải sách mua sẵn. Họ **tự soạn**, mỗi trang một chủ đề, trang nào cũng theo cùng một khung: món ăn thì ghi món là gì,
ăn ở đâu, giá bao nhiêu, mở mấy giờ; di tích thì ghi lịch sử, vé, giờ mở cửa. Cuối trang ghi thông tin lấy từ đâu. Khi phát hiện một dòng đã cũ, họ sửa lại cho
đúng, chứ không để nguyên rồi nhớ trong đầu.

Kho của hue_rag chính là cuốn sổ đó.

## Kho gồm những gì

Kho có **204 bài viết tiếng Việt** (lúc viết bài này, 11/11; ngày 14/11 thêm 43 bài nữa thành **247**, xem bài 22), mỗi bài là **một file Markdown**, chia làm năm thư mục theo chủ đề:

| Chủ đề (thư mục) | Số bài | Gồm |
|---|---:|---|
| Món ăn (`foods`) | 91 | đặc sản Huế, quán ăn, nhà hàng, quán cà phê, một bài hướng dẫn chung |
| Di tích (`heritages`) | 29 | Đại Nội, Kinh thành, các lăng, chùa, đàn tế, di sản như Nhã nhạc, Mộc bản |
| Lễ hội (`festivals`) | 27 | lễ hội, ngày hội, lễ tế trong năm |
| Nghệ thuật biểu diễn (`performing_arts`) | 12 | ca Huế, các chương trình biểu diễn, đêm nhạc |
| Du lịch (`travel`) | 45 | địa điểm (biển, đầm phá, chợ, phố đi bộ, đèo), lịch trình mẫu, chi phí, vé |

Ngoài 204 bài này, chatbot **không biết gì khác**. Có ba ngoại lệ, và cả ba đều được ghi rõ khi hiện ra:
- ngày tháng, ngày âm lịch: code tính;
- dự báo thời tiết: code lấy từ một dịch vụ thời tiết;
- mục **"Từ web (chưa kiểm)"**: chỉ xuất hiện khi kho không có, tách riêng khỏi phần trả lời từ kho.

## Một bài trong kho trông thế nào

Mỗi chủ đề có một **mẫu bài**. Mọi bài cùng chủ đề đều theo cùng các mục. Ví dụ bài về một món ăn luôn có mô tả món, nơi ăn, giá, giờ mở cửa. Một vài luật viết
áp cho mọi bài:

- file **bắt đầu bằng tiêu đề** `# Tên bài`, rồi chia mục bằng `##`, `###`;
- **không có mục rỗng**: thông tin nào không có thì bỏ hẳn mục đó, không ghi "đang cập nhật";
- câu văn tự nhiên, viết cho người đọc, **đọc riêng một bài vẫn hiểu**;
- cuối bài có mục **"Nguồn dữ liệu"** ghi thông tin lấy từ đâu. Nguồn là các trang công khai: cổng thông tin của tỉnh, báo, trang du lịch, văn bản pháp luật.
  Tổng cộng khoảng 76 trang web khác nhau.

Vì kho đã là chữ sạch, chia mục rõ ràng, chatbot **đọc thẳng các file Markdown**. Nó không cần bước rút chữ từ PDF hay Word (loader).

Ngoài 204 bài, thư mục kho còn ba loại file **không** đưa vào chatbot: 3 file danh mục dùng lúc soạn (chỉ là danh sách tên), thư mục `meta/` (mẫu bài, sao lưu, ghi chú soạn), thư mục
`_source-dumps/` (bản thô tải từ trang nguồn) và thư mục `evaluation/` (bộ câu hỏi chấm). Danh sách file bị loại được ghi trong cấu hình, không để máy tự đoán.

## Vì sao phải tự soạn kho

Trên mạng, cùng một quán có thể có ba giờ mở cửa khác nhau, lẫn quảng cáo và bài cũ nhiều năm. Nếu chatbot đọc thẳng như vậy mỗi lần có câu hỏi, không ai biết
trước nó sẽ nói gì. Soạn kho một lần thì kiểm được trước: bài nào nói gì, lấy từ đâu, chỗ nào mâu thuẫn. Từ đó có luật chính của hue_rag: **chatbot chỉ nói
điều kho có** (gọi là trả lời *closed-world*, "trong phạm vi đóng").

Cái giá phải trả là soạn kho tốn công, và kho phải được giữ đúng theo thời gian. Bù lại, câu trả lời tốt tới đâu thì trước hết phụ thuộc vào thứ mình kiểm soát
được.

## Vì sao mỗi câu phải "đọc riêng vẫn hiểu"

Khi trả lời, người viết **không đọc cả bài**. Nó chỉ đọc 10 đoạn nhỏ, thường cắt ra từ nhiều bài khác nhau. Nếu một đoạn viết "Quán này mở từ 6 giờ sáng" mà
không nói quán nào, người viết không biết "quán này" là quán nào, và có thể gán nhầm sang quán khác.

Vì vậy kho được viết sao cho **từng câu, từng dòng mang đủ tên và bối cảnh của nó**. Ở bước chuẩn bị còn có hai cách giữ bối cảnh cho từng đoạn. Một là dòng
tiêu đề bảng đi kèm mỗi dòng giá (bài 2). Hai là tên bài và đường tiêu đề đi kèm mỗi đoạn (bài 3). Thêm nữa, có 3 quy tắc gắn sẵn: ví dụ câu lưu ý chung ở
đầu một bài vé được gắn kèm vào từng đoạn giá của bài đó, để đoạn giá nào được tìm ra cũng mang theo lưu ý.

## Kho được giữ đúng như thế nào

**Rà toàn kho.** Ngày 25/10, nhiều agent đọc mọi dòng có con số hoặc mốc thời gian trong kho và lập danh sách **139 điểm đáng ngờ**: hai bài nói khác nhau,
hoặc thông tin có thể đã cũ.

**Sửa có luật.** Ví dụ lớn nhất: từ 01/07/2025, Huế sắp xếp lại phường xã, nên nhiều tên phường trong kho thành sai. Luật sửa:
- chỉ sửa khi có căn cứ: ngay trong kho, hoặc trong nguồn ngoài anh cho phép tra (đọc nguyên văn, một agent khác đọc lại cho khớp);
- tên mới đứng trước, **tên cũ để trong ngoặc** để người dùng quen tên cũ vẫn nhận ra;
- chỗ nào không chắc thì **viết nhẹ đi** (bỏ con số không chắc) chứ không đoán; không thêm khẳng định mới, không xoá câu cảnh báo.

**Sửa bằng máy, có sao lưu.** Kho không nằm trên GitHub vì là dữ liệu riêng, nên không có lịch sử phiên bản tự động. Vì vậy trước khi sửa, bài gốc được sao lưu.
Máy chỉ thay một câu khi câu cũ xuất hiện **đúng một lần** trong bài, để không sửa nhầm chỗ khác. Sau đó một agent khác đối chiếu từng chỗ với bản sao lưu.

**Chấm lại sau khi sửa.** Trước khi sửa, ghi sẵn mức tối thiểu "không làm hỏng": không thêm câu ngoài kho bị trả lời, không thêm lỗi an toàn (vé, giờ, cảnh
báo). Sửa xong thì chấm lại trên bộ câu hỏi mẫu và bộ 32 câu an toàn.

**Sửa kho mà quên chuẩn bị lại thì chatbot không chạy.** Mỗi lần chuẩn bị (bài 5), máy ghi một **phiếu chuẩn bị**. Phiếu ghi danh sách file, **dấu** của từng
file và số đoạn. Lúc khởi động, chatbot so phiếu với kho hiện tại: dấu khác, thiếu file hay thừa file đều làm nó **không nhận câu hỏi** cho tới khi chuẩn bị
lại. Giống thủ thư không cho mượn sách khi mục lục chưa cập nhật: thà đóng cửa còn hơn đưa sai sách.

## Một chuyện thật: kho đúng hơn mà điểm không tăng

Cuối tháng 10 có hai đợt sửa, tổng cộng khoảng 250 chỗ (đợt đầu chạm 65 bài, đợt sau 40 bài), chủ yếu là tên phường mới và vài con số mâu thuẫn giữa hai bài.
Chấm lại trên bộ câu hỏi mẫu, điểm **gần như không đổi**: "đủ ý" chênh chưa tới 0,01 trên thang 5, "đúng" giữ nguyên.

Thoạt nghe thì như phí công, nhưng đó lại đúng là kết quả mong muốn:
- **mục tiêu của đợt sửa là "đúng hơn mà không làm hỏng"**, không phải tăng điểm. Mức tối thiểu ghi trước là không câu nào bị hỏng thêm, và mức đó đạt ở cả
  hai đợt;
- điểm không tăng vì chỉ khoảng **1/6** câu hỏi mẫu chạm vào chỗ sửa, và đáp án mẫu hầu như không hỏi đúng tên phường.

Điều rút ra: **điểm chấm chỉ nhìn thấy những gì bộ câu hỏi mẫu có hỏi.** Sửa kho cho đúng vẫn cần làm, kể cả khi điểm không phản ánh.

Có một lần sửa làm thêm thông tin: ngày 05/11, 11 bài điểm tham quan của Quần thể Cố đô được thêm một dòng giờ mở cửa chung, kèm "có thể thay đổi theo mùa".
Lý do: câu "mấy giờ mở cửa" hay bị hỏi mà kho thiếu. Giờ lấy từ bài vé đã có trong kho, không lấy từ ngoài.

## Tốt tới đâu, khi nào hỏng

Kho đủ cho phần lớn câu khách hay hỏi: ăn gì, đi đâu, vé, lễ hội. Có bốn chỗ hỏng cần biết:

- **Kho thiếu thật.** Đếm trên 15 câu "về Huế mà kho không có", các chỗ thiếu là: khách sạn, nhà nghỉ; ăn uống theo nhu cầu rất cụ thể; giờ, vé, giá của chợ
  hay chùa ngoài Quần thể Cố đô; lễ hội đúng một ngày cụ thể. Khi đó chatbot nói "không đủ thông tin", rồi tra web một lần và hiện riêng mục **"Từ web (chưa
  kiểm)"** (bài 15).
- **Kho cũ dần.** Giá và giờ thay đổi theo thời gian. Câu trả lời trích bài vé, điểm tham quan và lễ hội luôn kèm dòng "thông tin có thể đã thay đổi".
- **Kho tự mâu thuẫn ở vài chỗ còn sót.** Có vài điểm vẫn "chờ tra ngoài", tức là bài đã tự ghi là chưa chắc.
- **Kho có mà tìm không ra.** Đây không phải lỗi của kho mà của bước tìm. Đó lại là lỗi hay gặp nhất (bài 6).

## Ba điều chính

1. Kho là **204 bài Markdown tự soạn theo mẫu**, chia năm chủ đề, có nguồn ở cuối bài. Chatbot đọc thẳng file, **chỉ nói điều kho có**.
2. Mỗi câu trong kho phải **đọc riêng vẫn hiểu**, vì người viết chỉ đọc vài đoạn nhỏ chứ không đọc cả bài.
3. Kho được **sửa có luật** (có căn cứ, tên cũ trong ngoặc, viết nhẹ chỗ không chắc, sao lưu, chấm lại), và **phiếu chuẩn bị** chặn chatbot chạy trên kho đã
   lệch.

**Bài sau:** Bài 2 — Cắt sổ thành thẻ ghi chú (chunking): bài được cắt thành đoạn thế nào, vì sao cắt theo cấu trúc bài, và vì sao đoạn to hơn lại tệ hơn.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Số bài theo chủ đề: đếm file trong `knowledge-base-hue/<chủ đề>/` ngày 11/11, đã trừ 3 file danh mục [đã chạy]
- File bị loại: `backend/config/settings.yaml` (`exclude_files`, `exclude_parts`) [code]
- Luật viết bài (bắt đầu bằng `#`, không mục rỗng, "Nguồn dữ liệu"): `session_prompt/Session_Prompt.md` §5; mẫu bài `knowledge-base-hue/meta/*-template.md` (riêng tư) [code / tài liệu]
- Khoảng 76 trang nguồn; 139 điểm đáng ngờ (25/10); hai đợt sửa 28/10 và 30/10 (123 + 123 chỗ; Đủ ý −0,008 / +0,008, Đúng không đổi; ~1/6 câu chạm chỗ sửa); giờ mở cửa 05/11 (11 bài); 15 câu "về Huế mà kho không có": `bao_cao_he_thong/02_BAO_CAO_KHO_DU_LIEU.md` [đã chạy]
- 3 quy tắc gắn lưu ý: `knowledge-base-hue/meta/full_corpus_conditions.json` (riêng tư), dùng trong `backend/ingestion/chunking/full_corpus_chunker.py` [code, theo sổ ghi việc 03]
- Phiếu chuẩn bị: `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json`; kiểm lúc khởi động: `backend/retrieval/full_corpus.py` hàm `verify_full_corpus_record_freshness` (kiểm trạng thái, schema, tên collection, cấu hình Qdrant và danh sách + dấu file kho) [code]
- "Quán này mở từ 6 giờ sáng" là ví dụ tự đặt.

</details>
