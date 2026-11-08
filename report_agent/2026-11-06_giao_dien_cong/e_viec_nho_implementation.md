# Implementation Report: việc nhỏ trước đóng gói (Nhóm 1 + 2, phần E)

Người làm: E (Claude Code, `hue-rag-22`) · Date: 10:26 08/11/2026
Nhánh `p11-viec-nho-e` `45b3710` (2 commit trên `main` `1611d34`, đã push) · 6 file +106 / −24 · Tiền ≈ **0,0055 USD** (trần 0,01)

## 1. Phạm vi

A giao (User 08/11 duyệt "Nhóm 1 + 2"): (2) giới hạn 500 ký tự + đếm · (5) gợi ý cách hỏi dưới câu từ chối của kho · (7) nút Dừng + server huỷ lần gọi
model · (12) lỗi stream không do SDK cũng huỷ model · (+) dòng Nguồn gộp theo bài · (9) khẩn cấp ô `tel:` + ẩn 👍/👎.

- **(9) GÁC** theo A (User đang bàn đổi định tuyến). Code (9) đã viết rồi **gỡ khỏi nhánh**, nhánh không còn gì của (9).
- **Thêm ngoài danh sách**, tìm thấy khi đo (7): đường song song (#6) mất số đo tiền khi người dùng ngắt. Đã tái tạo trước rồi sửa (commit 2).

## 2. Thay đổi chính

| Việc | File | Thay đổi |
|---|---|---|
| (7) Dừng | `frontend/src/chat.jsx` | Đang trả lời thì nút "Hỏi" thành **"Dừng"** ⇒ huỷ `fetch` stream. Lượt bị dừng: **xoá chữ đã hiện** + "Đã dừng. Phần trả lời chưa xong nên không hiện (chưa kiểm nguồn)." + nút "Hỏi lại". Lý do chọn xoá thay vì giữ: chữ đó chưa qua kiểm trích dẫn — cùng luật D3 (kiểm cuối hỏng ⇒ rút lại); server cũng không nhớ lượt bị ngắt (`client_disconnected` ∉ `REMEMBERED_OUTCOMES`) ⇒ màn hình khớp thứ trợ lý nhớ. Rời trang vẫn huỷ như cũ, không hiện gì |
| (12) | `backend/llm/assistant.py` `answer_turn_stream` | Đóng finding m-1 của review streaming 31/10. Trước: chỉ huỷ khi có `CancelledError` / `GeneratorExit` / `TimeoutError`. Sau: huỷ khi **luồng model còn sống** (`stream_live`). Lỗi trong code của mình ⇒ huỷ; luồng tự hết hoặc chính luồng báo lỗi (lần chạy đã dừng) ⇒ không huỷ |
| (7) số đo khi ngắt | `backend/llm/assistant.py` `answer_turn_stream_parallel` | Che (`anyio.CancelScope(shield=True)`) lần chờ `gather` trong `finally`, như route đã che `aclose`. Trước: Starlette huỷ kiểu anyio ⇒ `gather` bị huỷ ⇒ bỏ qua bước gộp ⇒ `chat_metrics` chỉ còn lần gọi định tuyến, **thiếu tiền phần trả lời** |
| (2) | `chat.jsx`, `index.css` | ô hỏi `maxLength={500}` (= `ChatRequest.query` `max_length`); từ 450 ký tự hiện "n / 500 ký tự", tới 500 hiện "Đã đủ 500 ký tự…" (`aria-live`, nối `aria-describedby`) |
| (5) | `backend/api/routes/chat.py` `StreamEvents.done`; `chat.jsx` | Sự kiện `done` có `tu_choi_kho: true` khi kho không đủ (`refusal` và không phải `out_of_scope`). Giao diện hiện 2 gợi ý cố định do code viết ("gõ đúng tên…", "tách câu nhiều ý…") + link Khám phá. Không gọi model. Không hiện khi mục web có câu trả lời (`web.outcome === "co_muc"`) |
| (+) Nguồn | `chat.jsx` `SourceLine`, `index.css` | Gộp theo `bai_id` (không có thì theo tên) ⇒ một bài một tên, theo thứ tự xuất hiện; bấm tên ⇒ mọi đoạn được trích của bài (mỗi đoạn kèm đường mục) + "Đọc cả bài" |
| test | `tests/test_chat_stream.py`, `tests/test_feedback.py` | 2 khẳng định `done` của câu từ chối thêm `tu_choi_kho`; 1 test mới: model từ chối ⇒ có cờ; câu trả lời thường / ngoài phạm vi ⇒ không |

## 3. Cách đã chạy thật

- Worktree `/tmp/e_viec_nho` (nhánh từ `c9931be`, rebase lên `main` `1611d34` sạch). `npm ci && npm run build`. Server thật `uvicorn api.app:app` cổng 8854, `--env-file`.
  - Riêng cho lượt kiểm giao diện: `tra_web: false` **chỉ trong file của worktree**, đã trả lại trước commit. Lý do: tra web bật thì câu kho từ chối thường có mục web ⇒ không thấy được gợi ý (5).
- **Tái tạo trước khi sửa (12):** `data/phase_11/viec_nho_e/do_huy_loi.py`, lõi thật + model thật. Ở chữ đầu, ném `ValueError` vào thân vòng đọc (`athrow`), rồi xem tác vụ nền SDK + dòng `chat_stream_drain`. Chạy trên `main` (thư mục chính) rồi trên nhánh.
- **Tái tạo trước khi sửa số đo khi ngắt:** `data/phase_11/viec_nho_e/do_dung_song_song.py`, đường song song thật. Đọc tới mảnh chữ thứ 3 rồi huỷ bằng vùng huỷ anyio như Starlette, sau đó `aclose()` trong vùng che như route. Chạy trên `main` rồi trên nhánh.
- **Trình duyệt:**
  - `data/phase_11/viec_nho_e/ui_viec_nho.py` (Playwright 1440 + 390): gõ 520 ký tự, câu trong kho (Nguồn), Dừng giữa chừng + Hỏi lại, câu kho không có, câu ngoài phạm vi;
  - sau commit 2: `ui_dung.py` (chỉ bước Dừng) trên server khởi động lại.
- **Q1:** `capture_all.py` (0 USD) trên nhánh, `cmp` với bản chụp mới của `main` `1611d34` (chụp trong review bản đồ).
- **Test:** 11 file chạm đường stream / giao diện / lịch: `test_chat_stream`, `test_feedback`, `test_static_ui`, `test_cong_dot_1`, `test_b2_tool_loop`, `test_b3_memory`, `test_b5_lich_trinh`, `test_b5b_thoi_tiet`, `test_b6_tra_web`, `test_toc_do_song_song`, `test_p10_anh`.

## 4. Kết quả quan sát

| Việc | Kết quả (lần chạy mới) |
|---|---|
| (12) tái tạo | `main`: **không** có `chat_stream_drain` (không `cancel()`), tác vụ nền SDK còn sống sau 2 s rồi tự chạy tới hết · nhánh: `chat_stream_drain {"finished": true}`, không còn tác vụ nền sau 2 s |
| Số đo khi ngắt (đường song song) | `main`: `llm_calls` chỉ còn lần định tuyến (mất tiền phần trả lời), không drain · nhánh: đủ 4 lần gọi (định tuyến + 3 lần trả lời), drain xong; lần gọi bị dừng **56 token ra** |
| (7) trình duyệt | Dừng sau 60 ký tự (lượt 1) / 28 ký tự (lượt sau sửa): chữ bị xoá, không nguồn, "Đã dừng" + "Hỏi lại", ô hỏi mở lại; Hỏi lại ra câu đầy đủ |
| (7) log lượt Dừng sau sửa | `client_disconnected`, `chat_stream_drain` có, `llm_calls` đủ 4 lần, lần trả lời bị dừng **89 token ra** — câu đầy đủ cùng loại 517 token (lượt Hỏi lại) ⇒ model dừng thật; USD ghi 0,00078 |
| (7) lượt Dừng trước sửa | không có drain: hôm đó định tuyến chậm (chữ đầu 9,96 s) nên phần chạy song song đã xong trước khi chữ hiện — không còn gì để huỷ; nhưng log mất tiền phần đó (đúng lỗi đã sửa) |
| (2) | gõ thật 520 ký tự ⇒ ô giữ **500**, dòng "Đã đủ 500 ký tự…"; 449 ký tự ⇒ không có dòng đếm; 390: "460 / 500 ký tự" |
| (+) Nguồn | câu về một lăng: **1 tên** (trước sửa cùng câu ra 8 lần cùng tên — E thấy khi kiểm ảnh 08/11), bấm ⇒ 5 đoạn + link "Đọc cả bài" |
| (5) | câu kho không có ⇒ chữ từ chối + khối gợi ý (2 gợi ý + link Khám phá); câu ngoài phạm vi ⇒ 0 khối gợi ý cách hỏi, vẫn 3 câu gợi ý cũ |
| Lỗi giao diện | 0 lỗi CSP / console / pageerror; không cuộn ngang (1440 + 390) |
| Q1 chuỗi gửi model | **giống byte** `main` 228 / 228 |
| Test | **520 passed**, 1 failed = `test_b6_tra_web.py::test_web_section_renderer_uses_filter_without_links` — hỏng sẵn trên `main` (E chạy trên `main`: cũng hỏng); B đã sửa ở `p11-ban-do` ⇒ hết khi rebase |
| Log | `chat_metrics` 5 dòng = 5 câu (lượt giao diện); grep chữ câu hỏi trong log = 0 |

**Tiền:**
- Log ghi được 0,00445 USD: giao diện 0,002175 + Dừng sau sửa 0,000776 + các phép dò 0,0015.
- Thêm phần **không ghi được** ở 2 lượt tái tạo trên `main`, ước ≤ 0,001 USD — đúng là phần lỗi làm mất.
- ⇒ tổng ≈ **0,0055 USD**, tiền Phase 11.

## 5. Lỗi và giới hạn

- **(9) chưa làm** (gác). Câu khẩn cấp vẫn như cũ (có 👍/👎).
- (5) chỉ kiểm khi tra web **tắt** (server thử). Khi tra web bật: gợi ý ẩn nếu mục web có câu trả lời (`co_muc`), hiện nếu web không ra gì — logic đọc từ code, **chưa chạy** lượt có phí cho ca này.
- Cổng ổn định (câu trong kho + ngoài kho + `chat_metrics` + grep log) chạy ở lượt giao diện **trước** commit 2, với `tra_web` tắt. Commit 2 chỉ đổi `finally` của đường song song khi bị ngắt; đã đo lại riêng bước Dừng sau sửa ⇒ **dùng lại** kết quả cổng cho phần còn lại. A chạy cổng trên `main` sau merge.
- Lượt bị dừng khi định tuyến chậm: phần trả lời chạy song song có thể đã xong trước khi người dùng thấy chữ ⇒ bấm Dừng không tiết kiệm được tiền ở ca đó (bản chất của #6); log nay ghi đủ tiền.
- `maxLength` của trình duyệt đếm đơn vị UTF-16, server đếm ký tự Unicode ⇒ emoji tính 2 ở trình duyệt, 1 ở server: trình duyệt chặt hơn, không bao giờ vượt 500 của server.
- Chồng file khi merge: B (`p11-ban-do`: `chat.jsx` `LichExtras`, `assistant.py` nạp toạ độ, `pages.jsx`) — nhánh này **không chạm** `LichExtras`, `pages.jsx`; `assistant.py` khác đoạn ⇒ bên merge sau rebase.

## 6. Bàn giao cho người kiểm

- Đọc `git diff main...p11-viec-nho-e` (2 commit), rồi chạy lại hai phép dò trên `main` ↔ nhánh (mỗi lần ≈ 0,0005 USD):
  - `do_huy_loi.py "<câu>"`;
  - `do_dung_song_song.py "<câu>" song_song huy`.
- Trình duyệt: `ui_viec_nho.py <BASE> <OUT>` (≈ 0,0025 USD; server có `tra_web: false` để thấy (5)).
- Ảnh: `data/phase_11/viec_nho_e/ket_qua/` (a đếm 500, b Nguồn gộp, c Đã dừng, d gợi ý dưới từ chối, e đếm 390).
- Ca dò gợi ý cho người kiểm: bấm Dừng **trước** chữ đầu (đang "Đang tìm…") ⇒ cùng nhãn "Đã dừng"; dòng Nguồn của câu có ≥ 2 bài.

**Giải thích ngắn:**
- Người dùng bấm Dừng được khi trợ lý đang trả lời. Phần đã hiện bị xoá vì chưa kiểm nguồn, và server dừng model thật (log thấy số token ra ít hẳn).
- Server giờ huỷ model mỗi khi luồng còn chạy mà phải dừng, kể cả khi chính code của mình lỗi. Lượt bị ngắt ghi đủ tiền vào log.
- Ô hỏi chặn ở 500 ký tự và báo trước, thay cho lỗi "Yêu cầu không hợp lệ".
- Câu kho không trả lời được có gợi ý cách hỏi lại (không gọi model).
- Dòng Nguồn mỗi bài chỉ ghi một tên.
