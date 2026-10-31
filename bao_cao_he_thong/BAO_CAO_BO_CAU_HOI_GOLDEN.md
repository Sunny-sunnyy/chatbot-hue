# Báo cáo cho bạn: Bộ câu hỏi chuẩn Golden (Phase 7A, 8.1, sửa kho đợt 1–2)

**Cập nhật lần cuối: 17:19 31/10/2026 — bản 7: rà lại cho đúng hiện trạng, xoá phần không còn đúng (User 31/10); chạy lại kiểm Golden sau 2 đợt sửa kho: 1 câu lệch kho.**
Các bản trước: xem `git log` file này. Người viết: agent con của A (bản 7) · Review: agent con ngữ cảnh mới (31/10). Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (luôn đúng hiện trạng)

- **Khâu này làm gì:** giữ "đề thi" để chấm chatbot. **Golden** là bộ 176 câu hỏi phủ cả 5 mảng của kho (món ăn, di tích, lễ hội,
  nghệ thuật biểu diễn, du lịch), kèm **bộ thử nhanh** 10 câu lấy nguyên từ 176 câu đó. Mỗi câu có 4 phần: câu hỏi viết như người thật hỏi,
  đáp án tham chiếu ngắn, keyword (từ khoá chép nguyên văn từ kho, để chấm bước tìm đoạn) và loại câu. Các lần đo từ Phase 7B tới nay
  (8.1, 8.2, hai đợt sửa kho, thử Qwen3-8B) đều chấm trên đề này — riêng lần chấm cuối 8.2 dùng bộ câu kín.
- **Hiện trạng (31/10):** file private `knowledge-base-hue/evaluation/golden_full_corpus.jsonl`, 176 câu, mã kiểm tra file (md5)
  **`6331e88fb171`** từ 30/10. Đi kèm, cũng private:
  - chia **120 câu thử / 56 câu kiểm** (thử để tìm hướng, kiểm để xác nhận — không dùng nhóm kiểm để chọn);
  - **nhãn đoạn đúng** (vị trí trong file nguồn chứa câu trả lời) cho 55 câu khó, **bản 5** (theo kho sau đợt 2, 30/10);
  - **nhãn độ tự nhiên**: 82 câu tự nhiên / 65 câu chỉ đo năng lực / 29 câu không tự nhiên — số chính của mọi thí nghiệm bỏ 29 câu không tự nhiên.
- **Đo được:** 176 câu = một dữ kiện 75, nhiều nguồn 29, có điều kiện 29, so sánh 25, ngoài kho 18; 100 % câu đã đối chiếu với file nguồn
  (23/10). Dùng thật ở 7B: chấm hai lần chênh ≤ 0,011 điểm ⇒ thước đo ổn định.
- **Bộ 36 câu kín** (viết kiểu người dùng thật, khoá 25/10) **đã dùng** ở lần chấm cuối Phase 8.2 (28/10) ⇒ từ đó chỉ còn là bộ kiểm hồi quy,
  **không còn bộ kiểm "chưa ai thấy"**.
- **Sau mỗi đợt sửa kho, đề được quét lại** xem đáp án còn khớp kho không: đợt 1 (28/10) 0 câu cần sửa; đợt 2 (30/10) sửa đáp án tham chiếu
  của 2 câu theo bạn chọn. Chạy lại kiểm định dạng 31/10 vẫn bắt thêm **1 câu** có keyword không còn nguyên văn trong kho mà
  3 lớp quét sót — chờ bạn duyệt sửa (§6).
- **Giới hạn chính:** câu do AI viết rồi người duyệt, không phải câu người dùng thật hỏi; keyword chỉ là thước gần đúng ("proxy"); giá vé, giờ
  mở cửa lấy mốc 09/2026; đoạn đúng mới có cho 55 / 176 câu; 121 / 176 câu đã đạt điểm tối đa ở mốc 7B (cải tiến chủ yếu thấy ở số còn lại).
- **Chi phí:** kiểm định dạng và quét lại đề 0 USD.
- **Bạn cần quyết gì:** duyệt sửa **1 câu Golden lệch kho** (keyword / đáp án mẫu theo kho mới; §6). Trước buổi bảo vệ cần một bộ câu kín mới (đã ghi vào bước đóng gói Phase 1–8, §6).

## 2. Hoạt động thế nào (bản đang chạy)

```text
Làm đề (Phase 7A, 23/10):
đọc file .md của kho → viết thử 20 câu → bạn chỉnh văn phong → agent con viết các nhóm còn lại
 → máy kiểm định dạng + keyword có nguyên văn trong kho → người kiểm đối chiếu từng câu với kho
 → bạn đọc mẫu → sửa → gộp thành 1 file (nối các nhóm theo thứ tự cố định, không xáo) + chọn tay 10 câu thử nhanh

Chấm (từ Phase 7B):
176 câu → chatbot thật trả lời → chấm bước tìm đoạn (keyword, đoạn đúng) + Claude chấm câu trả lời (Đúng / Đủ / Trúng ý)

Sau mỗi đợt sửa kho:
quét đề 3 lớp (theo chữ cũ quanh chỗ sửa · theo cụm chữ bị bỏ · theo vị trí đoạn bị sửa) → agent đọc từng câu bị chạm
 → người khác kiểm → bạn chọn cách sửa → sao lưu bản cũ → sửa đúng cụm chữ; nhãn đoạn đúng dựng lại theo kho mới
```

Năm loại câu: một dữ kiện (`direct_fact`), nhiều nguồn (`multi_source`), có điều kiện (`conditional`), so sánh (`comparative`), ngoài kho
(`out_of_scope`, đáp án đúng là từ chối).

Code: `backend/evaluation/golden_full_corpus.py` (lệnh `check` kiểm định dạng + keyword nguyên văn; `merge` gộp các nhóm). Tự kiểm (không tốn phí),
từ `backend/`:

```bash
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus.jsonl
```

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Câu một dữ kiện | **Đã xử lý, đóng gói** | 75 câu |
| Câu nhiều nguồn | **Đã xử lý, đóng gói** | 29 câu |
| Câu có điều kiện | **Đã xử lý, đóng gói** | 29 câu |
| Câu so sánh | **Đã xử lý, đóng gói** | 25 câu |
| Câu ngoài kho (đáp án đúng là từ chối) | **Đã xử lý, đóng gói** | 18 câu |
| Kiểm định dạng + keyword nguyên văn trong kho | **Xử lý một phần** | `golden_full_corpus.py:24` (4 phần), `:80–82` (keyword nguyên văn); test 8 / 8 đạt (31/10). **Chạy lại `check` trên Golden 17:17 31/10/2026** (A, sau 2 đợt sửa kho): 176 câu đọc được, **1 lỗi** — 1 câu có một keyword không còn nguyên văn trong kho (kho đổi chữ ở đoạn nguồn); chấm keyword của câu đó lệch, phần còn lại không đổi. Sửa Golden cần bạn duyệt |
| Đối chiếu dữ kiện từng câu với kho | **Đã xử lý, đóng gói** | 100 % câu (23/10); 4 câu xoá, 10 câu sửa |
| Đáp án lệch kho sau mỗi đợt sửa kho | **Xử lý một phần** | đợt 1: 59 câu bị chạm ⇒ 0 sửa; đợt 2: 39 câu ⇒ 2 câu sửa đáp án (bạn chọn); bộ thử nhanh không chứa 2 câu này; **31/10 chạy lại `check`: 1 câu còn keyword không khớp kho — chờ bạn duyệt** |
| Bộ thử nhanh 10 câu | **Đã xử lý, đóng gói** | 10 / 10 câu trùng khớp file chuẩn |
| Giá vé, giờ mở cửa còn đúng | **Xử lý một phần** | lấy mốc 09/2026, có thể cũ |
| Tách nhóm thử / nhóm kiểm | **Đã xử lý, đóng gói** | 120 / 56, chia theo loại câu, cách chia cố định |
| Đoạn đúng cho câu khó | **Xử lý một phần** | 55 câu (40 thử / 15 kiểm); bản 5 (30/10) là bản code đo đang dùng |
| Nhãn độ tự nhiên | **Đã xử lý** | 82 / 65 / 29; số chính bỏ 29 câu không tự nhiên |
| Đáp án tham chiếu chỉ trả lời điều được hỏi | **Đã xử lý** | sửa 10 câu (25/10); 5 câu "chưa chắc" giữ nguyên |
| Bộ câu kín cho chấm cuối | **Đã xử lý** (đã dùng 28/10) | 36 câu, đủ dấu, 36 / 36 tự nhiên; nay là bộ hồi quy; bộ kín mới: **chưa thực hiện** |
| Câu người dùng thật hỏi | **Chưa thực hiện** | đề do AI viết, người duyệt; câu kín viết theo kiểu người dùng thật nhưng vẫn do AI soạn |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Lịch sử các lần đổi đề / nhãn (mới ở trên)

- **30/10 — sửa kho đợt 2:** quét 39 câu bị chạm (thêm lớp "cụm chữ bị bỏ" vì lớp theo chữ cũ sót 2 câu) ⇒ sửa đúng một cụm chữ ở đáp án tham
  chiếu của 2 câu (một câu bỏ tên phường cũ kho đã bỏ; một câu thêm chữ "khoảng" như kho nay ghi); câu hỏi, keyword, loại câu giữ nguyên; có sao lưu.
  md5 `0f7dbf41b422` ⇒ `6331e88fb171`. Nhãn đoạn đúng bản 4 ⇒ bản 5 (1 trích dẫn bị chỗ sửa chồng, bạn duyệt). Điểm 2 câu này trước 30/10 không so
  trực tiếp được. PASS · 0 USD.
- **28/10 — sửa kho đợt 1:** quét 59 câu ⇒ 0 câu cần sửa (bạn duyệt); nhãn đoạn đúng bản 3 ⇒ bản 4 (2 trích dẫn đổi chữ, bạn duyệt). PASS · 0 USD.
- **27/10 — nhãn đoạn đúng bản 2, bản 3:** sửa khoảng trích dẫn ở vài câu và thêm luật đếm dòng tiêu đề (bản 2, bạn duyệt); sửa nhãn 3 câu nhóm kiểm
  (bản 3). Kết luận cũ không đổi. 0 USD.
- **25/10 — Phase 8.1:** sửa đáp án tham chiếu 10 câu theo nguyên tắc bạn duyệt (đáp án chỉ trả lời điều được hỏi; chỉ thêm điều kiện khi thiếu
  nó thì sai; chi tiết phụ đúng nguồn thì giữ) — điểm 7B của 10 câu này không so trực tiếp được; md5 ⇒ `0f7dbf41b422`. Bộ 36 câu kín: thêm dấu,
  sửa đáp án lặp chủ ngữ, đổi 3 câu "chỉ đo năng lực" thành câu người dùng hay hỏi; bạn duyệt mẫu ⇒ khoá chiều 25/10. PASS · 0 USD.
- **24/10 — Phase 8.1:** chia 120 thử / 56 kiểm; gắn đoạn đúng cho 55 câu khó (agent gắn, agent khác kiểm 55 / 55, bạn xem mẫu); nhãn độ tự nhiên
  (2 agent gắn độc lập, đồng ý cao — kappa 0,765; 9 câu bất đồng bạn giữ là tự nhiên). PASS · 0 USD.
- **24/10 — dùng thật ở 7B và dọn code cũ:** 176 câu chạy đủ, chấm hai lần chênh ≤ 0,011; gỡ bộ chấm món ăn của Phase 7, đề vẫn đạt `check`.
- **23/10 — đóng Phase 7A:** 176 câu đủ 5 loại; 100 % kiểm với file nguồn, 4 câu xoá, 10 câu sửa; phát hiện 53 mục mâu thuẫn trong kho gốc
  (21 mục đủ căn cứ sửa ⇒ dẫn tới Phase 7A2 sửa kho).
- **24/08 — Phase 7 (lịch sử):** chấm thử bộ món ăn 104 câu (tìm đoạn MRR 0,83; Đúng / Đủ / Trúng ý 4,37 / 4,02 / 4,19); không so trực tiếp với số
  toàn kho; code chấm đó đã thay ở 7B.

## 5. Hôm nay còn đúng không

Kiểm 31/10/2026 với code (commit `1985a81`) và `session_prompt/Project_Status.md` §4.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Golden 176 câu + thử nhanh 10, mỗi câu 4 phần (`question`, `keywords`, `reference_answer`, `category`) | **còn dùng** | `backend/evaluation/golden_full_corpus.py:24`; `backend/evaluation/full_corpus_eval.py:41–42` |
| 5 loại câu (gồm ngoài kho) | **còn dùng** | `golden_full_corpus.py:13` |
| File soạn theo nhóm (`*/evaluation/golden_full_corpus_authoring.jsonl`), gộp theo thứ tự cố định | **còn dùng** cho `check` / `merge` | `golden_full_corpus.py:26`, `:110–119` |
| Thước đo: tìm đoạn (MRR@10, nDCG@10, Keyword Coverage@10) + Đúng / Đủ / Trúng ý 1–5, trung bình theo câu | **còn dùng** | `full_corpus_eval.py` |
| Người chấm câu trả lời | **Claude chính**, `gpt-6-luna` chấm phụ để so (7B, bạn chọn) | `BAO_CAO_DANH_GIA.md` |
| Chia đề 120 thử / 56 kiểm | **còn dùng** | `knowledge-base-hue/evaluation/phase_8_1/split.json` (private) |
| Số chính bỏ 29 câu không tự nhiên | **còn dùng** | `data/phase_8_1/golden_realism_final.jsonl` (private) |
| Golden md5 `6331e88fb171` | **còn dùng** (từ 30/10); bản trước sao lưu | `knowledge-base-hue/meta/golden_backup_dot2_2026-10-30/` (private) |
| Nhãn đoạn đúng bản 5 | **còn dùng** (từ 30/10) | `data/phase_8_1/gold/gold_v5.jsonl` (private) |
| Bộ 36 câu kín là bộ "chưa ai thấy" | **đã thay** 28/10: đã dùng ở lần chấm cuối 8.2 ⇒ bộ hồi quy | `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md` |
| Bộ chấm món ăn Phase 7 và notebook 07 | **đã gỡ** (24/10), thay bởi `full_corpus_eval.py` | commit `1832201` |

## 6. Việc còn lại / cần quyết

- **Bộ câu kín mới** trước buổi bảo vệ (để có một mốc trung thực): đã ghi vào bước đóng gói Phase 1–8; chưa làm.
- **Sửa 1 câu Golden có keyword không còn nguyên văn trong kho** (phát hiện 17:17 31/10/2026 khi chạy lại `check` sau 2 đợt sửa kho): cần bạn duyệt sửa keyword / đáp án mẫu theo kho mới (như 30/10 đã sửa 2 đáp án); 0 USD.
- Sau mỗi đợt sửa kho sau này: quét lại đề đủ 3 lớp như 30/10 (lớp "cụm chữ bị bỏ" bắt buộc) **và** chạy `golden_full_corpus check` (miễn phí,
  vài giây) — 31/10 lệnh này bắt 1 câu mà 3 lớp quét sót.
- Đề xuất chưa làm: gắn thêm đoạn đúng cho câu nhóm thử (hiện ít câu thuộc số chính có đoạn đúng, nên nhiều kết quả tầng tìm chỉ "chưa rõ").
- Giới hạn nên nhớ khi đọc số: keyword là "proxy" (đoạn chứa keyword chưa chắc đủ ý; đoạn đúng diễn đạt khác thì bị tính trượt).

## Phụ lục — hồ sơ kỹ thuật

- **Mã file (private):** Golden md5 `6331e88fb171` (30/10; trước `0f7dbf41b422` 25/10; bản 7A `c30b56f22bd3`); thử nhanh md5 `d80b58c50f38`;
  nhãn đoạn đúng bản 5 sha256 `33d16fd6b8f4`; `split.json` `e2b1788dfbbc`; nhãn độ tự nhiên `0b65d1c138d2`; câu kín chính thức
  `sealed_official.jsonl` md5 `ddc59587b502` (bản soạn v6 `631334704fdd`; mẫu cho bạn bản 5 `4f7fe6df5cca`); manifest khoá mốc 8.1 (G0.6) `9ea480d0d083`.
- **Báo cáo đợt:** spec 7A `docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md` (`:32`, `:138`: nối theo nhóm, không xáo);
  8.1 `report_agent/2026-10-24_phase_8_1_ra_soat/` — `phase_8_1_g0_1_2_measure_implementation.md` (chia nhóm), `phase_8_1_g0_3_gold_review.md`
  (đoạn đúng), `phase_8_1_g0_4_sealed_review.md` (câu kín), `phase_8_1_golden_fix_review.md` (sửa 10 đáp án), `phase_8_1_g0_6_baseline_lock.md` (khoá);
  câu kín dùng ở 8.2 (B3, 36 câu): `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md`; nhãn bản 2 / 3: `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`,
  `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md`; sửa kho đợt 1 `sua_kho_b7_8_implementation.md`, đợt 2 `sua_kho_dot2_implementation.md`
  §1 bước 7–8 (cùng thư mục `report_agent/2026-10-27_phan_ton_phase_cu/`; hồ sơ quét private `data/sua_kho_2026-10-27/dot2/`).
- **Lịch sử Phase 7:** danh sách dọn `reports/phase_7_cleanup_inventory_2026_10_24.md`; giả thuyết Phase 8 `reports/phase_8_candidate_hypotheses_2026_10_24.md`.
- Guide `guides/full_corpus_rag.md` phần Golden cũ (bullet trước 7A) có ghi chú "supersede" ở đầu mục (`:285–290`) — không sai nhưng đọc nhanh dễ nhầm.
