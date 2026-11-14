# Review nhánh `p9-gt-song` `d8b2071` (C): Giới thiệu — sông dọc ba bến + thẻ "Ví dụ" + ảnh thời kỳ lộ qua mặt nạ

- **Người kiểm:** B, 15:38 14/11/2026.
- **Mức:** nhẹ, một review cả nhánh (A giao).
- **Kết luận: `changes_requested`.** 1 major, 1 minor.

## Cổng tối thiểu
- **Diff:** 3 file (`App.jsx` +`onAsk`, `GioiThieu.jsx` ba bến + `ViDu`, `gt.css`). Không có gì ngoài phạm vi. `HueQuaCacThoiKy.jsx` của B không bị sửa; hiệu ứng mặt nạ đặt ở `gt.css`, đúng như C ghi.
- **Thẻ Ví dụ:** đối chiếu `data/gt_vi_du_2026-11-14/vi_du_1.json`. Câu trả lời là bản rút gọn câu thật; 4 nguồn được trích đều thuộc "Cẩm nang ẩm thực Huế" ⇒ khớp `n_trich: 4`. Có nhãn "Ví dụ" và nút "Hỏi thử câu này" (gọi `askAnywhere` có sẵn). Link bài chỉ hiện khi bài còn trong `/api/kham_pha`; repo không ghi mã bài.

## Kiểm [Chạy] (0 USD)
- **Cách chạy:** bản build nhánh, server tạm 8879, `data/hue_thoi_ky_2026-11-14/pw_mat_na.py`, ảnh `anh_review_gt_song/`.
- **1440:** 3 bến, 3 thẻ Ví dụ, 1 nút hỏi thử, 0 lỗi console.
  - clip-path của khung ảnh ghim, đo khi từng mốc ở giữa màn hình: mốc 1 `inset(7.8%)` · mốc 2 `inset(3.1%)` · mốc 3–6 `inset(0)`.
- **390:** mọi ảnh từng mốc `inset(0)` khi tới mốc; 3 bến + Ví dụ hiện đúng (`ba_ben_390.png`).

## Finding
- **M-1 (major) — khổ rộng: lúc đọc mốc 1, số năm "1306" trên ảnh bị cắt thành "306"; ảnh còn co ~8 %** (`mat_na_1440_1.png`).
  - Nguyên nhân: `.tk-khung-anh` là khối ghim (`sticky`). Với `animation-timeline: view()`, khi khối đã ghim thì vị trí của nó so với màn hình gần như đứng yên, nên tiến độ mặt nạ chỉ chạy trong đoạn cuộn **trước khi** ghim. Tới lúc mốc 1 nằm giữa màn hình, khung mới đi ~80 % đoạn đó. Mặt nạ cắt cả `.tk-nam-lon` vì chữ nằm trong khung.
  - Tác động: người xem thấy năm sai đúng ở mốc đầu tiên, chỗ dễ thấy nhất của màn.
  - Đề xuất (chọn một):
    - (a) Bỏ mặt nạ cho khung ghim ở khổ rộng, chỉ giữ cho `.tk-anh-nho` (khổ hẹp không ghim, đo đã đạt).
    - (b) Đặt mặt nạ lên `.tk-khung-anh img` (không cắt chữ năm) và cho xong sớm (`animation-range: entry 0% entry 100%`), rồi đo lại mốc 1 = `inset(0)`.
  - Tiêu chí đóng: đo lại bằng `pw_mat_na.py`; mốc 1 ở 1440 phải `inset(0)` hoặc không có mặt nạ, và chữ năm đủ 4 số trên ảnh chụp.
- **m-1 (minor) — "Tìm được 10 đoạn" không có trong bản ghi `vi_du_1.json`** (bản ghi chỉ có 4 nguồn được trích).
  - Số 10 khớp trần ngữ cảnh 10 đoạn đang chạy, nhưng nên trỏ tới dòng `chat_metrics` của lượt đó (`n_sources` / số đoạn) để có nguồn.
  - Tiêu chí đóng: ghi nguồn của số 10 vào comment hoặc vào bản ghi.

## Vòng 2 — `63ba5c6` (15:44 14/11/2026): **`ready_for_user_confirmation`**
- **M-1 đóng.** Diff `d8b2071..63ba5c6` chỉ bỏ `.tk-khung-anh` khỏi bộ chọn mặt nạ; giữ `.tk-anh-nho` ở khổ hẹp. C đo bằng `pw_mat_na.py`: 1440 cả 6 mốc không mặt nạ, 390 6 / 6 `inset(0)`. B xem ảnh `data/ui_anh_gt_2026-11-14/mat_na_sau/mat_na_1440_1.png`: "1306" hiện đủ, ảnh đầy khung.
- **m-1 đóng.** `data/gt_vi_du_2026-11-14/vi_du_1_chat_metrics.json` cùng `turn_id` với `vi_du_1.json` (B đối chiếu), có `n_context_sources: 10`; comment trong code trỏ tới file này.
- 0 finding mở. Chưa chạy lại test: lần sửa chỉ đổi CSS + comment; C đã chạy `test_static_ui` + `test_cong_dot_1`, 26 đạt.
