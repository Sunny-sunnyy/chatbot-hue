# Review — nhánh `p9-diem-v9` (bảng điểm lịch v9, 7 nơi mới) · người kiểm B · 15:41 15/11/2026

Người làm: E. Bản kiểm: origin `7cab458` (chứa `main` mới nhất). Report: `e_diem_v9_implementation.md` (trên nhánh). 0 USD (chỉ đọc + chạy lại công cụ 0 USD; không chạy lại lượt có phí).

**Kết luận: `ready_for_user_confirmation` — 0 blocker / 0 major / 3 minor.** m-1, m-2 mỗi cái ≤ 2 dòng ⇒ E sửa, A kiểm bằng grep / diff rồi merge (không cần vòng 2).

## Đã kiểm (cổng tối thiểu + theo rủi ro)

| Điểm kiểm | Cách B kiểm (khác cách E) | Kết quả |
|---|---|---|
| Git / phạm vi | `git diff origin/main...` 13 file; `git diff --check` | đúng phạm vi report; `settings.yaml` chỉ 3 đường bảng; sạch |
| Bảng v9 = v8 + 7 | so từng điểm v8 ↔ v9 bằng script riêng; md5 3 bảng | 34 điểm cũ **giống hệt**; 7 điểm mới đủ cột như điểm cũ; md5 khớp report; bảng ảnh v2 ↔ v4: 33 dòng cũ giống hệt, +6 |
| Mô phỏng 3.840 khung | script riêng `/tmp/b_rv9_tools/tinh_lai.py` (tự đi qua khung, không dùng `diem_ban_ngay`) | v9: ẩm thực **44,0 %** · chụp ảnh **36,8 %** · thiên nhiên **17,6 %** · di tích 0 % · **0 lỗi kiểm khung**; v8 ra đúng 56,4 / 51,7 / 24,4 — khớp |
| Ngoại lệ test đơn điệu (A duyệt) | cùng script, đếm trên 320 và 1.280 tổ hợp | v8: 0 / 0. v9: **1 / 320** và **4 / 1.280**, cùng một tổ hợp (3 ngày · không hạn chế · chỉ "chụp ảnh": 9 / 12 / 10, ngày cụm xa 0 / 0 / 1). Điều kiện trong test là so chặt `xa[2] > xa[1]`, vế "nhẹ nhàng ≤ cân bằng" giữ nguyên, trần 6 ngoại lệ ⇒ đúng điều A duyệt, không nới rộng hơn. `pytest -s` in "1 / 320". (Lưới 1.280 có ngày đi không nằm trong test — chỉ script của B / E đếm.) |
| Khung toạ độ 108,25 | đọc 7 toạ độ mới; test 2 điểm; tìm chỗ khác dùng khung cũ | server: đúng, 2 ca test đạt, ca toạ độ sai cũ vẫn chặn. **Phía trình duyệt còn khung cũ ⇒ m-1** |
| `kiem_cau` "chỉ có mã nguồn = rỗng" | 7 câu biên tự đặt | chỉ đổi kết quả với câu **không còn chữ / số nào** sau khi bỏ mã nguồn (trước: lọt hoặc "không mã" ⇒ nay "rỗng", đều ra câu dự phòng); câu có chữ + mã vẫn đạt như cũ. Bất biến giữ: câu hợp lệ không bị chặn thêm |
| 3 ghi chú ăn (chữ người dùng thấy) | `scripts/grep_kb.sh` hai bài kho | Lập An (2 câu): có căn cứ (mục nhà hàng ven đầm + mục ẩm thực hàu). Hải Vân: **một chữ suy luận ⇒ m-2** |
| 7 đoạn mô tả | đọc qua Qdrant (chỉ đọc) theo `chunk_id` | cả 7 có trong chỉ mục, đều là đoạn tả nơi (4 đoạn gắn lại không còn là dòng một ý). Ghi nhận: 3 đoạn có nhắc tên một điểm khác của bảng ⇒ câu model lặp tên đó sẽ thành câu dự phòng (luật sẵn có); lượt thật của E 0 dự phòng ở các điểm này ⇒ không phải finding |
| 6 ảnh (luật chọn ảnh) | B nhìn cả 6 | 5 ảnh tự nhận ra nơi / có biển tên / chú thích tác giả đúng tên; không trẻ em, không mặt người rõ, không số điện thoại. Ảnh Hải Vân ⇒ **m-3** |
| Test | 3 file chạm trên worktree tách | 119 đạt; 1 trượt = test CSP đòi bản build giao diện (worktree của B không build) — không do nhánh |
| Report tracked | đọc cả file | không chép câu kho / tên + địa chỉ; hook 0 trùng |

## Finding

- **m-1 (minor, tiềm ẩn — cờ `ban_do_lich` đang tắt):** `frontend/src/toaDo.js` dòng 4 vẫn kiểm kinh độ ≤ 108, trong khi chú thích file ghi "như server". Bật bản đồ sau này ⇒ Hải Vân và Lập An bị coi là "chưa có trên bản đồ" mà không báo lỗi. *Đóng:* đổi cận trên thành 108.25 (1 dòng) cho khớp `KHUNG_HUE`.
- **m-2 (minor, chữ người dùng thấy):** ghi chú bữa trưa ở đèo mở đầu bằng "Gần nhất là…". Kho không nói gì về chỗ ăn trên đèo (grep bài đèo: 0 dòng về quán / ăn uống) ⇒ "gần nhất" là suy luận của người viết, không phải điều kho nêu. *Đóng:* bỏ hai chữ đó, giữ phần kho có (chân đèo phía bắc là Lăng Cô; ven đầm có nhà hàng).
- **m-3 (minor, không chặn merge):** ảnh điểm đèo là đoàn tàu trên sườn núi. Đạt luật nhờ tên file của tác giả, nhưng lịch đưa người dùng lên đèo bằng đường bộ / cửa ải, ảnh không cho thấy thứ họ sẽ đến. *Đóng:* thay khi có ảnh cửa ải hoặc cung đèo đạt luật; chưa có thì giữ, ghi vào danh sách ảnh cần tìm.

## Giới hạn của lượt review

Không chạy lại 28 lượt có phí của E (đọc số đếm trong report, không đọc lại từng câu model); không khởi động server nhánh (E đã làm, test nạp bảng thật đạt); không Playwright (đúng luật: nhánh chỉ đổi ảnh + dữ liệu bảng). Việc sau merge E đã ghi: danh sách file bản deploy nháp đổi sang 3 bảng mới.
