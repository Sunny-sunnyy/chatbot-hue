# Plan một trang — dời một điểm bị từ chối: nói đúng lý do + gợi ý chỗ dời ĐƯỢC (E viết 15:31 20/11/2026, giờ `date`; chờ phiên điều phối duyệt)

**Từ dùng:** *khu* = cụm điểm gần nhau (mã `cum` trong bảng điểm) · *đổi chỗ* = luật có sẵn: buổi đích có đúng một điểm thì hai điểm đổi chỗ cho nhau · *mốc* = phép đếm chiều 20/11 trên bốn kiểu lịch, dời được 24 / 176 (script riêng tư `data/test_cuoi/tools/dem_doi_buoi_2026-11-20.py`).

**1. Người dùng thấy gì — trước ↔ sau** (lịch 3 ngày · cân bằng · di tích; lịch KHÔNG đổi ở lượt bị từ chối, như bây giờ)
- Trước, mọi ca một câu: "Không đổi được: X đặt ở chỗ đó sẽ làm lịch phạm luật xếp (giờ mở cửa / cụm xa / quá dày) nên mình chưa đổi."
- Sau, ca 1 — Phố cổ Bao Vinh (sáng ngày 3) ⇒ chiều ngày 1: "Không đổi được: Phố cổ và chợ Bao Vinh chưa dời sang buổi chiều ngày 1 được vì lịch sẽ có buổi quá kín hoặc quá giờ. Dời được sang: buổi sáng ngày 1 (đổi chỗ với Đại Nội Huế)."
- Sau, ca 2 — Bao Vinh ⇒ chiều ngày 2: "… vì một ngày sẽ phải đi hai khu không liền nhau. Dời được sang: buổi sáng ngày 1 (đổi chỗ với Đại Nội Huế)."
- Sau, ca 3 — Chùa Thiên Mụ (chiều ngày 1) ⇒ sáng ngày 1: "… vì lịch sẽ có buổi quá kín hoặc quá giờ. Trong lịch này Chùa Thiên Mụ chỉ đứng được ở chỗ hiện tại."

**2. Cách làm** (chỉ `backend/llm/sua_lich_v2.py`, nhánh `doi_buoi` của hàm `ap`, điểm ĐANG ở trong lịch; ước ~35 dòng)
- Tách phép thử một chỗ đích (giữ mọi điểm khác, đổi chỗ khi đích có đúng một điểm, xếp, kiểm luật) thành một hàm con dùng CHUNG cho lần dời thật và cho gợi ý ⇒ gợi ý nào cũng là chỗ mà chính đường dời thật nhận.
- Bị từ chối ⇒ lấy mã luật của `kiem_khung_v2` trên khung thử, quy về MỘT lý do theo thứ tự: có mã khu (`cum_khong_ke`, `qua_2_cum`, `ghep_khong_ke`, `cum_xa`) ⇒ "hai khu không liền nhau" · không thì có mã kín / giờ (`qua_day_buoi`, `vuot_quy`, `sang_chong_chieu`, `gio_chong`) ⇒ "quá kín hoặc quá giờ" · chỉ `ngoai_gio_mo` ⇒ "rơi ngoài giờ mở cửa" · không mã nào ⇒ giữ câu cũ. Câu nói ở mức CẢ LỊCH ("lịch sẽ có buổi…", "một ngày sẽ…") vì bộ kiểm không cho biết lỗi nằm ở ngày nào (có thể ở ngày của điểm bị đổi chỗ).
- Gợi ý: thử mọi (ngày, buổi) khác chỗ đang đứng mà điểm đi được buổi đó (≤ 9 lần xếp, mỗi lần dưới 1 ms theo phép đếm mốc); ghi kèm tên điểm sẽ đổi chỗ.
- Mục `khong_doi` giữ `ma_luat = "khong_hop_luat"` (nhãn bộ đo và log không đổi), thêm ba trường `ly_do`, `dich`, `goi_y`; câu do `thay_doi` viết từ ba trường đó. KHÔNG đụng: `kiem_khung_v2`, luật xếp, ca dời được, `them_diem`, lời dặn model, giao diện (dòng chữ hiện ở khối "Không đổi được" có sẵn).

**3. Xong khi (ghi trước)** — chạy lại script mốc trên nhánh, in ra:
- a. dời được vẫn **24 / 176**, và 24 khung đó giống từng byte khung của main;
- b. **152 / 152** ca từ chối: lịch trả về = bản đã lưu; có `ly_do` (đếm theo ba lý do; "giữ câu cũ" phải 0 — khác 0 thì báo số, không sửa cho đẹp);
- c. mọi gợi ý đem áp lại bằng `ap` ⇒ dời ĐƯỢC đúng (ngày, buổi) đó: **100 %**; ca câu nói "chỉ đứng được ở chỗ hiện tại" ⇒ phép đếm mốc cũng ra 0 chỗ dời được cho điểm đó;
- d. test mới trong `backend/tests/test_sua_lich_v2.py` ĐỎ trên code cũ, xanh sau; bốn file `test_sua_lich_v2`, `test_len_ke_hoach_v2`, `test_b5_lich_trinh`, `test_rao_so_ngay` đạt (Python 3.13 của cây chính).

**4. Chưa làm ở nhánh này / giới hạn biết trước**
- Lượt thật qua giao diện (model + trình duyệt): gộp vào lượt bật server chung do phiên điều phối báo. Cả bộ test: một lượt cuối đợt.
- Tỉ lệ dời được KHÔNG tăng (vẫn 14 %) — bản này chỉ làm câu từ chối có ích; nới luật hay thêm đường lui là việc khác, chưa ai giao.
- Một lý do cho mỗi ca: ca dính cả khu lẫn kín (60 / 152 ở mốc) chỉ nói lý do khu. `them_diem` và điểm chưa có trong lịch giữ câu cũ.
- Câu dài hơn khi có nhiều gợi ý (lịch nhẹ nhàng: tới 4 chỗ) — không cắt.
