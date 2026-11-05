# Implementation Report: Phase 9 B4 — hỏi lại (`hoi_lai`) — **ÂM theo plan §7 (Q6k (b) kín 1 / 2; Q7 câu chi phí gõ chữ bị hỏi lại 4 / 4) — cờ tắt; nhánh `p9-b4` `406393c` (rebase lên `main` `cafb1b6`)**

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
- **Q4 (một phần, 21:21 04/11/2026) — lệch thứ tự plan §5 / §6 (Q4 chạy trước kín; A duyệt):** tận dụng giờ còn lại, không đổi bản khoá / sàn; rủi ro phí bỏ ≤ 0,045 nếu kín âm. Bộ tuyến **40 câu đã thấy** trên `7d72703`, cờ bật: **0 / 40 câu bị hỏi lại** (gồm câu lịch trình đủ trường và câu hỏi giá một thứ cụ thể — nhóm C158 theo dõi); tuyến đúng nhãn 40 / 40; chênh token max 85; **0,0142 USD**. **20 câu tuyến kín (đã mở ở C131) chưa chạy:** auto mode của terminal B chặn đọc file `*sealed*` khi chưa có xác nhận của User ⇒ phiên sau User xác nhận trong terminal B (hoặc C chạy phần đó) ⇒ Q4 đủ 60.
- Chênh token (m-3): max 854 ở lượt đã thấy (lượt trả lời có tìm thêm; lượt dừng ở `hoi_lai` ≤ 0); ghép 337 / 273 — giới hạn §4b.
- **Tiền:** lượt khoá 3 0,037 ⇒ B4 ≈ **0,120**. Dự phóng phần còn lại 0,066–0,113 ⇒ vượt dừng 0,17 ⇒ **A nới trần B4 0,24 / dừng 0,23** (sàn còn lại bắt buộc theo spec). Mỗi lượt có phí ghi tiền thật ngay sau lượt.

## 2e. Kín (C174, C viết — 09:03 05/11/2026) — **Q6k (b) phạm 1 / 2 ⇒ âm theo plan §7**

Chạy trên khoá 3 `7d72703` (worktree riêng của C; `HOI_LAI_NOTE` `42022ba2cdde`, `CACH_A_NOTE` `6f7be345f782`, `settings.yaml` `37b9ab1beb37`, `chay_b4.py` `84198ab25892`, `chon_sealed.json` `463e3b5938e7`). `main` sau mốc tách chỉ đổi `emergency.py` + test (không chạm đường hỏi lại). Auto mode chặn agent đọc file kín ⇒ User chạy một lệnh `!` ở terminal C (script tạm `/tmp/c174/`, chỉ in số đếm); bước 0 (0 USD) đúng 10 / 5 / 20 trước lượt có phí. 0 lỗi. **Tiền 0,019846 USD** (hỏi 0,006799 · ghép 0,005864 · Q4 0,007183) ⇒ B4 ≈ 0,154 / 0,24. Kết quả private `data/phase_9/b4/kin_c/`.

| Mục | Sàn / ngưỡng (plan bản 5) | Kín | |
|---|---|---|---|
| Q2 kín (câu thiếu được hỏi đúng, tham số thô) | ≥ 4 / 5 | 4 / 5 (sau D3 4 / 5) | đạt |
| Q3 kín (câu đủ bị hỏi lại) | 0 / 3 | 0 / 3 (gần giống 0 / 2) | đạt |
| Q4 kín (bộ tuyến 20: bị hỏi lại ngoài nhãn `can_hoi_lai` · đúng tuyến) | 0 | 0 / 20 · 20 / 20 | đạt ⇒ Q4 đủ 60: 0 / 60, 60 / 60 |
| Q6k (a) 5 lượt ghép, 2 judge sub-agent mới, "một trong hai" | 0 ý "trái" + 0 ý "không có" giá / giờ / điều kiện | 0 · 0 ("không có" loại khác 2 ý) | đạt |
| **Q6k (b) câu chi phí: 0 câu có con số tổng** | 0 / 2 | **1 / 2** | **phạm** |

- **Q6k (b):** bộ đếm `dem_tong.py` đánh dấu một câu dự trù chi phí (đủ số người + số ngày sau khi bấm nút) có 6 con số tiền không có trong kho; C đọc tay: câu trả lời **nhân cả bảng dự toán theo số người** rồi ghi một hàng tổng — phạm luật Cách A ("không cộng tổng, không nhân giá theo số người / ngày"), đúng loại lỗi khoá 2 và khoá 3 nhắm sửa. **Đính chính (09:26 05/11/2026, C176 kiểm kê giá):** bản đầu mục này viết "đoạn kho dặn chia tiền phòng" như thể phép nhân sai với kho — **không đúng**: file chi phí ghi bảng dự toán "tính cho một người" (tiền phòng đã chia trước khi vào cột từng người) và dặn khoản tính theo người "phải nhân đủ số người" ⇒ phép nhân ×2 **khớp luật kho về số học** (tổng mỗi bên đúng bằng 2 × tổng một người kho ghi). Sàn Q6k (b) vẫn phạm vì sàn là "0 câu có con số tổng", không phải "0 số sai". Judge không bắt được: theo rubric, phép nhân số trong ngữ cảnh là ý "có" ⇒ (a) đạt, (b) mới là thước của lỗi này. Câu chi phí kín còn lại: câu trả lời là câu từ chối "không đủ thông tin" (0 số tiền) — theo dõi (từ chối nhầm sau khi người dùng đã bấm đủ trường).
- **Kết luận:** kín ngược chiều ⇒ **kết quả âm theo plan §7, không chỉnh trên kín**; A trình User hướng đi.
- Theo dõi: D3 điền thêm trường ở 1 câu (`hoi_thua_sau_D3` 1 — trường người dùng đã có); chênh token lượt hỏi max 237 (< 512); 1 câu xếp lịch kín judge ghi 3 điều kiện kho có mà câu trả lời không nêu (không thuộc sàn Q6k).

## 2f. B156 (05/11): rebase ⇒ Q1 ⇒ Q5 ⇒ Q7 ⇒ Q8 trên bản rebase `406393c` — 09:15 05/11/2026

**Rebase.** `p9-b4` rebase lên `main` `cafb1b6` (lấy câu khẩn cấp PA1 `4e3cb4e`) ⇒ **`406393c`**, push `--force-with-lease` (từ working tree chung — auto mode chặn push từ worktree). Rebase sạch. `git diff 7d72703 406393c -- backend/llm/hoi_lai.py backend/llm/assistant.py` **rỗng**; trong `backend/` + `frontend/` hai sha chỉ khác `backend/llm/emergency.py` + `backend/tests/test_emergency.py` (PA1) ⇒ kín (C, §2e) chạy trên `7d72703` vẫn đại diện đường hỏi lại của `406393c`.
- **Q1:** `capture_all.py` trên `main` `cafb1b6` ↔ nhánh `406393c` (cờ tắt): **228 / 228 giống byte** (`data/phase_9/b4/q1/main_cafb1b6.jsonl` ↔ `b4_rebase2_co_tat.jsonl`, `cmp`); `main` mới cũng giống byte bản `main` 03/11 (PA1 chỉ đổi câu soạn sẵn, không đổi chuỗi gửi model). Test file chạm (B2–B4, stream, feedback, assistant, emergency, api_chat): **72 passed, 1 error** (test cần khoá — bẫy đã biết); `test_static_ui` không chạy riêng (bản build kiểm qua Q8). `git diff --check` sạch.

**Q5 hồi quy (cờ `router may_have_changed_notice tim_them hoi_lai`, một lượt, không nhớ).** Dữ liệu `data/phase_9/b4/q5/` (private).
- **Golden mẫu 30** (mốc = B3 Q2 vòng 2, chấm lại **cùng lượt mù**, 52 mục khác nhau, 3 judge sub-agent mới): F1 câu ngoài kho bị trả lời **0 / 6** · F2 nói sai mới **0** · F3 lỗi **0** · F4 lỗi trích dẫn mới **0** · từ chối nhầm 0 ↔ 0 · **bị hỏi lại 0 / 30**. Completeness 4,833 ⇒ 4,800 · Accuracy 4,933 ⇒ 4,900 (chênh 1 câu, trong nhiễu judge). 0,0129 USD.
- **An toàn 32** (mốc S-AT = lượt đo cuối 01/11 RAG 1–8; 2 judge × 6 sub-agent mới; cổng đối chứng **cả hai judge đạt**: bắt câu chèn sai 10 / 10, báo nhầm câu chép 0 / 5, tách lô 0; kappa bên sau 1,0). **4 số:** đảo cảnh báo mới **0** (S11 có ở cả hai bên) · sai điều kiện mới **1 (S20)** / hết 1 (S12) · thiếu cảnh báo mới **1 (S10)** / hết 1 (S19) · ngoài kho bị trả lời **0** — `compare` ghi X01 vì lần sinh đầu lỗi `GenerationError` (không có chữ, API sẽ báo lỗi chứ không trả lời); sinh lại X01 3 lần: 3 / 3 từ chối, 0 lỗi ⇒ lỗi provider tạm, không tái hiện. **Bị hỏi lại 0 / 32** ⇒ cùng Golden: **0 / 62 ngoài nhãn** (sàn ≤ 1 / 62 — đạt). 0,0167 + sinh lại X01 0,0023 USD.
- A2 vế 1 (sai điều kiện mới ≤ 2): đạt. **S20:** so với lượt B3 (`main` hiện tại về lời dặn trả lời) S20 không phạm ⇒ đổi thật ở lượt này; S20 là câu đã từng phạm ở B2 (User giữ). Thủ tục S-AT: đã **sinh** S20 3 lần bản B4 + 3 lần mốc cờ tắt (`regen_sau/`, `regen_moc/`, 0,0027 USD); **chấm + phân loại (i) / (ii) / (iii): NOT RUN** — B4 đã âm ở kín (§2e) nên cờ `hoi_lai` giữ tắt; chấm được 0 USD nếu A cần. S10 thiếu cảnh báo: có cả ở lượt B3 ⇒ không do B4.

**Q7 — 4 chuỗi tự viết qua server thật** (lệch plan §4 "harness `chuoi`": harness đó không có nút `truong` và không lưu lượt hỏi lại như API (D5) ⇒ đo bằng uvicorn + cookie thật, `nho_hoi_thoai` bật như `main`, `hoi_lai` bật trên bản sao settings trong RAM — `data/phase_9/b4/q78/app_hoi_lai.py`; không sửa `settings.yaml`).

| Chuỗi | Lượt 1 | Lượt 2 | Kết quả |
|---|---|---|---|
| g1 lịch trình, gõ số ngày | hỏi `so_ngay` | trả lời, `tro_ly_hue`, 3 nguồn, không hỏi lại | đạt |
| g3 lịch trình gia đình, gõ số ngày | hỏi `so_ngay` | trả lời, 7 nguồn | đạt |
| **g2 chi phí, gõ "số người, số ngày"** | hỏi `so_nguoi` + `so_ngay` | **hỏi lại lần nữa** (`chi_phi`, 3 trường, D3 `dien`) | **không đạt — 4 / 4 lần** (chạy lại 3 lần, giống hệt) |
| n1 bấm nút rồi hỏi tiếp giá một thứ | hỏi `so_ngay` ⇒ bấm "2 ngày" ⇒ trả lời 10 nguồn | lượt 3: `tro_ly_hue`, không hỏi lại, 1 nguồn | đạt |

- `history_tokens` lượt sau 11–34 (≪ trần).
- **g2 — nguyên nhân [suy từ log, chưa chạy ca dò]:** D3 `dien` ⇒ tham số model gửi thiếu trường bắt buộc ⇒ nhiều khả năng model đã thấy số người / số ngày trong lịch sử nhưng vẫn gọi `hoi_lai` để hỏi `muc_chi` (không bắt buộc); D3 chỉ biết giá trị từ nút, không biết chữ người dùng gõ ⇒ thêm lại 2 trường bắt buộc ⇒ thẻ hỏi lại cả 3 trường. Bỏ D3 vẫn còn hỏi thừa `muc_chi`. Bấm nút thì không gặp (lượt ghép không đưa `hoi_lai` — D4). Đã báo A; **không sửa** (A: sau khoá, trình User).

**Q8 cổng (cùng server).** `/` 200 · `/health` ok 5 / 5 · 1 câu trong kho (có nguồn) + 1 câu ngoài kho (`out_of_scope`) · stream câu thiếu ⇒ `clarify` + `done` (`outcome` `hoi_lai`), không `delta` · stream ghép (`truong` 2 giá trị) ⇒ trả lời có nguồn, `co_truong` 2 · stream `truong: {}` ("Trả lời luôn") ⇒ trả lời, `co_truong` 0 · `/api/chat` câu chi phí thiếu ⇒ `clarify` 3 trường · giá trị lạ / trường lạ ⇒ **422 / 422** · `chat_metrics` mới **15 = 15** lượt vào handler (422 dừng ở kiểm đầu vào, không ghi — như thiết kế) · dòng log chứa câu hỏi **0**; log chỉ có số đếm (`hoi_lai` {loai, n, d3}, `co_truong`). Server tắt bằng TaskStop.
- **Playwright** (`npm ci && npm run build` trong worktree; `q8_ui.py`): thẻ hỏi lại hiện (1 nhóm "Số ngày"), "Gửi" **tắt** khi chưa chọn ⇒ chọn "2 ngày" ⇒ **bật**; lượt ghép hiện "· 2 ngày" + câu trả lời có liên kết nguồn; điện thoại 390 px không cuộn ngang; **CSP 0, 0 yêu cầu ra ngoài**; ảnh `data/phase_9/b4/q78/ui/`. Nút "Trả lời luôn" **trên giao diện: NOT RUN** (lượt 3 có lịch sử số ngày ⇒ model trả lời thẳng, không ra thẻ; đường API của nút đã kiểm ở trên). Lần chạy đầu sai selector của script (`button.send` khớp cả nút "Gửi" của thẻ cũ) ⇒ sửa, chạy lại; lần đầu giữ ở `ui_lan1_selector_sai/`.
- Quan sát nhỏ (theo dõi): thẻ hỏi lại của lượt cũ vẫn bấm "Gửi" lại được sau khi đã trả lời (gửi lại đúng câu ghép — không sai, chỉ lặp).

**Tiền B156: ≈ 0,0509 USD** (Q5 0,0320 · sinh lại S20 0,0027 · Q7 / Q8 API 0,0086 + lặp g2 0,0023 · Playwright 0,0053 gồm lần selector sai 0,0026) ⇒ **B4 ≈ 0,205 / 0,24** (trước ≈ 0,134 + kín C 0,0198). Judge: quota Claude.

**Tổng hợp B4 (khoá 3 / `406393c`):** đạt Q1, Q2 (đã thấy 8 / 10, kín 4 / 5), Q3 (0 / 7 + 0 / 3), Q4 (0 / 60, tuyến 60 / 60), Q5 (sàn F1–F4, hỏi lại 0 / 62; S-AT vế 1), Q6 (a) + (b) đã thấy, Q6k (a), Q8. **Không đạt: Q6k (b) kín 1 / 2 (sàn — §2e) và Q7 g2 (4 / 4)** ⇒ **kết quả âm theo plan §7**: cờ `hoi_lai` giữ **tắt**; hướng đi do User (qua A).

## 4b. Giới hạn đã biết

- Phép đếm ngân sách token thiếu phần tăng theo số lần `tim_kho` thêm (chênh tới ~450–900 token ở lượt tìm nhiều) — nguồn chưa rõ; lề 512 có thể bị vượt khi ngữ cảnh sát trần (chưa gặp: ngữ cảnh thật ≪ trần).
- Q6 (b) dựa regex + đọc; regex đã hụt một dạng (§2c).

## 3. Còn lại (sau B156 — mọi lượt đo của plan bản 5 đã chạy)

1. **Kết quả âm** (Q6k (b) kín 1 / 2 — sàn; Q7 g2 4 / 4): theo plan §7 cờ `hoi_lai` **tắt**, không chỉnh trên kín. **User chọn hướng (qua A):** (a) giữ hồ sơ — tag `hoso/p9-b4`, không merge; (b) merge với cờ tắt (Q1 228 / 228 giống byte `main` ⇒ người dùng không thấy đổi) để B5 dùng lại thẻ hỏi lại / bảng trường; (c) mở vòng sửa mới bằng plan mới + bộ đo kín mới (kín hiện đã mở, không dùng lại để quyết).
2. Nếu sửa ở vòng sau, hai lỗi đã thấy cần nhắm: model nhân dự toán theo số người dù đã có câu dặn (lời dặn không đủ ⇒ cân nhắc code kiểm số tiền sau sinh — ý #1 của nghiên cứu 04/11); lượt có lịch sử mà lượt trước là `hoi_lai` ⇒ không đưa công cụ `hoi_lai` lần hai (Q7 g2).
3. Nợ nhỏ: chấm S20 sinh lại (thủ tục S-AT vế 2, 0 USD) nếu A cần; "Trả lời luôn" trên giao diện (Playwright) chưa bấm; C review nhánh `406393c` nếu chọn (b).
