# Báo cáo dành cho người dùng: Giai đoạn 3 — Embedding toàn corpus và biểu diễn thưa

```text
Trạng thái: Đang chờ bạn xác nhận
Cập nhật lúc: 12-09-2026 +07
Notebook tham khảo: notebooks/03_embedding_models.ipynb
```

## 1. Bạn nhận được gì

Phase 3 đã chuẩn bị và kiểm chứng bốn lựa chọn embedding trên toàn kho tri thức
Huế. Qwen3-Embedding-0.6B đã chạy thật trên GTX 1650 bằng CUDA FP16; đồng thời hệ
thống có sparse state deterministic tương đương BM25 để Phase 4/5 sử dụng.

Dense inference hiện chỉ chạy trên mẫu 12 chunks như đã duyệt. Chưa tạo dense
vectors cho toàn bộ 8.460 chunks và chưa ghi Qdrant.

## 2. Hệ thống hoạt động như thế nào

Hệ thống lấy fresh chunks từ Phase 2, kiểm chúng khớp artifact đã đóng, quét
tokenizer trên toàn corpus, tạo sparse state, rồi lần lượt chạy bốn model dense
trên mẫu nhỏ. Mỗi model được giải phóng trước khi model tiếp theo chạy; Qwen dùng
GPU, ba model còn lại dùng CPU.

## 3. Codex đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| GPU WSL2 và PyTorch | Đạt: GTX 1650 4096 MiB, CUDA khả dụng | Máy hiện chạy được Qwen trên GPU |
| Offline preflight | Đạt: 205 files, 8.460 chunks, mẫu 12 | Luồng Phase 3 chạy bằng snapshots cục bộ |
| Qwen bounded inference | Đạt: CUDA FP16, eager, 1024D, batch 1 | Đúng hợp đồng model đã duyệt |
| Tokenizer toàn corpus | Đạt: không có input vượt giới hạn | Chunks Phase 2 phù hợp cả bốn model |
| Sparse state | Đạt: sinh lặp byte-identical và round-trip | Có đầu vào ổn định cho sparse retrieval sau này |
| Tests | 31 core và 35 extended đã đạt ở Correction 1 | Được dùng lại vì Correction 2 không đổi code/test |
| Notebook và Git diff | Đạt | Notebook sạch; diff không có lỗi whitespace |

## 4. Cách bạn kiểm tra thêm nếu cần

Bạn không bắt buộc chạy lại kỹ thuật để xác nhận. Nếu muốn xem luồng học tập,
mở `notebooks/03_embedding_models.ipynb`; máy cần WSL2 nhận GTX 1650 và các model
snapshots đã có trong cache. Run All phải cho thấy preflight PASS, thông tin GPU,
tokenizer/model summaries và sparse/BM25 equivalence. Notebook không dùng paid
API.

## 5. Giới hạn và bước tiếp theo

Phase 3 chưa encode dense toàn corpus, chưa dùng Qdrant và chưa chọn model thắng.
Đó là công việc của các phase sau với scope và approval riêng. Phase 4 hiện vẫn
đóng; xác nhận Phase 3 chỉ cho phép Reviewer bắt đầu thiết kế Phase 4, không tự
cho phép implementation hoặc mutation.

Sau khi đọc kết quả, bạn có thể phản hồi:

- Tôi xác nhận Phase 3.
- Tôi muốn sửa: <nội dung cần sửa>.
