# Bài 2 — Cắt sổ thành thẻ ghi chú: chunking

*Cập nhật lần cuối: 09:55, ngày 11/11/2026 · viết lại: kể thẳng từ đầu, giữ đủ chi tiết kỹ thuật.*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Đoạn (thẻ ghi chú) | **chunk** | Mẩu nhỏ cắt ra từ một bài. |
| Cắt đoạn | **chunking** (trong code: `full_corpus_chunker.py`) | Bước chia bài thành đoạn. |
| Khối — **mới** | **block** (`paragraph`, `list_item`, `table`, `blockquote`) | Một phần tự nhiên của bài Markdown: đoạn văn, mục danh sách, bảng, đoạn trích. |
| Gối đầu | **overlap** | Hai đoạn liền nhau lặp lại một phần chữ ở chỗ nối. hue_rag không dùng. |
| Token | **token** | Đơn vị chữ mà model đếm. Một từ tiếng Việt khoảng 1–2 token. |
| Giới hạn độ dài — **mới** | **max tokens** của tokenizer (e5-small: 512) | Model embedding chỉ đọc tối đa 512 token một lần; dài hơn là bị cắt mất. |
| Phần bằng chứng — **mới** | **evidence parts** (`body`, `header`, `condition`) | Các mảnh chữ làm nên một đoạn, kèm vị trí chính xác trong file gốc. |
| Mã đoạn | **chunk_id** (dạng `<file>#<số thứ tự>`) | Tên riêng của mỗi đoạn; chạy lại ra đúng mã cũ. |

---

*Bài 1 nói kho là 204 bài Markdown soạn theo mẫu, mỗi câu "đọc riêng vẫn hiểu". Bài này kể bước đầu tiên của giai đoạn chuẩn bị: cắt bài thành đoạn.*

## Quay lại người hướng dẫn viên

Mỗi lần khách hỏi, người hướng dẫn viên không thể đọc lại cả cuốn sổ. Nên họ làm một việc từ trước: **cắt sổ thành những thẻ ghi chú nhỏ**, mỗi thẻ một ý,
rồi xếp vào hộp. Khách hỏi gì, họ rút ra vài thẻ đúng chuyện đó để đọc.

Cắt thế nào cho tốt? Một thẻ quá to thì chứa nhiều thứ không liên quan, và trong túi chỉ mang được vài thẻ. Một thẻ cắt ngang câu thì nửa ý nằm ở thẻ này,
nửa ý ở thẻ kia. Cách khôn nhất là **cắt theo đúng chỗ người soạn đã chia ý**: hết một đoạn văn thì cắt, hết một mục thì cắt.

Chunking của hue_rag làm đúng như vậy.

## Cắt theo cấu trúc bài

Máy đọc mỗi file Markdown và nhận ra các **khối** tự nhiên của bài: đoạn văn, mục danh sách, bảng, đoạn trích. Tiêu đề (`#`, `##`, `###`) không thành đoạn riêng.
Tiêu đề được ghi lại thành "đường tiêu đề" để gắn vào các đoạn bên dưới nó (bài 3). Rồi máy làm theo bốn luật:

1. **Mỗi khối là một đoạn**, nếu khối đó vừa giới hạn độ dài. Một đoạn văn là một đoạn. Một mục danh sách là một đoạn. Một bảng ngắn là một đoạn.
2. **Bảng quá dài thì tách từng dòng**, và **mỗi dòng mang theo dòng tiêu đề của bảng**. Nhờ vậy dòng giá nào cũng biết cột nào là món, cột nào là giá.
3. **Mục danh sách có mục con mà quá dài** thì tách từng mục con, mỗi mục con giữ lại nhãn của mục cha.
4. **Đoạn văn quá dài thì tách ở ranh giới câu**, không bao giờ cắt giữa câu.

**Không gối đầu.** Gối đầu sinh ra để chữa chuyện cắt ngang ý: lặp lại vài câu ở chỗ nối để ý bị cắt vẫn còn. Ở đây máy cắt đúng ranh giới ý mà người soạn đã
đặt, nên không cắt ngang ý nào, và không cần gối đầu.

Ví dụ tự đặt, không lấy từ kho. Một bài quán ăn có bảng giá dài:

```text
| Món        | Giá         |
| Bún bò     | 40.000 đồng |
| Bánh bèo   | 30.000 đồng |
… (nhiều dòng nữa)
```

Bảng này quá dài nên được tách. Đoạn của dòng "Bún bò" sẽ gồm dòng tiêu đề "Món | Giá" và dòng "Bún bò | 40.000 đồng". Nhờ đó người viết đọc đoạn này là biết
40.000 đồng là giá của món gì. Nếu cắt theo số ký tự, dòng tiêu đề có thể rơi vào một đoạn khác, và con số đứng trơ trọi.

## Giới hạn độ dài: đếm bằng đúng tokenizer của model

"Vừa giới hạn" nghĩa là gì? Model embedding e5-small (bài 4) chỉ đọc được tối đa **512 token** một lần. Đoạn dài hơn thì phần đuôi bị bỏ mà không ai báo. Vì
vậy máy đếm token **bằng chính tokenizer của model**, không ước theo số chữ. Trong code còn hai tokenizer cũ cùng được kiểm (một cái 512, một cái 256), có từ
hồi còn định thử nhiều model. Đã thử bỏ hai cái này: đoạn đúng không đổi. Vì vậy giữ nguyên cho tới khi cần chuẩn bị lại vì lý do khác.

Số đo hiện nay: đoạn dài nhất là **366 / 512 token** theo e5-small, tức còn dư khá xa. Phần lớn đoạn ngắn: một nửa số đoạn dưới khoảng **85 token**, cỡ một
hai câu. Số này đếm trên kho trước đợt sửa cuối tháng 10, nhưng cách cắt không đổi.

## Mỗi đoạn mang theo những gì

Mỗi đoạn không chỉ là một khúc chữ. Nó mang theo ba thứ:

- **Phần bằng chứng**: các mảnh chữ làm nên đoạn (thân đoạn, dòng tiêu đề bảng nếu có, câu lưu ý gắn kèm nếu có), mỗi mảnh kèm **vị trí bắt đầu và kết thúc
  chính xác trong file gốc**. Nhờ vậy khi chatbot ghi nguồn, phần "xem đoạn gốc" lấy đúng mảnh chữ trong bài, không phải chữ đã ghép lại.
- **Chữ để tìm**: tên bài + đường tiêu đề + các phần bằng chứng ghép lại. Đây là chữ được biến thành vector và đếm từ khoá (bài 3, bài 4).
- **Mã đoạn** dạng `<tên file>#<số thứ tự>`. Từ mã này máy suy ra mã cất trong Qdrant theo một công thức cố định. Nhờ vậy **chạy lại cắt đoạn trên cùng kho thì
  ra đúng các đoạn cũ, đúng mã cũ**, và có test kiểm điều này.

## Máy tự kiểm trước khi cho qua

Cắt xong, máy chạy một **vòng kiểm cuối trên mọi đoạn**:
- đoạn nào vượt giới hạn token thì báo lỗi;
- mảnh bằng chứng nào không khớp đúng từng chữ với file gốc ở đúng vị trí đã ghi thì báo lỗi;
- quy tắc gắn lưu ý nào không khớp đúng một chỗ trong kho thì báo lỗi.

Chỉ cần **một lỗi là cả bước chuẩn bị dừng lại**, không có chuyện "bỏ qua đoạn lỗi rồi chạy tiếp". Kết quả lần chuẩn bị gần nhất: 204 bài → **8.435 đoạn,
0 lỗi**.

## Một chuyện thật: đoạn to tìm được nhiều hơn, nhưng lại tệ hơn

Trong đợt rà lại mọi lựa chọn cũ (cuối tháng 10), mình thử **12 cách cắt khác** trên 32 câu hỏi đã biết chắc đáp án nằm ở đâu trong kho. Ví dụ: gộp đoạn ngắn
thành đoạn 128, 256, 384 hay 512 token; sau khi tìm thì mở rộng ra cả mục chứa đoạn đó; gộp các dòng bảng liền nhau; bỏ tên bài và tiêu đề khỏi chữ để tìm.

Thước đo là: đoạn chứa đáp án có còn nằm trong phần đưa người viết không. Để so cho công bằng, mọi cách đều chỉ được đưa **cùng một lượng chữ** cho người viết
(750 token). Giống như xếp đồ vào cùng một chiếc vali: được mang 9 món nhỏ, hay 4 món to. Nếu không giữ chung một cỡ vali, đoạn to sẽ "tự thắng" chỉ vì chở
được nhiều chữ hơn. Luật ghi **trước** khi chạy: cách mới chỉ được nhận nếu **không làm câu nào mất đáp án**.

Kết quả trên 32 câu, so với cách đang dùng:

| Cách thử | Câu tốt lên / câu mất đáp án | Nghĩa là |
|---|---|---|
| Gộp nhỏ tới 128 token; gộp dòng bảng | 0 / 0 | không khác ⇒ đổi cũng không được gì |
| Gộp tới 256 token | 0 / 4 | không câu nào tốt lên, 4 câu mất ⇒ bỏ |
| Gộp tới 384 token | 1 / 6 | được 1 mất 6 ⇒ bỏ |
| Gộp tới 512 token | 0 / 6 | mất 6 câu, và ở mức này phép thử thống kê cũng xác nhận là tụt thật, không phải may rủi |
| Mở rộng ra cả mục sau khi tìm | 0 / 8 | tệ hơn rõ: các đoạn "anh em" của 1–2 đoạn đầu chiếm gần hết vali |
| Bỏ tên bài + tiêu đề, hoặc chỉ giữ tiêu đề gần nhất | 3–4 / 7–8 | có câu tốt lên nhưng mất nhiều hơn ⇒ bỏ theo luật "không câu nào mất" (bài 3 kể kỹ) |

Vì sao đoạn to lại tệ? Đoạn to quả thật **chứa được đáp án nhiều hơn**. Nhưng mỗi đoạn chiếm nhiều chỗ, nên chỉ khoảng 4–5 đoạn vừa vali, thay vì khoảng 9
đoạn nhỏ trỏ tới 9 chỗ khác nhau trong kho. Câu hỏi nào cần ghép thông tin từ nhiều chỗ thì đoạn to thua.

Điều rút ra lớn hơn chuyện cắt đoạn: thứ giúp thật là **cho người viết thấy nhiều chỗ hơn**, không phải cho mỗi chỗ to hơn. Cũng chính đợt rà này dẫn tới quyết
định đưa 10 đoạn thay vì 5 (bài 0).

Một lưu ý về độ chắc: 32 câu là mẫu nhỏ. Với đoạn to, kết luận đủ chắc: cả bốn mức gộp đều cùng chiều (gần như không câu nào tốt lên, 4–6 câu mất), và ở mức
512 token phép thử thống kê xác nhận. Còn "gộp nhỏ không khác" chỉ có nghĩa là trên 32 câu này chưa thấy khác.

## Khi nào hỏng

- **Bảng dài.** Mỗi dòng giá đứng riêng thành một đoạn rất ngắn, ít chữ. Câu hỏi viết khác chữ thì bước tìm dễ trượt dòng đó. Gốc của lỗi nằm ở bước tìm
  (bài 6); thử gộp dòng bảng không giúp.
- **Nhiều đoạn rất ngắn.** Gần 1.800 đoạn dưới 50 token (đếm trên kho cũ). Đoạn quá ngắn có ít chữ để tìm theo nghĩa. Thử gộp lại thì không giúp hoặc tệ hơn.
- **Mã đoạn dồn số khi sửa giữa bài.** Mã đánh số theo thứ tự trong bài, nên xoá một dòng giữa bài thì các đoạn phía sau đổi số. Chatbot vẫn chạy đúng, vì
  chuẩn bị lại thì mọi thứ khớp. Nhưng khi so "trước và sau khi sửa kho", phải so theo nội dung chứ không theo mã.
- **Ba cặp đoạn lặp một phần.** Ở 3 bài di tích có đoạn trích nằm trong mục danh sách, nên một phần chữ xuất hiện ở hai đoạn. Đã thử bỏ phần lặp: không khác,
  nên để nguyên.

## Ba điều chính

1. hue_rag **cắt theo cấu trúc bài**: mỗi đoạn văn, mục danh sách, bảng ngắn là một đoạn. Bảng dài tách từng dòng **kèm dòng tiêu đề**. Đoạn dài tách ở
   **ranh giới câu**. **Không gối đầu**, vì không cắt ngang ý nào.
2. Mỗi đoạn mang **vị trí chính xác trong file gốc** (để ghi nguồn đúng chỗ) và **mã cố định** (chạy lại ra đúng đoạn cũ). Máy kiểm mọi đoạn; **một lỗi là
   dừng**. Hiện nay: 8.435 đoạn, 0 lỗi.
3. Đã thử 12 cách khác với **cùng một lượng chữ** đưa người viết. **Đoạn to tệ hơn**, vì người viết thấy ít chỗ hơn. Điều giúp thật là **thấy nhiều chỗ hơn**.

**Bài sau:** Bài 3 — Ghi tên lên góc thẻ (metadata): mỗi đoạn mang theo tên bài và đường tiêu đề, ví dụ "Bún bò Huế > Quán nổi tiếng". Thử bỏ phần này đi: 3–4 câu
tốt lên nhưng 7–8 câu mất đáp án.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Bốn luật cắt: `backend/ingestion/chunking/full_corpus_chunker.py` hàm `chunk_document` (bảng: cả bảng nếu vừa, không thì từng hàng kèm tiêu đề; mục danh sách có mục con: tách mục con giữ nhãn cha; còn lại: tách ở ranh giới câu) + `markdown_blocks.py` (loại khối `paragraph` / `list_item` / `table` / `blockquote`) [code, xem 11/11]
- Giới hạn token 3 tokenizer (512 / 512 / 256): `backend/config/settings.yaml` [code]; thử bỏ 2 tokenizer cũ: không đổi đoạn đúng (Phase 8.1) [đã chạy]
- Dài nhất 366 / 512 (30/10); trung vị 85 token, 1.787 đoạn dưới 50 token, 3 cặp lặp (24/10, kho cũ): `bao_cao_he_thong/03_BAO_CAO_CHIA_DOAN.md` [đã chạy]
- Chữ để tìm = tên bài + đường tiêu đề + phần bằng chứng: `full_corpus_chunker.py` hàm `build_representation_a_search_text` [code]
- Mã đoạn `file#số`, mã Qdrant suy ra cố định (UUID5): `backend/core/schema.py` hàm `point_id_for_chunk_id` [code]; test chạy lại ra đúng build record: `backend/tests/test_full_corpus_chunker.py` [code, đạt 30/10]
- 8.435 đoạn, 0 lỗi: build record `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` (05/11) [đã chạy]
- 12 cách cắt, 32 câu, cùng lượng chữ 750 token; số câu mất đáp án theo từng cách: `bao_cao_he_thong/03_BAO_CAO_CHIA_DOAN.md` §4 (Phase 8.1, 25/10) [đã chạy]
- Bảng "Món | Giá" là ví dụ tự đặt, không lấy từ kho.

</details>
