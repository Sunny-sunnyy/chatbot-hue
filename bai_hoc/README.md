# Bài học hue_rag — đọc theo thứ tự

*Cập nhật lần cuối: 20:35, ngày 14/11/2026 · bài 22 thêm lần ghi kho 6 (16 bài lễ hội / nghệ thuật), bài 01 kho nay 263 · Trước: 19:45, ngày 14/11/2026 · bài 22 thêm lần ghi kho 5 (23 bài: 10 món, 13 địa điểm / di tích — chỉ viết chỗ trợ lý từ chối / trả lời mỏng), bài 01 kho nay 247 · Trước: 18:55, ngày 14/11/2026 · bài 24 thêm ảnh tối 14/11 (218 / 224 bài, hiện cạnh câu trả lời 169), bài 25 thêm khách sạn theo hạng + ảnh, ảnh quán, quán đã đóng, năm trong câu hỏi; đã sửa theo kiểm độc lập · Trước: 18:06, ngày 14/11/2026 · bài 22 thêm lần ghi kho 4 (tám quán ăn; bữa có quán trong sổ ở lịch 49,3 ⇒ 69,1 %), đã sửa theo kiểm độc lập; bài 01 kho nay 224 bài · Trước: 17:14, ngày 14/11/2026 · bài 25 thêm quán ăn, khu ở theo buổi tối, lịch mẫu, so tiền mục web; bài 19 thêm dòng 38–42 · bài 22 thêm lần ghi kho 3, bài 24 / 25 thêm ảnh chiều 14/11 (184 / 216) · đủ 26 bài (0–25); thêm bài 25 cho bốn việc xong chiều 14/11 (sửa lịch bằng lời, câu hỏi nhiều ý, chỗ ở trong lịch, ảnh dưới câu trả lời); sửa bài 23, 24 theo giao diện chiều 14/11 (lịch mẫu, sông qua từng điểm, "Huế qua các thời kỳ", bỏ ghi công). Bài 22–24 đã sửa theo một lượt kiểm độc lập (5 câu sai, 14 chỗ dễ hiểu nhầm — ghi ở Nguồn từng bài).*

Thư mục này là **bài học** để anh hiểu và kể lại được đồ án: chatbot làm gì, vì sao làm cách này, đo ra sao, còn yếu ở đâu. Bài viết theo kiểu: dễ hiểu, đủ nội dung, mỗi bài
một ý, nói "vì sao" trước, đi theo đúng hai giai đoạn của RAG, giữ đủ chi tiết kỹ thuật quan trọng. Mỗi bài chỉ dựa vào bài trước nó. Gần cuối mỗi bài
có một "chuyện thật": mình đã thử cách khác ra sao, vì sao giữ cách đang dùng.

Khác với `bao_cao_he_thong/`: đó là **sổ ghi việc** (quá khứ) của các agent, anh không cần đọc để hiểu.

Đầu mỗi bài có **Bảng từ**: tên dùng trong bài ↔ tên gốc tiếng Anh (như trong code / tài liệu) ↔ nghĩa ngắn. Từ anh chưa gặp ghi **mới**. Hình vẽ (mermaid)
chỉ có ở bài cần.

**Phần 1 — Đường RAG của hue_rag** (bám sơ đồ hai giai đoạn)

| Bài | Nội dung | Trạng thái |
|---|---|---|
| [0](00_HUE_RAG_TRONG_3_PHUT.md) | hue_rag trong 3 phút: người hướng dẫn viên tra sổ tay; hai giai đoạn; đoạn kể 3 phút | đã sửa 13/11 — số từ chối nhầm mới, câu "0 câu ngoài kho bị trả lời" nói đúng 3 chỗ phạm sàn |
| [1](01_KHO_DU_LIEU.md) | Cuốn sổ tay: kho dữ liệu | thêm ghi chú 14/11 — kho nay 263 bài (bài 22) |
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
| [11](11_CHAM_CAU_TRA_LOI.md) | Chấm câu trả lời, và mỗi con số tốt tới đâu | đã sửa 13/11 — bảng số chính theo lượt đo giữa kỳ; bản đang chạy đã được chấm lại cả bộ |

**Phần 3 — Từ chatbot thành trợ lý**

| Bài | Nội dung | Trạng thái |
|---|---|---|
| [12](12_VI_SAO_CAN_TRO_LY.md) | Từ chatbot thành trợ lý: xếp loại câu và công cụ | đã viết, chờ anh đọc |
| [13](13_TIM_THEM_VA_NHO_CAU_HOI.md) | Rút thêm thẻ và nhớ câu hỏi | đã sửa 13/11 — thêm "hết lượt tìm thì dừng" (bật 13/11) |
| [14](14_VIEC_DE_NHAM_THI_CODE_LAM.md) | Việc dễ nhầm thì code làm: ngày âm lịch, thời tiết, lịch trình | thêm ghi chú 14/11 — biểu mẫu nay là bản 2 (bài 23) |
| [15](15_TRA_WEB_VA_HOI_BANG_ANH.md) | Khi sổ không có: tra web, và hỏi bằng ảnh | đã sửa 13/11 — thêm chuyện thật thử Exa, giữ Serper |
| [16](16_KE_DO_AN_VA_CHO_CON_YEU.md) | Kể đồ án trong 2–3 phút, và chỗ còn yếu | đã sửa 13/11 — thêm kết quả lượt đo giữa kỳ; sửa bảng chỗ yếu |

**Phần 4 — Phần người dùng thấy, đóng gói, tra cứu, cách làm, bảo mật** (bù phần đã làm mà bài 0–16 chỉ nhắc qua; thêm 11/11 chiều)

| Bài | Nội dung | Trạng thái |
|---|---|---|
| [17](17_GIAO_DIEN_VA_TOC_DO.md) | Trang người dùng thấy, và chờ bao lâu: giao diện và tốc độ | thêm ghi chú 14/11 — giao diện mới ở bài 24 |
| [18](18_DONG_GOI_DOCKER.md) | Mang cả chatbot sang máy khác: đóng gói Docker | đã viết, chờ anh đọc |
| [19](19_BANG_TONG_CAC_LAN_SO_SANH.md) | Bảng tổng các lần so sánh (trang tra cứu) | thêm dòng 38–42 (chiều 14/11) |
| [20](20_LAM_DO_AN_THE_NAO.md) | Làm đồ án thế nào: dòng thời gian, nhiều agent, rào bằng máy, tiền | đã sửa 13/11 — thêm ví dụ "đếm lỗi trước khi xây", tiền tới hết 12/11 |
| [21](21_DU_LIEU_NGUOI_DUNG_VA_BAO_MAT.md) | Dữ liệu người dùng đi đâu, và bảo mật | đã viết, chờ anh đọc |

**Phần 5 — Việc xong ngày 14/11** (viết sau khi xong; việc đang làm chưa đưa vào)

| Bài | Nội dung | Trạng thái |
|---|---|---|
| [22](22_BO_SUNG_SO_TAY.md) | Viết thêm vào sổ tay mà không làm hỏng trang cũ: sáu lần ghi kho 14/11, đo trước ↔ sau, chỉ đo câu bị chạm | thêm lần 4 (tám quán ăn), lần 5 (10 món, 13 địa điểm / di tích), lần 6 (16 lễ hội / nghệ thuật) |
| [23](23_LEN_KE_HOACH_BAN_2.md) | "Lên kế hoạch" bản 2: code xếp theo luật, nghiệm thu trượt rồi đạt nhờ dữ liệu và ba sửa nhỏ | đã sửa theo kiểm độc lập; thêm ghi chú chiều 14/11 (sửa lịch, chỗ ở ở bài 25; lịch mẫu; bỏ ghi công) |
| [24](24_GIAO_DIEN_H1.md) | Giao diện "Sông Hương": đẹp hơn mà không chậm hơn, và đo được; ảnh cho 249 / 263 bài ở Khám phá | đã sửa theo kiểm độc lập; thêm chiều 14/11 (sông qua từng điểm, ba bến, "Huế qua các thời kỳ", bỏ ghi công) |
| [25](25_TRO_LY_LAM_VIEC_THAT.md) | Trợ lý làm việc thật: sửa lịch bằng lời, câu hỏi nhiều ý, chỗ ở, quán ăn, lịch mẫu đủ đi – ăn – ở, so tiền mục web, ảnh dưới câu trả lời | thêm chiều 14/11: mục 4–7 + chuyện thật thứ hai |

Nhịp: đã viết đủ 17 bài (sáng 11/11), thêm bài 17–21 (chiều 11/11) theo yêu cầu của anh: bộ bài kể **mọi việc đã làm xong** (xây, triển khai, so sánh, tối ưu, đóng gói, cách làm); phần đang làm dở chưa đưa vào, xong sẽ viết bổ sung. Đã sửa các câu sai / chưa rõ ở bài 4, 8, 11, 14 (ghi ở Nguồn từng bài); bài 17–19 đã qua một lượt kiểm độc lập. Anh đọc dần theo số, góp ý lúc nào thì mình sửa lúc đó; thấy câu nào sai thì mình sửa ngay và ghi ở mục Nguồn của bài.
