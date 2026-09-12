# Phase 3 — Full-corpus dense embedding và sparse representation

```text
Status: approved by User 2026-09-12
Date: 2026-09-12 +07
Owner: Codex Reviewer
Runtime authorization: none
Dependency: Full-corpus Phase 2 User-approved closure
```

## 1. Mục tiêu

Phase 3 xác lập đường embedding và sparse representation cho toàn bộ 8.460 chunks
đã quan sát từ Phase 2, trước khi Phase 4 tạo Qdrant points hoặc collections.
Kết quả cần chứng minh bốn dense candidates chạy đúng preprocessing, revision,
dimension và device đã chốt; đồng thời tạo một sparse state deterministic dùng
chung cho indexing và query về sau.

Phase này chỉ kiểm chứng dense inference trên một tập mẫu nhỏ, cố định. Việc
encode dense toàn corpus và mọi Qdrant write thuộc Phase 4.

## 2. Thuật ngữ và lifecycle

Tài liệu active và tương lai dùng `Phase` làm đơn vị thiết kế, triển khai,
review và closure; không tạo thêm một lớp phân chia thực thi song song. Guide
Phase 3 là entrypoint canonical lâu dài. Written spec này khóa behavior; plan
khóa paths, thứ tự, commands và quyền; Review Contract khóa evidence và kiểm
tra độc lập.

Các report/tên artifact lịch sử đã đóng không bị đổi hồi tố. Sau khi spec, plan
và Review Contract Phase 3 được User duyệt, các tài liệu Markdown canonical và
active liên quan được đồng bộ sang terminology Phase trước khi giao Implementer.

## 3. Dependency và ranh giới

Input canonical là output Phase 2 đã được User phê duyệt closure:

- 205 curated Markdown files, sorted và unique;
- 8.460 deterministic chunks;
- Representation A và exact source locators;
- ba condition rules;
- zero blocking errors và zero oversized groups;
- max token đã quan sát `366/512`, `366/512`, `255/256` cho ba model
  tokenizer của Phase 2.

Các counts trên là observed dependency evidence, không phải hard-coded product
invariants. Phase 3 phải đọc fresh Phase 2 output và fail closed nếu identity,
count hoặc tokenizer input không khớp artifact được giao.

Trong scope:

- explicit full-corpus model contracts cho bốn dense candidates;
- local model resolution/download tại exact pinned revisions;
- bounded real-model document/query preflight;
- full-corpus tokenizer scan với preprocessing thật và `truncation=False`;
- CUDA readiness và Qwen GPU preflight trên GTX 1650 4 GB;
- deterministic sparse state trên toàn bộ Representation A corpus;
- JSON evidence không chứa dense vectors;
- cập nhật Notebook 03 để minh họa đường backend thật.

Ngoài scope:

- dense encoding toàn bộ 8.460 chunks;
- Qdrant schema, point construction, collection creation hoặc mutation;
- active Foods runtime/config/wiring, collections và Golden datasets;
- retrieval, fusion, reranker, context, generation, API hoặc frontend;
- Representation B;
- quality benchmark, model winner, threshold hoặc cutover;
- quantization, FlashAttention, CPU fallback cho Qwen hoặc automatic device/
  dtype/batch/revision changes.

## 4. Representation A

Phase 3 dùng nguyên `search_text` đã được Phase 2 tạo bởi
`build_representation_a_search_text()`:

```text
title
heading path nối bằng " > " khi có
evidence parts theo thứ tự nguồn
```

Không thêm nhãn `Tiêu đề:`, `Nội dung:` hoặc một renderer thứ hai. Dense model
preprocessing được áp sau renderer này và không được ghi ngược vào payload hay
`evidence_parts`. Sparse representation dùng chính `search_text`, không dùng
dense prefix/instruction.

## 5. Dense candidate contract

| Candidate | Pinned revision | Dimension | Device/dtype | Input contract |
|---|---|---:|---|---|
| `intfloat/multilingual-e5-small` | `614241f622f53c4eeff9890bdc4f31cfecc418b3` | 384 | CPU/FP32 | document `passage: `, query `query: ` |
| `intfloat/multilingual-e5-base` | `d128750597153bb5987e10b1c3493a34e5a4502a` | 768 | CPU/FP32 | document `passage: `, query `query: ` |
| `CODE4LIFEOFFICIAL/huydang-dek21-embedding` | `517f1af7dd04a57194f1de2990f0c6ede0a3109b` | 768 | CPU/FP32 | PyVi 0.1.1 cho document và query; không E5 prefix |
| `Qwen/Qwen3-Embedding-0.6B` | `97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3` | native 1024 | GTX 1650/CUDA FP16 | custom English instruction chỉ cho query; document nguyên `search_text` |

Model được load tuần tự, dùng Sentence Transformers trực tiếp và được release
trước model kế tiếp. Không tạo provider/plugin framework hoặc dùng benchmark
collection settings làm runtime contract Phase 3.

Mọi output phải:

- giữ đúng số lượng và thứ tự input;
- có exact configured dimension;
- chỉ chứa finite values;
- được L2-normalize với norm xấp xỉ `1`;
- đến từ exact revision/device/dtype đã khai báo.

Cosine similarity có thể được ghi như diagnostic nhưng không có threshold PASS
và không được dùng chọn winner trong Phase 3.

### 5.1 Qwen query instruction

Qwen document input là Representation A không instruction. Query dùng chính xác:

```text
Instruct: Given a Vietnamese question about Hue culture, heritage,
festivals, performing arts, food, and travel, retrieve relevant
Vietnamese passages that answer the question.
Query: {question}
```

Qwen dùng native 1024D; không `truncate_dim`, slicing hoặc PCA. Biến thể 384D
đã có Foods/CPU historical rejection evidence và không được đưa lại vào Phase 3.

## 6. GPU readiness và Qwen gate

Qwen là candidate thứ tư có điều kiện sử dụng tiếp: nếu toàn bộ Phase 3 đạt,
Qwen 1024D trở thành candidate cho Phase 4 indexing và benchmark sau đó.
Phase 3 không được đánh complete nếu Qwen chưa chạy thật trên GTX 1650 qua CUDA.

Trình tự readiness:

1. User thực hiện mọi thay đổi cần quyền Windows/Administrator.
2. NVIDIA Windows driver phải cung cấp CUDA passthrough cho WSL2; không cài
   NVIDIA Linux display driver trong Ubuntu.
3. `/usr/lib/wsl/lib/nvidia-smi` phải nhận GTX 1650 và VRAM thật.
4. Đúng project environment phải báo `torch.cuda.is_available() == True`, nhận
   đúng device và có CUDA runtime usable.
5. Qwen được load hoàn toàn bằng CUDA FP16, batch size 1, rồi chạy document và
   query smoke với model tensors/inference thực sự ở CUDA.
6. Evidence ghi Torch/CUDA/device identity cùng allocated, reserved và peak VRAM.

Trạng thái khảo sát trước implementation là
`GPU access blocked by the operating system`. Đây là observed precondition,
không phải model failure. Implementer chỉ chẩn đoán, đưa exact Windows commands
và xác minh sau khi User hoàn tất host changes; không tự thay đổi Windows.

Dependency policy:

- thử đúng `uv.lock` hiện hành trước;
- nếu host/WSL đã nhận GPU nhưng PyTorch project environment không dùng được
  CUDA do package/runtime mismatch, Implementer được điều chỉnh tối thiểu
  `pyproject.toml` và `uv.lock` trong approved Phase 3 scope;
- mọi thay đổi phải dùng `uv`, ghi exact versions và giữ dependency ngoài phần
  CUDA không đổi;
- không tạo environment phụ hoặc dùng `pip`.

CUDA/Qwen failure, OOM hoặc dependency incompatibility phải giữ nguyên observed
result và làm Phase 3 `blocked` cho tới khi được giải quyết. Không fallback sang
CPU, quantization, FlashAttention, batch auto-shrink hoặc revision khác.

## 7. Dense preflight và tokenizer coverage

Dense inference dùng một ordered sample cố định khoảng 10–15 chunks:

- mỗi P7 có ít nhất một chunk;
- phủ paragraph, list, table và condition-attached content;
- gồm các chunks dài sát tokenizer limits đã quan sát;
- sample identity, source, heading và thứ tự được ghi trong evidence.

Một tập query tiếng Việt nhỏ, cố định dùng để kiểm query preprocessing của cả
bốn models. Preflight xác minh load, input preparation, token count, output
shape/order/dimension, finite values và normalization. Nó không đánh giá chất
lượng retrieval.

Ngoài inference sample, Phase 3 tokenize toàn bộ 8.460 Representation A texts
bằng exact tokenizer/revision/preprocessing của cả bốn candidates với
`truncation=False`. Special tokens và prefix/instruction áp dụng cho đúng input
role phải được tính. Bất kỳ input nào vượt model contract đều fail closed và
quay lại Phase 2 chunking; không truncate, drop hoặc âm thầm giữ partial output.

## 8. Sparse state contract

Sparse state fit một lần trên ordered full-corpus Representation A texts và dùng
chung cho Phase 4 document vectors cùng Phase 5 query vectors.

Tokenization tái sử dụng trực tiếp `backend.scoring.bm25.tokenize`: lowercase
Unicode rồi lấy các token khớp `\w+`. Không tạo tokenizer thứ hai.

Constants và formula:

```text
k1 = 1.5
b = 0.75
N = số document có ít nhất một token
avgdl = trung bình token count của N documents

idf(term) = ln(1 + (N - df(term) + 0.5) / (df(term) + 0.5))

document_value(term) =
  idf(term) * tf(term) * (k1 + 1)
  / (tf(term) + k1 * (1 - b + b * dl / avgdl))
```

Vocabulary gồm mọi corpus term theo lexicographic order, index tuần tự từ 0.
Mỗi known query term xuất hiện tối đa một lần với value `1.0`; unknown terms bị
bỏ và không mutate vocabulary. Sparse dot product vì vậy bằng BM25 score hiện
hành cho cùng query/document.

Artifact cấp build lưu tối thiểu:

- schema version và corpus identity gắn với ordered Phase 2 chunks;
- document count, average document length, `k1` và `b`;
- tokenizer identity;
- ordered vocabulary và aligned IDF values.

Artifact phải byte-identical với cùng exact inputs/config và là nguồn duy nhất
cho sparse indexing/query. Phase 3 không lưu 8.460 sparse document vectors;
Phase 4 tạo chúng khi dựng points. Không lặp sparse/model/build metadata ở từng
point payload.

## 9. Evidence và Notebook 03

Versioned dense/GPU evidence là một JSON nhỏ, không chứa vector values. Nó ghi:

- corpus/sample identities;
- model IDs, revisions, dimensions, devices, dtypes và preprocessing;
- token counts và full-corpus over-limit counts;
- output counts/shapes cùng norm range;
- CUDA/Torch/device và VRAM observations cho Qwen;
- exact status/error cho phần failed, skipped hoặc blocked;
- sparse artifact identity và deterministic summary.

Generated sparse state được giữ ở build-state path do implementation plan khóa;
không nhét full vocabulary vào report Markdown.

`notebooks/03_embedding_models.ipynb` được cập nhật để:

- giải thích bốn dense input contracts và sparse flow bằng tiếng Việt;
- gọi public backend Phase 2/3 APIs, không copy algorithms;
- hiển thị bounded real sample và evidence summary;
- chứng minh Qwen dùng CUDA FP16 khi Phase đạt;
- không encode dense toàn corpus hoặc truy cập Qdrant;
- giữ repository outputs rỗng và `execution_count: null`.

Implementer chạy Run All trên temporary copy. Notebook failure là failure thật,
không được thay bằng output cũ hoặc hand-written expected values.

## 10. Acceptance và failure behavior

Phase 3 chỉ đạt technical readiness khi:

1. bốn exact pinned models được resolve và preprocessing contract được đối
   chiếu với model artifacts thực;
2. ba model nền chạy bounded CPU/FP32 preflight và Qwen chạy bounded CUDA/FP16
   preflight trên GTX 1650;
3. vector outputs đúng order/count/dimension, finite và normalized;
4. full-corpus tokenizer scan của cả bốn models có zero silent truncation và
   zero over-limit input;
5. sparse state đúng tokenizer/formula/vocabulary contract, round-trip được và
   repeated generation byte-identical;
6. JSON evidence không chứa vectors/secrets và phản ánh đúng mọi outcome;
7. temporary Notebook 03 Run All đi qua backend thật; canonical notebook sạch;
8. active Foods code/config/data/collections và Qdrant không bị thay đổi;
9. không có fallback, quantization, FlashAttention, provider framework hoặc
   artifact/vector duplication ngoài contract.

Thiếu host authority hoặc CUDA availability làm Phase `blocked`. Sai behavior,
thiếu required evidence hoặc silent fallback là implementation failure cần sửa.
Không dùng previous Foods benchmark result làm fresh Phase 3 PASS.

## 11. Quyền

Spec approval không tự cấp quyền implementation, model download, Windows/WSL
mutation, dependency change, notebook execution hoặc Git write. Các quyền đó
chỉ có hiệu lực theo exact Phase 3 implementation plan, Review Contract và
active handoff được User duyệt sau này.
