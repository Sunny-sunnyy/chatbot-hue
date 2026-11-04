# Implementation Report: Phase 9 B4 — hỏi lại (`hoi_lai`) — **dở: khoá 3 `7d72703` — Q1 / Q2 / Q3 / Q6 đạt đã thấy; chờ kín (C) ⇒ Q4 / Q5 / Q7 / Q8**

Người làm: B (Claude Opus 5.5, `hue-rag-32` → `hue-rag-2d` 04/11) · việc **B144 → B153** (A giao) · bản này 20:46 04/11/2026 (`date`; §2c mới) — trước 21:10 03/11/2026. **Plan nay bản 5 `acfaf8ca0df5`** (A duyệt 20:14 04/11/2026; trần B4 0,18 / dừng 0,17). Plan: `docs/superpowers/plans/2026-11-03-phase-9-b4-plan.md` bản 2 **`42fa62d2425f`** (A duyệt; Lệch Q6 chấp nhận; Q-a giữ + đo hỏi thừa; Q-b không trả lời tạm).
Nhánh **`p9-b4`** từ `main` `849005c`, worktree `/tmp/b_b4`. Commit (sau rebase lên `main` `ac46c96` — có B143 `e3cdb96`, 21:13 03/11/2026): **`c4f2b76`** (backend + test), **`86c311b`** (giao diện); trước rebase `18da59b`, `10d57c1`. Đã push (`--force-with-lease`, nhánh riêng chưa review). **Chưa merge, cờ `hoi_lai` tắt.** B4 không chạm `ROUTER_INSTRUCTIONS`.
Report tracked, repo public: không chép câu bộ đo; câu ví dụ tự viết. Dữ liệu: `data/phase_9/b4/` (private). B không mở `cau_sealed.jsonl`.

## 1. Đã làm (theo D1–D10)

| File | Thay đổi |
|---|---|
| `backend/llm/hoi_lai.py` (mới) | D2 bảng trường / giá trị / bắt buộc (khớp C143 + plan B5); D3 `loc_truong` (bỏ trường sai loại, rỗng ⇒ bắt buộc "dien", > 3 ⇒ cắt "cat"); D8 `the_hoi_lai` (dữ liệu nút + `bat_buoc`); D4 `TruongInput` (`Literal`, `extra="forbid"`) + `ghep_cau` (nhãn code, tất định; `{}` ⇒ câu gốc) |
| `backend/llm/generator_openai_full_corpus.py` | `_assistant_for(…, hoi_lai_fn)`: công cụ thứ hai `hoi_lai` + `StopAtTools(["hoi_lai"])` + lời dặn có `HOI_LAI_NOTE`; `_tools_result`: `final_output` là dict công cụ trả ⇒ `GeneratedText.clarify` (đọc **trước** khi ép `AnswerOutput`, spec §3) — thường + stream; `assistant_instructions_for(history, hoi_lai)` (ngân sách đếm đúng chuỗi) |
| `backend/llm/assistant.py` | cờ `hoi_lai`; trace `da_co_truong`, `search_query` (m-3: lần tìm đầu = câu gốc), `clarify`, `hoi_lai_raw` (tham số thô — Q2, M-1), `hoi_lai_d3`; `hoi_lai_for_turn`; chỉ đưa công cụ khi cờ bật **và** lượt chưa có trường (D4: không hỏi lại lần hai); `_finish_generated` ⇒ `outcome="hoi_lai"`, không chữ, không kiểm citation; stream không phát "đang tìm" cho `hoi_lai` |
| `backend/llm/full_corpus_prompt.py` | `HOI_LAI_NOTE` (khi nào gọi + Cách A cho câu chi phí — D7), chỉ ghép khi cờ bật |
| `backend/api/routes/chat.py` | `ChatRequest.truong`; `_model_query` (câu ghép, `co_truong`); `/api/chat` trả `clarify` (answer rỗng, không `turn_id`); stream: sự kiện `clarify` + `done` (không `turn_id`); lượt hỏi được nhớ "chỉ câu hỏi" (D5); log `hoi_lai` {loai, n, d3}, `co_truong` (số, không giá trị) |
| `backend/config/settings.yaml` | `assistant.hoi_lai: false` |
| `frontend/src/App.jsx`, `stream.js`, `index.css` | D10 thẻ hỏi lại: nhóm nút / trường (chọn một, bỏ chọn được), "(không bắt buộc)", "Gửi" chỉ bật khi đủ bắt buộc, "Trả lời luôn" (`truong: {}`); lượt ghép hiện câu gốc + "· 2 ngày · 2 người"; Thử lại giữ lựa chọn; khung nguồn ghi "Chọn thêm thông tin…" |
| `backend/tests/test_b4_hoi_lai.py` (mới, 8 test) | D3, D4; **SDK thật + client giả có kịch bản** (không mạng): dừng ngay ở `hoi_lai` (1 lần gọi), công cụ + lời dặn gửi đi, `clarify` sau D3, tham số thô; stream không "đang tìm", không `delta`; cờ tắt / lượt đã có trường ⇒ chỉ `tim_kho`, lời dặn = B3 (Q1 mức test); route `clarify` ⇒ `truong` ⇒ câu ghép tới model, không `hoi_lai`; 422 giá trị / trường lạ; log số đếm; sự kiện `clarify` |

**Lệch plan:** harness đo đặt ở `data/phase_9/b4/tools/chay_b4.py` (private, như harness định tuyến C156) thay vì lệnh mới trong `backend/evaluation/full_corpus_eval.py` (plan §3) — ít code tracked hơn, đủ cho Q2 / Q3 / Q6; ghi tham số thô + sau D3 (M-1). Lệnh `kiem` / `dem` chạy thử 0 USD (W36 4b): đọc đúng `chon_da_thay.json` C158 (`060d62a56e97`, khoá `chon`), `dem` trên kết quả giả ở `/tmp` (kiểm logic, đã xoá).

## 2. Đã chạy (0 USD)

- Test: `test_b4_hoi_lai` + `test_b3_memory` + `test_b2_tool_loop` + `test_api_chat` + `test_chat_stream` + `test_feedback` + `test_assistant_boundary` ⇒ **66 passed** (+ `test_b4` thêm 1 sau đó), 1 error = test cần khoá API (bẫy đã biết); `test_static_ui` 3 / 3; `npm ci && npm run build`.
- **Q1 (byte, `capture_all.py` B134 — thay `AsyncResponses.create`, không gọi mạng; 176 Golden + 32 an toàn + smoke = 228 ca × 2 lần gọi):** lần 1 (nhánh trước rebase ↔ cây `main`) khác ở **lần định tuyến 228 / 228**, lần trả lời giống 228 / 228 ⇒ nguyên nhân: A merge B143 vào `main` trong lúc chạy (`ROUTER_INSTRUCTIONS` main `164bd4a254e9` ↔ nhánh `fb4e1aa7f8fe`), không phải B4. Sau rebase: **giống byte 228 / 228** (`data/phase_9/b4/q1/main.jsonl` ↔ `b4_rebase_co_tat.jsonl`, `cmp`) ⇒ **Q1 PASS** — cờ tắt, chuỗi gửi model như `main`.

## 2b. Pilot + Q2 / Q3 đã thấy (B145, A giao tối 03/11; 21:39 03/11/2026) — **chưa khoá, chưa kín**

Harness `data/phase_9/b4/tools/chay_b4.py` (cờ `hoi_lai` bật ở rìa trên bản sao cờ, nhớ tắt, định tuyến theo settings), commit nhánh lúc chạy: pilot + v0 trên `86c311b`, v1 trên cây có ghi chú vòng 1 (commit sau đó `c76934c`; phần sửa m-1 chỉ chạm đường stream, harness đi đường thường). Không đo latency.

| Lượt | Ghi chú `HOI_LAI_NOTE` | Q2 thiếu hỏi đúng (tham số thô) | Q3 câu đủ bị hỏi | gần giống bị hỏi | hỏi thừa · D3 điền / cắt | USD |
|---|---|---|---|---|---|---|
| pilot 4 câu (2 thiếu · 1 đủ · 1 gần giống) | bản code `c4f2b76` | 2 / 2 | **1 / 1** (LD1 — hỏi thêm 2 trường không bắt buộc) | 0 / 1 | — · 0 / 0 | 0,0016 |
| **v0** 20 câu | như trên | **9 / 10** (trượt LT4) | **0 / 7** | 0 / 3 | 0 · 0 / 0 | 0,0124 |
| **v1** 20 câu (vòng chỉnh 1: "câu đã đủ bắt buộc thì không gọi hoi_lai chỉ để hỏi trường không bắt buộc", sha `2b62c390f2fa`) | `c76934c` | **9 / 10** (trượt LT4) | **1 / 7** (CD4) | 0 / 3 | 0 · 0 / 0 | 0,0115 |

- Ngưỡng plan: Q2 ≥ 8 / 10 — **đạt cả hai lượt**; Q3 ≤ 1 / 10 (7 đã thấy + 3 kín) — v0 0 / 7, v1 1 / 7 (còn 0 suất cho phần kín nếu giữ v1).
- **Câu đủ bị hỏi chập chờn:** LD1 bị hỏi ở pilot, không bị hỏi ở v0 / v1; CD4 không bị ở v0, bị ở v1 ⇒ vòng chỉnh 1 **không cho thấy cải thiện rõ** (quan sát trên 1 lượt mỗi bản; chưa đo A/A). Đề xuất phiên sau: đo lại v0 ↔ v1 trên 7 câu đủ × 2–3 lượt trước khi chọn bản khoá.
- LT4 (lịch trình theo sở thích ẩm thực, thiếu số ngày): model **trả lời luôn** bằng mẹo ăn uống có nguồn (3 nguồn), không hỏi — trượt Q2 nhưng không nói sai.
- Tiền B145: **0,0256 USD** (ước pilot 0,002 — đúng; mỗi lượt 20 câu ≈ 0,012, cao hơn ước 0,008 / lượt của plan — câu đủ / gần giống có lượt viết). B4 tới giờ ≈ 0,026 / 0,12.

**Review sớm C163** (`b144_review.md` "Vòng sớm" `1ccb676f475d`, 0B / 0M / 3m) — A quyết:
- **m-1** stream phát "đã tìm" cho lần gọi `hoi_lai` ⇒ **sửa xong `c76934c`** (bỏ cả `searching` lẫn `searched` khi công cụ là `hoi_lai`; test mới hỏng khi bỏ phần sửa, đạt khi có).
- **m-2** model chỉ hỏi trường không bắt buộc ⇒ câu lịch trình thiếu `so_ngay` vẫn đi tiếp ⇒ **sửa ở phiên sau**: D3 thêm "code luôn thêm trường bắt buộc còn thiếu (theo `loai`) vào thẻ" ⇒ **plan bản 3** (chỉ D3 + chỗ đổi), C kiểm, A duyệt sha lại. Q2 vẫn đếm trên tham số thô (M-1).
- **m-3** đệm token chưa đếm lược đồ công cụ `hoi_lai` ⇒ báo `usage − builder` max ⇒ **chưa có số**: harness `chay_b4.py` chưa ghi `usage_tru_builder` ⇒ phiên sau thêm trường này (như harness `chuoi` B3) rồi báo max ở lượt đã thấy.

## 2c. Phiên 04/11 (B153): chọn ghi chú ⇒ khoá 1 ⇒ Q6 phạm ⇒ khoá 2 ⇒ Q6 còn phạm (đọc chữ) — **20:46 04/11/2026**

**Code (0 USD).** D3 bản 5: `loc_truong` **luôn thêm trường bắt buộc còn thiếu**, cờ D3 là danh sách ⊂ {`dien`, `cat`} (có ca vừa thêm vừa cắt). Hằng `HOI_LAI_TOOL_OVERHEAD = 185` (A chọn (a)) — chỉ cộng vào phép đếm ngân sách khi lượt đưa công cụ `hoi_lai`. Test 69 / 69 (B2–B4, stream, feedback, assistant, context).

**Chọn ghi chú (A cho chạy thêm câu đủ):** 7 câu đủ × 2 lượt × v0 (`917621e6d1c9`) / v1 (`2b62c390f2fa`), harness `--ghi_chu` (đổi ghi chú chỉ trong tiến trình harness, kiểm sha trước khi chạy). Câu đủ bị hỏi nhầm, cộng mọi lượt đã thấy: v0 1 / 21 (+ 1 ở pilot), v1 1 / 21; Q2 9 / 10 cả hai ⇒ chênh trong nhiễu ⇒ **chọn v1** (A đồng ý). 0,0268 USD.
**Ngân sách token (m-3):** token vào thật − số bộ đếm ≥ 185 ở 28 / 28 lượt (đúng 185 khi không tìm thêm), max 639 ≥ 512 ⇒ báo A ⇒ hằng 185 ⇒ tính lại max 454. Phần còn tăng theo số lần tìm thêm: **chưa rõ nguồn** — giới hạn (§4b).

**Khoá 1 `6cf67e9`** (ghi chú v1, `settings.yaml` `37b9ab1beb37`, D3 bản 5, hằng 185). Q1 chạy lại: **228 / 228 giống byte `main`** (cờ tắt).
**Q6 đã thấy trên khoá 1** (10 lượt ghép `chon_da_thay.json` + 10 H0 cờ tắt câu gốc; 0,0197 USD): **(b) phạm — 2 / 5 câu chi phí ghép có con số tổng do model tự tính** (nhân dự toán mỗi người theo số người; con số không có trong kho). **Đính chính (bộ đếm bản 2, xem dưới):** lần đầu B ghi hai câu khác — một câu bị đánh dấu nhầm (số **có** trong kho, chỉ viết theo đơn vị "triệu" thay vì số đủ), một câu bị bỏ sót (regex bản 1 hụt khi xuống dòng); số câu phạm vẫn **2 / 5**. H0 (`main`, không có Cách A) cũng có tổng. (a) chưa chấm.
- **Nguyên nhân [Code, đã đọc + test]:** câu Cách A (D7) nằm trong `HOI_LAI_NOTE`, mà ghi chú chỉ gửi khi lượt **đưa công cụ** `hoi_lai`; lượt ghép (sau khi bấm nút) không đưa công cụ (D1 — không hỏi lại lần hai) ⇒ model không thấy "không cộng tổng" ở đúng lượt trả lời câu chi phí. Plan D7 ghi "khi cờ bật" ⇒ **lỗi cài đặt lệch plan**. C163 và Q1 không bắt được (Q1 chỉ xét cờ tắt).
- **A chọn (2) có điều kiện:** sửa đúng chỗ lệch D7, không đổi chữ / ngưỡng / bộ đo; khoá 1 ghi **ÂM do lỗi cài đặt**; tính là vòng sửa 1 / 3 sau khoá; Q6 khoá 2 còn phạm ⇒ dừng.

**Khoá 2 `f8c9914`**: `CACH_A_NOTE` (`50006a120d03`) tách riêng, gửi mọi lượt trợ lý khi cờ `hoi_lai` bật (thường + stream); `HOI_LAI_NOTE` giữ **đúng byte** `2b62c390f2fa` (= phần công cụ + "\n" + `CACH_A_NOTE`) ⇒ lượt hỏi không đổi. Test mới: lượt ghép có Cách A (đường thường + stream + route), không có `hoi_lai`. Test 70 / 70. Q1 lại: **228 / 228 giống byte `main`**.
**Q6 đã thấy trên khoá 2** (10 lượt ghép; 0,0105 USD): regex ghi trước đánh dấu **0 / 5**; B vẫn đọc mọi câu chi phí có số tiền và đối chiếu từng con số với kho: **1 / 5 có con số tổng** — dự toán mỗi người trong kho **nhân lên theo số người** chọn ở nút (con số kết quả không có trong kho); 2 câu số đúng như kho; 2 câu không nêu số. ⇒ theo ý sàn ("0 câu có con số tổng") **còn phạm** ⇒ dừng, báo A (theo điều kiện A). (a) chưa chấm. **Kín chưa mở.**
- **Bộ đếm Q6 (b) bản 2** (`data/phase_9/b4/tools/dem_tong.py`, khoá 3 dùng): gộp xuống dòng, lấy mọi số tiền (cả hai đầu khoảng "A–B đồng"), tra từng số trong kho bằng `grep_kb.sh` (quy đổi "x,yz triệu" ⇔ số đủ) ⇒ số không có trong kho = ứng viên tự tính ⇒ B vẫn đọc tay mọi câu có số. Chạy lại trên khoá 1 / khoá 2: khớp kết quả đọc tay (khoá 1: 2 câu, khoá 2: 1 câu).
- **Finding cho bộ đếm (regex Q6 (b) bản 1):** regex "tổng / khoảng … số tiền" trên một dòng hụt khi câu xuống dòng giữa "khoảng:" và danh sách số ⇒ theo đúng chữ luật thì (b) "đạt" ở khoá 2, theo ý sàn thì phạm. B báo theo ý sàn. Bộ đếm sau phải đọc theo đoạn (bỏ xuống dòng) và đối chiếu con số với kho, không chỉ tìm từ khoá.
- Chênh token lượt ghép (không đưa `hoi_lai`): khoá 1 max 909, khoá 2 max 514 ≥ 512 — A: ghi giới hạn, không đo bây giờ (ngữ cảnh đo 1.700–4.000 token ≪ trần 16.384).

**Đang chờ User (qua A):** (1) B4 âm — cờ `hoi_lai` tắt, tag hồ sơ; (2) vòng sửa 2 — thêm vào chữ Cách A "không nhân theo số người / số ngày" (đổi chữ ghi chú ⇒ cần duyệt); (3) coi "giá mỗi người × số người" là tính trực tiếp — đổi định nghĩa (b) sau khi thấy kết quả, B không khuyên.

**Tiền B4:** ≈ **0,083 / 0,18** (pilot + v0 + v1 0,0256 · chọn ghi chú 0,0268 · Q6 khoá 1 0,0197 · Q6 khoá 2 0,0105). Dữ liệu: `data/phase_9/b4/{chon_ghi_chu,q6,q1}/` (private). Công cụ Q5 `data/phase_9/b4/tools/q5_golden.py` + `sinh_an_toan.py --hoi-lai` đã viết, **chưa chạy**. Q4 / Q5 / Q7 / Q8: NOT RUN.

## 2d. Khoá 3 `7d72703` (User chọn vòng sửa 2, A ghi nhận 20:55 04/11/2026) — 21:10 04/11/2026

**Lệch luật "sau khoá không chỉnh" (plan bản 5 §5 bước 4):** khoá 2 còn phạm Q6 (b) trên **đã thấy**; **kín chưa mở** (cả lượt hỏi lẫn lượt ghép) ⇒ chỉnh lần nữa không dùng thông tin kín — User chọn, A duyệt; vòng sửa 2 / 3 sau khoá (vòng 3 không dùng: còn phạm ⇒ âm).
**Đổi đúng một câu** trong `CACH_A_NOTE`: "Không nhân giá theo số người hay số ngày: nêu giá mỗi người / mỗi mục đúng như nguồn ghi để người dùng tự tính." (A chọn (b): câu vào cả `HOI_LAI_NOTE` — phần mô tả công cụ giữ đúng byte `54df89780cc6`; `CACH_A_NOTE` `6f7be345f782`, `HOI_LAI_NOTE` `42022ba2cdde`). Không đổi ngưỡng / bộ đo.
- Q1: **228 / 228 giống byte `main`** (cờ tắt). Test 70 / 70.
- Q2 / Q3 đã thấy chạy lại (chuỗi lượt hỏi đổi): Q2 **8 / 10** (≥ 8 — đạt sát; khoá trước 9 / 10); Q3 câu đủ **0 / 7**, gần giống 0 / 3. D3 điền 2 lượt ⇒ hỏi thừa sau D3 2 lượt (theo dõi).
- Q6 (b) — 10 lượt ghép × **2 lượt**: bộ đếm bản 2 0 số tiền ngoài kho; B đọc tay mọi câu chi phí có số: chỉ giá mỗi người / dòng tổng có sẵn trong bảng dự toán của kho, **0 câu nhân theo số người** ⇒ **0 / 5 cả hai lượt**.
- **Q6 (a) ĐẠT:** 30 mục mù (20 ghép + 10 H0) × 2 judge sub-agent mới (Opus 5.5, rubric `data/loi_nang_2026-10-28/rubric.md` giữ nguyên, ngữ cảnh = đoạn câu trả lời trích; công cụ `data/phase_9/b4/tools/q6_an_toan.py`): bên ghép cả 2 lượt **0 ý "trái", 0 ý "không có" loại giá / giờ / điều kiện** ("một trong hai"); "không có" loại khác 3 ý (lời xếp lịch chung, không phải dữ kiện). H0: 0 "trái", 0 "không có" giá / giờ / điều kiện. Bộ phân loại ý (code) lần đầu bắt nhầm chữ viết tắt "3N2Đ" là giá (chỉ chạm H0) ⇒ sửa regex (chữ "đ" / "k" phải viết thường), phân tích lại; bản đầu giữ ở `ket_qua_regex1.json`.
- **Kết luận đã thấy (khoá 3): Q1, Q2, Q3, Q6 đạt ⇒ đủ điều kiện mở kín** (A cho C).
- Chênh token (m-3): max 854 ở lượt đã thấy (lượt trả lời có tìm thêm; lượt dừng ở `hoi_lai` ≤ 0); ghép 337 / 273 — giới hạn §4b.
- **Tiền:** lượt khoá 3 0,037 ⇒ B4 ≈ **0,120**. Dự phóng phần còn lại 0,066–0,113 ⇒ vượt dừng 0,17 ⇒ **A nới trần B4 0,24 / dừng 0,23** (sàn còn lại bắt buộc theo spec). Mỗi lượt có phí ghi tiền thật ngay sau lượt.

## 4b. Giới hạn đã biết

- Phép đếm ngân sách token thiếu phần tăng theo số lần `tim_kho` thêm (chênh tới ~450–900 token ở lượt tìm nhiều) — nguồn chưa rõ; lề 512 có thể bị vượt khi ngữ cảnh sát trần (chưa gặp: ngữ cảnh thật ≪ trần).
- Q6 (b) dựa regex + đọc; regex đã hụt một dạng (§2c).

## 3. Còn lại (theo plan bản 5 §6, sau quyết định của User)

1. **Quyết của User:** vòng sửa 2 (A ghi nhận 20:55 04/11/2026) ⇒ khoá 3 (§2d).
2. Nếu đi tiếp: Q6 đã thấy đạt (cả (a) judge 2 sub-agent thước an toàn trên đoạn câu trả lời trích, lẫn (b)) ⇒ **kín (C)**: 10 lượt hỏi (Q2 / Q3) + 5 lượt ghép (Q6k) trên bản khoá cuối ⇒ Q4 (bộ tuyến 60, nhãn `can_hoi_lai.json`) ⇒ Q5 (mẫu Golden 30 + an toàn 32, `q5_golden.py` + `sinh_an_toan.py --hoi-lai` ⇒ `an_toan_b2.py`) ⇒ Q7 (4 chuỗi, nhớ bật) ⇒ Q8 cổng + Playwright ⇒ C review nhánh ⇒ A merge.
3. Nếu âm: cờ `hoi_lai` giữ tắt; tag `hoso/p9-b4`; ghi kết quả vào báo cáo khâu.
