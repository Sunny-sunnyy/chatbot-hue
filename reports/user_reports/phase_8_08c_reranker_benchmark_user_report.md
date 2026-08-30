# Báo cáo dành cho người dùng: Giai đoạn 8 — Benchmark Reranker MiniLM 08c

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 30-08-2026 +07
Notebook cần kiểm tra: notebooks/08c_reranker_benchmark.ipynb
```

## 1. Bạn nhận được gì

Notebook 08c so sánh kết quả giữ nguyên thứ hạng với việc dùng MiniLM reranker
trên ba bộ Top-10 cố định từ benchmark retrieval 08b. Mỗi bộ gồm 45 câu hỏi
Golden V3, chạy MiniLM ba lần và lưu cả kết quả tổng hợp lẫn bằng chứng từng câu.

Kết quả hiện tại không ủng hộ đưa MiniLM reranker này vào production. Cả ba phép
so sánh đều không vượt toàn bộ quality/category guardrails; không pairing nào có
`eligible=True` hoặc clear gain.

## 2. Hệ thống hoạt động như thế nào

Notebook đọc ba danh sách ứng viên đã được 08b cố định, nạp MiniLM local đúng một
lần, warm up một lần rồi rerank từng danh sách từ 10 xuống 5 kết quả. Hệ thống
so sánh recall, MRR, nDCG, category regressions, latency và memory với nhánh
không rerank.

Hai artifact cuối được reconcile lại từ bằng chứng từng câu. Numeric boundary
hiện từ chối dữ liệu thiếu, sai kiểu, NaN hoặc vô hạn thay vì cho artifact lỗi
được đánh dấu hoàn tất.

## 3. Codex đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| Focused test suite | Đạt — 61 tests | Numeric reconciliation và các tamper boundaries không có regression quan sát được |
| Independent invalid-data probes | Đạt — 9/9 bị từ chối | Candidate sai, latency/resource sai và NaN không thể tạo false completion |
| Artifact reconciliation | Đạt — 60/135 | Summary và per-case evidence hiện đầy đủ, nhất quán |
| MiniLM trên E5-small | ΔnDCG@5 `-0.0703` | Chất lượng giảm rõ; không eligible |
| MiniLM trên HuyDang dense | ΔnDCG@5 `+0.0065` | Cải thiện quá nhỏ và vẫn vi phạm category guardrails |
| MiniLM trên hybrid diagnostic | ΔnDCG@5 `-0.0605` | Chất lượng giảm và production safety không đạt |
| Warm latency p50/p95 | `246.13/538.79`, `231.58/487.66`, `248.27/481.02 ms` | Tốc độ local nằm dưới latency ceiling, nhưng quality gates vẫn chặn selection |

Reviewer không chạy lại model trong complexity reset vì producer, notebook và
artifacts không đổi. Real single-load Notebook Run All trước đó đã exit 0 và
được reuse trong cùng implementation series.

## 4. Cách bạn chạy lại

Mở `notebooks/08c_reranker_benchmark.ipynb` từ repository root, bảo đảm môi
trường `uv` đã sẵn sàng và model
`cross-encoder/ms-marco-MiniLM-L-6-v2` có trong local cache. Chọn **Run All** từ
trên xuống.

Bạn cần quan sát:

- model load một lần và warm up một lần;
- technical smoke pass trước benchmark chính;
- reconciliation trả `True` với 60 summary rows và 135 case records;
- cả ba pairing có `eligible=False` và `clear_gain=False`;
- hybrid pairing có `production_safety=False`.

Notebook dùng model local, không gọi paid API. Source notebook trong repository
được giữ sạch outputs và execution counts.

## 5. Giới hạn và bước tiếp theo

- 08c chỉ đánh giá Foods corpus và Golden V3; kết quả không đại diện cho toàn bộ
  dữ liệu văn hóa/du lịch Huế.
- MiniLM hiện tại không được chọn làm reranker finalist và production không nên
  cutover dựa trên evidence này.
- Bạn đã xác nhận Notebook 08c ngày 30-08-2026; work package hiện `approved`.
- Phase 8 tổng thể vẫn `not_ready`. Bước tiếp theo là thiết kế workstream mở rộng
  đầy đủ curated corpus dưới `knowledge-base-hue/`, combined Golden Dataset và
  isolated full-corpus index; chưa authorize thay đổi dữ liệu, index hoặc
  production.
- MiniLM hiện tại không có finalist; production configuration giữ nguyên.
- User đã cấp quyền riêng để commit và push work package 08c cùng approval
  closure. Quyền này không mở rộng sang implementation post-08c.
