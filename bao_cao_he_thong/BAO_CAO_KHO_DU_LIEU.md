# Báo cáo cho bạn: Kho dữ liệu — sửa dữ liệu và tạo lại chỉ mục (Phase 7A2 → đợt sửa kho 27/10)

**Cập nhật lần cuối: 16:45 27/10/2026 — bản 4: thêm lượt rà kho 25/10 (139 mục), đợt sửa kho đã soạn và kiểm 27/10 (chưa áp), tài liệu thiết kế
đợt sửa kho bạn đã duyệt, Qwen3-8B thành thí nghiệm sau đợt sửa, script tìm trong kho an toàn. Kho và chỉ mục đang chạy chưa đổi.**
Người viết: B (bản 4; bản 1–3: C) · Review: A. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** giữ kho tri thức Huế đúng và đảm bảo chỉ mục chatbot dùng luôn khớp kho.
- **Đang chạy cách nào (chưa đổi từ 24/10):** chatbot dùng chỉ mục `hue_full_corpus_7a2_e5_small_384` (205 file, 8.459 đoạn), dựng bằng một lệnh build;
  "phiếu build" ghi dấu vân tay từng file, kho lệch thì chatbot từ chối khởi động. Kho hiện tại = kho sau 25 chỗ sửa của Phase 7A2.
- **Mới (25–27/10):**
  - Một lượt rà toàn kho (25/10) tìm **139 chỗ** hai nơi trong kho ghi khác nhau hoặc thông tin có thể đã cũ — nhóm lớn nhất là địa chỉ còn dùng tên phường /
    quận cũ sau đợt sắp xếp đơn vị hành chính 01/07/2025.
  - Ngày 27/10 đã **soạn và kiểm xong** đợt sửa (chưa áp vào kho): 41 bản sửa có căn cứ ngay trong kho + 11 bản sửa tên phường cũ còn sót; 12 mục đọc lại
    thấy không đủ căn cứ nên chuyển nhóm; 16 câu hỏi cho bạn; 78 mục cần tra ngoài (đã soạn yêu cầu ChatGPT, chỉ gửi câu ngắn); đề xuất loại khỏi chỉ mục
    một file "danh mục biên soạn" không phải nội dung trả lời (33 đoạn).
  - **Bạn đã duyệt** tài liệu thiết kế đợt sửa kho (15:39 27/10): làm **sau khi đóng Phase 8.2**, thay chỉ mục tại chỗ có sao lưu, trần **0,15 USD**
    (≈ 3.750 đồng).
  - Qwen3-8B (model tìm thứ hai, chưa từng đo) chuyển thành **thí nghiệm sau đợt sửa kho**, không bỏ.
- **Giới hạn chính:** chưa sửa gì trong kho, chatbot vẫn có thể trả lời theo chỗ kho mâu thuẫn. 78 mục cần nguồn ngoài (đợt 2). Kho đúng tới mức nào chỉ
  biết sau khi đo lại 176 câu "trước ↔ sau".
- **Chi phí:** soạn đợt sửa 0 USD (đọc trên máy + Claude). Áp đợt sửa ước ≈ 0,074 USD (hai lượt 176 câu), trần 0,15 USD.
- **Bạn cần quyết gì:** trả lời 16 câu trong `data/sua_kho_2026-10-27/cau_hoi_user.md` (câu nào chưa trả lời thì để đợt 2); gửi yêu cầu ChatGPT 78 mục khi
  tiện (`gửi chatgpt/2026-10-27/tìm thông tin/tra_ngoai_kho_2026_10_27.md`).

## 2. Hoạt động thế nào (bản đang chạy)

```text
Markdown đã sửa → chia đoạn (không đổi so với Phase 2) → e5-small (chạy trên máy) + BM25
 → Qdrant (chỉ mục mới) → "phiếu build" ghi dấu vân tay từng file dữ liệu
khi chatbot khởi động: so dấu vân tay với dữ liệu hiện tại → khác thì từ chối chạy
```

"Phiếu build" (build record) là nguồn sự thật duy nhất cho câu hỏi "chỉ mục có khớp dữ liệu không".
Sửa một chữ trong kho mà chưa build lại thì chatbot không khởi động — để không trả lời bằng chỉ mục cũ.
Sửa dữ liệu về sau chỉ cần chạy lại lệnh build, không phải sửa code.

Code: `backend/ingestion/full_corpus_pipeline.py` (lệnh build), `backend/ingestion/source_state.py`
(phiếu build), `backend/retrieval/full_corpus.py` (kiểm khi khởi động).

Tự kiểm (không bắt buộc): hỏi chatbot một câu về thông tin vừa sửa (ví dụ diện tích đầm Cầu Hai), hoặc
mở `http://localhost:6335/dashboard` để xem các collection.

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Sửa mâu thuẫn có căn cứ trong kho (Phase 7A2) | **Đã xử lý, đóng gói** | 25 chỗ / 27 file; Golden sửa 1 đáp án; Golden 176 + smoke 10 đạt sau khi sửa |
| Rà toàn kho tìm mâu thuẫn / thông tin cũ (25/10) | **Đã xử lý** | 139 mục / 205 file (8 sub-agent + C tự kiểm 42 mục: 42 / 42 trích đúng); danh sách private |
| Sửa 139 mục — phần có căn cứ trong kho (đợt 1) | **Xử lý một phần** (đã soạn + review, **chưa áp**) | 41 bản sửa (C review: 40 giữ + 1 có điều kiện ⇒ không áp) + 11 bản tên phường sót (C review đạt); áp sau khi đóng 8.2 |
| Mục không đủ căn cứ trong kho | **Xử lý một phần** | 12 mục đọc lại ⇒ 9 sang tra ngoài (8 vì hai nguồn trong kho ngang nhau), 3 "không cần sửa" |
| Mục chỉ người địa phương biết | **Chưa thực hiện** (chờ bạn) | 16 câu hỏi lời thường, mỗi câu có gợi ý; câu chưa trả lời ⇒ đợt 2 |
| Mục cần tra nguồn ngoài | **Chưa thực hiện** (đợt 2) | 78 mục, 7 loại; yêu cầu ChatGPT đã soạn (chỉ câu ngắn), bạn tự gửi; kết quả phải đối chiếu link trước khi sửa |
| Loại file "danh mục biên soạn" nghệ thuật biểu diễn khỏi chỉ mục | **Xử lý một phần** (bạn duyệt, chưa áp) | 33 đoạn; 205 → 204 file, 8.459 → 8.426 đoạn; đo 8.1 bỏ 33 đoạn này: không khác; vào context ở 3 / 176 câu |
| Tìm trong kho mà không lọt bộ đánh giá / câu kín | **Đã xử lý, đóng gói** | `scripts/grep_kb.sh`: danh sách cờ trắng, chỉ quét trong kho, loại thư mục đánh giá / meta / bản thô / tên chứa sealed; B thử phá 4 vòng ⇒ đạt |
| Qwen3-8B | **Chưa thực hiện** (thí nghiệm sau đợt sửa kho) | bạn chọn "đo, không bỏ" (15:21 27/10); collection riêng, đo tầng tìm trước |
| Chỉ mục e5-small trên dữ liệu đã sửa | **Đã xử lý, đóng gói** | 8.459 / 8.459 đoạn (dense + sparse); HTTP 200; kiểm lại 24/10 |
| Phiếu build: dữ liệu lệch → từ chối khởi động | **Đã xử lý, đóng gói** | Phiếu `v3`, `complete`, 205 file (kiểm 24/10); `source_state.py:133`; `full_corpus.py:353,415` |
| Một lệnh build cho mọi lần sửa dữ liệu | **Đã xử lý, đóng gói** | `full_corpus_pipeline.py:232–244` |
| Build lại sau khi sửa kho (từ điển BM25) | **Xử lý một phần** | Từ điển ghi một lần: phải xóa file cũ trước khi build, không thì build báo lỗi; `full_corpus_pipeline.py:121–131` |
| Chỉ mục Qwen3-8B qua OpenRouter (7A2) | **Đã thử, chưa áp dụng** | Lần 1 trộn 3 nhà cung cấp (vector không đồng nhất); lần 2 chỉ Nebius lỗi 504; hoãn ⇒ 27/10: thí nghiệm sau đợt sửa kho (dòng trên) |
| Dọn collection cũ trong Qdrant | **Đã xử lý, đóng gói** | 16 → 3 collection (7A2) → 1 (24/10), đúng danh sách duyệt |
| Xóa 2 collection món ăn không dùng | **Đã xử lý, đóng gói** | Đã xóa 24/10 (liệt kê trước/sau); Qdrant chỉ còn `hue_full_corpus_7a2_e5_small_384`. Không có bản sao lưu (theo danh sách dọn) |
| Đoạn bị giữ nhỏ vì kiểm tokenizer model đã bỏ | **Chưa thực hiện** | 6 bảng bị tách chỉ vì HuyDang 256; Phase 8 xử lý |
| Notebook 03, 04 mô tả/gọi tên cũ | **Đã xử lý, đóng gói** | Đã sửa khi dọn (commit `1832201`); Run All 0 lỗi (kiểm lại ở review dọn) |
| Notebook 06 mô tả tên cũ | **Đã xử lý** | Chỉ sửa phần chữ; chưa chạy lại vì có gọi API trả phí |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 27/10/2026 — Soạn và kiểm đợt sửa kho (bản 4; chưa áp vào kho)
- **Cách làm:** 7 sub-agent đọc lại dòng gốc của 52 mục "sửa khi build" (B làm 1 mục), chỉ dựa vào căn cứ trong kho; mục không chắc thì chuyển nhóm, không
  đoán. Bản sửa dựng bằng máy: chuỗi cũ phải khớp đúng 1 lần, không hai mục chồng nhau. B tự kiểm mẫu (ví dụ cộng lại 12 giá vé lẻ = 1.200.000 đồng, số
  trong kho 1.050.000 là sai).
- **Review C:** vòng 1 tìm 3 bản sửa phải sửa (một câu đúng bị sửa thành sai hướng, hai câu làm mất thông tin) ⇒ B sửa ⇒ vòng 2 đạt; áp thử toàn bộ trong bộ nhớ
  0 lỗi. 11 bản tên phường sót (B tự làm, căn cứ duy nhất là ghi chú sắp xếp phường trong kho) — C review đạt.
- **Sự cố:** một sub-agent nhóm món ăn tìm cả thư mục nên đọc nhầm bộ câu đánh giá món ăn cũ (không phải câu kín). Các bản sửa của nhóm đó được đánh dấu
  riêng; C đối chiếu từng bản với căn cứ trong kho, giữ cả 9. Rút kinh nghiệm: sub-agent chỉ được tìm trong kho bằng `scripts/grep_kb.sh` (rào bằng máy,
  B thử phá 4 vòng tới khi kín).
- **Kết quả:** PASS (soạn + review) · kho, chỉ mục, chatbot **không đổi** · tiền: 0 USD.

### 25/10/2026 — Rà toàn kho (C, chỉ đọc)
Script gom mọi dòng có số / từ chỉ thời điểm (3.901 dòng) ⇒ 8 sub-agent rà theo nhóm, đối chiếu chéo giữa file ⇒ 162 mục thô ⇒ bỏ trùng ⇒ **139 mục**
(mâu thuẫn chắc 22, mâu thuẫn có thể 53, có thể cũ 37, khác 27). Đề xuất: tra ngoài 69, sửa khi build lại 53, bạn biết thì báo 16, đã biết 1. C tự kiểm 42
mục: 42 / 42 trích đúng file / dòng / giá trị · PASS · tiền: 0 USD. Kho **không sửa** ở Phase 8.2 (spec 8.2 để ngoài).

### 24/10/2026 — Dọn code và collection món ăn sau Phase 7 (bản 3)
Xóa 2 collection món ăn và 5 file dữ liệu metadata cũ; gỡ code/test/notebook món ăn. Kiểm lại sau dọn
(C, chỉ đọc): Qdrant còn 1 collection, 8.459 điểm, cả 8.459 điểm đúng 7 trường; 205 file khớp phiếu
build; chunker vẫn ra 8.459 đoạn; kết quả tìm kiếm giống hệt từng byte mốc 7B; chatbot `/health` 200 ·
**PASS** · tiền: 0 (lượt sinh thử 10 câu của B ~0,0013 USD).

### 24/10/2026 — Kiểm lại hiện trạng (C, chỉ đọc)
Kết quả: **PASS** — Qdrant 3 collection; chỉ mục 7A2 có 8.459 điểm (dense + sparse); phiếu build `v3`,
`complete`, 205 file · hiện trạng đúng như lúc đóng · tiền: 0.

### 24/10/2026 — Đóng Phase 7A2
Golden 176 + smoke 10 sau khi sửa kho: **PASS** · chỉ mục mới 8.459 / 8.459, không lỗi: **PASS** ·
chatbot khởi động HTTP 200 · 5 câu thật với `gpt-6-luna`: 4 đạt / 1 chưa đạt — giống hệt trước khi sửa
(câu chưa đạt là lỗi bảng giá cũ) · dọn Qdrant còn đúng 3 collection · code dựng chỉ mục cũ (kiểm thử
trước, migration metadata…) **đã bỏ**; backup kho **đã xóa** khi đóng.
Chỉ mục Qwen3-8B qua OpenRouter: lần 1 trộn 3 nhà cung cấp → vector không đồng nhất; lần 2 chỉ Nebius
→ lỗi 504 · **FAIL** (chưa có chỉ mục dùng được) · bạn chọn **hoãn** sang Phase 8.

## 5. Hôm nay còn đúng không

Kiểm với code (commit `1832201`, sau dọn), Qdrant (GET) và `session_prompt/Project_Status.md` §4 ngày 24/10/2026. Hai dòng cuối thêm 27/10/2026 (bản 4).

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Chỉ mục `hue_full_corpus_7a2_e5_small_384`, 8.459 đoạn, là chỉ mục chatbot dùng | **còn dùng** | `backend/ingestion/full_corpus_pipeline.py:66–69`; `backend/config/settings.yaml:41`; Qdrant GET |
| Phiếu build `full_corpus_build:v3` là nguồn sự thật; dữ liệu lệch thì từ chối chạy | **còn dùng** | `backend/ingestion/source_state.py:133`; `backend/retrieval/full_corpus.py:353,415` |
| Một lệnh build `cd backend && uv run python -m ingestion.full_corpus_pipeline build --candidate <id>` (từ 25/10, gói 1b: chạy từ `backend/`; lệnh cũ `python -m backend.ingestion…` từ gốc không còn chạy) | **còn dùng** | `backend/ingestion/full_corpus_pipeline.py:232–244` |
| Sparse state (từ điển BM25) chung, ghi một lần; dữ liệu đổi thì phải xóa file cũ trước khi build | **còn dùng** (bẫy đã ghi ở `Project_Status.md` §8) | `full_corpus_pipeline.py:121–131` |
| Hai model dense: e5-small (chạy máy) và Qwen3-Embedding-8B (OpenRouter, pin Nebius) | **còn trong code**; 8B **chưa có chỉ mục** → thí nghiệm sau đợt sửa kho | `backend/embedding/full_corpus.py:41–66` |
| Chia đoạn giữ nguyên từ Phase 2 | **còn dùng**, tới khi Phase 8 đổi (có số liệu ủng hộ đổi) | `backend/ingestion/chunking/full_corpus_chunker.py`; [R1] |
| Payload 7 trường (metadata v2) | **còn dùng** | `backend/retrieval/full_corpus.py` `REQUIRED_PAYLOAD_FIELDS` |
| 13 collection cũ (4 legacy, 4 metadata v2, 3 món ăn 08a, 2 TF-IDF 08b) | **đã xóa** | Qdrant GET 24/10 |
| Hai collection món ăn (572 điểm mỗi cái) | **đã xóa** 24/10 khi dọn sau Phase 7 (bạn duyệt) | [R2] §2.1; Qdrant GET sau dọn |
| Backup Gate 1 của kho | **đã xóa** khi đóng Phase | `Project_Status.md` §4 |
| 205 file / 8.459 đoạn trong chỉ mục | **còn dùng** tới đợt sửa kho (sau đó 204 / 8.426 nếu loại file danh mục) | build record `corpus.file_count`; Qdrant đếm 33 đoạn của file danh mục (27/10) |
| Hai model dense, 8B "Phase 8 xử lý" | **đã thay** bởi: 8B = thí nghiệm sau đợt sửa kho (bạn chọn 15:21 27/10) | spec đợt sửa kho §4 Q4 |

## 6. Việc còn lại / cần quyết

- **Đợt sửa kho (đã duyệt, chạy sau khi đóng Phase 8.2):** thứ tự các bước, ai làm / ai kiểm:
  0. đo bộ câu trả lời "trước" (176 câu, ≈ 0,037 USD) trên chatbot cuối 8.2, plan đo có review trước;
  1. sao lưu file kho sẽ sửa, snapshot Qdrant, bản sao phiếu build + từ điển BM25;
  2. áp bản sửa (B) ⇒ C kiểm diff với bản sao lưu; 3. loại file danh mục khỏi chỉ mục + sửa test; 4. chia đoạn thử (không vượt giới hạn token, test mẫu);
  5. build lại tại chỗ (xóa đủ collection + phiếu build + từ điển rồi build); 6. kiểm sau build (`/health`, 2 câu thật, kết quả tìm mới làm mốc mới).
  Bước 2–6 làm liền một lần (giữa chừng chatbot khởi động lại sẽ bị từ chối). Sau đó: 7. nhãn đoạn đúng bản 4 (tìm lại trích dẫn sau khi kho đổi; trích
  dẫn đổi thì bạn duyệt); 8. sửa câu Golden lệch kho (bạn duyệt từng câu); 9. đo "sau" (≈ 0,037 USD), chấm cùng lượt với "trước"; 10. báo cáo; 11. xóa bản
  sao lưu khi bạn duyệt; 12. plan thí nghiệm Qwen3-8B.
  **Khôi phục khi hỏng:** chép lại file kho từ bản sao lưu, hoàn lại cấu hình + file mẫu + bản nhãn, khôi phục snapshot Qdrant + phiếu build + từ điển, khởi
  động lại và kiểm. **Tiêu chí:** 0 câu ngoài kho bị trả lời, 0 lỗi mới; điểm "đủ ý" / "đúng" trung bình không tụt quá 0,1 và số câu tụt ≤ 5 (mỗi câu tụt
  có giải thích).
- **16 câu hỏi cho bạn** và **78 mục tra ngoài** (đợt 2) — như mục 1.
- Bộ chia đoạn vẫn kiểm cả 3 tokenizer (gồm HuyDang 256 đã bỏ) → đoạn bị giữ nhỏ; chưa có số ủng hộ đổi (8.1: bỏ ràng buộc này "không khác").
- Lỗi bảng giá và tổng hợp nhiều nguồn: xem `BAO_CAO_DANH_GIA.md`, `BAO_CAO_TIM_KIEM.md`.

## Phụ lục — hồ sơ kỹ thuật

- **Bản 4 (B77, 27/10):** spec `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (bạn duyệt sha `937cf8969810`, 15:39 27/10; review C68 3 vòng);
  rà kho C32 `report_agent/2026-10-25_ra_soat_noi_dung_kho/`; soạn đợt sửa B73 / B74, review C66 / C67 (private `data/sua_kho_2026-10-27/`, mục lục `README.md`);
  yêu cầu ChatGPT B76; script `scripts/grep_kb.sh` (W27, commit cuối `77ac6ec`); sự cố S42 (`session_prompt/SO_CAI_TIEN_CACH_LAM.md`). Mã: Kxxx = mục rà kho C32.
- Mã: lỗi bảng giá = **F2**; tổng hợp nhiều nguồn = **F1**; việc dọn sau Phase 7 = **B9** (B làm, C
  review); 8B hoãn theo review Gate 2 (`reports/phase_7a2_gate_2_review_2026_10_24.md` §6).
- [R1] giả thuyết Phase 8: `reports/phase_8_candidate_hypotheses_2026_10_24.md` (C1, C7).
- [R2] danh sách dọn sau Phase 7: `reports/phase_7_cleanup_inventory_2026_10_24.md` (C2).
- Bản 1 (C8, 24/10/2026, commit `4426ed0`). Bản 3 (C13): sau dọn B9 (commit `1832201`); số đo ở
  `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_review.md` §4.
- **Lệch phát hiện (24/10):**
  - `Project_Status.md` §4 ghi "mỗi chunk vừa cả 3 tokenizer e5-small / e5-base / huydang" — đúng với
    code (`backend/config/settings.yaml:22–34`), nhưng e5-base và HuyDang không còn là model ứng viên
    từ 7A2; ràng buộc này chỉ còn tác dụng làm đoạn nhỏ đi (6 bảng bị tách chỉ vì HuyDang). Đã báo ở C1.
  - **Đã xử lý:** notebook `04_qdrant_ingestion.ipynb` (bản commit `54670a0`) từng lặp qua cả 2 model và
    gọi trường không tồn tại (`prepared.sample_chunk_ids`). B9 đã sửa (chỉ kiểm candidate có phiếu
    build, lấy mẫu như `full_corpus_pipeline`); Run All 0 lỗi.
