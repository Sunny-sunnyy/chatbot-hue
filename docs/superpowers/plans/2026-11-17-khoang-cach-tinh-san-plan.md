# Plan mức nhẹ — "khoảng cách tính sẵn" (C, 15:52 16/11/2026)

User chọn 16/11: làm trong tuần, **xong trước 22/11** (B7 cần code đứng yên từ 23/11). Mức nhẹ: A đọc rồi duyệt; không review plan. Trần **0,05 USD**.
Phân tích nền: `data/khoang_cach_2026-11-16/toc_do.md` (private).

## 1. Lỗi có thật (đã đo, 0 USD)
Câu khoảng cách chữ đầu p50 **3,7 s** / p95 **6,2 s** (sàn 3 / 5 s; 14 câu, lượt đo sau review 16/11). Chỗ tốn nhất: lần gọi model chỉ để trả "gọi `khoang_cach`
với 2 mã" — p50 1,8 s / p95 3,1 s, nằm thẳng trên đường chữ đầu.

## 2. Đổi gì (một nhánh, cờ riêng `khoang_cach_tinh_san: false`, cần `khoang_cach`)
- **Code tìm tên điểm** (`khoang_cach.tim_hai_diem(cau, bang) -> (a, b) | None`, hàm thuần): tên + tên khác của bảng, so nguyên cụm sau NFC + chữ thường, cụm dài
  trước, không chồng nhau; **đúng 2 mã khác nhau** ⇒ trả cặp theo thứ tự xuất hiện; 0 / 1 / ≥ 3 mã ⇒ `None`. Chỉ xét **câu đang gõ** (không lịch sử).
- **Chỉ khi** cờ bật + bộ dò từ khoá hiện có bật + `tim_hai_diem` ra cặp ⇒ code tra bảng (`kc.ket_qua`), đăng nguồn khoảng cách vào sổ nguồn và nối vào ngữ cảnh
  **trước lần gọi model đầu** (cùng chỗ với "Lịch hệ thống", `assistant.py` ~dòng 800), **không đưa** công cụ `khoang_cach` ở lượt đó (`max_turns` như lượt
  không có công cụ). Bước kiểm số sau khi sinh giữ nguyên (đọc `trace.khoang_cach`).
- Còn lại (không khớp đúng 2 tên, câu hỏi tiếp "từ đó sang…", nơi ngoài bảng) ⇒ **đường hiện nay** (model gọi công cụ).
- **Dữ liệu:** thêm tên khác ngắn vào bảng điểm cho các tên hay gõ tắt (đếm 16/11: "Đại Nội" — bảng ghi "Đại Nội Huế"; "phố Tây" — bảng ghi "Khu phố Tây Huế").
  Đổi bảng điểm ⇒ theo `WORKFLOW.md` §3.4 quét nhãn các bộ đo dùng bảng này + mô phỏng 0 USD trước merge. **Tên khác cũng vào mô tả công cụ** ⇒ đường cũ có thêm
  một tên trong danh sách gửi model (ghi rõ trong report; test byte "cờ tắt" so với bảng mới).
- Không đổi: bảng km / phút, công thức phút, lời dặn trả lời, bộ dò từ khoá.

## 3. Tiêu chí (ghi trước) + bộ đo
| Vai | Bộ / cách đo | Ngưỡng |
|---|---|---|
| Bộ dò tên (W82, 0 USD) | ≥ 20 câu **người không viết code** soạn (A giao agent con): câu 2 tên đúng · tên khác · tên trùng một phần ("lăng", "Kinh thành" ↔ "Đại Nội") · câu 3 nơi · **câu nhắc 2 nơi mà hỏi việc khác** · câu 1 nơi + "trung tâm" | **0 sai cặp** (ra cặp khác nhãn). Ra `None` khi nhãn có cặp = đi đường cũ, được phép, ghi số |
| Test (0 USD) | cờ `khoang_cach_tinh_san` tắt ⇒ chuỗi gửi model giống byte (lượt đầu, hỏi tiếp, có lịch sử, stream / không); cờ bật + câu không khớp ⇒ giống byte bản cờ tắt; cờ bật + khớp ⇒ ngữ cảnh có nguồn khoảng cách, danh sách công cụ không có `khoang_cach` | đạt; có ca đối chứng ra "khác" |
| Lượt có phí (server tạm 8041, 1 lượt) | 16 câu của lượt đo 16/11 (`data/khoang_cach_2026-11-16/do.py`) | **câu đi đường nhanh: chữ đầu p50 ≤ 3 s**; mọi câu: **0 số sai, 0 sai cặp**; câu đường cũ: đúng cặp như trước (≥ 12 / 14 tổng); nơi ngoài bảng ra số 0 / 2 |
| An toàn 32 | đếm bằng code số câu chạm từ khoá **và** ra cặp | 0 câu chạm ⇒ không lượt an toàn có phí |
Sàn tốc độ đặt trên câu **đi đường nhanh**; báo kèm p50 / p95 của cả 14 câu trong bảng và số câu đi mỗi đường.

## 4. Tiền + giờ
Lượt đo ≈ 16 × 0,0008 ≈ 0,013 USD; chạy lại sau sửa ≤ 0,013 ⇒ **≤ 0,03**, trần 0,05. Giờ ≈ 2–3 (code + test 1 giờ, bộ dò + đo 1 giờ, tài liệu 0,5 giờ).
Ngày làm: phiên ban ngày 17/11 (việc nhẹ, một server tạm lúc đo). Review: một review cả nhánh ≤ 5 dòng (xử lý chữ người dùng + chuỗi gửi model).

## 5. Rủi ro đã biết
- Câu nhắc 2 nơi mà hỏi việc khác, có từ khoá ("đi Đại Nội rồi Thiên Mụ có xa không, mua vé gì?") ⇒ nguồn khoảng cách vẫn đúng cặp, chỉ thừa; câu không có từ
  khoá thì không vào đường này.
- Hai nơi sát nhau trong một cụm tên ("Kinh thành Huế (Ngọ Môn – Kỳ Đài)" ↔ "Đại Nội") — bộ dò phải có; mập mờ ⇒ ưu tiên `None` (đường cũ).
