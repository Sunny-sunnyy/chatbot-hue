# Báo cáo cho bạn: Lưu đoạn vào Qdrant (Phase 4)

**Cập nhật lần cuối: 16:18 14/11/2026 — bản 8: dựng lại sau lần ghi kho 3 (8.603 điểm, phiếu `82abd97169cd`).** Bản 7 (14:05 14/11): 8.522 điểm sau lần ghi kho 2. Bản 6 (10:30 14/11): 8.474 điểm; collection thử ảnh đã xoá (Qdrant còn 1 collection). Bản 5 (19:28 10/11/2026): sửa số cũ — Qdrant có 2 collection (thêm collection thử ảnh), lần build mới nhất là 05/11 tối, đã build lại 3 lần. Các bản trước: xem lịch sử git.**
Người viết: agent con của A (bản 31/10; bản trước: B) · Review: agent con ngữ cảnh mới. Bản 10/11: agent con của A, chưa review. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** đưa các đoạn (kèm vector nghĩa và từ khoá) vào cơ sở dữ liệu vector Qdrant để chatbot tìm được, và giữ một
  "phiếu build" ghi chỉ mục được tạo từ đúng bản corpus nào. Đã đóng (Phase 4, 09/2026); đường build hiện nay có từ Phase 7A2 (24/10).
- **Đang chạy cách nào:** Qdrant chạy trong **Docker Desktop** (Windows) ở `127.0.0.1:6335`, có **1 collection**: `hue_full_corpus_7a2_e5_small_384` — chỉ mục chatbot dùng,
  **8.603 điểm** (dựng lại 16:09 14/11 sau lần ghi kho 3 — 4 bài nơi mới + giờ Đại Nội; lần 2 8.522; lần 1 8.474; 05/11: 8.435), mỗi điểm có vector nghĩa (384 số) + từ khoá + 7
  trường thông tin. Collection thử ảnh `hue_anh_siglip2` (thử nghiệm đã bỏ) **đã xoá** — Qdrant hôm nay chỉ còn chỉ mục chatbot. Khi khởi động, chatbot so lại từng file corpus với phiếu build; lệch một file là từ chối chạy.
- **Đo được:** mỗi lần build, code tự kiểm số điểm, thông tin từng điểm và 5 vector mẫu (đoạn đầu mỗi chủ đề). Lần build mới nhất (14/11):
  216 file, 8.603 điểm, phiếu `82abd97169cd` (lần 2: `38b3ca3eb323`; lần 1: `efbf748c2195`); kiểm Qdrant thật 16:18 14/11/2026: 1 collection, 8.603 điểm.
- **Giới hạn chính:** sửa corpus thì phải build lại mới chạy được (đã làm 6 lần: 28/10, 30/10, 05/11, ba lần 14/11; mỗi lần vài phút trên máy). Tắt Docker Desktop
  thì chatbot không tìm được (gặp 31/10).
- **Chi phí / tốc độ:** không tốn tiền (Qdrant chạy trên máy).
- **Bạn cần quyết gì:** không có.

## 2. Hoạt động thế nào (bản đang chạy)

```text
216 file Markdown -> chia đoạn -> 8.603 đoạn
  -> vector nghĩa (e5-small, 384 số) + từ khoá (BM25)
  -> mỗi đoạn một điểm: ID suy từ ID đoạn, 7 trường thông tin
  -> ghi từng lô 64 điểm vào collection mới
  -> đếm lại điểm, so thông tin từng điểm, đọc lại 5 vector mẫu
  -> ghi phiếu build (hash từng file corpus, số file, số đoạn, model, dấu của danh sách từ khoá)
```

- Cùng ID đoạn luôn ra cùng ID điểm, nên không sinh bản sao.
- Build chỉ chạy khi collection đích chưa có và phiếu build chưa có (`full_corpus_pipeline.py:184-186`). Lỗi ở bất kỳ bước nào thì dừng; không tự thử lại, không
  chạy tiếp từ giữa. Build lại tại chỗ = theo đúng quy trình trong `guides/full_corpus_rag.md` mục "Build lại index khi corpus đổi" (sao
  lưu, gỡ collection + phiếu build + danh sách từ khoá cũ, rồi build); chatbot ngừng phục vụ từ lúc gỡ tới khi build xong.
- Khi khởi động, chatbot kiểm phiếu build, hash corpus, danh sách từ khoá, cấu trúc collection và số điểm.
- Code: `backend/ingestion/full_corpus_pipeline.py:149-262` (build), `backend/vectorstore/qdrant.py`, `backend/vectorstore/points.py`,
  `backend/vectorstore/upsert.py`, `backend/ingestion/source_state.py`; kiểm lúc khởi động `backend/retrieval/full_corpus.py:668-720`.
- Chạy Qdrant: `docker-compose.yml` (ảnh Qdrant ghim bản v1.18.3, cổng 6335 / 6336, dữ liệu ở `qdrant_storage/`, không commit).

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Nạp toàn kho bằng e5-small | **Đã xử lý, đóng gói** | 8.603 điểm (build 16:09 14/11, phiếu `82abd97169cd`); chatbot đang dùng |
| Phiếu build ghi chỉ mục khớp corpus nào | **Đã xử lý, đóng gói** | `source_state.py:95`, `:99-150` (tạo), `:159-176` (ghi, không ghi đè) |
| Chatbot từ chối chạy khi corpus đổi mà chưa build lại | **Đã xử lý, đóng gói** | `source_state.py:179-196`; `retrieval/full_corpus.py:383-385`, `:685` |
| Kiểm cấu trúc collection và số điểm khi khởi động | **Đã xử lý, đóng gói** | `retrieval/full_corpus.py:707-720`; `vectorstore/qdrant.py:75-80` |
| Không ghi đè collection hay phiếu build đã có | **Đã xử lý, đóng gói** | `vectorstore/qdrant.py:91-109`, `:135-140`; `full_corpus_pipeline.py:184-186`; `source_state.py:162-163` |
| Collection cho model lớn Qwen3-Embedding-8B | **Đã thử, chưa áp dụng** (30/10) | collection thử 8.424 điểm, build 0 lỗi; tìm kém hơn e5-small ⇒ không chọn, **đã xoá** (`04_BAO_CAO_EMBEDDING_TU_KHOA.md`) |
| Lọc theo trường thông tin (payload index) | **Chưa thực hiện** | chưa có nhu cầu; collection có index sẽ bị từ chối (`vectorstore/qdrant.py:77-80`) |
| Notebook 04 minh hoạ nạp / kiểm Qdrant | **Xử lý một phần** | chạy hết không lỗi (bản tạm, 24/10, chỉ đọc Qdrant); phần chữ đầu notebook còn ghi số đoạn cũ 8.459 (hiện 8.435) |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

- **14/11/2026 12:45–12:50 — Dựng lại sau lần ghi kho 2 (5 bài lưu trú):** 8.474 ⇒ **8.522 điểm** (+48), phiếu `38b3ca3eb323`, sparse `47f4b88b1309`, ~4 phút, cùng kịch bản tự lùi (`data/sua_kho_2026-11-14_ghi_kho_2/tools/chay.sh`); trước khi dựng, mọi server / lượt đo đã dừng.
- **14/11/2026 — Dựng lại sau lần ghi kho (3 bài mới + 4 chỗ sửa):** 8.435 ⇒ **8.474 điểm** (+39 đoạn), phiếu `efbf748c2195`, ~5 phút. Kịch bản của agent (gói bạn duyệt 13/11) tự kiểm máy rảnh ⇒ sao lưu ⇒ ghi kho ⇒ chia thử ⇒ xoá chỉ mục cũ + phiếu + danh sách từ khoá ⇒ dựng lại ⇒ đo tìm; lỗi thì tự lùi. Bản sao phiếu / từ điển cũ trong `data/sua_kho_2026-11-14_ghi_kho/backup/`; không chụp snapshot Qdrant (lùi = chép lại kho + dựng lại).
- **05/11/2026 tối — Build lại sau đợt giờ mở cửa (11 file Quần thể):** 8.424 ⇒ **8.435 điểm** (+11 đoạn), phiếu `9921888f2030`, ~4 phút; xoá collection do bạn chạy lệnh `!` (rào quyền chặn agent); bản sao phiếu / từ điển cũ trong `data/sua_kho_2026-11-05_gio/backup/`.
- **30/10/2026 — Build lại sau sửa kho đợt 2:** 8.426 ⇒ **8.424 điểm** (hai dòng kho bị xoá), phiếu `51fb1ec63cbc`; đo trước ↔ sau trên 176
  câu Golden + 32 câu an toàn: không làm hỏng · giữ (`02_BAO_CAO_KHO_DU_LIEU.md`).
- **30/10/2026 — Collection thử cho Qwen3-Embedding-8B:** 8.424 điểm, 0 lỗi; tìm kém hơn (3 / 40 câu thử mất đoạn đúng, luật cho 0), mỗi câu
  hỏi chậm thêm ~2,2 s; 0,0089 USD · bỏ, collection đã xoá (`04_BAO_CAO_EMBEDDING_TU_KHOA.md`).
- **28/10/2026 — Build lại sau sửa kho đợt 1:** 205 ⇒ 204 file (bỏ file danh mục nghệ thuật biểu diễn), 8.459 ⇒ 8.426 điểm, phiếu
  `574b5d02088b`; không làm hỏng · giữ tới 30/10 (`02_BAO_CAO_KHO_DU_LIEU.md`).
- **24/10/2026 — Xoá 2 collection bản món ăn, gỡ code nạp bản món ăn:** tiêu chí ghi trước (tìm giống từng byte, test đạt, API lên) ·
  **PASS**: 191 test, giống từng byte, sức khỏe 200; xoá `hue_foods_e5_small_384` và `hue_foods_e5_small_384_dense` (mỗi cái 572 điểm; bạn
  chạy lệnh xoá) ⇒ còn 1 collection · 0 USD.
- **24/10/2026 — Build lại và dọn (Phase 7A2):** build e5 mới 8.459 điểm (205 file), 5 vector mẫu khớp · **PASS**; xoá 13 collection cũ.
- **09/2026 (lịch sử, các collection đều đã xoá):** 12–13/09 bản toàn kho đầu tiên — 4 collection, mỗi model một cái, 8.460 điểm; 30/09
  thông tin điểm bản 2 (7 trường) chép sang 4 collection mới; 12/08 và 25/08 bản món ăn 572 điểm (có / không có từ khoá) · đều **PASS**.

## 5. Hôm nay còn đúng không

Số dòng code kiểm lúc 17:13 31/10/2026 (`main` `1985a81`, chưa kiểm lại); số điểm và danh sách collection kiểm lại bằng Qdrant thật 10:30 14/11/2026 (1 collection: 8.474 điểm).

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Thông tin điểm 7 trường (`search_text`, `source`, `title`, `heading_path`, `evidence_parts`, `chunk_id`, `domain`) | **còn dùng** (thay bản 5 trường cũ) | `backend/core/schema.py:126-135`; `backend/vectorstore/points.py:43-52` |
| Phiếu build `full_corpus_build:v3` | **còn dùng** (thay v1, v2) | `backend/ingestion/source_state.py:95` |
| ID điểm suy từ ID đoạn | **còn dùng** | `backend/core/schema.py:49-51`; `backend/vectorstore/points.py:78` |
| Hash corpus so phiếu build | **còn dùng** | `source_state.py:179-196`; `retrieval/full_corpus.py:383-385` |
| Kiểm số điểm và cấu trúc collection khi chạy | **còn dùng** | `retrieval/full_corpus.py:707-720` |
| Không payload index, không lọc | **còn dùng** | `backend/vectorstore/qdrant.py:77-80` |
| Lô 64 điểm mỗi lần ghi | **còn dùng**; hằng số khai một chỗ | `backend/vectorstore/points.py:15`; dùng lại ở `upsert.py:11`, `:23-24`, `full_corpus_pipeline.py:206-211` |
| Địa chỉ Qdrant, timeout 30 s | **còn dùng**, cổng đổi 6333 ⇒ 6335 (để chạy song song một dự án khác của bạn) | `backend/config/settings.yaml:38-39`; `full_corpus_pipeline.py:56`, `:99-102`; `docker-compose.yml` |
| Không tự thử lại, không chạy tiếp từ giữa; đích phải chưa có | **còn dùng** | `full_corpus_pipeline.py:184-186` |
| Danh sách từ khoá ghi một lần (đã có mà khác ⇒ dừng) | **còn dùng** | `full_corpus_pipeline.py:137-146`, gọi ở `:189` |
| Đường build Phase 4 (preflight, hằng số corpus) | **đã thay** bởi một đường build thẳng (7A2) | `full_corpus_pipeline.py:149-262` |

## 6. Việc còn lại / cần quyết

- Sửa corpus thì chatbot từ chối chạy cho tới khi build lại; build lại theo quy trình trong guide (gỡ collection, phiếu build, danh sách từ
  khoá cũ trước).
- Sửa phần chữ đầu notebook 04 cho đúng số đoạn hiện tại (nhỏ, chưa có lịch).

## Phụ lục — hồ sơ kỹ thuật

- Report lịch sử: `reports/user_reports/phase_4_qdrant_ingestion_user_report.md`,
  `phase_4_5_qdrant_retrieval_simplicity_user_report.md`,
  `reports/full_corpus_phase_4_qdrant_ingestion_implementation_2026_09_12.md`,
  `full_corpus_metadata_v2_final_user_report_2026_09_30.md`,
  `reports/phase_7a2_gate_2_reindex_implementation_2026_10_24.md`,
  `reports/phase_7a2_gate_3_cleanup_implementation_2026_10_24.md`.
- Tên kỹ thuật: phiếu build = build record (`data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json`); danh sách từ khoá = sparse
  state (`data/full_corpus_builds/full_corpus_sparse_state.json`, `47f4b88b1309` từ 12:50 14/11; `79aa34a6a68d` 10:24 14/11 — 05/11 `4a8311a2dfef`; 5.640 từ); thông tin điểm = payload; điểm = point.
- "Gate 2 / Gate 3" = hai bước build lại và dọn của Phase 7A2; "B9" = việc dọn code / collection bản món ăn (24/10, commit `1832201`).
- Bản 1: B8, 24/10/2026. Bản 2: B10, sau B9 (`report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md` §4b). Bản 3:
  31/10 (build lại hai lần, Qwen3-8B, Docker Desktop).
- **Tài liệu cũ lệch code (còn, lịch sử, không gây lỗi):** spec `docs/superpowers/specs/2026-09-12-phase-4-full-corpus-qdrant-ingestion-written-spec.md:175-178` đòi kiểm lại trạng thái collection đích ngay trước
  khi tạo; code kiểm đích một lần ở đầu build rồi tạo; ghi phiếu build vẫn từ chối nếu đã có. Các lệch khác ghi ở bản 1 (notebook 04 lỗi /
  ghi 4 collection, nạp bản món ăn bị từ chối) đã sửa hoặc hết hiệu lực ở B9.
