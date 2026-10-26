# B42 — Phân loại lỗi tầng tìm (40 câu dev có đoạn đúng)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-23`) · Date: 2026-10-26 20:5x +0700 (`date` 20:53) · Việc: `CURRENT_HANDOFF.md` mục
"Việc giao phiên tối 26/10" — B42 · **0 USD** (chỉ đọc Qdrant `:6335`, e5-small CPU, không gọi model sinh) · Trạng thái: **chờ review**.

## 1. Tóm tắt

- Có 40 câu dev có đoạn đúng (101 fact). Mỗi câu được tính "đủ" khi **mọi** fact có ít nhất một đoạn đúng.
  - Context 5 (chatbot hiện chạy): **17 / 40** câu đủ.
  - Context 10 (mốc đợt cải tiến): **22 / 40** câu đủ.
- Context 10 sửa hết loại "đoạn đúng đã ở top-10 nhưng bị cắt khỏi context 5": 14 fact, 12 câu. Hai fact hàng bảng thuộc loại này và cũng
  được sửa.
- **18 câu vẫn thiếu ở context 10** (24 fact). Lỗi chia hai nửa gần bằng nhau:
  - **Đoạn đúng không vào pool 30 của dense** (`missed evidence`, 11 fact, 8 câu). 7 / 11 fact được **BM25 trên cả kho** xếp hạng ≤ 30,
    trong khi runtime chỉ cho BM25 xếp lại 30 đoạn của dense (B40). Có 2 fact dense không tìm thấy kể cả trong 300 đoạn.
  - **Đoạn đúng đã trong pool 30 nhưng RRF xếp ngoài top-10** (12 fact, 11 câu). Trong đó 5 fact dense đã xếp ≤ 10, nhưng gộp với BM25 đẩy
    chúng ra ngoài. 7 fact dense xếp 11–30 và RRF không kéo lên.
  - Còn 1 fact là **giới hạn của thước đo**: đoạn đúng là một dòng tiêu đề, và tiêu đề không nằm trong `evidence_parts`.
- **Một file chiếm chỗ** (`noisy evidence`): 6 / 18 câu còn thiếu ở context 10 vừa thiếu file đúng, vừa có một file khác chiếm ≥ 3 chỗ trong
  top-10. Ở context 5 là 9 câu.
- **Hàng bảng** (`wrong table association`): dev chỉ có 2 fact hàng bảng, cả hai đã vào context 10. Tầng tìm không có lỗi bảng nào để đo.
- **Câu tự nhiên** (12 / 40) **không được lợi** từ context 10: đủ 6 / 12 ở cả context 5 lẫn 10. Phần context 10 cứu được rơi vào câu
  `capability_only` (7 → 11 / 20) và câu `unnatural` (4 → 5 / 8).
- Suy ra (chưa đo): ở mốc context 10, phần còn thiếu chỉ sửa được ở tầng tìm, bằng đúng hai cách: mở rộng pool (BM25 cả kho) hoặc đổi cách
  xếp trong pool. Sửa tầng trả lời không cứu được những câu này. Điều này khớp nhận xét của C36 (`phan_loai_loi_C.md` dòng 12, 81–83).

## 2. Dữ liệu và cách đo

| Thành phần | Nguồn |
|---|---|
| Câu | `data/phase_8_1/gold/gold_draft.jsonl` (sha `bab707b9ab22`) ∩ dev của `split.json` (`e2b1788dfbbc`) = 40 câu, đều `is_answerable: full` |
| Tìm kiếm | chạy mới qua `build_retrieval` của evaluator (runtime `dense_bm25_rrf`, pool 30, top-10). **Kiểm chéo:** top-10 của G1 `data/phase_8_1/g1/runtime.jsonl` = T1 hiện tại 108 / 108 câu dev; tầng pool / top-10 / context 5 của B42 = cột `*_gold_all` của G1 **40 / 40** |
| Context | `FullCorpusContextBuilder` thật, `max_documents` 5 và 10 (mọi câu đóng đủ 5 / 10 đoạn) |
| Dense sâu | cùng vector câu hỏi, Qdrant `limit=300` (chỉ để chẩn đoán; hạng ≤ 30 trùng pool runtime 101 / 101 fact) |
| BM25 cả kho | Qdrant sparse trên cả collection, cùng mã hóa câu hỏi của runtime, `limit=300` |
| "Trúng" | `g1_retrieval.chunk_hits_quote` (cùng file, `evidence_parts` giao khoảng trích dẫn), như 8.1 G1 |
| Script | `data/cai_tien_tung_khau_2026-10-26/tools/b42_retrieval_errors.py` (`eb30d8978ed2`), `b42_summary.py` (`62d419c9ac67`) |
| Kết quả | `data/cai_tien_tung_khau_2026-10-26/b42_per_case.jsonl` (`79e4ba43b38e`), `b42_summary.json` (`e9b511cc3fd1`) — private |

**Nhãn**: dùng §6 mục 5 của báo cáo ChatGPT. Mỗi fact thiếu nhận **một** nguyên nhân:

| Nhãn §6.5 | Nguyên nhân (mã trong script) | Định nghĩa |
|---|---|---|
| `missed evidence` | ngoài pool, BM25 cả kho thấy (`out_pool_bm25`) | dense hạng > 30; BM25 trên cả kho hạng ≤ 30 |
| `missed evidence` | ngoài pool, cả hai xa (`out_pool_both`) | dense > 30 và BM25 cả kho > 30 |
| `missed evidence` | trong pool, BM25 kéo xuống (`pool_rank_bm25`) | trong pool; dense hạng ≤ 10 nhưng RRF xếp ngoài top-10 |
| `missed evidence` | trong pool, xếp thấp (`pool_rank_low`) | trong pool; dense 11–30; RRF không đưa vào top-10 |
| `missed evidence` | cắt bởi context (`ctx_cut`) | trong top-10 nhưng sau đoạn cuối của context (chỉ có ở context 5) |
| (thước đo) | `heading_quote` | trích dẫn đúng là dòng tiêu đề, không khớp đoạn nào |
| `noisy evidence` | cờ theo câu | thiếu ≥ 1 file đúng ở tầng đó, đồng thời một file khác chiếm ≥ 3 chỗ (định nghĩa B40) |
| `wrong table association` | cờ theo câu | fact thiếu là hàng bảng (trích dẫn bắt đầu bằng `|`) |

`incorrect citation ID`, `unsupported claim`, `under-answer`, `over-refusal`, `format` thuộc tầng trả lời — xem C36.

## 3. Kết quả (dev, 40 câu / 101 fact)

### 3.1 Theo tầng

| Tầng | Câu đủ mọi fact | Ghi chú |
|---|---|---|
| pool 30 (dense) | 31 / 40 | 9 câu: 8 câu có fact ngoài pool + câu 143 (thước đo) |
| top-10 = context 10 | **22 / 40** | thêm 9 câu mất ở bước xếp hạng |
| context 5 (runtime) | **17 / 40** | thêm 5 câu mất vì cắt từ 10 xuống 5 |

### 3.2 Nguyên nhân (số fact / số câu)

| Nguyên nhân | Context 5 | Context 10 |
|---|---|---|
| ngoài pool, BM25 cả kho thấy | 7 / 6 | 7 / 6 |
| ngoài pool, cả hai xa | 4 / 4 | 4 / 4 |
| trong pool, BM25 kéo xuống (dense ≤ 10) | 5 / 5 | 5 / 5 |
| trong pool, xếp thấp (dense 11–30) | 7 / 7 | 7 / 7 |
| cắt bởi context | 14 / 12 | 0 |
| thước đo (dòng tiêu đề) | 1 / 1 | 1 / 1 |
| **cờ** một file chiếm chỗ (câu) | 9 | 6 |
| **cờ** hàng bảng thiếu (câu) | 2 | 0 |

Một câu có thể mang nhiều nguyên nhân. Hạng của 11 fact ngoài pool:
- dense: 36, 36, 39, 48, 49, 51, 55, 68, 99, 163, và 2 fact > 300;
- BM25 cả kho: 2, 3, 4, 9, 15, 30, 30, 63, 67, 70, 114, và 1 fact > 300.

### 3.3 Theo loại câu và độ tự nhiên (câu đủ / tổng)

| Nhóm | Context 5 | Context 10 |
|---|---|---|
| `multi_source` | 6 / 18 | 9 / 18 |
| `comparative` | 6 / 13 | 8 / 13 |
| `conditional` | 5 / 8 | 5 / 8 |
| `direct_fact` | 0 / 1 | 0 / 1 |
| natural | 6 / 12 | 6 / 12 |
| capability_only | 7 / 20 | 11 / 20 |
| unnatural | 4 / 8 | 5 / 8 |

### 3.4 Từng câu còn thiếu ở context 5 (chỉ số câu, không nội dung)

| Câu | Loại | Tự nhiên | Context 5 | Context 10 |
|---|---|---|---|---|
| 17 | multi_source | unnatural | xếp thấp · file chiếm chỗ | xếp thấp · file chiếm chỗ |
| 19 | multi_source | capability | xếp thấp, ngoài pool (BM25 thấy) | như cũ · file chiếm chỗ |
| 22 | multi_source | natural | ngoài pool (BM25 thấy), cắt | ngoài pool (BM25 thấy) · file chiếm chỗ |
| 30 | comparative | capability | cắt · bảng | **đủ** |
| 38 | comparative | capability | BM25 kéo xuống, cắt ×2 | BM25 kéo xuống |
| 48 | multi_source | capability | xếp thấp · file chiếm chỗ | xếp thấp |
| 67 | multi_source | capability | xếp thấp · file chiếm chỗ | xếp thấp |
| 68 | multi_source | capability | cắt, ngoài pool (BM25 thấy) · file chiếm chỗ | ngoài pool (BM25 thấy) |
| 70 | comparative | capability | xếp thấp, cắt | xếp thấp |
| 85 | multi_source | unnatural | xếp thấp (top-10 cả 10 đoạn một file, file đúng) | xếp thấp |
| 89 | multi_source | capability | cắt | **đủ** |
| 92 | conditional | capability | ngoài pool, cả hai xa (top-10 cả 10 đoạn một file, file đúng) | như cũ |
| 97 | comparative | unnatural | ngoài pool ×3 (BM25 thấy 2 fact ở hạng 30) | như cũ |
| 113 | comparative | natural | ngoài pool cả hai xa, cắt · file chiếm chỗ | ngoài pool · file chiếm chỗ |
| 120 | direct_fact | natural | ngoài pool (1 fact BM25 hạng 4; 1 fact cả hai xa) · file chiếm chỗ | như cũ |
| 134 | multi_source | capability | cắt | **đủ** |
| 143 | conditional | natural | dòng tiêu đề (thước đo), cắt | dòng tiêu đề (thước đo) |
| 154 | multi_source | unnatural | cắt | **đủ** |
| 156 | comparative | natural | xếp thấp, BM25 kéo xuống, cắt · file chiếm chỗ | xếp thấp, BM25 kéo xuống |
| 159 | conditional | natural | BM25 kéo xuống | như cũ |
| 167 | multi_source | capability | BM25 kéo xuống · file chiếm chỗ | BM25 kéo xuống |
| 168 | multi_source | capability | ngoài pool (BM25 thấy), BM25 kéo xuống · file chiếm chỗ | như cũ · file chiếm chỗ |
| 172 | comparative | capability | cắt ×2 · bảng | **đủ** |

Đối chiếu C36: C ghi 48 / 67 / 159 / 167 là "có đủ đoạn đúng trong pool 30 nhưng không vào top-10" và 120 là "vắng cả pool". B42 khớp, và
chia thêm theo nguyên nhân:
- 159 và 167: BM25 kéo xuống (dense đã xếp ≤ 10);
- 48 và 67: dense chỉ xếp 11–30;
- 120: 1 fact BM25 cả kho xếp hạng 4, fact còn lại thì cả dense lẫn BM25 đều không thấy.

**Nhóm test** (15 câu, chỉ đếm): đủ 4 / 15 ở context 5 và 7 / 15 ở context 10. Fact thiếu ở context 10: xếp thấp 5, ngoài pool BM25 thấy 2,
ngoài pool cả hai xa 4. Không có fact nào bị "BM25 kéo xuống". Cờ file chiếm chỗ: 2 câu.

## 4. Quan sát · giả thuyết · giới hạn

**Quan sát (đo được):**
1. Ở mốc context 10, đóng góp lớn nhất là hai nhóm ngang nhau: đoạn đúng ở **ngoài pool 30** (11 fact) và **trong pool nhưng bị xếp sau**
   (12 fact).
2. 7 / 11 fact ngoài pool có hạng BM25 cả kho ≤ 30. 4 trong số đó ≤ 9.
3. Có 5 fact mà dense một mình đã đưa vào top-10, nhưng RRF với BM25 (BM25 chỉ chấm lại trong pool) đẩy ra ngoài.
4. Context 10 cứu đủ 5 câu (30, 89, 134, 154, 172), không câu nào là câu tự nhiên.

**Giả thuyết (chưa đo — NOT RUN):**
- H-a: nếu pool = dense 30 ∪ BM25 cả kho 30 (cách 8.1 gọi là `native`), 6 câu (19, 22, 68, 97, 120, 168) sẽ có thêm đoạn đúng trong pool.
  Đoạn đó có lên được top-10 hay không thì chưa biết. 8.1 G1.3 đã so `native p30` với runtime: top-10 đủ đoạn đúng +0,025, không khác,
  mất 2 câu (`report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_implementation.md` dòng 71). Vì vậy số này là tín hiệu giải thích vì sao,
  không phải đề xuất đổi.
- H-b: nhóm "BM25 kéo xuống" (5 fact) cho thấy cách gộp RRF hiện tại có lúc hại những câu dense đã làm đúng. Đổi trọng số gộp hay rerank
  (8.1: rerank luna MRR +0,17 là tín hiệu) có thể cứu nhóm này, nhưng cũng có thể làm hỏng câu khác. Cần đo theo cặp trên toàn dev.

**Giới hạn:**
- Chỉ có 40 câu dev có đoạn đúng, mỗi ô của bảng 3.3 chỉ có 1–20 câu. Bảng này dùng để định hướng, không đủ để kết luận.
- Đoạn đúng do agent gắn, User duyệt khoảng 10 câu (8.1). Fact ở câu 143 là dòng tiêu đề nên thước đo không bắt được. Câu này có thể thật ra
  đã đủ.
- "Đủ đoạn đúng" không có nghĩa câu trả lời đúng. Tầng trả lời xem ở C36.
- Dense `limit=300` chỉ để chẩn đoán. Hạng > 30 có thể lệch nhẹ so với một lượt hỏi `limit` khác (HNSW, `Project_Status.md` §8).

## 5. Bàn giao cho người kiểm

- Chạy lại (từ `backend/`, 0 USD): `PYTHONPATH=. HF_HUB_OFFLINE=1 uv run python ../data/cai_tien_tung_khau_2026-10-26/tools/b42_retrieval_errors.py`,
  rồi chạy `uv run python data/cai_tien_tung_khau_2026-10-26/tools/b42_summary.py` từ gốc repo.
- Kiểm rẻ nhất: tầng pool / top-10 / context 5 so với `data/phase_8_1/g1/runtime.jsonl` (`*_gold_all`), phải khớp 40 / 40.
- Report này không chép câu hỏi, đáp án hay nội dung kho; không mở câu kín; nhóm test chỉ đếm.
