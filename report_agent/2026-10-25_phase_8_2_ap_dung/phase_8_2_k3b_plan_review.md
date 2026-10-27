# Review: Phase 8.2 §10 K3b — plan "luna chọn 10 đoạn từ pool 30, hai nhánh mức suy luận"

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 4 minor) — tiêu chí, Holm, cỡ mẫu và tiền tính lại khớp; bước bù theo RRF là fallback
có lý do, có đếm, có trần, và tác hại hiện ra ở chính chỉ số quyết. A nên ghi rõ hai quyết định ở §6 khi duyệt.
Người kiểm: C (Claude Opus 5.5, `hue-rag-5b`) · Việc: C50 (A giao 27/10)
Date: 2026-10-27 09:18 +0700 (`date`)
Canonical guide: spec 8.2 §10.2–§10.4 (bản `cd910c4c4169`); K3 plan `0a6370204c7d` §1, §4, §6; `Session_Prompt.md` §7
Plan được review: `phase_8_2_k3b_plan.md` sha **`4f92e478cb65`** (C tính từ file lúc bắt đầu: khớp A)

## 1. Phạm vi đã review

Chỉ dựa trên mục "Căn cứ để review" của plan (WORKFLOW §9.1); không đọc STATUS_B hay tin của B.
- Đọc hết plan; spec §10.2–§10.4; K3 plan §1, §4, §6; report K3 `origin/p82-k3` §4.1, §4.3–§4.5, §5 và review C49 §5–§6; `g4_rerank.py` 63–93 và
  `generator_openai_full_corpus.py` 94–118 ở `811d25d`; harness `k3.py` trên `origin/p82-k3`.
- Tính lại bằng lệnh chỉ đọc, 0 USD (chạy từ `backend/` working tree chính, `PYTHONPATH=. uv run python -c …`): `bootstrap_mean_diff` / `holm_adjust`
  (seed 20261024) trên vector 40 câu; trần trên `data/phase_8_2/k3/base_{dev,test}.jsonl`; token / USD / `rerank_ms` / dạng đầu ra từ
  `l1_pilot.jsonl` + `l1_rest.jsonl`. Không đọc câu test theo từng câu, không mở câu kín.

## 2. Findings

Không có blocker hoặc major.

### m-1 — tiêu đề §2 "không phải fallback che lỗi" mâu thuẫn với chính đoạn "Bước (d) là fallback"; và K3b nới một sàn của K3 thành mức tụt mà không nói thẳng

- **Vị trí:** §2 tiêu đề; §2 loại 3; §4 YAML (mức tụt sai hợp đồng ≤ 4 / 95).
- **Bằng chứng:** K3 plan §4 ghi sàn "lỗi đầu ra luna (**không phải hoán vị** 1..30 / API lỗi / bị cắt) — floor 0", và K3 dừng đúng vì dạng "không phải hoán vị"
  (câu 173). K3b giữ API lỗi / bị cắt là sàn, nhưng chuyển "danh sách sai" sang **mức tụt** (≤ 4 / 95) có sửa tất định. Đây là thay đổi hợp lệ vì K3b là
  biến thể mới, plan mới, ghi trước, vòng 2 / 3 (§6.6) — nhưng plan chỉ nói gián tiếp.
- **Tác động:** người đọc report sau này (A, User) có thể không thấy rằng điều làm K3 "kém hơn" nay không còn là sàn. Không đổi kết quả, nhưng đúng loại
  thay đổi `Session_Prompt.md` §4 yêu cầu phải minh bạch.
- **Tiêu chí đóng:** sửa tiêu đề §2 (bỏ "không phải fallback che lỗi", ví dụ "có đếm, có trần") và thêm một câu ở §2 hoặc §4: "Sàn K3 'không phải hoán vị'
  thành mức tụt ở K3b; lý do: …; A duyệt cùng sha." Spec §10.2 sàn chung "0 lỗi kỹ thuật / 500" vẫn đạt vì người dùng không nhận lỗi.

### m-2 — lý do "cách trực tiếp không đủ" bỏ sót phương án đơn giản hơn: vi phạm hợp đồng ⇒ dùng nguyên top-10 RRF của câu đó

- **Vị trí:** §2 "Bước (d) là fallback" gạch 2 ("Dừng cả câu thì chatbot không có top-10").
- **Bằng chứng:** có phương án thứ ba plan không nêu: câu vi phạm ⇒ dùng **nguyên** top-10 RRF (= mốc) cho câu đó. Tác hại bị chặn đúng bằng mốc, không trộn
  hai thứ tự. Plan chọn (a)–(d) thì giữ được các số luna hợp lệ — *suy ra* tốt hơn khi luna trả 1–9 số hợp lệ, nhưng phức tạp hơn một bậc.
- **Tác động:** nhỏ; ở K3 không lần gọi nào cần bù (mọi lần trả ≥ 29 số hợp lệ, C đếm 40 / 40), nên hai phương án gần như chắc cho cùng kết quả ở K3b.
- **Tiêu chí đóng:** thêm một dòng nêu phương án "nguyên RRF" và vì sao không chọn (ví dụ: giữ lựa chọn hợp lệ của luna), hoặc chọn nó nếu B thấy đơn giản hơn.
  Không bắt buộc đổi.

### m-3 — trần "≤ 5 % (≤ 4 / 95)" và "≤ 2 / 95": chưa rõ là số đếm tuyệt đối hay tỉ lệ khi nhánh có ít hơn 95 lần gọi

- **Vị trí:** §4 YAML hai dòng mức tụt; §6.2 dòng cuối ("đếm cộng dồn… > 4, hoặc bước (d) > 2").
- **Bằng chứng:** nhánh dừng ở L2 vì chỉ số quyết trượt (§6.5) có 80 lần gọi; 5 % của 80 = 4, nhưng nhánh dừng sớm hơn (pilot 10) thì 5 % = 0,5. §6.2 dùng số
  tuyệt đối, YAML ghi cả hai.
- **Tiêu chí đóng:** ghi một cách: "số đếm tuyệt đối cộng dồn trong nhánh, sai hợp đồng ≤ 4, bước (d) ≤ 2, bất kể n" (C khuyên — khớp §6.2), báo kèm k / n và CI.

### m-4 — K3b-m gần như không cải thiện "giá", nên luật chạy nhánh m có thể gọn hơn

- **Vị trí:** §1 "Thứ tự"; §5 dòng 1m–4m.
- **Bằng chứng (C tính trên 40 lần gọi K3):** `rerank_ms` gần như tuyến tính theo token ra — tương quan **0,94**, ≈ 9,2 ms / token + 1,8 s. *Suy ra* (ngoại suy, chưa
  đo): K3b-m (ra ≈ 410, G3) ≈ **5,6 s** — như K3; K3b-n (ra ≈ 25–40) ≈ **2,1 s**. Vậy K3b-m chỉ sửa hợp đồng lỗi, không sửa vấn đề giá làm K3 không trình User
  được (§1 lý do 1).
- **Tác động:** khi K3b-n **đạt luật giữ nhưng dưới trần** (ví dụ 6 / 0), plan vẫn chạy K3b-m (0,058 USD) chỉ để đo "bỏ suy luận mất bao nhiêu". Đó là thông
  tin có ích cho User (đánh đổi chất lượng ↔ tốc độ), nên giữ được — nhưng là lựa chọn của A, không phải hệ quả bắt buộc.
- **Tiêu chí đóng:** ghi kèm ước latency K3b-m ≈ K3 (*suy ra*) ở §1 hoặc §5, để A chọn khi duyệt Q1: (i) như plan; hoặc (ii) chỉ chạy K3b-m khi K3b-n kém hơn /
  chưa rõ (không chạy khi K3b-n đạt dưới trần). Không bắt buộc đổi.

## 3. Cách người kiểm chạy lại thật

0 USD, chỉ đọc. Từ `backend/` working tree chính: `PYTHONPATH=. uv run python -c …` với `evaluation.full_corpus_eval.bootstrap_mean_diff`, `holm_adjust`
(vector 40 câu, k câu +1, còn lại 0); đọc `data/phase_8_2/k3/{base_dev,base_test,l1_pilot,l1_rest}.jsonl`; `numpy.polyfit` cho `rerank_ms` ~ `output_tokens`.

## 4. Kết quả quan sát — bốn điểm A hỏi

**(1) "Bù theo RRF" có phải fallback che lỗi không; lý do §7 đủ chưa; trần ≤ 2 / 95 hợp lý không.**
- **Là fallback, nhưng không che lỗi:** mọi lần dùng được đếm (`n_filled_from_rrf`, `contract_violation`), có trần ghi trước, vượt trần ⇒ nhánh **kém hơn**; và chỉ
  số quyết + sàn tính trên top-10 **sau** bước sửa, nên nếu bù làm mất đoạn đúng thì sàn bắt. Lỗi kỹ thuật thật (API, bị cắt, không parse) vẫn là sàn, không
  gọi lại, không thay RRF. Đủ năm điều kiện của `Session_Prompt.md` §7, trừ chỗ thiếu ở m-2; tiêu đề §2 cần sửa (m-1).
- **Dạng lỗi K3 (câu 173) không chạm bước (d):** C đếm 40 lần gọi K3 — số đoạn hợp lệ trả về nhỏ nhất là **29**; với đầu ra 10 số, dạng "thiếu 1 trong 30" chỉ
  rơi vào (c) (cắt về 10) và **không cần bù** (G4 đúng). Bước (d) chỉ chạy khi luna trả < 10 số hợp lệ — chưa thấy lần nào.
- **Trần ≤ 2 / 95 hợp lý:** ở mức tần suất quan sát (0 / 40 cần bù), trần không chặt; nhưng nó đặt nghĩa "ngoại lệ, không phải cơ chế chính", và report ghi
  `case_index` + số đoạn bù. Trần sai hợp đồng ≤ 4 / 95 (≈ 4,2 %) cũng hợp lý: K3 1 / 40 = 2,5 % ở dạng nặng hơn. Cần làm rõ số tuyệt đối (m-3).

**(2) Tách K3b-n / K3b-m có cần không; thứ tự đúng chưa.**
- So **mốc B1** mỗi nhánh vẫn là "một bước thêm" (spec §10.2 so cùng mốc, không so nối tiếp); hai tham số (đầu ra 10 số, mức suy luận) ảnh hưởng hai thứ khác
  nhau (hợp đồng lỗi ↔ chất lượng xếp hạng) — lý do tách của plan đúng. Gộp mà trượt thì không biết vì đâu.
- Thứ tự n trước: hợp với vấn đề K3 vướng (giá) và rẻ hơn. Không trái "chất lượng trước" vì nhánh m vẫn chạy khi n chưa tới trần, và cả hai cùng luật (i).
  Bỏ m khi n đạt **9 / 0 ổn định** là đúng (m không thể hơn ở chỉ số quyết). Xem m-4 cho lựa chọn gọn hơn.

**(3) Holm họ cố định + ngưỡng 5 / 0.**
- C tính lại (n 40, seed 20261024): 4 / 0 ⇒ p **0,0264**, Holm họ 4 {K1 0,798, K3 1, K3b-n, K3b-m 1} ⇒ **0,106** trượt; 5 / 0 ⇒ p **0,0076** ⇒ **0,0304** qua; 6 / 0 ⇒
  0,0024 ⇒ 0,0096. Nếu **cả hai** nhánh 5 / 0: Holm step-down 0,0304 / 0,0304 — cả hai qua. Khớp plan §4.
- Họ cố định gồm cả K3 (p 1, dừng) và K3b-m (p 1 khi không chạy) — bảo thủ, đúng tinh thần "cố định trước" của R2; vì "thua" = mất đoạn đúng = phạm sàn, luật thực
  tế là **≥ 5 thắng ổn định / 0 thua**, trần 9 đủ chỗ. CI 5 / 0 = [0,025; 0,225] > 0.
- Đổi chỉ số quyết `top10_gold_all` → `context_gold_all`: C kiểm ở mốc context = top-10 ở **40 / 40** dev và **15 / 15** test, nên hai chỉ số trùng ở mốc; sàn tính
  cả hai — hợp lý (Q4).
- Trần trên đúng mốc (W23): dev 9 (17, 38, 48, 67, 70, 85, 156, 159, 167), test 3 (20, 95, 130) — khớp G1. Pilot = đúng 10 câu pilot K3 (17, 22, 27, 29, 45, 48, 51, 89,
  156, 169) — khớp §5.

**(4) Ước tiền 0,040 / 0,098.**
- Token vào K3 TB **4.012,85** / lần ⇒ 0,000401 USD. K3b-n: + 25–40 token ra ⇒ ≈ **0,000416** / lần × 95 ≈ **0,0396**; K3b-m: + 410 ⇒ ≈ **0,000606** × 95 ≈ **0,0576**;
  cộng ≈ **0,097** — khớp 0,040 / 0,058 / 0,098. Đầu vào K3b đổi một câu chỉ dẫn ⇒ token vào gần như bằng K3.
- Rủi ro ước: token ra K3b-n là *ước* (G3); 8.1 G2.4 `none` ở khâu sinh vẫn ra ~54 token — nếu rerank `none` cũng còn chút suy luận, USD / lần đổi < 0,00002, không
  đáng kể. Luật pilot "> 1,5 × ước ⇒ dừng" bắt sai ước.
- Trần 0,10 (con 0,045 / 0,055) trong trần 8.2: đã dùng 0,0647 (B1 0,0369 + R2 0,0027 + K3 0,0251); + R1 ≤ 0,05 + K3b ≤ 0,10 ⇒ ≤ 0,215 < 0,5.

## 5. Giới hạn hoặc phần chưa chạy

- Chưa có harness `k3b.py` để review (plan §3 mô tả). C không kiểm `responses.parse` nhận `reasoning={"effort": "none"}` (G2 — plan kiểm ở lần gọi đầu).
- Ước latency ở m-4 là ngoại suy tuyến tính từ 40 lần gọi K3 (một model, một phiên) — chỉ để A chọn, không phải tiêu chí.
- Số 9 / 0 của K3 vẫn mang các giới hạn ở review C49 §5 (một lượt, dev đã thấy, mẫu 39).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation** — A có thể duyệt sha sau khi B sửa (hoặc A chấp nhận để nguyên) 4 minor; sửa ⇒ sha mới, C kiểm phần sửa. Khi duyệt, C đề nghị A
ghi rõ hai quyết định: (1) **nới sàn K3 "không phải hoán vị" thành mức tụt có trần** ở K3b (m-1); (2) **luật chạy nhánh m** — như plan hay chỉ khi K3b-n kém hơn /
chưa rõ (m-4, Q1 của plan). Trần 0,10 USD và chỉ số quyết `context_gold_all` (Q2, Q4): C không thấy vấn đề.

## Vòng 2 — kiểm phần sửa (bản 2 sha `57dad7150322`, C tính từ file; 09:26 27/10/2026 +0700, `date`)

Cách kiểm: `git diff HEAD -- phase_8_2_k3b_plan.md` (bản 1 `4f92e478cb65` ở `ee658bf` → bản 2 trên đĩa); `grep` tìm chỗ còn sót của bản 1 (`n_filled`, `2 / 95`,
`bước (d)`, `5 %`, `9 / 0 ổn định`): chỉ còn trong bảng "Sửa sau review C50" (đúng, là ghi chép). Quét trùng: 0.

| Finding | Đóng? | Ghi chú |
|---|---|---|
| m-1 | **đóng** | Tiêu đề §2 "có đếm, có trần"; đoạn "Đổi so với K3 — nói thẳng": sàn "không phải hoán vị" ⇒ mức tụt có trần, lý do, kết luận K3 giữ "kém hơn", lỗi kỹ thuật vẫn sàn 0 |
| m-2 | **đóng** | Chọn "sai hợp đồng ⇒ nguyên top-10 RRF": một điều kiện, tác hại chặn đúng bằng mốc, câu đó không thể thắng / thua — đúng tiêu chí "nêu phương án và lý do"; bỏ (a)–(d) và trần riêng của bước bù cho khớp |
| m-3 | **đóng** | "≤ 4 lần, số đếm tuyệt đối cộng dồn trong nhánh, bất kể n" thống nhất ở §2, YAML §4, §6.2 |
| m-4 | **đóng** | §1: nhánh m chỉ chạy khi n kém hơn / chưa rõ (A chốt); ước latency m ≈ 5,6 s, n ≈ 2,1 s ghi là *suy ra*; §5 bảng tiền và §8 Q1 sửa khớp |

**Ngoài phạm vi sửa — không đổi** (đối chiếu diff): chữ prompt rerank, chỉ số quyết `context_gold_all` + luật thắng / thua hai lượt, Holm họ cố định 4, sàn mất đoạn
đúng + sàn lỗi kỹ thuật, trần 0,10 USD (con 0,045 / 0,055), các điều kiện dừng khác, ước tiền. Không có finding mới.

**Ghi chú (không phải finding):** với m-2, dạng đầu ra của K3 (≥ 29 số hợp lệ) nếu lặp lại ở K3b sẽ thành "sai hợp đồng ⇒ RRF" (bản 1 thì cắt về 10 số luna). Prompt
K3b đòi đúng 10 số nên dạng này khó xảy ra; nếu xảy ra nhiều thì trần ≤ 4 bắt — đúng ý "hợp đồng không được thành cơ chế chính". G4 bản 2 đã ghi đúng là loại 3.

**Decision vòng 2: ready_for_user_confirmation** — A có thể ghi "duyệt bản sha `57dad7150322`".
