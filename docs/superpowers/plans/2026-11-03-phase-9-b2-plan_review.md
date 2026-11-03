# Review: Phase 9 B2 plan bản 1 (B132)

Người kiểm: C (Claude Opus 5.5) — viết bộ đo B2 (C133), không code B2. Date: 09:28 03/11/2026 (`date`). Việc C135 (A giao sáng 03/11).
Plan `docs/superpowers/plans/2026-11-03-phase-9-b2-plan.md` **bản 1 sha `0cf5c194a182`** (C tính lại từ file — khớp). 0 USD.

## 1. Phạm vi đã review

- Chỉ dựa mục "Căn cứ để review" của plan: plan (toàn bộ); spec bản 9 `169c2dd5f86a` §3, §4, §5 B2, §6, §8; `data/phase_9/b2/README.md` + `c133_bo_do_b2.md`. Không đọc `STATUS_B` / tin nhắn của B.
- Lệnh chỉ đọc / tính lại từ dữ liệu, 0 USD: code `main` `f01c032` (= B1 merge) ở các chỗ plan dẫn; SDK 0.19.4 trong `.venv`; `bo_cau_b2.json`; `data/phase_9/b1/p5_judge/golden/analyze.json` (số B1 plan dẫn ở Q6).
- **D5 coi là đã biết sẽ đổi** (A: `max_turns` 4 + chuỗi "đã hết lượt tìm" ở lần `tim_kho` thứ 3, vào bản 2) — không review phần trần của D5.
- Điểm A dặn soi: D2 (đo lại P1), D3 (S-T1 ở V0), D5 / D6 [chưa chạy] (probe 0 USD trước lượt có phí — W36), D8 (chỉnh trên 43 câu dev có lộ test không), tiền 0,35–0,43.

## 2. Findings

**0 blocker · 3 major · 5 minor.**

### M-1 (major) — Q6: N_AA = 2 cũ quá nhỏ so với nhiễu sinh lại đã đo ở B1 ⇒ V1 / V3 dễ trượt S-G chỉ vì nhiễu

- **Vị trí:** §4 Q6 "V1 / V3 (không công cụ) dùng N_AA = 2 cũ"; S-G "câu tụt ≤ N_AA + 3" (spec §4).
- **Bằng chứng (tính lại từ dữ liệu):** B1 P5 (`p5_judge/golden/analyze.json`): `T1_completeness.drops` = **6**, ngưỡng N_AA 2 + 3 = 5. Ở B1, lần gọi trả lời giống byte B0 176 / 176 (plan §9 dòng cuối, B131), nên 6 câu tụt này **chỉ là nhiễu sinh lại + chấm**. Lần đó A phải dùng lại kết quả theo spec §4 "chuỗi gửi model không đổi".
  V1 / V3 làm đổi ngữ cảnh ⇒ không còn dùng lại được ⇒ phải chịu ngưỡng 5 mà nhiễu đã là 6.
- **Tác động:** Q6 có thể gỡ một biến tốt chỉ vì nhiễu (kết quả âm giả), hoặc A lại phải quyết ngoại lệ sau khi thấy số. Luật nên ghi **trước** khi đo.
- **Tiêu chí đóng:** plan ghi N_AA cho Q6 trước khi đo, bằng một trong hai cách (A chọn):
  - (a) dùng số nhiễu đã đo ở B1 P5 (6 câu tụt Đủ / 2 câu tụt Đúng, cùng thủ tục, 0 USD), ghi rõ nguồn;
  - (b) sinh A/A cho V0 (Golden lượt 2, ≈ 0,07–0,09 USD), cộng vào bảng tiền §6 và kiểm lại trần (xem m-2).

### M-2 (major) — tầng tìm V1 / V3 / V2: chưa định nghĩa câu bị định tuyến **khác `tro_ly_hue`** ghi gì vào file lượt ⇒ V0 và biến không so cùng thước

- **Vị trí:** D2 "`cau_tim` chỉ dùng khi tuyến cuối là `tro_ly_hue`"; §3 lệnh `tang_tim` ghi "đúng hợp đồng C133 (61 câu, `{case_index, top_chunk_ids[, goi_tim_kho]}`)"; Q1, Q2.
- **Bằng chứng:**
  - V0 của bộ đo (`ket_qua/v0.jsonl`, = T1) tìm bằng câu gốc **không qua định tuyến**.
  - Ở V1 / V3 / V2, định tuyến chạy với lời dặn mới. Một câu Golden có thể bị đưa sang `ngoai_pham_vi` / `tro_chuyen`; khi đó trên chatbot thật không có lần tìm nào.
  - Plan không nói harness ghi gì cho câu đó. Nếu ghi top rỗng, tầng tìm bị lẫn lỗi định tuyến mà V0 không có. Nếu quay về tìm bằng câu gốc, ta lại đo một đường không có trên chatbot thật.
- **Tác động:** số `them` / `mat` / mất đoạn đúng của Q2 có thể lệch theo cách không ai ghi trước.
- **Tiêu chí đóng:** plan ghi một luật cho tầng tìm. C khuyên: tầng tìm luôn tìm bằng `cau_tim` của biến, **bất kể tuyến**, để chỉ đo câu tìm. Lỗi tuyến đo riêng ở Q5. Ghi thêm số câu Golden trong 61 bị định tuyến khác `tro_ly_hue` ở mỗi lượt (theo dõi, Q3).
  V2 không có `cau_tim` ⇒ hợp đồng C133 giữ nguyên (không gọi ⇒ `goi_tim_kho: false`); câu bị định tuyến khác thì ghi cùng luật trên (chạy trợ lý bất kể tuyến) hoặc ghi rõ cách khác.

### M-3 (major) — D8: vòng chỉnh trên dev không chấm được bằng script C133 mà không thấy số test

- **Vị trí:** D8 "mỗi vòng 1 lượt trên 43 câu dev"; §5 bước 4 "xem số đếm `cham` trên dev (không mở kết quả test)"; §4 "Chấm tầng tìm bằng script C133".
- **Bằng chứng (đọc code `do_tang_tim.py` `04bdba9ea11a`):**
  - `score_run` dừng khi lượt thiếu câu ("lượt thiếu N câu"), vì mỗi lượt phải đủ 61 câu. Một lượt chỉ có 43 câu dev thì không chấm được.
  - Nếu chạy đủ 61 câu thì `cham` **in ra** `them_trong_12_theo_nhom.test`, `test_them_tru_mat` và `paired.test`. Người chỉnh sẽ thấy số test ở mọi vòng.
  - Chia nhóm đúng như plan ghi: 23 câu ngoài 38 = dev 15 / test 8 (C tính lại từ `split.json`).
- **Tác động:** hoặc vòng chỉnh không chạy được, hoặc lộ số test trong lúc chỉnh — đúng chỗ A dặn soi.
- **Tiêu chí đóng:**
  - **C** (người giữ bộ đo) thêm chế độ chấm chỉ nhóm dev, ví dụ `cham --nhom dev`: nhận lượt 43 câu, không in số test. Plan D8 / bước 4 dẫn chế độ đó.
  - Harness của B chạy vòng chỉnh chỉ trên 43 câu dev.
  - Kết quả test chỉ đọc ở lượt đo cuối Q2, sau dòng "Khoá".
  - C sửa bộ đo khi A đồng ý (0 USD, không chồng file B).

### m-1 (minor) — Q5: ngưỡng kín "≥ 16 / 20" không có nguồn; sàn 2 cần chấm lại phần tuyến đổi

- Plan B1 P1 quyết **≥ 90 %** đúng trên phần đã thấy và kín "không ngược chiều" (B1 kín 20 / 20). Ngưỡng 16 / 20 (80 %) lỏng hơn và chưa ghi lý do.
- **Đóng:**
  - giữ thước B1: đã thấy ≥ 90 % + sàn 1 = 0 + kín không ngược chiều so B1, và ghi rõ "ngược chiều" là bao nhiêu câu;
  - "sàn 2 không cần đo lại" chỉ đúng với câu giữ nguyên tuyến. Câu nào **mới** vào `tro_chuyen` dưới lời dặn V1 / V3 thì chấm sàn 2 cho riêng các câu đó (thường 0–vài câu).

### m-2 (minor) — tiền §6: cận dưới sai; hai mục lớn nhất dựa trên số chưa đo

- **Tính lại từ bảng §6:**
  - Đường V1 / V3 + B2b = 0,004 + 0,05 + 0,05 + 0,03 + 0,09 + 0,20 + 0,005 ≈ **0,43** ✓.
  - Đường V2 qua + không B2b = 0,004 + 0,05 + 0,05 + 0,18 + 0,005 ≈ **0,29**, không phải 0,35.
  - Số / câu từ B1 khớp quan sát: định tuyến 0,000078; một câu cả hai lần gọi 0,00042 — C134, server nhánh 03/11.
- Q6-V2 (0,18) và B2b (0,20) dựa trên "đường có công cụ ≈ 0,0005 / câu — ước, chưa đo". Lượt thứ hai của trợ lý mang cả kết quả công cụ (10 đoạn) nên có thể cao hơn. Pilot bước 3 chỉ đo **tới lần gọi công cụ đầu**.
- Nếu M-1 chọn (b) thì đường V1 / V3 + B2b ≈ 0,50 > trần 0,45.
- **Đóng:**
  - sửa cận dưới;
  - thêm pilot 10 câu **cả lượt** đường có công cụ trước Q6-V2 / Q8 (luật pilot 10 câu, `Project_Status.md` §8);
  - ghi cách xử lý trần nếu chọn M-1 (b).

### m-3 (minor) — D5 / D6 / D2: phần [chưa chạy] không chạy được ở mức 0 USD như bước 2 ghi

- Bước 2 ghi "chạy thử … đường V2 `stop_on_first_tool` và `error_handlers` với generator bắt yêu cầu". Nhưng generator chỉ bắt yêu cầu thì không trả lời model ⇒ không có lần gọi công cụ nào ⇒ `stop_on_first_tool`, vòng nhiều lượt và hết lượt **không chạy tới được**. Ở 0 USD chỉ thấy được thân yêu cầu đầu tiên (có schema công cụ).
- C đã kiểm có trong `.venv` (0.19.4): `stop_on_first_tool` (`agents/agent.py:374`), `run_error_handlers.py` có `max_turns` (`:53`), `reciprocal_rank_fusion` (`retrieval/full_corpus.py:105`). `strict_schema.py` không nhắc `maxItems` ⇒ plan đúng khi không dựa vào nó.
- **Đóng:** ghi rõ 0 USD kiểm được gì (thân yêu cầu, schema công cụ, tham số `max_turns` / `parallel_tool_calls`), và ghi lần đầu hành vi thật chạy là pilot bước 3. Hoặc dùng một `Model` giả của SDK trả về một lần gọi hàm (logic, 0 USD).

### m-4 (minor) — D5 tìm thêm: chưa ghi trần số đoạn mỗi lần / cả lượt

- "Ngân sách token = phần còn lại" đã ghi, nhưng chưa ghi lần `tim_kho` thứ 2 / 3 thêm tối đa bao nhiêu đoạn. Hôm nay `max_context_documents` 10 là trần của **một** lần dựng ngữ cảnh.
- Con số này đổi token, tiền (m-2) và cách đánh số `[11]…`.
- **Đóng:** ghi trần, ví dụ ≤ 10 đoạn mới mỗi lần và tổng ≤ 30 hoặc theo ngân sách. Test sổ nối số khoá con số đó.

### m-5 (minor) — chữ: "B2 không có phần kín" lệch Q5

- Đầu file ghi "B2 không có phần kín", nhưng Q5 dùng bộ tuyến kín 20 câu (C chạy).
- **Đóng:** sửa thành "bộ đo tầng tìm / khâu trả lời không có phần kín; Q5 dùng lại bộ tuyến kín B1".

## 3. Cách người kiểm chạy lại thật

0 USD, chỉ đọc:
- `sha256sum` plan (khớp `0cf5c194a182`).
- Đọc `full_corpus_context.py` `build(query, documents, today)`: token đếm theo `query` ⇒ **D3 đúng và cần**.
- Đếm dev / test của 23 câu ngoài 38 từ `split.json`.
- Đọc `do_tang_tim.py` (M-3).
- Đọc `analyze.json` P5 B1 (M-1).
- `grep` SDK 0.19.4 trong `.venv` (m-3).
- Cộng lại bảng tiền §6 (m-2).

## 4. Kết quả quan sát — trả lời các điểm A dặn

| Điểm | Kết luận |
|---|---|
| **D2** đo lại P1 | Có Q5. Đủ khi sửa m-1 (thước B1 + sàn 2 cho câu đổi tuyến). M-2: tầng tìm phải tách khỏi lỗi tuyến |
| **D3** S-T1 ở V0 | **Giữ.** V0 truyền câu gốc cho cả `cau_tim` lẫn `cau_hoi`. `build` chỉ dùng `query` để đếm token ⇒ ngữ cảnh + chuỗi gửi model như B1. S-T1 chỉ đi qua `search` (không đổi). Q1 + Q7 bắt được nếu sai |
| **D5 / D6** [chưa chạy] | Có bước 0 USD + pilot. Nhưng 0 USD **không** chạy tới vòng công cụ (m-3). Lần chạy thật đầu là pilot 10 câu (≈ 0,004 USD) — chấp nhận được nếu ghi rõ |
| **D8** chỉnh trên 43 câu dev | Ý đúng (15 / 8 khớp `split.json`), nhưng công cụ chấm hiện tại lộ số test hoặc không chạy với 43 câu (**M-3**) |
| **Tiền** 0,35–0,43 | Số / câu khớp B1. Cận trên 0,43 đúng, cận dưới ≈ 0,29. Hai mục lớn dựa trên số chưa đo (m-2). M-1 (b) có thể đẩy quá trần 0,45 |

Khớp spec (không finding): 4 biến + B2b đúng §5; cổng sàng + Holm chỉ báo số đúng quyết định A; sàn 55 câu; chọn một biến đứng đầu vào khâu trả lời; quyết Completeness 18 câu CI 95 % > 0 + sàn §4 trên 208;
A/A đường có công cụ cho V2 / B2b; luật cắt 16/11 + 25/11 chép đúng §6; bước 0 câu hai ý sau B2a; rà bảo mật §8 (công cụ một tham số, không URL, câu tìm không vào log).

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy code nào của B2 (chưa có).
- Không đánh giá chất lượng lời dặn V1 / V3 (chưa viết) và không kiểm phần trần D5 (A đã quyết đổi).
- Số nhiễu ở M-1 lấy từ một lượt B1, nên chỉ là một mẫu.

## 6. Decision và bước tiếp theo

**`changes_requested`** — sửa M-1, M-2, M-3 (M-3 cần C thêm chế độ chấm dev vào bộ đo, chờ A đồng ý). Minor sửa cùng bản 2. C kiểm lại phần sửa ở bản 2 (kèm D5 mới).

---

## Vòng 2 — bản 2 sha `52fd872b941f` (C135 · 09:38 03/11/2026 `date`)

Phạm vi: chỉ phần sửa. Cách kiểm: `diff` bản 1 (`git show HEAD:…` = `0cf5c194a182`) ↔ bản 2; bảng "Chỗ đổi bản 2"; kiểm lại sha các file mới dẫn (`probe_sdk.md` `2f43c894e2d5`, README `7cbc8eec3e59`, script `45e35e800500` — khớp);
cộng lại bảng tiền §6; đối chiếu plan B1 bản 2 §4 P1. 0 USD. D5 = (b) (A quyết) chỉ kiểm cho nhất quán, không review lại lựa chọn.

### Đóng finding vòng 1

| Finding | Sửa ở bản 2 | Kết luận |
|---|---|---|
| M-1 N_AA | Q6: V1 / V3 dùng số P5 B1 (`analyze.json`: Đủ 6 ⇒ câu tụt ≤ 9; Đúng 2 ⇒ ≤ 5 — C tính lại: `T1_completeness.drops` 6, `T2_accuracy.drops` 2 ✓); V2 A/A riêng | **đóng** cho Q6. Q8 ⇒ M-4 mới (A quyết) |
| M-2 tuyến ≠ `tro_ly_hue` ở tầng tìm | D2 "Ở tầng tìm": tìm bằng `cau_tim` bất kể tuyến; V2 chạy trợ lý bất kể tuyến; §3 harness có dòng `route`; Q3 đếm câu đổi tuyến | **đóng** |
| M-3 chỉnh dev lộ test | D8 + bước 4 / 5: `tang_tim --nhom dev` + `cham --nhom dev` (`45e35e800500`); cổng chỉ ở `--nhom tat_ca` | **đóng** |
| m-1 Q5 | Thước B1 P1: ≥ 90 % trên 40 đã thấy, sàn 1 = 0 / 253, kín ≥ 16 / 20 + sàn 1 kín = 0, sàn 2 chỉ câu mới vào `tro_chuyen` (so `p1_da_thay_r2.jsonl` + kín C131) | **đóng.** C nhận sai một phần ở vòng 1: "≥ 16 / 20" **có** nguồn — plan B1 bản 2 §4 P1 định nghĩa kín "không ngược chiều = ≥ 90 % − 10 điểm, tức ≥ 16 / 20"; bản 1 chỉ thiếu dẫn nguồn. Phần sàn 2 của m-1 vẫn đúng và đã sửa |
| m-2 tiền | §6 tính lại: C cộng lại từ bảng — không biến nào qua, không B2b 0,004 + 0,05 + 0,05 + 0,005 = **0,109**; + B2b 0,21 = **0,32**; V2 qua 0,004 + 0,05 + 0,05 + 0,19 + 0,005 = **0,299**; V1 / V3 + B2b 0,004 + 0,05 + 0,05 + 0,03 + 0,09 + 0,21 + 0,005 = **0,439** ✓ (≤ trần 0,45). Pilot 10 câu cả lượt trước Q6-V2 và Q8 | **đóng** |
| m-3 0 USD | Bước 2 tách: bắt yêu cầu (thân đầu) · client giả SDK trên code B2 thật (logic) · lần thật đầu = pilot | **đóng** |
| m-4 trần đoạn | D5: ≤ 10 đoạn mới / lần; V2 ≤ 20, B2b ≤ 30 / lượt; một ngân sách token chung; `n_doan_moi`; test khoá | **đóng** |
| m-5 chữ "không có phần kín" | đầu file: bộ đo tầng tìm / khâu trả lời không kín; Q5 dùng lại tuyến kín B1 | **đóng** |

Kiểm nhất quán phần D5 (b): `max_turns` 4 đúng §2 D5, §3, §8, §9. Đếm: V2 = model gọi 2 lần tìm thật + lần 3 trả "đã hết lượt" + lượt 4 viết; B2b = 1 lần code (không tính) + ≤ 2 lần model.
Khớp spec §3 "`max_turns` 3–4; `tim_kho` ≤ 2" và §5 B2b "gọi `tim_kho` thêm ≤ 2 lần". `error_handlers` đặt `fixed_outcome` + 1 `delta` khi chạm trần; không mở cổng web.

### Finding mới

**0 blocker · 1 major · 0 minor.**

#### M-4 (major — A quyết 03/11, C ghi để B sửa ở bản 3) — Q8 (B2b): mức tụt S-G phải dùng N_AA từ A/A đường có công cụ sinh ngay ở B2b, không dùng 6 / 2 của P5 B1

- **Vị trí:** §4 Q8 "sàn §4 trên 208 với **N_AA như Q6 V1 / V3 (Đủ 6 / Đúng 2)** … A/A đường có công cụ vẫn sinh … ⇒ báo số; N_AA đường có công cụ đo được **thay N_AA từ bậc sau** (B3…)"; dòng M-1 của bảng "Chỗ đổi bản 2".
- **Yêu cầu bị ảnh hưởng:**
  - spec §5 B2b: "A/A đường có công cụ ở đây: Golden sinh 2 lượt cùng cấu hình; thay N_AA (nhiễu A/A cũ) cho mức tụt S-G **từ đây**". "Từ đây" gồm cả chính phép quyết Q8, không chỉ từ B3.
  - Nhất quán với V2 ở Q6 (đường có công cụ dùng A/A riêng). Lý do A: đường có công cụ nhiều lượt nên nhiễu khác đường một lần sinh.
- **Tác động:** Q8 có thể quyết theo thước nhiễu của đường khác (6 / 2), làm luật giữ / gỡ B2b đặt sai chỗ.
- **Tiêu chí đóng:**
  - Q8 ghi trước: N_AA (Đủ, Đúng) = số câu tụt của cặp A/A Golden 2 lượt B2b, cùng thủ tục `do_cuoi.py` / `analyze.json` ⇒ ngưỡng câu tụt ≤ N_AA + 3.
  - Thứ tự: A/A sinh + chấm **trước** khi so B2b ↔ biến B2a.
  - Sửa dòng M-1 ở bảng chỗ đổi cho khớp. V0 / V1 / V3 giữ 6 / 2. Tiền không đổi (2 lượt 176 đã có trong §6 dòng B2b).

### Kết luận vòng 2

**`changes_requested`** — chỉ M-4 (một dòng Q8 + dòng bảng chỗ đổi). Mọi finding vòng 1 đóng. Bản 3 sửa M-4 ⇒ C kiểm lại riêng phần đó.

---

## Vòng 3 — bản 3 sha `efa27cb8207c` (C135 · 09:43 03/11/2026 `date`)

Phạm vi (A giao): M-4 + bảng "Chỗ đổi bản 3" (5 điểm chuẩn bị code A đã đồng ý). Cách kiểm: đọc các đoạn đổi; `diff` bản 1 ↔ bản 3, lọc mọi dòng mới không thuộc bảng chỗ đổi bản 2 / bản 3 ⇒ **không có chỗ đổi ngoài hai bảng**
(bản 2 không có bản sao để diff trực tiếp — giới hạn). Đối chiếu code `main` `f01c032`. 0 USD.

| Mục | Kiểm | Kết luận |
|---|---|---|
| **M-4** Q8 N_AA | Q8: N_AA = câu tụt Đủ / Đúng của A/A Golden 2 lượt B2b, sinh + chấm trước khi so, ngưỡng = N_AA + 3; ghi rõ không dùng 6 / 2; dòng M-1 bảng bản 2 sửa khớp ("V2 + B2b dùng A/A đường có công cụ riêng"). Tiền: 2 lượt 176 đã có ở §6 | **đóng** |
| (1) bọc công cụ ở generator | `tests/test_assistant_boundary.py:16-19`: `agents` chỉ cho `llm.generator_openai_full_corpus` ⇒ lõi đưa hàm async thường, generator bọc `function_tool` mỗi lượt — đúng ranh giới, không sửa `ALLOWED` | đạt |
| (2) cờ `hit_max_turns` | handler ở generator không thấy `trace` ⇒ trả cờ trên `GeneratedText`, lõi đặt `fixed_outcome` — giữ một chỗ quyết outcome ở lõi | đạt (m-6) |
| (3) D10 token = tổng mọi lượt | `generator_openai_full_corpus.py:305-314` đúng chỉ lấy `raw_responses[-1]` ⇒ thiếu token các lượt gọi công cụ; đường 1 lần có 1 `raw_response` ⇒ số không đổi (Q7 bắt); ghi đổi nghĩa vào report + `BAO_CAO_SINH` | đạt |
| (4) đếm ngân sách đường trợ lý | `settings.yaml`: `context_limit` 16.384, `reserved_output_tokens` 2.048, `safety_margin` 512. B2b ≤ 30 đoạn nên ngân sách **có thể** chạm thật ⇒ cách đếm đúng là cần | đạt (m-7) |
| (5) nhãn `searching` | `frontend/src/App.jsx:6, :8`: `searching` "Đang tìm thông tin…", `searched` có sẵn ⇒ không sửa giao diện | đạt |

### Finding mới — 0 blocker · 0 major · 2 minor (sửa trong lúc code, không mở vòng mới)

- **m-6** — D5 (2): ghi rõ handler `max_turns` + cờ `hit_max_turns` (như `function_tool`) **dựng mỗi lượt**, không giữ trạng thái trên đối tượng generator dùng chung — server chạy nhiều câu cùng lúc, cờ trên đối tượng chung sẽ lẫn giữa hai câu.
  **Đóng:** một câu trong D5 + test 2 lượt đồng thời (một lượt chạm trần, một lượt không) ⇒ chỉ lượt chạm trần có `outcome="max_turns"`.
- **m-7** — D5 (4): test chênh ngân sách < 512 dùng client giả + tokenizer, chưa phải token thật. **Đóng:** ở pilot cả lượt (bước 6 / 8) ghi số đếm của builder ↔ `usage.input_tokens` thật của lượt viết, ít nhất 1 câu có ≥ 2 lần `tim_kho`; chênh ≥ 512 ⇒ dừng, báo A.

### Kết luận vòng 3

**`ready_for_user_confirmation`** cho plan B2 bản 3 `efa27cb8207c`. m-6, m-7 ghi trong report khi code (không cần bản 4). A duyệt sha (tính từ file).
