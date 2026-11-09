# Review: Phase 9 T2 — plan "tra web thành công cụ" (nháp B, vòng 1)

Decision: **changes_requested** (0 blocker · 3 major) — một vòng, chỉ blocker / major (A 09/11: User dặn làm nhanh, tiền không còn là lý do chờ)
Người kiểm: C (Claude Code, `hue-rag-6a`)
Date: 20:20 09/11/2026 (`date`)
Canonical guide: spec `docs/superpowers/specs/2026-11-02-phase-9-design.md` §12 (User duyệt `5557f0fd7650`)
Đối tượng: `docs/superpowers/plans/2026-11-08-phase-9-t2-web-plan.md` sha256 `921f75d64a7c` (B, 12:29 08/11/2026, commit `82b44a0`)
Implementation report: chưa có (plan, chưa code)

## 1. Phạm vi đã review

- Plan T2 (đọc toàn bộ, 51 dòng).
- Spec Phase 9 §12 (dòng 491–610): §12.2 hàng T2, §12.3 sàn chung, §12.4, §12.5 T2, §12.6, §12.7, §12.8.
- Code `main` `5c982a0`: `backend/llm/assistant.py` — `tool_for_turn` / `TOOLS` (`:265-295`), `_lich_extra` (`:723-741`), `_finish_generated` chạm trần (`:653-655`),
  `web_gate_open` (`:817-825`), `cong_web` (`:828-862`), `answer_turn` (`:875-897`), đường song song #6 + `_merge_spec` (`:1100-1150`);
  `backend/llm/tra_web.py` `cau_tim_web` (`:59-64`), `dau_vao_model` (`:152-155`); `backend/llm/generator_openai_full_corpus.py` `ASSISTANT_MAX_TURNS` (`:77`),
  `parallel_tool_calls=False` (`:294`), `web_agent` (`:307-313`); `backend/llm/full_corpus_prompt.py` `TU_WEB_LUAT` (`:164-170`), câu chuẩn (`:7-53`).
- Bộ B6 đã thấy `data/phase_9/bo_do_b6/cau_da_thay.jsonl`: **chỉ đếm** trường `loai` / `ky_vong` (không đọc chữ câu).
- Theo lời A: không đọc `STATUS_B.md`; G chưa vào `main` ⇒ những gì plan giả định về G (outcome `out_of_scope` do code đặt) chưa kiểm được trên code.

## 2. Findings

### M-1 (major) — Số vòng tối đa (`max_turns`) chưa tính thêm cho công cụ mới ⇒ câu trả lời được bị từ chối

- **Vị trí:** plan §1.1 (công cụ trong mọi lượt của agent Huế), §2 (không có sàn nào về `max_turns`).
- **Yêu cầu:** spec §12.6 dòng "§4 trần + phục hồi": "plan kiểm `max_turns` đủ khi đủ 4 công cụ … plan đo `max_turns` = 0".
- **Bằng chứng (code):** `ASSISTANT_MAX_TURNS = 4` (`generator_openai_full_corpus.py:77`) = tìm ×2 + lần 3 "hết lượt" + 1 lượt viết. Công cụ gọi lần lượt
  (`parallel_tool_calls=False`, `:294`) ⇒ `yeu_cau_tra_web` ăn **một vòng riêng**. Chuỗi tìm, tìm, tìm ("hết lượt"), yêu cầu web, viết = **5 vòng > 4** ⇒ chạm trần ⇒
  `_finish_generated` đặt `INSUFFICIENT_ANSWER` + outcome `max_turns` (`assistant.py:653-655`) ⇒ `web_gate_open` đóng (outcome ∉ {None, `refusal_no_sources`}, `:823`) ⇒
  câu đó **mất cả câu trả lời kho lẫn mục web**. Đúng loại câu T2 nhắm (hỏi kèm, kho thiếu một phần) là loại hay dùng hết lượt tìm. T1 (`max_turns_for`, +1 khi
  có `ngay_lich`) và T3 (`max_turns_cho`) đều đã phải thêm vòng vì đúng lỗi này (T1: 1 câu chạm trần ở lượt đo).
- **Tác động:** từ chối nhầm mới + sai thước "câu hỏi kèm có phần web".
- **Tiêu chí đóng:** plan ghi (a) +1 vòng khi lượt có `yeu_cau_tra_web` (giá trị này không vào thân yêu cầu ⇒ Q1 không đổi — như T3), cộng dồn với T1 / T3 (trên
  nhánh T3 đã rebase có `max_turns_for(ngay_lich_fn, ve_gio_fn, thoi_tiet_fn)` — T2 thêm một tham số cùng chỗ); (b) một test 0 USD cho chuỗi xấu nhất; (c) sàn
  "outcome `max_turns` = 0 trên mọi lượt đo" (code đếm từ `chat_metrics`, 0 USD).

### M-2 (major) — Thiếu sàn chung S2c, S5, S6 của spec; S1 chỉ 1 lượt

- **Vị trí:** plan §2 bảng tiêu chí.
- **Yêu cầu:** spec §12.3 "Sàn chung … áp cho mọi việc có lượt trả lời"; `Session_Prompt.md` §7 mức nhẹ: "đo 1 lượt (**chỉ bộ an toàn 32 chạy 2 lượt**)".
- **Bằng chứng:**
  - **S2c** (câu Huế kho thiếu vẫn có web ≥ mốc − 1, trên 7 câu Golden ngoài phạm vi nhãn `tro_ly_hue` + 10 câu B6 "web trả lời được") không có trong plan. Với T2 đây là
    rủi ro thật: có công cụ mới, model có thể chuyển từ "từ chối" (cổng cũ mở) sang "trả lời một phần, không yêu cầu web" (không cổng nào mở) ⇒ mất mục web mà mốc có.
    10 câu B6 đã có trong bộ 28 (đếm `loai`: `web_tra_loi_duoc` 10); 7 câu Golden chưa có.
  - **S5** (chữ đầu p50 ≤ 3 s / p95 ≤ 5 s, không chậm hơn mốc quá nhiễu) chỉ còn dòng "theo dõi chữ đầu mục web". Công cụ thêm một vòng model **trước** lượt viết ở mọi câu
    model gọi nó ⇒ chữ đầu của **câu kho** chậm thêm khoảng một vòng (~1 s, chưa đo) — đúng thứ S5 đo.
  - **S6** (≤ 0,0005 USD / câu Huế) không có; G đo câu Huế 0,000425 (handoff) ⇒ còn ~0,00008 cho mô tả công cụ ở mọi lượt + một vòng thêm khi gọi.
  - **S1:** plan tính tiền an toàn 32 **một lần** cho biến thể (§4); luật mức nhẹ đòi 2 lượt.
- **Tiêu chí đóng:** thêm S2c (dùng 10 câu đã có + 7 câu Golden), S6 (đọc `chat_metrics.usd`, 0 USD thêm), S5 (lượt riêng do A xếp — ghi tiền vào §4 hoặc ghi rõ
  "S5 tính ở quỹ chung"), S1 ×2; cập nhật §4.

### M-3 (major) — Bộ "hỏi kèm 10" chưa chốt + "có phần web" chưa có định nghĩa đếm được

- **Vị trí:** plan §2 dòng "Câu hỏi kèm có phần web ≥ mốc + 2 / 10", §3 "khi viết bản chính: kiểm câu nào dùng được …".
- **Yêu cầu:** `run-experiment` / `Session_Prompt.md` §6: tiêu chí và bộ đo ghi **trước** khi chạy; plan mức nhẹ = "tiêu chí + bộ đo + tiền".
- **Bằng chứng:** đây là chỉ số quyết định duy nhất cho lợi ích của T2, nhưng (a) bộ chưa tồn tại (E20 cần cờ `lich_trinh` đang tắt — plan tự ghi); (b) "có phần web" chưa
  nói đếm bằng gì: `trace.web.outcome == "co_muc"`? hay người / sub-agent đọc xem mục web có trả lời **phần kho thiếu**? Hai cách cho số khác nhau — xem ghi chú về câu tra bên dưới.
- **Tiêu chí đóng:** bản chính có (a) đường dẫn + md5 bộ 10 câu, người viết ≠ người viết mô tả công cụ; (b) định nghĩa bằng chữ: ví dụ "web mở ∧ outcome `co_muc` ∧ mục web
  có ≥ 1 câu về phần câu kho không trả lời (sub-agent đọc mù biến thể / mốc)"; (c) cách đếm ở mốc (mốc chỉ mở web khi kho từ chối cả câu).

### Ghi chú không chặn (một dòng mỗi ý, B tự quyết)

- Mục web giữ tiền đề "kho **không có**" (`TU_WEB_LUAT`, `full_corpus_prompt.py:165`) và câu tra = cả câu hỏi (`tra_web.py:59-64`) ⇒ với câu hỏi kèm, mục web có thể trả lời lại phần kho đã có với số khác — đáng đếm "mục web nói khác câu kho" lúc chấm bộ 10 (quan sát).
- Test cổng nên chạy trên cả 3 đường (`answer_turn`, stream, #6 sau `_merge_spec`) + 1 ca lượt ghép `truong`; cờ `web_yeu_cau` phải là trường của `AnswerTrace` để `_merge_spec` chép sang.

**Không có blocker.** Thiết kế công cụ (không tham số, câu cố định trung tính, cổng một chỗ, truy vấn code dựng, chữ web không vào agent chính) khớp spec §12.5 / §12.8;
không thấy over-engineering.

## 3. Cách người kiểm chạy lại thật

Docs-only: đọc plan, spec, code `main` `5c982a0` (đường dẫn ở §1). Một lệnh đếm trường `loai` / `ky_vong` của `cau_da_thay.jsonl` (`uv run python -I -c …`, không in chữ câu).
Không chạy lượt có phí, không chạy test (plan chưa có code). 0 USD.

## 4. Kết quả quan sát — tiền

A chuyển lời User 09/11: tiền không còn là lý do chờ ⇒ không cần ép ≤ 0,2. Ghi lại cho đúng số: plan ≈ 0,215; thêm phần M-2 (S1 ×2, S2c) ≈ +0,04; 4 câu "kho có" của B6 đã nằm trong bộ 28 (đếm `loai`) ⇒ đếm trùng nhỏ. Cách rẻ hơn nếu cần: bỏ mốc 18 câu B6 có sàn tuyệt đối (chỉ giữ mốc 10 câu S2c) và dùng lại lượt G làm mốc S1 / S4 khi T2 tách từ đúng sha G đã đo ⇒ ≈ 0,2.

## 5. Giới hạn hoặc phần chưa chạy

- G chưa vào `main`: điều kiện "chữ = `OUT_OF_SCOPE_ANSWER` ⇒ outcome `out_of_scope`" plan dựa vào code G chưa kiểm được; review lại phần cổng khi plan bản chính viết trên
  `main` sau G.
- Đơn giá / câu là của plan (B6, G); không đo lại. Không đọc `STATUS_B.md` (theo A) ⇒ không biết G đã đo S2c / lưu câu trả lời mẫu 30 hay chưa — điều kiện cho dòng cuối bảng §4.
- Không kiểm `max_turns` bằng lượt thật; M-1 dựa trên đọc code (chuỗi vòng là suy luận từ `ASSISTANT_MAX_TURNS`, `parallel_tool_calls=False` và tiền lệ T1).

## 6. Decision và bước tiếp theo

**changes_requested.** B sửa M-1 (vòng thêm + test + sàn `max_turns` = 0), M-2 (S2c, S5, S6, S1 ×2, cập nhật tiền), M-3 (chốt bộ hỏi kèm 10 + định nghĩa "có phần web")
trong bản chính viết trên `main` sau G. Một vòng: B sửa xong thì A duyệt (không review lại), C trả lời B trực tiếp nếu cần.
