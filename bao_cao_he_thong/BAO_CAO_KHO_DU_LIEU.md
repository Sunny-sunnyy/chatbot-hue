# Báo cáo cho bạn: Kho dữ liệu — sửa dữ liệu và tạo lại chỉ mục (Phase 7A2 → sửa kho đợt 1, 2)

**Cập nhật lần cuối: 17:14 31/10/2026 — bản 7: rà lại cho đúng hiện trạng, xoá phần không còn đúng (User 31/10).** Các bản trước: xem `git log` file này.
Người viết: B (bản 4–6; bản 1–3: C), A (bản 7, qua sub-agent) · Review: A (bản 1–6); bản 7 chưa review. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** giữ kho tri thức Huế đúng và đảm bảo chỉ mục chatbot dùng luôn khớp kho.
- **Đang chạy cách nào (từ 30/10):** chatbot dùng chỉ mục `hue_full_corpus_7a2_e5_small_384` dựng lại trên kho đã sửa hai đợt — **204 file, 8.424 đoạn**
  (sau đợt 1: 8.426; trước đó 205 file / 8.459 đoạn). "Phiếu build" ghi dấu vân tay từng file; kho lệch thì chatbot từ chối khởi động. File "danh mục biên
  soạn" của nghệ thuật biểu diễn **không còn** trong chỉ mục (từ 28/10).
- **Đã sửa kho hai đợt — bạn đã đóng cả hai, giữ sao lưu** (đợt 1 ngày 28/10, đợt 2 ngày 30/10):
  - **Đợt 1:** **123 chỗ thay chữ / 65 file / 51 mục**, chỉ dựa vào căn cứ ngay trong kho — phần lớn là địa chỉ ghi tên phường mới, giữ tên cũ trong ngoặc
    (sau đợt sắp xếp đơn vị hành chính 01/07/2025), còn lại là vài con số mâu thuẫn giữa hai chỗ trong kho; bỏ file danh mục khỏi chỉ mục.
  - **Đợt 2:** **123 chỗ thay chữ / 40 file / 20 mục**, theo luật bạn đặt 29/10 (câu không chắc thì sửa theo nguồn đọc được — một session khác đọc lại khớp — hoặc
    làm yếu / bỏ chi tiết; không thêm khẳng định mới, không xóa câu cảnh báo an toàn): bỏ cấp "quận" và tên phường cũ; 1 mục viết lại theo nguồn, 2 mục sửa
    theo nguồn; **11 mục làm yếu** (bỏ con số / chi tiết không chắc; 2 dòng bị xóa hẳn); 8 mục **không sửa** (kho đã tự rào, hoặc không mâu thuẫn thật).
- **Đo "trước ↔ sau" mỗi đợt** (176 câu Golden; đợt 2 thêm 32 câu an toàn; chấm mù cùng lượt): **không làm hỏng** — 0 câu ngoài kho bị trả lời, 0 lỗi, 0 lỗi
  trích dẫn, 0 câu "nói chắc sai" mới; điểm đủ ý / đúng gần như y hệt; từ chối nhầm 12 → 13 (đợt 1), 13 → 12 (đợt 2). Bộ an toàn đợt 2: 0 câu nói sai điều kiện
  mới, 0 câu đảo cảnh báo. Nhãn "đoạn đúng" và Golden đã cập nhật theo kho mới, phần đổi bạn đã duyệt — riêng **1 câu Golden** còn
  keyword không khớp kho (phát hiện 31/10 khi chạy lại kiểm Golden; chờ bạn duyệt — `BAO_CAO_BO_CAU_HOI_GOLDEN.md`).
- **Giới hạn chính:** hai đợt làm kho **đúng hơn / thận trọng hơn** nhưng **không làm điểm tăng** — thước đo không nhạy với loại sửa này (tên phường, bỏ chi
  tiết không chắc). Vài mục vẫn chờ tra ngoài (kho đã tự rào). Kho còn thiếu vài thông tin hay được hỏi (ví dụ giờ mở cửa một điểm tham quan lớn). Mã đoạn dạng
  "tên file + số thứ tự" bị dồn số khi xóa một dòng giữa file (đợt 2 đã đo bù).
- **Chi phí:** đợt 1 ≈ 0,073 USD (trần 0,15); đợt 2 ≈ **0,047 USD** (≈ 1.200 đồng; trần 0,10). Chấm bằng Claude: 0 USD.
- **Bạn cần quyết gì:** không có việc gấp. Bản sao lưu hai đợt đang giữ theo bạn chọn; muốn xoá thì báo (§6).

## 2. Hoạt động thế nào (bản đang chạy)

```text
Markdown đã sửa → chia đoạn (không đổi so với Phase 2) → e5-small (chạy trên máy) + BM25
 → Qdrant (chỉ mục) → "phiếu build" ghi dấu vân tay từng file dữ liệu
khi chatbot khởi động: so dấu vân tay với dữ liệu hiện tại → khác thì từ chối chạy
```

"Phiếu build" (build record) là nguồn sự thật duy nhất cho câu hỏi "chỉ mục có khớp dữ liệu không".
Sửa một chữ trong kho mà chưa build lại thì chatbot không khởi động — để không trả lời bằng chỉ mục cũ.
Sửa dữ liệu về sau chỉ cần chạy lại lệnh build (xóa trước 3 đích: collection, phiếu build, từ điển từ khóa), không phải sửa code.

Code: `backend/ingestion/full_corpus_pipeline.py` (lệnh build `:263–279`, hàm build `:149`), `backend/ingestion/source_state.py` (phiếu build `:95`,
so dấu vân tay `:179`), `backend/retrieval/full_corpus.py` (kiểm khi khởi động `:383–385`, `:685`).

Tự kiểm (không bắt buộc): hỏi chatbot một câu về một thông tin đã sửa, hoặc mở `http://localhost:6335/dashboard` để xem các collection.

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Sửa mâu thuẫn có căn cứ trong kho (Phase 7A2) | **Đã xử lý, đóng gói** | 25 chỗ / 27 file; Golden sửa 1 đáp án; Golden 176 + smoke 10 đạt sau khi sửa |
| Rà toàn kho tìm mâu thuẫn / thông tin cũ (25/10) | **Đã xử lý** | 139 mục / 205 file (8 sub-agent + C tự kiểm 42 mục: 42 / 42 trích đúng); danh sách private |
| Sửa kho đợt 1 — phần có căn cứ trong kho | **Đã xử lý, đóng gói** (28/10; bạn đóng) | **123 chỗ / 65 file / 51 mục** (40 mục rà kho + 11 chỗ tên phường sót; 1 mục không áp vì file danh mục bị bỏ); áp bằng máy, chuỗi cũ khớp đúng 1 lần; C kiểm diff với bản sao lưu từng mục |
| Sửa kho đợt 2 — luật "không chắc ⇒ sửa theo nguồn / làm yếu" (bạn 29/10) | **Đã xử lý, đóng gói** (30/10; bạn đóng) | **123 chỗ / 40 file / 20 mục**; nguồn đọc nguyên văn, session khác đọc lại khớp; áp bằng máy, kho = bản sao lưu + chỗ sửa từng byte |
| Mục không đủ căn cứ trong kho (cần nguồn ngoài / người địa phương) | **Xử lý một phần** | Đợt 2 xử lý theo luật 29/10: có nguồn đọc được ⇒ sửa theo nguồn; không nguồn ⇒ làm yếu hoặc không sửa (8 mục kho đã rào / không mâu thuẫn thật); vài mục còn chờ tra ngoài |
| Loại file "danh mục biên soạn" nghệ thuật biểu diễn khỏi chỉ mục | **Đã xử lý, đóng gói** (28/10) | 33 đoạn; **205 → 204 file, 8.459 → 8.426 đoạn**; `exclude_files` (`backend/config/settings.yaml:18–21`) + test kiểm file bị loại |
| Đo "trước ↔ sau" đợt 1 (176 câu) | **Đã xử lý, đóng gói** (28/10; C kiểm đạt) | Không làm hỏng; đủ ý −0,008 / đúng 0,000 trên 129 câu chính (4 / 1 câu tụt, mức cho phép 5); từ chối nhầm 12 → 13; không thấy "tốt hơn" ở 31 câu chạm phần sửa |
| Đo "trước ↔ sau" đợt 2 (176 câu Golden + 32 câu an toàn) | **Đã xử lý, đóng gói** (30/10; bạn đóng) | Không làm hỏng; đủ ý +0,008 / đúng 0,000 trên 129 câu chính (4 tăng / 3 tụt đủ ý, 1 tụt đúng; mức cho phép 5); từ chối nhầm 13 → 12; bộ an toàn 0 câu sai điều kiện mới, 0 đảo cảnh báo; câu bị làm yếu: 0 câu mất điểm đủ ý. C đọc tay 8 câu: 0 lỗi nội dung kho; 1 câu thiếu một lời nhắc vì thứ hạng đoạn đổi (theo dõi) |
| Mã đoạn bền khi xóa dòng giữa file | **Chưa thực hiện** (phát hiện 30/10) | Mã "file#số" dồn số ở 2 file khi xóa 1 dòng ⇒ đợt 2 đo bù bằng luật "chạm theo file"; đợt sau: ghi trước, hoặc đổi mã theo nội dung (đổi chunker ⇒ cần thí nghiệm) |
| Nhãn "đoạn đúng" theo kho mới | **Đã xử lý, đóng gói** | Bản 5 đang dùng (30/10): 173 / 174 trích dẫn tìm lại nguyên văn (38 dời vị trí), 1 đổi chữ ⇒ bạn duyệt. Bản 4 (28/10): 172 / 174, 2 đổi chữ ⇒ bạn duyệt. Bản cũ giữ nguyên |
| Câu Golden lệch kho sau khi sửa | **Xử lý một phần** (31/10: kiểm Golden bắt thêm 1 câu lệch, chờ bạn duyệt) | Đợt 1: quét 59 câu ⇒ 0 câu cần sửa (bạn duyệt). Đợt 2: quét 39 câu (theo chữ + theo cụm bị bỏ + theo vị trí; 3 agent đọc, B kiểm, C quét độc lập) ⇒ **2 câu sửa đáp án mẫu** theo bạn chọn (bỏ tên phường cũ; thêm "khoảng" trước một con số), có sao lưu |
| Tìm trong kho mà không lọt bộ đánh giá / câu kín | **Đã xử lý, đóng gói** | `scripts/grep_kb.sh`: danh sách cờ trắng, chỉ quét trong kho, loại thư mục đánh giá / meta / bản thô / tên chứa sealed; B thử phá 4 vòng ⇒ đạt |
| Chỉ mục e5-small trên dữ liệu đã sửa | **Đã xử lý, đóng gói** (dựng lại 30/10) | **8.424 / 8.424** đoạn (dense + sparse), kiểm từng payload + vector mẫu; `/health` 5 / 5; kết quả tìm 158 câu: 133 giống hệt, 25 đổi danh sách 10 đoạn (11 chỉ đổi thứ tự; 24 có đoạn của file đã sửa). Đợt 1 (28/10): 8.426, 40 câu đổi |
| Phiếu build: dữ liệu lệch → từ chối khởi động | **Đã xử lý, đóng gói** | Phiếu `full_corpus_build:v3`, `complete`, 204 file / 8.424 đoạn (dựng 30/10); `source_state.py:95`, `:179`; `retrieval/full_corpus.py:383–385` |
| Một lệnh build cho mọi lần sửa dữ liệu | **Đã xử lý, đóng gói** | `full_corpus_pipeline.py:263–279` |
| Build lại sau khi sửa kho (từ điển BM25) | **Đã xử lý** (làm thật 28/10 và 30/10) | Xóa đủ ba đích (collection + phiếu build + từ điển) rồi build, ~4–5,5 phút; từ điển 5.660 → 5.631 từ (đợt 2 giữ 5.631). Lệnh xóa bị chặn ở terminal agent ⇒ bạn chạy bằng `!`. Từ điển ghi một lần, khác kho thì build dừng: `full_corpus_pipeline.py:137–146` |
| Chỉ mục Qwen3-Embedding-8B qua OpenRouter | **Đã thử, chưa áp dụng** | 7A2: lần 1 trộn 3 nhà cung cấp (vector không đồng nhất), lần 2 chỉ Nebius lỗi 504 ⇒ hoãn. 30/10: dựng được (chỉ Nebius, 0 lỗi, ~31 phút, 0,0089 USD) nhưng **kém hơn** ở tìm đoạn ⇒ giữ e5-small; collection thử đã xóa — `BAO_CAO_TIM_KIEM.md` |
| Dọn collection cũ trong Qdrant | **Đã xử lý, đóng gói** | 16 → 3 collection (7A2) → 1 (24/10, xóa 2 collection món ăn, không sao lưu theo danh sách dọn); còn `hue_full_corpus_7a2_e5_small_384` |
| Đoạn bị giữ nhỏ vì kiểm tokenizer model đã bỏ | **Đã thử, chưa áp dụng** | 6 bảng bị tách chỉ vì giới hạn HuyDang 256 (`settings.yaml:23–35`); 8.1 bỏ ràng buộc này: không đổi kết quả ⇒ chưa có lý do đổi — `BAO_CAO_CHIA_DOAN.md` |
| Notebook 03, 04 mô tả / gọi tên cũ | **Đã xử lý, đóng gói** | Đã sửa khi dọn (commit `1832201`); Run All 0 lỗi |
| Notebook 06 mô tả tên cũ | **Đã xử lý** | Chỉ sửa phần chữ; chưa chạy lại vì có gọi API trả phí |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 30/10/2026 — Sửa kho đợt 2 + dựng lại chỉ mục + đo "trước ↔ sau" (bạn đóng 14:39 30/10, giữ sao lưu)
- Soạn theo luật bạn đặt 29/10 (20 mục, 123 chỗ); C review 3 vòng, A duyệt; plan đo ghi tiêu chí trước. Bộ "trước" dùng lại bộ "sau" đợt 1 sau 4 kiểm "còn hiệu
  lực" ⇒ không tốn tiền chạy lại.
- Sao lưu 40 file + ảnh chụp Qdrant; áp bằng máy; build ~4 phút ⇒ 8.424 / 8.424; chatbot chạy lại đạt. Phát hiện mã đoạn dồn số ⇒ thêm luật "chạm theo file"
  **trước** khi thấy số "sau".
- Kết quả: **không làm hỏng** (số ở §3) · thời gian chờ trung vị 2,19 s, câu chậm 4,90 s · ≈ 0,047 USD. Hồ sơ:
  `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_implementation.md`.

### 28/10/2026 — Sửa kho đợt 1 + dựng lại chỉ mục + đo "trước ↔ sau" (bạn đóng 13:26 28/10, giữ sao lưu)
- Đo "trước" 176 câu trên chatbot đang chạy (10 đoạn ngữ cảnh), sao lưu 65 file + phiếu build + từ điển + ảnh chụp Qdrant; áp 123 chỗ; loại file danh mục; build
  ~5,5 phút ⇒ 8.426 / 8.426; chatbot chạy lại đạt.
- Kết quả: **PASS — không làm hỏng** (C kiểm từng bước) · câu chậm của lượt "sau" 9,8 s **không đại diện** (chậm phía mạng / nhà cung cấp; phần tìm trên máy không
  đổi) · ≈ 0,073 USD. Hồ sơ: `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_b9_implementation.md`.

### 27/10/2026 — Soạn và kiểm đợt sửa kho (chưa áp)
- 7 sub-agent đọc lại dòng gốc của 52 mục, chỉ dựa vào căn cứ trong kho; bản sửa dựng bằng máy (chuỗi cũ khớp đúng 1 lần). C review vòng 1 bắt 3 bản sửa phải
  sửa ⇒ vòng 2 đạt · 0 USD.
- Sự cố: một sub-agent đọc nhầm bộ câu đánh giá món ăn cũ (không phải câu kín) ⇒ C đối chiếu lại từng bản sửa của nhóm đó (giữ cả 9); từ đó sub-agent chỉ tìm
  trong kho bằng `scripts/grep_kb.sh`.

### 25/10/2026 — Rà toàn kho (C, chỉ đọc)
3.901 dòng có số / mốc thời gian ⇒ 8 sub-agent rà ⇒ **139 mục** (mâu thuẫn chắc 22, mâu thuẫn có thể 53, có thể cũ 37, khác 27); C tự kiểm 42 / 42 trích đúng ·
**PASS** · 0 USD. Đây là đầu vào của hai đợt sửa.

### 24/10/2026 — Đóng Phase 7A2; dọn code và collection món ăn
- Đóng 7A2: sửa 25 chỗ / 27 file; Golden 176 + smoke 10 đạt; chỉ mục 8.459 / 8.459; 5 câu thật 4 đạt / 1 chưa đạt — giống trước khi sửa (lỗi bảng giá cũ).
  Chỉ mục Qwen3-8B: **FAIL** (trộn nhà cung cấp, rồi lỗi 504) ⇒ bạn chọn hoãn.
- Dọn: xóa 2 collection món ăn + 5 file metadata cũ, gỡ code / test / notebook món ăn; kiểm lại: 1 collection, 205 file khớp phiếu build, kết quả tìm giống từng
  byte · **PASS**.

## 5. Hôm nay còn đúng không

Kiểm với code trên `main` (số dòng kiểm lúc 17:14 31/10/2026), phiếu build (`51fb1ec63cbc`: 204 file / 8.424 đoạn, `complete`) và `session_prompt/Project_Status.md` §4
(17:00 31/10/2026). Qdrant không chạy lúc kiểm ⇒ số điểm lấy từ phiếu build và `Project_Status.md` §4.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Chỉ mục `hue_full_corpus_7a2_e5_small_384` là chỉ mục chatbot dùng (8.424 đoạn từ 30/10) | **còn dùng** | `backend/ingestion/full_corpus_pipeline.py:66–69`; `backend/config/settings.yaml:41–42` |
| Phiếu build `full_corpus_build:v3` là nguồn sự thật; dữ liệu lệch thì từ chối chạy | **còn dùng** | `backend/ingestion/source_state.py:95`, `:179`; `backend/retrieval/full_corpus.py:383–385` |
| Một lệnh build `cd backend && uv run python -m ingestion.full_corpus_pipeline build --candidate <id>` (chạy từ `backend/`) | **còn dùng** | `backend/ingestion/full_corpus_pipeline.py:263–279` |
| Từ điển BM25 chung, ghi một lần; dữ liệu đổi thì phải xóa file cũ trước khi build | **còn dùng** (bẫy đã ghi ở `Project_Status.md` §8) | `full_corpus_pipeline.py:137–146` |
| Model vector: e5-small chạy; Qwen3-Embedding-8B còn trong code | **còn dùng** e5-small; 8B **đã thử 30/10 — kém hơn**, không có chỉ mục | `backend/embedding/full_corpus.py:41–66` |
| Chia đoạn giữ nguyên từ Phase 2 | **còn dùng** (8.1 thử 12 cách chia khác: không cách nào hơn) | `backend/ingestion/chunking/full_corpus_chunker.py`; `BAO_CAO_CHIA_DOAN.md` |
| Payload 7 trường (metadata v2) | **còn dùng** | `backend/retrieval/full_corpus.py:166` (`REQUIRED_PAYLOAD_FIELDS`) |
| Qdrant chỉ còn 1 collection | **còn đúng** | `Project_Status.md` §4 |
| 205 file / 8.459 đoạn trong chỉ mục | **đã thay** 28/10 bởi 204 / 8.426 (đợt 1), rồi 30/10 bởi **204 / 8.424** (đợt 2) | phiếu build `corpus.file_count` 204, `chunk_count` 8.424 |
| Sao lưu đợt 1 + đợt 2 | **còn giữ** (bạn chọn khi đóng mỗi đợt) | `Project_Status.md` §5 (28/10 13:26, 30/10 14:39) |

## 6. Việc còn lại / cần quyết

- Duyệt sửa **1 câu Golden lệch kho** (xem `BAO_CAO_BO_CAU_HOI_GOLDEN.md` §6). Sau mỗi đợt sửa kho sau này: chạy thêm `golden_full_corpus check`.

- **Sao lưu đợt 1 + đợt 2:** đang giữ theo bạn chọn (mỗi đợt: ảnh chụp Qdrant ~51 MB, bản gốc file kho, phiếu build + từ điển cũ); giữ thì quay lại được bất cứ
  lúc nào. Muốn xóa thì báo — không gấp.
- Vài mục còn "tra ngoài" (kho đã tự rào); kho thiếu giờ mở cửa của một điểm tham quan lớn (cần nguồn ngoài).
- Mã đoạn "file#số" không bền khi xóa dòng giữa file — lần sửa kho sau: ghi luật đo bù trước, hoặc đổi cách đặt mã (đổi chunker ⇒ cần thí nghiệm).
- Bộ chia đoạn vẫn kiểm cả 3 tokenizer (gồm HuyDang 256 đã bỏ) → đoạn bị giữ nhỏ; 8.1 bỏ ràng buộc này "không khác" ⇒ chưa có số ủng hộ đổi.
- Lỗi bảng giá và tổng hợp nhiều nguồn: xem `BAO_CAO_DANH_GIA.md`, `BAO_CAO_TIM_KIEM.md`.

## Phụ lục — hồ sơ kỹ thuật

- **Mã:** Kxxx = mục rà kho C32; giới hạn Phase 6: F1 = tổng hợp nhiều nguồn, F2 = lỗi bảng giá; B9 = việc dọn sau Phase 7 (B làm, C review). Trong report
  đo "trước ↔ sau" (`sua_kho_do_truoc_sau_plan.md` §4), F1–F4 là bốn sàn "không làm hỏng" — khác nghĩa F1 / F2 trên: F1 câu ngoài kho bị trả lời, F2 nói chắc
  sai mới, F3 lỗi kỹ thuật, F4 lỗi trích dẫn mới. T1 = mốc kết quả tìm 158 câu; luật chạm "f" = câu chạm theo file khi mã đoạn dồn số.
- **Bản 6 (B93 / B97, 30/10):** report `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_implementation.md` (plan `sua_kho_dot2_do_plan.md` bản 3 + §10, A duyệt
  `2adef0d4e5fc`; review C85 3 vòng, `sua_kho_dot2_b2_6_review.md`); bộ sửa `dot2.jsonl` `c0b5876ea510`; phiếu build `51fb1ec63cbc`, từ điển `c8134c49a648`, T1
  `4d5bbe9e0edc`; nhãn đoạn đúng bản 5 `33d16fd6b8f4` (`GOLD_PATH` trỏ v5 từ `bfb0b41`); Golden md5 `6331e88fb171` (trước `0f7dbf41b422`); dữ liệu private
  `data/sua_kho_2026-10-27/dot2/`, `data/loi_nang_2026-10-28/an_toan/{sau_dot2,moc_regen,dot2}_2026-10-30/`. Tổng hợp: `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md` §8.
- **Bản 5 (B85, 28/10):** report `report_agent/2026-10-27_phan_ton_phase_cu/` — `sua_kho_do_truoc_sau_plan.md` (A duyệt `41485782b39e`, review C72),
  `sua_kho_b1_6_implementation.md` (B81, review C75), `sua_kho_b7_8_implementation.md` (B82, review C76), `sua_kho_b9_implementation.md` (B83, review C80 ready);
  code `6b59788` (loại file danh mục, phiếu build `574b5d02088b`, T1 `23c58c47635d`), `e08a126` (nhãn đoạn đúng bản 4 `927bae1bf201`); dữ liệu private
  `data/sua_kho_2026-10-27/` (`applied_edits.jsonl`, `eval_truoc/`, `eval_sau/`, `judge/`, `backup/`).
- **Bản 4 (B77, 27/10):** spec `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` (bạn duyệt sha `937cf8969810`, 15:39 27/10; review C68 3 vòng);
  rà kho C32 `report_agent/2026-10-25_ra_soat_noi_dung_kho/`; soạn đợt sửa B73 / B74, review C66 / C67 (private `data/sua_kho_2026-10-27/`, mục lục `README.md`);
  yêu cầu ChatGPT B76; script `scripts/grep_kb.sh` (W27, commit cuối `77ac6ec`); sự cố S42 (`session_prompt/SO_CAI_TIEN_CACH_LAM.md`).
- **Qwen3-8B (30/10):** `report_agent/2026-10-27_phan_ton_phase_cu/qwen3_8b_implementation.md`, review `qwen3_8b_review.md`; code tag `hoso/b92-qwen3-harness`.
  Hoãn ở 7A2 theo review Gate 2 (`reports/phase_7a2_gate_2_review_2026_10_24.md` §6).
- [R1] giả thuyết Phase 8: `reports/phase_8_candidate_hypotheses_2026_10_24.md` (C1, C7). [R2] danh sách dọn sau Phase 7:
  `reports/phase_7_cleanup_inventory_2026_10_24.md` (C2).
- Bản 1 (C8, 24/10/2026, commit `4426ed0`). Bản 3 (C13): sau dọn B9 (commit `1832201`); số đo ở
  `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_review.md` §4.
- **Lệch phát hiện (24/10):**
  - `Project_Status.md` §4 ghi "mỗi chunk vừa cả 3 tokenizer e5-small / e5-base / huydang" — đúng với code (`backend/config/settings.yaml:23–35`), nhưng e5-base và
    HuyDang không còn là model ứng viên từ 7A2; ràng buộc này chỉ còn tác dụng làm đoạn nhỏ đi (6 bảng bị tách chỉ vì HuyDang). Đã báo ở C1.
  - **Đã xử lý:** notebook `04_qdrant_ingestion.ipynb` (bản commit `54670a0`) từng lặp qua cả 2 model và gọi trường không tồn tại (`prepared.sample_chunk_ids`).
    B9 đã sửa (chỉ kiểm candidate có phiếu build, lấy mẫu như `full_corpus_pipeline`); Run All 0 lỗi.
