# Kế hoạch G4 — phần từ khóa (BM25): cách tách từ, khử dấu, k RRF, b (tiêu chí ghi trước)

Người viết: B (Claude Opus 5.5, terminal `hue-rag-3f`) · 2026-10-25 13:19 +0700 (`date`) · Việc: B18 · Trạng thái: **C review
ready (2 minor đã sửa); chờ A duyệt kèm sha; mới chạy cổng tương đương (A cho phép)** · 0 USD.

Căn cứ: spec `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` §5 G4 dòng "Từ khóa" (BM25 âm tiết +
cặp âm tiết + nguyên cụm mã; tách từ `pyvi`; đo với cách trộn thắng ở G1), §8; mục B18 trong `CURRENT_HANDOFF.md` (A 13:17);
C11 dòng 0.5, 3.7, 3.8, 5.3; G1 (`phase_8_1_g1_implementation.md` §4 G1.3, G1.4, §7); G4 (`phase_8_1_g4_implementation.md`
§4.4: lợi chủ yếu do pool rộng); skill `run-experiment`.

## 0. Lớp bài toán và cơ chế đang chạy (đã đọc code)

**Lớp bài toán:** nhánh từ khóa so khớp theo **âm tiết** (`scoring/bm25.py`: `\w+` + lowercase; k1 1,5, b 0,75). Tiếng Việt
ghép từ bằng nhiều âm tiết, nên "bún bò" khớp mọi đoạn có "bún" hoặc "bò"; mã / số ("QL1A", "70.000") bị cắt vụn; câu hỏi gõ
**không dấu** không khớp từ nào (G1.4: MRR 0,716 → 0,162; đoạn đúng đủ trong 5 đoạn 13/32 → **1/32**).

**Hai cách trộn (`retrieval/full_corpus.py`):**
- **runtime `dense_bm25_rrf`:** dense top-30 từ Qdrant → BM25 chấm **lại chính 30 đoạn đó** (`encode_sparse_document` + tích
  vô hướng, giữ điểm > 0, phá hòa theo point_id) → RRF k 60 → top-10. BM25 chỉ đổi **thứ tự** trong 30 đoạn dense; không đưa
  được đoạn mới vào.
- **native `native_hybrid_rrf` pool 100:** dense top-100 ∪ sparse top-100 (Qdrant sparse, vector tài liệu là trọng số BM25,
  câu hỏi trọng số 1,0 mỗi từ khác nhau, phá hòa theo point_id) → RRF k 60 → top-10. BM25 **tìm ứng viên mới**.
- Hai cách đều: top-10 → `FullCorpusContextBuilder` → 5 đoạn đưa model (id từ `packed.sources`, như G4).

**Hệ quả cho thiết kế:** nhánh dense không phụ thuộc biến thể BM25 ⇒ chạy dense **một lần** cho mỗi dạng câu hỏi (có dấu /
không dấu), lưu top-100; mọi biến thể BM25 tính **trong bộ nhớ** trên 8.459 `search_text` (payload Qdrant, đọc một lần).
**Không tạo collection Qdrant** (không cần `hue_81_g4k_*`). Không đổi `scoring/bm25.py`, `embedding/sparse.py`, retrieval
production; harness mới dựng lại công thức BM25 có tham số (tách từ, k1, b) và dùng `reciprocal_rank_fusion` production.

## 1. Chung

- **Vì sao đo cả hai cách trộn** (spec ghi "đo với cách trộn thắng ở G1"): G1.3 không có cách trộn nào thắng sau Holm, còn
  G4 (§4.4) cho thấy pool rộng (native 100) mang phần lớn mức tăng ⇒ đo trên cả runtime lẫn native pool 100, Holm nhân đôi
  (C review m2; A xác nhận 25/10).
- **Baseline (2 mốc, một cho mỗi cách trộn):** (R0) runtime; (N0) native pool 100 âm tiết. Bước 0 (§4) chạy lại BM25 trong
  bộ nhớ với tách từ âm tiết và **phải ra đúng** top-10 + 5 đoạn đưa model của G1 `runtime.jsonl` / `native_p100.jsonl`
  trên mọi câu dev; thêm so điểm BM25 trong bộ nhớ với `encode_sparse_document` production trên 200 cặp ngẫu nhiên (seed
  20261024, |chênh| ≤ 1e-9). Lệch top-10 / context: ghi từng câu, xác định do hòa điểm float (thứ tự cộng) hay lỗi công thức;
  lỗi công thức ⇒ dừng sửa harness; chỉ do hòa ⇒ dùng mốc trong bộ nhớ làm baseline cho mọi so sánh (cùng đường code) và ghi
  số câu lệch. Mốc byte runtime `cefb2d1a…` chạy lại trước (evaluator, không qua harness).
- **Tập câu:** dev số chính (bỏ `unnatural`, nhãn sha `0b65d1c138d2`): **32 câu có đoạn đúng** (chỉ số quyết), **88 câu trong
  kho** (keyword). CPU, không giới hạn 30 câu. Nhóm "không dấu" = chính các câu đó qua `transform_query(…, "noaccent")` của
  harness G1 (G1.4). Số phụ "chỉ natural". Xác nhận trên test: 15 câu có đoạn đúng (10 số chính; đã nhìn ở G1.6 — ghi giới
  hạn) + 41 câu trong kho cho keyword.
- **Đoạn đúng:** `gold_draft.jsonl` (`bab707b9…`), `gold_coverage` của harness G1.
- **Theo cặp:** `compare` của harness G1 (bootstrap 10.000, seed 20261024, CI 95%, thắng/hòa/thua), Holm theo nhóm ghi ở §3.
- **Tiền:** 0 USD (e5 local CPU, Qdrant chỉ đọc). Không GPU.

## 2. Chỉ số (ghi trước)

| Tên | Cách tính | Tập, n | Vai trò | Ngưỡng |
|---|---|---|---|---|
| `context5_gold_all` | đoạn đúng đủ mọi fact trong 5 đoạn đưa model (`packed.sources`) | 32 | **quyết** | CI 95% > 0 sau Holm |
| mất đoạn đúng | số câu baseline `context5_gold_all` = 1 mà biến thể = 0 | 32 | **sàn** | 0 câu |
| `top10_gold_all`, `context5_gold_frac` | như G1 / G4 | 32 | theo dõi | — |
| `pool_sparse_gold_all` (chỉ native) | đoạn đúng đủ trong sparse top-100 | 32 | theo dõi (tầng) | — |
| MRR@10, nDCG@10 keyword | `score_retrieval` | 88 | theo dõi | — |
| keyword coverage top-10 | `score_retrieval` (thang **%**, 0–100) | 88 | mức tụt cho phép | cận dưới CI của chênh ≥ −2,0 điểm % |
| kích thước từ vựng, token TB/đoạn, thời gian fit + chấm / câu | thống kê harness | — | theo dõi | — |

**Luật (skill §4):** tốt hơn = 0 câu mất + keyword coverage không tụt quá mức + `context5_gold_all` CI > 0 sau Holm. Kém hơn =
mất ≥ 1 câu, hoặc cận trên CI < 0. Còn lại = chưa rõ / không khác. Riêng nhánh khử dấu: luật đọc ở §3 E.

**Cỡ mẫu / trần (tính từ JSONL G1 trên 32 câu, ghi trước):**
- runtime: 13/32 câu đã đủ trong 5 đoạn; dense-30 chứa đủ đoạn đúng ở 24/32 ⇒ BM25 (chỉ xếp lại 30 đoạn) cứu được tối đa
  **11 câu**.
- native pool 100: 16/32 đã đủ; hợp hai nhánh @100 đủ 31/32 (sparse riêng 28/32, dense riêng 29/32) ⇒ tối đa **16 câu**.
- Cần ≥ 4–5 thắng / 0 thua cho CI > 0; Holm trên 6 cần nhiều hơn (~6). G1.3 đã thấy đổi cách trộn / k chỉ thắng 3/29/0 ⇒
  ghi trước: **kết quả có thể chỉ là "chưa rõ"**.
- Không dấu: runtime 1/32; câu nào có thể cứu tính ở bước 0 (dense-100 không dấu đủ đoạn đúng ở bao nhiêu câu). Với runtime,
  BM25 không dấu chỉ xếp lại dense-30 không dấu ⇒ trần thấp; native là nơi khử dấu có thể cứu nhiều.

## 3. Thí nghiệm

Tách từ áp cho **cả kho lẫn câu hỏi**; mỗi biến thể fit lại thống kê BM25 (df, idf, độ dài TB) trên 8.459 `search_text`
như `fit_sparse_state` (bỏ đoạn rỗng). Câu hỏi: mỗi từ khác nhau trọng số 1,0 (như production).

```yaml
- experiment_id: G4K.A_tokenizer      # một thay đổi: hàm tách từ
  baselines: {runtime: R0, native100: N0}
  variants:
    T1_syllable_bigram: >
      âm tiết (như production) + cặp âm tiết liền nhau "a_b"; cặp chỉ lấy trong cùng một đoạn chữ không bị ngắt bởi dấu câu
      (tách trước theo [.,;:!?()\[\]"“”\n]); cặp và âm tiết cùng một túi từ, cùng công thức BM25
    T2_syllable_codes: >
      âm tiết + "nguyên cụm mã": mỗi chuỗi không chứa khoảng trắng có ≥ 1 chữ số, bỏ dấu câu ở hai đầu, lowercase (ví dụ
      "ql1a", "70.000", "2024", "dt-15") thêm thành một từ riêng (âm tiết của nó vẫn giữ)
    T3_pyvi: >
      `pyvi.ViTokenizer.tokenize` (đã có trong pyproject, dùng ở ingestion/preview.py) → tách theo khoảng trắng → lowercase →
      bỏ mảnh không có ký tự chữ/số; từ ghép giữ dạng "bún_bò"; THAY âm tiết (không cộng thêm)
  measure_on: [runtime, native100]
  holm: 6 (3 tách từ × 2 cách trộn)
  report_also: kích thước từ vựng; % đoạn có ≥ 1 cặp / mã / từ ghép; thời gian tách + fit
- experiment_id: G4K.E_deaccent       # một thay đổi: khử dấu cả kho lẫn câu hỏi (tách từ âm tiết)
  transform: NFD → bỏ ký tự kết hợp → "đ"/"Đ" → "d"/"D" → lowercase (như `transform_query("noaccent")` của G1), áp cho
             search_text và câu hỏi trước khi tách âm tiết
  query_sets: [có dấu (bộ thường), không dấu (biến đổi từ cùng câu)]
  baselines: {runtime: R0, native100: N0} — chạy trên cùng dạng câu hỏi
  rule: >
    (1) câu có dấu: chỉ cần KHÔNG kém — 0 câu mất + keyword coverage không tụt quá −2,0 điểm % (khử dấu gộp các âm tiết khác
    dấu, có thể làm nhiễu); (2) câu không dấu: `context5_gold_all` CI > 0 sau Holm. Đủ cả (1) và (2) mới "tốt hơn".
  holm: 2 (2 cách trộn, trên câu không dấu; A giữ 2 dù runtime gần như chắc "chưa rõ")
  note_ceiling: >   # C review m1, ghi trước
    G1 `q_noaccent`: dense-30 runtime với câu không dấu chỉ chứa đủ đoạn đúng ở 3/32 câu (1/32 đã đủ trong 5 đoạn) ⇒ nhánh E
    trên runtime cứu tối đa 2 câu, không thể ra CI > 0 ⇒ gần như chắc "chưa rõ"; native pool 100 là câu hỏi chính của E
  note: nhánh dense (e5) vẫn nhận câu không dấu nguyên dạng — đó là tình huống thật; harness chỉ đổi BM25
- experiment_id: G4K.N_nfc_query       # chỉ xác nhận, nếu rẻ
  status: NOT RUN (có lý do) — G1.4 đã đo: câu hỏi NFD → MRR −0,200 [−0,269; −0,132]; NFD rồi NFC = giống hệt gốc. Không có gì
          mới để đo ở đây; chỉ ghi lại làm đề xuất 8.2 (thêm `unicodedata.normalize("NFC", …)` cho câu hỏi — 1 dòng, rẻ).
- experiment_id: G4K.P_params          # sau G4K.A / G4K.E
  base: >
    tách từ thắng ở A hoặc E (nếu có, trên cách trộn nó thắng); không có thì âm tiết. Nếu base là âm tiết + runtime thì bỏ phần k
    (G1.3 đã đo k = 2, 10, 30 trên đúng cấu hình đó: không biến thể nào qua Holm) và chỉ đo b.
  variants: [k10, k30, b0.5, b1.0]   # k60 / b0.75 là base; mỗi biến thể đổi đúng một tham số
  holm: 4 (hoặc 2 nếu bỏ k)
```

**Thứ tự + dừng:** A trước (3 tách từ × 2 cách trộn), rồi E, rồi P. Một biến thể vi phạm sàn thì không làm base cho P nhưng vẫn
ghi đủ số. Lỗi pyvi / harness: ghi lỗi quan sát được, không thử lại. Bước nào > 20 phút CPU thì dừng, báo A.

**Xác nhận trên test** chỉ cho biến thể "tốt hơn": 15 câu đoạn đúng (số chính 10: thắng > thua, 0 câu mất, cùng dấu) + keyword
41 câu; ghi giới hạn "đã nhìn ở G1.6".

**Không làm ở đây:** câu trả lời / judge (paid) — nếu có biến thể "tốt hơn", đề xuất đo câu trả lời ở G5/8.2 cùng context 10
(G2.1a); đổi production (`bm25.py`, `sparse.py`, index) — việc 8.2, User duyệt.

## 4. Thứ tự chạy (sau khi A ghi "duyệt bản sha …")

0. Mốc byte runtime `cefb2d1a…` (evaluator). Harness: đọc payload 8.459 đoạn (scroll chỉ đọc); chạy dense top-100 cho 108 câu
   dev trong kho × 2 dạng (có dấu / không dấu) **một lần**, lưu `data/phase_8_1/g4k/dense_<dạng>.jsonl`, gồm hai lần
   hỏi Qdrant: `limit=30` (runtime) và `limit=100` (native). Sửa theo dữ kiện ở bước 0 (13:25, A cho chạy trước cổng): 30 đầu
   của `limit=100` khác `limit=30` ở 1/108 câu (HNSW phụ thuộc `limit`) ⇒ runtime dùng đúng `limit=30`. Kiểm tương đương
   R0/N0 + 200 cặp điểm (§1). Tính trần không dấu.
1. G4K.A (6 lượt trong bộ nhớ) → 2. G4K.E (2 cách trộn × 2 dạng câu) → 3. G4K.P → 4. test cho biến thể "tốt hơn".
5. Report `phase_8_1_g4_keyword_implementation.md`: bảng do script in ra; thông số từng lượt (tách từ, k1, b, k RRF, pool,
   từ vựng, sha danh sách câu, thời gian, lệnh, đường dẫn kết quả); 3–5 dòng lời thường. Review: C.
   Ước thời gian: dense 216 câu ≈ 1 phút; mỗi biến thể fit + chấm ≈ 10–60 s (pyvi chậm nhất, chưa đo) ⇒ tổng < 30 phút CPU.

## 5. Code

| File | Việc |
|---|---|
| `backend/experiments/phase_8_1/g4_keyword.py` (mới) | các hàm tách từ (T0–T3, khử dấu); BM25 trong bộ nhớ có tham số (k1, b, tách từ) — công thức chép đúng `fit_sparse_state` / `encode_sparse_document` / `encode_sparse_query`; nhánh runtime (chấm lại dense-30) và native (sparse top-100 + `reciprocal_rank_fusion` production); context từ `FullCorpusContextBuilder` + `g4_rerank.packed_chunk_ids`; dùng lại `gold_coverage`, `compare`, `keep_realism`, `transform_query` của G1; **từ chối ghi đè** file kết quả trùng `--name` |
| — | Không sửa production. Không tạo / ghi collection. |

Khâu dính ghi cho G5 / 8.2 (không sửa ở đây): `tokenize` là hằng trong `scoring/bm25.py` và được `embedding/sparse.py`
import trực tiếp (không truyền được tách từ khác vào `fit_sparse_state` / encode) — muốn đưa tách từ mới vào runtime phải
thêm tham số + build lại sparse state và index.

## 6. Quyền, rủi ro, hợp đồng kiểm

- Quyền: Qdrant chỉ đọc (dense query + scroll); file private `data/phase_8_1/g4k/`; 0 USD; không commit; không mở câu kín.
- Rủi ro: (1) harness BM25 lệch production → kiểm tương đương ở bước 0 là cổng; (2) so nhiều biến thể trên 32 câu → Holm
  6 / 2 / 4; (3) khử dấu gộp từ khác nghĩa ("ma / má / mà") → sàn trên câu có dấu.
- Người kiểm (C) chạy lại: kiểm tương đương bước 0; `compare` từ JSONL; một biến thể bất kỳ chạy lại từ đầu phải ra cùng
  JSONL (tất định).
