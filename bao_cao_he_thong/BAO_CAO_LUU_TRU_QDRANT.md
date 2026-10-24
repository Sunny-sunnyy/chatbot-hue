# Báo cáo dành cho người dùng: Giai đoạn 4 - Nạp dữ liệu vào Qdrant

```text
Trạng thái: Đã đóng (lịch sử) — viết lại 2026-10-24
```

## 1. Bạn nhận được gì

Phase 4 đưa các đoạn dữ liệu (chunk) vào Qdrant để chatbot tìm được. Có hai đợt.
Đợt Foods (tháng 8/2026) nạp 572 chunk ẩm thực vào `hue_foods_e5_small_384`.
Đợt full-corpus (tháng 9/2026) nạp 8.460 chunk của 5 domain vào 4 collection,
mỗi collection một model dense. Cuối tháng 9 có thêm bản metadata v2 (payload 7 field).

Hôm nay chỉ còn một index phục vụ chatbot: `hue_full_corpus_7a2_e5_small_384`,
8.459 point, dense + sparse, payload 7 field. Phase 7A2 (2026-10-24) build lại
bằng một đường build thẳng và xóa 13 collection cũ. Hai collection Foods vẫn còn
nhưng không đứng sau API nào.

## 2. Hệ thống hoạt động như thế nào

```text
205 file Markdown -> chunker -> 8.459 chunk
  -> vector dense (e5-small, 384 chiều) + vector sparse (BM25)
  -> point có ID UUID5 tính từ chunk_id, payload 7 field
  -> ghi từng nhóm 64 point vào collection mới
  -> đếm lại point, so payload, đọc lại 5 vector mẫu
  -> ghi build record
```

- Cùng `chunk_id` luôn ra cùng point ID, nên không sinh bản sao ngẫu nhiên.
- Build chỉ chạy khi collection đích chưa có và build record chưa có.
- Build record ghi hash từng file corpus, số file, số chunk, model, sparse state.
  Đây là nguồn sự thật duy nhất cho câu hỏi "index có khớp corpus không".
- Khi khởi động, runtime hash lại file corpus và so với build record. Lệch một
  file là từ chối khởi động. Nó cũng kiểm schema collection và số point.
- Lỗi ở bất kỳ bước nào thì dừng. Không retry, không resume.

## 3. Agent đã chạy và quan sát gì

**Theo report cũ** (không chạy lại):

| Nội dung | Kết quả quan sát | Nguồn |
|---|---|---|
| Foods, 12-08-2026 | 572/572 point, dense 384 cosine, có sparse | `reports/user_reports/phase_4_qdrant_ingestion_user_report.md:41-50` |
| Foods 4–5, 25-08-2026 | Tạo thêm `hue_foods_e5_small_384_dense` chỉ dense; bỏ retry thủ công | `phase_4_5_qdrant_retrieval_simplicity_user_report.md:12-19` |
| Full-corpus, 12/13-09-2026 | 4 collection `hue_full_corpus_a_*`, mỗi cái 8.460 point | `reports/full_corpus_phase_4_qdrant_ingestion_implementation_2026_09_12.md:84-144` |
| Metadata v2, 30-09-2026 | 4 collection v2 chép vector từ 4 legacy, 8 collection đều 8.460 point | `full_corpus_metadata_v2_final_user_report_2026_09_30.md:10-13, 29-31` |
| 7A2 Gate 2, 24-10-2026 | Build e5 mới: 8.459 point, 8.459 payload khớp, 5 vector mẫu | `reports/phase_7a2_gate_2_reindex_implementation_2026_10_24.md:137-140` |
| 7A2 Gate 3, 24-10-2026 | Xóa 13 collection; health 200 | `reports/phase_7a2_gate_3_cleanup_implementation_2026_10_24.md:51-75` |

**Đã kiểm hôm nay** (2026-10-24, chỉ GET Qdrant và đọc file):

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| Số collection | 3: `hue_foods_e5_small_384`, `hue_foods_e5_small_384_dense`, `hue_full_corpus_7a2_e5_small_384` | Đúng trạng thái sau Gate 3 |
| Index full-corpus | green, 8.459 point, dense 384 Cosine + sparse, `payload_schema` rỗng | Khớp build record, không có payload index |
| Hai collection Foods | green, mỗi cái 572 point; bản gốc có sparse, bản `_dense` không | Không đổi từ tháng 8 |
| Build record | `full_corpus_build:v3`, `complete`, 205 file, 8.459 chunk, `point_count` 8.459, vocabulary 5.660 | Số trong record khớp Qdrant |
| `data/full_corpus_builds/` | 2 file: build record e5 7a2 và `full_corpus_sparse_state.json` | Build record cũ đã xóa |

Không chạy build, test, health hay notebook. Không gọi API trả phí.

## 4. Hôm nay còn đúng không

| Kết quả/quyết định Phase 4 | Hôm nay | Bằng chứng |
|---|---|---|
| 4 collection legacy `hue_full_corpus_a_*` | *đã bỏ* — xóa ở Phase 7A2 Gate 3 | GET `/collections` (3 tên); grep `hue_full_corpus_a_` trong `backend/*.py` không ra kết quả |
| Payload full-corpus 5 field | *đã thay bởi* 7 field (`chunk_id`, `domain` thêm ở metadata v2, build thẳng ở 7A2) | spec 2026-09-12:144 vs `backend/core/schema.py:126-136`, `backend/vectorstore/points.py:145-149` |
| Build record schema (v1 rồi v2) | *đã thay bởi* `full_corpus_build:v3` (7A2) | `backend/ingestion/source_state.py:133, 157-187`; `retrieval/full_corpus.py:366-369` |
| Point ID UUID5 từ `chunk_id` | *còn dùng* | `backend/core/schema.py:49-51`; `points.py:138-139` |
| Freshness: hash file corpus so build record | *còn dùng*, nay trên `corpus.sources` của v3 | `source_state.py:217-234`; `retrieval/full_corpus.py:415-417, 736-738` |
| Runtime kiểm số point và schema collection | *còn dùng* | `retrieval/full_corpus.py:763-773` |
| Không payload index, không filter | *còn dùng* | `vectorstore/qdrant.py:127-130`; GET `payload_schema` = {}; grep `Filter(` trong `retrieval/full_corpus.py` không ra |
| Batch 64 point mỗi lần upsert | *còn dùng* (hằng số khai báo ở 2 nơi) | `points.py:77`, `upsert.py:94, 103-104`; `full_corpus_pipeline.py:175-181` |
| Qdrant port, timeout 30 pinned trong code | *còn dùng*, port đổi 6333 → 6335 | `full_corpus_pipeline.py:56, 99-102`; `settings.yaml:69, 73`; spec 2026-09-12:82 ghi 6333 |
| Không retry, không resume; đích phải chưa có | *còn dùng* | `full_corpus_pipeline.py:137, 157-158`; `upsert.py:105-107` |
| Sparse state ghi một lần, build sau phải giống hệt | *còn dùng* | `full_corpus_pipeline.py:122-131` |
| Đường build Phase 4 (preflight, hằng số corpus) | *đã thay bởi* một đường build thẳng (7A2) | spec 7A2:113-114, 149-154; `full_corpus_pipeline.py:134-229` |
| Foods ingestion `pipeline.py` | *còn trong code*, không đứng sau API | `backend/ingestion/pipeline.py:74-76`; `backend/api/app.py:61-62` gọi `build_full_corpus_retrieval_service` |
| 2 collection Foods | *còn*, chỉ code/test/notebook Foods cũ tham chiếu | `settings.yaml:70`; `tests/conftest.py:30`; `tests/test_full_corpus_qdrant_ingestion.py:398-400`; `notebooks/05_retrieval_profiles.ipynb:108`; `evaluation/sparse_benchmark.py:1012-1014` |
| Retry thủ công trong Foods upsert | *đã bỏ* (Phase 4–5) | `upsert.py:24-49` chỉ log rồi raise |

## 5. Giới hạn và bước tiếp theo

- Hai collection Foods và code Foods cũ chờ dọn sau Phase 7 (quyết định User
  2026-10-24, `Project_Status.md:106`).
- Candidate `qwen3-embedding-8b-4096` có trong code nhưng chưa có index; build
  lại thuộc Phase 8 (`Project_Status.md:74-77`).
- Sửa corpus thì runtime từ chối khởi động cho tới khi build lại. Build lại cần
  xóa sparse state cũ trước (`Project_Status.md:157-159`).
- Notebook 04 có lẽ không chạy được hôm nay (xem mục Lệch).

## Lệch phát hiện

1. `notebooks/04_qdrant_ingestion.ipynb:10` ghi "8,460 chunks in four isolated
   candidate collections". Thực tế còn 1 collection full-corpus, 8.459 point (GET).
2. Notebook 04 lặp qua `FULL_CORPUS_CANDIDATES` (`:72`) rồi đọc build record
   (`:74`). Candidate 8B không có record, nên theo code sẽ lỗi. Dòng `:89` dùng
   `prepared.sample_chunk_ids`, nhưng `PreparedFullCorpus` không có field này
   (`backend/ingestion/full_corpus_pipeline.py:77-82`). `Project_Status.md:166-167`
   chỉ ghi "notebook 04 chưa kiểm hành vi". Kết luận từ đọc code; chưa chạy notebook.
3. Report Foods `phase_4_qdrant_ingestion_user_report.md:24-25` và docstring
   `backend/vectorstore/upsert.py:29` nói chạy lại an toàn. Nhưng
   `hue_foods_e5_small_384` có sparse vector (GET), còn `ensure_collection` chỉ
   chấp nhận dense (`backend/vectorstore/qdrant.py:67`). Vậy chạy `pipeline.py`
   vào collection mặc định (`settings.yaml:70`) sẽ bị từ chối. Đây là thay đổi có
   chủ đích từ Phase 4–5 (`phase_4_5_qdrant_retrieval_simplicity_user_report.md:33-35`). Kết luận từ đọc
   code; chưa chạy.
4. Spec 2026-09-12:175-178 yêu cầu kiểm lại trạng thái collection đích ngay trước
   khi tạo. Code hôm nay chỉ kiểm lại hash corpus (`full_corpus_pipeline.py:168-170`)
   rồi tạo collection (`:172-174`). Spec 7A2:113-114 đã thay đường build cũ.
   Lần ghi build record vẫn từ chối nếu file đã có (`source_state.py:200-210`).
