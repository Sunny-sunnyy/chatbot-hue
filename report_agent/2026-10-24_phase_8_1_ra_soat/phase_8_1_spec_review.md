# Review: spec Phase 8.1 (nháp của A)

Decision: **changes_requested** (2 major, 10 minor; không có blocker)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-a3`)
Date: 24/10/2026, 20:15–20:24 (giờ lấy bằng `date`)
Spec: `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` (đọc hết, bản 20:20)
Đối chiếu:

- C11 `phase_8_1_decision_inventory.md` (top 10 §4, thứ tự §5);
- C14 `phase_8_1_research_url_check.md`;
- `session_prompt/CURRENT_HANDOFF.md` (User chốt 19:00, 20:01) và `Project_Status.md` §5;
- code ở `1832201` (working tree).

Chỉ đọc; không sửa spec.

## 1. Phạm vi đã review

- **Sự thật về code/dữ liệu trong spec:** loader, generator, retrieval, context builder, pipeline build,
  sparse state, dependency.
- **Độ phủ** so với top 10 và các dòng "ngay dưới top 10" của C11.
- **Thứ tự gate và phụ thuộc** giữa chúng.
- **Tiêu chí nghiệm thu** §6: có kiểm được không.
- **Quyền và tiền** (§8).
- **Độ phức tạp.**

**Đúng sự thật** (đã kiểm):

- Số liệu C11 (2/56, 29, 16);
- loader ép tổ hợp runtime (`settings_loader.py:39-44`);
- giá luna và ước 120 câu ~0,016 USD (= 0,024 × 120/176);
- thông số M1 (bge 568M, Apache-2.0, fine-tune 1024; C14 S20/S21);
- M2 tối đa 1024 chiều (C14 S22);
- D8 khớp User chốt 20:01;
- D1–D5 khớp `Project_Status.md` §5 dòng 2026-10-24 (tối).

**Độ phủ top 10 C11:** cả 10 dòng đều có bước.

| Hạng C11 | Bước trong spec |
|---|---|
| 1 | G3 (H1/H2/section) |
| 2 | G2.1–2 |
| 3 | prompt + effort ở G2; model sinh loại theo D7 |
| 4 | G4 M2 |
| 5 | G0 |
| 6 | G1.1–3 |
| 7 | G3 H3 |
| 8 | G1.5 + G4 M1 |
| 9 | G3 H1 |
| 10 | §3.1–3.2 |

Các dòng ngay dưới top 10 cũng có bước: NFC (G1.4), validator (G2.3), tiền tố tiêu đề (G3), BM25 tiếng
Việt (G4).

## 2. Findings

### Major

**M1. Nhiều thí nghiệm không chạy được bằng "gọi hàm production với tham số" như §3.1 viết.**

- **Bằng chứng** (code `1832201`):
  - Generator gắn cứng prompt và model settings: `backend/llm/generator_openai_full_corpus.py:117-126`
    (`instructions=ANSWER_SYSTEM_INSTRUCTIONS`, `ModelSettings(max_tokens, include_usage, store)`,
    không có reasoning). Vậy G2.2 (3 prompt) và G2.4 (`reasoning.effort`) không đổi được qua tham số.
  - Retrieval có pool, `k` và cách tìm là hằng: `retrieval/full_corpus.py:465`, `:561` (`limit=30`),
    `:608` (`reciprocal_rank_fusion(branches, k=60, limit=30)`). `query_points` không có `search_params`
    (`:461-476`). Vậy G1.1 (pool 100/200), G1.2 (`exact`) và G1.3 (k ∈ {2,10,30,60}) không đổi được qua
    tham số.
  - Pipeline build ánh xạ cố định candidate → collection runtime (`ingestion/full_corpus_pipeline.py:66-69`),
    record ở `data/full_corpus_builds/` (`:53`), sparse state chung ghi một lần
    `full_corpus_sparse_state.json` (`:55`, `:125-131`). Gọi `build_candidate` cho một biến thể chunker
    sẽ raise vì sparse state khác, hoặc nhắm vào collection runtime. §3.2 muốn record riêng ở
    `data/phase_8_1/builds/` nhưng không nói sparse state riêng, và không nói build bằng đường nào.
- **Yêu cầu bị ảnh hưởng:**
  - §3.1 ("không sửa runtime");
  - §4 "Ngoài: sửa runtime": không nói rõ có được thêm tham số vào module production không;
  - §6.4.
- **Tác động:** người làm G1–G3 sẽ phải tự chọn một trong hai. Hoặc sửa module production (đụng ranh
  giới "không đổi runtime"). Hoặc chép lại logic retrieval/generator/build vào harness (code trùng, lệch
  dần, đo nhầm vì không còn là đường production).
- **Tiêu chí đóng:** spec ghi rõ **một** luật. C đề xuất cách đơn giản nhất:
  - Cho phép thêm tham số keyword có **mặc định = giá trị hiện tại** vào đúng các chỗ sau:
    - pool, `k`, `search_params` của retrieval;
    - `instructions`, `model_settings` của generator;
    - đường dẫn collection/record/sparse state của build.
  - Kèm điều kiện sau mỗi lần sửa: pytest full-corpus đạt; retrieval runtime giống từng byte mốc 7B;
    review chéo.
  - Ghi sparse state riêng mỗi biến thể trong `data/phase_8_1/builds/`.
  - Liệt kê các file production được phép đổi trong §4 "Trong".

**M2. Chưa rõ cách "xác nhận trên 56 câu kiểm" cho metric cần đoạn đúng.**

- **Bằng chứng:**
  - §6.2 bắt phương án "tốt hơn" phải xác nhận trên 56 câu kiểm.
  - Đoạn đúng chỉ gắn cho ~40 câu, "ưu tiên trong 120 câu thử" (G0.3).
  - Nhưng nhiều metric chính lại cần đoạn đúng: candidate recall theo đoạn đúng (G1.1), nhãn tầng lỗi
    (G1.6), claim không nguồn / required facts (G2.2, "40 câu có đoạn đúng").
- **Tác động:** hoặc không xác nhận được trên tập kiểm (§6.2 không đạt được), hoặc phải gắn đoạn đúng cho
  câu kiểm giữa chừng mà không ai quyết.
- **Ghi thêm:** 56 câu kiểm không còn "chưa ai thấy". B4, B5, C1, C11 đã phân tích cả 176 câu, trong đó
  có 22 câu từ chối nhầm. Nghiên cứu §2 nói rõ trường hợp này không còn là holdout thật. Chỉ 30–40 câu
  mới là kín thật.
- **Tiêu chí đóng:** spec chọn một trong hai:
  - (a) Gắn đoạn đúng cho cả các câu khó thuộc 56 câu kiểm ngay ở G0. Gắn nhãn không phải tune, nhưng
    người gắn không xem kết quả thí nghiệm.
  - (b) Ghi rõ metric nào dùng để xác nhận trên 56 câu (keyword + điểm câu trả lời), và metric theo đoạn
    đúng chỉ là bằng chứng trên tập thử.

  Kèm theo: ghi giới hạn "56 câu kiểm đã từng được phân tích" vào §9.

### Minor

- **m1. M3 `pyvi` không phải dependency mới.** `pyvi==0.1.1` đã có trong `pyproject.toml`, chunker
  đang dùng (`backend/ingestion/preview.py:21`). Sửa §7: bỏ "`uv add`", ghi "đã có, không cần duyệt
  thêm" hoặc bỏ khỏi bảng duyệt.
- **m2. Kích thước và lựa chọn dense.**
  - M2 chạy CPU thường ở fp32: 0,6B ≈ **2,4 GB**. Con số 1,2 GB là bf16.
  - Ứng viên rẻ hơn `intfloat/multilingual-e5-base` (dự án từng dùng, cùng họ e5) không có trong G4.
    C11 3.1 đề xuất nó như phương án free. Thêm vào G4, hoặc ghi lý do bỏ.
- **m3. Phụ thuộc G2 → G3.** Kết luận context 5/10 và prompt ở G2 đo trên chunker hiện tại. G3 đổi cỡ
  chunk, mà nghiên cứu §2 chỉ ra chunk và context có tương tác. Tiêu chí đóng: G3 chạy lại context 5 vs
  10 cho biến thể thắng (paid nhỏ), hoặc G5 ghi kết luận G2 chỉ đúng với chunker cũ.
- **m4. Tự kiểm thống kê G0.2 mới có đối chứng âm.**
  - Cần định nghĩa "không khác", ví dụ CI 95% chứa 0 ở mọi metric chính.
  - Nên thêm một đối chứng dương để chắc phép kiểm phát hiện được khác biệt thật, ví dụ một biến thể
    cố ý kém: context 1 đoạn, hoặc bỏ BM25.
  - Lỗi citation tự dao động giữa Run 1/Run 2 ở 6/176 câu (review B9 §4). Metric này cần đo theo cặp
    và báo nhiễu.
- **m5. Bớt độ phức tạp thống kê.** Paired bootstrap (CI) là đủ cho mỗi metric chính. Permutation trùng
  vai với bootstrap. Holm chỉ cần khi tuyên bố nhiều phương án thắng cùng lúc. Đề xuất: bootstrap CI +
  thắng/hòa/thua; Holm khi có >1 phương án "tốt hơn" trong cùng câu hỏi. Kiểm khớp cấu hình ở §3.2 nên
  giữ ở mức một phép so hash cấu hình chunker ghi trong record, không thêm validator.
- **m6. Tiền cho `reasoning.effort=high`.** Token suy luận tính giá output ($0,5/M), số lượng chưa biết.
  §8 không ước. Tiêu chí đóng: chạy thử 10 câu trước, chiếu tiền cho 120 câu, dừng nếu vượt phần trần
  còn lại.
- **m7. Ghi NOT RUN cho hướng bị loại.** §6.3 chỉ đòi top 10. Representation B (H10) và BM25 k1/b (C11
  3.8) không có bước nào. H10 ước thô ~0,6 USD (8.459 call; lấy 104 token ra của lần gọi thử duy nhất ở Phase 6 làm
  mức mỗi call; ~200 token vào) > trần 0,5 USD. G5 nên liệt kê chúng là NOT RUN kèm lý do.
- **m8. Quyết định User chưa ghi đủ ở nguồn sự thật.** `Project_Status.md` §5 dòng 2026-10-24 (tối) có
  D1–D5. **D6, D7, D9 chưa có**, và `CURRENT_HANDOFF.md` "Câu hỏi cho User" còn để mở các câu Golden và
  bằng chứng chuẩn. D7 hoãn cam kết của amendment 2026-10-01 §5 / 2026-10-23 R6. Cần ghi D7 là
  "supersede" amendment đó để reviewer sau không tưởng sót.
- **m9. Quota judge Claude.** C3 tốn ~1,1M token Claude Code cho 382 lượt chấm. G2–G3 có thể cần chấm
  hàng chục lượt × 120 câu.
  - Tiêu chí đóng: chỉ chấm câu trả lời cho biến thể đã qua vòng truy xuất/đếm từ chối, và ước số lượt
    chấm trong §8.
  - §3.5 nên ghi: judge **cùng model** với lần chấm baseline (Opus 5.5); đổi model thì chấm lại
    baseline (C11 7B.3).
- **m10. Lỗi chữ nhỏ.** G1.3 ghi "`native_hybrid_rrf`, pool 30/100". Pool hiện là hằng 30 (xem M1),
  nên pool 100 phụ thuộc luật ở M1. §3.4 "permutation test" gắn với m5.

## 3. Cách người kiểm chạy lại thật

Không chạy thí nghiệm. Chỉ đọc code ở `1832201`:

- `sed`/`grep` trên `backend/llm/generator_openai_full_corpus.py:110-130`;
- `backend/retrieval/full_corpus.py` (dòng 149, 465, 561, 608);
- `backend/retrieval/full_corpus_context.py:25-38` (tham số `context_limit`, `max_documents` có sẵn);
- `backend/ingestion/full_corpus_pipeline.py:53-131`;
- `pyproject.toml` / `uv.lock` (`pyvi 0.1.1`, `transformers 5.14.1`).

Đối chiếu tài liệu: `CURRENT_HANDOFF.md` dòng 13–23, `Project_Status.md` dòng 114.

## 4. Kết quả quan sát

Như mục 2. Context builder đã nhận `max_documents` / `context_limit` (`full_corpus_context.py:25-33`),
nên G2.1 (5 vs 10 đoạn) chạy được bằng tham số mà không cần sửa code.

## 5. Giới hạn

- Không kiểm `transformers 5.14.1` có chạy được `Qwen3-Embedding-0.6B` không (cần thử khi G4 được
  duyệt).
- Không kiểm giấy phép của M2 trên trang model (spec ghi Apache-2.0; C14 không kiểm mục giấy phép).
- Không đánh giá thời gian công người của D5/D6.

## 6. Decision và bước tiếp theo

**`changes_requested`.** A sửa M1 (một luật rõ cho thay đổi code production + sparse state riêng) và M2
(cách xác nhận trên tập kiểm) trước khi trình User. Các minor sửa cùng lượt nếu tiện; m1, m8 nên sửa vì
ảnh hưởng tới bảng duyệt và nguồn sự thật. Sau khi sửa, C kiểm lại phần đổi.

## 7. Kiểm lại spec v2 (C15b, 24/10/2026 20:28)

Đọc lại toàn bộ spec v2 (file untracked, không có diff), tập trung các mục A nêu: §3.1, §3.4–5, §4,
G0.2–G0.6, G2.4, G3, G4, §7, §9. Đối chiếu `Project_Status.md` §5 và code `backend/retrieval/full_corpus.py`.

| Finding | Xử lý ở v2 | Kết luận |
|---|---|---|
| M1 thí nghiệm cần tham số trong code production | §3.1 thêm luật "tham số keyword, mặc định = giá trị hiện tại"; §4 liệt kê 3 file; G0.5 gate pytest + retrieval giống byte + review; G3 sparse state riêng `data/phase_8_1/builds/<biến_thể>/` | **Đóng**, còn r1–r2 (dưới) |
| M2 xác nhận 56 câu kiểm với metric đoạn đúng | Phương án (a): ~40 câu thử + ~15 câu kiểm có đoạn đúng (D6 ghi rõ là A mở rộng, công User không đổi); §9 thêm rủi ro "56 câu không kín thật" | **Đóng** |
| m1 pyvi / e5-base | §7 "Không cần duyệt (đã có)"; G4 thêm e5-base | **Đóng** |
| m2 cỡ M2 | 2,4 GB fp32 | **Đóng** |
| m3 chunk × context | G3: biến thể thắng chạy lại context 5 vs 10 | **Đóng** |
| m4 đối chứng | G0.2: đối chứng âm (CI chứa 0) + dương (xáo thứ tự top-10 → MRR/nDCG phải kém) | **Đóng** (r3) |
| m5 thống kê | §3.4 bỏ permutation; Holm khi >1 biến thể thắng | **Đóng** |
| m6 tiền effort | G2.4 pilot 10 câu trước | **Đóng** |
| m7 NOT RUN | §4: H10 (~0,6 USD), k1/b, H12, H13 kèm lý do | **Đóng** |
| m8 quyết định User | `Project_Status.md` §5 có dòng D6 (đoạn đúng) và D7 (giữ luna, **thay** amendment 10-01 §5 + 10-23 R6); D8/D9 ở dòng B9 đóng | **Đóng** |
| m9 judge | §3.5 cùng model judge; đổi thì chấm lại baseline; ước ~12 lô/lượt 120 câu | **Đóng** |
| m10 pool 100 phụ thuộc M1 | Nằm trong luật M1 | **Đóng** |

**Còn lại (minor, sửa chữ trong cùng lượt; không cần vòng review mới):**

- **r1. Danh sách tham số của retrieval còn thiếu hai chỗ thí nghiệm cần.** §3.1 chỉ ghi "pool, RRF k".
  - G1.2 cần thêm `search_params` / `exact`: `query_points` hiện không nhận (`full_corpus.py:461-476`).
  - G3 cần truy vấn collection `hue_81_*`, nhưng `build_full_corpus_retrieval_service` lấy cố định
    `candidate.collection_name`, `build_record_path(candidate)` và `SPARSE_STATE_PATH`
    (`full_corpus.py:723-750`).

  Tiêu chí đóng: thêm "exact/search params; collection, build record, sparse state" vào danh sách tham
  số của retrieval ở §3.1.
- **r2. Chưa nói code biến thể chia đoạn nằm ở đâu.** H3 (nhóm dòng), H2 (gộp khối), "1 heading lá = 1
  đoạn", tiền tố tiêu đề là **logic mới**, không chỉ là "cấu hình tokenizer" như §4 ghi. Tiêu chí đóng:
  §3.1/§4 chọn một trong hai:
  - (a) logic mới nằm trong harness, xử lý tiếp danh sách chunk của `chunk_full_corpus`; chunker
    production không đổi;
  - (b) thêm tham số vào chunker, mặc định tắt, chịu cùng gate G0.5.

  C nghiêng (a): không đụng chunker runtime; small-to-big vốn đã là xử lý sau khi tìm.
- **r3. Seed cố định cho đối chứng dương** (xáo top-10) để tái lập. Một chữ trong G0.2.

**Kết luận v2:** `ready_for_user_confirmation` sau khi A bổ sung r1–r3 (sửa chữ). Không còn
blocker/major. C không cần kiểm lại riêng phần r1–r3. A tự xác nhận khi trình User, ghi trong
`CURRENT_HANDOFF.md`.

## 8. Kiểm nhanh spec v4 (C15c, 24/10/2026 20:40) — chỉ phần đổi

**Đã đọc trong spec:** D10, D11, §3.1 (r1–r2), G0.2 (r3), G1.3, G4, §4, §7, §10.

**Đã đối chiếu:**

- `Project_Status.md` §5;
- ghi chú private về dự án khác của User (`data/phase_8_1/external_lessons_private.md`, không commit) —
  chi tiết đối chiếu nằm ở đó;
- model card `AITeamVN/Vietnamese_Reranker` (WebFetch).

**Đã chạy:** `uv run python -c "import torch…"` ra `2.13.0+cu130 True NVIDIA GeForce GTX 1650` — khớp D11.

| Phần đổi | Kiểm | Kết luận |
|---|---|---|
| r1 tham số retrieval | §3.1 thêm `exact`/search params cho `query_points` (`full_corpus.py:461-476`), tên collection + build record + sparse state (`:723-750`) | **Đóng** |
| r2 nơi đặt logic chia đoạn | §3.1: logic mới nằm trong harness, xử lý tiếp chunk của `chunk_full_corpus`; chunker production không đổi | **Đóng** |
| r3 seed | G0.2 "seed cố định ghi trong report" | **Đóng** |
| D10 (dense chỉ e5-small + 8B) | Khớp `Project_Status.md` §5 dòng 117 và spec 7A2 §2. §4 "Ngoài" có "dense model khác e5-small (D10)". §7 bỏ e5-base/Qwen3-0.6B. C11 hạng 4 sẽ thành NOT RUN có lý do — §6.3 cho phép | **Đúng** |
| D11 (rerank GPU fp32, đo thêm CPU) | torch CUDA có thật (trên). Lý do chọn fp32 khớp ghi chú private. Ghi ở `Project_Status.md` §5 dòng 117 | **Đúng** |
| G1.3 DBSF + "0 câu mất đoạn đúng" | Bài học "để từ khóa chọn ứng viên có thể làm mất đáp án; chỉ cho từ khóa xếp lại thì không" khớp ghi chú private. Chú ý: cách "chỉ xếp lại" đó **chính là** `dense_bm25_rrf` đang chạy, nên G1.3 đúng là phép kiểm chiều ngược lại | **Đúng** (n1) |
| G4 từ khóa "âm tiết + cặp âm tiết + nguyên cụm mã" | Khớp ghi chú private | **Đúng** |
| G4 rerank: chỉ xếp lại top-10, đoạn trơn vs đoạn kèm mục | Khớp ghi chú private: chấm kèm ngữ cảnh rộng hơn tốt hơn chấm đoạn rời | **Đúng** (n2, n3) |
| §7 M1 bge | Như C14 (S20/S21); fp32 ~2,3 GB VRAM hợp lý cho 568M × 4 byte | **Đúng** |
| §7 M2 `AITeamVN/Vietnamese_Reranker` | Card: "License: apache-2.0", "fine-tuned from the bge-reranker-v2-m3", "0.6B params", F32, max length 2304 (256 query + 2048 passage), huấn luyện ~1,1M triplet, benchmark Legal Zalo 2021 MRR@10 0,8672. Ghi chú private: chạy CPU chậm hơn GPU nhiều lần | **Đúng** (n4) |
| §10 nguồn ngoài | Spec chỉ trỏ ghi chú private, ghi rõ là giả thuyết từ dữ liệu khác | **Đúng** |

**Ghi chú minor** (không chặn; sửa chữ nếu tiện):

- **n1. Tiêu chí "0 câu mất đoạn đúng khỏi top-10" (G1.3) cần nói đo trên tập câu nào.** "Đoạn đúng"
  chỉ có ở ~55 câu. Với các câu còn lại nên dùng keyword-hit so với baseline. Nếu không ghi, tiêu chí
  chỉ phủ ~55/158 câu.
- **n2. Ở G4 rerank, chỉ số "mất" cần đo ở 5 đoạn đưa model, không phải top-10.** Rerank chỉ xếp lại
  top-10 thì theo định nghĩa không làm mất đoạn khỏi top-10. Nên đổi thành "0 câu mất đoạn đúng khỏi 5
  đoạn đưa model".
- **n3. Mục tiêu "p95 ≤ 3 s" có thể không đạt với biến thể "đoạn kèm mục".**
  - Số đo tốc độ GPU trong ghi chú private cho thấy chấm nhiều cặp dài vài trăm token đã mất vài giây.
  - 10 cặp × đoạn trơn (trung vị 85 token) chắc nhanh.
  - 10 cặp × "đoạn kèm mục" cắt tới 1024 (bge) hoặc 2048 (AITeamVN) token có thể vượt 3 s.

  Đề xuất: giữ tiêu chí, nhưng đo trước 5–10 câu với độ dài thật, và ghi cắt mục ở bao nhiêu token. Có
  một điểm cần chốt: max length của AITeamVN là 2304, không phải 1024; "cắt ở giới hạn huấn luyện của
  model" nghĩa là hai model cắt khác nhau. Hai model sẽ thấy lượng chữ khác nhau; nên chọn cùng một
  mức cắt (ví dụ 1024) để so công bằng.
- **n4. §7 M2:** nay ghi được giấy phép **Apache-2.0** (đã kiểm card), thay cho "kiểm khi tải". Con số
  VRAM ~2,3 GB nên ghi là "ước 0,6B × 4 byte" nếu không có số đo trực tiếp.
- **n5.** Dòng Status còn ghi "draft v3". Nên ghi "draft v4".

**Kết luận v4:** phần đổi đúng sự thật và nhất quán với các quyết định đã ghi; không có blocker/major.
**`ready_for_user_confirmation`**. n1–n5 là sửa chữ, A tự áp dụng, không cần C kiểm lại.

*Sửa 24/10 (C15d): repo public — đã gỡ tên dự án khác, số đo và đường dẫn của dự án đó khỏi mục này; chi
tiết đối chiếu ở ghi chú private. Kết luận review không đổi.*
