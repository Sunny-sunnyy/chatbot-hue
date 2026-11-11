# Bài 2 — Chunking: cắt theo cấu trúc bài

*Cập nhật lần cuối: 09:40, ngày 11/11/2026 · bài mới.*

## Bảng từ — tên mình dùng và tên gốc

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Cắt đoạn | *chunking* | Chia bài thành đoạn nhỏ để tìm (anh đã biết). |
| Gối đầu | *overlap* | Hai đoạn liền nhau lặp lại một phần chữ ở chỗ nối (anh đã biết). |
| Token | *token* | Đơn vị chữ mà model đếm. Một từ tiếng Việt khoảng 1–2 token (anh đã biết). |
| Chỗ trống đưa người viết | *context budget* — **mới** | Tổng lượng chữ được phép đưa người viết cho một câu hỏi. Đoạn to thì vừa ít đoạn hơn. |

---

*Ở bài 1, kho là 204 bài Markdown soạn theo mẫu, mỗi câu "đọc riêng vẫn hiểu". Bài này kể bước tiếp theo trên sơ đồ: cắt bài thành đoạn.*

## Bản cơ bản làm gì, hue_rag làm gì

Trong bản cơ bản anh đã học, cách hay dùng là **cắt theo số ký tự**, ví dụ mỗi đoạn 500–1.000 ký tự và gối đầu một ít để không mất ý ở chỗ cắt. Cách này dễ, dùng
được cho mọi loại file. Điểm yếu của nó là hay cắt ngang một ý: nửa câu ở đoạn này, nửa câu ở đoạn kia, hoặc tên món ở một đoạn còn giá ở đoạn sau.

hue_rag **cắt theo cấu trúc của bài**:
- mỗi **đoạn văn** là một đoạn;
- mỗi **mục danh sách** là một đoạn;
- bảng ngắn để nguyên; bảng dài thì **mỗi dòng bảng là một đoạn, kèm dòng tiêu đề của bảng**;
- khối nào quá dài thì tách ở **ranh giới câu**, không tách giữa câu;
- **không gối đầu**.

Kết quả: 204 bài thành **8.435 đoạn**. Phần lớn đoạn ngắn, cỡ một hai câu.

Ví dụ tự đặt: một bảng giá có hai cột "Món | Giá". Cắt theo cấu trúc thì dòng "Bún bò | 40.000 đồng" thành một đoạn, và đoạn đó mang theo dòng tiêu đề
"Món | Giá". Nhờ vậy người viết biết 40.000 đồng là giá của món gì. Cắt theo số ký tự thì dòng tiêu đề có thể nằm ở đoạn khác.

## Vì sao cắt theo cấu trúc

Cách cắt này hợp với chính cách kho được viết. Bài 1 kể rằng kho được soạn sao cho **mỗi đoạn văn, mỗi dòng mang trọn một ý**. Khi người soạn đã đặt sẵn ranh
giới ý, cắt đúng theo ranh giới đó thì không bao giờ xé đôi một ý. Cũng vì vậy không cần gối đầu: gối đầu sinh ra để chữa chuyện cắt ngang ý, mà ở đây không
cắt ngang ý.

Còn một lý do nữa: đoạn nhỏ thì **10 đoạn đưa người viết trỏ được tới 10 chỗ khác nhau** trong kho. Lý do này quan trọng hơn ta tưởng, như chuyện dưới đây.

## Một chuyện thật: đoạn to tìm được nhiều hơn, nhưng lại tệ hơn

Trong đợt rà lại mọi lựa chọn cũ (cuối tháng 10), mình thử **12 cách cắt khác** trên 32 câu hỏi đã biết chắc đáp án nằm ở đâu trong kho. Ví dụ: gộp đoạn ngắn
thành đoạn 256, 384 hay 512 token; sau khi tìm thì mở rộng ra cả mục chứa đoạn đó; gộp các dòng bảng liền nhau.

Để so cho công bằng, mọi cách đều chỉ được dùng **cùng một chỗ trống** đưa người viết. Giống như xếp đồ vào cùng một chiếc vali: được mang 9 món nhỏ, hay 4 món
to. Nếu không giữ chung một cỡ vali, đoạn to sẽ "tự thắng" chỉ vì chở được nhiều chữ hơn.

Kết quả:
- Đoạn to quả thật **chứa được đáp án nhiều hơn**. Nhưng mỗi đoạn chiếm nhiều chỗ, nên chỉ khoảng 4–5 đoạn vừa vali, thay vì khoảng 9 đoạn nhỏ trỏ tới nhiều
  chỗ khác nhau.
- Tính ra, gộp tới 256–512 token **làm mất đáp án ở 4–6 trên 32 câu**. Mở rộng ra cả mục làm mất 8 câu. Gộp nhỏ (tới 128 token) và gộp dòng bảng thì **không
  khác** gì cách đang dùng.
- Không cách nào tốt hơn, nên **giữ cách cắt hiện tại**.

Cách để số này dễ đọc: 4–6 trên 32 câu là cứ khoảng 6 câu thì có 1 câu người viết không còn thấy đáp án. Đó là mức hỏng rõ. Còn "không khác" nghĩa là cùng một
câu tìm ra cùng đoạn đúng, nên đổi cũng không được gì.

Điều rút ra lớn hơn chuyện cắt đoạn: thứ giúp thật là **cho người viết thấy nhiều chỗ hơn**, không phải cho mỗi chỗ to hơn. Chính vì vậy về sau chatbot chuyển
từ 5 đoạn lên 10 đoạn (bài 0, chuyện thật).

## Khi nào hỏng

- **Bảng dài.** Mỗi dòng giá đứng riêng thành một đoạn rất ngắn, ít chữ, nên khi câu hỏi viết khác chữ thì bước tìm dễ trượt. Gốc của lỗi này nằm ở bước
  tìm (bài 6). Thử gộp dòng bảng không giúp.
- **Nhiều đoạn rất ngắn.** Gần 1.800 đoạn dưới 50 token (đếm trên kho cũ). Đoạn quá ngắn có ít chữ để tìm theo nghĩa. Thử gộp lại thì không giúp hoặc tệ hơn.
- **Số đo trên 32 câu là cỡ mẫu nhỏ.** Kết luận "đoạn to tệ hơn" đủ chắc vì chênh lệch rõ. Còn kết luận "gộp nhỏ không khác" chỉ có nghĩa là trên 32 câu này chưa thấy khác.

## Ba điều chính

1. hue_rag **cắt theo cấu trúc bài** (đoạn văn, mục danh sách, dòng bảng kèm tiêu đề), **không gối đầu**, vì kho đã được viết sẵn mỗi đoạn một ý.
2. Đã thử 12 cách cắt khác với **cùng một chỗ trống** đưa người viết. **Đoạn to tệ hơn**, vì vừa ít đoạn hơn nên người viết thấy ít chỗ hơn.
3. Điều giúp thật là **thấy nhiều chỗ hơn**. Từ đó dẫn tới quyết định đưa 10 đoạn.

## Bài sau

**Bài 3 — Metadata** *(sắp viết)*: mỗi đoạn mang theo tên bài và đường tiêu đề (ví dụ "Bún bò Huế > Quán nổi tiếng"). Đã thử bỏ đi thì mất đáp án ở 7–8 trên 32 câu.

<details>
<summary>Nguồn (anh không cần đọc)</summary>

- Cách cắt: `backend/ingestion/chunking/full_corpus_chunker.py` (bảng tách từng hàng kèm tiêu đề, danh sách tách từng mục, đoạn văn tách ở ranh giới câu) + `markdown_blocks.py` [code, theo sổ ghi việc 03]
- 8.435 đoạn từ 204 bài: build record `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` (05/11) [đã chạy]
- 12 cách cắt, 32 câu, cùng chỗ trống 750 token; gộp 256 / 384 / 512 mất 4 / 6 / 6 câu; mở rộng cả mục mất 8; tiền tố chỉ tiêu đề gần nhất / bỏ hẳn mất 7 / 8: `bao_cao_he_thong/03_BAO_CAO_CHIA_DOAN.md` §4 (Phase 8.1, 25/10) [đã chạy]
- 1.787 đoạn dưới 50 token: đếm 24/10 trên kho cũ, chưa đếm lại [đã chạy, số cũ]
- Bảng "Món | Giá" với "Bún bò | 40.000 đồng" là ví dụ tự đặt, không lấy từ kho.

</details>
