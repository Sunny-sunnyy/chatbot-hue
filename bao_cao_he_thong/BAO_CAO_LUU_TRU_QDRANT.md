# Báo cáo cho bạn: Lưu đoạn vào Qdrant (Phase 4)

**Cập nhật lần cuối: 19:58 24/10/2026 — bản 2: đưa về mẫu mới; sau dọn 24/10: Qdrant còn đúng 1
collection (2 collection bản món ăn đã xóa), code nạp bản món ăn đã gỡ, notebook 04 sửa và chạy được.**
Người viết: B · Review: A. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** đưa các đoạn (kèm vector nghĩa và từ khóa) vào cơ sở dữ liệu vector Qdrant để
  chatbot tìm được, và giữ một "phiếu build" ghi index được tạo từ đúng bản corpus nào. Đã đóng (Phase 4,
  09/2026; build lại ở Phase 7A2).
- **Đang chạy cách nào:** Qdrant ở máy (`127.0.0.1:6335`) có **đúng 1 collection**
  `hue_full_corpus_7a2_e5_small_384`: 8.459 điểm, mỗi điểm có vector nghĩa (384 số) + từ khóa + 7 trường
  thông tin. Khi khởi động, chatbot so lại từng file corpus với phiếu build; lệch một file là từ chối chạy.
- **Đo được:** số điểm, thông tin và 5 vector mẫu khớp phiếu build (7A2, 24/10); sau dọn 24/10 collection
  vẫn 8.459 điểm, trạng thái bình thường, kết quả tìm kiếm giống từng byte.
- **Giới hạn chính:** model 8B chưa có collection; sửa corpus thì phải build lại mới chạy được.
- **Chi phí / tốc độ:** không tốn tiền (Qdrant chạy trên máy).
- **Bạn cần quyết gì:** không.

## 2. Hoạt động thế nào (bản đang chạy)

```text
205 file Markdown -> chia đoạn -> 8.459 đoạn
  -> vector nghĩa (e5-small, 384 số) + từ khóa (BM25)
  -> mỗi đoạn một điểm: ID suy từ ID đoạn, 7 trường thông tin
  -> ghi từng lô 64 điểm vào collection mới
  -> đếm lại điểm, so thông tin từng điểm, đọc lại 5 vector mẫu
  -> ghi phiếu build (hash từng file corpus, số file, số đoạn, model, danh sách từ khóa)
```

- Cùng ID đoạn luôn ra cùng ID điểm, nên không sinh bản sao.
- Build chỉ chạy khi collection đích chưa có và phiếu build chưa có. Lỗi ở bất kỳ bước nào thì dừng;
  không tự thử lại, không chạy tiếp từ giữa.
- Khi khởi động, chatbot kiểm hash corpus, cấu trúc collection và số điểm so với phiếu build.
- Code: `backend/ingestion/full_corpus_pipeline.py:134-229` (build), `backend/vectorstore/qdrant.py`,
  `backend/vectorstore/points.py`, `backend/vectorstore/upsert.py`, `backend/ingestion/source_state.py`.

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Nạp toàn kho bằng e5-small | **Đã xử lý, đóng gói** | 8.459 điểm, 5 vector mẫu khớp (7A2); chatbot đang dùng |
| Phiếu build ghi index khớp corpus nào | **Đã xử lý, đóng gói** | `source_state.py:133`, `:157-187` |
| Chatbot từ chối chạy khi corpus đổi mà chưa build lại | **Đã xử lý, đóng gói** | `retrieval/full_corpus.py:415-417`, `:736-738` |
| Kiểm cấu trúc collection và số điểm khi khởi động | **Đã xử lý, đóng gói** | `retrieval/full_corpus.py:763-773`; `vectorstore/qdrant.py:75-79` |
| Không ghi đè collection hay phiếu build đã có | **Đã xử lý, đóng gói** | `vectorstore/qdrant.py:91-108`; `source_state.py:200-210` |
| Collection cho model 8B | **Chưa thực hiện** | code có; build gặp 504, hoãn Phase 8 |
| Lọc theo trường thông tin (payload index) | **Chưa thực hiện** | chưa có nhu cầu; collection có index sẽ bị từ chối (`vectorstore/qdrant.py:77-79`) |
| Notebook 04 minh họa nạp/kiểm Qdrant | **Đã xử lý, đóng gói** | sửa ở B9; chạy hết không lỗi trên bản tạm (chỉ đọc Qdrant) |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 24/10/2026 — Xóa 2 collection bản món ăn, gỡ code nạp bản món ăn (bản 2)
Gỡ `ingestion/pipeline.py`, `vectorstore/reset.py` và các hàm chỉ bản món ăn dùng trong
`vectorstore/{qdrant,points,upsert}.py`; sửa notebook 04 chỉ kiểm model có phiếu build. Tiêu chí ghi
trước: kết quả tìm kiếm giống từng byte, test bản toàn kho đạt, API lên — đạt hết mới xóa · kết quả
**PASS**: 191 test đạt, giống từng byte, sức khỏe 200; sau đó xóa `hue_foods_e5_small_384` và
`hue_foods_e5_small_384_dense` (mỗi cái 572 điểm; bạn chạy lệnh xóa trong terminal B). Sau xóa Qdrant còn
đúng 1 collection, 8.459 điểm, sức khỏe vẫn 200 · tiền: 0 ở khâu này.

### 24/10/2026 — Kiểm lại hiện trạng (bản 1, chỉ đọc)
3 collection: 2 bản món ăn (mỗi cái 572 điểm; bản gốc có từ khóa, bản `_dense` không) + 1 toàn kho
(8.459 điểm, 384 chiều Cosine + từ khóa, không payload index). Phiếu build `full_corpus_build:v3`, 205
file, 8.459 đoạn, 5.660 từ khóa — khớp Qdrant.

### 24/10/2026 — Build lại và dọn (Phase 7A2 Gate 2–3)
Build e5 mới: 8.459 điểm, 8.459 thông tin khớp, 5 vector mẫu · **PASS** · Gate 3 xóa 13 collection cũ;
sức khỏe 200.

### 30/09/2026 — Thông tin điểm bản 2 (metadata v2)
4 collection v2 chép vector từ 4 collection cũ; 8 collection đều 8.460 điểm · **PASS** (nay đã xóa).

### 12–13/09/2026 — Bản toàn kho
4 collection `hue_full_corpus_a_*`, mỗi model một cái, mỗi cái 8.460 điểm · **PASS** (nay đã xóa).

### 25/08/2026 — Đơn giản hóa bản món ăn
Thêm `hue_foods_e5_small_384_dense` chỉ có vector nghĩa; bỏ tự thử lại khi ghi · **PASS** (nay đã xóa).

### 12/08/2026 — Bản món ăn
572/572 điểm, vector 384 Cosine, có từ khóa · **PASS** (nay đã xóa).

## 5. Hôm nay còn đúng không

Kiểm với code (commit `1832201`) và `GET /collections` ngày 24/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| 4 collection `hue_full_corpus_a_*` | **đã bỏ** (xóa ở 7A2 Gate 3) | `GET /collections` |
| Thông tin điểm 5 trường | **đã thay** bởi 7 trường (thêm `chunk_id`, `domain`) | `backend/core/schema.py:126-136`; `backend/vectorstore/points.py:52-54`, `:91-94` |
| Phiếu build v1, v2 | **đã thay** bởi `full_corpus_build:v3` (7A2) | `backend/ingestion/source_state.py:133`, `:157-187` |
| ID điểm suy từ ID đoạn | **còn dùng** | `backend/core/schema.py:49-51`; `backend/vectorstore/points.py:85` |
| Hash corpus so phiếu build | **còn dùng** | `source_state.py:217-234`; `retrieval/full_corpus.py:415-417`, `:736-738` |
| Kiểm số điểm và cấu trúc collection khi chạy | **còn dùng** | `retrieval/full_corpus.py:763-773` |
| Không payload index, không lọc | **còn dùng** | `backend/vectorstore/qdrant.py:77-79` |
| Lô 64 điểm mỗi lần ghi | **còn dùng** (hằng số khai ở 2 nơi) | `backend/vectorstore/points.py:24`; `backend/vectorstore/upsert.py:19`, `:28-29`; `full_corpus_pipeline.py:175-181` |
| Port Qdrant, timeout 30 | **còn dùng**, port đổi 6333 → 6335 | `backend/config/settings.yaml:37-38`; `full_corpus_pipeline.py:56`, `:99-102` |
| Không tự thử lại, không chạy tiếp từ giữa; đích phải chưa có | **còn dùng** | `full_corpus_pipeline.py:137`, `:157-158` |
| Danh sách từ khóa ghi một lần | **còn dùng** | `full_corpus_pipeline.py:122-131` |
| Đường build Phase 4 (preflight, hằng số corpus) | **đã thay** bởi một đường build thẳng (7A2) | `full_corpus_pipeline.py:134-229` |
| Nạp bản món ăn `ingestion/pipeline.py` | **đã bỏ** (gỡ ở B9) | file không còn |
| 2 collection bản món ăn | **đã bỏ** (xóa 24/10, B9) | `GET /collections` chỉ còn `hue_full_corpus_7a2_e5_small_384` |
| Tự thử lại khi ghi bản món ăn | **đã bỏ** (Phase 4–5); hàm ghi bản món ăn **đã gỡ ở B9** | `backend/vectorstore/upsert.py` chỉ còn hàm toàn kho |

## 6. Việc còn lại / cần quyết

- Collection cho model 8B — Phase 8.
- Sửa corpus thì chatbot từ chối chạy cho tới khi build lại; build lại phải xóa danh sách từ khóa cũ trước.
- Không cần bạn quyết gì ở khâu này.

## Phụ lục — hồ sơ kỹ thuật

- Report lịch sử: `reports/user_reports/phase_4_qdrant_ingestion_user_report.md`,
  `phase_4_5_qdrant_retrieval_simplicity_user_report.md`,
  `reports/full_corpus_phase_4_qdrant_ingestion_implementation_2026_09_12.md`,
  `full_corpus_metadata_v2_final_user_report_2026_09_30.md`,
  `reports/phase_7a2_gate_2_reindex_implementation_2026_10_24.md`,
  `reports/phase_7a2_gate_3_cleanup_implementation_2026_10_24.md`.
- Tên kỹ thuật: phiếu build = build record (`data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json`);
  thông tin điểm = payload; điểm = point.
- Bản 1: B8, 24/10/2026. Bản 2: B10, sau dọn B9 (commit `1832201`; report
  `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md` §4b).
- **Lệch đã ghi ở bản 1 và trạng thái hôm nay:**
  1. Notebook 04 ghi "8,460 chunks in four collections" — **đã sửa ở B9**.
  2. Notebook 04 sẽ lỗi (đọc phiếu build 8B không có; dùng field không tồn tại) — **đã sửa ở B9**, chạy
     hết không lỗi.
  3. Nạp bản món ăn vào collection mặc định sẽ bị từ chối (collection có từ khóa, hàm kiểm chỉ nhận vector
     nghĩa) — **hết hiệu lực**: code và collection bản món ăn đã gỡ ở B9.
  4. Spec 2026-09-12 (`:175-178`) đòi kiểm lại trạng thái collection đích ngay trước khi tạo; code chỉ
     kiểm lại hash corpus rồi tạo. Spec 7A2 đã thay đường build cũ; ghi phiếu build vẫn từ chối nếu đã có
     — **còn** (lịch sử, không gây lỗi).
