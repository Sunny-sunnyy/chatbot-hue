# Báo cáo cho bạn: sửa code sau khi rà Phase 0–7 (đã xong cả 5 gói)

**Cập nhật lần cuối: 17:11 31/10/2026 — bản 3: rà lại cho đúng hiện trạng, xoá phần không còn đúng (User 31/10).**
Các bản trước: xem `git log` file này. Người viết: A (bản 1–2), agent con của A (bản 3) · Rà code: B (dựng kho tìm kiếm), C (trả lời + đánh giá),
kiểm chéo lẫn nhau. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt

- **25/10:** rà toàn bộ code, test, notebook, guide của Phase 0–7 (chỉ đọc, 0 USD) ⇒ 39 phát hiện (2 nặng, khoảng 14 vừa, còn lại nhẹ), gom thành
  5 gói sửa. Bạn duyệt **cả 5 gói** tối 25/10.
- **26/10: sửa xong cả 5 gói**, đã vào bản chính (`main`). Mỗi gói: một session sửa, session khác review, chạy test + "cổng ổn định" (mở API thật:
  trang chủ, kiểm sức khoẻ, 1 câu trong kho có nguồn, 1 câu ngoài kho bị từ chối, log sạch).
- **Kết quả chính:**
  - lỗi người dùng gặp thật — câu trả lời đúng nhưng bị báo "không đáp ứng yêu cầu trích dẫn" vì model ghi nguồn kiểu "[Nguồn 2]" — **đã hết**: chấm
    lại 1.600 câu trả lời đã sinh, lỗi trích dẫn 69 ⇒ 14, không câu đạt nào bị đổi thành sai; số 30/10 trên chatbot hiện tại: lỗi trích dẫn 0 / 489;
  - API báo đúng loại lỗi (Qdrant lỗi ⇒ "tạm không tìm được" thay vì "lỗi nội bộ");
  - dựng lại kho chặn chắc hơn: đoạn quá dài luôn dừng; kiểm "kho khớp bản ghi" so cả nội dung, không chỉ số đoạn;
  - code thừa gỡ, backend 8.345 ⇒ 6.218 dòng (26/10); nội dung kho ra khỏi file trong repo public;
  - chatbot trả lời **y như trước** (kết quả tìm và chuỗi gửi model giống từng byte trước / sau).
- **Tiền:** cả đợt sửa ≈ 0,003 USD (phần lớn là ước — lúc đó API chưa ghi số token).
- **Bạn cần quyết gì:** không còn gì ở việc này.

## 2. Đã sửa gì (bảng tra)

| Gói | Sửa gì (lời thường) | Commit | Kết quả kiểm |
|---|---|---|---|
| 1a | Bộ kiểm trích dẫn nhận cả "[Nguồn n]" lẫn "[n]", đổi về "[n]" trước khi gửi giao diện; không đổi câu trả lời của model | `9e6d371` (25/10) | 1.600 câu đã sinh: lỗi 69 ⇒ 14, 0 câu đạt bị đổi; 2 câu hỏi API thật · PASS |
| 1b | Một kiểu nạp module cho API, lệnh dựng kho, test (mọi lệnh chạy từ `backend/`) ⇒ API bắt đúng lỗi tìm kiếm; "model không nạp được" báo 503, không lẫn với "cần lập chỉ mục lại" 409; bỏ nhánh không bao giờ chạy | `1e4acd0` (25/10) | module nạp đôi 3–14 chỗ ⇒ 0; 3 test viết trước (API bắt đúng lỗi tìm kiếm; kho lệch ⇒ 409; thiếu model ⇒ 503) đỏ ⇒ xanh; kết quả tìm giống byte · PASS |
| 2 | Đoạn vượt giới hạn token luôn dừng việc dựng kho; test gọi đúng hàm thật; kiểm "kho khớp bản ghi" so nội dung + dữ liệu từ khoá; guide có quy trình "dựng lại khi kho đổi" | merge `421c302` (26/10); guide trong `1b9c126` | mã băm toàn bộ đoạn giống trước; kết quả tìm 158 câu giống byte; test đạt (trừ phần cần key) · PASS |
| 3 | Công cụ đo: một hàm so cặp chung (sửa chiều thắng / thua ở chỉ số "càng ít càng tốt"), một chỗ dựng tin nhắn gửi model | `47a4e32` (25/10) | so cặp giống byte trên 5 cặp file thật, chiều đúng; chuỗi gửi model giống byte 25 câu · PASS |
| 4 | Guide / notebook lệch code: guide Phase 0–6 có dòng "lịch sử" + mục "Hiện hành"; guide 7 / 8 tả đúng hiện trạng; bỏ đường dẫn tới dự án khác | `1b9c126` (25/10) | đường dẫn chết ngoài phần lịch sử 34 ⇒ 1 (thư mục dự kiến Phase 9); đường dẫn tới dự án khác 48 ⇒ 0; 3 notebook chạy lại hết ô · PASS |
| 5 | Dọn code thừa (không đổi hành vi): gỡ đường "Representation B" (agent thứ hai tạo đoạn tìm kiếm — chatbot không dùng), bộ kiểm khói Phase 5, nhánh model `minilm`, script chuyển đổi dùng một lần; bộ kiểm khói Phase 6 giữ, bỏ phần thừa (còn 4 câu) | merge `421c302` (26/10) | như gói 2; review toàn nhánh: 0 lỗi nặng / vừa · PASS |
| Repo public | Nội dung kho chép nguyên văn trong file cấu hình / test / script ⇒ bỏ khỏi file trong repo; 8 file cũ ở `reports/artifacts/` ⇒ chuyển sang `data/` (private), lịch sử git giữ | merge `421c302` + commit tài liệu 26/10 | quét: 0 chuỗi kho trong code / test / notebook; 80 report lịch sử còn trích một phần kho — bạn chọn để nguyên (26/10) |

**Một giả thuyết đi kèm đã đo xong:** sau khi sửa 1a, đếm lại cho thấy lý do 8.1 bỏ "suy luận none" (lỗi trích dẫn tăng) yếu đi. Đã thử lại ở đợt cải tiến
27/10: "suy luận none" **kém hơn** (có câu trả lời vòng, không trích nguồn) ⇒ giữ suy luận mặc định.

## 3. Giới hạn còn lại

- Một số tác động chỉ suy ra từ code, chưa tái tạo trên hệ thống thật (vd. "Qdrant lỗi giữa lúc hỏi").
- Test cần key OpenAI không chạy trong đợt rà; số tiền đợt sửa là ước.
- Để sau (thiết kế, không phải lỗi): cấu hình sinh câu trả lời còn ghim cứng trong code; một dependency thừa bạn chọn giữ.

## Phụ lục — hồ sơ kỹ thuật

- Đợt: `report_agent/2026-10-25_ra_soat_code/` — `TONG_HOP.md` (bảng sửa, commit, kết quả), `ra_soat_code_B.md` (B-01…B-21), `ra_soat_code_C.md`
  (C-01…C-20), `kiem_cheo_B.md`, `kiem_cheo_C.md`, report từng gói `sua_1a_*`, `sua_1b_*`, `sua_3_*`, `sua_3c_citation_v2.md`, `sua_4_*`, `sua_dot3_*`,
  `a_dong_dot3_review.md`; nhật ký `bao_cao_he_thong/nhat_ky/2026-10-26_sua_code_xong.md`.
- Mã phát hiện theo gói: 1a = C-09; 1b = B-01 / C-01 + C-11; 2 = B-11 (+ B-04), B-20, B-18; 3 = C-02 + C-20, C-03; 3c = C-09 (suy ra, thử lại là R1
  ở 8.2, `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`); 4 = B-16, C-12, B-17, B-21, C-14, C-13, B-19; 5 = B-02, B-05–B-07, B-09, B-14,
  B-15, C-04, C-06, C-07, C-10, C-17, C-18, C-05, C-19; repo public = B-12, B-19; để sau = B-03, B-13, B-10.
- Đợt 3 (gói 2 + 5 + B-12) = 12 commit `3a37af4`…`8f0e5c4`, merge `421c302`; đoạn sha `60591acff422ece6`, mốc tìm `cefb2d1ad609` (khi đó; mốc hiện hành
  sau hai đợt sửa kho: `Project_Status.md` §4).
