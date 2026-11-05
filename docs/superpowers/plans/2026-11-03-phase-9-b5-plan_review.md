# Review: Phase 9 — plan B5 lịch trình gợi ý (`lich_trinh`), bản 2

Decision: **changes_requested** (0 blocker · 3 major · 6 minor)
Người kiểm: B (Claude Opus 5.5, `hue-rag-2d`) · việc **B152** (A giao)
Date: 19:50 04/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-03-phase-9-b5-plan.md` sha **`0df068b47df6`** (C161, commit `b683514`)
Cách review: chỉ dựa trên gói "Căn cứ để review" của plan + lệnh chỉ đọc / tính lại từ dữ liệu (`WORKFLOW.md` §9.1); không đọc STATUS / tin của C. 0 USD. Repo public: không chép kho / bộ đo.

## 1. Phạm vi đã review

- Plan bản 2 toàn bộ; spec Phase 9 `169c2dd5f86a` §3, §4, §5 B4 + B5, §6, §8; `data/phase_9/lich_trinh/diem.json` (`335786dafb97`, khớp sha plan ghi) + `diem_cho_user.md` (`f87c81699a32`); plan B4 bản 2 D2 / D4 / D5 (B là người viết B4 — đối chiếu tên / giá trị trường); dòng User chọn B5 (nay ở `session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-11-03_toi.md:55` và `CURRENT_HANDOFF.md` mục "Phiên sau" bước 5).
- Code hiện hành đường tìm (`backend/llm/assistant.py` `search_into_trace` :138–168, `tool_for_turn` :181–) để kiểm D6 làm được như chữ plan.

## 2. Findings

**Đã khớp (không finding):** D1 dùng đúng 4 trường + giá trị + `so_ngay` bắt buộc của plan B4 D2 (B4 bản 3 `507bd5b72ae9` không đổi D2; D3 bản 3 thêm trường bắt buộc ⇒ câu lịch trình qua thẻ luôn có `so_ngay`, khớp D1); bảng 28 điểm / 8 cụm, 28 `nguon` khác nhau, 28 / 28 có `vi_tri_can_cu`, 4 / 28 có `thoi_luong` (3 `nua_buoi`, 1 `ngan`) — khớp §9; 8 cụm trong bảng kề §2b đều là cụm của bảng; 11 id ở D5 (a) đều có trong bảng và mỗi tên có trong file vé Quần thể (đếm bằng `scripts/grep_kb.sh --dir travel/tickets -c -i -F`, 2–13 lần); Quyết 1 / 2 chép đúng; D3, D9, D10 theo User / spec; **Lệch** spec ở D5 có ghi lý do; bộ đo 18 (13 / 5) và 3 / 3 ngoài Huế khớp spec §4; tiền nằm trong trần Phase.

| Mã | Mức | Vị trí | Bằng chứng | Tác động | Tiêu chí đóng |
|---|---|---|---|---|---|
| **M-1** | major | §4 (thiếu); D8 | Spec §4 "Đo riêng agent" có **đường đúng** (nhãn đường kỳ vọng ↔ lời gọi công cụ). Plan không có chỉ số "câu lịch trình đủ trường **có gọi** `lich_trinh`", và `kiem_cuoi` (D8) chỉ có tập điểm / giờ để so khi có khung ⇒ câu model **tự viết lịch không qua công cụ** (đúng lỗi TravelPlanner / TRIPO plan nêu ở §1) không bị code kiểm, cũng không bị Q2 đếm ("mọi lịch trong bộ" — lịch không khung thì so với gì?) | Lỗi tệ nhất của B5 có thể lọt cả sàn lẫn quyết | Thêm sàn ghi trước: câu lịch trình đủ trường (10 đã thấy + 5 kín) **gọi `lich_trinh`** ở mọi câu (hoặc ngưỡng A chọn, vd ≥ 9 / 10, ≥ 5 / 5); câu lịch trình không gọi công cụ ⇒ tính là phạm Q2; ghi hành vi chạy thật khi model không gọi (vd D8 vẫn chạy (2) giờ + (3) giá trên mọi câu `tro_ly_hue` có chữ "ngày 1 / buổi sáng"…, hoặc chỉ ghi giới hạn — A chọn) |
| **M-2** | major | D6 | D6 "`tim_kho(<tên điểm>)` (đường tìm hiện hành) … lấy đoạn đầu tiên trong top-10 có `source` = `nguon`". Đường hiện hành `search_into_trace` **đóng gói cả top-10** vào ngữ cảnh + sổ nguồn mỗi lần tìm (:151–162) và **bỏ đoạn đã thấy** (`skip_ids=frozenset(trace.seen_ids)`, :152). Lượt `tro_ly_hue` đã có 10 đoạn từ lần tìm đầu (B2 `lan_tim_dau: v0`) | Đi đúng chữ "đường hiện hành": ≤ 9 điểm × 10 đoạn ⇒ ngữ cảnh nổ (`ContextBudgetError` ⇒ câu lỗi); đoạn của điểm đã nằm trong lần tìm đầu bị bỏ ⇒ D6 tưởng "không có đoạn" ⇒ **bỏ nhầm điểm khỏi lịch**; D8 (4) cần biết đoạn n của từng điểm | Ghi rõ đường dữ liệu D6: (i) tìm theo điểm chỉ **chọn 1 đoạn** (gọi `retrieval_service.search` rồi dựng ngữ cảnh cho đúng các đoạn chọn, không qua `search_into_trace` nguyên khối); (ii) đoạn đã có trong sổ nguồn ⇒ **dùng lại mã [n] cũ**, không bỏ điểm; (iii) tổng ngữ cảnh = lần tìm đầu + đoạn lịch (≤ 10) — ước token, hành vi khi vượt ngân sách; (iv) một test: điểm có đoạn đã nằm trong lần tìm đầu |
| **M-3** | major | D4, D5, D8 (2) | `gio_mo_cua` trong bảng là **chữ tự do** (10 / 28 điểm có; vd "đóng cửa khoảng …; phố đêm … (kho không ghi giờ mở)", "mở tự do …; khuyến nghị …", "… trong mùa khô (tháng …)"), không phải giờ có cấu trúc. D5 "code **không xếp** điểm vào buổi ngoài giờ có nguồn" và D8 (2) "mọi giờ ∈ tập giờ khung" cần dữ liệu / luật tất định mà plan chưa định nghĩa: buổi nào hợp lệ cho từng điểm, tập giờ khung gồm chuỗi nào, so thế nào (model viết "7 giờ" ↔ khung "07h00"; "5h30" ↔ "5 giờ 30"); regex `\d{1,2}\s*(h\|giờ\|:)\s*\d{0,2}` cũng bắt thời lượng ("đi khoảng 2 giờ") | Sàn Q2 "0 giờ ngoài tập giờ khung" và "0 điểm xếp ngoài giờ có nguồn" không đếm lại được giống nhau giữa người code và người kiểm ⇒ rút lại nhầm hoặc lọt | Ghi trước: (a) luật buổi = cột có cấu trúc (vd `buoi` ⊂ {sang, chieu, toi}, hoặc cột `toi` §5 bước 1 thành **bắt buộc**, sáng / chiều mặc định được trừ khi bảng ghi khác) — User duyệt cùng bảng; (b) tập giờ khung = các cặp (giờ, phút) chuẩn hoá từ chuỗi giờ code đưa vào khung; so sau chuẩn hoá; chữ giờ là thời lượng ⇒ tính vi phạm (lời không nêu thời lượng — D4); (c) ca test cho từng dạng |
| m-1 | minor | D5 (a) | Chữ Quyết 1 "điểm có **tên** trong file vé": một điểm khác của bảng (`chua_thien_mu`) cũng có tên trong file vé Quần thể (1 lần, ở đoạn gợi ý chung, không phải mục vé) — plan loại đúng, nhưng không ghi luật lấy 11 id | Người đọc / User hiểu Quyết 1 theo nghĩa đen sẽ thấy lệch; gán 07h00–17h30 cho điểm ngoài Quần thể là bịa giờ | Ghi luật: "điểm thuộc Quần thể (có mục / giá vé trong file vé)", nêu điểm bị loại và lý do; A báo User một dòng |
| m-2 | minor | §9 | "B3 nhớ chưa bật (B3b đang sửa)" — cũ: B3b merge `9e2ecd9`, nhớ bật (chỉ nhớ câu hỏi) | Điều kiện "nếu nhớ bật trước B5" đã xảy ra nhưng 2 chuỗi theo dõi chưa ghi trước | Sửa câu; ghi trước 2 chuỗi theo dõi (hỏi tiếp sau lịch) như plan nói |
| m-3 | minor | §4 bộ đo | Câu đủ trường "gửi thẳng"; đường **câu ghép B4 D4** ("<câu gốc> (Thông tin thêm: 2 ngày; …)") — nguồn giá trị D1 nêu — không có câu nào trong bộ | Không biết model trích đúng giá trị từ chữ ghép | Thêm ≥ 2 câu đã thấy dạng câu ghép (dựng bằng `ghep_cau` của B4, tất định) |
| m-4 | minor | D8 (1), (3) | (1) "mọi tên điểm bảng xuất hiện trong lời ∈ khung" — lời tả vị trí hay nhắc điểm gần ("gần …") sẽ bị rút lại; (3) "số + nghìn / ngàn" gặp cả câu lịch sử ("hơn … nghìn năm") | Rút lại nhầm (Q5 có theo dõi > 1 / 13) | Ghi sẵn hai dạng báo nhầm này vào D8 "sai khi" + ca test âm; giữ ngưỡng Q5 |
| m-5 | minor | D11 | `query` = `ten` + `vi_tri_can_cu`: cột này là chữ mô tả ("…, phường …, ~… km phía …") — phần khoảng cách / hướng làm truy vấn Maps rộng / lệch; plan đã nêu ở "sai khi" | Link kém hơn cách đơn giản hơn | Cân nhắc `query` = `ten` + ", Huế" (đơn giản hơn, ít lệch); hoặc chỉ phần địa chỉ trước dấu phẩy đầu — ghi lựa chọn |
| m-6 | minor | Căn cứ để review | Hàng `CURRENT_HANDOFF.md` mục "Phiên tối 03/11" — mục đã dời sang `archive/CURRENT_HANDOFF_LICH_SU_2026-11-03_toi.md` (dòng 55 ghi "Quyết 3 đang hỏi"); chốt thời lượng nay ở `CURRENT_HANDOFF.md` "Phiên sau" bước 5 | Người review sau không tìm được căn cứ Quyết 3 | Trỏ đúng hai chỗ |

## 3. Cách người kiểm chạy lại thật

Chỉ lệnh đọc / đếm, 0 USD: `sha256sum` plan + bảng; Python đọc `diem.json` (đếm điểm / cụm / loại / trường có giá trị); `scripts/grep_kb.sh --dir travel/tickets -c -i -F <tên điểm>` cho 28 tên (chỉ số đếm); đọc `assistant.py` :138–200.

## 4. Kết quả quan sát

Như bảng "Đã khớp" + bằng chứng trong từng finding. Không chạy model, Qdrant hay server.

## 5. Giới hạn hoặc phần chưa chạy

- Chưa kiểm định dạng URL Google Maps (plan tự dời sang lúc code, WebFetch).
- Bước 0 D6 (28 điểm có đoạn đúng file trong top-10) chưa chạy — việc của người code (0 USD, đọc Qdrant).
- Không mở bộ đo B5 (chưa có) hay câu kín.

## 6. Decision và bước tiếp theo

**changes_requested** — C sửa M-1, M-2, M-3 (+ minor nếu muốn) thành bản 3, báo sha; B kiểm phần sửa; A duyệt sha. M-1 (ngưỡng "gọi công cụ"; có chạy kiểm giờ / giá trên câu không qua công cụ không) và M-3 (a) (cột buổi vào bảng User duyệt) là chỗ A / User quyết. Plan vẫn chờ B4 merge + bảng điểm User duyệt trước khi chạy — không chặn việc khác.

## Vòng 2 — kiểm phần sửa bản 3 (sha `bba7d2559b77`, B, 20:43 04/11/2026)

Decision: **ready_for_user_confirmation** (0 blocker · 0 major · 0 minor mới) — A chốt trần (đề xuất 0,15 / dừng 0,14) rồi duyệt sha. 0 USD. Cách kiểm: `git diff HEAD` bản 2 ↔ 3 — mọi hunk thuộc bảng "Chỗ đổi bản 3".

| Finding | Kiểm | Kết luận |
|---|---|---|
| M-1 | **Q2a** mới (gọi `lich_trinh` ≥ 9 / 10 mỗi lượt đã thấy, ≥ 4 / 5 kín); câu không gọi vẫn chấm Q2 với khung rỗng; D8 (7) chạy thật trên câu không gọi mà lời có dạng lịch (≥ 2 tiêu đề ngày hoặc ≥ 2 dòng Sáng / Chiều / Tối kèm tên điểm bảng) ⇒ lịch tự viết không còn lọt; giá phải trả (rút nhầm câu thường) có sàn Q4 "≤ 1 / 62" + "sai khi" D8 | **đóng** |
| M-2 | D6 (i) gọi thẳng `retrieval_service.search`, chọn 1 đoạn đúng `source`, không qua `search_into_trace`; (ii) đoạn đã có ⇒ dùng lại `[n]`; (iii) ≤ 20 đoạn, vượt ngân sách ⇒ bớt từ ngày cuối, không thành câu lỗi; (iv) ba ca test. Khớp code hiện hành (`search_into_trace` đóng gói cả top-10 + `skip_ids`) | **đóng** |
| M-3 | cột `buoi` có cấu trúc (mặc định {sáng, chiều}; tối chỉ khi kho ghi) — User duyệt cùng bảng, §5 bước 1 thành bắt buộc; code không đọc chữ `gio_mo_cua`; tập giờ khung = cặp (giờ, phút) chuẩn hoá; D8 (2) liệt kê 6 dạng giờ + thời lượng tính vi phạm + ca test; Q2 "0 suất ở buổi ∉ `buoi`" | **đóng** |
| m-1 … m-6 | D5 (a) ghi luật lấy 11 id + điểm bị loại; §9 hai chuỗi nhớ ghi trước; 2 / 10 câu đủ trường dạng câu ghép; D8 "sai khi" + trừ "nghìn năm"; D11 `ten` + ", Huế" (Q2 so theo đó); căn cứ trỏ đúng archive + handoff | **đóng** |
| §1 "bản đồ" (A) | "bản đồ tương tác / chỉ đường" — hết mâu thuẫn với D11 | **đóng** |
| Tiền | §6 theo giá thật B4 (câu trả lời cờ bật ≈ 0,00075 với 10 đoạn; lịch ≤ 20 đoạn ⇒ ≈ 0,0015 hợp lý); cộng 0,06–0,14; trần đề xuất 0,15 / dừng 0,14 — A chốt | **đóng** (số A chốt) |

**Ghi nhận (không finding):** B4 khoá 2 (`p9-b4` `f8c9914`) gắn câu Cách A vào mọi lượt trợ lý khi cờ `hoi_lai` bật ⇒ lượt B5 cũng mang câu đó khi B4 bật — không đụng luật B5 (Cách A chỉ nói về câu chi phí), nhưng chuỗi gửi model của B5 phải lấy mốc là `main` **sau** B4 merge (Q1 của B5 đã ghi "giống byte B4").

## Vòng 3 — review bản 4 (sha `e176b7478b2d`, E — việc **E3**, 10:02 05/11/2026)

Decision: **changes_requested** (0 blocker · 1 major · 5 minor)
Người kiểm: E (Claude Opus 5.5, `hue-rag-7a`) — người kiểm mới, không đọc STATUS / tin của C. Cách review: gói "Căn cứ để review" của plan +
**spec Phase 9 bản 12 `77250689e605` §11** (A giao: B5 thêm "dòng tiến độ bước thật"; bản đồ sang Phase 11) + lệnh chỉ đọc. 0 USD. Repo public: không chép kho / bộ đo.

### 1. Phạm vi đã review
- Plan bản 4 toàn bộ (sha tính từ file = `e176b7478b2d`, khớp handoff C173); spec bản 12 §3, §4, §5 B4 / B5, §6, §8, **§11.1–§11.5**; review spec bản 10 (`…design_review_v10.md` m-2, m-3, m-4, m-5).
- Bảng `diem_v3.json` (`e94b7f4263f2`) + `diem_cho_user_v3.md` (`76694bbff550`) — khớp sha handoff; plan B4 **bản 8** `69afbb2732cf` (D2, D2′, D4, D10).
- Code: `backend/llm/assistant.py` (`search_into_trace` :126–168, `context_builder.build(..., first_id=…)` :151); `generator_openai_full_corpus.py` (`ASSISTANT_MAX_TURNS = 4` :69);
  nhánh `p9-b4` `990825e` (`StopAtTools(stop_at_tool_names=["hoi_lai"])`); `frontend/src/App.jsx` :9–12 (4 nhãn tiến độ cố định), :106 (sự kiện `status`); `backend/api/routes/chat.py` :350 (`status`), :412–420.

### 2. Ca dò riêng (khác cách người viết) + câu bất biến
- **Luật khớp tên D2** chạy lại trên `diem_v3.json` bằng script riêng (NFC + casefold + gộp khoảng trắng + bỏ " Huế" khi còn ≥ 2 chữ; khoá = `id` ∪ `ten` ∪ `ten_khac`):
  **110 khoá, 0 khoá trỏ hai điểm**; "Lycée Khải Định" không khớp khoá nào ⇒ luật D2 làm được như chữ plan.
- 11 id D5 (a) đều có trong bảng; 8 cụm §2b = đúng 8 cụm của bảng (không thừa / thiếu); cột `buoi`: 24 điểm {sáng, chiều} · 3 điểm chỉ {tối} · 1 điểm {sáng, chiều, tối};
  `luu_y` 2 điểm; "17h30" có trong file vé Quần thể (`scripts/grep_kb.sh --dir travel/tickets -c -F`, chỉ số đếm).
- **Câu bất biến:** cờ `lich_trinh` tắt ⇒ chuỗi gửi model giống byte `main` sau B4b — Q1 của plan giữ đúng (mốc "B4" nay là B4b).

**Đã khớp (không finding):** D1 dùng đúng 4 trường lịch trình + giá trị của B4 D2 — B4b bản 8 chỉ bỏ `chi_phi` / `so_nguoi` / `muc_chi` (D2′), không đổi trường lịch trình;
D6 làm được với code hiện hành (`retrieval_service.search` + `context_builder.build(..., first_id=…)`); D11 chỉ là **link** do code dựng, không toạ độ, không tile, không đổi CSP
⇒ khớp spec §11 "plan B5 bản 4 giữ 'không bản đồ'" (C178 đóng m-4 cùng nghĩa); bảng "Chỗ đổi bản 4" phủ đủ 9 ý #1–#7, #12, #18; Q2a / Q2 / Q3 / Q4 giữ sàn spec §4 / §5 B5; tiền trần 0,15 = spec §11.5.
**Ý kiến về "Lệch chữ #3" (D2b — plan nhờ reviewer chọn):** E đề xuất **giữ cách bản 4** (code nối nguyên câu theo mã luật). Lý do: đúng khung spec §11.3 "luật ⇒ code";
bài học B4 cho thấy dặn model "nhớ nhắc" thì không chặn được lỗi. Câu kém tự nhiên là cái giá chấp nhận được. Cách #3 nguyên văn cần thêm D8 (8) đọc chữ model ⇒ thêm chỗ báo nhầm.

### 3. Findings

| Mã | Mức | Vị trí | Bằng chứng | Tác động | Tiêu chí đóng |
|---|---|---|---|---|---|
| **M-1** | major | thiếu (D…, §3, §4) | Spec bản 12 §11.1 "**B5** thêm (i) dòng tiến độ dùng bước thật … các bước của `lich_trinh` ('đang xếp lịch', 'đã kiểm luật ✓', 'bỏ 1 điểm vì …') **chỉ phát khi code đã làm bước đó**. Kiểm: Playwright + so danh sách sự kiện SSE". Plan bản 4 (viết 09:07, trước spec bản 11) không có quyết định, file, test hay tiêu chí nào cho việc này. Hôm nay giao diện chỉ có 4 nhãn cố định (`App.jsx:9–12`), sự kiện `status` do lõi phát (`chat.py:350`, :420). Công cụ chạy **bên trong** `Runner.run_streamed` ⇒ cần một đường để code trong `lich_trinh` đẩy sự kiện ra luồng SSE — đường này chưa có | Thiếu một hành vi bắt buộc của bậc. Nếu không ghi trước thì dễ thành bước giả (phát "đã kiểm ✓" trước khi `kiem_khung` chạy), đúng lỗi spec muốn tránh | Thêm một D mới: (a) danh sách bước = sự kiện do code phát **sau** việc thật: bắt đầu `xep` ⇒ "đang xếp lịch"; `kiem_khung` trả **0 lỗi** ⇒ "đã kiểm luật ✓" (lỗi ⇒ không phát ✓); mỗi mục `khong_xep` ⇒ "bỏ <điểm> vì <chữ theo mã luật D2b>" (cùng bảng hằng); (b) đường dữ liệu từ công cụ tới SSE (vd hàng đợi trong `AnswerTrace` mà `answer_turn_stream` đọc) + nhãn mới ở `App.jsx` (dùng lại sự kiện `status`, review v10 m-2); (c) §3 thêm file; (d) test: khung có `khong_xep` ⇒ có đúng sự kiện "bỏ …"; `kiem_khung` lỗi ⇒ không có "✓"; cờ tắt ⇒ chuỗi sự kiện giống `main`; (e) Q2 thêm sàn "**0 sự kiện tiến độ không khớp việc code đã làm**" (so log sự kiện SSE ↔ khung) + Q8 / cổng: Playwright thấy các dòng |
| m-1 | minor | dòng đầu "Spec: bản 9 `169c2dd5f86a`"; Căn cứ hàng 2 + hàng 5; §1 "Phụ thuộc"; §1 "Không làm" ("chi phí là B4 Cách A") | Spec nay là bản 12 `77250689e605` (§11 đổi bậc); B4 nay là B4b — plan bản 8 `69afbb2732cf`; Cách A đã bỏ, chi phí thành **B5c** (spec §11.1); §1 "A / User chưa chốt hướng" đã cũ (User chọn "Tách — giữ lịch trình") | Người review / code sau đối chiếu sai bản | Trỏ spec bản 12 (+ §11) và plan B4 bản 8; §1 sửa câu tình trạng B4 + "chi phí ⇒ B5c" |
| m-2 | minor | §7 dòng cuối "Luật cắt spec §6 (4): 07/12 B5 chưa đóng ⇒ dừng B5" | Spec §11.4 **thay** §6 (1)–(5): luật mới "23/11 B5 chưa merge ⇒ B5c thu nhỏ còn vé" (không còn luật dừng B5 07/12); lịch B5: code 05–09/11, đo + merge 10–16/11 | Điều kiện dừng lệch lịch đã duyệt | Chép luật cắt §11.4 phần chạm B5 |
| m-3 | minor | D8 (3) "dùng chung bộ nhận số tiền với `dem_tong.py` B4" | `dem_tong.py` nằm ở `data/phase_9/b4/tools/` (private, không tracked) ⇒ code chạy (`backend/llm/lich_trinh.py`) không được import từ `data/` (bản clone không có). B5c (spec §11.2 sàn (1)) cũng cần đúng bộ nhận này | Code chạy phụ thuộc file private, hoặc hai bản regex lệch nhau | Ghi: bộ nhận số tiền là **một hàm trong `backend/`** (vd `backend/llm/so_tien.py`, B5c dùng lại); script đo import từ `backend`, không làm ngược lại |
| m-4 | minor | D1 trần ≤ 1; spec §3 "max_turns 3–4" | `ASSISTANT_MAX_TURNS = 4` (`generator_openai_full_corpus.py:69`, chú thích "≤ 2 lần tìm + lần 3 'đã hết lượt' + 1 lượt viết"). Lượt có lịch: model có thể gọi `tim_kho` (dù D6 tự lấy đoạn) rồi `lich_trinh` rồi viết ⇒ chạm trần ⇒ câu từ chối `max_turns`, mất lịch | Lịch đúng bị thay bằng câu từ chối mà Q2a chỉ đếm là "có gọi công cụ" | Ghi số `max_turns` cho lượt có `lich_trinh` (giữ 4 hay 5 — lý do); Q5 đếm `outcome=max_turns` ở câu lịch trình; test: chuỗi lời gọi `tim_kho` ×2 + `lich_trinh` ⇒ vẫn ra lời |
| m-5 | minor | D12 (a) "code nối **đầu** câu trả lời"; Q5 "chữ đầu"; §6 tiền | Spec §3: "chữ đầu = chữ trả lời, không tính dòng trạng thái". Dòng "Mình hiểu…" do code nối trước chữ model ⇒ nếu đo chữ đầu tại dòng này thì số đẹp giả. Thêm: spec §11.5 luật **quỹ B7** (trước mỗi bậc: 2,0 − đã dùng − 0,35 ≥ ước bậc, không thì A xin User trước) chưa có ở §6 | Số chữ đầu của câu lịch không so được với bậc trước; thiếu bước kiểm tiền trước khi chạy | Q5: chữ đầu câu lịch = **chữ đầu của model** (ghi riêng thời điểm dòng code); §6 thêm một dòng điều kiện quỹ B7 trước pilot |

### 4. Giới hạn
- Không chạy model, Qdrant, server, Playwright; bước 0 D6 (28 điểm có đoạn đúng file) là việc người code.
- Không mở bộ đo B5 (chưa có) hay câu kín; chưa kiểm `ghep_cau` trên nhánh `p9-b4` (plan chỉ dùng tên).
- Bảng v3 **chưa User duyệt** (handoff "Câu hỏi cho User" 3) — plan đã ghi đúng: không chạy có phí trước khi duyệt.

### 5. Decision và bước tiếp
**changes_requested** — C sửa M-1 (+ minor) thành bản 5, báo sha; E kiểm phần sửa; A duyệt sha. M-1 không chặn phần code D1–D13 khác, nhưng phải có trong bản khoá trước lượt đo.

## Vòng 4a — kiểm phần sửa bản 5 (sha `dff61a2db4e6`, E, 10:07 05/11/2026)

Decision (tạm, **bị thay**): ready_for_user_confirmation cho bản 5 (0 blocker · 0 major · 1 minor mới). **A báo sau đó: User chọn hướng B4b mới (cờ `hoi_lai` tắt; B5 tự trả thẻ hỏi lại khi thiếu `so_ngay`) ⇒ C ra bản 6 ⇒ A không duyệt sha bản 5; kết luận cuối ở "Vòng 5" (phần sửa 5 ⇒ 6).** Phần kiểm dưới đây dùng lại cho vòng 5 nếu đoạn đó không đổi. 0 USD.
Cách kiểm: sha tính từ file = `dff61a2db4e6`; so từng dòng bản 4 (`git show HEAD:…` = `e176b7478b2d`) ↔ bản 5 bằng difflib theo từ — mọi đoạn đổi thuộc bảng "Chỗ đổi bản 5", không đổi ngoài phạm vi; `git diff --check` sạch;
đối chiếu D14 với code `backend/llm/assistant.py:389–448` (`answer_turn_stream`: nhánh `run_item_stream_event` `tool_called` ⇒ `status searching`, `tool_output` ⇒ `status searched`) và `frontend/src/App.jsx:9–12, 107` (trạng thái lạ giữ nhãn "đã tìm").

| Finding | Kiểm | Kết luận |
|---|---|---|
| M-1 dòng tiến độ | **D14**: bước ghi vào `trace.buoc_lich` trong công cụ **sau** việc thật; `kiem_luat_ok` chỉ khi `kiem_khung` 0 lỗi (lỗi ⇒ `kiem_luat_loi`, không ✓); `bo_diem` theo bảng hằng D2b; đường tới SSE = nhánh `tool_output` sẵn có đọc `buoc_lich` ⇒ `status` `stage = lich_trinh` (dùng lại sự kiện, không sự kiện mới); nhãn `App.jsx`; log `lich_trinh_buoc`; test thứ tự + ca khung lỗi không có ✓ + cờ tắt giống byte; Q2 sàn "0 sự kiện không khớp việc code"; Playwright bước 8. Làm được với code hiện hành; "phát sau khi công cụ xong" có ghi ở "sai khi" | **đóng** |
| m-1 | dòng Nền + Căn cứ trỏ spec bản 12 `77250689e605` (§11.1, §11.4, §11.5) + plan B4 bản 8 `69afbb2732cf`; §1 chi phí ⇒ B5c; tình trạng B4 = B4b (kín B4b đạt — khớp handoff dòng C180) | **đóng** |
| m-2 | §7: luật cắt §11.4 (23/11 B5 chưa merge ⇒ B5c thu nhỏ; không còn luật dừng B5 07/12) | **đóng** |
| m-3 | D8 (3) + §3: `backend/llm/so_tien.py`, B5c dùng lại; script trong `data/` import từ `backend` | **đóng** |
| m-4 | D1: giữ `ASSISTANT_MAX_TURNS = 4` + lý do (nới trần đổi mọi câu ⇒ hồi quy 208); test `tim_kho` ×2 + `lich_trinh`; Q5 đếm `max_turns` ở câu lịch, > 1 / 13 ⇒ báo A | **đóng** |
| m-5 | D12 (a) + Q5: chữ đầu = chữ model, ghi riêng thời điểm dòng code; §6 kiểm quỹ B7 trước pilot, thiếu ⇒ A xin User / thu nhỏ | **đóng** |
| D2b | "A quyết giữ code nối nguyên câu" | ghi nhận |

**Minor mới (không chặn — sửa lúc code hoặc A cho bỏ):**

| Mã | Vị trí | Bằng chứng | Tiêu chí đóng |
|---|---|---|---|
| m-6 | D14 (a)–(b) | Nhánh chung `assistant.py:445–448` phát `status searching` ("Đang tìm trong kho…") ở **mọi** `tool_called` và `searched` ở mọi `tool_output`, không xét tên công cụ. D14 thêm sự kiện `lich_trinh` nhưng không nói nhánh chung có còn chạy cho `lich_trinh` không ⇒ lượt có lịch có thể hiện "Đang tìm trong kho…" trước "đang xếp lịch", trái với thứ tự test D14 ghi (`tool_called` ⇒ `xep_xong` ⇒ …). Cùng mẫu: `hoi_lai` (B4b) hôm nay cũng đi nhánh chung | D14 ghi: `tool_called` / `tool_output` **của `lich_trinh`** (xét tên công cụ) ⇒ chỉ phát sự kiện `lich_trinh`, không phát `searching` / `searched`; test thứ tự khẳng định không có `searching` giữa `tool_called` của `lich_trinh` và `xep_xong`. (`hoi_lai` hiện "đang tìm" — ngoài phạm vi B5, ghi để A xem) |

**Bước tiếp:** chờ bản 6 (C) ⇒ E kiểm 5 ⇒ 6 ở "Vòng 5"; m-6 = việc lúc code (A). Không duyệt sha bản 5.

## Vòng 5 — kiểm phần sửa bản 5 ⇒ 6 (sha `46c1ec1a8242`, E, 10:13 05/11/2026)

Decision: **changes_requested** (0 blocker · 1 major · 2 minor). 0 USD.
Cách kiểm: sha tính từ file = `46c1ec1a8242`; đọc mục "Chỗ đổi bản 6" + từng đoạn được nêu (Nền, §1, D1, D7, D14 (b), D15, §3, Q1m, Q4, §7); `git diff --check` sạch;
đối chiếu code nhánh B4b `990825e`: `backend/api/routes/chat.py:65` (`truong: TruongInput | None`, chú thích "`{}` = 'Trả lời luôn'"), :116–120 (`_model_query`: có `truong` ⇒ `da_co_truong`, không gắn cờ — khớp lời C);
`frontend/src/App.jsx:385, 410` (thẻ: "Trả lời luôn" gửi `truong: {}`); `backend/llm/generator_openai_full_corpus.py:96–97, 366–381` (`clarify` + `StopAtTools(["hoi_lai"])` đặt trong `_assistant_for`).
Phần vòng 4a (M-1 / D14, m-1…m-5) không đổi ngoài D14 (b) ⇒ dùng lại kết luận "đóng".

| Mục | Kiểm | Kết luận |
|---|---|---|
| (1) Nền / §1: B4b cờ tắt, dùng lại đường `clarify` / `truong` / thẻ | `_model_query` không gắn cờ (đúng); **Lệch** spec §11.1 dòng B4b ghi + "User duyệt 10:07 05/11/2026" (theo tin A) | khớp |
| (3) D7: luật trình bày ở mô tả công cụ + đầu `khung_chu`, không lời dặn hệ thống | có lý do (bài học B4b), Q1m đo được | khớp — xem m-7 về ngân sách |
| (4) Q1m | "cờ bật, câu không lịch trình chỉ khác `main` một mục công cụ" — kiểm được bằng so cấu trúc yêu cầu | khớp |
| (5) Q4 thủ tục S-AT | 4 số + 3 + 3 lần sinh lại, 2 judge mù, đạt ⇔ B5 ≤ mốc mọi câu | khớp |
| (6) m-6 | D14 (b): `tim_kho` giữ `searching` / `searched`, `lich_trinh` chỉ phát sự kiện `lich_trinh`; test "0 `searching` giữa…" | **đóng** |
| (2) D15 | xem M-2 | **mở** |

| Mã | Mức | Vị trí | Bằng chứng | Tác động | Tiêu chí đóng |
|---|---|---|---|---|---|
| **M-2** | major | D15 (1)–(4) + câu "Lượt ghép có `truong` ⇒ không bao giờ hỏi lần hai (luôn có `so_ngay`)" | Thẻ B4b có nút **"Trả lời luôn" gửi `truong: {}`** (`App.jsx:410`, `chat.py:65`) ⇒ lượt ghép **không có `so_ngay`**. Theo D15: (1) `truong.so_ngay` trống · (2)–(3) model / dò số không có (câu gốc đã thiếu số ngày — chính vì thế mới hỏi) · (4) ⇒ **hỏi lại lần nữa**. Thẻ D15 chỉ có `so_ngay` nên người bấm "Trả lời luôn" lần hai lại nhận đúng thẻ đó ⇒ **vòng hỏi không dứt**. Câu khẳng định "luôn có `so_ngay`" sai với code B4b | Lặp đúng loại lỗi đã thấy ở B4 (Q7 g2: hỏi lại lần hai — lý do tách B4b); người dùng không có lối ra trừ gõ số ngày | D15 ghi luật cho lượt `da_co_truong` mà thiếu `so_ngay`: **không hỏi lại** — chọn một trong hai và ghi trước: (a) xếp với giá trị mặc định công khai (vd 1 ngày) + câu giả định trong khối D4b ("chưa biết số ngày nên gợi ý 1 ngày — bấm Sửa", D12); hoặc (b) thẻ D15 **không có** "Trả lời luôn" (chỉ "Gửi") — ghi lệch so với thẻ B4b. Thêm test: lượt `truong: {}` + câu không số ngày ⇒ **0 `clarify`**; thêm 1 chuỗi Q7-kiểu vào bộ đo (lịch thiếu số ngày ⇒ "Trả lời luôn" ⇒ có lịch, không thẻ) |
| m-7 | minor | D7 (luật trình bày chuyển vào **mô tả công cụ**) ↔ ngân sách ngữ cảnh | B4 phải cộng lược đồ công cụ vào ngân sách (`HOI_LAI_TOOL_OVERHEAD`, `assistant.py` `extra_tool_tokens` trên `990825e`); "A còn nợ" (handoff): đếm token không tính mô tả công cụ. Cờ bật ⇒ mô tả `lich_trinh` đi vào **mọi** lượt trợ lý | Bộ dựng ngữ cảnh đếm thiếu ⇒ có thể vượt trần thật mà không biết | §3: cộng token mô tả + lược đồ `lich_trinh` vào ngân sách (như B4); Q5 `usage − builder` ghi riêng cho câu không lịch trình khi cờ bật |
| m-8 | minor | §3 hàng `assistant.py` "`tool_use_behavior` dạng hàm"; §5 bước 3 probe | `tool_use_behavior` đặt trong `generator_openai_full_corpus.py` `_assistant_for` (:366–381), nhánh đọc `clarify` cũng ở generator (:96–97) — §3 không liệt kê file này. Hàm thay `StopAtTools` áp cho **mọi** lời gọi công cụ của lượt | Sót file; hàm dừng sai ⇒ lượt dừng ở `tim_kho` (mất câu trả lời) | §3 thêm `generator_openai_full_corpus.py`; test hàm: kết quả `tim_kho` ⇒ chạy tiếp · `lich_trinh` có khung ⇒ chạy tiếp (lượt viết) · `lich_trinh` dấu "cần hỏi" ⇒ dừng + `clarify` |

**Bước tiếp:** C sửa M-2 (+ m-7, m-8) thành bản 7, báo sha; E kiểm phần sửa (vòng 6). A chưa duyệt sha.

## Vòng 6 — kiểm phần sửa bản 6 ⇒ 7 (sha `b572443dc9cd`, E, 10:16 05/11/2026)

Decision: **ready_for_user_confirmation** (0 blocker · 0 major · 0 minor mới) — A duyệt sha. 0 USD.
Cách kiểm: sha tính từ file = `b572443dc9cd`; `git diff --check` sạch; đọc "Chỗ đổi bản 7" + D15, D16, §3 (hàng `full_corpus_context.py`, `generator_openai_full_corpus.py`), tests (dòng 88), Q2 (dòng 103);
đối chiếu nhánh B4b `990825e`: `backend/retrieval/full_corpus_context.py:54, 68, 107, 119` (tham số `extra_tool_tokens` có sẵn, cộng vào số đếm), `backend/llm/assistant.py:165` (B4 dùng `HOI_LAI_TOOL_OVERHEAD`).

| Finding | Kiểm | Kết luận |
|---|---|---|
| **M-2** "Trả lời luôn" ⇒ hỏi không dứt | D15 (A quyết (a)): lượt mang `truong` **không bao giờ hỏi lần hai**; `truong` rỗng / thiếu `so_ngay` ⇒ `so_ngay = 1` + dòng giả định cố định do code ("tạm xếp 1 ngày — bấm Sửa") + "Mình hiểu: 1 ngày (tạm)"; bước (4) hỏi chỉ khi lượt **không** mang `truong` ⇒ hết vòng lặp. Test "`truong: {}` ⇒ 0 `clarify`, có lịch 1 ngày + dòng giả định"; Q2 sàn chuỗi "thiếu ngày ⇒ thẻ ⇒ Trả lời luôn" ≥ 2 chuỗi (server thật + cookie) ⇒ 0 hỏi lần hai. Giá phải trả ("lịch 1 ngày có thể không đúng ý") ghi ở "sai khi" | **đóng** |
| m-7 ngân sách | D16: `LICH_TRINH_TOOL_OVERHEAD` vào `extra_tool_tokens` (tham số có thật — trên) mọi lượt có công cụ khi cờ bật; đo ở pilot (token thật − số đếm); test khoá sha mô tả ⇒ đổi mô tả thì đo lại | **đóng** |
| m-8 file + hàm dừng | §3 thêm `generator_openai_full_corpus.py` `_assistant_for`; test hàm 3 nhánh (`tim_kho` chạy tiếp · `lich_trinh` có khung chạy tiếp · "cần hỏi" dừng + `final_output` là thẻ, client giả SDK) | **đóng** |

**Câu bất biến kiểm lại:** cờ `lich_trinh` tắt ⇒ chuỗi gửi model giống byte `main` (Q1); cờ bật, câu không lịch trình ⇒ chỉ khác một mục công cụ (Q1m) — bản 7 không đổi hai mục này.
**Phạm vi vòng này:** chỉ phần sửa 6 ⇒ 7 (A giao); phần khác dùng lại kết luận vòng 3–5. Vẫn chờ bảng v3 User duyệt + B4b merge trước lượt có phí.
