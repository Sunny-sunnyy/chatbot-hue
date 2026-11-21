# Plan (một trang) — sửa lịch bằng lời: "đổi chỗ ngày 1 với ngày 2" (C, 16:14 20/11/2026, giờ `date`; nền main `9fee16a2`; CHỜ phiên điều phối duyệt — chưa viết code sản phẩm, 0 USD)

**Điều đã chốt:** `guides/RUNBOOK_BAN_GIAO.md` mục 10.2, dòng "Đổi chỗ ngày 1 với ngày 2": chủ dự án chọn chặn lịch giả trước, làm hành động đổi chỗ hai ngày "sau lượt so sánh cuối".
**Hôm nay người dùng thấy gì:** gõ câu đó trong cuộc đã có lịch ⇒ khối thay đổi ghi "Chưa làm: đổi chỗ, gộp hay tách các ngày…" (`backend/llm/sua_lich_v2.py:55`), lịch giữ nguyên.
Chỗ quyết: `backend/llm/len_ke_hoach.py:279` — sau khi MODEL đã nhận câu là câu sửa, hàm `la_viec_ngay_chua_lam` (code đọc câu) gắn dòng "Chưa làm".

**Phép đếm 0 USD trước khi xây** (C chạy hàm xếp thật; script riêng tư `data/doi_cho_ngay_2026-11-20/dem_doi_cho_ngay_C.py`; chưa ai tính lại):
bốn kiểu lịch của phiên E (3 ngày cân bằng · 2 ngày cân bằng · 3 ngày nhẹ nhàng · 4 ngày khám phá) × ba kiểu ngày đi (không nêu · đi thứ Tư 07/04/2027 · đi thứ Bảy 21/11/2026),
hoán đổi MỌI cặp ngày, giữ nguyên buổi của từng điểm rồi cho bộ xếp + bộ kiểm luật chạy lại: **39 / 39 cặp hợp luật, mọi điểm giữ đúng chỗ sau hoán đổi.**
Nghĩa là: luật xếp hầu hết tính TRONG từng ngày (cụm, độ dày, giờ mở cửa) nên đổi nguyên hai ngày gần như luôn làm được — khác hẳn "dời một điểm" (24 / 176).
Chưa đếm: lịch có dự báo MƯA (chỉ có khi ngày đi nằm trong 7 ngày tới) và ngày một điểm đóng cửa theo thứ — hai ca này là nơi hoán đổi có thể bị chặn; bước 2 dưới đếm thêm.

**Bản NHỎ NHẤT (không gộp / tách ngày, không đổi lời dặn, không đổi khuôn hành động của model):**
1. Hàm thuần đọc câu `cap_ngay_doi_cho(cau, so_ngay) -> (a, b) | None` trong `sua_lich_v2.py`, theo DANH SÁCH CHO PHÉP như hàm đọc câu "dời hai điểm" đang chạy: câu phải có một động từ
   đổi chỗ (đổi chỗ, hoán đổi, tráo, đảo) + ĐÚNG hai mốc ngày khác nhau ("ngày 1", "ngày đầu", "ngày cuối", ≤ số ngày của lịch) + vài từ đệm; có tên một điểm của lịch, có chữ gộp / tách,
   hoặc chữ lạ ⇒ None ⇒ giữ đúng dòng "Chưa làm" hôm nay (từ chối nhầm được phép, áp sai thì không).
2. Hàm thuần `doi_cho_ngay(bang, luu, a, b)`: lấy vị trí mọi điểm ban ngày, đổi số ngày a ↔ b, giữ buổi, gọi đúng đường xếp-rồi-kiểm đang dùng cho mọi sửa (`_thu_giu`).
   Hợp luật ⇒ khung mới + dòng "Đã đổi chỗ ngày a với ngày b". Phạm luật ⇒ lịch giữ nguyên + dòng "Không đổi được" kèm lý do quy từ mã luật bằng CHÍNH bảng lý do phiên E đã đưa vào main
   (khu xa / buổi đã kín / ngoài giờ mở cửa).
3. Chỗ gắn: `len_ke_hoach.py:279` — `la_viec_ngay_chua_lam` đúng VÀ bước 1 đọc ra cặp ngày ⇒ gọi bước 2 thay cho dòng "Chưa làm". Phần sau (lưu lịch, thẻ lịch, file tải, câu an toàn
   thừa hưởng) đi đường của mọi lượt sửa làm được. Cờ `sua_lich_doi_cho_ngay`, mặc định TẮT; cờ tắt ⇒ y như hôm nay; chuỗi gửi model không đổi ở cả hai trạng thái.

**Tiêu chí ghi TRƯỚC:**
- Test hàm thuần (có ca đỏ trước): đổi chỗ xong mỗi điểm nằm đúng ngày kia, cùng buổi · đổi hai lần ⇒ về đúng lịch cũ · câu không khớp ⇒ None · ca phạm luật dựng bằng bảng ⇒ lịch
  giữ nguyên + dòng có lý do · một ca có câu an toàn thừa hưởng (bài học 20/11: sửa chỗ GHI trạng thái thì liệt kê thứ đi theo lần ghi đó).
- Đếm 0 USD mở rộng: mọi tổ hợp nút biểu mẫu (960 khung) × mọi cặp ngày + ba kiểu ngày đi + một ngày có mưa ⇒ ghi số cặp hợp luật / tổng; ca bị chặn phải ra đúng dòng "Không đổi được", 0 ca văng lỗi.
- Bộ dò nhỏ của phiên khác cho hàm đọc câu: 10 phải đọc + 10 giống-mà-không-phải (đổi chỗ HAI ĐIỂM, đổi ngày đi, đổi chỗ ở, gộp ngày); sàn: đọc nhầm 0 / 10.
- MỘT lượt thật qua giao diện (≈ 4 lượt, ≈ 0,01 USD, ở lượt bật server chung): lập lịch 3 ngày ⇒ "đổi chỗ ngày 1 với ngày 3" ⇒ thẻ lịch đổi đúng, nhãn "Đã sửa theo lời bạn";
  hỏi tiếp "ngày 1 đi những đâu" ⇒ trả theo lịch mới; file tải về theo lịch mới. Không đạt ⇒ cờ TẮT, báo phiên điều phối.
- File test chạm: `test_sua_lich_v2`, `test_len_ke_hoach_v2`, `test_b5_lich_trinh`, `test_rao_so_ngay`. Cả bộ test: một lượt cuối đợt.

**Không làm:** gộp / tách ngày (vẫn "Chưa làm") · đổi chỗ hai BUỔI của một ngày · hiểu câu nói vòng ("cho ngày đi lăng lên trước") · đổi lời dặn để model tự ra hành động này.
**Rủi ro / chỗ C chưa biết:** (1) buổi TỐI, bữa ăn, chỗ ở do bộ xếp dựng lại theo ngày ⇒ sau hoán đổi có thể đổi quán / hoạt động tối (phố đi bộ chỉ tối cuối tuần) — đúng luật nhưng người dùng
thấy "đổi nhiều hơn mình nhờ" ⇒ dòng báo phải nói rõ; đếm ở bước đếm mở rộng. (2) Lịch có ngày đi: thứ trong tuần của từng ngày đổi theo ⇒ điểm đóng cửa theo thứ sẽ chặn — đúng, cần lý do rõ.
(3) Hàm đọc câu là code đọc chữ người dùng — bài học [18] hôm nay: bộ câu "giống-mà-không-phải" tự viết dễ thiếu kiểu ⇒ bộ dò của phiên khác là bắt buộc.
**Cỡ:** ước ~40 dòng code + test; không file mới. **Ý C:** đáng làm — rẻ, 39 / 39 cặp làm được, và là việc chủ dự án đã hẹn làm.
