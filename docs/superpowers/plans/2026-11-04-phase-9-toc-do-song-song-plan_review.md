# Review: Phase 9 — plan thí nghiệm tốc độ #6 (lần trả lời song song với định tuyến), bản 1

Decision: **changes_requested** (0 blocker · 0 major · 3 minor) — m-1 cần một câu sửa (định nghĩa sàn KC); m-2, m-3 tuỳ C / A. Sửa xong ⇒ B kiểm phần sửa ⇒ A duyệt sha.
Người kiểm: B (Claude Opus 5.5, `hue-rag-2d`) · 20:45 04/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-04-phase-9-toc-do-song-song-plan.md` sha **`c3c787b78650`** (C169, chưa commit)
Cách review: chỉ gói "Căn cứ để review" + lệnh chỉ đọc (`WORKFLOW.md` §9.1); không đọc STATUS / tin của C. 0 USD.

## 1. Phạm vi đã review

Plan bản 1; `backend/llm/assistant.py` trên `main` (`_before_model` :275, `_pick_route` :336, `answer_turn_stream` :389–) + `backend/api/routes/chat.py` `_answer_events` (:411); plan #1 bản 5 §2–§3 + report `c156_toc_do_dinh_tuyen.md` (B đã review — B155); spec §4, §7.

## 2. Findings

**Đã kiểm, khớp:** dòng tham chiếu code đúng trên `main`. **Đầu vào của (ii) không phụ thuộc tuyến** (đọc `answer_turn_stream`): lần tìm đầu dùng câu gốc khi `lan_tim_dau: v0`; lời dặn trợ lý / lịch sử / dòng ngày lấy từ `trace.history` và cờ, không từ tuyến; `tool_for_turn` + `start_tools_stream` chỉ cần `tool_prompt` ⇒ chạy trước khi có tuyến được — D1–D4 làm được. Đường khẩn cấp hôm nay trả câu soạn sẵn ngay sau `_pick_route` (`fixed_outcome`) ⇒ sàn **AN** (0 sự kiện lượt bỏ lọt ra) + **KC** đúng chỗ rủi ro. Sàn K / S1 / N / R / AT chép đúng plan #1 bản 5; mốc C165 khớp số B155 đã tính lại; dùng lại mốc khác ngày ghi **Lệch** + phương án thay (A quyết) — đúng cách. Q1 hai vế (cờ tắt giống byte `main`; cờ bật mỗi yêu cầu giống byte bản cờ tắt) đủ để AT dùng lại 4 số S-AT. Đường ra / dữ liệu cá nhân (§6: câu khẩn cấp / ngoài phạm vi nay cũng kèm đoạn kho tới OpenAI) ghi để trình User — đúng. Số học §5: 173 × (0,000088 + 0,0003) ≈ 0,067; 56 × 0,0004 ≈ 0,022 ⇒ ≈ 0,09 — khớp.

| Mã | Mức | Vị trí | Bằng chứng | Tác động | Tiêu chí đóng |
|---|---|---|---|---|---|
| **m-1** | minor | §4 **KC** ↔ §3 chữ đầu / §5 | KC: "chữ đầu 2 câu khẩn cấp (**8 lần đo mỗi bên**)"; §3: 14 câu × **2 lượt** × 2 bên (ABBA) ⇒ mỗi câu khẩn cấp 2 lần / bên ⇒ **4 lần / bên**; §5 tiền tính 14 × 2 × 2 | Sàn KC không đếm lại được giống nhau (4 hay 8 mẫu; nếu 8 thì tiền + lịch đo thiếu) | Ghi một con số: 4 lần / bên (trung vị trên 4), hoặc thêm lượt cho 2 câu khẩn cấp để đủ 8 + sửa tiền |
| m-2 | minor | D2 `usd_bo_uoc` | "cận dưới = token vào bộ dựng đếm × giá vào; lần bị huỷ không có usage". Khi định tuyến **chậm hơn** lần trả lời (đúng ca T thứ nhất), (ii) có thể xong trước khi bị bỏ ⇒ có usage thật | Ghi "cận dưới" cho cả lượt đã có usage ⇒ số theo dõi thấp hơn thật | Lượt bỏ đã xong ⇒ ghi usage thật; chỉ lượt bị huỷ giữa chừng mới dùng cận dưới; `chat_metrics` tách hai loại |
| m-3 | minor (độ tương xứng) | §3 tầng an toàn 173 lượt end-to-end | Yêu cầu định tuyến giống byte (Q1) ⇒ K / S1 / N / R đo lại chỉ là nhiễu model so mốc C165, không đo thay đổi của #6. Phần #6 thật sự đổi là **AN** — cần đủ mọi lượt tuyến ≠ `tro_ly_hue` (khẩn cấp 30, ngoài phạm vi, trò chuyện) nhưng chỉ cần một mẫu lượt `tro_ly_hue` cho `delta_matches_final` | ≈ 2 / 3 của 0,067 là lượt `tro_ly_hue` chạy hết, phần lớn không thêm bằng chứng cho AN | Tuỳ A: giữ 173 (rẻ, thêm một lượt nhiễu), hoặc chạy đủ lượt tuyến khác + ~20 lượt `tro_ly_hue`; K / S1 / N / R đếm trên lượt đã chạy, ghi rõ |

## 3. Cách người kiểm chạy lại thật

Đọc code `main` (grep vị trí hàm, đọc `answer_turn_stream`); tính lại số §5. Không gọi API.

## 4. Kết quả quan sát

Như §2. Không chạy code (plan chưa code).

## 5. Giới hạn hoặc phần chưa chạy

Chưa kiểm được thực tế huỷ task SDK giữa stream có dừng sạch ở mọi giai đoạn (đang `tim_kho`, đang stream) — plan dựa B131 (d); test T + AN sẽ bắt. CPU / RAM khi lần nhúng chạy cùng lúc định tuyến: chỉ theo dõi.

## 6. Decision và bước tiếp theo

**changes_requested** (0 / 0 / 3) — C sửa m-1 (một câu); m-2 / m-3 tuỳ. Báo sha ⇒ B kiểm phần sửa ⇒ A duyệt sha, chốt trần (đề xuất 0,10 / dừng 0,095) và quyết dùng lại mốc C165.

## Vòng 2 — kiểm phần sửa bản 2 (sha `093d548445a3`, B, 20:48 04/11/2026)

Decision: **ready_for_user_confirmation** (0 / 0 / 0 mới) — A duyệt sha. 0 USD.

| Finding | Kiểm | Kết luận |
|---|---|---|
| m-1 | §3 chữ đầu 16 câu (10 `tro_ly_hue` + 4 khẩn cấp + 1 ngoài phạm vi + 1 trò chuyện) × 2 lượt ⇒ KC 4 × 2 = **8 lần / bên** — khớp §4 KC; §5 tiền 16 × 2 × 2 × 0,0004 ≈ 0,026 | **đóng** |
| m-2 | D2 tách `usd_bo` (usage thật khi lượt bỏ đã xong) / cận dưới khi huỷ giữa chừng (`bo_huy_giua`) | **đóng** |
| m-3 | tầng an toàn 90 = mọi lượt nhãn ≠ `tro_ly_hue` + 20 lượt `tro_ly_hue` chọn trước (theo qid / thứ tự file — không chọn theo kết quả). B đếm lại từ file mốc C165: nhãn ≠ `tro_ly_hue` = **70** (123 câu: 57 · lịch sử: 13, gồm đủ 30 khẩn cấp) — khớp; R tính trên đúng các lượt đã chạy; AT dựa Q1 giống byte cả hai lần gọi + 10 câu an toàn trong bộ theo thủ tục S-AT — hợp lý; tiền 90 × ≈ 0,00039 ≈ 0,035 + 0,026 ≈ **0,061** < dừng 0,095 | **đóng** |
| Chốt A (mốc C165 dùng lại, trần 0,10 / dừng 0,095, Q 0,5 s) | đã ghi đúng chỗ (§3, §4, §5) | — |
