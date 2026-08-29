# Báo cáo dành cho người dùng: Giai đoạn 8 — Benchmark Dense Embedding 08a

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 29-08-2026 +07
Notebook cần kiểm tra: notebooks/08a_embedding_benchmark.ipynb
```

## 1. Bạn nhận được gì

Notebook 08a giúp bạn so sánh dense embedding local trên cùng 572 đoạn dữ liệu
ẩm thực Huế và 45 câu hỏi Golden V3. Danh mục executable cuối cùng chỉ còn
E5-small, Huydang DEk21 và E5-base; MiniLM-L12, Qwen, BGE-M3 và E5-large đã bị
loại khỏi mọi đường chạy local.

Kết quả hiện có cho thấy E5-small vẫn là đối chứng cân bằng nhất: nDCG@5 và
MRR@5 cao hơn hai candidate hiện hành, trong khi độ trễ thấp. E5-base có Recall@5 cao hơn
nhẹ nhưng xếp hạng tổng thể thấp hơn và chậm hơn. Đây là bằng chứng cho bước lựa
chọn sau, chưa thay đổi cấu hình production.

## 2. Hệ thống hoạt động như thế nào

Notebook đọc 45 câu hỏi chuẩn và tạo 572 chunks bằng backend production. Mỗi
model mã hóa cùng dữ liệu vào một collection Qdrant cô lập, chạy dense retrieval
ba lần, rồi trình bày chất lượng, độ trễ, tài nguyên và regression theo category.
Active collection production chỉ được đọc để đối chiếu an toàn.

## 3. Codex đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| Focused tests | Đạt — 23 tests | Metric, guardrail, CSV và safety boundary vẫn đúng |
| Catalog runtime | Đạt — 3 settings, 2 candidates | Không còn MiniLM/Qwen/BGE/E5-large trong đường chạy |
| Qdrant active | Đạt — 572 points, 384D cosine | Production collection giữ nguyên và chỉ được đọc |
| Ba collection cô lập | Đạt — mỗi collection 572 points, đúng 384/768/768D | Evidence của ba model hiện hành còn đầy đủ |
| Golden Dataset V3 | Đạt — 45 full + 10 smoke | Input benchmark không bị sửa |
| CSV | Đạt — 50 data rows | Giữ 30 rows hiện hành, 10 MiniLM và 10 Qwen historical rows |
| Notebook canonical | Đạt — output rỗng, execution count null | Repo không lưu output chạy máy cá nhân |

Codex không chạy lại model sau cleanup vì correction không đổi encoding,
retrieval, scoring hoặc metric của ba model giữ lại. Evidence 3/3 hiện có được
giữ; bạn đã chạy Notebook 08a thành công và xác nhận kết quả.

## 4. Cách bạn chạy lại

Mở `notebooks/08a_embedding_benchmark.ipynb`, bảo đảm Qdrant đang chạy và môi
trường đã được đồng bộ bằng `uv`, rồi chọn **Run All** từ trên xuống. Notebook
chạy local CPU FP32, không gọi paid API.

Bạn cần quan sát:

- bảng settings chỉ có ba model;
- control E5-small chạy riêng, sau đó đúng hai candidates chạy tuần tự;
- mỗi setting hoàn tất 3/3 repetitions;
- các bảng quality/category/latency/resource được hiển thị;
- active snapshot trước và sau giống nhau;
- không có MiniLM/Qwen trong run loop hoặc collection được tạo lại.

## 5. Giới hạn và bước tiếp theo

Notebook 08a chỉ đánh giá dense embedding. Nó chưa benchmark BM25/fusion,
reranker, generation, paid API và chưa cutover production. Phase 8 tổng thể vẫn
chưa approved; bước tiếp theo là research và brainstorming exact Notebook 08b.
Implementation/run 08b vẫn cần một approval riêng.
