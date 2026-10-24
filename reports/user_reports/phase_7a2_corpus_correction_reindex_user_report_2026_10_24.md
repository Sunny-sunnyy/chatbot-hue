# Báo cáo dành cho người dùng: Phase 7A2 - Sửa dữ liệu và tạo lại chỉ mục

Ngày đóng: 2026-10-24. Người viết: A. Chi tiết kỹ thuật: các report
`reports/phase_7a2_gate_{1,2,3}_*`.

## 1. Bạn nhận được gì

- Kho tri thức Huế đã sửa **25 chỗ mâu thuẫn** có căn cứ (ngày tháng, số liệu, địa
  chỉ, số văn bản…) trong 27 file. Bộ câu hỏi Golden chỉ phải sửa 1 câu trả lời mẫu.
- Chatbot full-corpus chạy trên **chỉ mục mới** `hue_full_corpus_7a2_e5_small_384`
  dựng từ dữ liệu đã sửa (8.459 đoạn), nên trả lời theo thông tin mới.
- Code dựng chỉ mục **gọn hơn nhiều** (bỏ khoảng 4.500 dòng code cũ): sửa dữ liệu
  về sau chỉ cần chạy lại một lệnh build, không phải sửa code.
- Qdrant được dọn: từ 16 xuống 3 collection.

## 2. Hệ thống hoạt động như thế nào

```text
Markdown đã sửa -> chia đoạn (không đổi) -> e5-small (chạy trên máy) + BM25
-> Qdrant (chỉ mục mới) -> tìm 5 đoạn liên quan -> gpt-6-luna trả lời kèm nguồn
```

Mỗi chỉ mục có một "phiếu build" ghi dấu vân tay từng file dữ liệu. Khi khởi động,
hệ thống so dấu vân tay với dữ liệu hiện tại; dữ liệu đổi mà chưa build lại thì
từ chối chạy, để không trả lời bằng chỉ mục cũ.

## 3. Agent đã chạy và quan sát gì

| Kiểm | Kết quả |
|---|---|
| Golden 176 + smoke 10 sau khi sửa dữ liệu | đạt |
| Chỉ mục mới: số đoạn, cấu trúc, vector | đạt (8.459 / 8.459, không lỗi) |
| Khởi động hệ thống (health) | đạt (HTTP 200) |
| 5 câu hỏi thật với `gpt-6-luna` | 4 đạt / 1 chưa đạt — **giống hệt trước khi sửa**; câu chưa đạt là lỗi cũ (không tìm ra bảng giá vé) |
| Dọn Qdrant | còn đúng 3 collection, số đoạn không đổi |

## 4. Cách bạn kiểm tra thêm nếu cần

Hỏi chatbot một câu có thông tin vừa sửa, ví dụ diện tích đầm Cầu Hai (giờ chỉ
còn "khoảng 104 km²"). Không bắt buộc kiểm thêm.

## 5. Giới hạn và bước tiếp theo

- **Qwen3-Embedding-8B chưa có chỉ mục.** Lần build thứ nhất trộn vector của 3 nhà
  cung cấp nên không đồng nhất; lần thứ hai (chỉ dùng Nebius) bị lỗi quá thời gian
  (504). Bạn chọn hoãn sang Phase 8.
- Câu hỏi về bảng giá vé vẫn chưa tìm đúng đoạn (F2); câu cần tổng hợp nhiều nguồn
  mới trích 1 nguồn (F1). Cả hai để Phase 8.
- Hai collection Foods cũ và vài notebook cũ (06, 08a, 08b) còn tên cũ — dọn sau
  Phase 7.
- **Tiếp theo:** Phase 7B — dựng bộ đánh giá và chạy đủ 176 câu để có điểm
  baseline; sau đó Phase 8 thử các cải tiến trên baseline đó.
