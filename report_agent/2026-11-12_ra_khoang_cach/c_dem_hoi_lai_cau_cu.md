# Đếm "cùng một cuộc: hỏi A ⇒ hỏi tiếp B ⇒ hỏi lại A" (C, 20:41 15/11/2026) — lượt đếm KHÔNG sạch, đọc như quan sát

A duyệt ≈ 0,02 USD; dùng **0,0149 USD** (24 lượt hỏi, tra web tắt bằng biến môi trường cho lượt đếm). Không sửa lời dặn. Tiêu chí ghi trước: `data/hoi_lai_cau_cu_2026-11-15/tieu_chi.md`.

## Vì sao không sạch
- **5 / 24 lượt lỗi kết nối tới nhà cung cấp model** (`generation_failed`), đều ở lần chạy đầu ⇒ cả 4 cuộc của lần đầu thiếu một lượt trong lịch sử.
- **1 / 4 bộ câu trượt đối chứng:** câu A loại "giờ mở cửa một di tích" bị kho từ chối ngay ở cuộc mới (2 / 2) ⇒ bộ đó không đo được gì về lịch sử.
- Theo tiêu chí ghi trước (đối chứng phải 8 / 8) ⇒ **không đọc con số "x / 8"** như kết luận. Số thô: lượt 3 bị từ chối 3 / 8, trong đó 2 thuộc bộ trượt đối chứng.

## Điều thấy được [đã chạy] — 3 cuộc sạch (đủ 2 lượt lịch sử, đối chứng đạt)

| Bộ (loại câu) | Câu B ở lượt 2 | Lượt 3 (hỏi lại A) | Câu tìm kho model viết ở lượt 3 |
|---|---|---|---|
| vị trí di tích ⇒ khoảng cách sang di tích khác | kho từ chối | **từ chối** | 2 câu, đều hỏi về **khoảng cách của câu B** |
| nguyên liệu món ăn ⇒ quán bán món đó | trả lời được | trả lời đúng A | không tìm thêm |
| thời gian lễ hội ⇒ chương trình năm nay | trả lời được | trả lời đúng A | 2 câu, đều hỏi về **chương trình của câu B** |

- Cộng với 3 lần tái tạo trên đường HTTP lúc sửa lỗi tải lại trang: bộ "vị trí ⇒ khoảng cách" bị từ chối ở lượt 3 **4 / 4** khi câu B nằm trong lịch sử; ở cuộc mà lượt B bị lỗi kết nối (không vào lịch sử) thì lượt 3 **trả lời được** (1 / 1).
- **Quan sát:** ở lượt 3 model tìm kho cho câu B chứ không phải câu A vừa gõ (2 / 3 cuộc sạch). Khi B là câu kho không trả lời được ⇒ cả lượt 3 thành từ chối.
- **Giả thuyết (chưa chứng minh):** lịch sử gửi model chỉ có các CÂU HỎI cũ, không có câu trả lời (cờ nhớ câu trả lời đang tắt — `generator_openai_full_corpus.with_history` bỏ tin trợ lý khi rỗng) ⇒ model thấy ba câu người dùng liên tiếp, coi câu B là câu chưa được đáp và làm tiếp nó.

## Đề xuất (A quyết)
- Lỗi có thật và người dùng sẽ gặp (User đã gặp), nhưng mới chắc ở một kiểu: câu B bị kho từ chối rồi người dùng hỏi câu khác / hỏi lại.
- **Một hướng sửa để thử (plan mức nhẹ, đo trước–sau):** đưa lịch sử cho model dưới dạng một khối ghi rõ "các câu đã hỏi trước, đã xử lý xong — chỉ dùng để hiểu từ như 'đó', 'ở đấy'" thay vì các tin người dùng trần; không bật nhớ câu trả lời (đã cân và bỏ trước đây). Đo: bộ ba câu ở đây (thay bộ trượt đối chứng) + bộ câu hỏi tiếp sẵn có + bộ an toàn, vì đổi chuỗi gửi model ở mọi lượt có lịch sử.
- Trước khi làm plan nên chạy lại lượt đếm này một lần cho sạch (≈ 0,015 USD) — tối nay không đo thêm (luật không đo thêm sau khi thấy số).

Dữ liệu (private): `data/hoi_lai_cau_cu_2026-11-15/` — `dem.py`, `ket_qua.json` (có chữ câu tìm + lịch sử), `chat_metrics.log`.
