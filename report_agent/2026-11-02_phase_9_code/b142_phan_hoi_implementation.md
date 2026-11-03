# Implementation Report: B142 — nút đánh giá 👍 / 👎 + câu ngoài phạm vi kèm nút gợi ý

Người làm: B (Claude Opus 5.5, `hue-rag-32`) · việc **B142** (A giao; User chọn từ nghiên cứu sản phẩm thật `bao_cao_he_thong/BAO_CAO_NGHIEN_CUU_PHASE_9.md` mục 00: "chỉ lưu đánh giá") · 19:34 03/11/2026 (`date`).
Nhánh **`p9-phan-hoi`** từ `main` `9e2ecd9`, worktree `/tmp/b_phanhoi`, commit **`6f45f58`** (đã push). Chưa merge. Report tracked: không chép kho / Golden; câu thử tự viết. Dữ liệu: `data/phase_9/b142/` (private).

## 1. Thay đổi (`git diff 9e2ecd9..6f45f58`, 6 file, +243 / −13)

| File | Thay đổi |
|---|---|
| `backend/api/feedback.py` (mới) | `FeedbackTurns`: mã lượt `secrets.token_urlsafe(12)` (16 ký tự) ⇒ {tuyến, outcome, số nguồn được trích}, RAM, trần 2.000 (bỏ cũ nhất), mất khi khởi động lại; `POST /api/feedback` `{turn_id, rating: up|down}` (`extra="forbid"`, khuôn mã `^[A-Za-z0-9_-]{16}$`) ⇒ 422 sai khuôn, 404 mã lạ, 200 + **một dòng log** `chat_feedback` (`FEEDBACK_FIELDS` = mã lượt, tuyến, outcome, số nguồn, đánh giá) |
| `backend/api/app.py` | gắn router + `app.state.feedback_turns` (trong `create_app`, không cần lifespan) |
| `backend/api/routes/chat.py` | `ChatResponse.turn_id`; stream: `done` mang `turn_id` **chỉ** ở lượt có câu trả lời cuối (thường + câu cố định), không ở lượt lỗi / bị rút lại; không truyền hàm cấp mã ⇒ `done` như cũ (test cũ giữ nguyên) |
| `frontend/src/App.jsx`, `index.css` | dưới mỗi lượt xong có mã: "Câu trả lời có hữu ích không?" + 2 nút **biểu tượng SVG** (không emoji — lượt Playwright 1 thấy nút trống vì máy thiếu font emoji), `aria-pressed`, đổi ý được, bấm lại cùng nút không gửi; lỗi ⇒ dòng báo nhẹ, giữ lựa chọn cũ, ô hỏi không khoá. Câu `out_of_scope` ⇒ "Bạn có thể hỏi, ví dụ:" + 3 nút cố định (Đại Nội — trang phục · lễ hội Điện Huệ Nam — thời gian · Nhã nhạc — giờ diễn; đã kiểm có trong kho bằng `scripts/grep_kb.sh`), bấm = hỏi luôn. CSP giữ, 0 gói npm mới |
| `backend/tests/test_feedback.py` (mới, 4 test) | `/api/chat` ⇒ `turn_id` ⇒ 👍 rồi 👎 ⇒ 2 dòng log đúng tập trường, không chữ câu hỏi / trả lời / `conversation_id`; 5 thân sai ⇒ 422, mã lạ ⇒ 404; mã ngẫu nhiên + trần RAM; `done` có / không có `turn_id` theo loại lượt |

Không đổi model, lời dặn, tìm kho, `settings.yaml`. Đánh giá **không** vào lịch sử cuộc trò chuyện, không gửi model.

## 2. Đã chạy thật

- Test: `test_feedback.py`, `test_chat_stream.py`, `test_b3_memory.py`, `test_api_chat.py`, `test_static_ui.py` ⇒ **47 / 48** (1 = `test_health_is_cached_and_ready_after_real_lifespan` cần khoá API, bẫy đã biết). `npm ci && npm run build`.
- **Playwright trên server thật** (uvicorn cổng 8854 từ worktree, `settings.yaml` của `main` — nhớ bật; `data/phase_9/b142/ui_b142.py`, `ket_qua_ui.json`, ảnh `anh/`; lượt 1 emoji ở `anh_lan1_emoji/`). Lượt 2 (bản `6f45f58`):

| Kiểm | Kết quả |
|---|---|
| 👍 ⇒ 👎 (đổi ý) ⇒ bấm lại 👎 | 2 yêu cầu `/api/feedback`, cả hai **200**; lần bấm lại không gửi; `aria-pressed` đúng; chữ "Cảm ơn bạn đã đánh giá." |
| Log | 2 dòng `chat_feedback` đúng 5 trường (tuyến `tro_ly_hue`, `success`, số nguồn 8, `up` rồi `down`); 3 dòng `chat_metrics` = 3 lượt; grep chữ câu hỏi / tên món / `conversation_id` trong dòng log mới = **0** |
| Câu ngoài phạm vi | 3 nút gợi ý; bấm nút đầu ⇒ đúng 1 yêu cầu stream mới, câu hỏi hiện đúng chữ nút, có câu trả lời có nguồn |
| **Lỗi mạng thật** (tắt server bằng TaskStop rồi mới bấm 👍) | dòng "Chưa gửi được đánh giá — bạn thử lại sau nhé." hiện, nút không chuyển sang đã chọn, ô hỏi vẫn dùng được |
| CSP · request ra ngoài · điện thoại 390 | **0 · 0** · không cuộn ngang |

Tiền: lượt 1 0,0011 + lượt 2 0,0011 ⇒ **≈ 0,0022 USD**. Không đo latency.

## 3. Giới hạn / chưa làm

- Mã lượt nằm trong RAM: khởi động lại server ⇒ đánh giá lượt cũ trả 404 (giao diện báo nhẹ); đánh giá chỉ là dòng log, chưa có công cụ đọc / tổng hợp (đọc bằng grep `chat_feedback` khi cần).
- Không chặn bấm nhiều lần bằng script (một người dùng, chạy local); mỗi lần đổi ý thêm một dòng — dòng sau cùng của một mã là ý cuối.
- Câu gợi ý cố định (không theo ngữ cảnh câu bị từ chối) — đúng phạm vi A giao.
- Câu khẩn cấp cũng có nút đánh giá (mọi lượt có câu trả lời cuối) — đổi nếu A / User muốn ẩn.

**Giải thích ngắn:** mỗi câu trả lời có hai nút "hữu ích / chưa hữu ích"; bấm thì server ghi một dòng log chỉ gồm mã lượt ngẫu nhiên, loại câu, số nguồn và đánh giá — không lưu chữ. Câu ngoài phạm vi giờ kèm 3 câu gợi ý bấm là hỏi.
