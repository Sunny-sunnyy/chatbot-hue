# Review: nhánh `p9-tra-web-exa` — phần code + test (0 USD)

Decision: **ready_for_user_confirmation cho phần 0 USD** (0 blocker · 0 major · 6 minor). Phần đo có phí X2–X6 của plan **chưa chạy** — không thuộc review này; cờ mặc định vẫn Serper.
Người kiểm: B (`hue-rag-1b`, Claude Code — Fable 5.2). Date: 21:35 12/11/2026 (`date`).
Bản được review: `origin/p9-tra-web-exa` **`4b37051`** (1 commit, từ `main` `547a405`; người làm: E). Plan: `docs/superpowers/plans/2026-11-12-tra-web-exa-plan.md` bản 2.

## 1. Phạm vi đã review

Cổng tối thiểu: commit gốc + danh sách file (6 file, +272 / −4); đọc hết diff; `git diff --check` sạch; đối chiếu với plan §1, §4 X1 / X5, §5. Chạy lại (worktree tạm, đã gỡ): test chạm, Q1, thử gộp. Không chạy lượt có phí, không gọi Exa / Serper.

## 2. Đối chiếu tiêu chí A giao

| Điểm kiểm | Kết quả | Bằng chứng |
|---|---|---|
| Cờ mặc định `serper` giống hôm nay | **đạt** | đường mặc định của `_tim_web_server` gọi đúng `tim_web(cau, api_key=…, timeout=…)` như cũ; Q1 228 / 228 **giống byte `main`** (`cmp` với bản chụp `main` cùng buổi); test `test_default_source_is_serper_as_before` |
| Hạn Exa 3 s + Serper dự phòng | **đạt** | `tim_web_exa_truoc`: Exa chạy với `min(exa_timeout, timeout)`; lỗi / hết giờ / 0 kết quả ⇒ đúng **một** lần Serper với phần còn lại tính từ thời gian thật đã trôi; còn < 0,5 s ⇒ không gọi; test cho 402, 0 kết quả, lỗi mạng, hết giờ ở hạn riêng, cả hai cùng hỏng, hết thời gian |
| Trần 40 lượt / ngày | **đạt** | bộ đếm trong RAM theo ngày, kiểm + tăng trước `await` (không chen được trong một vòng lặp sự kiện); vượt ⇒ Serper; test với trần 2 |
| Thiếu khoá ⇒ Serper | **đạt** | thiếu `EXA_API_KEY` ⇒ không mở kết nối Exa, đi Serper, `nguon = "exa>serper"`; test |
| Không lộ khoá trong log | **đạt** | khoá đọc trong hàm mỗi lần tra (không nằm trong `repr` của hàm đóng); `KetQuaWeb` không chứa khoá; diff không thêm lệnh log nào; khoá chỉ đi trong header `x-api-key` |
| Một nơi duy nhất gọi ra web | **đạt theo grep** | địa chỉ Exa chỉ có ở `backend/llm/tra_web.py` — nhưng chưa có test khoá điều này (m-1) |
| Test | **112 đạt** không khoá (18 s) và **112 đạt** có `--env-file` (17 s) | `tests/test_tra_web_exa.py`, `test_settings_env.py`, `test_b6_tra_web.py` |
| Gộp với nhánh "hết lượt tìm" | **sạch** | `git merge-tree origin/p9-het-luot-tim origin/p9-tra-web-exa` không xung đột (hai nhánh thêm dòng ở hai chỗ khác nhau của khối `assistant:`) |

## 3. Findings (đều minor — sửa khi làm phần đo, không chặn)

- **m-1 — thiếu test ranh giới plan đã ghi** (plan §1 dòng "test": "chỉ `tra_web.py` có địa chỉ Exa"). Hôm nay đúng theo `grep`, nhưng không có test giữ. Tiêu chí đóng: một test quét `backend/` (trừ `tests/`) như test ranh giới của B6.
- **m-2 — trường `nguon` chưa vào log `chat_metrics`** (plan tự ghi là làm sau khi nhánh "hết lượt tìm" merge). Tiêu chí X5 ("`nguon: exa>serper`" ở lượt thật) **không kiểm được** cho tới khi có ⇒ làm trước lượt có phí X5; thêm test khoá tập trường log.
- **m-3 — trần / ngày đếm lượt THỬ, theo ngày của máy, trong RAM một tiến trình:** lượt thiếu khoá hoặc Exa lỗi cũng tốn một suất; `date.today()` là giờ máy (bản Docker thường là UTC ⇒ "ngày" đổi lúc 07:00 giờ Việt Nam); nhiều tiến trình ⇒ trần nhân lên; khởi động lại ⇒ đếm lại từ 0. Đủ dùng cho mục đích "không vượt tín dụng miễn phí" vì còn mã 402 ⇒ Serper, nhưng nên ghi 3 ý này vào chú thích `settings.yaml` / checklist deploy.
- **m-4 — hạn giờ là theo từng pha của `httpx`, không phải tổng:** `timeout=3` áp riêng cho kết nối / đọc ⇒ một lượt Exa có thể vượt 3 s tổng. Cùng kiểu với Serper hôm nay (không phải lỗi mới) và phần dự phòng tính bằng thời gian thật nên không gọi Serper khi hết hạn chung; nhưng "tra p95 ≤ 5 s" (X4) phải đo bằng thời gian thật, không suy từ cấu hình.
- **m-5 — kết quả Exa không có tiêu đề bị bỏ:** `doc_ket_qua_exa` đòi `title` là chuỗi. B chưa kiểm trên phản hồi thật của thí nghiệm 12/11 có bao nhiêu kết quả `title` rỗng / null ⇒ E đếm trên dữ liệu đã ghi (0 USD); nếu đáng kể thì dùng tên miền làm tiêu đề thay vì bỏ.
- **m-6 — tiền Exa ghi theo `costDollars.total` kể cả khi đang trong tín dụng miễn phí** ⇒ `usd` trong log tăng ~0,007 / lượt web dù tiền thật là 0; đúng như plan §3 đã nêu, chỉ cần ghi rõ trong báo cáo đo để số "USD / câu" không bị hiểu nhầm.

Không thấy thay đổi ngoài phạm vi; không over-engineering (2 hàm + 1 nhánh chọn nguồn; không thêm lớp trừu tượng). Test dùng phản hồi ghi sẵn qua `MockTransport` và ghi rõ "không phải bằng chứng Exa thật trả đúng" — đúng mức cho logic thuần.

## 4. Giới hạn của review

Không gọi Exa thật ⇒ khuôn phản hồi thật (tên trường, `costDollars`) chỉ dựa trên phản hồi ghi sẵn của người làm. Không kiểm phần đo X2–X6, không kiểm chất lượng mục web. Câu hỏi quyền riêng tư (câu hỏi thật của người dùng tới Exa — plan §5) là việc A hỏi User trước khi bật, không thuộc code.

## 5. Bước tiếp theo

E sửa m-1, m-2 trước lượt có phí; m-3…m-6 ghi vào report đo. Rebase sau khi nhánh "hết lượt tìm" có kết luận (gộp thử: sạch).
