# Báo cáo dành cho người dùng: Giai đoạn 4–5 - Qdrant và Retrieval đơn giản

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 25-08-2026 +07
Notebook cần kiểm tra: notebooks/03_embedding_models.ipynb,
notebooks/04_qdrant_ingestion.ipynb, notebooks/05_retrieval_profiles.ipynb
```

## 1. Bạn nhận được gì

Hue Foods RAG đã có candidate Qdrant mới chỉ lưu dense vectors cần thiết, thay
cho schema active cũ còn giữ sparse vectors không được truy vấn. Ba chế độ
`dense_only`, `hybrid_no_rerank` và `hybrid_rerank` vẫn hoạt động như trước bằng
E5, Python BM25 và MiniLM thật.

Code ingestion/retrieval đã bỏ sparse embedder, wrapper reranker, client cache,
manual retry, fingerprints và optional stack không cần thiết. Candidate chưa tự
động trở thành active nên hệ thống vẫn có cổng kiểm soát trước cutover.

## 2. Hệ thống hoạt động như thế nào

```text
572 curated chunks
-> E5 dense vectors
-> dense-only Qdrant candidate
-> dense retrieval
-> optional Python BM25 fusion
-> optional MiniLM reranking
-> bounded JSON context
```

Active cũ vẫn đọc được trước cutover. Ingestion candidate tiếp tục yêu cầu strict
dense-only schema; retrieval startup chỉ bỏ qua sparse field lịch sử không dùng
trên active cũ.

## 3. Codex đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| Active/candidate state | Cùng 572 points; không có collection test còn sót | Active không bị mutate và candidate đầy đủ |
| 104 × 3 comparison | 104/104 thứ tự IDs giống nhau ở cả ba profiles | Bỏ stored sparse không làm đổi retrieval ranking |
| Notebook 03 | 572 × 384, norm 1.0, Run All đạt | Dense E5 pipeline chạy thật |
| Notebook 04 | Candidate dense 384/cosine, sparse `None`, Run All đạt | Candidate đúng pure dense schema |
| Notebook 05 | Ba profiles trả 10/10/5 documents, Run All đạt | E5, BM25 và MiniLM chạy đúng stage |
| Focused tests | 27 passed, 1 warning | Các hành vi Phase 4–5 cần giữ được bảo vệ |
| Full non-paid suite | 90 passed, 6 paid tests deselected, 19 warnings | Shared backend regression check đạt mà không gọi paid generation/judge |

## 4. Cách bạn chạy lại

Mở repo bằng Jupyter và Run All theo thứ tự:

1. `notebooks/03_embedding_models.ipynb`: quan sát 572 × 384 vectors và norm gần
   1.0.
2. `notebooks/04_qdrant_ingestion.ipynb`: cần Qdrant local và candidate
   `hue_foods_e5_small_384_dense`; quan sát count 572, dense 384/cosine và không
   có sparse vectors.
3. `notebooks/05_retrieval_profiles.ipynb`: quan sát cả ba profiles, score fields
   theo đúng stage và bounded context.

Ba notebook dùng model local/Qdrant thật và không gọi paid API. Repository
notebooks hiện sạch outputs; kết quả Run All chỉ nằm trong phiên kiểm tra của
bạn.

## 5. Giới hạn và bước tiếp theo

- Candidate chưa được cutover; config vẫn trỏ active
  `hue_foods_e5_small_384`.
- MiniLM vẫn là local latency baseline và có retrieval metrics thấp hơn hai
  profiles còn lại trong evidence hiện có; Phase 8 mới được chọn winner.
- Sáu paid generation/judge/chat tests không chạy vì generation không thuộc
  thay đổi Phase 4–5.
- Implementation report còn lỗi đếm nhỏ ở evaluation tests và chưa ghi exact
  fresh suite counts; Codex review đã ghi số observed đúng, không ảnh hưởng kết
  quả technical review.

Bạn đã xác nhận Giai đoạn 4–5 ngày `25-08-2026 +07`. Candidate chưa được
cutover vì xác nhận phase và cho phép cutover là hai quyết định riêng.
Collection active cũ sẽ được giữ làm rollback; cutover hoặc xóa nó cần approval
riêng.
