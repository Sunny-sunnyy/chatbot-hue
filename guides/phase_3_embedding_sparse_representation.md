# Phase 3: Dense embedding và sparse representation

## Mục tiêu và giá trị cho người dùng

Phase 3 tạo hai biểu diễn có thể tái lập cho 572 canonical food chunks: dense vectors để tìm tương đồng ngữ nghĩa và sparse vectors để giữ tín hiệu từ khóa. Phase này khóa interface giữa text và vector trước khi Qdrant ingestion bắt đầu.

## Trạng thái

```text
Status: approved
Brainstorming level: Level 2 - standard
Owner: Codex Reviewer
Implementer: DeepSeek
```

Level 2 brainstorming đã được người dùng phê duyệt ngày 2026-08-11 +07. Người dùng đã chạy và xác nhận notebook `notebooks/03_embedding_models.ipynb` ngày 2026-08-11 +07. Phase 3 được approved; Phase 4 vẫn cần brainstorming riêng trước implementation.

## Dependency

- Phase 1–2 phải hoàn tất governance retrofit và được người dùng xác nhận.
- Input baseline là 572 chunks từ `chunk_foods_markdown()`.
- `backend/config/settings.yaml` đang dùng `intfloat/multilingual-e5-small`, 384 dimensions, CPU.
- Phase này không tạo, reset, upsert hoặc query Qdrant.

## Chức năng phải tạo

- Local dense embedding bằng SentenceTransformer, cache một model instance mỗi process.
- Phân biệt query text và document text khi model yêu cầu instruction/prefix.
- Batch embedding có giới hạn và thứ tự output khớp input.
- Vector normalization và dimension validation.
- Provider boundary đủ để thêm OpenRouter embeddings mà không thay đổi consumer interface.
- Custom sparse representation tương thích kỹ thuật đã dùng trong `llm_rag`.
- Unit tests không download model hoặc gọi API mặc định.
- Notebook học tập cho model metadata, sample vectors và resource preflight.

## Scope được đề xuất để brainstorming phê duyệt

### Trong scope

```text
backend/embedding/base.py
backend/embedding/embedder.py
backend/embedding/batch_embed.py
backend/embedding/sparse_embedder.py
backend/config/settings.yaml
backend/tests/test_embedder.py
backend/tests/test_sparse_embedder.py
notebooks/03_embedding_models.ipynb
```

Nếu OpenRouter adapter được implement ngay ở phase này, file dự kiến là:

```text
backend/embedding/openrouter_embedder.py
```

Adapter remote chỉ được test bằng mock. Live embedding run thuộc benchmark gate và cần user approval.

### Ngoài scope

- Qdrant client, collection schema hoặc ingestion.
- Retrieval, BM25 score fusion và reranking.
- Model quality winner selection.
- Live OpenRouter benchmark trước khi local end-to-end baseline có retrieval evidence.
- Tự tải nhiều Vietnamese-specific models mà chưa kiểm tra RAM, disk, license và exact model ID.

## Dense embedder interface contract

Consumer không được phụ thuộc trực tiếp vào SentenceTransformer hoặc HTTP payload. Interface tối thiểu:

```python
class BaseEmbedder:
    @property
    def model_id(self) -> str: ...

    @property
    def dimension(self) -> int: ...

    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...

    def embed_query(self, query: str) -> list[float]: ...
```

Behavior:

- `embed_documents([])` trả `[]` mà không load model hoặc gọi provider.
- Empty/whitespace query bị reject bằng validation error rõ ràng.
- Một output vector cho mỗi input text, cùng thứ tự.
- Mỗi vector là `list[float]`, finite và đúng `dimension`.
- Dense vectors được normalize khi cosine distance được dùng.
- Provider/model ID thực tế được expose cho logging và benchmark metadata, không log input corpus hoặc credentials.
- Không request-level fallback giữa embedding models vì vector spaces không tương thích.

## Local baseline bắt buộc

Model đầu tiên:

```text
Model ID: intfloat/multilingual-e5-small
Execution: local CPU
Expected dimension: 384
Library: sentence-transformers
Role: initial offline baseline
```

Preflight phải xác nhận:

- model đã có trong local cache hoặc người dùng cho phép download;
- RAM/disk đủ;
- dimension thực tế bằng config;
- `query:` và `passage:` prefixes được áp dụng đúng khuyến nghị của E5;
- Vietnamese sample có finite normalized vectors;
- latency và peak memory của sample batch được ghi, nhưng chưa tuyên bố quality winner.

Document indexing và query retrieval phải dùng đúng instruction pair. Không embed cùng raw string cho cả hai đường nếu model contract yêu cầu prefix khác nhau.

## OpenRouter embedding boundary

OpenRouter là provider remote cho vòng benchmark sau local baseline. Trước implementation/live run phải xác minh lại:

- exact catalog model ID của Qwen3 Embedding candidate;
- embeddings endpoint và response schema hiện hành;
- output dimension hoặc dimension parameter;
- input limits, batching support, pricing và Vietnamese/multilingual evidence;
- retry/timeout/rate-limit policy;
- `OPENROUTER_API_KEY` tồn tại trong environment nhưng không được in.

OpenRouter error không được tự đổi sang local embedding trong cùng collection. Run phải fail rõ để tránh index chứa trộn vector spaces.

## Optional Vietnamese embedding candidates

Các model sau chỉ vào benchmark mở rộng sau resource/model-card preflight:

| Candidate | Trạng thái guide | Gate |
|---|---|---|
| `huyydangg/DEk21_hcmute_embedding_v2` | Exact ID chưa được xác minh | Xác minh model card, dimension, training domain, license và resource |
| `bkai-foundation-models/vietnamese-bi-encoder` | Optional local | Xác minh license, pooling, instruction và resource |
| `AITeamVN/Vietnamese_Embedding_v2` | Optional local | Xác minh exact ID, dimension, license và benchmark relevance |
| Qwen3 Embedding | Remote priority family | Xác minh exact OpenRouter catalog ID trước mỗi paid batch |

Không dùng leaderboard tổng quát làm bằng chứng đủ cho domain foods Huế; winner chỉ đến từ Phase 8 controlled evaluation.

## Sparse representation contract

Sparse baseline kế thừa kỹ thuật từ `llm_rag`, nhưng implementation mới phải có English code/comments và tests rõ ràng.

Tokenization baseline:

```text
lowercase
replace non-word/non-space characters with spaces
split on whitespace
preserve Vietnamese Unicode word characters
```

Fit behavior:

- fit đúng toàn bộ canonical chunk texts theo deterministic order;
- tạo token-to-index vocabulary ổn định;
- đếm document frequency một lần mỗi unique token trong document;
- lưu `num_documents`;
- calling `fit()` lần hai phải reset state hoặc bị reject rõ, không cộng dồn âm thầm.

Encode behavior:

```text
idf(term) = log((num_documents + 1) / (document_frequency + 1)) + 1
value = term_frequency * idf(term)
```

Output:

```python
{
    "indices": [0, 4, 9],
    "values": [1.2, 2.4, 1.0],
}
```

Invariants:

- indices và values cùng length;
- indices là unique integers thuộc vocabulary;
- values là finite positive floats;
- unknown query tokens bị bỏ qua;
- empty text trả hai lists rỗng;
- encode trước fit bị reject rõ;
- vocabulary/IDF state có thể tái tạo từ cùng corpus.

Phase 3 không tuyên bố sparse retrieval quality. Sparse vector chỉ là representation được Phase 4 lưu và Phase 5 có thể dùng gián tiếp qua cùng tokenization/BM25 corpus.

## Batching và performance contract

- `batch_size` lấy từ config, baseline là 64 nhưng phải giảm nếu CPU/RAM preflight yêu cầu.
- Không giữ hai bản sao lớn không cần thiết của toàn corpus vectors.
- Local model load đúng một lần mỗi process.
- Remote batching tuân provider limit; không gửi toàn corpus trong một request không bounded.
- Ghi elapsed time, item count, provider/model và dimension; không log full texts.

## Brainstorming bắt buộc trước implementation

Codex phải làm rõ với người dùng:

1. Model đã có trong local Hugging Face cache hay cần cho phép download `multilingual-e5-small`.
2. Giữ `batch_size=64` hay giảm sau CPU/RAM sample preflight.
3. Provider interface có implement OpenRouter adapter ngay trong Phase 3 bằng mock, hay chỉ khóa interface rồi thêm adapter khi benchmark remote bắt đầu.
4. Sparse state chỉ tái fit từ corpus hay cần artifact serialization trong MVP.
5. Dimension được lấy từ model runtime và so với config theo fail-fast policy nào.

Decision record phải ghi exact lựa chọn, evidence và revisit trigger. Đây là năm câu hỏi thay đổi implementation/test; không thêm câu hỏi không ảnh hưởng design.

## Decision record đã được phê duyệt

```text
Decision: Dùng 572 chunks từ chunk_foods_markdown() theo thứ tự ổn định làm corpus canonical cho Phase 3, thay mọi tham chiếu lịch sử 366 chunks.
Approved by: User
Approval date +07: 2026-08-11
Evidence: User xác nhận sau khi đối chiếu Project Status, Phase 2 evidence và Phase 3 guide.
Affected scope: Dense/sparse fit, tests, notebook và acceptance criteria của Phase 3.
Revisit trigger: Canonical chunking của Phase 2 thay đổi và được người dùng phê duyệt.
```

```text
Decision: Dùng intfloat/multilingual-e5-small đã có trong local cache, CPU và batch_size=64 là mức tối đa ban đầu; chỉ giảm sau local smoke có evidence CPU/RAM không đủ.
Approved by: User
Approval date +07: 2026-08-11
Evidence: Local cache preflight xác nhận model hiện diện; user xác nhận batch policy.
Affected scope: Local SentenceTransformer embedder, batching, local smoke và notebook.
Revisit trigger: Local smoke vượt resource limit hoặc model cache không còn dùng được.
```

```text
Decision: Implement OpenRouter embedding adapter live-ready trong Phase 3. Adapter dùng endpoint embeddings hiện hành, input_type tách query/document, batch bounded, timeout 30 giây và tối đa hai retries cho 429 hoặc lỗi 5xx; không retry lỗi auth/config/input và không fallback sang E5.
Approved by: User
Approval date +07: 2026-08-11
Evidence: User chọn live-ready adapter; OpenRouter official embeddings API và catalog model qwen/qwen3-embedding-0.6b được reviewer xác minh read-only.
Affected scope: backend/embedding/openrouter_embedder.py, settings embedding và unit tests mock HTTP client.
Revisit trigger: OpenRouter đổi endpoint/schema/catalog, provider limits thay đổi, hoặc user không còn cho phép live embedding run.
```

```text
Decision: SparseEmbedder reset state và fit lại từ toàn bộ 572 canonical chunk texts mỗi process; không serialize vocabulary/IDF artifact trong MVP Phase 3. Consumers nhận SparseEmbedder instance tường minh, không dùng mutable module global.
Approved by: User
Approval date +07: 2026-08-11
Evidence: User xác nhận đề xuất sau khi reviewer đối chiếu sparse pipeline của llm_rag.
Affected scope: SparseEmbedder, Phase 4 point building boundary và Phase 5 BM25 startup boundary.
Revisit trigger: Corpus đủ lớn để startup fit trở thành bottleneck có đo đạc, hoặc sparse retrieval/native state cần artifact versioned.
```

```text
Decision: Dimension runtime phải khớp dimension cấu hình; mismatch fail-fast trước khi vector được trả về hoặc index. Không tự sửa config, pad/truncate vector hay fallback sang model khác. Remote model có dimension khác cần experiment/collection mới và reindex được user phê duyệt.
Approved by: User
Approval date +07: 2026-08-11
Evidence: User xác nhận fail-fast policy.
Affected scope: BaseEmbedder, local/remote validation, config và Phase 4 collection contract.
Revisit trigger: User phê duyệt model hoặc dimension mới cho experiment khác.
```

## Nhiệm vụ của DeepSeek Implementer

- Viết failing tests cho empty input, output order, dimension mismatch, model cache và sparse state trước implementation.
- Mock SentenceTransformer/OpenRouter client trong unit tests; default tests không download hoặc gọi network.
- Dùng English identifiers, comments và docstrings.
- Không thêm Qdrant dependency behavior vào Phase 3 modules.
- Tạo notebook import runtime modules, không copy embedding/sparse algorithms.
- Ghi model cache/resource evidence đã được phép vào implementation report, không ghi private cache path nếu không cần.

## Notebook bắt buộc

`notebooks/03_embedding_models.ipynb` phải:

- giải thích dense vs sparse bằng tiếng Việt;
- import Phase 2 chunks và Phase 3 modules;
- Run All chunk 572 foods và tạo dense vectors thật bằng local E5 cache-only
  (`HF_HUB_OFFLINE=1`), không có fake fallback;
- hiển thị model ID, dimension, vector norms, sparse vocabulary size và sample sparse indices/values;
- không gọi OpenRouter mặc định;
- giữ committed outputs rỗng và `execution_count=null`.

## Tests và validation dự kiến

Unit tests tối thiểu:

- empty dense batch;
- query/document instruction separation;
- vector count/order/dimension/norm;
- model cache chỉ khởi tạo một lần;
- provider error không fallback sang vector space khác;
- deterministic sparse vocabulary;
- TF-IDF values trên corpus nhỏ biết trước;
- empty/unknown tokens;
- fit-state reset/reject behavior.

Commands sau chỉ chạy sau khi dependency/model access đã được người dùng cho phép:

```bash
cd backend
uv run python -m py_compile embedding/base.py embedding/embedder.py embedding/batch_embed.py embedding/sparse_embedder.py
uv run pytest tests/test_embedder.py tests/test_sparse_embedder.py -q --tb=short
```

Live/local model smoke command phải được ghi chính xác trong implementation report sau brainstorming; không đưa secret vào command.

## Security, reliability và performance gates

- Không đọc `.env`; chỉ environment access trong provider adapter được phê duyệt.
- Không log texts, vectors đầy đủ, key hoặc raw provider response.
- Dimension mismatch fail trước Phase 4 ingestion.
- Partial remote batch không được coi là complete corpus.
- Model download và paid API cần approval riêng.
- Không dùng GPU mặc định khi resource preflight chưa xác nhận.

## Tiêu chí phê duyệt Phase 3

- Local E5 interface và sparse representation đúng contracts.
- Unit tests pass mà không cần network/model download.
- Approved local smoke xác nhận 384-dimensional normalized vectors.
- Sparse vocabulary non-empty và deterministic trên 572 chunks.
- OpenRouter boundary không cho phép mixed vector spaces hoặc silent fallback.
- Notebook an toàn và report đầy đủ.
- User report phản ánh đúng validation/limitations và được người dùng xác nhận cùng notebook.
- Không có Qdrant mutation hoặc live paid run ngoài approval.

## Reports và cập nhật trạng thái

Sau implementation thực tế:

```text
reports/phase_3_embedding_sparse_representation_implementation_report.md
reports/phase_3_embedding_sparse_representation_codex_review.md
reports/user_reports/phase_3_embedding_sparse_representation_user_report.md
```

Benchmark evidence liên quan model/resource được nối vào `reports/hue_foods_rag_benchmark.md`. Sau technical review đạt, Codex tạo user report `pending`; chỉ cập nhật `Project_Status.md` sau khi người dùng xác nhận notebook/report.

## Bước tiếp theo

Sau khi Phase 1–2 trở lại `approved`, brainstorm Phase 3. Chỉ sau user confirmation của Phase 3 mới mở Phase 4.
