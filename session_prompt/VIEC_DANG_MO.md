# VIỆC ĐANG MỞ — mục lục theo việc (sống xuyên ngày; GHI ĐÈ tại chỗ)

Cập nhật: 22:32 19/11/2026 (giờ `date`; kết phiên cuối ngày 19/11). Người giữ: phiên điều phối. **[đang thử từ 19/11, xét lại sau 3 ngày làm việc]**

Trang này là gì: mỗi việc kéo quá một ngày có MỘT khối ở đây, để phiên mở sáng hôm sau tìm lại đủ hồ sơ mà không lục từng thư mục ngày. Việc xong ⇒ dời MỘT dòng sang `session_prompt/VIEC_DA_XONG.md` (tên · ngày xong · sha gộp · các thư mục ngày có hồ sơ) rồi xoá khối. Trần: 8 việc / 60 dòng. **"Bước kế" của một việc CHỈ ghi ở trang này** — trang hiện trạng, `TONG_HOP.md` của ngày và `STATUS_<X>.md` chỉ trỏ tới đây, không chép lại. Dòng "plan" luôn là bản HIỆN HÀNH + sha đã duyệt; bản plan cũ có dòng đầu "đã thay bởi …". Report đã nằm ở thư mục ngày nào thì KHÔNG dời; bản cập nhật ngày sau là file MỚI ở thư mục ngày mới, dòng "report" liệt kê đủ theo ngày. Dữ liệu riêng tư ở `data/<tên việc>/` (không vào git) — ở đây chỉ ghi đường dẫn.

## 1. Tới buổi User test — thứ tự còn lại của bước 5 (User chốt 19/11; chi tiết quyết định: `HIEN_TRANG.md` mục 4)
- Đã xong + bật (main `ea777c2`, 29 cờ): lịch vào lượt hỏi thường · nói thật giới hạn · xuất lịch · nhớ tên nơi vừa trích. Đo lại bộ 80 kịch bản (file ghi trước `5f736af19dca`): xong việc 51 ⇒ 58 / 80, 0 "có điều sai" mới, kịch bản đích cả bốn việc đạt; hồ sơ `data/kich_ban_pho_thong_2026-11-19/luot_2/` (`PHAN_XU_E.md`).
- **BƯỚC KẾ, theo thứ tự:** (a) việc 2 dưới (sửa nhỏ cờ nhớ tên) ⇒ (b) soát mù khác hãng: đề bài `data/review_khac_hang/2026-11-19_diem_dung_buoc_5/DE_BAI.md` bản `40ef48d21966` (B giữ; sửa mã HEAD lúc gửi) — GPT 6.2 sol nhóm gọi qua Codex, Gemini 4 Hydrogen nhờ User lái (A nói User khi gửi); đối chiếu ba cột theo skill `soat-tich-hop` ⇒ (c) E chạy trọn `data/test_cuoi/DANH_SACH.md` bằng trình duyệt thật trên bản 29 cờ (CHƯA làm; E đã thêm dòng B9–B13) ⇒ (d) cả bộ test một lượt trên main cuối ⇒ (e) sao lưu ổ D + mời User test MỘT lần ⇒ sửa lỗi buổi test ⇒ deploy (bước 7).
- Không làm trước khi đóng (đã ghi giới hạn — runbook mục 10): xem `HIEN_TRANG.md` mục 4 gạch "GHI GIỚI HẠN". Nhờ User, không chặn: ~20 câu tự gõ vào `data/kich_ban_pho_thong_2026-11-19/CAU_CUA_USER.md`.
- Chưa ai kiểm: chữ của mục web ở 9 kịch bản "kho từ chối, mục web có nội dung"; sáu gợi ý lịch model tự viết bằng chữ (đã được chấm "xong", chưa đối chiếu nguồn).

## 2. Cờ `nho_ten_goi_y` — hỏi tiếp "kể hết các chỗ vừa nêu" có lúc ra danh sách thiếu (thấy 22:32 19/11; B)
- Bằng chứng: một kịch bản "kể hết… trong bài đó" chạy lại × 3 mỗi bên: kể đủ BẬT 1 / 3 · TẮT 2 / 3; một lượt BẬT chỉ kể đúng ba nơi có trong dòng ghi chú (model coi ghi chú là danh sách đủ). Hồ sơ `data/kich_ban_pho_thong_2026-11-19/luot_2/kiem_P07/`. Cờ GIỮ BẬT (nói chắc sai nơi 8 lượt ⇒ 0 vẫn là lợi lớn hơn); dòng giới hạn runbook 10.1: B soạn trong nhánh kết phiên.
- Bước kế: B đề xuất sửa nhỏ nhất (ghi ở `STATUS_B.md`) ⇒ plan mức nhẹ, A duyệt ⇒ bộ dò do người khác soạn ⇒ đo: kịch bản đó × 3 mỗi bên + bộ 17 chuỗi đích không tụt (md5 `4e45408521db`) ⇒ đạt thì gộp (đổi hành vi nhỏ của cờ đã bật: báo User, không hỏi lại) ⇒ rồi mới gửi soát khác hãng.

## 3. Cách làm việc theo thư mục từng ngày (User giao 19/11) [đang thử — ngày 1 / 3]
- Đã có: `report_agent/2026-11-19/` · trang này · `STATUS_<X>.md` ghi đè theo khuôn bảy mục · `scripts/mo_ngay.sh` · `CURRENT_HANDOFF.md` cắt còn khối trỏ (bản cũ nguyên văn: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-19.md`, đã `cmp`).
- Bước kế: E sửa `guides/CACH_LAM_VIEC.md` + `guides/khung/` sau khi thử đủ 3 ngày; ghi hai con số của ngày + số dòng mỗi phiên đọc lúc mở vào `SO_CAI_TIEN_CACH_LAM.md`.

## 4. Nhánh hồ sơ không gộp + việc dọn cần User (lệnh `!`, không gấp)
- Hồ sơ: `origin/p9-c-lich-tien-ve` `10aadc2` (tổng tiền vé do code — không đạt) · `origin/p9-c-s09-luu-y-an-toan` `2d613ce` (bản lời dặn — không đạt) · `origin/p9-e-chi-sang-len-ke-hoach` `d0249b1` (câu cố định khi gõ "lên lịch" — lỗi không còn tái hiện).
- Nhánh CỤC BỘ `p9-b-nho-ten-goi-y` còn một commit có một câu của bộ 80 kịch bản (bản trên origin User đã xoá): đề nghị User `! git -C /home/minhhieu/hue_rag branch -D p9-b-nho-ten-goi-y`. Các nhánh đã gộp trên origin: danh sách ở báo cáo kết phiên của A.
