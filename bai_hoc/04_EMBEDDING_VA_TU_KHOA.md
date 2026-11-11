# Bài 4 — Biến thẻ thành thứ tìm được: embedding và từ khoá

*Cập nhật lần cuối: 14:41, ngày 11/11/2026 · sửa cỡ model Qwen3-8B (ghi ở Nguồn).*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Vector nghĩa | **embedding** / **dense vector** | Dãy 384 con số đại diện cho ý nghĩa một đoạn. |
| Model embedding | **intfloat/multilingual-e5-small** (trong code: `e5-small-384`) | Model nhỏ biến chữ thành vector, chạy ngay trên máy, không tốn tiền. |
| Độ gần — **mới** | **cosine similarity** | Cách đo hai vector "chỉ cùng hướng" tới đâu; càng gần 1 càng cùng nghĩa. |
| Nhãn đầu câu — **mới** | tiền tố **`query: `** / **`passage: `** | Chữ thêm vào đầu câu hỏi / đầu đoạn để model e5 biết đâu là câu hỏi, đâu là tài liệu. |
| Từ khoá | **BM25** / **sparse vector** | Cách chấm đoạn theo số chữ trùng với câu hỏi (đã gặp ở bài 0). |
| Tách chữ — **mới** | **tokenize** (trong code: `scoring/bm25.py`) | Cắt một câu thành các "từ" để đếm. |
| Từ điển của kho — **mới** | **vocabulary** + **IDF** (trong file **sparse state**) | Danh sách 5.631 từ có trong kho, kèm độ "hiếm" của từng từ. |

---

*Bài 3 kể mỗi thẻ mang tên bài và đường tiêu đề ở góc, ghép thành "chữ để tìm". Bài này kể chữ đó được biến thành thứ máy tìm được, theo hai cách.*

## Quay lại người hướng dẫn viên

Có 8.435 thẻ trong hộp, làm sao rút đúng thẻ thật nhanh? Người hướng dẫn viên dùng hai cách cùng lúc.

**Cách thứ nhất: nhớ theo ý.** Khách hỏi "chỗ nào ngắm hoàng hôn đẹp", họ nghĩ ngay tới các thẻ nói về sông Hương lúc chiều, đồi Vọng Cảnh, phá Tam Giang, dù
thẻ không có chữ "hoàng hôn". Họ nhớ theo **nghĩa**.

**Cách thứ hai: dò theo chữ.** Khách hỏi đích danh tên một quán, hay "vé 200.000 đồng", họ dò đúng những thẻ có chữ đó. Dò theo **chữ trùng** thì không bao
giờ nhầm tên riêng hay con số.

Mỗi cách giỏi một việc, và hay hỏng ở chỗ cách kia giỏi. Nên dùng cả hai. hue_rag cũng biến mỗi đoạn thành **hai dạng**: một vector nghĩa và một bảng từ khoá.

## Dạng thứ nhất: vector nghĩa (embedding)

Mỗi đoạn, cụ thể là "chữ để tìm" của nó (tên bài + đường tiêu đề + thân đoạn, bài 3), được đưa qua model **e5-small**. Model trả về **384 con số**. Đó là vector
nghĩa của đoạn. Hai đoạn nói cùng một ý thì vector "chỉ cùng hướng", dù dùng chữ khác nhau.

Vài chi tiết kỹ thuật quan trọng:
- **Nhãn đầu câu.** Model e5 được huấn luyện để phân biệt câu hỏi và tài liệu. Nên mỗi đoạn được thêm `passage: ` ở đầu, mỗi câu hỏi được thêm `query: `. Quên
  nhãn này thì tìm kém đi rõ.
- **Chuẩn hoá độ dài.** Mọi vector được đưa về cùng độ dài 1. Khi đó Qdrant chỉ cần đo **cosine** (độ chỉ cùng hướng) để biết hai vector gần nhau tới đâu.
- **Ghim đúng phiên bản model.** Code ghi cứng một phiên bản cụ thể của e5-small. Hôm nay và tháng sau tải về vẫn là cùng một model, nên vector không âm thầm
  đổi.
- **Chạy trên máy (CPU), không gọi mạng, 0 đồng.** Tính vector cho cả kho mất vài phút. Tính vector câu hỏi rồi tìm trong Qdrant mất khoảng **21 mili giây**
  ở câu giữa (28 mili giây ở câu chậm), tức gần như tức thì.
- **Câu hỏi được chuẩn hoá chữ có dấu** về một dạng chuẩn (NFC) trước khi tính. Tiếng Việt có hai cách lưu cùng một chữ có dấu trong máy. Nếu câu hỏi lưu theo
  cách kia, vector sẽ lệch dù mắt nhìn giống hệt.

Vì sao chọn e5-small? Ngay từ đầu (cuối tháng 8, bản thử chỉ có phần món ăn), ba model được so trên cùng bộ câu: e5-small, e5-base (to hơn) và một model
tiếng Việt. e5-small nhỉnh hơn một chút, chưa model nào thắng rõ. Vì vậy chọn cái **nhỏ nhất, nhanh nhất, chạy được trên máy**. Hai tháng sau, mình thử lại
với một model lớn hơn rất nhiều (chuyện thật bên dưới).

## Dạng thứ hai: bảng từ khoá (BM25)

Cùng "chữ để tìm" đó được **tách thành từ**. Cách tách rất đơn giản: đổi hết sang chữ thường, rồi cắt ở mọi chỗ không phải chữ hay số. Tiếng Việt viết cách
giữa các âm tiết, nên thực tế mỗi "từ" là một âm tiết: "bún bò huế" thành "bún", "bò", "huế".

Từ đó máy lập **từ điển của kho**: 5.631 từ khác nhau, mỗi từ kèm độ **hiếm**. Từ có ở hầu hết đoạn (như "huế", "và") thì gần như không có giá trị. Từ chỉ có
ở vài đoạn (như tên một quán) thì rất có giá trị. Khi tìm, đoạn được cộng điểm cho mỗi từ trùng với câu hỏi, từ càng hiếm thì càng nhiều điểm. Đoạn quá dài
bị trừ bớt để không "thắng" chỉ vì nhiều chữ. Đây là công thức **BM25**, với hai hằng số chuẩn (k1 = 1,5; b = 0,75).

Từ điển này được ghi **một lần** vào một file riêng (sparse state). Lần chuẩn bị sau phải ra đúng file đó từng byte, nếu không thì bước chuẩn bị dừng lại. Nhờ
vậy từ điển không bao giờ lệch với kho mà không ai biết.

## Hai dạng làm việc với nhau thế nào

Cả hai dạng được cất vào Qdrant trên cùng một điểm (bài 5). Lúc trả lời, tìm theo nghĩa lấy ra 30 đoạn trước. Rồi BM25 **chấm lại đúng 30 đoạn đó** theo từ
khoá, và hai bảng xếp hạng được trộn lại (bài 6). Tức là: **nghĩa chọn ứng viên, từ khoá giúp xếp lại cho đúng tên riêng và con số**.

## Một chuyện thật: model lớn hơn khoảng 70 lần mà lại thua

Ngày 30/10, mình thử thay e5-small bằng **Qwen3-Embedding-8B**: một model lớn hơn rất nhiều, vector 4.096 con số thay vì 384, phải gọi qua mạng. Ý tưởng nghe
rất hợp lý: model to hơn thì hiểu nghĩa tốt hơn.

Luật ghi trước: **không câu nào được mất đoạn đúng**, và không được chậm thêm quá 50 mili giây. Kết quả:

| Đo gì | e5-small (đang dùng) | Qwen3-8B | Nghĩa là |
|---|---|---|---|
| 40 câu thử: tốt lên / như cũ / mất đoạn đúng | — | 2 / 35 / 3 | mất 3 câu ⇒ vỡ luật; đo lại lần hai vẫn đúng 3 câu đó |
| 15 câu kiểm | — | 2 / 10 / 3 | lại mất 3 câu |
| Thời gian tính vector câu hỏi + tìm (câu giữa / câu chậm) | 21 / 28 ms | 2.228 / 6.487 ms | chậm khoảng **100 lần**; cả câu ước vượt 11 giây ở câu chậm, trong khi trần là 5 giây |
| Tiền | 0 | khoảng 0,009 USD cho lượt thử | nhỏ, nhưng là tiền thêm cho mỗi câu |

Kết luận: **giữ e5-small**, xoá chỉ mục thử. Điều thú vị hơn nằm ở chỗ báo cáo chỉ ra: ở 9 trên 40 câu, đoạn đúng **đã nằm trong 30 ứng viên** nhưng bị xếp
dưới hạng 10. Tức là chỗ thiếu không nằm ở việc hiểu nghĩa (model nào cũng tìm ra), mà ở việc **xếp hạng**. Đổi model to hơn không chữa được chỗ đó.

Một thí nghiệm nhỏ hơn cùng tinh thần (25/10): thử tách từ "đúng tiếng Việt" hơn, như ghép hai âm tiết thành từ ghép, hay dùng thư viện tách từ tiếng Việt
`pyvi`. Cả hai cách **làm mất đoạn đúng ở 1 câu** (và 3–4 câu nếu lấy rộng hơn). Cách tách theo âm tiết đơn giản vẫn tốt nhất. Thử đổi hằng số của BM25 cũng
không cách nào tốt hơn.

## Khi nào hỏng

- **Câu gõ không dấu.** "bun bo hue" khác hoàn toàn "bún bò huế" với cả hai dạng. Thử trên 32 câu: gõ không dấu thì chỉ 1 câu có đủ đoạn đúng, so với 13 câu khi
  gõ có dấu. Anh đã chốt (25/10): câu không dấu nằm **ngoài phạm vi** đồ án.
- **Vector nghĩa bỏ sót thì từ khoá không cứu được.** BM25 chỉ chấm lại 30 đoạn mà tìm theo nghĩa đã chọn. Đoạn nào không lọt 30 thì dù trùng chữ y hệt cũng
  không được xét.
- **Từ không có trong từ điển** được 0 điểm. Ví dụ một tên quán mới chưa có trong kho.
- **Con số bị tách đôi.** Cách tách cắt ở dấu chấm, nên "40.000" thành "40" và "000". Dò đúng một con số giá vì vậy kém chính xác hơn mong đợi.
- **Bộ đo nhỏ** (40 + 15 câu có nhãn đoạn đúng): chỉ thấy được khác biệt lớn. Chênh lệch nhỏ giữa hai model thì chưa đo ra.

## Ba điều chính

1. Mỗi đoạn có **hai dạng để tìm**: **vector nghĩa** 384 con số từ e5-small (chạy trên máy, 0 đồng, khoảng 21 mili giây) và **bảng từ khoá BM25** (tách theo
   âm tiết, từ điển 5.631 từ).
2. **Nghĩa chọn ứng viên, từ khoá xếp lại** cho đúng tên riêng và con số. Mỗi cách bù chỗ hỏng của cách kia.
3. Model lớn hơn khoảng 70 lần (Qwen3-8B) **mất đoạn đúng ở 3 câu và chậm khoảng 100 lần**, nên giữ e5-small. Chỗ thiếu thật là **xếp hạng**, không phải hiểu nghĩa.

**Bài sau:** Bài 5 — Cất hộp thẻ vào tủ (Qdrant): cất ở đâu, phiếu chuẩn bị kiểm những gì, và vì sao chatbot thà không chạy còn hơn chạy trên kho lệch.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- e5-small, ghim phiên bản `614241f6…`, 384 chiều, CPU, batch 8, chuẩn hoá độ dài: `backend/embedding/full_corpus.py` `DENSE_MODEL_SPECS` [code, xem 11/11]; tiền tố `passage: ` / `query: `: hàm `prepare_document` / `prepare_query` [code]
- Chuẩn hoá NFC câu hỏi: `backend/retrieval/full_corpus.py` hàm `normalize_query` [code]; đo NFD làm MRR tụt 0,20: `bao_cao_he_thong/06_BAO_CAO_TIM_KIEM.md` [đã chạy]
- 21 / 28 ms là `dense_ms` (gồm tính vector câu hỏi và tìm trong Qdrant, không riêng bước tính vector): `report_agent/2026-10-27_phan_ton_phase_cu/qwen3_8b_implementation.md` [đã chạy, 30/10]
- Tách chữ `\w+` trên chữ thường: `backend/scoring/bm25.py` hàm `tokenize`; k1 1,5, b 0,75: `bm25.py`, `sparse.py` [code, xem 11/11]. "Âm tiết" là cách gọi gần đúng.
- Từ điển 5.631 từ, sparse state ghi một lần: `data/full_corpus_builds/full_corpus_sparse_state.json`; `backend/ingestion/full_corpus_pipeline.py` [code + đã đọc 11/11]
- BM25 chấm lại 30 ứng viên của tìm theo nghĩa, trộn RRF: `backend/retrieval/full_corpus.py` hàm `search` [code]
- Chọn e5-small ban đầu (29/08, 45 câu món ăn; nDCG@5 e5-small 0,7425 · e5-base 0,7061 · model tiếng Việt 0,7164; chưa model nào thắng rõ): `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` thẻ N2-07 [đã chạy]
- Qwen3-8B (30/10): 2 / 35 / 3 trên 40 câu thử, 2 / 10 / 3 trên 15 câu kiểm; 2.228 / 6.487 ms; p95 cả câu ước khoảng 11,4 s; 0,0089 USD; 9 / 40 câu có đoạn đúng trong 30 ứng viên nhưng ngoài 10: `qwen3_8b_implementation.md` [đã chạy]
- Tách từ ghép / `pyvi` / đổi hằng số BM25 (25/10, 32 câu, kho cũ); không dấu 1 / 32 ↔ 13 / 32: `phase_8_1_g4_keyword_implementation.md` qua 91 thẻ N2-11 [đã chạy]
- "vé 200.000 đồng", "hoàng hôn" là ví dụ tự đặt để minh hoạ, không phải câu trong bộ chấm.

- **Sửa 14:41 11/11/2026:** bản trước ghi Qwen3-8B "lớn hơn 10 lần" — số 10 là tỉ lệ số chiều vector (4.096 / 384); về cỡ model: 8 tỉ tham số ↔ e5-small khoảng 118 triệu ⇒ khoảng 70 lần [kiến thức công khai, chưa tra lại trong phiên].

</details>
