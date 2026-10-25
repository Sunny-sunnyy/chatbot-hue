# Kế hoạch G3 — biến thể chia đoạn (tiêu chí ghi trước)

Người viết: C (Claude Opus 5.5, terminal `hue-rag-a1`) · 2026-10-25 12:48 +0700 (`date`) · Việc: C28 · Trạng thái:
**nháp, chờ A duyệt kèm sha; B review khi rảnh; chưa build, chưa chạy gì có phí**.

Căn cứ:
- spec `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` §3.1 (logic chia đoạn mới nằm trong
  harness, chunker production không đổi), §3.2 (mỗi biến thể một collection `hue_81_*` + build record riêng), §5 G3, §6, §8;
- skill `run-experiment`;
- G1 (`phase_8_1_g1_implementation.md` §4–§7), G4 (`phase_8_1_g4_implementation.md`);
- `report_agent/2026-10-25_cai_tien_cach_lam/de_xuat_cho_du_an.md`;
- bảng rà C11 (`phase_8_1_decision_inventory.md` dòng 0.2, 0.7, 2.1–2.7);
- giả thuyết `reports/phase_8_candidate_hypotheses_2026_10_24.md` H1–H3.

## 0. Lớp bài toán và dữ kiện đã kiểm bằng máy (12:45, chỉ đọc)

**Lớp bài toán (G1):** đoạn đúng thường đã có trong pool, nhưng bị xếp ra khỏi top-10 hoặc khỏi 5 đoạn đưa model. Nguyên
nhân nghi ngờ: đơn vị chia quá vụn. Trung vị 85 token; 2.750/8.459 đoạn (32%) dưới 64 token e5. Một mục (heading lá) bị
chia thành nhiều đoạn, nên mỗi đoạn mang ít ngữ cảnh để khớp câu hỏi. Bảng dài bị tách mỗi dòng một đoạn, nên dòng giá
không có ngữ cảnh.

C chạy chunker production trên corpus hiện tại (script tạm `/tmp/c28/probe*.py`, không ghi dữ liệu dùng chung):

| Dữ kiện | Hiện tại (3 tokenizer) | Chỉ e5-small 512 (H1) |
|---|---:|---:|
| Số đoạn | 8.459 | 8.398 (−61) |
| Token e5 p50 / p90 / max | 85 / 163 / 366 | 85 / 162 / 495 |
| Đoạn có phần `header` (dòng bảng / mục con bị tách) | 180 | 100 |
| Heading lá (source, heading_path) | 2.457 | 2.457 |
| Heading lá có > 1 đoạn | 2.006 | 2.003 |
| File có số đoạn khác nhau so với hiện tại | — | 14 (heritages 7, travel/tickets 3, mỗi domain còn lại ≤ 1) |

Thêm:
- Dev số chính có đoạn đúng: **32 câu** (nhãn `golden_realism_final.jsonl` sha `0b65d1c138d2`; gold `bab707b9…`).
  - 13/32 câu có đoạn đúng nằm ở một trong 14 file mà H1 làm đổi. Đây là trần trên cho số câu H1 có thể đổi.
  - 7/32 câu có đoạn đúng nằm trong đoạn có phần `header` (bảng / mục con bị tách). Đây là trần trên cho H3.
- File inventory performing_arts **vẫn được index**: 33 đoạn (C11 dòng 0.2).
- 2 file có code fence: `Đàn Nam Giao.md`, `Đàn Xã Tắc.md`. Parser bỏ fence không báo, mất ~360 ký tự (C11 dòng 0.7).
- 3 cặp đoạn lặp body (blockquote trong list item, `markdown_blocks.py:233-251`; C11 dòng 2.6).
- Embed e5-small trên CPU: 512 đoạn mất 11,8 s, nên 8.459 đoạn mất khoảng **3,3 phút**. Build một biến thể (chia + embed +
  upsert + kiểm) ước **≈ 5 phút CPU**. **G3 không cần GPU**: nếu dùng GPU thì kiểm như B17 §0, chỉ khi B không giữ GPU.

## 1. Chung cho mọi biến thể

- **Baseline:** runtime commit hiện hành (`dense_bm25_rrf`, pool 30, k 60, top-10, e5-small-384, collection
  `hue_full_corpus_7a2_e5_small_384`). Trước khi đo, chạy lại retrieval runtime; phải giống byte mốc `cefb2d1a…`. Không
  khớp thì dừng, báo A.
- **Tập câu:** dev **số chính** (bỏ `unnatural`, nhãn sha `0b65d1c138d2`), tức 88 câu trong kho, trong đó 32 câu có đoạn
  đúng. G3 chạy CPU nên không chịu giới hạn 30 câu GPU: **chạy cả nhóm dev**. Số phụ là "chỉ natural". Xác nhận trên test:
  15 câu có đoạn đúng (10 thuộc số chính). Ghi giới hạn: 15 câu này đã bị nhìn ở G1.6.
- **Đoạn đúng:** chấm theo vị trí trong file nguồn (`gold_coverage` / `chunk_hits_quote` của harness G1). Đúng cho mọi cách
  chia, vì đoạn gộp giữ nguyên `evidence_parts` (offset).
- **Ngân sách token context cố định** (spec G3 "tránh đoạn to tự thắng"):
  - Bước 2 (§5) đo **B** = trung vị số token `o200k_base` phần bằng chứng của 5 đoạn context runtime trên dev, làm tròn lên
    bội 50. Ghi B vào report **trước** khi đo biến thể nào.
  - Mọi biến thể dựng "context-B": lấy đoạn theo hạng (sau bước bỏ đoạn không bằng chứng như `FullCorpusContextBuilder`)
    cho tới khi tổng token ≤ B.
  - Đoạn hạng 1 lớn hơn B thì vẫn lấy nguyên đoạn đó, và đếm riêng số câu như vậy.
  - "5 đoạn đưa model" (đếm theo số đoạn, như runtime) là chỉ số theo dõi.
- **Theo cặp:** `compare` của harness G1 (bootstrap 10.000, seed 20261024, CI 95%, thắng/hòa/thua); Holm trong từng
  nhóm biến thể ghi ở §3.
- **Một collection một biến thể:**
  - tên `hue_81_g3_<biến_thể>`;
  - build record + sparse state riêng: `data/phase_8_1/builds/<biến_thể>/{build_record.json,sparse_state.json}`;
  - harness từ chối chạy nếu record không khớp cấu hình biến thể (ghi `variant_config` + sha danh sách đoạn trong record
    phụ của harness);
  - **tối đa 3 collection `hue_81_*` cùng lúc**; đo xong biến thể nào thì xóa ngay collection đó;
  - liệt kê `GET /collections` trước và sau mỗi lần tạo / xóa, ghi vào report;
  - không bao giờ ghi collection runtime.
- **Tiền:** retrieval và build miễn phí (e5 local). Paid chỉ ở §4 (câu trả lời cho biến thể thắng).

## 2. Chỉ số (định nghĩa chính xác, ghi trước)

| Tên | Hàm / cách tính | Tập, n | Vai trò | Ngưỡng |
|---|---|---|---|---|
| `ctxB_gold_all` — đủ mọi fact trong context-B | `gold_coverage(facts, payloads của context-B)["all"]` | dev số chính có đoạn đúng, n = 32 | **quyết** | tốt hơn = CI 95% của chênh > 0 (sau Holm trong nhóm) |
| mất đoạn đúng | số câu baseline `ctxB_gold_all` = 1 mà biến thể = 0 | n = 32 | **sàn** | 0 câu |
| `ctxB_gold_frac` | `gold_coverage(...)["frac"]` | n = 32 | theo dõi | — |
| `top10_gold_all`, `pool_union_gold_all` | như G1 | n = 32 | theo dõi (tầng lỗi) | — |
| `ctx5_gold_all` — 5 đoạn theo số đoạn, như runtime | context builder production, id từ `packed.sources` | n = 32 | theo dõi | — |
| keyword coverage trong context-B | `score_retrieval(keywords, texts của context-B)` | dev số chính trong kho, n = 88 | mức tụt cho phép | trung bình không tụt quá −0,02 (cận dưới CI); báo số câu tụt |
| MRR@10 / nDCG@10 keyword | như G1 | n = 88 | theo dõi | **không** dùng để quyết, vì đổi đơn vị đoạn làm thay đổi ý nghĩa thứ hạng |
| số đoạn, token p50/p90/max, số câu có đoạn hạng 1 > B | thống kê chunk + context | — | theo dõi | — |
| latency retrieval p95 (CPU) | `total_ms` như harness G4 | n = 88 | theo dõi | — |

Luật giữ / gỡ (skill §4): **tốt hơn** cần đủ ba điều:
1. không vi phạm sàn;
2. keyword coverage không tụt quá mức;
3. `ctxB_gold_all` có CI > 0 sau Holm.

Còn lại phân loại như sau:
- **kém hơn** khi vi phạm sàn, hoặc cận trên CI của `ctxB_gold_all` < 0;
- **chưa rõ / không khác** trong các trường hợp khác.

**Cỡ mẫu (ghi trước):**
- Baseline `ctx5_gold_all` dev số chính = 13/32 (G1 §7: 0,406), nên tối đa **19 câu** có thể tốt lên.
- Muốn CI > 0 cần khoảng ≥ 4–5 thắng / 0 thua; Holm trên 4 cần nhiều hơn, khoảng ≥ 6.
- Trần riêng từng hướng:
  - **H1 ≤ 13 câu** (thực tế ít hơn nhiều, vì chỉ 61 đoạn đổi);
  - **H3 ≤ 7 câu**.

  ⇒ **H1 và H3 có thể chỉ ra "chưa rõ"** dù không làm hỏng gì. H2 và small-to-big chạm mọi câu.

## 3. Thí nghiệm (thứ tự theo spec: H1 → H3 → H2 → small-to-big → tiền tố → sửa nhỏ)

**Luật nối tiếp:**
- Mỗi bước so với **baseline** và với **base hiện hành**. Base hiện hành = chunker runtime, trừ khi một bước trước đó ra
  "tốt hơn".
- Ngoại lệ ghi trước: H3 và H2 **cần** bỏ giới hạn HuyDang 256 (gộp tới 384/512 token là không thể nếu còn kiểm tokenizer
  256). Vì vậy hai bước này dựng trên chunker H1 bất kể kết luận của H1, và so với cả baseline lẫn H1. Nhờ đó tách được phần
  của H1 khỏi phần của H3 / H2.

```yaml
- experiment_id: G3.H1_tokenizer_e5_only
  changed_variable: chunker chỉ kiểm giới hạn e5-small 512 (bỏ e5-base 512, HuyDang 256) — tham số production sẵn có
                    `build_candidate(embedding_models=[e5-small])`, không cần code chia đoạn mới
  expected: 8.398 đoạn (−61), 14 file đổi
  compare: baseline · Holm: 1
- experiment_id: G3.H3_table_row_groups
  base: H1
  changed_variable: đoạn dòng-bảng / mục-con bị tách (có phần header) gộp các dòng liền nhau của cùng bảng thành nhóm
                    ≤ 256 token e5 (đã gồm tiêu đề + heading + header lặp lại ở mỗi nhóm); điều kiện đi kèm giữ nguyên
  not_in_scope: câu văn hóa từng dòng, đoạn "tổng quan bảng" — đổi representation, cần quyết riêng (NOT RUN, có lý do)
  compare: baseline + H1 · Holm: 1
- experiment_id: G3.H2_merge_same_heading
  base: H1 (+ H3 nếu H3 "tốt hơn")
  changed_variable: gộp các đoạn liền nhau cùng (source, heading_path) theo thứ tự tới ngưỡng T token e5 (tính trên
                    search_text đã dựng lại); chỉ gộp các đoạn có CÙNG tập phần điều kiện (giữ luật điều kiện / phương án
                    loại trừ); không gộp qua heading khác
  variants: [T128, T256, T384, T512_leaf]   # T512 = "1 heading lá = 1 đoạn" khi lá vừa 512; lá lớn hơn thì gộp tham lam tới 512
  report_also: số lá vừa trọn 1 đoạn; số lần gộp bị chặn vì khác điều kiện
  compare: baseline + base hiện hành · Holm: 4
- experiment_id: G3.S2B_small_to_big
  base: index tốt nhất tới lúc đó (không build mới)
  changed_variable: sau khi tìm, mỗi đoạn trong top-10 được mở rộng bằng các đoạn anh em cùng heading lá (theo thứ tự trong
                    file), rồi xếp vào context-B; trùng đoạn thì bỏ
  compare: cùng index, không mở rộng · Holm: 1
- experiment_id: G3.P_title_prefix
  base: chunker tốt nhất tới lúc đó
  changed_variable: tiền tố trong search_text (đổi cả dense lẫn BM25): [đầy đủ = hiện tại, chỉ heading gần nhất, không tiền tố]
  variants: [P_nearest, P_none]   # "đầy đủ" chính là base
  compare: base · Holm: 2
- experiment_id: G3.S_small_fixes   # mỗi sửa một biến thể, dựng trên chunker runtime để đo riêng
  variants:
    S1_drop_inventory: bỏ 33 đoạn của performing_arts/performing-arts-entities-inventory.md (lọc theo source trong harness)
    S2_keep_fences: thêm đoạn cho 2 code fence bị parser bỏ (span lấy từ file nguồn, harness dựng evidence_part)
    S3_dedupe_3_pairs: bỏ đoạn sau của 3 cặp lặp body (giữ đoạn đầu)
  compare: baseline · Holm: 3
  note: >
    sửa nhỏ, có thể "không khác". Mục đích: kiểm không hỏng gì để đưa vào đề xuất 8.2 cùng chunker thắng. S1 còn đo số
    lần đoạn inventory lọt top-10 (7B: 3/158)
```

**Dừng sớm:**
- Một bước "kém hơn" vì vi phạm sàn thì không dùng làm base, nhưng vẫn ghi đủ số.
- 3 vòng sửa cùng một biến thể không đạt thì dừng (skill §4).
- Build lỗi thì ghi lỗi quan sát được, không thử lại hay fallback. Bước nào tốn quá 20 phút thì dừng, báo A.

## 4. 2×2 context và câu trả lời (chỉ cho biến thể "tốt hơn" ở §3)

- **Retrieval 2×2 (miễn phí):** {baseline, chunker thắng} × {context 5 đoạn, 10 đoạn} (đếm theo số đoạn, như runtime), đo
  `ctx_gold_all`. Mục đích: kiểm tương tác chunk × context (spec G3, C15 m3) trước khi kết luận.
- **Câu trả lời (paid, `gpt-6-luna`):** sinh 120 câu dev cho {chunker thắng × context 5} và {chunker thắng × context 10}.
  - Baseline dùng lượt **G2.0** (context 5) và **G2.1a** (context 10) của B17, nếu cùng Golden (`0f7dbf41b422`), cùng prompt,
    cùng model và cùng ngày. Không thỏa thì sinh lại baseline và ghi lý do.
  - Pilot 10 câu mỗi lượt trước khi chạy đủ.
  - Judge: Claude, cùng model với G2. Tiêu chí: dùng nguyên §2.1 của plan G2/G4 (chỉ số chính Completeness, guardrail
    out_of_scope / Accuracy / lỗi citation / USD).
- **Ước tiền:** 120 × (0,000136 + 0,00021) ≈ **0,042 USD**; pilot ≈ 0,004. Nếu "tốt hơn", xác nhận trên test 56 câu ×
  2 ≈ 0,02. **Cộng ≤ 0,07 USD**, trần G3 **0,10 USD**. Luật lượt của A: ước lại từ pilot; một lượt ≤ 0,05 USD.
- **Không có biến thể "tốt hơn"** thì §4 **NOT RUN** (0 USD), lý do: không có gì để đề xuất.

## 5. Thứ tự chạy (sau khi A ghi "duyệt bản sha …")

1. Sửa code (§6) + test nhỏ cho tham số mới. Mốc byte runtime `cefb2d1a…` vẫn phải khớp; pytest retrieval / ingestion
   liên quan không paid.
2. Mốc: chạy lại retrieval runtime trên dev bằng harness G3. Ghi B (§1), baseline `ctxB_gold_all`, `ctx5_gold_all` (phải
   khớp G1 / G4 trên cùng câu; lệch thì ghi từng câu như C23 m4).
3. Kiểm giả định từng biến thể bằng máy **trước khi build**: số đoạn đổi, số lá gộp, số lần gộp bị chặn vì khác điều kiện,
   trần câu có thể đổi. Ghi vào report.
4. Build → đo → xóa collection, theo thứ tự §3: H1 → H3 → H2 (4) → small-to-big → tiền tố (2) → S1–S3. Khoảng 12 build ×
   ~5 phút, cộng đo ≈ **1–1,5 giờ CPU**.
5. §4 nếu có biến thể thắng. Xác nhận trên test cho biến thể "tốt hơn".
6. Report `phase_8_1_g3_implementation.md`: bảng do script in ra; thông số từng lượt (cấu hình chunker, sha danh sách đoạn,
   số đoạn, B, collection, build record, sparse state sha, thời gian, lệnh, đường dẫn kết quả); 3–5 dòng lời thường. Sau
   đó C review chéo: B hoặc A (vì C làm).

## 6. Code sẽ sửa / thêm (khâu dính cần tách)

| File | Sửa | Mặc định |
|---|---|---|
| `backend/ingestion/full_corpus_pipeline.py` | `prepare_full_corpus_input(..., chunks=None)` và `build_candidate(..., chunks=None)`: khi có `chunks` thì dùng danh sách đó thay vì gọi `chunk_full_corpus`; sources / identity / sparse state tính từ chính danh sách đó | `None` = chunker production (hành vi cũ). Đã có sẵn `collection_name`, `sparse_state_path`, `record_path`, `embedding_models` |
| `backend/experiments/phase_8_1/g3_chunking.py` (mới) | biến đổi danh sách đoạn (H3, H2, tiền tố, S1–S3) dựng lại `search_text` bằng `build_representation_a_search_text`; `build` (gọi `build_candidate` với đích `hue_81_g3_*`); `run` (retrieval + context-B + context-5 lấy id từ `packed.sources` như `g4_rerank.packed_chunk_ids`, đoạn đúng, keyword); `compare` / `summary` dùng lại G1; `drop` (chỉ xóa tên bắt đầu `hue_81_g3_`, liệt kê trước / sau) | **Từ chối ghi đè** file kết quả trùng `--name` (C21 m3; như harness G4) |
| — | Không sửa chunker production, `settings.yaml`, `settings_loader.py`, retrieval runtime (retrieval đã nhận `collection_name` / `record_path` / `sparse_state_path`) | — |

Khâu còn dính, ghi cho G5 / 8.2 (không sửa ở G3):
- `_phase4_settings()` tự đọc settings bên trong prepare / build;
- `build_candidate` tự tạo client;
- `TOP_K` / `fused[:10]` là hằng;
- `run_retrieval_eval` gọi `load_settings` bên trong.

## 7. Quyền, giới hạn, rủi ro

- **Quyền** (spec §8): Qdrant chỉ tạo / ghi / xóa `hue_81_*`; file private ở `data/phase_8_1/`; paid chỉ `gpt-6-luna` trong
  trần G3 0,10 USD; không commit (A commit); không mở câu kín.
- **Rủi ro:**
  1. Đoạn to "tự thắng" keyword: chặn bằng context-B và luật chỉ quyết theo đoạn đúng.
  2. Gộp làm trộn điều kiện loại trừ: chặn bằng luật chỉ gộp khi cùng tập điều kiện, và đếm số lần bị chặn.
  3. Đo nhầm index: record riêng + `variant_config` trong record.
  4. Cỡ mẫu nhỏ (32 câu): ghi trước "chưa rõ" là kết quả có thể.
  5. Không giữ GPU (CPU đủ).
- **Đổi spec umbrella §4** ("không trộn sibling để lấp token"): H2 chỉ là thí nghiệm. Đưa vào runtime cần User duyệt ở 8.2.

## 8. Hợp đồng kiểm

- Người làm (C nếu A giao) nộp: report §5.6 + JSONL / meta từng lượt + danh sách collection trước / sau.
- Người kiểm (B hoặc A) chạy lại:
  - mốc byte;
  - `compare` từ JSONL;
  - một biến thể bất kỳ build lại từ đầu, kiểm sha danh sách đoạn và số đoạn giống báo cáo;
  - `drop` cuối cùng: Qdrant chỉ còn collection runtime.

## 9. Phụ lục A duyệt (25/10, sau review của B; ghi trước khi đo biến thể nào)

1. **Keyword coverage** dùng thang 0–100 (`score_retrieval` trả %). Ngưỡng mức tụt cho phép: **cận dưới CI 95% của chênh
   trung bình ≥ −2,0 điểm %**. Điều này thay cách hiểu (a) A ghi khi duyệt bản `e089243fb612` (−0,02).
2. **H3 và H2 quyết bằng phép so với H1** (base mà hai bước này dựng lên), để tách đóng góp riêng của từng bước. Holm: H3
   trên 1, H2 trên 4. Phép so với baseline vẫn báo đầy đủ. Muốn vào danh sách đề xuất 8.2 thì cũng phải **không vi phạm sàn
   so với baseline**.
3. **§4:** được dùng lại câu trả lời G2.0 / G2.1a làm baseline. Nhưng **điểm của baseline phải chấm lại cùng lượt judge mù**
   với câu trả lời G3 (judge dùng quota, 0 USD).
