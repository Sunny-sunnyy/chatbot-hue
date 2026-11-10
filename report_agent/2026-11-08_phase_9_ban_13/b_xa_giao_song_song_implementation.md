# Implementation Report: xã giao — gọi model trò chuyện song song với định tuyến (CHƯA ĐẠT tiêu chí ghi trước)

Người làm: B (Claude Code, `hue-rag-05`) · 19:31 10/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-10-phase-9-xa-giao-song-song-plan.md` bản 1 `47009c7dc791` (mức nhẹ, A duyệt; AT chọn (a)). Tự soi 1 (A chốt): AN = bộ 90 của #6,
S = 60 câu (bỏ 5 câu ngày), không dựng test ngắt kết nối mới.
Nhánh `p9-xa-giao-song-song` (từ `main` `624a17b`, worktree `/tmp/b_xg`). **Không merge** (A quyết 10/11): chờ User chọn bật hay không.

## 0. Kết luận

- **Nhãn: CHƯA ĐẠT tiêu chí ghi trước** — xã giao chữ đầu p95 **5,74 s** (sàn ≤ 5) và ngoài phạm vi p95 **5,21 s** (sàn ≤ 5). Các sàn khác đạt.
- **Quan sát:** trung vị chữ đầu câu xã giao **3,46 → 1,85 s** (−1,6 s); 19 / 19 câu đi tuyến trò chuyện ≤ 5,6 s; chữ đầu ≈ đúng lúc định tuyến xong.
- **Giả thuyết (chưa chứng minh):** đuôi p95 do định tuyến, không do phần sửa — xã giao: 1 câu bị định tuyến xếp sang Huế (đi đường Huế 8,2 s; S5 09/11 câu này
  cũng 7,6 s) + 1 câu định tuyến mất 5,6 s; ngoài phạm vi: 2 câu bị xếp sang Huế (5,2 / 6,2 s). Với 20 câu, p95 ≈ câu chậm thứ hai ⇒ chỉ cần 2 câu xếp nhầm là trượt.
- **Tiền:** câu ngoài phạm vi **0,00056 USD** (gồm phần bỏ) > NFR 0,0005; câu Huế không web 0,000414 — **cận dưới** (lần trò chuyện bị huỷ giữa chừng không có
  usage ⇒ tính 0; thật có thể cao hơn tối đa ≈ 0,00004).
- Cờ `assistant.song_song_tro_chuyen: false` trong nhánh (tắt ⇒ chuỗi gửi model như `main`, test khẳng định).

## 1. Thay đổi

| File | Đổi gì |
|---|---|
| `backend/llm/assistant.py` | `AssistantFlags.song_song_tro_chuyen` (+ kiểm: cần `song_song_tra_loi`); `answer_turn_stream_parallel`: mỗi tuyến có thể có **một phần chạy trước** trên trace phụ riêng + hàng đợi riêng (`tro_ly_hue` như #6; `tro_chuyen` khi cờ bật — chính `answer_turn_stream` với tuyến đặt sẵn `tro_chuyen`). Có tuyến ⇒ giữ phần của tuyến đó (xả hàng đợi, `_merge_spec`), huỷ ngay phần còn lại; tuyến không có phần chạy trước ⇒ huỷ hết. `n_tra_loi_bo` = số phần bỏ (1 hoặc 2), `usd_bo` cộng cả hai, `bo_huy_giua` = có phần nào bị huỷ trước khi xong. Cổng web chỉ chạy khi giữ phần Huế. |
| `backend/config/settings.yaml` | `song_song_tro_chuyen: false` |
| `backend/tests/test_toc_do_song_song.py` | +4 test (5 ca): tuyến trò chuyện giữ sự kiện tới khi có tuyến + yêu cầu gửi model giống byte đường #6; tuyến Huế không bao giờ hiện lần trò chuyện (xong trước / bị huỷ giữa chừng); ngoài phạm vi bỏ cả hai; lỗi lần trò chuyện ra như đường cũ / bị bỏ ở tuyến khác |

Không đổi: lời dặn, đầu vào mọi lần gọi model, `/api/chat` (không stream), nhớ hội thoại, giao diện.

## 2. Kết quả theo tiêu chí ghi trước

| Mã | Kết quả | Nhãn |
|---|---|---|
| **T** | `test_toc_do_song_song.py` 15 đạt (31 s); `test_b6_tra_web.py` + `test_ngay_lich.py` (đường song song) 157 đạt (23 s); test rộng 855 đạt (4 phút) | PASS |
| **AN** (90 lượt thật, cả hai cờ bật; `data/phase_9/xa_giao_song_song/an_r1.jsonl`, chấm `tools/an_cham.py`) | **0 lượt lọt**: tuyến ≠ trò chuyện không có lần gọi `tro_chuyen` trong trace chính; tuyến trò chuyện không nguồn, không lần gọi `tro_ly_hue`; `delta_matches_final` đúng 78 / 78 lượt thành công; 0 lỗi. Bộ chấm so chữ thô (chặt hơn #6) bắt 2 lệch **không phải lọt**: 1 lượt trò chuyện chữ hiện dư 1 dấu cách cuối (đường trò chuyện cũ, so sau `strip()` khớp); 1 lượt Huế câu cuối được đánh số lại citation (#6 cũng có 1 ca y vậy) | PASS |
| **AT** | **dùng lại 4 số của `main`** (A chọn (a)): yêu cầu gửi model của đường Huế giống byte (T) + AN 90 lượt (58 lượt tuyến Huế) không lần nào hiện lần trò chuyện ⇒ câu an toàn cùng phân phối với `main` | dùng lại, có lý do |
| **S** (Chromium, 60 câu, 1 lượt, server nhánh cờ bật tạm; `s_r1.jsonl`, `s_r1_tong.json`) | xã giao p50 **1,85** / p95 **5,74** ✗ · Huế p50 2,28 / p95 4,23 ✓ (S5 2,16 / 4,32) · ngoài phạm vi p50 1,92 ✓ (S5 1,62, +0,30 = đúng ngưỡng) / p95 **5,21** ✗ | **FAIL** (2 sàn p95) |
| theo dõi tiền | USD / câu gồm phần bỏ (TB, không web): xã giao 0,00031 · Huế 0,000414 (cận dưới) · ngoài phạm vi **0,00056** | ngoài phạm vi vượt NFR |

**Phần huỷ thật (C hỏi):** AN — tuyến Huế: lần trò chuyện bị huỷ giữa chừng 42 / 58, xong trước khi có tuyến 16 / 58; tuyến trò chuyện: phần Huế huỷ giữa chừng 16 / 20,
xong trước 4 / 20; ngoài phạm vi: 12 / 12 có phần bị huỷ giữa chừng. ⇒ đường huỷ giữa chừng đã chạy thật nhiều lần, 0 lọt.
**Người dùng ngắt kết nối (C hỏi):** [Code, chưa test riêng — A chốt không dựng test mới] `finally` của `answer_turn_stream_parallel` huỷ **mọi** task trong `running`
rồi chờ cả hai trong vùng che (`anyio.CancelScope(shield=True)` + `gather`), như #6 (việc nhỏ (7) 08/11 đã đo thật cho một phần). Phần chạy trước chỉ khởi động sau
sự kiện `routing` ⇒ ngắt đúng lúc đó không có task nào. (Một test thử viết rồi gỡ: `aclose()` ở `routing` không tới được chỗ task chạy; kết quả "0 task treo" của nó đạt.)
**Định tuyến chậm hơn?** Thời gian định tuyến p50 S5 ↔ nay: xã giao 1,75 ↔ 1,67 · Huế 1,65 ↔ 1,73 · ngoài phạm vi 1,58 ↔ 1,89 s — lên xuống hai chiều ⇒ giả thuyết nhiễu
provider; chưa đo được lần trò chuyện chạy kèm có làm chậm định tuyến không.

## 3. Nếu User vẫn muốn bật

- **Được:** câu xã giao (chào, cảm ơn, hỏi bot là ai…) hiện chữ đầu sớm hơn ≈ 1,5 s ở câu điển hình (3,5 → 1,9 s trung vị); câu Huế không đổi.
- **Mất:** mỗi câu không phải xã giao trả thêm một lần gọi trò chuyện bị bỏ (≈ 0,00004 USD đủ / phần đã chạy khi bị huỷ) ⇒ câu ngoài phạm vi ≈ 0,00056 USD (> 0,0005);
  câu Huế ≈ 0,00041–0,00046. Đuôi chậm (câu bị định tuyến xếp nhầm / định tuyến chậm) **không** được sửa — p95 xã giao vẫn > 5 s ở lượt này.
- **Cách bật:** merge nhánh với cờ `false` (sau review C) ⇒ đổi `song_song_tro_chuyen: true` ⇒ cổng ổn định. Không ⇒ tag `hoso/p9-xa-giao-song-song`, xoá nhánh.

## 4. Kiểm tra, thời gian, tiền

| Bước | Thời gian (đo) | USD (log) |
|---|---|---|
| test file chạm + 2 file đường song song | 31 s + 23 s | 0 |
| AN 90 lượt (song song 4) | ~4 phút (19:14 → 19:18) | 0,0422 + phần bỏ 0,0097 |
| S 60 câu + 1 khởi động | ~3,5 phút chạy câu (19:25:59 → 19:29:16) | 0,0268 (gồm phần bỏ) |
| test rộng `backend/tests` (có key, cờ `false`) | 4 phút 00 giây — **855 đạt** | 0 |
| **Tổng** | | **≈ 0,079** (trần 0,1) |

Cổng ổn định (trên server lượt S, nhánh, cờ bật tạm): `/` 200 · `/health` 5 / 5 · mỗi câu đúng 1 dòng `chat_metrics` (60 / 60) · 0 câu hỏi trong log (1 khớp nhầm:
câu 2 ký tự trùng chữ thường trong log). Giao diện không đổi ⇒ không Playwright riêng (lượt S đã chạy qua Chromium). Q1 `capture_all` không chạy (không chạm chỗ dựng chuỗi
gửi model; T so byte bằng client giả).

Lệnh chạy lại một chỗ rủi ro (C): `cd /tmp/b_xg/backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_toc_do_song_song.py -q -k
"chat or hue_route or out_of_scope"` (0 USD); chấm lại AN: `cd data/phase_9/xa_giao_song_song/tools && uv run --project /home/minhhieu/hue_rag python an_cham.py ../an_r1.jsonl`.

## Giải thích ngắn

Câu chào hỏi phải chờ bước "xếp loại câu" xong (~1,7 s) mới bắt đầu viết. Sửa: viết luôn cùng lúc, giữ chữ lại tới khi biết đúng là câu chào hỏi. Câu chào hỏi
điển hình nhanh hơn ~1,5 s và không chữ trò chuyện nào lọt sang câu khác. Nhưng vài câu chậm vẫn chậm vì chính bước xếp loại (xếp nhầm / chậm), và câu ngoài phạm vi
tốn thêm tiền vượt mức 0,0005 USD ⇒ chưa đạt tiêu chí ghi trước; User quyết có bật không.
