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
