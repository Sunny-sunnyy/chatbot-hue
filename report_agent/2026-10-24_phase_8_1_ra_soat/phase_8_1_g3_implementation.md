# Implementation Report: Phase 8.1 G3 — biến thể chia đoạn

Người làm: C (Claude Opus 5.5, terminal `hue-rag-a1`) · 2026-10-25 (giờ theo `date`) · Việc: C29 · Kế hoạch duyệt:
`phase_8_1_g3_plan.md` sha **`9f00c460c3e9`** (bản `e089243fb612` + §9 phụ lục; A duyệt lại sau review của B) · Spec 8.1
§5 G3 · skill `run-experiment`, `practical-project-coding`. Report không chép corpus, câu hỏi, đáp án hay đoạn trích.

**Trạng thái: xong (13:56), chờ B review.**
- Mọi bước §3 + §10 (B10) đã chạy.
- **Không biến thể nào "tốt hơn"** ⇒ §4 (2×2 + câu trả lời paid) **NOT RUN**, xác nhận test **NOT RUN** (plan: chỉ cho
  phương án tốt hơn).
- Tiền: **0 USD**. Runtime cuối G3 vẫn giống byte `cefb2d1a…`. Qdrant chỉ còn collection runtime.

## 1. Thay đổi code

- `backend/ingestion/full_corpus_pipeline.py`: `prepare_full_corpus_input(..., chunks=None)` và `build_candidate(...,
  chunks=None)`. Khi có `chunks`, hàm dùng danh sách đó thay vì gọi `chunk_full_corpus`; sources / identity / sparse state
  tính từ chính danh sách đó. Mặc định `None` = chunker production (hành vi cũ).
- `backend/experiments/phase_8_1/g3_chunking.py` (mới):
  - biến thể là chuỗi bước nối bằng "-" (`h1`, `h3`, `h2_<T>`, `p_nearest`, `p_none`, `s1`, `s2`, `s3`);
  - các lệnh: `stats`, `budget` (ghi B một lần), `build`, `run`, `compare`, `summary`, `drop`;
  - **từ chối:** ghi đè `--name` hay `variant.json` đã có; build khi đã có 3 collection `hue_81_g3_*`; đo khi danh sách đoạn
    tính lại khác sha lúc build;
  - `drop` chỉ xóa đúng `hue_81_g3_<biến thể>` và in danh sách trước / sau;
  - dùng lại `compare` / `gold_coverage` / `load_payloads` / `keep_realism` của harness G1 và `packed_chunk_ids` của G4.
  - Sửa trong lúc làm:
    - runtime gọi tầng sparse là `bm25` (như G1) — lần chạy `budget` đầu lỗi `KeyError`, chưa ghi file nào;
    - `compare` / `summary` bỏ câu out_of_scope cho đúng n = 88 của plan §2. Lần so H1 đầu tính keyword trên 100 câu; số
      dưới đây là số đã tính lại trên 88.
- Không sửa chunker production, `settings.yaml`, `settings_loader.py`, retrieval runtime.

## 2. Bước 1–3: kiểm runtime không đổi, mốc, B, giả định

1. **Runtime không đổi.**
   - Mốc HEAD **trước khi sửa** (12:55): `full_corpus_eval retrieval --treatment dense_bm25_rrf --golden full` → sha
     `cefb2d1a…` = mốc 7B.
   - **Sau khi sửa:** vẫn `cefb2d1a…`.
   - `pytest tests/test_full_corpus_qdrant_ingestion.py tests/test_full_corpus_retrieval.py`: **41 passed**.
   - Biến thể `base` của harness tái tạo đúng `corpus_identity` trong build record runtime (8.459 đoạn), nên bước đánh số lại
     không đổi gì.
   - Qdrant trước G3: chỉ collection runtime.
2. **B = 750 token** `o200k_base` (`data/phase_8_1/g3/budget.json` sha `d02ea2211297`, ghi 12:59:42, **trước** mọi biến thể).
   Trung vị 725,5 trên 88 câu dev số chính trong kho.
   - Baseline G3 (`base.jsonl`, 13:00) khớp G1 `runtime.jsonl` từng câu (108 câu dev): top-10 / context-5 / pool / MRR **0
     lệch**. Ghi chú C23 m4 của plan không xảy ra.
   - Baseline `ctxB_gold_all` = 13/32 = `ctx5_gold_all`, nên trần vẫn là 19 câu.
3. **Giả định trước khi build** (`stats`, cùng chunker):

| Biến thể | Số đoạn | Token e5 p50 / p90 / max | < 64 token | Heading lá 1 đoạn / tổng | Ghi chú |
|---|---:|---|---:|---|---|
| base (runtime) | 8.459 | 85 / 163 / 366 | 2.750 | 451 / 2.457 | |
| h1 | 8.398 | 85 / 162 / 495 | 2.750 | 454 / 2.457 | 14 file đổi |
| h1-h3 | 8.359 | 85 / 163 / 495 | 2.750 | 454 / 2.457 | 100 đoạn dòng bảng → 61 |
| h1-h2_128 | 6.369 | 110 / 172 / 495 | 434 | 770 / 2.457 | 7 lần gộp bị chặn vì khác điều kiện |
| h1-h2_256 | 3.959 | 175 / 241 / 495 | 182 | 1.427 / 2.457 | 7 bị chặn |
| h1-h2_384 | 2.991 | 212 / 349 / 495 | 157 | 2.001 / 2.457 | 7 bị chặn |
| h1-h2_512 | 2.643 | 222 / 429 / 512 | 153 | 2.289 / 2.457 | 7 bị chặn |
| s1 | 8.426 | 85 / 163 / 366 | 2.734 | | −33 đoạn inventory |
| s2 | 8.461 | 85 / 163 / 366 | 2.750 | | +2 đoạn fence |
| s3 | 8.456 | 85 / 163 / 366 | 2.750 | | −3 đoạn lặp (đúng 3 cặp đã dò) |

**Ghi minh bạch:** collection `hue_81_g3_h1` được build (13:03–13:06) trong lúc A / B đang chốt §9. Tin nhắn tới khi lệnh đã
chạy. **Chưa đo gì** trên H1 cho tới khi A duyệt bản `9f00c460c3e9`. A chấp nhận.

## 3. Kết quả

So theo cặp: bootstrap 10.000, seed 20261024, CI 95%. Dev số chính: 32 câu có đoạn đúng, 88 câu trong kho, nhãn sha
`0b65d1c138d2`. Chỉ số quyết: `ctxB_gold_all`. Sàn: 0 câu mất. Keyword trong context-B: cận dưới CI ≥ −2,0 điểm %.

### 3.1 H1 — chỉ kiểm tokenizer e5-small (so baseline; Holm 1)

| Chỉ số | chênh [CI], t/h/t |
|---|---|
| `ctxB_gold_all` (quyết) | 0,000 [0,000; 0,000], 0/32/0 |
| `ctx5_gold_all`, `top10_gold_all` | 0, 0/32/0 |
| keyword context-B (88) | −0,758 [−3,409; +1,136], 1/86/1 |

**Kết luận: không khác.**
- Không câu nào đổi đoạn đúng.
- Cận dưới CI của keyword (−3,41) **vượt** mức tụt cho phép −2,0. Nguyên nhân là đúng 1 câu tụt (và 1 câu tăng), nên H1
  không đủ điều kiện "tốt hơn" dù có thay đổi gì.
- H1 vẫn là base của H3 / H2 theo luật ghi trước (§3 plan: cần bỏ giới hạn HuyDang 256 mới gộp được tới 384 / 512).

### 3.2 H3 — gộp dòng bảng (quyết so với H1; Holm 1)

| So với | `ctxB_gold_all` | `ctxB_gold_frac` | keyword context-B (88) | `ctx5_gold_all` |
|---|---|---|---|---|
| H1 (quyết) | 0,000, 0/32/0 | −0,010 [−0,031; 0], 0/31/1 | −0,284 [−0,852; 0], 0/87/1 | +0,031 [0; 0,094], 1/31/0 |
| baseline | 0,000, 0/32/0 | −0,010, 0/31/1 | −1,042 [−3,693; +0,758], 1/85/2 | +0,031, 1/31/0 |

**Kết luận: không khác.**
- So với H1: không vi phạm sàn, keyword trong mức cho phép, chỉ số quyết không đổi.
- Theo dõi: 1 câu tốt lên ở context 5 đoạn; 1 câu giảm độ phủ một phần.
- H3 không "tốt hơn", nên H2 dựng trên H1, không kèm H3.

### 3.3 H2 — gộp đoạn cùng heading tới T token (quyết so với H1; Holm 4)

| T | `ctxB_gold_all` chênh [CI], t/h/t, p Holm | keyword context-B (88) [CI] | `ctxB_gold_frac` | theo dõi: `ctx5` / `top10` / `pool_union` (t/h/t) | Kết luận |
|---|---|---|---|---|---|
| 128 | 0,000, 0/32/0, 1,0 | −0,852 [−2,841; +0,568] | +0,010, 1/31/0 | 2/30/0 · 0/32/0 · 0/32/0 | **không khác** (keyword cận dưới vượt −2,0) |
| 256 | −0,125 [−0,250; −0,031], 0/28/**4**, 0,091 | −0,284 [−3,788; +3,409] | −0,045, 3/23/6 | 3/26/3 · 1/29/2 · 2/29/1 | **kém hơn** (mất 4 câu) |
| 384 | −0,156 [−0,312; 0,000], 1/25/**6**, 0,135 | −4,924 [−10,606; +0,379] | −0,094, 2/21/9 | 4/24/4 · 3/28/1 · 2/30/0 | **kém hơn** (mất 6 câu) |
| 512 | −0,188 [−0,312; −0,062], 0/26/**6**, **0,018** | −10,038 [−15,720; −4,924] | −0,131, 2/19/11 | 3/26/3 · 5/26/1 · 3/29/0 | **kém hơn** (mất 6 câu; tụt có CI sau Holm) |

So với baseline, `ctxB_gold_all` cho cùng số t/h/t như cột trên vì H1 = baseline ở chỉ số này. Keyword so với baseline:
- 128: −1,61 [−4,83; +0,76];
- 256: −1,04 [−4,07; +1,61];
- 384: −5,68 [−11,74; 0];
- 512: −10,80 [−17,05; −5,11].

**Đọc kết quả:**
- Đoạn to hơn giúp **tìm thấy** đoạn đúng: `top10` / `pool` tăng dần theo T; ở T = 512, top-10 được 5/26/1 và pool 3/29/0.
- Nhưng với **cùng ngân sách 750 token**, số đoạn lọt context ít đi. Đoạn đúng của câu khác bị đẩy ra, nên mất câu.
- Đếm theo số đoạn (`ctx5`, 5 đoạn bất kể độ dài) thì gần hòa. Lý do là context to hơn chứ không phải tìm tốt hơn.
- Đây đúng là bẫy "đoạn to tự thắng" mà ngân sách cố định được đặt ra để chặn.
- **Không biến thể H2 nào "tốt hơn".**

### 3.4 Small-to-big — mở rộng tới cả heading lá sau khi tìm (index runtime; so baseline; Holm 1)

Không có chunker nào "tốt hơn", nên dùng index runtime (plan §3: index tốt nhất tới lúc đó), không build.

| Chỉ số | chênh [CI], t/h/t |
|---|---|
| `ctxB_gold_all` (quyết) | −0,250 [−0,406; −0,125], 0/24/**8** |
| `ctxB_gold_frac` | −0,183 [−0,281; −0,096], 0/19/13 |
| keyword context-B (88) | −15,53 [−23,49; −8,14], 3/63/22 |

Token context-B trung bình: 674,9 (baseline 666,1), 0 câu có đoạn hạng 1 vượt B.

**Kết luận: kém hơn.** Đoạn anh em của 1–2 đoạn đầu chiếm gần hết ngân sách, nên các đoạn xếp hạng sau, gồm cả đoạn đúng,
bị đẩy ra.

### 3.5 Tiền tố tiêu đề trong `search_text` (base = chunker runtime vì chưa có chunker thắng; so baseline; Holm 2)

| Biến thể | `ctxB_gold_all` [CI], t/h/t, p Holm | theo dõi: `top10` / `pool_union` / `ctx5` (t/h/t) | Kết luận |
|---|---|---|---|
| `p_nearest` (chỉ heading gần nhất) | −0,094 [−0,281; +0,094], 4/21/**7**, 0,457 | 4/21/7 · 3/21/8 · 3/24/5 | **kém hơn** (mất 7 câu) |
| `p_none` (không tiền tố) | −0,156 [−0,344; +0,031], 3/21/**8**, 0,317 | 4/21/7 · 4/18/10 · 3/22/7 | **kém hơn** (mất 8 câu) |

- Top-10 đổi ở 120/120 câu, nên tiền tố có tác động mạnh tới tìm kiếm (cả dense lẫn BM25). Bỏ tiêu đề / heading cha làm đoạn mất
  ngữ cảnh "nói về cái gì": có câu được, nhưng nhiều câu mất hơn.
- **Lưu ý đo:** keyword trong context-B (−7,8 / −11,0 điểm %) và MRR keyword tụt một phần vì **cách đo**: chúng tính trên
  `search_text`, mà biến thể đã bỏ tiêu đề khỏi `search_text`. Context đưa model thì vẫn có "Tiêu đề / Mục".
  - Hai số này **không** dùng để kết luận ở đây.
  - Kết luận dựa vào đoạn đúng (chấm theo offset, không phụ thuộc `search_text`): vi phạm sàn.
- Kết luận: giữ tiền tố đầy đủ như runtime (Representation A).

### 3.6 Sửa nhỏ S1–S3 (trên chunker runtime; so baseline; Holm 3)

| Biến thể | `ctxB_gold_all` | keyword context-B (88) | `top10` / `ctx5` | top-10 đổi ở | Kết luận |
|---|---|---|---|---|---|
| S1 bỏ inventory performing_arts (−33 đoạn) | 0/32/0 | 0/88/0 | 0/32/0 · 0/32/0 | 6/120 câu | **không khác** |
| S2 thêm 2 đoạn code fence | 0/32/0 | 0/88/0 | 0/32/0 · 0/32/0 | 4/120 câu* | **không khác** |
| S3 bỏ 3 đoạn lặp | 0/32/0 | 0/88/0 | 0/32/0 · 0/32/0 | 2/120 câu* | **không khác** |

\* Một phần do `chunk_id` trong file bị sửa được đánh số lại, không nhất thiết đổi đoạn thật.

Ở baseline, đoạn inventory lọt top-10 ở 2/120 câu dev.

**Kết luận:** cả ba không làm hỏng gì và không đổi chỉ số nào. Đây là sửa "vệ sinh dữ liệu" an toàn, có thể gộp vào lần build
lại index ở 8.2 (C11 dòng 0.2, 0.7, 2.6). Không có bằng chứng chất lượng tăng.

### 3.7 G3.B10 — đoạn to dưới ngân sách cỡ context 10 (plan §10, bản duyệt `d89a919067ba`)

**Cổng tự kiểm (m2 review B):** `rebudget --budget 750 --prefix ctxB` trên `base`, `h1`, `h1-h2_384`, `h1-h2_512` ra **giống
hệt** bản lưu từ lượt chạy thật:
- 0 lệch ở `ctxB_chunk_ids` / `ctxB_tokens` / `ctxB_first_over` / keyword / `ctxB_gold_all` / `ctxB_gold_frac`;
- 120/120 câu mỗi lượt.

Cổng này chạy **trước** khi tính B10.

**B10 = 1.500 token** (`budget10.json` sha `856a8ab4beb9`, ghi 13:48:39): trung vị 1.475 trên 88 câu.

Context-B10 tính từ top-10 đã lưu; danh sách đoạn dựng lại bằng `make_chunks`, sha khớp `variant.json`. Trung bình trên 88 câu:

| Biến thể | token context-B10 | số đoạn |
|---|---:|---:|
| base | 1.255 | 9,0 |
| H1 | 1.253 | 8,9 |
| H2_384 | 1.329 | 4,8 |
| H2_512 | 1.293 | 4,2 |

0 câu có đoạn hạng 1 vượt B10.

| So sánh | `ctxB10_gold_all` [CI], t/h/t, p Holm | keyword [CI] | Kết luận |
|---|---|---|---|
| **quyết:** H2_384 vs H1 (dưới B10) | 0,500 → 0,344: −0,156 [−0,312; 0], 1/25/**6**, 0,062 | −2,18 [−6,63; +2,18] | **kém hơn** (mất 6 câu) |
| **quyết:** H2_512 vs H1 (dưới B10) | 0,500 → 0,312: −0,188 [−0,344; −0,062], 0/26/**6**, **0,009** | −2,56 [−6,25; +0,85] | **kém hơn** (mất 6 câu; tụt có CI sau Holm) |
| phụ: H2_384 vs runtime ctx10 (G2.1a) | 0,531 → 0,344, 1/24/7 | −2,84 | không đạt (mất 7 câu) |
| phụ: H2_512 vs runtime ctx10 | 0,531 → 0,312, 0/25/7 | −3,22 | không đạt |
| theo dõi: H1 dưới B10 vs runtime ctx10 | 0,531 → 0,500, 0/31/1 | −0,66 [−1,71; 0] | (mất 1 câu: ngân sách B10 cắt trước đoạn thứ 10 ở một câu) |

**Kết luận B10: kém hơn.** Dù ngân sách gấp đôi, đoạn to vẫn để mất 6 câu so với đoạn runtime cùng ngân sách. Đoạn gộp kéo theo
nhiều chữ không liên quan, nên chỉ ~4–5 đoạn vừa ngân sách, thay vì ~9 đoạn nhỏ trỏ tới nhiều chỗ khác nhau. ⇒ **Đóng G3.**

## 3.8 Kết luận G3 (theo tiêu chí ghi trước)

| Hướng | Kết luận | Ghi chú |
|---|---|---|
| H1 chỉ tokenizer e5-small | không khác | 0/32/0; keyword vượt mức tụt do 1 câu |
| H3 gộp dòng bảng | không khác | so H1: 0/32/0 |
| H2 gộp cùng heading (128 / 256 / 384 / 512) | 128 không khác; 256 / 384 / 512 kém hơn | mất 4–6 câu ở ngân sách 750; tìm thấy tốt hơn ở top-10 / pool nhưng ít đoạn lọt context |
| small-to-big | kém hơn | 0/24/8 |
| tiền tố (gần nhất / không) | kém hơn | mất 7 / 8 câu |
| S1 / S2 / S3 sửa nhỏ | không khác | an toàn, đề xuất gộp vào build 8.2 |
| B10: H2 384 / 512 dưới ngân sách cỡ context 10 | kém hơn | mất 6 câu so với H1 cùng ngân sách |
| §4 2×2 + câu trả lời | NOT RUN | không có biến thể "tốt hơn" |

**Lời thường cho User:**
- Mình thử 12 cách chia đoạn khác nhau cho kho dữ liệu, đo xem đoạn có đáp án có lọt vào phần đưa cho model không, với cùng một
  "hạn mức chữ" để công bằng.
- Không cách nào tốt hơn cách đang chạy.
- Gộp đoạn cho to ra thì tìm thấy nhiều hơn, nhưng mỗi đoạn chiếm nhiều chỗ nên ít đoạn vừa hạn mức, và 4–8 câu bị mất đoạn
  đúng. Điều này đúng cả khi nâng hạn mức lên bằng mức "10 đoạn".
- Bỏ tiêu đề khỏi đoạn cũng làm mất câu.
- Ba sửa nhỏ (bỏ file danh mục, giữ 2 khối code, bỏ 3 đoạn lặp) an toàn nhưng không đổi kết quả.
- Kết luận: **giữ cách chia hiện tại**. Cách cải thiện đã có bằng chứng là đưa 10 đoạn cho model (G2).
- Tốn 0 đồng, khoảng 1 giờ máy tính.
- Giới hạn: 32 câu có nhãn đoạn đúng; chỉ đo bước tìm kiếm, chưa đo câu trả lời.

## 3.9 Giới hạn

- **Cỡ mẫu:** 32 câu có đoạn đúng (dev số chính). Kết luận "không khác" ở H1 / H3 / S có thể chỉ vì trần thấp (H1 ≤ 13, H3 ≤ 7
  câu có thể đổi).
- **Chỉ đo retrieval / context.** Không đo câu trả lời (§4 NOT RUN); không xác nhận trên test (không có gì để xác nhận).
- **B10 dùng lại retrieval đã lưu.** Retrieval tất định, sha danh sách đoạn khớp, cổng 750 tái lập 0 lệch. Đây không phải lần
  chạy retrieval mới.
- **Latency** đo khi B chạy G2 / G4-keyword song song (load 1,5–6,3), nên chỉ để theo dõi.
- **Keyword / MRR của biến thể tiền tố** bị lệch theo cách đo (§3.5).
- **B / B10 chỉ đếm token của các khối bằng chứng** (`_block` với id = 1), không gồm dấu ngăn giữa các khối, câu hỏi hay system
  prompt. Đây là xấp xỉ token context thật, nhưng áp như nhau cho mọi biến thể nên không đổi kết luận (review B m1).
- **Keyword trong context-B / B10 chấm trên `search_text`** của các đoạn. Đoạn gộp dài hơn có thể có thêm keyword "miễn phí",
  nên chỉ số này hơi thiên về H2. Dù vậy H2 vẫn kém hơn ở chỉ số quyết (đoạn đúng, chấm theo offset) (review B m2).
- **H1 có 1 câu tụt keyword** (cận dưới CI −3,41). Cần nhắc điều này khi đề xuất bỏ kiểm tokenizer HuyDang ở 8.2.

## 3.10 Khâu còn dính (cho G5 / 8.2; không sửa ở G3)

- `prepare_full_corpus_input` / `build_candidate` tự đọc settings (`_phase4_settings`) và tự tạo client.
- Chunker production chỉ cho đổi tokenizer qua settings. Gộp đoạn / tiền tố phải làm trong harness. Nếu 8.2 cần thì thêm tham
  số vào chunker.
- `FullCorpusContextBuilder` không có ngân sách token nhỏ hơn `context_limit`, cũng không trả `chunk_id` trong
  `PackedSource`. Harness phải dùng `_source` / `_block`, là hai hàm private.

## 4. Thông số từng lượt

Chung:
- e5-small-384 (`intfloat/multilingual-e5-small`, CPU);
- retrieval `dense_bm25_rrf` pool 30, k 60, top-10;
- context-5 / 10 = `FullCorpusContextBuilder` (settings, `max_context_documents` 5 / 10);
- context-B = B 750 token `o200k_base`, lấy theo hạng, dừng ở đoạn đầu tiên làm vượt B;
- split `knowledge-base-hue/evaluation/phase_8_1/split.json` (dev 120); gold `bab707b9…`; seed 20261024.
- Lệnh:
  - `HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g3_chunking build|run|drop --variant <v> [--name <v>]`
    (từ `backend/`);
  - chuỗi build → run → drop chạy bằng `/tmp/c29/queue.sh` (script tạm của C, dừng ở lỗi đầu tiên).
- Kết quả: `data/phase_8_1/g3/<tên>.jsonl` + `.meta.json`; build: `data/phase_8_1/builds/<v>/` (`variant.json`,
  `build_record.json`, `sparse_state.json`).

| Biến thể | collection | số đoạn | sha danh sách đoạn | sparse state sha | build record sha | build (s) | build xong | đo retrieval p50 / p95 ms | load lúc đo | đã xóa |
|---|---|---:|---|---|---|---:|---|---|---|---|
| base | runtime | 8.459 | — | — | — | — | — | 23 / 27 | 1,8 | — |
| h1 | `hue_81_g3_h1` | 8.398 | `60f213fb4af1` | `9fb0057e3797` | `cbc589daf691` | 199 | 13:06:30 | 26 / 30 | 1,5 | ✓ (13:09) |
| h1-h3 | `hue_81_g3_h1-h3` | 8.359 | `8a2d81769689` | `3fb6a6fbb1a9` | `a1a328464fcb` | 202 | 13:13:39 | 24 / 27 | 4,9 | ✓ (13:14) |
| h1-h2_128 | `hue_81_g3_h1-h2_128` | 6.369 | `59fd5cd60cf7` | `b8ac35341101` | `28bac7b94a29` | 189 | 13:18:32 | 25 / 33 | 5,4 | ✓ |
| h1-h2_256 | `hue_81_g3_h1-h2_256` | 3.959 | `948172610fc7` | `b58de9745e4c` | `9ea07d12415b` | 169 | 13:22:09 | 26 / 29 | 4,9 | ✓ |
| h1-h2_384 | `hue_81_g3_h1-h2_384` | 2.991 | `dee84e7bcebc` | `4d712a533472` | `a45eb525c660` | 169 | 13:25:46 | 28 / 34 | 5,8 | ✓ |
| h1-h2_512 | `hue_81_g3_h1-h2_512` | 2.643 | `908f09f17c3d` | `91c389580b84` | `33e807690d72` | 167 | 13:29:25 | 28 / 33 | 5,8 | ✓ |
| s2b_base (`--expand`) | runtime | 8.459 | — | — | — | — | — | 25 / 30 | 3,1 | — |
| p_nearest | `hue_81_g3_p_nearest` | 8.459 | `c0a8023eb920` | `8663daa42e42` | `8dbda08facd8` | 203 | 13:35:34 | 25 / 31 | 5,9 | ✓ |
| p_none | `hue_81_g3_p_none` | 8.459 | `bde81b16e8d7` | `c8aec6f520de` | `3feb7b6c6f29` | 180 | 13:39:51 | 23 / 29 | 6,0 | ✓ |
| s1 | `hue_81_g3_s1` | 8.426 | `e8d8dc70a93c` | `d19188bcc217` | `665314bbab79` | 222 | 13:44:21 | 24 / 32 | 6,3 | ✓ |
| s2 | `hue_81_g3_s2` | 8.461 | `0c4b63904d6b` | `3d8bd889b9cd` | `b74cf8dc28a2` | 220 | 13:49:03 | 26 / 31 | 5,9 | ✓ |
| s3 | `hue_81_g3_s3` | 8.456 | `ba949d2a08fa` | `01dac59ed724` | `f9f6f4e76966` | 219 | 13:53:49 | 23 / 27 | 5,2 | ✓ |

B10 (`rebudget`, offline, không Qdrant), từ: `base`, `h1`, `h1-h2_384`, `h1-h2_512` →
`b10_<v>.jsonl`. Cổng: `gate750_<v>.jsonl`.

Latency chỉ để theo dõi (A, cách hiểu b). "load" là load average 1 phút lúc bắt đầu đo. B chạy G2 + judge cùng lúc, nên
load 2–5 khi build / đo H1, H3. Collection: **tối đa 1 `hue_81_g3_*` cùng lúc** tới giờ. Mỗi lần xóa đều in danh sách
trước / sau; sau mỗi lần chỉ còn collection runtime.

Tiền: **0 USD**. Collection `hue_81_g3_*`: 11 lần tạo / 11 lần xóa, tối đa 1 cùng lúc. Cuối G3 (13:56) `GET /collections` chỉ
còn `hue_full_corpus_7a2_e5_small_384`. Mốc byte runtime cuối G3: `cefb2d1a…`.

## 5. Bàn giao cho người kiểm (B)

Theo plan §8:
- Mốc byte. Đã chạy 3 lần: trước sửa, sau sửa, cuối G3.
- `compare` từ JSONL: lệnh ở §3, có `--a-fields` cho §3.7.
- **Build lại một biến thể bất kỳ từ đầu**, kiểm sha danh sách đoạn + số đoạn giống §4. `stats` cho sha ngay, không cần build.
- `drop` cuối cùng: Qdrant chỉ còn collection runtime (đã đạt).

Diff:
- `backend/ingestion/full_corpus_pipeline.py` (`chunks=None`);
- `backend/experiments/phase_8_1/g3_chunking.py` (mới).

Dữ liệu private:
- `data/phase_8_1/g3/`, `data/phase_8_1/builds/<v>/`;
- script tạm `/tmp/c29/` (queue, probe) và `/tmp/c28/` (probe kế hoạch).
