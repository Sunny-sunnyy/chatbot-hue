# Hướng dẫn viết câu hỏi Golden full-corpus

Áp dụng cho mọi file `golden_full_corpus_authoring.jsonl`. Nguồn quy tắc:
spec Phase 7A §3–§6. Bản này là bản pilot `heritages`, chờ User xác nhận.

## Quy tắc

1. **Đọc hết các file `.md` của partition trước khi viết.** Mọi ý trong
   `reference_answer` phải tìm thấy trong file ghi ở `sources`.
2. **Mỗi câu chỉ có một đáp án khách quan.** Không viết câu xin lời khuyên hay
   phụ thuộc sở thích ("nên đi lăng nào", "quán nào ngon"), kể cả khi corpus có
   viết gợi ý.
3. **Giọng người thật hỏi:** du khách hoặc người thích tìm hiểu văn hóa, lịch
   sử. Câu ngắn đến vừa, có dấu, đúng chính tả. Mỗi câu chỉ hỏi một ý chính. Không
   viết "theo tài liệu", "hãy cho biết". Không chép nguyên tiêu đề mục làm câu
   hỏi.
4. **Tên gọi khác** (khoảng 10% số câu) chỉ dùng khi corpus xác nhận đó là cùng
   một thực thể, ví dụ Khiêm Lăng là lăng Tự Đức, Điện Huệ Nam là Điện Hòn Chén.
5. **Không dùng dữ kiện mà corpus tự mâu thuẫn.** Danh sách mâu thuẫn đã biết
   nằm ở `knowledge-base-hue/meta/corpus-contradictions-2026-10-23.md`; không
   dùng các dữ kiện trong đó. Nếu gặp mâu thuẫn mới, ghi vào report để người
   duyệt quyết định.
6. **Nhãn category:**
   - `direct_fact`: dữ kiện nằm trong một đoạn.
   - `multi_source`: phải ghép thông tin từ ít nhất 2 đoạn hoặc 2 file, và không
     đoạn nào tự trả lời đủ. `sources` liệt kê đủ các file.
   - `comparative`: so sánh thật hai thực thể theo một tiêu chí (hơn/kém,
     trước/sau, giống/khác). Câu chỉ hỏi hai dữ kiện riêng rẽ thì không phải
     `comparative`.
   - `conditional`: đáp án có điều kiện, quy định hoặc ngoại lệ; phải nêu đủ
     điều kiện.
   - `out_of_scope`: thực thể hoặc thông tin vắng mặt trong corpus. Trước khi
     đưa vào, tìm text trên toàn bộ 205 file. Case loại này có `keywords: []`,
     `sources: []` và `reference_answer` đúng bằng câu `INSUFFICIENT_ANSWER`.
7. **Keywords:**
   - Mỗi keyword là chuỗi nguyên văn trong corpus, phân biệt dấu và hoa thường.
   - Cần ít nhất 1 keyword mang đáp án: không có trong câu hỏi nhưng có trong
     `reference_answer`.
   - Được thêm tên thực thể trung tâm.
   - Không dùng từ chung chung.
   - Không chọn keyword là chuỗi con của một thực thể khác. Ví dụ "Quốc gia I"
     nằm trong "Quốc gia IV" nên không dùng.
   - Keyword dạng số phải đủ đặc thù để không khớp nhầm đoạn khác: lấy chuỗi
     nguyên văn dài hơn có kèm ngữ cảnh (ví dụ "trung tâm thành phố khoảng
     10 km" thay vì "10 km"), hoặc đi cùng tên thực thể trong `keywords`.
8. **Ưu tiên câu có đáp án nằm trong bảng** (giá vé, giờ mở cửa, lịch) khi
   corpus có bảng phù hợp. Đây không phải quota.

## Mẫu `reference_answer`

Chỉ trả lời đúng điều câu hỏi hỏi, cộng điều kiện hoặc ngoại lệ bắt buộc nếu
có. Không thêm dữ kiện phụ, và không thêm mốc thời gian nếu câu hỏi không hỏi.
Lý do: ở Phase 7B, Completeness chấm theo reference, nên reference thừa ý sẽ
làm câu trả lời đúng mà ngắn bị trừ điểm oan.

- Thường chỉ cần một câu.
- Câu có/không: mở đầu bằng "Có." hoặc "Không." rồi nêu đúng ý quyết định.
- `conditional`: nêu đủ điều kiện, nhưng chỉ những điều kiện liên quan tới câu
  hỏi.
- `comparative`: nêu kết luận so sánh, kèm hai giá trị được so.
- Mọi chi tiết phải lấy từ `sources`.

## 5 ví dụ tốt (từ pilot)

| Câu hỏi | Vì sao tốt |
|---|---|
| Lăng Khải Định có tất cả bao nhiêu bậc thang? | Một dữ kiện, một đáp án (127 bậc). Keyword mang đáp án không có trong câu hỏi. |
| Người Việt Nam 65 tuổi đi tham quan Đại Nội có được giảm giá vé không? | `conditional` thật: người hỏi phải biết điều kiện "từ 60 tuổi trở lên" và cách xuất trình giấy tờ. |
| Văn bia ở lăng Gia Long và lăng Minh Mạng do vị vua nào soạn? | `multi_source` thật: mỗi file chỉ chứa một nửa đáp án. |
| Tấm bia Khiêm Cung Ký ở Khiêm Lăng nặng khoảng bao nhiêu? | Dùng tên gọi khác (Khiêm Lăng) mà corpus đã xác nhận. |
| Vé combo 4 điểm gồm Đại Nội và ba lăng Minh Mạng, Tự Đức, Khải Định giá bao nhiêu cho người lớn? | Đáp án nằm trong bảng; `reference_answer` chỉ nêu giá người lớn. |

## 6 ví dụ xấu đã loại hoặc sửa trong pilot

| Bản nháp | Vấn đề | Cách xử lý |
|---|---|---|
| Đàn Nam Giao gồm mấy tầng và mỗi tầng tượng trưng cho gì? | Lồng hai câu hỏi. | Sửa thành "Ba tầng của Đàn Nam Giao tượng trưng cho những gì?" |
| Ba nhà hát cung đình của Huế xưa là những nhà hát nào? (nhãn `multi_source`) | Một đoạn ở file Cung An Định đã liệt kê đủ cả ba, nên không cần 2 nguồn. | Loại. Nếu giữ thì phải gán `direct_fact`. |
| Du khách có được đi qua cửa giữa Đại Hồng Môn ở lăng Minh Mạng không? | Corpus không nói quy định cho du khách, nên đáp án phải suy diễn. | Loại. |
| Lăng Thiệu Trị có phải là lăng vua duy nhất quay hướng Tây Bắc không? | Corpus mâu thuẫn: file lăng Dục Đức cũng ghi hướng Tây Bắc. | Loại; ghi mâu thuẫn vào report. |
| Mộc bản và Châu bản triều Nguyễn hiện lưu giữ ở đâu? (keyword "Trung tâm Lưu trữ Quốc gia I") | Keyword là chuỗi con của "Quốc gia IV". File Quần thể có đủ đáp án trong một câu, nên cũng không phải `multi_source`. | Loại. |
| Ai đã cho dựng chùa Thiên Mụ? → "Chùa Thiên Mụ do chúa Tiên Nguyễn Hoàng cho dựng vào năm 1601 trên đồi Hà Khê, bên bờ sông Hương." | Đáp án thừa ý: câu hỏi chỉ hỏi "ai", nhưng reference thêm năm và địa điểm. Câu trả lời đúng mà ngắn sẽ bị trừ Completeness oan. | Sửa thành "Chùa Thiên Mụ do chúa Tiên Nguyễn Hoàng cho dựng." và bỏ keyword `1601`. |
