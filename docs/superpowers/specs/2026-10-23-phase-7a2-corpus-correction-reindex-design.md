# Phase 7A2 — Sửa corpus + tạo lại index: Written Spec

**Date:** 2026-10-23 (+07)
**Status:** Approved by User 2026-10-23
**Owner:** Reviewer (Claude Opus 5.5)
**Design approved by User:** 2026-10-23 (brainstorming trong phiên Reviewer)
**Inputs:**
- `gửi chatgpt/kết quả nghiên cứu/TONG_HOP_REVIEWER_2026_10_23.md` (private;
  nguồn duy nhất cho giá trị chuẩn, căn cứ và file cần sửa)
- `reports/phase_7a2_openrouter_embedding_survey_2026_10_23.md` (survey thật,
  8 call)
**Implementation authorization:** chỉ qua `CURRENT_HANDOFF.md` sau khi plan được
User duyệt

## 1. Mục tiêu

Sửa các mâu thuẫn tri thức đã đủ căn cứ trong curated corpus, rồi build lại
index full-corpus trên corpus đã sửa với hai dense embedding:
`e5-small-384` (local) và `qwen3-embedding-8b` (OpenRouter). Runtime full-corpus
cutover sang index e5-small mới. Sau khi index mới được kiểm, xóa các collection
cũ không còn dùng.

Thứ tự: Phase 7A (Golden) → **Phase 7A2** → Phase 7B (Evaluator) → Phase 8.

## 2. Quyết định User ngày 2026-10-23

| Chủ đề | Quyết định |
|---|---|
| Phạm vi sửa corpus | 21 mục nhóm A + chỉnh câu chữ 4 mục nhóm B (K30, K33, K34, K48); không rà thêm ngoài các mục này |
| Dense embedding | Chỉ `e5-small-384` (local) và `qwen/qwen3-embedding-8b` (OpenRouter). Bỏ `e5-base-768`, `huydang-dek21-768`, `qwen3-embedding-0.6b-1024` |
| Cách build | Build thẳng ra schema metadata v2 vào collection tên mới; build record là nguồn sự thật duy nhất |
| Runtime mặc định | e5-small mới; cutover sang 8B chờ bằng chứng Phase 7B/8 |
| Provider OpenRouter | Không pin provider; mọi request gửi `data_collection: "deny"` |
| Golden | `check` trước/sau + tìm giá trị cũ trong 176 + smoke 10; sửa tối thiểu case bị ảnh hưởng |
| Nghiệm thu cutover | Live smoke Phase 6 (5 call `gpt-6-luna`) + retrieval smoke 10 trên cả hai index |
| Backup corpus | Copy file gốc vào backup private trước khi sửa; xóa khi Phase đóng |
| Xóa | 13 collection cũ + build record tương ứng, sau khi index mới được kiểm |

Data egress: User cho phép gửi toàn bộ chunk của corpus đã sửa tới OpenRouter
để build index 8B, và gửi query (Golden smoke, live smoke) để embed.

## 3. Cấu trúc Phase

Ba gate tuần tự. Mỗi gate có Implementer report, independent review và User
closure trước khi mở gate sau.

| Gate | Nội dung | Đổi code | Qdrant | Paid |
|---|---|---|---|---|
| 1 | Sửa corpus + Golden | Không | Không | Không |
| 2 | Build 2 index + cutover runtime | Có | Tạo 2 collection mới | OpenRouter + `gpt-6-luna` |
| 3 | Xóa collection/build record cũ | Không | Xóa 13 collection | Không |

Mọi thay đổi code nằm ở Gate 2, vì sau Gate 1 mọi collection cũ đã stale và
không còn đường nào dùng được chúng. Gate 3 chỉ xóa dữ liệu.

## 4. Gate 1 — Sửa corpus

### 4.1 Backup

Trước khi sửa, copy nguyên bản mọi file sẽ sửa vào
`knowledge-base-hue/meta/backup_7a2_2026_10_23/`, giữ nguyên đường dẫn tương đối
dưới `knowledge-base-hue/`. Backup là private và chỉ dùng để diff/khôi phục; nó
không thuộc corpus. Phase 2 discovery hiện chỉ quét năm domain, nên backup trong
`meta/` không vào index; Implementer xác nhận điều này bằng chunker thật.

### 4.2 Sửa nội dung

- Mỗi mục nhóm A sửa theo đúng "Giá trị chuẩn" và "File cần sửa" trong file
  tổng hợp. Mục ghi "rà" (K1: các file lăng có mã UNESCO) được rà trong đúng
  phạm vi giá trị của mục đó.
- Bốn mục nhóm B chỉ chỉnh câu chữ để nói rõ ngữ cảnh, không đổi sự kiện.
  Implementer xác định vị trí từ R1/R2 trong cùng thư mục với file tổng hợp.
- Body viết tự nhiên, answer-facing, tuân thủ quy tắc curated data trong
  `Session_Prompt.md`: không frontmatter, không field rỗng, không ghi chú biên
  tập trong body.
- Căn cứ được thêm vào `## Nguồn dữ liệu` của file bị sửa, gồm URL và ngày truy
  cập lấy từ file tổng hợp/R1/R2. K27 ghi rõ ở đó rằng văn bản gốc chưa được
  Reviewer tự mở để kiểm.
- Không sửa 28 mục nhóm C và không sửa nội dung nào khác.

### 4.3 Golden

1. Chạy `check` trên Golden 176 case và smoke 10 trước khi sửa (baseline).
2. Sau khi sửa, chạy lại `check`.
3. Tìm giá trị cũ của 25 mục trong `question`, `keywords`, `reference_answer`
   của 176 case và smoke 10.
4. Case bị ảnh hưởng: sửa tối thiểu `keywords`/`reference_answer` theo giá trị
   mới. Smoke vẫn phải deep-equal với case tương ứng trong file canonical.
5. Không có case bị ảnh hưởng thì Golden giữ nguyên.

### 4.4 Acceptance Gate 1

- Đủ 25 mục được sửa đúng giá trị/ngữ cảnh; diff giữa file sửa và backup chỉ
  chứa các thay đổi đó và dòng nguồn tương ứng.
- `check` PASS sau khi sửa.
- Danh sách case Golden bị ảnh hưởng (có thể rỗng) và từng sửa đổi được User và
  Reviewer đọc.
- Report tracked chỉ ghi mã mục, path, dòng và kết quả lệnh; không chép nội dung
  corpus hoặc Golden.

## 5. Gate 2 — Build 2 index và cutover runtime

### 5.1 Đường build

Một đường build duy nhất cho cả hai candidate, ghi thẳng ra collection mới:

- input: chunker hiện hành trên corpus đã sửa (không đổi chunker);
- payload: đúng 7 field metadata v2 (`search_text`, `source`, `title`,
  `heading_path`, `evidence_parts`, `chunk_id`, `domain`);
- vector: dense named vector + sparse vector trên cùng point, như metadata v2;
- sparse state: tính lại từ corpus đã sửa theo đúng thuật toán hiện hành.

Đường build này thay thế đường build Phase 4 (`build_candidate` gắn với
preflight 2026-09-12), không tồn tại song song.

### 5.2 Hai candidate

| Candidate | Collection | Dense |
|---|---|---|
| `e5-small-384` | `hue_full_corpus_7a2_e5_small_384` | local, spec và prefix hiện hành |
| `qwen3-embedding-8b-4096` | `hue_full_corpus_7a2_qwen3_8b_4096` | OpenRouter `qwen/qwen3-embedding-8b`, 4096 chiều |

Hợp đồng OpenRouter (từ survey):

- `POST /api/v1/embeddings`, input là mảng, batch cố định 64 chunk;
- document gửi nguyên `search_text`, không instruction; query có prefix
  `Instruct: {task}\nQuery: {query}` như Qwen hiện hành;
- không gửi `dimensions` (dùng 4096 gốc); `encoding_format: "float"`;
- không pin provider; mọi request gửi `provider.data_collection: "deny"`;
- kiểm mỗi response: đủ số vector, đúng thứ tự `index`, đúng 4096 chiều;
- lỗi bất kỳ (HTTP, thiếu vector, sai chiều) làm build dừng và ghi lỗi thật;
  không retry, không fallback, không resume.

Vector OpenRouter không bit-identical giữa các lần gọi (survey: cos ≥ 0,99985
giữa provider/batch), nên kiểm tra vector dùng cosine, không so bit.

### 5.3 Build record và freshness

Build record của từng collection là nguồn sự thật duy nhất cho "index khớp
corpus". Record ghi tối thiểu: tên collection, candidate/dense model (model id,
revision hoặc model OpenRouter, số chiều), hash từng source file, số file, số
chunk, identity/hash của sparse state, và với 8B là danh sách provider đã phục
vụ (đọc từ field `provider` của response).

Bỏ khỏi code: các hằng số `EXPECTED_FILE_COUNT`, `EXPECTED_CHUNK_COUNT`,
`EXPECTED_CORPUS_IDENTITY`, `EXPECTED_SPARSE_SHA256`, kiểm tra
`vocabulary_size == 5662` và phụ thuộc vào preflight artifact 2026-09-12. Runtime
giữ kiểm tra freshness: hash file corpus hiện tại phải khớp build record, nếu
không thì từ chối khởi động như hiện nay. Sửa corpus về sau chỉ cần build lại,
không phải sửa code.

### 5.4 Runtime

- Danh sách candidate full-corpus trong code chỉ còn hai candidate trên. Xóa
  cùng lúc code chỉ phục vụ collection cũ: module copy
  `backend/ingestion/full_corpus_metadata_v2.py`, dense spec của ba model bị bỏ,
  mapping tên collection cũ và test đi kèm. Kết quả lịch sử trong `reports/` và
  `evaluation/results/` giữ nguyên.
- API full-corpus mặc định dùng `hue_full_corpus_7a2_e5_small_384`; profile
  retrieval, reranker, context và generation giữ nguyên Phase 6.
- Đường query 8B dùng được cho retrieval smoke và Phase 7B, không phải mặc định.
  Không thêm cấu hình chọn model.

### 5.5 Acceptance Gate 2 (chạy thật)

1. Mỗi collection: số point bằng số chunk của corpus đã sửa; mọi payload đúng 7
   field; dense đúng 384/4096 chiều; có sparse vector.
2. Embed lại thật một mẫu chunk rải đủ 5 domain: cosine với vector đã lưu
   ≥ 0,999.
3. Health khởi động runtime PASS trên index e5-small mới, gồm kiểm tra freshness.
4. Live smoke Phase 6 (`backend/llm/phase6_live_smoke.py`, đúng 5 call
   `gpt-6-luna`) chạy trên index e5-small mới: không tệ hơn kết quả Phase 6
   (4 PASS / 1 FAIL, FAIL đã biết là `conditional_evidence`). Case regression
   phải được báo kèm root cause; không chạy lại ngoài 5 call.
5. Retrieval smoke 10: chạy Golden smoke 10 qua retrieval thật trên cả hai index
   (không gọi LLM), K=10, ghi top-10 source và keyword nào xuất hiện. Kết quả
   chỉ ghi nhận, không có ngưỡng, vì dự án chưa đặt ngưỡng metric trước baseline
   Phase 7B.
6. Test bị ảnh hưởng được cập nhật; test chỉ bảo vệ hằng số/preflight/module đã
   bỏ được xóa. Không còn import/tham chiếu tới module/spec đã xóa trong
   `backend/`. Không mock/fake/stub.

### 5.6 Quyền paid và data trong Gate 2

- OpenRouter `qwen/qwen3-embedding-8b`: build toàn bộ chunk (ước ~133 batch,
  ~780k token, ~$0,01) tối đa 2 lần build đầy đủ; tối đa 50 call embed query cho
  kiểm tra mẫu và retrieval smoke.
- Build lỗi: Implementer được xóa collection 7a2 đang build dở của chính lần đó
  rồi build lại, trong giới hạn 2 lần.
- `gpt-6-luna`: đúng một lần chạy live smoke 5 call.

## 6. Gate 3 — Dọn dẹp

### 6.1 Xóa collection

Chỉ xóa đúng 13 collection sau (Qdrant `127.0.0.1:6335`):

```text
hue_full_corpus_a_e5_small_384
hue_full_corpus_a_e5_small_384_metadata_v2
hue_full_corpus_a_e5_base_768
hue_full_corpus_a_e5_base_768_metadata_v2
hue_full_corpus_a_huydang_dek21_768
hue_full_corpus_a_huydang_dek21_768_metadata_v2
hue_full_corpus_a_qwen3_06b_1024
hue_full_corpus_a_qwen3_06b_1024_metadata_v2
hue_foods_08a_e5_small_384
hue_foods_08a_e5_base_768
hue_foods_08a_huydang_dek21_768
hue_rag_phase8_08b_tfidf_v1_unicode_word_49c5d03359f9
hue_rag_phase8_08b_tfidf_v1_unicode_word_5297c8604335
```

Giữ nguyên `hue_foods_e5_small_384`, `hue_foods_e5_small_384_dense` và hai
collection 7a2 mới.

### 6.2 Xóa file

- Build record của 8 collection full-corpus cũ trong `data/full_corpus_builds/`
  và `phase_3_sparse_state.json` cũ (đã được thay ở Gate 2).
- Backup Gate 1 được xóa khi User đóng Phase.

### 6.3 Acceptance Gate 3

- Qdrant chỉ còn đúng bốn collection ở §6.1; point count của bốn collection này
  không đổi so với trước khi xóa.
- `data/full_corpus_builds/` chỉ còn build record và sparse state của hai
  collection 7a2.
- Health runtime vẫn PASS.

## 7. Tài liệu khi đóng Phase

Reviewer cập nhật `Project_Status.md`, guide full-corpus liên quan và ghi chú
cho Phase 8: candidate set đã đổi thành e5-small + qwen3-8b, nên spec/plan
Phase 8 phải thiết kế lại trước khi chạy.

## 8. Ngoài phạm vi

- Đổi chunker, payload schema, retrieval profile, reranker hoặc generation.
- 28 mục nhóm C; mọi nghiên cứu thêm ngoài file tổng hợp.
- Cutover runtime sang 8B; cấu hình chọn model.
- Full evaluation 176 case (Phase 7B).
- Foods production collection và Foods Golden V2/V3.
- Pin provider, retry, resume, checkpoint, cost accounting.

## 9. Rủi ro

| Rủi ro | Cách xử lý |
|---|---|
| Corpus không có Git | Backup Gate 1 + diff thật trước closure |
| Gửi corpus private ra ngoài | `data_collection: "deny"`; User đã chấp nhận; survey không kiểm được provider tuân thủ |
| OpenRouter lỗi/429 giữa build | Dừng, build lại trong giới hạn 2 lần; vượt giới hạn thì báo User |
| Runtime phụ thuộc mạng | Không áp dụng cho runtime mặc định (e5-small local) |
| Xóa không hoàn tác được | Chỉ ở Gate 3, sau closure Gate 2, đúng danh sách tên |
| LLM không tất định ở live smoke | So với baseline 4/5; regression phải có root cause |
