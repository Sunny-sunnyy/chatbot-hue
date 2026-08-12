# README_config

## Nhiệm Vụ Của Thư Mục

Thư mục `config` chứa các file cấu hình YAML của Hue Foods RAG MVP.

- `settings.yaml`: cấu hình tổng thể ứng dụng và pipeline RAG.
- `logging.yaml`: cấu hình logging.
- `README_config.md`: mô tả thư mục và cách dùng các file cấu hình.

## settings.yaml

### Cách chọn retrieval profile

Đổi giá trị `active_profile` ở đầu file:

```yaml
active_profile: dense_only
```

Các profile có sẵn:

| Profile | Dense retrieval | BM25 hybrid score | CrossEncoder rerank |
|---|---:|---:|---:|
| `dense_only` | yes | no | no |
| `hybrid_no_rerank` | yes | yes | no |
| `hybrid_rerank` | yes | yes | yes |

Mọi profile dùng chung một code path; profile chỉ thay đổi hành vi qua config.

### Các nhóm cấu hình

- `knowledge_base`: thư mục curated knowledge base, globs include và exclude parts.
- `embedding`: model SentenceTransformer, vector size, device, batch size.
- `vector_database`: Qdrant URL, active collection name, vector size, distance, timeout, upsert batch size và retry limit. `reset_collection` luôn là `false` khi ingestion chạy; xóa collection chỉ qua command `vectorstore.reset` riêng với user approval và confirmation string chính xác.
- `retrieval`: top_k, candidate multiplier, score threshold, dense/bm25 weights.
- `reranking`: CrossEncoder model, device, top_k cuối cùng.
- `llm`: provider, answer model, temperature, max output tokens.
- `evaluation`: đường dẫn test file, judge model.

### Ghi chú quan trọng

- Không đặt API key trong file này. Key lấy từ `.env` hoặc environment khi có phase sử dụng model.
- `embedding.vector_size` và `vector_database.vector_size` phải khớp nhau.
- Đổi `embedding.model` hoặc vector size cần: 1) user approval; 2) chạy exact `vectorstore.reset` command với confirmation string và expected count; 3) giữ `vector_database.reset_collection: false`; 4) chạy ingestion để tạo lại collection.
- Không bao giờ đặt `vector_database.reset_collection: true`; ingestion từ chối giá trị này và collection chỉ bị xóa qua command reset riêng.
- Model ID của OpenAI (`llm.answer_model`, `evaluation.judge_model`) phải được xác minh với tài liệu chính thức trước khi chạy.

## logging.yaml

Cấu hình logging gồm:

- `formatters.simple`: định dạng log.
- `handlers.console`: ghi log ra stdout.
- `handlers.file`: ghi log vào `logs/application.log` trong `backend/`.
- `loggers`: logger theo module (`ingestion`, `embedding`, `scoring`, `vector_database`, `llm`, `retrieval`, `reranking`, `evaluation`, `chat`).
- `root`: logger mặc định.

## Cách Hoạt Động

- `core/settings_loader.py` đọc `settings.yaml` và validate `active_profile`.
- `core/logging_setup.py` đọc `logging.yaml`, tạo thư mục `logs` nếu cần và áp dụng config logging.

Các file trong thư mục này không tự chạy. Chúng được các module trong `core` đọc và chuyển thành cấu hình Python.
