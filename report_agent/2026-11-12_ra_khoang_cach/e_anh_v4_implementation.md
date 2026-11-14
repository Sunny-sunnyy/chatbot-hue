# Ảnh Khám phá đầy đủ v4 — implementation · E · 18:12 14/11/2026

Ưu tiên mới của User (17:50 14/11, qua A): mọi địa điểm, món ăn, di tích… phải có ảnh.
- Nhánh `p9-anh-v4`.
- Tiền: Serper 95 lượt ≈ **0,095 USD** (trần ghi trước 0,16). Agent con: 6 lượt, tốn quota Claude.
- Tiêu chí ghi TRƯỚC khi chạy, cùng luật gộp, brief và biên bản: `data/anh_day_du_2026-11-14/` (private: `TIEU_CHI.md`, `BRIEF_CHON_ANH_V4.md`, `tools/tim_anh_v4.py`, `tools/gop_anh_v4.py`, `bang_anh_kham_pha_v4.json`).

## Kết quả
| | Trước | Sau |
|---|---|---|
| Bài Khám phá có ảnh | 184 / 224 | **212 / 224** |
| Ảnh `kc` (không hiện cạnh câu trả lời trợ lý) | 38 | 50 |
| Ảnh hiện được cạnh câu trả lời (có ảnh, không `kc`) | 146 | **162** |

Đổi theo nhóm:
- **Bài về một nơi / món đang trống (21):** nhận 9.
  - 5 ảnh có biển tên rõ, cả hai lượt chọn đều chấm "cao" ⇒ không `kc`.
  - 4 ảnh `kc`, trong đó có biển Thuận An.
  - 12 bài vẫn trống: 6 bài không còn ứng viên mới (mọi ảnh Serper trả về đều đã bị loại ở hai lần trước); 6 bài có ảnh nhưng không ảnh nào đúng quán.
- **Bài chủ đề (vé, đi lại, lưu trú theo khu, lịch trình, cẩm nang — 19):** 19 / 19 có ảnh minh hoạ đúng chủ đề ở Huế, luôn `kc`.
- **Xem lại 38 ảnh `kc`:**
  - 6 bài thay bằng ảnh có biển tên + số nhà đọc được (5 quán và 1 lễ hội), bỏ `kc`.
  - 5 bài giữ ảnh cũ nhưng bỏ `kc`: cả hai lượt chắc đó là ảnh đúng, và E đã xem tay.
  - 27 bài giữ nguyên. Không ảnh nào bị gỡ.
- **Ảnh lịch biển Thuận An:** KHÔNG thêm. Ảnh Khám phá của bài này là `kc` (biển chung, chỉ dựa vào tiêu đề trang). Theo tiêu chí, ảnh lịch phải chắc.

## Sàn: người nhìn mọi ảnh sẽ hiện không `kc`
- E xem 19 ảnh, **bác 3**, đưa về `kc`. Cả 3 ảnh này đều được hai lượt agent con chấm "cao":
  - múa lân trên đường làng: không nhận ra đúng làng;
  - 2 quán cà phê: ảnh không có biển tên.
- E còn nhìn lướt 23 ảnh `kc` mới: đều đúng chủ đề.

## Kiểm [Chạy]
- `dung_anh_bai_js.py` (đọc thêm v4): 212 ảnh, 50 `kc`. Luật không chép chuỗi trùng kho vào repo vẫn chạy (assert đạt).
- `npm ci && npm run build`: 2 s.
- pytest `test_cong_dot_1` + `test_static_ui` 26 đạt (39 s); `test_anh_tra_loi` 1 đạt.
- Server tạm của worktree (cổng 8037, kiểm cwd, không lượt có phí):
  - 212 / 212 file ảnh trả 200 `image/jpeg`;
  - Playwright 1440, 5 trang lĩnh vực: 60 / 60 thẻ đầu tải được ảnh, 0 lỗi console.
  - Ảnh chụp: `data/anh_day_du_2026-11-14/anh_chup/`. Ảnh trình User sẽ chụp sau nhánh cuối.

## Giới hạn
- Bài chủ đề lệch 7 / 19 giữa hai lượt; luật lấy ảnh lượt 1, nên lượt 2 thừa. Vòng tự soi đã chốt: ảnh chủ đề / `kc` chỉ cần 1 lượt.
- 12 bài trống đều là quán. Muốn đủ 100 % thì cần nguồn ảnh khác (vd trang đánh giá có ảnh của chính quán), không phải tìm lại bằng Serper.
- Một ảnh lễ hội vẫn `kc` dù cả hai lượt nghi đó là phiên chợ cùng tên ở nơi khác. Ảnh lấy từ báo địa phương Huế; luật là không bao giờ gỡ ảnh đang có thành trống. Nên xem lại nếu có nguồn tốt hơn.
