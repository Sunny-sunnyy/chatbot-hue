# Nhật ký 08/11/2026 — chốt phạm vi trước đóng gói, ảnh cổng vào chatbot

**Cập nhật lần cuối: 09:58 08/11/2026.** Tiền paid trong ngày tới giờ: ≈ 0,011 USD (~275 đồng) — B bản đồ ≈ 0,0015 · E thử ảnh ≈ 0,0083 · A cổng ổn định ≈ 0,0009.

## Tóm tắt
- Bạn quyết: **chưa deploy**; chỉ đưa lên AWS khi hệ thống đủ tính năng, ổn định, code đóng gói + Docker đầy đủ.
- Phạm vi trước đóng gói (ngoài phần bắt buộc: so sánh cuối B7, đóng gói, báo cáo): **bản đồ lịch trình**, **bật hỏi bằng ảnh**, **giữ giọng nói** (bạn thu 40 câu); không làm tiếng Anh. Thêm **Nhóm 1 + 2**: 14 việc nhỏ (sao chép lịch, nút Dừng, báo rõ khi câu quá dài, sửa thẻ Khám phá, kiểm mọi con số ở mục web…).
- C + E rà mọi file `.md`: gộp còn khoảng 60 ý đã ghi mà chưa làm, chia 4 nhóm theo cỡ việc (bản đầy đủ: `data/ra_soat_tinh_nang_2026-11-08/C.md`, `E.md`).
- **7 ảnh thật lên cổng** (merge `c9931be`): kiểm trên `main` — build, 24 test, trang `/`, 7 ảnh tải được, 1 câu trong kho trả lời có nguồn + 1 câu ngoài kho từ chối đúng, log không ghi chữ câu hỏi.
- README của repo sửa cho đúng hiện trạng (trước ghi sai "chưa nhớ hội thoại").

## Bạn cần làm gì
- Xem phiếu toạ độ bản đồ (tick "Đúng chỗ?"): `data/phase_11/ban_do/phieu_toa_do_11_diem.md`; ảnh chụp bản đồ: `data/phase_11/ban_do/anh_v2/`.
- Thu 40 câu giọng nói khi rảnh: `data/phase_10/giong_noi/bo_40_cau/huong_dan_thu_cho_user.md`.
- Việc 14 (định tuyến lỗi mà câu có dấu hiệu khẩn cấp ⇒ vẫn trả câu khẩn cấp): A sẽ hỏi riêng.

## Trạng thái
| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Ảnh cổng | vào `main` | trang chủ / Khám phá / lĩnh vực có ảnh thật, ghi công đủ |
| Bản đồ lịch trình | vào `main`, cờ tắt (`a4fde29`) — chờ bạn xem ảnh + phiếu toạ độ | plan duyệt; thư viện Leaflet + ảnh nền OpenStreetMap; cờ tắt tới khi kiểm đạt |
| Bật hỏi bằng ảnh | **bật trên `main`** (`cf57309`) | 5 ảnh thử: đúng cả 5 (ảnh không phải Huế ⇒ "chưa nhận ra"); đoán tên trung vị 3,5 s, chậm nhất 9,1 s |
| Nhóm 1 + 2 việc nhỏ | phần B + E **vào `main`** (Dừng, 500 ký tự, gợi ý, Nguồn gộp, sao chép lịch); phần C đang review | mỗi việc ≤ ½ ngày, gần 0 USD |
| Đổi khung: cổng 2 nhóm + 4 công cụ | spec bản 13 (C viết) đang review (B) ⇒ bạn duyệt | trần Phase 9 3,5 USD |
| Deploy | hoãn (bạn quyết) | làm sau khi đóng gói |

## Bàn kiến trúc (đang bàn)
Bỏ tuyến khẩn cấp; cổng chỉ còn 2 nhóm (trò chuyện xã giao / về Huế), chạy mọi câu; câu ngoài phạm vi vào agent Huế tự từ chối. Bộ đệm: đệm phần đầu câu gửi OpenAI đang chạy tự động; đệm câu trả lời để Phase 12 khi có người dùng thật.

## Giải thích ngắn (để bạn tự nói lại được)
Trước khi đóng gói, nhóm rà lại mọi ghi chú cũ để không bỏ sót tính năng; việc nhỏ người dùng thấy ngay làm trước, việc lớn / thí nghiệm ghi làm "hướng phát triển". Ảnh cổng: ảnh không có giấy phép mở để ngoài git, bản tải về tự dùng ảnh Commons thay — nên repo công khai không chứa ảnh không được phép.

## Đọc thêm
- `bao_cao_he_thong/BAO_CAO_SINH_CAU_TRA_LOI_API.md` (bản 42), `LUONG_HOAT_DONG_HE_THONG.md`
- `report_agent/2026-11-06_giao_dien_cong/b_anh_cong_implementation.md`, `c_anh_cong_review.md`; plan bản đồ `docs/superpowers/plans/2026-11-08-ban-do-lich-trinh-plan.md`
