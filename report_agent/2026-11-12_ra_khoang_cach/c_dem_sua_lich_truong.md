# Đếm trước — sửa lịch bằng lời đổi ngày đi / hạng sao (C, 12:51 15/11/2026)

A nhận làm ứng viên 15/11. Đếm 10 câu **tự đặt** (không đo nhu cầu thật: log không lưu chữ — B nói đúng) trên một lịch thật 3 ngày có ngày đi + hạng sao "vừa". Gọi đúng lần "hiểu ý sửa" của hệ thống đang chạy + `sl.ap` (`data/sua_lich_truong_2026-11-15/tools/dem.py`, `dem_2012.py`). Tiền **0,0012 USD**.

| Loại câu | Lượt | Lần hiểu ý trả | Người dùng thấy |
|---|---|---|---|
| Đổi hạng sao (4 câu + 1 câu kèm ngày) | 5 | rỗng 5 / 5 | đi đường hỏi đáp thường; lịch không đổi, không có dòng "Chưa làm" |
| Đổi ngày đi (5 câu khác nhau) | 5 | rỗng 4 · **sai 1** | câu "đi từ ngày 20/12" ⇒ hành động **đổi số ngày 3 ⇒ 1**, code áp, báo "Đã đổi số ngày: 3 ngày → 1 ngày" |
| Lặp lại câu "đi từ (ngày) 20/12" | 8 | rỗng 6 · "đổi số ngày" không kèm số 2 | lịch không đổi; lượt sửa không có dòng nào |

**Đọc:**
- **Lỗi thật:** câu đổi ngày đi có thể bị hiểu thành đổi **số ngày** (1 / 1 lượt đầu, 0 / 8 lần lặp sau làm sai số ngày nhưng 2 / 8 ra hành động rỗng). Model đọc "20/12" thành số ⇒ lịch đổi sai mà vẫn báo "Đã đổi". Hiếm, nhưng là kiểu lỗi tệ: làm sai mà nói đã làm.
- Hai trường còn lại không sửa được, và hệ thống không nói "chưa làm được", mà lặng lẽ trả lời như một câu hỏi thường.
- **Không có số nhu cầu thật.** Việc này xây theo khoảng trống (3 / 8 trường biểu mẫu) + 1 lỗi làm sai, không theo lỗi người dùng đã gặp.

**Đề xuất (theo phản biện B):**
1. Bậc 1 — **hạng sao**: `doi_tham_so` thêm `ngan_sach`. Code chỉ ghi vào `tham_so`; đường giữ mức qua `sl.ap` đã có. "Rẻ hơn / sang hơn" mơ hồ ⇒ "Chưa làm", không đoán mức.
2. Bậc 2 — **ngày đi**:
   - code tính ngày từ chữ bằng công cụ ngày sẵn có (model chỉ trích cụm ngày);
   - lấy lại dự báo mưa; kiểm giới hạn ngày;
   - **chặn lỗi trên**: câu có cụm ngày ⇒ không nhận hành động "đổi số ngày" thiếu số.
3. Đo mỗi bậc (đổi schema đầu ra hiểu ý, chạy ở mọi câu trong cuộc có lịch): Q3 đã thấy + kín, **Q5 an toàn 0 / 64**, bộ trộn sửa + khẩn cấp 0 / 16. Ước ≈ 0,1–0,25 USD mỗi bậc.
