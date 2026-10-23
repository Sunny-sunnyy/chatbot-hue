# Báo cáo dành cho người dùng: Giai đoạn 7A — Bộ câu hỏi chuẩn cho toàn bộ dữ liệu

```text
Trạng thái: Đã xác nhận (23-10-2026)
Cập nhật lúc: 23-10-2026 +07
```

## 1. Bạn nhận được gì

Một **bộ 176 câu hỏi chuẩn** (Golden) phủ cả 5 mảng dữ liệu: món ăn, di tích,
lễ hội, nghệ thuật biểu diễn, du lịch. Kèm theo là **bộ smoke 10 câu** để chạy
thử nhanh.

Mỗi câu gồm:

- câu hỏi viết như người thật hỏi;
- đáp án tham chiếu ngắn, chỉ trả lời đúng điều được hỏi;
- các keyword lấy nguyên văn từ dữ liệu, dùng để chấm phần tìm kiếm;
- loại câu.

Bộ câu này sẽ được dùng ở Phase 7B (chấm điểm chatbot) và Phase 8 (so sánh cấu
hình). Dữ liệu là private, không đưa lên GitHub.

## 2. Bộ câu hỏi được làm thế nào

```text
đọc file .md -> viết thử 20 câu di tích -> bạn chỉnh văn phong, chốt hướng dẫn viết
-> 6 sub-agent viết song song 6 nhóm còn lại -> máy kiểm tra định dạng/keyword
-> Reviewer đối chiếu từng câu với dữ liệu -> bạn đọc mẫu -> sửa -> gộp file
```

## 3. Đã chạy và quan sát gì

| Nội dung | Kết quả | Ý nghĩa |
|---|---|---|
| Số câu | 176 (sự kiện 75, nhiều nguồn 29, điều kiện 29, so sánh 25, ngoài phạm vi 18) | Đúng tỷ lệ đã chốt (±20%) |
| Theo nhóm | món ăn 37, di tích 36, lễ hội 27, nghệ thuật 17, địa điểm 32, dịch vụ 13, vé 14 | Nhóm nào cũng ≥10 câu |
| Đối chiếu dữ kiện | 100% câu được kiểm với file nguồn | Đáp án có trong dữ liệu |
| Bạn đọc | 20 câu thử + 55 câu mẫu | Văn phong được bạn xác nhận |
| Câu bị loại hoặc sửa | 4 xóa, 10 sửa, chủ yếu vì dữ liệu mâu thuẫn hoặc đáp án lấp lửng | Bộ câu chỉ giữ dữ kiện chắc chắn |
| Kiểm tra máy | Đạt cho cả 7 file nhóm, file chuẩn và smoke | Đúng định dạng, keyword có nguyên văn trong dữ liệu |
| Mâu thuẫn trong dữ liệu gốc | 53 mục, đã được 3 AI tra cứu; 21 mục đủ căn cứ để sửa | Bộ câu tránh hết các dữ kiện này |

## 4. Cách bạn kiểm tra thêm nếu cần

Mở `knowledge-base-hue/evaluation/golden_full_corpus.jsonl`: mỗi dòng là một câu.
Muốn kiểm lại định dạng, chạy từ thư mục `backend/`:

```bash
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus.jsonl
```

Lệnh này không gọi API, không tốn phí.

## 5. Giới hạn và bước tiếp theo

- Câu hỏi do AI viết rồi người duyệt, không phải câu hỏi thật của người dùng.
- Model chấm điểm sẽ cùng là `gpt-6-luna`, có thể thiên vị cách viết của chính
  nó. Sẽ xem lại ở Phase 7B.
- Giá và giờ mở cửa có mốc tháng 09/2026, có thể lỗi thời.
- **Bước tiếp theo:** phase "Sửa corpus và tạo lại index". Sửa 21 mục mâu thuẫn
  đã đủ căn cứ, rồi tạo lại index để chatbot dùng dữ liệu mới. Sau đó là Phase
  7B (công cụ chấm điểm). Cả hai phase đều cần thiết kế và bạn duyệt trước.
