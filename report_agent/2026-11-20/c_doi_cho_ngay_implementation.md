# C — sửa lịch bằng lời "đổi chỗ ngày 1 với ngày 2": code + test + đếm (nhánh `p9-c-doi-cho-ngay`; plan đã duyệt `c_doi_cho_ngay_plan.md` `03b40a5`)

Ghi 16:30 20/11/2026 (giờ `date`). Cờ `sua_lich_doi_cho_ngay` mặc định **TẮT**. Tiền: 0 USD. CHƯA có: bộ dò độc lập cho hàm đọc câu, review nhánh, lượt thật qua giao diện.

**1. Người dùng thấy gì khác (khi cờ bật).** Trong cuộc đã có lịch, gõ "đổi chỗ ngày 1 với ngày 3" ⇒ thẻ lịch đổi các điểm buổi sáng và chiều của hai ngày đó cho nhau, kèm dòng
"Đã đổi chỗ các điểm buổi sáng và chiều của ngày 1 với ngày 3; hoạt động buổi tối giữ theo từng ngày." Không đổi được ⇒ lịch giữ nguyên và có dòng nói lý do
(ví dụ "… vì ngày 1 sẽ có điểm ở khu xa trung tâm, mà lịch không xếp khu xa vào ngày đầu"). Câu gộp / tách ngày, câu kèm ý sửa khác, câu nói vòng ⇒ vẫn dòng "Chưa làm" như hôm nay.

**2. Đã sửa.** `backend/llm/sua_lich_v2.py` (hàm đọc câu `cap_ngay_doi_cho` theo danh sách cho phép; `doi_cho_ngay` hoán đổi rồi đi đúng đường xếp-rồi-kiểm; hai câu lý do riêng;
một nhánh trong `thay_doi` và `_cau_khong_doi`) · `backend/llm/len_ke_hoach.py` (+7 dòng ở chỗ đang gắn dòng "Chưa làm") · `assistant.py` + `settings.yaml` (cờ) · test ·
`guides/RUNBOOK_BAN_GIAO.md`: dòng của việc này + BỐN dòng của mục "hẹn sau lượt đo cuối" đổi thành "giữ giới hạn (20/11)" kèm số đếm (phiên điều phối chốt).
Không đổi lời dặn, không đổi khuôn hành động gửi model.

**3. Bằng chứng [máy kiểm; chưa có người thứ hai].**
- Đếm mở rộng bằng hàm thật của nhánh (script riêng tư `data/doi_cho_ngay_2026-11-20/dem_mo_rong_C.py`): mọi tổ hợp nút biểu mẫu lịch 2–5 ngày × 4 kiểu ngày đi (không nêu · giữa tuần khô ·
  cuối tuần · trong 7 ngày có mưa 80 %) × mọi cặp ngày = **15.360 cặp**: đổi được **13.831 (90 %)**; bị chặn 1.529 — 1.346 vì điểm khu xa rơi vào ngày 1, 183 (chỉ ở lịch có ngày đi / mưa) ra câu lý do
  chung; **0 lỗi văng**; đổi lại lần hai luôn về đúng lịch cũ; 516 cặp (3,7 % số đổi được) bộ xếp đổi THÊM ngoài phần được nhờ ⇒ có dòng "Ngoài phần đổi chỗ, lịch xếp lại thêm: …".
- Điều đếm mới thấy, lệch với plan: buổi TỐI KHÔNG đi theo phần đổi chỗ (bộ xếp dựng buổi tối theo từng ngày) ⇒ dòng báo nói rõ "buổi tối giữ theo từng ngày" thay vì coi đó là "đổi thêm".
  Và lý do chặn phổ biến không phải "hai khu không liền nhau" mà là luật "khu xa không xếp vào ngày 1" ⇒ viết câu lý do riêng cho đúng.
- Test `tests/test_doi_cho_ngay.py` 23 đạt (đọc câu 5 nhận / 11 không · đổi xong mỗi điểm sang đúng ngày kia cùng buổi, đổi hai lần về lịch cũ, bản lưu truyền vào không bị sửa · ca bị chặn thật
  và ca dựng · nối vào luồng sửa: cờ bật ⇒ đổi, cờ tắt ⇒ dòng "Chưa làm" cũ, lượt có ý khác / câu gộp ⇒ như cũ). Ca nối vào luồng ĐỎ khi vô hiệu dòng gọi (1 hỏng / 22 đạt).
- File chạm: `test_rao_so_ngay` 44 · `test_sua_lich_v2` 13 · `test_b5_lich_trinh` 245 · `test_len_ke_hoach_v2` 93 · `test_settings_env` 6 — đều đạt.

**4. Chưa làm / giới hạn.** [chưa đo trên đường thật]: thẻ lịch, nhãn "Đã sửa theo lời bạn", file tải về, hỏi tiếp trên lịch mới — chưa có lượt nào · hàm đọc câu CHƯA qua bộ dò của phiên khác ·
lượt chỉ tới được hàm này khi MODEL đã nhận câu là câu sửa (trả "chưa hỗ trợ" hoặc hành động bị rào) — model trả rỗng thì câu đi đường hỏi đáp thường như hôm nay; tỉ lệ đó chưa đo ·
183 ca bị chặn ở lịch có ngày đi chỉ có câu lý do chung · bữa ăn / chỗ ở do bước sau dựng lại theo khung mới — chưa nhìn trên giao diện · cả bộ test chưa chạy (một lượt cuối đợt).

**5. Cách thử trong 2 phút (sau khi bật cờ + mở server).** Trang Lên kế hoạch: lập lịch 3 ngày ⇒ gõ "đổi chỗ ngày 2 với ngày 3" ⇒ hai ngày đổi nội dung ban ngày, có dòng "Đã đổi chỗ…";
gõ tiếp "gộp ngày 1 với ngày 2" ⇒ vẫn dòng "Chưa làm".

| Đã làm | Chưa làm | Tự hoãn + lý do | Lệnh kiểm + đầu ra |
|---|---|---|---|
| hàm đọc câu + hoán đổi + nối luồng sửa + cờ tắt + test + đếm 15.360 cặp + năm dòng runbook | bộ dò của phiên khác; review; lượt thật; bật cờ | lượt thật chờ lượt bật server chung | `cd backend && uv run pytest tests/test_doi_cho_ngay.py -q` ⇒ `23 passed` |
