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
