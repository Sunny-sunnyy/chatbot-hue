# Review: việc nhỏ trước đóng gói — phần E (`p11-viec-nho-e`)

Người kiểm: B (Claude Code, `hue-rag-a1`) · Date: 10:40 08/11/2026 (`date`)
Nhánh: `p11-viec-nho-e` `45b3710` (2 commit trên `main` `1611d34`). Report người làm: `report_agent/2026-11-06_giao_dien_cong/e_viec_nho_implementation.md`.
Tiêu chí: tin A 08/11 — (2) 500 ký tự khớp `ChatRequest`; (5) gợi ý chỉ dưới câu từ chối của kho; (7) Dừng (xoá chữ chưa kiểm + "Đã dừng / Hỏi lại",
backend dừng thật, `chat_metrics` đủ mọi lần gọi kể cả đường song song #6 — vùng che không treo / không rò tác vụ); (12) lỗi trong vòng đọc ⇒ cancel + drain;
Nguồn gộp theo bài, bấm xem đủ đoạn; chuỗi gửi model giống byte; rebase lên `main` mới không đụng.

## 1. Phạm vi đã review

- Cổng tối thiểu: commit gốc `1611d34` + 2 commit khớp report; 6 file (`chat.py`, `assistant.py`, 2 test, `chat.jsx`, `index.css`), không file ngoài phạm vi;
  `git diff --check` sạch; đọc toàn bộ diff.
- Rebase thử (cục bộ, không push) lên `main` `3da1cb1` (đã có bản đồ + ảnh): **sạch**, 2 commit `157856b` / `a676f91`. `main` hiện `06dafb4` = `3da1cb1` + cờ
  `anh.bat: true` (chỉ `settings.yaml`) ⇒ không chạm đường chat.
- Mọi lần chạy dưới đây trên **bản đã rebase** (`/tmp/b_rv_e`) — đúng bản sẽ vào `main`.

## 2. Findings

### m-1 (minor) — "`chat_metrics` đủ mọi lần gọi" chỉ đúng với lần gọi **đã chạy xong** trước khi ngắt

- Vị trí: report §1 / §4 ("đủ 4 lần gọi"); `assistant.py` `answer_turn_stream` `finally` (`result.cancel()`), `CallLog.on_llm_end`.
- Bằng chứng (B chạy, ngắt ở tầng HTTP thật — `ngat_http.py`, `ui_review.py`):
  - ca A (đóng sau chữ đầu, lúc 5,0 s — phần trả lời song song đã chạy xong trong hàng đợi): `llm_calls` = định tuyến + trả lời ✓;
  - ca C1, C3 (đóng sau chữ đầu lúc 1,5–2,1 s, **model còn đang sinh**): `llm_calls` **chỉ có định tuyến**, thiếu lần trả lời đang chạy;
  - lượt giao diện bấm Dừng **trước** chữ đầu: `llm_calls` = `[]` (cả lần định tuyến đang chạy cũng mất);
  - nguyên nhân: SDK 0.19.4 `RunResultStreaming.cancel(mode="immediate")` (mặc định) huỷ ngay ⇒ không có `usage` ⇒ `on_llm_end` không chạy. Docstring SDK:
    chỉ `after_turn` "Tracks usage accurately".
- Tác động: tiền / token của lần gọi bị cắt giữa chừng không vào log (cận dưới thấp hơn thật, ước ≤ ~0,0003 USD / lượt). **Có từ trước** (không phải lỗi nhánh
  này gây ra); sửa của E (che `gather`) đúng và cần — giữ được lần gọi đã xong mà trước đây mất.
- Tiêu chí đóng: report sửa câu thành "đủ mọi lần gọi **đã chạy xong**; lần bị cắt giữa chừng không có usage (SDK huỷ ngay)". Ghi cận dưới như D2 (`usd +=
  cost_usd(input_tokens, 0)`) cho tuyến `keep` là việc riêng nếu A muốn — không mở vòng sửa.

### m-2 (minor, [Code, chưa chạy]) — gợi ý cách hỏi (5) có thể hiện dưới lượt **biểu mẫu** bị từ chối

- Vị trí: `chat.py` `StreamEvents.done` (`tu_choi_kho` khi `refusal` và không `out_of_scope`); `chat.jsx` khối `.goi-y-hoi`.
- Lượt biểu mẫu mà model từ chối viết lịch ⇒ `refusal` ⇒ hiện "Gõ đúng tên nơi, món hay lễ hội…" — không hợp người vừa bấm nút biểu mẫu.
- Tiêu chí đóng: ẩn khi `turn.bieuMau` (một điều kiện ở giao diện) — hoặc A chấp nhận. Không chặn.

### Ghi nhận (không phải finding)

- (12) `stream_live`: đọc từng nhánh — hết luồng ⇒ không huỷ; lỗi `Exception` từ `anext` (lỗi của chính luồng) ⇒ không huỷ; `TimeoutError`, `CancelledError`,
  `GeneratorExit`, lỗi trong thân vòng ⇒ huỷ + drain. Không có `break` chủ động nào khác trong vòng đọc. Đúng ý review streaming 31/10 m-1.
- Vùng che `gather` không treo được vì phần model: `finally` của (ii) đọc nốt trong `move_on_after(STREAM_DRAIN_SECONDS = 0,5)`; còn lại chỉ chờ phần tìm kho
  nếu đang chạy (ngắn).
- Độ đơn giản: thay đổi nhỏ, đúng chỗ; không thêm cơ chế phòng xa.

## 3. Cách người kiểm chạy lại thật

- Worktree tách rời `/tmp/b_rv_e` từ `origin/p11-viec-nho-e`, `git rebase 3da1cb1`; `npm ci && npm run build`.
- Test rộng không khoá (mọi `tests/test_*.py` trừ 3 file cần khoá / model).
- Q1 `capture_all.py`: chụp **mới** trên `main` (working tree `06dafb4`) và trên bản rebase, `cmp`.
- Server thật `uvicorn api.app:app --port 8876` (cờ như `settings.yaml` của bản rebase, tra web bật), tắt bằng TaskStop.
- `data/phase_11/review_viec_nho_e/tools/ngat_http.py` — **cách khác E**: client `httpx` đóng kết nối thật (không `athrow`, không vùng huỷ tự dựng): A đóng sau chữ
  đầu; B đóng lúc 0,4 s (đang định tuyến); C0–C5 sáu lần ngắt liên tiếp xen kẽ; D một câu đủ + `/health` ngay sau. Đọc log: `chat_metrics`, `chat_stream_drain`,
  dòng ERROR / WARNING / "Task was destroyed" / Traceback.
- `data/phase_11/review_viec_nho_e/tools/ui_review.py` (Playwright 1440): dán 600 ký tự bằng `fill`; Dừng **trước** chữ đầu rồi Hỏi lại; câu so sánh 2 lăng (≥ 2
  bài) — đếm nhóm Nguồn so với `bai_id` trong SSE, bấm từng nhóm đếm đoạn; câu ngoài phạm vi.

**Bất biến kiểm:** người dùng ngắt ở bất kỳ lúc nào ⇒ server không treo, không rò tác vụ, lượt sau chạy bình thường; mỗi lượt đúng **một** dòng `chat_metrics`.

## 4. Kết quả quan sát

| Tiêu chí | Kết quả |
|---|---|
| Rebase lên `main` mới | sạch; test rộng **735 đạt** (1 hỏng + 1 lỗi = đúng 2 test cần khoá); bundle chính 108,86 KB gzip |
| Chuỗi gửi model | **228 / 228 giống byte** (`main` `06dafb4` ↔ bản rebase; `data/phase_11/review_viec_nho_e/*.jsonl`) |
| (2) 500 ký tự | dán 600 ⇒ ô giữ **500**, "Đã đủ 500 ký tự…"; `MAX_QUERY` = `ChatRequest.query` `max_length` 500 (đọc code) |
| (5) | câu ngoài phạm vi: `done` không có `tu_choi_kho`, **0** khối gợi ý cách hỏi, 3 câu gợi ý cũ còn. Câu từ chối của kho: dùng lại bằng chứng của E (B không chạy — tra web bật trên server của B). Thêm m-2 |
| (7) Dừng | trước chữ đầu: "Đã dừng…" + "Hỏi lại", 0 khối chữ, ô hỏi mở lại; Hỏi lại ra câu đầy đủ. Ngắt HTTP: 8 / 8 lượt `client_disconnected`, **mỗi lượt đúng 1 dòng** `chat_metrics`, 8 / 8 `chat_stream_drain finished: true` (0,3–0,5 ms) |
| Không treo / không rò | sau 8 lần ngắt: câu đủ trả lời bình thường (3,6 s, có `sources` + `done`), `/health` ok; **0** dòng ERROR / WARNING / "Task was destroyed" / Traceback |
| `chat_metrics` đủ lần gọi | đủ khi lần gọi đã xong trước ngắt (ca A, C4, C5); **thiếu** lần đang sinh dở (C1, C3, Dừng trước chữ) ⇒ m-1 |
| Nguồn gộp | 7 nguồn / 3 bài ⇒ **3** tên; bấm từng tên: 1 / 2 / 4 đoạn = số nguồn cùng `bai_id` trong SSE (4 / 1 / 2) |
| Lỗi giao diện | 0 lỗi console / pageerror |
| Log | chữ câu hỏi trong log = 0 |

Tiền (log server của B): **≈ 0,0053 USD** — **vượt trần A cho review (≤ 0,005) khoảng 0,0003 USD**; cộng phần không ghi được (m-1). Ảnh:
`data/phase_11/review_viec_nho_e/anh/`; kết quả: `ngat_http.json`, `ui_review.json`.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại hai phép dò `do_huy_loi.py` / `do_dung_song_song.py` của E (B dò bằng cách khác ở tầng HTTP); (12) nhánh "lỗi trong code của mình" kiểm bằng đọc code
  + bằng chứng của E.
- (5) dưới câu từ chối khi tra web bật + mục web không ra gì: chưa ai chạy (E ghi ở §5).
- 390 px không chạy lại (E đã chụp).

## 6. Decision và bước tiếp theo

**`ready_for_user_confirmation`** — 0 blocker / 0 major / 2 minor. m-1 sửa chữ trong report của E (không mở vòng); m-2 E sửa nếu tiện hoặc A chấp nhận.
A merge (rebase lên `main` hiện tại sạch) + cổng ổn định trên `main`.
