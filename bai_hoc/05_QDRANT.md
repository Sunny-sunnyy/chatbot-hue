# Bài 5 — Cất hộp thẻ vào tủ: Qdrant

*Cập nhật lần cuối: 10:19, ngày 11/11/2026 · bài mới.*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Tủ thẻ | **Qdrant** (vector database) | Phần mềm cất các đoạn cùng vector và từ khoá, tìm rất nhanh. |
| Ngăn tủ — **mới** | **collection** (`hue_full_corpus_7a2_e5_small_384`) | Một bộ dữ liệu trong Qdrant. Chatbot dùng đúng một ngăn. |
| Thẻ trong tủ — **mới** | **point** | Một đoạn khi đã cất vào Qdrant: mã + vector nghĩa + vector từ khoá + hồ sơ 7 trường. |
| Phiếu chuẩn bị | **build record** (schema `full_corpus_build:v3`) | Tờ ghi lại lần chuẩn bị (đã gặp ở bài 1). |
| Kiểm lúc mở cửa — **mới** | **freshness check** + kiểm schema lúc khởi động | Chuỗi kiểm chạy mỗi lần chatbot khởi động, trước khi nhận câu hỏi đầu tiên. |
| Hộp đóng gói — **mới** | **Docker** (container) | Cách chạy Qdrant như một khối đóng gói sẵn, cùng phiên bản trên mọi máy. |
| Mã lỗi — **mới** | **HTTP 409** / **503** | Mã máy chủ trả về: 409 = "kho đã đổi, phải chuẩn bị lại"; 503 = "tạm thời không phục vụ được". |

---

*Bài 4 kể mỗi đoạn được biến thành hai dạng: vector nghĩa và bảng từ khoá. Bài này kể chúng được cất ở đâu, và vì sao chatbot luôn kiểm tủ trước khi mở cửa.*

## Quay lại người hướng dẫn viên

8.435 thẻ không thể để rời trong túi. Người hướng dẫn viên cất chúng vào **một cái tủ có ngăn**, xếp sao cho rút thẻ theo ý hay theo chữ đều nhanh. Trên nóc
tủ dán một **tờ phiếu**: tủ này xếp từ cuốn sổ bản nào, gồm những trang nào, bao nhiêu thẻ.

Mỗi sáng trước khi dẫn khách, họ làm một việc nhỏ mà rất quan trọng: **so tờ phiếu với cuốn sổ đang cầm**. Nếu tối qua họ đã sửa vài trang trong sổ mà chưa
xếp lại thẻ, thì tủ đang chứa thông tin cũ. Khi đó họ **không đi dẫn khách**, mà xếp lại tủ trước đã. Thà trễ một chút còn hơn nói với khách thông tin cũ mà
tưởng là mới.

Qdrant là cái tủ. Build record là tờ phiếu. Chuỗi kiểm lúc khởi động là việc so phiếu mỗi sáng.

## Tủ chứa gì

- Qdrant chạy trên máy anh bằng **Docker**, ghim đúng một phiên bản (1.18.3). Chatbot nói chuyện với nó qua cổng 6335. Dữ liệu nằm trong thư mục `qdrant_storage/`
  của dự án, nên tắt Docker rồi bật lại vẫn còn nguyên.
- Chatbot dùng **một ngăn** (collection) duy nhất, tên `hue_full_corpus_7a2_e5_small_384`. Tên này ghi luôn model đã dùng (e5-small, 384 chiều), để không bao
  giờ lẫn với ngăn của model khác.
- Ngăn có **8.435 thẻ** (point), đúng bằng số đoạn. Mỗi thẻ gồm:
  - một **mã** cố định, suy ra từ mã đoạn (bài 2);
  - **vector nghĩa** 384 con số, đo độ gần bằng cosine;
  - **vector từ khoá** (bảng từ BM25);
  - **hồ sơ 7 trường** (bài 3).
- Tủ để cấu hình mặc định: không thêm chỉ mục lọc theo trường, không chia ổ đĩa. Với 8.435 thẻ, tìm vẫn mất chỉ vài mili giây.

## Phiếu chuẩn bị ghi gì

Mỗi lần chuẩn bị kho, máy ghi **một phiếu** (build record). Phiếu được ghi **một lần**: nếu đã có phiếu cùng tên thì bước chuẩn bị dừng, không ghi đè. Phiếu ghi:

- danh sách 204 file kho và **dấu (hash) của từng file**;
- số đoạn (8.435);
- model đã dùng: tên, phiên bản ghim, số chiều;
- dấu của file từ điển từ khoá (bài 4);
- cấu hình ngăn: tên vector, cách đo khoảng cách, kiểu hồ sơ;
- số thẻ đã cất.

Phiếu này là **nguồn sự thật duy nhất** cho câu hỏi "tủ có khớp sổ không".

## Kiểm lúc mở cửa: 5 bước

Mỗi lần chatbot khởi động, trước khi nhận câu hỏi đầu tiên, nó chạy đúng 5 bước kiểm theo thứ tự:

1. **Phiếu có đúng không:** có tồn tại, đã hoàn tất, đúng kiểu phiếu, đúng tên ngăn, đúng tên vector, đúng cách đo cosine, số thẻ bằng số đoạn, đúng model và
   phiên bản.
2. **Sổ có bị sửa không:** tính lại dấu của **từng file kho hiện tại** rồi so với phiếu. Phát hiện được file mới thêm, file bị mất, và file bị sửa dù chỉ một
   chữ.
3. **Từ điển từ khoá có khớp không:** dấu file từ điển phải đúng như phiếu ghi.
4. **Tủ có khớp phiếu không:** ngăn có tồn tại, đúng cấu trúc, số thẻ trong Qdrant bằng số đoạn trong phiếu.
5. **Model có chạy không:** nạp e5-small và thử tính vector cho một câu.

Kết quả:
- **Bước 1–4 sai** ⇒ chatbot trả mã **409**, kèm lý do "kho đã đổi, phải chuẩn bị lại". Nó không trả lời câu nào cho tới khi chuẩn bị lại.
- **Bước 5 sai, hoặc Qdrant không chạy** ⇒ mã **503**, "tạm thời không phục vụ được".
- Trang kiểm sức khoẻ (`/health`) vẫn trả lời, nhưng báo trạng thái "đang hỏng" (degraded). Người vận hành nhìn vào là biết chỗ nào sai.

**Vì sao thiết kế "đóng khi lệch"?** Nếu kho đã sửa mà tủ còn thẻ cũ, chatbot vẫn trả lời trôi chảy, có ghi nguồn hẳn hoi, nhưng nội dung là bản cũ. Không ai
nhận ra, kể cả người viết, vì ngữ cảnh đưa vào trông rất hợp lý. Lỗi im lặng kiểu này tệ hơn nhiều so với một chatbot báo thẳng "chưa sẵn sàng". Với đồ án
có luật "chỉ nói điều kho có", trả lời từ một kho không còn khớp chính là vi phạm luật đó.

## Chuẩn bị lại khi kho đổi

Quy trình có 7 bước, ghi trong hướng dẫn của dự án:
1. sửa kho, có sao lưu bài gốc (bài 1);
2. cắt đoạn thử để chắc không lỗi (bài 2);
3. sao lưu phiếu cũ, từ điển cũ, và chụp ngăn cũ nếu còn cần;
4. xoá **đủ ba thứ**: ngăn trong Qdrant, phiếu, từ điển từ khoá. Thiếu một thứ thì bước chuẩn bị từ chối chạy. Lệnh xoá do anh tự chạy, agent không được tự
   xoá dữ liệu;
5. chạy lệnh chuẩn bị;
6. kiểm `/health` và kiểm kết quả tìm;
7. dọn bản sao lưu khi anh duyệt.

Bước chuẩn bị chỉ chạy khi chưa có ngăn và chưa có phiếu. Nó kiểm dấu kho cả **trước và sau** khi tính vector, để chắc kho không bị sửa giữa chừng. Nó ghi mỗi
lần 64 thẻ. Ghi xong, nó đếm lại số thẻ, kiểm hồ sơ của từng thẻ, và đọc lại vài vector mẫu cho chắc. Lỗi ở đâu là dừng ở đó; không có chuyện "chạy tiếp từ giữa".

Thời gian: khoảng **4 phút** cho cả kho trên máy anh. Trong lúc đó chatbot ngừng phục vụ.

## Một chuyện thật: sửa 11 bài, chatbot từ chối mở cửa

Ngày 05/11, 11 bài điểm tham quan của Quần thể Cố đô được thêm một dòng giờ mở cửa chung (bài 1). Sửa xong, chatbot **từ chối khởi động**: bước 2 phát hiện
dấu của 11 file đã đổi. Đây đúng là điều thiết kế muốn: nếu không có bước này, chatbot sẽ tiếp tục trả lời "kho không có giờ mở cửa" trong khi kho đã có.

Phải chuẩn bị lại: xoá ba thứ (anh tự chạy lệnh xoá vì agent bị chặn quyền), chạy lệnh chuẩn bị khoảng 4 phút, số đoạn tăng từ 8.424 lên **8.435** (thêm 11
đoạn, đúng mỗi bài một dòng). Đây là lần chuẩn bị lại thứ ba từ cuối tháng 10. Cả ba lần các bước kiểm đều đạt.

Một chuyện nhỏ khác (31/10): Docker Desktop trên Windows bị tắt, Qdrant không chạy, chatbot trả 503 cho mọi câu. Bật Docker lên là chạy lại, không mất dữ liệu.

## Khi nào hỏng

- **Sửa kho trong lúc chatbot đang chạy.** Bước kiểm chỉ chạy lúc khởi động. Sửa kho khi server đang chạy thì nó vẫn trả lời bằng tủ cũ cho tới lần khởi động
  sau. (Suy ra từ code; chưa thử.)
- **Đổi cách cắt đoạn mà không đổi kho.** Phiếu ghi dấu file kho, không ghi dấu của code cắt đoạn hay file quy tắc gắn lưu ý. Đổi code cắt đoạn mà không chuẩn
  bị lại thì bước kiểm không bắt được. (Suy ra từ code.)
- **Docker tắt** ⇒ 503 cho mọi câu.
- **Xoá thiếu một trong ba thứ** ⇒ bước chuẩn bị từ chối chạy. Đây là lỗi an toàn, không làm hỏng gì, chỉ mất công.
- **Thiếu model trong bộ nhớ tạm của máy** (máy mới, chưa tải e5-small) ⇒ bước 5 hỏng ⇒ 503.

## Ba điều chính

1. Qdrant là **tủ thẻ**: một ngăn, 8.435 thẻ, mỗi thẻ có vector nghĩa + vector từ khoá + hồ sơ 7 trường. Chạy bằng Docker trên máy anh.
2. **Phiếu chuẩn bị** ghi dấu từng file kho. Mỗi lần khởi động, chatbot **kiểm 5 bước**; tủ lệch sổ thì trả **409** và không trả lời, thà đóng cửa còn hơn
   trả lời bằng thông tin cũ.
3. Chuẩn bị lại mất khoảng **4 phút**, kiểm cả trước và sau. Đã làm 3 lần, gần nhất là khi thêm giờ mở cửa cho 11 bài.

**Bài sau:** Bài 6 — Rút đúng thẻ (retrieval): tìm theo nghĩa lấy 30, chấm lại theo từ khoá, trộn hai bảng, giữ 10. Và vì sao chatbot đôi khi từ chối nhầm.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Qdrant 1.18.3 ghim digest, cổng 6335 → 6333, `qdrant_storage/`: `docker-compose.yml` [code, xem 11/11]; `backend/config/settings.yaml` (URL, timeout 30 s) [code]
- Cấu trúc ngăn (dense 384 cosine + sparse, không payload index): `backend/vectorstore/qdrant.py` `expected_full_corpus_schema` [code]
- Phiếu chuẩn bị ghi một lần: `backend/ingestion/source_state.py` `make_full_corpus_build_record` [code]
- 5 bước kiểm lúc khởi động: `backend/retrieval/full_corpus.py` `build_full_corpus_retrieval_service` + `verify_full_corpus_record_freshness` [code, xem 11/11]
- 409 `corpus_reingest_required` / 503: `backend/api/app.py` (khởi động); `/health` degraded: `backend/api/health.py` [code, xem 11/11]
- Chuẩn bị: kiểm dấu trước + sau, lô 64, đếm + kiểm hồ sơ + đọc lại vector mẫu: `backend/ingestion/full_corpus_pipeline.py` [code]; 7 bước: `guides/full_corpus_rag.md` mục "Build lại index" [tài liệu]
- Chuẩn bị lại 05/11 (11 bài, 8.424 → 8.435, khoảng 4 phút); Docker tắt 31/10: `bao_cao_he_thong/05_BAO_CAO_LUU_TRU_QDRANT.md`, `session_prompt/Project_Status.md` §8 [đã chạy]
- Hai ý "sửa kho lúc đang chạy" và "đổi code cắt đoạn" là suy ra từ code, chưa thử thật.

</details>
