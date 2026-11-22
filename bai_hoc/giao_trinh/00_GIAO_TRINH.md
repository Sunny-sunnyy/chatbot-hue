# Giáo trình hue_rag: hiểu cả hệ thống từ đầu, không cần đọc code

*Cập nhật 10:05, ngày 22/11/2026 · mục lục và khuôn bài chốt sau khi anh trả lời bốn câu hỏi sáng 22/11 · đã viết 3 bài mẫu (bài 2, 10, 21), mỗi bài đã qua một lượt đối chiếu độc lập với chương trình và số đo; các bài còn lại viết theo từng chặng · mọi con số trong bộ này lấy từ hệ thống đang chạy và các phép đo đã ghi, không có phép thử mới.*

**Bộ này cho ai.** Cho anh, người sẽ tự chạy thử, tự trình bày và tự trả lời câu hỏi về đồ án. Không cần đọc code. Biết dùng một chatbot là đủ để bắt đầu.

**Đọc thế nào.** Đọc theo đúng số thứ tự: bài sau dựa trên bài trước, khái niệm mới luôn được giảng trước khi dùng. Mỗi bài chia hai nửa:

- **Nửa để hiểu** (từ đầu bài tới mục "Những điều cần nhớ"): đọc lần đầu chỉ cần nửa này.
- **Nửa để tra** (từ mục "Cấu hình đang chạy" trở xuống): model nào, tham số nào, đã thử phương án nào, ra số bao nhiêu, hỏng ở đâu. Không cần đọc để hiểu bài, nhưng đây là chỗ trả lời các câu "cụ thể là bao nhiêu" và "vì sao không làm cách khác".

**Con số của hệ thống trong bộ này** (số bài, số đoạn, tính năng nào đang mở) là số lúc bài được viết, ghi ở dòng cập nhật của từng bài. Hệ thống vẫn đang được làm tiếp nên vài con số có thể đã lớn hơn khi anh đọc; cách hoạt động thì không đổi theo.

**Năm ví dụ dùng suốt cả bộ** (đều là lượt chạy thật qua hệ thống):

| Ví dụ | Người dùng gõ / chọn | Dùng để giảng |
|---|---|---|
| **Ví dụ chính** | *"Giá vé tham quan Đại Nội Huế là bao nhiêu?"* | đường đi bình thường của một câu hỏi: tìm ra 10 đoạn, model viết, có 5 nguồn |
| **Ví dụ "kho không có"** | *"Chùa Thiên Mụ có chỗ đậu ô tô không?"* | kho không nói tới thì hệ thống từ chối thay vì đoán, rồi tra web ở một mục riêng |
| **Ví dụ "phải tìm thêm"** | *"Mặc áo dài vào Đại Nội có được miễn vé không?"* | lần tìm đầu chưa đủ, trợ lý tự tìm thêm hai lần rồi mới trả lời |
| **Ví dụ "kho có mà tìm không ra"** | *"Vào chùa ở Huế có phải cởi giày không?"* | giới hạn của bước tìm: kho có một câu trả lời nhưng ba lần tìm đều không lấy ra |
| **Ví dụ lập lịch** | trang Lên kế hoạch: 3 ngày, 2 người lớn, thích di tích | chương trình xếp 11 điểm vào 3 ngày, model chỉ viết câu mô tả |

## Đường chính: chín chặng

Cột cuối: ✅ đã viết · ⬜ chưa viết.

### Chặng 0 — Nền: vì sao phải xây cả một hệ thống quanh model?

| Số | Bài | |
|---|---|---|
| 1 | Model ngôn ngữ là gì, và vì sao nó viết trôi chảy mà vẫn sai | ⬜ |
| 2 | [RAG là gì: cho model đọc tài liệu trước khi trả lời](02_RAG_LA_GI.md) | ✅ |
| 3 | Trợ lý và công cụ: model chỉ "xin", chương trình mới là thứ chạy | ⬜ |

### Chặng 1 — Bức tranh: hệ thống này làm gì, cho ai, gồm những khối nào?

| Số | Bài | |
|---|---|---|
| 4 | Bài toán: ai dùng, hỏi gì, nhận gì, và những thứ cố ý không làm | ⬜ |
| 5 | Người dùng thấy gì: các trang của ứng dụng | ⬜ |
| 6 | Kiến trúc: các khối, công nghệ, và đường đi của một câu hỏi | ⬜ |

### Chặng 2 — Chuẩn bị kho: làm một lần, trước khi có câu hỏi nào

| Số | Bài | |
|---|---|---|
| 7 | Kho dữ liệu: 266 bài viết về Huế, ai soạn, lấy từ đâu, kiểm thế nào | ⬜ |
| 8 | Cắt bài thành đoạn (chunking) | ⬜ |
| 9 | Thông tin gắn kèm mỗi đoạn (metadata) và "chữ để tìm" | ⬜ |
| 10 | [Biến mỗi đoạn thành một dãy số mang nghĩa: embedding](10_EMBEDDING.md) | ✅ |
| 11 | Tìm theo chữ trùng: từ khoá BM25 | ⬜ |
| 12 | Cất vào Qdrant, cập nhật khi kho đổi, và vì sao hệ thống không chịu chạy khi kho lệch chỉ mục | ⬜ |

### Chặng 3 — Trả lời một câu hỏi: mỗi lần người dùng gõ

| Số | Bài | |
|---|---|---|
| 13 | Tìm: lấy 30 ứng viên, trộn hai bảng xếp hạng, giữ 10 đoạn | ⬜ |
| 14 | Xếp lại bằng model (reranking): đã thử ba cách, không dùng | ⬜ |
| 15 | Viết câu trả lời: lời dặn, ngữ cảnh 10 đoạn, và số nguồn [n] | ⬜ |
| 16 | Kiểm nguồn bằng chương trình, và câu từ chối cố định | ⬜ |

### Chặng 4 — Vì sao tin được: đo

| Số | Bài | |
|---|---|---|
| 17 | Bộ 176 câu hỏi mẫu: đề kiểm tra của hệ thống | ⬜ |
| 18 | Chấm bước tìm: đoạn đúng có lọt vào 10 đoạn không | ⬜ |
| 19 | Chấm câu trả lời: ba thang điểm, người chấm là model, và nhiễu | ⬜ |
| 20 | Một thí nghiệm được làm thế nào, và nhìn cả bảng các lần so sánh thấy gì | ⬜ |

### Chặng 5 — Trợ lý hỏi đáp: khi tìm một lần rồi viết là chưa đủ

| Số | Bài | |
|---|---|---|
| 21 | [Harness: phần chương trình bao quanh model](21_HARNESS.md) | ✅ |
| 22 | Xếp loại câu trước khi tìm: bốn tuyến | ⬜ |
| 23 | Tìm thêm, nhớ câu hỏi trước, và câu hỏi nhiều ý | ⬜ |
| 24 | Việc phải đúng thì chương trình tính: ngày âm lịch làm mẫu, rồi thời tiết, khoảng cách và các công cụ khác | ⬜ |
| 25 | Khi kho không có: tra web một lần, để riêng mục "chưa kiểm" | ⬜ |
| 26 | Hỏi bằng ảnh | ⬜ |

### Chặng 6 — Lên kế hoạch: chương trình xếp lịch, model chỉ diễn đạt

| Số | Bài | |
|---|---|---|
| 27 | Trang Lên kế hoạch: từ mấy nút chọn tới một lịch, và bảng điểm tham quan đứng sau | ⬜ |
| 28 | Chương trình xếp lịch theo luật nào: một lịch thật được xếp từng bước | ⬜ |
| 29 | Khi không xếp được, bước kiểm lịch, và phần việc của model | ⬜ |
| 30 | Quanh một lịch: chỗ ở, quán ăn, ảnh, bản đồ, xuất file | ⬜ |
| 31 | Sửa lịch bằng lời: model hiểu ý, chương trình áp và kiểm | ⬜ |
| 32 | Đo một trợ lý: hội thoại nhiều lượt, người dùng mô phỏng, kịch bản chạy lặp | ⬜ |

### Chặng 7 — Máy móc bên dưới

| Số | Bài | |
|---|---|---|
| 33 | Model viết, mức suy luận, và đổi model bằng một dòng cấu hình | ⬜ |
| 34 | Người dùng chờ bao lâu, một câu tốn bao nhiêu tiền | ⬜ |
| 35 | Trang web và máy chủ: ai gửi gì cho ai | ⬜ |
| 36 | Bật hệ thống trên máy, và đóng gói bằng Docker | ⬜ |
| 37 | An toàn: khoá bí mật, dữ liệu người dùng, và chữ lạ chen vào lời dặn | ⬜ |
| 38 | Bộ test: chương trình tự kiểm những gì | ⬜ |

### Chặng 8 — Nhìn lại

| Số | Bài | |
|---|---|---|
| 39 | Đồ án được làm thế nào: một người quyết định và nhiều coding agent | ⬜ |
| 40 | Làm được tới đâu, còn yếu ở đâu, hướng phát triển | ⬜ |
| 41 | Kể lại toàn bộ trong một phút, trong năm phút, và kịch bản chạy thử | ⬜ |

## Phụ lục để tra (viết sau khi đường chính đủ)

| | Phụ lục | |
|---|---|---|
| A | Mọi tham số cấu hình: giá trị đang chạy, dùng để làm gì, bài nào giảng | ⬜ |
| B | Mọi tính năng đang mở và đang tắt: làm gì, một con số, vì sao | ⬜ |
| C | Sổ mọi phép so sánh đã làm, kể cả phương án bị bỏ; mỗi phép so chỉ có số ở một nơi | ⬜ |
| D | Lời dặn gửi model và mô tả từng công cụ, chép nguyên văn từ chương trình | ⬜ |
| E | Thuật ngữ Việt – Anh | ⬜ |
| F | Các con số chính trên một trang | ⬜ |

## Khuôn của mỗi bài

**Nửa để hiểu**

1. **Tên bài** là một câu hỏi hoặc một câu khẳng định.
2. **Dòng cập nhật:** viết lúc nào, số lấy từ đâu.
3. **Nối mạch:** "Bài trước đã biết… Bài này thêm…".
4. **Ý chính:** 3–5 gạch; đọc riêng mục này cũng nắm được bài.
5. **Từ dùng trong bài:** chỉ các từ mới của bài; tên dùng trong bài · tên gốc tiếng Anh · nghĩa.
6. **Thân bài:** 3–5 mục, tên mỗi mục là một câu khẳng định (đọc riêng các tên mục là ra dàn ý của bài). Nói thẳng cơ chế, không dùng ẩn dụ; ví dụ lấy từ lượt chạy thật; mỗi hình tối đa 6 ô.
7. **Dễ nhầm:** 1–3 câu người mới hay nói, kèm câu sửa.
8. **Những điều cần nhớ:** 3–5 câu.

**Nửa để tra** (bài nào có mục nào thì ghi mục đó; bài nền thường chỉ có hai mục cuối)

9. **Cấu hình đang chạy:** bảng mục · giá trị · dùng để làm gì và vì sao là giá trị đó · đã thử giá trị khác chưa.
10. **Đã so:** vấn đề thật đã gặp · so cái gì với cái gì, trên bộ câu nào · bảng kết quả kể cả phương án bị bỏ · đọc bảng thế nào · đã chọn gì · giới hạn của phép đo. Mỗi con số ghi rõ đo với model viết nào.
    Bài nào giảng lời dặn thì có thêm bảng **lời dặn**: từng phần, một câu nguyên văn.
11. **Giới hạn đã biết:** khi nào hỏng, người dùng thấy gì.
12. **Vì sao không làm cách khác:** vài câu người ngoài hay đặt ra về một thiết kế khác, trả lời thẳng, mở bằng "Đã đo", "Chưa thử" hoặc "Quyết định đã ghi".
13. **Chi tiết để tra:** con số phụ, ngoại lệ, ngày đo.
14. **Bài sau.**
15. **Nguồn** (thu gọn, anh không cần đọc): mỗi con số và mỗi khẳng định trỏ về file code hoặc file số đo.

Luật viết: thân bài không có tên file, tên hàm, mã bản code, ngày giờ phép thử, tên phiên làm việc. Mỗi chữ "vì" trong bài phải có căn cứ ở code, ở số đo hoặc ở một quyết định đã ghi; không có thì viết "chưa rõ vì sao". Mỗi con số đi kèm thứ nó đếm và mốc để so.

## Bộ bài cũ

Bộ 27 bài ở thư mục [`bai_hoc/`](../README.md) giữ nguyên để tra cho tới khi đường chính của giáo trình đủ. Việc mới xong trong lúc giáo trình đang viết vẫn được ghi ở [Việc mới xong](../VIEC_MOI_XONG.md).

<details>
<summary>Nguồn (để giữ trang đúng — anh không cần đọc)</summary>

- Bốn câu anh trả lời sáng 22/11/2026 (mức nền: ba bài nền ngắn · bốn chỗ vướng của bộ cũ: không ghép được bức tranh, quá nhiều chi tiết thi công, thiếu cấu hình và kết quả so sánh, ẩn dụ che cơ chế · nhịp giao: viết tiếp theo chặng · bài mẫu thứ ba: harness): ghi chép riêng của phiên viết giáo trình.
- Năm ví dụ: sổ ghi từng lượt của hệ thống trên máy phát triển, các ngày 20–21/11/2026 [đã chạy; người viết không chạy lại]; bản sao riêng tư ở `data/hoc_cung_D/vi_du_*_vet.json`. "Kho không nói về chỗ đậu xe ở chùa Thiên Mụ": dò bằng `scripts/grep_kb.sh` ngày 22/11/2026. "Kho có câu về giày dép": biên bản kiểm độc lập `data/hoc_cung_D/kiem/bai_02_10.md`.
- Model viết: hệ thống đang chạy Claude Sonnet 5.5 (đổi tạm từ 21/11/2026); phần lớn phép so cũ đo với gpt-6-luna. Mỗi bài ghi rõ con số nào đo với model nào.
- Luật nội dung: `session_prompt/WORKFLOW.md` mục 6 và mục 10.

</details>
