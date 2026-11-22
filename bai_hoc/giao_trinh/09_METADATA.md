# Bài 9 — Thông tin gắn kèm mỗi đoạn (metadata) và "chữ để tìm"

*Cập nhật 10:21, ngày 22/11/2026 · cơ chế đọc từ chương trình đang chạy; ví dụ lấy từ lượt hỏi thật ngày 21/11; số của phép so lấy từ báo cáo đo cuối tháng 10; người viết không chạy lại phép đo nào.*

**Bài trước đã biết:** 266 bài được cắt thành 9.458 đoạn nhỏ, phần lớn chỉ một hai câu.
**Bài này thêm:** một đoạn nhỏ đứng riêng thì không biết nó nói về cái gì. Bài này giảng những thông tin được gắn kèm mỗi đoạn, và chúng được dùng ở đâu.

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

Có thể gắn thêm nhiều trường nữa (chủ đề con, khu vực, mức giá…) rồi dùng chúng để lọc trước khi tìm, ví dụ "chỉ tìm trong nhóm món ăn". hue_rag không làm vậy: mọi câu hỏi đều tìm trên cả 9.458 đoạn.

Ví dụ chính cho thấy một hệ quả của lựa chọn này: câu hỏi về giá vé được trả lời bằng đoạn của hai bài vé **và** một đoạn của bài nghệ thuật biểu diễn. Nếu hệ thống lọc "chỉ tìm trong nhóm du lịch" (nhóm chứa các bài vé) thì đoạn số 4, nơi có giá vé trẻ em, đã không được xét.

Lựa chọn này là lập luận thiết kế, chưa có phép đo riêng so "có lọc" với "không lọc". Hai trường chủ đề con và thẻ phân loại được nghĩ tới lúc thiết kế hồ sơ nhưng bị loại ngay, vì chưa có chỗ nào dùng: mỗi trường thêm vào là một thứ phải giữ đúng mỗi lần sửa kho.

## Dễ nhầm

- **"Metadata là để lọc."** Ở hệ thống này thì không. Nó để đoạn tự nói được mình thuộc bài nào, mục nào, lúc tìm và lúc viết.
- **"Vector được tính từ thân đoạn."** Không. Nó được tính từ chữ để tìm, tức có cả tên bài và tên mục.
- **"Model viết nhìn thấy cả bài."** Không. Nó chỉ thấy từng khối: số nguồn, tên bài, tên mục, và mảnh bằng chứng.

## Những điều cần nhớ

- Mỗi đoạn mang tên bài và đường tiêu đề; đó là thứ làm một đoạn nhỏ tự đủ nghĩa.
- Dùng ở hai chỗ: trong chữ để tìm, và ở đầu mỗi khối đưa cho model viết.
- Hồ sơ của đoạn có đúng 7 trường.
- Không lọc theo chủ đề; mọi câu hỏi tìm trên cả kho.
- Thử bỏ tên bài và tên mục khỏi chữ để tìm: được 3–4 câu, mất 7–8 câu trên 32 câu, nên giữ.

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

## Vì sao không làm cách khác

**Vì sao không dùng model viết cho mỗi đoạn một câu tóm tắt bối cảnh rồi gắn vào?** Đã gọi thử ở giai đoạn đầu nhưng chưa từng lập thành chỉ mục và chưa đo; phần chương trình đó đã gỡ cuối tháng 10. Tên bài và đường tiêu đề lấy được ngay từ cấu trúc của bài, không tốn lần gọi model nào và không có rủi ro model viết sai bối cảnh.

**Vì sao không lọc theo chủ đề để tìm cho gọn?** Chưa đo. Lý do thiết kế ở trên: lọc sai một lần là mất đáp án, và ví dụ chính có một đoạn đúng nằm ở nhóm không ngờ tới.

## Chi tiết để tra

- Phép so làm ngày 25/10/2026, trên kho của thời điểm đó, lượng chữ 750 token (thời còn đưa 5 đoạn). Giá trị p sau hiệu chỉnh của hai cách: 0,457 và 0,317, tức chưa có ý nghĩa thống kê.
- Trong chữ để tìm, đường tiêu đề giữ nguyên số thứ tự của mục nếu bài có đánh số (như "6. Các dịch vụ…").
- Dòng "Giờ mở cửa, giá vé, lịch lễ hội có thể đã thay đổi…" được thêm khi câu trả lời trích một đoạn có trường nguồn thuộc nhóm vé, địa điểm, lễ hội, hoặc bài lưu trú (bài 21).

**Bài sau (bài 10):** chữ để tìm của 9.458 đoạn được đổi thành vector như thế nào.

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

</details>
