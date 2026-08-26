# Báo cáo dành cho người dùng: Giai đoạn 7 - Đồng bộ evaluation sau đơn giản hóa

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 26-08-2026 16:03 +07
Notebook cần kiểm tra: notebooks/07_evaluation.ipynb
```

## 1. Bạn nhận được gì

Luồng đánh giá câu trả lời giờ luôn dùng collection đang được cấu hình cho hệ
thống; người dùng không thể vô tình chọn collection khác ở public answer path.
Khả năng chọn collection vẫn được giữ riêng cho các phép so sánh retrieval đã
được duyệt.

Notebook 07 trong repository đã sạch kết quả cũ, còn hai CSV lưu đúng lần smoke
run 20 câu gần nhất.

## 2. Hệ thống hoạt động như thế nào

Hệ thống đọc 20 câu hỏi thật, tìm thông tin trong Qdrant, dựng context, sinh câu
trả lời bằng `gpt-5.4-nano`, rồi dùng `gpt-5.4-mini` để chấm accuracy,
completeness và relevance. Retrieval và answer ghi vào hai CSV cố định theo đúng
thứ tự câu hỏi.

## 3. Codex đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| Focused integration suite | Đạt: 9 tests, 4 warnings | Real Qdrant, local E5 và OpenAI paths hoạt động; warnings chỉ là thông báo đổi tên API thư viện |
| Notebook 07 Run All | Đạt trên bản tạm | Toàn bộ luồng retrieval, generation và judge chạy từ đầu đến cuối |
| Retrieval smoke set | 20/20 thành công; MRR 0.7917, nDCG 0.8020, coverage 96.67% | Retrieval pipeline và artifact chạy đúng trên bộ smoke hiện hành |
| Answer smoke set | 20/20 thành công; 4.40 / 4.05 / 4.25 | Generation/judge hoàn thành không có row lỗi trong lần Reviewer chạy |
| Canonical notebook | 22 cells, outputs rỗng | Repository không lưu output hoặc execution count cũ |
| Active Qdrant | 572 points trước và sau | Collection active được giữ read-only |

## 4. Cách bạn chạy lại

Mở `notebooks/07_evaluation.ipynb` từ repo root, bảo đảm Qdrant đang chạy và
repo-root `.env` có cấu hình provider cần thiết, rồi chọn **Run All** từ trên
xuống.

Bạn nên thấy notebook đọc 20 câu, chạy một ví dụ retrieval/answer, sau đó hoàn
thành hai batch 20 câu và hiển thị summary. Notebook dùng local model, Qdrant
thật và paid OpenAI API thật. Không cần dán secret vào notebook hoặc chat.

Cell cuối tạo `Gradio Blocks`. Để mở giao diện trong notebook, chạy thêm
`app.launch(inline=True)`; chỉ ghi `app` sẽ hiển thị cấu trúc hai backend
functions chứ chưa khởi chạy giao diện.

## 5. Giới hạn và bước tiếp theo

Correction này không sửa golden dataset và không chạy lại paid batch 104 câu;
đó là chủ ý của scope đã duyệt. Bạn đã chạy Notebook 07 và xác nhận correction
ngày 26-08-2026 +07. Bộ smoke hiện tại còn thiếu câu cafe và các finding
annotation vẫn chờ session dữ liệu riêng. Phase 8 tiếp tục đóng.
