# Bài 3 — Ghi tên lên góc thẻ: metadata

*Cập nhật lần cuối: 10:16, ngày 11/11/2026 · bài mới.*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Thông tin kèm theo | **metadata** | Những gì đi kèm một đoạn ngoài chính khúc chữ: tên bài, mục, chủ đề, vị trí… |
| Tên bài | **title** | Tiêu đề lớn nhất của bài (dòng `# …`). |
| Đường tiêu đề — **mới** | **heading_path** | Chuỗi các tiêu đề con đứng trên đoạn, nối bằng " > ", ví dụ "Quán nổi tiếng > Buổi sáng". |
| Chữ để tìm — **mới** | **search_text** (code gọi kiểu này là *Representation A*) | Chữ thật sự được biến thành vector và chấm từ khoá: tên bài + đường tiêu đề + thân đoạn. |
| Hồ sơ cất kèm — **mới** | **payload** (Qdrant) | 7 trường cất cùng mỗi đoạn trong Qdrant, để khi tìm ra thì lấy lại được đủ thông tin. |
| Chủ đề | **domain** | Một trong 5 thư mục: `foods`, `heritages`, `festivals`, `performing_arts`, `travel`. |

---

*Bài 2 kể bài viết được cắt thành 8.435 thẻ ghi chú nhỏ. Bài này kể mỗi thẻ được ghi thêm gì ở góc, và vì sao chỉ vài chữ ở góc thẻ lại quan trọng.*

## Quay lại người hướng dẫn viên

Cắt cuốn sổ thành thẻ xong, người hướng dẫn viên gặp ngay một vấn đề. Rút ra một thẻ ghi "Mở cửa từ 6 giờ sáng, giá 40.000 đồng một tô", họ không biết thẻ này
thuộc trang nào. Quán nào? Món gì?

Nên trước khi bỏ thẻ vào hộp, họ **ghi ở góc mỗi thẻ**: thẻ này cắt từ trang nào, nằm dưới mục nào. Ví dụ "Bún bò Huế > Quán nổi tiếng". Nhờ vài chữ đó, thẻ
nào rút ra cũng tự nói được nó đang nói về cái gì. Lúc tìm, chữ ở góc thẻ cũng giúp họ nhận ra đúng thẻ nhanh hơn.

Metadata của hue_rag chính là chữ ở góc thẻ.

## Mỗi đoạn mang theo những gì

Khi cất vào Qdrant (bài 5), mỗi đoạn mang theo một **hồ sơ** đúng **7 trường**:

| Trường | Là gì | Dùng để làm gì |
|---|---|---|
| `search_text` | tên bài + đường tiêu đề + thân đoạn, ghép thành một khúc chữ | biến thành vector (bài 4) và chấm từ khoá lúc tìm (bài 6) |
| `title` | tên bài (dòng `#`) | đưa cho người viết, hiện ở dòng "Nguồn" |
| `heading_path` | đường tiêu đề con, ví dụ "Quán nổi tiếng > Buổi sáng" | đưa cho người viết để biết đoạn nằm ở mục nào |
| `evidence_parts` | các mảnh chữ làm nên đoạn, kèm vị trí đầu–cuối trong file (bài 2) | hiện "đoạn gốc" đúng từng chữ khi người dùng bấm nguồn |
| `source` | đường dẫn file của bài | biết đoạn thuộc bài nào; dùng cho dòng "thông tin có thể đã thay đổi" |
| `chunk_id` | mã đoạn `<file>#<số>` (bài 2) | gọi tên đoạn; mã cất trong Qdrant suy ra từ mã này |
| `domain` | chủ đề, lấy từ thư mục đầu của đường dẫn | biết đoạn thuộc món ăn, di tích, lễ hội, nghệ thuật hay du lịch |

Có hai chỗ metadata được dùng, và cả hai đều quan trọng.

**Một: lúc tìm.** Chữ được biến thành vector không phải thân đoạn trơn, mà là **chữ để tìm**:

```text
Bún bò Huế                      ← tên bài
Quán nổi tiếng > Buổi sáng      ← đường tiêu đề
Mở cửa từ 6 giờ sáng, giá …     ← thân đoạn
```

*(ví dụ tự đặt, không lấy từ kho)*

Nhờ vậy khi khách hỏi "bún bò ăn sáng ở đâu", đoạn này khớp cả theo nghĩa lẫn theo từ khoá, dù thân đoạn không hề có chữ "bún bò".

**Hai: lúc viết.** Mỗi đoạn đưa cho người viết được trình bày thành một khối có nhãn:

```text
[Nguồn 3]
Tiêu đề: Bún bò Huế
Mục: Quán nổi tiếng > Buổi sáng
Bằng chứng:
- Mở cửa từ 6 giờ sáng, giá …
```

Người viết đọc là biết ngay đoạn này nói về món gì, ở mục nào, và phải ghi số nguồn nào nếu dùng nó.

## Vì sao chỉ giữ 7 trường

Có thể gắn thêm nhiều thứ nữa: chủ đề con, thẻ phân loại, quận, mức giá… và dùng chúng để **lọc** khi tìm (ví dụ chỉ tìm trong món ăn). hue_rag cố ý **không
làm**. Các trường như chủ đề con và thẻ phân loại đã bị bỏ vì không có chỗ nào dùng tới. Chatbot cũng không lọc theo chủ đề khi tìm. Lý do: câu hỏi của khách
hay chạm nhiều chủ đề cùng lúc ("đi Đại Nội xong ăn gì gần đó"), lọc sai một lần là mất đáp án. Bước tìm theo nghĩa và theo từ khoá, cộng với tên bài và tiêu đề
nằm sẵn trong chữ để tìm, đã đủ để tìm đúng chủ đề mà không cần lọc.

Mỗi trường thêm vào là một thứ phải giữ đúng mỗi lần sửa kho. Nên chỉ giữ thứ có chỗ dùng thật.

## Một chuyện thật: bỏ chữ ở góc thẻ thì sao

Cuối tháng 10, trong đợt rà lại mọi lựa chọn cũ, mình thử hai cách đơn giản hơn cho chữ để tìm, trên cùng 32 câu hỏi đã biết chắc đáp án nằm ở đâu:
- **chỉ giữ tiêu đề gần nhất** (bỏ tên bài và các tiêu đề cấp trên);
- **bỏ hẳn**, chỉ còn thân đoạn.

Luật ghi trước khi chạy: cách mới chỉ được nhận nếu **không làm câu nào mất đáp án**. Kết quả, so với cách đang dùng:

| Cách thử | Câu tốt lên | Câu như cũ | Câu mất đáp án |
|---|---:|---:|---:|
| Chỉ giữ tiêu đề gần nhất | 4 | 21 | 7 |
| Bỏ hẳn | 3 | 21 | 8 |

Đọc bảng này thế nào cho đúng:
- **Có câu tốt lên.** Bỏ bớt chữ ở góc thẻ đôi khi giúp vì đoạn ngắn hơn, nghĩa của thân đoạn nổi rõ hơn. Không nên kể là "bỏ đi thì tệ hẳn".
- **Nhưng số câu mất gấp đôi số câu tốt lên**, và luật là không được làm mất câu nào. Nên cả hai cách bị loại, giữ cách đang dùng.
- **Độ chắc:** với 32 câu, chênh lệch này chưa đủ để phép thử thống kê khẳng định là thật. Cách nói đúng: "thử bỏ thì mất nhiều câu hơn được, nên giữ", chứ
  không phải "đã chứng minh tên bài giúp tìm tốt hơn".

Báo cáo đợt đó giải thích các câu bị mất: thiếu tên bài và tiêu đề thì đoạn mất ngữ cảnh "đang nói về cái gì", y như tấm thẻ không ghi góc.

## Khi nào hỏng

- **Bài có tiêu đề nghèo hoặc đặt sai** thì đoạn mang nhãn kém, khó tìm. Đây là lý do mẫu bài (bài 1) quy định các mục cố định cho từng chủ đề.
- **Đoạn rất ngắn:** tên bài và tiêu đề chiếm phần lớn chữ để tìm. Mọi đoạn trong cùng một bài lại có chung tên bài, nên chúng trông giống nhau, khó phân biệt
  đoạn nào đúng.
- **Không lọc được theo chủ đề.** Chatbot không có cách "chỉ tìm trong lễ hội". Đây là lựa chọn có chủ đích, nhưng nếu sau này cần lọc thì phải thêm.
- **Mã đoạn dồn số khi sửa giữa bài** (bài 2): hồ sơ vẫn đúng sau khi chuẩn bị lại, chỉ khó so "trước và sau" theo mã.

## Ba điều chính

1. Mỗi đoạn mang **7 trường**, quan trọng nhất là **tên bài + đường tiêu đề**. Đó là chữ ở góc thẻ giúp đoạn tự nói "tôi đang nói về cái gì".
2. Metadata dùng ở **hai chỗ**: nằm trong **chữ để tìm** (giúp tìm đúng) và trong **khối đưa người viết** (giúp hiểu đúng, ghi nguồn đúng).
3. Thử bỏ tên bài và tiêu đề: **3–4 câu tốt lên nhưng 7–8 câu mất đáp án**, nên giữ. Chỉ giữ trường có chỗ dùng thật, **không lọc theo chủ đề**.

**Bài sau:** Bài 4 — Biến thẻ thành thứ tìm được (embedding và từ khoá): model nhỏ e5-small chạy ngay trên máy, cộng thêm BM25, và vì sao model lớn hơn lại thua.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Chữ để tìm = tên bài + đường tiêu đề (" > ") + phần bằng chứng: `backend/ingestion/chunking/full_corpus_chunker.py` hàm `build_representation_a_search_text` [code, xem 11/11]
- Hồ sơ 7 trường: `backend/core/schema.py` hàm `to_qdrant_payload`; `domain` từ hàm `domain_for_source`; build record ghi `full_corpus_qdrant_payload:v2`, 8.435 điểm [code + đã đọc 11/11]
- Khối đưa người viết "[Nguồn n] / Tiêu đề / Mục / Bằng chứng": `backend/retrieval/full_corpus_context.py` hàm `_block` [code, xem 11/11]
- Bỏ chủ đề con / thẻ phân loại vì không ai dùng; không lọc theo trường: `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` thẻ N2-16; spec metadata v2 (29/09) [tài liệu]
- Thí nghiệm tiền tố (25/10, 32 câu, 750 token): chỉ tiêu đề gần nhất 4 / 21 / 7, bỏ hẳn 3 / 21 / 8; p Holm 0,457 và 0,317 (chưa có ý nghĩa thống kê): `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g3_implementation.md` §3.5 [đã chạy]. Cách "chỉ tiêu đề gần nhất" bỏ cả tên bài: `backend/experiments/phase_8_1/g3_chunking.py` hàm `with_prefix` [code]
- Lý do không lọc theo chủ đề (câu hỏi chạm nhiều chủ đề) là suy luận của mình từ thiết kế, chưa có thí nghiệm riêng.
- Các khối "Bún bò Huế / Quán nổi tiếng > Buổi sáng" là ví dụ tự đặt.

</details>
