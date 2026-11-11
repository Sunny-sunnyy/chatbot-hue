# Bài học hue_rag — đọc theo thứ tự

*Cập nhật lần cuối: 10:36, ngày 11/11/2026 · đủ 17 bài (0–16), chờ anh đọc dần và góp ý.*

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
| [7](07_RERANKING.md) | Xếp lại thẻ: reranking (đã thử, không dùng) | đã viết, chờ anh đọc |
| [8](08_GENERATION.md) | Đọc thẻ rồi trả lời: generation | đã viết, chờ anh đọc |

**Phần 2 — Đánh giá** (hai giai đoạn, như anh học của Ed Donner)

| Bài | Nội dung | Trạng thái |
|---|---|---|
| [9](09_BO_CAU_HOI_MAU.md) | Đề kiểm tra: bộ câu hỏi mẫu | đã viết, chờ anh đọc |
| [10](10_CHAM_BUOC_TIM.md) | Chấm bước tìm | đã viết, chờ anh đọc |
| [11](11_CHAM_CAU_TRA_LOI.md) | Chấm câu trả lời, và mỗi con số tốt tới đâu | đã viết, chờ anh đọc |

**Phần 3 — Từ chatbot thành trợ lý**

| Bài | Nội dung | Trạng thái |
|---|---|---|
| [12](12_VI_SAO_CAN_TRO_LY.md) | Từ chatbot thành trợ lý: xếp loại câu và công cụ | đã viết, chờ anh đọc |
| [13](13_TIM_THEM_VA_NHO_CAU_HOI.md) | Rút thêm thẻ và nhớ câu hỏi | đã viết, chờ anh đọc |
| [14](14_VIEC_DE_NHAM_THI_CODE_LAM.md) | Việc dễ nhầm thì code làm: ngày âm lịch, thời tiết, lịch trình | đã viết, chờ anh đọc |
| [15](15_TRA_WEB_VA_HOI_BANG_ANH.md) | Khi sổ không có: tra web, và hỏi bằng ảnh | đã viết, chờ anh đọc |
| [16](16_KE_DO_AN_VA_CHO_CON_YEU.md) | Kể đồ án trong 2–3 phút, và chỗ còn yếu | đã viết, chờ anh đọc |

Nhịp: đã viết đủ 17 bài (11/11). Anh đọc dần theo số, góp ý lúc nào thì mình sửa lúc đó; thấy câu nào sai thì mình sửa ngay và ghi ở mục Nguồn của bài.
