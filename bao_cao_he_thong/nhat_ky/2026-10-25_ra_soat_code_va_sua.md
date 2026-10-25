# Nhật ký 25/10/2026 (đêm) — rà code xong, bắt đầu sửa

**Cập nhật lần cuối: 21:50 25/10/2026.** Người viết: A. Tiền phiên: ~0,0023 USD (~60 đồng; phần lớn là chạy thật kiểm ổn định).

## Hôm nay làm gì

- **Rà code Phase 0–7 xong** (18:55): B rà phần dựng kho tìm kiếm, C rà phần trả lời + đánh giá; mỗi bên kiểm lại 5 phát hiện nặng
  nhất của bên kia bằng script riêng. 39 phát hiện, gom thành 5 gói ⇒ `../DE_XUAT_SUA_CODE.md`.
- **Bạn duyệt 19:4x:** sửa cả 5 gói; gỡ code không dùng nếu không ảnh hưởng hệ thống; guide cũ thêm dòng lịch sử; đưa nội dung kho /
  đường dẫn dự án khác ra khỏi file public từ giờ (không xóa lịch sử).
- **A đổi một chỗ trong đề xuất của chính mình:** không đưa "10 đoạn" (B1) vào trước — spec 8.2 chỉ cho đưa vào sau khi bạn đọc cặp mù.
  Sửa code trên bản chính trước; B1 chờ, sau này chạy lại 2 kiểm tra miễn phí.
- **Gói 1a xong (commit `9e6d371`):** chatbot hết báo lỗi nhầm khi model ghi nguồn kiểu "[Nguồn 2]". Trên 1.600 câu đã sinh: lỗi
  69 → 14, không câu đúng nào bị đổi. C làm, B review.
- **Gói 4 xong (`1b9c126`):** guide 0–6 có dòng "lịch sử" + phần "hiện hành", guide 7 / 8 cập nhật, có hướng dẫn dựng lại kho; 48 đường dẫn tới
  dự án khác ⇒ 0. B làm, C review.
- **Gói 3 xong (`47a4e32`):** sửa công cụ so cặp (đảo thắng / thua ở chỉ số "số câu từ chối"), gộp chỗ ghép tin nhắn gửi model; kết quả giống hệt
  từng byte. C làm, B review. Đếm lại lỗi trích dẫn mọi mốc cũ: 69 ⇒ 14; lý do loại "suy luận none" ở 8.1 không còn (chờ thí nghiệm xác nhận).
- **Gói 1b xong (`1e4acd0`):** API báo đúng loại lỗi (409 cần dựng lại chỉ mục / 503 lỗi tạm). Bạn chạy giúp test "thiếu model" hai lần (đỏ ⇒
  xanh). **Lệnh dựng kho đổi:** chạy từ `backend/`. B làm, C review.
- **Thêm luật (bạn 20:0x):** sau mỗi gói phải qua "cổng ổn định" — test + chạy chatbot thật + 2 câu hỏi thật; 8.2 chỉ chạy lại khi xong 5 gói.
- **Đang làm:** kế hoạch đợt 3 (gói 2 chốt an toàn + gói 5 dọn code + đưa nội dung kho ra khỏi repo public) — C viết, B review bắt được một lỗi
  lớn (cách chuyển file vẫn để file trong Git), C đang sửa. Chuẩn bị đợt "tìm hướng tốt hơn": C lập 12 ứng viên, A soạn nháp yêu cầu ChatGPT.

## Trạng thái

| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Rà code | Xong + kiểm chéo hai chiều | 2 lỗi nặng: báo lỗi nhầm "[Nguồn n]" (đã sửa), API báo sai loại lỗi (đợt 2) |
| Gói 1a — "[Nguồn n]" | **Đã sửa, đang chạy** | Lỗi người dùng thấy: 4–8/176 → 0–2/176 câu |
| Gói 4 — tài liệu | **Xong** | Guide cũ không còn tả hệ thống đã gỡ như đang chạy |
| Gói 3 — công cụ đo | **Xong** | So cặp đúng chiều; chuẩn bị cho 8.2 |
| Gói 1b — mã lỗi API | **Đã sửa, đang chạy** | Người vận hành biết đúng: dựng lại chỉ mục hay chỉ là lỗi tạm |
| Gói 2, 5 | Chờ (đợt 3) | Chốt an toàn + dọn code, cùng lần dựng lại kho |
| Phase 8.2 | Vẫn tạm dừng | B1 ở nhánh riêng, chờ bạn đọc cặp mù |

## Giải thích ngắn (để bạn tự nói lại được)

Model được đưa các đoạn tài liệu có nhãn "[Nguồn 1]", "[Nguồn 2]"… và được dặn trích bằng "[1]", "[2]". Đôi khi nó chép theo nhãn.
Bộ kiểm cũ chỉ hiểu "[1]" nên tưởng câu trả lời không có nguồn và báo lỗi. Giờ bộ kiểm hiểu cả hai dạng và đổi hết về "[1]" trước khi
hiện lên web. Điều này cũng cho thấy một kết luận cũ của 8.1 ("model quên ghi nguồn") là sai nguyên nhân.

## Bạn cần làm gì

- Không cần gì ngay. A sẽ hỏi trước khi chạy thí nghiệm có phí (xem lại "suy luận none").
- Khi tiện: đọc cặp mù `data/phase_8_2/b0/nhan_xet_user.md` (~30–45 phút) — cần trước khi đưa "10 đoạn" vào chatbot.

## Đọc thêm

- `../DE_XUAT_SUA_CODE.md`, `../BAO_CAO_SINH_CAU_TRA_LOI_API.md` (bản 6)
- `report_agent/2026-10-25_ra_soat_code/` (`TONG_HOP.md`, `sua_1a_implementation.md`, `sua_1a_review.md`)
