# Review: spec 8.2 §10 "Sửa đổi 26/10" — Bước 2 thành đợt cải tiến từng khâu

Decision: **changes_requested** (0 blocker / 4 major / 5 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-b5`)
Date: 2026-10-26 21:28 +0700 (`date`)
Bản được kiểm: `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` sha `ace705ec7142` (chưa commit), §10. §1–§9 chỉ đọc
để tìm mâu thuẫn.
Căn cứ dùng (đúng danh sách "Căn cứ để review (mục 10)"):
- `phan_loai_loi_C.md` §1, §3;
- `phan_loai_loi_B.md` §1, §3.2;
- `de_xuat_khau_tim_B.md` §3–§5;
- `de_xuat_khau_tra_loi_C.md` §1, §3–§5;
- `skills/run-experiment/SKILL.md` §1, §3, §4.

Ngoài danh sách, C mở thêm hai nguồn để kiểm một khẳng định cụ thể: `phase_8_1_g1_implementation.md` §G1.3 (nguồn số K2) và
`backend/retrieval/full_corpus.py:393` (`rrf_k` mặc định 60). Mọi số tính lại đều chạy `uv run`, chỉ đọc, 0 USD. C không dùng tin nhắn của A làm căn cứ.

**Tự kiểm phần của mình:** R1–R4, "trần 5 câu" của R2 và luật (a) "chênh TB ≥ −0,1 và số câu tụt ≤ A/A + 3" lấy từ C37 / C36 do C viết.
C chỉ đối chiếu §10 có chép đúng không (đúng). C **không** tự đánh giá lại đề xuất của mình. Nếu A cần đánh giá độc lập luật (a) và R1–R4 thì
nên nhờ B.

## 1. Phạm vi đã review

§10.1–§10.6, đối chiếu với §2 (D1–D5), §5 B2, §8 của bản gốc. Trọng tâm A nêu:
- luật (a) / (i) có đủ để quyết không;
- sàn / Holm / test "không làm hỏng";
- mỗi biến thể có đổi đúng một thứ không;
- ước tiền;
- mâu thuẫn với §1–§9.

Q1 ("không tốn thêm tiền") A đang hỏi User nên không thành finding. `git status`: file spec sửa chưa stage; ngoài phạm vi review.

## 2. Findings

### M-1 (major) — Cỡ mẫu ghi ở §10.3 trái với luật Holm ở §10.2

- **Vị trí:** §10.3 câu cuối: "khâu tìm cần ≥ 4 thắng / 0 thua trên 40 câu; R3 ≥ 4 / 0 trên 88; R2 ≥ 4 / 0". §10.2: "trong nhánh, Holm trên
  các biến thể chạy thật".
- **Yêu cầu:** `run-experiment` §1.6: số câu phải thắng tính "kể cả Holm khi nhiều biến thể".
- **Bằng chứng** (`bootstrap_mean_diff` của harness, seed 20261024, mỗi câu ±1):
  - n 40, 4 / 0: p 0,026 ⇒ **trượt** Holm trên 2 biến thể (cần < 0,025). 5 / 0: p 0,008, qua cả Holm 3.
  - n 88, 4 / 0: p 0,031 ⇒ trượt Holm 2 và 3. 5 / 0: p 0,013, qua Holm 3.
- **Tác động:** kết quả 4 / 0 vừa "đạt cỡ mẫu" theo §10.3, vừa "chưa rõ" theo §10.2. Hai câu cùng spec cho hai kết luận. Nhánh khâu tìm có K1 +
  K2 (+ K3) chạy thật nên chắc chắn rơi vào ít nhất Holm 2.
- **Tiêu chí đóng:** §10.3 ghi số thắng cần **theo số biến thể trong họ**, ví dụ "Holm 2–3: ≥ 5 / 0". Hoặc nói rõ họ Holm chỉ gồm biến thể
  dùng luật (i) có p-value (xem m-4).

### M-2 (major) — K2 dùng lại kết quả dev đã thấy và đã trượt Holm; K2 đổi hai thứ

- **Vị trí:** §10.3 dòng K2: "native p30 k = 2 … chỉ còn **xác nhận trên test**"; cột 8.1 "dev 4 / 36 / 0 [+0,025; +0,200], không qua Holm 10
  biến thể".
- **Yêu cầu:** `run-experiment` §1.3 "không đổi tiêu chí sau khi thấy số"; §1.2 "một thay đổi mỗi biến thể"; §4 cần chỉ số quyết vượt nhiễu.
- **Bằng chứng:**
  1. K2 là biến thể tốt nhất trong 10 biến thể G1.3. Nó trượt Holm 10 nên 8.1 ghi "chưa rõ; không mở test"
     (`phase_8_1_g1_implementation.md` G1.3). §10 xếp K2 vào họ Holm mới nhỏ hơn và bỏ bước dev. Như vậy cùng dữ liệu dev, đã nhìn thấy số,
     được chấm lại bằng luật nhẹ hơn. Bước còn lại chỉ là test "không làm hỏng" (§10.2), nên **không có bằng chứng mới nào cho "tốt hơn"**.
  2. So với runtime, K2 đổi **hai thứ**: tập ứng viên (dense ∪ BM25 cả kho) **và** `rrf_k` 60 → 2 (`full_corpus.py:393`). Từng thứ riêng
     lẻ: native p30 (k 60) **mất 2 câu** đoạn đúng; runtime k = 2 cho 2 / 38 / 0 (G1.3).
- **Tác động:** A có thể tự đưa K2 vào chatbot (§10.4) chỉ dựa trên một kết quả chọn sau khi đã thấy số.
- **Tiêu chí đóng:** chọn một trong hai.
  - (a) Coi K2 là **giả thuyết mới** cần bằng chứng mới: chỉ số quyết đo trên test với CI > 0. Trần 2 / 15 câu nên gần như chắc "chưa rõ";
    ghi trước điều này.
  - (b) Ghi rõ K2 chỉ được nhận theo luật (a) (giữ chất lượng), không được nhận như "tốt hơn".

  Thêm vào đó, ghi rõ K2 là gói hai thay đổi đã đo sẵn cùng nhau, và vì sao không tách ra.

### M-3 (major) — Luật (i) không có mức tụt cho chất lượng, trong khi A được tự đưa vào chatbot

- **Vị trí:** §10.2 luật (i): quyết vượt nhiễu, latency ≤ +50 ms, không tốn thêm. Không có dòng nào về Completeness / Accuracy / từ chối
  nhầm / lỗi citation. §10.4: A tự đưa biến thể qua luật (i).
- **Yêu cầu:** `run-experiment` §1.3 (mức tụt cho phép **của từng chỉ số còn lại**); §4 điều (2).
- **Bằng chứng:** với K1 / K2, chỉ số quyết là đoạn đúng trong context 10. Theo đúng chữ §10.2, một biến thể tăng đoạn đúng nhưng làm Accuracy
  hoặc Completeness tụt vẫn đạt luật (i). "Test = không làm hỏng (sàn + mức tụt như luật tương ứng)" cũng rỗng với luật (i), vì luật (i) không
  có mức tụt nào. B43 §4 và C37 §4 có ghi mức tụt, nhưng §10 không chép sang.
- **Tiêu chí đóng:** luật (i) thêm mức tụt tối thiểu cho mọi biến thể, ví dụ Completeness và Accuracy dev chính như luật (a), từ chối nhầm
  ≤ A/A, lỗi citation v2 ≤ A/A + k. Hoặc nói rõ "plan từng biến thể ghi mức tụt; thiếu ⇒ không được duyệt sha".

### M-4 (major) — "Không chờ B0" bỏ một biện pháp giảm rủi ro của §8 mà không ghi "thay"

- **Vị trí:** §10.2: "Thí nghiệm chạy bằng harness trên mốc; **không chờ B0**". §10 mở đầu: "§1–§9 giữ nguyên, trừ chỗ mục này ghi 'thay'".
- **Mâu thuẫn:**
  - §8 dòng 1: "Judge Claude sai nhất quán ⇒ quyết sai | **B0 mốc người trước Bước 2**; luật dừng 3.4".
  - D1: "Bước 2 thử tín hiệu **trên chatbot mới**".
  - §10 không ghi thay hai dòng này. R2 / R3 (quyết bằng judge) và mọi mức tụt Completeness đều dựa vào judge mà B0 dùng để kiểm.
- **Tác động:** kết luận "tốt hơn" có thể chốt trước khi biết judge có lệch người hay không. Nếu B0 kích luật dừng 3.4 thì không có chỗ nào
  nói phải xem lại các kết luận đã chốt.
- **Tiêu chí đóng:** thêm một câu, ví dụ: "kết luận dựa judge của Bước 2 là **tạm** cho tới khi B0 xong; B0 kích luật dừng 3.4 ⇒ A trình
  User trước khi dùng các kết luận đó". Ghi rõ §10 thay §8 dòng 1 và D1 ở chỗ nào.

### m-1 (minor) — §10.5 nói đoạn đúng "không làm chỉ số quyết", nhưng K1 / K2 quyết bằng đoạn đúng

- **Vị trí:** §10.5 dòng cuối, so với §10.2 (sàn khâu tìm) và §10.3 (K1 / K2: chỉ số quyết = đoạn đúng trong context 10, theo B43 §4).
- **Tiêu chí đóng:** sửa §10.5 thành "nhãn lỗi C36 chỉ dùng để chọn biến thể và tính trần; đoạn đúng (agent gắn, User duyệt ~10 câu ở 8.1)
  là chỉ số quyết của khâu tìm — giới hạn đã biết".

### m-2 (minor) — Luật (a) bằng latency chưa nói cách gộp 2 lượt và chưa có lượt mốc

- **Bằng chứng (A/A, dev 120, tính lại từ `b1_dev.jsonl` và `g2_context10.jsonl`):**
  - USD / câu và token ra **bằng nhau** (0,0002043; 9.235 token ra) ⇒ ngưỡng 0,95 × USD nằm ngoài nhiễu. Tốt.
  - Latency harness: p50 1,77 s so với 1,69 s (**+4,6 %**), p95 3,29 s so với 2,82 s (+17 %). Ngưỡng 0,9 × p50 chỉ cách nhiễu khoảng 2 lần.
- **Vấn đề:** latency mốc trong `b1_*` đo ở một thời điểm khác (mạng / provider khác).
- **Tiêu chí đóng:** latency mốc phải đo lại **cùng phiên, xen kẽ** với biến thể. "≥ 2 lượt" thì phải ghi điều kiện, ví dụ "cả hai lượt ≤ 0,9
  ×", và ghi rõ tập câu (dev 120 hay dev chính 88). Cộng tiền các lượt mốc này vào ước §10.4 (~0,036 USD / lượt dev + test).

### m-3 (minor) — "Test = không làm hỏng" là lệch luật skill, nên để User duyệt thay vì "A chấp nhận"

- **Vị trí:** §10.2 gạch cuối: "Lệch `run-experiment` §4 — A chấp nhận".
- **Yêu cầu:** `run-experiment` §4 ("tốt hơn" chỉ đề xuất vào chatbot khi **đã xác nhận trên nhóm kiểm"); `Session_Prompt.md` §4 (không tự
  hạ tiêu chí).
- **Tiêu chí đóng:** đưa câu này vào §10.6 thành câu chờ User. Spec sửa đổi đằng nào cũng cần User duyệt, nên không tốn thêm vòng.

### m-4 (minor) — Họ Holm "theo nhánh" gộp các biến thể có chỉ số quyết khác loại

- Nhánh khâu trả lời có R1 (luật (a): chỉ số quyết là USD / latency, so tỷ lệ, không có p-value), R2 (từ chối nhầm), R3 (Completeness). Holm
  trên ba chỉ số khác nhau không có nghĩa rõ, và R1 không có p-value để đưa vào Holm.
- **Tiêu chí đóng:** ghi rõ "Holm trên các biến thể luật (i) cùng nhánh; luật (a) không vào Holm". Khi đó họ khâu trả lời = {R2, R3} ⇒ cần
  ≥ 5 / 0 (M-1).

### m-5 (minor) — Thứ tự mới thay D3 của User mà không ghi "thay"

- D3 (User chốt): E1 → E2 → E3. §10.3: R4 → R1 → R2 (= E1), E2 NOT RUN, và K song song. User 21:1x cho A tự chọn trong luật, nên có thể đã
  đủ quyền. Nhưng theo chính câu mở đầu §10, chỗ nào thay phải ghi "thay D3".
- **Tiêu chí đóng:** thêm "thay D3" kèm lý do một dòng.

### Đã kiểm, đạt (không finding)

- **Đổi đúng một thứ:** K1 (pool 30 → 100, giữ BM25 xếp lại trong pool, k 60), K3, R1, R2, R3 đúng một thứ. R4 là thước. K2 xem M-2.
- **Số trong §10.1 khớp căn cứ:**
  - 10 / 88 câu bị cờ, cả 10 thiếu bằng chứng; 20 + 9 điểm; trần +0,33 (C36 §1);
  - 18 / 40 câu, 11 fact ngoài pool / 12 fact trong pool (B42 §1, §3.2).
- **Bảng §10.3 khớp B43 §3 và C37 §3:**
  - K1 trần 6, K2 4, K3 9, ước tiền;
  - R1 +0,136 / 0,91× / 0,92×;
  - R2 trần 5, R3 trần 9, R4 2 / 5.
- **Ước tiền §10.4:** 0,07 + 0,11 + 0,04 = 0,22 USD. Cộng phần mốc latency (m-2) thì vẫn < 0,5 − 0,037.
- **Sàn chung:**
  - 0 / 18 out_of_scope;
  - 0 câu mất đoạn đúng;
  - 120, 168 vẫn từ chối (đúng như C36 §3: context có 0 / 2 fact);
  - 0 lỗi 500.

### Ngoài phạm vi (ghi cho A)

- Căn cứ B42 §3.2 liệt kê hạng của "11 fact ngoài pool" nhưng có **12 giá trị** ở mỗi dòng: dense 10 số + 2 "> 300"; BM25 11 số + 1 "> 300".
  Không ảnh hưởng §10 (chỉ dùng số 11 / 12 fact), nhưng B nên sửa.

## 3. Cách người kiểm chạy lại thật

Từ `backend/`, `HF_HUB_OFFLINE=1 uv run python -` (inline, không lưu file):
- `bootstrap_mean_diff` (seed 20261024, 10.000 vòng) cho n 40 / 88 với 4 / 0, 5 / 0, 6 / 0, 5 / 1, so ngưỡng Holm 2 / 3;
- USD / token ra / p50 / p95 từ `data/phase_8_2/b1/b1_dev.jsonl` so với `data/phase_8_1/g2/g2_context10.jsonl`.

Đọc `phase_8_1_g1_implementation.md` G1.3 và `full_corpus.py:393`. Không gọi API, không ghi dữ liệu.

## 4. Kết quả quan sát

Như §2 (số p, CI, latency A/A). Không có kết quả paid.

## 5. Giới hạn hoặc phần chưa chạy

- C viết C37 (R1–R4, luật (a) bản đề xuất), nên phần đó không được kiểm độc lập ở review này (xem đầu file).
- C không đọc plan E1 / B1 report ngoài căn cứ. Câu "plan E1 sửa: …" ở §10.3 chỉ đối chiếu với C37 §3.

## 6. Decision và bước tiếp theo

**changes_requested.** A sửa M-1 → M-4 (mỗi chỗ một câu hoặc một dòng bảng); m-1 → m-5 sửa cùng lượt hoặc A quyết. Ra bản sha mới ⇒ C kiểm phần
sửa ⇒ A ghi "duyệt bản sha" ⇒ trình User (§10 đổi luật nhận và thay một phần D1 / D3 / §8, nên cần User duyệt một lần, kèm Q1).

## Vòng 2 — kiểm phần sửa (spec sha `7ea7ed3a1600`, 21:34 26/10/2026 +0700, `date`)

Decision (vòng 2): **ready_for_user_confirmation** (0 blocker / 0 major; 3 ghi chú chữ không chặn). Phần User quyết lúc 21:3x (Q1 "không thêm
lần gọi API, USD / câu ≤ +20 %"; nguyên tắc "chất lượng cần thiết trước, tối ưu hiệu suất sau" ⇒ thứ tự R4 → R2 → R3 → R1): C chỉ kiểm §10.2,
§10.3 và §10.6 ghi **nhất quán với nhau**. C không thấy lời User gốc nên không kiểm được câu chữ có khớp lời User không.

Đọc `git diff docs/` (§10, +86 dòng so với `5e6936b`). Sha file lúc đọc: `7ea7ed3a1600`.

| Finding | Sửa ở | Kết quả |
|---|---|---|
| M-1 cỡ mẫu / Holm | §10.3 cuối: 4 / 0 p 0,026 / 0,031 trượt ngưỡng đầu Holm 2; K1 ≥ 5 / 0 trên 40, R3 ≥ 5 / 0 trên 88, R2 5 / 5 | **đóng**. Số khớp lần tính của C (5 / 0: 0,008 / 0,013). R2 5 / 0 trên 88 (nhị phân) p 0,013 < 0,025 ⇒ qua |
| M-2 K2 | §10.3: K2 **NOT RUN**, ghi lý do (chọn lại vì may, hai thay đổi, `full_corpus.py:393`) | **đóng** |
| M-3 mức tụt luật (i) | §10.2: Completeness / Accuracy dev chính số câu tụt ≤ A/A + 3; từ chối nhầm ≤ A/A + 1; citation v2 ≤ +2 | **đóng** — test "không làm hỏng" nay có nội dung với cả hai luật |
| M-4 B0 | §10.2: "thay §8 dòng 1 và D1 cho mục 10"; kết luận judge **tạm** tới B0 + luật dừng 3.4 | **đóng** |
| m-1 | §10.5 dòng cuối: đoạn đúng **là** chỉ số quyết khâu tìm, ghi giới hạn | **đóng** |
| m-2 | §10.2 luật (a) và (i): latency đo cùng phiên, ≥ 2 lượt | **đóng** (xem n-3) |
| m-3 | §10.6 Q2 chờ User | **đóng** |
| m-4 | §10.2: Holm chỉ luật (i); họ {K1, K3}, {R2, R3}; R1 ngoài họ | **đóng** |
| m-5 | §10.3: "thay D3 cho Bước 2" | **đóng** |

Tiền §10.4: 0,036 + 0,11 + 0,04 = 0,186 ≈ 0,19 USD — đúng.

**Ghi chú chữ (không chặn, A sửa khi tiện):**
- **n-1:** dòng K3 còn ghi "chỉ khi **K1 / K2** không đủ". K2 đã NOT RUN ⇒ "chỉ khi K1 không đủ".
- **n-2:** dòng K2 ghi "dev 4 / 36 / 0 [+0,025; +0,200], **p 0,031**". 4 / 36 / 0 là n 40 nên p là **0,026**; 0,031 là của n 88. Câu cuối §10.3 đã
  ghi đúng 0,026.
- **n-3:** nếu R1 chọn latency làm chỉ số quyết thì cần ≥ 2 lượt mốc + ≥ 2 lượt biến thể cùng phiên. Khoảng +0,07–0,1 USD đó chưa nằm trong
  ước 0,19. Dùng USD làm chỉ số quyết thì không tốn thêm. Vẫn trong trần 0,5.

Bước tiếp: A ghi "duyệt bản sha" sau khi trình User (§10 thay D1 / D3 / D4 / §8 dòng 1 cho Bước 2, kèm Q2). Lưu ý tự kiểm vẫn như vòng 1:
R1–R4 và luật (a) bản đề xuất do C viết.
