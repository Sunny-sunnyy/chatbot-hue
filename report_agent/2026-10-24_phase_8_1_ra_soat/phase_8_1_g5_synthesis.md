# Phase 8.1 G5 — tổng hợp kết quả rà quyết định

Người viết: A (Claude Opus 5.5, terminal `hue-rag-c6`) · 14:05 25/10/2026 (`date`); bản 2 14:2x sau review B
(`phase_8_1_g5_review.md`: M1–M2, m1–m4) · Trạng thái: **review vòng 2 ready (B, `phase_8_1_g5_review.md` §5) — **User đóng 8.1 lúc 15:27 25/10**; G0.6 khóa 15:22** · Spec `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` §5 G5, §6.

Bảng kết luận từng quyết định: `phase_8_1_g5_decision_table_draft.md` (B19, cập nhật G3; A review 13:5x — đối chiếu số
G2.1a, G2.4, luna rerank, khử dấu, G3 với report gốc, khớp). File đó là **bảng chính thức của G5**; file này tóm lại,
kiểm tiêu chí nghiệm thu và đề xuất phạm vi 8.2.

## 1. Kết luận một đoạn

8.1 thử lại bằng số đo các quyết định cũ ở mọi khâu: chia đoạn (12 cách), tìm kiếm (cách trộn, pool, HNSW), từ khóa (4
cách tách từ, khử dấu, tham số), xếp hạng lại (2 model GPU + `gpt-6-luna`), sinh câu trả lời (context, thứ tự, 2 prompt,
mức suy luận, chính sách citation). Luật quyết ghi **trước** khi đo, so theo cặp, Holm, dev chọn / test xác nhận.
**Chỉ một phương án đủ chuẩn để thay:** đưa model **10 đoạn thay vì 5** (Completeness dev +0,26 [+0,08; +0,48], test
+0,27 [+0,02; +0,59]; 0 câu ngoài phạm vi bị trả lời; tiền ×1,5). Phần lớn quyết định cũ **đứng vững** (giữ). Lỗ hổng lớn
nhất phát hiện được: **câu hỏi không dấu** làm tìm kiếm gần như hỏng (đủ đoạn đúng trong 5 đoạn: 13/32 → 1/32 câu).

## 2. Tiêu chí nghiệm thu (spec §6)

| # | Tiêu chí | Trạng thái | Căn cứ |
|---|---|---|---|
| 1 | G0 xong: tự kiểm thống kê; tham số mặc định-như-cũ (byte); baseline tái lập; split / đoạn đúng / câu kín tồn tại và được duyệt | **PASS** — G0.1–G0.5 xong + review; G0.4 User duyệt mẫu bản 5 (15:15); **G0.6 khóa 15:22** (`phase_8_1_g0_6_baseline_lock.md`, manifest `9ea480d0d083`) | `phase_8_1_g0_*`; `phase_8_1_g0_4_sealed_review.md` §8–§10 |
| 2 | Mỗi thí nghiệm có tiêu chí ghi trước, kết quả theo cặp **(theo loại câu)**, kết luận; phương án "tốt hơn" xác nhận trên test | **PASS** — plan có sha duyệt trước khi đo (G1, G2/G4 `a4adfc8eedd9`, G3 `d89a919067ba`, G4K `d7e53186b364`); G2.1a xác nhận trên test 41 câu; **theo loại câu** bổ sung ở `phase_8_1_g5_by_category.md` (B, sha `1f630d9db100`; A chạy lại script, 51/51 dòng bảng khớp) | report G1–G4K + review; `phase_8_1_g5_by_category.md` |
| 3 | Mỗi dòng top 10 C11 có kết luận hoặc lý do NOT RUN | **PASS** | bảng G5 §1 |
| 4 | Runtime không đổi (retrieval 176 câu giống byte mốc); Qdrant chỉ còn collection runtime | **PASS tại 14:05** — mốc `cefb2d1a…` khớp ở cuối G3 (C29); `GET /collections` 14:05: chỉ `hue_full_corpus_7a2_e5_small_384`. Kiểm lại lần cuối khi đóng 8.1 | `phase_8_1_g3_implementation.md`; lệnh `curl` 14:05 |
| 5 | Tiền thật ≤ trần (0,5 USD cả 8.1); report ghi token + USD | **PASS** — cả 8.1: **0,1653 USD**. Theo session: B 0,1653 (G4 luna 0,0088 + G2 0,1565); C 0 (G3 §4 NOT RUN; G4K trong bộ nhớ); A 0 (sub-agent dùng quota); trước 25/10: 0 (`CURRENT_HANDOFF.md` kết phiên 24/10) | `phase_8_1_g2_implementation.md`, `phase_8_1_g4_implementation.md`, `phase_8_1_g3_implementation.md` |

**Lệch spec có User duyệt (25/10):** (1) G4-B pool 100 + GPU mỗi lượt 20–30 câu; (2) câu kín thêm dấu cho mọi câu (thay
"không dấu"), sửa đáp án 5 dòng (C25: 4; C26: dòng 6) + viết lại 3 câu `capability_only` (C26); (3) **Golden chính thức sửa `reference_answer` 10 câu** (spec §1 ghi
"Golden chính thức giữ nguyên") — User duyệt 12:20 vì đáp án lặp / thiếu làm judge chấm sai; G2 trở đi chấm bằng Golden mới
(md5 `0f7dbf41b422`), 10 câu đó không còn so trực tiếp với 7B Run 1; (4) thêm `sentencepiece` (A duyệt theo ủy quyền User).

**Đổi quy trình / bổ sung có lý do (A, không cần User duyệt riêng — ghi để minh bạch):** (5) G3 §10 B10 là thí nghiệm
**thêm sau khi thấy kết quả H2** (tiêu chí ghi trước khi đo B10; kết quả kém hơn); (6) luật tiền đổi giữa chừng (12:4x: so với
ước lại từ pilot, trần lượt 0,05 / B17 0,25) sau khi một lượt luna vượt 54% ước plan; (7) judge mỗi sub-agent 40 câu (7B: 10),
cùng cho mọi biến thể; (8) `hue_81_g3_h1` build trước khi A duyệt §9 (chưa đo); (9) tiêu chí "theo loại câu" bổ sung sau ở
`phase_8_1_g5_by_category.md` (tiêu chí 2).

## 3. Kết quả theo khâu (chi tiết: bảng G5)

| Khâu | Đã thử | Kết luận |
|---|---|---|
| Chia đoạn (G3) | bỏ ràng buộc tokenizer cũ; gộp dòng bảng; gộp cùng mục 128–512; small-to-big; tiền tố tiêu đề; 3 sửa nhỏ; đoạn to ở ngân sách context 10 | **giữ**; 4 sửa dọn (H1, S1–S3) không khác → đưa vào lần build lại 8.2 |
| Tìm kiếm (G1, G4) | 10 cách trộn; pool 30/100; HNSW vs exact | **giữ**; pool rộng là tín hiệu (+4/−1 câu, chưa rõ) |
| Từ khóa (G4K) | cặp âm tiết, nguyên cụm mã, `pyvi`, khử dấu, k RRF, b BM25 | **giữ**; khử dấu cứu mạnh câu không dấu ở tầng tìm (sparse@100 0,25→0,81) nhưng hại câu có dấu |
| Xếp hạng lại (G4) | `bge-reranker-v2-m3`, `Vietnamese_Reranker` (GPU), `gpt-6-luna` listwise; top-10 và pool 100 | **giữ không rerank**; M1/M2 kém hơn; luna MRR +0,17 (chưa rõ ở chỉ số chính) |
| Sinh câu trả lời (G2) | context 10; thứ tự theo tài liệu; 2 prompt; reasoning effort none/low/high; chính sách citation | **thay context 5 → 10**; còn lại giữ (P1 bớt từ chối nhầm 13→1 nhưng phạm sàn 2 câu ngoài phạm vi) |
| Theo loại câu (G5) | bảng chỉ số quyết theo direct / multi / conditional / comparative / OOS | context 10 lợi chủ yếu ở **nhiều nguồn** (dev +0,71, 3/11/0) và **so sánh** (dev +0,64; test +0,83, n 6 — mô tả); trực tiếp 1/42/1. Đoạn to (H2 512 / B10) mất câu chủ yếu ở nhiều nguồn. 32 câu có đoạn đúng gần như toàn câu khó ⇒ chỉ số đoạn đúng không nói gì về câu trực tiếp |
| Thước đo (G0) | so theo cặp + Holm; 120 dev / 56 test; đoạn đúng 55 câu; độ tự nhiên; câu kín | **đã sửa**; còn thiếu mốc người |

## 4. Đề xuất phạm vi 8.2 (A xếp thứ tự; User quyết khi brainstorm 8.2)

Thứ tự theo lợi đã đo / chi phí / rủi ro. Mỗi mục vẫn qua skill `run-experiment` ở 8.2 (đo lại trên runtime mới).

0. **Điều kiện trước (bước 0 của 8.2):** (a) **mốc người ~20 câu** (D6) — mục 1 và 6 chỉ có bằng chứng từ điểm judge Claude,
   nên chỉ vào runtime **sau** khi có mốc người; (b) **tách khâu dính** (bảng G5 §4) trước khi thêm cải tiến vào code.
1. **Context 10 đoạn** — bằng chứng mạnh nhất; đổi một tham số settings. Rủi ro thấp.
2. **NFC câu hỏi** — một dòng; phục hồi hoàn toàn câu NFD (G1.4).
3. ~~Câu không dấu~~ — **User 15:15 25/10 bỏ khỏi phạm vi:** "cứ thiết kế có dấu hết, người dùng hỏi cũng viết có
   dấu"; không nghiên cứu thêm. Số đo G1.4 / G4K giữ làm hồ sơ (giới hạn đã biết của chatbot).
4. **Dọn chunker khi build lại index** (H1 + S1–S3) — **không có lợi đo được** (không khác), lập luận bằng vệ sinh / bớt
   ràng buộc cũ; không đứng riêng — gộp vào lần build của mục 3 hoặc 8, kèm sửa mâu thuẫn kho (Hải Vân).
5. **Pool rộng + rerank luna** — tín hiệu, đo lại cùng context 10.
6. **H8 trả lời một phần có chặn câu ngoài phạm vi** — bớt từ chối nhầm; đổi hợp đồng spec Phase 6 §10.
7. **Lỗi citation ở bước sinh** (thiếu `[n]`, validator không chạm tới) — thiết kế cách sửa rồi đo.
8. **Index Qwen3-Embedding-8B** — spec đã để 8.2; cần cách gọi chịu 504/429.
9. **Mở câu kín** ở mốc cuối 8.2 (User quyết).

## 5. Việc để đóng 8.1

1. User xem mẫu câu kín bản 5 (`knowledge-base-hue/evaluation/phase_8_1/sealed_user_sample.md`, 8 dòng `[ĐỔI]`).
2. A khóa câu kín (file chính thức 4 field) + G0.6 baseline (commit, hash corpus / build record / split / gold / realism /
   sealed / Golden, mốc retrieval 2 cách trộn).
3. Kiểm cuối: mốc byte runtime + `GET /collections`.
4. Báo cáo cho User (`bao_cao_he_thong/`: B20 review ready bởi C; C30 review ready bởi B — sửa minor chữ; phần của A xong) + `TONG_HOP.md` (đóng khi User đóng 8.1).
5. User đóng 8.1 → A brainstorm + spec 8.2.

## 6. Giới hạn

- Bộ thử nhỏ (32 câu dev có đoạn đúng; test 10–15 câu) ⇒ nhiều kết luận "chưa rõ" là do trần số câu, đã ghi trước.
- Judge là Claude, chưa có mốc người; nhiễu judge-only 2/88 câu, nhiễu cả đường 10/83.
- Câu không dấu / NFD là biến đổi máy. 15 câu test có đoạn đúng đã nhìn ở G1.6. Câu kín chưa dùng.
- **Bám nguồn chưa có số ở 8.1** (7B.2): chỉ số phụ "claim không nguồn" của plan G2.2 NOT RUN (`phase_8_1_g2_implementation.md` §6).
- A đã thấy nội dung 3 câu kín (User trích khi hỏi) — không đề xuất biến thể nhắm vào chúng.
