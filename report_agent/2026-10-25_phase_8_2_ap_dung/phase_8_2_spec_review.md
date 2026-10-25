# Review: Phase 8.2 — nháp spec "Áp dụng phương án thắng 8.1" (B22)

Decision: **changes_requested**
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-de`)
Date: 2026-10-25 16:11 +0700 (`date`)
Canonical guide: `skills/run-experiment/SKILL.md` §1, §3, §4; `session_prompt/WORKFLOW.md` §9.1
Bản được review: `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` bản 1, sha256 `2c8d40e3aa4c` (B kiểm lại
16:11, khớp tin A). Việc: B22 trong `CURRENT_HANDOFF.md`. 0 USD.

## 1. Phạm vi đã review

Chỉ dựa trên gói "Căn cứ để review" của spec (`WORKFLOW.md` §9.1), theo đúng mức đọc spec ghi:

- spec — full-read (132 dòng);
- `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g5_synthesis.md` §3, §4, §6;
- `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g5_decision_table_draft.md` §1 (dòng 2a, 2b, 6, 8 và cả bảng §1 để
  thấy ngữ cảnh), §3;
- `skills/run-experiment/SKILL.md` §1, §3, §4.

Ngoài gói, B chỉ chạy **lệnh chỉ đọc** để kiểm khẳng định của spec (được phép theo B22): đọc code
`backend/core/settings_loader.py`, `backend/api/app.py`, `backend/evaluation/full_corpus_eval.py`,
`backend/evaluation/golden_full_corpus.py`, `backend/tests/test_phase6_settings.py`; đọc metadata / đếm từ
`data/phase_8_1/g2/`, `data/phase_8_1/g4/`, `data/phase_8_1/baseline/g0_6_manifest.json`,
`data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl`; đếm `category` trong Golden.
**Không** đọc `STATUS_A.md`, tin nhắn khác của A, hay câu kín. Không sửa spec.

## 2. Findings

Không có blocker. **4 major, 5 minor.**

### Major

**M1 — E3: căn cứ chi phí / độ trễ / tín hiệu của luna là từ cấu hình khác (top-10 của pool 30, context 5).**
- Vị trí: spec §3.6 ("~3,5 s / câu"), §5 B2 bảng dòng E3, §7 ("E3 luna ~0,05").
- Yêu cầu: `run-experiment` §1.5 (ước tiền trước), §1.6 (cỡ mẫu / câu có thể đổi); spec §1 (thử lại tín hiệu "trên chatbot mới").
- Bằng chứng: `data/phase_8_1/g4/a_luna_plain_{pilot,rest}.meta.json`: `"input": "top10"`, `"pool": 30`; 30 câu dùng
  42.852 token vào (≈ 1.430 token / câu), 0,0088 USD (≈ 0,00029 USD / câu), rerank p50 3,3–3,6 s, p95 ≈ 5,1 s. Bảng G5 §1 dòng 8
  cũng ghi luna đo ở "top-10". Chưa có lượt nào luna xếp lại pool 100.
- Tác động:
  1. Khi context = 10, luna xếp lại đúng 10 đoạn top-10 rồi đưa cả 10 vào model ⇒ **tập đoạn model thấy không đổi**, chỉ đổi
     thứ tự. Tín hiệu 8.1 (MRR@10 +0,17; 3 câu được đưa đoạn đúng vào 5 đoạn) đo ở context 5 nên không chuyển sang được. Muốn
     luna có tác dụng ở context 10 thì phải xếp lại > 10 ứng viên — đúng như E3 ghi "pool 100", nhưng cấu hình đó **chưa đo**.
  2. *Suy ra (chưa đo)*: xếp lại 100 đoạn ≈ 10 lần token vào ⇒ cỡ 0,0015–0,002 USD / câu, 176 câu ≈ 0,26–0,35 USD, tức hơn
     nửa trần D5 0,5 USD (spec ước 0,05). Độ trễ cũng nhiều khả năng > 3,5 s.
  3. §3.6 trình User "~3,5 s / câu" là số của cấu hình khác.
- Tiêu chí đóng: spec ghi rõ E3 xếp lại bao nhiêu ứng viên (N); ghi số chi phí / độ trễ là "chưa đo, ước từ token của G4 × N/10";
  ước lại tổng tiền 8.2 so với D5 (hoặc ghi E3 sẽ hỏi lại trần tiền nếu pilot vượt); sửa §3.6 cho khớp. Không cần chạy gì
  thêm để đóng finding này.

**M2 — E3 gộp hai thay đổi (pool 100 và rerank luna) trong một biến thể.**
- Vị trí: spec §5 B2 bảng dòng E3 ("pool 100 + rerank listwise `gpt-6-luna` → top-10").
- Yêu cầu: `run-experiment` §1.2 ("một thay đổi mỗi biến thể").
- Bằng chứng: bảng G5 §3 dòng 4: pool rộng tự nó +4 / −1 câu, "G4-B cho thấy phần lợi chủ yếu do pool"; dòng 4 gần như không
  tốn tiền, tất định; dòng 5 (luna) tốn tiền + độ trễ + phụ thuộc API.
- Tác động: nếu E3 "tốt hơn" thì không biết do pool hay do luna ⇒ có thể đưa luna (+độ trễ, +một lần gọi API mỗi câu) vào
  chatbot trong khi riêng pool 100 đã đủ.
- Tiêu chí đóng: tách E3a = pool 100, không rerank (miễn phí, tất định, đo trước) và E3b = E3a + luna xếp lại N ứng viên; E3b
  chỉ chạy khi luật bỏ sớm còn đủ câu sau E3a. Luật bỏ sớm hiện tại giữ nguyên làm cổng cho cả hai.

**M3 — Luật dừng của mốc người (§3.4) chưa đo được như đang viết.**
- Vị trí: spec §3.3, §3.4; §6 tiêu chí 1.
- Yêu cầu: `run-experiment` §1.3 ("mỗi chỉ số định nghĩa chính xác: hàm nào tính, đếm gì, không đếm gì, n bao nhiêu"); B22
  yêu cầu kiểm riêng luật dừng 3.4.
- Bằng chứng / lập luận: (a) "judge chấm khác nhau" không nói theo chỉ số nào (Completeness? Accuracy? tổng ba chỉ số?) và file
  điểm nào (`data/phase_8_1/g2/judge/`, `judge_test/`). (b) Không có số cặp tối thiểu: mẫu 15–20 câu, User "không bắt buộc" ghi
  bên hơn ⇒ số cặp vừa có ý User vừa khác điểm judge có thể chỉ 0–3. Khi đó 1 cặp quyết, hoặc 0 cặp thì luật **lặng lẽ cho qua**
  — đúng trường hợp mốc người không kiểm được gì. (c) Cặp judge chấm **như nhau** mà User thấy rõ một bên hơn (judge không nhạy)
  không được tính, dù mẫu cố ý lấy ~1/2 cặp như vậy. (d) Người tóm nhãn chỉ ghi "một session khác A" — B đã chạy G2 và từng thấy
  điểm judge tổng hợp; người tóm nhãn phải không thấy khóa X / Y và điểm judge.
- Tác động: luật bảo vệ quyết định giữ context 10 và mọi quyết định Bước 2 dựa vào judge; như đang viết có thể "đạt" mà không có
  bằng chứng.
- Tiêu chí đóng: spec ghi (1) chỉ số và file điểm judge dùng để so; (2) số cặp tối thiểu (ví dụ ≥ 5 cặp có ý User **và** judge
  khác nhau), dưới mức đó ⇒ kết quả "chưa rõ" ⇒ A trình User trước Bước 2, không tự cho qua; (3) cách tính cặp judge hòa mà User
  ghi một bên hơn (ít nhất là báo số đó); (4) người tóm nhãn không thấy khóa và điểm judge.

**M4 — Mù X / Y bị lộ qua số citation.**
- Vị trí: spec §2 D2 ("xếp ngẫu nhiên"), §3.3.
- Yêu cầu: D2 / §3.3 — User đọc cặp **mù**.
- Bằng chứng: đếm trên `data/phase_8_1/g2/g2_context10.jsonl` + `t_context10.jsonl` (176 câu): 146 câu có trả lời (không từ chối),
  **25 câu có citation `[6]`–`[10]`** — không thể có ở câu trả lời context 5. Danh sách nguồn kèm theo (10 vs 5) cũng lộ.
  Mẫu cố ý lấy ~1/2 câu judge chấm context 10 hơn (thường là câu nhiều nguồn, nơi citation cao hay xuất hiện) ⇒ tỉ lệ lộ trong mẫu
  có thể cao hơn 25/146.
- Tác động: User biết bên nào là context 10 ⇒ mốc người không còn độc lập với giả thuyết đang kiểm.
- Tiêu chí đóng: spec ghi cách trình bày làm hai bên không phân biệt được bằng hình thức — ví dụ đánh số lại citation mỗi câu trả
  lời theo thứ tự xuất hiện (1..k) và chỉ hiện nguồn được trích; kèm kiểm bằng code trên file đưa User: 0 câu trả lời có số
  citation > số nguồn hiện kèm, và số nguồn hiện không cho biết context.

### Minor

**m1 — B1.2 "retrieval 176 câu giống byte mốc `cefb2d1a…`": mốc chỉ có 158 dòng.** `g0_6_manifest.json`:
`retrieval_baselines.dense_bm25_rrf.stored` = `data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl`, `lines: 158`; Golden
có 18 câu `out_of_scope`, không câu nào có dòng trong file đó (158 = 176 − 18). Đóng: sửa thành "158 câu trong phạm vi".
Thêm: `backend/evaluation/golden_full_corpus.py:33` đã NFC câu Golden khi nạp ⇒ phép so byte này **không** chạm được NFC ở đường
API. Đóng: B1.2 thêm một kiểm live — câu NFD qua `/chat` trả cùng nguồn với bản NFC (ngoài test đơn vị NFC đã ghi).

**m2 — B1.2 có thể kiểm "đường runtime = harness" bằng số tất định, không chỉ CI chứa 0.** Mỗi dòng G2.1a có `top_chunk_ids`,
`context_sources`, `input_tokens` (kiểm `g2_context10.jsonl`; 120 dev + 56 test = 176). Cùng prompt + cùng context ⇒
`input_tokens` phải bằng nhau từng câu. Đóng: thêm tiêu chí "176/176 câu `top_chunk_ids`, `context_sources`, `input_tokens` bằng
G2.1a" (lệch ⇒ dừng, đúng như "đường runtime ≠ harness"). Kèm: ghi rõ lượt B1 và G2.1a cùng là context 10 không đổi gì ⇒ chính
là **A/A nhiễu của context 10** (`run-experiment` §3.1 cần trước E1 / E2; A/A 7B là context 5), và G2.1a được chấm lại **cùng
lượt mù** với lượt B1 (§7 đã ghi luật chung, B1.2 nên ghi rõ).

**m3 — Phạm vi §4 / §7 ("chỉ các file mục 4") thiếu test.** `backend/tests/test_phase6_settings.py:25` ghim
`"max_context_documents": 5` ⇒ đổi settings làm test này fail. Đóng: §4 ghi thêm test bị ảnh hưởng (sửa giá trị ghim), và chỗ NFC
trong evaluator (`full_corpus_eval.py:91`, `:132` đã có NFC riêng) để plan B1 chọn đúng "một chỗ" ở §3.2.

**m4 — D4 khác dòng luật trong skill.** `run-experiment` §4: "đưa vào runtime là việc riêng, User duyệt"; bảng G5 §3 cột "Cần
User duyệt" ghi đổi runtime. D4 là quyết định của User nên hợp lệ, nhưng spec nên ghi một câu "D4 thay dòng §4 của
`run-experiment` cho 8.2" để người review sau không ghi finding.

**m5 — Tiền B3 chưa ước, mốc "chatbot đầu 8.2" chưa gắn commit.** B3 chạy 36 câu kín × 2 chatbot (*suy ra* ≈ 0,015 USD) nhưng
§7 không ghi. "Chatbot đầu 8.2 (context 5)" phải tái lập được sau khi code đã đổi ⇒ ghi commit gốc (ví dụ `f26485b`) và cách
chạy (worktree tại commit đó).

## 3. Cách người kiểm chạy lại thật

Chỉ đọc, 0 USD, không gọi API, không ghi dữ liệu dùng chung:

- `sha256sum docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` ⇒ `2c8d40e3aa4c…`.
- Đọc `backend/core/settings_loader.py:77-78`, `backend/api/app.py:93-102`, `backend/evaluation/full_corpus_eval.py:272-284, 372-375`,
  `backend/evaluation/golden_full_corpus.py:33`, `backend/tests/test_phase6_settings.py:25`; `grep` `max_context_documents` trong `backend/`.
- `python3 -I` đọc JSON: `data/phase_8_1/baseline/g0_6_manifest.json` (mục chứa `cefb2d1a`); đếm dòng / key của
  `data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl`; đếm `category` Golden; metadata `data/phase_8_1/g2/*context10*.meta.json`,
  `data/phase_8_1/g4/a_luna_plain_*.meta.json`; đếm citation `[n] > 5` trong câu trả lời `g2_context10.jsonl` + `t_context10.jsonl`.

## 4. Kết quả quan sát

**Số trích trong spec khớp gói căn cứ:**

| Spec | Gói căn cứ | Khớp |
|---|---|---|
| §1 Completeness dev +0,26 [+0,08; +0,48], test +0,27 [+0,02; +0,59] | bảng G5 §1 dòng 2a: +0,261 [+0,080; +0,477]; test +0,268 [+0,024; +0,585] | ✓ (làm tròn) |
| D3 / E1 "P1 8.1 phạm sàn 2 câu" | dòng 2b: 2 câu out_of_scope bị trả lời | ✓ |
| E2 "luật prompt P2" | dòng 3b: lỗi citation 4 → 1 (phụ) | ✓ |
| §3.6 luna "~3,5 s / câu" | dòng 8: "+3,5 s/câu" | ✓ số, nhưng cấu hình khác — M1 |
| E3 "pool 100", luật bỏ sớm | dòng 6 / §3 dòng 4: native p100 +4 / −1 | ✓ |
| §4 kiểm cứng `settings_loader.py:77` | code: `if generation.get("max_context_documents") != 5: raise` | ✓ |
| B1.2 so với G2.1a 176 câu | `g2_context10.jsonl` 120 + `t_context10.jsonl` 56 | ✓ |
| B1.2 mốc `cefb2d1a…` 176 câu | manifest: 158 dòng | ✗ — m1 |
| §7 B1 ~0,04 USD | G2.1a: 0,00019–0,00021 USD / câu × 176 ≈ 0,035 + pilot | ✓ |
| §7 E3 ~0,05 USD | luna top-10 0,00029 USD / câu; pool 100 chưa đo | ✗ — M1 |

**Tiêu chí B1.2:** đo được; đủ chặt về sàn (0 OOS bị trả lời, 0 lỗi kỹ thuật). Phần "không khác (CI chứa 0)" là định nghĩa
"không khác" của `run-experiment` §3.3 nên hợp luật, nhưng là phép kiểm yếu cho câu hỏi "runtime có giống harness không" — m2 đề
xuất phép kiểm tất định bổ sung. **E1:** sàn, chỉ số quyết, mức tụt đều có; số cụ thể để plan (§3.5) — hợp lý. **E2:** như E1;
chỉ số quyết đếm bằng code. **E3:** xem M1, M2. **Luật dừng 3.4:** M3, M4.

**Ranh giới:** không thấy chỗ spec cho mở câu kín ngoài B3; Qdrant chỉ đọc; paid chỉ `gpt-6-luna`; B/C không commit — khớp
`Session_Prompt.md` §4–§5.

## 5. Giới hạn hoặc phần chưa chạy

- Số tiền / độ trễ E3 pool 100 ở M1 là *suy ra* từ token G4 × 10, chưa đo (đo là việc của plan E3, có pilot).
- B không đọc report G2 / G4 (ngoài gói); số G4 lấy từ metadata trong `data/phase_8_1/g4/`.
- B là người đã chạy G2 / G4 ở 8.1 nên biết dữ liệu đó; đây cũng là lý do M3 (d) đề nghị người tóm nhãn không phải người thấy điểm
  judge.
- Không review độ hợp lý của thứ tự D3 hay phạm vi D1 — đó là quyết định User đã chốt.

## 6. Decision và bước tiếp theo

**changes_requested** — 4 major (M1–M4), 5 minor (m1–m5). Cả bốn major là sửa chữ trong spec, không cần chạy gì thêm; không có
blocker, không có vi phạm quyền.

Correction cho A (người viết spec):
- Sửa spec theo tiêu chí đóng M1–M4; minor sửa cùng lượt nếu tiện (không mở vòng riêng).
- Bản mới có sha mới; B kiểm lại **phần đổi** + §3.4, §5 B1/B2, §7 (dùng lại các kiểm số ở §4 bảng trên vì gói căn cứ không đổi).
- Giữ nguyên: D1–D5, phạm vi §4 "Ngoài", ranh giới câu kín.

Sau khi B kiểm lại đạt: A trình User duyệt spec một lần (sha). Phase 8.2 vẫn chưa được giao việc thực thi cho tới lúc đó.

## 7. Vòng 2 — kiểm phần sửa (bản 2 `f5fd17418c41`)

Người kiểm: B (`hue-rag-de`) · 2026-10-25 16:16 +0700 (`date`) · 0 USD, chỉ đọc. Gói căn cứ không đổi ⇒ dùng lại các kiểm số ở §4
(bảng khớp số). Đọc lại toàn bộ spec bản 2 (153 dòng; sha kiểm trước và sau khi đọc đều `f5fd17418c41`). Lệnh chạy lại vòng này
dùng `uv run python -I` (A nhắc: vòng 1 §3 dùng `python3 -I` — sai `Session_Prompt.md` §10; chỉ đọc JSON, không đổi kết quả,
ghi nhận để lần sau làm đúng).

### 7.1 Finding vòng 1

| Finding | Chỗ sửa ở bản 2 | Kiểm | Trạng thái |
|---|---|---|---|
| M1 E3 căn cứ luna | §3.6 (số 3,3–3,6 s là xếp 10 đoạn, N > 10 chưa đo), bảng B2 "Lý do tách", §7 ước E3b *suy ra* + dừng hỏi User | số khớp `a_luna_plain_*.meta.json`; N 30 ≈ 0,15 / N 100 ≈ 0,26–0,35 USD hợp tính (xem m7) | **đóng** |
| M2 E3 gộp 2 thay đổi | bảng B2 tách E3a (pool 100 không rerank) / E3b (+ luna N > 10); luật bỏ sớm cho cả hai | đúng tiêu chí đóng | **đóng** (m6 nhỏ về cách đếm cho E3b) |
| M3 luật dừng 3.4 | §3.4: Completeness, file `judge/` + `judge_test/`, ≥ 5 cặp quyết, < 5 ⇒ "chưa rõ" ⇒ trình User, cặp judge hòa báo số (≥ 1/2 ⇒ "judge kém nhạy"), sub-agent mới tóm nhãn, A ghép khóa sau | đủ 4 ý tiêu chí đóng | **đóng** |
| M4 mù X / Y | §3.3: đánh số lại citation 1..k, chỉ hiện nguồn được trích, kiểm bằng code trong report B0; §8 thêm rủi ro | B đếm lại (`uv run python -I`, 176 câu G2.1a): **0** câu trích > 5 nguồn khác nhau, 25 câu có `[n]` > 5 ⇒ đánh số lại đủ che — khớp A | **đóng** |
| m1 158 câu + NFD live | B1.2 dòng 1 và dòng 4 | khớp manifest | **đóng** |
| m2 kiểm tất định + A/A | B1.2 dòng 2–3 | `top_chunk_ids`, `context_sources`, `input_tokens` có ở **176 / 176** dòng G2.1a (kể cả 18 câu OOS, 10 id mỗi câu), 0 dòng lỗi ⇒ tiêu chí đo được | **đóng** |
| m3 test ghim 5, chỗ NFC evaluator | §4, §3.2 | đúng | **đóng** |
| m4 D4 vs skill §4 | D4 | đúng | **đóng** |
| m5 tiền B3, commit mốc | §3.8 `f26485b` + worktree, §7 B3 ~0,015 | đúng | **đóng** |

### 7.2 Finding mới (do phần sửa sinh ra — dòng E3a mới có ở bản 2)

**N1 (major) — E3a vào chatbot chỉ dựa trên số tầng tìm kiếm; thiếu sàn từ chối câu ngoài phạm vi và mức tụt ở câu trả lời.**
- Vị trí: §5 bảng B2 dòng E3a (sàn "0 câu mất đoạn đúng khỏi context", chỉ số quyết tầng tìm kiếm, mức tụt chỉ "latency (ms)"; câu
  trả lời "nếu đo tiếp"); dòng "E2, E3a thắng ⇒ A đưa vào (D4)".
- Yêu cầu: `run-experiment` §1.3 (sàn gồm "từ chối đúng `out_of_scope` giữ nguyên"; mức tụt cho lỗi citation, từ chối nhầm…);
  §4 (đủ ba điều mới là "tốt hơn"). E1, E2 đều có sàn OOS; E3a thì không.
- Bằng chứng / lập luận: E3a đổi 10 đoạn đưa model ở **mọi** câu, kể cả 18 câu OOS (G2.1a có `top_chunk_ids` cho cả 18 câu đó), nên
  câu trả lời có thể đổi ở cả 176 câu; chỉ số quyết đếm trên 32 câu dev có đoạn đúng. 8.1 G1 / G3 đã thấy tầng tìm kiếm và câu trả
  lời không luôn cùng chiều (bảng G5 §1 dòng 1: đoạn to tìm thấy nhiều hơn nhưng kém hơn ở context). Lượt sinh 176 câu ≈ 0,04 USD
  (G2.1a 0,0002 USD / câu).
- Tác động: theo D4, A có thể đưa pool 100 vào chatbot mà chưa ai kiểm câu trả lời / từ chối OOS trên chatbot mới.
- Tiêu chí đóng: dòng E3a ghi: trước khi vào chatbot phải có lượt sinh (dev + test) với sàn **0 câu OOS bị trả lời** và mức tụt cho
  Completeness / lỗi citation (plan ghi số), chấm cùng lượt mù với mốc B1; §7 ghi tiền lượt đó (E3a không còn "0").

**m6 (minor) — luật bỏ sớm cho E3b nên đếm trong N ứng viên luna thấy, không phải pool 100.** Luna chỉ xếp lại N đoạn đầu ⇒ câu
cứu được = đoạn đúng nằm trong N đầu nhưng ngoài 10 đoạn đưa model. Với N 30, đếm theo pool 100 có thể đếm thừa. Đóng: câu cuối
luật bỏ sớm ghi "có trong N ứng viên đầu" cho E3b.

**m7 (minor) — ước E3b chỉ tính bước rerank.** `run-experiment` §1.3: USD / câu tính đầu–cuối gồm rerank + sinh. Thêm sinh
≈ 0,0002 USD / câu ⇒ N 30 ≈ 0,19 USD / 176 câu (không đổi kết luận "dừng hỏi User nếu vượt trần còn lại"). Đóng: §7 ghi gồm cả sinh.

### 7.3 Kết luận vòng 2

**changes_requested** (vòng 2 / tối đa 4) — 1 major mới (N1), 2 minor (m6, m7); 4 major + 5 minor vòng 1 **đã đóng**. N1 là sửa chữ
(thêm sàn OOS + mức tụt + tiền cho E3a), không cần chạy gì. Sửa xong: B kiểm lại dòng E3a, luật bỏ sớm, §7; phần còn lại dùng lại
kết quả vòng này.

## 8. Vòng 3 — kiểm phần sửa (bản 3 `dabae90b2b60`)

Người kiểm: B (`hue-rag-de`) · 2026-10-25 16:20 +0700 (`date`) · 0 USD, chỉ đọc. Kiểm sha (`dabae90b2b60`, khớp tin A); đọc dòng
trạng thái, §5 B2 (bảng E1–E3b, luật bỏ sớm, lý do tách, luật đưa vào chatbot), §6, §7, §8, §9. Bản 3 dài 154 dòng, bản 2 153 dòng:
+1 dòng khớp câu E3b mới trong luật bỏ sớm. B không giữ bản sao byte của bản 2 nên không diff byte được; các mục A không nêu
(§1–§4, B0, B1) B chỉ lướt lại, không thấy đổi. Dùng lại kết quả vòng 2 cho phần không đổi (gói căn cứ không đổi).

| Finding | Chỗ sửa ở bản 3 | Kiểm | Trạng thái |
|---|---|---|---|
| N1 E3a thiếu sàn OOS / mức tụt câu trả lời | bảng B2 dòng E3a: sàn thêm "0 câu out_of_scope bị trả lời"; "trước khi vào chatbot: lượt sinh dev + test, chấm cùng lượt mù với mốc B1"; mức tụt Completeness, lỗi citation (số câu), latency; §7 E3a ~0,04 | đủ tiêu chí đóng; E3b cũng có sàn OOS | **đóng** |
| m6 luật bỏ sớm E3b | "thiếu đoạn đúng trong 10 đoạn đưa model nhưng **có trong N ứng viên đầu**, trên mốc tốt hơn giữa B1 và E3a" | đúng | **đóng** |
| m7 ước E3b gồm sinh | §7: + ~0,0002 USD / câu ⇒ N 30 ≈ 0,0011 USD / câu ≈ 0,19 USD; N 100 ≈ 0,30–0,39 USD | tính lại: 0,0009 + 0,0002 = 0,0011 × 176 ≈ 0,194; (0,26–0,35) + 0,035 ≈ 0,30–0,39 ✓ | **đóng** |

Tổng ước (*suy ra*): B1 0,04 + E1 0,05 + E2 0,05 + E3a 0,04 + B3 0,015 ≈ 0,20 USD; thêm E3b N 30 ≈ 0,19 ⇒ ≈ 0,39 ≤ trần 0,5;
N 100 có thể vượt phần còn lại — spec đã ghi dừng hỏi User. Không có finding mới.

Ghi chú cho plan E3b (không phải finding, không cần sửa spec): cột mức tụt của E3b ghi latency, USD / câu; plan E3b nên ghi thêm
Completeness / lỗi citation (như E3a) vì E3b đổi câu trả lời. Plan có review theo §3.5 nên sẽ được kiểm ở đó.

### 8.1 Kết luận vòng 3

**ready_for_user_confirmation** — mọi finding (vòng 1: M1–M4, m1–m5; vòng 2: N1, m6, m7) đã đóng; 0 blocker / 0 major / 0 minor
còn mở. Spec là việc rủi ro cao ⇒ A trình User duyệt **một lần bản sha `dabae90b2b60`**; sửa sau đó là bản mới (`WORKFLOW.md` §9.1).
Phase 8.2 chưa giao việc thực thi cho tới khi User duyệt.
