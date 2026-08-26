# Báo cáo dành cho người dùng: Giai đoạn 7 - Đánh giá Retrieval và Câu trả lời

> **Current progression note (2026-08-26 +07):** baseline Phase 7 vẫn
> `approved`. Simplicity review Phase 0–6 đã hoàn tất; một post-simplicity
> correction hẹp đã được duyệt. Golden Dataset V2 design/plan đã được user xác
> nhận và đang chờ session Implementer; Phase 8 benchmark vẫn đóng cho tới khi
> Gate 0 implementation được Reviewer/user chấp nhận.

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 24-08-2026 09:24 +07
Notebook cần kiểm tra: notebooks/07_evaluation.ipynb
```

## 1. Bạn nhận được gì

Phase 7 cung cấp một cách đơn giản để kiểm tra Hue Foods RAG: hệ thống tìm đoạn
thông tin liên quan, sinh câu trả lời và dùng một model riêng để chấm độ chính
xác, đầy đủ và liên quan.

Bạn có thể chạy 20 câu mẫu trước, xem từng row trong bảng Gradio và xem hai file
CSV. Khi cần đánh giá đầy đủ, cùng code đó chạy bộ 104 câu.

## 2. Hệ thống hoạt động như thế nào

```text
câu hỏi -> tìm tài liệu -> tạo ngữ cảnh -> sinh câu trả lời
-> chấm ba tiêu chí -> hiển thị bảng và ghi CSV
```

Retrieval dùng MRR, nDCG và keyword coverage. Answer judge cho điểm integer 1–5
về accuracy, completeness, relevance cùng feedback ngắn. Phase này chưa so sánh
profiles/models và không có groundedness score.

## 3. Codex đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| Test Phase 7 | 8 passed | Loader, metrics, Qdrant, nano/mini và UI handler đi qua real path |
| Retrieval UI 20 câu | 20/20, bảng 20x9 | Named columns và thứ tự rows hiển thị đúng |
| Answer UI 20 câu | 20/20, bảng 20x9 | Hai model thật sinh/chấm và UI trình bày đúng trong run này |
| Retrieval 104 câu | 104/104 | MRR 0.8250, nDCG 0.8263, coverage 95.83% |
| Answer 104 câu | 103/104 | Điểm 4.37 / 4.02 / 4.19; một lỗi thật được giữ trong row |
| Notebook tạm | Run All thành công | Luồng học tập 22 cells gọi backend thật |

Câu `Quán nào mở cửa buổi tối, Mệ Kéo hay Bà Nga?` có một lần model trả source
ID không hợp lệ trong full run. Hệ thống không che lỗi, không retry và vẫn hoàn
thành 103 câu còn lại đúng thứ tự.

## 4. Cách bạn chạy lại

1. Bảo đảm Qdrant local đang chạy và repo-root `.env` có cấu hình OpenAI hợp lệ.
2. Mở `notebooks/07_evaluation.ipynb` từ repo root.
3. Chọn đúng project kernel rồi Run All từ trên xuống.
4. Kiểm tra:
   - notebook đọc đúng 20 câu;
   - retrieval result có MRR, nDCG và coverage;
   - answer result có ba điểm cùng feedback;
   - batch summary ghi rõ successful/failed;
   - cell cuối hiển thị app Gradio với hai nút và bảng named columns.

Notebook gọi Qdrant, `gpt-5.4-nano` và `gpt-5.4-mini` thật, nên có network và
paid API calls. Không lưu outputs hoặc secrets vào notebook repository.

## 5. Giới hạn và bước tiếp theo

Phase 7 hiện chỉ chạy profile `dense_only`. Một provider/model output đôi lúc có
thể thất bại; lỗi được ghi vào CSV thay vì che bằng fallback. So sánh profiles
và models chưa mở trong Phase 7.

Bạn đã xác nhận baseline Phase 7 ngày 24-08-2026 +07. Phase 0–6 simplicity
review sau đó đã hoàn tất. Phase 7 hiện chờ triển khai correction hẹp đã duyệt
và xác minh lại;
golden dataset được thảo luận ở session riêng trước khi sửa hoặc tạo dữ liệu.
Các số liệu 104 câu trong report này là historical evidence tại thời điểm
review, không phải row count hiện tại của hai CSV. Phase 8 vẫn đóng.
