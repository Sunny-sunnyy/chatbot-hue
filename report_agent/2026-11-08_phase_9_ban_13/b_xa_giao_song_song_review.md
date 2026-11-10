# Review: xã giao chạy song song định tuyến (nhánh `p9-xa-giao-song-song` `9ce7cfd`)

Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-4f`) · 10/11/2026 · A giao (review một vòng cả nhánh, chỉ chỗ rủi ro; kết quả đo đã biết **chưa đạt** ⇒ A không merge,
review để sẵn nếu User chọn bật). Plan `docs/superpowers/plans/2026-11-10-phase-9-xa-giao-song-song-plan.md` `47009c7dc791` + chốt tự soi 1. Report
`b_xa_giao_song_song_implementation.md` (B). Dữ liệu private `data/phase_9/xa_giao_song_song/`.

## 1. Phạm vi đã review

- `git diff 624a17b..9ce7cfd`: 3 file — `backend/llm/assistant.py` (+62 / −35), `backend/config/settings.yaml` (+1, cờ `false`), `backend/tests/test_toc_do_song_song.py` (+45). Không file ngoài plan.
- Chỗ rủi ro A / B / C ghi trước: `answer_turn_stream_parallel` (`running`, `done_before_route`, khối `finally`, `dropped` ⇒ `n_tra_loi_bo` / `usd_bo`), `_merge_spec` cho trace trò chuyện,
  AN 0 lọt, cờ tắt giống byte, nhãn report trung thực.

## 2. Findings

**Blocker:** không. **Major:** không.

**Đọc code (khớp thiết kế):**
- Trace phụ trò chuyện = `spec_trace(route=ROUTE_TRO_CHUYEN)` + `answer_turn_stream(…, without_router)`. `_pick_route` với `router=False` **không ghi đè** `trace.route`
  (`assistant.py:788-806`) ⇒ đi nhánh `start_chat_stream` (`:937-940`) — đúng đường cũ của tuyến này (đường cờ tắt cũng gọi y vậy trên trace chính). `route` không
  nằm trong `ROUTE_INPUTS` (`:1067`) ⇒ không trùng tham số.
- `khan_cap`: `_pick_route` đổi thành `tro_ly_hue` trên trace chính ⇒ giữ phần Huế như #6 (phương án B) — không đổi.
- `_merge_spec` giữ `route` / `routing_ms` / `emergency_by` / `llm_calls` của trace chính, nối `llm_calls` = định tuyến + trò chuyện; `packed` của trace trò chuyện `None` ⇒ không
  ghi recorder (như đường cũ). Cổng web chỉ khi giữ phần Huế; trace trò chuyện dùng `without_router` (`tra_web=False`) ⇒ câu xã giao không ra Serper.
- `finally`: huỷ **mọi** task trong `running`, chờ cả hai trong `CancelScope(shield=True)` + `gather(return_exceptions=True)`; `n_tra_loi_bo` / `usd_bo` / `bo_huy_giua`
  đặt **sau** `_merge_spec` ⇒ không bị trường của trace phụ ghi đè. Lỗi / ngắt trước khi gộp ⇒ gộp trong `finally` rồi mới tính phần bỏ.
- Cờ tắt: `running` chỉ có phần Huế; `kept`, thời điểm huỷ, `done_before_route` (= `finished_before_route` cũ, lấy cùng lúc), `usd_bo` cho một phần bỏ ⇒ cùng giá trị như
  `main`. Test sẵn có "cờ tắt" + test mới so `_request_bytes` với đường #6.
- `AssistantFlags`: `song_song_tro_chuyen` cần `song_song_tra_loi` (raise khi thiếu) — đúng "cờ cần cờ" như các cờ khác.

**Minor (không chặn):**
- **m-1 · tiền phần trò chuyện bị huỷ giữa chừng tính 0** (`finally`, nhánh `cost_usd(spec.packed.input_tokens, 0)` chỉ chạy khi có `packed`). Report đã ghi "cận dưới,
  tối đa ≈ 0,00004" — đúng nhãn. Hệ quả cho User: tiền câu Huế thật ≈ 0,00041–0,00046 (vẫn dưới 0,0005); câu ngoài phạm vi 0,00056 là số **có** usage thật (phần xong
  trước). Đóng: giữ nguyên, ghi số này khi A trình User (đã có ở report §3).
- **m-2 · docstring `_merge_spec`** (`assistant.py:1162`) còn ghi "Tuyến `tro_ly_hue` ⇒ …" — nay dùng cho cả `tro_chuyen`. Đóng: sửa một dòng nếu merge.
- **m-3 · ngắt kết nối chưa có test riêng** — đúng như A chốt ở tự soi 1, report ghi rõ [Code, chưa test riêng]. Cơ chế giống #6 (đã đo thật ở việc nhỏ (7) 08/11) và
  task chỉ khởi động sau sự kiện `routing`. Chấp nhận.

## 3. Cách người kiểm chạy lại thật

| Lệnh (0 USD) | Kết quả |
|---|---|
| `cd /tmp/b_xg/backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_toc_do_song_song.py -q` | **15 passed** (18,6 s) |
| `uv run … python data/phase_9/xa_giao_song_song/tools/an_cham.py ../an_r1.jsonl` | n 90 · tuyến 20 / 12 / 58 · success 78 + out_of_scope 12 · `AN_vi_pham` = 2 (`tuyen#c06`, `ls_b3#T04#2`) |
| đọc 2 dòng bị báo (chỉ so chữ, không in nội dung) | `tuyen#c06`: chữ hiện dư **1 dấu cách** cuối, `strip()` bằng nhau, `llm_routes` = router + trò chuyện · `ls_b3#T04#2`: khác **chỉ** ở `[Nguồn n]` ↔ `[n]` (đổi dạng citation — bẫy đã biết), `delta_matches_final` true |
| đếm trên `an_r1.jsonl` | tuyến trò chuyện có lần gọi `tro_ly_hue` trong trace chính: **0** · tuyến khác có lần gọi `tro_chuyen`: **0** · `n_tra_loi_bo` 1 = 78, 2 = 12 (ngoài phạm vi) · `bo_huy_giua` 70 / 90 ⇒ đường huỷ giữa chừng đã chạy thật |
| `s_r1_tong.json` | xã giao chữ đầu p50 1.846 / p95 **5.736** ms (19 trò chuyện + 1 xếp Huế; định tuyến max 5.574 ms) · Huế 2.277 / 4.231 · ngoài phạm vi 1.918 / **5.208** — khớp report |

Không chạy lại: lượt S (tốc độ, A chốt không chạy lại), test rộng (B: 855 đạt), lượt có phí.

## 4. Kết quả quan sát

- **AN 0 lọt** — xác nhận độc lập (2 dòng bộ chấm báo là khác chữ ngoài nội dung, đúng như B giải thích).
- **Nhãn report trung thực:** tiêu đề + §0 + §2 ghi **CHƯA ĐẠT / FAIL** cho S (2 sàn p95), tiền ngoài phạm vi vượt NFR, giả thuyết đuôi p95 do định tuyến ghi là
  **chưa chứng minh**; không đổi tiêu chí ghi trước. Số khớp file kết quả.

## 5. Giới hạn hoặc phần chưa chạy

Ngắt kết nối thật (m-3) chưa đo trên nhánh. Một lượt S, n = 20 / loại ⇒ p95 ≈ câu chậm thứ hai (report đã ghi).

## 6. Decision và bước tiếp theo

**Code: `ready_for_user_confirmation`** (0 blocker, 0 major; m-2 sửa khi merge) — nghĩa là **an toàn để merge với cờ `false`** nếu User chọn. **Kết quả đo: chưa đạt tiêu
chí ghi trước** (đúng nhãn của B) ⇒ quyết bật / không là của User qua A (report §3 có "được / mất"). Không chọn ⇒ tag `hoso/p9-xa-giao-song-song`.
