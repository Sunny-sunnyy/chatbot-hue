# Phase 8.2 — Áp dụng phương án thắng 8.1 và thử tín hiệu trên chatbot mới

**Status:** `draft` — bản 3 (A, terminal `hue-rag-00`; bản 1 `2c8d40e3aa4c` → bản 2 `f5fd17418c41` sửa theo review B22
`report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_spec_review.md` M1–M4, m1–m5 → bản 3 sửa N1, m6, m7 của vòng 2); chờ B kiểm phần đổi rồi User duyệt một lần (sha) ·
Đợt: `report_agent/2026-10-25_phase_8_2_ap_dung/` (mở 16:05 25/10 khi User chọn phạm vi)

## Căn cứ để review

1. File này — toàn bộ.
2. `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g5_synthesis.md` §3–§4, §6 (kết luận 8.1, đề xuất 8.2, giới hạn).
3. `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g5_decision_table_draft.md` §1 dòng 2a, 2b, 6, 8 và §3 (số đo dùng
   làm căn cứ).
4. `skills/run-experiment/SKILL.md` §1, §3, §4 (luật tiêu chí ghi trước, nhiễu, giữ / gỡ).

## 1. Mục tiêu

8.1 đo lại các quyết định Phase 0–7; chỉ **context 10 đoạn** đủ chuẩn để thay (Completeness dev +0,26 [+0,08; +0,48], test
+0,27 [+0,02; +0,59]). 8.2 **đưa phần đã chắc vào chatbot thật**, rồi **thử lại các tín hiệu** của 8.1 trên chatbot mới
(vì số đo cũ là ở context 5). Mỗi thay đổi vào chatbot phải qua luật ghi trước + review chéo.

## 2. Quyết định đã chốt (User, brainstorm 15:5x–16:0x 25/10)

| # | Quyết định | Cái giá |
|---|---|---|
| D1 | **Phạm vi hai bước, không build lại index:** Bước 1 context 10 + NFC vào chatbot; Bước 2 thử tín hiệu trên chatbot mới | Kho Hải Vân còn tự mâu thuẫn tới đợt build lại (giới hạn đã biết); dọn chunker, index 8B để đợt sau |
| D2 | **Mốc người = đọc cặp mù:** 15–20 câu, mỗi câu 2 câu trả lời X / Y (context 5 vs 10, xếp ngẫu nhiên); User nhận xét tự do, thấy rõ thì ghi bên nào hơn (không bắt buộc, không chấm điểm) | ~30–45 phút User |
| D3 | **Bước 2 thử cả ba, theo thứ tự:** E1 trả lời một phần có chặn câu ngoài phạm vi → E2 lỗi thiếu `[n]` → E3 pool rộng + rerank luna (có luật bỏ sớm; A tách E3a / E3b, mục 5) | 8.2 dài nhất; có thể kéo nhiều phiên |
| D4 | **Đưa vào chatbot:** A tự đưa khi qua luật ghi trước + review chéo đạt, báo User sau; **đổi quy ước trả lời (E1) vẫn chờ User duyệt**. Cho 8.2, D4 thay dòng "đưa vào runtime là việc riêng, User duyệt" của `run-experiment` §4 | Lỗ hổng luật mà người kiểm không thấy ⇒ chatbot đổi trước khi User biết (gỡ bằng revert một commit) |
| D5 | Trần tiền **0,5 USD cả 8.2** (mặc định A đặt, User không đổi), trong trần 1 USD / phiên | — |

## 3. Quyết định kỹ thuật của A (trong phạm vi, kèm lý do)

1. **Tách khâu dính chỉ ở chỗ thí nghiệm cần** (bảng G5 §4), không dọn tràn lan. Lý do: sửa code lớn chưa có nhu cầu đo được.
   Mỗi tham số mới mặc định = hành vi hiện tại (như 8.1).
2. **NFC ở một chỗ mọi đường đi qua** (API và evaluator đều gọi) — chỗ cụ thể chọn trong plan Bước 1 (evaluator đã có NFC riêng
   ở `full_corpus_eval.py:91`, `:132` và `golden_full_corpus.py:33` khi nạp Golden). Lý do: evaluator phải đo đúng cái người dùng nhận.
3. **Mốc người dùng câu trả lời 8.1 G2 đã sinh thật** (G2.0 context 5 vs G2.1a context 10, dev + test). Lý do: kiểm đúng điểm
   judge đã dùng để quyết context 10; không tốn tiền. Mẫu **20 câu** chọn bằng máy, seed ghi trước, trộn theo điểm judge: ~1/2 câu
   judge chấm 10 hơn, còn lại judge chấm như nhau hoặc 10 kém hơn; **không lấy câu kín**. Một sub-agent không thấy điểm judge xếp
   X / Y; A chỉ giữ khóa.
   **Giữ mù hình thức** (25/176 câu trả lời context 10 có citation `[6]`–`[10]`): mỗi câu trả lời đánh số lại citation theo thứ tự
   xuất hiện (1..k) và chỉ hiện các nguồn được trích. Kiểm bằng code trên file đưa User, ghi trong report B0: 0 câu trả lời có số
   citation > số nguồn hiện kèm. A đã đếm (16:1x): 0 / 176 câu trả lời context 10 trích > 5 nguồn khác nhau ⇒ đánh số lại đủ che.
4. **Luật dừng của mốc người** — chỉ số so: **Completeness** (chỉ số quyết context 10 ở 8.1), điểm judge trong
   `data/phase_8_1/g2/judge/` (dev) và `judge_test/` (test); "judge chấm khác nhau" = chênh Completeness ≠ 0.
   - **Cặp quyết** = cặp User ghi bên hơn **và** judge chấm khác nhau. Có **≥ 5 cặp quyết**: số cặp User ngược judge **nhiều hơn**
     số cặp cùng chiều ⇒ dừng, A xem lại judge với User trước Bước 2 (và trước khi giữ context 10). **< 5 cặp quyết ⇒ "chưa rõ"**
     ⇒ A trình User trước Bước 2, không tự cho qua.
   - **Cặp judge hòa** mà User ghi bên hơn: báo số; nếu chiếm ≥ 1/2 số cặp User ghi bên hơn ⇒ ghi "judge kém nhạy" vào giới hạn, báo User.
   - Nhận xét tự do tóm thành nhãn đúng / thiếu ý / sai / thừa bởi **một sub-agent mới** (không thấy khóa X / Y, không thấy điểm
     judge); User xem lại bảng nhãn. A ghép khóa sau khi bảng nhãn xong.
5. **Mỗi thí nghiệm Bước 2 có plan riêng** (khuôn YAML `run-experiment` §1, mục "Căn cứ để review"), session khác người viết
   review, A duyệt sha trước khi đo (`WORKFLOW.md` §9.1). Mốc của Bước 2 = chatbot **sau** Bước 1.
6. **Luna (E3b) dù thắng vẫn trình User** trước khi vào chatbot: thêm một lần gọi API mỗi câu và độ trễ (8.1 đo ~3,3–3,6 s p50
   khi xếp lại 10 đoạn; xếp lại N > 10 đoạn **chưa đo**, nhiều khả năng chậm hơn) là đổi trải nghiệm, không chỉ đổi chất lượng.
7. **3 câu kín A đã thấy:** giữ trong bộ; ở mốc cuối báo số cả 36 câu và 33 câu (bỏ 3 câu đó). Lý do: thay câu mới cần tạo +
   duyệt lại; báo hai số đủ minh bạch.
8. **Mốc "chatbot đầu 8.2"** = commit `f26485b` (context 5, chưa NFC), chạy lại bằng `git worktree` tại commit đó khi cần (B3).

## 4. Phạm vi

**Trong:** đổi `max_context_documents` 5 → 10 (`backend/config/settings.yaml` + kiểm cứng ở `backend/core/settings_loader.py:77`);
test ghim giá trị cũ (`backend/tests/test_phase6_settings.py:25` ghim 5); NFC câu hỏi; prompt / generator cho E1, E2; retrieval + rerank luna cho E3 (tham số mặc định = hiện tại); harness thí nghiệm
`backend/experiments/phase_8_2/`; file mốc người (private, `data/phase_8_2/`); paid `gpt-6-luna` trong trần D5; báo cáo.

**Ngoài:** build lại index / sửa chunker / sửa corpus (gồm Hải Vân); index Qwen3-8B; model sinh khác (giữ `gpt-6-luna`); reranker
GPU (M1 / M2 đã kém hơn ở 8.1); câu không dấu (User 15:15 25/10: ngoài phạm vi); Representation B; Agentic RAG (Phase 9).
Qdrant **chỉ đọc** (8.2 không tạo collection).

## 5. Các bước

Mỗi bước: người làm → report → session khác review chéo → A đóng / đưa vào chatbot theo D4. Mỗi thay đổi runtime: A sửa đủ 4
chỗ `bao_cao_he_thong/` (`WORKFLOW.md` §6).

### B0 — Mốc người (free; User ~30–45 phút)

Chuẩn bị file đọc cặp mù (mục 3.3); User đọc; tóm nhãn (3.4); áp luật dừng (3.4). Chạy song song được với phần code B1.

### B1 — Context 10 + NFC vào chatbot (paid nhỏ)

1. Code: settings + loader cho 10; NFC (3.2). Test nhỏ cho NFC (câu NFD → NFC giống hệt).
2. Tiêu chí ghi trước:
   - **retrieval 158 câu trong phạm vi giống byte mốc** `cefb2d1a…` (`data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl`,
     158 = 176 − 18 out_of_scope; retrieval không đổi). Phép so này không chạm NFC (Golden đã NFC khi nạp) ⇒ thêm kiểm live dưới;
   - **đường runtime = harness, tất định:** lượt sinh 176 câu trên runtime mới có `top_chunk_ids`, `context_sources`, `input_tokens`
     bằng G2.1a **176 / 176 câu**; lệch ⇒ dừng, tìm nguyên nhân;
   - cùng lượt đó + judge Claude, **G2.1a chấm lại cùng lượt mù**: **0 câu out_of_scope bị trả lời**, lỗi kỹ thuật 0, Completeness
     không khác (CI chứa 0). Lượt B1 ↔ G2.1a là **A/A nhiễu của context 10** (cùng cấu hình) — ghi làm nhiễu cho E1 / E2;
   - API live qua `/chat`: một câu hỏi thật trả tới 10 nguồn đã đóng gói, có citation; **một câu NFD** trả cùng nguồn với bản NFC của nó.
3. Đạt + review chéo + B0 không dừng ⇒ A commit, báo User (D4).

### B2 — Tín hiệu trên chatbot mới (paid nhỏ; thứ tự D3)

| Thí nghiệm | Thay đổi | Sàn | Chỉ số quyết | Mức tụt cho phép (plan ghi số) |
|---|---|---|---|---|
| **E1** trả lời một phần | prompt cho phép trả lời phần có căn cứ, **giữ từ chối câu ngoài phạm vi** (P1 8.1 phạm sàn 2 câu) | 0 câu out_of_scope bị trả lời (dev + test) | số câu trong phạm vi bị từ chối nhầm giảm vượt nhiễu | Completeness, Accuracy, lỗi citation (số câu) |
| **E2** lỗi thiếu `[n]` | một cách sửa chọn trong plan (ví dụ luật prompt P2, hoặc sinh lại một lần khi thiếu `[n]`) | 0 câu out_of_scope bị trả lời | số câu lỗi citation (đếm bằng code) giảm | Completeness, USD / câu, latency p95 |
| **E3a** pool rộng | pool 100 (cách trộn native như G4-B 8.1), **không rerank** → top-10; tầng tìm free, tất định; **trước khi vào chatbot: lượt sinh dev + test**, chấm cùng lượt mù với mốc B1 | 0 câu mất đoạn đúng khỏi context; 0 câu out_of_scope bị trả lời | số câu đủ đoạn đúng trong 10 đoạn đưa model | Completeness, lỗi citation (số câu), latency (ms) |
| **E3b** + luna | E3a + rerank listwise `gpt-6-luna` xếp lại **N ứng viên đầu (N > 10, plan ghi N)** → top-10 | 0 câu mất đoạn đúng khỏi context; 0 câu out_of_scope bị trả lời | chỉ số câu trả lời chọn trong plan | latency (giây), USD / câu |

- **Luật bỏ sớm E3** (free, tầng tìm kiếm): trên chatbot sau B1, đếm câu dev có đoạn đúng mà **thiếu** đoạn đúng trong 10 đoạn
  đưa model nhưng **có** trong pool 100. Không đủ số câu để CI 95% > 0 (cách tính cỡ mẫu `run-experiment` §1.6) ⇒ E3a, E3b NOT RUN,
  ghi lý do. E3b chỉ chạy khi, sau E3a, vẫn còn đủ câu có thể cứu — đếm câu thiếu đoạn đúng trong 10 đoạn đưa model nhưng **có trong N
  ứng viên đầu** (N của E3b), trên mốc tốt hơn giữa B1 và E3a.
- **Lý do tách:** ở context 10, luna xếp lại đúng 10 đoạn top-10 chỉ đổi thứ tự, không đổi tập đoạn model thấy; số luna 8.1 đo ở
  top-10 của pool 30 (`data/phase_8_1/g4/a_luna_plain_*.meta.json`) nên không chuyển sang được. Pool tự nó đã có tín hiệu (+4 / −1).
- Mỗi thí nghiệm chọn trên dev, xác nhận trên test (`split.json`); nhiễu A/A ghi trước khi đo biến thể (dùng lại nếu đầu vào không
  đổi). Kết luận theo luật giữ / gỡ `run-experiment` §4.
- **E1 thắng ⇒ trình User** kèm ~10 câu đổi từ "từ chối" sang "trả lời một phần" để User đọc (đổi hợp đồng
  `docs/superpowers/specs/2026-09-14-phase-6-full-corpus-generation-api-ui-written-spec.md` §10). E3b thắng ⇒ trình User (3.6). E2, E3a
  thắng ⇒ A đưa vào (D4).

### B3 — Mốc cuối (User quyết mở câu kín)

Chatbot cuối 8.2 chạy 36 câu kín (`knowledge-base-hue/evaluation/phase_8_1/sealed_official.jsonl`) so với chatbot đầu 8.2
(context 5) — một session được giao rõ mở câu kín; báo 36 và 33 câu (3.7). Sau đó tổng hợp, `TONG_HOP.md`, User đóng 8.2.

## 6. Tiêu chí nghiệm thu 8.2

1. B0 xong: User đã đọc, bảng nhãn User xem lại; luật dừng áp và ghi kết quả.
2. B1: tiêu chí B1.2 đạt; chatbot thật chạy context 10 + NFC; 4 chỗ `bao_cao_he_thong/` cập nhật.
3. Mỗi E1, E2, E3a, E3b có plan duyệt sha trước khi đo, kết luận tốt hơn / không đổi / kém hơn / chưa rõ / NOT RUN, xác nhận trên test khi
   "tốt hơn"; thay đổi vào chatbot theo D4.
4. B3 chạy khi User quyết; kết quả ghi cả âm.
5. Tiền thật từ log ≤ 0,5 USD; mỗi report ghi token + USD. Qdrant vẫn đúng 1 collection runtime.

## 7. Quyền và giới hạn

- Paid: chỉ `gpt-6-luna` (0,1 / 0,5 USD mỗi 1M token vào / ra); trần 0,5 USD cả 8.2; mỗi lượt có phí pilot 10 câu, ước lại từ
  pilot; vượt ước pilot > 50% ⇒ dừng báo A. Ước: B1 ~0,04; mỗi biến thể E1 / E2 ~0,03–0,05 (dev + test); E3a ~0,04 (lượt sinh dev + test; tầng tìm 0); B3 ~0,015
  (36 câu kín × 2 chatbot, *suy ra*). **E3b chưa đo**: *suy ra* từ token G4 (~1.430 token vào / câu khi xếp 10 đoạn) × N/10, cộng lượt sinh
  ~0,0002 USD / câu — N 30 ≈ 0,0011 USD / câu ≈ 0,19 USD / 176 câu; N 100 ≈ 0,30–0,39 USD. Trước E3b: pilot 10 câu, ước lại; tổng dự kiến vượt phần trần
  còn lại ⇒ dừng, hỏi User nâng trần hoặc bỏ E3b.
- Judge: Claude sub-agent (quota, không USD); baseline và biến thể chấm cùng lượt mù.
- Ghi file private: `data/phase_8_2/`. Không sửa corpus, Golden, split, đoạn đúng, câu kín.
- Sửa runtime: chỉ các file mục 4; A commit / push; B/C không commit.

## 8. Rủi ro và cách giảm

| Rủi ro | Giảm |
|---|---|
| Judge Claude sai nhất quán ⇒ quyết sai | B0 mốc người trước Bước 2; luật dừng 3.4 (≥ 5 cặp quyết, dưới mức ⇒ hỏi User) |
| User nhận ra bên nào là context 10 | Đánh số lại citation, chỉ hiện nguồn được trích; kiểm bằng code (3.3) |
| Đường runtime khác harness 8.1 (context 10 chạy khác) | B1.2: so với G2.1a, retrieval giống byte |
| E1 làm chatbot trả lời câu ngoài phạm vi | Sàn 0 câu; User đọc mẫu trước khi vào chatbot |
| Bộ thử nhỏ ⇒ nhiều "chưa rõ" | Cỡ mẫu tính trước; luật bỏ sớm E3; "chưa rõ" là kết quả hợp lệ |
| Test 56 câu đã bị nhìn ở 8.1 | Ghi giới hạn; câu kín ở B3 là phép kiểm cuối |
| 8.2 kéo dài | Thứ tự D3; dừng giữa chừng vẫn giữ được phần đã vào chatbot |

## 9. Nguồn

- 8.1: `report_agent/2026-10-24_phase_8_1_ra_soat/` (`TONG_HOP.md`, `phase_8_1_g5_synthesis.md`, `phase_8_1_g5_decision_table_draft.md`,
  `phase_8_1_g2_implementation.md`, `phase_8_1_g4_implementation.md`, `phase_8_1_g5_by_category.md`).
- Spec 8.1: `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md`. Hợp đồng trả lời: spec Phase 6 full-corpus §10.

## 10. Sửa đổi 26/10 — Bước 2 mở rộng thành "đợt cải tiến từng khâu" (A, terminal `hue-rag-2d`)

Bản gốc §1–§9 (sha `dabae90b2b60`, User duyệt 16:21 25/10) giữ nguyên, trừ chỗ mục này ghi "thay". Mục này **chỉ đổi Bước 2** (B2); B0, B1,
B3 như cũ. Đợt báo cáo: `report_agent/2026-10-26_cai_tien_tung_khau/`.

**Căn cứ để review (mục 10):** (1) mục này; (2) `phan_loai_loi_C.md` §1, §3 và `phan_loai_loi_B.md` §1, §3.2 (lỗi theo tầng ở context 10);
(3) `de_xuat_khau_tim_B.md` §3–§5 và `de_xuat_khau_tra_loi_C.md` §1, §3–§5 (biến thể, số 8.1 đã đo, cỡ mẫu); (4) `skills/run-experiment/SKILL.md`
§1, §3, §4.

### 10.1 Vì sao đổi

User 20:0x 25/10 mở "đợt tìm hướng tốt hơn từng khâu"; 21:1x 26/10 chọn **phạm vi B: khâu trả lời + thí nghiệm khâu tìm, không ghi Qdrant**,
và cho A tự đề xuất / thử / so sánh / chọn trong luật dưới. Phân loại lỗi trên mốc context 10 (C36, B42; A tính lại số chính — review cùng đợt):
88 câu dev chính còn 10 câu bị cờ, **cả 10 thiếu bằng chứng trong 10 đoạn**; 18 / 40 câu có đoạn đúng còn thiếu, chia gần đôi "ngoài pool
30" (11 fact) và "trong pool nhưng ngoài top-10" (12 fact). Phần riêng khâu trả lời: 5 câu từ chối khi context có một phần fact (20 điểm
Completeness), 9 câu trả lời gọn bỏ chi tiết có sẵn (9 điểm) — trần ≈ +0,33 Completeness. ⇒ thí nghiệm **cả hai khâu**, mỗi khâu một nhánh.

### 10.2 Mốc và luật nhận (thay dòng "chỉ số quyết" ở bảng B2 cho các biến thể mới)

- **Mốc duy nhất:** chatbot context 10 + NFC = nhánh `p82-b1` `811d25d` (B41; T1 `cefb2d1ad609`); câu trả lời mốc `data/phase_8_2/b1/b1_{dev,test}.jsonl`.
  **Mọi biến thể so với mốc này** (User 20:4x: không so nối tiếp). Cấu hình ghép các biến thể thắng = một lượt xác nhận riêng, cũng so với mốc.
  Thí nghiệm chạy bằng harness trên mốc, **trước B0** — **thay §8 dòng 1 và D1 cho mục 10**: mọi kết luận dựa judge là **tạm** tới khi B0 xong và
  luật dừng 3.4 áp; B0 cho thấy judge lệch người ⇒ A xét lại kết luận trước khi đưa vào chatbot. Đưa vào chatbot: context 10 chỉ sau B0 (B1 §5);
  biến thể thắng chỉ sau khi context 10 đã vào.
- **Luật (a)** (User 20:4x) — biến thể làm **rẻ / nhanh hơn**: chỉ số quyết = USD / câu hoặc latency (một trong hai, ghi trước) tốt hơn rõ
  (≤ 0,95 × mốc USD hoặc ≤ 0,9 × mốc tốc độ — **đo theo khâu, xem dòng "Đo tốc độ theo khâu"**; latency khâu tìm: mốc và biến thể đo **cùng phiên, ≥ 2 lượt** — A/A B1 ↔ G2.1a p50 +4,6 %, p95 +17 %, C38 m-2); **mức tụt** Completeness dev chính: **chênh TB ≥ −0,1 và số câu tụt ≤
  A/A + 3** (A chốt theo C37 §1.4: cận dưới CI quá khắt với n 41–88).
- **Luật (i)** (User 21:1x) — biến thể làm **chất lượng tăng**: chỉ số quyết vượt nhiễu (paired bootstrap CI 95 % > 0; A/A ghi trước) **và**
  tốc độ không tệ hơn (khâu tìm ≤ +50 ms / câu; khâu sinh theo dòng "Đo tốc độ theo khâu") **và** không tốn thêm tiền = **không thêm lần gọi API / dịch vụ nào, USD / câu tăng ≤ 20 %** (User 21:3x, 10.6 Q1). Biến thể vượt ngưỡng tốn (ví dụ K3 luna +3–5 s)
  ⇒ **A trình User kèm số**, không tự nhận. **Chất lượng trước** (User 22:03): biến thể chậm / tốn hơn nhưng có thể nâng chất lượng (K3) **vẫn được
  thử** để biết trần chất lượng; thắng thì tìm cách làm nhanh / rẻ hơn trước khi trình User đưa vào chatbot. Trần độ trễ 5 s / câu (p95) = **theo dõi**
  tới khi User đặt yêu cầu phi chức năng. Latency đo cùng phiên với mốc. **Mức tụt luật (i)** (C38 M-3): Completeness và Accuracy dev chính —
  số câu tụt ≤ A/A + 3; từ chối nhầm trong phạm vi tăng ≤ A/A + 1 câu; lỗi citation (validator v2) tăng ≤ 2 câu.
- **Đo tốc độ theo khâu** (A 22:2x, B49 M-1): khâu tìm (chạy trên máy, tất định) — latency trung bình chênh theo câu ≤ +50 ms, mốc và biến
  thể xen kẽ cùng phiên. Khâu sinh (R*) — latency một lần gọi dao động mạnh (B1 ↔ G2.1a cùng đầu vào: SD chênh theo câu ≈ 808 ms ⇒ 30 câu chỉ
  phân giải ±289 ms; ±50 ms cần ~1.000 lần gọi) ⇒ "tốc độ" đo bằng **`output_tokens` / câu** (0 USD thêm; gồm cả token suy luận — 8.1 G2.4: `none` 54 so với `medium` 79; A/A B1 ↔ G2.1a
  dev 120: TB 77,0 / 77,0, SD chênh theo câu 28 token ⇒ ±6,6 % — B, 22:3x): mức tụt
  ≤ +20 % (khớp USD), "nhanh hơn rõ" (luật (a)) ≤ 0,9 × mốc; latency p50 / p95 chỉ theo dõi, kèm CI. User nói "hiệu suất = tiền + tốc độ": cả
  hai vẫn báo trong mọi report.
- **Sàn chung:** 0 / 18 câu out_of_scope bị trả lời (dev + test); khâu tìm: 0 câu mất đoạn đúng khỏi context so với mốc; khâu trả lời: 120, 168 (từ
  chối đúng — context không có fact) vẫn từ chối; 0 câu lỗi kỹ thuật / 500.
- **Họ Holm:** chỉ biến thể luật (i) (có p-value); R1 (luật a) không vào họ. Nhánh tìm {K1, K3 nếu chạy}, nhánh trả lời {R2, R3}; Holm trên
  biến thể chạy thật của nhánh.
- **Test (41 câu chính / 15 câu có đoạn đúng)** quá nhỏ để thấy "tốt hơn" ⇒ xác nhận trên test = **"không làm hỏng"** (sàn + mức tụt như luật
  tương ứng). Lệch `run-experiment` §4 ⇒ **chờ User** (10.6 Q2); câu kín (B3) là phép kiểm cuối.

### 10.3 Biến thể và thứ tự

| Nhánh | # | Đổi một thứ | Luật | 8.1 đã đo | Trần dev | Ước tiền |
|---|---|---|---|---|---|---|
| tìm | **K1** | pool dense 30 → 100, giữ cách runtime (BM25 xếp lại trong pool, RRF k 60) — **thay E3a** | (i) | chưa (thử khô 5 câu) | 6 câu | 0 (tầng tìm); lượt sinh khi qua tầng tìm ≈ 0,036 |
| tìm | ~~K2~~ | native p30 k = 2 — **NOT RUN** (C38 M-2): là biến thể tốt nhất trong 10 của G1.3 và đã trượt Holm-10; chọn lại trên cùng dev là chọn vì may; còn đổi hai thứ (ứng viên native + `rrf_k` 60 → 2, `retrieval/full_corpus.py:393`; native p30 k 60 mất 2 câu) | — | dev 4 / 36 / 0 [+0,025; +0,200], p 0,026 | — | 0 |
| tìm | K3 | rerank luna listwise pool 30 → top-10 (= E3b, N = 30) — chỉ khi K1 không đủ | trình User | luna top-10 MRR +0,17 (không đổi tập 10) | 9 câu | ≈ 0,0005 USD / câu + 3–5 s (ước; pilot 10 câu trước) |
| trả lời | **R4** | thước "số trong câu trả lời có trong đoạn được trích" (theo dõi, không chặn) | thước | C36 thử tay 2 / 5 đúng | — | 0 |
| trả lời | **R1** | `reasoning_effort="none"` (runtime hiện không gửi ⇒ `medium`) | (a), chỉ số quyết (User 22:03): **USD / câu ≤ 0,95 × mốc HOẶC `output_tokens` / câu ≤ 0,9 × mốc**, mặt còn lại không tệ hơn mốc (= ước lượng điểm ≤ 1,00 × mốc trên dev 120 — USD / câu phân giải ±1,2 %, `output_tokens` ±6,6 %; token vào
  chiếm ~80 % USD ⇒ R1 giảm USD tối đa ~19 % — B 22:3x; 0 USD thêm — 10.2 "Đo tốc độ theo khâu") | ctx 5: Completeness +0,136, USD 0,91×, p50 0,92×; lý do loại (citation) hết với validator v2 | — | ≈ 0,034 |
| trả lời | **R2** | trả lời phần có căn cứ (= **E1** / E1b; plan E1 sửa: mốc `811d25d`, `paired_stats` / `false_refusal`, citation v2, trần 5 câu) | (i) + **User duyệt hợp đồng** (D4) | P1 ctx 5 phạm sàn 2 câu | 5 câu | ≈ 0,04 |
| trả lời | **R3** | câu prompt "nêu đủ chi tiết có trong bằng chứng" | (i) | chưa | 9 câu (+1 mỗi câu) | ≈ 0,036 |
| — | E2 | sửa lỗi thiếu `[n]` | — | validator v2: mốc 0 lỗi | 0 | **NOT RUN** (luật bỏ sớm) |

- **Thứ tự:** hai nhánh **song song** (file không chồng: khâu tìm = harness retrieval, khâu trả lời = prompt / settings harness) —
  **thay D3 cho Bước 2** (C38 m-5): khâu tìm K1 → (K3 nếu cần); khâu trả lời R4 → R2 → R3 → R1. **Nguyên tắc User 21:3x: "ưu tiên đạt chất lượng cần thiết trước, sau đó mới tối ưu hiệu
  suất"** ⇒ biến thể nâng chất lượng (luật (i)) chạy trước biến thể tối ưu tiền / tốc độ (luật (a), R1); R1 so cùng mốc, đo sau cùng. Không chạy: giới hạn đoạn / file (B43 V4 — 17 / 22 câu đang đủ có file đúng chiếm > 3 chỗ), G4-B M1
  (10–14 s / câu GPU), `low` / `high`, xếp theo tài liệu, streaming, tách câu hỏi (để đợt sau).
- **Ghép:** sau hai nhánh, các biến thể nhận được ghép thành một cấu hình, chạy một lượt dev + test so mốc (luật của biến thể chặt nhất); hỏng ⇒ giữ
  từng cái riêng theo thứ tự lợi lớn hơn.
- Mỗi biến thể: **plan có "Căn cứ để review" + YAML** (khuôn B43 §4 / C37 §4) ⇒ session **khác người viết** review ⇒ A ghi "duyệt bản sha" ⇒ chạy
  ⇒ report ⇒ review chéo ⇒ kết luận tốt hơn / không đổi / kém hơn / chưa rõ / NOT RUN. **Cỡ mẫu ghi trước** (`bootstrap_mean_diff`, seed 20261024,
  mỗi câu ±1; C38 M-1): 4 thắng / 0 thua cho p 0,026 (40 câu) / 0,031 (88 câu) ⇒ trượt ngưỡng đầu Holm họ 2 (0,025); 5 / 0 cho 0,008 / 0,013 ⇒ qua.
  ⇒ K1 cần **≥ 5 / 0** trên 40 câu (trần 6); R3 **≥ 5 / 0** trên 88 (trần 9); R2 **5 / 5** câu trần ⇒ **"chưa rõ" rất có thể** — kết quả hợp lệ.

### 10.4 Quyền, tiền, dừng

- Tiền: trần 8.2 **0,5 USD** giữ (đã dùng 0,0369); ước cả mục 10 không K3 ≈ 0,19 USD (K1 lượt sinh 0,036, R1–R3 0,11, ghép 0,04 ⇒ ≈ 0,19), K3 thêm ≈ 0,1.
  Trong trần 1 USD / phiên (User 20:3x). Pilot 10 câu trước mỗi lượt có phí; vượt ước pilot > 50 % ⇒ dừng báo A.
- Không ghi Qdrant, không build index, không sửa corpus / Golden / split / đoạn đúng / câu kín. File private ở `data/phase_8_2/` (`k*`, `r*`).
- Đưa vào chatbot (thay D4 cho mục 10): A tự đưa biến thể qua luật (a) / (i) + review chéo (User 21:1x); **R2 và mọi biến thể "tốn hơn" chờ User**.
  Mỗi lần vào chatbot: cổng ổn định (CURRENT_HANDOFF "Cổng ổn định") + 4 chỗ `bao_cao_he_thong/`.

### 10.5 Rủi ro thêm

| Rủi ro | Giảm |
|---|---|
| Thử nhiều biến thể trên cùng dev ⇒ chọn nhầm vì may | Holm theo nhánh; test xác nhận "không làm hỏng"; câu kín B3 cuối |
| R1 `none` làm câu trả lời ngắn ⇒ under-answer tăng | Theo dõi 9 câu U của C36 + R4; mức tụt luật (a) |
| K1 BM25 chấm thêm 70 đoạn đẩy đoạn đúng của câu đang đủ ra ngoài | Sàn 0 câu mất đoạn đúng khỏi context |
| Nhãn lỗi C36 do một agent gắn | Chỉ dùng chọn biến thể / tính trần. Đoạn đúng 8.1 (agent gắn, agent khác kiểm, User duyệt ~10 câu) **là** chỉ số quyết khâu tìm như 8.1 — report ghi giới hạn (C38 m-1) |

### 10.6 Câu chờ User

- **Q1 — đã trả lời (User 21:31):** "không tốn thêm tiền" của luật (i) = **không thêm lần gọi API / dịch vụ nào, USD / câu tăng ≤ 20 %**
  (≈ +0,00004 USD / câu). Kèm nguyên tắc "chất lượng cần thiết trước, tối ưu hiệu suất sau" (thứ tự 10.3).
- **Q2 (C38 m-3):** xác nhận trên test (41 câu chính / 15 câu có đoạn đúng) = **"không làm hỏng"** (sàn + mức tụt), không đòi "tốt hơn" vượt
  nhiễu — vì test quá nhỏ (3 / 0 vẫn CI [0; +0,171]). (A khuyên) đồng ý; khác: đòi test cũng "tốt hơn" ⇒ gần như mọi biến thể thành "chưa rõ".
