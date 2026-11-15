# Đếm "cùng một cuộc: hỏi A ⇒ hỏi tiếp B ⇒ hỏi lại A" (C, cập nhật 20:57 15/11/2026) — lượt chạy lại SẠCH: 0 / 8; còn một chỗ chưa khớp

## Kết luận ngắn (đọc phần này)

- **Lượt chạy lại sạch [đã chạy]:** 4 bộ ba câu × 2 cuộc = 8 cuộc, tra web TẮT cho lượt đếm. Đối chứng (câu A ở cuộc mới được trả lời) **8 / 8**; lượt lỗi 0; **lượt 3 (hỏi lại A) bị từ chối 0 / 8** ⇒ theo cách đọc ghi trước (< 2 / 8) ⇒ **không phải lỗi rộng, ghi giới hạn**.
- **Vẫn thấy:** ở lượt 3 model tự tìm kho cho câu B (không phải câu A vừa gõ) ở **3 / 8** cuộc — lần này cả 3 vẫn trả lời đúng A.
- **Chỗ chưa khớp (chưa giải thích được):** bộ "vị trí di tích ⇒ khoảng cách" bị từ chối ở lượt 3 **3 / 3** khi tái tạo trên server thật (tra web BẬT, đúng cấu hình đang chạy) và 1 / 1 ở lượt đếm đầu, nhưng **0 / 2** ở lượt sạch này (tra web tắt). Hai khả năng, chưa đo: (a) dao động của model (mẫu nhỏ); (b) tra web bật làm đổi thứ gì đó ở lượt sau. Lượt đếm tắt web để giữ tiền ⇒ **không tái lập đúng cấu hình đang chạy** — đây là hạn chế của phép đo, do C chọn.
- **Đính chính lượt đếm đầu:** 5 lượt "lỗi kết nối nhà cung cấp" ghi ở dưới nhiều khả năng do **công cụ đếm của C** (mỗi cuộc tạo một client thử riêng trong tiến trình ⇒ khác vòng lặp sự kiện với client model của ứng dụng); bản đầu của lượt chạy lại lỗi 32 / 32 vì đúng lý do này, sửa sang một client duy nhất thì 0 lỗi. Không phải sự cố của nhà cung cấp.
- **Nhánh chẩn đoán "lịch sử kèm câu trả lời": chưa đo** — lượt chính ra 0 / 8 nên nhánh này không còn gì để so, và tiền đã vượt mức duyệt.
- **Tiền lượt chạy lại: 0,0298 USD** (duyệt ≈ 0,015–0,02; vượt vì 32 lượt hỏng của bản công cụ lỗi vẫn tốn phần định tuyến). Cộng lượt đầu 0,0149 ⇒ việc đếm này 0,0447 USD.
- **Đề xuất (A quyết):** chưa làm plan sửa lịch sử. Phiên sau một phép thử nhỏ đúng cấu hình đang chạy: bộ "vị trí ⇒ khoảng cách" × 3 cuộc qua server thật có tra web (≈ 0,013 USD, công cụ `data/f5_cuoc_moi_2026-11-15/tai_tao.py`) — vẫn từ chối ≥ 2 / 3 ⇒ lỗi gắn với lượt có tra web, soi đường đó; không ⇒ ghi giới hạn "câu B bị kho từ chối có thể kéo lượt sau từ chối theo, hiếm".
- Dữ liệu (private): `data/hoi_lai_cau_cu_2026-11-15/` — `dem2.py`, `ket_qua2_chinh.json` (có chữ câu tìm + lịch sử gửi model), `chat_metrics2.log`, `tieu_chi.md` (tiêu chí hai lượt, ghi trước khi chạy).

---

## (Lượt đếm đầu, 20:41 — KHÔNG sạch; giữ để tra)

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
