# Báo cáo dành cho người dùng: Giai đoạn 8 — Benchmark Retrieval và Fusion 08b

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 30-08-2026 +07
Notebook cần kiểm tra: notebooks/08b_retrieval_fusion_benchmark.ipynb
```

## 1. Bạn nhận được gì

Notebook 08b so sánh dense retrieval, BM25, TF-IDF, rescore và hai cách fusion
trên cùng 572 đoạn dữ liệu ẩm thực Huế cùng 45 câu hỏi Golden V3. Tổng cộng 20
cấu hình đã được đánh giá ba lần và lưu evidence theo từng câu hỏi.

Hybrid retrieval tăng recall tổng thể so với dense control, nhưng không có cấu
hình BM25 hoặc TF-IDF nào được chọn làm finalist. Lý do là thứ hạng trong nhóm
`relationship` giảm quá guardrail đã duyệt, dù cả 14/14 câu vẫn có hit. Hệ thống
đã giữ quyết định fail-closed thay vì chọn một winner chỉ dựa vào metric tổng.

## 2. Hệ thống hoạt động như thế nào

Notebook đọc cùng corpus và Golden V3, hiệu chuẩn BM25/tokenizer, kiểm tra TF-IDF
trong một Qdrant collection cô lập, rồi đọc hoặc chạy tuần tự 20 cấu hình. Mỗi
kết quả đi qua cùng metric và category guardrails trước khi được phép trở thành
finalist. Active production collection chỉ được đối chiếu trước/sau và không bị
thay đổi.

Tokenizer Unicode hiện hành được giữ vì Underthesea không tạo cải thiện đủ lớn
để biện minh thêm độ phức tạp.

## 3. Codex đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| Safety probes | Đạt | Thiếu live client hoặc sai experiment identity đều bị từ chối; quoted secrets không bị persist |
| Relevant test suite | Đạt — 85 tests | Calibration, retrieval, fusion, checkpoint và fail-closed contracts không có regression quan sát được |
| Notebook Run All | Đạt — 20 settings | Source notebook chạy end-to-end qua Qdrant thật và đọc đủ experiment matrix |
| Reconciliation | Đạt — 70/200/900 records | Calibration, summary và per-case evidence đầy đủ, nhất quán |
| Finalist selection | BM25 `None`, TF-IDF `None` | Không candidate nào vượt toàn bộ guardrails; production chưa nên cutover |
| Production isolation | Đạt — active collection vẫn 572 points | Review không thay đổi dữ liệu retrieval đang hoạt động |
| Artifact stability | Đạt | Tests và notebook không làm đổi bốn durable evidence files |

Một cảnh báo thư viện về tên method embedding dimension vẫn xuất hiện; kích
thước vector và retrieval behavior hiện tại không bị ảnh hưởng.

## 4. Cách bạn chạy lại

Mở `notebooks/08b_retrieval_fusion_benchmark.ipynb` từ repository root, bảo đảm
Qdrant local đang chạy, project environment đã được đồng bộ bằng `uv`, `.env`
trỏ đúng local services và các local model cache của 08a còn sẵn. Chọn **Run
All** từ trên xuống.

Bạn cần quan sát:

- active production snapshot có 572 points;
- catalog có đúng 20 retrieval settings;
- reconciliation trả `True` với 70 calibration rows, 200 result rows và 900
  case records;
- `BM25 Finalist: None` và `TF-IDF Finalist: None`;
- bảng category cho thấy `relationship` không vượt guardrail;
- production snapshot trước/sau giống nhau.

Notebook dùng model local và Qdrant local, không gọi paid API. Kết quả cached đã
hoàn thành được reuse; xóa artifacts/collections hoặc bật mutation sẽ không còn
là quy trình kiểm tra read-only được review ở đây.

## 5. Giới hạn và bước tiếp theo

- 08b chỉ đánh giá retrieval/fusion; chưa đánh giá reranker, generation hoặc
  chất lượng câu trả lời end-to-end.
- Không có sparse finalist đồng nghĩa production configuration phải giữ nguyên;
  đây là kết quả khoa học hợp lệ, không phải experiment bị thiếu.
- Bạn đã xác nhận Notebook 08b ngày 30-08-2026; work package hiện `approved`.
- Phase 8 tổng thể vẫn `not_ready`. Bước tiếp theo là research và brainstorming
  exact Notebook 08c; implementation/run vẫn cần design/spec/plan và approval
  riêng.
- Codex chưa commit hoặc push thay đổi.

User đã cấp quyền riêng để commit và push closure cùng toàn bộ work package 08b
sau final diff check; quyền này không mở rộng sang implementation/run 08c.
