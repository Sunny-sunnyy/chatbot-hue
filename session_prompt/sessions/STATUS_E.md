# STATUS E — GHI ĐÈ theo khuôn bảy mục (kết phiên nhẹ 11:19 19/11/2026, `date`) · vai người kiểm / người đặt tiêu chí

Bản cũ nguyên văn (tới 11:16 19/11): `session_prompt/archive/STATUS_E_LICH_SU_2026-11-18_19.md` (`cmp` giống nhau lúc chép). Cả bốn phiên được tắt / bật lại ~11:28 19/11 — phiên E mới đợi tin tên terminal của A mới, trả lời MỘT tin.

1. **Đang dở:** bộ kịch bản "việc phổ thông" bản đầu — riêng tư `data/kich_ban_pho_thong_2026-11-19/` (đọc mục "Trạng thái" cuối `README.md` ở đó trước): `PLAN.md` sha256 đầu `b16eb85e65e6`, `bo_kich_ban.jsonl` `6a8db610054e` (80 kịch bản / 106 lượt). Đã sửa theo trả lời của B. Không nhánh, không worktree. Bước kế: mục lục việc, việc 2.
2. **Đã soạn / đã review chưa gộp:** không.
3. **Việc kế:** báo A mới hai sha trên để A ghi duyệt. Xong khi: A duyệt sha và xếp lượt máy cho B (sau bậc 1 thí nghiệm mức suy luận). Lệnh kiểm sha: `sha256sum data/kich_ban_pho_thong_2026-11-19/PLAN.md data/kich_ban_pho_thong_2026-11-19/bo_kich_ban.jsonl`.
4. **Ai chờ mình ↔ mình chờ ai:** A chờ hai sha cuối · sau lượt đo, B và C chấm, E phân xử chỗ hai phiếu lệch · thí nghiệm mức suy luận (việc 1): E đặt tiêu chí (plan `eb0a43776125` đã duyệt), B chạy, C đọc tay.
5. **Câu treo:** E không có câu nào đang chờ User. File câu thật của User cho bộ kịch bản còn trống (A nhờ User điền; có thì thay vào kịch bản E tự viết, giữ 80).
6. **Thứ đang chạy / rác:** không tiến trình, không container, không worktree của E.
7. **Bẫy phiên này:** sổ này từng phình tới 74 KB vì nối thay vì ghi đè · viết sẵn phần "giữ kín 1 / 3" của bộ kịch bản rồi phải gộp lại khi User nhắc không làm quá tay · thêm chữ vào trang có trần byte rồi mới đo ⇒ đo `wc -c` sau mỗi lần thêm · `scripts/grep_kb.sh` chỉ nhận cờ rời (`-l -i`), không che stderr — số 0 hàng loạt là lệnh hỏng · ước tiền lượt đo cao gấp 3–6 lần số thật vì lấy ngưỡng dừng thay cho tiền thật mỗi lượt ⇒ hỏi người chạy số thật trước. Tiền API của E hôm nay: 0 USD. Nhật ký: `report_agent/2026-11-19/e_nhat_ky.md`.
