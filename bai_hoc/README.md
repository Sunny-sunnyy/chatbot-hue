# Bài học hue_rag — đọc theo thứ tự

*Cập nhật lần cuối: 10:19, ngày 11/11/2026 · đang viết liền bài 3–16 (anh chốt nhịp 11/11).*

Thư mục này là **bài học** để anh hiểu và kể lại được đồ án: chatbot làm gì, vì sao làm cách này, đo ra sao, còn yếu ở đâu. Bài viết theo kiểu: dễ hiểu, đủ nội dung, mỗi bài
một ý, nói "vì sao" trước, đi theo đúng hai giai đoạn của RAG, giữ đủ chi tiết kỹ thuật quan trọng. Mỗi bài chỉ dựa vào bài trước nó. Gần cuối mỗi bài
có một "chuyện thật": mình đã thử cách khác ra sao, vì sao giữ cách đang dùng.

Khác với `bao_cao_he_thong/`: đó là **sổ ghi việc** (quá khứ) của các agent, anh không cần đọc để hiểu.

Đầu mỗi bài có **Bảng từ**: tên dùng trong bài ↔ tên gốc tiếng Anh (như trong code / tài liệu) ↔ nghĩa ngắn. Từ anh chưa gặp ghi **mới**. Hình vẽ (mermaid)
chỉ có ở bài cần.

**Phần 1 — Đường RAG của hue_rag** (bám sơ đồ hai giai đoạn)

| Bài | Nội dung | Trạng thái |
|---|---|---|
| [0](00_HUE_RAG_TRONG_3_PHUT.md) | hue_rag trong 3 phút: người hướng dẫn viên tra sổ tay; hai giai đoạn; đoạn kể 3 phút | đã viết, chờ anh đọc |
| [1](01_KHO_DU_LIEU.md) | Cuốn sổ tay: kho dữ liệu | đã viết, chờ anh đọc |
| [2](02_CHUNKING.md) | Cắt sổ thành thẻ ghi chú: chunking | đã viết, chờ anh đọc |
| [3](03_METADATA.md) | Ghi tên lên góc thẻ: metadata | đã viết, chờ anh đọc |
| [4](04_EMBEDDING_VA_TU_KHOA.md) | Biến thẻ thành thứ tìm được: embedding và từ khoá | đã viết, chờ anh đọc |
| [5](05_QDRANT.md) | Cất hộp thẻ vào tủ: Qdrant | đã viết, chờ anh đọc |
| [6](06_RETRIEVAL.md) | Rút đúng thẻ: retrieval | đã viết, chờ anh đọc |
| 7 | Reranking: đã thử 3 cách, vì sao không dùng | chưa viết |
| 8 | Generation: lời dặn, ghi nguồn, câu từ chối, kiểm nguồn | chưa viết |

**Phần 2 — Đánh giá** (hai giai đoạn, như anh học của Ed Donner)

| Bài | Nội dung | Trạng thái |
|---|---|---|
| 9 | Bộ câu hỏi mẫu và bộ câu kín: vì sao cần, vì sao phải là câu người thật hỏi | chưa viết |
| 10 | Chấm bước tìm | chưa viết |
| 11 | Chấm câu trả lời; mức tối thiểu; tốc độ và tiền — mỗi số tốt tới đâu | chưa viết |

**Phần 3 — Từ chatbot thành trợ lý**

| Bài | Nội dung | Trạng thái |
|---|---|---|
| 12 | Vì sao cần trợ lý: xếp loại câu và công cụ | chưa viết |
| 13 | Tìm thêm và nhớ câu hỏi | chưa viết |
| 14 | Việc dễ nhầm thì code làm: ngày âm lịch, thời tiết, lịch trình | chưa viết |
| 15 | Tra web và hỏi bằng ảnh | chưa viết |
| 16 | Đoạn kể 2–3 phút bản đủ + chỗ còn yếu và hướng sửa | chưa viết |

Nhịp viết: bài 0–2 viết trước, chờ anh đọc. Anh thấy dễ hiểu thì mình viết liền tới bài 16, báo anh sau mỗi 2 bài. Anh góp ý lúc nào thì mình sửa lúc đó.
