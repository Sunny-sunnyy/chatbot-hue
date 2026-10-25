# Review: Phase 8.1 G3 — biến thể chia đoạn (C29)

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 2 minor — sửa chữ, không cần chạy lại)
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-3f`) · 2026-10-25 (`date` khi viết: sau 13:56)
Report được kiểm: `phase_8_1_g3_implementation.md` sha `abc9cb72d1a0` · Plan: `phase_8_1_g3_plan.md` (§1–§9 bản
`9f00c460c3e9`, §10 bản `d89a919067ba`) · Skill `risk-gated-agent-review`. Review không chép corpus / câu hỏi / đoạn trích.

## 1. Cổng tối thiểu

| Kiểm | Kết quả |
|---|---|
| Git | HEAD `0c19756`; thay đổi của C: `backend/ingestion/full_corpus_pipeline.py` (M), `backend/experiments/phase_8_1/g3_chunking.py` (mới), report G3 (mới), `STATUS_C.md` — khớp report §1 |
| Diff production | `prepare_full_corpus_input(..., chunks=None)` / `build_candidate(..., chunks=None)`: chỉ bỏ qua `chunk_full_corpus` khi có `chunks`; mặc định giữ nguyên đường cũ (kể cả raise khi chunker lỗi). Đúng plan §6, tham số mặc định = hành vi đang chạy |
| Ngoài phạm vi | không thấy: không sửa chunker, settings, loader, retrieval runtime |
| `git diff --check` | sạch |
| Qdrant | `GET /collections` (B, lúc review): chỉ `hue_full_corpus_7a2_e5_small_384` |

## 2. B chạy lại độc lập (0 USD, chỉ đọc)

| Kiểm | Kết quả |
|---|---|
| Mốc byte runtime với working tree hiện tại (đã có sửa `full_corpus_pipeline.py`) | `cefb2d1a…` — **PASS** |
| `stats --variant h1-h2_512` | 2.643 đoạn, sha `908f09f17c3d`, 7 lần gộp bị chặn vì khác điều kiện — **khớp** §2 / §4 |
| `stats --variant h1-h3` | 8.359 đoạn, sha `8a2d81769689` — **khớp** |
| `compare` H2 128/256/384/512 vs H1 (Holm 4) | 0/32/0 · 0/28/4 (p 0,091) · 1/25/6 (0,135) · 0/26/6 (0,018) — **khớp** §3.3 |
| `compare` H3 vs H1 | 0/32/0; keyword −0,284 [−0,852; 0] — **khớp** §3.2 |
| `compare` small-to-big vs base | 0/24/8 [−0,406; −0,125] — **khớp** §3.4 |
| `compare` tiền tố vs base | p_nearest 4/21/7 (0,457), p_none 3/21/8 (0,317) — **khớp** §3.5 |
| `compare` B10: H2 384 / 512 vs H1 (Holm 2) | 1/25/6 (0,062), 0/26/6 (0,009); keyword −2,18 / −2,56 — **khớp** §3.7 |

Không build lại collection (C đã build 11 lần với sha danh sách đoạn trong record; `stats` tính lại sha là đủ chứng minh
cùng đầu vào — plan §8 cho phép). Không chạy lại pytest ingestion (test này import đường upsert; dùng lại bằng chứng của C:
41 passed, cùng diff).

## 3. Đọc code theo điểm C nhờ soi

- **Luật gộp H2** (`merge_same_heading`): chỉ gộp đoạn **liền nhau** cùng `(source, heading_path)` và cùng `condition_key`
  (tập (start, end) của phần `condition`); khác điều kiện thì đếm `blocked_by_condition` và mở đoạn mới; phần trùng
  `(role, start, end)` (nhãn cha, điều kiện) bỏ, nên không lặp; dừng khi `search_text` dựng lại vượt T token e5 (đếm như
  checker chunker, prefix `passage: `). Đúng plan §3 + luật "chỉ gộp cùng tập điều kiện".
- **Ngân sách** (`budget_context` / `block_tokens`): token `o200k_base` của `_block(_source(doc, 1))` — đúng khối builder
  đưa model; bỏ đoạn không bằng chứng như builder; dừng ở đoạn đầu tiên làm vượt (không nhảy qua lấy đoạn nhỏ hơn); đoạn
  hạng 1 vượt vẫn lấy và đếm riêng. Đúng plan §1 + §9.
- **B10** (`budget10`, `rebudget`): B10 tính trên `ctx10_chunk_ids` của `base.jsonl` (88 câu) trước biến thể; `rebudget`
  dựng lại payload bằng `make_chunks` và **từ chối** nếu sha khác lúc build; cổng 750 đã chạy 0 lệch (report §3.7). Đúng §10.
- **Tiền tố** (§3.5): keyword / MRR chấm trên `search_text` mà biến thể đã đổi ⇒ lệch theo cách đo; C đã ghi và chỉ quyết
  bằng đoạn đúng (offset). Đồng ý.

## 4. Findings

- **m1 (minor) — ngân sách là xấp xỉ token context thật.** `block_tokens` đếm từng khối với `id = 1` và không cộng dấu
  ngăn `\n\n` giữa các khối, cũng không gồm câu hỏi / system prompt. Áp như nhau cho baseline và mọi biến thể nên **không
  đổi kết luận**; nhưng "B = 750 token" không phải số token prompt thật. **Đóng khi:** §3.9 thêm một dòng nói B là tổng
  token các khối bằng chứng (xấp xỉ), không phải token prompt.
- **m2 (minor) — keyword trong context-B tính trên `search_text`, không trên phần bằng chứng model thấy.** Với đoạn gộp,
  `search_text` dài hơn nên keyword có thể tăng "miễn phí" (bẫy đoạn to); ở đây keyword chỉ là mức tụt cho phép và mọi H2
  đã kém hơn theo đoạn đúng, nên không ảnh hưởng. **Đóng khi:** §3.9 ghi giới hạn này cạnh dòng tiền tố (cùng nguyên nhân).

Ghi nhận khác (không phải finding):
- H1 "không khác" nhưng keyword context-B có cận dưới −3,41 (1 câu tụt, 1 câu tăng): đúng luật plan (keyword chỉ chặn
  "tốt hơn"). Khi đề xuất "bỏ ràng buộc HuyDang" ở 8.2 nên nhắc 1 câu tụt keyword này.
- Collection `hue_81_g3_h1` build trước khi A duyệt §9 (report §2 ghi minh bạch, chưa đo gì, A chấp nhận) — không phải
  vi phạm vì chưa có số đo nào trước duyệt.
- Mức đơn giản: harness 587 dòng cho 12 biến thể + B10; mỗi biến đổi là một hàm nhỏ gọi tên được; dùng lại G1/G4. Phù hợp.

## 5. Kết luận

Kết luận của C theo luật ghi trước đứng vững: **không biến thể chia đoạn nào "tốt hơn"**; H2 256/384/512, small-to-big,
tiền tố, B10 **kém hơn** (vi phạm sàn); H1, H3, H2 128, S1–S3 không khác; §4 và test NOT RUN đúng plan.

## 6. Kiểm lại phần sửa (report sha `834342d24899`)

- m1: §3.9 ghi B / B10 chỉ đếm token các khối bằng chứng, xấp xỉ, áp đều mọi biến thể — **đóng**.
- m2: §3.9 ghi keyword context-B chấm trên `search_text` nên hơi thiên về đoạn gộp, kết luận dựa trên đoạn đúng — **đóng**.
- Thêm dòng nhắc "H1 có 1 câu tụt keyword" cho đề xuất bỏ HuyDang ở 8.2 — đúng ghi nhận ở §4.

Kết luận giữ nguyên: **ready_for_user_confirmation**, không còn finding mở.
