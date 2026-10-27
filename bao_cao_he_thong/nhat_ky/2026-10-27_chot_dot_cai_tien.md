# Nhật ký 27/10/2026 (sáng) — chốt đợt cải tiến từng khâu: bốn thí nghiệm, một hướng có tín hiệu thật

**Cập nhật lần cuối: 11:17 27/10/2026.** Tiền paid sáng nay: ≈ 0,173 USD (~4.300 đồng). Phần lớn đo từ log; 0,0087 USD là ước, vì một lượt mất số
liệu (cận trên ≈ 0,0055 USD thêm).

## Tóm tắt

- Bạn mô tả mục tiêu sản phẩm: **đồ án tốt nghiệp, xem như sản phẩm kinh doanh thật**; người dùng là bạn, du khách, người dân. Thời gian chờ và tiền mỗi
  câu chưa có con số ⇒ so sánh, đánh giá, chỗ nào tối ưu được thì tối ưu.
- Sáng nay thử thêm bốn cách. Ba cách **dừng sớm đúng luật**: cho model tự xếp 30 đoạn (K3), tắt suy luận khi viết câu trả lời (R1), và bản nhanh của
  "model chọn 10 đoạn" (K3b-n).
- Cách thứ tư, **cho model chọn 10 đoạn trong 30, suy nghĩ như thường (K3b-m)**, là tín hiệu tốt nhất của cả đợt. Số câu có đủ đoạn đúng tăng **22 → 31 / 40**,
  không mất câu nào. Câu bị từ chối nhầm giảm **7 → 2**; điểm trung bình cũng tăng (chỉ báo, không dùng để quyết).
- Nhưng có **5 câu bị chấm thấp hơn**, luật cho tối đa 4 ⇒ theo luật ghi trước: **kém hơn, chưa nhận**. Thêm vào đó, người dùng phải chờ khoảng **6,5 s (trung
  vị) / 9 s (p95)** (đo khi chạy 4 câu song song) thay vì ~2–3,5 s ước cho bản hiện tại, và tiền mỗi câu gấp ~3,8 lần.
- Bạn chọn **chốt đợt**: chatbot giữ nguyên, sang B0 rồi đưa context 10 vào chatbot, rồi làm tính năng mới.
- **Chatbot không đổi.**

## Bạn cần làm gì

- **B0:** đọc cặp mù 20 câu (`data/phase_8_2/b0/nhan_xet_user.md`, ~30–45 phút). Đây là việc duy nhất còn chặn việc đưa context 10 vào chatbot.
- Khi tiện: gửi yêu cầu nghiên cứu `gửi chatgpt/2026-10-27/tìm thông tin/muc_tieu_san_pham_2026_10_27.md` (thời gian chờ chấp nhận được, tiền / câu, mức
  nặng lỗi), lưu kết quả vào `gửi chatgpt/2026-10-27/kết quả nghiên cứu/`.
- Cho A biết ngày bảo vệ đồ án (để xếp việc).
- (Không bắt buộc) xem Usage OpenAI cho `gpt-6-luna` khoảng 09:30–09:31 sáng nay để thay số ước 0,0087 USD bằng số thật.

## Trạng thái

| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| R2 trả lời một phần | đóng: kém hơn | trả lời 1 câu ngoài kho — hướng gác |
| K3 model xếp lại 30 đoạn | kém hơn (1 / 40 lần trả danh sách hỏng) | tín hiệu tốt nhưng chậm 5–9 s |
| R1 tắt suy luận khi viết | kém hơn (1 câu "trả lời vòng") | lợi nhỏ (rẻ ~5 %) — gác |
| K3b-n model chọn 10, tắt suy luận | kém hơn (viết thừa chữ sau kết quả) | nhanh (+2 s) nhưng chưa ổn định |
| K3b-m model chọn 10, suy nghĩ thường | bước tìm **tốt hơn (tạm)**; câu trả lời **kém hơn theo luật** | hướng có thật, để lại hồ sơ |
| Đo "nói sai con số" (C48) | 0 / 68 câu có số bị sai | lỗi này hiếm ở chatbot hiện tại |
| Nhãn "đoạn đúng" | chỉ đánh dấu một chỗ / thông tin | thước đếm thiếu ít; kết luận không đổi |
| Cải tiến cách làm W21–W23 | bạn duyệt, đang dùng | sha tính từ file; tách lệnh rủi ro; harness không ghi đè |

## Giải thích ngắn (để bạn tự nói lại được)

Khâu tìm thường lấy được đoạn đúng trong 30 ứng viên nhưng xếp nó ngoài 10 đoạn đầu, nên model không thấy. Cho chính model đọc 30 đoạn rồi chọn 10 đã
sửa được đúng chỗ đó (9 câu cứu được, 0 câu mất), và câu trả lời trung bình tốt lên. Nhưng luật nhận đếm từng câu bị tụt điểm, và 5 câu tụt (đa số chỉ
thiếu một chi tiết nhỏ) đã vượt mức cho phép; thêm nữa người dùng phải chờ lâu hơn khoảng 3 lần (số đo khi chạy song song, chưa đo cùng điều kiện). Vì vậy nhóm giữ chatbot như cũ và ghi hướng này làm hồ sơ để
mở lại khi có con số thời gian chờ chấp nhận được.

## Đọc thêm

- `bao_cao_he_thong/BAO_CAO_TIM_KIEM.md` (bản 8 — các thử nghiệm xếp lại đoạn)
- `bao_cao_he_thong/BAO_CAO_SINH_CAU_TRA_LOI_API.md` (bản 10 — R1, khâu trả lời của K3b-m)
- `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md` (kỹ thuật, đã đóng)
