# Review: plan Phase 8.2 §10 — K1, pool dense 30 → 100

Decision: **changes_requested** (0 blocker / 1 major / 4 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-b5`)
Date: 2026-10-26 21:39 +0700 (`date`)
Bản được kiểm: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k1_plan.md` sha `ad71594e17e7` (B, chưa commit)
Căn cứ dùng: đúng mục "Căn cứ để review" của plan.
1. Spec §10.2–§10.4. C đọc bản **đã duyệt** `09e8f3932ede`, không phải bản `7ea7ed3a1600` plan ghi (xem m-1).
2. `phan_loai_loi_B.md` §2, §3.2, §3.4.
3. `g1_retrieval.py:161-222`, `:243-268`.
4. B1 §4 (`git show p82-b1:…/phase_8_2_b1_implementation.md`).

Tính lại từ `b42_per_case.jsonl` (sha `79e4ba43b38e`), chỉ đọc, `uv run`, 0 USD. C không dùng tin nhắn của B. Câu trả lời của A cho §7 có trong
`CURRENT_HANDOFF.md` dòng C41; C dùng nó vì A ghi rõ là quyết định, không phải căn cứ của người viết.

## 1. Phạm vi đã review

Toàn bộ plan (148 dòng): lớp bài toán, giả định, mốc M1 / M2, thay đổi harness, YAML, luật giữ, cỡ mẫu, lệnh, tiền, dừng, §7, đầu ra.
Đối chiếu từng tiêu chí với spec §10.2–§10.4.

## 2. Findings

### M-1 (major) — Xác nhận trên test thiếu mức tụt của tầng trả lời

- **Vị trí:** plan §4 YAML, các dòng tầng trả lời: `set: dev chính 88` cho Completeness / Accuracy / từ chối nhầm. Luật giữ bước 2–3: test chỉ
  đếm "0 câu mất / 15" của tầng tìm. Bước 3 chỉ nói "đạt sàn + mọi mức tụt", mà mọi mức tụt đều ghi trên dev.
- **Yêu cầu:** spec §10.2: "xác nhận trên test = **'không làm hỏng'** (sàn + **mức tụt như luật tương ứng**)".
- **Bằng chứng:** lượt sinh của plan có chạy test (`test_pilot` / `test_rest`, §5), nhưng không có tiêu chí nào cho Completeness, Accuracy hay
  từ chối nhầm trên 41 câu test chính. B1 §4 chỉ có A/A cho 176 câu và dev chính; **không có A/A riêng cho test chính**.
- **Tác động:** K1 có thể làm tụt câu trả lời ở test mà vẫn được ghi "tốt hơn (tạm)". Đây đúng là chỗ spec dùng test để chặn.
- **Tiêu chí đóng:** YAML thêm các dòng `set: test chính 41`, gồm số câu Completeness / Accuracy tụt ≤ A/A test + 3 và từ chối nhầm ≤ A/A test
  + 1. **A/A test tính và ghi trước khi đo**, từ lượt B1 ↔ G2.1a đã chấm cùng lượt mù ở `data/phase_8_2/b1/judge/`, 0 USD. Luật giữ bước 3
  ghi rõ "dev **và** test".

### m-1 (minor) — Plan dẫn spec bản working tree, không dẫn bản đã duyệt

- Plan "Căn cứ" 1 ghi sha `7ea7ed3a1600`. A đã duyệt `09e8f3932ede`. Bản duyệt chỉ sửa n-1 → n-3: K3 "chỉ khi K1 không đủ", p K2 0,026, R1 quyết
  bằng USD. Không đổi gì của K1, nhưng plan phải trỏ đúng bản duyệt.
- **Tiêu chí đóng:** đổi sha thành `09e8f3932ede`; bỏ câu "C đang kiểm vòng 2".

### m-2 (minor) — Đưa câu trả lời của A cho §7 vào plan

- A trả lời (handoff dòng C41):
  1. sàn 120 / 168 chỉ áp cho khâu trả lời, với K1 chỉ theo dõi;
  2. ngưỡng 5 / 0 cố định;
  3. quyền ghi khi duyệt sha.
- Plan còn để dạng câu hỏi; YAML chưa có dòng theo dõi 120 / 168.
- **Tiêu chí đóng:** YAML thêm `{name: 120 / 168 trả lời hay từ chối + context có fact không, role: watch}`; §7 ghi "A đã trả lời", kèm 3 ý.

### m-3 (minor) — Latency: "trung vị chênh" nhẹ hơn chữ của spec; chưa ghi nhiễu đo

- Spec luật (i): "latency thêm ≤ 50 ms / câu". Plan dùng **trung vị** chênh theo câu; p95 chỉ theo dõi. Nếu pool 100 làm chậm một số câu (BM25
  mã hóa 100 đoạn), trung vị có thể đạt dù trung bình hoặc p95 vượt.
- Thứ tự đo base → k1 → base → k1 đã cho sẵn A/A latency (base ↔ base) mà không tốn thêm.
- **Tiêu chí đóng:** tolerance dùng **trung bình** chênh theo câu, hoặc cả trung vị **và** p95 ≤ +50 ms. Report ghi chênh base ↔ base làm nhiễu.

### m-4 (minor) — Theo dõi số câu đổi tập 10 đoạn

- Đổi pool đổi điểm BM25 trong pool của **mọi** câu, không chỉ 6 câu trong trần. Số câu có tập 10 đoạn khác mốc cho biết lượt sinh dự kiến đổi
  rộng tới đâu, và giúp đọc mức tụt Completeness.
- **Tiêu chí đóng:** YAML thêm `{name: số câu đổi tập top-10 (dev 108 / test 50), role: watch}`. 0 USD, tính từ file retrieval.

## 3. Đã kiểm, đạt

- **Đổi đúng một thứ:** chỉ `candidate_pool` 30 → 100. Treatment, `rrf_k` 60, context 10 giữ nguyên. `run_config` truyền `args.pool` vào
  `candidate_pool` và `args.rrf_k` (`g1_retrieval.py:164-166`). Plan đã ghi rõ `candidate_pool` vừa là số ứng viên dense vừa là số giữ sau RRF.
- **Giả định tính lại khớp** (`b42_per_case.jsonl`):
  - dev 18 câu thiếu; 8 câu (11 fact) có fact ngoài pool 30, không tính fact "thước đo" của câu 143;
  - 9 / 11 fact có hạng dense ≤ 100;
  - **trần dev 6** (19, 22, 92, 97, 113, 168), trong đó 19 và 168 còn fact trong pool nhưng xếp sau;
  - **trần test 2** (136, 138).
- **Bẫy cột `context5_gold_*`** (`g1_retrieval.py:212`: `"context5": context_ids` lấy theo số nguồn đóng gói). Ở `811d25d` cột này là
  context 10. Plan ghi đúng; chỉ số quyết dùng `top10_gold_all`.
- **Chỉ số quyết, sàn, Holm, cỡ mẫu:** sàn "0 câu mất" trên dev nghĩa là K1 không được có câu thua ở chỉ số quyết. Cộng với họ Holm 2 cố định
  (A trả lời §7), "≥ 5 / 0" tương đương p × 2 < 0,05 (4 / 0 p 0,026; 5 / 0 p 0,008 — C38). Khớp spec §10.3. Ghi trước "chưa rõ rất có thể" là đúng.
- **`compare`** (`:243-268`) chỉ Holm khi > 1 biến thể trong cùng lần gọi. Với K1 một mình, plan áp ngưỡng cố định ngoài hàm. Đúng.
- **Mức tụt dev** khớp spec §10.2 và B1 §4: Completeness và Accuracy A/A dev chính đều 1 câu tụt ⇒ ≤ 4; từ chối nhầm A/A 0 câu đổi ⇒ ≤ 1; citation
  v2 ≤ +2; USD ≤ +20 %, 0 lần gọi API thêm.
- **Mốc M1 / M2, dùng lại câu trả lời B1** (đầu vào model giống byte, B41 T2) và **chấm lại mốc cùng lượt mù:** đúng `run-experiment` §3.1 / §3.6.
- **Tiền:** pilot ≈ 0,002 + 0,034 ≈ 0,036 trong trần 0,04 (B1 thật 0,0369 cho 176 câu). Dừng khi pilot vượt 50 %. Hợp spec §10.4.
- **Harness mới từ chối ghi đè; không sửa production / `g1_retrieval.py` / `b1.py`; không ghi Qdrant:** hợp phạm vi.

## 4. Cách người kiểm chạy lại

`uv run python -` (inline, chỉ đọc) trên `data/cai_tien_tung_khau_2026-10-26/b42_per_case.jsonl`:
- đếm câu dev / test thiếu ở context 10 (`in_ctx10`);
- lọc fact ngoài pool 30;
- trần = câu mà mọi fact ngoài pool có `dense_rank` ≤ 100.

Kết quả ở §3. Số p dùng lại từ C38 (`bootstrap_mean_diff`, seed 20261024), vì đầu vào không đổi.

## 5. Giới hạn

- Không chạy harness. `k1.py` chưa có; mới chỉ kiểm thiết kế.
- Hạng dense trong `b42_per_case.jsonl` lấy ở một `limit` cố định. Với `limit=100`, HNSW có thể lệch nhẹ (plan §1 đã ghi qua B43), nên trần là
  ước.

## 6. Decision

**changes_requested:** sửa M-1 (thêm mức tụt test và A/A test, ghi trước). m-1 → m-4 sửa cùng lượt. Ra sha mới ⇒ C kiểm phần sửa ⇒ A ghi "duyệt
bản sha".

## Vòng 2 — kiểm phần sửa (plan sha `b8f1597f6a0f`, 21:48 26/10/2026 +0700, `date`)

Decision (vòng 2): **ready_for_user_confirmation** (0 blocker / 0 major; 1 ghi chú chữ). Việc tiếp: A ghi "duyệt bản sha" (`WORKFLOW.md` §9.1).

| Finding | Sửa (plan) | Kiểm | Kết quả |
|---|---|---|---|
| M-1 | YAML thêm 3 dòng `test chính 41` (Completeness ≤ 6, Accuracy ≤ 5, từ chối nhầm ≤ +1); bảng A/A §4; luật giữ bước 3 "dev chính và test chính" | C **tính lại độc lập** từ `data/phase_8_2/b1/judge/` (map `runs` b1 / g21a, `scores_*`, split + realism, bỏ OOS): dev chính C 1/86/1, A 1/86/1, R 1/84/3; test chính C **3/38/0**, A **2/38/1**, R 2/37/2 — **khớp** bảng của B. "A/A tụt" = chiều nhiều hơn ⇒ C 3, A 2 ⇒ ngưỡng 6 / 5 đúng | **đóng** |
| m-1 | Căn cứ 1 trỏ `09e8f3932ede` (`a5cace6`) | đọc | **đóng** |
| m-2 | §7 ghi 3 ý A trả lời; YAML có dòng watch 120 / 168 | đọc | **đóng** |
| m-3 | latency = **trung bình** chênh theo câu ≤ +50 ms; p95 watch; nhiễu = base lượt 2 − lượt 1 | đọc | **đóng** |
| m-4 | watch "số câu đổi tập top-10" (dev 108 / test 50) | đọc | **đóng** |

Phần B tự thêm (§3 / §5 khớp `k1.py` trên nhánh `p82-k1`, gồm `check-base`, `latency --runs 2`, `.answers.jsonl`, tính lại citation v2 cho cả
hai lượt): thuộc phạm vi harness, không đổi tiêu chí. C **không đọc** `k1.py` (ngoài căn cứ, chưa commit). Người review report K1 sẽ đọc code.

**Ghi chú chữ: rút lại.** Vòng đầu C ghi "khối §7 bị lặp". Kiểm lại thì **sai**: `grep "^## "` cho §7 (dòng 147) → §8 (161) → "Sửa sau review
C41" (174), không có khối lặp. Khối "lặp" là do lệnh `sed` của C in chồng: mẫu `/Sửa sau review C41/` khớp cả dòng 5 ở đầu file nên in từ
đầu. B đã chỉ ra. Plan sha `b8f1597f6a0f` không cần sửa gì.
